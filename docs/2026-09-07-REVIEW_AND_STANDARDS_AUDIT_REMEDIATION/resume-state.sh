#!/bin/zsh
# Ka0s 2026-09-07 remediation — what has actually landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " exists on the
# remediation branch of the repo that owns it. That is the only definition used
# anywhere in this cycle, and it is checkable without trusting any notes.
#
# Two items legitimately land with NO commit — M1-LK-00 repairs working-tree
# bytes against an index that is already correct, and M4-03 is a smoke-only
# session. Those live in exceptions.tsv with the evidence that closed them, and
# a resume must not re-run them. An id may only be added to that file with a
# command in the reason column that a reader can run to check the claim.
#
#   ./resume-state.sh          # summary per milestone
#   ./resume-state.sh -v       # also list every remaining item id
#   ./resume-state.sh M2       # one milestone
#
# Exit 0 always. Prints a RESUME line naming exactly what to hand the next run.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-07-audit-review-remediation
HERE=${0:A:h}
MANIFEST=$HERE/items.tsv

[[ -r $MANIFEST ]] || { echo "missing $MANIFEST"; exit 0 }

verbose=0; only=""
for a in "$@"; do
  case $a in
    -v) verbose=1 ;;
    M[1-5]) only=$a ;;
  esac
done

# Collect every landed item id across all repos, once.
typeset -A landed
for r in $(cut -f3 $MANIFEST | sort -u); do
  [[ -d $BASE/$r/.git ]] || continue
  # master..BR is the branch's own work; fall back to the whole branch if master
  # is absent or the branch was created from something else.
  ids=$(git -C $BASE/$r log --format='%s' master..$BR 2>/dev/null \
        || git -C $BASE/$r log --format='%s' $BR 2>/dev/null)
  for s in ${(f)ids}; do
    # Everything before the first colon is the id list. Usually one id, but a
    # commit that squashes a gate into its fix carries both -- "M1-LK-01 +
    # M1-LK-02: ..." -- and reading that as a single id marks BOTH outstanding
    # forever. Split on " + " and credit each.
    for id in ${(s: + :)${s%%:*}}; do
      [[ $id == M[1-5]-* ]] && landed[$id]=$r
    done
  done
done

# Items that complete without producing a commit, with the evidence that closed them.
EXC=$HERE/exceptions.tsv
if [[ -r $EXC ]]; then
  while IFS=$'\t' read -r id reason; do
    [[ $id == M[1-5]-* ]] || continue
    [[ -n ${landed[$id]} ]] || landed[$id]="(no commit)"
  done < $EXC
fi

total_done=0; total_all=0; typeset -a resume_all
for m in M1 M2 M3 M4 M5; do
  [[ -n $only && $only != $m ]] && continue
  typeset -a todo done_ids
  todo=(); done_ids=()
  while IFS=$'\t' read -r id mi repo desc; do
    [[ $mi == $m ]] || continue
    if [[ -n ${landed[$id]} ]]; then done_ids+=$id; else todo+=$id; fi
  done < $MANIFEST
  n=$(( ${#done_ids} + ${#todo} ))
  (( n == 0 )) && continue
  total_done=$(( total_done + ${#done_ids} )); total_all=$(( total_all + n ))
  state="not started"
  (( ${#done_ids} > 0 )) && state="in flight"
  (( ${#todo} == 0 ))    && state="COMPLETE"
  printf '%-3s %3d/%-3d  %s\n' $m ${#done_ids} $n $state
  if (( verbose && ${#todo} )); then
    print -- "     remaining: ${todo}"
  fi
  resume_all+=($todo)
done

echo
printf 'TOTAL %d/%d items landed\n' $total_done $total_all
if (( ${#resume_all} )); then
  echo "RESUME: ${resume_all}"
else
  echo "RESUME: nothing outstanding"
fi

# Tags and working-tree cleanliness, because both gate the later milestones.
echo
echo "-- LibKa0s tags:  $(git -C $BASE/LibKa0s tag -l 'v1.2[67].0' | tr '\n' ' ')"
dirty=""
for r in $(cut -f3 $MANIFEST | sort -u) Ka0sAddonsCommonTasks; do
  [[ -d $BASE/$r/.git ]] || continue
  n=$(git -C $BASE/$r status --porcelain | wc -l | tr -d ' ')
  [[ $n != 0 ]] && dirty="$dirty $r($n)"
done
echo "-- dirty trees: ${dirty:-none}"
