# Owner feedback on the adoption smoke (2026-11-19)

The owner ran every wave A–D smoke check and reported all of them passed. They then gave the feedback below, to be
addressed. It is kept verbatim. Screenshots `img-N.png` are in `screenshots/`, numbered as the owner attached them
(Image #N). Image #14 was not attached.

> All addons with an anchor strip like this [img-6]
> - Change the order to be [?][Settings][Close]
> - Reduce the gap between these three
> - Color of these (normal and hover) should match other HUD displays headers [img-7] [img-8] [img-9]
> - Tooltip for the anchor displays should be on top like in dropwatcher [img-10] rather than to the side as it currently is today [img-11]
>
> All addons with a HUD like this [img-12]
> - Mandatory - needs to have close, settings and lock icons, all others are upto the discretion of the addon.
> - All such icons need to be in the header, unless there is a stroing reason to have them in a footer
>   - e.g. [img-13] DropWatcher has 2 buttons in footer which makes sense because its not window control - it provides actions
>   - Flag all deviations and let me take a call one by one
>
> CombatTrail
> - [img-3] [img-4] [img-5] Bar texture doesnt seem to be uniformally applied - it should be the skins default texture by default - in several cases its not
> - Add a GH issue in LibKa0s to do an audit that all skin elements should be applied by default - unless I have explcitly asked you to override it - mark such cases in the audit
>
> SkillMaster
> - Add a drag resizer option for the Main Window, controlled by /sm lock or /sm unlock (lock icon)
>   - Do not resize the LDB tooltip
> - [img-19] Set waypoint when tomtom is installed doesnt set anything - pleaser fix this
>
> DropWatcher
> - [img-15] tooltips seem to be going beyond the roll campanion window, even when it doesnt need to
>   - Have the tooltip be flush to the main window, unless it would overalp with the roll companion window, in which case keep it where it is [img-16]
> - [img-17] For the roll popup companion window, have a small header which says Drop Wwatcher - no window controls needed (i.e. no x, gear, etc etc), same format and styling as the main dropwatcher window header [img-18]
>
> DpsRace
> - Is no longer an active addon, its merged into CombatTrail now. Remove it from ADDONS.md and everywhere else
> - Push all changes from DpsRace to master
>
> All addons
> - After this batch of changes is done, any Ka0s addon repo which doesnt have default branch as master, make teh default branch to master
>
> LibKa0s
> - Add a LibKa0s issue to add a fade for all windows/hud elements - configurable (time, duration) from every addons settings (General page, new window tab) with a reasonable defaults

## Owner rulings from the grilling (2026-11-19)

| Question | Ruling |
|---|---|
| Base branch | Merge the adoption run first (done 2026-11-19), then branch this run from master |
| Other sessions | Fold Drop Watcher's v1.106.0 branch (merged in the finalize). RangeMaster's session has since merged its branch, so RM is in scope |
| HUD scope | Primary persistent windows need close + settings + lock. Secondary windows need close only |
| DpsRace | Remove it from the roster and every live doc, and archive the GitHub repo. Keep the local checkout and the journal history. Frozen bundles stay as written |
| Strip marks | All three marks on every strip, as [?][settings][close]. Settings opens that display's settings. Close hides or disables the display and keeps its settings |
| Strip tooltip | Above the strip everywhere. The per-addon `tooltipPlace` hooks for strip tooltips are removed. Aura Master's aura tooltips stay client-placed (wave C option B) |
| Fade issue | Show/hide fade, filed as LibKa0s#98 |
| BankLedger, LootHistory | Add a header lock that toggles `settings.locked`, plus `/bl lock` and `/lh lock` |
| Skin Tester showroom | Waived: a dev tool with no lock |
| Outfitter Reborn outfit window | Waived: docked, nothing to lock |
| Quick Comms pads | Add settings, lock and close to every pad header. Close hides that pad, which can be restored |
| WhatGroup popup | Add a header lock and `/wg lock`. Keep the bottom Close button as a recorded deviation |
| Skill Master detached and group windows | Waived: the dock mark is the way back |
| PGF Extension filter panel | Waived: a docked child of PGF's dialog |
| Standard | Codify the HUD header rule, with waivers recorded in each addon's Documented deviations |

Issues filed: LibKa0s#97 (skin-defaults audit) and LibKa0s#98 (show/hide fade).
