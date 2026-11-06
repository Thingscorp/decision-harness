# Contributing

Thanks for helping improve decision-harness.

## Ground rules

- **Stdlib only.** The CLI (`bin/clef-decide`) is Python 3 with zero
  dependencies. Do not add a package requirement.
- **Tests are fully mocked.** No test may touch the network, a real API
  key, or a paid endpoint. Live calls are opt-in and never part of the
  suite.
- **Every claim in the README must be backed by a test.** If your change
  alters documented behavior, update the docs and the pinning tests in
  the same commit.
- **Judges are configuration, not code.** A new judge is three config
  lines (see `docs/adding-a-judge.md`), not a code path. Named judges in
  the source are optional convenience defaults only.

## Running the tests

```bash
python3 -m unittest discover -s tests
```

The suite is hermetic: results must not depend on the machine, its
environment variables, or a real `~/.config/clef-decide/config`.

## Pull requests

- Keep the change scoped; one concern per PR.
- Include the test run output in the PR description.
- CI runs the suite on Python 3.10, 3.11, and 3.12.
