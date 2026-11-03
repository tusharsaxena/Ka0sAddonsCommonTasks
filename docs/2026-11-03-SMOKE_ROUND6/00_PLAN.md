# Round 6: the skin picker's preview (2026-11-03)

Inputs: `inputs/OWNER_FEEDBACK.md` (verbatim, images 62, 63 and 66). Survey: run wf_b50a295f-81f (read-only, 17 agents),
summarised below. Same branch as every earlier round, `feat/2026-11-01-full-skinning`. Outfitter is never touched.

## The owner's rule

When the skin picker shows and the addon's main surface is hidden, the addon enters its preview mode: test mode if it
has one, otherwise unlock mode. The eye button toggles that mode. When the picker closes, by any route, the addon goes back
to the state it had when the picker opened. This becomes an upstream standard.

## What the survey found

- In the library, `spec.onPreview` is a one-shot callback (`OptionsSkinPicker.lua:927-934`). The eye has no on/off state.
  Nothing calls the host at show time, and `closed()` (:854-864) restores the skin but not the mode.
- PFE (`locked=false`), DropWatcher, AuraMaster, BankLedger, LootHistory, DpsRace, MultiMeters, QuickComms, WhatGroup and the
  Skin Tester have an eye, and every one of them only enters the mode. None of them toggles it or restores it on close.
- The mode verbs already exist in each addon's Launcher descriptor (`isTestMode`/`toggleTestMode`, `isLocked`/`toggleLock`,
  `isWindowShown`).

## The lead's calls

1. **The contract lives in the library.** `spec.preview = { mode = "test"|"unlock"|"window"|"console", enter(why),
   exit(why), isActive(), isShown() }`.
   - On a fresh show, the picker records `{ active, shown }` on the per-owner record P. If the main surface is hidden and
     the mode is off, it calls `enter("picker")`, then raises the picker. A host with no `isShown` counts as hidden.
   - The eye toggles the mode with `exit("eye")` or `enter("eye")`. It shows a lit or dimmed state, and its tooltip is
     worded per mode, for example "Preview: test mode on/off" or "unlock".
   - `closed(p)`, which every close route passes through (Apply, Apply to all, gear, the close control, Escape,
     HideSkinPicker), runs `exit("picker")` when the mode is on now but was off at open. It also runs `enter` when the mode
     was on at open and the eye turned it off. The restore runs before `onClose` and `advance()`. Alt-Z hiding UIParent is
     not a close.
   - A refused enter, for example in combat, leaves the recorded state alone. The restore only undoes a change that
     actually happened.
   - `spec.onPreview` keeps working, as a one-shot eye with no auto-enter and no restore, for back-compat. Every Ka0s host
     moves to `spec.preview`. The queue, the first-run picker and SkinNotice all go through `show` and `closed`, so they are
     covered.
2. **Per-addon modes**, shown to the owner in chat before the build:

   | Addon | Mode | Calls |
   |---|---|---|
   | AuraMaster | test, `/am test` | Preview.SetTestMode |
   | BankLedger | test, `/bl test` | LedgerTable test mode |
   | DpsRace | test, `/dr test` | state.testMode through SetByPath |
   | DropWatcher | test, `/dw test` | NS.SetTestMode |
   | LootHistory | test, `/lh test` | BrowserTable:SetTestMode |
   | MultiMeters | test, `/mm test` | SetTestMode / IsTest |
   | QuickComms | test, `/qc test` | Preview test mode |
   | WhatGroup | test, `/wg test` | H.Set("state.testMode") |
   | AbsorbTracker | unlock, `/at unlock` | the lock seam |
   | ConsumableMaster | unlock, `/cm unlock` | RunLock / MacroBar.SetLocked |
   | KickCD | unlock, `/kcd unlock` | the lock seam |
   | PanelMaster | unlock, `/pm unlock` | Schema:Set("state.locked"), never NS.Unlock directly |
   | PartyFrameEnhanced | unlock, `/pfe unlock` | SetByPath("locked") |
   | LibKa0sSkinTester | window | the showroom: R.Show, R.Hide, R.IsShown |
   | PrettyChat | console | owner's answer: the debug console filled by `/pc test` sample lines; hidden again on close if the picker opened it |
   | PGFE | none | no window of its own; its panel lives inside PGF's dialog. Documented in the standard as a no-preview addon |

   Every enter and exit goes through the addon's own write seam, so the settings panel, the launcher and the slash command
   stay in step and the addon's combat refusals still apply. "Main surface hidden" means: for test hosts, test mode is off
   and the main window is not shown; for unlock hosts, the frames are locked; for window and console hosts, the window is not
   shown.
3. **Unlock is a stored setting.** A /reload while the picker is up leaves the frames unlocked until `/xx lock`. Each unlock
   host notes this in its smoke step. No new persistence is added.
4. **The standard:** a new rule in the options-ui family (or wherever the skin picker is specified today), with an
   anti-pattern for an enter-only eye, the mode order test > unlock > window, and the documented no-preview list (PGFE).
   Bump the version and update the changelog, index blurb and context pack as that repo requires.
5. **The tag:** v1.85.0 is re-cut locally and not pushed. A picker minor bump follows the R4-L4 reasoning, since Outfitter's
   vendored copy stays put.

## Order

M1: R6-STD and R6-L1 (one agent each, in parallel), then an independent library review, then R6-REL. M2: a 16-addon
pipeline (re-vendor, wire spec.preview, smoke row, then an independent reviewer). M3: R6-GATE writes 06_SMOKE_TESTS.md and
99_REPORT.md and pushes 19 repos (WowAddonStandards included). No tag push, and no merge until the owner gives the go-ahead.
