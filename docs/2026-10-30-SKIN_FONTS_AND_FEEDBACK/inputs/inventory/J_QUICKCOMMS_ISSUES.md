# J: QuickComms test-dial icons (item 15) and the issues to file (items 10, 11, 14, 15)

Read-only inventory, 2026-10-30. All repos were read on `feat/2026-10-30-skin-library-followups` (the run
before this one; this run branches from master once that run is merged). Every repo's remote is
`github.com/tusharsaxena/<Repo>`. All three target repos carry the same label set: `bug`, `enhancement`,
`documentation`, `state:untriaged|triaged|done|will-not-do`, `severity:critical|high|medium|low`
(`gh label list`). A new issue is filed `state:untriaged` plus a severity, as `/dev-copilot:issue-add` does.

## (a) The `/qc test` dial's red "?" group icons (image-52)

### Current behaviour

- Test mode's groups are built in `QuickComms/modules/Surfaces.lua`. There are four
  (`S.TEST_COUNTS = { 4, 8, 12, 16 }`, `:41`). The pad's are built at `S.TestPlan` (`:229-236`) and the
  dial's at `S.TestDialPlan` (`:250-261`). A group is `{ id = "test."..s, title = L["Test group %d"], slots = ... }`
  (`:254`). **It has no `icon` and no `iconColor`.**
- The slots are fine. `testSlots` (`:214-226`) gives each slot a shipped callout's name, icon and color,
  taken in order from `NS.BuiltIns` (`testSamples`, `:190-209`). That is why image-53's second level has
  proper glyphs.
- The dial's first ring is made of group entries. `Dial_Layout.lua:330-333` `ringEntry` copies `src.icon`
  and `src.iconColor`, so a test group gives `icon = nil`.
- `Dial_Render.lua:571`, `btn.qcIcon:SetTexture(item.icon or DEFAULT_ICON)`, with
  `DEFAULT_ICON = "Interface\\Icons\\INV_Misc_QuestionMark"` (`:47`). That is the red "?".

### Real (non-test) groups fall back to "?" too

- A user group's icon defaults to `false` (`Library.lua:936`, `MEMBER_DEFAULTS.group.icon = false`,
  and `CreateGroup` `:537`). The dial plan copies `g.icon` (`Surfaces.lua:314`, and `:321` for children).
  `false or DEFAULT_ICON` draws the "?".
- A callout with no icon does the same on a pad (`Pad_Render.lua:44` and `:350`) and on a dial wedge.
- The settings editor's preview uses the same texture for "no icon" (`settings/Editors.lua:226`
  `Ed.NO_ICON`, used at `:375` and at `settings/Groups.lua:490`). The comment at `Editors.lua:221` says
  "the member draws none". That is false today, because the member draws the "?".
- Every built-in group and node has a glyph (`defaults/BuiltIns_*.lua`). Mythic+ uses `gi:dungeon-gate`
  in purple, Raid `gi:dragon-head-lorc` in red, Arena `gi:arena` in gold, World `gi:world` in green,
  Battlegrounds `gi:flag-objective` in gold, and In Group `ph:users-three` in cyan. So only test groups and
  user groups or callouts saved without an icon hit the fallback.

### The available icon keys

- QuickComms declares `LibKa0s icons: all (icon browser)` (`QuickComms/CLAUDE.md:45`), so the whole
  catalog ships in `libs/LibKa0s/media/icons/`. QuickComms has no icons of its own: `media/` holds only
  `logos/`, `screenshots/` and `textures/{dial,shine}`.
- The catalog (`LibKa0s/LibKa0s/Media.lua:92-` `lib.ICONS`, plus the generated
  `LibKa0s/LibKa0s/MediaIcons.lua`) has:
  - 113 hand-written semantic keys, for example `close`, `settings`, `chat`, `speech-bubble` (`Media.lua:115`);
  - 111 more Open Iconic marks, unprefixed;
  - 1434 Phosphor Fill marks, `ph:`;
  - 4178 Game-icons marks, `gi:`, under CC BY 3.0, with the author shown through `NS.IconAuthor`.
- They resolve through `NS.Icon(name)` (`core/MediaSetup.lua:16`). Glyphs are white on transparent, so
  `Library.IconTint` tints them (`Library.lua:307`).
