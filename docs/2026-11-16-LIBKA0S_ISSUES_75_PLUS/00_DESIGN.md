# LibKa0s issues #75 and up: design

**Opened:** 2026-11-16. **Run branch** (every repo touched): `feat/2026-11-16-libka0s-75-plus`.
**Inputs:** `inputs/owner-rulings.md` (normative), `inputs/issues/` (the issue bodies as of 2026-11-16) and
`inputs/research/R1..R9` (the read-only research with file:line evidence). R9 is the critic's pass, and where R9
corrects an earlier note, R9 wins.

## 1. Intent

Ship every open LibKa0s issue numbered #75 or higher that has library work, as one LibKa0s release, **v1.105.0**.
Then re-vendor that release into all 19 Ka0s addons and keep every green gate green. Plan, but do not execute,
the adoption of the new surfaces in each addon. The owner will run that later.

- **Goals.** The library work for #75, #78, #79, #80, #81, #82, #84, #86, #87, #90 and #92. The standard rules
  those surfaces need, as WowAddonStandards v2.113.0. CombatTrail joins `ADDONS.md`. Every addon vendors v1.105.0
  with its gate green.
- **Non-goals in this run.**
  - #83 FTUX (owner: a later run).
  - #76 Ace3, which is blocked upstream: no Ace3 tag contains `ac3d1225`. The newest is `Release-r1403` and is
    21 commits behind.
  - #85 (Callout consumers), #88 (docked strips) and #89 (footers). These are adoption only.
  - #91 (wago.tools survey). The validate-seeds rollout already covered it. Close the issue and file two
    follow-ups (R6).
  - Every addon-side adoption (phase [3], `03_ADOPTION_PLAN.md`).
- **Anti-goals.**
  - A re-vendor that changes an addon's own behavior beyond what the library change itself forces.
  - A standard rule that makes all 19 addons non-compliant the moment they re-vendor.
  - Any bump of an addon version, tag push or merge without the owner's go-ahead.

## 2. Approaches considered

- **A: one branch and one tag (v1.105.0), then the sweep. Chosen.** One release record, one re-vendor per addon,
  and one smoke at the end (owner Q5).
