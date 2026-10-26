# Execution record: skin feedback, rounds 1 to 4, the title bar and the Scope (SF-01..SF-40)

Executed 2026-10-26 against [`00_PLAN.md`](00_PLAN.md) and its addenda
[`01_SHOWROOM_NOTES.md`](01_SHOWROOM_NOTES.md), [`02_ROUND2_NOTES.md`](02_ROUND2_NOTES.md), [`03_ROUND4_NOTES.md`](03_ROUND4_NOTES.md) and
[`04_TITLEBAR_AND_SCOPE.md`](04_TITLEBAR_AND_SCOPE.md). Branch `feat/2026-10-26-skin-feedback` in all four repos.

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
| SF-25 + SF-26 | LibKa0s | `ce9a2a3` | WoW Default's tabs one height, its inputs a 1px edge (round 3) |
| SF-06 | LibKa0s | `e131bc6` | Name release record 20261026-193808 in the v1.78.0 release-gate line |
| SF-27 | LootHistory | `9c8bf82` | Re-vendor the re-cut LibKa0s v1.78.0 (round 3) |
| SF-28 | LibKa0sSkinTester | `288da15` | Re-vendor the re-cut LibKa0s v1.78.0 (round 3) |
| SF-29 | LootHistory | `e9ec74e` | The skin's face on LootHistory's own text; the browser tabs in the text roles |
| SF-30 + SF-31 + SF-32 | LibKa0s | `afbcb85` | Ka0s Default sets every token; Azeroth dark; Forever in Atkinson (round 4) |
| SF-30 | LibKa0s | `e1fca8b` | Keep the named-media case under CCN 15 |
| SF-06 | LibKa0s | `de76300` | Name release record 20261026-222042 in the v1.78.0 release-gate line |
| SF-33 | LootHistory | `0227508` | Re-vendor the re-cut LibKa0s v1.78.0 (round 4) |
| SF-34 | LibKa0sSkinTester | `a78b7fc` | Re-vendor the re-cut LibKa0s v1.78.0 (round 4) |
| SF-35 | LibKa0s | `f70882c` | Draw a fill as its target's own region, never on a frame below it |
| SF-06 | LibKa0s | `a6c00a4` | Name release record 20261027-001339 in the v1.78.0 release-gate line |
| SF-36 | LootHistory | `900e4fb` | Re-vendor the re-cut LibKa0s v1.78.0 (the title-bar fill) |
| SF-37 | LibKa0sSkinTester | `ed70d01` | Re-vendor the re-cut LibKa0s v1.78.0 (the title-bar fill) |
| SF-38 | LibKa0s | `fb8ff61` | The Appearance tab's Scope: Ignore settings panel, Ignore fonts |
| SF-38 | LibKa0s | `854ad32` | Never keep a page as its own backdrop |
| SF-06 | LibKa0s | `d4007bc` | Name release record 20261027-005758 in the v1.78.0 release-gate line |
| SF-39 | LootHistory | `be8201e`, `c03406d` | The Scope: storage, seams and pins |
| SF-40 | LibKa0sSkinTester | `4f2b793` | The Scope: storage, seams and pins |

The local tag `v1.78.0` was re-cut from `7bc3e9b` to `fe7c3fc` after a clean-tree
`run-automated-tests.sh --release 1.78.0` (bundle `docs/automated-tests/20261026-181407/`), then to `8291ecc`
after round 2 (bundle `docs/automated-tests/20261026-190317/`), then to `e131bc6` after round 3 (bundle
`docs/automated-tests/20261026-193808/`), then to `de76300` after round 4 (bundle `docs/automated-tests/20261026-222042/`;
a first round-4 run at `afbcb85` measured one test case at CCN 16 and was not kept), then to `a6c00a4` after SF-35
(bundle `docs/automated-tests/20261027-001339/`) and to `d4007bc` after SF-38 (bundle `docs/automated-tests/20261027-005758/`). It is still unpushed. The first release run, at `a8bb0ad`, was aborted before it finished; the run that counts is the
one at `fcdbb68`.

## Gates at the end

