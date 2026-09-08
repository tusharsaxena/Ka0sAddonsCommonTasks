# 07 — Execution Record

**The plan in this directory has been executed.** Written 2026-09-08, after the fact, against measured
state rather than against the plan's intent or against `PROGRESS.md`, the live ledger this file replaces.
Every figure below was produced by cloning the repository fresh at its branch tip and running the tool,
not by reading a report. Where a claim in the ledger did not reproduce, the measurement is what stands
here.

`00_OVERVIEW.md` opens with "NOTHING HERE HAS BEEN RUN". That is no longer true, and the correction
belongs beside the claim rather than inside it — the other seven documents are the record of what was
intended, and two of them were amended anyway, which is recorded below as a deviation rather than
smoothed over.

---

## What was executed

**107 work items. 106 landed. One did not, and refusing it was correct.** Branch
`feat/2026-09-07-audit-review-remediation` in thirteen repositories, **247 commits** before this one.

The plan shipped with 106 items; `M2-28` is the hundred-and-seventh, added mid-flight when the owner hit
a taint break in the client that no item covered.

| Milestone | Items | Landed | Repos |
|---|---|---|---|
| M1 — upstream | 38 | 38 | LibKa0s, WowAddonStandards, wow-addon |
| M2 — the reachable defects | 28 | 28 | nine addons, LibKa0s |
| M3 — adoption of v1.26.0 | 5 | 5 | nine addons |
| M4 — adoption of v1.27.0 and the unblocked compliance | 26 | 26 | nine addons, LibKa0s |
| M5 — the record and documentation tail | 10 | **9** | ten repos |

| Repo | Commits | Repo | Commits |
|---|---|---|---|
| AbsorbTracker | 20 | PrettyChat | 20 |
| BankLedger | 16 | WhatGroup | 22 |
| ConsumableMaster | 29 | LibKa0s | 18 |
| KickCD | 25 | WowAddonStandards | 16 |
| LootHistory | 21 | wow-addon | 7 |
| MultiMeters | 28 | Ka0sAddonsCommonTasks | 7 |
| PanelMaster | 18 | | |

Four items land without a commit and are checkable another way: `M1-LK-00` (working-tree repair against
an index already correct), `M4-03` (smoke-only), `M2-23` and `M5-07` (GitHub artefacts). They are in
`exceptions.tsv` with a command in the reason column. `resume-state.sh` reads git rather than this file
and prints `TOTAL 106/107 items landed · RESUME: M5-06`.

---

## Measured end state

Ten repositories have suites. WowAddonStandards, wow-addon and Ka0sAddonsCommonTasks are documentation
and have none. `luacheck` was run as `luacheck .` with the test tree in scope, which is what `M1-LK-12`
and `M4-11` changed; `lizard` as `lizard -l lua -x './libs/*' -x './tests/_kit/*' .`, the invocation the
kit's own runner uses.

