# Completeness critic: MultiMeters + KickCD Forever synthesis

2026-11-23. Read-only. No client and no suite was run. The result is sound in outline (approach B for both addons), but the
MultiMeters identity design, the KickCD "not ready" design and the question list must change before the owner sees them.

Pins: MultiMeters bf67258, KickCD 333cd49, Forever UI 734f065 (1.60.1.71037), Retail UI ab5cb85 (12.1.5.70961), standard 6e062cf.
`MM/` and `KC/` are the pinned snapshots. `D:` is Forever `Interface/AddOns/Blizzard_APIDocumentationGenerated/<Name>Documentation.lua`.

Method: both research code audits and the fact check were read; a scan of every secret-annotated API name against both addons'
shipped files (`work/critic/scan.py`); a client-surface grep of the 13 files no report mentions (11 MultiMeters, 2 KickCD);
code reading of identity, roster, format, export, cooldown, render, cast bar, diagnostics and database paths.

## 1. Must fix

### C1. The identity rule in 3.3 can still show a wrong player's number, and its cost is misdescribed
- VERIFIED: new windows open on **Overall** (`MM/defaults/Profile.lua:653`). The synthesis counts remembered members for Overall.
  That map holds everyone grouped with since the last meter reset, persists across sessions, and holds up to 160
  (`MM/modules/Roster.lua`, INSTALL-5 header, `rememberMember`, `REMEMBER_CAP`). INFERRED: after a few groups all nine classes
  are ambiguous, so "a party of five different classes looks full" (Q1 A) is false under the default window.
- INFERRED from the code, four ways the uniqueness proof fails and mislabels:
  1. a member leaves mid-fight. Current and pinned segments count only the live roster in the design;
  2. a partial roster build (documented at combat start in `build()`) counts one of two same-class members;
  3. the remembered map is incomplete: pruned at 160, or never written, because it builds only when a window reads it;
  4. an ungrouped Ally or an unfolded pet carries the one member's class (U8, U9). `sourceDisplayType` was measured secret
     for a whole pull on Retail (`MM/modules/Aggregator.lua`, comment above `realClass`), so it cannot filter them.
- So Q1 A's "never showing the wrong player's number" is false, by the synthesis's own U8.
- Fix: the safe default is the sorted column plus the local row (`isLocalPlayer`) only. Filling others is an opt-in design with a
  stated residual risk and needs a Current-fight member snapshot, a partial-roster veto and a content limit. MKF-MM-05, 3.3, U8, Q1.
- Visible cost to state: a player with nothing in the sorted column has no row until combat ends. With Deaths as the sort column,
  each death is its own row mid-pull (`identityRow`, `rank_<index>`; existing on Retail).

### C2. "Drawn not ready" does not exist in KickCD
- VERIFIED: `ready = (not isActive) and usable and chargesAvailable(cur)` (`KC/modules/Cooldowns.lua`, `buildSpellState`), but
  `renderState` picks the look from the duration handle only, and `renderIdle` draws full brightness
  (`KC/modules/IconGrid_Render.lua`). `ready` drives only the glow, and both glow triggers default to `never`
  (`KC/defaults/Profile.lua:151,156`).
- So on Forever these all look ready with default settings: cat Feral Charge (3.4 says otherwise), Pummel outside Berserker
  Stance, Shield Bash without a shield, Bash out of bear form, Kick below 25 energy, any kick without mana.
- Q7 asks about a feature that is off by default and misses this one. Replace it (final Q5). A dim look needs a `usable` payload
  field, `plainStateMoved` and `MaterialChange` entries, a render branch and a test that the GCD does not dim.
  UNKNOWN whether usable drops during the GCD. Probe, right after an instant: `/dump C_Spell.IsSpellUsable(6552)`.

### C3. "Highest known rank" gives a false answer for downrankers
- VERIFIED DB2 71037 (`forever-interrupt-data-raw/rows/SpellPower.csv`): Earth Shock costs 30 mana at rank 1 and 450 at rank 7.
  All ranks have a 2 s lockout and share category 19. Spell Lock costs 120 and 200.
