# PROGRESS — live execution ledger

**This file is written DURING execution and is the one document in this directory that changes.**
The other seven are the frozen record of what was intended and are never rewritten. When the work is
finished this file's contents are folded into `07_EXECUTION_RECORD.md` and this file is deleted.

**If this session was interrupted, start here.** Everything needed to resume is below: what is done,
what is in flight, and the exact commands to establish ground truth from the repositories rather than
from this file. **Trust the repositories over this file** — this file is updated after a milestone
completes, so an interruption mid-milestone leaves it stale by design.

Execution began 2026-09-07.

---

## Ground truth — one command

```sh
cd docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION && ./resume-state.sh -v
```

That reads the thirteen repositories and prints what has landed, per milestone, plus a `RESUME:` line
naming every item id still outstanding. **It does not read this file**, which is the point: it cannot
be stale and it cannot be wrong about work it can see. Hand its `RESUME:` list to the next workflow
and the run picks up exactly where the last one stopped.

It works because **every commit subject opens with its item id** — `M2-09: …` — so "has this landed?"
is a `git log` question in the repo that owns it. `items.tsv` beside the script is the manifest of all
106 items and their owning repository, generated from `04_EXECUTION_PLAN.md` rather than typed by hand.

**Two items land without a commit** and would otherwise read as outstanding forever: `M1-LK-00`, which
repairs working-tree bytes against an index that is already correct, and `M4-03`, which is a smoke-only
session. They live in `exceptions.tsv` with a command in the reason column that a reader can run to
check the claim. Nothing goes in that file without one.

### Re-running an item is safe

Every item is scoped to its own files and ends in one commit. Handing a workflow an item that already
landed wastes an agent; it does not corrupt anything, because the agent finds the change already
present and reports `not-needed`. **Prefer re-running a doubtful item to assuming it is done.**

### The manual fallback, if the script is unavailable

```sh
BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-07-audit-review-remediation

# What branch is each repo on, and what has landed?
for r in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters \
         PanelMaster PrettyChat WhatGroup LibKa0s WowAddonStandards wow-addon \
         Ka0sAddonsCommonTasks; do
  printf '%-22s %-42s dirty:%s\n' "$r" "$(git -C $BASE/$r rev-parse --abbrev-ref HEAD)" \
    "$(git -C $BASE/$r status --porcelain | wc -l)"
done

# Which work items have actually landed? Every commit subject opens with its item id.
for r in LibKa0s WowAddonStandards wow-addon AbsorbTracker BankLedger ConsumableMaster \
         KickCD LootHistory MultiMeters PanelMaster PrettyChat WhatGroup; do
  echo "== $r"; git -C $BASE/$r log --oneline master..$BR 2>/dev/null | sed 's/^/   /'
done

# Do the tags exist yet, and where do they point?
git -C $BASE/LibKa0s tag -l 'v1.2*' --format='%(refname:short) %(objectname:short)'
```

An item is **done** when a commit whose subject opens with its id exists on the branch. That is the
only definition used here, and it is checkable without this file.

---

## Decisions this execution runs under

Taken by the owner on 2026-09-07; the reasoning is in `00_OVERVIEW.md` § *The decisions, as taken*.

| # | Decision | Consequence for execution |
|---|---|---|
| 1 | Two LibKa0s tags | `M1-LK-04` cuts v1.26.0, `M1-LK-15` cuts v1.27.0 |
| 2 | Amend fifteen standards sections | Group B runs in full |
| 3 | **M2 waits for M1** | Milestones run strictly serially, M1 → M2 → M3 → M4 → M5 |
| 4 | Do all seven unmapped findings | `M2-24` … `M2-27`, `M5-09`, `M5-10` are in scope |
| 5 | **This cycle does not ship** | No addon version bump anywhere. Upstream tags and the standards rollup only |

Answered separately when execution was authorised: run all five milestones without stopping; cut and
push both tags; push the per-repo branches but do **not** merge them; do both GitHub issue items
(`M2-23`, `M5-07`) with the writes throttled.

---

## Standing caveats — read before believing any "done"

**The tags are cut on the branch, not on master.** `04_EXECUTION_PLAN.md` § *Branches, merge order*
warns that a tag on an unmerged branch is a tag on a commit that may not survive review, and it is
right. The owner chose branch-and-review over merge, and M3/M4 cannot re-vendor without real tags, so
the deviation is deliberate. The commit shas survive an ordinary merge, so this is sound **unless
review causes that branch to be rewritten** — in which case both tags must be re-cut and all nine
addons re-vendored.

**No WoW client is available to this execution.** Eighteen items carry an in-client check. Their code
lands and their smoke step is written into the owning addon's `docs/smoke-tests.md` in the same commit,
per the plan's standing rule, and they are recorded here as *implemented, in-client verification
pending*. **No smoke step in this cycle has been performed.** Roughly seventy-five minutes of client
time across six sessions is outstanding at the end; `06_SMOKE_TESTS.md` is the checklist.

**`M4-03` is smoke-only** — the five-addon load-order sweep. There is nothing to implement and it
cannot be verified here.

**`M5-10` ships no code.** `WHATGROUP-R-06` conditions its own fix on a session-6 observation
confirming `C_SpellBook.IsSpellKnown` and the bare global are both present and agreeing. That
observation cannot be made without a client, so shipping the rung would be inventing the evidence the
finding asks for. It stays filed.

---

## Milestone state

Legend: ☐ not started · ◐ in flight · ☑ complete · ⚠ complete with items not done

