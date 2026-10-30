# Owner feedback, 2026-10-30

Given after the owner's in-game smoke pass of the skin library follow-ups (LibKa0s v1.81.0), in which every check
passed. The screenshots are in `screenshots/`, named `image-NN.png` after the number the owner gave them.

## The batch (owner's numbering)

1. **Overrides reset on a skin change** (image-06). With a Font and a Texture override selected, choosing another
   skin must reset both to that skin's own. Today they persist across skin changes.
2. **Obsidian's font is Expressway.** "Ka0s Expressway" from the owner's SharedMedia_MyMedia; ship it in LibKa0s.
3. **Ka0s Default's font is Prototype.** "Ka0s Prototype", the same source, shipped in LibKa0s. The owner:
   "I am not making money off this addon so License should be fine."
4. **WoW Forever's font is Fira Sans Medium.** "Ka0s Fira Sans Medium", the same source, shipped in LibKa0s.
5. **Equal font sizes across skins.** Every skin's default size should give roughly the same text width, so no skin
   truncates text another does not. Ka0s Default (now Prototype) is the baseline, because every layout is built
   for it; width matters most. Reference: one LootHistory window in every skin, image-17 (Ka0s Default, Prototype),
   image-18 (Obsidian, Expressway), image-20..27, image-28 (WoW Forever, Fira Sans Medium).
   - image-19: some faces cannot draw some characters (footer "Database [] 1.6 MB"). Find every such character in
     display text and replace it with an ASCII one every shipped skin font draws.
   - (The owner's second "5. Change the font of" line was a stray: no other skin changes font.)
6. **Skin tab, every addon.** image-29: a reset-to-default button for Font and one for Texture. image-30: fix the
   Scope section's alignment.
7. **Remove every font no skin uses any more**, so it no longer ships in LibKa0s.
8. **PremadeGroupsFilterExtension.** image-33/34: the expand/collapse button shows text ("up", "down") instead of a
   glyph. image-48..51: the button is misaligned. Some of it is skin-specific.
9. **AuraMaster.** image-35: test mode puts a small "TEST" placeholder next to every container; remove it.
   image-36/37: glow behind the text has regressed and looks bad, worst behind red text.
10. **DropWatcher.** image-38: the Loot rule dropdown is cut off; move it left to fit. image-39: Proc (flipbook) is
    the default upgrade-glow style, main spec color 19FF19, off-spec 3FC7EB. image-40/41: hide the sections the
    style dropdowns (image-42) do not select; with two styles chosen, show both sections.
    - File a LibKa0s issue to check this across every Ka0s addon, and to make it a MUST in the standard.
    - File a DropWatcher issue: stack the toasts when several apply, instead of showing them one after another.
11. **KickCD and anchors.** image-43..45: in nearly every addon the anchor's title is cut off in almost every skin.
    File an issue to check every anchor's width in every addon once the fonts are frozen. image-46: simulation
    mode shows a placeholder anchor ("Simulation: Mythic+ pull, several ki..."); remove it, in every addon that
    has it, with a library change if needed, and in the standard.
12. **`/xx skin`** in every addon opens the skin picker that a new profile shows. A LibKa0s change, added to the
    standard.
13. **Outline by default** for every skin's fonts.
14. **MultiMeters.** File issues: an Insights view; bar animations.
15. **QuickComms.** File an issue (unless one exists): open and close animations for a pad and for the dial, each
    on its own. image-52: in `/qc test` the dial's first level of callout groups has placeholder icons; replace them
    with proper glyphs like image-53's.

## Answers to the lead's questions

- **Finalize first.** The follow-ups run (v1.81.0) is merged and its tag pushed before this run starts; this run
  branches from master.
- **Outline (item 13) is a setting.** A Skin-tab choice of where the font flags apply: All text, HUD text only, or
  Off. The default is All text.
- **Anchors (item 11).** Fix the truncation in the library now, and still file the per-addon width issue.
- **Item 5's stray line.** No other skin changes font.

## Standing guidelines (pasted with the request)

Ask questions upfront, then decide; a resumable, checkpointed plan; a branch with incremental commits; push at
major milestones; never merge without the go-ahead; after the merge delete every branch, stash and worktree the run
created; use ultracode (dynamic workflows).
