# M1 addendum: the lead's calls on candidates the plan did not name (2026-11-06)

M1's re-vendor items reported two candidates that `00_PLAN.md`'s decisions table does not cover. Each
was recorded as *undecided* in its addon's frozen bundle. The owner told the run to decide what it can,
so the lead decided both. Both are additive and small, and neither needs an issue.

| Item | Addon | Candidate | Call | Why |
|---|---|---|---|---|
| V89A-ST | LibKa0sSkinTester | A Showroom sample of a skinned `W.ContextMenu` cascade (`modules/ShowroomWidgets.lua`): submenu arrow, tick column, stacked levels (its bundle `02_CANDIDATES.md:23-29`) | **adopt** | The tester exists to show every skinned surface. The cascade's child levels are new skinned frames, and nothing else in the collection shows them under each skin. |
| V89A-DWH | DropWatcher | The History row's one-entry menu (`modules/WindowHistory.lua:323-329`), from `NS.Compat.ContextMenu` over `MenuUtil` onto `W.ContextMenu` (its bundle `02_CANDIDATES.md:14`) | **adopt** | V89A-DW puts Filters ▾ on the shared skinned menu. Leaving the History row on the client menu would make DropWatcher's two menus look different. The client path stays as the no-library fallback. |

Both items join `plan-data/items.tsv` and `06_SMOKE_TESTS.md` as SM-06 and SM-07.

## The line-ending repair (M1)

Every M1 agent wrote its bundle's `.md` files with bare LF, but the addons' `.gitattributes` declare
`eol=crlf`. The committed blobs were correct; only the working-tree bytes were wrong. Ten verifiers
therefore re-ran the gate red on `eol: every tracked file carries the terminator .gitattributes
declares`. The lead re-checked those files out through the filter (`rm <files> && git checkout --
<files>`, in every committed repo) without amending any commit, then re-ran the gates.
