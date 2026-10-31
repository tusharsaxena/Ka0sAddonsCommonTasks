# I_DROPWATCHER: item 10 (image-38..42)

Read-only inventory. DropWatcher is at `acd2980` on `feat/2026-10-30-skin-library-followups` and vendors
LibKa0s v1.81.0 (`CLAUDE.md:44`, OptionsWidgets minor 36). LibKa0s is at `aefeba9`. Paths are relative
to `../DropWatcher` unless stated otherwise.

## (a) The Situations table's Loot rule dropdown is cut off (image-38)

**Current behavior.** The table is a raw frame with fixed x offsets, built in `settings/PageEditors.lua`:

- `:119` `SIT_COL = { situation = 8, track = 140, autoOpen = 205, quality = 285, rule = 460 }`
- `:120` `SIT_QUALITY_W, SIT_RULE_W = 160, 150`
- `:181-197` `situationPick` anchors each dropdown `LEFT` at `x` with `SetWidth(width)`. `:229-230` places
  the quality and rule cells, and `:241` (`situationHeader`) places the headers at the same x.
- The host fills the holder (`:315-317`, `SetAllPoints(holder.frame)`), which is a full-width child of
  the AceGUI scroll. LibKa0s's scroll takes a 20 px `GUTTER` for the always-visible scrollbar
  (`LibKa0s/OptionsScroll.lua:57`, `:94-97`).

