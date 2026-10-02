# Resume

1. `./resume-state.sh -v` prints done/reviewed per milestone, the READY items and each tree's branch,
   dirt and unpushed count. Git is the only state.
2. A dirty tree: read it; continue the interrupted item or stash it. Never reset work you have not read.
3. The LibKa0s tag v1.68.0 is local until the owner's go-ahead. If TP-LK-01's release commit moved,
   re-point the local tag (`git tag -f`) before any re-vendor, and re-vendor from the tag.
4. After the M2 checkpoint row: push every feature branch and `refs/notes/ka0s-review`.
5. On the owner's go-ahead: `/wow-addon:finalize` in dependency order (LibKa0s first, push the tag),
   then delete every `feat/2026-10-02-drag-attach` branch, local and origin.
