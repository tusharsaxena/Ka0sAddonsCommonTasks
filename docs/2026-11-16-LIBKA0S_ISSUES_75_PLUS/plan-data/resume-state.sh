#!/usr/bin/env bash
# Progress from git alone. An item is done when a commit whose subject starts "<ID>: " (or carries
# "<ID> + " / "+ <ID>:") exists on the run branch of its repo, on its default branch after merge, or when
# exceptions.tsv lists it. DropWatcher's re-vendor may live in a worktree; branches are shared, so git log works.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
GIT="$(cd "$HERE/../../../.." && pwd)"
BR=feat/2026-11-16-libka0s-75-plus
defbr() { git -C "$1" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo master; }
done=0; total=0
while IFS=$'\t' read -r id ms repo title deps rest; do
  [ "$id" = id ] && continue
  total=$((total+1)); d="$GIT/$repo"; state=TODO; pat="(^|\+ )$id(:| \+)"
  if cut -f1 "$HERE/exceptions.tsv" | grep -qx "$id"; then state=DONE-EXC
  elif git -C "$d" rev-parse -q --verify "$BR" >/dev/null 2>&1 &&
       git -C "$d" log "$BR" --since=2026-11-16T00:00 --format=%s | grep -qE "$pat"; then state=DONE
  elif git -C "$d" log "$(defbr "$d")" --since=2026-11-16T00:00 --format=%s 2>/dev/null | grep -qE "$pat"; then state=DONE-MERGED
  fi
  case $state in DONE*) done=$((done+1));; esac
  printf '%-7s %-3s %-29s %-11s %s\n' "$id" "$ms" "$repo" "$state" "${title:0:70}"
done < "$HERE/items.tsv"
echo "---- $done / $total done"
for r in $(cut -f3 "$HERE/items.tsv" | tail -n +2 | sort -u); do
  printf '%-29s branch=%-36s dirty=%s\n' "$r" "$(git -C "$GIT/$r" branch --show-current)" "$(git -C "$GIT/$r" status --porcelain | wc -l)"
done
git -C "$GIT/LibKa0s" tag -l v1.105.0 | sed 's/^/local tag: /'
git -C "$GIT/DropWatcher" worktree list 2>/dev/null | grep -i 75plus | sed 's/^/DW worktree: /'
