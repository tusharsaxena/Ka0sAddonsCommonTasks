# 06 — In-client smoke tests

The owner runs these in game; no agent marks one passed. Result column: `owed` until the owner reports.
Grouped by repo and item, in plan order. Checks marked *outcome A only* apply only if LK-11 made `W.StepPanel` public.

## LibKa0s

| check | item | what to verify | result |
|---|---|---|---|
| SM-LK-1 | LK-11 | SM-LK-1 (outcome A only): in any roster addon, /<slash> perf shows the step panel looking identical to v1.74.0: same dots, colors, row height, command column, gold hover, red cancel hover, close mark top right | owed |
| SM-LK-2 | LK-11 | SM-LK-2 (outcome A only): drag the perf panel's resize grip: width changes, height stays pinned, rows stretch | owed |
| SM-LK-3 | LK-11 | SM-LK-3 (outcome A only): an addon that passes decorate (its own corner) shows no library close mark and its decoration still works | owed |
| SM-LK-4 | LK-19 | in any roster addon carrying v1.75.0, /<slash> debug diag: the 'LibKa0s running:' header lists Glow 1 and Sim 1 / SimTimeline 1 / SimPanel 1 when another addon (or this one) registered them | owed |
## dev-copilot

| check | item | what to verify | result |
|---|---|---|---|
| SM-DC-1 | DC-04 | After dev-copilot 2.4.0 is merged and pushed, the owner runs /plugin update dev-copilot and /reload-plugins. The reload line shows the expected plugin/skill/agent/hook counts, and the installed ~/.claude/plugins/cache/dev-copilot/dev-copilot/2.4.0/commands/wow-revendor-libka0s.md contains 'prune-icons'. | owed |
## AbsorbTracker

| check | item | what to verify | result |
|---|---|---|---|
| SM-AT-1 | AT-RV | /console scriptErrors 1, then /reload twice with AbsorbTracker enabled: no Lua error and no LibKa0s minor-mismatch line in chat. | owed |
| SM-AT-2 | AT-RV | /at debug opens the debug console. Its title bar draws the close X, COPY and CLEAR icon marks as art, not blank squares. Click Copy: the Copy window opens and its close X draws. | owed |
| SM-AT-3 | AT-RV | /at perf opens the perf step panel (or whichever /at perf verb shows it). Its close X draws and closes the panel. | owed |
| SM-AT-4 | AT-RV | /at unlock: each enabled bar's drag handle shows the ? help mark and the X close mark as art. Hovering each shows its tooltip, and clicking X turns that bar off as before. /at lock afterwards. | owed |
| SM-AT-5 | AT-RV | /at config: every page (About, General with both tabs, Appearance with all five tabs, Profiles) renders as before, with no blank icon anywhere. | owed |
## AuraMaster

| check | item | what to verify | result |
|---|---|---|---|
| SM-AM-1 | AM-RV | /reload with AuraMaster enabled: no Lua error; /am help, /am diagnostics and the settings panel open as before | owed |
| SM-AM-2 | AM-RV | /am debug on, then open the console: the title-bar close X, COPY and CLEAR buttons each draw an icon, not a blank square (declared close, copy, clear survived the prune) | owed |
| SM-AM-3 | AM-RV | /am unlock: every container's handle draws its ? help mark and its X close mark; hover the X and the tooltip is unchanged | owed |
| SM-AM-4 | AM-RV | Settings > Containers > Filters > Overrides (a blacklisted spell that a category claims) and General > Spell Categories (a claimed spell): the entry's help mark draws the library's info art, not blank and not the client's blue disc | owed |
| SM-AM-5 | AM-RV | /am perf start, then open the perf panel: its close X draws an icon | owed |
| SM-AM-6 | AM-RV | The Interface > AddOns folder Interface/AddOns/AuraMaster/libs/LibKa0s/media/icons holds only close, copy, clear, help, info .tga and LICENSE-open-iconic.txt (no phosphor/ or game-icons/ folder) and the zip is about 28 MB smaller | owed |
## BankLedger

