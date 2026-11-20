# LibKa0s #94, #97, #99, #100 (2026-11-20)

Branch `feat/2026-11-20-libka0s-94-97-99-100` in every repo it touches. RangeMaster is in scope (owner, 2026-11-20:
every collection-wide pass includes it).

## Owner rulings (2026-11-20, upfront)

- **R-1, #97 gaps.** Fix every plain gap. Unclear rows (a color that may carry meaning, a look an addon may have
  chosen on purpose) go to the owner in one list mid-run (SD-RULE).
- **R-2, option defaults.** An addon option for a texture, font or color whose default is the addon's own value
  changes its default to follow the skin. A player who never set it moves to the skin's look; a stored pick stays.
- **R-3, #99.** When a drag strip's rect reads secret, its tooltip goes above the nearest ancestor whose rect reads.

## Milestones

- **M0.** SD-PLAN; SD-AUDIT, the frozen audit bundle `docs/2026-11-20-SKIN_DEFAULTS_AUDIT/` (one table per consumer:
  element, token, OK / GAP / OVERRIDE (owner) / UNCLEAR, evidence), read-only fan-out, every GAP adversarially checked;
  SD-RULE, the owner's calls on UNCLEAR rows.
- **M1, LibKa0s.** SD-LK-94 (footer lays out shown marks only), SD-LK-99 (readable-ancestor fallback), SD-LK-100
  (Callout onClose and onSettings), run alongside M0. Then SD-LK-97 (library gaps), SD-LK-GUARD (a test-kit check that
  a skinned surface draws the active skin's statusbar texture, through the probe skin of `test_skin_switch`),
  SD-LK-REL (v1.108.0, local tag). SD-STD: the standard records R-2 and the guard (skinning-§6/§9), and releases.
- **M2, every addon on ADDONS.md (19).** SD-RV-x (re-vendor v1.108.0 and the standard), SD-SK-x (the audit's GAP fixes
  for that addon and its guard declaration; an exception row where it has none), plus SD-CT-100 (call-out close and
  settings, deviation row removed), SD-AM-99 (fallback wired, known limitation removed) and SD-DW-94 (smoke check).
  Each item is built, independently reviewed, and gated on every client it ships.
- **CP-1.** Re-gate every repo, push the run branches with their review notes, write `SMOKE.md` and the execution
  record. Stop for the owner's smoke. Merge only on the go-ahead, then `/dev-copilot:finalize`, push the tags, close
  #94 #97 #99 #100, and delete the run's branches, stashes and worktrees.

State is git only: `plan-data/resume-state.sh`, `items.tsv`, `exceptions.tsv`, `checkpoints.tsv`. See `RESUME.md`.
