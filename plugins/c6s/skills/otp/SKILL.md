---
name: otp
description: Read a current c6s one-time code and its expiry for an owner-authorized use when that field already permits direct code reads. Do not reveal the setup key, enable access, approve requests, or retry a login automatically.
---

# Read an OTP with c6s

Use this for a current authenticator code, not its permanent setup key. It is a
separate mode from approval-bound injection. First inspect `c6s version` and
`c6s help otp get`; if unsupported, stop and request the compatible client update.
Do not invent this command on an older installation or treat missing help as an
account/Keychain problem.

1. Establish the user's intended account and destination. Pin `--profile PROFILE`
   for every command; do not switch the shared default. Use `c6s:find` for value-free
   hosted metadata discovery if needed. Resolve an exact item ID and field ID.
2. Require `kind: totp_seed`, `sensitivity: secret`, `agentPolicy: never_agent` and
   explicit `otpCodePolicy: allow_read`. The policy grants derived-code reads only;
   `never_agent` still forbids revealing the setup key. An absent/unknown policy is
   not permission. Do not change policy to make the task work.
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

If `otp_code_read_not_allowed`, stop and explain that the owner can enable
**Allow CLI code reads** for that authenticator, or use `c6s:request` and `c6s:run`
for existing approval-bound injection. Do not issue `otp policy`, change seed policy,
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
