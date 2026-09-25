#!/bin/zsh
# Ka0s 2026-09-25 diagnostics rollout: what has landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " (or "<ID> + ...")
# exists in the repo items.tsv names, on the rollout branch or the default branch.
# Owner gates (OW-*) are commits in Ka0sAddonsCommonTasks. Items that land with no
# commit go in exceptions.tsv as "<ID>\t<reason with a proving command>".
#
#   ./resume-state.sh        # summary per milestone, ready items, dirty trees
#   ./resume-state.sh -v     # also list every remaining id
#   ./resume-state.sh M3     # one milestone
#
# Read-only. Exit 0 always.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-25-diagnostics-rollout
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
while IFS=$'\x1f' read -r id ms repo title deps effort smoke; do
  [[ $id == id || -z $id ]] && continue
  order+=$id; repo_[$id]=$repo; ms_[$id]=$ms; deps_[$id]=$deps
done < <(tr '\t' '\037' < $MANIFEST)

# Subjects per repo, from the rollout branch and the default branch.
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

echo "== diagnostics rollout ($BR)"
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
# Owner gates are listed apart: the executor never "does" one, it waits for the recorded ruling.
exec_ready=(); owner_ready=()
for id in $ready; do
  if [[ $id == DR-OW-* ]]; then owner_ready+=$id; else exec_ready+=$id; fi
done
echo "READY (executor): ${exec_ready[*]:-none}"
echo "WAITING ON OWNER: ${owner_ready[*]:-none}"

echo "== trees"
for r in ${(u)repo_}; do
  [[ -d $BASE/$r/.git ]] || { echo "$r: missing"; continue }
  b=$(git -C $BASE/$r branch --show-current)
  dirty=$(git -C $BASE/$r status --porcelain | wc -l)
  note=""
  [[ $r == AuraMaster && $b != $BR ]] && note=" (owned by another workflow until DR-OW-05; do not touch)"
  if [[ $r == LibKa0s && $b != $BR ]]; then
    tip=$(git -C $BASE/$r rev-parse --short feat/2026-09-25-draghandle-close 2>/dev/null)
    note=" (draghandle-close tip=$tip, planned base 53c141a; confirm no other workflow is using this tree before cutting $BR)"
  fi
  echo "$r: branch=$b dirty=$dirty$note"
done
echo "RESUME: run the READY items, one per repo at a time; owner gates (OW-*) are recorded, never assumed."
exit 0
