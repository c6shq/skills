# Owner-authorized encrypted file upload

Confirm the user's authorized source file, destination account/profile and existing
remote item. Check `c6s attachment upload --help`; do not assume upload is absent
because an older CLI or skill only listed metadata. CLI v0.9.19 adds this command.
If unsupported, use `c6s:setup` to update through the installation's supported path;
do not substitute raw HTTP, plaintext exports or ad hoc crypto.

Use the remote item ID from value-free metadata inspection:

```sh
c6s --profile PROFILE attachment upload REMOTE_ITEM_ID --file /authorized/source --json
c6s --profile PROFILE attachment list REMOTE_ITEM_ID --json
```

The CLI reads/encrypts the source itself. Do not use `cat`, print a file, pass file
contents in arguments, or create a plaintext staging copy. Regular files up to
16 MiB minus 28 bytes are supported; symlinks/directories are rejected. Exact bytes
and line endings are preserved. Use encrypted attachments for configuration,
cookie, certificate or binary backups instead of splitting content into fields.
Backup authorization must actually include the source; a request to list files or
diagnose a connection does not authorize uploading them.

Default policy is `reference_only`. `never_agent` is appropriate for a backup the
agent must never use. Choose `approved_injection` only if the user explicitly wants
that file eligible for later approved execution. It does not grant immediate use;
`c6s:request` and `c6s:run` remain separate and never self-approve. Optional `--name`
and `--media-type` change encrypted descriptive metadata, not file bytes.

This uploads directly to the connected remote vault. No `vault upload`, local item
deletion, conflict reconciliation, or re-entry of the secret is needed afterward.
Verify only attachment ID, revision, policy and `state: ready` via metadata.

## Retry boundary

The CLI saves a private ciphertext-only journal before remote mutation and reports
its path on completion/failure. `--journal /new/path.json` overrides the private
cache location; an existing file is never overwritten. Resume under the same profile:

```sh
c6s --profile PROFILE attachment upload --resume /exact/journal.json --json
```

Only an ambiguous transport failure justifies a bounded explicit resume of this
exact operation. It reuses the same encrypted bytes, ID and idempotency keys; the
source file need not exist. Repeating `--file` instead creates another attachment.
Stop on `attachment_conflict`, invalid journal/destination, missing parent, or
authentication/approval failure. Do not edit a journal, regenerate its ID, delete
an item, lower a revision, or change policy to bypass the stop. Preserve the journal
for recovery; it contains encrypted file data, so never publish it as a support log.
