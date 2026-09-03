# The upstream half — LibKa0s v1.24.0 and Standard v2.38.0

Both landed before any addon was touched, because nine parallel implementers reasoning about four
different libraries during the same week is the failure this ordering exists to avoid.

## LibKa0s v1.24.0

Tagged and pushed. Four majors moved and a fifth file arrived.

**`OptionsCompose.lua` (new, minor 1)** — composers that expand one declaration into a canonical
control group. `FontGroup`, `BorderGroup`, `BarGroup`, `ColorPair` and `MasterControls`. This is what
made rule 1c–1f affordable: the row order, the class-colour companion and the stored-path layout are
decided once in the library instead of nine times in nine schemas, so "consistent" is the default
rather than something nine implementers have to independently achieve.

**The class-colour resolver** — `lib.ClassColor(unit)` and `lib.ResolveColor(stored, on, unit)` in
Core. `nil` is an answer: an NPC, an unresolvable token, a class the palette only half-knows. The
stored alpha always applies, and an unresolvable class falls through to the stored swatch rather than
to a default grey. Only the player's answer is memoised.

**The tab strip is mandatory.** `RenderTabbedSchema`'s single-group fallback is deleted. A page's
chrome had been a function of how many sections it currently held, which meant merging two sections
deleted the strip as a side effect. A page with no grouped rows is now a reported authoring defect
that still renders — a blank page under an empty strip is a worse failure than a strip-less one.

**The wrap bug (4c), root-caused.** The selected tab is cut from `Options_Tab_Active_*` and every
other tab from `Options_Tab_*`, and the client does not draw the two families at the same height.
`TabStrip` seeded the wrap pitch from the first tab it built — `ctx.__tabArtH = ctx.__tabArtH or artH`
— so on a strip that *wraps*, selecting tab 1 packed the rows by the active art instead of the
inactive art. That pitch fed both the row offsets and the reserved chrome band, which is why the
content container below moved and resized too, and why it was invisible on an unwrapped strip: the
pitch is multiplied by `rowCount - 1`, which is zero.

It showed up under **Food** specifically because `ConsumableMaster/settings/Panel.lua:64` puts
`"food"` first in the macro order. Nothing about that tab was special except its position.

The pitch is now measured once, from the inactive atlas, on a throwaway probe. The suite's atlas
harness had been answering a single height for both families — which is precisely why this shipped
green — and now answers a different height per family.

**`ReorderList` owns its chrome** — the hamburger handle and the per-row bounded box. Contents stay
the consumer's. The box defaults on, so a consumer that draws its own row background must delete it
in the same commit as the re-vendor or paint two stacked fills.

### One bug found by reading, not by the workflow

The workflow's own verifier returned `passed: true` for LibKa0s while still logging this, and the
repair loop only fires on failures — so it would have shipped.

`SubTabStrip` drains its ledger on entry, which covers *redrawing* a strip. It cannot cover a page
moving to a tab that draws no secondary strip at all: `SubTabStrip` never runs, nothing drains, and
`ClearScroll`'s `ReleaseChildren` hands the buttons' parent back to AceGUI's pool with them still
shown on it. The next page to take that pooled frame inherits a stack of live buttons over its own
content. Pretty Chat's nested strips would have hit it on the first click away from a rewrite
category.

Fixed at `Options.lua:559` — drain **before** `ReleaseChildren`, while the buttons still have a parent
to be unparented from. Pinned by a test confirmed red under the fix's removal (761 passed / 1 failed).

**Final: 762 tests (+57), 0 lint warnings, max CCN 14.**

## Standard v2.38.0

`options-ui` gains four sections and four amendments.

- **§13** promotes the strip from MAY to MUST, and states the exemption as a *call-graph property* —
  the two pages the flow engine does not render, the AceConfig Profiles sub-page and the host-drawn
  landing page — rather than as a list of names an addon could extend. Carries the wrap-stability
  rule: measure the pitch from an unselected tab, never from a position the selection can move to.
- **§14** generalizes from "the page banner" to "the chrome block": controls applying to every tab sit
  above the strip, in one block, and that block is not boxed a second time.
- **§15** Master controls — the exact tab name, the canonical row table, include-only-what-applies,
  and an explicit MUST NOT invent a movable frame to fill it.
- **§16** the font, border and bar groups and their exact row orders.
- **§17** the class-colour companion, with the resolution rule declared on the row itself, and two
  carve-outs that matter: palette-definition swatches are exempt (a companion beside *Damage done
  color* is a control with no meaning), and a darkened per-class background set is a different set of
  hues rather than the class colour times a constant, so the two must not be substituted.
- **§18** reorder lists: the widget owns the handle and the row box, the consumer owns the contents.
- **§7** gains the non-suppressed subsection heading; **§8** gains the constants that make §13 and §18
  measurable, and now distinguishes the button frame height (37) from the row pitch — two different
  quantities the old single row conflated, which is the exact confusion 4c was made of.

Anti-patterns **#68–#75** append. `AUDIT.md` gains nine mechanical checks, so every new rule is
decidable by reading a schema or running a grep rather than by taste.
