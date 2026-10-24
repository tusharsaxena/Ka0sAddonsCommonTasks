# WhatGroup — frame strata analysis

Read from `../WhatGroup` on `master` (clean), 2026-10-24: `modules/Frame.lua` (every frame the addon draws),
`core/*.lua`, `settings/*.lua`, `Bindings.xml`, `docs/frame.md`, and the vendored LibKa0s surfaces the addon
drives: `Core.lua` (`ApplySkin`, the grip), `DebugLog.lua` (the console), `Widgets.lua` (the copy window),
`OptionsCombat.lua` / `OptionsTabs.lua`, `Launcher*.lua`, plus `LibDBIcon-1.0` and AceGUI's dropdown. The standard
has **no** strata or frame-level rule today (no match for strata, frame level or toplevel in
`standards/standards/*.md`).

WhatGroup draws one real window, the group info popup `WhatGroupFrame`, plus two invisible helper frames. It has
no HUD, bars, icons, glows, sim strip or perf panel. Everything else on screen is drawn by a library or by
Blizzard.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Group info popup `WhatGroupFrame` | modules/Frame.lua:745 | UIParent | **DIALOG, explicit** (:748) | client-assigned; `Raise()` on every show (:341 combat-guarded, :349) | not toplevel / clamped (:751) | BackdropTemplate, movable, `EnableMouse(true)` on the body (:750) although the drag lives on the title bar (:810-818), so the body's mouse only stops clicks falling through. Parents a **secure** button, so Show, Hide, Raise and SetPoint are refused in combat. In combat it is "soft-hidden" at alpha 0 instead (:312-316). Default anchor CENTER, +25% of UIParent height (:144-147). |
| Inner highlight (skin) | libs/LibKa0s/Core.lua:141, called from Frame.lua:840 | popup | inherited DIALOG | inherited (popup +1) | — | Full-size child BackdropTemplate, 1px edge, no mouse. Created **after** titleBar and before content, so it shares level +1 with every sibling. |
| Popup backdrop + separator | Frame.lua:833 (`sep`, ARTWORK on popup) | popup | inherited | popup's own regions | — | Drawn below every child frame by construction. |
| Title bar (drag handle) | Frame.lua:806 | popup | inherited DIALOG | inherited (+1) | — | 30px, `EnableMouse(true)` (:810), drags unless `locked`. Title FontString OVERLAY (:826). |
| Content frame | Frame.lua:843 | popup | inherited | inherited (+1) | — | No mouse. Holds the 6 label/value FontString pairs (OVERLAY, :849/:856), the Teleport label (:876) and the teleport note (:928). `topAnchor` (:864) is +2, a 1x1 anchor with no visuals. |
| Teleport button (secure) | Frame.lua:893 | popup | inherited | inherited (+1) | — | `SecureActionButtonTemplate`, 24x24, anchored by offset from the popup's TOPLEFT. Mouse is on or off depending on state (:547, :564, :568). Icon ARTWORK (:913). |
| Teleport cooldown swipe | Frame.lua:921 | teleport button | inherited | inherited (+2) | — | `CooldownFrameTemplate`, numbers hidden. |
| Close button | Frame.lua:938 | popup | inherited | inherited (+1) | — | `UIPanelButtonTemplate` 90x24, bottom center. |
| Teleport tooltip | Frame.lua:517-519 | GameTooltip (Blizzard) | TOOLTIP (Blizzard) | Blizzard | — | Spell tooltip, ANCHOR_RIGHT. |
| ESC proxy `WhatGroupFrameEscape` | Frame.lua:730 | UIParent | inherited MEDIUM (UIParent's) | inherited | — | No textures, no mouse, never drawn. Shown only to keep a UISpecialFrames entry alive. Strata does not matter. |
| Binding button `WhatGroupTogglePopup` | Frame.lua:1321 | UIParent | inherited MEDIUM | inherited | — | Hidden, plain, never drawn. Target of `CLICK …:LeftButton` (Bindings.xml:3). |
| Debug console `WhatGroupDebugWindow` (library) | libs/LibKa0s/DebugLog.lua:533-536 | UIParent | **DIALOG, explicit (library)** | client-assigned; no Raise | not toplevel / clamped | 700x344 at CENTER(220,-80). Drag bar (:512-520). Diagnostics button title-level +1 (:337). Resize grip parent +10 (Core.lua:611, `GRIP_LEVEL` :546). |
| Debug copy window (library) | libs/LibKa0s/Widgets.lua:650-653 | UIParent | **FULLSCREEN, explicit (library)** | client | clamped | Above the DIALOG console that opens it, by design (comment :651-652). |
| Minimap button (LibDBIcon) | libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:246-248 | Minimap | **MEDIUM, level 8 (library, absolute)** | absolute 8 | — | Not the addon's choice. |
| Launcher context menu | libs/LibKa0s/Launcher.lua:395 (`MenuUtil.CreateContextMenu`) | Blizzard Menu | Blizzard's menu strata | Blizzard | — | Not the addon's choice. |
| Launcher / row tooltips | GameTooltip | — | TOOLTIP | — | — | — |
| Reset confirmation `WHATGROUP_RESET_ALL` | settings/Schema.lua:658 (StaticPopupDialogs) | Blizzard StaticPopupN | DIALOG (Blizzard template), toplevel | Blizzard | toplevel | Shown from the Settings panel, `/wg resetall` or the header Defaults button. |
| Settings canvases (General, Profiles, landing) | settings/Panel.lua:304, Profiles.lua:51, OptionsSetup.lua:193 | Blizzard SettingsPanel | inherited from SettingsPanel (HIGH in Blizzard_Settings, not verified in-repo) | inherited | SettingsPanel is toplevel | Raw AceGUI inside. Profiles' container is re-parented to `ctx.body` (Profiles.lua:64-69). |
| Combat-lock cover (library) | libs/LibKa0s/OptionsCombat.lua:179-183, Options.lua:589-590 | panel | inherited | **computed**: max(panel+100, deepest descendant+1), capped | — | Relative and measured. The right pattern. |
| Tab strip buttons (library) | libs/LibKa0s/OptionsTabs.lua:712-714, :375-377 | panel body | inherited | relative +1 | — | — |
| General visibility dropdown pullout (AceGUI) | libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua:287 (pullout; its slider, scroll and item frames :309-326; the items' own frames DropDown-Items.lua:75, :162) | UIParent | FULLSCREEN_DIALOG (AceGUI) | AceGUI | — | The Profiles page's AceConfigDialog selects open the same pullout. |

## Problems

| id | where | problem |
|---|---|---|
| WHA-S01 | Frame.lua:312-316, :750, :810; :547/:564 | **An invisible click-catcher at DIALOG in combat.** The combat soft hide sets the popup's alpha to 0 and leaves it shown. The popup itself (`EnableMouse(true)`), its title bar, and possibly the armed secure teleport button stay mouse-live. Until `PLAYER_REGEN_ENABLED`, a 420x280 invisible rectangle above the screen center at DIALOG strata eats clicks meant for whatever is under it: unit frames, boss frames, the world. This is the most serious layering defect in the addon, because the player cannot see what is blocking the click. It is not rare: four paths reach the soft hide: the Close button, ESC, and the toggle key or launcher entry pressed in combat (all through `dismissPopup`, :409-418, `ToggleFrame` :1278-1285), and *General visibility* = *Only out of combat* with the popup up when a pull starts (:216-229, :452-461). The armed teleport button is the worst part, because it is an invisible secure `/cast` target, and its `EnableMouse` is refused in combat on a secure frame, so no combat-time fix can reach it. The Close button (plain child, :938) is also live and invisible, and a click there is harmless (it re-enters `dismissPopup`). |
| WHA-S02 | Frame.lua:748; DebugLog.lua:536 | **The popup and the debug console share DIALOG with no ordering rule.** Neither is toplevel, and the console never raises. Which one is on top is decided by the last `Raise()`, which is always the popup's (:349). At the default anchors with UIParent height about 768, the popup's bottom 40px (including its Close button) overlaps the left part of the console's title bar. Clicking the console does not bring it forward. |
| WHA-S03 | Frame.lua:748 vs SettingsPanel; Frame.lua:816-818 | **The popup sits above the Settings panel it is configured from.** Tick *Test mode* (Master controls) and the DIALOG popup appears over the HIGH Settings panel, near its top center (Frame.lua:146), and stays above it whatever the player clicks. With *Lock frame* on, the drag is refused (:817), so the player cannot move it off the panel without unticking a setting on that same panel. **This is also the behavior the feature needs.** Test mode exists "so you can drag it into place" (Panel.lua:222), and sizing it with Width / Height (layout WHA-L10) only works if the popup stays visible while the player drags a slider on the panel. Moving the popup under or level with the panel would trade a lock-only annoyance for a preview that disappears on the first click (see rejected Z02-alt). The residual is the lock case alone, and it is handled in wording (layout WHA-L17). |
| WHA-S04 | Frame.lua:349; Schema.lua:658 | **The popup and the reset confirmation share DIALOG.** The StaticPopup is toplevel and is raised when shown. But the popup's unconditional `Raise()` on every show, for example when a join fires or `/wg show` runs while the confirmation is up, can put an information window above a pending destructive confirmation. Their default anchors (upper center) overlap. |
| WHA-S05 | Frame.lua:806, :843, :893, :938; Core.lua:141 | **Every child of the popup sits at the same inherited level (+1)**: the inner highlight, title bar, content, the secure button and the close button. Their order is creation order, and that is safe today only because no two of them overlap. The full-size inner highlight frame is a sibling at the same level as the interactive controls, so a future backdrop on `content`, or a moved control, would render in undefined order. |
| WHA-S06 | Frame.lua:748; docs/frame.md:18 | **The strata is a bare literal with no stated reason.** `"DIALOG"` is typed inline, and docs/frame.md:18 records the value but not why. Nothing says the popup is meant to sit above bags and the LFG frame but below confirmations. |
| WHA-S07 | Frame.lua:341, :349 | **Raise is used for ordering, but the window is not toplevel.** `Raise()` runs on show only, and only out of combat. A click on the popup never raises it above a same-strata window that covers it (S02). This needs care, because the popup parents a secure frame: an addon `Raise()` in combat is refused (hence the guard), and whether engine-driven toplevel raising is also refused on such a frame has not been measured. |
| WHA-S08 | DebugLog.lua:533-538 | **(Library)** The debug console is DIALOG and not toplevel, in every addon. Any addon window at DIALOG that overlaps it hits the S02 problem. Recorded here because WhatGroup's popup is one such window. The fix belongs to LibKa0s. |

## Proposed strata map

| tier | strata | level band | WhatGroup elements |
|---|---|---|---|
| T0 never drawn | inherited MEDIUM | inherited | ESC proxy, binding button. No change: no visuals, no mouse. |
| T0 world-attached (not ours) | MEDIUM, LibDBIcon's absolute 8 | library | minimap button |
| T1 windows | HIGH, toplevel | — | none in WhatGroup (the Settings panel is Blizzard's tier-mate here) |
| T2 dialogs and event-raised notices | **DIALOG** | client base; children inherit (+1, creation order; nothing overlaps) | **group info popup** (not toplevel: `Raise()` on explicit show, out of combat), debug console (library; toplevel per the S08 library ask), Blizzard StaticPopups (reset confirmation, toplevel) |
| T3 detached child windows | FULLSCREEN | client base | debug copy window (library) |
| T4 transient popups | FULLSCREEN_DIALOG | client / AceGUI | AceGUI dropdown pullout, Blizzard Menu (launcher context menu) |
| T5 | TOOLTIP | Blizzard | GameTooltip (teleport spell, launcher) |

Rules, matching the tier model in the BankLedger analysis, with one stated exception: the popup is an
event-raised notice that is also previewed from the Settings panel, so it sits at the dialog tier rather than the
window tier (Z02).
- A surface is always at least one tier above the frame that opens it.
- Nothing invisible stays mouse-live (S01).
- No absolute `SetFrameLevel`. Use only parent-relative offsets.
- Every explicit `SetFrameStrata` reads a named constant whose comment states the tier.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| WHA-Z01 | **Make the soft hide mouse-dead.** In `hidePopup`'s combat branch (Frame.lua:312-316), next to `f:SetAlpha(0)`, call `titleBar:EnableMouse(false)` (titleBar is a plain child with no secure descendants, so this is legal in combat). For the popup itself, call `f:EnableMouse(false)` **only if** an in-game probe shows it is not refused on a frame that parents a secure child. Restore both in `showPopup` (:336-353) and in the `PLAYER_REGEN_ENABLED` settle. If `f:EnableMouse` turns out to be refused, record the residual (the background still catches clicks) as a documented deviation, with the bigger fix as its trigger: move the secure button onto a separate secure holder frame so the popup itself is not protected. | Removes the invisible click-catcher (S01). It changes what is clickable in combat, so it needs an in-game check before it lands. The owner smoke-tests it: join a group in combat, close the popup, click unit frames under where it was. **Review addition, a probe-free route for the body:** the popup body needs no mouse at all (the drag is on the title bar, :810-818), so `f:EnableMouse(true)` at :750 can become `false` at build, out of combat, and only the plain children are toggled in combat. That removes the probe and the separate-holder refactor for the body. Its cost is that clicks on the popup's empty body fall through to the world while it is visible, and the owner should accept that explicitly. **Residual in every route:** the armed secure teleport button stays live and invisible, because its `EnableMouse` is refused in combat. Record that as a known limitation, or disarm it on `PLAYER_REGEN_DISABLED`, where secure writes are still allowed (the same edge test mode uses, Frame.lua:1167-1173). Disarming is the better fix but it is a behavior change, so it needs the owner's nod. Also restore the title bar in the soft-show branch of `showPopup` (:337-343), not only in the full show. | 55% |
| WHA-Z02 | **Keep the popup at DIALOG, as a named, reasoned tier** (review rewrite). At Frame.lua:748, `f:SetFrameStrata("DIALOG")` becomes `f:SetFrameStrata(STRATA_POPUP)`, with `local STRATA_POPUP = "DIALOG"` declared next to `anchorDefault` (:144) and a comment: "Dialog tier: an event-raised notice that must surface over the LFG frame, bags and the Settings panel it is previewed from (Test mode, Width/Height). Not toplevel. Dialogs that must beat it (the console, StaticPopups) are toplevel." No `SetToplevel` here. | WhatGroup has one window, so consistency inside the addon (the owner's 030 bar) holds at any tier, and the cross-addon tier argument does not outweigh the feature. The test-mode preview and the size sliders only work while the popup stays above the HIGH, toplevel Settings panel (S03). S02 is fixed by the console becoming toplevel (S08, library), not by moving the popup. S04 is left as it is (see Considered and rejected). | 70% |
| WHA-Z03 | Keep the `Raise()` calls (Frame.lua:341, :349) as they are, combat guard included, and add a comment: they bring the popup to the front of the **DIALOG** tier on an explicit show, and a toplevel dialog (the console, a StaticPopup) comes back on top with a click. | It documents why Raise is safe on a frame with a secure child (it is combat-guarded, S07), and why it is acceptable that Raise can put the popup over a pending confirmation (S04). Comment only. | 75% |
| WHA-Z05 | docs/frame.md:18: `Strata \| DIALOG` → `Strata \| DIALOG (dialog tier, not toplevel) — an event-raised notice above the LFG frame, bags and the Settings panel it is previewed from; toplevel dialogs (debug console, StaticPopups) win a click; children inherit the popup's level`. The Frame.lua:748 comment comes from Z02. | Records the reason, not just the value (S06). | 85% |
| WHA-Z06 | No change to the ESC proxy (Frame.lua:730) or the binding button (:1321). | They inherit MEDIUM, have no visuals and no mouse, and must stay invisible. Setting a strata on them would only add noise. | 90% |

Not proposed here, because they are library-owned (see the next section): making the console toplevel (S08),
and setting the inner highlight's level explicitly.

### Considered and rejected

| change | confidence | why not |
|---|---|---|
| **Z02-alt (the original Z02):** move the popup to HIGH and make it toplevel. | 35% | The Settings panel is HIGH and toplevel, and the popup's default anchor (CENTER, +25% of screen height, Frame.lua:144-147) falls inside the panel. The first click on any panel control, such as a Width slider, would raise the panel over the popup and hide the preview the player is sizing (S03, layout WHA-L10), and it would hide the Test mode preview too. Toplevel on a frame with a secure child has also never been measured in combat (S07). The S02 and S04 gains are better reached through S08 and are small anyway. |
| **Z04 (the original):** pin child levels at build: title bar and content at +2, teleport and close at +3. | 35% | The popup's own level moves on every `Raise()` (Frame.lua:341, :349), so levels taken at build are relative to a number that changes afterward. Nothing overlaps today (S05), so the change buys no visible fix, and a child level that falls behind its parent after a Raise is a new risk. Revisit only if a child ever overlaps another. |
| Skip `Raise()` while a StaticPopup is shown (S04). | 30% | StaticPopups are toplevel, so one click brings the confirmation back. For the two to coincide, a join or `/wg show` has to land while the reset confirmation is open. A new guard is code to keep in step with Blizzard's StaticPopup API for a case that rare. |

## Notes for the upstream guidance

- **A window that parents a secure child cannot be hidden in combat, so "hidden" may mean alpha 0.** The
  guidance should require that any soft-hidden (alpha-0) frame is also **mouse-dead**. Where the frame itself
  cannot be mouse-disabled in combat, keep the secure child on a separate holder so the window is not
  protected. WhatGroup is the collection's worked example (S01).
- **Name the tiers once.** Windows HIGH + toplevel, dialogs DIALOG + toplevel, detached child windows
  FULLSCREEN, menus and pullouts FULLSCREEN_DIALOG, tooltips and drag ghosts TOOLTIP. An addon window that
  is **raised by an event and previewed from the Settings panel** (WhatGroup's popup) MAY sit at DIALOG, as long as
  it is not toplevel and every true dialog at that tier is toplevel (console, StaticPopups), so a click on the
  dialog always wins. The guidance must state this exception. A flat "windows are HIGH" rule would put such a
  preview under the Settings panel on the first click (Z02-alt).
- **`Raise()` is not a layering policy.** Use toplevel for click-to-front, and Raise only on an explicit show,
  always combat-guarded on any frame with secure descendants (S07).
- **Levels are relative:** never absolute (LibDBIcon's fixed level 8 is the library's own choice), and set only
  where siblings actually overlap, with overlays such as a grip at base+10. Bands pinned at build on a frame that
  is `Raise()`d later are relative to a moving base, so the guidance should not demand bands for children that do
  not overlap (Z04 rejected). The library's measured
  combat-cover level (OptionsCombat.lua:179-183) is the model for anything that must sit over unknown children.
- **Preview / test-mode windows open from the Settings panel** must stay visible while the player edits the
  panel, which means above it, and must stay movable. *Lock frame* can block that, so either let test mode imply
  unlocked (§15 already allows "it MAY unlock as a side effect") or say so in the Test mode tooltip
  (layout WHA-L17) (S03).
- **Invisible-but-shown frames and secure buttons.** A soft-hidden window's secure child cannot be mouse-disabled
  in combat. The guidance should say to disarm (clear the action attributes on) a secure child at
  `PLAYER_REGEN_DISABLED` whenever its parent can be soft-hidden during the fight (Z01).
- **Library asks (LibKa0s):** `SetToplevel(true)` on the debug console (DebugLog.lua:536), so every addon's
  console raises on click (S08). Optionally give the `ApplySkin` inner highlight a defined place
  under host content (Core.lua:141). Low value while nothing overlaps it, and a level pinned at build goes stale
  on a later `Raise()`, as Z04's rejection explains. Optionally export a `STRATA` tier table that hosts
  read instead of typing literals.

## Review

Independent review, 2026-10-24, checked against `../WhatGroup` on `master`: every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel`, `SetToplevel`, `Raise`, `EnableMouse` and `SetClampedToScreen` in `core/`,
`modules/` and `settings/` (there are 8 `CreateFrame`s, 1 strata call, 0 level or toplevel calls, and 2 `Raise`s), the
show, hide and combat-gate paths in Frame.lua, and the library sites the inventory cites.

- **Inventory: accurate, with one ref fixed and two notes added.** All 8 addon frames are listed with correct lines.
  The AceGUI pullout's strata is set at `AceGUIWidget-DropDown.lua:287`, not DropDown-Items (those lines are the
  items), and the Profiles page's selects use the same pullout. The popup row now says that the body's
  `EnableMouse` serves no drag (the drag lives on the title bar), which Z01 relies on.
- **S01 widened.** Four paths reach the soft hide (Close, ESC, toggle key or launcher in combat, and *Only out of
  combat* at a pull), so the defect is common. The armed secure teleport button is an invisible live `/cast`
  target that no combat-time `EnableMouse` can reach. Z01 gained a probe-free route (body mouse off at build),
  the `PLAYER_REGEN_DISABLED` disarm option for the teleport button, and the missing soft-show restore point.
  Confidence went from 50% to 55%.
- **Z02 reversed (60% → rejected at 35%), and a new Z02 keeps DIALOG (70%).** The interaction check failed. The
  Settings panel is HIGH and toplevel, and the popup's default anchor falls inside it, so HIGH + toplevel would hide
  the Test mode preview and the Width/Height preview behind the panel on the first click on the panel. The original
  had listed S03 as a problem, but it is the feature working. S02 is fixed by the library making the console
  toplevel (S08), and S04 is rare and self-correcting (StaticPopups are toplevel). The strata map moved the popup
  to the dialog tier with the exception stated, and the layout file's L10 now cites this.
- **Z03 reworded** for the DIALOG tier (80% → 75%). **Z04 rejected (45% → 35%)**: `Raise()` moves the base the bands
  would be pinned to, and nothing overlaps. **Z05** is rewritten to match the new Z02.
- **Upstream notes** now carry the event-raised-notice exception, relative levels without mandatory bands, the
  Test mode vs Lock frame point, and the secure-child disarm rule. None of the remaining changes affects dropdowns
  (FULLSCREEN_DIALOG), tooltips (TOOLTIP), StaticPopups, the Settings panel's combat cover or the secure button's
  combat rules.
