# State: memory purge (reset)

## Summary

The task was to purge an agent memory file of stale, finished, and interim entries, while keeping curated entries that carry rules. The loop ran on 2026-11-05 with all five judges (Clef, Clef Flash, Jev, Luna, SubQ). It terminated by a 5 to 0 vote. The file shrank from 43,188 bytes to 40,228 bytes, a cut of 2,960 bytes (about 6.9 percent). There was one disclosed executor override.

## Source

- Memory file before: 43,188 bytes.
- Memory file after: 40,228 bytes.
- Content mix: curated entries that carry rules, entries that recorded the owner's choices, and accumulated material such as finished tasks, interim states, and stale descriptions.

## Policy options put to the panel

1. **Delete all.** Turn memory off and start empty, following learning 8 in its strongest form.
2. **Keep all.** Treat the file as curated and leave it alone.
3. **Purge by standard.** Cut entries that are stale, finished, or interim. Keep entries that carry rules and entries that record current owner choices.

The vote was 5 to 0 for option 3. The reasoning recorded with the vote was that rule carrying memory differs from auto accumulated memory, so deleting everything would lose rules. Keeping everything would leave the slop in place.

## Triage passes

- **First pass: rejected.** One judge's triage cut nothing and marked every entry as keep. The tribunal rejected this pass as a rubber stamp. The reason given was that the pass applied no standard, so its result could not be told apart from not reviewing the file at all.
- **Rerun: accepted, 5 to 0.** The rerun used a sharper standard. Each kept entry had to name a rule it carries or a current choice it records. Each cut entry had to be shown to be stale, finished, or interim. This standard produced the cuts.

## Execution

- The executor applied the accepted cuts.
- **Override, disclosed.** One accepted cut targeted an entry that records a current owner choice. Under the adopted policy, current owner choices are kept, so the executor did not carry out that cut. The override was reported to the panel with the entry identified and the reason stated. No judge contested it at termination.

## Open items

- Decide whether the policy should be written down as a standing rule for future purges, so the sharper standard is the default.
- Turn the rejected rubber stamp pass into an eval case for judge triage.
- Look at how the cut that hit an owner choice got through triage. It suggests the standard should check owner choices explicitly.
- Schedule the next purge. Accumulated memory will grow back.

## What passed

- Strategy: 5 to 0.
- Purge policy (option 3): 5 to 0.
- Triage rerun: 5 to 0.
- Termination: 5 to 0.
- Result: 43,188 bytes to 40,228 bytes, with one disclosed override.
