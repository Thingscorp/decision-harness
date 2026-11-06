# Learnings for loop operators

These are operating principles distilled from Theo Browne's stream of November 4, 2026. The numbers are as he reported them. We have not verified them independently, except where the last section reports our own runs.

Each entry gives the principle, the source numbers, and where it plugs into decision-harness. Read them as guidance for running the loop, not as new rules the loop enforces.

## 1. Human attention is the bottleneck

Tokens are cheap and so is code generation. The scarce resource is the human who has to look at the result. The agent should not bother the human until the work is ready to merge.

Source: his agents reach about 80 percent of PRs mergeable on first look.

Plugs in: the tribunal takes the judgment calls that would otherwise interrupt the human. Escalate to the human only after a termination vote.

## 2. Gardeners, not builders

Tend the environment the agent works in. When an agent errs, fix the problem at the highest layer available. Codebase architecture comes first, static analysis second, and prompt and skill instructions last. Remove the holes in the floor. Do not hand the blind agent better directions.

Source: stated as a working rule, no figures.

Plugs in: when the panel finds a defect, ask it which layer the fix belongs in before anyone patches a prompt.

## 3. Verification is the multiplier

A model that can check its own work produces much better output. The agent must show the output. Saying it is done is not enough.

Source: Boris, the creator of Claude Code, puts the gain at 2 to 3 times better output when the model can verify its own work.

Plugs in: the agent's legwork should end in evidence the judges can inspect, such as test output, diffs, and logs. A bare claim of completion goes back to the agent.

## 4. Review is spellcheck, not a gate

Review exists to catch mistakes cheaply. It is not a checkpoint to pass. The metric is human time. Reverts and incidents are the guardrails. Measure reviewer noise by how the human disposes of each comment: Fixed, Wrong, Intentional, or Ignored.

Source: at Anthropic, the share of review comments that were substantive rose from 16 percent to 54 percent once AI reviewed every PR.

Plugs in: record a disposition for each judge finding. A judge whose findings are mostly Wrong or Ignored is costing attention, not saving it.

## 5. Reviews must converge

Score the work from 1 to 10. Do not count comments. Set a ship bar, such as 9.5, and cap the number of rounds.

Source: a forgotten review loop grew one PR to 80,000 lines. Anthropic ran 50 plus rounds overnight.

Plugs in: termination is a tribunal vote against a score and a round cap. Set both before the loop starts.

## 6. The Council

Rival model families should review the same change. Two reviewers from the same family are the same reviewer at a different time of day. One judge can be a jester whose vote does not count. Scoring can run against taste: severity, future problems, how likely something is to annoy the owner, or even iterating until a named person would be happy.

Source: over 144 scored rounds, average scores went from 7.4 to 8.9, and 128 of the 144 rounds scored 9 or higher. The council caught 3 real security holes. One was revoked shares that still served content from the browser cache.

Warnings: it is a token furnace. A 200 dollar plan's weekly limit was gone in 2 to 3 days. One thread spawned 600 plus subagents and grew a change from 1,000 lines to 20,000. It is viable only on flat rate subscriptions, not at API prices.

Plugs in: this is the panel. Keep its judges on different families, and watch the cost before raising round caps.

## 7. Slop tests

For every test, ask one audit question: can this test actually fail?

Source: he deleted 258,000 lines and about 11,000 tests, then restored 4. No deleted test would have caught a regression.

Plugs in: put the question to the panel whenever the agent offers tests as evidence. A test that cannot fail is not verification.

## 8. Turn memory off

His audit of agent memory found stale diagrams, finished tasks, and interim states. Memory is a firehose of slop aimed at your agent. He disabled it and his results improved.

Caveat from our own run: curated memory that carries rules is a different animal from memory that accumulates automatically. The purge discipline matters more than the delete key.

Plugs in: run the loop on the memory file itself, as shown in examples/reset.

## 9. Most friction is one unasked conversation

Engineers hand massaged a JSON blob for months. One conversation with the owner of the API fixed it. Agents endure friction forever instead of complaining, so go find the JSON blob.

Source: anecdote, no figures.

Plugs in: ask the panel to name repeated workarounds in the agent's legwork. Each one is a candidate conversation for the human.

## 10. Failures are the dataset

Log every inference request and response through your own proxy. Mine the failures into evals. Every incident becomes an eval that an engineer confirms, and the reviewer is re-run against those evals daily. Data on subagent orchestration is the scarce moat the labs protect.

Source: his six months of logs come to about 500 billion tokens in about 6 gigabytes.

Plugs in: keep every run's state and votes. Rejected passes and overrides are eval material.

## 11. Code is disposable

About half his PRs never merge, by design. Starting is cheap and closing is free.

Source: his operation runs about 20 trillion tokens a day. One colleague ships about 400 PRs a day.

Plugs in: abandoning the work is a legitimate termination outcome. Do not push weak work through the loop to avoid closing it.

## Proven in this repo's own runs, 2026-11-05

We ran the loop on two tasks that were not code. The first pruned a skills document. The second purged an agent memory file.

- The strategy vote was 5 to 0, and the termination vote was 5 to 0.
- The purge policy passed 5 to 0.
- On the first pass, one judge cut nothing. The tribunal rejected that pass as a rubber stamp. The rerun passed 5 to 0, and its sharper standard produced the cuts.
- The memory file went from 43,188 bytes to 40,228 bytes.
- There was one disclosed executor override. One cut targeted a current owner choice, so the executor did not carry it out. The override was disclosed to the panel and recorded.

What this shows: the tribunal will reject a pass that does no work, even when every judge agreed on the policy. It also shows that curated memory needs judgment, not deletion. The full state is in examples/reset.

## Cycle hardening, 2026-11-05

The panel tested the loop cycles against the failure evidence from the night of 2026-11-05. It voted unanimously for improvement bundle A (5 to 0, mean 0.928).

**Truncation rule.** Any smart LLM run that ends with finish reason `length` is incomplete by definition. A continuation pass is mandatory before assembly. The run record carries the finish reason of every run. This failure was observed twice in one night, once mid sentence in a deliverable appendix.

The other three fixes:

- **Rubber stamp triage:** a judge pass that changes nothing must show it applied the standard entry by entry, with checkable reasons.
- **Schema conformance:** structured outputs are checked mechanically against the consumer's schema before assembly, and repairs are disclosed.
- **Preflight:** every external dependency is probed before a cycle starts.

These fixes are available as optional gates in docs/question-sets.md under "Optional cycle hardening gates".

Open items:

- A gate proven only on synthetic records is claimed, not proven, for real use. Until a gate has run on real records, treat it as claimed.
- A tribunal dissent carries no rationale in the current vote format. Nobody has fixed this yet.
