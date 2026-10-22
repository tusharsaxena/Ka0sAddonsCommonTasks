# Owner scope and binding decisions — LibKa0s issues #45–#58

Run branch, in every repo touched: `feat/2026-10-22-libka0s-issues-45-58`. Created 2026-10-22.

The owner asked for every open LibKa0s issue from #45 onwards to be addressed: changes in LibKa0s and
WowAddonStandards, a re-vendor into every roster addon (QuickComms included), and adoption in each addon.
The library bar is **very high**. Items marked *owner* were answered by the owner on 2026-10-22. Items marked
*lead* were decided by the session lead under the owner's standing instruction ("use your best judgement,
ask only when absolutely necessary"). Every *lead* item is binding on the executors as well.

## A. Verdicts per issue

| Issue | Verdict | Source |
|---|---|---|
| #45 dead test-seam exports | Remove `O.__releaseChrome` (OptionsTabs minor 9) and `Kit.__deviationRows` / `Kit.__declineFor` (kit revision) | lead |
| #46 + #47 complexity runner | Fix in kit 41. A lizard crash or bound means complexity `fail`, `CCN_*` zero, parity skipped, and a separate `crashed` bucket from a per-file retry that names the file; `fld` is numeric; stderr stays out of the parse. No `S.forInFunctionLiterals` detector and no shadow rewrite (both rejected, triggers recorded). The note carries the static hoist hint. | lead |
| #48 test-mode strip | **Promote `W.TestStrip`** into Widgets; adopters LootHistory, BankLedger, MultiMeters, DropWatcher | owner |
| #49 chat sender, tooltip reader, loot parser, restriction tracker (+ the four restriction readers, the GlobalString pattern compiler) | Reject all; close with census and triggers | lead |
| #50 grid composer | Reject; close | lead |
| #51 item read | **Promote `Item.BonusIDsFromLink`** (Item minor 3; adopters BankLedger, LootHistory). Reject the other functions (LinkDetail/BetterLink, IdentityKey/SameItem, EffectiveItemLevel, ItemLevelAt/QualityAt, QualityOf, Wowhead URL builder) and the loot parser | owner (promotion) / lead (rest) |
| #52 flat widgets | **Promote `W.SearchBox`** (adopters LootHistory, BankLedger, DropWatcher; gold focus line for all). Reject `W.Checkbox` and a published flat skin | lead |
| #53 step panel | Accept as Sim-1.0's panel (see C) | owner (via #54) |
| #54 Sim-1.0 | **Accept.** The owner wants new simulators **built in this run in LootHistory and BankLedger** on Sim-1.0; DropWatcher migrates onto it and drops its generic copy. MultiMeters#60, WhatGroup#24 and KickCD#38 stay open, `state:triaged`, repointed at Sim-1.0 | owner |
| #55 icon attribution | Standard rule (documentation-§1 credits: MUST for `gi:`, SHOULD for the MIT sets actually shipped) + README credits in each addon at re-vendor. No in-game helper (QuickComms already credits) | lead |
| #56 icon style + glow | **Promote `LibKa0s-Glow-1.0`** (stateless LibCustomGlow driver; adopters DropWatcher, QuickComms, KickCD). Reject IconStyle, the lifecycle/signature layer, published defaults and catalogs, `O.GlowGroup` and the LSM "Solid" registration | owner (promotion) / lead (rest) |
| #57 icon subset | Release v1.75.0 with kit 40 + prune tool; every addon declares `LibKa0s icons:` and prunes at re-vendor | lead |
| #58 key bindings | **launcher-§6 MUST** for Show-window addons; implemented in BankLedger, LootHistory, MultiMeters, DropWatcher, WhatGroup; QuickComms already complies in shape. No LibKa0s helper; kit check deferred | owner (MUST) / lead (rest) |

## B. Release shape (lead)

- **One LibKa0s release, v1.75.0**, carrying: kit 40 (already merged), #45, kit 41 (#46/#47 plus #45's kit
  half), the stale icon comments (Core / DebugLog / OptionsIdList, **with** minor bumps), `W.SearchBox` and
  `W.TestStrip` (one Widgets minor), the step panel, `LibKa0s-Glow-1.0`, `LibKa0s-Sim-1.0`, `Item.BonusIDsFromLink`,
  and one DebugLogDiagnostics minor adding both new majors to its MAJORS list.