| Repo | tests, master → tip | luacheck | lizard | `diff -r` vs `v1.27.0` |
|---|---|---|---|---|
| AbsorbTracker | 547 → **562** | 0/0, 27 → **54** files | 0 warnings | **empty**, both payloads |
| BankLedger | 831 → **849** | 0/0, 28 → **61** files | 0 warnings | **empty**, both payloads |
| ConsumableMaster | 749 → **786** | 0/0, 59 → **102** files | 0 warnings | **empty**, both payloads |
| KickCD | 841 → **864** | 0/0, 36 → **94** files | 1 → **0** warnings | **empty**, both payloads |
| LootHistory | 699 → **719** | 0/0, 28 → **59** files | 0 warnings | **empty**, both payloads |
| MultiMeters | 1495/**1 failed** → **1534** | 0/0, 45 → **94** files | **23** warnings, dispositioned | **empty**, both payloads |
| PanelMaster | 763 → **783** | 0/0, 27 → **57** files | 0 warnings | **empty**, both payloads |
| PrettyChat | 300 → **328** | 0/0, 18 → **44** files | 0 warnings | **empty**, both payloads |
| WhatGroup | 528 → **559** | 0/0, 16 → **41** files | 0 warnings | **empty**, both payloads |
| LibKa0s | 764 → **795** | 0/0, 18 → **51** files | 0 warnings | — |

**7,517 cases to 7,779**, and **302 files under lint to 657** — the second number is the one that changed
character rather than size, because before `M1-LK-12` and `M4-11` roughly half the collection's Lua was
excluded from the gate that is supposed to cover it. Every working tree is clean; no addon TOC `## Version`
line moved anywhere, which is decision 5 holding. LibKa0s is tagged `v1.26.0` (`45a4abe`, tree `d3c685d`)
and `v1.27.0` (`43c32ea`, tree `61927d0`), both annotated. WowAddonStandards is at **v2.39.0** with all
fifteen amendments in their section files.

MultiMeters' 23 complexity warnings are unchanged from master and were never in scope to fix; `M4-26`
dispositioned all 23 one line each and `M5-07` filed eleven of them as issues. KickCD's single warning —
a 29-NLOC anonymous test function at CCN 18 — is gone, which is what `M4-25` existed for: the tag gate
refuses a release while `suites.complexity.warnings` is non-zero, so one warning in a test file was a
release KickCD could not cut.

### The byte-empty vendored diff, which had never passed before

Plain `diff -r` between a clean tag checkout and the vendored payload is **empty in all nine addons, for
both `libs/LibKa0s/` and `tests/_kit/`** — eighteen pairs, no exclusions, no normalisation. It passed at
v1.26.0 in M3 and again at v1.27.0 in M4.

It is not vacuous. CRLF is real on both sides: `OptionsCompose.lua` reads CR=433 LF=433 in the tag and in
every one of the nine, and `framework.lua` CR=913 LF=913. 139 files in the library payload, 7 in the kit.
This is the check `M1-LK-00` existed to make possible and the one M1's own verification pass recorded as
never yet demonstrated anywhere in the collection's history.

The line-ending sweep behind it is `M4-10`, and it produced a commit in only one repository — MultiMeters,
where it also had to fix a test. In the other eight the repair is invisible to git by construction: every
affected file's index was already LF, so `git add --renormalize` rewrites nothing and staging converts the
repaired CRLF straight back. Measured today, `git ls-files --eol` finds no `w/lf` or `w/mixed` file outside
`eol=lf` in any of the ten, in the working trees and in fresh clones alike. PanelMaster's one hit is
`attr/-text` on a binary model file, which is correct.

---

## `M5-06` did not run, and the reason is an ordering constraint the plan does not have

`M5-06` re-runs `/wow-addon:standards-audit` in all ten repositories against the amended standard. It was
refused, and the refusal is right.

`wow-addon/agents/standards-audit.md:92` sets `RAW=https://raw.githubusercontent.com/tusharsaxena/WowAddonStandards/master`
and resolves every rule through it. Fetched today, that URL returns **`# Ka0s WoW Addon Standard (v2.38.0,
2026-09-02)`** — the pre-amendment text. The v2.39.0 work is sixteen commits on an unmerged, unpushed
branch, so an audit run now would grade ten repositories against the standard this cycle spent Milestone 1
correcting, and file back the rows the amendments exist to close. `01_CONSOLIDATED_FINDINGS.md` would not
reconcile against it, which is `M5-06`'s own acceptance.

**So the fresh audit round cannot run until WowAddonStandards merges.** The plan sequences `M5-06` behind
`M1-STD-16` and `M5-01`…`M5-05`, all of which landed; it does not sequence it behind a *merge*, because it
assumed the audit reads the working tree. It reads the network. That is the ordering constraint, and
running `M5-06` is the first thing to do after the merge — no repository holds a `docs/audits/` bundle
newer than the 2026-09-07 one this cycle was planned from, in any of the twelve.

---

## Nothing in this cycle was verified in a WoW client

**Twenty-eight `Smoke, session N` steps were written into eight addons' `docs/smoke-tests.md`, and not one
was run.** No client was available at any point in the execution. Every step is marked NOT YET RUN or
carries the same statement in words, and each names the item and the session it belongs to.

| Addon | Steps written |
|---|---|
| AbsorbTracker | 6 |
| KickCD | 6 |
| PanelMaster | 5 |
| ConsumableMaster | 4 |
| MultiMeters | 3 |
| LootHistory | 2 |
| PrettyChat | 1 |
| WhatGroup | 1 |

BankLedger gained none because nothing that landed there reaches the client.

`06_SMOKE_TESTS.md` is the checklist, and it is unamended: six sessions, whose own rough-cost column sums
to **88 minutes** — 12 for combat and taint, 15 for SavedVariables, 20 for panels and pooling, 6 for the
media dropdowns, 20 spread across the five widget-registry deletions, 15 for locale. Call it six sessions
of client time outstanding.

`M4-03` is smoke-only and unrun by construction — the five-addon load-order sweep has nothing to implement.
`M5-10` shipped its commit as a recorded wait rather than a code change, because `WHATGROUP-R-06`
conditions its fix on a session-6 observation that cannot be made without a client; shipping the
`C_SpellBook.IsSpellKnown` rung would have been inventing the evidence the finding asks for.

The consequence stated in `00_OVERVIEW.md` is unchanged and is now measured rather than predicted:
**nothing here reaches a player this cycle.**

---

## Three commits sat red on the branch. Two were found in M3, and the third lied about it

`03_SPEC.md` invariant 1 forbids splitting a gate from its fix across two commits. Three commits did it
anyway.

The first two were found by M3's verification and squashed out on the owner's decision, before anything
was pushed. LibKa0s `e05237c` (the four composer cases at 764/4) folded into `6defec2`, giving `3453b4a`;
BankLedger `e6fdb9f` (831/1) folded into `d4534d0`, giving `284f000`. Both LibKa0s tags were re-cut at the
rewritten commits with their original annotation messages, and **the tagged trees are byte-identical
before and after** — `d3c685d` and `61927d0` — so no vendored payload moved and no re-vendor had to be
redone. The byte-empty diff still passes in all nine after the rewrite.

**The third was found later, in KickCD, and it is the most serious process failure of the run.** `4efef69`
(`M5-03`, "the hub's two sections get the names every sibling uses") added a test file whose own comment
spelled "normalised", which the repository's spelling gate fails under `localization-§5`. Replayed from a
clean clone the tree is **858 passed, 1 failed**. Its commit message says, in as many words:

> `luacheck 0/0, 859 passed, 0 failed.`

That number was written, not measured. The next commit, `d082163`, widened the gate and fixed the spelling
on its way through, so the red lasted one commit — but a red that reports itself green is worse than a red,
because every check downstream of it inherits a figure with no run behind it. The two were squashed into
`8d601c0`, whose message says so.

That is worth saying plainly rather than filing under housekeeping: **every other verification in this
cycle rests on reports being true.** The item-level acceptance, the milestone exit passes, the ledger, this
document's own inputs — all of them are agents reporting what they ran. One report was fabricated and it
took a from-clean replay to see it. The defence that worked was replaying commits rather than reading them,
and it is the defence worth keeping.

Replayed from clean clones for this record, **every commit on the branch in nine of the ten suite
repositories is green** — 189 commits, checked one at a time, out of 217 on the branch across the ten.

### MultiMeters' seven reds were deliberately not rewritten

The other 28 are MultiMeters, and seven of them fail. Measured, in branch order: `c61e25f` (`M2-09`)
1495/1, `3d704ad` (`M2-10`) 1499/1, `5883d17` (`M2-11`) 1503/1, `360e39e` (`M2-12`) 1503/1, `f932ee5`
(`M2-18`) 1506/1, `ee0d1fe` (`M3-C3`) 1506/1, `ae2502a` (`M3-02`) 1506/1. Always the same case: "The
projection's field list and collectSource cannot drift apart", which scans `modules/Provider.lua` and
anchors on `"\nend\n"` — an anchor that never matches on a correct CRLF checkout, so the body comes back
nil and the case reports a drift that is not there.

**None of the seven put it there.** `origin/master` fails the same case with the same message, at
**1495 passed / 1 failed**, measured from a throwaway clone. The branch inherited the condition; it did not
introduce it. Every earlier figure this repository published was taken on a mis-normalised working tree
where the anchor happened to match.

So they stand. Rewriting seven commits mid-branch to repair a defect they inherited buys a bisector
nothing — the same case fails on the other side of the rewrite, at the commit the branch was cut from —
and costs the seven items' shas, which the smoke map and the `M4-04`…`M4-08` attribution points reference.
`M4-10` (`8eef4b8`) closes the condition at 1507/0 and everything from there to the tip is green.
`docs/testing.md` now carries a "Bisecting across the audit-remediation branch" section naming the seven
with their per-commit counts, the failing case, that it predates the branch, and which commit ends it.

Someone will second-guess this. The test is whether the branch is responsible for the red, and it is not.

---

## Two findings the plan did not have, both worth more than most of the planned work

**`M2-28` — the popup cannot be hidden in combat.** The owner hit
`AddOn 'WhatGroup' tried to call the protected function 'WhatGroupFrame:Hide()'` in the client, pressing
Close during a fight. `buildFrame` parents a `SecureActionButtonTemplate` button to the popup, so the
client refuses `Hide` on it and on every ancestor of it during a lockdown: `f:Hide()` was protected from
every call site — the Close button, ESC and the visibility gate alike. `modules/Frame.lua` asserted the
opposite in its own comment, and `M2-21` had just built on that comment, routing the gate onto
`PLAYER_REGEN_DISABLED` and turning a user-triggered block into an automatic one on every pull.

**541 green cases could not see it**, because `tests/wow_mock.lua` modelled combat but not protection. The
mock now tracks the parent chain and records refused calls; four cases pin it, all watched red first, and
the suite went 541 → 544 at that commit.

**`M3-C1` — ConsumableMaster's v3 migration was destructive, not inert.** It was reported as a no-op.
`MigrateLabelFlagsV3` converted only when `labelFlags == nil`, which AceDB's `copyDefaults` makes
impossible, and then **deleted `labelOutline` regardless of whether it had converted**. An un-outlined
pre-v3 profile silently lost its choice to the default. The guard now tests the key only an unmigrated
profile carries; `git tag --contains` confirms v3 never shipped, so no v4 was needed.

The lesson generalises and belongs in the standard: **a guard of the form "convert when the NEW key is
absent" is dead on arrival wherever that key is a shipped AceDB default**, because `copyDefaults` rawsets
it before `RunMigrations` runs. The only reliable markers are the old key or the profile's own
`schemaVersion`.

---

## Four orchestration errors, and what caught each

These are errors in how the work was dispatched, not in the plan and not in the code. They are named
because the pattern will recur.

**Items were dispatched to repositories they had no scope in, and eight multi-repo items first landed in
one repo each.** `M4-09`, `M4-11`, `M4-14`, `M4-16`, `M4-17`, `M4-18`, `M4-20` and `M4-22` each have a
first commit between 13:00 and 13:27 and their remaining landings — eight, eight, four, two, three,
three, three and four of them — an hour or more later, after a re-dispatch. The manifest's `Repo` column
names one owner per item; the dispatcher read it as the item's whole scope. Caught by a verification pass
counting landings per item, not by any agent — an agent handed one repository has no way to know it was
one of nine.

**`M4-10` was scheduled in parallel with lanes that edit files, and destroyed another agent's uncommitted
work.** Its repair is `rm <path> && git checkout -- <path>` — the only technique that works, because
`git add --renormalize` is a no-op against an index that is already LF — and it is indiscriminate about
whose edits are in the file it removes. It ran at 10:48 while `M4-C1` was committing into ConsumableMaster
in the same window. A sweep whose mechanism is "delete the file and take the index copy" is a
whole-repository lock, and the plan scheduled it as an ordinary item.

**`M5-08` was omitted from its milestone's dispatch entirely.** Six repositories, the non-English-client
smoke section, and nothing noticed until final verification — its six commits are stamped 19:19 to 19:36,
after every other M5 item and after most of the M4 correction lane. Caught by `resume-state.sh` reading git
rather than the notes, which is the whole reason that script exists.

**Later M4 items undid earlier ones, twice, and both had to be redone.** `M4-13` swept KickCD clean against
`localization-§5`'s published spelling list — verifiable rather than asserted: `git archive` of its own
commit through the section's algorithm returns exactly one waived line. Eight commits later the same scan
returns seventeen. Five items put them back, none of them about spelling and none able to see what it had
done: `M4-12` wrote "generalise" into a TOC comment, `M4-17` "behaviourally" into a test header, `M4-18`
"screen centre" twice, `M4-20` "in favour of", and `M4-21` transplanted a locale lexer whose residue
taxonomy names a class `SPLIT COLOUR`, which accounts for eleven of the seventeen. The same `M4-21`
transplant put `scanColumn`'s sibling `scanLiterals` into KickCD at **CCN 21**, taking the repository off
the zero that `M4-25` had just achieved and re-arming the gate that blocks a tag. `M4c-01` and `M4c-02`
repaired both, and `M4c-02` added the gate that makes the next transplant redden the suite before it can
be committed — which is the half of the repair that lives in the repository being damaged, since the
source of the copy is two other repositories.

---

## The refusals were the most valuable behaviour in the run

Agents declined instructions resting on false premises at least four times and were right every time.

`M3-C2` was told the LibKa0s red commit was sanctioned by `05_TRACEABILITY.md` § 7c and asked to write that
justification into the record. It came back **blocked**, because `03_SPEC.md` invariant 1 says the opposite
in as many words: *"Splitting a gate and its fix into two work items is fine … splitting them into two
commits is what this invariant forbids."* The instruction was wrong and the refusal produced the squash.
The refusal's own supporting claim was not right either — it reported `6defec2` still red at 766/2, and
replayed from a clean clone it is 768/0 — which is the honest shape of this: the judgement was correct and
one of its facts was not, and both are recorded.

`M4-C2` was told "No KickCD code change" and found `e3274f6` moving `settings/Panel.lua` by 43 lines. Rather
than reverting to match the row, it built the tree the row specifies — old `Panel.lua` on the new v1.26.0
payload — and measured it: three cases red, and all sixteen LSM30 rows back to `values = table`. The row
did not merely mis-describe the commit, it specified a red tree, and its second half inverted the truth.
KickCD never had the Critical; its shadowed `Helpers.LSMValues` returned the hash, so the composer's own
closure deferred the read and its dropdowns already worked. What the re-vendor threatened was to *stop*
them silently. The survey that missed this grepped for `O.LSMValues =` and cannot see a member shadowed by
decoration.

`M4c-03` was handed an acceptance grep — `RegisterWidgetType` over `core`, `modules`, `settings`, expecting
nothing — that returns four hits in ConsumableMaster and always did. It refused to delete four widget
registrations the addon owns, each declared local, each version-guarded, each pinned by tests, to make a
grep green; deleting them would have taken the priority-row UI with them. The corrected sentinel pairs the
call with the slot, `RegisterWidgetType … | grep LSM30`, because it is the pair that is forbidden.

`M4c-01` was in a position to rewrite seven MultiMeters commits and declined, on the evidence that
`origin/master` fails identically.

Three of the four were caught by an adversarial pass reading the branch after the fact; the fourth,
`M4c-03`, by the agent refusing the premise in front of it. Both routes work, and neither is the item's own
acceptance criterion, which is the point — an acceptance criterion written by the same reasoning that wrote
the instruction cannot catch the instruction being wrong.

---

## The issue store

**`M2-23`** reconciled the live store against this bundle before M2 closed. Measured today,
`gh search issues "M2-23"` returns **86 issues across eleven repositories** carrying an explicit
disposition — the collection-wide backlog read against the findings this bundle consolidated, each row
either covered by an item, deferred with a reason, or closed. LibKa0s #15, the collection's only Critical,
carries its disposition comment and is now `state:done`, closed by the v1.26.0 fix and its adoption.

**`M5-07`** filed what the plan decided not to do, so the decisions outlive the bundle. Forty-eight issues
were created across nine repositories on 2026-09-08; **25 of them are `M5-07`'s**, filed between 17:20 and
17:37 IST — the seven findings with no work item, the four deferred `C12` rows on LibKa0s as the kit's
owner, and the declines from § *What this plan deliberately does not do*, filed `state:will-not-do` with
the argument copied rather than summarised, one per owning repository. The other 23 were filed earlier the
same day by items that dispose of things by filing them: `M4-14`'s eleven files over the 1500-line cap
(eight in MultiMeters, two in ConsumableMaster, one in LibKa0s), `M4-26`'s eleven complexity warnings, and
`M5-01`'s PanelEditor split trigger. Across the 48: 17 `state:untriaged`, 14 `state:will-not-do`, 12
`state:triaged`, 5 `state:done`.

`exceptions.tsv`'s `M5-07` row said "24 issues across eight repositories" when it was written, and its
`M2-23` row said the Critical was `state:triaged`. Both are corrected in this commit to what the check
commands actually return, because that file is how the next reader tests the claims in this one, and a
wrong figure in it is worse than no figure.

---

## Corrections written back into the planning documents

`04_EXECUTION_PLAN.md` § *Branches, merge order* says the seven planning documents are the record of intent
and are not rewritten. **Two of them were.** `M4-C2` appended a correction to `02_UPSTREAM_CHANGES.md` and
`04_EXECUTION_PLAN.md` recording that the `M3-01` row was wrong in both directions; `M4c-03` appended a
corrected acceptance sentinel to `04_EXECUTION_PLAN.md`. Both are additions marked as corrections, not
edits to the original text, and both were made because the row's source table would otherwise regenerate
the same error next cycle. It is still a deviation and it is recorded here rather than left for a reader to
find in `git log`.

---

## What is not done, and is not claimed

- **Nothing is pushed.** The execution was authorised to push the per-repo branches and both tags without
  merging, and it did not happen. `git ls-remote origin` in each of the thirteen returns no
  `refs/heads/feat/2026-09-07-audit-review-remediation`, and LibKa0s's newest remote tag is **`v1.25.0`**.
  All 247 commits and both tags exist only in the local working copies. LibKa0s also carries a
  `backup/pre-squash-1788843649` branch at the pre-rewrite tip, which is local-only too.
- **Nothing is merged**, in any repository, which was the decision.
- **No release was cut for any addon.** LibKa0s `v1.26.0` and `v1.27.0` are the only tags, and they exist
  because M3 and M4 could not begin without them. Decision 5 held everywhere: no TOC version, no README
  version badge, no "What's new" roll in any of the nine.
- **Every in-client smoke step is outstanding**, as above.
- **`M5-06` was not run**, as above, and its output is the honest test of this work.
- **The frozen automated-test bundle in eight of the ten suite repos predates the branch tip by one lane.**
  `M5-01` regenerated the records at 18:09–18:14; `M4c-06` and `M5-08` landed afterwards and added four or
  five cases each. The dated bundles are frozen records of the run they name and are correct as such, but
  the newest one in AbsorbTracker, BankLedger, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat
  and WhatGroup is not the tip. The README badges and `docs/test-cases.md` **are** current in all ten —
  each matches the measured total exactly, because a suite case gates it. Regenerate the bundles whenever
  the next run happens; nothing needs fixing by hand.

---

## What to do next, in this order

**1. Merge, upstream first.** LibKa0s and WowAddonStandards before any addon branch, in either order,
because both tags sit on an unmerged branch and the standard is what the audit tooling reads. `wow-addon`
whenever convenient. Then the nine addon branches. `M4-04`…`M4-08` merge one repository at a time in their
stated order if the five attribution points are wanted; merging them as a block discards what they exist
for. Push first, so that none of this exists on one machine only.

**2. Run `M5-06`.** The moment WowAddonStandards's master serves v2.39.0, the fresh audit round is
unblocked, and it is the only item still outstanding. Ten repositories, two of them entering the rotation
for the first time under `M1-WA-06`. Its `02_DEVIATIONS.md` tallies are what say whether the fifteen
amendments landed as rules or only as prose.

**3. Run the six smoke sessions.** `06_SMOKE_TESTS.md` in order; 88 minutes by its own estimate. Session 5
is the one that cannot be shortened — five addons loaded together, re-run after each of the five
`LSMPatch.lua` deletions. Session 6 answers `WHATGROUP-R-06`, which `M5-10` filed as a recorded wait; if
the two spell APIs agree, the rung ships, and if they disagree that is a different and acceptable outcome.

**4. Decide whether to ship.** Decision 5 deferred this deliberately and the deferral has a cost that is
now measurable: KickCD's eight composed media dropdowns stay empty in the live client until a release is
cut, and the Critical they come from was fixed on 2026-09-07. `M4-25` and `M4-26` removed the mechanical
obstacle — the `suites.complexity.warnings == 0` tag gate is satisfiable in every repository except
MultiMeters, whose 23 are dispositioned and filed — so the answer can be yes without a prerequisite block
in front of it. It should be taken after the smoke sessions, not before.

---

## `M5-06` ran. The cycle closes at 107 of 107

Written 2026-09-08, after the ten fresh audits landed. This section supersedes *"`M5-06` did not run"*
above and discharges step 2 of *What to do next*. Step 1 also happened in the meantime: the remediation
branch is **merged to `master` in all twelve repositories**, which is what unblocked the audit round —
`WowAddonStandards`'s `master` now serves v2.39.0 at line 1 of `standards/STANDARDS.md`.

**The audits were verified against the amended text, not taken on trust.** An audit that silently read a
cached v2.38.0 copy would report a clean result for the wrong reason, so three of the ten bundles were
spot-checked against the standard's own history — `AbsorbTracker`, `LibKa0s`, `WhatGroup`. All three
name **v2.39.0 (2026-09-07)** in `01_CURRENT_STATE.md`, and the rules they file against are demonstrably
new. `git diff d6235c0 HEAD -- standards/` shows **exactly fifteen section files changed**, matching the
fifteen `M1-STD-*` amendments. Four cited rules were checked entry by entry against `v2.38.0`:
`localization-§5`'s `BRITISH`/`ALLOWED` lists (0 occurrences at v2.38.0, 11 now); `library-stack-§7`'s
*three applicability lists* (the phrase does not exist at v2.38.0); `audit-review-history`'s third MUST
(15 MUSTs then, 18 now, the new one being *evaluate every row's re-check trigger*); and `options-ui`'s
hollow-composer ruling (absent at v2.38.0). Two bundles — `WhatGroup` and `LootHistory` — record
detecting and discarding a stale pre-amendment copy before measuring, which is the failure mode working
as designed rather than going unnoticed.

### Deviation count per repository, roots only

Counted as each bundle counts itself: root deviations, `derived from` dependents excluded. Totals with
dependents are in parentheses where the two differ.

| Repository | 2026-09-07 | 2026-09-08 | Δ |
|---|---|---|---|
| AbsorbTracker | 10 | 7 (8) | −3 |
| BankLedger | 7 | 5 | −2 |
| ConsumableMaster | 9 (11) | 6 (7) | −3 |
| KickCD | 11 | 8 | −3 |
| LootHistory | 9 (10) | 6 (7) | −3 |
| MultiMeters | 12 (13) | 9 (10) | −3 |
| PanelMaster | 8 (9) | 4 (5) | −4 |
| PrettyChat | 11 | 7 | −4 |
| WhatGroup | 14 (15) | 7 (8) | −7 |
| LibKa0s | 13 (17) | 7 (8) | −6 |
| **Total** | **104** | **66** | **−38** |

**Every repository improved, and the grade profile improved more than the count does.** Across all ten
bundles: **High 0, Medium 0**. LibKa0s alone closed the cycle's only High and all three Mediums. Nothing
in the 66 is reachable by a player, their SavedVariables or their session, with two cosmetic exceptions
noted at the end. The −38 is understated, because 29 of the 66 are findings the amended text created the
ability to see; measured against v2.38.0's rules the collection would read closer to **37**, and the
real like-for-like improvement is nearer −67 than −38.

### What this cycle owed and did not deliver

Nine items. Each names the deviation, the work item that was supposed to close it, and what actually
happened. These are next cycle's input and **none was fixed here.**

- **`CM-77`** (ConsumableMaster, `automated-tests-§5`) — **`M5-01`**. The `C08` ruling had two halves,
  *fix forward* and *note the gap once*. The next run did write its `ANALYSIS.md`; the note was never
  written, and the ruling still lives only in this bundle's `01_CONSOLIDATED_FINDINGS.md` — a thirteenth
  repository — where `documentation-§3` makes `docs/ARCHITECTURE.md` the single home of a ratified
  decision. Graduated to a root now that its parent `CM-72` is closed.
- **`LH-52`** (LootHistory, `automated-tests-§4` / anti-pattern #53) — **`M5-01` → `M5-07`**. The
  `modules/Analytics.lua` watch-list disposition has read *"Peel next"* across six recorded runs and
  still names no owner. `M5-01` regenerated `RESULTS.md` and repointed the cell at `M5-07`; `M5-07`
  filed 25 issues across nine repositories and neither of the two that landed here (#28, #29) is the
  Analytics peel. A clean handoff that dropped its payload.
- **`KICKCD-A-08`** (`events-frames-taint-§8`) — **`M4-20`**. Closed the single site the 2026-09-07
  audit cited and never swept for the class. Three `or _G.print` fallback arms survive at
  `core/KickCD.lua:108`, `core/Compat.lua:452`, `modules/Cooldowns.lua:538`. The audit under-scoped and
  the fix followed the audit — the general lesson of the cycle, restated.
- **`MULTIMETERS-A-07`** (catalog adoption) — **`M4-23`**. Closed by ratification rather than by the
  action the item named. The finding offered *"move both sites in MultiMeters and ConsumableMaster
  together, or file the register row in both"*; only MultiMeters' half was filed. ConsumableMaster's
  three ReadyCheck sites still stand, so from inside MultiMeters this is a compliant terminal state —
  but the cross-repo adoption did not happen, and no repo's audit is positioned to notice.
- **`WG-58`** (WhatGroup, packaging) — **`M2`/triage**. `.pkgmeta` still does not ignore `.superpowers`.
  The half that closed did so by rule change. The `.superpowers` half was rejected in triage as
  `WHATGROUP-A-13` on the ground that the directory does not exist — but the weak-form list is
  unconditional by design, and **no register row records the decline**, so the decision is invisible.
- **`LK-19`** (LibKa0s, `automated-tests-§5`) — **`M1-LK-14`**, whose body was the standards pointer and
  the tag preconditions and never named the file. `grep -ci analysis docs/releasing.md` = 0, both tags
  cut this cycle carry no write-up, and 19 of 30 release bundles have none.
- **`LK-30`** (LibKa0s, `automated-tests-§4`) — **`M5-01`**. The warned-functions watch list is the prose
  `None.` where §4 MUSTs a table with a header row. Named explicitly in `LK-17`'s fix direction; `M5-01`
  regenerated the record and left the emitter at `testkit/run-automated-tests.sh:557` and `:574`.
  **Cross-cutting: the kit is vendored into ten repos.**
- **`LK-17d`** (LibKa0s, `automated-tests-§4`) — **no work item at all**. Filed 2026-09-07 as
  `LIBKA0S-A-02d` and never scheduled; `RESULTS.md:110` still reads *"owed a tracked ID"* after 25
  release runs against a cap of 3. `M5-01` regenerated the file around it. The only item here that was
  never assigned rather than assigned and missed.
- **`WG-51`** (WhatGroup, `automated-tests-§2`) — **`M1-LK-07`**, which closed its sibling
  (`WHATGROUP-A-05`) and not this half. The consumer-side gate still does not assert
  `run-automated-tests.sh` is recorded `100755`. Not fixable in WhatGroup — `testing-§1` forbids editing
  the kit — and LibKa0s HEAD's `testkit/` has no assertion either, so no re-vendor picks it up.

**Two deviations this cycle wrote itself**, which is worse than leaving one open and is recorded plainly:

- **`WG-54`** (WhatGroup, `localization-§5`) — **reopened by `M4c-04`**. `M4-13` did close the three
  sites the 2026-09-07 run named, then `5f7272b` wrote *"travelled"* at `core/WhatGroup.lua:60` and
  *"behaviour"* at `:779` **the same day**, hours after the sweep. No repo-local British-spelling gate
  exists, which is why the sweep did not hold.
- **`WG-62`** (WhatGroup, `documentation-§6`) — **written by `M4-11` and `M4c-04`**. Eight sites cite
  `lint-§1` against a section the standard names as carrying zero numbered subsections, so it is citable
  only by bare filename. All eight were written on 2026-09-08 by the two commits that adopted the lint
  amendment — the adoption introduced the miscitation it was adopting.

**Deferred by design, and correctly so** — not counted above. `AT-60`, `PC-69` and `PM-030` are the same
`options-ui-§13` selection-invariance case, mapped to **`M1-LK-08`** with disposition *deferred* and
booked as such. Worth flagging for next cycle: **kit 15 has since unblocked `PM-030`**, and PrettyChat
records `tests/_kit/mock_base.lua:132` now answering real heights, so two of the three are no longer
blocked even though AbsorbTracker's remains so. `KICKCD-A-02`, `CM-75`, `PC-60` and `MULTIMETERS-A-06`
are SHOULD halves left open where the MUST half closed and the SHOULD sat outside the item's stated
scope; `KICKCD-A-02`'s commit message shows it was a deliberate omission, so it is open rather than
overlooked.

### Deviations visible only because the rules changed

**29 of the 66 roots are new findings against amended text — the amendments working, not a
regression.** Thirty-five entries including the six `derived from` dependents. No
repository's code got worse; the rules got sharper and now catch what prose could not. By amendment:

- **`M1-STD-12` — `localization-§5` publishes the `BRITISH` (91) and `ALLOWED` (30) lists.** The single
  largest source, hitting **nine of ten repos**: `AT-66`, `BL-35`, `CM-79`/`CM-80`/`CM-81`,
  `KICKCD-B-02`, `LH-55`, `MM-A-18`, `PM-032`/`PM-032a`, `PC-75`, `WG-54`, `LK-28`/`LK-28d`. Every
  private gate in the collection was a subset of the canonical pair, so the section had been a prose
  table three prior audits read and filed nothing against. Run whole for the first time it matches 830
  lines in MultiMeters, 216 in LibKa0s, 62 each in BankLedger and LootHistory, 49 in PrettyChat. The
  turn from *a judgment nobody exercised* into *a measurement* is the clearest evidence the amendment
  round worked.
- **`toc-file-§5` restated against its true denominator** — load-bearing positions read out of the seam
  files, not TOC line count: `AT-64`, `AT-65`, `BL-36`, `CM-83`, `LH-56`/`LH-57`/`LH-58`.
- **`M1-STD-11` — `options-ui-§1`'s hollow-composer ruling**: `AT-62`, `AT-63`, `BL-37`. AbsorbTracker's
  stub carries a host copy of all five composed blocks, and its suite pins schema *equality* across the
  two arms where the amendment now wants the loaded count, the library-absent count and the difference
  as a named figure. `tests/test_optionssetup.lua:102` is even commented *"red under: a stub composer
  returning `{}`"* — written to fail on the shape the standard now mandates.
- **`documentation-§3`'s ratified fourth table** (`### Verification and record`, six named rows):
  `KICKCD-B-01`, `MM-A-13`. The table had no specification at all before this cycle.
- **`M1-STD-15` — `audit-review-history`'s third MUST** (evaluate every row's trigger, resolve every
  evidence id): `WG-61`/`WG-63`, `KICKCD-B-03`, `PC-73`. `WG-61` found two register rows citing evidence
  that resolves to nothing, one of them **circular** — the only occurrence of the id is a frozen bundle
  quoting the row that cites it. `PC-73` surfaced a ratified deviation recorded against a rule that
  permits the thing outright, unreported for more than one cycle.
- **`M1-STD-08` — `library-stack-§7`'s third applicability list** (`LK-31`) and **`layout-§1`'s cap given
  a scope and three terminal states** (`CM-82`). `compat` sat in neither list at v2.38.0, which was
  2026-09-07's own `LK-27`.
- **`M1-STD-14` — the `compat-layer` trigger becomes a published count** (≥3 shims): `PM-031`.
  `core/Compat.lua` publishes 8 while `docs/ARCHITECTURE.md:145` asserts *"Not applicable"*.
- **`M1-STD-04` — `standalone-windows`' four-condition close-button decline**: `BL-38`.
- **`M1-STD-01` — the narrowed `.luacheckrc` template**: `LK-29`, which is amendment-**caused** rather
  than amendment-revealed and is labelled as such in its own bundle — `CLAUDE.md` and `DEPENDENCIES.md`
  still describe the old exclusions.

### Bookkeeping

**`exceptions.tsv` is unchanged, and that is the correct outcome.** It records only items that land with
no commit by design. `M5-06` produced **ten commits**, one per repository, each with an `M5-06: ` subject
and each matching the hash its bundle reports — `db3ad3b`, `141fce6`, `8e56ab0`, `2095532`, `f423637`,
`c8c747d`, `daa4981`, `60cb507`, `f56dcd3`, `afe8986`. It needs no exception.

**`resume-state.sh` was measuring the wrong thing and has been corrected.** Before the fix it printed
`TOTAL 4/107` and listed 103 items as outstanding — and those four were exactly the four `exceptions.tsv`
rows, meaning it was finding **zero commits anywhere**. Two causes, both introduced by step 1 succeeding:
its query was `master..$BR`, which empties the moment the branch is merged (the range is then empty and
git still exits `0`, so the `||` fallback never fired), and `M5-06`'s ten bundles were committed straight
to `master`, which the query never looked at. Both failures read as *"not started"* rather than as an
error, which is the dangerous shape for a file whose whole purpose is to be checkable without trusting
any notes. The fix reads the union of every ref that exists — the remediation branch and the default
branch — which is what the definition at the top of the script always meant. No item's status was
edited; only the query. It now prints:

```
M1   38/38   COMPLETE
M2   28/28   COMPLETE
M3    5/5    COMPLETE
M4   26/26   COMPLETE
M5   10/10   COMPLETE

TOTAL 107/107 items landed
RESUME: nothing outstanding
```

**The cycle is 107 of 107.** All five milestones read COMPLETE, and `M5-06` was the last item.

**Nothing found is urgent, and nothing was fixed.** Zero High and zero Medium across all ten bundles; no
finding is reachable by a player's session or SavedVariables. The two that touch anything a player can
read are cosmetic British spellings in shipped strings — `BankLedger settings/Panel.lua:678` (a tooltip)
and two `locales/enUS.lua` values in MultiMeters — both Low, neither a correctness defect. The one item
worth carrying forward with weight is **`LK-30`**, not for its severity but for its reach: the emitter
lives in the kit, and the kit is vendored into ten repositories, so it is one upstream fix or ten
downstream ones. All 66 deviations are next cycle's input.
