export const meta = {
  name: 'ka0s-execute-milestone',
  description: 'Execute plan items with a dependency-aware scheduler: implement test-first, commit "<ID>: …", independent review, one fix round',
  phases: [
    { title: 'Implement', detail: 'one agent per item, serial within a repo, parallel across repos' },
    { title: 'Review', detail: 'independent review of each item commit' },
    { title: 'Fix', detail: 'one fix round when review finds real problems' },
  ],
}
const BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = `${BASE}/Ka0sAddonsCommonTasks/docs/2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION`
const BR = 'feat/2026-09-23-review-audit-remediation'
const KB = '/home/tushar/.claude/wow-addon/bin/ka0s-bounded'
const ITEMS = args.items
const ALL = new Set(ITEMS.map(i => i.id))
const TRAILER = `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ldej1stXpdhQLvEJxKqube`

const RESULT = { type: 'object', properties: {
  id: { type: 'string' }, status: { type: 'string', enum: ['done', 'already-landed', 'blocked'] },
  commits: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, reviewed: { type: 'boolean', description: 'for already-landed: true if any of the item commits carries a refs/notes/ka0s-review note (git log --notes=ka0s-review --format="%h %N")' },
  deviations: { type: 'string', description: 'where and why the implementation departed from the item text; empty if none' },
  suite: { type: 'string', description: 'final lint/tests/lizard/line-cap results' } },
  required: ['id', 'status', 'commits', 'summary', 'reviewed', 'deviations', 'suite'] }
