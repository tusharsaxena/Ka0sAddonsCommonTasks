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
