# 06 — Smoke Tests

**Everything in this plan that no out-of-game suite can reach, as steps a player runs in the client.**

> **Nothing below has been performed.** No step here has been run against a client as part of producing
> this bundle, and none of the work it checks has been done. Every step describes a check on a change
> that does not exist yet. See `00_OVERVIEW.md`.

---

## What is not here

The four out-of-game suites — `luacheck`, the headless harness, `tests/perf.lua` and `lizard` — are
green in all ten repositories today at the figures the per-repo bundles recorded, and every work item
carries its own headless verification in `04_EXECUTION_PLAN.md`. None of that is repeated here.

This document covers only the five things a headless suite structurally cannot see:

1. **Rendering.** A dropdown that populates, a texture that hides, a control that lands in the right band.
2. **Taint.** "Interface action failed because of an AddOn" is never a test failure.
3. **The Blizzard options list.** Combat refusals, category registration, duplicated entries.
4. **SavedVariables on a real store.** A migration that reads what the client actually wrote at logout.
5. **Cross-addon interaction in one session.** Nine addons sharing AceGUI's widget registry and its
   frame pool, which no repository's suite can even observe.

Each addon's own `docs/smoke-tests.md` is the standing pass and is referenced rather than restated. Where
a step below is already covered there, the reference is the step — run the existing one, and read the
line here for what has changed about it.

## Conventions

Taken from the collection's own smoke docs so the vocabulary matches
(`KickCD/docs/smoke-tests.md:10-17`, `LootHistory/docs/smoke-tests.md:17-31`).

- **`/reload`** abbreviates `/console reloadui`.
- **BugSack / BugGrabber**, or the stock error frame under `/console scriptErrors 1`, is the primary
  regression signal. A clean run is "no error thrown at any point".
- **Chat banner** — every line an addon prints carries its own bracketed prefix. A missing or doubled
  banner is a bug in its own right.
- **"In combat"** means auto-attacking a training dummy is enough; the gates read
  `PLAYER_REGEN_DISABLED` / `_ENABLED`.
- **Pass** lines say what success looks like. If a step says "should X" and X does not happen, the smoke
  test failed — record the addon, the step and the exact chat text.
- **Back up `WTF/` before session 2.** It is the only session that can lose settings, and it edits a
  copy of the account's SavedVariables on purpose.

## Session index

`04_EXECUTION_PLAN.md` marks every item carrying a check that cannot be made out of game with `⚠` and
assigns it a session. **There are eighteen, and every one of them is in a session below.** The reverse
does not hold and is not meant to: a session also picks up checks on items that *can* be proved headless,
because the operator is already logged in. Those steps are marked **(opportunistic)** and are never the
reason a login is scheduled — if you drop them the session still earns its place. A step that is *not*
marked opportunistic and does not name a `⚠` item is a defect in one of the two documents. The sessions
are batched because each costs a login, several need combat, and one needs five addons loaded at once —
running them item by item across five milestones costs a login per item and finds nothing extra.

| Session | Milestone | After | Needs | Rough cost |
|---|---|---|---|---|
| **1 — combat and taint** | M2 | Lanes E and F | a dummy, one character | 12 min |
| **2 — SavedVariables** | M2 | Lane B | a **copy** of `WTF/`, two profiles | 15 min |
| **3 — panels and pooling** | M2, M4 | Lane A, then `M4-01`, `M4-15`, `M4-16` | nothing special | 20 min |
| **4 — the media dropdowns** | M3 | `M3-01`, then again after `M3-02` | LibSharedMedia with a registered face | 6 min |
| **5 — the shared widget registry** | M4 | `M4-02`, and again after each of `M4-04` … `M4-08` | five addons loaded together | 20 min, spread |
| **6 — locale** | M5 | `M5-08`, which owns it | a non-English client | 15 min |

**Total for the plan's own five: about seventy-five minutes**, most of it session 5, which is
deliberately run six times against a one-line change each, and session 3, which now also cycles the tab
strip in all nine addons after the `M4-01` wave.

