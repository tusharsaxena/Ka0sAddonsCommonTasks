# R1-kit-console-sim: LibKa0s #75, #90, and the LibKa0s part of #78

Research is read-only. Repos were read on their default branches. LibKa0s is at master `9bc9cc51`
(v1.104.0, Kit.VERSION 56), WowAddonStandards at `3dfb951` (v2.112.2), and dev-copilot at `793a277` (2.10.0).

---

## 1. #75: test kit `unregisterAll` + weak frame registries

### 1a. Half 1 (the unregisterAll guard) is ALREADY DONE

- `testkit/mock_ace.lua:110-128`: `Callbacks:unregisterAll` already guards both loops
  (`if list[target] ~= nil then list[target] = nil end`). `Callbacks:unregister` (`:97-108`) is guarded too.
- Landed in **kit revision 51** by commit `367a9f10` ("LK-K1: Kit revision 51 clears a callback only
  where one exists, as CallbackHandler does", 2026-11-05). CHANGELOG.md:496 records it.
- There is already a regression test: `tests/test_mock_ace.lua:336-372`, "ace: unregistering targets that
  hold no registration leaves a send in flight intact". It covers both the `UnregisterMessage` and the
  `UnregisterAllMessages` paths with 40 ghost targets to force the rehash.
- `testkit/README.md:28` already documents it ("An unregister clears only a registration that exists ...
  (kit revision 51)").
- **Action:** none in code. Tick the first acceptance box on the issue with a pointer to `367a9f10` and
  the case name. The issue was filed at kit rev 50, which is why it still reads as open.

### 1b. Half 2 (frames held only by weak registries are collected) is STILL OPEN

Evidence:
- `testkit/mock_base.lua:259`: `frameSet = setmetatable({}, { __mode = "k" })`. Every tracked frame goes
  in here (`trackFrame`, `:260-268`), and `M.__registrations()` / `M.__fire()` walk it
  (`testkit/mock_record.lua:553-563` reads `ctx.frames`, which is `frameSet`, published at `mock_base.lua:670`).
- A raw frame registration is stored **on the frame itself** (`f.__frameEvents` / `f.__unitEvents`,
  `mock_base.lua:234-240`). So the only kit-side reference to a frame that a suite registered but does
  not hold is the weak `frameSet`. The next GC frees it, `M.__fire` no longer finds it, and its events
  silently stop.
- `mock_base.lua:415` `eventRegistry` (weak-keyed) is **not** a delivery path. AceEvent dispatch goes
  through the CallbackHandler fake's `self.events[eventname][target] = fn` lists (`mock_ace.lua:79-95`),
  which are plain strong tables. An AceEvent-embedded *target* therefore stays alive while it holds a
  registration, and `eventRegistry` is only the recorder. The issue names it, but **only `frameSet`
  needs to change**. The other kit weak tables (`mock_record.lua:61` ids, `:686` AceGUI type map,
  `secrets.lua:65`, `loader.lua:20`) are surveys, not delivery paths. `EventRegistry`
  (`mock_events.lua:66`) and the bucket set in mock_record are strong.
- Consumer workaround: OutfitterReborn `0694218` ("FU: Hold the mock-gear listener's frame so a GC
  cycle cannot drop it"; `tests/test_mock_gear.lua:36-37`, and `:83` forces `collectgarbage`).

Constraint from the kit's own history: `tests/test_mock_base.lua:321-340` ("a dropped mock build takes
every target embedded in it with it") pins that **a dropped build must be collectable** (kit rev 22 leaked
685 MB through a process-wide weak table whose value reached its key). Any strong hold must therefore
live **inside the build closure (per `M`)**, never in a module-level table.

#### Proposed design (recommended: hold while registered, per build)

In `testkit/mock_events.lua`'s `Events.decorateFrame(M, f)` (already wraps `RegisterEvent` /
`RegisterUnitEvent` with `M` in scope, `:42-54`):

- Keep a per-build strong set, `M.__heldFrames = M.__heldFrames or {}`, created in `mock_base`'s builder
  beside `frameSet`.
- `RegisterEvent` / `RegisterUnitEvent` set `held[f] = true` after the name passes `isBad`.
- Also wrap `UnregisterEvent` and `UnregisterAllEvents`. After the stub runs, `release(f)` drops
  `held[f]` when both `f.__frameEvents` and `f.__unitEvents` are empty.
- `mock_ace.lua:247-259` `unregisterAllEvents` replaces the method on an *embedded frame* and resets the
  two raw tables directly, so it must call the same release. Publish it as `M.__releaseFrame(f)`, or
  reach it via `buildOf(self.__events)`.
- Leave `frameSet` weak. That keeps the "a frame nobody holds is not kept alive by the survey" property
  for frames that never registered anything.

Alternative B is simpler: hold forever once registered, for the build's life. It never releases, so it
cannot miss a reset path (three paths clear registrations today: the stub's two methods and mock_ace's
embedded override). It is also faithful in the sense that the client never frees frames. Cost: a frame
that unregistered stays in `frameSet`, and then in `M.__shownFrames()` if it is still shown. That is
what the client would show too, but it could turn a consumer's "nothing on screen" assertion red where
the frame was dropped rather than hidden.

Alternative C is to make `frameSet` strong. This is the most faithful option (the client never frees
any frame), but it widens the change to every frame, registered or not, and risks the most
consumer-suite verdict changes. Not recommended.

Recommendation: **A** (hold while registered), matching the issue's "strongly hold a frame while it has a
live event registration".

#### Tests (in `tests/test_mock_base.lua` 574 lines or `tests/test_mock_events.lua` 209; both far from band)
1. Register a raw frame with no local holding it (build it inside a closure that returns nothing). Run
   `collectgarbage("collect")` twice, call `M.__fire(event)`, and assert that the handler ran once (an
   upvalue counter in its OnEvent). Without the hold this is red deterministically, as Outfitter's
   forced-GC case proved.
2. The same for `RegisterUnitEvent`.
3. Release: register, then `UnregisterEvent` (and in a second case `UnregisterAllEvents`, and in a third
   the embedded-frame `UnregisterAllEvents` from mock_ace). Watch the frame through a weak sentinel,
   GC, and assert it was collected.
4. Extend the dropped-build case (`test_mock_base.lua:321`) with a registered raw frame and assert that
   it is collected with its build. This guards the per-build placement.

#### Version / ripple
- `Kit.VERSION` 56 -> **57** (`testkit/framework.lua:20`). New `docs/api/testkit/version-57-docs.md`,
  with version 56 marked superseded. Add a row to `testkit/README.md`'s file table (the `mock_events.lua`
  / `mock_base.lua` rows). Add a CHANGELOG kit entry. Re-copy into `tests/_kit/`, which
  `tests/test_kitsync.lua` gates.
