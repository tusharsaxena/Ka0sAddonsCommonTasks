# Findings

Twelve read-only surveys, 2026-09-25. Every addon was on `master`, clean, and vendored LibKa0s
**v1.58.0**, except AuraMaster's batch-8 branch, which vendors the local-only **v1.59.0**. File:line
references are as surveyed and must be re-checked when an item is executed.

## 1. Per-addon survey table

| Addon | Slash | Debug surface today | Domain state the report needs (headline) | Hazards | Buffer pins (1500) | DragHandle | Effort |
|---|---|---|---|---|---|---|---|
| **AbsorbTracker** | `/at`, `/absorbtracker` | `debug on/off`, bare toggles window, `debug events` (to chat), `debug hold`. No dump. `[Init]` summary only. | Per unit (player/target/focus): enabled, mirror, `ShouldShowBar` + reason; bar frames vs stored position; resolved media and LSM fallbacks; class colors; gated absorb readout; event registration; repaint pending; session counters | `UnitGetTotalAbsorbs` / `UnitHealthMax` secret (gate with `IsConcatSafe`, print `<secret>`); `AbbreviateNumbers(secret)` is a secret string; never read bar value back. Four file-local seams (`visibilityReason`, `dbgLastShown`, Timer `pending`, dbg counters). Degraded stub `Add` is a no-op. | Docs only: `ARCHITECTURE.md:75`, `module-map.md:306,362,808,908`, `smoke-tests.md:89,94,95`. No test pin. | **Yes, 3 strips** (`modules/Bar.lua:43-91`) | M |
| **AuraMaster** (reference) | `/am`, `/auramaster` | **Complete on batch-8:** both forms, no alias, live while disabled (host `liveVerbs`), ungated, append, secret-safe, markers, cap `min(1200, MAX_BUFFER-100)`, README section, `docs/debug.md` | Already dumps identity, state flags, apply queue, counts, non-default profile rows, auras per unit, per-container Cont/Filt/Plan/Cfg/Shown | Aura reads skipped while `AurasAreSecret`; engine `IsShown` via `CanAccess`. Deviations listed in §4 | `DebugLogSetup.lua:5`, `Diagnostics.lua:41` (`or 1500`), `:43`, `debug.md:19,126`, `known-limitations.md:234`, `smoke-tests.md:1328`; `test_diagnostics.lua:535` pins MAX_LINES ≤ 1200 | **Yes, already uses X** (container enabled=false) | S (M if it migrates onto the helper) |
| **BankLedger** | `/bl`, `/bankledger` | `debug on/off`, bare toggles, **`debug scan`** and **`debug panel`** structured dumps (ungated, append) | Non-default rows (reuse `traceSettingsReset` walk); filters; ledger counts, tail of ~20 entries; capture engine state; session; fold `Ledger:Diagnose` as a section; windows; bank-replacing addons loaded | No secrets. Strip item-link escapes. Never call `QueryGuildBankTab`. Degraded fallback live list at `settings/Slash.lua:404` | `smoke-tests.md:391,393`. No test pin. | No | M |
| **ConsumableMaster** | `/cm`, `/consumablemaster` | `debug on/off`, bare toggles; **any other word toggles**, so `/cm debug diagnostics` toggles today. `/cm dump <target>` namespace, chat-only, uncapped, color escapes | Spec context; per-category picks (top 5, not full lists); macro state and account slots; MacroManager `pendingUpdates` (file-local); TooltipCache pending; macro bar frame; rejected events | `C_Spell.GetSpellCooldown` fields secret; secure macro bar (read only, no setters); `string.format` on a secret raises before `Add`; degraded path falls back to **chat**, which a report would flood | **`tests/test_debuglog.lua:281`** `t.eq(lib.MAX_BUFFER, 1500)`; `smoke-tests.md:289,651` | **Yes, 1 strip** (`modules/MacroBar.lua:177`) | M |
| **KickCD** | `/kcd`, `/kickcd` | `debug spells/castbar/interrupt/window/on/off/toggle/events`; four chat dumps; bare prints verb list and toggles | Spell list per class/spec (unreachable by `/kcd get`); Cooldowns runtime; CM cache (read only); IconGrid and Castbar per unit; target/focus casting; UnitLabel; link state | Cast info (name, texture, spellID, notInterruptible) secret; charges secret; curve-driven alpha may be secret; `Castbar.lua` 1435/1500 lines | `core/DebugLogSetup.lua:5`, `debug.md:28-29`, `smoke-tests.md:659,667`. No test pin. | **Yes, up to 4 strips** (IconGrid `:694-714`, Castbar `Castbar_Handle.lua:87-120`) | M (L if a new `icons.enabled` row) |
| **LootHistory** | `/lh`, `/loothistory` | `debug on/off`, bare toggles, `debug events`. No dump. | Locale pattern build; capture wiring; filters; attribution context; **aggregate** history summary and ~25-row tail; AH providers; test mode; browser | Never call `GetItemInfo`, tooltip scans, `C_ChallengeMode`. Host `LIVE_WHILE_DISABLED` at `settings/Schema.lua:858` pinned equal to the library list; degraded dispatcher | `smoke-tests.md:706,715,716,963`. No test pin. | No | M |
| **MultiMeters** | `/mm`, `/multimeters` | **`/mm debug diag`** runs a full report (ungated, append, secret-safe, per-section pcall) that **breaks the no-alias rule**. Also `recap`, `identity`, `feign`, `tooltip`. No cap, no end marker, color escapes | Most exists. Add: settings diff per profile and per window, window inventory with Visibility results, lifecycle, restriction state, cache and roster counts | Every `C_DamageMeter` figure, GUID and duration is secret under restriction; frames given secrets have secret geometry (positions from config only); ~30 files cite `/mm debug diag` | Prose only: `DebugLogSetup.lua:5,59,87`, `debug.md:47`, `common-tasks.md:66`, `scope.md:406`; `ARCHITECTURE.md:399` is history (append, do not rewrite) | No | M |
| **PanelMaster** | `/pm`, `/panelmaster` | **`/pm debug dump`** writes `D:Diagnose()` ungated and appending; no markers, no cap, `tostring` not `SafeToString`, no per-section pcall | Per-panel non-default fields; renderer vs record geometry; media and art resolution; Sunn packs; combat unlock queue (file-local); mouseover ticker | Low secret exposure; must not trigger Recover/FitToArtwork/SetPoint | `smoke-tests.md:685,718,881`, `DebugLogSetup.lua:9` | No | M |
| **PartyFrameEnhanced** | `/pfe`, `/partyframeenhanced` | `debug on/off`, bare toggles. `/pfe status` prints a summary to chat. No dump. | Party context (class tokens only); frame provider; non-default rows; free-placement positions; per feature per unit element state; secure button driver vs want; RangeFade mode; secure-write queue (file-local) | Party cast info secret; fade frame `GetAlpha` secret; compound-token `UnitIsUnit` secret; `IsShown` on secure buttons unverified; no `GetPoint` on Blizzard/EllesmereUI frames | Comment `DebugLogSetup.lua:4` only | No (own Anchor grips) | M |
| **PrettyChat** | `/pc`, `/prettychat` | `debug on/off`, bare/`toggle` toggles, other words print usage. `/pc test` previews. No dump. | Master and visibility gate; combat watcher; changed-row summary; per-string overrides (`||`-escaped); **live-global audit** (installed vs `_G`); snapshot health; patch drift; render check | No secrets. Data **is** format strings: escape `|` as `||`, do not strip; pass format strings as `%s` args. Host comment claims `liveVerbs` widens; it replaces | **`tests/test_debuglog.lua:184-212`** (1520-line loop, `1500`, `"1 / 1500 lines"`), **`tests/test_libka0s.lua:204`**; `smoke-tests.md:217,222,223,226,727`; `Schema.lua:955` comment | No | M |
| **WhatGroup** | `/wg`, `/whatgroup` | `debug on/off`, bare toggles, other words print two usage lines (pinned `test_slash.lua:304-308`). `docs/debug-content.md` says "ships no debug verb". | LFG applications as the client sees them vs capture tables (file-local); pending info; teleport resolution; popup file-locals; saved vs live position | Latent: `GetSpellCooldownRemaining` does arithmetic without a secret check; never build the popup (secure button). Accessors land in files at 1143 (`core/WhatGroup.lua`) and 1182 (`modules/Frame.lua`) lines | `ARCHITECTURE.md:262`, `smoke-tests.md:106,736`; `debug-content.md:5-6` names the minor | No | M |

