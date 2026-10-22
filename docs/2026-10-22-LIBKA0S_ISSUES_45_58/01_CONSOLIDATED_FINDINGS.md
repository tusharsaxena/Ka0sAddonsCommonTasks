# 01 — Consolidated findings: one verdict per candidate

Source: the analysis workflow (`inputs/analysis-workflow.json`, 25 agents). Each issue cluster had one analyst, who censused all
14 roster addons, verified every consumer claim at file:line and judged it against library-stack-§7's three promotion bars. Each
also had one **high-bar challenger**, who re-verified the analyst's work and argued against putting the thing in the library. A
survey agent recorded every repo's vendoring state. Final verdicts combine that with the owner's answers of 2026-10-22
(`inputs/OWNER_SCOPE.md` §A).

**The bars** (library-stack-§7): (1) two or more consumers with the **same semantics**, (2) no per-consumer escape
hatches, (3) a stable abstraction, not a coincidence of today's code. The anti-frequency rule also applies: high
frequency combined with low semantic content stays inline.

Legend: **A** is the analyst's verdict, **C** the challenger's, **Final** the run's verdict.

## #45 — dead test-seam exports

| Candidate | A / C | Final | Evidence |
|---|---|---|---|
| `O.__releaseChrome` (OptionsTabs.lua:636) | fix / fix | **Remove**, OptionsTabs minor 9 | Zero callers in LibKa0s and in all 14 addons. Seven addon Options stubs mirror it as a no-op, and parity reads only live keys, so they stay green. They are deleted at re-vendor. |
| `Kit.__deviationRows`, `Kit.__declineFor` (framework.lua:913-914) | fix / fix | **Remove**, in kit 41 | No self-test calls either. The decline reader is pinned through fixtures in test_kit_inventory.lua. The comment claiming otherwise is false. |

The standard ripple: library-stack-§7's additive-only MUST says "never removed". The challenger showed that several `__` members are
documented and **called** by consumers (`__PatchLSM30Border` in 12 files, `__panels` in 26, `__AttachCompose` in 4, `__IsCombatLocked` in 1),
so the v2.86.0 clause is narrowed. A `__` member documented as internal or as a test seam, with zero roster consumers, may be removed in a
minor. One that consumers call remains contract.

## #46 + #47 — the complexity runner and lizard crashes

| Candidate | A / C | Final | Evidence |
|---|---|---|---|
| Treat a lizard crash or bound as a crash (exit status, footer shape, numeric `fld`, valid JSON) | fix / fix | **Fix**, kit 41 | Reproduced on master d9f9454. One crashing file made **every** file read blind (fine.lua included) and wrote `"warnings": str` into manifest.json. |
| A separate `crashed` bucket from a per-file retry that names the file | fix / fix | **Fix**, kit 41 | "Blind" (lizard parsed the file but missed functions) and "crashed" (nothing was measured) need different remedies. |
| `S.forInFunctionLiterals` detector | reject / reject | **Reject** | The retry already names the file. The shape has occurred once in the collection's history (PGFE, since hoisted). |
| Rewrite the shape in the sighted shadow | reject / reject | **Reject** | Renaming `for` stops the crash but lowers the function's CCN by 1, so the gate would under-count. |
| automated-tests-§3 ripple | standard-only / accept-minimal | **Clarification** in v2.86.0 | A crashed or bounded run is not a complexity pass. The hazard row's facts are corrected (closes WowAddonStandards#8). `crashedFiles` is a parenthetical, not a new gate term. |

## #48 — the test-mode strip

| Candidate | A / C | Final | Evidence |
|---|---|---|---|
| `W.TestStrip` | defer / defer (only DropWatcher draws one) | **Promote**, owner | The owner wants the strip in Loot History, Bank Ledger and Multi Meters, which makes four consumers with the same semantics. The surface is cut to the constructor, `HEIGHT` and `strip.text`. Art is host-passed. |
| A shared tone/colour table | reject / reject | **Reject** | No such table exists. DropWatcher's tones are semantic to its drop tables, and other addons give the same names other meanings. |
| A test mode must say so on the display | standard-only | **v2.86.0 MUST** (preview-mode) | Five addons, five ad-hoc styles. Multi Meters' marker vanishes when its header is hidden (Window_Header.lua:344). |

## #49 — Drop Watcher promotion candidates (and #51 item 2)

