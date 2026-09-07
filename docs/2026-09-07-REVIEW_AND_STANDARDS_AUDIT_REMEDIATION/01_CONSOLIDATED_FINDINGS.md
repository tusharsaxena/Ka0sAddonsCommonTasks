# 01 — Consolidated Findings

**207 surviving triaged findings across 10 repositories, in 39 clusters.**

> **Nothing in this bundle has been executed.** Not one line of any repository has changed. Every
> sentence below describes work that is *proposed*. Where a remedy is written in the imperative, it is
> an instruction to a future change, not a report of a past one. No branch exists, no tag has been cut,
> no re-vendor has happened, and every suite named here is green today at the numbers the per-repo
> bundles recorded.

The inputs are the twenty frozen per-repo bundles under `docs/reviews/2026-09-07/` and
`docs/audits/2026-09-07/` in each of the ten repositories, triaged against the code as it stands on
2026-09-07, plus four cross-cutting passes over the collection held as a whole.

---

## How to read this

| Column | Meaning |
|---|---|
| **Repo** | Which repository the finding is against. |
| **ID** | Stable consolidated id. `<REPO>-R-nn` = review bundle, `<REPO>-A-nn` = audit bundle. |
| **Src** | `R` = `docs/reviews/2026-09-07/`, `A` = `docs/audits/2026-09-07/`. |
| **Sev** | **Triaged** severity — reachable impact, not the strength of the rule broken. `†` marks a row whose grade, count or evidence moved in triage; the move is stated under the table. |
| **Locus · evidence** | The `file:line` the finding anchors to, re-opened during triage, followed by what was found there. Paths are relative to the repo. |
| **Rule** | The `filename-§N` section, where one applies. `—` means no rule was violated: the finding is a defect, or hygiene no section governs. |
| **Remedy** | The proposed change, in one sentence. Proposed. |

**Severity rubric.** Critical = a shipped, always-on player-facing control does nothing, or data loss,
taint propagation or a failure to load. High = a player, their SavedVariables or their session can
reach it today. Medium = real but narrow, self-correcting, or an integrity gap in the record rather
than in shipped behaviour. Low = developer-facing, config-only, or unreachable in any shipping
configuration.

**Section references** use `filename-§N`. Where a bundle cited a number the file does not carry, the
bare filename is used and the discrepancy is carried by C14.

**Coverage caveat, stated up front.** Three repositories in the collection received **neither a review
nor an audit** on 2026-09-07: `WowAddonStandards`, `wow-addon` and `Ka0sAddonsCommonTasks`. A `find`
over all three returns no `reviews/`, no `audits/` and no `docs/automated-tests/` directory of any
date. That matters more than it looks. `WowAddonStandards` is the normative source every audit finding
below cites, and two clusters (C16, C25) plus `LIBKA0S-R-15` and `LIBKA0S-A-14` are filed *against* it
with no audited baseline for the repo receiving the work. `wow-addon/agents/review.md` (321 lines) and
`WowAddonStandards/AUDIT.md` (515 lines) drove all twenty passes, so a defect in either was reproduced
twenty times and reviewed zero times. Both are docs-only, which is presumably why they were skipped;
the standard's own text is nevertheless exactly what an audit exists to check.

---

## Severity × repo

| Repo | Critical | High | Medium | Low | Total | Rejected |
|---|---|---|---|---|---|---|
| AbsorbTracker | 0 | 0 | 2 | 20 | **22** | 1 |
| BankLedger | 0 | 1 | 2 | 11 | **14** | 2 |
| ConsumableMaster | 0 | 0 | 1 | 20 | **21** | 2 |
| KickCD | 0 | 1 | 0 | 20 | **21** | 0 |
| LootHistory | 0 | 0 | 4 | 20 | **24** | 0 |
| MultiMeters | 0 | 1 | 5 | 16 | **22** | 2 |
| PanelMaster | 0 | 0 | 3 | 13 | **16** | 2 |
| PrettyChat | 0 | 2 | 1 | 15 | **18** | 5 |
| WhatGroup | 0 | 0 | 2 | 23 | **25** | 2 |
| LibKa0s | 1 | 0 | 5 | 18 | **24** | 8 |
| **Total** | **1** | **5** | **25** | **176** | **207** | **24** |

One Critical (`LIBKA0S-A-01`) and five Highs: `BANKLEDGER-R-02`, `KICKCD-R-01`, `MULTIMETERS-R-01`,
`PRETTYCHAT-R-01`, `PRETTYCHAT-R-02`. Everything else is Medium or below, which is the honest shape of
a collection that has been through this cycle twice before. The Critical is a three-line library
defect; the Highs are five unrelated local ones.

Twenty-four bundle items did not survive triage and are not in the 207. They are in Part 3, with the
reason each was dropped.

## Clusters

Thirty-nine clusters. A cluster is one problem seen from one or more repositories; clusters touching
three or more repos are marked **[COLLECTION]** in their heading. Eight `CX*` clusters came out of
holding all ten bundles at once and are in Part 1. Two of them — `CX01` and `CX02` — carry **no
per-repo finding at all**, because no single-repo pass was in a position to state them; two more,
`CX05` and `CX06`, are aggregates that a single repo caught one corner of.

| Cluster | Title | Sev | Repos | Findings | Disposition | Effort |
|---|---|---|---|---|---|---|
| `C01` | Composed media dropdowns hand the flow engine a closure | Critical | 2 | 3 | `libka0s-upstream` | S |
| `C02` | LSMPatch mutates AceGUI's process-global widget registry | Medium | 5 | 2 | `libka0s-upstream` | M |
| `C03` | Migration runners gated on the wrong storage scope | High | 2 | 4 | `per-addon` | M |
| `C04` | MultiMeters feign-trace subsystem: unconditional allocation, blind spots, no coverage | High | 1 | 8 | `per-addon` | M |
| `C05` | estimateRecordBytes truncates on a nil field, with a test that cannot fail | Medium | 1 | 2 | `per-addon` | S |
| `C06` | PrettyChat stores a player-entered format with no conversion-signature check | High | 1 | 1 | `per-addon` | M |
| `C07` | Landing-page logo rides AceGUI's pooled SimpleGroup | High | 1 | 1 | `per-addon` | M |
| `C08` | Automated-test records stale in every repo | Low | 10 | 25 | `per-addon` | XL |
| `C09` | Shared test-kit runner drops the skipped count and mis-renders release rows | Low | 5 | 8 | `libka0s-upstream` | M |
| `C10` | Working-tree line endings disagree with the CRLF pin in all ten repos | Low | 10 | 12 | `mixed` | M |
| `C11` | .pkgmeta ignore lists diverge; dev bytes reach players | Medium | 7 | 7 | `per-addon` | S |
| `C12` | Tab-strip geometry cannot be tested: the shared mock answers GetHeight 0 | Low | 5 | 4 | `libka0s-upstream` | M |
| `C13` | Perf-panel decorate hook re-draws the library's own close button | Low | 3 | 2 | `per-addon` | S |
| `C14` | Deviation registers cite dead IDs, spent triggers and unratified decisions | Low | 7 | 11 | `per-addon` | M |
| `C15` | README and ARCHITECTURE structure against documentation-§1/§3 | Low | 5 | 8 | `per-addon` | M |
| `C16` | documentation-§3 names three tiers; every repo needs a fourth table | Low | 2 | 2 | `standards-upstream` | S |
| `C17` | British spellings ship, and the prose gate that should catch them is a six-word list | Low | 4 | 5 | `mixed` | M |
| `C18` | Localization routing gaps: unwrapped strings and missing locale keys | Low | 4 | 4 | `per-addon` | M |
| `C19` | Comments and rationales describing code that has moved or gone | Low | 8 | 13 | `per-addon` | M |
| `C20` | Dead exports, dead arms and hand-copied helpers | Low | 5 | 7 | `per-addon` | S |
| `C21` | Tests that assert less than their names claim | Low | 6 | 9 | `per-addon` | M |
| `C22` | layout-§1's 1500-LOC cap breached in four repos, and unclassified for a library | Low | 5 | 6 | `mixed` | L |
| `C23` | LibKa0s tab strip creates frames per click and pools none | Medium | 1 | 2 | `libka0s-upstream` | M |
| `C24` | LibKa0s options and perf seam defects | Medium | 1 | 4 | `libka0s-upstream` | M |
| `C25` | Standards text out of date about LibKa0s, and LibKa0s out of date about the standard | Low | 1 | 2 | `standards-upstream` | S |
| `C26` | performance-§12 exemption pages no longer reproduce their own evidence | Medium | 4 | 5 | `per-addon` | M |
| `C27` | Allocation and hot-path nits, plus perf ceilings that no longer bound anything | Low | 6 | 8 | `per-addon` | M |
| `C28` | Stored values reaching APIs unvalidated, and session state left behind | Low | 5 | 8 | `per-addon` | M |
| `C29` | Event and lifecycle gaps: state read at the wrong moment | Medium | 4 | 7 | `per-addon` | M |
| `C30` | Settings-panel shape deviations against options-ui | Medium | 6 | 8 | `mixed` | L |
| `C31` | Naming, lint config and vendored-payload hygiene | Low | 5 | 8 | `per-addon` | S |
| `CX01` | KickCD ships empty Font, Border and Bar-texture dropdowns; three siblings each hand-rolled a private fix *(aggregate)* | High | 5 | 0 | `mixed` | M |
| `CX02` | Nine hand-maintained LibKa0s-absent stubs, no library-published no-op surface *(aggregate)* | Medium | 10 | 0 | `libka0s-upstream` | L |
| `CX03` | SetRenderer adoption is uneven, so the combat guard is missing exactly where pages were hand-wired | Medium | 3 | 1 | `per-addon` | M |
| `CX04` | toc-file-§5's per-line load-bearing MUST is satisfied in no repo | Low | 9 | 3 | `mixed` | L |
| `CX05` | Every .luacheckrc excludes tests/, so half the collection's Lua is never linted *(aggregate)* | Medium | 10 | 1 | `per-addon` | M |
| `CX06` | lib.MakeCloseButton's third argument forces the same wrapper into eight repos and two declines *(aggregate)* | Low | 10 | 1 | `libka0s-upstream` | M |
| `CX07` | Tier-2 topic docs missing where their triggers have fired | Low | 5 | 3 | `per-addon` | L |
| `CX08` | Shared icon catalog bypassed by hard-coded Blizzard texture paths | Low | 8 | 2 | `per-addon` | M |

---

# Part 1 — What only the collection view produced

These eight are the reason this consolidation exists. `CX01` and `CX02` have no underlying per-repo
finding at all: each is a property of the set, invisible from inside any one repo. `CX05` and `CX06`
are the same shape, caught from one side only — LibKa0s filed the lint exclusion against its own
`.luacheckrc` and BankLedger filed the close button against its own decline, and neither could see that
ten repos and eight wrappers were doing the same thing. The remaining four each carry one to three
per-repo findings that saw a corner of something larger.

Three of the eight change a disposition rather than adding work. `CX04` and `CX05` in particular ask
ten repositories to do something the standard's own text does not require — see
`02_UPSTREAM_CHANGES.md`, which routes both upstream instead.

## CX01 · KickCD ships empty Font, Border and Bar-texture dropdowns; three siblings each hand-rolled a private fix — **aggregate**, 5 repos **[COLLECTION]**

Four addons consume the LibKa0s media composers. AbsorbTracker, ConsumableMaster and MultiMeters each independently discovered C01 and wrote their own values rewrite (fixMediaValues, two separate lsmValues). KickCD's AddComposed copies a stamp onto each row and never touches values, so its Label, Icons and Castbar media dropdowns render empty in game.

Only four addons call the media composers. `AbsorbTracker/settings/Appearance.lua:114-137` (`LSM_KIND` + `fixMediaValues`, three call sites at `:181`, `:237`, `:257`), `ConsumableMaster/settings/MacroBar.lua:121-123` (`lsmValues`, three row overrides) and `MultiMeters/settings/Schema.lua:607` each wrote their own rewrite; all three comments state an end condition, and ConsumableMaster's at `:118` names LibKa0s issue #15. KickCD wrote none: `Helpers.AddComposed` (`settings/Panel.lua:191-197`) stamps host fields onto every returned row and never touches `values`, so eight composed rows render empty in game — `settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`, `settings/Label.lua:184`. The upstream fix repairs all eight with no KickCD code change, which is why KickCD is the proof the fix landed.

*Repos* KickCD, AbsorbTracker, ConsumableMaster, MultiMeters, LibKa0s · *disposition* `mixed` · *effort* M · *cluster severity* High

No single-repo finding carries this. It exists only because all ten bundles were held at once.

## CX02 · Nine hand-maintained LibKa0s-absent stubs, no library-published no-op surface — **aggregate**, 10 repos **[COLLECTION]**

Every addon carries its own settings/OptionsSetup.lua degraded arm mirroring the LibKa0s-Options surface — 185 to 384 lines each, 12 to 56 stub members, all hand-written. The library publishes no canonical no-op surface, so the nine drift: only AbsorbTracker, ConsumableMaster and KickCD have a parity test, and AbsorbTracker's stub omits SetRenderer outright.

Verified stub sizes: AbsorbTracker 369 lines, MultiMeters 384, KickCD 351, PrettyChat 265, WhatGroup 258, BankLedger 230, PanelMaster 217, LootHistory 199, ConsumableMaster 185 — nine hand-written `settings/OptionsSetup.lua` degradation arms. Only AbsorbTracker, ConsumableMaster and KickCD carry a `tests/test_surface_parity.lua`; the other six have nothing checking the stub against the live surface, which is how AbsorbTracker's stub can omit `SetRenderer` (CX03) with every suite green.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, LibKa0s · *disposition* `libka0s-upstream` · *effort* L · *cluster severity* Medium

No single-repo finding carries this. It exists only because all ten bundles were held at once.

## CX03 · SetRenderer adoption is uneven, so the combat guard is missing exactly where pages were hand-wired — 1 finding, 3 repos **[COLLECTION]**

O.SetRenderer owns the Blizzard-sidebar combat refusal. Eight addons route through it; AbsorbTracker has zero callers and three settings pages on a raw OnShow, and KickCD (Profiles, Spells) and MultiMeters (Profiles) each keep pages off it too. Those pages document a combat refusal they do not deliver.

`O.SetRenderer` (`LibKa0s/Options.lua:695`) is where the Blizzard-sidebar combat refusal lives, inline at `:700-716`. A grep over each repo's `core/` and `settings/` outside `OptionsSetup.lua` returns: AbsorbTracker 0 files, BankLedger 1, LootHistory 1, PrettyChat 1, WhatGroup 1, PanelMaster 2, KickCD 4, ConsumableMaster 5, MultiMeters 9. AbsorbTracker is the only zero, and it is the repo whose own `docs/settings-panel.md:278-285` documents the refusal.

*Repos* AbsorbTracker, KickCD, MultiMeters · *disposition* `per-addon` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-04` | R | Medium † | `settings/General.lua:283, settings/Appearance.lua:320, settings/Profiles.lua:57` — Each calls panel:SetScript("OnShow", ...) directly; grep finds no O.SetRenderer caller outside libs/. Guard lives at Options.lua:695-716. | `options-ui-§11` | Move all three page bodies onto Helpers.SetRenderer, drop their own EnsureDefaultsButton call, add SetRenderer to the degradation stub. |

**† Regraded or corrected in triage.** `ABSORBTRACKER-R-04` — held at medium: docs/settings-panel.md:278-285 documents a combat refusal the Blizzard-sidebar path does not deliver, and that is the path a player takes mid-fight.

## CX04 · toc-file-§5's per-line load-bearing MUST is satisfied in no repo — 3 findings, 9 repos **[COLLECTION]**

The rule requires every load-bearing TOC line to carry a comment naming what resolves at load. Across nine TOCs listing 23 to 81 files each, the annotation appears 1 to 4 times per file. A MUST that every addon violates identically is a sign the rule as written is unworkable at that granularity.

The rule as written binds narrowly. `toc-file.md:144` reads "A line whose position is **load-bearing MUST** carry a comment saying so, at the line, naming **what resolves at load**" — not every line. Measured against that denominator these are roughly eight one-line additions, and `AbsorbTracker.toc:39-40` is already a compliant instance. What is near-universally unmet is `toc-file.md:147`'s *conventional* SHOULD, once per group. See `02_UPSTREAM_CHANGES.md` — the cluster's own disposition is the thing being corrected, not the repos.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup · *disposition* `mixed` · *effort* L · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| KickCD | `KICKCD-A-02` | A | Low | `KickCD.toc:55 (core\PerfSetup.lua), KickCD.toc:73 (settings\OptionsSetup.lua)` — Four modules take `local Perf = NS.Perf` at file scope; four settings files take `local Helpers = NS.Settings.Helpers` | `toc-file-§5` | Add a LOAD-BEARING comment above each line naming what resolves, in the shape KickCD.toc:42-45 already uses |
| PrettyChat | `PRETTYCHAT-A-01` | A | Low † | `PrettyChat.toc:40,57` — core/Util.lua:14 reads NS.Const.Color at file scope; settings/Panel.lua:22 reads NS.Helpers at file scope. Both positions load-bearing, unannotated. | `toc-file-§5` | Add one at-line comment per position naming the symbol and its publisher, in the shape PrettyChat.toc:28-35 already uses. |
| WhatGroup | `WHATGROUP-A-02` | A | Low | `WhatGroup.toc:44,47,53-56` — Those lines carry only group headers; DebugLogSetup reads NS.FONT_MONO at file scope and Panel.lua:204 calls Helpers.MasterControls at load. | `toc-file-§5` | Add one comment per load-bearing line naming what must already resolve, plus a conventional note on each remaining group. |

**† Regraded or corrected in triage.** `PRETTYCHAT-A-01` — Line 43 dropped: core/CoreSetup.lua:38 does NS.Util = NS.Util or {}, so it self-initializes and its TOC position is not load-bearing.

## CX05 · Every .luacheckrc excludes tests/, so half the collection's Lua is never linted — **aggregate**, 10 repos **[COLLECTION]**

All ten repos exclude the whole tests/ tree from luacheck. That is 308 tracked test .lua files against 329 source files — the clean-lint claim in every RESULTS.md covers roughly half the code. Only tests/_kit/ is genuinely redundant.

Counted over `git ls-files '*.lua'` in all ten repos, excluding `libs/` and `tests/_kit/`: **329** source files against **308** test files. Every `.luacheckrc` excludes the whole `tests/` tree, so each repo's clean-lint claim covers a little over half its Lua. But `lint.md:11` ships that exclusion *as the template* and `lint.md:32` states it normatively — the addons are complying, and flipping them one at a time turns 308 files red at once. This is a standards amendment with LibKa0s as the pilot, not ten repos of work.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, LibKa0s · *disposition* `per-addon` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LibKa0s | `LIBKA0S-R-09` | R | Low † | `.luacheckrc:4` — exclude_files = { "tests/", "docs/" } excludes all 31 files under tests/; only tests/_kit/ is genuinely redundant with testkit/ | `lint` | Narrow the exclusion to tests/_kit/ and add a files["tests/"] stanza declaring LK_TEST rather than widening top-level read_globals |

**† Regraded or corrected in triage.** `LIBKA0S-R-09` — was medium; lowered to low. Review's "18 of 40" is wrong — the tracked total is 49 files, 31 of them under tests/.

## CX06 · lib.MakeCloseButton's third argument forces the same wrapper into eight repos and two declines — **aggregate**, 10 repos **[COLLECTION]**

The library takes addonName as a third argument rather than binding it, so eight addons publish a byte-identical three-line wrapper to curry it. BankLedger and LootHistory declined the library entirely and hand-rolled their own close buttons, giving one collection four visible close-button designs.

`lib.MakeCloseButton(parent, onClick, addonName)` is at `LibKa0s/Core.lua:234`. Eight consumers publish the same three-line currying wrapper — `AbsorbTracker/core/CoreSetup.lua:110`, `ConsumableMaster:155`, `KickCD:157`, `LootHistory:167`, `MultiMeters:238`, `PanelMaster:118`, `PrettyChat:111`, `WhatGroup:135`. **The cluster's "BankLedger and LootHistory declined" is one release stale:** `LootHistory/core/CoreSetup.lua:19-26` records the decline as *expired* at LibKa0s v1.10 and the repo now wraps at `:167`. BankLedger is the only live decline, reasoned at `core/CoreSetup.lua:117-129`. Total payoff of rebinding is roughly 24 lines against a signature change on a surface all nine vendor.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, LibKa0s · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| BankLedger | `BANKLEDGER-A-02` | A | Low | `core/CoreSetup.lua:117-125; modules/Browser.lua:98` — 'lib.MakeCloseButton IS DELIBERATELY NOT REPUBLISHED'; B:MakeCloseButton, 24x24, serves four title bars; no register row. | `standalone-windows` | Ratify with a standalone-windows register row and raise the section's MAY/MUST tension upstream; adoption would change four visible controls. |

## CX07 · Tier-2 topic docs missing where their triggers have fired — 3 findings, 5 repos **[COLLECTION]**

docs/compat-layer.md is absent in four repos that ship a real compat layer — MultiMeters most starkly at 761 lines and 31 shims — and docs/slash-dispatch.md is absent in three that ship subcommand trees. Only WhatGroup's and two other passes caught their own case; the pattern is collection-wide.

`docs/compat-layer.md` is absent where the trigger has fired hardest: MultiMeters ships 761 lines of `core/Compat.lua`, ConsumableMaster 83, WhatGroup 130 — none carries the doc, while BankLedger (175 lines), KickCD (496) and LootHistory (416) all do. MultiMeters at 761 lines and 31 shims is not a judgment call; the marginal three are, because `documentation.md:237` is the only Tier 2 trigger with no threshold — `docs/slash-dispatch.md` got "eight or more" at `:235` and `docs/message-bus.md` "more than ten" at `:238`.

*Repos* AbsorbTracker, ConsumableMaster, MultiMeters, PanelMaster, WhatGroup · *disposition* `per-addon` · *effort* L · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-02` | A | Low | `docs/ARCHITECTURE.md:324` — Row says "no subcommand tree"; PROFILE_VERBS at settings/Slash.lua:327 is dispatched at :386, and NS.COMMANDS:60 holds 17 verbs | `documentation-§3` | Write docs/slash-dispatch.md, spill ARCHITECTURE.md's Slash Commands to a summary plus one link, flip the row to Present. |
| ConsumableMaster | `CONSUMABLEMASTER-A-01` | A | Low | `docs/ARCHITECTURE.md:279` — Row claims a flat set with no subcommand tree; settings/Slash.lua:202 reads "seventeen verbs, five sub-command tables". | `documentation-§3` | Write docs/slash-dispatch.md from COMMANDS and the five sub-verb namespaces; change the map row to Present with the real trigger. |
| WhatGroup | `WHATGROUP-A-08` | A | Low | `docs/ARCHITECTURE.md:316; core/Compat.lua:24,40,52,62,83,105,125` — Seven addon-specific shims exist; the row reads "no addon-specific shim to document separately", and docs/ carries no compat-layer.md. | `documentation-§3` | Write docs/compat-layer.md covering the seven shims and their degrade contracts, then flip the row to Present. |

