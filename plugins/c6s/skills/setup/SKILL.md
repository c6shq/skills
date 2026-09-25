---
name: setup
description: Install, connect, configure, or diagnose the c6s CLI, accounts, trusted devices, encrypted vault, and local MCP integration. Use for c6s onboarding or connection problems; do not bypass trusted-device approval.
---

# Set up c6s

Use the installed CLI as the current contract. Start with `c6s version`, `c6s channel`,
and the relevant `c6s help <command>` instead of assuming a newer command exists.

## Establish the selected environment

- Stable, beta, and development clients have separate accounts, Keychain entries,
  devices, and vaults. Never repair one channel by copying another channel's files.
- List configured profiles with `c6s profile list` and inspect the default with
  `c6s profile default`. Select a non-default profile per command with the global
  `c6s --profile <name> ...` option; unattended processes may instead set
  `C6S_PROFILE` explicitly.
- Verify the selected sign-in with `c6s whoami --json`. It performs server
  verification and automatic session renewal without exposing credentials. Treat
  “session ended” as a login requirement, but keep transient network renewal and
  Keychain-read errors distinct and do not delete the profile for either one.
- Inspect `c6s device status`, `c6s device remote-status`, `c6s vault status`, and
  `c6s vault remote-status` for the selected profile before changing state.
- Do not print Keychain contents, bearer credentials, vault keys, recovery material,
  or protected configuration.

## Onboard in dependency order

### Existing sign-in fails only in SSH or an agent

Do not restart onboarding for a Keychain error. Resolve `type -a c6s` and the
reviewed absolute binary's version first; stale PATH entries may select an old
client. If installed help exposes them, use `c6s doctor --json` and
`c6s agent status --json` in the failing execution session. They read no credentials;
neither store status nor socket presence proves a working account.

Current signed macOS clients can use an owner-operated local connector:

1. Report the failing session's `sessionId` and selected profile to the owner.
2. The owner, not the agent, runs `c6s --profile <name> agent serve --allow-session
   <sessionId> --ttl 12h` in their own authenticated terminal. Do not start it by
   moving into a GUI/other security session, changing Keychain ACLs or capturing
   an unlock password. No screen/PTY recovery relay is necessary.
3. Only after owner startup, explicitly use `C6S_CONNECTION=agent` with the same
   profile for `whoami`, remote metadata and request commands. Do not silently
   fall back to direct access, change scope, or replay a failed request.

The connector is foreground, local, signed-peer and audit-session bound, not a
restart-persistent service account. It stops on owner exit or at most twelve hours;
credential-store denial fails the operation. The OS may still require the owner to unlock their own
terminal through Apple's hidden prompt. Another terminal's successful unlock does
not prove this agent can read credentials. Do not loop over unlock or OAuth login.

Connection permission is not secret-use permission. Exact trusted-device approval
is still required. Reveal, policy edits, uploads, account changes and device approval
are denied through this connector. Preserve profiles, refresh credentials, devices
and vaults on every failure; hand off genuine owner authentication instead of
deleting state. For `session_metadata_unavailable`, repair profile-file storage and
retry the read; do not log out or restore an old rotated refresh token.

### New account or explicitly requested enrollment

1. Install only when requested. Stable Apple Silicon macOS supports
   `brew install c6shq/tap/c6s-cli` or the checksum-verifying public installer.
2. Sign in with `c6s login --provider google --name <profile>`. Each profile has
   isolated account credentials, device registration, and remote vault state. Use
   `c6s profile default set <name>` only when the user explicitly wants to change
   the interactive default; automation should pin a profile instead of mutating it.
3. Create the local identity with `c6s device setup`, then enroll with
   `c6s device enroll`.
4. Stop while the device is pending. Only a trusted Cerberus iPhone or Mac may
   approve it; this skill must never approve its own device.
5. After `c6s device remote-status` reports trusted, connect the Personal vault with
   `c6s vault connect` and read both vault status commands back.

`c6s --profile <name> mcp` is a local stdio server pinned to one profile. Configure
clients with an absolute executable path when they may not inherit the interactive
shell `PATH`. Plugin installation does not log in, enroll a device, connect a vault,
or enable MCP automatically.

If authentication, Keychain access, device trust, or encrypted sync fails, report
the failing boundary without weakening it or deleting account/vault state.

For hosted item-read failures, require `c6s v0.9.12` or newer before diagnosing
from the message. Older clients incorrectly collapsed authenticated-decryption and
typed-document incompatibility into “the remote service is unavailable.” On current
clients:

- `vault_item_document_invalid` means the envelope authenticated but its typed-item
  document is unsupported or invalid. Upgrade compatible clients first; do not
  reconnect, delete, or replace a key.
- `vault_item_decryption_failed` identifies one opaque hosted item ID and revision
  that did not authenticate with the selected profile key. Do not infer that the
  server is down, and do not delete the item or rotate keys automatically.
- `c6s vault connect --json` is an idempotent key-consistency check, not a generic
  repair. Current clients accept an equal server-provided key but fail closed as
  `vault_key_mismatch` before changing Keychain or connection state when it differs.
  Never use an older client to reconnect during a suspected key mismatch because it
  may replace the stored hosted-vault key without preserving the prior one.

`c6s vault upload` is an explicit initial local-to-hosted import, not a general sync
repair. When installed help exposes `--item <exact-local-item-id>`, use it for one
authorized initial registration without processing unrelated local items. This
does not resolve a conflict on the selected item, and a
one-item request must never fall back to bulk upload on an older CLI.
If it reports a tombstone conflict, do not retry the upload or delete remote
state. Hand the exact local item ID and observed tombstone revision to the
`c6s:organize` recovery flow only when the user chooses to keep that local item as a
new hosted item.

A `vault_active_item_conflict` is different: an active hosted branch already owns
the ID and has different encrypted content. Do not retry, reconcile, delete, or pick
a winner. First use only the two value-free `item inspect` commands emitted by the
CLI and report the local ID, hosted ID, hosted revision, and zero writes. `--json`
emits the typed error on stderr and intentionally leaves stdout empty. If and only
if the user explicitly chooses the hosted branch, hand the exact
`resolutionCommands.keepRemote` command to `c6s:organize`. It is revision-bound,
preserves the losing local branch as an encrypted local-only copy, and must perform
zero hosted writes.

For a confirmed lost or compromised CLI device, inspect the selected profile and
remote device status first, then use `c6s --profile <name> device revoke --yes`.
Explain that it
revokes the server device and session and removes only that account's local remote
registration and wrapped vault key; it preserves other accounts and the encrypted
local vault. Do not run it as a generic sync repair or without explicit authority.
