#!/usr/bin/env python3
"""Validate c6s plugin packaging and security boundaries."""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "c6s"
EXPECTED_SKILLS = {"setup", "find", "organize", "otp", "request", "run"}
PROFILE_DOCUMENTS = (
    "find/SKILL.md",
    "organize/SKILL.md",
    "find/references/profiles.md",
)


def profile_commands(text: str) -> list[list[str]]:
    """Read documented argv only; never execute a CLI or shell command."""
    return [shlex.split(command) for command in re.findall(r"`(c6s\s+[^`]+)`", text)]


def explicit_profile(arguments: list[str]) -> str | None:
    """Mirror the CLI selector syntax and child-argument boundary for linting."""
    selector = None
    index = 1
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            break
        value = None
        if argument == "--profile":
            index += 1
            assert index < len(arguments), "Missing profile value"
            value = arguments[index].strip()
        elif argument.startswith("--profile="):
            value = argument.removeprefix("--profile=").strip()
        if value is not None:
            assert selector is None, "Duplicate profile selectors"
            assert value, "Empty profile value"
            selector = value
        index += 1
    return selector


def assert_profile_pinned(arguments: list[str]) -> None:
    # These read-only global commands do not select an account. Do not exempt the
    # entire profile namespace: changing the default is not a workflow step.
    if arguments[1:2] in (["help"], ["version"]):
        return
    if arguments[1:] == ["profile", "list", "--json"]:
        return
    if arguments[-1:] == ["--help"] and "--" not in arguments:
        return
    assert explicit_profile(arguments) == "PROFILE", f"Unpinned example: {arguments}"


def validate_profile_binding() -> None:
    for name in PROFILE_DOCUMENTS:
        path = PLUGIN / "skills" / name
        text = path.read_text(encoding="utf-8")
        commands = profile_commands(text)
        assert commands, f"No profile examples found: {path}"
        for arguments in commands:
            assert_profile_pinned(arguments)
    for name in ("find", "organize"):
        text = (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert "references/profiles.md" in text
        assert "shared default" in text
        assert "nextCommands" in text
        assert "stop condition" in text
        assert "do not repair or execute" in text
    guidance = (PLUGIN / "skills/find/references/profiles.md").read_text(encoding="utf-8")
    for guard in (
        "same immutable", "before any `--` boundary", "proceed unchanged",
        "Do not append or replace", "remove revision guards", "channel-local",
        "does not change that local storage boundary", "without a profile selector",
    ):
        assert guard in guidance, f"Missing profile safety guidance: {guard}"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    validate_profile_binding()
    codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    mcp = load_json(PLUGIN / ".mcp.json")["mcpServers"]["c6s"]

    assert codex["name"] == claude["name"] == "c6s"
    assert codex["version"] == claude["version"] == "0.1.21"
    assert codex_marketplace["name"] == claude_marketplace["name"] == "c6s-skills"
    assert codex_marketplace["plugins"][0]["source"]["path"] == "./plugins/c6s"
    assert claude_marketplace["plugins"][0]["version"] == codex["version"]
    assert mcp == {
        "command": "c6s",
        "args": ["mcp"],
        "enabled": False,
        "env_vars": ["PATH", "C6S_PROFILE"],
        "startup_timeout_sec": 10,
        "tool_timeout_sec": 120,
    }

    skill_directories = {
        path.name for path in (PLUGIN / "skills").iterdir() if path.is_dir()
    }
    assert skill_directories == EXPECTED_SKILLS
    assert "approve" not in skill_directories
    setup = (PLUGIN / "skills" / "setup" / "SKILL.md").read_text(encoding="utf-8")
    assert "Do not loop over unlock or OAuth login" in setup
    assert "another terminal" in setup.lower()
    assert "v0.10.2" in setup
    run = (PLUGIN / "skills" / "run" / "SKILL.md").read_text(encoding="utf-8")
    assert "must not end account sign-in" in run
    assert "do not retry" in run.lower()
    assert "outputSuppressed: true" in run
    assert "Do not rerun a payment" in run
    request = (PLUGIN / "skills" / "request" / "SKILL.md").read_text(encoding="utf-8")
    assert "v0.10.4+" in request
    assert "never pad, combine, reveal" in request
    waiting = (PLUGIN / "skills" / "request" / "references" / "waiting.md").read_text(encoding="utf-8")
    assert "request wait REQUEST_ID --timeout 5m --execute --json" in waiting
    assert "resume that handle" in waiting
    assert "executionAttempted: false" in waiting
    assert "do not retry execution" in waiting
    assert "no MCP wait tool or approval callback" in waiting
    assert "../request/references/waiting.md" in run
    assert "references/waiting.md" in request
    otp = (PLUGIN / "skills" / "otp" / "SKILL.md").read_text(encoding="utf-8")
    assert "otp get ITEM_ID --field FIELD_ID --json" in otp
    assert "otpCodePolicy: allow_read" in otp
    assert "Do not change policy" in otp
    assert "Do not issue `otp policy`" in otp
    assert "expiresAt" in otp and "Preserve leading zeroes" in otp
    assert "No OTP MCP result is provided" in otp
    assert "Expiry does not make disclosure harmless" in otp
    assert "c6s:otp" in request and "c6s:otp" in run
    attachments = (PLUGIN / "skills" / "organize" / "references" / "attachments.md").read_text(encoding="utf-8")
    assert "v0.10.5+" in attachments
    assert "attachment policy --resume" in attachments
    assert "--revision CURRENT_REVISION" in attachments
    assert "neither the policy nor journal grants execution" in attachments
    for name in EXPECTED_SKILLS:
        skill_text = (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        prompt_text = (PLUGIN / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert f"name: {name}\n" in skill_text
        assert "[TODO:" not in skill_text
        assert "C6S_CONNECTION" not in skill_text
        assert "agent serve" not in skill_text
        assert f"${name}" in prompt_text

    # An agent must be able to follow every packaged reference after installation.
    for path in (PLUGIN / "skills").rglob("*.md"):
        for href in re.findall(r"\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            link = urlsplit(href)
            if link.scheme or link.netloc or not link.path:
                continue
            target = (path.parent / unquote(link.path)).resolve()
            assert target.is_relative_to(PLUGIN), f"Reference escapes plugin: {path}: {href}"
            assert target.is_file(), f"Missing packaged reference: {path}: {href}"

    repository_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path != Path(__file__).resolve()
    ).lower()
    for forbidden in ("api_key=", "access_token=", "bearer ey", "private_key="):
        assert forbidden not in repository_text

    print("c6s skills packaging and security-boundary checks passed.")


if __name__ == "__main__":
    main()