---

# M1 — nothing in-client, and that is not an omission

**Zero steps.** Every one of Milestone 1's 38 items lands in LibKa0s, WowAddonStandards or the
`wow-addon` plugin. None of the three is an addon: LibKa0s has no TOC a client loads, and the other two
are documentation. Nothing M1 changes reaches a client until an addon vendors it, which is M3 and M4.

Three M1 items change bytes a player eventually sees, and each is checked at the commit that vendors it
rather than at the commit that writes it. `M1-LK-02`, the three-line composed-media fix — **session 4**,
under `M3-01`. `M1-LK-03`, the pooled tab strip, which re-dresses buttons every addon's settings panel
renders — **session 3**, under `M4-01`. `M1-LK-11`, which rewrites five player-facing strings in
`LibKa0s/Perf.lua` — the M4 table at the end of this document, under `M4-01`. None of the three is an M1
step, and none of them is nobody's.

---

# M2 — the defects that need no upstream anything

Eleven `⚠` items across three sessions — `M2-02`, `M2-05`, `M2-07`, `M2-08`, `M2-11`, `M2-16`, `M2-17`,
`M2-18`, `M2-20`, `M2-21`, `M2-22`. This is the milestone holding every reachable defect in the collection, and it is the
one to run first.

## Session 1 — combat and taint

Run after M2 Lanes E and F. One login, a training dummy, and about twelve minutes.

### 1.1 · The sidebar combat refusal, three addons — `M2-16`, `M2-17`, `M2-18`

`O.SetRenderer` owns the Blizzard-sidebar combat refusal at `LibKa0s/Options.lua:700-716`. AbsorbTracker
has zero callers today and drives three pages off a raw `OnShow`; KickCD's Profiles and Spells pages and
MultiMeters' Profiles page are off it too. All three addons document a refusal they do not deliver.

1. Enter combat on a dummy.
2. From the Blizzard **Settings → AddOns** sidebar, open AbsorbTracker. Then KickCD. Then MultiMeters.
3. For each, walk every sub-page in the addon's category.

**Pass** — each addon prints its refusal line and the panel closes, on every page, in all three addons.
**Fail** — a page renders in combat, or one addon refuses and another does not.

Existing coverage: `AbsorbTracker/docs/smoke-tests.md:24` § C, `KickCD/docs/smoke-tests.md:363` § 14,
`MultiMeters/docs/smoke-tests.md:209` § 4. Each of those three asserts the refusal already. **The point
of this step is that they currently pass for the wrong reason in AbsorbTracker's case** — its pages
never opened the sidebar path the refusal guards — so run them again against the changed code rather
than trusting the last green.

### 1.2 · ConsumableMaster registers its category out of combat — `M2-08`

`settings/Panel.lua:866-867` calls `Settings.RegisterAddOnCategory` from a `PLAYER_LOGIN`/`ADDON_LOADED`
bootstrap with no `InCombatLockdown` gate, and an in-combat `/reload` reaches it.

1. Enter combat. Stay in combat.
2. `/reload`.
3. Watch chat and the error frame through the reload and for ten seconds after.
4. Leave combat. Open **Settings → AddOns**.

**Pass** — no taint error at any point, and ConsumableMaster's category is in the list after regen, not
before. **Fail** — "Interface action failed because of an AddOn", or the category never appears.

Existing coverage: `ConsumableMaster/docs/smoke-tests.md:150` § 6 covers combat deferral for macro
writes. This is the same gate on a different call and needs its own pass.

### 1.3 · WhatGroup's reset popup does not touch the global — `M2-20`

`settings/Schema.lua:577` assigns `StaticPopupDialogs = StaticPopupDialogs or {}` directly beneath a
comment explaining that registration is deferred precisely to avoid touching the table.

1. Out of combat: `/wg`, open the settings page, press **Defaults**, confirm the popup, dismiss it.
2. Enter combat and do it again.
3. Open the game menu and **Log out**, then cancel.

