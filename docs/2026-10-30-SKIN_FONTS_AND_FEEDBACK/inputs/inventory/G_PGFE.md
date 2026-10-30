# G_PGFE: PremadeGroupsFilterExtension expand/collapse button (item 8)

Inputs: OWNER_FEEDBACK.md item 8, screenshots image-33, 34, 48, 49, 50, 51. Read-only inventory. PGFE and
LibKa0s are both on `feat/2026-10-30-skin-library-followups` (PGFE `a02c946`, LibKa0s `aefeba9`, v1.81.0
vendored).

## 1. Which skin is in each screenshot

| Image | State | Skin (identified from) |
|---|---|---|
| 33, 34 | expanded / collapsed | **EllesmereUI source (`eui`)**: flat black shell, the stock gold check art (EUI `Checkbox`), and the button is EUI's flat block with a white text glyph (EUI's `PageButton` fallback, see section 2). Not a Ka0s skin. |
| 48, 49 | collapsed / expanded | **Ember**: charred brown, accent `#FF7A33`, Bitter face (`SkinDefs.lua:804-812`) |
| 50, 51 | expanded / collapsed | **WoW Forever**: warm charcoal, white title, tan accent `FV_TAN` (`SkinDefs.lua:967-974`) |

In 48-51 the arrow is the library's texture, which is correct. Only the placement is wrong there. The
text "up"/"down" appears only under EllesmereUI.

## 2. Current behavior and root causes

### 2a. "up" / "down" text (image-33/34): a LibKa0s bug in the EllesmereUI route

- PGFE paints the two template buttons with the direction words
  (`PremadeGroupsFilterExtension/modules/Panel.lua:783-787`):
  `S.PageButton(mm.MinimizeButton, "up")` and `S.PageButton(mm.MaximizeButton, "down")`.
- Under a Ka0s skin, `prim.PageButton` (`LibKa0s/LibKa0s/SkinPaintControls.lua:611-627`) draws
  `Interface\ChatFrame\ChatFrameExpandArrow`, turned by `PAGE_ROTATION[dir]` (`:604`), 12x12, tinted
  `icon.arrow` through `P.glyph`. This is correct.
- Under `eui`, `PageButton` is one of EllesmereUI's native names (`SkinEUI.lua:84-87`). `euiCall`
  (`SkinEUI.lua:265-280`) forwards the call **verbatim** to EllesmereUI's facade, apart from stripping
  options. EllesmereUI's signature is different: `S.PageButton(button, "<" or ">")`
  (`Interface/AddOns/EllesmereUI/SKINNING_API.md:103`). Its implementation,
  `EllesmereUIBlizzardSkin_WindowEngine.lua:827-873` (EllesmereUI 9.6.9), maps only `"<"` and `">"` to
  arrow PNGs. Any other value is drawn as a font string, `fs:SetText(ch)`, in white at 14px. So `"up"`
  and `"down"` are rendered literally.
- **Root cause:** SkinEUI does not translate the Ka0s direction vocabulary into EllesmereUI's
  character, and EllesmereUI has no up or down arrow at all. EllesmereUI's facade cannot draw any
  vertical PageButton correctly. PGFE is the only caller of `S.PageButton` in the collection (grep over
  every repo), so no other addon shows the bug today.
- No test catches it. `LibKa0s/tests/test_skin_eui.lua` has no PageButton case, and PGFE's
  `tests/test_panel.lua:628-636` only asserts the recorded argument `"up"`/`"down"`.

### 2b. Misalignment against the title band (all skins): PGFE anchoring

- `buildMinMax` (`Panel.lua:700-708`) creates `MaximizeMinimizeButtonFrameTemplate` and anchors it
  `RIGHT` to the **hidden** template `CloseButton`'s `RIGHT` (`:703`). It never sets a size. The
  button therefore takes the Blizzard template's geometry: the close button's default anchors at the
  frame's top-right corner, and the template's own button size.
