# 08 — The In-Game Smoke Checklist

**What this cycle owes a client, arranged for the person who has to sit down and run it.**

> **Nothing below has been run.** No step in this document has been performed against a WoW client, by
> anyone, at any point in the 2026-09-07 remediation cycle — no client was available while the work was
> being done. Every pass condition here describes what someone will see when they look, not what anyone
> saw. `07_EXECUTION_RECORD.md` § *Nothing in this cycle was verified in a WoW client* is the measured
> statement of that; this document is the work list it implies.

---

## What this is, and what it is not

106 of 107 work items landed across thirteen repositories. Twenty-eight `Smoke, session N` steps were
written into eight addons' `docs/smoke-tests.md` while that happened, plus six non-English-client
sections `M5-08` scaffolded, `M4-03` — which is smoke-only and has nothing to implement — and a handful
of one-line looks that `06_SMOKE_TESTS.md` files under M4 with no session of their own. This is all of
it in one place, in the order worth running it.

**The addon's own `docs/smoke-tests.md` is the authority for every step.** Each entry below names the
addon and the section, and the section is where the step lives next cycle. What this document adds is
grouping, ordering and setup — the things a checklist owes a player's evening that a per-repo document
structurally cannot know.

`06_SMOKE_TESTS.md` assigned the session numbers, and they are baked into twenty-eight commit-landed
step headers across eight repositories. **Those numbers do not change here.** The running order does:
the sessions below are numbered by when to run them and labelled with the session they are.

## Conventions

Taken from the collection's own smoke docs so the vocabulary matches.

- **`/reload`** abbreviates `/console reloadui`.
- **BugSack / BugGrabber**, or the stock error frame under `/console scriptErrors 1`, is the primary
  regression signal throughout. "No error thrown at any point" is part of every pass condition below
  whether it is restated or not — and **§ 4.5 of WhatGroup's document cannot fail visibly without one
  of the two enabled**, so turn it on before session 1.
- **"In combat"** means auto-attacking a training dummy. The gates read `PLAYER_REGEN_DISABLED` /
  `_ENABLED` and do not care what is hitting back.
- **Fail** lines say what the defect looks like. A step whose failure mode is not stated is not
  runnable, so every step below carries one.
- **Record what you see, including on a pass.** Four steps here — LootHistory 18a, PanelMaster 22.1,
  WhatGroup 12b.5, BankLedger S-27.2 — exist to *obtain* a reading that exists nowhere in any
  repository. A pass with no recorded value is a step that has to be run again.

---

## The three checks with no prior coverage at all

Everything else below re-runs an existing step against changed code, or runs one that was written this
cycle against a surface that already had a neighbour. These three are new ground, and if client time
runs out they are the ones that leave a real hole:

- **PrettyChat's pooled-logo leak, crossing into another addon's panel** — PrettyChat § T-29c, run
  order 3. AceGUI pools the `SimpleGroup` frame across every addon in the session, so the leak lands in
  *somebody else's* settings page. No headless case and no PrettyChat-only pass can see it; the check is
  the paging between two addons, not either addon on its own.
- **The late-registration media check** — MultiMeters § 4 (the eleven-picker bullet), run order 2. It is
  the only signal in the collection for `M1-LK-02`'s `__AttachCompose` contract change. If MultiMeters'
  `M3-02` revert had been missed the dropdowns would be complete except for the faces registered after
  MultiMeters' files loaded — no crash, no warning, nothing red anywhere.
- **The five-addon load-order sweep** — `M4-03`, run order 4. Five addons in one client, one
  process-global widget-registry slot. `M4-03` is smoke-only by construction; it has no commit because
  there was nothing to implement, only something to look at, and nobody has looked.

## The two that gate something

- **WhatGroup § 7a, run from § 12b step 5 (run order 6).** The `C_SpellBook.IsSpellKnown` observation is
  what `WHATGROUP-R-06` waits on. `M5-10` shipped a recorded wait rather than the rung, because adding
  it without the observation would be inventing the evidence the finding asks for. **Until the six
  readings are written down, that finding cannot be fixed either way** — both outcomes close it, and a
  blank is the only result that does not.
- **WhatGroup § 4.5 (run order 1).** The only thing in the collection that can see the
  `ADDON_ACTION_BLOCKED` the owner reported on 2026-09-07 —
  `AddOn 'WhatGroup' tried to call the protected function 'WhatGroupFrame:Hide()'`. `M2-28` taught the
  addon's mock to model frame protection and four cases pin the behaviour, but **the mock records a
  refusal; only the client raises the error.** Nothing gates on it formally. It gates on it in fact:
  `M2-21` built on a comment that asserted the opposite, and the client is what caught that.

---

## Before you log in

| # | Session | What to arrange first | Time |
|---|---|---|---|
| 1 | **Session 1 — combat and taint** | A training dummy. BugGrabber or `/console scriptErrors 1` **on**. One character. The last step wants two live group-finder applications, so be somewhere you can queue. | 20 min |
| 2 | **Session 4 — the media dropdowns** | A media addon that registers **late** — on `PLAYER_LOGIN` rather than at file scope; a profile-swapped LibSharedMedia pack does this. KickCD, MultiMeters, AbsorbTracker and ConsumableMaster loaded. | 12 min |
| 3 | **Session 3 — panels, pooling and the tab strip** | All nine addons loaded. A throwaway PanelMaster panel to press Delete on. One step wants `KickCD/libs/LibKa0s` renamed aside; one wants two hostile casters mid-pull. | 30 min |
| 4 | **Session 5 — the shared widget registry** | KickCD, PanelMaster, AbsorbTracker, ConsumableMaster and MultiMeters loaded **together**, and a way to change which loads last (disable/re-enable, or rename a folder). | 15 min |
| 5 | **Session 2 — SavedVariables** | A **backed-up copy** of `WTF/`. A text editor. A second AceDB profile you are willing to create. This is the only session that can lose settings. | 25 min |
| 6 | **Session 6 — the non-English client** | A **deDE or frFR** client. A warbound drop and a warbound-until-equipped drop. An auction-house purchase. Herbs, ore and something disenchantable. A teleport spell you have learned and one you have not. | 45 min |
| 7 | **The closing login** | Everything loaded. Nothing else. | 15 min |

**Total: about 165 minutes.** `06_SMOKE_TESTS.md`'s own column summed to 88, and that figure is now
low rather than wrong: it was written before `M5-08` scaffolded six locale sections, and before the M4
correction lane added steps to session 3. Session 5 moved the other way and is shorter than planned —
see its note.

---

# 1 · Session 1 — combat and taint

**Needs:** a training dummy; BugGrabber or the stock error frame **enabled**; a group-finder queue for
1.6. **~20 minutes.**

**Why first.** Every defect here is live for a player today, and two of them poison the whole session
rather than one panel: a settings page that renders under lockdown taints Blizzard's Settings window
until logout, and a protected `Hide` refusal is the error the owner actually hit. This is also the
only session where an untouched addon can be broken by a sibling — three addons document a combat
refusal and, until `M2-16`…`M2-18`, one of them did not deliver it.

### 1.1 · The Blizzard sidebar refuses, in all three addons — `M2-16`, `M2-17`, `M2-18`

The sidebar reaches a canvas directly without going through `OpenOptionsPanel`, so the slash-command
gate never sees it. `O.SetRenderer` (`LibKa0s/Options.lua`) owns the refusal; AbsorbTracker had no
caller at all and drove three pages off a raw `OnShow`, and KickCD's Spells and Profiles pages and
MultiMeters' Profiles page were off it too.

1. Enter combat on a dummy and **stay** in combat.
2. Esc → Options → **AddOns**. Open **Ka0s Absorb Tracker** and walk General, Appearance, Profiles.
3. Then **Ka0s KickCD** — all six: General, Icons, Cast bar, Text Label, Spells, Profiles.
4. Then **Ka0s Multi Meters** — every sub-page, Profiles included.
5. Leave combat and open each page again.

