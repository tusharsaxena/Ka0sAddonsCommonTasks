# Smoke tests — owner-run, in client

Status is **pending** until the owner reports. Never mark one passed on the owner's behalf.

| Id | Check | Status |
|---|---|---|
| SM-LK-01a | with any re-vendored addon, start a reset (Reset all settings confirmation up), then open the debug console (/<slash> debug or the Test button): the confirmation stays on top and stays clickable | pass (owner, 2026-10-24) |
| SM-LK-01b | open the debug console and then the Settings window, click the console: it comes in front of the Settings window; click the Settings window: it comes back in front | pass (owner, 2026-10-24) |
| SM-LK-01c | /dump on the console frame: GetFrameStrata() is DIALOG and IsToplevel() is true; the console's Copy window still opens above the console | pass (owner, 2026-10-24) |
| SM-LK-02 | covered per addon by the ZS items (AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, QuickComms): unlocked, the drag strip and its ? and X marks draw over the content and stay fully visible while the display is faded | pass (owner, 2026-10-24) |
| SM-LK-03 | in BankLedger's or LootHistory's browser moved to the bottom edge of the screen, open a LibKa0s dropdown whose menu would run off-screen: the menu stays fully on screen | pass (owner, 2026-10-24) |
| SM-LK-04 | in an addon with an IdList (for example BankLedger, KickCD or AuraMaster), type into the id box until suggestions show, then enter combat (attack a training dummy): the suggestion list closes with the page covered, and after combat nothing reopens by itself | pass (owner, 2026-10-24) |
| SM-LK-12a | in any windowed addon after its KB item, General -> Keybindings: bind a key with Key 1; Options -> Keybindings -> Ka0s <Name> shows the same key; /reload and it is still bound | pass (owner, 2026-10-24) |
| SM-LK-12b | while a slot is listening, press Esc: the capture cancels, the key is unchanged and the Settings window stays open | pass (owner, 2026-10-24) |
| SM-LK-12c | bind a key already used by another action (for example M): the status line names the action that lost its key, as Blizzard's page does | pass (owner, 2026-10-24) |
| SM-LK-12d | turn on Character Specific Keybindings in Options -> Keybindings, return to the tab: the line reads 'Saved for: this character only'; a key bound in the tab is saved to that character's set only | pass (owner, 2026-10-24) |
| SM-LK-12e | start a capture, then enter combat: the capture stops, the page is covered, nothing is bound, no error or taint message appears; after combat the tab works again | pass (owner, 2026-10-24) |
| SM-LK-12f | bind a mouse button (Button4) and the mouse wheel through the tab: both bind and show as Blizzard names them | pass (owner, 2026-10-24) |
| SM-LK-13a | with the addon's Keybindings tab open beside it, change the same action's key in Options -> Keybindings: going back to the tab shows the new key without reopening the settings | pass (owner, 2026-10-24) |
| SM-LK-13b | toggle Character Specific Keybindings with different keys in each set: the tab repaints to the set now in force | pass (owner, 2026-10-24) |
| SM-DC-31 | After dev-copilot 2.6.0 is installed (/plugin update + /reload-plugins), run /dev-copilot:review all in an addon still on its pre-ZS master (for example ../KickCD before its ZS item merges). The 01_FINDINGS.md carries layering findings that cite frame-layering-§N with file:line (KickCD: glow Start without frameLevel, text under the glow), and grades a literal-only finding Low. Owner judges whether the findings are real and not noisy. | pass (owner, 2026-10-24) |
| SM-DC-32 | After dev-copilot 2.6.0 is installed, run /dev-copilot:review all in one windowed addon before its KB item merges (for example ../BankLedger). The findings name the header= attribute and the AddOns-category Bindings.xml shape (launcher-§6) and the missing General > Keybindings tab, and do not flag QuickComms-style runtime override bindings. Owner judges the findings. | pass (owner, 2026-10-24) |
| SM-AT-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-AM-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-BL-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-BL-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-BL-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-BL-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-CM-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-DR-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-DR-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-DR-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-DR-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-DW-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-DW-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-DW-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-DW-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-KC-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-LH-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-LH-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-LH-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-LH-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-MM-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-MM-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-MM-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-MM-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-PM-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-PF-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-PG-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-PC-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-QC-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-QC-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-QC-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-QC-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-WG-KB1 | Options -> Keybindings shows a section titled with the brand, holding this addon's bindings with the new labels; no blank spacer row | pass (owner, 2026-10-24) |
| SM-WG-KB2 | binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes | pass (owner, 2026-10-24) |
| SM-WG-KB3 | the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses | pass (owner, 2026-10-24) |
| SM-WG-ZS | every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts) | pass (owner, 2026-10-24) |
| SM-AT-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-AM-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-BL-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-CM-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-DR-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-DW-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-KC-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-LH-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-MM-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-PM-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-PF-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-PG-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-PC-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-QC-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-WG-LY | every settings page this addon's LY item touched reads as its docs/smoke-tests.md describes; no setting lost, no moved key, no changed default; values survive a /reload | pass (owner, 2026-10-24) |
| SM-WG-POPUP-10 | WhatGroup's in-game probe POPUP-10 (docs/smoke-tests.md): during the popup's soft hide, clicks on the visible body behave as recorded; the residual in ARCHITECTURE stands or the body may go mouse-dead | pass (owner, 2026-10-24) |
| SM-LK-30a | in any framed addon after its RV2, General > Master controls: the second line reads Master scale / Master opacity, and moving the slider still changes the whole display's opacity (no setting reset) | pass (owner, 2026-10-24) |
| SM-LK-30b | in PrettyChat or PremadeGroupsFilterExtension (frameless) after its RV2: Debug console and Minimap button sit on one line, and both still work | pass (owner, 2026-10-24) |
| SM-LK-30c | in an addon whose LY item passes lockIsPreview: hover Lock frame and read the preview sentence; in an addon whose LY item passes notes, hover the noted row and read the canonical tooltip followed by the addon's sentence | pass (owner, 2026-10-24) |
| SM-LK-31a | in AbsorbTracker after its LY item: hover Bar opacity; the tooltip is the addon's wording, the label is still Bar opacity, and color swatches still end with the class-color sentence | pass (owner, 2026-10-24) |
| SM-LK-32a | in a windowed addon after its LY item, hover the General page's header Defaults: the text equals Reset all settings' tooltip followed by 'Key bindings are not changed.' | pass (owner, 2026-10-24) |
| SM-LK-40a | in a windowed addon, General > Keybindings shows one key button and Clear per action; bind a key: Options -> Keybindings shows it in the first column; bind a second key on Options -> Keybindings: the tab's button reads '<key> +1' and its tooltip names both keys; Clear on the tab removes both | pass (owner, 2026-10-24) |
| SM-BL-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-DR-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-DW-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-LH-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-MM-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-QC-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-WG-RV3 | General > Keybindings shows one key button and Clear per action, and a key bound there still toggles the window | pass (owner, 2026-10-24) |
| SM-AM-OC1 | AuraMaster: the three confirm buttons read Delete container…, Delete this category…, Forget unreadable categories…, and the … draws as an ellipsis, not a box (addon check SETLAYOUT-9) | pass (owner, 2026-10-24) |
| SM-AT-OC2 | AbsorbTracker General unit band: switching Player / Target / Focus never moves the strip below; the four controls sit on one row; Enable this unit and Copy from Player are not truncated (addon check LOOK-19) | pass (owner, 2026-10-24) |
