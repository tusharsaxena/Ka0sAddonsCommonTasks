# Owner feedback, round 5 (2026-11-03, verbatim)

Images are in `images/` and keep the owner's numbers (31 to 56). The owner used the number 6 twice. This bundle calls
the second one 6b.

Some uber feedback about the skins

1. [Image #31] [Image #32] [Image #38] [Image #39] [Image #44] LootHistory, BankLedger, DropWatcher, WhatGroup look fantastic, looks how i wanted it to be.
   - Small change is to make the header a bit darker
2. [Image #33] MultiMeters doesnt look that great though
   - seems like there is an "inner border" of sorts which sits between the main window and the window edge which shows up as a black strip
   - change this so it looks just like LootHistory
   - make this the same for all addon windows (do a sweep across all Ka0s addons)
3. [Image #34] [Image #35] [Image #36] [Image #37] DPS Race doesnt seem to have the header at all, in any skin
   - Fix this
   - Also make it consistent with the feedback for #2 (i.e. the border and gape between window edge and border should be more like LootHistory)
3a. [Image #45] Make the Dps Race header text left aligned
4. [Image #40] [Image #41] QucikComsm dial does not have the header element at all
   - add it please
   - Also make it consistent with the feedback for #2 (i.e. the border and gape between window edge and
  border should be more like LootHistory)
5. [Image #43] [Image #42] PGFE works and skin looks great; however the header text please align the vertical center of the text with the vertical center of the expand/collapse arrow (both should be centered in the header)
   - In fact this vertical centering of text/glyphs/other elements the header should be done for all addon windows for all skins
6. [Image #46] In the /st skin window openeing the first dropdown and clicking outside of it doesnt close it. Clicking on the dropdown main element [Image #47] again does close it however
   - Check this for all addons
   - This functionality seems to work for all dropdowns in the SkinTester addon though [Image #48] - so not sure why its not working here
6. (6b) /dr sim starts like this [Image #49] - on step 2 already with a resume button
   - [Image #50] it should be more like this with a start button and a scenario drop down
   - it also zooms through the run - even the last 10s countdown is super fast
7. Icons sometimes still have the rough edges and no border
  - DPS Race [Image #51] [Image #52]
  - DropWatcher seems better but not 100% correct? [Image #53] [Image #54] [Image #55] [Image #56] - plz check and validate

Grill me if you have any questions that need to be resolved

## Execution guidelines (owner, verbatim)

- If you have any questions, ask me upfront
- After that, use your best judgement and take any decisions you feel you can take. Ask me only when absolutely necessary.
- Create a resumable and checkpointed plan for this change.
- Work in a branch and commit incrementally.
- Push to origin after major milestones, but do not merge without my go-ahead.
- At the end of the run, after everything is merged, delete all branches, stashes and worktrees created as part of this run
- Use ultracode to spawn dynamic workflows.
