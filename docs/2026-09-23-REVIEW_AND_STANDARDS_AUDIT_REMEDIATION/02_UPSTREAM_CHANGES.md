# 02 — Upstream Changes (Milestone 1)

**Every change to WowAddonStandards, LibKa0s and the `wow-addon` plugin, in execution order.**

> **Nothing in this bundle has been executed.** No section has been amended, no minor bumped, no tag
> cut and no payload copied. Every item below is a proposal. The version numbers, tag names and orders
> say what *should* happen. Where this document states a present-tense fact about a repository, it was
> measured on 2026-09-23 against the working trees under `/mnt/d/Profile/Users/Tushar/Documents/GIT/`.

Item ids are the ones in `plan-data/items.json`: `WS-nn` for WowAddonStandards, `LK-nn` for LibKa0s and
`WA-nn` for the plugin. Milestone 2 holds the re-vendors `RV-<AB>` and the eight fixes that must land
before them (AT-01, AM-01, AM-02, BL-01, BL-02, CM-01, KC-01, WG-01). The rest of the addon items
(`<AB>-nn`) are Milestone 3, except the eleven owner-gated `/wow-addon:revendor-standards` items, which
are Milestone 4 (see *Release mechanics*). The plan-review decisions behind that shape are in
`plan-data/PLAN_REVIEW_RESOLUTIONS.md`, and each amendment is listed in `items.json`'s `amendment_log`.

---

## What shapes the milestone

**The collection starts flat.** The LibKa0s review's suite run (`inputs/findings/LibKa0s.json`,
measured at `46ccaa6`) found all eleven consumers byte-identical to LibKa0s v1.55.0 for both
`libs/LibKa0s/` and `tests/_kit/`, at kit revision 25, with `## Interface: 120100` everywhere. One
release can therefore reach every consumer in one re-vendor wave. The plan uses **one release per
upstream repository**:

| Repo | From | To | Kind |
|---|---|---|---|
| LibKa0s | v1.55.0 (kit 25) | **v1.56.0** (kit 26) | Minor. Every change is additive, no `NEEDS_*` floor rises, no major changes. |
| WowAddonStandards | v2.64.0 (2026-09-23) | **v2.65.0** | One version, one changelog entry. WS-01 opens it and WS-08 closes it. |
| wow-addon | 2.3.0 | **2.4.0** | Additive: `bin/`, two command/agent spec fixes. |

**The cost of the milestone lands downstream, and it comes from the test kit, not the library.** Kit
revision 26 makes the fakes behave more like the client: `CreateFrame` starts frames shown, the AceDB
fake raises and strips defaults, `EventRegistry` callbacks are recorded, frame `RegisterEvent` honors
`__badEvents`, `test_eol` counts lone CRs, the prose gate scans store-root files, and kit case names
carry `§`. Each of those can redden a consumer suite that passed on kit 25. The owner's standing ruling
is that such reds expose real bugs, so they are fixed in the addon before its re-vendor commit, never by
weakening an assertion. LK-05 and LK-33 run the payload against a `git archive` copy of every addon to
find them in advance. **No dry-run has been run yet**: no `dryrun-*` output exists in the scratchpad.

**Branches.** All three upstream repos already have `feat/2026-09-23-review-audit-remediation` checked
out. LibKa0s is one commit ahead of `origin/master` (`ab6404d`, the review record). WowAddonStandards and
wow-addon are level with `origin/master`. The "create branch first" preconditions in WS-01 and WA-01 are
therefore already met. All three default branches are **`master`**, not `main`.

### The three upstream repositories

| Repo | Path | Role | Consumers |
|---|---|---|---|
| WowAddonStandards | `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards` | The standard (`standards/`), the playbooks (`AUDIT.md`, `NEW_ADDON.md`, `AUTOMATED_TESTS.md`) and the roster (`standards/ADDONS.md`). | All eleven addons, LibKa0s, and the plugin's agents, which fetch it from **GitHub**, not from the sibling. |
| LibKa0s | `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s` | Fifteen LibStub majors (`tests/majors.lua`) and the shared test kit (`testkit/`), vendored whole into all eleven addons. | All eleven addons. |
| wow-addon | `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon` | The plugin: commands, agents, the bounded runner. | Every session. **Installed from GitHub** (`~/.claude/plugins/installed_plugins.json`: `wow-addon@wow-addon` 2.3.0, marketplace `tusharsaxena/wow-addon`, autoUpdate on), not from the sibling checkout. |

The last column decides the release mechanics at the end of this document: a change to WowAddonStandards
or wow-addon is invisible to the tooling until it is merged and pushed.

### Milestone 1 at a glance

| Group | Items | Effort (S/M/L) | Findings resolved | Of those, closed with no addon item | Clusters touched |
|---|---|---|---|---|---|
| WowAddonStandards | WS-01 … WS-08 | 6 / 2 / 0 | 25 | 11 | C02, C04, C11, C12, C17, C24, C26, C27, C34, C37, C46, C47 |
| LibKa0s | LK-01 … LK-33 | 17 / 14 / 2 | 49 | 36 (all 29 LibKa0s findings, plus 7 routed from addons) | C03, C08, C09, C10, C12, C13, C14, C15, C18, C20, C21, C26, C32, C35, C37, C38, C45, C47 |
| wow-addon | WA-01 … WA-03 | 3 / 0 / 0 | 5 | 5 | C01, C47 |
| **Total** | **44** | 26 / 16 / 2 | **79** | **52** | |

Severity of the 79: 1 High (`LibKa0s-R-01`), 7 Medium, 49 Low, 22 Info. **Every one of LibKa0s's 29
findings closes in this milestone.** The other 27 of the 79 are addon findings whose resolution needs
an upstream change *and* an addon change; each names its addon item in the per-item sections below and in
`05_TRACEABILITY.md`.

---

## Execution order, and the dependencies between the three repos

### Do LibKa0s items depend on WowAddonStandards rulings? Yes: seven of them.

| LibKa0s item | Waits on | Why |
|---|---|---|
| LK-06 (`test_eol` lone CR) | **WS-07** | `line-endings-§7` must stop saying "No file in the collection has one" before the kit gate that finds one ships. |
| LK-07 (prose gate scope, `synchronis`) | **WS-07** | The kit's `BRITISH` list must equal the standard's published list (`localization-§5`, 92 entries after WS-07). |
| LK-19 (DebugLog batched buffer trim) | **WS-07** | `MAX_BUFFER` stays 1500, which WS-07 makes the standard's number. |
| LK-11 (`Core.SafeRegisterEvent`) | **WS-04** | `events-frames-taint-§1` has to name the helper and the host-owned rejected list the library implements. |
| LK-18 (`Kit.assertLibraryConstant`, the Slash stub contract) | **WS-02** | The prescribed stub shape (one verbatim library string, no `FormatRow` copy, the library-absent line) is WS-02's ruling. |
| LK-23 (Schema `writeThrough`) | **WS-02** | `writeThrough` is route (a) of WS-02's degraded composed-row ruling. |
| LK-33 (cut v1.56.0) | **WS-08** | The README standards pointer rolls to v2.65.0, and the release notes cite it. |

WA-01 also waits on WS-01, because the plugin writes the consolidated span bundle WS-01 defines.

**No WowAddonStandards item has an LibKa0s item in its `depends_on`, but four of them name library
surfaces that do not exist yet.** WS-02 names `writeThrough`, `normalize`, `SetMany` (LK-22/LK-23) and
`Kit.assertLibraryConstant` (LK-18). WS-04 names `SafeRegisterEvent` (LK-11). WS-07 names the kit-26
lone-CR count (LK-06). WS-08 writes "v1.56.0, kit revision 26" into `library-stack-§7`. The standard is
written first and the library implements it, so the names are a contract. If an LK item has to change a
name or a signature while it is implemented, amend the same unreleased v2.65.0 changelog entry before the
merge. Do not ship a v2.65.1 to correct a version nobody outside this machine has seen.

### The order

1. **WS-01** opens v2.65.0. **WS-02 … WS-07** follow in any order. **WS-08** closes the entry.
2. **LK-01 … LK-32 in id order.** Id order is a valid topological order: no item depends on a higher
   id (checked against every `depends_on`). LK-01 goes first because later items write into
   `testkit/asserts.lua` and `testkit/prose_lists.lua` and need `framework.lua` and `test_prose.lua`
   under the 1500-line cap.
3. **LK-33** cuts v1.56.0 and tags it **locally**.
4. **WA-02** has no dependency and can land at any time. **WA-01** can land at any time after WS-01.
   **WA-03** goes last, after LK-33.
5. No addon repo is touched until Milestone 1 is complete. Every `RV-<AB>` depends on LK-33's local
   tag and on WA-01. WA-02 and WA-03 are plugin-only and are not ancestors of any `RV-`, but they are
   still Milestone 1 items, and Milestone 2 starts only once all of Milestone 1 is done.

The narrative below follows that order: WowAddonStandards, then LibKa0s, then the plugin.

**Critical path (13 items):** LK-01 → LK-02 → LK-24 → LK-25 → LK-26 → LK-27 → LK-28 → LK-29 → LK-30 →
LK-31 → LK-32 → LK-33 → WA-03. The Options chain (LK-24 … LK-28) is serial because each item edits
the same unreleased Options version document and moves its key. The WS chain (WS-01 → WS-0x → WS-08)
has to finish before LK-33 and is not on the critical path.

```
WS-01 ─┬─ WS-02 ─┬───────────────────────────── LK-18 (also LK-17) ─┐
       │         └───────────────────────────── LK-23 (also LK-22) ─┤
       ├─ WS-03                                                      │
       ├─ WS-04 ─────────────────────────────── LK-11 (also LK-10, LK-04)
       ├─ WS-05                                                      │
       ├─ WS-06                                                      │
       ├─ WS-07 ─┬───────────────────────────── LK-06 ──────────────┤
       │         ├───────────────────────────── LK-07 ── LK-08 ─────┤
       │         └───────────────────────────── LK-19 (also LK-02) ─┤
       └─ WS-08 (after WS-02..07) ──────────────────────────────────┤
                                                                     ├─ LK-33 ─ WA-03
LK-01 ─ LK-02 ─┬─ LK-03, LK-10, LK-12..LK-17, LK-19..LK-22, LK-24 ───┤
       │       └─ LK-24 ─ LK-25 ─ LK-26 ─ LK-27 ─ LK-28 ─ LK-29 ─ LK-30 ─ LK-31 ─ LK-32
       ├─ LK-04 ─ LK-05
       └─ LK-09
WS-01 ─ WA-01          WA-02 (free)        LK-33 + WA-02 ─ WA-03
```

---

# Group A — WowAddonStandards (v2.64.0 → v2.65.0)

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards`. Docs only, LF repo. Every item
appends a numbered paragraph to the one v2.65.0 changelog entry in `standards/STANDARDS.md`, and nobody
bumps the version a second time. The verify commands include
`git ls-files -z | xargs -0 grep -lI $'\r'`, which must print nothing.

**Blast radius for the whole group.** The standard binds all eleven addons. A ruling changes nothing
in an addon until that addon applies it, so the cost of each item is its consumer follow-ups. The
standard also feeds `/wow-addon:standards-audit`, `/wow-addon:review` and
`/wow-addon:revendor-standards`, and all three read it **from GitHub**. Until the merge, those tools
still see v2.64.0.

---

## WS-01 · Open v2.65.0; the AUDIT.md re-vendor check grades by step 5, counts same-day commits and reads a consolidated span bundle

**Resolves (7, all Info/Low, all closed here):** `AbsorbTracker-A-22`, `AuraMaster-A-20`,
`ConsumableMaster-A-03`, `KICKCD-A-02`, `LootHistory-A-22`, `PanelMaster-A-16` (step 4 hard-codes High
while step 5's impact table grades a docs-only gap Low), `PartyFrameEnhanced-A-19` (the check's
`git log --since="$horizon"` skips same-day commits). Cluster C02.

**Change.**
- `standards/STANDARDS.md` line 1 becomes `# Ka0s WoW Addon Standard (v2.65.0, <date>)`. The entry
  `- **v2.65.0 (<date>):**` opens with paragraph (1).
- `AUDIT.md`, re-vendor bundle check (about :296-347): `--since="$horizon 00:00"`. Git fills a bare
  date's time from the clock, which is why same-day commits vanish. Both hard-coded High grades (:335,
  :341-342) are replaced with "graded by step 5 like every other: an unrecorded re-vendor is doc-only,
  so **Low**, and the entry names the `audit-review-history` MUST it fails". One sentence says step 5
  governs every grade in step 4.
- The recorded-side loop reads a two-tag folder (`docs/revendor/<YYYY-MM-DD>-v<A>-v<B>/`) by emitting
  every `v[0-9]+\.[0-9]+\.[0-9]+` on line 1 of its `01_DELTA.md` instead of `tail -1`. The single-tag and
  bare-date branches are unchanged.
- `standards/standards/audit-review-history.md` defines the **consolidated span bundle** as the
  sanctioned record for a lapsed span: `01_DELTA.md` and `05_SUMMARY.md` only; line 1 exactly
  `Delta: LibKa0s v<A> -> v<B> (span: v<A> v<...> v<B>)`; one `05_SUMMARY.md` line per tag ("carried by
  sweep, nothing adopted" or the adoption sha). Frozen bundles are never edited. A base misstatement is
  corrected in the next bundle.

**Ripple.** Changelog paragraph (1). No executable gate. The behavioral check runs the current loop over
a scratch copy of `AuraMaster/docs/revendor/` plus a fake span folder (records only the last tag), then
the amended loop (records all three).

**Blast radius.** Every addon's next audit. The span-bundle format is also the output format of WA-01.

**Consumer follow-ups (one span bundle per addon):** AbsorbTracker AT-25 (v1.18.0…v1.55.0),
AuraMaster AM-02, BankLedger BL-23, ConsumableMaster CM-28, KickCD KC-24, LootHistory LH-34,
MultiMeters MM-30, PanelMaster PM-18, PartyFrameEnhanced PF-24, PrettyChat PC-25, WhatGroup WG-29.
Two corrections from the addon planners: AuraMaster's span is **22 tags**, not the finding's 20 (the
provenance history also shows v1.43.0 at `76224d7` and v1.45.0 at `8923a1a`). PanelMaster's line 1 must
match WA-01's final template byte for byte, because this check reads every tag on it.

**Depends on:** nothing. **Effort:** S.

---

## WS-02 · Rule the degraded composed-row conflict: hollow composers stand; host verbs write through a declared `writeThrough` list or refuse with one library-absent line

**Resolves:** `AbsorbTracker-A-23` (Info, closed here): `options-ui-§1`'s hollow-composer rule collides
with `slash-commands-§1/§2`'s live `enable`/`disable` on a degraded load. Cluster C26. **Owner-scope
issues:** PartyFrameEnhanced#14 and WhatGroup#22 (whose owner ruling takes route (b)).

**Change.**
- `options-ui.md §1` (the hollow-composer and fall-together passage, about :50-60). Keep "a
  library-absent Options stub's composers answer `{}`" and anti-pattern #73 (no host copies). Replace
  the fall-together bound with this rule: on a library-absent load, a host verb whose write targets a
  composed row (`enabled`, `locked`, test mode, the combat re-lock, the launcher stub) **MUST** either
  (a) write through the schema seam's declared `writeThrough` path list (LibKa0s-Schema-1.0 minor 2,
  LibKa0s v1.56.0, kit 26), which is data handed to both the live instance and the stub, or
  (b) refuse with the library-absent line. It **MUST NOT** raise and **MUST NOT** acknowledge a write
  that did not land. `enable`/`disable` **SHOULD** take (a). Taking (b) for them is a SHOULD deviation
  recorded in the host's Documented deviations.
- `slash-commands.md §1`: the library-absent line, through the locale, one sentence, one placeholder:
  `%s is unavailable: the LibKa0s library did not load.` (`%s` is the full verb, e.g. `/wg enable`). A
  library-absent Slash stub **MAY** carry exactly one library string verbatim, `DISABLED_LINE_FORMAT`,
  and **MUST** pin it with `Kit.assertLibraryConstant`. It **MUST NOT** copy `FormatRow`. Minimal
  `OnSlash` dispatch is sanctioned. `§7` cross-references the verbatim refusal line.
