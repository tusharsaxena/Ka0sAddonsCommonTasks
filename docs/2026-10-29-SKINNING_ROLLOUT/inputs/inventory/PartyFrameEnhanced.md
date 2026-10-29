# Inventory: PartyFrameEnhanced (prefix PF)

Read-only inventory for the skinning rollout (`00_PLAN.md`, items PF-RV, PF-01..PF-05), taken 2026-10-29
from `../PartyFrameEnhanced`. Inventory time state: the checkout is on `feat/2026-10-29-skinning-rollout`
with a clean tree and nothing past master. It vendors LibKa0s v1.77.0, and `CLAUDE.md` has
`LibKa0s icons: clear, close, copy.`. The library was read at v1.79.0: Skin minor 6, SkinDefs minor 14,
SkinPaintExtras minor 4, Options key 34.4.35.4.6.10.3.12.8.3.2.5.3.1.

**What the addon is, visually.** Most of PFE is a **HUD**: one cast bar, one target frame and one pet frame
per party unit (five units). They are built by one shared drawing module (`modules/Element.lua`) and styled
entirely from per-feature profile settings composed with `O.BarGroup` / `O.BorderGroup` / `O.FontGroup`.
It also draws a stand-in party frame for preview and three free-placement drag holders. It has **no
standalone window of its own**. The debug console and perf panel are the library's, and the settings
pages are the library's Options panel plus one AceConfigDialog Profiles page.

---

## 1. Surfaces

Legend: **Lib** = drawn by the library; registering the owner is enough, because the descriptor already
carries `addonName`. **Host** = the addon's own code paints it.

### 1a. HUD elements: cast bars, target frames, pet frames (Host)

All three features call `Element.Build` (`modules/Element.lua:26-71`) and are restyled by `Element.Reskin`
(`:198-217`) and `Element.ApplyColors` (`:224-232`).

