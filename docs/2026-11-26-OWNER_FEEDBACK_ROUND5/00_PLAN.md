# Owner feedback round 5 (2026-11-26)

The owner's feedback after the round 4 and SkillMaster windows merges: a Lua error that was still happening, and
feedback on SkillMaster, Drop Watcher, RangeMaster and Combat Trail. Screenshots are in `inputs/` under the owner's
numbers. Image 5 duplicates image 4; the `/sm probe` output arrived later as text and is condensed in
`inputs/SM_PROBE_2026-11-26.md`. Later messages: "Combat sequence also doesnt differentiate between player and
pet", and three more C stack overflows from a merchant scan (AlreadyKnown → SetHyperlink, with Drop Watcher,
ItemTree and SkillUpForever on top).

The owner's standing guidelines apply ([owner-run-guidelines]): decide yourself, checkpoint the plan, work on
branches with incremental commits, push feature branches at milestones, merge only on the go-ahead, and delete
branches and scratch clones after the merge.

Branch `feat/2026-11-26-owner-feedback-round5` in each repo touched. All four addons are built in clones under
`~/ka0s-scratch/r5/`. The live DropWatcher folder stays on the branch at the crash fix (R5-DW-00), so the owner can
test that now without half-finished builds landing under `/reload`. The green gate is each repo's own `CLAUDE.md`.

## M0: the crash (done before this plan was written)

**R5-DW-00.** Cause, read off the first stack: Drop Watcher's Item tooltip post call computes the verdict, the
verdict reads Pawn (`Compat.PawnItemValue` → `PawnGetItemData`), and Pawn fills its hidden `PawnPrivateTooltip1`
with `SetHyperlink`. That fill runs every Item post call again, Drop Watcher's included, so the loop goes round
until the C stack overflows. The deepest post call takes the blame, which is why ItemTree, SkillUpForever and
Drop Watcher all show up. The merchant-scan stacks (AlreadyKnown) are the same loop entered from a different
tooltip. Fix: a re-entry guard on `IST.OnTooltip` (pcall, so an error releases it), with a red-then-green test
that models Pawn's nested fill. Commit `ebd701f` (DropWatcher), pushed.

## M1: the builds (one builder per repo, in parallel)

### SkillMaster

| id | item | lead call |
|---|---|---|
| R5-SM-01 | Remove the hint tooltip ("Fold this section in the tooltip" / "Unfold") on collapsible headers | Removed in the LDB tooltip **and** the windows (images 1 and 4 show both). The chevron says it. |
| R5-SM-02 | A click anywhere on a collapsible header folds and unfolds it, in the LDB tooltip and in every window | The whole header row is the hit area, at every depth (Statistics nests). |
| R5-SM-03 | A pin icon next to each row pinned to a broker's title | Shown in the windows and in the LDB tooltip. A small pin glyph at a fixed spot (not one that moves with the text). |
| R5-SM-04 | More relevant icons for the six display brokers | Each family gets an icon that says what it is (professions, character stats, currencies, reputations, skills, statistics), from textures on both clients. The addon's own control broker keeps the Ka0s logo. |
| R5-SM-05 | `/sm toggle` → `/sm professions`; `/sm toggle` opens all windows | `/sm professions` toggles the Professions window. `/sm toggle` hides all six windows if any is shown, otherwise shows all six. The keybinding stays on Professions and is relabeled to match. Help, README and docs follow. |
| R5-SM-06 | The probe: every profession comes back twice (parent line + child line with `parentSkillLineID`) | Check that no window or tooltip lists a profession twice; if one does, fix it with a test built from the probe's rows. |
| R5-SM-07 | No Lua errors with all six windows open while playing | Covered by owner smoke. The builder exercises open-all → play → close-all headless and fixes anything it finds. |

### Drop Watcher (Item Search tooltip, window, verdict panel)

