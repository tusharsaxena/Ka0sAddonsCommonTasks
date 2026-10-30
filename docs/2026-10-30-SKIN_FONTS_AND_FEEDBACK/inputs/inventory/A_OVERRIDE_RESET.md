# A_OVERRIDE_RESET: overrides reset on a skin change (item 1), the Skin tab's reset buttons and Scope alignment (item 6)

Read-only inventory, 2026-10-30. LibKa0s is at `aefeba9` (`feat/2026-10-30-skin-library-followups`, v1.81.0).
Every path below is relative to `../LibKa0s/` unless it names another repo. Screenshots: image-06, image-29, image-30.

## 1. Current behavior

### 1.1 Where the overrides live

| Layer | Where | Evidence |
|---|---|---|
| Applied (the live state) | `Skin.owners[owner].font` / `.texture`: an LSM key, or nil for the skin's own | `LibKa0s/Skin.lua:664-668` (GetOverride), `:685-699` (SetOverride) |
| Stored (the profile) | each addon's `profile.skin.font` / `skin.texture`: `""` means the skin's own | e.g. `../AbsorbTracker/core/SkinSetup.lua:57-60, 110-125`; rows at `../AbsorbTracker/settings/General.lua:396-405` |
| Written by | the owner's write seam `spec.set(source, skin, ignore, media)` (the 4th argument, `media = {font, texture}`) and `Skin:WriteChoice` (the copy) | `LibKa0s/OptionsAppearance.lua:408-417`, `LibKa0s/Skin.lua:474-485` |
| Re-applied by | `NS.ApplySkinChoice()` with no arguments: SetChoice, then SetIgnore, then SetOverride from the store (load, profile events) | `../AbsorbTracker/core/SkinSetup.lua:337-354` |

The overrides lay over whatever base the owner draws: `withOverrides` replaces `font.body`, `font.title`, `hud.font`
and `bar.texture` (`LibKa0s/Skin.lua:738-753`). The base is the Ka0s skin, or EllesmereUI's derived table while
EllesmereUI paints (`baseOf`, `:757-764`; `SkinEUI.lua:321-329`).

All 16 adopters, PGFE and the Skin Tester included, have a media-aware seam (`NS.WriteSkinChoice` / `KCM.WriteSkinChoice`, `grep -c media` = 4 to 7 per file). Each font or
texture row's `onChange` re-applies only its own half (`NS.ApplySkinOverride(v, nil)`), which is a no-op once the
library has moved the applied pair. **No addon change is needed for any proposal below.**

### 1.2 Why the overrides persist across a skin change (item 1, root cause)

Nothing on any skin-change path touches them. A skin change moves only `o.source` / `o.skin`:

- **Skin tab pick:** `choose()` calls `Skin:SetChoice(owner, source, skin)`, then `spec.set(source, skin)` with no
  media half (`LibKa0s/OptionsAppearance.lua:330-338`). Called from the skin radios (`:532-534`) and the source
  radios (`:504-510`).
- **`Skin:SetChoice`** moves `o.source` / `o.skin` and repaints (`LibKa0s/Skin.lua:589-607`). It never reads or
  clears `o.font` / `o.texture`.
- **First-run picker:** a pick previews through `SetChoice` (`LibKa0s/OptionsSkinPicker.lua:418-426`). Apply saves
  `spec.set(source, key)` (`:430-439`). **Apply to all** calls `lib.__copySkinTo(Skin, name, source, key)` with
  `media` nil (`:493-505`), so every other owner keeps its overrides. Test
  `tests/test_options_skin_picker.lua:642-667` asserts that: *"and its font"* is left alone.
- **Copy to every Ka0s addon:** `copyTo()` sends this owner's overrides with the skin (`OptionsAppearance.lua:364-377`
  into `lib.__copySkinTo`, `:237-243`). That is a copy of the look, not a reset, and it stays correct.
- **The profile/CLI path:** `/xx set skin.skin <key>` runs the row's `onChange`, `NS.ApplySkinChoice(nil, v)`, which
  is SetChoice alone (`../AbsorbTracker/settings/General.lua:376-381`).
- The existing test `tests/test_options_appearance.lua:691-705` **pins the persistence**: it sets a texture
  override, picks `obsidian`, and expects `"Ka0s Flat"` to be read back.

