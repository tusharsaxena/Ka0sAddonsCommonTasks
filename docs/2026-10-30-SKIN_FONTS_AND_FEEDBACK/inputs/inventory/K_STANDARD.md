# K_STANDARD: the WowAddonStandards text this batch touches

Read-only inventory, 2026-10-30. Repo: `../WowAddonStandards`, which is checked out on
`feat/2026-10-30-skin-library-followups` at `4915f78` (v2.92.0, two commits ahead of `master` at `f5e5009`, not yet
merged). The owner's "finalize first" means this run branches from a `master` that already carries v2.92.0, so every
line number below is the branch head's, which becomes `master`. Paths are relative to
`WowAddonStandards/standards/standards/` unless stated otherwise.

## 0. Summary of the touch points

| Owner item | Section today | Change |
|---|---|---|
| 1 overrides reset on skin change | skinning.md:45 (the tab holds overrides) | new bullet in skinning-§3 |
| 2-4, 7 fonts per skin, fewer fonts | skinning.md:72; library-stack.md:430-437 (already stale) | rewrite both; license rule (section 7) |
| 3 Prototype license | no explicit rule; R7 "ship OFL fonts" lives only in the bundle; skinning.md:72 says "under the OFL" | new library-stack-§8 media-terms rule |
| 5 equal widths | skinning.md:73 (geometry invariant); skinning.md:66 High Contrast "larger text" | new width-parity bullet in skinning-§4; table row edit |
| 5 glyphs (image-19) | none; options-ui.md:544 ASCII ` > ` only; options-ui.md:547 MUST `…` | new localization-§7 |
| 6 reset buttons, Scope alignment | skinning.md:45 | wording in §3; alignment has no rule |
| 9 AuraMaster TEST badge | preview-mode.md:11-24 MUST marker; anti-patterns.md:126 (#97) | **conflict**: needs a carve-out |
| 10 hide unselected sections | options-ui: no rule (only `disabledIf`, :545) | new options-ui-§22 MUST |
| 11 anchor title truncation | none (DragHandle mandated nowhere, open-evolutions.md:102-118) | covered by the width-parity bullet, plus a text-fits bullet |
| 11 sim placeholder anchor | preview-mode.md:51; standalone-windows.md:46 | amend: no HUD sim strip |
| 12 `/xx skin` | slash-commands.md:40 reserved list; picker not normative anywhere | reserve `skin`; add a picker bullet to skinning-§3 |
| 13 outline setting | skinning.md:45-48, :92 | new Scope row in §3 and a clause in §6 |

Version: **v2.93.0** (new MUSTs, one MUST narrowed). Section 9 lists the ripple.

## 1. Skinning section (`skinning.md`)

### 1a. Fonts per skin: skinning.md:72 (the "Fonts and art" bullet)

Current:
> **Every skin names its own HUD face** (`hud.font`) ... each Ka0s skin a face the library already ships under the OFL,
> and WoW Default the client's own Friz Quadrata, named explicitly rather than reached by falling back.

"Under the OFL" becomes false once Prototype (personal use only) and Expressway ship. Proposed replacement for the last
sentence:
> **Every skin names its own HUD face** (`hud.font`), so HUD text changes face with the skin as the rest of the addon
> does (owner ruling of 2026-10-30, from `LibKa0s v1.81.0`): each Ka0s skin a face the library ships
> (library-stack-§8, *The skin media*, under the terms recorded there), and WoW Default the client's own Friz Quadrata,
> named explicitly rather than reached by falling back. **A skin's faces are library data**: which face a skin draws
> is set in the library's skin table (Ka0s Default Ka0s Prototype, Obsidian Ka0s Expressway and WoW Forever Ka0s Fira
> Sans Medium from `LibKa0s v1.82.0`, owner ruling of 2026-10-30), and a face that no skin names any more leaves the
> payload in the same library minor (library-stack-§8).

