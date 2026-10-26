# Bounded lint in every green gate (2026-10-26)

## The problem

The owner kept hitting this when a session ran an addon's green gate:

```
PreToolUse:Bash hook error: Unbounded heavy run (luacheck). Prefix it with the bounded runner: ...
```

The session was doing what the addon's `CLAUDE.md` told it to: *Green gate before every commit:
`lua tests/run.lua` and `luacheck .` (0/0)*. Every roster addon inherited that line from the stub
`CLAUDE.md` in the standard's context pack (`WowAddonStandards@36da4ef:standards/NEW_ADDON_CONTEXT.md:1491`).

The hook is right. testing-§15 requires `luacheck` to run bounded. `lua tests/run.lua` passes the hook
because a kit at revision 23 or later bounds itself on load, and every repo here vendors kit 42. `luacheck`
loads no kit, so a bare run is refused every time. The documented gate contradicted the rule it serves.

## Ruling

Fix the instructions, not the guard. The hook stays as strict as it is, and every place that tells a
session how to lint names the bounded form, `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`. That
is the form the hook's own message prescribes, and it prints luacheck's full output. The kit's
`run-automated-tests.sh --suite lint --no-bundle` prints only a summary line.

## Items

Branch `feat/2026-10-26-bounded-lint` in every repo touched. An item is done when a commit whose subject
starts `<ID>: ` exists in its repo.

| ID | Repo(s) | Change |
|---|---|---|
| BL-01 | dev-copilot | The hook's refusal prints each blocked run with the runner in front, redirections dropped, so the retry is a copy. One new hook case (27). Plugin 2.6.0 → 2.6.1. |
| BL-02 | WowAddonStandards | The context pack's stub `CLAUDE.md` gate line and its *Am I set up correctly?* block name the bounded lint, and the block's complexity run goes through the runner too. A pack-only correction to an existing MUST, so no version change; the unmerged skinning branch owns v2.89.0. |
| BL-03 | the 15 roster addons + LibKa0s | Each `CLAUDE.md` gate line (ConsumableMaster's and LibKa0s' gate code blocks) names the bounded lint; ConsumableMaster's release-time complexity command too. |
| BL-04 | Ka0sAddonsCommonTasks | This bundle, and the Verification note in `CLAUDE.md`. |

## Out of scope

- `docs/testing.md` in each addon. It is the human-facing how-to, and a person in a terminal is not under
  the hook. Agents read the gate in `CLAUDE.md`.
- PanelMaster's `CLAUDE.md` names `tests/_kit/run-automated-tests.sh` in prose about release. Releases
  run through `/dev-copilot:bump-version`, which already bounds it.
- Exempting a kit-23+ `run-automated-tests.sh` from the hook the way `tests/run.lua` is exempted. Possible,
  but it would loosen the guard, and nobody asked for it.
