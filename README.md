# c6s Skills

Official private-preview skills and plugins for [c6s](https://c6s.whitekiwi.link),
the approval-gated secret system displayed to users as Cerberus.

The single `c6s` plugin provides five intentionally separated workflows:

- `c6s:setup` — install, connect, configure, and diagnose c6s;
- `c6s:find` — locate and inspect vault metadata without values;
- `c6s:organize` — structure items, fields, and agent-use policy;
- `c6s:request` — create one exact approval-gated process request;
- `c6s:run` — execute one already approved request with redacted output.

There is deliberately no agent approval workflow. A human-controlled trusted
Cerberus app remains the only approval surface.

## Private-preview install

Install the stable CLI first:

```sh
brew install c6shq/tap/c6s
```

Then add this repository as a marketplace and install the plugin:

```sh
codex plugin marketplace add c6shq/skills
codex plugin add c6s@c6s-skills

claude plugin marketplace add c6shq/skills
claude plugin install c6s@c6s-skills
```

The bundled local `c6s mcp` declaration is disabled by default. Plugin installation
does not log in, enroll or approve a device, connect a vault, reveal a value, or grant
access to an account.

## License

Proprietary and confidential. See [LICENSE](LICENSE).
