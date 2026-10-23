# 99 — Execution record

## M1 (2026-10-23, 14:22–15:20)

- 13/13 items landed and reviewed (`plan-data/m1-results.json`). One fix round: LK-90 (CLAUDE.md 1000–1500 band
  prose), commit 9949368.
- **Local tag move:** v1.76.0 was created by LK-90 at `82d76f6`; the review fix landed after it, outside the
  payload (`git diff v1.76.0 HEAD -- LibKa0s testkit` empty). The lead moved the tag to `9949368` (the branch head).
- Deviations worth knowing:
  - dev-copilot has no CHANGELOG.md; its 2.5.0 history lives in CLAUDE.md "Current version" (DC-00).
  - The standard's current entry lives in STANDARDS.md ## Changelog, and v2.86.0 moved to standards/CHANGELOG.md
    (WS-00).
  - LK-90 landed as two commits (`LK-90 (1/2):`, then `LK-90:`), per releasing.md step 7. Its CONSUMERS rows for
    MM/KC are planned; the census is re-run after M3.
- Pushed: WowAddonStandards a72d35a, LibKa0s 9949368, dev-copilot 6d45079, plus review notes. Tag not pushed.

## Addendum 01 (2026-10-23, during M2)

- **QC-05**, from an owner bug report (`inputs/qc-05-groups-preview.png`). The owner first said DropWatcher, then
  corrected it to QuickComms. In the Groups page's edit preview, the icons look faded and a dark circle sits over
  the dial icons; the preview should look exactly like live mode plus the PREVIEW tag.
- Queued as the last item of M3's QuickComms chain, debug-first. Smoke check SM-QC-8.
- **QC-06**, from an owner bug report (`inputs/qc-06-callout-strata.png`): the preview dial's hub dot and pointer
  draw over the New callout dialog. Probable cause, from reading the code: the dial header and the popup share the
  DIALOG strata, and the hub's front frame sits at header level + 20. Queued after QC-05. Smoke check SM-QC-9.
