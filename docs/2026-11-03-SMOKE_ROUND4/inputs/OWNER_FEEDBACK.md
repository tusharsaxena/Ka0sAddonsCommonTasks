# Owner feedback, 2026-11-03 (after smoke round 3)

Verbatim, with image numbers as pasted. Images are in `images/<n>.png`.

1. For all dropdowns, across all addons, clicking outside of the dropdown should close an opened dropdown
   - [Image #1] It works for DropDown and WowStyle1Dropdown, but not the other 3
2. [Image #2] [Image #3] For these 3 in skin tester, show these as if they are out of the settings panel
   - in fact, dont need to make any code changes - for the skin tester addon ONLY, set ignore settings panel = off - treat this as an accepted deviation if needed
3. [Image #4] [Image #5] [Image #7] [Image #6] This element seems broken (misaligned) across all skins. Where is this actually being used?
   - first two screenshots are with ignore settings panel = ON; last two are with it OFF
4. [Image #8] Give Ka0s Default a slightly visually distinct header (dark shade of yellow or grey - latter like Obsidian) - to make it stand out a bit more like other skins [Image #9] [Image #10]
   - in fact show me a UX mockup of all skins with header and main elements only; so i can visually compare and sign off
5. DPS Race
   - [Image #11] [Image #12] make all these blocks central aligned horizontally
   - [Image #13] Fix spacing between the target block and Your best block - should be consistent spacing between all blocks. Block = label + box(es) combo. Add a little EXTRA spacing above ARM RACE
   - [Image #14] Just call this "Your best"
   - [Image #15] Remove top damaging ability, put consumables used instead (blank if none used)
   - [Image #16] Label just as "Arm Race" - remove the beat xxx
   - [Image #17] /dr sim Add more damage events between race start and buzzer (e.g. model it like MultiMeters where the Pull Trash and Pull Speaker steps actually have lots of events inside it [Image #18])
     - For both DPS Race and MultiMeters - the core steps where lots of damage happens, make those steps last about 10s each (e.g. pull trash and pull speaker in Multi Meters sim; and new step between race starts and buzzer in DPS race sim)
6. Icon Borders
   - Ka0s Default [Image #19] Glass [Image #20] dont have proper icon borders - good counter example is Obsidian [Image #21]
   - [Image #22] IconBorder appears twice in SkinTester - remove the bottom one next to Waiting for the pull box
