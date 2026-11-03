# Library preview contract survey (read-only, wf_b50a295f-81f)

I changed nothing; this was read-only. Paths are relative to `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s` (branch `feat/2026-11-01-full-skinning`, `PICKER_MINOR = 10`) unless an addon is named.

## 1. The preview contract today

**It is a one-shot callback.** The eye button exists only when `spec.onPreview` is a function. `applySpec` shows or hides it on every show (OptionsSkinPicker.lua:1202), and the dropdown's right edge is anchored to whichever icon is visible (:1061-1066). It is built at :1072 with `iconButton(f, "eye", PREVIEW_GLYPH, PREVIEW_TIP, preview)`. `iconButton` (:938-964) is a plain Button: its OnClick runs `dropFocus(P)` and then the handler. It has no checked or highlighted state, and its tooltip is the fixed string `PREVIEW_TIP = "Preview: open test mode"` (:190).

**The handler** is `preview()` at :927-934. It runs `safeCall(p.spec.onPreview)` and then `f:Raise()` if the frame is shown. The library never asks whether the mode is on, never turns it off, and remembers nothing.

**Show** is `show(owner, spec, Skin)` at :1222-1256. A showing counts as fresh when `not (P and P.owner == owner and P.shown)` (:1223). Only a fresh showing runs `opening(P)` (:1208-1220), which records the skin, media, outline and scope it opened with, and `place(f)`. After that come `f:Show()` and `RaiseStaticPopups()` (:1243-1244), then `queue().current = { owner, inst, frame, settle, rebase }` (:1247-1254). `onPreview` is never called at show time.

**Close routes.** All of them end in `closed(p)` (:854-864). It returns early unless `p.shown`, then clears `shown`, the OnUpdate, the list and the rows, calls `revert(p)` (:820-832, which puts back the skin, media, outline and scope), calls `safeCall(p.spec.onClose)`, and finally calls `advance()` if `p` is the current queue entry.
- **Apply** (`apply`, :876-880): refused in combat. Otherwise `save()`, the reload popup if one is needed, then `hide()`.
- **Apply to all** (`applyAll`, :892-908): refused in combat. Otherwise `save()`, a copy to every other skin owner, `dismissWaiting()`, then `hide()`. `dismissWaiting` (:339-344) runs `onClose` for queued pickers that were never shown.
- **Gear** (`openSettings`, :913-925): refused in combat. Otherwise `save()`, then `spec.onSettings` or `OpenOptionsPanel` + `SelectTab`, then `hide()`. If the panel refuses to open, it returns with the window still up (:921).
- **Close control** (`core.MakeCloseButton(f, hide, owner)`, :1118-1123): calls `hide()` (:867-872), which catches `P` before `Hide()` and then calls `closed(p)`.
- **Escape**: the frame name goes into `UISpecialFrames` (:1188), and the OnHide hook (:1163-1165) calls `closed(mine)` only when `not self:IsShown()`. Hiding UIParent (Alt-Z) is therefore not treated as a close.
- **`O.HideSkinPicker`** (:1329-1332): `dropWaiting(O)` (no `onClose` for queued owners), then `hide()`. Hosts call this on stand-down and on a profile change, with their own `quietClose` flag set (DropWatcher/core/SkinSetup.lua:540-548).
- The close control and Escape still work in combat (header :48-49).

**The queue** is `lib.__pickerQueue` (:268-277), shared by every addon. A call for another owner while one is up, or while the queue is parked, is queued (:1283-1288). `advance()` (:328-336) clears `current`, parks on `lib.__parkRegistration` (OptionsRegistry.lua:83) when the client is in combat lockdown, and otherwise shows the next owner. `advance()` runs inside `closed()` after `onClose`, so the next owner's picker shows inside the previous one's close. The picker state `P` is per owner (`pickers[owner]`, :1224-1225), and a close always acts on the picker record it was given, never on the shared variable `P` (:850-853).

