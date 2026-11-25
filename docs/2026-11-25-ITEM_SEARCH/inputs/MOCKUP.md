# Mockup (owner-approved, 2026-11-25)

The canvas is https://claude.ai/artifact/SdeXqCBDRn7kUgSyhELR5v (private to the owner). The owner's verdict: "Mockups look
good, go ahead and build this". It has three boards. Rows written in brackets are placeholders.

1. **Item tooltip.** Under the client's own item tooltip and other addons' lines:
   - a separator line in the Drop Watcher skin accent;
   - a magnifier and "Drop Watcher · Item Search" title line, in the accent;
   - **Drops from**: the top 3 sources with their chance, then "and N more";
   - **Sold by**: shown when a vendor is known;
   - **Quests**: `!` in your log, `?` not picked up yet, `✓` completed;
   - **Crafting**: `●` a known recipe, coloured by the skill-up colour, and `○` a recipe you don't know;
   - "Ctrl-Alt-D: open in Item Search".
2. **Item Search window.** Drop Watcher's style, with lock, settings and close buttons in the header.
   - **Left pane:** an "Item name or id" box, a Clear button, the matches (icon, name in quality colour, id) and recent
     searches.
   - **Right pane:** the item header (icon, name, quality, class, subclass, required level, id) and a "Link in chat"
     button, then these sections:
     - **DROPS FROM**: name, level, zone, a bar scaled to the top chance, the %, and a waypoint pin;
     - **QUESTS**: mark, title, zone and state;
     - **CRAFTING**: mark, recipe, profession, then the orange/yellow/green/grey breakpoints and your skill, or "learnable
       at N" for a recipe you don't know, then the state;
     - **ALSO**: Sold by, Reward from, Starts quest, Skinned from.
   - **Footer:** the ForeverDB version and status, and the keybind hint.
   - **Ways in:** the magnifier icon in the main window's header, or the keybind.
3. **Settings, a new "Item Search" page.**
   - **Item tooltip:**
     - on/off;
     - only while holding Shift;
     - the separator and title line;
     - the keybind hint;
     - the sections in order (Drops from, Sold by, Quests, Crafting, Reward from / starts quest);
     - how many drop sources to show (3);
     - hide completed quests.
   - **Item Search window:**
     - bar colour (follow the skin, or custom);
     - row density;
     - font size;
     - the zone and level columns;
     - waypoint pins (TomTom when installed);
     - remember recent searches.
   - **Keybind:** Item Search, Ctrl-Alt-D.
