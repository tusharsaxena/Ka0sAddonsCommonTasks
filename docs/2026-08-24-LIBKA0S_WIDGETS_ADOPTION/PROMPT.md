# Drop-in prompt — adopt `LibKa0s-Widgets-1.0` in this addon

Paste everything below the line into a session opened **in the addon's own repo root**. It is written to
be pasted unchanged into any Ka0s addon; it decides for itself whether this addon should adopt at all.

Written 2026-08-24, out of the two adoptions that already happened: BankLedger (`modules/Browser.lua`,
the file the widget was lifted FROM) and MultiMeters (`modules/Export.lua`). Current library release at
writing: **v1.11.2, Widgets minor 3**.

---

Adopt `LibKa0s-Widgets-1.0` — the collection's shared flat dropdown — in this addon, **if and only if this
addon has a control that genuinely wants one**. Read `../LibKa0s/docs/api/Widgets/version-3-docs.md` first
and treat it, not this prompt, as the contract.

## Step 0 — Decide whether to adopt at all, and be willing to say no

Find every menu-shaped control in this addon: `UIDropDownMenu*`, `MenuUtil.CreateContextMenu`,
`NS.Compat.OpenContextMenu`, any hand-rolled popup with pooled rows, any button whose OnClick shows a list.

Adopt for a control that is **a labelled selector in a form or a filter bar** — it shows the current value,
the player clicks it to change that value, and the list is short and known.

**Do not adopt** for:
- A **context menu** — a right-click action list, or a mark in a header strip whose list is built from live
  client state and carries dividers. MultiMeters keeps `Compat.OpenContextMenu` for exactly this and says
  so in `docs/ARCHITECTURE.md`; the two mechanisms are meant to coexist.
- A control needing something the major does not have: a search box, keyboard navigation, scrolling for a
  long list, sub-menus, per-row disable, or restyling after construction. All of those are listed as
  deliberate absences and none is coming without a caller.
- **Nothing at all.** Several addons in the collection have no such control. If that is this addon, say so,
  name what you looked at, and stop — do not convert a context menu to justify the exercise.

Report the candidates with `file:line` and your recommendation per candidate **before touching anything**,
and wait for a decision.

## Step 1 — Vendor the library

`/wow-addon:revendor-libka0s` if it is available; otherwise by hand, both payloads, from the newest tag:

```sh
cp -r ../LibKa0s/LibKa0s/. libs/LibKa0s/
diff -r --strip-trailing-cr ../LibKa0s/LibKa0s libs/LibKa0s   # content — MUST be empty
diff -r ../LibKa0s/LibKa0s libs/LibKa0s                       # bytes  — SHOULD be empty
```

Then, in the **same commit**: roll the provenance line in the root `CLAUDE.md`
(`Bundles [LibKa0s](…) vX.Y.Z (MIT).` — `CLAUDE.md`, never `README.md`), and add `Widgets.lua` to the
`libs/LibKa0s/LibKa0s.xml` load list if this repo's copy predates it. The vendor-sync cases compare against
the **tag** the provenance line names, so a line naming a tag that does not exist on origin is 2 red cases.

**Never edit anything under `libs/` or `tests/_kit/`.** A defect there is fixed in LibKa0s, bumped, and
re-vendored — a local patch is silently reverted by the next copy.

## Step 2 — Wire it, soft-optional, like every other LibKa0s seam

```lua
local W = LibStub and LibStub("LibKa0s-Widgets-1.0", true)
```

`nil` is a real state and must be handled: **refuse to draw the surface**, never build a dead control that
opens no menu. Both shipped consumers refuse. If this addon's `nil` path prints, print through its existing
`NS.LIBKA0S_MISSING` / shared cause clause rather than inventing a second sentence.

Art and fonts are **parameters**, because a vendored copy cannot know which addon folder it sits in and
`Media.Icon` needs that name. Resolve on this side and hand over — one factory, not a call site per
dropdown:

