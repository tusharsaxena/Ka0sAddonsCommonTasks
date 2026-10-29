# Inventory: DropWatcher (prefix DW)

Read-only inventory for M0 of `docs/2026-10-29-SKINNING_ROLLOUT/00_PLAN.md`, items DW-RV and DW-01..DW-05.
Repo `../DropWatcher`, read at the head of `feat/2026-10-29-skinning-rollout` (no commits beyond master,
`369f462`). It vendors LibKa0s v1.77.0 (`CLAUDE.md:44`) **plus `libs/LibKa0s/Toast.lua` vendored alone ahead of
the rest** (`CLAUDE.md:47-49`, TOC line after `LibKa0s.xml`, `docs/ARCHITECTURE.md:373` deviation row). The
library was read at v1.79.0 (`../LibKa0s` main checkout, tag `v1.79.0`). The vendored `Toast.lua` is v1.79.0's
file byte for byte once CRLF is normalized (`git show v1.79.0:LibKa0s/Toast.lua` diffed against the vendored file,
`\r` stripped: no difference).

The owner's rulings for this run, confirmed in the request that started this workflow, apply: O2 (the one-time HUD
style reset is **kept**), O3 (the first-run picker is **shown to everyone**: `skin.pickerSeen` defaults to false on
every profile), O4 (PGFE's own EllesmereUI bridge is retired for LibKa0s's `eui` source). O4 does not touch DropWatcher.

**Shape of the addon.** One standalone window (`DropWatcherWindow`) in two layouts, full tables and compact cards.
Around it are an inline detail card, a docked or floating Offer panel, the Edit message modal, the compact Filters
popover, the upgrade toast, GameTooltip lines with a DW-drawn grid, and settings pages that hand-build one AceGUI
table (Situations). Most chrome already goes through `NS.ApplySkin` (`Core.ApplySkin`) or the library factories.
The **text and state colors** are a private palette: `C.TONE`, `C.GOLD` and `C.IDLE` in `core/Constants.lua:178-227`.
About half of those values are not in SkinDefs, so they are the gap list (§5). The "HUD" here is the item
icon's border (Window › Icons) and the upgrade glow. There are no bars, apart from a 3px countdown bar in a cell.

Below, `S` is the owner facade `Skin:For("DropWatcher")` (to be published as `NS.Skin` by `core/SkinSetup.lua`).
A token named in a cell equals today's literal **exactly** unless the cell says otherwise. "→ G<n>" names the
proposed rung-2 token from §5.

## 1. Surfaces

### 1.1 The main window shell (`modules/Window.lua`, `modules/WindowTitleBar.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Window frame `DropWatcherWindow` (backdrop, edge, inner rule, title tint, divider) | `Window.lua:530`; skinned `:543` `NS.ApplySkin(f)` = `lib.ApplySkin` (`core/CoreSetup.lua:94`) **with no owner** | Core.SKIN (library) | `NS.ApplySkin(f, nil, "DropWatcher")` (Core minor 13 hands the frame to `S.Shell`): `win.bg`, `win.border`, `win.inner`, `title.text`, `divider`, `title.bg`. A degraded arm reads an `NS.SKIN_FALLBACK` (the LootHistory pattern) |
| Title FontString (brand, centered, gold) | `WindowTitleBar.lua:312` (`GameFontNormal`) | gold from ApplySkin (`frame.title`) | Shell's `frame.title`: `title.text`, `font.title`. `S.TitleBar(bar, { text = f.title })` if the bar should take the `title.bg` band. See D3 |
| Divider under the title bar | `WindowTitleBar.lua:321` | Core.SKIN divider via ApplySkin (`frame.divider`) | Shell's `frame.divider`: `divider` |
| Close mark (window, Offer panel, editor) | `NS.MakeCloseButton` `CoreSetup.lua:105` → `lib.MakeCloseButton(parent, onClick, addonName)` | library | already passes the owner; `close.rest` / `close.hot` follow once the owner is registered. Nothing to change |
| Minimize and layout-toggle icon buttons | `WindowTitleBar.lua:166-177`; marks `:159`, glyph fallback `GameFontHighlight` `:172` | media icon untinted (white art); glyph template white | `S.Color("icon.hot")` (WHITE) as the art's vertex color; the glyph `S.Text(glyph, ...)`, or `S.Font`. Rest tint = untinted today, so `icon.hot` (1,1,1) is exact; `icon.tint` (.7) would dim it |
| Restriction badge (lock icon + "Restricted: …" text) | `WindowTitleBar.lua:231-244` | lock `SetVertexColor(1,0.6,0.2)` `:237`, text `SetTextColor(1,0.6,0.2)` `:240` (`GameFontNormalSmall`) | → **G9** `sem.restricted` |
| TEST MODE word beside the title | `buildModeText` `WindowTitleBar.lua:249-262` (`GameFontNormalLarge`) | `TB.TEST_TONE {1,0.15,0.15}` `:124` | `S.Color("sem.modeTest")` (exact) |
| SIMULATION word beside the title | same, `:316` | `TB.SIM_TONE {0.35,0.80,1.00}` `:127` | → **G8** `sem.modeSim` (`sem.info` is .3,.8,1; `strip.sim` has the rgb at alpha .12) |
| "n new" chip (minimized) | `WindowTitleBar.lua:264-271` (`GameFontHighlightSmall`) | template white | `S.Text(fs, "body")`? No: `text.body` is .9 and the template is 1.0. Use `S.Color("text.highlight")` (1,1,1, exact) with `S.Font` |
| Tab strip (Drops, History): label + 2px underline | `buildTab` `Window.lua:397-411`; painted `paintTabs` `:605-613` | underline `C.GOLD` `:405`; label `C.GOLD` active / `C.IDLE {0.62,0.62,0.64}` idle `:609-610` (`GameFontNormal`) | Compose, as LootHistory and BankLedger do (not `S.Tab`, which adds a `tab.bg` backing DW never drew): underline `S.Color("tab.onLine")`, active label `tab.onText`, idle label → **G5** `text.idle` (`tab.text` is .7,.7,.72). Re-run `paintTabs` on `OnLooksChanged` |
| Tab placeholder text | `Window.lua:427` (`GameFontHighlight`) | template | `S.Text(fs, "body")` font only, or leave (shown only for a tab with no body; none today) |
| Mode strips (amber test, cyan sim) | `buildBanner` `Window.lua:446-456` → `NS.MakeTestStrip` → `W.TestStrip` (`core/WidgetsSetup.lua:68-71`) | library | pass `owner = "DropWatcher"` in `W.TestStrip`'s opts (Widgets `:730`): `strip.test` / `strip.sim` |
| Resize grip | `makeResizable` `Window.lua:496` → `NS.MakeResizable` | client art | none: `MakeResizable` takes no owner |
| Flat text buttons (`TB.TextButton`, the one button class: Scan group, Post my tradeables, Expand all, Ask, Offer, Announce, Send, Cancel, card actions, History actions, toast Ask) | `WindowTitleBar.lua:182-199`; callers `FooterRow.lua:98`, `CompactGroup.lua:239`, `DetailCard.lua:272,629,636`, `HistoryCard.lua:240`, `OfferPanel.lua:199`, `Toast.lua:329` | backdrop fill `0.12,0.12,0.14,1` `:188`, edge `S.innerBorder` (Core.SKIN, `0.24,0.24,0.27,0.85`) `:189`; label `GameFontHighlightSmall` white; mark untinted | → **G10** (`btn.bgAlt` / `btn.borderAlt`): `btn.bg` and `btn.border` are .1,.1,.12,.9 and .24,.24,.27,.9. Once the tokens exist: `S.Button(b, { alt = true })`-like, or compose `b:SetBackdropColor(S.Color(...))` plus a repaint hook. **Label and mark color are state tones**, set by `WG.ToneButton` (`WindowGroup.lua:388-394`): see 1.3 |

