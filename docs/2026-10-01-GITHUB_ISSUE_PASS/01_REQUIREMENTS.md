# Consolidated requirements

One row per issue the owner actioned in column S. *Verdict* is the 2026-10-01 validation result (`02a_ISSUE_DESIGNS.md` has the evidence). *Items* are the `items.tsv` ids that satisfy the row.

| Issue | Owner action | Sev | Verdict | Requirement / acceptance | Items |
|---|---|---|---|---|---|
| AbsorbTracker#10 | Close - no longer an issue | high | owner close | Closed 2026-10-01 (state:done), owner: no longer an issue | — |
| KickCD#7 | Close - no longer an issue | high | owner close | Closed 2026-10-01 (state:done), owner: no longer reproduces; correction comment records the fix was never applied | — |
| AbsorbTracker#20 | Fix this now | medium | addressed | A test pins that a hidden Appearance page is not rebuilt by a mirror flip and rebuilds on next OnShow; doc sentence added | GI-AT-01 |
| BankLedger#2 | Fix this now | medium | not-addressed | Rows missing itemName/itemType get name, quality, type, subtype, link filled (nil fields only) after load; ≤40 ids per login; idempotent; one LedgerChanged | GI-BL-01 |
| LibKa0s#40 | Fix now | medium | not-addressed | Host L overrides reach every parse/format string (red test first); 2-arg ParseValue unchanged; ConsumableMaster#16 closed after re-vendor | GI-LK-03, GI-CM-01 |
| PanelMaster#15 | Fix now | medium | not-addressed | Frame level slider (C.MIN_PANEL_LEVEL..C.MAX_PANEL_LEVEL) under Frame strata; Registry clamps; Known-limitations entry removed | GI-PM-02 |
| PanelMaster#42 | Fix this now | medium | not-addressed | S.Installed deleted; assertions rewritten on S.Themes(); rendering.md trimmed; nil guard assertion | GI-PM-01 |
| PartyFrameEnhanced#3 | Fix this now | medium | not-addressed | Mid-combat roster change leaves target/pet frames beside the right member with no ADDON_ACTION_BLOCKED (in-client); offline: secure snippet and attribute sync tested against the mock | GI-PF-02 |
| WowAddonStandards#6 | Fix now | medium | partially-addressed | Kit 35 sighted complexity + parity; standard v2.74.0 documents the blind spots; every addon re-runs the sighted gate at ≤ 15; AuraMaster local scanner retired | GI-LK-10, GI-LK-11, GI-STD-01, GI-PLUG-01, GI-AT-RV, GI-AM-RV, GI-BL-RV, GI-CM-RV, GI-KC-RV, GI-LH-RV, GI-MM-RV, GI-PM-RV, GI-PF-RV, GI-PC-RV, GI-WG-RV, GI-AM-01, GI-BL-02, GI-CM-02, GI-KC-12, GI-LH-02, GI-MM-02 |
| AbsorbTracker#32 | Fix this now | low | blocked | Appearance strip renders via O.RenderTabbedSchema with minor-8 opts; AT-15 characterization cases stay green; host partition/TabStrip composition deleted | GI-LK-06, GI-AT-02 |
| KickCD#9 | Fix this now | low | not-addressed | Steady cooldown emits ~0 SPELL_STATE; curves/brighten/text driven by the ticker regardless of showCooldownText; swipe re-armed only on state change | GI-KC-10 |
| KickCD#10 | Fix this now | low | partially-addressed | fillRows renders through RenderGrid with no inter-row gap; reorder stride unchanged; row strip visually unchanged | GI-LK-05, GI-KC-11 |
| KickCD#24 | Fix this now | low | partially-addressed | Castbar.lua < 1000 lines; pure move, identical suite totals | GI-KC-04 |
| KickCD#25 | Fix this now | low | not-addressed | IconGrid.lua < 1000; pure move | GI-KC-01 |
| KickCD#26 | Fix this now | low | not-addressed | IconGrid_Render.lua < 1000; ticker in IconGrid_Ticker.lua | GI-KC-02 |
| KickCD#27 | Fix this now | low | not-addressed | wow_mock.lua < 1000 | GI-KC-03 |
| KickCD#28 | Fix this now | low | not-addressed | Spells.lua < 1000 | GI-KC-06 |
| KickCD#29 | Fix this now | low | not-addressed | Database.lua < 1000 | GI-KC-05 |
| KickCD#30 | Fix this now | low | not-addressed | test_slash.lua < 1000, case count identical | GI-KC-07 |
| KickCD#31 | Fix this now | low | not-addressed | test_options_panel.lua < 1000, case count identical | GI-KC-08 |
| KickCD#32 | Fix this now | low | not-addressed | test_perfsetup.lua < 1000, case count identical | GI-KC-09 |
| LibKa0s#1 | Fix now | low | not-addressed | Optional budget={msPerSec,maxMs} per bucket, validated, carried into the record and JSON, reported ok/OVER/not exercised; byte-identical report without budgets; nothing gates | GI-LK-09 |
| LibKa0s#7 | Fix this now | low | not-addressed | Perf.lua < 1000 via PerfCommands.lua (paired minor); command tests unchanged; absent-file stub case | GI-LK-07 |
| LibKa0s#9 | Fix now | low | not-addressed | docs/api/CONSUMERS.md census with file:line and classification; adoption-prompt counts rewritten; zero-consumer exports documented; host-adoption issues filed | GI-LK-13 |
| LibKa0s#12 | Fix now | low | not-addressed | A declared parent with no calls appears in the record with zero counts whenever a child names it; red test first | GI-LK-08 |
| LibKa0s#17 | Fix now | low | addressed | Closed 2026-10-01 (state:done): already addressed by test_options_tabs.lua invariance cases | GI-LK-10 (comment only) |
| LibKa0s#18 | Fix now | low | addressed | Closed 2026-10-01 (state:done): already addressed by test_options_tabs.lua invariance cases | GI-LK-10 (comment only) |
| LibKa0s#19 | Fix now | low | addressed | Closed 2026-10-01 (state:done): already addressed by test_options_tabs.lua invariance cases | GI-LK-10 (comment only) |
| LibKa0s#20 | Fix now | low | addressed | Closed 2026-10-01 (state:done): already addressed by test_options_tabs.lua invariance cases | — |
| LibKa0s#35 | Fix this now | low | not-addressed | test_options.lua < 1000 via test_options_render.lua; case count identical | GI-LK-01 |
| LibKa0s#36 | Fix this now | low | not-addressed | Widgets.lua < 1000 via WidgetsReorder.lua (paired minor); load-without case | GI-LK-04 |
| LibKa0s#38 | Fix this now | low | not-addressed | test_schema.lua < 1000 via test_schema_write.lua; case count identical | GI-LK-02 |
| LootHistory#32 | Fix now | low | not-addressed | Analytics.lua < 1000 via AnalyticsFormat/AnalyticsCharts; NS.Analytics surface unchanged; sighted CCN of Analytics ≤ 15 | GI-LH-01 |
| MultiMeters#56 | Fix this now | low | not-addressed | A classed NPC None-source is refused in DamageDone; Valeera (Creature GUID, allowlisted id) still admitted; Enemy gate kept | GI-MM-01 |
| PanelMaster#54 | Fix this now | low | not-addressed | Every per-panel field write goes through SchemaRuntime.Set/SetMany with the panel id; architecture-§5 row retired; Slash/Options rows unchanged for profile paths | GI-PM-03 |
| PartyFrameEnhanced#12 | Fix this now | low | partially-addressed | castStartStop attributed (first-cast table growth) in docs/performance.md; warm-up cycle; ceiling re-derived to 24 | GI-PF-01 |
| PrettyChat#1 | Close - will not do | low | owner close | Closed 2026-10-01 (state:will-not-do) | — |
| PrettyChat#5 | Close - will not do | low | owner close | Closed 2026-10-01 (state:will-not-do) | — |
| WhatGroup#1 | Fix this now | low | not-addressed | Popup shows the role (assigned > application > offered) with icon; chat row behind notify.showRole (default on); secret-safe | GI-WG-01 |

