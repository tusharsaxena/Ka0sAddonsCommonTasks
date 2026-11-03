# Addendum: PGFE collapsed strip (owner, 2026-11-03, during the run)

Owner's words: "PGFE one more small change - [Image #59] in collapsed mode, there is just a black strip that eppears
below the bottom border - fix this as well plz (can be seen across all skins) - [Image #60] [Image #61]"

- **R5-PG2 (PremadeGroupsFilterExtension):** when the panel is collapsed it is exactly the header band and its edge.
  No strip of body colour or black appears below the bottom border in any skin (images 59 to 61: Ka0s Default, Ember,
  WoW Midnight). Write a test that is red first and measures the collapsed height against the band plus its edges in
  every skin. Add a smoke row.
- It arrived after the run was launched, so it runs as a follow-up step once `plan-data/run.js` finishes, before the
  owner's smoke. It is pushed with its own commit.
