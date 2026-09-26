export const meta = {
  name: 'ats-sweep-execute',
  description: 'Automated-tests sweep: run item chains per repo (implement -> independent review -> fix loop), git is state',
  phases: [{ title: 'Execute', detail: 'one sequential chain per repo, chains in parallel' }],
}

const BUNDLE = '/mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-AUTOMATED_TESTS_SWEEP'
const BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
const BR = 'feat/2026-09-26-automated-tests-sweep'
const TRAILERS = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0137w2iyvwbPYwaYca4pi2Bz'

const IMPL = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    status: { type: 'string', enum: ['landed', 'already_done', 'exception', 'blocked'] },
    sha: { type: 'string' },
    summary: { type: 'string' },
    gate: { type: 'string' },
    blocker: { type: 'string' },
  },
  required: ['id', 'status', 'summary'],
}
const REVIEW = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    issues: { type: 'array', items: { type: 'string' } },
    noteWritten: { type: 'boolean' },
  },
  required: ['verdict', 'issues', 'noteWritten'],
}

const common = (repo) => `
Context: you are executing one item of the Ka0s automated-tests sweep plan. The plan bundle is ${BUNDLE}
(read 01_EXECUTION_PLAN.md, especially "Rules every fix item follows", and 00_FIX_QUEUE.md for the evidence;
items.tsv has the item's full title). The repo is ${BASE}/${repo}; follow its own CLAUDE.md (green gate, conventions,
line endings). Branch: ${BR} (if the repo is not on it and no sweep item has landed there, cut it from master;
if the repo is on another branch, stop and report blocked).
- Every heavy command (lua tests, perf, luacheck, lizard, run-automated-tests.sh) goes through
  ~/.claude/wow-addon/bin/ka0s-bounded. Exit 124 = time limit, 137 = killed: report as such.
- If the Write tool refuses a file (subagent report-file guard), write it into your scratchpad directory and cp
  it into place. If the bounded-run hook blocks a heredoc because its prose mentions a tool name, use the
  scratchpad-file + cp route instead. Never disable the hook.
- Never reset --hard / checkout . unread work. Never edit frozen bundles (docs/automated-tests/<stamp>/,
  docs/audits/, docs/reviews/). In addons never hand-edit libs/LibKa0s/ or tests/_kit/.
- Other agents work in OTHER repos concurrently; touch only ${repo} (a perf bisect may use a throwaway
  git worktree under your scratchpad; remove it when done).
- Commit messages end with a blank line then exactly:
${TRAILERS}`

async function runItem(repo, id) {
  const impl = await agent(`${common(repo)}

YOUR ITEM: ${id} (look up its title and traces in items.tsv).
1. Run ${BUNDLE}/resume-state.sh and check git: if a commit subject "${id}: " already exists in ${repo}, return status already_done with its sha.
2. If the tree is dirty, read the diff: continue it if it is this item's partial work, else stash it with a message naming it.
3. Do the item fully and carefully, per the plan's rules. Investigate the code before cutting; peels are moves on real seams,
   no behavior change; test counts must be preserved exactly on test splits (state before/after totals).
4. Run the repo's full green gate (bounded). Everything must be green; no authored file over 1500 lines.
5. Commit as ONE commit with subject "${id}: <what changed>" and a body citing the ATS ids (and "Fixes #N" for an existing issue it fixes).
   If the item honestly needs no code change (e.g. a CCN function with no permitted refactor shape, or a perf rise that is an intended feature),
   still land a commit that records the finding in the right doc (commit body explains), unless the plan says an exceptions.tsv row is right —
   in that case append the row to ${BUNDLE}/exceptions.tsv (do not commit it; say so) and return status exception.
6. If you cannot complete it (red gate you cannot fix within the item's scope, missing prerequisite), leave the tree clean or stashed and return blocked with the reason.
Return: id, status, sha (short), summary (what changed, figures before/after), gate (the gate figures).`,
    { label: `impl ${id}`, phase: 'Execute', schema: IMPL })
  if (!impl) return { id, status: 'died' }
  if (impl.status === 'blocked' || impl.status === 'exception') return { id, impl }

  let review = null
  for (let round = 0; round < 3; round++) {
    review = await agent(`${common(repo)}

You are the INDEPENDENT REVIEWER for item ${id} in ${repo}. You did not write it; be skeptical.
Find the item's commit(s): subjects starting "${id}: " and any "${id}R: " fixes on ${BR}. Review the full diff against:
the item's title in items.tsv, the plan's rules (peel = move on a real seam, no behavior change, test counts preserved, load order,
census/watch-list rows; CCN items only via performance-§11 permitted shapes, no extraction for the number; perf items: bisect evidence real),
the repo's CLAUDE.md conventions, line endings, and the ripple (docs, test inventories, TOC/xml, majors, manifests) the change owes.
Re-run the repo's full green gate yourself (bounded) and check no authored file exceeds 1500 lines.
Do NOT modify code. Then write a git note on the item's LAST commit (the ${id} or latest ${id}R commit):
  git -C ${BASE}/${repo} notes --ref=ka0s-review add -f -m "${id} review: PASS|FAIL — <one-paragraph verdict with gate figures>" <sha>
Return verdict pass only if the item is complete and correct; otherwise fail with concrete, actionable issues (file:line).`,
      { label: `review ${id}${round ? ' r' + round : ''}`, phase: 'Execute', schema: REVIEW })
    if (!review || review.verdict === 'pass') break
    if (round === 2) break
    const fix = await agent(`${common(repo)}

Item ${id} in ${repo} FAILED independent review. Fix exactly these issues, then run the full green gate (bounded) and
commit ONE commit with subject "${id}R: <what was fixed>":
${review.issues.map((s) => '- ' + s).join('\n')}
If you believe an issue is wrong, do not change code for it; explain in your summary. Return the IMPL schema with status landed (or blocked).`,
      { label: `fix ${id} r${round + 1}`, phase: 'Execute', schema: IMPL })
    if (!fix || fix.status === 'blocked') return { id, impl, review, fix }
  }
  return { id, impl, review }
}

const results = await parallel(args.chains.map((c) => async () => {
  const out = []
  for (const id of c.items) {
    const r = await runItem(c.repo, id)
    out.push(r)
    log(`${c.repo} ${id}: ${r.impl ? r.impl.status : r.status}${r.review ? ' / review ' + r.review.verdict : ''}`)
    const ok = r.impl && (r.impl.status === 'landed' || r.impl.status === 'already_done' || r.impl.status === 'exception') && (!r.review || r.review.verdict === 'pass')
    if (!ok) { log(`${c.repo}: chain stopped at ${id}`); break }
  }
  return { repo: c.repo, out }
}))
return results