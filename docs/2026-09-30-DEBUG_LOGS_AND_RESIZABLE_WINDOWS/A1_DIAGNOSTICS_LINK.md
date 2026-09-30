# Addendum A1: a Diagnostics link in every console's title bar (owner, 2026-09-30)

Added after M4. The plan files above stay as written; this addendum and the new `items.tsv` rows carry it.

## The ask

`/<prefix> diagnostics` is a must-have in every addon, so every debug console gets a control in its title
bar, top left beside "Debug On/Off", that runs that addon's diagnostics report. It must not look like a
button: text like the Debug On/Off label, a small gap after it, drawn **orange**. All addons, with the
upstream changes (LibKa0s, WowAddonStandards, wow-addon) it needs. **AuraMaster first**, for the owner to
see in game, before it goes anywhere else.

## Spec (S5)

1. **LibKa0s (DL-LIB-02).** `DebugLog.lua` draws a text control labelled `Diagnostics` (localizable
   through the module's strings, like `COPY` / `CLEAR`), anchored LEFT to the right edge of the Debug
   On/Off label's font string with a small gap (so the gap holds whichever word the toggle shows). Plain
   text, no frame art: orange at rest (`1, 0.5, 0`), brighter under the pointer. A click runs
   `D:RunDiagnostics()` exactly as `/<prefix> diagnostics` does (ungated, lands with logging off). Drawn
   only when the instance has `RunDiagnostics` (DebugLogDiagnostics loaded). The console's minimum width
   (the title-bar arithmetic) includes it. **DebugLog minor 16**, so the newest copy wins when addons with
   minor 15 are loaded beside it. Folded into the still-unreleased **v1.64.0**: CHANGELOG and api docs
   updated, local tag moved to the new release commit (still not pushed). Tests: drawn when diagnostics
   exist and not otherwise, anchored to the label, color, click runs the report, minimum width grows.
2. **AuraMaster preview (DL-AM-03).** Re-vendor the new v1.64.0 into AuraMaster; add the smoke row. Then
   **stop for the owner's look.**
3. After the owner's go-ahead: **DL-STD-02** (debug-logging §1 "What the library guarantees" and §14 name
   the link; version bump), **DL-PLUG-01** (wow-addon, only where it describes the console's title bar or
   the diagnostics surface), and **DL-<XX>-03** for the other ten addons (re-vendor, smoke row).
