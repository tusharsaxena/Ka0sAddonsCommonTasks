# Plan: per-addon font and texture overrides (LibKa0s#63) and the first-run skin picker (LibKa0s#64)

Created 2026-10-28 on the owner's word ("go ahead and build issues #63 and #64", under the standing run
guidelines: decide yourself, a checkpointed plan, a branch and incremental commits, push at milestones,
merge only on the go-ahead, clean up afterwards).

Branch `feat/2026-10-28-skin-overrides-picker` in LibKa0s, LootHistory, LibKa0sSkinTester and this repo.
An item is done when a commit whose subject starts `<ID>: ` exists in the repo that owns it.

## Scope

- **Library:** LibKa0s (the Skin major, SkinDefs, Media, the Appearance tab, a new picker file in the
  Options major).
- **First adopters:** LootHistory and LibKa0sSkinTester only. Every other addon gets this in the later
  collection-wide skinning adoption pass.

## Decisions (mine, recorded so a reviewer can check them)

- **D1. An override is applied where tokens resolve.** `Skin:__Tokens(owner)` answers the skin's table
  with the owner's overrides laid over it, so every primitive and every host `S.Token` read sees them
  with no per-primitive change. A font override replaces `font.body`, `font.title` and `hud.font`;
  `font.mono` stays the skin's (the debug console and tables need a monospace face). Sizes stay the
  skin's. A texture override replaces `bar.texture`.
- **D2. "Texture" means the bar texture** (an LSM `statusbar` key), the one most WoW addons offer as
  "Texture". It reaches every element that draws a bar of data: status and progress bars, chart bars,
  stacked bars. Window, button, tab and check-box art stay the skin's.
- **D3. Ignore fonts wins over a font override.** With "Ignore fonts" on, every string keeps the
  game's face, as today, and the font override is kept but has no effect.
- **D4. The tab's key stays `Appearance`; only its label becomes "Skin".** Hosts name the key in
  `before` and in a stored active tab, and renaming it would move every one of them for no visible gain.
- **D5. The picker lives in the Options major** (`OptionsSkinPicker.lua`), because its gear button
  opens the settings panel at the Skin tab (`O.OpenOptionsPanel`, `O.SelectTab`), and it paints itself
  with the owner's own skin through the Skin facade.
- **D6. The picker shows while the profile key `skin.pickerSeen` is false.** A new profile and a reset
  profile both start from the defaults, so both show it; closing the picker (its close button, or the
  gear) sets the key. Picking a skin or pressing the eye does not close it.
- **D7. The picker's dropdown shows three swatches per skin**, as the owner asked (the first three of a
  skin's four), and each skin's name in that skin's own body face and size.
- **D8. "Copy to every Ka0s addon" carries the overrides** along with the source, skin and scope: they
  are part of the look.

## Items

| Id | Repo | What | Depends on |
|---|---|---|---|
| SO-01 | LibKa0s | Skin minor 6: `GetOverride`, `SetOverride`, overrides in `__Tokens`, `WriteChoice`'s fifth argument `media` | — |
| SO-02 | LibKa0s | `S.BarTexture(target, r, g, b, a)`, a new vocabulary entry: the owner's bar texture onto a Texture or StatusBar, tinted, replayed on a repaint | SO-01 |
| SO-03 | LibKa0s | OptionsAppearance minor 3: the tab is labeled "Skin"; a "Font and texture" section with two dropdowns; the copy carries them | SO-01 |
| PK-01 | LibKa0s | `OptionsSkinPicker.lua`: `O.SkinPicker(spec)`, `O.HideSkinPicker()` | SO-01 |
| SO-04 | LibKa0s | A default bar texture for every skin: `tools/artwork/skin_textures.py`, seven new TGAs, Media's catalog, SkinDefs' `bar.texture` per skin. **Waits for the owner's approval of the texture mockup.** | owner |
| SO-05 | LibKa0s | Release record v1.79.0: CHANGELOG, `docs/api/`, the version suite, a clean-tree release run, local tag | all LibKa0s items |
| LH-01 | LootHistory | Re-vendor; store and apply the overrides; `BarTexture` on the chart bars; the picker; the icons; "Skin" wording; smoke checks | SO-01..03, PK-01 |
| ST-01 | LibKa0sSkinTester | The same, plus a Textures section in the showroom | SO-01..03, PK-01 |
| LH-02, ST-02 | both | Re-vendor the tagged v1.79.0 (with SO-04's textures) | SO-05 |
| CT-01 | this repo | This plan and the execution record | — |

## The library surface (exact)

- `Skin:GetOverride(owner)` → `font, texture`: LSM keys, or nil for "the skin's own".
- `Skin:SetOverride(owner, font, texture)`: nil keeps that half; `false` or `""` clears it. Idempotent.
  A change repaints the owner's frames (unless a reload is pending) and fires its OnLooksChanged
  listeners. Answers `changed`.
- `Skin:WriteChoice(owner, source, skin, ignore, media)`: `media`, optional, is
  `{ font = key|false, texture = key|false }` and reaches the host's setter as its fourth argument
  (`set(source, skin, ignore, media)`). An older setter ignores it.
- `S.BarTexture(target, r, g, b, a)`: on a Texture, `SetTexture(<the owner's bar texture>)` and
  `SetVertexColor(r, g, b, a)`; on a StatusBar, `SetStatusBarTexture` and `SetStatusBarColor`. With no
  texture resolved it falls back to `SetColorTexture(r, g, b, a)`, today's flat look. Recorded, so a skin
  switch or an override change re-applies it.
- `O.SkinPicker(spec)`: shows the picker (one per Options instance) and answers its frame. `spec`:
  `owner` (default the descriptor's `addonName`), `get` and `set` (the same seams as `O.AppearanceTab`),
  `onPreview` (the eye; the button is absent without it), `onSettings` (the gear; default: open the panel,
  then `O.SelectTab(spec.page, spec.tab or "Appearance")`), `page`, `onClose` (the host sets
  `skin.pickerSeen`), `strings`. `O.HideSkinPicker()` hides it.

## The hosts' profile keys

`skin.font` and `skin.texture` (strings, `""` = the skin's own) and `skin.pickerSeen` (bool, default
false), each a skip-render schema row beside the existing `skin.*` rows, written only through the host's
skin write seam.

## Checkpoints

1. The library items SO-01..03 and PK-01 are committed and green; the feature branch is pushed.
2. Both consumers are committed and green against the branch's library; branches pushed.
3. After the owner approves the textures: SO-04, SO-05, LH-02, ST-02; branches pushed.
4. Merge, the tag push and branch deletion only on the owner's go-ahead.

## Gates

Every repo: `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` and
`~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` (0 warnings, 0 errors), the 1500-line file cap.
In-client smoke checks are the owner's; they are listed in each addon's `docs/smoke-tests.md` and in
the execution record, and none is marked passed here.
