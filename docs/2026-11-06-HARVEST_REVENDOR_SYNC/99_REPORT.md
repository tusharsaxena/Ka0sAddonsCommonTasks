# 2026-11-06 — Report: harvest, re-vendor, sync docs, finalize

The record of the run planned in `00_PLAN.md`. Every claim was measured on 2026-11-06.

## Outfitter Reborn joins the suite

The owner ruled Outfitter Reborn (folder `OutfitterReborn/`, GitHub `tusharsaxena/Outfitter`) a full member
of the Ka0s collection. It was already on the roster (`WowAddonStandards/standards/ADDONS.md`, commit
`c21052b`); the harvest read it for the first time, and it took part in every step below. Memory records the
ruling and retires the earlier hands-off note.

## 1. The harvest — WowAddonStandards v2.101.0 → v2.102.2

Bundle: `WowAddonStandards/harvests/2026-11-06/` (01–06). Four read-only sweeps (quirks; audit and review
corpus; code patterns; LibKa0s drift and tooling) plus the issue store of all eighteen repos. Eight
proposals; the owner accepted seven and declined one:

| Proposal | Decision |
|---|---|
| client-quirks section (new) — 21 independently rediscovered client behaviors, build-stamped; contested ones as open probes | accepted |
| documentation-§5/§6 — an addon's own citations by symbol, own counts as rule/date/list (reading B) | accepted |
| packaging — `media/screenshots` ignored where it exists | accepted |
| documentation-§3 — the shape of `docs/superpowers/` for new files | accepted |
| events-frames-taint-§2 — `InCombatLockdown()` is false inside `PLAYER_REGEN_DISABLED` (erratum) | accepted |
| library-stack-§7 — LibKa0s v1.89.0 (21 majors, 67 files, IconBrowser, Toast stack, `W.ContextMenu`) and a `libka0s-counts` check | accepted |
| open-evolutions — votes and four new entries | accepted |
| a spill target for the `## Skins` hub section | **declined** (reading B: stays in the hub) |

**Three releases, because the first re-vendor tested the second.** v2.102.0 (the harvest) was merged and
pushed before the re-vendor, since `/dev-copilot:wow-revendor-standards` reads the standard from GitHub
`master`. The re-vendor's dry run then found three defects in what the harvest wrote, all fixed upstream
before any addon carried them:

- client-quirks-§1 first said "cite, do not restate", against the re-vendor command's vendored-block design
  (fixed on the branch before v2.102.0 was merged; recorded in `harvests/2026-11-06/06_OUTCOME.md`).
- **v2.102.1** — *catalogue* is on localization-§5's British list and would have turned every addon's prose
  gate red inside markers nobody may edit; the section's header link resolved nowhere inside an addon.
- **v2.102.2** — the section showed the literal `BEGIN/END VENDORED` comments in an example, so every vendored
  copy would have carried a second end marker for the next re-vendor to cut at.

The two gaps behind those defects are not closed: `scripts/check-standard.sh` does not scan for British
spellings, and nothing tests that a vendored section is safe to vendor. Both are candidates for the next
harvest.

## 2. Re-vendor the standard (v2.102.2) — all seventeen addons

Dry-run plans per repo, one owner approval for the whole plan, then apply. Every addon's
`docs/midnight-quirks.md` carries the client-quirks block stamped `quirks catalog v2.102.2`, with exactly one
end marker, above its own section; the file was created in six (DpsRace, LibKa0sSkinTester, PanelMaster,
PremadeGroupsFilterExtension, PrettyChat, QuickComms). The Documentation-map row for the file reads "always".
Nothing was pruned: every overlap with the catalog kept addon-specific detail. One `REVENDOR-STD:` commit per
addon.

## 3. Sync docs — twenty-one repos

The seventeen addons, WowAddonStandards (no change; `check-standard.sh` 8/8), LibKa0s (README and CLAUDE.md
name IconBrowser and twenty-one majors), dev-copilot (CLAUDE.md payload size and Tier 2 list) and this
workspace. In the addons, roughly 800 own-code `path:line` citations in live docs became `path` plus a symbol
or heading, and many of them had already drifted off their targets; stale counts were corrected or dated.

