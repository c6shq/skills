---
name: run
description: Inspect and execute one exact approved c6s action request with a one-time grant and redacted output. Use only for an already approved request; do not create, approve, broaden, or silently retry it.
---

# Run with c6s

Use the exact request ID. Inspect it immediately before execution and verify that it
is approved, unexpired, and matches the action the user intends now: summary,
executable, arguments, working directory, item and field or attachment IDs,
revisions, filenames, and environment destinations.

If the request is pending, rejected, expired, missing, or different from the intended
action, stop. A trusted human-controlled Cerberus app is the only approval surface;
this skill must never obtain or simulate approval.

Execute once with `c6s request execute <request-id> [--json]`. The CLI revalidates
field and private-file eligibility, consumes the short-lived grant atomically,
materializes approved files in a mode-`0600` temporary directory, invokes the
executable without a shell, and removes temporary files after exit. It redacts exact
injected values from bounded stdout and stderr.

For a TOTP request, use the same execution command or `c6s request wait <request-id>
--execute` when the user explicitly asked to wait. c6s may briefly wait out the last
five seconds of a code window before consuming the grant, then derives a fresh code
at process start. The seed and code never belong in output, chat, clipboard, logs, or
manual verification. Do not replace this constrained execution with `item reveal`.

Redaction is not general data-loss prevention: a program can transform or transmit a
secret. Treat the executable and arguments—not just the displayed output—as the
security decision. Do not retry when grant consumption or process start is ambiguous;
inspect state and report the uncertainty. Never reveal the field to verify execution.
