# Addendum: MultiMeters export glyph size (owner, 2026-11-04, during the run)

Owner's words: "One more minor change - [Image #67] In MultiMeters, the export button (chat box) is a bit smaller than
all other glyphs in that section, make it the same size"

- **R6-MM2 (MultiMeters):** the export (chat bubble) button in the meter window's header draws at the same visual size
  as the other header glyphs (reset, menu, settings, lock, minimise, close) in every skin. Check both the button's size
  and the glyph's inset or texcoords, because the art itself may have more padding. Write a test that is red first and
  compares the export glyph's drawn size with its neighbours'. Add a smoke row.
- It arrived after `plan-data/run.js` was launched, so it runs as a follow-up step once that run finishes, before the
  owner's smoke. It is pushed with its own commit.
