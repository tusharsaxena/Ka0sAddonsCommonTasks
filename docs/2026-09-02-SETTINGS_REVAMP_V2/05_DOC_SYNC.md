# The documentation sync

`/wow-addon:sync-docs` run against each of the nine addons after the code landed. The playbook is
per-repo, so it ran nine times in parallel rather than once.

Documentation-only held: `git status` across all nine showed **nothing but `.md`**, and every suite
came back exactly as green as it went in — no `.lua`, `.xml`, `.toc`, `.luacheckrc` or `.pkgmeta` was
touched by the sync.

## What had drifted

The revamp moved the settings surface a long way in one pass, and the docs describing it moved
correspondingly far out of date. The recurring classes:

- **Counts taken from prose rather than from the schema.** Tab counts, row counts, suite counts,
  "three vendored files" for a library that now ships four. Every one re-derived from the code.
- **`afterRestoreAll`**, a descriptor hook that no longer exists — the global reset became a profile
  reset in `options-ui-§12`, so it is `resetProfile` now. The dead name was still being cited across
  seven files in Absorb Tracker alone.
- **"Class colour is always the player's"**, stated in four places in Absorb Tracker, which is the
  exact claim this pass reversed.
- **The LibKa0s payload description** — "ten majors across thirteen files" everywhere, now fourteen,
  since `OptionsCompose.lua` arrived.
- **Controls renamed by the revamp** still cited under their old names in FAQ and troubleshooting rows
  — "Show only in combat" for what is now the General visibility dropdown, "Lock Position" for
  "Lock frame".

## Findings reported rather than fixed

**Every addon's `docs/automated-tests/RESULTS.md` is stale**, and correctly so. It is generated, its
newest row predates the revamp, and it is regenerated at release by `/wow-addon:bump-version`. A
hand-edited complexity or test record reads as measured when it is not — that is anti-pattern #51, and
the playbook is explicit that staleness here is reported, never corrected in place. It will resolve
itself the moment these branches are released.

**Dead exports** were flagged, not removed: 2 in Absorb Tracker, 5 in Bank Ledger, 1 in Consumable
Master, 3 in KickCD, 3 in Loot History, 1 in Multi Meters, 3 in Panel Master, 5 in Pretty Chat, 4 in
What Group. The user decides on those.

## Comment citations

The sweep read every comment in the addons' own source for citations that no longer resolve. It
produced 47 raw hits, most of which it correctly cleared itself — a comment deliberately describing
history ("this replaced `modules/DebugLog.lua`, which was 357 lines of window, buffer and scrollbar"),
a cross-repo reference naming a sibling addon's file, a path resolving in the LibKa0s checkout rather
than here. Those are not defects and were left alone.

Roughly twenty were genuine, and were applied on explicit confirmation, comment-only:

- **KickCD** — four comments citing the dead `afterRestoreAll` hook, and a `settings/Panel_Widgets.lua:49`
  in a file of 44 lines.
- **Panel Master** — a composed block described as "these six rows, and nothing else" that is seven; a
  `P.__ui` table described as ten entries that holds nine.
- **What Group** — a `WhatGroup_Frame.PopulateFields` with no definition and no call site anywhere; two
  comments describing a reset as wiping `db.profile` when it is a `ResetProfile`.
- **Pretty Chat** — "~350 rows" and "~170 Blizzard globals" where the schema returns 173 rows and
  `ApplyStrings` walks 79 unique globals. These are countable-claim drift, which the mechanical check
  cannot see: they name nothing that fails to resolve, they are just wrong. Included on the user's
  explicit instruction to apply all of them.
- **Bank Ledger** — a `modules/LedgerTable.lua:1044` pointing at the Whitelist menu entry rather than
  the delete call it means.

### One that was not a comment

`PanelMaster/settings/Panel.lua:365` carried a user-visible tooltip reading *"Reset every setting on
this page to its default. Your panels are untouched."* The General page's Defaults now runs a profile
reset, so that is false, and a player trusting it could lose panel settings. A string is outside
`sync-docs`' edit boundary by design, so it was raised separately and corrected on explicit approval —
the one runnable line this documentation pass touched, and the reason the boundary exists is so that
it had to be asked about rather than quietly changed.
