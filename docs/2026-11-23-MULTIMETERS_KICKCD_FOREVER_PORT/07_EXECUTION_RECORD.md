# Execution record

Run 2026-11-23, branch `feat/2026-11-23-multimeters-kickcd-forever-port`. Built by workflow `wf_c1c41cd9-e5c` in scratch
clones (9 agents: KickCD in four stages, MultiMeters in one, one independent review and one fix pass per repo).

## Outcome

| Repo | Items | Head | Gate at merge |
|---|---|---|---|
| KickCD | MKF-KC-01..13, 15..18, REV (KC-14 is an exceptions row) | 21c9a65 | Retail 1904/0/1, Forever 1894/0/11, luacheck 0/0, max CCN 15 |
| MultiMeters | MKF-MM-01..04, REV (MM-00 is an exceptions row) | 414ee58 | Retail 2682/0/1, luacheck 0/0 (Retail only) |
| WowAddonStandards | MKF-STD-01 | 49145b3 | check-standard passed; no version bump |

MultiMeters stacked on `fix/2026-11-23-r2-restore-probe-fixes`, which merged first.

## Decisions the run took (owner may revisit)

- **KC-REV-4, R8 reading.** On the live class, admission is "known, or on the live class's own Forever list". A spell
  on another class's list is admitted only when editing that class. Stricter than "any KickCD list"; the owner was told.
- **KC-REV-2, test harness.** Under the forever kit profile the shared instance stays Retail-shaped; Forever behavior is
  tested through the opt-in Forever world. Recorded in KickCD `docs/testing.md`. Follow-up: make the Forever world the
  default there (about 195 Retail-only cases to pin).
- **Seed order.** `seeds.py apply` orders by id, so the list order (Pummel first) was set by hand, as validate-seeds
  allows. Death Coil keeps category fear.
- **MM-03.** The header note keeps its count with new wording; diagnostics gained a "withheld" bucket.
- **KC-16.** The GCD log mark is unchanged; on Forever it never fires, and the probe records what the GCD read answers.

## Smoke

Not run before the merge: the owner gave the go-ahead on 2026-11-23 with the smoke sheet outstanding
(`Documents/Ka0sPendingSmoke-2026-11-23.csv`, run "MKF 11-23": KickCD SPELLS-19..24, FOREVER-1..16; MultiMeters
INSTALL-19, COMBAT-31..33). Failures found there are fixed on master as follow-ups.

## Smoke result (2026-11-24)

The owner reported on 2026-11-24 that all 26 checks of run "MKF 11-23" passed, in chat: KickCD SPELLS-19 to SPELLS-24
and FOREVER-1 to FOREVER-16, and MultiMeters INSTALL-19 and COMBAT-31 to COMBAT-33, each on the client it names.
Recorded on the owner's word; each check's `Result:` line in its addon's `docs/smoke-tests.md` reads
`pass (owner, 2026-11-24)`.