### Live-verb status of the top-level `diagnostics` verb today

| Addon | How the live set is built | `/<slash> diagnostics` while disabled | `/<slash> debug diagnostics` |
|---|---|---|---|
| AbsorbTracker | host `liveVerbs` = `LIVE_VERBS` + `resetposition`, `profile` | Refused | Live |
| AuraMaster | host `liveVerbs` = `LIVE_VERBS` + `containers`, `select`, `diagnostics` | **Live** | Live |
| BankLedger | library default; degraded copy at `Slash.lua:404` | Refused | Live |
| ConsumableMaster | host `LIVE_VERBS` = 12 + `dump` | Refused | Live, but toggles the window today |
| KickCD | `LIVE_VERBS` + `NS.EXTRA_LIVE_VERBS` (`spells`); `test_slash.lua:940-955` pins COMMANDS − live = FEATURE_VERBS | Refused | Live |
| LootHistory | library default + host table gate `Schema.lua:858` | Refused (both gates) | Live |
| MultiMeters | library default, deliberately | Refused | Live (only `diag` exists) |
| PanelMaster | library default, deliberately; degraded copy `Slash.lua:447-455` | Refused | Live (only `dump` exists) |
| PartyFrameEnhanced | host `LIVE_WHILE_DISABLED` = 12 + `status`, `profile` | Refused | Live |
| PrettyChat | library default | Refused | Live |
| WhatGroup | library default, deliberately (pinned `test_disabled.lua:316-318`) | Refused | Live |

