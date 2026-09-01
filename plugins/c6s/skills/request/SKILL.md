---
name: request
description: Prepare and create an exact c6s approval-gated action request using remote field or encrypted-file revisions, process, and environment bindings. Use when protected input needs trusted-device approval; do not approve or execute the request.
---

# Request with c6s

An action request authorizes one exact process intent, not general secret access.
Work only with remote metadata and never resolve the referenced value.

1. Confirm the active account, trusted CLI device, connected remote vault, and the
   user's intended action.
2. For values, use remote item list/inspect to resolve the exact item ID, field ID,
   current revision, and `approved_injection` policy. For private files, use
   `c6s attachment list <item-id> --json` to resolve the exact attachment ID,
   revision, ready state, filename, media type, size, and `approved_injection`
   policy. Stop if any part is ambiguous or ineligible; never export the file.
3. Require an absolute executable path. Do not wrap the command in a shell, add
   unreviewed arguments, or turn a narrow task into arbitrary command execution.
4. Present the summary, executable, every argument, working directory, expiry
   behavior, and each `item:field:revision -> ENV` or
   `item:attachment:revision -> ENV` binding before submission when those details
   were not already explicitly authorized.
5. Create with `c6s request create --summary <text> --inject
   <item>:<field>:<revision>:<ENV> [--cwd <absolute-path>] --
   <absolute-executable> [args...]`. Bind an approved private file path with
   `--inject-file <item>:<attachment>:<revision>:<ENV>`; the request becomes Intent
   V3 and the CLI materializes it only after consuming the one-time grant.
6. Read the returned request back with `c6s request inspect <request-id>` and report
   its state and expiry without secret values.

Do not create duplicate requests after an ambiguous response. Do not approve,
reject, execute, poll indefinitely, or claim that a notification was delivered.
Approval belongs only to the human-controlled trusted Cerberus app.
