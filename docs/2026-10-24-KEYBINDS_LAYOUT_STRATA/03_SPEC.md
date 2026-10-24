# The end state

- **015.** Each of the 7 windowed addons appears in Options → Keybindings as its own section titled with its brand
  (`category="BINDING_HEADER_<FOLDERUPPER>"`, no `header=`). Labels are short and drop the brand. The last tab of the
  addon's General page is **Keybindings**: the LibKa0s `O.KeybindingsTab` with two key slots and Clear per binding,
  saving to the set in force (account or character) and re-reading on `UPDATE_BINDINGS` and on show, so both places
  always agree. It refuses in combat. Binding names do not change, so saved keys survive.
- **030.** Every addon follows the standard's `frame-layering` section. Each addon has one `NS.Constants.LAYERS`
  table; levels are set relative to the parent; edit chrome is reachable above its display; windows are toplevel;
  popups sit above their openers; regions inside a display are ordered fill < border < text < overlay. Only the strata
  changes in `plan-data/accepted.json` are made, and no setting key, default or value set changes.
- **020.** Each addon's settings are laid out as the owner approved in `preview.html` (`accepted.json` `layout` ids),
  following the collection conventions in `inputs/LAYOUT_CROSS_ADDON.md`, with no setting changes. Planned as M3.

The per-item specs in `plan-data/items.json` (and its addenda) are binding over this summary.