**Also stale at re-vendor:** AbsorbTracker states the LibKa0s file count ("twenty-one files") at `docs/ARCHITECTURE.md:49`, `docs/module-map.md:908` and `docs/performance.md:390`. It becomes twenty-two with `DebugLogDiagnostics.lua` (DR-AT-05). ConsumableMaster's README debug rows are at `:117` and `:120`, not `:114`/`:116`.

**10 of 11 addons would refuse the top-level verb while disabled.** Adding `diagnostics` to
`LibKa0s-Slash` `lib.LIVE_VERBS` fixes the six that use the library default with no host edit, and the
hosts with their own lists pick it up because they build on `LIVE_VERBS`. Only the host **copies** of the
list (in code and in tests) need a same-commit edit at re-vendor.

## 2. Cross-cutting findings

| ID | Finding | Consequence for the plan |
|---|---|---|
| **C1** | The top-level verb is not live while disabled anywhere except AuraMaster (§1 table). | Slash minor 16 adds `diagnostics` to `LIVE_VERBS` (DR-LK-04). Each re-vendor commit rolls the host copies: CM `settings/Slash.lua:325-329` (and drops nothing, `dump` stays), LH `Schema.lua:858` + `test_disabled.lua:310-313` + `test_slash.lua:908`, PC `test_disabled.lua:272-276`, WG `test_slash.lua:473-475`, BL `Slash.lua:404`, PM `Slash.lua:447-455`, PF `LIVE_WHILE_DISABLED`, AT liveVerbs builder. |
| **C2** | Every addon's degraded DebugLog stub makes `Add` a no-op, so a report on a library-absent install writes nothing silently (AT, BL, LH, PM, PC, WG, PF). CM falls back to chat instead, which a report would flood. | The stub MUST answer `RunDiagnostics` with the collection's library-absent line (STD-14). Every addon's DebugLog parity case goes red at re-vendor until its stub gains the member, which is the enforcement. |
| **C3** | **The literal 1500 is overloaded.** Besides `MAX_BUFFER`, it is the layout-§1 1500-line file cap (every `tests/_kit/test_layout_cap.lua`, many ARCHITECTURE/testing/test-cases lines, file headers), plus fixtures (LH AH prices, MM tooltip amounts, AT `debug hold 1500000`). | No sed sweeps. Each addon's buffer ripple is the explicit site list in §1 and in its `-05` item. Frozen bundles (`docs/audits`, `docs/reviews`, `docs/automated-tests/<run>`, `docs/revendor`, `docs/superpowers/research`) are never edited. |
| **C4** | State the report needs is file-local in most addons: AT (4 seams), CM (3), PM (1), PF (3), WG (2 snapshot accessors), KC (reads existing module tables). | Each addon gets a `-02` "read-only seams" item with tests, landed before the report. Accessors return copies. `test_surface_parity` degraded arms may need matching members. |
| **C5** | Existing dump verbs collide with the "exactly two forms" rule: MM `debug diag` (a true alias), PM `debug dump` (same report, different name). Others are separate topics: BL `scan`/`panel`, KC `spells`/`castbar`/`interrupt`/`events`, AT/LH `events`, MM `recap`/`identity`/`feign`/`tooltip`, CM `/cm dump <target>`, PF `/pfe status`. | Rule: a verb that runs the diagnostics report under another name is forbidden (MM `diag`, PM `dump` retire). Topic dumps stay under the MAY and are folded into the report as sections where useful. Owner confirms (Q7). |
| **C6** | The report can hold player names, alts' `Name-Realm`, group titles and gold balances. | Ruled (Q11): nothing is redacted, because users send the report to the owner privately. No README note. |
| **C7** | Escapes: most report text wants `|c`/`|T`/`|H` stripped for a clean Copy. PrettyChat's data **is** format strings, where stripping destroys the evidence. | Helper strips by default; `out:escape(s)` renders `|` as `||` for values that must round-trip (STD-11, DR-LK-03). |
| **C8** | AuraMaster's report cap `min(1200, MAX_BUFFER-100)` means trace room is 300 lines at 1500, 1800 at 3000, 3800 at 5000. "One copy carries both" is only really true after the buffer rises. | The helper keeps AuraMaster's formula as the default (Q8). The rule states the report is guaranteed complete and the trace is best effort. |
| **C9** | Unknown `debug` words differ: most toggle the window, PC and WG print usage, KC prints an error and the list. | STD-03 fixes only that `diagnostics` is checked first and that no other word runs the report. The fallback stays per addon. |
| **C10** | Verb and live-set counts are pinned in prose: AT "18" (≈8 docs), BL "17" (`ARCHITECTURE.md:174,357`), LH "16"/"sixteen" (with `test_schema.lua:798-803` prose check), MM "18"/"seven words", PF "seventeen", PC "twelve verbs", WG "thirteen verbs" comment, CM order pin `test_slashsetup.lua:244`. | Each `-03` item updates its counts; M4 runs `sync-docs` to catch the rest. |
| **C11** | A report walks the Schema for non-default rows in every addon; AuraMaster does it by hand (`Signature(get)` vs `Signature(default)` + `FormatValue`). | The helper gains `out:nonDefaults(schemaRows, get, default, format)` (DR-LK-03), so the walk is written once. |
| **C12** | `D:Add` runs `UpdateScrollBar` and `UpdateStatus` per line, so a 1200-line report is 1200 status updates. | DR-LK-03 writes the report through a batched internal append (one status update at the end). Measured together with the Copy timing. |

