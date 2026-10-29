# 01 Inventory: what the fourteen addons need (M0, 2026-10-29)

Fourteen read-only inventories (`inputs/inventory/<Addon>.md`) and one skeptic per addon that tried to refute every claimed gap by composing it from the existing primitives (`inputs/m0-results.json` holds both, verbatim).

| Addon | HUD | Surfaces | HUD style keys | Exceptions | Gaps claimed / survived | Doubtful calls | Effort |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | yes | 19 | 12 | 8 | 0 / 0 | 10 | L |
| AuraMaster | yes | 34 | 7 | 13 | 9 / 8 | 12 | L |
| BankLedger | no | 40 | 0 | 12 | 2 / 1 | 11 | L |
| ConsumableMaster | yes | 40 | 13 | 11 | 5 / 3 | 14 | L |
| DpsRace | yes | 66 | 10 | 17 | 5 / 4 | 20 | L |
| DropWatcher | yes | 58 | 5 | 11 | 15 / 12 | 12 | L |
| KickCD | yes | 42 | 8 | 9 | 0 / 0 | 12 | L |
| MultiMeters | yes | 30 | 24 | 9 | 4 / 4 | 16 | XL |
| PanelMaster | yes | 20 | 0 | 10 | 1 / 0 | 8 | M |
| PartyFrameEnhanced | yes | 13 | 9 | 7 | 1 / 1 | 11 | M |
| PremadeGroupsFilterExtension | no | 32 | 0 | 8 | 3 / 0 | 11 | L |
| PrettyChat | no | 28 | 0 | 9 | 2 / 2 | 8 | M |
| QuickComms | yes | 58 | 30 | 10 | 4 / 4 | 11 | L |
| WhatGroup | no | 22 | 0 | 8 | 0 / 0 | 8 | M |

