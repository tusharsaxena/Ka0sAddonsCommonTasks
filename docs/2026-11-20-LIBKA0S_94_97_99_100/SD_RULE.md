# SD-RULE: the owner's calls on the audit's UNCLEAR rows (2026-11-20)

The questions are `docs/2026-11-20-SKIN_DEFAULTS_AUDIT/02_UNCLEAR.md` (U-1 to U-31, with evidence and options). The
owner took **every recommendation as written** (2026-11-20), with one change to U-31.

| U | Ruling | Lands in |
|---|---|---|
| U-1 | R-2 supersedes L17: the Callout follows the skin (Skin font, "@skin" outline, glow from skin, shadow companion); a one-time move only for stored values still at the L17 defaults | SD-LK-97.10; Combat Trail calls the key list (SD-SK-CT) |
| U-2 | Callout info/go/stop/warn/error are meaning colors: defaults read `sem.*`, a player's swatch wins | SD-LK-97 (new part, beside .11) |
| U-3 | CalloutSettings plain build is exempt, documented as a fallback no Ka0s host may use | SD-LK-97 (doc note) |
| U-4 | Window chart bars take the skin's gloss under Glass, through the same Texture gloss as the Bar | SD-LK-97.3 (Charts part) |
| U-5 | The skin-switch kit compares each setter family on its own; AbsorbTracker's texture pins stay until it lands | SD-LK-GUARD (97.18 b) |
| U-6 | Kit rows whose cause id is bookkeeping move to named kit categories | SD-LK-GUARD (category if missing); SD-SK-AM, SD-SK-ST rows |
| U-7 | Lines written into a stock client frame (GameTooltip, StaticPopup) read `gtip.title/body/muted` | SD-SK-SM, SD-SK-LH, SD-SK-OR |
| U-8 | R-2 supersedes SF-AM-3: bar fill, icon border and Text-line colors follow the skin, one-time step for stored v17 defaults | SD-SK-AM |
| U-9 | SF-AM-2: the bar background follows the skin; the bar border stays dark (OVERRIDE, owner) | SD-SK-AM |
| U-10 | AuraMaster's text glow stays black in every skin (OVERRIDE, owner) | nothing |
| U-11 | The bar spark is under the A6 game-art Leave | nothing |
| U-12 | AuraMaster's preset role bar colors keep their hues in every skin (OVERRIDE, owner); line in its presets spec | SD-SK-AM |
| U-13 | Bank Ledger's Insights data-fill alphas are a fades-and-dims Leave | nothing |
| U-14 | Combat Trail's HUD fight clock is **not** a race clock: font flags default "@skin" with a FollowOnce key | SD-SK-CT |
| U-15 | The Race detail Timing-strip bands are flat thin bars (A7), Leave | nothing |
| U-16 | Consumable Master's macro bar and flyout edge take the skin's `bar.border` | SD-SK-CM |
| U-17 | Keep CM's near-miss owner tokens under Ka0s Default (button fill 0.6, flyout fill 0.85, flyout shade 0.8), the shade included (OVERRIDE, owner) | nothing |
| U-18 | Drop Watcher's expanded-row wash follows `list.sel` | SD-SK-DW |
| U-19 | Drop Watcher's Edit message box is skinned (skin face, `input.text`) | SD-SK-DW |
| U-20 | The Skin Tester's "Stock" twins stay stock under every skin; recorded as a note or skinValues row | SD-SK-ST |
| U-21 | Fix the library dropdown (skip measuring when a width is given) and drop MultiMeters' in-combat client-menu fallback | SD-LK-97 (new part, WidgetsDropdown); SD-SK-MM |
| U-22 | An outfit glyph with no picked color draws `icon.tint`; a picked color stays the player's | SD-SK-OR |
| U-23 | PanelMaster's new-panel look is the player's content (A8, OVERRIDE, owner) | nothing |
| U-24 | A preview stand-in keeps the host frame's look under every skin: a new skinning-§9 class; PFE's (test) mark reads `text.muted` | SD-STD; SD-SK-PFE |
| U-25 | Pretty Chat's `/pc test` report is not a chat line: its labels read owner tokens following role tokens, and it becomes a switch surface | SD-SK-PC |
| U-26 | Quick Comms' dial slices and hub are shape art; only the tint follows | nothing |
| U-27 | Quick Comms' pad buttons keep the texture-plus-shine look (PLOOK-7) | nothing |
| U-28 | Quick Comms' End-preview button becomes `S.Button` with `btn.*` | SD-SK-QC |
| U-29 | Quick Comms' callout-row violet is a category hue (meaning color) | nothing |
| U-30 | Range Master's Band-mode container border and background are a meaning color (OVERRIDE, owner); SD-SK-RM.4/.6 stay at their Fixed-mode scope and SD-SK-RM.10 stands as a GAP | SD-SK-RM |
| U-31 | **Changed by the owner:** SkillMaster's trainer popup cards get a `list.hover` wash (not the journal rows). Filed as SkillMaster#9, **and built in this run** under SD-SK-SM | SD-SK-SM |

Combat Trail rows SD-SK-CT.3 and SD-SK-CT.6 had no U row and stand as GAP.

## Later rulings

- **U-21, narrowed (owner, 2026-11-20 18:00).** As built in SD-LK-97 Batch B (`0a80ef32`, `fb5b1b2c`), the dropdown skips
  measuring only labels and widths that read secret, not every row where the host gives a width. That fixes MultiMeters'
  in-combat segment picker without clipping long labels in menus whose width is only a floor. The owner accepted the
  narrower form. MultiMeters still drops its client-menu fallback (SD-SK-MM).