- File sizes stay fine: `mock_events.lua` 148 -> ~180, `mock_ace.lua` 820 -> ~822, `mock_base.lua` 679 -> ~682.
- No LibStub minor moves (the kit is not payload).
- Consumers owe only the re-vendor, plus a full-suite run to catch any verdict change. Outfitter's
  hold becomes redundant but harmless. Offer its removal as an adoption item, not this run.

#### Risks
- A consumer suite that relied, unknowingly, on GC dropping a registered frame (for example a teardown
  check that counts `__registrations()` after letting a frame go out of scope) now sees the
  registration and turns red. That is correct behavior, but it surfaces at re-vendor. Mitigation: run
  every consumer's gate in the re-vendor milestone (the plan does this anyway).
- `Events.decorateFrame` is also reached by `M.__stubFrame()` frames built for the Ace fakes
  (`mock_ace.lua:746`, `AceAddon.frame`). They are held only while registered, so there is no change
  unless they register.

---

## 2. #90: debug console status line onto `W.Footer` (24 px)

### Current state (evidence)
- `LibKa0s/DebugLogWindow.lua:81` `STATUS_H = 16`. `:383-441` `buildBody` anchors the log and the
  scrollbar `STATUS_H + 4` above the bottom, draws `f.statusDivider` by hand (a 1 px texture, inset 8 px
  each side, at y=STATUS_H, `:429-434`), and draws `f.lineCount` (a FontString in `ctx.d.font` mono at
  `ctx.fontSize`, RIGHT at `-COUNT_INSET` (22), y 3, `:436-441`).