**Pass** — every page closes the Settings window and prints its addon's grey refusal line; **no page
draws**; out of combat all of them render normally.
**Fail** — a page that renders in combat, one addon refusing while another does not, or eight pages
refusing and one rendering. Any "Interface action failed because of an AddOn" is a fail on its own.

> **Run these against the current build rather than trusting the last green.** AbsorbTracker's three
> pages never opened the guarded path, so the section passed for the wrong reason for its whole life.

`AbsorbTracker/docs/smoke-tests.md` § C step 13a · `KickCD/docs/smoke-tests.md` § 14 · `MultiMeters/docs/smoke-tests.md` § 4

### 1.2 · ConsumableMaster registers its category out of combat — `M2-08`

`Settings.RegisterAddOnCategory` is protected; registering under lockdown taints Blizzard's Settings
window for the rest of the session. The bootstrap does not normally land mid-fight — an in-combat
`/reload` does.

1. Log in normally and confirm the category is under **Settings → AddOns**. If it is missing here,
   stop: the rest of this step cannot tell you anything.
2. Pull a dummy, stay on it, `/reload`, and keep swinging so you come back mid-fight.
3. Watch chat and the error frame through the reload and for ten seconds after. ConsumableMaster
   should be **absent** from the AddOns list at this point.
4. Drop combat. Open **Settings → AddOns**.

**Pass** — no taint error at any point, and the category is in the list once combat ends.
**Fail** — the taint error, or a category that never comes back, which is the parked flag set with
nothing replaying it.

`ConsumableMaster/docs/smoke-tests.md` § 6a

### 1.3 · WhatGroup's reset popup no longer touches the global — `M2-20`

`Settings.EnsureResetPopup` used to assign `StaticPopupDialogs = StaticPopupDialogs or {}` — a write to
the protected global, guarding against a client that does not exist.

1. Out of combat: `/wg config`, open the settings page, press **Defaults**, confirm the popup, dismiss it.
2. Pull a target, stay in combat, do step 1 again.
3. Out of combat, Esc → **Logout**, then cancel at the confirmation.

**Pass** — the popup shows and dismisses in both combat states, and step 3 raises nothing.
**Fail** — any "Interface action failed because of an AddOn" or `ADDON_ACTION_FORBIDDEN`. **Step 3 is
the one that catches a leak**; it is § 1.3 run after a reset has touched the table.

`WhatGroup/docs/smoke-tests.md` § 1.4 (and § 1.3, which step 3 is)

### 1.4 · The popup in combat, and Close is not lost — `M2-28` — **gating**

This is the error the owner found: `AddOn 'WhatGroup' tried to call the protected function
'WhatGroupFrame:Hide()'`. The popup parents a `SecureActionButtonTemplate` teleport button, so the
client refuses `Hide` on it and on every ancestor during a lockdown. **Run with BugGrabber enabled or
this check cannot fail visibly.**

1. `/wg test` out of combat to raise the popup.
2. Pull a dummy with the popup still on screen. → No red error, nothing in BugGrabber naming
   WhatGroup, and the popup **stays up** — correct, not a bug.
3. Press **Close** while still in combat. → No error; the popup stays and one chat line reads
   *"Popup deferred until combat ends."*
4. Drop combat. → The popup disappears, honouring the press from step 3.
5. Repeat 1–2 with **General visibility = Out of combat**.
6. Set **General visibility = In combat** out of combat while holding a capture; pull, then drop.

**Pass** — no error at any point, and the deferred Close is honoured on the combat edge rather than
forgotten.
**Fail** — any red error, or a Close press in combat silently lost once combat ends.

`WhatGroup/docs/smoke-tests.md` § 4.5

### 1.5 · The visibility gate follows a combat transition — `M2-21`

The gate was read only when something opened the popup, so a transition taken with the popup already
up was missed entirely. `OnEnable` now registers both regen events.

1. **General visibility → Only out of combat**. `/wg test` so the popup is up with a capture in it.
2. Pull a dummy **without closing it**. → It hides the moment combat starts, no taint line.
3. Drop combat. → It comes back with the same capture, all six rows populated, not "No data".
4. Repeat with **Only in combat**: nothing out of combat, appears on the pull, goes on the drop.
5. `/reload` to clear the capture, then pull and drop again with *Only out of combat* set.
   → **Nothing opens.** An empty popup on a combat transition is worse than no popup.

**Also here, because it has no other observable:** with the popup hidden by the gate and a teleport on
cooldown, the countdown ticker must not be running. Leave it hidden for a stretch, let it open, and
confirm the time shown has dropped by the real elapsed amount rather than sitting where it was.

**Fail** — the popup stays up in combat; hides and never returns; returns showing "No data"; appears in
step 5; a stalled countdown; or any taint line at the transition.

`WhatGroup/docs/smoke-tests.md` § 3.8, with § 4.1a for the ticker

### 1.6 · Two concurrent applications pair correctly — `M2-22`

The pairing was positional, so with one application outstanding every possible pairing was the right
one. This is the step that only ever meant anything with more than one.

1. `/wg debug on`.
2. Apply to **two** group-finder listings in quick succession — different activities if you can, so the
   titles are told apart at a glance.
3. Let both resolve, one accepted and one declined, in either order. **If you can arrange for the
   decline to land first, do** — that is the ordering the old code got wrong.

**Pass** — the notification and popup name the group you actually joined; the console shows one
`[LFG] dropped the capture for appID=<N> (declined)` at the moment of the decline rather than at
group-leave; remaining captures are wiped at `inviteaccepted`.
**Fail** — the two swap, or the declined application's group is the one that surfaces.

> This is the step whose length is not yours to decide. If the queue will not give you two
> applications, note it and move on — the rest of the session does not depend on it.

`WhatGroup/docs/smoke-tests.md` § 5.2

### 1.7 · Two small ones while you are here — `M2-11`, `M2-22`

- **BankLedger.** Blacklist an item (History ▸ right-click, or `/bl` ▸ Filters), then `/bl` → reset
  everything, and **without reloading** move that item in or out of your bank. **Pass** — it is now
  recorded, because the reset emptied the blacklist and the capture gate re-read. **Fail** — the
  movement is dropped, or one that should be dropped is recorded, until you `/reload`; the gate holds
  its settings in cached upvalues and was judging movements by settings the reset had destroyed.
  (`BankLedger/docs/smoke-tests.md` § S-16 step 4)
- **KickCD.** Target a hostile caster mid-cast for a protected interrupt so `notInterruptible` comes
  back secret, and run `/kcd debug castbar`. **Pass** — the `isSecret=true` line is always followed by a
  `secret-tainted; …` line, whether or not `C_CurveUtil` exists on this client. **Fail** — the dump
  reports the field as secret and then says nothing further, which reads to whoever is handed the paste
  as a dump that had nothing to say. On live Retail only the evaluator-present half is observable.
  (`KickCD/docs/smoke-tests.md` § 15)

---

# 2 · Session 4 — the media dropdowns

**Needs:** a media addon that registers faces or textures **late** — on `PLAYER_LOGIN`, not at file
scope. KickCD, MultiMeters, AbsorbTracker and ConsumableMaster loaded. **~12 minutes.**

**Why second.** This is the proof that `LIBKA0S-A-01` — the collection's only Critical — is closed in a
consumer. KickCD's eight composed media dropdowns come back **empty** in a live client on the payload
players have; the fix landed on 2026-09-07 and reaches nobody until a release is cut. Twelve minutes,
and it settles the most expensive open question in the cycle.

### 2.1 · KickCD's eight rows populate — `M3-01`

Nothing here is headless-testable end to end: the harness pins that a composed row hands back a
*reader* rather than a reading, and only a live client has a LibSharedMedia that fills after the schema
files have been read.