## CX08 · Shared icon catalog bypassed by hard-coded Blizzard texture paths — 2 findings, 8 repos **[COLLECTION]**

LibKa0s-Media publishes an icon catalog, yet 75 hard-coded Interface\ paths remain across the nine addons (LootHistory 19, BankLedger 17, ConsumableMaster 11). Two passes filed their own; nobody saw the scale, and no register row ratifies the practice anywhere.

**The cluster's 75 is correct, and it is the addressable number** — measured over tracked `*.lua`, excluding `libs/`, `tests/` and `PrettyChat/GlobalStrings/`, which is generated, unloaded, `.pkgmeta`-ignored and exempted by rule under `M1-STD-08`. 75 lines carry 76 paths: BankLedger 17, LootHistory 19, ConsumableMaster 11, MultiMeters 8, KickCD 7, PanelMaster 7, AbsorbTracker 3, WhatGroup 2, PrettyChat 1. This is the one cluster claim in the collection that a triage "correction" made worse rather than better; the correction is itself corrected under *Cluster claims corrected against the code*. The repo list below omits PrettyChat, which under the corrected census is a one-site gap (`settings/Panel.lua`) rather than the 93-site contradiction the raw figure implied — but it is still a gap, and the site is in scope for `CX08`'s acceptance. Of the 76, 21 are `Interface\\Buttons\\WHITE8x8` — the texture `standalone-windows.md:20` mandates for the shared window edge — and 12 are the addon's own `Interface\\AddOns\\…` art; what remains is Blizzard chrome for which the roughly thirty-mark catalog at `LibKa0s/Media.lua:92` has no equivalent. `lib.Icon` (`Media.lua:202`) already exists; what is missing is a decision about which paths the catalog is even supposed to replace.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, WhatGroup · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LootHistory | `LOOTHISTORY-A-09` | A | Low | `settings/Panel.lua:459-461` — READY, NOTREADY and INFO_ICON hard-code Blizzard paths with only a colour gloss; Browser.lua:1047-1051 records a real reason for its one-off grip texture | `library-stack-§8` | Route through NS.Icon with the Blizzard paths as the `or` fallback, or record the reason beside them the way Browser.lua does |
| MultiMeters | `MULTIMETERS-A-07` | A | Low | `settings/ColumnBlocks.lua:60-61` — Confirmed ENABLED_TEX and DISABLED_TEX hard-code Interface\RaidFrame\ReadyCheck-Ready/-NotReady, with a comment citing ConsumableMaster parity. | `library-stack-§8` | Move both to NS.Icon("circle-check")/NS.Icon("ban") in MultiMeters and ConsumableMaster together, or file the register row in both. |
---

# Part 2 — Clustered findings

Thirty-one clusters, 196 findings. Ordered by cluster id, which runs roughly by severity: `C01` is the
Critical, `C02`–`C07` carry the Highs and the reachable Mediums, and the tail from `C08` is the record,
documentation and hygiene band.

## C01 · Composed media dropdowns hand the flow engine a closure — 3 findings, 2 repos

OptionsCompose wraps O.LSMValues in a second closure, but LSMValues already returns one, so enumList sees a function and yields an empty list. No composer test ever invokes values().

This one-liner is the whole of the collection's critical band. `O.LSMValues` (`LibKa0s/Options.lua:764`) already returns the deferred closure `enumList` wants, and its own docstring at `:759-763` says the deferral is load-bearing. The three composers wrap it again, `enumList` (`OptionsWidgets.lua:78-79`) unwraps once, sees a function, and returns `{}`. The report at `OptionsWidgets.lua:1443` is gated at `:1442` on `row.values == nil`, so nothing prints. `git diff v1.25.0 HEAD -- LibKa0s/` is empty and all nine provenance lines read v1.25.0, so this ships to every consumer today.

*Repos* LibKa0s, AbsorbTracker · *disposition* `libka0s-upstream` · *effort* S · *cluster severity* Critical

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-08` | R | Low † | `libs/LibKa0s/OptionsCompose.lua:231, :275, :304` — values = function() return O.LSMValues(kind) end; LSMValues:764 already returns a function, so enumList:79 sees type ~= table and returns {} | — | Fix in LibKa0s: values = O.LSMValues(kind), drop the outer wrapper. Bump OptionsCompose minor, re-vendor whole folder into every consumer. |
| LibKa0s | `LIBKA0S-A-01` | A | **Critical** † | `LibKa0s/OptionsCompose.lua:231,275,304` — values = function() return O.LSMValues("font") end; O.LSMValues (Options.lua:764) already returns a closure, so enumList (OptionsWidgets.lua:78) sees a function and returns {} | `options-ui-§16` | values = O.LSMValues("font") directly in all three composers; bump OptionsCompose minor, add API doc, re-vendor consumers |
| LibKa0s | `LIBKA0S-A-01d` | A | Medium † | `tests/test_options_compose.lua:274` — The only values assertion in the composer suite is against O.VISIBILITY_VALUES; nothing invokes rows[n].values(). 764 green cases missed A-01. | `testing-§12` | Add three cases asserting type(rows[n].values()) == "table" for FontGroup, BorderGroup, BarGroup |

**† Regraded or corrected in triage.** `ABSORBTRACKER-R-08` — medium to low here: settings/Appearance.lua:130 fixMediaValues already rewrites every LSM row's values, tests/test_schema pins it, and the comment says it is reported upstream. `LIBKA0S-A-01` — was high; raised to critical — an always-on player control silently does nothing in every consumer, with no warning printed. `LIBKA0S-A-01d` — held at medium — this is the gate that would have caught the critical.

## C02 · LSMPatch mutates AceGUI's process-global widget registry — 2 findings, 5 repos **[COLLECTION]**

Five addons each ship a private core/LSMPatch.lua that re-registers LSM30_Border at a higher version, so the last addon to load rewrites the Border dropdown for every addon in the session. All five copies differ.

All five copies confirmed distinct by md5, at 50 (AbsorbTracker), 65 (ConsumableMaster), 66 (PanelMaster), 68 (KickCD) and 101 (MultiMeters) lines. Each calls `AceGUI:RegisterWidgetType("LSM30_Border", …)` at `currentVersion + 1` against a process-global registry, so the last Ka0s addon to load owns that dropdown for every addon in the client, Ka0s or not. `anti-patterns` #8 sanctions `RegisterWidgetType` extension over forking and says nothing about blast radius; the list ends at #75, so there is no rule to cite until one is written.

*Repos* KickCD, PanelMaster, AbsorbTracker, ConsumableMaster, MultiMeters · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| KickCD | `KICKCD-R-01` | R | **High** | `core/LSMPatch.lua:46` — RegisterWidgetType at currentVer+1 on PLAYER_LOGIN; I diffed all five copies — AbsorbTracker, ConsumableMaster, MultiMeters, PanelMaster all differ | `library-stack`, `anti-patterns #48`, `anti-patterns #55` | Promote to LibKa0s as idempotent Options.PatchLSMBorder with a registry sentinel; delete all five local copies; call from OptionsSetup live branch |
| PanelMaster | `PANELMASTER-R-01` | R | Medium † | `core/LSMPatch.lua:44` — AceGUI:RegisterWidgetType("LSM30_Border", wrapper, currentVer+1) at PLAYER_LOGIN; same file confirmed in AbsorbTracker, ConsumableMaster, KickCD, MultiMeters | `library-stack` | Hide displayButton and re-anchor per widget at PanelMaster's own LSM30_Border creation site; leave AceGUI.WidgetRegistry untouched. |

**† Regraded or corrected in triage.** `PANELMASTER-R-01` — high to medium: every other addon's Border dropdown is affected, but the change is purely visual, raises no error and taints nothing.

## C03 · Migration runners gated on the wrong storage scope — 4 findings, 2 repos

Two addons stamp the schema version in a scope the migration steps do not write: BankLedger ships schemaVersion as an AceDB default so the runner never sees a pre-stamp store, ConsumableMaster gates profile writes on an account-wide key so OnProfileChanged is inert. Both are pinned by tests that cannot go red.

Both defects are pinned by tests that cannot go red, so the fake has to move before the code. BankLedger: `defaults/Global.lua:14` ships `schemaVersion` as an AceDB default, so `core/Database.lua:17`'s `g.schemaVersion or 1` always reads 2 and the `< NS.SCHEMA_VERSION` arm at `:21` never runs against a real v1 store. ConsumableMaster: `core/Database.lua:65-90` reads and stamps the account-wide `g.schemaVersion` while both steps write `db.profile`, so the `OnProfileChanged` hook at `core/ConsumableMaster.lua:401-410` does nothing on a second profile. Neither is provable headless until `BANKLEDGER-R-03` and `CONSUMABLEMASTER-R-14` land first.

*Repos* BankLedger, ConsumableMaster · *disposition* `per-addon` · *effort* M · *cluster severity* High

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| BankLedger | `BANKLEDGER-R-02` | R | **High** † | `defaults/Global.lua:14 + core/Database.lua:15-21` — Default 2 is always readable, so `g.schemaVersion or 1` never sees 1; logout removeDefaults (AceDB-3.0.lua:170-172) strips the equal stored value. | `savedvariables-§1` | Drop schemaVersion from defaults; let RunMigrations seed it, using an empty ledger to separate fresh install from pre-stamp store. |
| BankLedger | `BANKLEDGER-R-03` | R | Medium † | `tests/wow_mock.lua:582-589 (case at tests/test_database.lua:330)` — Local override returns deepcopy(defaults.global); setting the key nil reads nil. The kit fake copies defaults in too, so it fails identically. | `testing-§12` | Model the defaults fallback (metatable or logout strip) in the AceDB fake, then pin the absent-key case against it. Never weaken the case. |
| ConsumableMaster | `CONSUMABLEMASTER-R-01` | R | Medium † | `core/Database.lua:65-90` — Steps read g.schemaVersion, write db.profile; :85 stamps g.schemaVersion=3, so the OnProfileChanged reload at ConsumableMaster.lua:410 runs nothing. | `savedvariables` | Gate profile-writing steps on db.profile.schemaVersion, keep db.global for account-wide steps, and let the profile callbacks do real work. |
| ConsumableMaster | `CONSUMABLEMASTER-R-14` | R | Low | `tests/test_database.lua:56-63` — Named "never writes into the profile scope" while both steps write db.profile; its second assertion pins the account-wide key CM-R-01 faults. | `testing` | Rename to what is asserted and revisit the schemaVersion assertion alongside the CM-R-01 fix, adding the missing multi-profile case. |

**† Regraded or corrected in triage.** `BANKLEDGER-R-02` — kept high: today only stale vendorPrice keys, but the next SCHEMA_VERSION bump silently skips migration for every existing store. `BANKLEDGER-R-03` — high to medium (test-only), and the review's fix is wrong: wrapping the kit fake would not restore the ability to fail. `CONSUMABLEMASTER-R-01` — was high; worst reachable outcome is one cosmetic font-flag preference reverting on a non-active profile.

## C04 · MultiMeters feign-trace subsystem: unconditional allocation, blind spots, no coverage — 8 findings, 1 repo

The issue-25 feign diagnostic builds its trace payload before checking whether tracing is armed, shares one 120-entry ring across kinds, misses the eviction branch that most likely explains the bug, and has no test coverage at all.

*Repos* MultiMeters · *disposition* `per-addon` · *effort* M · *cluster severity* High

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| MultiMeters | `MULTIMETERS-R-01` | R | **High** | `modules/Aggregator.lua:1488-1496, modules/Feign.lua:102-105, modules/Feign.lua:274-281` — Verified: judge sits inside `for index, src in ipairs(column.sources)`; fields plus its nested order table are built before TraceFeign's nil check. | `performance-§2` | Read a plain published boolean (Diagnostics.feignArmed) before building the table; hoist it above Aggregator's per-source loop. |
| MultiMeters | `MULTIMETERS-R-02` | R | Medium † | `core/Diagnostics.lua:1604, :1643` — FEIGN_TRACE_MAX = 120 confirmed at :1604; table.remove(log, 1) oldest-first at :1643; judge fires per death row per refresh. | — | Admit judge only for GUIDs a cast line named, with a suppressed-row counter; or one bounded ring per kind. |
| MultiMeters | `MULTIMETERS-R-03` | R | Medium † | `modules/Feign.lua:247-249` — Confirmed: present admits only IsSafeKey GUIDs with entry.unit; `if unit == nil then feigned[guid] = nil` falls through with no trace call. | — | Trace this branch with a distinct verdict (state="<not in group>"), behind the same armed boolean R-01 introduces. |
| MultiMeters | `MULTIMETERS-R-04` | R | Medium | `tests/test_diagnostics.lua:1290, tests/test_feign.lua` — grep across tests/: judge appears in two comments and one unrelated Feign title; FEIGN_TRACE_MAX appears nowhere. Zero assertions either way. | `testing-§12` | Add cases for judge, for cast surviving a full ring, and for the not-in-group eviction, each with a verified red-under. |
| MultiMeters | `MULTIMETERS-R-09` | R | Low | `core/Diagnostics.lua:1643` — Confirmed table.remove(log, 1), O(n) with n up to 120, on every armed insert. Armed-only, so no player pays it. | — | Use a write index into a fixed-size table and have reportFeign read from that index forward. |
| MultiMeters | `MULTIMETERS-R-10` | R | Low | `core/Diagnostics.lua:1618` — grep over core, modules, settings, tests returns the definition at :1618 and one reference at tests/test_diagnostics.lua:1293. Nothing else. | — | Keep it as the tested accessor, and have it read the plain published field R-01 introduces, which the hot sites read directly. |
| MultiMeters | `MULTIMETERS-R-12` | R | Low | `settings/Slash.lua:470-484` — Confirmed: anything not exactly on or off falls to the else branch calling ReportFeign; /mm debug of prints a report and leaves the trace armed. | — | Name the rejected argument and return, following the addon's existing unknown-verb "name it, then help" pattern. |
| MultiMeters | `MULTIMETERS-R-13` | R | Low | `modules/Feign.lua:280` — Confirmed: feigned[guid] cleared inside the evicted branch above the trace, so state falls to "<evicted>" for every evicted row. | — | Hoist the prior state into a local above the eviction and report that, so noted and down stay distinguishable in the log. |

**† Regraded or corrected in triage.** `MULTIMETERS-R-02` — review had high; only executes behind an armed debug verb, so no player ever sees it. `MULTIMETERS-R-03` — review had high; diagnostic blind spot only, and the same bug it hides is itself untriaged.

## C05 · estimateRecordBytes truncates on a nil field, with a test that cannot fail — 2 findings, 1 repo

A literal field array is walked with ipairs, so a currency record with no itemLink runs zero iterations and is charged flat overhead; the case under it asserts only bytes > 0.

*Repos* LootHistory · *disposition* `per-addon` · *effort* S · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LootHistory | `LOOTHISTORY-R-01` | R | Medium † | `core/Database.lua:748-754` — strFields literal walked with ipairs; Collector.lua:190-196 builds currency records with no itemLink, so zero iterations run | — | Sum the seven fields inline with no intermediate table; the per-record allocation R-04 names disappears with it |
| LootHistory | `LOOTHISTORY-R-02` | R | Low † | `tests/test_database.lua:379` — assertTrue(s.bytes > 0) passes at 512 of pure overhead; the fixture rows carry no zone, so they already run the truncating path | `testing-§12` | Assert an exact byte total over a fully-populated fixture plus a currency row, with a "-- red under:" comment naming R-01 |

**† Regraded or corrected in triage.** `LOOTHISTORY-R-01` — R-04 was a separate medium; it is the same two lines and the same fix, and its own cost is negligible. `LOOTHISTORY-R-02` — Lowered from medium and scoped addon-local: it is one sleeping assertion, not a cross-cutting pattern.

## C06 · PrettyChat stores a player-entered format with no conversion-signature check — 1 finding, 1 repo

Schema.Set accepts any string and pushes it into _G, while the Preview synthesises its arguments from the format itself, so a surplus conversion can never be seen before it raises inside Blizzard's chat handler.

*Repos* PrettyChat · *disposition* `per-addon` · *effort* M · *cluster severity* High

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| PrettyChat | `PRETTYCHAT-R-01` | R | **High** † | `settings/Schema.lua:464 (Schema.Set); modules/Override.lua:275-292; tests/test_defaults.lua:174` — row.set stores any string; buildSampleArgs synthesizes args from the format itself, so RenderSample can never see a surplus conversion. | `architecture-§5` | Move conversionSequence into modules/Override.lua as NS.ConversionSequence; have Schema.Set reject a write whose sequence differs from the shipped default's. |

