# DEPENDENCIES.md — Ka0sAddonsCommonTasks

The toolchain for **this** workspace: the planning and record repo for work that spans several Ka0s
repositories (`README.md`). It ships nothing to the WoW client and builds nothing, so the list is short. It
follows the shape the Ka0s standard gives a documentation-and-tooling repo (`documentation-§8`): a required
list, then what is deliberately not used here. This workspace sits outside the audit rotation
(`WowAddonStandards/standards/ADDONS.md`), so this file is a convenience for a new machine rather than an
audited contract.

Measured on 2026-11-06 from the tracked files (`git ls-files`).

## Required

| Tool | Needed for | Evidence | Install (WSL2 / Ubuntu) | Verify |
|---|---|---|---|---|
| **git** | Everything. A bundle's progress is computed from git, not from a status table (`CLAUDE.md`, *Resumable, checkpointed plans*). | every bundle's `resume-state.sh` | `sudo apt install -y git` | `git --version` |
| **zsh** and **bash** | Running a bundle's `resume-state.sh`. Most start `#!/bin/zsh`, a few `#!/bin/bash`. | `head -1 docs/*/resume-state.sh` | `sudo apt install -y zsh` (bash is preinstalled) | `zsh --version` |
| **gh** (GitHub CLI), authenticated | The `/dev-copilot:*` issue commands and the issue passes these bundles record; `gh auth login` once per machine. | the issue-pass bundles, e.g. `docs/2026-10-01-GITHUB_ISSUE_PASS/` | see <https://github.com/cli/cli/blob/trunk/docs/install_linux.md> | `gh auth status` |

## Needed only to re-run a specific bundle's helpers

Frozen bundles keep the scripts that produced their plan data. Re-running one is rare; each needs only what
its own header names.

| Tool | Which helpers | Install | Verify |
|---|---|---|---|
| **python3** (standard library) | `docs/*/plan-data/**/*.py` | preinstalled on Ubuntu | `python3 --version` |
| **fontTools** | the font-metrics helpers in `docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK/plan-data/` and `docs/2026-10-31-FONT_PICKERS_AND_SKIN_FACES/plan-data/`, and `docs/2026-10-25-SKINNING/plan-data/tools/assemble.py` | `sudo apt install -y python3-fonttools` (Ubuntu's Python is PEP 668 externally managed, so a bare `pip install --user` is refused) | `python3 -c "import fontTools"` |
| **lua5.1** | the census scripts in `docs/2026-10-01-GITHUB_ISSUE_PASS/plan-data/`, `docs/2026-10-02-LIBKA0S_CENSUS_ADOPTION/plan-data/`, `docs/2026-10-22-LIBKA0S_ISSUES_45_58/plan-data/census-v1.75.0/` and `docs/2026-10-31-FINDINGS_REMEDIATION/plan-data/census-v1.83.0/`, run from the LibKa0s repo root (the 2026-10-01 header says so; the later copies keep its logic) | `sudo apt install -y lua5.1` | `lua5.1 -v` |

## Not used here

- **luacheck, lizard, the test kit.** Each addon's green gate runs in that addon's repo, under its own
  `DEPENDENCIES.md`, never from here.
- **Node.js.** The `*.js` files under `docs/*/plan-data/` are workflow scripts run by Claude Code's Workflow
  tool, not by Node.
- **The WoW client and the CurseForge packager.** In-client smoke tests are the owner's; this repo records
  their results.
- **A CurseForge API key** is needed by `/dev-copilot:wow-curseforge-releases` and
  `/dev-copilot:wow-curseforge-comments`, which write `journal/curseforge/`; the key lives with the plugin,
  never in this repo.