- The skin's title band is drawn by `S.Shell` at `inset` from the frame edges, `title.height` tall
  (`SkinPaint.lua:879-896` `band`, `:914` height, `:974` `inset = flat ? win.borderSize : 1`). The button
  ignores both values.
- Measured from the screenshots (6x crops): the box is about 26-28px, top-flush with the frame (it sits
  over the window edge), overhangs the right edge by about 1-2px, and is not vertically centered on the
  30px band. Ember's box bottom sits about 6px above the band's lower rule (image-48). Forever's sits on
  the window's own 1px edge (image-50/51). Under EllesmereUI the shell bar is 25px
  (`EUI_SHELL_HEADER_H`, `:656`), so the box overhangs the bar's bottom (image-33).
- The offset reads differently in each skin because the window edge differs while the button stays in
  place. The `winBorder` edges in `SkinDefs.lua` are: Obsidian, Azeroth, Ember and Forever 1px flat;
  High Contrast and Midnight 2px flat; Glass an 8px nine-slice (`:707`); WoW Default a 32px Blizzard
  Dialog nine-slice (`:862`). With a nine-slice border, `inset` is 1, yet the art is far thicker, so the
  button lands on the border art.
- Related constants that assume the old geometry: `HEADER_CLICK_H = 24` (`:659`, the band is 30) and
  `HEADER_CLICK_RT = 30` (`:713`, room for the arrow).
- Template sizes and the close-button anchor offsets are from memory of Blizzard's
  SharedUIPanelTemplates and are **not verified** (no FrameXML copy on disk). The measurements above
  are what counts.

## 3. Proposed change

### 3a. LibKa0s (owner of the bug in 2a)

**`LibKa0s/SkinEUI.lua`, minor 2 to 3.** In `euiCall` (`:265`), special-case `PageButton`:

```lua
local EUI_PAGE = { prev = "<", left = "<", next = ">", right = ">" }
-- in euiCall, before the facade call:
if name == "PageButton" then
  local dir, popts = ...
  local ch = EUI_PAGE[dir]
  if not ch or (type(popts) == "table" and popts.icon) then        -- up/down, or a caller's icon
    return lib.prim.PageButton(owner, target, ...)                  -- library technique, EUI tokens
  end
  trackEUI(owner, target, name, ...)  -- then pcall(fn, target, ch)
end
```

- A vertical arrow takes the library's technique, colored from EllesmereUI's derived tokens (the same
  fallback as `remapped`). Prev and next reach EllesmereUI as the character it understands.
- `giveBack` (`:335-352`) unpaints records with native names and replays them through `__euiRoute`.
  Because the replay goes through the same `euiCall`, the fallback covers it. A test must confirm this.
- Optional, for the lead (Q3): add `"icon.arrow"` to `ACCENT_TOKENS` (`:104`). Without it the arrow under
  EllesmereUI is Ka0s Default's gold, not the EllesmereUI accent.

**`LibKa0s/SkinPaintControls.lua`, minor 10 to 11.** Give `PageButton` the option the owner asked for:
an icon texture.

- `opts.icon`: a texture path that the **caller** resolves, typically `Media.Icon(addon, "chevron-up")`.
  When it is set, the primitive uses that path, sets no rotation and no desaturation (Open Iconic art is
  white by contract, `Media.lua:82-86`), and tints it `icon.arrow` with `P.tint`. The header's "draws no
  Media icon" promise stays true, because the library never resolves an icon the consumer may have
  pruned.
- `opts.size`: the arrow's size, defaulting to 12.
- Both are replayed on repaint, like `stock`, `noBg` and `noBorder`.
- Without `opts.icon`, the in-client arrow is unchanged.
- Docs: `docs/api/` adds a SkinPaintControls 11 / SkinEUI 3 row; `CONSUMERS.md` already lists PageButton
  opts (`:75`).

