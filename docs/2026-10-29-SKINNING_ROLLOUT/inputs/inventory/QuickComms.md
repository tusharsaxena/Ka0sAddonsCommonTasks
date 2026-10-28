# Inventory: QuickComms (prefix QC)

Read-only inventory for items QC-RV and QC-01 to QC-05 of `00_PLAN.md`. Written 2026-10-29 against
`../QuickComms` at `76934d1` (master's head; the checkout already sits on `feat/2026-10-29-skinning-rollout`
with no commit of its own, tree clean), vendoring LibKa0s v1.77.0 (`CLAUDE.md:44`). Library references are
the LibKa0s main checkout at v1.79.0 (`4e1ae41`). Every `file:line` without a repo prefix is in QuickComms.

**What QuickComms draws.** Two HUD surface kinds, each with any number of instances stored per profile
(`profile.pads[id]`, `profile.dials[id]`): the **Comms Pad** (a window of secure send buttons, a header row,
section titles, a drag strip) and the **Comms Dial** (a radial ring of wedges over a secure header, a hub, a
pointer, page arrows and indicators). Both are styled per instance by a large set of player settings
(`defaults/PadStyle.lua`, `defaults/Icons.lua`, `modules/Library.lua:904-950`). Outside the HUD: the
Preview window, two modal windows (callout popup, icon browser) built on Blizzard's `SettingsFrameTemplate`,
the settings pages (library-rendered, plus many AceGUI widgets QuickComms acquires itself), and the library
tool windows (debug console, perf panel, copy window). No sim, no `W.TestStrip`, no chart, no list rows of
its own.

**QuickComms already has its own EllesmereUI bridge** (`core/EUIBridge.lua`, `settings/CalloutPopup_Skin.lua`):
it calls `EllesmereUI.RegisterSkin("QuickComms", ...)` at file load and paints the two modal windows with
EllesmereUI's facade. LibKa0s's `SkinEUI.lua` registers the same name (`LibKa0s/SkinEUI.lua:419`,
`pcall(eui.RegisterSkin, owner, ...)`), so the two collide the moment QC-01 calls `RegisterOwner`. See
doubtful call D1 (retire it, as O4 does for PGFE).

## 1. Surfaces

Token names are from `LibKa0s/SkinDefs.lua` (minor 14). "exact" means Ka0s Default's token value equals
today's literal, "near" that it does not (see section 6), "player" that the value is a stored HUD setting
(section 3).

### 1a. HUD: the Comms Pad (QC-03)

