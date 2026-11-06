# Panel question sets for the quality loop

Use these verbatim, filling in the IDs. The sets are judge-agnostic: any
judge on the panel (Clef, Clef Flash, Jev, Luna, SubQ) can answer any set, and
the default judge table below assigns each gate to its best-fit judge.
State shapes are suggestions — keep state concise (diffs, summaries,
records, reports), never the repo.

Call pattern:

```bash
bin/clef-decide --state-file state.json --questions questions.json
bin/clef-decide --state-file state.json --questions questions.json --judge jev
bin/clef-decide --state-file report.md --questions done.json --panel
```

`--model` is sent exactly as given, so a `clef:free` spelling survives verbatim.

## Default judge per phase

Specialize: one judge, one strength. Routine gates stay single-judge;
the panel (`--panel`) is for the loop-termination verdict and other
high-stakes calls.

| Phase | Gate | Judge | Why |
|---|---|---|---|
| 1 discovery | `coverage` (noul) | `clef` | nuanced judgment about what's missing |
| 1 discovery | `dedup_<pair>` (choice) | `clef-flash` | high-volume binary calls, speed wins |
| 2 risk triage | `risk_<F-ID>` (score) | `jev` | risk scoring is Jev's home turf |
| 3 triage | `triage_<T-ID>` (choice) | `clef-flash` | high-volume three-way classification |
| 3 severity | `severity_<D-ID>` (choice) | `clef` | severity needs the thorough reader |
| 4 fix review | `fix_review_<D-ID>` (choice) | `clef` | the thorough reader reviews the diff |
| 4 fix audit | (record) | `luna` | scored audit appended to the iteration report |
| 5 regression | `regression_clean` (noul) | `clef-flash` | fast re-verdict |
| 5 adversarial | `slipped_<area>` (choice) | `jev` | "what could still be broken?" |
| 6 termination | `done` (choice) | `--panel` | one judge one vote, majority wins |

Luna takes choice questions only; give her the fix audit as a choice
(`sound` / `needs_work`) and keep her scored rationale in the report.

---

## Phase 1 — discovery gates

State: `{repo, surfaces_covered[], feature_count, features: [{id, name,
surface}], discovery_method, areas_not_yet_examined[]}`

```json
{
  "coverage": {
    "type": "noul",
    "instructions": "Judge the proposition: this inventory documents every identifiable user-facing feature, screen, route, workflow, API interaction, configuration option, and business process in the codebase — nothing remains undocumented. The inventory summary and the areas not yet examined are in state.",
    "criteria": {
      "true": "The inventory is complete; no screen, route, workflow, API, or config is missing",
      "false": "At least one identifiable feature, screen, route, workflow, API, or config is missing or only partially documented"
    }
  }
}
```

For each suspected duplicate pair (`<A>`/`<B>` are the two Feature IDs):

```json
{
  "dedup_<A>_<B>": {
    "type": "choice",
    "instructions": "Two inventory rows may describe the same feature. Their names, user stories, and expected behaviour are in state. Decide whether to merge them.",
    "criteria": {
      "merge": "Both rows describe the same user-facing feature; merge into one row",
      "keep": "They are distinct features; keep both rows"
    }
  }
}
```

Exit: `coverage` true.

---

## Phase 2 — risk triage (batch up to 32 features per call)

One question per feature; `<F>` is the Feature ID. State per feature:
`{id, name, user_story, expected_behaviour, edge_cases, dependencies}`.

```json
{
  "risk_<F>": {
    "type": "score",
    "instructions": "Rate the defect risk of this feature from its complexity, dependencies, and user impact (details in state).",
    "criteria": [
      "Negligible: trivial, isolated, low impact",
      "Low: simple logic, few dependencies",
      "Medium: meaningful logic or several dependencies",
      "High: complex logic, critical path, or data-integrity risk"
    ]
  }
}
```

Suite-depth mapping: High → all 7 categories (happy, error, boundary,
invalid input, permission/security, performance, mobile); Medium →
happy + error + boundary + invalid input; Low → happy + error;
Negligible → happy path only. Major journeys get an end-to-end case
crossing features regardless of level.

---

## Phase 3 — failure triage, then severity (two separate calls)

`<T>` is a failure record ID. State: `{test_case, feature_id,
reproduction_steps, expected_result, actual_result, environment}`.

