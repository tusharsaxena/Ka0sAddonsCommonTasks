export const meta = {
  name: 'libka0s-adoption-wave-a',
  description: 'Adoption wave A: default skin (MM PGFE WG), #88 docked test/sim strip, #89 W.Footer in 13 addons, each with an independent review',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-17-LIBKA0S_V1_105_ADOPTION'
const OLD = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-17-libka0s-adoption'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RESULT = {type: 'object', properties: {
  items: {type: 'array', items: {type: 'object', properties: {
    id: {type: 'string'}, status: {type: 'string', enum: ['done', 'already-done', 'not-applicable', 'library-blocker', 'failed']},
    commit: {type: 'string'}, summary: {type: 'string'}, naProof: {type: 'string', description: 'for not-applicable: a shell command whose output proves it'},
  }, required: ['id', 'status', 'summary']}},
  gate: {type: 'string', description: 'tests run/failed/skipped per client profile, luacheck totals, largest .lua file'},
  smokeChecks: {type: 'array', items: {type: 'string'}, description: 'the in-game checks the owner should run, one line each, naming the window and what to look for'},
  notes: {type: 'array', items: {type: 'string'}},
}, required: ['items', 'gate', 'smokeChecks']}
const VERDICT = {type: 'object', properties: {
  verdict: {type: 'string', enum: ['approve', 'changes']},
  findings: {type: 'array', items: {type: 'object', properties: {severity: {type: 'string', enum: ['blocker', 'major', 'minor']}, file: {type: 'string'}, line: {type: 'integer'}, issue: {type: 'string'}}, required: ['severity', 'issue']}},
}, required: ['verdict', 'findings']}

const GUARD = 'If a message from the user or lead appears mid-task asking a question, do not answer it: note it in your result and carry on with this task.'
const COMMON = (repo) => `Repo: ${G}/${repo}, on branch ${BR} (already created and checked out; verify with git branch --show-current; never switch branches, never reset --hard, checkout ., or stash). Follow ${G}/${repo}/CLAUDE.md.
Read first: ${BUNDLE}/00_PLAN.md (rulings), ${OLD}/03_ADOPTION_PLAN.md, and this addon's ${G}/${repo}/docs/revendor/2026-11-16-v1.105.0/02_CANDIDATES.md (its sites are approximate: re-check them in the code). The normative rules are WowAddonStandards v2.113.0 at ${G}/WowAddonStandards/standards/ (preview-mode "Where the strip sits"; standalone-windows "The footer" and "Window chrome geometry"; skinning-§2 for the default skin). The API is ${G}/LibKa0s/docs/api/ (Widgets: TestStrip opts.dock = "title" / "hud", W.DockTestStrip, strip:BodyOffset(), onOffset, strip:Place(); W.Footer(parent, opts), W.FOOTER.HEIGHT; Skin DefaultSkin). The reference adoption of #88 and #89 is ${G}/DropWatcher on master (read only; never edit it): read how it docks its strips and builds its footer before you start.
Hard rules:
- The vendored libs/ and tests/_kit/ are read-only. If the library blocks you (a defect, a missing member), stop that item and return library-blocker with the evidence.
- Test first: a characterization or red test for each behavior you change, then the change. Never weaken, skip or delete a test; a test that pins the old geometry is updated to pin the new rule, and you say so.
- Keep each window's text, tooltips and controls; only the chrome moves. Update the addon's docs (ARCHITECTURE.md, smoke-tests.md, README where it describes the window) in the same commit.
- Gate before each commit: lua tests/run.lua and luacheck ., each wrapped in /home/tushar/.claude/dev-copilot/bin/ka0s-bounded, under EVERY client profile the addon ships (KA0S_KIT_CLIENT=forever as well when ${G}/WowAddonStandards/standards/ADDONS.md lists it for WoW Forever), 0 failed and luacheck 0/0, no .lua file over 1500 lines. Check the eol gate (.gitattributes) before committing: files must match the repo's line endings.
- Commit subjects start with the item id, e.g. "AD-89-BL: ...". One commit per item; #88 and #89 may share one commit "AD-88-XX + AD-89-XX: ..." when they move the same window's geometry. Messages end with these two trailer lines exactly:\n${TRAILER}
- Already done? git log ${BR} --format=%s finds the id: verify and return already-done.
- An item you find does not apply (no such window or HUD in the code): make no commit and return not-applicable with a proof command.
- NEVER push, tag, merge, or write to GitHub. ${GUARD}`