**Pass** — the popup shows and dismisses in both states, and the logout attempt raises nothing.
**Fail** — any "Interface action failed because of an AddOn", especially at the logout step.

Existing coverage: `WhatGroup/docs/smoke-tests.md:33` § 1.3 is the standing taint regression and is
marked CRITICAL there. Run it verbatim; step 3 above **is** that section. `:123` § 3.4 covers the
Defaults button itself.

### 1.4 · WhatGroup's frame follows a combat transition — `M2-21`

`modules/Frame.lua:148-151` never re-evaluates visibility across a transition. The gate is read at every
`ShowFrame`, so the option is not inert — only the mid-window change is missed.

1. With "hide in combat" on and an application pending, get the frame on screen out of combat.
2. Enter combat without dismissing it.
3. Leave combat.

**Pass** — the frame hides on entering combat and returns on leaving it, with the pending info intact.
**Fail** — the frame stays up in combat, or does not come back.

Also here: with the frame **hidden**, confirm the cooldown ticker is not running — `:275` arms it
regardless today. The observable is that a hidden frame's teleport countdown is not being driven; check
it by leaving the frame hidden for a full cooldown and confirming the button is correct when it returns.
Existing coverage: `WhatGroup/docs/smoke-tests.md:239` § 4.1a.

### 1.5 · Two concurrent applications pair correctly — `M2-22`

`core/WhatGroup.lua:678` binds `table.remove(captureQueue, 1)` to whatever application id arrives, which
is positional. Two outstanding applications is the case that exposes it.

1. Apply to two group-finder listings in quick succession.
2. Let both resolve — one accepted, one declined, in either order.

**Pass** — each notification names the group it belongs to. **Fail** — the two swap, or a declined
application leaves a stale entry behind.

Existing coverage: `WhatGroup/docs/smoke-tests.md:289` § 5, specifically § 5.2 *Multiple concurrent
applications*. That section exists and is the right one; the plan's change is what makes it able to fail
for the right reason.

### 1.6 · Three small ones while you are here — `M2-22`, `M2-11`

- **BankLedger** — `/bl` → reset everything, then without reloading, capture a bank movement. **Pass:**
  the capture gate re-reads immediately; today it stays stale until reload.
- **KickCD** — `/kcd` debug dump on a client with and without `C_CurveUtil`. **Pass:** the secret branch
  prints in both. Existing coverage: `KickCD/docs/smoke-tests.md:437` § 19.
- **MultiMeters** — `/mm debug of`. **Pass:** a rejection line. Today it prints the full report and
  leaves the trace armed.

## Session 2 — SavedVariables

**Back up `WTF/` first. Work on a copy.** This is the only session in the plan that can touch existing
player data, and both defects are in migration runners that a wrong fix would run against a real ledger.

### 2.1 · BankLedger's v1 → v2 ladder actually runs — `M2-05`

`defaults/Global.lua:14` ships `schemaVersion` as an AceDB default, so `core/Database.lua:17`'s
`g.schemaVersion or 1` always reads the current version and the `< NS.SCHEMA_VERSION` arm at `:21` has
never run on a real store.

1. Copy `WTF/Account/<ACCOUNT>/SavedVariables/BankLedger.lua` aside.
2. Hand-edit the **copy**: delete the `schemaVersion` key, add one `vendorPrice` row.
3. Put the copy in place and log in.
4. `/bl debug` on, watch the migration line.
5. Log out. Reopen the file.

**Pass** — `v1 -> v2, 1 rows touched` in the debug output, and after logout the file carries
`schemaVersion = 2` and the migrated row. **Fail** — no migration line (the defect), or a line with a
row count that does not match what you planted.

Existing coverage: `BankLedger/docs/smoke-tests.md:634` § 14 *SavedVariables integrity* and `:362` § S-15
*Test mode*. Neither can see this today because the ladder is unreachable.

### 2.2 · ConsumableMaster migrates a second profile — `M2-07`

