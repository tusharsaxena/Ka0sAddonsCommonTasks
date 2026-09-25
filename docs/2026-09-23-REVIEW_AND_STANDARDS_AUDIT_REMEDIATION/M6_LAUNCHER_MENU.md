# M6 — launcher: left-click opens settings, right-click opens a context menu (owner request, 2026-09-24)

Supersedes M5's click behaviour (M5's tooltip stays; only its click-hint lines change). Before the merge.
Same branch and loop as M5. Resume from this file and `git log`.

## Owner rulings

- The tooltip text stays as M5 built it, except the click hints (below).
- **Left-click opens the settings panel**, on every addon. launcher-§2's three rungs and ADDONS.md's
  rung column are **retired** (replace the column with the addon's menu entries).
- **Right-click opens a context menu** listing only the toggles that addon has, in this order:
  **Enabled** (always), **Locked** (if the addon has a lock), **Test mode** (if it has one),
  **Show window** (if it has a primary window). Each is a checkbox showing the current state; clicking it
  toggles through the addon's own code path (the same handlers `/<slash> enable|disable|lock|unlock|test`
  and the window toggle use), so refusals, combat rules and messages are the addon's.
- **While disabled**, Enabled stays clickable; Locked / Test mode / Show window are shown **greyed out**
  with the note "enable the addon first" (features refuse while disabled, slash-commands-§7).
- It becomes an upstream standard and lives in LibKa0s, so every new addon inherits it.
- **Versions**: standard **v2.67.0**, LibKa0s **v1.58.0** (Launcher minor 4). The unpushed local tag
  v1.57.0 stays as history; v1.58.0 is also local-only until the owner pushes.

## The shapes

Tooltip (M5's, with new hints):
```
<label>  v<version>
Enabled: Yes|No
Locked: Yes|No            (if isLocked)
Test mode: On|Off         (if isTestMode)
<host lines>
Left-click: Open settings
Right-click: Options menu
```
Menu (the client's own context menu, `MenuUtil.CreateContextMenu` on 11.0+; title = label):
```
<label>
[x] Enabled
[ ] Locked          (greyed while disabled)
[ ] Test mode       (greyed while disabled)
[ ] Show window     (greyed while disabled)
```

## Items

| ID | Repo | What |
|---|---|---|
| WS-11 | WowAddonStandards | v2.67.0: launcher-§2 rewritten (left = settings; right = context menu with the entries above; greyed while disabled; host handlers own the effect); M5's tooltip hint lines updated in launcher-§1; ADDONS.md rung column replaced by a "menu entries" column; anti-pattern #81 and #89 updated (a host building its own menu or click routing); AUDIT.md launcher check; NEW_ADDON_CONTEXT.md / NEW_ADDON.md templates (new addons inherit it); slash-commands-§7 cross-reference; index blurb, changelog, version stamps. |
| LK-37 | LibKa0s | v1.58.0, Launcher minor 4: left-click → `openSettings`; right-click → context menu built from descriptor toggles `setEnabled(bool)` (with `isEnabled`), `toggleLock` (with `isLocked`), `toggleTestMode` (with `isTestMode`), `toggleWindow` (with `isWindowShown`); greyed-while-disabled; `onClick`/`leftClickLabel` retired (documented; ignored if passed); tooltip hints updated; strings in lib.STRINGS; a headless mock of the menu API and tests for every combination; docs/api version-4 doc, CHANGELOG, releasing ripple; LOCAL tag v1.58.0 on the item's last commit (never pushed). |
| M6-AT … M6-WG | each addon | Re-vendor v1.58.0 whole (libs/LibKa0s + tests/_kit, provenance, the revendor bundle as before); in core/LauncherSetup.lua pass the toggles the addon really has, wired to the SAME handlers its slash verbs use; drop onClick/leftClickLabel; tests through the mock; docs (settings-panel.md launcher row, README's minimap description, ARCHITECTURE.md, smoke-tests.md). |
| M6 checkpoint | all touched | batteries green, push branches + notes (no tags), checkpoints.tsv. |

After M6, the owner re-checks the minimap buttons in-client.
