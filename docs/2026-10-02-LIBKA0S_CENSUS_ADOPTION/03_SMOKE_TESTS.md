# In-client smoke tests

The owner's to run, on a Retail client with every Ka0s addon on its feature branch. Record each result in the
**Result** column. Nobody else marks a check passed. Each addon's `docs/smoke-tests.md` carries the same checks
under its own ids; the ids below are the planned ones and the executor may renumber them to the next free id.

Before you start: `/console scriptErrors 1`, and BugSack (or the default error frame) visible.

## S0. Load

| # | Check | Expected | Result |
|---|---|---|---|
| S0-1 | Log in with all eleven addons, `/reload` twice | No Lua error; no LibKa0s minor-mismatch line | |
| S0-2 | Open each addon's settings panel | Every page renders as before | |
| S0-3 | Library windows: resize the debug console, the copy window and the perf panel | Exactly as on v1.66.0 | |

## S1. IdList help art (LibKa0s#42)

| # | Check | Expected | Result |
|---|---|---|---|
| ID-1 | AuraMaster: `/am` → Filters, and General → spells, on an entry that carries help | The mark is the white `info` glyph tinted by level (gold, amber, red), not Blizzard's blue disc, and no green or empty square | |
| ID-2 | Hover a help mark | Brightens, returns to its level colour on leave; tooltip lists the help lines | |
| ID-3 | `/am debug on`, open those pages | No `[Cfg] help art:` line | |
| ID-4 | BankLedger and LootHistory item lists | Render exactly as before | |

## S2. Resize grips (LibKa0s#41, BankLedger#21, LootHistory#33, MultiMeters#58)

| # | Check | Expected | Result |
|---|---|---|---|
| LH-1 | LootHistory unlocked: drag the History window's grip with the left button, release, `/reload`, `/lh show` | Resizes, pressed hatch while held, stops at its minimum; size kept. Right-click does nothing | |
| LH-2 | Tick Lock frame, drag the grip | Grip still drawn, nothing resizes, nothing saved; untick and it resizes again | |
| LH-3 | The DB-size footer | Never sits under the grip | |
| BL-1 | BankLedger `/bl show`: drag the grip both ways | Table re-flows live, stops at the all-columns width; footer clear of the grip | |
| BL-2 | Resize only (no title drag), `/reload`; then Reset position, `/reload` | Size kept; after reset the default size and centre | |
| BL-3 | Session window at a bank: resize, close, `/reload`, reopen | Rows re-bind live, scroll arrow clickable, size kept | |
| BL-4 | Lock frame ticked, drag either grip | Still resizes (unchanged; lock gates the drag only). Say if it should gate | |
| MM-1 | MultiMeters window unlocked: drag the grip, `/reload` | Resizes, stops at the grid minimum, size kept; one `[Set]` width/height pair per drag with debug on | |
| MM-2 | Grip size | Now 16 px (was 12); it does not cover the last row's value at the minimum size | |
| MM-3 | Frame strata HIGH, then DIALOG; window alpha 0.5 | The grip follows strata and alpha | |
| MM-4 | Rule-driven hide then show; lock; minimize then `/mm lock off`; expand | Grip back after the show; none when locked; none over a collapsed window; back on expand | |

## S3. Slash vocabulary (AbsorbTracker#33, ConsumableMaster#44, KickCD#36)

| # | Check | Expected | Result |
|---|---|---|---|
| AT-1 | `/at profile new alpha`, `/at profile Default`, `/at profile list`, bare `/at profile` | `Available profiles`, sorted ignoring case, `Default (current)` once; the bare list shows the same order | |
| AT-2 | `/at debug EVENTS`, `/at toggle TARGET`, `/at profile CURRENT` | Same answers as before (verb case-insensitive) | |
| CM-1 | `/cm priority`, `/cm stat`, `/cm aio`, `/cm bar help` | Rows look like `/cm help`: gold command, em dash, white text | |
| CM-2 | `/cm priority hp_pot list`, `/cm stat list` | Do what they name | |
| KC-1 | `/kcd debug`, `/kcd spells` | Sub-help rows look like `/kcd help` | |
| KC-2 | `/kcd debug interrupt` on a hostile caster with secret flags | `<secret>` where values are secret, no Lua error | |

## S4. Secret sentinel and layout (AbsorbTracker#33, MultiMeters#58, PanelMaster#56)

| # | Check | Expected | Result |
|---|---|---|---|
| SE-1 | Mid-fight: `/at diagnostics`, `/mm diagnostics` | Secret values read `<secret>`, plain fields still print | |
| PM-1 | `/pm config` → Profiles | Ace's profile controls line up with the divider and title on both edges; nothing clipped | |

## S5. Degraded (libs/LibKa0s renamed aside, `/reload`; restore afterwards)

| # | Check | Expected | Result |
|---|---|---|---|
| DG-1 | LootHistory, BankLedger | The grip still draws and resizes (old 2 px inset, no pressed art); LootHistory's lock still gates | |
| DG-2 | MultiMeters | No grip, no Lua error; `/mm lock` and `/mm lock off` raise nothing | |
| DG-3 | `/cm stat`, `/kcd debug`, `/kcd spells` | Plain `cmd  desc` rows, no colour, no Lua error | |
| DG-4 | `/at profile list`, `/at debug EVENTS` | Work; list order not checked | |
