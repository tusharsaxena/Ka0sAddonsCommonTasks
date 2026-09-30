# Execution record

Run: 2026-09-29 09:20 → 2026-09-30 ~01:30 (IST), with a 13:07–20:14 pause while the owner's PC slept.
All 33 items done and independently reviewed (git notes `refs/notes/ka0s-review`). Branch
`feat/2026-09-29-smoke-and-profile` pushed in 14 repos. **Nothing merged; LibKa0s tag `v1.63.0` local
only** (on `1856218`, the release-record commit for kit revision 32).

## What shipped

- **LibKa0s v1.63.0**: Slash minor 17 adds `CliProfile`, `ProfileSwitch`, `ProfileNames` and the
  `profiles` descriptor field. Consumer guidance names both stub members (a reviewer caught the first
  draft's wrong claim, measured on all eleven consumers).
- **`/<prefix> profile [name]` in all eleven addons**: bare lists, a name switches to an existing profile
  (exact case, quotes stripped), unknown names refused and never created, works while disabled, refused
  in combat. AbsorbTracker and PartyFrameEnhanced keep their sub-verbs on the shared code
  (AbsorbTracker's silent create on `use` is gone).
- **Profile support where there was none**: PrettyChat, WhatGroup (Profiles page, callbacks,
  `docs/profiles.md`); BankLedger, LootHistory (settings moved into the profile by a one-time migration,
  recorded data and `retentionDays` stay account-wide per D6; BankLedger's `savedvariables-§2` deviation
  retired).
- **Smoke tests**: all eleven `docs/smoke-tests.md` rewritten as evergreen, deduplicated, theme-grouped
  suites with stable IDs, a Non-English client section (LOC) and a Pending sign-off list; each has a
  coverage map in `smoke-maps/`. The plugin's `new-addon.md` cites ConsumableMaster/KickCD LOC-1.
- **AuraMaster**: the fresh-login weapon-enchant name fix (engine flip after the loading screen and on
  weapon item data) and `/am redraw light|full` (bare = full when allowed, else light).

## How it ran

M0 plan → M1 (5 items) → M2 (11) → M3 (11 smoke + plugin + 2 AuraMaster) → M4 (doc sync in 13 repos). Every
item: implement → adversarial review → fix rounds. The smoke rewrites needed the most review: up to
five full rounds plus a scoped close-out, after the owner-facing policy for Pending sign-off and the
review bar were clarified mid-run (02_SPEC S4).

Owner decisions taken mid-run: D6 (data-governing settings stay account-wide), the `/am redraw` forms and
their semantics (S7: full re-dresses in place rather than rebuilding engines, which would leak frames).

## M4 doc sync heads (all gates green)

| Repo | Head | Tests | Lint |
|---|---|---|---|
| AbsorbTracker | 144204e | 819 | 0/0 |
| AuraMaster | d4edc0d | 1750 | 0/0 |
| BankLedger | 11a7395 | 1150 | 0/0 |
| ConsumableMaster | eff8eb9 | 1130 | 0/0 |
| KickCD | 17ed9ce | 1216 | 0/0 |
| LootHistory | 812703f | 987 | 0/0 |
| MultiMeters | 959afc5 | 2107 | 0/0 |
| PanelMaster | 2647230 | 975 | 0/0 |
| PartyFrameEnhanced | e1086cb | 393 | 0/0 |
| PrettyChat | cea1ed4 | 538 | 0/0 |
| WhatGroup | 5b62a2f | 846 | 0/0 |
| LibKa0s | 1856218 (was a05ae00 at M4) | 1777 (+1 skipped) | 0/0 |
| wow-addon | da32bba | 20 (its own suite) | n/a |

## Left for the owner

1. In-game checks: `IN_GAME_CHECKS.md` (includes the ConsumableMaster key test owed from 2026-09-29).
2. Merge go-ahead: then per repo, LibKa0s first: merge `--no-ff`, gate on the merge, push master, push
   the `v1.63.0` tag, delete the branches.
3. Comment corrections from the doc sync: six APPLIED on 2026-09-30 with the owner's OK (KickCD 2312d75,
   WhatGroup a65e4de, PrettyChat ea56280, AbsorbTracker f11a3d7, BankLedger ceb629d, MultiMeters
   241976d; each gated green). The seventh, LibKa0s `testkit/README.md`'s consumer count, was
   folded into v1.63.0 on the owner's call: kit revision 32 (06cc010), release run re-taken
   (20260930-084657, record commit 1856218), local tag `v1.63.0` moved to 1856218 (still unpushed), and
   `tests/_kit/` re-vendored in all eleven addons (each gated green, byte-identical to the tag).
4. Dead exports reported, not deleted (see each repo's sync notes), e.g. MultiMeters test-only seams.