| Element part | Built | What it types today | Rung-1 paint |
|---|---|---|---|
| Status bar fill texture | `Element.lua:35` | `bar:SetStatusBarTexture(NS.FetchMedia("statusbar", cfg.barTexture, C.FALLBACK_TEXTURE))`, `Element.lua:99-100`. Default `"Blizzard"` (`defaults/Profile.lua:50,84,117`); fallback `Interface\TargetingFrame\UI-StatusBar` (`core/Constants.lua:11`) | `S.Resolve("bar.texture", cfg.barTexture, cfg.barTextureFromSkin)`, then `NS.FetchMedia` as today. Token **`bar.texture`**. Do not use `S.BarTexture`; see Risks R4. |
| Background (same texture, tinted) | `Element.lua:37` | `el.bg:SetTexture(texture)` at `:103`, and `el.bg:SetVertexColor(resolve(cfg.bgColor, cfg.useClassColorBg))` at `:225`. bgColor default `{0,0,0,0.6}` | Texture: the same resolved `bar.texture`. Color: the player's stored swatch, unchanged (player data with a class companion, not a call-site literal). `bar.bg` (nil in Ka0s Default) is not used; see D3. |
| Border (BackdropTemplate frame, child of the bar) | `Element.lua:40` | `SetBackdrop({ edgeFile = NS.FetchMedia("border", cfg.borderStyle, C.FALLBACK_BORDER), edgeSize = cfg.borderSize })` at `:145-146`; `SetBackdropBorderColor(resolve(cfg.borderColor, ...))` at `:227`. Defaults: borderShow false, style `"Blizzard Tooltip"`, size 8, color black (`Profile.lua:59-60` and equivalents) | Style: `S.Resolve("bar.borderStyle", cfg.borderStyle, cfg.borderStyleFromSkin)`. Token **`bar.borderStyle`** (Ka0s Default `"None"`; see D2). Size and color stay the player's. |
| Text lines `text` / `text2` (on the mouse-off overlay frame) | `Element.lua:46,49` | `fs:SetFont(font, size, flags)` at `:150` with `font = NS.FetchMedia("font", cfg.font, C.FALLBACK_FONT)` at `:161`, size `cfg.fontSize * scale`, flags `cfg.fontFlags`; `SetShadowOffset(1,-1)` + **`SetShadowColor(0,0,0,1)` literal** at `:152-153`; `SetTextColor(resolve(cfg.fontColor, ...))` at `:230-231`. Defaults: Friz Quadrata TT, 11/10/9, OUTLINE, no shadow, white | Face: `S.Resolve("hud.font", cfg.font, cfg.fontFromSkin)`. Token **`hud.font`**. Size, flags, shadow and color stay the player's. Not `S.Text`, which would override the player's size and color. The shadow literal: see D5. |
| Cast icon (cast bars only) | `Element.lua:52-53` | `SetTexCoord(0.07,0.93,0.07,0.93)`; spell texture at `CastBars.lua:169,294` | Spell icon: rung 4. Optional icon edge: `S.IconBorder(iconHolder)`, token **`icon.border`** (nil in Ka0s Default, so no change). It needs a small icon holder frame, because IconBorder takes a frame and the icon is a Texture; see D4. |
| Spark | `Element.lua:56-58` | `Interface\CastingBar\UI-CastingBar-Spark`, ADD blend (`:16`) | Exception, rung 4 (client cast-bar art). |
| Shield | `Element.lua:61-62` | `Interface\CastingBar\UI-CastingBar-Small-Shield` (`:19`; deliberately Blizzard's, per the comment at `:17-18`) | Exception, rung 4 (means "cannot be interrupted"). |
| Raid marker | `Element.lua:65-66` | `Interface\TargetingFrame\UI-RaidTargetingIcons` (`:20`) | Exception, rung 4 (game icon). |
| Cast fill colors | `CastBars.lua:105-127` (applyFill), `:186-189` (failed hold) | `SetStatusBarColor` from stored `barColor`, `channelColor`, `empowerColor`, `uninterruptibleColor`, `failedColor` (`Profile.lua:51-55`), times barAlpha; class color via `NS.ResolveColor` | Exception, rung 4: cast-state meaning colors, player-set. No token. |
| Target bar colors | `TargetFrames.lua:55-71`, preview `:96-99` | stored `barColor` / `hostileColor` / `neutralColor` / `friendlyColor` (`Profile.lua:85-90`); class via `Element.ClassResolver` (`Element.lua:247-259`, `RAID_CLASS_COLORS`) | Exception, rung 4: reaction and class colors. |
| Pet bar colors | `PetFrames.lua:42-43,52-53` | stored `barColor` `{0.35,0.70,0.35}` (`Profile.lua:118`), class via `NS.ResolveColor` | Exception, rung 4: health and class (player-set). |
| Text content | `CastBars.lua:167-168,191-192,292-293`; `UnitButtons.lua` (RenderName/Health/Preview) | `SetText` only, no color | Nothing (the color is the Element's). |

The roots are a plain `Frame` per cast bar (`CastBars.lua:371`) and a **`SecureUnitButtonTemplate`** button
per target and pet frame (`UnitButtons.lua:33-34`). Those buttons are the reason the restyle must stay inside
`NS.RunSecure` (`TargetFrames.lua:270-277`). See Risks R1.

### 1b. Free-placement drag holders (Host)

There are three, one per feature (`modules/Anchor.lua:265-306`), shown only while unlocked and in free
placement.

| Part | Built | Types today | Paint |
|---|---|---|---|
| Plate | `Anchor.lua:269-272` | **`SetColorTexture(0, 0.6, 1, 0.25)`** literal | **Gap PF-G1** (no token holds a move-handle wash; see §5) |
| Caption label | `Anchor.lua:273-276` | `GameFontNormalSmall` (gold 1, 0.82, 0; Friz 10) | `S.Text(holder.label, "accent")`, token `text.accent` (gold in Ka0s Default). The face becomes the skin body (Oxanium on Ka0s Default, by v1.79.0's design). |
| Grip | `Anchor.lua:284-290` | invisible mouse frame | Nothing. |

### 1c. Preview stand-in party frame (Host, proposed exception)

This is `modules/StandIn.lua:153-175` (built) with three looks at `:91-142`, which **imitate a foreign frame
system** (EllesmereUI or Blizzard raid / party): bg `SetColorTexture(0.06,0.06,0.06,0.9)` at `:95`, a 1px
`WHITE8X8` edge `SetBackdropBorderColor(0,0,0,1)` at `:96-97`, `Raid-Bar-Hp-Fill/Bg` at `:32-33,108,112`,
bg `(0,0,0,0.5)` at `:121`, a green `(0,0.8,0)` health bar at `:129`, a power color at `:69-76`, class
color at `:62-67`, `GameFontHighlightSmall` name at `:172`, and the `|cff999999(test)|r` mark at `:29,247`.
**It stays untouched** (§4, E-PF-3). Its job is to look like the party frame it stands in for, so that
offsets tuned against it match a real party.

### 1d. Settings surfaces

| Surface | Where | Paint |
|---|---|---|
| Options panel: General, Cast Bars, Target Frames, Pet Frames, About landing | `settings/OptionsSetup.lua:40-98` (descriptor `addonName = addonName`, `:45`), pages via `H.CreatePanel` / `RenderTabbedSchema` | **Lib**: the page owner is the descriptor's `addonName` once registered. Nothing else to do. |
| Composer rows (BarGroup / BorderGroup / FontGroup / ColorPair) | `settings/ElementRows.lua:90-136` | **Lib**, plus `fromSkin = true` on the three group composers (§3). |
| Profiles page: a self-acquired AceGUI `SimpleGroup` filled by AceConfigDialog | `settings/Profiles.lua:36-46` | **Host**: `Skin:PaintAceTree(owner, container)` after `AceConfigDialog:Open`, as LootHistory does (`LootHistory/settings/Profiles.lua:68-69`). The container is kept and never released, so a host `OnRelease` is not needed. |
| Appearance tab (new) | General page: `settings/General.lua:277-280` | `O.AppearanceTab(spec)` passed as a host tab in `RenderTabbedSchema`'s 5th argument (`opts.tabs`). It goes **last**, since General has no Keybindings tab (skinning-§3). The tab budget is fine: 2 group tabs + 1. |
| First-run skin picker (new) | `O.SkinPicker` from a new `core/SkinSetup.lua` | **Lib**. The eye is `onPreview`, the host's preview (unlock); see D6. |
| Reset-all confirmation | `settings/General.lua:247-262` (`StaticPopupDialogs`) | Exception, rung 3 (StaticPopup). |

### 1e. Tool surfaces (Lib, owner-aware already)

| Surface | Descriptor | Status |
|---|---|---|
| Debug console + its copy window | `core/DebugLogSetup.lua:92-140` (`name` and `addonName = addonName`) | No `applySkin`, `skin` or `makeCloseButton` hook, so the library paints it for the registered owner. Nothing to change beyond registering. The font is `C.FONT_MONO` (`:102`): the mono face JetBrains Mono equals Ka0s Default's `font.mono`. |
| Perf panel | `core/PerfSetup.lua:25-34` (`name`, `addonName`) | As above. Nothing to change. |
| Close button seam | `core/CoreSetup.lua:117-119`: `lib.MakeCloseButton(parent, onClick, addonName)` | Already passes the owner. It has no caller. |
| `NS.SKIN` / `NS.ApplySkin` | `core/CoreSetup.lua:107-108` (`NS.ApplySkin = lib.ApplySkin`, no owner bound); stub at `:52-54` | It has no caller. Once adopted, a bare `ApplySkin` publication is an invitation to #107 ("Core.ApplySkin called with no owner"). Either bind the owner (`function(f) return lib.ApplySkin(f, addonName) end`, after checking the Core signature) or delete both and their stub; the delete is recommended (D8). |
| Minimap/broker launcher tooltip | `core/LauncherSetup.lua:46-102` | Lines drawn by `LibKa0s-Launcher-1.0` on GameTooltip. The library takes no owner there, so there is nothing to do (GameTooltip frame: rung 3). |
| Sim panel, test strip, copy windows of its own, toasts | none | PFE has none. |

### 1f. Chat lines (not a skin surface)

`NS.PREFIX = "|cff00ffff[PFE]|r"` (`core/Namespace.lua:9`), `|cff40ff40ON|r` / `|cffff4040OFF|r`
(`core/DebugLogSetup.lua:47`), `|cff808080` refusals (`modules/Preview.lua:43-46`) and `|cFFFFFF00`
(`settings/Slash.lua:397`). These go to the Blizzard chat frame; see D7.

---

## 2. Library factories that take an owner

| Call | File:line | Owner today | Action |
|---|---|---|---|
| `LibKa0s-Options-1.0` `lib:New(descriptor)` | `settings/OptionsSetup.lua:173` | `addonName` (`:45`) | None. It becomes live when `RegisterOwner(addonName)` runs. |
| `LibKa0s-DebugLog-1.0` `lib:New` | `core/DebugLogSetup.lua:92` | `addonName` (`:97`) | None. |
| `LibKa0s-Perf-1.0` `lib:New` | `core/PerfSetup.lua:25` | `addonName` (`:29`) | None. |
| `Core.MakeCloseButton` | `core/CoreSetup.lua:118` | `addonName` | None (no caller). |
| `Core.ApplySkin` | `core/CoreSetup.lua:108` (published unbound) | **none** | Bind or delete (D8). |
| `O.AppearanceTab`, `O.AppearanceRows`, `O.SkinPicker`, `O.HideSkinPicker` | new | (spec `owner`) | Pass `owner = addonName`. |
| `Skin:PaintAceTree` | new, `settings/Profiles.lua` | (arg) | `addonName`. |
| Widgets factories (dropdown, search box, copy window, test strip, autocomplete, drag handle, reorder list, line chart), `Toast` | none called | n/a | n/a |

`Skin:RegisterOwner("PartyFrameEnhanced", { get, set, label = "Ka0s Party Frame Enhanced" })` goes at file load
in a new `core/SkinSetup.lua`, placed after `core/CoreSetup.lua` and before `core/DebugLogSetup.lua`,
`core/PerfSetup.lua` and every module. The TOC comments and `tests/test_loadorder.lua` must be updated.

---

## 3. HUD style settings (the one-time R3 reset, ruling O2)

Each of the three feature sections (`castbar`, `target`, `pet`) carries the same three skin-governable keys.
The composer's `fromSkin = true` (OptionsCompose C12) appends the companion bool. The host draws through
`S.Resolve(token, pick, companion)`.

| Schema key (×3 sections) | Default today | Companion added by `fromSkin` | Token (Ka0s Default value) | Host read |
|---|---|---|---|---|
| `<sec>.barTexture` | `"Blizzard"` (`Profile.lua:50,84,117`) | `<sec>.barTextureFromSkin` (BarGroup, `ElementRows.lua:117-126`) | `bar.texture` = `"Ka0s Default"` | `Element.lua:99` applyBar |
| `<sec>.font` | `"Friz Quadrata TT"` (`:63,96,124`) | `<sec>.fontFromSkin` (FontGroup, `ElementRows.lua:103-113`) | `hud.font` = `"Ka0s Oxanium SemiBold"` | `Element.lua:161` applyFonts |
| `<sec>.borderStyle` | `"Blizzard Tooltip"` (`:59,93,121`) | `<sec>.borderStyleFromSkin` (BorderGroup, `ElementRows.lua:90-99`) | `bar.borderStyle` = `"None"` | `Element.lua:145` applyBorder |

The sections are `castbar` (`Profile.lua:35`), `target` (`:75`) and `pet` (`:106`), giving 9 companion keys
in all.

**HUD style settings that do not follow the skin**, because the composer gives them no companion. They stay
the player's:

- `barAlpha`
- `bgColor`
- `borderShow`
- `borderSize`: default 8; the token `bar.borderSize` is 1.
- `borderColor`
- `fontSize`: 11 / 10 / 9; the token `hud.fontSize` is 12.
- `fontFlags`: OUTLINE, which equals `hud.outline`.
- `fontShadow`
- `fontColor`

**How to implement the reset:**

- Set the companions' **profile default to `true`**, so new and untouched profiles follow the skin.
- Add **one `profile`-scope migration step** to `core/Database.lua`'s ladder: `NS.SCHEMA_VERSION` goes 1 → 2,
  as `{ to = 2, scope = "profile", apply = ... }`. It sets the nine companions to `true` on each stored
  profile.
- Write the companions **directly**, creating the section table if it is absent, or call
  `Skin.ResetToSkin(p, keys)` only after the table and companion exist. **Do not** hand `ResetToSkin` the
  picker paths on a raw stored profile; see Risks R3.
- The stored picks are left alone, so a player who turns a companion off gets their old pick back.

---

## 4. Exceptions

| Id | Rung | What | Reason |
|---|---|---|---|
| E-PF-1 | 4 | Cast fill palette: `barColor`, `channelColor`, `empowerColor`, `uninterruptibleColor`, `failedColor` (`CastBars.lua:105-127,186-189`) | Cast-state meaning, player-set and stored; read against the default UI's cast bars. |
| E-PF-2 | 4 | Target reaction colors (`hostile/neutral/friendlyColor`), target and pet `barColor`, every *Use class color* companion (`RAID_CLASS_COLORS` via `Element.ClassResolver` / `NS.ResolveColor`) | Reaction, health and class colors. |
| E-PF-3 | 3 | The preview stand-in party frame (`modules/StandIn.lua` whole), including its `(test)` gray mark | An imitation of Blizzard's or EllesmereUI's party frame (protected, foreign frames skinning-§7 never touches). Skinning it would make offsets tuned against it wrong for a real party. |
| E-PF-4 | 4 | Spark, shield and raid-marker art (`Element.lua:16-20,56-67`), spell icons (`CastBars.lua:169,294`), `FALLBACK_ICON` / `PREVIEW_ICON` file ids | Game art with meaning (uninterruptible, raid target, spell). |
| E-PF-5 | 3 | `StaticPopupDialogs["PARTYFRAMEENHANCED_RESET_ALL"]` (`settings/General.lua:247`) | StaticPopup is a Blizzard shared frame. |
| E-PF-6 | 3 | The Blizzard and EllesmereUI party frames the elements attach to (`modules/Providers.lua`, `modules/SecureFollow.lua` wraps, `modules/RangeFade.lua` reads) | Protected Blizzard and foreign frames; only PFE's own overlays skin (00_PLAN rung 3). |
| E-PF-7 | 3 | Launcher tooltip / GameTooltip frame (`core/LauncherSetup.lua`) | GameTooltip frame; the lines are the library's. |
| E-PF-8 | — | Chat lines' color escapes (§1f) | The Blizzard chat frame is not a skin surface, and the `[PFE]` prefix color is slash-commands'. See D7. |
| E-PF-9 | — | Fallback media constants `C.FALLBACK_TEXTURE/BORDER/FONT` (`core/Constants.lua:11-13`) | The last-rung fallback when LSM cannot resolve a key, not a style choice. |

There is no PF-03 "no HUD" exception: PF-03 has work.

---

## 5. Gaps (rung 2)

### PF-G1: a move-handle (drag-plate) wash token

- **Component.** The free-placement holder's plate, shown while unlocked (`modules/Anchor.lua:269-272`).
- **Why no primitive or token fits.**
  - It is a translucent fill marking "this is where you grab and drag".
  - The candidates do not match:
    - `strip.sim` is `{0.35,0.8,1,0.12}`, a sim meaning color.
    - `strip.test` is amber, a meaning color.
    - `cover.dim` is black.
    - `handle.bg` is `{0,0,0,0.75}` and `handle.edge` is gold; they belong to the library drag handle, a different look.
    - `nav.selBg` is `{0.3,0.5,1,1}`, opaque.
    - `list.hover` is gold.
  - Every one of them would change Ka0s Default's pixels.
  - `S.Strip` / `S.Cover` paint those meaning tokens.
- **Proposed.** Token `mover.bg` (color) in the Lists-and-cards or Overlays group, painted by the host
  through `S.Color("mover.bg")` on `SetColorTexture`. A primitive is not needed: the host keeps the texture
  and re-tints it on `OnLooksChanged`. Alternatively, a primitive option `S.Cover(target, { mover = true })`.
  The token is preferred.
- **Ka0s Default must reproduce** `{ 0, 0.6, 1, 0.25 }` (`modules/Anchor.lua:271`).
- **Other skins.** Each skin's accent at about 0.25 alpha. The `eui` fallback is EllesmereUI's accent at 0.25.
- **Recurrence.** Not confirmed in the other addons by this inventory: a grep for the literal found only PFE.
  The consolidation should check the other HUD addons' unlock overlays (KickCD, MultiMeters, AbsorbTracker,
  DropWatcher, QuickComms, ConsumableMaster, AuraMaster). If only PFE has one, D1's alternative applies.

No other gap was found. Every other HUD and settings surface composes from `bar.texture`, `hud.font`,
`bar.borderStyle`, `icon.border`, `text.accent` and the library-owned surfaces.

---

## 6. Doubtful calls (for DECISIONS.md)

**D1. PF-G1 vs. exception.**

- If no other addon has a drag plate, a one-addon token is thin.
- Recommendation: add `mover.bg` anyway, because every movable HUD in the collection needs an unlock
  affordance, and the token documents it.
- Fallback: list the plate as a rung-4-style exception, because blue reads as Edit Mode's selection.

**D2. Resetting `borderStyleFromSkin` changes nothing visible today, but can remove a player's border.**

- Ka0s Default's `bar.borderStyle` is `"None"`. A player with `borderShow = true` and a chosen style would
  see the border vanish after the reset, because Show border governs but the style resolves to None. Mixing
  a skin's style with the player's `borderSize` (default 8) can also look wrong under skins with a flat 1px
  style.
- Recommendation: in the migration, set `borderStyleFromSkin = true` only on sections whose stored
  `borderShow` is not `true`. Players who deliberately show a border keep it.
- This is a deliberate narrowing of O2; the owner may overrule.

**D3. Background color and `bar.bg`.**

- `bgColor` is a player swatch with a class companion, and the composer has no `fromSkin` companion for
  `ColorPair`. Ka0s Default `bar.bg` is nil.
- Recommendation: leave `bgColor` as player data; do not route it through `bar.bg`.

**D4. A cast icon border via `S.IconBorder`.** It needs a new holder frame around `el.icon` (castbars only).
In Ka0s Default it is invisible. Recommendation: add it (castbars are insecure frames), so other skins' icon
edges reach the HUD. Low priority, and it may be skipped with a note.

**D5. The text shadow literal `SetShadowColor(0,0,0,1)` (`Element.lua:153`).**

- It applies only when the player turns `fontShadow` on. It is the client's stock shadow, and the library's
  `P.font` uses the same 1, -1 black.
- Recommendation: keep it, with a comment citing that it is the client shadow and not a chrome color.
- If the reviewer reads #107 strictly, the fallback is to note it in `exceptions` as stock client behavior.

**D6. The picker's eye (`onPreview`).**

- PFE has no test mode. Unlocking is its preview (`settings/General.lua:101-105`), and it is refused in
  combat and while stood down.
- Recommendation: `onPreview = function() NS.SetByPath("locked", false) end` through the write seam, so the
  player sees the stand-in and placeholder elements. This leaves the addon unlocked until the player locks
  it again; the Lock row and `/pfe lock` remain.
- Alternative: omit `onPreview` (the eye is hidden).

**D7. Chat-line color escapes (§1f).**

- Recommendation: an exception. The chat frame is Blizzard's, and the `[PFE]` prefix color is fixed by
  slash-commands.
- If the owner wants them skinned, `|cff808080` would need a token-to-escape helper (LootHistory's
  `NS.SkinEscape`), and no exact token exists for `0x80` gray.

**D8. `NS.SKIN` / `NS.ApplySkin`** (`core/CoreSetup.lua:52-54,107-108`) are published with no caller and no
owner bound. Recommendation: delete them and their stub entries in PF-02 (`tests/test_surface_parity.lua`'s
Core stub check must agree), rather than bind an owner to dead code.

**D9. `EllesmereUIDB` read in `modules/Providers.lua:315`.**

- This sizes the stand-in. It is not the skin gate.
- After adoption, anti-pattern #107 lists "an `EllesmereUIDB` read in the addon's own code". skinning-§5
  lets a read under a ratified register row stand until it moves onto the provider, and the provider offers
  no party-size API.
- Recommendation: keep the read and its `library-stack-§6` register row (`docs/ARCHITECTURE.md:463`). Add a
  line to that row citing skinning-§5's carve-out, so the audit does not flag it.

**D10. The companion default `true` for new profiles.** Recommendation: `true`, matching O2. Every player,
new or old, sees the skin. A `false` default would make new profiles keep Blizzard and Friz, which O2 does
not want.

**D11. Ka0s Default changes PFE's look at adoption.** After the reset, cast, target and pet bars switch from
the `Blizzard` bar and Friz Quadrata to the `Ka0s Default` bar and Oxanium SemiBold. This is v1.79.0's stated
consumer consequence, and the owner ruled it in O2. 00_PLAN says "stop to ask only if a change would alter
Ka0s Default's look today". Recommendation: proceed and record it in the smoke checks. This is not a stop,
because the owner already ruled it in O2 and v1.79.0.

---

## 7. Re-vendor obligations, v1.77.0 → v1.79.0 (PF-RV)

1. **Copy the whole folder** from the run's library tag with `git archive`: `libs/LibKa0s/` and
   `tests/_kit/`. New files arrive with their shells:
   - v1.78.0: `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, plus
     the Skin major's files (`Skin.lua`, `SkinDefs.lua`, `SkinPaint*.lua`, `SkinEUI.lua`).
   - v1.79.0: `Toast.lua`, `OptionsSkinPicker.lua`.
   - The new fonts and textures under `media/`.
   - `tests/run.lua` and `tests/test_loadorder.lua` read the library list from `LibKa0s.xml`, so neither
     needs a list update.
2. **Extend the Options degradation stub** (`settings/OptionsSetup.lua:138-148`) with
   **`AppearanceTab`, `AppearanceRows`** (v1.78.0) and **`SkinPicker`, `HideSkinPicker`** (v1.79.0). Without
   them, `Kit.assertSurfaceParity` in `tests/test_surface_parity.lua:97-114` goes red. The stub must stay
   load-completing: `AppearanceTab` is called at render in the live arm only, so a no-op returning nil is
   enough.
3. **Roll the provenance line** in `CLAUDE.md`: `Bundles [LibKa0s](...) v1.77.0 (MIT).` becomes the run's tag.
   `tests/test_vendor_sync.lua` holds the payload to that tag.
4. **Change the icons line** in `CLAUDE.md` from `LibKa0s icons: clear, close, copy.` to add **`eye`** and
   **`settings`**, which the picker draws. Then prune `media/icons/` with the tag's
   `tools/prune-icons.lua`, and keep the README icon credits in step.
5. **Version pins:** `settings/OptionsSetup.lua:152,154` comments name v1.77.0 (comments only).
   `docs/smoke-tests.md` names v1.77.0. No test pins a library minor or a file list by hand.
6. **Look change at re-vendor.** Nothing visible, while PFE registers no owner. After PF-01 registers one, the
   Ka0s Default Oxanium and bar changes apply (D11).
7. **`## OptionalDeps`** already lists `EllesmereUI` (`PartyFrameEnhanced.toc:8`), as skinning-§5 requires.
8. **Test kit revision 44** comes with the payload. `mock_paint.lua` is opt-in, for the new skin tests.

---

## 8. Risks

**R1. Secure buttons and combat.** Target and pet roots are `SecureUnitButtonTemplate`.

- `Element.Reskin` sets size and anchors on them, which is why `reskinAll` runs inside
  `NS.RunSecure("target:reskin")` (`TargetFrames.lua:270-277`; PetFrames likewise).
- A skin change (`OnLooksChanged`) or a profile switch in combat must re-enter the same path, for example by
  publishing `CONFIG("master")` or a new `MSG.SKIN` that each feature handles through its existing reskin.
  It must never call `Reskin` directly.
- **Do not hand secure buttons to a facade primitive** (`S.IconBorder`, `S.Text`, and so on). The library's
  repaint runs outside `RunSecure`, and a holder child created on a protected frame is avoidable.

**R2. The structure-signature memo.** `Element.lua:178-186` skips the structural restyle unless a listed
config field changed, and the file warns "IF YOU ADD A CONFIG READ ... ADD THE FIELD HERE".

- The three companions and the **resolved** media keys (or a skin generation counter) must enter the
  signature.
- Otherwise a skin switch, a texture or font override, or a companion toggle draws nothing until another
  field moves.
- `tests/perf.lua`'s `settingsDrag` scenario guards the memo's purpose.

**R3. `Skin.ResetToSkin` on raw stored profiles.**

- AceDB's raw `profiles` lack defaulted keys. For a path like `castbar.barTexture` whose companion is not
  stored, `ResetToSkin` writes the **`@skin` sentinel into the LSM key** (`Skin.lua:657-663`).
- If it is handed the companion path itself and the companion is not stored, it writes the sentinel into
  the bool.
- The migration must set the companions to `true` directly; see §3.
- A missing section table is skipped, which is correct when the companion's default is `true`.

**R4. `S.BarTexture` records the frame.** Using it on the bars would make every skin repaint overwrite the
player's own texture pick whenever the companion is off. Use `S.Resolve` plus PFE's own reskin path for all
three keys.

**R5. Pooled AceGUI.** The Profiles page container is acquired once and never released, and its
AceConfigDialog children are re-acquired on every `Open`. Paint with `PaintAceTree` after each `Open`, as
LootHistory does. Nothing else here acquires AceGUI widgets itself.

**R6. Hot paths.** These are untouched:

- the cast `OnUpdate` (`castTick`)
- the target ticker (`targetTick`)
- cast events

Skin reads happen only in `Element.Reskin`'s structural half (config, profile or skin change). Do not put
`S.Resolve` or `S.Color` inside `applyFill`, `paintColors` or the ticker.

**R7. Settings layout tests.**

- `tests/test_settings_layout.lua:239-243` pins General's tabs to exactly Master controls and All elements,
  derived from row groups. The `skin.*` rows must be skip-render (no `group`) or the test must exclude them;
  the Appearance host tab must be checked separately.
- `:260+` pins the feature pages' Bar and Text tab rows, which gain the `*FromSkin` rows.
- `tests/test_schema.lua`, `tests/test_optionssetup.lua` (the stub row delta) and
  `tests/test_profile_switch.lua` (a profile change re-applies the choice) all need cases.

**R8. File cap.** There is no pressure. The largest authored files are `settings/Slash.lua` (523 lines),
`modules/CastBars.lua` (427) and `modules/Anchor.lua` (434). The tests top out at `tests/test_slash.lua`
(611). A new `core/SkinSetup.lua` (LootHistory's is about 600 lines) stays well under 1500.

**R9. Taint.** No facade primitive is ever pointed at a Blizzard or EllesmereUI party frame. The stand-in
stays untouched (E-PF-3). The `SecureFollow` wraps are not skin-related.

---

## 9. Effort

**M.** The work is all small and well bounded:

- One HUD drawing module (`Element.lua`) restyles all three features. Three composer calls gain
  `fromSkin`, plus one migration step and one skin seam file.
- The tool surfaces and settings chrome are already owner-aware.
- The remaining host surfaces are three drag plates (one gap token) and the Profiles page tree.

The risk is concentrated in R1 to R3: the secure restyle path, the signature memo and the migration.
