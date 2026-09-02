# The adoption — what each of the nine changed

One implementer and one independent verifier per repo, pipelined so each addon verified as soon as it
was built. Six failed verification and went through repair; three passed first time. Every one is
green on its own four-suite gate: lint, headless tests, offline perf, complexity.

| Addon | Tests before | after | delta | blocking/important found | repaired |
|---|---|---|---|---|---|
| AbsorbTracker | 522 | 544 | +22 | 1 | yes |
| BankLedger | 809 | 830 | +21 | 2 | yes |
| ConsumableMaster | 705 | 744 | +39 | 1 | yes |
| KickCD | 788 | 836 | +48 | 1 | yes |
| LootHistory | 663 | 699 | +36 | 2 | yes |
| MultiMeters | 1456 | 1486 | +30 | 1 | yes |
| PanelMaster | 740 | 760 | +20 | 0 | no |
| PrettyChat | 274 | 295 | +21 | 0 | no |
| WhatGroup | 493 | 528 | +35 | 0 | no |

**5,450 tests before, 6,722 after — 1,272 added.** No test was weakened to pass; the verifiers were
told to diff the test files specifically looking for loosened assertions, deleted cases and cases
turned into skips.

## Per addon

**Absorb Tracker** — Bar, Border and Text become composer calls. `showOnlyInCombat` becomes the
four-value visibility dropdown behind a schema-v5 migration that walks every profile in the store,
running after the backfill so the old value wins over the seeded default. Class colour re-scoped from
always-the-player to the bar's own unit. The Appearance page now draws its strip for a mirrored unit
too, with the mirrored state as content under it rather than as a reason to skip the strip.

**Bank Ledger** — Filters folded into General and retired. This addon has no colour control anywhere,
so rule 1c is satisfied vacuously — worth stating, because an inventory that reports "0 colour rows"
looks identical to one that missed them.

**Consumable Master** — the General page gains a strip it never had. AIO Health and AIO Mana get the
drag-reorder the other category tabs already had, scoped *within* the In Combat and Out of Combat
subsections rather than across the boundary. Stat Priority's four secondary dropdowns collapse into
one reorder list under a full-width primary.

**KickCD** — Annotations re-laid out with a new font shadow. Cast bar > General splits into *Size and
position* and a new *Icon* tab; Font gains a colour. The Spells page gains a strip and its list
becomes the shared widget.

*The Label text answer.* It rendered as an empty dropdown because `settings/Label.lua` declared
`units.<unit>.label.text` as `type = "string"` with no `values` and no `dialogControl`, and the
library's dispatch turns that shape into a dropdown with nothing to list. It was always meant to be
free text — you type the label. It now declares `dialogControl = "EditBox", maxLetters = 32`
explicitly, and the re-vendored library warns on the bad shape so the next one announces itself the
first time its page is opened instead of silently rendering an empty control.

**Loot History** — Filters and AH price folded into General and retired. Price Sources ranks by
dragging; the paired arrow buttons are gone, and are now anti-pattern #75.

**Multi Meters** — already drew the target look, so its work was mostly *removal*: `ColumnBlocks`
drops the row background it drew itself now that `ReorderList` paints one, rather than stacking two
fills at the same alpha the library uses.

**Panel Master** — Create and Edit move into the page's chrome band above the strip, where controls
that apply to every tab belong. The inner box around the panel controls then has nothing to
distinguish and goes.

**Pretty Chat** — each category tab gains a secondary strip, one tab per rewritten string, so a
category stops being one long scroll of near-identical five-row blocks. The Test button prints into
the debug console rather than into the chat frame it is in the middle of rewriting.

**What Group** — master controls and the mandatory strip; the smallest surface of the nine.
