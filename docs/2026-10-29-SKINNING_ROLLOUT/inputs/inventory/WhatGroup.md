# Inventory: WhatGroup (prefix WG)

Read-only M0 inventory for items WG-RV and WG-01..WG-05 of `00_PLAN.md`. Repo
`/mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup`, branch `master`, clean, vendors LibKa0s v1.77.0
(`CLAUDE.md:48`, icons line `CLAUDE.md:49`: `close, copy, clear`). Read against `skinning.md` §1-§8,
anti-pattern #107, and LibKa0s v1.79.0 (`Skin.lua` VOCAB, `SkinDefs.lua` minor 14 schema and Ka0s Default,
`docs/api/Skin/version-6.14.10.4.8.1.3-docs.md`).

**Short version:** WhatGroup draws one window of its own, the group-info popup (`modules/Frame.lua`), plus one
host-acquired AceGUI button and the Profiles page's AceGUI container. It has **no HUD**, no test strip, and no
perf or sim panel. The debug console and every settings page are library-drawn and follow the owner once it is
registered. **No rung-2 gap.** Two hard-to-see risks: `modules/Frame.lua` is at **1472 of 1500 lines**, and
the secure teleport button's anchor is computed once from a label's rendered position. A live font change
leaves that anchor misaligned (Risks R1, R2).

---

## 1. Surfaces