- With one resolver for usability, a Shaman at 100 mana reads "not usable" although rank 1 interrupts.
- Fix: texture, tooltip and cooldown use the highest known rank; **usable = any known rank is usable**. Cache the known set at
  rebuild, because the ticker and every poll call it. Add a KickCD perf scenario (the plan has one for MultiMeters only).

### C4. Feral Charge has no refresh edge
- VERIFIED: KickCD registers no `UPDATE_SHAPESHIFT_FORM` (grep; the event is at `D:SpellBook:990`). An override resolved "before
  drawing" goes stale on a form change. Register it through `ForClient({"forever"})`, with the pet and talent events.
- U16 must also read `C_SpellBook.IsSpellInSpellBook(1238122,0,false)` in each form, or the slot may vanish in cat.

### C5. An unguarded secret boolean in the KickCD dump
- VERIFIED: a secret's `type` is its underlying type (standard `client-quirks.md:115`). `NINT_REPORT` is keyed on type and assumes
  a secret falls to the default arm, so a secret `notInterruptible` reaches `"plain value = " .. tostring(v)`
  (`KC/modules/Castbar_Debug.lua:32-62, dumpCastRecord`), and `diagnostics` reuses that dump.
- INFERRED result: a secret string in the report, or a raise at its first compare or table.concat. Test `IsSecret` before dispatch.
  Same item as the header fix (MKF-KC-06).
- Both mocks hide the class: KickCD's `issecretvalue` always answers false (`KC/tests/wow_mock.lua:713`) and MultiMeters models a
  secret as a table. The host mocks need secrets that keep their type.
- Otherwise the scan found no unguarded live read beyond those listed. Low: `Export.TargetName` compares a name with `""`
  before any secret test (`MM/modules/Export.lua:626-634`; `D:Unit` UnitName `SecretWhenUnitNameIdentityRestricted`). Guard it with MM-08.

### C6. Retail changes that no question covers (3.1 says there are none)
| Change | Retail effect | Fix |
|---|---|---|
| MKF-MM-12 creature name on pet spell rows | new text in tooltip and drill-down | Forever only |
| "validate class and spec" in `resolveClassSpec` (MKF-KC-13) | reset, list and remove refuse input they took | Forever only |
| "classes from the per-client table" (3.4) | picker order and source change | Forever only; Retail keeps the client loop |
| resolver through every consumer | must be identity | byte-identical behavior test on Retail |
| same-class/spec mislabel "filed, not fixed" | knowingly keeps wrong numbers | the owner's call, final Q4 |

### C7. The start blocker is still real, and the default contradicts "in parallel"
- VERIFIED again 01:34 IST: no such branch locally, in any sibling's refs, or on GitHub (`git ls-remote`, read-only). Master bf67258
  is the only MultiMeters head.
- The lead resolves it at launch. If it is still absent, ask (final Q0) and do not park half of the request silently.

## 2. Missing decisions (lead's, with the call to record)

| # | Gap | Evidence | Call |
|---|---|---|---|
| L1 | War Stomp reaches only the first character of a profile's creator class | shared "Default" profile (`KC/core/Database.lua:771`), `BuildSpells` appends once | on Forever seed 20549 in the Warrior, Hunter, Shaman and Druid lists; the known filter hides it for non-Tauren |
| L2 | Empower events kept "harmless" while glide events are gated | same evidence class (documented, no emitter); clients-4 counts a registration as a feature | gate both the same way: Retail only |
| L3 | Instance chat export has no feature row | `MM/core/Constants.lua:497`; mm-code INFERRED BG use | port, probe in a battleground |
| L4 | Deaths can undercount in a 40-player raid | `ITERATION_LIMIT = 512` (`MM/core/Secrets.lua:308`); research found it, synthesis dropped it | higher limit on Forever, with a test and the perf scenario |
| L5 | `Targets.ENEMY_LIMIT = 64` can truncate on Forever Overall | mm-code 4.2, dropped | document; probe |
| L6 | Rank-per-id spells in drill-down and tooltip | clients-10; 40-row cap (`MM/modules/DrillDown.lua:126`); whether the meter splits ranks is UNKNOWN | probe after a downranking fight; label ranks only if it does |
| L7 | Role override was dropped | QuickComms ruling R5: talents, player override, saved per character. `Resolve(nil)` has neither step | follow R5: `db.char.role` store and a Forever-only role row. Else record a deviation |
| L8 | Follow-up issue for seeds not checked in game | AuraMaster ruling 5 | add the text to MKF-CT-REC |
| L9 | Forever number fallback skipped `AbbreviateLargeNumbers` | Blizzard's own meter uses it (FC F; `D:Localization:10-13`) | probe it and prefer it over a whole number if it floors |
| L10 | GitHub issue filing is called the lead's | the request authorizes pushes, not issues | write the texts; file after the owner's OK. Tell the owner ConsumableMaster already ships the class-loop bug |
| L11 | KickCD's default visibility rests on U14 | `target_casting_interruptible` (`KC/defaults/Profile.lua:375`) hides the whole grid without a readable cast | U14 is smoke check 1 and the first probe. UNKNOWN still: wago serves no game-rule assignment table (GameMode only, tried on 71037) |

