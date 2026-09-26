export const meta = {
  name: 'ats-sweep-m4-syncdocs',
  description: 'Automated-tests sweep M4: /wow-addon:sync-docs per touched repo on the sweep branch, committed, independently reviewed',
  phases: [{ title: 'Sync', detail: 'one sync-docs pass per repo' }, { title: 'Review', detail: 'independent doc-accuracy check' }],
}
const BUNDLE = '/mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-AUTOMATED_TESTS_SWEEP'
const BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const TRAILERS = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0137w2iyvwbPYwaYca4pi2Bz'
const SD = { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string', enum: ['landed', 'no_drift', 'already_done', 'blocked'] }, sha: { type: 'string' }, summary: { type: 'string' }, gate: { type: 'string' }, pendingCommentCitations: { type: 'array', items: { type: 'string' } }, proof: { type: 'string' } }, required: ['id', 'status', 'summary', 'pendingCommentCitations'] }
const VER = { type: 'object', properties: { ok: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['ok', 'issues'] }

const results = await pipeline(args.repos,
  (x) => agent(`Item ${x.id} of the Ka0s automated-tests sweep (plan ${BUNDLE}/01_EXECUTION_PLAN.md, M4). Repo ${BASE}/${x.repo}, branch feat/2026-09-26-automated-tests-sweep, must be clean (if a commit subject "${x.id}: " exists, return already_done).
Run the ${x.skill} command for this repo (invoke the Skill tool with skill "${x.skill}"; if unavailable, read its command file under ${BASE}/wow-addon/commands/ or the dev-copilot plugin and follow it). There is no human to answer questions: apply every documentation rewrite the command would make to docs files (README, CLAUDE*.md, DEPENDENCIES.md, ARCHITECTURE*, docs/*.md that it owns). Do NOT edit comments inside source/test code — the command requires owner confirmation for those; instead list every stale comment citation you find (file:line, what it says, what is true) in pendingCommentCitations. Never edit frozen bundles (docs/automated-tests/<stamp>/, docs/audits/, docs/reviews/, docs/revendor/<date>/, docs/perf-analysis/) or libs/, tests/_kit/.
Heavy commands through ~/.claude/wow-addon/bin/ka0s-bounded. If Write refuses a file, write to your scratchpad and cp it into place. Keep line endings per .gitattributes. Run the repo's green gate after (docs tests like doc_structure/test-cases/citation checks live in the suite).
If there is drift: ONE commit, subject "${x.id}: Sync docs to the tree after the automated-tests sweep", body listing what changed, ending with a blank line then:
${TRAILERS}
If there is no drift: return no_drift and a proof (the command(s) you ran and their clean result). Do not push.`,
    { label: `sync ${x.repo}`, phase: 'Sync', schema: SD }),
  (r, x) => r && r.status === 'landed' ? agent(`Independently review commit ${r.sha} ("${x.id}") in ${BASE}/${x.repo}: a documentation sync. For each changed claim, check it against the tree (counts, file names, line figures, commands, versions, LibKa0s v1.62.0 provenance). Flag anything now wrong, any edit to code or to a frozen bundle, and line-ending violations. Re-run the repo's test suite through ~/.claude/wow-addon/bin/ka0s-bounded (doc tests live there). Do not modify anything. Write a git note: git -C ${BASE}/${x.repo} notes --ref=ka0s-review add -f -m "${x.id} review: PASS|FAIL — <verdict>" ${r.sha}. Return ok and concrete issues.`,
    { label: `review ${x.repo}`, phase: 'Review', schema: VER }).then((v) => ({ sync: r, review: v })) : { sync: r }
)
return results