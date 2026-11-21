# The house pattern for a WoW Forever port (LootHistory + BankLedger)

Research date 2026-11-21. Paths: `STD` = `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards/standards`,
`LK` = `.../GIT/LibKa0s`, `CT` = `.../GIT/Ka0sAddonsCommonTasks`. V = VERIFIED (read in source), I = INFERRED.

## 0. Current state of the two addons (V)

| | LootHistory | BankLedger |
|---|---|---|
| Branch / tree | `master`, clean, head `e855607` | `master`, clean, head `1f51a0e` |
| TOC line 1 | `## Interface: 120105` (CRLF) (`LootHistory.toc:1`) | `## Interface: 120105` (CRLF) (`BankLedger.toc:1`) |
| `## Version:` | `1.5.0` (`LootHistory.toc:5`) | `1.3.0` (`BankLedger.toc:5`) |
| Gating lines | none (correct for port-pending, clients-§8) | none |
| LibKa0s vendored | v1.109.0 (`LootHistory/CLAUDE.md:58`) | v1.109.0 (`BankLedger/CLAUDE.md:48`) |
| Kit revision | 59 (`tests/_kit/framework.lua:20`) | 59 (same) |
| Standard vendored | quirks catalog v2.117.0 (`docs/midnight-quirks.md:7`) | v2.117.0 (`docs/midnight-quirks.md:5`) |
| Standard head | v2.117.0 (`STD/STANDARDS.md:1`), tag pushed per CT 6517101 | |
| Roster row | `Retail (port pending)` (`STD/ADDONS.md:27`) | `Retail (port pending)` (`STD/ADDONS.md:21`) |
| README badge / sentence | `Midnight_12.1.5`, "Retail only for now; WoW Forever support is planned." (`README.md:3,9`) | same (`README.md:3,9`) |
| Quirks docs | `docs/midnight-quirks.md` only; ARCHITECTURE map row `forever-quirks.md` Not applicable (`docs/ARCHITECTURE.md:576`) | same (`docs/ARCHITECTURE.md:779`) |
| Client reads | none: no `IsForever/IsRetail/ClientKey/ForClient/clients =` anywhere in core/defaults/settings/modules | none |
| Default skin | literal `skin = "ka0s"` (`defaults/Profile.lua:68`), no `NS.DEFAULT_SKIN` | literal (`defaults/Profile.lua:89`), no `NS.DEFAULT_SKIN` |
| Name/realm sites | `core/Util.lua:7-9` char key `UnitName`+normalized realm; `core/Util.lua:370` realm; `core/Compat.lua:1050` `local name, realm = UnitName("NPC")` (surname read as realm on Forever); `core/Compat.lua:1054,1066-1067` | `core/Compat.lua:37-39` char key `Name-Realm` |
| Bindings.xml | 2 lines, `CLICK LootHistoryToggleWindow:LeftButton` (serves both, I) | `CLICK BankLedgerToggleWindow:LeftButton` |
| `.pkgmeta` | no game-version field (none in any Ka0s repo) | same |
| `test_client_globals` wired | yes (`tests/run.lua:220`); no `tests/client_globals_allow.lua` | yes (`tests/run.lua:51`); no allowlist |

**Baseline runs (V, this session, bounded runner, scratch outputs `baseline-*.txt`):**
- LootHistory retail 2054/0/1, forever 2054/0/1.
- BankLedger retail 1724/0/1, **forever 1719/5/1**: SimWorld identity and sample-character cases expect
  `Sampleblade-Samplerealm` and get `Sampleblade Mockvale` (`baseline-BankLedger-forever.txt:1337-1408`).
  I: the forever profile drives LibKa0s Sim/Compat regional names, so BL's `core/SimSetup.lua:130-140`
  `Name-Realm` sample roster needs a per-client list (precedent DW-FP04/DW-FP09).
- **Forever globals scan armed** (scratch shallow clones with TOC `120105, 16001`, `clones/armed-*.txt`):
  `client globals: no call of a global a client lacks` PASS for both; BL still the same 5 failures, LH 0.
  (The 2 extra skips are vendor-sync cases that cannot find sibling LibKa0s from the clone path.)

## 1. Rules a port must satisfy (V, with citations)