1. Log in fresh with the media addon enabled. **Do not `/reload` before the first check.**
2. `/kcd config` → **Icons**: open **Border texture** and **Cooldown text font**.
3. → **Text Label**: open **Font**.
4. → **Cast bar**: open **Font**, and for **both** the interruptible and uninterruptible state open
   **Bar texture** and **Border texture**. That is the eight rows this item moved.
5. `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose`
6. Pick a non-default face in **Text Label → Font**; confirm the label redraws in it and survives a
   `/reload`.
7. With the client already running, enable a media addon you had disabled, `/reload`, and reopen
   **Cast bar → Bar texture**.

**Pass** — all eight list real media, not a lone `Default` and not an empty list that opens onto
nothing; the dump reports **3**; the chosen face applies live and survives the reload; the newly
registered media is in the list after step 7.
**Fail** — any empty dropdown. A dump of **2** means the vendored payload is still v1.25.0 and
CLAUDE.md's provenance line is lying; anything else means a foreign LibKa0s won the LibStub resolve. A
step 7 list identical to what it held before means `Helpers.LSMValues` is returning a **table** again
and every composed row is frozen at file load — silently, with no error and no empty control.

`KickCD/docs/smoke-tests.md` § 27

### 2.2 · MultiMeters' media list is still deferred — `M3-02` — **NEW, no prior coverage**

**The only signal for the `__AttachCompose` contract change.** `M1-LK-02` moved the composer from
asking the host for its media list at render time to asking once, at row-declaration time. MultiMeters
supplies a table-returner; if the revert had been missed, its rows would take a media list frozen at
file load — no crash, no warning, no red case.

1. With the late-registering media pack loaded, `/mm config` and open **every** media picker the addon
   draws. There are eleven: Frame → General's **Font** and **Bar texture**, Frame → **Border style**,
   Bars → **Texture** and **Border style**, Tooltip → **Bar texture** and **Bar border style**, and the
   font picker on each of Bars → Text style, Header → Title text, Columns → Header text and
   Tooltip → Text.

**Pass** — each list contains **a name that could only have come from the media pack**. Nine of the
eleven are what this step is for; Frame → General's two are written out by hand in `settings/Schema.lua`
and prove nothing.
**Fail** — a list that is complete except for exactly the faces that registered after MultiMeters'
files loaded. **A dropdown that opens and looks plausible is not a pass here.** That difference is the
entire signal, and nothing else in the collection will tell you.

`MultiMeters/docs/smoke-tests.md` § 4, the eleven-picker bullet

### 2.3 · ConsumableMaster's three rows, with nothing local propping them up — `M3-04`

The Bar border style, Button border style and Label font rows did not take their lists from the
composer at all until the re-vendor — `settings/MacroBar.lua` overrode all three because the
composer's own list came back empty. The override is gone.

1. `/cm config` → **Macro Bar**. Open **Bar border style**, **Button border style** and **Label font**.
2. Pick a different value in each.
3. `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose`
4. `/cm set macroBar.barBorderStyle "Not A Border"`, then
   `/cm set macroBar.barBorderStyle "Blizzard Tooltip"`.

**Pass** — three populated lists; the bar edge, button edges and label face change and the closed
dropdown shows the new name; the dump reads **3**; the bad value is **rejected** with the allowed values
printed and the good one accepted and tracked by the panel.
**Fail** — one empty dropdown is the whole finding; **do not read a populated other dropdown as proof**.
A `2` from step 3 means the payload on disk is not the one this commit vendored and step 1 proved
nothing. A `Not A Border` that saves is the CLI half failing open: the composed row hands the validator
a self-keyed map where every other row hands it an ordered array.

`ConsumableMaster/docs/smoke-tests.md` § 17

### 2.4 · AbsorbTracker's three, and the late registration — `M3-03`

`settings/Appearance.lua` carried a `fixMediaValues` that re-pointed every composed row on the way
past. It is deleted, so these dropdowns are filled by library code this addon has never exercised in a
client.

1. `/at config` → **Appearance**. On *Bar* open **Bar texture**, on *Border* open **Border style**, on
   *Text* open **Font**.
2. Pick a different entry in each.
3. With the media addon loaded, confirm a face **it** registers is in **Font** and a texture it
   registers is in **Bar texture**.

**Pass** — three real lists; the fill, edge and text change live and survive a `/reload`; the
registered face and texture are both present.
**Fail** — an empty dropdown means the re-vendor regressed the composer rather than fixing it. A list
holding only the Blizzard stock entries means the reader froze, which is the silent failure
`libs/LibKa0s/OptionsCompose.lua:182-186` describes.

`AbsorbTracker/docs/smoke-tests.md` § O steps 103–104

---

# 3 · Session 3 — panels, pooling and the tab strip

**Needs:** all nine addons loaded. A throwaway PanelMaster panel. `KickCD/libs/LibKa0s` renamed aside
for 3.7 — do it once and run 3.7 while you are in there. Two hostile casters for 3.8.
**~30 minutes.**

**Why third.** `M1-LK-03` rewrote `TabStrip` to acquire its buttons and content panel from pools and
re-dress them. `TabStrip` renders in the live settings code of **all nine addons**. Its only headless
proof counts `CreateFrame` calls on a second selection pass; the cases that would pin band geometry as
invariant under selection are deferred to kit 16, because the shared mock answers `GetHeight` with 0
for every frame. **A stale label, a mis-anchored button or a wrong band height on a re-dressed tab is
invisible to every automated check in this cycle**, and it is in front of a player the first time they
open a settings page.

### 3.1 · The landing logo does not ride the shared pool — `M2-02` — **NEW, no prior coverage**

A Texture is not an AceGUI child, so `ReleaseChildren` does not take the logo away with the
`SimpleGroup` that carries it — and AceGUI pools that group's frame **across every addon in the
session**. PrettyChat hand-copied the library's landing renderer and omitted the `OnRelease` that hides
the texture, so the next widget handed that frame inherited a 300px logo. **The leak lands in somebody
else's panel**, which is why no headless case and no PrettyChat-only pass can see it.

1. Open **Settings → AddOns → Ka0s Pretty Chat**. Land on the landing page and let it draw.
2. **Without closing the window**, page to another addon's settings — BankLedger and PanelMaster are
   easiest, both draw wide groups.
3. Page back and forth three or four times, visiting every page of both addons.
4. Close the window, `/reload`, repeat once.

**Pass** — the logo appears on PrettyChat's landing page and **nowhere else**. No ghost texture, no
unexplained 300px vertical gap, on any page of any addon.
**Fail** — a 300px image, or a 300px hole where nothing drew one, in *any* panel. Step 2 is the whole
test; steps 1 and 3 alone will pass through the defect.

`PrettyChat/docs/smoke-tests.md` § T-29c

### 3.2 · The tab strip survives being pooled and re-dressed — `M4-01`

Nine addons. Cycle every tab of every strip **three times**, ending back on the first, and on each pass
watch three things: the **label** is that tab's own, the **selected** tab is the one you pressed, and
the strip's **band height** does not move.

| Addon | Where | The strip worth the attention |
|---|---|---|
| ConsumableMaster | `/cm config` → General, Macro Bar, Stat Priority, any Category page | four strips, all four |
| MultiMeters | `/mm config`, every page that draws one | **Columns** — the one page driving `H.TabStrip` directly, a block editor rather than a schema group |
| KickCD | `/kcd config` → General, Icons, Cast bar | Icons, six tabs, the widest strip here |
| LootHistory | `/lh config` → General, all six tabs; then **Filters**' secondary strip | `SubTabStrip`, pooled by the same change |
| PanelMaster | `/pm` → Panels | drawn straight onto the chrome band with `H.TabStrip`, not through `RenderTabbedSchema` |
| AbsorbTracker | `/at config` → Appearance | — |
| BankLedger | `/bl config` → General | — |
| PrettyChat | `/pc config` → Categories | eight tabs |
| WhatGroup | `/wg config` | hands the whole strip to `RenderTabbedSchema` and measures no band of its own |

