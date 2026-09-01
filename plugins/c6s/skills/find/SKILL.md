---
name: find
description: Find and inspect c6s vault item and encrypted-attachment metadata without revealing protected values. Use to locate local or remote items, fields, files, policies, and exact revisions; do not retrieve plaintext or create approval requests.
---

# Find in c6s

Confirm the active account and whether the task needs the local encrypted vault or
the connected remote Personal vault. Prefer JSON output for exact identifiers.

- List local metadata with `c6s item list --json`.
- List synchronized metadata with `c6s item list --remote --json`.
- Inspect an exact local item with `c6s item inspect <item-id> --json`.
- Inspect an exact remote revision with
  `c6s item inspect <remote-item-id> --remote --json`.
- List one remote item's encrypted-file metadata with
  `c6s attachment list <remote-item-id> --json`; this returns IDs, revisions,
  filenames, media types, sizes, states, and policies, never file contents.

Filter returned metadata to the user's need instead of opening every item. Treat
titles, contexts, account aliases, item IDs, field IDs, and revisions as protected
metadata even though they are not secret values.

Never run `c6s item reveal --show`, read encrypted vault files directly, inspect
Keychain entries, or infer a value from surrounding metadata. Never upload, mutate,
request, approve, or execute as part of a lookup.

Legacy imported local IDs can differ from their server IDs. When another workflow
needs a remote reference, use the ID returned by the remote list and verify the
field ID, agent policy, and revision from the remote inspect result.