(If the lead prefers that the standard name no face per skin, drop the parenthesis. I recommend keeping it, because
skinning-§4's table already describes each skin, and the Ka0s Default face is a visible change that the rule at
skinning.md:68 has to own anyway.)

### 1b. Ka0s Default is no longer "the look as it was": skinning.md:68

The bullet lists three exceptions (retired `opts.stockDefault`, newly skinned widgets, `q.*`). It already misses the
v1.79.0 change (SO-06: Ka0s Default draws Oxanium and the generated Ka0s Default bar texture, not Friz and the
Blizzard bar). This batch adds Prototype and a default outline (item 13). Append:
> A fourth and fifth are owner rulings of 2026-10-28 and 2026-10-30: Ka0s Default's text face (Oxanium from
> `LibKa0s v1.79.0`, Ka0s Prototype from `v1.82.0`) and its bar texture are the skin's own, not the client's, and
> its text is outlined by default (§3, *Font outline*), so a pin of the client face, the client bar or an unoutlined
> string under Ka0s Default moves.

### 1c. Equal text width across skins (item 5, and the anchor half of item 11): skinning.md:73

Current:
> **Geometry is skin-invariant.** Title-bar height, scrollbar width and every content inset are Ka0s Default's in
> every skin ... options-ui-§8's layout constants hold under every skin.