`core/Database.lua:65-90` reads and stamps `g.schemaVersion`, which is account-wide, while both steps
write `db.profile`. The `OnProfileChanged` hook at `core/ConsumableMaster.lua:401-410` is therefore inert
on any profile after the first.

1. On an existing character with migrated settings, open the Profiles page.
2. Create a **new** profile and switch to it.
3. Watch chat with debug on.

**Pass** — the migration line fires for the new profile. **Fail** — silence, which is what happens today.

4. Switch back to the original profile and confirm nothing was re-run and nothing was lost.

Existing coverage: `ConsumableMaster/docs/smoke-tests.md:150` § 5 covers spec changes; the profile switch
itself has no standing step, which is part of why this went unnoticed.

### 2.3 · Nothing else moved

With both migrations landed, log in on each of the nine addons in turn and confirm your settings,
positions, profile selection and window geometry are exactly as you left them. This is cheap and it is
the check that catches a migration that ran when it should not have.

## Session 3 — panels and pooling (M2 half)

### 3.1 · The landing logo does not ride the pool — `M2-02`

PrettyChat hand-copied LibKa0s's landing renderer at `settings/Panel.lua:646-721` and omitted the
`OnRelease` that hides the logo texture. AceGUI's `SimpleGroup` pool is **shared with every other addon
in the session**, so a 300px texture can ride into the next widget that takes the group.

1. Open **Settings → AddOns → PrettyChat**. Land on the landing page and let it draw.
2. Without closing the window, page to another Ka0s addon's settings — BankLedger and PanelMaster are
   the easiest, both draw wide groups.
3. Page back and forth three or four times.
4. Close the window, `/reload`, repeat once.

**Pass** — no logo, no ghost texture, no unexpected vertical gap on any page of any addon. **Fail** — a
300px image or a 300px hole appearing where nothing drew it, in *any* addon's panel.

Existing coverage: `PrettyChat/docs/smoke-tests.md:91` § S and `:489` § K. The leak crosses addons, so
neither of those alone would catch it — step 2 is the whole test.

### 3.2 · PrettyChat's format writer refuses a surplus conversion — `M2-01` *(opportunistic)*

Not in-client-only — the refusal is testable headless, which is why `M2-01` carries no `⚠` — but the
failure it prevents is, because the raise happens inside Blizzard's chat handler, not in the addon. Worth
two minutes while the panel is open; not worth a login of its own.

1. `/pc`, open a chat format row, and enter a format with one more `%s` than the shipped default.
2. Save.

**Pass** — the write is refused with a message naming the signature. **Fail** — it saves, and then the
first matching chat line raises a Lua error from a Blizzard frame.

3. Enter a valid format that reorders or truncates the shipped conversions. **Pass:** accepted.

Existing coverage: `PrettyChat/docs/smoke-tests.md:49` § O and `:219` § L.

---

# M3 — adoption of v1.26.0

One session, and it is the shortest and highest-value in the plan: it is the proof the collection's only
Critical is fixed.

## Session 4 — the media dropdowns

### 4.1 · KickCD's eight rows populate — `M3-01`

Run **after `M3-01` and before `M3-02` opens**. KickCD's re-vendor carries no KickCD code change at all.

1. `/kcd config`.
2. Open **Icons**, **Label** and **Castbar**.
3. Open every font, border and bar-texture dropdown on those three pages — eight rows:
   `settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`,
   `settings/Label.lua:184`.
4. `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose`.

**Pass** — every one of the eight lists real media names, the dump reports **3**, and selecting a face
changes what renders. **Fail** — any empty dropdown, or a dump reporting 2, which means the payload did
not land.

Existing coverage: `KickCD/docs/smoke-tests.md:424` § 18 *LSM dropdown rendering* is exactly this
scenario and has been passing against empty lists, because it checks the control draws rather than that
it has entries. Run it, then run step 3 above, which is the part it does not assert.

### 4.2 · MultiMeters' media list is still deferred — `M3-02`

