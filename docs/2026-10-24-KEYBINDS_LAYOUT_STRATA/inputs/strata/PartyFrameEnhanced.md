# PartyFrameEnhanced — frame strata analysis

Scope: item 030. Read from `../PartyFrameEnhanced` at `master` on 2026-10-24: `modules/{RangeFade,Element,CastBars,UnitButtons,TargetFrames,PetFrames,Anchor,StandIn,Preview,SecureFollow,Providers}.lua`,
`core/*.lua`, `settings/*.lua`, `defaults/Profile.lua`, and the vendored `libs/LibKa0s/{DebugLog,PerfPanel,PerfSampler,Options,OptionsCombat}.lua`
(v1.76.0). Read-only. Nothing was run in game, so the client's own levels (party frames, UIParent) are inferred
from the code's comments and Blizzard defaults, and are marked where it matters.

**How the addon layers today.** Each unit has one plain **fade frame** (`PartyFrameEnhanced_Fade_<unit>`, on
UIParent). That unit's cast bar, target frame and pet frame are all children of it. The fade frame is the **only**
frame whose strata and level the addon sets on purpose (`RangeFade.restack`, RangeFade.lua:264-280). With
`general.strata = auto` (the default) it copies the unit's party frame's strata and sits one level above that
frame's highest descendant. A fixed choice sets the strata but still takes the level from the party frame.
Everything else either inherits from the fade frame or is left at UIParent's default (**MEDIUM**), except the
stand-in (explicit LOW) and the raid-marker layer (one explicit level).

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Fade frame ×5 (`PartyFrameEnhanced_Fade_<unit>`) | modules/RangeFade.lua:77 | UIParent | **explicit**: copied from the party frame (auto) or `general.strata`; LOW fallback (:55, :254-260, :271) | **explicit**: party frame's top descendant + 1, capped 9000 (:59, :261, :272); 50 when the frame is unreadable (:58, :255); 1 with no frame (:254) | no / no | Never moved or sized, no regions, mouse off. Written through `NS.RunSecure("fade:strata")` (:284). Restacked on LAYOUT, VISIBILITY, PROFILE, CONFIG general/master (:351-361), only when the computed `STRATA:level` changed (:269-273). |
| Cast bar root ×5 (`PartyFrameEnhancedCastBar_<unit>`) | modules/CastBars.lua:371 | fade frame | inherited (fade) | inherited: fade + 1 | no / no | Plain Frame, **never mouse-enabled** (no `EnableMouse` in CastBars.lua). In free placement it is anchored into the cast-bar holder, but its parent stays the fade frame. |
| Target frame ×5 (`PartyFrameEnhancedTarget_<unit>`) | modules/UnitButtons.lua:33 (via TargetFrames.lua) | fade frame | inherited | inherited: fade + 1 (**same level as the cast bar and pet frame of that unit**) | no / no | SecureUnitButtonTemplate; parent fixed at creation. Mouse on only with *Click to target* (UnitButtons.lua:84-93). |
| Pet frame ×5 (`PartyFrameEnhancedPet_<unit>`) | modules/UnitButtons.lua:33 (via PetFrames.lua) | fade frame | inherited | inherited: fade + 1 (same as above) | no / no | Default attach: right of the party frame, 20 px under the target frame (`defaults/Profile.lua:112-114` vs target height 20, :79-81). Exactly abutting, so they overlap once a border is shown. |
| Element background texture | modules/Element.lua:29 | element root (region) | — | root level, layer BACKGROUND | — | `SetAllPoints(bar)` (:94-96). |
| Element status bar | modules/Element.lua:27 | element root | inherited | inherited: root + 1 | — | |
| Element name text / right text (`text`, `text2`) | modules/Element.lua:30, :33 | status bar (regions) | — | **bar level (root + 1)**, layer OVERLAY | — | **Below the border frame** (a child of the bar). Inset 3 px from the bar's ends (:157-159). |
| Element border | modules/Element.lua:36 | status bar | inherited | inherited: root + 2 | — | BackdropTemplate, **hidden** while *Show border* is off (:125-127; default off on all three, Profile.lua:59/93/121). Anchored to the root, so it extends `size/2` outside the whole element (icon included) and draws its `size`-wide edge inward, i.e. `size/2` inside it (:129-135); default size 8. |
| Cast bar spell icon | modules/Element.lua:38 | element root (region) | — | root level, ARTWORK | — | Below the bar and border, which is correct (the border frames it). |
| Cast bar spark | modules/Element.lua:42 | status bar (region) | — | bar level, OVERLAY, ADD blend | — | 2× bar height, rides the fill edge (:107-108), so it crosses the border's top and bottom edges. **Below the border.** |
| Cast bar shield | modules/Element.lua:47 | status bar (region) | — | bar level, OVERLAY | — | 1.6× bar height, centred on the bar's left edge (:112-113), so it crosses the border's top and bottom edges. With the icon on the left that edge is the icon/bar seam, inside the border's side edge. **Below the border.** |
| Raid-marker layer (target/pet) | modules/Element.lua:54-55 | status bar | inherited | **explicit, absolute**: `border:GetFrameLevel() + 1` (= root + 3), written once at build | — | The one deliberate intra-element level. It exists because the marker as a bar region sat behind the border (comment :51-53). |
| Raid-marker texture | modules/Element.lua:58 | marker layer (region) | — | marker layer, OVERLAY | — | |
| Free-placement holder ×3 (`PartyFrameEnhanced_<castbar|target|pet>_Holder`) | modules/Anchor.lua:265 | UIParent | **inherited: UIParent = MEDIUM** (never set) | inherited (UIParent + 1) | no / **clamped** (:293) | Sized to the whole stack (Anchor.lua:193), so it sits exactly **over** its elements' rect. Mouse-enabled while unlocked in free placement (:323-325). Secure elements anchor to it, so its writes go through RunSecure (:319-325). |
| Holder plate | modules/Anchor.lua:269-272 | holder (region) | — | holder, BACKGROUND, colour 0/0.6/1 at 0.25 | — | Shown while unlocked + free. The comment describes it as showing *between* the elements (:277-281). |
| Holder caption | modules/Anchor.lua:273-276 | holder (region) | — | holder, OVERLAY | — | Above the stack (BOTTOM to holder TOP + 2). |
| Holder grip (drag handle) | modules/Anchor.lua:284-289 | holder | inherited MEDIUM | inherited: holder + 1 | — | Sized to the caption ± 4 px, so it reaches 2 px into the stack's top edge; otherwise outside the stack's rect. |
| Stand-in party frame (`PartyFrameEnhancedStandIn`) | modules/StandIn.lua:152 | UIParent | **explicit LOW**, re-set on every `Place` (:229); MEDIUM between build and the first Place | inherited (default) | no / **clamped** (:156) | Preview only, out of a party. Pushed into the provider map as party1's frame (Preview.lua:69-70), so the elements restack against it (on LOW). Mouse-enabled, draggable. |
| Stand-in health / power bars | modules/StandIn.lua:145, :166-167 | stand-in | inherited LOW | inherited: stand-in + 1 | — | |
| Stand-in bg / portrait / name | modules/StandIn.lua:163, :165, :168 | stand-in / health bar (regions) | — | BACKGROUND / ARTWORK / OVERLAY | — | |
| Secure follow header | modules/SecureFollow.lua:226 | UIParent | inherited MEDIUM | inherited | — | SecureHandlerBaseTemplate; draws nothing. Listed for completeness. |
| Settings pages (LibKa0s canvas panels) | settings/General.lua:238, ElementRows.lua:143, Profiles.lua:26 (`H.CreatePanel`) | Blizzard SettingsPanel | Blizzard's | Blizzard's | — | Library- and Blizzard-owned. The Profiles AceGUI container is re-parented into the page body (Profiles.lua:36-41) and inherits it. |
| Settings combat cover (LibKa0s) | libs/LibKa0s/OptionsCombat.lua:209-215 | the settings canvas | inherited | **explicit**: raised over the page on show (Options.lua:586-592, `lib.__coverLevel`) | — | Library-owned. |
| Debug console window (LibKa0s) | libs/LibKa0s/DebugLog.lua:533-539 | UIParent | **explicit DIALOG** (:536, library) | inherited; its own buttons +1 (:337) | **not toplevel** / clamped | The addon picks nothing. |
| Perf step panel (LibKa0s, `/pfe perf`) | libs/LibKa0s/PerfPanel.lua:183-189 | UIParent | **explicit DIALOG** (:186, library) | inherited | **not toplevel** / clamped | The addon picks nothing. Overlaps the console's default spot only if the player moves one of them. |
| Perf sampler | libs/LibKa0s/PerfSampler.lua:192 | none | — | — | — | Invisible OnUpdate frame. |
| Minimap button | LibDBIcon (via core/LauncherSetup.lua) | Minimap | library default | library default | — | The addon picks nothing. |
| Reset-all confirmation | settings/General.lua:218-233 | StaticPopup | Blizzard DIALOG | Blizzard | — | Blizzard-owned. |