Add a new bullet after it:
> **Text width is skin-invariant (MUST, owner ruling of 2026-10-30).** Every layout in the collection is built for
> Ka0s Default, so every other skin's default sizes (`font.bodySize`, `font.titleSize`, `hud.fontSize`) are chosen so
> that its faces set a reference string **no wider than Ka0s Default's faces set it**, and not visibly narrower. A
> string that fits under Ka0s Default fits under every shipped skin. The library measures this offline, from each
> face's advance widths over a fixed reference corpus, in the tool that pins the faces, and its suite asserts the
> recorded ratios, so a face or size change that breaks parity fails a test rather than a layout. A fixed-width
> label the library draws (a drag handle's title, a strip, a button) fits its text under every shipped skin, or the
> library widens it. It never truncates it. An addon's own fixed widths are held to the same test under Ka0s Default.

Table row skinning.md:62 reads `contrast | High Contrast | black, white and yellow, 2px edges, larger text`.
"Larger text" contradicts parity. Proposed: `black, white and yellow, 2px edges, heavy faces`. **Lead decision** (Q1).

### 1d. The Skin tab: skinning.md:45-48 (items 1, 6, 13)

Current "What it holds" (:45) lists the source, the skin grid, "the owner's **font and texture** overrides, each led
by the skin's own", the Scope with two check boxes, Copy, and the fixed note. Proposed replacement of the
overrides-to-Scope span:
> ... the owner's **font and texture** overrides, each a dropdown led by the skin's own (*Skin's own (<face>)*), with
> a **Reset font** and a **Reset texture** button beside it that put the override back on the skin's own (no
> confirmation, so no ellipsis, options-ui-§21); the **Scope**, two check boxes, *Ignore settings panel* and
> *Ignore fonts*, and the **Font outline** choice (below); ...

New bullet after the Scope bullet (:46-48):
> - **A skin change resets the overrides (MUST, owner ruling of 2026-10-30).** Choosing another skin, in the tab or the
>   first-run picker, puts the font and texture overrides back on the new skin's own, in the same write. A profile
>   change, the picker's revert and *Copy to every Ka0s addon…* apply the stored values as they are and reset nothing.
>   HUD style values the player set (§6) are not overrides and survive a skin change.
> - ***Font outline*** is a dropdown with three values: *All text* (the default), *HUD text only* and *Off*. It
>   decides where the skin's font flags (`font.outline`, `hud.outline`) apply. It is stored per profile through the
>   write seam like the Scope, and *Copy to every Ka0s addon…* carries it. While *Ignore fonts* is on, the choice is not
>   read and the row says so in its tooltip (options-ui-§21, *Dependent rows*).

Also amend §3's Copy clause "which carries the source, the skin, the Scope and the overrides" to add "and the font
outline".

The Scope alignment in image-30 (the check boxes, then the red Copy button, then the note, with two stray icons at the
right edge) is a library layout defect. options-ui-§6's two-column layout and options-ui-§8's constants already
govern it, so it needs **no new rule**.

### 1e. HUD clause for the outline: skinning.md:92

Append to the *Ignore fonts covers the HUD* bullet:
> Under *Font outline* (§3), *HUD text only* and *All text* let `hud.outline` resolve as the skin states it, and *Off*
> makes it answer `""`. *All text* also applies `font.outline` to every other string the library paints for the
> owner, and *HUD text only* and *Off* answer `""` for it.

### 1f. The picker and the `skin` verb (item 12)

The first-run picker exists only in prose. skinning.md:47 names it as a window, and open-evolutions.md:266 records
ruling O3, "shown to every player". No rule says when it shows or how to reopen it. New bullet in §3, after
*Degradation*:
> - **The skin picker (MUST).** An adopted addon shows the library's skin picker (`O.SkinPicker`, `LibKa0s-Options-1.0`)
>   once per profile, on a profile that has not seen it (owner ruling O3 of 2026-10-29), and again whenever the player
>   types **`/<slash> skin`** (slash-commands-§2, owner ruling of 2026-10-30). The verb opens the same picker in the same
>   state a new profile shows, through the addon's own picker seam, and writes nothing until the player applies. It is
>   not a feature verb: it answers while the addon is disabled, and in combat it prints the refusal `config` prints
>   (options-ui-§2).

## 2. Simulation and test markers (`preview-mode.md`, `standalone-windows.md`)

### 2a. The sim placeholder anchor (item 11, image-46)

What it is: KickCD's `modules/SimStrip.lua:1-26`, a cyan `W.TestStrip(..., { kind = "sim" })` floated over each HUD grid
(and at `UIParent CENTER 0,180` when no grid is on). It reads "Simulation: <scenario> - /kcd sim stop ends it."
(`KickCD/locales/enUS.lua:106`). The other `kind = "sim"` users are windows: MultiMeters `modules/Window.lua`, LootHistory
`modules/Browser.lua` and BankLedger `modules/Browser.lua`, `SessionWindow.lua`.

Current rule, preview-mode.md:51:
> **MUST** mark the session on the display while it runs ... The major's step panel on screen satisfies this. A window
> that marks test mode with the strip **SHOULD** mark a running simulation with the strip's simulation flavor ...

The standard never required the HUD strip. It came from KickCD#38 / OWNER_SCOPE B2. Proposed replacement:
> - **MUST** mark the session while it runs, and the library's step panel on screen is that mark (owner ruling of
>   2026-10-30). A HUD display **MUST NOT** carry a simulation marker of its own, whether a strip, a floating anchor or
>   a badge: during a session the step panel is the one marker on screen. A window that marks test mode with the strip
>   **MAY** show the strip's simulation flavor (`kind = "sim"`, Widgets minor 14, `LibKa0s v1.76.0`) under the same
>   one-marker rule.

anti-patterns.md:126 (#97): delete "and a simulation session whose displays are unmarked", or replace it with "and a
simulation session with no step panel on screen".

### 2b. AuraMaster's TEST badge (item 9, image-35): **conflict with a MUST**

The owner wants the per-container "TEST" placeholder removed. preview-mode.md:11 makes it mandatory:
> **A test mode MUST say so on the display (v2.86.0).** While the explicit test mode is on, every display drawing
> placeholder data **MUST** carry a visible **text** marker ...

AuraMaster's placeholder data is real spell names, so the escape at preview-mode.md:22 (placeholder text that names
the test) does not apply. Removing the badge is anti-pattern #97 unless the rule changes. The measured failure that
motivated v2.86.0 (preview-mode.md:16) was a **window**. Proposed carve-out, appended to the bullet:
> **A HUD display MAY go unmarked (owner ruling of 2026-10-30).** Bars, icons and text the addon draws over the world
> with no window chrome need no on-display marker while the explicit test mode is on: the mode is session-only, ends
> with combat, and is reached only from the player's own switch. A **window** keeps the marker as above
> (standalone-windows, the `TestStrip` bullet).

