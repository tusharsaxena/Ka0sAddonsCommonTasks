# H_AURAMASTER: item 9 (image-35, 36, 37)

Read-only inventory. AuraMaster was inspected on `feat/2026-10-30-skin-library-followups` at `b734425`. Its
`docs/smoke-tests.md` shows as modified in `git status`, but `git diff` is empty, so this is probably a
line-ending artifact. Leave that file alone and do not reset it.

## 9a. The "TEST" label next to every container

### What draws it

The label belongs to AuraMaster. LibKa0s does not draw it.

- `modules/Preview.lua:241-322` is the TEST marker. `Preview.ApplyMarker(container, on)` builds a
  mouse-less frame `container.testMarker` with one font string, `container.testMarkerText`. It places that
  string over the placeholder block (`container.previewExtent`) at the corner where the first placeholder
  starts, inset by 2 px (`MARKER_INSET`), at level `C.LAYERS.LEVEL.MARKER` (40, `core/Constants.lua:246`).
  The text is `Preview.TestTag()` (`:259`), the localized `L["TEST"]` (`locales/enUS.lua:761`) in the
  skin's `sem.warn`.
  - `Preview.Reskin` repaints it on `OnLooksChanged` (`:304-312`).
  - `Preview.Hide` hides it (`:315-319`).
- It is called from `modules/Container.lua:927-928`, inside `ApplyVisibility`:
  `NS.Preview.ApplyMarker(self, show and previewing and not (self.handle and self.stripShown))`. The marker
  therefore appears whenever test mode is on and the drag strip is not shown, which means a locked
  `/am test`. That matches image-35: the containers are locked, every block has a TEST at its first
  placeholder's corner, and on the bars it covers the first letters of the name ("TESTower Word").
- A second, separate TEST lives in the unlocked strip label: `modules/Anchors.lua:644-655`
  (`tag = "  " .. NS.Preview.TestTag()`). It is not what image-35 shows.

### History

| Commit | Date | Change |
|---|---|---|
| `ffe08ae` | 2026-10-22 | "AM-01: mark a locked test mode TEST on the display". The only commit that adds `ApplyMarker` (`git log -S'ApplyMarker' --all`). |

It was added on purpose, to satisfy the standard:

- `WowAddonStandards/standards/standards/preview-mode.md:11-24`, the v2.86.0 rule "A test mode MUST say so
  on the display". While the explicit test mode is on, every display that draws placeholder data **MUST**
  carry a visible, localized text marker in every layout where that data shows.
- Missing markers are anti-pattern #97.
- The rule says explicitly that the launcher tooltip and the Master-controls checkbox do not count as
  markers.
- Smoke check CONT-27 (`docs/smoke-tests.md:772`) covers it and passed on 2026-10-23 (`:2508`).

**Removing the marker breaks a MUST in the standard.** The removal has to ship with an amendment to the
standard (see open question Q1), or AuraMaster becomes non-compliant with anti-pattern #97.

### Proposed change (AuraMaster, plus the standard)

1. **`modules/Preview.lua`**
   - Delete lines 241-302: the marker block comment, `MARKER_INSET`, `MARKER_LEVEL`, `Preview.MarkerText`
     and `Preview.ApplyMarker`.
   - Delete `Preview.Reskin` and its `NS.Skin.OnLooksChanged` registration (`:304-312`).
   - Delete the `testMarker` line in `Preview.Hide` (`:318`).
   - Keep `Preview.TestTag()`, because the strip label uses it (`modules/Anchors.lua:655`). Its comment at
     `:256-258` should name only the strip.
2. **`modules/Container.lua:927-928`**: delete the comment and the `ApplyMarker` call.
3. **`core/Constants.lua`**
   - Drop `MARKER = 40` from `LAYERS.LEVEL` (`:246`). Do this only if nothing else reads it; today only
     `Preview.lua` and `tests/test_layers.lua` do. The alternative is to keep it as a reserved band.
   - Fix the comments at `:203` and `:291`.
   - Fix the `core/SkinSetup.lua:130` comment, which lists "the TEST tag".