**LibKa0s tests:**

- `tests/test_skin_eui.lua`, new case "eui: a vertical PageButton takes the library's arrow; prev and
  next reach EllesmereUI as < and >". The fixture facade (`tests/fixture_skin_eui.lua`) records calls.
  Assert:
  - no facade `PageButton` call carries `"up"`;
  - `painted[btn].regions.arrow` exists and is shown;
  - `prev` reaches the facade as `"<"`;
  - after `__EnterEUI` (the giveBack-and-replay path), an `"up"` button still has the library arrow.
- `tests/test_skin_paint_controls.lua` near `:543`: `opts.icon` sets the given texture, rotation 0, not
  desaturated, vertex color = `icon.arrow`, and `opts.size` sets the size. A repaint after a skin switch
  keeps the icon and retints it.
- `tests/test_skin_stock_default.lua:185`: extend the forward-and-replay case with `icon` and `size`.

### 3b. PremadeGroupsFilterExtension (owner of the bug in 2b)

**`modules/Panel.lua`:**

1. **A fixed button size.** Add `local ARROW_BTN = 20` and `ARROW_PAD = 4` (the lead may tune them). In
   `buildMinMax` (`:700`), drop the anchor on `CloseButton`. Call `mm:SetSize(ARROW_BTN, ARROW_BTN)`, and
   for each of `mm.MinimizeButton` and `mm.MaximizeButton` call `ClearAllPoints`,
   `SetPoint("CENTER", mm)` and `SetSize(ARROW_BTN, ARROW_BTN)`. Same size in every skin.
2. **Place the button on the band.** Add a new `local function titleBand()` that returns `top, height`:
   - EllesmereUI painting (`NS.SkinEUIPainted()`): `0, EUI_SHELL_HEADER_H`;
   - otherwise the visible edge (`win.borderSize` when `win.borderStyle == "flat"`, else 1, matching
     `SkinPaint.lua:974`) and `title.height` (fallback `HEADER_H`).

   Then add `local function placeMinMax(f)`:

   ```lua
   local top, h = titleBand()
   mm:ClearAllPoints()
   mm:SetPoint("TOPRIGHT", f, "TOPRIGHT", -(top + ARROW_PAD), -(top + (h - ARROW_BTN) / 2))
   ```

   Call it from `applyLayout` (`:680`), which every skin switch already reaches through
   `onLooksChanged` and `Refresh`, so it follows a live pick. `collapsedHeight` (`:674`) can reuse
   `titleBand`. Fold the inset in as well if the lead wants the collapsed height to cover the whole band
   (Q4).
3. **Keep the click band in step.** `buildHeaderClick` (`:715`) sizes its height from `h`, and its right
   gap is `ARROW_BTN + ARROW_PAD + top`. Re-set both in `placeMinMax`. Check that `TITLE_INSET` (`:736`)
   still clears the button, since 20 + 4 + 2 is at least 24.
4. **The icon.** In `paint` (`:783-787`):

   ```lua
   S.PageButton(mm.MinimizeButton, "up",   { icon = NS.Icon("chevron-up"),   size = 12 })
   S.PageButton(mm.MaximizeButton, "down", { icon = NS.Icon("chevron-down"), size = 12 })
   ```

   `NS.Icon` is `core/MediaSetup.lua:14`, and a nil path falls back to the in-client arrow. Add
   `chevron-up, chevron-down` to `CLAUDE.md:53`'s `LibKa0s icons:` line, then re-vendor or prune
   `libs/LibKa0s/media/icons/` with the tag's `tools/prune-icons.lua`, and update the README's icon
   credits if needed.

**PGFE tests:**

- `tests/test_panel.lua:628-636`: also assert `calls.PageButton[2].icon` is the chevron path for each
  button.
