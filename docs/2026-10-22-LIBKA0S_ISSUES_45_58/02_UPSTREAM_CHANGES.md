# 02 — Upstream changes (M1)

Three repos change before any addon is touched. Item ids refer to `04_EXECUTION_PLAN.md`; each item's full end state is in
`plan-data/items.json`.

## WowAddonStandards: v2.86.0 (one version for the whole run)

| Item | Section | Change |
|---|---|---|
| WS-01 | STANDARDS.md, CHANGELOG.md, stamps; library-stack-§7 | Opens v2.86.0. **Narrowed `__` clause**: a `__` member documented as internal or as a test seam, with zero roster consumers, may be removed in a minor. Documented `__` members that consumers call remain contract. The testkit is not reached by it. AUDIT.md: a stub mirroring a removed `__` member is a finding. |
| WS-02 | launcher-§6 (new), §2; layout-§1; slash-commands-§7 | **The Show window key binding (MUST).** A `CLICK <Folder>Toggle<Window>:LeftButton` binding on a hidden, named, non-secure button, routed to the same handler as the Show window entry and the toggle verb. No default key. Header and label are localized. The by-hold refusal stays a SHOULD. A new anti-pattern. Playbook and context-pack ripple. |
| WS-03 | preview-mode; standalone-windows; anti-patterns | **A test mode says so on the display (MUST)**: visible, localized and present in every layout. It covers the explicit Test mode only, and a minimised window with its header hidden is carved out. `W.TestStrip` is the SHOULD form for a window with a filter bar. A new anti-pattern. |
| WS-04 | documentation-§1 item 12 | Icon-set credits. A README `## Credits` is a MUST when any `gi:` (Game-icons, CC BY 3.0) icon ships, and a SHOULD for each MIT set (Open Iconic, Phosphor) it ships. Credit only the sets actually shipped after pruning. |
| WS-05 | automated-tests-§3; AUTOMATED_TESTS.md | A crashed or bounded lizard run is not a complexity pass (a clarification). `crashedFiles` appears as a parenthetical. The hazard row's facts are corrected. |
| WS-06 | library-stack-§2, §7 | The LibCustomGlow-1.0 row. Module table rows for `LibKa0s-Glow-1.0`, `Item.BonusIDsFromLink`, `W.SearchBox` and `W.TestStrip`. Glow is "required of none". |
| WS-07 | preview-mode | **The in-game simulator.** A simulator is a MAY to ship and a MUST to build on `LibKa0s-Sim-1.0`. It MUST route simulated reads through NS.Compat, MUST refuse while stood down, in test mode, in combat, in an instance or in a group, and MUST NOT send or write saved data. It is slash-only. |
| WS-08 | library-stack-§7 | The `LibKa0s-Sim-1.0` row, the StepPanel row (public or Sim-private, per LK-11), and the major and file counts. |
| WS-09 | library-stack-§7; anti-patterns #95 | The closed library-drawn icon set: **close, copy, clear, info**. TestStrip and step-panel art is host-passed. |
| WS-10 | open-evolutions; library-stack-§7 | The recorded rejections for #46–#58, each with its bar and re-check trigger. |
| WS-11 | all | Landing pass: the final changelog entry, the date re-stamp and a read-for-meaning. |

## LibKa0s: v1.75.0 (local annotated tag, pushed only at finalize)

| Item | Change | Version |
|---|---|---|
| (merged) | Kit 40 icon-subset gate and `tools/prune-icons.lua` | Kit 40 |
| LK-01 | `O.__releaseChrome` no longer exported (#45) | OptionsTabs 9 |
| LK-02 | Stale "install missing the art" comments corrected | Core 11, DebugLog 20, OptionsIdList +1 |
| LK-03..05 | Kit 41: #45's kit seams removed. A lizard crash or bound is `fail` with zeroed figures, and a separate `crashed` bucket comes from a per-file retry that names the file. The runner script stays ≤ 1450 lines, or the suite moves to a sourced helper. | Kit 41 |
| LK-06, LK-07 | `W.SearchBox(parent, width, opts{hint, icon, onChange})` and `W.TestStrip(parent, opts{text, icon})` with `TEST_STRIP.HEIGHT`. Each shares one file-local skin. | Widgets 13 |
| LK-08 | `Item.BonusIDsFromLink(link)` | Item 3 |
| LK-09 | New major `LibKa0s-Glow-1.0`: `Start(frame, style, knobs, key, frameLevel)` / `Stop(frame, style, key)`, with LCG soft-resolved on every call | Glow 1 |
| LK-10, LK-11 | `W.StepPanel` in WidgetsStepPanel.lua, then a spike rebuilding PerfPanel on it. If PerfPanel's suite passes unedited, the panel stays public. Otherwise it is reverted into a Sim-private renderer. | WidgetsStepPanel 1 / PerfPanel +1 (outcome A) |
| LK-12..16 | New major `LibKa0s-Sim-1.0`: `NewSeam` (Sim.lua), the session `New` / Start / Stop / Fire / After / listeners, SimTimeline.lua (steps, gate, delay, internal RunTo), the verbs `RunVerb`, and SimPanel.lua (a docked step panel, picker and controls, with session-only position) | Sim 1, SimTimeline 1, SimPanel 1 |
| LK-17, LK-18 | Sim contract tests (two-copy isolation, the reference degradation stub with parity, a DropWatcher-shaped mini host) and the API document with host contract H1–H10 | — |
| LK-19 | DebugLogDiagnostics lists Glow and Sim | DebugLogDiagnostics 3 |
| LK-25 | Rejections recorded in the API documents of the majors each candidate would have joined | docs only |
| LK-20..22 | Repo-wide ripple (README, CLAUDE.md, DEPENDENCIES, the adoption prompt), releasing.md (icon-subset re-vendor steps, attribution), and the release: green gate, release run with ANALYSIS.md, **local** tag | v1.75.0 |
| LK-23, LK-24 (M4) | Consumer census restamped after adoption; GitHub closure of #45–#58 after merge | — |

## dev-copilot: 2.4.0

| Item | Change |
|---|---|
| DC-01 | `wow-revendor-libka0s`: the `LibKa0s icons:` declaration (derive, confirm, split a run-on provenance line), the tag's own `tools/prune-icons.lua`, the whole-catalog test blocker, icon-set README credits, dead `__` stub mirrors, and a refresh after a moved local tag |
| DC-02 | The kit-41 `crashedFiles` bucket in bump-version, wow-automated-tests, the WoW review, the audit and finalize |
| DC-03 | The audit, sync-docs and new-addon learn the icon declaration, the pruned `media/icons/`, icon-set credits and launcher-§6 |
| DC-04 | Release 2.4.0, no tag. **The owner then updates and reloads the installed plugin before M2.** |
