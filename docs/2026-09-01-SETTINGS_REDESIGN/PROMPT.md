# Drop-in prompt — redesign this addon's settings panel

Paste everything below the line into a session opened **in the addon's own repo root**. It is written to
be pasted unchanged into any Ka0s addon; it decides for itself how much of it applies.

Written 2026-09-01, out of the pass that was actually executed on **MultiMeters** — nine pages, 137 rows
before and 154 after, taken from untabbed sections to a consolidated tab strip and then through four
rounds of UX work. Every rule below is one that pass either established or was corrected by; none of it is
speculative. Standard at writing: **v2.37.0**, which is the release that added `options-ui-§13` (the tabbed
page) and `§14` (the page banner). Library at writing: **LibKa0s v1.23.0**.

The reference implementation is `MultiMeters/settings/Schema.lua` and `MultiMeters/docs/settings-panel.md`.
Read them when a rule here is unclear — but **do not copy that addon's tab layout**. Its pages are its own.

---

Redesign this addon's settings panel. There are two halves and they are not the same work: **reorganization**
(what is a tab, what it is called, what order it is in) and **UX** (what the controls look like, what they
offer, and which chrome literals should have been settings all along). Do both, in that order, and measure
before you move anything.

## Step 0 — Inventory first, and print it

Do not change anything until you can show the current state as a table.

Read `settings/Schema.lua`, `docs/settings-panel.md`, `docs/schema.md` and every file in `settings/`. Then
print, per page: each tab in strip order, each row in declaration order, and the row count per tab.

Derive the counts **from the schema**, never from the docs — the docs are what you are about to check.

Then answer these, with evidence:

1. **Is this addon tabbed at all?** `H.RenderTabbedSchema` means yes; `H.RenderSchema` means the page draws
   scrolling sections with headings. If it is untabbed, adopting `§13` is the first change and it is usually
   a one-line edit per page file — the `group` field already declares the sections.
2. **Does every window-scoped page draw the banner (`H.WindowBanner`)**, and is the banner the **only**
   window picker in the panel? `§14` requires it to replace a picker, never mirror one.
3. **Does this addon have per-window settings at all?** Several do not. An account-wide addon (no `profile`
   section in its AceDB, everything in `global`) has no active-window state, no banner and no
   window-relative paths, and Steps 1–2 still apply while the banner rules do not.
4. **How many pages, and does any page carry fewer than two visible tabs?** A single-group page falls back to
   `RenderSchema` and draws no strip — that is the library's behaviour, not a bug, and it is why a page whose
   sections you are about to merge into one may lose its strip entirely.

Report the inventory and stop for a decision **if** any page would lose its strip, or if the addon is
untabbed. Otherwise continue.

## Step 1 — The tab strip

`RenderTabbedSchema` partitions a page's rows by `group`, **in declaration order**, and draws one tab per
distinct group. So the schema array's order *is* the tab order, and a group's rows **must be contiguous** —
a row filed under a group the page has already left prints that heading a second time further down.

### What is a tab

**One tab is one subject, not one drawer.**

- **A tab holding fewer than two visible controls is not a subject.** Merge it into the tab whose subject
  contains it. The exemption is a tab whose stored row sits beside **bespoke** controls that have no path
  and cannot be counted — a picker, a create/delete button pair. Exempt those **by name** in the test, never
  by loosening the rule.
- **Two tabs that are halves of one question are one tab.** MultiMeters had *Rows* and *Row behavior*, four
  controls each, one subject between them; and *Window buttons* and *Meter buttons*, which split eight
  toggles for eight icons in one strip by what they act on — a true distinction and a useless one to click
  through.
- **A tab that exists to hold a checkbox and two buttons is not a subject either.** Retire it and hang the
  buttons off the tab whose subject they belong to.

### What a tab is called

**A tab name must not repeat what the page already says.** On a page called Bars, *Bar background* and
*Bar border* become **Background** and **Border** — every tab there is about the bar, so the word carried
nothing. On a page called Tooltip, the tab called *Tooltip* becomes **General**.

Watch for the inverse: on a page where two surfaces coexist, the qualifier is doing real work. The Tooltip
page's *Bar background* keeps its word, because the tooltip has a background of its own that the bars' is
not.

### What order the tabs are in

- **First is what a player reaches for when they open the page.** Usually a General tab: the master toggles
  and the page-wide shortcuts.
- **Last is what they set once and leave.** A contents/inclusions tab, an export tab.
- **Tabs read together sit adjacent.** Three bar tabs (fill, background, border) belong in a run; a text tab
  wedged between them makes a reader cross it twice.

Moving a tab means moving its whole run of rows in the array. Keep each group's leading divider comment with
its group.

## Step 2 — Row order inside a tab

The flow engine pairs **consecutive rows two per line**, so declaration order is layout. This is the half
that is easiest to skip and most visible in game.

