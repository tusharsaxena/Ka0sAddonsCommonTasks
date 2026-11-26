#!/usr/bin/env bash
# Progress from git alone. Done = a commit whose subject starts "<ID>: " (or carries "<ID> + " / "+ <ID>:")
# on the run branch or, after merge, on the default branch; or a row in exceptions.tsv.
# GIT is the folder that holds the clones: ~/ka0s-scratch/r4 by default (where the run is built), or the
# live GIT folder once the branches are fetched there. Ka0sAddonsCommonTasks (R4-PLAN) is always this repo.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; GIT="${KA0S_GIT:-$HOME/ka0s-scratch/r4}"
PLAN_REPO="$(cd "$HERE/../../.." && pwd)"
BR=feat/2026-11-26-owner-feedback-round4
SINCE=2026-11-26T00:00
defbr() { git -C "$1" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo master; }
repodir() { if [ "$1" = Ka0sAddonsCommonTasks ]; then echo "$PLAN_REPO"; else echo "$GIT/$1"; fi; }
done=0; total=0
while IFS=$'\t' read -r id ms repo title deps rest; do
  [ "$id" = id ] && continue
  total=$((total+1)); d="$(repodir "$repo")"; state=TODO; pat="(^|\+ )$id(:| \+)"
  if cut -f1 "$HERE/exceptions.tsv" | grep -qx "$id"; then state=DONE-EXC
  elif git -C "$d" rev-parse -q --verify "$BR" >/dev/null 2>&1 &&
       git -C "$d" log "$BR" --since=$SINCE --format=%s | grep -qE "$pat"; then state=DONE
  elif git -C "$d" log "$(defbr "$d")" --since=$SINCE --format=%s 2>/dev/null | grep -qE "$pat"; then state=DONE-MERGED
  fi
  case $state in DONE*) done=$((done+1));; esac
  printf '%-12s %-3s %-22s %-11s %s\n' "$id" "$ms" "$repo" "$state" "${title:0:70}"
done < "$HERE/items.tsv"
echo "---- $done / $total done"
for r in $(cut -f3 "$HERE/items.tsv" | tail -n +2 | sort -u); do
  d="$(repodir "$r")"
  printf '%-22s branch=%-38s dirty=%s\n' "$r" "$(git -C "$d" branch --show-current 2>/dev/null)" "$(git -C "$d" status --porcelain 2>/dev/null | wc -l)"
done
if [ -d "$GIT/LibKa0s" ]; then
  printf 'LibKa0s tag v1.118.0: %s\n' "$(git -C "$GIT/LibKa0s" rev-parse -q --verify 'refs/tags/v1.118.0' >/dev/null && echo present || echo absent)"
fi
