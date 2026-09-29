# Smoke map — PartyFrameEnhanced (SP-PF-03)

Old `docs/smoke-tests.md` (at `09b8665`): 448 lines, 90 checks (steps 1-59, 27 lettered steps, T1-T4).
New: 553 lines, 94 checks in 13 themes. 0 dropped. The new file is longer, not shorter: it adds 4 new
PROFILE checks, splits the old step 20 into 3 (the `profile <name>` verb) and old step 37 into 2
(visibility and moves), and adds a `## Before you start` list, a `Result:` line on every check and a
33-row `## Pending sign-off` table. Merging duplicates
saved lines elsewhere. Coverage comes first (spec S4).

Where one old step now lives in several new checks, its row lists every new ID and says which part
went where.

| Old location | Behavior | New ID |
|---|---|---|
| A 1 | Fresh install, zero Lua errors, `[PFE]` prefix | INSTALL-1 |
| A 2 | `/reload` with no errors | INSTALL-2 |
| A 3 | The AddOn-list logo | INSTALL-3 |
| B 4 | Bare `/pfe` opens the panel; the help block with eighteen verbs; combat refusal | SLASH-1 (pending: the eighteenth verb, `diagnostics`, arrived in DR-PF-03 after the v0.1.0 pass saw seventeen); the in-combat half is COMBAT-1 |
| B 5 | `/partyframeenhanced` and `help` match `/pfe` | SLASH-2 |
| B 6 | `/pfe wibble` → unknown command, then help | SLASH-3 |
| B 7 | `/pfe version` | SLASH-4 (expects "the TOC version" now, not a hard-coded v1.1.0) |
| B 8 | `/pfe list` shape and colors | SLASH-5 |
| B 9 | `set`, `reset`, an invalid value | SLASH-6 (pending: owed as PF.10's `/pfe set castbar.width 150`, `/pfe reset castbar.width` after PF-11 put both verbs on the LibKa0s-Schema-1.0 seam; the reset echo `general.provider = auto` and the refusal `Invalid value for scale` / `expected a number` are quoted from libs/LibKa0s/Slash.lua CliReset, CliSet and STRINGS) |
| B 10 | `/pfe unlock` / `lock` line and the *Lock frame* checkbox | PREV-1 (merged with I 43; pending: PF.10 ticks and unticks every Master controls checkbox after PF-11 moved `locked` onto writeThrough; the lock line is quoted as `Elements locked`, settings/Slash.lua:126) |
| B 10a | Disable and enable, the live surface while disabled | STATE-1 |
| B 10b | Feature verbs refuse while disabled | STATE-2 |
| B 10c | The stand-down is total (no trace lines) | STATE-3 |
| B 10d | Minimap clicks and *Lock frame* while disabled | STATE-4 (also takes the disabled halves of K 54 and K 55) |
| B 10e | Re-enable reads the current settings | STATE-5 |
| B 10f | Target and pet frames through a stand-down, in and out of combat | STATE-6 |
| B 10g | Edit Mode through a stand-down | STATE-7 |
| B 10h | Fade frames and holders through a stand-down in combat | STATE-8 |
| C 11 | `/pfe config` landing page | PANEL-1 |
| C 12 | General → Master controls layout, no Test mode, visibility dropdown | PANEL-2 (the old step's "two-tab strip" is corrected to the three tabs the page registers: Master controls, Party frames, Health updates; pending as corrected); "unticking *Lock frame* starts preview" is PREV-1; "combat re-ticks it" is COMBAT-3 |
| C 13 | General → Party frames tab | PANEL-3 (corrected: it also lists *Fade with party frames*, the row 402312a added after the v0.1.0 pass; pending) |
| C 14 | Defaults button style | PANEL-4 |
| C 15 | `/pfe config` refused in combat | COMBAT-1 (merged with the combat halves of B 4 and K 54) |
| C 16 | The combat lock cover | COMBAT-2 |
| D 17 | Profiles page renders | PROFILE-1 |
| D 18 | Page Defaults, one `[Set]` line | PANEL-5 (pending: owed as PF.10's "Defaults on one page"; after PF-11 the `[Set] reset general: 2 rows` line comes from libs/LibKa0s/Schema.lua:677, BulkEnd, which counts only the rows the act changed) |
| D 19 | Reset all settings popup and scope; `/pfe resetall` | PROFILE-10 (corrected: the tooltip reads `Profiles -> Reset Profile` with an ASCII arrow, LibKa0s Options.lua `RESET_ALL_TIP_PROFILES_PAGE`, not the old step's `→`; pending) |
| D 20 | `/pfe profile` list, `profile new Test`, `profile use Default` | PROFILE-2 (`new`; pending, since it now quotes the `Created and switched to new profile 'Test'` line), PROFILE-3 (the list), PROFILE-4 (the switch, by name and by `use`) |
| D 20a | Profile sub-verbs refuse bad names | PROFILE-9; the `profile use Typo` part is PROFILE-5 |
| E 21 | Debug console opens and closes | DIAG-1 |
| E 22 | The `[Init]` line; logging is session-only | DIAG-2 (expects "the TOC version" now) |
| E 23 | The perf walk | DIAG-3 |
| E 23a | The perf capture worth recording | DIAG-4 |
| E 23b | Diagnostics appends, ungated | DIAG-5 |
| E 23c | Copy; the long-alias diagnostics forms | DIAG-6 |
| E 23d | Diagnostics in combat, in a dungeon, and while disabled | DIAG-7 |
| E 23e | No `diag` short name | DIAG-8 |
| E 23f | The 3000-line buffer cap | DIAG-9 |
| F preamble | Run each cast-bar step on the three frame systems | `## Before you start` (not a check) |
| F 24 | Cast bar attached over each member's frame | CAST-1 |
| F 25 | Your own row; classic has none unless free placement | CAST-2 |
| F 26 | Channels drain | CAST-3 |
| F 27 | Interrupt color, the client's word, the hold and fade | CAST-4 (the German word is LOC-3) |
| F 28 | Uninterruptible fill and shield; no error on the secret flag | CAST-5 |
| F 29 | Frame-system switch with EllesmereUI loaded | CAST-6 |
| F 30 | Cast bars follow a re-sort in combat | COMBAT-6 (merged with G 38) |
| F 31 | Cast Bars page tabs and live restyle | CAST-7 (pending: *Cast color* is a color swatch, the check PF.10's "Drag a colour picker" lands on after PF-11) |
| F 31a | Size & Position shows only the block that applies, on three pages | PANEL-6 |
| G 32 | Target frame beside each member | UNIT-1 |
| G 33 | Target health moves; no secret errors | UNIT-2 |
| G 34 | Reaction colors and class color on target frames | UNIT-6 (merged with H 41) |
| G 34a | A new member's target fills in | UNIT-3 |
| G 35 | Raid marker on a target frame | UNIT-7 |
| G 35a | Marker placement controls | UNIT-8 |
| G 35c | Marker above the border, both pages | UNIT-9 |
| G 35d | Pet raid marker, and its placement controls | UNIT-7 (the marker) and UNIT-8 (the placement) |
| G 35b | Health updates off, targets | UNIT-10 (merged with H 42a; the unresolved-target repaint allowance is pending) |
| G 36 | Click to target; untick passes through; tick in combat applies after | UNIT-11; the in-combat tick is COMBAT-7, now through `/pfe set target.clickToTarget` (the combat lock, 996570f, refuses the panel's checkbox in combat) |
| G 36a | Click to target toggled back within one combat | COMBAT-7 (the untick and re-tick now go through `/pfe set target.clickToTarget false` / `true`) |
| G 37 | Visibility change and free-placement moves in combat | COMBAT-5 (visibility, now through `/pfe set visibility`: set before the pull so the driver's `[combat]` clause is what hides the frames, then an in-combat change that queues the driver write) and COMBAT-8 (moves: free placement, unlock, pull, then drag a target frame in combat) |
| G 38 | Target frames through a re-sort in combat, secure queue | COMBAT-6 |
| H 39 | A pet frame appears, dismiss, resummon | UNIT-4 |
| H 40 | Your own pet | UNIT-5 |
| H 41 | Pet takes the owner's class color | UNIT-6 |
| H 42 | Click a pet frame to target it | UNIT-11 |
| H 42a | Health updates off, pets | UNIT-10 |
| I 43 | Unlock shows placeholders; lock clears them | PREV-1 |
| I 44 | `/pfe unlock` refused in combat | COMBAT-4 (merged with J 52's combat half and K 55's combat half) |
| I 45 | Free-placement drag, persist, reset position | PREV-3 |
| I 46 | Preview in a party uses the real frames | PREV-2 |
| I 47 | `/pfe status` | PREV-4 |
| I 47a | Range fade, EllesmereUI | FADE-1 |
| I 47b | Range fade, Blizzard raid-style, in an instance | FADE-2 |
| I 47c | Range fade, Blizzard classic | FADE-3 |
| I 47d | Fade switch off; preview at full opacity; mid-combat reshuffle | FADE-4; the reshuffle clause is COMBAT-6 (both pending) |
| J 48 | Party-only rule | PREV-5 |
| J 49 | Stand-in, EllesmereUI, and the `[Preview]` size source | PREV-6 |
| J 50 | Stand-in, Blizzard raid-style | PREV-7 |
| J 51 | Stand-in, Blizzard classic | PREV-8 |
| J 52 | Live switch to and from a party; combat re-lock; unlock refused in combat; disable while unlocked; status while unlocked | PREV-9 (the switch and the status text), COMBAT-3 (the re-lock; pending, owed as Q.10 after PF-09 moved preview's combat listener), COMBAT-4 (the refusal), STATE-9 (disable while unlocked; pending, since it adds "no placeholder or stand-in is left on screen") |
| K 53 | Minimap button logo, status tooltip in three states, drag persists | LAUNCH-1 (logo, drag), LAUNCH-2 (tooltip) |
| K 54 | Left-click opens settings in every state; combat refusal | LAUNCH-3; the disabled half is STATE-4; the combat half is COMBAT-1 (pending: M6 made left-click open settings, so its in-combat refusal is new) |
| K 55 | Right-click options menu; its Locked and Enabled entries | LAUNCH-4; the grayed entry while disabled is STATE-4; the combat refusal is COMBAT-4 (pending: the menu is new in M6) |
| K 56 | The broker plugin is the same object | LAUNCH-5 (pending: M6 rewrote its right-click) |
| K 57 | The Minimap button row from the panel and the CLI; SavedVariables shape | LAUNCH-6 (corrected: the get and set echo `global.minimap.shown = <value>`, the old path answers `Setting not found: global.minimap.hide`, and the file holds `["hide"] = true`) |
| K 58 | The button is account-wide across profiles and characters | LAUNCH-7 (switches with `/pfe profile Test`, or `Default` when on Test, not `profile new smoke`; pending, since the switch now runs through the new verb) |
| K 59 | The button survives both resets; `/pfe reset global.minimap.shown` | LAUNCH-8 (pending whole: the both-resets half is owed as PF.10 after PF-11, and the `reset global.minimap.shown` clause is PF-13) |
| T lead list | Localized touchpoints, enumerated | kept as the lead list of `## Non-English client` (not a check) |
| T1 | Load on deDE | LOC-1 |
| T2 | Class colors from the token on deDE | LOC-2 (the old "covered headlessly once its case exists" note is replaced: the case exists, but its mock returns the token for both values, so the client stays the witness) |
| T3 | Spell names and the stop word on deDE | LOC-3 |
| T4 | Frame-system detection on deDE | LOC-4 |
| T closing note | Which T steps may be signed off on English | folded into LOC-1, LOC-4 and `## Before you start` (not a check) |
| Completion record | The v0.1.0 full-pass row (2026-09-18) | dropped: a filled-in historical sign-off record (D4); git keeps it, and `## Pending sign-off` names it as the last full pass |
| Index | Section → coverage → client table | replaced by the new `## Index` (not a check) |

New checks with no old step: PROFILE-6 (quotes and spaces), PROFILE-7 (while disabled), PROFILE-8 (in
combat) and most of PROFILE-5 (unknown name, did-you-mean). All four sit under Pending sign-off with
PROFILE-3 and PROFILE-4.

Pending sign-off, rebuilt in SP-PF-03R to the clarified S4 policy (2026-09-29). It lists (a) every
old check with no recorded pass for its current expectation, including checks a Ka0sAddonsCommonTasks
smoke list owes and nobody ran, and (b) every check new in this run or corrected against the code in
it. The old doc had no `Result:` lines. The passes on record are the v0.1.0 full pass (2026-09-18,
65ca753), `2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/06_SMOKE_TESTS.md` X1.4 (the minimap
button after M6: left-click, right-click menu, tooltip, all out of combat; PASS 2026-09-25) and
`2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` PF-S1 to PF-S11 (DIAG-5 to DIAG-9; PASS 2026-09-26).
That plan's Session PF (PF.1 to PF.12) and its Q.10 have no recorded result, and the plan's checkpoint
lists them as owed.

- (a), changed after the last pass: SLASH-1 (`diagnostics`, DR-PF-03), STATE-4 (PF-07), STATE-6
  (PF-04), STATE-7 (PF-05), STATE-8 (PF-06), PANEL-6 (ea6f8ff), PROFILE-9 (PF-01), UNIT-3 (b6eb1dd),
  UNIT-7 to UNIT-9 (f104e43), UNIT-10 (b6eb1dd, 49 minutes after the 65ca753 sign-off), FADE-1 to
  FADE-4 (402312a), LAUNCH-5 (M6 8263238), LAUNCH-6 (PF-13 ac00e34), COMBAT-1 (the left-click in
  combat, M6), COMBAT-2 (996570f), COMBAT-4 (the menu's *Locked* in combat, M6), COMBAT-5, COMBAT-6
  (402312a), COMBAT-7 (PF-03) and COMBAT-8.
- (a), owed by a plan and never run, with an unchanged expectation: LAUNCH-8 (PF.10 re-checks both
  resets after PF-11; PF-13 added the `reset global.minimap.shown` clause), PANEL-5 (PF.10's "Defaults
  on one page"; the `[Set] reset general: 2 rows` line is now libs/LibKa0s/Schema.lua:677's), SLASH-6
  (PF.10's `/pfe set castbar.width 150` and `/pfe reset castbar.width`, now through the adopted
  seam), PREV-1 (PF.10 ticks and unticks every Master controls checkbox, *Lock frame* included, which
  PF-11 moved onto writeThrough {enabled, locked}), CAST-7 (PF.10's color picker drag: *Cast color*)
  and COMBAT-3 (Q.10 re-checks
  `Locked — combat started` after PF-09 moved preview's `PLAYER_REGEN_DISABLED` listener into
  modules/Preview.lua `listen`). PF.3, PF.5 to PF.9, PF.1, PF.2 and PF.12 fall on checks already listed, and so do PF.10's Reset
  all settings (PROFILE-10) and its *Minimap button* checkbox (LAUNCH-6). PF.10's *Enable* and *Debug
  console* checkboxes have no check in the old doc or the new one (STATE-1 drives enable through the
  verbs), so no row carries them.
- (b), new or corrected in this run (SLASH-6's reset echo and refusal lines and PREV-1's `Elements
  locked` line are quoted for the first time in SP-PF-03R, on checks already pending under (a)):
  PROFILE-2 (the quoted `Created and switched` line), PROFILE-3 to
  PROFILE-8 (the verb), PANEL-2 (three tabs), PANEL-3 (the fade row), PROFILE-10 (the `->` arrow),
  STATE-9 (the no-placeholder clause), LAUNCH-6 (the echo and `Setting not found` lines), LAUNCH-7 (the
  switch through the new verb), and COMBAT-5, COMBAT-7 and COMBAT-8 (steps rewritten because the combat
  lock refuses the panel in combat).

Not pending, with reasons: SLASH-4 and DIAG-2 name "the TOC version" where the old steps hard-coded
v0.1.0 and then v1.1.0; the expectation (the version the TOC declares) is unchanged. LAUNCH-2 to
LAUNCH-4 passed in X1.4. DIAG-5 to DIAG-9 passed as PF-S1 to PF-S11. PF.13 (the standing full pass
before a release) names no checks, so it does not make the whole suite pending. PF.4 and PF.11 check
behavior the old doc never covered.

Expected strings re-verified against the code in SP-PF-03R: the Slash, profile, launcher, combat-lock,
preview, status, diagnostics and debug lines (settings/Slash.lua, core/PartyFrameEnhanced.lua,
core/DebugLogSetup.lua, modules/Preview.lua, modules/Diagnostics.lua, and libs/LibKa0s Slash.lua,
Launcher.lua, Options.lua, OptionsCompose.lua, Schema.lua, DebugLogDiagnostics.lua). The second SP-PF-03R pass also checked SLASH-6
(libs/LibKa0s/Slash.lua CliSet, CliReset, `INVALID`, `ERR_NUMBER`), PANEL-5 (libs/LibKa0s/Schema.lua
BulkEnd; Options.lua RestoreDefaults brackets act `reset`, scope `general`; the Debug console row has no
default, so the page reset never touches it) and PREV-1 (settings/Slash.lua:126). Three did not
match and were fixed: PROFILE-10's tooltip arrow, LAUNCH-6's `/pfe get` echo and `Setting not found:
<path>` line, and LAUNCH-6's SavedVariables shape.

Inbound references updated: `docs/debug.md:164` (steps 21 to 23f → DIAG-1 to DIAG-9),
`docs/ARCHITECTURE.md:341` and `docs/midnight-quirks.md:90` (step 47b → FADE-2), and
`docs/ARCHITECTURE.md:386` (the doc-table row names the `## Non-English client` section). There were no
`ConsumableMaster § 3c` or `KickCD § 9b` citations in this repo. No test reads `docs/smoke-tests.md`.