## 3. Standard findings (WowAddonStandards `master` @ `9a21c66`, v2.67.0, 2026-09-24)

| Where | Today | Needed |
|---|---|---|
| `STANDARDS.md:1` | v2.67.0, 2026-09-24 | v2.68.0 (minor: a new MUST that addons fail until adoption; precedents v2.42.0, v2.52.0). Footer line 245 says "Authoritative as of 2026-09-23"; fix in the same pass. |
| `debug-logging.md:9` | Adoption story: "debug on, reproduce, Copy, paste" | Add the `/<slash> diagnostics` step |
| `debug-logging.md:22` (§1) | `lib.MAX_BUFFER` (1500) | The measured number, a history clause, and the helper in the guarantee list |
| `debug-logging.md:58-59` (§4) | "**MAY** support structured dump verbs" | MUST ship the diagnostics dump (§14); other topics stay MAY |
| `debug-logging.md:67` (§5) | bare toggles; on/off | `debug diagnostics` dispatched first |
| `debug-logging.md:86` (§7) | stub member list | add `RunDiagnostics` |
| `debug-logging.md:125-126` (§9), `:199` (§11) | 1500 | the new number |
| new | — | **debug-logging-§14** appended (numbers stay stable, v1.11.0 precedent) |
| `slash-commands.md:40,45,72,225,293` | the reserved verbs are **enumerated** (the file never says "twelve"); no `diagnostics` | `diagnostics` added to each enumeration: thirteenth reserved verb, registered in every addon, live while disabled |
| `documentation.md` §1 (from `:77`) | items 8 Troubleshooting, 9 Issues | new item 9 `## Reporting a bug`; renumber 9-11 → 10-12 (live refs at `:10`, `:92`, `~:96`) |
| `documentation.md` §3 (`:256`) | Tier 2 `docs/debug.md` fires on surfaces "beyond the default console" | Ruling needed: the report fires it everywhere, or the trigger excludes it (Q6) |
| `anti-patterns.md`, `STANDARDS.md:80` | #1–#89 | #90 |
| `AUDIT.md` step 4 (near `:599`), `:624,631` | no check; the live verbs enumerated | §14 check; `diagnostics` in each enumeration |
| `library-stack.md:82,93,256`, `STANDARDS.md:57,69`, `EXECUTIVE_SUMMARY.md:56`, `open-evolutions.md:13`, `NEW_ADDON_CONTEXT.md:516-521,742,816,1361` | 1500; no diagnostics; twenty-one files (`:82` is a recount paragraph); `:256` is the library's debug-logging applicability row | new number; helper; twenty-two files, recounted; template sections; applicability row names the helper |
| `NEW_ADDON.md` (the playbook `/wow-addon:new-addon` executes step by step) `:123`, `:177`, `:253-257` | README order has no `## Reporting a bug`; setup and slash steps have no diagnostics | a scaffold must be born with both forms, the sections file and the README section (missed by the first draft) |
| root `README.md` `## Status` (`:144`) | names v2.67.0 | v2.68.0 (`standards/README.md` step 5) |
| `documentation.md:92`, `:96` | `## Credits` is item 11 | item 12 |
| wow-addon plugin | `bump-version.md:124` cites Version History as item 10 (`:192` says item 11); `sync-docs.md:172` and `new-addon.md:210` cite `## Credits` as item 13, already stale (it is 11 today); `agents/standards-audit.md:219-221,263` and `agents/review.md:470` enumerate the live verbs; `new-addon` and `sync-docs` do not know the new section; `plugin.json` 2.4.0 | STD-25, DR-WA-01 |