| Candidate | A / C | Final | Why |
|---|---|---|---|
| Chat sender (`Compat.ChatSender`) | reject / reject | **Reject** | Two consumers, but the content is one presence guard. The deprecated-global rung can never run on 12.x. Trigger: Blizzard reshapes the send API again. |
| Tooltip line reader + duration decoder | reject / reject | **Reject** | One consumer. Loot History's `ScanBound` scans differently (whole-line bind wordings, a `readable` flag). |
| Loot-line parser (DropWatcher vs Loot History) | reject / reject | **Reject** | The two disagree on **correctness**: Loot History counts crafted and refunded items as receipts, and DropWatcher rejects them. Trigger: a second every-looter consumer, with written agreement on receipt kinds. |
| Restriction tracker | reject / reject | **Reject** | Quick Comms now holds a second copy (the issue missed it). The two drifted the day it was taken, so the tracker fails bars 2 and 3. |
| The four restriction readers | defer / reject | **Reject** | They are guards, not readers, so every host keeps the full body as its stub. Their only consumers are a declared same-author copy. |
| GlobalString-to-pattern compiler (found by the census) | reject / reject | **Reject** | Three copies differ on positionals. Trigger: a non-enUS or positional break. |

## #50 — Options grid composer

| Candidate | A / C | Final | Why |
|---|---|---|---|
| `O.MixedGrid` | reject / reject | **Reject** | One consumer (DropWatcher's Situations table), which has since built its own raw-frame table. |
| Loot History Price-sources host lacks an `OnRelease` undo (found on the side) | fix / fix | **Fix in LH-01** | An options-ui-§19 MUST, latent today. |

## #51 — the item read

| Candidate | A / C | Final | Why |
|---|---|---|---|
| `Item.BonusIDsFromLink` | accept-minimal / defer | **Promote**, owner | Bank Ledger and Loot History share the same positional walk, and DropWatcher's LinkDetail does it too. |
| LinkDetail + BetterLink | reject / reject | **Reject** | Only DropWatcher merges two reports of one item. |
| IdentityKey / SameItem | reject / reject | **Reject** | Loot History and Bank Ledger deliberately key by base item id. |
| EffectiveItemLevel | reject / reject | **Reject** | Different non-gear rules: DropWatcher shows a level, Loot History answers nil. |
| ItemLevelAt / QualityAt | reject / reject | **Reject** | One consumer, and DropWatcher's simulator must route through NS.Compat. |
| QualityOf | reject / reject | **Reject** | Uncached-item policy, which Item-1.0 deliberately does not own (Loot History guesses, Bank Ledger refuses). |
| Wowhead URL builder | reject / reject | **Reject** | Presentation tied to a third-party URL scheme. With BonusIDsFromLink it is about five lines. |

## #52 — flat widgets

| Candidate | A / C | Final | Why |
|---|---|---|---|
| `W.SearchBox` | accept-minimal / accept-minimal | **Promote** | Three verified copies: Loot History, Bank Ledger (the issue missed it) and DropWatcher. All adopters get the gold focus line. `opts.icon` serves Bank Ledger's magnifier. |
| `W.Checkbox` | reject / reject | **Reject** | No consumer. DropWatcher deleted its only flat checkbox five hours after drafting the issue. |
| A published flat skin / `W.Button` | defer / reject | **Reject** | Four lines of backdrop calls: the anti-frequency case. |

## #53 + #54 — step panel and Sim-1.0

The analysis and challenge said **defer**: DropWatcher had the only simulator, and the five "adopter" issues were templated in one
two-minute batch. **The owner then chose to build simulators in Loot History and Bank Ledger in this run.** With DropWatcher, that
makes three hosts, so the promotion is decided now (owner). The library API was designed against all three hosts' requirements
(`inputs/req-*-sim.md`, `inputs/design-sim.md`), and the design challenger's eight blocking findings were folded in as
OWNER_SCOPE §C.

- **The five safety rules "enforced by the library"** are rejected as a library guarantee. Only the refusals are computable there. The
  rest are host obligations, written as the host contract (H1–H10) and as the preview-mode simulator subsection.
- **The step panel** is built first. PerfPanel is then rebuilt on it as a spike. If PerfPanel's suite passes unedited, `W.StepPanel` is
  public, with two consumers, Perf and Sim. Otherwise it is Sim-private (OWNER_SCOPE C.6).
- **MultiMeters#60, WhatGroup#24 and KickCD#38** stay open and are repointed at Sim-1.0.

## #55 + #57 — icon subset and attribution

| Candidate | Final | Evidence |
|---|---|---|
| Release v1.75.0 with kit 40 and the prune tool | **Release** | Already merged at d9f9454. The tool parses with the gate's own functions. |
| Stale "missing art" comments in Core, DebugLog and OptionsIdList | **Fix**, with minor bumps | `Media.Icon` never looks at the disk, so an undeclared icon draws **blank**. It does not fall back. |
| Per-addon declarations, the prune and the consumer tests | **Every RV item** | Grepping for `Media.Icon(` alone finds nothing. Every addon draws through a seam (`NS.Icon`, `KCM.Icon`, data tables, constants). The declarations were derived per addon with file:line evidence. The provenance paragraphs in Loot History and Panel Master must be split for the gate to parse them. |
| README credit per shipped set | **v2.86.0** (documentation-§1): MUST for `gi:`, SHOULD for Open Iconic and Phosphor | No .pkgmeta strips the license files. Quick Comms already credits in its README and in its icon browser's tooltip. |
| An in-game credit helper | **Reject** | Quick Comms already credits through `Media.IconAuthor`. |
| Closing the library-drawn icon set | **v2.86.0** | close, copy, clear, info. TestStrip and step-panel art is host-passed. |
| A kit check of resolved icons against the declaration | **Defer** | Trigger: the first blank-icon report after the sweep. |

## #56 — icon style and glows

| Candidate | A / C | Final | Why |
|---|---|---|---|
| Stateless LibCustomGlow driver | defer / defer | **Promote** as `LibKa0s-Glow-1.0`, owner | DropWatcher, Quick Comms and KickCD map knobs to LCG arguments identically, with the same traps (pixelLength 0 → nil, pixelBorder a boolean). `Start(frame, style, knobs, key, frameLevel)`, soft-resolved at call time. |
| IconStyle (Config/ApplyIcon/PaintBorder/PaintRing) | reject / reject | **Reject** | Every host means something different by it. Only a one-line crop is shared. |
| Published GLOW_STYLES / GLOW_KNOBS | defer / reject | **Reject** | The hosts disagree on defaults, key spelling and kind vocabulary. |
| Glow lifecycle / signature no-op | reject / reject | **Reject** | Three different change keys and target-frame rules. |
| `O.GlowGroup` | reject / reject | **Reject** | No canonical glow block in options-ui. |
| LSM "Solid" registration | reject / reject | **Reject** | One line in four addons: anti-frequency. |
| LibCustomGlow row in library-stack-§2 | standard-only | **v2.86.0** | Three addons vendor it, but the standard does not list it. |

## #58 — key bindings

| Candidate | Final | Why |
|---|---|---|
| launcher-§6 | **MUST**, owner | A `CLICK <Folder>Toggle<Window>:LeftButton` binding on a hidden, non-secure button, calling the **same** handler as the Show window entry and the toggle verb, so it refuses exactly as the toggle does. No default key. Implemented in Bank Ledger, Loot History, Multi Meters, DropWatcher and WhatGroup. Quick Comms already complies in shape, and its perf-hold refusal is fixed (QC-02). |
| A LibKa0s helper | **Reject** | About six lines. `Bindings.xml` has to stay per-addon anyway. |
| A kit check | **Defer** | ADDONS.md is not vendored, so the audit catches the miss more reliably. Trigger: three addons ship identical static binding tests. |

## Found outside the issues

| Finding | Disposition |
|---|---|
| Loot History options-ui-§19 Price-sources undo | Fixed in LH-01 |
| DropWatcher bonus-hole modifier offset (core/ItemRead.lua:55-57) | Filed as a DropWatcher issue (DW-11) |
| DropWatcher restriction edge lacking the combat flag | Filed as a DropWatcher issue (DW-11) |
| Quick Comms prints the disabled line under the perf hold alone (breaks slash-commands-§7) | Fixed in QC-02 |
| Multi Meters' `Compat.ChatSender` comment claims "exactly one consumer" | Corrected in MM-04 |
| Every v1.71 addon's Options stub lacks `Drawer` (v1.73.0 parity churn) and its kit 39 `__fireUnconditional` cases may go red for real reasons | Fixed in each RV item |