const ADDONS = [
  ['AbsorbTracker', ['AD-88-AT'], 'HUD: the test/sim strip docks to the HUD top edge, outside it (dock = "hud"), flipping under near the screen top; strip:Place() after the host moves the HUD; the sim step panel stays. Remove any hand-anchored strip or header mode word.'],
  ['AuraMaster', ['AD-88-AM', 'AD-89-AM'], '#88: the container strips in /am test dock as HUD strips (modules/Anchors.lua). #89: the PresetPicker\'s status/footer line (settings/PresetPicker.lua) onto W.Footer at 24 px. Another Claude session works in this repo at times: touch only your branch.'],
  ['KickCD', ['AD-88-KC'], 'Ruling 2: the icon grids and cast bar under /kcd sim (and test) show the docked HUD strip (dock = "hud"); this reverses ruling D-13, and tests/test_sim_marker.lua is inverted in the same commit (say so in the message). The sim step panel stays.'],
  ['BankLedger', ['AD-88-BL', 'AD-89-BL'], 'Browser: the strip under the filter bar takes dock = "title" and the 18 px footer (FOOTER_H, _dbFooter) becomes W.Footer 24 px; SessionWindow: its strip takes dock = "title". Do both in one commit per window if they share geometry.'],
  ['CombatTrail', ['AD-88-CT', 'AD-89-CT'], 'Default branch is main. HUD strip (modules/Hud.lua STRIP_MAKER) docks with dock = "hud"; the Results strip (anchorStrip) docks with dock = "title". The Hud buildFooter and RaceWindow footer (20 px) become W.Footer 24 px. CombatTrail\'s footer was the reference look the library copied, so keep its content.'],
  ['DpsRace', ['AD-88-DR', 'AD-89-DR'], 'Hud test and sim anchorStrip docks with dock = "hud"; Results anchorStrip with dock = "title". The HUD\'s 20 px buildFooter becomes W.Footer 24 px. Retail-only addon.'],
  ['LootHistory', ['AD-88-LH', 'AD-89-LH'], 'Browser: the strip under the filter bar (NS.MakeTestStrip, NS.TestStripReserve) takes dock = "title"; the 18 px footer (FOOTER_H, the "Database ~N MB" _dbFooter line, the skin bottomBar) becomes W.Footer 24 px. Its leak gate test must stay green.'],
  ['LibKa0sSkinTester', ['AD-89-ST'], 'The Showroom\'s hand-built 22 px footer (modules/Showroom.lua) becomes W.Footer 24 px. AD-88-ST is an exception (ruling 3): leave the showcase strips alone.'],
  ['MultiMeters', ['AD-DS-MM', 'AD-88-MM', 'AD-89-MM'], 'AD-DS-MM: the profile defaults take the skin from DefaultSkin() as skinning-§2 requires (grep finds none today); a test pins it. AD-88-MM: the meter window strip (modules/Window_Frame.lua, PlaceTestStrip in modules/Window_Header.lua) takes dock = "title". AD-89-MM: check whether a meter window has a hand-built footer; if not, not-applicable with proof.'],
  ['OutfitterReborn', ['AD-88-OR', 'AD-89-OR'], 'Ships Retail and WoW Forever. Find its windows that show test or preview data and its hand-built footers (outfit window, outfit bar) and adopt; Forever rule: never open CharacterFrame from addon code.'],
  ['SkillMaster', ['AD-88-SM', 'AD-89-SM'], 'Default branch is main. Its main window and journal: strip dock = "title" where it shows test/sim data; hand-built footers become W.Footer 24 px. Do NOT touch modules/Bar.lua or the launcher (later waves).'],
  ['PremadeGroupsFilterExtension', ['AD-DS-PGFE'], 'The profile defaults take the skin from DefaultSkin() as skinning-§2 requires; a test pins it. Retail-only addon.'],
  ['WhatGroup', ['AD-DS-WG'], 'The profile defaults take the skin from DefaultSkin() as skinning-§2 requires; a test pins it. Retail-only addon.'],
]

const build = (a) => agent(`You are executing wave A items ${a[1].join(', ')} of a checkpointed multi-repo adoption run.\n${COMMON(a[0])}\nThis addon: ${a[2]}\nReturn the structured result, with one items[] entry per id, the gate totals, and the in-game smoke checks the owner should run for what changed.`,
  {label: `build:${a[0]}`, phase: 'Build', schema: RESULT})
const review = (r, a) => agent(`Independent review of adoption wave A in ${G}/${a[0]} on branch ${BR}: git log and git diff $(git merge-base ${BR} origin/HEAD)..${BR} (origin/HEAD is the default branch). Items: ${a[1].join(', ')}. Brief: ${a[2]}
Judge against WowAddonStandards v2.113.0 (${G}/WowAddonStandards/standards/: preview-mode "Where the strip sits", standalone-windows "The footer" and "Window chrome geometry", skinning-§2) and the API docs in ${G}/LibKa0s/docs/api/, with ${G}/DropWatcher (master) as the reference adoption. Look for: a strip or footer still hand-placed, body insets that do not follow strip:BodyOffset()/onOffset or W.FOOTER.HEIGHT, a header mode word left while the strip shows, lost window text/controls/tooltips, a weakened or deleted test, docs and smoke checks not updated, an edited libs/ or tests/_kit/. Re-run the gate yourself (ka0s-bounded lua tests/run.lua and ka0s-bounded luacheck . under every client the addon ships). Read-only: change nothing, commit nothing. ${GUARD}`,
  {label: `review:${a[0]}`, phase: 'Review', schema: VERDICT}).then(v => ({build: r, review: v}))
const fix = (rv, a) => {
  if (!rv || !rv.review || rv.review.verdict === 'approve') return {repo: a[0], ...rv}
  const real = rv.review.findings.filter(f => f.severity !== 'minor' || true)
  return agent(`Fix the review findings for adoption wave A in ${G}/${a[0]}.\n${COMMON(a[0])}\nFindings (JSON): ${JSON.stringify(real)}\nFix each one you agree with; for one you judge wrong, say why in notes. Commit as "<item id>: review fixes" (one commit, the id of the item the fixes belong to, several ids joined by " + "). Return the structured result for the items you touched, with the gate.`,
    {label: `fix:${a[0]}`, phase: 'Fix', schema: RESULT}).then(f => ({repo: a[0], ...rv, fix: f}))
}
const out = await pipeline(ADDONS, a => build(a), (r, a) => review(r, a), (rv, a) => fix(rv, a))
for (const o of out.filter(Boolean)) log(`${o.repo}: ${(o.build?.items || []).map(i => i.id + ' ' + i.status).join(', ')}; review ${o.review?.verdict}${o.fix ? ' (fixed)' : ''}`)
return out