Then, in at least PanelMaster, PrettyChat, LootHistory and WhatGroup: **Esc, reopen, and walk the strip
once more.** The pools are per-`ctx`, so a second build is where a released frame can come back dressed
for a different tab.

**Pass** — every tab labelled and selected correctly on all three passes, in all nine, with no band
that grows or shrinks and the body under the strip always the selected tab's rows.
**Fail** — a label carried over from the previously-dressed tab; a highlight on the wrong button; a
body drawn under the wrong tab; a strip whose height moves between passes. Each is the pool handing
back a frame it did not finish dressing, and each is a **library** finding — nothing in the consuming
repo places those buttons.

`AbsorbTracker` § P step 105 · `BankLedger` § S-26 · `ConsumableMaster` § 18 · `KickCD` § 28 ·
`LootHistory` § 17k · `MultiMeters` § 29 · `PanelMaster` § 19 · `PrettyChat` § T-99 · `WhatGroup` § 12a

### 3.3 · The perf strings read US — `M1-LK-11`, via `M4-01`

`LibKa0s-Perf-1.0` minor 8 respells five player-facing strings — two `CANCELLED` and three
`unlabelled`. Two are on the cancel path and three on the unlabelled path, so **no single capture shows
all five**. Run two per addon, in the four that wire `Perf`: AbsorbTracker, ConsumableMaster, KickCD,
MultiMeters.

1. `/<slash> perf start mylabel`, then `finish`.
2. `/<slash> perf start` with no label, then `cancel`.

**Pass** — the started line and the report header both name the label in run 1; in run 2 the start
line, the report header and the cancel line read **`unlabeled`** and **`perf run CANCELED`**.
**Fail** — a double-L in either. That is a copy of the string that did not come from the vendored
payload.

`AbsorbTracker` § P step 106 · `ConsumableMaster` § Perf harness step 7 · `KickCD` § 28 · `MultiMeters` § 29

### 3.4 · Three perf panels, one close button each — `M4-16`

The `decorate` hook and the library's own else arm are **exclusive**. For as long as the descriptor
carried `decorate`, `libs/LibKa0s/PerfPanel.lua`'s arm never executed once, in any client, ever.
Deleting the field runs it for the first time.

1. `/at perf`, `/kcd perf`, `/mm perf`.
2. Put each panel and that addon's debug console on screen together and compare the two close controls.

**Pass** — **exactly one** close control per panel, in the top-right corner at the same inset it has
always been at, drawn as this collection's own `close` mark — indistinguishable from the console's,
because they come from one factory. Clicking it hides the panel and nothing else: the run is not
cancelled, and `/<slash> perf report` afterwards still has the capture.
**Fail** — a multiplication sign `×` (the addon **folder** name is not reaching `MakeCloseButton`, so
the library cannot build the path and falls back), an empty corner (the arm did not run), two controls
stacked in the same corner (a `decorate` hook came back), or a control that has moved off the corner.
A texture path that is never built draws nothing and raises nothing, which is how one of these panels
wore a `×` through a green suite once already.

`AbsorbTracker` § S step 109 · `KickCD` § 30 · `MultiMeters` § 30

### 3.5 · PanelMaster's page acts moved into the chrome band — `M4-15`

Copy, Enabled, Unlock, Reset and Delete came out of a sixth **General** tab and into the `H.PageHeader`
band; the emptied tab is gone.

1. `/pm` → **Panels**. Walk **every one of the five tabs** and confirm all six band controls
   (**Panel name**, **Copy settings from panel**, **Enabled**, **Unlock**, **Reset**, **Delete**) are
   present and enabled on each.
2. From a tab that is **not** the first: tick and untick **Enabled**, tick **Unlock**, press **Reset**,
   then **Delete** — on a throwaway panel.
3. Select a panel, click into **Panel name**, type a few characters **without pressing Enter**, and run
   `/pm new Interloper` from chat.
4. With nothing typed, run `/pm rename <selected panel> Renamed`.

**Pass** — every act operates on the panel the **Panel** picker is showing, not on whichever was
selected when the page was first opened; the frame name lives on the Panel name box's tooltip, not as
a label of its own; step 3 leaves your uncommitted text in the box; step 4 makes the box follow to the
new name.
**Fail** — a control that vanishes when you change tab (the move was not made); an act on a stale
panel; a gap in the tab strip where General was; a rename box that snapped back to the stored name in
step 3 (the guard is missing).

`PanelMaster/docs/smoke-tests.md` § 5c and § 5c-2

### 3.6 · LootHistory's tick and ⓘ are catalog marks now — `M4-23`

Three Blizzard textures (`ReadyCheck-Ready`, `ReadyCheck-NotReady`, `FriendsFrame\InformationIcon`)
now resolve through `NS.Icon` against `circle-check`, `ban` and `info`. Two things changed on purpose:
the off mark is a **ban** (a slash through a circle), not an X — the catalog has no X — and the ⓘ is
white-on-transparent rather than Blizzard's blue, dimmed to 0.55 by vertex colour.

1. `/lh config` → **AH Price**.
2. Read the leading mark on every row, and the ⓘ trailing each Price Module text.
3. Untick a collecting row's **On** box.

**Pass** — green on every *Collecting data* row, red on every other, an ⓘ on every row (bright on a
collecting row, dimmed otherwise) whose hover still shows that key's label and description, and a mark
that flips green → red in place when the box changes.
**Fail** — a white or missing mark (wrong catalog name, or the tint was dropped), a vanished ⓘ
(`NS.Icon("info")` answering nil with no fallback reached), or a mark that disagrees with the row's
Status text.

**Its pair, while you are here:** MultiMeters' `ENABLED_TEX` / `DISABLED_TEX` in the Columns page's
blocks moved in the same item. **They move together or neither moves** — the comment cites
ConsumableMaster parity. Open `/mm config` → **Columns** and confirm the blocks look the same as
ConsumableMaster's.

`LootHistory/docs/smoke-tests.md` § 17l; `MultiMeters/docs/smoke-tests.md` § 5 for the column blocks

### 3.7 · KickCD's castbar dump with no LibKa0s — `M4-20`

`modules/Castbar_Debug.lua` lost `local emit = NS.Util and NS.Util.print or _G.print` in favour of
`local emit = NS.Util.print`. The deleted arm was unreachable, but the guard and the fallback went
together, and what used to degrade into an untagged global `print` now raises. That is the intended
trade — an untagged dump pasted into a bug report is worse than a visible error — and it is the only
behaviour this deletion can change. Nothing headless runs the dump on a library-less load.

**Setup:** rename `Interface/AddOns/KickCD/libs/LibKa0s` to `libs/LibKa0s_off`, `/reload`. Run § 25's
degraded-install and `L`-trap checks in the same visit.

1. Target anything and run `/kcd debug castbar`.
2. Rename the folder back and `/reload` **before you finish**.

**Pass** — the dump prints, every line carries the `[KCD]` tag, and the one-off missing-library notice
appears **once** before the dump rather than once per line.
**Fail** — a Lua error naming `Castbar_Debug.lua` and a nil `emit`, which would mean `Util.print` is
not on the namespace by the time a slash command runs on the degraded path — something no headless load
reproduces. A run of untagged lines means something else is doing the printing.

`KickCD/docs/smoke-tests.md` § 31, with § 25 for the setup

### 3.8 · Two cast bars, one cached handler each — `M4-22`

`Castbar:Start` no longer mints `function() onUpdate(inst) end` on every cast start; `EnsureFrame`
builds `inst.onUpdateScript` once per unit. The risk is not a handler that was never installed — § 7a
would catch that — but one installed and bound to the **wrong instance**, which only two live casts can
show.

**Setup:** `/kcd set units.target.castbar.enabled true` and the same for `units.focus.castbar`;
`/kcd lock`; `/kcd set units.target.visibility always`. Find a pull with two casting mobs.

