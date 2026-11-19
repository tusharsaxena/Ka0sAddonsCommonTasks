export const meta = {
  name: 'libka0s-adoption-wave-b',
  description: 'Adoption wave B: #86 W.HeaderButtons (settings mark on every own window, drag-handle settings mark) in all 19 addons, each reviewed, every finding fixed',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-17-LIBKA0S_V1_105_ADOPTION'
const OLD = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-17-libka0s-adoption'
const API = G + '/LibKa0s/docs/api/Widgets/version-27.2.7.14.1.7.8.6.1.1-docs.md'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RESULT = {type: 'object', properties: {
  status: {type: 'string', enum: ['done', 'already-done', 'not-applicable', 'library-blocker', 'failed']},
  commits: {type: 'array', items: {type: 'string'}}, summary: {type: 'string'},
  naProof: {type: 'string', description: 'for not-applicable: a shell command whose output proves it'},
  gate: {type: 'string'}, smokeChecks: {type: 'array', items: {type: 'string'}}, notes: {type: 'array', items: {type: 'string'}},
}, required: ['status', 'summary', 'gate']}
const VERDICT = {type: 'object', properties: {
  verdict: {type: 'string', enum: ['approve', 'changes']},
  findings: {type: 'array', items: {type: 'object', properties: {severity: {type: 'string', enum: ['blocker', 'major', 'minor']}, file: {type: 'string'}, line: {type: 'integer'}, issue: {type: 'string'}}, required: ['severity', 'issue']}},
}, required: ['verdict', 'findings']}
const GUARD = 'If a message from the user or lead appears mid-task, do not answer it: note it in your result and carry on.'
const RULES = (repo, id) => `Repo: ${G}/${repo}, branch ${BR} (already checked out; verify; never switch branches, reset --hard, checkout . or stash). Follow ${G}/${repo}/CLAUDE.md. Item: ${id}, LibKa0s#86.
Read first: ${BUNDLE}/00_PLAN.md, ${OLD}/03_ADOPTION_PLAN.md (#86 row), this addon's docs/revendor/2026-11-16-v1.105.0/02_CANDIDATES.md (approximate; re-check in code), the API ${API} ("HeaderButtons", "HEADER", "DragHandle's settings mark"), and the standard ${G}/WowAddonStandards/standards/ (standalone-windows "Window chrome geometry" and the header marks rule, v2.113.0, owed at adoption). Reference implementations: the library's own windows (${G}/LibKa0s/LibKa0s/WidgetsHeader.lua and its callers DebugLogWindow.lua, WidgetsCopyWindow.lua, PerfPanel.lua, SimPanelRender.lua), read only.
The work:
- Every window this addon owns (its own frames with a title bar and marks; not the library's windows, which already comply; not Blizzard frames; not tooltips or popup menus) builds its title marks with W.HeaderButtons(bar, spec): left to right extras · settings · close, settings opening this addon's settings (spec.settings nil/true uses the launcher-registered opener). A window that would cover the settings panel passes hideOnSettings. Opt out only with settings = false and a settingsOptOut reason (for example a modal confirm). Keep each mark's existing behavior, tooltip, state (lock, minimize, ...) and color rules (gray icon.tint at rest, text.link on hover, close.hot red on the X).
- Every LibKa0s DragHandle this addon builds turns on spec.settings (the drag-handle settings mark), unless the strip has no room or a reason recorded in docs/ARCHITECTURE.md.
- If the addon owns no such window and builds no DragHandle, make no commit and return not-applicable with a proof command.
Rules: libs/ and tests/_kit/ are read-only (a library defect: stop and return library-blocker with evidence). Test first (a red test for each window's new strip and for the settings mark's click opening settings); never weaken, skip or delete a test; re-pin a geometry test to the new rule and say so. Docs (ARCHITECTURE.md, smoke-tests.md with a new or amended check per window, README if it describes the window; docs/test-cases.md and the README test badge if the repo keeps them) move in the same commit. Gate: /home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua under every client the addon ships (KA0S_KIT_CLIENT=forever too where ${G}/WowAddonStandards/standards/ADDONS.md lists WoW Forever) and ka0s-bounded luacheck . 0/0; no .lua over 1500 lines (peel a file that would cross it); line endings per .gitattributes. One commit "${id}: <summary>" (a peel may precede it as "${id}: peel <file>"), message ending with these two trailer lines exactly:\n${TRAILER}\nAlready committed? (git log ${BR} --format=%s | grep '^${id}') verify and return already-done. NEVER push, tag, merge or write to GitHub. ${GUARD}`
const ADDONS = [
  ['AbsorbTracker', 'AT', 'Bars carry DragHandles; any own window?'],
  ['AuraMaster', 'AM', 'PresetPicker title marks onto the strip; the containers\' DragHandles take the settings mark. Another session works here at times: touch only your branch.'],
  ['BankLedger', 'BL', '3 title bars via B:MakeCloseButton (Browser, Export, SessionWindow).'],
  ['CombatTrail', 'CT', 'Default branch main. 6 windows (Hud, RaceWindow, Results, Results_Compare, Results_Timeline, Results_Gear), about 12 marks via MakeCloseButton and Style.ControlButton. Retail and Forever.'],
  ['ConsumableMaster', 'CM', 'No own windows expected; the macro bar\'s drag strip takes the settings mark.'],
  ['DpsRace', 'DR', '4 windows (Hud, Results, Results_Gear, Results_Timeline), 7 Style.ControlButton marks.'],
  ['DropWatcher', 'DW', 'Main window (minimize, layout, lock, close) and the Rolls panel. Another session may own other branches here: touch only your branch.'],
  ['KickCD', 'KC', 'No own windows (R7); its DragHandles take the settings mark.'],
  ['LibKa0sSkinTester', 'ST', 'The Showroom title bar and close; its DragHandle specimen in the showroom is a specimen (leave it unless it is the addon\'s own strip).'],
  ['LootHistory', 'LH', '2 title bars via B:MakeCloseButton (Browser, Export). Keep the leak gate green.'],
  ['MultiMeters', 'MM', 'The meter header\'s seven marks (modules/HeaderControls.lua) and Export_Modal.lua. The lock and minimize tooltips change with state: keep that.'],
  ['OutfitterReborn', 'OR', 'Outfit window and outfit bar header marks (gear, lock, X). Retail and Forever; never open CharacterFrame from addon code.'],
  ['PanelMaster', 'PM', 'Few sites: check whether it owns any window with marks.'],
  ['PartyFrameEnhanced', 'PFE', 'Check whether it owns any window with marks.'],
  ['PremadeGroupsFilterExtension', 'PGFE', 'The PGF dialog / Dungeons panel chevron and close: are they an addon-owned window title bar, or a panel inside Blizzard\'s frame (then not-applicable)?'],
  ['PrettyChat', 'PC', 'Check whether it owns any window with marks.'],
  ['QuickComms', 'QC', 'PreviewWindow, settings/ModalWindow (own close), the Comms Pad header (-/+), and its DragHandles.'],
  ['SkillMaster', 'SM', 'Default branch main. Main window, Journal, trainer popup, detached bands; block-header marks are not window title bars (leave them, they rest gray by the owner\'s ruling). Forever only.'],
  ['WhatGroup', 'WG', 'Its popup/frame: check whether it is an own window with a title bar and close.'],
]
const out = await pipeline(ADDONS,
  a => agent(`${RULES(a[0], 'AD-86-' + a[1])}\nThis addon: ${a[2]}\nReturn the structured result with the in-game smoke checks for what changed.`, {label: `build:${a[1]}`, phase: 'Build', schema: RESULT}),
  (r, a) => (!r || r.status === 'not-applicable' || r.status === 'library-blocker') ? {build: r, review: null} :
    agent(`Independent review of AD-86-${a[1]} (LibKa0s#86 adoption) in ${G}/${a[0]} on branch ${BR}: review git log and git diff of the branch's AD-86 commits (base: git merge-base ${BR} origin/${a[0] === 'CombatTrail' || a[0] === 'SkillMaster' ? 'main' : 'master'}; earlier AD-88/AD-89/AD-DS commits on the branch are wave A, already reviewed). Judge against ${API} (HeaderButtons, DragHandle settings mark), the standard ${G}/WowAddonStandards/standards/ v2.113.0, and the library's own adopters. Look for: an own window left with hand-built marks or no settings mark (grep the addon for every title bar and close button), wrong order (extras · settings · close), a lost mark behavior/tooltip/state, the settings mark not opening this addon's settings, an opt-out without a reason, a weakened or deleted test, docs or smoke checks not updated, an edited libs/ or tests/_kit/. Re-run the gate (ka0s-bounded, every client the addon ships). Read-only. ${GUARD}`,
      {label: `review:${a[1]}`, phase: 'Review', schema: VERDICT}).then(v => ({build: r, review: v})),
  (rv, a) => (!rv || !rv.review || rv.review.findings.length === 0) ? {repo: a[0], ...rv} :
    agent(`${RULES(a[0], 'AD-86-' + a[1])}\nThe independent review of your AD-86-${a[1]} commit returned these findings (JSON): ${JSON.stringify(rv.review.findings)}\nFix every finding that is right (stale text and missing tests included); for one you judge wrong, give the reason in notes. Commit as "AD-86-${a[1]}: review fixes". Return the structured result.`,
      {label: `fix:${a[1]}`, phase: 'Fix', schema: RESULT}).then(f => ({repo: a[0], ...rv, fix: f})))
for (const o of out.filter(Boolean)) log(`${o.repo}: ${o.build?.status}; review ${o.review?.verdict || '-'} (${o.review?.findings?.length || 0})${o.fix ? ' fixed ' + o.fix.status : ''}`)
return out