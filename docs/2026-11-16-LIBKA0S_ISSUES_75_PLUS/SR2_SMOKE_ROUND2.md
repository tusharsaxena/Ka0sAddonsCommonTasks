# Addendum: smoke round 2 feedback (2026-11-17)

The owner's re-smoke of `SR1_SMOKE.md`, from screenshots of Combat Trail's title bar (the Results mark
hovered) and the skin picker in all nine skins. Each item is done when a commit whose subject starts `<ID>: `
exists on `feat/2026-11-16-libka0s-75-plus` in its repo.

## Owner feedback, verbatim in substance

1. The hover color reads well in some skins and poorly in others. Good: Ka0s Default, Obsidian, High
   Contrast, Ember, WoW Default. Bad: Azeroth, Glass, WoW Midnight, WoW Forever. For the bad ones, make the
   header button's hover color much more distinct from its rest color.
2. One skin draws a much thicker (gold) window border than the others. Make it the same as the other skins,
   with WoW Forever as the reference. Check Azeroth and Ember too.

## Findings

1. Rest is `icon.tint` (the palette's `muted`) and hover is `text.link` (the palette's `accent`). In the four
   bad skins, `muted` is tinted toward the accent's own hue, so hover changes the shade but not the color.
   CIEDE2000 between rest and hover (sRGB, D65):

   | Skin | Rest | Hover | ΔE00 | Owner |
   |---|---|---|---|---|
   | High Contrast | `#A0A0A0` | `#FFFF00` | 37.2 | good |
   | Ka0s Default | `#B3B3B8` | `#FF8000` | 31.6 | good |
   | WoW Default | `#B8B8B8` | `#FFD100` | 30.2 | good |
   | Obsidian | `#9B9BA4` | `#4DB8FF` | 25.0 | good |
   | Ember | `#C7A993` | `#FF7A33` | 20.1 | good |
   | WoW Midnight | `#B4AFC8` | `#B48CFF` | 18.5 | bad |
   | WoW Forever | `#A39E97` | `#C9A07A` | 14.8 | bad |
   | Glass | `#9AA2B3` | `#B69CFF` | 14.6 | bad |
   | Azeroth | `#B8A07A` | `#E2B659` | 12.9 | bad |

   ΔE00 separates the owner's two groups cleanly. The plain CIE76 distance does not (Obsidian is 41 and good,
   Midnight 51 and bad).
2. Window edges (`win.border` plus `win.inner`, the 1px inner rule):
   - WoW Forever: 1px edge, no inner rule (the reference);
   - WoW Midnight: a 2px gold edge plus a dark inner rule, 3px in all (the thick gold one);
   - Azeroth: a 1px dark-brown edge plus a gold inner rule, so the gold line the eye reads sits inside a
     second line;
   - Ember: a 1px edge plus an amber inner rule at 0.45, the same double line.

## Rulings (the lead's, under the owner's standing guidelines)

1. **SR2-L1.** A title-bar control's hover must be clearly distinct from its rest in every skin: ΔE00
   between `icon.tint` and the hover color is **at least 20** (the lowest the owner accepted, Ember's 20.1),
   pinned per skin in `tests/test_skin_defs.lua`. The four bad skins are raised to **at least 25** (about
   Obsidian's level), staying inside each skin's own palette and never red (red is `close.hot`'s). This is
   done by setting `text.link` in those skins; rest (`icon.tint`) does not move. Every consumer reads the token,
   so the addons need no code change, only the re-copy.
2. **SR2-L2.** Window edges follow WoW Forever: one 1px line. WoW Midnight's edge drops to 1px gold with no inner
   rule. Azeroth and Ember drop their inner rule, and their single 1px edge takes the color the eye read as
   their border (Azeroth's gold inner rule, Ember's amber inner rule composited over its edge). Popup, menu and
   tooltip edges are not changed; any still above 1px are listed as an owner call.

## Items

| Id | Repo | What |
|---|---|---|
| SR2-L1 | LibKa0s | Title-bar hover ΔE00 ≥ 20 in every skin; Azeroth, Glass, Midnight and Forever raised to ≥ 25 |
| SR2-L2 | LibKa0s | Window edges 1px like WoW Forever in Midnight, Azeroth and Ember |
| SR2-REL | LibKa0s | v1.105.0 release record amended (unreleased), release battery re-run |
| SR2-<ABBR> | each addon | Re-copy the re-cut tag; gate under every roster client |
| SR2-SMOKE | CommonTasks | The re-smoke sheet, `SR2_SMOKE.md` |