## 3. Plan and probe corrections
- Back up both clients' SavedVariables (owner's step, or with owner's OK) before any checkout switch. The same checkouts load on
  Retail, and AuraMaster's migration reached live data before its commit (patterns 4.5). The plan says only "look again".
- Linked worktrees outside GIT skip vendor-sync, which needs `<root>/../LibKa0s` (`tests/_kit` vendor-sync `DEFAULT_SIBLING`).
  CP-1 requires it to run, so give the worktree parent a LibKa0s sibling at the tag.
- U4 (324 characters) and U7 (258) exceed the 255-character chat limit and cannot be typed. Split them or put them in the probe verb.
- U14 does not test nil. Use `/run local v=select(8,UnitCastingInfo("target")) print(issecretvalue(v) and "secret" or type(v))`.
- U3 must run in a group, with a non-grouped player nearby, and cover Current and Overall.
- MKF-MM-05 also owns the header note, tooltip and death-list paths (`row.deaths`), and a test for each of C1's four cases.
- MKF-MM-11 needs no commit once Avoidable is a lead call (exceptions row).
- 3.2's mock list lacks typed secrets, `IsSpellUsable` per stance or rank, and a partial roster.

## 4. Question list corrections

| Synthesis | Verdict |
|---|---|
| Q1 | false assurance and hidden Overall cost. Rewrite |
| Q2 | keep. Arithmetic checks: 92 to 136 px at 11 px x 0.958 |
| Q3 | four of five are answered by LootHistory ruling R8 (both clients, own commit and test). Ask only the visible number change. Its "2.76M" example is wrong: the default ladder has one decimal (`MM/modules/Format.lua:179-182`); 2.76M is the two-decimal mode |
| Q4 | not a question: parity on a safe default, with a follow-up if contradicted (R3). Lead call: on |
| Q5 | keep. One spec id per class is data; the order and trees are the owner's |
| Q6 | keep. AuraMaster ruling 2 would delegate it, but KickCD's newer, specific `docs/validate-seeds.md` makes CC curation the owner's. Say that the **core** list already has four spells with no cooldown (Cheap Shot, Polymorph, Fear, Mind Control), not only option C |
| Q7 | replace with the unusable look. Glow stays literal (off by default, lead call) |
| Q8 | keep, and say that off the player's own class any spell is accepted, as on Retail |
| new | the Retail mislabel |
| not asked | runes (AuraMaster ruling 3), ranks as one row (validate-seeds "one id per ability", with the clients-10 reason recorded), content kinds (QuickComms R1), names, skin, probe shape (R4), role (R5) |

## 5. Final recommended questions

Settled and not asked: Retail-only features are absent on Forever, Forever has its own spell lists and skin, whole two-word names,
small invisible fixes go to both clients, no merge without go-ahead. Saved Retail profiles are never rewritten.

### Q0. Only if still true at launch: where is the MultiMeters restore-fix branch?
`fix/2026-11-23-r2-restore-probe-fixes` is neither on this machine nor on GitHub.
- **A (recommended).** KickCD starts now. You point to the session or branch, and MultiMeters starts from it.
- **B.** MultiMeters starts from master now and rebases before merge. Conflicts are likely in defaults and skin tests.
- **C.** The fix is dropped, and MultiMeters is built on master as it is.