1. Target one caster, focus the other, both mid-cast, and watch both bars at once.
2. Let each finish and start a second cast without retargeting.
3. Swap target and focus and repeat.

**Pass** — both bars animate simultaneously and independently; the second cast on a unit animates like
the first; spell name and remaining time track on both and neither shows the other's spell.
**Fail** — one bar frozen while the other runs, or both showing the same fill (a shared or mis-bound
handler, exactly what a single file-scope handler would produce); a bar that fills on the first cast of
a session and is static afterwards (torn down and not re-installed); a Lua error naming `Castbar.lua`
and a nil `onUpdateScript`.

`KickCD/docs/smoke-tests.md` § 32

### 3.9 · Four one-line looks, folded in here because you are already in the panels

- **PanelMaster's `[Init]` line reports the packaged version** (`M4-19`). In the **installed** copy
  under `Interface/AddOns/PanelMaster/`, never the repo, set `## Version:` to `1.0.0-smoke`. Log in,
  `/pm debug on`, read the `[Init]` line, then `/pm version`. **Pass** — both read `1.0.0-smoke`.
  **Fail** — an `[Init]` line reading `v1.0.0` while `/pm version` reads `v1.0.0-smoke`: one string with
  two sources of truth, and the `[Init]` line is the one a user pastes into a bug report. Restore the
  TOC and `/reload`. (`PanelMaster` § 21)
- **PanelMaster's byte-scale alpha** (`M4-18`). `/pm panel <name> bgColor 255,0,0,0.5` → the identical
  translucent red as `1,0,0,0.5`, echoing `1.00,0.00,0.00,0.50`. Then `/pm panel <name> bgColor 255,0,0,1`
  → **the same red, fully opaque**, echoing `1.00,0.00,0.00,1.00`. **Fail** — a panel that vanishes off
  screen with nothing in chat or the error frame: the byte scale chosen from RGB was applied to alpha,
  so a 1 there meant 1/255. `255,0,0,128` must still scale to `0.50`. (`PanelMaster` § 5b step 1a)
- **PanelMaster's preview after a wipe** (`M4-18`). `/pm preview on`, then **without turning it off**
  `/pm panel deleteall` → Yes. `/pm preview on` again → **the three placeholders come back**, and the
  screen stays unlocked across the wipe. **Fail** — a silent no-op. Finish with `/pm preview off`.
  (`PanelMaster` § 17 step 4a)
- **KickCD's icon-grid reset lands on the shipped default** (`M4-18`). `/kcd resetposition` → the target
  icon grid snaps to `CENTER / CENTER, x = 0, y = +120` — **above** screen centre. **Fail** — anywhere
  else, and `y = -180` specifically, which is the hand-written second copy the item removed. A check
  that only asks whether the grid moved cannot tell the two apart. (`KickCD` § 12 Resets, the slash table)
- **No `colour`, `behaviour` or `grey` on screen** (`M4-13`). While `/cm`, `/kcd config` and `/wg` are
  open anyway, read the labels, tooltips and chat lines. **Fail** — any of the three spellings in a
  string a player reads. And in `/kcd config` → **Cast bar**, every row shows a **sentence, not a bare
  key** — the three description keys `M4-21` added to `locales/enUS.lua`. A `SCREAMING_SNAKE_CASE`
  string on screen is the `L` trap, and it fails for every key in that module at once, so one sighting
  means dozens. (`KickCD` § 25, the `L`-trap half)

---

# 4 · Session 5 — the shared widget registry

**Needs:** KickCD, PanelMaster, AbsorbTracker, ConsumableMaster and MultiMeters loaded **together**,
and a way to change which one loads last. **~15 minutes.**

**Why fourth, and why it is shorter than the plan said.** AceGUI's `WidgetRegistry` is process-global:
one slot named `LSM30_Border`, shared by every addon in the client, Ka0s or not. Five Ka0s addons each
carried a private copy of the wrapper — KickCD 68 lines, PanelMaster 66, ConsumableMaster 65,
AbsorbTracker 50, MultiMeters 101, **all five different** — each registering at whatever version it
found plus one, so the wrapper a Border dropdown actually got belonged to whichever addon loaded last.
No headless suite in any of the five repos can see the interaction at all.

`06_SMOKE_TESTS.md` budgeted twenty minutes spread over six runs, one after each deletion. **All five
deletions have landed.** There is one run left — the one with none of the private copies present — plus
the load-order re-check. That is the whole session.

### 4.1 · Every Border dropdown is the same control, whatever loaded last — `M4-02`, `M4-04`…`M4-08` — **NEW, no prior coverage**

1. Enable all five together and log in.
2. Open each addon's Border dropdown in turn:
   - `/kcd config` → **Cast bar** → **Border style**
   - `/pm` → **Panels** → select a panel → **Border style**
   - `/at config` → **Appearance** → *Border* → **Border style**
   - `/cm config` → **Macro Bar** → **Bar border style** and **Button border style**
   - `/mm` → **Frame** → **Border style** and **Tooltip** → **Bar border style**
3. Screenshot each open dropdown.
4. Change the load order — disable and re-enable addons, or rename a folder so a different one is
   reached last — `/reload`, and walk them all again.

**Pass** — in all five, the closed control's left edge is **flush** with the sliders and checkboxes
stacked with it, with **no ~42px gap**, and opening it still draws the per-row hover previews. Nothing
differs between the two passes. Out of game, `grep -rn 'RegisterWidgetType' | grep LSM30` finds nothing
outside `libs/` in any of the nine repositories.
**Fail** — any dropdown that looks different from the other four, or that changes when the load order
changes. The whole point of moving the registration into LibKa0s is that the answer no longer depends
on who loaded last.

> **What this run cannot tell you, and it is worth knowing before you start.** `M4-03` asked for the
> same sweep with all five private copies still in place — the "before" reading. It was never run, and
> it can no longer be taken without reverting five commits. So a failure here does not distinguish
> "the promotion is wrong" from "it was always like this". If it fails, the five deletion commits are
> what turn *one of them is wrong* into *this one is wrong*: bisect on `M4-04`…`M4-08` in that order,
> with AbsorbTracker last because its copy is the one that diverged — a callable
> `NS.ApplyLSMBorderPatch()` from `OnEnable` rather than a `PLAYER_LOGIN` frame, so its deletion is the
> one most likely to have changed load-time behaviour.

`KickCD` § 29 · `PanelMaster` § 20 · `ConsumableMaster` § 19 · `MultiMeters` § 29 (Border) ·
`AbsorbTracker` § Q step 107

### 4.2 · The cross-addon sweep, while all of them are up — `M1-WA-01`

Nothing has ever asked this. The four collision classes were measured by hand for
`01_CONSOLIDATED_FINDINGS.md` § *Verified-clean negatives* and were clean then; nothing repeats the
measurement, and this is the one login where they are all loaded anyway.

1. Type each slash root and confirm it reaches its own addon: `/at`, `/bl`, `/cm`, `/kcd`, `/lh`,
   `/mm`, `/pm`, `/pc`, `/wg`.
2. Open **Settings → AddOns**: each addon appears **once**, and each multi-page addon's pages appear
   once each.

**Pass** — nine distinct roots, nine single entries.
**Fail** — a root that lands in the wrong addon, or a duplicated category.

`06_SMOKE_TESTS.md` § 5.3; the per-addon halves are `KickCD` § 14's last bullet and each addon's own
panel section.

---

# 5 · Session 2 — SavedVariables

**Needs:** a **backed-up copy of `WTF/`**. A text editor. A second AceDB profile. **~25 minutes.**

> **Back up `WTF/` before you start, and work on the copy.** This is the only session in the cycle that
> can lose settings, and both migrations under test are runners that a wrong fix would run against a
> real ledger.

