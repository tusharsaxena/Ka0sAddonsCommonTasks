# Owner feedback round 6 (2026-11-27)

The owner's messages after round 5's follow-ups merged (CT 65c78f8, DW 630847c). Screenshots in `inputs/`
under the owner's numbers. Standing go-ahead: merge each branch once built, reviewed and green.
Branch `feat/2026-11-27-owner-feedback-round6` per repo, built in clones under `~/ka0s-scratch/r6/`.

| id | repo | item (owner's words) | lead call |
|---|---|---|---|
| R6-RM-01 | RangeMaster | "remove that yellow band from headers, looks ugly" (image 35) | Drop the band texture behind the band set dropdown's group headers (R5-RM-01); keep the larger heading font. |
| R6-SM-01 | SkillMaster | "Rename secondary skills to secondary professions" (image 36) | Player-visible label only (the Professions window group, its detached window title, tooltips, settings, docs); saved keys keep their ids. |
| R6-SM-02 | SkillMaster | Journal Log: "a new column Type - skill up, reputation, currency, etc. Increase min width of the window to accommodate" (image 39) | A TYPE column (Skill-up / Reputation / Currency / Standing where applicable) with its own header filter like the others; minimum window width raised so every column fits at the minimum. |
| R6-CT-01 | CombatTrail | "Looks a bit weird out of combat - doesn't seem to line up with the in combat view" (images 37 in combat, 38 out of combat) | The idle HUD keeps the in-combat layout: the target line, the Damage profile section (empty chart), the spell rows' space and the Combat Sequence at the same places, so nothing jumps when a fight starts or ends. |