```json
{
  "triage_<T>": {
    "type": "choice",
    "instructions": "A test case failed. The failure record is in state. Judge what the failure is.",
    "criteria": {
      "real-defect": "The production code behaves incorrectly; file a Defect ID",
      "bad-test": "The test itself is wrong (bad expectation, wrong setup); rewrite the test and re-execute",
      "environment-flake": "The failure comes from the environment (missing dep, port conflict, timing); re-run in a clean environment"
    }
  }
}
```

Only for `real-defect` outcomes, in a follow-up call with the triage
outcome in state (`<D>` is the Defect ID):

```json
{
  "severity_<D>": {
    "type": "choice",
    "instructions": "Assign severity to this confirmed defect. The defect record is in state.",
    "criteria": {
      "critical": "Data loss, security breach, or core journey completely broken",
      "high": "Major feature broken or broken for a large user segment; workaround painful",
      "medium": "Feature degraded but usable; workaround exists",
      "low": "Cosmetic, typo-level, or edge case with minimal impact"
    }
  }
}
```

---

## Phase 4 — fix review

`<D>` is the Defect ID. State: `{defect_record, proposed_diff,
root_cause, files_touched}`.

```json
{
  "fix_review_<D>": {
    "type": "choice",
    "instructions": "Review the proposed fix for this defect. The defect record and the full diff are in state.",
    "criteria": {
      "accept": "Smallest safe fix: addresses the root cause, no scope creep, no new risk",
      "review": "Needs rework: too broad, misses the root cause, or introduces new risk"
    }
  }
}
```

`accept` → apply, verify locally, mark `fixed`. `review` → rework the
fix and re-ask. On a docs-only repo this phase stops at documenting
defects; each fix needs the owner's explicit order.

---

## Phase 5 — regression verdict

State: `{cases_rerun, passed, failed[], journeys_rerun[], new_failures[]}`.

```json
{
  "regression_clean": {
    "type": "noul",
    "instructions": "Judge the proposition: the regression re-run shows every test case passing, every major end-to-end journey green, and no new failures introduced by the fixes. The results are in state.",
    "criteria": {
      "true": "All green, no new failures, no broken journeys",
      "false": "Something still fails or a journey is broken"
    }
  }
}
```

New failures become new D-IDs and go back to Phase 3.

### Optional: incidents become evals

This addendum is optional. It extends Phase 5 and changes nothing above it.

Every production incident becomes an eval. Someone who knows the code confirms the incident case. The case is added to the regression set and re-run on every later iteration, so a shipped bug cannot ship twice.

Reviewer noise is tracked by disposition. Each reviewer finding is marked Fixed, Wrong, Intentional, or Ignored, so a noisy judge shows up in the counts instead of hiding in the volume.

```json
{
  "incident_eval_clean": {
    "type": "noul",
    "instructions": "Does the re-run include every confirmed incident case in the regression set, and does every one of those cases pass?",
    "criteria": {
      "true": "Every confirmed incident case is in the regression set and passes",
      "false": "An incident case is missing from the set, or one fails"
    }
  }
}
```

---

## Phase 6 — loop control (independent — same request is fine)

Single-judge form: `confidence` and `done` in one request to one judge.
For the termination verdict itself, prefer the panel variant below.

State: the iteration report — `{coverage_summary, features_tested,
defects_found[], defects_fixed[], remaining_risks[], sheet_summary:
{open_critical, open_high, failing_tests, undocumented_features}}`.

```json
{
  "confidence": {
    "type": "score",
    "instructions": "Rate overall confidence in this codebase's quality after this iteration, from the iteration report in state.",
    "criteria": [
      "0-20: major gaps remain",
      "20-40: many areas untested or defects open",
      "40-60: core covered, notable risks remain",
      "60-80: broad coverage, minor issues only",
      "80-100: complete coverage, no meaningful risks"
    ]
  },
  "done": {
    "type": "noul",
    "instructions": "Judge the proposition: ALL of the following are true — no undiscovered features, no failing tests, no open critical defects, no open high-severity defects, no unresolved UX issues, no incomplete user journeys. The iteration report and sheet summary are in state.",
    "criteria": {
      "true": "Every exit criterion is satisfied; the loop may stop",
      "false": "At least one exit criterion is not satisfied; the loop must continue"
    }
  }
}
```

If `done` is false, loop back to Phase 1. If the gate refuses `done`,
keep trying: re-run the verdict; if the refusal is stable, strengthen
the work (more discovery, more fixes) and re-ask. The sheet must agree
mechanically — both must say go before anything is called done.

### Panel variant (recommended for termination)

`--panel` needs exactly one choice question. Reframe `done` as a choice
and let the tribunal vote — one judge, one vote, majority wins (the
tribunal rule is Pgeon technology, https://pgeon.com; who sits on the
panel is a preference, see `--panel-judges` / `panel_judges=`):

