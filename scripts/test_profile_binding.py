#!/usr/bin/env python3
"""Offline synthetic regressions for skill instructions, not live CLI isolation.

The CLI contract was inspected at c6shq/c6s-cli commit
2984c55cc730e07a0dc5ba0eef96d3b01e5a748e: internal/command/run.go,
internal/command/profile_test.go, internal/account/profile.go, and
internal/command/sync.go. No vault, account files, credentials, or CLI are read.
"""

import shlex
import unittest

from validate import (
    PLUGIN,
    PROFILE_DOCUMENTS,
    assert_profile_pinned,
    explicit_profile,
    profile_commands,
    validate_profile_binding,
)


# Deliberately synthetic identifiers. Alias and ID both resolve to one identity,
# as in the CLI, but the documented workflow prefers the immutable ID.
PROFILES = {"profile-work": "work", "profile-personal": "personal"}


def resolve(selector: str) -> str:
    matches = [
        profile_id for profile_id, alias in PROFILES.items()
        if selector == profile_id or selector.lower() == alias.lower()
    ]
    if len(matches) != 1:
        raise ValueError("Unknown or ambiguous synthetic profile")
    return matches[0]


def selected_account(arguments: list[str], environment: str, default: str) -> str:
    return resolve(explicit_profile(arguments) or environment or default)


def accept_returned(command: str, chosen: str) -> str:
    """Model only the documented account-binding gate; never execute the string.

    Real use also needs operation/target/revision/authorization validation. This
    helper intentionally does not claim to implement a safe shell interpreter.
    """
    selector = explicit_profile(shlex.split(command))
    if selector is None or resolve(selector) != chosen:
        raise ValueError("Returned command is not bound to the chosen account")
    return command


class ProfileBindingTests(unittest.TestCase):
    def test_all_documented_examples_are_pinned(self):
        validate_profile_binding()

    def test_examples_ignore_default_and_environment_changes(self):
        checked = 0
        for name in PROFILE_DOCUMENTS:
            text = (PLUGIN / "skills" / name).read_text(encoding="utf-8")
            for arguments in profile_commands(text):
                if explicit_profile(arguments) is None:
                    continue  # Global discovery/help has no account context.
                pinned = ["profile-work" if arg == "PROFILE" else arg for arg in arguments]
                for default in PROFILES:
                    for environment in ("", "personal", "profile-personal", "unknown"):
                        with self.subTest(document=name, argv=arguments, default=default,
                                          environment=environment):
                            self.assertEqual(
                                selected_account(pinned, environment, default), "profile-work"
                            )
                checked += 1
        self.assertGreaterEqual(checked, 14)

    def test_unpinned_regression_reproduces_default_drift(self):
        arguments = ["c6s", "item", "list", "--remote", "--json"]
        self.assertEqual(selected_account(arguments, "", "profile-work"), "profile-work")
        self.assertEqual(selected_account(arguments, "", "profile-personal"), "profile-personal")
        with self.assertRaises(AssertionError):
            assert_profile_pinned(arguments)

    def test_each_example_rejects_removed_or_wrong_profile(self):
        for name in PROFILE_DOCUMENTS:
            text = (PLUGIN / "skills" / name).read_text(encoding="utf-8")
            for arguments in profile_commands(text):
                if explicit_profile(arguments) is None:
                    continue
                index = arguments.index("--profile")
                for broken in (
                    arguments[:index] + arguments[index + 2:],
                    arguments[:index + 1] + ["OTHER"] + arguments[index + 2:],
                ):
                    with self.subTest(argv=broken), self.assertRaises(AssertionError):
                        assert_profile_pinned(broken)

    def test_global_commands_need_no_selector(self):
        for command in ("c6s profile list --json", "c6s version", "c6s help item",
                        "c6s attachment upload --help"):
            assert_profile_pinned(shlex.split(command))
        with self.assertRaises(AssertionError):
            assert_profile_pinned(shlex.split("c6s profile default set work"))
        with self.assertRaises(AssertionError):
            assert_profile_pinned(shlex.split("c6s request create -- echo --help"))

    def test_cli_selector_forms_and_child_boundary(self):
        self.assertEqual(explicit_profile(shlex.split("c6s item list --profile=work")), "work")
        arguments = shlex.split("c6s --profile work request create -- /bin/echo --profile personal")
        self.assertEqual(explicit_profile(arguments), "work")
        self.assertIsNone(explicit_profile(shlex.split("c6s request create -- echo --profile work")))
        for command in ("c6s --profile", "c6s --profile= item list",
                        "c6s --profile work item list --profile=personal"):
            with self.subTest(command=command), self.assertRaises(AssertionError):
                explicit_profile(shlex.split(command))

    def test_returned_commands_fail_closed_without_rewriting(self):
        # Current CLI-generated nextCommands and recovery commands lack selectors.
        # They must stop even if today's shared default happens to be correct.
        operations = (
            "item inspect local-example --json",
            "item inspect remote-example --remote --json",
            "vault reconcile local-example --tombstone-revision 7 --keep-local-as-new --yes",
            "vault resolve local-example --hosted-item-id remote-example --hosted-revision 9 "
            "--keep-remote --preserve-local-as-copy --yes",
        )
        for operation in operations:
            for prefix in ("c6s", "c6s --profile personal", "c6s --profile unknown",
                           "c6s --profile work --profile personal"):
                command = f"{prefix} {operation}"
                with self.subTest(command=command), self.assertRaises((ValueError, AssertionError)):
                    accept_returned(command, "profile-work")
            for selector in ("--profile profile-work", "--profile=work"):
                command = f"c6s {selector} {operation}"
                original = command
                self.assertEqual(accept_returned(command, "profile-work"), original)
        with self.assertRaises(ValueError):
            accept_returned("c6s request create -- echo --profile work", "profile-work")


if __name__ == "__main__":
    unittest.main()
