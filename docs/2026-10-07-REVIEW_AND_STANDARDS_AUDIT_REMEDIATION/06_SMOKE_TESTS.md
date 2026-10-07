# 06 — Smoke Tests

**The owner's in-client checklist for the 2026-10-07 remediation: one row for every work item with a
non-empty `smoke` field (57 items), grouped by addon, plus LootHistory's Ledger Phase 2 checks
LED-P2-01 to LED-P2-24 (finding LH-R-03).**

> **The owner records results here, and nobody else does.** No agent runs these steps, fills in a Result
> cell or marks a check passed. That covers LED-P2 too: `inputs/OWNER_SCOPE.md` item 2 puts LH-R-03 in
> this file only so the owner has it to hand. Every Result cell starts blank. When a step has not been
> run, its cell stays blank. It never reads "pass".

Sources: `plan-data/items.json` (the `smoke` field of each item), `inputs/OWNER_SCOPE.md` and
LootHistory's `docs/smoke-tests.md`, section "Ledger capture (timeline ledger Phase 2)".

---

## What is not here

Each item's own `verify` field covers the out-of-game suites (`luacheck`, the headless harness,
`tests/perf.lua`, `lizard`), so none of that is repeated. WowAddonStandards and dev-copilot items have
no in-client part and do not appear. This file covers what only a live client shows: rendering, taint,
event order, SavedVariables as the client writes them, and several addons sharing one LibStub registry.

Each addon's `docs/smoke-tests.md` stays the standing pass. Where a row names one of its sections
(INSTALL-4, PANEL-28, LOC-1, NUM-3 and so on), run that section as well.

## Conventions

- **`/reload`** means `/console reloadui`.
- **Errors.** Run `/console scriptErrors 1` once and keep BugSack/BugGrabber on. "No Lua errors" means
  nothing reaches BugSack or the error frame during the step, including on `/reload`.
- **Taint** is any "Interface action failed because of an AddOn", `ADDON_ACTION_BLOCKED` or
  `ADDON_ACTION_FORBIDDEN`. It counts as a failure even when nothing visible breaks.
- **"In combat"** means hitting a training dummy.
- **Build under test.** Every addon runs on the LibKa0s **v1.71.0** payload re-vendored in M2 (the local
  tag). LibStub loads the highest minor any enabled addon ships, so one stale copy in any enabled addon
  hides a regression. Check that every Ka0s addon's `libs/LibKa0s/` came from v1.71.0 before you start.
- **Result column.** Write `pass`, or `fail` with the exact chat text, the date and the build. When a
  row fails, stop that addon's session unless the next row does not depend on it.
- **When to run.** Run an addon's rows after its last M3 item has landed and before that addon's
  branch is merged. The LibKa0s rows ride along with the first addon session that exercises them.
- **Slash roots:** `/at` AbsorbTracker, `/am` AuraMaster, `/bl` BankLedger, `/cm` ConsumableMaster,
  `/kcd` KickCD, `/lh` LootHistory, `/mm` MultiMeters, `/pm` PanelMaster, `/pc` PrettyChat,
  `/pfe` PartyFrameEnhanced, `/wg` WhatGroup.

## Index