The addon creates no tooltips (no `GameTooltip:SetOwner` anywhere in `core/`, `modules/` or `settings/`), no glows
and no sim strip (it does not use LibKa0s-Sim). No frame in the addon calls `SetToplevel`.

## Problems

| id | file:line | problem |
|---|---|---|
| PAR-S01 | modules/Anchor.lua:265, :193, :325 | **The drag holder sits above the elements it is a handle for.** The holder never sets a strata, so it takes UIParent's MEDIUM. The elements take the party frame's strata through their fade frame, which is **LOW** whenever the frames they stack against are LOW. That is certain in the out-of-party preview, the very session in which a player places a free stack, because the stand-in is explicitly LOW (StandIn.lua:229) and is pushed in as the party's frame. It is also the case for Blizzard's frames per the addon's own comments (RangeFade.lua:39-42, StandIn.lua:226), which this review did not verify in game. The holder is sized to the whole stack, so while unlocked in free placement: (a) the 25 % blue plate is drawn **over** the bars, not between them as Anchor.lua:277-281 describes; (b) the holder is mouse-enabled and covers the bars, so the target and pet frames' drag forwarding (:326-339) is unreachable and **click-to-target on them is swallowed while unlocked**, contradicting the comment at :330-331 ("the click stays the element's own"). Which one wins **changes with `general.strata`**: on High or Dialog the elements sit above the holder again. One element class, two stacking orders depending on a setting. |
| PAR-S02 | modules/Element.lua:30, :33, :42, :47 vs :36 | **Overlays below the border.** The name and time texts, the spark and the shield are regions of the status bar, so they draw under the border frame (a child of the bar). With *Show border* on (off by default) at the default 8 px thickness, the border's edge reaches 4 px inside the element: it overlaps the outer 1 px of the texts (inset 3 px), and cuts across the spark (2× bar height) and the shield (1.6× bar height) where they cross the top and bottom edges. This is the same defect the raid marker was given its own layer to fix (:51-53). The fix was applied to one overlay out of five. |
| PAR-S03 | modules/Element.lua:54-55 | **A hardcoded absolute level that is written once.** `layer:SetFrameLevel(border:GetFrameLevel() + 1)` runs at build time. Every later `restack` moves the fade frame (and so the border) to a new level. Whether the explicitly levelled child is shifted with its parent is client behaviour this code relies on without re-asserting it. The rest of the element relies only on inheritance. Note that `Element.Reskin`'s structural half is memoized on config fields (:163-176, :192) and does **not** run on a restack, so it is not a place where a re-assert would help. Unverified in game; flagged as a risk, not a confirmed bug. |
| PAR-S04 | modules/CastBars.lua:371, modules/UnitButtons.lua:33 | **Sibling elements share one level.** A unit's cast bar, target frame and pet frame are all `fade + 1`. Which draws on top where they overlap is left to the client's sibling order. The default layout abuts the target and pet frames exactly, so any border, or a player's nudge, makes them overlap with no defined winner. |
| PAR-S05 | modules/RangeFade.lua:253-261 | **The level under a fixed strata is borrowed from a frame on another strata.** With `general.strata` = Background/Low/Medium/High/Dialog, the fade frame still takes `topLevel(partyFrame) + 1`, a level measured on the party frame's own strata. Harmless today (the units do not overlap except inside a free stack), and correct in the one case that matters: when the fixed strata **is** the party frames' strata, the walk is what keeps an attached cast bar above the party frame's own children. See Considered and rejected. |
| PAR-S06 | modules/RangeFade.lua:61-63; libs/LibKa0s/DebugLog.lua:536, PerfPanel.lua:186 | **The player can put the HUD into the addon's own window strata.** `general.strata = dialog` puts every element on DIALOG, the strata of the addon's debug console and perf panel. Neither is toplevel, so a bar can draw over the console that is meant to diagnose it, depending on levels. StaticPopups (DIALOG) and possibly Blizzard's Settings panel may be covered too (its strata not checked here). The option is a setting (not changed here); the collision is a strata-map gap. |
| PAR-S07 | modules/StandIn.lua:229 | **The stand-in's strata is a literal, set late.** It is LOW "as Blizzard's unit frames are", but the frame system it imitates may not be on LOW (EllesmereUI's buttons are whatever EllesmereUI sets). The strata is also set in `Place`, not at build, so the frame exists on MEDIUM until it is first dressed. Today `Place` always runs before `Show()` (Preview.lua:58-69), so this is latent, not live. |
| PAR-S08 | libs/LibKa0s/DebugLog.lua:533-539, PerfPanel.lua:183-189 | **Two DIALOG windows, neither toplevel.** When the console and the perf panel overlap (both are draggable), clicking one does not raise it. The order is fixed by level and creation. This is library-owned and applies to every addon (SimPanel.lua:211 is the same shape). |
| PAR-S09 | modules/RangeFade.lua:351-361 | **Restack triggers do not cover a party frame re-levelling itself.** The fade level is measured when LAYOUT/VISIBILITY/PROFILE/CONFIG fire. A frame system that later raises its own children (new aura buttons, an EllesmereUI rebuild) can end up above the elements until the next trigger. Low impact: forbidden aura buttons are already skipped in the walk. Noted for completeness. |
| PAR-S10 | modules/Anchor.lua:265 (×3) | **Three holders, one default level.** The cast-bar, target and pet holders are siblings on MEDIUM at the same level. Two free stacks dragged over each other have no defined order, and neither do their captions and grips. |
| PAR-S11 | modules/Anchor.lua:326-339; modules/CastBars.lua:371 | **Not a strata defect, but it decides whether Z01 is safe.** The bars' drag forwarding only reaches mouse-enabled elements. Cast bar roots never enable the mouse, and target/pet buttons do only with *Click to target* on. So a cast-bar stack is draggable **only** through its holder (today it works because the holder is on top), and a non-mouse element passes the mouse through to whatever is below it. |

