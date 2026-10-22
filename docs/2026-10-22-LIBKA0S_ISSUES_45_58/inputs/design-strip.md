# W.TestStrip: design for LibKa0s-Widgets-1.0 (LibKa0s v1.75.0, closes LibKa0s#48)

Read-only survey, done 2026-10-22, at these heads: LibKa0s `d9f9454` (master, unreleased v1.75.0, kit 40), DropWatcher `5611fe4`, LootHistory `8c79b23`, BankLedger `b0f9493`, MultiMeters `9638180`. The prior analysis (cluster `c48`) recommended *defer*. The owner has overruled that, so this document designs the promotion. It also shows how the design answers the analysis's objections under bars 2 and 3 (section 9).

---

## 1. What exists today (the source and the three markers it replaces)

| Addon | How test mode is marked today | Where | Body placement |
|---|---|---|---|
| **DropWatcher** (the source) | Strip `f.banner` between the filter bar and the panes. 18 px tall (`K.BANNER_H - 4`), 2 px under `f.filterHost`, amber fill `C.TONE.warn {1,0.65,0.15}` at 0.12 alpha, a 12x12 `NS.Icon("info")` at LEFT+6, a `GameFontNormalSmall` line at icon RIGHT+6, and the tooltip `NS.WindowTitleBar.TestTip` attached through `Window.AttachTooltip`. A title-bar word `TEST MODE` (`f.testText`) also shows | `modules/Window.lua:433-452` (buildBanner), shown at `:626`. Compact variant: `modules/CompactChrome.lua:365-377` (layoutStrip: shorter text, `SetWordWrap(compact)`, RIGHT anchor in compact only), `:452-456` (Paint: `SetHeight(BannerH()-4)`), `:473-482` (BannerH: one line, or `+ CC.WRAP_H` (12) when the unbounded width exceeds the room) | Panes re-anchored on every Refresh: `top = TAB_H + 4 + FILTER_H + (testMode and CC.BannerH() or 0)` (`Window.lua:479-486`) |
| **LootHistory** | A red `GameFontNormalLarge` `"TEST MODE"` on the title bar, hard-coded (not run through `L`), `SetTextColor(1,0.15,0.15)` | `modules/Browser.lua:887-892`. Toggled by `B:UpdateTestBadge()` (`:581-584`), which is called from `:575` (dataset swap) and `:1112` (Show) | Panes anchored **once**, at creation: `CreatePane` `top = titleBarH + tabStripH + contentGap + FILTERBAR_H(46) + FILTER_GAP(8)` (`:135-140`). `filterHost` at `:916-920` |
| **BankLedger** | The same badge, byte for byte | `modules/Browser.lua:992-997`; `B:UpdateTestBadge()` `:740-743`, called from `:1111` and `modules/Browser_Views.lua:301` | Panes anchored once at `paneTop = barTop + 46 + 8` (`:1012-1023`); `filterHost` `:1027-1031` |
| **MultiMeters** | A red `\|cffff2020TEST MODE\|r` appended to the title, plus `Test` on the session line. Both are header content: `frame.title:SetShown(header.show ~= false)` hides the marker when the player hides the header. This is the **header-hidden gap** | `modules/Window_Header.lua:339-343`, `:1193`; re-applied on `MSG.TEST_MODE_CHANGED` (`Window_Lifecycle.lua:95-103`) | No filter bar. The layout is built **from config only** (`Window.lua:338-378` BuildLayout, a secret-values rule: no widget geometry is read). `body` top = `pad + titleHeight + headerHeight` (`:714`), `headerFrame` top = `pad + titleHeight` (`Window_Header.lua:672`), `titleHeight = 0` when the header is hidden |

Nothing in any of the four suites pins LootHistory's or BankLedger's `testBadge`. MultiMeters pins its title marker (`tests/test_window_header.lua:593-608`). DropWatcher pins `f.banner` and `f.banner.text` across five suites (listed in section 6.1).

---

## 2. The contract

### 2.1 Placement and minor

