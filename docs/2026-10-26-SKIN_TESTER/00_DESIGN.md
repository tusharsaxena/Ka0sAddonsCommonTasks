# LibKa0sSkinTester: design (2026-10-26)

## Intent

The owner wants to judge the Ka0s skins the way you choose a sofa fabric: pick a swatch and see it on
the real thing. Today the only way to see a skin is to switch Ka0s Loot History's skin and look around
its window and settings. That shows only the elements Loot History happens to use, one tab at a time.

The tester is a Ka0s addon. You type `/st` or `/skintester` and it shows a skin selector and
one window that displays every element a Ka0s skin can paint, so a skin can be judged, and a skin bug
spotted, in one place.

It comes from leg 1 of the skinning run (`docs/2026-10-25-SKINNING/`). The owner's round-1 screenshots
and notes are in LibKa0s `docs/skins/screenshots/2026-10-26-leg1/`. The skin fixes those notes call for
come after this tool, so they can be judged in it.

## Goals

- **One command, one window.** `/st` and `/skintester` toggle the tester window. *(Owner.)*
- **A skin selector.** A row of swatch cards, one per Ka0s skin, each with the skin's name and its color
  swatches, as on the Appearance tab. Clicking a card repaints the whole window at once, with no reload.
  The selected card is marked. *(Owner.)*