| check | item | what to verify | result |
|---|---|---|---|
| SM-BL-1 | BL-RV | /bl debug: the console's close, copy and clear marks draw (not blank) and work | owed |
| SM-BL-2 | BL-RV | /bl show: the title-bar close, the column sort arrows, the group chevrons (open and shut), the dropdown chevron and multi-select tick, and the search magnifier all draw | owed |
| SM-BL-3 | BL-RV | Export: the dialog's export mark draws, and the CSV copy window's library close draws and closes it | owed |
| SM-BL-4 | BL-RV | /bl session: the session window's close X draws | owed |
| SM-BL-5 | BL-01 | Export a History slice that holds an upgraded gear row to CSV: its Wowhead URL carries ?bonus=<ids> in link order, and a trade-good row carries a plain item=<id> URL | owed |
| SM-BL-6 | BL-02 | /bl show: the search box looks as before (flat gray, magnifier, 'Search items…'), and clicking into it lights its border gold; Escape and Enter drop focus and the line goes back to gray | owed |
| SM-BL-7 | BL-02 | Typing filters the History table after the short debounce, the suggestion list still opens under the box at its width, and picking a name applies it at once | owed |
| SM-BL-8 | BL-03 | /bl test: an amber strip with the info mark reads 'TEST MODE: a sample ledger, not your bank. Combat ends it.' directly under the filter bar, the History table starts below it, and the red TEST MODE badge is still on the title | owed |
| SM-BL-9 | BL-03 | The Insights tab is shifted down by the same amount while test mode is on | owed |
| SM-BL-10 | BL-03 | Entering combat ends test mode: the strip hides and both panes move back up | owed |
| SM-BL-11 | BL-03 | Hovering the strip shows its tooltip (Test mode / Shows: a sample ledger / Ended by: combat, /bl test, the launcher menu) | owed |
| SM-BL-12 | BL-03 | Opening the window while test mode is already on shows the strip at once | owed |
| SM-BL-13 | BL-04 | Esc > Options > Key Bindings > AddOns > 'Ka0s Bank Ledger' lists 'Toggle the ledger window' with no default key; bind one, then pressing it opens and closes the ledger window once per press | owed |
| SM-BL-14 | BL-04 | /bl disable, then press the key: exactly one line, the standard disabled refusal; the window does not open; /bl enable restores it | owed |
| SM-BL-15 | BL-04 | The key opens and closes the window in combat (non-secure window, no taint error) | owed |
| SM-BL-16 | BL-05 | Regression: a bank visit (character bank and warband deposit and withdrawal, gold both ways) and a guild-bank visit record exactly as before, and the session window opens and closes with the frames | owed |
| SM-BL-17 | BL-08 | With the addon loaded normally, /bl show, a bank visit and a guild visit behave exactly as before (the idle seam is invisible) | owed |
| SM-BL-18 | BL-13 | /bl sim start bank: the ledger window opens with the amber 'Simulation: Bank - nothing here is saved.' strip, the step panel docks beside it, and Run all fills History, Insights and the Current Banking Session window; /bl sim stop restores the real ledger and the real row count is unchanged | owed |
| SM-BL-19 | BL-13 | Each refusal prints its one line: in combat; with test mode on; with the real bank or guild bank open; with General visibility keeping the window shut; while /bl disable is in force | owed |
| SM-BL-20 | BL-13 | /bl sim start warband: the deposit's warband half lands about 1.5 s later and the row appears only then; the alt's withdrawals carry 'Simbanker-<realm>' and the alt's class color | owed |
| SM-BL-21 | BL-13 | /bl sim start guild (also on an unguilded character, which shows 'Simulated Guild'): the first step (guild data while away) records nothing; the guild rows carry the guild name | owed |
| SM-BL-22 | BL-13 | /bl sim start onesided: no rows are recorded; the debug log (/bl debug on) shows the held change dropped at close | owed |
| SM-BL-23 | BL-13 | With a simulation running, opening the real bank stops it at once (stop line printed) and the real visit records normally; entering combat stops it; /reload ends it and nothing simulated remains | owed |
| SM-BL-24 | BL-13 | Panel click-ahead: clicking a later row runs every step up to it in order, waiting while the ledger settles; a completed row's tooltip says when it ran and what it recorded | owed |
| SM-BL-25 | BL-13 | /bl purge during a simulation prints 'Stop the simulation first.' and no confirm opens; /bl test during a simulation is refused | owed |
| SM-BL-26 | BL-13 | The panel position after a drag is kept for the session only; after /reload it docks beside the ledger window again | owed |
| SM-BL-27 | BL-13 | 12.1.5 check: watch /bl debug on during a REAL warband deposit and record which events fire (PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED, BANK_TABS_CHANGED?); if they differ from modules/SimDrivers.lua's list, file the one-line correction | owed |
## ConsumableMaster