**Owner rulings on the held items (one batch):**

- About fifteen comment-only and doc-only corrections — applied.
- AuraMaster (`tests/test_docs.lua`, 164 citations) and MultiMeters (`tests/test_texture_paths.lua`, 2) keep
  test-pinned `path:line` citations; each records a documentation-§6 row in `## Documented deviations`,
  because the test already removes the rot the rule targets. **Evidence for the next harvest:** a citation a
  test verifies may deserve to be an allowed form.
- The skin notice's combat retry (`core/SkinSetup.lua`, `NS.MaybeShowSkinNotice`) is **not** a combat path;
  the performance-§12 exemptions in BankLedger, LootHistory, PrettyChat and WhatGroup stand, each sweep now
  lists the retry with the ruling.
- OutfitterReborn's README names all 36 verbs; its quirks doc and `core/Secrets.lua` comment now match
  events-frames-taint-§8; `DEPENDENCIES.md` adds `curl`; three Blizzard citations pinned to wow-ui-source
  `297d7aa`.
- This workspace gains a root `DEPENDENCIES.md`.
- **The library-absent Slash stub's em-dash help row** (slash-commands-§1) — approved for DropWatcher and
  PremadeGroupsFilterExtension; a sweep of every addon found the same defect in PrettyChat, WhatGroup and
  LibKa0sSkinTester, fixed the same way. Five `FIX:` commits, each test-first. The harvest had counted two
  live instances; the real number was five, which is itself evidence for the kit gate recorded in
  open-evolutions (*Kit gates the audits keep asking for*).

## 4. Gates before finalize

Re-run on every branch head through `ka0s-bounded`, all clean trees:

| Repo | Tests | luacheck |
|---|---|---|
| AbsorbTracker | 1062 passed, 0 failed | 0/0 |
| AuraMaster | 2355 passed, 0 failed | 0/0 |
| BankLedger | 1657 passed, 0 failed | 0/0 |
| ConsumableMaster | 1403 passed, 0 failed | 0/0 |
| DpsRace | 1448 passed, 0 failed | 0/0 |
| DropWatcher | 2238 passed, 0 failed | 0/0 |
| KickCD | 1675 passed, 0 failed | 0/0 |
| LibKa0sSkinTester | 887 passed, 0 failed | 0/0 |
| LootHistory | 1979 passed, 0 failed | 0/0 |
| MultiMeters | 2585 passed, 0 failed | 0/0 |
| OutfitterReborn | 1536 passed, 0 failed | 0/0 |
| PanelMaster | 1194 passed, 0 failed | 0/0 |
| PartyFrameEnhanced | 647 passed, 0 failed | 0/0 |
| PremadeGroupsFilterExtension | 545 passed, 0 failed | 0/0 |
| PrettyChat | 691 passed, 0 failed | 0/0 |
| QuickComms | 1706 passed, 0 failed | 0/0 |
| WhatGroup | 1100 passed, 0 failed | 0/0 |
| LibKa0s | 4197 passed, 0 failed | 0/0 |

Each addon skips one case and LibKa0s three, as before this run. During sync-docs LibKa0s showed one
unexplained failure in one of five runs; every later run was clean. Worth watching.

## 5. Finalize

Merged `--no-ff` into `master`, pushed and the feature branch deleted, in dependency order. No tags, no
version bumps, no LibKa0s release. The heads are recorded in the merge commits of each repo.

## Owed, not done here

- **In-game:** nothing in this run changes what a player sees except the five slash stubs' help rows, which
  appear only when LibKa0s is absent (a degraded install). No smoke check is owed.
- **Audits:** DpsRace and LibKa0sSkinTester have never been audited; thirteen repos were last audited at
  v2.76.1.
- **Issue store:** LibKa0sSkinTester and Outfitter carry no `state:` labels — `/dev-copilot:issue-audit` has
  never run there.
- **Kit:** fourteen addons are on kit revision 50 (revision 51 fixes a flake) until their next
  `/dev-copilot:wow-revendor-libka0s`.
- **Open probes** in client-quirks-§6: `string.format` on a secret, the restriction event's second argument,
  `SetAllPoints` on a secure button at load (OutfitterReborn smoke O11).