| id | item | lead call |
|---|---|---|
| R5-DW-01 | The badge overlaps the "Drop Watcher" label (image 9) | Fix the width reserved for the badge so the label never runs under it, at any UI scale. |
| R5-DW-02 | The badge looks shabby next to ItemTree's: colors, rough edges, font, font colors | Redesign it as one rounded pill like ItemTree's: smooth (no stepped or jagged corners), verdict-colored fill, readable dark text in a clean font, lock/coin icon, the score in the same pill. The tooltip and the verdict panel share it. |
| R5-DW-03 | Verdict panel: quests you can pick up show a count, not the quest | "Quests you could pick up (N)", like the recipe line. |
| R5-DW-04 | Color +xx and -xx | Positive green, negative red, zero muted. |
| R5-DW-05 | Remove the Score row | It's already in the badge. |
| R5-DW-06 | "Keep from 50" — what does it mean? | The builder finds out what it is (the threshold line, by the look of it) and replaces it with plain words, or drops it if the (?) tooltip covers it. The meaning goes in the execution record so the owner gets an answer. |
| R5-DW-07 | A (?) icon next to the score with a tooltip that explains scoring | Explains what adds and what subtracts, the verdict bands (Keep / Hold / Sell / Toss) and their thresholds, and the confidence rule, read from the scorer's own constants (never hand-copied numbers). |
| R5-DW-08 | Skill breakpoints: start at the bracketed [X] and show only the ones to its right | "[1] 55 75 95" stays; "1 20 20 [20]" becomes "[20]". Applies to the tooltip and the window's Skill column. |
| R5-DW-09 | Always show the crafting profession (e.g. Cooking) | Every crafting row names its profession, mixed or not. |
| R5-DW-10 | Crafting rows look tabular: fixed slots for the skill-up arrow, recipe name, skill-up and profession | Arrow and name left-aligned; breakpoints and profession right-aligned in their own fixed columns. In the tooltip, that means font strings of the tooltip's own, anchored like the badge (never measured mid-fill). |
| R5-DW-11 | "Sells for 30" — 30 what? | Money with gold, silver and copper icons (the client's coin text), wherever a reason or row shows money. |

### RangeMaster (band set picker)

| id | item | lead call |
|---|---|---|
| R5-RM-01 | Category headers in the band set dropdown are easier to see | Larger font and a band of background color behind each header. Not selectable. |
| R5-RM-02 | Your band sets that came from a class preset take that class's color | From the set's recorded source preset; a set with no class source stays plain. |
| R5-RM-03 | Shipped general presets get their own non-class colors | A fixed palette that is clearly none of the class colors. |
| R5-RM-04 | Healer appears under "Your band sets" for a level 11 Retribution Paladin | Only the class's set may be auto-created. The builder finds why Healer was created and fixes it. A migration removes an auto-created set only when it can prove the set was seeded and never edited or picked by hand; otherwise it leaves the set alone and records why. |

### Combat Trail

| id | item | lead call |
|---|---|---|
| R5-CT-01 | Default HUD shows 5 spell breakdown rows and 4 combat sequence rows; it should be 5 and 5 | The default height fits 5 and 5 exactly. |
| R5-CT-02 | Changing "Rows shown" doesn't resize the window | Changing the setting resizes it at once, and wins over a size dragged earlier. Dragging still resizes until the setting changes again. |
| R5-CT-03 | Combat Sequence doesn't track buffs and debuffs gained and lost (image 22: only CAST rows, with the Buffs and Debuffs chips on) | Find out why on WoW Forever (the event, its arguments, the filter, the sample data) and fix it with a test from a recorded event shape. |
| R5-CT-04 | Combat Sequence doesn't tell player rows from pet rows | Pet rows carry the pet marker the spell breakdown uses (the paw) and the pet's color. |

## M2: review and fix

One independent review per repo after its build; findings are fixed as `R5-REV:` commits. Branches pushed.

## M3: hand-off

`EXECUTION_RECORD.md` with what was built, the owner's answer about "Keep from 50", and the smoke list. Merge on
the owner's go-ahead only.
