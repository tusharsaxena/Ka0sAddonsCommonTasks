# Coverage map — LootHistory (DL-LH-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis) and §9 (coalescing + quiet steady
state). Branch `feat/2026-09-30-debug-logs-and-resize`, commit `2f3f5f0`. Gate: 1003/1003 tests,
luacheck 0/0 (74 files), lizard 0 functions over CCN 15 (`NS.StandDown` is at 15, the most of any
touched function).

Legend: **ok** = already covered, **added** = new line, **fixed** = existing line changed,
**left** = deliberately not logged (why given).

## 1. Events registered

| Event / hook | Handler | Existing line | Gap | Done |
|---|---|---|---|---|
| `PLAYER_ENTERING_WORLD` | `addon:OnEnterWorld` (core/LootHistory.lua) | none | arms two login deferrals; flag is session-only and off at login | **left**: gated off at login by construction; the deferrals' own `[Prune]`/`[Migrate]` lines land if logging is on |
| `CHAT_MSG_LOOT` | `Collector:OnChatMsgLoot` | `[Loot]`, `[AHPrice]`, `[Drop] … reason=` | other players' lines return silently | **left**: not the player's loot; a line per group member's loot would be per-item spam |
| `CHAT_MSG_CURRENCY` | `Collector:OnChatMsgCurrency` | `[Currency]`, `[Drop] … blacklist/source` | two silent returns on a self line: capture off, unresolved link (a non-self line still returns silently, at the self-parse, before either) | **added** `[Drop] currency line reason=recordCurrency-off` / `reason=unresolved-link` |
| `LOOT_OPENED` | `Attribution:OnLootOpened` | one `[Open]` summary per window | none | ok |
| `ENCOUNTER_START/END` | Attribution | `[Attr] encounter …` | none | ok |
| `CHALLENGE_MODE_START/COMPLETED/RESET` | Attribution | `[Attr] keystone …` | none | ok |
| `ZONE_CHANGED_NEW_AREA` | `Attribution:OnZoneChanged` | `[Attr] keystone cleared / re-armed` on change only | none | ok (already change-only) |
| `TRADE_ACCEPT_UPDATE` | `Attribution:OnTradeAcceptUpdate` | stamp line on full accept | partial accepts silent | **left**: fires repeatedly, changes nothing |
| `QUEST_TURNED_IN` | Attribution | Stamp's `[Attr]` | none | ok |
| `UNIT_SPELLCAST_SUCCEEDED` (player) | `Attribution:OnSpellSucceeded` | `[Cast]` on deconstruct only | none | ok (already quiet on the rotation) |
| `PLAYER_REGEN_DISABLED/ENABLED` | Browser → `ApplyVisibility`, `EndTestModeForCombat` | none | combat edge that hides the window / ends test mode had no line | **added** `[UI] window hidden by visibility=<mode> (combat=<b> | setting changed)`; **added** `[Table] test mode off (combat started)` |
| hooks: `BuyMerchantItem`, `TakeInboxItem`, `AutoLootMailItem`, `GetQuestReward` | Stamp funnel | `[Attr] stamp`, `[Mail]` | stamp refused while stood down was silent | **added** `[Attr] stamp <src> ignored: stood down` |
| hook: `UseContainerItem` | `Attribution:OnContainerItemUse` | `[Open] UseContainerItem bag slot hasLoot spellTargeting` on **every** use | per-item stream on a merchant sale / bag-addon bulk action (§9) | **fixed**: non-loot use logs nothing; lootable+targeting logs `[Open] container use … ignored: spell targeting`; a stamp is Stamp's own line |
| bus: `RecordAdded` (coalesced), `HistoryChanged`, `SettingsChanged` | Browser, Analytics, Panel, Collector | `[Table]`, `[Insights]` per repaint | identical summaries repeat (test mode, filtered Insights, resize, no-op HistoryChanged) | **fixed**: change-gated (below) |
| refused registrations | `core/CoreSetup.lua` `noteRefusals` | `[Init] event X refused` once per name | none | ok |

## 2. State edges

| Edge | Existing | Done |
|---|---|---|
| Addon stand-down / stand-up (Lifecycle latch; the library narrates nothing) | none | **added** `[State] stood down (holds: …): capture unregistered, N deferral(s) canceled` and `[State] stood up: capture registered (price providers: …; latch: …)` |
| Profile switch / copy / reset | `[Profile]` / `[Set]` in `traceProfileEvent` | ok |
| Combat in/out | none | **added** only where the addon reacts (hide by visibility, test-mode end); an edge that changes nothing logs nothing |
| Addon-restriction / secret state, spec, roster | not reacted to | n/a (standard: an edge the addon does not react to needs no line) |
| Debug enable/disable | library `[Debug]` bracket + `[Init]` | ok |

## 3. Deferred work

| Deferral | Hold | Flush | Done |
|---|---|---|---|
| `NS.After` login prune (5 s) + bound repair (5 s, 20 s) | not logged (flag off at login) | `[Prune]`, `[Migrate] bound repair …` | **fixed** repair line: now `(attempt N, still pending / done / gave up)`, attempt read before the clear (it printed `attempt 0` on every job end) |
| Stand-down cancels all live deferrals | none | — | **added** count in the `[State] stood down` line (held-then-never-flushed is visible) |
| `NS.Coalesce` repaint triggers | not logged | the `[Table]`/`[Insights]` line | **left**: a hold line per burst would be per-item; the flush line and the stand-down count cover it |
| Bound repair on window open | — | `[Migrate]` pass line | ok (content changes each pass) |