**Why fifth.** Both defects are migrations that have **never once run against a real store** — one
because `schemaVersion` shipped as an AceDB default and was re-supplied at every login as the runner's
own target, the other because the stamp was account-wide while the work was profile-scoped. Neither is
breaking anything for a player today; what they are is the next schema bump already disarmed. Worth
proving, worth proving carefully, not worth doing before the four sessions above.

### 5.1 · BankLedger's v1 → v2 ladder runs, and the stamp survives a logout — `M2-05`

The headless suite now pins the seeding, the discriminator and the `[Migrate]` line. Only the client
can prove that a stamp the runner wrote **survives a logout**, which is the exact thing the defaults
declaration broke.

1. Copy `WTF/Account/<ACCOUNT>/SavedVariables/BankLedger.lua` somewhere safe.
2. Hand-edit it: delete the `["schemaVersion"] = 2,` line under `["global"]`, and add
   `["vendorPrice"] = 20,` to exactly one existing ledger entry. **Note which entry.**
3. Log in, `/bl debug` on, open the console.
4. Log out **fully** — exit to desktop; the strip runs on `PLAYER_LOGOUT`. Reopen the file.
5. Log back in once more.

**Pass** — step 3's console carries `[Migrate] v1 -> v2, 1 rows touched`; step 4's file carries
`["schemaVersion"] = 2,` under `["global"]` with the `vendorPrice` key gone from the entry you edited;
step 5 shows **no** migration line, because the runner is idempotent.
**Fail** — no migration line at all, which is the defect this step exists to catch; a row count that is
not the one you planted; or a stamp missing again at step 4, which would mean something reinstated it
as a default and the next schema bump is already disarmed.

`BankLedger/docs/smoke-tests.md` § S-25

### 5.2 · ConsumableMaster migrates a second profile — `M2-07`

The headless suite pins the gate against a fake. What only a live client proves is that the real AceDB
fires `OnProfileChanged` on a profile the SavedVariables file has been holding un-opened, which is the
shape the whole gate exists for.

1. `/cm debug on`.
2. On a character whose settings you already have, Options → Profiles, create a **new** profile and
   switch to it.
3. Switch back to the original.
4. Log out. Reopen the copy.
5. Set the new profile's macro bar **off**, switch away, switch back.

**Pass** — step 2 prints `[DB] migrated profile '<name>' schema v1 -> v3`; step 3 reports nothing and
loses nothing — settings, macro-bar position and geometry exactly as you left them; step 4's file gives
every profile you visited its own `schemaVersion = 3` with `global.schemaVersion` still 3; step 5's bar
**stays** off.
**Fail** — **silence at step 2**, which is what happened before the profile-scoped stamp. A bar that
re-enables itself on *every* switch at step 5 is the profile stamp not being written. **The one-time
cost is not a bug:** no profile in a file written before this build carries a stamp, so each meets the
v2 step once on its first arrival and a deliberately-disabled bar comes back on exactly once.

`ConsumableMaster/docs/smoke-tests.md` § 13, with § 1a for the single-profile upgrade path

### 5.3 · AbsorbTracker's `migrateAllProfiles` walks the real store — `M4-20`

`M4-20` reduced `core/Database.lua`'s `migrateAllProfiles` to `forEachProfile(NS.MigrateProfileToV3)`.
Behaviour-identical by inspection; what headless cannot reach is the store the walk walks. Under a mock
AceDB the identity test the skip depends on is the mock's; in a client, `NS.db.profile` is a
metatable-backed view whose identity against the entries in `NS.db.sv.profiles` is what the skip
compares. **The count is the tell**, which is why this step reads the console rather than the bar.

> AbsorbTracker's own document files this under session 5, and says plainly that it lands there because
> that was the repository's outstanding client run rather than because it has anything to do with the
> Border patch. It wants a hand-edited SavedVariables file, so it belongs here.

1. Log out. In `WTF/Account/<acct>/SavedVariables/AbsorbTracker.lua`, add a second profile block
   carrying a flat `["barWidth"] = 333,` and `["schemaVersion"] = 1,` and **no `units` table** — a
   hand-made pre-v3 profile is the only thing that makes the lift do work.
2. Log in with a **different** profile active. `/at debug on`, `/reload`, read the console.
3. `/at profile use <the hand-made profile>`, then `/at get units.player.barWidth`.

**Pass** — `[Migrate] lifted N profile(s) to v3` with **N counting the hand-made profile**, followed by
the `vX → vY` ladder in the same order as before; step 3 answers **333**.
**Fail** — a missing `lifted` line; an N that does not count the inactive profile (the store lookup
returned nothing and only the active profile migrated); or a width of 200.

`AbsorbTracker/docs/smoke-tests.md` § R step 108

### 5.4 · ConsumableMaster's colour codec, and the absent channel — `M4-18`

`settings/OptionsSetup.lua` and `settings/Slash.lua` each carried a hand-written decoder for the stored
positional `{ r, g, b, a }` and disagreed about a channel the table does not carry — `or 1` in the panel
against `or 0` in the CLI, so one stored value read **white** on the swatch and **black** from `/cm get`.
The headless suite pins the decoders against each other and cannot see the picker; the raise this rules
out happens inside Blizzard's texture API.

> Filed opportunistic in its own document — do not book a login for it — but step 4 wants a hand-edited
> SavedVariables file, so it is cheapest here.

1. `/cm config` → **Macro Bar** → **Bar backdrop color**. Pick a colour with an obviously non-default
   alpha and confirm.
2. `/cm get macroBar.barBackdropColor`, reopen the picker, `/reload`, repeat both.
3. Repeat for **Bar border color**, **Button backdrop color**, **Button border color** and the label's
   **font color**.
4. Log out. In the SavedVariables file, find `barBackdropColor` and **delete its third and fourth
   entries**, leaving two. Log back in and open `/cm config` → **Macro Bar**.
5. Restore the file, or re-pick the colour in the panel, before running anything else.

**Pass** — the bar repaints as you drag and keeps the colour on confirm; `/cm get` prints four channels
matching the swatch, across the reload, on all five surfaces; at step 4 the page draws, the swatch
draws, **no Lua error**, and `/cm get` prints the four channels the swatch is showing.
**Fail** — two different answers to one stored value. A codec fault is per-surface, not per-addon, so
five swatches means five round trips.

`ConsumableMaster/docs/smoke-tests.md` § 20

### 5.5 · Nothing else moved

With both migrations landed, log in on each of the nine in turn and confirm settings, positions,
profile selection and window geometry are exactly as you left them. Cheap, and it is the check that
catches a migration that ran when it should not have.

`06_SMOKE_TESTS.md` § 2.3

---

# 6 · Session 6 — the non-English client

**Needs:** a **deDE or frFR** client — a language pack on PTR/beta, or a non-English account. A warbound
drop and a warbound-until-equipped drop. An auction-house purchase. Herbs, ore and something
disenchantable. A teleport spell you have learned and one you have not. **~45 minutes.**

**Why sixth, and not last.** It is here rather than earlier because of the setup, not because of the
value — three of these steps are the likeliest failures in the whole document. It carries the cycle's
one **gating** observation, and it is the session for which the headless gate is structurally blind
everywhere: `tests/wow_mock.lua` answers enUS for every global it defines, so a path that keys off a
localized string is green whether it is right or wrong. **The test and the bug agree with each other.**

Only three of the nine addons carried a non-English step before this cycle. `M5-08` wrote sections into
six more. The two addons whose code is *most* locale-sensitive had none.

**English output is not a failure here.** Every label, tooltip and chat line these addons print is a
hardcoded English literal and stays English on a German client. That is scope, not regression, and it
is not what these steps are looking for.

### 6.1 · WhatGroup § 7a — the `C_SpellBook.IsSpellKnown` reading — **gating**

**Run this first; it is why the session is scheduled.** `core/Compat.lua:62-67` calls the bare
`IsSpellKnown` global and returns false when it is absent, while its five siblings all try `C_Spell.*`
first. `WHATGROUP-R-06`'s own fix text conditions the modern rung on an in-client check confirming both
APIs present and agreeing.

