# Verification

Every number here was re-run by hand after the agents finished, not copied from their reports.

## The four-suite gate, all eleven repos

| Repo | lint | tests | perf | complexity |
|---|---|---|---|---|
| LibKa0s | 0/0 in 18 files | 762 / 0 | no offline scenarios (recorded disposition) | max CCN 14 |
| Absorb Tracker | 0/0 in 27 | 544 / 0 | 6 scenarios | 0 over threshold |
| Bank Ledger | 0/0 in 28 | 830 / 0 | none shipped | 0 |
| Consumable Master | 0/0 in 59 | 744 / 0 | 4 scenarios | 0 |
| KickCD | 0/0 in 36 | 836 / 0 | 5 scenarios | 0 |
| Loot History | 0/0 in 28 | 699 / 0 | none shipped | 0 |
| Multi Meters | 0/0 in 45 | 1486 / 0 | 13 scenarios | 21 recorded, identical to master |
| Panel Master | 0/0 in 27 | 760 / 0 | none shipped | 0 |
| Pretty Chat | 0/0 in 18 | 295 / 0 | none shipped | 0 |
| What Group | 0/0 in 16 | 528 / 0 | none shipped | 0 |

Multi Meters' 21 complexity warnings are pre-existing and unchanged — master reports the same 21. The
suite records complexity without gating on it outside a release, where `bump-version` evaluates it.

Every repo was re-tested *after* committing, because `.gitattributes` renormalizes line endings on
commit and that rewrites working-tree bytes. All nine stayed green and clean.

## Requirements checked against the schemas, not the reports

- **1a** — all nine call the `MasterControls` composer; the tab leads the General strip in each.
- **1c** — every colour row enumerated across all nine. Three of Multi Meters' carry a
  `...ColorMode` dropdown with `classColorSource` and a class value, which §17 names as the *richer*
  form and forbids converting back to a checkbox. `statColors.<stat>` is the palette-definition
  exemption §17 carves out. Bank Ledger, Loot History, Panel Master, What Group and Pretty Chat have
  no raw colour rows at all — all via composers or none to have.
- **1h** — Consumable Master, Loot History and Multi Meters all reach the shared `ReorderList`; no
  consumer-drawn handle or row box left double-drawing.
- The addon-specific items were each confirmed present in source.

## The LibKa0s tag

The addons' vendor-sync tests compare their vendored copy against `git show v1.24.0:` in the sibling
checkout, so an untagged library failed two tests in all nine. `v1.24.0` was tagged and pushed. The
payload matched the tag byte-for-byte on the first try — Multi Meters went from 2 failures to
1458/1458 with no other change, which is itself the evidence that the re-vendor was clean.

## Two workflow failures worth recording

**The spec-revision agent died twice**, both times exceeding the 64k output cap while regenerating a
large spec wholesale. The first time this was silent and expensive: `agent()` answers `null` on a
terminal error, so `finalSpec` became `null` and both upstream implementers received the literal
string `"null"` where the design should have been. They still had every requirement — those live in
the shared context, not the spec — so they produced real work, but built to their own invented API
rather than the designed one, which would have desynced the adoption contract the nine addons then
followed.

Caught by reading the journal rather than the summary. The attempts were preserved on
`wip/null-spec-attempt` in both repos and handed to the real implementers as prior art to mine but
not to trust. The guard is now `(revised && revised.adoptionContract) ? revised : spec` — a dead
reviser falls through to the reviewed-but-unrevised spec instead of erasing it.

**A verifier passed a target while logging important issues.** LibKa0s came back `passed: true` with
two important findings, and the repair loop only fires on failures, so both would have shipped. One
was the real `SubTabStrip` lifecycle bug. A verdict that says "passed" while listing important issues
should route to repair on the issue list, not on the boolean.
