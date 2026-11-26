# Execution record: owner feedback round 6 (2026-11-27), with round 5's follow-ups

Everything built, reviewed and merged on the owner's standing go-ahead; feature branches (local and origin) and
scratch clones deleted. No tags, no version bumps. In-client smoke is the owner's.

| Repo | Merges | Items |
|---|---|---|
| CombatTrail | 65c78f8, 31b8512, 1d1665f | R5-CT-05..08 (Forever in-combat aura refusal measured, told, tallied) + 3 R5-REV; R6-CT-01 idle HUD keeps the live layout (owner: "Looks good now", recorded a9cd7ee); SD-FIN-06 |
| DropWatcher | 630847c, 81b8239, 20d2045 | R5-DW-12 badge on the right; R5-DW-13..16 Auction/Vendor via optional Auctionator + 3 R5-REV; R6-DW-01 gavel; R6-DW-02 smaller badge; R6-DW-03 help sections; R6-DW-04 "?" unknown rate; R6-DW-05 resize grows the verdict panel; R6-DW-06 no-vendor item with an auction price says Auction; R6-DW-07/08 how-sure score (01_DW_SCORING_DESIGN.md, approved); GLYPH-02 + 3 R6-REV; SD-FIN-06 |
| RangeMaster | 87b8110, a36944e | R6-RM-01 no band behind the picker's group rows; SD-FIN-06 |
| SkillMaster | ed058ba, 8f7607f, 7083d42 | R6-SM-01 Secondary Professions; R6-SM-02 Journal TYPE column, min width 840; R6-SM-03 type colors; R6-SM-04 Alts tooltips, "-" for unlearned; SD-FIN-06 |
| AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, QuickComms, OutfitterReborn | de1d37b, 2b6d34b, 83102b6, a2f1024, 0d08efe, 899a802 | GLYPH-01: help marks `ph:question`; OutfitterReborn's unknown-slot mark `gi:help` |
| 17 addons | SD-FIN-06 merges | docs synced with the code (PGFE, ConsumableMaster: no drift) |

## Owner rulings

- SkillMaster launcher-§6 deviation confirmed (`/sm toggle` opens all windows).
- Scoring: approved as designed; Liferoot Auction 100 right; unknown Hold shows its low number; ranking stays on U.
- Glyphs: help marks `ph:question`; missing-icon fallbacks `gi:help` ("so its different").
- Toss with an auction price → Auction; gavel; "No auction price known" without Auctionator is fine.

## Corrections to the frozen design

- "Keep, U 60, D 0.9 → 50" is 54 by the design's own formula; the code follows the formula. In practice "item info
  loading" reads Hold 17 (data known 67%), not the example's 15.
- Review wording change awaiting the owner: the money line reads "(needs over 10%)", not "(needs 10%)" (Auction
  is a strict greater-than).

## Left open

- Two old, fully merged remote branches the auto-mode classifier would not let me delete:
  DropWatcher `feature/upgrade-glow`, KickCD `feature/glow-options` (0 commits not on master).
- SkillMaster `docs/message-bus.md` owed (13 bus messages, past the more-than-ten trigger); ARCHITECTURE holds them.
- Dead exports reported, not deleted (SD-FIN-06 reports): RM `NS.PresetPickerHolding`; DW `IST.ColumnsOf`; CT 8
  zero-caller members; KC, LH, MM, OR, AM, BL, PFE, PGFE, PC, QC members called only by tests.
- MultiMeters `docs/schema.md` is 1725 lines (docs, cap applies to source).
- Forever deposit rates (5/20/60%) assumed, smoke ITEM-SEARCH-65.
