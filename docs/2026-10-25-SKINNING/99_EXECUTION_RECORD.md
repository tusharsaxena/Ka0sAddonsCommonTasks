# Execution record — skinning, leg 1

(Written during execution: outcomes per milestone, deviations, local-tag moves, review fix rounds, lead calls.)

## Heads at the stop (2026-10-25)

| Repo | Branch head | Commits on the branch | Pushed |
|---|---|---|---|
| WowAddonStandards | `b9ee560` (WS-90, standard v2.89.0) | 4 | yes (branch + `ka0s-review` notes) |
| LibKa0s | `65a23cb` (= local tag `v1.78.0`) | 28 | branch + notes yes; **tag no** |
| LootHistory | `1c010e8` (LH-05 review fix) | 14 | yes (branch + notes) |
| Ka0sAddonsCommonTasks | this record | — | yes |

Nothing is merged. No addon version was bumped.

## M0 — plan review

The adversarial plan review produced 68 raw findings, folded into 19 resolutions, 3 new items (LK-11, WS-02, LH-06)
and 7 rejections (`plan-data/plan-review.json`, commit f4d68f7).

## M1 — upstream (run `wf_b2aa3b31-5e0`, 01:36 → about 10:21)

- **Result:** 17 of 17 items landed and reviewed. None failed or reported a library gap.
- **Gates:** LibKa0s luacheck 0/0 in 223 files; tests 3001 passed, 0 failed, 2 skipped. The standard's
  `check-standard.sh` passes all checks at v2.89.0, with anti-patterns #1–#107.
- **The tag:** LK-90 cut `v1.78.0` at `948007c`. Its review fix `fb7b7a3` touched only the CHANGELOG and
  `releasing.md`, adding DpsRace to the TestStrip hosts. The lead moved the local tag to `fb7b7a3`; the payload
  did not change.
- **Pace:** about 40 minutes per LibKa0s item, review and fix round included. The status report's estimate,
  made after the first 4 items, was too short.

## M2 — LootHistory (runs `wf_15a32176-ae2`, `wf_11a56594-673`, `wf_3eac422b-dbc`, `wf_5e1e846a-d9b`, `wf_4b737fe1-53f`)

**Result:** 12 of 12 items landed and reviewed: the 7 planned and 5 addenda. LootHistory luacheck 0/0 in 148 files;
tests 1782 passed, 0 failed, 1 skipped. **Every `tests/*_golden.txt` is byte-identical to master**, so Ka0s Default
reproduces the old look for every pinned surface.

### Owner-reported defect: LibSharedMedia "invalid file" (LK-A1)

- **Report:** after LH-RV, the owner saw BugSack errors from many addons:
  `LibSharedMedia-3.0: Attempt to register an invalid font/file ('Interface\AddOns\<Addon>\libs\LibKa0s\media\...')`,
  thrown from `LootHistory/libs/LibKa0s/Media.lua` while running `PremadeGroupsFilterExtension` and
  `PartyFrameEnhanced` `core/MediaSetup.lua`.
- **Cause:** LibStub keeps the highest minor. Every addon loading after LootHistory ran Media 6's `RegisterLSM`,
  which offered the new skin faces and Glass art at that addon's own v1.77.0 folder, where the files do not exist.
  LSM-3.0 validates the file *before* its first-registration-wins check, so the later registrations were not
  silent, contrary to the docblock.
- **Fix:** LK-A1 (`d8ac604`, Media 7) skips a key LSM already holds. Lead review inline, recorded as a note.
- **Interim:** the owner was told to disable LootHistory until LH-RV2 (`068e70f`, 12:37) re-vendored the fix.
- **Residual, documented in Media.lua:** a host that vendors Media 7 and never calls `RegisterLSM` could leave a
  key unheld. No Ka0s addon does that, and leg 2's re-vendor removes the case.

### Library gaps found by addon items (the RESUME §5 / tag re-cut rule)

- **LH-03 (bind-state colors):** the gap became LK-A2 (`dfbd0a1`, SkinDefs 5). It added nine Semantic tokens,
  `sem.bound*`, `sem.bound*Alt` and `sem.danger`. `sem.danger` = 1, ⅓, ⅓ keeps `|cffff5555` byte-exact; `sem.bad`'s
  .33 would encode ff5454. The new contrast test showed Azeroth needs dark overrides for all nine.
