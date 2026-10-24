# Execution record

(Written during execution: outcomes per milestone, deviations, local-tag moves, review fix rounds.)

## M1 — Upstream (2026-10-24)

- Run `wf_eb43309a-9a5`: all 23 items landed and reviewed. Three reviews asked for a fix, and each fix round
  resolved it: WS-04 (a stray period in debug-logging.md:22), LK-11 (the capture accepted a left or right
  mouse-button chord) and WS-07 (stale major counts in library-stack-§7 and open-evolutions).
- LK-90 found three functions above CCN 15 from LK-10..LK-12 and split them in a third commit (3c2bb20). The
  failing first release bundle is kept as the record.
- The local tag v1.77.0 is at 78240f7 and is not pushed. Checkpoint row in `checkpoints.tsv`.

## M2 — Addons (launched 2026-10-24)

- The owner had recorded no decisions on the preview page (`decisions` export empty). So M2 was split:
  run `wf_9c7197ff-aa6` covers only the RV and KB items (22). The 15 ZS items are held until the owner has had a
  chance to reject strata changes, and are then launched from a fresh `accepted.json`.
- Installed dev-copilot is 2.4.0. Both re-vendor commands are unchanged on dev-copilot master since 2.4.0
  (`git log 8c562da..master -- commands/wow-revendor-*.md` is empty), so the installed procedures were used.
- Run `wf_9c7197ff-aa6` finished: 22 of 22 landed and reviewed, none blocked, no library gap. The reviews of BL-KB,
  LH-KB and WG-KB each asked for a fix (a wrong test citation in a comment, stale tab counts, a stale TOC annotation),
  and each fix round landed it.
- RV deviation, every addon: the item's VERIFY `grep 2.88.0 *.toc README.md CLAUDE.md` finds nothing. The installed
  wow-revendor-standards procedure writes no standard version into a repo file, so this was intended. The reading
  version is recorded in each addon's `docs/revendor/2026-10-24-v1.77.0/05_SUMMARY.md`.
- RV: each addon's Options degradation stub gained the four new no-op members (`KeybindingsTab`, `KeybindRows`,
  `KEYBINDS_UNCHANGED`, `StrataTooltip`), as kit 42's surface-parity case requires.

## Owner decisions (2026-10-24)

- The owner accepted all six calls on the preview page (CALL-01..CALL-06) and said: "in general, go ahead with all
  changes you are confident about". `accepted.json` (1ddc875) applies the page defaults to everything else: 438
  changes land. Read as the M3 go-ahead too, at the same >= 50 bar.
- ZS (strata) launched as run `wf_bf619483-f06`. M3 design launched as run `wf_0f27c45a-4b1`.
- Issues filed for the ideas the review moved out of item 020 (XC-34) and for CALL-05 (U-13):
  QuickComms#10 (QUI-L16), QuickComms#11 (QUI-L30), PartyFrameEnhanced#16 (PAR-L17), PrettyChat#19..#22
  (PRC-L02, L06, L11, L12), WowAddonStandards#13 (U-13). All `state:untriaged`, `severity:low`.

## M2 — strata (ZS)

- Run `wf_bf619483-f06`: 15 of 15 landed and reviewed, no library gap. PC-ZS's review asked for two doc fixes,
  and its fix round made them.
- **Lead fix, WG-ZS (f664624).** The implementer took WHA-Z01 beyond the accepted text. It made the popup body
  ignore the mouse permanently, so a click on the visible popup fell through. The accepted text disables the body
  only if an in-game probe allows it, and otherwise records the residual. f664624 restores `f:EnableMouse(true)`
  and records the soft-hide residual in the ARCHITECTURE register. POPUP-10 is now the owner's in-game probe.
- Accepted deviations, recorded in each commit body:
  - KickCD and PrettyChat name the table `NS.Const.LAYERS`, their existing constants module.
  - AbsorbTracker, ConsumableMaster and AuraMaster use the standard's level bands where the analysis drafted
    other numbers.
  - DropWatcher sets the Offer panel's strata at build, not in `dock()`.
  - Unaccepted ids were left out, as specified (for example LOO-Z07, PAR-Z02, PAR-Z05, QUI-Z08).

## M3 — settings layout (020), planned

- Design run `wf_0f27c45a-4b1`: 9 agents. The adversarial review raised 11 issues; all were resolved in the fix
  round.
- U-14 was dropped from the library: every accepted change it would have served can be built on the existing
  surface, and LK-95 files an issue for it.
- 4 layout ids were vetoed for conflicts: AUR-L01, CON-L02, DPS-L14 (CALL-03 labels) and KIC-L29 (XC-33 is
  all-or-none). That leaves 326 to make.
- addendum-01: 45 items (7b60430).
