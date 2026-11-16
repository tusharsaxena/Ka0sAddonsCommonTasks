export const meta = {
  name: 'libka0s-75plus-sr1-addons',
  description: 'Smoke round 1, addon half: re-copy the re-cut v1.105.0 into 19 addons and apply the title-bar tooltip/color rulings and header bands to each addon\'s own windows',
  phases: [{ title: 'Addons' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-16-libka0s-75-plus'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RESULT = {type: 'object', properties: {
  status: {type: 'string', enum: ['done', 'already-done', 'library-blocker', 'failed']},
  commit: {type: 'string'},
  gate: {type: 'string', description: 'tests passed/failed/skipped per client profile, luacheck, largest file'},
  titleBar: {type: 'array', items: {type: 'string'}, description: 'each addon-owned window: its title-bar controls, the tooltip each now shows, and the colors applied'},
  fixes: {type: 'array', items: {type: 'string'}},
  smoke: {type: 'array', items: {type: 'string'}, description: 'short in-game checks for the owner'},
  blocker: {type: 'string'},
}, required: ['status', 'gate', 'fixes']}

const prompt = (repo, id, clients, extra) => `You are executing item ${id} of smoke round 1 of a checkpointed run in ${G}/${repo}, branch ${BR} (checked out; verify with git branch --show-current; never switch branches, never reset --hard / checkout . / stash). Follow ${G}/${repo}/CLAUDE.md.
Read first: ${BUNDLE}/SR1_SMOKE_ROUND1.md (the owner's feedback and rulings 2-5; they win), then the CHANGELOG v1.105.0 "What a consumer owes" section in ${G}/LibKa0s (read-only) for what moved since this addon's RV commit.
Already done? If git log ${BR} --format=%s | grep -E '^${id}: ' finds a commit, verify the gate and return status already-done.

1. RE-COPY. The LOCAL LibKa0s tag v1.105.0 was re-cut at 2cd727d5 (it is not on origin; expected). Copy both payloads whole from it (git -C ../LibKa0s archive v1.105.0 LibKa0s testkit tools into a scratch dir outside the repo): libs/LibKa0s/ and tests/_kit/, then re-run the prune with the tag's tools/prune-icons.lua against this addon's existing "LibKa0s icons:" declaration (and sounds line, if any). The CLAUDE.md provenance line already names v1.105.0; keep it. Never edit ../LibKa0s.
2. GATE. ${clients}. Every lua run and luacheck through /home/tushar/.claude/dev-copilot/bin/ka0s-bounded; luacheck 0/0; 1500-line cap. Fix what the release moved (stub members, tooltip pins that expected "below" now "above", close tooltips, close.rest following icon.tint, list.header.bg values, re-pins). Diagnose anything else first; NEVER weaken, skip or delete a test. If a red test's cause is in the library payload, STOP without committing and return library-blocker with evidence.
3. THIS ADDON'S OWN WINDOWS (rulings 3 and 4). Find every window the addon draws itself (not the library's) that has a title bar or header strip with controls: lock, minimize/collapse, settings, export, close, expand-all, tabs' header icons, any icon button in a title bar. For each control: (a) it shows a tooltip on hover, placed with LibKa0s-Tooltip-1.0's PlaceAttached (above, flips below) or AttachTitleTip, in the owner's gtip.title color; (b) at rest it paints the skin's icon.tint, on hover it keeps its glow/highlight and paints text.link; a close X paints icon.tint at rest and close.hot on hover; state toggles whose color carries meaning (on/off, locked/unlocked if the addon colors it) keep their state colors. Use the library's existing surfaces (the facade's Mark/Token, Core.MakeCloseButton with the owner, AttachTitleTip); do NOT adopt W.HeaderButtons unless it is clearly the smaller change, and say which you did. Red tests first: one case per window that every title-bar control has a non-empty tooltip, and rest/hover colors resolve to the tokens in at least Ka0s Default and one other skin. If the addon draws no title-bar controls of its own, say so and skip this step.
${extra}
4. RECORD. Add docs/revendor/2026-11-16-v1.105.0/07_SR1.md (the bundle stays frozen otherwise): the re-cut tag, what the re-copy changed, the title-bar pass per window, the header-band work if any, gate totals. Regenerate docs/test-cases.md and the README Tests badge if this repo keeps them.
5. LINE ENDINGS. Every file you wrote keeps the terminator .gitattributes declares (git check-attr eol): for each, tr -dc '\\r' < f | wc -c must equal tr -dc '\\n' < f | wc -c where eol is crlf. The addon's eol test must be green.
6. COMMIT ONCE: subject "${id}: Re-copy the re-cut v1.105.0; title-bar tooltips and colors<; header bands>", message ending with exactly:\n${TRAILER}
NEVER push, tag, merge, or write to GitHub. Return the structured result, including short smoke checks for the owner.`

const BOTH = 'Run the gate under KA0S_KIT_CLIENT=retail and KA0S_KIT_CLIENT=forever'
const RET = 'Run the gate under the Retail profile (the addon is Retail only)'
const FOR = 'Run the gate under KA0S_KIT_CLIENT=forever (the addon is Forever only)'
const BAND_DW = 'HEADER BANDS (ruling 5): DropWatcher\'s group headers (modules/WindowGroup.lua WG.NewHeader, and the compact layout in modules/CompactGroup.lua, and any other section header the addon draws) paint list.header.bg as a full-row band behind the header, so a header is told apart from the plain row, the stripe and the hover in every skin, with list.header.text for its text where it is not already. Red test first: the band is painted with list.header.bg and repaints on a skin switch.'
const BAND_SM = 'HEADER BANDS (ruling 5): Skill Master\'s block headers paint sm.headerBg (core/SkinSetup.lua, default black .35, follow list.header.bg). The library\'s list.header.bg now carries Ka0s Default black .35 and a distinct band in every skin. Make the header band follow list.header.bg in every skin (keep the addon token as a follow if that is how the addon routes colors, but its value must resolve to list.header.bg in all nine skins); red test first, per skin.'
const ADDONS = [
  ['AbsorbTracker','SR-AT',BOTH,''], ['AuraMaster','SR-AM',BOTH,''], ['BankLedger','SR-BL',RET,''],
  ['CombatTrail','SR-CT',BOTH,'Default branch main.'], ['ConsumableMaster','SR-CM',BOTH,''], ['DpsRace','SR-DR',RET,''],
  ['DropWatcher','SR-DW',BOTH,BAND_DW], ['KickCD','SR-KC',RET,''], ['LibKa0sSkinTester','SR-ST',BOTH,''],
  ['LootHistory','SR-LH',RET,'Its kit leak gate (256 MB) must stay green at the default budget.'], ['MultiMeters','SR-MM',RET,''],
  ['OutfitterReborn','SR-OR',BOTH,''], ['PanelMaster','SR-PM',BOTH,''], ['PartyFrameEnhanced','SR-PFE',BOTH,''],
  ['PremadeGroupsFilterExtension','SR-PGFE',RET,''], ['PrettyChat','SR-PC',BOTH,''], ['QuickComms','SR-QC',BOTH,''],
  ['SkillMaster','SR-SM',FOR,'Default branch main. '+BAND_SM], ['WhatGroup','SR-WG',RET,''],
]
phase('Addons')
const results = await parallel(ADDONS.map(a => () =>
  agent(prompt(a[0], a[1], a[2], a[3]), {label: a[1], phase: 'Addons', schema: RESULT})
    .then(r => ({repo: a[0], id: a[1], ...(r || {status: 'failed', gate: 'agent returned nothing', fixes: []})}))))
for (const r of results.filter(Boolean)) log(`${r.id} ${r.status}`)
return results
