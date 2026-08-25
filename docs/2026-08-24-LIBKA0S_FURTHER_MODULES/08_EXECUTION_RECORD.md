# 08 — Execution record

**Executed 2026-08-25.** Everything in `03_`–`07_` has been implemented, gated and committed
locally. **Nothing has been pushed.** Eleven repos were touched.

## What shipped

| Plan | Work | Result |
|---|---|---|
| `03_` A | LootHistory's chart-pool leak | fixed, `76e1791` |
| `04_` B | `Env` 1, `Pool` 1, `Item` 1, `Widgets` 6, `DebugLog` 11 | **LibKa0s v1.15.0**, tagged |
| `04_` B | re-vendor | 9 consumers, payload **and test kit** |
| `05_` C | `LibKa0s-Env-1.0` adoption | 9 addons |
| `06_` D | `Pool` + `Item` adoption | BankLedger, LootHistory |
| `07_` E | `Widgets.CopyWindow` adoption | BankLedger, LootHistory, MultiMeters |

Every commit landed behind `lua tests/run.lua` green and `luacheck .` at 0/0.

## Three things the plan got wrong, and what was done instead

**The release is v1.15.0, not v1.14.0.** The bundle was written 2026-08-24 naming v1.14.0 as next;
v1.14.0 shipped in the interim (*"testkit revision 12"*, `2c3a39c`) and is an ancestor of HEAD. New
majors added compatibly, so the successor is a minor bump. Corrected everywhere, with genuine
historical references to the real v1.14.0 deliberately left alone.

**The consumers owed a test-kit bump, and the two payloads cannot move apart.**
`tests/_kit/vendor_sync.lua`'s `DEFAULT_PAIRS` registers two cases — one for `libs/LibKa0s`, one for
`tests/_kit` — and compares **both** against the single tag greped out of `CLAUDE.md`. Rolling the
provenance line therefore obliges the kit to move with it. Eight of the nine consumers were still on
kit revision 11, a debt from skipping v1.14.0; MultiMeters was already on 12, which is why it alone
went green on the first attempt. `02_SPEC.md`'s non-goal ("no `tests/_kit/` re-vendor") was true of
the *library* and false of the *consumers*. Both are now corrected, and the pairing rule is written
into `04_PLAN_B` as Task 8 Step 1b.

**`perf = skip` is not a release-gate failure here.** LibKa0s ships no `tests/perf.lua` and that skip
is a permanent recorded condition (`docs/automated-tests/RESULTS.md:87`, `README.md:58`, a 2026-08-05
decision). The gate met was: lint pass, tests pass, complexity pass with zero functions above CCN 15,
perf the standing documented hole — the same gate every prior release shipped under.

## Two defects found by work that was supposed to be a formality

**The consumers table was wrong in six places** (`04_PLAN_B` Task 7). Most seriously,
**`LibKa0s-Media-1.0` had no row at all** despite all nine consumers looking it up in
`core/MediaSetup.lua` — it shipped at v1.9.0 into everyone at once and was never tracked. Also:
MultiMeters absent from five rows while consuming all five, and two ConsumableMaster rows naming
files that do not exist.

**The v1.14.0 changelog block had been overwritten in place**, destroying that release's notes rather
than merely misnumbering them. Restored byte-for-byte from `git show v1.14.0:CHANGELOG.md`, with the
v1.15.0 block split out above it.

## Deliberately left undone

`LibKa0s/LibKa0s/DebugLog.lua` keeps its own copy window — the fourth of the four. The reason is now
a comment beside `EnsureCopyFrame` (`bed64c1`): it is the smallest, it already lives inside the
library, and it is wired to `escClose` / `applySkin` / `dragBar`, which are file-locals. Converting
it is a `DebugLog` minor with its own API document, worth taking **after** the three host-side
adoptions have been seen in a live client.

That commit puts the library source one comment ahead of the v1.15.0 tag. The nine vendored copies
match the **tag** exactly, which is what `vendor_sync` compares, so every consumer is green; the
comment rides the next release.

---

# The in-client smoke checks — RECORDED, NOT RUN

**None of the checks below have been run.** Every agent in this execution was headless and could not
launch the client. Each is recorded in its addon's own `docs/smoke-tests.md`; this is the index.
Until they are run, the copy window's visual fidelity and every TOC-read path are **unverified**.

## The copy window — the highest-value checks

The three windows were three copies of one design, so the adoption is only correct if they still look
identical **to each other**. Nothing headless can see focus, selection or an Esc binding.

- **Cross-addon (do this one first).** Open the CSV export copy window in BankLedger, LootHistory and
  MultiMeters in **one** session and compare size, strata, backdrop alpha, monospace face and title
  placement. Any one differing from the other two means the descriptor is wrong — not that one host
  is nicer. Recorded in `LibKa0s/docs/api/Widgets/version-6-docs.md`, which has no single host.
- **MultiMeters** `docs/smoke-tests.md` §25 — `/mm` → Export → Export to CSV; centred above the
  modal, CSV pre-selected; Ctrl+C round-trips whole; Esc closes the copy window and leaves the modal;
  follows a dragged meter window; after `/reload` still one window, still centred.
- **LootHistory** `docs/smoke-tests.md` 17j — as above from History, plus: the **Insights** tab's
  `:Open` path reuses the SAME window, and with the History window closed it centres on screen.
- **BankLedger** `docs/smoke-tests.md` S-24 — as above from the ledger, plus: switching Data Set to
  Current View reuses the same window with new text selected, and the close glyph (now the library's
  18×18 red-hover control) is not clipped by the 26px title bar.

## Item and quality — BankLedger's F-006 refusal

- `docs/smoke-tests.md` S-23 — log in with `scriptErrors` on: zero Lua errors, proving
  `core\ItemSetup.lua` resolves before `core\Constants.lua` builds quality labels at file load.
  Then: the Minimum quality dropdown lists six quality-coloured localized names; `/bl show` and
  `/bl export` render the same quality words as before; and **with Minimum quality at Rare, an
  uncached item movement is recorded as skipped with cause `uncached` and is NOT guessed from the
  link colour.** That last one is F-006 and is the point of shipping primitives without a resolver.
- `docs/smoke-tests.md` S-18 — the degraded-install walk, now listing eight seams.

## The Env seam — the TOC read, per addon

Each is "the version the client shows comes from the TOC, not from a constant", and each has a
degraded twin ("rename `libs/LibKa0s` aside; it still answers").

- **LootHistory** 17i.1–17i.4 and 17a.5 — `/lh version` follows the TOC (prove by editing the TOC,
  `/reload`, reverting); zone + subzone reach the row, tooltip and export; **a loot on the first
  frames after a portal, before the client has zone text, buckets under Unknown and never as its own
  blank-named group**; exported rows still carry a mapID.
- **ConsumableMaster** step 16 + degraded section — `/cm version`, `/cm help`, `/cm config` → About.
- **WhatGroup** 2.16, 2.17, §Settings panel — `/wg version`, `/wg help` header, config landing page.
- **PrettyChat** T-97, T-98 — `/pc version`, the About tagline, and the degraded boot.
- **AbsorbTracker** items 94, 95 — `/at version` verbatim from the TOC (bump it by hand and
  `/reload` to distinguish the TOC read from the `NS.version` fallback), and the About blurb.