4. **Tests**
   - `tests/test_preview.lua:619-670`. Replace the three marker cases with one: "a locked test mode draws
     no TEST marker". It should assert that `inst.testMarker == nil` for every previewing container, and
     that the placeholders still show and `Preview.Hide` still works. Keep the half of the unlocked case
     that checks the strip still carries its TEST tag.
   - `tests/test_skin_surfaces.lua:235-249`. Delete "a shown TEST marker is retold in the new skin's
     sem.warn". The strip-tag case at `:97` stays.
   - `tests/test_layers.lua:31-33` (the band ordering, if `MARKER` goes) and `:90-102` (the marker's level).
   - Regenerate `docs/test-cases.md` and its badge.
5. **Docs**
   - `docs/smoke-tests.md`:
     - Retire CONT-27 (`:772`). Mark it retired or rewrite it as "locked `/am test` shows placeholders with
       no TEST word; `/am unlock` shows the strip with its TEST tag". Keep its id rather than renumber.
     - Change the index row at `:24` ("test mode and its TEST marker").
     - Change the mentions at `:2152`, `:2282`, `:2296` and `:2333`.
     - Leave the historical result line at `:2508` as it is.
   - `docs/ARCHITECTURE.md:165, 324, 360` and `docs/module-map.md:110` (Preview row).
   - CHANGELOG Unreleased.
6. **WowAddonStandards**: amend `preview-mode.md` (anti-pattern #97 and the `STANDARDS.md:62` blurb).
   This connects to item 11, where the owner already asked for the simulation placeholder anchor to be
   removed "and in the standard". Both are owner rulings against on-display test text on HUD displays.

**Risks.**
- In a locked test mode, nothing on screen says the auras are fake. That is the failure #97 was written
  for, and the owner is accepting it.
- Strict audits flag AuraMaster until the standard changes. Land the standard amendment first or in the
  same milestone.

## 9b. The glow behind the text regressed

### The owner's inputs (SavedVariables)

Source: `WTF/Account/ADD1KTED2KA0S/SavedVariables/AuraMaster.lua`, profile `Default`, containers 13, 14 and 15
(`[4] PLYR TXT Offensive CD`, `[5] ... Defensive CD`, `[6] ... Raid CD`). The `text` block holds:

| Setting | Value |
|---|---|
| `glow` | `true` |
| `glowColor` | `{0,0,0,1}` (black) |
| `glowIntensity` | `0.5` |
| `glowThickness` | `4` |
| `glowX` | `-4` |
| `glowY` | `0` |
| `font.font` | `"Ka0s Kait"` |
| `font.fontFromSkin` | `true` |
| `font.fontFlags` | `THICKOUTLINE` |
| `font.fontShadow` | `true` |
| `font.fontSize` | `36` |
| `fontColor` | green `19FF19` for [4], red `FF2020` for [5] |

- The profile's `skin` holds only `pickerSeen`, so the skin is Ka0s Default, whose
  `hud.font = "Ka0s Oxanium SemiBold"` (`LibKa0s/LibKa0s/SkinDefs.lua:336`).
- The glow values are exactly the defaults the owner set on 2026-10-16 (`defaults/Profile.lua:311-314`).
  They were never changed.

### Bisect

- **The glow code has not changed since the owner approved it.** `git log -- modules/Style_TextGlow.lua`
  ends at `93ef023` (TG-13, 2026-10-16).
- `C.TEXT_GLOW_RING`, `TEXT_GLOW_PAIRED` and `TEXT_GLOW_TWINS` (`core/Constants.lua:347-349`) are
  unchanged.
- `Style.ApplyFont`'s shadow is still black at (1, -1) (`modules/Style.lua:153-157`).
- Between TG-13 and HEAD, only two commits touch the glow's path:
  - **`891b987`** (AM-ZS, 2026-10-24). It renames the frame levels of the twin engines and their holder
    (`Container_Twins.lua`). That affects only the live twins' stacking, not their look. It also cannot
    explain image-36, which shows test-mode placeholders, whose copies are strings on the same frame's
    BACKGROUND layer (`Style_TextGlow.lua:136-140`).
  - **`f91ca81`** (AM-03, 2026-10-29, the skinning rollout). **This is the cause.**
    - `Style.FontKey` (`modules/Style.lua:1052-1057`) now resolves the face through
      `Style.SkinKey("hud.font", t.font, fromSkin)`.
    - `defaults/Profile.lua` makes `fontFromSkin` true by default.
    - The one-time schema v13 step (`core/Database_Migrations.lua`, `Database.MigrateV13`) turns
      `fontFromSkin` on for every stored container, under ruling O2.
    - Result: the three Text containers stopped drawing the owner's **Ka0s Kait** and draw Ka0s Default's
      **Oxanium SemiBold**. The stored pick `"Ka0s Kait"` is kept, and image-37 shows "Use the skin's font"
      ticked.
    - The glow copies follow the same face, because `Text.GlowFontKey` goes through `Style.FontKey`, so the
      ring and the main text stay matched. What changed is the face.
- **Red tint ruled out.** I sampled pixels in image-36. The ring is pure black at 50%. The dark-red pixels,
  for example `(112,2,2)` inside the counter of "B", are just the one-pixel anti-aliased edge of the red
  glyph over opaque black. The glow color never changed, and nothing paints the copies in the font color.

### Why it looks worse, especially behind red

The ring has 8 copies in total: 4 copies (`C.TEXT_GLOW_RING[1..4]`), each with a paired shadow at −2·t·d.

- **Geometry.** With t = 4 and X = −4, the copies sit at (0,0), (−4,+4), (0,+4) and (0,−4), and the
  shadows at (−8,0), (−4,−4), (−8,−4) and (−8,+4). The ring is centered 4 px left of the text and reaches
  8 px left and 0 px right. It is a deliberately one-sided black smear, which the owner tuned against Kait.
- **Kait hid that shape.** It is a very heavy all-caps display face: thick strokes and tiny counters. A
  half-opaque black ring 4 px wide merges behind it into one dense dark slab that reads as a strong drop
  glow.
- **Oxanium exposes it.** It is mixed case with thinner strokes, open counters and ascenders. The same
  fixed-pixel ring is now about as wide as a stroke, so it shows as a second, offset ghost of each letter.
  It fills the counters solid black and leaves ragged steps where the eight offsets do not overlap, which
  is the smudged double image in image-36.
- **Why red suffers most.** Red `FF2020` has a relative luminance of about 0.22, against about 0.73 for
  green `19FF19` and about 0.45 for orange. The THICKOUTLINE plus a solid-black ring touching the glyph
  leaves red with very little contrast at its edges, so the dark-red anti-aliased fringe and the black mass
  merge and the letters look muddy and thin. Green stays bright against black, so it only looks smeared.

A simulation using the owner's real values and the real font files confirms this. Kait looks dense and
clean, while Oxanium and Prototype look ghosted and smeared, worst in red. It is at
`/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/b89d9d2c-15cf-430b-86d0-0d23a60c5516/scratchpad/sim.png`
(Prototype at the top). **Moving Ka0s Default to Prototype under item 3 does not restore the look**:
Prototype is also mixed case and smears the same way.

### Proposed fix

- **Recommended (no code): give these three containers their face back.**
  - On each of [4], [5] and [6], untick Text style → Font → "Use the skin's font". The stored "Ka0s Kait"
    returns at once, and the glow looks exactly as it did on 2026-10-16. The design of
    `fontFromSkin`/v13 already allows a later pick to stick.
  - This is the owner's action in game. It must not be done by editing SavedVariables.
  - Add one line to the smoke-test record: "TXT containers: skin font off, Kait restored, glow as before".
- **Optional AuraMaster code, if the owner wants the glow to survive face changes:**
  - (i) **Center the default ring.** Change `defaults/Profile.lua:314` to `glowX = 0`. That affects new
    containers only, so the owner's stored −4 stays.
  - (ii) **Scale the ring with the font size.** In `Text.GlowFont` and `dressSet`
    (`modules/Style_TextGlow.lua:116-127` and `:157-170`), multiply `t` by `size / 36`, or by a per-face
    factor. This touches twins and copies alike through the one `GlowFont` path. Tests go in
    `tests/test_style_text_glow.lua` (offsets for a given size and thickness) and `test_container_twins`
    (shadow offsets).
  - I do not recommend either for this run. Neither restores the earlier look by itself, and both change a
    look the owner tuned.
- **Not recommended:** a v14 migration that turns `fontFromSkin` off for glowing Text containers. It
  overturns ruling O2 for the whole account and would need a sentinel to run once.

**Risks.** The data-only fix leaves these containers off the skin's face, so a skin change no longer reaches
them. That is the intended meaning of unticking. Other glowing Text containers on other accounts or
characters behave the same way; the CAMRY1 account was not checked.

## Open questions for the lead

1. **The standard's preview-mode MUST (anti-pattern #97) and the TEST marker.** How do we reconcile them?
   Recommendation: amend `preview-mode.md`.
   - For a **HUD display** (a positionable overlay such as an aura container, not a standalone window),
     the on-display marker becomes a **MAY**.
   - The unlocked strip's tag stays the recommended form.
   - Land it with item 11's removal of the simulation placeholder in the same standard bump, so there is
     one ruling: "no test text drawn over HUD content".
2. **Does the unlocked drag strip keep its TEST tag** (`modules/Anchors.lua:655`)? Recommendation: keep
   it. The owner's complaint is the locked marker sitting on the content (image-35), and the strip is
   chrome, outside the content.
3. **Glow: data fix or code?** Recommendation: the owner unticks "Use the skin's font" on [4], [5] and
   [6], which restores Kait and the glow exactly, with no code change.
   - Report to the owner that the glow code did not regress. The skinning rollout's v13 reset (`f91ca81`)
     swapped Ka0s Kait for Oxanium.
   - Ask whether they want option (ii), the glow scaled to the font size, filed as an issue for later.
4. **Ka0s Kait as a shipped face?** If the owner wants these displays on the skin's face and the old look,
   that only works if a skin's HUD face is a heavy all-caps face like Kait. Recommendation: no. Keep Kait
   as the owner's per-container pick.