All of these are built lazily inside `buildFrame()` (`modules/Frame.lua:769`) on the first `ShowFrame`,
never at load (taint reasons in that file's header). Every paint call therefore runs at first show, after
`core/SkinSetup.lua` has registered the owner at file load.

| # | Surface | Built at | Typed look today | Facade primitive(s), tokens (rung 1) |
|---|---|---|---|---|
| S1 | **Popup window** `WhatGroupFrame` (BackdropTemplate, MODAL strata, movable) | `modules/Frame.lua:772` | `NS.ApplySkin(f)` with **no owner** at `modules/Frame.lua:871`, i.e. Core.SKIN: bg 0.06,0.06,0.08,0.92, border 0,0,0,1, inner rule 0.24,0.24,0.27,0.85 | `NS.ApplySkin(f, nil, addonName)` (Core minor 13 hands it to `S.Shell`) **or** `S.Shell(f)` directly. Tokens: `win.bg`, `win.border`, `win.borderSize`, `win.borderStyle`, `win.inner`, `win.inset`, `win.radius`, `win.bgTop/bgBottom/bgTexture`, `title.bg` (Ka0s Default now fills a 30px top bar, 0.04,0.04,0.05,0.9), `title.height` (30, matches the host's 30px title bar), `title.text`, `divider`, `font.title`. Keep the bare bind `NS.ApplySkin = lib.ApplySkin` (`core/CoreSetup.lua:153`), because `tests/test_libka0s.lua:84,111` pin its identity; pass the owner at the call site. |
| S2 | **Title bar** (drag handle, plain frame, no art) | `modules/Frame.lua:837-855` | none (no fill) | Painted by `Shell`'s top bar (`title.bg`), so no extra call. `S.TitleBar` would be the alternative, but Shell already covers it. |
| S3 | **Title text** `f.title` (GameFontNormalLarge) | `modules/Frame.lua:857-860` | Inline `|cffFFD700` on "WhatGroup", then `|r — Group Info` in the color ApplySkin sets (Core.SKIN.title 1,0.82,0) | `Shell` colors `frame.title` with `title.text` and sets `font.title`. **Remove the inline `|cffFFD700` span** (it survives SetTextColor and would stay gold under every skin, #107). Doubtful call D1 covers the 0.843→0.82 green delta. |
| S4 | **Divider** under the title, `f.divider` (1px texture at -30) | `modules/Frame.lua:864-869` | colored by ApplySkin: 0.24,0.24,0.27,0.85 | `Shell` (via `frame.divider`), token `divider`. No literal at the site today; keep it that way. |
| S5 | **Field labels** x6 (Group/Instance/Type/Leader/Role/Playstyle), GameFontNormal | `MakeLabel`, `modules/Frame.lua:879-892` (text at :883) | inline `|cffFFD700` + GameFontNormal gold | Strip the inline code. Use `S.Font(label)` + `label:SetTextColor(S.Color("text.heading"))` in a reskin function on `S.OnLooksChanged` (keeps the body face; see D2), or `S.Text(label, "heading")` (title face). Token `text.heading`, `font.body`. |
| S6 | **Teleport label** `lblPort`, GameFontNormal | `modules/Frame.lua:907-912` | inline `|cffFFD700` (:909) | Same as S5. |
| S7 | **Field values** x6, GameFontHighlight (white) | `modules/Frame.lua:887-890`; set in `PopulateFields` `:1048-1093` | GameFontHighlight white; placeholders inline `|cff888888` at `:1051`, `:1056`, `:1057`, `:1081`, `:1090` ("No data", "—") | `S.Font(value)` + color `text.highlight` (Ka0s Default = WHITE, exact) through the same reskin hook. Build placeholders from a token, either with an `NS.SkinEscape(token)` helper like LootHistory's (`core/SkinSetup.lua`) or by `SetTextColor` per state. Placeholder token: `text.disabled` (D3). The reskin hook re-runs only the text fill, **never** `ConfigureTeleportButton` (R3). |
| S8 | **Teleport note** (GameFontHighlightSmall), cooldown or "not learned" line | `modules/Frame.lua:959-962`; text at `:610`, `:618` | inline `|cff888888` | `S.Font(note)` + `text.disabled` (D3), or `S.Text(note, "disabled")` after dropping the inline code. The 1s ticker re-sets the text (`:610`), so the color must come from `SetTextColor`, not a cached escape that a skin switch would leave stale. Otherwise use `SkinEscape` read on each tick. |
| S9 | **Close button** (UIPanelButtonTemplate, 90x24, "Close") | `modules/Frame.lua:969-976` | Blizzard red button art + GameFontNormal | `S.Button(closeBtn)`, tokens `btn.bg`, `btn.border`, `btn.borderSize`, `btn.borderStyle`, `btn.text`, `btn.hover`, `text.disabled`, `font.body`. Call it **after** `SetScript("OnClick")` (`:976`); the primitive HookScripts hover. Under Ka0s Default this replaces the red Blizzard art with the flat control (SkinPaint minor 6), which is D4. |
| S10 | **Teleport button** (SecureActionButtonTemplate, 24x24) + icon texture | `modules/Frame.lua:924-945` | spell icon via `icon:SetTexture(texID)` `:1025`, desaturated and alpha 0.5 when not ready `:1026-1027` | **Exception** (rung 3 secure frame / rung 4 spell icon). No border today. See D5 for an optional `S.IconBorder`. |
| S11 | **Cooldown swipe** (CooldownFrameTemplate) | `modules/Frame.lua:952-954` | Blizzard swipe | **Exception** (rung 3: engine-drawn Blizzard template). |
| S12 | **Teleport tooltip** | `modules/Frame.lua:543-549` (`GameTooltip:SetSpellByID`) | Blizzard spell tooltip; WG writes **no** lines | **Exception** (rung 3, GameTooltip frame; no addon-written lines to color). |
| S13 | **ESC proxy** `WhatGroupFrameEscape` | `modules/Frame.lua:756-767` | invisible, no regions | Nothing to paint. |
| S14 | **Toggle button** `WhatGroupTogglePopup` (hidden, keybinding target) | `modules/Frame.lua:1354-1363` | invisible | Nothing to paint. |
| S15 | **Settings: "Test notification" inline button**, host-acquired AceGUI `SimpleGroup` + `Button` | `settings/Panel.lua:41-74` (`AceGUI:Create` at `:47`, `:52`) | stock AceGUI | `Skin:PaintAce(addonName, btn)` (via an `NS.SkinPaintAce` seam like LootHistory's) right after `Create`. The SimpleGroup has no art. No host `OnRelease` is set, so no `Skin:OnRelease` chain is needed. Tokens: `btn.*`, `font.body`. |
| S16 | **Settings: Profiles page**, host-acquired AceGUI `SimpleGroup` container, filled by `AceConfigDialog:Open` with AceDBOptions widgets | `settings/Profiles.lua:64-72` | stock AceGUI | `Skin:PaintAceTree(addonName, container)` **after every** `AceConfigDialog:Open(APPNAME, container)` (`:72`), because Open releases and re-acquires the children on each render. The container is kept across renders, never released, so no OnRelease of the host's own exists. |
| S17 | **Settings pages**: landing page (logo, notes, slash rows), General (Master controls, Notifications, Keybindings tabs), headers, Defaults button, scrollbars, tab strip | library: `settings/Panel.lua:179` (`BuildLandingPage`), `:317-345`; descriptor `settings/OptionsSetup.lua:201-261` | library chrome | **Automatic** once the owner is registered: the page's skin owner is the descriptor's `addonName` (`settings/OptionsSetup.lua:209`, already the folder). WG-01 adds the **Appearance** host tab: `GENERAL_OPTS.tabs` (`settings/Panel.lua:317`) gains `Helpers.AppearanceTab(spec)` with `before` = the Keybindings tab's key. Result: Master controls, Notifications, Appearance, Keybindings (4 labels, under the budget). |
| S18 | **Debug console** + its copy window | descriptor `core/DebugLogSetup.lua:142-218`, `addonName = addonName` at `:155` | library palette; host passes `font = resolveConsoleFont(NS.FONT_MONO)` `:161` | **Automatic** (DebugLogWindow minor 1: owner = descriptor `addonName` once registered). No `skin` or `applySkin` is passed, so the library skins it. The host `font` stays JetBrains Mono under every skin, which is the library's contract and equals Ka0s Default's `font.mono`. |
| S19 | **Launcher**: minimap button (LibDBIcon), library hover tooltip, right-click menu (`MenuUtil.CreateContextMenu`) | `core/LauncherSetup.lua:109-` | library / Blizzard | Minimap button = third-party LibDBIcon, menu = Blizzard's context menu: **exception** (rung 3). The tooltip block is the library's; WG adds no lines (no `onTooltipShow`). |
| S20 | **Static popups** `WHATGROUP_RESET_ALL` (+ the reload popup WG-01 adds for leaving `eui`) | `settings/Schema.lua:673` | Blizzard StaticPopup | **Exception** (rung 3, skinning-§7). |
| S21 | **Chat output**: `[WG]` cyan prefix `core/WhatGroup.lua:66`, summary labels `GOLD = "FFD700"` `core/WhatGroup.lua:811` (used `:902`, `:910`), the green "[Click here…]" link `:918`, the spell-link fallback `|cff71d5ff` `:831`, the gray tag `|cff888888` `:845`, `|cffFFFF00` command hints (`settings/Slash.lua:152,323,455-458`, `locales/enUS.lua:136-139`), `|cff808080` test-mode refusal (`modules/Frame.lua:1148`) | — | chat escapes | **Out of scope** (chat frame is Blizzard's; not a skinning-§ surface). See D6. |
| S22 | **Degraded window fallback** (library absent) | `core/CoreSetup.lua:97-107` | literal WHITE8x8 backdrop, 0.06,0.06,0.08,0.92 / 0,0,0,1 | Stays: the library-absent path draws Ka0s Default through its own fallback (skinning-§3 "Degradation"). Not #107: no owner exists on that path. |

**Font note.** Every WG FontString uses a `GameFont*` object today (`docs/ARCHITECTURE.md:302` says so). Under
v1.79.0 Ka0s Default sets `font.body` = "Ka0s Oxanium SemiBold" and `font.title` = "Ka0s Oxanium Bold", so the
popup changes face at adoption with no host choice. That is the library's accepted "Ka0s Default looks
different" (CHANGELOG v1.79.0, consumer owes). Smoke checks re-look at it.

## 2. Library factories that take an owner

| Factory | Call site | Owner today | Action |
|---|---|---|---|
| `Core.ApplySkin(frame, skin, owner)` | `modules/Frame.lua:871` | **none** | Pass `addonName` as the third argument (or call `S.Shell`). |
| `Core.MakeCloseButton(parent, onClick, addonName)` | wrapped at `core/CoreSetup.lua:171-173` | `addonName` already | No production caller (the popup uses a text "Close" button). Already owner-aware; nothing to do. |
| `LibKa0s-DebugLog-1.0:New` | `core/DebugLogSetup.lua:142`, `addonName` at `:155` | already | Follows once registered. |
| `LibKa0s-Options-1.0:New` | `settings/OptionsSetup.lua:201`, `addonName` at `:209` | already | Follows once registered. WG-01 adds `AppearanceTab` and WG-04 adds `SkinPicker` / `HideSkinPicker`. |
| `LibKa0s-Launcher-1.0:New` | `core/LauncherSetup.lua:109` | n/a | Takes no skin owner (its menu is the client's). |
| Widgets (dropdown, search box, strip, copy window, autocomplete, drag handle, reorder, line chart) | none | — | WG calls none. |
| Perf panel / Sim panel | none | — | Perf is declined (`docs/ARCHITECTURE.md:327`). Sim is not adopted. |

## 3. HUD style settings

**No HUD.** The popup is a dialog window, not a HUD. The schema (`defaults/Profile.lua`) holds no bar texture,
border, HUD font or style color: `enabled`, `visibility`, `scale`, `alpha`, `locked`, `frame.{autoShow,width,height}`,
`notify.*`. Nothing for `S.Resolve` / `FROM_SKIN` / `fromSkin` companions, and no O2 reset step.
**WG-03 goes to `exceptions.tsv`** with proof:
`grep -nE 'texture|border|font|color' /mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup/defaults/Profile.lua` prints nothing.
`scale` and `alpha` are geometry and opacity, master controls (options-ui-§15), not style.

## 4. Exceptions

| What | Rung | Reason |
|---|---|---|
| Teleport `SecureActionButtonTemplate` button (`modules/Frame.lua:924`) and its spell icon (`:944`, `:1025-1027`) | 3 + 4 | A protected frame, plus game-meaning art (a spell icon; desaturation and alpha 0.5 mean "not ready"). |
| `CooldownFrameTemplate` swipe (`modules/Frame.lua:952`) | 3 | A Blizzard template, drawn by the engine. |
| `GameTooltip:SetSpellByID` (`modules/Frame.lua:544`) | 3 | GameTooltip's frame. WG writes no lines of its own. |
| `StaticPopup` `WHATGROUP_RESET_ALL` (`settings/Schema.lua:673`) and the WG-01 reload popup | 3 | skinning-§7. |
| Launcher right-click menu (`MenuUtil.CreateContextMenu`, library) and the LibDBIcon minimap button | 3 | Blizzard shared menu and a third-party button. |
| `SettingsPanel` chrome around the canvases | 3 | skinning-§7. |
| Settings landing-page logo `media/logos/whatgroup.logo.tga` (`settings/Panel.lua:96`) | 4 (brand art) | The brand mark, like the TOC IconTexture. Not a skin token. |
| Chat output colors (S21) | out of scope | Chat is not a skinned surface (D6). |
| **WG-03 (the HUD item)** | — | No HUD (section 3). |

## 5. Gaps (rung 2)

**None.** Every surface composes from existing primitives and tokens (`Shell`, `Button`, `Font`, `Text`,
`Color`, `PaintAce`, `PaintAceTree`). Two near-misses are resolved by tokens that already exist, at a sub-10/255
delta. They are recorded as doubtful calls, not gaps:

- `|cffFFD700` (1, 0.843, 0) on the title's brand span and the seven field labels. The nearest tokens are
  `title.text` and `text.heading`, both GOLD (1, 0.82, 0): a 6/255 green delta (D1).
- `|cff888888` (0.533 gray) on placeholders and the teleport note. The nearest tokens are `text.disabled`
  (0.5: 8/255), `icon.dim` (0.55), `sem.unknown` (0.6) and `text.muted` (0.7) (D3).

If the owner rules that neither delta is acceptable, the rung-2 fallback would be two tokens,
`text.label` = {1, 215/255, 0, 1} and `text.placeholder` = {136/255, 136/255, 136/255, 1}. Ka0s Default exact
values come from `modules/Frame.lua:859,883,909` and `:610,618,1051,1056,1057,1081,1090`. I do not recommend
this route: v1.79.0 already changes Ka0s Default's face to Oxanium, which dwarfs both deltas.

## 6. Doubtful calls (for DECISIONS.md)

- **D1, the FFD700 brand gold.** Drop the inline `|cffFFD700` from the title (`modules/Frame.lua:859`) and the
  labels (`:883`, `:909`), and take `title.text` / `text.heading` (1, 0.82, 0). **Recommend: accept the 6/255
  delta.** It is invisible next to the Oxanium face change. Keeping a literal is #107, and a new token for 6/255
  is token sprawl.
- **D2, the field-label role.** `S.Text(label, "heading")` gives the labels the title face (Oxanium Bold, scaled
  by `font.titleSize`). `S.Font(label)` plus `text.heading` keeps today's body-face, body-size label.
  **Recommend `S.Font` + `S.Color("text.heading")` in one reskin function**, because the values (S7) need the
  same hook anyway and the labels stay visually subordinate to the title.
- **D3, the 888888 placeholder gray.** **Recommend `text.disabled` (0.5)**, the role the library already uses
  for "no value" (LootHistory's `LedgerFormat` dash and its `(none)` text). The 8/255 delta is acceptable.
- **D4, the Close button under Ka0s Default.** `S.Button(closeBtn)` fades the Blizzard red UIPanelButton art
  and draws the flat control under Ka0s Default too (SkinPaint minor 6, owner ruling 2026-10-26: "Ka0s Default
  has a setting for everything"). `S.Button(closeBtn, true)` keeps the stock art and paints only the label.
  **Recommend the full `S.Button(closeBtn)`.** It is consistent with LootHistory, and the owner's ruling makes
  the flat button Ka0s Default's look. Note that it changes how the popup reads under Ka0s Default, so the plan's
  "stop if Ka0s Default's look changes" clause applies only if the owner treats this as new rather than as the
  leg-1 ruling.
- **D5, an icon edge on the secure teleport button.** `S.IconBorder(teleportBtn)` would add a 1px `icon.border`
  edge (black under Ka0s Default) that WG never drew, on a holder child of a protected frame. **Recommend: no
  edge.** List the button as a rung-3/4 exception. That keeps the secure frame free of new children and the
  look unchanged.
- **D6, chat colors.** The chat summary's FFD700 labels, the green link, the cyan `[WG]` prefix and the yellow
  command hints. **Recommend: leave them.** Chat is the client's frame, not a skinned surface (skinning-§
  intro lists none), and the prefix is the collection's brand convention. If the owner wants chat to follow, the
  summary labels would take `NS.SkinEscape("text.heading")`.
- **D7, the tab's name.** `00_PLAN.md` XX-01 says "the Skin tab on General", but skinning-§3 requires the label
  to be exactly **`Appearance`**, before Keybindings. **Recommend `Appearance`** (the standard wins; the plan's
  word is shorthand).
- **D8, where the skin rows live.** The `skin.*` keys are skip-render schema rows, but each row still carries a
  `group`. `tests/test_settings.lua:517-569` pins the General partition (`Master controls` 8, `Notifications`
  12) and the closed set of group names. **Recommend** a group `Appearance` for the rows, with the partition and
  known-groups tests updated in WG-01, or verify that skip-render rows are excluded from the partition walk.
  Either way, the test pin moves in the same commit.

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (WG-RV)

- **Payload**: copy `libs/LibKa0s/` and `tests/_kit/` whole from the run's tag via `git archive`. 12 new
  library files arrive (XML goes from 41 to 53 `<Script>`s): `Toast.lua`, `Skin.lua`, `SkinDefs.lua`,
  `SkinPaint.lua`, `SkinPaintExtras.lua`, `SkinPaintControls.lua`, `SkinEUI.lua`, `SkinAce.lua`,
  `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, `OptionsSkinPicker.lua`. The kit
  gains `mock_paint.lua`. Media gains the skin faces (Oxanium SemiBold/Bold plus the five leg-1 faces, with OFL
  texts), the Glass textures and the eight generated bars.
- **`tests/loader.lua:23-91` LIBKA0S list**: the hand-kept XML-order list must gain all 12 files in XML order
  (Toast after Glow; Skin, SkinDefs, SkinPaint, SkinPaintExtras, SkinPaintControls, SkinEUI, SkinAce after
  MediaIcons; WidgetsCopyWindow after WidgetsAutocomplete; DebugLogWindow after DebugLogGates;
  OptionsAppearance, OptionsSkinPicker after OptionsKeybinds). Otherwise the XML-order check fails and the
  Skin major never loads in tests.
- **Options degradation stub** (`settings/OptionsSetup.lua:52-181`): add `H.AppearanceTab` (answers nil, no tab
  entry), `H.AppearanceRows`, `H.SkinPicker` and `H.HideSkinPicker` as inert members. `Kit.assertSurfaceParity`
  in `tests/test_surface_parity.lua` is red until they exist. `APPEARANCE_STRINGS` is lib-level data, so it
  stays live-only like `MASTER_GROUP`.
- **Provenance**: `CLAUDE.md:48` becomes `v1.79.0` (or the run's tag), in the same commit as the bytes
  (`tests/test_vendor_sync.lua` reads it).
- **Icons line** `CLAUDE.md:49`: add **`eye, settings`** (the picker's two buttons, v1.79.0 consumer owes), making
  `close, copy, clear, eye, settings`. Then prune with the tag's `tools/prune-icons.lua`. Add it at WG-RV if the
  picker is certain (WG-04), or at WG-04 with a re-prune. Recommend WG-RV, so one prune covers both.
- **README icon/font credits**: the README credits only JetBrains Mono (`README.md:102-103`). Oxanium and the
  skin faces arrive in the payload and are drawn once WG adopts, so WG-05 adds their OFL credits.
- **Test pins that should hold**: `tests/test_libka0s.lua:40-71` pins majors and per-file `MODULES` for Core,
  DebugLog, Slash, Options (`Options`, `OptionsWidgets`, `OptionsScroll`) and Perf. These are names only, no
  minors, so they stay green. The Core `STRINGS` / `d.L` tripwires (`:1001-1021`) are checked against v1.79.0:
  `Core.lua` has neither and Options files read no `d.L`, so they stay green. `NO_LIBKA0S` (`:541-549`) skips
  `Core.lua`, which makes every other major refuse, so no update is needed.
- **TOC** (WG-01, not RV): `## OptionalDeps` (`WhatGroup.toc:8`) gains `EllesmereUI` (skinning-§5), and
  `core\SkinSetup.lua` gets a load-order annotation per toc-file-§5 (after `core\MediaSetup.lua` and before
  `core\DebugLogSetup.lua` and `modules\Frame.lua`).
- **Mock**: the suite's own `tests/wow_mock.lua` (an extender over `mock_base`) has `CreateFont` (`:545`) and
  `HookScript` (`:304`). For WG-02's assertions (popup painted `win.bg`, repainted on a switch), install
  `tests/_kit/mock_paint.lua` in the frame cases (opt-in, revision 43/44).

## 8. Risks

- **R1, the file cap.** `modules/Frame.lua` is **1472/1500** lines. WG-02's paint calls, reskin hook and
  comments will not fit. Plan an extraction first: move the popup's look into `modules/FrameSkin.lua` (paint and
  the OnLooksChanged recolor), or move the keybinding/toggle-button block (`:1324-1380`) out. `core/WhatGroup.lua`
  is 1340 (headroom 160), and `core/SkinSetup.lua` is new.
- **R2, the secure anchor and live font changes.** `teleportBtn`'s TOPLEFT is computed once from `lblPort`'s
  rendered position (`modules/Frame.lua:921-926`), and the rows are stacked label-to-label (`:900-906`). A skin
  with a larger `font.bodySize`/face (High Contrast 13.5/15, Vollkorn 13) moves the labels after a live
  `SetChoice`, while the secure button keeps its old offset and drifts off its label. Its `SetPoint` is protected,
  so it is refused in combat. **Fix**: on `S.OnLooksChanged`, out of combat, recompute the offset and re-anchor
  the button. In combat, defer to `PLAYER_REGEN_ENABLED` the way `ApplyFrameSize` does. Or give rows fixed heights
  so the anchor is font-invariant. A test should pin it.
- **R3, combat and the reskin hook.** `PopulateFields` ends in `ConfigureTeleportButton` (protected
  `SetAttribute` and `Show`). The OnLooksChanged recolor must touch only FontString colors and fonts, never call
  `PopulateFields` whole. `SetChoice` can arrive in combat through `/wg set skin.skin …` (the CLI is not
  combat-locked like the panel).
- **R4, paint on a frame that parents a secure child.** `Shell` sets a backdrop and creates an edge holder at
  level +10 as a child of `f`. `f` is protected by ancestry, so do the first paint inside `buildFrame` (out of
  combat on every path that builds, since test mode is refused in combat). A later repaint touches only
  colors and regions. Smoke-check a skin switch with the popup open in combat (no `ADDON_ACTION_BLOCKED`). The
  holder must not take the mouse over the teleport button (a plain frame does not by default).
- **R5, label truncation.** Labels are fixed at `LABEL_WIDTH = 72` with word-wrap off (`:26`, `:882-885`).
  "Playstyle:" at 13.5pt in a wider face may clip. Check it in the per-skin smoke.
- **R6, soft hide.** The combat soft hide is `f:SetAlpha(0)` (`ApplyFrameAlpha`, `:183-186`). Shell's holders are
  children, so they inherit the alpha. No primitive should `SetAlpha(1)` on `f` itself (`P.subTex` resets region
  alpha only). Verify that a repaint during a soft hide does not bring the popup back.
- **R7, pooled AceGUI.** S15 and S16 go through `Skin:PaintAce` / `PaintAceTree`, which restore on `OnRelease`.
  WG sets no `OnRelease` of its own, so nothing needs `Skin:OnRelease`. Do not paint the Profiles container's
  `frame` directly.
- **R8, taint at load.** `core/SkinSetup.lua` runs `RegisterOwner` at file load. The library creates no frames
  until a primitive is called, and WG's first paint is in the lazy `buildFrame`. The first-run picker (WG-04)
  must also stay off the boot path. Show it on a timer after `PLAYER_LOGIN` (LootHistory uses `NS.After(2, …)`),
  never inside a GameMenu or settings `OnShow` chain (`docs/midnight-quirks.md`). It must be hidden by the
  stand-down (`NS.FrameStandDown`).
- **R9, docs drift.** `docs/ARCHITECTURE.md:302-303` states a "Blizzard-default-only baseline" and that "every
  other FontString uses a GameFont* object". Both become false at adoption, so WG-05 rewrites them.
- **Perf**: no hot path. The one repeating thing is the 1s cooldown ticker (`modules/Frame.lua:634`), which only
  sets text. Reading a token per tick is a table lookup. Nothing else is skinned per frame.

## 9. Effort

**M.** There are few surfaces (one popup, one AceGUI button, one AceGUI container) and no HUD, no gap and no
migration. But the 1472-line file needs an extraction first, the secure-button anchor needs a combat-safe
re-anchor on a font change, and the re-vendor brings 12 loader entries, four stub members and the picker.
