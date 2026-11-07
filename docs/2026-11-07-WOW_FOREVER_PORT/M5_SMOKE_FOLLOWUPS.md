# M5 addendum: smoke follow-ups (owner, 2026-11-07)

After smoke (R1–R5 pass, F1 recorded, F2 waived) the owner asked for four more pieces before the finalize:

1. **WFP-FIX-01, DpsRace:** in sim mode DPS Race shows the **test-mode** strip ("Test mode: sample numbers…"), not the sim strip.
2. **WFP-FIX-02, collection:** the sim-mode strip is named inconsistently, "SIM" in some places and "SIMULATION" in others. Call it **SIM** everywhere. The prose after the label should be consistent across addons: similar, though not identical, and suited to each addon's context.
3. **WFP-LK-06 (reopened), LibKa0s#77:** build the static missing-globals check. Its exceptions.tsv row is withdrawn.
4. **WFP-LK-08, LibKa0s:** peel `OptionsTabs.lua` (header block and sub-strip) to clear the census trigger. It is at 1295 lines, against a trigger of 1300.
5. **WFP-REVIEW:** a full whole-branch review at the end, on the most capable model, before the finalize.

The library changes ship as **LibKa0s v1.93.0** (local tag; WFP-LK-09). Every addon then re-vendors it (WFP-RV2-<abbr>). Any host-owned sim-strip prose is aligned in the same commit.