- `:85` `COUNT_INSET = 22` already equals Widgets' `FOOT_GRIP` (`Widgets.lua:753`). The Widgets API doc
  says so: the GRIP row in `docs/api/Widgets/version-27.1.6.13.7.8.5-docs.md:43`.
- `:320-322` `consoleMinHeight = TITLE_H + 6 + MIN_LINES*(fs+2) + STATUS_H + 4`.
- `:604-611` calls `core.MakeResizable(f, {minWidth, minHeight, onResize, owner})` with the grip on `f`.
- Palette `:133-146`: `rule = {"divider", {0.24,0.24,0.27,0.85}}` and `count = {"log.count", {0.6,0.6,0.62}}`.
- `:529-547` `adopt()` calls `S.Divider(f.statusDivider)`. `:510-527` `recolor()` calls `setText(f.lineCount, pal.count)`.
- Shell: `LibKa0s/DebugLog.lua:530-533` `D:UpdateStatus()` writes `frame.lineCount:SetText(...)`. No
  shell change is needed if `f.lineCount` keeps pointing at the counter FontString.
- Load order is fine: `LibKa0s/LibKa0s.xml:33` Widgets.lua loads before `:40-43` DebugLog*.lua.
  `DebugLog.lua:33` already resolves Widgets (optional) for the copy window.
