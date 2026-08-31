# Agent guidance

- Treat every plugin command as constrained by the invoking user's authorization.
- Never add a skill or MCP tool that approves its own c6s request.
- Never include credentials, vault values, private keys, tokens, account exports, or
  protected configuration in this repository.
- Keep Codex and Claude plugin versions aligned.
- Commit messages must use `{type}: {imperative message}`.
