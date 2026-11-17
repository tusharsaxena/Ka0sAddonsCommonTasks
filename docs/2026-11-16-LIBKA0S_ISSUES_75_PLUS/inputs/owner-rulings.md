# Owner rulings, 2026-11-16

These rulings were made in the session that opened this run. They are quoted or recorded as the owner gave them.

## Scope

- Build every open LibKa0s issue numbered #75 or higher. The scope is **all Ka0s addons**, not only the ones ported to WoW Forever.
- The run has three phases: [1] build the changes in LibKa0s, [2] re-vendor LibKa0s into every Ka0s addon and fix whatever breaks, [3] adopt the new LibKa0s features in every addon. **Phase [3] is planned but not executed in this run**, because tokens are short this week.
- **Do NOT build #83 (FTUX).** "We'll do that in a later run."
- **CombatTrail:** "add it to ADDONS.md". It is in scope for every phase.
- **DropWatcher's live feature branch** (`feat/2026-11-16-loose-ends`, from another session): "Those are minor changes which should not affect the plan."

## Decisions (asked upfront, answered 2026-11-16)

| # | Question | Ruling |
|---|---|---|
| Q1 | #80 (bar widget) and #81 (launcher extra entries) have one consumer, Skill Master | **Build both now.** Record the one-consumer ruling (library-stack-§7 bar 1) in their API docs and in the CHANGELOG. |
| Q2 | #82: seven of nine skins fail hot-vs-rest or hot-vs-heading | **Fix all failing skins and add a kit contrast check.** Forever's hot becomes white. High Contrast gets a named exemption on hot-vs-heading. #84's stripe is fixed the same way. |
| Q3 | #86 order of the header marks | **extras · settings · close** (left to right). Settings opens the owning addon's settings, found through its launcher. |
| Q4 | #87 home for the sample characters | **A standard rule plus LibKa0s data** (on LibKa0s-Sim). |
| Q5 | Smoke the new tag before the sweep? | **Sweep straight through.** Re-vendor all 19 without waiting, and smoke everything at the end. |
| Q6 | Standard rules for #79 and the others | **Write the rules in this run.** Each one is owed when the addon adopts the feature, not at re-vendor. |

## Standing guidelines for this run (pasted by the owner)

- Ask questions upfront. After that, decide yourself and ask only when absolutely necessary.
- Write a resumable, checkpointed plan. Work on a branch and commit incrementally.
- Push to origin after major milestones. Do not merge without the owner's go-ahead.
- After everything is merged, delete every branch, stash and worktree the run created.
- Use ultracode (dynamic workflows).
