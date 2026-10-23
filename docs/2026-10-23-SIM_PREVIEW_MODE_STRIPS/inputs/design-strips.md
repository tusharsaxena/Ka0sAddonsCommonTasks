# Mode strips and header words: design (OWNER_SCOPE A blocks 3-4, C)

Read-only survey, 2026-10-23, at these heads (all on their default branch, clean): LibKa0s `99fb662`
(v1.75.2, Widgets minor 13), WowAddonStandards `db00f05` (v2.86.0), BankLedger `8b93492`, DropWatcher
`e017d26`, LootHistory `ceb76a0`, MultiMeters `a14acce`. Item ids: LK-10, WS-05, BL-10, DW-10, LH-10,
MM-01. The MultiMeters and KickCD simulators (their sim strips) belong to the simulator designs; this note
gives them the library flavor they build on and the header-word rule they follow.

---

## 1. Current state, with evidence

### 1.1 The library strip

`LibKa0s/LibKa0s/Widgets.lua:775-834`: `lib.TestStrip(parent, opts)` and `lib.TEST_STRIP = { HEIGHT = 18 }`,
Widgets `MINOR = 13` (`:62`), key `13.1.4.3.2`. The fill is a file-local amber
`STRIP_FILL = { 1.00, 0.65, 0.15, 0.12 }` (`:777`). There is no color option (the header's "WHAT IT
DELIBERATELY IS NOT" block, `:45-53`, gives the re-check trigger "a consumer needs a different color").
The strip is born hidden and unanchored, with the mouse off. It never changes after construction, and the
fill and icon are stored as `__fill` / `__icon`, which are not part of the contract. Its suite is
`tests/test_widgets_teststrip.lua` (12 cases, registered in `tests/run.lua:83`). Its API doc is
`docs/api/Widgets/version-13.1.4.3.2-docs.md` with `members-13.1.4.3.2.json`, and its consumer rows are
`docs/api/CONSUMERS.md:91-93, :506-507`.

### 1.2 How each window marks a mode today

| Addon | Test mode | Simulation | Strip hidden by a layout? |
|---|---|---|---|
| **BankLedger** | The amber `frame.testStrip` under the filter bar (`modules/Browser.lua:1069-1085`), **plus** a red `TEST MODE` badge on the title (`:1026-1031`, `frame.testBadge`). `B:UpdateTestStrip` (`:788-799`) shows the badge only for `DatasetKind()=="test"` | The **same** amber Browser strip, with its text swapped to `NS.SimHost.MarkerText()` (`:796`). No header word. The session window has its own strip, `f.testStrip` (`modules/SessionWindow.lua:475-525`), built with `W.TestStrip` and shown only for `"sim"` | No minimize, no compact |
| **DropWatcher** | The amber `f.banner` (`modules/Window.lua:434-444`, via `NS.MakeTestStrip`, `core/WidgetsSetup.lua:64`), **plus** red `f.testText` `TEST MODE` / compact `TEST` beside the title (`modules/WindowTitleBar.lua:314`, `modules/CompactChrome.lua:54,343`), with tooltip `TB.TestTip` | **No strip.** A cyan `f.simText` `SIMULATION` / compact `SIM` (`WindowTitleBar.lua:315`), with tooltip `TB.SimTip` (scenario), plus the footer's `Simulating: …` | **Minimized**: `paintMinimized` hides `frame.body`, which parents the banner (`Window.lua:600-605`). Compact keeps the strip and wraps it (`CompactChrome.lua:365-372, 473-482`) |
| **LootHistory** | The amber `frame.testStrip` under the filter bar (`modules/Browser.lua:965-987`) **plus** a red badge `frame.testBadge` (`:929-934`) | The **same** amber strip with the text `SIM_MARK.strip`, **plus** the badge rewritten to a cyan `SIMULATION` (`:602-625`) | No minimize, no compact |
| **MultiMeters** | The amber `self.testStrip` under the title (`modules/Window.lua:666-671`, placed by `Window_Header.lua:767-781`), **plus** a red `|cffff2020TEST MODE|r` appended to the title (`Window_Header.lua:339-342`). The session line says `Test` (`:1121, :1250`) | None yet (the MM simulator is new in this run) | **Minimized**: `stripShown` (`Window_Header.lua:756-759`) hides it. **Header hidden**: the strip stays (that was the point of #59), and the title word goes with the header |

Tooltips: DropWatcher's `TestTip` already sits on both the word and the banner (`Window.lua:442`), and
its `SimTip` sits only on the word. BankLedger's and LootHistory's badges are plain FontStrings with no
tooltip, while their strips have one (BL `B.StripTipLines`, LH an inline hook that switches on
`simulating()`). MultiMeters' strip has the mouse off and no tooltip, and its title word has none either.

Untouched by owner direction: QuickComms, AuraMaster, WhatGroup and KickCD keep their header words. KickCD
has no test mode. Its simulation gets a sim strip on the icon grid, which is the KickCD simulator design's
job, built on LK-10.

### 1.3 The standard

- `standards/standards/preview-mode.md:11-22`: the marker MUST (v2.86.0). Its form is the addon's: a title
  badge, inline title text, or a strip. `:49`: a simulator MUST mark the session "as a test mode is marked".
- `standards/standards/standalone-windows.md:41-46`: a filter-bar window SHOULD use `TestStrip`. The bullet
  does not mention simulation and does not mention the header word.
- `standards/standards/library-stack.md:94`: the Widgets row in the module table (TestStrip since minor 13).
- `standards/standards/anti-patterns.md:126`: #97.
- `AUDIT.md:938-946`: the test-mode marker check.
- `standards/NEW_ADDON_CONTEXT.md:1626`: item 18.

---

## 2. The design

### 2.1 Library: `opts.kind`, not a new function (LK-10)

```lua
-- Widgets.lua, the strip section
local STRIP_FILL = {
  test = { 1.00, 0.65, 0.15, 0.12 },   -- DropWatcher's C.TONE.warn at 12% (unchanged)
  sim  = { 0.35, 0.80, 1.00, 0.12 },   -- the collection's simulation cyan (DW TB.SIM_TONE, LH SIM_MARK) at 12%
}
...
function lib.TestStrip(parent, opts)
  opts = type(opts) == "table" and opts or {}
  local kind = opts.kind == "sim" and "sim" or "test"
  ...
  fill:SetColorTexture(unpack(STRIP_FILL[kind]))
  s.kind = kind
  ...
end
```

- **One new option, `opts.kind`**, which is `"test"` (the default) or `"sim"`. Any other value, including
  nil, a non-string or an unknown string, gives `"test"`, so every existing call is byte-for-byte
  unchanged.
- **One new read-only field, `strip.kind`** (`"test"` or `"sim"`). Host suites can then ask which flavor a
  strip is without reading `__fill`, which is not contract. Like the rest of the strip, it is set once at
  birth.
- **No new library member.** `TestStrip` and `TEST_STRIP` are still the whole surface, so
  `members-14.1.4.3.2.json` lists the same two names. Height, inset, icon, font and the birth-only contract
  are the same for both kinds.
- **Widgets MINOR 13 → 14** (key `14.1.4.3.2`). If another v1.76.0 item also changes `Widgets.lua`, it
  shares minor 14, as SearchBox and TestStrip shared 13. The attach files re-pair through their shell-minor
  probes and keep their own minors.

**Rejected:** `lib.ModeStrip` with `TestStrip` kept as an alias. It adds a member and a second name for one
function, purely for naming, and the four existing hosts would keep calling `TestStrip` anyway. The header
comment and the API doc call the widget "the mode strip (test or simulation)". Re-check trigger: a third
kind is asked for.

**Rejected:** a host-supplied color (`opts.color`). The sameness is still the point. Two fixed flavors are
two skins, not N.

**Rejected:** a method or helper to recolor a live strip (`SetKind`). The strip has no methods by design. A
window that marks both modes builds one strip of each kind at the same anchor and shows the one in force.
That costs a few lines in BankLedger, LootHistory and DropWatcher, keeps the birth-only contract, and lets
the two strips carry different text and tooltips without swapping text.

**Text color:** both kinds use `GameFontNormalSmall` (gold). Only the band's tint tells them apart, and the
words say which mode it is ("TEST MODE: …", "SIMULATION: …").

### 2.2 The header-word rule (all four addons, and the standard)

> **The mode word in a window header shows exactly when its mode is on and that mode's strip is not on
> screen.**

In practice this means:
- **Expanded, strip built:** the header word is not drawn. The strip is the marker. This is the owner's
  "remove TEST MODE / SIMULATION from the header wherever the strip exists".
- **Minimized** (DropWatcher, MultiMeters): the strip goes with the body, so the header word comes back.
  The title bar is all that is left on screen, and it should still say the window is not live. In
  DropWatcher the `n new` chip anchors after the word, as today.
- **Degraded** (no Widgets library, so the strip is nil): the header word stays as the only marker. Every
  existing degraded test case keeps its meaning.
- **Compact** (DropWatcher): the strip is shown and wrapped, so there is no word. `placeTitle` already
  centers the title alone when no word is shown (`CompactChrome.lua:417-425`).
- **Header hidden** (MultiMeters): nothing changes. The strip is the marker, as since #59.

So no locale key goes dead. `TEST MODE`, `SIMULATION`, `TEST` and `SIM` are still drawn in the minimized
and degraded states. The locale-parity and luacheck gates are therefore unaffected by the removal, and
each item adds only the new strip lines it needs.

**Tooltips:** DropWatcher's `SimTip` goes onto the new sim strip, and the word keeps it for the minimized
state. `TestTip` is already on both. The BankLedger and LootHistory badges had no tooltip, and their strips
already carry one per mode. MultiMeters' strip stays mouse-off, as decided in #59; its title word never had
a tooltip.

**MultiMeters' session line `Test`** (`Window_Header.lua:1121, :1250`) is the session label, not a mode
word. A test grid has no Current or Overall session, so the label names what is drawn. It stays.
**BankLedger's step-panel title** `"<brand> - Simulation"` (`modules/Sim.lua:327`) names the Sim panel, not
a data window with a strip. It stays.

### 2.3 Per addon

**BankLedger (BL-10).**
- In `Browser.lua`, factor the strip build (`:1069-1085`) into `local function buildModeStrip(filterHost, kind, text)`,
  which creates the strip with `W.TestStrip(frame, { kind = kind, text = text, icon = NS.Icon("info") })`,
  anchors it 2 px under `filterHost`, and hooks the existing `B.StripTipLines` tooltip.
- `frame.testStrip = buildModeStrip(…, "test", TEST_LINE)` and `frame.simStrip = buildModeStrip(…, "sim", "")`.
- `B:UpdateTestStrip` (`:788-799`) does four things:
  - shows `testStrip` when `kind=="test"`;
  - shows `simStrip` when `kind=="sim"`, setting its text from `MarkerText()`;
  - shows `testBadge` only when `kind=="test" and not frame.testStrip`;
  - re-anchors the panes.
- `stripReserve` (`:764-767`) counts either strip while it is shown.
- `SessionWindow.lua:buildStrip` (`:482-500`) passes `kind = "sim"` and renames `f.testStrip` to
  `f.simStrip` (comment `:475-478` updated).
- `Browser.lua` grows to about 1250 lines, under the cap.

**DropWatcher (DW-10).**
- `NS.MakeTestStrip(parent, text, kind)` passes `kind` to the library.
- `Window.lua:buildBanner` also builds `f.simBanner` (`kind = "sim"`, the full sim line, `TB.SimTip`) at
  the same anchor as `f.banner`.
- `Window.Refresh` shows `f.banner` for test mode and `f.simBanner` for an active simulation. The two modes
  are exclusive, the same predicate `PaintModeText` uses.
- `layoutPanes` reserves `CC.BannerH()` while either is in force.
- `CompactChrome`:
  - `layoutStrip` sets the full or compact text and wrap on both strips;
  - `CC.Paint` sizes the strip in force;
  - `CC.BannerH()` measures the strip in force through a new `CC.ModeStrip(f)` (`f.banner` while testing,
    `f.simBanner` while simulating, else `f.banner`).
- `TB.PaintModeText` hides the word unless the window is minimized or that mode's strip is nil.
- Two new locale keys: the full and compact sim lines.

**LootHistory (LH-10).**
- `NS.MakeTestStrip(parent, text, kind)`.
- `Browser.lua` builds `frame.testStrip` (`kind "test"`) and `frame.simStrip` (`kind "sim"`, text
  `L[SIM_MARK.strip]`) through one local `buildModeStrip(kind)`, which holds the per-kind tooltip, under
  `filterHost`.
- `B:UpdateTestStrip` shows the strip of the mode in force. It shows the badge, with the mode's text and
  color as today, only when that strip is nil.
- `anchorPane` reserves while either strip is shown.
- `Browser.lua` grows to about 1310 lines, under the cap.

**MultiMeters (MM-01).**
- Hoist `stripShown` (`Window_Header.lua:756`) above `ApplyTitle` (`:309`).
- `ApplyTitle` appends the red word only when `NS.State.testMode and not stripShown(self)`, which covers
  the degraded and minimized cases.
- `ApplyMinimized` calls `self:ApplyTitle()` after `PlaceTestStrip`, so the word follows a collapse even on
  a path that skips `ApplyConfig`.
- The MM simulator's own sim strip follows the same rule. It is designed by the MM-sim agent with
  `kind = "sim"`, and there is no MM header word to remove for it.

### 2.4 Standard (WS-05, v2.87.0)

- **preview-mode.**
  - The marker bullet gains: "Where a display shows the strip, the same mode's word is **not** also drawn in
    its header (SHOULD NOT); a header word remains the marker in a state that hides the strip (minimized,
    or no Widgets library)."
  - The simulator marker bullet (`:49`) gains: "A window that marks test mode with the strip marks a
    running simulation with the strip's simulation flavor (`kind = "sim"`, Widgets minor 14,
    `LibKa0s v1.76.0`) (SHOULD)."
- **standalone-windows `:41`.** Name the two flavors (amber for test mode, cyan for simulation; a host passes
  `kind`, and the colors are the library's), the one-strip-per-kind pattern, and the header-word rule.
- **library-stack-§7 Widgets row.** "From Widgets minor 14 (`LibKa0s v1.76.0`), `TestStrip` takes
  `opts.kind = "sim"` for the simulation flavor and publishes `strip.kind`; no new member."
- **Anti-pattern #97.** Add: "a mode word in a window's header beside a shown strip of the same mode (the
  marker said twice; from v2.87.0)".
- **AUDIT.md test-mode check.** Add the duplicate-word case and the sim flavor.
- **NEW_ADDON_CONTEXT item 18.** Add one clause.
- **Index blurbs** for preview-mode and standalone-windows.
- **The v2.87.0 changelog ruling paragraph** goes under WS-00's entry.

---

## 3. Decisions taken (and why)

1. **`opts.kind` on `TestStrip`, with no alias and no new member.** This is the least surface that makes the
   strip generic, and the owner asked for it to be generic. Every existing call stays green unedited.
2. **Sim tint is cyan `{0.35, 0.80, 1.00}` at 0.12.** It is the collection's existing simulation color
   (DropWatcher `TB.SIM_TONE`, LootHistory `SIM_MARK.color`), so players who know the cyan word get the same
   color as a band.
3. **Two strips, not a recolorable one.** This keeps the birth-only contract and lets each strip keep its
   own tooltip and text.
4. **The header word is dropped only while the strip is on screen.** The minimized and degraded states keep
   the word, so no layout that still shows the window shows an unmarked live-looking title bar. It also
   means no locale key dies.
5. **The MM session-line `Test` and the BL step-panel `- Simulation` title stay.** Neither is a mode word in
   a header that sits over a strip.
6. **BL `SessionWindow` field rename, `testStrip` → `simStrip`.** The window only ever shows the sim strip,
   and a field named for the other mode misleads the next reader. Method names (`UpdateTestStrip`) stay,
   because `Sim.lua:358-359` and the LH SimPanel listener call them and they mean "update the mode strip".
7. **A duplicated header word is anti-pattern #97, under a SHOULD NOT.** An audit finding then catches a
   window that re-grows the word, rather than leaving it to memory.

## 4. Risks

- **DropWatcher compact measure.** `CC.BannerH` reads the text width of the strip in force. If the sim strip
  is measured while hidden, `GetWidth` answers 0 and the existing `room` fallback (`:479`) covers it. The
  DW-10 tests pin the sim line at 380 px compact.
- **Exclusivity assumption.** All three dual-mode hosts refuse a simulation in test mode and test mode
  during a simulation (DW `PaintModeText` `:342-343`, LH Browser comment `:607-610`, BL
  `test_sim_session.lua:23`). If that ever changed, the hosts prefer the simulation strip, matching
  today's `mark` precedence.
- **A host test reading `__fill`.** DropWatcher's suite asserts the amber literals on `f.banner`, and that
  stays true. New sim assertions use `strip.kind`, not `__fill`.
- **The MM minimized title.** If a CONFIG_CHANGED path runs `ApplyMinimized` without `ApplyTitle`, the
  explicit call added in MM-01 covers it.
- **The roster is out of step until each addon re-vendors.** No addon uses `kind` before its `<PFX>-RV`.
  The library ignores an unknown option on an older copy (minor 13 reads no `kind`), so a host on 13 that
  passed `kind="sim"` would draw amber, not error. LibStub serves the highest minor anyway.
