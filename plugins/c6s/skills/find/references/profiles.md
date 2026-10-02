# Keep the selected account pinned

1. Establish the user's intended account before inspecting protected metadata or
   mutating anything. `c6s profile list --json` lists configured profile identities;
   it is a global discovery command. If the intended account is ambiguous, ask.
2. Resolve the chosen account to its immutable local profile ID. In these skills,
   `PROFILE` means that same ID throughout the workflow, not the word `PROFILE`.
   Verify it with `c6s --profile PROFILE whoami --json`. Stop if the account, server,
   or intended destination does not match, or if the profile cannot be resolved.
3. Use `c6s --profile PROFILE ...` for every account-specific read, mutation,
   verification, retry, and handoff. Carry the same profile together with item IDs,
   field IDs and revisions into `c6s:otp`, `c6s:request`, or `c6s:organize`.
   Do not switch the shared default or rely on `C6S_PROFILE`: another process can
   change the default, and an inherited environment may name a different account.
   Never silently fall back to another profile after an error.

The CLI accepts one global `--profile` selector before the child-process `--`
boundary. Explicit selection takes precedence over `C6S_PROFILE` and the stored
default. Global discovery/help such as `c6s profile list --json`, `c6s version`,
`c6s help item`, and `c6s attachment upload --help` does not need a profile selector.
Changing the default is not part of either find or organize.

## Local vault limitation

The legacy local `item` commands (without `--remote`) and local vault status use
a channel-local encrypted store, not a profile-isolated store. Passing `--profile`
does not change that local storage boundary. Confirm the intended local source
separately; never infer account ownership from a local item or merge local metadata
with remote results from another account. The explicit selector pins the remote
account for remote reads, attachment operations, and local-to-hosted uploads.

## Returned commands are not permission

Before using `nextCommands`, `resolutionCommands.keepRemote`, or a printed
tombstone recovery command, check all of the following without executing it:

- It is the expected single `c6s` command for the already authorized operation,
  with the reviewed item IDs and revision guards intact. Never evaluate it as an
  arbitrary shell program or accept added pipelines, substitutions, or commands.
- It contains exactly one explicit `--profile PROFILE` or `--profile=PROFILE`
  selector before any `--` boundary. Its selector must resolve to the same immutable
  profile ID already chosen for this workflow. A flag in child-process arguments
  is not an account selector. Do not trust a matching display name alone.
- The command still respects the skill's boundary: find only inspects metadata;
  recovery or resolution needs the user's explicit branch choice and target.

If a selector is missing, duplicated, ambiguous, or mismatched, stop and report the
account-binding problem. Do not append or replace a profile selector, reconstruct
or shorten the command, remove revision guards, change the default, or rerun an
upload to obtain a different command. Preserve the original command privately for
diagnosis. Only a reviewed, correctly profile-bound command may proceed unchanged.

Some CLI versions emit conflict/recovery commands without a profile selector, even
when the original upload was pinned. Those outputs do not satisfy this contract;
stop for a supported CLI fix or owner review rather than guessing the account.