- **LH-04 (about ten more constants):** the gap became LK-A3 (`d6b5bec`, SkinDefs 6). After the second stop, the
  lead ruled that one sweep should cover every surface left to LH-04, LH-06 and LH-05, so no third stop came. It
  added 11 tokens: `text.value`, `text.bodyAlt`, `text.subtle`, `text.highlight`, `gtip.value`, `gtip.subtle`,
  `icon.dim`, `sem.goodAlt`, `sem.badAlt`, `sem.warbandAlt` and `sem.unknown`. The schema is now 235 tokens.
- **Re-vendors:** LH-RV2 (`068e70f`) and LH-RV3 (`b4a218e`) brought each re-cut into LootHistory.

### Local tag moves (never pushed)

`948007c` → `fb7b7a3` (M1) → `a3790f4` (LK-A1) → `7ec0e0a` (LK-A2) → `65a23cb` (LK-A3).

Each re-cut followed a clean-tree `run-automated-tests.sh --release 1.78.0`. The records in LibKa0s are
`docs/automated-tests/20261025-113223/`, `-122953/` and `-134526/`. Each has its own `ANALYSIS.md`, and the
CHANGELOG release-gate line names it. Final figures: 3006 passed, 0 failed, 2 skipped; complexity max CCN 15,
0 warnings; perf not measured, because LibKa0s has no `tests/perf.lua`.

### Lead calls (recorded in `plan-data/addendum-01.json` / `-02.json` as `rulings`)

1. Delete and Forget take `sem.danger`, not `sem.bad`, to keep the byte-exact color.
2. LH-02's binding resolution applies to LH-03..LH-05: under Ka0s Default, keep the same paint calls in the same
   order, arity and objects, and keep the goldens clean.
3. AH status colors map to the exact `sem.statusOk` / `statusWarn` / `statusBad`.
4. A value with no exact token is a gap only when a golden or a test pins it. Otherwise the item takes the nearest
   token and names the visible change. Two such changes landed: the "Source inferred" tooltip line, .62 → .5
   (LH-03), and the strip tooltip body lines, 1 → .9 (LH-02).
5. `execute_milestone.js` now tells implementers to read the addendum `rulings`. This is a tooling change only; the
   plan text is untouched.

### Notable item deviations (full text in each item's commit body)

- **Primitives not used:** LH-02 tabs and LH-03 table rows don't use `S.Tab` / `S.ListRow`, and the LH-04 Timeline
  toggle doesn't use `S.Checkbox`. On Ka0s Default those primitives would draw different paint calls, so these
  surfaces keep their own textures with token colors, repainted by a host walk. 03_SPEC §6 allows this.
- **Fonts:** LootHistory's own GameFont* text (table cells, Insights, Timeline, Holdings, the AH table) keeps the
  client font. Its layout is measured against that font and the goldens pin it. Skin fonts reach the facade
  primitives and the AceGUI controls. This is noted in SK-05 and recorded in LootHistory's ARCHITECTURE as a
  leg-2 item.
- **Owner-bound AceGUI paint:** LH-06 publishes its own seam functions (`NS.SkinPaintAce`, `SkinPaintAceTree`,
  `SkinOnRelease`) over the public `Skin:PaintAce` / `PaintAceTree` / `OnRelease`. The facade has no PaintAce, and
  surface parity forbids adding keys to it.
- **Color gate:** LH-05 adds a color-literal gate (`tests/test_skin_literals.lua`) with a 5-entry allow-list.

### Review fix rounds

- **M2:** LH-01, LH-02, LH-03, LH-05 and LH-RV2 each had one, all doc, comment or count ripples. LH-RV3's
  working-tree file had LF line endings; it was re-checked-out, with no new commit.
- **M1:** LK-02, LK-03, LK-04, LK-05, LK-07, LK-10, LK-11 and LK-90 each had one.

## Leg-2 items surfaced by this run

- **Every addon:** re-vendor v1.78.0, adopt the skin owner, and apply the HUD reset to "From skin" (OWNER_SCOPE R3).
- **PGFE:** move it onto the library's EllesmereUI provider.
- **Azeroth tooltips:** GameTooltip lines that take `sem.good` / `sem.bad` (Timeline Gained/Lost) get Azeroth's dark
  ink on the always-dark tooltip. They need a gtip-specific pair.
