# Execution record: skin feedback, rounds 1 and 2 (SF-01..SF-24)

Executed 2026-10-26 against [`00_PLAN.md`](00_PLAN.md) and its addenda
[`01_SHOWROOM_NOTES.md`](01_SHOWROOM_NOTES.md) and [`02_ROUND2_NOTES.md`](02_ROUND2_NOTES.md). Branch `feat/2026-10-26-skin-feedback` in all four repos.

## Commits

| Id | Repo | Commit | Subject |
|---|---|---|---|
| SF-01..SF-05 | LibKa0s | `a8bb0ad` | Retune five skins from the owner's notes (SkinDefs minor 7) |
| SF-10..SF-14 | LibKa0s | `fcdbb68` | Relative font sizes, row hover, disabled buttons, square checkboxes |
| SF-06 | LibKa0s | `fe7c3fc` | Name release record 20261026-181407 in the v1.78.0 release-gate line |
| SF-07 | LootHistory | `ac006e5` | Re-vendor the re-cut LibKa0s v1.78.0 |
| SF-08 | LibKa0sSkinTester | `3eed31f` | Re-vendor the re-cut LibKa0s v1.78.0 |
| SF-15 | LibKa0sSkinTester | `1fe24ba` | Draw the slider sample the way a host draws one |
| SF-09 | this repo | see `git log` | This record |
| SF-16..SF-22 | LibKa0s | `d7a610e` | Skin feedback round 2 |
| SF-06 | LibKa0s | `8291ecc` | Name release record 20261026-190317 in the v1.78.0 release-gate line |
| SF-23 | LootHistory | `625f9c5` | Re-vendor the re-cut LibKa0s v1.78.0 (round 2) |
| SF-24 | LibKa0sSkinTester | `d99008a` | Re-vendor the re-cut LibKa0s v1.78.0 (round 2) |

The local tag `v1.78.0` was re-cut from `7bc3e9b` to `fe7c3fc` after a clean-tree
`run-automated-tests.sh --release 1.78.0` (bundle `docs/automated-tests/20261026-181407/`), then to `8291ecc`
after round 2 (bundle `docs/automated-tests/20261026-190317/`). It is still unpushed. The first release run, at `a8bb0ad`, was aborted before it finished; the run that counts is the
one at `fcdbb68`.

## Gates at the end

| Repo | Tests | Lint |
|---|---|---|
| LibKa0s | 3017 passed / 2 skipped / 3019 | 0/0 over 223 files |
| LootHistory | 1782 passed / 1 skipped / 1783 | 0/0 over 148 files |
| LibKa0sSkinTester | 483 passed / 1 skipped / 484 | 0/0 over 65 files |

Mutation-checked, each turning its case red when undone: the size-keyed font object (SF-10), the disabled
label (SF-12), the shadowless dark label and the hint's face (SF-22).

## Decisions taken

- **Azeroth's "hard to read" font** was read as the body: the client's dark drop shadow on light parchment.
  Ember wears the same Cinzel titles and drew no note, so the titles stayed. Round 2 showed the rest of it:
  strings a primitive only tinted kept the client's font and shadow (SF-22), and the body moved to Atkinson
  Hyperlegible (SF-16).
- **WoW Default's "more original" buttons** come from tokens, not art: the schema has no button-art token,
  so the red gradient under a thin dark rim stands for `UIPanelButtonTemplate`. Blizzard's own button art
  would need a new token and a three-slice in `Button`.
- **"Every skin sets a size"** is met relatively: Ka0s Default's sizes are the reference, and a string keeps
  its own stock size scaled by the skin's over it. An absolute size per role would grow every caption to
  body size, which is the layout break the owner asked to avoid. Ka0s Default sets no face, so its text is
  unchanged.
- **Ka0s Default changes in two places on purpose:** the square checkbox, and with it LootHistory's Timeline
  toggle, which drew .24 gray. Its row hover stays gold.

## Owner smoke

Restart the client (the font objects are new), then `/st show` in the Skin Tester and Loot History on the
same skin. Only the owner fills Result.

| Id | Check | Expect | Result |
|---|---|---|---|
| SF-S1 | Click through all nine cards and scroll the whole showroom | Captions stay caption-sized in every skin; no text overlaps (High Contrast's EditBox caption, the Cinzel title lines in Text) | |
| SF-S2 | Lists section in every skin | "A row, hover" is clearly lighter than "normal" and clearly different from "selected" | |
| SF-S3 | Controls section in every skin | "Button (disabled)" reads dimmed; the Slider shows a track, a fill and a thumb, Ka0s Default included | |
| SF-S4 | Checkboxes in Ka0s Default and WoW Default | Ka0s Default: a square dark box with a thin edge and a gold mark. WoW Default: one Blizzard box, no second box round it | |
| SF-S5 | Azeroth | Muted parchment; body text crisp (no smear); tabs cream on brown, the selected one wax red; titles still Cinzel | |
| SF-S6 | Glass | The world no longer shows through; buttons, inputs and tabs flat with a thin frosted edge; tabs underlined in lilac | |
| SF-S7 | Obsidian, High Contrast, WoW Midnight, WoW Forever | Obsidian reads black next to Ka0s Default; High Contrast's control borders thin; Midnight's buttons violet with gold; Forever's primary filled tan | |
| SF-S8 | Loot History on each changed skin, and its settings pages | The History table, filters, Insights, Timeline (its toggle) and the settings checkboxes look right; nothing overflows its column | |

Round 2 rows (fill these too):

| Id | Check | Expect | Result |
|---|---|---|---|
| SF-S9 | Azeroth: the search box hint, the sort header, the footer | Crisp, no smear; the parchment a notch darker than round 1 | |
| SF-S10 | Primary next to Normal in every skin | The primary reads as a different button in all nine; its text reads cleanly (Obsidian, Ember, High Contrast, Forever) | |
| SF-S11 | High Contrast's tabs | The selected tab yellow on black with the yellow underline | |
| SF-S12 | WoW Default's buttons | Red with a thin dark rim, no gold frame; the primary brighter with a thin gold edge | |
| SF-S13 | The Slider in every skin | One shape everywhere: a thin bar, a fill in the skin's accent, a thumb; no box | |

## Open

- The owner's smoke pass above, then `/dev-copilot:finalize` over LibKa0s, LootHistory, LibKa0sSkinTester
  and this repo on the go-ahead. The v1.78.0 tag stays local until the owner says to push it.
- Still for a later round: renaming the Appearance tab to Styles, and the scope and font settings.
