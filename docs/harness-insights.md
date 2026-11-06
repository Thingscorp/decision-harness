# Harness insights for decision-harness

Lessons from large-scale coding-agent harness comparisons (fixed model, varying scaffold) applied to decision-harness’s decision calls.

A decision harness = the state you send + the questions + the judge chosen + context rules + compaction. Small differences in these produce large swings in reliability and cost, just as they do for coding agents.

## Core observations

- Scaffold differences routinely exceed model differences. A mediocre harness on a strong judge can lose to a good harness on a cheaper judge.
- Rankings do not transfer. The best state format or judge for coverage gates is not the best for fix-review or termination.
- Cost per reliable judgment matters more than raw accuracy. Expensive full-panel calls on routine gates are usually waste.
- Lightweight, high-signal state often beats verbose dumps. Bash-only style simplicity (concise diffs, failure summaries, explicit criteria) frequently wins.
- Document the actual differences (prompts/questions, tools/state shape, compaction strategy) and measure them. Anecdotes are not enough.

## Practical recommendations for decision-harness

**Judge selection**
- Default high-volume gates (coverage, risk, triage, severity) to the cheapest sufficiently reliable judge (clef-flash or subq).
- Reserve full panel (`--panel`) and Luna scored audits for termination, high-stakes fix review, and final confidence.
- Test combinations on your actual workload; do not assume one configuration is universally best.

**State design (the dominant lever)**
- Keep state under the 16k budget with room to spare. Prefer structured, minimal evidence: key diffs, failing assertions, current sheet status, prior verdicts.
- Avoid dumping whole files or long logs. Extract the signal first.
- Use `--sot` when independent sub-judgments would otherwise starve each other of context.
- Version and document the state templates that actually move verdict stability.

**Questions and criteria**
- Make criteria explicit and mutually exclusive. Ambiguous options inflate cost and variance.
- Batch independent questions; never chain dependent ones in one request.
- Prefer choice/noul for gates that need a hard pass/fail; reserve score for relative ranking or confidence.

**Cost and iteration**
- Track tokens or estimated cost per successful gate exit, not per call.
- When a gate is flaky, first tighten the state and criteria before switching to a more expensive judge or full panel.
- Stop optimizing a particular gate once additional changes produce <5–10% relative improvement in stability or cost on repeated runs.

**Measurement**
- Maintain a small private log of (gate type, judge, state style, outcome stability, approximate cost).
- Periodically re-evaluate top configurations the way a harness leaderboard does: fix the model/judge, vary only the surrounding harness.

These practices keep the agent doing the legwork and the panel doing the judging, while reducing waste and increasing the reliability of the loop.