const REVIEW = { type: 'object', properties: { ok: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['ok', 'issues'] }

const itemCmd = (id) => `python3 -c "import json;print(json.dumps([i for i in json.load(open('${BUNDLE}/plan-data/items.json'))['items'] if i['id']=='${id}'][0],indent=1))"`
const findCmd = `python3 -c "import json,glob,sys;ids=set(sys.argv[1:]);[print(json.dumps(f,indent=1)) for p in glob.glob('${BUNDLE}/inputs/findings/[A-Z]*.json') for f in json.load(open(p))['findings'] if f['id'] in ids]" <finding ids...>`

const COMMON = (it) => `You are executing one work item of the Ka0s 2026-09-23 remediation plan. Item ${it.id}, repo ${it.repo} at ${BASE}/${it.repo} (cd there; your shell starts elsewhere).
- Read the item spec: \`${itemCmd(it.id)}\`. Read the findings it resolves: \`${findCmd}\`. For context: ${BUNDLE}/03_SPEC.md (the end state), ${BUNDLE}/02_UPSTREAM_CHANGES.md, ${BUNDLE}/plan-data/PLAN_REVIEW_RESOLUTIONS.md, ${BUNDLE}/inputs/OWNER_SCOPE.md (binding owner rulings). Read ${BASE}/${it.repo}/CLAUDE.md and follow that repo's conventions (for LibKa0s also docs/releasing.md and docs/api/ conventions; for WowAddonStandards its changelog/version ripple rules).
- The repo must be on branch ${BR}; if it is not, stop and return blocked. Only touch ${it.repo} (other sibling repos are read-only). Never push, never merge, never amend or rebase existing commits, never edit an addon's libs/ or tests/_kit/.
- Heavy runs MUST go through the bounded runner: \`${KB} luacheck .\`, \`${KB} lua5.1 tests/run.lua\`, \`${KB} lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .\` (a hook blocks unbounded luacheck/lua/lizard). Gates: lint clean, tests green, no function above CCN 15, no authored .lua file above 1500 lines, plus the item's own verify commands.`

const implement = (it) => agent(`${COMMON(it)}
TASK: implement ${it.id}.
0. If \`git log --format=%s ${BR}\` already has a subject starting "${it.id}: " (or "${it.id} + " / " + ${it.id}:"), the item is landed: return status already-landed with those commits, and set reviewed=true only if one of them carries a refs/notes/ka0s-review note (\`git log --notes=ka0s-review --format='%h %s | %N' ${BR}\`). Otherwise set reviewed=false and do nothing else.
DIRTY TREE: if \`git status --porcelain\` is not empty when you start, it is leftover from an interrupted run of an item in this repo (items run one at a time per repo). Inspect the diff. If it is partial work for ${it.id}, continue from it. If it belongs to another item or you cannot tell, run \`git stash push -u -m "interrupted: <what it looks like>"\`, name the stash in deviations, and proceed from a clean tree. Never discard work with checkout/reset.
1. Where behaviour changes, write the failing (red) test first and confirm it fails for the right reason; then implement until green. Docs-only items: make the edit and run whatever gates the repo has.
2. Implement the item's change completely, including every ripple the repo's conventions demand (version/minor bumps, generated inventories such as docs/test-cases.md, API docs, changelog entries) exactly where the item or the repo's rules say so.
3. If the item text is wrong against the actual code (a wrong line cite, a name that does not exist), do what the item INTENDS and the spec requires, and record the departure in the commit body and in deviations. Return blocked only if it truly cannot be done (explain precisely).
4. Commit with \`git add\` of the specific files (never \`git add -A\` blindly; confirm \`git status\` shows nothing unrelated). Subject: "${it.id}: <imperative summary, <= 72 chars>". Body: what changed and why, the finding ids, deviations. End the message with exactly these two trailer lines:\n${TRAILER}\nIf git warned that LF will be replaced by CRLF, re-checkout the touched files (rm them, then \`git checkout -- <files>\`) so the working tree matches .gitattributes, and confirm \`git status --porcelain\` is empty.
Return the result object.`, { label: `impl:${it.id}`, phase: 'Implement', schema: RESULT })

const review = (it, res) => agent(`${COMMON(it)}
TASK: independently review the commit(s) that implemented ${it.id}: ${res.commits.join(' ')} (\`git show\` them). The implementer reported: ${res.summary}\nDeviations: ${res.deviations || 'none'}
Check, against the item spec, the findings and 03_SPEC.md: does the change actually resolve every finding it claims, correctly? Any bug, regression, missed ripple (version/minor, docs/api, test-cases.md, changelog), test that does not really pin the behaviour, standards deviation introduced, or collateral edit? Re-run the gates yourself. Do NOT edit or commit anything. If and only if ok=true, record the review so a resumed run can see it: \`git notes --ref=ka0s-review add -f -m "reviewed ok ${it.id}" <the item's LAST commit>\` (a note, not a commit). Report only REAL problems with evidence (file:line); stylistic preferences are not issues. ok=true if none.`, { label: `review:${it.id}`, phase: 'Review', schema: REVIEW })

const fix = (it, res, rev) => agent(`${COMMON(it)}
TASK: an independent review of ${it.id} (commits ${res.commits.join(' ')}) found these problems:\n${rev.issues.map((x, i) => `${i + 1}. ${x}`).join('\n')}
Verify each against the code. Fix every real one (tests first where behaviour is involved) in ONE new commit with subject "${it.id}: address review — <summary>" and the same trailer lines:\n${TRAILER}\nFor any issue you judge not real, say why in deviations. Do not amend earlier commits. After committing, record the review round as closed: \`git notes --ref=ka0s-review add -f -m "reviewed, fixed ${it.id}" <your new commit, or the item's last commit if nothing needed fixing>\`. Return the result object (commits = only the new commit, or empty if nothing needed fixing; status done).`, { label: `fix:${it.id}`, phase: 'Fix', schema: RESULT })

const runItem = async (it) => {
  const res = await implement(it)
  if (!res || res.status === 'blocked') return { it, res, rev: null }
  if (res.status === 'already-landed' && res.reviewed) return { it, res, rev: { ok: true, issues: [] } }
  const rev = await review(it, res)
  if (!rev || rev.ok || !rev.issues.length) return { it, res, rev }
  const fx = await fix(it, res, rev)
  return { it, res, rev, fix: fx }
}

const done = new Set(), failed = new Set(), busy = new Set(), running = new Map(), out = []
const pending = [...ITEMS]
while (pending.length || running.size) {
  for (const it of [...pending]) {
    if (it.deps.some(d => failed.has(d))) {
      failed.add(it.id); pending.splice(pending.indexOf(it), 1)
      log(`${it.id} skipped: a dependency failed`); out.push({ id: it.id, status: 'skipped' }); continue
    }
    if (busy.has(it.repo)) continue
    if (!it.deps.every(d => done.has(d) || !ALL.has(d))) continue
    busy.add(it.repo); pending.splice(pending.indexOf(it), 1)
    running.set(it.id, runItem(it).catch(e => ({ it, res: null, err: String(e) })))
  }
  if (!running.size) { log(`deadlock: ${pending.map(p => p.id).join(' ')}`); break }
  const r = await Promise.race(running.values())
  running.delete(r.it.id); busy.delete(r.it.repo)
  const ok = r.res && (r.res.status === 'done' || r.res.status === 'already-landed')
  if (ok) done.add(r.it.id); else failed.add(r.it.id)
  const residual = r.fix ? (r.fix.deviations || '') : ''
  log(`${r.it.id} ${ok ? 'DONE' : 'FAILED'}${r.rev && !r.rev.ok ? ` (review: ${r.rev.issues.length} issue(s), fix round run)` : ''} — ${done.size}/${ITEMS.length}`)
  out.push({ id: r.it.id, status: ok ? 'done' : 'failed', result: r.res, review: r.rev, fix: r.fix || null, err: r.err || null, residual })
}
return { done: [...done], failed: [...failed], results: out }
