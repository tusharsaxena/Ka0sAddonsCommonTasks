export const meta = {
  name: 'libka0s-75plus-revendor',
  description: 'M8: re-vendor LibKa0s v1.105.0 into all 19 roster addons (copy half only), then the Skin Tester hot-state row',
  phases: [{ title: 'Re-vendor' }, { title: 'DropWatcher' }, { title: 'Skin Tester row' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-16-libka0s-75-plus'
const CMD = '/home/tushar/.claude/plugins/cache/dev-copilot/dev-copilot/2.10.0/commands/wow-revendor-libka0s.md'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RESULT = {type: 'object', properties: {
  status: {type: 'string', enum: ['done', 'already-done', 'library-blocker', 'failed']},
  commit: {type: 'string'},
  gate: {type: 'string', description: 'tests run/failed/skipped per client profile, luacheck totals, largest file'},
  fixes: {type: 'array', items: {type: 'string'}},
  adoptionOwed: {type: 'array', items: {type: 'string'}},
  blocker: {type: 'string', description: 'for library-blocker/failed: the failing test, the evidence, and why the cause is in LibKa0s'},
}, required: ['status', 'gate', 'fixes']}

const RULES = (repo, id) => `You are executing item ${id} of a checkpointed multi-repo run: re-vendor LibKa0s v1.105.0 into ${G}/${repo}.
Read first: ${BUNDLE}/00_DESIGN.md section 5 (normative, including the list of fixes each addon is expected to need), ${BUNDLE}/01_EXECUTION_PLAN.md "Re-vendor procedure" and "Rules for every item", and the research notes it cites in ${BUNDLE}/inputs/research/ (R7, R8, R9 §3; R9 corrects earlier notes). Follow ${G}/${repo}/CLAUDE.md.
Hard rules:
- Work ONLY in ${G}/${repo}, on branch ${BR}. It is already created and checked out; verify with git branch --show-current. Never switch branches, never reset --hard / checkout . / stash.
- Already done? If git log ${BR} --format=%s | grep -E '^${id}: ' finds a commit, verify the gate and return status already-done.
- Source: the LOCAL LibKa0s tag v1.105.0 in ${G}/LibKa0s (git archive; it is not on origin yet, that is expected). Never edit ${G}/LibKa0s.
- Follow ${CMD} for the COPY AND BUNDLE HALF only: copy both payloads whole (libs/LibKa0s/ and tests/_kit/), roll the CLAUDE.md provenance line, keep or write the "LibKa0s icons:" declaration, prune with the tag's tools/prune-icons.lua, keep README icon credits in step, write the delta report and the docs/revendor/2026-11-16-v1.105.0/ bundle (plus a span bundle if one is owed). SKIP the adoption interview and every GitHub issue filing: list adoption candidates in the bundle as owed in phase [3] with their LibKa0s issue numbers (#79 #85 #86 #87 #88 #89 #92 where they apply).
- Gate: the addon's own green gate from its CLAUDE.md, under every client profile it lists (KA0S_KIT_CLIENT=retail and =forever for a Retail · Forever addon), with /home/tushar/.claude/dev-copilot/bin/ka0s-bounded around every lua run and around luacheck (0 warnings / 0 errors), and the 1500-line cap.
- Fix what goes red using design §5's list of expected fixes (stub members such as Options SideTabs, DebugLog Report/Serialize, Compat identity, Sim SAMPLE/Sample; loader-list XML-order lines for the new payload files Tooltip.lua, WidgetsDragHandleTip.lua, WidgetsHeader.lua, WidgetsBar.lua, OptionsSkinPickerQueue.lua; pins the release moved). Diagnose anything else before changing it (bisect before theorising). NEVER weaken, skip or delete a test.
- If the cause of a red test is in the library payload itself, STOP: make no commit, leave the tree as it is, and return status library-blocker with the evidence. The lead fixes LibKa0s.
- No behaviour change beyond what the library change itself forces.
- Commit ONCE: subject "${id}: Re-vendor LibKa0s v1.105.0 (kit 57): <fixes>", message ending with these two trailer lines exactly:\n${TRAILER}
- NEVER push, tag, merge, or write to GitHub.`

const ADDONS = [
  ['AbsorbTracker', 'RV-AT', ''],
  ['AuraMaster', 'RV-AM', ''],
  ['BankLedger', 'RV-BL', 'Expected: Ka0s Default fallback copies.'],
  ['CombatTrail', 'RV-CT', 'Default branch is main. Expected: its stripe default (#84).'],
  ['ConsumableMaster', 'RV-CM', 'Expected: color-pin tests read through the view.'],
  ['DpsRace', 'RV-DR', 'Expected: its stripe default (#84).'],
  ['KickCD', 'RV-KC', ''],
  ['LibKa0sSkinTester', 'RV-ST', 'Expected: its hand-written loader list gains the new payload files.'],
  ['LootHistory', 'RV-LH', 'Expected: Ka0s Default fallback copies.'],
  ['MultiMeters', 'RV-MM', 'Expected: Compat identity stub members and its font-row pin.'],
  ['OutfitterReborn', 'RV-OR', 'Expected: of.bar.worn moves to text.accent (design D-7), and per-skin icon.hot pins if red.'],
  ['PanelMaster', 'RV-PM', ''],
  ['PartyFrameEnhanced', 'RV-PFE', ''],
  ['PremadeGroupsFilterExtension', 'RV-PGFE', 'Expected: loader list and Compat identity stub members.'],
  ['PrettyChat', 'RV-PC', ''],
  ['QuickComms', 'RV-QC', ''],
  ['SkillMaster', 'RV-SM', 'Default branch is main. Expected: per-skin icon.hot pins if red. LibKa0s v1.105.0 promoted this addon\'s modules/Bar.lua as W.Bar; do NOT adopt it here (phase [3]).'],
  ['WhatGroup', 'RV-WG', 'Expected: loader list and Compat identity stub members.'],
]
const run = (repo, id, extra, phaseName) =>
  agent(`${RULES(repo, id)}\n${extra}\nReturn the structured result.`, {label: id, phase: phaseName, schema: RESULT})

phase('Re-vendor')
const results = await pipeline(ADDONS,
  a => run(a[0], a[1], a[2], 'Re-vendor').then(r => ({repo: a[0], id: a[1], ...(r || {status: 'failed', gate: 'agent returned nothing', fixes: []})})),
  (r) => r.id !== 'RV-ST' || r.status === 'library-blocker' || r.status === 'failed' ? r :
    agent(`You are executing item ST-82 in ${G}/LibKa0sSkinTester on branch ${BR} (already checked out; never switch, reset or stash). RV-ST is committed. Read ${BUNDLE}/00_DESIGN.md §3.4 and ${BUNDLE}/inputs/research/R5*.md (decision D-9): add ONE showroom row to the Skin Tester that shows the hot state (icon.hot against rest and against a heading, plus list hover and stripe) so LibKa0s#82/#84 can be smoked in one window across all nine skins. Follow the repo's CLAUDE.md; red test first for the new row; gate as its CLAUDE.md says, through /home/tushar/.claude/dev-copilot/bin/ka0s-bounded (luacheck 0/0). If ${G}/LibKa0s/docs/api documents a sample/showroom surface, use it. Commit once as "ST-82: <summary>" ending with these two trailer lines exactly:\n${TRAILER}\nNever push, tag, merge or write to GitHub. Also add the row to the run's smoke sheet ONLY by reporting the check text back (do not edit the bundle). Return the structured result.`,
      {label: 'ST-82', phase: 'Skin Tester row', schema: RESULT}).then(s => ({...r, st82: s}))
)
for (const r of results.filter(Boolean)) log(`${r.id} ${r.status}`)

phase('DropWatcher')
const dw = await run('DropWatcher', 'RV-DW', 'This addon goes last. Its checkout is on the run branch, which was created from a clean master. Expected: Ka0s Default fallback copies, and per-skin icon.hot pins if red. Never touch any other branch of this repo.', 'DropWatcher')
return {addons: results, dw}
