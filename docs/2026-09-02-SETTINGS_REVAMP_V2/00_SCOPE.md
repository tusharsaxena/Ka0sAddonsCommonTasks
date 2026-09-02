# Settings revamp v2 — scope and decisions

Opened 2026-09-02, on the branch `feat/settings-revamp-v2` across twelve repos: the nine Ka0s addons,
plus `LibKa0s` and `WowAddonStandards` upstream, plus this one for the record.

This is the pass **after** `docs/2026-09-01-SETTINGS_REDESIGN`. That one established the tab strip and
the page banner and proved them out on one addon. This one takes the rules that pass discovered,
makes them normative, gives the library the surface to make them cheap, and adopts them everywhere.

## What is being changed

### Cross-cutting, upstream first

| # | Rule |
|---|---|
| 1a | Every addon's General page opens on a tab named exactly **Master controls**, carrying whichever of the canonical rows apply: enable, general visibility, master scale, master alpha, lock frame, debug console, reset position, reset all settings. |
| 1b | **Every** page draws a tab strip — one tab is still a strip. The Profiles page is the only exemption. |
| 1c | Every colour picker anywhere gains a **Use class color** companion checkbox beside it, defaulting off. |
| 1d | Font controls always appear together: face, size, colour, use-class-colour, flags, shadow. |
| 1e | Border groups always carry: style, thickness, colour, use-class-colour. |
| 1f | Bar groups always carry: `[texture][opacity]` then `[colour][use class colour]`. |
| 1g | A tab mixing control types breaks them up with subsection headers. |
| 1h | The drag-and-drop widget owns its chrome — the handle and the per-row bounded box. Row contents stay the consumer's. |
| 4c | The tab-strip wrap bug: on a strip that wraps to several rows, selecting one particular tab opens a gap between the rows and shifts the container below. Fixed in the library, guarded by a regression test and a normative rule. |

### Per addon

- **Absorb Tracker** — master controls; the Bar tab re-laid out.
- **Bank Ledger** — master controls; the Filters page folded into General as tabs, then retired.
- **Consumable Master** — master controls (the General page has no tabs at all today); the AIO Health and
  AIO Mana tabs get the drag-reorder controls the other category tabs already have, scoped within the
  In Combat and Out of Combat subsections rather than across them; the wrap bug; Stat Priority's four
  secondary dropdowns become one drag-reorder list under a full-width primary dropdown.
- **KickCD** — Annotations re-laid out and given a font shadow; Cast bar > General split into
  *Size and position* and a new *Icon* tab; a font colour on Cast bar > Font; a tab strip and the
  drag-reorder widget on the Spells page; and an answer to why *Label text* renders empty.
- **Loot History** — master controls; the Filters and AH price pages folded into General, then retired;
  Price Sources ranked by dragging instead of arrow buttons.
- **Panel Master** — Create and Edit lifted above the tab strip, where they belong, and the now-redundant
  inner box around the panel controls removed.
- **Pretty Chat** — a nested secondary tab strip, one tab per rewritten string inside each category; the
  Test button prints to the debug console rather than to chat.

## Decisions taken up front

1. **Which class does "use class color" mean?** The **tracked unit's** class where the control is
   unit-scoped — KickCD's and Absorb Tracker's per-unit frames — and the **player's** class everywhere
   else. A unit whose class will not resolve (an NPC, an empty target) falls through to the stored
   swatch, never to a default grey.
2. **How far the release goes.** Branch and commits only. Every repo stays on
   `feat/settings-revamp-v2`, pushed as work lands. No version bumps, no merges to master, no tags —
   those are a separate, gated act.
3. **What Master controls must hold.** The tab is mandatory and its name is exact; its contents are the
   applicable subset. A frameless addon omits the frame rows rather than growing a frame to fill them.
4. **Pushing.** Incremental, to `origin`, as each repo's work lands. No PRs.
5. **Tagging LibKa0s.** Taken mid-pass, because the nine addons' vendor-sync tests compare their
   vendored copy against `git show v1.24.0:` in the library checkout, and an untagged library fails
   two tests in every addon. `v1.24.0` is tagged and pushed. This is the one place decision 2 gives
   way: the library is released so that the addons consuming it can be tested at all. Confirmed
   correct by the payload matching the tag byte-for-byte — Multi Meters went to 1458/1458 the moment
   the tag existed, with no other change.

## Record

- `01_UPSTREAM.md` — the library and standard changes, as designed and as built.
- `02_ADOPTION.md` — what each of the nine addons actually changed.
- `03_VERIFICATION.md` — the test batteries, and what the independent verifiers found.
- `04_OPEN.md` — anything deliberately left, and why.
