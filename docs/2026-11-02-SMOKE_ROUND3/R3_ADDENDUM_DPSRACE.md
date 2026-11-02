# Addendum: DpsRace defaults (owner, 2026-11-03, mid-run)

- **Report:** the window no longer shows by itself near a training dummy. The lead read the SavedVariables (written 2026-11-03 00:33). `profiles.Default`, shared by all four characters, holds only `skin.pickerSeen` and `skin.fullSkinReset`. So `hud.autoShow` reads its default, `false`: it has been opt-in since TA-D1 (4a88dca, 2026-10-28). `lastLength` is also missing, and DpsRace.lua.bak from 2026-11-02 11:00 is the same, so the profile was reset to defaults. The only whole-profile wipe in the code is the settings Reset (settings/OptionsSetup.lua:31). No run code changed either setting.
- **Ruling:** `hud.autoShow` defaults to **true**. `race.autoArm` stays opt-in. The owner's reset profile picks this up through the defaults, so no migration is needed.
- **Ruling:** a new profile's race length (`race.defaultLength`) is **60 s**, not 120.

Items R3-DR-2 (length) and R3-DR-3 (auto-show), in the DpsRace stage with R3-DR-1.

## R3-DR-4: "Your best" target card on the idle screen (owner, 2026-11-03 00:45, image 101)

Owner's ask: on the idle race screen (length buttons, Target card, Arm Race), show the current best for that duration and target type as the target to beat. The owner approved the lead's mockup, "Build as mocked":

- **Section** "Your best · <spec> · <category> · <length>", in the skin's label color, between the Target card and Arm Race.
- **Card:** the best's DPS as the big figure (HUD font) and its damage on the right (dim). Line two: date · ilvl · top spell (dim, truncated).
- **Arm Race** reads "Arm Race · beat <DPS>" while a best exists.
- **Empty state:** "No race yet: this one sets the mark." With no target: "Target a dummy to see your best."
- **Data:** the existing bests board, keyed spec | target category | length (modules/Bests.lua:32), the same best the live chart's pace and the result delta read. Flagged runs never count. Nothing new is stored.
- **Live:** it swaps at once on a length button, Custom, a new target or a spec change, and when the board invalidates.
- **Hover:** a tooltip with the full run (date, length, damage, DPS, top 3 spells). **Click:** opens Results on that run.
- **Skinned:** every element through the library, like the Target card. It fits the window's current width, and none of the existing layout moves.

## R3-DR-5: Compare bars as bright as the runs table's (owner, 2026-11-03 00:48, images 103, 104)

Owner's ask: the bars in the Results compare view (image 103: the This run column's blue and the Runner-up column's gold, behind each figure) are far too dim. Make them as bright as the run list's bars (image 104), keeping each bar's own tint. The lead's reading: raise the fill's alpha and brightness to the run list's values under the same skin, through the same skin token or alpha path, and leave the hue alone. It must hold in every skin, and the numbers on the bars stay readable (check the contrast of text on a bright fill).