- **Fonts:** the skin font doesn't reach LootHistory's own GameFont* text (see above).
- **Split tokens:** the "Split roles" tables in the Skin API doc list the Alt/split tokens as candidates to merge.

## M3 — stop

CT-01 is this record. `06_SMOKE_TESTS.md` now carries the plan-review resolution: full client restart, item ids
per row, the reworded SK-02/06/08/12, and SK-15..SK-18. It also adds SK-07's check for the LK-A1 error and SK-05's
font caveat. **The run stops here for the owner's in-game smoke test.** Finalize only on the owner's go-ahead
(RESUME §6).

## M4 — the owner's smoke test, round 1 (2026-10-26)

### Defect: client crash going from WoW Forever to WoW Midnight (LK-A4)

The owner moved LootHistory from Ka0s Default to WoW Forever without trouble. The next pick, WoW Midnight,
crashed the client with `0xC00000FD STACK_OVERFLOW`; the log is `Errors/2026-10-26_11.54.58_Crash_48668.txt`.

- **What the log shows.** The native stack is one engine frame repeated thousands of times. The Lua stack
  runs `OptionsAppearance` → `Skin:SetChoice("midnight")` → `Repaint` → `prim.EditBox`
  (`SkinPaintControls.lua:154`) → `P.font` → `P.unfont` → `SkinPaint.lua:400`
  `EditBox:SetFontObject(Font <UnknownFile:0>)`. The target was the History search box (`lib.SearchBox`).
- **Why that path ran.** WoW Midnight has no body face, so `P.font` put back the font the box had before
  Forever's font reached it.
- **The cause, confirmed by an owner probe.** After `CreateFrame("EditBox"):SetFontObject(GameFontHighlightSmall)`,
  `:GetFontObject()` prints an unnamed table that is not `GameFontHighlightSmall`. So the font object the skin
  had recorded for the box was the anonymous one the client's EditBox answers with, and handing that object
  back recursed without end. The kit's mock answers with the named font it was given, so no headless test
  could see this.
- **Probe side effect.** The probe's EditBox was created without `SetAutoFocus(false)`, so it took the
  keyboard until the client restarted. A probe that creates an EditBox should clear its focus.
- **The fix.** LK-A4 (`1e21c1f`, SkinPaint minor 3, Skin key 4.6.3.1.1.1.1) records a prior font object only
  when it is a named font that is not the target. Any other target gets its face back by
  `SetFont(path, size, flags)`. The test came first and was red on minor 2.
- **Review.** An independent review found no defect and two hardening points, both taken in `f759a5e`: the
  by-path restore puts back the target's own shadow too, and `P.unfont` checks the recorded object again
  before handing it back. A mutation check showed that removing either guard makes the new case fail.
- **Records.** Release record `docs/automated-tests/20261026-134954/` (`585d40e`), and the CHANGELOG
  release-gate line (`7bc3e9b`, docs only).

### Found while gating: a date-dependent LootHistory test (LH-FX1)

`TestData: the sample rollup books a holder move's loss and gain on each holder` failed on LootHistory
`master` and on this branch from 2026-10-26. `BuildTestData` stamps its rows from `time()`, while the test
pinned `now` to 2026-10-06, so the sample drifted out of the window that date selects. LH-FX1 (`701a1fe`)
reads `T.mocks.time()` instead. It is a test change only.

### Re-vendor (LH-RV4)

LH-RV4 (`9edc52a`, retargeted in `a1af6e8`) brought SkinPaint 3 into LootHistory, with SkinPaint 3 pinned
in `tests/test_libka0s.lua` and recorded in `docs/revendor/2026-10-25-v1.78.0/08_RECUT3.md`.

### Local tag moves (never pushed), continued

`65a23cb` (LK-A3) → `585d40e` (LK-A4 release record) → `7bc3e9b` (LK-A4 CHANGELOG release-gate line,
docs only; the payload is byte-identical to `585d40e`).

### Gates at this stop

| Repo | Lint | Tests |
|---|---|---|
| LibKa0s | 0/0 in 223 files | 3007 passed, 0 failed, 2 skipped |
| LootHistory | 0/0 in 148 files | 1782 passed, 0 failed, 1 skipped |

### Stop

**The run stops again for the owner's smoke test.** SK-19 covers the crash path, and SK-01..SK-18 are
still open. Finalize only on the owner's go-ahead (RESUME §6), and the v1.78.0 tag is pushed only then.
