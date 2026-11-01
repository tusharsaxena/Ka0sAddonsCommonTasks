# Plan: smoke feedback on the full skinning run

The owner's smoke feedback of 2026-11-01. Everything is on the existing, unmerged `feat/2026-11-01-full-skinning` in each repo; `docs/2026-11-01-FULL_SKINNING/` is frozen. Images are `inputs/images/<n>.png`, numbered as the owner's message cited them. `items.tsv` holds every item with its image numbers.

Owner's rulings on this batch, 2026-11-01:

- The plan holds every change, and the bugs and skin fixes run first (M1, M2). Features (M3) wait for the owner's weekly limit to reset, and resume from this bundle.
- Lean spend: one agent per repo on a cheaper model, gates on every commit, one review at the end.
- QuickComms: Scale in and Scale out merge into one style, Scale, which grows from small on open and shrinks into the center on close. Their fade versions merge into Scale and fade. The start-large motion goes. Stored picks of a removed style move to the merged one.
- QuickComms: swap the labels of Outward spiral and Inward spiral, which read backwards on Open. Keep Rotate and scale as the default.
- MultiMeters: the export button's glyph is `chat-text`.
- AuraMaster: defaults for every container type: Bar fill use-skin-color off; Text font use-skin-color off; Icon border use-skin-color off. MultiMeters: cell borders off by default in every skin, all other borders stay. Each is an accepted deviation if the standard requires it: record it in that addon's register.
- MultiMeters: bar background opacity 15% for a new profile, never changed by a skin.
- High Contrast: window borders a bit thinner everywhere.
- All skins: a visible separation between header and content, and a separator line. Good: images 65, 66. Bad: 67. Obsidian's rule too dark: 68; good: 69.
- PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat: all smoke passed. DpsRace's existing smoke passed.

- LibKa0s #70, #71, #72, added to M3, 2026-11-02: #72 keeps the anchor in the library, not a documented limit. #71 is a straight fix. #70 is not just retired: the chart gains an area-fill mode and DpsRace's Damage profile moves onto it. Its users today are LootHistory and the Skin Tester; DropWatcher takes it when an Insights tab comes. Close the three issues after the merge, spaced out.

- 2026-11-02: M3 starts straight after M2, not at the limit reset, and the owner smokes everything together at the end.
- Lead's call: AuraMaster's v17 keeps forcing bars' Show border on, because a deliberate off cannot be told from the old default, the owner asked for a border on every bar, and overwriting is accepted. Named on the smoke list.

Order: M1 library, re-cut local v1.85.0. M2 one re-vendor, then each addon's bugs. M3 features, which needs a further library change and re-cut. Nothing merges or tags remotely without the owner's go-ahead. After the merge, delete every branch, stash and worktree the run made.