#97 then reads "...placeholder data drawn **in a window** with no visible text marker...". Other HUD markers that would
fall under the carve-out: DpsRace `modules/Hud.lua` and DropWatcher `modules/CompactChrome.lua` (grep hits for
`"TEST"`, not yet read). **Lead decision** (Q2).

standalone-windows.md:46-48 needs no edit for 2a or 2b. frame-layering.md:17 (T2, "overlaying test and sim markers")
still holds for windows.

## 3. Slash commands (`slash-commands.md`)

slash-commands.md:40, the reserved list:
> `help`, `get`, `set`, `list`, `reset`, `resetall`, `config`, `version`, `debug`, **`enable`**, **`disable`**,
> **`perf`** and **`diagnostics`** are reserved ...

Proposed: add **`skin`** to the list, then append:
> **`skin` opens the skin picker (skinning-§3) and is registered in every addon that has adopted skins**, reserved in
> the rest. It **MUST NOT** be re-used or given an alias, and it is never a feature verb.

slash-commands.md:45, the "never feature verbs" list: add `skin`. No addon registers `skin` today (grep of `{ "skin"`
over the collection's non-vendored Lua finds only test fixtures and diagnostics rows), so nothing collides.

## 4. Options (`options-ui.md`): conditional sections (item 10)

Nothing in options-ui covers hiding rows that a choice does not use. The only conditional mechanism is `disabledIf`
(options-ui.md:545, *Dependent rows*, SHOULD). The library has no `hiddenIf`: `OptionsWidgets.lua:455-461` resolves only
`disabledIf`. options-ui.md:369 is a counter-rule for the page banner: the band's height **MUST NOT** depend on the
selected instance.

Proposed new section `### 22. Sections a choice does not use are hidden (MUST)`:
> Where a dropdown (or a set of check boxes) picks one or more **styles, modes or kinds**, and each value has its own
> group of rows, the page shows the group of **every selected value** and hides the rest, live, by a structural
> refresh of the on-screen page only (options-ui-§11). Two values selected show both groups, in the value list's
> order. This is not *Dependent rows* (§21): a row that only matters while a boolean is on stays visible and is
> disabled. Hiding is for a group whose rows describe an option the player has not chosen. The page banner's band
> (§14) is exempt and keeps its fixed height. The library carries the row key (`hiddenIf`, `LibKa0s` issue to be
> filed); a host **MUST NOT** hand-roll it by re-rendering from its own `onChange`.

Commencement: each addon's next release after v2.93.0. Owner item 10 asks for a LibKa0s issue (the audit across every
addon plus the row key) and for this MUST.

## 5. Anchors and drag strips (item 11, image-43..45)

No rule covers an unlock anchor's label. `DragHandle` is mandated nowhere (open-evolutions.md:102-118, recorded and
not ruled), and frame-layering.md:54 and :75 cover only its alpha and level. The truncation fix belongs to the library
(owner answer). The standard's part is the last two sentences of the width-parity bullet in 1c, which a fixed-width
library label falls under. I do not recommend ruling the DragHandle-mandate question in this batch. Instead, update
open-evolutions.md:102-118 with one line: the per-addon anchor-width issue is filed, and the question is re-checked
when it closes.

## 6. Character set for display strings (item 5's image-19)

