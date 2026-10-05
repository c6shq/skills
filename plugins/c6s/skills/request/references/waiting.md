# Waiting for a human decision

Use this for an existing exact request. It applies equally to field values, TOTP,
and encrypted files. No agent or skill may approve the request.

## Choose the intended outcome

| User intent | What to do |
| --- | --- |
| Send a request; user will return later | Create once, inspect, report ID/expiry, stop. |
| Wait for approval, but do not execute | Use the bounded wait command without `--execute`. |
| Complete this exact action after human approval | Inspect intent first, then use `c6s:run` and bounded `--execute`. |
| Only report status | Inspect the existing request; do not create or execute. |

Replace PROFILE and REQUEST_ID with the already selected profile and returned ID.
Keep them fixed for creation, inspection, waiting and execution; never change the
shared default profile as part of this flow.

```sh
c6s --profile PROFILE request inspect REQUEST_ID --json
c6s --profile PROFILE request wait REQUEST_ID --json
```

The second command only waits. When the user has authorized the exact action and
asked you to continue after approval, use this **instead**, through `c6s:run`:

```sh
c6s --profile PROFILE request wait REQUEST_ID --execute --json
```

Do not run both as a fixed sequence: waiting without execution can use up the grant
window while another agent turn starts. Inspect the summary, executable, arguments,
working directory and every exact input/environment binding before starting
wait-and-execute. Trusted-app approval supplies the human decision; it does not
broaden the action the user asked the agent to perform.

## Keep one supervised process alive

- Tell the user the request ID, action summary and expiry before waiting. Creation
  success is not proof a push notification arrived.
- Launch one wait command with the host execution tool. If it yields a process or
  task handle, resume that handle to collect completion; do not launch another wait
  or create a replacement request at each tool yield.
- An output-yield interval is not a command deadline. Let the CLI own the approval
  timeout; give an approved child sufficient lifetime to finish. Keep the process
  supervised and provide brief status while doing other authorized work.
- If the host cannot retain a live process, report the pending ID and return. Do
  not invent a webhook, a persistent connection daemon, detached shell loop,
  scheduled wakeup or a promise to resume after the agent has ended.
- Cancel a live wait through its existing execution handle if requested. Cancelling
  waiting does not reject the server request. After execution has begun, interruption
  can leave an external side effect; never infer rollback from cancellation.

## Interpret the result, not just the exit status

- Read the exact request expiry and execution duration rather than assuming a fixed
  lifetime. Compatible V4 clients default both windows to 15m; options override saved
  channel defaults. Earlier clients retain 5m review and 2m execution. Omitting
  `--timeout` uses the client default; waiting extends neither lifetime.
- Wait-only returns metadata. `state: approved` is executable only when
  `grantState: available` / `effectiveState: executable`. Consumed means no replay.
- Wait-and-execute returns the usual execution JSON. Inspect `exitCode` and
  `grantState`; CLI success can contain a nonzero child exit. A failed child still
  consumes its grant. `outputSuppressed: true` is intentional for short inputs.
- Rejected, expired, missing or unverifiable: stop and report the reason. Do not
  automatically make a fresh request, resave item metadata, broaden policy or log in
  repeatedly. Missing from bounded recent history does not prove deletion.
- Timeout or lost execution handle: inspect **the same ID/profile** first. A timeout
  changes no remote state. If execution may have started or consumption is ambiguous,
  do not retry execution; report uncertainty and check authorized read-only status.
- An unambiguously still-pending request can be waited on again within its original
  expiry and the user's still-current intent. Do not keep renewing local timeouts
  indefinitely, and never equate this with permission to re-create expired requests.

Existing stable versions support these commands. CLI v0.10.6+ with `--json` also
emits typed `request_wait_*` failures as one JSON object on **stderr**, with stdout empty.
`executionAttempted: false` refers only to that wait invocation, not another process.
Use `code`, `nextAction` and optional `lastErrorCode`; never assume every error means
the service is down. `request_wait_timeout` with a rate-limit/transport last error
means status could not be kept current, not that the person rejected the request.
On older versions, errors may be plain text: preserve them and inspect safely rather
than assuming a JSON decoding failure authorizes another execution.
Profile/credential loading before waiting keeps its own diagnostic family; once
execution begins, use the executor's result instead of expecting a wait diagnostic.

MCP inspection remains read-only and MCP execution remains a separate guarded tool.
There is no MCP wait tool or approval callback subscription in this release; use
the CLI supervised wait when a shell tool is available. Never pass protected values,
grant tokens or generated OTPs through the agent to bridge tools.