- Footer: `LibKa0s/Widgets.lua:748-899`. `FOOT_H 24, PAD 8, GRIP 22`. With no owner, `footText` uses
  `GameFontHighlightSmall` in `FOOT_TEXT {0.7,0.7,0.72}` (text.muted's Ka0s Default). With an owner,
  `skinFooter` (`:834-839`) runs `S.Text(foot.right, "muted")`, which paints color **and the skin's body
  font** (`SkinPaintExtras.lua:718-731`, `P.font(... "body")`) and is replayed on every skin switch.
  `opts.resize` builds the grip on the footer (`footResize`, `:844-853`) and passes `resize.owner`
  through when the host sets it (`if o.owner == nil then o.owner = owner end`).
- Consumers: no addon references `statusDivider` / `lineCount` outside `libs/` (git grep over every
  sibling's HEAD). Only LibKa0s's own suites pin them:
  `tests/test_debuglog.lua:258` (`lineCount.SetText`), `:751` (`statusDivider ~= nil`),
  `tests/test_tool_windows_skin.lua:164-165, 205, 210-214, 232, 246-247` (count = `log.count`, the 0.6
  constant, and the rule = `divider`).
- Standard: standalone-windows *The footer* (v2.110.0) says "Every window that has one, a host's window or
  a library's, MUST build it with ... Footer". It requires left/right text in `text.muted`, 24 px,
  a 1 px hairline "inset to the window edge", the grip in the corner, and "A window the library draws is
  the library's to move, in the same release". Anti-pattern #118 covers "text in a color other than the
  muted token". debug-logging-§11 (`debug-logging.md:282`) requires the counter to be "a 1px divider plus
  a right-aligned label in the same monospace font". skinning's Leave classes keep the monospace face.

### The three decisions the issue asks for

| Decision | Options | Recommendation |
|---|---|---|
| **Counter face** | (a) keep the descriptor's mono face (`ctx.d.font`, `ctx.fontSize`); (b) take the footer's body face | **(a) mono.** debug-logging-§11 and §2 make it a MUST, and skinning lists the mono face as a Leave class. The footer table says nothing about face, so there is no conflict. |
| **Counter color** | (a) `text.muted` (the footer rule; Ka0s Default 0.7/0.7/0.72); (b) keep `log.count` (0.6/0.6/0.62) | **(a) `text.muted`.** Anti-pattern #118 names any other color. In every non-Default skin `log.count` already aliases to `text.muted` (`SkinDefsOthers.lua:169`), so the only visible move is Ka0s Default and unowned consoles going from 0.60 to 0.70 gray. **Keep the `log.count` token defined** (it is skin data; retiring it is a Skin/SkinDefs minor and a contrast-table edit in `test_tool_windows_skin.lua:413,441`). Record it as "no longer read by the console" and leave its retirement as a follow-up. |
| **Min height** | (a) keep `MIN_LINES = 4`; the minimum grows 8 px (`STATUS_H` 16 -> `FOOTER.HEIGHT` 24); (b) cut to 3 lines to hold the old minimum | **(a).** Derived, not tuned. With `fontSize` 12 the minimum goes from 112 to 120 px. **The default 700x344 stays**: debug-logging-§1 states the 344 normatively, so changing it needs a standard edit. The visible log loses 8 px, about half a line, at default size. |

Further calls I would take myself (flag to owner only if they disagree):
- **Left text: empty.** There are no new strings and no localization. The footer's left slot stays "".
- **Divider inset: the footer's 1 px**, so the hairline now runs to the window edge (today it is 8 px in
  each side). The rule says "inset to the window edge".
- **Counter vertical position:** the footer centers it in 24 px (today it sits 3 px off the bottom). Accept.

### Proposed implementation (recommended: Option A', no Widgets minor)

In `DebugLogWindow.lua` (WINDOW_MINOR 4 -> **5**):
- Resolve `W = LibStub("LibKa0s-Widgets-1.0", true)` at call time.
- Build `local foot = W.Footer(f, { resize = { minWidth, minHeight, onResize, owner = S and d.addonName or nil } })`
  **with no footer `owner`**. The console keeps doing its own skin job, as it does for every other part.
  The footer then draws Ka0s Default constants, and the console paints:
  - `foot.right:SetFont(ctx.d.font, ctx.fontSize, "")` (mono), colored from the palette (`count` re-pointed
    to `{"text.muted", {0.7,0.7,0.72}}`, which is the same entry as `rest`);
  - in `adopt()`, `S.Divider(foot.line)` replaces `S.Divider(f.statusDivider)`. `recolor()` keeps
    `setText(f.lineCount, pal.count)`.
- Keep aliases for the shell and the tests: `f.footer = foot`, `f.lineCount = foot.right`,
  `f.statusDivider = foot.line`. `DebugLog.lua` does not change, so the shell minor stays at 22.
- Log and scrollbar bottom anchors: `W.FOOTER.HEIGHT + 4` (or a local `FOOTER_H = 24`, read from
  `W.FOOTER.HEIGHT` when present). `consoleMinHeight` uses the same figure.
- Retire `STATUS_H`, `COUNT_INSET` and the direct `core.MakeResizable` call. The grip now comes from
  `opts.resize`, which keeps the guard: `footResize` returns nil on a Core without `MakeResizable`.
- Guard: `if not (W and type(W.Footer) == "function") then` build no footer (`f.lineCount` stays nil and
  `UpdateStatus` no-ops, `DebugLog.lua:531`). Under whole-folder vendoring and LibStub's highest-minor
  rule, any client that loads this file has Widgets >= 27, so the guard only covers a Widgets load failure.
  Not worth keeping the hand-drawn path as a fallback.

Why not pass the owner to `W.Footer` (Option B)? `skinFooter`'s recorded `S.Text(foot.right, "muted")`
would put the body face on the counter and replay it on every switch. The console would have to re-set the
mono face after each replay (in its `OnLooksChanged` handler, which runs after the replay per
`DebugLogWindow.lua:507`) and after "Ignore fonts". Two writers would fight over one FontString. The clean
version of B is a **Widgets minor 28** option such as `opts.face = { right = { path, size, flags } }`, a
line held to a host face and tinted color-only. That is a Widgets API addition, plus a doc, a members JSON
and tests. It is worth it only if a second window wants a mono footer line. **Recommend A' now**, and
note B as the route if Drop Watcher or Combat Trail later need a mono count.

### Tests (peel first)
- `tests/test_debuglog.lua` is 1002 lines, accepted in the band (`CLAUDE.md:302`) with its trigger
  "1100 lines, **or the next console case added**", and the seam named: "the close-button factory across
  a Core upgrade section (`coreCopy`, `loadSkewed` and their cases, from about line 585)".
  - **Peel commit (pure move):** lines 586-647 (section header, `Loader`/`buildMocks` locals,
    `CORE_SRC`, `coreCopy`, `loadSkewed`, the two `dbg:` cases at 631 and 639) go to a new
    `tests/test_debuglog_coreskew.lua`. Add it to `tests/run.lua:100`'s list after `test_debuglog`,
    regenerate `docs/test-cases.md` (CRLF), and update the `CLAUDE.md:302` census row (the file leaves the
    band at about 940; record the exit as the v1.91.0 peels paragraph does). A suite is not payload, so a
    peel is no release. Check the new file's prologue: it needs whatever `test`/`assert*` globals the parent
    gets from the runner.
  - Then add the new console cases, in `test_debuglog.lua`'s console-window section (`:399`) or a new
    `tests/test_debuglog_footer.lua`. A new suite keeps test_debuglog out of the band for good.
    **Recommendation:** the new suite.
- New cases:
  1. The console's footer is a `W.Footer`: `f.footer` exists, its height is `W.FOOTER.HEIGHT` (24),
     `f.lineCount == f.footer.right` and `f.statusDivider == f.footer.line`.
  2. The counter is in the descriptor's mono face at `fontSize` (a survey of `SetFont`), right-aligned, and
     its color is `text.muted`'s constant (0.7, 0.7, 0.72) on an unowned console.
  3. The log and the scrollbar end `FOOTER.HEIGHT + 4` above the bottom. `minHeight` equals
     `TITLE_H + 6 + 4*(fs+2) + 24 + 4` (a survey of the MakeResizable opts, or the grip's recorded bounds).
  4. The grip is the footer's (`f.footer.grip` non-nil when Core has `MakeResizable`), with the owner
     passed on an owned console.
  5. Owned console: the hairline is painted `S.Divider`, and after a skin switch the counter is
     `text.muted` of the new skin and still mono, also under "Ignore fonts".
- Edits to existing pins: `tests/test_tool_windows_skin.lua:164, 205, 246-247` change `log.count` to
  `text.muted`, and `:232` changes `"0.600,0.600,0.620,1"` to `"0.700,0.700,0.720,1"`. `:165, 214` keep
  working through the `statusDivider` alias. `test_debuglog.lua:751` keeps working (update its message to
  "the footer's hairline").

### Version / ripple
- **DebugLog key 22.10.1.4 -> 22.10.1.5** (only `WINDOW_MINOR` moves). Write
  `docs/api/DebugLog/version-22.10.1.5-docs.md` ("What changed": the footer, the counter color, the min
  height). Mark the old document superseded. Add the `api/README.md` row, run
  `lua tools/gen-api-members.lua` (members-22.10.1.5.json; no member moves, but the gate regenerates and
  compares), and add the CHANGELOG version block. Widgets stays 27.x under A' (Widgets 28 under B).
- CHANGELOG / release ANALYSIS: close v1.103.0's "open and not ratified" note on the console footer.
- **Standard ripple (small, optional):** debug-logging-§11's "A thin bottom status bar — a 1px divider
  plus a right-aligned label" could read "the window's footer (standalone-windows, *The footer*), its right
  text the count in the same monospace font", with a pointer to the LibKa0s release. Also check
  standalone-windows' "same release" clause for wording that implies the console already complies. This
  is a WowAddonStandards patch, so mind the version-collision memory: fetch and renumber before finalize.
- `docs/releasing.md` Consumers table: no change, since no consumer drives this.
- Consumers: re-vendor only. No consumer code or test touches these frames.
- Owner smoke, Retail and Forever: open `/x debug`. Check the 24 px footer, the full-width hairline, the
  mono `N / 3000 lines` counter clear of the grip, the resize floor (4 lines), and a skin switch plus
  Ignore fonts (counter stays mono and recolors).

### Deviation-row alternative
If the owner prefers to keep the 16 px line, add a `## Documented deviations` row in LibKa0s
`CLAUDE.md`: `standalone-windows` (*The footer*), "the debug console's status line is 16 px, hand-drawn,
counter in log.count", why = "debug-logging-§11 predates the footer; console is a tool window", trigger =
"the next DebugLogWindow minor". **Not recommended:** the change is about 40 lines of payload, and the
rule's same-release clause was written for exactly this window.

---

## 3. #78 (the LibKa0s part): SimPanel default title should say SIM

- `LibKa0s/SimPanel.lua:594-599` `title(P)` falls back to `tostring(P.ctx.d.name) .. " - Simulation"`.
- Every live host sets an explicit SIM title, so nobody sees the default: AbsorbTracker
  `modules/Sim.lua:181`, BankLedger `:391`, DpsRace `:272`, KickCD `:392`, LootHistory
  `modules/SimPanel.lua:97`, MultiMeters `:311`, CombatTrail `:332`, DropWatcher (master)
  `modules/SimPanel.lua:125`. All read "<Brand> - SIM".
- Proposed change: add a string `PANEL_TITLE = "%s - SIM"` to the `lib.STRINGS` loop at `:141-151`, so a
  host can override it like every other panel string. `title()` then returns
  `P.ctx.tr("PANEL_TITLE"):format(tostring(P.ctx.d.name))`. Check that `tr` answers a format string; it
  does for `PANEL_START = "Start: %s"`. The simpler alternative is to change the literal to `" - SIM"`.
  Recommend the string key: it costs one line and honors localization.
- **Sim key 2.3.10.3 -> 2.3.11.3** (`SIM_PANEL_MINOR` 10 -> 11, `SimPanel.lua:66`). Write
  `docs/api/Sim/version-2.3.11.3-docs.md`, whose descriptor table row (old doc `:622`,
  `` `title` | `name .. " - Simulation"` ``) becomes `name .. " - SIM"` (Since 11). Add the members JSON
  and a CHANGELOG entry. `docs/releasing.md` step 5's "preview and simulation re-look" applies: re-read
  `tests/fixture_sim_panel.lua` and `tests/test_sim_*.lua`. The consumer list is empty in effect, because
  every host overrides the title.
- Test: `tests/test_sim_panel_controls.lua:17-27` changes its name and its `"Host - Simulation"`
  assertion to `"Host - SIM"`. Add one assertion that a host-overridden `PANEL_TITLE` string is used.
  The override half (`"Brand - Simulation"`) is host-chosen text and can stay, or move to `"Brand - SIM"`
  for consistency.
- File size: SimPanel.lua is 679 lines, out of the band.

---

## 4. #78: the WowAddonStandards and dev-copilot items (triage)

| Item | Repo | State today | Size | In this run? |
|---|---|---|---|---|
| M-2 `clients.md:30` "The library reads `WOW_PROJECT_ID` once" | WowAddonStandards | **Still wrong.** `LibKa0s/Compat.lua:105-112` reads it on every `isForever()` / `isRetail()` call | 1 line + changelog patch bump | **Yes**, trivial. Wording: "The library reads `WOW_PROJECT_ID` on each call, against the project constants, and owns the nil-tolerance of `WOW_PROJECT_CAMELOT`." |
| M-4 clients-§4 promises no Retail-only bindings on Forever, but `Bindings.xml` entries still list in Blizzard's panel | WowAddonStandards | Open. clients.md:42-47 lists "a key binding" as a gated feature | a note of a few lines | **Yes, as a note only** ("a `Bindings.xml` entry is listed by the client regardless; the descriptor gate keeps the action from binding/doing anything; a per-client Bindings file is step 5's design"). Designing a fix is out of scope. |
| M-5 Retail-only exclude names only `camelot`; consider `camelot, forever` | WowAddonStandards + WG, PGFE (+ DpsRace, now Retail-only: `DpsRace.toc:3`) | Open. All three TOCs read `## ExcludeLoadGameType: camelot` | small, but touches 3 addon TOCs | **Recommend NO / defer.** `forever` is not a game-type token anyone has verified exists. clients.md:87 and toc-file.md:71 rest on the wiki's names, and open-evolutions.md:356 already carries the Forever gate as "verify at first smoke". An unrecognized name in an exclude list is harmless, but adding an unverified token is guesswork. Leave it as an owner decision: record it in open-evolutions, or close it as will-not-do. |
| open-evolutions.md:13 "sixty-seven" | WowAddonStandards | **Already fixed.** `grep -i sixty` finds nothing in the file | none | Tick the box on the issue. |
| `scripts/bump_interface.py` has no Clients awareness | dev-copilot | Partly addressed: since `609445c` (WFP-DC-02) and `3f93791` (SM-0.2, 2.9.0) it bumps per slot and never invents a slot (`bump_interface.py:2-12, 30-44`). It still does not read ADDONS.md's Clients column | small (a roster cross-check plus a test in `scripts/test_bump_interface.py`) | Optional. Recommend **close as covered** (the slot logic plus the command doc asking is enough), or a ~30-line roster check if the owner wants it. |
| `profiles/wow/bump-version.md` hardcodes 120105/16001 | dev-copilot | Open (`profiles/wow/bump-version.md:77`, "as of 2026-11-07; ask the owner when not certain") | 1-2 lines | Yes if dev-copilot is touched anyway. Reword to "the current Live values (ask the owner when not certain, never guess)", with no numbers. |
| Releases report table has no game-versions column | dev-copilot | Open. `scripts/curseforge_journal.py:711` header `| Addon | Version | Release Date | Downloads | ... |`; `gameVersions` is already captured (`:478, 484`; tests at `test_curseforge_journal.py:237-245`) | ~10 lines + a test | Small. Yes if dev-copilot is touched. It needs a dev-copilot patch version, and the owner updates the installed plugin (memory: use the installed plugin). |

Overall: the standard items (M-2 wording, M-4 note, and ticking the "sixty-seven" box) are one
WowAddonStandards patch release, about 10 lines. The dev-copilot items are one patch release, about 40
lines with tests. Both fit in the same run as leaf items with no dependency on the LibKa0s release. They
**do** add two more repos to the branch/merge set, and the standard is prone to version collisions with
other sessions.

---

## 5. Summary of LibKa0s minors / revisions that move (this researcher's scope)

| Thing | From | To |
|---|---|---|
| `Kit.VERSION` (#75 half 2) | 56 | 57 |
| `DebugLogWindow.lua` `WINDOW_MINOR` (#90) | 4 | 5 (DebugLog key 22.10.1.4 -> 22.10.1.5) |
| `SimPanel.lua` `SIM_PANEL_MINOR` (#78) | 10 | 11 (Sim key 2.3.10.3 -> 2.3.11.3) |
| Widgets | 27 | unchanged (28 only under #90 option B) |

No new payload file and no new major. One new suite (`tests/test_debuglog_coreskew.lua`), plus
optionally `tests/test_debuglog_footer.lua`.

## 6. Open questions for the owner (decisions, with recommendations)

1. **#90 counter color: `text.muted` (0.70 gray, rule-compliant) or keep `log.count` (0.60)?**
   Recommend `text.muted`, keeping the `log.count` token defined and unread.
2. **#90 counter face: keep the mono face?** Recommend yes (debug-logging-§11 MUST).
3. **#90 min height: keep 4 log lines (minimum +8 px) and the 700x344 default?** Recommend yes.
4. **#90 build route: A' (no Widgets change; the console paints the footer's parts itself) or B (Widgets
   minor 28 adds a host-held face option)?** Recommend A'.
5. **#90: footer or deviation row?** Recommend the footer.
6. **#75 hold policy: while registered (A) or once registered, for the build's life (B)?** Recommend A.
7. **#78 standard M-5 (`camelot, forever`):** recommend defer or will-not-do until the token is verified
   in a client. **M-2 and M-4:** do them in this run as one standard patch. **dev-copilot nits:** do the
   game-versions column and the hardcoded-number wording in this run if the owner accepts a dev-copilot
   patch release. Close bump_interface's Clients awareness as covered.
8. **#75 half 1:** tick it as done by kit rev 51 (`367a9f10`). There is nothing to build.