**First-run picker and SkinNotice.** `O.SkinNotice(spec, store, recordOnly)` (:1311-1325) and `O.SkinVerb(spec)` (:1340-1368) both end up in `O.SkinPicker(spec)` (:1280-1292). They use the same `show()` and the same close path, so one hook in `show()` and `closed()` covers all of them. `SkinVerb` refuses in combat. `SkinPicker` itself does not refuse; only the queue waits out combat.

**Layering.** The window is DIALOG, toplevel and clamped (:1150-1152). It is DIALOG rather than HIGH so that the HIGH main window the eye opens cannot cover it (header :67-79). It is `Raise()`d after `onPreview` (:933). The skin list is FULLSCREEN_DIALOG.

**What hosts do today.** No host turns its mode on when the picker shows, toggles it from the eye, or restores it on close. `onClose` only records `skin.pickerSeen`.
- PartyFrameEnhanced/core/SkinSetup.lua:216-218: `previewSkin` runs `NS.SetByPath("locked", false)`. That is a stored profile write, and nothing writes it back on close, so the frames stay unlocked after the picker closes.
- DropWatcher/core/SkinSetup.lua:503-509: shows the window if test mode is already on, otherwise `NS.SetTestMode(true)`. Test mode stays on after the close.
- AuraMaster/core/SkinSetup.lua:334-338: `P.SetTestMode(true, "skin picker")` unless test mode is already on. Same leak.

## 2. Library mode helpers hosts already share

The library has no test-mode or unlock-mode engine. Each host owns its own. Two shared pieces carry the vocabulary:

- **The Launcher descriptor** (Launcher.lua:208-222, menu table :151-152) has `isLocked`/`toggleLock`, `isTestMode`/`toggleTestMode`, `isSimMode`/`toggleSim` and `isWindowShown`/`toggleWindow`. Every addon already wires these in `core/LauncherSetup.lua`:
  - Test mode plus a window check: DropWatcher (:99-104), DpsRace (:99-104), MultiMeters (:344-349), QuickComms (:64-70), WhatGroup (:189-201), BankLedger (:247-262) and LootHistory (:173-191).
  - Test mode without `isWindowShown`: AuraMaster (:129-134).
  - Lock only (unlocking is the preview): AbsorbTracker (:151-152), KickCD (:153-156), PanelMaster (:214, :234), PartyFrameEnhanced (:84-88) and ConsumableMaster (:194-202).
  - No lock and no test mode: PrettyChat (:198-200).
  - Window only: LibKa0sSkinTester (:66-67).
- **OptionsCompose MasterControls** has `testModePath` (OptionsCompose.lua:888-892, :520) and `lockIsPreview` (:909-913, :935-936). `lockIsPreview` is the flag that already says "this addon's unlocked view is its test mode."
- **Other mode surfaces:** the mode strip in Widgets.lua (around :898-1015, `opts.onEnd` "END_TEST") and Sim.lua's `IsActive`/`Stop`. Neither enters or exits a test mode for the host.

These pairs give the library the per-addon choice of test, unlock or neither without the library holding a list of addons.

## 3. What the library change needs

**(1) Turn the mode on when the picker shows.** In `show()`, on a fresh showing only, right after `opening(P)` (:1235-1239):
- Record what to restore: `P.previewWas = { active = hook.isActive(), shown = hook.isShown and hook.isShown() }`.
- If `isShown` reports the main surface hidden and the mode is off, call `hook.enter("picker")`.
- Then `f:Raise()`, because the mode may open a DIALOG-level window of its own.

A repeat call while the picker is up must not record the state again. Each queued owner records its own state when its picker shows, because the record lives on the per-owner `P`. Hosts with no `isShown` (no primary window, for example a lock-only HUD) should be treated as hidden, so the mode turns on.

**(2) Make the eye a toggle.** Rewrite `preview()` (:929-934): if the mode is on, call `exit("eye")`, otherwise `enter("eye")`; then `Raise()` and a refresh. The eye needs a visible state: a lit or desaturated icon (`btn.icon:SetDesaturated`, `P.Sk.Button` state) and on and off tooltips. New strings would replace the single `PREVIEW_TIP` (:190), for example `PREVIEW_ON_TIP` and `PREVIEW_OFF_TIP`, with test and unlock wording. Visibility at :1202 becomes "a preview hook exists."