- **Pair a mode with the thing it modes**: `[text color mode] [text color]`, not the mode three rows up.
- **Pair rest with hover so the reader goes across, not down**:
  `[control color mode] [control hover color mode]` / `[control color] [control hover color]` /
  `[control opacity] [control hover opacity]`. Reading down a column is one state; reading across a line
  compares the two, which is the question someone setting a hover actually has.
- **A master toggle leads the thing it governs**: `[show icon] [icon position]` / `[icon size]`.
- **Make the text tabs agree with each other.** If this addon has more than one text surface (cell text,
  header text, tooltip text, column labels), give them all the same shape —
  `[font] [size]` / `[color mode] [color]` / `[outline] [shadow]` / `[opacity]`. Four text tabs in four
  different orders is the drift a player feels without being able to name.
- A `solo = true` row breaks onto its own line. Use it for a genuine pivot, not for spacing.

## Step 3 — The UX conventions

These are collection-wide and are the half most likely to be missing.

### Colour modes: the legal set follows what the surface IS

- A surface that belongs to **one column** may offer `stat` (per-statistic).
- A surface that spans the **whole window** — a title bar, a divider, a window background — **may not**.
  Per-statistic there could only ever mean the sort column's colour, which is already on screen in that
  column's own header and in its arrow.
- `class` on a window-wide surface means the **local player's** class, because that is the only class such a
  surface can mean. This is legitimate: state it in the desc rather than refusing the mode.
- Where the **shared skin** owns the accent (`frame.title`, `frame.divider`), offer a `skin` mode, make it
  the shipped default, and have it **write nothing at all** — leaving whatever `NS.ApplySkin` painted. That
  is how a per-window picker coexists with `standalone-windows`, whose rule is *never restate `Core.SKIN`'s
  values*: nothing is copied into the repo, nothing is stored in a profile, and a re-skin still reaches every
  window that has not overridden it.

### Three rules that apply to every mode

1. **The configured alpha survives the mode.** A class colour carries no alpha of its own, so it takes the
   swatch's. Inventing one means the opacity silently changes when the mode does.
2. **An unknown class keeps the configured colour**, never a tenth hue invented for the occasion.
3. **A row read only under one mode is not disabled.** Setting the colour before switching the mode is the
   normal order of operations, and a greyed-out control makes it a two-visit job. `bars.customColor` under a
   non-custom mode is the precedent; say so in the comment.

### Controls that govern an on-screen glyph

Put **the glyph in the label** and run the rows in the **on-screen order**. Eight checkboxes named *Show
lock*, *Show segment picker* ask a player to translate a word back into the picture they were looking at.

Bake it into `label` — the library's `makeCheckbox` reads `row.label` and nothing else, so an `icon` field
beside it is a field with no renderer. Prefix a texture escape, never replace the words:

```lua
local function controlLabel(art, text)
    local path = NS.Icon and NS.Icon(art)
    if not path then return text end
    return string.format("|T%s:14:14:0:0|t %s", path, text)
end
```

`NS.Icon` answers nil on a degraded install, so it must fall back to the plain sentence. Then teach the
localization test to strip a leading `|T…|t ` before checking the key still exists — a row must not lose its
translation by gaining a picture.

### A tab whose effect is conditional says so

If a tab's controls only bite under some other setting, it needs a sentence. Eight colour swatches with
nothing over them read as *the colour of this statistic*, full stop — and someone who sets one and sees
nothing change has been misled by the page, not by the setting.

There is **no before-group hook**; `afterGroup` fires after the group's last row, which is the right shape
for a footnote anyway:

```lua
H.RenderTabbedSchema(c, PAGE, { [L["Statistic colors"]] = afterStatColors })
```

with the note drawn by `H.TextRow`, after an `H.AddSpacer` so it does not read as part of the grid.

## Step 4 — Literals that should have been settings

Grep the render path for magic numbers in chrome: alphas, insets, hairline thicknesses, hardcoded colours,
anything a player might reasonably want to move.

- **Each promoted literal ships as its own default**, so a window that touches nothing is drawn exactly as
  it was. If the default is not the number it replaced, you have changed how every existing install looks.
- **Clamp anything a player can hand-edit.** These come from SavedVariables; an alpha outside 0..1 is not an
  error, it is a control silently drawn at the nearest legal value, which reads as the setting not working.
- **Do not promote a value the shared skin owns** unless you add a mode that defers to it (see `skin` above).
- **A pair of literals is usually a pair of settings.** A hardcoded `0.25` at rest and `1` on hover are two
  answers to two questions; do not collapse them into one slider.
- When one of the pair stops being read in some state, say which and why — *"with fading off there is no
  faded state, so the rest slider is not read at all"* — and pick the fallback the player means, not the one
  the code finds first.