| # | Surface | Built | Typed today | Paints through (rung 1) |
|---|---|---|---|---|
| H1 | Pad root window | `modules/Pad.lua:280` (`BackdropTemplate`), `NS.ApplySkin(root)` `:286`, re-dressed `:444` with `R.SkinFor(look)` (`modules/Pad_Render.lua:341-354`) | Core.SKIN base (`NS.SKIN`, `core/CoreSetup.lua:127`) overlaid with player `look.borderStyle/borderSize/borderColor/background` (defaults `modules/Library.lua:911-914`: flat 1px `{0,0,0,1}`, bg `{0.06,0.06,0.08,0.92}`, Core's inner rule kept at size 1) | While the look follows the skin: `S.Shell(root, { noTopBar = true })` (`win.bg`, `win.border`, `win.borderSize`, `win.borderStyle`, `win.inner`: all exact). A player-set look keeps `R.SkinFor`, its colors read through `S.Resolve` (section 3). Not `NS.ApplySkin(root)` bare: Core.ApplySkin's `S.Shell(frame)` draws the top bar (`title.bg`) |
| H2 | Pad header row | `modules/Pad.lua:290`; dressed `Pad_Render.lua:413-421` (`NS.ApplySkin(header, hl.skin)` with an explicit table) | player header block (`defaults/PadStyle.lua:29-38`): Friz Quadrata 16 gold OUTLINE, bg clear, border "None" | Host-drawn (explicit skin table, not recorded): fonts and colors through `S.Resolve`; repaint on `S.OnLooksChanged` via the surfaces rebuild |
| H3 | Header texts: situation, collapse "+/-" | `Pad_Render.lua:527`, `:537` (`GameFontNormalSmall`, `GameFontNormal`) | header block font; collapse = header color, size +2 (`:420`) | header font (`hud.font` / `title.text` via section 3) |
| H4 | Header LOCKDOWN chip | `Pad_Render.lua:531`; recolored `:418` with `LOCKDOWN_COLOR {1,0.1,0.1,1}` `:359` | literal red (GameFontRedSmall's) | near `sem.modeTest {1,0.15,0.15}` / `sem.statusBad` (D7) |
| H5 | Header stale hint "updates after combat" | `Pad_Render.lua:546`; `STALE_COLOR {0.5,0.5,0.5,1}` `:360` | literal gray | `text.disabled` (exact `0.5,0.5,0.5`) |
| H6 | Section title band + text | `modules/Pad.lua:141-143`; `Pad_Render.lua:427-445` (`NS.ApplySkin(band, sl.skin)`) | player section block (`PadStyle.lua:42-51`): Friz 12 gold OUTLINE, no band | font through section 3 (`hud.font`, `text.heading`) |
| H7 | Drag strip (`W.DragHandle`) | `modules/Pad.lua:309` via `core/WidgetsSetup.lua:21-25` | library | factory: pass `spec.owner = addonName` (section 2): `handle.bg`, `handle.edge`, `text.accent`, `icon.tint`/`icon.hot` |
| H8 | Strip label marker PREVIEW / TEST MODE | `Pad_Render.lua:567` (`MARK_GREEN = "\|cff19ff19"`), `:575-578` | literal green escape | near: `sem.goodAlt {0.25,1,0.25}` (D7); escape built at call time from the token (LootHistory `NS.SkinEscape`, `core/SkinSetup.lua:215`) |
| H9 | Pad button body `qcBg` | `Pad_Render.lua:181-183` (literal `0.10,0.10,0.12,0.90`, overwritten), `:494` | player `button.background` `#3F3F3F @0.25` (`PadStyle.lua:62`) | player (no exact token; D5). The Dress literal at `:183` is dead on first apply: drop it or read `btn.bg` (exact `0.1,0.1,0.12,0.9`) |
| H10 | Pad button edge `qcEdge` | `Pad_Render.lua:185-188`, `:495` (`NS.ApplySkin(btn.qcEdge, cl.edge)`) | player `button.borderStyle/Size/Color` (`#3F3F3F @0.10`) | style via `borderStyleFromSkin` (`bar.borderStyle`); color player (D5) |
| H11 | Pad button label | `Pad_Render.lua:193`, `:496` | player button font (Friz 10 white OUTLINE, `PadStyle.lua:66-67`) | `hud.font`; color `btn.text` (exact white) |
| H12 | Padlock | `Pad_Render.lua:195-203` | `NS.Constants.GOLD` (`core/Constants.lua:241`) vertex color | `text.accent` (exact gold) |
| H13 | Veils: dim / cooling | `Pad_Render.lua:204-205` (`veil()` `:125-131`) | `{0,0,0,0.55}`, `{0,0,0,0.35}` | gap QC-G1 |
| H14 | Send-result flash | `Pad_Render.lua:206`, `:505-509`; `C.FLASH` `core/Constants.lua:252-254` | sent `{1,0.82,0}`, dropped `{0.9,0.15,0.15}`, guarded `{1,0.5,0}`, alpha 0.45 | meaning colors (skinning-§4): sent `text.accent` (exact), guarded `sem.warn` (exact), dropped near (D7); the 0.45 wash alpha rides QC-G1 |
| H15 | Hover wash | `Pad_Render.lua:207-210` | `GOLD @0.25` | gap QC-G2 |
| H16 | Button glow | `modules/Glow.lua` (LibKa0s-Glow via `core/GlowSetup.lua`), `Pad_Render.lua:498` | player `button.glowColor` gold | `S.GlowColor()` (`glow.color`, exact gold) through section 3 |
| H17 | Button shine overlay | `modules/Shine.lua:123-151` | player `button.shine*` tints, art layers | player art (D6), not skinned |
| H18 | Icon (pad square border, tint, crop) | `modules/IconStyle.lua:113-151` (`IconFrame` backdrop `:129`, `SetBackdropBorderColor` `:151`) | player `icon.*` (`defaults/Icons.lua:212-223`): border off, "Solid" 1px black | border style via `borderStyleFromSkin`, color `icon.border` (exact black) (section 3) |
| H19 | Tooltips (button, header "why", title hit) | `Pad_Render.lua:143-159`, `modules/Pad.lua:162-165` | `AddLine(line, 1, 1, 1, true)`; channel name in the chat-type color `:80-86` | GameTooltip frame untouched (rung 3); white lines `gtip.value` (exact), title line `gtip.title`; channel color rung 4 |

### 1b. HUD: the Comms Dial (QC-03)

| # | Surface | Built | Typed today | Paints through (rung 1) |
|---|---|---|---|---|
| D1 | Hub front frame, disc, rim, ring, dot | `modules/Dial_Render.lua:181-189` (`circle()` `:75-82`, initial literals overwritten); painted `PaintHubLook` `:335-352` | player `dial.hub.*` (`PadStyle.lua:129-136`): bg `{0.12,0.12,0.14,0.95}`, border gold, circle gold | border/circle `text.accent` (exact); hub bg player (D5) |
| D2 | Hub labels: stale / LOCKDOWN / TEST-PREVIEW | `Dial_Render.lua:192-202` (`GameFontDisableSmall`, `GameFontRedSmall`, `GameFontGreenSmall`) | font-object colors 0.5 gray, `{1,0.1,0.1}`, `{0.1,1,0.1}` | `S.Text(fs, "disabled")` (exact 0.5); red/green near (D7); face `hud.font` |
| D3 | Pointer arrow | `Dial_Render.lua:203-204`, `PaintPointer` `:308-317` | player `dial.slice.pointerColor` gold | `text.accent` (exact) |
| D4 | Ring title | `Dial_Render.lua:398`; `PaintRing` (`NS.PadRender.ApplyFont`) | player `dial.title.*` Friz 16 gold | `hud.font`, `title.text` (exact gold) |
| D5 | Slices: fills, highlight | `modules/Dial_Slices.lua:59-131` | player `dial.slice.background {0.06,0.06,0.08,0.80}`, `highlight {1,0.82,0,0.25}` | fill: `win.bg`'s hue with the stored opacity (D4); highlight: QC-G2 (or `text.accent` hue + stored opacity) |
| D6 | Page indicators: dots, pills, borders, back | `Dial_Slices.lua:96-103`, `:300-320` | player `dial.page.*` (`PadStyle.lua:144-156`) | current `text.accent` (exact); dot border `win.border` hue + opacity; back `win.bg` hue + opacity (D4); other-pages gray player (D5) |
| D7 | Page arrows: plate, chevron, dimmed end | `Dial_Render.lua:413-442`; `Slices.DIM = 0.4` (`Dial_Slices.lua:44`), alpha 0.6 `:441` | player `arrowColor` gold, `plateColor`; literal dim | chevron `icon.arrow` (exact gold); plate `win.bg` hue + opacity (D4); dimmed end near (D7) |
| D8 | Wedge: icon, label, padlock | `Dial_Render.lua:489-500`, `PaintWedge` `:537-556` | player `dial.label.*` Friz 12 white; lock `C.GOLD` | label `hud.font` + `text.highlight` (exact white); lock `text.accent` |
| D9 | Wedge veils, flash | `Dial_Render.lua:498-503`, `:564-568` | `{0,0,0,0.55}`, `{0,0,0,0.35}`, flash `C.FLASH` @0.45 | as H13 / H14 |
| D10 | Wedge round icon border | `modules/IconStyle.lua:163-177` (disc texture vertex color) | player `dial.icon.borderColor` black | `icon.border` (exact) |
| D11 | Dial glow, shine | `modules/Glow.lua`, `modules/Shine.lua` via `Dial_Slices.lua:240-255` | player | as H16 / H17 |
| D12 | Dial tooltips | `Dial_Render.lua:373-384` (`ShowTip`), arrows `:420-422` | `AddLine(..., 1, 1, 1, true)` | as H19 |

The secure frames under the dial and pad (`modules/SendEngine.lua:85`, `:207`, `:220`, `:233`, `:252`:
`SecureActionButtonTemplate`, `SecureHandlerClickTemplate`, `SecureFrameTemplate`) and the full-screen dial
catcher draw nothing; only their insecure child regions above are painted. See section 4.

### 1c. Windows (QC-02)

| # | Surface | Built | Typed today | Paints through (rung 1) |
|---|---|---|---|---|
| W1 | Preview window shell + title | `modules/PreviewWindow.lua:181-207` (`BackdropTemplate`, `NS.ApplySkin(f)` `:200`), title `GameFontNormal` `:173` | Core.SKIN | `S.Shell(f)` (sets `frame.title` font and `title.text`); top bar is `title.height` 30 vs the window's `TITLE_H` 24 (D9) |
| W2 | Preview window close | `PreviewWindow.lua:185` via `NS.MakeCloseButton` (`core/CoreSetup.lua:142-144`, already passes `addonName`) | library | owner already handed (`close.rest` / `close.hot`) |
| W3 | Preview window dropdown | `PreviewWindow.lua:132` `W.Dropdown(parent, DROP_W, { chevron, check })` | library | add `owner = addonName` to opts (section 2) |
| W4 | "End preview" button | `PreviewWindow.lua:107-127`, `:215-219` (`NS.ApplySkin(b)`, `REST {0.9,0.9,0.92}`, `GOLD`, `GRAY {0.6,0.6,0.6}` `:47`) | literals | as LibKa0s SimPanel's step buttons: `S.Shell`/`S.Panel` box + label `sem.stepReady` (exact `0.9,0.9,0.92`), hover `btn.hover` (exact gold), locked `sem.unknown` (exact 0.6). Or `S.Button(b)` (white rest label: a Ka0s Default change, D9) |
| W5 | Preview window tooltips | `PreviewWindow.lua:95-99` | `AddLine(body, 1,1,1)`, `AddLine(typed, GRAY)` | `gtip.value`, `sem.unknown`/`gtip.subtle` near (D8) |
| W6 | Modal window: template chrome | `settings/ModalWindow.lua:64-77` (`SettingsFrameTemplate`: NineSlice + title text, `Bg`, `ClosePanelButton`) | Blizzard template art; title `NS.BRAND` `:72` | D2 (recommended: stock under every Ka0s skin, which needs QC-G4 = PG-G1; facade paint under `eui` replaces `settings/CalloutPopup_Skin.lua:175-180`) |
| W7 | Modal window: fallback chrome (no template) | `ModalWindow.lua:81-97` (`UI-DialogBox-Border` 32px, fill `0.05,0.05,0.05,0.96`) | literals | `S.Shell(bg)` (a Ka0s Default change on a client without the template; D2) |
| W8 | Modal catcher dim | `ModalWindow.lua:99-112`, `DIM {0,0,0,0.45}` `:57` | literal | `S.Cover(dim)` → `cover.dim {0,0,0,0.6}` near (D7) |
| W9 | Modal page (header, rule, body) | `ModalWindow.lua:140` `H().CreatePanel(...)` | library | lib-auto: the Options descriptor's `addonName` (`settings/OptionsSetup.lua:106`) is the owner once registered |
| W10 | Callout popup body | `settings/CalloutPopup.lua:305`, `:350`, `:436` (`SimpleGroup`, `Label`) + `settings/Editors.lua` rows | AceGUI | `Skin:PaintAceTree(owner, group)`; release work through `Skin:OnRelease` (section 8) |
| W11 | Callout popup token glyph | `CalloutPopup.lua:226-247` (catalog `info` mark, white) | none (white art) | `icon.tint`/`icon.hot` on hover, or leave (D8) |
| W12 | Callout popup error row | `CalloutPopup.lua:63` `ERROR_COLOR = "\|cffff4040"`, `:196` | escape | `sem.badAlt` (exact `1,0.25,0.25`), escape from token |
| W13 | Callout popup token tooltip | `CalloutPopup.lua:205-209` (`SetText(..., 1,1,1)`, `AddDoubleLine(..., 1,0.82,0, 1,1,1)`) | literals | `gtip.value`, `gtip.title` (exact gold) |
| W14 | Icon browser grid cells | `settings/IconBrowser.lua:339-360`: selected wash `GOLD {1,0.82,0,0.7}` `:76`, `:345`; `SetHighlightTexture("Interface\\Buttons\\ButtonHilight-Square", "ADD")` `:352` | literal + Blizzard hilight | selected: gap QC-G3; highlight: `S.ListRow(cell, "hover")` (`list.hover`, a Ka0s change) or leave the client hilight (D8) |
| W15 | Icon browser scroller | `IconBrowser.lua:373-384` (`Slider`, `UI-ScrollBar-Knob`, track `{0,0,0,0.35}`) | literal + Blizzard knob | `S.ScrollBar(slider, { track = track })`: `scroll.track`, `scroll.thumb` (a Ka0s Default change, D3) |
| W16 | Icon browser status / count / name text | `IconBrowser.lua:370` (`GameFontHighlight`), `:429` (`GameFontDisableSmall`), `:536` (`GameFontNormal`) | font objects | `S.Text(fs, "body" / "disabled" / "heading")` |
| W17 | Icon browser "Click an icon..." | `IconBrowser.lua:77` `GRAY = "\|cffaaaaaa"`, `:178`, `:683` (chat) | escape | `cover.text` is exactly `0.667` (= `aa`) but is the combat cover's role; PC-G2's proposed `text.note` (`#aaaaaa`) is the right home (D8). `:683` is chat (exception) |
| W18 | Icon browser search glyphs | `IconBrowser.lua:80` `MUTED_GOLD {0.79,0.65,0.42}`, `MARK_GRAY {0.54,0.54,0.54}`; `:433-466` | literals | magnifier `log.tag` (`c9a66b`, 8-bit equal); clear mark `icon.dim` near (`0.55`) (D8) |
| W19 | Icon browser hint box | `IconBrowser.lua:500-531`, `HINT_FILL {0.08,0.07,0.05,0.9}`, `HINT_EDGE {0.24,0.2,0.13,1}` `:81` | literals | `drawer.boxBg`, `drawer.boxBorder` (both exact); text `S.Text(fs, "body")` |
| W20 | Icon browser AceGUI toolbar/footer | `IconBrowser.lua:390-424` (2 Dropdowns, ColorPicker), `:445-452` (EditBox), `:516` (Button), `:540-558` (2 Buttons) | AceGUI, reparented, kept for the browser's life (`place()` `:382`) | `Skin:PaintAce(owner, w)` each, at build |
| W21 | Icon browser tooltips | `IconBrowser.lua:205-211` (credit `0.7,0.7,0.7`, line `1,1,1`) | literals | `gtip.subtle` (exact), `gtip.value` |
| W22 | Wowhead link copy window | `IconBrowser.lua:491-496` via `NS.MakeCopyWindow` (`core/WidgetsSetup.lua:32-36`, sets `d.addonName`) | library | owner already handed |

### 1d. Settings pages QuickComms acquires itself (QC-04)

The pages are library-rendered (`O.RenderTabbedSchema`, `RenderGrid`, ...), so they follow the owner once the
descriptor's `addonName` (`settings/OptionsSetup.lua:106`) is registered. What QuickComms acquires by hand:

| # | Widget | Site | Notes |
|---|---|---|---|
| S1 | Dropdown (callout channel / parent pickers) | `settings/Editors.lua:204` | `PaintAce` |
| S2 | Label gaps, chooser label (`SetFontObject(GameFontNormalSmall)` `:247`) | `Editors.lua:236`, `:245`, `:252` | `PaintAce`; the font object becomes `S.Text(label.label, "heading")` or stays the row's |
| S3 | Icon chooser: Icon, Button, Icon (clear), ColorPicker, SimpleGroup | `Editors.lua:332-381` | `PaintAce`; swatch `OnRelease` `:369` must chain through `Skin:OnRelease` |
| S4 | Reorder row Icons/Labels with image tint | `Editors.lua:432`, `:482`, `:506-523`, `:598`, `:638-639` | `PaintAce`; `OnRelease` at `:522`, `:598`, `:638` chain through `Skin:OnRelease`; image tints are player glyph colors (rung 4) |
| S5 | ReorderList | `Editors.lua:405-406` `W.ReorderList{...}` | factory: `owner = addonName` (section 2) |
| S6 | Dial key EditBox | `settings/Dials.lua:225` | `PaintAce` |
| S7 | Popup rows | `CalloutPopup.lua:305`, `:350`, `:436`; its own `onRelease` helper `:256-267` sets `SetCallback("OnRelease")` | `PaintAceTree`; `onRelease` rebuilt on `Skin:OnRelease` |
| S8 | Hint text rows with color escapes inside locale keys | `Dials.lua:188`, `Groups.lua:214`, `Groups_When.lua:226`, `:706` (`\|cffa0a0a0`), `Groups_When.lua:228` (`\|cff40ff40`), `:230` (`\|cffff6060`), `:703` (`\|cffc9a66b`) | the escape moves out of the `L[...]` key (locales/enUS.lua) and is built from a token at call time: `a0a0a0` near (D7), `40ff40` `sem.goodAlt` (exact), `ff6060` near (D7), `c9a66b` `log.tag` (exact) |
| S9 | Callout dropdown labels | `Groups.lua:254-257` (`\|cffffd100` name, channel color, `\|cffb3b3b3` preview), `MUTED_GOLD = "\|cffc9a66b"` `:261`, `:299` | escapes | name `text.heading` (exact), channel rung 4, preview `gtip.subtle`/`text.muted` (D8), group part `log.tag` (exact) |
| S10 | Groups_When tooltip | `Groups_When.lua:320-321` (`SetText(c.text, 1, 1, 1)`) | literal | `gtip.value` |
| S11 | Appearance tab, first-run picker | new (QC-01, QC-04) | — | `O.AppearanceTab` on General before Keybindings (`settings/Panel.lua:53-64`: today Master controls, Behavior, Keybindings; four tabs after) ; `O.SkinPicker` gated on `skin.pickerSeen` |

### 1e. Library tool surfaces (QC-04)

| # | Surface | Site | Owner today | Change |
|---|---|---|---|---|
| T1 | Debug console | `core/DebugLogSetup.lua:90-93` (`name`, `addonName = addonName`, `font = NS.Constants.FONT_MONO`) | `addonName` already handed: lib-auto | `font` is a typed face (`core/Constants.lua:236-238`, JetBrains Mono): leave (the descriptor requires it, `DebugLogWindow.lua:356`), or resolve it from `S.Token("font.mono")` (Ka0s Default `JetBrains Mono`, exact). D10 |
| T2 | Perf panel | `core/PerfSetup.lua:49-50` (`name`, `addonName`) | handed: lib-auto | none |
| T3 | Copy window | W22 | handed | none |
| T4 | Launcher / LDB tooltip | `core/LauncherSetup.lua` (`lib:New`, library lines) | library | none (GameTooltip lines are the library's) |
| T5 | Sim panel, TestStrip, LineChart | — | QuickComms has none | — |

Chat output (`core/Namespace.lua:16` prefix `|cff00ffff[QC]|r`, `core/DebugLogSetup.lua:54`, `settings/Slash.lua:275`,
`:400`, `settings/Schema.lua:249`, `:267`, `IconBrowser.lua:683`) is not a frame QuickComms draws: section 4.

## 2. Library factories that take an owner

| Factory | Site | Today | QC-04 change |
|---|---|---|---|
| `Core.MakeCloseButton(parent, onClick, addonName)` | `core/CoreSetup.lua:142-144` | passes `addonName` | none |
| `Core.ApplySkin(frame, skin, owner)` | `core/CoreSetup.lua:128` (`NS.ApplySkin = lib.ApplySkin`, no owner); callers `Pad.lua:286`, `:444`, `Pad_Render.lua:416`, `:444`, `:495`, `PreviewWindow.lua:111`, `:200` | no owner | wrap like `MakeCloseButton` (`function(frame, skin) return lib.ApplySkin(frame, skin, addonName) end`); bare calls with no skin table become `S.Shell` (noTopBar where it has no title, H1); calls with an explicit table stay host-repainted (risk R4). Degraded stub `:84` keeps its shape |
| `W.DragHandle(parent, spec)` | `core/WidgetsSetup.lua:21-25` | no owner | `spec.owner = addonName` in the seam |
| `W.CopyWindow(d)` | `core/WidgetsSetup.lua:32-36` | `d.addonName = addonName` | none |
| `W.Dropdown(parent, width, opts)` | `modules/PreviewWindow.lua:132` | no owner | `opts.owner = addonName` |
| `W.ReorderList(spec)` | `settings/Editors.lua:406` | no owner | `owner = addonName` |
| `LibKa0s-DebugLog-1.0` descriptor | `core/DebugLogSetup.lua:90-91` | `addonName` | none |
| `LibKa0s-Perf-1.0` descriptor | `core/PerfSetup.lua:49-50` | `addonName` | none |
| `LibKa0s-Options-1.0` descriptor | `settings/OptionsSetup.lua:103-132` | `addonName` | none (gains the Appearance tab and picker calls) |
| `Skin:RegisterOwner("QuickComms", opts)` | new `core/SkinSetup.lua` | — | QC-01; `opts.log` = the debug console's writer (`NS.Debug`) |
| `Skin:PaintAce` / `PaintAceTree` / `OnRelease` | section 1d | — | QC-04 |

Not owner-taking: `LibKa0s-Glow-1.0` (colors are the host's; `S.GlowColor()` feeds them), `LibKa0s-Launcher-1.0`,
`LibKa0s-Media-1.0`.

## 3. HUD style settings (O2's one-time reset)

QuickComms has a HUD, and its style settings are **per instance**: every pad in `profile.pads[id]` and every
dial in `profile.dials[id]` carries its own copy (defaults `modules/Library.lua:904-950`, `Lib.TEMPLATES`;
`fillShape` backfills one level deep, `:1278`). The member rows are `pad.<block>.<leaf>` / `dial.<block>.<leaf>`
(`settings/SchemaMembers.lua:412`, `:557`; `settings/SchemaIcons.lua:100`), composed with `O.FontGroup` /
`O.BorderGroup` / `O.ColorPair` (`SchemaMembers.lua:417-420`, `:521-531`, `:739`, `:775`; `SchemaIcons.lua:144`,
`:172`).

**The step (QC-03).** One `perProfile` migration, `{ to = 10, ... }` appended to `NS.MIGRATIONS`
(`core/Database.lua:16-41`, runner `:46-66`), that walks `profile.pads` and `profile.dials` and calls
`Skin.ResetToSkin(surface, keys)` per instance with the dotted keys below. It lives in
`modules/Library_Migrate.lua` (208 lines), not `modules/Library.lua` (1340). New pads and dials get the companions
`true` in `Lib.TEMPLATES`, so they follow the skin from birth; `fillShape` gives a pre-adoption pad the template's
`true` too, which the step makes explicit.

**How each resolves.** Faces and border styles through the composers' `fromSkin = true` companions
(`fontFromSkin` → `hud.font`, `borderStyleFromSkin` → `bar.borderStyle`); colors through a host-built
`<key>FromSkin` bool row beside the `ColorPair` (`ResetToSkin` sets a color's companion and keeps the value),
drawn with `S.Resolve(token, value, fromSkin)`. A sentinel never enters an LSM list.

| Instance key (`pads[id].` / `dials[id].`) | Default today (file:line) | Follows (token) | Note |
|---|---|---|---|
| `look.borderStyle` | `"None"` (`Library.lua:912`) | `bar.borderStyle` (`"None"`, exact) | QC reads "None" as the flat edge (`Pad_Render.lua:326-332`); keep that reading |
| `look.borderColor` | `{0,0,0,1}` (`:912`) | `win.border` (exact) | with the two below, all-follow = `S.Shell(root, { noTopBar = true })` |
| `look.background` | `{0.06,0.06,0.08,0.92}` (`:914`) | `win.bg` (exact) | |
| `header.font` | `"Friz Quadrata TT"` (`PadStyle.lua:32`) | `hud.font` (`Ka0s Oxanium SemiBold`) | the face changes under Ka0s Default (v1.79.0's ruled Oxanium; D11) |
| `header.fontColor` | gold (`PadStyle.lua:32`) | `title.text` (exact) | |
| `header.borderStyle` | `"None"` (`:35`) | `bar.borderStyle` (exact) | |
| `section.font` | Friz (`:45`) | `hud.font` | D11 |
| `section.fontColor` | gold (`:45`) | `text.heading` (exact) | |
| `section.borderStyle` | `"None"` (`:48`) | `bar.borderStyle` (exact) | |
| `button.font` | Friz (`:66`) | `hud.font` | D11 |
| `button.fontColor` | white (`:66`) | `btn.text` (exact) | |
| `button.borderStyle` | `"None"` (`:64`) | `bar.borderStyle` (exact) | |
| `button.glowColor` | gold (`:68`) | `glow.color` (exact; `S.GlowColor()`) | |
| `icon.borderStyle` | `"Solid"` (`Icons.lua:216`) | `bar.borderStyle` (`"None"`) | host maps the skin's `"None"` to `IS.SOLID` (`modules/IconStyle.lua:37`), or a shown border would vanish |
| `icon.borderColor` | `{0,0,0,1}` (`Icons.lua:216`) | `icon.border` (exact) | |
| `icon.glowColor` | gold (`Icons.lua:219`) | `glow.color` (exact) | |
| `label.font` (dial) | Friz (`PadStyle.lua:84`) | `hud.font` | D11 |
| `label.fontColor` (dial) | white (`:84`) | `text.highlight` (exact) | |
| `title.font` (dial) | Friz (`:97`) | `hud.font` | D11 |
| `title.fontColor` (dial) | gold (`:97`) | `title.text` (exact) | |
| `slice.background` | `{0.06,0.06,0.08,0.80}` (`:110`) | `win.bg` hue, stored opacity | D4 |
| `slice.highlight` | `{1,0.82,0,0.25}` (`:112`) | QC-G2 `hud.hover` (exact), or `text.accent` hue + opacity (D4) | |
| `slice.pointerColor` | gold (`:113`) | `text.accent` (exact) | |
| `hub.borderColor` | gold (`:133`) | `text.accent` (exact) | |
| `hub.circleColor` | gold (`:134`) | `text.accent` (exact) | |
| `page.arrowColor` | gold (`:147`) | `icon.arrow` (exact) | |
| `page.plateColor` | `{0.06,0.06,0.08,0.80}` (`:148`) | `win.bg` hue, stored opacity | D4 |
| `page.currentColor` | gold (`:150`) | `text.accent` (exact) | |
| `page.dotBackColor` | `{0.06,0.06,0.08,0.80}` (`:153`) | `win.bg` hue, stored opacity | D4 |
| `page.dotBorderColor` | `{0,0,0,0.9}` (`:154`) | `win.border` hue, stored opacity | D4 |

**Not reset (player style with no exact token, D5):** `button.background` `#3F3F3F @0.25` (`PadStyle.lua:62`),
`button.borderColor` `#3F3F3F @0.10` (`:64`), `hub.background` `{0.12,0.12,0.14,0.95}` (`:132`),
`page.dotColor` `{0.4,0.4,0.4,0.9}` (`:151`), the header and section `background` / `borderColor` (clear and
white: decorations off by default, `:34-35`, `:47-48`), `icon.tint` (`Icons.lua:215`, a glyph multiplier), and
every `shine*` leaf (D6). Sizes (`fontSize`, `borderSize`, `height`) and `fontFlags` (already `"OUTLINE"` =
`hud.outline`) stay the player's: no composer companion covers them.

Every "Use class color" companion (`useClassColor*`, `NS.ResolveColor`, `core/CoreSetup.lua:133`) wins over the
skin while set; the R3 step leaves them alone.

## 4. Exceptions

**Rung 3 (skinning-§7: never touched).**
- `GameTooltip` itself: every tooltip QC fills (H19, D12, W5, W13, W21, S10) keeps Blizzard's frame; only the
  lines QC writes take `gtip.*`.
- `StaticPopup` confirms: `settings/ModalWindow.lua:173-185` (`MW.LiftConfirm`) lifts and hands back their
  strata only; never styled.
- `ColorPickerFrame`: opened by AceGUI swatches (`Editors.lua:279-370`, `TrackPicker`), never styled.
- `SettingsPanel`: `IconBrowser.lua:572-575` hooks its `OnHide` only.
- AceGUI-3.0-SharedMediaWidgets pull-outs: the LSM font and border pickers of the composed blocks.
- The secure frames (`modules/SendEngine.lua:85`, `:207`, `:220`, `:233`, `:252`; the toggle click target
  `settings/SlashVerbs.lua:98`): no visual of their own; the skin paints only insecure child regions.
- Chat output (the `[QC]` prefix `core/Namespace.lua:16`, the debug toggle line `core/DebugLogSetup.lua:54`,
  slash help `settings/Slash.lua:275`, `:400`, schema errors `settings/Schema.lua:249`, `:267`, the combat line
  `IconBrowser.lua:683`): not a frame QuickComms draws.

**Rung 4 (game-meaning colors stay).**
- WoW chat-type colors: a callout's channel in the button tooltip (`Pad_Render.lua:80-86`, `:116-121`,
  `NS.Compat.ChatColor`, fallback `core/Constants.lua:245-249`) and in the Groups dropdown labels
  (`Groups.lua:236`, `:256`).
- Class colors through every `useClassColor*` companion (`NS.ResolveColor`).
- Spell and item icons, raid target markers, and the player's glyph colors (`iconColor`, `NS.Library.IconTint`:
  `Pad_Render.lua:264`, `Dial_Render.lua:541`, `Editors.lua:482`, `IconBrowser.lua:165`, `:173`).

## 5. Gaps (rung 2)

Each needs Ka0s Default to equal today's value exactly, and no token holds it or a near one.

### QC-G1: the HUD state veils (tokens `hud.veil`, `hud.veilCool`)
- **Component.** The pad button's and the dial wedge's state veils: dim (a refused bake) and cooling (the spam
  guard), drawn over the icon and label.
- **Why no token fits.** Black washes at 0.55 and 0.35. The only black wash is `cover.dim {0,0,0,0.6}` (the combat
  cover over a settings page): 0.55 is near it, 0.35 is not, and the two must stay distinct states. The flash's
  0.45 alpha rides the same family (its hue is the meaning color, H14).
- **Ka0s Default must reproduce:** `hud.veil = {0,0,0,0.55}` (`modules/Pad_Render.lua:204`,
  `modules/Dial_Render.lua:498`), `hud.veilCool = {0,0,0,0.35}` (`Pad_Render.lua:205`, `Dial_Render.lua:500`).

### QC-G2: the HUD hover wash (token `hud.hover`)
- **Component.** The pad button's hover highlight; also the default of the dial's slice highlight
  (`dial.slice.highlight`), which then follows it.
- **Why no token fits.** Gold at 0.25. The gold washes in the schema are `list.hover` 0.10, `menu.hover` 0.15 and
  `list.sel` 0.18, each a settings-list role and visibly weaker on a HUD over the game world.
- **Ka0s Default must reproduce:** `{1,0.82,0,0.25}` (`modules/Pad_Render.lua:207-210`, `NS.Constants.GOLD`
  `core/Constants.lua:241`; `defaults/PadStyle.lua:112`).

### QC-G3: a strong selection wash (token `list.selStrong`)
- **Component.** The icon browser's selected cell.
- **Why no token fits.** Gold at 0.7 fills the whole 38px cell behind the icon. `list.sel` is gold at 0.18 (with
  `list.selOutline` none in Ka0s Default): under it the selection all but disappears behind a bright icon.
- **Ka0s Default must reproduce:** `{1,0.82,0,0.7}` (`settings/IconBrowser.lua:76`, `:343-346`).

### QC-G4: the modal window's stock template under Ka0s Default (primitive-option; the same as PG-G1)
- **Component.** The callout popup's and the icon browser's window chrome (`settings/ModalWindow.lua:64-77`):
  `SettingsFrameTemplate`'s NineSlice, `Bg` and `ClosePanelButton`.
- **Why no primitive fits.** Since SkinPaint minor 6 `Shell`, `FadeNineSlice` and `CloseButton` fade stock art
  under Ka0s Default too (`LibKa0s/SkinPaint.lua:975-994`), and a host that skips the paint under Ka0s Default
  cannot give the frame back on a live switch back (`Skin:Untrack` restores nothing). The owner ratified this
  window as "matches the settings window exactly" (`docs/ARCHITECTURE.md:260-261`), and no skin touches
  `SettingsPanel`. Needed only if D2 keeps that look; it is PG-G1's `opts.stockDefault`, so one library option
  serves both.
- **Ka0s Default must reproduce:** Blizzard's `SettingsFrameTemplate` as drawn, title `NS.BRAND` on
  `NineSlice.Text` (`ModalWindow.lua:72`), `Bg` at `MODAL_BG` (`:150`), the template's close X (`:153-154`).

## 6. Doubtful calls (for DECISIONS.md)

- **D1. Retire QuickComms's own EllesmereUI bridge in favour of the library's `eui` source (O4's ruling, applied
  to the second addon that has one).** `core/EUIBridge.lua` and `settings/CalloutPopup_Skin.lua` register
  `EllesmereUI.RegisterSkin("QuickComms", ...)`, the name `SkinEUI.lua:419` registers for the owner: one of the
  two callbacks is lost. **Recommend: retire both in QC-01**, with the TOC lines, `NS.EUIBridge`, the three call
  sites (`modules/Diagnostics.lua:59`, `settings/CalloutPopup.lua:467`, `settings/IconBrowser.lua:576`),
  `tests/test_eui_skin.lua` and `tests/test_harness.lua:95`'s `OPTIONAL_SUITES`. **No migration step is owed:**
  QuickComms never stored a choice ("There is no switch of this addon's own", `core/EUIBridge.lua:9-10`).
  A player whose popup was EllesmereUI-painted gets Ka0s Default until they pick EllesmereUI on the Appearance tab;
  the first-run picker (O3) puts that choice in front of every player. The diagnostics line becomes
  `Skin:GetEUIStatus(owner)`'s summary.
- **D2. The modal windows' chrome.** Recommend: **keep the template look under every Ka0s skin** (QC-G4 /
  PG-G1's option; the ARCHITECTURE rows 260-261 stand), paint it through the facade (`S.Shell`,
  `S.FadeNineSlice`, `Bg:SetAlpha(0)`, `S.CloseButton`, today's `CalloutPopup_Skin.lua:175-180` pass) so that
  `eui` reaches EllesmereUI as it does today, and let the page inside and every control follow the skin. If the
  owner declines the option: the windows wear the Ka0s shell under every skin (a Ka0s Default change), and the two
  deviation rows retire. The fallback chrome (`ModalWindow.lua:81-97`, a client without the template) takes
  `S.Shell` either way.
- **D3. The icon browser's scroller** (`IconBrowser.lua:373-384`). Recommend `S.ScrollBar(slider, { track =
  track })`, the corridor and knob every other scroll bar draws under every skin since SkinPaintControls minor 7
  (a Ka0s Default change: Blizzard knob and black 0.35 track become `scroll.thumb` / `scroll.track`). The
  alternative keeps the knob and asks for a track token.
- **D4. "Follow the skin's hue, keep the player's opacity"** for the dial's dark plates (`slice.background`,
  `page.plateColor`, `page.dotBackColor`: `win.bg`'s `0.06,0.06,0.08`) and the indicator border
  (`page.dotBorderColor`: `win.border`'s black). QuickComms documents opacity as each color's alpha
  (`defaults/PadStyle.lua:128`). Recommend it: exact under Ka0s Default, no new token, and the alpha is a stored
  player value, not a literal.
- **D5. HUD colors with no exact token stay the player's** (button body and edge `#3F3F3F`, hub disc
  `0.12,0.12,0.14`, other-page dots `0.4`, header and section band colors). Recommend: no companion, no reset,
  no gap; they are a style the owner picked on 2026-10-20 / 21 and read on every dark skin. The alternative is a
  `hud.*` token family (button fill, button edge, hub fill, inactive dot), four more gaps.
- **D6. Shine overlays** (`modules/Shine.lua`, `shineLook`, `shineTint`, `shineBloomA/B`). Recommend: player art,
  not skinned and not reset (a shader look with its own tints, not chrome).
- **D7. Near shades with no exact token** (each changes Ka0s Default slightly if folded). Recommend **fold**, as
  DpsRace's D-1 and D-8 do, rather than add six tokens:
  `a0a0a0` hint lines (S8) → `sem.neutral {0.62,0.62,0.66}` (Δ ≤ 0.03; `text.muted` 0.7 is the role but Δ 0.07);
  `ff6060` "Not active now" (S8) → `sem.bad {1,0.33,0.33}`;
  `19ff19` PREVIEW / TEST MODE marks (H8, D2) → `sem.goodAlt {0.25,1,0.25}` (PrettyChat draws `19ff19` too);
  LOCKDOWN `{1,0.1,0.1}` (H4, D2) → `sem.modeTest {1,0.15,0.15}`;
  flash dropped `{0.9,0.15,0.15}` (H14) → `sem.modeTest`;
  modal catcher dim `{0,0,0,0.45}` (W8) → `S.Cover` / `cover.dim` 0.6 (DpsRace D-8 folds the same 0.45);
  dial end-arrow dim `0.4 @0.6` (D7, `Dial_Render.lua:441`) → `text.disabled` 0.5 at the token's alpha.
  If the owner wants none of Ka0s Default to move, these become tokens `text.hint`, `sem.badSoft`,
  `sem.modePreview`, `sem.lockdown`, `sem.dropped`, `cover.modal`, `icon.off`.
- **D8. Exact values from another role's token.** Several QuickComms literals equal a token whose name says
  something else: `c9a66b` = `log.tag` (Groups' muted gold, the magnifier), `#aaaaaa` = `cover.text`, `b3b3b3` =
  `gtip.subtle`, `0.9,0.9,0.92` = `sem.stepReady`, `0.6` = `sem.unknown`, `0.54` ≈ `icon.dim` 0.55. Recommend:
  take the exact token where the role is close (the Preview window copies the step panels, so `sem.step*` is
  right; the magnifier and Groups' group label are the console's tag color by design, `Groups.lua:259-260`), and
  share PrettyChat's PC-G2 (`text.note` = `#aaaaaa`) for the browser's gray line if M1 adds it, else `text.muted`.
  The browser's cell highlight (`ButtonHilight-Square`, W14) and the popup's white `info` glyph (W11) stay the
  client's art.
- **D9. The Preview window's title band and button.** `S.Shell(f)` adds Ka0s Default's `title.bg` band at the
  skin-invariant `title.height` 30 over a window laid out with `TITLE_H` 24 (`PreviewWindow.lua:45`); the dropdown
  starts at 32, so it fits, but the title sits 6px down in a 30px band. Recommend: `S.Shell(f)` and move the
  title's anchor into the band (as LibKa0s's perf and sim panels, which this window copies, already draw under
  Ka0s Default). For the button, the step-panel tokens (W4) keep today's look; `S.Button` would whiten the rest
  label.
- **D10. The console font descriptor** (`core/DebugLogSetup.lua:93`, `FONT_MONO`). Recommend leave: the face equals
  `font.mono` in every shipped skin, and the descriptor requires a path at build. Revisit if DebugLog learns to read
  `font.mono` itself.
- **D11. The pads' and dials' faces move to Oxanium on adoption.** `hud.font` under Ka0s Default is `Ka0s Oxanium
  SemiBold` (v1.79.0, the owner's choice of face) while every QuickComms font block defaults to Friz Quadrata, so
  O2's reset changes the HUD face for every player. This is O2 plus v1.79.0's "Ka0s Default looks different" as
  ruled; listed because the label metrics move: pad widths (`Pad_Render.HeaderMinWidth` `:558-564`,
  `R.LabelRoom` `:247-250`, `Pad_Layout`), label truncation and the dial's label ring are measured from the face.

## 7. Re-vendor v1.77.0 → v1.79.0 obligations (QC-RV)

- **Whole-folder re-vendor from the run's tag** (`git archive`): v1.78.0's new files (`WidgetsCopyWindow.lua`,
  `DebugLogWindow.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, and the Skin major's `Skin.lua`, `SkinDefs.lua`,
  `SkinPaint.lua`, `SkinPaintControls.lua`, `SkinPaintExtras.lua`, `SkinEUI.lua`), v1.79.0's (`Toast.lua`,
  `OptionsSkinPicker.lua`), the five skin faces, Oxanium (SemiBold, Bold, OFL), the Glass textures and the eight
  bars. `tests/loader.lua:17` reads the file list from `libs/LibKa0s/LibKa0s.xml`, so no file list is pinned.
- **Options degradation stub** (`settings/OptionsSetup.lua:35-99`) gains `AppearanceTab`, `AppearanceRows`
  (v1.78.0) and `SkinPicker`, `HideSkinPicker` (v1.79.0); `tests/test_surface_parity.lua:50-60` fails until it
  does. LootHistory's shape: `AppearanceTab` answering an inert entry, `AppearanceRows` nil, `SkinPicker` nil,
  `HideSkinPicker` a no-op (`../LootHistory/settings/OptionsSetup.lua:142-153`).
- **Provenance line** `CLAUDE.md:44` (`Bundles LibKa0s v1.77.0`) rolls to the tag; `tests/test_vendor_sync.lua`
  (the kit's `VendorSync`) holds `libs/LibKa0s/` and `tests/_kit/` to it. No test pins a library minor or the
  release (grep of `tests/*.lua` for `1.77`, `v1.7`, `minor`: none outside `_kit`).
- **Icons:** `CLAUDE.md:45` declares `LibKa0s icons: all (icon browser)`, so `eye` and `settings` (the picker's)
  are kept by the prune; the README's icon-set credits do not move.
- **`## OptionalDeps`** already lists `EllesmereUI` (`QuickComms.toc:8`), as skinning-§5 asks.
- **Look change at adoption** (v1.79.0): Oxanium faces and the `Ka0s Default` bar under Ka0s Default; QuickComms
  draws no bar, so only the faces (D11). Smoke checks re-look.
- **Test pins that move with QC-03** (not the re-vendor): `tests/schema_pins.lua` (new companion rows, e.g.
  `:58`, `:60`, `:71`, `:73`, `:97`), `tests/test_pad_render.lua:213`, `:226`, `:286`, `tests/test_pad.lua:515`,
  `:671`, `tests/test_dial.lua:1264`, `:1297`, `:1354` (gold and face pins: gold stays exact; faces follow
  `hud.font` once companions default on).

## 8. Risks

- **EllesmereUI double registration** (D1): until QC-01 retires the bridge, `RegisterOwner` and
  `CalloutPopup_Skin.lua:249` both register "QuickComms"; retire in the same commit that registers the owner.
- **Secure frames and combat.** Every pad button is a `SecureActionButtonTemplate` (`SendEngine.lua:85`); the pad
  root turns protected in combat; the dial header is secure at DIALOG (`core/Constants.lua:272-280`). Paint only
  insecure regions and child holders, never `S.Button` on a send button (it hooks `OnEnable`/`OnDisable` and fades
  the template art), and route any repaint that re-lays out a pad (a face change moves widths) through
  `SendEngine.RunOrQueue`, as `Pad.Apply` already declines in combat (`modules/Pad.lua` header). A live
  `SetChoice` from another addon's *Copy to every Ka0s addon* or a profile event can arrive in combat.
- **Look-signature caches.** `Pad_Render.lookSig` (`:370-394`), `qcLookSig` (`:414`, `:442`, `:492`) and the
  per-button shine/glow caches reuse a look while its settings hold, and `NS.ApplySkin` with an explicit table is
  not recorded by the engine. A skin switch changes neither, so nothing repaints: the signature must include the
  applied style (`S.GetStyle()`) and the overrides, and `S.OnLooksChanged` must drive `Settings.RebuildSurfaces`.
- **Per-frame path.** `Dial_Render.PointerUpdate` (`:130-140`) runs every frame the dial is open (perf bucket
  `dialRender`): no token read or `S.*` call there; resolve colors into the look at rebuild (`R.Look`).
  F-001 (`Pad_Render.lua:484-490`) pinned the rebuild's byte cost: keep token reads per look, not per button.
- **Pooled AceGUI.** QuickComms sets `OnRelease` itself at `Editors.lua:369`, `:522`, `:598`, `:638` and
  `CalloutPopup.lua:261`; each must go through `Skin:OnRelease` or it overwrites the skin's restore and leaks a
  painted widget into the pool. The browser's widgets (`IconBrowser.lua:382`) are never released and reparented:
  paint once.
- **Strata.** Library holders sit at their parent's level + 1 (edges) inside the pad's and modal's bands
  (`core/Constants.lua:296-304`): `tests/test_layers.lua` greps literals only in QuickComms, but check the
  edge holder of H1 against the buttons at L+1 and the modal close at base + 5.
- **File cap.** `modules/Library.lua` 1340 and `locales/enUS.lua` 1348 lines: put the migration in
  `modules/Library_Migrate.lua`; moving escapes out of locale keys (S8) must not grow `enUS.lua` past 1500.
  `settings/SchemaMembers.lua` (834) gains about twenty color companions and the composers' `fromSkin` rows.
- **Taint.** None new if D2 is taken as written: the template frame is QuickComms's own instance, and nothing is
  written onto `SettingsPanel`, `StaticPopup*` or `GameTooltip`.

## 9. Effort

**L.** Two HUD kinds with per-instance styling (about thirty reset keys, twenty new color companions, a
per-instance migration, signature caches to rework under secure-frame constraints), plus the bridge retirement,
two modal windows, a dozen self-acquired AceGUI widgets with release chaining, and the locale escape move; the
library gaps are small (three tokens and PG-G1's option).