| check | item | what to verify | result |
|---|---|---|---|
| SM-CM-1 | CM-RV | /cm debug on -> the console title bar's copy, clear and close marks draw as light-gray square marks, never blank (re-run DIAG-10) | owed |
| SM-CM-2 | CM-RV | press Copy -> the copy window's close mark draws; /cm perf -> the perf panel's close mark draws (re-run DIAG-31, DIAG-21) | owed |
| SM-CM-3 | CM-RV | /cm unlock -> the macro bar handle shows its help mark and the X close mark left of it, neither blank (re-run BAR-9, BAR-10) | owed |
| SM-CM-4 | CM-RV | the segment drag handle draws on Macros priority rows, AIO section rows, Stat Priority secondaries and Macro Bar -> Buttons rows (re-run PRIO-8, BAR-16) | owed |
| SM-CM-5 | CM-RV | a Macros tab row's blue info score button shows the library info art, and its click still opens the score tooltip (re-run PRIO-14) | owed |
| SM-CM-6 | CM-RV | the new DIAG-42 check (every declared LibKa0s mark draws after the prune), with no Lua error on /reload | owed |
## DropWatcher

| check | item | what to verify | result |
|---|---|---|---|
| SM-DW-1 | DW-RV | /reload with Drop Watcher alone on the v1.75.0 payload: no Lua error, no new chat line; /dump LibStub.minors['LibKa0s-Widgets-1.0'] -> 13 and LibStub.minors['LibKa0s-Options-1.0'] matches the v1.75.0 key (record INSTALL-5). | owed |
| SM-DW-2 | DW-RV | every declared icon draws (none blank): title-bar minimise/add and fullscreen-enter/exit, the lock badge, group-header and footer chevrons (down/right/up), the dropdown chevron and tick, action buttons (chat, confirm, clock, reset, ban, external-link, speech-bubble, people, link-intact, edit, transfer, cancel), tooltip marks (arrow-up/down/right, transfer), the item-cell help fallback, and the /dw test banner's info mark. | owed |
| SM-DW-3 | DW-RV | the library-drawn set draws: the debug console's close, copy and clear (/dw debug), the perf panel's close (/dw perf), and the main window's close mark. | owed |
| SM-DW-4 | DW-02 | re-run SIM-1 on the library session: /dw sim start dungeon prints DW's own start line (nothing is sent, saved history untouched); each refusal (group, instance, combat, test mode, second start) prints its existing line; join a group -> stopped with the group line; /dw disable -> stopped with the disabled line; after /reload no simulation runs. | owed |
| SM-DW-5 | DW-02 | /dw sim start key then /dw sim run: steps play 2 s apart (the sim.stepDelay setting still applies), pause/resume/restart work; /dw sim restart prints the library's restart stop line (accepted change, OWNER_SCOPE C.7) and starts the same scenario again. | owed |
| SM-DW-6 | DW-03 | /dw sim (bare) prints status and usage and opens the panel; /dw sim start key, step, pull, kill, loot 3, lockdown on, trade, status, stop each print the same lines as before; /dw sim bogus prints usage; /dw sim start nosuch prints the library's unknown-scenario line plus the names (accepted change, C.7); /dw sim run while disabled prints the one refusal line. | owed |
| SM-DW-7 | DW-04 | /dw sim panel: the panel docks beside the window (right, else left, else centre +420), shows Start, the steps and Stop with the done tick, ready/busy/locked/cancel colours and hover; buttons are now the library's default buttons and tips GameTooltip lines (accepted change, C.7); the panel gains a width grip. | owed |
| SM-DW-8 | DW-04 | pick Raid in the picker -> the size dropdown appears (Random, 9, 12, 15, 19); Start; click a step two ahead -> every step up to it plays in order; Pause/Resume/Restart/Stop; the panel grows with the rows without empty space. | owed |
| SM-DW-9 | DW-04 | drag the panel, /reload -> it docks beside the window again (position is session-only now; nothing written to SavedVariables); /dw disable while open hides it; /dw sim panel while disabled is refused. | owed |
| SM-DW-10 | DW-05 | the whole Simulator theme (SIM-1..SIM-13, plus SIM-14..SIM-16 added by DW-02..DW-04) re-run on the library, owner-run; record results in docs/smoke-tests.md and the bundle's smoke file. | owed |
| SM-DW-11 | DW-06 | /dw test, full layout: the amber strip under the filter bar looks as before (info mark, gold text, same tooltip); a long text now truncates with an ellipsis instead of overflowing. | owed |
| SM-DW-12 | DW-06 | compact layout at 380 px: the short text wraps to two lines and the panes move down; at 520 px it is one line. | owed |
| SM-DW-13 | DW-06 | combat ends test mode: the strip and its reserve go; the TEST MODE title word still shows while test mode is on, including minimised. | owed |
| SM-DW-14 | DW-07 | the filter bar's search box looks as before (flat dark box, gray line, `Filter looter or item…` hint); focus lights the line gold and blur restores it; typing filters live; Enter and Escape drop focus; in compact layout the box moves into the Filters panel with its hint (FB.Anchor) and still filters. | owed |
| SM-DW-15 | DW-08 | each of the four glow styles (rotating rays/button, proc flash, pixel border, sparkles/autocast) on the Drops row, the compact card and the detail header, for main and off-spec, with each knob slider restarting the glow; the proc burst plays once per drop. | owed |
| SM-DW-16 | DW-09 | Key Bindings -> AddOns -> Ka0s Drop Watcher lists `Toggle Drop Watcher window` with no default key; bind one; a press opens the window and a second press closes it (one toggle per press), in and out of combat. | owed |
| SM-DW-17 | DW-09 | /dw disable, press the key -> exactly one disabled refusal line and no window; /dw enable, start /dw perf capture, press -> exactly `Not available during a performance capture.` and no toggle. | owed |
## KickCD

