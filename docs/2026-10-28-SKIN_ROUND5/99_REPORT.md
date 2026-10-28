# Execution record: skin round 5 (R5-01..R5-08)

Executed 2026-10-28 against [`00_PLAN.md`](00_PLAN.md) and the owner's notes in
[`inputs/OWNER_NOTES.md`](inputs/OWNER_NOTES.md). Branch `feat/2026-10-28-skin-round5` in all four repos.

## Commits

| Id | Repo | Commit | Subject |
|---|---|---|---|
| R5-01 | LibKa0s | `247ccf4` | A scroll corridor and one flat knob in every skin |
| R5-02 | LibKa0s | `91513c4`, `8d3142b` | Draw a window's edge over its children (and the lint follow-up) |
| R5-03 | LibKa0s | `f58852c` | A font family of its own for every skin |
| R5-04 | LibKa0s | `3974846` | Arrows in each skin's accent, and WoW Forever's check in its tan |
| R5-07 | LibKa0s | `55883fa` | Name release record 20261028-015008 in the v1.78.0 release-gate line |
| R5-06 | LootHistory | `02d03ef` | Re-vendor the re-cut LibKa0s v1.78.0 (skin round 5) |
| R5-05 | LibKa0sSkinTester | `221f4cc` | Re-vendor the re-cut LibKa0s v1.78.0; card names on one line |
| R5-08 | this repo | see `git log` | The plan and this record |

The local tag `v1.78.0` was re-cut from `3b640fd` to `55883fa`, after a clean-tree release run
(`docs/automated-tests/20261028-015008/`). It is **not pushed**.

## What landed

- **Scroll bars (R5-01).** Every skin draws a corridor that stands apart from its window and one flat
  knob in the skin's color inside it. The client's knob art is faded, so High Contrast no longer shows
  two knobs. `scroll.thumbFill` and `scroll.thumbTexture` are retired (never released). A case checks,
  in every skin, the corridor against the window (contrast at least 1.12) and the knob against the
  corridor (at least 3).
- **Corners (R5-02).** The window's edge and inner rule sit on a holder ten frame levels above the
  window, so the title bar and footer can no longer cover the edge at the four corners (Azeroth's 3px
  edge, High Contrast's and WoW Midnight's 2px). Ka0s Default's 1px edge draws where it did.
