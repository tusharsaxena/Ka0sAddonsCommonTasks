# Owner scope — 2026-10-24 keybindings, settings layout and frame strata

## The brief (verbatim)

> 015 Add Keybinding for all addons with a window - should do the /xx toggle action (already done) Changes below:
> - Proper names and categories for all in settings > keybindings menu - use the actual addon name for the category and a logical name for the keybinding
> - Keybindings in Addon > General > Keybindings tab (follows global or character specific from keybindings menu - should sync across both)
>
> 020 Relook into the grouping and layout and semantics of all settings menus for all addons
> - Do a deep analysis and tell me what can be changed to make it more logical and user friendly, and avoid a lot of page/tab switching
> - Do not change any settings, just change the layout.
> - Be extremeley throroughy and nitpicky in your analysis.
> - Giv me a preview of what you will change for every addon, along with a reason why, and confidence score of that change
>
> 030 Frame strata analysis - clear separation of strata and z-order across all visual elements of a single addon
> - Needs consistency within a single addon
> - Do this for all addons indvidually
> - Add this as an upstream guidance in WowAddonStandards, etc

## Execution guidelines (verbatim)

> - If you have any questions, ask me upfront
> - After that, use your best judgement and take any decisions you feel you can take. Ask me only when absolutely necessary.
> - Create a resumable and checkpointed plan for this change.
> - Work in a branch and commit incrementally.
> - Push to origin after major milestones, but do not merge without my go-ahead.
> - At the end of the run, after everything is merged, delete all branches, stashes and worktrees created as part of this run
> - Use ultracode to spawn dynamic workflows.

## Upfront answers (2026-10-24)

1. **Keybinding category:** each addon gets its **own top-level category** in Settings > Keybindings, named after
   the addon (e.g. "Ka0s Bank Ledger"), not a header under "AddOns".
2. **Keybinding scope:** only the **7 addons with a window** (the roster's *Show window* column: BankLedger,
   DpsRace, DropWatcher, LootHistory, MultiMeters, QuickComms, WhatGroup). Their existing extra bindings
   (DpsRace results/arm, QuickComms dials) stay and get the same treatment.
3. **Layout latitude (020):** move, regroup and relabel. Rows may move between sections, tabs and pages; tabs
   and pages may merge or split; section headers, labels and tooltips may be reworded. Setting keys, defaults,
   ranges, behaviour and the set of settings stay untouched.

## Lead's calls (not owner decisions)

- 020 is gated: the per-addon preview (change, reason, confidence) goes to the owner before any layout code
  changes. 015 and 030 proceed without that gate.
- 030's strata changes are made in each addon and the guidance lands as a WowAddonStandards rule. A LibKa0s
  helper is added only if the analysis shows the addons need a shared surface.
- No addon version bumps, no tags beyond the LibKa0s local release tag, which is pushed only at finalize.
