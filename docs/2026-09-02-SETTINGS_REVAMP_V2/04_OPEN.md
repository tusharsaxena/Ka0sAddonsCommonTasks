# Left open

## One documented deviation from a MUST

`MultiMeters/settings/Schema.lua:1761` — `window.header.bgColor` carries no class-colour companion.
The argument is in the code and recorded in that addon's `ARCHITECTURE.md`: the title bar is one strip
spanning the whole window, so "per statistic" over it could only ever mean the sort column's colour, a
fact already on screen twice. The same argument previously took the mode off that strip's *text*
background.

This is a good argument, and `options-ui-§17` is a MUST, which makes it a deviation rather than an
exemption. §17 already carves out palette-definition swatches and background palettes; a
window-spanning chrome strip is a third case it does not quite reach. **Either** §17 grows that
carve-out at the next standards harvest, **or** the swatch takes a companion it does not need. I left
it as a deviation rather than deciding a standards question by silently editing one addon.

## Deliberately not done

- **No version bumps on the nine addons, no merges, no tags.** Per the decision taken up front. The
  branches are pushed and waiting.
- **LibKa0s *is* tagged** (`v1.24.0`), which is the one place that decision gave way, and for a
  mechanical reason: the addons cannot test their own vendored copy without it.
- **Minor verifier findings were not swept.** Each addon's verifier logged 3–7 minor issues that
  repair did not address, since repair was scoped to blocking and important. They are in the workflow
  journal at `wf_50fd2350-6ce`. None affects behaviour.

## Not verifiable out of game

Everything here is schema and layout, and the suites assert over the schema — tab names, tab order,
row order within a tab, the companion beside every colour row. What no headless test can see is
whether the panel *looks* right: that the wrap fix actually removes the gap under Food, that Panel
Master's Create and Edit sit where the banner sits on other pages, that Pretty Chat's nested strip
reads as two levels rather than as noise. Each addon's `docs/smoke-tests.md` carries the in-client
checklist.