- **Where it lives:** `LibKa0s/Widgets.lua`, the shell. It is about 45 lines and needs no new file. A new file would move the key's shape, need a `tests/majors.lua` entry and a `LibKa0s.xml` line, and touch the attach-file pairing. Widgets.lua is 655 lines now. With SearchBox (about 110) and TestStrip it reaches about 820, well under the 1500 cap and below the 1000 band.
- **Minor: one bump carries both new members.** `Widgets.lua` MINOR is **12** today (`Widgets.lua:36`) and the major key is `12.1.4.3.2`. W.SearchBox and W.TestStrip both land in the unreleased v1.75.0, so **both go out as Widgets minor 13 (key `13.1.4.3.2`)**. A file minor counts *released* changes (`docs/releasing.md` row 1: "every released change to that file"), and there is precedent for two changes sharing one bump: the 12.1.4.3.2 doc records that "the chart's half was briefly keyed 12.1.4.3.1 on the release branch; no release carried that key". Whichever item lands first bumps 12 to 13 and creates `docs/api/Widgets/version-13.1.4.3.2-docs.md` and `members-13.1.4.3.2.json`. The second adds its section and regenerates the manifest under the same key. The attach files (Reorder 1, DragHandle 4, LineChart 3, Autocomplete 2) re-pair on the shell's new minor through their `__*ShellMinor` probes, so none of their minors moves.
  - If the execution plan wants one minor per item instead (13 = SearchBox, 14 = TestStrip, key `14.1.4.3.2`), that also works. The cost is an API document for a key that never shipped. Not recommended.
