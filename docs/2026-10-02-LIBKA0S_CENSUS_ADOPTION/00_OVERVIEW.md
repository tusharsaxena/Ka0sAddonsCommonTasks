# LibKa0s census adoption (2026-10-02)

The owner asked for the nine issues the LibKa0s v1.66.0 consumer census filed (GI-LK-13, LibKa0s#9) to be
fixed. Two settle library contracts and seven adopt a library surface in place of a host copy.

| Issue | Repo | What |
|---|---|---|
| LibKa0s#41 | LibKa0s | `Core.MakeResizable` has no lock gate |
| LibKa0s#42 | LibKa0s | The Options descriptor's `addonName` has no consumer, so IdList help marks draw the fallback glyph |
| AbsorbTracker#33 | AbsorbTracker | Adopt `Slash.SplitVerb`, `Slash.ProfileNames`, `Core.SECRET` |
| BankLedger#21 | BankLedger | Adopt `Core.MakeResizable` (two windows) |
| ConsumableMaster#44 | ConsumableMaster | Adopt `Slash.SplitVerb`, `FindCommand`, `CommandRows` |
| KickCD#36 | KickCD | Adopt the Slash vocabulary and `Core.SECRET`; drop the `LAYOUT` copies |
| LootHistory#33 | LootHistory | Adopt `Core.MakeResizable` (blocked on #41) |
| MultiMeters#58 | MultiMeters | Adopt `Core.MakeResizable` and `Core.SECRET` |
| PanelMaster#56 | PanelMaster | Adopt `O.PADDING_X` |

## Shape

LibKa0s v1.67.0 first (Core 10 for #41; Options 28 and OptionsIdList 3 for #42), with a standard edit that
#42's answer needs (v2.75.0). Then all eleven addons re-vendor v1.67.0 and pass `addonName` on their Options
descriptor, and the seven host adoptions land. Then the census is re-run so `CONSUMERS.md` records the new
consumers.

## Files

| File | What |
|---|---|
| `01_DESIGN.md` | The two library contracts and every decision taken on the owner's behalf |
| `02_EXECUTION_PLAN.md` | Milestones, the per-item recipe, checkpoints (frozen once execution starts) |
| `03_SMOKE_TESTS.md` | In-client checks for the owner |
| `items.tsv` | The manifest |
| `RESUME.md`, `resume-state.sh` | How a fresh session picks up; state computed from git |
| `checkpoints.tsv`, `exceptions.tsv` | Milestone evidence; items that land with no commit |
| `inputs/issue-bodies-2026-10-02.md` | The nine issue texts as filed |
| `plan-data/design-scout.json` | The design and scouting workflow's raw output (10 agents, read-only) |

## Rules for this run

- One branch everywhere: `feat/2026-10-02-libka0s-census-adoption`.
- Commit incrementally. Push the feature branches at each milestone checkpoint. No merge to `master`, no
  pushed tag, until the owner says so. (The owner's "push to master after major milestones, but do not merge"
  is read as "push the feature branches"; pushing `master` is a merge.)
- No addon version bump. LibKa0s v1.67.0 and standard v2.75.0 are versioned as their repos require; the
  LibKa0s tag stays local until finalize.
- Heavy runs go through `ka0s-bounded`. GitHub writes are throttled.
