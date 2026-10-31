#!/bin/bash
# Done = a commit on the run branch whose subject starts "<id>: ", or an exceptions.tsv row.
cd "$(dirname "$0")"; G=../../..; G=$(cd "$G/.." && pwd); B=feat/2026-10-31-findings-remediation; done=0; all=0
while IFS=$'\t' read -r id m repo t; do [ "$id" = id ] && continue; all=$((all+1))
 if git -C "$G/$repo" log --format=%s master..$B 2>/dev/null | grep -q "$id"; then done=$((done+1)); elif grep -q "^$id"$'\t' exceptions.tsv; then done=$((done+1)); else echo "OPEN $id $repo"; fi
done < items.tsv; echo "TOTAL $done/$all"
