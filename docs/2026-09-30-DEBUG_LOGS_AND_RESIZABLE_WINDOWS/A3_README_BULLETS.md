# Addendum A3: README uses bullets, never numbered lists (owner, 2026-09-30)

> This is by design - numbered lists dont seem to work in Curseforge's description page, so use bullet
> points instead. Make this change upstream first (standards, wow-addon, etc) and then change all READMEs
> for all addons. After that do a /wow-addon-finalize for all addons.

Scope decided by the owner (question asked): **every numbered list in README.md**, not only Reporting a bug.

## Spec (S7)

1. **Standard v2.72.0 (DL-STD-03).** documentation-§1's CurseForge rendering rules gain a MUST NOT: README.md
   (the CurseForge description) uses **bullets, never numbered lists**, because CurseForge's description page
   does not render them; where order matters the words carry it. Item 9's fixed "Reporting a bug" body becomes
   three `- ` bullets (same words, the slash in place), closing sentence unchanged. Item 6's "a numbered
   pipeline or prose" becomes "a bulleted pipeline or prose". Every other place the standard shows README
   content (templates in NEW_ADDON.md / NEW_ADDON_CONTEXT.md, AUDIT.md's README checks) matches; AUDIT.md
   grades a numbered list in README.md. Full ripple, version bump.
2. **wow-addon (DL-PLUG-02).** Wherever the plugin writes or checks README content (new-addon, sync-docs,
   bump-version, review/standards-audit agents, CLAUDE.md), match v2.72.0: bullets, the bulleted fixed text.
3. **Every addon (DL-AM-05, DL-<XX>-04 for the other ten).** README.md: every numbered list becomes bullets
   (order carried by the words where it matters, no other rewording), "Reporting a bug" is exactly the v2.72.0
   fixed text with the addon's slash (AuraMaster's reworded closing sentence is aligned to it). Update any test
   that pins the README's shape or text (e.g. tests/test_doc_structure.lua, tests/test_docs.lua). Refresh the
   standards reference to v2.72.0 wherever a live stamp names the version. Gate green, reviewed.
4. Then the owner's **finalize** across the collection (standard, LibKa0s, wow-addon first, then the addons):
   doc sync, merge `--no-ff`, gate on the merge, push master, push LibKa0s tag v1.64.0, delete the branches.