## 4. Library findings (LibKa0s, tree on `feat/2026-09-25-draghandle-close` @ `53c141a`, local tag `v1.59.0`)

- `v1.59.0` = `53c141a`, two commits past the master merge `0491c1a`: `e8faa5d` (WidgetsDragHandle
  minor 3, the opt-in close mark: `onClose`, `closeIcon`, `closeTooltip`) and `53c141a` (release run).
  The **branch** is on origin; the **tag** is local only.
- `LibKa0s/Slash.lua:111-114`: `lib.LIVE_VERBS` has twelve verbs, no `diagnostics`. Slash is minor 15. The "twelve reserved verbs" comments are at `:89`, `:478` and `:826`.
- There is no runtime LibKa0s release string: `Core.lua:31-32` exports only `MODULES` (per-major minors). The report prints running minors (STD-10).
- `docs/releasing.md` names the file count at `:28` ("All twenty-one, by their exact constant names") and `:226`, besides the `:7` constants table. `testkit/` has no DebugLog or Slash coupling, so `Kit.VERSION` would stay put, but Q20 (b) adds the shared `test_diagnostics_contract.lua` case, so the kit revision bumps in v1.60.0.
- The LibKa0s working tree is checked out on `feat/2026-09-25-draghandle-close` (clean). AuraMaster's batch workflow may still need it, so the M2 branch cut has a pre-check (`03_EXECUTION_PLAN.md` §1).
- `LibKa0s/DebugLog.lua` (minor 13, 821 lines): `:57` `lib.MAX_BUFFER = 1500`; `:68` `local BUFFER_SLACK = 64`
  (not exported); `:501` `SetMaxLines(lib.MAX_BUFFER)` reads at first frame build only; `:624-629` `Add` is
  public and ungated; `:635-636` compaction; `:734-742` `ShowCopy`.