| check | item | what to verify | result |
|---|---|---|---|
| SM-KC-1 | KC-RV | /kcd debug window -> the title bar's copy, clear and close are three small white glyphs, not a multiplication sign or the words Copy/Clear (re-run DIAG-21); click copy -> the copy window's close is the white glyph (DIAG-22); /kcd perf start -> the step panel's one close control is the white glyph (DIAG-23) | owed |
| SM-KC-2 | KC-RV | /kcd unlock -> the icon grid strip's and the cast bar strip's ? mark draws as the white help glyph (GRID-14, CAST-9/10) | owed |
| SM-KC-3 | KC-RV | /kcd config -> Spells page -> each row's drag handle draws the segment glyph and each row's remove mark is the red-tinted close glyph, not Blizzard's transmog-icon-remove atlas (SPELLS-13, SPELLS-14) | owed |
| SM-KC-4 | KC-RV | /kcd diagnostics -> the identity header lists the running LibKa0s majors including LibKa0s-Glow-1.0 and LibKa0s-Sim-1.0 with their minors, and no Lua error | owed |
| SM-KC-5 | KC-RV | Interface\AddOns\KickCD\libs\LibKa0s\media\icons holds exactly clear, close, copy, help, segment .tga plus LICENSE-open-iconic.txt (no phosphor/ or game-icons/ folder), and the addon loads with no missing-texture green squares anywhere | owed |
| SM-KC-6 | KC-01 | Grid -> Icons -> Ready glow, primary trigger always, an interrupt off cooldown: cycle the style through Button, Proc, Pixel border and Autocast for the PRIMARY slot, then the SECONDARY slot -> each draws as before the change, the proc burst plays once per start, and switching style leaves no stale glow of the previous style | owed |
| SM-KC-7 | KC-01 | with a pixel-style primary glow showing, move Pixel lines / frequency / thickness and untick the dark border -> the running glow restarts at once with the new knobs (re-run GRID-19); /kcd set units.target.icons.primaryGlowPixelLines 900 still clamps to 20 (GRID-20) | owed |
| SM-KC-8 | KC-01 | primary trigger target_casting_interruptible -> target a hostile caster: the glow lights only on interruptible casts and an uninterruptible cast neither glows nor shows (interruptible-only mask unchanged) | owed |
| SM-KC-9 | KC-01 | rename libs/LibCustomGlow-1.0 aside and /reload, /kcd debug on -> one '[Init] LibCustomGlow-1.0 absent; no icon glows' line and no Lua error with a ready interrupt (DEGRADED path); restore the folder | owed |
## LootHistory

