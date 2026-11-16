# Execution record

What actually happened, against `01_EXECUTION_PLAN.md`, which stays as it was written. Progress comes from git
(`plan-data/resume-state.sh`). Checkpoint evidence is in `plan-data/checkpoints.tsv`.

## Timeline (2026-11-16, IST)

- **02:59–03:24.** REC-00 (the bundle), ISS-00's GitHub comments on #75, #76 and #85, and LK-P1, with its
  review approved. The build workflow then stopped when the PC restarted overnight, while LK-P2 was starting.
  Nothing was half-written: every tree was clean.
- **Morning.** Recovery. `resume-state.sh` reported 0 / 40 because `--since=2026-11-16` reads as "today at the
  current clock time". It now reads `--since=2026-11-16T00:00` (`b59b283`).
  - With the owner's OK, #91 was closed as `state:done` with a comment mapping its three questions, and two
    follow-ups were filed: dev-copilot#1 (the shared wago helper) and LibKa0s#93 (a validate-seeds contract for
    Compat and the test kit's client globals). ISS-00 went into `exceptions.tsv` (`900f0c8`).
  - The build workflow was relaunched from LK-P2 with this session's trailer
    (`plan-data/build-workflow.js`, `bb31778`).
- **11:52–19:26.** M1–M7. Every library item was reviewed, and each review is a `refs/notes/ka0s-review` note.
  All approved; LK-92B needed one round of review fixes (`35948d42`).
  - **LK-REL** split three LK-86 functions back under CCN 15 before the release run (`fa7d5b51`). The release
    battery is `docs/automated-tests/20261116-184422`.
  - **STD-01/02:** standard v2.113.0, which was free on origin (origin at v2.112.2).
  - **DC-78:** dev-copilot 2.10.1.
- **19:40. Checkpoint A** passed. The lead re-ran the gates, cut the local tag `v1.105.0` at `79b1d9c4`, and
  pushed the run branches of LibKa0s, WowAddonStandards and dev-copilot.
- **M8.** DropWatcher's other session had finished, and its checkout was back on a clean `master`. So no worktree
  was needed: every addon's run branch was created by the lead in its main checkout
  (`plan-data/revendor-workflow.js`). 18 of 19 re-vendors committed green, and ST-82 followed RV-ST.
- **LK-FIX-1 (a library fix found at re-vendor).** LootHistory stopped with its kit leak gate 6 MB over its
  256 MB budget.
  - **Cause, proven by elimination:** the first cut of kit 57 (LK-75) wrapped `UnregisterEvent` and
    `UnregisterAllEvents` on every mock frame, and LootHistory makes about 26,000 frames.
  - **Fix:** the frame stub in `mock_base.lua` holds and releases through one hooks table per build
    (`Events.frameHooks`), so the hold adds no closure per frame.
  - A new case pins it; it is red against the first cut. All seven LK-75 hold cases still pass. Kit revision
    stays 57, since it is unreleased. LibKa0s gate: 4871 / 0 / 3.
  - The local tag was re-cut at `8209c104`.
  - The release battery bundle predates the fix. The fix touches only `testkit/`, and its new branches sit in
    the stub's own small methods (lizard counts them apart; `stubFrame` stays CCN 2).
- **Re-copy.** The 18 addons that had already re-vendored received the two changed kit files from the re-cut
  tag. Each got a second `RV-<ABBR>:` commit and a bundle addendum, `06_RECOPY_LK-FIX-1.md`, and its gate was
  re-run under every client the roster lists.
  - ConsumableMaster, KickCD and PrettyChat had their eol gate red: the M8 agents had left their bundle files
    with LF on disk under a CRLF declaration. They were repaired with the gate's own recipe
    (`rm <path> && git checkout -- <path>`) and then gated green.
- **RV-LH** was finished on the corrected kit (`678a737`). Its leak gate passes at the default budget.

## Smoke checks added during execution

`06_SMOKE_TESTS.md` is unchanged. These belong with it:

- **Skin Tester SHOW-52** (ST-82, in `LibKa0sSkinTester/docs/smoke-tests.md`). Open `/st show` → Overlays →
  the "Hot" row, in all nine skins. This is the one-window form of SM-82 and SM-84.
- **AuraMaster** (from RV-AM's bundle, `01_DELTA` 3g). The library's attached-tooltip fallback no longer goes to
  the cursor. Where neither the strip, the cursor nor the screen reads, the strip tooltip is left unanchored,
  in the restricted tree. Check the strip tooltip in and out of combat.
- **AuraMaster owner ruling owed in phase [3]:** the player option `tooltipAnchor` still offers `ANCHOR_CURSOR`
  and the corner anchors, which #92's placement rule retires.

## Adoption

Each addon's `docs/revendor/2026-11-16-v1.105.0/` bundle lists the adoption it owes, with issue numbers, for
phase [3] (`03_ADOPTION_PLAN.md`). Nothing was interviewed and nothing was filed.

## Not done by this run

Pushing the tag, merging and closing the built issues wait for the owner's smoke and go-ahead (`RESUME.md`
step 5). Fetch WowAddonStandards and renumber v2.113.0 first if another session has released it.