**† Regraded or corrected in triage.** `PRETTYCHAT-R-01` — Kept high. Confirmed reachable: a surplus %s raises inside Blizzard's chat handler on every matching message, and the Preview reports success.

## C07 · Landing-page logo rides AceGUI's pooled SimpleGroup — 1 finding, 1 repo

PrettyChat hand-rolled a copy of LibKa0s's landing renderer and omitted the OnRelease that hides the texture, so a 300px logo survives into the next widget that takes the pooled group.

*Repos* PrettyChat · *disposition* `per-addon` · *effort* M · *cluster severity* High

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| PrettyChat | `PRETTYCHAT-R-02` | R | **High** † | `settings/Panel.lua:646-721, esp. 663-675` — libs/LibKa0s/OptionsWidgets.lua:322 sets OnRelease to hide the texture; Panel.lua's copy caches pcLogo but sets no OnRelease at all. | `options-ui-§5` | Replace buildParentBody with H.BuildLandingPage(ctx, spec); add a BuildLandingPage no-op to settings/OptionsSetup.lua's degradation stub. |

**† Regraded or corrected in triage.** `PRETTYCHAT-R-02` — Kept high, but the review's stated cause is half right: texture creation is already guarded; the missing OnRelease hide is the actual leak.

## C08 · Automated-test records stale in every repo — 25 findings, 10 repos **[COLLECTION]**

RESULTS.md rows, standing prose and complexity watch lists are one to eight runs behind everywhere, and 46 of 89 frozen bundles carry no ANALYSIS.md. Nothing regenerates the record except a manual run, and no gate reads it.

The cluster's numbers do not survive re-counting, and the mechanism is upstream. `documentation.md:180` calls `docs/automated-tests/RESULTS.md` "**generated**, never hand-edited", while `automated-tests.md:223-224` requires a per-entry disposition ("*accepted and why*", "*peel next*") and `:236` "a short standing section for each of the **other three** suites" — narrative no generator produces, and `run-automated-tests.sh` writes none of it. `automated-tests.md:245` makes `ANALYSIS.md` a MUST only for **release** runs. Settle the contradiction before sizing this; a large part of the XL is probably not work.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, LibKa0s · *disposition* `per-addon` · *effort* XL · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-04` | A | Low | `docs/automated-tests/20260825-103352/` — ls shows complexity/lint/manifest/perf.json/perf.txt/test-cases/tests only; that run moved NLOC 7766 to 7997 and tests 489 to 508 | `automated-tests-§5` | Write ANALYSIS.md per the root AUTOMATED_TESTS.md prompt, reporting complexity totals and averages both. |
| AbsorbTracker | `ABSORBTRACKER-A-11` | A | Low † | `docs/automated-tests/RESULTS.md:100-130` — Fresh lizard: ValidateSchema 15 (listed 14), ResolveColor 14 unlisted, BuildMainContent absent from output entirely | `automated-tests-§4` | Folded into the record regeneration above; kept as its own id so the merged fix is checkable per-row. |
| AbsorbTracker | `ABSORBTRACKER-R-06` | R | Low † | `docs/automated-tests/RESULTS.md rows :23 and narrative :100-130` — Newest row: 508 tests, 7997 NLOC, 29 files, max CCN 14. Today: 547, 8903, 27, 15. Narrative anchored to 20260807-114413, two rows back. | `automated-tests-§4` | Re-anchor the four standing sections and both watch-list tables to the newest bundle, rebuilt from a fresh complexity.txt, at the next recorded run. |
| BankLedger | `BANKLEDGER-A-05` | A | Low | `docs/automated-tests/20260807-110442/, docs/automated-tests/20260825-103400/` — Confirmed absent in both; 20260825 moved every figure (727→791 tests, 12735→13409 NLOC, 24→28 files) with no write-up. | `automated-tests-§5` | Do not back-fill frozen bundles; write the next run's analysis and explain the 20260825 jump there. |
| BankLedger | `BANKLEDGER-R-05` | R | Low † | `docs/automated-tests/RESULTS.md:23,41-42,97-98,113-129` — Newest row 13409 NLOC/2043 fn/791 tests vs measured 14174/2153/831; prose cites 20260807-115101 and five CCN-15 funcs incl. ensureFrame (today four, not it). | `automated-tests-§4/§6` | Regenerate at the next release run via bump-version; roll both watch tables forward then. Never hand-edit a measured report. |
| ConsumableMaster | `CONSUMABLEMASTER-A-07` | A | Low † | `docs/automated-tests/RESULTS.md:9-11` — Lead-in is the old two-sentence text; tests/_kit/run-automated-tests.sh:425-433 emits four paragraphs naming the tag gate and CCN 15. | `automated-tests-§4` | Replace the lead-in with the paragraphs the runner emits; never touch the table header. It is only written on file creation. |
| ConsumableMaster | `CONSUMABLEMASTER-A-10` | A | Low † | `docs/automated-tests/20260825-103407/, docs/automated-tests/20260807-110619/` — Both hold seven artifacts and no ANALYSIS.md; the sibling 20260807-114612 has one, so the omission is real and not layout. | `automated-tests-§5` | Write the analyses, or record in RESULTS.md that both are green non-release runs deliberately skipped under the SHOULD. |
| ConsumableMaster | `CONSUMABLEMASTER-R-06` | R | Low † | `docs/automated-tests/RESULTS.md:15, :109, :155` — Top row 20260825-103407 reads 698/58/15870 against today's 749/59/17632; watch list anchors on 20260807-114612 and lists test_macrobar at 1688. | `automated-tests-§4` | Run the vendored runner to prepend a row, re-anchor the Current-state line, and rewrite both watch-list tables against wc -l. |
| KickCD | `KICKCD-A-09` | A | Low | `docs/automated-tests/20260825-103417/, docs/automated-tests/20260807-110522/` — Both manifests read `"release": null`, so the MUST arm is untriggered; 20260825's tests 780, lint 35, NLOC 15802 all moved from the run before | `automated-tests-§5` | Write ANALYSIS.md for the new bundle KICKCD-R-05's rerun produces. Do not backfill the frozen 20260807-110522 |
| KickCD | `KICKCD-R-05` | R | Low † | `docs/automated-tests/RESULTS.md:36,56,120 vs :23` — Prose says 756 cases / 33 lint files as of 20260807-114618; table row :23 says 780/35; today 841/36 | `performance-§10`, `automated-tests-§4` | Fix the vendored kit's generator upstream to regenerate prose alongside the table row; never hand-edit the report here |
| LootHistory | `LOOTHISTORY-A-06` | A | Low | `docs/automated-tests/20260807-110451/, docs/automated-tests/20260825-103428/` — Directory listing confirms five of seven bundles have ANALYSIS.md and these two do not; 20260825 moved tests 594 to 644 and NLOC 11479 to 12116 | `automated-tests-§5` | Write ANALYSIS.md with the next bundle per the root playbook, reporting complexity totals and averages; do not retro-fit frozen bundles |
| LootHistory | `LOOTHISTORY-A-08` | A | Low † | `docs/automated-tests/RESULTS.md:143` — The row says the disposition "has stopped being one" and that nothing tracks it; gh shows no open issue for the Analytics peel | `automated-tests-§4` | Open a state:triaged issue naming the renderers-versus-helpers seam and repoint the band disposition at its number, or do the peel |
| LootHistory | `LOOTHISTORY-R-11` | R | Low | `docs/automated-tests/RESULTS.md:33,58,91,138-148` — Prose reads 594 cases "as of 20260807-114650" against a newest row of 20260825-103428 (644/12116); today measures 699/13222 | `automated-tests-§4` | Regenerate via the kit runner, rewrite the four standing prose sections, and give settings/Panel.lua (1004 LOC) its own band disposition |
| MultiMeters | `MULTIMETERS-R-05` | R | Medium † | `docs/automated-tests/RESULTS.md:30-66` — "Current as of 20260809-195454", "None. lizard reports 0 warnings"; bands Schema.lua 1371 and Window.lua 1232 against 3069 and 2644 today. | `automated-tests-§3` | Run tests/_kit/run-automated-tests.sh, then re-author both watch-list tables against the new bundle with a disposition per entry. Never hand-edit. |
| MultiMeters | `MULTIMETERS-A-13` | A | Low | `docs/automated-tests/20260825-021705/, docs/automated-tests/20260825-103437/` — Confirmed: of four bundles only 20260809-195454/ANALYSIS.md exists. Both 2026-08-25 runs are non-release, so this is the SHOULD. | `automated-tests-§5` | Write ANALYSIS.md for the next bundle produced; never back-fill a frozen bundle. |
| MultiMeters | `MULTIMETERS-R-06` | R | Low † | `docs/test-cases.md:1656, README.md:7` — docs/test-cases.md:1656 reads Total 1487; README.md:7 badge reads Tests-1487%2F1487_passing; suite reports 1496. | `documentation-§1` | Run lua tests/run.lua --list > docs/test-cases.md and set the badge from the run bundle's manifest, in one commit. |
| PanelMaster | `PANELMASTER-A-08` | A | Low | `docs/automated-tests/20260807-110543/, docs/automated-tests/20260825-103450/` — Confirmed by listing: six of the eight bundles carry ANALYSIS.md, these two do not | `automated-tests-§5` | Write the two readings, or record in docs/automated-tests/README.md that non-release runs may ship without one. |
| PanelMaster | `PANELMASTER-R-08` | R | Low | `docs/automated-tests/RESULTS.md:23, :157, :174-175` — Newest row records 731/731, 11223 NLOC, 1379 funcs against today's 763/763, 12122, 1472; watch list still carries PanelEditor.lua at 1091 | `automated-tests-§4` | Regenerate at the next release via /wow-addon:bump-version; re-anchor the watch-list prose and settle PanelEditor.lua. Never hand-edit, never gate a commit on it. |
| PrettyChat | `PRETTYCHAT-R-05` | R | Low † | `docs/automated-tests/RESULTS.md:44,48,55-74,84` — Prose says 260 cases over 17 files, max CCN 12 over 531 functions; today measures 300 over 18 files and 645 functions. | `automated-tests-§4` | Run the vendored runner without --release and let it regenerate the four standing sections. Never hand-edit a generated figure. |
| WhatGroup | `WHATGROUP-A-04` | A | Low | `docs/automated-tests/20260807-110421/, 20260825-103505/` — Confirmed by ls: those two hold no ANALYSIS.md, the other seven do. Both manifests record "release": null, so this is the SHOULD. | `automated-tests-§5` | Backfill both, or state once in RESULTS.md that non-release runs get no write-up and stop the question recurring. |
| WhatGroup | `WHATGROUP-R-08` | R | Low | `docs/automated-tests/RESULTS.md:23,47,72,98,126` — Newest row is 20260825-103505 at 485/485, 6377 NLOC; four standing sections still say "as of 20260807-121935", 462 cases. Measured today: 528, 7047. | `automated-tests-§1`, `automated-tests-§4` | Re-run tests/_kit/run-automated-tests.sh and let it roll the row and the four standing sections forward; never hand-edit a recorded number. |
| LibKa0s | `LIBKA0S-R-02` | R | Medium † | `docs/automated-tests/RESULTS.md:49, :79, :119-129, :158` — "499 cases" (764), "Clean over 12 files" (18), "Nothing is over the 1500 cap" vs manifest overCapFiles 2; watch list names Kit.run@framework.lua:394-433, now :668 | `automated-tests-§4` | Regenerate all four standing sections and both watch-list tables against 20260903-161751; give drawContentPanel a disposition as the new ceiling |
| LibKa0s | `LIBKA0S-A-04` | A | Low | `docs/automated-tests/` — 31 dated bundles, 14 with ANALYSIS.md; the write-up is absent from 20260903-161751. Audit's "of 28" is wrong — 31 bundles exist. | `automated-tests-§5` | Add the ANALYSIS.md write-up as a numbered sub-step of docs/releasing.md step 7; do not backfill frozen runs |
| LibKa0s | `LIBKA0S-A-05` | A | Low | `docs/automated-tests/ vs git tag v1.24.0` — Tag v1.24.0 exists; bundle manifest releases run 1.23.0 (20260831-185425) then 1.25.0 (20260903-161751). No bundle names 1.24.0. | `automated-tests-§6` | Make the four-suite bundle a hard precondition of the tag in docs/releasing.md; note the gap in the next ANALYSIS.md |
| LibKa0s | `LIBKA0S-R-12` | R | Low | `docs/automated-tests/20260903-161751/manifest.json` — git sha 895cdf4 with dirty: true, branch feat/settings-revamp-v2; the bundle was committed in d3fc4a0, which also changed OptionsCompose.lua by 21 lines | `automated-tests-§6` | Require a clean tree for the release battery in docs/releasing.md, or have the runner refuse to stamp a dirty release run as reproducible |

**† Regraded or corrected in triage.** `ABSORBTRACKER-A-11` — retained under R-06's merge as the verifiable half; severity low, developer record only. `ABSORBTRACKER-R-06` — three findings, one defect: the stale row, the stale anchor and the stale watch list are the same record not having been regenerated. `BANKLEDGER-R-05` — medium to low: a dev-facing record, zero player impact, and it regenerates mechanically. `CONSUMABLEMASTER-A-07` — recategorised from perf; this is prose about gates, not a measurement. `CONSUMABLEMASTER-A-10` — recategorised from perf; the missing artifact is the write-up, not a measurement. `CONSUMABLEMASTER-R-06` — was medium; a record-keeping gap, and the release gate reads manifest.json rather than this file. `KICKCD-R-05` — medium (review) / low (audit); prose only, and the table row beside it is correct. `LOOTHISTORY-A-08` — Audit said five runs; RESULTS.md's own text says four. `MULTIMETERS-R-05` — audit had low; the release gate reads this list, and it states a false all-clear. `MULTIMETERS-R-06` — both passes had medium; a stale badge misleads a reader, it cannot break anything. `PRETTYCHAT-R-05` — Both passes found this; merged. Medium to low — a stale record, no reachable impact. Max CCN is 13, not 12, and fitTree is unlisted. `LIBKA0S-R-02` — held at medium; R-02's claimed "generated, never hand-edited" banner is not what the file says — the banner claims overwrite-in-place only.

## C09 · Shared test-kit runner drops the skipped count and mis-renders release rows — 8 findings, 5 repos **[COLLECTION]**

testkit/run-automated-tests.sh's pass regex cannot span ", N skipped", the manifest has no skipped key, the release row shows the pre-bump version, and the corrected lead-in only reaches a file that does not yet exist. Every consumer inherits all four.

All four defects are in one file. `testkit/run-automated-tests.sh:195` matches `'[0-9]+ passed, [0-9]+ failed(, [0-9]+ total)?'` while `framework.lua:566` prints `N passed, N failed, N skipped, N total`, so the `awk '{print $5}'` total reads empty and falls back to passed+failed; the manifest has no `skipped` key; the trend row at `:388` renders `$ADDON_VERSION` only, so a release run shows the pre-bump version; and the corrected four-checkpoint lead-in at `:414-432` sits in the branch reached only when `RESULTS.md` does not exist. `tests/_kit/` is byte-identical in all nine consumers, so one kit revision fixes all of it.