- Both clients default; flip row in the **same change** that lands the port (`STD/standards/clients.md:25-28`).
- TOC: one unsuffixed TOC, `## Interface: <retail>, <forever>` = `120105, 16001`, **no** gating line
  (`STD/standards/toc-file.md:61-62`; `clients.md:27`). Forever = 1.60.1, interface 16001, project 18
  (`clients.md:17`). Retail number has no literal in the standard (`toc-file.md:82`).
- README badge `WoW-Midnight_12.1.5_and_Forever_1.60.1` and opening sentence "Supports Retail and WoW
  Forever." (`STD/standards/documentation.md:66`; `toc-file.md:85` badge in lockstep with TOC).
- Detection only via Compat `IsForever/IsRetail/ClientKey`; never `WOW_PROJECT_*` or interface numbers
  (`clients.md:33-36`; `compat.md:42`). Feature detection allowed only for one API gap inside a supported
  feature (`clients.md:37`).
- Per-client features: declared `clients = { "retail" }` on the library descriptor (options/slash/launcher/
  bindings) or `Compat.ForClient(...)` at the host's own registration (module OnInitialize, events); absent,
  never hidden (`clients.md:42-46`; `LK/docs/api/Compat/version-5-docs.md:176-192`).
- Bindings.xml line cannot be gated; not graded (`clients.md:47`).
- `docs/ARCHITECTURE.md` per-client feature table (feature, client, gating file) or "all features serve both
  clients" (`clients.md:48`). DW model: `DropWatcher/docs/ARCHITECTURE.md:129-170`.
- Seeds: two lists picked once by `ClientKey()`; never a filtered Retail list; empty-by-decision allowed
  (`clients.md:59-75`); DB2/wago re-validation SHOULD (`clients.md:113-168`).
- Tests: whole suite green under **both** `KA0S_KIT_CLIENT=retail|forever`; each per-client feature has a
  present-here/absent-there case (`clients.md:79`). Kit profiles: retail leaves `WOW_PROJECT_CAMELOT` nil;
  forever = 18, build `1.60.1/70790/16001`, removes spec globals + `SetDesaturation`
  (`LK/docs/api/testkit/version-52-docs.md:25-36`; `LK/testkit/mock_client.lua:18-28`).
  The globals scan checks forever **only when the TOC carries a 16xxx number** (`LK/docs/api/testkit/version-53-docs.md:34`),
  so the TOC flip arms it.
- Smoke: every check names its client; absent features get a "not there" check on Forever; agents never mark
  passed (`clients.md:81-82`). PanelMaster shape: `docs/smoke-tests.md:34,39-41,1440-1442` (a `## WoW Forever`
  section, **Client: WoW Forever (1.60.1, interface 16001)**).
- Quirks: port **adds** `docs/forever-quirks.md` (vendored Forever catalog block `<!-- BEGIN VENDORED: forever
  quirks catalog v2.117.0 (source: WowAddonStandards) -->` ... END, then `## <Addon>-specific quirks`, may be
  empty) in the change that flips the row; keep `docs/midnight-quirks.md` (`clients.md:91`;
  `STD/standards/forever-quirks.md:42-72`; `documentation.md:297-298`; DW example `DropWatcher/docs/forever-quirks.md:5,191`).
  ARCHITECTURE doc-map row moves from Not applicable to Present (`documentation.md:507`; DW `ARCHITECTURE.md:785`).
- Names/realms: use Compat `UnitCharacterName`, `CharacterKey`, `RealmKey`, `RegionalNames` (Compat minor 4+,
  LibKa0s v1.94.0+); never read `UnitName`'s 2nd return as realm; never split names on whitespace; size
  surfaces for "First Surname" and the long realm label (`forever-quirks.md:119-152`;
  `LK/docs/api/Compat/version-5-docs.md:24-32,85-88`). Realm key = ruleset (`PvP`), so two PvP realms share a key.
- Default skin: `NS.DEFAULT_SKIN = Skin:DefaultSkin()` read once at load, named in profile defaults; never the
  literal or an own client check (`STD/standards/skinning.md:36`; PM `core/SkinSetup.lua:104`, `defaults/Profile.lua:84`;
  DW `core/SkinSetup.lua:105`).
