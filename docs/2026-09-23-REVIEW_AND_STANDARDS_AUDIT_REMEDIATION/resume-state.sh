#!/bin/zsh
# Ka0s 2026-09-23 remediation — what has actually landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " exists in the
# repo that owns it, on the remediation branch or the repo's default branch.
# That is the only definition used in this cycle, and it is checkable without
# trusting any notes. A commit may carry several ids: "LK-01 + LK-02: ...".
#
# Items that legitimately land with no commit go in exceptions.tsv, each with a
# command in the reason column that a reader can run to check the claim.
#
#   ./resume-state.sh          # summary per milestone
#   ./resume-state.sh -v       # also list every remaining item id
#   ./resume-state.sh M3       # one milestone
#
# Exit 0 always. Prints a RESUME line naming exactly what to hand the next run.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-23-review-audit-remediation
HERE=${0:A:h}
MANIFEST=$HERE/items.tsv
IDRE='^(WS|LK|WA|RV|AT|AM|BL|CM|KC|LH|MM|PM|PF|PC|WG|REC)-[A-Z0-9]+$'

[[ -r $MANIFEST ]] || { echo "missing $MANIFEST"; exit 0 }

verbose=0; only=""
for a in "$@"; do
  case $a in
    -v) verbose=1 ;;
    M[0-9]) only=$a ;;
  esac
done

typeset -A landed
for r in $(tail -n +2 $MANIFEST | cut -f3 | sort -u); do
  [[ -d $BASE/$r/.git ]] || continue
  refs=()
  for ref in $BR master main; do
    git -C $BASE/$r rev-parse --verify -q $ref >/dev/null 2>&1 && refs+=$ref
  done
  (( ${#refs} )) || continue
  subjects=$(git -C $BASE/$r log --format='%s' $refs 2>/dev/null)
  for s in ${(f)subjects}; do
    [[ $s == *:* ]] || continue
    for id in ${(s: + :)${s%%:*}}; do
      [[ $id =~ $IDRE ]] && landed[$r/$id]=1
    done
  done
done

EXC=$HERE/exceptions.tsv
typeset -A excepted
if [[ -r $EXC ]]; then
  while IFS=$'\t' read -r id reason; do
    [[ $id =~ $IDRE ]] && excepted[$id]=1
  done < $EXC
fi

total_done=0; total_all=0; typeset -a resume_all
for m in M1 M2 M3 M4; do
  [[ -n $only && $only != $m ]] && continue
  typeset -a todo done_ids
  todo=(); done_ids=()
  while IFS=$'\t' read -r id mi repo title; do
    [[ $mi == $m ]] || continue
    if [[ -n ${landed[$repo/$id]} || -n ${excepted[$id]} ]]; then done_ids+=$id; else todo+=$id; fi
  done < <(tail -n +2 $MANIFEST)
  n=$(( ${#done_ids} + ${#todo} ))
  (( n == 0 )) && continue
  total_done=$(( total_done + ${#done_ids} )); total_all=$(( total_all + n ))
  state="not started"
  (( ${#done_ids} > 0 )) && state="in flight"
  (( ${#todo} == 0 ))    && state="COMPLETE"
  printf '%-3s %3d/%-3d  %s\n' $m ${#done_ids} $n $state
  (( verbose && ${#todo} )) && print -- "     remaining: ${todo}"
  resume_all+=($todo)
done

echo
printf 'TOTAL %d/%d items landed\n' $total_done $total_all
if (( ${#resume_all} )); then
  echo "RESUME: ${resume_all[1,40]}${resume_all[41]:+ ...}"
else
  echo "RESUME: nothing outstanding"
fi

# Landed but never closed by a review (no refs/notes/ka0s-review note). A resumed executor
# re-reviews these; the list is informational here.
for m in M1 M2 M3 M4; do
  [[ -n $only && $only != $m ]] && continue
  ur=$(python3 $HERE/plan-data/tools/next_args.py $m --unreviewed 2>/dev/null | tr -d '[]"' | tr ',' ' ')
  [[ -n ${ur// } ]] && echo "-- $m landed, review not recorded:${ur}"
done

# Last recorded checkpoint.
[[ -r $HERE/checkpoints.tsv ]] && echo "-- last checkpoint: $(tail -n 1 $HERE/checkpoints.tsv | tr '\t' ' ')"

echo
echo "-- LibKa0s tag v1.56.0: $(git -C $BASE/LibKa0s tag -l v1.56.0 | grep -q . && echo 'present (local)' || echo absent)"
dirty=""; offbranch=""
for r in $(tail -n +2 $MANIFEST | cut -f3 | sort -u) Ka0sAddonsCommonTasks; do
  [[ -d $BASE/$r/.git ]] || continue
  n=$(git -C $BASE/$r status --porcelain | wc -l | tr -d ' ')
  [[ $n != 0 ]] && dirty="$dirty $r($n)"
  b=$(git -C $BASE/$r branch --show-current)
  [[ $b != $BR ]] && offbranch="$offbranch $r($b)"
done
echo "-- dirty trees: ${dirty:-none}"
echo "-- not on $BR: ${offbranch:-none}"
exit 0