The standard has no rule. The only nearby rules are:
- options-ui.md:544: ASCII ` > ` in location strings, never `->` or a triangle glyph.
- options-ui.md:547: "A button that opens a confirmation ends in '…' (MUST) (U+2026)".
- slash-commands.md:131, :277: em dash in help rows. These go to chat in the client's chat font, not a skin face.
- debug-logging.md:49: ▲/▼ allowed as a glyph in its own FontString pinned to JetBrains Mono.
- debug-logging.md:45 still says every other text surface "**MUST** still use stock Blizzard font objects". That has
  been stale since skinning, and skinning-§7 (skinning.md:103-109) does not rescope it. It is worth fixing in the
  same pass.

The image-19 cause is LootHistory `modules/Browser.lua:591`, `"Database \226\137\136 %s"`, U+2248 `≈`.

I measured coverage from each face's cmap (scratch script; the owner's files are in
`_retail_/Interface/AddOns/SharedMedia_MyMedia/font/`):

| glyph | Prototype | Expressway | Fira Sans Med | Philosopher | Atkinson / Nunito / Oxanium | Vollkorn / Bitter / Inter / JBMono |
|---|---|---|---|---|---|---|
| `— – … · • × ° ' ' " "` | yes | yes | yes | yes | yes | yes |
| `≈` U+2248 | yes | **no** | yes | **no** | yes | yes |
| `▲ ▼` | **no** | **no** | yes | **no** | **no** | yes |
| `→ ← ↑ ↓` | **no** | **no** | yes | **no** | **no** | yes |
| `✓` U+2713, `●` U+25CF | **no** | **no** | partial | **no** | **no** | Inter/JBMono only |
| `− ≥ ≤` | partial | partial | yes | **no** | yes | yes |

Friz Quadrata (WoW Default) ships only as CASC `.slug` files and could not be measured.

Proposed new `### 7. Display characters every face draws (MUST)` in `localization.md`:
> A string the addon or the library paints in a skinned face (every string under skinning-§1, chat excluded) uses only
> printable ASCII plus this allow-list, which every face a shipped skin names draws: `—` (U+2014), `–` (U+2013), `…`
> (U+2026), `·` (U+00B7), `•` (U+2022), `×` (U+00D7), `°` (U+00B0) and the curly quotes (U+2018/2019/201C/201D).
> Any other character is replaced with ASCII (`~` or `approx.` for `≈`, `->` for `→`, `x` for `✓`) or drawn as a
> catalog mark (library-stack-§8). A glyph kept for its shape (▲/▼) is drawn in its own FontString pinned to the
> monospace face (debug-logging-§2). Game data the client hands over (item, player and zone names) is exempt. A
> face added to a skin is checked against the list before it ships, and the library's suite asserts it.
> Commencement: each addon's next release after v2.93.0. AUDIT.md gains the grep:
> `grep -rnP '[^\x00-\x7F]' --include='*.lua' core modules settings locales`, plus the `\ddd` escapes, read hit by hit.

If the owner wants strict ASCII (his words were "an ASCII one"), options-ui-§21's MUST `…` has to become `...` in every
addon, which is a large label sweep. **Lead decision** (Q3).

## 7. Font and license rules

What the standard says today:
- STANDARDS.md:11 and toc-file.md:28: the **addon's** license is MIT, and "All Rights Reserved" is forbidden. This is
  about the addon's own code, not third-party assets.
- library-stack.md:430-433 describes the skin faces as "Five OFL display faces ... Barlow Regular and Barlow SemiBold,
  Cinzel SemiBold, and Atkinson ..., each ships ... with its SIL Open Font License 1.1 text beside it". This is
  **already stale**: Barlow and Cinzel left at Media minor 8 (`LibKa0s/LibKa0s/Media.lua:151-156`), and the payload now
  carries Inter, Nunito, Vollkorn, Bitter, Philosopher, Fira Sans, Atkinson, Oxanium and JetBrains Mono
  (`LibKa0s/LibKa0s/media/fonts/`).