| check | item | what to verify | result |
|---|---|---|---|
| SM-LH-1 | LH-RV | /lh toggle: the title-bar close mark draws on the History window and on the Export window (close). | owed |
| SM-LH-2 | LH-RV | /lh debug: the console's close, copy and clear marks draw; /lh perf panel's close draws. | owed |
| SM-LH-3 | LH-RV | History row right-click menu shows marks on Link to chat, Show in Timeline, Blacklist item/currency and Delete; Holdings row menu shows Show in Timeline and Forget this character marks. | owed |
| SM-LH-4 | LH-RV | column sort arrows (up and down) and group-header chevrons (right and down) draw in the History and Holdings tables; the Bound lock mark draws in the History table and its legend. | owed |
| SM-LH-5 | LH-RV | filter-bar dropdowns draw their chevron and the multi-select tick; the Export window's Export to CSV button shows its spreadsheet mark. | owed |
| SM-LH-6 | LH-RV | Settings > AH Price tab: the leading tick (circle-check / ban) and each row's info button draw, the cascade reorder handle (segment) draws; Filters tab id lists show their info help marks. | owed |
| SM-LH-7 | LH-01 | Settings > General > AH Price tab, switch to another General tab and back several times, then close and reopen the panel: the price-sources table draws once, in place, never orphaned or doubled. | owed |
| SM-LH-8 | LH-02 | /lh, Export, History data set as CSV: an item with bonus IDs (e.g. a dungeon drop) has a wowhead.com/item=<id>?bonus=a:b:c URL whose ids match the item; a plain item has a bare item=<id> URL. | owed |
| SM-LH-9 | LH-03 | /lh toggle, click the Search box on History, Insights, Timeline and Holdings: its bottom line lights gold while focused and returns to grey on Esc/Enter; the 'Search items…' hint hides while text is present; filtering and the autocomplete list still work. | owed |
| SM-LH-10 | LH-04 | /lh test: an amber strip with the info mark reading 'TEST MODE: a sample loot history, not yours. Combat ends it.' sits under the filter bar, the History table starts under it, and the red TEST MODE badge is still beside the title. | owed |
| SM-LH-11 | LH-04 | in test mode the Insights, Timeline and Holdings tabs are shifted down the same way. | owed |
| SM-LH-12 | LH-04 | entering combat (or /lh test again) removes the strip and the badge, and every pane moves back up. | owed |
| SM-LH-13 | LH-04 | hovering the strip shows its tooltip (Test mode / what it shows / what ends it). | owed |
| SM-LH-14 | LH-05 | Esc > Options > Keybindings > AddOns > Ka0s Loot History lists 'Toggle Loot History window' with no key; bind one and press it twice: the History window opens, then closes. | owed |
| SM-LH-15 | LH-05 | /lh disable, press the key: exactly one disabled refusal line, no window. /lh enable. | owed |
| SM-LH-16 | LH-05 | during /lh perf start (perf hold only), press the key: exactly one 'Not available during a performance capture.' line and no window; never the disabled line. | owed |
| SM-LH-17 | LH-05 | the key still works in combat (the History window is non-secure), subject to the General visibility setting's own refusal line. | owed |
| SM-LH-18 | LH-06 | regression: kill a mob and loot it, open a lockbox, take mail and buy from a vendor: rows record with the same sources as before (KILL with npcID detail, CONTAINER, MAIL, VENDOR); zone and subzone columns still fill. | owed |
| SM-LH-19 | LH-07 | regression after the dispatch refactor: one session of normal play (loot, merchant sell and buy, mailbox, auction post, bank deposit) records the same rows as before; /lh disable then /lh enable resumes capture; with gains and losses off only loot rows appear. | owed |
| SM-LH-20 | LH-14 | /lh sim start loot outside any instance and group: the panel docks beside the History window, the start line says nothing is saved, the SIMULATION badge and strip show; /lh sim stop ends it with one line. | owed |
| SM-LH-21 | LH-14 | refusals: /lh sim start loot in combat, in an instance, in a group, with test mode on, with the mailbox open, and right after login: each prints its one line; ah with gains and losses off refuses. | owed |
| SM-LH-22 | LH-14 | each scenario (loot, key, vendor, ah, bank, social) run with Run all: the expected rows appear in History, Holdings and Timeline. | owed |
| SM-LH-23 | LH-14 | during a simulation, loot a real mob: the simulation stops ('world') and the real loot is recorded live. | owed |
| SM-LH-24 | LH-14 | after a simulation, /reload: the real history, holdings and timeline are exactly as before; no sim rows remain. | owed |
| SM-LH-25 | LH-14 | the panel follows the run, clicking a row ahead runs the steps in between, settling shows while the ledger settles, and the panel position is forgotten on /reload. | owed |
| SM-LH-26 | LH-14 | /lh purge, Forget this character and row Delete each refuse with their line while a simulation runs. | owed |
## MultiMeters

