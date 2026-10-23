# OWNER_SCOPE — sim auto-run, QuickComms preview selector, mode strips, MM/KCD simulators

Received 2026-10-23. The owner's request, verbatim, followed by the answers to the upfront questions.
This file is binding: an item spec or design note that contradicts it loses.

## A. The request (verbatim)

> For /xx sim - it should just "run all" by default - remove the run all button
> - can still manually pause and click on every step indvidually
>
> For /qc preview, by default it should open a small window (similar to perf or wim window) which adds a dropdown to select the various preview situations that are available in the settings panel.
> - This preview mode selector should be active while preview mode is active
> - This preview mode selector should be available no matter how preview mode was invoked (slash command, settings page)
> - The /qc preview xxx slash commands should still work, and change the preview mode selector window option as well
> - Add a "end preview" button in the window next to the selector as well
>
> Remove the "TEST MODE" from window headers wherever the test mode strip exists
> - E.g. remove it from multimeters, dropwatcher, loothistory, bankledger
> - do NOT remove it from QuickComms, etc where the test mode strip does not exist
>
> Add a "simulation strip" similar to the "test mode strip"
> - Consider reusing the test mode strip since its similar in nature (make it more genric in libka0s)
> - Remove the SIMULATION from the header of addosn which have sim mode
>
> Add a /mm sim and /kcd sim workflow for multimeters and kickcd respectively
>
> Add a note upstream (WowAddonStandards, LibKa0s, devcopilot for wow addons in version bump) to relook at the test mode data and sim mode data + workflows

Execution guidelines: ask upfront, then decide; resumable checkpointed plan; branch + incremental commits; push
feature branches at major milestones; never merge without the go-ahead; after merge, delete every branch, stash
and worktree the run created; use ultracode workflows.

## B. Answers to the upfront questions (2026-10-23)

1. **QuickComms preview window covers "Preview as…" only.** A bare `/qc preview` opens the window and starts a
   preview of the current situation. Plain Test mode (placeholder pads) is unchanged and gets no window.
2. **KickCD's simulation marker is a sim strip attached to the top of the party icon grid**, shown only while
   a simulation runs. (KickCD has no test mode, so there is no TEST MODE header to remove.)
3. **The upstream note is a release-check rule:** a rule in the standard's release section; a step in
   dev-copilot's WoW bump-version flow that asks the owner whether test-mode data and sim scenarios are still
   current; and a line in LibKa0s's release checklist. No tracking issues.
4. **MultiMeters and KickCD simulators take the scenario lists in MultiMeters#60 and KickCD#38 as scope**, each
   with a headless end-to-end suite. Both issues close when the work merges.

## C. Lead's interpretations (decided, not asked)

- "/xx sim" means every Sim-1.0 host. The change lives in LibKa0s (SimPanel/SimTimeline): starting a simulation,
  from the picker's Start or the typed `/<slash> sim start …`, and a Restart, plays the run straight away at the
  host's step delay. The "Run all" button goes. Pause/Resume, Restart and Stop stay. While paused, clicking a step
  row still steps or runs up to it. The typed `run` verb stays as a synonym of resume, for scripts and muscle memory.
- "Similar to perf or wim window" is read as the Perf panel or the Sim step panel: a small docked/floating
  library-styled window.
- The QC selector window is shown exactly while a "Preview as…" preview is active, from any entry point; ending the
  preview from anywhere hides it. Its close control ends the preview (it is the "End preview" path).
- The generic strip is the existing `W.TestStrip`, generalized in LibKa0s with a sim flavor (its own tint); the
  existing `TestStrip` call keeps working unchanged.
- "Window headers" means the title bar / title text mode word. The header word goes from every window that shows
  the corresponding strip; any surface without a strip keeps its word.
- Every roster addon re-vendors the new LibKa0s tag and the new standard reference, as previous runs did.
- No addon version bump, no tag push, no merge without the owner's go-ahead.
