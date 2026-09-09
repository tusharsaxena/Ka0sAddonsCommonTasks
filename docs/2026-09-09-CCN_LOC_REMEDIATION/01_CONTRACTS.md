# The contract each refactor must not break

Written by the Phase 1a characterization wave, one section per file, from reading the
warned functions and the comments around them. `performance-§11` forbids a complexity
refactor from changing behaviour; this is what "behaviour" means for each of these files,
in the words of the agent that pinned it. Every claim here is now backed by a test that was
run against the UNREFACTORED code.


---

## `core/Database.lua`

### Tests added (12)

- Database v2: the widening uses the window's OWN padding, not the template's
- Database v2: a frame with no numeric width is given one, and every window gets its own
- Database v5: a stored false and a stored 0 are lifted, not read as unset
- Database v5: only the key the window actually carried is lifted
- Database v5: only the FIRST window is consulted, even when it carries neither key
- Database v5: a first window whose data block is not a table lifts nothing
- Database v5: EVERY profile lifts from its OWN first window
- Database: v12 -> v13 keeps the rest of an existing header block
- Database: v12 -> v13 overwrites a control colour mode that was already there
- Database: v12 -> v13 maps each control flag on its own
- Database: v12 -> v13 leaves a window with no frame block at all alone
- Database: v12 -> v13 walks every saved profile, not just the active one

### What must not change

Behaviours a refactor of core/Database.lua must not change, now pinned:

migrations[1]. `pad = frame.padding or defaultPad`, and `defaultPad` itself falls back through `((template.frame or {}).padding) or 6` — the stored padding is counted on BOTH edges. `needed` is computed inside the per-window loop from that window's own `#columns`, so it must not be hoisted (a window with no columns array is sized for zero columns). The width is replaced when `type(frame.width) ~= "number"` OR when it is smaller than needed — never narrowed, so the type test cannot be dropped in favour of the `<` alone. The width loop skips a non-table column entry, but the arithmetic counts the raw array length including junk; a refactor that filters before measuring changes the width a hand-edited profile lands on. Only `col.width` is written; nothing else in a column is touched. Ends at schemaVersion = 2.

migrations[4]. The lift reads `windows[1]` ONLY — not "the first window with an opinion". A first window with no usable `data` (absent, or a non-table) lifts nothing even when a later window carries values. The two keys are lifted independently (`~= nil` per key), so a window that set one must not drag the other along. `~= nil`, never truthiness: a stored `mergePets = false` and `throttle = 0` are lifted over whatever AceDB merged into `profile.data` — this is deliberately the OPPOSITE rule from EnsureWindowShape's `== nil`, because before v5 nothing read the profile-level address. `lifted = type(profile.data) == "table" and profile.data or {}` must keep creating a table for a profile that has none. The prune over every window sits OUTSIDE the lift guard and runs whether or not anything was lifted. Every profile from allProfiles lifts from its own first window. Ends at schemaVersion = 5.

migrations[12]. `header.show` is written only when `frame.titleBar ~= nil`; an absent key stays absent so the merge decides. When the header block exists it is mutated in place (`w.header.show = ...`), never replaced — fonts, colours and heights on it must survive — and the moved value OVERWRITES an existing `header.show`. `frame.titleBar` is pruned. The two control flags are read and written separately (base and hover), true -> "class" and false -> "custom", and unlike migrations[6] there is NO `== nil` guard: an existing `controlColorMode` / `controlHoverColorMode` is overwritten, which a shared boolean-to-mode helper folding steps 6 and 12 together would silently change. `type(frame) == "table"` guards both halves. Every saved profile is walked. Ends at schemaVersion = 13.

Shared: allProfiles must keep reaching db.sv.profiles (the account-wide schemaVersion means an inactive profile gets exactly one chance), and RunMigrations must keep bumping to CURRENT_DB_VERSION rather than spinning when a step is missing, then run SeedWindows unconditionally after the walk.

### Risks and judgement calls

The suite was verified by loading tests/test_database.lua under a copy of tests/run.lua with `test()` stubbed to execute immediately — 68 cases, 0 failures — rather than by running the whole suite, since sibling test files are being edited concurrently. luacheck on tests/test_database.lua is 0 warnings / 0 errors. Only tests/test_database.lua was modified; no source file was touched.

Two judgement calls worth review: (1) the v2 padding test pins that a non-table entry in `columns` still counts toward the width arithmetic — that is today's behaviour, not an endorsement, and the comment says so, so a refactor that filters first will go red deliberately rather than silently; (2) a v4 profile whose `windows` array holds a bare string raises in SeedWindows (core/Database.lua:213, indexing `w`) rather than in migrations[4], so no test was written for that shape — pinning a login-time raise would be pinning a defect. Worth a separate issue if the wave wants that guard.

Note: the scratchpad directory is shared with the other concurrently-running agents; one of them overwrote a probe file mid-run. Work under a per-agent subdirectory there.

---

## `core/Diagnostics.lua`

### Tests added (12)

- Diagnostics: the dating header prints the format the window is ACTUALLY set to
- Diagnostics: the formatter is resolved as Numbers first, and asked for both styles by name
- Diagnostics: with NS.Numbers gone the dating falls through to NS.Format
- Diagnostics: with no formatter at all it says so and dates nothing
- Diagnostics: the dating stops at four deaths
- Diagnostics: a secret id costs the row its dating, and still spends one of the four
- Diagnostics: a death the client holds no recap for still gets its row
- Diagnostics: the death is dated off the NEWEST event, which is events[1]
- Diagnostics: every roster row carries all six fields, in one fixed order
- Diagnostics: with no group the roster says so instead of printing a bare header
- Diagnostics: a unit read that REFUSES is named, and the row survives it
- Diagnostics: the roster is printed BELOW the entries, on the armed path too

### What must not change

