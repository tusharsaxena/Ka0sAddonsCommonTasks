# Suite sweep 2026-09-22/23: the report

Everything in the plan of record (`00_PLAN.md`) is done and **shipped**. `/wow-addon:finalize` merged
the sweep branch in all 15 repos on 2026-09-23 and pushed it, with LibKa0s `v1.55.0` on origin. The
owner's 20 in-game smoke checks all passed.

**Added after the sweep, at the owner's request:** AbsorbTracker's unlocked bars now carry the
`LibKa0s-Widgets-1.0` `DragHandle` strip (`6416d11`, `7c43ab4`). The survey found every other
unlock mode already on the strip (ConsumableMaster, KickCD, AuraMaster) or on a shape that does not
need it (MultiMeters' title bars, PanelMaster's outline). PartyFrameEnhanced was surveyed and left
as it is, by the owner's choice.

## What shipped

| Repo | What changed |
|---|---|
| **WowAddonStandards** | **v2.63.0**: the harvest, 16 accepted proposals, and commencement clauses citing kit revision 25. **v2.64.0**: the ripple of the three new majors, recounted from the tree. It adds named degradation-stub shapes and records three open questions without ruling on them. No addon gains an obligation. |
| **LibKa0s** | **v1.55.0**, tagged at `6f9c5e0` and pushed. It carries **test-kit revision 25** (the layout-§1 cap census gate, the `.gitattributes` body gate, suite declaration keyed by (basename, directory), and the commit SHA in the automated-test record) and three new majors: **`LibKa0s-Compat-1.0`** (9 members), **`LibKa0s-Bus-1.0`** (a live stand-down record plus a strict `Catalog`) and **`LibKa0s-Schema-1.0`** (the portable settings runtime). The release record is `20260923-144526`: clean tree, lint, tests and complexity pass, 0 functions above CCN 15. |
| **11 addons** | The standard re-vendored (Phase 4). LibKa0s v1.55.0 re-vendored, with each measured checklist row discharged (Phase 5). The majors adopted per the design specs, with a characterization test before each change (Phase 6). Re-vendor bundles are in `docs/revendor/2026-09-23-v1.55.0/`. |
| **wow-addon** | Standard reference refreshed, and its gate sentences name their checkpoints. |

## Adoption matrix

See `00_PLAN.md` → *Adoption matrix*. **20 adoptions and 15 declines**, and every decline is a GitHub
issue with one `state:` and one `severity:` label. `will-not-do` issues are closed and `triaged`
issues are open.

## Final battery (Phase 7, `wf_2f3cdd7d-47f`, then the minors pass `wf_d7ad1a5d-97e`)

| Repo | Tests | Lint | CCN > 15 |
|---|---|---|---|
| AbsorbTracker | 692 / 0 | 0/0 | 0 |
| AuraMaster | 1296 / 0 | 0/0 | **2, both pre-existing on master** (`Cat.SyncUserCategories` 25, `renderCategories` 16) |
| BankLedger | 1017 / 0 | 0/0 | 0 |
| ConsumableMaster | 998 / 0 | 0/0 | 0 |
| KickCD | 1050 / 0 | 0/0 | 0 |
| LootHistory | 858 / 0 | 0/0 | 0 |
| MultiMeters | 1948 / 0 | 0/0 | 0 |
| PanelMaster | 884 / 0 | 0/0 | 0 |
| PartyFrameEnhanced | 289 / 0 | 0/0 | 0 |
| PrettyChat | 438 / 0 | 0/0 | 0 |
| WhatGroup | 727 / 0 | 0/0 | 0 |
| LibKa0s | 1484 / 0 / 1 skip (the recorded prose decline) | 0/0 | 0 |

Every addon's `libs/LibKa0s/` hashes identically to `git archive v1.55.0 LibKa0s` (146 files).
The cross-collection pass found no same-session collision in SavedVariables, slash tokens, global
frame names or bus message names.

## What the verify passes caught that would otherwise have shipped

- **3a, kit revision 25:** six fix rounds, each closing one instance of *enforced here, unenforced
  beside it*. The worst was a path-spelling comparison that aborted the entire suite in the two
  repos that declare the kit the way the standard prescribes.
- **2b, standard v2.64.0:** a fix agent widened a no-copy prohibition, which would have made all
  eleven addons' Slash stubs non-compliant. The orchestrator narrowed it by hand.
- **3t, the tag:** the release run found 4 functions above CCN 15, all new in this release. They
  were split with differential fuzzing of old against new before the tag was cut.
- **Phase 6:** a degraded-load UNITS handler in AbsorbTracker re-registered events on a
  stood-down addon; BankLedger's Bus stub lacked `New`; PanelMaster's in-game check described
  behavior the code does not have.
- **Phase 7:** ten re-vendor bundles were bare-dated against audit-review-history's
  `<YYYY-MM-DD>-v<tag>` MUST. The orchestrator's brief had named the wrong path. They were renamed,
  and the 15 in-repo references and 14 issue bodies updated.

## Owed by the owner

1. ~~Merge and push~~: done 2026-09-23.
2. ~~In-game smoke tests~~: all 20 passed 2026-09-23, and so did AbsorbTracker's drag-handle strip
   check (`docs/smoke-tests.md` item 68).
3. **Before AuraMaster's next release:** its two pre-existing CCN > 15 functions block
   `/wow-addon:bump-version`.

## Left open, on purpose

- The 8 `state:triaged` declines (mostly Schema adoptions deferred as the spec permits), and
  AuraMaster #16–#19 (peel seams for its four over-cap files).
- The three questions `open-evolutions` records: the write-seam name, the panel live-refresh
  subscription, and the Core floor for runtime-critical majors.
- MultiMeters declares its catalog as `NS.Constants.MSG` rather than architecture-§4's `<NS>.MSG`.
  This predates the run; a future audit finding.
- Bare `§N` shorthand in some comments. The playbook does not rewrite that form.
- The addons' newest automated-test bundles are 30–127 commits behind HEAD. Bundles are written at
  release by `/wow-addon:bump-version`, which no addon ran here, since no version bumps were
  authorized.
