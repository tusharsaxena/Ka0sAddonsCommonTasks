# Collection-wide frame layering model (item 030)

Item 030's design input. The model below is built from the 15 reviewed per-addon analyses in
`inputs/strata/*.md`, from the five standard sections named in the brief
(`events-frames-taint`, `standalone-windows`, `preview-mode`, `options-ui`, `anti-patterns`, all at standard
v2.87.0) and from the frame-creating modules of LibKa0s v1.76.0 (`Core`, `Widgets*`, `Launcher`, `SimPanel`,
`PerfPanel`, `OptionsDrawer`, `DebugLog*`, plus `Options`, `OptionsCombat`, `OptionsTabs`, `OptionsIds`).

Owner brief (030): "clear separation of strata and z-order across all visual elements of a single addon; needs
consistency within a single addon; do this for all addons individually; add this as upstream guidance in
WowAddonStandards, etc". The lead's call (`OWNER_SCOPE.md`): changes land in each addon, the guidance lands as a
standard rule, and a LibKa0s helper is added only if the addons need a shared surface.

Contents:

1. How WoW draws (the facts the rules rest on)
2. The tier model: element class to strata
3. The level bands: inside a display element, inside a HUD display, inside a window
4. The rules (XS-01 to XS-24)
5. Anti-patterns
6. Library- and third-party-owned tiers, and how LibKa0s's own frames measure up
7. LibKa0s recommendation
8. Draft WowAddonStandards text
9. dev-copilot
10. Per-addon check: overrides and adds
11. In-client verifications the model depends on

---

## 1. How WoW draws

These are the client facts the analyses relied on. Items marked *verify* were inferred from code, comments or
Blizzard defaults and need an `/fstack` or `/dump` check in game (section 11).

- **Order of comparison:** strata first (`BACKGROUND < LOW < MEDIUM < HIGH < DIALOG < FULLSCREEN <
  FULLSCREEN_DIALOG < TOOLTIP`), then frame level within a strata, then draw layer (`BACKGROUND < BORDER <
  ARTWORK < OVERLAY < HIGHLIGHT`) and sublevel for regions within one frame level.
- **A child frame draws over every region of its parent**, whatever the regions' draw layer. An `OVERLAY`
  texture on a button is under that button's `Cooldown` or `BackdropTemplate` child. This one fact is behind the
  most common defect in the collection (KIC-S01, MUL-S01, CON-S05, PAR-S02, QUI-S01, ABS-S02).
- **A child with no explicit level is at parent + 1**, so two children of one parent tie, and a tie between
  overlapping frames that both draw is broken by creation order, which pooling and lazy builds scramble.
- **A frame with no explicit strata inherits its parent's**, and a parent's `SetFrameStrata` carries every child
  that is not `SetFixedFrameStrata(true)` with it (AUR-S12).
- **`SetParent` re-derives the level** from the new parent, so an explicit level set before a reparent is lost
  (KIC-Z06).
- **A toplevel frame is raised on show and on click** within its strata. `Raise()` does the same once. Both move
  the frame's level; unfixed children are expected to move with it (*verify* for explicitly levelled children,
  MUL-Z02, ABS-Z05, PAR-S03).
- **The per-strata level cap is 10000** (`OptionsCombat.lua:157`, `MAX_FRAME_LEVEL`).
- **Strata, level and toplevel writes on a protected frame are refused in combat** (events-frames-taint-§2), and
  so are `Show`, `Hide`, `Raise` and `EnableMouse` on a frame that parents a secure child (WHA-S01).

## 2. The tier model: element class to strata

**Strata separates roles. Frame level orders within a role.** Elements of different roles (a HUD, its edit chrome,
a window, a modal, a popup, a tooltip) are separated by strata, because a level race against another addon's or
Blizzard's frame in the same strata is not winnable by construction. Elements within one role are ordered by named
level bands (section 3).

The strata column is the collection default. The **key** column is the name an addon's layers table uses for that
tier (XS-16), so that "the window tier" is spelled the same in every addon.

| tier | element class | strata | key | toplevel / clamped | collection examples |
|---|---|---|---|---|---|
| T0 | Non-visual frames: event frames, binding click targets, ESC proxies, measurers, hidden parents, secure follow headers that draw nothing | none set (exempt) | — | — | every addon's `Toggle…` binding button, WhatGroup ESC proxy, AuraMaster hidden BuffFrame parent |
| T1 | **HUD display**: a world-anchored, persistent display (bar, icon grid, cast bar, meter, pad, backdrop, attached unit elements) | **MEDIUM**, set explicitly on the display root; children inherit | `HUD` | not toplevel unless several can overlap (XS-19) / clamped | AbsorbTracker bars, KickCD grid and cast bar, ConsumableMaster macro bar, QuickComms pad, AuraMaster containers |
| T1p | **Player-chosen HUD strata**: a display whose strata is a setting | the player's pick from **BACKGROUND / LOW / MEDIUM / HIGH**; a knob shipped before this rule keeps its stored values (DIALOG included) and its tooltip says what DIALOG covers | `HUD` (the default) | as T1 | AuraMaster `layout.strata`, MultiMeters `window.frame.strata`, PFE `general.strata` |
| T1h | **Host-matched surface**: a surface grafted onto another addon's or Blizzard's frame (an attached panel; elements that decorate a party frame) | **the host's strata, read** (`host:GetFrameStrata()`) or simply inherited; never restated as a literal | — | as the host | PGFE panel under PGF's dialog (FULLSCREEN today), PFE fade frames matching the party frame |
| T1b | **Player-layered backdrop**: a frame whose strata *and* level are the player's composition | any strata the addon offers, as a documented deviation; the addon keeps its own popups answerable (XS-08) | — | not toplevel | PanelMaster panels |
| T2 | **Edit-mode chrome**: drag handles, unlock outlines, name labels while unlocked, test and sim markers that overlay a display, resize grips shown only while unlocked | the **display's strata**; mouse-enabled chrome floored at `max(display, MEDIUM)`; mouse-off chrome MAY float at `max(display, HIGH)` | `CHROME` | — | AuraMaster handle (L+50, floored MEDIUM), PanelMaster unlock overlay (mouse-off, lifted to HIGH), KickCD handles and sim strip |
| T2b | **Drag backplate**: a holder or plate a display is dragged *by*, sitting behind it | the display's strata, at the display root's level, under every element | — | clamped | PFE free-placement holders |
| T3 | **HUD popup**: a transient surface opened from a HUD element (an action-button flyout) | **one strata above the HUD root**, set once at construction; where Blizzard has an equivalent, its strata (`SpellFlyout`) | `HUD_POPUP` | clamped like its root | ConsumableMaster flyout |
| T4 | **Window, persistent**: a movable display window the player keeps up while playing | **MEDIUM** | `WINDOW` (or `HUD` where it is the addon's only display) | **toplevel** / clamped | DpsRace HUD, DropWatcher main window, MultiMeters windows |
| T4 | **Window, on demand**: a browser the player opens to read, then closes | **HIGH** (the Settings panel's tier; both toplevel, so the last clicked wins) | `WINDOW` | **toplevel** / clamped | LootHistory and BankLedger browsers, BankLedger session window, DpsRace Results |
| T5 | **Alert**: an interactive toast | **HIGH** | `ALERT` | not toplevel / clamped | DropWatcher toast |
| T5s | **Screen alert**: a non-interactive centre-screen notice | **FULLSCREEN**, mouse-disabled | `SCREEN_ALERT` | — | DpsRace countdown |
| T6 | **Modal and tool window**: a dialog the player answers or a developer window (export, edit box, debug console, perf panel, sim panel); Blizzard StaticPopups live here | **DIALOG** | `MODAL` | **toplevel** / clamped | BankLedger, LootHistory and MultiMeters export dialogs; DropWatcher edit box; the three LibKa0s tool windows |
| T7 | **Detached child window**: a window opened *from* a T6 window that must sit over it | **FULLSCREEN** (one strata above its opener) | `CHILD` | not toplevel / clamped | LibKa0s `CopyWindow` (console Copy, export copy windows, QuickComms Share) |
| T8 | **Transient popup**: dropdown menu, autocomplete, suggestion list, context menu, AceGUI pullout, colour picker, a borrowed confirmation lifted while shown, a drag-time full-screen highlight | **FULLSCREEN_DIALOG**, clamped, closed when its opener hides, dismissed by `GLOBAL_MOUSE_DOWN` | `POPUP` | — / clamped | LibKa0s menu and autocomplete, IdList suggestions, LootHistory/BankLedger row menus, AuraMaster snap highlight, QuickComms lifted confirms |
| T9 | **Cursor**: tooltips, drag ghosts, an overlay that labels the frame under the cursor | **TOOLTIP** | `CURSOR` | — | GameTooltip, LibKa0s reorder ghost, AuraMaster frame picker |

Two collection-specific tiers are **documented exceptions**, allowed with a reasoned comment and a register row:

- **Secure fixed point.** A secure frame that shows in combat cannot change strata in combat, so its strata is
  chosen first and every insecure frame that must sit over it moves up a tier. QuickComms: the Comms Dial is
  DIALOG; its windows and modals sit at FULLSCREEN and its over-modal at FULLSCREEN_DIALOG (QC-06). A window that
  shares a strata with the addon's own modal band MUST NOT be toplevel or `Raise()`d (QuickComms preview window,
  `PreviewWindow.lua:35-38`).
- **Event-raised notice previewed from Settings.** A popup raised by a game event that the player sizes from the
  Settings panel MAY sit at DIALOG, not toplevel, `Raise()`d on explicit show out of combat, provided every true
  dialog in DIALOG is toplevel so a click on it wins. WhatGroup's group popup (WHA-Z02). A flat "windows are
  HIGH" rule would hide its Test mode preview under the Settings panel on the first click.

What the tiers guarantee by construction:

- A HUD can never cover the addon's dialogs, popups or tooltips (T1 to T3 stop below DIALOG; only a legacy
  player choice can reach DIALOG, and its tooltip says so).