### 1.2 The filter bar and compact chrome (`modules/WindowFilterBar.lua`, `modules/CompactChrome.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Dropdowns (View, Quality, Content, Character, the tab's Sort) | `NS.MakeDropdown` `core/WidgetsSetup.lua:33-39` → `W.Dropdown` | library (Widgets SKIN) | add `owner = addonName` to the opts (Widgets `:541-543`); the shared popup menu follows the opener |
| Search box | `FB` `buildSearch` `WindowFilterBar.lua:676` → `NS.MakeSearchBox` → `W.SearchBox` | library | add `owner` to the opts (Widgets `:670-675`) |
| `FB.FLAT` table (the flat skin's fill, line, hover) | `WindowFilterBar.lua:666-672` | `fill 0.1,0.1,0.12,0.9`, `line 0.24,0.24,0.27,0.9`, `hover 1,0.82,0,0.9` | delete; its readers below take tokens. Exact: `input.bg`, `input.border`, `input.focus` |
| Compact "Filters (n)" button | `CompactChrome.lua:279-296`; `flat()` `:270-277` | FLAT fill/line `:275-276`; chevron `SetVertexColor(0.7,0.7,0.72)` `:291`; label `GameFontHighlightSmall` | `S.Inset(b)` (`input.bg`, `input.border`, flat 1px: exact) and arrow `S.Color("icon.tint")` (.7,.7,.72 exact). Not `S.Dropdown` (that paints the arrow `icon.arrow` gold) |
| Compact Filters popover panel | `CompactChrome.lua:299-310` | FLAT fill/line | `S.Inset(p)` (exact), or `S.Panel(p)` if the owner wants it to read as a panel (changes Ka0s Default: `panel.bg` .08 at .6) |

### 1.3 The drop tables, full layout (`modules/WindowGroup.lua`, `modules/WindowCells.lua`, `SideCells.lua`, `MineCells.lua`, `WindowRows.lua`, `DropsStrip.lua`, `WindowFooter.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Column header labels | `buildHeads` `WindowGroup.lua:913-925` (`GameFontNormalSmall`) | `C.GOLD` `:923` | `S.Color("list.header.text")` (gold, exact). Not `S.SortHeaderBar` (it adds the `list.header.bg` band DW never drew) |
| Encounter header row (fill, chevron, text) | `newHeader` `WindowGroup.lua:661-679` | fill `1,1,1,0.06` `:667`; chevron `C.GOLD` `:671`; text `C.GOLD` `:675` | fill `S.Color("list.box")` (1,1,1,.06 exact); chevron and text `text.heading` (gold) |
| Drop row: stripe, selected (expanded) wash | `newRow` `WindowGroup.lua:640-659` | stripe `1,1,1,0.03` `:646`; selected `C.GOLD` at 0.08 `:649` | stripe `list.stripe` (exact). Selected → **G6** `list.open` (`list.sel` is gold .18, `list.hover` gold .10). `S.ListRow` would paint both as regions with its own record; composing keeps DW's two textures |
| Drop row chevron | `WG.RowChevron` `WindowGroup.lua:624-631` | `C.CHEVRON_ROW {1,1,1,0.55}` `:628` (`Constants.lua:183`) | → **G7** `icon.muted` |
| Item button (icon + border + glow) | `itemButton` `WindowGroup.lua:467-477`; `setItem` `:481-489` | item icon art (game); border via IconStyle (1.8); `NS.Icon("help")` fallback | icon art untouched (rung 4); border, see 1.8 |
| Cell text tones (Item, Ilvl, Slot, Type, Looter, Me, Them, Trade, Trade window, Actions) | `setTone` `WindowGroup.lua:301-304`, `:693` (quality), `:699-702` (class color / fallback tone); tone tables `WindowCells.lua:60-61` (VERDICT_TONE), `:102` (TRADE_TONE), `:862-869` (ACTION_TONE, OFFER_TONE) | `C.TONE.*` (`Constants.lua:189-227`); item name `ITEM_QUALITY_COLORS`; looter class color | the palette re-plumbed: each `C.TONE` key reads a token (`NS.Tone(key)` → `S.Color(map[key])`), rebuilt on `OnLooksChanged`. `muted` → `text.muted` (exact); `plain` → **G4**; the verdict and state tones → **G1/G2/G3**; quality → `q.*` (see E4); class → untouched (rung 4) |
| Inline trade reason escape | `WindowCells.lua:516-521` (`hexOf(WC.TRADE_REASON_TONE)`, "muted") | `C.TONE.muted` as `|cff` | `text.muted` as an escape (LH `NS.SkinEscape`) |
| Verdict glyphs ▲ ≈ ▼ (monospace) | `WindowGroup.lua:542` (lead glyph), `:585` (glyph): `SetFont(C.FONT_MONO, 12, "")` | `C.FONT_MONO` = Media's "JetBrains Mono" (`Constants.lua:13-15`) | `S.Token("font.mono")` (Ka0s Default "JetBrains Mono", exact) resolved through LSM; size 12 kept. See R5 (glyph coverage under other skins) |
| Gold mark after a cell's text | `WR.NewMark` `WindowRows.lua:128-136` | `C.GOLD` `:134` | `text.accent` (gold, exact) |
| Font size row (`window.fontSize`) | `WR.SetFontSize` `WindowRows.lua:80-91` | `SetFont(base[1], size, base[3])`, the face read from the template on first use | keep the size; the face must be the skin's (see R4). Not a skin token: a layout setting |
| Trade window countdown text + 3px bar + track | `tradeWindowCell` `WindowGroup.lua:592-614`; `paintTradeWindow` `:846-859` | track `1,1,1,0.12` `:607`; bar `SetColorTexture(tone,0.9)` `:857`, tone `warn` or `good`; text `SetFontObject` bold/normal `:849` | bar `S.BarTexture(f.bar, r,g,b,0.9)` in **G2** `sem.urgent` / **G1** `sem.upgrade` (doubtful: the Ka0s Default bar texture on a 3px bar, D5); track → **G11** `bar.trackAlt`. Text font: see R4 |
| Action button label and mark tone | `WG.ToneButton` `WindowGroup.lua:388-394` | `C.TONE[red|yellow|good|cyan|bad]`, else `WHITE {1,1,1}` `:156` | tones via the palette (G1); untoned `btn.text` (WHITE, exact) |
| Drops strip (bottom): rule + info text | `DropsStrip.lua:94-110` | rule `1,1,1,0.1` `:100`; info `C.TONE.muted` `:179-180` | rule → **G12** `list.rule`; info `text.muted` (exact) |
| Drops empty state (title + line) | `DropsStrip.lua:131-140` (`GameFontNormalLarge` / `GameFontHighlightSmall`) | template gold / white | `S.Text(title, "heading")` (gold, exact; font `font.title`), line `text.highlight` |
| Footer segments ("Last loot 12s ago", situation) | `buildSegment` `WindowFooter.lua:192-199` (`GameFontDisableSmall`) | `C.IDLE` `:197` | **G5** `text.idle`. Not `S.Footer` (it adds a `foot.bg` band) |
| Scroll frames (Drops, History, compact, Offer) | `UIPanelScrollFrameTemplate` at `WindowGroup.lua:932`, `WindowHistory.lua:540`, `CompactGroup.lua:611`, `OfferPanel.lua:186` | stock Blizzard scroll bar art | `S.ScrollBar(scroll.ScrollBar)`: `scroll.*`. Changes Ka0s Default (corridor and flat knob instead of the stock art): D2 |

### 1.4 The detail card, inline under a row (`modules/DetailCard.lua`, `DetailCells.lua`, `OffSpecCells.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Boxes (For you / For the looter / Trade estimate, the chips) | `box` `DetailCard.lua:99-107`; chips `newChip` `:127-136` | backdrop fill `0.08,0.08,0.10,0.9` `:103`; edge `S.innerBorder` `:104` | → **G13** `card.bgAlt` (`card.bg` is .1,.1,.12,.85, `panel.bg` .08,.08,.10,.6); edge `win.inner` / `divider` hold the exact value but carry another role, so G13 also proposes `card.borderAlt` = .24,.24,.27,.85 (`card.border` is .9) |
| Header: item button, name (`GameFontNormal`), quality color | `DetailCard.lua:164-170`; `:384` | `ITEM_QUALITY_COLORS`, else `plain` | `q.*` (E4) / G4 |
| Side titles ("For you", "For Seta") | `DetailCard.lua:230-232` (`GameFontNormalSmall`) | `C.IDLE` `:232` | **G5** `text.idle` |
| Side rows: label (`GameFontDisableSmall`), value, glyph text, lead, "more" | `DetailCard.lua:189-220`; label color restored `:465` (`labelRGB`, captured from the template `:198`) | template 0.5 gray restored after a class color; values toned | label `text.disabled` (.5, exact); class color rung 4; values via palette |
| Stats row: per-stat name colors | `DetailCells.lua:333-345`; `C.STAT_TONE` `Constants.lua:231-236` | `statCrit 1,.62,.30`, `statHaste 1,.88,.45`, `statMastery .74,.58,1`, `statVers .45,.75,1` (`Constants.lua:218-221`); gain `greenMuted`, loss `redMuted` | stat names: exception E5 (identity by hue). gain → **G3** `sem.goodMuted`; loss → **G1** `sem.cantUse` (`redMuted`) |
| Verdict glyph in a chip / row | `newGlyph` `DetailCard.lua:111-116` | `SetFont(C.FONT_MONO, 12, "")` `:114` | `font.mono` (exact) |
| Action buttons (Ask, Offer, Edit…, Whisper) | `DetailCard.lua:272`, `:520-540` (`b.art:SetTexture(NS.Icon(a.icon))` `:534`, `SetAlpha(0.5)` disabled) | TextButton (1.1), tones via `ToneButton` | as TextButton (G10) + palette |
| Edit message modal: frame | `buildEditor` `DetailCard.lua:658-679`; `NS.ApplySkin(e)` `:668` (no owner) | Core.SKIN | `NS.ApplySkin(e, nil, "DropWatcher")` → `S.Shell` |
| Edit modal: title | `:669-671` (`GameFontNormal`) | `C.GOLD` `:671` | `S.Text(e.title, "heading")` (gold, exact; `font.title`) |
| Edit modal: the text box frame + EditBox | `editorBox` `:644-656` | `box()` fill (G13); `SetFontObject("ChatFontNormal")` `:652` | box: `S.Inset(frame)` would be `input.*` (.1,.1,.12,.9: changes); keep G13. EditBox font: `S.Font(e.box)`? `ChatFontNormal` is the chat face, deliberately (WYSIWYG for a whisper). D6 |
| Edit modal: counter | `:675` (`GameFontDisableSmall`) | template .5 gray; red refusal line toned | `text.disabled` (exact) |
| Edit modal: Send / Cancel | `:629`, `:636` | TextButton | G10 |

### 1.5 The Offer panel (`modules/OfferPanel.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Panel frame (docked or floating) | `build` `OfferPanel.lua:198-214`; `NS.ApplySkin(p)` `:206` (no owner) | Core.SKIN | `NS.ApplySkin(p, nil, "DropWatcher")` → `S.Shell` |
| Title "Who could use this?" + kind tag | `buildTitle` `:128-138` (`GameFontNormal` / `GameFontDisableSmall`) | `C.GOLD` `:132`; kind template gray | `text.heading`; kind `text.disabled` |
| Item name | `buildHeader` `:141-152`, `SetFontObject("GameFontNormal")` `:147`; quality `:281` | `ITEM_QUALITY_COLORS` | `q.*` (E4) |
| Column heads | `buildHeads` `:154-167` (`GameFontNormalSmall`) | `C.IDLE` `:162` | **G5** `text.idle` |
| Candidate rows: stripe, toned text | `OfferPanel.lua:108-116`; `setTone` `:66-69` | stripe `1,1,1,0.03` `:114`; `C.TONE` | `list.stripe` (exact); palette |
| Announce button, note | `buildFoot` `:174-184` | TextButton | G10 |
| Empty line | `:192` (`GameFontHighlight`) | template | `text.highlight` |

### 1.6 History tab (`modules/WindowHistory.lua`, `HistoryCard.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Column heads | `WindowHistory.lua:501-515` | `C.GOLD` `:510` | `list.header.text` |
| Rows: stripe, selected | `WindowHistory.lua:383-392` | `1,1,1,0.03` `:388`; gold .08 `:391` | `list.stripe`; **G6** |
| Cells: tones, class color, mono glyph | `:314-315`, `:439`, `:365` (`SetFont(C.FONT_MONO,12,"")`) | `C.TONE`; class; `C.FONT_MONO` | palette; rung 4; `font.mono` |
| Group header, chevrons | `:495` (`NS.Icon(chevron)`), header via `WG.NewHeader` | as 1.3 | as 1.3 |
| Bottom strip: rule + info | `:519-530` | rule `1,1,1,0.1` `:524`; info `GameFontDisableSmall` | **G12**; `text.disabled` |
| History card (expanded): quality name, action buttons | `HistoryCard.lua:240`, `:299`, `:333` | `ITEM_QUALITY_COLORS`; TextButton | `q.*`; G10 |

### 1.7 Compact layout cards (`modules/CompactGroup.lua`, `CompactHistory.lua`, `CompactCards.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Card background: stripe, selected, 2px quality bar | `buildBackground` `CompactGroup.lua:223-234` | `1,1,1,0.03` `:226`; gold .08 `:229`; quality `SetColorTexture(qualityColor)` `:399`, `CompactHistory.lua:115` | `list.stripe`; **G6**; `q.*` (E4) |
| Card text: tones, item name quality, looter class color, the `·` separator | `CompactGroup.lua:151-154`, `:169`, `:401`, `:417`; `SEP = "|cff9e9ea3·|r "` `:97`; `CompactHistory.lua:117` | `C.TONE`; quality; class; `9e9ea3` = `C.IDLE` | palette; `q.*`; rung 4; the separator as a **G5** `text.idle` escape |
| Mono glyph | `CompactGroup.lua:207` | `C.FONT_MONO` 12 | `font.mono` |
| Group label | `CompactGroup.lua:478` | `C.GOLD` | `text.heading` |
| Card Ask button | `CompactGroup.lua:239` | TextButton | G10 + palette |
| Header chevrons | `CompactGroup.lua:598` | as 1.3 | as 1.3 |

### 1.8 HUD-style surfaces: item icon border, upgrade glow, toast

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Item icon border (every item button: rows, cards, detail card, toast, History, Offer) | `paintBorder` `IconStyle.lua:111-133`; backdrop `read` `:80-90` | LSM border `icons.borderStyle` ("Solid" = WHITE8X8, registered at `:56-59`), `edgeSize = icons.borderSize` (2), color `icons.borderColor` {0,0,0,1}, class-color and quality companions (`defaults/Profile.lua:179-187`) | the color through `S.Resolve("icon.border", stored, borderColorFromSkin)` (`icon.border` is 0,0,0,1: exact). The style through the BorderGroup `fromSkin` companion; see §3 and **G14**. Quality color stays meaning (E4) |
| Upgrade glow (main, off-spec) | `modules/Glow.lua:72-82` → `NS.GlowLib` (LibCustomGlow-1.0) | colors stored `glow.main.color` #FFF468 / `glow.offSpec.color` #3FC7EB (`Constants.lua:225-226`, `defaults/Profile.lua:168-170`) | **not skinned**: E6 (the two colors carry main-vs-off-spec meaning; `glow.color` is one gold for every glow). D4 |
| Upgrade toast frame + close mark | `NS.NewToast` `core/ToastSetup.lua:34-39` (`d.owner = addonName` already) → Toast shell `Core.ApplySkin(f, nil, owner)` (Toast.lua:216-218) | library | already owner-aware: it skins once the owner is registered. Nothing to change |
| Toast rows: title, item name, ilvl, verdict glyphs, trade word, reason | `modules/Toast.lua:253-322` | title `C.GOLD` `:282`; `setTone` `C.TONE` `:254-255`; glyph `SetFont(C.FONT_MONO,12,"")` `:269`; templates | `text.heading`; palette; `font.mono` |
| Toast Ask button | `Toast.lua:329` | TextButton | G10 + palette |

### 1.9 Tooltip lines DW writes (GameTooltip; the frame stays Blizzard's, §7)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Tooltip title | `Window.lua:228` `GameTooltip:SetText(lines[1], C.GOLD)` | gold | `gtip.title` (exact) |
| Body lines | `Window.lua:214-218` `AddLine(…, 1, 1, 1, …)` | white | `gtip.value` (1,1,1 exact; `gtip.body` is .9) |
| Row labels and bullets `• Label:` | `TipMarks.lua:186-193` via `GroupRoster.Colored` escapes (`GroupRoster.lua:138`) | `C.TONE.mutedGold {0.80,0.68,0.36}` | → **G15** `gtip.label` |
| Hint lines | `TipMarks.lua:213` `TM.Hint` → `idle` `:185` | `C.IDLE` | → **G5b** `gtip.hint` (or `text.idle` if the owner wants one token for both; D7) |
| Verdict marks and arrow (texture escapes tinted) | `TM.Mark` `TipMarks.lua:96-103`, `TM.Arrow` `:111-117` | `C.TONE.good/yellow/red/offspec`, arrow `muted` | palette (G1), `text.muted` |
| Grid cells drawn on a pooled child of GameTooltip | `TipGrid.lua:83` (holder), `:96-104` (font strings, `SetFont(C.FONT_MONO, 12)` `:100`, `SetFontObject(lineFont)` `:103`), `:115-120` tones / `WHITE` `:44` | `C.TONE`, white | palette; `gtip.value`; `font.mono`. These are DW's own font strings on a child frame, so painting them is allowed; GameTooltip itself is not touched |
| Item name in a tooltip | `TipMarks.lua:166-180` (the link's own color code) | game quality | rung 4 / `q.*` |
| Class names | `TipMarks.lua:161` | class colors | rung 4 |

### 1.10 Library tool surfaces this addon configures

| Surface | Configured | Owner today | What DW-04 does |
|---|---|---|---|
| Debug console (and its copy window, the diagnostics dump) | `core/DebugLogSetup.lua:82-108` (`addonName = addonName`, `font = C.FONT_MONO`, no `skin` / `applySkin`) | becomes owned automatically once `RegisterOwner("DropWatcher")` runs (DebugLog.lua:305) | nothing in code; smoke-check it per skin. `font = C.FONT_MONO` is the same face as `font.mono` |
| Perf panel | `core/PerfSetup.lua:47-63` (`addonName = addonName`) | automatic (PerfPanel minor 10) | nothing; smoke |
| Sim panel | `modules/Sim.lua:275-298` (`name = "DropWatcher"`, `panel = NS.SimPanel.FIELDS`, which carries no colors) | automatic (SimPanel minor 7 reads the adapter's `name`) | nothing; smoke |
| Test / sim strips | 1.1 | needs `owner` | DW-01 / DW-04 |
| Toast shell | 1.8 | already `d.owner` | nothing |
| Launcher (minimap button, context menu, tooltip) | `core/LauncherSetup.lua:84-113` | LibDBIcon button and the client's MenuUtil menu | never touched (E2) |
| Keybind toggle button `DropWatcherToggleWindow` | `LauncherSetup.lua:34` | hidden, no visuals | nothing |

### 1.11 Settings-page widgets DW acquires itself (`settings/PageEditors.lua`, `settings/Profiles.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Clear history button | `PageEditors.lua:88-98` `AceGUI:Create("Button")` | stock | `Skin:PaintAce(w, owner)` (LH `NS.SkinPaintAce`); released with the page |
| Situations table host (raw frame), header labels, stripes, labels | `buildSituationTable` `PageEditors.lua:226-238`; headers `:214-221`; slots `:194-212`; repaint `:116-132` | headers `SIT_HEAD_RGB {0.91,0.77,0.42}` `:110,:219`; stripe `1,1,1,0.03` `:202`; labels `0.86` live / `0.5` off `:111,:123` | headers `text.headingAlt` (exact); stripe `list.stripe`; labels `text.bodyAlt` (.86) / `text.disabled` (.5), both exact |
| Situations table AceGUI CheckBox ×20, Dropdown ×20 | `situationCheck` `:147-159`, `situationPick` `:161-177` | stock; acquired once a session, parented to raw frames, **never released** | `PaintAce` each; see R2 (they outlive the page's re-render, so a live skin switch does not reach them) |
| Situations placeholder SimpleGroup with its own `OnRelease` | `P.SituationTable` `:258-281`; `holder:SetCallback("OnRelease", …)` `:272` | none | if painted, chain the release work through `Skin:OnRelease` (anti-pattern #107); an unpainted SimpleGroup needs nothing |
| Weights import EditBox, token Buttons | `:351`, `:454` (`AceGUI:Create`) | stock | `PaintAce` |
| Text rows with font objects | `:62`, `:65`, `:77`, `:370`, `:398`, `:496-498`, `:527` (`h.TextRow(…, { fontObject = … })`) | GameFont templates | library TextRow; the library paints it under the owner (no DW code) |
| Profiles page SimpleGroup + AceConfigDialog (AceDBOptions) | `settings/Profiles.lua:27-37` | stock AceGUI tree | `PaintAceTree(container)` as LootHistory does, or leave stock (D8) |
| Schema-driven rows (every page) | library flow engine | library | nothing beyond registering the owner (Options paints rows for a registered owner) |

### 1.12 Out-of-window text (chat)

`NS.PREFIX = "|cff00ffff[DW]|r"` (`core/Namespace.lua:16`); `debug logging |cff40ff40ON|r / |cffff4040OFF|r`
(`core/DebugLogSetup.lua:54`, `locales/enUS.lua:165-166`); command highlights `|cffFFFF00` (`settings/Slash.lua:111,220`,
`settings/SlashVerbs.lua:20,178`, `locales/enUS.lua:65,85,172-173`); schema errors `|cffff0000` (`settings/Schema.lua:232,253`).
They print to the client's chat frame. See E8.

`settings/Editors.lua:236` `RED = "|cffff4040%s|r"` (a refusal in a settings row) is on the settings panel:
`sem.badAlt` (1,.25,.25 = `ff4040`, exact) as an escape.

## 2. Library factories that take an owner

| Factory | Call site | Owner today | Change |
|---|---|---|---|
| `Core.ApplySkin(frame, skin, owner)` | `Window.lua:543`, `OfferPanel.lua:206`, `DetailCard.lua:668` (through `NS.ApplySkin`) | **none** | pass `nil, "DropWatcher"`, or wrap `NS.ApplySkin` in `CoreSetup.lua:94` as `MakeCloseButton` is wrapped (`:105`) so every call says who is asking |
| `Core.MakeCloseButton(parent, onClick, owner)` | `CoreSetup.lua:105-107` wrapper; callers `WindowTitleBar.lua:276`, `OfferPanel.lua:136`, `DetailCard.lua:672` | `addonName` | none |
| `W.Dropdown(parent, width, opts)` | `core/WidgetsSetup.lua:35` | none | `owner = addonName` |
| `W.SearchBox(parent, width, opts)` | `core/WidgetsSetup.lua:51` (opts from `WindowFilterBar.lua:676`) | none | set `opts.owner = addonName` in the seam |
| `W.TestStrip(parent, opts)` | `core/WidgetsSetup.lua:70` | none | `owner = addonName` |
| `DebugLog:New(d)` | `core/DebugLogSetup.lua:82` | `addonName` (owner by default) | none |
| `Perf:New(d)` | `core/PerfSetup.lua:47` | `addonName` | none |
| `Sim:New(d)` (panel) | `modules/Sim.lua:275` | `name = "DropWatcher"` | none (the literal equals the folder; `addonName` is safer) |
| `Toast:New(d)` | `core/ToastSetup.lua:38` | `d.owner = addonName` | none |
| `O.SkinPicker(spec)` / `O.AppearanceTab(spec)` | new (DW-01, DW-04) | — | spec owner = `addonName` |
| `Skin:PaintAce(w, owner)` / `Skin:OnRelease` | new (DW-04) for 1.11's widgets | — | owner bound in a seam helper |
| Not used by DW: `W.CopyWindow`, `W.LineChart`, `W.DragHandle`, `W.ReorderList`, `W.Autocomplete` | — | — | — |

## 3. HUD style settings (O2, the one-time reset)

DropWatcher has a small HUD: the **item icon's border** (Window › Icons, a composed `BorderGroup`,
`settings/ComposedRows.lua:33-62`) and the **upgrade glow**. There are no bars, no HUD font face setting and no HUD
texture setting.

| Setting | Schema key | Default (`defaults/Profile.lua`) | How it follows the skin |
|---|---|---|---|
| Border style | `icons.borderStyle` | `"Solid"` (`:182`) | `fromSkin = true` on the `BorderGroup` (`ComposedRows.lua:33`) emits `icons.borderStyleFromSkin`; `Skin.ResetToSkin(p, { "icons.borderStyle" })` sets it true. **But the composer's companion answers `bar.borderStyle`**, which is `"None"` in Ka0s Default. Followed literally, R3 would erase every icon border on Ka0s Default. DW must draw the skin's icon edge instead: `S.IconBorder(b, { size = … })` (flat, `icon.border`), which reproduces Solid black exactly. The disabled picker would still show "None". → **G14** |
| Border color | `icons.borderColor` | `{0,0,0,1}` (`:184`) | a color table: ResetToSkin sets `icons.borderColorFromSkin = true`; DW reads `S.Resolve("icon.border", stored, profile.icons.borderColorFromSkin)` (`icon.border` 0,0,0,1, exact). The composer emits no color companion row, so the flag is invisible in the panel until the player picks a color (which should clear it). D9 |
| Border thickness | `icons.borderSize` | `2` (`:183`) | **leave out of the reset.** ResetToSkin would write the `"@skin"` sentinel into a number row validated `Check.inRange(1,16)` (`ComposedRows.lua:57`); `RepairStoredSettings` (`core/Database.lua`, step 2) and the slider would meet a string. There is no `icon.borderSize` token. → G14 |
| Show border | `icons.borderShow` | `true` | not style (a player's on/off). Never reset: ResetToSkin sets a bool to **true**, which would turn borders back on for a player who turned them off |
| Use class color / Color by item quality | `icons.useClassColorBorder`, `icons.borderQuality` | `false`, `false` | meaning (class, quality); never reset |
| Icon zoom | `icons.zoom` | `0.1` | a crop, not a style; never reset |
| Glow colors | `glow.main.color`, `glow.offSpec.color` (+ `useClassColor`) | #FFF468, #3FC7EB (`:168-170`) | E6: the two colors mean main spec vs off-spec; `glow.color` is one token. Not reset (D4) |
| Glow style and knobs | `glow.*.type`, `pixel*`, `autocast*`, … | `pixel`, … | behaviour, not skin; never reset |
| Table font size | `window.fontSize` | `0` (= template size) (`:151`) | a layout size, not a face; 0 already means "the default", which follows the skin's face (R4). Not reset |

The R3 step for DW-03 is therefore a **migration step 10** (`core/Database.lua:209-221`, `perProfile = true`):
`Skin.ResetToSkin(profile, { "icons.borderStyle", "icons.borderColor" })`. It runs on profiles that have an
`icons` table; ResetToSkin skips a path whose table does not exist, so a profile that never stored `icons` keeps the
AceDB defaults. Those defaults need `borderStyleFromSkin = true, borderColorFromSkin = true` too, or a fresh profile
would not follow the skin. The same step can seed `skin.pickerSeen = false` (O3), though AceDB's default already
answers false.

## 4. Exceptions

| # | Rung | What | Reason |
|---|---|---|---|
| E1 | 3 | GameTooltip's frame (`Window.lua:224-236`, `RowTooltip.lua`) | skinning-§7: lines DW writes take tokens (1.9); the frame keeps Blizzard's look. `TipGrid`'s holder child (`TipGrid.lua:83`) is DW's own font strings and is painted, but gets no backdrop |
| E2 | 3 | Launcher: LibDBIcon minimap button, the MenuUtil context menu, the launcher tooltip (`core/LauncherSetup.lua`) | Blizzard shared menu and a third-party button |
| E3 | 3 | StaticPopups: Reset all (`settings/Schema.lua:321`), Clear history (`modules/History.lua:607`), retention (`modules/HistoryRetention.lua:244`) | skinning-§7 |
| E4 | 4 | Item quality colors: names, compact quality bars, the icon border's "Color by item quality" (`WindowGroup.lua:693`, `CompactGroup.lua:399-401`, `CompactHistory.lua:115-117`, `DetailCard.lua:384`, `OfferPanel.lua:281`, `HistoryCard.lua:299`, `IconStyle.lua:96-104`, `TipMarks.lua:171-180`) | meaning. Read through the `q.*` tokens (Ka0s Default = the client's ITEM_QUALITY_COLORS written out, so exact) via an `NS.QualityColor` helper (LH's), which keeps the hue and lets a skin adjust legibility. A link's own `|c` code inside a tooltip stays the game's |
| E5 | 4 | Secondary-stat name colors (`C.STAT_TONE`, `Constants.lua:218-221,231-236`; `DetailCells.lua:333-345`) | identity by hue, like LootHistory's per-source colors (SkinDefs "Split roles": identity colors are not tokens) |
| E6 | 4 | Upgrade glow colors (`glow.main.color`, `glow.offSpec.color`) | the two hues tell main spec from off-spec, and both are the player's stored swatches with a class-color companion. `glow.color` (gold) cannot hold two meanings. The owner may overrule (D4) |
| E7 | 4 | Class colors (looter, member names: `GroupRoster.lua:138`, `WindowGroup.lua:702`, `WindowHistory.lua:439`, `CompactGroup.lua:417`, `DetailCard.lua:465`, `TipMarks.lua:161`) and item, spec and class icon art | game meaning |
| E8 | 3 | Chat output: `NS.PREFIX` cyan `[DW]`, `|cffFFFF00` command highlights, ON/OFF, schema errors (1.12) | printed into the client's chat frame, not a frame DW draws; the prefix is the addon's brand identity. Recommend leaving all of it (D10) |
| E9 | 3 | AceGUI-3.0-SharedMediaWidgets pull-out (the Border style picker) and ColorPickerFrame (the glow and border swatches) | skinning-§7 |
| E10 | 3 | Blizzard Settings panel chrome, the Keybindings page | skinning-§7; the library's own rows paint for the owner |
| E11 | — | The resize grip (`Core.MakeResizable`) | the library factory takes no owner; client art |

## 5. Gaps (rung 2)

DW keeps its own palette, `C.TONE` / `C.GOLD` / `C.IDLE` (`core/Constants.lua:178-227`), plus a handful of chrome
literals. Where a value equals a SkinDefs token it is mapped in §1, and needs nothing: `C.GOLD` = `text.heading` /
`title.text` / `list.header.text` / `tab.onLine`; `muted` = `text.muted`; `TEST_TONE` = `sem.modeTest`; `FLAT` =
`input.*`; stripes = `list.stripe`; header fill = `list.box`; `SIT_HEAD_RGB` = `text.headingAlt`; tooltip white =
`gtip.value`; `ff4040` = `sem.badAlt`; `font.mono` = JetBrains Mono. Each gap below has **no token holding its
value**. Snapping it to the nearest token would change Ka0s Default's pixels, which the plan's policy forbids without
asking (skinning-§4: "Ka0s Default reproduces the look as it was"). That is the same reason SkinDefs minors 5 and 6
added LootHistory's near-duplicates (`sem.goodAlt`, `text.bodyAlt`, …). Proposed names follow the schema's groups.
Every other skin derives each token through FOLLOW from its nearest sibling (noted per gap); Azeroth and High Contrast
need their own legible values.

### DW-G1: the verdict and state tones (seven `sem.*` tokens)

The drop tables, cards, toast and tooltips color every verdict, trade estimate and action state from one palette
(`WindowCells.lua:60-61` VERDICT_TONE, `:102` TRADE_TONE, `:862-869` ACTION_TONE / OFFER_TONE, `TipMarks.lua:67-71`).
These are addon meaning colors. skinning-§4 requires them to be read from semantic tokens whose Ka0s Default value is
the addon's old one, and no token holds these values:

| Proposed token | Ka0s Default (exact) | Today | Nearest existing (why not) |
|---|---|---|---|
| `sem.upgrade` | `0.30, 0.85, 0.40, 1` | `C.TONE.good` `Constants.lua:190` (upgrade, Yes/Likely tradeable, Traded) | `sem.good` .35,.80,.45; `sem.on` .3,.85,.3 |
| `sem.sidegrade` | `1.00, 0.96, 0.42, 1` | `C.TONE.yellow` `:195` (sidegrade, waiting on someone) | none |
| `sem.downgrade` | `1.00, 0.36, 0.32, 1` | `C.TONE.red` `:197` (downgrade, your move, trade No) | `sem.statusBad` 1,.32,.32; `sem.bad` 1,.33,.33 |
| `sem.offer` | `0.35, 0.82, 0.95, 1` | `C.TONE.cyan` `:200` (Offer while your move) | `sem.info` .3,.8,1 |
| `sem.offSpec` | `0.30, 0.85, 0.85, 1` | `C.TONE.offspec` `:203` | none |
| `sem.cantUse` | `0.72, 0.36, 0.34, 1` | `C.TONE.redMuted` `:207` (Can't use; a stat lost) | `sem.boundBoPAlt` .85,.45,.45 |
| `sem.notWanted` | `0.55, 0.55, 0.58, 1` | `C.TONE.bad` `:191` (not wanted, not tradeable, no action) | `icon.dim` .55,.55,.55 |

FOLLOW for the other skins: `sem.upgrade` ← `sem.good`, `sem.downgrade` ← `sem.bad`, `sem.offer` ← `sem.info`,
`sem.sidegrade` ← `sem.statusWarn`, `sem.notWanted` ← `sem.neutral`, `sem.cantUse` ← `sem.badAlt`, `sem.offSpec` ← its own teal.

### DW-G2: `sem.urgent`, a trade window ending soon

Amber `1.00, 0.65, 0.15, 1` (`C.TONE.warn`, `Constants.lua:192`; the countdown text and its 3px bar,
`WindowGroup.lua:849-857`; the warning chip). `sem.warn` is `1, 0.5, 0`. `strip.test` carries this rgb, but at alpha
.12 and as a wash. FOLLOW ← `sem.warn`.

### DW-G3: `sem.goodMuted`, a stat gained

`0.42, 0.74, 0.46, 1` (`C.TONE.greenMuted`, `Constants.lua:210`; the detail card's Stats row, `DetailCells.lua:343`).
A value, deliberately dimmer than a verdict. No green token near it (`sem.boundBoEAlt` is .55,.8,.6). FOLLOW ← `sem.good`.
`sem.cantUse` (G1) is its loss partner.

### DW-G4: `text.bodyBright`, the tables' plain text

`0.92, 0.92, 0.92, 1` (`C.TONE.plain`, `Constants.lua:214`; the default of every `setTone` in `WindowGroup.lua:302`,
`DetailCard.lua:80`, `OfferPanel.lua:67`, `Toast.lua:254`, `WindowHistory.lua:314`, `CompactGroup.lua:152,169`).
`text.body` .9, `text.bodyAlt` .86, `text.subtle` .85, `text.highlight` 1. (`sem.boundBoE` has the rgb, at .95, with
an unrelated role.) FOLLOW ← `text.body`.

### DW-G5: `text.idle` (and G5b `gtip.hint`), the idle gray

`0.62, 0.62, 0.64, 1` (`C.IDLE`, `Constants.lua:179`): idle tab labels (`Window.lua:609-610`), footer segments
(`WindowFooter.lua:197`), detail side titles (`DetailCard.lua:232`), Offer column heads (`OfferPanel.lua:162`), the
compact separator escape (`CompactGroup.lua:97`, `9e9ea3`), and tooltip hints and idle words
(`TipMarks.lua:185,213`). `tab.text` / `text.muted` are .7,.7,.72; `sem.neutral` is .62,.62,.66. FOLLOW ←
`text.muted` / `gtip.muted`. Whether the tooltip half is its own `gtip.hint` is D7.

### DW-G6: `list.open`, an expanded row's wash

Gold `1, 0.82, 0, 0.08` (`WindowGroup.lua:649`, `WindowHistory.lua:391`, `CompactGroup.lua:229`). `list.hover` is
gold at .10 and `list.sel` gold at .18. FOLLOW ← `list.hover` (accent at low alpha).

### DW-G7: `icon.muted`, a drop row's chevron

`1, 1, 1, 0.55` (`C.CHEVRON_ROW`, `Constants.lua:183`, `WindowGroup.lua:628`). `icon.tint` is .7,.7,.72,1 and
`icon.dim` .55,.55,.55,1: the same perceived gray over the dark row only, since this one is translucent white. FOLLOW
← `icon.tint`.

### DW-G8: `sem.modeSim`, the SIMULATION word

`0.35, 0.80, 1.00, 1` (`TB.SIM_TONE`, `WindowTitleBar.lua:127`). It is the text partner of `sem.modeTest` (the TEST MODE
word, already a token). `sem.info` is .3,.8,1. LootHistory's SIM_MARK took `sem.info`, so this is a split role. FOLLOW ←
`strip.sim`'s rgb at alpha 1. **Recurs**: BankLedger, MultiMeters and KickCD draw a sim word too, so check their
inventories for the same value before naming it.

### DW-G9: `sem.restricted`, the restriction badge

Orange `1, 0.6, 0.2, 1` (`WindowTitleBar.lua:237,240`): asks are held (combat, encounter, a restricted instance).
`sem.warn` is 1,.5,0 and `sem.boundWarbandUE` .95,.52,.12. FOLLOW ← `sem.warn`.

### DW-G10: `btn.bgAlt` / `btn.borderAlt`, the flat text button

DW's one button class (`WindowTitleBar.lua:182-199`): fill `0.12, 0.12, 0.14, 1` and edge `0.24, 0.24, 0.27, 0.85`
(Core.SKIN `innerBorder`). `btn.bg` / `btn.border` are `.1,.1,.12,.9` / `.24,.24,.27,.9`, which LootHistory's flat
buttons and `FLAT` use. Painting it needs either `S.Button(b, { alt = true })` (a **primitive option**) or DW composing
the backdrop itself plus `S.WhiteButtonLabel`. The label and mark tint is DW's state tone (G1) and must survive
`S.Button`'s hover recolor, so composing is likelier (D1). FOLLOW ← `btn.bg` / `btn.border`.

### DW-G11: `bar.trackAlt`, the countdown bar's track

`1, 1, 1, 0.12` (`WindowGroup.lua:607`). `bar.bg` is `0,0,0,.5`, `chart.track` `1,1,1,.06`; `list.boxEdge` has the value
but means a box edge. FOLLOW ← `chart.track`. (If the owner accepts `chart.track` here the gap closes; D5.)

### DW-G12: `list.rule`, the strips' top rule

`1, 1, 1, 0.10` (`DropsStrip.lua:100`, `WindowHistory.lua:524`). `divider` is .24,.24,.27,.85, `section.rule` gold .35,
`list.boxEdge` 1,1,1,.12. FOLLOW ← `divider`.

### DW-G13: `card.bgAlt` / `card.borderAlt`, the detail card's boxes and chips

Fill `0.08, 0.08, 0.10, 0.9` and edge `0.24, 0.24, 0.27, 0.85` (`DetailCard.lua:99-107`; also the editor's text box
`:645`). `card.bg` .1,.1,.12,.85, `card.border` .24,.24,.27,.9, `panel.bg` .08,.08,.10,.6. `S.Card(f, { alt = true })`
would be a primitive option; composing the backdrop works without one. FOLLOW ← `card.bg` / `card.border`.

### DW-G14 (primitive-option + tokens): the icon border's skin values

`OptionsCompose`'s `fromSkin` companion maps `borderStyle` to `bar.borderStyle` (`OptionsCompose.lua:326-333`, the `FROM_SKIN` map), Ka0s
Default `"None"`, with `bar.borderSize` 1. DW's icon border today is `Solid` (flat WHITE8X8), 2 px, black
(`defaults/Profile.lua:179-187`, `IconStyle.lua:51-59,80-90`). Two pieces are missing:

- **tokens** `icon.borderStyle` (Ka0s Default `"flat"`, the `S.IconBorder` edge) and `icon.borderSize` (Ka0s Default
  `2`), so a skin can say how thick and in what art an icon is edged. `icon.border` (the color) exists.
- **an option** on `BorderGroup`'s `fromSkin` naming the token family (for example `fromSkin = "icon"` →
  `icon.borderStyle`). The disabled picker then shows the icon's skin value and not the bar's "None", and `Resolve`
  answers the right token.

**Recurs**: AuraMaster, KickCD and ConsumableMaster each compose an icon `BorderGroup` (DW's "Solid" is AuraMaster's
name, `IconStyle.lua:23-25`), so the M1 consolidation should size this once for all four. Without it, DW-03 can still
draw `S.IconBorder` while the companion is on, but `icons.borderSize` cannot be reset and the panel shows "None".

### DW-G15: `gtip.label`, a tooltip row's label and bullet

Muted gold `0.80, 0.68, 0.36, 1` (`C.TONE.mutedGold`, `Constants.lua:213`; `TipMarks.lua:185-193`). `text.headingAlt`
.91,.77,.42 and `gtip.title` gold. FOLLOW ← `gtip.title` dimmed (each skin's own).

## 6. Doubtful calls (for DECISIONS.md)

| # | Call | Recommendation |
|---|---|---|
| D1 | TextButton (G10): `S.Button` with a new `alt` option, or DW composing the backdrop from `btn.bgAlt`/`btn.borderAlt` and recoloring on `OnLooksChanged` | **Compose.** `S.Button` owns label color and hover (`btn.text` / `btn.hover`); DW's label carries state tones (`WG.ToneButton`) that a hover repaint would overwrite. Add only the tokens |
| D2 | `UIPanelScrollFrameTemplate` bars: `S.ScrollBar` (corridor + flat knob in every skin, including Ka0s Default) or leave stock | **`S.ScrollBar`**, as LootHistory's History window. It changes Ka0s Default's scroll bar from the stock art, which is the library's Ka0s Default look since SkinDefs minor 10. Flag it to the owner in smoke |
| D3 | Title bar: Shell's top bar (`title.bg` band, `title.height` 30 = DW's `TITLE_H`) or keep DW's bare bar | **Shell's top bar.** Ka0s Default's `title.bg` (.04,.04,.05,.9) is the band LootHistory's window wears; DW's window had none, so this is a visible Ka0s Default change. Ask in smoke, or pass `{ noTopBar = true }` for zero change |
| D4 | Glow colors: E6 (keep the stored swatches) or follow `glow.color` and reset at R3 | **E6.** One token cannot carry main vs off-spec; resetting both to gold erases the distinction. A future `glow.alt` token could make it skinnable |
| D5 | The countdown bar: `S.BarTexture` (the skin's bar texture on a 3px bar) or a flat `SetColorTexture` in token colors | **Flat, tokens only.** At 3px a texture reads as noise, and the Ka0s Default bar texture would change today's flat look. Track: `chart.track` (.06) if the owner accepts it, else G11 |
| D6 | The Edit message box's `ChatFontNormal` | **Keep the chat face**: the box previews a whisper. Paint only its box (G13) |
| D7 | Tooltip hint gray: its own `gtip.hint` (G5b) or reuse `text.idle` | **`gtip.hint`.** Tooltip lines already have their own `gtip.*` family, so a light skin can differ there |
| D8 | Profiles page (AceConfigDialog in a DW SimpleGroup): `PaintAceTree` or stock | **`PaintAceTree`**, as LootHistory; release restores stock |
| D9 | `icons.borderColorFromSkin`: a hidden flag set by R3 with no row (the composer emits no color companion) | **Accept**, and clear it in the Border color row's write (`onChange`) so a pick takes effect. Otherwise ask M1 for a color companion on `BorderGroup` (folds into G14) |
| D10 | Chat output colors (E8) | **Leave all chat colors** (brand prefix, command yellow, ON/OFF). Chat is the client's frame, and BankLedger and LootHistory leave theirs |
| D11 | The tab strip: compose (label + underline) vs `S.Tab` | **Compose** (no backing today). `S.Tab` would add `tab.bg` and its gradient, a Ka0s Default change |
| D12 | G1-G15 is fifteen-odd tokens for one addon. The alternative is snapping DW's chrome grays (G4, G5, G6, G7, G10, G11, G12, G13) to the nearest existing token, with deltas ≤ 0.1 alpha or ≤ 0.08 per channel | **Tokens**, per O1 and skinning-§4 (LootHistory got the same at SkinDefs minor 6). The owner may prefer the snap for the chrome ones; the semantic ones (G1-G3, G8, G9, G15) should be tokens either way |

## 7. Re-vendor v1.77.0 → v1.79.0 obligations (DW-RV)

1. **Whole folder from the tag** (`git archive v1.79.0`), both payloads (`libs/LibKa0s/`, `tests/_kit/`). New files arrive
   with their shells: `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, the Skin
   major (`Skin.lua`, `SkinDefs.lua`, `SkinPaint*.lua`, `SkinEUI.lua`), `OptionsSkinPicker.lua`, `Toast.lua`; fonts
   (the five skin faces, Oxanium SemiBold/Bold + OFL) and textures (the two Glass, the eight bars).
2. **Retire the Toast-ahead deviation**, which the re-vendor makes obsolete (the tag now carries `Toast.lua`):
   - TOC: drop `libs\LibKa0s\Toast.lua` and its three comment lines (`DropWatcher.toc`, after `LibKa0s.xml`).
   - `tests/test_vendor_sync.lua:7-79`: drop the AHEAD exception and the branch-blob case. It is built to fail loudly
     ("the tag now carries Toast.lua: drop this exception…", `:41-42`).
   - `tests/loader.lua:19-28`: the TOC-read block that appends `libs\LibKa0s\*.lua` lines (harmless with no such line;
     remove it with the deviation).
   - `CLAUDE.md:47-49` ("Plus LibKa0s-Toast-1.0 …") and `docs/ARCHITECTURE.md:373` (the deviation row), plus the module
     map row's "Vendored alone for now" (`docs/ARCHITECTURE.md:36`) and `docs/known-limitations.md`'s mention.
   - `core/ToastSetup.lua:8-11` header comment ("vendored ALONE … on v1.77.0's Core it wears Core's SKIN").
3. **Options degradation stub** (`settings/OptionsSetup.lua:22-84`) gains `AppearanceTab` (answers nil: no tab, as
   `KeybindingsTab` does), `AppearanceRows`, `SkinPicker` and `HideSkinPicker`. `tests/test_surface_parity.lua:50`
   (`T.assertSurfaceParity(…Helpers, "LibKa0s-Options-1.0", …)`) is red until they exist.
4. **CLAUDE.md provenance**: `Bundles … v1.79.0` (`CLAUDE.md:44`). **Icons** (`CLAUDE.md:45`): add `eye` and
   `settings` (the picker's two buttons, `OptionsSkinPicker.lua:624-626`; DW has a test mode, so `onPreview` will be
   wired and the eye shows). Prune `media/icons/` with the tag's `tools/prune-icons.lua`; the README icon credits follow.
5. **TOC `## OptionalDeps`** gains `EllesmereUI` (skinning-§5). It is not a re-vendor item strictly, but it is owed at
   adoption (DW-01).
6. **Test pins**: no DW test pins a library minor or the payload's file list (only `test_vendor_sync` via the kit).
   Comments citing minors (`test_bindings.lua:211` OptionsKeybinds 3; `test_sim_panel.lua:195`,
   `test_sim_scenario.lua:270-621` v1.75.2/v1.76.0) are history, not pins. `tests/test_window_shell.lua:49` pins
   ApplySkin's gold title (`1,0.82,0`), which stays green under Ka0s Default. About 25 assertions read
   `C.TONE` / `C.GOLD` / `C.IDLE` or their literals (`grep -c` over `tests/*.lua`). They stay green only if the
   palette's Ka0s Default values are exact (the reason for §5).
7. **Ka0s Default looks different at the re-vendor once DW-01 registers the owner**: Oxanium body and title faces (the
   Toast shell already wears Core's skin), the Ka0s Default bar (DW draws no bar texture today). Its smoke checks re-look.
8. Sim / TestStrip re-look (v1.78.0 changelog: "DropWatcher (Sim and the strip)"): the scenarios and strips change
   only once the owner is registered (SimPanel minor 7, Widgets minor 16).

## 8. Risks

- **R1: the palette is read at paint time across ~15 files.** `C.TONE[...]` is indexed directly
  (`WindowGroup.lua:302,699,856`, `DetailCard.lua:80`, `OfferPanel.lua:67`, `Toast.lua:254`, `WindowHistory.lua:314`,
  `CompactGroup.lua:152,169`, `TipGrid.lua:117`, `TipMarks.lua:101,114,187,204`, `DetailCells.lua:137`,
  `DropsStrip.lua:179`, `WindowCells.lua:510`). The cleanest fix keeps the `C.TONE` shape and refills it from
  `S.Color` at registration and on `OnLooksChanged`, then repaints the window. A refill costs nothing per row. Calling
  `S.Color` per cell per repaint would add a function call to the countdown ticker (1 s) and the footer ticker (5 s):
  cheap, but the refill is free. Built-once strings (the `SEP` escape `CompactGroup.lua:97`, `TB.TEST_TONE`) must be
  rebuilt too.
- **R2: the Situations table's AceGUI widgets are acquired once a session and never released** (`PageEditors.lua:147-177`,
  cached in `ctx.dwSituations`). skinning-§2 repaints settings rows by re-rendering, which never reaches these. After
  a live skin switch they keep the old skin until `/reload`, unless DW releases and rebuilds the table on
  `OnLooksChanged` (or repaints them through `PaintAce` on that event). The placeholder's `OnRelease` (`:272`) must be
  chained through `Skin:OnRelease` if the placeholder is ever painted.
- **R3: pooled AceGUI widgets.** The page's own Button, EditBox and token Buttons (`PageEditors.lua:90,351,454`) go back
  to AceGUI's pool on every render. Each painted one needs `Skin:OnRelease` (restore) or another addon inherits DW's skin
  (anti-pattern #107).
- **R4: fonts set after the skin paints overwrite it.** `WR.SetFontSize` caches the face it first reads
  (`WindowRows.lua:83-90`, `fs.dwBaseFont`). If it caches before `S.Text` paints, a skin's face never shows; if after,
  a skin switch is undone by the next size change. `paintTradeWindow` calls `SetFontObject` on every repaint
  (`WindowGroup.lua:849`), which resets the face to the template's Friz. The size row needs the skin's face as its
  base, re-read on `OnLooksChanged`.
- **R5: glyph coverage.** The verdict glyphs ▲ ≈ ▼ need the mono face (`font.mono`). Ka0s Default's JetBrains Mono covers
  them; check every skin's `font.mono` before DW reads the token, or keep `C.FONT_MONO` fixed for glyph strings (they are
  symbols, not text).
- **R6: the R3 reset and the sentinel.** `Skin.ResetToSkin` writes `"@skin"` into a non-table non-bool key. Never list
  `icons.borderSize` (§3), or step 2's `RepairStoredSettings` and `/dw set` validation meet a string in a number row.
  The step must be a new `NS.MIGRATIONS` entry (`core/Database.lua:209-221`), idempotent and per profile.
- **R7: combat.** No secure or protected frame is skinned; the window is a plain `BackdropTemplate` frame and the keybind
  button is hidden. The Appearance tab and picker refuse in combat (the library's `__combatRefused`). The picker must be
  held to `PLAYER_REGEN_ENABLED` and must respect DW's `disabled` hold and perf suspend (LootHistory's
  `MaybeShowSkinPicker` pattern). DW's auto-open of the window in an instance is not a picker trigger.
- **R8: the shared popup menu** is repainted per opener (the library's job), so it needs the `owner` on `W.Dropdown`.
  An unowned dropdown resets it to Ka0s Default.
- **R9: file-cap pressure** (1500): `locales/enUS.lua` **1317**, `modules/WindowCells.lua` 1167, `modules/WindowGroup.lua`
  1118 (22 style calls to convert), `core/Compat.lua` 1051, `modules/LootFeed.lua` 1041. Converting WindowGroup adds
  little, but put palette plumbing in `core/SkinSetup.lua`, not in the module files, and route any new strings to
  `locales/enUS_Settings.lua` (340), not `enUS.lua`.
- **R10: Toast shell ordering.** The toast's frame is skinned by the shell at build (`Toast.lua:216`). DW's rows inside it
  (`modules/Toast.lua:253-322`) are DW's to repaint on `OnLooksChanged`. The toast lives off the main window, so it needs
  its own repaint hook.

## 9. Effort

**L.** There are about 20 surfaces and ~55 typed call sites in 17 files. The palette needs re-plumbing (R1), DW-03 needs a
migration step with a G14 dependency, and the re-vendor also retires the Toast-ahead deviation. About fifteen tokens wait
on M1, and ~25 test pins must stay green. Most of the chrome already goes through `ApplySkin` and the library
factories, and the tool surfaces are owner-aware for free, which keeps this short of XL.