| Section | Items | Notes |
|---|---|---|
| [LibKa0s v1.71.0](#libka0s-v1710-checked-through-the-addons) | 4 | Checked through LootHistory, BankLedger and the full collection |
| [AbsorbTracker](#absorbtracker) | 6 | Needs a target dummy and a shield. AT-09 only confirms or refutes, it does not judge |
| [AuraMaster](#auramaster) | 6 | AM-02 is optional (needs an old-schema profile) |
| [BankLedger](#bankledger) | 4 | |
| [ConsumableMaster](#consumablemaster) | 5 | Needs two characters on different profiles, a Devourer DH and a group |
| [KickCD](#kickcd) | 4 | Needs a hostile caster, a friendly caster and a focus target |
| [LootHistory](#loothistory) | 7 | Needs PrettyChat enabled for LH-01 |
| [LootHistory: Ledger Phase 2 (LH-R-03)](#loothistory-ledger-phase-2-led-p2-01-to-led-p2-24-finding-lh-r-03) | 24 | Release gate for LootHistory 1.4.0, not a merge gate |
| [MultiMeters](#multimeters) | 3 | MM-01 needs a pet class |
| [PanelMaster](#panelmaster) | 6 | Needs an alt on the same profile and a target dummy |
| [PartyFrameEnhanced](#partyframeenhanced) | 5 | Needs a party for PF-03 |
| [PrettyChat](#prettychat) | 4 | |
| [WhatGroup](#whatgroup) | 3 | WG-01 needs an M+ group invite while in combat |

---

## LibKa0s v1.71.0 (checked through the addons)

LibKa0s has no in-client surface of its own. Each row runs in a consumer after the M2 re-vendor.

| Item | What to do | Expected result | Result |
|---|---|---|---|
| LK-03 | In LootHistory, open the Timeline tab, rest the cursor on the chart, then resize the pane. | The crosshair and tooltip re-snap to the point under the cursor instead of staying at the old pixel. An ordinary Timeline still draws its line and dashed ranges as before. | |
| LK-04 | Type in the search box in LootHistory and in BankLedger. Try arrows, Enter, Tab and Esc, then click away. | The suggestion list opens under the box in the box's colors. Arrows, Enter, Tab and Esc work, and losing focus closes the list, exactly as before. | |
| LK-05 (optional) | In any addon wired to Slash, run `/<slash> set <an unbounded number row> nan`. | The not-a-number refusal prints and the setting is unchanged. | |
| LK-12 | With every Ka0s addon enabled on v1.71.0, `/reload`. Open each addon's settings panel and slash help. | No Lua errors. Every settings panel and slash help opens as before. | |

## AbsorbTracker

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-AT | `/reload` with AbsorbTracker enabled on the v1.71.0 payload. Run `/at`, open the settings panel, then `/at unlock`. | No Lua errors. Help prints, the settings panel opens, and unlock shows the drag strips. | |
| AT-02 | `/at unlock`. Drag a bar by its strip, then another by the bar body. `/reload`, then `/at lock`. | Each visible bar shows its drag strip above it. Both drags move and save the bar, the position survives `/reload`, and `/at lock` hides the strips. | |
| AT-05 | In combat at a target dummy with a shield up, watch the Player, Target and Focus bars. Run `/at debug on`. (Review S-01.) | The bars update as before. The `[Combat]` rollup shows events >= repaints. | |
| AT-06 | `/at perf start`, then `/at debug hold 50000`. Then `/at perf finish`, then `/at debug hold 50000 5`. (Review S-03.) | During the perf capture: a refusal line, no `Holding` line, bars unchanged. After finish: the hold runs for 5 s as before. | |
| AT-07 | Out of combat, `/at unlock`, then `/at disable`. Enter combat at a dummy and `/at enable`. Separately, `/reload` in combat on an unlocked profile. (Review S-04.) | One `Bars locked` line. The bars show live absorbs, not the placeholder, for the rest of the fight. After the in-combat `/reload` the bars are locked and live. | |
| AT-09 | Drag the Player bar away from its default spot, then set General > Master scale 1.0, then 1.5, then back to 1.0. (Review S-05, confirm or refute only.) | Record whether the bar's on-screen position moved. This row has no pass or fail. A "confirmed" result opens C-6 as a follow-up outside this run. | |

## AuraMaster

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-AM | `/reload` with AuraMaster enabled. Run `/am help`, `/am containers` and open the settings panel. | No Lua errors. All three open as before. | |
| AM-01 | Create two containers and rename the second to `1`, so container #1 and the container named `1` differ. Run `/am delete 1`, then `/am select 1`, then `/am delete #1`. Delete the test containers afterwards. | `/am delete 1` is refused, naming both, and nothing is deleted. `/am select 1` is refused the same way. `/am delete #1` deletes container #1. | |
| AM-02 (optional) | On a character whose saved profile predates the current schema, or after restoring an older AuraMasterDB backup, `/reload`, then `/am debug on`. | The debug console shows the `[Migrate] vX -> vY` line after the `[Init]` lines. | |
| AM-03 | Run `/am help` and bare `/am`, then `/am containers`. | The debug row reads `Toggle the debug console — on/off enable/disable logging`. The `/am containers` output matches `docs/slash-dispatch.md` row 11. | |
| AM-06 | `/reload` on an existing profile. Then `/am debug on` and `/reload` again. | Containers draw as before with no Lua errors, and no migration error appears in chat. | |
| AM-07 | Open the settings panel's container picker. | Each entry shows its type and style labels with their translated capitalisation (for example `Buffs, Bars`). Nothing else about the picker changed. | |

## BankLedger

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-BL | `/reload` with BankLedger enabled. Run `/bl`, type in the search box and pick a suggested name. | No Lua errors. The browser opens, the suggestion list appears, and picking a name applies it. | |
| BL-02 | `/bl`, History tab. Type ` linen` (leading space), then `cloth ` (trailing space). Switch History to Insights and back. Use Save and Reset on a tab. Run `/bl resetall` and answer Yes. | The table keeps the Linen Cloth rows and the suggestion list offers Linen Cloth. Each pane paints correctly with its own filter, with no flicker or stale rows. Save prints `<Tab> view saved as your default.` and Reset prints `... reset to stock defaults.` The resetall line names the profile. | |
| BL-03 | `/reload`, `/bl`. On each tab use Save view, Reset and Clear. Close and reopen the window. Turn Test mode on and off. | Both tabs open and behave as before. Each tab keeps its live filter across close and reopen within the session. Test mode repaints both tabs. | |
| BL-04 | Run the extended PANEL-28 in BankLedger's `docs/smoke-tests.md`: save a view on History and on Insights, Reset all settings and answer Yes, then Clear on each tab. | Clear on each tab lands on stock defaults. | |

## ConsumableMaster

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-CM | `/reload` with ConsumableMaster enabled on the v1.71.0 payload. Run `/cm help`, open the settings panel (General, Macros, Stat Priority, Macro Bar) and the macro bar. | No Lua errors. Everything opens and behaves as before. | |
| CM-01 | Use two characters on different per-character profiles that pick different items for the same `KCM_` macro. Log in A, then B. Delete one `KCM_` macro in the macro UI and trigger a bag change or `/cm resync`. Watch `/cm debug on` for a few passes. | B's `KCM_` macro body shows B's pick on arrival. The deleted macro is recreated. A written body reads back byte-identical, so no rewrite happens on every pass. | |
| CM-02 | On a Devourer Demon Hunter, open the Stat Priority page, then run `/cm dump` or check the flask or stat-food macro. | Intellect is primary, followed by the seeded secondary order. Intellect consumables are preferred. | |
| CM-03 | With an unseeded consumable in bags that only the other spec's bucket has seen, switch spec. In a group with `/cm debug on`, have a groupmate respec. | The relevant macro picks up the consumable with no bag change. The groupmate's respec produces no ConsumableMaster recompute line. | |
| CM-06 | Out of combat, after a bag change, open several flyouts on the macro bar. | Each flyout lists the same ranked items as before, in the same order and count. | |

## KickCD

| Item | What to do | Expected result | Result |
|---|---|---|---|
| KC-01 | Set cast bar Anchor mode to Primary icon. Remove or disable every watched spell for the current spec (or switch to a spec with none learned), then target a hostile caster. Re-add a spell. | The cast bar stays visible, anchored at the grid position. After the re-add it re-anchors to the first icon without `/reload`. | |
| KC-02 | Set Cast bar > Truncate after (characters) to 5 and target a caster whose spell name is longer than 5 characters. Optionally repeat on a non-English client. Set the option back to 0. | The bar shows the first 5 characters plus `…`. On an accented or Cyrillic name it truncates at the same character count with no broken glyph box. | |
| KC-03 | Set an icon glow trigger to "When target is casting" and target a friendly player or NPC that casts, for example a party member's Hearthstone. Then try the "interruptible" trigger on a hostile caster. | The glow comes on during the friendly cast and goes off when it ends. The interruptible trigger behaves as before. | |
| KC-04 | Run `/kcd debug spels`. Set a focus on a hostile caster and run `/kcd debug castbar focus`, `/kcd debug interrupt focus` and `/kcd debug castbar`. | The typo prints the refusal and the list and does not open or close the debug console. The focus forms print the focus unit's state. Bare `castbar` still reports the target. | |

## LootHistory

| Item | What to do | Expected result | Result |
|---|---|---|---|
| LH-01 | With PrettyChat enabled, loot an item and gain a currency. Change any PrettyChat setting (or `/pc disable` then `/pc enable`, or cross a combat boundary with an in/out-of-combat visibility rule). Loot an item and gain currency again without `/reload`. | All four records appear in the `/lh` browser, including the two after the change. | |
| LH-02 | Open Settings > AddOns > Loot History with the storage readout visible. Loot something and immediately `/lh disable`, then `/lh enable`, then loot again. | The record-count readout updates. | |
| LH-08 | `/lh`. Use group-by, look at the holder-moves rows and sort a grouped view. | The browser opens. Grouping, holder-moves rows and grouped sorting behave as before. | |
| LH-12 | `/lh disable`, then `/lh enable`, then loot something. | On disable the addon goes inert: no capture, and the launcher shows disabled. On enable it comes back and the loot is recorded. | |
| LH-14 | `/lh`. Use group-by, the History and Holdings character dropdowns, and Test mode on and off. | All behave as before. | |
| LH-18 | `/lh`. Use the filter bar, the sort headers and the History and Holdings character dropdowns. Close and reopen the browser. | Everything renders and behaves as before, and the browser keeps its layout. | |
| LH-STD | Run LED-P2-01 to LED-P2-24 in the next section. | Each LED-P2 row has a result. This gates the 1.4.0 release, not the merge. | |

## LootHistory: Ledger Phase 2, LED-P2-01 to LED-P2-24 (finding LH-R-03)

Source: LootHistory `docs/smoke-tests.md`, section "Ledger capture (timeline ledger Phase 2)". That
section is the full text. The rows here are short forms so the owner can work through them.

**Setup:** the live account, with **Track holdings and losses** and **Record gold** ticked, History's
Direction filter set to **All** (row 1 of the filter bar) so transfers show, and Quality on its default.
A move inside one holder is one `⇄` row. Since Phase 7, a move between two holders is a loss on the
sender and a gain on the receiver under the action's reason.

Each check also states API facts that the headless suite could not verify. They are bracketed in the
source doc. When one of them turns out wrong, the fix is a Compat or mock correction in a follow-up
commit, and the check is run again. `trackLedger` defaults to true, so a wrong assumption writes bad rows
account-wide. That is why Phase 2 is signed off only when all 24 rows are recorded, and why the owner
must record them before LootHistory 1.4.0 ships.

| Check | What to do | Expected result | Result |
|---|---|---|---|
| LED-P2-01 | At a banker, deposit a stack from your bags, then withdraw half of it. | Only `⇄` rows (Transfers), `Bags` to `Bank` and back. No gain or loss row for the item. The Holdings tab's bank column updates. | |
| LED-P2-02 | Put an item stack and some gold into the warband bank. | For each, an `OUT WARBAND_DEPOSIT` on the character and an `IN WARBAND_DEPOSIT` on the Warband. No `⇄`. | |
| LED-P2-03 | At a vendor, sell a junk item, repair, buy one item and buy one back. | Item `OUT SELL` and gold `IN SELL` (about 1.5 s later). Gold `OUT REPAIR`. Gold `OUT BUY` with item `IN VENDOR`, the item row chat-claimed. The buyback is gold `OUT BUY`. | |
| LED-P2-04 | Kill a mob that drops gold and two items, one of them gray. | One claimed row per item and one claimed gold row, `source=KILL`. The gray item shows only after Quality > Poor is selected. | |
| LED-P2-05 | Drink 3 potions in one pull. Do a second pull within 60 s. | No hitch during the pull. After combat, exactly one `OUT CONSUME` row with quantity 3. The second pull amends that row rather than adding one. | |
| LED-P2-06 | Send items and gold to an alt. Log the alt in and take the mail. | `OUT ALT_MAIL` rows on the sender and a gold `OUT MAIL_SEND` for postage. `IN ALT_MAIL` rows on the alt, with no `⇄` and no second loss. | |
| LED-P2-07 | Take a mail from another player and an auction you won. | `IN MAIL` and `IN AH`, chat-claimed when a loot line fires. | |
| LED-P2-08 | Post one item and one commodity on the auction house. | A `⇄` to `me/auctions` for each, and gold `OUT AH_POST_FEE`. | |
| LED-P2-09 | Cancel one auction and take the return. Let another sell and take the money. | The cancel return is a `⇄`. The sale gives item `OUT AH_SOLD` and gold `IN AH_SOLD`. | |
| LED-P2-10 | At a guild bank, deposit and withdraw an item and some gold. | `OUT GUILD_DEPOSIT` and `IN GUILD_WITHDRAW`. | |
| LED-P2-11 | Craft 5 of a recipe. | The reagents as `OUT CRAFT_REAGENT` rows and the product as `IN CRAFT`. | |
| LED-P2-12 | Disenchant one item. | The item as `OUT DECONSTRUCT` and the materials as `IN DISENCHANT`. | |
| LED-P2-13 | Transfer a transferable currency to an alt, then log the alt in. | `OUT CURRENCY_TRANSFER` on you and `IN CURRENCY_TRANSFER` on the alt (to `Alt/currency`, one shared `pairId`). Any fee as `OUT TRANSFER`. No `UNTRACKED` row for it on the alt's next login. | |
| LED-P2-14 | Spend crests on an upgrade and currency at a vendor. If a reason is wrong, `/dump Enum.CurrencySource` and `/dump Enum.CurrencyDestroyReason`. | `OUT` rows with mapped reasons, not `OTHER`. | |
| LED-P2-15 | Disable the addon, log in, move items about, re-enable it and `/reload`. Also log in a brand-new character. | `UNTRACKED` rows for the differences. The new character's first login writes none. | |
| LED-P2-16 | `/lh disable`, loot something, `/lh enable`. | The loot appears as `UNTRACKED` about one second after enabling. | |
| LED-P2-17 | Look at History. Tick **Show transfers by default**, then **Clear**. Try Group by Direction and by Holder. | ▲ ▼ ⇄ render in the mono face (no boxes), colored green, red and gray. Qty reads `+3` / `-3`. Gold rows are pale gold. Direction defaults to Gains + Losses, and after the tick, Clear includes transfers. Both groupings work. | |
| LED-P2-18 | Open Insights with losses in range. Use a range before the upgrade date with kept history. | Gained, Lost, Net and Transfers cards, and the "Gains vs losses by reason / character / kind" charts above LOOT. Under the default filter, Transfers reads 0. The yellow pre-ledger caveat shows for the early range. | |
| LED-P2-19 | Export the History CSV and the Insights CSV with losses in range. | The History CSV ends `...,wowheadLink,dir,kind,holder,from,to`, and legacy rows read `IN,ITEM,<char>,,`. The Insights CSV ends with `Ledger` sections. | |
| LED-P2-20 | `/lh perf`. Complete both arms on a training dummy with a loot-heavy pull, then `/lh perf finish`. Record it with `/dev-copilot:wow-perf-analysis`. | The step panel opens. The report's `lootLine`, `spellCast` and `ledgerEvent` buckets are non-zero. | |
| LED-P2-21 | Train a skill and take a flight. | Gold `OUT TRAINING` and `OUT TRAVEL`. | |
| LED-P2-22 | In a group, loot gold that is split. With guild perks, note the `YOU_LOOT_MONEY_GUILD` amount. | "Your share of the loot is ..." is parsed and claimed. Record whether the guild amount is the pre-cut or post-cut figure (pre-cut is a known limitation). | |
| LED-P2-23 | Trade an item and gold to another player. | `OUT TRADE_GIVE` rows. | |
| LED-P2-24 | Delete an item from your bags. | `OUT DESTROY`. | |

## MultiMeters

| Item | What to do | Expected result | Result |
|---|---|---|---|
| MM-01 | With Merge pets ticked, on a pet class (hunter or warlock) whose pet out-damages you, fight, then check Current and Overall and run `/mm export`. | Your row's Damage Done equals your damage plus your pet's (compare against Blizzard's meter), on Current and Overall, and the export shows the same number. | |
| MM-04 | Rename a window `Raid` to `raid` from the Windows page, and again with `/mm window rename` or the panel name field. | The title shows `raid`, not `raid 2`. | |
| MM-06 | Open a drill-down on a window, right-click to go back, and switch views a few times. | No stray Back button appears and the window renders normally. | |

## PanelMaster

| Item | What to do | Expected result | Result |
|---|---|---|---|
| PM-01 | Run `/pm delete all` (or Delete all on the Panels page). Answer No, then repeat and answer Yes. Log in an alt on the same profile. | The confirmation names the current profile (for example `Default`) and says every character on it loses its panels. No keeps the panels. Yes removes them, and the alt has none after login. | |
| PM-02 | Untick Lock frame and open the debug console. Run Reset all settings and accept. Create a new panel. | Panels lock (no drag handles or labels), the console closes, and the Profiles list is unchanged. The new panel is locked. | |
| PM-03 | In the Panels page editor, press Delete and answer No, then Yes. On another panel, press Reset and answer No, then Yes. | Delete asks `Delete the panel "<name>"?`. No keeps it and Yes removes it. Reset asks, naming the panel. No keeps size and colors. Yes restores defaults and keeps the name and frame name. | |
| PM-04 | In combat at a target dummy, untick Lock frame (a queued message appears), then `/pm disable`, `/pm enable` and leave combat. Repeat without the disable and enable. | With the disable and enable, panels stay locked after combat. Without them, panels unlock on leaving combat, as before. | |
| PM-05 | Run LOC-1, LOC-2, LOC-3 and LOC-5 in PanelMaster's `docs/smoke-tests.md`: `/pm new Übersicht`, `/pm new Ärger`, `/pm new Örger`, `/pm new übersicht`, `/pm panel übersicht`, and a pasted Cyrillic or CJK name created twice. `/reload` and do a profile round trip. | Übersicht gets its own frame name. Ärger and Örger make two panels. `übersicht` is refused as a duplicate, and `/pm panel übersicht` finds Übersicht. The Cyrillic or CJK name can be created twice with different names. Everything survives `/reload` and the round trip. | |
| PM-06 | NUM-3: run `/pm panel <name> set x nan` and `set width 1e999`, then `/reload`. If an older SavedVariables holds a non-finite value, run `/pm recover` twice. | Both are refused with `expected a number`, and the panel is where it was after `/reload`. The first `/pm recover` fixes the bad value and the second reports nothing moved. | |

## PartyFrameEnhanced

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-PF | INSTALL-4 in PartyFrameEnhanced's `docs/smoke-tests.md`: load on v1.71.0, then `/pfe status` and `/pfe unlock`. | The addon loads clean with no Lua errors, and both commands work. | |
| PF-01 | Out of combat, run `/pfe profile new <fresh name>`. | One `Created and switched to new profile` line, no reset line, and the frames rebuild once. | |
| PF-02 | In combat, run `/pfe profile copy <a profile saved unlocked>`. After combat, run `/pfe unlock`. | Elements stay locked, the combat re-lock line prints, and no `Preview cast` placeholders appear for the rest of the fight. After combat, unlock works. | |
| PF-03 | In a party and in combat, disable the addon (`/pfe disable` or the Enabled toggle), then leave combat. Run `/pfe diag`. | Party frames return to their default positions and visibility within a second, with no Lua error. The diagnostics show no pending writes and the listener not armed. | |
| PF-04 | `/pfe unlock`, then `/pfe status`. | The Note line shows `unlocked (stand-in)` or `unlocked (your party frames)` once, with no second bare `unlocked`. | |

## PrettyChat

| Item | What to do | Expected result | Result |
|---|---|---|---|
| RV-PC | `/reload` with PrettyChat enabled. Run `/pc config` and open General, Categories and Profiles. Run `/pc test`. | No Lua errors. All three pages open and the preview prints. | |
| PC-01 | `/pc config` > Categories > Loot. Clear one message's New box and press Enter. Run `/pc test`. | The empty value is refused with a message, and `/pc test` still prints that message formatted, not blank. | |
| PC-03 | Press the Categories page header Defaults and answer No, then repeat and answer Yes. Then use the Settings window footer Defaults on the Categories page. | The header Defaults asks first. No keeps edits and Yes resets every tab. The footer Defaults asks once (Blizzard's dialog) and resets with no second popup. | |
| PC-04 | Run `/pc test category General`, then `/pc test category Loot`. | General prints the unknown-category message with a Valid list that starts at Loot. Loot still previews. | |

## WhatGroup

| Item | What to do | Expected result | Result |
|---|---|---|---|
| WG-01 | S-001: in combat at a target dummy, get invited to and join a Mythic+ group listed with a teleport you have learned that is on cooldown. Wait until combat ends and the cooldown runs out. | No Lua error. The chat notice prints in full, including the Teleport row. The popup appears after combat, its cooldown note keeps showing and counts down out of combat, and the button becomes usable when the cooldown ends. | |
| WG-02 | Join or capture a real group, then run `/wg test notify` and separately press the panel Test button. Close the popup and run `/wg show`, then click the chat details link. Then `/wg disable`, press Test, and `/wg enable`. | The sample notice and popup appear. `/wg show` and the link open the real group, not `Test Group`. While disabled, Test gives a chat preview only with no popup. After enable, no popup appears unasked. | |
| WG-04 | Open the settings panel, Popup > Layout, and hover Height. | The tooltip reads `Height of the group-info popup, in pixels.` and states no default. | |

## Owner session 2026-10-07: minimal set

The owner ran the minimal set below on the feature-branch build (LibKa0s v1.71.0 payload in every addon)
and reported **all pass** on 2026-10-07. Rows in the per-addon tables above that are not listed here were
not run; their Result cells stay blank.

| Check | Rows covered | Result |
|---|---|---|
| Load all addons, open every settings panel | RV-AT, RV-AM, RV-BL, RV-CM, RV-PF, RV-PC, LK-12 | pass |
| BankLedger search suggestions | LK-04 | pass |
| LootHistory Timeline hover + resize | LK-03 | pass |
| MultiMeters pet merge vs Blizzard meter | MM-01 | pass |
| LootHistory records loot after a PrettyChat change | LH-01 | pass |
| Deleted KCM_ macro recreated on resync | CM-01 | pass |
| Devourer DH stat priority | CM-02 | pass |
| PanelMaster delete-all prompt names the profile | PM-01 | pass |
| KickCD cast bar with an empty icon grid | KC-01 | pass |
| WhatGroup M+ teleport cooldown in combat | WG-01 | pass |
| PartyFrameEnhanced disable in combat | PF-03 | pass |
| AbsorbTracker enable in combat after unlock | AT-07 | pass |
| KickCD glow on a friendly cast | KC-03 | pass |
| PrettyChat Categories Defaults prompts | PC-03 | pass |

Deferred: LED-P2-01..24 (LootHistory 1.4.0 release gate) and every unlisted row.

---

# Sign-off

The owner fills this in as each session runs, and nobody else does. Put failing row ids and the exact
chat text in Notes.

| Session | Date | Build / tag | Tested? | Pass/Fail | Failing rows and notes |
|---|---|---|---|---|---|
| LibKa0s v1.71.0 | | | | | |
| AbsorbTracker | | | | | |
| AuraMaster | | | | | |
| BankLedger | | | | | |
| ConsumableMaster | | | | | |
| KickCD | | | | | |
| LootHistory | | | | | |
| LootHistory LED-P2 (LH-R-03) | | | | | |
| MultiMeters | | | | | |
| PanelMaster | | | | | |
| PartyFrameEnhanced | | | | | |
| PrettyChat | | | | | |
| WhatGroup | | | | | |