*Repos* LibKa0s, AbsorbTracker, BankLedger, ConsumableMaster, WhatGroup · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-05` | A | Low | `tests/_kit/run-automated-tests.sh:369,391` — suite_json tests emits passed/failed/total with no skipped; the ROW cell renders $TESTS_PASS/$TESTS_TOTAL | `automated-tests-§4` | Fix in the LibKa0s test kit: capture N skipped, render passed/skipped/total, add "skipped" to the manifest, re-vendor. |
| BankLedger | `BANKLEDGER-A-07` | A | Low | `tests/_kit/run-automated-tests.sh:195` — Regex matches only '[0-9]+ passed, [0-9]+ failed(, [0-9]+ total)?'; the runner emits '831 passed, 0 failed, 0 skipped, 831 total'. | `automated-tests-§4` | Fix in the LibKa0s kit: capture skipped into the manifest tests object and the RESULTS column; re-vendor here. |
| ConsumableMaster | `CONSUMABLEMASTER-A-11` | A | Low | `tests/_kit/run-automated-tests.sh:372, :388` — ROW emits cell tests "$TESTS_PASS/$TESTS_TOTAL"; the manifest suite_json writes passed, failed and total with no skipped key. | `automated-tests-§4` | Fix in the LibKa0s testkit and re-vendor; a header change needs a consumer migration note. Not patchable under tests/_kit. |
| WhatGroup | `WHATGROUP-A-05` | A | Low | `docs/automated-tests/20260825-103505/manifest.json` — tests object carries passed/failed/total only; the runner prints "0 skipped" but never records it, so a skip would read as a pass. | `automated-tests-§4` | Raise on LibKa0s: the runner must emit skipped alongside passed and total; adopt at the next re-vendor. |
| WhatGroup | `WHATGROUP-A-06` | A | Low | `tests/_kit/vendor_sync.lua` — grep for 100755, ls-files and executable across the file returns nothing; this repo's mode is correct today, so nothing is broken. | `automated-tests-§2` | Raise on LibKa0s: the consumer-side gate should assert git ls-files -s reports 100755 for the runner script. |
| LibKa0s | `LIBKA0S-A-06` | A | Low | `testkit/run-automated-tests.sh:408-432` — The four-checkpoint text sits in the else branch reached only when RESULTS.md is absent or header-mismatched; RESULTS.md:9-11 still carries the old half-truth | `automated-tests-§4` | Rewrite the prose block above a matching header while preserving rows; bump Kit.VERSION and re-vendor nine consumers |
| LibKa0s | `LIBKA0S-A-07` | A | Low | `testkit/run-automated-tests.sh:195-200,369` — Regex '[0-9]+ passed, [0-9]+ failed(, [0-9]+ total)?' cannot span ", 0 skipped"; TESTS_TOTAL silently falls back to passed+failed | `automated-tests-§4` | Capture N skipped, emit passed/skipped/total in the row and suites.tests.skipped in the manifest; keep the column name |
| LibKa0s | `LIBKA0S-R-13` | R | Low † | `docs/automated-tests/RESULTS.md:16; testkit/run-automated-tests.sh:388` — Row 20260903-161751 reads Version 1.24.0 while its manifest carries "release": "1.25.0"; the ROW uses $ADDON_VERSION only | `automated-tests-§4` | Render the cell as version arrow release when manifest.release is set, in testkit/run-automated-tests.sh, then re-vendor the kit whole |

**† Regraded or corrected in triage.** `LIBKA0S-R-13` — scope corrected from libka0s-upstream — this repo IS the kit's master copy, so the fix lands here and ripples to nine consumers.

## C10 · Working-tree line endings disagree with the CRLF pin in all ten repos — 12 findings, 10 repos **[COLLECTION]**

Every repo pins eol=crlf but carries LF or mixed stragglers in the working tree (2 to 21 each, 76 in total), and LibKa0s's own EOL gate only scans docs/automated-tests, so nothing catches them. Two LibKa0s source files are LF, which makes every consumer's vendor diff report false drift.

Two of the stragglers are the prerequisite for everything else upstream. `git ls-files --eol` in LibKa0s returns exactly seven tracked files at `w/lf` under `attr/text=auto eol=crlf` (the two `.sh` are correctly `eol=lf`), and two of them — `LibKa0s/DebugLog.lua` and `LibKa0s/Pool.lua` — are in the shipped payload. `docs/releasing.md:134`'s byte diff will therefore report drift in nine repos on every re-vendor, forever, while `:133`'s content diff passes. LibKa0s's own gate cannot see them: `tests/test_eol.lua:29` scopes `BUNDLES` to `"docs/automated-tests"`.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, LibKa0s · *disposition* `mixed` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-07` | A | Low † | `docs/revendor/2026-08-25/01_DELTA.md and tests/test_units.lua` — git ls-files --eol \| grep mixed prints exactly two rows, both attr/text=auto eol=crlf; the review claimed only the doc | `line-endings-§1` | git add --renormalize . as its own commit on a clean tree, then rm and git checkout -- the two stragglers. |
| BankLedger | `BANKLEDGER-R-08` | R | Low | `tests/test_marks.lua, docs/media.md, docs/revendor/2026-08-25/{01_DELTA,05_SUMMARY}.md` — git ls-files --eol: four text=auto eol=crlf paths at w/lf (01_DELTA w/mixed); tests/_kit/run-automated-tests.sh is correctly eol=lf. | `line-endings-§1/§7` | git add --renormalize . as one whitespace-only commit, taken last. |
| BankLedger | `BANKLEDGER-R-09` | R | Low † | `libs/LibKa0s/{DebugLog,Pool}.lua vs ../LibKa0s/LibKa0s/` — diff -rq flags both; identical after tr -d '\r'. The vendored copies are correct; the source-side files are the LF ones. | `line-endings-§2` | Renormalise in the LibKa0s repo. No minor bump, no local edit; re-vendor whole folder only if blobs move. |
| ConsumableMaster | `CONSUMABLEMASTER-R-08` | R | Low † | `.gitattributes vs git ls-files --eol` — Counter reproduces at 7: .pkgmeta, ConsumableMaster.toc, core/ItemSetup.lua, core/SlashCommands.lua, two revendor docs, tests/test_itemsetup.lua. | `line-endings-§2` | Renormalize in its own commit, then rm plus checkout any straggler the index refresh misses; re-run the counter to zero. |
| KickCD | `KICKCD-R-06` | R | Low † | `.gitattributes:26; .pkgmeta, KickCD.toc, core/PoolSetup.lua, modules/IconGrid.lua, docs/slash-dispatch.md, tests/test_icongrid_buildlist.lua, +2` — git ls-files --eol excluding -text binaries: 7 w/lf + 1 w/mixed = 8, not the review's 9. Two of the eight sit inside the frozen docs/revendor/2026-08-25/ bundle | `line-endings-§1`, `line-endings-§2` | git add --renormalize . as its own commit, last; decide first whether the two frozen-bundle files are in scope |
| LootHistory | `LOOTHISTORY-R-15` | R | Low | `.pkgmeta, core/Constants.lua, core/MediaSetup.lua, core/Util.lua (cr=216 lf=252), modules/Analytics.lua, settings/Slash.lua, tests/test_util.lua, +2 frozen docs` — I re-counted CR against LF over git ls-files excluding libs and tests/_kit: exactly 9 disagree; .gitattributes is correct and complete | `line-endings-§1`, `line-endings-§2`, `line-endings-§7` | git add --renormalize . in its own commit, then re-checkout the stragglers; re-run the CR/LF count and expect zero |
| MultiMeters | `MULTIMETERS-A-05` | A | Low | `repo working tree (.gitattributes:26 pin is correct)` — git ls-files --eol: 22 files w/lf, 21 of them non-.sh, including README.md, .pkgmeta, core/Compat.lua, docs/ARCHITECTURE.md. Index is LF throughout. | `line-endings-§7` | git add --renormalize . in its own commit, then delete and re-checkout the tree. .gitattributes needs no edit. |
| PanelMaster | `PANELMASTER-R-09` | R | Low | `settings/Slash.lua, tests/test_slash.lua, tests/wow_mock.lua, docs/revendor/2026-08-25/01_DELTA.md and 05_SUMMARY.md` — git ls-files --eol returns exactly those five as w/lf or w/mixed against attr eol=crlf; the *.sh carve-out and the binary markers are correct | `line-endings-§7` | git add --renormalize . as its own commit after the code changes, then re-run the count to zero. |
| PanelMaster | `PANELMASTER-R-10` | R | Low | `../LibKa0s/LibKa0s/DebugLog.lua, ../LibKa0s/LibKa0s/Pool.lua` — diff -r reports 1,793c1,793 for DebugLog.lua against the sibling working tree; Core.lua is CRLF on both sides. Content is identical. | `line-endings-§2` | Fix in the LibKa0s repo via git add --renormalize. No minor bump, no re-vendor. Never edit libs/ here. |
| PrettyChat | `PRETTYCHAT-A-07` | A | Low † | `docs/revendor/2026-08-25/01_DELTA.md; docs/revendor/2026-08-25/05_SUMMARY.md; libs/LibKa0s/DebugLog.lua; libs/LibKa0s/Pool.lua` — `git ls-files --eol` returns **four** paths w/lf or w/mixed under the CRLF pin. Two outside libs/ and tests/_kit/, which is the audit's scope and where its "two" is right; the other two are inside the **shipped** vendored payload, which is where it matters. | `line-endings-§1` | `rm` plus `git checkout --` on all four — `git add --renormalize` rewrites an index that is already correct and repairs no working-tree byte. The two payload files are repaired by the M3-05 re-vendor once LibKa0s itself is CRLF; the two frozen docs are the repo's own. |
| WhatGroup | `WHATGROUP-R-13` | R | Low | `.pkgmeta, locales/enUS.lua, tests/test_debuglog.lua, tests/test_mediasetup.lua, docs/revendor/2026-08-25/01_DELTA.md, 05_SUMMARY.md` — git ls-files --eol: five w/lf, 01_DELTA.md w/mixed; .gitattributes itself is correct, and the tests/_kit/*.sh eol=lf carve-out is legitimate. | `line-endings-§1`, `line-endings-§2` | Renormalize the index, then rm and re-checkout those six paths so the working tree follows; the roll-up belongs to the standards audit. |
| LibKa0s | `LIBKA0S-R-04` | R | Low † | `tests/test_eol.lua:29 (BUNDLES = "docs/automated-tests"); LibKa0s/DebugLog.lua, LibKa0s/Pool.lua, tests/test_debuglog.lua, tests/test_pool.lua, three docs/api files` — git ls-files --eol shows exactly 7 files i/lf w/lf under eol=crlf (the two .sh are correctly eol=lf); the gate can only see docs/automated-tests | `line-endings-§7` | Widen trackedFiles() to the whole tracked set, keeping the NUL guard at :107; repair the seven with rm plus git checkout -- in the same change |

**† Regraded or corrected in triage.** `ABSORBTRACKER-A-07` — kept low; corrected the review's count of one to the audit's two, and the second is a test source file, not a frozen doc. `BANKLEDGER-R-09` — kept low; note the audit's 'diff empty' compared the v1.25.0 tag while LibKa0s HEAD is v1.25.0-2-g4eacebe — both statements are true. `CONSUMABLEMASTER-R-08` — was medium; the index is correct LF and packaging reads git, so nothing malformed ships. `KICKCD-R-06` — medium (review) / low (audit); working-tree hygiene, no shipped artifact differs. `PRETTYCHAT-A-07` — Kept low; the count is **4**, and the scope is what moved. The audit's four reproduce exactly; the triage pass narrowed the scope to "outside libs/ and tests/_kit/", got two, and recorded that as a correction. It was not one: there are no binary .tga/.ttf hits at all, and the two paths the narrowing dropped are `libs/LibKa0s/DebugLog.lua` and `libs/LibKa0s/Pool.lua` — Lua source in the shipped payload, and the only stragglers in this repository that reach a player. `PRETTYCHAT-X-02` had to re-find them from the other direction. `LIBKA0S-R-04` — was medium; lowered to low — index bytes are already LF-normalized, so nothing a player installs is affected.

## C11 · .pkgmeta ignore lists diverge; dev bytes reach players — 7 findings, 7 repos **[COLLECTION]**

Nine independently worded ignore blocks with no shared template, and two different kinds of omission inside them. What actually ships is `media/screenshots`: tracked in every repo that has one and ignored in only four, so KickCD (7.5M), LootHistory (5.9M), AbsorbTracker (2.0M) and WhatGroup (880K) put 16.3M of project-page art into every download, WhatGroup adding CLAUDE.md and DEPENDENCIES.md. What does not ship is the agent tooling: `.claude`, `.superpowers` and `.pytest_cache` are untracked in every repository in the collection, so no packager clone carries them — they belong on the lists under `packaging.md:28`'s strong form, which binds every root dot-entry **present in the repo** whether or not git tracks it, and not because a player downloads them. `.gitattributes` and `.pkgmeta` are unaccounted in five.

*Repos* AbsorbTracker, ConsumableMaster, KickCD, LootHistory, PanelMaster, PrettyChat, WhatGroup · *disposition* `per-addon` · *effort* S · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-01` | A | Medium † | `.pkgmeta:5-12` — ignore: lists docs/tests/_dev/dotfiles but not .claude, .superpowers or media/screenshots. .superpowers is 2.8M across 60 files, exactly 30 of them review-*.diff — and **untracked**: .gitignore:11,15 names both directories, `git ls-files .claude .superpowers` returns nothing, so no packager clone carries either. What this repo does ship is media/screenshots, 4 tracked files at 2.0M, absent from the ignore list. | `packaging` | Add `  - media/screenshots` — the shipped half — plus `  - .claude` and `  - .superpowers` under packaging.md:28's present-in-the-repo rule, each with a one-line comment saying which half it is. |
| ConsumableMaster | `CONSUMABLEMASTER-A-09` | A | Low | `.pkgmeta` — Confirmed by reading .pkgmeta: docs, tests, .claude, .superpowers and media globs are listed; _dev is not, and the directory does not exist. | `packaging` | Add the _dev entry beside tests. Nothing ships differently today; this closes the gap before a _dev directory ever appears. |
| KickCD | `KICKCD-A-01` | A | Low | `.pkgmeta:5-12` — Ignore block lists .luacheckrc/.gitignore/.gitattributes but not .claude, .superpowers, .pkgmeta; 4 of 5 sibling addons omit .superpowers too | `packaging` | Add `- .claude`, `- .superpowers`, `- .pkgmeta` to the ignore block with a justification comment |
| LootHistory | `LOOTHISTORY-A-01` | A | Low | `.pkgmeta:6-17` — Ignore names .luacheckrc and .gitignore only; .gitattributes and .pkgmeta are tracked and would ship, .superpowers and .pytest_cache sit untracked at root | `packaging` | Add .gitattributes, .claude, .superpowers and .pytest_cache to ignore, plus a comment covering .pkgmeta itself |
| PanelMaster | `PANELMASTER-A-04` | A | Low † | `.pkgmeta:5-12` — Root dot-entries are .gitattributes, .gitignore, .luacheckrc, .pkgmeta; the ignore list names only the middle two | `packaging` | Add .gitattributes to the ignore list with the standard's comment, and justify .pkgmeta's own presence in a comment. |
| PrettyChat | `PRETTYCHAT-A-04` | A | Low † | `.pkgmeta:8-32` — The ignore block lists .luacheckrc, .gitignore, .gitattributes, docs, tests, _dev, *.bak, GlobalStrings and media art — no .claude, no .pkgmeta. | `packaging` | Add - .claude to the ignore block with a comment, and give .pkgmeta itself a row or a stated justification. |
| WhatGroup | `WHATGROUP-R-09` | R | Low | `.pkgmeta:6-19` — logos png/jpg ignored as client-unloadable; 880K of screenshots in those same formats are not, nor are CLAUDE.md and DEPENDENCIES.md. Three of the four repos shipping unignored screenshots ship more: KickCD 7.5M, LootHistory 5.9M, AbsorbTracker 2.0M. | `packaging` | Add media/screenshots, CLAUDE.md and DEPENDENCIES.md to the ignore list; keep README.md and LICENSE, which players do read. |

**† Regraded or corrected in triage.** `ABSORBTRACKER-A-01` — audit said low; **held at medium, on corrected evidence.** The triage grounds — "every player downloads 2.8MB of internal diffs" — are false: .superpowers and .claude are gitignored and wholly untracked here, exactly as in the three repos Part 3 rejects the identical claim for, and the directory is 60 files with 30 review-*.diff rather than 62 mostly-diffs. Medium survives on what was measured instead: this repo ships 2.0M of tracked, unignored media/screenshots, which is real end-user reach, and it is one of four repos doing so. `PANELMASTER-A-04` — narrowed: .claude and .superpowers do not exist in this repo, and scope drops to addon-local. `PRETTYCHAT-A-04` — Kept low. .claude holds only settings.local.json, so the shipped payload is negligible.

## C12 · Tab-strip geometry cannot be tested: the shared mock answers GetHeight 0 — 4 findings, 5 repos **[COLLECTION]**

tests/_kit/mock_base.lua returns 0 from GetHeight for every frame and never writes a height on SetAtlas, so OptionsWidgets' atlas-derived tab pitch always falls back and any options-ui-§13 invariance assertion would pass vacuously. Four repos filed the missing case; none can write one until the kit's fidelity moves.

`tests/_kit/mock_base.lua:97` is `function f:GetHeight() return 0 end` for every frame, and the kit defines no `SetAtlas` at all, so `OptionsWidgets.lua:433-442`'s atlas-derived tab pitch always takes its `L.TAB_H` fallback and any `options-ui-§13` invariance assertion passes vacuously. Four repos filed the missing case and none can write one. The fix is not additive: roughly 308 test files across ten repos lean on `GetHeight` answering zero.

*Repos* AbsorbTracker, MultiMeters, PanelMaster, PrettyChat, LibKa0s · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-10` | A | Low | `tests/test_widgets.lua:770` — Only assertTrue(ctx.chromeHeight > 0, ...); nothing asserts band height and row y offsets equal across every selection | `options-ui-§13` | Add a wrapping-page case asserting chromeHeight and each row's y offset are identical per selection; vary mock heights so it can fail. |
| MultiMeters | `MULTIMETERS-A-08` | A | Low | `tests/test_options_panel.lua:630-640` — Confirmed: nearest case asserts activeTab and #__tabKids >= 2 only; grep for wrap in that file returns zero hits. | `options-ui-§13` | Make wow_mock answer different selected/unselected atlas heights, then assert chrome band and every row y offset are selection-invariant. |
| PanelMaster | `PANELMASTER-A-07` | A | Low † | `tests/wow_mock.lua:165; tests/_kit/mock_base.lua:97` — OptionsWidgets.lua:434-435 measures pitch from unselected atlas art, but the mock's GetHeight answers 0 for any atlas, so tabArtHeight always falls back | `options-ui-§13` | Give wow_mock a per-atlas height, then assert band height and every row y-offset stay equal across active tabs; verify red under the TAB_ATLAS mutation. |
| PrettyChat | `PRETTYCHAT-A-10` | A | Low † | `tests/_kit/mock_base.lua:97; tests/test_panel.lua (absent case)` — mock_base.lua:97 is function f:GetHeight() return 0 end for every frame, so any geometry-invariance assertion would pass vacuously. | `options-ui-§13` | Give atlas-bearing textures per-atlas heights in tests/wow_mock.lua, then assert band and row offsets are identical across selections. |

**† Regraded or corrected in triage.** `PANELMASTER-A-07` — cited locus corrected: wow_mock's reader("__h") is the effective definition, and SetAtlas never writes __h. `PRETTYCHAT-A-10` — Kept low. A real gap, topical after the tab revamp, but the fix touches the shared kit's fidelity contract, not just this repo.

## C13 · Perf-panel decorate hook re-draws the library's own close button — 2 findings, 3 repos **[COLLECTION]**

Three of the nine addons carry a core/PerfSetup.lua decorate hook whose body duplicates PerfPanel.lua's else-branch anchor for anchor; the descriptor already supplies the addonName the library needs.

*Repos* AbsorbTracker, KickCD, MultiMeters · *disposition* `per-addon` · *effort* S · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-06` | A | Low | `core/PerfSetup.lua:149-159` — Hook body matches libs/LibKa0s/PerfPanel.lua:191-196 anchor-for-anchor; descriptor supplies addonName at PerfSetup.lua:43 | `performance-§4` | Delete the decorate field; let the library's else-branch draw it. Assert the descriptor has addonName and no decorate. |
| KickCD | `KICKCD-A-06` | A | Low | `core/PerfSetup.lua:217-226` — Hook body is only a close button; PerfPanel.lua:191-194 draws the identical control, and the descriptor's `name = addonName` (:69) feeds the library's `d.addonName or d.name` | `performance-§4` | Delete the decorate field and its comment block; the library's else arm resolves the folder name via d.name |

## C14 · Deviation registers cite dead IDs, spent triggers and unratified decisions — 11 findings, 7 repos **[COLLECTION]**

ARCHITECTURE.md's register is the collection's single ratification store, and nothing verifies it: rows cite audit IDs that exist in no bundle, triggers that have already fired, rules the standard has since changed, and real declines live only in code comments or closed issues.

The register is the collection's ratification store and nothing reads it back. `audit-review-history.md:32-39` mandates resolving each row's *rule* citation against the current standard and nothing else; `documentation.md:150` defines the Re-check trigger as "the condition that ends the deviation, stated so a reader can tell whether it has already fired" — with no rule requiring anyone to evaluate it, and none requiring a cited evidence id to resolve. Both live failures below are of exactly those two unchecked kinds.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-09` | A | Low | `docs/ARCHITECTURE.md:354,356,357` — Rows cite AT-A-10 / AT-A-03 / AT-A-09; grep over docs/audits/2026-08-05/ yields only AT-30 through AT-50, no AT-A-* anywhere | `documentation-§3` | Correct to the real IDs and add a test_docs case asserting every cited deviation ID resolves in docs/audits/. |
| BankLedger | `BANKLEDGER-A-01` | A | Low † | `docs/ARCHITECTURE.md:228-232` — Register holds only performance-§12, savedvariables-§2, options-ui-§12; the rationale lives at locales/enUS.lua:8-13, which the register itself says does not ratify. | `localization-§3` | Add a localization-§1 row: decided date, trigger 'first non-English locale file in locales/'; close the tracking issue state:done. |
| ConsumableMaster | `CONSUMABLEMASTER-A-04` | A | Low | `docs/ARCHITECTURE.md:316` — Verified upstream: standards/standards/toc-file.md:129 now reads "compliant and needs no deviation-register row" once the TOC comment is present. | `documentation-§3` | Delete the row; the rationale already lives in the TOC comments at :42-48 and :68-70, which is where the section now puts it. |
| KickCD | `KICKCD-A-10` | A | Low | `docs/ARCHITECTURE.md:241, :244-261` — The row and the note under the table both say it is a recorded decision under review, not a ratified deviation; library-less load registers 112 of 228 rows | `options-ui-§1` | Upstream ruling only: ship composers without the Options major, or state which options-ui-§1 MUST wins. No local fix |
| KickCD | `KICKCD-A-11` | A | Low | `KickCD.toc:14` — `# ## X-Wago-ID: <id>   -- TODO(KCD-18): add once published on Wago`; the ledger is retired collection-wide | `audit-review-history` | Open a state:triaged issue and cite its number, or drop the marker and keep the bare comment |
| LootHistory | `LOOTHISTORY-A-03` | A | Low | `docs/ARCHITECTURE.md:389-396` — gh confirms issue #21 closed state:will-not-do declining SetRenderer for AH Price; the register's five rows cover architecture-§5, performance-§12 and options-ui only | `documentation-§3` | File the register row citing #21 with a re-check trigger, or close #21 as superseded if the page now routes through O.SetRenderer |
| LootHistory | `LOOTHISTORY-A-04` | A | Low | `locales/enUS.lua:7-11` — The comment calls English-only "an accepted scope decision, not an oversight"; no register row cites localization-§1 | `documentation-§3`, `localization-§3` | Add the register row citing localization-§1, trigger "the first non-English locale file added to locales/", and shorten the comment to point at it |
| LootHistory | `LOOTHISTORY-A-10` | A | Low † | `docs/ARCHITECTURE.md:392` — Trigger reads "the standard names a session-only row kind"; upstream options-ui.md names session-only rows outright at three places, including a debug console toggle | `documentation-§3`, `audit-review-history` | Retire the row into the "Retired, deliberately not rows" paragraph citing options-ui, and correct the matching prose above the table |
| MultiMeters | `MULTIMETERS-A-10` | A | Low | `docs/ARCHITECTURE.md:676-682` — grep for audits and reviews in ARCHITECTURE.md returns no hits; superpowers/ and revendor/ rows are present in the Topic detail table. | `documentation-§3` | Add one audits/ row and one reviews/ row to the Topic detail table beside revendor/. Never a row per bundle. |
| MultiMeters | `MULTIMETERS-A-11` | A | Low | `GitHub issue #17 (bug, state:untriaged, severity:medium)` — gh confirms #17 OPEN, state:untriaged, "Both allocation ceilings in tests/perf.lua are breached on master". perf.lua exits 0; both figures under ceiling. | `audit-review-history` | Re-run, then close #17 as state:done citing the run, or re-triage it with the measurement that still fails. |
| PanelMaster | `PANELMASTER-A-06` | A | Low | `docs/ARCHITECTURE.md:199` — Row reads "The addon is pre-release, so the rule is not yet engaged"; tag 1.0.0-release exists and no TODO.md does | `audit-review-history` | Retire the row; the register is the single home of live ratified deviations, not a history of settled ones. |

**† Regraded or corrected in triage.** `BANKLEDGER-A-01` — scope narrowed from likely-cross-cutting: this is one missing row in this repo's own register. `LOOTHISTORY-A-10` — Substance verified against the sibling standards checkout; the exact §12/§15 numbering the audit cites I did not map to section numbers.

## C15 · README and ARCHITECTURE structure against documentation-§1/§3 — 8 findings, 5 repos **[COLLECTION]**

Headings, tables and section names drifted from what documentation-§1/§3 name: extra changelogs, tab-granular settings tables where page granularity is asked for, missing Overview/Module map headings, oversized unspilled ARCHITECTURE.md sections.

*Repos* KickCD, LootHistory, MultiMeters, PrettyChat, WhatGroup · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| KickCD | `KICKCD-A-07` | A | Low † | `docs/ARCHITECTURE.md:7, :22, :286` — No `## Overview` and no `## Module map`; material sits under What it does / Subsystems at a glance / Load order. All five sibling addons do have `## Overview` | `documentation-§3` | Rename the two headings, keep Load order as an extra section, then sweep inbound anchors and the map row |
| LootHistory | `LOOTHISTORY-A-07` | A | Low | `README.md:36, README.md:141` — ## Unreleased is a third changelog beside What's new in 1.2.0 and Version History; ## Auction-house pricing sits between Usage and How attribution works | `documentation-§1` | Promote the Unreleased bullets into the next bump's What's new plus a Version History row; fold Auction-house pricing into How attribution works |
| MultiMeters | `MULTIMETERS-A-06` | A | Low | `docs/ARCHITECTURE.md:452-636` — wc confirms 787 lines. Known limitations is the largest block, with Taint notes, Event subscriptions and Overview behind it. | `documentation-§3` | Spill Known limitations and Overview to scope.md, Taint notes to midnight-quirks.md, Event subscriptions to module-map.md; one link each. |
| PrettyChat | `PRETTYCHAT-A-08` | A | Low | `README.md:71-82` — An eight-row Tab table sits directly below the compliant page-granularity table at :66-69. Confirmed verbatim. | `documentation-§1` | Move anything not already in docs/settings-panel.md across, then delete README.md:71-82, keeping :66-69 and the paragraph at :84. |
| PrettyChat | `PRETTYCHAT-A-11` | A | Low | `CLAUDE.md:3` — Line 3 is a description of the addon; the adherence statement first appears at :7-8 inside the Standards compliance section. | `documentation-§2` | Insert a one-sentence adherence line above the Standards compliance heading; leave the existing :7-8 paragraph in place. |
| WhatGroup | `WHATGROUP-A-07` | A | Low | `docs/ARCHITECTURE.md:352` — The row's Rule cell reads standalone-windows-§33 and its body also cites §29 and §32; the standards text is outside this repo, so numbering is unverified here. | `documentation-§3` | If standalone-windows.md carries no numbered subsections, drop to the bare filename in all three citations and quote the SHOULD's words instead. |
| WhatGroup | `WHATGROUP-A-10` | A | Low | `README.md:121 vs README.md:21` — :121 says "add a delay under Notify"; :21 says "Set a delay under Chat"; Schema.lua files notify.delay under group Chat. | `documentation-§1` | Correct README.md:121 to Chat. |
| WhatGroup | `WHATGROUP-A-11` | A | Low | `README.md:69-73` — Header is Tab \| Covers with three rows for the one General subcategory; §1 asks for a page-granular table and puts tabs in docs/settings-panel.md. | `documentation-§1` | Collapse to one row per page and link docs/settings-panel.md, or take the Tab-versus-Page header question upstream first. |

**† Regraded or corrected in triage.** `KICKCD-A-07` — scope narrowed from likely-cross-cutting: siblings comply, KickCD is the outlier.

## C16 · documentation-§3 names three tiers; every repo needs a fourth table — 2 findings, 2 repos

Two repos independently added a Verification and record table because the standard's tier model has nowhere to put testing.md, smoke-tests.md and the run record. The gap is upstream, not in the addons.

*Repos* PrettyChat, WhatGroup · *disposition* `standards-upstream` · *effort* S · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| PrettyChat | `PRETTYCHAT-A-09` | A | Low † | `docs/ARCHITECTURE.md:189-195` — A Verification and record table exists beside the three canonical tables, holding testing.md, smoke-tests.md and the rest. | `documentation-§3` | Raise upstream that documentation-§3 should name a Verification table; meanwhile keep it with a note citing the issue. |
| WhatGroup | `WHATGROUP-A-15` | A | Low | `docs/ARCHITECTURE.md:292-335` — Four headed tables: Tier 1, Tier 2, Verification and record, Tier 3. §3 describes three tiers and places the record docs outside the tier model. | `documentation-§3` | Upstream only: name a fourth Verification and record table in §3 and say whether ARCHITECTURE.md registers itself. Nothing to change here. |

**† Regraded or corrected in triage.** `PRETTYCHAT-A-09` — Kept low. An upstream gap the repo papers over sensibly, not a repo defect.

## C17 · British spellings ship, and the prose gate that should catch them is a six-word list — 5 findings, 4 repos **[COLLECTION]**

localization-§5 asks for US spelling in authored English; four repos carry hits, including a public LibKa0s icon-catalog key ("minimise") and chat text a player reads. LibKa0s's own gate checks six substrings, none of which match the live hits.

*Repos* ConsumableMaster, KickCD, WhatGroup, LibKa0s · *disposition* `mixed` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| ConsumableMaster | `CONSUMABLEMASTER-A-02` | A | Low | `README.md:165; CLAUDE.md; docs/schema.md; tests/test_mediasetup.lua +7 files` — README.md:165 "Every colour here has a Use class color checkbox … class's colour". My sweep counts 25 sites, not 28; two hits are vendored libs. | `localization-§5` | Sweep the live files only; edit test case names at source and regenerate docs/test-cases.md. Skip libs/ and every frozen bundle. |
| KickCD | `KICKCD-A-03` | A | Low † | `docs/settings-panel.md (13), settings/Panel_Widgets.lua (5), docs/smoke-tests.md (4), docs/module-map.md (4), +7 files` — Case-insensitive colour\|behaviour sweep excluding libs/, tests/_kit and frozen bundles: 37 hits in 11 files, not the audit's 51 in 12 — its count folded in frozen audit/review bundles | `localization-§5` | Case-preserving sweep of the 11 live files; re-point the renamed settings-panel.md heading anchor. No locale key moves, no frozen bundle touched |
| WhatGroup | `WHATGROUP-A-09` | A | Low | `modules/Frame.lua:267; settings/Schema.lua:115; settings/OptionsSetup.lua:92` — grey, behaviour, colour — all three are comment text; grep finds no player-facing string affected in core, modules, settings, defaults or locales. | `localization-§5` | One sweep over source, live docs and tests; regenerate docs/test-cases.md if a test case name changes. |
| LibKa0s | `LIBKA0S-A-08` | A | Low † | `LibKa0s/Media.lua:94; LibKa0s/Perf.lua:723,864,948,1029,1063` — "minimise" is a lib.ICONS catalog key; "unlabelled" and "CANCELLED" reach chat text a player reads | `localization-§5` | Sweep comments and strings; add "minimize" as a live key beside "minimise" per the additive-only rule, deprecate the old one |
| LibKa0s | `LIBKA0S-A-08d` | A | Low | `tests/test_prose.lua:113` — BRITISH = { colour, grey, behaviour, synthesise, normalis, recognis }; the suite passes green while minimise, unlabelled and CANCELLED ship | `testing-§12` | Widen the list to at least minimis, centre, cancelled, labelled, travelled, organis, optimis, initialis, customis |

**† Regraded or corrected in triage.** `KICKCD-A-03` — count corrected downward; severity unchanged. `LIBKA0S-A-08` — was medium; lowered to low — zero functional impact, and the catalog key cannot be removed without breaking consumers.

## C18 · Localization routing gaps: unwrapped strings and missing locale keys — 4 findings, 4 repos **[COLLECTION]**

User-facing text bypasses the L seam in four repos — bare FontString literals, slash usage lines, desc keys used but never defined — and the coverage tests only scan for L["…"] call sites, so an unwrapped string is invisible to them.

*Repos* ConsumableMaster, KickCD, LootHistory, PrettyChat · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| ConsumableMaster | `CONSUMABLEMASTER-R-02` | R | Low † | `modules/KCMMacroDragIcon.lua:74,77; modules/KCMItemRow.lua:171,173,175,228` — Neither file takes an L upvalue; literals "Macro not created yet", "Drag to action bar", "MH+OH", "MH", "OH", "[Loading]" go straight into FontStrings. | `localization` | Take local L = KCM.L in both files, wrap the six literals with colour escapes outside the key. Weigh the ASCII hand-tag rationale first. |
| KickCD | `KICKCD-R-03` | R | Low † | `settings/Castbar.lua:219,227,302 vs locales/enUS.lua:340,342,347` — Used descs carry the 'Overridden by…' / 'Capped at…' clauses; enUS defines the superseded short sentences. locales/enUS.lua:15 __index returns the key | `localization`, `anti-patterns #2` | Add the three current sentences, drop the three superseded keys, and add a TOC-derived L[...] coverage case that is seen red first |
| LootHistory | `LOOTHISTORY-R-12` | R | Low † | `core/Compat.lua:229, modules/Attribution.lua:66-67` — Lua %s misses U+00A0; a surviving NBSP breaks the exact WARBAND_LINES[lower] lookup and the dropLast suffix strip in seedToken | — | Match [ \194\160] rather than %s in both trims; do not add more locale literals to the fallback tables |
| PrettyChat | `PRETTYCHAT-R-04` | R | Medium † | `tests/test_locale.lua:44-50; docs/ARCHITECTURE.md:228; settings/Slash.lua:241,278-284,349,365,379` — callSites comes from gmatch of L["..."] only; the register row asserts an unwrapped string is red. Slash.lua's usage lines are bare English. | `localization-§1` | Correct the localization-§1 register row to state what is actually verified, then either wrap the Slash.lua sentences or record them as known residue. |

**† Regraded or corrected in triage.** `CONSUMABLEMASTER-R-02` — was medium; enUS is the only locale that ships, so nothing is user-visible until a second one exists. `KICKCD-R-03` — medium; the L metatable falls back to the key, so enUS renders the correct sentence today — the exposure is a future translator. `LOOTHISTORY-R-12` — Lowered from medium: WARBAND_LINES is only the fallback for nil globals, and the seedToken path ends in a substring find, not equality. `PRETTYCHAT-R-04` — Merged: one defect, two halves. R-06's premise was wrong — the fragments are unwrapped, not translated, which is why R-04's scan misses them.

## C19 · Comments and rationales describing code that has moved or gone — 13 findings, 8 repos **[COLLECTION]**

The collection's comment style carries file:line citations and design arguments in prose; nothing verifies them, so they rot silently. Roughly forty sites across seven repos now name functions, lines or hazards that no longer exist.

*Repos* AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-07` | R | Low | `core/Units.lua:74 and :108` — APPEARANCE_KEYS at :25-31 holds 19 entries and the header at :19 says nineteen; both doc comments say fifteen | — | Make both read nineteen, or drop the prose count entirely and let Units.APPEARANCE_KEYS be the single answer. |
| AbsorbTracker | `ABSORBTRACKER-R-09` | R | Low | `core/AbsorbTracker.lua:69` — Says "CreateOptionsPanel is not safely re-callable"; Options.lua:838-844 documents it idempotent with `if mainCategory then return end` | — | Rewrite the parenthetical: the extraction is for test isolation, and LibKa0s-Options owns the idempotence guard. |
| BankLedger | `BANKLEDGER-R-10` | R | Low | `settings/OptionsSetup.lua:180-181` — Says MasterControls is REACHED via ComposeMaster, but the stub arm returns at :214 and ComposeMaster runs at :227 on the live arm only. | — | Reword to say the stub member is unreached on the degraded path; keep the (correct) consequence paragraph. |
| ConsumableMaster | `CONSUMABLEMASTER-A-08` | A | Low | `settings/Category.lua:156, modules/MacroManager.lua:331, settings/Panel.lua:690,724 +5 sites` — Confirmed shape — "the standard §12 zero-alloc rule these paths are written to". My count is 9 code sites, not the audit's 13. | `documentation-§6` | Expand each to filename-§N after resolving it against the standard; the TECHNICAL_DESIGN and smoke-tests numberings are out of scope. |
| ConsumableMaster | `CONSUMABLEMASTER-R-04` | R | Low † | `core/DebugLogSetup.lua:93,113; modules/MacroBarButton.lua:115,146; tests/test_surface_parity.lua:84,126` — DebugLogSetup:113 cites PerfSetup.lua:98, which reads slash = "/cm". MacroBarFlyout:413 is local edge; Slash.lua:305 is printHelp. | `documentation` | Cite the symbol rather than the number wherever the name is unambiguous; re-derive the genuinely positional ones against today's tree. |
| ConsumableMaster | `CONSUMABLEMASTER-R-13` | R | Low | `tests/test_surface_parity.lua:169-174 and :182-186` — The "Live-only ON PURPOSE … the panel is not registered AT ALL" argument appears twice, the second copy leading into a different point. | — | Delete the copy at :169-174, keeping the one that leads into the what-is-NOT-on-this-list argument. |
| LootHistory | `LOOTHISTORY-R-13` | R | Low | `modules/Browser.lua:1162` — Comment says frame:Hide() does not reach the popup; Browser.lua:1074-1077 hooks the same frame's OnHide straight to NS.CloseMenu | — | Correct the comment to name the OnHide hook as the guard, or drop the now-redundant call |
| LootHistory | `LOOTHISTORY-R-14` | R | Low † | `defaults/Global.lua:6-9, core/Database.lua:195` — Global.lua says the v1-to-v2 migration "bumps the stamp to 2"; the suite asserts schemaVersion 8. Database.lua says "v6->v9"; there is no v9 | — | Correct both, and add one line stating that the shipped schemaVersion = 1 floor is deliberate |
| LootHistory | `LOOTHISTORY-R-17` | R | Low | `modules/Attribution.lua:127-140` — Reads State.lootContext, checks expires against GetTime, returns it, never clears; TTL expiry alone ends the context | — | Rename to PeekContext across its bounded call set, or add one line stating the context is TTL-scoped by design |
| MultiMeters | `MULTIMETERS-R-11` | R | Low | `tests/test_vendor_sync.lua:14` — Header quotes "v1.8.3"; CLAUDE.md:52 says v1.25.0. The gate reads the live provenance line, so it passes correctly. | — | Update the quoted version in the comment to v1.25.0 so it names the version actually under test. |
| PanelMaster | `PANELMASTER-R-07` | R | Low | `settings/OptionsSetup.lua:190-195` — Comment names Sl:CliResetAll reaching session-only rows through each row's set; no .lua file defines it, and Sl:DoResetAll is db:ResetProfile() | `options-ui-§12` | Restate the reason as the profile-reset-vs-row-walk distinction and name where session state is actually cleared. |
| PrettyChat | `PRETTYCHAT-R-09` | R | Low † | `core/MediaSetup.lua:54-58 vs settings/Panel.lua:31-32` — The comment says the seam exists so a window asks the catalog rather than typing a path; Panel.lua:31 concatenates a .tga path by hand. | — | Name Panel.lua's LOGO_PATH in the comment and say why per-addon branding art sits outside the shared icon catalog. |
| PrettyChat | `PRETTYCHAT-R-10` | R | Low | `tests/test_vendor_sync.lua:25 vs CLAUDE.md:30` — The comment illustrates the gate's input as v1.10.2; CLAUDE.md:30 reads v1.25.0. The gate matches by pattern, so it passed today. | — | Drop the version from the illustrative quote, or cite the match pattern rather than one instance of it. |

**† Regraded or corrected in triage.** `CONSUMABLEMASTER-R-04` — was medium; comment-only drift, invisible to any running session. `LOOTHISTORY-R-14` — Cited line was :193; the comment is at :195. `PRETTYCHAT-R-09` — Kept low, evidence corrected: the comment does not say what the review quoted. It says PrettyChat builds no frames of its own — a milder tension.

## C20 · Dead exports, dead arms and hand-copied helpers — 7 findings, 5 repos **[COLLECTION]**

Seams published for a caller that never arrived, fallback branches the load order makes unreachable, and one function that is a hand-copy of the one above it.

*Repos* AbsorbTracker, ConsumableMaster, KickCD, MultiMeters, PrettyChat · *disposition* `per-addon` · *effort* S · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-10` | R | Low | `settings/Schema.lua:101-111; only caller tests/test_schema.lua:524-530` — grep across the repo excluding docs finds exactly two hits: the definition and the one test | — | Delete the function, its case and its doc entries; regenerate docs/test-cases.md and move the README badge in the same commit. |
| AbsorbTracker | `ABSORBTRACKER-R-11` | R | Low | `core/Database.lua:95-112 vs :118-135` — Same store walk; the four-line AceDB db.sv.profiles comment block is byte-identical in both, though not at the lines the review cited | — | Move forEachProfile above it and reduce migrateAllProfiles to forEachProfile(NS.MigrateProfileToV3); delete the duplicated comment block. |
| ConsumableMaster | `CONSUMABLEMASTER-R-03` | R | Low † | `tests/test_surface_parity.lua:44-52` — The file's own documented grep returns six members; CORE_SEAM lists five. Only core/CoreSetup.lua and tests reference MakeCloseButton. | `testing` | Add MakeCloseButton to CORE_SEAM plus a CORE_LIVE_ONLY entry recording the deliberate deadness, carrying the argument from test_coresetup.lua:154-206. |
| KickCD | `KICKCD-A-08` | A | Low | `modules/Castbar_Debug.lua:125` — core/CoreSetup.lua defines Util.print at :112 (degraded) and :171 (library), so the `or _G.print` arm is unreachable; ARCHITECTURE.md:278-284 already records it as open | `events-frames-taint-§8` | Reduce to `local print = NS.Util.print` and delete the now-spent note at docs/ARCHITECTURE.md:278-284 |
| KickCD | `KICKCD-R-09` | R | Low | `tests/test_bus.lua:48` — 'NewBusTarget lands in Sprint 3' guards a branch; NS.NewBusTarget is declared and used, so the branch never runs | `testing` | Delete the branch and comment; assert NS.NewBusTarget exists directly. Case count unchanged |
| PrettyChat | `PRETTYCHAT-A-05` | A | Low † | `core/CoreSetup.lua:74-85 vs :111-113; tests/test_libka0s.lua:683-689` — The degraded branch publishes NS.Format explicitly then returns at :85; MakeCloseButton is published at :111, past the return. coreSurface omits it. | `testing-§8` | Publish a nil-returning MakeCloseButton in the stub branch and add it to coreSurface and the non-vacuity key list. |
| PrettyChat | `PRETTYCHAT-R-11` | R | Low | `core/MediaSetup.lua:62 (NS.Icon); core/CoreSetup.lua:111 (NS.MakeCloseButton), :78 and :132 (NS.Format)` — Confirmed by grep over core/ defaults/ locales/ modules/ settings/: no call site for any of the three. Each is argued in place. | — | Leave them and record the intent in docs/module-map.md so a later dead-code sweep does not misread them as cruft. |

**† Regraded or corrected in triage.** `CONSUMABLEMASTER-R-03` — was medium; a test blind spot over a wrapper with zero production call sites is doubly inert. `PRETTYCHAT-A-05` — Kept low. Nothing calls it yet, so the asymmetry is latent — precisely the risk the file's own comment at :74-77 names for NS.Format.

## C21 · Tests that assert less than their names claim — 9 findings, 6 repos **[COLLECTION]**

Cases that pcall and assert only ok, sweeps that skip silently when a file is missing, hand-maintained suite lists pinned in neither direction, and restores that run only on the green path — all of which stay green under the very change they exist to catch.

*Repos* KickCD, LootHistory, MultiMeters, PanelMaster, WhatGroup, LibKa0s · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| KickCD | `KICKCD-R-04` | R | Low † | `tests/test_schema.lua:581,630; tests/test_options_panel.lua:552` — `if cfg then cfg.link = before end` is the last statement of each body; tests/_kit/framework.lua:613 pcalls t.fn, so a red skips it | `testing` | Take a fresh T.load(true) instance per case, or restore in a guaranteed-run wrapper; weaken no assertion |
| LootHistory | `LOOTHISTORY-R-08` | R | Medium † | `modules/Attribution.lua:327-361` — grep over core, modules, settings, tests finds the definition and core/LootHistory.lua:41 only; 7 events, 1 unit frame and 5 hooks untested | `testing-§8` | Add an integration case calling Enable() against the mock, asserting the registered event set and the hooked globals |
| LootHistory | `LOOTHISTORY-R-09` | R | Low † | `tests/run.lua:43-47` — Comment says "the lifecycle kick the client's OnInitialize does"; OnInitialize calls four things, the runner three, omitting NS.Slash:Register | `testing-§9` | Publish the kick through Kit.expose and pin it in test_harness.lua against OnInitialize's actual call set |
| MultiMeters | `MULTIMETERS-R-14` | R | Low | `tests/test_diagnostics.lua:1373-1381` — Confirmed: nulls UnitIsFeignDeath and UnitIsDead, then asserts ok alone. Stays green if the roster block prints nothing at all. | `testing-§12` | Assert on the printed roster lines as well as on not raising, so an empty report reddens the case. |
| PanelMaster | `PANELMASTER-R-04` | R | Low † | `core/Database.lua:141` — tostring(NS.version) where NS.Version() exists at core/EnvSetup.lua:71; test_database.lua:160 asserts the same constant, so it cannot go red | `library-stack-§7` | Call NS.Version(); point the mock TOC version at a different string so the existing case can actually fail. |
| WhatGroup | `WHATGROUP-R-05` | R | Low † | `tests/run.lua:59-77` — 17 suites listed; test_harness pins the TOC list, the LibKa0s list and load order, but grep finds nothing pinning the suite list itself. | `testing-§9` | Add the two-direction pin testing-§9's reference implementations use, so a suite dropped from the list or a file with no entry goes red. |
| WhatGroup | `WHATGROUP-R-10` | R | Low | `tests/test_mediasetup.lua:147-155` — Titled "ships no private copy of the shared art" but asserts only on media/fonts/JetBrainsMono-Regular.ttf; any other private face or catalog icon passes. | `testing-§12` | Scan media/ for any .ttf/.otf and any filename in the library ICONS catalog; add the red-under note the case is missing. |
| WhatGroup | `WHATGROUP-R-11` | R | Low | `tests/test_libka0s.lua:806` — if src then wraps the assertion, so a renamed seam file narrows the sweep with no red; SEAM_FILES at :22-27 is hand-maintained. | `testing-§9` | assertTrue(src ~= nil) before the assertNil, and derive SEAM_FILES from the TOC-derived load list instead of listing four paths. |
| LibKa0s | `LIBKA0S-R-11` | R | Low | `tests/run.lua:110-118` — The XML load list at :24 is derived and commented; the 22-name suite list is hand-typed, complete today, guarded by Kit.assertSuiteInventory at framework.lua:678 | `testing-§9` | Add one comment naming Kit.assertSuiteInventory as what holds the hand-typed list honest, so the next reader need not go find it |

**† Regraded or corrected in triage.** `KICKCD-R-04` — medium; only bites during an already-red run, as misleading cascade failures. `LOOTHISTORY-R-08` — Scope narrowed from likely-cross-cutting: Attribution is this addon's own module. `LOOTHISTORY-R-09` — Lowered from medium: ADDON_FILES is already TOC-derived and pinned, so this is not "a fourth hand-maintained list", just one three-line drift. `PANELMASTER-R-04` — medium to low: the constant and the TOC agree today, so the only live cost is a debug line that would lie after a TOC-only bump. `WHATGROUP-R-05` — medium → low: a latent silent-skip risk, not a live one; all 17 suites run today.

## C22 · layout-§1's 1500-LOC cap breached in four repos, and unclassified for a library — 6 findings, 5 repos **[COLLECTION]**

Eleven tracked files sit over the cap, one of them past its own ratified split trigger, and library-stack-§7's applicability lists say nothing about whether layout binds a library repo at all.

**The census is wrong in both directions.** `wc -l` over every tracked `.lua` outside `libs/` and `tests/_kit/` finds **18** files over 1500, not eleven — and two of the five repos the cluster names have none. KickCD's largest is `modules/Castbar.lua` at 1320 and PanelMaster's is `tests/test_artwork.lua` at 1356, so `KICKCD-R-02` (a CCN-18 test function) and `PANELMASTER-R-05` (`settings/PanelEditor.lua` at 1350, past its own ratified split trigger) are on-notice-band and complexity findings, not cap breaches. The unreported breaches are seven MultiMeters test files — `tests/test_window.lua` 2737, `test_tooltip.lua` 2708, `wow_mock.lua` 2265, `test_row.lua` 1606, `test_aggregator.lua` 1605, `test_schema.lua` 1573, `test_export.lua` 1509 — and `PrettyChat/GlobalStrings/GlobalStrings.lua` at 23,842, which is generated, unloaded and `.pkgmeta`-ignored. `layout.md:55` caps "any single `.lua` file" with no carve-out for tests, generated data or a library repo, and the collection answered that silence three different ways.

*Repos* ConsumableMaster, KickCD, MultiMeters, PanelMaster, LibKa0s · *disposition* `mixed` · *effort* L · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| ConsumableMaster | `CONSUMABLEMASTER-A-06` | A | Low | `tests/test_macrobar.lua` — wc -l confirms 1894 against the watch list's recorded 1688; RESULTS.md:155 calls it unowned and no issue tracks it. | `layout-§1` | Peel into test_macrobar_flyout.lua and test_macrobar_button.lua with the case count unchanged, or open a tracked issue plus a register row. |
| KickCD | `KICKCD-R-02` | R | Low † | `tests/test_schema.lua:595` — My lizard run: 29 NLOC CCN 18 (anonymous)@595-631; the function's own comment at :613 names the seam to split on | `automated-tests-§3`, `testing-§7`, `performance-§10` | Split the case along the seam its own comment names; regenerate docs/test-cases.md and the README badge in the same change |
| MultiMeters | `MULTIMETERS-R-08` | R | Low † | `settings/Schema.lua (3069), modules/Tooltip.lua (2652), modules/Window.lua (2644), modules/Aggregator.lua (2058), modules/Export.lua (1743), core/Diagnostics.lua (1726), modules/Row.lua (1702)` — wc -l confirms all seven figures exactly as cited. Diagnostics.lua crossed the cap in 81642e6. | `layout-§1` | Peel each along the seam its own header names: Diagnostics by probe, Schema by page, Window's header out, Tooltip's column builders. One per commit. |
| PanelMaster | `PANELMASTER-R-05` | R | Medium † | `settings/PanelEditor.lua` — 1350 LOC confirmed; RESULTS.md watch list records 1091 and says "if the next change also grows it, execute the split rather than re-accept" | `layout-§1` | Peel along the editor's own section boundaries into siblings under settings/, annotating each new TOC line. No part2 helper. |
| LibKa0s | `LIBKA0S-R-15` | R | Medium | `WowAddonStandards standards/standards/library-stack.md:175-226` — Applies list names 8 sections, does-not-apply names 9; layout, architecture, performance, compat, anti-patterns, public-api and more appear in neither | `library-stack-§7` | Add a third disposition naming the remaining sections, or state a default with the two lists as exceptions; then peel or ratify here |
| LibKa0s | `LIBKA0S-A-03` | A | Low † | `LibKa0s/OptionsWidgets.lua (1838), tests/test_options_widgets.lua (2287)` — manifest.json records "overCapFiles": 2; nothing reads it and the RESULTS.md watch list denies it. Whether layout binds a library repo is R-15's open question. | `layout-§1` | Peel OptionsWidgets at the tab-strip seam (:593+) into OptionsTabs.lua minor 1; split the test suite by widget family |

**† Regraded or corrected in triage.** `KICKCD-R-02` — medium; zero player impact — test-only code, though it will block the next version bump's release gate. `MULTIMETERS-R-08` — review had medium; wc verified every figure, but nothing a player runs changes when a file is split. `PANELMASTER-R-05` — kept medium: no player impact, but the file's own recorded commitment has fired rather than merely being on notice. `LIBKA0S-A-03` — held at low — zero player impact, and the binding rule is itself unclassified upstream.

## C23 · LibKa0s tab strip creates frames per click and pools none — 2 findings, 1 repo

TabStrip rebuilds every button and the content panel on each click while releaseLedger only hides and reparents; the library ships a Pool major that its own widget code does not use, and there are three different release contracts inside one library.

*Repos* LibKa0s · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LibKa0s | `LIBKA0S-R-01` | R | Medium † | `LibKa0s/OptionsWidgets.lua:1050-1072 (TabStrip), :942 (makeTab), :643 (drawContentPanel), :874-880 (releaseLedger)` — TabStrip releases __tabKids then rebuilds every Button via makeTab and calls drawContentPanel; releaseLedger only Hide()/SetParent(nil). WoW never collects frames. | `library-stack-§7` | Acquire buttons and the panel from per-ctx LibKa0s-Pool-1.0 pools; split makeTab into newTabButton and dressTab; re-set OnClick each dress |
| LibKa0s | `LIBKA0S-R-05` | R | Low † | `LibKa0s/Widgets.lua:799-825 vs LibKa0s/OptionsWidgets.lua:874-880; LibKa0s/Pool.lua:49` — Widgets pools into handlePool/boxPool with an attic reparent; OptionsWidgets sets parent nil; LibKa0s-Pool-1.0 is referenced nowhere outside Pool.lua | `library-stack-§7` | Route both through LibKa0s-Pool-1.0, carrying the attic reparent and __row clear in ReleaseAll's before hook |

**† Regraded or corrected in triage.** `LIBKA0S-R-01` — was high; lowered to medium — a real permanent leak, but bounded by tab clicks while an options panel is open, not a hot frame path. `LIBKA0S-R-05` — was medium; lowered to low — Widgets' hand-rolled pool is correct; the reachable defect is R-01, and this is the duplication behind it.

## C24 · LibKa0s options and perf seam defects — 4 findings, 1 repo

A composed reset button renders live with a nil handler and silently does nothing, the widget printer swallows its own diagnostics, the perf capture arm allocates per bracket undocumented, and a deprecated spec API is called with no namespaced rung.

*Repos* LibKa0s · *disposition* `libka0s-upstream` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LibKa0s | `LIBKA0S-R-08` | R | Medium | `LibKa0s/OptionsCompose.lua:393-402; LibKa0s/OptionsWidgets.lua:1313-1319` — resetAll/resetPosition built regardless of spec.onResetAll/onResetPosition; makeBtn's OnClick returns early when spec.onClick is nil | `options-ui-§15` | Add lib.STRINGS.DEAD_BUTTON and report once at build time from makeBtn, following the EMPTY_DROPDOWN report-and-render precedent |
| LibKa0s | `LIBKA0S-A-10` | A | Low † | `LibKa0s/Perf.lua:615-618` — if GetSpecialization and GetSpecializationInfo then — no namespaced path, while Env.lua:60-66 models the C_AddOns shim for exactly this shape | `compat` | Take C_SpecializationInfo.GetSpecialization first, falling back to the global; add the read_global and a case |
| LibKa0s | `LIBKA0S-R-06` | R | Low † | `LibKa0s/OptionsWidgets.lua:696 vs LibKa0s/Options.lua:289-291` — local print = d.print or function() end — no type guard, no DEFAULT_CHAT_FRAME fallback; Options.lua has both. Discards NO_GROUPS, EMPTY_DROPDOWN, BUTTON_FAILED | — | Store the shell's constructed sink on the instance as O.__print and have __AttachWidgets read it rather than re-deriving from d |
| LibKa0s | `LIBKA0S-R-07` | R | Low † | `LibKa0s/Perf.lua:478` — openStack[#openStack+1] = { key = key, t0 = debugprofilestop() }, guarded by if not P.on then return end; only the dormant path is measured (test_perf_isolation.lua:66) | `performance-§2` | Reuse slots via a high-water free list; state the active-arm cost in the docstring; add an active-arm allocation case beside the dormant one |

**† Regraded or corrected in triage.** `LIBKA0S-A-10` — was medium; lowered to low — failure mode is ctx.spec == "?" in a diagnostic capture, already guarded. `LIBKA0S-R-06` — was medium; lowered to low — the swallowed lines are developer diagnostics, never player-facing. `LIBKA0S-R-07` — was medium; lowered to low — reachable only inside a player-initiated profiling capture, which is itself a diagnostic mode.

## C25 · Standards text out of date about LibKa0s, and LibKa0s out of date about the standard — 2 findings, 1 repo

library-stack.md's module inventory is one file behind the library it describes, and LibKa0s's own standards pointer names v2.28.0 against a live v2.38.0.

The missing file is `OptionsCompose.lua`. `LibKa0s/LibKa0s.xml` lists fourteen `Script` entries; `library-stack.md:70` says "ten LibStub majors across thirteen files" and `:82` gives the Options row `Options.lua, OptionsWidgets.lua, OptionsScroll.lua`. So the section describing the library's module set does not know about the file that holds C01.

*Repos* LibKa0s · *disposition* `standards-upstream` · *effort* S · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| LibKa0s | `LIBKA0S-A-14` | A | Low † | `WowAddonStandards standards/standards/library-stack.md:70,:82` — :70 says "ten majors across thirteen files"; LibKa0s.xml lists fourteen Script entries. :82 gives Options three files, omitting OptionsCompose.lua. | `library-stack-§7` | Correct :70 to fourteen and add OptionsCompose.lua to the Options row at :82; bump the standard version |
| LibKa0s | `LIBKA0S-R-10` | R | Low | `CLAUDE.md:3, README.md:3` — Both read v2.28.0; WowAddonStandards standards/STANDARDS.md:1 reads v2.38.0 (2026-09-02), and options-ui-§15-§18 cited in OptionsCompose.lua arrived at v2.38.0 | `documentation-§6` | Move both pointers to v2.38.0 and add a pointer check to docs/releasing.md's order so it moves on a schedule |

**† Regraded or corrected in triage.** `LIBKA0S-A-14` — R-14's evidence was wrong — OptionsScroll.lua IS in the table at :82; the absent file is OptionsCompose.lua, as the audit found.

## C26 · performance-§12 exemption pages no longer reproduce their own evidence — 5 findings, 4 repos **[COLLECTION]**

Each ratified perf exemption rests on a sweep pasted into docs/performance.md; five of them now miscount events or timers, cite moved files, or understate the work a handler does. The exemptions survive on merit; their evidence does not.

*Repos* BankLedger, LootHistory, PrettyChat, WhatGroup · *disposition* `per-addon` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| BankLedger | `BANKLEDGER-R-06` | R | Low | `docs/performance.md:39` — Row says core/Compat.lua LoadItem; the only C_Timer.After(0.4, cb) is core/ItemSetup.lua:67, and Compat only mentions the move. | `performance-§12` | Repoint the row at core/ItemSetup.lua:67; the combat-path reasoning is unchanged. |
| LootHistory | `LOOTHISTORY-R-06` | R | Medium † | `docs/performance.md:45` — Row says "one table insert"; Collector.lua:123-124 runs GetItemExtras (a C_TooltipInfo build via Compat.ScanBound) then GatherAll's three-addon cascade | `performance-§12` | Rewrite the row to name the tooltip build and the price cascade, then re-affirm criterion (a) explicitly rather than by omission |
| LootHistory | `LOOTHISTORY-R-05` | R | Low † | `docs/performance.md:40-60` — Page claims eleven events (13 registered, Browser.lua:1277-1278 missing) and four timers (five: ItemSetup.lua:71, Util.lua:242, OptionsSetup.lua:181) | `performance-§12` | Regenerate both tables from the page's own greps and re-resolve every file:line; Compat.lua:202 and OptionsSetup.lua:129 no longer exist |
| PrettyChat | `PRETTYCHAT-R-03` | R | Low † | `docs/performance.md:33-50 vs settings/Panel.lua:528-532` — I re-ran the page's own grep verbatim: it now returns Panel.lua:528,531,532. The page asserts zero C_Timer call in settings/. | `performance-§12` | Re-run the sweep, paste the real output, and give the one-shot C_Timer.After(0) a render-path disposition. |
| WhatGroup | `WHATGROUP-R-02` | R | Low † | `modules/Frame.lua:275` — PopulateFields (:664) arms before the visibility gate (:665); the combat-deferred replay (:315-330) arms unconditionally; OnHide (:351) fires only on a transition. | `performance-§12` | Arm only when f:IsShown(), reconfiguring after f:Show(); amend the ARCHITECTURE.md deviation row, whose "cannot outlive that window" claim is currently false. |

**† Regraded or corrected in triage.** `LOOTHISTORY-R-06` — Kept at medium: the ratified performance-§12 exemption rests on this row, and it is the one claim that bears on criterion (a)'s substance. `LOOTHISTORY-R-05` — Both medium originally; lowered because I checked all 13 events and all 5 timers and every one is occasional or one-shot, so the exemption's substance holds. `PRETTYCHAT-R-03` — Medium to low: the hit is a single render-time C_Timer.After(0) on no combat path, so the exemption still holds on merit — only its evidence is stale. `WHATGROUP-R-02` — medium → low: one handle, never stacked (ConfigureTeleportButton cancels first) and self-cancelling at zero, so the stray is one C call per second, bounded.

## C27 · Allocation and hot-path nits, plus perf ceilings that no longer bound anything — 8 findings, 6 repos **[COLLECTION]**

Closures and small tables allocated per event where a cached one would do, a driver that never stops, and two dormant-allocation ceilings re-baselined far above what the suite now measures.

*Repos* AbsorbTracker, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-01` | R | Low † | `modules/Display.lua:375 vs core/PerfSetup.lua:51,63` — Note("paintBar", ms) passes two args while appearance:236 and visibility:320 pass openBucket third. P.Note takes parentKey at Perf.lua:403. | `performance-§3` | Have doRepaint pass its open bucket into UpdateAbsorbBar and on to Perf.Note's third argument, as appearance and visibility already do. |
| AbsorbTracker | `ABSORBTRACKER-R-03` | R | Low † | `tests/perf.lua:235` — PROBE_OFF_BYTES_CEILING = 320, comment cites a 312.0 baseline; my run reports probeOverheadOff at 48.0 bytes/iter | `performance-§2` | Re-baseline the ceiling from 320 to about 72 after three runs; record the new figure and date in the comment. |
| AbsorbTracker | `ABSORBTRACKER-R-12` | R | Low | `settings/General.lua:218-229 and the composed state.debugConsole row` — Neither row declares onChange; Schema.lua:163 falls back to defaultOnChange, which publishes MSG.APPEARANCE. appearancePass today: 0.029 ms, 48 API calls, 384.5 bytes. | — | Give both rows an explicit no-op onChange with a one-line reason; leave defaultOnChange alone for the appearance rows that need it. |
| ConsumableMaster | `CONSUMABLEMASTER-R-09` | R | Low | `settings/Panel.lua:908-928` — Confirmed: token bump plus an unconditional C_Timer.After closure per call, roughly 150 during the one first-open item-info burst. | `performance` | Schedule only when nothing is pending and re-derive the capped delay inside the single live timer; add a perf scenario first. |
| KickCD | `KICKCD-R-10` | R | Low † | `modules/Castbar.lua:833` — Line 833 is `inst.frame:SetScript("OnUpdate", function() onUpdate(inst) end)`; tests/perf.lua has no castStart scenario, so the cost is unmeasured | `performance-§8` | Cache inst.__onUpdate in EnsureFrame. Take this only together with a castStart perf scenario, else skip it |
| LootHistory | `LOOTHISTORY-R-10` | R | Low † | `modules/AuctionPrice.lua:58,73` — wantedByProvider allocates 1-4 small tables per recorded loot line from a set that changes only on a settings edit | — | Memoise behind a SettingsChanged refresh via NS.NewBusTarget only if it is ever measured; otherwise leave it |
| MultiMeters | `MULTIMETERS-R-07` | R | Medium | `tests/perf.lua:564, rationale :539-563` — Confirmed PROBE_OFF_BYTES_CEILING = 336000 commented "measured 325955"; today's run reports 310158.1, so headroom is 7.7%, not the stated 3.5%. | `performance-§9` | After R-01, re-record the measured figure and re-derive the ceiling with the stated margin, recording why it moved. |
| PanelMaster | `PANELMASTER-R-06` | R | Low † | `modules/Canvas.lua:642-666` — Script never cleared; the comment at :654-656 claims it "stops doing any work the moment the tracked set is empty", which is false | `performance-§2` | Clear the script in SetMouseoverTracked when the tracked set empties; re-install in ensureMouseoverDriver. Keep the frame. |

**† Regraded or corrected in triage.** `ABSORBTRACKER-R-01` — medium to low: the record is developer-facing only, and the declared nesting happens to be the true one. `ABSORBTRACKER-R-03` — medium to low: a lax test guard, no player reach; it would still catch a catastrophic regression, just not the one-table-per-pass case it claims to. `KICKCD-R-10` — code fact confirmed, perf claim unverified; cast starts are event-rate, not frame-rate. `LOOTHISTORY-R-10` — Lowered from medium: the allocation is dwarfed by the pcall'd cross-addon fetches on the very same line, and the proposed cache costs more than it saves. `PANELMASTER-R-06` — medium to low: one accumulator per frame and a 10Hz walk of an empty table is not measurable; the false comment is the larger defect.

## C28 · Stored values reaching APIs unvalidated, and session state left behind — 8 findings, 5 repos **[COLLECTION]**

Numbers taken straight from SavedVariables into timer and colour APIs with no clamp, two decoders over one storage shape disagreeing on the missing-channel default, a defaults table mutated in place, and reset paths that clear the tables but not the flag beside them.

*Repos* AbsorbTracker, ConsumableMaster, KickCD, PanelMaster, PrettyChat · *disposition* `per-addon` · *effort* M · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-02` | R | Low † | `core/Units.lua:111-119, reached from settings/UnitPanel.lua:224-228` — CopyFromPlayer does dst[key] = deepcopy(src[key]) for 19 keys plus dst.mirror = false; no SetByPath, so no [Set] line. | `debug-logging-§10` | Route each key and the mirror flag through NS.SetByPath; drop the now-redundant manual APPEARANCE publish at settings/UnitPanel.lua:226. |
| AbsorbTracker | `ABSORBTRACKER-R-05` | R | Low † | `modules/Timer.lua:50` — GetMasterAlpha:248, GetMasterScale:257, GetBarAlpha:276 all tonumber and clamp; Timer passes raw GetSetting. AceTimer new() does delay < 0.01. | — | Add NS.GetThrottleWindow beside the three clamped getters in core/Data.lua and call it from modules/Timer.lua:50. |
| ConsumableMaster | `CONSUMABLEMASTER-R-05` | R | Low † | `settings/OptionsSetup.lua:101-104 vs settings/Slash.lua:295-298` — Confirmed verbatim: OptionsSetup returns c[1] or 1, Slash returns c[1] or 0; KCM.SwatchColor has its own per-surface fallback. | `options-ui` | One shared decoder returning nil for an absent channel, passed to both descriptors; per-surface defaults stay in KCM.SwatchColor. |
| KickCD | `KICKCD-R-08` | R | Low † | `settings/Panel_Render.lua:304` — Fallback y = -180 against defaults/Profile.lua:314's y = 120, under a header promising no duplicated magic numbers | `savedvariables` | Early-return when the defaults tree is absent; keep defaults/Profile.lua the one source for the coordinate |
| PanelMaster | `PANELMASTER-R-02` | R | Low † | `modules/Registry.lua:588` — dropSessionIDs clears the flag at :561; DeleteAll clears only the two tables at :588-589 — the failure its own comment at :543-545 names | — | Extract one private sweep clearing unlockedPanels, previewIDs and NS.State.preview; call it from both dropSessionIDs and R:DeleteAll. |
| PanelMaster | `PANELMASTER-R-03` | R | Low † | `core/Util.lua:99-106` — scale picked from nums[1..3] then applied to nums[4]; "255,0,0,1" yields alpha 0.0039 — an invisible panel, no error | — | Under scale 255, treat nums[4] <= 1 as already fractional, and update the comment's round-trip argument. Extend the round-trip cases. |
| PrettyChat | `PRETTYCHAT-R-07` | R | Low † | `modules/Override.lua:154; core/PrettyChat.lua:81-84` — Snapshot is _G[globalName], nil when the client omits the global; the elseif then skips restore, so the override survives every disable. | `savedvariables` | Track presence with a separate key set, not the snapshot's truthiness, and restore to nil. The review's ~= nil test does not work. |
| PrettyChat | `PRETTYCHAT-R-12` | R | Low † | `core/PrettyChat.lua:20-25` — local defaults = NS.ProfileDefaults then defaults[k] = defaults[k] or v. Confirmed; grep finds no other consumer of NS.ProfileDefaults. | `savedvariables-§2` | Build a fresh merged table so NS.ProfileDefaults keeps meaning exactly what defaults/Profile.lua declares. |

**† Regraded or corrected in triage.** `ABSORBTRACKER-R-02` — medium to low: the caller publishes APPEARANCE and re-renders, so the only loss is the debug log line, not user-visible state. `ABSORBTRACKER-R-05` — medium to low: LibKa0s/Slash.lua:338 coerces type="number" rows, so the only route to a string is a hand-edited SavedVariables. `CONSUMABLEMASTER-R-05` — was medium; colorEncode always writes four channels, so the divergent branch needs a hand-edited SavedVariables to reach. `KICKCD-R-08` — reachable only if defaults/Profile.lua failed to load, which the TOC guarantees it did. `PANELMASTER-R-02` — medium to low: Unlock:SetPreview(false) still succeeds, so the stuck toggle is recoverable by one untick, not a dead end. `PANELMASTER-R-03` — medium to low, and not taint: the behavior is a documented deliberate tradeoff at :83-87, reachable only by hand-typed mixed-scale CLI input. `PRETTYCHAT-R-07` — Medium to low: a client that does not define a global never reads it, so the leaked value is invisible. The review's proposed fix is itself broken. `PRETTYCHAT-R-12` — Kept low. The sole consumer is the mutating line itself, so nothing observes the graft today; it is a trap for the second consumer.

## C29 · Event and lifecycle gaps: state read at the wrong moment — 7 findings, 4 repos **[COLLECTION]**

Gates evaluated once and never re-evaluated across a combat transition, a positional FIFO pairing captures to application IDs, a wholesale reset that never broadcasts, and a flag snapshotted at schedule time rather than read at fire.

Three of these need a client to prove and cannot be closed headless: `WhatGroup/modules/Frame.lua:148-151` never re-evaluates across a combat transition, `core/WhatGroup.lua:678`'s positional FIFO pairing only mismatches when several applications are outstanding, and `:605`'s snapshot only bites if the setting is changed inside the scheduled window.

*Repos* BankLedger, KickCD, LootHistory, WhatGroup · *disposition* `per-addon` · *effort* M · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| BankLedger | `BANKLEDGER-R-01` | R | Medium † | `settings/Slash.lua:92-103` — ResetEverything wipes and refills db.global, calls ResetWindow/Refresh, never SendMessage; Ledger re-caches only on that message (Ledger.lua:872-878). | `architecture-§4` | Send Ka0s_BankLedger_SettingsChanged once at the end of ResetEverything; do not enumerate consumers. |
| BankLedger | `BANKLEDGER-R-04` | R | Low † | `core/BankLedger.lua:44-59 (no OnDisable) + modules/Ledger.lua:845-847` — Confirmed absent, and Enable early-returns on _enabled. But nothing in the repo calls Disable; the `settings.enabled` row is a capture gate, not AceAddon disable. | — | Add addon:OnDisable clearing _enabled on Ledger, Browser, SessionWindow and Insights; verify _guildHooked separately. |
| KickCD | `KICKCD-R-07` | R | Low † | `modules/Castbar_Debug.lua:42` — reportSecretNint's whole body sits inside `if _G.C_CurveUtil and ...` with no else; :87 makes it NINT_REPORT's default arm | — | Print the secret-tainted line unconditionally, with C_CurveUtil availability as a separate clause; delete the abandoned-design comment |
| LootHistory | `LOOTHISTORY-R-03` | R | Medium † | `settings/Panel.lua:155-162` — Browser.lua:1273 and Analytics.lua:655 wrap RecordAdded in NS.Coalesce; Panel registers a raw handler that runs StorageStats over the whole history | — | Wrap onChange in NS.Coalesce(onChange, NS.Constants.RECORD_ADDED_COALESCE) for RecordAdded only, leaving HistoryChanged immediate |
| WhatGroup | `WHATGROUP-R-01` | R | Medium † | `modules/Frame.lua:148-151` — ApplyFrameVisibility only calls f:Hide(); sole caller settings/Panel.lua:246 onChange; no PLAYER_REGEN_* drives it anywhere in the repo. | `options-ui-§15` | Register PLAYER_REGEN_DISABLED/ENABLED and route both to ApplyFrameVisibility, made symmetric: hide when the gate closes, show when it opens with pendingInfo. |
| WhatGroup | `WHATGROUP-R-07` | R | Medium † | `core/WhatGroup.lua:678` — table.remove(captureQueue, 1) binds the FIFO head to whatever appID "applied" carries; nothing correlates them. Declined applications never clear. | — | Key captures by searchResultID, resolving it from appID through the existing GetApplicationInfo bridge; clear pendingApplications on declined and cancelled. |
| WhatGroup | `WHATGROUP-R-14` | R | Low | `core/WhatGroup.lua:605` — autoShow read at :605-606 and used in the callback at :627, which already re-reads pendingInfo for exactly this reason. | — | Move the frame.autoShow read inside the scheduled callback; delay correctly stays at schedule time as the timer's own argument. |

**† Regraded or corrected in triage.** `BANKLEDGER-R-01` — high to medium: real silent-wrong-capture window, but only after a confirm-gated destructive act, and it clears on reload. `BANKLEDGER-R-04` — medium to low: no in-addon or in-game route reaches OnDisable, so the latch cannot bite a player. `KICKCD-R-07` — medium; needs a 12.0 secret value AND a missing C_CurveUtil, and costs one line of a debug-only dump. `LOOTHISTORY-R-03` — Held at medium, not raised to issue #27's high: it only fires while the General page is actually shown. `WHATGROUP-R-01` — high → medium: the gate IS evaluated at every ShowFrame (:665), so the option is not inert; only the mid-window transition is missed. `WHATGROUP-R-07` — held at medium: reachable whenever several applications are outstanding, but :704 prefers the fresh re-fetch when it carries mapID.

## C30 · Settings-panel shape deviations against options-ui — 8 findings, 6 repos **[COLLECTION]**

Page acts under a tab rather than the chrome band, hand-written control groups where a composer exists, a degraded help list offering a verb that then declines, a library constant hardcoded as a literal, and a category registered with no combat guard.

`ConsumableMaster/settings/Panel.lua:866-867` calls `Settings.RegisterAddOnCategory` from a `PLAYER_LOGIN`/`ADDON_LOADED` bootstrap at `:984-993` with no `InCombatLockdown` gate, which is reachable through an in-combat reload and is a taint question rather than a shape one. Batch it with the other in-client checks.

*Repos* BankLedger, ConsumableMaster, LootHistory, MultiMeters, PanelMaster, WhatGroup · *disposition* `mixed` · *effort* L · *cluster severity* Medium

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| BankLedger | `BANKLEDGER-R-07` | R | Low | `settings/Schema.lua:438-442` — With NS.LedgerTable absent, `on` is nil and the verb prints "test mode off"; the session verb two rows up handles nil properly. | `slash-commands-§3` | Distinguish unavailable from off, in the shape the session verb already uses. |
| ConsumableMaster | `CONSUMABLEMASTER-R-11` | R | Low | `settings/Panel.lua:866-867` — Confirmed: bootstrap at :984-993 fires registerPanel from PLAYER_LOGIN / ADDON_LOADED with no InCombatLockdown gate; reachable via an in-combat reload. | `events-frames-taint` | If this file is touched, defer on InCombatLockdown and retry from the existing PLAYER_REGEN_ENABLED handler rather than registering twice. |
| LootHistory | `LOOTHISTORY-R-16` | R | Low | `settings/Slash.lua:178-181, 200` — LIBRARY_OWNED omits config, so Schema.lua:434's entry survives the subtraction; P:Open reaches O.OpenOptionsPanel, a noop stub on that path | `slash-commands-§1` | Add config to the subtracted set and rename LIBRARY_OWNED to name what it means on the degraded path |
| MultiMeters | `MULTIMETERS-A-12` | A | Low | `settings/Schema.lua:1553-1566` — Confirmed: window.barTexture and window.font are single All-surfaces rows with LSM30_ dialogControls and broadcastBarTexture/broadcastFont onChange. | `options-ui-§16` | Upstream: narrow the clause to hits reproducing a mandated block, or have LibKa0s-OptionsCompose expose a broadcast-meta composer. No local change. |
| PanelMaster | `PANELMASTER-A-01` | A | Medium | `settings/PanelEditor.lua:565-677 (Copy :607, Enabled :633, Unlock :648, Reset :667, Delete :673)` — All five acts are inside sections[TAB_GENERAL]; H.PageHeader band exists and is drawn at :1112-1199. docs/settings-panel.md:257 argues the placement. | `options-ui-§14` | Move the five acts into the H.PageHeader band, drop the emptied General tab, re-point the :1058 fallback, and rewrite the doc paragraph in the same commit. |
| PanelMaster | `PANELMASTER-A-03` | A | Low † | `settings/PanelEditor.lua:738-757, :770-800, :814-830` — O.BorderGroup/O.BarGroup at OptionsCompose.lua:262/:297 emit path-keyed schema rows; this page edits registry records, so no composer arm fits | `options-ui-§16` | Add a record-backed bind arm to the LibKa0s composers, re-vendor, replace the three blocks; meanwhile file an options-ui-§16 register row. |
| WhatGroup | `WHATGROUP-R-03` | R | Low † | `settings/Schema.lua:577` — StaticPopupDialogs = StaticPopupDialogs or {} sits directly under a comment explaining that registration is deferred precisely to avoid touching the table. | `events-frames-taint` | Delete the assignment and keep the indexed write below it; the table always exists in retail, so the guard is dead code. |
| WhatGroup | `WHATGROUP-R-04` | R | Low † | `settings/Panel.lua:285` — ["Master controls"] = MASTER_TAIL copies libs/LibKa0s/OptionsCompose.lua:50, which exports the same string as O.MASTER_GROUP at :189. | `options-ui-§8` | Key off [Helpers.MASTER_GROUP or "Master controls"] so a library rename cannot silently drop the reset button pair. |

**† Regraded or corrected in triage.** `PANELMASTER-A-03` — kept low: the blocks already follow the mandated row order, so the deviation is structural only. `WHATGROUP-R-03` — medium → low: the next line's indexed write already taints the table, and this runs only on a reset the player invoked. `WHATGROUP-R-04` — medium → low: correct today; the failure needs an upstream rename that has not happened.

## C31 · Naming, lint config and vendored-payload hygiene — 8 findings, 5 repos **[COLLECTION]**

Bare WoW globals beside _G.-prefixed reads in the same file, a parameter named print, a version constant duplicating the TOC with nothing pinning them, a .luacheckrc that disagrees with .pkgmeta about _dev, and a vendored LibStub shipping files the TOC never loads.

*Repos* AbsorbTracker, ConsumableMaster, KickCD, LootHistory, WhatGroup · *disposition* `per-addon` · *effort* S · *cluster severity* Low

| Repo | ID | Src | Sev | Locus · evidence | Rule | Remedy |
|---|---|---|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-A-08` | A | Low | `libs/LibStub/tests/, libs/LibStub/LibStub.toc` — find libs/LibStub lists 6 files; AbsorbTracker.toc:17 loads only libs\LibStub\LibStub.lua | `library-stack` | Delete libs/LibStub/tests/ and LibStub.toc so the vendored copy is exactly what the TOC loads. |
| ConsumableMaster | `CONSUMABLEMASTER-R-07` | R | Low † | `settings/Category.lua:764; modules/Selector.lua:610,655` — docs/debug.md:30 forbids %d/%f on the secret-safe sink; the three arguments are #priority, curIdx/newIdx and from/to. | `debug-logging` | Change the three placeholders to %s; the rendered line is identical because SafeToString already ran on every vararg. |
| KickCD | `KICKCD-R-11` | R | Low † | `modules/IconGrid.lua:232; modules/Cooldowns.lua:80; settings/Panel_Widgets.lua:121; +3` — IconGrid.lua:232 UnitClass("player") against :148's _G.UnitExists, both in the same file | `architecture-§1` | Prefix the stragglers with _G.; mechanical, no behaviour change, lint and suite unaffected |
| KickCD | `KICKCD-R-12` | R | Low | `modules/Castbar_Debug.lua:33,37,42,54,69,80,97,111` — Eight function signatures take `print` as a parameter; routing is correct, resolved at :125 to NS.Util.print | `slash-commands-§4` | Rename the parameter to emit, matching settings/Slash.lua:61's out(line) convention |
| LootHistory | `LOOTHISTORY-R-18` | R | Low | `core/Namespace.lua:5 vs LootHistory.toc:5` — Both read 1.2.0 today; test_envsetup.lua:63 asserts equality only on the branch where the TOC is unreadable | `slash-commands-§3` | Add a case parsing ## Version: out of LootHistory.toc and asserting it equals NS.version |
| WhatGroup | `WHATGROUP-A-14` | A | Low | `.luacheckrc:9` — exclude_files lists libs/, docs/audits/, docs/reviews/, tests/ — no _dev/, while .pkgmeta:12 already reserves _dev whether or not it exists. | `lint` | Add "_dev/" to exclude_files so the two config files agree about the scratch directory. |
| WhatGroup | `WHATGROUP-R-06` | R | Low † | `core/Compat.lua:62-67` — Siblings at :24, :40, :52, :83, :105 all try C_Spell.* first; this one calls the bare global and returns false when absent. | `compat` | Add a C_SpellBook.IsSpellKnown rung above the global, but only once an in-client check confirms both APIs present and agreeing. |
| WhatGroup | `WHATGROUP-R-12` | R | Low † | `settings/Panel.lua:207` — addonName = "WhatGroup" while the file's own vararg holds it at :14; OptionsSetup.lua:13 and Schema.lua:20 take the same vararg. | — | Pass the addonName upvalue the file already binds at :14. |

**† Regraded or corrected in triage.** `CONSUMABLEMASTER-R-07` — was medium; all three arguments are loop indices and counts, never combat-restricted values, and only fire with debug on. `KICKCD-R-11` — scope narrowed from likely-cross-cutting: I verified only KickCD. `WHATGROUP-R-06` — medium → low: the global still exists on live, so the degrade path is unreachable until Blizzard removes it. `WHATGROUP-R-12` — scope narrowed: likely-cross-cutting → addon-local; this is the repo's only hardcoded site.

---

# Part 3 — What triage rejected, and why

This section is the proof the ledger above is filtered rather than collected. Twenty-four bundle items
were dropped or merged, six cluster-level claims were corrected against the code, and eleven counts in
surviving findings were wrong in the bundle that filed them.

## Rejected — the claim did not survive re-checking

| Repo | Bundle id | Title | Why it is not carried forward |
|---|---|---|---|
| AbsorbTracker | `ABSORBTRACKER-R-13` | One committed doc has mixed line endings in the working tree | Not rejected but merged into A-07; its distinguishing claim "only such file" is false — git ls-files --eol prints two, including tests/test_units.lua. |
| BankLedger | `BANKLEDGER-A-03` | .superpowers directory absent from .pkgmeta ignore list | Evidence fails: .superpowers is gitignored and wholly untracked, so no packager export can carry it. The .pkgmeta half is zero-impact. |
| BankLedger | `BANKLEDGER-R-11` | Two files near layout-§1 boundaries the stale watch list does not show | Numbers verified (1478, 992) but this is not a defect — its own fix is 'no action now'. Folded into the stale-record finding. |
| ConsumableMaster | `CONSUMABLEMASTER-R-12` | Six functions sit at exactly CCN 15, the release gate's cap | Reproduced exactly, but the gate is above 15 and nothing sits above it. No rule broken, no impact, no action — a note, not a finding. |
| ConsumableMaster | `CONSUMABLEMASTER-R-10` | KCM.MakeCloseButton has zero call sites | Confirmed and deliberate — the review's own remedy is to keep it. Folded into CM-R-03, whose fix records the deadness as data. |
| MultiMeters | `MULTIMETERS-A-04` | .pkgmeta ships .claude and .superpowers to players | Neither directory has a tracked file; .gitignore ignores .superpowers/ and .claude is empty. A packager clone receives nothing, so no player bytes. |
| MultiMeters | `MULTIMETERS-A-03` | Five Tier 2 doc triggers fire; four rows assert false Not applicable | The four rows carry measured arguments matching the source, and compat-layer.md already self-flags "the trigger now fires". This re-litigates a recorded evaluation. |
| PanelMaster | `PANELMASTER-A-04b` | .pkgmeta leaves .claude and .superpowers unignored | Neither directory exists in this repo's root; the sweep output the audit quoted cannot have named them. The .gitattributes half stands. |
| PanelMaster | `PANELMASTER-A-00` | Audit suite claim: both LibKa0s vendor diffs empty | diff -r against the sibling working tree is not empty for DebugLog.lua and Pool.lua. Content matches; line endings do not, as the review found. |
| PrettyChat | `PRETTYCHAT-A-03` | Message-bus applicability trigger fired; no bus, no register row | ARCHITECTURE.md:125 says no NAMED MESSAGE exists, which is true. The combat watcher is already registered in the performance-§12 deviation row at :222. |
| PrettyChat | `PRETTYCHAT-A-02` | Register row cites a standard-internal conflict the standard has resolved | Evidence cites layout.md:53 in the standards repo, outside this repo and unreadable here. The row already names WowAddonStandards#2 as its re-check trigger. |
| PrettyChat | `PRETTYCHAT-R-08` | Production format-signature logic lives only in the test suite | Confirmed but not independent: it is the prerequisite half of PRETTYCHAT-R-01's fix. Merged there rather than tracked twice. |
| PrettyChat | `PRETTYCHAT-R-06` | Slash error and usage lines concatenate translated fragments | Premise fails on re-reading: note() and cmd() are colour wrappers, not L[]. The fragments are unwrapped, not translated. Merged into R-04. |
| PrettyChat | `PRETTYCHAT-A-06` | Automated-test record's standing sections two runs stale | Same defect as PRETTYCHAT-R-05, found from the audit side. Merged there. |
| WhatGroup | `WHATGROUP-A-12` | Message Bus rationale answers only half the applicability condition | The recorded rationale is accurate: grep for SendMessage/RegisterMessage over source returns nothing. The two PLAYER_REGEN_ENABLED registrations are transient combat-defer hops, not a bus question. |
| WhatGroup | `WHATGROUP-A-13` | .pkgmeta accounts for neither .superpowers nor .pkgmeta | No .superpowers path exists at the repo root or in git; only docs/superpowers/, already covered by the docs ignore. The .pkgmeta self-reference remainder is Info, not a deviation. |
| LibKa0s | `LIBKA0S-A-12` | Ratified perf-skip decision has no register row | Not a deviation. RESULTS.md:97 frames the skip as automated-tests-§3's sanctioned "nothing to run", explicitly not a ratified performance-§12 exemption. |
| LibKa0s | `LIBKA0S-R-14` | Standard describes thirteen LibKa0s files; library ships fourteen | Substance survives but evidence fails: OptionsScroll.lua is present at library-stack.md:82. Merged into A-14 with corrected evidence. |
| LibKa0s | `LIBKA0S-R-03` | Complexity ceiling moved into shipped library; watch list unaware | Confirmed but not independent — it is one stale section of the same RESULTS.md defect. Merged into R-02. |
| LibKa0s | `LIBKA0S-A-13` | library-stack-§7's applicability lists are not exhaustive | Confirmed and identical to R-15 from the other direction. Merged into R-15. |
| LibKa0s | `LIBKA0S-A-09` | Seven tracked files disagree with the declared CRLF pin | Confirmed but is the effect of the blind gate. Merged with R-04 and A-09d into one finding. |
| LibKa0s | `LIBKA0S-A-09d` | Repo's own eol gate is scoped to one directory | Confirmed and identical to R-04. Merged into R-04. |
| LibKa0s | `LIBKA0S-A-02` | RESULTS.md standing sections and watch list are eight runs stale | Confirmed and identical to R-02 from the other direction. Merged into R-02. |
| LibKa0s | `LIBKA0S-A-11` | Standard-version pointer ten minor versions stale in both places | Confirmed and identical to R-10. Merged into R-10. |

Three of these are worth naming individually, because they are the shape of error a second pass exists
to catch. `BANKLEDGER-A-03`, `MULTIMETERS-A-04` and `WHATGROUP-A-13` all file `.superpowers` as
shipping to players. In all three repos the directory is either gitignored, empty, or absent from the
root entirely, so a packager clone receives nothing.

**And the fourth filing fails the same test.** `ABSORBTRACKER-A-01` was carried forward as the one true
positive on the strength of `du -sh .superpowers` reporting 2.8M — but that directory is gitignored
(`AbsorbTracker/.gitignore:15`, with `.claude` at `:11`) and `git ls-files .superpowers` returns nothing,
so AbsorbTracker stands exactly where the three rejected findings stand. The rule was right **zero** times
in four on the claim it made, which is worse than the "one in four" this paragraph originally recorded and
is the real lesson: `du` reads a working directory and a packager reads a git clone, and no audit in this
cycle asked git.

`ABSORBTRACKER-A-01` is nevertheless retained, and retained at medium, on evidence the audits did not
gather: `media/screenshots` is **tracked** in AbsorbTracker, KickCD, LootHistory and WhatGroup and absent
from all four ignore lists, so those four ship 16.3M of project-page art to every player. Only
`WHATGROUP-R-09` named it, and only for its own 880K. A finding kept on corrected evidence is not the
same as a finding kept, and this is the one place in this ledger where that distinction had to be made
after the fact.

## Cluster claims corrected against the code

The clusters are triage output, and six of them state something the repositories do not.

| Cluster | Claim as filed | What the code says |
|---|---|---|
| `C22` | "Eleven tracked files sit over the cap", across ConsumableMaster, KickCD, MultiMeters, PanelMaster and LibKa0s. | **Eighteen** files exceed 1500 LOC over `git ls-files '*.lua'` excluding `libs/` and `tests/_kit/`. **KickCD and PanelMaster have none** — their largest are `modules/Castbar.lua` at 1320 and `tests/test_artwork.lua` at 1356. Seven MultiMeters *test* files over cap are unreported anywhere, and PrettyChat — absent from the cluster — holds the collection's largest file at 23,842 lines. |
| `CX06` | "BankLedger and LootHistory declined it." | LootHistory **adopted** it. `core/CoreSetup.lua:19-26` records the decline as expired at LibKa0s v1.10 and `:167` is the wrapper. BankLedger is the only live decline, and it is reasoned at `core/CoreSetup.lua:117-129`. |
| `CX08` | "75 hard-coded `Interface\` paths remain across the nine addons." | **The ledger was right and the triage correction was the error.** Over tracked `*.lua` excluding `libs/`, `tests/` and `PrettyChat/GlobalStrings/` — generated, unloaded, `.pkgmeta`-ignored, and exempted by rule under `M1-STD-08` — the count is **75 lines carrying 76 paths**: BankLedger 17, LootHistory 19, ConsumableMaster 11, MultiMeters 8, KickCD 7, PanelMaster 7, AbsorbTracker 3, WhatGroup 2, PrettyChat 1. The "PrettyChat 93" reading counted the 92 hits inside `GlobalStrings/`; the "246 Buttons / 138 Tooltips" pair was measured over a scope including `libs/` and is nine vendored copies of one payload — over the scope above it is 4 and 3. 21 of the 76 are `Interface\Buttons\WHITE8x8`, which `standalone-windows.md:20` mandates, and 12 are the addon's own `Interface\AddOns\…` art. |
| `C02` | "All five copies differ." | True by md5, but the differences are not equal. KickCD and PanelMaster are functionally identical, ConsumableMaster differs in a bootstrap header line and MultiMeters in a `local _ = ...`; AbsorbTracker is the one real divergence, exposing a callable `NS.ApplyLSMBorderPatch()` at `core/LSMPatch.lua:20` invoked from `core/AbsorbTracker.lua:52` rather than a `PLAYER_LOGIN` frame. Sequencing the deletion of the five copies depends on that distinction. |
| `C08` | "46 of 89 frozen bundles carry no `ANALYSIS.md`." | 93 bundles, 35 without. And `automated-tests.md:245` makes the write-up a MUST only for **release** runs, so most of the 35 are the SHOULD, not a deviation. |
| `C10` | "76 tracked stragglers across ten repos." | The per-repo enumerations do not add to a scope. `MULTIMETERS-A-05` gives its locus as "repo working tree" against an actual 21 files; `CONSUMABLEMASTER-R-08` counts 7; `PRETTYCHAT-A-07` names two frozen docs and misses the two stragglers that sit inside a **shipped** payload — `libs/LibKa0s/DebugLog.lua` and `libs/LibKa0s/Pool.lua`, both `w/lf` under a `crlf` pin, and the vendored image of LibKa0s's own two. Re-enumerated today: MultiMeters 21, LootHistory 9, KickCD 8, ConsumableMaster 7, LibKa0s 7, PanelMaster 6, WhatGroup 6, BankLedger 4, PrettyChat 4, AbsorbTracker 2. |

## Fix directions rejected — do not execute as written

**`CX06` — rebinding `MakeCloseButton`.** Both the cluster and the library lens propose binding
`addonName` inside `LibKa0s-Core-1.0`. The payoff is roughly 24 lines against a signature change to a
surface all nine consumers vendor, and it is contradicted by the library's own recorded reasoning at
`LibKa0s/Media.lua:14-20`: `...` carries the addon name only for a file the TOC loads directly, so the
library cannot infer it. If the eight wrappers are to go, the shape is a one-time `lib.SetHost(name)`,
not inference — and the cheaper close is to ratify BankLedger's decline with a register row and raise
the MUST/MAY tension at `standalone-windows.md:30` against `:34` upstream.

**`C17` — renaming the `minimise` icon key.** `lib.ICONS` (`LibKa0s/Media.lua:94`) publishes
`"minimise"`, and `lib.Icon` (`Media.lua:202`) builds the path *from* the key: `base .. ICON_DIR ..
"\\" .. name`. The file on disk is `minimise.tga`, vendored into all nine `libs/LibKa0s/media/icons/`
trees. Adding `"minimize"` to the catalog alone therefore yields a path to a file that does not exist —
the exact silent failure `Media.lua:190-196` records, where a missing texture draws nothing and raises
nothing. The fix needs a second `.tga` or an alias map, and the key itself should stay. Correct the
authored prose and the player-facing chat strings — `CANCELLED` at `Perf.lua:948` and `:1063`, `unlabelled` at `:723`,
`:864` and `:1029`, the second of which `localization.md:139` carries as `labelled` → `labeled` — and
leave the public key alone. The five are not one word: a single perf capture reaches two of them, so the
in-client check has to start a labelled capture and an unlabelled one.

**`C08` — backfilling missing `ANALYSIS.md` files.** These are frozen, dated records. Writing an
analysis today into a bundle stamped in August is fabricating a record. Fix forward: make the next run
write one, and note the gap once.

**`BANKLEDGER-R-03` — wrapping the kit's AceDB fake.** The review directs you to wrap
`tests/_kit/`'s fake. The kit fake copies defaults in exactly as the local override at
`tests/wow_mock.lua:582-589` does, so wrapping it restores nothing; the case still cannot fail. The
defaults fallback has to be *modelled* — metatable or logout strip — before the case means anything.

**`PRETTYCHAT-R-07` — testing the snapshot with `~= nil`.** The snapshot is `_G[globalName]`, which is
nil precisely when the client omits the global. A `~= nil` test cannot distinguish "absent" from
"present and nil", which is the case the finding is about. Presence needs its own key set.

## Claims corrected but the finding retained

| Finding | Correction |
|---|---|
| `ABSORBTRACKER-A-07` | Review said one file; `git ls-files --eol` prints two, and the second (`tests/test_units.lua`) is source, not a frozen doc. |
| `CONSUMABLEMASTER-A-02` | Audit reports 28 British-spelling sites; the sweep excluding `libs/` finds 25. |
| `CONSUMABLEMASTER-A-08` | Audit reports 13 unparseable citations; there are 9 code sites. |
| `KICKCD-A-03` | Audit reports 51 hits in 12 files; excluding `libs/`, `tests/_kit/` and the frozen bundles it is 37 in 11. The audit's count folded in frozen audit and review bundles. |
| `KICKCD-R-06` | Review counts 9 line-ending stragglers; excluding `-text` binaries it is 8, which is the audit's number. |
| `LIBKA0S-A-04` | Audit says "17 of 28" bundles lack a write-up; 31 dated bundles exist, 14 with `ANALYSIS.md`. |
| `LIBKA0S-R-09` | Review says lint covers "18 of 40" files; the tracked total is 49, 31 of them under `tests/`. |
| `LOOTHISTORY-A-08` | Audit says the band disposition has read "peel next" for five runs; `RESULTS.md`'s own text says four. |
| `LOOTHISTORY-R-14` | Cited line was `:193`; the comment is at `core/Database.lua:195`. |
| `PANELMASTER-A-07` | Cited locus corrected: `tests/wow_mock.lua`'s `reader("__h")` is the effective definition, and `SetAtlas` never writes `__h`. |
| `PRETTYCHAT-A-07` | Audit counts 4 files off the CRLF pin; 2. The extra hits were vendored `libs/` files and binary `.tga`/`.ttf` assets. |
| `PRETTYCHAT-A-01` | `PrettyChat.toc:43` dropped from the finding: `core/CoreSetup.lua:38` does `NS.Util = NS.Util or {}`, so it self-initialises and its position is not load-bearing. |
| `LIBKA0S-A-14` | The competing `LIBKA0S-R-14` was wrong about which file is missing. `OptionsScroll.lua` **is** in `library-stack.md:82`; the absent one is `OptionsCompose.lua`. |

## Verified-clean negatives

Recorded so no one re-spends the effort. These were checked and are genuinely clean, not merely
unexamined.

- **Cross-addon collisions in a same-session load.** Neither playbook contains a cross-addon check,
  and the collection's stated deployment is all nine loaded together. Four collision classes were run:
  slash tokens are all distinct (`at`/`bl`/`cm`/`kcd`/`lh`/`mm`/`pm`/`pc`/`wg`, all through AceConsole,
  no raw `SLASH_*`); the vendored LibKa0s minors are identical across all nine consumers for all ten
  majors (Core 7, DebugLog 12, Env 1, Item 1, Media 3, Options 14, Perf 7, Pool 3, Slash 7, Widgets 9),
  so LibStub's same-minor-different-bytes hazard is latent rather than live; 137 of 139 vendored
  LibKa0s files are byte-identical across the nine, the two exceptions being the CRLF-only pair in
  `C10`; and `## Interface: 120007` is uniform. The one live cross-addon mutation is `C02`.
- **PanelMaster artwork**, 1,660 lines no finding touches: the catalog holds 101 rows against 101
  `.tga` on disk with zero either way, every declared `w`/`h` matches the TGA header bytes, and all are
  power-of-two.
- **Tests that assert nothing.** Over 6,000 `test(...)` bodies scanned; every hit was a local helper
  (e.g. `approx` at `AbsorbTracker/tests/test_data.lua:17-20`, which wraps `assertTrue`) or a genuine
  `T.fail` scanner. `C21` already holds the real cases.
- **TOC ↔ disk**: zero missing files and zero unloaded own-source files in all nine.
- **Pattern injection from user text**: both search boxes use plain-find
  (`LootHistory/core/Database.lua:362`, `BankLedger/core/Database.lua:131`).
- **ConsumableMaster's macro and secure subsystem**, 43 of 59 files named by no finding: `FO.Apply`
  early-returns on `inCombat()` before every protected call, and `KCM:OnRegenEnabled`
  (`core/ConsumableMaster.lua:506-518`) flushes both queues.
- **luacheck**: 0 warnings / 0 errors in all ten repos, re-run on 2026-09-07.

## Process flags — do not lift these into a commit message

- **Two new defects surfaced during the cross-cutting passes that no bundle carries.** Both are
  PrettyChat, both low, both real. `PRETTYCHAT-X-01`: `GlobalStrings/split_globalstrings.py:40`'s
  `RE_SIMPLE` requires an all-uppercase key, so the 26 emitted chunks hold 22,879 of the source's
  23,760 entries — 881 dropped, 878 of them `VOICEMACRO_*`, and four documents
  (`GlobalStrings/README.md:3`, `docs/global-strings.md:3`, `docs/module-map.md:204` and the script's
  own TOC assert at `:83`) describe the split as complete. Impact today is nil, because no override
  targets a mixed-case global; a future one would fail `tests/test_defaults.lua:236` with a message
  blaming the default. `PRETTYCHAT-X-02`: `PRETTYCHAT-A-07` names the two frozen docs and misses
  `libs/LibKa0s/DebugLog.lua` and `libs/LibKa0s/Pool.lua`, which is why PrettyChat is the one consumer
  whose vendored copies of those two files are not byte-identical to the other eight.
- **In-client locale coverage is missing from six of nine smoke-test documents**, including the two
  addons whose code is most locale-sensitive. Only ConsumableMaster (`docs/smoke-tests.md:102`), KickCD
  (`:229`) and MultiMeters (`:1446`) carry a non-English-client step. LootHistory has none, yet
  `core/Compat.lua:188-195` defines four English wordings as the fallback when the client leaves
  `ITEM_ACCOUNTBOUND*` nil, reached at `:230-231`, and the same file calls the tooltip "the ONLY
  witness" for items whose bind type lies. PrettyChat has none in 797 lines, and its whole function is
  overwriting localised `_G` chat format strings. Every headless case for these paths asserts against
  enUS mock globals — `LootHistory/tests/test_compat.lua:65-66` passes the literals `"Auction House"`
  and `"Auction won: …"`.
