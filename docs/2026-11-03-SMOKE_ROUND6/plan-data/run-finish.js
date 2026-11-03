export const meta = {
  name: 'r6-finish',
  description: 'Round 6 finish: automated tests and sync-docs per repo, finalize (merge, push, tag v1.85.0, cleanup), then close the GitHub issues the merged work resolved; Outfitter excluded',
  phases: [
    { title: 'Tests+Docs', detail: 'R6-AT then R6-SD per addon; R6-SD in LibKa0s and WowAddonStandards' },
    { title: 'Finalize', detail: 'R6-FIN: merge --no-ff in dependency order, push, tag, cleanup' },
    { title: 'Issues', detail: 'R6-ISSUES: assess per repo (read-only), then one spaced-out closer' },
    { title: 'Record', detail: 'checkpoint, merge Ka0sAddonsCommonTasks' },
  ],
}
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const B = `${G}/Ka0sAddonsCommonTasks/docs/2026-11-03-SMOKE_ROUND6`
const BR = 'feat/2026-11-01-full-skinning'
const ADDONS = ['LibKa0sSkinTester','AbsorbTracker','AuraMaster','BankLedger','ConsumableMaster','DpsRace','DropWatcher','KickCD','LootHistory','MultiMeters','PanelMaster','PartyFrameEnhanced','PremadeGroupsFilterExtension','PrettyChat','QuickComms','WhatGroup']
const TR = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JV4dmLSn8ys2xpPiPZV4gK'
const BASE = `You are an unattended workflow step in the finish of round 6 of the Ka0s full skinning run. Bundle: ${B}. Read R6_ADDENDUM_SIM_RENAME_FINISH.md (the owner's finish instructions: "After the workflow completes, Run automated-tests, Do a sync-docs, Do a finalize", and "after finalize, please close all github issues that have been done"), items.tsv and 99_REPORT.md. Every repo is on branch ${BR}; check it. Rules: NEVER modify, re-vendor into, merge, push or close issues in ${G}/Outfitter: a separate agent owns it (owner: "ignore the Outfitter repo from this sweep"). Never bump an addon version or cut a release. Never reset --hard or checkout . over unread work. Skip an id whose "<ID>: " commit already exists in the repo. Each repo's CLAUDE.md governs its green gate (/home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua, ka0s-bounded luacheck . 0/0, 1500-line cap, CRLF eol test). Use your own scratch directory, never a shared one. Commit subjects "<ID>: <sentence>", body ending:\n${TR}\nNever mark a smoke check passed. A question from the owner that appears mid-task is for the lead: note it and carry on. Use literal refspecs in git push (zsh reads $B:r as a modifier).`
const OK = { type: 'object', properties: { ok: { type: 'boolean' }, commits: { type: 'array', items: { type: 'string' } }, tests: { type: 'string' }, report: { type: 'string' } }, required: ['ok', 'report'] }
const ISS = { type: 'object', properties: { repo: { type: 'string' }, close: { type: 'array', items: { type: 'object', properties: { number: { type: 'number' }, title: { type: 'string' }, commit: { type: 'string' }, comment: { type: 'string' } }, required: ['number', 'commit', 'comment'] } }, keep: { type: 'array', items: { type: 'object', properties: { number: { type: 'number' }, title: { type: 'string' }, why: { type: 'string' } }, required: ['number', 'why'] } } }, required: ['repo', 'close', 'keep'] }
const SD_NOTE = `Before you start, read the reviewers' notes on this branch: git log --notes=ka0s-review master..${BR} (and git notes --ref=ka0s-review list). Notes and builder reports left stale-doc items explicitly for sync-docs (README Tests badges behind the live count, docs that still call the sim verb slash-only with no launcher entry, settings-panel row counts such as MultiMeters' Columns page at 12 when it is 13, a README Simulator section that does not mention the new Sim mode box); fix every one that applies to this repo.`