```json
{
  "done": {
    "type": "choice",
    "instructions": "ALL of the following are true — no undiscovered features, no failing tests, no open critical defects, no open high-severity defects, no unresolved UX issues, no incomplete user journeys. The iteration report and sheet summary are in state. Vote done only if every criterion is satisfied.",
    "criteria": {
      "done": "Every exit criterion is satisfied; the loop may stop",
      "not_done": "At least one exit criterion is not satisfied; the loop must continue"
    }
  }
}
```

```bash
bin/clef-decide --state-file report.md --questions done.json --panel
```

A tie re-runs once; a second tie escalates to the owner (exit 2) —
never auto-pick, never call it done on a tie.

### Optional: scored convergence gate

This addendum is optional. It extends Phase 6 and does not change the panel variant above or any existing gate.

Review rounds are scored with a score question on a 1 to 10 scale, using the criteria bands below. The owner sets the ship bar before the first round. The source practice used 9.5. The owner also sets a hard round cap, and the cap is recorded in the iteration report.

Rounds stop at the bar or at the cap, whichever comes first. If a run stops at the cap without reaching the bar, the report says so and does not record it as a pass.

Without a cap, review loops balloon. In the source practice, a forgotten loop grew a PR to 80,000 lines.

```json
{
  "convergence": {
    "type": "score",
    "instructions": "Rate the final review score state against the owner's ship bar and the recorded round cap.",
    "criteria": [
      "1-3: Blocking findings remain open, or no round cap was recorded in the iteration report.",
      "4-6: Major findings remain open. The final score is well below the ship bar.",
      "7-8: Only minor findings remain. The final score is close to the ship bar but has not reached it.",
      "9-10: The final score meets or exceeds the ship bar within the recorded round cap, with no open blocking findings."
    ]
  }
}
```

## Optional cycle hardening gates

These gates are optional. They harden any loop run, whether or not it produces code. Each one traces to a failure observed in real runs on 2026-11-05. Add a gate to a cycle's question set wherever the failure it prevents is possible.

### preflight_ready

Before a cycle starts, run one cheap probe per external dependency the run will need. Confirm that judge endpoints answer, that repo auth can write to the target, and that file grants are verified by byte size. The gate asks whether every dependency probed ready. It prevents a credential wall discovered after all content was built.

```json
{
  "preflight_ready": {
    "type": "noul",
    "instructions": "Judge the proposition: before the cycle started, one cheap probe ran for each external dependency the run needs (judge endpoints answer, repo auth can write to the target, file grants verified by byte size), and every dependency probed ready.",
    "criteria": {
      "true": "The run record shows one probe per needed dependency, each with a ready result, logged before any cycle work began.",
      "false": "A needed dependency was not probed, a probe failed, or probing happened after cycle work had started."
    }
  }
}
```

### no_rubber_stamp

Ask this after any judge pass that changed nothing: zero cuts, zero findings, or a straight accept. The gate asks whether the pass applied the stated standard entry by entry, with reasons a rerun could check. An empty result is allowed. An unexplained one is not. It prevents a purge judge whose first pass cut zero lines and read as thorough.

```json
{
  "no_rubber_stamp": {
    "type": "noul",
    "instructions": "Judge the proposition: this judge pass, which changed nothing, applied the stated standard entry by entry and gave reasons a rerun could check.",
    "criteria": {
      "true": "The pass output addresses each entry against the stated standard and gives a specific, checkable reason for keeping it.",
      "false": "The pass gives a blanket verdict, skips entries, or offers reasons too general for a rerun to confirm or refute."
    }
  }
}
```

### schema_conformant

Check every structured output mechanically against its consumer's schema before assembly. The JSON must parse, required fields must be present, and no extra fields may change meaning. The gate asks whether that check ran and passed, with any format repair disclosed in the run record. It prevents three outputs arriving in a shape the helper could not consume, and a conversion that silently drops a criteria map.

```json
{
  "schema_conformant": {
    "type": "noul",
    "instructions": "Judge the proposition: every structured output was checked mechanically against its consumer's schema before assembly (JSON parses, required fields present, no extras that change meaning), the check passed, and any format repair is disclosed in the run record.",
    "criteria": {
      "true": "A mechanical check ran on every structured output before assembly, all outputs passed, and the run record lists each format repair made.",
      "false": "An output was not checked, a check failed, or a repair (such as a conversion that dropped fields) is missing from the run record."
    }
  }
}
```
