#!/bin/zsh
# Ka0s 2026-09-26 automated-tests sweep: fix everything the sweep queued (00_FIX_QUEUE.md, ATS-01..24),
# then re-run the battery everywhere. What has landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " (or "<ID> + ...") exists in the repo
# items.tsv names, on the sweep branch or the default branch. "<ID>R: " is a review fix on a done item.
# Items that land with no commit go in exceptions.tsv as "<ID>\t<reason with a proving command>".
#
#   ./resume-state.sh        # summary per milestone, READY items, trees, local tag
#   ./resume-state.sh -v     # also list every remaining id
#   ./resume-state.sh M2     # one milestone
#
# Read-only. Exit 0 always.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-26-automated-tests-sweep
TAG=v1.62.0
HERE=${0:A:h}
MANIFEST=$HERE/items.tsv
EXC=$HERE/exceptions.tsv

[[ -r $MANIFEST ]] || { echo "missing $MANIFEST"; exit 0 }

verbose=0; only=""
for a in "$@"; do
  case $a in
    -v) verbose=1 ;;
    M[0-9]) only=$a ;;
  esac
done

typeset -A done_ repo_ ms_ deps_ reviewed_
typeset -a order
while IFS=$'\x1f' read -r id ms repo title deps effort traces; do
  [[ $id == id || -z $id ]] && continue
  order+=$id; repo_[$id]=$repo; ms_[$id]=$ms; deps_[$id]=$deps
done < <(tr '\t' '\037' < $MANIFEST)

typeset -A subjects
for r in ${(u)repo_}; do
  [[ -d $BASE/$r/.git ]] || continue
  refs=()
  for ref in $BR master main; do
    git -C $BASE/$r rev-parse --verify -q $ref >/dev/null 2>&1 && refs+=$ref
  done
  (( ${#refs} )) && subjects[$r]=$(git -C $BASE/$r log --format='%H %s' ${refs[@]} 2>/dev/null)
done

unrev=()
for id in $order; do
  s=${subjects[${repo_[$id]}]}
  line=$(print -r -- "$s" | grep -E "^[0-9a-f]+ (.*\+ )?${id}(:| \+)" | head -1)
  if [[ -n $line ]]; then
    done_[$id]=1
    sha=${line%% *}
    if git -C $BASE/${repo_[$id]} notes --ref=ka0s-review show $sha >/dev/null 2>&1; then reviewed_[$id]=1
    elif [[ ${ms_[$id]} == M[12] ]]; then unrev+=$id; fi
  fi
  if [[ -r $EXC ]] && cut -f1 $EXC | grep -qx "$id"; then done_[$id]=1; reviewed_[$id]=1; fi
done

echo "== automated-tests sweep ($BR)"
for m in M0 M1 M2 M3 M4; do
  [[ -n $only && $m != $only ]] && continue
  total=0; d=0; rem=()
  for id in $order; do
    [[ ${ms_[$id]} == $m ]] || continue
    (( total++ ))
    if [[ -n ${done_[$id]} ]]; then (( d++ )); else rem+=$id; fi
  done
  (( total )) || continue
  st=""; (( d == total )) && st=" COMPLETE"
  echo "$m: $d/$total$st"
  (( verbose && ${#rem} )) && echo "   remaining: ${rem[*]}"
done

ready=()
for id in $order; do
  [[ -n ${done_[$id]} ]] && continue
  [[ -n $only && ${ms_[$id]} != $only ]] && continue
  ok=1
  for dep in ${(s:,:)deps_[$id]}; do
    [[ -z $dep ]] && continue
    [[ -n ${done_[$dep]} ]] || { ok=0; break }
  done
  (( ok )) && ready+=$id
done
echo "READY: ${ready[*]:-none}"
echo "LANDED, REVIEW NOT RECORDED: ${unrev[*]:-none}"

tagged=$(git -C $BASE/LibKa0s rev-parse --short -q --verify "$TAG^{}" 2>/dev/null)
echo "LibKa0s local tag $TAG: ${tagged:-not yet (made by LK-ATS-10; every *-ATS-RV copies from it)}"

echo "== trees"
for r in ${(u)repo_}; do
  [[ -d $BASE/$r/.git ]] || { echo "$r: missing"; continue }
  b=$(git -C $BASE/$r branch --show-current)
  dirty=$(git -C $BASE/$r status --porcelain | wc -l)
  note=""
  [[ $b != $BR ]] && note=" (expected $BR)"
  (( dirty )) && note="$note (dirty: an interrupted item's work -- continue it or stash it, never discard it)"
  echo "$r: branch=$b dirty=$dirty$note"
done
exit 0
