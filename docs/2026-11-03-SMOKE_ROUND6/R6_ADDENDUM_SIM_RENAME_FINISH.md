# Addendum: sim checkbox, rename, and finish (owner, 2026-11-04, during the run)

Owner's words, verbatim:

> Few more small changes:
> - Add a sim checkbox in settings (next to test) for all Ka0s addons that support it. make this an upstream standard.
> - Rename addons everywhere to drop the Ka0s (TOC, README, Addon compartment, settings pages, etc)
>   - Do not change any folder names
>   - Give me a preview of where all you will make changes before you make it
>   - Do this as the last step of the workflow
>
> After the workflow completes,
> - Run automated-tests
> - Do a sync-docs
> - Do a finalize

## Items

- **R6-SIM-STD (WowAddonStandards):** a rule that every addon with a sim mode shows a Sim checkbox in its settings, next
  to Test.
- **R6-SIM-L (LibKa0s):** the Sim checkbox in OptionsCompose MasterControls, next to Test. It is driven by host hooks
  (the same is/toggle pair as the launcher's `isSimMode`/`toggleSim`), so ticking it does what `/xx sim` does and
  unticking it stops the sim.
- **R6-SIM (each addon with a sim mode):** wire the checkbox, with a test and a smoke row.
- **R6-MM2:** the MultiMeters export glyph (R6_ADDENDUM_MM_EXPORT_GLYPH.md).
- **R6-NAME (every addon, last step):** drop Ka0s from the display name everywhere, with folder names unchanged. The
  owner approves a preview of every site first (R6_RENAME_PREVIEW.md).
- **Finish:** `/dev-copilot:wow-automated-tests` per addon, `/dev-copilot:sync-docs` per repo, then `/dev-copilot:finalize`
  across every repo. The owner's "Do a finalize" is the go-ahead to merge.

## Later instruction (owner, 2026-11-04, verbatim)

> At the end of this workflow, after finalize, please close all github issues that have been done

- **R6-ISSUES:** after finalize, sweep the open issues in every collection repo and close each one the merged work
  resolved (commit or bundle evidence, or a `state:done` label), with a comment naming the commit. Issues that are only
  partly done stay open and are reported: LibKa0s#70 (SF-DR-9, deferred) and #74 (filed this round). GitHub writes are
  spaced out.

## Scope note (owner, 2026-11-04, verbatim)

> Note - ignore the Outfitter repo from this sweep - that is currently being converted to a Ka0s addon by a separate agent

- Every finish step skips ../Outfitter: the automated tests, sync-docs, finalize (no merge, push or branch cleanup there)
  and R6-ISSUES (no issue closed there). This is the same rule the whole run already follows.
