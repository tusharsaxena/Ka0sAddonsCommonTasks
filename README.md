# Ka0sAddonsCommonTasks

A workspace for work that spans **several** Ka0s repositories at once, and therefore has no single repo it
belongs in.

## What this is not

- **Not an addon.** Nothing here is installed by a player, loaded by the client, or packaged. There is no
  TOC, no `libs/`, no test suite.
- **Not upstream of anything.** It is not `LibKa0s`, not `WowAddonStandards`, not the `wow-addon` plugin.
  No addon vendors from here, depends on here, or fetches anything from here at runtime. Those three are the
  real upstreams — this folder sits beside them, not above them.
- **Not a home for code that has a home.** If a script belongs to one addon, it goes in that addon. If a rule
  belongs to the standard, it goes in `WowAddonStandards`. If a command belongs to the plugin, it goes in
  `wow-addon`.

## What belongs here

Only things that are genuinely cross-repo and genuinely homeless:

- **Cross-repo docs, specs and plans** — consolidated findings, remediation specs, execution plans, anything
  that reasons about the collection as a whole rather than about one addon.
- **Reusable tools and scripts** that operate across repos and would be arbitrary to park in any one of them.

Everything else has somewhere better to live.

## Layout

```
docs/
  <YYYY-MM-DD>-<TOPIC>/     one dated bundle per cross-repo exercise
```

Bundles are dated at creation and treated as frozen once the work they describe has been executed — the
plan is the record of what was intended, and rewriting it after the fact destroys that.

## The collection

Everything below is a sibling directory under the same parent.

**The upstreams** — the three repos the addons actually depend on:

| Repo | Role |
|---|---|
| `WowAddonStandards` | The Ka0s WoW Addon Standard — source of truth for every rule an addon is audited against |
| `LibKa0s` | The shared library and the test kit, vendored into every addon |
| `wow-addon` | The Claude Code plugin — the `/wow-addon:*` commands and agents |

**The addons** — read [`../WowAddonStandards/standards/ADDONS.md`](../WowAddonStandards/standards/ADDONS.md).
That roster is the single source of truth for which addons are in scope, and it is the one place scope is
edited. Do not restate it here; a copied list goes stale the first time an addon is added or retired.
