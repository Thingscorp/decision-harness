# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's
**Report a vulnerability** flow (Security tab of this repository)
rather than opening a public issue.

## Scope notes

- The CLI never prompts for a key interactively and never logs one.
  Keys come from `--api-key`, `$CLEF_API_KEY`, or
  `~/.config/clef-decide/config`. Prefer the env var or the config
  file: a CLI flag can appear in shell history and process listings.
- Endpoint overrides must be `https://` URLs; plain HTTP is rejected.
- Requests are single attempts with no retries and no idempotency key,
  by design: an unknown outcome may already be charged by the provider.
