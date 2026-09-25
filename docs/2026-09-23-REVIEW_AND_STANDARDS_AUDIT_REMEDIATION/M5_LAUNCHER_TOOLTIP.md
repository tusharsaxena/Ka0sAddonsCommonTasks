# M5 — the always-on launcher status tooltip (owner request, 2026-09-24 smoke feedback)

Added after the in-client smoke pass, **before** the merge/push cycle, on the owner's ruling. Same
branch everywhere (`feat/2026-09-23-review-audit-remediation`), same loop (implement test-first →
commit `<ID>: …` → independent review with a `refs/notes/ka0s-review` note → one fix round). Git is the
state; `resume-state.sh` does not know these ids, so resume from this file and `git log`.

## Owner rulings

- The minimap button **always** shows a tooltip, **including while the addon is disabled**, with the
  addon's status: **Enabled**, and **Locked** / **Test mode** where the addon has that state.
- **Left-click keeps launcher-§2's three rungs** (a) primary window, (b) preview switch, (c) settings
  (ADDONS.md's column is unchanged); while disabled, rungs (a)/(b) still refuse with the one line.
  **Right-click always opens settings.**
- It lands before the merge.

## The tooltip (drawn by the library, identical shape in all eleven addons)

```
<label>  v<version>                      (version optional)
Enabled: Yes|No                          (green/red; always)
Locked: Yes|No                           (only if the addon passes isLocked)
Test mode: On|Off                        (only if the addon passes isTestMode)
<the addon's own extra lines>            (optional onTooltipShow, appended; never a title or hints)
Left-click: <leftClickLabel>             (rung a/b; while disabled: "Left-click: disabled — /<slash> enable")
Left-click: Open settings                (rung c)
Right-click: Open settings
```

All strings through `lib.STRINGS` / the descriptor's `L`. Status is read on every show, never cached.

## Items

| ID | Repo | What |
|---|---|---|
| WS-10 | WowAddonStandards | v2.66.0: launcher-§1 — the tooltip is a MUST, drawn by `LibKa0s-Launcher-1.0` from the descriptor (status lines for the states the addon has, the host's lines after, the click hints last), shown while disabled; launcher-§2 cross-reference for the disabled hint; changelog entry, version ripple, context pack, AUDIT.md check, anti-pattern if a host draws its own title/hints. |
| LK-36 | LibKa0s | v1.57.0: Launcher minor 3 — new optional descriptor fields `isLocked`, `isTestMode`, `leftClickLabel`, `version`, `slash` (for the disabled hint; or derive the hint from `disabledLine`); the library always sets `OnTooltipShow` and draws the block; the host's `onTooltipShow` is appended. Tests (every combination, disabled state, rung c, host lines appended once), docs/api, CHANGELOG, releasing ripple, **local** tag `v1.57.0` (never pushed without the owner). Kit revision only if the kit changes. |
| M5-AT, M5-AM, M5-BL, M5-CM, M5-KC, M5-LH, M5-MM, M5-PM, M5-PF, M5-PC, M5-WG | each addon | Re-vendor LibKa0s v1.57.0 whole (libs/LibKa0s + tests/_kit, provenance line, the revendor bundle as the RV items did); in `core/LauncherSetup.lua` pass `isLocked` / `isTestMode` where the addon has the state, `leftClickLabel` for its rung, `version`; move any existing tooltip content to extra lines only; tests; docs (settings-panel.md launcher row, ARCHITECTURE.md). |
| M5 checkpoint | all touched | batteries green, push branches + notes, a checkpoints.tsv line. |

After M5, the owner re-runs smoke #1 (minimap buttons) in-client.
