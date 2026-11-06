#!/usr/bin/env bash
# Progress of the 2026-11-07 WoW Forever port (steps 1-4), computed from git only.
# Done = a commit whose subject starts "<ID>: " (or "... + <ID>: ") on the run branch or on master,
# or a row in exceptions.tsv. GATE-A/GATE-B are merge commits on master.
G=/mnt/d/Profile/Users/Tushar/Documents/GIT; B=feat/2026-11-07-wow-forever-port; D=$(dirname "$0")
done=0; tot=0
while IFS=$'\t' read -r id m repo title rest; do [ "$id" = id ] && continue; tot=$((tot+1)); hit=0
  pat="(^|\+ )$id( \+ [A-Z0-9-]+)*: "
  git -C "$G/$repo" log --format=%s "master..$B" 2>/dev/null | grep -qE "$pat" && hit=1
  git -C "$G/$repo" log --format=%s master 2>/dev/null | grep -qE "$pat" && hit=1
  grep -q "^$id"$'\t' "$D/exceptions.tsv" && hit=1
  [ $hit = 1 ] && done=$((done+1)) || echo "OPEN $m $id $repo"; done < "$D/items.tsv"
echo "TOTAL $done/$tot"
for r in $(cut -f3 "$D/items.tsv" | tail -n +2 | sort -u); do p=$G/$r
  s=$(git -C "$p" status --porcelain | wc -l); [ "$s" != 0 ] && echo "DIRTY $r $s"
  b=$(git -C "$p" branch --show-current); [ "$b" != "$B" ] && [ "$b" != master ] && echo "BRANCH $r $b"; done