- Adding ~180 lines of helper would push `DebugLog.lua` past 1000 lines (layout-§1 "on notice"), and
  `tests/test_debuglog.lua` is already 988 lines. Hence a **secondary file** `DebugLogDiagnostics.lua`,
  paired the way `WidgetsDragHandle.lua:48-56` pairs.
- `tests/test_debuglog.lua`: `:92-96` pins 1500 (deliberately); `:195` boundary set; `:212-239`
  compaction case whose **arithmetic** breaks once slack ≥ 100, not just its literals. Reader cases grow
  ~3.3× in `Add` count; check against `KA0S_KIT_TIMEOUT_S` (900) and `KA0S_KIT_PROC_MB` (2048).
- Slack math: moves per line ≈ `MAX_BUFFER / (SLACK + 1)`; 23 today. Keeping the ratio gives 200 at
  5000 or 128 at 3000.
- A 5000-line buffer is roughly 0.6–1 MB in one multiline EditBox (`Widgets.lua:604-615`). That is the
  cost the measurement gate exists for.

### AuraMaster reference: deviations from the rule as drafted

| # | AuraMaster today | Rule / helper |
|---|---|---|
| a | `MAX_LINES = min(1200, BUFFER-100)`, `BUFFER = lib.MAX_BUFFER or 1500` | Cap comes from the library (`lib.DIAG_MAX_LINES`, clamped to `MAX_BUFFER - 100`); no `or 1500` literal |
| b | `Run()` shows the console itself | Required (STD-09); README step 3 stays as the fallback wording the owner gave |
| c | `diagnostics` added to host `liveVerbs` | Library `LIVE_VERBS`; the host extra becomes redundant (harmless) |
| d | Begin marker names short brand "Aura Master"; end marker names no addon | Both markers carry the brand name (STD-08) |
| e | No LibKa0s → chat line, returns 0 | Required, through the stub (STD-14) |
| f | Body lines English, chat line localized | Stated explicitly (STD-13) |
| g | `UnitAffectingCombat`/`InCombatLockdown` unguarded in `stateLine` | Helper header wraps its own reads |

## 5. Tooling findings (added in review, 2026-09-26)

| ID | Finding | Consequence |
|---|---|---|
| **C13** | `/wow-addon:revendor-standards` and `/wow-addon:standards-audit` fetch the standard from `raw.githubusercontent.com/tusharsaxena/WowAddonStandards/master` (`wow-addon/commands/revendor-standards.md:28`). | M4 `-07` items cannot use them until v2.68.0 is on GitHub `master`. New owner gate DR-OW-07 (Q21). |
| **C14** | `/wow-addon:revendor-libka0s` takes the payload from a **tag** with `git archive`, and each consumer's `tests/test_vendor_sync.lua` pins the bytes at the named tag. It also interviews per new surface and files declines as issues. | Local tag `v1.60.0` is enough for M3. A tag is never re-cut: a fix ships as v1.60.1. The `-01` interview is answered from this plan, and no decline issues are filed. |
| **C15** | The plugin runs from the installed cache, so DR-WA-01 changes nothing until the owner updates the plugin. | M4's `sync-docs` may run on the old text. The README section is checked by hand (AUD-01 step 6). |