1. `/dump C_SpellBook.IsSpellKnown(<a teleport you have learned>)` and
   `/dump IsSpellKnown(<the same spell>)`.
2. Both again for a teleport you have **not** learned.
3. Record all six, in issue #15 and in the session result:

```
client build (/dump GetBuildInfo()):
client locale (/dump GetLocale()):
learned spellID:     C_SpellBook.IsSpellKnown = ___   IsSpellKnown = ___
unlearned spellID:   C_SpellBook.IsSpellKnown = ___   IsSpellKnown = ___
did C_SpellBook.IsSpellKnown exist at all? (yes / no, it errored)
```

**Pass** — both APIs resolve and agree on both spells. `M5-10` can then add the rung in the shape the
five siblings use.
**Fail** — either call errors, or the two disagree. **Do not add the rung.** A disagreement means the
two are not interchangeable and the shim needs a decision rather than a fallback ladder; record what
you saw on issue #15 and leave `core/Compat.lua:62-67` exactly as written.

Both outcomes close the obligation — one ships a rung, the other files a finding. **A blank is the only
result that does not**, and it is the state the finding has been in for five milestones.

`WhatGroup/docs/smoke-tests.md` § 12b step 5, running § 7a

### 6.2 · LootHistory's tooltip fallback and the deconstruct names

`core/Compat.lua` defines four English wordings as the fallback for when the client leaves the
`ITEM_ACCOUNTBOUND*` globals nil, and the same file calls the tooltip "the ONLY witness" for items
whose bind type lies. The comment above the literals says they are safe "because this addon is
English-only" — but the tooltip is not something the addon prints; it is text the **client** wrote.

1. **Before looting anything**, `/dump` each of the six: `ITEM_BIND_TO_ACCOUNT_UNTIL_EQUIP`,
   `ITEM_ACCOUNTBOUND_UNTIL_EQUIP`, `ITEM_BIND_TO_BNETACCOUNT`, `ITEM_BIND_TO_ACCOUNT`,
   `ITEM_BNETACCOUNTBOUND`, `ITEM_ACCOUNTBOUND`. **Record all six verbatim.** Which are nil *is* the
   finding, either way — the literal fallback is only ever reached for a global the client leaves nil.
2. Acquire a warbound item and a warbound-until-equipped item. `/lh` → History, read **Bind** on both.
3. Buy something on the auction house, take it from the mailbox, read the row's **Source**.
4. Disenchant something, mill a stack of herbs, prospect a stack of ore — plain and **mass** variants.
   Read **Source** on all of them, and `/dump C_Spell.GetSpellName(434926)` and
   `/dump C_Spell.GetSpellName(225904)`.

**Pass** — the two bind types classify distinctly; the AH row is attributed to the auction house; all
deconstruct rows, plain and mass alike, carry their source.
**Fail** — the until-equipped item classified as plain warbound (both wordings contain the shorter one,
so a missed qualifier silently demotes every until-equipped drop); an empty Bind cell where the enUS
client fills it; an AH row attributed to mail-from-a-player; **a mass mill or mass prospect row with no
source while the plain cast on the same client is right** — that is the one most likely to fail, because
`modules/Attribution.lua` builds its match token from the seed spell's localized name and strips its
final word, and German and French do not build that name the way English does.

`LootHistory/docs/smoke-tests.md` § 18a–18d

### 6.3 · PrettyChat's whole function

The addon's entire job is overwriting **localized** `_G` chat format strings, and its 797-line document
had no locale step at all. `tests/test_defaults.lua` checks every override against Blizzard's real
signature — but the signatures come from `GlobalStrings/`, an **enUS** dump. A locale whose string
carries fewer conversions, or orders them positionally, is checked against nothing.

1. `/pc test formatstring LOOT_ITEM_SELF` and read the `Original:` line.
2. `/pc set General.enabled false`; loot something, gain reputation, take repair gold. Then
   `/pc set General.enabled true` and trigger the same three again.
3. With every category enabled, trigger one line from each of the eight — loot, currency, money,
   reputation, XP (grouped, so guardian and exhaustion fire), honor, a craft, a quest XP reward — with
   the chat frame and the error frame both in view.
4. `/pc test` (the full report) and scan the `Original:` lines for empties.
5. **Record the `Original:` line verbatim** for one global from each category: `LOOT_ITEM_SELF`,
   `CURRENCY_GAINED`, `LOOT_MONEY`, `FACTION_STANDING_INCREASED_GUARDIAN`,
   `COMBATLOG_XPGAIN_FIRSTPERSON`, `COMBATLOG_HONORGAIN`, `CREATED_ITEM`, `ERR_QUEST_REWARD_EXP_I`.
   Their real signatures on this locale exist nowhere in the repository.

**Pass** — the `Original:` line renders the client's own sentence; the master toggle off gives the
client's untouched text and on gives PrettyChat's layout; eight rendered lines and no Lua error; every
registered global has a non-empty `Original:`.
**Fail** — an English `Original:` on a German client (the snapshot is reading something other than
`_G`, and every restore is handing players text their client never wrote); a
`bad argument #N to 'format'` raise; a literal `%s`, `%d` or `%1$s` left in a rendered line; an empty
`Original:`, which is an override doing nothing at all on this locale, silently, while the panel shows
it enabled — **that list is the finding**. `FACTION_STANDING_INCREASED_GUARDIAN` is the global whose
argument list already raised once, for every user, on a routine reputation gain.

`PrettyChat/docs/smoke-tests.md` § N, T-104 to T-107

### 6.4 · BankLedger's persisted display strings, its CSV, and non-ASCII sorting

Four seams, and one of them writes localized strings into SavedVariables as analytics **keys**.

1. Deposit two items of different classes. **Insights** → read **Movements By Item Type** and the
   sub-type facets. If this account has rows captured on an English client, look for **both spellings
   in the same facet list**.
2. History ▸ **Export** ▸ Current View ▸ **Export to CSV**. Read the header row, then **write down**
   the `date` cell's month token and the `itemType` / `itemSubType` pair.
3. With rows whose names begin with an accented letter, sort by **Item** both ways, then search for the
   name in lower case with the accent (`änderung`, `épée`).
4. Walk S-1, S-2 and S-8 once.

**Pass** — facets in the client's own words with correct counts and a correct type × sub-type pivot; a
CSV header **byte-identical** to the enUS one, all ASCII, with `quality` localized beside a numeric
`qualityRaw` and direction/store/kind still the English constants; accented names sorting in with their
neighbours and search finding the row whichever case you type; no Lua error anywhere.
**Fail** — one category with an English label and a German one in the same facet list (the
persisted-display-string defect, and what step 1 is really for — **a finding to file, not a step to
re-run**); a translated header key; every accented name clumped at one end of the sort, or a search
that finds nothing until you match the capital exactly. **Step 3 is the step most likely to fail** —
`string.lower` folds ASCII and nothing else, so `Ä` is not `ä` to any of the five call sites.

`BankLedger/docs/smoke-tests.md` § S-27

### 6.5 · PanelMaster's slug, which is a public contract

`Util.Slugify` collapses every run of `[^%w]+` to one underscore, and Lua's `%w` is ASCII-only.
`Übersicht` slugs to `bersicht`; `Ärger` and `Örger` both slug to `rger`. That slug is
`PanelMaster_Panel_<slug>`, which other addons anchor to.

1. `/pm new Übersicht` (or `Écran`). Hover the band's **Panel name** box to read the reported frame
   name, then `/run print(PanelMaster_Panel_<the reported slug>:GetWidth())`. **Write down the slug.**
2. `/pm new Ärger`, then `/pm new Örger`.
3. `/pm panel übersicht` in lower case.
4. With three or four accented and unaccented names, open the Panels page and read the sort order.
5. `/reload` and check all of it again, then switch profiles and back.

