export const meta = {
  name: 'libka0s-75plus-sr2-edges',
  description: 'Smoke round 2: every flat popup/menu/tooltip edge 1px; release record re-closed',
  phases: [{ title: 'Library' }, { title: 'Release' }],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = G + '/Ka0sAddonsCommonTasks/docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS'
const BR = 'feat/2026-11-16-libka0s-75-plus'
const TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmKVFwa6abTbHHP2Wfj'
const RULES = `Context: you are executing one item of smoke round 1 of a checkpointed run. Read ${BUNDLE}/SR2_SMOKE_ROUND2.md first (then SR1_SMOKE_ROUND1.md for the round before): it holds the owner's feedback and the rulings, and it wins over ${BUNDLE}/00_DESIGN.md where they differ. Then read the parts of 00_DESIGN.md and ${BUNDLE}/07_EXECUTION_RECORD.md your item touches. Follow the repo's own CLAUDE.md and (LibKa0s) docs/releasing.md.
Hard rules:
- Work ONLY in the named repo, on branch ${BR} (checked out; verify with git branch --show-current; never switch branches, never reset --hard / checkout . / stash).
- Already done? If git log ${BR} --format=%s | grep -E '^<ID>: ' finds a commit, verify the gate and return without changes.
- v1.105.0 is NOT released (the tag is local), so this is the same release: LibStub minors are bumped at most once per file on this branch (check git diff master -- <file>; reuse a bump already there), the CHANGELOG's v1.105.0 block and the docs/api documents of this release are amended in place, and kit revision stays 57.
- TDD: a red test first for every behavior change.
- Gate before committing (LibKa0s): /home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua (0 failed, no new skip) and /home/tushar/.claude/dev-copilot/bin/ka0s-bounded luacheck . (0/0); every file <= 1500 lines and its size trigger respected; diff -r testkit tests/_kit empty. Never weaken, skip or delete a test.
- Line endings: files keep the terminator .gitattributes declares (git check-attr eol). A Python or shell write can drop CRLF: check tr -dc '\\r' < f | wc -c equals tr -dc '\\n' < f | wc -c on every file you wrote.
- Commit with subject starting '<ID>: ' and end the message with these two trailer lines exactly:\n${TRAILER}
- NEVER push, tag, merge, or write to GitHub.
- Final answer: commit hash(es), gate totals, minors moved (or reused), and anything uncertain.`
const REVIEW_SCHEMA = {type:'object', properties:{verdict:{type:'string', enum:['approve','fix-required']}, findings:{type:'array', items:{type:'object', properties:{severity:{type:'string'}, file:{type:'string'}, line:{type:'integer'}, issue:{type:'string'}, fix:{type:'string'}}, required:['severity','issue']}}, summary:{type:'string'}}, required:['verdict','findings','summary']}

const L4 = `Owner answer in SR2_SMOKE_ROUND2.md ("Owner call this round surfaced"): every skin that does not draw its border from art uses a 1px flat edge for popups, menus and tooltips too, as SR2-L2 did for windows. In SkinDefsOthers.lua: Azeroth popBorder edge(2,...) -> edge(1,...) and tipBorder edge(2,...) -> edge(1,...); WoW Midnight popBorder edge(2,...) -> edge(1,...); WoW Default tipBorder edge(2, "flat", ...) -> edge(1, "flat", ...) (its tooltip draws client art and reads only the color, so the declaration is made truthful; confirm that by reading the paint path and say what you found). Colors do not change. Nine-slice ("nine:...") edges (Glass, WoW Default windows and popups) are untouched. Red first: one table-driven case over all nine skins asserting every flat-style win, popup, menu and tooltip edge size is 1 (skip nine-slice styles by name, list them in the case), plus a painted check for one popup and one menu in Azeroth and Midnight through the kit as the SR2-L2 cases do. Update pins, the Skin API doc of this release, the skin comments and the CHANGELOG v1.105.0 skin entry (extend SR2-L2's entry) and its re-pin list. SkinDefsOthers' minor reuses this branch's bump.`
phase('Library')
await agent(`${RULES}\n\nRepo: ${G}/LibKa0s. Item SR2-L4.\n${L4}`, {label: 'SR2-L4', phase: 'Library'})
const rev = await agent(`You are an independent reviewer who did NOT write this change. Repo ${G}/LibKa0s, branch ${BR}. Review the commit(s) for item SR2-L4 (git log ${BR} --format='%h %s' | grep '^[0-9a-f]* SR2-L4'; git show each). Spec: ${BUNDLE}/SR2_SMOKE_ROUND2.md and the brief: ${L4}\nCheck: every flat edge in every skin is 1px and no nine-slice art edge moved; no color moved; real tests (red-first: verify against the parent commit in a temporary worktree, remove it after); LibStub minor discipline; docs/api and CHANGELOG; no weakened test; eol; gate (re-run ka0s-bounded lua tests/run.lua and ka0s-bounded luacheck . yourself); size caps. Record: git notes --ref=ka0s-review add -f -m "<SR2-L4 review: verdict + key findings>" <the item's last commit>. Do not modify code. fix-required only for real defects.`, {label: 'review:SR2-L4', phase: 'Library', schema: REVIEW_SCHEMA})
if (rev && rev.verdict === 'fix-required') {
  await agent(`${RULES}\n\nRepo: ${G}/LibKa0s. Item SR2-L4 - REVIEW FIXES. Verify each finding against the code, fix the real ones (red test first where it applies), commit as "SR2-L4: review fixes". Findings:\n${JSON.stringify(rev.findings, null, 1)}`, {label: 'fix:SR2-L4', phase: 'Library'})
}
log(`SR2-L4 done (${rev ? rev.verdict : 'no review'})`)
phase('Release')
const rel = await agent(`${RULES}\n\nRepo: ${G}/LibKa0s. Item SR2-REL (third pass): amend the v1.105.0 release record for SR2-L4 (after the earlier SR2-REL commits): CHANGELOG version block vs live minors (tests/test_versioning.lua), docs/api current document and members JSON for every moved key, the re-pin list (popup/menu/tooltip edge sizes), docs/test-cases.md regenerated, the CLAUDE.md band census. Re-run the release battery (tests/_kit/run-automated-tests.sh, release 1.105.0, clean tree: new docs/automated-tests/<stamp>/ bundle, RESULTS.md row, ANALYSIS.md; 0 functions above CCN 15 via the vendored runner, never raw lizard) and update the CHANGELOG release-gate line. Do NOT tag. Commit "SR2-REL: ...". Final answer lists the payload files (LibKa0s/ and testkit/) changed since commit 2cd727d5.`, {label: 'SR2-REL', phase: 'Release'})
return {l4: rev, rel}
