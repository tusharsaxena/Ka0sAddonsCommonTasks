# LibKa0s issues #45–#58 — overview

**Dated 2026-10-22. Branch `feat/2026-10-22-libka0s-issues-45-58` in every repo the run touches.**

## 1. What this run does

It addresses every open LibKa0s issue from #45 to #58. It changes LibKa0s, WowAddonStandards and dev-copilot, re-vendors
LibKa0s v1.75.0 into all fourteen roster addons (Quick Comms included), and adopts what shipped in each addon that
consumes it. It also builds two new in-game simulators, in Loot History and Bank Ledger, on the new `LibKa0s-Sim-1.0`.

The owner set a very high bar for what goes into LibKa0s. Every candidate was censused across the collection and judged
against library-stack-§7's three promotion bars, and an independent skeptic tried to keep each one out. What
survived, plus the owner's own calls, is below.

## 2. The outcome in one table

| Ships in LibKa0s v1.75.0 | Standard v2.86.0 | Rejected (recorded, closed) |
|---|---|---|
| Kit 40 icon-subset gate + `tools/prune-icons.lua` (#57) | launcher-§6: the Show window key binding (MUST, #58) | Chat sender, tooltip reader, loot parser, restriction tracker (#49) |
| `O.__releaseChrome` and two kit seams removed (#45) | preview-mode: a test mode says so on the display (MUST, #48) | Grid composer (#50) |
| Kit 41: lizard crash ≠ pass; `crashed` bucket (#46, #47) | documentation-§1: icon-set credits (MUST for Game-icons, #55) | The rest of the item read (#51) |
| Stale "missing art" comments corrected (#57) | automated-tests-§3: a crashed run is not a pass (#46) | Flat checkbox, published flat skin (#52) |
| `W.SearchBox` (#52) and `W.TestStrip` (#48) | library-stack-§2: LibCustomGlow row | IconStyle, glow lifecycle, defaults, `O.GlowGroup` (#56) |
| `W.StepPanel`, public or Sim-private (#53) | library-stack-§7: narrowed `__` clause, closed icon set, module table, recorded rejections | A key-binding helper (#58) |
| `LibKa0s-Sim-1.0` (#54) | preview-mode: the simulator contract (MAY ship, MUST build on Sim-1.0) | |
| `LibKa0s-Glow-1.0` (#56) | | |
| `Item.BonusIDsFromLink` (#51) | | |

Details and evidence: `01_CONSOLIDATED_FINDINGS.md`. Binding decisions: `inputs/OWNER_SCOPE.md`.

## 3. Reading order

| File | What it holds |
|---|---|
| `inputs/OWNER_SCOPE.md` | Every decision, owner and lead, binding on the executors |
| `01_CONSOLIDATED_FINDINGS.md` | Verdict per issue and candidate, with the census and the bar each one met or failed |
| `02_UPSTREAM_CHANGES.md` | What changes in WowAddonStandards, LibKa0s and dev-copilot |
| `03_SPEC.md` | The end state, per repo |
| `04_EXECUTION_PLAN.md` | The 123 items by milestone (generated from `plan-data/items.json`, which holds each item's full spec) |
| `05_TRACEABILITY.md` | Issue → items |
| `06_SMOKE_TESTS.md` | The owner's in-client checks, all `owed` |
| `RESUME.md`, `resume-state.sh`, `checkpoints.tsv`, `exceptions.tsv` | Resumable execution |
| `plan-data/PLAN_REVIEW_RESOLUTIONS.md` | How each plan-critic finding was disposed |
| `inputs/` | Issue texts, the analysis workflow (25 agents), the design workflow (11 agents), designs and simulator requirements |

## 4. How it runs

- **M1, upstream.** WowAddonStandards v2.86.0 (WS-01..11), LibKa0s v1.75.0 (LK-01..22, LK-25) ending in a **local**
  annotated tag, and dev-copilot 2.4.0 (DC-01..04). The checkpoint pushes the three feature branches, but not the tag.
  The owner then updates and reloads the installed dev-copilot plugin to 2.4.0, because M2 uses its re-vendor procedure.
- **M2, re-vendor.** One `<PFX>-RV` item per addon. Each copies both payloads from the local tag, writes the
  `LibKa0s icons:` declaration, prunes, fixes the v1.71→v1.75 adoption blockers (the Options stub `Drawer`, kit 39 stand-down
  cases, icon tests) and the README credits. Items run in parallel across repos. The checkpoint pushes every branch.
- **M3, adoption.** It runs serially within a repo and in parallel across repos. DropWatcher's move onto Sim-1.0 (DW-01..05) is the
  contract proof and goes first. The Loot History (LH-06..14) and Bank Ledger (BL-05..13) simulators build on it. If
  either exposes a gap in Sim-1.0, the fix is additive in LibKa0s, the local tag moves, and the affected addons re-vendor
  (OWNER_SCOPE B). Every addon also gets a standards-reference refresh. The checkpoint pushes every branch.
- **M4, finalize.** CT-01 writes the run records. **CT-02 runs only on the owner's merge go-ahead**: `--no-ff` merges in
  dependency order, then the push of tag v1.75.0, then deletion of every run branch, stash and worktree. The GitHub
  closures come after the merge.

Each item is implemented test-first, committed as `<ID>: …`, reviewed independently (the result recorded as a
`refs/notes/ka0s-review` note), and given one fix round. Git is the only state: `./resume-state.sh`.

## 5. Owner touchpoints

1. After M1, update and reload the dev-copilot plugin to 2.4.0.
2. In-client smoke runs (`06_SMOKE_TESTS.md`), at any point after M3. Bank Ledger's warband deposit event sequence
   (BL smoke) feeds back into its simulator's driver data.
3. The merge go-ahead, which triggers CT-02.
