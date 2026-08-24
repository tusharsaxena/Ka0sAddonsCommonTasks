# 01 — Step 0: the collection-wide scan

**What every Ka0s addon was found to have, and what was decided for each.**

Produced 2026-08-24, by running [`PROMPT.md`](PROMPT.md)'s Step 0 against all nine addons on the
roster at [`../../../WowAddonStandards/standards/ADDONS.md`](../../../WowAddonStandards/standards/ADDONS.md)
— one read-only scanner per repo, each reading
[`../../../LibKa0s/docs/api/Widgets/version-3-docs.md`](../../../LibKa0s/docs/api/Widgets/version-3-docs.md)
as its contract. Library release at scan time: **v1.11.2, Widgets minor 3**.

The scan changed nothing. What was done about it is [`02_EXECUTION_RECORD.md`](02_EXECUTION_RECORD.md).

---

## The verdict, in one table

| Addon | Vendored | Verdict | Why |
|---|---|---|---|
| AbsorbTracker | v1.10.2 | **Do not adopt** | No hand-rolled menu. Every selector is an AceGUI widget in LibKa0s-Options' layout tree, or an LSM media picker. |
| BankLedger | v1.11.2 | **Already adopted** — 8 gaps | The addon the major was lifted from. A half-wired second consumer in the export modal. |
| ConsumableMaster | v1.10.2 | **Do not adopt** | Same AceGUI reason. Its one hand-rolled popup is a secure hover flyout of SecureActionButtons. |
| KickCD | v1.10.2 | **Do not adopt** | Same AceGUI reason, and the one candidate outside a layout is ~39 rows with no scrolling in the major. |
| LootHistory | v1.10.2 | **ADOPT** | Carries a full hand-rolled clone of the widget — factory, singleton popup, pooled rows — with ten live instances. |
| MultiMeters | v1.11.2 | **Already adopted** — 4 gaps | Adopted in the right place; the test that clicks a dropdown empties the list first. |
| PanelMaster | v1.10.2 | **Do not adopt** | Fourteen AceGUI instances; four families hit a documented deliberate absence outright. |
| PrettyChat | v1.10.2 | **Do not adopt** | No selector of any kind. The schema is bool and string rows only. |
| WhatGroup | v1.10.2 | **Do not adopt** | No selector of any kind. Nine bool rows and one number row. |

`BuffTextNotifications` and `WhoGotLoots` sit beside these as sibling directories but are not Ka0s
addons — no Ka0s branding, no `libs/LibKa0s`, not on the roster — and were not scanned.

---

## The one adoption

**LootHistory** is the only addon in the collection with a control that genuinely wants this widget,
and what it has is not a control but a copy of the widget itself:

| Where | What |
|---|---|
| `modules/Browser.lua:351` | A local `MakeDropdown` factory — the same seven instance methods, the same two callback fields, the same `"all"` sentinel, the same `"<Prefix>: N selected"` rule. |
| `modules/Browser.lua:277` | Its own `FULLSCREEN_DIALOG` singleton popup with pooled rows and a click-catcher. ~140 lines. |
| `modules/Browser.lua:440` | `B:MakeDropdown`, so `modules/Export.lua` shares the machinery. |
| `modules/Browser.lua:937, :998–:1060` | Nine instances: Group-by plus eight column filters. |
| `modules/Export.lua:450` | The tenth: the export modal's Data set picker. |

Adoption also fixes a live defect. The export modal is in `UISpecialFrames` (`modules/Export.lua:473`)
and its close button just calls `frame:Hide()` (`:445`); neither path hides the shared menu, and the
frame has no `OnHide` handler at all. Closing that modal by Escape while the Data set menu is open
orphans the menu today.

**Not converted:** `modules/BrowserTable.lua:1057`, the right-click row menu. A context menu, *and* it
needs per-row disable. Two independent disqualifiers; it stays hand-rolled and coexists.

### The blocker, and what was done about it

The Character filter (`modules/Browser.lua:1060`) used two things Widgets version 3 did not have:

- `opt.isActive(dd)` — a per-option predicate, so the synthetic "Character: Current" row can light up
  when the selection is exactly the current player. Its own value, `"current"`, is nobody's key, so
  membership of `_selected` can never report it.
- `dd.presets` — a per-value handler, so clicking that row *replaces* the selection rather than
  toggling the literal string into it.

A third extension, `opt.icon`, was **not** taken upstream: the library already measures inline
`|T…|t` markup in a label, so the class icon folds into the label string host-side.

Per the prompt's closing clause, the two real gaps went upstream rather than being worked around.
They shipped as **LibKa0s v1.12.0, Widgets minor 4** —
[`version-4-docs.md`](../../../LibKa0s/docs/api/Widgets/version-4-docs.md) — along with a behavior
fix the same reading surfaced: `UpdateMultiLabel` walked `_options` and asked which were selected, so
a selected value with no row in the *current* list was invisible to it and the button read "All"
while the filter was on.

All three releases of this major have now come from an adopter hitting a gap in the same step of the
same prompt.

---

## Why six addons decline for one reason

Five of the six do not decline on taste. They decline on mechanism, and it is the same mechanism each
time: **every selector they have is a genuine AceGUI widget living inside LibKa0s-Options' own AceGUI
container tree** — built with `SetLabel` and `SetRelativeWidth`, parented by `AddChild`, wired by
`SetCallback`, and released and rebuilt through AceGUI's widget pool. `Widgets.Dropdown` returns a
bare 20px frame with none of that protocol. Adopting anywhere would mean hand-writing an AceGUI
wrapper around the library frame in each consumer — the exact local fork the collection forbids — and
would still leave the converted row looking unlike the ones beside it.

The remaining reasons, where a control failed on content rather than mechanism, are all documented
deliberate absences of the major: an unbounded LibSharedMedia list needing scrolling and a per-row
texture preview (AbsorbTracker, ConsumableMaster, KickCD, PanelMaster), ~39 class/spec rows (KickCD),
~270 artwork rows and a `SetDisabled` (PanelMaster), and ~40 spec rows (ConsumableMaster).

PrettyChat and WhatGroup decline for the simplest reason available: they have no selector at all.

This is recorded upstream as a LibKa0s issue. The honest home for the flat skin on a schema-driven
page is `LibKa0s/OptionsWidgets.lua`'s own `makeDropdown`, behind the Options major, so every
schema-driven page in the collection gets it at once and no consumer forks the maker.

---

## Two things the scan got wrong, corrected here

- **The LootHistory scanner reported that LibKa0s tags above v1.9.2 were not pushed to origin**, which
  would have put every addon's provenance line at risk of the vendor-sync rule. It is not true:
  `git ls-remote --tags origin` lists v1.10.0 through v1.11.2, and now v1.12.0. Nothing was at risk.
- **Every vendored copy was byte-clean against the tag its own provenance line named.** Six addons
  sitting at v1.10.2 are behind the newest release, not stale relative to their own pin, and for a
  non-adopter the whole delta is a 344-line file the addon would never load. None of the six was
  re-vendored for this exercise.