- I checked that these candidates are in the catalog and that each one's `.tga` is in the vendored
  `QuickComms/libs/LibKa0s/media/icons/phosphor/`: `ph:number-circle-one` … `ph:number-circle-four`,
  `ph:dice-one` … `four`, `ph:flask`, `ph:test-tube`, `ph:folder`, `ph:folder-simple`, `ph:folders`,
  `ph:chat-circle-dots`, `ph:chat-dots`, `ph:megaphone`, `ph:squares-four` and `ph:circles-four`.

### Proposed change (QuickComms only)

1. **Test groups get distinct numbered glyphs.** Add a table beside `S.TEST_COUNTS` in
   `modules/Surfaces.lua`:
   `S.TEST_GLYPHS = { {"ph:number-circle-one","cyan"}, {"ph:number-circle-two","gold"}, {"ph:number-circle-three","purple"}, {"ph:number-circle-four","green"} }`
   The colors are `NS.BuiltIns.COLOR` keys (`defaults/BuiltIns.lua:19-22`). `TestPlan` and
   `TestDialPlan` then set `icon = NS.Icon(glyph)` and `iconColor = BI.COLOR[c]` on each group (and on
   each pad section, which ignores them today but stays symmetric).
   - **Why numbers:** the label already says "Test group N", the four glyphs cannot be confused, and
     they look like placeholders, which is the point of test mode.
   - **Alternative:** each test group borrows the glyph of the built-in group its first sample came
     from. I would not do that. The samples walk `BI.order`, which starts with Mythic+ (TOC load order
     at `QuickComms.toc:95-102`), so groups 1 and 2 would both get the M+ gate.
2. **A real default instead of the "?".** Add one helper in `core/MediaSetup.lua`:
   `NS.DefaultIcon(kind)`. It returns `NS.Icon("ph:folder-simple")` for a group or ring,
   `NS.Icon("ph:chat-circle-dots")` for a callout, and `INV_Misc_QuestionMark` as the last fallback when
   the library is absent. Use it in four places:
   - `Dial_Render.lua:47` and `:571`: pick by `item.kind == "ring"`;
   - `Pad_Render.lua:44` and `:350`: always a callout;
   - `settings/Editors.lua:226`: `Ed.NO_ICON` becomes a function of the editor's member kind, so the
     preview shows what will actually be drawn, and the comment at `:221` gets fixed;
   - `settings/Groups.lua:490`.

   The tint is white, because `IconTint` gives white for a glyph with no color.