| check | item | what to verify | result |
|---|---|---|---|
| SM-MM-RV-1 | MM-RV | Every header control draws its icon, not a blank square: close, minimise and then expand when collapsed, lock and unlock, settings, segment, reset, export. Also check Settings -> Header -> Controls, where each checkbox label carries its icon. | owed |
| SM-MM-RV-2 | MM-RV | Column headers show the sort-up/sort-down arrow art. The Columns editor's block handle shows the segment glyph. | owed |
| SM-MM-RV-3 | MM-RV | /mm export opens the modal. The three selectors draw the chevron, and the 'Export to CSV' and 'Print to Chat' buttons show the spreadsheet and chat icons. The CSV copy window's close X draws. | owed |
| SM-MM-RV-4 | MM-RV | Open the debug console (/mm debug): the close, copy and clear buttons in its title bar all draw. Open the perf panel (/mm perf start, then show it): its close X draws. | owed |
| SM-MM-RV-5 | MM-RV | In the settings panel, scroll a long page, then trigger a structural refresh (for example add or remove a column on the Windows page). The scroll position is kept (LibKa0s v1.73.0 Options 29 behaviour). | owed |
| SM-MM-1 | MM-01 | /mm test with the header shown. A yellow strip ('TEST MODE: placeholder numbers, not your fight. Combat ends it.') sits under the title. The column headers sit under it, no row overlaps it, and the red TEST MODE title marker and the session-line 'Test' are still there. | owed |
| SM-MM-2 | MM-01 | Hide the header (Settings -> Header), then /mm test. The strip is at the very top of the window, so the window is still marked as test data. | owed |
| SM-MM-3 | MM-01 | Make a window narrow. The strip text truncates with '...' inside the frame and never spills past the window edge. | owed |
| SM-MM-4 | MM-01 | /mm test off. The strip goes, the column headers and rows move back up, and the visible row count returns. | owed |
| SM-MM-5 | MM-01 | Minimize a window while in test mode. The strip hides with the body; expand, and it is back. | owed |
| SM-MM-6 | MM-01 | Test mode on, pull a training dummy. One 'Test mode off - combat started' line prints, the strip disappears, and the window does not jump, re-skin or change scale or position. | owed |
| SM-MM-7 | MM-01 | Drag a window down to its minimum height in test mode. The resize floor does not move, the strip takes the room of the one row, and the window size saved after test mode ends is the size you dragged to. | owed |
| SM-MM-8 | MM-02 | Key Bindings -> AddOns lists a 'Ka0s Multi Meters' header with one 'Toggle meter windows' entry and no key preassigned. | owed |
| SM-MM-9 | MM-02 | Bind a key and press it. Every meter window hides; press again and they show, the same as /mm toggle. One press toggles once. | owed |
| SM-MM-10 | MM-02 | /mm disable, then press the key. Exactly one chat line ('Ka0s Multi Meters is disabled - enable it with /mm enable'), and no window appears. | owed |
| SM-MM-11 | MM-02 | Start a perf capture (/mm perf start), then press the key. Exactly the line /mm toggle prints during a capture, once, and the windows do not change. | owed |
| SM-MM-12 | MM-02 | Press the key in combat. The windows toggle with no error and no taint message (non-secure window). | owed |
## PanelMaster

