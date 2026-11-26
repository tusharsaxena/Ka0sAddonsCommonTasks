# Execution record

Two workflows built this bundle: `wf_bac662d6-7aa` (ISR3-LK-01 to ISR3-DW-06 and their review fixes, run in parallel with
CombatTrail's Combat Sequence) and `wf_7d6d3e02-5b9` (the owner's 2026-11-26 addenda, ISR3-DW-07 to DW-09, plus
CombatTrail's CSEQ-4). Builders worked in `~/ka0s-scratch/isr3/<Repo>`. Nothing is merged yet: every branch waits on the
owner's go-ahead.

## Branch heads (pushed)

| Repo | Branch | Head | Retail | Forever | luacheck | seeds | perf |
|---|---|---|---|---|---|---|---|
| LibKa0s | feat/2026-11-25-item-search-round3 | 966a08cd | 5260/0 | 5260/0 | 0/0 | n/a | n/a |
| DropWatcher | feat/2026-11-25-item-search-round3 | b71ee69 | 2842/0/119 | 2844/0/115 | 0/0 (303) | 33 | green both clients |
| CombatTrail (Combat Sequence) | feat/2026-11-25-combat-sequence | 56b0ca6 | 1813/0/3 | 1803/0/3 | 0/0 (218) | 37 | green both clients |

The lead re-ran the Drop Watcher and CombatTrail gates on these heads on 2026-11-26. The LibKa0s tag `v1.117.0` exists
locally on 966a08cd and is **not pushed**; it is pushed with the merge.

## What was built

- **LibKa0s v1.117.0 (ISR3-LK-01).** ForeverDB minor 4: spawn spots read `spz`, then `spm`, then `spw` converted to map
  positions over `umaa` and `zbord`; `VendorPriceAt` and `vendx`; `FullStatus`, `LoadFull` and `FullCost`. Kit revision 65.
  The `spw` conversion was measured against the spots that have both: the map pick agrees on 1428 of 1517 (94.1%), the
  position error is median 0.89% and p90 2.53%, and 11637 of 14360 world spots convert.
- **Drop Watcher ISR3-DW-00 to DW-06.** Re-vendor; glyphs at one size, the column inset, header hover and LootHistory-style
  sort triangles; skill breakpoints on tooltip recipe rows; the hairline and label line in place of the header text;
  game-style quest marks with a ready state; rank colors on Source and Type; test sources out; a Gathered from tab;
  recorded vendor prices and "<Side> only" in place of "can't buy"; the key's hover/toggle rule; the Keep / Hold / Sell /
  Toss badge with a 0–100 score, a confidence and its reasons.
- **ISR3-DW-07.** The tooltip shows 3 rows per section by default (was 5), still 1 to 20. A profile that had chosen exactly
  5 stored nothing (AceDB strips defaults) and now reads 3.
- **ISR3-DW-08.** A not-known recipe in the window's Crafting tab says where it is learned. The generator joins each recipe
  to its teaching item from the client data (1,966 of 2,466 recipes; the other 500 read "Trainer"). The Status cell shows the
  recipe item's best source (vendor, then quest, then drop, then World drop), the row tooltip lists them, and a click opens
  the recipe item. New seed bundle `docs/seed-research/2026-11-26-forever-recipes` (build 1.60.1.70938).
- **ISR3-DW-09.** Tooltip anchor audit of every Item Search tooltip (17 surfaces). All were already owned at ANCHOR_NONE and
  placed by the standard. The Makes cell and the other item tooltips drifted because an uncached item's tooltip grows after
  it loads; they are now placed again when they grow and on the next frame.
- **CombatTrail CSEQ-1 to CSEQ-4.** See CombatTrail's `docs/superpowers/specs/2026-11-25-combat-sequence-design.md`.

## Review

Each workflow ended with an independent read-only review per repo and a fix pass.

- `wf_bac662d6-7aa`: vendor price recording now waits out combat; the badge holds gear the gear verdict has not answered
  (never Toss); a verdict test was split back under CCN 15; a rich item hover joined the offline perf.
- `wf_7d6d3e02-5b9`: the reviewer rebuilt the recipe join from the raw tables with its own script (0 mismatches of 2,466).
  Fixed: README said five rows; a test now asserts the waypoint arrow's tooltip anchor; the smoke row names the "chose 5"
  case. CombatTrail: one doc re-wrap.

## Calls made without asking

- **ForeverDB_Full loads on the first window open** (`itemSearch.fullDB = "window"`), the owner's "World coords, then Full".
  It costs about 82 MB and half a second once, never in combat or from a tooltip. "never" is available.
- **Recipe sources:** a quest-spell recipe reads "Trainer"; a No-profession row names its first recipe item without reading
  sources (Rune Thread has about 300 recipes); the tooltip caps each kind at 6 rows.
- **The CombatTrail detached window's chips and Resume** are filter-bar chrome under the standard, so their tooltips now open
  centered above the control instead of beside the window. The owner's "to the right" note was about a body element. A
  deviation row is needed if the owner wants them beside the window.
- **Main-window item tooltips** (outside Item Search) keep the old placer; their items are cached.

## Smoke owed (owner)

- Drop Watcher: ITEM-SEARCH-31 to 46, and probes P-QREADY, P-GOSSIP, P-FULL, P-W2M.
- CombatTrail: SM-CT-SQ1 to SQ11.
