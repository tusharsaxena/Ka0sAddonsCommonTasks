#!/usr/bin/env bash
# Round 7 progress, computed from git. WowAddonStandards is read from its worktree.
G=/mnt/d/Profile/Users/Tushar/Documents/GIT; B=feat/2026-11-04-smoke-round7; D=$(dirname "$0")
ALL="WowAddonStandards LibKa0s LibKa0sSkinTester AbsorbTracker AuraMaster BankLedger ConsumableMaster DpsRace DropWatcher KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PremadeGroupsFilterExtension PrettyChat QuickComms WhatGroup Ka0sAddonsCommonTasks"
path() { [ "$1" = WowAddonStandards ] && echo "$G/.worktrees/WowAddonStandards-r7" || echo "$G/$1"; }
done=0; tot=0
while IFS=$'\t' read -r id m repo title; do [ "$id" = id ] && continue; tot=$((tot+1)); hit=0
  for r in $([ "$repo" = "*" ] && echo $ALL || echo $repo); do git -C "$(path $r)" log --format=%s master..$B 2>/dev/null | grep -qE "(^|\+ )$id( \+ [A-Z0-9-]+)*: " && hit=1 && break; done
  grep -q "^$id"$'\t' "$D/exceptions.tsv" && hit=1
  [ $hit = 1 ] && done=$((done+1)) || echo "OPEN $id $repo"; done < "$D/items.tsv"
echo "TOTAL $done/$tot"
for r in $ALL; do p=$(path $r); s=$(git -C "$p" status --porcelain | wc -l); [ "$s" != 0 ] && echo "DIRTY $r $s"; b=$(git -C "$p" branch --show-current); [ "$b" != "$B" ] && echo "BRANCH $r $b"; done