| check | item | what to verify | result |
|---|---|---|---|
| SM-PM-1 | PM-RV | `/pm debug`: the console title bar shows the copy, clear and close marks (gray, white or red on hover). It must not show blank squares, the words Copy/Clear, or a multiplication sign. This re-runs smoke-tests.md DIAG-2 against the pruned media/icons/. | owed |
| SM-PM-2 | PM-RV | Log in with only PanelMaster plus its libs (and again with the full Ka0s set). No Lua error from the new LibKa0s-Glow-1.0 / LibKa0s-Sim-1.0 files or from anything else at load or on the first `/pm`. | owed |
| SM-PM-3 | PM-RV | In the Panels page, scroll down and change a field that re-renders the page (for example the edge checkboxes). The page keeps its scroll position (Options minor 29) and does not jump to the top, and a tab click still starts at the top. | owed |
## PartyFrameEnhanced

| check | item | what to verify | result |
|---|---|---|---|
| SM-PF-1 | PF-RV | `/pfe debug on`, open the debug console -> the title bar's Copy and Clear controls and the close x draw as icons (not blank squares, not text labels); Copy opens the copy window and its close x draws too | owed |
| SM-PF-2 | PF-RV | `/pfe perf` -> the step panel's close x draws as an icon, matching the console's (DIAG-3) | owed |
| SM-PF-3 | PF-RV | SM-PF-3 (INSTALL-4 on v1.75.0): log in, `/reload` twice -> no Lua error and no LibKa0s missing/older-module line; `/pfe config` draws every page as before; `/pfe status` prints; `/pfe unlock` unlocks the frames | owed |
## PremadeGroupsFilterExtension

| check | item | what to verify | result |
|---|---|---|---|
| SM-PG-1 | PG-RV | /pgfe debug -> the console's title bar draws the clear, copy and close glyphs (none blank, no fallback 'x'); Copy opens the copy window and its close glyph draws too | owed |
| SM-PG-2 | PG-RV | /pgfe config -> Region colors tab, scroll down, change a color, Defaults on another tab and back -> the page keeps its scroll offset (Options 29) and nothing errors | owed |
| SM-PG-3 | PG-RV | re-run DEGRADED-1 (rename libs/LibKa0s, /reload): one missing-library line, /pgfe config says the panel is unavailable, no Lua error; restore the folder | owed |
## PrettyChat

| check | item | what to verify | result |
|---|---|---|---|
| SM-PC-1 | PC-RV | /reload with PrettyChat enabled shows no Lua error; /pc config opens the landing page, General, Categories and Profiles; /pc test prints the preview. | owed |
| SM-PC-2 | PC-RV | /pc debug opens the console; the copy, clear and close marks draw as three square icons (DIAG-17 re-check after the prune). A blank control means an undeclared name was pruned. | owed |
| SM-PC-3 | PC-RV | the console's Copy window draws its close mark and closes on click. | owed |
| SM-PC-4 | PC-RV | SM-PC-4 (Options minor 29): on a long Categories page, scroll down and change a setting that re-renders the page. The scroll position is kept, not reset to the top. | owed |
## QuickComms

