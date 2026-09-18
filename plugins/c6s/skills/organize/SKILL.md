---
name: organize
description: Create and organize c6s vault items, semantic fields, encrypted file uploads, and agent policy. Use for explicit vault mutations; do not ask for secrets in chat, reveal values, or approve their use.
---

# Organize c6s

Inspect the selected account, local vault status, the current item, and the installed
`c6s help item` surface before mutation. Preserve unrelated fields and revisions.

Supported item kinds are `login`, `api_credential`, `secure_note`, `identity`,
`certificate`, `ssh_key`, `database`, and `custom`. Supported semantic field kinds
are `text`, `concealed`, `multiline`, `url`, `email`, `phone`, `date`, `boolean`,
`public_key`, and `private_key`.

## Mutation boundary

For an explicit file backup/upload, read [Encrypted attachments](references/attachments.md).
Check the installed help first; upload support starts in CLI v0.9.19. This path uses
an authorized existing local file without reading its contents into the conversation.

- Create structure with `c6s item create --kind <kind> --title <title>`.
- Add or replace one field through `c6s item set <item-id> --field <label>
  --value-stdin --kind <kind> --agent-policy <policy>`.
- Change only an existing field's agent policy through `c6s item policy <item-id>
  --field <label-or-id> --agent-policy <policy>`. This preserves the field identity,
  kind, sensitivity, and encrypted value; do not use `item set` merely to change a
  policy.
- For an existing connected remote item, use its remote ID and add `--remote`. The
  CLI reads the latest encrypted revision, changes one policy, and fails closed on a
  concurrent write. Never lower local revisions or use `vault upload` as a conflict
  override.
- Use `reference_only` by default. Use `approved_injection` only when the user wants
  the exact field eligible for a separately approved action. Use `never_agent` when
  an agent must not use it.
- Never put a secret in argv, a temporary plaintext file, logs, or chat. If a value
  is not already available through an authorized local input channel, hand the stdin
  entry step to the user rather than asking them to paste it into the conversation.
- Read the item back with `item inspect`; never verify a mutation by revealing it.
- A missing field is not a policy edit. Add it once through the authorized stdin
  path, then keep later policy changes value-preserving.

Remote upload is a separate external mutation intended only for an explicit initial
local-to-hosted import. It is not continuous or bidirectional sync. For one item,
check that installed `c6s help vault upload` exposes `--item`,
then use `c6s vault upload --item <exact-local-item-id> --yes --json`. Resolve the ID
through value-free inspection; title/wildcard selection is not supported. It reads
only that local item, preserves its policies, and leaves unrelated local items and
binding receipts untouched. Verify `localItemId`, `localItems: 1` and uploaded or
unchanged counts, then inspect the resulting remote metadata. If the installed CLI
lacks `--item`, stop for an upgrade; never silently broaden a one-item request to a
whole-vault import. Use `c6s vault upload --yes` only for an explicitly requested
whole-vault initial import. Use the dedicated remote policy mutation when the
requested difference is exactly one field policy.

The upload plan reads active items and deletion tombstones before any write. A
matching selected-item tombstone must stop the complete plan (the one selected
item, or the whole batch when no selector was given). Never delete/recreate an item,
lower a revision, retry a 409, or choose a branch implicitly. If the user explicitly
wants to preserve the local item as a new hosted item, inspect `c6s help vault
reconcile` and use only the exact recovery command printed by `vault upload`. It
must bind the local item ID and currently observed tombstone revision and include
both `--keep-local-as-new` and `--yes`. A revision mismatch is a new stop condition.
The recovery creates a new hosted ID, preserves the tombstone, never prints a value,
and must be verified through value-free remote metadata.

If upload reports `vault_active_item_conflict`, stop before mutation. This is an
active hosted branch, not a recoverable tombstone. Run only the exact local and
remote value-free inspect commands in `nextCommands`; never run `vault reconcile`,
repeat upload, or infer which protected value differs. If the user explicitly chooses
the hosted branch, inspect `c6s help vault resolve` and run only the exact
`resolutionCommands.keepRemote` command emitted for that conflict. It must bind the
local ID, hosted ID, and reviewed hosted revision and include `--keep-remote`,
`--preserve-local-as-copy`, and `--yes`. Never reconstruct or shorten it. Afterward,
verify through value-free local and remote metadata that the local loser exists under
a fresh ID with `syncDisposition=local_only_conflict_copy`, the reviewed hosted
revision is unchanged, and the result reports `hostedWritesApplied: 0`. A moved
branch, missing command, or unsupported CLI version is a new stop condition.

Deletion and field removal require explicit target confirmation and the CLI's
`--yes` flag. This skill never approves a device, action request, or OTP request.
