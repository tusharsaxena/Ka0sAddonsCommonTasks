#!/usr/bin/env bash
# Progress from git alone. Done = a commit whose subject starts "<ID>: " (or carries "<ID> + " / "+ <ID>:")
# on the run branch or, after merge, on the default branch; or a row in exceptions.tsv.
# GIT is the directory four levels up: the GIT folder, or the run's scratch folder that holds the clones.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; GIT="${KA0S_GIT:-$(cd "$HERE/../../../.." && pwd)}"
BR=feat/2026-11-25-seeds-foreverdb
SINCE=2026-11-25T00:00
defbr() { git -C "$1" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo master; }
done=0; total=0
while IFS=$'\t' read -r id ms repo title deps rest; do
  [ "$id" = id ] && continue
  total=$((total+1)); d="$GIT/$repo"; state=TODO; pat="(^|\+ )$id(:| \+)"
  if cut -f1 "$HERE/exceptions.tsv" | grep -qx "$id"; then state=DONE-EXC
  elif git -C "$d" rev-parse -q --verify "$BR" >/dev/null 2>&1 &&
       git -C "$d" log "$BR" --since=$SINCE --format=%s | grep -qE "$pat"; then state=DONE
  elif git -C "$d" log "$(defbr "$d")" --since=$SINCE --format=%s 2>/dev/null | grep -qE "$pat"; then state=DONE-MERGED
  fi
  case $state in DONE*) done=$((done+1));; esac
  printf '%-12s %-3s %-30s %-11s %s\n' "$id" "$ms" "$repo" "$state" "${title:0:70}"
done < "$HERE/items.tsv"
echo "---- $done / $total done"
for r in $(cut -f3 "$HERE/items.tsv" | tail -n +2 | sort -u); do
  printf '%-30s branch=%-36s dirty=%s\n' "$r" "$(git -C "$GIT/$r" branch --show-current)" "$(git -C "$GIT/$r" status --porcelain | wc -l)"
done