- **The tag is local-only and movable until the owner approves the merge** (the 2026-10-07 run's v1.71.0
  precedent). If building DropWatcher's migration or the LootHistory/BankLedger simulators exposes a gap in
  Sim-1.0, the fix lands **additively** in LibKa0s on the run branch, the local tag is moved, and the affected
  addons re-vendor (an `RV2` refresh item per addon). The tag is pushed only at finalize, on the owner's go-ahead.
- WowAddonStandards ships **one** version, v2.86.0. Later WS items append to its changelog entry.

## C. Sim-1.0 and the step panel (lead, from the design challenge)

The design is `inputs/design-sim.md`, with these fixes binding over it:

1. `ready()` is bound to the session that issued it. A stale `ready` (after restart, or stop then start) is ignored.
   Stop is re-entrancy-safe (a stop inside Fire→deliver, or a second stop, is a no-op).
2. RunTo shares Run's `playing` slot: Run answers "playing", Pause cancels a pending RunTo poll, Stop cancels it. Tested.
3. `DeliverForCleanup` keeps DropWatcher's stood-down check (answers 0 while stood down).
4. Host members never hang on the library instance. The host keeps its own table (e.g. `NS.SimHost`) for
   host fields (`Status` extras, `HistoryLog`, `MarkGUID`, `SetRestriction`, …). This is written into the host contract.
5. The step panel re-pins its height bounds itself (a guarded `SetResizeBounds`) when the row count changes. No Core API change.
6. **Order:** build the step panel, then rebuild PerfPanel on it as a spike, **before** any Sim file. If
   `test_perf_panel.lua` passes unedited, `W.StepPanel` is public (Perf + Sim = two consumers). If it does not, the
   step panel is **Sim-private** (library-internal, no public contract) and PerfPanel stays untouched, with the
   deliberate duplication noted at both copies.
7. Scope cuts: no `seam:IsActive`, no `seam:IsGuarded`, no `help` verb, one `Live` (on the seam), `RunTo`
   Sim-internal, no StepPanel `place`/`onDragStop`, no `d.panel.button`/`d.panel.tooltip` (DropWatcher takes the
   library's default button and GameTooltip; its visible line changes such as the Restart stop line and the
   unknown-scenario line are accepted and go on the smoke list).
8. A second `SetProvider` for a key that already has one raises an error. `Live` re-raises the original error
   value and logs the traceback to the debug sink. No `__newindex` auto-wrap: the seam exposes `Unwrapped()`
   and every host suite asserts it is empty.
9. The restriction / chat-lockdown simulation stays host code (DropWatcher).
10. The DropWatcher contract proof: DW's sim suites are ported to the library API; edits are limited to call sites
    that moved, and every behavioural assertion is kept. Lines the library now owns are asserted in the library.
11. The simulators are slash-only (`/<slash> sim …`), with no launcher entry and no key binding (DW precedent).
    The step delay is a fixed constant (no schema row). The panel position is **session-only**, so a simulation
    writes nothing to SavedVariables.
12. LootHistory: a deterministic fixture world; stop on real interference (a real loot line, a loot or interaction
    frame, trade, a quest turn-in, an encounter); row Delete, purge, ledger reset, Forget and the retention prune
    are refused during a simulation; ledger scenarios refuse when `trackLedger` is off. The Timeline takes an
    optional host `gate()` predicate (the Reconciler settle), checked before each step.
13. BankLedger: `/bl purge` is refused during a simulation ("stop the simulation first"). A profile reset does not end
    a simulation. `Compat.PlayerName`/`PlayerClass` are justified in its `docs/compat-layer.md`. The warband-tab
    deposit event sequence on 12.1.5 is an in-client check on the owner's smoke list; the driver data is built
    from the best documented knowledge.

## D. TestStrip (lead)

