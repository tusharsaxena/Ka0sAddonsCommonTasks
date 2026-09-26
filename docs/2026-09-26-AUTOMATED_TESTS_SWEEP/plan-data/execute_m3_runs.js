export const meta = {
  name: 'ats-sweep-m3-runs',
  description: 'Automated-tests sweep M3: fresh recorded /wow-addon:automated-tests run per repo, dispositions refreshed, committed, then independently verified',
  phases: [{ title: 'Run', detail: 'one recorded battery per repo' }, { title: 'Verify', detail: 'numbers-vs-artifacts check' }],
}
const BUNDLE = '/mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-AUTOMATED_TESTS_SWEEP'
const BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const TRAILERS = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0137w2iyvwbPYwaYca4pi2Bz'
const RUN = { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string', enum: ['landed', 'already_done', 'blocked'] }, sha: { type: 'string' }, bundle: { type: 'string' }, verdict: { type: 'string' }, suites: { type: 'string' }, newlyCrossed: { type: 'string' }, notes: { type: 'string' } }, required: ['id', 'status', 'suites', 'notes'] }
const VER = { type: 'object', properties: { ok: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['ok', 'issues'] }

const results = await pipeline(args.repos,
  (x) => agent(`Item ${x.id} of the Ka0s automated-tests sweep (plan: ${BUNDLE}/01_EXECUTION_PLAN.md, M3). Repo: ${BASE}/${x.repo}, branch feat/2026-09-26-automated-tests-sweep (must be clean; if a commit subject "${x.id}: " exists, return already_done).
Perform the /wow-addon:automated-tests command for this repo EXACTLY as its playbook says (invoke the Skill tool with skill "wow-addon:automated-tests" if available; otherwise read ${BASE}/wow-addon/commands/automated-tests.md and follow it, fetching the AUTOMATED_TESTS.md playbook — the local clone ${BASE}/WowAddonStandards is acceptable if the network hangs). Every run through ~/.claude/wow-addon/bin/ka0s-bounded. Capture runner console output to a unique path in your scratchpad, never a shared name.
Write <bundle>/ANALYSIS.md per the template (if Write refuses it, write to your scratchpad and cp it in; never disable the bounded hook). Line endings per .gitattributes.
ATS-23: in RESULTS.md, refresh EVERY carried Disposition cell whose figures are stale so it states today's figures (keep the ruling unless the facts changed; this sweep peeled many files — a file that left the band leaves the table; a file newly in the band needs a ruling). Only Disposition cells are authored; never hand-edit generated rows or frozen bundles.
Then commit the bundle + RESULTS.md as ONE commit, subject "${x.id}: Final automated-tests sweep run (<stamp>)", body summarising the figures and what moved vs the 2026-09-26 sweep run. End the message with a blank line then:
${TRAILERS}
Do not push. Return id, status, sha, bundle path, verdict, one-line-per-suite figures, anything newly crossed, and notes (skips, oddities).`,
    { label: `run ${x.repo}`, phase: 'Run', schema: RUN }),
  (r, x) => r && r.status === 'landed' ? agent(`Independently verify commit ${r.sha} ("${x.id}") in ${BASE}/${x.repo}. Read the new bundle's manifest.json and suite artifacts and check: ANALYSIS.md exists and every figure in it matches an artifact (no invented numbers); the RESULTS.md new row matches the manifest; the Disposition cells state current figures (compare against the bundle's complexity.txt / wc -l) and no generated row was hand-edited; no frozen older bundle changed in the commit (git show --stat); line endings match .gitattributes. Do not modify anything. Return ok and concrete issues.`,
    { label: `verify ${x.repo}`, phase: 'Verify', schema: VER }).then((v) => ({ run: r, verify: v })) : { run: r }
)
return results