**Pass** — the name renders correctly in the band, the Panels list and `/pm panels`; the reported frame
name resolves to a real frame; two panels from step 2 with two distinct frame names; step 3 resolves the
way `/pm panel chat bg` resolves `Chat BG` on English; names and anchors identical across the reload.
**Fail** — a name that renders as `?` or mojibake; a reported frame name that does not resolve; a step 2
refusal naming a frame name (`PanelMaster_Panel_rger`) that looks like neither name typed — **record
which happened; a refusal is a finding to file, not a step to re-run**; "no panel called übersicht" while
the ASCII half of the same name matches; a name that changed shape across the reload.

`PanelMaster/docs/smoke-tests.md` § 22

### 6.6 · AbsorbTracker's two seams

`AbbreviateNumbers` and `UnitClass` are the whole list. Blizzard localizes both the suffix and the
grouping, and `bgClassColors` is keyed on `UnitClass`'s **third** return — the English token — which is
supposed to make class colour locale-independent by construction. That is the claim this checks rather
than assumes.

1. With the player bar visible, take an absorb worth a few hundred, then one over a million (a stacked
   shield, or `/at test 1500000`).
2. Tick **Use class color** for bar, background, border and text; target a player of a different class
   and enable the target bar.
3. `/at debug on`, open the console, gain and lose an absorb out of combat and once in combat.

**Pass** — the number renders in the client's own convention and stays **inside the bar** at the default
width at every magnitude; the player bar wears the player's class colour and the target bar the
target's, with the background as the dimmed variant; `shield up:` / `shield gone:` and the
`[Combat] left: N events, M repaints` rollup all render with no error.
**Fail** — a raw unabbreviated integer where enUS abbreviates, or a string overflowing or clipped by the
bar's right edge (**expect this one**: a locale whose abbreviation is longer than `M` has more glyphs to
fit in a width chosen against English); any of the four colours falling back to the stored colour, or
every bar drawing the same colour, which is `UnitClass`'s localized **first** return reaching
`bgClassColors` — invisible on an English client because there the two strings differ only in case. The
combat pass is the one that matters: it is the only step that puts a secret and a localized formatter in
the same line.

`AbsorbTracker/docs/smoke-tests.md` § T steps 110–112

### 6.7 · The three that already had a step, and the addon-level sweeps

- **ConsumableMaster § 3c.** `/cm dump item <id>` shows a **localized** `subType` while `classified:`
  stays correct and the `KCM_*` macros populate. Before the classifier keyed on numeric subclass, every
  consumable classified as `(none)` and the macros sat empty on this client.
- **KickCD § 9b (issue #8).** The spell grid seeds and resolves on frFR. An Elemental Shaman
  reproduces the original report exactly.
- **MultiMeters' CSV header.** Run one export and diff the header against the enUS one recorded in
  `MultiMeters/docs/smoke-tests.md` § *Export*: **26 columns, `snake_case`, byte-identical.** A German
  client must produce a file a colleague on an English client can open with the same formulas.
- **WhatGroup § 12b steps 1–4 and 6.** A real application through the LFG UI — not `/wg test`, whose
  fixture spells the activity name out in English and is *expected* to show English here. **Pass** —
  Instance shows the client's own activity name, Type and Playstyle read as words, the longer German
  name fits its row or truncates cleanly, `/dump GROUP_FINDER_GENERAL_PLAYSTYLE1` through `4` give four
  non-empty strings, and the teleport button's tooltip is the German one and the click casts. **Fail** —
  `Unknown` in the Instance row; text overrunning the popup border; any of the four playstyle globals
  nil (`Labels.PLAYSTYLE` is built once at file load, so a nil there is nil for the session — **record
  which ones**); a teleport click that does nothing while the button draws as ready, which would mean
  the macrotext holds a name this client does not answer to.
- **Nothing else moved**, in each of the six: walk that addon's boot, capture and table sections once.
  Any Lua error here means a localized string reached something that assumed an English one.

---

# 7 · The closing login

**Needs:** everything loaded. **~15 minutes.**

Not a session in `06_SMOKE_TESTS.md` — it is the one thing that document says is worth doing at the end
of M5. It is last because its only outcome is "nothing changed", and it is worth doing because it is
the only pass that sees M2 through M4 together in one client.

1. Load all nine.
2. Open every settings page once, in every addon.
3. `/reload`.
4. Open them again.

**Pass** — no error at any point, every panel as you last saw it, every profile and position intact.
**Fail** — anything at all, which at this point means an interaction between two items that individually
passed.

`06_SMOKE_TESTS.md` § M5

---

# If a step fails

Record the **addon**, the **step**, the **exact chat text**, and the client build
(`/dump GetBuildInfo()`). Then stop and write it down — **do not fix it in the session.**

The four out-of-game suites are green in all ten repositories at the figures
`07_EXECUTION_RECORD.md` measured, and every work item carries its own headless verification. So a
failure here is not a small thing to patch over between two smoke steps: it is a defect no automated
check in the collection can see, which makes it a finding for the next cycle with a test owed to it.
Hot-fixing it mid-session costs the one thing this whole document was expensive to obtain — a clean
reading — and the fix will not have a red case standing behind it.

Where to look first:

- **A rendering or lifecycle regression from the options work** — run orders 1, 2 and 3, most likely in
  AbsorbTracker, KickCD, MultiMeters or PrettyChat. `git log --oneline` in the addon's repository,
  matched on the item id in the commit subject, isolates it to one commit.
- **The `__AttachCompose` contract change** — step 2.2 specifically. If MultiMeters' `M3-02` revert was
  missed, the symptom is a media list complete except for late registrations, and nothing else in the
  collection will tell you.
- **The registry sentinel** — run order 4. Bisect on `M4-04`…`M4-08` in that order; that is what five
  separate deletion commits were bought for. Note the caveat in 4.1: with `M4-03` unrun there is no
  "before" reading to compare against.
- **A migration** — run order 5, and this is why that session works on a copy. Restore the backup
  before doing anything else.
- **A locale seam** — run order 6. Every one of these is a finding to file rather than a step to re-run,
  and several of them (LootHistory 18a, BankLedger's split facet list, PanelMaster's slug) are
  *questions* whose answer is the deliverable. A recorded answer closes the step whichever way it went.

Two of these carry a decision rather than a bug report. **WhatGroup 6.1** ships the rung on agreement
and files a finding on disagreement — both outcomes close `WHATGROUP-R-06`, and `M5-10`'s recorded wait
ends either way. **WhatGroup 1.4** is the only witness the collection has to the error the owner
reported; a clean pass there is the evidence `M2-28` currently lacks.

---

# What is not in this document

- **The four out-of-game suites.** `luacheck`, the headless harness, `tests/perf.lua` and `lizard` are
  green in all ten repositories; `07_EXECUTION_RECORD.md` carries the figures. None of it is repeated
  here.
- **`M5-06`.** The fresh audit round is still outstanding and is not a client task — it is blocked on
  WowAddonStandards merging, because `standards-audit` resolves every rule through a raw GitHub URL that
  still serves v2.38.0.
- **Anything M1 changed on its own.** LibKa0s has no TOC a client loads, and WowAddonStandards and
  `wow-addon` are documentation. The three M1 items that change bytes a player sees are checked at the
  commit that vendors them, and they are above: `M1-LK-02` in step 2.1, `M1-LK-03` in step 3.2,
  `M1-LK-11` in step 3.3.
- **`M4-10`, `M4-11`, `M4-12`, `M4-14`, `M4-24`, `M4-25`, `M4-26`.** Line endings, lint config, TOC
  comments, cap dispositions, exemption evidence and the two complexity items. `M4-25` splits a KickCD
  **test** function and `M4-26` writes dispositions; neither changes a shipped byte.
- **A release.** Nothing here is a release gate and running all of it does not cut one. Decision 5
  deferred shipping deliberately, and `07_EXECUTION_RECORD.md` § *What to do next* puts that decision
  **after** these sessions rather than before them.
