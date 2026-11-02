# Addendum: DpsRace defaults (owner, 2026-11-03, mid-run)

- **Report:** the window no longer shows by itself near a training dummy. The lead read the SavedVariables (written 2026-11-03 00:33). `profiles.Default`, shared by all four characters, holds only `skin.pickerSeen` and `skin.fullSkinReset`. So `hud.autoShow` reads its default, `false`: it has been opt-in since TA-D1 (4a88dca, 2026-10-28). `lastLength` is also missing, and DpsRace.lua.bak from 2026-11-02 11:00 is the same, so the profile was reset to defaults. The only whole-profile wipe in the code is the settings Reset (settings/OptionsSetup.lua:31). No run code changed either setting.
- **Ruling:** `hud.autoShow` defaults to **true**. `race.autoArm` stays opt-in. The owner's reset profile picks this up through the defaults, so no migration is needed.
- **Ruling:** a new profile's race length (`race.defaultLength`) is **60 s**, not 120.

Items R3-DR-2 (length) and R3-DR-3 (auto-show), in the DpsRace stage with R3-DR-1.