The design is deliberate (skinning-§3 and Skin minor 6 present the overrides as independent of the skin). The owner
has now overruled it: *"choosing another skin must reset both to that skin's own"*.

### 1.3 The Font and texture section (image-29) and the Scope section (image-30)

Draw order in `O.AppearanceRows` (`OptionsAppearance.lua:604-626`): `drawSource`, `drawSkins`, `drawMedia`,
`drawScope`, `drawCopy`.

| Element | Code | Width | Container |
|---|---|---|---|
| Source radios (2) | `radio()` `:298-311` | `W_CHOICE` 0.32 (`:120`) | Flow group |
| Skin radios (9) | same | 0.32, three to a line | Flow group |
| Font / Texture dropdowns | `mediaDropdown()` `:449-462` | `O.BUTTON_PAIR_REL` 0.492 | Flow group |
| Scope check boxes (2) | `toggle()` `:391-403`, `drawScope()` `:475-486` | **`W_CHOICE` 0.32** (`:394`) | Flow group |
| Copy button | `drawCopy()` `:542-557` | 0.492 | **straight into `view.parent`**, between two `O.AddSpacer(ROW_VSPACER)` |
| `COPY_NONE` hint, `NOTE` | `textLine()` `:261-273` | full width | `view.parent` |

The dropdowns offer "Skin's own (<key>)" as their first entry (`mediaList`, `:429-446`), so a reset is possible
today but takes two clicks. No button does it in one (item 6, image-29).

**The Scope misalignment (image-30), measured on the screenshot:**

1. **The columns disagree.** *Ignore fonts* begins at about x=245, that is 0.32 of the row, because the Scope
   boxes use `W_CHOICE` (`:394`). The *Texture* dropdown directly above it (image-29) begins at about x=368, which
   is 0.492. These are two adjacent two-control sections on two different grids. options-ui-§6 says a schema
   page pairs into 50/50 cells. The Scope pair is the only two-control row on the tab that uses the
   three-column grid, apart from Source, which aligns with the skin grid below it.
