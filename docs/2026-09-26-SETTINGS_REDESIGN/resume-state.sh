#!/bin/zsh
# Ka0s 2026-09-26 AuraMaster settings redesign (#6): what has landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " (or "<ID> + ...", or a review fix
# "<ID>R: ") exists in the repo items.tsv names, on the redesign branch or the default branch.
# Items that land with no commit go in exceptions.tsv as "<ID>\t<reason with a proving command>".
# One exception: SR-LK-03 (the release) is done only once the local tag v1.61.0 also exists.
#
#   ./resume-state.sh        # summary per milestone, ready items, trees, the local tag
#   ./resume-state.sh -v     # also list every remaining id
#   ./resume-state.sh M2     # one milestone
#
# Read-only. Exit 0 always.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-26-settings-redesign
TAG=v1.61.0
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

typeset -A done_ repo_ ms_ deps_
typeset -a order
# Tab is IFS whitespace in zsh, so empty columns would collapse; split on \x1f instead.
while IFS=$'\x1f' read -r id ms repo title deps effort smoke traces; do
  [[ $id == id || -z $id ]] && continue
  order+=$id; repo_[$id]=$repo; ms_[$id]=$ms; deps_[$id]=$deps
done < <(tr '\t' '\037' < $MANIFEST)

# Subjects per repo, from the redesign branch and the default branch.
typeset -A subjects
for r in ${(u)repo_}; do
  [[ -d $BASE/$r/.git ]] || continue
  refs=()
  for ref in $BR master main; do
    git -C $BASE/$r rev-parse --verify -q $ref >/dev/null 2>&1 && refs+=$ref
  done
  (( ${#refs} )) && subjects[$r]=$(git -C $BASE/$r log --format=%s ${refs[@]} 2>/dev/null)
done

for id in $order; do
  s=${subjects[${repo_[$id]}]}
  if print -r -- "$s" | grep -qE "(^|\+ )${id}(:| \+)"; then done_[$id]=1; fi
  if [[ -r $EXC ]] && cut -f1 $EXC | grep -qx "$id"; then done_[$id]=1; fi
done

# SR-LK-03 makes two commits and then the local tag (docs/releasing.md step 7). A subject alone marks
# it done at its FIRST commit, before the release battery, the analysis and the tag exist, which would
# list SR-AM-01 as READY too early. So the release item also needs the tag, and until then it reads
# as in progress and holds everything behind it.
typeset -A partial_
tagged=$(git -C $BASE/LibKa0s rev-parse --short -q --verify "$TAG^{}" 2>/dev/null)
if [[ -n ${done_[SR-LK-03]} && -z $tagged ]]; then
  unset "done_[SR-LK-03]"
  partial_[SR-LK-03]="commit(s) landed, $TAG not tagged yet: finish SR-LK-03 Steps 4-6"
fi

echo "== settings redesign ($BR)"
for m in M1 M2 M3; do
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
for id in ${(k)partial_}; do echo "IN PROGRESS: $id -- ${partial_[$id]}"; done

echo "== trees"
for r in ${(u)repo_}; do
  [[ -d $BASE/$r/.git ]] || { echo "$r: missing"; continue }
  b=$(git -C $BASE/$r branch --show-current)
  dirty=$(git -C $BASE/$r status --porcelain | wc -l)
  note=""
  [[ $r != Ka0sAddonsCommonTasks && $b != $BR ]] && note=" (expected $BR; cut it from master if no item in this repo has landed)"
  (( dirty )) && [[ $r != Ka0sAddonsCommonTasks ]] && note="$note (dirty: an interrupted item's work -- continue it or stash it, never discard it)"
  echo "$r: branch=$b dirty=$dirty$note"
done
echo "LibKa0s $TAG: ${tagged:-not tagged yet} (local only; never pushed by this run)"
echo "RESUME: run the READY items, one per repo at a time; M1's two repos run in parallel; AuraMaster's items in order."
exit 0