Design: `inputs/design-strip.md`, with these changes binding:
- The public surface is the constructor plus `HEIGHT` and `strip.text`. There is no `RESERVE`. `fill` and `icon` are stored as `__fill` / `__icon`.
  Its art (`info`) is host-passed, the way Widgets takes all art, so it is a host-declared icon and not library-drawn.
- One Widgets minor carries SearchBox and TestStrip.
- LootHistory and BankLedger keep their red title badge alongside the strip; MultiMeters keeps its title marker and session-line word.
- MultiMeters: a narrow `ApplyTestStrip` on toggle, never the full ApplyConfig. The strip has no tooltip. At minimum height the strip
  takes a row. A window that is minimised with its header hidden is the rule's carved-out collapsed state.
- Wording: LH "TEST MODE: a sample loot history, not yours. Combat ends it."; BL "TEST MODE: a sample ledger, not
  your bank. Combat ends it."; MM "TEST MODE: placeholder numbers, not your fight." (verify MM's ending condition; add the clause only if it is true).

## E. Glow-1.0 (lead)

Design: `inputs/design-glow.md`, with these binding:
- `Start(frame, style, knobs, key, frameLevel)`. Colour lives in `knobs`. `pixelBorder` and `procStartAnim` are coerced `~= false`.
- No `STYLES` member is published. A nil-style `Stop` stops every style.
- `tests/run.lua` lists `test_glow`. The fake LCG's ProcGlow_Start calls setmetatable, as the real one does.
- Order in the XML and majors list: after Item. No new anti-pattern sentence for the fork.

## F. The standard, v2.86.0 (lead)

Design: `inputs/design-std.md`, with these binding:
- The `__` clause is **narrowed**: a `__` member documented as internal or as a test seam, with zero roster consumers, may be removed with a
  minor bump. Documented `__` members that consumers call (`__PatchLSM30Border`, `__IsCombatLocked`, `__AttachCompose`,
  `__panels`, …) remain contract.
- The closed library-drawn icon set stays **close, copy, clear, info** (the `info` is OptionsIdList's). TestStrip and step-panel art is
  host-passed. Drop the "adding a name is a major decision" sentence.
- launcher-§6: the key press MUST call the same handler as the Show window entry and the slash toggle, and so refuses
  exactly as that toggle does. The by-hold refusal stays the SHOULD it already is in slash-commands-§7. Don't enumerate addons in the
  section body. **QuickComms' perf-hold line is fixed in this run** (V.TogglePads must not print the disabled line under the perf hold alone).
- preview-mode marker rule: it covers the explicit Test mode only, not unlock-to-preview. WhatGroup's "Test Group — …" content counts as its marker.
- automated-tests-§3: a crashed or bounded lizard run is not a complexity pass (a clarification, with `crashedFiles` as a parenthetical, not a gate term).
- Sim-1.0 and Glow-1.0 adoption is *required of none* (the Compat/Bus/Schema precedent). The named adopters adopt in this run.
- Recorded rejections go where library-stack-§7 says (open-evolutions).

## G. Addon-side extras (lead)

- QuickComms: fix the perf-hold refusal (F).
- LootHistory: fix the options-ui-§19 Price-sources OnRelease defect in this run (the repo is being touched anyway).
- File as new issues, not fixed here: DropWatcher bonus-hole modifier offset (core/ItemRead.lua:55-57); DropWatcher restriction edge lacking the combat flag.
- Delete the dead `O.__releaseChrome` mirrors from addon Options stubs at re-vendor (KickCD M4-09 precedent).
- MultiMeters: the test marker must not vanish when the header is hidden (the strip fixes it).
- LootHistory/BankLedger: route the "TEST MODE" badge text through L.

## H. Execution rules (owner)

- Work on the run branch in every repo, commit incrementally (`<ID>: …`), push feature branches at milestone checkpoints,
  never merge without the owner's go-ahead. At the end, after merging: delete every branch, stash and worktree this run created.
- In-client smoke tests are the owner's; never mark one passed.
- Use the bounded runner for heavy batteries. Never edit an addon's `libs/` or `tests/_kit/` except in a re-vendor item.
- The game loads `GIT/<Addon>` through a symlink, so never test from a side worktree, and work in place.
- Space out GitHub writes (issue close, comment, create).
