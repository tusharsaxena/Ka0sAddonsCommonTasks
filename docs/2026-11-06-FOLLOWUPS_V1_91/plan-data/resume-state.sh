#!/usr/bin/env bash
# Progress of the 2026-11-06 v1.91.0 follow-ups, computed from git only.
G=/mnt/d/Profile/Users/Tushar/Documents/GIT; B=feat/2026-11-06-followups-v1-91; D=$(dirname "$0")
done=0; tot=0
while IFS=$'\t' read -r id m repo title rest; do [ "$id" = id ] && continue; tot=$((tot+1)); hit=0
  git -C "$G/$repo" log --format=%s master..$B 2>/dev/null | grep -qE "(^|\+ )$id( \+ [A-Z0-9-]+)*: " && hit=1
  git -C "$G/$repo" log --format=%s master 2>/dev/null | grep -qE "(^|\+ )$id( \+ [A-Z0-9-]+)*: " && hit=1
  grep -q "^$id"$'\t' "$D/exceptions.tsv" && hit=1
  [ $hit = 1 ] && done=$((done+1)) || echo "OPEN $id $repo"; done < "$D/items.tsv"
echo "TOTAL $done/$tot"
for r in $(cut -f3 "$D/items.tsv" | tail -n +2 | sort -u); do p=$G/$r; s=$(git -C "$p" status --porcelain | wc -l); [ "$s" != 0 ] && echo "DIRTY $r $s"; b=$(git -C "$p" branch --show-current); [ "$b" != "$B" ] && [ "$b" != master ] && echo "BRANCH $r $b"; done