| M | What | Items | State | Notes |
|---|---|---|---|---|
| **M1** | Upstream — LibKa0s, WowAddonStandards, wow-addon | 38 | ⚠ complete | 38/38 landed, both tags cut. Four caveats below |
| **M2** | The defects that need no upstream anything | 27 | ◐ in flight | Nine addon lanes, then the cross-repo items, then `M2-23` |
| **M3** | Adoption of v1.26.0 | 5 | ☐ | KickCD first — that one re-vendor repairs every consumer in a live session |
| **M4** | Adoption of v1.27.0, and the compliance the rulings unblock | 26 | ☐ | `M4-04` … `M4-08` land one repo at a time, five attribution points |
| **M5** | The record and documentation tail | 10 | ☐ | Last, because everything above rewrites what it records |

**106 work items total.** Per-item outcomes are appended below as each milestone completes.

### Workflow runs

Each milestone is one Workflow invocation. A run can be resumed with its script path and run id —
completed agents replay from cache, so a resume re-runs only what was in flight.

| M | Run id | Script |
|---|---|---|
| M1 | `wf_14ba5d9d-4ee` | `ka0s-m1-upstream-wf_14ba5d9d-4ee.js` |
| M2 | `wf_2b86e5d7-1f3` | `ka0s-m2-reachable-defects-wf_2b86e5d7-1f3.js` |

Scripts live under
`~/.claude/projects/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/cc7de98b-2023-425e-a118-ad5b0ca212ee/workflows/scripts/`,
and each run's per-agent return values are in `journal.jsonl` beside its transcript. **Resume only
works inside the session that started the run.** From a fresh session, establish state with the ground
truth commands above and start a new workflow over what is missing — the item ids make that safe,
because an item that already has a commit is visible and can be skipped.

---

## Item outcomes

### M1 — complete, 38/38, with four caveats

39 agents, no failures. 16 commits in LibKa0s, 16 in WowAddonStandards, 7 in wow-addon (Group C picked
up `M1-STD-03`'s plugin ripple as a seventh). `M1-LK-00` is the one item with no commit, by design.

**Measured after the fact, by a pass that re-ran everything rather than trusting the item reports:**

| | |
|---|---|
| LibKa0s `luacheck .` | 0 warnings / 0 errors, **49 files** — was 18 of 49 before `M1-LK-12` |
| LibKa0s `lua tests/run.lua` | **791** passed / 0 failed — was 764 |
| LibKa0s complexity | 0 warnings, max CCN 14, 14376 NLOC |
| `git ls-files --eol` stragglers | exactly the two `attr eol=lf` shell scripts, as intended |
| Tags | `v1.26.0` → b2079450, `v1.27.0` → b635fd46, both annotated, **neither pushed** |
| The standard | v2.39.0, all fifteen amendments verified present in their section files |

**The Critical fix was proved, not asserted.** The verifier replayed commit `e05237c` in a scratch
tree: 762 passed / 6 failed, with the four composer cases failing on *"expected table, got function"*.
At `6defec2` the same cases pass and `grep -c 'function() return O.LSMValues'` goes 3 → 0 with
`COMPOSE_MINOR` 2 → 3. Gate-before-fix happened rather than being claimed.

**Caveat 1 — the exit criteria contain a clause M1 cannot satisfy.** Clause 1's second half asks that
`diff -r LibKa0s <Addon>/libs/LibKa0s` be byte-empty for the first consumer re-vendored. No consumer is
re-vendored until `M3-01`; all nine still stamp v1.25.0. This is a defect in the criterion's placement,
not in the work — it belongs to M3's exit, and it is why the exit pass returned `false`.

**Caveat 2 — v1.26.0's release bundle was measured on a dirty tree.** Bundle
`docs/automated-tests/20260907-201015/` names `"release": "1.26.0"` and sits inside the tagged tree, so
the criterion's letter holds, but its manifest records `git.sha b903483` (the tag's *parent*),
`git.dirty true` and `addonVersion 1.25.0`. v1.27.0's bundle is clean by contrast. **Not fixed here:**
the bundle commit precedes the tag, so correcting it means rewriting a branch that already carries two
tags, and the payload itself is correct. If review re-cuts v1.26.0 for any reason, fix it then —
`M1-LK-14` rewrote `docs/releasing.md` to make a dirty release tree refuse, so this cannot recur.

**Caveat 3 — one commit deliberately leaves LibKa0s red.** `e05237c` (`M1-LK-01`) is the four composer
cases without their fix, which is what `04_EXECUTION_PLAN.md` orders and what `05_TRACEABILITY.md` § 7c
sanctions. `02_UPSTREAM_CHANGES.md` and `03_SPEC.md` invariant 1 both say the gate and its fix land in
one commit. The conflict is now in the shipped history rather than only in the documents. **The remedy,
if you want one, is to squash `e05237c` into `6defec2`** — the content is right either way. Left alone
because a bisector reading "red for exactly one commit, and here is why" is better served than one
reading a squashed commit that hides the ordering the whole item exists to demonstrate.

**Caveat 4 — five reported figures did not reproduce.** None changes a conclusion; all are recorded so
they are not later read as drift. `M1-WA-03` claimed `grep -ci 'blocker'` → 8, actual 6 at its own
commit and at HEAD. `M1-STD-16` claimed three plugin files still describe three tables; all three
already carried the four-table register, swept by `M1-STD-03`'s ripple. `M1-STD-01`'s 308/329 file
census measures 310/331 today — LibKa0s's own later M1 work added the difference, so the figure was
right when taken and is stale now. `M1-WA-01`'s grep reads 12 at HEAD against 11 at its commit, for the
same reason. `M1-LK-00`'s byte-empty vendored diff is no longer reproducible because five later items
changed the library — **so the collection's "check that has never passed" still has not been
demonstrated passing anywhere, and will not be until `M3-01`.**
