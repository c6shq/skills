# c6s Skills

Official public-preview skills and plugins for [c6s](https://c6s.whitekiwi.link),
the approval-gated secret system displayed to users as Cerberus.

These workflow definitions help agents use the c6s CLI without placing secret values
in prompts, logs, or tool arguments. Product source code remains private during beta.

The single `c6s` plugin provides five intentionally separated workflows:

- `c6s:setup` — install, connect, configure, and diagnose c6s;
- `c6s:find` — locate and inspect vault metadata without values;
- `c6s:organize` — structure items, fields, agent-use policy, and authorized encrypted file uploads;
- `c6s:request` — create one exact approval-gated process request;
- `c6s:run` — execute one already approved request with redacted output.

There is deliberately no agent approval workflow. A human-controlled trusted
Cerberus app remains the only approval surface.

## Install

Install the stable CLI first:

```sh
brew install c6shq/tap/c6s-cli
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

For SSH/agent-only Keychain errors, `c6s:setup` distinguishes account expiry from
OS-store access. Use the ordinary selected profile and `doctor`; owner recovery
uses Apple's hidden terminal prompt only when necessary. There is no connection
daemon or session setup. No password capture, Keychain ACL relaxation, automatic
unlock or account reset is supplied. CLI v0.10.2 removes the unrequested connector
from v0.10.0–v0.10.1; use the current stable release.

## License

The public agent workflow definitions are available under the [MIT License](LICENSE).
This does not license the c6s service, CLI, Cerberus applications, trademarks, or
private product source code.

## Feedback and security

Report workflow bugs and feature requests in
[c6shq/feedback](https://github.com/c6shq/feedback/issues/new/choose). Do not include
secret values, credentials, recovery material, or unredacted logs. Report suspected
vulnerabilities privately using the c6s
[security policy](https://github.com/c6shq/.github/blob/main/SECURITY.md).