- skinning.md:72: "a face the library already ships under the OFL".
- No rule **forbids** a non-OFL face. "OFL only" was owner ruling R7 (`docs/2026-10-25-SKINNING/inputs/OWNER_SCOPE.md:24`),
  and Prototype was dropped on 2026-10-28 for its terms (`docs/2026-10-28-SKIN_OVERRIDES_AND_PICKER/SO06_KA0S_DEFAULT_MEDIA.md:24-38`).
  Both records are in the bundles, not in the standard.

What the three requested files say (their OpenType name tables):
- **Ka0s Prototype.ttf**: "Copyright 2001, free for personal use, freely distributed with Prototype.txt". Distribution
  is allowed only with `Prototype.txt`, which is **not** in the owner's MyMedia folder and has to be sourced. The face
  has no Cyrillic and no full Latin Extended-A, so its mask is western only.
- **Ka0s Expressway.ttf**: "(c) 2005 Typodermic. **Do not distribute.** Report Piracy to piracy@typodermic.com".
  Expressway is a commercial Typodermic face. This is a different case from Prototype: its own terms forbid
  redistribution outright, and the owner's reason ("not making money") does not answer it. **This needs to go back to
  the owner before anything ships** (Q4). Recommendation: an OFL face of the same highway-gothic family instead, such
  as Overpass or Barlow Semi Condensed, rendered beside Expressway the way SO-06 rendered Oxanium beside Prototype.
- **Ka0s Fira Sans Medium.ttf**: SIL OFL 1.1, Reserved Font Name "Fira". This is clean. Cut it from upstream with
  `tools/artwork/fonts.py` at a pinned commit, like the other faces (library-stack.md:472-477, the generators are the
  provenance record), rather than copying the owner's file.

Proposed replacement for library-stack.md:430-433:
> - **The display faces the skins name**, beside the monospace one, listed in `FONTS` with the file recording each
>   face's terms beside it (`license`). The catalog is the list; this standard does not restate it. **A face ships
>   only under terms that allow redistributing it with a free addon (MUST).** SIL OFL 1.1 is the default, and a face
>   under other terms (Ka0s Prototype, free for personal use and distributed with its `Prototype.txt`) ships only on a
>   recorded owner ruling that names the face and its terms (owner ruling of 2026-10-30). The ruling is recorded in the
>   library's changelog and in the README credits of every addon that ships the payload. A face whose own terms forbid
>   distribution never ships, whatever the ruling. **A face no skin names leaves the payload** in the next library
>   minor, together with its terms file. The monospace face stays, because the debug console names it
>   (debug-logging-§2).

Ripple outside the standard: every addon README's font credits, which documentation-§1 governs. LootHistory's
`README.md:151-162` lists OFL faces, according to the earlier PrettyChat inventory.

## 8. Risks

- **Expressway**: shipping it is redistribution of a commercial font against its stated terms, on CurseForge, from
  15 addons. This is the highest risk in the batch.
- **Prototype**: CurseForge's author rewards make "personal use" arguable. The owner has accepted that risk. It is
  still unsafe without `Prototype.txt` beside the file.
- **Western-only masks**: Prototype has no Cyrillic, so a ruRU client falls back to the client face under Ka0s
  Default. That is correct behavior, but it is visible.
- **The marker carve-out (2b)** reverses part of a v2.86.0 MUST. If it is worded loosely, windows lose their marker
  too.
- **Width parity** with no tolerance stated becomes a vibe check. The suite assertion is what makes it auditable.
- **Renumbering**: new material goes in as bullets, plus options-ui-§22 and localization-§7 appended at the end. No
  existing `filename-§N` moves, so the citation check stays green.

## 9. Version bump and ripple (per the repo's CLAUDE.md and the v2.92.0 commits 2e2643b / 4915f78)

1. `standards/STANDARDS.md` line 1 → `(v2.93.0, <date>)`. The v2.92.0 changelog entry moves **verbatim** to the top of
   `standards/CHANGELOG.md`. Write the new entry in the house shape: numbered rulings, each **The finding.** /
   **The rule.**, then **The ripple.**
