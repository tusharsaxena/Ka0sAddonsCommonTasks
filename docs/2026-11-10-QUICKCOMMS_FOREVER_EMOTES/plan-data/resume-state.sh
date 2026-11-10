#!/usr/bin/env bash
# Progress from git alone: an item is done when a commit whose subject starts "<ID>: " (or "<ID> + ")
# exists on the run branch of its repo, or when exceptions.tsv lists it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
GIT="$(cd "$HERE/../../../.." && pwd)"
BR=feat/2026-11-10-quickcomms-forever-emotes
done=0; total=0
while IFS=$'\t' read -r id ms repo title deps rest; do
  [ "$id" = id ] && continue
  total=$((total+1)); d="$GIT/$repo"; state=TODO
  if cut -f1 "$HERE/exceptions.tsv" | grep -qx "$id"; then state=DONE-EXC
  elif git -C "$d" rev-parse -q --verify "$BR" >/dev/null 2>&1 &&
       git -C "$d" log "$BR" --format=%s | grep -qE "(^|\+ )$id(:| \+)"; then state=DONE
  elif git -C "$d" log master --since=2026-11-10 --format=%s 2>/dev/null | grep -qE "(^|\+ )$id(:| \+)"; then state=DONE-MERGED
  fi
  case $state in DONE*) done=$((done+1));; esac
  printf '%-11s %-4s %-22s %-11s %s\n' "$id" "$ms" "$repo" "$state" "$title"
done < "$HERE/items.tsv"
echo "---- $done / $total done"
for r in QuickComms DpsRace LibKa0s LibKa0sSkinTester WowAddonStandards Ka0sAddonsCommonTasks; do
  printf '%-22s branch=%s dirty=%s\n' "$r" "$(git -C "$GIT/$r" branch --show-current)" "$(git -C "$GIT/$r" status --porcelain | wc -l)"
done
