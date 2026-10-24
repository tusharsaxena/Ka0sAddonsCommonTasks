# 2026-10-24 — Keybindings (015), settings layout (020) and frame strata (030)

A collection-wide run over the 15 roster addons and the three upstreams. The owner's brief, rulings and the lead's
calls are in [`inputs/OWNER_SCOPE.md`](inputs/OWNER_SCOPE.md).

| Item | What | Where it lands |
|---|---|---|
| 015 | Each windowed addon (7) gets its own category in Options → Keybindings, named for the addon, with logical labels, and a General > Keybindings tab that reads and writes the same bindings | standard launcher-§6 + options-ui-§20; LibKa0s `OptionsKeybinds.lua` (`O.KeybindingsTab`); `<PFX>-KB` per windowed addon |
| 020 | Settings layout: regroup, move and relabel, with no setting changes, to cut page and tab switching | owner-gated: [`preview.html`](preview.html), published at https://claude.ai/artifact/3iN2yVj3u9rrV9ndLB5PU8; M3 is planned after the review |
| 030 | One frame-layering model; each addon's strata and levels made consistent | new standard section `frame-layering`; small LibKa0s fixes; `<PFX>-ZS` per addon; dev-copilot review check |

## Reading order

1. `inputs/OWNER_SCOPE.md`: the brief and the rulings.
2. `inputs/KEYBINDINGS_RESEARCH.md`: how the client builds the Keybindings page, and the tab's design.
3. `inputs/layout/<Addon>.md`, `inputs/strata/<Addon>.md`: per-addon analysis, each independently reviewed.
4. `inputs/LAYOUT_CROSS_ADDON.md`, `inputs/STRATA_MODEL.md`: the collection conventions and the strata model.
5. `04_EXECUTION_PLAN.md`: milestones and gates. `items.tsv` / `plan-data/items.json`: the manifest.
6. `RESUME.md`: picking the run up from any point. `06_SMOKE_TESTS.md`: the owner's in-client checks.

## Versions

WowAddonStandards v2.87.0 → **v2.88.0**; LibKa0s v1.76.0 → **v1.77.0** (local tag until finalize); dev-copilot
2.5.0 → **2.6.0**. No addon version bumps.

## Branch

`feat/2026-10-24-keybinds-layout-strata` in every repo the run touches.