2. Version stamps: `README.md` `## Status` (:173), `CLAUDE.md` "As of v2.93.0" (:172),
   `standards/EXECUTIVE_SUMMARY.md` "current:" line, `standards/NEW_ADDON_CONTEXT.md` line 1. `check-standard.sh`
   enforces all four.
3. Section bodies: `skinning.md` (§3, §4, §6), `preview-mode.md`, `slash-commands.md` §2, `options-ui.md` new §22,
   `localization.md` new §7, `library-stack.md` §8, `debug-logging.md` §2 (the stale font sentence).
4. `anti-patterns.md`: #97 narrowed (2a, 2b). Decide whether options-ui-§22 and localization-§7 get a number (#109,
   #110) or stay plain MUST findings like options-ui-§21. I recommend no new numbers, matching v2.88.0's precedent.
   Then the index range stays #1–#108.
5. Sections blurbs in `STANDARDS.md` for skinning, preview-mode, slash-commands, options-ui, localization and
   library-stack.
6. `AUDIT.md`: *Check skinning* (d) gains the reset buttons, *Font outline*, the overrides-reset write and the
   `skin` verb. The marker check at about :1031 gains the HUD carve-out. Settings check (l) at :1205 gains §22. A
   localization check gains the non-ASCII grep.
7. `standards/NEW_ADDON_CONTEXT.md`: the reserved-verb list and the skins item (24b, about :1678).
   `EXECUTIVE_SUMMARY.md`: the skinning line (:25). `NEW_ADDON.md`: only if the Skin tab sentence changes.
8. `open-evolutions.md`: close the v1.81.0 follow-up entry (:270-287) once that run merges. Record this run (bundle
   `docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK/`, branch, rulings). Add the anchor-width issue line to :102-118.
9. `bash scripts/check-standard.sh` must exit 0, and CR bytes must be 0 (`tr -dc '\r' < f | wc -c`). Write US English.
10. Commit subject `<ID>: ... (v2.93.0)` on the run's branch, with the session trailers.

## 10. Open questions for the lead

- **Q1, High Contrast "larger text".** Keep it as an exception to width parity, or drop it? *Recommend: drop it.*
  Make its faces heavier instead. Parity is the owner's stated goal, and "no skin truncates" admits no exception.
- **Q2, the TEST badge.** Carve HUD displays out of the v2.86.0 marker MUST (2b), or keep the MUST and give
  AuraMaster one marker per screen? *Recommend: the HUD carve-out*, with windows still bound. It matches the owner's
  "remove it" and the measured case.
- **Q3, strict ASCII or an allow-list?** *Recommend: the allow-list in section 6.* Every shipped face draws it,
  including all three new faces, and it keeps options-ui-§21's `…` MUST. Strict ASCII forces a collection-wide
  label sweep for no visible gain.
- **Q4, Expressway's "Do not distribute".** Raise it with the owner before LibKa0s ships it. *Recommend: an OFL
  lookalike*, unless the owner holds a Typodermic license that allows redistribution.
- **Q5, the sim marker scope.** Remove only HUD sim markers (KickCD), or the windows' sim strips too (MultiMeters,
  LootHistory, BankLedger)? *Recommend: HUD only.* The screenshot and the word "anchor" both point at the floating
  HUD strip, and a window's strip is chrome.
- **Q6, *Font outline* and *Ignore fonts*.** Does *Ignore fonts* also suspend the outline choice? *Recommend: yes*,
  so "ignore fonts" leaves fonts entirely alone. Also, does *All text* outline the monospace debug console?
  *Recommend: no*, and say so in the rule.
- **Q7, the overrides reset and Copy.** Should a skin change made by *Copy to every Ka0s addon…* reset the target
  addons' overrides? *Recommend: no.* Copy carries the source's overrides, so the targets end up matching the source
  exactly.
- **Q8, does `/<slash> skin` answer while the addon is disabled?** *Recommend: yes*, the same as `config`. It is a
  settings surface.