## 4. Refusals / guards

| Guard | Existing | Done |
|---|---|---|
| `B:Show` stood down (chat silent by design) | none | **added** `[UI] open refused: stood down` |
| `B:Show` visibility | chat only | **added** `[UI] open refused: visibility=<mode>` |
| Slash feature verb while disabled (library prints, logs nothing) | none | **added** `[Cmd] /lh <verb> refused: addon disabled` (host reads switch, `NS.COMMANDS`, live set; typos and aliases not logged) |
| Schema write rejected (library logs only accepted writes) | chat only | **added** `[Set] <path> rejected: <reason>` in `S:Set`, arity preserved |
| Test mode start refused (combat / visibility) | chat only | **added** `[Table] test mode refused: <why>` |
| Item gate (blacklist/quality/source/quest) | `[Drop] … reason=` | ok |
| Retention Always | silent return | **added** `[Prune] skipped: retention is Always` |

## 5. Dependencies

Price providers (Auctionator, TSM, Oribos) and the latch kind are named once per stand-up in the
`[State] stood up` line. **Left**: the load-time stand-up runs with the flag off (session-only), so a
session sees the dependency line only after an edge while logging is on; the diagnostics report's
`auction:` and `lifecycle:` sections carry the same facts for the login case. Emitting it on debug
enable would need the `[Init]` line changed or a second line in the library's enable bracket — not
done (library-owned seam).

## 6. Errors caught by addon-owned pcalls

| Site | Existing | Done |
|---|---|---|
| `AuctionPrice:GatherAll` provider fetch | swallowed | **added** `[AHPrice] <prov> fetch failed: <err>`, once per distinct (provider, message) |
| `settings/Panel.lua` `runRebuilders` | swallowed | **added** `[Cfg] panel rebuilder failed: <err>`, once per distinct message |
| `filterWrite`, `writeRetentionQuietly`, stub `BulkRun` | re-raise | ok (not swallowed) |
| CoreSetup `SafeRegister` pcall | `[Init] event refused` | ok |

## 7. Data mutations and views

| Flow | Existing | Done |
|---|---|---|
| Delete / purge / prune / migrate | `[Data]`, `[Prune]`, `[Migrate]` | ok |
| Filter-list edits | `[Filters] blacklist=N whitelist=N` (no act, no currency count) | **fixed** `[Filters] <act> <list> <id>: blacklist=N whitelist=N currency=N`, format args built behind the gate |
| Test mode (dataset swapped) | none | **added** `[Table] test mode on: N sample rows` / `off (<why>)` |
| CSV export | none | **added** `[UI] export csv: data set=<ds>, N chars` |
| Window shown/hidden, tab switch | `[UI]` | ok |
| Settings seam | library `[Set]` | ok |

## 8. Repeating paths (§9 quiet steady state)

| Path | Before | After |
|---|---|---|
| `BrowserTable:Refresh` (coalesced RecordAdded, resize, HistoryChanged, filter keystrokes) | one `[Table]` per repaint, identical in test mode / resize / no-op | **change-gated** on the built summary; reset on each window OnShow so an open still logs its render |
| `Analytics:Refresh` (live refresh per coalesced RecordAdded while the tab is up) | one `[Insights]` per pass, identical under a non-matching filter or test mode | **change-gated** the same way |
| `UseContainerItem` hook | one `[Open]` per use | only the targeting refusal logs |
| `UNIT_SPELLCAST_SUCCEEDED`, `ZONE_CHANGED_NEW_AREA`, `TRADE_ACCEPT_UPDATE` | already quiet | ok |
| AH fetch error, panel rebuilder error | (silent) | once per distinct error |

No timer, ticker or OnUpdate in this addon logs; the only repeating timers are the one-shot
`NS.After` deferrals and the coalescers.

## 9. Tests (tests/test_debug_coverage.lua, 16 cases, each with a red-under comment)

State lines (and nothing built with logging off); stamp/open/verb refusals while disabled; live
verb and typo not logged; visibility refusal and hide; rejected `[Set]`; currency drops; container
use; AH error once; bound repair done/gave up; prune skip; `[Filters]` act; **quiet steady state:
10 table repaints → 1 line, a real change still logs; each window open logs once; 10 Insights
recomputes → 1 line**; test-mode on/off/refused. Mutation-checked: removing either change gate, the
AH seen-set, or the repair outcome each turns exactly its case red.

## 10. Deliberately left / follow-ups

- `[Attr] consume`, `[Loot]` and `[AHPrice]` are three lines per recorded item. Each carries
  distinct detail (context detail, record fields, price map); not merged, not per-slot. Candidate
  for a later consolidation if owner wants one line per loot.
- Export `[UI] export csv` and the panel rebuilder error line are not pinned by a test (the export
  frame needs the Widgets dropdown path; `runRebuilders` is file-local). Covered by code review only.
- Observed, not in scope (a behavior bug, not a log gap): `NS.Coalesce`'s `pending` flag stays
  true when `NS.CancelDeferrals` cancels its timer. Browser and Analytics build a fresh coalescer on
  every Enable, so they recover. The settings Panel's `RecordAdded` coalescer (settings/Panel.lua,
  built once under `if not P.__ev`, kept through a stand-down as setup) does not: a stand-down inside
  the coalesce window after a loot leaves it stuck, and the General page's storage readout stops
  refreshing on new loot until /reload. Reported as an open question; not fixed here.
- docs/smoke-tests.md was not extended with in-game checks for the new lines (spec S4 asks for the
  headless pins and docs/debug.md only).
