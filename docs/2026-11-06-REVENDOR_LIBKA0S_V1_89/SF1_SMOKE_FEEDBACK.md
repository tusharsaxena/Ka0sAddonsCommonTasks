# SF1: the owner's first smoke feedback, and what it adds to the run (2026-11-06)

The owner smoke-tested the run branch and reported four problems, then a fifth while the lead was still
working. A read-only diagnosis workflow diagnosed each report, and an adversarial agent challenged each
diagnosis; the lead re-measured the edges in the screenshots. The screenshots and the raw diagnosis
stay out of the repo because they carry account details. The owner then answered three questions.
None of the problems comes from a commit in this run: the v1.85.0..v1.89.0 library diff touches no
Skin, Options or edge code, and the owner disabled EllesmereUI (updated the same day) and saw no
change.

| # | Report | Cause (evidence) | Owner ruling | Item |
|---|---|---|---|---|
| 1 | ConsumableMaster under Ka0s Default: a thick white edge on every bar button | CM's HUD token `cm.buttonBorder` (`core/SkinSetup.lua:147`) is `{1,1,1,1}` under Ka0s Default and follows `icon.border` under every other skin (since FS-CM-FLIP `3827acf`, 2026-11-01). The test character's profile was untouched, so the default border showed; the owner's usual profile turns it off. Pixel sample: `000000 f8f8f8×3 000000` | **Thin dark edge**: Ka0s Default follows the skin's icon edge like the other skins | SF1-CM |
| 2 | Skin Tester: the three "PaintAce (Scope: panel)" cells drew stock AceGUI chrome | The tester's Ignore settings panel was ON in the live session, so the painter declines the owner (`SkinAce.lua:858`). The likely cause is an Apply to all or Skin-tab copy from another addon (`lib.__copySkinTo`, `OptionsAppearance.lua:432`), which carries that addon's Scope over the tester's documented `ignorePanel = false`. Round 4 flagged this risk (`2026-11-03-SMOKE_ROUND4/inputs/INVESTIGATION.md:199,282`). The owner confirmed that `GetIgnore` printed true and that unticking the box fixed it | A copy leaves a host's documented Scope deviation alone | SF1-L2 + SF1-ST |
| 3 | Skin Tester EditBox edge looks too thick | Fixed by the untick in 2 (the owner confirmed). The edge is also a 1-UI-unit backdrop edge, so SF1-L1 covers it | (with 2) | SF1-L1 |
| 4 | DropWatcher's and DpsRace's dropdowns and filter box look different from LootHistory's, which is correct ("the border seems different") | They are already the same component (`W.Dropdown` / `W.SearchBox`, with identical opts in all three seams). The edge is a BackdropTemplate `edgeSize = 1` in **UI units** (`Widgets.lua:828` dropdown, `:1035` search box, `:671` the shared menu), so at the owner's UI scale it renders 1 or 2 px depending on the frame's sub-pixel position. Measured: DropWatcher's top edge is 2 px and its bottom edge 1 px, where LootHistory's are 1 px each. The library already sizes icon edges in physical pixels (`SkinPaintExtras.lua:567` `P.px`, re-sized on scale changes) | Every addon's window dropdowns and search boxes look like LootHistory's. Scope is addon windows only; AceConfig settings panels are left alone | SF1-L1 |
| 5 | DpsRace's column headers have a grey line above and below. LootHistory's do not, and LootHistory is correct | To be diagnosed in its item | Match LootHistory, in every addon that draws such lines | SF1-DR (+ `SF1-<X>-HDR`) |

## The items

- **SF1-L1** (LibKa0s): every Widgets edge of 1 UI unit on a host surface becomes one **physical**
  pixel at any UI scale and any sub-pixel position. That covers the dropdown, the search box, the
  shared menu and its cascade levels, the Autocomplete list, and any other `edgeSize = 1` backdrop
  under `Widgets*.lua`. The edges are re-sized on scale changes through the existing `P.px` and
  pixel-refresh mechanism, under every skin and with no skin.
- **SF1-L2** (LibKa0s): `RegisterOwner` takes an opt-out that `lib.__copySkinTo` honours. Apply to
  all and the Skin-tab copy then carry skin and media to that owner, but never its Scope.
- **SF1-L3** (LibKa0s): release v1.90.0 (CHANGELOG, API documents, releasing.md, the minors), with the
  tag cut **locally**. The tag is pushed only at the owner's go-ahead.
- **SF1-RV-<X>**: re-vendor v1.90.0 into all 17 addons, OutfitterReborn included, each with a
  `docs/revendor/2026-11-06-v1.90.0/` bundle.
- **SF1-CM**: `cm.buttonBorder` under Ka0s Default follows `icon.border` (a thin dark edge). The
  stored default changes to match.
- **SF1-ST**: the Skin Tester registers with the SF1-L2 opt-out.
- **SF1-DR**: DpsRace's column-header lines go, to match LootHistory. Every other addon's column
  headers are checked for the same lines, and any fix lands in that addon's own `SF1-<X>-HDR` commit.

Not taken:

- Relabelling DpsRace's dropdowns to "Field: Value", or changing gaps and widths. The owner named the
  border, not the labels.
- Changing PremadeGroupsFilterExtension's panel. It keeps its deliberate Blizzard LFG look, because
  it sits inside the Group Finder.
- Changing MultiMeters' 24 px Export dropdown. It is left as it is.