### Q1. MultiMeters: what does the grid show during a fight on Forever?
Forever hides who each number belongs to, and also the spec, so players can only be matched by class. After combat the grid is complete.
- **A (recommended). Only what is certain.** The sorted column for everyone and all your own cells. Other cells are blank until
  combat ends. A healer with no damage has no row while you sort by Damage. Never a wrong number.
- **B. Also fill likely matches in dungeons and raids.** Only for the current fight and a class that one group member plays. New
  Forever windows open on Current instead of Overall. A five-player party mostly fills and a raid looks like A. A pet or an
  unnoticed leaver could still get someone else's number.
- **C. Fill whenever the class looks unique, everywhere and in Overall.** The most cells. Strangers and past group members can
  cause wrong numbers, and guarding against past members blanks Overall after a few groups.

Start with A; B can follow when the in-game probes prove it safe.

### Q2. MultiMeters: how much room does a Forever name get?
Names reach 25 characters and the column holds 15. A name hidden in combat cannot be shortened, so it is clipped.
- **A (recommended).** 25 characters, window 694 to about 738 px, same number columns.
- **B.** 25 characters, same window, each number column about 7 px narrower.
- **C.** Keep 15: "Samplehunter Mo", whole on hover.

New Forever windows only. Retail is unchanged.

### Q3. MultiMeters: fix mid-fight number formatting on Retail too?
The client refuses to format hidden numbers for addons, so the decimals setting is ignored. Measured on Forever, very likely on Retail.
- **A (recommended).** Both clients. Retail mid-fight numbers follow your format: "24.3M" where it may show "24M", "39" where it may
  show "39.714285714286". If Retail refuses the new route it keeps today's display.
- **B.** Forever only. Retail looks as today and keeps the bug.

Either way, if Forever refuses the route its live rates are whole numbers ("30190").

### Q4. MultiMeters: the port found that Retail can also show a wrong player's number. Fix it now?
Two players of one class and spec, each appearing in different columns during a fight, can swap onto one row.
- **A (recommended).** Not in this port. File an issue and design it separately; the bug stays for now.
- **B.** Apply Forever's rule from Q1 to Retail now. No wrong numbers, but Retail grids become much emptier during fights.

### Q5. KickCD: should an icon dim when the spell is off cooldown but cannot be pressed?
Today brightness follows the cooldown only. On Retail that is nearly always right. On Forever kicks need a stance, shield, form,
energy or mana, so Pummel in Battle Stance and cat-form Feral Charge look ready.
- **A (recommended).** Dim on Forever only. It flickers as energy or rage crosses the cost. The global cooldown does not dim.
- **B.** Keep cooldown only on both. An icon can look ready when it is not; only the optional glow (off by default) knows.
- **C.** Dim on both. Retail's look changes.

The optional glow keeps its meaning, so on Forever it blinks off during the global cooldown.

### Q6. KickCD: one list per class, or per talent tree?
Forever reports one spec per class. The first learned spell is the big icon.
- **A (recommended).** Nine lists, Pummel first for Warriors. A shield tank past 38 may want to reorder.
- **B.** Nine lists, Shield Bash first. Better for shield tanks, worse for everyone without a shield.
- **C.** Twenty-seven lists. Respeccing switches lists, and the saved shape is new, so changing later needs a conversion.

### Q7. KickCD: how many control spells in the default lists?
- **A.** Core: every reachable interrupt plus Forever's versions of what Retail ships. This already includes Cheap Shot, Polymorph,
  Fear and Mind Control, which have no cooldown. Shaman has Earth Shock alone, plus War Stomp for Tauren.
- **B (recommended).** Core plus Gouge and Intercept.
- **C.** Core plus nine: B plus Holy Wrath, Scare Beast, Confounding Flash, Grounding Totem, Seduction, Pounce and Hibernate.

A later change reaches existing profiles only through Defaults.

### Q8. KickCD: which spells may a Forever player add to their own class's list?
Retail takes only what Blizzard's Cooldown Manager tracks. Forever's sets omit Spell Lock.
- **A (recommended).** Anything you or your pet know, plus KickCD's own Forever list. An unlearned talent outside that list is refused.
- **B.** Blizzard's gate, widened to all ranks and known pet spells. Can refuse a spell you know.
- **C.** Any existing spell. A wrong id saves as an invisible row.

Another class's list accepts any spell, as on Retail.
