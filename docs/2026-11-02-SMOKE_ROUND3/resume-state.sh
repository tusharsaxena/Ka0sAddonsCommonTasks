#!/bin/bash
# Done = a commit on the run branch whose subject holds "<id>: " in the owning repo (any repo for "*"),
# or an exceptions.tsv row.
cd "$(dirname "$0")"; G=$(cd ../../.. && pwd); B=feat/2026-11-01-full-skinning; done=0; all=0
ALL="Ka0sAddonsCommonTasks LibKa0s LibKa0sSkinTester AbsorbTracker AuraMaster BankLedger ConsumableMaster DpsRace DropWatcher KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PremadeGroupsFilterExtension PrettyChat QuickComms WhatGroup"
while IFS=$'\t' read -r id m repo t; do [ "$id" = id ] && continue; all=$((all+1)); hit=
 for r in $([ "$repo" = "*" ] && echo $ALL || echo $repo); do git -C "$G/$r" log --format=%s master..$B 2>/dev/null | grep -q "$id: " && hit=1 && break; done
 if [ -n "$hit" ] || grep -q "^$id"$'\t' exceptions.tsv; then done=$((done+1)); else echo "OPEN $id $repo"; fi
done < items.tsv; echo "TOTAL $done/$all"
echo "TAG v1.85.0 -> $(git -C "$G/LibKa0s" rev-parse --short v1.85.0^{commit}) (remote: $(git -C "$G/LibKa0s" ls-remote --tags origin v1.85.0 | wc -l))"
for r in $ALL; do s=$(git -C "$G/$r" status --porcelain | wc -l); [ "$s" != 0 ] && echo "DIRTY $r $s"; b=$(git -C "$G/$r" branch --show-current); [ "$b" != "$B" ] && echo "BRANCH $r $b"; done