- **Dropdowns and menus are unaffected**: nothing an addon draws sits at FULLSCREEN_DIALOG or above except T8 and
  T9 surfaces, so AceGUI pullouts, the LibKa0s menu, Blizzard `Menu` and the colour picker open over every window.
  A window that wants an AceGUI pullout to open over it stays at or below FULLSCREEN.
- A window opened from another window sits at least one tier above it (T4 < T6 < T7 < T8).
- Tooltips are always on top, and the Blizzard Settings panel (HIGH) is never covered by a default HUD.

## 3. The level bands

Levels are always written as `base:GetFrameLevel() + LAYERS.LEVEL.<NAME>`, where `base` is the frame that owns
the band. The order in each ladder is **normative**; the numbers are the addon's own, named once in its layers
table, and SHOULD use the reference values where the classes match so the collection reads alike.

### 3.1 Inside one display element (a bar, an icon, a button, a wedge, a row)

| rung | reference offset (from the element root `E`) | holds |
|---|---|---|
| E0 | `E` itself (regions only) | background, icon texture, backdrop fill drawn on the root |
| E1 `FILL` | +1 | progress: StatusBar fill, cooldown swipe (explicit, never the implicit default), spark riding the fill |
| E2 `BORDER` | +2 | borders and frame chrome: backdrop edges, icon borders, dispel edges. **A border is a frame above the fill**, or the fill is inset by the full border width |
| E3 `EFFECT` | +3 | glow hosts. `LibKa0s-Glow-1.0`'s `Start(..., frameLevel)` is passed a small explicit `frameLevel` (1 or 2) so LibCustomGlow's default +8 does not leap over E4 |
| E4 `OVERLAY` | +4 | one **mouse-off overlay child frame** holding every region that must read over the rest: text (OVERLAY sublevel 0), marks and padlocks, and state veils, washes and highlights (higher sublevels, so a dim veil dims the label too) |

An addon-specific class slots between rungs under its own name (ConsumableMaster's flyout indicator between FILL
and BORDER, AuraMaster's dispel edge above BORDER, QuickComms' nested button-border/glow/icon-border/glow pairs)
provided the canonical order still holds for every element. Nested pairs follow the order per pair.

Text above effects is a deliberate departure from Blizzard's action button, whose proc alert covers the count
text. Legibility of numbers wins in a Ka0s display; an addon that wants the Blizzard look records it as a
deviation.

### 3.2 Inside one HUD display (root `L`)