- Forever secret values: `UnitStat` secret, `C_UnitAuras` raises when tainted; treat Retail secret rules as
  assumed on Forever (`forever-quirks.md:73-117`). Missing-API surface open (LibKa0s#44, `forever-quirks.md:156-158`).
- Interface bumps later: Forever number moves only when Blizzard moves it, via `/dev-copilot:wow-bump-interface`
  (`STD/standards/versioning-git.md:8`).

## 2. The port checklist (what every port touched)

Evidence: OutfitterReborn `3ce8e90` (OR-F6 "the port shape", 9 files), PanelMaster `e75f69c` (W2-PM-01,
25 files), DropWatcher `8134b3f` (DW-FP12, 10 files) + DW-FP00..FP22, AuraMaster port plan folder.

1. **TOC** line 1 -> `## Interface: 120105, 16001` (keep CRLF). No gating lines. (all three ports)
2. **README**: badge `Midnight_12.1.5_and_Forever_1.60.1`; sentence "Supports Retail and WoW Forever.";
   test-count badge regenerated; optional "On WoW Forever" section (OR) ; Version History bullet but **no
   version bump** (OR-F6 body: "No version bump"; DW/AM TOC still 1.1.0, V).
3. **CLAUDE.md** green gate: `lua tests/run.lua`, `KA0S_KIT_CLIENT=forever lua tests/run.lua`, bounded luacheck
   (`DropWatcher/CLAUDE.md:39`, `AuraMaster/CLAUDE.md:34`).
4. **docs/testing.md**: both-profile commands and a "Both clients" subsection (`DropWatcher/docs/testing.md:11,880`).
5. **DEPENDENCIES.md**: runtime is Retail or Forever at the TOC's two numbers; forever-profile run in the
   setup check (OR-F6 body; DW-FP12 body).
6. **docs/ARCHITECTURE.md**: overview names both clients; per-client feature table; Known Limitations Forever line;
   doc-map `forever-quirks.md` Present.
7. **docs/forever-quirks.md** NEW (vendored block + own section). midnight-quirks.md stays (pre-v2.117.0 ports
   put a Forever section in midnight-quirks, DW-FP12; under v2.117.0 Forever findings go in forever-quirks).
8. **docs/smoke-tests.md**: index row + `## WoW Forever` section; each check names client; absent-feature checks;
   Retail parity; load without "Out of date"; WoW Forever default skin on a fresh profile; diagnostics.
9. **core/Compat.lua** (or `core/CompatClient.lua`, DW): route `IsForever/IsRetail/ClientKey/ForClient/
   RegionalNames/UnitCharacterName/CharacterKey/RealmKey` from LibKa0s-Compat-1.0, plus degradation-stub
   arms; the Retail/Forever API differences (bank, loot) live here behind named flags (`compat.md`).
10. **core/SkinSetup.lua + defaults/Profile.lua**: `NS.DEFAULT_SKIN` (DW-FP03, PM e75f69c).
11. **Name-key adoption** (DW-FP04 `d0f6dec`): a `PlayerRecordKey()` seam: `CharacterKey()` on regional names,
    the existing `Name-Realm` on Retail so stored Retail data stays the same character
    (`DropWatcher/core/CompatClient.lua:60-75`). LH `core/Util.lua:7-9`, `:370`, `core/Compat.lua:1047-1067`;
    BL `core/Compat.lua:37-39`. I: neither addon then needs a SavedVariables migration on Retail.
12. **Feature gating**: Warband bank, group finder, any Retail-only bank tabs/types, Retail-only loot sources
    declared `clients = { "retail" }` / `ForClient`; defaults only a Retail feature reads added on Retail alone
    (DW-FP21). I: the bank model and loot sources are the port's real work (00_CLASSIFICATION.md:65-66).
13. **Seeds per client**: test-mode/sim sample characters, places, items (DW-FP09); BL's SimSetup roster
    (current forever failures). Any Retail item/currency/source seed gets a Forever twin or is empty by decision.
14. **tests/**: a TOC case pinning `120105, 16001` and no gating line; a case that the TOC arms the forever
    globals scan; README dual badge + sentence case (DW-FP12 body); per-client present/absent cases;
    fixtures that pinned `Name-Realm` read a per-profile helper (DW: `T.rosterName`/`T.ME`).
    `docs/test-cases.md` regenerated (`lua tests/run.lua --list`).
15. **.luacheckrc**: add any newly read globals (PM added `issecretvalue`, e75f69c).
16. **Other docs** that name client reads: compat-layer.md, module-map.md, data-flow.md, schema.md, scope.md
    (PM e75f69c touched compat-layer, module-map, schema, scope; DW-FP04 touched compat-layer, module-map, data-flow).
17. **Roster flip** in `WowAddonStandards/standards/ADDONS.md`: one-line commit, "Roster data only; **no version
    bump**" (`git show 88185bb` AM WS-FP01; DW `4a16a2d`, OR `28f927a`, CM `5bd7dda`: each 1 file, 1+/1-).
18. **Not touched by any port**: `.pkgmeta` (no game-version mechanism; last .pkgmeta commits unrelated, V),
    `## Version:`, tags. CurseForge dual tagging is **unproven**: every journal file is still `['12.1.0']`
    (latest release 2026-10-09, `CT/journal/curseforge/*/files.json`, V); the open question
    (`CT/docs/2026-11-07-WOW_FOREVER_PORT_STEP5/00_CLASSIFICATION.md:76-78`; CurseForge Forever type 88568,
    `CT/docs/2026-11-07-WOW_FOREVER_PORT/research_notes/WoW Forever porting research/04_multi_client_packaging.md:92,103,108`).

## 3. Plan/bundle mechanics (V)

- Two addons + the standard = cross-repo: CommonTasks bundle `docs/<date>-<TOPIC>/` (CT CLAUDE.md). Precedent for
  a multi-repo port bundle: `CT/docs/2026-11-10-QUICKCOMMS_FOREVER_EMOTES/` (00_DESIGN, 01_EXECUTION_PLAN,
  06_SMOKE_TESTS, 07_EXECUTION_RECORD, RESUME.md, checkpoints.tsv, inputs/owner-rulings.md, plan-data/
  {items.tsv, exceptions.tsv, resume-state.sh}). Single-repo ports kept the plan in the addon:
  `DropWatcher/docs/superpowers/plans/2026-11-13-drop-watcher-forever-port/` and AuraMaster's (RESUME, items,
  checkpoints, exceptions, resume-state.sh).
- items.tsv header (latest): `id milestone repo title` (`SYNC_FOLLOWUPS/plan-data/items.tsv:1`); QC's richer
  `id milestone repo title deps effort smoke source`.
- resume-state.sh (23 lines, `SYNC_FOLLOWUPS/plan-data/resume-state.sh`): done = subject matches
  `(^|\+ )<ID>(:| \+)` on the run branch since the run date, or on the default branch after merge, or a row in
  exceptions.tsv; prints per-repo branch and dirty count.
- checkpoints.tsv: `checkpoint date evidence` (totals both profiles, lint, heads). DW's rows record
  `retail N/0/x, forever N/0/y, lint 0/0, TOC 120105, 16001` (`DropWatcher/.../checkpoints.tsv`).
- RESUME.md steps: state script; interrupted item = read diff, finish or stash, never reset; relaunch; checkpoint
  gate + push + row; finalize in dependency order after owner smoke (`QUICKCOMMS.../RESUME.md:1-13`).
- Commit ids: DW used `DW-FP00` (research/design/plan) .. `DW-FP22`, with `DW-FP: Checkpoint Mn` commits and
  `Review fixes:` follow-ups under the same id.

## 4. Gaps / open questions this research leaves (I)

- Whether LH/BL owe a seed-validation pipeline (clients-§10 SHOULD) depends on whether they ship id seeds; not checked here.
- CurseForge: does the CurseForge packager tag `120105, 16001` for both 517 and 88568? Unproven; nothing to change
  in `.pkgmeta`; the owner's first release after the port settles it.
- BankLedger's 5 forever-profile failures exist **today** without any port, so the port's first test item fixes them.
- Name-key decision: keep Retail `Name-Realm` (DW precedent, no migration) vs move Retail to AceDB `Name - Realm`.