## Carried-in requirement not in the CSV

| Issue | Why | Requirement | Items |
|---|---|---|---|
| ConsumableMaster#16 | The consumer half of LibKa0s#40 | ERR_BOOL / ERR_ALLOWED / ERR_COLOR overrides un-marked dead and tested live | GI-CM-01 |


## Cross-cutting requirements

- **R1. Tests first.** Every behaviour change starts with a test that is red against today's code. Pure moves keep suite totals identical (record the before/after counts in the commit body).
- **R2. Green gate per repo**, as its `CLAUDE.md` defines it: `lua tests/run.lua` and `luacheck .` at 0/0, the sighted complexity suite with no function above CCN 15, the 1500-line cap, and vendor parity. All heavy runs go through `ka0s-bounded`.
- **R3. Docs move with code.** Each repo's `CLAUDE.md` names its required docs: `docs/test-cases.md`, the README tests badge, `ARCHITECTURE.md` / module map, `smoke-tests.md` rows for anything visible.
- **R4. Never edit `libs/` or `tests/_kit/`** in an addon. Library changes land in LibKa0s and arrive by re-vendor.
- **R5. Line endings.** Addon files are CRLF. Python edits use `newline=''`.
- **R6. No version bump, no merge, no pushed tag** without the owner's go-ahead.
