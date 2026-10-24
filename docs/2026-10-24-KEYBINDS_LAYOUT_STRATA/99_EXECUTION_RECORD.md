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
