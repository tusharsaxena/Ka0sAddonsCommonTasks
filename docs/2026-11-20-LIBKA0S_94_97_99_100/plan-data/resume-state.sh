#!/usr/bin/env bash
# Progress from git alone. Done = a commit whose subject starts "<ID>: " (or carries "<ID> + " / "+ <ID>:")
# on the run branch or, after merge, on the default branch; or a row in exceptions.tsv.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; GIT="$(cd "$HERE/../../../.." && pwd)"
BR=feat/2026-11-20-libka0s-94-97-99-100
defbr() { git -C "$1" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo master; }
done=0; total=0
while IFS=$'\t' read -r id wave repo title; do
  [ "$id" = id ] && continue
  total=$((total+1)); d="$GIT/$repo"; state=TODO; pat="(^|\+ )$id(:| \+)"
  if cut -f1 "$HERE/exceptions.tsv" | grep -qx "$id"; then state=DONE-EXC
  elif git -C "$d" rev-parse -q --verify "$BR" >/dev/null 2>&1 &&
       git -C "$d" log "$BR" --since=2026-11-20T00:00 --format=%s | grep -qE "$pat"; then state=DONE
  elif git -C "$d" log "$(defbr "$d")" --since=2026-11-20T00:00 --format=%s 2>/dev/null | grep -qE "$pat"; then state=DONE-MERGED
  fi
  case $state in DONE*) done=$((done+1));; esac
  printf '%-11s %-2s %-29s %-11s %s\n' "$id" "$wave" "$repo" "$state" "${title:0:60}"
done < "$HERE/items.tsv"
echo "---- $done / $total done"
for r in $(cut -f3 "$HERE/items.tsv" | tail -n +2 | sort -u); do
  printf '%-29s branch=%-36s dirty=%s\n' "$r" "$(git -C "$GIT/$r" branch --show-current)" "$(git -C "$GIT/$r" status --porcelain | wc -l)"
done