- **One skin at a time.** No side-by-side comparison. *(Owner.)*
- **A showroom of every paintable element**, grouped into labeled sections. Each sample carries a small
  caption naming its primitive (for example `Button (primary)`), so a defect can be traced to the code.
  *(Owner approved the grouping as played back.)*
  - **Window chrome:** Shell, TitleBar, CloseButton, Tab and SetTabSelection (two or three sample tabs),
    Footer.
  - **Controls:** Button (normal, primary, disabled), WhiteButtonLabel, StateButtonLabel (on and off),
    PageButton, SquareIcon, EditBox (the library SearchBox with a hint), Dropdown, Checkbox (checked and
    unchecked), Slider.
  - **Lists:** a small table with a SortHeaderBar, a few ListRows (plain, alternating, selected,
    hovered) and a ScrollBar.
  - **Text:** every Text role: body, muted, heading, headingAlt, accent, disabled, link, linkHot and
    title. Also Font and White.
  - **Panels:** Panel, Inset, Card, Divider, Drawer (open and closed), Strip, Cover, NavItem
    (selected and not).
  - **Overlays:** a Tooltip (shown when a sample is hovered), a MenuFrame (a dropdown's open menu), a
    confirm popup, and the library TestStrip.
  - **HUD:** a sample status bar through ApplyBarFill, and IconBorder on a sample icon.
  - **Getters:** GetAccentColor, GetPanelColor, GetFont, GlowColor, ChartStyle and BarStyle are
    read-only and paint nothing. They are shown as labeled swatches, or a short sample line for a font,
    so their values are visible too.
  - **Semantic colors:** every `sem.*` token the skin resolves (about 20, including danger, the bind
    states and the Alt variants), each as a labeled line. No `Text` role reaches them; they are read
    through `Skin:Color`. *(My call: all of them, since this is a portfolio.)*
  - **Fading primitives:** FadeRegions and FadeNineSlice act on stock Blizzard art. Each is shown on a
    stock-template button or frame placed beside a plain one.
- **A sample settings page.** A button in the tester opens a small settings page, built with the
  LibKa0s Options shell, that shows the settings controls in the chosen skin: the nav rail, tabs, a
  heading, a checkbox, a slider, a dropdown and a color swatch. *(Owner approved.)*
  - **It does not include the library's own Appearance tab.** That tab always draws "Copy to every
    Ka0s addon", which nothing can switch off, so it would let the tester change every other addon's
    skin. The tester's own selector is the only selector. *(My call. A later item can add a hide option
    to the library, and the tab, once the tab's rename to Styles and its new settings land.)*
- **No element missed.** If an element can be skinned but the tester doesn't show it, a skin bug can
  hide there. *(Owner approved this as the failure to avoid.)* A headless test therefore fails if any
  name in `LibKa0s-Skin-1.0`'s `lib.VOCAB` is neither painted by the showroom nor shown as a getter
  swatch. When a later minor adds a primitive, the test turns red until the tester shows it.

## Non-goals

- Side-by-side comparison of skins (the owner declined it).
- Editing or creating skins, or a token inspector.
- Changing any other addon's skin. The tester has no "Copy to every Ka0s addon" action.
- Publishing. The tester is never published on CurseForge. *(Owner, 2026-10-26.)*

## Anti-goals

- An element type that skins can paint but the tester leaves out (above).
- The tester changing how a skin looks. Every skinnable element is painted only through the library's
  public facade (`Skin:For(owner)`) and the library's own widgets, so what you see is what an adopting
  addon gets. The only drawing of its own is the value displays (getter swatches, semantic lines, the
  bar's BarStyle texture and the glow). They are drawn from the owner's tokens and redrawn on
  `Skin:OnLooksChanged`, the way the library's `Widgets.lua` does it (`__onSkin`). *(My call.)*

## Constraints and decisions

- **Repo.** A new git repository at `../LibKa0sSkinTester`, a sibling of the other collection repos,
  with default branch `master`. The owner symlinks it into the game's `AddOns` folder. *(Owner.)*
- **A Ka0s addon in full.** *(Owner, 2026-10-26, replacing my earlier "developer tool" call.)* The
  tester gets a row in the standard's roster (`WowAddonStandards/standards/ADDONS.md`). It is built to
  the whole Ka0s WoW Addon Standard, scaffolded by `/dev-copilot:wow-new-addon` so it is compliant from
  the start. Like every other roster addon, it receives every collection-wide upgrade: LibKa0s
  re-vendors, standards re-vendors, audits and every sweep.
- **Never on CurseForge.** *(Owner.)* The TOC leaves out `X-Curse-Project-ID` and puts the standard's
  one-line comment in its place (toc-file-§1: compliant, with no deviation row). The CurseForge journal
  already skips a roster addon that has no id. The README says it is a developer tool that is not
  distributed.
- **A GitHub repository** at `tusharsaxena/LibKa0sSkinTester`. *(Owner.)* It is public, like the other
  Ka0s repos *(my call)*. Its default branch is `master`.
- **LibKa0s is vendored**, as in every Ka0s addon, from the local `v1.78.0` tag on
  `feat/2026-10-25-skinning`:
  - Both payloads, `libs/LibKa0s/` and `tests/_kit/`, are copied with `git archive`. The CLAUDE.md
    provenance line and the `LibKa0s icons:` declaration are written, and icons are pruned with the
    tag's `tools/prune-icons.lua`.
  - The Ace3 libraries and LibSharedMedia are copied from Loot History's `libs/`, since the Options
    shell and AceGUI need them.
  - "Take LibKa0s as a dependency" (the owner's words) means it is vendored. It is not a TOC
    `## Dependencies` on another addon, because LibKa0s is not an installed addon of its own. *(My
    reading.)*
- **Skin owner.** The tester registers as owner `LibKa0sSkinTester` with label `Ka0s Skin Tester`. It
  keeps its choice in its own SavedVariables (`LibKa0sSkinTesterDB`), and it opens on the last skin
  chosen.
- **Skins listed.** The nine Ka0s skins, in the library's own order (`Skin:Skins()`). EllesmereUI is not
  offered as a source. Its paint is one-way and needs a reload to undo, which defeats quick swapping.
  The settings page's Appearance tab still shows the source choice, as the library draws it. *(My
  call.)*
- **Slash commands.** `/st` and `/skintester` are registered through the library's slash surface.
  `/st` is short, so it may collide with another installed addon. If it does, `/skintester` still works,
  and the tester reports the collision once in chat rather than silently losing it. *(My call.)*
- **What the standard brings with it:**
  - the full doc set;
  - the launcher (minimap button and broker), with the roster's menu entries **Enabled · Show window
    (the showroom)** *(my call)*;
  - the Show window key binding (launcher-§6);
  - the reserved slash verbs, including `diagnostics`;
  - a settings panel.

  The sample settings page above becomes the tester's own settings panel, with the sample controls on
  a page of their own *(my call)*.
- **Green gate**, as everywhere: `lua tests/run.lua` and
  `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`, both 0 failures and 0 warnings, and no authored
  file over 1500 lines.
- **Which LibKa0s it carries.** The tester vendors whatever the skinning run's library tag is when it is
  built. Every later skin fix follows the run's existing re-cut rule (`docs/2026-10-25-SKINNING/RESUME.md`
  §5: the local `v1.78.0` tag moves while it is unpushed), and the tester re-vendors with Loot History.
  So the plan includes a repeatable re-vendor step for the tester, in the same shape as Loot History's
  `LH-RV` items. *(My call, from the run's rule.)*
- **Whose copy runs.** LibStub runs the highest minor of each library file from any installed addon.
  With Loot History installed, the tester may draw from Loot History's copy rather than its own. They
  are the same while both vendor the same tag, and the smoke file says so. *(Builder's note, recorded.)*
- **Combat.** The window can be opened, and skins switched, in combat. The library's repaint touches no
  protected frames. The confirm popup sample is a plain frame, not a StaticPopup.

## Left to the builder

- The window's size and layout: how the sections flow, whether the body scrolls, and where the selector
  sits (top row or left column), as long as all nine cards are visible without scrolling.
- The sample data in the table rows, and the captions' wording.
- How the coverage test reads `lib.VOCAB` and what the showroom records: for example, a list of the
  primitive names it called, kept on the tester's namespace.
- Whether the tester ships a tiny own primitive list for its captions, or reads the vocabulary.
- File layout inside the repo.

## How it is judged

- The owner's in-game smoke test, recorded in this bundle's `02_SMOKE_TESTS.md` when the plan writes it:
  - `/st` opens the window; each card repaints it; the choice survives a `/reload`.
  - The settings page opens and follows the skin.
  - Nothing errors in combat.
  - Every section is legible in every skin, or the illegible ones are recorded as skin defects for the
    next round of skin fixes.
- Headless:
  - the coverage test above;
  - a test that a skin change repaints every showroom element (the paint recorder in kit revision 43);
  - a test that the value displays are redrawn from the new skin's tokens on `OnLooksChanged`.
