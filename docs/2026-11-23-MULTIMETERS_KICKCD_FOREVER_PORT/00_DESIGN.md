# MultiMeters and KickCD for WoW Forever: design

Created 2026-11-23. Research: `inputs/research/` (read `critic.md` first: it overrides `SYNTHESIS.md`; `factcheck.md`
overrides the readers). Pins: MultiMeters f1b0d79 (on `fix/2026-11-23-r2-restore-probe-fixes`), KickCD 333cd49,
Forever 1.60.1.71037 (UI 734f065), Retail 12.1.5.70961 (UI ab5cb85).

Branch `feat/2026-11-23-multimeters-kickcd-forever-port` in KickCD and WowAddonStandards (from master), MultiMeters
(from the fix branch) and this repo.

## Owner rulings (2026-11-23)

| # | Question | Ruling |
|---|---|---|
| R1 | MultiMeters mid-fight on Forever | "Nothing. Leave multimeter as retail only." |
| R2 | MultiMeters name room on Forever | "Nothing. Mark multimeter as retail only." |
| R3 | MultiMeters secret number formatting | "Fix on retail only." |
| R4 | MultiMeters wrong-player numbers on Retail | "Fix it now": apply the only-what-is-certain rule to Retail. |
| R5 | KickCD dim when off cooldown but unusable | "Cooldown only" (unchanged on both clients). |
| R6 | KickCD Forever lists | Nine lists, one per class, Pummel first for Warriors. |
| R7 | KickCD control spells | Core plus Rogue Gouge and Warrior Intercept. |
| R8 | KickCD adding spells on Forever | Anything the player or pet knows, plus KickCD's own Forever lists; another class's list takes any spell. |

Standing rulings applied without asking: features absent on Forever, never hidden (clients-4); per-client seed lists
(clients-5); the Forever skin by default (skinning-2); whole two-word names (forever-quirks-4); probe verbs with safe
defaults and follow-ups (2026-11-22 R3, R4); Retail-invisible fixes on both clients, one commit and test each
(2026-11-22 R8); no version bump, tag or release; push at milestones; **no merge without the owner's go-ahead**.

## MultiMeters: Retail only, two Retail fixes

- **Retail only by the owner's decision (R1, R2).** Roster value `Retail`; TOC one number plus
  `## AllowLoadGameType: standard` and `## ExcludeLoadGameType: camelot` (toc-file-§3); README and
  `docs/ARCHITECTURE.md` give the reason (clients-§9): on Forever the meter hides the spec, so numbers cannot be tied
  to players mid-fight, and the owner chose not to ship it there. `docs/forever-quirks.md` stays Not applicable.
- **Secret number text (R3).** For a secret, skip the formatter: `AbbreviateNumbers(v, { config = cfg })`, the
  config built once per mode and trusted only if it renders plain test values exactly; else today's path. The
  decimals setting then applies mid-fight. Retail-visible: its own commit and test.
- **Only what is certain mid-fight (R4).** While the meter's identities are secret, a cell is filled only for the
  sorted column (every row) and for the local player's row; every other cell of another player is blank until
  combat ends, with the existing header note. Retail-visible: its own commit and test. Out of combat nothing changes.

## KickCD: dual client

The synthesis section 3.4 as amended by the critic, with these rulings:
- Seeds `defaults/Spells_Forever.lua` (R6, R7), from a frozen `wowf` 71037 seed run with rulings as data; one row per
  ability family, resolved to the highest known rank; War Stomp 20549 seeded for Warrior, Hunter, Shaman, Druid.
- Brightness follows the cooldown only (R5). A rank family is usable when any known rank is (critic C3), for the glow.
- Admission (R8): the Cooldown Manager gate, its tag, invalidator and diagnostics section are Retail-only.
- Feral Charge resolves its form override and refreshes on `UPDATE_SHAPESHIFT_FORM` (Forever only).
- Both clients (R8 of 2026-11-22): availability through `C_SpellBook`; namespaced spec count, spec id 0 read as nil;
  nil `notInterruptible` reads false; the cast debug dump tests a secret before its type.
- Empower and other Retail-only registrations are gated by declaration. Probe verbs `/kcd debug probe`.
- Existing Forever profiles: add absent class keys only, never re-seed or delete.
