# QuickComms preview selector window: design (QC-01..QC-04)

Read-only survey, 2026-10-23, at QuickComms `4987594` (master, LibKa0s v1.75.2 vendored) and LibKa0s
`99fb662`. Binding scope: `OWNER_SCOPE.md` A (second block), B1 and C. No LibKa0s piece is needed: the
window is built host-side from members the addon already vendors (`W.Dropdown`, `W.CloseMenu`,
`Core.ApplySkin`, the `NS.MakeCloseButton` wrapper), so no LK-2x item is proposed.

## 1. Current state, with evidence

### 1.1 The switch (`modules/Preview.lua`, 286 lines)

- One owner of three flavors: test mode (`State.testMode`), "Preview as…" (`State.previewAs`) and the
  edit preview (`State.editPreview`). Every change announces through the local `announce()`
  (`Preview.lua:30-34`): `TEST_MODE_CHANGED` with `on`, then `refreshPanel()` (the settings page).
- `P.CURRENT = "current"` (`:75`) is **the off value**. `P.Presets()` (`:128-155`) lists
  `current` (no snapshot), `mplus`, `raid:lfr|normal|heroic|mythic`, `arena`, `bg:<short>` per
  battleground set, `world` (label "Solo"). `P.FindPreset` `:157`, `P.Label` `:164` (also answers
  `P.EDIT`), `P.Choices` `:174` (the settings row's `values`, `{value,text}`), `P.PreviewAs` `:180`,
  `P.PreviewSnapshot` `:185` (nil for off).
- `P.SetPreviewAs(key)` (`:195-216`): nil, `""`, `"off"` and `"current"` all mean off; an unknown key
  answers false silently; a start is refused with one line while stood down (`NS.StoodDownRefusal`)
  or in combat (`L["Preview is not available in combat."]`); a start clears `State.testMode`.
- End paths of "Preview as…" today:
  1. `P.SetPreviewAs(nil|"off"|"current")` from the slash, the settings row, or the test.
  2. `P.SetTestMode(true)` sets `State.previewAs = nil` (`:58`) and announces.
  3. Combat: `onRestrictionChanged` (`:259-270`) on `RESTRICTION_CHANGED` with `InCombat()`: one
     `L["Preview ended: you entered combat."]` line.
  4. The settings window closing: `P.WatchPanel` (`:249-257`) hooks the client's `SettingsPanel`
     `OnHide` and ends both Preview as and the edit preview.
  5. The stand-down: `NS.STAND_DOWN` entry (`:280-283`) clears all three **silently, with no
     announce** (the surfaces are torn down by the stand-down itself).
  A profile change does not end it (the state is session-only and profile-independent).
- Consumers of `previewAs`: `modules/Surfaces.lua:405-422` (`ApplyAll`: `preview = PreviewSnapshot()`,
  `MarkPreview(plan, PreviewAs())`, disarmed slots), `settings/Editors.lua:69` (`Ed.Snapshot`),
  `settings/Callouts.lua:101`, `settings/Groups_When.lua:250`, `modules/Diagnostics.lua:111`,
  `modules/Pad.lua:342-350` (header `Preview: <label>`, strip `PREVIEW`), and the dial (opens dial 1
  on `TEST_MODE_CHANGED`, display-only, `qc-display`).

### 1.2 The entry points

- Slash: `settings/Slash.lua:64-65`, row `{"preview", L[...help...], function(rest) NS.SlashVerbs.Preview(rest) end}`.
  `settings/SlashVerbs.lua:106-127` `V.PreviewLines(rest)`: bare prints the menu (`Preview as (now: %s):`
  then `  key: label` per preset); a name is lower-cased, `off` maps to `current`, unknown prints
  `No situation named %s. Type /qc preview for the list.`; success prints `Previewing: %s` or `Preview off.`.
- Settings: General → Master controls, the block's one `extra` row (`settings/Panel.lua:61-65`):
  `state.previewAs`, `sessionOnly`, `default = "current"`, `values = NS.Preview.Choices()`, `validate =
  FindPreset(v) ~= nil`, desc `"… It ends when the settings close or combat starts."`. Its seam is
  `settings/Schema.lua:53-56` (`get` answers `PreviewAs() or "current"`, `set` calls `SetPreviewAs`).
- No launcher entry for Preview as (the launcher carries Test mode only, `core/LauncherSetup.lua:65-66`).

### 1.3 Window building blocks the addon already has

- `NS.ApplySkin` and the one close wrapper `NS.MakeCloseButton(parent, onClick)` (`core/CoreSetup.lua:92-107`;
  degraded stubs at `:48-49`). standalone-windows' wrapper MUST is met by going through it.
- `LibKa0s-Widgets-1.0` is leased in `core/WidgetsSetup.lua` (DragHandle, CopyWindow today). `W.Dropdown(parent,
  width, opts)` (`Widgets.lua:440`; `dd:SetOptions({ {value,label} })`, `dd:SelectValue(v)`, `dd.onSelect`,
  `dd._value`, `dd.text`) and `W.CloseMenu()` (`:464`, a host MUST call it from every non-click close path).
- `settings/ModalWindow.lua` is MODAL (a full-screen catcher) and template-based: wrong shape here.
- The library's step panels (`PerfPanel.lua:168-210`, `SimPanel.lua:202-222, 330-347, 782-830`) are the
  look to copy: `BackdropTemplate` frame, `DIALOG` strata, movable, clamped, drag on the left button,
  a `GameFontNormal` title at TOP -6, the close mark at TOPRIGHT -6, `ApplySkin`, born hidden,
  `UISpecialFrames`, `HookScript("OnHide", CloseMenu)`, a session-only point remembered on drag stop. The
  sim panel's button (`SimPanel.lua:615-640` `makeButton`) is private to the library: the host builds
  its own copy (about 20 lines).
- Mock: `tests/wow_mock.lua` carries `m.UISpecialFrames` (asserted by `test_callout_popup.lua:325` and
  `test_icon_browser.lua:485`) and a `SettingsPanel` whose `OnHide` can be fired.

## 2. The design

### 2.1 "Current" becomes a real preview; `off` becomes the off value (QC-01)

B1 says a bare `/qc preview` "starts a preview of the current situation". Today `current` *is* off, so
the selector could never show for it. Decided:

- `P.OFF = "off"`. `SetPreviewAs(nil | "" | "off")` ends; `SetPreviewAs("current")` **starts** a preview
  of where you are: the live snapshot, every slot marked and disarmed, `Preview: Current` on the header,
  PREVIEW on the strip, the echo on click (the same treatment as any preset).
- `P.PreviewSnapshot()`: for `current` answer `NS.Situation.Current()` (the live table, so the preview
  follows a zone change through the existing `SITUATION_CHANGED` → `Surfaces.Request`); others as today.
- `P.Label(nil | "off")` answers `L["Off"]`.
- `P.Choices()` (the settings row only) = `{ {value="off", text=L["Off"]} }` followed by every preset;
  the row's `default` and `Schema` `get` fallback become `"off"`, `validate` accepts `"off"`.
- **Closing the settings window no longer ends Preview as** (`WatchPanel`'s OnHide keeps ending only the
  edit preview). The window now carries the end control and is the point of the request ("available no
  matter how preview mode was invoked"); a preview that died with the settings window would make the
  window pointless for every settings-started preview. Desc text becomes: `"Draw every pad, and open
  dial 1, as it would look in another situation. Nothing on them sends. A small window lets you switch
  it or end it; combat ends it."`

### 2.2 The window (`modules/PreviewWindow.lua`, new, about 200 lines; QC-02)

`NS.PreviewWindow` = `{ Sync, IsShown, __frame }`. TOC line `modules\PreviewWindow.lua` directly after
`modules\Preview.lua` (everything it needs — Core seam, Widgets lease, Bus, Preview — is loaded by then).

**Lifecycle: one function, `PW.Sync()`, is the only thing that shows or hides it.**

- Shown iff `NS.Preview.PreviewAs() ~= nil and not NS.IsStoodDown()`; otherwise hidden (and the menu
  closed through `W.CloseMenu`).
- Called from `Preview.lua`'s `announce()` (after the message, before `refreshPanel`) and from
  `Preview.lua`'s `NS.STAND_DOWN` entry after it clears the state (the stand-down announces nothing, so a
  bus listener would miss it). The call is late-bound and guarded:
  `if NS.PreviewWindow then NS.PreviewWindow.Sync() end`. A direct call rather than a
  `TEST_MODE_CHANGED` listener: deterministic in tests, no degraded-bus branch, and the stand-down path
  is covered by the same line. This covers every entry and every exit in 1.1: slash, settings row,
  window dropdown, End button, close X, Escape, `/qc test`, combat, stand-down — each goes through
  `SetPreviewAs`/`SetTestMode` (announce) or the stand-down.
- On show it re-reads the options (`P.Presets()` → `{value=key,label=label}`, **no Off entry**; labels
  move with spec and season) and `dd:SelectValue(P.PreviewAs())`, so `/qc preview <name>` and the
  settings row move the dropdown.

**Controls, one row under a title bar:**

```
+---------------------------------------------------------------+
|          Ka0s Quick Comms - Preview                       [x] |   TITLE_H 24
|  [ Raid · Heroic · The Voidspire        v ]  [ End preview ]  |   ROW_H 22
+---------------------------------------------------------------+
   PAD 8 | DROP_W 240 | GAP 6 | BUTTON_W 100 | PAD 8   -> 362 x 62
```

- Title `L["%s - Preview"]:format(NS.BRAND)` (`frame.title`, tinted by `ApplySkin`).
- Dropdown: `W.Dropdown(frame, 240)`, label word-wrap off (SimPanel minor 4's fix). `dd.onSelect = function(v)
  NS.Preview.SetPreviewAs(v) end` — the same setter as the slash and the row; no chat line (the pads and the
  dropdown are the answer). Tooltip: `L["Preview as"]` then `/qc preview <name>`.
- End preview: a host button (BackdropTemplate + `NS.ApplySkin`, a centered `GameFontNormalSmall`
  label, gold under the pointer), label `L["End preview"]`, click → `NS.Preview.SetPreviewAs(NS.Preview.OFF)`;
  tooltip names `/qc preview off`.
- Close mark: `NS.MakeCloseButton(frame, endPreview)` at TOPRIGHT -6; the close ends the preview (OWNER C).
- Escape: the frame's name `QuickCommsPreviewWindow` goes in `UISpecialFrames` (standalone-windows MUST;
  the library panels do the same). Escape hides the frame directly, so `OnHide` ends the preview — but
  only when the frame's own shown flag is off (`not frame:IsShown()`): hiding UIParent (Alt+Z, a
  cinematic) fires the child's OnHide with the flag still on and must not end anything. `OnHide` also
  calls `W.CloseMenu()` (the Widgets contract). A state-driven `Sync` hide finds `PreviewAs()` already nil,
  so there is no recursion.
- Placement: `DIALOG` strata (above the settings window, as the popup and step panels sit), movable,
  clamped, drag by the left button anywhere on the frame. Default point `TOP, UIParent, TOP, 0, -140`
  (clear of the screen centre where a dial opens). **Session-only**: on drag stop the point is kept in a
  file-local and reused on the next show; nothing is written to SavedVariables (the step-panel precedent
  preview-mode-§ sanctions for preview controls; this is a preview-mode control strip, not the addon's main
  window). Fixed size, no resize grip.
- Combat: the frame is a plain insecure `Frame` with no secure child, so Show/Hide in combat is legal; in
  practice it is never shown in combat (a start is refused and combat ends the preview, which hides it).
  It calls no protected API: `SetPreviewAs` → `Surfaces.Request` is the same out-of-combat path the
  slash and the row take. `tests/test_sendengine.lua`'s grep for secure templates stays green.
- Degraded (LibKa0s absent): `Sync` is a no-op when `W.Dropdown` or `CreateFrame` is missing; the slash
  still previews and prints.
- Diagnostics: `modules/Diagnostics.lua:111` gains `previewWindow=shown|hidden` beside `previewAs=`.

### 2.3 The slash (QC-03)

| Typed | Does | Prints |
|---|---|---|
| `/qc preview` | if nothing is previewed, `SetPreviewAs("current")`; either way the window is up (Sync) | `Previewing: <label>` (refusal line instead on a refused start) |
| `/qc preview <name>` | switches; the dropdown follows | `Previewing: <label>` (unchanged) |
| `/qc preview off` | ends; the window goes | `Preview off.` (unchanged) |
| `/qc preview list` | nothing changes | the old bare output: `Preview as (now: <label or Off>):` then each `  key: label` |
| `/qc preview nope` | nothing | `No situation named nope. Type /qc preview list for the list.` |

`list` cannot collide with a preset key (keys: `current`, `mplus`, `raid:*`, `arena`, `bg:*`, `world`).
Help row text: `Preview the pads and dials as another situation in a small window — `/qc preview` here,
`/qc preview <name>`, `off`, or `list`` (keeps the prefix `test_slash.lua:196`'s neighbour asserts).

### 2.4 Doc ripple (QC-04)

README Usage paragraph and the 0.1.0 Version History bullet; `docs/ARCHITECTURE.md` (Module Map row, the
session-state paragraph, the `TEST_MODE_CHANGED` row's consumers note, Slash Commands, Known Limitations:
Escape now ends the preview before it closes the settings window; the Documentation map is unchanged);
`docs/module-map.md` (new row after 16l, test row); `docs/slash-dispatch.md` (the `preview` row);
`docs/settings-panel.md` (the Preview as row: Off, the window, no end on close); `docs/scope.md` line 32
sentence; `docs/test-cases.md` (new `test_preview_window.lua` section, changed titles, the counts table);
`docs/smoke-tests.md` (new theme `PREVIEW-1..9` in the index and a `## Preview window` section; EDIT-3,
EDIT-27 and DIAL-9 text amended where they say closing the settings ends Preview as, their `Result:`
reset to pending — the owner re-runs them).

## 3. Decisions and why

1. **No library work.** The window is one host's preview control, not a pattern three addons share;
   `W.Dropdown`, `CloseMenu`, `ApplySkin` and the close wrapper already exist. LibKa0s's bar for a public
   member is not met.
2. **`current` is a live preview; `off` is off.** Required by B1; the alternative (a new key such as
   `here`) would leave two entries that read "Current" and a settings row whose default looks like an
   active preview.
3. **Settings close no longer ends Preview as** (edit preview unchanged). Without this, the window would
   vanish with the settings for every settings-started preview, contradicting "available no matter how
   preview mode was invoked".
4. **The window's dropdown has no Off entry**: the End preview button is the off control (owner A).
5. **Escape ends the preview** (UISpecialFrames), the close X ends it, and the parent-hide guard keeps
   Alt+Z harmless. The invariant "shown exactly while previewing" holds on every path.
6. **Session-only position**, no SavedVariables: matches the Perf/Sim panels the owner compared it to.
7. **Direct Sync call from Preview**, not a bus listener, so the silent stand-down is covered.
8. **No chat line from the window's own controls**; the slash keeps its lines.
9. Test mode (placeholders) gets no window (B1).

## 4. Risks

- **Two Escapes with the settings open.** With the window in UISpecialFrames, the first Escape ends the
  preview (the window is the special frame), the second closes the settings (as the callout popup
  behaves, `test_callout_popup.lua:328`). Smoke PREVIEW-4 checks it; acceptable and arguably right.
- **A preview now outlives the settings window**, so dial 1 can sit open in display mode with no settings
  behind it. Its hub still closes it, and End preview / Escape end the preview. Smoke DIAL-9 amended.
- **standalone-windows reading.** An auditor could read the SV-persist MUST onto this window. It is a
  preview-mode control panel (the sim step panel's sanctioned session-only shape), not the addon's main
  window; QC-04 writes one sentence saying so in ARCHITECTURE's Known Limitations rather than a
  deviation row. If the owner disagrees, persisting the point in `db.global` is a small follow-up.
- **The mock's W.Dropdown path** has not been exercised by QuickComms' own suite before (only the library's).
  The test-first step in QC-02 surfaces any mock gap early; a gap is fixed in `tests/wow_mock.lua`,
  never in `tests/_kit/`.
- **Line caps.** New file ~200; `Preview.lua` 286 → ~300; `SlashVerbs.lua` 155 → ~170;
  `locales/enUS.lua` 1351 → ~1362 (already in the 1000-1500 band; still under the cap);
  `tests/test_preview.lua` 392 → ~400; the new suite ~300. No split needed.
