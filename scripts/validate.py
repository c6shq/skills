#!/usr/bin/env python3
"""Validate c6s plugin packaging and security boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "c6s"
EXPECTED_SKILLS = {"setup", "find", "organize", "request", "run"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    mcp = load_json(PLUGIN / ".mcp.json")["mcpServers"]["c6s"]

    assert codex["name"] == claude["name"] == "c6s"
    assert codex["version"] == claude["version"] == "0.1.7"
    assert codex_marketplace["name"] == claude_marketplace["name"] == "c6s-skills"
    assert codex_marketplace["plugins"][0]["source"]["path"] == "./plugins/c6s"
    assert claude_marketplace["plugins"][0]["version"] == codex["version"]
    assert mcp == {
        "command": "c6s",
        "args": ["mcp"],
        "enabled": False,
        "env_vars": ["PATH"],
        "startup_timeout_sec": 10,
        "tool_timeout_sec": 120,
    }

    skill_directories = {
        path.name for path in (PLUGIN / "skills").iterdir() if path.is_dir()
    }
    assert skill_directories == EXPECTED_SKILLS
    assert "approve" not in skill_directories
    for name in EXPECTED_SKILLS:
        skill_text = (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        prompt_text = (PLUGIN / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert f"name: {name}\n" in skill_text
        assert "[TODO:" not in skill_text
        assert f"${name}" in prompt_text

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