phase('Tests+Docs')
const libDocs = parallel([
  () => agent(`${BASE}\nRepo ${G}/LibKa0s. Item R6-SD: run the installed Skill "dev-copilot:sync-docs" here, content sync only (do not create or move documents; record anything you would have proposed). The payload (LibKa0s/ and tests/_kit/) must not change: tag v1.85.0 is what the addons vendored. Confirm afterwards with git diff --stat v1.85.0 -- LibKa0s tests/_kit (empty). Gate green. Commit "R6-SD: ..." (skip the commit and say so if nothing drifted). Do not move the tag.`, { label: 'sync-docs LibKa0s', phase: 'Tests+Docs', schema: OK }),
  () => agent(`${BASE}\nRepo ${G}/WowAddonStandards. Item R6-SD: run the installed Skill "dev-copilot:sync-docs" here, content sync only (do not create or move documents). bash scripts/check-standard.sh must exit 0. Commit "R6-SD: ..." (skip and say so if nothing drifted).`, { label: 'sync-docs WowAddonStandards', phase: 'Tests+Docs', schema: OK }),
])
const per = await pipeline(ADDONS,
  a => agent(`${BASE}\nRepo ${G}/${a}. Item R6-AT: run the installed Skill "dev-copilot:wow-automated-tests" here: the full battery through the vendored runner, a frozen bundle in docs/automated-tests/<stamp>/, RESULTS.md rolled, ANALYSIS.md written. If the battery finds a real failure, fix it test-first only when it is small and clearly a regression of this run; otherwise stop and report it with ok=false. Commit "R6-AT: ...".`, { label: `tests:${a}`, phase: 'Tests+Docs', schema: OK }),
  (r, a) => (r && !r.ok && a === 'LibKa0sSkinTester') ? agent(`${BASE}\nRepo ${G}/${a}. Item R6-AT, repair: the recorded battery (109cad2) was amber only because perf skinRepaint is over its pins in tests/perf.lua (1415.0 calls vs 1360, 249621.7 bytes vs 221880, pinned at SF-ST-2 3e5a661). The lead's call: re-pin, do not cut work. The bisect in that bundle's ANALYSIS.md shows the rise came in steps at deliberate skin commits (R3-RV 115020c, R4-ST1/ST3/ST4, R5-RV, R5-WIN) and round 6 left it flat; the pin comment's own rule (re-measure and re-pin at each LibKa0s re-vendor) was missed then. Re-measure skinRepaint (several runs, take the stable figure), set its limits with the same headroom rule the comment uses, and extend the comment with the date, the new figures and the commits that moved them. Gate green, then re-run the installed Skill "dev-copilot:wow-automated-tests" so a green bundle is recorded. Commit "R6-AT: ..." (the re-pin and the new bundle may be one or two commits). Return ok=true only if the new bundle is green.`, { label: `repin:${a}`, phase: 'Tests+Docs', schema: OK }).then(x => (x && x.ok) ? x : null) : r,
  (r, a) => (r && r.ok) ? agent(`${BASE}\nRepo ${G}/${a}. Item R6-SD: run the installed Skill "dev-copilot:sync-docs" here, content sync only (do not create or move documents; record what you would have proposed). ${SD_NOTE} The README is display-name-only per R6-NAME: keep it. Never touch libs/ or tests/_kit/ or frozen bundles. Gate green. Commit "R6-SD: ..." (skip and say so if nothing drifted). R6-AT result for context: ${JSON.stringify(r).slice(0, 1500)}`, { label: `docs:${a}`, phase: 'Tests+Docs', schema: OK }).then(d => ({ at: r, sd: d })) : { at: r, sd: null },
)
const [lsd, wsd] = await libDocs
const bad = ADDONS.filter((a, i) => !per[i] || !per[i].at || !per[i].at.ok || !per[i].sd || !per[i].sd.ok)
if (bad.length || !lsd || !lsd.ok || !wsd || !wsd.ok) return { stopped: 'tests+docs', bad, per, lsd, wsd }

phase('Finalize')
// R6-FIN ran in the lead's session: subagent pushes to master were refused by the permission classifier (finalize agent, 2026-11-04).
const fin = { ok: true, report: 'R6-FIN done by the lead: 18 repos merged --no-ff (R6-FIN), master and notes pushed, tag v1.85.0 pushed, branch deleted locally and on origin; no stashes or extra worktrees.' }

phase('Issues')
const REPOS = ['WowAddonStandards', 'LibKa0s', ...ADDONS]
const found = await parallel(REPOS.map(r => () => agent(`${BASE}\nItem R6-ISSUES, assessment only for ${G}/${r}: READ ONLY, make no GitHub write. The branch is now merged into master. List open issues (gh issue list -R <owner/repo from git remote> --state open --limit 200 --json number,title,labels,body). For each, decide whether the merged work on master resolves it completely: look for commits citing it (git log master --grep "#<n>"), state:done labels, bundle evidence under ${G}/Ka0sAddonsCommonTasks/docs/2026-11-0* (items.tsv issue refs, 99_REPORT.md), and read the code on master to confirm the issue's ask is actually true now. Close only when complete and evidenced by a commit on master; partial, deferred or untouched stays open. Fixed rules: LibKa0s #71 and #72 close (round 6 shipped them; find the commits); LibKa0s #70 and #74 stay open. Return the close list with the commit and a one-paragraph comment naming the commit and what it did, and the keep list with why.`, { label: `issues:${r}`, phase: 'Issues', schema: ISS })))
const plan = found.filter(Boolean)
// The writes and the record are done by the lead (subagent outward writes are refused).
return { plan }