- New `tests/test_skin.lua` case, "the min/max button is the same size and centered on the title band in
  every skin". Loop over every registered skin key (`NS.ApplySkinChoice("ka0s", key)`) and assert:
  - `mm.__width == mm.__height == ARROW_BTN`, and both buttons the same;
  - `mm:GetPoint()` is `TOPRIGHT` at x `-(inset + 4)` and y `-(inset + (title.height - 20) / 2)`, from
    `Skin:Token(OWNER, ...)`.

  It goes red under the old `CloseButton` anchor.
- New `tests/test_skin_eui.lua` case: with EllesmereUI painting, the facade records no `PageButton` with
  `"up"` or `"down"`, the button carries the library arrow, and it is centered on the 25px bar.
- `tests/test_layers.lua:75` already covers the min/max frame level. Check that it still passes after
  the re-anchor.
- `tests/wow_mock.lua:332`: the template buttons may need `SetSize` and `GetPoint`. The stub frame
  already records `__points` and `__width` (`:200-217`).

## 4. Risks

- **Blizzard template internals.** `MaximizeMinimizeButtonFrameTemplate` buttons may carry their own
  anchors and atlas sizes, and `SetMinimizedLook`/`SetMaximizedLook` may re-show art that the skin
  faded. `syncMinMax` (`:665`) calls these on every layout, so this needs an in-client check (smoke).
- **Nine-slice skins (Glass, WoW Default).** `win.borderSize` is 8 or 32 and not flat, so `inset` is 1
  and the button can still sit on the border art. The lead must choose an inset rule (Q2).
- **Mixed arrows under EllesmereUI.** EllesmereUI keeps its own look for every other control, so the
  library arrow inside EUI's block is a mixed look. There is no EUI up/down arrow to use instead.
- **Release coupling.** This is a LibKa0s minor bump (SkinEUI 3, SkinPaintControls 11) while v1.81.0 is
  still unmerged and awaiting smoke. Folding it into v1.81.0 means re-cutting the local tag again.
  Re-vendoring costs nothing collection-wide, because PGFE is the only PageButton caller.
- **Icon prune.** Adding icons to the declaration changes `libs/LibKa0s/media/icons/`, and
  `test_vendor_sync` and the prune tool must agree.

## 5. Open questions for the lead

1. **Icon source.** Use the Open Iconic `chevron-up`/`chevron-down` through `opts.icon` (white art, exact
   token color), or keep the rotated `ChatFrameExpandArrow`? **Recommendation: chevrons.** The owner
   asked for a texture from the set, the art is crisper, and it gets the exact tint instead of
   desaturated yellow. The alternatives `collapse-up`/`collapse-down` or `caret-*` exist, but there is no
   vertical caret.
2. **Inset for nine-slice skins.** **Recommendation:** use the band's own inset (`SkinPaint.lua:974`)
   for every skin, and add `ARROW_PAD`. Then the button sits inside the band wherever the band is drawn.
   If WoW Default's dialog border still overlaps it in-client, add a per-skin pad. Do not invent a token
   for it now.
3. **The arrow color under EllesmereUI.** Add `icon.arrow` to SkinEUI's `ACCENT_TOKENS`, so the arrow is
   the EUI accent rather than Ka0s gold? **Recommendation: yes.** It matches how `check.mark` and
   `tab.onLine` already follow the EllesmereUI accent.
4. **Button size and collapsed height.** **Recommendation:** a 20px box with a 12px arrow in every
   skin. Leave `collapsedHeight` as `title.height` (it has tests at `test_skin.lua:192`). The band sits
   `inset` lower, which is invisible at 1-2px.
5. **Library or PGFE for placement.** Should LibKa0s expose the title band rectangle (for example
   `Skin:TitleBand(owner)` returning `inset, height`) instead of PGFE re-deriving `SkinPaint.lua:974`?
   **Recommendation:** keep it PGFE-local now, with a test that pins it to the tokens. File a LibKa0s
   issue if a second addon needs a header button.
