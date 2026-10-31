# M2: library release v1.84.0 (addendum)

Owner, 2026-10-31: address the file length rulings and those near the cap, and LibKa0s issues #69, #68, #67, #66, #59. #65 (skin editor) stays open by ruling. #44, #6, #5, #3 are out of scope.

Runs after M1 and the DpsRace bar work land. One release carries all library changes, so addons re-vendor once. Same branch name in every repo; tag v1.84.0 stays local until the go-ahead. This supersedes the v1.83.1 mentioned in chat.

Order:

1. **Peels, pure moves:** rows with a spent ruling (`Skin.lua`, `SkinDefs.lua`, `SimPanel.lua`, the two test files) and payload files at 1400 lines or more (`OptionsSkinPicker.lua`, `OptionsIds.lua`, `testkit/mock_base.lua`). #59 also names the flow-engine peel of `OptionsWidgets.lua` and the tabbed-page peel of `OptionsTabs.lua`, so those two go too.
2. **#59:** `afterSubgroup` and before-group seams, schema `note` row, Position-block composer, `PageBanner{ acts }`.
3. **#69:** measure the real Friz at `Interface/AddOns/DialogueUI/Fonts/frizqt__.ttf`, hash checked against Prototype, retune WoW Default, add it to the width guard. The owner's smoke needs a client without the font replacement.
4. **#66:** Charts module from DpsRace's port. LootHistory and DpsRace adopt it; the deviation row goes.
5. **#68:** code pass over every mover with computed widths per skin; fix what is short. The in-client sweep and screenshots stay the owner's, so the issue stays open until then.
6. **#67:** sweep the roster; KickCD `settings/Icons.lua` is the known candidate. Update the options-ui §22 pointer in WowAddonStandards.
7. Re-vendor v1.84.0 into all 16 consumers, gates, review, recorded runs, push branches. Close no issue before merge.
