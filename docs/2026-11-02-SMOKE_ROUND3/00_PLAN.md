# Plan: the owner's third smoke round on the full skinning run

The owner's smoke feedback of 2026-11-02, after M4 of `docs/2026-11-01-SMOKE_FEEDBACK/` (that bundle is executed and stays as it is; its 06 file only gets Result cells filled). The work is on the existing, unmerged `feat/2026-11-01-full-skinning` in each repo. Images are `inputs/images/<n>.png`, numbered as the owner's message cites them. `items.tsv` holds every item.

## What the owner reported

1. **DpsRace (img 81, 82):** the Elapsed and Left clocks, the green and red numbers (not their labels), draw the same face in every skin. They must follow the skin's font. SG-DR-2 failed. The owner's profile stores no clock font (SavedVariables read 2026-11-02: `profiles.Default` holds only `skin.pickerSeen` and `skin.fullSkinReset`), so the defaults apply (`fontFromSkin = true`) and the cause is in code. The lead's hypothesis, unproven: `bigText` (modules/Hud_States.lua:157) calls `fs:SetFont` at creation, and that string-level font wins over the font object S.HudFont later sets with `SetFontObject`. The Damage and DPS figures and the spell rows also look unchanged in both images, so they are in scope if the same cause holds. Diagnose before fixing.
2. **AceGUI dropdowns (img 83, 84):** AceGUI Dropdown, Ka0sMedia_Font and Ka0sMedia_Statusbar do not take the skin's dropdown look.
3. **FadeNineSlice (img 85 to 87):** no border, invisible on dark skins. It needs a border in every skin, like MakeResizable's frame (img 93).
4. **IconBorder (img 88 to 92):** zoom the icon in more, 0.07 by default, so the original icon edge never shows; draw a 1 px outline in the skin's border color. Some skins draw 2 px (img 91, 92): it must be 1 px in every skin.
5. Everything else passed: mark every smoke check so far passed for every addon, except the checks these issues fail.

## Owner's rulings, 2026-11-02

- Dropdowns match the skinned Blizzard (WowStyle1) dropdown: a flat box in the skin's colors, the label left-aligned, one chevron in the skin's color, no gold button. The open list is skinned as well. The media pickers keep their font or texture preview inside the box. It follows the existing panel rules: the settings panel stays stock while Ignore settings panel is ticked.
- SF-DR-9 (LibKa0s#70) is deferred out of this run. #70 stays open with a note that says why: the live chart draws secret values, which the library's line chart cannot plot. The live chart and Results keep the column look. This does not block the merge.
- KickCD and MultiMeters get the Simulation step delay slider, the same setting and behavior as the other five sims. This closes the open call from round 2.
- Asked up front, with no further questions: the lead decides everything else.

## The lead's calls

- One new bundle, not more milestones on the executed one.
- FadeNineSlice and IconBorder are library primitives, so the fix lands in LibKa0s and reaches every caller. The border is always drawn, 1 px, in the skin's `bar.border` or the equivalent border token. A skin whose border token is none still gets a visible edge, its divider or text color at low alpha.
- The IconBorder zoom is a default that a caller's opts can override.
- Smoke results are recorded as "Passed (owner, 2026-11-02)" in the Result cells of both earlier bundles' 06 files (owner-reported, entered by the lead at the owner's word). The failed checks are recorded as "Failed (owner, 2026-11-02): re-opened as <id>". The per-addon `docs/smoke-tests.md` files are updated too, wherever they carry a result column.

## Order and checkpoints

- **M1 Library:** diagnose R3-DR-1 first, and if the cause is the library's, fix it there. Then R3-L1 to R3-L3 and the re-cut R3-REL of local tag v1.85.0, with a recorded release battery.
- **M2 Addons:** R3-RV re-vendor into the 16 addons, then R3-DR-1, R3-SIM-KC, R3-SIM-MM, R3-DEFER and R3-SMOKE.
- **M3 Final:** an independent review with two lenses, the fixes, a green loop across every repo, the new `06_SMOKE_TESTS.md` and `99_REPORT.md`, then a push of the branch and the review notes (never a tag).
- Afterwards, waiting for the owner: a combined smoke run, then the go-ahead to merge with `/dev-copilot:finalize`, push tag v1.85.0, and close LibKa0s #71 and #72 (spaced out; #70 stays open). After the merge, delete every branch, stash and worktree this run and its parents made.