| band | reference offset | holds |
|---|---|---|
| backplate | `L` | drag holders and plates (T2b); the root's own regions |
| content | `L+1` … `L+19` | elements and their E0–E4 ladders; per-element-class sub-bands when sibling classes overlap (PFE: pet +1, target +5, cast bar +9; KickCD: cast bar = grid +20) |
| label | `L+20` | name labels that may be nudged over the content |
| outline | `L+30` | unlock outline |
| marker | `L+40` | test/sim marker that **overlays** the display (a displacing strip stays at the content's chrome level) |
| handle | `L+50` | drag handle, its help and close marks; resize grip shown while unlocked |

The handle is the top of its display. When two displays of one addon can overlap, the handle clears the top
content band of both (KickCD `HUD_LEVEL + 39` over a cast bar at `+20`). A marker and a handle that never show
together MAY share or invert a slot only when the exclusion is enforced in code (KickCD `Sim.lua:117-119, :333`).

### 3.3 Inside one window (base `W`)

| band | reference offset | holds |
|---|---|---|
| frame | `W` | backdrop, title, divider (regions) |
| chrome | `W+1` | title bar / drag bar, close and header controls (controls +1 over the drag bar where they overlap it), tab strip, body, displacing test/sim strips |
| content | `W+2` … `W+8` | panes, filter bars, tables, rows, cells, cards; a pane laid inside another's rectangle gets an explicit level above it (DpsRace detail pane) |
| row overlay | above the cells it marks | selection edges, hover washes (MultiMeters `ROW_OVERLAY`) |
| grip | `W+10` | the library resize grip (`Core.lua:546`, `GRIP_LEVEL`). Content stays at or below `W+8` so the grip clears it |
| popover | `W+30` … | a popover over the window's own content, in the window's strata (DropWatcher floating Offer panel +30, compact Filters panel +35) |
| modal over the window | own strata (T6) | an input box the player must answer (DropWatcher edit box, DIALOG, +40 as belt and braces) |

## 4. The rules

Each rule has an id used in the conventions list of the structured result and in section 10.

**Tiers**

- **XS-01 Two axes.** Strata separates roles (section 2's tiers); frame level orders frames within one role.
  Different owners or roles never rely on a level race to stay apart.
- **XS-02 Non-visual frames are exempt.** Event frames, binding click targets, ESC proxies, measurers and hidden
  parents set no strata and no level, and an audit does not flag them.
- **XS-03 A HUD states its tier on its root.** The display root calls `SetFrameStrata(LAYERS.STRATA.HUD)` in the
  same block as its `CreateFrame`, even when the value equals the inherited one; children inherit and set no strata
  of their own unless XS-05 or XS-11 says so. A player-facing strata choice offers BACKGROUND to HIGH; a knob
  shipped before this rule keeps its stored values and its tooltip names what DIALOG covers.
- **XS-04 Attached and decorating surfaces match their host.** A surface grafted onto a host frame reads the
  host's strata (or inherits it) and raises its level by a named offset over the host; it never restates the
  host's strata as a literal. Elements that decorate a host's frames copy its strata and stack one level over its
  highest readable descendant, guarded against secret values and forbidden frames.
- **XS-05 Edit chrome is reachable, on top and undimmed.** Chrome lives in the display's strata at the top of the
  display's band (3.2). Where the display's strata can be below MEDIUM, mouse-enabled chrome is floored at
  `max(display, MEDIUM)` and mouse-off chrome MAY float at `max(display, HIGH)`, with `SetFixedFrameStrata(true)`
  re-applied after every parent strata write; a lift is never below the parent. A drag affordance does not
  inherit the display's content alpha (`SetIgnoreParentAlpha(true)`). A backplate sits at the root's level under
  every element, and the elements above it pass the mouse through or forward their drag.
- **XS-06 Windows are toplevel.** A movable window calls `SetToplevel(true)`. Persistent windows sit at MEDIUM,
  on-demand browsers at HIGH. A window whose own frame takes no mouse adds an explicit `Raise()` on drag start.
  Exceptions are the two documented in section 2 (secure fixed point; event-raised notice).
- **XS-07 Alerts.** An interactive toast sits at HIGH, over windows and under modals. A non-interactive screen
  alert sits at FULLSCREEN with the mouse disabled, never in the popup tier, so a menu always draws over it.
- **XS-08 Modals and tool windows.** DIALOG, toplevel, clamped. A destructive confirmation is never buried by a
  window the same addon showed after it: a tool window that is toplevel re-raises a shown StaticPopup when it is
  itself shown. An addon that lets the player put its own frames in DIALOG or above keeps its own confirmations
  answerable, without restyling shared Blizzard frames permanently.
- **XS-09 A window opened from a window sits at least one strata above its opener.** The detached child window
  tier is FULLSCREEN for an opener in DIALOG.
- **XS-10 Transient popups.** FULLSCREEN_DIALOG, clamped, closed on every path its opener closes (OnHide, the
  disable ladder, Escape), dismissed by a `GLOBAL_MOUSE_DOWN` listener that ignores presses inside it. No
  full-screen click catcher for a transient popup. A HUD popup goes one strata above its HUD root, set once at
  construction (never per refresh), clamped like its root.
- **XS-11 Cursor tier.** Tooltips, drag ghosts and an overlay that labels the frame under the cursor sit at
  TOOLTIP. A drag-time full-screen highlight sits at FULLSCREEN_DIALOG, above every player-selectable strata and
  below tooltips.
- **XS-12 Pick the secure tier first.** Where an addon owns a secure frame that shows in combat, its strata is
  fixed first and the insecure stack is built around it; a window sharing a strata with the addon's modal band is
  not toplevel and is never raised.

**Levels**

- **XS-13 The element ladder.** Inside one display element: root regions < fill/progress < border < effects <
  overlay frame (text, marks, veils). The order is a MUST; the reference offsets 1/2/3/4 are a SHOULD.
- **XS-14 A region never has to draw over a child frame of its own frame.** Anything that marks or overlays a
  child frame (text over a cooldown, a highlight over cells, a wash over buttons, a veil over a glow) lives on its
  own mouse-off overlay child frame at the top of the element's band. An overlay frame over a clickable or secure
  button is `EnableMouse(false)`.
- **XS-15 No absolute levels.** Every level is `base:GetFrameLevel() + LAYERS.LEVEL.X`. A player-chosen level is a
  base, not an exception; a measured level (a combat cover over the deepest descendant, PFE's host walk) is
  relative by construction. Levels read under a restricted anchor go through a secret-safe guard.
- **XS-16 One layers table per addon.** `NS.Constants.LAYERS = { STRATA = { … }, LEVEL = { … } }` in
  `core/Constants.lua`, keyed by section 2's tier keys and section 3's band names, its header comment stating the
  addon's stack once (including the library- and Blizzard-owned tiers it relies on). Every `SetFrameStrata` and
  `SetFrameLevel` in the addon reads it; no strata string and no bare level number at a call site. An addon with a
  single explicit strata call MAY use one named local constant with the same comment. `docs/ARCHITECTURE.md`
  points at the table rather than copying it, so the record cannot go stale. A frameless addon owns no strata and
  pins that with a static test.
- **XS-17 Overlapping siblings that both draw never tie.** They get explicit, distinct levels. A sibling that
  draws nothing and takes no mouse, or siblings separated by geometry and documented as such, need no band of
  their own; do not add bands for non-problems.
- **XS-18 Re-assert what moves.** An explicit level is set again after every `SetParent` and wherever the code
  re-levels its base (a restack), never only in a memoized restyle. Set a frame's level before its children are
  built where possible. A child given its own strata is `SetFixedFrameStrata(true)` and re-lifted after every
  parent strata write. Children deliberately sunk to the parent's level (non-interactive art) are re-sunk by any
  code that re-levels the parent.
- **XS-19 Peers stack whole.** Several frames of one kind that can overlap (bars, windows, panels, grids) get a
  defined order: toplevel or an explicit `Raise()` on interaction, or a deterministic per-instance base with a
  stride at least the element's band height. Where the player sets equal levels, interleaving MAY stay, provided
  the setting's tooltip says so.
- **XS-20 Library bands are part of the addon's map.** The library's grip (+10), drop line (+20), reorder box (−1)
  and combat cover (computed) are named in the addon's table comment, and a window keeps its content at or below
  +8 so the grip clears it. A degraded fallback reproduces the library's offsets.
- **XS-21 Never switch strata to fix an order.** A level does that. The exceptions are a strata the player
  chose, and lifting a borrowed shared Blizzard frame while it is shown, restoring the value recorded on show.
- **XS-22 Clamp popups as their roots are clamped**, the library's own menus included.
- **XS-23 Nothing invisible stays mouse-live.** A frame soft-hidden at alpha 0 (because it parents a secure child
  and cannot hide in combat) is made mouse-dead; a secure child that cannot be is disarmed at
  `PLAYER_REGEN_DISABLED`, or the residual is recorded.
- **XS-24 Combat.** Strata, level and toplevel writes on a protected frame, or on a frame secure elements are
  anchored to, go through the addon's secure queue and run out of combat.

## 5. Anti-patterns

Proposed for `anti-patterns.md`. The numbers are provisional: the next free number is #98 at v2.87.0, and items
015 and 020 of this bundle may claim numbers first, so the landing commit assigns them in order.

- **#98 Layering by accident.** A strata string or a bare level number at a call site; an addon with explicit
  layering and no layers table; an absolute `SetFrameLevel(n)`; a level set relative to a sibling (`dragBar + 5`);
  a level captured once against a base that moves later (a pooled carrier on GameTooltip, a raised parent); a
  layering comment that states a reason that is no longer true (a "catcher" the library retired).
- **#99 An overlay under what it overlays.** Text, marks, veils, highlights or washes drawn as regions of a frame
  whose child frames (cooldown, border, glow host, cells, buttons) cover them; a border drawn on the parent under
  a fill child; two overlapping drawing siblings left at the default parent + 1.
- **#100 Edit chrome that cannot be reached.** A drag handle, outline or grip that inherits a player strata below
  the UI over it, ties with the content it edits, sits under a sibling display's content, or fades with the
  display's alpha while still clickable; a drag plate drawn over the display it moves.
- **#101 A HUD in the dialog tiers.** A new player-facing strata choice above HIGH; a HUD, HUD popup or HUD
  window hard-set to DIALOG or above without a secure-fixed-point register row; a strata jump used to beat a
  level problem, or strata switched at runtime to change an order.
- **#102 Windows ordered by accident.** Two movable windows sharing a strata where clicking the lower one does not
  raise it; a library tool window that is not toplevel; a window opened from another window in a lower or equal
  strata at a lower level.
- **#103 A transient popup that misbehaves.** A full-screen click catcher behind a menu; a popup that outlives its
  opener's hide; an unclamped popup; a popup in the same strata as a non-interactive alert.
- **#104 An invisible frame that still takes the mouse, or a shared Blizzard frame left re-strata'd.** An alpha-0
  soft-hidden window still mouse-enabled; a StaticPopup raised and not restored to the value recorded on show.

## 6. Library- and third-party-owned tiers

### 6.1 What every addon inherits

| frame | strata | level | toplevel / clamped | owner |
|---|---|---|---|---|
| Debug console | DIALOG (`DebugLog.lua:536`) | inherited; Diagnostics link +1 (`:337`) | **not toplevel** / clamped | LibKa0s |
| Perf panel | DIALOG (`PerfPanel.lua:186`) | inherited | **not toplevel** / clamped | LibKa0s |
| Sim step panel | DIALOG (`SimPanel.lua:211`) | inherited | **not toplevel** / clamped | LibKa0s |
| Copy window | FULLSCREEN (`Widgets.lua:653`) | inherited | not toplevel / clamped | LibKa0s |
| Dropdown menu (process singleton) | FULLSCREEN_DIALOG (`Widgets.lua:225`) | inherited | — / **not clamped** | LibKa0s |
| Autocomplete list | FULLSCREEN_DIALOG (`WidgetsAutocomplete.lua:66`, overridable via `opts.strata`) | inherited | — / **not clamped** | LibKa0s |
| IdList suggestion list | FULLSCREEN_DIALOG (`OptionsIds.lua:997`) | inherited | clamped | LibKa0s |
| Reorder ghost / drop line / row box | TOOLTIP (`WidgetsReorder.lua:107`) / inherited / inherited | — / +20 / −1 | — | LibKa0s |
| Resize grip | inherited | +10 (`Core.lua:546, :611`) | — | LibKa0s |
| Tab strip / tab buttons | inherited | = body / +1 (`OptionsTabs.lua:375, :714`) | — | LibKa0s |
| Combat cover | inherited | `max(panel+100, deepest+1)`, capped 10000 (`OptionsCombat.lua:157-182`) | — | LibKa0s |
| Drag handle and its marks | inherited | parent + 1 / handle + 1 (no level option) | — | LibKa0s |
| Test / sim strip | inherited | parent + 1 (a displacing strip) | — | LibKa0s |
| Glow effect frames | inherited | host + `frameLevel` (LCG default +8 when none passed) | — | LibCustomGlow via LibKa0s-Glow |
| Settings panel | HIGH, toplevel (*verify*) | Blizzard | toplevel | Blizzard |
| StaticPopups | DIALOG, toplevel | Blizzard | toplevel | Blizzard |
| AceGUI dropdown pullouts, colour picker | FULLSCREEN_DIALOG | AceGUI | scroll toplevel / clamped | AceGUI |
| AGSMW (LSM30) media pullouts | TOOLTIP | AGSMW | — | AceGUI-3.0-SharedMediaWidgets |
| AceConfigDialog confirmation (Profiles) | TOOLTIP, level 100 | fixed | — | AceConfigDialog |
| Minimap button | MEDIUM fixed, level 8 fixed | LibDBIcon | — | LibDBIcon |
| GameTooltip, `AceGUITooltip` | TOOLTIP | Blizzard / template | — | Blizzard / AceGUI |

### 6.2 How LibKa0s's own frames measure up against the model

| frame | model tier | verdict |
|---|---|---|
| Debug console, perf panel, sim panel | T6 modal/tool window | strata right; **missing toplevel** (XS-06, XS-08). Reported by 9 of 15 analyses |
| Copy window | T7 detached child | right (one strata above the DIALOG opener, reason commented at `Widgets.lua:651-652`) |
| Dropdown menu, autocomplete | T8 popup | strata right, dismissal right (`GLOBAL_MOUSE_DOWN`, no catcher since Widgets minor 5); **not clamped** (XS-22) |
| IdList suggestions | T8 popup | strata right and clamped; on UIParent it escapes the combat cover over its page (BAN-S11, *verify*) |
| Reorder ghost | T9 cursor | right; shares TOOLTIP with GameTooltip, cosmetic |
| Resize grip | window band `W+10` | right; headroom against content depth is undocumented (DPS-S07, DRO-S07) |
| Drag handle | T2 chrome | inherits parent + 1, so it ties with the content it edits (ABS-S04, KIC-S06, CON-S08), and fades with the host's alpha (ABS-S05); hosts re-level it after its marks are built, which risks the marks (CON-Z08, KIC-Z07) |
| Combat cover, tab strip, drop line, reorder box | in-page bands | right: relative and measured |
| Test / sim strip | displacing chrome | right for a strip that pushes content down; a host that overlays it raises it itself |
| Glow | effect rung | right: `frameLevel` is already a parameter; hosts must pass it (KickCD does not) |

LibKa0s's strata choices are consistent with each other and with the model. The defects are four small omissions
(toplevel, clamping, a DragHandle level/alpha option, the IdList list outliving the cover), none of which needs a
new public tier table.

## 7. LibKa0s recommendation

**A change is needed, and it is small and additive.** No new module, no tier constants table.

| id | change | why | confidence |
|---|---|---|---|
| LK-01 | `DebugLog.lua:536`, `PerfPanel.lua:186`, `SimPanel.lua:211`: `frame:SetToplevel(true)`. In the same change, each window's `OnShow` re-raises any shown Blizzard StaticPopup (`StaticPopup1`…`StaticPopup4`, `:IsShown()` then `:Raise()`), so a tool window shown after a confirmation never covers it (PrettyChat S02). `CopyWindow` is **excluded**: it is already one strata above its opener, and a toplevel FULLSCREEN window would rise over QuickComms' FULLSCREEN modal band on show (XS-12). A LibKa0s suite pin asserts the three windows are DIALOG and toplevel, so a minor cannot drop the console under the Settings panel the Test button opens it from (moved here from PrettyChat PRE-Z04). | Requested by 9 analyses (ABS-Z07, BAN-Z08, KIC-Z10, MUL-Z10, PAR-Z10, PrettyChat PRE-Z01+Z02, WHA S08, LOO S05, DPS). One library edit fixes 15 addons by re-vendor. `Raise` on a StaticPopup is a C method on a non-protected frame. | 65% |
| LK-02 | `WidgetsDragHandle.lua` `lib.DragHandle(parent, spec)`: two optional spec fields. `level` (number): the handle's level offset over `parent:GetFrameLevel()`, applied before `dhBuildHelp`/`dhBuildClose` so the marks are born at handle + 1, and re-applied by a `handle:ApplyLevel()` method a host calls after it re-levels the parent. `ignoreParentAlpha` (boolean): `SetIgnoreParentAlpha(true)` on the handle. Both default to today's behaviour. DragHandle minor 5. | Five addons re-level the handle by hand after construction (ABS-Z04, AUR handle L+50, CON-Z08, KIC-Z07, QuickComms strip) and four alpha their display (AbsorbTracker, AuraMaster, ConsumableMaster, QuickComms); the host route risks the help and close marks drawing under the strip. | 70% |
| LK-03 | `Widgets.lua:224` dropdown menu and `WidgetsAutocomplete.lua:161` list: `SetClampedToScreen(true)`. | XS-22; LootHistory clamps its own row menu and is ahead of the library it borrows from (LOO-S09). | 75% |
| LK-04 | `OptionsIds.lua` suggestion list: closed by the combat cover's owned-focus release (`__releaseOwnedFocus`, `OptionsCombat.lua`), as AceGUI pullouts already are. Land only after an in-client check shows it stays clickable over a locked page. | A T8 popup must not outlive the lock over its page (BAN-S11). | 45% |
| LK-05 (optional, deferred) | A `strata` field on the DebugLog descriptor, the PerfPanel descriptor and `CopyWindow` (default unchanged), with the console's copy window opening one strata above whatever the console uses. | Only QuickComms (dial at DIALOG, QUI-Z05/Z06, 45-50%) and PGFE (surface at FULLSCREEN, PGFE PRE-Z05, 40%) need it, and both cases are developer-facing. Recommend filing it as a LibKa0s issue and not landing it in this run. | 40% |

Considered and rejected for LibKa0s:

- **A published tier table (`lib.STRATA` / `Core.LAYERS`).** Asked for by BankLedger, LootHistory, WhatGroup and
  ConsumableMaster. Rejected: it carries no behaviour (the values are Blizzard's strings), each addon needs a
  table anyway for its own level bands, and a library table would let a library minor re-tier fifteen addons'
  host frames, where the standard says a value every Ka0s window shares is a standard change first. The standard
  publishes the tier keys (section 2); each addon's `NS.Constants.LAYERS` uses them. Confidence that this is right:
  60%.
- **`W.ContextMenu`** (LOO-Z02 library variant, BankLedger has the identical catcher menu). A new widget surface;
  both addons can take the local `GLOBAL_MOUSE_DOWN` fix in this run. Record in open-evolutions.
- **A StaticPopup lift-while-shown helper** (QuickComms `ModalWindow.LiftConfirm`, PGFE PRE-Z03, gated on an
  in-client confirmation). Record in open-evolutions; promote if PGFE's case is confirmed.
- **A guarded `LevelOf(frame, fallback)`** (AuraMaster). One consumer; record in open-evolutions.
- **A grip level computed over the deepest descendant.** No collision today; documenting the +8 content ceiling
  (XS-20) is enough.

## 8. Draft WowAddonStandards text

### 8.1 Where it goes

No current section mentions strata (`grep -i strata standards/standards/*.md` finds only debug-logging's one
clause). The rules are cross-cutting (HUD, windows, popups, settings, library frames), so they get a **new section
file**, `standards/standards/frame-layering.md`, listed in `STANDARDS.md`'s Sections list after
`preview-mode`, with small pointer edits elsewhere (8.3). Version: the next minor at landing (v2.88.0 if nothing
lands first).

### 8.2 Full proposed prose: `standards/standards/frame-layering.md`

```markdown
> Part of the **[Ka0s WoW Addon Standard](../STANDARDS.md)** — the split standard. Cross-references use the `filename-§N` form (see the index's section map).

## Frame layering: strata and frame level

Every frame an addon draws sits somewhere in the client's draw order: strata first (`BACKGROUND`, `LOW`, `MEDIUM`, `HIGH`, `DIALOG`, `FULLSCREEN`, `FULLSCREEN_DIALOG`, `TOOLTIP`), then frame level within the strata, then draw layer and sublevel for regions within one level. This section says where each kind of element goes, so that "what strata?" is a lookup rather than a choice, and so that every visual element of one addon layers by one rule.

Two client facts drive most of it. **A child frame draws over every region of its parent**, whatever the region's draw layer, so an `OVERLAY` texture on a button sits under the button's cooldown or border child. **A child with no explicit level is at parent + 1**, so siblings tie, and a tie between overlapping frames that both draw is broken by creation order, which pooling and lazy builds scramble. The 2026-10-24 collection review found both in more than half the addons.

### 1. Strata separates roles; level orders within a role (MUST)

Elements of different roles are separated by **strata**. Elements within one role are ordered by **named level bands** (§3). An addon **MUST NOT** rely on a frame-level race to keep its window above another addon's or Blizzard's frame in the same strata.

| tier | element class | strata | layers-table key |
|---|---|---|---|
| T0 | non-visual frames: event frames, binding click targets, ESC proxies, measurers, hidden parents | none (exempt) | — |
| T1 | HUD display: a world-anchored, persistent display (bar, icon grid, cast bar, meter, pad) | `MEDIUM`, set on the display root | `HUD` |
| T2 | edit-mode chrome: drag handles, unlock outlines, overlaying test and sim markers, unlock-only grips | the display's strata (§2) | `CHROME` |
| T3 | HUD popup: a transient surface opened from a HUD element | one strata above the HUD root, or its Blizzard equivalent's | `HUD_POPUP` |
| T4 | window: persistent (kept up while playing) / on demand (opened to read) | `MEDIUM` / `HIGH` | `WINDOW` |
| T5 | alert: interactive toast / non-interactive screen alert | `HIGH` / `FULLSCREEN`, mouse disabled | `ALERT` / `SCREEN_ALERT` |
| T6 | modal and tool window: dialogs the player answers, the debug console, perf and sim panels; Blizzard StaticPopups live here | `DIALOG` | `MODAL` |
| T7 | detached child window opened from a T6 window | `FULLSCREEN` | `CHILD` |
| T8 | transient popup: menu, autocomplete, suggestion list, context menu, pullout, colour picker, a borrowed confirmation lifted while shown, a drag-time full-screen highlight | `FULLSCREEN_DIALOG` | `POPUP` |
| T9 | cursor: tooltips, drag ghosts, an overlay that labels the frame under the cursor | `TOOLTIP` | `CURSOR` |

What the ladder guarantees, and why each line is where it is:

- A HUD never covers the addon's own dialogs, popups or tooltips, and never covers the Blizzard Settings panel (`HIGH`) by default.
- **Dropdowns, menus and tooltips are never covered.** Nothing an addon draws sits at `FULLSCREEN_DIALOG` or above except T8 and T9 surfaces, so AceGUI pullouts, the `LibKa0s-Widgets-1.0` menu and Blizzard's `Menu` open over every window. A window that wants a pullout to open over it **MUST** stay at or below `FULLSCREEN`.
- A frame opened from another frame sits **at least one strata above its opener** (T4 < T6 < T7 < T8). The library's copy window, `FULLSCREEN` over the `DIALOG` console that opens it, is the reference.
- A non-interactive alert is not in the popup strata, so a menu opened while it shows draws over it.

**Variants of T1.**
- **Player-chosen strata.** A display whose strata is a setting **MUST** offer `BACKGROUND`, `LOW`, `MEDIUM` and `HIGH` only. A knob that shipped before v2.88.0 with `DIALOG` or higher keeps its stored values (a value-set change needs a migration and an owner decision), and its tooltip **MUST** say what those values cover: the addon's own popups and debug console, and the Settings window.
- **Host-matched surfaces.** A surface grafted onto another addon's or Blizzard's frame **MUST** take the host's strata by reading it (`host:GetFrameStrata()`) or by inheriting it, never by restating it as a literal, and raises its level by a named offset over the host. Elements that decorate a host's frames copy its strata and stack one level over its highest readable descendant, the read guarded against secret values and forbidden frames.
- **Player-layered backdrops.** An addon whose purpose is letting the player compose strata and level (a backdrop panel addon) **MAY** offer every strata, as a row in its `## Documented deviations`; it **MUST** keep its own confirmations answerable while its frames are unlocked (§4).

**Documented exceptions** (each **MUST** carry a reasoned comment at the call site and a `## Documented deviations` row):
- **The secure fixed point.** A secure frame that shows in combat cannot change strata in combat, so its strata is chosen first and every insecure frame that must sit over it moves up a tier. A window that shares a strata with the addon's own modal band **MUST NOT** be toplevel or `Raise()`d, because a raise lifts it over the modal's catcher.
- **The event-raised notice previewed from Settings.** A popup raised by a game event that the player sizes or places from the Settings panel **MAY** sit at `DIALOG`, not toplevel, `Raise()`d on an explicit show out of combat, provided every true dialog at `DIALOG` is toplevel.

### 2. Edit-mode chrome (MUST)

Chrome lives in the display's strata at the **top of the display's band** (§3), above every content level of every display of the same addon that can overlap it.

- Where the display's strata can be below `MEDIUM` (a player choice, a host it follows), mouse-enabled chrome **MUST** be floored at `max(display, MEDIUM)`; mouse-off chrome **MAY** float at `max(display, HIGH)`. A child given its own strata **MUST** be `SetFixedFrameStrata(true)` and re-lifted after every `SetFrameStrata` on its parent, which otherwise takes it back. A lift is never below the parent.
- A drag affordance (handle, close mark, grip) **SHOULD NOT** inherit the display's content alpha: `SetIgnoreParentAlpha(true)`, or `LibKa0s-Widgets-1.0` `DragHandle`'s `ignoreParentAlpha`. An affordance that fades to invisible while still clickable is anti-pattern #100.
- A drag **backplate** (a holder the display is dragged by) sits at the display root's level, under every element, and the elements over it pass the mouse through or forward their drag.
- Order within chrome: outline < overlaying marker < handle and its marks. A marker and a handle that never show together **MAY** share or invert a slot only when the exclusion is enforced in code.
- A test or sim strip that **displaces** content (pushes it down by its height) stays at the content's chrome level; one that **covers** content is raised above the content band.

### 3. Level bands (MUST)

**Every level is relative**: `base:GetFrameLevel() + LAYERS.LEVEL.<NAME>`. An addon **MUST NOT** call `SetFrameLevel` with an absolute number, and **MUST NOT** set a level relative to a sibling. A player-chosen level is a base, not an exception; a measured level (the library's combat cover, computed over the deepest descendant and capped at 10000) is relative by construction. A level read under a restricted anchor goes through a secret-safe guard (events-frames-taint-§8).

**Inside one display element** (a bar, an icon, a button, a row) the order is normative:

| rung | reference offset from the element root | holds |
|---|---|---|
| root | +0 (regions) | background, icon texture, a fill drawn on the root |
| `FILL` | +1 | progress: the StatusBar fill, the cooldown swipe (given an explicit level, never the implicit default), a spark riding the fill |
| `BORDER` | +2 | borders: backdrop edges, icon borders, dispel edges. A border is a frame **above** the fill, or the fill is inset by the full border width |
| `EFFECT` | +3 | glow hosts. `LibKa0s-Glow-1.0`'s `Start` **MUST** be passed an explicit small `frameLevel`, so LibCustomGlow's default +8 does not leap over the overlay |
| `OVERLAY` | +4 | one **mouse-off overlay child frame** holding text, marks and padlocks (sublevel 0) and state veils, washes and highlights (higher sublevels) |

The order is a **MUST**; the offsets are a **SHOULD**, and an addon-specific class (an indicator, a spark, a dispel edge) slots between rungs under its own name as long as the order holds. **A region never has to draw over a child frame of its own frame**: anything that marks or overlays a child frame lives on the overlay frame. An overlay frame laid over a clickable or secure button **MUST** be `EnableMouse(false)`.

**Inside one HUD display** (root level `L`): backplate `L`; content `L+1` to `L+19`, with per-class sub-bands where sibling classes overlap; label `L+20`; outline `L+30`; overlaying marker `L+40`; handle `L+50`. **Inside one window** (base `W`): chrome `W+1` (title or drag bar, header controls, tab strip, body, displacing strips); content `W+2` to `W+8`; the library grip `W+10`; popovers over the window's own content `W+30` and up, **in the window's strata**. A popover over its own window is a level problem, never a reason to jump strata.

- **Siblings.** Two overlapping siblings that both draw **MUST** have explicit, distinct levels. A sibling that draws nothing and takes no mouse, or siblings kept apart by documented geometry, need no band.
- **Re-assert what moves.** An explicit level **MUST** be set again after every `SetParent` (which re-derives it) and by the code that re-levels its base, never only in a memoized restyle. Set a frame's level before its children are built where possible. Art deliberately sunk to its parent's level is re-sunk by any code that re-levels the parent.
- **Peers stack whole.** Several frames of one kind that can overlap (bars, windows, panels) **MUST** have a defined order: toplevel or an explicit `Raise()` on interaction, or a deterministic per-instance base with a stride at least the element's band height. Where the player sets equal levels, interleaving **MAY** stay if the setting's tooltip says so.
- **Library bands are part of the map.** The library's grip (+10), reorder drop line (+20) and reorder box (−1) are named in the addon's table comment, and a window's content stays at or below +8. A degraded fallback reproduces the library's offsets.

### 4. Windows, modals and popups (MUST)

- **Windows are toplevel.** A movable window **MUST** call `SetToplevel(true)`, so a click raises it among its strata peers (the Settings panel included, for a `HIGH` window). A window whose own frame takes no mouse adds `Raise()` on drag start. The two §1 exceptions apply.
- **Modals and tool windows** sit at `DIALOG`, toplevel, clamped. A destructive confirmation is never buried by a window the same addon showed after it: a toplevel tool window re-raises a shown StaticPopup when it shows (the library's do).
- **Transient popups** sit at `FULLSCREEN_DIALOG`, **MUST** be clamped as their opener is, **MUST** close on every path their opener closes (its `OnHide`, the disable ladder, Escape), and **MUST** be dismissed by a `GLOBAL_MOUSE_DOWN` listener that ignores presses inside the popup. A full-screen click catcher behind a transient popup is forbidden: it swallows the click that dismisses, which is why the library retired its own (Widgets minor 5). A modal's dimming scrim that closes with its modal is not a catcher.
- **A HUD popup** sits one strata above its HUD root, set **once at construction** (never per refresh, never by a runtime strata switch), clamped like its root, and where Blizzard ships an equivalent (an action-button flyout), at that equivalent's strata.
- **Never switch strata to fix an order.** Set a level. The exceptions are a strata the player chose, and a borrowed **shared** Blizzard frame (a StaticPopup) lifted while it is shown and put back, on hide, to the strata recorded on show, never to a hard-coded value.
- **Nothing invisible stays mouse-live.** A frame soft-hidden at alpha 0 because it parents a secure child **MUST** be made mouse-dead; a secure child that cannot be (its `EnableMouse` is refused in combat) is disarmed at `PLAYER_REGEN_DISABLED`, or the residual is a `## Documented deviations` row.
- **Combat.** Strata, level and toplevel writes on a protected frame, or on a frame secure elements are anchored to, go through the addon's secure queue (events-frames-taint-§2).

### 5. One layers table per addon (MUST)

An addon that sets any strata or level **MUST** declare them once, in `core/Constants.lua`:

    NS.Constants.LAYERS = {
      STRATA = { HUD = "MEDIUM", MODAL = "DIALOG", ... },   -- §1's keys
      LEVEL  = { FILL = 1, BORDER = 2, EFFECT = 3, OVERLAY = 4, HANDLE = 50, ... },
    }

Its header comment states the addon's whole stack once, the library- and Blizzard-owned tiers it relies on included (debug console `DIALOG`, copy window `FULLSCREEN`, menus `FULLSCREEN_DIALOG`, grip +10). Every `SetFrameStrata` and `SetFrameLevel` in the addon reads it, so `grep -rn 'SetFrameStrata("' core modules settings` returns nothing and every `SetFrameLevel` argument names a `LAYERS.LEVEL` member. An addon with a single explicit strata call **MAY** use one named local constant carrying the same comment. `docs/ARCHITECTURE.md` points at the table in one line rather than copying it, because a copied tier table goes stale the first time a library choice changes.

**A frameless addon owns no strata.** An addon whose only surfaces are the Settings canvas, library windows and Blizzard or Ace3 popups **MUST NOT** call `SetFrameStrata`, `SetFrameLevel`, `SetToplevel` or `Raise` itself, and **SHOULD** pin that with a static test.

### 6. Library-owned tiers (reference)

What a Ka0s addon inherits, so its own tiers are placed around known neighbours. Changing a library row is a standard change first.

| frame | strata | level | toplevel / clamped |
|---|---|---|---|
| `LibKa0s-DebugLog-1.0` console, `LibKa0s-Perf-1.0` panel, `LibKa0s-Sim-1.0` step panel | `DIALOG` | inherited | toplevel / clamped |
| `LibKa0s-Widgets-1.0` `CopyWindow` | `FULLSCREEN` | inherited | not toplevel / clamped |
| `LibKa0s-Widgets-1.0` dropdown menu, autocomplete; `LibKa0s-Options-1.0` IdList suggestions | `FULLSCREEN_DIALOG` | inherited | clamped |
| `LibKa0s-Widgets-1.0` reorder ghost | `TOOLTIP` | — | — |
| `LibKa0s-Core-1.0` resize grip | inherited | +10 | — |
| `LibKa0s-Options-1.0` combat cover | inherited | `max(panel + 100, deepest + 1)`, capped 10000 | — |
| Blizzard Settings panel | `HIGH` | Blizzard | toplevel |
| Blizzard StaticPopups | `DIALOG` | Blizzard | toplevel |
| AceGUI pullouts and colour picker | `FULLSCREEN_DIALOG` | AceGUI | clamped |
| AceGUI-3.0-SharedMediaWidgets pullouts; AceConfigDialog confirmation | `TOOLTIP` (the latter at level 100) | — | — |
| LibDBIcon minimap button | `MEDIUM`, fixed | 8, fixed | — |

Third-party rows are documented, not fought: an addon **MUST NOT** re-strata a third-party or shared Blizzard frame except by the lift-and-restore of §4.
```

### 8.3 Ripple edits

| file | edit |
|---|---|
| `standards/STANDARDS.md` | Sections list: a `frame-layering` entry after `preview-mode` ("strata separates roles and level orders within a role: the ten-tier ladder from HUD `MEDIUM` to cursor `TOOLTIP`; edit chrome on top of its display and reachable; the element ladder fill < border < effect < overlay frame; relative levels only; toplevel windows; popups at `FULLSCREEN_DIALOG`, clamped, closed with their opener, no catchers; one `NS.Constants.LAYERS` table per addon"). Version and date bump. |
| `standards/standards/anti-patterns.md` | #98 to #104 as in section 5 (renumbered at landing). |
| `standards/standards/standalone-windows.md` | One bullet after the `UISpecialFrames` bullet: "**MUST** call `SetToplevel(true)` and sit in the window tier of frame-layering-§1 (`MEDIUM` persistent, `HIGH` on demand); a popup it opens closes with it (frame-layering-§4)." |
| `standards/standards/preview-mode.md` | One sentence in the marker bullet: "A marker that overlays the display sits in the display's chrome band (frame-layering-§2); a strip that displaces content stays at the content's chrome level." |
| `standards/standards/debug-logging.md` | The strata clause becomes: "on **`DIALOG`** strata, **toplevel**, so it sits above the addon's main window and comes forward on click (frame-layering-§1, T6); an addon whose own surface is at `DIALOG` or above records why its console may be covered." |
| `standards/standards/options-ui.md` | Where an addon exposes a strata setting: "the value set and tooltip follow frame-layering-§1 (player-chosen strata)." |
| `standards/standards/events-frames-taint.md` | §6 Frame creation gains: "**MUST** set a frame's strata in the same block as its `CreateFrame` where it sets one at all, read from the layers table (frame-layering-§5)." §2 gains the protected strata/level write line (frame-layering-§4). |
| `standards/standards/open-evolutions.md` | `W.ContextMenu`; a StaticPopup lift-while-shown helper; a guarded `LevelOf`; a `strata` option on the library's tool windows (LK-05). |
| `AUDIT.md` | A layering step: the two greps of frame-layering-§5, a check for regions that must draw over child frames (text under cooldown/border, highlight under cells), library tool windows toplevel (from the LibKa0s tag that ships LK-01), player strata knobs above `HIGH` without a tooltip warning, transient popups with a catcher or without a clamp. |
| `standards/NEW_ADDON_CONTEXT.md`, `NEW_ADDON.md` | The scaffold's `core/Constants.lua` carries an empty `LAYERS` table with the header comment template. |
| `standards/EXECUTIVE_SUMMARY.md`, `standards/CHANGELOG.md` | One line each. |

## 9. dev-copilot

The audit command reads `AUDIT.md` at run time, so it needs no change. One edit is needed:

- `profiles/wow/agent-review.md`: a **layering** check in the WoW review overlay, run over `core/ modules/
  settings/`: `SetFrameStrata("` literals, `SetFrameLevel(<number>)`, `SetFrameLevel(<sibling>:GetFrameLevel()`,
  movable windows without `SetToplevel`, `CreateFontString`/`CreateTexture` text on a frame that also gets a
  `Cooldown` or `BackdropTemplate` child, and `GLOBAL_MOUSE_DOWN`-less popups with a full-screen sibling at
  `SetAllPoints(UIParent)`. Each finding cites frame-layering-§N. Confidence 60%.

## 10. Per-addon check: overrides and adds

Every proposed change in the 15 analyses was checked against sections 2 to 4. Changes not listed below conform as
written and stand. **Bundle note:** PremadeGroupsFilterExtension and PrettyChat both use the `PRE-` prefix
(PGFE `PRE-Z01`…`Z08`, PrettyChat `PRE-Z01`…`Z05`). The ids below are qualified by addon; the plan should give
PGFE its own prefix (for example `PGF-`) before items are numbered.

| change id | action | note |
|---|---|---|
| AbsorbTracker ABS-Z01 | modify | Read `NS.Constants.LAYERS.STRATA.HUD`, not a literal `"MEDIUM"` (XS-16). Same visual result. |
| AbsorbTracker ABS-Z04 | modify | Set the handle level through LK-02's `level` spec field (`5`) once the LibKa0s tag ships; the host-side re-level is the fallback only for a tag without it. Removes the marks-under-strip risk. |
| AbsorbTracker ABS-Z06 | modify | Use LK-02's `ignoreParentAlpha = true` spec field rather than a host call, so the `tests/wow_mock.lua` stub is the library's to carry. |
| AbsorbTracker ABS-Z08 | modify | `docs/ARCHITECTURE.md` points at the layers table (one line); the tier table lives in the `LAYERS` header comment, not copied into the doc (XS-16). |
| AbsorbTracker ABS-Z09 | add | `core/Constants.lua`: `NS.Constants.LAYERS = { STRATA = { HUD = "MEDIUM" }, LEVEL = { FILL = 1, BORDER = 2, TEXT = 3, HANDLE = 5 } }`, read by Z01-Z04, with a headless pin that FILL < BORDER < TEXT < HANDLE. The analysis proposes the bands but no table (XS-16). 80%. |
| AuraMaster AUR-Z12 | add | Drag handle ignores the container's alpha (`Container.lua:772` sets `anchor:SetAlpha(layout.alpha × master)`; the handle is the anchor's child): pass `ignoreParentAlpha = true` through LK-02 at `Anchors.lua:663`. Same defect as ABS-S05 (XS-05). 60%. |
| BankLedger BAN-Z06 | modify | The table is the host's (`NS.Constants.LAYERS`), using the standard's tier keys (`WINDOW`, `MODAL`, `POPUP`); no LibKa0s tier table exists or is planned (section 7). Add `LEVEL.GRIP = 10` for Z07. |
| BankLedger BAN-Z08 | modify | Lands as LK-01: DebugLog and SimPanel (and PerfPanel) toplevel with the StaticPopup re-raise on show. |
| BankLedger BAN-Z10 | modify | Lands as LK-04 (close the suggestion list from the cover's owned-focus release), not a reparent; still gated on an in-client check. |
| ConsumableMaster CON-Z05 | modify | The level table becomes `NS.Constants.LAYERS` and also names the strata (`HUD = "MEDIUM"` for the bar, `HUD_POPUP` for the flyout, whose value is Z01's outcome), so `MacroBar.lua:225` and `MacroBarFlyout.lua:551` read it (XS-16). |
| ConsumableMaster CON-Z08 | modify | Raise the handle through LK-02's `level` spec field, which is the review's own preferred route; the host re-level after construction is dropped. |
| ConsumableMaster CON-Z10 | add | Drag handle ignores the bar's alpha (`MacroBar.lua:393-397` alphas the bar, mouseover fade included): LK-02 `ignoreParentAlpha = true`. Same defect as ABS-S05 (XS-05). 60%. |
| DpsRace DPS-Z06 | modify | ARCHITECTURE points at Z04's table instead of copying the strata map (XS-16). Z04 gains `LEVEL.DETAIL = 2` for Z03 so that offset is named too. |
| KickCD KIC-Z01 | modify | The text layer goes **above** the glow: `btn + 5` (`LEVEL.TEXT = 5`), not `btn + 3`. XS-13 orders effects under the overlay frame so the countdown and charges stay legible over a ready glow. |
| KickCD KIC-Z03 | modify | Glow host at `btn + 3` (`LEVEL.GLOW = 3`), and the `NS.GlowLib.Start(g, kind, vals, LCG_KEY)` call at `IconGrid_Render.lua:487` passes an explicit `frameLevel = 1` so LibCustomGlow's frames sit at `btn + 4`, under the text layer at `btn + 5`. Today no `frameLevel` is passed and LCG's +8 puts the glow above everything (KIC-S08). Visible change: the charges badge now draws over a proc glow. Owner look. 55%. |
| KickCD KIC-Z07 | modify | Through LK-02's `level` spec field (`HUD_LEVEL + 39` expressed as the offset over each handle's parent), which settles the review's open question about the help and close marks. |
| KickCD KIC-Z10 | modify | Lands as LK-01; the StaticPopup interaction the review accepted is closed by the re-raise on show. |
| LootHistory LOO-Z02 | modify | Take the local fix (75%). The `W.ContextMenu` library variant is not part of 030's minimal LibKa0s surface; it goes to open-evolutions with BankLedger's identical menu as the second consumer. |
| LootHistory LOO-Z06 | modify | Host table only, with the standard's tier keys; drop the "ideally LibKa0s's" variant (section 7). |
| LootHistory LOO-Z08 | modify | The library half (menu and autocomplete clamp) lands as LK-03; this change stays the row menu's clamp. |
| MultiMeters MUL-Z04 | supersede | Not planned. XS-03 keeps a pre-existing knob's stored values (DIALOG included) with a tooltip warning (layout MUL-L22); dropping DIALOG is a value-set change with a migration, which 020 forbids and 030 does not need. Left as an owner decision. |
| MultiMeters MUL-Z08 | modify | The table also names the strata (`MODAL = "DIALOG"` read at `Export_Modal.lua:738`; the window's default `HUD` value), so the addon has no strata literal left (XS-16). |
| MultiMeters MUL-Z09 | modify | ARCHITECTURE points at the table; the smoke tests stay in `docs/smoke-tests.md` and the bundle's smoke file. |
| MultiMeters MUL-Z10 | modify | Lands as LK-01. |
| PanelMaster PAN-Z03 | supersede | By PAN-Z03b (90%). XS-19 allows player-equal levels to interleave when the tooltip says so; Z03's cross-panel ranking adds coupling and still overflows at the ninth panel. |
| PanelMaster PAN-Z04 | modify | Conforms (the overlay is mouse-off, so XS-05 allows `max(panel, HIGH)`); record in the `LAYERS` comment that the floor is HIGH **because** the overlay takes no mouse, so nobody later makes it mouse-enabled without dropping the floor to MEDIUM. |
| PartyFrameEnhanced PAR-Z10 | modify | Lands as LK-01 (DebugLog, PerfPanel, SimPanel). |
| PartyFrameEnhanced PAR-Z11 | add | `NS.Constants.LAYERS` naming the element ladder (`FILL = 1`, `BORDER = 2`, `OVERLAY = 3`), the per-class sub-bands (`PET = 1`, `TARGET = 5`, `CASTBAR = 9`), `GRIP = 13` and the stand-in's fallback strata `"LOW"`, read by Z01, Z02, Z03, Z05 and Z07. The analysis adds several new offsets with no table (XS-16). 70%. |
| PGFE PRE-Z05 | modify | Becomes the optional LK-05, filed as a LibKa0s issue and not landed in this run (developer-facing, 40%). |
| PrettyChat PRE-Z01+Z02 | modify | Lands as LK-01, which is exactly the merged change, except that `CopyWindow` is excluded from toplevel (a toplevel FULLSCREEN window would rise over QuickComms' FULLSCREEN modal band on show, XS-12). |
| PrettyChat PRE-Z04 | modify | The library half (console is DIALOG and toplevel) is LK-01's suite pin, as the review already moved it. |
| QuickComms QUI-Z05 | modify | Becomes the optional LK-05 (developer-facing, 45%); not landed in this run. QuickComms records in its `LAYERS` comment that the dial can cover the console. |
| QuickComms QUI-Z06 | modify | The `CopyWindow` `strata` option is part of LK-05 and deferred with it. The local half stays: the Share window keeps the library's FULLSCREEN, now named in `NS.Layers` as the `WINDOW` tier, and the icon link window keeps its post-hoc lift with a comment pointing at the LibKa0s issue. |
| QuickComms QUI-Z11 | add | The pad's drag strip ignores the pad root's alpha (`Pad.lua:483` alphas the root by setting, combat and hover; the strip is its child): LK-02 `ignoreParentAlpha = true` at `Pad.lua:296`. Same defect as ABS-S05 (XS-05). 60%. |

Checked and conforming as written (no override): AuraMaster Z01-Z08, Z10; BankLedger Z01-Z05, Z07, Z09;
ConsumableMaster Z01-Z04, Z06, Z07, Z09; DpsRace Z01-Z05; DropWatcher Z01-Z08; KickCD Z02, Z04-Z06, Z08, Z09;
LootHistory Z01, Z03-Z05, Z07, Z09 (the edge colour is outside 030's scope and stays the owner's call); MultiMeters
Z01-Z03, Z05-Z07; PanelMaster Z01, Z02, Z03b, Z05-Z08; PartyFrameEnhanced Z01-Z05, Z07, Z09; PGFE PRE-Z01, Z03
(gated), Z06, Z08; PrettyChat PRE-Z03, Z05; QuickComms Z01-Z04, Z08-Z10 (the secure fixed point and the
never-raised preview window are section 2's documented exceptions); WhatGroup Z01-Z03, Z05, Z06 (the popup is
the event-raised-notice exception; `STRATA_POPUP` is the single-call named local XS-16 allows).

## 11. In-client verifications the model depends on

The owner runs these; none is marked passed here.

1. `/dump SettingsPanel:GetFrameStrata(), SettingsPanel:IsToplevel()`: expected `HIGH`, true (every analysis
   assumed it).
2. `/dump SpellFlyout:GetFrameStrata()`: decides ConsumableMaster CON-Z01 (HUD popup at its Blizzard equivalent's
   strata).
3. With `/fstack`, raise a parent that has an **explicitly** levelled child (a DragHandle after LK-02, a grip):
   does the child keep its offset? Decides whether XS-18's re-assertion is needed after a toplevel raise
   (ABS-Z05, MUL-Z02, DRO-Z05).
4. A toplevel frame shown while another is up: is it raised on show as well as on click? (LootHistory LOO-Z03,
   LK-01.)
5. LK-01: open a reset confirmation, then the debug console over it; the confirmation stays on top.
6. LK-04: open an IdList suggestion list, enter combat; is the list still clickable over the locked page?
