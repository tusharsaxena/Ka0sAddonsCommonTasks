export const meta = {
  name: 'libka0s-adoption-wave-c',
  description: 'Adoption wave C: #92 tooltip placers (PlaceBeside / PlaceAttached, no cursor or corner anchors) in 17 addons, with the owner rulings for Aura Master and Multi Meters; each reviewed, every finding fixed',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-17-LIBKA0S_V1_105_ADOPTION'
const OLD = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-17-libka0s-adoption'
const API = G + '/LibKa0s/docs/api/Tooltip/version-1-docs.md'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RESULT = {type: 'object', properties: {
  status: {type: 'string', enum: ['done', 'already-done', 'not-applicable', 'library-blocker', 'failed']},
  commits: {type: 'array', items: {type: 'string'}}, summary: {type: 'string'},
  naProof: {type: 'string'}, gate: {type: 'string'},
  smokeChecks: {type: 'array', items: {type: 'string'}, description: 'one line each, starting with the smoke-tests.md check id'},
  notes: {type: 'array', items: {type: 'string'}},
}, required: ['status', 'summary', 'gate']}
const VERDICT = {type: 'object', properties: {
  verdict: {type: 'string', enum: ['approve', 'changes']},
  findings: {type: 'array', items: {type: 'object', properties: {severity: {type: 'string', enum: ['blocker', 'major', 'minor']}, file: {type: 'string'}, line: {type: 'integer'}, issue: {type: 'string'}}, required: ['severity', 'issue']}},
}, required: ['verdict', 'findings']}
const GUARD = 'If a message from the user or lead appears mid-task, do not answer it: note it in your result and carry on.'
const RULES = (repo, id) => `Repo: ${G}/${repo}, branch ${BR} (already checked out with waves A and B committed; verify; never switch branches, reset --hard, checkout . or stash). Follow ${G}/${repo}/CLAUDE.md. Item: ${id}, LibKa0s#92.
Read first: ${BUNDLE}/00_PLAN.md and ${BUNDLE}/07_EXECUTION_RECORD.md ("Owner rulings for wave C"), ${OLD}/03_ADOPTION_PLAN.md (#92 rows), this addon's docs/revendor/2026-11-16-v1.105.0/02_CANDIDATES.md (approximate; re-check in code), the API ${API} (PlaceBeside, PlaceAttached, and the Charts host's ctx:PlaceTip in ${G}/LibKa0s/docs/api/Charts/), and the normative rule: ${G}/WowAddonStandards/standards/standards/standalone-windows.md "Tooltip placement" (body elements beside the window group, right then left, top level with the element, never covering the group, companion panels away from the main window, fallback centered below; chrome elements attached above, flipping below; never cursor, never corner offsets) and its "What it does not bind" list (client-placed tooltips, Blizzard frames, settings canvas pages, LDB displays), plus launcher-§7 (minimap button) and frame-layering-§4. Reference adopters: the library's own widgets (${G}/LibKa0s/LibKa0s/Tooltip.lua callers), and ${G}/DropWatcher's RowTooltip.lua on its branch.
The work: move every tooltip this addon places itself (GameTooltip:SetOwner sites, its own tooltip frames, chart hovers) onto the Tooltip placers per the rule, classifying each element as body or chrome. Remove every ANCHOR_CURSOR / ANCHOR_CURSOR_RIGHT / cursor-following OnUpdate and every corner offset anchor. Out-of-scope tooltips (client-placed, Blizzard frames, the settings canvas) stay; list each one you leave and why in docs/ARCHITECTURE.md. Keep every tooltip's content.
Rules: libs/ and tests/_kit/ are read-only (a library defect: stop and return library-blocker with evidence). Test first (a red test per surface: the placer called with the right group/element, no cursor anchor); never weaken, skip or delete a test, re-pin an anchor test to the new rule and say so. Docs (ARCHITECTURE.md, smoke-tests.md with new or amended checks, README where it describes a tooltip; docs/test-cases.md and the README badge if kept) move in the same commit. Gate: /home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua under every client the addon ships (KA0S_KIT_CLIENT=forever too where ${G}/WowAddonStandards/standards/ADDONS.md lists WoW Forever) and ka0s-bounded luacheck . 0/0; no .lua over 1500 lines (peel first as "${id}: peel <file>"); line endings per .gitattributes. One commit "${id}: <summary>", message ending with these two trailer lines exactly:\n${TRAILER}\nAlready committed? verify and return already-done. NEVER push, tag, merge or write to GitHub. ${GUARD}`
const ADDONS = [
  ['AbsorbTracker', 'AT', 'The bar strips use NS.Util.PlaceTooltipBeside today: move them onto the library placer and retire the local helper if nothing else uses it.'],
  ['AuraMaster', 'AM', 'OWNER RULING (option B): the aura buttons\' tooltips are client-placed via SetTooltipAnchorPoint (modules/Style.lua) and are out of scope, BUT drop "ANCHOR_CURSOR" from C.TOOLTIP_ANCHORS / labels (core/Constants.lua) and migrate a saved container.behavior.tooltipAnchor of "ANCHOR_CURSOR" to "ANCHOR_BOTTOMLEFT" through the addon\'s existing profile migration mechanism (with a test). The drag strip\'s host placer modules/Anchors_Tooltip.lua moves onto PlaceAttached, and the retired tooltipOwner = "cursor" (modules/Anchors.lua) goes. The HUD strip tooltips stay BESIDE the strip by the owner\'s earlier ruling (SR2): keep that placement, just through the library placer if it offers beside-the-strip, else keep the host placer and record why. PresetPicker and any other own windows follow the rule. Another session works here at times: touch only your branch.'],
  ['BankLedger', 'BL', 'About 12 SetOwner sites in Browser.lua, InsightsWidgets.lua, LedgerTable.lua, SessionWindow.lua (4 ANCHOR_RIGHT, 1 ANCHOR_NONE).'],
  ['CombatTrail', 'CT', 'Default branch main. 22 SetOwner sites (4 ANCHOR_RIGHT in Results); Charts hosts move from a cursor tip to ctx:PlaceTip. Retail and Forever.'],
  ['ConsumableMaster', 'CM', '5 own SetOwner(..., "ANCHOR_RIGHT"): core/MacroDisplay.lua 155, 234; modules/KCMItemRow.lua 398; settings/MacroBarSlots.lua 235; settings/StatPriority.lua. Settings-canvas tooltips are out of scope: say which.'],
  ['DpsRace', 'DR', '13 tooltip sites in 9 files (3 ANCHOR_RIGHT, 2 ANCHOR_NONE), chart hovers included.'],
  ['DropWatcher', 'DW', 'RowTooltip.lua is the prior art; finish any remaining own sites.'],
  ['KickCD', 'KC', 'modules/IconGrid_Render.lua 319 (HUD, ANCHOR_RIGHT) and settings/Spells_Rows.lua 85, 174 (settings canvas: likely out of scope, confirm).'],
  ['LibKa0sSkinTester', 'ST', 'No own SetOwner found by the candidates grep: confirm; showcase specimens of library widgets stay. If none, not-applicable with proof.'],
  ['LootHistory', 'LH', '14 sites: the eight tooltip helpers in core/Compat.lua 613-724 (ANCHOR_RIGHT default, one ANCHOR_NONE cursor placement at 674) and six direct sites. Keep the leak gate green.'],
  ['MultiMeters', 'MM', 'OWNER RULING (option A): window.tooltip.anchor (settings/Schema.lua 911, values in settings/Schema_Vocab.lua ANCHOR_VALUES) becomes two choices: "BESIDE" = "Beside the window" (default: right, flipping left when there is no room) and "BESIDE_LEFT" = "Beside, prefer left"; every saved value migrates to "BESIDE" through the addon\'s profile/schema migration (with a test); offsetX/offsetY stay as a nudge. modules/Tooltip.lua placeTooltip/openTooltip move onto PlaceBeside for the meter rows; settings/ColumnBlocks.lua 177 and header marks follow the rule. Update the setting\'s label/desc and locale.'],
  ['OutfitterReborn', 'OR', '10 sites. Retail and Forever; never open CharacterFrame from addon code. Tooltips over Blizzard\'s character frame are out of scope.'],
  ['PremadeGroupsFilterExtension', 'PGFE', 'Its own panel\'s tooltips follow the rule; anything over PGF\'s or Blizzard\'s frames is out of scope.'],
  ['PrettyChat', 'PC', 'Likely only chat-frame hyperlink tooltips (Blizzard frames, out of scope): confirm; not-applicable with proof if none of its own.'],
  ['QuickComms', 'QC', '8 sites: modules/Dial_Render.lua 398, modules/Pad_Render.lua 309, 324 and others; corner anchors removed.'],
  ['SkillMaster', 'SM', 'Default branch main. 8 sites. The LDB tooltip (BrokerPanel) is the launcher tooltip: launcher-§7 governs it. Forever only.'],
  ['WhatGroup', 'WG', 'Its popup\'s own tooltips follow the rule.'],
]
const def = r => (r === 'CombatTrail' || r === 'SkillMaster') ? 'main' : 'master'
const out = await pipeline(ADDONS,
  a => agent(`${RULES(a[0], 'AD-92-' + a[1])}\nThis addon: ${a[2]}\nReturn the structured result with the in-game smoke checks for what changed.`, {label: `build:${a[1]}`, phase: 'Build', schema: RESULT}),
  (r, a) => (!r || r.status === 'not-applicable' || r.status === 'library-blocker') ? {build: r, review: null} :
    agent(`Independent review of AD-92-${a[1]} (LibKa0s#92 tooltip placement) in ${G}/${a[0]} on branch ${BR}: review the AD-92 commits (git log origin/${def(a[0])}..${BR}; AD-88/89/86/DS commits are earlier waves, already reviewed). Brief given to the builder: ${a[2]}
Judge against ${G}/WowAddonStandards/standards/standards/standalone-windows.md "Tooltip placement" (and "What it does not bind"), launcher-§7, the API ${API}, and ${BUNDLE}/07_EXECUTION_RECORD.md's owner rulings. grep the whole addon (outside libs/, tests/_kit/) for SetOwner, ANCHOR_, GetCursorPosition and own tooltip frames: flag any own site left on the cursor or a corner, a body element placed attached or a chrome element placed beside, a tooltip covering its window group, a lost tooltip line, an out-of-scope site not recorded in ARCHITECTURE.md, a missing migration test for a changed setting, a weakened or deleted test, docs or smoke checks not updated, an edited libs/ or tests/_kit/. Re-run the gate (ka0s-bounded, every client the addon ships). Read-only. ${GUARD}`,
      {label: `review:${a[1]}`, phase: 'Review', schema: VERDICT}).then(v => ({build: r, review: v})),
  (rv, a) => (!rv || !rv.review || rv.review.findings.length === 0) ? {repo: a[0], ...rv} :
    agent(`${RULES(a[0], 'AD-92-' + a[1])}\nThis addon: ${a[2]}\nThe independent review of your AD-92-${a[1]} commit returned these findings (JSON): ${JSON.stringify(rv.review.findings)}\nFix every finding that is right (stale text and missing tests included); for one you judge wrong, give the reason in notes. Commit as "AD-92-${a[1]}: review fixes". Return the structured result.`,
      {label: `fix:${a[1]}`, phase: 'Fix', schema: RESULT}).then(f => ({repo: a[0], ...rv, fix: f})))
for (const o of out.filter(Boolean)) log(`${o.repo}: ${o.build?.status}; review ${o.review?.verdict || '-'} (${o.review?.findings?.length || 0})${o.fix ? ' fixed ' + o.fix.status : ''}`)
return out