- `library-stack.md §7` Schema row names `writeThrough`, `normalize` and `SetMany` as minor-2 surfaces.
  `anti-patterns.md` #73 cross-references the writeThrough route.
- Changelog paragraph (2), citing AbsorbTracker's review item 62 / Info-6 (not plan item AT-62),
  PartyFrameEnhanced#14 and WhatGroup#22.

**Ripple.** Standard text only. The executable halves are LK-18 (the kit assertion and the Slash stub
doc) and LK-23 (the Schema field and the reference stub).

**Blast radius.** Every addon with a library-absent build, which is all eleven. Each has to decide
route (a) or (b) for its composed-row verbs.

**Consumer follow-ups, by route.**

| Route | Addon items |
|---|---|
| (a) `writeThrough` | AbsorbTracker AT-08, AT-09 (`{enabled, locked}`); AuraMaster AM-16 (mirrors the semantics in its own seam and passes the list to `S.New`); BankLedger BL-10 (`settings.enabled`); KickCD KC-18, KC-19 (`{enabled, locked}`); LootHistory LH-15, LH-16; MultiMeters MM-15; PanelMaster PM-09 (enable/disable); PartyFrameEnhanced PF-11, PF-12 (#14) |
| (b) library-absent line, SHOULD deviation row | ConsumableMaster CM-18 (a library-absent load has no Lifecycle latch, so a written-through `enabled` would not be obeyed that session); WhatGroup WG-12 (#22, owner ruling) |
| None planned | PrettyChat. Its degraded `MasterControls` stub emits leaves instead of answering `{}` (`settings/OptionsSetup.lua:156-203`). The 2026-09-23 audit did not file it, so no item covers it. The next audit against v2.65.0 may grade it. |

**Depends on:** WS-01. **Effort:** M.

---

## WS-03 · Rule migration-stamp ownership: defaults declare `schemaVersion = 0`, the runner owns the stamp, profile steps run per profile

**Resolves:** `WHATGROUP-R-03` (Medium: the default equals the current version, so AceDB strips it at
logout and the first real migration is skipped for every existing user), `LootHistory-A-18` (Low),
`PanelMaster-A-17` (Info). Cluster C11. All three also need an addon item: WG-08, LH-12, PM-10.

**Change.**
- `savedvariables.md §1` template (:10, :18-24): `global = { schemaVersion = 0 }`. The text explains why.
  AceDB's `removeDefaults` strips a stored value equal to its default at logout, so a default equal to
  the current version never persists (WhatGroup F-003). AceDB also backfills a declared default onto a
  legacy account with no stamp, which a current-version default would mask (PanelMaster `febf108`). A
  default of 0 has neither problem.
- New rules: `NS.SCHEMA_VERSION` is the runner's target. The stamp advances only past a step that
  returned without raising. A profile-scoped step runs for **every stored profile** (walk the raw SV
  `profiles` table), or idempotently on `OnProfileChanged` with a per-profile stamp. It is never gated by
  the account-wide stamp alone (KickCD R-01, PartyFrameEnhanced R-15, PrettyChat R-03). Every step is
  idempotent against a fresh default profile.
- `toc-file.md §2` (:55), `versioning-git.md` (:8, "add a runner step and raise `NS.SCHEMA_VERSION`;
  the defaults value stays 0"), `open-evolutions.md` (:15-24, "Migration-stamp ownership" moves to ruled
  at v2.65.0). Changelog paragraph (3).

**Ripple.** Standard text only. The executable form is each addon's own red-first migration test.
The plan fixes this at the template, not with a library runner, because the steps are host-specific
and a runner is about 20 lines (see *Considered and not done upstream*).

**Blast radius.** Every addon with a migration runner, which is all eleven. The WS-06 minimap rename
adds no step under this rule: the stored key does not move, so no addon writes a minimap migration or
bumps its schema version.

**Consumer follow-ups:** AbsorbTracker AT-06, AuraMaster AM-10, BankLedger BL-11 (global-only, nothing
per-profile to walk; `ResetEverything` re-stamps after the wipe), ConsumableMaster CM-16, KickCD KC-03
(color-shape and font-flag steps per profile), LootHistory LH-12 (1 → 0), MultiMeters MM-12 (MM-13's
v15 → v16 step depends on it), PanelMaster PM-10, PartyFrameEnhanced PF-08, PrettyChat PC-03 (the 0 is
already declared at `core/Database.lua:36`; PC-14 moves it into `defaults/Profile.lua`), WhatGroup WG-08.

**Depends on:** WS-01. **Effort:** S.

---

## WS-04 · Settle `events-frames-taint-§1` against `library-stack-§1`, name LibKa0s-Core's `SafeRegisterEvent` as the helper, and state `architecture-§4`'s threshold

**Resolves:** `PRETTYCHAT-A-08`, `PRETTYCHAT-A-11`, `WHATGROUP-A-04` (all Low). Clusters C04, C34. Each
also needs a doc edit in the addon (PC-12, WG-23).

**Change.**
- `events-frames-taint.md §1`. (a) Carve-out: an addon that embeds **no** AceEvent-3.0 **MAY** carry
  one lazily created private watcher frame for non-unit boundary events (`PLAYER_REGEN_DISABLED/ENABLED`).
  The frame is fully unregistered on stand-down and listed in `## Event Subscriptions`, with no register
  row. An addon that embeds AceEvent gets no carve-out. (b) Name the helper: from LibKa0s v1.56.0,
  "the single pcalled helper" is `LibKa0s-Core-1.0`'s `SafeRegisterEvent` / `SafeRegisterUnitEvent` /
  `SafeRegisterEvents` (LK-11), which front-gates on `C_EventUtils.IsEventValid` when present. The host
  owns the rejected list and surfaces it in `[Init]` or a debug verb. Its Core stub carries one-rung
  pcall bodies.
- `library-stack.md §1` (:24): the PrettyChat citation cites the carve-out instead of contradicting it.
- `architecture.md §4` (:60-71): the bus threshold is "two or more feature modules, or a feature module
  that registers game events and whose events a second feature module must react to". The AceAddon
  object's own handlers are not a feature module. Keep the same-target clobber rationale.
- Changelog paragraph (4).

**Blast radius.** Every addon (the helper is named for all eleven). The carve-out applies to PrettyChat
only. The threshold decides the bus MUST for WhatGroup and PrettyChat.

**Consumer follow-ups:** PrettyChat PC-12 (the combat watcher at `modules/Override.lua:120-139` is the
carve-out; `## Message Bus` cites the threshold), WhatGroup WG-23 (shell plus one feature module is
below the threshold), ConsumableMaster CM-15 (depends on it for the rejected-list surface). The helper's
own adoption is under LK-11.

**Depends on:** WS-01. **Effort:** S.

---

## WS-05 · Give `compat` an applicability condition: `core/Compat.lua` is required only by an addon that owns a deprecated or version-variant call

**Resolves:** `AbsorbTracker-A-15`, `PRETTYCHAT-A-18` (both Low). Cluster C27. Each also needs its dead
rung deleted (AT-16, PC-15).

**Change.** `compat.md` (:5, :25): "every addon MUST ship `core/Compat.lua`" becomes "an addon that calls
any deprecated or version-variant client API outside LibKa0s's majors MUST own those calls in
`core/Compat.lua`, the only file allowed to make them. An addon with none carries no `Compat.lua` and
records `compat-layer` as Not applicable, citing this condition." Add: a library-absent fallback rung that
calls a global every supported client provides only through a newer namespace (e.g. `GetAddOnMetadata`
behind `C_AddOns`) is dead code and **MUST** be deleted rather than shimmed. `library-stack.md §7`
(:88) cites the condition. `documentation.md §3`: the `compat-layer.md` trigger counts shims in a
*present* `core/Compat.lua`. Changelog paragraph (5).

**Blast radius.** The two addons with no `core/Compat.lua` (AbsorbTracker, PrettyChat). The dead-code
sentence reaches every addon that carries a legacy global rung.

**Consumer follow-ups:** AbsorbTracker AT-16 (`core/EnvSetup.lua:70-71`), PrettyChat PC-15
(`core/EnvSetup.lua:75-76`), LootHistory LH-26 (`core/EnvSetup.lua:56-58`), AuraMaster AM-19 (the
pre-11.0 `GetMouseFocus` rung). PanelMaster's planner found a candidate outside the plan:
`Compat.AddOnFolders`' `GetNumAddOns`/`GetAddOnInfo` rung may become dead code under this sentence, and
it is why that function sits at CCN 15. PM-20 only documents it. Deleting it is the owner's call.

**Depends on:** WS-01. **Effort:** S.

---

## WS-06 · Clarify reserved verbs in sub-trees, the value-hold verb, who pins a library strip, and the minimap row's CLI path polarity

**Resolves:** `KICKCD-A-27` (Info), `AbsorbTracker-A-14` (Low), `PRETTYCHAT-A-26` (Info, closed here),
`WHATGROUP-R-15` (Low). Clusters C37, C46, C47.

**Change.**
1. `slash-commands.md §2` (:31): `enable`/`disable` are reserved at the top level. Under a feature
   noun's sub-tree (`/<slash> <noun> enable <id>`) they **MAY** toggle that noun's items (KickCD
   `/kcd spells`).
2. `options-ui.md §15` and `preview-mode.md`: an addon whose unlocked view is its preview ships no
   `test` verb. A one-shot value hold, if kept, lives at `/<slash> debug hold <value> [secs]`.
3. `options-ui.md §13` Testing: for a strip the library draws (`O.TabStrip`, `O.RenderTabbedSchema`),
   the library suite pins the wrap invariance and a consumer **MUST NOT** duplicate it
   (`testing-§8`). A host-drawn strip is pinned by the host.
4. `launcher.md §3`, cross-referenced from `options-ui.md §15`: storage stays LibDBIcon's `minimap.hide`
   and a stored `shown` key is still forbidden (anti-pattern #81). The minimap row's schema path, which
   is its CLI name, **MUST** read in the row's own sense, `<root>.minimap.shown`, with get/set closures
   that invert onto `minimap.hide`. Commencement: each addon's next release. No SavedVariables
   migration, because the stored key does not move.

Changelog paragraph (6).

**No migration anywhere (plan-review decision 1).** WS-06's sentence stands as written. Every existing
player's `hide = true` survives the rename with no code, because the stored value stays LibDBIcon's
`db.global.minimap.hide`. An earlier reconcile pass had added defensive "fold a stray `shown` key" steps
to four addons and called them an owner requirement. The owner made no such ruling, and three of the
four steps were also wrong under AceDB's copyDefaults (`hide == nil` is never true once `hide = false`
is materialized). Those steps are gone: PF-26 and PC-27 are dropped, and LH-13 and WG-11 carry no step.
No addon bumps its schema version for the rename. Instead, all eleven rename items carry one identical
carry-over check, written test-first: a legacy store with `minimap = { hide = true, minimapPos = 200 }`
reads `<root>.minimap.shown` as false, the button stays hidden, `minimapPos` is untouched, and no `shown`
key is ever written to the raw SV after a set.

**Blast radius.** The minimap rename touches all eleven addons' schema, docs, tests and `/<slash> get|set`
path. It is a player-visible CLI change: `/<slash> set <root>.minimap.hide` answers "unknown setting"
afterwards, and every addon's release notes must say so. The hold verb affects AbsorbTracker only. The
sub-tree ruling affects KickCD only. The strip-pin ruling removes duplicated wrap cases from any
consumer that pins a library strip.

**Consumer follow-ups.**
- Minimap path, each with the carry-over check above and no migration: AbsorbTracker AT-12, AuraMaster
  AM-14, BankLedger BL-12, ConsumableMaster CM-19, KickCD KC-17, LootHistory LH-13, MultiMeters MM-16,
  PanelMaster PM-11, PartyFrameEnhanced PF-13, PrettyChat PC-13, WhatGroup WG-11.
- Hold verb: AbsorbTracker AT-11 (`/at test` → `/at debug hold`).
- Sub-tree: KickCD KC-25 records the ruling. `KICKCD-A-27` closes by rule.
- Strip pin: AbsorbTracker AT-15; ConsumableMaster CM-20 deletes its duplicated wrap-geometry cases.

**Depends on:** WS-01. **Effort:** S.

---

## WS-07 · Text corrections: debug buffer 1500, bootstrap underscore, the settings-panel table, the TOC literal, `.png ships`, `synchronis`, and the lone-CR note

**Resolves:** `AbsorbTracker-A-21`, `PRETTYCHAT-A-28` (both Info, closed here), `WHATGROUP-A-22`,
`WHATGROUP-A-23` (Info; WG-26 re-checks the addon side), `ConsumableMaster-A-06` (Low; CM-01 fixes the
spelling). Clusters C02, C12, C17, C24, C47.

**Change.**
1. `debug-logging.md §1` (:22, :126, :199) and `NEW_ADDON_CONTEXT.md` (:658, :1274): the ring buffer is
   **1500** lines, matching LibKa0s `DebugLog` `MAX_BUFFER` (a perf dump overflowed 500).
2. `architecture.md §1` (:7-11): "destructure both varargs; name the first `_` when the file never reads
   it". This removes the conflict with lint's warning 211.
3. `documentation.md §3` `settings-panel.md` row (:237): a `Page | Covers` table, one row per settings
   subcategory page, plus the page → tab → row tree.
4. `toc-file.md §3` (:10, :61): drop "currently 120007"; point at `standards/ADDONS.md` and
   `/wow-addon:bump-interface`.
5. `layout.md §4` (:125): the editable `.png` is committed but excluded by a `.pkgmeta` ignore.
6. `localization.md §5` `BRITISH`: add `synchronis` (91 → 92). No US word contains it. Published
   counts become 92/33.
7. `line-endings.md §7` (:505-510): from kit 26, `test_eol` counts lone CRs in every scanned path. Delete
   "No file in the collection has one" (AuraMaster has one).

Changelog paragraph (7).

**Blast radius.** Doc text in every addon that restates these (the `_` bootstrap, the buffer size, the
TOC literal). Points 6 and 7 become executable in kit 26 (LK-06, LK-07) and redden two addons (below).

**Consumer follow-ups:** ConsumableMaster CM-01 (`synchronisation` at `docs/settings-panel.md:80`,
before RV-CM), WhatGroup WG-26 (`Page | Covers`, `.pkgmeta` png ignore). Point 7's red is AuraMaster's
(`tests/page_helpers.lua:80`, AM-01, under LK-06).

**Depends on:** WS-01. **Effort:** S.

---

## WS-08 · v2.65.0 ripple: executive summary, context pack, playbooks, README; close the changelog entry

**Resolves:** no finding of its own. It makes WS-02 … WS-07 consistent everywhere the standard restates
them.

**Change.** Carry WS-02 … WS-07 into `standards/EXECUTIVE_SUMMARY.md`, `standards/NEW_ADDON_CONTEXT.md`
(the `schemaVersion = 0` template and per-profile runner, the `_` bootstrap, the 1500-line buffer, the
minimap row at `<root>.minimap.shown`, `SafeRegisterEvent` through Core and the Core stub's one-rung
bodies, `writeThrough` and the library-absent line in the Slash/Options stub templates, the span
bundle), `NEW_ADDON.md` and `AUTOMATED_TESTS.md` wherever they quote changed text, `README.md`'s version
mention, `CLAUDE.md`'s "As of vX" sentence if it moves, and `library-stack.md §7`'s LibKa0s inventory
sentence (v1.56.0, kit 26, 21 files, unchanged). Date the entry and add its one-line summary.

**Recommended addition (not in the item today).** LK-25 makes the library park a combat-time
`CreateOptionsPanel` and replay it at `PLAYER_REGEN_ENABLED`, in every consumer. `options-ui-§9` says
category registration is taint-free and eager (:105, :233-236), and WhatGroup's own test
(`tests/test_panel.lua:100-110`) pins "registering during combat still registers" as the fix for
WG-A-12. No WS item rules on the park. Before LK-25 lands, either add a sentence to `options-ui-§9` in
this entry (the library **MAY** park a registration requested under `InCombatLockdown()` and **MUST**
replay it once at `PLAYER_REGEN_ENABLED`, whatever the host's stand-down state), or narrow LK-25 (see
LK-25). The WhatGroup planner flagged this and WG-02 re-pins the two cases either way.

**Ripple.** Closes the changelog entry. After this, `grep -rnE '§[0-9]+\.[0-9]+'` over `standards`,
`AUDIT.md` and `NEW_ADDON.md` prints nothing, and `v2.64.0` survives only in historical mentions.

**Blast radius.** Every scaffold and audit that reads the context pack. `/wow-addon:new-addon` fetches it
at run time, so a new addon started after the merge is born on v2.65.0.

**Consumer follow-ups: `/wow-addon:revendor-standards` to v2.65.0 in all eleven**, rolling the TOC
`## X-Standard`, the README badge and `CLAUDE.md`'s "Standards compliance": AbsorbTracker AT-26,
AuraMaster AM-35, BankLedger BL-25, ConsumableMaster CM-31, KickCD KC-27, LootHistory LH-36,
MultiMeters MM-32, PanelMaster PM-16, PartyFrameEnhanced PF-25, PrettyChat PC-26, WhatGroup WG-30.
**All eleven are Milestone 4 and owner-gated: they are blocked until the owner merges and pushes
v2.65.0** (see *Release mechanics*).

**Depends on:** WS-02 … WS-07. **Effort:** M.

---

# Group B — LibKa0s (v1.55.0 → v1.56.0)

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s`. Every item's verify runs, through
`~/.claude/wow-addon/bin/ka0s-bounded`, `luacheck .`, `lua5.1 tests/run.lua`, the `--list` diff against
`docs/test-cases.md`, `lizard -l lua -x './libs/*' -x './tests/_kit/*' -C 15 -w .` (must print nothing)
and, for kit items, `diff -r testkit tests/_kit` (must be empty). LibKa0s has no `tests/perf.lua`, so
perf is a skip with reason (1).

### The versioning rules this release follows

- **One bump per file per release.** The first item that touches a file bumps its LibStub minor and
  creates `docs/api/<Major>/version-<new>-docs.md` and its members JSON (`lua5.1 tools/gen-api-members.lua`).
  Later items extend the same unreleased document and regenerate the JSON. They never bump twice. The
  previous document becomes Superseded with a "Moving to" note, and `docs/api/README.md` gains a row.
- **Kit revision 26** is bumped once, by LK-01. `docs/api/testkit/version-26-docs.md` collects every
  later kit item.
- **`CHANGELOG.md`'s `## v1.56.0 — unreleased` block** is opened by LK-01 and dated by LK-33.
  `tests/test_versioning.lua` fails if the block's versions line and `lib.MODULES` disagree, so every
  minor-bumping item edits that line in the same commit.
- **The Options version key** (Options.WIDGETS.TABS.COMPOSE.SCROLL) moves three times inside the
  release: `23.30.3.7.3` → `24.30.3.7.4` (LK-24) → `24.31.3.7.4` (LK-26) → `24.31.4.7.4` (LK-27). The one
  unreleased Options document is renamed each time. Only `version-23.30.3.7.3-docs.md` becomes Superseded.

### Per-file minor table (what v1.56.0 ships)

| Major / file | v1.55.0 | v1.56.0 | Bumped by | Extended by | New docs/api document |
|---|---|---|---|---|---|
| Core | 7 | **8** | LK-10 | LK-11 | `Core/version-8-docs.md`, `members-8.json` |
| Item | 1 | **2** | LK-12 | — | `Item/version-2-docs.md`, `members-2.json` |
| Media | 3 | **4** | LK-13 | — | `Media/version-4-docs.md`, `members-4.json` |
| Bus | 1 | **2** | LK-14 | — | `Bus/version-2-docs.md`, `members-2.json` |
| Lifecycle | 1 | **2** | LK-15 (comment only; the bytes move) | — | `Lifecycle/version-2-docs.md`, `members-2.json` |
| Launcher | 1 | **2** | LK-16 | — | `Launcher/version-2-docs.md`, `members-2.json` |
| Slash | 14 | **15** | LK-17 | LK-18 (doc only) | `Slash/version-15-docs.md`, `members-15.json` |
| DebugLog | 12 | **13** | LK-19 | — | `DebugLog/version-13-docs.md`, `members-13.json` |
| Perf / PerfPanel | 12 / 5 | **13** / 5 (key 12.5 → 13.5) | LK-20 | — | `Perf/version-13.5-docs.md`, `members-13.5.json` |
| Widgets / DragHandle | 9 / 2 | **10** / 2 (key 9.2 → 10.2) | LK-21 | — | `Widgets/version-10.2-docs.md`, `members-10.2.json` |
| Schema | 1 | **2** | LK-22 | LK-23 | `Schema/version-2-docs.md`, `members-2.json` |
| Options (`MINOR`) | 23 | **24** | LK-24 | LK-25, LK-28 | one `Options/version-24.31.4.7.4-docs.md` by release end |
| OptionsScroll (`SCROLL_MINOR`) | 3 | **4** | LK-24 | — | (in the Options key) |
| OptionsWidgets (`WIDGETS_MINOR`) | 30 | **31** | LK-26 | LK-28 | (in the Options key) |
| OptionsTabs (`TABS_MINOR`) | 3 | **4** | LK-27 | LK-28 | (in the Options key) |
| OptionsCompose (`COMPOSE_MINOR`) | 7 | 7 | — | — | — |
| Env, Compat, Pool | 1, 1, 3 | unchanged | — | — | — |
| **Test kit** (`Kit.VERSION`) | 25 | **26** | LK-01 | LK-02 … LK-09, LK-18, LK-27 | `testkit/version-26-docs.md` |

The v1.55.0 values were read from the working tree with the WA-01 grep
(`grep -hoE 'local (MAJOR, )?[A-Z_]*MINOR *= *("[^"]+", *)?[0-9]+' LibKa0s/*.lua`) and
`testkit/framework.lua:20`.

### Which consumers take which major (measured, excluding `libs/` and `tests/`)

| Major | Acquired by | Where |
|---|---|---|
| Core, Slash, DebugLog, Lifecycle, Launcher, Media, Options | **all eleven** | `core/CoreSetup.lua`, `settings/Slash.lua`, `core/DebugLogSetup.lua`, `core/LifecycleSetup.lua` (AbsorbTracker: `core/Lifecycle.lua`), `core/LauncherSetup.lua`, `core/MediaSetup.lua`, `settings/*` |
| Bus | 8: AT, AM, BL, CM, KC, LH, MM, PF | `core/Bus.lua` or `core/Constants.lua` (MultiMeters also `core/Namespace.lua:211`) |
| Perf | 6: AT, AM, CM, KC, MM, PF | `core/PerfSetup.lua`. BL, LH, PM, PC and WG decline Perf. |
| Pool | 5: AM, BL, KC, LH, MM | `core/PoolSetup.lua` |
| Schema | 5 today: AT, BL, LH, PM, PC | `settings/Schema.lua` (AT :223, BL :441, LH :587, PM :351, PC :715). After Milestone 3: all eleven (AM-15, CM-17, KC-18, MM-14, PF-11, WG-12). |
| Widgets | 7: AT, AM, BL, CM, KC, LH, MM | `ReorderList` callers: CM `settings/Category.lua:725, :940`; KC `settings/Spells.lua:1143`; LH `core/WidgetsSetup.lua:150` (used at `settings/Panel.lua:674`); MM `settings/ColumnBlocks.lua:241` |
| Item | 3: BL, CM, LH | `core/ItemSetup.lua` |
| Test kit | **all eleven** | `tests/_kit/` |

---

## LK-01 · Kit revision 26 groundwork: peel `framework.lua`'s assertion and parity families into `asserts.lua`, and `test_prose`'s lists into `prose_lists.lua`

**Resolves:** `LibKa0s-A-04` (Low: the census claims a "Ratified deviation row" for
`testkit/framework.lua` that the register does not hold). Cluster C14.

**Change.** No behavior change. (a) New `testkit/asserts.lua` (`return function(Kit)`) takes
`Kit.assertEqual/True/False/Nil/Near/Error` (:235-303) and `Kit.setSurfaceSource`, `callable`,
`resolveSurface`, `Kit.publicMembers`, `Kit.assertSurfaceParity` (:305-452). `framework.lua` loads it
where the block stood, from a dir derived from `debug.getinfo(1, "S").source` (fallback `tests/_kit/`),
and drops from **1583** to about 1360 lines, under the cap. (b) New `testkit/prose_lists.lua` takes
`BRITISH`, `ALLOWED`, `PUBLISHED_*` (`test_prose.lua:158-198`) and `SKIPPED_DIRS` (:209-213).
`test_prose.lua` drops from **1499** to about 1450, and later list growth lands outside it. LibKa0s's own
`tests/test_prose.lua` exempts `testkit/prose_lists.lua` (:73). (c) `Kit.VERSION` 25 → 26. (d) Open the
`## v1.56.0 — unreleased` block. (e) `CLAUDE.md`: delete the over-cap census row for `framework.lua` and
fix the census counts.

**Ripple.** Kit 26 (bumped here, and only here). `docs/api/testkit/version-26-docs.md` created from
version-25 (Supersedes 25; "two new files, no behavior change"). `testkit/README.md` inventory. Sync
`tests/_kit`. Tests: totals and `--list` byte-identical before and after, apart from kit-revision lines.
One red-first case in `tests/test_kitsync.lua` (both files exist in `testkit/` and `tests/_kit/`).

**Blast radius.** All eleven receive two new kit files at their re-vendor. No behavior change.

**Consumer follow-ups:** none of its own. It is carried by every `RV-<AB>`.

**Depends on:** nothing. **Effort:** M.

---

## LK-02 · `Kit.assertErrorMatches`, and the 23 statement-position `assertError` calls assert on the raised text

**Resolves:** `LibKa0s-R-07` (Low). Cluster C37.

**Change.** `testkit/asserts.lua` gains `Kit.assertErrorMatches(fn, needle, msg)`: pcalls, fails if
`fn` did not raise or if `tostring(err):find(needle, 1, true)` is nil, returns `err`, and is exposed by
`Kit.expose`. The 23 call sites are rewritten to assert on a substring: `tests/test_launcher.lua:123-128`
(×4; the strings now passed as failure messages become the needles), `test_kit_inventory.lua` (×5),
`test_mock_ace.lua` (×9), `test_loader.lua:116-117`, `test_options_compose.lua:674-675`,
`test_schema.lua:548`.

**Ripple.** Kit 26 doc: new member, Since 26. New `tests/test_kit_asserts.lua` (three red-first cases).
Each rewritten site is shown red once by changing its needle locally. After it,
`grep -nE '^\s*(T\.|Kit\.)?assertError\(' tests/*.lua` prints nothing.

**Blast radius.** A new kit member in all eleven. Nothing changes for a consumer that does not call it.
LK-03 and LK-18 use it.

**Consumer follow-ups:** none required.

**Depends on:** LK-01. **Effort:** M.

---

## LK-03 · AceDB fake fidelity: `CopyProfile` and `DeleteProfile` raise as AceDB-3.0 does, and `SetProfile` strips defaults

**Resolves:** `AbsorbTracker-R-06`, `PartyFrameEnhanced-R-09` (both Medium). Cluster C09. Both were
routed upstream and are dispositioned here.

**Change.** `testkit/mock_record.lua:241-270`. `CopyProfile(name, silent)` raises AceDB's own message at
level 2 when `name` is the current profile, and when the source is missing unless `silent`.
`DeleteProfile(name, silent)` raises on the active profile, and on a missing one unless `silent`.
Messages are copied byte for byte from a vendored `libs/AceDB-3.0/AceDB-3.0.lua:531-537` and `:581-587`,
with the line cited. `SetProfile(name)` runs a `removeDefaults` mirror over the **outgoing** profile
before switching (AceDB :460-463): scalar and plain-table arms, with the unmodeled `*`/`**` wildcard
arms named in a comment. Callback firing is unchanged.

**Ripple.** Kit 26 doc marks this **behavioral**. Seven red-first cases in `tests/test_mock_record.lua`,
asserted with `assertErrorMatches`. `mock_record.lua` already holds two functions at exactly CCN 15
(`liveTimers` :95, `M.__fire` :539), so the new branches must go in new functions, not into those two.

**Blast radius.** Every consumer suite that calls these on a bad name, or relies on a value equal to
its default surviving a profile switch. KickCD owns its own AceDB fake and is unaffected.
ConsumableMaster keeps a whole local AceDB fake (see CM-02).

**Consumer follow-ups:** AbsorbTracker AT-03 (guard names before AceDB sees them; `AbsorbTracker-R-02`),
PartyFrameEnhanced PF-01 (the `exists()` guards and three refusal lines for `PartyFrameEnhanced-R-05`,
with no `pcall` around `db:CopyProfile`), ConsumableMaster CM-02. **The CM follow-up cannot be taken
literally.** It says "drop `tests/wow_mock.lua`'s SetProfile override", but that file keeps a whole local
AceDB fake, because the kit's fake has no CallbackHandler string-method form and no `db.profiles`. CM-02
brings the local fake to kit-26 fidelity instead. Retiring it would need those two features in the kit,
which is not in this milestone.

**Depends on:** LK-02. **Effort:** S.

---

## LK-04 · Kit mock: a recording `EventRegistry`, frame `RegisterEvent`/`RegisterUnitEvent` honoring `__badEvents`, and `C_EventUtils.IsEventValid`

**Resolves:** `PartyFrameEnhanced-R-10` (Low; PF-05 also needs an addon change). Cluster C09.

**Change.** New `testkit/mock_events.lua`, loaded by `testkit/mock_base.lua` through its own dir.
`mock_base.lua` is 1446 lines and grows by at most the load line. (1) `EventRegistry` with
`RegisterCallback`/`UnregisterCallback`/`TriggerEvent`; each live callback appears in
`M.__registrations()` as `{ kind = "callback", event, owner }`. (2) stubFrame `RegisterEvent` and
`RegisterUnitEvent` (metatable no-ops today) raise `Attempt to register unknown event "<NAME>"` for a
name in `M.__badEvents`, read at call time, with the message the AceEvent path uses at
`mock_base.lua:715-727`. (3) `C_EventUtils.IsEventValid(name)` answers false for bad names; a suite may
set `C_EventUtils = nil` to model an older client.

**Ripple.** Kit 26 doc (three members, Since 26). New `tests/test_mock_events.lua`.

**Blast radius.** **Behavioral** in every consumer suite that surveys `__registrations()`: a surviving
`EventRegistry` callback now shows up. Consumers with their own `EventRegistry` fake (WhatGroup) are
unaffected until they drop it.

**Consumer follow-ups:** PartyFrameEnhanced PF-05 (the surviving `callback|EditMode.Exit` entry is the
red that `Providers:Suspend`'s `UnregisterCallback` turns green; `sig()` must handle a callback entry with
no `target`), WhatGroup WG-10 (shrink the local fake to the kit's). AbsorbTracker AT-07 and
ConsumableMaster CM-15 use `__badEvents` and `IsEventValid` in their LK-11 tests.

**Depends on:** LK-01. **Effort:** M.

---

## LK-05 · Kit mock `CreateFrame` starts shown, as the client does; collection dry-run of the flip

**Resolves:** `PartyFrameEnhanced-A-02` (Low, dispositioned here). Cluster C09.

**Change.** `testkit/mock_base.lua:121`: `local f = { __shown = true, __scripts = {} }`. Update the
comment and fidelity rule 5's note. Audit this repo's suites that read shown state and fix any case that
relied on hidden-by-default by giving its setup the `Hide()` production performs, never by weakening an
assertion. Then run the **collection dry-run**: `git -C ../<A> archive HEAD` into a temp dir, copy
`testkit/.` over its `tests/_kit/`, run the suite bounded, write `<scratchpad>/dryrun-lk05-<A>.txt`. It
touches no addon repo. Every red goes into the commit body and becomes a pre-re-vendor fix for that
addon.

**Ripple.** Kit 26 doc: a behavioral flip, with a consumer note that a stand-down suite's `F_on`
baseline now sees container frames. One red-first case in `tests/test_mock_base.lua`.

**Blast radius.** The most likely source of kit-26 reds. Suites with a shown-state baseline:
PartyFrameEnhanced `test_disabled` step 5 (fade and holder frames), BankLedger `test_disabled`'s
`__shownFrames`, LootHistory's `shownNames`, and the AbsorbTracker suites its planner lists
(`test_disabled`, `test_display`, `test_draghandle`, `test_helpers`, `test_launcher`, `test_optionssetup`,
`test_perf`, `test_perfcmds`, `test_widgets`). KickCD owns its `CreateFrame` and PanelMaster's local
`wow_mock.lua` already starts frames shown, so neither is expected to redden.

**Consumer follow-ups:** PartyFrameEnhanced PF-06 (hide `PartyFrameEnhanced_Fade_*` and `*_Holder` on
stand-down, `PartyFrameEnhanced-A-01`, and keep the direct step-5 `IsShown()` assertions; PF-06 is
Milestone 3 and follows RV-PF). The Milestone 2 pre-RV items that absorb any other red: AuraMaster
AM-01, BankLedger BL-01, ConsumableMaster CM-01, KickCD KC-01, WhatGroup WG-01. PanelMaster PM-01 and
WhatGroup WG-02 are Milestone 3 and pick up what their re-vendors leave. Any red at RV-WG is listed in
that commit's body, and WG-02 clears it in Milestone 3.

**Depends on:** LK-04. **Effort:** M.

---

## LK-06 · `test_eol` catches a lone CR in any scanned text file

**Resolves:** `AuraMaster-A-18` (Low, dispositioned here). Cluster C37.

**Change.** `testkit/test_eol.lua` `terminators()` (:175-185) also counts lone CRs (byte 13 not
followed by 10) in every path the gate already scans (text attribute not unset, no NUL byte) and fails
with `path:line`. It must **not** key on the index's `-text` classification, which would redden
auto-detected binaries such as PanelMaster's `tools/artwork/bin/realesrgan-ncnn-vulkan` (see the comment
at :199). Dry-run over all eleven, as LK-05.

**Ripple.** Kit 26 doc. New fixture cases in `tests/test_kit_eol.lua`. Implements WS-07 point 7.

**Blast radius.** All eleven run `test_eol`. One known red.

**Consumer follow-ups:** AuraMaster AM-01 removes the lone CR at `tests/page_helpers.lua:80` **before**
RV-AM. On 2026-09-23 it was the only one in that repo (the `.gz` files are `text: unset`).
PartyFrameEnhanced's planner found no lone CR in its tree.

**Depends on:** LK-01, **WS-07**. **Effort:** S.

---

## LK-07 · Prose gate: scan store-root README/RESULTS files, skip `docs/superpowers/` and `docs/investigations/`, and publish `synchronis`

**Resolves:** `ConsumableMaster-A-05`, `KICKCD-A-06` (both Low, dispositioned here),
`PanelMaster-A-09` (Low; PM-17 restores the respelled specs). Cluster C12.

**Change.** `testkit/prose_lists.lua`: `SKIPPED_DIRS` gains `docs/superpowers/` and
`docs/investigations/` (frozen stores under `documentation-§3`). A new named list `SCAN_BACK` names
`docs/automated-tests/README.md`, `docs/automated-tests/RESULTS.md` and `docs/perf-analysis/README.md`,
file by file with no pattern (`localization-§5`). `BRITISH` gains `synchronis`; `PUBLISHED_BRITISH` is
92. The walker in `testkit/test_prose.lua` honors `SCAN_BACK`. LibKa0s's own `tests/test_prose.lua`
(register row 3) applies the same scan-back to this repo, and any hit is fixed in this commit.

**Ripple.** Kit 26 doc. New `tests/test_kit_prose.lua` over a temp fixture tree.

**Blast radius.** All eleven run the gate. Expected reds: ConsumableMaster and KickCD
`docs/perf-analysis/README.md` (`analysed`, `neighbours`) and ConsumableMaster
`docs/settings-panel.md:80` (`synchronisation`). Planners' spot checks found no hit in the store roots of
AbsorbTracker, AuraMaster, LootHistory, MultiMeters, PartyFrameEnhanced or PrettyChat.

**Consumer follow-ups:** ConsumableMaster CM-01 and KickCD KC-01 **before** their re-vendors.
PanelMaster PM-17 **after** RV-PM: restore line 5 of the two `docs/superpowers/specs/` files from
`git show e30e329^:<path>` (`catalogued`, respelled to the non-word `catalogd`). The now-skipped
directory keeps the gate green.

**Depends on:** LK-01, **WS-07**. **Effort:** M.

---

## LK-08 · Kit citations carry the section sign; the ASCII gate scopes to the shipped `LibKa0s/` payload

**Resolves:** `AbsorbTracker-A-17` (Low; AT-21 fixes the addon's own citations), `WHATGROUP-A-13` (Low;
WG-21/WG-DOCS regenerate). Cluster C20.

**Change.** The ASCII gate in LibKa0s `tests/test_prose.lua` (:405) scans only `LibKa0s/`. Kit strings
print to a terminal, and `tests/_kit` never ships (every `.pkgmeta` ignores `tests`). Rewrite the comment
block (:271-310) and register row 3's text. Respell every kit string literal and case name that cites a
section: `localization-5` → `localization-§5`, `line-endings-N` → `line-endings-§N`, `layout-1` →
`layout-§1`, `testing-9/12` → `testing-§9/§12`, in `test_prose.lua`, `test_eol.lua` (e.g. :529-630),
`test_layout_cap.lua`, `framework.lua` (`KIT_GATE_RULE` :799-803 and its comment) and `asserts.lua`.
`normRule` is unchanged and still matches both spellings in register cells.

**Ripple.** Kit 26 doc: **case names change**. Two red-first cases.

**Blast radius.** All eleven: every consumer's `docs/test-cases.md` and README Tests badge must be
regenerated after its re-vendor, or the inventory diff stays red.

**Consumer follow-ups:** the `RV-<AB>` commit is copy-only and lists the inventory red in its body; the
addon's next item regenerates `docs/test-cases.md` and the badge, at the latest `<AB>-DOCS`. AbsorbTracker
AT-21 and WhatGroup WG-21/WG-DOCS fix the addon-side citations.

**Depends on:** LK-07. **Effort:** S.

---

## LK-09 · Runner: headed watch-list tables when empty, and the `performance-§12` exemption as perf skip reason (2)

**Resolves:** `LibKa0s-A-09` (Low), and three routed findings that each still need a fresh run in the
addon: `BankLedger-A-04`, `LootHistory-A-12`, `PRETTYCHAT-A-15` (all Low). Clusters C13, C14.

**Change.** `testkit/run-automated-tests.sh`. (1) `fn_table` (:713-728) and `band_table` (:730-) print
the header row and separator unconditionally; the `printf 'None.'; return` exits are deleted. (2) Perf
skip (:343-344): before reason (1), read the `## Documented deviations` table in `docs/ARCHITECTURE.md`
(addon) or root `CLAUDE.md` (library) with `deviationRows`' parsing. A rule cell matching
`performance-§?12` sets `NOTE[perf]` to the reason-(2) text, which the manifest's `skipReason` and
`md_perf_section` (:833-848) carry. An unparseable register exits 2. `KA0S_PERF_EXEMPT=1` counts only
when no register exists. Keep the `+x` bit on the synced copy.

**Recommended tightening.** Match the rule cell **exactly** (after `normRule`), not as a substring.
WhatGroup's row is keyed `performance-§12 (the exemption is not claimed)` (`docs/ARCHITECTURE.md:502`).
WhatGroup ships `tests/perf.lua`, so the skip branch is never reached there today. But a substring match
would record an exemption the addon explicitly disclaims on the day that file goes.

**Ripple.** Kit 26 doc and `testkit/README.md` runner section. New `tests/test_kit_runner.lua` drives the
script over fixture repos (reason 2, reason 1, malformed register exits 2, and a headed empty table,
skipped when lizard is absent).

**Blast radius.** Every consumer's next automated-test bundle. **Reason (2) applies to three addons
only:** BankLedger (`docs/ARCHITECTURE.md:501`), LootHistory (`:485`) and PrettyChat (`:269`). All three
have no `tests/perf.lua` and a `performance-§12` row. The two other follow-ups filed against LK-09 do not
apply as worded. PanelMaster has no `tests/perf.lua`, but its row is `performance-§1` and says "§12 does
not apply", so reason (1) is correct and PM-DOCS must not re-label it. WhatGroup ships `tests/perf.lua`,
so perf runs, and WG-DOCS verifies that instead.

**Consumer follow-ups:** BankLedger BL-DOCS, LootHistory LH-DOCS, PrettyChat PC-23 and PC-DOCS (PC-23
also fixes `docs/testing.md`'s release-notes wording, `PRETTYCHAT-A-16`). PanelMaster PM-DOCS and
WhatGroup WG-DOCS record what the runner writes (reason (1) and a perf pass).

**Depends on:** LK-01. **Effort:** M.

---

## LK-10 · Core minor 8: `printer.Format` survives a secret value in a numeric specifier

**Resolves:** `LibKa0s-R-08` (Low). Cluster C38.

**Change.** `LibKa0s/Core.lua:455-460`:
`local ok, out = pcall(string.format, SafeToString(fmt), unpack(parts))`. On failure, emit `fmt` and the
stringified parts joined with single spaces, the fallback `DebugLog.lua:640-658` already uses.

**Ripple.** **Core `MINOR` 7 → 8.** `docs/api/Core/version-8-docs.md` (from version-7; Supersedes 7;
Since 8), version-7 Superseded, README row, `members-8.json`, changelog versions line. Red-first case in
`tests/test_core.lua`. Smoke S-007 (a Midnight dungeon with debug on).

**Blast radius.** All eleven addons print through Core's printer (`core/CoreSetup.lua`). It is
runtime-only: a chat line that raised now prints. No surface change.

**Consumer follow-ups:** none required. LootHistory LH-25 (chat lines hand their values to the printer's
`Format` instead of pre-formatting) benefits from it.

**Depends on:** LK-02. **Effort:** S.

---

## LK-11 · Core: `SafeRegisterEvent` / `SafeRegisterUnitEvent` / `SafeRegisterEvents`, the collection's pcalled registration helper

**Resolves:** `AuraMaster-R-05` (Low; AM-07 is the host half). Cluster C03. The recurrence is the reason
for a shared surface: bare event registration was found in **all eleven** addons.

**Change.** `LibKa0s/Core.lua`, still minor 8 (no second bump). Three lib-level members.
`lib.SafeRegisterEvent(target, event, handler, rejected) -> boolean`: if `C_EventUtils.IsEventValid`
exists and answers false, the name is rejected with no call; otherwise
`pcall(target.RegisterEvent, target, event, handler)`, which works for an AceEvent-embedded object and a
Frame. `lib.SafeRegisterUnitEvent(frame, event, rejected, unit1, unit2) -> boolean` does the same through
`RegisterUnitEvent`. `lib.SafeRegisterEvents(target, events, handler, rejected) -> number`. `rejected` is
a caller-owned array, appended once per name. The library keeps no state and prints nothing. A
Bus-stamped target still records the registration, because the call goes through `target:RegisterEvent`.
Each function stays at CCN 10 or below.

**Ripple.** Extends `Core/version-8-docs.md` (three members, Since 8, and a **Degradation** note: a
host's Core stub carries one-rung pcall bodies with no front gate). Regenerate `members-8.json`.
Red-first cases in `tests/test_core.lua` using LK-04's `__badEvents` and `C_EventUtils`.

**Blast radius.** **Surface-parity churn in all eleven.** `Kit.assertSurfaceParity` is one-directional:
the stub must carry every live member. After the re-vendor, any addon whose parity case enumerates the
live Core surface goes red until its Core stub gains the three bodies. Adding them before the re-vendor
would be harmless on v1.55.0, but each addon's LK-11 adoption item is Milestone 3 and follows `RV-<AB>`,
so a parity red at the re-vendor is recorded in that commit's body and closed by the adoption item. This
is the rule for every `RV-<AB>`: the commit is copy-only and is green or lists its reds in its body; the
addon's M2 pre-fixes aim to make it green, its M3 items clear any remaining red, and the addon is green
again at the latest by `<AB>-DOCS`. PrettyChat
projects the Core surface by name (`coreSurface`), so its Core case stays green until PC-01 adds the
names. Core parity tests exist in `tests/test_surface_parity.lua` in BankLedger, ConsumableMaster,
KickCD and PrettyChat, and in `tests/test_libka0s.lua`/`test_coresetup.lua`-style suites elsewhere.

**Consumer follow-ups (route every registration through the helper, and keep a host-owned rejected
list):** AbsorbTracker AT-07 (7 registrations; `/at debug`), AuraMaster AM-07, BankLedger BL-06 (replaces
its local pcall helper; the five bypassing sites), ConsumableMaster CM-15, KickCD KC-04, LootHistory
LH-17, MultiMeters MM-07, PanelMaster PM-08, PartyFrameEnhanced PF-10, PrettyChat PC-01 (stub bodies)
and PC-12 (the `Override.lua` loop), WhatGroup WG-06.

**Depends on:** LK-10, LK-04, **WS-04**. **Effort:** M.

---

## LK-12 · Item minor 2: `QualityFromLink` reads the 11.1.5+ `|cnIQ<n>` link color, and the quality map is cached only when non-empty

**Resolves:** `LibKa0s-R-01` (**High**, the milestone's only High: the library cannot parse the current
item-link color, and its tests pin the retired `|cff` format), `LibKa0s-R-13` (Low). Cluster C38.

**Change.** `LibKa0s/Item.lua:85`, ahead of the hex rung:
`local q = link:match("|cnIQ(%d+)"); if q then return tonumber(q) end`. The hex rung stays for stored
legacy links. `buildQualityByHex` (:63-71) builds into a local and assigns `qualityByHex` only when an
entry landed, so an empty early build is retried. `LoadItem`'s fixed 0.4 s timer (:124) is deliberately
unchanged; the version-2 doc says why.

**Ripple.** **Item `MINOR` 1 → 2.** `Item/version-2-docs.md`, version-1 Superseded, README row,
`members-2.json`, changelog. Red-first cases in `tests/test_item.lua` (`|cnIQ4:` → 4, `|cnIQ0` → 0,
empty-then-populated map). Smoke S-001.

**Blast radius.** The three Item consumers: BankLedger, ConsumableMaster and LootHistory
(`core/ItemSetup.lua`). For LootHistory and BankLedger this is a player-visible fix: uncached epics
record their quality.

**Consumer follow-ups:** LootHistory LH-21 (`tests/test_itemsetup.lua:14` `EPIC_LINK` moves to the
`|cnIQ4:` shape, one legacy `|cff` case kept), BankLedger BL-DOCS (in-client smoke). ConsumableMaster
has no item; it benefits without change.

**Depends on:** LK-02. **Effort:** S.

---

## LK-13 · Media minor 4: register JetBrains Mono with a western+ruRU langmask and count only what LSM accepted

**Resolves:** `LibKa0s-R-04` (Medium). Cluster C32.

**Change.** `LibKa0s/Media.lua:274-275`:
`LSM:Register("font", name, path, LSM.LOCALE_BIT_western + LSM.LOCALE_BIT_ruRU)` when those constants
exist, plain `Register` otherwise. Count a font or statusbar only if `LSM:IsValid(type, name)` answers
true afterwards. Rewrite the comment at :251-258: first registration wins, every consumer's path names
identical bytes, CJK clients are excluded because the face has no CJK glyphs.

**Recommended tightening.** Test `type(LSM.LOCALE_BIT_western) == "number"` (and the same for ruRU),
not mere existence. KickCD's LSM fake answers a **function** for `LOCALE_BIT_western`, so the sum as
written raises in KickCD's suite. KC-01 fixes the fake, but a type check also keeps a non-conforming
third-party LSM copy from raising in the client.

**Ripple.** **Media `MINOR` 3 → 4.** `Media/version-4-docs.md`, version-3 Superseded, README row,
`members-4.json`, changelog. Red-first cases with a fake non-western LSM. Smoke S-004 (ruRU and enUS).

**Blast radius.** All eleven call `RegisterLSM` through `core/MediaSetup.lua`. The first registration
wins in a session, so the fix reaches a ruRU player as soon as any one re-vendored addon loads first.

**Consumer follow-ups:** KickCD KC-01 (fix the LSM fake's locale bits before RV-KC).

**Depends on:** LK-02. **Effort:** S.

---

## LK-14 · Bus minor 2: re-stamp tracking wrappers a newer AceEvent re-embed overwrote

**Resolves:** `LibKa0s-R-05` (Low). Cluster C38.

**Change.** `LibKa0s/Bus.lua:152-196`: keep `rec.wrap[kind]`. `restamp(rec)`: for each of the six
members, if `target[member] ~= rec.wrap[member]`, adopt the new raw member into `rec.raw[member]` and
re-assign the wrapper. A weak-keyed `created` list beside `held` is restamped at the top of `StandDown`
and `StandUp`. `isDown`'s debug seam returns a trailing restamped count. The docstring states the
residual window: registrations made between a re-embed and the next edge are untracked until that edge.
No Ace3 fork and no metatable proxy. `lib.Catalog` (:295) is already at CCN 15 and must not grow.

**Ripple.** **Bus `MINOR` 1 → 2.** `Bus/version-2-docs.md`, version-1 Superseded, README row,
`members-2.json`, changelog. Red-first case in `tests/test_bus.lua`. Smoke S-005.

**Blast radius.** The eight Bus hosts (AT, AM, BL, CM, KC, LH, MM, PF). Runtime-only: registrations
made through an overwritten wrapper now stand down.

**Consumer follow-ups:** none.

**Depends on:** LK-02. **Effort:** M.

---

## LK-15 · Lifecycle minor 2: document and pin the nested-edge (re-entrancy) behavior

**Resolves:** `LibKa0s-R-17` (Low). Cluster C38.

**Change.** `LibKa0s/Lifecycle.lua` `New` docstring (:75-89): a `standDown`/`standUp` callback **MUST
NOT** take or release a hold. If it does, `edge()` re-enters synchronously and the nested edge runs inside
the outer one; the latch stays consistent but host teardown interleaves. The code is unchanged.

**Ripple.** **Lifecycle `MINOR` 1 → 2**, because a comment still changes the file's bytes.
`Lifecycle/version-2-docs.md` gains a *Re-entrancy* section; version-1 Superseded; README row;
`members-2.json`; changelog. One characterization case in `tests/test_lifecycle.lua`, green on first run
by design.

**Blast radius.** All eleven carry the new bytes. No behavior change.

**Consumer follow-ups:** none.

**Depends on:** LK-02. **Effort:** S.

---

## LK-16 · Launcher minor 2: an `isEnabled`/`disabledLine` gate for a rung (a)/(b) left click, and missing-library notices printed once, untagged

**Resolves:** `LibKa0s-R-06`, `LibKa0s-R-09` (both Low). Cluster C08. The recurrence: three hosts
hand-write the rung (a)/(b) refusal differently.

**Change.** `LibKa0s/Launcher.lua`. The descriptor (:98-127) gains optional `isEnabled` and
`disabledLine`. In `click()` (:178-185), a left click with `onClick` present and `isEnabled()` false
emits `disabledLine()` and returns without calling `onClick`. Rung (c) is still expressed by omitting
`onClick`, and right-click is unchanged. `NO_BROKER`/`NO_ICON`/`NO_MINIMAP` (:203, :228, :235) print
once per instance. The `[LibKa0s] ` prefix is dropped from `lib.STRINGS` values (:70-75), because the
host printer tags them. Keys are unchanged, so locale overrides still work.

**Ripple.** **Launcher `MINOR` 1 → 2.** `Launcher/version-2-docs.md` (fields Since 2), version-1
Superseded, README row, `members-2.json`, changelog. Red-first cases in `tests/test_launcher.lua`. Smoke
S-006.

**Blast radius.** All eleven register a launcher (`core/LauncherSetup.lua`). The string change is
visible to any consumer test that asserts the `[LibKa0s]` prefix; PanelMaster's planner found none there,
and the dry-run will show the rest. The gate is opt-in.

**Consumer follow-ups (adopt the gate and delete the hand-written one):** AbsorbTracker AT-10
(`core/LauncherSetup.lua:160-161`), AuraMaster AM-09 (:119-120), BankLedger BL-08 (:156),
ConsumableMaster CM-09, LootHistory LH-11, MultiMeters MM-02 (`isEnabled` latch-inclusive through
`NS.IsStoodDown`, so a perf suspend also refuses; replaces :229-237). **Not planned:** KickCD and
PartyFrameEnhanced. Their planners left adoption to the re-vendor candidate interview, because each
already gates the left click itself.

**Depends on:** LK-02. **Effort:** S.

---

## LK-17 · Slash minor 15: `CliSet`/`CliReset` print the write seam's refusal instead of echoing the unchanged value

**Resolves:** `LibKa0s-R-03` (Medium). Cluster C10.

**Change.** `LibKa0s/Slash.lua` `CliSet` (:669-695, the call at :688):
`local ok, err, why = d.set(row.path, v)`. When `ok == false`, print `INVALID` for the path, then `err`
and `why` indented, and return. Otherwise echo as today; `nil` or `true` still means success. `CliReset`
(:696-, the call at :703): when `applyDefault` answers exactly `false`, print the new
`lib.STRINGS.NO_DEFAULT` (`%s has no default to restore`). The descriptor's `set` is documented as
possibly answering `false, reason[, why]`.

**Ripple.** **Slash `MINOR` 14 → 15.** `Slash/version-15-docs.md`, version-14 Superseded, README row,
`members-15.json`, changelog. New `tests/test_slash_refusal.lua` (`test_slash.lua` is 1327 lines). Smoke
S-003.

**Blast radius.** All eleven dispatch through Slash. Behavior changes only where the descriptor's `set`
returns `false`. **BankLedger** passes `Schema.Set` straight through, so `/bl set` starts printing
refusals and any test asserting the old echo goes red. **MultiMeters** discards the seam's return
(`settings/Slash.lua:295, :301`). **AuraMaster** prints its own refusal in the wrapper
(`settings/Slash.lua:467-471`): if that wrapper also starts returning `false`, the player sees two
refusals, so AM-11 drops the host print in the same commit. AbsorbTracker needs nothing (no row carries
`validate`).

**Consumer follow-ups:** AuraMaster AM-11, BankLedger BL-09, MultiMeters MM-09, LootHistory LH-14,
PrettyChat PC-02 (pins `CliSet`), ConsumableMaster CM-17 (through its Schema adoption).

**Depends on:** LK-02. **Effort:** S.

---

## LK-18 · Degraded Slash stub contract: `Kit.assertLibraryConstant` and the Slash doc's prescribed stub shape

**Resolves:** `PartyFrameEnhanced-R-11` (Low; PF-12 is the addon half). Cluster C08. The recurrence:
degraded refusal-line drift in five addons. Owner-scope issue WhatGroup#22.

**Change.** `testkit/asserts.lua` gains `Kit.assertLibraryConstant(value, majorName, memberPath, msg)`:
resolve the live library through the source `Kit.setSurfaceSource` registered, read `memberPath` (e.g.
`DISABLED_LINE_FORMAT`), assert byte equality, name both strings on failure.
`docs/api/Slash/version-15-docs.md` gains **The degradation stub**: minimal `OnSlash` dispatch;
`DisabledLine` built from the verbatim `DISABLED_LINE_FORMAT` bytes and pinned with the new assertion;
help rows printed `cmd  desc` with no `FormatRow` copy; composed-row verbs either write through
`writeThrough` or print `%s is unavailable: the LibKa0s library did not load.`, never raising.
`Slash.lua` does not change.

**Required amendment before implementation: the resolver.** AbsorbTracker's `tests/run.lua:55` registers
the Slash **instance** (`NS.Slash.__cli`) as the `LibKa0s-Slash-1.0` surface source, and WhatGroup's
`tests/run.lua` does the same. `DISABLED_LINE_FORMAT` is **lib-level** (`libs/LibKa0s/Slash.lua:83`), not
an instance member. As specified, the assertion would fail to find the member in at least those two
addons, and AT-09 and WG-13 could not be written as prescribed. `assertLibraryConstant` must fall back
to `LibStub(majorName)` when `memberPath` is absent on the registered source, and a case in
`tests/test_kit_asserts.lua` must pin that fallback.

**Ripple.** Kit 26 doc (member, Since 26). Slash 15 doc extended (no second bump). Three red-first cases,
plus the fallback case above. Implements WS-02's Slash half.

**Blast radius.** All eleven have a library-absent Slash stub, and every one is asked to pin its line.

**Consumer follow-ups:** AbsorbTracker AT-09, AuraMaster AM-16 (`settings/Slash.lua:388-391`),
BankLedger BL-10 (hoists the literal to `Sl.__DISABLED_LINE_FORMAT`), ConsumableMaster CM-18 (no
disabled state in the degraded build, so it pins the library-absent line and the live format),
KickCD KC-19, LootHistory LH-16 (the launcher tooltip derives from `NS.Slash.DisabledLine`, LH-11),
MultiMeters MM-02 (publishes `Sl:DisabledLine` only if `cli.DisabledLine` exists), PanelMaster PM-09,
PartyFrameEnhanced PF-12 (drop the copied em-dash `FormatRow`, correct the false comment at
`settings/Slash.lua:322-324`), PrettyChat PC-02 (`STUB_DISABLED_LINE_FORMAT`), WhatGroup WG-13 (the
launcher fallback returns the stub's line instead of a re-spelled literal).

**Depends on:** LK-17, **WS-02**. **Effort:** S.

---

## LK-19 · DebugLog minor 13: batched buffer trim instead of `table.remove(1)` per line at the cap

**Resolves:** `LibKa0s-R-10` (Low). Cluster C35.

**Change.** `LibKa0s/DebugLog.lua:623`. `D.buffer` stays a public ordered array, because
`tests/test_debuglog.lua:87-142` and the AbsorbTracker and BankLedger tests index it. Once `#D.buffer`
exceeds `MAX_BUFFER + 64`, compact by moving the newest `MAX_BUFFER` lines down in one pass.
`BufferSize`/`LastLine`/`FindLine`/`CopyText` read only the newest `MAX_BUFFER` lines. `MAX_BUFFER` stays
1500, which WS-07 makes the standard's number.

**Ripple.** **DebugLog `MINOR` 12 → 13.** `DebugLog/version-13-docs.md` states the 64-line slack (the
raw array may briefly hold 1564 entries while every public reader answers 1500); version-12 Superseded;
README row; `members-13.json`; changelog. Characterization first (1499/1500/1501/1600 lines), then a red
case (1564 adds cost at most one compaction). Smoke S-008.

**Blast radius.** All eleven. Only a consumer test that reads `#D.buffer` directly past the cap could see
the slack. AbsorbTracker and BankLedger index the buffer; the dry-run will show whether either reads its
length past 1500.

**Consumer follow-ups:** none.

**Depends on:** LK-02, WS-07. **Effort:** S.

---

## LK-20 · Perf minor 13: `armed`/`recording`/`label` stay raw fields (false, never nil), and `openDepth` resets at window edges

**Resolves:** `LibKa0s-R-11`, `LibKa0s-R-16` (both Low). Cluster C35.

**Change.** `LibKa0s/Perf.lua`: initialize `P.armed`, `P.recording`, `P.label` to `false` (:400-405) and
rewrite the :400-401 comment (the metatable exists only for `suspended`). Every later nil write becomes
`false` (:911, :921, :959, :1011, :1033, :1044), after auditing `== nil` reads in `Perf.lua` and
`PerfPanel.lua`. `openWindow` (:909) and `closeWindow` (:919) reset `openDepth = 0`.

**Ripple.** **Perf `MINOR` 12 → 13**, PerfPanel stays 5, key **13.5**. `Perf/version-13.5-docs.md`,
version-12.5 Superseded, README row, `members-13.5.json`, changelog. Red-first cases in
`tests/test_perf_core.lua` and `tests/test_perf_isolation.lua`.

**Blast radius.** The six Perf hosts (AT, AM, CM, KC, MM, PF). A leaked `Open` no longer misattributes
parents in the next window. Consumers that read `P.recording == nil` would change meaning; none was found
by the planners.

**Consumer follow-ups:** none.

**Depends on:** LK-02. **Effort:** S.

---

## LK-21 · Widgets minor 10: `ReorderList` polls on its own ghost frame and draws its drop line from a library pool

**Resolves:** `LibKa0s-R-12` (Low). Cluster C38.

**Change.** `LibKa0s/Widgets.lua`: the drag poll moves from `row.frame:SetScript("OnUpdate")` (:999,
cleared at :915 and :1080) to the library-owned ghost frame, so a host row frame's `OnUpdate` is never
touched. The drop line (:739-753, today cached on the AceGUI-pooled container as `__ka0sDropLine`) comes
from a library pool (LibKa0s-Pool-1.0, or a module-local free list if Widgets does not floor on Pool),
acquired per drag, recolored per list, released on cancel or drop. This restores the file's own
pooled-frame invariant at :783-795.

**Ripple.** **Widgets `MINOR` 9 → 10**, DragHandle stays 2, key **10.2**. `Widgets/version-10.2-docs.md`,
version-9.2 Superseded, README row, `members-10.2.json`, changelog. New `tests/test_widgets_reorder.lua`
(`test_widgets.lua` is 1493 lines).

**Blast radius.** The four `ReorderList` callers: ConsumableMaster, KickCD, LootHistory and MultiMeters
(sites in the consumer table above). The behavior change is visible only in the client, so each needs an
in-client drag smoke.

**Consumer follow-ups (smoke only, no code):** ConsumableMaster CM-29 (all three sites, including
`StatPriority.lua:122` and `MacroBar.lua:723`), KickCD KC-12 (`settings/Spells.lua` ~:1001), MultiMeters
MM-18 (`settings/ColumnBlocks.lua`; runs and is recorded in `docs/smoke-tests.md §5` even if MM-18's
RenderTabbedSchema adoption is declined). **Gap:** LootHistory's reorder list (`settings/Panel.lua:674`,
through `NS.MakeReorderList`) has no follow-up and no smoke step in any LootHistory item. Add the drag
check to LH-DOCS's smoke or to LootHistory's `docs/smoke-tests.md` at RV-LH.

**Depends on:** LK-02. **Effort:** M.

---

## LK-22 · Schema minor 2: `instanceId` forwarding, `row.normalize`, and `SetMany` (all-or-nothing batch, one bracket line, one announce)

**Resolves:** `LibKa0s-R-14` (Low). Cluster C38. **Owner-scope issues:** ConsumableMaster#39,
MultiMeters#52, KickCD#22, AuraMaster#21.

**Change.** `LibKa0s/Schema.lua`. (1) `S.Get` calls `row.get(instanceId)` (:358), and
`S.ApplyDefault(row, instanceId)` forwards the id to `S.Set` (:497-502). (2) `row.normalize(value, rid)`
runs after validate and before store. It answers the value to store, or `nil, why`, which refuses with
`INVALID`. It has two consumers (AuraMaster and ConsumableMaster), which clears `library-stack-§7` bar 2.
(3) `S.SetMany(entries, opts)`. Phase 1 resolves, validates and normalizes every entry and returns
`false, err, why, index` before any store. Phase 2 stores in order, inside one bracket when `opts.act` is
given (one `[Set] <act> <scope>: N rows` line). Each row's `onChange` runs. Then the descriptor's
optional `announceBatch(writes, rid)` runs once, or `announce` runs per write without it. Returns true.
A shared `prepareWrite` keeps `S.Set` and `SetMany` at CCN 10 or below. The header's "deliberately does
not do" paragraph is updated.

**Ripple.** **Schema `MINOR` 1 → 2.** `Schema/version-2-docs.md` (Current, Since 2). Its stub table adds
`SetMany` with the same all-or-nothing semantics and log-silence. Its **Adoption notes** gain per-host
mappings: KickCD (`row.section` read by `announce`; SESSION/GLOBAL paths as rows with get/set; the master
switch as the `enabled` row's `onChange`), ConsumableMaster (validate-coerce into `normalize`;
`SetManyAndRefresh` → `SetMany` + `announceBatch`), MultiMeters (`SetByPaths` → `SetMany`), AuraMaster
(partial adoption now possible with `normalize`). Version-1 Superseded, README row, `members-2.json`
(lib-level unchanged). New `tests/test_schema_batch.lua` (`test_schema.lua` is 1233 lines), and
`tests/test_schema.lua`'s `referenceStub` gains `SetMany`, pinned with the two-table parity.

**Blast radius.** **Surface-parity churn in the five current Schema consumers** (AT, BL, LH, PM, PC):
their instance stubs must gain `SetMany`, or their two-table parity case goes red at the re-vendor.
BankLedger's is `tests/test_surface_parity.lua:315-320`. Adding the member before the re-vendor is
harmless on v1.55.0. The six adoption items take the major for the first time.

**Consumer follow-ups.**
- Stub parity, landing before the re-vendor in Milestone 2: AbsorbTracker AT-01, BankLedger BL-02
  (which mirrors LK-22's semantics exactly; the post-RV-BL parity check is against the LK-22 surface).
  Each must pass on both the v1.55.0 payload and the v1.56.0 dry run.
- Stub parity, Milestone 3 after the re-vendor: LootHistory LH-15 (also the `instanceId` forwarding in
  `R.Get`/`R.ApplyDefault`), PanelMaster PM-01, PrettyChat PC-01.
- Adoption: AuraMaster AM-15 (#21: primitives, registry, bulk bracket, Validate; re-evaluates `Set` and
  declines it), ConsumableMaster CM-17 (#39), KickCD KC-18 (#22: no new surface needed beyond the
  adoption note), MultiMeters MM-14 (#52: `SetByPaths` becomes `S:SetMany`, `announceBatch` fires
  `CONFIG_CHANGED` once, and the host primitives, registry and bracket are deleted from
  `settings/Schema_Paths.lua`), WhatGroup WG-12 (#22), PartyFrameEnhanced PF-11 (#14, via LK-23).
- PrettyChat#18 (move `Schema.ResetRows` onto `BulkRun`/`BulkAdd`) needs **no** upstream change and is
  PC-05.

**Depends on:** LK-02. **Effort:** L.

---

## LK-23 · Schema `writeThrough`: a declared path list the live seam and the degraded stub both store without a row

**Resolves:** `AbsorbTracker-A-02`, `AbsorbTracker-A-03` (both Low; AT-08 is the addon half). Cluster
C26. **Owner-scope issues:** PartyFrameEnhanced#14, WhatGroup#22.

**Change.** `LibKa0s/Schema.lua`, still minor 2. The descriptor gains `writeThrough` (an array of paths;
the instance builds a set once). In `S.Set`, when no row is indexed for a path in that set, the value is
stored raw via `writeTarget`/`lib.Write` (a copy), with no validate, normalize or `onChange`. `announce`
is then called with a synthetic row `{ path = path, writeThrough = true }`, built once per path so a
write allocates nothing. It logs like any write and returns true. A path with a row always takes the
row. This also covers a partial load (Schema present, Options absent).

**Ripple.** Extends `Schema/version-2-docs.md`. **The degradation stub** section prescribes that the
runtime-completing stub takes the same list, stores it the same way, and refuses every other row-less
path. This is WS-02 route (a). Adoption notes for AbsorbTracker, PartyFrameEnhanced (#14) and
WhatGroup (#22, route (b), no list). `referenceStub` gains `writeThrough`. Red-first cases in
`tests/test_schema_batch.lua`, against the live instance and the stub.

**Design note consumers must carry.** A written-through value runs no `onChange`. So a degraded
`/<slash> disable` stores `false` but does not move the stand-down latch unless the host reacts to the
synthetic row. AbsorbTracker (AT-08: `announce` dispatches the host's own reaction table,
`NS.MasterReactions`), KickCD (KC-19), LootHistory (LH-16: the degraded `CliSet` calls
`S.OnEnabledWritten`) and AuraMaster (AM-16: `NS.SyncEnabled()` after a successful write) each handle
this themselves. ConsumableMaster declines route (a) for the same reason (CM-18).

**Blast radius.** Opt-in. Nothing changes for a consumer that passes no list.

**Consumer follow-ups:** AbsorbTracker AT-01 (stub) and AT-08 (`{enabled, locked}`; delete
`composeBlock`, `ORDER_STEP` and the five host composer copies at `settings/OptionsSetup.lua:237-377`;
re-pin `tests/test_perf.lua:501` and `tests/test_optionssetup.lua:233-243` as full count, degraded count
and the named composer gap), AuraMaster AM-16, BankLedger BL-10 (`settings.enabled`), KickCD KC-18/KC-19,
LootHistory LH-15/LH-16, MultiMeters MM-15, PanelMaster PM-09, PartyFrameEnhanced PF-11
(#14: `{'enabled','locked'}` covers `settings/Slash.lua` runEnabled :152 and runLock :117 and
`modules/Preview.lua` forceLock :134; done when `tests/test_schema.lua:209` is green), WhatGroup WG-12
(#22: **no** list; `/wg enable`, `/wg disable` and `/wg test on|off` print
`/wg enable is unavailable: the LibKa0s library did not load.` and raise no error; the two
`tests/test_libka0s.lua` characterization cases assert the line and the unchanged store; the
`options-ui-§1` SHOULD deviation row goes in `docs/ARCHITECTURE.md`).

**Depends on:** LK-22, **WS-02**. **Effort:** M.

---

## LK-24 · Options: peel the font preload out of `Options.lua` into `OptionsScroll.lua`

**Resolves:** no finding. It makes room under the cap for LK-25.

**Change.** Move the `-- the font preload (minor 17)` block, `LibKa0s/Options.lua:334-434`
(`preloadState`, `preloadFrame`, `preloadPath`, `subscribeLate`, `lib.__PreloadFonts`), into
`LibKa0s/OptionsScroll.lua` as lib-level code. Both callers (:408 and :620) look up
`lib.__PreloadFonts` at call time, so a partial copy missing OptionsScroll degrades to no preload; make
both call sites nil-guarded. `lib.__PatchLSM30Border` stays. `Options.lua` drops from **1476** to about
1376.

**Ripple.** **Options `MINOR` 23 → 24** and **`SCROLL_MINOR` 3 → 4**. Key `23.30.3.7.3` →
**`24.30.3.7.4`**. The one unreleased Options document is created here; `version-23.30.3.7.3-docs.md`
becomes Superseded. README row, members JSON, changelog. Characterization:
`tests/test_options_fontpreload.lua` passes unchanged with the same case count. One red-first case
(no raise with `lib.__PreloadFonts` nil).

**Blast radius.** All eleven carry the new bytes. No behavior change. Smoke: font previews still render in
their own faces.

**Consumer follow-ups:** none.

**Depends on:** LK-02. **Effort:** S.

---

## LK-25 · Options: `CreateOptionsPanel` parks in combat and replays itself; `OpenOptionsPanel` answers a boolean

**Resolves:** `ConsumableMaster-A-04` (Low; CM-05 is the addon half). Cluster C47.

**Change.** `LibKa0s/Options.lua` `registerMain`/`CreateOptionsPanel` (:1322-1387). Under
`InCombatLockdown()`, park the request and register `PLAYER_REGEN_ENABLED` on a library-private frame
only while something is parked. On that event, replay once and unregister. This runs whatever the host's
stand-down state, which also fixes `ConsumableMaster-R-03`'s lost category. A second call while parked is
a no-op. `OpenOptionsPanel` (:1411-1430) answers `true` when opened, `false` when refused in combat (it
still prints `COMBAT_REFUSED`), and `nil` when no category exists. No new instance member (no
`ReplayPending`), so no host stub moves.

**Ripple.** Options already at 24 (LK-24); the Options doc is extended with park/replay semantics, return
values and the private frame, which LK-30 records in the `events-frames-taint-§1` register row. Red-first
cases in `tests/test_options_combat.lua` (578 lines).

**Blast radius: all eleven, and it is a behavior change the standard does not rule on.** Today every
consumer except ConsumableMaster registers its category at login even in combat, and
`options-ui-§9` says the registration is taint-free and eager (:105, :233-236). After LK-25, a login or
`/reload` taken in combat registers the category only when combat ends. WhatGroup pins the opposite
(`tests/test_panel.lua:100-110`, "registering during combat still registers", the WG-A-12 fix), and those
two cases go red. **Owner decision before LK-25 lands:** either
- **keep the park** and add the `options-ui-§9` sentence recommended under WS-08, so the standard and the
  library agree (WG-02 then re-pins); or
- **narrow LK-25**: keep the boolean return from `OpenOptionsPanel`, but make `CreateOptionsPanel`
  register immediately. ConsumableMaster (CM-05) then deletes its own park instead of delegating to one,
  which also removes `ConsumableMaster-R-03`'s failure mode.

The plan as written takes the first option. The private frame is a third widget-owned private event
site in the library (LK-30).

**Consumer follow-ups:** ConsumableMaster CM-05 (adopt: `KCM.Options.Open` → `UI.OpenOptionsPanel`,
`registerPanel` → `UI.CreateOptionsPanel`; delete `expandMainCategory`, `KCM._settingsCategoryID` and the
host park at `settings/OptionsShim.lua:192-236` and `Panel.lua:1253-1286`), WhatGroup WG-02 (forced
re-pin in Milestone 3; a red at RV-WG is listed in that commit's body and WG-02 clears it). Smoke: CM §6a, enabled and disabled.

**Depends on:** LK-24. **Effort:** M.

---

## LK-26 · OptionsWidgets minor 31: the slider and color throttles track their own armed flag, ignoring `scheduleTimer`'s return

**Resolves:** `KICKCD-R-19` (Medium, dispositioned here). Cluster C35.

**Change.** `LibKa0s/OptionsWidgets.lua`: the slider live commit (:1326-1337) and the color throttle
(:1468-1482) each keep a library-local boolean, set before calling `d.scheduleTimer` and cleared in the
callback. Callers stop testing the handle, so a nil-returning `C_Timer.After` wrapper gets the 50 ms
throttle. `LibKa0s/Options.lua:537-542`: the descriptor doc says the return value is unused.

**Ripple.** **`WIDGETS_MINOR` 30 → 31**. Key `24.30.3.7.4` → **`24.31.3.7.4`**; rename the unreleased
Options document. New `tests/test_options_throttle.lua` (`test_options_widgets.lua` is 4086 lines, a
census row).

**Blast radius.** Every consumer with a slider or color picker (all eleven use Options). The fix is
player-visible in the three hosts whose `scheduleTimer` returns nil: KickCD, LootHistory and MultiMeters
(today one commit per frame while dragging). The others are unchanged.

**Consumer follow-ups:** KickCD KC-10 (switch `settings/OptionsSetup.lua:243` to `C_Timer.NewTimer` as
belt and braces), LootHistory LH-14 (restate the contract; `NewTimer` optional), MultiMeters MM-17
(`NewTimer` declined, reason in the comment). Smoke: KickCD color and slider drag at about 20 commits per
second.

**Depends on:** LK-25. **Effort:** S.

---

## LK-27 · OptionsTabs minor 4: `PageBanner`, `PageHeader` and the chrome divider stop leaking a widget per render; the kit's AceGUI fake surveys Create/Release

**Resolves:** `LibKa0s-R-02` (Medium). Cluster C38.

**Change.** `LibKa0s/OptionsTabs.lua`. `PageHeader` (:1117) acquires its frame from a per-ctx pool
(`ctx.__headerPool`, LibKa0s-Pool-1.0, already floored with `NEEDS_POOL`), released in `releaseChrome`.
`drawChromeDivider` (:577) builds its texture once per ctx (`ctx.__ruleTex`) and hides it on release;
`SetParent(nil)` is never called on a Region. `PageBanner` (:1036) keeps `ctx.__bannerWidget` and
`AceGUI:Release`s it at the top of the next `releaseChrome`. `releaseLedger` (:734-741) is updated. Kit:
`testkit/mock_record.lua` gains a per-type AceGUI Create/Release survey (`M.__aceguiLive(type)`), hooked
with two lines in `testkit/mock_base.lua` around :1364.

**Ripple.** **`TABS_MINOR` 3 → 4**. Key → **`24.31.4.7.4`** (final). Kit 26 doc extended. Sync
`tests/_kit`. Red-first cases in `tests/test_options_tabs.lua`, plus a kit self-test.
`mock_record.lua` again: keep the survey out of the two CCN-15 functions. Smoke S-002 (AuraMaster, 50
banner-page switches, memory flat).

**Blast radius.** Every consumer that renders a banner or a page header, which is every consumer that
renders a tabbed page. Direct `PageBanner` callers: AuraMaster, ConsumableMaster (`StatPriority.lua`),
KickCD, MultiMeters (`Windows.lua`). The fix is library-side and reaches all of them with no host change.

**Consumer follow-ups:** AuraMaster AM-17 (via LK-28). No other obligation.

**Depends on:** LK-26, LK-01. **Effort:** M.

---

## LK-28 · `RenderTabbedSchema` moves to `OptionsTabs.lua` and gains host tabs, a disabled notice and a chrome hook; `PageBanner` gains an action button

**Resolves:** `AuraMaster-R-04` (Low; AM-17 is the addon half). Cluster C45. The recurrence: the
tab-strip render is forked in five hosts.

**Change.** Move `O.RenderTabbedSchema` (`LibKa0s/OptionsWidgets.lua:3820-3921` with its doc block) into
`OptionsTabs.lua`'s `__AttachTabs`, and change `Options.lua:1471` to `lib.__AttachTabs(O, d)` so it
reaches `d.rowsForPage`. OptionsWidgets keeps an untabbed fallback (at most 10 lines) that the Tabs
attach overrides, so a partial copy without OptionsTabs still renders. This is a first peel toward
LibKa0s #16 (OptionsWidgets over the cap). A new optional 5th argument `opts`: `tabs` (bespoke non-row
tabs placed `before` a named group), `disabledFor(cfg)` plus `disabledNotice`, and `chrome(ctx)` (after
the strip, before rows). `O.PageBanner` gains an optional `action = { text, tooltip, onClick }` for the
`options-ui-§14` picker+create band. Anti-pattern #55 check: each field serves AuraMaster's seven pages,
and four other hosts hand-build the same strip (AbsorbTracker `settings/UnitPanel.lua:327`, KickCD
`settings/Panel_Render.lua:208`, ConsumableMaster `settings/General.lua:402`, MultiMeters
`settings/Columns.lua:321`).

**The `disabledFor` and `tabs` shape (plan-review correction).** When `disabledFor(cfg)` answers true,
the `disabledNotice` is drawn **above** the rows, and the rows are rendered disabled (`RenderRows`
`opts.disabled`, plus `ctx.__renderDisabled` around a bespoke render). The notice does not replace the
rows. A `tabs` entry whose key equals a schema group takes that group's place in the strip and is handed
the group's rows (`render(ctx, rows)`). The library tests pin both, so AM-17 adopts with no change to
its disabled-state characterization. The item's own test line ("the notice and no rows") predates this
correction and is superseded by it.

**Ripple.** No bump; the Options minors were already bumped by LK-26/LK-27. Options doc extended (fields
Since 31/4). Characterization first: every existing `RenderTabbedSchema` case passes unchanged after the
move. Then red-first cases, including rendering without OptionsTabs, the notice drawn above disabled
rows, and a host tab that replaces a same-named group.

**Blast radius.** **Every current caller** takes the moved function: direct callers exist in AbsorbTracker,
BankLedger, KickCD, MultiMeters (six settings files), PanelMaster, PartyFrameEnhanced, PrettyChat and
WhatGroup. The existing signature is unchanged. Smoke: every tabbed settings page draws its strip, switches
tabs and heals a stale tab as before.

**Consumer follow-ups:** AuraMaster AM-17 (depends on LK-28; adopt: replace `Helpers.RenderTabbedPage`/`collectTabs`/
`settleActiveTab`/`renderActiveTab` at `settings/OptionsSetup.lua:560-659` and `buildContainerHeader`
:480-504). Evaluate-and-adopt-or-decline: AbsorbTracker AT-15, ConsumableMaster CM-20 (adopt on General
and Macro Bar; decline Stat Priority and Macros as list pages), KickCD KC-20, MultiMeters MM-18 (with a
decision gate and a decline-issue fallback).

**Depends on:** LK-27, LK-25. **Effort:** L.

---

## LK-29 · US-English sweep of the authored prose (the roughly 210 British spellings)

**Resolves:** `LibKa0s-A-07` (Low: 210 hits in 33 live authored files). Cluster C12.

**Change.** Re-run the counter at HEAD with the published lists (92/33) over `tests/` (excluding
`tests/_kit`), the **highest-version** `docs/api` documents only, `docs/releasing.md`, `README.md`,
`DEPENDENCIES.md`, `CLAUDE.md` and `tools/artwork/*.py`, and fix prose, comments and test names. Two
exclusions: `.cancelled`/`IsCancelled` member accesses that model AceTimer/C_Timer handles
(`tests/test_mock_ace.lua:237, 415, 443-444, 465`), ratified by extending register row 1 and
`tests/test_prose.lua`'s `RATIFIED`; and `tests/test_prose.lua`'s own quoted fixtures. Released
CHANGELOG entries and Superseded documents are not touched. Register row 3's figures in `CLAUDE.md` go
to 0 prose hits.

**Ripple.** The red-first test is the scope widening itself: LibKa0s's `tests/test_prose.lua` British
gate extended to `tests/*.lua` and the live docs, red on today's tree, then swept green. Test names change
here, so `docs/test-cases.md` regenerates.

**Blast radius.** LibKa0s only. `tests/` is not vendored.

**Consumer follow-ups:** none.

**Depends on:** LK-28, LK-07. **Effort:** M.

---

## LK-30 · Root `CLAUDE.md`: figures pointed at their generated sources, a register row for widget-owned private event frames, and a traceable row-1 citation

**Resolves:** `LibKa0s-A-08` (Low), `LibKa0s-A-10` (Info), `LibKa0s-A-12` (Info). Clusters C03, C18, C21.

**Change.** (a) The hand count "eighty files" (:268-269) and its copies at `docs/releasing.md:19` and
`DEPENDENCIES.md:124` become a pointer to `RESULTS.md`'s generated lint sentence. (b) Re-run `wc -l` for
every band figure (:185-218), including every file this milestone moved (`Options.lua`, `OptionsTabs.lua`,
`OptionsWidgets.lua`, `test_prose.lua`, `framework.lua`, `tests/test_schema.lua`). (c) :180 cites
`lib.__tabsMinor`/`lib.__tabsShellMinor` by symbol, not `:39`. (d) A Documented deviations row keyed
`events-frames-taint-§1` for the widget-owned private frames: OptionsTabs combat-lock
(`PLAYER_REGEN_DISABLED/ENABLED`, :102-103/:139-140), Widgets popup dismiss (`GLOBAL_MOUSE_DOWN`, :393) and
the Options park frame from LK-25. The reason is that these carry one widget's UI state on stable core
events, not "the library cannot use AceEvent". Re-check trigger: an event newer than the current
expansion, or a fourth private site. (e) Row 1 evidence cites commit `1f1790c`, recorded in
`docs/api/testkit/version-17-docs.md`.

**Ripple.** Docs only. The kit's register parser (`deviationRows`) still reads the table, so the suite
runs.

**Blast radius.** LibKa0s only. If the owner narrows LK-25, the register row names two sites, not three.

**Consumer follow-ups:** none.

**Depends on:** LK-29. **Effort:** S.

---

## LK-31 · `docs/releasing.md` step 7: a manifest precondition, an `ANALYSIS.md` sub-step, and a release-notes perf-skip line

**Resolves:** `LibKa0s-A-01`, `LibKa0s-A-05`, `LibKa0s-A-06` (all Low). Clusters C13, C14.

**Change.** `docs/releasing.md` step 7 (:85-160). (1) A hard precondition:
`grep -l '"release": "<X.Y.Z>"' docs/automated-tests/*/manifest.json` prints at least one path, and the
stamp being tagged is one of them. Re-runs are normal, so exactly-one is not required. (2) A numbered
sub-step writes `<stamp>/ANALYSIS.md` per the `AUTOMATED_TESTS.md` prompt, in the bundle commit before
the tag, and `test -f` joins the precondition block. (3) A release-notes line filled from the manifest,
ending "perf SKIPPED, not measured: no tests/perf.lua, so the gate covered three suites, not four."
Forward only: no released entry and no frozen bundle is edited.

**Ripple.** Docs only. LK-33 exercises all three steps.

**Blast radius.** LibKa0s only.

**Consumer follow-ups:** none.

**Depends on:** LK-30. **Effort:** S.

---

## LK-32 · Watch-list terminal states: file the owed issues and re-rule the band files

**Resolves:** `LibKa0s-A-03` (Low). Cluster C14.

**Change.** File LibKa0s issues with
`gh issue create -R tusharsaxena/LibKa0s --label state:triaged --label severity:low`, **at least 5 s
apart**: `tests/test_options.lua` (peel the render/refresh block), `LibKa0s/Widgets.lua` (per-widget
files), `tests/test_widgets.lua` (split by widget family), `tests/test_schema.lua` (split by pipeline
stage), and `testkit/test_prose.lua` only if still in the 1000-1500 band after LK-01/LK-07. Record each
issue number in `CLAUDE.md`'s census, plus a written re-rule for `LibKa0s/Options.lua` (about 1416 after
LK-24/LK-25: accepted, re-check at the next member or 1450 lines) and `LibKa0s/OptionsTabs.lua` (measured
after LK-28: accepted, re-check at 1450).

**Ripple.** Issue store and `CLAUDE.md`. The `RESULTS.md` Disposition cells are written in LK-33, after
the release run regenerates the table.

**Blast radius.** LibKa0s only. **This is the only item in Milestone 1 that writes GitHub issues before the
owner's merge approval.** Issues are not code and merge nothing, so this does not break the no-merge rule,
but the writes must be spaced.

**Consumer follow-ups:** none.

**Depends on:** LK-31. **Effort:** S.

---

## LK-33 · Cut v1.56.0: version block, release run with `ANALYSIS.md` and dispositions, and a LOCAL tag

**Resolves:** `LibKa0s-R-15` (Info), `LibKa0s-A-02` (Low), `LibKa0s-A-11` (Info). Clusters C14, C15.

**Change.**
1. `CHANGELOG.md`: date the v1.56.0 block. Its versions line lists Core 8, Item 2, Media 4, Bus 2,
   Lifecycle 2, Launcher 2, Slash 15, DebugLog 13, Perf 13 (key 13.5), Widgets 10 (key 10.2), Schema 2,
   Options key 24.31.4.7.4, with Env 1, Compat 1, Pool 3, WidgetsDragHandle 2 and PerfPanel 5 unchanged,
   and kit revision 26. A **consumer obligations** section lists the surface-parity churn (Core stub +
   `SafeRegister*`; Schema instance stub + `SetMany`) and the behavioral kit flips (`CreateFrame` shown,
   AceDB raises and strips defaults, `EventRegistry` recorded, lone CR, store-root prose, `§` case names).
2. `docs/api/README.md` rows all present.
3. `README.md`: the Tests badge from `docs/test-cases.md` Totals, and the standards pointer rolled to
   v2.65.0 (`head -1 ../WowAddonStandards/standards/STANDARDS.md`).
4. `docs/releasing.md`: provenance template → v1.56.0; rewrite "Where v1.56.0 stands" (steps 1-7 done,
   step 8 pending the owner); step 9 re-sweeps the Consumers table (the Core row names
   `SafeRegisterEvent` consumers once adopted; the Schema row notes `writeThrough`/`SetMany`).
5. Commit, confirm `git status --porcelain` is empty, run
   `~/.claude/wow-addon/bin/ka0s-bounded tests/_kit/run-automated-tests.sh --release 1.56.0`, and check
   LK-31's manifest preconditions.
6. Second commit: the bundle, `RESULTS.md` and `<stamp>/ANALYSIS.md`. The analysis names once the six
   tags with no bundle (v1.28.0, v1.29.0, v1.36.0, v1.36.1, v1.54.1, v1.54.2), the release-run
   `ANALYSIS.md` gap, the misreading at `20260916-093057/ANALYSIS.md:60-62`, and the one-off over-count
   at `20260908-181447/ANALYSIS.md:92`. It also holds the authored Disposition cells: over-cap rows point
   at the `CLAUDE.md` census row and its issue, band rows cite LK-32's issues or re-rules, and the
   CCN-15 functions are recorded as watch entries.
7. Final collection dry-run with the full payload (`libs/LibKa0s` from `LibKa0s/`, `tests/_kit` from
   `testkit/`) into an archived copy of each addon, as LK-05. The red cases per addon go into
   `ANALYSIS.md`'s consumer section.
8. `git tag -a v1.56.0 -m 'LibKa0s v1.56.0'` **locally** on `feat/2026-09-23-review-audit-remediation`.
   The tag stays local until the owner approves the LibKa0s merge. The branch is pushed to origin at the
   end of Milestone 1, unmerged.

**A count to correct in the analysis.** `LibKa0s-R-15` says **four** functions sit at exactly CCN 15.
Running the item's own lizard command at HEAD (bounded, 2026-09-23) reports **six**: `lib.Catalog`
(`Bus.lua:295`), `lib.GetSpellCooldown` (`Compat.lua:243`), `idHelpIcon` (`OptionsWidgets.lua:2944`),
`liveTimers` and `M.__fire` (`testkit/mock_record.lua:95`, `:539`) and `audit`
(`testkit/test_layout_cap.lua:427`). LK-33's list of six is right. The finding under-counts, most likely
because the review bundle excluded `testkit/`. Record all six as watch entries. LK-03, LK-14 and LK-27
edit three of those files and must not push any of the six over 15.

**Ripple.** The release gate is the test: lint, tests and complexity pass, zero functions above CCN 15,
perf recorded as a reason-(1) skip, and `test_versioning`, `test_kitsync` and the layout cap green.
`git ls-remote --tags origin v1.56.0` must stay empty until the owner approves.

**Blast radius.** All eleven, through the eleven re-vendors.

**v1.56.0 must carry LK-03.** LK-03 (the AceDB fake fidelity change) was outside the tag's dependency
closure in the first draft. LK-33 now depends on it directly (plan-review decision 5).

**Consumer follow-ups.** The re-vendors RV-AT, RV-AM, RV-BL, RV-CM, RV-KC, RV-LH, RV-MM, RV-PM, RV-PF,
RV-PC, RV-WG (Milestone 2) each copy both payloads whole from the local tag, roll the `CLAUDE.md`
provenance line in the same commit. The `RV-` commit does not regenerate `docs/test-cases.md` or the
README tests badge; the addon's next item does, at the latest `<AB>-DOCS`. The same commit
writes `docs/revendor/2026-09-23-v1.56.0/` by hand (see WA-01 and *Release mechanics*). Each `RV-`
depends on LK-33 and WA-01.

The pre-re-vendor fixes are Milestone 2 items. Each depends on LK-33, its addon's `RV-` depends on it,
and each must pass on both the v1.55.0 payload and the v1.56.0 dry run (plan-review decision 2). The
`RV-` commit itself stays copy-only.

| Addon | Before its `RV-` (M2) | Why |
|---|---|---|
| AuraMaster | AM-01, AM-02 | Lone CR (LK-06) and every dry-run red; the span bundle before the re-vendor's own bundle. |
| BankLedger | BL-01, BL-02 | The `wow_mock` `C_Timer.After` override (dropping it alone reddens `test_disabled` until the prune moves to AceTimer), and the Schema stub's `SetMany` for `test_surface_parity.lua:315-320`. |
| ConsumableMaster | CM-01 | LK-07 prose reds, plus any other dry-run red. |
| KickCD | KC-01 | LK-07 prose reds and the LSM fake's locale bits (LK-13). |
| WhatGroup | WG-01 | The `SetItemRef` `EventRegistry` survivor. |
| AbsorbTracker | AT-01 | Schema stub parity (`SetMany`, `writeThrough`). |

The other named fixes are Milestone 3 and follow their re-vendor:

| Addon | After its `RV-` (M3) | Why |
|---|---|---|
| WhatGroup | WG-02 (a red at RV-WG is listed in that commit's body; WG-02 clears it) | LK-25's combat park re-pin. |
| PartyFrameEnhanced | PF-05, PF-06, PF-01 | Kit-26 `test_disabled` steps 3 and 5; profile verbs. |
| AbsorbTracker | AT-03 | Profile guards; green on kit 25 and 26. |
| PrettyChat | PC-01 | Schema stub parity. |
| PanelMaster | PM-01 | Schema stub parity, plus any dry-run red RV-PM left. |

**Red re-vendor commits.** The `RV-<AB>` item text still says "if the suite goes red, record the
failures in the commit body; the fixes are this addon's M3 items", and that is the rule for all eleven.
Every `RV-<AB>` commit is copy-only (`libs/LibKa0s`, `tests/_kit`, the `CLAUDE.md` provenance line and
`docs/revendor/2026-09-23-v1.56.0/`). It is green or lists its reds in its body. For the six addons with
an M2 pre-fix, the dry run finds the reds and the pre-fixes land first to make the commit green. For
LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced and PrettyChat, which have no M2 pre-fix, a
predicted red is recorded in the commit body. Either way the addon's M3 items clear any remaining red,
and the addon is green again at the latest by `<AB>-DOCS`.

**Depends on:** LK-32, WS-08, LK-05, LK-06, LK-08, LK-09, LK-11, LK-12, LK-13, LK-14, LK-15, LK-16, LK-18,
LK-19, LK-20, LK-21, LK-23, LK-03. **Effort:** M.

---

# Group C — the `wow-addon` plugin (2.3.0 → 2.4.0)

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon`. Markdown commands and agents, a Python
test, and one shell wrapper.

---

## WA-01 · `revendor-libka0s`: take the delta base from the addon's provenance line, name bundles by tag, and write consolidated span bundles

**Resolves:** `AuraMaster-A-21` (Low, dispositioned here). Cluster C01. **The finding's premise is wrong,
but the change is still right.**

**Change.** `commands/revendor-libka0s.md`. Step 3a: the base tag is the one the addon's `CLAUDE.md`
provenance line names, cross-checked against `git log -1 --format=%H -- libs/LibKa0s` and that commit's
`CLAUDE.md`. It is never "the library's previous tag". Step 3c: the per-file minor table comes from the
tag's `LibKa0s.xml` plus the `grep -hoE 'local (MAJOR, )?[A-Z_]*MINOR …'` command, which covers
`TABS_MINOR`, `COMPOSE_MINOR`, `DRAG_MINOR`, `SCROLL_MINOR`, `WIDGETS_MINOR` and `PANEL_MINOR`, replacing a
stale constant table. The bundle folder is `docs/revendor/<YYYY-MM-DD>-v<tag>/`. When the span crosses
unrecorded tags, write WS-01's consolidated span bundle (`<date>-v<first>-v<last>/`, line 1 exactly
`Delta: LibKa0s v<A> -> v<B> (span: ...)`). A frozen bundle with a misstated base is never edited.
The new bundle notes the correction once. A report-only pre-flight lists, per addon in
`standards/ADDONS.md`, whether its newest bundle's line-1 base equals the provenance tag at the previous
re-vendor commit.

**Correction to the item's dry-run expectation.** WA-01 says the amended Step 3a, followed by hand on
AuraMaster, "yields v1.53.0 as the base of the v1.55.0 span, where the old procedure gave v1.54.2", and
that the pre-flight "finds AuraMaster's v1.54.2-for-v1.53.0 base". The tree says otherwise. Commit
`329e1a3` ("Adopt the kit's US-English gate…") re-vendored LibKa0s **v1.54.2** whole (kit-only; the
library bytes equal v1.53.0's), and `CLAUDE.md`'s provenance line reads v1.53.0 at `f6f61d3`, **v1.54.2
at `329e1a3`** and v1.55.0 at `f6f3ffb`. The previous re-vendor before v1.55.0 is therefore `329e1a3`,
the provenance base is v1.54.2, and AuraMaster's frozen bundle `docs/revendor/2026-09-23-v1.55.0/`
(`Delta: LibKa0s v1.54.2 -> v1.55.0`) is **correct**. The AuraMaster planner reached the same conclusion
independently. Consequences:
- The WA-01 dry-run check must expect **v1.54.2** for AuraMaster, and the pre-flight must report
  AuraMaster clean.
- `AuraMaster-A-21` should be closed as not a defect, with this evidence, rather than as fixed.
- The LK-33 AuraMaster follow-up ("note once that the frozen v1.55.0 bundle's base should have read
  v1.53.0") must **not** be carried out. AM-02 already writes no correction paragraph. RV-AM's bundle
  must not add one either.

The plan-review correction in WA-01's item text now says the same: every addon had a kit-only v1.54.2
re-vendor (AuraMaster `329e1a3`, ConsumableMaster `1f86d4e`, BankLedger `6b12edf`, PrettyChat `8421342`,
WhatGroup `7f38ddd`), so the frozen v1.55.0 bundles correctly read `v1.54.2 -> v1.55.0`; the base is
cross-checked with `git log -1 -- libs/LibKa0s tests/_kit` (both paths); and the dry run expects v1.54.2.
The item's `tests` line still quotes the old v1.53.0 expectation and is superseded by the correction.

The rule WA-01 writes (base = provenance line) is still correct, and the rest of the item (tag-named
folders, the minor grep, span bundles) stands.

**Ripple.** Part of plugin 2.4.0 (bumped by WA-03).

**Blast radius.** Every re-vendor in Milestone 2. **But the installed plugin is 2.3.0 from GitHub**, so
`/wow-addon:revendor-libka0s` keeps running the old command until the merge (see *Release mechanics*).
That is why every `RV-<AB>` depends on WA-01 and writes its bundle by hand from the local command file.

**Consumer follow-ups:** every `RV-<AB>` follows the amended procedure by hand, from the local
`../wow-addon/commands/revendor-libka0s.md` at the WA-01 commit, and writes
`docs/revendor/2026-09-23-v1.56.0/` with line 1 exactly `Delta: LibKa0s v1.55.0 -> v1.56.0`. The span
bundles are WS-01's; the ones in AM-02, BL-23, CM-28, KC-24, LH-34, MM-30, PF-24, PC-25, PM-18 and
WG-29 are normalized to WS-01's exact line-1 grammar and depend on WA-01.

**Depends on:** WS-01. **Effort:** S.

---

## WA-02 · Ship `bin/ka0s-bounded` so the bare name resolves on the plugin's PATH entry

**Resolves:** `MultiMeters-R-20`, `ConsumableMaster-R-19` (both Info, dispositioned here). Cluster C47.

**Change.** The plugin's PATH entry is `<plugin>/bin`, but the runner ships only at
`scripts/ka0s-bounded` (confirmed: `wow-addon/bin/` does not exist). Add `bin/ka0s-bounded`, a POSIX sh
wrapper: `exec "$(dirname "$0")/../scripts/ka0s-bounded" "$@"`, mode `+x`, LF, and a `.gitattributes`
entry if one lists scripts. Keep the hook's `~/.claude/wow-addon/bin` symlink refresh. `CLAUDE.md` :23
names `bin/`. `scripts/test_bounded_runs.py` gains a case that the bare prefix is classified as bounded.

**Ripple.** Part of plugin 2.4.0. Red-first case in `scripts/test_bounded_runs.py` and a shell check.

**Blast radius.** Every session, **once the plugin updates**. Until then every verify command in this
plan uses the absolute `~/.claude/wow-addon/bin/ka0s-bounded`, which works today. The local hook refused
an unbounded `lizard` during this document's own measurement, which confirms the hook is active.

**Consumer follow-ups:** none. The addon items already use the absolute path.

**Depends on:** nothing. **Effort:** S.

---

## WA-03 · Review agent's cross-addon baseline re-measured at v1.56.0 and derived rather than trusted; plugin 2.4.0

**Resolves:** `LootHistory-R-19`, `MultiMeters-R-19` (both Info, dispositioned here). Cluster C47.

**Change.** `agents/review.md`: replace the 2026-09-07 baseline (:357-368, and the nine-addon counts at
:193 and :365) with values measured at LibKa0s v1.56.0: eleven addons; fifteen majors
(`grep -c 'major = "LibKa0s-' ../LibKa0s/tests/majors.lua`); the per-file minors in LK-33; kit 26;
`## Interface: 120100` uniform; the slash-root count by the brief's own command (22 on 2026-09-23). Each
figure sits beside its command, with an instruction to re-derive at run time and to read a mismatch after
a library tag move as a stale brief, not drift. Bump `.claude-plugin/plugin.json` **2.3.0 → 2.4.0**.
Update `CLAUDE.md`'s "Current version" and `README.md` if it states the version.

**Ripple.** Closes plugin 2.4.0.

**Blast radius.** Every `/wow-addon:review` run after the plugin updates.

**Consumer follow-ups:** none.

**Depends on:** LK-33, WA-02. **Effort:** S.

---

# Owner-scope issues and the upstream work each needs

| Issue | Upstream work | Addon item |
|---|---|---|
| AuraMaster#21 (Schema primitives, registry, bulk bracket, validation) | LK-22 (`normalize` makes a partial adoption possible) | AM-15 |
| AuraMaster#16 … #19 (file peels) | **None** | AM-23 … AM-26 |
| ConsumableMaster#39 (Schema for the write seam) | LK-22 (`normalize`, `SetMany`) | CM-17 |
| KickCD#22 (Schema for the settings runtime) | LK-22's adoption note only; no new surface | KC-18 |
| MultiMeters#52 (Schema path primitives, registry, bracket) | LK-22 (`SetMany`) | MM-14 |
| PanelMaster#52 (Bus `Catalog` for message constants) | **None**: `lib.Catalog` already ships in v1.55.0 | PM-12 |
| PartyFrameEnhanced#14 (adopt Schema once a library-less build can write composed rows) | WS-02 (ruling), LK-23 (`writeThrough`) | PF-11 |
| PrettyChat#18 (`ResetRows` onto `BulkRun`/`BulkAdd`) | **None** | PC-05 |
| WhatGroup#22 (adopt Schema; degraded `enable`/`test` accepted as a known gap) | WS-02 (route (b) and the library-absent line), LK-18 (stub contract), LK-23 (reference stub; WhatGroup passes no list) | WG-12, WG-13 |

The owner's WhatGroup ruling (no Lua error; a chat line saying the verb is unavailable without LibKa0s)
is WS-02's route (b), and its exact text is WS-02's locale sentence. The PartyFrameEnhanced ruling ("once
a library-less build can still write its composed rows") is what LK-23 makes true.

---

# Considered and not done upstream

These are recorded so the decision is not re-argued next cycle.

- **Option A1 of AbsorbTracker's review item 62 / Info-6 (not plan item AT-62)** (composers in a unit
  that loads without the Options major) is declined in favor of `writeThrough`. A1 cannot help the truly
  library-less build that `tests/degraded_env.lua` models. `writeThrough` serves that build and a partial load.
- **A shared migration runner in LibKa0s.** The per-profile bug (KickCD, PartyFrameEnhanced, PrettyChat)
  and the stripped stamp (WhatGroup, LootHistory, PanelMaster) are fixed at the standard's template
  (WS-03). The steps are host-specific and a runner is about 20 lines, which does not clear
  `library-stack-§7`'s bar for a shared surface.
- **The `InCombatLockdown()`-versus-combat-edge defect** (LootHistory, PanelMaster) recurs in two addons
  only and stays local.
- **`ReplayPending` on the Options instance** (the original A3 proposal) is replaced by LK-25's
  self-replay, so no Options stub gains a member.
- **Renaming the `minimise` icon key** stays out of scope. It is `LibKa0s-Media-1.0`'s public icon name
  (`media/icons/minimise.tga`), and MultiMeters MM-13 records it as a sanctioned library-field-name
  waiver.
- **Retiring ConsumableMaster's local AceDB fake** would need a CallbackHandler string-method form and
  `db.profiles` in the kit fake. It is not in this milestone (see LK-03).

---

# Release mechanics

**Nothing in Milestone 1 is merged to `master` until the owner approves the merge.** At the end of each
milestone the remediation branch of every repository it touched is pushed to origin, unmerged. The
`v1.56.0` tag stays local until the owner approves the LibKa0s merge. LK-32's issue filing writes
issues, not code.

## LibKa0s: v1.56.0 is a local tag, and every re-vendor copies from it

- LK-33 creates the annotated tag `v1.56.0` **locally** on `feat/2026-09-23-review-audit-remediation`.
  The tag stays local and is pushed only when the owner approves the LibKa0s merge. The branch is
  pushed to origin at the end of Milestone 1, unmerged.
- **Every `RV-<AB>` item copies from that local tag**, not from the working tree and not from GitHub:
  `git -C ../LibKa0s archive v1.56.0` (or a worktree at the tag), `rm -rf` then copy
  `LibKa0s/` → `libs/LibKa0s/` and `testkit/` → `tests/_kit/` whole, keeping the runner executable, and
  roll the `CLAUDE.md` provenance line to v1.56.0 in the same commit.
- Consumers' `tests/test_vendor_sync.lua` resolves the provenance tag from the **local sibling
  checkout**, so the re-vendored suites pass offline against the local tag.
- **The tag must not move once any re-vendor has copied it.** A defect found in Milestone 2 or 3 is fixed
  forward as v1.56.1 (also local). Re-pointing v1.56.0 would leave earlier re-vendors byte-different from
  the tag their provenance line names, and `test_vendor_sync` would stop agreeing with them.
- **An addon branch whose provenance line names v1.56.0 may reach origin before the tag does.** That is
  acceptable: the branch is unmerged, and the tag is one push away once the owner approves the LibKa0s
  merge.

## WowAddonStandards v2.65.0 and plugin 2.4.0 reach the default branch only on the owner's merge approval

- **v2.65.0** exists only on WowAddonStandards' feature branch (pushed to origin at the end of Milestone
  1, unmerged) until the merge. The addon items that
  *apply* a v2.65.0 ruling (WS-02 … WS-06 follow-ups) do not need the merge: they read the local
  sibling, like this plan does. What does need it:
  - `/wow-addon:revendor-standards` fetches `standards/STANDARDS.md` and the section files from GitHub.
    Run before the merge, it finds v2.64.0 and records the wrong version.
  - `/wow-addon:standards-audit` and `/wow-addon:review` fetch the standard and `AUDIT.md` from raw
    GitHub. Until the merge they grade against v2.64.0 and the old AUDIT.md re-vendor check.
- **Plugin 2.4.0** exists only on wow-addon's feature branch (pushed, unmerged). The installed plugin is
  `wow-addon@wow-addon` **2.3.0**, installed from the GitHub marketplace `tusharsaxena/wow-addon` with
  autoUpdate on. Until the merge and a plugin update:
  - **`/wow-addon:revendor-libka0s` runs the 2.3.0 command, not WA-01's.** A local WA-01 commit does not
    change what the installed command does. So Milestone 2 does not run the command: each `RV-<AB>` depends
    on WA-01 and writes `docs/revendor/2026-09-23-v1.56.0/` by hand, following the **local**
    `../wow-addon/commands/revendor-libka0s.md` at the WA-01 commit (base = provenance line, tag-named
    folder, span bundle where one is owed). Line 1 of its `01_DELTA.md` is exactly
    `Delta: LibKa0s v1.55.0 -> v1.56.0`, and the item's verify command checks it (plan-review
    decision 3).
  - The bare `ka0s-bounded` (WA-02) does not resolve. Keep the absolute path.
  - The review agent keeps the 2026-09-07 baseline (WA-03).

## The standards-dependent addon items are Milestone 4 and wait for the merge

The eleven `/wow-addon:revendor-standards` items form **Milestone 4**, which is owner-gated. They are
**blocked** until WowAddonStandards' branch, carrying WS-01 … WS-08 and the dated v2.65.0 entry, is merged
to its default branch and pushed (plan-review decision 4):

AbsorbTracker AT-26 · AuraMaster AM-35 · BankLedger BL-25 · ConsumableMaster CM-31 · KickCD KC-27 ·
LootHistory LH-36 · MultiMeters MM-32 · PanelMaster PM-16 · PartyFrameEnhanced PF-25 · PrettyChat PC-26 ·
WhatGroup WG-30.

Gate, run before each:

```
gh api repos/tusharsaxena/WowAddonStandards/contents/standards/STANDARDS.md --jq .content | base64 -d | head -1
```

It must name v2.65.0. If it does not, stop and leave the item open. Do **not** hand-edit the three-place
reference (TOC `## X-Standard`, README badge, `CLAUDE.md`) from the local sibling. The default branch is
**`master`**. The per-addon `<AB>-DOCS` items no longer
wait on the gate: each is Milestone 3, and each gated item runs **after** its addon's DOCS item and
carries its own three-place ripple. For example, LH-36 runs after LH-DOCS and WG-30 after WG-DOCS.

## What the owner approves, and in what order it is published

The standard names LibKa0s v1.56.0 and kit 26 (WS-02, WS-04, WS-08). LibKa0s's README names standard
v2.65.0 (LK-33). The plugin's review brief names v1.56.0 (WA-03). None of the three reads correctly on
GitHub without the other two, so **one approval should cover all three**, published in this order:

1. **WowAddonStandards**: merge the feature branch to `master` and push. v2.65.0 is live for
   `revendor-standards`, the audit and the review agents.
2. **LibKa0s**: merge to `master`, push the branch, then `git push origin v1.56.0`. Confirm with
   `git ls-remote --tags origin v1.56.0`.
3. **wow-addon**: merge to `master` and push. Confirm the marketplace update brings
   `installed_plugins.json` to 2.4.0 before relying on WA-01, WA-02 or WA-03 behavior.
4. Unblock the eleven Milestone 4 revendor-standards items. Each runs after its addon's `<AB>-DOCS`
   item, which has already landed in Milestone 3.
5. Addon branches are already on origin from the milestone-end pushes. One whose provenance line names
   v1.56.0 may have been pushed before step 2; that is acceptable, because it is unmerged and step 2
   publishes the tag. No addon branch is merged without the owner's go-ahead.

## Milestone 1 exit criteria

- WowAddonStandards: `head -1 standards/STANDARDS.md` names v2.65.0 with a date. One changelog entry
  holds paragraphs (1) … (7) and the WS-08 summary. `grep -rnE '§[0-9]+\.[0-9]+'` over `standards`,
  `AUDIT.md` and `NEW_ADDON.md` prints nothing. No CR in any tracked file.
- LibKa0s: `lua5.1 tests/run.lua` green, the `--list` diff empty, lizard silent at `-C 15` with the six
  CCN-15 functions recorded as watch entries, `diff -r testkit tests/_kit` empty, `test_versioning` green
  against the versions line in the per-file table above, and `framework.lua`, `test_prose.lua`,
  `Options.lua` and `mock_base.lua` under 1500 lines.
- The release bundle's `manifest.json` reads `"release": "1.56.0"`, `git.dirty: false` and zero complexity
  warnings, and `ANALYSIS.md` exists beside it.
- `git tag -l v1.56.0` prints the tag, and `git ls-remote --tags origin v1.56.0` prints nothing.
- The LK-33 dry-run output exists for all eleven addons, and every red in it is assigned to an item in
  the tables under LK-33 (a Milestone 2 pre-fix, or a Milestone 3 item after the re-vendor).
- wow-addon: `.claude-plugin/plugin.json` reads 2.4.0, `bin/ka0s-bounded` is executable,
  `python3 scripts/test_bounded_runs.py` passes, and WA-01's AuraMaster dry-run check expects v1.54.2.
- WA-02 and WA-03 are done too. They are not ancestors of any `RV-`, but Milestone 2 starts only once
  every Milestone 1 item is complete.
- The owner has ruled on the two open points this document still raises: LK-25's combat park against
  `options-ui-§9`, and LK-18's resolver fallback. (WS-06's migration sentence and the green-re-vendor
  rule were settled by the plan review: no minimap migration anywhere, and the pre-re-vendor fixes are
  Milestone 2 items that land before their `RV-`, which is green or lists its reds in its body.)