## Step 5 — Overturning a recorded decision

This addon's comments argue for the shape it currently has. Some of those arguments are load-bearing and some
have been outlived. Both cases turn up in this exercise, and the failure mode is leaving a comment that now
contradicts the code.

When you are about to overturn one:

1. **Find every copy.** The same argument is usually in four places: the schema row, `defaults/Profile.lua`,
   the module that reads it, and a doc — plus, sometimes, a test whose *name* asserts the old position.
2. **Split it.** Most of these arguments have two halves and only one has expired. MultiMeters' *"the title
   bar has no colour mode"* was two claims: no `stat` (still true — one strip cannot mean one column) and no
   `class` (overturned — the controls and the divider on the same strip both wear one, so the title was the
   odd one out rather than the principled one).
3. **Rewrite, do not delete.** Say what changed and what settled it. A reader who finds the new behaviour
   with no trace of the old argument will re-make the old argument.
4. **Check the migration ladder.** If a past migration *pruned* the key you are reviving, do not retire that
   step — a profile below that version can be holding a value the new row does not accept. Rewrite its
   rationale to say what the prune is worth now.

**Ask before overturning anything recorded as a documented deviation** (`docs/ARCHITECTURE.md` →
*Documented deviations*) or as a "never will be" in a comment. Ask before changing a shipped default a player
would notice. Decide for yourself on ordering, merging obviously-sub-tabs, and renames that drop an implied
word.

## Step 6 — The ripple

Every one of these was a red test or a stale doc during the reference pass. Work the list.

- **`defaults/Profile.lua`** — a mirror for every new row. `NS.ValidateSchema()` proves the two agree, and it
  is deliberate that the default is stated twice.
- **`locales/enUS.lua`** — a key for every new `label` **and** every new `desc`. The suite checks labels and
  groups; descs are checked by nothing, so they are the ones that go missing.
- **Pure ASCII in every displayed string.** A `\226\128\146` (figure dash) is missing from the settings-panel
  font and renders as an empty box; `\226\128\148` (em dash) is fine. If you want an arrow in a menu path,
  write `>`. Verify any escape you type rather than assuming — this bug ships silently.
- **The partition test** — the page → tab → count table in `tests/test_schema.lua`. Update it with the
  designed numbers; it is the case that catches a row drifting into the wrong tab.
- **Any test that counts rows on a page or names a tab.** Grep the suite for the old tab names.
- **Docs**, all of them, with counts derived from the schema: `settings-panel.md` (the page table),
  `schema.md` (defaults and their arguments), `module-map.md` (per-page row counts, and the ASCII tree,
  which is easy to miss when you have already fixed the table beside it), `ARCHITECTURE.md` (total rows,
  window-relative count, absolute-path enumeration).
- **`smoke-tests.md`** — a check per new control, and per changed default, written so a reader can tell
  whether it passed.
- **Regenerate** `docs/test-cases.md` (`lua tests/run.lua --list > docs/test-cases.md`) and move the README
  `Tests` badge in the same change.

## Step 7 — The gate, and what not to do

```sh
lua tests/run.lua      # must be green
luacheck .             # 0 warnings / 0 errors
```

Both, before every commit. Run `lizard` only to check you have not pushed a function over CCN 15 — it is a
**release** gate, not a commit gate, so do not let it block you, but do notice if this work put a new
function over the line. Extracting a helper is usually the honest fix.

**Never:**

- **Move a path.** A row's page is where it is **edited**; its path is where it is **stored**, and the two
  are allowed to disagree. Renaming `text.size` to `bars.textSize` for tidiness migrates every saved profile
  in the collection for something nobody can see. Every reorganization in this exercise is a `page` and
  `group` change and nothing else.
- **Touch `libs/` or `tests/_kit/`.** A defect there is fixed in LibKa0s, bumped and re-vendored.
- **Bump the version or write a CHANGELOG entry.** `/wow-addon:bump-version` owns both.
- **Break the secret-value rules** if this addon reads `C_DamageMeter` or any restricted API. You may not
  compare, add, key on or `#` a meter value. Concatenating two formatted values goes through
  `string.format` under `pcall`, never `..`, and never `table.concat`.
- **Loosen a test to make it pass.** Twice in the reference pass a test was passing for the wrong reason and
  the redesign exposed it — a padlock fingerprint that read alpha but never the texture path, and a layout
  case that only worked because a default happened to compute back to a constant. Both wanted the test made
  *more* specific, not less.

## Step 8 — Report

Print, in this order:

1. The before/after tab strip per page, side by side.
2. Every new row, with its default and the literal it replaced (or "new setting" if it replaced nothing).
3. Every recorded decision you overturned, with where the argument lived and which half survived.
4. Anything you left alone because it needed a decision, and what the decision is.
5. The gate output, actual numbers.
