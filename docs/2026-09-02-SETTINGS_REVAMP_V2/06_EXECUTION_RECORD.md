# The execution record

Executed 2026-09-03 by `/wow-addon:finalize` across the twelve repos [`00_SCOPE.md`](00_SCOPE.md)
names. This document exists because the five before it are the record of what was *intended*, and the
README treats a bundle as frozen once its work has been executed. Three things those five state are no
longer true, and rewriting them would destroy the very thing the freeze protects — so the corrections
live here instead.

## Where the plan gave way

**Decision 2 is spent.** It read: *"Branch and commits only. Every repo stays on
`feat/settings-revamp-v2` … No version bumps, no merges to master, no tags — those are a separate,
gated act."* That separate act is this one. All twelve repos are now merged to their default branch
(`master`, except this repo's `main`) with `--no-ff`, and pushed. No version was bumped and no tag was
created, so those two halves of the decision still stand.

**The library shipped v1.25.0, not the v1.24.0 recorded throughout.** Decision 5, `01_UPSTREAM.md` and
`03_VERIFICATION.md` all name v1.24.0, which was correct when they were written — it was tagged
mid-pass so the addons' vendor-sync tests had something to compare against. A second release followed:
`OptionsCompose.lua` minor 2, *MasterControls takes a `leadButton`*. `options-ui-§15` fixes the wording
of the two reset buttons and that composer is the only thing that writes them, so an addon with a verb
of its own to put beside them had nowhere to put it — Pretty Chat's **Test** button. All nine addons
carry **v1.25.0**, and each states it on the `CLAUDE.md` provenance line the gate actually greps.

**`04_OPEN.md`'s "the branches are pushed and waiting" no longer holds.** They landed.

## What shipped

`/wow-addon:sync-docs` ran once more per repo before the gate, which is what produced the doc-sync
commits below. `libs/` and `tests/_kit/` were untouched everywhere; `lizard` was not run, because the
complexity record's checkpoint is release, not commit.

| Repo | Doc sync | Gate today | Merge | Pushed |
|---|---|---|---|---|
| LibKa0s | `ab221d4` — 2 files | 764 / 0 in 18 | `4eacebe` | `3887b6a..4eacebe` |
| WowAddonStandards | `708b3b0` — 2 files | no automated gate in repo | `03a9aa0` | `4a05ce5..03a9aa0` |
| Absorb Tracker | `78b65f9` — 1 file | 547 / 0 in 27 | `686cae5` | `156077c..686cae5` |
| Bank Ledger | `5f30808` — 3 files | 831 / 0 in 28 | `0aec078` | `abed21a..0aec078` |
| Consumable Master | `402a16c` — 2 files | 749 / 0 in 59 | `69a4d56` | `a256a2e..69a4d56` |
| KickCD | `2e21463` — 1 file | 841 / 0 in 36 | `1dca167` | `2cf78fe..1dca167` |
| Loot History | `72df1e2` — 4 files | 699 / 0 in 28 | `6d3c2de` | `2832dcf..6d3c2de` |
| Multi Meters | `909075b` — 1 file | 1487 / 0 in 45 | `0e74319` | `a2cbffb..0e74319` |
| Panel Master | none needed | 763 / 0 in 27 | `c5b4159` | `77d354a..c5b4159` |
| Pretty Chat | `63155d9` — 2 files | 300 / 0 in 18 | `6469f88` | `696dbc2..6469f88` |
| What Group | `d82092c` — 4 files | 528 / 0 in 16 | `9b35a23` | `8122e40..9b35a23` |

**6,745 tests across the nine addons**, against the 6,722 `02_ADOPTION.md` records — the +23 is the
v1.25.0 adoption and the regression tests that came with it. Every gate was run twice: once before the
commit and once on the merge result, because a merge that compiles is not a merge that passes. No
gate was red at any point, so nothing was committed or pushed against a failure.

Ordering was `LibKa0s → the nine addons → here`, with `WowAddonStandards` independent of the library
and merged alongside it. The edge is not decorative: each addon's provenance line and vendored payload
name a library release, so an addon reaching origin first would have cited a version not yet there.

## What the sync found and did not fix

The nine syncs were content-only by construction — no document was created, moved or restructured in
any addon, because the run was parallel and nobody was available to confirm a structural change. What
they turned up, all reported rather than acted on:

- **Two comment sets that assert a reader which does not read.** KickCD's `settings/Panel.lua:236` and
  `:376` (`Helpers.PrintSchemaError`, `Helpers.FireOnChange`) are dead exports whose comments each name
  a file that does not reference them. A natural pair for `/wow-addon:issue-add`.
- **Countably-wrong comments** in Bank Ledger (`settings/Panel.lua:661`, `:691` — "six tabs" and "two
  filter tabs", now five and one), Multi Meters (`settings/OptionsSetup.lua:53-56`, `:95` — "nine
  pages" naming three that the tabbed redesign folded away; six remain) and Pretty Chat
  (`settings/Panel.lua:544`, and the test name at `tests/test_panel.lua:442` that carries the wording
  into the generated inventory). Comment-only, and the replacement text is the author's to name.
- **Absorb Tracker `core/PerfSetup.lua:8`** cites `docs/record-schema.md`, which does not exist.
- **Panel Master's ratified `documentation-§4` deviation has fired its own re-surface condition.** It
  rests on *"The addon is pre-release, so the rule is not yet engaged"*, with the trigger *"The first
  published release"* — and v1.0.0 shipped, tagged `1.0.0-release`, 2026-08-07. The premise is false
  now; the deviation needs re-ratifying on new grounds or a root `TODO.md`.
- **An ordinal contradiction inside the standard itself.** `documentation.md:117` enumerates
  `## Documentation map` ninth and `## Documented deviations` tenth; `:137` and `:276` say the
  opposite, as does the frozen v2.23.0 changelog entry. Frozen history cannot be edited and the live
  text cannot be corrected without contradicting it, so all three were left alone. This is a real
  defect an audit could file against an addon either way.
- **Dead exports** were surfaced and none deleted, as always.
- **Every addon's `docs/automated-tests/RESULTS.md` is stale**, and correctly so — it is generated, and
  `/wow-addon:bump-version` owns the refresh at release. No addon bumped a version in this changeset,
  so no fresh bundle was owed and none was regenerated.

## One upstream finding, from the vendor gate

Eight of the nine addons reported the same non-empty *byte* diff — `LibKa0s/DebugLog.lua` and
`LibKa0s/Pool.lua` — while the content diff (`--strip-trailing-cr`, the MUST) was empty in all nine.

It is not drift and not a fork. The addons' committed blobs are hash-identical to `v1.25.0`, and
`git -C ../LibKa0s diff v1.25.0 -- LibKa0s` is empty, so the library's *index* matches the tag exactly.
Only the library's **working tree** is the straggler: those two files sit checked out as LF while the
repo declares `eol=crlf`, which `git status` reports as clean because attributes normalize at add time.
Every addon's `tests/test_vendor_sync.lua` passes, because it compares against the tag rather than the
sibling working tree.

Settled in the LibKa0s checkout with `git add --renormalize .`, or `rm <path> && git checkout -- <path>`
per file. Nothing was patched under any `libs/` — a local edit there is reverted by the next re-vendor.

## The branch deletion, and why `-d` refused

Ten of the twelve repos refused `git branch -d feat/settings-revamp-v2` with the same message:

```
warning: not deleting branch 'feat/settings-revamp-v2' that is not yet merged to
         'refs/remotes/origin/feat/settings-revamp-v2', even though it is merged to HEAD
error: the branch 'feat/settings-revamp-v2' is not fully merged.
```

Git compares against the branch's **upstream ref**, not against `HEAD` or `master` — and it says so in
its own warning. Each repo's doc-sync commit was made on the feature branch and reached origin via
`master`, never via `origin/feat/settings-revamp-v2`, so every branch was ahead of its own remote. No
work was ever at risk: every commit is an ancestor of the pushed default branch.

`-D` was not used anywhere. The refusal is a safety check that was doing its job, and routing around it
with a force-delete is how a collection learns to distrust its own guardrails.
