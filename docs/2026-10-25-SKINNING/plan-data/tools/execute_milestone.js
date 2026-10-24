export const meta = {
  name: 'ka0s-execute-milestone-2026-10-25',
  description: 'Execute skinning (leg 1) plan items: dependency-aware scheduler, test-first implement, commit "<ID>: …", independent review, one fix round',
  phases: [
    { title: 'Implement', detail: 'one agent per item, serial within a repo, parallel across repos' },
    { title: 'Review', detail: 'independent review of each item commit' },
    { title: 'Fix', detail: 'one fix round when review finds real problems' },
  ],
}
const BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BUNDLE = `${BASE}/Ka0sAddonsCommonTasks/docs/2026-10-25-SKINNING`
const BR = 'feat/2026-10-25-skinning'
const KB = '/home/tushar/.claude/dev-copilot/bin/ka0s-bounded'
const TRAILER = `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Kt1E8LrUvMRud7LfQfXGD7`

// Input: args.items = [{id, repo, deps, note?}] (hard deps: a failed dep skips the item), or
//        args.order = {repo: [ids in execution order]} (soft chain per repo; each implementer checks its
//        real depends_on in git). args.note (optional) = an owner/lead ruling handed to every agent.
let ITEMS = []
if (args.order) {
  for (const [repo, ids] of Object.entries(args.order)) ids.forEach((id, k) => ITEMS.push({ id, repo, deps: [], soft: k ? [ids[k - 1]] : [] }))
} else ITEMS = args.items.map(i => ({ ...i, soft: [] }))
const ALL = new Set(ITEMS.map(i => i.id))

const RESULT = { type: 'object', properties: {
  id: { type: 'string' }, status: { type: 'string', enum: ['done', 'already-landed', 'blocked'] },
  commits: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' },
  reviewed: { type: 'boolean', description: 'for already-landed: true if any item commit carries a refs/notes/ka0s-review note' },
  deviations: { type: 'string', description: 'where and why the implementation departed from the item text; empty if none' },
  library_gap: { type: 'string', description: 'for addon items: a LibKa0s contract gap found (needs an additive library fix + local tag move); empty if none' },
  suite: { type: 'string', description: 'final lint/tests/line-cap results' } },
  required: ['id', 'status', 'commits', 'summary', 'reviewed', 'deviations', 'library_gap', 'suite'] }