**Root cause.** The rule column's right edge is at 460 + 150 = **610**. I measured image-38: the column
headers sit at situation 8 → 32 px and track 140 → 192 px, which gives about 1.21 screen px per unit. On
that scale the dropdown ends at about 760 px, and the scroll gutter starts at about 755 px. So roughly
**600 units** are usable, and the cell runs 10 to 15 units past them. The comment at `:117` ("Five
columns since feedback-24 ... the cells sit closer") shows that the fifth column was squeezed in, not
measured.

**Proposed change** (DropWatcher, `settings/PageEditors.lua`):

- Shift everything left and narrow the two dropdowns slightly, so the table ends about 25 units clear of
  the gutter:
  `SIT_COL = { situation = 8, track = 128, autoOpen = 188, quality = 262, rule = 424 }`
  `SIT_QUALITY_W, SIT_RULE_W = 150, 150`
  The quality cell ends at 412, a 12-unit gap before the rule cell, as today's gap is 15. The rule cell
  ends at **574**. The widest label, "Follower dungeon", is about 95 units from x = 8, so it still clears
  Track at 128. Its tooltip hit box ends at `track - 8` (`:206`) and follows automatically. "Auto-open",
  about 50 units from 188, clears Quality at 262. "Use global", "Personal loot" and "Legacy loot" fit in
  150.
- Add `SIT_TABLE_W = 576` and expose `P.SIT_COL`, `P.SIT_WIDTHS` and `P.SIT_TABLE_W` for the suite.
- Alternative (more robust, more change): anchor the rule cell and its header to the row's `RIGHT` with a
  -8 inset, so the table always fits at any panel width. I don't recommend it. The headless mock would
  need right anchors measured, and the other tables in the collection (Loot History's price table) use
  fixed x.

**Tests** (`tests/test_settings_pages.lua`, beside the "five gold, left-aligned column headers" test at
`:171`):

- Every column's x is strictly increasing.
- `SIT_COL.rule + SIT_RULE_W <= SIT_TABLE_W`, and `SIT_COL.quality + SIT_QUALITY_W < SIT_COL.rule`.
- Each header's x equals its cell's x.

This should be red before the change: 610 > 576.

**Risk.** Low. It is a cosmetic offset change, but the real usable width depends on the Settings canvas.
This needs an owner smoke at the default Settings window size and in a narrow skin.

## (b) Proc (flipbook) by default, main #19FF19, off-spec #3FC7EB (image-39)

**Current behavior.**

- `defaults/Profile.lua:27-41` `glow(enabled, style, tone)`, then `:168-171`
  `main = glow(true, "pixel", TONE.glowMain)` and `offSpec = glow(true, "pixel", TONE.glowOffSpec)`.
- The colors are fixed tones in `core/Constants.lua:213-217`: `glowMain` is #FFF468 (255,244,104) and
  `glowOffSpec` is #3FC7EB (63,199,235). **The off-spec color is already the requested value**, so only
  the main color changes, to (25,255,25)/255.
- The schema rows take their defaults from `P.glow` (`settings/SchemaRows.lua:514-517` for the type,
  `:536` for the color), and Database.lua builds the AceDB defaults from those rows
  (`core/Database.lua:4-7`).

**Migration under AceDB.** **No migration is needed for "follow the default".** AceDB merges defaults
through a metatable, so a profile that never wrote `glow.*.type` or `glow.*.color` reads the new default
at once. At logout AceDB also strips any stored value equal to its default.

The owner's SavedVariables (`ADD1KTED2KA0S/SavedVariables/DropWatcher.lua:15061-15073`) store
`main.type = "proc"`, `offSpec.type = "proc"` and `main.color = { r = 0.09803922474384308, g = 1, b =
0.09803922474384308 }`:

- The two `type` values will be stripped as defaults. That is harmless.
- The stored red and blue (0.0980392247...) are float32-rounded and are **not** equal to `25/255`
  (0.0980392156...). That color entry will persist. It looks identical and is harmless, but
  `/dw diagnostics` non-defaults would still list it.

There is a consequence for players: every existing profile that never chose a style switches from Pixel
border to Proc on update. The precedent is "no migration" (`toast.enabled`, `modules/Toast.lua:26-27`).

**Proposed change** (DropWatcher):

- `core/Constants.lua:213-217`: set `glowMain = { r = 25/255, g = 255/255, b = 25/255 }` and update the
  comment to "#19FF19, owner 2026-10-30".
- `defaults/Profile.lua:164-171`: change `"pixel"` to `"proc"` for both glows and update the comment.
- The comment at `settings/SchemaRows.lua:151-152` says "the default, Pixel border, first". Keep the
  dropdown order and fix the wording only.
- Docs: `docs/schema.md:177` (the #FFF468 row and the type default row), `docs/module-map.md:20,38`,
  `docs/settings-panel.md:291-292`, and `docs/smoke-tests.md` GLOW-10, which covers the H6 defaults.

**Tests to change:**

- `tests/test_schema_rows.lua:252-263`: the type is now `"proc"` and `hex(TONE.glowMain)` is now
  "19FF19".
- `tests/test_schema_rows.lua:323-345`: the knob-dim test assumes both glows default to pixel (comment
  `:327`, and `assertFalse(dim("glow.offSpec.pixelLines"))` at `:330` and `:345`). Set
  `glow.offSpec.type = "pixel"` explicitly at the start, or flip the expectations.
- `tests/test_glow.lua:112-136`: the comments say both default to pixel. The asserts set the type
  explicitly, so check `:121-124`, where the off-spec is expected to be pixel by default; that test
  probably needs an explicit `Set`.
- The `:211` `"PixelGlow_Start"` default-render assertion needs checking.

## (c) Hide a style's sections unless a style dropdown selects it (image-40, -41, -42)

**Current behavior.** The rows are built by DropWatcher's own schema (`settings/SchemaRows.lua:500-559`)
and rendered by **LibKa0s-Options' flow engine** through `RenderTabbedSchema`, with a declared renderer
(`settings/Pages.lua:66-70`). They are not AceConfig and use no `hidden=`. Each knob of each glow is a
row in subgroup `knob.heading` and carries `disabledIf = knobOff(key, knob.styles)` (`:503-509`, `:546-552`). So
the rows are **dimmed, not hidden**, which is what image-40 and -41 show: Pixel border, Auto cast and
Button are all drawn grey under Proc/Proc.

**What the library offers today.** LibKa0s-Options W22 `shownWhen = { path, equals = v | {v, ...} }`
(`LibKa0s/LibKa0s/OptionsWidgets.lua:1280-1326`, docs `docs/api/Options/version-34...-docs.md:1402-1429,
3142`). It drops a row before the subgroup pass, so a subgroup with every row dropped loses its heading.
It also watches the selector and re-renders the page once on the next frame. AuraMaster
(`settings/Layout.lua:54`, `:366-453`) and PartyFrameEnhanced (`settings/ElementRows.lua`) use it.

**Gap.** `shownWhen` takes **one** selector path (`shownNow` at `:1294-1305` reads `sw.path` only), and
`switchedRows` (`:1310-1326`) collects single paths. The owner asks for an **OR across two selectors**:
show the Pixel border section (both columns) when main.type or offSpec.type is pixel. Hiding per glow
would break the main | off-spec pairing, which a test pins (`tests/test_schema_rows.lua:265-286`, and
rows alternate main and off-spec). So both rows of a pair must carry the same OR predicate.

**Proposed change.**

1. **LibKa0s** (`OptionsWidgets.lua`, minor 36 → 37, W23): `shownWhen` also accepts
   `{ any = { { path = p1, equals = ... }, { path = p2, equals = ... } } }`. The row is shown when any
   clause holds, and a clause read that raises reads as shown. `switchedRows` registers every clause's
   path as a selector. The single-path form stays byte-for-byte the same.
   - Tests in LibKa0s's Options suite: an `any` row is dropped only when every clause fails, a subgroup
     whose rows are all dropped loses its heading, a change to either selector re-renders once, and two
     changes in one frame still cost one re-render.
   - Docs: the API doc, `members-*.json` and `CONSUMERS.md` (DropWatcher becomes a consumer of W23).
   - Then re-vendor DropWatcher.
2. **DropWatcher** `settings/SchemaRows.lua:546-552`: for each knob, add
   ```lua
   shownWhen = { any = { { path = "glow.main.type",    equals = stylesList(knob.styles) },
                         { path = "glow.offSpec.type", equals = stylesList(knob.styles) } } }
   ```
   to both rows of the pair. `stylesList` turns the `styles` set into a sorted list. Keep `knobOff` as
   `disabledIf`: with Pixel and Proc chosen, both sections show, and in each section the column whose
   glow is in the other style stays dimmed, as does a glow that is turned off. That keeps the existing
   dim test meaningful. The **Offset** subgroup (pixel, autocast, proc) follows the same rule, so it
   hides only when both glows are Button. I recommend this; it is open question Q3 below.
   - Whether a turned-off glow's style should still open its section is open question Q2.
3. If the lead does not want a library change in this run, a DropWatcher-only workaround is possible: a
   synthetic, path-less `field` selector computed from both types. **I don't recommend it.** The watcher
   keys on a drawn row's `path` or `field` (`:1343-1365`), so a synthetic selector would need a hidden
   drawn row. That is a hack.

**Tests** (DropWatcher):

- `tests/test_settings_pages.lua`: render Alerts › Upgrade glow and assert the drawn subgroup headings:
  - Proc/Proc (the new default): `Effect|Offset|Proc (flipbook)`.
  - Pixel/Proc: `Effect|Offset|Pixel border|Proc (flipbook)`, with the off-spec pixel row dimmed.
  - Button/Button: `Effect|Button (rotating rays)`.
  - A `Set` of `glow.main.type` re-renders: drive the mock `C_Timer`.
- `tests/test_schema_rows.lua:288-302` ("style subsections read in the Style dropdown's order") stays
  as it is, because it walks the schema, not the render.
- `docs/settings-panel.md` and smoke GLOW-8 change from "dimmed" to "hidden; dimmed column within a
  shown section".

**Risks.**

- The re-render happens on the next frame, so a pullout that is open closes. The library already
  handles this (options-ui-§11).
- The hidden rows are still in the schema, and `/dw set` and Defaults still reach them (W22 contract).
- Because LibKa0s moves, every addon needs a revendor eventually, but only DropWatcher needs W23 now.

## (d) A generic "show a section only when it is selected" mechanism, and the LibKa0s issue

LibKa0s has W22 `shownWhen` (single selector, above). The standard says nothing about it: there is no
`shownWhen` or "switched section" text in `WowAddonStandards/standards/standards/options-ui.md`. Only
`options-ui.md:545` covers dependent rows, and only as wording. Known candidates for a sweep:

- KickCD `settings/Icons.lua:427-455`: Primary and Secondary glow style, with `knobOff` dimming. This is
  the same pattern as DropWatcher, which shares its knob table (`defaults/Profile.lua:23-26`).
- Any other addon with a style or mode dropdown whose subsections are dimmed.

**Draft issue for LibKa0s.**

> **Title:** Options: `shownWhen` across several selectors (OR), then sweep every addon's dropdown-chosen sections and make it a MUST
>
> **Labels:** enhancement, state:untriaged, severity:medium
>
> **Body:**
> A subsection that a dropdown chooses should be **hidden**, not dimmed, while the dropdown chooses
> something else. This is the owner's ruling, from DropWatcher's Upgrade glow tab on 2026-10-30
> (Ka0sAddonsCommonTasks `docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK`, item 10). W22 `shownWhen`
> (`OptionsWidgets.lua:1280-1326`) already does this for **one** selector. DropWatcher's two glows (main
> | off-spec, paired rows) need the section shown when **either** style dropdown selects it.
>
> 1. **Library (W23):** `shownWhen = { any = { { path = ..., equals = ... }, ... } }`. The row is shown
>    when any clause holds, and a raising clause reads as shown. Every clause's path is watched as a
>    selector, so a change to any of them re-renders the page once, on the next frame and coalesced.
>    The single-path form is unchanged. Tests, the API doc, `members-*.json` and `CONSUMERS.md`.
> 2. **Sweep:** check every Ka0s addon (ADDONS.md) for subsections chosen by a dropdown and drawn
>    dimmed through `disabledIf`, and move them to `shownWhen`. Known: KickCD `settings/Icons.lua:427-455`
>    (glow style knobs). Users already: AuraMaster `settings/Layout.lua`, PartyFrameEnhanced
>    `settings/ElementRows.lua`. Keep `disabledIf` for a single row that a checkbox gates, and for a
>    column within a shown section.
> 3. **Standard:** add an options-ui MUST: "A subsection whose relevance a dropdown (or several, OR)
>    chooses is drawn only while it is chosen (`shownWhen`); a row a checkbox gates keeps `disabledIf`."
>    Add the matching anti-pattern: a dropdown-chosen section left dimmed. Also add an audit check.
>
> Acceptance: the library suite covers `any`, DropWatcher's Upgrade glow tab shows only the selected
> styles' sections, the sweep's findings are each fixed or ticketed, and the standard is bumped.

My recommendation is to file it as one umbrella issue on LibKa0s, with the standard change as a
checklist item. I would build part 1 in this run, since DropWatcher needs it, and leave the sweep as a
follow-up.

## (e) Draft DropWatcher issue: stack the toasts

**Current behavior.** "ONE AT A TIME" (`modules/Toast.lua:46-52`):

- Drops that qualify queue in the shell, keyed by drop id, `Toast.MAX_QUEUE = 5` (`:95`), with the
  oldest dropped first. The next one shows when the current one goes, after `toast.duration` (8 s),
  through close or right-click.
- `Toast.Consider` (`:524-536`) calls `toast:Show(id, {key, sticky})`.
- The shell is **LibKa0s-Toast-1.0 minor 1** (`LibKa0s/LibKa0s/Toast.lua:53`). It has a single frame
  (`build`/`ensureFrame` `:225-244`) and a single queue (`enqueue`/`pump` `:248-297`, where `pump` shows
  the first presentable entry and stops).
- The API doc (`docs/api/Toast/version-1-docs.md:22-37`) makes "one alert at a time" a design bar and
  says "no queue-or-replace flag". DpsRace's `modules/BestToast.lua` is the second consumer.

So stacking **needs a LibKa0s-Toast minor 2**, not only DropWatcher code.

**Draft issue for DropWatcher.**

> **Title:** Toast: stack the toasts when several drops qualify, instead of showing them one after another
>
> **Labels:** enhancement, state:untriaged, severity:low
>
> **Body:**
> When several drops qualify close together (a raid boss), the upgrade toast shows them one at a time
> (`modules/Toast.lua:46-52`). Each waits up to `toast.duration` (8 s) behind the one before, and a
> sixth drop pushes the oldest out of the queue (`MAX_QUEUE = 5`, `:95`). The owner wants them
> **stacked**: every toast that applies is on screen at once, one under another, each with its own
> countdown, hover pause, Ask and close.
>
> Needs a LibKa0s-Toast-1.0 change. The shell has one frame and one queue (`LibKa0s/Toast.lua:225-297`),
> and its v1 contract is "one alert at a time". Proposal for minor 2: an opt-in descriptor field
> `stack = <max visible>`, with a growth direction (`stackGrow = "DOWN" | "UP"`) and a spacing. That gives
> a frame pool, each frame anchored to the previous one and the first to the saved point. A closed toast
> re-flows the rest. The overflow beyond `stack` still queues. `Hold` puts every visible toast back at
> the head in order. `Remove(key)`, `Stats()` (a `shown` count and the keys of the visible toasts),
> `Preview` and drag, which moves the head frame, all keep working. Absent, it behaves exactly as v1
> (DpsRace unchanged).
>
> DropWatcher side:
>
> - Add a `toast.stack` setting (Alerts › Toast, 1 to 5, default to be decided).
> - Change `Toast.Prune`/`Dismiss`/`Ask` (`:538-560`, `:607`) to name a toast, since "the" current toast
>   no longer exists. `shownId()` (`:249`) becomes a set.
> - Diagnostics change to list the visible toasts.
> - In test mode, the sticky placeholders stack too.
> - Tests: `tests/test_toast*.lua` for N qualifying drops → N frames, re-flow on close, overflow
>   queued, the combat hold.
>
> Smoke: TOAST-* gets a "three upgrades at once" step (`/dw sim`).

## Open questions for the lead

1. **(b) Existing profiles follow the new default** (Pixel → Proc for anyone who never chose). Migrate to
   pin `"pixel"` for them? *Recommendation: no migration.* It matches the `toast.enabled` precedent and is
   the owner's stated default.
2. **(c) Does a turned-off glow's style still open its section?** *Recommendation: yes, by style only.*
   The section shows and is dimmed by the existing `knobOff`, so hiding never depends on a checkbox, in
   line with W22's "a row a checkbox gates keeps `disabledIf`".
3. **(c) Does the Offset section hide too** when both styles are Button? *Recommendation: yes.* It uses
   the same OR mechanism with styles {pixel, autocast, proc}.
4. **(c) Library W23 in this run, or the DropWatcher-only hack?** *Recommendation: W23 in LibKa0s in this
   run.* It is small and opt-in, and the issue's sweep and standard MUST follow later.
5. **(c) Should Proc move first in the subsection order,** now that it is the default? *Recommendation:
   no.* Keep the dropdown's order; the test at `tests/test_schema_rows.lua:288-302` pins it.
6. **(a) Fixed offsets or right-anchored?** *Recommendation: fixed offsets* as proposed, with a width
   test.
7. **(e) The stack issue's library half:** file it on DropWatcher only, which references LibKa0s, or also
   as a LibKa0s issue? *Recommendation:* file the DropWatcher issue now, and file the LibKa0s-Toast
   minor 2 issue when it is scheduled.