- **Fonts (R5-03).** One family per skin, used for body and titles alike; the title is the family's
  heavier weight:

  | Skin | Family | Body / title size |
  |---|---|---|
  | Obsidian | Inter | 12 / 14 |
  | Azeroth | Vollkorn | 13 / 14 |
  | Glass | Nunito | 12.5 / 14 |
  | High Contrast | Atkinson Hyperlegible | unchanged |
  | Ember | Bitter | 12 / 13.5 |
  | WoW Midnight | Philosopher | 12.5 / 14 |
  | WoW Forever | Fira Sans | 12 / 14 |
  | Ka0s Default, WoW Default | Friz Quadrata (the client's) | unchanged |

  Barlow and Cinzel leave the payload. `tools/artwork/fonts.py` pins each upstream by sha and cuts
  the static weights from the variable fonts.
- **Showroom audit (R5-04, R5-05).** The paging, dropdown and sort arrows are desaturated before they
  are tinted, so they take each skin's accent (a new `icon.arrow` token) instead of always showing the
  client's yellow. WoW Forever's check mark is its tan. The tester's skin cards keep their name on one
  line: a name wider than the card is drawn at a smaller text scale. Glass's "On" label was sampled
  and reads correctly, so it is unchanged.
- **Consumers (R5-05, R5-06).** Both addons re-vendored. LootHistory's chrome cases read the window
  edge from its holder, its table case answers Azeroth's Vollkorn, and its v1.78.0 minors are pinned
  at the re-cut. README credits and smoke checks name the new faces.

## Gates at the end

| Repo | Tests | Lint |
|---|---|---|
| LibKa0s | 3030 passed / 2 skipped / 3032 (release run, complexity max CCN 15, perf not measured) | 0/0 in 223 files |
| LootHistory | 1788 passed / 1 skipped / 1789 | 0/0 in 149 files |
| LibKa0sSkinTester | 486 passed / 1 skipped / 487 | 0/0 in 65 files |

## Calls I made

- **Ka0s Default and WoW Default share Friz Quadrata.** You asked for a reason if two skins share a
  face. Both skins exist to look like the game itself, and Friz Quadrata is the game's face; giving
  either one anything else would make it stop being the client's look. Every other skin has its own.
- **Vollkorn, not Alegreya, for Azeroth.** The plan named Alegreya. The collection's US-English prose
  gate flags the substring "grey" inside the name in every doc and file that mentions it, so the
  face was swapped for Vollkorn, a book serif of the same old-world kind.
- **Obsidian in Inter.** The modern face asked for: a neutral grotesque built for screens.
- **The payload grows.** The vendored fonts folder is 3.6 MB, up from about 0.6 MB, in every addon that
  vendors LibKa0s. Each family ships two weights.
- **Arrows follow the accent.** Every skin's arrows now wear its accent color, not only the four
  screenshots that showed the yellow.
- **A possibly timing-sensitive case.** "tool windows skin: without a registered owner each window is
  the previous minors' paint" (LibKa0s) failed twice while the machine was under heavy load, and
  passed in 40 repeated runs of a snapshot and in the release run. Recorded, not waived; worth a look
  if it recurs.

## Owner smoke

Record a result per row. None is marked passed here.

| Id | Where | Expected | Result |
|---|---|---|---|
| R5-S1 | Scroll bars in every skin: the showroom's lists, Loot History's History table, the settings panel's longest page | A corridor that stands apart from the window, one flat knob in the skin's color inside it, moving with the scroll; High Contrast shows one knob | |
| R5-S2 | The window corners on Azeroth, High Contrast and WoW Midnight (the showroom and Loot History) | The edge runs unbroken round all four corners; the title bar and footer sit inside it | |
| R5-S3 | Ka0s Default's window edge | The 1px edge where it was | |
| R5-S4 | Fonts, every skin | Each skin in its own family (table above), titles in the same family's heavier weight; no empty squares; sizes read comfortably | |
| R5-S5 | Obsidian | Inter reads modern and crisp | |
| R5-S6 | Paging, dropdown and sort arrows in every skin | In the skin's accent color (gold where the accent is gold), not the client's yellow in every skin | |
| R5-S7 | WoW Forever's checkboxes | The check mark in tan | |
| R5-S8 | The showroom's skin cards under High Contrast | Every name on one line, "High Contrast" a little smaller; full size again under Ka0s Default | |
| R5-S9 | Loot History with each skin | Nothing overflows its column in the new faces | |

## Later

Azeroth's border, R5-09..R5-11 and the smoke check R5-S10: [`01_AZEROTH_BORDER.md`](01_AZEROTH_BORDER.md).

## Screenshots and showcase (R5-13)

The owner's screenshots after round 5 ("skins look great now"), cropped to the window, are in LibKa0s
`docs/skins/screenshots/2026-10-28-round5/` (`60119af`): the Skin Tester's showroom and Loot History's
History tab in all nine skins, each folder with a `showcase.png` grid of every skin. The reusable
script is LibKa0s `tools/skin_gallery.py`; it reads the skins from `SkinDefs.lua`, so it needs no
change when a skin is added. `docs/skins/README.md` says how to run it for any addon.

## Finalized (2026-10-28)

Merged `--no-ff` and pushed to `master` on the owner's go-ahead ("go ahead and do the merge and push
everything to master"); the feature branch deleted in every repo.

| Repo | Merge | Gate on the merge |
|---|---|---|
| LibKa0s | `5caa63b` | 3031 passed / 2 skipped, luacheck 0/0 over 223 files |
| LootHistory | `4db0fb1` | 1788 passed / 1 skipped, luacheck 0/0 over 149 files |
| LibKa0sSkinTester | `2f1d12e` | 486 passed / 1 skipped, luacheck 0/0 over 65 files |
| this repo | see `git log` | — |

The local tag `v1.78.0` (`b2f6ec6`) is **not pushed**: the owner has not said to push it.
