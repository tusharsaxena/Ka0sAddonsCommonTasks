# Owner scope: Ka0s skinning (2026-10-25)

## The brief (owner's words, condensed)

- Add skinning support to Ka0s addons so that they can use EllesmereUI skins. It has been done once already, in
  PremadeGroupsFilterExtension (`core/EUIBridge.lua`, `modules/EUISkin.lua`). Do it for every addon with a visual element.
- Extend it: Ka0s ships its own skins, and today's look is one of them. The user picks a skin, or uses the EllesmereUI
  skin when EllesmereUI is installed and loaded and its third-party skinning is on.
- Use the same skinning format as EllesmereUI, so that skins apply consistently.
- Skins cover every visual element: windows, panels, dialogs and the settings pages, especially the custom LibKa0s
  elements.
- Prototype in one addon, then roll out to every Ka0s addon once it works.

## Rulings

| # | Question | Ruling |
|---|---|---|
| R1 | Skin choice: account-wide or per addon? | **Per addon.** A "copy to every Ka0s addon" action is acceptable. |
| R2 | Do skins reach the HUD (bars, icons, meters), or chrome only? | **Every visual element, HUD included.** |
| R3 | Saved HUD style values when skins arrive | **The chosen skin shows right away**: existing HUD style values reset to "From skin". |
| R4 | Which skins | Nine: **Ka0s Default** (today's look), Obsidian, Azeroth, Glass, High Contrast, Ember, **WoW Default** (the vanilla 1.12 look), **WoW Midnight**, **WoW Forever** (the EllesmereUI-on-WoW-Forever look from the owner's five screenshots: warm charcoal, black title bars with centered white titles, tan accent, gold headings, thin borders). |
| R5 | Prototype addon | **LootHistory.** |
| R6 | Run scope | **Prototype, then stop** for the owner's in-game smoke test. Rollout to the other addons is a second leg. |
| R7 | Fonts | **Ship a few free (OFL) fonts** in LibKa0s media. |
| R8 | Mockups | Saved in the LibKa0s repo for later reference. |

The mockups: canvas https://claude.ai/artifact/Dt32859dvnj1cCWoUkadzj; the token source is
[`mockup-tokens.dc.html`](mockup-tokens.dc.html).

## Execution guidelines (owner)

Ask questions upfront, then decide; ask only when absolutely necessary. A resumable, checkpointed plan. Work on a
branch and commit incrementally. Push to origin after major milestones; never merge without the owner's go-ahead.
After the merge, delete every branch, stash and worktree the run created. Use ultracode (dynamic workflows).

## Research facts the design rests on

- EllesmereUI's skinning API (v9.6.7, `SKINNING_API.md`, API version 3) is a facade of primitives over a small
  token set (accent, panel fill, inset fill, border, font, outline) and two styles (`eui` atlas backdrop, `modern`
  flat). "Blizz Default" in its options means "off". A third-party addon gets one style by majority vote of the user's
  window styles; it cannot choose. The callback fires once per session; removing a skin needs a reload.
- EllesmereUI's license is **all rights reserved**: mirror its API names and token model, never its code or media.
- The WoW Forever client (`IS_FOREVER`) is a separate client; Ka0s addons do not run there yet (LibKa0s#44). The
  "WoW Forever" skin is a look, usable on retail.
