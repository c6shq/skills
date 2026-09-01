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
- Inspect `c6s device status`, `c6s device remote-status`, `c6s vault status`, and
  `c6s vault remote-status` for the selected profile before changing state.
- Do not print Keychain contents, bearer credentials, vault keys, recovery material,
  or protected configuration.

## Onboard in dependency order

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

For a confirmed lost or compromised CLI device, inspect the selected profile and
remote device status first, then use `c6s --profile <name> device revoke --yes`.
Explain that it
revokes the server device and session and removes only that account's local remote
registration and wrapped vault key; it preserves other accounts and the encrypted
local vault. Do not run it as a generic sync repair or without explicit authority.