| Repo | Tests | Lint |
|---|---|---|
| LibKa0s | 3027 passed / 2 skipped / 3029 | 0/0 over 223 files |
| LootHistory | 1787 passed / 1 skipped / 1788 | 0/0 over 149 files |
| LibKa0sSkinTester | 484 passed / 1 skipped / 485 | 0/0 over 65 files |

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
  body size, which is the layout break the owner asked to avoid. Rounds 1 to 3 also read Ka0s Default as
  setting no face; the owner overturned that in round 4 (SF-30: it sets Friz Quadrata by name, and every
  other token).
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

Round 3, the owner's last notes ("Rest looks good"), on WoW Default alone: Tab 2 and Tab 3 stood shorter
than Tab 1 (Blizzard's `-InActiveTab` art is drawn shorter, so idle tabs now wear the active art and the
selected tab is told by its white label: SF-25), and the edit box and dropdown border was exaggerated (a
2px `bevelIn`; now 1px, the primary button's size, the nav rail with it: SF-26).

| Id | Check | Expect | Result |
|---|---|---|---|
| SF-S14 | WoW Default's tabs and inputs | Tab 1, Tab 2 and Tab 3 one height; the edit box and dropdown edges as thin as the primary button's | |

Round 4 (`03_ROUND4_NOTES.md`): Ka0s Default sets every token and is painted like every skin, Azeroth is
dark, WoW Forever wears Atkinson. Restart the client (new font objects and a new face on Default).

| Id | Check | Expect | Result |
|---|---|---|---|
| SF-S15 | Ka0s Default in the showroom, Loot History and its settings | The same look as before in Friz Quadrata; the scroll thumbs, slider, tabs and the settings rows drawn by the skin; nothing reverts to a different client look | |
| SF-S16 | Azeroth everywhere | Dark leather with parchment text; gold edges; the primary button and the selected tab wax red; no light parchment left anywhere | |
| SF-S17 | WoW Forever | Crisp Atkinson text (no blur); the background a touch browner than before, still dark | |
| SF-S18 | Loot History item names and the Insights quality bars, every skin | The client's quality colors (Epic purple, Rare blue) | |

The title bar and the Scope (`04_TITLEBAR_AND_SCOPE.md`). Restart the client again.

| Id | Check | Expect | Result |
|---|---|---|---|
| SF-S19 | Loot History on Azeroth (and two other skins) | The title bar wears its own dark band over the window, not the window's fill | |
| SF-S20 | Appearance tab, any addon | A **Scope** section below the skins: *Ignore settings panel* and *Ignore fonts* side by side, then *Copy to every Ka0s addon…* | |
| SF-S21 | Tick *Ignore fonts* in Loot History | Its window and settings text go back to the game's fonts at once, still colored by the skin; untick brings the skin's fonts back, no reload | |
| SF-S22 | Tick *Ignore settings panel* in Loot History | A reload popup; after the reload the settings pages are the game's own look while the History window still wears the skin; untick re-skins the open page | |
| SF-S23 | Copy to every Ka0s addon with a Scope set | The confirmation says "skin source, skin and scope"; the Skin Tester takes the same toggles | |

**A rule bent in SF-33:** LootHistory's `tests/golden.lua` asks a deliberate render change to regenerate
the golden in a commit of its own. The Insights golden (41 quality-color lines) went in with the re-vendor
commit instead, with the change stated in its message.

## Open

- The owner's smoke pass above, then `/dev-copilot:finalize` over LibKa0s, LootHistory, LibKa0sSkinTester
  and this repo on the go-ahead. The v1.78.0 tag stays local until the owner says to push it.
- Still for a later round: renaming the Appearance tab to Styles. (The scope and font settings shipped as SF-38..SF-40.)
- Azeroth's title bar in Loot History: the probe confirmed a frame-level tie; fixed in SF-35, awaiting SF-S19.
- Found while fixing the tests: Options-1.0's combat lock keeps PLAYER_REGEN_* registered after the
  Profiles page hides, until the next REGEN event re-syncs it. Harmless in the client, but worth a
  LibKa0s issue.
