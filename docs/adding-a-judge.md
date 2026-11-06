# Adding a judge

Any SystemOne-compatible decision endpoint becomes a judge with three lines in `~/.config/clef-decide/config`:

```ini
judge_oracle_endpoint=https://oracle.example/v1/systemone
judge_oracle_model=oracle-1
judge_oracle_api_key=sk-...
```

The key may also come from `$JUDGE_ORACLE_API_KEY`. The name must not collide with a built-in (`clef`, `clef-flash`, `jev`, `luna`, `subq`).

Use it:

```bash
bin/clef-decide --state-file state.md --questions questions.json --judge oracle
```

Named judges are optional convenience defaults. They work only when their provider keys are present. Prefer custom judges for any other endpoint or model.

The tool accepts any model string on a SystemOne route. No allowlist is enforced.
