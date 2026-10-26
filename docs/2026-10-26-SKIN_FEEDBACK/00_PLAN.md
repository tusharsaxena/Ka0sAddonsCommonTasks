# Skin feedback, round 1 (2026-10-26)

The owner's in-game feedback on the nine Ka0s skins (shared 2026-10-26 with the leg-1 screenshots, now in
LibKa0s `docs/skins/screenshots/2026-10-26-leg1/`), applied to five of them. The owner's words, then the
reading taken and the fix. Branch `feat/2026-10-26-skin-feedback` in LibKa0s, LootHistory,
LibKa0sSkinTester and this repo.

## Scope

In: the five skin notes. Out, for a later round: renaming the Appearance tab to Styles, and the two new
settings (skin everything vs the main window only; skin font vs default fonts). Both are features rather
than skin fixes.

## How it ships

The skins are data in LibKa0s `LibKa0s/SkinDefs.lua`. The v1.78.0 tag is still local and vendored only by
LootHistory and LibKa0sSkinTester, so this extends v1.78.0 as **SkinDefs minor 7** and re-cuts the local tag,
the same route LK-A1..LK-A4 took. Both consumers then re-vendor. No tag is pushed and no version is bumped.

## Items

| Id | Repo | Owner's note | Reading and fix |
|---|---|---|---|
| SF-01 | LibKa0s | Azeroth: "font is not great, very hard to read; doesn't work well with tabs; foreground is too bright, darken/mute it a bit" | The body is the client's font with the client's dark drop shadow on light parchment, which smears ink. Ember uses the same Cinzel titles and drew no note, so the titles stay. Body moves to Barlow with no shadow. The parchment is muted a step darker throughout. Tabs move to light-on-leather (cream text on brown, wax-red when selected), which reads on parchment and on the settings strip alike. |
| SF-02 | LibKa0s | Glass: "too transparent; buttons and tabs look awkward" | Window and popups go from .55/.60 alpha to .88. Buttons, inputs, tabs and drawers drop the radius-8 nine-slice for a flat 1px frosted edge; the window and popups keep the rounded art. Tabs become Obsidian-style: no box, lilac underline when selected. |
| SF-03 | LibKa0s | Obsidian: "looks a bit too much like default; darken it up" | Every surface a step darker (window near #0A0A0B, inputs and title bar near-black), so it reads as black rather than Default's navy. |
| SF-04 | LibKa0s | High Contrast: "borders are too thick on most elements" | Controls go from 2px to 1px; the window edge stays 2px and the popup edge drops from 3px to 2px. Yellow focus and the larger Atkinson type stay. |
| SF-05 | LibKa0s | Midnight: "I don't like the buttons, make them more midnight themed" | The red WoW buttons become night violet under a gold edge with gold text; the primary button is a brighter violet with white text. |
| SF-06 | LibKa0s | | SkinDefs minor 7, the CHANGELOG's v1.78.0 block, the Skin API doc (key 4.6.3.1.1.1.1 -> 4.7.3.1.1.1.1), the case list, and the tag re-cut. The two test pins the notes overturn (High Contrast's 2px controls, Glass's rounded controls) move with them; the WCAG contrast checks stay as the legibility guard. |
| SF-07 | LootHistory | | Re-vendor the re-cut v1.78.0. |
| SF-08 | LibKa0sSkinTester | | Re-vendor the re-cut v1.78.0. |
| SF-09 | this repo | | Execution record and the owner's smoke rows. |

## Smoke (owner)

In the Skin Tester (`/st show`), pick each of the five and scroll the whole window, then open Loot History on
the same skin. Rows in `99_REPORT.md`.
