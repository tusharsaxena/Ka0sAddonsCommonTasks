# 02 — Execution record

**What was actually done, 2026-08-24.** The scan that decided it is
[`01_STEP0_SCAN.md`](01_STEP0_SCAN.md); the prompt both were run against is [`PROMPT.md`](PROMPT.md).

Unlike the 2026-08-05 bundle, **this one has been executed**. Everything below is merged and pushed.

---

## What shipped

| Repo | On | Change | Suite |
|---|---|---|---|
| LibKa0s | `20f6112`, tag `v1.12.0` | Widgets minor 4 — `opt.isActive`, `dd.presets`, and the collapsed-label fix | 568 / 568 |
| LootHistory | `6b10b3b` | **Adopted.** ~200 lines of hand-rolled widget deleted; ten instances converted | 621 / 621 |
| BankLedger | `7900fbb` | Two live bugs fixed, mock fidelity, four doc gaps | 775 / 775 |
| MultiMeters | `7f18c31` | Real-row-build coverage, one art factory, two stale citations, one smoke check | 1216 / 1216 |

`luacheck` 0 warnings / 0 errors in every repo. Every vendored copy is byte-identical to the
`v1.12.0` tag — both the content diff and the plain byte diff. No addon was tagged and no addon's
version was bumped: a re-vendor is not a release.

---

## The library came first, because the adoption depended on it

LootHistory's Character filter used two seams version 3 did not have, and adopting without them meant
either losing the behavior or keeping the copy. Both went upstream.

**`opt.isActive(dd)`** — a per-option predicate, asked *instead of* the selection set. A preset row is
one whose `value` is not among the values it selects; membership of `_selected` can never report it,
so through minor 3 it was the one row in a menu that could never light up.

**`dd.presets`** — `{ [value] = function(dd) end }`, whose handler runs in place of the toggle.

**A third thing was refused.** `opt.icon` did not go upstream: the library already measures inline
`|T…|t` markup in a label, so the class icon folds into the label string host-side. A field nobody
needs in a frozen `-1.0` major is permanent.

**And one behavior changed.** Reading the two implementations side by side surfaced a defect in the
library's own `UpdateMultiLabel`: it walked `_options` asking which were selected, so a selected value
with no row in the *current* list was invisible to it — and these lists are data-driven, so the button
read "Character: All" while the filter was on. It now labels every value in `_selected`. That is
visible to an existing host, and version 3's *Moving to version 4* section says so where an adopter
still on that copy will read it.

Thirteen new library cases, nine red before the change. The collapsed label had no case at all before
this release.

---

## LootHistory — the adoption

The point of it was the deletion, and the deletion happened: `modules/Browser.lua` no longer contains
a `MakeDropdown` factory, a singleton popup, `acquireRow`, `styleOption`, `optionClicked`,
`activePresetLabel`, `selectionLabels` or `summarizeSelection`. The seam is one file,
`core/WidgetsSetup.lua`, with one factory and two questions — `NS.MakeDropdown` and `NS.HasWidgets`.

All ten instances converted, including the Character filter, which now uses the library's own
`isActive` and `presets`. `glyphFont` is deliberately **not** passed: no option in this addon carries
a `glyph`, and the class icons are inline texture markup rather than monospace characters.

**The live bug it fixed:** the export modal was in `UISpecialFrames` with no `OnHide` handler, so
Escape with the Data set menu open orphaned the shared popup over the game.

**Not converted:** `modules/BrowserTable.lua`'s right-click row menu. A context menu *and* it needs
per-row disable. It stays hand-rolled and coexists, and `docs/ARCHITECTURE.md` now says so.

---

## The two spot checks, which were not clean

Both addons were already adopted and both had real work outstanding.

**BankLedger** had a half-wired second consumer. `modules/Export.lua` called the documented-nil-able
`MakeDropdown` unguarded and then called methods on the result, and the modal called `W.CloseMenu()`
from no close path at all — the same orphaned-menu bug LootHistory had. The nil guard was filed by
the 2026-08-03 review as C-012/F-013 T4.5 and had never been applied. Its mock also still answered
`CreateFontString` with the frame itself, conflating a row's label with its glyph — the exact
conflation that let the v1.11.0 crash ship.

**MultiMeters** had the coverage hole rather than the bug. Its one case that clicked a dropdown
emptied the option list first, so `Populate` iterated zero options and `makeMenuRow` was never
reached — precisely the shape that let 553 green library cases sail over a first-click crash. The
comment justifying the workaround had been stale since minor 3.

---

## What the adversarial pass caught

Each repo's work was verified by a separate read-only agent that re-ran the suites itself and checked
every claim against the tree. It was worth running.

- **A false red-before-green claim in each of the three repos.** MultiMeters' new case was green
  against unmodified code and had been made "red" by re-inserting the workaround *inside the test*.
  LootHistory's implementer reported "all 17 red" where the truth was 14 of 16. Both records were
  corrected rather than quietly restated — one commit message was replayed to say
  "NOT RED FIRST, AND IT SHOULD NOT HAVE BEEN CALLED THAT".
- **A test that pinned nothing.** LootHistory's "the filter bar builds all nine dropdowns through the
  seam" asserted a shape equally true of the widget the branch had just deleted. It now wraps
  `lib.Dropdown` and asserts identity.
- **A smoke-test step that could not be performed.** BankLedger's new slash-command check told the
  tester to toggle the window shut with `/bl show`, which is not a toggle in that addon.
- **A degraded-path leak.** LootHistory's export modal built and discarded a frame per refusal — ten
  `Open` calls stranded ten frames. `NS.HasWidgets()` now answers before `CreateFrame`.
- **A fragile assertion** in MultiMeters that indexed rows by a frame count, false from the second
  click of any session onward.

Not every finding was accepted. LootHistory's verifier flagged a strata case as "already green"; it
was kept, because a regression guard on a precondition the adoption depends on is not required to be
red first, and manufacturing redness by breaking the strata would be theatre.

---

## Filed, not fixed

- **Six decline records**, one per non-adopting addon, `state:will-not-do` + `severity:low`, closed as
  not planned to match how the collection treats a terminal label — AbsorbTracker #26,
  ConsumableMaster #28, KickCD #12, PanelMaster #43, PrettyChat #11, WhatGroup #12. Each carries the
  evidence and the condition that would reopen it, so the next re-vendor does not re-litigate it.
- **LibKa0s #10** — the flat skin on a schema-driven page belongs to `OptionsWidgets`' own
  `makeDropdown`, behind the Options major, rather than to each consumer. An observation and a
  proposal, not a defect.
- **LibKa0s #11** — the menu's click-catcher is a `Button` with no `RegisterForClicks`, so it takes
  `LeftButtonUp` only and **swallows** a right-click while a menu is open. Found because LootHistory
  is the first host with a right-click surface on the same window. Recorded in that addon's
  smoke tests as expected in-client behavior rather than worked around locally.

One thing was fixed rather than filed: `LibKa0s/media/icons/LICENSE-open-iconic.txt` sat LF in the
LibKa0s working tree while `.gitattributes` declares CRLF and the tag ships CRLF, which made the byte
reading of every consumer's vendor check report a false difference. Re-checked-out; index untouched.
Both diffs are now empty in all three consumers.