- **B: two tags.** Fixes first (#75, #78, #82, #84, #90), surfaces second (#79, #80, #81, #86, #87, #92). Rejected:
  each addon would be re-vendored twice, which costs two release records and doubles the sweep. It only paid off
  with a smoke gate between the tags, and the owner declined one.
- **C: re-vendor after each issue.** Rejected: 19 × 11 commits for no benefit.

## 3. Library design (v1.105.0)

There is one local tag, and it is pushed only at finalize. Each surface below lists the issue, what ships, and the
owner rulings or my calls (marked **[call]**). The detail and evidence are in the cited research note.

### 3.1 Hygiene peels first (R9 §2)

The files these issues edit are already past their size triggers, so each one is peeled before any behavior moves.
A peel changes no behavior and the gate stays green.

- `OptionsSkinPicker.lua` (1493 lines, trigger 1400): peel on its queue seam.
- `tests/test_launcher.lua` (1235 lines, trigger 1200).
- `tests/test_debuglog.lua`: move the core-skew cases to `tests/test_debuglog_coreskew.lua`. The new console
  cases go in `tests/test_debuglog_footer.lua`.
- `WidgetsDragHandle.lua`: peel its tooltip half as part of #92.

### 3.2 #75 test kit: keep registered frames alive (R1)

Half 1, the `unregisterAll` guard, already shipped in kit rev 51 (`367a9f10`). The fix here is to hold a frame
strongly while it has a raw event registration.

- `Events.decorateFrame` wraps `RegisterEvent`, `RegisterUnitEvent`, `UnregisterEvent` and `UnregisterAllEvents`.
- `mock_ace.lua`'s override for embedded frames releases the hold too.
- The hold is per build, never module-level, or `test_mock_base.lua:321` (the dropped build) goes red.
- The kit goes to **rev 57**, which it shares with #92's `mock_screen.lua`.
- Regression test: register, `collectgarbage()`, fire, and the frame still receives the event.

### 3.3 #78 SimPanel default title (R1)

A new string, `PANEL_TITLE = "%s - SIM"`. SimPanel's minor moves (one Sim key move, shared with #92 and #86).
No player sees the change, because every host sets its own title. The rest of #78:

- **WowAddonStandards:** M-2 (clients.md "once") and M-4 (the Bindings.xml note), in v2.113.0.
- **dev-copilot:** a game-versions column in the releases report, and no hard-coded interface numbers in
  `profiles/wow/bump-version.md`, as a patch release.
- **Closed with evidence:** M-5 (`camelot, forever`) as will-not-do, since `forever` is an unverified game-type
  token; "sixty-seven" (already fixed); `bump_interface`'s client awareness (covered by its per-slot logic).

### 3.4 #82 and #84 skin contrast (R5; owner Q2)

- **Every failing skin** gets new `icon.hot` (and `list.hover` where it fails) values. **Forever's `icon.hot`
  becomes `#FFFFFF`.**
- **Ka0s Default rows:** stripe `.08`, hover `.16`, selected `.26` **[call, R5 D-5]**. The Ka0s exemption in the
  stripe test is dropped.
- **High Contrast** has a named exemption on hot-vs-heading. Its rest tint dims to `#A0A0A0` and its hot is white.
- **A kit contrast floor in `tests/test_skin_defs.lua`,** written red first:
  - hot vs rest, ΔL* ≥ 10
  - hot vs heading, ΔL* ≥ 10 (High Contrast exempt)
  - stripe vs plain row, composited over the window background
  - hover wash vs background

  The floors follow R5 §4.
- One Skin key move: SkinDefs 27→28, SkinDefsOthers 9→10.
- **Re-vendor follow-ups:**
  - OutfitterReborn's `of.bar.worn` moves to `text.accent` (R5 D-7).
  - LootHistory, BankLedger and DropWatcher re-copy the Ka0s Default fallbacks.
  - CombatTrail's and DpsRace's own stripe defaults (.025 / .04) move to the new Ka0s values **[call]**, so
    #84 is fixed where it was reported.
- **Skin Tester** gains a hot-state sample row (R5 D-9), so #82 can be smoked in one window across all nine
  skins.

### 3.5 #79 report seam and #90 console footer, one DebugLog key `23.11.1.5` (R3, R1, R9 C7)

- **`D:Report(tag, title, fn) -> n`** lives in `DebugLogDiagnostics.lua` **[call, R3 D1]**.
  - It collects the body first, so a refusal writes nothing.
  - It writes a `/<slash> <title>` header and then the body, ungated. It does not turn logging on (D7).
  - It reveals the console and prints exactly one pointer line through the descriptor's `print`:
    `<title>: N lines written to the debug console. Use Copy to share it.` (D8). N counts the header.
  - A raising body is caught with `pcall`. What was collected is written, plus one `<title> failed: <err>` line,
    and the pointer is still printed (D2).
  - The degradation stub streams the report to chat with no pointer.
- **`D:Serialize(value, opts) -> lines`.** Keys are sorted, nested tables are indented, values are secret-safe,
  and depth, line count and cycles are capped. It is on the instance as a forwarder, so the stub can answer it
  (D6). It returns the lines and does not write them.
- **Plain-text Copy.** `D:Add` keeps the colored line for the view, in a private parallel `__view` that a skin
  switch re-renders (D3), and keeps the color-stripped line in `D.buffer`. `|n` becomes a space and a raw newline
  is kept (D5). `||` escapes survive the strip. Host tests pin colors through the view, with no new public
  reader (D4).
- **#90.** The console's status line moves onto `W.Footer` at 24 px. The footer has no owner, so its counter
  keeps the mono face (debug-logging-§11). The counter is drawn in `text.muted`. The window keeps a four-line
  minimum height and its 700×344 default. The left text is empty. `f.lineCount` and `f.statusDivider` stay as
  aliases.
- The console's header marks carry **no tooltips**, which keeps the documented choice at
  `DebugLogWindow.lua:192-197` **[call, R9 C2]**.
- **Re-vendor cost:** the stub gains `Report` and `Serialize` in 14 addons. ConsumableMaster's three
  color-pinned tests are rewritten to read the view.

### 3.6 #92 tooltip placement: new major `LibKa0s-Tooltip-1.0` (R2, R9 C1)

- **`Tooltip.lua`,** minor 1, with no dependencies. It loads after CorePixel and publishes:

  | Member | What it does |
  |---|---|
  | `TIP_GAP = 2` | The gap between a tooltip and what it is placed against. |
  | `Tip.Own` | Takes ownership of the tooltip for a frame. |
  | `Tip.PlaceBeside(tip, el, group, opts)` | Beside the window group: right if it fits, else left, else centered below. Its top is level with `el`, clamped vertically, and a companion opens on its side away from the main window. |
  | `Tip.PlaceAttached(tip, el, "top"\|"bottom")` | Attached and horizontally centered, below top chrome or above the footer, flipping at the screen edge. |
  | `Tip.PlaceLauncher` | Toward the screen centre, by screen half and third. |
  | `Tip.SetGroup`, `Tip.GroupOf` | Set or look up a frame's window group. |
  | `Tip.Replace` | Re-places a tooltip after late growth. |
  | `__solve*` | The pure solver functions behind the placers. |

  Placement is applied as absolute UIParent points after `Show()`. Only the launcher uses a relative anchor.
- **The library's own sites move:**
  - IconBrowser (cell and toolbar)
  - WidgetsDropdown entries
  - WidgetsReorder handle
  - SimPanel `showTip`
  - WidgetsDragHandle. A HUD strip is **top chrome**, so its tooltip goes attached and centered below it
    **[call, the standard's text]**. `tooltipOwner = "cursor"` and `tooltipAnchor` are retired to the attached
    placer.
  - Charts and ChartsRender, through an additive host seam: a fourth `ctx` argument with `ctx:PlaceTip`, plus an
    optional `host.group`.
  - The Launcher's `drawTooltip`, which re-places a LibDBIcon minimap tooltip only when the owner is the
    addon's own button. LibDBIcon is not patched.
  - The skin picker's three `attachTip` sites (R9 C1).
- **N/A:** the debug console and the PerfPanel have no tooltips. Options pages on the Settings canvas are out of
  scope (owner, 2026-11-15).
- **Kit `mock_screen.lua`** (rev 57) gives every host a fake screen for its own tests.
- **A grep-guard test:** no `ANCHOR_CURSOR`, `ANCHOR_CURSOR_RIGHT`, `ANCHOR_RIGHT` or `ANCHOR_TOP` in the payload
  outside the Settings-canvas Options files.
- **Smoke risk:** whether `SetAnchorType` re-anchors the tooltip. Check it in wow-ui-source and add a smoke check.

### 3.7 #86 header buttons and #81 launcher extras (R4; owner Q1, Q3)

- **`W.HeaderButtons(titleBar, spec)`** lives in a new `WidgetsHeader.lua`.
  - The marks are right-aligned, left to right **extras · settings · close**. They share one size, one pitch and
    one paint path (`S.Mark`), and draw from the LibKa0s icon set.
  - Each mark's tooltip is placed by the chrome rule through `Tip.PlaceAttached`, except on the console (§3.5).
  - The `help` icon is not used, because 12 addons do not declare it.
- **Where settings comes from:** a Core registry that `Launcher:New` fills, keyed by the descriptor's `addonName`.
  Each window spec can override it with `onSettings`. A library test pins the `addonName` lookup. At re-vendor,
  each host is checked so its Launcher name matches (R9 C8).
- **Windows that migrate:**
  - debug console, copy window (which hides itself before it opens settings), perf panel, sim panel, skin picker:
    each carries settings.
  - icon browser: opts out, because it is opened from a settings row.
  - drag handle (HUD strip): settings is **opt-in** this run (`spec.settings = true`) **[call, R4 Q4]**.
- **The launcher's instance gains no public member** (it is parity-checked in 9 addons).
- **#81:** an optional `extraEntries = { { label, checked = fn|nil, onClick = fn, clients = {...}|nil } }`.
  - At most 2 entries.
  - They are placed between Show window and Open settings, gated by default, with a plain-string label only.
  - launcher-§2 is amended to match.
- The one-consumer ruling (Skill Master) is recorded in the API doc and the CHANGELOG.

### 3.8 #80 `W.Bar` (R4; owner Q1)

The Skill Master `modules/Bar.lua` bar is promoted into a new `WidgetsBar.lua`:

- A fill segment, plus a bonus overflow segment (temp or permanent) clamped to the bar.
- Tier ticks and threshold markers. Marker labels are carried in `geom` and not drawn **[call, R4 Q11]**.
- An expiry timer and a text template.
- The presets `row`, `compact`, `tooltip` and `mini`.
- Thin `W.AcquireBar` and `W.ReleaseBars` over LibKa0s-Pool.
- An owner-token repaint. There are no new skin tokens: the bonus segments default to `sem.info` and `sem.good`,
  and a host remaps them **[call, R4 Q10]**.

The Skill Master internals it depends on are generalized (R4 §3). Skill Master swaps to it in the adoption phase.
The one-consumer ruling is recorded.

### 3.9 #87 sample characters (owner Q4; R6)

- **A naming convention**, written into the standard's preview-mode section:
  - The names are obviously fictional ("Sample…" or "Mock…").
  - No real realm names and no real-looking `Name-Realm` pairs.
  - Fixed sample realm names.
  - Pets and guilds follow the same pattern.
- **Two sets as data on LibKa0s-Sim** (Sim minor moves): `Sim.SAMPLE.retail` and `Sim.SAMPLE.forever`. Each holds
  about five characters, each with a name, realm, class token, a spec or talent tree that is valid on that client,
  and a pet where one fits. `Sim.Sample(client)` returns the active client's set.
- DropWatcher and MultiMeters keep their seeded crowd lists.
- **Re-vendor cost:** one stub edit in the 5 addons that parity-check Sim. Addons switch to the data at adoption.

### 3.10 Release record

The release is recorded the way earlier releases were:

- One version block naming every file's live minor (R9 §5 has the table).
- `docs/api` for every key that moved, and the members JSON for every stub.
- `CONSUMERS.md`.
- The CHANGELOG entry, with a "What a consumer owes" section.
- The automated-tests bundle and its `RESULTS.md` row.
- `docs/test-cases.md` regenerated.
- The local tag `v1.105.0`.

Before tagging, fetch tags: if `v1.105.0` already exists, renumber.

## 4. Standard and roster (WowAddonStandards v2.113.0)

Everything ships as one minor on the run branch:

- **`ADDONS.md`** gains Ka0s Combat Trail. Its clients, launcher entries, skin-picker preview and sim checkbox are
  read from CombatTrail's own code. Repo `https://github.com/tusharsaxena/CombatTrail`, default branch `main`.
- **debug-logging and slash-commands:** the report ruling from #79, carried over as written.
- **debug-logging-§11:** the console footer wording (#90).
- **standalone-windows:**
  - The header-button rule from #86: the order, settings on every window, the opt-outs. The one-wrapper close
    bullet admits `W.HeaderButtons`.
  - The tooltip-placement "future surface" text names `LibKa0s-Tooltip-1.0` (#92).
- **launcher-§2:** the amendment for extra entries (#81). The ADDONS launcher column lists extras.
- **skinning-§4:** the hover/hot contrast bullet (#82 and #84).
- **preview-mode:** the sample-character convention (#87).
- **clients:** M-2 and M-4 (#78).
- **What is owed when (owner Q6).** Every new rule binds an addon **when it adopts the feature**. The open
  adoption issues are the tracker. A re-vendor to v1.105.0 does not by itself make an addon non-compliant. Each
  addon's re-vendor bundle names what it now owes. The tooltip text from v2.112.0 is reworded the same way.
- Each addon's standard pointer stays where it is in this run **[call, R9 §7.10]**.
- Other sessions release the standard mid-run (memory `standard-version-collisions`), so fetch and renumber
  before finalize.

## 5. Re-vendor (phase [2])

All 19 addons re-vendor v1.105.0. Each addon gets one commit on its run branch: `RV-<ABBR>: ...`.

- **The copy half only.** Follow `/dev-copilot:wow-revendor-libka0s` from the installed plugin (2.10.0) for the
  copy and the bundle: both payloads copied whole, the provenance line rolled, the icon and sound prune, the delta
  report, and the `docs/revendor/<date>-v1.105.0/` bundle (plus the span bundle where one is owed). **Skip the
  adoption interview and its GitHub issue filing.** That is phase [3], and workflow agents cannot write to GitHub.
- **Fixes each addon is expected to need** (R7, R8, R9 §3):
  - Options stub `SideTabs` (15 addons)
  - DebugLog stub `Report` and `Serialize` (14)
  - Compat identity stub members (MultiMeters, PGFE, WhatGroup)
  - Sim stub sample members (5)
  - XML-order lines in the hand-written loader lists for the new payload files (PGFE, WhatGroup, Skin Tester)
  - MultiMeters' font-row pin
  - Ka0s Default fallback copies (LootHistory, BankLedger, DropWatcher)
  - per-skin `icon.hot` pins (Skill Master, DropWatcher, OutfitterReborn, if red)
  - OutfitterReborn's `of.bar.worn` (D-7)
  - CombatTrail's and DpsRace's stripe defaults
  - any suite turned red by the kit-57 frame hold
- **Never weaken a test to get green.** A red test is diagnosed (bisect before theorizing). If the cause is in the
  library, the fix goes to LibKa0s, the local tag is re-cut, and every addon that has already re-vendored is
  re-copied.
- **Gate:** each addon's own green gate from its `CLAUDE.md` (both client profiles where it lists both), luacheck
  through `ka0s-bounded` at 0/0, and the 1500-line cap.
- **Order:** everything in parallel, except DropWatcher, which goes last.
  - If DropWatcher's checkout is still on the other session's branch, its re-vendor runs in a worktree off
    `master` (`../.worktrees/DropWatcher-75plus`). That worktree is removed at cleanup.
  - The game loads the main checkout, so DropWatcher's smoke waits until its branch is merged or checked out.
- **Default branches:** SkillMaster and CombatTrail use `main`. Detect the default branch in every repo.

## 6. Adoption (phase [3]), planned only

`03_ADOPTION_PLAN.md` holds the per-addon matrix for #79, #80, #81, #85, #86, #87, #88, #89 and #92, with the
counts and sites from R3, R7 and R8 and the order to run it in.

## 7. What is left to the builder

Exact token values inside R5's floors, the exact solver geometry, and file splits under the size caps. Also
anything a test proves better than prose. Anything that changes a ruling above goes back to the owner.