3. **Tests** in `tests/test_surfaces.lua`:
   - Extend "test mode's dial holds the four test groups" (`:166-180`): every `kind == "ring"` item on
     the first ring has a non-nil icon that `NS.Library.IsGlyph` accepts, and the four icons are distinct.
   - New: "a dial group saved with no icon draws the group default, not the question mark". Assert it on
     `plan.rings[1].items[i]` through the render, or on the helper with a test in
     `tests/test_dial.lua` / `tests/test_pad.lua` that paints a slot with `icon = false` and reads
     `qcIcon`'s texture from the mock.
   - The red-under check: today the "?" path is the expected value.

   A smoke line goes in `docs/smoke-tests.md` (test mode's dial shows ①②③④ in four colors).

### Risks

- The preview-mode MUST "kept current at every release" applies, and the change is a refresh of test
  data. Record it as *Refreshed* at the next bump.
- Changing the "no icon" look also changes what saved user groups show today. This is intended, but the
  owner should know.
- `NS.Icon` answers nil when the library is absent, so the helper must keep the Blizzard fallback.

### Note for item 5 (glyph coverage)

`Dial_Layout.lua:321` formats flat-ring titles as `"%s · %s"` (U+00B7). That character belongs in item
5's sweep.

## (b) Existing issues: QuickComms open and close animations

**It already exists: QuickComms #13**, "Animate the Comms Pad and the dial on open and close". It is
open, labeled `enhancement, state:untriaged, severity:low`, and was filed on 2026-10-28.

- The body covers the dial (a fan or scale out, a fade, emphasis on the slice that sent) and the pad (a
  fade and scale). It also covers secure-header safety, a duration of about 0.1 to 0.2 s, one on/off
  setting, the stand-down and the preview window's dial.
- **The gap against the owner's wording, "each on its own":** #13 asks for *one* setting. Do not file a
  duplicate. Add this comment to #13 instead:

  > Owner, 2026-10-30 (Ka0sAddonsCommonTasks `docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK`, item 15): the
  > animations are configured **separately**: the pad and the dial each get their own open animation and
  > their own close animation. That is four independent switches, or a per-surface Open / Close style
  > dropdown with `None`. These are per-instance surface settings (`pads.<id>` / `dials.<id>`, on each
  > surface's own page), not one addon-wide toggle. The preview window follows the surface it previews.

Other searches with no duplicates. Each was run with `gh issue list --state all --search`:

- MultiMeters, `insight`: nothing.
- MultiMeters, `animation`: #23, closed and `state:done`, "Animate bar fills smoothly instead of
  snapping". It shipped in 1.1.0 (`bars.animate`, `modules/Row.lua:845-870`).
- DropWatcher, `stack` and `toast`: nothing about stacking. #12 (Insights tab) and #1 (wishlist) are
  unrelated.
- LibKa0s, `width`, `anchor`, `conditional` and `section`: nothing about either topic. Related: LibKa0s
  #66 (promote the Insights chart renderers, open).
- WowAddonStandards: nothing.

## (c) Issue drafts

### 1. QuickComms: no new issue

Comment on #13 as above.

### 2. MultiMeters: an Insights view

What MultiMeters shows today:

- the grid windows;
- the summary and spell-breakdown tooltips;
- the cell drill-down (`modules/DrillDown.lua`);
- the death recap;
- Targets (`modules/Targets.lua`);
- Export (`modules/Export.lua`, `Export_Modal.lua`);
- the segment picker, which reads Blizzard's own sessions (`C_DamageMeter.GetCombatSessionFromType`).

The hard constraint is `docs/scope.md:145-147`: the addon persists no meter numbers. On top of that,
`docs/scope.md:90-126` ("Deferred: scoring") rules that cross-column arithmetic is impossible in combat,
because the values are secret, and legal only out of combat or after a run.

> **Title:** Insights view: post-fight analysis of a segment, out of combat
>
> **Labels:** enhancement, state:untriaged, severity:low
>
> **Body:**
> ## Request
> Add an **Insights** view to Multi Meters. It is a window, or a mode of a meter window, that explains a
> finished segment instead of ranking it. It is modeled on the Insights tabs in Ka0s Loot History and
> Ka0s DPS Race (DpsRace#12), with KPI cards plus chart sections.
>
> ## Why it is out of combat only
> Every number is a secret value while the `Combat` restriction is active, and tainted code may not
> add, divide or compare one (`docs/scope.md`, *Deferred: scoring*). So Insights is computed **only when
> the restriction is inactive**: between pulls, after a boss, at the end of a key. It is read from the
> sessions the client already keeps (the segment picker's source), and **nothing is persisted**
> (`docs/scope.md`, *Persisting meter numbers*). In combat the view says *Available after combat* and
> computes nothing. It never guards arithmetic with `IsRestricted()` as a fallback.
>
> ## Candidate insights (to be checked against real segments before building)
> - **Cards:** group DPS and HPS, the pull's length, total interrupts, total dispels, deaths, and
>   avoidable damage taken.
> - **Shares:** each player's share of damage, of healing and of interrupts (stacked bar per column).
> - **Utility vs output:** interrupts and dispels per player next to their damage rank, which is the
>   "who carried" view that the scoring section defers.
> - **Avoidable damage:** ranked, with the top spells (drill-down data).
> - **Deaths:** count per player, and the killing blow per death (death-recap data).
> - **Overall vs current:** the same cards for Overall, for a key summary. This links to #9 (end-of-dungeon
>   summary popup) and #18 (time-into-the-fight).
>
> ## Notes
> - Build the charts on LibKa0s Charts if LibKa0s#66 has landed, instead of a private copy
>   (library-stack-§7).
> - It is a new window kind, so it needs a test-mode placeholder and a sim scenario step (preview-mode),
>   and it honors the stand-down.
> - Decide first whether it is a separate window, a tab of the drill-down, or a header control that
>   flips a meter window into Insights.

### 3. MultiMeters: bar animations

The bar-fill slide is already done (#23). The owner's "bar animations" must mean something beyond it.
The draft names the candidates and the constraint that decides each one:

> **Title:** Bar animations beyond the fill slide: rank changes, rows entering and leaving, value changes
>
> **Labels:** enhancement, state:untriaged, severity:low
>
> **Body:**
> ## Request
> #23 made each bar's fill slide to its new length (`bars.animate`, `modules/Row.lua:845-870`, through
> the client's `Enum.StatusBarInterpolation`). Add the other animations a meter usually has:
>
> 1. **Rank change:** a row slides to its new position instead of jumping when the order changes.
> 2. **Enter and leave:** a new row fades or slides in, and a row that leaves fades out.
> 3. **Change pulse** (optional): a brief highlight on a cell whose value just changed.
>
> ## Constraints to settle before designing
> - **Identity is sealed in combat.** In combat the rows come from the live ranking of the sort column,
>   and the other columns are matched by class and spec. The addon cannot always tell *which* player moved
>   (`README`, the restricted-header FAQ). A rank slide needs a stable per-row key. Out of combat that is
>   the identity. In combat it is the class+spec key, and a duplicate pair stays unanimated. Comparing
>   two values to detect a move is illegal on secrets, so movement has to come from the order the
>   provider hands over, never from comparing numbers.
> - A change pulse needs "did it change", which is a comparison of secrets. It is out of combat only, or
>   dropped. Investigate whether the fill's own interpolation can drive it.
> - Only insecure visuals: alpha and translation on the row frames, with AnimationGroups owned by the
>   row pool (`LibKa0s-Pool`), and nothing left running at stand-down.
> - Perf: the grid refreshes at `data.throttle` (0.25 s), so an animation must finish or retarget inside
>   one tick. Add a perf scenario.
>
> ## Done when
> Each animation that survives the constraints has its own switch next to `bars.animate` (Windows › Bars),
> has tests for the row-key and retarget logic, and has a smoke check.

The lead should ask the owner which of 1 to 3 he means.

### 4. The anchor-width check: track it in LibKa0s

Item 11 asks for this. Item E (`E_ANCHORS_SIM.md`) fixes the library's DragHandle fit in this run. This
issue is the follow-up check, run after the fonts are frozen.

> **Title:** Check every addon's mover/anchor label width in every skin, once the skin fonts are frozen
>
> **Labels:** bug, state:untriaged, severity:medium
>
> **Body:**
> In nearly every addon and nearly every skin, an unlocked anchor's title is cut off ("Ka0s KickCD — Fo…",
> owner, 2026-10-30, Ka0sAddonsCommonTasks `docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK` item 11, image-43..45).
> This run re-fits `LibKa0s-Widgets-1.0`'s drag handle (`WidgetsDragHandle.lua`, minor 8) so that it
> measures in the current skin's face with slack. That fix covers the library strip only. **After the
> skin fonts are frozen**, check every mover in every addon under every shipped skin, with Outline on
> and off and Ignore fonts on and off.
>
> - [ ] KickCD: `modules/IconGrid_Handle.lua`, `modules/Castbar_Handle.lua`
> - [ ] AbsorbTracker: `modules/Bar.lua`, `modules/Display.lua`
> - [ ] ConsumableMaster: `modules/MacroBar.lua`
> - [ ] QuickComms: `modules/Pad.lua` via `core/WidgetsSetup.lua`
> - [ ] AuraMaster: `modules/Anchors.lua` (deliberately capped strips; the shortened-text cache has no
>       face in its key)
> - [ ] LibKa0sSkinTester: `modules/ShowroomWidgets.lua`
> - [ ] PartyFrameEnhanced: `modules/Anchor.lua` (its own label, not DragHandle)
> - [ ] PanelMaster: `modules/Unlock.lua` (its own label, not DragHandle)
> - [ ] Any other roster addon (ADDONS.md) with an unlock or mover view: confirm none.
>
> For each: a screenshot per skin, and a fix (the host's `ApplyWidth` floor, a re-fit on skin change, or
> a shorter label) or a "fits" note. Where a check shows the library is at fault, fix it here. Where it
> is host code, fix it in that addon on a branch that cites this issue.
>
> Done when every box is ticked, with the screenshots under each repo's `media/screenshots/skins/vN`.

Which repo: I recommend **LibKa0s as the single tracker**, with the checklist above, not nine per-addon
issues. It is one check with one trigger (the font freeze) and one owner pass. `E_ANCHORS_SIM.md`
recommends one issue per addon instead. If the lead prefers that, the per-addon issues can be split out
from the checklist when the work is scheduled.

### 5. LibKa0s: conditional sections (validate across all addons, plus a MUST in the standard)

`I_DROPWATCHER.md` §(d) already has a full draft. Use it unchanged, with two wording additions so it
coordinates the three repos:

- In the title or the first line, say it is an **umbrella issue**, and that the standard's half is
  filed or done in WowAddonStandards: "adds an options-ui MUST and an anti-pattern; WowAddonStandards
  change cited here".
- In the sweep step, add "every addon in `WowAddonStandards/standards/ADDONS.md`", so it is checked
  against the roster rather than a list copied into the issue. Name the known non-users of `shownWhen`:
  KickCD (`settings/Icons.lua:427-455`) and DropWatcher (`settings/SchemaRows.lua:503-552`, which today
  greys the knobs through `knobOff` / `disabledIf`). The known users are AuraMaster
  `settings/Layout.lua` and PartyFrameEnhanced `settings/ElementRows.lua`.

The facts it rests on, which I checked: `shownWhen` exists at `LibKa0s/LibKa0s/OptionsWidgets.lua:1280-1326`
and takes a single `path`. Nothing in `WowAddonStandards/standards/standards/options-ui.md` mentions
`shownWhen` or switched sections. `:545` covers dependent rows as wording only. Labels:
`enhancement, state:untriaged, severity:medium`.

### 6. DropWatcher: stack the toasts

`I_DROPWATCHER.md` §(e) has a full draft, and I agree with it. The facts I checked:

- The one-at-a-time behavior is the library contract (`LibKa0s/LibKa0s/Toast.lua:23-24`,
  `lib.MAX_QUEUE = 5` at `:64`, the queue at `:246-297`).
- DropWatcher's side is `modules/Toast.lua:46-52`.
- DpsRace's `modules/BestToast.lua` is the second consumer and must stay unchanged, so the stacking is
  opt-in.

Labels: `enhancement, state:untriaged, severity:low`. Add one line to its Notes: "DpsRace#5 (personal-best
toast) is the other Toast-1.0 consumer; keep it on v1 behavior."

## Open questions for the lead

1. **Test-group glyphs:** use numbered circles (①②③④ in cyan, gold, purple and green), or themed
   glyphs? *Recommendation: numbered circles*, because they read as placeholders and match the labels.
2. **The "no icon" default for real groups and callouts:** use `ph:folder-simple` and
   `ph:chat-circle-dots`, or keep the "?" for real members and fix only test mode? *Recommendation:
   change it*. The "?" reads as a broken texture, which is exactly what the owner flagged. The editor
   preview should follow the same default.
3. **QuickComms #13:** comment with "each on its own", or edit the body? *Recommendation: comment.* It
   keeps the original record, and GitHub writes stay minimal.
4. **MultiMeters bar animations:** which of rank slide, enter and leave, or change pulse does the owner
   mean? *Recommendation:* file the draft with all three as candidates and let triage choose. The
   rank-change slide is the likely intent.
5. **MultiMeters Insights:** is it allowed to compute between pulls without persisting anything, given
   scope.md's no-persist rule? *Recommendation: yes*, from the client's sessions only. A history store
   would be a scope change for the owner to rule on separately.
6. **The anchor-width tracker:** one LibKa0s issue with a checklist, or one issue per addon?
   *Recommendation: one LibKa0s tracker* (see above).
7. **The toast stack's library half:** a LibKa0s issue now, or later? *Recommendation:* as in
   `I_DROPWATCHER.md`, file the DropWatcher issue now and the LibKa0s-Toast minor 2 issue when it is
   scheduled.
8. **Spacing:** the bulk filing is six writes (five issues and one comment). Space them out (memory: throttle
   GitHub writes).