**(3) Restore the opening state on every close.** Put the restore in `closed(p)`, the one place every route passes through (:854-864). It goes after `revert(p)` and before `onClose` and `advance()`, so the next queued owner's mode can turn on without overlapping this one. If the mode is on now but was off at open, call `exit("close")`. If it was on at open and the eye turned it off, call `enter("close")`. Window visibility follows the mode's own exit; an optional `hook.restore(was)` lets a host take over the whole restore. Points to handle:
- Use the record `p`, never the shared `P`. The Escape OnHide and `advance()` reentrancy rules at :850-853 apply.
- `dismissWaiting()` (:339-344) and `dropWaiting()` must not restore anything. Those pickers never showed, so they never recorded a state.
- **Combat.** The close control and Escape close in combat, but a host's enter or exit can refuse there (secure frames such as PartyFrameEnhanced's). The proposal: `exit` or `enter` returns `false` when refused, and the library then queues the restore on `lib.__parkRegistration` (OptionsRegistry.lua:83). The alternative is a documented contract that the host defers it itself. In either case the picker never leaves the mode stuck on after combat.
- **Stand-down and profile change** via `O.HideSkinPicker`: pass the route (`"hide"`) so a stood-down host can skip a restore it has already done. `closed()` does not know its route today. A `p.closeRoute` value set by `hide()` callers and by OnHide (`"escape"`) would supply it.
- **Gear:** the restore runs after the settings panel opens (:922-924). That matches "on any close, return to the previous state."
- **Persistence:** several hosts' lock toggles are stored profile writes (`SetByPath("locked", …)` in PartyFrameEnhanced, AbsorbTracker, DpsRace and others). Restoring through the same toggle writes the old value back, which fixes PartyFrameEnhanced's current leak. Session-only test modes are unaffected.

## 4. Proposed hook shape and back-compat

```lua
spec.preview = {
  mode     = "test" | "unlock",   -- tooltip wording; standard picks test when the host has one
  isActive = fn() -> bool,        -- REQUIRED (Launcher's isTestMode, or not isLocked())
  enter    = fn(route) -> false?, -- REQUIRED; false = refused (combat) → library parks the restore
  exit     = fn(route) -> false?, -- REQUIRED
  isShown  = fn() -> bool,        -- optional (Launcher's isWindowShown); absent = treat as hidden
  restore  = fn(was, route),      -- optional override of the default restore logic
}
```

A convenience builder would let hosts reuse what their Launcher descriptor already has, for example `O.PreviewFromLauncher(desc)`. It would map `isTestMode`/`toggleTestMode` (falling back to `isLocked`/`toggleLock`, with `isActive = not isLocked()`) plus `isWindowShown` onto the table.

**Back-compat:**
- A spec with only a plain `onPreview` function keeps today's behaviour exactly: a one-shot eye, then Raise, no turn-on at show, no restore. An addon that has not moved over cannot break.
- If both are present, `spec.preview` wins and `onPreview` is ignored. Document that.
- Mixed vendored copies are safe. LibStub loads the newest minor client-wide, guarded at :162-167, so an addon passing `preview` always gets a copy that understands it, and older addons' `onPreview` keeps working on the new copy.
- This needs `PICKER_MINOR = 11` and a header entry. The change sits on top of minor 10's R5-L4 work, which is still unvendored (:158-160).
- New tests belong next to `tests/test_options_skin_picker_close.lua`, one per close route: Apply, Apply to all, gear, close control, Escape OnHide, HideSkinPicker. Also needed: the toggle back and forth, a queue handover (A's exit before B's enter), queued pickers dismissed with no restore, and a combat refusal parking the restore.

Hosts would each replace `onPreview = previewSkin` in their `core/SkinSetup.lua` with the `preview` table. PartyFrameEnhanced (:216-234), DropWatcher (:503-527) and AuraMaster (:334-355) are the three that matter most now.