This is the one step in the plan that catches a regression the plan itself introduces. `M1-LK-02` moves
`__AttachCompose` from calling a host's `LSMValues` at render time to calling it once at row-declaration
time. MultiMeters supplies a table-returner at `settings/Schema.lua:670`; if the revert is missed, its
rows take a media list **frozen at file load** — no crash, no warning, nothing red anywhere.

1. Run **after `M3-02`**, with a media addon loaded that registers a font or a bar texture *late* —
   anything that registers on `PLAYER_LOGIN` rather than at file scope. A profile-swapped LibSharedMedia
   pack does this.
2. `/mm`, open the settings page, open a font dropdown.

**Pass** — the late-registered face is in the list. **Fail** — the list is complete but missing exactly
the faces that registered after MultiMeters' files loaded. That difference is the entire signal.

Existing coverage: `MultiMeters/docs/smoke-tests.md:209` § 4 sweeps the settings panel and will not see
this; the late-registration condition in step 1 is what makes the check able to fail.

### 4.3 · The three workaround deletions changed nothing — `M3-03`, `M3-04` *(opportunistic)*

AbsorbTracker and ConsumableMaster each carried a private rewrite of every composed row's `values`, and
both come out with the re-vendor.

1. `/at` → Appearance. Every font, border and texture dropdown lists media.
2. `/cm` → Macro bar. Same.

**Pass** — identical to before the change, from the player's side. This is a step whose success is that
nothing happened. Existing coverage: `AbsorbTracker/docs/smoke-tests.md:30` § D and `:47` § E;
`ConsumableMaster/docs/smoke-tests.md:403` § 11a.

### 4.4 · The five no-op re-vendors — `M3-05` *(opportunistic)*

BankLedger, LootHistory, PanelMaster, PrettyChat and WhatGroup consume `MasterControls` and `ColorPair`
and no media composer. One login each, open the settings page, confirm nothing moved a pixel.

**Pass** — five panels identical to the last time you saw them.

---

# M4 — adoption of v1.27.0

Two sessions. Session 5 is the only proof `C02` has and it is run six times.

## Session 5 — the shared widget registry

Five addons each ship a private `core/LSMPatch.lua` that re-registers `LSM30_Border` into AceGUI's
**process-global** widget registry at `currentVersion + 1` — KickCD 68 lines, PanelMaster 66,
ConsumableMaster 65, AbsorbTracker 50, MultiMeters 101, and all five differ. Whichever loads last owns
that dropdown for every addon in the client, Ka0s or not. No headless suite can see the interaction at
all.

### 5.1 · Baseline, after `M4-02` and with all five copies still in place

`M4-02` adds the library call and deletes nothing, on purpose, so there is something to compare against.

1. Load **KickCD, PanelMaster, AbsorbTracker, ConsumableMaster and MultiMeters together**.
2. Open each addon's Border dropdown in turn: `/kcd config` → Icons; `/pm` → Appearance → border;
   `/at` → Appearance; `/cm` → Macro bar; `/mm` → settings → appearance.
3. Screenshot each open dropdown.