2. **The Copy button and the note look like part of Scope.** They are drawn after the Scope heading with no heading
   of their own (`drawCopy`, `:542-557`), but they are not scope settings. `NOTE` ("Skins change every visual
   element. HUD style options follow the skin...") applies to the whole tab. It describes the Look.
3. **Left edges.** The check box art begins at about x=9 and the button art at about x=8. The note's text begins at
   about x=5. This is AceGUI's own art inset. image-29 shows the same 4 px offset between the *Font* label and its
   dropdown box, so it is consistent across the tab and needs no fix.
4. **The "stray icons" at the right** (a grey rounded square above a gold chevron with a red gem, x≈745, beside the
   Copy button and the note) are almost certainly **the page's scroll bar**: AceGUI's `UIPanelScrollBarTemplate`
   knob, with its *ScrollDownButton* under it. The page is scrolled to its foot, and the note is the last row.
   `../AbsorbTracker/libs/AceGUI-3.0/widgets/AceGUIContainer-ScrollFrame.lua:177-190` creates the bar, and its only
   track is a 40% black texture, which is invisible on a dark page. `lib.PatchAlwaysShowScrollbar` keeps it shown
   (`LibKa0s/OptionsScroll.lua:111-160`). Image-30 is the client's stock look: *Ignore settings panel* is ticked, and
   the button is the stock red UIPanelButton. While the panel is ignored, `__chromePaint` paints nothing
   (`OptionsScroll.lua` minor 7, header `:24-28`), so the bar is Blizzard's. Under a skinned panel,
   `S.ScrollBar` draws a corridor and knob (`SkinPaintControls.lua:412-430`) and the parts would not look stray.
   **This is not a Scope element, and no Scope code draws it.**

## 2. Proposed change: LibKa0s only

### 2.1 Overrides reset on a skin change (item 1)

**A new library-level helper** in `LibKa0s/OptionsAppearance.lua`, next to `lib.__copySkinTo` (`:237`). The tab,
the picker and both copies share it:

```lua
--- Move `name` to (source, skin) and, when the look it draws changed (Skin:DrawsKey before and
--- after), its font and texture back to the skin's own. Answers changed, reload, cleared. Internal.
function lib.__chooseSkin(Skin, name, source, skin)
  local draws = type(Skin.DrawsKey) == "function" and function() return Skin:DrawsKey(name) end
  local before = draws and draws()
  local changed, reload = Skin:SetChoice(name, source, skin)
  if not (changed and type(Skin.SetOverride) == "function") then return changed, reload, false end
  local font, texture = Skin:GetOverride(name)
  if not (font or texture) or (draws and draws() == before) then return changed, reload, false end
  return changed, reload, Skin:SetOverride(name, false, false)
end
```

- **When the overrides reset.** Only when the face actually changes, measured as `DrawsKey` before against after
  (`Skin.lua:778-781`):
  - a Ka0s skin to another Ka0s skin: they reset;
  - `ka0s` to `eui` while EllesmereUI paints: they reset, because the base becomes EllesmereUI's face;
  - picking a Ka0s fallback skin while EllesmereUI paints the owner: they are kept, because the look did not change;
  - re-clicking the checked skin: they are kept, because SetChoice is idempotent;
  - leaving `eui` after a paint (a pending reload): they reset, with no repaint until the reload, and the reload
    then shows the new skin's own face.
- **`choose()`** (`:330-338`) calls `lib.__chooseSkin`. After `spec.set(source, skin)`, when `cleared` is true, it
  also calls `spec.set(nil, nil, nil, { font = false, texture = false })` so the profile matches. Combat is still
  refused first, so nothing resets in combat. `view.sync()` already re-reads both dropdowns (`:572-576`).
- **`lib.__copySkinTo`** (`:237-243`) calls `__chooseSkin` in place of `SetChoice`:
  - With `media` given (the tab's copy) it then applies that media, as today, so the result is this owner's
    overrides. That behavior is unchanged.
  - With `media` nil (the picker's *Apply to all*), when `cleared` is true it passes
    `{ font = false, texture = false }` to `WriteChoice`, so the other owner's profile matches its applied state.
  - The picker therefore needs no copy change of its own.
- **The picker** (`OptionsSkinPicker.lua`):
  - **Show** (`show()` `:727-749`): a fresh showing also records `P.openedMedia = { Skin:GetOverride(owner) }`.
  - **`pick(key)`** (`:418-426`): measure the pick against the look the window **opened** with, not the last
    preview. If the pick draws a different key from `P.opened`, preview with the overrides cleared
    (`SetOverride(owner, false, false)`, no write). If the player picks back to the opened skin, restore
    `P.openedMedia`. The preview then shows exactly what Apply will save.
  - **`save()`** (`:430-439`): after `spec.set(source, key)`, if the saved skin differs from `P.opened`, call
    `spec.set(nil, nil, nil, { font = false, texture = false })`.
  - **`revert(p)`** (`:446-451`): after its `SetChoice`, put back `p.openedMedia` with `SetOverride`.
- **The Copy to every Ka0s addon action:** no behavior change. It still carries this owner's font and texture,
  whether those are the skin's own after a reset or overrides the player picked after it. The confirmation's
  wording stays true.
- **EllesmereUI source:** covered by the `DrawsKey` rule above. `SkinEUI.lua` needs no change.
- **The profile and CLI paths are left alone.** These are a profile switch, copy or reset (re-applying stored
  values) and `/xx set skin.skin <key>` (a raw row write). Resetting inside `Skin:SetChoice` itself would be
  **wrong**: at load, `ApplySkinChoice()` moves the owner from the registration-time Ka0s Default to the stored
  skin, and a reset there would wipe the profile's own overrides. See Q2.
- **Minors:** OptionsAppearance 3 to 4, OptionsSkinPicker 2 to 3. The Skin major is unchanged.

**The cost: two repaints per pick.** A pick that clears costs two repaints (SetChoice, then SetOverride) and two
`OnLooksChanged` firings, both synchronous and out of combat, with no visible flash. Q3 asks whether to remove the
second one.

### 2.2 Reset-to-default buttons for Font and Texture (item 6, image-29)

`drawMedia()` (`:465-472`) gains a second Flow row under the dropdowns:

```
Font and texture
[ Font dropdown        0.492 ][ Texture dropdown     0.492 ]
[ Reset font           0.492 ][ Reset texture        0.492 ]
```

- Each button uses `O.AceGUI:Create("Button")` at `O.BUTTON_PAIR_REL`, so it sits exactly under its dropdown.
  `OnClick` calls `setMedia(view, which, FROM_SKIN)` and then `view.sync()`. That is the same seam as a dropdown
  pick: combat refusal, the live `SetOverride`, then `spec.set(nil, nil, nil, media)`.
- **Why a separate row:** an AceGUI Dropdown carries its label above the box. A button on the same Flow line would
  top-align with the label, not the box, and look misaligned. A cell of its own also cannot truncate under item 5's
  font widths.
- **State:** `view.sync()` disables each button while its half is already the skin's own (`media[which] == false`),
  and both while `ctx.__renderDisabled` is set. They join the view as `view.reset = { font, texture }`.
- **Words:** new `lib.APPEARANCE_STRINGS` keys, ASCII and in sentence case (options-ui-§21):
  - `RESET_FONT = "Reset font"`, `RESET_FONT_TIP = "Use the skin's own font again (%s)."`
  - `RESET_TEXTURE = "Reset texture"`, `RESET_TEXTURE_TIP = "Use the skin's own bar texture again (%s)."`
  - `%s` is the skin's own key, from `baseTokens()` as in `mediaList`.

### 2.3 Scope alignment (item 6, image-30)

1. **One grid for the pair rows.** `toggle()` uses `O.BUTTON_PAIR_REL or 0.492` in place of `W_CHOICE`
   (`OptionsAppearance.lua:394`). *Ignore fonts* then starts in the same column as *Texture* and *Reset texture*
   above it. `W_CHOICE` stays for the Source and skin radios (the three-column grid).
2. **The Copy button leaves Scope.** `drawCopy()` (`:542-557`) opens with its own heading, through `heading(view, S.COPY_HEADING)`,
   so the button stops reading as a scope setting. Recommended text: `COPY_HEADING = "Other Ka0s addons"`. The
   button goes into a `flowGroup` row, so it gets the same container and left edge as every other control row. The
   `COPY_NONE` hint stays under it.
3. **`NOTE` moves to the Look section.** It becomes the muted lead line under the "Look" heading in `drawSkins()`
   (`:524-539`), where `SKIN_EUI_NOTE` already sits, because it describes what a skin changes. The tab then ends on
   the Copy row, not on a free-floating line. The `view.note` member is kept.
4. **Left edges:** no change (§1.3 item 3).
5. **The stray icons:** no code change, pending Q4. They are the page's stock scroll bar, shown because *Ignore
   settings panel* is on.

## 3. Tests (LibKa0s)

`tests/test_options_appearance.lua`:

- **Change** `:691-705` ("sync re-reads the overrides, and the skin's own entry follows a skin switch"). Set the
  override *after* the switch, or assert that the switch reset it. Today it pins the old behavior.
- **New tests:**
  - A skin pick with both overrides set clears both. Check `Skin:GetOverride` = nil, nil, the seam receiving
    `set(nil, nil, nil, {font=false, texture=false})` after `set(source, skin)`, both dropdowns reading `@skin`, and
    the store holding `""`.
  - Re-clicking the checked skin keeps both overrides, with no media write.
  - A pick with no overrides set writes no media half.
  - An override picked after a switch sticks until the next switch.
  - A Ka0s fallback pick while EllesmereUI paints keeps the overrides (`fixture_skin_eui.lua`). A source switch
    `ka0s` to `eui` that paints resets them.
  - In combat a skin pick resets nothing.
  - Copy: an other owner whose skin changes ends up with *this* owner's overrides (extend `:707-722`).
  - The reset buttons: they draw under the dropdowns at `BUTTON_PAIR_REL`; each is disabled while its half is the
    skin's own; a click clears only its half (live, then the seam); the click is refused in combat; a page drawn
    disabled draws them disabled; `spec.strings` translates both labels and tips.
  - Scope layout: both toggles at `BUTTON_PAIR_REL`; the Copy row sits under its own heading after Scope; `NOTE`
    sits under the Look heading, ahead of the first skin radio (adjust `:494-511` and the draw-order test `:213`).

`tests/test_options_skin_picker.lua`:

- **Change** `:642-667` ("Apply to all ... the source and skin alone"). The other owners whose skin changed now have
  their overrides cleared, and their setter receives `w[4] = {font=false, texture=false}`. Their scope is still
  left alone.
- **New tests:**
  - A pick to another skin previews with the overrides cleared and writes nothing.
  - Picking back to the opened skin restores them.
  - A close or Escape restores `openedMedia`.
  - Apply writes the cleared media only when the saved skin differs from the opened one.

`tests/test_skin.lua` / `test_skin_override.lua`: no change, because the Skin major is unchanged. Add a guard test
that `Skin:SetChoice` still never clears an override, so the load path stays safe.

`tests/test_prose.lua`: the new strings are ASCII, so `:534`'s single ratified ellipsis is unchanged.

## 4. Docs and standard ripple

- `docs/api/Options/`: new version docs for OptionsAppearance minor 4 and OptionsSkinPicker minor 3, covering
  `lib.__chooseSkin`, `view.reset`, the five new string keys and the moved `NOTE`. Also update
  `docs/api/CONSUMERS.md`.
- `WowAddonStandards` `standards/standards/skinning.md` §3 "What it holds": add "selecting another skin resets the
  font and texture overrides to the new skin's own (from LibKa0s v1.82.0); a *Reset font* and a *Reset texture*
  button under the two dropdowns". Its prose order (Scope, then Copy, then note) also changes to match §2.3. Add a
  CHANGELOG entry and a version bump.
- Addons: a re-vendor only. No addon source changes (§1.1).

## 5. Risks

- **The load path.** If anyone later moves the reset into `Skin:SetChoice`, every profile's overrides are wiped at
  login (§2.1). The guard test in §3 pins this.
- **The picker revert.** `openedMedia` is the *applied* pair at open. A Skin-tab override change made while the
  picker is up would be undone by a close. This is the same class as today's `revert` for the choice, which
  re-reads `spec.get`. There is no media getter on the picker spec. Low risk: the picker is modal-ish and shows on a
  new profile.
- **`DrawsKey` absent.** On a Skin copy older than minor 7, `draws` is nil and any changed choice resets.
  Acceptable: v1.81.0 ships minor 8 everywhere.
- **Two repaints and two `OnLooksChanged`** per clearing pick. Addons broadcast APPEARANCE twice. This is cheap and
  only happens outside combat.

## 6. Open questions for the lead

1. **Which change resets?** Recommend: a change in `DrawsKey` (the face actually drawn), so a source switch to a
   painting EllesmereUI also resets and an EllesmereUI fallback pick does not. The alternative is a change in the
   skin key only, which is simpler but reacts to a fallback pick the player cannot see.
2. **Should `/xx set skin.skin <key>` also reset?** Recommend **no**: it is a raw row write. Profile events
   re-apply stored values and must never reset. Document this in skinning-§3. If the lead wants yes, it is a
   16-addon row `onChange` change, which this inventory does not cost.
3. **One repaint in place of two?** Recommend accepting two. The alternative is a Skin-major minor 9 (for example
   `SetChoice(owner, source, skin, media)`, with a single repaint). That widens the Skin API and its parity surface
   for no visible gain.
4. **The "stray icons" (image-30).** Recommend confirming with the owner, using a full-page screenshot under
   *Ignore settings panel*, that they are the stock scroll bar. If the owner wants them gone, the choices are:
   (a) paint the page scroll bar even while the panel is ignored, which contradicts skinning-§3's "settings panel
   keeps the client's look"; (b) give the stock bar a visible track (raise AceGUI's `scrollbg` alpha) in
   `PatchAlwaysShowScrollbar`; (c) leave it. Recommend (c), or (b) if the owner insists.
5. **The Copy section heading text.** Recommend "Other Ka0s addons". The alternative is no heading, with only the
   spacer and Flow row, which fixes items 1 and 3 of §2.3 but leaves Copy visually under Scope.
6. **Should `NOTE` move to the Look section?** Recommend yes (§2.3 item 3). The alternative is to keep it last,
   under the new Copy heading.
7. **Reset button placement.** Recommend a row under the dropdowns. The alternative is a narrow button beside each
   dropdown (dropdown about 0.39 plus a button about 0.10), which is rejected because of the label top-alignment
   and the truncation risk.
