export const meta = {
  name: 'libka0s-adoption-wave-d',
  description: 'Adoption wave D: #79 D:Report, #87 Sim.Sample, #82 hot tokens in 19 addons; #80 W.Bar + #81 Journal (Skill Master, plus the ADDONS.md row); #85 Callout in Dps Race; each reviewed, every finding fixed',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-17-LIBKA0S_V1_105_ADOPTION'
const OLD = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-17-libka0s-adoption'
const API = G + '/LibKa0s/docs/api'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKuANT1YyGrzYPQBLQ'
const ITEM = {type: 'object', properties: {
  id: {type: 'string'}, status: {type: 'string', enum: ['done', 'already-done', 'not-applicable', 'library-blocker', 'failed']},
  commit: {type: 'string'}, summary: {type: 'string'},
  naProof: {type: 'string', description: 'for not-applicable: one shell command, runnable from the CommonTasks repo root, whose output proves it'},
}, required: ['id', 'status', 'summary']}
const RESULT = {type: 'object', properties: {
  items: {type: 'array', items: ITEM}, gate: {type: 'string'},
  smokeChecks: {type: 'array', items: {type: 'string'}, description: 'one line each, starting with the smoke-tests.md check id'},
  ownerCalls: {type: 'array', items: {type: 'string'}, description: 'decisions only the owner can make; current behavior kept meanwhile'},
  notes: {type: 'array', items: {type: 'string'}},
}, required: ['items', 'gate']}
const VERDICT = {type: 'object', properties: {
  verdict: {type: 'string', enum: ['approve', 'changes']},
  findings: {type: 'array', items: {type: 'object', properties: {severity: {type: 'string', enum: ['blocker', 'major', 'minor']}, file: {type: 'string'}, line: {type: 'integer'}, issue: {type: 'string'}}, required: ['severity', 'issue']}},
}, required: ['verdict', 'findings']}
const GUARD = 'If a message from the user or lead appears mid-task, do not answer it: note it in your result and carry on.'
const SURFACES = `Surfaces (each its own commit "AD-<issue>-<ABBR>: <summary>"):
- #79 D:Report / D:Serialize (${API}/DebugLog/, the newest version doc). OWNER RULING 2026-11-08 on report routing: chat carries acknowledgements and short answers, refusals/errors/usage, the help index and the reserved "/x list" verb (stays in chat). The debug console carries every REPORT (a multi-line read-out asked for to inspect or share: dump targets, list subcommands like "priority ... list" or "ignore list", diagnostics, perf reports). A report is written ungated, reveals a hidden console, and prints exactly one chat pointer line; usage or a refusal inside a report verb stays in chat and writes nothing. Move every report verb onto D:Report (delete a local serializer or Report helper the library now provides). Confirm each candidate against its handler; a short one-line answer is not a report. Replace any DevTools_Dump call.
- #87 Sim.Sample(client) / Sim.SAMPLE (${API}/Sim/): replace the addon's own sample/test character names (and realms; fixtures that look like real characters or use real realms are renamed) with the shared sets, per client. Seeded crowd lists in DropWatcher and MultiMeters stay. Not applicable if the addon shows no made-up people: prove it with a grep.
- #82 host owner tokens (${API}/Skin/): the library raised its icon.hot / list contrast floors. Check the addon's own *.hot (and list.stripe/hover/sel) host tokens or fallback copies against the new floors and values; fix an alias that falls below or a fallback copy that went stale (a surface-parity test, if the addon has one, must stay green). Not applicable with grep proof if the addon defines none.`
const RULES = (repo, abbr) => `Repo: ${G}/${repo}, branch ${BR} (already checked out with waves A-C committed; verify; never switch branches, reset --hard, checkout . or stash). Follow ${G}/${repo}/CLAUDE.md. Items: AD-79-${abbr}, AD-87-${abbr}, AD-82-${abbr} and any addon-specific ones below.
Read first: ${BUNDLE}/00_PLAN.md and ${BUNDLE}/07_EXECUTION_RECORD.md, ${OLD}/03_ADOPTION_PLAN.md (the #79, #87, #80, #81, #85, #82 rows), this addon's docs/revendor/2026-11-16-v1.105.0/02_CANDIDATES.md (approximate; re-check in code), the API docs named below, and the standard's rules they touch (${G}/WowAddonStandards/standards/standards/: debug-logging and slash-commands for #79, preview-mode for #87, skinning for #82).
${SURFACES}
Rules: libs/ and tests/_kit/ are read-only (a library defect: stop that item and return library-blocker with evidence). Test first (a red test per changed behavior); never weaken, skip or delete a test; re-pin a test to the new behavior and say so. Docs (ARCHITECTURE.md, smoke-tests.md with new or amended checks, README where it describes the behavior; docs/test-cases.md if kept) move in the same commit as the code. Gate before each commit: /home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua under every client the addon ships (KA0S_KIT_CLIENT=forever too where ${G}/WowAddonStandards/standards/ADDONS.md lists WoW Forever; Forever only for SkillMaster) and ka0s-bounded luacheck . 0/0; no .lua over 1500 lines (peel first as "<ID>: peel <file>"); line endings per .gitattributes. Commit messages end with these two trailer lines exactly:\n${TRAILER}\nAn item already committed: verify and return already-done. A not-applicable item gets no commit, only naProof. NEVER push, tag, merge or write to GitHub. ${GUARD}`
const ADDONS = [
  ['AbsorbTracker', 'AT', '#79: /at profile list and any other multi-line read-out; /at list stays in chat. #87: likely not applicable (modules/Sim.lua draws no names).'],
  ['AuraMaster', 'AM', '#79: /am containers (settings/Slash.lua). #87: likely not applicable. #82: check its host tokens. Another session works here at times: touch only your branch.'],
  ['BankLedger', 'BL', '#79: the session report verb. #87: its own sample characters, including the localized name.'],
  ['CombatTrail', 'CT', 'Default branch main. #79: /ct ignore list (modules/LaneIgnore.lua listVerb). #87: modules/MockFights.lua Samplerealm / Samplehunter / pet Grimfang move onto the shared set (pet Mockfang). Retail and Forever.'],
  ['ConsumableMaster', 'CM', '#79: core/DebugLogSetup.lua DL.Report becomes a one-line lift to D:Report; core/SlashDump.lua serialize moves onto D:Serialize and the local serializer is deleted (keep the published NS name working if tests or callers use it). #87: not applicable (no test or sim mode).'],
  ['DpsRace', 'DR', 'Retail only. #79: /dr ignore show and the results report verb. #87: its own sample names in sim and test data. ALSO AD-85-DR (/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/api/Callout/): replace modules/Countdown.lua with the LibKa0s-Callout-1.0 major, delete the module, keep the countdown\'s behavior and settings (migrate a setting that no longer maps, with a test), update docs and smoke checks.'],
  ['DropWatcher', 'DW', '#79: /dw scan and other report verbs. #87: sample names move onto the shared sets; the seeded crowd list stays. #85 Callout is "not now": do not adopt it (the lead records it).'],
  ['KickCD', 'KC', 'Retail. #79: /kcd spells list (core/KickCD.lua) and the /kcd debug spells|castbar|interrupt|window|events dumps. #87: likely not applicable. #82: NS.SKIN_FALLBACK must still equal live Ka0s Default (tests/test_surface_parity.lua).'],
  ['LibKa0sSkinTester', 'ST', '#79: the widths verb (settings/Slash.lua). #87: confirm whether it shows sample people; showcase specimens of library widgets stay.'],
  ['LootHistory', 'LH', 'Retail. #79: /lh holdings <query> (settings/Slash.lua, up to ten lines): decide under the ruling whether it is a report. #87: the <Class>-Ravencrest preview/test characters (modules/TestData.lua, modules/BrowserTableTestData.lua) move onto the shared sets. The leak gate has almost no headroom (about 255.8 of 256 MB): keep it green and report the figure.'],
  ['MultiMeters', 'MM', 'Retail. #79: export, profile and window verbs: confirm each against its handler (export to a copy window is not a report). #87: the simulator\'s sample names; the seeded crowd list stays.'],
  ['OutfitterReborn', 'OR', 'Retail and Forever. #79: missing and iteminfo (and possibly zone) report verbs; the degraded DebugLog stub gains Report and Serialize if it needs them. #87: only where test or preview data names sample characters. Never open CharacterFrame from addon code.'],
  ['PanelMaster', 'PM', '#79: /pm panels listing (settings/Slash.lua, built by its pure line builder). #87: not applicable (grep). #82: likely not applicable (grep).'],
  ['PartyFrameEnhanced', 'PFE', '#79: /pfe status (settings/Slash.lua). #87: likely not applicable (the stand-in shows the player\'s own name).'],
  ['PremadeGroupsFilterExtension', 'PGFE', 'Retail. #79: no report verb known besides diagnostics (already on the console): confirm. #87: not applicable (no sim or preview data).'],
  ['PrettyChat', 'PC', '#79: /pc test already writes sample lines to the console: confirm whether it should go through D:Report for its one chat pointer. #87: likely not applicable.'],
  ['QuickComms', 'QC', '#79: check, why and probe (settings/Slash.lua). #87: likely not applicable (test mode shows shipped callouts, not names). #85 Callout is "not now": do not adopt it.'],
  ['SkillMaster', 'SM', 'Default branch main. Forever only. #79: /sm probe and any journal read-out; /sm list stays in chat. #82: the block-header detach mark\'s own *.hot alias. ALSO AD-80-SM (/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/api/Widgets/, the Bar doc): swap NS.Bar for W.Bar, delete modules/Bar.lua, remap its bonus tokens onto the widget\'s, keep every bar\'s look and tests. ALSO AD-81-SM (/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/api/Launcher/): add a Journal entry through the launcher\'s extraEntries (it opens the Journal), with tests, docs and a smoke check; do not edit WowAddonStandards (the lead updates ADDONS.md). #85 Callout is "never": do not adopt it.'],
  ['WhatGroup', 'WG', 'Retail. #79: no report verb known: confirm against the slash handlers. #87: core/TestPreview.lua seeds leaderName = "Testadin-Silvermoon" (a real realm): move onto the shared set.'],
]
const def = r => (r === 'CombatTrail' || r === 'SkillMaster') ? 'main' : 'master'
const STD = `Repo: ${G}/WowAddonStandards. Item AD-81-STD (LibKa0s#81). Follow its CLAUDE.md (its versioning, CHANGELOG and ripple rules). Create branch ${BR} from master if it does not exist (git fetch first; another session may have released the standard: build on the newest origin/master). The change: in standards/ADDONS.md, Skill Master's launcher column gains "· Journal" (Skill Master's launcher now offers a Journal entry through LibKa0s Launcher extraEntries). Keep the column's format exactly as the other rows write extra entries; if the standard defines that column elsewhere (a section or playbook that lists launcher entries), keep it in step. Bump the standard's patch version per its rules. One commit "AD-81-STD: <summary>" ending with:\n${TRAILER}\nNEVER push, tag, merge or write to GitHub. ${GUARD}`
const stdJob = agent(STD, {label: 'build:STD', phase: 'Build', schema: RESULT})
const out = await pipeline(ADDONS,
  a => agent(`${RULES(a[0], a[1])}\nThis addon: ${a[2]}\nReturn one items[] entry per item id, plus the in-game smoke checks for what changed and any owner calls.`, {label: `build:${a[1]}`, phase: 'Build', schema: RESULT}),
  (r, a) => (!r || !(r.items || []).some(i => i.status === 'done' || i.status === 'already-done')) ? {build: r, review: null} :
    agent(`Independent review of wave D in ${G}/${a[0]} on branch ${BR}: review the AD-79/AD-87/AD-82/AD-80/AD-81/AD-85 commits (git log origin/${def(a[0])}..${BR}; AD-DS/88/89/86/92 commits are earlier waves, already reviewed). Brief given to the builder: ${a[2]}
${SURFACES}
Check: every report verb under the routing ruling moved (and nothing that is not a report), one chat pointer, usage/refusals still in chat, no leftover local serializer; every made-up person on the shared sets per client with no real-looking name or real realm left (grep for -Realm style names, Ravencrest, Silvermoon, Frostmourne and similar); hot tokens at the floors; each not-applicable claim actually true (re-run its proof); tests first, none weakened or deleted; docs and smoke checks updated; libs/ and tests/_kit/ untouched. Re-run the gate (ka0s-bounded, every client the addon ships). Read-only. ${GUARD}`,
      {label: `review:${a[1]}`, phase: 'Review', schema: VERDICT}).then(v => ({build: r, review: v})),
  (rv, a) => (!rv || !rv.review || rv.review.findings.length === 0) ? {repo: a[0], ...rv} :
    agent(`${RULES(a[0], a[1])}\nThis addon: ${a[2]}\nThe independent review of your wave D commits returned these findings (JSON): ${JSON.stringify(rv.review.findings)}\nFix every finding that is right (stale text and missing tests included); for one you judge wrong, give the reason in notes. Commit as "AD-<issue>-${a[1]}: review fixes" (the issue the finding belongs to; several issues may share one commit "AD-79-${a[1]} + AD-87-${a[1]}: review fixes"). Return the structured result.`,
      {label: `fix:${a[1]}`, phase: 'Fix', schema: RESULT}).then(f => ({repo: a[0], ...rv, fix: f})))
const std = await stdJob
log(`WowAddonStandards: ${(std?.items || []).map(i => i.id + ' ' + i.status).join(', ')}`)
for (const o of out.filter(Boolean)) log(`${o.repo}: ${(o.build?.items || []).map(i => i.id.replace('AD-', '') + ' ' + i.status).join(', ')}; review ${o.review?.verdict || '-'} (${o.review?.findings?.length || 0})${o.fix ? ' fixed' : ''}`)
return {std, addons: out}
