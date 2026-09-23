# 06 — Smoke Tests

**The in-client checklist for the 2026-09-23 remediation: every work item with a non-empty `smoke`
field, batched into as few logins as possible.**

> **Nothing below has been performed.** No step here has been run against a client while this bundle
> was being produced, and none of the work it checks exists yet. Each step describes a check on a change
> still to be made.

Sources: `plan-data/items.json` (168 items with a smoke field, reconcile results and plan-review
amendments included), `plan-data/PLAN_REVIEW_RESOLUTIONS.md` (the minimap rename needs no
SavedVariables migration, so every rename carries one upgrade carry-over check instead), and the
LibKa0s review's `LibKa0s/docs/reviews/2026-09-23/03_SMOKE_TESTS.md` (S-001 … S-008), which
LK-33 names as its pre-merge gate.

---

## What is not here

Each item's own `verify` field already covers the four out-of-game suites (`luacheck`, the headless
harness, `tests/perf.lua`, `lizard`). None of that is repeated. This document covers what a headless
suite cannot see: rendering, taint, the Blizzard options list, SavedVariables as the client really wrote
them at logout, event order on a live client, library-absent loads, and several addons sharing one
LibStub and AceGUI registry in the same session.

Each addon's own `docs/smoke-tests.md` is the standing pass. Where an item names one of its sections
(C-01, SM-04, §6a, S-003 and so on), the step here says only what has changed. Run that section
alongside it.

## Conventions

- **`/reload`** means `/console reloadui`.
- **Errors.** Run `/console scriptErrors 1` once and keep BugSack/BugGrabber on. "No Lua error" means
  nothing reaches BugSack or the error frame at any point during the step, including on `/reload`.
- **Taint** means any "Interface action failed because of an AddOn", `ADDON_ACTION_BLOCKED` or
  `ADDON_ACTION_FORBIDDEN`. It is a failure even when nothing visible breaks.
- **"In combat"** means hitting a training dummy. The gates read `PLAYER_REGEN_DISABLED` / `_ENABLED`.
- **Refusal line.** The collection's one disabled line is
  `<Brand> is disabled — enable it with /<slash> enable`. The library-absent line is
  `/<slash> <verb> is unavailable: the LibKa0s library did not load.` A second wording, a doubled
  line or a missing bracketed prefix is a failure in its own right.
- **SavedVariables inspection** means log out (not `/reload`), then open
  `WTF/Account/<ACCOUNT>/SavedVariables/<Addon>.lua` in a text editor. Only a logout writes the file.
- **Pass / Fail.** Each step gives an observable pass condition and what failure looks like. If a step
  fails, record the item id, the step and the exact chat text in the sign-off table at the end, and
  stop that addon's session unless the next step does not depend on it.
- **Slash roots:** `/at` AbsorbTracker, `/am` AuraMaster, `/bl` BankLedger, `/cm` ConsumableMaster,
  `/kcd` KickCD, `/lh` LootHistory, `/mm` MultiMeters, `/pm` PanelMaster, `/pc` PrettyChat,
  `/pfe` PartyFrameEnhanced, `/wg` WhatGroup.

### Two facts about LibStub that shape the sessions

1. **One vendored copy upgrades everyone.** LibStub keeps the highest minor of each library that any
   loaded addon ships. Copying the v1.56.0 payload into a single consumer's `libs/LibKa0s/` is enough
   for every loaded Ka0s addon to run the new library files. That is why LK-33 names one consumer, and
   why Session L works on a scratch copy of the AddOns folder.
2. **A library-absent test must remove every copy.** Renaming one addon's `libs/LibKa0s` proves nothing
   while any other loaded addon still ships LibKa0s, because LibStub hands the degraded addon the other
   copy. Every library-absent step is therefore collected into **Session X2**: rename `libs/LibKa0s` in
   every Ka0s addon at once (or disable the ones not under test), then restart the client. Renames and
   restores are file-system changes, so do them with the game closed.

## Session index

