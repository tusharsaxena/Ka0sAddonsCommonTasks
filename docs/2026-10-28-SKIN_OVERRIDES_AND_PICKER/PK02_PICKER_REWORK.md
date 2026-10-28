# Addendum PK-02 and PK-03: the picker reworked after the owner's first look

Added 2026-10-28 during execution. The owner looked at PK-01's picker in game and asked for these changes:

- Move the window up, to about 75% of the screen height, so the addon window the eye opens does not
  cover it.
- Name the addon the skin is being chosen for.
- Add an "Apply" button that saves the choice and closes the window.
- Add an "Apply to all Ka0s addons" button.
- Show the window only once when several Ka0s addons are installed at the same time.

## PK-02 (LibKa0s 9bc1826, c40e937, 0c7b822, 1f179ea)

- The picker's center sits at 75% of UIParent's height. The title reads "Choose a skin for <addon>".
- A pick only previews the skin. **Apply** saves it and closes. The close button and Escape put the old
  skin back and close. The gear saves the pick, then opens General > Skin:
  `O.OpenOptionsPanel(pageKey)` is OptionsRegistry minor 4.
- **Apply to all Ka0s addons** applies this owner's skin to every registered owner, using the Skin tab's
  own copy helper. One reload popup lists every addon that needs a reload.
- **One window across addons.** LibStub loads only the newest copy of the library, so every Ka0s addon
  shares the same Options table. `lib.__pickerQueue` shows one picker at a time; the others queue, oldest
  first. Apply to all ends the queue and marks every queued owner as seen.
- The Skin tab's heading over the skins reads "Look", so it no longer repeats the tab's name
  (options-ui-§7).

## PK-03 (LibKa0s 25be9d3, 183bc57)

The consumer reviews found three problems in the library. Loot History had worked around the first two
on its own side. All three were fixed upstream, and the workarounds were removed in LootHistory ca095c2:

- The picker now uses DIALOG strata and raises itself after the eye runs, so no HIGH addon window can
  cover it. The frame-layering-§6 row pending for the standard now names DIALOG, not HIGH.
- A close undoes only the unsaved preview: it puts back the stored choice as `spec.get` reads it at
  that moment. With no usable `get`, it puts back the choice the window opened with.
- A queued picker waits until combat ends before it shows.

## Open owner decisions

- A close during combat still puts the preview back (`SetChoice`, not a write). The alternative is to
  refuse the close in combat.
- A direct first `O.SkinPicker` call made in combat still shows at once; hosts defer it themselves, as
  Loot History does.

## Heads after PK-03 (pushed 2026-10-28)

| Repo | Head | Tests | luacheck |
|---|---|---|---|
| LibKa0s | 183bc57 | 3154 passed, 0 failed, 2 skipped | 0 / 0 |
| LootHistory | ca095c2 | 1830 passed, 0 failed, 1 skipped | 0 / 0 |
| LibKa0sSkinTester | 4540e17 | 534 passed, 0 failed, 1 skipped | 0 / 0 |

The in-game checks are in each addon's `docs/smoke-tests.md`: Loot History SKIN-1, SKIN-2, SKIN-7,
SKIN-23 and SKIN-27..38, plus PANEL-3 and PANEL-22; the Skin Tester PICKER-1..16, SHOW-13 and PANEL-3.
None is marked passed here.