```lua
function NS:MakeDropdown(parent, width)
  if not W then return nil end
  return W.Dropdown(parent, width, {
    chevron   = NS.Icon and NS.Icon("chevron-down"),   -- falls to Blizzard's arrow if absent
    check     = NS.Icon and NS.Icon("confirm"),        -- multi-select tick; falls to Blizzard's
    glyphFont = C.FONT_MONO,                           -- ONLY if a row will carry `glyph`
  })
end
```

Then per instance: `SetOptions`, `SetMulti(true)` for a filter, `SelectValue` / `SetSelected` to seed it,
and `onSelect` / `onMultiSelect` for the write. Options are `{ value =, label =, color =, glyph = }`.

## Step 3 — The four things that have already gone wrong

1. **`glyphFont` is a precondition, not a decoration.** An option carrying `glyph` with no face named draws
   nothing — the column is dropped. Pass `C.FONT_MONO` (or this addon's equivalent) whenever any row will
   carry a glyph, and do not pass a proportional face: the row font has no ▲/▼ and renders a box.
2. **Call `W.CloseMenu()` from every non-click close path.** The popup is a process-wide singleton parented
   to `UIParent` at `FULLSCREEN_DIALOG`, shared with every other Ka0s addon's dropdowns. Your frame's own
   `Hide()` does not reach it. Miss this and closing your window by Escape or a slash command leaves a menu
   floating over the game with nothing left to hide it. Wire it on `OnHide` and on any explicit close.
3. **Strata.** Put the frame that owns the dropdowns **below** `FULLSCREEN_DIALOG` — `DIALOG` is what
   MultiMeters' export modal uses — so a click outside an open menu closes the menu instead of landing on
   your frame.
4. **The rows are pooled across every dropdown in the process, and across addons.** Never stash state on a
   row and never read anything back off one; everything the widget shows comes from the options you set.

## Step 4 — Test it, and test the creation, not just the paint

TDD: characterization test first, red before green. Then, specifically:

- A case that drives the **real** widget through a **real** row build — not a hand-seeded stand-in row.
  v1.11.0 and v1.11.1 shipped a crash on the first click (`FontString:SetText(): Font not set`) that 553
  green library cases sailed over, because every case seeded stand-ins and none reached `makeMenuRow`.
- A case for the **degraded** path: library `nil`, surface refuses, addon still enables end to end.
- If your mock is friendlier than the client, fix the mock. A `FontString` with no font must raise on
  `SetText`; a `CreateFontString` that answers with the frame itself conflates a label with its glyph.

Green gate before every commit: `lua tests/run.lua` and `luacheck .` (0/0).

## Step 5 — Sweep the docs, because none of this is visible to a suite

- `docs/module-map.md`: the converted file's dependency list must name `LibKa0s-Widgets-1.0`, and say
  whether it is looked up directly or through a `core/*Setup.lua` seam.
- `docs/ARCHITECTURE.md`: if it claims some Blizzard menu API is "the only menu wired", that claim is now
  false — record which control kept the context menu and why.
- `docs/smoke-tests.md`: add the in-client checks no headless suite can make — the menu opens on the first
  click, it closes on Escape and on a slash-command close, two of this addon's dropdowns do not fight, and
  a glyphed row shows a glyph rather than a box.
- Any prose restating the bundled version (`DEPENDENCIES.md`, a media doc) — a version written in prose does
  not move with the copy.

## Step 6 — Finish

`/wow-addon:finalize`. Do not tag this addon and do not bump its version for a re-vendor; that is
`/wow-addon:bump-version`'s job and a separate, deliberate act.

## If the library is missing something

Do not work around it locally. Report it, and let it become the next `Widgets` minor upstream — both patch
releases so far (`CloseMenu()` at v1.11.1, the font template at v1.11.2) came from an adopter hitting the
gap in exactly this step.
