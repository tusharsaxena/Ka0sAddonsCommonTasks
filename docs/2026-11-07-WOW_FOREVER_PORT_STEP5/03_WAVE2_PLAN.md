# WoW Forever port, step 5, wave 2: PanelMaster, PrettyChat, PartyFrameEnhanced

The owner's instruction of 2026-11-08: "lets do it - go ahead and build them in this order: 1. PanelMaster
2. PrettyChat 3. PartyFrameENhanced". These are the classification's group 3 (`00_CLASSIFICATION.md`). Wave 1
(`01_WAVE1_PLAN.md`) is the pattern. Its follow-ups, the default skin per client (skinning-§2) and Forever's
two-word names (client-quirks-§5), now bind every port too.

## Branch

`feat/2026-11-08-forever-port-wave2` in PanelMaster, PrettyChat, PartyFrameEnhanced, WowAddonStandards (the roster
rows) and Ka0sAddonsCommonTasks (this bundle). Git is the state: an item is done when a commit whose subject
starts `<ID>: ` exists in its repo.

## Baseline (2026-11-08, before any change)

| Repo | retail | forever | luacheck | inventory |
|---|---|---|---|---|
| PanelMaster | 1197 passed, 0 failed, 1 skipped | same | 0 / 0 | stale (the known kit-53 drift) |
| PrettyChat | 694 passed, 0 failed, 1 skipped | same | 0 / 0 | stale |
| PartyFrameEnhanced | 650 passed, 0 failed, 1 skipped | same | 0 / 0 | stale |

All three vendor LibKa0s v1.93.0.

## Sources for what Forever has

Shallow clones in the session scratchpad, not in any repo:
- Gethe/wow-ui-source `forever`, head "1.60.1 (70862)", 2026-11-07, and `live`, "12.1.5 (70783)", 2026-11-04.
- Ketho/BlizzardInterfaceResources `forever`, "1.60.1 (70532)", and `live`, "12.1.5 (70448)", both 2026-10-22: the
  GlobalStrings and global frame names per client.

## What every port in this wave changes

1. **Re-vendor LibKa0s v1.94.0** (Skin minor 18, Compat minor 4) and roll the `CLAUDE.md` provenance line.
2. **The default skin per client** (skinning-§2): `NS.DEFAULT_SKIN = Skin:DefaultSkin()` in `core/SkinSetup.lua`,
   named by `defaults/Profile.lua` and by the stand-in fallbacks. The tests pin the default per kit profile.
3. **The port**, wave 1's seven items: the TOC's `## Interface: 120105, 16001`, the README's badge and opening
   line, DEPENDENCIES, the per-client feature table in `docs/ARCHITECTURE.md`, both kit profiles in the gate
   (`CLAUDE.md`, `docs/testing.md`), a WoW Forever section in `docs/smoke-tests.md`, and a regenerated
   `docs/test-cases.md`.
4. **Names** (client-quirks-§5): any place the addon reads a character name goes through
   `Compat.UnitCharacterName`, and a surface that shows a name is sized for the long form.

## Per addon

| ID | Repo | What, beyond the four above |
|---|---|---|
| W2-PM-01 | PanelMaster | The four strata reads (`modules/Unlock.lua`) read the panel's own stored strata, and fall back to `GetFrameStrata` only behind `IsSecret`. Its `core/Compat.lua` stops calling itself Retail-only |
| W2-PC-01 | PrettyChat | The format-string seed list per client (clients-§5): a Forever list built from Forever's GlobalStrings, picked once by `ClientKey()`. Chat senders are two words on Forever |
| W2-PF-01 | PartyFrameEnhanced | Edit Mode and Forever's unit frames against the Forever UI source; the name labels (`UnitName` first-name-only reads) through `UnitCharacterName`, sized for two words |
| W2-STD-01 | WowAddonStandards | The three roster rows go to `Retail · Forever`, each after its port |
| W2-REC | Ka0sAddonsCommonTasks | This plan, the smoke run sheet and the report |

If a port turns up something that is not minimal, it stops at that point and asks.

## Gates and what is not done

- Before each commit, both kit profiles and luacheck are green, through the bounded runner, and the inventory
  matches.
- Smoke on both clients is the owner's (`04_WAVE2_SMOKE.md`). Claude marks no check passed.
- The feature branches are pushed when the wave ends. Nothing is merged, tagged or version-bumped without the
  owner's go-ahead.