**Pass** — all five draw the same styled control, and the styling does not change when you reorder the
load (rename one addon's folder to move it in the alphabet and repeat). **Fail** — a dropdown that looks
different from the other four, or one whose appearance depends on load order.

Existing coverage: `PanelMaster/docs/smoke-tests.md:99` § 5b *Textures (LibSharedMedia)* and
`AbsorbTracker/docs/smoke-tests.md:47` § E each cover one addon's border control. Neither is a
cross-addon check, and the cross-addon check is the one that matters here.

### 5.2 · After each of the five deletions — `M4-04` … `M4-08`

The deletions are one repository per commit, in the order KickCD, PanelMaster, ConsumableMaster,
MultiMeters, AbsorbTracker. **Repeat 5.1 after every one of the five.** That is six runs of 5.1 in total
counting the `M4-02` baseline, and it is the whole reason the deletions are five commits rather than one:
run after every deletion and a failure names one repository, run twice and you are back to bisecting the
range the split was bought to avoid.

AbsorbTracker is last because it is the one real divergence — it exposes a callable
`NS.ApplyLSMBorderPatch()` at `core/LSMPatch.lua:20` invoked from `core/AbsorbTracker.lua:52` rather than
from a `PLAYER_LOGIN` frame, so it is the deletion most likely to change load-time behaviour.

**Pass, after all five** — the five Border dropdowns are indistinguishable from the screenshots taken in
5.1, and `grep -rn 'RegisterWidgetType'` finds nothing outside `libs/` in any of the nine repositories.

### 5.3 · While five addons are loaded, the standing cross-addon sweep *(opportunistic)*

`M1-WA-01` adds this to the review playbook because nothing has ever asked it. The four collision classes
were measured by hand for this bundle and are **clean today** — recorded in `01_CONSOLIDATED_FINDINGS.md`
§ *Verified-clean negatives* so nobody re-spends the effort — but nothing repeats the measurement, and
session 5 is the one login where all five are up anyway.

1. Type each slash root and confirm it reaches its own addon: `/at`, `/bl`, `/cm`, `/kcd`, `/lh`, `/mm`,
   `/pm`, `/pc`, `/wg`.
2. Open **Settings → AddOns** and confirm each addon appears **once**, and each multi-page addon's pages
   appear once each.

**Pass** — nine distinct roots, nine single entries. **Fail** — a root that lands in the wrong addon, or
a duplicated category.

## Session 3 — panels and pooling (M4 half)

Run after `M4-15` and `M4-16`; folds into session 3 above.

### 3.3 · PanelMaster's five page acts sit in the chrome band — `M4-15`

Copy, Enabled, Unlock, Reset and Delete move out of `sections[TAB_GENERAL]` into the `H.PageHeader` band,
and the emptied General tab goes.

1. `/pm` → **Panels**.

**Pass** — the five controls are in the chrome band above the page, the General tab is gone, and each of
the five still does what it did. Press every one of them on a throwaway panel. **Fail** — an act that
lost its handler in the move, or a tab strip that now has a gap where General was.

Existing coverage: `PanelMaster/docs/smoke-tests.md:376` § 9 *Options panel* covers the page; the five
acts individually are at `:53` § 4 and `:361` § 8.

### 3.4 · Three perf panels, one close button each — `M4-16`

The `decorate` hook in three addons redraws the close button `LibKa0s/PerfPanel.lua:191-196` already
draws, anchor for anchor.

1. `/at perf`, `/kcd perf`, `/mm perf`.

**Pass** — each panel opens with exactly **one** close button, in the same place in all three, and it
closes the panel. **Fail** — two overlapping buttons, or a button that moved.

Existing coverage: `AbsorbTracker/docs/smoke-tests.md:124` § L, `KickCD/docs/smoke-tests.md:437` § 19,
`MultiMeters/docs/smoke-tests.md:1071` § 18.

### 3.5 · The tab strip survives being pooled and re-dressed — `M4-01`

`M1-LK-03` rewrites `TabStrip` (`LibKa0s/OptionsWidgets.lua:1050-1072`) to acquire its buttons and its
content panel from per-`ctx` `LibKa0s-Pool-1.0` pools, and splits `makeTab` (`:942`) into `newTabButton`
plus `dressTab` with `OnClick` re-set on every dress. `TabStrip` renders in the live settings code of
**all nine** addons. Its only headless proof counts `CreateFrame` calls on a second selection pass; the
four `C12` findings that would pin band geometry as invariant under selection are deliberately deferred
to kit 16, because the shared mock's `GetHeight` returns 0. **So a stale label, a mis-anchored button or
a wrong band height on a re-dressed tab is invisible to every automated check in this bundle.**

1. Run after `M4-01` has landed in the first consumer, and again after the full wave.
2. In each of the nine, open the multi-tab settings panel — `/at`, `/bl`, `/cm`, `/kcd`, `/lh`, `/mm`,
   `/pm`, `/pc`, `/wg` — and cycle every tab three times, ending back on the first.
3. Watch three things per tab: the **label** is the tab's own, the **selected** tab is the one you
   pressed, and the strip's **band height** does not change as you move through it.

**Pass** — nine panels, every tab labelled and selected correctly on all three passes, no band that
grows or shrinks. **Fail** — a label from the previously-dressed tab, a selection highlight on the wrong
button, a body drawn under the wrong tab, or a strip whose height moves between passes.

Existing coverage: each addon's own `docs/smoke-tests.md` covers its settings pages, but none of them
opens a tab three times, which is what a reuse defect needs to show itself.

## The M4 items with a visible surface but no session of their own

Fold these into whatever login is convenient. Each is a one-line look.

| Item | Check | Pass |
|---|---|---|
| `M1-LK-11`, via `M4-01` | The library's five player-facing `Perf.lua` strings, which reach a client only when an addon vendors v1.27.0 — **not `M4-13`, whose repos are ConsumableMaster, KickCD and WhatGroup and whose grep excludes `libs/`**. Two are `CANCELLED` (`:948`, `:1063`) and three are `unlabelled` (`:723`, `:864`, `:1029`), so one capture cannot see all five: start a **labelled** capture (`/at perf start mylabel`) and finish it, then start an **unlabelled** one and cancel it. | The started line names the label; the unlabelled start, the report header and the cancel line all read "unlabeled" and "canceled". |
| `M4-13` | The addon-side spelling sweeps — ConsumableMaster 25 live sites, KickCD 37, WhatGroup three comments. Only the ones in strings a player reads are visible: `/cm`, `/kcd config`, `/wg`. | No `colour`, `behaviour` or `grey` in any panel label, tooltip or chat line. |
| `M4-21` | KickCD's three cast-bar description keys are used but absent from `locales/enUS.lua`. `/kcd config` → Castbar. | Every row shows a sentence, not a bare key. Existing coverage: `KickCD/docs/smoke-tests.md:635` § 25, the `L` trap. |
| `M4-23` | Two icon-catalog swaps: LootHistory's READY/NOTREADY/INFO_ICON at `settings/Panel.lua:459-461`, MultiMeters' `ENABLED_TEX`/`DISABLED_TEX` at `settings/ColumnBlocks.lua:60-61`. **They move together or neither moves** — MultiMeters' comment cites ConsumableMaster parity. | The three marks render, and MultiMeters' column blocks look the same as ConsumableMaster's. |
| `M4-18` | PanelMaster's `ParseColor` divides a shorthand alpha by 255 under byte-scale RGB. Set a panel colour with a three-digit shorthand, `/reload`. | The colour survives the round trip unchanged. Existing coverage: `PanelMaster/docs/smoke-tests.md:129` § 5b-2. |
| `M4-18` | KickCD's anchor fallback at `settings/Panel_Render.lua:304` carries `y = -180` against `defaults/Profile.lua:314`'s 120. Reset the cast bar to defaults. | It lands where the default says, not 300px away. |
| `M4-10`, `M4-11`, `M4-12`, `M4-14`, `M4-24`, `M4-25`, `M4-26` | Nothing player-visible: line endings, lint config, TOC comments, cap dispositions, exemption evidence, and the two complexity items — `M4-25` splits a KickCD **test** function and `M4-26` writes dispositions, neither of which changes a shipped byte. | — |

---

# M5 — nothing in-client

**Zero steps of its own — except session 6, which `M5-08` owns and which is below.** Seven of M5's eight
items are record and documentation work: regenerating the automated-test record, sweeping the deviation
registers, README and ARCHITECTURE structure, the missing Tier 2 docs, the comment sweep, the fresh audit
round and the issue filing. None of that changes a shipped byte a client loads.

The one thing worth doing at the end of M5 is a **final nine-addon login** — load everything, open every
settings page once, `/reload`, and confirm nothing regressed across the whole plan. Fifteen minutes, and
it is the only step that sees M2 through M4 together.

---

# Session 6 — the locale pass

**Owned by `M5-08`**, which schedules this pass, records its outcome, and writes a locale section into
the six `docs/smoke-tests.md` files that have none. That last half matters: `M1-WA-05` scaffolds the step
into `commands/new-addon.md` and nothing else, so on its own it fixes the gap only for addons that do not
exist yet. It is here rather than in an addon's own document because the client is the only witness, and
because one of the seven unmapped findings cannot be written without it.

Only three of nine addons carry a non-English-client step today: `ConsumableMaster/docs/smoke-tests.md`
§ 3c, `KickCD/docs/smoke-tests.md:229` § 9b, and MultiMeters' CSV header check. The two addons whose code
is *most* locale-sensitive have none.

On a deDE or frFR client:

### 6.1 · LootHistory's tooltip fallback

`core/Compat.lua:188-195` defines four English wordings — `WARBAND_LINES`, `BIND_TO_WARBAND_PREFIX`,
`UE_LITERAL = "until equipped"` — as the fallback when the client leaves `ITEM_ACCOUNTBOUND*` nil, and
`:230-231` reaches them. The same file calls the tooltip "the ONLY witness" for items whose bind type
lies. Every headless case for that path asserts against enUS mock globals — `tests/test_compat.lua:65-66`
passes the literal strings "Auction House" and "Auction won: …".

1. Loot a warband-bound item and a bind-on-equip item.
2. `/lh` → History, check the bind column and the source attribution on both.

**Pass** — both classify correctly. **Fail** — either falls back to the English literal and misclassifies.

### 6.2 · PrettyChat's whole function

PrettyChat overwrites localized `_G` chat format strings, and its 797-line smoke doc has no locale step.

1. Trigger one line from each override family: a reputation change, a guardian XP gain, a loot line.

**Pass** — each renders with the localized wording and no `%d` or `%s` artifact. **Fail** — an English
sentence on a German client, or a stray conversion character.

### 6.3 · WhatGroup's `IsSpellKnown` rung — `WHATGROUP-R-06`

This is the check the fix waits on, not a check of a fix. `core/Compat.lua:62-67` calls the bare
`IsSpellKnown` global and returns false when it is absent, while its five siblings at `:24`, `:40`,
`:52`, `:83`, `:105` all try `C_Spell.*` first.

1. `/dump C_SpellBook.IsSpellKnown(<a spell you know>)` and `/dump IsSpellKnown(<the same>)`.

**Pass** — both resolve and agree. Record the result: the finding's own fix text says the modern rung
goes in **only once an in-client check confirms both APIs present and agreeing**, and this is that check.
`05_TRACEABILITY.md` § 3b carries the finding as unmapped for exactly this reason.

### 6.4 · The three that already have a step

Run them as written: `ConsumableMaster/docs/smoke-tests.md` § 3c (localized `subType`, macros still
populate), `KickCD/docs/smoke-tests.md:229` § 9b (issue #8, the grid populates on frFR), and MultiMeters'
CSV header (`snake_case`, never localized, byte-identical to the enUS header).

---

# If a step fails

Note the addon, the step number, and the exact chat text. The four out-of-game suites are green in all
ten repositories, so a failure here is one of a short list:

- **A rendering or lifecycle regression** from the options work — sessions 1, 3 and 4, most likely in
  AbsorbTracker, KickCD, MultiMeters or PrettyChat.
- **The `__AttachCompose` contract change** — session 4.2 specifically. If MultiMeters' `M3-02` revert was
  missed, the symptom is a media list that is complete except for late registrations, and nothing else in
  the collection will tell you.
- **The registry sentinel** — session 5, after a deletion. Bisect on the five deletion commits; that is
  what they are for.
- **A migration** — session 2, and this is why the session works on a copy.

Each maps to a single commit; `git log --oneline` in the addon's repository, matched on the item id in
the commit subject, isolates it.
