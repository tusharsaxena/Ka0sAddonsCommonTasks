#!/bin/zsh
# Ka0s 2026-10-25 skinning run (leg 1): what has actually landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " exists in the repo that owns it, among
# the run branch's commits on top of that repo's default branch.
# A commit may carry several ids: "LK-01 + LK-02: ...". Items that legitimately land with no commit go in
# exceptions.tsv, each with a command in the reason column that a reader can run to check the claim.
#
#   ./resume-state.sh          # summary per milestone
#   ./resume-state.sh -v       # also list every remaining item id
#   ./resume-state.sh M3       # one milestone
#
# Exit 0 always. Prints a RESUME line naming exactly what to hand the next run.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-10-25-skinning
HERE=${0:A:h}
MANIFEST=$HERE/items.tsv
IDRE='^[A-Z]{2}-[A-Z0-9]+$'

[[ -r $MANIFEST ]] || { echo "missing $MANIFEST"; exit 0 }
# Addenda (RESUME section 5) append rows without editing the frozen manifest.
manifest_rows() { tail -q -n +2 $MANIFEST $HERE/plan-data/addendum-*.tsv(N) }

verbose=0; only=""
for a in "$@"; do
  case $a in
    -v) verbose=1 ;;
    M[0-9]) only=$a ;;
  esac
done

# bases.tsv pins a repo whose run branch was merged early to its pre-merge default-branch sha.
defbr() { local b; b=$(awk -F'\t' -v r=$1 'NR>1 && $1==r {print $2}' ${0:A:h}/bases.tsv 2>/dev/null); [[ -n $b ]] && { print -- $b; return }; b=$(git -C $BASE/$1 symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null); print -- ${${b#*/}:-master} }

typeset -A landed
for r in $(manifest_rows | cut -f3 | sort -u); do
  [[ -d $BASE/$r/.git ]] || continue
  git -C $BASE/$r rev-parse --verify -q $BR >/dev/null 2>&1 || continue
  subjects=$(git -C $BASE/$r log --format='%s' $(defbr $r)..$BR 2>/dev/null)
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
  done < <(manifest_rows)
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

for m in M1 M2 M3 M4; do
  [[ -n $only && $only != $m ]] && continue
  ur=$(python3 $HERE/plan-data/tools/next_args.py $m --unreviewed 2>/dev/null | tr -d '[]"' | tr ',' ' ')
  [[ -n ${ur// } ]] && echo "-- $m landed, review not recorded:${ur}"
done

[[ -r $HERE/checkpoints.tsv ]] && echo "-- last checkpoint: $(tail -n 1 $HERE/checkpoints.tsv | tr '\t' ' ')"

echo
echo "-- LibKa0s tag v1.78.0: $(git -C $BASE/LibKa0s rev-parse -q --short 'v1.78.0^{commit}' 2>/dev/null || echo absent) (local; pushed: $(git -C $BASE/LibKa0s ls-remote --tags origin v1.78.0 2>/dev/null | grep -q . && echo YES || echo no))"
echo "-- installed dev-copilot: $(ls ~/.claude/plugins/cache/dev-copilot/dev-copilot 2>/dev/null | sort -V | tail -1) "
dirty=""; offbranch=""
for r in $(manifest_rows | cut -f3 | sort -u); do
  [[ -d $BASE/$r/.git ]] || continue
  n=$(git -C $BASE/$r status --porcelain | wc -l | tr -d ' ')
  [[ $n != 0 ]] && dirty="$dirty $r($n)"
  b=$(git -C $BASE/$r branch --show-current)
  [[ $b != $BR ]] && offbranch="$offbranch $r($b)"
done
echo "-- dirty trees: ${dirty:-none}"
echo "-- not on $BR: ${offbranch:-none}"
exit 0
