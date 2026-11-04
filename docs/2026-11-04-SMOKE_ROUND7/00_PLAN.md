# Round 7: PGFE test mode, README skin command, Sim mode box state

Branch `feat/2026-11-04-smoke-round7` in every repo touched. Owner feedback and answers in `inputs/`. Round 6
(`docs/2026-11-03-SMOKE_ROUND6`) is merged; its other smoke checks passed. Outfitter is excluded (a separate agent owns
it, and that agent is working in WowAddonStandards on `feat/2026-11-03-outfitter-roster`, so this run edits the
standard in its own worktree, `../.worktrees/WowAddonStandards-r7`, never in that checkout).

## The lead's calls

1. **PGFE gets `/pgfe test`** (owner's answer). Session-only test mode: the attached panel shows on its own, centred,
   with the current filters; Apply is disabled while PGF's dialog is absent; nothing is saved; no change in combat
   lockdown beyond what the panel already permits. It goes through the write seam like every other addon's test mode:
   the verb, a *Test mode* box in Master controls (`testModePath`) and the launcher entry the standard asks for.
   The skin picker passes `spec.preview = { mode = "test", ... }`, so the eye appears and `/pgfe skin` with the panel
   hidden turns test mode on and the close puts it back. If PGF's dialog is open, the panel is already shown and
   nothing changes. The standard's no-preview list becomes empty (the clause stays for future addons).
2. **Sim mode box state** (owner: checked while the sim window is open and/or a sim runs, unchecked otherwise). The
   host's `isSimMode()` returns `simWindowShown or simRunning`. Ticking does what bare `/xx sim` does (opens the sim
   window), so the box stays ticked. Unticking stops a running sim and hides the sim window. The box and the launcher's
   Sim mode entry re-read on window show and hide as well as on sim start and stop. Prefer no LibKa0s code change: the
   pair `isSimMode`/`toggleSim` already carries the meaning, so R7-L1 is docs and tests unless the library genuinely
   cannot express it. If LibKa0s code must change, it is a new tag v1.86.0 and a re-vendor in all 16 addons
   (R7-REL/R7-RV), never a move of the pushed v1.85.0.
3. **README skin command.** Every addon's README Usage section names `/<slash> skin` and says what it does (opens the
   skin picker; preview on hover/selection, the eye's mode, Apply). One or two sentences, in the README's voice, no
   command table (sync-docs rule). The standard gains the rule in its documentation section.
4. Standard version: next minor after master's v2.99.0. The Outfitter branch holds v2.99.1; whoever merges second
   rebases the stamps and changelog.

## Milestones

- **M1 upstream:** R7-STD, R7-L1 (and R7-REL only if code changed).
- **M2 addons:** R7-RV (only if R7-REL), R7-SIM (7 sim addons), R7-PG (PGFE), R7-RD (16 READMEs), each reviewed.
- **M3 gate:** 06_SMOKE_TESTS.md, 99_REPORT.md, checkpoint, push branches. Then the owner smokes; merge on go-ahead;
  delete this run's branches, stashes and the standards worktree.