| Session | Milestone | Run when | Needs | Logins | Rough time |
|---|---|---|---|---|---|
| **P — pre-coding observations and fixtures** | before M2 | before any M2 pre-re-vendor fix or M3 item lands, on the shipped (v1.55.0-payload) builds | a training dummy, a guild vault, one LFG application, all eleven addons | 2 (one mid-session logout) | 40 min |
| **L — LibKa0s v1.56.0 pre-merge gate** | M1 | after LK-33 cuts the **local** tag, before the owner approves the push | a scratch copy of the AddOns folder with the payload in one consumer | 1 (+1 optional ruRU) | 35 min |
| M2 | M2 | — (BL-01 and WG-01 are checked in Sessions BL and WG) | — | **0** | — |
| **BL … KC — one per addon** | M3 | after that addon's last item and its `-DOCS` item | varies, see each header | 1 each; MM, LH and AM need 2 (14 total) | 15–40 min each |
| **Q — group content night** | M3 | after every M3 addon item has landed, **before any addon branch is merged** (LH-02 is a pre-merge checkpoint) | a Mythic+ key or dungeon, a raid or raid dummy, LFG, an Evoker if available | 1–2 | 90 min |
| **X1 — LibKa0s v1.56.0 across the collection (library present)** | M3 | after all eleven addon sessions | all eleven addons, a cold item cache | 1 | 35 min |
| **X2 — LibKa0s absent, every addon at once (includes WhatGroup's degraded verbs)** | M3 | straight after X1 | every `libs/LibKa0s` renamed, then restored | 1 (+1 restart to restore) | 25 min |
| **X-ru — Media font on ruRU** | M1/M3 | optional, whenever a ruRU client is available | a ruRU client locale | 1 | 5 min |
| M4 | M4 | — (owner-gated `/wow-addon:revendor-standards` items; none has a smoke field) | — | **0** | — |

**About 22 logins in total:** P 2, L 1, the addon sessions 14, Q 1–2, X1 1, X2 2 (one degraded, one
to confirm the restore), X-ru 1 if a ruRU client is available. P, the addon sessions and X2 log out on
purpose because a logout is the only way to see what the client wrote to SavedVariables.

Every item with a smoke field appears in at least one step heading that carries its id. An item with a before and an after half (BL-07, PC-11, MM-20, MM-21, AM-08),
an upgrade and a live half (the minimap renames), or a live and a library-absent half (PF-11, WG-12)
appears in more than one. The LibKa0s items reappear in X1 as cross-collection re-checks. The coverage
table at the end maps every id to all of its steps.

---

# Session P — pre-coding observations and fixtures

**Run on the shipped builds, before M2 starts.** M2 lands the pre-re-vendor fixes (AT-01, AM-01,
AM-02, BL-01, BL-02, CM-01, KC-01, WG-01) and then the re-vendors, so after it no addon runs its shipped
build any more. Several items choose their fix from what the live client does (BL-07, WG-07, MM-21),
two need a "before" perf capture to compare against (MM-20, AM-08), and one needs a "before" text
capture (PC-11). The same session also records the **upgrade fixture**: SavedVariables written by the
*old* builds, which every addon session later restores to prove that the update keeps an existing
player's settings.

Needs: all eleven addons on their shipped builds, a training dummy (the raid dummies in a capital city
for AM-08), access to a guild vault, and one LFG application you can let time out.

### P.1 · BL-07 step 1 — which events a guild vault really fires

- **Setup:** BankLedger current build. Stand at a guild vault.
- **Do:** `/etrace`, filter to `GUILDBANK` and `PLAYER_INTERACTION_MANAGER`. Open the vault, deposit
  nothing, close it.
- **Pass (record, not judge):** write down every event that fired on open and close, with its
  arguments. `PLAYER_INTERACTION_MANAGER_FRAME_SHOW`/`_HIDE` with the guild-banker type, or
  `GUILDBANKFRAME_OPENED`/`_CLOSED`, decides BL-07's branch. Paste the list into BL-07's commit body.
- **Fail:** no trace captured. Do not code BL-07 until it is.

### P.2 · WG-07 (S-008) — the terminal LFG status strings

- **Setup:** WhatGroup current build. `/etrace` filtered to `LFG_LIST_APPLICATION_STATUS_UPDATED`.
- **Do:** apply to one listing and let it time out. Apply to another, get invited and decline the
  invite. If possible, produce a `failed` status as well.
- **Pass (record):** the exact `newStatus` strings (expected: `timedout`, `invitedeclined`, `failed`)
  are written down for WG-07's commit body.
- **Fail:** a string differs from the three the item codes against. Stop and amend WG-07 first.

### P.3 · PC-11 (SMK-C09) before — the `/pc test` order

- **Do:** `/pc test`, open the debug console, Copy, and save the text as `pc-test-before.txt`.
- **Pass:** the file exists. The after half is PC-11 in Session PC.

### P.4 · MM-20 (SM-07) and AM-08 before captures

- **Setup:** MultiMeters and AuraMaster current builds. For AM-08, set one container to "only auras
  without a duration" and turn nameplates on.
- **Do:** MultiMeters: `/mm perf` start, a dungeon pull (or a solo dummy fight of at least 60 s, which
  must then be reused for the after capture), `/mm perf finish`. AuraMaster: `/am perf` capture, a
  2-minute session on the raid target dummies, finish.
- **Pass:** each report and JSON dump is recorded with `/wow-addon:perf-analysis` into that repo's
  `docs/perf-analysis/<stamp>/` as the **before** bundle. Note the content used, because the after
  capture must match it.
- **Fail:** no JSON line, or a Lua error during capture. Record it; without a before bundle, MM-20's
  acceptance cannot be judged.

### P.5 · Fixtures for the upgrade checks (every minimap rename, and the migrations)

The eleven minimap renames (AT-12, AM-14, BL-12, CM-19, KC-17, LH-13, MM-16, PM-11, PC-13, PF-13,
WG-11) and three migrations (MM-13, PC-04, AM-10) are only honest if they run against a store the old
build wrote. The renames move only the CLI path (`…minimap.hide` → `…minimap.shown`). The stored key
stays LibDBIcon's `global.minimap.hide`, so there is no SavedVariables migration and no schema-version
bump. Each addon session instead opens with the same **upgrade carry-over check**: the button hidden
here stays hidden, `/<slash> get …minimap.shown` prints `false`, and the stored `minimap` table holds
only `hide` (plus `minimapPos` if the button was ever dragged), never a `shown` key.

- **Do, in each of the eleven addons:** untick Master controls → Minimap button (or right-click the
  LibDBIcon button and hide it). The button is gone.
- **MultiMeters (MM-13):** collapse one window with its minimize control.
- **PrettyChat (PC-04):** on the Loot category, set a custom format for `LOOT_ITEM_CREATED_SELF`.
- **MultiMeters (MM-21, SM-06):** fight a dummy so the meter has data.
- Log out. **Copy** `WTF/Account/<ACCOUNT>/SavedVariables/` to `WTF-fixture-P/` outside the game
  folder. Also keep a second, untouched backup of the whole `WTF/`.
- **Pass:** `WTF-fixture-P/` holds eleven addon files, and each shows its minimap `hide = true` and
  no `shown` key.
- **Fail:** a file shows no `hide = true`, so the button was not hidden in that addon. Redo it for that
  addon.

### P.6 · MM-21 (SM-06) — does the roster survive a real logout?

- **Do:** log back in (this is the session's second login) and open the MultiMeters window.
- **Pass (record):** write down whether the meter still has the pre-logout fight's data. Yes means
  branch A, no means branch B. That picks MM-21's branch.

LH-02's event-order question is answered in Session Q, before the LootHistory branch merges.

---

# M1 — Session L: the LibKa0s v1.56.0 pre-merge gate

**Run after LK-33 has cut the local `v1.56.0` tag and before the owner approves the push.** This is
LK-33's own smoke: install the payload into one consumer and run S-001 … S-008 from
`LibKa0s/docs/reviews/2026-09-23/03_SMOKE_TESTS.md`, which this session includes step for step.

The tag also carries LK-03 (the AceDB fake's fidelity change in `tests/_kit/`), which is headless
only and has no step here. M1's other two repositories have nothing in-client. WowAddonStandards is
documentation. The one
wow-addon item with a smoke field (WA-02) runs in a terminal and is listed under "Not in-client" at the
end.

**Setup.** With the game closed, make a scratch copy of `Interface/AddOns/`. Into
`AuraMaster/libs/LibKa0s/` of the **scratch copy** (not the repository), copy `LibKa0s/LibKa0s/`
whole from the local tag. Per the LibStub note above, every loaded Ka0s addon now runs v1.56.0.
No host has adopted anything yet, so steps that need a host descriptor change (LK-11's [Init] listing,
LK-16, LK-17, LK-25, the AuraMaster half of LK-28) are only checked for "no regression" here. Their
full check is in the addon sessions and in X1. Confirm the load:
`/run print(LibStub.minors["LibKa0s-Item-1.0"], LibStub.minors["LibKa0s-Media-1.0"])` prints `2 4`.

### L.1 · LK-33 — load and regression pass

- **Do:** log in with all eleven addons, `/reload` twice, open Settings → AddOns, type each of the
  eleven slash roots once.
- **Pass:** no Lua error. Each addon appears once in the AddOns list and each slash root reaches its
  own addon.
- **Fail:** any error naming `libs/LibKa0s/`. That blocks the tag push.

### L.2 · LK-11 — the registration helper does not regress a consumer

- **Do:** `/reload` with every consumer loaded.
- **Pass:** no Lua error at load, and every addon still reacts to its events (a meter counts, a cast
  bar fills). The "[Init] lists zero rejected events" half is checked per addon after adoption (AT-07,
  AM-07, BL-06, CM-15, KC-04, LH-17, MM-07, PC-12, WG-06).
- **Fail:** an addon goes silent after `/reload`.

### L.3 · LK-10 (S-007) — a secret value in a numeric specifier

- **Setup:** in combat against a dummy, with an absorb shield on yourself.
- **Do:** `/run local P=LibStub("LibKa0s-Core-1.0"):New{prefix="[t]"} P.Format("absorb=%d", UnitGetTotalAbsorbs("player"))`.
  Then, with `/at debug on`, let AbsorbTracker log a combat value.
- **Pass:** one chat line (`[t] absorb=%d <secret>` in combat, a number out of combat) and no Lua error.
- **Fail:** "bad argument #2 to 'format'" or any error from `Core.lua`.

### L.4 · LK-12 (S-001) — `|cnIQ` item quality

- **Do:** `/run local l=select(2,C_Item.GetItemInfo(6948)) or "" print((l:gsub("|","||")))`, then
  `/run print(LibStub("LibKa0s-Item-1.0").QualityFromLink(select(2,C_Item.GetItemInfo(6948))))`.
- **Pass:** the first prints a link starting `||cnIQ1`, and the second prints `1`.
- **Fail:** the second prints `nil`. The consumer halves (the LootHistory row colour and the BankLedger
  row) are in X1.1.

### L.5 · LK-13 (S-004, enUS half) — JetBrains Mono registers and counts

- **Do:** `/run print(LibStub("LibSharedMedia-3.0"):IsValid("font","JetBrains Mono"))`, then open any
  Ka0s debug console and any consumer's font dropdown.
- **Pass:** `true`. The console renders in JetBrains Mono and the face is listed in the dropdown.
- **Fail:** `false`, or the console falls back to a default face. The ruRU half is Session X-ru.

### L.6 · LK-14 (S-005) — the Bus survives an AceEvent re-embed

- **Setup:** AbsorbTracker loaded, in a group (a follower dungeon party works).
- **Do:** `/run local E=LibStub("AceEvent-3.0") for t in pairs(E.embeds) do E:Embed(t) end`, then
  `/at disable`, `/etrace` for `UNIT_AURA` for 10 s, then `/at enable`.
- **Pass:** while disabled, no AbsorbTracker handler runs and the bars are gone. After enable, the bars
  return and update.
- **Fail:** a bar repaints while disabled, or stays dead after enable.

### L.7 · LK-19 (S-008 console) — batched buffer trim

- **Do:** `/mm debug on`, generate more than 1600 lines (repeat `/mm perf report`, or a debug scan in a
  loop), open the console and press Copy.
- **Pass:** the copy window holds the newest 1500 lines in order, with the oldest dropped. The client
  does not stall while lines arrive.
- **Fail:** the count is wrong, lines are out of order, or there is a visible hitch per line at the cap.

### L.8 · LK-20 (S-008 perf) — perf fields and depth reset

- **Do:** `/mm perf start`, `measure a`, a dummy pull, `measure b`, a pull, `finish`, `report`. Repeat
  once with `/kcd perf start` … `/kcd perf finish`.
- **Pass:** the report and JSON line print, each bucket names its correct parent, the addon is restored
  after `finish`, and there is no Lua error.
- **Fail:** a bucket nested under the wrong parent, a `nil` label, or an error at a window edge.

### L.9 · LK-21 (S-008 drag) — ReorderList ghost frame and pooled drop line

- **Do:** ConsumableMaster → Category priority list: drag a row two places down. KickCD → Spells: drag
  a row up. MultiMeters → Columns: drag a column block.
- **Pass:** the ghost follows the cursor, the drop line draws in each list's own colour, the order
  saves, and a second list's drag draws its own line.
- **Fail:** a line in the wrong colour, a line left behind after the drop, a row left hidden, or
  stutter that continues after the drop (an `OnUpdate` left armed).

### L.10 · LK-24 — font preload moved (behaviour-neutral)

- **Do:** open any settings page with a font dropdown (MultiMeters → Appearance) and open the dropdown.
- **Pass:** each font name renders in its own face, as before.
- **Fail:** all entries render in the default face.

### L.11 · LK-26 — slider and colour throttles

- **Do:** `/kcd debug on`. Drag the cast-bar colour picker for about 3 s, then a slider for about 3 s.
- **Pass:** the console shows commits at about 20 per second, not one per frame.
- **Fail:** one commit per frame (60+ per second), or no commit until release.

### L.12 · LK-27 (S-002) — OptionsTabs stop leaking a widget per render

- **Do:** `/run UpdateAddOnMemoryUsage() print(GetAddOnMemoryUsage("MultiMeters"))`. `/mm config` →
  Windows, switch the window picker 30 times, and print the figure again. On AuraMaster, switch between
  banner pages 50 times, then `/dump collectgarbage('count')`. On AbsorbTracker → Appearance, switch
  the unit picker 30 times and `/fstack` over the chrome band.
- **Pass:** memory is within a few KB of the first reading, with no climb per switch. `/framestack`
  over a banner shows exactly one Dropdown under the chrome band, and the divider hairline is drawn once.
- **Fail:** memory grows with every switch, a second Dropdown sits under the band, or an error mentions
  `SetParent` or `Release`.

### L.13 · LK-28 (first half) — RenderTabbedSchema moved, strips unchanged

- **Do:** open every tabbed settings page in every consumer, switch each strip's tabs, and select a
  picker entry that removes the current tab (a stale tab).
- **Pass:** every strip draws and switches as before, and a stale tab heals to the first tab. The
  AuraMaster adoption half is AM-17.
- **Fail:** a blank page, a missing strip, or an error from `OptionsTabs.lua`.

### L.14 · The rest of 03_SMOKE_TESTS.md

- **Do:** the review's "Regression suite" and "Taint" sections, on two consumers.
- **Pass:** as written there. **Fail:** any taint line, any page drawn in combat.
- S-003 and S-006 need adopted hosts. They are checked in MM-09 and BL-08, and across the collection
  in X1.3 and X1.4.

**Gate:** record L.1 … L.14 in the sign-off table. The owner approves the push only when all pass.

---

# M2 — nothing in-client of its own

M2 holds the pre-re-vendor fixes (AT-01, AM-01, AM-02, BL-01, BL-02, CM-01, KC-01, WG-01), which land
ahead of their addon's re-vendor and must pass headless on both the v1.55.0 payload and the v1.56.0 dry
run, and then the re-vendors themselves (RV-AT … RV-WG).

No re-vendor has a smoke field. Each is a copy-only commit whose proof is the addon's headless suite
plus the `docs/revendor/2026-09-23-v1.56.0/` bundle it writes by hand from the local
`wow-addon/commands/revendor-libka0s.md`, and by LibStub note 1 the payload has already run in a client
in Session L. The first in-client check of each re-vendor is the start of its addon's M3 session.

Two pre-re-vendor fixes do carry a smoke field: BL-01 (the retention prune, C-07) and WG-01 (the
SetItemRef callback). Neither needs a login of its own. Their checks are BL.16 and WG.7, run in the
BankLedger and WhatGroup sessions on the finished branch, which still contains the fix. The other six
pre-re-vendor fixes have no smoke field.

---

# M3 — one session per addon

Each addon session follows the same order:

1. **Upgrade block** (game closed): back up the live `SavedVariables/<Addon>.lua`, copy that addon's
   file in from `WTF-fixture-P/`, then log in. This is what an existing player experiences on update.
   Every session's first step is the minimap **carry-over check** from P.5: the hidden button stays
   hidden, `/<slash> get …minimap.shown` prints `false`, and `/dump <Addon>DB.global.minimap` shows
   only `hide = true` (plus `minimapPos`), with no `shown` key.
2. **Live checks**, out of combat, then in combat.
3. **Logout and SavedVariables inspection.**
4. Where the `-DOCS` item has a smoke field, that item: its full `docs/smoke-tests.md` pass. It is listed
   last and can move to a separate login at the owner's convenience.

Library-absent steps are in X2, and group-content steps are in Q. Each session says which of its items
went there.

---

## Session BL — BankLedger

**Run after BL-DOCS.** Needs: a bank, a guild vault, a training dummy, an epic item this character has
not handled this session, and ledger rows older than a few days. One login, about 35 minutes.
Elsewhere: BL-10 → X2. The cross-addon cold-cache and refusal checks → X1.

### BL.1 · BL-12 upgrade — a hidden button stays hidden, and BL-11 stamps v2

- **Setup:** game closed. Back up `BankLedger.lua` and copy it in from `WTF-fixture-P/`. Log in.
- **Do:** look for the minimap button. `/bl get minimap.shown`. `/dump BankLedgerDB.global.minimap`.
  `/bl debug on`, `/reload`, and read the `[Init]` line.
- **Pass:** the button is still hidden. The get prints `false`. The dump shows only `hide = true` (and
  `minimapPos` if the button was ever dragged), with no `shown` key. `[Init]` reads `schema v2`. The
  ledger history from before the update is all there.
- **Fail:** the button reappeared (the rename lost the stored `hide`), the get prints `true`, a `shown`
  key is stored, `[Init]` names another version, or history rows are missing.

### BL.2 · BL-DOCS — LK-12 on a cold cache

Run it now, while the item cache is still cold from the fresh login.

- **Setup:** Settings → General quality threshold at **Epic**. An epic in the bags that you have not
  hovered or linked this session.
- **Do:** open the bank and deposit it. Open History.
- **Pass:** the row is recorded, and its quality shows epic (purple), read from the `|cnIQ4` link.
- **Fail:** no row (the threshold read the quality as nil or Poor), or the row is grey or white.

### BL.3 · BL-12 — the minimap row reads in its own sense

- **Do:** `/bl set minimap.shown true` (the button returns). `/bl get minimap.shown`.
  `/bl set minimap.shown false`, then `/reload`. Right-click the LibDBIcon menu (or the checkbox) to
  show it again, then `/bl get minimap.shown`.
- **Pass:** `true` → hidden → still hidden after reload → shown → `true`.
- **Fail:** `/bl set minimap.hide …` still works (the old path must answer "unknown setting"), or the
  get disagrees with what is on screen.

### BL.4 · BL-16 — the load-bearing TOC positions

- **Do:** `/reload`. Open Insights. `/bl list`.
- **Pass:** no Lua error, the Insights charts render, and `/bl list` prints the rows.
- **Fail:** an error at load naming `Insights` or `Slash`, or an empty chart area.

### BL.5 · BL-06 — one event record

- **Do:** `/reload`, then `/bl debug scan`. Then `/bl disable` and `/bl debug scan` again. Then `/bl enable`.
- **Pass:** "events registered" lists the bank, bag, money and guild set plus `PLAYER_ENTERING_WORLD`
  and the combat pair, followed by `events UNAVAILABLE (0): none`. After disable, the record is empty.
- **Fail:** an unavailable count above 0 on a current client, or registrations that survive the disable.

### BL.6 · BL-08 — the launcher refusal (the LK-16 consumer)

- **Do:** `/bl disable`, left-click the minimap button, then right-click it. `/bl enable`, left-click twice.
- **Pass:** exactly one line, `Ka0s Bank Ledger is disabled — enable it with /bl enable`, and the
  ledger does not open. Right-click opens settings. Once enabled, left-click toggles the ledger.
- **Fail:** the ledger opens while disabled, two lines print, or the wording differs.

### BL.7 · BL-18 — the brand is spelled once

- **Do:** hover the minimap button. Open Esc → Options → AddOns.
- **Pass:** the tooltip title reads `Ka0s Bank Ledger`, and the AddOns list shows `Ka0s Bank Ledger` once.
- **Fail:** a different spelling in either place, or two entries.

### BL.8 · BL-09 — `/bl set` prints the seam's refusal (the LK-17 consumer)

- **Do:** `/bl get settings.visibility`, `/bl set settings.visibility bogus`, then
  `/bl get settings.visibility` again.
- **Pass:** an `Invalid value for settings.visibility` line with the reason indented beneath it, and
  both gets print the same value.
- **Fail:** `settings.visibility = <old value>` is echoed as if the write succeeded, or the value changed.

### BL.9 · BL-17 — printer call sites

- **Do:** right-click a ledger row → Blacklist item. Then `/bl test`, and `/bl test` again to turn it off.
- **Pass:** one line naming the item (a clickable link, not a raw `|H` string). `/bl test` prints
  `test mode on`.
- **Fail:** a doubled prefix, raw escape codes, or a `%s` left in the text.

### BL.10 · BL-21 — `docs/debug.md` matches the client

- **Do:** `/bl debug scan` and `/bl debug panel`, with `docs/debug.md` open beside the client.
- **Pass:** every section and field the doc describes appears in the output, in the same order.
- **Fail:** a field in the doc that the client does not print, or the reverse.

### BL.11 · BL-20 — the in-client half of the citation sweep

- **Do:** open the debug console, press Copy, then close the copy window with its close button.
- **Pass:** the close button is the library's (the same chrome as other Ka0s copy windows), and it
  closes the window. The desk-check half is under "Not in-client".
- **Fail:** a second, BankLedger-specific close control, or one that does nothing.

### BL.12 · BL-03 — stand-down drops the capture context (C-01)

- **Case A — Do:** at the bank, `/bl disable`, deposit a stack, `/bl enable`, move nothing, close the bank.
- **Pass A:** no row appears for the deposit.
- **Case B — Do:** at the bank, `/bl disable`, close the bank, walk away, `/bl enable`, `/bl debug scan`.
- **Pass B:** the scan shows no open context, and the session window is closed.
- **Fail:** in A, the deposit is recorded on enable. In B, a stale open context or a session window
  that is still open.

### BL.13 · BL-04 — Reset all re-runs the enable latch (C-02)

- **Do:** open History and Insights. Master controls → Reset all settings → Yes. Then `/bl disable`,
  Reset all settings → Yes, and deposit a stack at the bank.
- **Pass:** both views empty at once, and the storage read-out reads 0. After the second reset the
  addon is enabled and the deposit records.
- **Fail:** a view still shows rows until reopened, or the addon stays disabled after the reset.

### BL.14 · BL-05 — one global reset, one popup

- **Do:** open the debug console, then try each door in turn: `/bl resetall`, the General page
  Defaults, the Blizzard footer Defaults, and Master controls → Reset all settings. Answer No to the
  first three and Yes to the fourth. Hide the minimap button before the Yes.
- **Pass:** all four raise the **same** popup. No leaves everything as it was. Yes empties History and
  the filter lists, closes the debug console, turns test mode off, and leaves the hidden minimap button
  hidden.
- **Fail:** a door with no popup or a different popup, a reset on No, or the button reappearing.
  Show the button again afterwards (`/bl set minimap.shown true`).

### BL.15 · BL-13 — combat visibility without a table per edge (C-04)

- **Do:** General visibility → "Only out of combat". Open the ledger and the session window, then pull
  a dummy. Leave combat. Then close the ledger yourself, pull again and leave combat.
- **Pass:** both windows hide on the pull and return when combat ends. A window you closed stays closed.
- **Fail:** a window stays up in combat, fails to return, or a closed window reopens.

### BL.16 · BL-01 (M2, pre-re-vendor fix) — the retention prune rides AceTimer (C-07)

- **Setup:** `/bl debug on`. Lower "Keep history for" so that at least one existing row is older than
  the retention window. Note that row.
- **Do:** `/reload`, and within 5 s of the loading screen ending, `/bl disable`. Wait 30 s and check the
  row. `/bl enable`, then zone (or `/reload`).
- **Pass:** the row is still there while disabled. After the next loading screen the debug console
  shows the prune and the row is gone.
- **Fail:** the row is pruned while disabled, or never pruned after enable (the latch was set without
  running).

### BL.17 · BL-07 — guild vault after the change

- **Do:** open a guild vault, deposit a stack, close the vault. `/bl debug scan`.
- **Pass:** the session window opens on the vault, the deposit records a guild-bank row, and the
  session ends on close. The scan lists no `GUILDBANKFRAME_*` name.
- **Fail:** no session or row (the chosen event never fired), or a `GUILDBANKFRAME_*` registration is
  still listed.

### BL.18 · BL-11 — logout and inspect

- **Do:** log out. Open `BankLedger.lua`.
- **Pass:** `schemaVersion = 2` is present under `global`. It is checked again at X1's login: `[Init]`
  still reads `schema v2` and the file still carries it.
- **Fail:** no `schemaVersion` key (AceDB stripped it as a default).

### BL.19 · BL-DOCS — the standing pass

- **Do:** walk `BankLedger/docs/smoke-tests.md` C-01 … C-07 (this session has run each once already,
  so this is a reading check that the doc says what you just did).
- **Pass:** each case's text matches the behaviour seen above.

---

## Session PF — PartyFrameEnhanced

**Run after PF-DOCS.** Needs a party with visible party frames. Queue a follower dungeon and run the
session from inside it, since the NPC party gives real party, target and pet frames and a dummy-free
way into combat. One login plus one logout inspection, about 35 minutes.
Elsewhere: PF-09 → Q. PF-11's library-absent half → X2.

### PF.1 · PF-13 upgrade — the minimap choice survives the rename

- **Setup:** game closed. Back up `PartyFrameEnhanced.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** look for the minimap button. `/pfe get global.minimap.shown`. `/pfe get global.minimap.hide`.
  `/dump PartyFrameEnhancedDB.global.minimap`.
- **Pass:** the button is still hidden, the first get prints `false`, and the old path answers
  "unknown setting". The dump shows only `hide = true` (and `minimapPos` if the button was ever
  dragged), with no `shown` key.
- **Fail:** the button is visible, the get prints `true`, the old path still answers, or a `shown` key
  is stored.

### PF.2 · PF-13 — the row in its shown sense

- **Do:** `/pfe set global.minimap.shown true`, then `/pfe get global.minimap.shown`. Then
  `/pfe set global.minimap.shown false`, `/reload`, open Master controls, and set it back to true.
- **Pass:** the button appears with the get printing `true`, hides on false, stays hidden after the
  reload, and the Master controls checkbox agrees at every step.
- **Fail:** the checkbox and the button disagree.

### PF.3 · PF-01 — profile sub-verbs refuse bad names

- **Do:** `/pfe profile new Healer`, `/pfe set castbar.width 222`, `/pfe profile use Default`,
  `/pfe profile new Healer`. Then `/pfe profile copy Nope`, `/pfe profile copy <current>`,
  `/pfe profile use Typo`, `/pfe profile list`.
- **Pass:** the second `new Healer` prints one "already exists" line, and Healer keeps width 222
  (check with `use Healer` and `get`). Each copy and the `use Typo` print one refusal line. `list`
  shows no `Typo`. No Lua error at any point.
- **Fail:** Healer is wiped back to defaults, AceDB raises on the copy, or `Typo` was created.

### PF.4 · PF-02 — anchors follow the new profile

- **Setup:** two profiles: Default (target frames attached) and Free (target frames in free placement).
- **Do:** `/pfe profile use Free`, `/pfe profile use Default`, five times. Then on Free, Reset all settings.
- **Pass:** the target and pet frames follow each profile immediately, with no `/reload`. The reset on
  Free returns them to attached.
- **Fail:** a frame stays where the previous profile placed it until `/reload`.

### PF.5 · PF-07 — the Lock-frame refusal is the collection's line

- **Do:** `/pfe disable`, open the panel, untick Lock frame.
- **Pass:** one line, `Ka0s Party Frame Enhanced is disabled — enable it with /pfe enable`, and the
  box snaps back to ticked.
- **Fail:** a different wording, two lines, or the box stays unticked.

### PF.6 · PF-05 — the EditMode.Exit callback stands down

- **Do:** still disabled, `/pfe debug on`, open and close Edit Mode. `/pfe enable`, open and close
  Edit Mode again.
- **Pass:** no `Providers` resolve lines while disabled. After enable, the resolve burst runs.
- **Fail:** resolve lines while disabled.

### PF.7 · PF-04 — the stand-down unregisters the state drivers

- **Do:** out of combat, `/pfe disable`, then `/pfe enable`. Then enter combat, untick Enable Party
  Frame Enhanced, and leave combat. Re-enable out of combat.
- **Pass:** the target and pet frames return after the first enable. After the combat disable, the
  debug console shows no `ADDON_ACTION_BLOCKED` and the frames are gone. Re-enabling restores them.
- **Fail:** any blocked action, or frames that stay after the stand-down.

### PF.8 · PF-06 — the fade frames and holders hide on stand-down

- **Do:** `/pfe disable`, then `/fstack` over the party area. Enable, then disable in combat and wait
  for combat to end. `/pfe enable`.
- **Pass:** `/fstack` shows no `PartyFrameEnhanced_Fade_*` or `*_Holder` frame. The in-combat disable
  hides them once combat ends, with no `ADDON_ACTION_BLOCKED`. Enable brings back cast bars, target and
  pet frames.
- **Fail:** any `_Fade_` or `_Holder` frame under the cursor while disabled.

### PF.9 · PF-03 — the secure-write memo keeps a toggle made in combat

- **Do:** in combat, untick and re-tick Target frames → Click to target. Leave combat. Left-click a
  target frame.
- **Pass:** the click targets the unit. Add this step to `docs/smoke-tests.md` if PF-03 did not.
- **Fail:** the click does nothing (the re-tick was memoised as a no-op).

### PF.10 · PF-11 — live half: the Schema adoption changes nothing a player sees

- **Do:** tick and untick every Master controls checkbox. Drag a colour picker.
  `/pfe set castbar.width 150`, `/pfe reset castbar.width`. Reset all settings. Defaults on one page.
  Hide the minimap button before both resets.
- **Pass:** every control behaves as before. The minimap button stays hidden through both resets.
  No Lua error.
- **Fail:** a row that no longer saves, or the button reappearing after a reset. The library-absent
  half is X2.5.

### PF.11 · PF-16 — holders stay out of the layout cache

- **Do:** unlock, drag a free-placement holder, lock, `/reload`, then log out. Open
  `WTF/Account/<ACCOUNT>/<realm>/<character>/layout-local.txt`.
- **Pass:** no `PartyFrameEnhanced_*_Holder` or `PartyFrameEnhancedStandIn` entry.
- **Fail:** either name appears.

### PF.12 · PF-08 and PF-13 — the stamp and the minimap table, on disk

- **Do:** with the client still logged out, open `SavedVariables/PartyFrameEnhanced.lua`.
- **Pass:** `global.schemaVersion = 1` is stored (PF-08; the minimap rename adds no step). The
  `minimap` table holds `hide` (as last set) and **no `shown` key**.
- **Fail:** no `schemaVersion` (stripped), a version other than 1, or a stored `shown`.

### PF.13 · PF-DOCS — the standing pass

- **Do:** the full `PartyFrameEnhanced/docs/smoke-tests.md` pass at the owner's convenience, before any
  release. It may be a separate login.

---

## Session MM — MultiMeters

**Run after MM-DOCS.** Needs a training dummy and the P.4 content for the after capture. Two logins,
because MM-21 needs a fresh login at the end. About 40 minutes.
Elsewhere: MM-03, MM-04 and MM-19 → Q. MM-20 → Q as well if P.4 used a dungeon pull.
The SavedVariables table is `MultiMetersDB` (MM-12's smoke names `Ka0s_MultiMetersDB`; the TOC's
`## SavedVariables` line is the one to use).

### MM.1 · MM-16, MM-13 and MM-12 upgrade

- **Setup:** game closed. Back up `MultiMeters.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** look for the minimap button and the window collapsed in P.5. `/mm get global.minimap.shown`.
  `/dump MultiMetersDB.global.minimap`. Open the Header page. `/dump MultiMetersDB.global.schemaVersion`.
- **Pass:** the button is still hidden and the get prints `false` (MM-16's legacy-account case). The
  minimap dump shows only `hide = true` (and `minimapPos`), with no `shown` key. The window is still
  collapsed, and the Header page shows "Show minimize". The version dump prints `16` (MM-13's
  minimize-key step; the minimap rename adds none).
- **Fail:** the button is back, a `shown` key is stored, the window is expanded (the v16 minimize-key
  step lost it), the label still reads "minimise", or the dump prints `nil` or `15`.

### MM.2 · MM-16 — the row in its shown sense

- **Do:** `/mm set global.minimap.shown true`. Then `/mm set global.minimap.shown false`, watch the
  General page checkbox, `/reload`, and set it back to true.
- **Pass:** the button hides on false, the checkbox follows, and it stays hidden after the reload.
- **Fail:** the checkbox disagrees with the button, or the reload brings it back.

### MM.3 · MM-07 — rejected events are reachable

- **Do:** `/mm debug diag`.
- **Pass:** `rejected events: none`.
- **Fail:** any event named on a current client, or no such line.

### MM.4 · MM-09 — the Slash refusal (the LK-17 consumer)

- **Do:** `/mm get window.frame.width`, `/mm set window.frame.width -5`, `/mm get window.frame.width`.
  Also `/mm set <another validated row> 999`.
- **Pass:** each bad set prints the refusal and its reason, and the width is unchanged.
- **Fail:** an echo of the unchanged value as if it were a success, or the width changing.

### MM.5 · MM-02 (SM-11 and the SM-02 launcher half) — the launcher gate

- **Do:** `/mm disable`, left-click the minimap button, right-click it. `/mm enable`. `/mm perf start`,
  and during the suspended arm left-click, then right-click. Finish the perf run.
- **Pass:** disabled gives one refusal line and no window. Suspended gives the suspend line and no
  window. Right-click opens settings in both states.
- **Fail:** a window shows in either state.

### MM.6 · MM-01 (SM-01, SM-02, SM-03) — the latch holds on every show path

- **SM-01 — Do:** `/mm disable`, tick then untick Test mode on the General page. **Pass:** no window appears.
- **SM-02 — Do:** `/mm perf start`, and during the suspended arm `/mm toggle`. **Pass:** nothing shows
  and the suspend line prints.
- **SM-03 — Do:** `/mm disable`, create a window from the Windows page, `/mm enable`. **Pass:** the new
  window appears and refreshes.
- **Fail:** any window drawn while stood down, or a new window that never paints after enable.

### MM.7 · MM-05 (SM-10) — rename keeps the drill-down

- **Do:** open a spell breakdown, then rename its window from the Windows page.
- **Pass:** the breakdown stays open, with the new title.
- **Fail:** the breakdown closes.

### MM.8 · MM-14 — the Schema adoption

- **Setup:** two windows. `/mm debug on`.
- **Do:** with window 1 active in the picker, change a Frame slider for window 2. Copy settings from
  window 1 to window 2 on the Windows page. Toggle the Minimap checkbox twice.
- **Pass:** only window 2 moves. The copy causes one refresh and exactly one `[Set]` line. The checkbox
  toggles the button.
- **Fail:** window 1 moves (the instanceId was lost), several `[Set]` lines for one copy, or a flicker
  per row.

### MM.9 · MM-17 — the colour throttle

- **Do:** on the Columns page, drag a column colour swatch around for a few seconds.
- **Pass:** the window recolours smoothly, with no per-frame stutter.
- **Fail:** a visible hitch per frame, or no recolour until release.

### MM.10 · MM-18 — Columns tabs and the ReorderList drag (the LK-21 consumer)

- **Do:** switch the Columns page's three tabs. Drag a column block by its handle from the middle of
  the list and drop it lower. Then do the same in another window's list.
- **Pass:** the tabs switch cleanly. The insertion line draws in the list colour, the order changes, the
  second list draws its own line, and nothing stutters after the drop (no row `OnUpdate` left armed).
  Record the result in `docs/smoke-tests.md` §5 "Column editor", even if the RenderTabbedSchema adoption
  was declined.
- **Fail:** a line left behind, the wrong colour, or continuing stutter.

### MM.11 · MM-22 (SM-09) — slash lines through the locale

- **Do:** with one window: `/mm lock`, `/mm test`, `/mm reset-positions`. Create a second window and
  repeat.
- **Pass:** the same English sentences as before, with a correct plural ("1 window", "2 windows").
- **Fail:** a raw locale key, or "1 windows".

### MM.12 · MM-20 (SM-07) — the after capture

Run here only if P.4 used a dummy fight. Otherwise this step is Q.4.

- **Do:** repeat P.4's MultiMeters capture on the same content and record it with
  `/wow-addon:perf-analysis` as the **after** bundle. Watch the rows while ranks change.
- **Pass:** the after bundle's render ms/call is lower than the before bundle's. Rows do not flicker or
  misorder.
- **Fail:** render ms/call equal or higher (the item is not accepted), or rows swapping visibly out of order.

### MM.13 · MM-21 (SM-06) — the bounded roster

- **Do:** fight a dummy, `/reload`, and look at the meter. Log out, open `MultiMeters.lua` and look at
  `global.roster`. Log in again (the session's second login).
- **Pass:** the roster survives the `/reload`. The stored roster is bounded as the chosen branch
  says, and after the fresh login the meter behaves as P.6 recorded for that branch.
- **Fail:** the roster is lost on `/reload`, or the stored roster is unbounded.

### MM.14 · the standing pass

- **Do:** the full `MultiMeters/docs/smoke-tests.md` pass, including the SM-01 … SM-11 steps these items
  added to §2, §3, §9, §10 and §14.

---

## Session LH — LootHistory

**Run after LH-DOCS.** Needs a training dummy and records older than 7 days. Two logins (the second
is LH-12's fresh-store check). About 30 minutes.
Elsewhere: LH-01, LH-02 and LH-03 → Q. LH-16 → X2. LH-21 (cold-cache epic) → X1.1.

### LH.1 · LH-13 and LH-12 upgrade — the rename keeps the setting without a migration

- **Setup:** game closed. Back up `LootHistory.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** look for the minimap button. `/lh get minimap.shown`. `/dump LootHistoryDB.global.minimap`.
  `/dump LootHistoryDB.global.schemaVersion`. Open History.
- **Pass:** the button is still hidden, the get prints `false`, the dump shows only `hide = true` (and
  `minimapPos` if the button was ever dragged) with **no `shown` key**. The schema dump prints `8`
  (LH-12; the minimap rename adds no step). Every earlier record is still in History.
- **Fail:** the button is back, a `shown` key is stored, the version is anything but `8`, or history is
  lost.

### LH.2 · LH-13 — the row in its own sense

- **Do:** `/lh set minimap.shown true`. Untick Master controls → Minimap button, then `/lh get minimap.shown`.
  Reset all settings. Then `/lh reset minimap.shown`.
- **Pass:** unticking hides the button and the get prints `false`. Reset all leaves it hidden.
  `/lh reset minimap.shown` brings it back.
- **Fail:** Reset all shows the button, or the reset does nothing.

### LH.3 · LH-11 (S-008.2, S-008.3) — the launcher tooltip and gate

- **Do:** hover the minimap button. `/lh disable`, hover again, left-click, right-click. `/lh enable`.
- **Pass:** enabled, the tooltip shows the brand title and a show/hide line. Disabled, it shows a grey
  disabled line and no left-click hint. Left-click prints the one refusal line. Right-click opens settings.
- **Fail:** the window opens while disabled, or the tooltip still advertises the left-click.

### LH.4 · LH-17 (S2) — rejected events and re-registration

- **Do:** `/lh debug events`. `/lh disable`, `/lh enable`. Loot something.
- **Pass:** `rejected events: none` on 12.1. After the toggle the loot still records.
- **Fail:** a rejected name on a current client, or loot not recorded after enable.

### LH.5 · LH-04 (S-004) — the retention confirm

- **Setup:** records older than 7 days. Keep history for = 90 days.
- **Do:** change it to 7 days and press No. Change it again and press Yes. Then set 90 again and run
  `/lh set settings.retentionDays 7`.
- **Pass:** the confirm names the record count. No keeps every record, puts the dropdown back at 90 and
  prints one chat line. Yes deletes them. The slash path raises the same confirm.
- **Fail:** records deleted without a confirm, or the dropdown left at 7 after No.

### LH.6 · LH-10 (S-007) — the resize grip honours Lock frame

- **Do:** tick Lock frame and drag the grip. Untick, drag, and `/reload`.
- **Pass:** locked, the window does not resize. Unlocked, it does, and the size persists across the reload.
- **Fail:** the grip resizes a locked window.

### LH.7 · LH-09 (S-008.1) — one bind-state vocabulary

- **Do:** export Insights as CSV, then History as CSV. Paste both into a text editor.
- **Pass:** bound-state labels read the same in both files.
- **Fail:** one file says, for example, `BoE` where the other says `Bind on Equip`.

### LH.8 · LH-05 (S1) — visibility from the combat edge

- **Do:** General → Window visibility "Only out of combat", open the window, pull a dummy. Then "Only in
  combat": with the window open in combat, leave combat. Then start a fight and try to start Test mode.
- **Pass:** the window hides at the pull, hides when combat ends in the second mode, and Test mode
  refuses to start mid-fight.
- **Fail:** the window lags one edge behind, or Test mode starts in combat.

### LH.9 · LH-12 — a fresh store

- **Do:** log out. With the game closed, move `LootHistory.lua` aside. Log in, `/reload`,
  `/dump LootHistoryDB.global.schemaVersion`. Log out and put the moved file back.
- **Pass:** the dump prints `8` on the fresh store, and the file written at logout carries
  `schemaVersion = 8`.
- **Fail:** `nil`, `0`, or no `schemaVersion` key in the file.

### LH.10 · LH-DOCS — the standing pass

- **Do:** re-run every check this plan touched, per `LootHistory/docs/smoke-tests.md`. That covers
  S-001 (Q.1), S-002 (Q.2), S-003 (Q.3), S-004, S1, S2, S-005 (X2.4), S-007, S-008.1 … S-008.4, the
  minimap row, and the cold-cache epic (X1.1). The list is complete once all of those sessions have run.

---

## Session AT — AbsorbTracker

**Run after the last AT item.** Needs a training dummy and a shield (a class that shields itself, or a
healer friend). One login, about 25 minutes.
Elsewhere: AT-08 and AT-09 → X2.

### AT.1 · AT-12 and AT-06 upgrade

- **Setup:** game closed. Back up `AbsorbTracker.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** look for the minimap button. `/at get global.minimap.shown`.
  `/dump AbsorbTrackerDB.global.minimap`. `/at debug on`, `/reload`, and read the `[Init]` line.
- **Pass:** the button is still hidden, the get prints `false`, the dump shows only `hide = true` (and
  `minimapPos`) with no `shown` key, `[Init]` reads `schema v5`, and every bar setting is as it was.
- **Fail:** the button is back, a `shown` key is stored, the version differs, or settings reset.

### AT.2 · AT-12 — the row in its own sense

- **Do:** `/at set global.minimap.shown true`, `/at get global.minimap.shown`. Untick the Minimap button
  checkbox, `/reload`, then Reset all settings.
- **Pass:** `true` once shown. The checkbox hides the button, it stays hidden after the reload, and
  Reset all leaves it hidden. Set it back to true.
- **Fail:** Reset all shows the button.

### AT.3 · AT-07 — SafeRegister and the rejected list

- **Do:** `/reload` with `/at debug on`, then `/at debug events`. Swap target and focus, take an absorb,
  and enter and leave combat.
- **Pass:** the `[Init]` line has no "rejected events" clause, `/at debug events` prints `none`, and
  every bar repaints on each swap, absorb and combat edge.
- **Fail:** a rejected name, or a bar that stops updating.

### AT.4 · AT-18 — the brand

- **Do:** Esc → Options → AddOns.
- **Pass:** `Ka0s Absorb Tracker` is listed once.
- **Fail:** any other spelling, or an `[AT]` prefix anywhere a brand is expected.

### AT.5 · AT-10 — the launcher gate moves into Launcher minor 2

- **Do:** `/at disable`, left-click the minimap button, right-click it. `/at enable`, left-click twice.
- **Pass:** disabled prints the disabled line once and the bars stay locked. Right-click opens settings.
  Enabled, left-click toggles the lock.
- **Fail:** the bars unlock while disabled, or the line prints twice.

### AT.6 · AT-03 — profile verbs against the real AceDB

- **Do:** `/at profile new Default`, `/at profile copy NoSuchProfile`, `/at profile copy <current>`,
  `/at profile delete NoSuchProfile`.
- **Pass:** "already exists" and the bars do not reset. Each copy prints its refusal. The delete prints
  "not found". BugSack stays clean.
- **Fail:** the Default profile is wiped, or AceDB raises.

### AT.7 · AT-04 — lock and unlock echo the stored value

- **Do:** unlock the bars out of combat, then pull a dummy. In combat, `/at unlock`. Leave combat. With
  the options panel open on the Lock frame row, `/at unlock`.
- **Pass:** the pull prints `Bars locked — combat started`. The in-combat unlock prints the refusal and
  `locked = true`. Out of combat, the unlock unticks Lock frame in the open panel at once.
- **Fail:** an in-combat unlock succeeds, the echo shows a value that is not the stored one, or the
  panel stays stale.

### AT.8 · AT-11 — `/at debug hold`

- **Do:** `/at debug hold 50000 2.5`. Then `/at debug hold 50000 -3`. Then `/at test 1`.
- **Pass:** the bar shows 50K for about 2.5 s and reverts on its own. The negative duration prints the
  usage. `/at test 1` prints "unknown command".
- **Fail:** the hold sticks, a negative duration is accepted, or the old verb still works.

### AT.9 · AT-15 — the Appearance strip (only if adopted)

- **Do:** Settings → Ka0s Absorb Tracker → Appearance. Pick each unit and click every tab. Pick Focus
  with "Linked to Player" ticked, then untick it.
- **Pass:** each unit shows the same five tabs, the picker block stays in place as you click tabs, the
  linked Focus shows the hint only, and unticking restores the rows.
- **Fail:** the picker jumps, a tab is missing, or the linked Focus shows editable rows. If AT-15 filed
  a decline instead, record "declined" and skip.

---

## Session PM — PanelMaster

**Run after the last PM item.** Needs at least two panels, a second profile, and a training dummy.
One login, about 25 minutes.
Elsewhere: PM-09 → X2.

### PM.1 · PM-11 upgrade and the row in its shown sense (§7b)

- **Setup:** game closed. Back up `PanelMaster.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** `/pm get global.minimap.shown`. `/dump PanelMasterDB.global.minimap`.
  `/pm set global.minimap.shown true` and get again.
  `/pm set global.minimap.shown false`. Show it, then hide it with LibDBIcon's right-click, and get.
  `/reload`. Finally set it back to true.
- **Pass:** the fixture's hidden button is still hidden, the first get prints `false`, and the dump
  shows only `hide = true` (and `minimapPos`) with no `shown` key. Then `true`, the button goes on
  false, the right-click hide makes the get print `false`, and the reload keeps it hidden.
- **Fail:** the get disagrees with the screen at any step, or a `shown` key is stored.

### PM.2 · PM-12 — the Bus Catalog is wired

- **Do:** `/reload`. Drag a panel. Change Master scale.
- **Pass:** no Lua error at load, and both actions repaint the panels.
- **Fail:** an error naming the bus or `Catalog`, or panels that ignore the drag or scale.

### PM.3 · PM-02 (§7) — stand-down beats unlock

- **Do:** `/pm unlock`, then `/pm disable`, and try to drag where a panel was. While disabled, untick
  Master controls → Lock frame and tick a panel's Unlock on the Panels page. Then `/pm enable`.
- **Pass:** while disabled, nothing is drawn (no panel, outline or label) and the drag moves nothing.
  After enable, the unlocked panels return outlined and draggable.
- **Fail:** an outline or label drawn while disabled.

### PM.4 · PM-06 (§9) — the per-panel Unlock tick tells the truth

- **Do:** open Panels and select a panel. Untick Lock frame on General. Re-lock. Then, in combat, tick
  the panel's Unlock and leave combat.
- **Pass:** unlocked globally, the per-panel box shows ticked and greyed. Re-locked, it shows unticked
  and enabled. After combat, the box shows ticked.
- **Fail:** the box shows a state the panel is not in.

### PM.5 · PM-04 (§10) — `/pm recover` in scaled space

- **Do:** Master scale 0.5, drag a panel to the far right half, `/pm recover`. Then Master scale 2 with
  a panel whose scaled position is off-screen, and `/pm recover`.
- **Pass:** the on-screen panel does not move. The off-screen one comes back into view.
- **Fail:** the on-screen panel jumps, or the off-screen one stays lost.

### PM.6 · PM-05 (§12) — a profile swap never duplicates a named frame

- **Setup:** two profiles whose panels carry swapped names.
- **Do:** switch between them five times, then `/pm debug dump`. `/framestack` over each panel.
- **Pass:** the dump's `frames: N active, M pooled, 0 orphaned` line shows no orphans, and each panel's
  frame is the expected `PanelMaster_Panel_<slug>`.
- **Fail:** orphans above 0, or a panel whose frame name belongs to the other profile.

### PM.7 · PM-03 (§8) — combat visibility flips at the first swing

- **Do:** General visibility "Only in combat", then pull a dummy and leave combat. Switch to "Only out of
  combat" and repeat. In combat, `/pm unlock`.
- **Pass:** the panels appear on the first swing and hide when combat ends. The second mode does the
  reverse. The in-combat unlock prints `unlock queued`.
- **Fail:** panels appear a beat late (on the next event instead of the first swing), or in the wrong mode.

---

## Session PC — PrettyChat

**Run after the last PC item.** Needs a training dummy and a profession that can create an item (or
any "create" loot). One login, about 25 minutes.
Elsewhere: PC-22 → Q (it needs LootHistory loaded and real loot in and out of combat).

### PC.1 · PC-13 and PC-04 upgrade — the minimap choice and the Loot override both survive

- **Setup:** game closed. Back up `PrettyChat.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** look for the minimap button. `/pc get global.minimap.shown`. `/dump PrettyChatDB.global.minimap`.
  Open General → Master controls. Open the Tradeskill category and find `LOOT_ITEM_CREATED_SELF`. Then
  `/pc set global.minimap.shown true`, and `/reload`.
- **Pass:** the button is still hidden, the get prints `false`, the dump shows only `hide = true` (and
  `minimapPos`) with no `shown` key, and the Minimap button checkbox is unticked (PC-13). The custom
  format set on **Loot** in P.5 now shows under **Tradeskill** (PC-04's v2 lift). The set brings the
  button back at its old dragged position, and it stays shown after the reload.
- **Fail:** the button reappears on its own, a `shown` key is stored, the override is gone or still
  under Loot, or the button returns at the default position (the rename touched `minimapPos`).

### PC.2 · PC-13 — the row in its shown sense

- **Do:** `/pc get global.minimap.shown`. `/pc set global.minimap.shown false`. Set it back to true.
- **Pass:** `true`. The false set hides the button and unticks the Master controls checkbox.
- **Fail:** the checkbox stays ticked, or `/pc get global.minimap.hide` still answers (it must be
  "unknown setting").

### PC.3 · PC-18 — the TOC notes changed nothing at load

- **Do:** `/reload`. Trigger any chat line from the addon (`/pc help`). Open the debug console.
- **Pass:** the addon loads, its lines carry the cyan `[PC]` prefix (not AceConsole green), and the
  console uses its monospace font.
- **Fail:** green prefix, a load error, or a proportional console font.

### PC.4 · PC-12 — the combat watcher registers through SafeRegisterEvents

- **Do:** General visibility "In combat". Enter and leave combat, triggering a loot or money line on
  each side. `/pc debug on`, `/reload`, and read the `[Init]` line.
- **Pass:** the overrides apply only in combat and switch off after it. `[Init]` has no
  "rejected events" tail.
- **Fail:** the overrides stay on (or off) across the edge, or a rejected name on a current client.

### PC.5 · PC-10 — stale text fixed

- **Do:** hover General → Master controls → Test. `/pc help`.
- **Pass:** the tooltip names the debug console. Help lists resetall as "Reset every setting to defaults".
- **Fail:** the old wording in either place.

### PC.6 · PC-11 (SMK-C09) after — one sorted name list per category

- **Do:** `/pc test`, copy the console output, and diff it against `pc-test-before.txt` from P.3.
- **Pass:** the order is identical.
- **Fail:** any line in a different position.

### PC.7 · PC-04 — the dead Loot copies are gone

- **Do:** set a custom Tradeskill "Created" format, then create (or loot-create) an item.
  `/pc test category Tradeskill`. `/pc test category Loot`.
- **Pass:** the chat line uses the custom format. The Tradeskill test shows the string once, and the Loot
  test no longer lists it.
- **Fail:** the string listed twice, or still listed under Loot.

### PC.8 · PC-05 — ResetRows on the bulk bracket

- **Do:** `/pc debug on`. Change two Loot strings. Press Defaults on the Loot tab of the Categories page.
- **Pass:** exactly one `[Set] reset …: 2 rows` line in the console.
- **Fail:** two `[Set]` lines, or no reset line.

### PC.9 · PC-06 — page-scoped Defaults

- **Do:** customise one Loot and one Money string, then press Defaults on the Loot tab. Customise both
  again and press the Blizzard footer Defaults. Hide the minimap button, then on the General page press
  its Defaults button and Accept.
- **Pass:** both Defaults paths revert both strings. The General page has a Defaults button, its click
  shows the reset-all confirmation, and Accept resets the profile while the hidden button stays hidden.
- **Fail:** only the Loot string reverts, there is no General Defaults button, or the button reappears.
  Show it again afterwards.

### PC.10 · PC-13 and PC-04 — the stamp and the minimap table, on disk

- **Do:** log out and open `PrettyChat.lua`.
- **Pass:** `global.schemaVersion = 2` (PC-04's v2 step; the minimap rename adds none). The `minimap`
  table has `hide` and `minimapPos` and no `shown`.
- **Fail:** version 1 (PC-04's v2 step never ran), a version above 2, or a stored `shown`.

---

## Session WG — WhatGroup

**Run after WG-DOCS.** Needs a training dummy and a capture (a real LFG join, or `/wg test notify`).
One login, about 30 minutes.
Elsewhere: WG-15 and WG-16 → Q (a real application and invite). WG-12's library-absent half → X2.1.

### WG.1 · WG-11 upgrade — the old build's hidden button stays hidden

- **Setup:** game closed. Back up `WhatGroup.lua`, copy it in from `WTF-fixture-P/` (the button was
  hidden with the old build in P.5), and log in.
- **Do:** look for the button. `/wg get global.minimap.shown`. `/dump WhatGroupDB.global.minimap`.
- **Pass:** the button is still hidden, the get answers `false`, and the dump shows only `hide = true`
  (and `minimapPos`) with no `shown` key.
- **Fail:** the button reappeared, the get answers `true`, or a `shown` key is stored.

### WG.2 · WG-11 — the row in its shown sense

- **Do:** `/wg set global.minimap.shown true`, then `/wg get global.minimap.shown`.
  `/wg set global.minimap.shown false`, `/reload`, then set it back to true.
- **Pass:** `true` while visible. False hides it and the reload keeps it hidden.
- **Fail:** the reload brings it back.

### WG.3 · WG-17 — landing logo and config target

- **Do:** Settings → AddOns → Ka0s WhatGroup. Then `/wg config`.
- **Pass:** the landing page shows the logo, and `/wg config` opens the General page.
- **Fail:** a green missing-texture square, or config landing on the wrong page.

### WG.4 · WG-06 — rejected events in `[Init]`

- **Do:** `/wg debug on`, `/reload`, read the `[Init]` line.
- **Pass:** no "rejected events" clause on 12.1.0.
- **Fail:** any rejected name.

### WG.5 · WG-13 — one refusal line

- **Do:** `/wg disable`, left-click the minimap button, right-click it. `/wg enable`.
- **Pass:** one line, `Ka0s WhatGroup is disabled — enable it with /wg enable`. No popup opens.
  Right-click opens settings.
- **Fail:** a popup, or a second wording.

### WG.6 · WG-12 — live half: the Schema adoption behaves as before

- **Do:** `/wg debug on`. `/wg disable`, `/wg enable`, `/wg test on`, `/wg test off`. Tick and untick
  each Master controls checkbox. `/wg set notify.delay 3`.
- **Pass:** each behaves as it did before adoption, and each write logs exactly one `[Set]` line.
- **Fail:** a verb that no longer takes effect, or zero or two `[Set]` lines for one write. The
  library-absent half is X2.1.

### WG.7 · WG-01 (M2, pre-re-vendor fix) — the SetItemRef callback follows the latch

- **Do:** `/wg disable`, `/wg enable`, then Game Menu → Log Out → Cancel. `/wg test notify` (or join via
  LFG) and click the chat "view details" link. `/wg disable` and click the same link again. `/wg enable`.
- **Pass:** no `ADDON_ACTION_FORBIDDEN` or `BLOCKED` at the logout. Enabled, the link opens the popup.
  Disabled, clicking it does nothing.
- **Fail:** taint at logout (per WG-01: revert and record a slash-commands-§7 deviation row instead), or
  the popup opening while disabled.

### WG.8 · WG-02 — settings registration parks in combat (LK-25)

- **Do:** pull a dummy and `/reload` while in combat. Check Settings → AddOns in combat, then again once
  combat ends. Then Game Menu → Log Out → Cancel.
- **Pass:** Ka0s WhatGroup is missing from the list during combat and appears after it, with no second
  `/wg config`. No Lua error, and no taint at logout.
- **Fail:** the category registers in combat, never appears, or the logout raises taint.

### WG.9 · WG-03 (S-001) — a soft-hidden popup in combat never calls the protected Hide

- **Do:** show the popup, pull a dummy, press Close in combat. Leave the group or let the capture wipe.
  Still in combat, click the minimap button (or `/wg show`). Leave combat.
- **Pass:** no `ADDON_ACTION_BLOCKED`. After combat the teleport button is gone and the popup shows
  "No data".
- **Fail:** a blocked action naming the teleport button.

### WG.10 · WG-04 — alpha honours the soft-hidden state

- **Do:** General visibility "Only out of combat". Open the popup and pull a dummy (the popup goes
  invisible). Mid-fight, `/wg show` and click the chat link. Leave combat and press Escape.
- **Pass:** the popup stays invisible throughout the fight. After combat it is closed for real, and
  Escape opens the game menu.
- **Fail:** the popup reappears mid-fight, or Escape is swallowed by an invisible popup.

### WG.11 · WG-05 — the combat-end queue

- **Do (1):** without opening the popup, enter combat and `/wg show` with a capture present. Leave combat.
- **Do (2):** open the popup out of combat with a teleport on cooldown, pull, change the capture in
  combat (`/wg test notify` again), leave combat. Then `/etrace` for `PLAYER_REGEN_ENABLED`.
- **Pass:** (1) prints the "deferred" line and the popup appears after combat. (2) the button reflects the
  latest capture. The trace shows no extra WhatGroup frame watching `PLAYER_REGEN_ENABLED`.
- **Fail:** the popup never appears, the button shows the old capture, or a private regen frame is still
  registered.

### WG.12 · WG-08 (S-003) and WG-11 — the stamp on disk

- **Do:** log out. Open `WhatGroup.lua`.
- **Pass:** `WhatGroupDB.global.schemaVersion = 1` is present (WG-08; the minimap rename adds no
  step). The `minimap` table has `hide` and `minimapPos` and no `shown`.
- **Fail:** no key (stripped), a version other than 1, or a stored `shown`.

### WG.13 · WG-DOCS — the standing pass

- **Do:** the full `WhatGroup/docs/smoke-tests.md` pass after the libs/ refresh. The per-item smokes it
  lists are WG.1 … WG.12 here plus Q.8 (WG-15), Q.9 (WG-16) and P.2 (WG-07).

---

## Session CM — ConsumableMaster

**Run after the last CM item.** Needs a training dummy, a weapon oil or stone for each hand in the
bags, and a second profile. One login, about 40 minutes.
Elsewhere: CM-18 → X2.

### CM.1 · CM-19 upgrade, and CM-16 on a copy

- **Setup:** game closed. Back up `ConsumableMaster.lua` and copy it in from `WTF-fixture-P/`. This
  copy is CM-16's "copy of the SavedVariables". Log in.
- **Do:** look for the button. `/cm get global.minimap.shown`. `/dump ConsumableMasterDB.global.minimap`.
- **Pass:** hidden, `false`, and the dump shows only `hide = true` (and `minimapPos`) with no `shown` key.
- **Fail:** the button is back, the get says `true`, or a `shown` key is stored.

### CM.2 · CM-19 — the row in its shown sense

- **Do:** `/cm set global.minimap.shown true`, `/cm get global.minimap.shown`. Set false, `/reload`, set true.
- **Pass:** `true` with the button visible. False hides it, and it stays hidden after the reload.
- **Fail:** the reload brings it back.

### CM.3 · CM-21 — the About logo

- **Do:** open the About page.
- **Pass:** the logo shows. **Fail:** a missing-texture square.

### CM.4 · CM-15 — nine events, none rejected

- **Do:** `/cm dump events`. `/cm debug on`, `/reload`, read `[Init]`.
- **Pass:** nine events, all registered. `[Init]` shows no rejected events.
- **Fail:** fewer than nine, or any rejected name.

### CM.5 · CM-09 — the launcher says what happened

- **Do:** `/cm bar off`, left-click the minimap button. `/cm disable`, left-click again. `/cm enable`,
  `/cm bar on`.
- **Pass:** with the bar off, the click says the bar is unlocked and that it is off. Disabled, the one
  disabled line prints and nothing unlocks.
- **Fail:** a silent unlock of an invisible bar, or an unlock while disabled.

### CM.6 · CM-17 — the Schema adoption (ConsumableMaster#39)

- **Do:** `/cm debug on`. On each of General, Macro Bar, Stat Priority and Macros, change a row and press
  that page's Defaults. Then `/cm set macroBar.<a number row> 9999`, `/cm set <an enum row> bogus`,
  and `/cm resetall` (accept).
- **Pass:** each page repaints once, the bar re-applies, and a page reset logs exactly one `[Set]` line.
  The number clamps, the enum prints one refusal, and resetall prints one line.
- **Fail:** several `[Set]` lines for one page reset, a page repainting per row, or an out-of-range value
  stored.

### CM.7 · CM-03 — the colour validator stores a copy

- **Do:** `/cm reset <a macro-bar colour path>`. Switch to the second profile and back. Open the Macro
  Bar page. `/cm get <that path>`.
- **Pass:** the swatch shows the shipped colour, and the get prints four channels.
- **Fail:** opaque black, or a colour with missing channels (the default table was aliased and emptied).

### CM.8 · CM-20 — RenderTabbedSchema on General and Macro Bar

- **Do:** shrink the settings window to its narrowest width. Open General and Macro Bar and switch every
  tab. Press each of Maintenance's three buttons. On the Macro Bar's Buttons tab, drag-reorder a button,
  then start a drag and switch tabs mid-drag.
- **Pass:** the strip wraps with no overlap, Master controls is the first tab, the Maintenance buttons
  work, the reorder works, and the tab switch cancels the drag in progress.
- **Fail:** overlapping tabs, a drag ghost left on screen after the switch, or a reorder that does not save.

### CM.9 · CM-29 — the three ReorderList sites (the LK-21 consumer)

- **Do:** drag a row in each of the three ReorderList sites (Category priority, the Macro Bar Buttons
  list, and the third site `docs/smoke-tests.md` names).
- **Pass:** in each, the ghost follows, the drop line draws in that list's colour, and the order saves.
  Record pass or fail for each site, and for CM.13's §6a runs, in the sign-off table.
- **Fail:** a line in the wrong colour, a line left behind, or an order that reverts.

### CM.10 · CM-11 — one reset act behind both doors

- **Do:** in combat, `/cm resetall` and accept, then the panel's Reset all settings and accept. Leave
  combat and do both again.
- **Pass:** in combat, both print the combat line and change nothing. Out of combat, both reset the
  profile and the open panel repaints.
- **Fail:** a reset in combat, or a panel that shows stale values after the reset.

### CM.11 · CM-04 — a combat-deferred enchant macro keeps both hands

- **Do:** with an oil or stone for each hand in the bags, enter combat, `/cm rewritemacros`, leave
  combat. Open the macro UI and read `KCM_WPN_ENCH`.
- **Pass:** the body has both `/use <item>` + `/use 16` and `/use <item>` + `/use 17`.
- **Fail:** one hand's lines missing (the queued body lost its slot lines).

### CM.12 · CM-06 (§11e) — the flyout drivers stand down and re-arm

- **Do:** with the bar on, `/cm disable` out of combat. `/cm enable`. `/cm disable` in combat (it
  completes on regen). `/cm enable`. Hover a slot in and out of combat.
- **Pass:** the flyout opens and closes on hover, and its combat-grace behaviour works after the re-arm.
- **Fail:** a flyout that opens while disabled, or never opens after enable.

### CM.13 · CM-05 (§6a, the LK-25 consumer) — the library parks and replays in combat

- **Enabled — Do:** `/reload` in combat, leave combat, `/cm config`. Then in combat `/cm config`.
- **Disabled — Do:** `/cm disable`, `/reload` in combat, leave combat, open Settings → AddOns. `/cm enable`.
- **Pass:** enabled, the category appears after combat and `/cm config` opens and expands it. In combat,
  `/cm config` prints the library's refusal once. Disabled, the category and its Enable checkbox appear
  after combat. No taint in either run.
- **Fail:** a category registered in combat, one that never appears, or a doubled refusal.

### CM.14 · CM-16 — the stamps on disk

- **Do:** log out. Open `ConsumableMaster.lua`.
- **Pass:** `global.schemaVersion = 3`, and every table under `profiles` carries `schemaVersion = 3`.
- **Fail:** a missing global stamp, or a profile left at an older version.

---

## Session AM — AuraMaster

**Run after the last AM item.** Needs the raid target dummies (for AM-08's after capture), a buff and a
debuff container, and a second profile. Two logins (AM-10's hand-edited store needs its own login).
About 45 minutes.
Elsewhere: AM-16 → X2. The cross-addon OptionsTabs memory check → X1.2.

### AM.1 · AM-14 upgrade

- **Setup:** game closed. Back up `AuraMaster.lua` (AM-10 needs this backup too) and copy it in from
  `WTF-fixture-P/`. Log in.
- **Do:** look for the button. `/am get global.minimap.shown`. `/dump AuraMasterDB.global.minimap`.
  `/am debug on`.
- **Pass:** hidden, `false`, and the dump shows only `hide = true` (and `minimapPos`) with no `shown` key.
- **Fail:** the button is back, the get says `true`, or a `shown` key is stored.

### AM.2 · AM-14 — the row in its shown sense

- **Do:** `/am set global.minimap.shown true`, get. `/am set global.minimap.shown false`, `/reload`.
  `/am reset global.minimap.shown`. Hide it again and press General → Defaults. Show it again afterwards.
- **Pass:** `true`. False hides it, the reload keeps it hidden, and the reset brings it back. General →
  Defaults does not un-hide it.
- **Fail:** Defaults shows the button.

### AM.3 · AM-07 — rejected events in `[Init]`

- **Do:** `/reload` with debug on, and read `[Init]`. `/am disable`, `/am enable`, `/reload`, read it again.
- **Pass:** no "rejected events" clause either time on 12.1.
- **Fail:** any rejected name.

### AM.4 · AM-12 — verbs confirm in the set shape

- **Do:** `/am disable`, `/am enable`, `/am lock`, `/am unlock`.
- **Pass:** `enabled = false`, `enabled = true`, `locked = true`, `locked = false`, in the gold/white shape.
- **Fail:** a free-text confirmation, or a value that differs from what `/am get` then prints.

### AM.5 · AM-09 — Test mode refuses while disabled, on every surface

- **Do:** `/am disable`. Tick General → Master controls → Test mode. Left-click the minimap button.
  Right-click it. `/am enable`, then tick the box and left-click.
- **Pass:** disabled, one refusal line and the box stays unticked. The left-click prints the same one
  line. Right-click opens the panel. Enabled, the box and the left-click both toggle test mode.
- **Fail:** test mode starts while disabled, or two different refusal wordings.

### AM.6 · AM-04 — a stood-down addon builds no frames

- **Do:** `/am disable`, `/reload`. `/framestack` over the screen, `/dump AuraMasterAnchor1`. `/am enable`.
  Disable again, switch to the second profile and back, and enable.
- **Pass:** no `AuraMasterAnchor` frame and the dump prints `nil`. Enable draws every container at
  once. After the profile round trip, enable draws the containers.
- **Fail:** anchor frames exist while disabled, or containers missing after enable.

### AM.7 · AM-03 — a returning container id revives its instance

- **Do:** on profile A, `/am new` twice (five containers). Create profile B with the starters. Out of
  combat, `/dump AuraMasterAnchor5` (note the table address), switch A → B → A, and dump again.
  `/framestack` over the container. Repeat the switch 10 times, with `/dump collectgarbage('count')`
  before and after.
- **Pass:** the same table address before and after, one `AuraMasterAnchor5` in the frame stack, and no
  memory climb across the ten switches.
- **Fail:** a new address, two anchors with the same name, or memory rising per switch.

### AM.8 · AM-15 — the Schema adoption (AuraMaster#21)

- **Do:** with debug on: General → Defaults, Containers → copy settings from another container, and Reset
  position. `/am set container.bars.width 300`. Reset all settings.
- **Pass:** each of the first three logs exactly one `[Set]` line. The set works. Reset all logs the
  profile reset once.
- **Fail:** one `[Set]` line per row, or a width that does not apply.

### AM.9 · AM-17 — the library tab renderer and banner (the LK-27 and LK-28 consumer)

- **Do:** open every page and switch its tabs. Select a container whose aura type hides Categories and
  Overrides while on one of them. Open Bars on an icons container. On Containers, use the picker and
  New container. Flip containers 20 times with `/dump collectgarbage('count')` before and after.
- **Pass:** every page draws its strip, including any host tab that takes a schema group's place, and
  the stale tab heals to the first tab. Bars on an icons container shows the muted-red notice
  (`disabledFor`) **above** its rows, which still draw, rendered disabled. Containers shows the picker
  and New container on one band, and New container creates one. Memory stays flat. The seven pages and
  the picker band match the pre-adoption screenshots (AM-17 adopts without behaviour change).
- **Fail:** a blank page, a strip left on a hidden tab, the notice missing or drawn in place of the
  rows, or memory climbing per flip.

### AM.10 · AM-13 — the category grids

- **Do:** Filters → Categories on a buff container, then a debuff container. Create a user category on
  General, then delete it. Switch profiles.
- **Pass:** the Spell Categories, Blizzard, Dispel Types and Who Cast It grids draw as before, and the
  grid rows follow the create, the delete and the profile switch.
- **Fail:** a missing grid, or a deleted category still listed.

### AM.11 · AM-23 — Dispel Colors peeled out

- **Do:** General → Dispel Colors. Change one swatch, then look at a dispel-typed bar.
- **Pass:** the lead-in, four bullets and five swatches draw, and the bar recolours.
- **Fail:** a missing swatch, or a bar that keeps the old colour.

### AM.12 · AM-19 — the GetMouseFoci path

- **Do:** `/am pick` and hover a frame.
- **Pass:** the frame under the cursor resolves. **Fail:** nothing resolves, or an error naming `GetMouseFocus`.

### AM.13 · AM-20 — one frame-pick flow

- **Do:** `/am pick` and click the player frame. Layout → Pick frame and click it again. Try both in combat.
- **Pass:** both attach, and the Layout path reopens the panel. In combat, both refuse with one grey line.
- **Fail:** a pick in combat, or two different refusal lines.

### AM.14 · AM-08 — the after capture and timed-spell learning

- **Do:** repeat P.4's AuraMaster capture (the same container setting, nameplates on, two minutes on the
  raid dummies) and record it with `/wow-addon:perf-analysis` as the after bundle. Out of combat, gain a
  new timed buff with debug on.
- **Pass:** the pre and post bundles are both recorded, for the owner to compare. The console shows
  `learned N timed spell(s)`.
- **Fail:** no learning line (the unit-event frame is not receiving `UNIT_AURA`).

### AM.15 · AM-32 — screenshots (issue #3)

- **Do:** capture a bar container, an icon container, the unlocked handle with Test mode on, and one image
  per settings page (General, Containers, Filters, Layout, Bars, Icons, Text, Profiles) into
  `media/screenshots/`.
- **Pass:** eleven images exist. The captioned `## Screenshots` section, the `.pkgmeta` ignore line and
  the register-row deletion follow in a later commit.

### AM.16 · AM-10 — the migration runs on a store with no stamp

- **Do:** log out. With the game closed, hand-edit `AuraMaster.lua` to delete `global.schemaVersion`.
  Log in (debug is still on), and read the `[Migrate]` lines. `/reload` and read `[Init]`. Log out and
  restore the AM.1 backup.
- **Pass:** `[Migrate]` lines run v2 … v6 (or report each as an idempotent no-op), and `[Init]` reads
  `schema v6`.
- **Fail:** no `[Migrate]` lines (the default masked the missing stamp), a failed step, or `[Init]`
  below v6.

---

## Session KC — KickCD

**Run after the last KC item.** Needs a training dummy, a Shaman (for KC-06) and a second profile. One
login, about 35 minutes.
Elsewhere: KC-05 → Q (it needs enemies that cast, ideally an Evoker). KC-19 → X2.

### KC.1 · KC-17 upgrade and the row in its own sense

- **Setup:** game closed. Back up `KickCD.lua`, copy it in from `WTF-fixture-P/`, and log in.
- **Do:** `/kcd get global.minimap.shown`. `/dump KickCDDB.global.minimap`.
  `/kcd set global.minimap.shown true`. Untick General → Master controls → Minimap button,
  `/kcd get global.minimap.shown`, `/reload`, then Reset all settings.
- **Pass:** the fixture's button is still hidden, the first get prints `false`, and the dump shows only
  `hide = true` (and `minimapPos`) with no `shown` key. The untick hides it, the get prints `false`, and
  it stays hidden through the reload and the Reset all. Show it afterwards.
- **Fail:** the button reappears at any point, or a `shown` key is stored.

### KC.2 · KC-04 — rejected events

- **Do:** `/kcd debug events`. `/kcd debug on`, `/reload`, read `[Init]`.
- **Pass:** `no rejected events` on live 12.1.x, and no rejected clause in `[Init]`.
- **Fail:** any rejected name.

### KC.3 · KC-23 — TOC comments only

- **Do:** `/reload`. **Pass:** no Lua error. **Fail:** any load error.

### KC.4 · KC-13 — Spells rows peeled out

- **Do:** open the Spells page. Add a spell, drag a row, remove a spell.
- **Pass:** rows, drag, add and remove look and behave as before.
- **Fail:** a missing row, or a control that does nothing.

### KC.5 · KC-12 — Spells rows, tooltips, and the ReorderList drag (the LK-21 consumer)

- **Do:** drag row 3 above row 1, `/reload`. Start another drag and press Esc mid-drag. Hover a spell
  name and a category dropdown. Close Settings, open another Ka0s panel (`/at config`) and hover its labels
  and click its controls. Look at the remove glyph.
- **Pass:** the drop line draws in the list colour and the order persists after the reload. Esc leaves
  no stray line. The spell tooltip and the category tooltip show. The other addon's labels show no KickCD
  spell tooltip, and its clicks land. The remove glyph reads as "remove".
- **Fail:** a KickCD tooltip on another addon's widget (a hooked pooled AceGUI frame), or a stray line.

### KC.6 · KC-06 — one resolver for spell input

- **Setup:** a Shaman.
- **Do:** `/kcd spells add Wind Shear`. `/kcd spells add <a spell not in the Cooldown Manager>`. With
  the Spells page closed, switch spec, then open it and try the Add box with the old spec's spell and the
  new spec's spell.
- **Pass:** Wind Shear is added (a multi-word name). The non-CM spell prints the Cooldown Manager line.
  After the spec switch, Add accepts only the new spec's CM spells.
- **Fail:** the multi-word name split, the non-CM spell added, or the old spec's list still accepted.

### KC.7 · KC-18 — the Schema adoption (KickCD#22)

- **Do:** open every settings page and edit one value per widget type, then `/reload` and check each
  persisted. With `/kcd debug on`, drag a colour. General → Units → Copy styling from Target. Untick
  Enable KickCD. Tick it again. Reset all settings. `/kcd set icons.nope 1`.
- **Pass:** every value persists. The colour drag logs one debounced `[Set]` line. The copy logs one
  `[Set] copy target→focus: N rows` line. Unticking Enable stands the grid and bar down at once. Reset
  all logs one profile-reset line. The bad path prints `Setting not found`.
- **Fail:** a value lost on reload, several `[Set]` lines for one copy, or a delayed stand-down.

### KC.8 · KC-10 — scheduleTimer returns a real handle

- **Do:** with debug on, drag the cast-bar colour picker for 2 s.
- **Pass:** one `[Set]` line for the path, and the frame rate holds.
- **Fail:** a `[Set]` line per frame, or a visible frame-rate drop.

### KC.9 · KC-20 — the linked-Focus page

- **Do:** Settings → Icons → unit picker Focus while Focus is linked. Repeat on Cast bar and Text Label.
  Click the note's link. Unlink Focus.
- **Pass:** the strip is present and greyed, the link opens General → Units, and unlinking restores the
  editable tabs.
- **Fail:** editable controls while linked, or a dead link.

### KC.10 · KC-03 — migrations run for every profile

- **Do:** create a second profile in Settings → Profiles, switch to it and back. Look at the cast-bar
  colour swatch and the outline dropdown. Check the debug console.
- **Pass:** both show stored values, never blank or defaults, and there is no `migration … failed` line.
- **Fail:** a blank swatch or outline, or a failed-migration line.

### KC.11 · KC-15 — resetposition restores every grid

- **Do:** `/kcd unlock`, drag both grids, `/kcd lock`, `/kcd resetposition`. Drag again and use
  General → Reset position.
- **Pass:** both grids jump to their defaults each time.
- **Fail:** only one grid resets.

### KC.12 · KC-07 — the combat listener is an AceEvent target

- **Do:** visibility "In combat". Enter and leave combat. Then `/kcd disable`, fight, leave combat,
  `/kcd enable`.
- **Pass:** the grid shows and hides on the edges. After the disabled fight, the combat flag is correct:
  the grid is hidden out of combat.
- **Fail:** the grid shows out of combat after enable (a stale combat flag).

### KC.13 · KC-08 (C-06) — a rebuilt icon keeps its cooldown

- **Do:** use your interrupt so it is on cooldown, then swap a talent (or summon a pet, or `/reload`).
- **Pass:** the icon keeps its cooldown swipe and does not flash ready.
- **Fail:** the icon shows ready while the spell is on cooldown.

### KC.14 · KC-14 — perf nesting on the Rebuild path (optional)

- **Do:** `/kcd perf start`, fight about 30 s, change talents once, `/kcd perf finish`.
- **Pass:** the nesting lines show `spellState` under `stateEmit` plus the `rebuildEmit` mix. Record it
  later with `/wow-addon:perf-analysis`.
- **Fail:** `spellState` nested under the wrong parent.

### KC.15 · KC-03 on disk (opportunistic)

- **Do:** log out and open `KickCD.lua`.
- **Pass:** `global.schemaVersion = 5` is stored.
- **Fail:** the key is missing (stripped as a default).

---

## Session Q — the group content night

**Run after every M3 addon item has landed and before any addon branch merges.** LH-02 is a pre-merge
checkpoint, and its failure rule is "revert the code half", which is only cheap before the merge.
Everything that needs other players, a real LFG invite, a Mythic+ key, a boss or a raid is here, so it
costs one evening rather than a login per addon.

Needs: all eleven addons on their finished branches. One route that covers it in order: apply to a
Mythic+ listing through the Group Finder (Q.8, Q.9), join (Q.10), run the key (Q.1, Q.2, Q.4, Q.6, Q.11,
Q.12), then a raid or LFR wing (Q.5, Q.7). About 90 minutes, one or two logins.

### Q.1 · LH-01 (S-001) — the keystone context clears on leaving

- **Setup:** `/lh debug on`.
- **Do:** run the key, complete it, loot the reward chest. Zone out and back in mid-key once and loot an
  object. After the key, leave the dungeon and mine an ore node or pick a herb.
- **Pass:** the chest and the mid-key object record as `MPLUS`. The ore or herb records as `CONTAINER`,
  and the console shows the `keystone cleared` line on the zone change.
- **Fail:** the gathering loot records as `MPLUS` (the context leaked), or the mid-key zone cleared it early.

### Q.2 · LH-02 (S-002) — encounter context in the grace window (pre-merge checkpoint)

- **Do:** kill a boss and loot its corpse, with debug on. Then
  `/dump LootHistoryDB.global.history[#LootHistoryDB.global.history].sourceDetail`.
- **Pass:** the console shows `encounter end` **before** `LOOT_OPENED`, and the dump carries `encounterID`.
- **Fail:** `sourceDetail` has no `encounterID`. **Not reproduced:** if `LOOT_OPENED` arrives first, the
  finding does not reproduce. Revert LH-02's code half and keep only its doc correction.

### Q.3 · LH-03 (S-003) — the currency-category cache

- **Do:** loot a currency not seen this session (a season-start currency is the item's case; any fresh
  currency works when a season start is not available). Then collapse a header on the Currency tab,
  `/reload`, and loot a currency under that header.
- **Pass:** the first row's Subtype column shows its Currency-tab header. For the collapsed case, record
  in `midnight-quirks.md` whether the subtype resolves. That is an observation, not a pass/fail.
- **Fail:** a blank or "Other" subtype for a currency whose header is expanded.

### Q.4 · MM-20 (SM-07) — the after capture, when the before was a dungeon pull

Run here only if P.4 used a dungeon pull. Otherwise it is MM.12.

- **Do / Pass / Fail:** as MM.12, on a comparable pull in this dungeon.

### Q.5 · MM-03 (SM-04) — "Always show yourself" is scroll-aware

- **Setup:** the default window in a raid, where you rank below the visible rows.
- **Do:** look at the last row. Scroll until your own row is in view.
- **Pass:** your row sits in the last slot with your true rank. Once you scroll to it, there is no
  duplicate row.
- **Fail:** a wrong rank in the pinned slot, or your name twice.

### Q.6 · MM-04 (SM-05) — chat export through Compat.ChatSender

- **Do:** in the group, export to PARTY. Then export to SELF.
- **Pass:** the lines arrive in party chat. SELF prints locally with no notice.
- **Fail:** a PARTY export that only prints locally, or a notice on SELF.

### Q.7 · MM-19 — two new perf buckets

- **Do:** `/mm perf` capture during a raid pull, then finish.
- **Pass:** the report lists `spellEvent` and `systemEvent` with calls and ms. Record it with
  `/wow-addon:perf-analysis` into `docs/perf-analysis/<stamp>/` to inform the registration decision.
- **Fail:** either bucket is missing, or it shows zero calls in a raid pull.

### Q.8 · WG-15 (S-006) — teleport button handlers at file scope

- **Do:** after the invite, hover the popup's teleport button. Click it while ready. With `/wg debug on`,
  count the log lines. Get a second capture (another listing, or `/wg test notify`) and hover again.
- **Pass:** the tooltip shows the dungeon's teleport spell, the click casts it, each press logs one
  `teleport button pressed` line, and after the second capture the tooltip shows the new spell.
- **Fail:** the old spell's tooltip after the recapture, or two log lines per press.

### Q.9 · WG-16 (S-005) — debug lines read the same

- **Do:** `/wg debug on`, apply to a listing, and get invited.
- **Pass:** the console lines read exactly as before the change: LFG appID and status, Invite, Capture,
  and Frame `popup shown`.
- **Fail:** a line with `%s` or `%d` left in it, or a missing value.

### Q.10 · PF-09 — session-long registrations move to their owners

- **Setup:** before joining, solo, `/pfe debug on`.
- **Do:** solo, change target. Join the party and change target. Put a raid marker on a party member.
  Unlock the frames and enter combat.
- **Pass:** solo, no Target line. In the party, your own target frame updates on
  `PLAYER_TARGET_CHANGED`, and raid markers repaint. Combat prints `Locked — combat started`.
- **Fail:** Target lines while solo, a stale target frame in the party, or no re-lock line.

### Q.11 · KC-05 (C-03 step 4) — one cast filter frame per unit, with the EMPOWER events

- **Do:** target an Evoker (in this group, a duel or PvP) and watch an empowered cast. Then
  `/kcd disable` and `/kcd enable` three times, and watch enemy casts.
- **Pass:** the empowered cast starts and stops the bar and the glow. After the three toggles, casts still
  drive the bar and grid, with no error. If no Evoker was available, record the empower half as
  **untested**.
- **Fail:** the bar stops following casts after the toggles, or the empowered cast never shows.

### Q.12 · PC-22 (SMK-F001) — PrettyChat rewrites the loot globals for everyone

- **Setup:** LootHistory loaded. PrettyChat visibility "In combat".
- **Do:** `/etrace` on `CHAT_MSG_LOOT`. Loot during combat, and again out of combat.
- **Pass:** `arg1` arrives in PrettyChat's format, and the wording changes between combat and
  non-combat. Once LootHistory's H-1 fix has landed, both loots are recorded in History.
- **Fail:** the format does not change across the edge. If only one of the loots is in History, record
  that as H-1 still open, not as a PC-22 failure.

---

# Sessions X1 and X2 — LibKa0s v1.56.0 across the collection

**Run once all eleven addon sessions have passed.** Session L proved the library files on addons that
had not adopted anything yet. X1 proves the surfaces the addons now use, all eleven loaded together, and
X2 proves the other side of the owner's ruling: with the library gone, every addon degrades with a
chat line and no Lua error.

## Session X1 — library present

**One fresh login** (the item cache must be cold for X1.1). All eleven addons loaded. About 35 minutes.

### X1.0 · BL-11, the second login

- **Do:** `/bl debug on`, `/reload`.
- **Pass:** `[Init]` still reads `schema v2`, so the stamp BL.18 saw on disk survived a second login.
- **Fail:** v1, or a migration that runs again.

### X1.1 · LH-21 — Item `|cnIQ` quality on a cold cache (LK-12 across the collection)

- **Do:** straight after login, loot an item of epic quality that this character has not seen this
  session (a dungeon end boss, a Delve or Vault chest). Open LootHistory's History. Then run L.4's two
  `/run` lines on the new item's id.
- **Pass:** the History row shows Epic and the purple name **immediately**, not Poor and not after a
  refresh. The `/run` prints `4`. If BankLedger is open at a bank, depositing the same item records a
  purple row (the BL.2 check, repeated with all addons loaded).
- **Fail:** a Poor or white row that corrects itself later (the hex rung answered first), or `nil`.

### X1.2 · OptionsTabs no-leak across repeated page renders (LK-27, LK-28, across the collection)

- **Do:** `/dump collectgarbage('count')`. For each addon with a tabbed or bannered settings page, open
  its settings and switch between pages and tabs 30 times: `/am` (all seven pages), `/mm` (Windows
  picker), `/at` (Appearance unit picker), `/cm` (General and Macro Bar), `/kcd` (Icons unit picker),
  `/pm`, `/pc`, `/lh`, `/bl`, `/wg`, `/pfe`. Then `/dump collectgarbage('count')` again. Finish with
  `/framestack` over one banner.
- **Pass:** the collection-wide figure is within a few hundred KB of the first reading after 330 switches,
  and it does not keep climbing if you repeat one addon's 30. The frame stack shows exactly one Dropdown
  under the chrome band, and the divider hairline is drawn once. (Per-addon memory from
  `GetAddOnMemoryUsage` lands on whichever addon's `libs/` copy LibStub kept, so use the global figure.)
- **Fail:** growth that scales with the number of switches, a second Dropdown under a band, or any
  `SetParent`/`Release` error.

### X1.3 · Slash refusal echo across the collection (LK-17, S-003)

- **Do:** for each addon, `/<slash> list`, pick a row with a validator or an enum, and
  `/<slash> set <path> <a value the parser accepts but validate rejects>`, then `/<slash> get <path>`.
  Cover at least `/mm set window.frame.width -5`, `/bl set settings.visibility bogus`, AuraMaster's
  validated string row from `settings/Containers.lua` (S-003), and a ConsumableMaster enum row.
- **Pass:** each prints `Invalid value for <path>` with the host's reason on an indented line, there is
  **no** `<path> = <old>` echo, and each get prints the unchanged value.
- **Fail:** any addon that still echoes the old value as a success.

### X1.4 · Launcher refusal in the library (LK-16, S-006), across the collection

- **Do:** for each addon with a minimap button, `/<slash> disable`, left-click the button, right-click
  it, then `/<slash> enable`.
- **Pass:** every rung (a)/(b) addon prints exactly one `<Brand> is disabled — enable it with
  /<slash> enable` line and opens nothing. PrettyChat (rung c) opens its settings panel instead.
  Right-click opens settings everywhere.
- **Fail:** any addon that opens its window, toggles a lock or prints a second wording while disabled.
- *(Optional, needs a test install with LibDBIcon removed: `/reload` twice. The NO_ICON notice prints
  once per session with no `[LibKa0s]` tag.)*

### X1.5 · SafeRegister across the collection (LK-11)

- **Do:** `/reload` once with debug on in every addon, and read each `[Init]` line.
- **Pass:** eleven `[Init]` lines, none with a "rejected events" clause. (PanelMaster, PartyFrameEnhanced
  and the others without a SafeRegister item just print their usual `[Init]`.)
- **Fail:** any rejected name on a current client.

### X1.6 · Regression and taint with everything loaded

- **Do:** with a banner page open, enter combat and click an action-bar button. Open settings through
  `/<slash> config` and through Esc → Options → AddOns, out of combat and in combat. Check that each
  addon appears once in the AddOns list and that each slash root reaches its own addon.
- **Pass:** no "Interface action failed", no duplicate entries, and in combat every panel is refused or
  covered without errors.
- **Fail:** any taint line, or a page drawn live in combat.

## Session X2 — library absent, every addon at once

**Run straight after X1.** Per LibStub fact 2, every copy must go, or the test proves nothing.
One client start, plus one more after restoring. About 25 minutes.

**Setup (game closed).** In each of the eleven addon folders under `Interface/AddOns/`, rename
`libs/LibKa0s` to `libs/LibKa0s.off`. Leave MultiMeters and PrettyChat renamed too: they have no X2 item,
but loading them degraded is a free check (X2.11). Start the client and log in. Confirm with
`/run print(LibStub("LibKa0s-Core-1.0", true))`, which must print `nil`. If it prints a table, some
addon still ships the library. Find it before going on.

### X2.1 · WG-12 — WhatGroup's degraded verbs (the owner's ruling on WhatGroup#22)

The owner accepted that adopting the Schema seam costs the library-less build its `enable` and `test`
verbs, on condition that they fail gracefully. WhatGroup passes **no** `writeThrough` list (WS-02 route b).

- **Do:** `/wg disable`. `/wg test on`. `/wg enable`. `/wg test off`. Then check that WhatGroup is still
  running: `/wg show`, or left-click the minimap button.
- **Pass:** each verb prints exactly one line of the form
  `/wg <verb> is unavailable: the LibKa0s library did not load.` (for example
  `/wg enable is unavailable: the LibKa0s library did not load.`). BugSack stays empty. The store did not
  change: WhatGroup is still enabled and test mode never started.
- **Fail:** any Lua error. Silence (no line at all). A false success such as `enabled = false`. Or the
  addon actually disabling, which would mean a write went through with no list to allow it.

### X2.2 · BL-10 — enable and disable write through (WS-02 route a)

- **Do:** `/bl disable`, open the bank and move a stack. `/bl enable`, move another.
- **Pass:** the disable prints `settings.enabled = false` with no Lua error, and the first move is not
  captured. After enable, the second is.
- **Fail:** an error, the library-absent line (BankLedger lists `enabled`), or capture that continues
  while disabled.

### X2.3 · AT-08 — writeThrough `{enabled, locked}`

- **Do:** `/at disable`, then swap targets a few times. `/at enable`. `/at unlock`, then `/at lock`.
- **Pass:** the bars go away and stay away through the target swaps. Enable brings them back. Unlock and
  lock both take effect. No Lua error.
- **Fail:** bars that reappear on a target swap while disabled (a composed-row write the stub dropped).

### X2.4 · LH-16 (S-005, S-008.4) — the degraded Slash stub

- **Do:** `/lh disable`, then loot something. `/lh` (help). `/lh enable`. `/lh resetall`.
- **Pass:** disable prints an acknowledgement and the loot is not recorded. Help lists `enable`. Enable
  restores recording with no Lua error. Resetall prints the counted filters line.
- **Fail:** recording that continues while disabled, or an uncounted resetall line.

### X2.5 · PF-11 — the library-less build still writes its composed rows (PartyFrameEnhanced#14)

- **Do:** `/pfe disable`, then `/reload`. Check the frames. `/pfe enable`.
- **Pass:** the addon is still disabled after the reload (the write reached the store through
  `writeThrough`), and enable restores it. No Lua error.
- **Fail:** the addon comes back enabled after the reload (the write was lost), or any error.

### X2.6 · AT-09 — the LK-18 Slash stub shape

- **Do:** `/at help`. `/at list`.
- **Pass:** help lists plain rows. `/at list` prints `/at list is unavailable: the LibKa0s library did
  not load.` No Lua error.
- **Fail:** formatted rows copied from the library, or an error on `list`.

### X2.7 · PM-09 — write-through verbs and the library-absent line

- **Do:** `/pm disable`, then `/pm enable`. `/pm unlock`.
- **Pass:** the panels go and come back, with the echo in chat and no Lua error. `/pm unlock` prints
  `/pm unlock is unavailable: the LibKa0s library did not load.`
- **Fail:** an error, or an unlock that silently does nothing.

### X2.8 · CM-18 — composed-row verbs print the library-absent line

- **Do:** `/cm enable`, `/cm bar on`, `/cm lock`.
- **Pass:** each prints one `… is unavailable: the LibKa0s library did not load.` line. BugSack stays
  empty. None claims success.
- **Fail:** a Lua error, or a line like `enabled = true` when nothing was written.

### X2.9 · AM-16 — hollow composers, write-through verbs

- **Do:** `/am disable`, then `/am enable`. `/am set enabled false`. `/am lock`.
- **Pass:** disable and enable toggle the containers with no Lua error. `/am set enabled false` prints the
  library-absent line. `/am lock` locks.
- **Fail:** any error, or containers that do not toggle.

### X2.10 · KC-19 — the degraded Slash stub

- **Do:** `/kcd disable`, then `/kcd enable`. `/kcd list`. `/kcd disable` once more and left-click the
  minimap button, if the degraded build shows one.
- **Pass:** disable and enable toggle the addon with chat lines and no Lua error. `/kcd list` prints
  `/kcd list is unavailable: the LibKa0s library did not load.` The disabled line matches the library's
  bytes.
- **Fail:** an error, or a disabled line with different wording.

### X2.11 · MultiMeters and PrettyChat load degraded (opportunistic)

- **Do:** `/mm`, `/pc`.
- **Pass:** both load without a Lua error and answer their root. They have no X2 item, so any failure
  here is a new finding to file, not a plan regression.

**Restore (game closed).** Rename every `libs/LibKa0s.off` back to `libs/LibKa0s`. Start the client,
`/reload`, and confirm `/run print(LibStub("LibKa0s-Core-1.0", true))` prints a table and every addon
answers its root. Then run `git -C <repo> status` in each repository: nothing may show, because the
renames happened in the game folder.

---

## Session X-ru — Media font on ruRU (optional)

**LK-13 (S-004, the ruRU half).** Run whenever a ruRU client is available, either after Session L or
after X1.

- **Setup:** Battle.net → Game Settings → Text Language → Русский, and re-log.
- **Do:** `/run print(LibStub("LibSharedMedia-3.0"):IsValid("font","JetBrains Mono"))`. Open a
  consumer's font dropdown (MultiMeters → Appearance → font). Open any Ka0s debug console.
- **Pass:** `true`. JetBrains Mono is listed and draws Cyrillic, and the console text is readable
  Cyrillic, not boxes.
- **Fail:** `false`, or the face missing from the list (LSM refused the registration because the langmask
  excluded ruRU). If no ruRU client is available, record LK-13's ruRU half as **untested** in the sign-off.
  L.5 has already proved enUS.

---

# Not in-client

Two items have a smoke field that no client can run. They are listed here so the coverage table is
complete.

### WA-02 — `bin/ka0s-bounded` resolves on the plugin's PATH

- **Setup:** a fresh Claude Code session with the wow-addon plugin installed.
- **Do:** in any addon, `ka0s-bounded luacheck .`.
- **Pass:** luacheck runs, bounded. **Fail:** `command not found`.

### BL-20 — the citation sweep's desk check (C-05)

- **Do:** open each symbol cited in BankLedger's `ARCHITECTURE.md` register and Event Subscriptions and
  confirm it resolves. The in-client half (the copy window's close) is BL.11.
- **Pass:** every citation resolves to a symbol that exists. **Fail:** any dangling citation.

---

# Coverage

Generated from the step headings above against `plan-data/items.json`: exactly the items with a
non-empty `smoke` field, each with its current milestone. **168 ids (M1 17, M2 2, M3 149; no M4
item has a smoke field), none unmapped.**

| Item | Milestone | Repo | Step(s) | Note |
|---|---|---|---|---|
| LK-10 | M1 | LibKa0s | L.3 |  |
| LK-11 | M1 | LibKa0s | L.2, X1.5 |  |
| LK-12 | M1 | LibKa0s | L.4, BL.2, X1.1 |  |
| LK-13 | M1 | LibKa0s | L.5, X-ru | ruRU half optional |
| LK-14 | M1 | LibKa0s | L.6 |  |
| LK-16 | M1 | LibKa0s | BL.6, X1.4 |  |
| LK-17 | M1 | LibKa0s | BL.8, MM.4, X1.3 |  |
| LK-19 | M1 | LibKa0s | L.7 |  |
| LK-20 | M1 | LibKa0s | L.8 |  |
| LK-21 | M1 | LibKa0s | L.9, MM.10, CM.9, KC.5 |  |
| LK-24 | M1 | LibKa0s | L.10 |  |
| LK-25 | M1 | LibKa0s | WG.8, CM.13 |  |
| LK-26 | M1 | LibKa0s | L.11 |  |
| LK-27 | M1 | LibKa0s | L.12, AM.9, X1.2 |  |
| LK-28 | M1 | LibKa0s | L.13, AM.9, X1.2 |  |
| LK-33 | M1 | LibKa0s | L.1 |  |
| WA-02 | M1 | wow-addon | Not in-client |  |
| BL-01 | M2 | BankLedger | BL.16 | pre-re-vendor fix, checked in Session BL |
| WG-01 | M2 | WhatGroup | WG.7 | pre-re-vendor fix, checked in Session WG |
| BL-03 | M3 | BankLedger | BL.12 |  |
| BL-04 | M3 | BankLedger | BL.13 |  |
| BL-05 | M3 | BankLedger | BL.14 |  |
| BL-06 | M3 | BankLedger | BL.5 |  |
| BL-07 | M3 | BankLedger | P.1, BL.17 |  |
| BL-08 | M3 | BankLedger | BL.6 |  |
| BL-09 | M3 | BankLedger | BL.8 |  |
| BL-10 | M3 | BankLedger | X2.2 |  |
| BL-11 | M3 | BankLedger | BL.1, BL.18, X1.0 |  |
| BL-12 | M3 | BankLedger | BL.1, BL.3 | upgrade carry-over check, no SV migration |
| BL-13 | M3 | BankLedger | BL.15 |  |
| BL-16 | M3 | BankLedger | BL.4 |  |
| BL-17 | M3 | BankLedger | BL.9 |  |
| BL-18 | M3 | BankLedger | BL.7 |  |
| BL-20 | M3 | BankLedger | BL.11, Not in-client |  |
| BL-21 | M3 | BankLedger | BL.10 |  |
| BL-DOCS | M3 | BankLedger | BL.2, BL.19 |  |
| PF-01 | M3 | PartyFrameEnhanced | PF.3 |  |
| PF-02 | M3 | PartyFrameEnhanced | PF.4 |  |
| PF-03 | M3 | PartyFrameEnhanced | PF.9 |  |
| PF-04 | M3 | PartyFrameEnhanced | PF.7 |  |
| PF-05 | M3 | PartyFrameEnhanced | PF.6 |  |
| PF-06 | M3 | PartyFrameEnhanced | PF.8 |  |
| PF-07 | M3 | PartyFrameEnhanced | PF.5 |  |
| PF-08 | M3 | PartyFrameEnhanced | PF.12 |  |
| PF-09 | M3 | PartyFrameEnhanced | Q.10 |  |
| PF-11 | M3 | PartyFrameEnhanced | PF.10, X2.5 |  |
| PF-13 | M3 | PartyFrameEnhanced | PF.1, PF.2, PF.12 | upgrade carry-over check, no SV migration |
| PF-16 | M3 | PartyFrameEnhanced | PF.11 |  |
| PF-DOCS | M3 | PartyFrameEnhanced | PF.13 |  |
| MM-01 | M3 | MultiMeters | MM.6 |  |
| MM-02 | M3 | MultiMeters | MM.5 |  |
| MM-03 | M3 | MultiMeters | Q.5 |  |
| MM-04 | M3 | MultiMeters | Q.6 |  |
| MM-05 | M3 | MultiMeters | MM.7 |  |
| MM-07 | M3 | MultiMeters | MM.3 |  |
| MM-09 | M3 | MultiMeters | MM.4 |  |
| MM-12 | M3 | MultiMeters | MM.1 |  |
| MM-13 | M3 | MultiMeters | MM.1 |  |
| MM-14 | M3 | MultiMeters | MM.8 |  |
| MM-16 | M3 | MultiMeters | MM.1, MM.2 | upgrade carry-over check (legacy account) |
| MM-17 | M3 | MultiMeters | MM.9 |  |
| MM-18 | M3 | MultiMeters | MM.10 | reconcile: LK-21 drag check |
| MM-19 | M3 | MultiMeters | Q.7 |  |
| MM-20 | M3 | MultiMeters | P.4, MM.12, Q.4 |  |
| MM-21 | M3 | MultiMeters | P.6, MM.13 |  |
| MM-22 | M3 | MultiMeters | MM.11 |  |
| LH-01 | M3 | LootHistory | Q.1 |  |
| LH-02 | M3 | LootHistory | Q.2 |  |
| LH-03 | M3 | LootHistory | Q.3 |  |
| LH-04 | M3 | LootHistory | LH.5 |  |
| LH-05 | M3 | LootHistory | LH.8 |  |
| LH-09 | M3 | LootHistory | LH.7 |  |
| LH-10 | M3 | LootHistory | LH.6 |  |
| LH-11 | M3 | LootHistory | LH.3 |  |
| LH-12 | M3 | LootHistory | LH.1, LH.9 |  |
| LH-13 | M3 | LootHistory | LH.1, LH.2 | upgrade carry-over check, no SV migration |
| LH-16 | M3 | LootHistory | X2.4 |  |
| LH-17 | M3 | LootHistory | LH.4 |  |
| LH-21 | M3 | LootHistory | X1.1 |  |
| LH-DOCS | M3 | LootHistory | LH.10 |  |
| AT-03 | M3 | AbsorbTracker | AT.6 |  |
| AT-04 | M3 | AbsorbTracker | AT.7 |  |
| AT-06 | M3 | AbsorbTracker | AT.1 |  |
| AT-07 | M3 | AbsorbTracker | AT.3 |  |
| AT-08 | M3 | AbsorbTracker | X2.3 |  |
| AT-09 | M3 | AbsorbTracker | X2.6 |  |
| AT-10 | M3 | AbsorbTracker | AT.5 |  |
| AT-11 | M3 | AbsorbTracker | AT.8 |  |
| AT-12 | M3 | AbsorbTracker | AT.1, AT.2 | upgrade carry-over check, no SV migration |
| AT-15 | M3 | AbsorbTracker | AT.9 |  |
| AT-18 | M3 | AbsorbTracker | AT.4 |  |
| PM-02 | M3 | PanelMaster | PM.3 |  |
| PM-03 | M3 | PanelMaster | PM.7 |  |
| PM-04 | M3 | PanelMaster | PM.5 |  |
| PM-05 | M3 | PanelMaster | PM.6 |  |
| PM-06 | M3 | PanelMaster | PM.4 |  |
| PM-09 | M3 | PanelMaster | X2.7 |  |
| PM-11 | M3 | PanelMaster | PM.1 | upgrade carry-over check, no SV migration |
| PM-12 | M3 | PanelMaster | PM.2 |  |
| PC-04 | M3 | PrettyChat | PC.1, PC.7 |  |
| PC-05 | M3 | PrettyChat | PC.8 |  |
| PC-06 | M3 | PrettyChat | PC.9 |  |
| PC-10 | M3 | PrettyChat | PC.5 |  |
| PC-11 | M3 | PrettyChat | P.3, PC.6 |  |
| PC-12 | M3 | PrettyChat | PC.4 |  |
| PC-13 | M3 | PrettyChat | PC.1, PC.2, PC.10 | upgrade carry-over check, no SV migration |
| PC-18 | M3 | PrettyChat | PC.3 |  |
| PC-22 | M3 | PrettyChat | Q.12 |  |
| WG-02 | M3 | WhatGroup | WG.8 |  |
| WG-03 | M3 | WhatGroup | WG.9 |  |
| WG-04 | M3 | WhatGroup | WG.10 |  |
| WG-05 | M3 | WhatGroup | WG.11 |  |
| WG-06 | M3 | WhatGroup | WG.4 |  |
| WG-07 | M3 | WhatGroup | P.2 |  |
| WG-08 | M3 | WhatGroup | WG.12 |  |
| WG-11 | M3 | WhatGroup | WG.1, WG.2, WG.12 | upgrade carry-over check, no SV migration |
| WG-12 | M3 | WhatGroup | WG.6, X2.1 | reconcile: owner ruling, degraded verbs |
| WG-13 | M3 | WhatGroup | WG.5 |  |
| WG-15 | M3 | WhatGroup | Q.8 |  |
| WG-16 | M3 | WhatGroup | Q.9 |  |
| WG-17 | M3 | WhatGroup | WG.3 |  |
| WG-DOCS | M3 | WhatGroup | WG.13 |  |
| CM-03 | M3 | ConsumableMaster | CM.7 |  |
| CM-04 | M3 | ConsumableMaster | CM.11 |  |
| CM-05 | M3 | ConsumableMaster | CM.13 |  |
| CM-06 | M3 | ConsumableMaster | CM.12 |  |
| CM-09 | M3 | ConsumableMaster | CM.5 |  |
| CM-11 | M3 | ConsumableMaster | CM.10 |  |
| CM-15 | M3 | ConsumableMaster | CM.4 |  |
| CM-16 | M3 | ConsumableMaster | CM.1, CM.14 |  |
| CM-17 | M3 | ConsumableMaster | CM.6 |  |
| CM-18 | M3 | ConsumableMaster | X2.8 |  |
| CM-19 | M3 | ConsumableMaster | CM.1, CM.2 | upgrade carry-over check, no SV migration |
| CM-20 | M3 | ConsumableMaster | CM.8 |  |
| CM-21 | M3 | ConsumableMaster | CM.3 |  |
| CM-29 | M3 | ConsumableMaster | CM.9 |  |
| AM-03 | M3 | AuraMaster | AM.7 |  |
| AM-04 | M3 | AuraMaster | AM.6 |  |
| AM-07 | M3 | AuraMaster | AM.3 |  |
| AM-08 | M3 | AuraMaster | P.4, AM.14 |  |
| AM-09 | M3 | AuraMaster | AM.5 |  |
| AM-10 | M3 | AuraMaster | AM.16 |  |
| AM-12 | M3 | AuraMaster | AM.4 |  |
| AM-13 | M3 | AuraMaster | AM.10 |  |
| AM-14 | M3 | AuraMaster | AM.1, AM.2 | upgrade carry-over check, no SV migration |
| AM-15 | M3 | AuraMaster | AM.8 |  |
| AM-16 | M3 | AuraMaster | X2.9 |  |
| AM-17 | M3 | AuraMaster | AM.9 |  |
| AM-19 | M3 | AuraMaster | AM.12 |  |
| AM-20 | M3 | AuraMaster | AM.13 |  |
| AM-23 | M3 | AuraMaster | AM.11 |  |
| AM-32 | M3 | AuraMaster | AM.15 |  |
| KC-03 | M3 | KickCD | KC.10, KC.15 |  |
| KC-04 | M3 | KickCD | KC.2 |  |
| KC-05 | M3 | KickCD | Q.11 |  |
| KC-06 | M3 | KickCD | KC.6 |  |
| KC-07 | M3 | KickCD | KC.12 |  |
| KC-08 | M3 | KickCD | KC.13 |  |
| KC-10 | M3 | KickCD | KC.8 |  |
| KC-12 | M3 | KickCD | KC.5 |  |
| KC-13 | M3 | KickCD | KC.4 |  |
| KC-14 | M3 | KickCD | KC.14 |  |
| KC-15 | M3 | KickCD | KC.11 |  |
| KC-17 | M3 | KickCD | KC.1 | upgrade carry-over check, no SV migration |
| KC-18 | M3 | KickCD | KC.7 |  |
| KC-19 | M3 | KickCD | X2.10 |  |
| KC-20 | M3 | KickCD | KC.9 |  |
| KC-23 | M3 | KickCD | KC.3 |  |

# Sign-off

Fill in as each session runs. One row per session; list failing step ids in Notes with the exact chat text.

| Session | Date | Build / tag | Tested? | Pass/Fail | Failing steps and notes |
|---|---|---|---|---|---|
| P | | | | | |
| L | | | | | |
| BL | | | | | |
| PF | | | | | |
| MM | | | | | |
| LH | | | | | |
| AT | | | | | |
| PM | | | | | |
| PC | | | | | |
| WG | | | | | |
| CM | | | | | |
| AM | | | | | |
| KC | | | | | |
| Q | | | | | |
| X1 | | | | | |
| X2 | | | | | |
| X-ru | | | | | |
