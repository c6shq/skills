# c6s Skills

Official public-preview skills and plugins for [c6s](https://c6s.whitekiwi.link),
the approval-gated secret system displayed to users as Cerberus.

These workflow definitions help agents use the c6s CLI without placing secret values
in prompts, logs, or tool arguments. Product source code remains private during beta.

The single `c6s` plugin provides five intentionally separated workflows:

- `c6s:setup` — install, connect, configure, and diagnose c6s;
- `c6s:find` — locate and inspect vault metadata without values;
- `c6s:organize` — structure items, fields, and agent-use policy;
- `c6s:request` — create one exact approval-gated process request;
- `c6s:run` — execute one already approved request with redacted output.

There is deliberately no agent approval workflow. A human-controlled trusted
Cerberus app remains the only approval surface.

## Install

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

## Feedback and security

Report workflow bugs and feature requests in
[c6shq/feedback](https://github.com/c6shq/feedback/issues/new/choose). Do not include
secret values, credentials, recovery material, or unredacted logs. Report suspected
vulnerabilities privately using the c6s
[security policy](https://github.com/c6shq/.github/blob/main/SECURITY.md).