## Proposed strata map

The addon's layering, one tier per element class. *F* is the unit's fade-frame level as computed today
(the party frame's top descendant + 1 on its strata under Automatic; LOW fallback). For a holder, *F* is the lowest
fade level among the units in its stack.

| tier | element class | strata | level band |
|---|---|---|---|
| T0 | Stand-in party frame (preview only) and its bars | the imitated system's strata when readable, else LOW; set at **build** | default (its bars + 1) |
| T1 | Fade frame (per unit): the stacking root for everything below | auto: the party frame's; fixed: `general.strata` | F (today's walk, unchanged) |
| T2 | Free-placement holder + plate (the drag surface behind a stack) | **the same strata as the fade frames it holds** | F (the fade frame draws nothing, so sharing its level puts the plate under every element and never ties with the party frame's own top level F − 1) |
| T3 | Pet frame (root, bar, border, overlay) | inherited from T1 | F + 1 … F + 4 |
| T4 | Target frame | inherited | F + 5 … F + 8 |
| T5 | Cast bar | inherited | F + 9 … F + 12 (the most transient and the one drawn over the party frame) |
| — inside every element | root (bg, icon) → bar (fill) → border → **overlay** (text, text2, spark, shield, marker) | inherited | root + 0, + 1, + 2, + 3: one fixed internal band of 4 |
| T6 | Holder caption + grip (unlocked only) | the holder's strata | above the stack's band where the grip overlaps it (2 px); otherwise outside the stack's rect |
| T7 | Debug console, perf panel (library) | DIALOG, **toplevel** | library-owned |
| T8 | Blizzard StaticPopup, Settings panel, menus, GameTooltip | Blizzard (DIALOG / FULLSCREEN_DIALOG / TOOLTIP) | — |

Rule in one line: **the HUD never leaves the party frame's strata unless the player picks a fixed one; the addon's
own drag surfaces follow the HUD's strata, at the HUD's root level and so under every element; the addon's windows
sit above every strata the HUD can be set to except DIALOG.** (S06 remains a deliberate player choice.)

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| PAR-Z01 | modules/Anchor.lua:265 + RangeFade.lua:264-280: the holder no longer inherits MEDIUM. `restack` also sets each feature's holder to the fade frames' strata at level **F** (the lowest fade level among the units in that stack), from → MEDIUM / UIParent + 1. It runs inside the existing `RunSecure("fade:strata")` callback, because secure elements are anchored to the holder (Anchor.lua:319-321). Needs a small `Anchor` accessor for the holders, since RangeFade loads after Anchor and must not reach into its locals. Re-run when the stack's units change (the LAYOUT trigger already covers it). | Fixes S01: the plate draws behind the bars as designed, click-to-target works while unlocked, and the order no longer depends on `general.strata`. Safe for dragging (S11): non-mouse elements pass the mouse through to the holder below, and mouse-enabled target/pet buttons keep forwarding their drag. Level F rather than F − 1 (the original proposal) so the plate never ties with the party frame's top descendant when a stack is dragged over a party frame. | 75% |
| PAR-Z02 | modules/Anchor.lua:284: holder.grip `SetFrameLevel(holder level + 13)`, re-asserted wherever Z01 re-levels the holder. | Once Z01 drops the holder under the stack, the grip (holder + 1) would tie with the pet band and sit under target/cast-bar bands in its 2 px overlap with the top element. Low value: the grip is otherwise outside the stack's rect. | 45% |
| PAR-Z03 | modules/Element.lua:30, :33, :42, :47, :54-58: replace `markerLayer` with one **overlay** frame per element (`SetAllPoints(bar)`), above the border. Create `text`, `text2`, `spark`, `shield` and `marker` on it, from → `bar:CreateFontString/CreateTexture` → `overlay:...`. | Fixes S02: every overlay draws above the border, one rule instead of one special case. A visible change only with *Show border* on. | 70% |
| PAR-Z04 | modules/Element.lua:36, :54-55, :123-137: get the overlay above the border **by inheritance, not by an explicit level**. Make the overlay a child of the border frame and stop hiding the border when *Show border* is off; clear its backdrop instead (`ClearBackdrop`/`SetBackdrop(nil)`), so the overlay is always shown. If an explicit level is kept instead, re-assert it from `RangeFade.restack` (the only code that runs when the fade frame moves), not from `Reskin`, whose structural half is memoized and does not run on a restack (the original proposal's location). | Removes S03's dependence on how the client re-levels an explicitly levelled child. The original Z04 would not have fixed it. | 50% |
| PAR-Z05 | modules/CastBars.lua:371, UnitButtons.lua:33-37: give each feature a fixed relative level band: pet `F + 1`, target `F + 5`, cast bar `F + 9` (`el:SetFrameLevel(fade:GetFrameLevel() + band)`). Set out of combat at creation (each feature's OnEnable runs after RangeFade's, so the fade level exists), and re-applied in `restack`'s changed branch through the existing secure key, since target and pet frames are protected. | Fixes S04 with a defined winner where elements overlap. Target over pet matches their default stacking (the pet column hangs under the target); the cast bar on top because it lies over the party frame. Lowered from 55%: the overlap it orders is a border's width in the default layout, and it adds three more explicit levels whose re-level behaviour (S03) is unverified. Needs an in-game check that each element's internal band moves with its root. | 45% |
| PAR-Z07 | modules/StandIn.lua:152/:229: set the strata in `build()` (from → only in `Place`) and in `Place` copy the imitated source frame's strata when it is readable, through the file's existing guarded `read()`/`plain()` helpers (:44-55), falling back to LOW (from → literal "LOW" every time). | Fixes S07: the stand-in is on the same strata as the frames it stands in for, so the elements stack against it exactly as they will in a party. | 50% |
| PAR-Z09 | settings/General.lua:174 (tooltip only; no value change): append to *Frame strata*'s tooltip "Dialog can cover this addon's debug console and perf panel." | Documents S06 without changing the setting's range (020 forbids that, and 030 does not need it). Coordinate with the layout report's General page changes; this is the only tooltip 030 adds. | 50% |
| PAR-Z10 | Upstream (LibKa0s, not this repo): DebugLog.lua:533 and PerfPanel.lua:183 (and SimPanel.lua:211) `SetToplevel(true)`. | S08. Library-owned, so every addon gets it with one revendor. | 70% |

S09 has no change: re-measuring on every party-frame event costs more than the rare case is worth. The existing
triggers stay. S11 needs no change of its own; it is recorded because Z01 depends on it.

**Interaction check** (item 5, for every change above):
- Dropdowns and menus: the settings panel's LSM and LibKa0s menus open on FULLSCREEN_DIALOG (`libs/LibKa0s/Widgets.lua:225`) and Blizzard's Menu system above that; no change here moves anything above DIALOG, so nothing opens under an addon frame.
- Tooltips: the addon has none of its own; GameTooltip is TOOLTIP strata and unaffected.
- Settings panel and StaticPopups: unchanged; only S06 (a player-chosen Dialog strata) can reach them, and Z09 documents it.
- Blizzard and EllesmereUI party frames: Z01/Z05 stay on the party frame's strata and at or above F, so attached elements still clear the party frame's children; Z07 moves the stand-in onto the imitated strata, which is what the elements already measure against.
- Combat-protected frames: every level or strata write that touches a secure element or a frame secure elements are anchored to (holders, fade frames, target/pet buttons) goes through `NS.RunSecure`, which defers to PLAYER_REGEN_ENABLED. Z03/Z04 touch only regions and plain child frames of the bar, which are content, not protected writes.
- Mouse: Z01 is the only change that moves a mouse-enabled frame, and S11 shows dragging and clicking survive it.

## Considered and rejected

| idea | why rejected | confidence |
|---|---|---|
| Original PAR-Z06: under a fixed strata, use a constant base level (e.g. 10) for every unit instead of `topLevel(partyFrame) + 1`. | Regression risk: when the player picks the strata the party frames are already on (e.g. *Low* with Blizzard frames), a constant 10 can sit **under** the party frame's own children, and the default cast bar lies over the party frame (Profile.lua:38-45). A conditional variant (walk when the fixed strata equals the party frame's, constant otherwise) would be correct but fixes nothing a player can see (S05). | 35% |
| Original PAR-Z08: give the three holders distinct level offsets (+0/+20/+40). | Contradicts Z01: with holders at F, a holder at F + 20 or F + 40 would sit **above** every element band (F + 1 … F + 12), putting the target and pet plates back over their own bars, which is S01 again. If two stacks must be ordered, order them by giving later holders the same band offsets as their features (T3-T5), not a wider one. | 20% |

## Notes for the upstream guidance

- **One stacking root per addon unit.** PFE's per-unit fade frame is the pattern worth codifying: one plain frame
  owns the strata and level, and every visual element under it inherits. The addon then sets strata in exactly one
  place. The guidance should say "set strata on a root, never on a leaf".
- **Match the frame you decorate.** An addon that attaches to another UI's frames should copy that frame's strata
  and stack one level above its highest *readable* descendant, skipping forbidden frames and pcall-ing the read
  (RangeFade.lua:214-241). Leaving such elements on UIParent's MEDIUM covers every LOW window on screen. The
  RangeFade header comment (:36-45) records that this was the original bug.
- **Drag surfaces follow the display, under it.** A holder, mover or plate created on UIParent silently takes
  MEDIUM and can end up above or below the display depending on the player's strata choice (S01). Guidance: a
  drag surface MUST take its display's strata explicitly, at the display root's level so it is below every
  element. A handle that must stay grabbable goes above the display, but only over its own caption area. Check
  that the elements above it either pass the mouse through or forward their drag (S11).
- **Overlays get an overlay frame.** Text, sparks, shields and markers on a bar with a border must live on a child
  frame above the border, not as bar regions. A region always draws under every child frame of its parent
  (S02). Codify a fixed internal band per element: root, fill, border, overlay.
- **Prefer inheritance to explicit levels.** Get an internal order from the parent chain where possible (Z04). Where
  an explicit level is needed, it MUST be re-asserted by the code that moves its stacking root (S03), not by a
  memoized restyle.
- **Fixed sibling bands, not ad-hoc +1s.** Give each element class a level band wide enough for its internal
  layers, and give sibling classes non-overlapping bands so overlaps have a defined winner (S04). Drag surfaces sit
  under all the bands, never between them (rejected Z08).
- **Windows are DIALOG and toplevel.** Library windows (console, perf, sim) should be `SetToplevel(true)`. A
  player-selectable HUD strata that includes DIALOG should be documented as able to cover them (S06, S08).
- **Secure children.** Under strata/level changes on a root that parents secure buttons, or on a frame secure
  buttons are anchored to, route the write through the addon's secure queue, as PFE does with
  `NS.RunSecure("fade:strata")`. Level writes on protected frames are refused in combat.

## Review

Independent review against the code at `master` (LibKa0s v1.76.0), 2026-10-24. Every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel` and `SetToplevel` under `core/`, `modules/` and `settings/` was re-grepped
and checked.

- **Inventory.** All rows confirmed. Corrected: the settings combat cover is explicitly raised (Options.lua:586-592),
  not inherited; added the settings canvas pages and the re-parented Profiles container; added that cast bar roots
  are never mouse-enabled and target/pet buttons only with *Click to target*; added that the border is hidden by
  default, anchored to the root (so it frames the icon), and that the shield sits on the icon/bar seam when the
  icon is left; added "no `SetToplevel` anywhere in the addon".
- **Problems.** S01 kept and tightened: it is certain in the out-of-party preview (the stand-in is explicitly LOW),
  and the Blizzard-frames-are-LOW premise is the addon's own comment, not verified in game. S02's overlap
  restated precisely (1 px of the texts; spark and shield where they cross the top and bottom edges). S03 now
  notes that `Reskin` is memoized and never runs on a restack. S05 now notes the walk is load-bearing when the
  fixed strata equals the party frames'. S06 marks the Settings panel's strata as unchecked. Added S11 (drag
  forwarding only reaches mouse-enabled elements), which is what makes Z01 safe.
- **Changes.** Z01: holder level F instead of F − 1 (avoids a tie with the party frame's top descendant), plus the
  accessor it needs. Z04 rewritten: the original location (`Reskin`) would not have fixed S03; now inheritance
  first, `restack` as the fallback. Z05 lowered 55 → 45%. Z02 lowered 65 → 45%, Z03 75 → 70%. Z07 now uses the
  file's guarded readers. Z06 moved to rejected (regression when the fixed strata equals the party frames'). Z08
  moved to rejected (contradicts Z01: it would lift holders above their own elements). Z10 extended to SimPanel.
- **Added.** An interaction check (menus, tooltips, settings panel, party frames, protected frames, mouse) and two
  upstream notes (prefer inheritance; drag surfaces under all bands).