**51 gaps claimed, 39 survived the skeptics.** Almost all of the survivors are one kind: a color Ka0s Default draws today whose exact value no token holds (a gray at 0.533 against text.muted's 0.7, DropWatcher's verdict tones, DPS Race's ahead and caution hues). Each would otherwise be a library schema token every skin must carry. They are met by one mechanism, owner tokens (LK-01), and the few structural gaps by four more items.

## The gaps and where each is met

| Gap | Verdict | Component | Met by |
|---|---|---|---|
| AM-G1 | real | AuraMasterDropdown AceGUI widget type (every dropdown row + 6 hand-built) | LK-03 |
| AM-G2 | real | Drag strip label, attached-container name gray | LK-01 |
| AM-G3 | refuted | Unlocked placement outline | rung 1: At outline creation, and again in an S.OnLooksChanged repaint: local r,g,b,a = S.Color('chart.crosshair'); NS.Style.DrawEdge(o, 1, r, g, b, a). OUTLINE_ALPHA is… |
| AM-G4 | real | Drag-to-attach snap / detach marks (box, dots, line) | LK-01 |
| AM-G5 | real | Frame picker outline | LK-01 |
| AM-G6 | real | Container page plan-warning lines | LK-01 |
| AM-G7 | real | Settings grays: container picker suffix and Filters '(info)' | LK-01 |
| AM-G8 | real | Secondary gold (growth note, player's own category marker) | LK-01 |
| AM-G9 | real | Filters 'See spells' in-panel link | LK-01 |
| BL-G1 | real | Gold-movement color: Item and Quality cells of a gold row, gold row tooltip title, session-window copy, search | LK-01 |
| BL-G2 | refuted | Insights legend swatch's GameTooltip line | rung 1: In the legend swatch's OnEnter (InsightsWidgets.lua:819), read the token at hover time and pass it to the existing helper: W.CursorTooltip(self, self._tip, {S.C… |
| CM-G1 | real | KCMIconButton hover swatch (priority-row up/down/delete) | LK-01 |
| CM-G2 | real | Warning text on the settings pages (no spec, empty list, no sub-categories, no categories) | LK-01 |
| CM-G3 | real | Two grays CM writes into GameTooltip lines (score explain tooltip) | LK-01 |
| CM-G4 | refuted | Disabled icon tint on CM's custom AceGUI icon widgets | rung 1: Delete the unreachable disabled branch. If it stays, tint the art from S.Color('text.disabled'), which is {0.5,0.5,0.5} on Ka0s Default, keeping AceGUI's stock … |
| CM-G5 | refuted | Follow-the-skin companion row for swatch rows (R3 reset of HUD colors) | rung 1: For each swatch: O.ColorPair{ key=K, ..., extra = {{ type='bool', path=<prefix>..K..'FromSkin', label='Use the skin's color', tooltip='Draw this in the skin's c… |
| DR-G1 | real | Opaque modal shell (ability timeline, gear view) | LK-02 |
| DR-G2 | real | Danger button (Cancel race, Delete run) | LK-02 |
| DR-G3 | real | Caution callout box (waiting hint, target-card badge, detail flags box) | LK-02 + LK-01 |
| DR-G4 | real | DPS Race semantic hues (ahead/gain, caution, info) | LK-01 |
| DR-G5 | refuted | FontGroup fromSkin companion for the monospace race clocks | rung 1: Call O.FontGroup for the two clock blocks without fromSkin, or with omit = { fontFromSkin = true }. Add the companion yourself through spec.extra: { path = '<pr… |
| DW-G1 | real | Verdict and action-state tones (drop tables, cards, toast, tooltip marks) | LK-01 |
| DW-G2 | refuted | Trade window ending soon (countdown text, 3px bar, warning chip) | rung 1: Text: `local r,g,b = S.Color("strip.test"); fs:SetTextColor(r,g,b)`, rgb only, the way LootHistory's NS.SkinColor drops the alpha. Bar (flat, per D5): `bar:SetC… |
| DW-G3 | real | Detail card Stats row: a stat gained | LK-01 |
| DW-G4 | real | Tables' plain text (default of every setTone) | LK-01 |
| DW-G5 | real | Idle gray: idle tab label, footer, side titles, Offer column heads, compact separator, tooltip hints | LK-01 |
| DW-G6 | real | Expanded (selected) row/card wash | LK-01 |
| DW-G7 | real | Drop row expand chevron | LK-01 |
| DW-G8 | refuted | SIMULATION word beside the title | rung 1: `local r,g,b = S.Color("strip.sim"); simWord:SetTextColor(r,g,b)`, rgb only, so the text is opaque, as NS.SkinColor does. Repaint on OnLooksChanged next to the … |
| DW-G9 | real | Restriction badge (lock icon + text) | LK-01 |
| DW-G10 | real | Flat text button (TB.TextButton, every DW action button) | LK-02 + LK-01 |
| DW-G11 | refuted | Trade window countdown bar track | rung 1: `f.barBg:SetColorTexture(S.Color("list.boxEdge"))`, all four components, repainted on OnLooksChanged. Ka0s Default draws 1,1,1,0.12, identical to WindowGroup.lu… |
| DW-G12 | real | Drops/History bottom strip top rule | LK-01 |
| DW-G13 | real | Detail card boxes, chips and the editor's text box | LK-02 + LK-01 |
| DW-G14 | real | Item icon border following the skin (Window › Icons BorderGroup fromSkin, R3 reset) | LK-04 |
| DW-G15 | real | Tooltip row label and bullet | LK-01 |
| MM-G1 | real | Meter row mouseover wash | LK-01 |
| MM-G2 | real | Meter row alternating stripe | LK-01 |
| MM-G3 | real | Tooltip hint / overflow lines | LK-01 |
| MM-G4 | real | Dim text in the meter window (session-line 'restricted' notes, notice reason line) | LK-01 |
| PM-G1 | refuted | Inline emphasis (/cffffff00.../r) inside GameTooltip bodies the Panels editor writes | rung 1: Keep the /cffffff00.../r escapes as they are (rung 4: content markup, the collection's command/path highlight). This is the same convention lib.FormatRow and La… |
| PF-G1 | real | Free-placement drag holder plate (unlock affordance), one per feature | LK-01 |
| PG-G1 | refuted | The attached filter panel (frame, header art, min/max, 8 check buttons, labels, readout, 3 edit boxes, 4 dropd | rung 1: Use two instances from the existing builder (modules/Panel.lua buildFrame, :778-800, which already builds the whole panel from BUILDERS). (1) The STOCK instance… |
| PG-G2 | refuted | PG-06's fourth EllesmereUI gate condition: Premade Groups Filter's own EllesmereUI skin loaded and on (missing | rung 1: Under 'eui' the panel's skinned instance is painted by the same S.* calls, which Skin.lua's __euiRoute sends to EllesmereUI's facade. The gate and the Appearanc… |
| PG-G3 | refuted | The 8 check buttons under the eui source | rung 1: Call S.Checkbox(cb, { borderInset = 4 }) once for every source. Under the Ka0s skins the Ka0s Checkbox honors borderInset. Under eui, SkinEUI's strip drops it a… |
| PC-G1 | real | AceGUI TreeGroup (string list pane + editor content pane, row buttons, selected row, tree scrollbar) on the Ca | LK-03 |
| PC-G2 | real | Gray note text: settings-page caption, footnote, landing alias row, preview error, and the gray lines PC write | LK-01 |
| QC-G1 | real | Pad button and dial wedge state veils (dim for a refused bake, cooling for the spam guard) | LK-01 |
| QC-G2 | real | Pad button hover wash, and the default of the dial's slice highlight | LK-01 |
| QC-G3 | real | Icon browser selected grid cell | LK-01 |
| QC-G4 | real | Callout popup and icon browser window chrome (SettingsFrameTemplate NineSlice, Bg, ClosePanelButton) | LK-05 |

## M1 items (rung 2)

| Id | Repo | What | Gaps |
|---|---|---|---|
| LK-01 | LibKa0s | **Owner tokens.** `Skin:RegisterOwner(owner, { tokens = { ["<ns>.<name>"] = { default = <Ka0s Default value>, follow = "<library token>", skins = { <skin> = <value>, ... } } } })`. An owner token's name carries the owner's own namespace (never a schema name); `S.Color` / `S.Token` and every primitive opt that names a token resolve it. Ka0s Default answers `default` (today's pixels), a skin answers its `skins` entry, else the `follow` token's value in that skin, so every skin gets a value of its own; the eui source answers the follow token's eui value. Tests: resolution per skin, an unknown or colliding name refused and logged, repaint on a skin switch. | 30 color gaps |
| LK-02 | LibKa0s | **Token remap on box and button primitives.** `opts.tokens = { bg = , border = , text = , hover = , ... }` on `Shell`, `Panel`, `Card`, `Inset` and `Button`, naming library or owner tokens for a slot instead of the primitive's fixed spec (a danger button, a caution callout, an opaque modal, an alternate card fill). Token NAMES, never values, so #107 holds. | DR-G1, DR-G2, DR-G3, DW-G10, DW-G13 |
| LK-03 | LibKa0s | **SkinAce coverage.** `Skin:AliasAceType(hostType, baseType)` so a custom AceGUI widget type (AuraMasterDropdown) is painted, restored on OnRelease and kept durable by its base type's painter; a `TreeGroup` painter (tree pane, row buttons, selection, border, the content pane), restored on OnRelease. | AM-G1, PC-G1 |
| LK-04 | LibKa0s | **Icon borders follow the skin.** Tokens `icon.borderStyle` and `icon.borderSize` (Ka0s Default: today's Solid 2px black), and the composer's `BorderGroup{ fromSkin = "icon" }` reading that family. | DW-G14 |
| LK-05 | LibKa0s | **Stock under Ka0s Default.** `opts.stockDefault` on `Shell`, `TitleBar`, `CloseButton` and the controls a template-built window carries, so a window that deliberately matches Blizzard's settings window keeps its stock art under Ka0s Default and is skinned under every other skin and eui (the mechanism `Slider` already has). | QC-G4 |
| ST-01 | LibKa0sSkinTester | Showroom samples for LK-01..05 (an owner token, a danger button, a callout, a TreeGroup, an icon border, a stock-under-Default window), re-vendored from the branch head. | — |
| LK-90 | LibKa0s | Release v1.80.0: CHANGELOG with "What a consumer owes", `docs/api/`, version suite, clean-tree release run, **local** tag. | — |
| WS-01 | WowAddonStandards | skinning-§1: an addon's own colors are owner tokens with a follow (never typed values); the rollout in open-evolutions. | — |
