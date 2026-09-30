---
name: otp
description: Use a c6s authenticator code for an authorized task. Read an already permitted code and expiry, or route approval-required fields to exact approved execution. Do not reveal the setup key, enable access, or approve requests.
---

# Use an OTP with c6s

Use this for a current authenticator code, not its permanent setup key. It is a
separate mode from approval-bound injection. Inspect `c6s version` and the help
for the chosen mode: `c6s help otp get` before a direct read, or `c6s help otp request`
and `c6s help request wait` before approved execution. Missing direct-read support
does not rule out supported approval-bound injection. Request a client update only
for the mode you need; do not invent commands or treat missing help as an
account/Keychain problem.

Choose by destination and permission, not just the presence of an OTP field.
Read [OTP routing](references/routing.md) when permission is absent/denied, the
task needs an exact process rather than a returned code, or browser input is the
destination. A denied direct read does not make approved OTP use unavailable.

1. Establish the user's intended account and destination. Pin `--profile PROFILE`
   for every command; do not switch the shared default. Use `c6s:find` for value-free
   hosted metadata discovery if needed. Resolve an exact item ID and field ID.
2. Require `kind: totp_seed`, `sensitivity: secret`, `agentPolicy: never_agent` and
   explicit `otpCodePolicy: allow_read`. The policy grants derived-code reads only;
   `never_agent` still forbids revealing the setup key. An absent/unknown policy is
   not permission for direct reads. Do not change policy to make the task work.
   `item inspect --remote --json` on newer clients also reports
   `otpCodeReadAllowed` explicitly; false means route to the alternatives below,
   not that the authenticator is missing or broken.
3. Immediately before the authorized destination needs its code, invoke:

   ```sh
   c6s --profile PROFILE otp get ITEM_ID --field FIELD_ID --json
   ```

   This returns `code` as a string, `generatedAt`, `expiresAt`, `remainingSeconds`,
   `periodSeconds`, and the exact item/field/revision. Preserve leading zeroes. The
   default five-second minimum validity can briefly wait for a new period; it
   rereads trust and policy afterward. `--min-validity 0s` is available when the user
   explicitly needs the current code immediately. No request/grant/process is
   created, and no per-use approval prompt occurs for an already allowed field.
4. Use the code only for the authorized destination while it remains valid. The
   success result is intentionally sensitive; do not repeat the code in commentary,
   a final answer, knowledge memory, logs, reusable scripts or general tool
   arguments. A direct entry into the user's authorized authentication form is the
   intended narrow use. Never retrieve or export the seed to generate codes yourself.

If `otp_code_read_not_allowed`, stop the direct read and follow
[OTP routing](references/routing.md). For an already authorized exact process,
continue through `c6s:request` and `c6s:run` using approval-bound injection, one
request and bounded wait; do not abandon the task or ask for duplicate chat
authorization. For browser-only input, explain **2FA → Edit → Allow agent code
reads** (older apps: **Allow CLI code reads**), or owner entry. Do not state that
manual entry is the only supported OTP workflow. Do not issue `otp policy`, change seed policy,
read Keychain, or use a callback/child echo to bypass a denied read. Policy changes
belong to a separate explicit owner-authorized `c6s:organize` task.

Online authentication, device trust and the latest hosted policy are mandatory.
Do not fall back to stale local state on network/Keychain/sync failures. Distinguish
missing/ambiguous fields, invalid configuration, denial and clock/expiry errors.
No OTP MCP result is provided; the skill uses the installed CLI.

Expiry does not make disclosure harmless. If a code expires before submission, a
fresh single read may be appropriate for the still-authorized pending input, but do
not loop, silently resubmit a failed login/payment or retry an ambiguous side effect.
Existing `otp request` continues to keep the code out of the agent's output; prefer
that mode when the task requires confidential process injection.