| check | item | what to verify | result |
|---|---|---|---|
| SM-QC-1 | QC-RV | /reload with no Lua error; Groups -> callout popup -> icon browser lists all three sets (Open Iconic, Phosphor, Game-icons) and its glyphs draw, search included (nothing was pruned) | owed |
| SM-QC-2 | QC-RV | library-drawn art still draws: /qc debug console's close, copy and clear marks; the export copy window's close; the When tab id list's info mark (Groups -> When); the pads' padlock and the dial's arrows and pointer | owed |
| SM-QC-3 | QC-01 | Pad -> Icons, Glow on: each style (Pixel border, Auto cast sparkles, Button, Proc) x Always / On hover / After sending on a pad and on a dial looks as before; Proc's burst plays once, not on every rebuild | owed |
| SM-QC-4 | QC-01 | Pad -> Buttons, button glow on: each style circles the whole pad button and coexists with the icon glow on the same button | owed |
| SM-QC-5 | QC-01 | in combat, hover a pad button and a dial wedge with On hover -> the glow starts and stops, no Lua error, no taint message | owed |
| SM-QC-6 | QC-02 | start a perf capture from /qc perf's step panel, then press the Toggle Comms Pads key, type /qc toggle and /qc test -> each prints 'Not available during a performance capture.' once and nothing toggles; finish the capture -> the key toggles the pads again | owed |
| SM-QC-7 | QC-02 | /qc disable, press the Toggle Comms Pads key -> the disabled line (unchanged, KEY-3) | owed |
## WhatGroup

| check | item | what to verify | result |
|---|---|---|---|
| SM-WG-1 | WG-RV | /wg debug -> the console's copy, clear and close controls are square marks (DIAG-12); a blank square means the declaration missed a name the library draws | owed |
| SM-WG-2 | WG-RV | click the console's copy control -> the copy window's close control is the same square mark, not blank and not a multiplication sign (DIAG-13) | owed |
| SM-WG-3 | WG-RV | cold login with the pruned payload -> no Lua error, no blank chrome anywhere (INSTALL-1 rerun); /wg diagnostics header lists the LibKa0s majors including Glow and Sim | owed |
| SM-WG-4 | WG-RV | scroll the General settings page down, run /wg profile Alt then /wg profile Default -> the page keeps its scroll offset (Options 29 structural refresh) | owed |
| SM-WG-5 | WG-01 | Esc > Options > Key Bindings > AddOns > 'Ka0s WhatGroup' lists 'Toggle group popup' with no key preassigned; bind a key | owed |
| SM-WG-6 | WG-01 | press the key with no capture -> the popup opens on its 'No data' fallbacks; press again -> it closes (ESC/Close semantics, test mode ends if on); one press toggles once | owed |
| SM-WG-7 | WG-01 | /wg test, then press the key -> the sample popup closes and test mode ends, as the menu's Show window does | owed |
| SM-WG-8 | WG-01 | /wg disable, press the key -> exactly one chat line 'Ka0s WhatGroup is disabled - enable it with /wg enable', no popup; /wg enable | owed |
| SM-WG-9 | WG-01 | press the key in combat -> it opens/closes exactly as the launcher's Show window does in combat (no ADDON_ACTION_BLOCKED, no taint line); /reload keeps the bound key | owed |
## AuraMaster

| check | item | what to verify | result |
|---|---|---|---|
| SM-AM-1 | AM-01 | AuraMaster test mode shows a visible TEST marker in every layout (only if AM-01 found a gap) | owed |

## Execution notes (CT-01, 2026-10-23)

These notes do not change any result; every check above stays `owed` until the owner reports.

- **SM-LK-1, SM-LK-2, SM-LK-3** are "outcome A only". LK-11 took outcome B (`99_EXECUTION_RECORD.md`), so
  the perf panel was not rebuilt and these three do not apply. The owner strikes them.
- **SM-LK-4:** the local tag moved twice after this file was written (LK-26, LK-27). At the final tag
  `9e5c4e2` the header should list Glow 1, Sim 2, SimTimeline 2 and SimPanel 2, not Sim 1 / SimTimeline 1 /
  SimPanel 1.
- **SM-AM-1 appears twice.** The second one, in the last AuraMaster section, is AM-01's check. AM-01 found
  the gap (a locked test mode showed no TEST marker) and fixed it in `ffe08ae`, so that check applies.
- The addendum items (LK-26, LK-27 and every `-RV2`/`-RV3` refresh) add no smoke check of their own. The
  Sim minor 2 and SimPanel minor 2 behaviour is exercised by SM-DW-4..10, SM-LH-20..26 (LH-14) and
  SM-BL-18..26.
