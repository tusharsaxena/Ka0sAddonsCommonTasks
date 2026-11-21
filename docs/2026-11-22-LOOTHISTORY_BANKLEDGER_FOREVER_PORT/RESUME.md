# Resuming the LootHistory + BankLedger Forever port

**Git is the only state.** Run `plan-data/resume-state.sh`: an item is done when a commit whose subject starts `<ID>: `
exists on `feat/2026-11-22-forever-port-lh-bl` (or, after merge, on `master`) in the repo `plan-data/items.tsv` names.

1. **Find the state:** `bash plan-data/resume-state.sh`.
2. **Clean up an interrupted item:** in a repo with `dirty>0`, read the diff. If it is the next TODO item's work, finish
   it (gate green, commit `<ID>: …`). If it is unreadable or unrelated, `git stash push -m "<ID> interrupted"`. Never
   `reset --hard` or `checkout .` work you have not read.
3. **Relaunch:** re-run the build workflow (script path in `07_EXECUTION_RECORD.md`). Every item agent first checks for its
   own commit and returns `skipped` when it exists, so a relaunch only does the remaining work. With the same session,
   `resumeFromRunId` replays finished agents from cache.
4. **Per-item gate** (inside the addon repo): `lua tests/run.lua`, `KA0S_KIT_CLIENT=forever lua tests/run.lua`,
   `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` (0/0), no file above 1500 lines.
5. **Checkpoint CP-1 (lead):** both profiles green in both addons, luacheck 0/0, TOCs `120105, 16001`, reviews recorded as
   `refs/notes/ka0s-review`; append a row to `checkpoints.tsv` with totals and heads; push the feature branches (with
   notes); then `/dev-copilot:finalize` merges `--no-ff` in order WowAddonStandards, LootHistory, BankLedger,
   Ka0sAddonsCommonTasks (owner authorized merge, R3). No version bump, no tag.
6. **After the owner's probes:** read `_forever_/WTF/Account/<acct>/SavedVariables/{LootHistory,BankLedger}.lua` `probe`
   tables, compare against each addon's `docs/forever-probes.md` safe defaults, and open a new bundle for any follow-up.
   This bundle stays frozen.
