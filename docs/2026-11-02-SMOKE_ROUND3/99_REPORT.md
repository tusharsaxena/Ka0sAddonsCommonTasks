# Report: the owner's third smoke round

Branch `feat/2026-11-01-full-skinning` in 18 repos (LibKa0s, 16 addons, this one). The branches and the `refs/notes/ka0s-review` notes are pushed. Nothing is merged, no tag is pushed and no version is bumped. The smoke list is `06_SMOKE_TESTS.md`, and nothing on it is marked passed.

## What shipped

- **Library (M1):** R3-DR-1L (the clock font cause, fixed in the paint). R3-L1: AceGUI Dropdown, Ka0sMedia_Font and Ka0sMedia_Statusbar now wear the skinned WowStyle1 look. R3-L2: FadeNineSlice draws a 1 px edge in every skin. R3-L3: IconBorder zooms the icon 0.07 and draws a 1 px outline in every skin. R3-L4: Obsidian's body text is now 12. R3-L5: alternate rows are 8% off the window in every dark skin. R3-L6: Ka0s Ubuntu (UFL) is WoW Default's face. R3-L7: Ka0s Friz Quadrata TT is deleted and stored picks of it migrate.
- **Addons (M2):** R3-RV and R3-FRIZ (re-vendor plus the stored Friz picks moved in 16 addons). DpsRace R3-DR-1 to R3-DR-5: the clocks, a 1:00 default race, Show near a training dummy on by default, the Your best card, and brighter compare bars. KickCD and MultiMeters get the step delay slider (R3-SIM-KC, R3-SIM-MM). R3-SMOKE records the owner's results.
- **Review (M3, R3-FIX):** DpsRace Style.IconEdge now passes the icon, so the zoom crops it. Pixel edges re-size on a UI scale, display or SetScale change. Every skin's icon border is Solid 1px, so the host-drawn borders in KickCD, ConsumableMaster and DropWatcher follow. The zoom now only tightens. KickCD's sim scales the story's times by the pace and never kicks an expired cast, with a test at step delay 4. The verify pass also fixed stale 2 px comments and docs in AuraMaster, DropWatcher, KickCD, MultiMeters, PartyFrameEnhanced and WhatGroup, and added a zoom test in WhatGroup.

## The clock bug

DpsRace's `bigText` gave each clock its own `SetFont` (JetBrains Mono at 26) at creation, and the client lets a string-level font beat any font object. As a result S.HudFont's `SetFontObject` only reached the shadow, and both clocks kept one face in every skin. The headless mock had let it pass because it did not model that precedence. The figures and spell rows never had the cause.

## Totals

- LibKa0s: v1.85.0 release battery `docs/automated-tests/20261103-042609/`. Lint 0/0 in 291 files. 3952 passed, 0 failed, 3 skipped (3955). Complexity max CCN 15, 0 over. Perf is not measured (no `tests/perf.lua`).
- 16 addons, after R3-FIX: 22514 passed, 0 failed, 16 skipped. luacheck 0 warnings / 0 errors in all 16, and no Lua file is over the 1500-line cap. The largest suites are MultiMeters 2547, AuraMaster 2345 and LootHistory 1957; the smallest is PremadeGroupsFilterExtension at 518.
- Across the 17 code repos: 26466 tests passed, 0 failed.

## Tag

The local tag v1.85.0 is at **fd57b83** (R3-REL, the twelfth re-cut), which is LibKa0s HEAD. That tree is clean. The tag is not pushed.

## The PC restart

The PC restarted after the re-cut, the re-vendor into all 16 addons and the addon-side fixes, but before any of them was committed. Recovery went like this. The vendored `libs/LibKa0s` files were compared byte for byte against `LibKa0s/LibKa0s` at HEAD and matched. Each addon's uncommitted work was read and then committed as R3-RV and R3-FIX, and each addon was re-verified green one repo at a time through `ka0s-bounded`. The Skin Tester had one leftover: `docs/test-cases.md` was on disk with LF endings although the repo declares it CRLF. It was repaired with `rm` and `git checkout --` (the committed blob was right, so no commit was needed). No work was reset or lost.

## The lead's calls

- One new bundle, not more milestones on the executed one.
- FadeNineSlice and IconBorder are fixed in the library and reach every caller. The edge is in the skin's border token, falling back to the divider, then the body text at 0.4.
- The zoom is 0.07 by default; `opts.zoom` overrides it and `false` turns it off. It only ever tightens an existing crop.
- Every skin's `icon.borderStyle` and `icon.borderSize` is Solid 1px, so host-drawn icon borders match the library's.
- Obsidian's body is 12. The stripe floor is 8% in every dark skin, and the hover rises to 0.15 so a hovered row still differs from a striped one.
- A stored Ka0s Friz pick moves to Ka0s Ubuntu through a one-time migration per addon. Blizzard's own Friz is untouched.
- Smoke checks re-opened by this round have their old pass marks withdrawn, with "not run" as the Result.

## Open items and not done

- **R3-DEFER is not done.** The comment on LibKa0s#70 (SF-DR-9 deferred on 2026-11-02 because the live Damage profile draws secret values the line chart cannot plot, so the live chart and Results keep the column look; #70 stays open) was refused by the session's permission check (external system write). It was not worked around, and no `exceptions.tsv` row was added. Post it yourself, or allow it and re-run R3-DEFER.
- Two leftovers. The Skin Tester's SHOW-17 still says "2px" (an old passed check whose wording was left alone). ConsumableMaster's SKIN-42 lacks a final full stop.
- Owed by you: the smoke run in `06_SMOKE_TESTS.md`, then the go-ahead. After that comes `/dev-copilot:finalize`, the push of tag v1.85.0, closing LibKa0s #71 and #72 (spaced apart; #70 stays open), and the cleanup of branches, stashes and worktrees.
