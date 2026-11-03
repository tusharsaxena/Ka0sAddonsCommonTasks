# Addendum: DpsRace SavedVariables cleanup (owner, 2026-11-03)

Owner's words: "At the end of the run, schedule a cleanup of my DpsRace saved variables file, where you delete all
entries where the Consumables, and talents, and spell ability timeline have not been captured - essentially, any race
entry which does not meet the latest db standards. But ask me before you do this, since i will need to log out of
the game when you do this."

- **When:** after M3 (R4-GATE), as the run's last step. Not a workflow agent: the lead does it in the main session.
- **Ask first.** The owner must log out (WoW rewrites SavedVariables on logout, so an edit while logged in is lost or
  clobbered). Do nothing to the file until the owner confirms they are logged out.
- **File:** `/mnt/g/Games/Blizzard/World of Warcraft/_retail_/WTF/Account/ADD1KTED2KA0S/SavedVariables/DpsRace.lua`
  (confirm the path, and check for per-character files too).
- **Rule:** keep a race record only if it meets the current DpsRace record schema: consumables captured, talents
  captured, and the spell/ability timeline captured. Read the schema from DpsRace's code (`docs/schema.md`, the record
  builder and the schema version / migrations) to define "captured" precisely, including whether an empty
  consumables list counts as captured (a run with none used is valid if the field exists).
- **Safety:** copy the file to a timestamped backup next to it first; show the owner the counts (kept / dropped per
  character, spec, type) before writing; keep bests and any index consistent (a "Your best" that pointed at a dropped
  record must be recomputed or cleared the way DpsRace itself would); write valid Lua the addon loads; leave every
  non-race key untouched. No temporary harness in the addon repo; use a script in the session scratchpad.
