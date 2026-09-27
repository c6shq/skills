# c6s Skills

Official public-preview skills and plugins for [c6s](https://c6s.whitekiwi.link),
the approval-gated secret system displayed to users as Cerberus.

These workflow definitions help agents use the c6s CLI through explicit access
boundaries. Approval-bound actions conceal values; a separately owner-permitted OTP
read returns only the current code and expiry for its authorized destination.
Product source code remains private during beta.

The single `c6s` plugin provides six intentionally separated workflows:

- `c6s:setup` — install, connect, configure, and diagnose c6s;
- `c6s:find` — locate and inspect vault metadata without values;
- `c6s:otp` — read an already owner-permitted current OTP code with exact expiry;
- `c6s:organize` — structure items, fields, agent-use policy, and authorized encrypted file uploads;
- `c6s:request` — create one exact approval-gated process request and optionally wait without execution;
- `c6s:run` — execute one approved request, or wait for human approval before an explicitly authorized action.

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

CLI v0.10.4 supports short approved inputs without rewriting them. For these
inputs, child output is suppressed and the result still reports execution/exit
and one-time grant state. Skills 0.1.17 distinguish this protection from an input
validation failure and prohibit automatic payment/action retries. Creation and
execution errors identify the exact metadata reference without revealing values.

Skills 0.1.18 document CLI v0.10.5+ `attachment policy`: change an existing file's
agent policy without replacing its ID or re-entering its bytes. The workflow pins
the ready revision and preserves the private encrypted retry journal. Eligibility
changes remain separate from human approval and one-time execution.

Approval waiting is a normal CLI workflow for values, TOTP and private files:

```sh
c6s --profile PROFILE request wait REQUEST_ID --timeout 5m --json
# Only when the exact action is already authorized after human approval:
c6s --profile PROFILE request wait REQUEST_ID --timeout 5m --execute --json
```

Use one of these modes, not both as a fixed sequence. The skills explain supervised
process handles, the five-minute request/two-minute grant windows, result parsing,
safe timeout recovery and no automatic replay. No approval callback, persistent
daemon or agent-approval capability is introduced.

Skills 0.1.20 direct-code reads require CLI v0.11.0+ `otp get`/`otp policy` support
and updated native editing clients (macOS 0.7.0+ and the matching iOS update). Existing fields
remain approval-only until an owner explicitly opts in. The new OTP skill never
enables access itself, never returns a setup key, and does not silently retry login
or payment attempts. Both direct reads and the existing confidential injection mode
remain available; MCP is unchanged.

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