- **Kit:** no change. The library does no measuring (2.4), so the mock needs no `GetUnboundedStringWidth`. Kit 41 (#46/#47) is independent.

### 2.2 Signature

```lua
--- The test-mode strip: a full-width band a window lays between its chrome and its data, saying the
--- data under it is not real. Draws itself and nothing else.
--- @param parent table          the frame to parent it to
--- @param opts table|nil        { text = string|nil, icon = string|number|nil }
---   text  the host's LOCALIZED line, set once at birth (nil -> ""); later changes go through strip.text
---   icon  a RESOLVED texture path or fileID (the host's NS.Icon("info")); nil -> no mark, text at LEFT+6
--- @return Frame strip  born HIDDEN, unanchored, HEIGHT tall, with:
---   strip.fill  Texture     BACKGROUND, all points, the collection's amber at 12%
---   strip.icon  Texture|nil ARTWORK, 12x12 at LEFT+6 (nil when opts.icon is nil)
---   strip.text  FontString  OVERLAY, GameFontNormalSmall, LEFT at icon RIGHT+6 (or strip LEFT+6),
---                           RIGHT at strip RIGHT-6, JustifyH LEFT, word wrap OFF (truncates with "...")
function lib.TestStrip(parent, opts)

--- Read-only layout numbers, published so a host lays out around the widget's own figures rather
--- than copying them (the DRAG_HANDLE / ROW_BOX precedent).
lib.TEST_STRIP = { HEIGHT = 18, RESERVE = 22 }   -- RESERVE = 2 gap + HEIGHT + 2 gap
```

Two members are added: `TestStrip` (function) and `TEST_STRIP` (table). The strip has **no methods**. This follows SearchBox's "no setters, the host writes `box.hint` directly" rule: the published fields are the surface.

### 2.3 What the strip does and does not do

**Does, at birth only:**
- Creates the Frame, its fill, its optional icon and its text.
- Calls `SetHeight(18)` once. It sets the colour, anchors its *own* regions, sets the initial text, and ends on `Hide()`. The DragHandle precedent applies: a widget born without an anchor must not flash at its parent's centre.

**Never, after the constructor returns:**
- Anchors itself, shows or hides itself, re-measures, or changes its own height or its text's anchors.

That is why a host's later `strip:SetHeight(h)`, `strip.text:SetText(...)` and `strip.text:SetWordWrap(true)` stick. DropWatcher's compact variant relies on exactly this (section 3).

**Deliberately not in it (recorded in the header's "WHAT IT DELIBERATELY IS NOT" block):**

| Omitted | Why |
|---|---|
| **A tooltip option** | Three hosts, three tooltip renderers. DropWatcher uses `Window.AttachTooltip` with TipMarks rows and keeps `widget.tooltip` for its suites. LootHistory and BankLedger use plain GameTooltip lines. MultiMeters wants none, so its body stays mouse-transparent. A library tooltip would either ignore DropWatcher's or grow a renderer. The strip is born with the mouse **off** (a bare `Frame`). A host that wants a tooltip enables the mouse and `HookScript`s OnEnter/OnLeave, which DropWatcher's `AttachTooltip` already does. |
| **A colour option** | All four adopters take the same look; that sameness is the point of promoting it ("two skins to keep in step", the file header). LibKa0s has no tone table. The amber is a file-local `STRIP_FILL = {1.00, 0.65, 0.15, 0.12}`, with a comment that it is DropWatcher's `C.TONE.warn` (`core/Constants.lua:149`) at 12%. Text colour comes from `GameFontNormalSmall` (gold), as in DropWatcher. A colour option can be added in a later minor if a consumer ever needs one. Adding it now would be an escape hatch that no consumer uses. |
| **Wrap, measure or a `:Height()` method** | Only DropWatcher's compact layout wraps, and MultiMeters *must not* measure (it lays out from config only). The two-line variant stays host-side, built on the published fields (section 3). |
| **Test-mode state** | The strip never reads test mode. The host decides when it shows and what it says. The name follows the owner's choice. |
| **Placement or body shift** | This is host layout. Hosts reserve `TEST_STRIP.RESERVE` while the strip is shown. |
| **An icon fallback** | `opts.icon = nil` is a valid, tested state: no mark, text at LEFT+6. Kit-40 caveat: a *pruned* icon still resolves to a path and draws blank, so **each adopter must declare `info`** on its `LibKa0s icons:` line (section 5). |

### 2.4 Height handling

- The one-line strip is **18 px** (`TEST_STRIP.HEIGHT`, DropWatcher's `K.BANNER_H - 4`).
- Hosts anchor it **2 px** below the chrome above it and push their body down by **`TEST_STRIP.RESERVE` = 22** (DropWatcher's `K.BANNER_H`) while it is shown, and by 0 while it is hidden.
- These numbers are constants, so MultiMeters can fold them into its config-only `BuildLayout`.
- A host with a two-line variant (DropWatcher's compact layout) sets the strip's height itself and adds its own extra to the reserve. The library publishes no wrap height: `CC.WRAP_H = 12` stays DropWatcher's own.

### 2.5 Localisation

The host passes localized text (`opts.text`, later `strip.text:SetText`). The library holds no strings. Each adopter adds its keys to `locales/enUS.lua`. LootHistory's and BankLedger's existing hard-coded `"TEST MODE"` badge text goes through `L` in the same change, which is a preview-mode rule item for v2.86.0.

### 2.6 Reference implementation (for the item's author)

```lua
-- Widgets.lua, after lib.CopyWindow
local STRIP_FILL = { r = 1.00, g = 0.65, b = 0.15, a = 0.12 }   -- DropWatcher's C.TONE.warn at 12%
local STRIP_H, STRIP_ICON, STRIP_INSET = 18, 12, 6
lib.TEST_STRIP = { HEIGHT = STRIP_H, RESERVE = STRIP_H + 4 }

function lib.TestStrip(parent, opts)
  opts = type(opts) == "table" and opts or {}
  local s = CreateFrame("Frame", nil, parent)
  s:SetHeight(STRIP_H)                       -- the local, not lib.TEST_STRIP: a host write cannot move it
  s.fill = s:CreateTexture(nil, "BACKGROUND")
  s.fill:SetAllPoints(s)
  s.fill:SetColorTexture(STRIP_FILL.r, STRIP_FILL.g, STRIP_FILL.b, STRIP_FILL.a)
  local icon = opts.icon
  if type(icon) == "string" or type(icon) == "number" then
    s.icon = s:CreateTexture(nil, "ARTWORK")
    s.icon:SetSize(STRIP_ICON, STRIP_ICON)
    s.icon:SetPoint("LEFT", s, "LEFT", STRIP_INSET, 0)
    s.icon:SetTexture(icon)
  end
  s.text = s:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")   -- from a template: never fontless
  if s.icon then s.text:SetPoint("LEFT", s.icon, "RIGHT", STRIP_INSET, 0)
  else s.text:SetPoint("LEFT", s, "LEFT", STRIP_INSET, 0) end
  s.text:SetPoint("RIGHT", s, "RIGHT", -STRIP_INSET, 0)
  s.text:SetJustifyH("LEFT")
  s.text:SetWordWrap(false)
  s.text:SetText(type(opts.text) == "string" and opts.text or "")
  s:Hide()
  return s
end
```

The RIGHT anchor is the one visible difference from DropWatcher's full layout today, which anchors LEFT only and lets text overflow. With both anchors and wrap off, the client truncates with an ellipsis. That is required for narrow meter windows. In DropWatcher's full layout the text fits, so it looks the same. In compact, DropWatcher already set this RIGHT anchor.

---

## 3. The compact variant: host-side, not an option

DropWatcher keeps its compact behaviour and builds it on the strip's published fields:

- `layoutStrip(f, compact)` (`CompactChrome.lua:365-377`) **drops its re-anchoring**, because the library already anchors LEFT and RIGHT. It keeps:
  - `b.text:SetText(compact and L[short] or L[full])`
  - `b.text:SetWordWrap(compact)`
- `CC.Paint`'s `f.banner:SetHeight(CC.BannerH() - 4)` and `CC.BannerH()`'s measurement stay as they are. `BannerH` reads `f.banner.text` and `GetWidth()`, which works the same now that the text always has both anchors (its `room` fallback still covers a zero width).
- `CC.WRAP_H` stays DropWatcher's own.

So the library carries no flag and no per-consumer branch (bar 2). The variant is presentation in one host, using the same contract every host uses.

---

## 4. MultiMeters: where the strip goes in a meter window

**Decision: at the top of the window, directly under the title strip and above the column-header row, always**, whether or not the header is shown.

```
pad
[ title strip ]            titleHeight   (0 when header.show == false)
  2px
[ TEST strip ]             18            (only while test mode is on; RESERVE 22 in all)
[ column headers ]         headerHeight
[ rows ... ]
```

Why there:
- It sits where the other three adopters put theirs, between the chrome and the data, so the grid is never read without passing the label.
- It is *not* header content, so it closes the header-hidden gap that the v2.86.0 preview-mode marker rule targets ("stays visible in every layout the display offers, a hidden header included").
- Its height is a constant, so MultiMeters' config-only layout rule holds: `BuildLayout` reads `NS.State.testMode` and a file-level `W` resolution, and no widget geometry.

**Rejected placements:**
- **Bottom of the body:** `rows.growthDirection == "UP"` anchors rows from the bottom, and a bottom band reads as status, not as a warning over the data.
- **An overlay on the rows:** it hides data and needs geometry reads.
- **"Force the title visible in test mode":** it changes `titleHeight` (and with it every anchor) behind the player's header setting, and puts the marker back inside the header the player asked to hide.

**Changes (all in MultiMeters):**
1. `modules/Window.lua` resolves `local W = LibStub and LibStub("LibKa0s-Widgets-1.0", true)` at file scope. Export_Modal already does this; there is no WidgetsSetup seam to reuse, so follow the repo's own pattern.
2. `BuildLayout` (`Window.lua:345-378`):
   - add `stripHeight = (W and NS.State and NS.State.testMode) and W.TEST_STRIP.RESERVE or 0` to the layout;
   - subtract it in `rowCapacity` (`:326-336`);
   - add it to `layout.minHeight` (`:376`).
3. Frame construction, beside `self.notice` (`:615-621`): `self.testStrip = W and W.TestStrip(frame, { text = L["TEST MODE: placeholder numbers, not your fight."], icon = NS.Icon and NS.Icon("info") })`. No tooltip, so the mouse stays off.
4. `ApplyConfig` (`:711-716`):
   - re-anchor the strip at `TOPLEFT frame pad, -(pad + titleHeight + 2)` and `TOPRIGHT frame -pad, same`;
   - body top becomes `pad + titleHeight + stripHeight + headerHeight`;
   - `SetShown(stripHeight > 0 and not minimized)`.
   - In `Window_Header.lua:672`, `headerFrame` top becomes `pad + titleHeight + stripHeight`.
5. `ApplyMinimized` (`Window_Header.lua:795-800`): hide the strip with the body. While minimized there is no data to mislabel, and the title marker remains whenever the header is shown.
6. `Window_Lifecycle.lua:95-103`, the `TEST_MODE_CHANGED` handler: replace `self:ApplyTitle()` with `self:RefreshUpvalues(); self:ApplyConfig()`, keeping `RefreshVisibility()` and `MarkDirty()`. The layout changes shape on the toggle, and the layout is only rebuilt there. `RefreshUpvalues` bumps `layoutVersion`, so rows re-anchor. `ApplyConfig` already calls `ApplyHeader`, which covers `ApplyTitle`.
7. **Keep** the red title marker (`Window_Header.lua:339-343`) and the session-line `Test` (`:1193`). The title word plus the strip is DropWatcher's reference form, and the marker covers the minimized and no-Widgets cases. (Open question 3.)

**Tests (`tests/test_window.lua`, `tests/test_window_header.lua`):**
- Test mode on: the strip is shown and its text matches. `body`'s TOPLEFT y = `-(pad + titleHeight + 22 + headerHeight)`; `headerFrame`'s y = `-(pad + titleHeight + 22)`.
- Test mode off: the strip is hidden and the offsets drop the 22.
- **`header.show = false` plus test mode: the strip is shown at y = `-(pad + 2)`.** This is the regression case for the header-hidden gap.
- Minimized: the strip is hidden.
- `layout.minHeight` and `maxRows` change by the reserve.
- With W nil (degraded), the window builds, nothing is reserved and the title marker still shows.
- The existing title-marker case at `:593-608` stays green.

**Smoke checks:**
- MM-TS-1: `/mm test` with the header shown. The strip is under the title, the column headers sit under it, and no row overlaps.
- MM-TS-2: header hidden in settings, then `/mm test`. The strip is at the top of the window.
- MM-TS-3: a narrow window. The text truncates with `...` inside the frame.
- MM-TS-4: toggle test mode off. The strip goes, the rows move back up, and the row count returns.
- MM-TS-5: minimize while in test mode. The strip hides.

---

## 5. Icon declaration (kit 40)

`Widgets.lua` cannot call Media (`Widgets.lua:12-17`), so each host resolves `NS.Icon("info")` and passes the path. Under kit 40's subset rule, a pruned `info` still resolves to a path and **draws blank, and the vendor gate cannot catch it** (CHANGELOG v1.75.0, "Declare the icons LibKa0s draws for you"). None of the four adopters has a `LibKa0s icons:` line yet. Each one's v1.75.0 re-vendor commit therefore adds it, and the list **must include `info`** next to the names the addon draws itself and the library-drawn set it wires (`close, copy, clear` for a debug console). `info` is also the Options id list's help mark, so most adopters need it anyway. In the CHANGELOG's v1.75.0 "What a consumer owes" list, add: "`W.TestStrip` adopters: `info`".

---

## 6. Per-adopter migration

Every adopter's item depends on (a) the LibKa0s TestStrip item and (b) that addon's v1.75.0 re-vendor (libs, kit, icons line, prune), because each suite loads the vendored copy. All four also add the strip's localized keys to `locales/enUS.lua`.

### 6.1 DropWatcher (moves its own copy into the library)

**Changes:**
- `core/WidgetsSetup.lua`: add `function NS.MakeTestStrip(parent, text)`, defined outside any `if W`. It answers `nil` when Widgets is absent, otherwise `W.TestStrip(parent, { text = text, icon = NS.Icon and NS.Icon("info") })`.
- `modules/Window.lua` buildBanner (`:433-452`) shrinks to these steps:
  1. `local b = NS.MakeTestStrip(body, L[full])`
  2. `if not b then return end`
  3. anchor to `f.filterHost` at 0/-2 left and right (as now)
  4. `Window.AttachTooltip(b, NS.WindowTitleBar.TestTip)`
  5. `f.banner = b`

  Delete its own fill, art, text, SetHeight and Hide: about 12 lines.
- `CompactChrome.lua`:
  - `layoutStrip` drops `ClearAllPoints`, both `SetPoint`s and `SetJustifyH` (the library owns them), and keeps `SetText` and `SetWordWrap(compact)`.
  - Rename every `b.art` reference to `b.icon`.
  - Guard `f.banner` nil in `layoutStrip`, `CC.Paint` (`:452-456`) and `CC.BannerH` (returns 0 with no banner).
  - `Window.Refresh` `:626` becomes `if frame.banner then ... end`.
  - With no Widgets: no strip, no reserve, and the title word still marks test mode.
- `core/Constants.lua:62`: keep `BANNER_H = 22`, with its comment changed to say it equals `Widgets.TEST_STRIP.RESERVE`. `test_surface_parity.lua:55` names it, so it stays.
- Update `Window.lua:4`'s header comment and the `buildBanner` comment ("the library's strip, anchored and tipped here").

**Tests:** the existing cases stay as they are, because they read `f.banner`, `f.banner.text`, `TooltipOf(f.banner)`, `GetHeight` and `__boundWidth`:
- `test_window.lua:94-104`
- `test_test_mode.lua:638-642`
- `test_window_shell.lua:82,113`
- `test_compact_chrome.lua:274-302`

New cases:
- `f.banner` is the library's strip: `f.banner.icon` texture == `NS.Icon("info")`, and the fill colour is amber at 0.12. Assert against literals, not `C.TONE`; this proves the look did not move.
- `K.BANNER_H == W.TEST_STRIP.RESERVE` and `K.BANNER_H - 4 == W.TEST_STRIP.HEIGHT`.
- Full layout: `f.banner.text` has a RIGHT point. Compact layout: wrap is on.
- Degraded (no Widgets): the window builds, test mode on raises no error, `f.banner == nil`, `layoutPanes` reserves 0 and `f.testText` is shown.

**Smoke checks:**
- DW-TS-1: `/dw test`, full layout. The strip looks identical to before (amber band, info mark, gold text) and its tooltip is unchanged.
- DW-TS-2: compact layout at 380 px. The short text wraps to two lines and the panes move down. At 520 px it is one line.
- DW-TS-3: combat ends test mode, and the strip and its reserve go.

### 6.2 LootHistory (badge kept, strip added)

**Changes:**
- `core/WidgetsSetup.lua`: add `NS.MakeTestStrip`, the same shape as DropWatcher's. The Widgets parity case (`tests/test_surface_parity.lua:87-110`) derives its members from the seam file's `function NS.` lines, so it covers the new member automatically, provided the function is defined on both paths.
- `modules/Browser.lua`:
  - After `filterHost` (`:916-920`): `frame.testStrip = NS.MakeTestStrip(frame, L["TEST MODE: a sample loot history, not yours. Combat ends it."])`. If it is non-nil, anchor TOPLEFT/TOPRIGHT to `filterHost`'s BOTTOMLEFT/BOTTOMRIGHT at y -2, and hook a tooltip: `EnableMouse(true)` plus OnEnter/OnLeave with GameTooltip lines "Test mode", "Shows: sample loot, holdings and timeline", "Ended by: combat, /lh test, the launcher menu".
  - `CreatePane` (`:135-140`) stops being the only place panes get anchored. Factor out `local function anchorPane(pane)`, using `top = … + FILTERBAR_H + FILTER_GAP + (stripShown and W.TEST_STRIP.RESERVE or 0)`. Read RESERVE through a `NS.TestStripReserve()` seam answer, or 0 when degraded.
  - Rename `B:UpdateTestBadge` to `B:UpdateTestStrip` and update both callers, `:575` and `:1112`. It now:
    - shows or hides the badge, as now;
    - shows or hides `frame.testStrip`;
    - re-anchors every pane.
  - The badge text becomes `L["TEST MODE"]`.
- The 22 px reserve comes out of the panes. Check that `minH` still leaves the table usable; nothing measured suggests otherwise.

**Tests (`tests/test_browser.lua`):** nothing pins the badge today. Add:
- Test mode on: the strip is shown with its L text, the pane TOPLEFT y moves by -22, and the badge is shown.
- Test mode off: both are hidden and y is back at the base.
- Show while already in test mode (the `:1112` path) reserves the space.
- The strip is anchored to `filterHost` (`GetPoint`).
- Degraded (no Widgets): no strip, no shift, and the badge still shows.

**Smoke checks:**
- LH-TS-1: `/lh test`. The strip sits under the filter bar, the History table starts under it, and the badge is still on the title.
- LH-TS-2: the Insights and Timeline tabs are shifted the same way.
- LH-TS-3: entering combat removes the strip and the panes move back up.
- LH-TS-4: hovering the strip shows its tooltip.

### 6.3 BankLedger (the same as LootHistory)

BankLedger has **no WidgetsSetup seam**: `W` is resolved in `modules/Browser.lua` (and Export.lua).

**Changes:**
- In `Browser.lua` after `filterHost` (`:1027-1031`): `frame.testStrip = W and W.TestStrip(frame, { text = L["TEST MODE: a sample ledger, not your bank. Combat ends it."], icon = NS.Icon and NS.Icon("info") })`, with the same anchor and tooltip as LootHistory ("Ended by: combat, /bl test, the launcher menu").
- The pane loop (`:1017-1023`) becomes an `anchorPanes()` helper that uses the reserve.
- Rename `B:UpdateTestBadge` (`:740-743`) to `B:UpdateTestStrip` and update its callers, `:1111` and `Browser_Views.lua:301`. It does the same three things as LootHistory's.
- The badge text becomes `L["TEST MODE"]`.
- The Widgets parity: BankLedger's by-name list does not project Widgets, so it needs no edit.

**Tests and smoke:** the same as LootHistory, in `tests/test_browser.lua`. Smoke BL-TS-1 to BL-TS-4 mirror LH-TS-1 to LH-TS-4 (`/bl test`, the ledger tabs, combat end, tooltip).

### 6.4 Interaction with the new simulators (owner decision 2)

The LootHistory and BankLedger simulators on Sim-1.0 are a separate item. The strip holds no state, so if a later design wants a simulation band, the host can reuse the same strip with its own text. That is not in scope here: DropWatcher shows its strip for test mode only, and its simulation is marked by its title word and footer.

---

## 7. LibKa0s deliverables

1. **`LibKa0s/Widgets.lua`:**
   - `lib.TestStrip` and `lib.TEST_STRIP` (section 2.6), MINOR 13. This is shared with SearchBox: whichever lands second does not bump again.
   - The header's first line names the strip, and a short "WHY THIS IS A LIBRARY" paragraph cites #48 and the owner's 2026-10-22 ruling.
   - "WHAT IT DELIBERATELY IS NOT" gains the five omissions from section 2.3, each with its re-check trigger: "a consumer needs a different colour, a tooltip renderer or a measured height with the same semantics as another".
2. **`tests/test_widgets_teststrip.lua`** (new), registered in `tests/run.lua`'s suite list (`:81`, after `test_widgets_autocomplete`). It installs `tests/fixture_geom.lua` per case, as `test_widgets.lua` does. For `SetJustifyH`, `SetWordWrap` and `SetTexture` recording, stub them locally on the built regions; `fixture_geom` already records `SetColorTexture` and points. Cases:
   - born hidden, unanchored (`GetNumPoints() == 0`) and 18 tall, with `fill`, `icon` and `text` present;
   - the fill is `1, 0.65, 0.15, 0.12`, all points;
   - an icon path gives `icon` its texture, 12x12 at `LEFT,+6`, with the text's LEFT on the icon's RIGHT at +6;
   - `opts.icon = nil` gives `strip.icon == nil` and the text's LEFT at strip LEFT +6;
   - a numeric fileID is accepted;
   - the text is built from `GameFontNormalSmall`, with a RIGHT point at -6, JustifyH LEFT and wrap false;
   - `opts.text` is set, and nil, a non-table opts or a non-string text each give `""`;
   - the constructor never enables the mouse; a host can `EnableMouse` and `HookScript("OnEnter")`, and its hook runs;
   - a host `SetHeight(30)` and a host `text:SetWordWrap(true)` stick (nothing re-asserts them);
   - `TEST_STRIP.RESERVE == TEST_STRIP.HEIGHT + 4`;
   - writing `lib.TEST_STRIP.HEIGHT = 99` does not change the next strip's height (the local is authoritative);
   - two strips share no regions.
3. **`docs/api/Widgets/version-13.1.4.3.2-docs.md`** (new, Current). In "What changed at 13.1.4.3.2", a TestStrip section: signature, fields, birth-only contract, height and reserve, what it is not, the icon-declaration note. Member rows: `TestStrip` and `TEST_STRIP`, **Since 13**. Mark the 12.1.4.3.2 doc *Superseded by* and add its "Moving to 13.1.4.3.2" section. Generate **`members-13.1.4.3.2.json`** with `lua tools/gen-api-members.lua`; it adds `TestStrip` (function) and `TEST_STRIP` (table). Add the row to `docs/api/README.md`.
4. **`docs/api/CONSUMERS.md`:** rows for `lib.TestStrip` and `lib.TEST_STRIP` as a host duplicate (DropWatcher) until the four adopters land, then as consumers LootHistory, BankLedger, MultiMeters and DropWatcher.
5. **`CHANGELOG.md` v1.75.0:**
   - the version block becomes `Widgets` key **13.1.4.3.2** (the same edit SearchBox makes);
   - add a "`W.TestStrip`" section;
   - in "What a consumer owes", add "declare `info`" for adopters.
   - `test_versioning` enforces that the block and `MODULES` agree.
6. Close **LibKa0s#48** with a pointer to the commit, once the four adopters land.

---

## 8. Standard (v2.86.0) touch points

- **library-stack-§7 module table, the Widgets row:** add "from **Widgets minor 13 (`LibKa0s v1.75.0`)**, `SearchBox` and **`TestStrip`**: the test-mode strip a window lays between its chrome and its data, with **`Widgets.TEST_STRIP`** (`HEIGHT`, `RESERVE`). It draws itself only; the text, tooltip, placement, body shift and when it shows stay the host's, and the icon arrives as a resolved path, so an adopter declares `info`."
- **The preview-mode marker rule** (owner decision 3): it may name `Widgets.TestStrip` as the shared form for a window with a filter bar or a data grid. Per the analysis, the title word stays acceptable on its own for displays without one. The rule's "visible in every layout, a hidden header included" clause is what the MultiMeters placement satisfies.
- **The closed set of library-drawn icons** (§7): `TestStrip` draws only the icon the host passes, so it adds nothing to that set. Its adopters still owe `info` because they pass it. State that in the rule so the set stays closed.

---

## 9. How this answers the analysis's objections

| Objection (c48) | Answer in this design |
|---|---|
| Bar 1: one consumer | The owner names four. The design gives each the same semantics: a band between chrome and data, saying the data is not real, shown only in test mode, with the same look. |
| Bar 2: the compact wrap and measure would need flags | It has no flags. The compact variant is built host-side on the published fields (section 3), the library never measures, and the birth-only contract makes the host's changes stick. |
| Bar 3: the colour is addon-local and gets restyled | The look is fixed in the library (the file-local amber). A restyle becomes a library minor that every adopter takes together, which is exactly the "two skins" argument. |
| "The art must arrive resolved" | Yes: `opts.icon`, with the kit-40 declaration owed (section 5). |
| "Hosts keep anchoring and body shift anyway" | Yes. `TEST_STRIP.RESERVE` is published so they stop copying 22. |

---

## 10. Suggested item breakdown (for the execution plan)

| ID (suggested) | Repo | Depends on | Effort |
|---|---|---|---|
| LK-TS | LibKa0s: Widgets.lua strip, tests, API doc and manifest, CONSUMERS, CHANGELOG | LK-SB if SearchBox lands first (it bumps the minor), otherwise none | S |
| DW-TS | DropWatcher | LK-TS, DW re-vendor v1.75.0 (`info` declared) | S |
| LH-TS | LootHistory | LK-TS, LH re-vendor | S |
| BL-TS | BankLedger | LK-TS, BL re-vendor | S |
| MM-TS | MultiMeters | LK-TS, MM re-vendor | M (layout, lifecycle, tests) |
| STD-TS | WowAddonStandards library-stack-§7 row and preview-mode reference | LK-TS | S |

Each addon's green gate is `lua tests/run.lua` and `luacheck .` at 0/0, with every file under 1500 lines. Size after the change, against the cap:

| File | Lines now | Lines after (about) |
|---|---|---|
| LH Browser.lua | 1231 | 1260 |
| BL Browser.lua | 1179 | 1205 |
| MM Window.lua | 1352 | 1375 |
| MM Window_Header.lua | 1233 | (minor change) |

In-client smoke checks DW/LH/BL/MM-TS-n are the owner's to run and are recorded in the bundle's smoke-test file.
