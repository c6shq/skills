# Choose an OTP workflow

Permission to return a code and permission to inject one into an approved process
are different. A missing `otpCodePolicy` denies direct reads; it does not disable
the authenticator or approval-bound execution.

| Destination and permission | Continue with |
| --- | --- |
| Owner-authorized input, eligible field with `allow_read` | `otp get` immediately before input; preserve the code string and expiry. |
| Exact owner-authorized process, eligible seed, approval-required code reads | `otp request`, then bounded wait and one execution through request/run. |
| Browser form only, code reads not allowed | Explain native owner opt-in or owner entry; injection does not return a code to browser tools. |
| Ineligible/ambiguous field, wrong profile, stale revision, trust or connection error | Diagnose that cause with find/setup; do not treat it as a missing code permission. |

## Approval-bound process

Resolve the hosted item, field and current revision with `c6s:find`. Require
`totp_seed`, `secret`, `never_agent`; `otpCodePolicy: allow_read` is not needed
for this mode. The user must have authorized the actual executable, arguments and
destination. An OTP request is not permission to substitute another process.

Use `c6s:request` to create one exact request:

```sh
c6s --profile PROFILE otp request --summary SUMMARY \
  --inject ITEM_ID:FIELD_ID:REVISION:ENV --json -- ABSOLUTE_EXECUTABLE AUTHORIZED_ARGS
```

Then use `c6s:run` when execution after trusted-device approval was already
authorized:

```sh
c6s --profile PROFILE request wait REQUEST_ID --timeout 5m --execute --json
```

For request-only scope omit `--execute`. Read the
[waiting guide](../../request/references/waiting.md) for supervised tool handles
and timeout recovery. Report the exact request and expiry, and say that a fresh
code will be generated at process start. Never claim a push arrived until delivery
is confirmed. Do not create another request while the first remains pending, or
repeat chat authorization already provided for the same action.

## Browser input

If a legitimate authorized CLI action can perform the same requested task, use
the process route. Do not invent an executable or turn a login into publication,
payment or another action just to obtain an approval target.

Otherwise explain: "This authenticator is set to approval-only. In Cerberus,
open 2FA → Edit → Allow agent code reads, save and sync to let this trusted CLI
read future codes. You can also enter this code yourself. Approval-bound program
execution remains available, but it cannot supply a plaintext code to this
browser tool." Older apps label the control Allow CLI code reads.

When the owner explicitly asks for a specific permission change, use the separate
organize workflow and exact revision; do not self-enable access after denial.
Native Agent code access can review several accounts together. Do not echo a code
from an approved child, use a clipboard/file bridge, reveal the seed, or treat a
request/grant as direct-read permission. Wait for synced metadata before a read.
