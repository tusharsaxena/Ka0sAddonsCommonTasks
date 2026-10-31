# Owner feedback, 2026-10-31

Verbatim batch. Screenshots are in `screenshots/`, named by the image number the owner used (4 has a .jpg and a .png).

1. Font drop down in settings and skin picker: preview of the font in the dropdown, LSM (see Absorb Tracker > Appearance > Text > Font [Image #2]).
   - Make this the default for all font pickers in all ka0s addons (add it to standard and LibKa0s if needed).
   - Make this change for all font pickers now.
   - Do the same thing for textures, borders, etc: see what AbsorbTracker does, make that the default (and mark this as a must do in WowAddonStandards, and if needed create custom LibKa0s widgets for this).
2. DpsRace
   - Run Details view, Spell breakdown: remove the 2nd set of column headers and add "Spell" to the first set; "Spell" is the header for the first column in the first set [Image #3].
   - Main HUD (pre race and mid race and post race): add tooltips for all the main elements on the screen.
3. Font changes
   - Obsidian: make the title the same color as the blue primary button background.
   - [Image #4] [Image #5] Ka0s Default and WoW Default skin fonts look the same; even switching between Friz Quadrata TT and Ka0s Prototype makes them look the same. Ship Ka0s Prototype and Ka0s Friz Quadrata TT as part of LibKa0s.
   - WoW Midnight [Image #7]: Segoe UI Semibold (from the WoW install); ship it and its variants [Image #10] as Ka0s xxx.
   - Ember [Image #9]: Emblem; ship as Ka0s Emblem.
   - Azeroth [Image #11]: Open Sans Semibold; ship it and its variants [Image #12] as Ka0s xxx.
   - High Contrast [Image #13]: Doris PP; ship as Ka0s Doris PP.
   - Glass [Image #14]: Avant Garde; ship as Ka0s Avant Garde.
   - Keep all the older fonts in LibKa0s even if not used by a skin.
   - Tell me about licensing for all fonts; remove font licensing text from the base README.md of LibKa0s and all addons. License files stay in the LibKa0s font directory.
4. [Image #6] Change "Skin's own" to "Skin's default".
5. [Image #8] Change the default Font outline to HUD text only.

Answer to the upfront question: "Ship all 4 Segoe weights. Also forgot to mention for all font changes, make sure you do the font size normalization (compared to Ka0s prototype) so they all somewhat fit in the same UX. I will build for Ka0s Default and Ka0s Prototype, but all skins and fonts should fit somewhat in that."