const REVIEW = { type: 'object', properties: { ok: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['ok', 'issues'] }

const itemCmd = (id) => `python3 -c "import json;print(json.dumps([i for i in sum([json.load(open(f))['items'] for f in ['${BUNDLE}/plan-data/items.json']+sorted(__import__('glob').glob('${BUNDLE}/plan-data/addendum-*.json'))],[]) if i['id']=='${id}'][0],indent=1,ensure_ascii=False))"`

const COMMON = (it) => `You are executing one work item of the Ka0s 2026-10-25 run "skinning, leg 1: LibKa0s skin engine + LootHistory prototype". Item ${it.id}, repo ${it.repo} at ${BASE}/${it.repo} (cd there; your shell starts elsewhere).
- Read the item spec: \`${itemCmd(it.id)}\` (any 'PLAN-REVIEW RESOLUTION' paragraph in it binds over the text above it). Binding rulings: ${BUNDLE}/inputs/OWNER_SCOPE.md. The end state: ${BUNDLE}/03_SPEC.md. Evidence: ${BUNDLE}/inputs/LIBKA0S_INTERNALS.md, LOOTHISTORY_SURFACES.md, ACEGUI_AND_ENGINE_RESEARCH.md; mockups and token tables: ${BUNDLE}/plan-data/mockups/ and ${BUNDLE}/inputs/mockup-tokens.dc.html (OWNER_SCOPE and the item spec override the evidence). Read ${BASE}/${it.repo}/CLAUDE.md and follow that repo's conventions (LibKa0s: also docs/releasing.md and the docs/api conventions; WowAddonStandards: its changelog/version ripple rules). The owner has explicitly instructed per-item commits on the run branch; that overrides any repo rule requiring a slash command to commit.
- BRANCH: the repo must be on ${BR}. If ${BR} does not exist yet in this repo and the tree is clean on its default branch (\`git symbolic-ref --short refs/remotes/origin/HEAD\`), create it there: \`git switch -c ${BR}\`. If the repo is on any other branch, stop and return blocked.
- Only touch ${it.repo} (sibling repos are read-only), EXCEPT a Ka0sAddonsCommonTasks bundle file the item spec names (exceptions.tsv, 99_EXECUTION_RECORD.md), which you may edit without committing there. Never push, never merge, never amend or rebase existing commits, never move or push a tag (the one exception: LK-90 creates the LOCAL annotated tag v1.78.0). Never edit an addon's libs/ or tests/_kit/ except in a <PFX>-RV item, which replaces them whole from the LibKa0s v1.78.0 local tag (\`git -C ${BASE}/LibKa0s archive v1.78.0 LibKa0s testkit | tar -x -C <tmp>\`; never check the tag out in that repo).${args.note ? `\n- RULING FOR THIS RUN (binding): ${args.note}` : ''}${it.note ? `\n- RULING FOR THIS ITEM (binding): ${it.note}` : ''}
- dev-copilot commands: use the INSTALLED plugin (read the skill/command files under ~/.claude/plugins/cache/dev-copilot/dev-copilot/<newest>/), never the ../dev-copilot checkout, except when the item's repo IS dev-copilot.
- Scratch: other agents run in parallel. Put temporary files under a directory YOU create with \`mktemp -d /tmp/claude-1000/ka0s-${it.id}.XXXXXX\`. Never git init/add/commit anywhere except ${BASE}/${it.repo} or your own mktemp dir.
- Heavy runs go through the bounded runner: \`${KB} luacheck .\`, \`${KB} lua tests/run.lua\` (use the interpreter the repo's CLAUDE.md names), and the repo's other gates. Gates: lint 0/0, tests green, no authored .lua file above 1500 lines, plus the item's VERIFY commands. Never run raw lizard over a tree.
- In-client smoke checks are the owner's: write them into the repo's smoke docs as the item says, never mark one passed.
- If, in an addon item, the LibKa0s contract cannot serve the need (a real gap, not a misunderstanding), do NOT work around it with a private copy: stop at a green state, return status blocked with library_gap describing the minimal additive fix.`

const implement = (it) => agent(`${COMMON(it)}
TASK: implement ${it.id}.
0. LANDED CHECK: if \`git log --format=%s <default>..${BR}\` has a subject starting "${it.id}: " (or "${it.id} + " / " + ${it.id}:"), the item is landed. Return already-landed with those commits; reviewed=true only if one carries a refs/notes/ka0s-review note (\`git log --notes=ka0s-review --format='%h %s | %N' <default>..${BR}\`). Some items legitimately land as more than one commit with the same prefix (the spec says so); if the spec's later part is missing, continue it instead.
0b. DEPENDENCIES: for each id in depends_on, confirm it landed in its own repo (same rule, run branch on top of that repo's default branch) or is listed in ${BUNDLE}/exceptions.tsv. If one is missing, return blocked naming it and change nothing.
DIRTY TREE: if \`git status --porcelain\` is not empty, it is leftover from an interrupted item (items run one at a time per repo). If it is partial work for ${it.id}, continue it. Otherwise \`git stash push -u -m "interrupted: <what it looks like>"\`, name the stash in deviations, and proceed clean. Never discard work with checkout/reset.
1. Where behaviour changes, write the failing test first and confirm it fails for the right reason; then implement until green. Docs-only items: make the edit and run the repo's gates.
2. Implement completely, with every ripple the repo's conventions demand (minor bumps, version keys, members manifests via tools/gen-api-members.lua, docs/api, CHANGELOG, generated inventories, README/ARCHITECTURE/smoke docs) exactly where the item or the repo's rules say.
3. If the item text is wrong against the code (a stale line cite, a renamed symbol), do what the item INTENDS and the spec requires, and record the departure in the commit body and deviations. Return blocked only if it truly cannot be done.
4. Commit with \`git add\` of the specific files (confirm \`git status\` shows nothing unrelated). Subject: "${it.id}: <imperative summary, <= 72 chars>". Body: what changed and why, the issue refs, deviations, and 'Closes #N' only where the spec says so. End the message with exactly these two trailer lines:\n${TRAILER}\nIf git warned that LF will be replaced by CRLF, re-checkout the touched files so the tree matches .gitattributes and \`git status --porcelain\` is empty.
Return the result object.`, { label: `impl:${it.id}`, phase: 'Implement', schema: RESULT })

const review = (it, res) => agent(`${COMMON(it)}
TASK: independently review the commit(s) that implemented ${it.id}: ${res.commits.join(' ')} (\`git show\` them). The implementer reported: ${res.summary}\nDeviations: ${res.deviations || 'none'}
Check against the item spec, OWNER_SCOPE.md and 03_SPEC.md: is every part of the item done, correctly? Any bug, regression, missed ripple (minor/version key, members manifest, docs/api, CHANGELOG, test inventory, README/ARCHITECTURE/smoke docs), a test that does not really pin the behaviour, a new standards deviation, library surface beyond what the item spec defines (no extra public members), or collateral edits? For a <PFX>-RV item: are libs/LibKa0s and tests/_kit byte-identical to the v1.78.0 local tag apart from media/icons pruned exactly to the CLAUDE.md 'LibKa0s icons:' line (each set's license/attribution files kept with any shipped icon), is the provenance line rolled, the docs/revendor bundle present, and every icon the addon draws (host seams, data tables, library-drawn close/copy/clear/info it wires) declared? Re-run the gates yourself. Do NOT edit or commit. If and only if ok=true: \`git notes --ref=ka0s-review add -f -m "reviewed ok ${it.id}" <the item's LAST commit>\`. Report only REAL problems with evidence (file:line). ok=true if none.`, { label: `review:${it.id}`, phase: 'Review', schema: REVIEW })

const fix = (it, res, rev) => agent(`${COMMON(it)}
TASK: an independent review of ${it.id} (commits ${res.commits.join(' ')}) found:\n${rev.issues.map((x, i) => `${i + 1}. ${x}`).join('\n')}
Verify each against the code. Fix every real one (tests first where behaviour is involved) in ONE new commit, subject "${it.id}: address review — <summary>", same trailer lines:\n${TRAILER}\nFor any issue you judge not real, say why in deviations. Do not amend. After committing: \`git notes --ref=ka0s-review add -f -m "reviewed, fixed ${it.id}" <your new commit, or the item's last commit if nothing needed fixing>\`. Return the result object (commits = only the new commit, or empty; status done).`, { label: `fix:${it.id}`, phase: 'Fix', schema: RESULT })

const runItem = async (it) => {
  const res = await implement(it)
  if (!res || res.status === 'blocked') return { it, res, rev: null }
  if (res.status === 'already-landed' && res.reviewed) return { it, res, rev: { ok: true, issues: [] } }
  const rev = await review(it, res)
  if (!rev || rev.ok || !rev.issues.length) return { it, res, rev }
  const fx = await fix(it, res, rev)
  return { it, res, rev, fix: fx }
}

const done = new Set(), failed = new Set(), finished = new Set(), busy = new Set(), running = new Map(), out = []
const pending = [...ITEMS]
while (pending.length || running.size) {
  for (const it of [...pending]) {
    if (it.deps.some(d => failed.has(d))) {
      failed.add(it.id); finished.add(it.id); pending.splice(pending.indexOf(it), 1)
      log(`${it.id} skipped: a dependency failed`); out.push({ id: it.id, status: 'skipped' }); continue
    }
    if (busy.has(it.repo)) continue
    if (!it.deps.every(d => done.has(d) || !ALL.has(d))) continue
    if (!it.soft.every(d => finished.has(d))) continue
    busy.add(it.repo); pending.splice(pending.indexOf(it), 1)
    running.set(it.id, runItem(it).catch(e => ({ it, res: null, err: String(e) })))
  }
  if (!running.size) { log(`deadlock: ${pending.map(p => p.id).join(' ')}`); break }
  const r = await Promise.race(running.values())
  running.delete(r.it.id); busy.delete(r.it.repo); finished.add(r.it.id)
  const ok = r.res && (r.res.status === 'done' || r.res.status === 'already-landed')
  if (ok) done.add(r.it.id); else failed.add(r.it.id)
  log(`${r.it.id} ${ok ? 'DONE' : (r.res && r.res.status === 'blocked' ? 'BLOCKED' : 'FAILED')}${r.res && r.res.library_gap ? ' [LIBRARY GAP]' : ''}${r.rev && !r.rev.ok ? ` (review: ${r.rev.issues.length} issue(s), fix round run)` : ''} — ${done.size}/${ITEMS.length}`)
  out.push({ id: r.it.id, status: ok ? 'done' : 'failed', result: r.res, review: r.rev, fix: r.fix || null, err: r.err || null })
}
return { done: [...done], failed: [...failed], results: out }