reportDeathDating (core/Diagnostics.lua:648-689) — what a refactor must not change:
1. Formatter resolution order: `NS.Numbers or NS.Format`. They are two names for one table today (modules/Format.lua:690), so the preference is invisible until pinned; swapping it is silent until NS.Format is ever given back to the chat printer.
2. The guard `not (F and F.DeathTime and P)` prints exactly "    formatter or provider unavailable" and RETURNS — no header rows, no rows of nil. (The P-nil arm is unreachable from ReportDeathRecap, which refuses earlier with "provider unavailable".)
3. The header line is exactly `    window 1: sessionType=%s  text.deathTimeFormat=%s`, and the format is read off `cfg.text`, NOT `cfg.data.text` — `data` is where the session fields live and both are on the same window table, so a folded lookup silently prints nil for a setting the player can see in the panel.
4. The cap is FOUR ROWS WALKED, not four rows dated: `printed = printed + 1` sits outside the if/else, so four secret ids exhaust it. Mid-pull every id is secret, and an increment moved into the else arm would walk the whole column looking for a fourth that cannot exist.
5. The safe-key gate (`S.IsSafeKey(id)`) is what keeps a secret out of `P.GetRecap` and out of `string.format`; its arm prints exactly "    [id is secret — nothing can be dated from it]" and nothing else for that row.
6. The death is dated off `recap.events[1]` — the client hands the array back newest-first. Dating off the last element puts the death at the fight's first damage instead of at the killing blow, and nothing in the output would look wrong.
7. A death with no recap still prints its row, with `recap timestamp=nil` and `clock=nil  ago=nil`. The absent recap is the finding issue #1 turns on; a row skipped for want of a timestamp reads as a death the report never saw.
8. `deathTimeSeconds` is printed although nothing reads it any more (the file's own comment): it is the field three failed derivations were built on, and seeing it read -1 is what a reader needs. It goes through `shown`, not tostring.
9. Both styles are printed, clock before ago, with the style as DeathTime's SECOND argument.

reportFeignRoster (core/Diagnostics.lua:1738-1761):
10. Guard `group == nil or #group == 0` prints "    &lt;no group&gt;" and returns — both arms happen (no Roster yet; solo/empty group).
11. The row is one fixed order of six fields: token, guid, hp, dead, feigning, local. All three unit APIs are read on EVERY member on purpose (the file's comment): without the non-feigning baseline a single hp=0 row proves nothing.
12. The three reads are deliberately NOT uniform. `hp` goes through `probe` (pcall + `%.1f` on a number) so it reads `&lt;refused&gt;` when UnitHealth raises OR is absent; `dead` and `feigning` are `_G`-guarded and read `nil` when absent. A refactor folding the three into one helper changes what this row says on a live client. The one-decimal health is not a stray format — it is probe's describe-don't-read path.
13. `local=%s` is `e.isPlayer and true or false`, so it always prints true/false, never nil.
14. The roster is printed on BOTH paths — the not-armed early return and the end of reportFeign — and BELOW the entries, because it is the key that joins GUIDs in the trace to names.
15. Everything reaches these two functions only through `Diagnostics.ReportDeathRecap` / `Diagnostics.ReportFeign`, each of which pcalls its whole body and prints "section failed:" on a catch. An assertion of "it did not raise" therefore proves nothing here; the tests assert the OUTPUT and the absence of "section failed".

### Risks and judgement calls

Verified against the unrefactored code: 87/87 cases in tests/test_diagnostics.lua pass, luacheck 0 warnings. I ran only this suite (via a scratch runner that loads test_diagnostics alone with the kit's suite-inventory gate disabled) so concurrent edits to sibling test files were not measured. No file outside /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/tests/test_diagnostics.lua was touched; the diff is 255 added lines and no deletions. Two soft spots for the refactor wave: the "ago" rendering is wall-clock dependent, so no test asserts its text (only that both styles print); and the four-secret-ids fixture leans on mocks.setSecretsAccessible(false), so a change to the mock's secret model would move those cases rather than the code under test.

---

## `modules/Aggregator.lua`

### Tests added (8)

- A pet's DEATH lands on the row the merge put it on
- A fold the gate refuses is COUNTED, and adds nothing on the way past
- A feigned death is a SKIP, never a drop
- A counted column publishes NO column total, so its percent stays empty
- A counted column ignores the session's maxAmount, however loud
- The Deaths pass prunes the feign set itself, and no other column does
- The judge verdict is recorded per death source, after the prune
- A column that is not counted records no judgement at all

### What must not change

The refactor named by issue #35 (split into placeSource + normalizeCountedMax) MUST NOT change any of these, and each now has a test:

1. THE THIRD PLACEMENT ARM EXISTS. `elseif isCount` — a source that is not its row's own (a merged pet) in a counted column is TALLIED (setCell with isCount true) and added to `touched`, never handed to foldPet. Verified today: merged pet + two Deaths rows yields one row, total 2, `#row.deaths == 2`.

2. A REFUSED FOLD IS COUNTED. `not foldPet(...)` increments `pass.unfolded`, whose only outlet is the one-per-pass debug line (`unfolded=1`). The owner's own figure must be untouched — no partial sum. The CanCompare2/type gate stays inside foldPet (issue #35 "what must not change" clause 1).

3. A FEIGN IS A SKIP, NOT A DROP. The feign path must not go through dropSource: `dropped` stays 0 and no `dropped guid=` line is printed. This is the observable half of clause 2 (the drop stays BEFORE rowForSource — filtering after leaves a phantom row).

4. THE COUNTED TAIL DELETES `pass.columnTotals[statKey]`. Consequences pinned: `result.columnTotals.Deaths`, `result.sortTotal` (when Deaths is the sort column), `cell.columnTotal` and `cell.percent` are ALL nil. Publishing the session's totalAmount here would put a header total and a percent column of nonsense on the grid.

5. `not isCount` GUARDS BOTH THE `maxAmount` LOCAL AND THE BACKFILL. A Deaths session reporting maxAmount 999 must still scale to the computed count max (2). Dropping either guard is the easy mistake when the tail moves out.

6. THE PRUNE IS THE COUNTED WALK'S, ONCE PER PASS. `Feign.Prune()` runs from the Deaths column and nowhere else on the refresh path — asserted against `Feign.IsFeigned` directly: a damage-only Build leaves the set standing, the next Deaths Build evicts. Hoisting it into Build would make a damage window prune; dropping it lets a stale feign eat every later death.

7. ORDERING: PRUNE BEFORE EVERY JUDGE. The recorded trace sequence for one pass is exactly `cast,prune,judge,judge` — one prune, then one judgement per death source, in source order. A judge line ahead of the prune is a verdict from the previous pass's set and points the issue #25 report at the wrong fork.

8. THE JUDGE RECORD'S SHAPE IS THE CONTRACT: fields `guid`, `recap`, `dropped`, with `order` = {"guid","recap","dropped"}, and `dropped` is FALSE, never nil, for a real death.

9. `traceJudge` STAYS RESOLVED ONCE PER COLUMN, off the Feign module (clause 3). A non-counted column records ZERO judgements even with the trace armed — resolving per source would put a fields table per source back on the hot path.

Constraints on the work itself: luacheck is clean on the file (0 warnings); the suite was run in isolation via a scratch runner (`suiteInventory = false`, suites = {"test_aggregator"}) rather than `lua tests/run.lua`, per instructions — 89 passed, 0 failed. No file outside tests/test_aggregator.lua was touched.

### Risks and judgement calls

One test monkey-patches `inst.NS.Diagnostics.TraceFeign` with a spy; `T.load()` returns a fresh isolated instance (run.lua exposes `load = loadInstance`, distinct from the `shared` instance), so the patch cannot leak into sibling suites. The `unfolded` case reaches the refusal through a pet whose `totalAmount` is nil — the type gate rather than the CanCompare2 gate, because the CanCompare2 path is unreachable from the GUID join (mid-pull the identity build runs instead); if a refactor ever makes a secret operand reachable here, that arm still wants its own case. `highest < 1 then highest = 1` in the counted tail is defensively unreachable — every touched row has a count of at least 1 — so it is deliberately not pinned.

---

## `modules/DrillDown.lua`

### Tests added (8)

- The exit toggle keys on the GUID too, not the stat alone
- A row that is not a table is refused whatever it is
- A row with no guid is refused, and the window stays on the grid
- A stat key outside the catalog is refused
- The Deaths ladder falls all the way to the ordinary breakdown
- A client with no C_DeathRecap and no id still reaches the breakdown
- The exit toggle is answered BEFORE the Deaths ladder is climbed
- Switching out of a deaths view replaces the state, it does not merge into it

### What must not change

Invariants a refactor of OnCellClick must not change, all now pinned:

1. GUARD FIRST. `type(row) ~= "table"` returns the exact string "none" before anything else is touched — for a string and a number as well as nil.

2. TOGGLE SECOND, AND IT IS A TWO-KEY MATCH. The exit test compares BOTH `current.guid == row.guid` AND `current.statKey == statKey`. A same-stat click on a different player's row must return "enter" and move the view, never "exit".

3. THE TOGGLE OUTRANKS THE DEATHS LADDER. A second click on a drilled Deaths cell returns "exit" and must NOT also hand row.deathRecapID to Blizzard's frame on the way out. Hoisting the ladder above the toggle is the failure this guards.

4. THE DEATHS LADDER'S ORDER IS THE WHOLE OF IT (the comment at 407-414 says so explicitly): (a) deaths view when canReadRecaps() AND copyRecapIDs(row.deaths) is non-nil — and then Blizzard's frame must not open; (b) openDeathRecap(row.deathRecapID) returning "recap"; (c) fall through to the ordinary spell breakdown. Rung (c) is reachable from both upper misses independently — empty deaths array with the API present, and no API with no id — and in both cases the result is "enter" with kind == "spells". The cell is never dead.

5. THE FOUR RETURN STRINGS ARE THE CONTRACT: exactly "none", "enter", "exit", "recap". Enter/Exit's boolean is mapped through `and "enter" or "none"` / `and "exit" or "none"` — a refusal out of Enter (row with no guid; a statKey absent from Const.STAT_BY_KEY, e.g. "EnemyDamageTaken", which is deliberately off-catalog) must surface as "none" with IsActive still false, not as an error and not as "enter".

6. ENTER REPLACES THE VIEW TABLE WHOLE. Switching from a deaths view to a spell cell must leave `view.deaths` nil; BuildRows picks its branch off `kind` alone, so an in-place field update would render a spell view off a stale death snapshot.

7. Untouched by these tests but load-bearing per the file header: nothing in this path may read, compare or `#` a meter amount, and the title stays display-only (IsActive is the plain boolean, already pinned at the top of the suite).

Verification: run in isolation via a scratchpad copy of tests/run.lua limited to the test_drilldown suite (the whole-suite run was left to the orchestrator as instructed) — 58 passed, 0 failed against the UNREFACTORED modules/DrillDown.lua. luacheck on tests/test_drilldown.lua: 0 warnings, 0 errors. No file outside the assigned test file was modified.

### Risks and judgement calls

Two of the new cases depend on fixtures owned by the existing suite (`deadRow` and `withRecaps`, defined mid-file); they are appended after those definitions, so a future reorganisation of the file must keep that ordering. `docs/test-cases.md` is generated from the registry by the automated-tests script and now lags by eight cases until the orchestrator regenerates it. Nothing else in the repo was touched.

---

## `modules/Export.lua`

### Tests added (21)

- Export.ChatLines refuses anything that is not a result table
- Export.ChatLines joins an empty segment name rather than asking whether it is empty
- Export.ChatLines omits a segment name that is not a string
- Export.ChatLines takes the duration from the result and never from the formatter
- Export.ChatLines asks the formatter for the amount, the rate and the share by name
- Export.ChatLines carries the rate alone when the aggregator computed no share
- Export.ChatLines drops a share the aggregator did not answer as a number
- Export.ChatLines prints a zero share rather than reading it as absent
- Export.ChatLines names a row that has no cell for the metric anyway
- Export.ChatLines reads the rows off result.rows when it is not the result itself
- Export.ChatLines answers a header and nothing under it for a result with no rows
- Print to Chat re-checks the restriction at the click, not at the open
- Print to Chat names a blank whisper recipient before it builds anything
- Print to Chat asks the game for the target at the click
- Print to Chat whispers the player currently targeted
- Print to Chat says so rather than swallowing a click with nothing to export
- Print to Chat builds with the chosen metric as the SORT COLUMN
- Print to Chat leaves the lines themselves as the confirmation on SELF
- Print to Chat confirms a send that left the client, without counting the header
- Print to Chat warns BEFORE a Say dump the server may truncate
- Print to Chat does not warn where the stagger is available or the dump is short

### What must not change

ChatLines (issue #36's "What must not change", now all pinned):
- EVERY JOIN STAYS `..`, never table.concat and never a comparison on a string a formatter produced. Two concrete consequences are now tests: session is admitted on `type(session) == "string"` alone, so an EMPTY session name is joined and the header reads "Multi Meters — Damage —  (2:14)" (a refactor that "tidies" this into `session ~= ""` goes red); and `hasExtra` stays a boolean, so a rate with no share yields "(5.0K)" with no trailing comma without ever asking whether `extra` is "".
- THE DURATION IS DECIDED FROM `result.durationSeconds`, never from F.Duration's answer. Both arms of `seconds ~= nil and F.Duration` are pinned: a nil durationSeconds omits the parenthetical, and a formatter table with no Duration member omits it too while the rest of the line still formats.
- Ordering inside the parenthetical is rate then share, joined ", ". Each formatter member (Number/Rate/Percent/Duration) is independently optional; losing one may only lose its own half.
- `type(cell.percent) == "number"` is a type test, not truthiness: percent 0 prints "(0.0%)" and percent "31.2" (a string) is dropped.
- Rank is the aggregator's order; nothing sorts (already pinned, still load-bearing).
- Refusal shape: a non-table result (nil from Export.Build on a load with no aggregator, a string, a number) answers `{}`, as does the restricted state and a missing formatter. A result with rows but none matching the stat still names the row and leaves the amount blank ("1. Kaosz " — trailing space is F.Number(nil)).
- `result.rows or result` must keep accepting both shapes: the aggregator's self-referential result and a hand-assembled `{ rows = {...} }`.

onPrintToChat (all newly pinned):
- THE ORDER OF THE GUARDS IS THE CONTRACT. Available() first (prints the reason AND calls refreshModal, so modal.warning carries the sentence); then the blank-whisper check; then the TARGET check; and only THEN Export.Build. Both whisper and target refusals must fire BEFORE the aggregator is asked — the tests assert Export.Build was never called, so moving either below the build turns "Enter a name to whisper to." into "There is nothing to export." on an empty segment.
- Exact strings: "Enter a name to whisper to.", "You have no target to whisper to.", "Your target is not a player.", "There is nothing to export.", "Export is not available while the game restricts combat data.", "Exported %d rows to chat.", and the flood sentence "Say and Yell go out all at once outside instances, so the server may drop some of %d lines. Fewer lines, or a group channel, will arrive whole."
- Export.Build is called with the resolved metric as the SORT COLUMN, and the same key is handed to ChatLines.
- The confirmation is `math.max(#lines - 1, 0)` — the header is not a ranked row — and it is printed ONLY when channel ~= "SELF"; on SELF the lines are the confirmation and nothing else is said.
- The flood warning is said BEFORE Export.Send, is counted on `#lines` (header included: 12 rows warn about 13 lines), and fires only when NeedsHardwareEvent(chatType) and #lines > Export.ChatBatch(). Inside an instance (SAY exempt) and for a dump of five lines or fewer it must stay silent.
- A blank whisper name is `tostring(whisperTo):match("^%s*$")`, so "" and "   " are the same mistake.

Hygiene notes for whoever refactors: luacheck is clean on tests/test_export.lua (0/0). I verified the suite in isolation with a scoped runner (dir pointed at a copy of only this suite) rather than `lua tests/run.lua`, since siblings are being edited concurrently: 112 passed, 0 failed. One stale figure the refactor should sweep: docs/ARCHITECTURE.md line 458 and the cap-census row at line 542 both record tests/test_export.lua as 1509 lines; it is now 1887. tests/test_layout_cap.lua reads only the path and the disposition from that row, so nothing is red today, but the number is wrong.

### Risks and judgement calls

The onPrintToChat cases drive the handler through `modal.chatButton:__fire("OnClick")`, which the mock runs even on a Disabled button. That is deliberate — it is the only seam onto a file-local handler, and the module's own comment says the greyed-out button is a hint rather than a guarantee — but a refactor that moves the availability check out of the handler and relies on the disabled state would pass in the client and go red here, correctly. The same cases stub Export.Build (recording its sortColumn) so they are about the click rather than about the join; if a refactor stops routing through Export.Build by name, every one of them will fail loudly rather than silently measure a stub.

---

## `modules/Feign.lua`

### Tests added (12)

- Feign: a confirmed 0 HP evicts even while the client still reads feigning
- Feign: an entry the client never confirmed is not evicted by a false reading
- Feign: a health figure that cannot be compared leaves the entry standing
- Feign: an evicted entry is traced with the state it HELD
- Feign: a surviving entry is traced with evicted=false and its raw readings
- Feign: leaving the group is traced as <not in group>
- Feign: the armed flag is read once per prune, not once per member
- Feign: a disarmed prune hands the recording nothing at all
- Feign: an absent Diagnostics file is not an error
- Feign: a group entry with no token or a secret guid counts as absent
- Feign: with no Roster at all every entry is evicted
- Feign: the set stops being walked once the last entry goes

### What must not change

Every clause of issue #37's "What must not change" is now pinned, plus the guards the comments call load-bearing:

1. `prior` is READ BEFORE THE EVICTION (the M2-11 bug). An entry evicted at 0 HP from "noted" must trace state="noted" and one from "down" must trace state="down"; collapsing both to nil/"<evicted>" is the exact regression. Pinned with two members in one prune.
2. `dead` WINS AHEAD OF `nowFeigning`. hp==0 evicts even while UnitIsFeignDeath reads true — UnitIsFeignDeath lingers true through a feign-then-die transition, so deferring to it hides the real death.
3. The `recording = armed()` READ STAYS HOISTED out of the walk: exactly one read of Diagnostics.feignArmed per Prune, with two feigners in the set. This is the constraint a `judgeMember(guid, unit, recording)` split is most likely to break by asking armed() per member.
4. THE seenDown GATE. `evicted = dead or (seenDown and alive and nowFeigning == false)` — an entry never seen "down" must survive a false feign reading, because that is what the client reports in the instant between the cast succeeding and the aura appearing. Dropping seenDown as "redundant" undoes every entry immediately.
5. THE TRACE IS OUTPUT, AND ITS SHAPE IS THE CONTRACT. Both prune lines carry order = { "unit", "guid", "hp", "feigning", "state", "evicted" } exactly (core/Diagnostics.lua walks `order` to render the line). The absent-member line reports unit="<not in group>", hp=nil, feigning=nil, state=prior, evicted=true. A survivor reports evicted=false — a boolean, never nil (`evicted and true or false`).
6. INSTRUMENTATION IS GUARDED AT THE CALL SITE, not inside TraceFeign: a disarmed prune must hand the recording nothing at all (performance-§2 — the cost is the fields table, which Lua builds before the call). Pinned by counting TraceFeign calls while disarmed.
7. NIL-NESS, THEN CanCompare, THEN the comparison. A secret/unreadable health figure is neither alive nor dead and leaves the entry exactly where it is; comparing first raises.
8. THE PRESENT-MAP GUARDS. `Secrets.IsSafeKey(entry.guid)` (a secret GUID as a table key raises outright) and `entry.unit` (no token = untrackable = same verdict as leaving the group). Both dropped members must be evicted, not left in the set forever.
9. NS.Roster AND NS.Diagnostics ARE RESOLVED AT CALL TIME AND MAY BE ABSENT. No Roster => group nil => every entry evicted; no Diagnostics => armed() answers false rather than raising.
10. `remaining` FEEDS `anyFeigned` FROM THE WHOLE WALK. One survivor keeps the walk alive on the next pass; the last eviction stops the roster being enumerated at all (the hot-path short circuit — Prune runs once per refresh, four times a second).

Verification: luacheck on tests/test_feign.lua is 0 warnings / 0 errors. All 27 cases in the suite (15 pre-existing + 12 new) pass AGAINST THE UNREFACTORED code, run in isolation via a scratchpad copy of tests/run.lua restricted to { "test_feign" } (suiteInventory disabled) so no sibling suite under concurrent edit was touched. No file outside tests/test_feign.lua was modified.

For the orchestrator: docs/test-cases.md is generated from the registry (`lua tests/run.lua --list > docs/test-cases.md`) and now under-counts this suite by 12; regenerate it once every agent has landed, along with any pass-count claim in README.md / docs/testing.md.

### Risks and judgement calls

Three of the new tests substitute a collaborator that Prune resolves through NS at call time — a Roster stub (GetGroup returning a hand-built group, and a call counter), a wrapped Diagnostics.TraceFeign, and a counting __index proxy over NS.Diagnostics. Each substitution is legitimate because the module deliberately resolves these at call time and documents that they may be absent, but a refactor that captured NS.Roster or NS.Diagnostics as an upvalue at load would make these tests fail — correctly so, since capturing at load is itself the behaviour change (modules/Roster.lua's header and this file's own header forbid it: the headless harness installs its unit mocks after the files load).

The trace assertions read the raw `fields` table handed to TraceFeign, not the rendered report line. If a refactor moves the describing (`shown`) into the call site rather than into core/Diagnostics.lua, these tests would see described strings instead of raw values and fail — again correctly, since the contract is that Feign hands raw values and Diagnostics describes them at capture time.

Not covered, deliberately: the mid-pull limitation (the filter cannot run while sourceGUID is secret) is structural and already stated in the file header and the suite header; there is no seam to assert it against inside Prune.

---

## `modules/Format.lua`

### Tests added (7)

- Format.DeathTime: the seconds/minutes boundary and the exact strings
- Format.DeathTime clamps a death in the future to zero
- Format.DeathTime treats any unknown style as the clock
- Format.DeathTime falls back to the clock when 'now' cannot be had
- Format.DeathTime defaults 'now' to the client clock
- Format.DeathTime routes both countdown strings through the locale
- Format.DeathTime refuses a secret timestamp in either style

### What must not change

The refactor MUST NOT change any of these, all now pinned and green against the unrefactored code:
1. Guard order. `when == nil or not Secrets.CanAccess(when)` runs FIRST and answers nil, before `date()` is called — an inaccessible timestamp is never handed to a client API, and both styles refuse identically.
2. The clock is computed before the style branch, and it is exactly date("%H:%M:%S", when).
3. Two distinct refusals with two distinct answers: a refused `when` answers nil (caller draws an em dash), a refused `now` (secret, CanCompare2 false) or an absent `time()` answers THE CLOCK, not nil. Collapsing these into one guard is the likeliest silent regression.
4. `now` defaults to `_G.time()` and is read per call, not cached; `_G.time` absent must degrade to the clock rather than raise.
5. Boundary and unit: seconds < 60 renders "%ds ago" (59 -> "59s ago"), >= 60 renders "%dm ago" with math.floor truncation (60 and 119 both -> "1m ago", 500 -> "8m ago"). No hour rung: 3600 -> "60m ago". The header's comment names the seconds branch as load-bearing ("0 min ago" for a death that happened while you were reading the tooltip is worse than saying nothing).
6. Negative clamp: seconds < 0 becomes 0, so a death stamped ahead of `now` reads "0s ago", never a negative.
7. "ago" is the only special style, matched case-sensitively; everything else ("elapsed", "fight", "AGO", nil) falls through to the clock. This is what makes a saved profile holding the removed third style (issue #18) render a clock instead of nil.
8. Both countdown strings come from L (L["%ds ago"], L["%dm ago"]) with a literal fallback; the module owns only the "%d".
Verification: luacheck on tests/test_format.lua is 0 warnings / 0 errors. The suite was run in isolation via a scratchpad copy of tests/run.lua restricted to test_format (no whole-suite run, per instructions): 39 passed, 0 failed.

### Risks and judgement calls

Two tests mutate instance-local state and restore it: `inst.mocks.time` is set to nil / to fixed-clock stubs and put back before the assertions, and `inst.NS.L` is overwritten on a FRESH T.load() instance so no other suite sees the German-ish strings. Both rely on T.load() giving a genuinely isolated NS and mocks, which tests/run.lua's loadInstance does. The default-now test depends on `_G.time` resolving through the loader env to `mocks.time` (mock_base sets M.time = os.time); if a future kit revision stops mapping it, that test goes red for a harness reason rather than a code reason — the comment says why it exists. No production file was touched.

---

## `modules/HeaderControls.lua`

### Tests added (14)

- HeaderControls: a click with no window, or no control, does nothing
- HeaderControls: a control name the chain does not know is a silent no-op
- HeaderControls: the two toggles name the EXACT settings paths
- HeaderControls: a toggle inverts what is STORED, as a boolean
- HeaderControls: a toggle points the seam at this window BEFORE it writes
- HeaderControls: with no settings seam a toggle changes nothing and raises nothing
- HeaderControls: the gear sets the active window BEFORE it opens the panel
- HeaderControls: the gear still points the panel when there is no panel
- HeaderControls: reset PREFERS the centred dialog over the bare popup
- HeaderControls: with settings/ absent the reset falls back to the bare popup
- HeaderControls: reset with no popup API at all raises nothing
- HeaderControls: segment and export are opened ON the window, or not at all
- HeaderControls: close hides the window AS a deliberate close
- HeaderControls: only the two toggles write to the settings seam

### What must not change

Behaviours the issue #38 refactor (a module-level ACTIONS table keyed by control name) MUST NOT change, now each pinned by a case:

1. The two guards run BEFORE any dispatch. `frame.mmWindow` or `frame.mmControl` missing returns silently; indexing an ACTIONS row before the guards raises on `window.config`. An unrecognised control name falls out of the chain with no `else` and no error — a lookup must tolerate a missing key.
2. Exact path strings, and they are the SavedVariables/schema contract: minimise writes "window.frame.minimised", lock writes "window.frame.locked", both through NS.SetByPath (`write`), never by poking window.config.frame — that seam is the sole publisher of CONFIG_CHANGED and what the settings panel's own checkbox writes through.
3. The written value is a BOOLEAN, from `not (stored and true or false)`. A profile holding a truthy non-boolean must still write `false`, not `nil` (a boolean schema row refuses nil).
4. ORDERING, load-bearing twice, and both are the shape a table-driven rewrite most easily swaps: `write` calls NS.State.SetActiveWindow(window.id) BEFORE set(path, value) — `window.`-prefixed paths resolve against the one active id, and the reverse order writes to whichever window the panel was last left on (the worst bug in the first cut). The gear likewise calls SetActiveWindow BEFORE NS.OpenOptionsPanel, which takes no arguments.
5. Every seam is resolved at CALL time and independently guarded: NS.SetByPath absent (settings/ loads after modules/) → silent no-op, no fallback poke; NS.OpenOptionsPanel absent → the active id is still set (two separate `if`s, not one around both); window.OpenSegmentMenu absent and NS.Export / E.Open absent → silent.
6. The reset ladder keeps its order and its arms: NS.ShowResetMeterData first (settings/General.lua owns and centres the dialog), the bare `_G.StaticPopup_Show("MULTIMETERS_RESET_METER_DATA")` only as the degraded arm, and neither present is inert rather than fatal. The exact popup key is the contract; a wrong name shows nothing, i.e. a reset that never asks. The warning text is deliberately NOT duplicated here.
7. Method calls stay method calls: `window:OpenSegmentMenu()` and `E:Open(window)` — Export.Open reads the window instance to centre its modal, and the config table has no frame to measure.
8. close calls `window:Hide("closed")` WITH the reason. Window:Hide clears `forcedShow` only for "closed"/"toggled"; a bare Hide() leaves an explicit show standing and the window reappears on the next settings edit.
9. The arms share no state: driving all seven controls produces exactly two seam writes, minimised then locked.

Verification: 65 passed / 0 failed against the UNREFACTORED code, run through a scratchpad single-suite copy of tests/run.lua (the full suite was not run — sibling test files are being edited concurrently). `luacheck tests/test_headercontrols.lua` is 0 warnings / 0 errors. The file is 1159 lines, under layout-§1's 1500 cap. Only tests/test_headercontrols.lua was modified. Note for the orchestrator: docs/test-cases.md still records 51 cases for this suite and is generated (`lua tests/run.lua --list > docs/test-cases.md`), so it needs regenerating once every agent is done.

### Risks and judgement calls

No source file was touched, so no behavioural risk. Two residual risks in the tests themselves: the guard case ("a click with no window, or no control, does nothing") deliberately does NOT pcall, so if the refactor drops the guards it fails as an error rather than an assertion — that is intended, but reads as a harness error in the log. And "only the two toggles write to the settings seam" asserts the write ORDER (minimised then locked) because it drives the controls in CONTROLS order; a refactor that legitimately reordered the loop, not the arms, would trip it — the order it encodes is the CONTROLS table's, which is itself load-bearing for the layout.

---

## `modules/Roster.lua`

### Tests added (17)

- Every member the build learns is remembered in db.global, as a plain copy
- A pet link is remembered too, and a secret one never reaches SavedVariables
- Refresh forgets the group but not the people; Forget forgets both
- The live entry is preferred over the remembered one, never the other way round
- A member whose own GUID is unreadable is left out, pet and all
- The raid duplicate is skipped WHOLE, its pet unit included
- An empty unit API yields an empty group rather than a raise
- A partial build is still STORED, so the lookups have something to answer from
- Roster.LocalGUID reads the player's GUID off the built map
- The player's role falls back to their specialization; another unit's cannot
- An assigned role beats the specialization fallback
- Test mode replaces the pet map and writes nothing to SavedVariables
- The test-mode map is cached whole, never marked partial
- Test mode with no preview group falls back to the real unit walk
- A completed build logs one line, with the counters the loop kept
- The build line says whether this was a raid
- A short build says so, and does not also claim it built the group

### What must not change

Behaviours the refactor of build() must not change, now pinned:

1. SavedVariables shape. db.global.roster.byGuid[guid] holds exactly { guid, name, classFilename, role, isPlayer } and NO `unit` field, and is a fresh table each build — never an alias of the live cache entry, which is wiped on every regroup. db.global.roster.pets[petGuid] = ownerGuid. Roster.Forget replaces the whole thing with { byGuid = {}, pets = {} } (both maps must exist as tables, or the next build indexes a nil); Roster.Refresh must leave it entirely alone.

2. Lookup precedence, live-then-remembered. Get / IsGroupMember / OwnerOf all read the live cache FIRST and the remembered map second. Note for anyone extending these tests: precedence is only observable while the cache is warm, because a rebuild rewrites the remembered snapshot from the live walk — an assertion that invalidates before looking up passes under a reversed `or` (I hit exactly that and fixed it).

3. Guard nesting inside the walk. The pet lookup lives INSIDE `if Secrets.IsSafeKey(guid) and byGuid[guid] == nil then`. Two consequences are pinned: a member whose own GUID is secret is skipped along with its pet, and in a raid the duplicate raidN pass is skipped whole, so `raid1pet` is never consulted (the player's pet is only ever reached as `playerpet`). Hoisting the pet block out of that guard breaks four cases.

4. First-entry-wins de-duplication. cache.byGuid[playerGuid] must be the `player` entry (entry.unit == "player"), not the raidN one — Roster.LocalGUID and Roster.Get both depend on it.

5. Order of the two role sources. UnitGroupRolesAssigned wins; GetSpecializationRole is a fallback and applies to `unit == "player"` only. A party member with an unassigned role stays "NONE".

6. The test-mode arm returns EARLY, and that is load-bearing three ways: cache.pets is REPLACED with a fresh empty table (not carried over and not seeded from the remembered map); nothing invented is written to db.global.roster; and cache.partial is never computed, so a preview group smaller than the real group is not treated as a short build and re-walked on every read. The arm is also `A and A.TestGroup` resolved at call time and must fall THROUGH to the real unit walk when the aggregator is absent, not return an empty group.

7. A partial build is MARKED, not withheld: cache.group, cache.byGuid and cache.pets are all stored before the `partial` check, so lookups answer from the short map while `ensure` retries.

8. Exact debug strings (chat/log output is contract): "built members=%d pets=%d raid=%s" with raid rendered "yes"/"no", and "partial build (%d of %d) — will retry" (em dash). petCount counts only pets that passed IsSafeKey — a secret pet must not be counted. A partial build logs the partial line and must NOT also log "built members=", which is what makes that string a reliable grep for a build that stuck.

Verification: luacheck on tests/test_roster.lua is 0/0; all 39 cases in the suite pass against the UNREFACTORED modules/Roster.lua, run through a scratch single-suite runner (no whole-suite run). I additionally mutation-checked the new cases against a throwaway copy of the tree in the scratchpad — aliasing the remembered entry, reversing both lookup `or` arms, hoisting the pet block out of the member guard, seeding test-mode pets from the remembered map, persisting invented members in test mode, and counting unreadable pets each go red on the expected case. modules/Roster.lua itself is untouched (git reports only tests/test_roster.lua modified).

### Risks and judgement calls

Two things a later wave should know. (a) The debug-line cases assert exact format strings via plain `find`, including the em dash in "partial build (%d of %d) — will retry"; if the refactor reflows that message the cases fail by design, and the fix is a deliberate decision about the log contract, not a test edit. (b) "Test mode with no preview group falls back to the real unit walk" nils out NS.Aggregator.TestGroup on its own isolated instance — harmless today because T.load leaves modules unsubscribed, but if the harness ever enables every module by default that case would need the bus quiesced first.

---

## `modules/Row.lua`

### Tests added (15)

- The border setting off builds no texture at all
- Turning the border off hides all four sides and keeps the textures
- Each of the four sides is anchored to its own two corners
- A second layout pass re-places the border rather than stacking anchors
- A thickness under one pixel is clamped to one, on both paths
- The art path takes the edge FILE and the swatch's colour
- The art path answers the colour mode too, and it is the ROW'S class
- Switching from the flat outline to art takes ALL FOUR sides down
- Icons on the RIGHT anchor to the right edge and give the name the left one
- The icon takes its configured size and is centred in the row
- ApplyIcons returns the inset it consumed, and never zero
- The slot list and the drawn flag are what SetPlayer reads
- A narrow name column still leaves the string a width of at least one
- A window config with no icons group at all draws a name and does not raise
- Re-laying the icons out does not stack anchors on the texture or the name

### What must not change

ApplyBorder — (1) BORDER_SIDES is exactly {top,bottom,left,right}; the create loop, the hide loop and the tint loop must keep walking one list. (2) Textures are created at CreateTexture(nil,"OVERLAY",nil,7) — sublevel 7 is load-bearing (issue #39 "what must not change"); the comment records that at the default sublevel the outline draws UNDER the bar it outlines. (3) Per-side anchoring is now pinned corner by corner: top = TOPLEFT+TOPRIGHT +height, bottom = BOTTOMLEFT+BOTTOMRIGHT +height, left = TOPLEFT+BOTTOMLEFT +width, right = TOPRIGHT+BOTTOMRIGHT +width, all at 0,0 relative to the cell's own StatusBar, and the axis NOT spanned is the one that takes the thickness. The issue proposes replacing the if/elseif chain with a BORDER_ANCHOR data table; that table must transcribe exactly these pairs. (4) Thickness clamp `type(size) ~= "number" or size < 1 then size = 1` applies on BOTH paths — the flat SetHeight/SetWidth and the backdrop's edgeSize; a string thickness must not reach a `<` comparison (Lua 5.1 raises). (5) The two paths are mutually exclusive and BOTH must be cleared: art hides all four flat textures and returns; non-art calls SetBackdrop(nil) before anything else. (6) The refusal path `if not (wanted or edges) then return end` must stay ABOVE the lazy create — the shipped default is border=false and hoisting the create costs four textures per cell per row. (7) `if not wanted` hides all four and returns without destroying them (pool contract: cell.border table and each texture keep their identity). (8) cellBorderColor is the single colour source for both paths: skin edge -> configured swatch -> class override, with the configured ALPHA surviving the class mode. (9) ClearAllPoints precedes the two SetPoints on every pass.

ApplyIcons — (a) one slot only, named "unit"; iconOrder and iconsShown are outputs read by SetPlayer, and iconsShown is derived from `#slots > 0`, not from the setting. (b) offset 2, stride size + ICON_TEXT_GAP (4, and NS.ICON_TEXT_GAP is shared with modules/Window.lua's nameColumnWidth — the same number in two files). (c) LEFT anchors TOPLEFT with +x and insets the name by `consumed`; RIGHT anchors TOPRIGHT with -x and puts the name back at LEFT +2. Both must move together. (d) y = (layout.rowHeight - size) * -0.5. (e) consumed is computed from the CONFIGURED slots, never from what the row drew, and is 2 (not 0) when there are none; the function returns it even though RowProto:ApplyLayout currently discards it. (f) width = nameColumn.width - consumed - 2, floored at 1, set as an explicit width — never a second anchor. (g) `config.icons or {}`, `layout.nameColumn or {}`, `icons.size or 14` guards must survive; a nil icons group must draw, not raise. (h) SetWordWrap(false)/SetMaxLines(1) stay guarded by presence checks. (i) The hide loop walks pairs(self.icons) and hides anything not in slots; textures are kept, never destroyed.

### Risks and judgement calls

Two assertions lean on harness defaults rather than on an explicit call: `edges.top:GetWidth() == 0` / `edges.left:GetHeight() == 0` read the mock frame's initial __w/__h of 0 to prove the thickness went on one axis only. They are correct today and fail loudly if a refactor sets both axes, but a mock change would move them. The art-path colour tests set the entry with row:Update and then re-run ApplyLayout so ApplyBorder is the last writer of __backdropBorderColor — if a refactor makes ApplyEntryBorderColor run after ApplyBorder within a layout pass the assertion still holds (same colour), so it does not over-constrain the ordering. Verification was done with a scratch single-suite runner (scratchpad/run_row.lua, a copy of tests/run.lua with suites={"test_row"} and suiteInventory=false) so no sibling agent's file was loaded; 106 passed / 0 failed, up from a 91-pass baseline, and luacheck reports 0 warnings on tests/test_row.lua. The whole-suite run is still the orchestrator's to make.

---

## `modules/Tooltip.lua`

### Tests added (13)

- Tooltip: an event with no id and no name reads as #? under the question mark
- Tooltip: a DIRECT heal with no spell id reads as Heal too
- Tooltip: an event AFTER the moment of death keeps the sign OFF
- Tooltip: a refused offset empties the time slot and reserves the column
- Tooltip: a recap whose events are not an array says so and draws nothing
- Tooltip: an EMPTY event array is a refusal, not an empty list
- Tooltip: a SECRET event array is refused whole, never indexed
- Tooltip: an entry that is not a table is skipped, and the rest still draw
- Tooltip: the collect stops at 64 events, keeping the NEWEST of them
- Tooltip: ONE unreadable caption abandons the whole measurement
- modules/Tooltip.lua never applies `#` to a recap's event array
- Tooltip: a stat key the catalog does not know heads with the key itself
- Tooltip: a Deaths cell reads deathTimeFormat off the WINDOW's text block

### What must not change

Orderings and rules a refactor of modules/Tooltip.lua MUST NOT change:

1. R1 — `#` is NEVER applied to the recap's event array. `Secrets.SafeIterate` is the only legal walk; `#ordered` on the local plain array this file builds is the reason the collect exists at all. Pinned by a source scan (`#events`, `#recap.events`) plus a live secretTable case.

2. The collect runs FORWARDS and the draw runs BACKWARDS. The client sends events newest first; element one is the killing blow, its timestamp IS deathTime, and it must render as the LAST line.

3. namesReadable is ALL-OR-NOTHING. One unreadable caption abandons the whole spell/caster measurement and both columns fall back to their character reservations — never sized from the readable half. Issue #40 names this explicitly; it is now pinned with a mixed recap (one plain name, one secret).

4. The four refusals of drawDeathEvents each return false and must stay ahead of any indexing: events not a table; Secrets.SafeIterate absent; CanAccessTable(events) false (indexing a secret table RAISES — the guard cannot move inside the callback); and total == 0. All four surface to the player as the exact line "No recap stored for this death", and applyDeathMinimumWidth is skipped on all four.

5. Per-entry gates inside the walk SKIP (bare `return`) — they must never `return false`, which would stop the walk and drop every event behind a junk entry.

6. COLLECT_LIMIT is 64, applied during the forward walk, so the events kept are the ones NEAREST the death. Capping after a reverse would keep the wrong end.

7. eventColumns' naming chain has four distinct arms and all four are now reached: SWING_DAMAGE → "Melee" + MELEE_ICON (135274); SPELL_HEAL *and* SPELL_PERIODIC_HEAL → "Heal"; a spell id → "#<id>"; nothing at all → the literal "#?" with FALLBACK_ICON. The explicit nil branch exists because string.format("%s", nil) raises in Lua 5.1.

8. The time column's sign is SPELLED, not left to the subtraction: `> 0` renders "%.1fs" with no sign, everything else renders "-%.1fs" of math.abs (unary minus on zero yields negative zero and doubles the sign into "--0.0s"). A refused offset renders EXACTLY "" and leaves `widest` nil, which makes the column fall back to the "-9.9s" floor rather than collapse.

9. eventColumns joins nothing — a spell name and a caster name are separate return values, and `..` on either would raise on a secret. An absent caster returns "" so the column stays shown and the rows line up.

10. CellTooltip's tail order is load-bearing: applyMinimumWidth → GameTooltip:Show() → reapplyFonts() → applyPlacement(). Show re-fonts the lines AND re-anchors the tooltip, so both must follow it.

11. CellTooltip's header falls back to the raw statKey when Const.STAT_BY_KEY misses, and `config.statKey = statKey or config.statKey` is the HOVERED column, not the sort column.

12. The Deaths branch passes `config.deathTimeFormat or (window and window.text and window.text.deathTimeFormat)`. The tooltip config block has no copy of that key, so the second term is the only path by which the player's setting reaches Format.DeathTime.

Housekeeping for the orchestrator: docs/test-cases.md is generated from the registry and is now stale (this suite went 124 → 137 cases). Regenerate once every agent is done with `lua tests/run.lua --list > docs/test-cases.md`.

### Risks and judgement calls

All 13 new cases were written and run against the UNREFACTORED modules/Tooltip.lua and pass (137 passed, 0 failed for tests/test_tooltip.lua, run through a scratch single-suite runner so sibling agents' edits were not measured). luacheck on tests/test_tooltip.lua is clean: 0 warnings, 0 errors. No file outside tests/test_tooltip.lua was touched.

Two cases lean on mock-specific mechanics and would need re-reading if the harness changes: the "refused offset" case distinguishes the measured column from the constant floor by comparing widths (the mock's ruler is 0.5px per character per point, so "-900.0s" beats the "-9.9s" fallback), and the "one unreadable caption" case compares a 2-character measured column against the 22-character reservation. Both are strict inequalities, not magic numbers, so a font-metric change in the mock does not silently flip them.

I could not exercise the `Secrets.SafeIterate` absent refusal — it would mean stubbing NS.Secrets, which pins the stub rather than the addon. The other three refusals are covered by real inputs.

---

## `modules/Visibility.lua`

### Tests added (8)

- With every state live at once, the vetoes answer in one fixed order
- Every veto is decided before the combat pair, not after it
- Each context switched off hides with its own name, and only its own
- A context key is show-shaped; a veto key is hide-shaped
- Both gates read truthiness, not `== true`
- Anything that is not a table is `no window`, whatever it is
- A visibility field that is not a table reads as `no rules`, not as hide
- The master enable, test mode and perf suspend are NOT read here

### What must not change

The refactor named in issue #41 (eight veto branches -> a module-level VETOES table plus one loop) must not change any of the following, all of which are now pinned.

1. THE VETO ORDER, which is the whole reason the order exists. It is, exactly: hideInVehicle "vehicle", hideWhenSkyriding "skyriding", hideWhenMounted "mounted", hideOnTaxi "taxi", hideInPetBattle "pet battle", hideWhenDead "dead", hideInHousing "housing", hideWhenSolo "solo". The function's own comment calls this load-bearing ("the order between them only shows up in the REASON when two states are true at once"), and every pre-existing per-veto case drives exactly ONE state at a time, so a mistyped table row reorders the chain with the old suite still fully green. The new order case drives all eight states at once and peels the winner off the front eight times.

2. THE THREE-TIER PRECEDENCE: context gate, then all eight vetoes, then the combat pair. The combat pair stays a hand-written branch below the loop (the issue says so); it must not become a table row, because a row would land it somewhere inside the veto sequence. Pinned by driving each veto against both combat rules on, on both sides of the pull.

3. THE TWO REFUSALS AND THEIR EXACT TOKENS. type(window) ~= "table" -> false, "no window" for every non-table shape, not just nil. type(window.visibility) ~= "table" -> true, "no rules" for false / "" / 0 / a function as well as for absent. `false` is the trap: a guard rewritten as `if not rules then` falls through and indexes a boolean on the next line.

4. THE TWO GATES READ TRUTHINESS, never `== true`. rules[context] = 1 shows; a veto key = 1 vetoes. Hand-edited SavedVariables and older schemas carry non-boolean values.

5. THE SHOW/HIDE ASYMMETRY BETWEEN THE TWO HALVES OF THE SCHEMA. A missing VETO key means "nothing objects"; a missing CONTEXT key means "not here" — an empty rules table hides everywhere and names the context. Both directions are deliberate and are now asserted side by side.

6. THE REASON TOKEN on both answers, for every context: a shown window returns its context name, and a context switched off returns the SAME player-facing name ("dungeon", not Blizzard's "party"). All seven contexts including "delve" are now covered on both answers; previously only "world" had a refusal case.

7. THE LADDER'S STEPS 0-2 STAY OUT. Perf.suspended, State.testMode and db.profile.enabled are set adversarially and ShouldShow must still answer purely from the window's own rules — including that test mode does NOT force-show here (its one-way force belongs to NS.ShouldShow in core/MultiMeters.lua).

8. Unchanged from the module header and still pinned by the pre-existing scans: no Show/Hide/SetAlpha anywhere in the file, UnitAffectingCombat and never InCombatLockdown, every input read LIVE with no cache, and no RegisterEvent (bus messages only).

### Risks and judgement calls

Tests only; nothing outside /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/tests/test_visibility.lua was touched. luacheck on that file: 0 warnings, 0 errors. The visibility suite alone runs 41 passed / 0 failed (33 before, 8 added) against the UNREFACTORED module, via a scratch single-suite runner at /tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/2d592c46-51ce-4870-9011-1520eed0343d/scratchpad/runvis.lua; the whole suite was deliberately not run, as instructed. One follow-up for the orchestrator: docs/test-cases.md is generated from `lua tests/run.lua --list` and now under-counts this suite by eight cases — it needs regenerating once every agent's file has landed. `gh issue view 41` fails in this environment with a Projects-classic GraphQL deprecation error; `gh api repos/:owner/:repo/issues/41` works and is what I read.

---

## `modules/Window.lua`

### Tests added (18)

- The stored per-column width is what a NEW column is born at, never the drawn one
- The name column is excluded from the share, and is not sized by the frame
- The name column is placed first, at x 0, and carries its bar unconditionally
- A window with every column disabled still lays out
- Hiding the title bar takes its height out of the layout, not out of the header strip
- bodyWidth is the frame minus its padding, whatever the grid inside it costs
- growUp is a boolean off growthDirection, and nothing else
- A window too short for even one row still asks the pool for one
- A maxRows cap LARGER than the frame holds does not win
- BuildLayout survives a config with the sub-tables missing, on the shipped numbers
- Header buttons are created ONCE per index and re-pointed, never rebuilt
- A column that goes away HIDES its header; it does not destroy it
- Every header sits exactly over the column it labels, from the same layout
- The Player header is a Button like every other, not a label with a gap beside it
- The strip background and the per-column ones are mutually exclusive, both ways
- The sort arrow follows the LABEL, rather than sitting at a fixed offset
- The atlas rung flips ONE texture with SetTexCoord, and only for ascending
- With no art and no atlas the arrow is an ASCII character, and a legible one

### What must not change

BuildLayout (issue #42). The stored `col.width` is the shape a NEW column is born at, never the drawn width, and BuildLayout must neither read it nor write back to it — the drawn width is (frame.width - pad*2 - nameWidth - COLUMN_GAP*#visible) / #visible, floored, then clamped up to Const.COLUMN_MIN_WIDTH. The name column is subtracted from the available width and is NOT in the divisor, and it never grows with the frame. Two distinct reasons a stored entry is not drawn (`enabled == false`, and a stat absent from STAT_BY_KEY) both filter into the same `visible` list; a peel must keep both. Zero visible columns is a live arm: nothing may divide by #visible, rowWidth is the name column with no trailing seam, and minWidth still reserves math.max(#visible,1) columns of floor. `header.show == false` zeroes titleHeight only — headerHeight stays rowHeight * HEADER_ROW_FACTOR (1.0). rowWidth (x - COLUMN_GAP) and bodyWidth (frame.width - pad*2) are different numbers. maxRows: `fits` bottoms out at 1, a positive `rows.maxRows` wins only when it is SMALLER than what fits, and Const.MAX_ROWS is the final cap that keeps a corrupted config from asking the pool for thousands of frames. Every read is `x or <default>` and the defaults are the shipped window (694x220, pad 6, row 16, spacing 1, title 18, no cap = NAME_COLUMN_WIDTH); a helper handed a sub-table rather than the default would break a profile that lost one.

place() (issue #43). One widget per index, CreateFrame on the first pass only and re-point on every pass after — dressing must cost zero frames, and the surplus (`#layout.columns + 2` onward) is HIDDEN and kept, so a column toggled off and on hands back the same button. The name column's header is a Button with mmKey "name", an OnClick and mmWindow, exactly like a stat header. Position and size come off the one layout table (TOPLEFT to headerFrame at col.x, size col.width x layout.headerHeight, text width = col.width) so a header cannot drift from its column. The strip texture (headerBg) and the per-column button.bg are mutually exclusive and BOTH are written every pass — a mode switch must not leave the previous one drawn underneath; the name column never takes a per-column stat background. Colour resolution order is load-bearing: `tr,tg,tb,ta` are resolved into locals BEFORE the arrow branches, so the arrow always wears the same colour as its label (white on the Player header in stat mode). Arrow ladder, three rungs in order: NS.Icon("sort-up"/"sort-down") with SetTexCoord(0,1,0,1) and no flip; else Compat.FirstAtlas("auctionhouse-ui-sortarrow") flipped to (0,1,1,0) for ascending only; else the ASCII FontString with the exact strings "^" (ascending) and "v" (descending), given the strip's font before SetText. Exactly one of arrow/arrowTex is ever shown, and both are hidden on a non-sort column. The arrow is anchored LEFT to button.text at GetStringWidth() + 3 — the one measurement this file makes, of a FontString that has never held a value (rule R3).

### Risks and judgement calls

Verification note: I ran only tests/test_window.lua, through a throwaway copy of tests/run.lua in the scratchpad with SUITES reduced to that one suite, so nothing touched the files sibling agents are editing — 159 passed, 0 failed. luacheck on tests/test_window.lua is at zero warnings. Two small things the refactor wave should know: the file is LF and stays LF; and one assertion depends on the mock's GetObjectType() rather than a `__frameType` field (the base kit records `__frameType`, this repo's wow_mock records `__objectType` and exposes it only through GetObjectType). Issue #43's "math.abs rather than unary minus wherever a signed zero can reach a %.1f" has no referent inside place() — there is no math.abs anywhere in modules/Window.lua — so nothing was written for that clause; it belongs to another file and should be re-checked before the split cites it.

---

## `settings/ColumnBlocks.lua`

### Tests added (18)

- Blocks: a spec that is not a table is refused, and refused without touching the page
- Blocks: with AceGUI absent the page refuses rather than half-drawing
- Blocks: an empty item list still builds and finishes a controller
- Blocks: the boundary is a COUNT of enabled items, never a scan for the first disabled
- Blocks: the rule is an empty AceGUI Heading, sitting after the boundary block
- Blocks: no rule is drawn when there is no divide to mark, at either end
- Blocks: the label is gold when the column is shown and grey when it is not
- Blocks: the carried copy says the same thing the row does
- Blocks: every hidden row is registered, so the indices the library moves are the real ones
- Blocks: the geometry handed to the library is the published pair, not a private copy
- Blocks: the handle offers the localized drag tooltip, and the catalogued icon
- Blocks: the glyph sits clear of the library's handle gutter
- Blocks: a reused block comes back at full alpha
- Blocks: an item with no label draws an empty string, not a nil
- Blocks: CancelReorder survives a page that never rendered a list
- Blocks: cancelling twice releases the blocks once
- Blocks: the release is announced on the debug log, with the count
- Blocks: the returned list and the list parked on the ctx are two tables, same contents

### What must not change

Behaviours a refactor of NS.ReorderableBlocks MUST NOT change (now all pinned):

1. THE ENTRY GUARD IS ONE THREE-WAY TEST AND IT RUNS BEFORE ANY ctx WRITE. `if not (scroll and AceGUI and type(spec) == "table") then return {} end`. It returns an empty TABLE, never nil. Critically, it must stay above the `ctx.mmReorder = list` / `ctx.mmBlocks = live` assignments: a refusal that cleared those strands the previous render's blocks on AceGUI SimpleGroups the page is free to re-hand out, with nothing left holding a reference to release them — the ghost-label bug the file's header documents, arriving through the bad-input door.

2. THE BOUNDARY IS A COUNT, NOT A SCAN. It is `for _, item in ipairs(items) do if item.enabled then boundary = boundary + 1 end end`. The tempting simplification — break at the first disabled item — agrees on every normalized list and diverges on an unsorted one. The file's own comment says the ordering is normalizeColumns' guarantee rather than something arranged here, so the count is the contract. Pinned with an on/off/on fixture: boundary must be 2, not 1.

3. THE RULE. Drawn inside the loop under condition `i == boundary and boundary < count`, as an AceGUI "Heading" with SetText(""), SetFullWidth(true), SetHeight(12), added to the scroll immediately after the boundary block's slot. Both suppression arms matter and fail differently: all-enabled (boundary == count) and all-disabled (boundary == 0, so `i == boundary` never fires). Hoisting it out of the loop to append at the end draws it under the last block instead of the last enabled one.

4. A HIDDEN COLUMN IS REGISTERED BUT NOT DRAGGABLE. `list:AddRow` is called for EVERY item; only `draggable` varies. AddRow returns nil for a non-draggable row, so `blocks[i].mmHandle == nil` is true either way — a refactor that skipped AddRow for hidden rows passes the existing handle test while silently shortening the library's row list, breaking the indices and the clamp. Pinned directly on `ctx.mmReorder.rows`: #rows == #items, rows[i].index == i, rows[i].frame == blocks[i], and exactly 3 handles for the 3-enabled fixture.

5. NO `handleSize` IS PASSED. The gutter is the library's pinned `Widgets.ROW_BOX.HANDLE_W` (options-ui-§8); restating it here is a host copy of a pinned constant. Already pinned. The new companion case pins the glyph's LEFT inset as a RELATION (x > HANDLE_W) rather than as the literal 42, so the glyph stays outside the gutter if the collection ever retunes it.

6. THE GEOMETRY IS THE PUBLISHED PAIR. `stride = NS.BLOCK_STRIDE` on the descriptor, `height = NS.BLOCK_HEIGHT` on every row, slot height = NS.BLOCK_STRIDE, and NS.BLOCK_STRIDE == NS.BLOCK_HEIGHT + 4. settings/Columns.lua's suite computes drop distances from NS.BLOCK_STRIDE, so a literal written into the descriptor would drag correctly and make that suite lie.

7. THE GHOST DESCRIPTOR COMES OFF THE SAME ITEM THE BLOCK WAS APPLIED FROM. ghostText = item.label, ghostIcon = block.mmGlyphTexture (the value applyBlock just set, not a re-derivation), ghostTextColor = {1,0.82,0} enabled / {0.5,0.5,0.5} disabled. The split named in issue #44 puts drawBlock and registerRow in separate functions; they must still agree per row.

8. EXACT LABEL COLOURS: 1, 0.82, 0 when shown; 0.5, 0.5, 0.5 when hidden. Greyed, never hidden — a label you cannot read is a block you cannot aim at, and aiming at it is how the column is turned back on. Dimming by alpha on the block instead would take the glyph down with it.

9. `block.mmLabel:SetText(item.label or "")`. FontString:SetText(nil) raises in the client, and a column key that outlived its locale entry is how a nil label arrives. Must not become SetText(item.label).

10. applyBlock RESTORES ALPHA (`block:SetAlpha(1)`) AND CALLS Show(). The library restores its own row on Cancel, but the block that comes out of THIS file's pool has been through Hide/reparent/unanchor since; applyBlock is the only place that can speak for it.

11. AN EMPTY ITEM LIST STILL BUILDS AND FINISHES A CONTROLLER. No early return on count == 0: the ctx must end every render owning a live controller, because that is what the next repaint calls Cancel on. `list:Finish(scroll.content or scroll.frame)` runs unconditionally when a list exists.

12. CancelReorder IS TOTAL AND IDEMPOTENT. Safe on nil, on a bare table, and on a ctx that never rendered. releaseBlocks walks the parked list BACKWARDS clearing each slot as it goes, so a second Cancel finds nothing — a release that ran twice would push each block into the free list twice and hand one frame to two rows of the next render.

13. THE DEBUG LINE IS `NS.Debug("Blocks", "released %d blocks", n)`, gated on `NS.State.debug` AND on `n > 0`. A render that released nothing must stay silent, or every first paint logs a zero.

14. THE RETURNED LIST AND ctx.mmBlocks ARE TWO TABLES WITH THE SAME CONTENTS. `ctx.mmBlocks = blocks` would let the next release empty the caller's copy out from under it, and settings/Columns.lua keeps what it was given.

15. The library's `handleTooltip` (L["Drag to reorder"]) and `handleIcon` (NS.Icon("segment")) are passed once on the ReorderList descriptor and are visible nowhere else; dropping either loses the affordance or silently swaps the collection's shared handle art for the library fallback.

Also worth knowing for the refactor: the ENABLED_TEX/DISABLED_TEX pair is a ratified deviation from library-stack-§8 (docs/ARCHITECTURE.md deviation register) and moves only when ConsumableMaster's do — do not "fix" it into a catalog lookup during the split.

### Risks and judgement calls

Verification done: `luacheck tests/test_columnblocks.lua` is 0 warnings / 0 errors, and the suite alone runs 35 passed / 0 failed / 0 skipped against the UNREFACTORED settings/ColumnBlocks.lua. I ran the suite in isolation via a scratch copy of tests/run.lua with `suites = { "test_columnblocks" }, suiteInventory = false` (at /tmp/claude-1000/.../scratchpad/cb_only.lua), never `lua tests/run.lua`, so the concurrent sibling edits were not disturbed.

One thing that nearly shipped wrong and is worth flagging to the orchestrator: the repo is pinned `* text=auto eol=crlf` and tests/test_columnblocks.lua was CRLF on disk, but a heredoc append writes LF — which the kit's tests/_kit/test_eol.lua gate would have caught as a mixed-terminator file. I renormalized the added lines to CRLF; `git diff --stat` is 374 insertions and 0 deletions, so no existing line was touched. Any sibling agent that appended to a test file the same way has the same latent red.

Non-vacuity checks I made rather than assumed: NS.Icon("segment") resolves to a real path (Interface\AddOns\MultiMeters\libs\LibKa0s\media\icons\segment) and L["Drag to reorder"] resolves, so the handle-furniture assertions are not nil == nil; DebugLog:FindLine is proven to work by the positive assertion that follows the negative one in the same case; and the Heading/SimpleGroup case asserts a concatenated shape string, which would show a stray "Heading" rather than passing silently.

Residual risk: I did not run mutation checks against the source (the brief forbids touching settings/, and a temporary edit-and-revert is unsafe with agents working concurrently in the same tree), so the "red under" claims in the comments are reasoned from the code rather than demonstrated. The two I am least able to demonstrate are the alpha-restoration case (the library's Cancel also sets alpha 1 on its own row frame, so that case could in principle stay green with applyBlock's SetAlpha removed — it is still worth keeping, but the refactor wave should not treat it as proof) and the mmLabel:IsShown() line in the label-colour case, which only guards a refactor that hides the label outright.

Scope note: I did not add coverage for the drag mechanics themselves (LibKa0s-Widgets-1.0's ReorderList owns those and LibKa0s' own tests/test_widgets.lua covers them for every consumer), per the existing file header.

---

## `settings/Slash.lua`

### Tests added (11)

- Slash: `diag`, `recap` and `identity` each reach their OWN report and no other
- Slash: the three read verbs run with no debug console seam at all
- Slash: a read verb moves neither the console window nor the logging flag
- Slash: the debug sub-verb is matched case-insensitively
- Slash: `debug feign on` arms the recording and says exactly what to do next
- Slash: `debug feign off` stops the recording and says so
- Slash: the feign argument is case-folded, and a word after it is ignored
- Slash: a refused feign argument does not fall through to the console toggle
- Slash: a word the ladder does not know toggles the console, as a bare `debug` does
- Slash: with core/Diagnostics.lua absent the debug verbs go quiet, not through
- Slash: a Diagnostics too old to arm a trace reports off rather than promising one

### What must not change

The invariants a refactor of doDebug MUST NOT change, now each pinned by a case:

1. ORDERING (issue #45's "what must not change", and the reason the source comment repeats itself three times). `diag`, `recap` and `identity` run ABOVE `if not NS.DebugLog then return end`. Pinned by driving all three with `inst.NS.DebugLog = nil` and asserting each spy fired exactly once and nothing raised. A lookup table folded into the console ladder goes red here.

2. ONE VERB, ONE REPORT. `diag` → NS.Diagnostics.Report, `recap` → ReportDeathRecap, `identity` → ReportIdentity, each exactly once and the other two untouched. The issue's proposed `{ diag = "Report", recap = "ReportDeathRecap", identity = "ReportIdentity" }` table is exactly the change that can cross-wire two names while still printing something plausible.

3. THE READ VERBS RETURN. None of them may fall through to the console toggle: DebugLog:IsShown() and NS.State.debug are unchanged across all three.

4. THE FINAL ARM IS A TOGGLE, NOT A REFUSAL. `debug wibble` toggles the console window, the same as a bare `debug`. This asymmetry with `feign` is deliberate — `feign` takes an argument and can be typed wrong; the console verb never validated one. A table-driven rewrite that answers "unknown" for anything it cannot find changes long-standing behaviour.

5. THE UNKNOWN-FEIGN REFUSAL NAMES WHAT WAS TYPED (already pinned) AND RETURNS — it must not also move the console window. That is the new half.

6. EXACT OUTPUT STRINGS, both bytes-for-bytes: "feign trace ON \226\128\148 run the dungeon, then `/mm debug feign`." (the only place the player is told the trace is running and which command prints it) and "feign trace off." The em dash is U+2014, written as a byte escape in the test the way the source writes it.

7. LENIENT ARGUMENT PARSE. The whole remainder is lowercased and only the SECOND word is read: `feign ON` arms, `feign OFF now` disarms — neither is a typo and neither may become one. Likewise the verb word itself is case-folded (`debug DIAG` runs the report).

8. THE PRINTED LINE FOLLOWS WHAT ARMING RETURNED, not what was asked for. With D.ArmFeignTrace absent, `feign on` prints the OFF line — so nobody runs a dungeon for a trace that was never armed. The `X and X(...) or false` idiom is load-bearing.

9. GUARD PATHS. With NS.Diagnostics nil, all four verbs (`diag`, `recap`, `identity`, `feign`, `feign on`) return silently, do not raise, and do not reach the console toggle. With NS.DebugLog nil, the tail of the function returns rather than raising.

### Risks and judgement calls

Verification: `luacheck tests/test_slash.lua` is clean (0 warnings / 0 errors). I did NOT run the whole suite as instructed; instead I ran an isolated copy of tests/run.lua from the scratchpad with `suites = { "test_slash" }, suiteInventory = false`, which loads only tests/_kit, tests/wow_mock.lua and my file — 47 passed, 0 failed, against the UNREFACTORED settings/Slash.lua. The scratchpad runner is at /tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/2d592c46-51ce-4870-9011-1520eed0343d/scratchpad/run_slash.lua; nothing was added under tests/ except the block in test_slash.lua, so no other agent's inventory gate is disturbed.

Risk 1: docs/test-cases.md is generated from the registry by `lua tests/run.lua --list`. Eleven new cases means its body is now stale. I did not regenerate it (docs are outside my remit and other agents are adding cases concurrently) — the orchestrator should regenerate it once after every agent lands.

Risk 2: three of the new cases mutate the shared NS.Diagnostics table on their instance (spyReports replaces Report / ReportDeathRecap / ReportIdentity, and two tests null out ArmFeignTrace or NS.Diagnostics itself). Each uses a fresh `T.load()` and every temporary nil is restored before the assertions, including on the pcall paths, so nothing leaks to a later suite — but a future refactor of T.load() that shares one Diagnostics table across instances would break that assumption.

Risk 3: I deliberately pinned two lenient behaviours (`feign OFF now` ignoring the trailing word, and `debug wibble` toggling rather than refusing). These are characterization, not endorsement: if the refactor wave decides either should become a refusal, that is a deliberate contract change and the test should be updated in the same commit, not quietly deleted.

The file uses CRLF line endings; the inserted block was converted to CRLF to match, and nothing else in the file was touched or reordered.
