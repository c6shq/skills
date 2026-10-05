---
name: request
description: Prepare and create an exact c6s approval-gated action request, and optionally wait for its decision without executing it. Use when protected input needs trusted-device approval; do not approve or execute the request.
---

# Request with c6s

An action request authorizes one exact process intent, not general secret access.
Work only with remote metadata and never resolve the referenced value.

If the user wants a code returned rather than injected, use `c6s:otp` only when the
owner has already enabled direct-code reads. Do not turn an injection request into
a plaintext read or change policy automatically.

For an OTP task, read [OTP routing](../otp/references/routing.md). A denied direct
read can continue as an approval-bound exact process; missing `allow_read` is not
a reason to abandon that route. Browser typing is not process injection. When the
exact task was already authorized, trusted-app approval is the remaining approval;
do not ask for another chat confirmation of the same executable and arguments.

1. Confirm the selected account profile, trusted CLI device, connected remote vault,
   and the user's intended action. Pin `--profile PROFILE` on every command; do not
   change the shared default profile for an agent task.
2. For values, use remote item list/inspect to resolve the exact item ID, field ID,
   current revision, and `approved_injection` policy. For private files, use
   `c6s attachment list <item-id> --json` to resolve the exact attachment ID,
   revision, ready state, filename, media type, size, and `approved_injection`
   policy. Stop if any part is ambiguous or ineligible; never export the file.
   A TOTP reference is the narrow exception to ordinary injection policy: require an
   exact `totp_seed` field classified `secret` with `never_agent`. Never request or
   reveal the seed or return the generated code; request only its injection.
3. Require an absolute executable path. Do not wrap the command in a shell, add
   unreviewed arguments, or turn a narrow task into arbitrary command execution.
4. Present the summary, executable, every argument, working directory, expiry
   behavior, and each `item:field:revision -> ENV` or
   `item:attachment:revision -> ENV` binding before submission when those details
   were not already explicitly authorized.
5. Create with `c6s --profile PROFILE request create --summary <text> --inject
   <item>:<field>:<revision>:<ENV> [--cwd <absolute-path>] --json --
   <absolute-executable> [args...]`. Bind an approved private file path with
   `--inject-file <item>:<attachment>:<revision>:<ENV>`; compatible V4 requests include both timing windows;
   older V3 creators remain supported and the CLI materializes it only after consuming the one-time grant.
   For TOTP use `c6s --profile PROFILE otp request --summary <text> --inject
   <item>:<field>:<revision>:<ENV> --json -- <absolute-executable> [args...]`. No code is
   generated at request time. Tell the user that, after approval, c6s will generate a
   fresh code immediately before the exact process starts and will not return it to
   the agent.
6. Read the returned request back with `c6s --profile PROFILE request inspect
   <request-id> --json` and report its state and expiry without secret values.
7. If asked to stay for approval, use the built-in bounded wait on that same ID and
   profile, not a repeated create/list loop. Read [waiting and handoff](references/waiting.md)
   before waiting. Request-only scope uses `request wait REQUEST_ID
   --json` without `--execute`. If the user already authorized the exact action after
   approval, hand off to `c6s:run` for its wait-and-execute mode; no extra chat approval
   is needed after the trusted app approves that same authorized action.

Do not create duplicate requests after an ambiguous response. Do not approve,
reject, execute, poll indefinitely, or claim that a notification was delivered.
Approval belongs only to the human-controlled trusted Cerberus app.

CLI v0.10.4+ preflights inputs before posting. A `request_input_*`,
`request_item_revision_unavailable`, `request_field_unavailable`, or
`request_totp_invalid` diagnostic identifies the exact metadata reference and
reports no grant consumption/process start. Follow that cause; do not repeatedly
resave metadata or request approval. Nonempty short values are supported, but the
approved process's output is suppressed to protect them. On older clients, a
generic eligibility error can mean the old four-byte minimum even when policy is
correct. Upgrade when authorized; never pad, combine, reveal or change a field's
policy as a workaround. Actual value changes require the user's organize scope.

Use ordinary CLI commands pinned to the selected profile. A local credential-store
error is not an invitation to reset login or create a connection daemon; diagnose
with `c6s:setup`. Preserve the exact action and avoid duplicate creation after an
ambiguous response.

Configurable timing (upcoming V4 CLI, pending release): both windows default to 15m.
Read `c6s request config --json` without changing it. For an authorized request,
`--approval-ttl` / `--execution-ttl` override the saved defaults before `--`.
Accept only whole seconds 1s–24h; show the selected durations with the exact intent.
Do not silently persist preference changes. Earlier clients do not accept these
options; inspect capabilities/help and do not re-create a request on version failure.
Use a matching explicit wait timeout when a request-specific window exceeds the
saved default. A configured duration is never approval or execution permission.
