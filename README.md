# decision-harness

A tribunal of AI decision helpers for coding agents. The agent does the legwork; judges make every gated decision. Plug in any SystemOne-compatible decision endpoint via config — no fixed LLM or provider required.

Routine gates go to a single judge; high-stakes termination can go to a panel (one judge, one vote, majority wins). None of the judges are chat models — they answer structured questions (choice / noul / score) about a state blob.

## Quickstart (any provider)

Define judges entirely in `~/.config/clef-decide/config` (or via environment variables). See `docs/adding-a-judge.md` for the three-line pattern.

```ini
# ~/.config/clef-decide/config
judge_myjudge_endpoint=https://your-provider.example/v1/systemone
judge_myjudge_model=your-model-name
judge_myjudge_api_key=sk-...
```

Then:

```bash
bin/clef-decide --state-file state.md --questions questions.json --judge myjudge
```

The tool is LLM- and key-agnostic. The five named judges (`clef`, `clef-flash`, `jev`, `luna`, `subq`) are optional convenience defaults that work only if you have the corresponding provider keys configured. Prefer custom judges for your own setup.

See `docs/question-sets.md` for ready-to-use question files per phase and `docs/harness-insights.md` for state design, cost, and measurement practices.

## Judges

`--judge` selects the judge. Custom judges are defined with three config lines and can use any model name their endpoint accepts. Named judges are optional shortcuts.

### Panel votes

`--panel` fans one choice question out to the configured panel in parallel: one judge, one vote, majority wins. A tie re-runs once; a second tie exits 2 (never auto-picks).

Panel composition is a preference: `--panel-judges` flag > `$PANEL_JUDGES` > `panel_judges=` in config > all registered judges.

## Configuration

Key and endpoint precedence (first found wins):

- `--api-key` / `--endpoint` flags
- Environment variables (`$CLEF_API_KEY`, `$CLEF_ENDPOINT`, per-judge `$JUDGE_<NAME>_API_KEY`, etc.)
- `~/.config/clef-decide/config`

Custom judges never consult the default key chain. Missing key for a judge fails loudly when that judge is used.

## Hard rules (enforced)

- No retries (an unknown outcome may already be charged).
- Context budget: 16,384 tokens shared by state + questions (refused before sending).
- Gateway bounds: ≤32 questions, ≤64 options, 2–10 score levels.
- Panel: majority wins; double tie escalates with exit 2.
- Custom judges: https endpoint, own key, own model name.

## Layout

- `SKILL.md` — drop-in agent skill.
- `bin/clef-decide` — the CLI (Python 3, stdlib only).
- `docs/quality-loop.md` — six-phase workflow.
- `docs/question-sets.md` — per-phase question sets.
- `docs/harness-insights.md` — state design, judge selection, cost, measurement.
- `docs/adding-a-judge.md` — how to define an arbitrary judge in three lines.
- `docs/learnings.md` — operating learnings and principles behind the loop.
- `examples/` — worked examples, including `examples/reset/`, a worked run on a non-code task.
- `tests/` — fully mocked test suite.

## Tests

Fully mocked: no network, no keys, no charges.

```bash
python3 -m unittest discover -s tests
```

CI runs the same suite on Python 3.10, 3.11, and 3.12 on every push and
pull request (`.github/workflows/tests.yml`). The suite is hermetic: the
missing-key tests hide any real `~/.config/clef-decide/config`, so results
do not depend on the machine they run on.

The suite covers request shape, key handling, context budget, gateway
bounds, judge routing, the Luna decisions route, the SubQ route and its
key isolation, panel voting, panel composition preferences,
config-defined custom judges, skeleton-of-judgment, flag conflicts, and
error surfacing. Live calls are always opt-in: ask before any potentially
charged call, and never claim it worked without a real response.

## Credit

The tribunal voting rule at the heart of `--panel` (one judge, one vote,
majority wins, a double tie escalates to a human instead of being
auto-picked) comes from [Pgeon](https://pgeon.com), Thingscorp's agent
QA platform, where judge panels decide open questions for agents.

## License

MIT. See `LICENSE`.
