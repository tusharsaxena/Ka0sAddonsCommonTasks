#!/bin/zsh
# Ka0s 2026-09-29 smoke-test rework + profile verb. What has landed, straight from git.
#
# An item is DONE when a commit whose subject opens with "<ID>: " exists in the repo items.tsv names,
# on the feature branch or the default branch. REVIEWED when that commit, or its latest "<ID>R: " fix,
# carries a refs/notes/ka0s-review note starting "OK <ID>".
#
#   ./resume-state.sh        # summary per milestone, ready items, trees, tag
#   ./resume-state.sh -v     # also list every remaining / unreviewed id
#
# Read-only. Exit 0 always.

BASE=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-29-smoke-and-profile
TAG=v1.63.0
HERE=${0:A:h}
MANIFEST=$HERE/items.tsv
EXC=$HERE/exceptions.tsv
verbose=0; [[ "$1" == "-v" ]] && verbose=1

typeset -A DONE REVIEWED REPO DEPS MS
ids=()
while IFS=$'\t' read -r id ms repo title deps spec; do
  [[ $id == id ]] && continue
  ids+=$id; REPO[$id]=$repo; DEPS[$id]=$deps; MS[$id]=$ms
done < $MANIFEST

commit_for() { # repo id -> newest commit hash whose subject starts "<id>: " or "<id>R: "
  local r=$1 id=$2 refs=()
  git -C $BASE/$r rev-parse -q --verify $BR >/dev/null && refs+=$BR
  refs+=HEAD
  git -C $BASE/$r log --format='%H %s' $refs 2>/dev/null | grep -E "^[0-9a-f]+ ${id}R?: " | head -1 | cut -d' ' -f1
}

for id in $ids; do
  r=${REPO[$id]}
  if [[ -r $EXC ]] && grep -q "^${id}	" $EXC; then DONE[$id]=1; REVIEWED[$id]=1; continue; fi
  h=$(commit_for $r $id)
  [[ -n $h ]] || continue
  DONE[$id]=1
  note=$(git -C $BASE/$r notes --ref=ka0s-review show $h 2>/dev/null | head -1)
  [[ $note == "OK $id"* ]] && REVIEWED[$id]=1
done

for m in M0 M1 M2 M3 M4; do
  t=0; d=0; v=0
  for id in $ids; do [[ ${MS[$id]} == $m ]] || continue; ((t++)); [[ -n ${DONE[$id]} ]] && ((d++)); [[ -n ${REVIEWED[$id]} ]] && ((v++)); done
  echo "$m: done $d/$t, reviewed $v/$t"
done

echo "READY (every dependency done AND reviewed):"
for id in $ids; do
  [[ -n ${DONE[$id]} ]] && continue
  ok=1
  if [[ ${DEPS[$id]} == all ]]; then
    for o in $ids; do [[ $o == $id ]] && continue; [[ -z ${REVIEWED[$o]} ]] && ok=0; done
  else
    for dep in ${(s:,:)DEPS[$id]}; do [[ -n $dep && $dep != - && -z ${REVIEWED[$dep]} ]] && ok=0; done
  fi
  (( ok )) && echo "  $id (${REPO[$id]})"
done

if (( verbose )); then
  echo "NOT DONE:"; for id in $ids; do [[ -z ${DONE[$id]} ]] && echo "  $id"; done
  echo "DONE, NOT REVIEWED:"; for id in $ids; do [[ -n ${DONE[$id]} && -z ${REVIEWED[$id]} ]] && echo "  $id"; done
fi

echo "LibKa0s tag $TAG: $(git -C $BASE/LibKa0s rev-parse -q --verify refs/tags/$TAG >/dev/null && echo present || echo absent)"
echo "TREES:"
for r in ${(u)REPO}; do
  b=$(git -C $BASE/$r branch --show-current 2>/dev/null)
  dirty=$(git -C $BASE/$r status --porcelain 2>/dev/null | wc -l)
  if git -C $BASE/$r rev-parse -q --verify origin/$b >/dev/null; then
    ahead=$(git -C $BASE/$r log --oneline origin/$b..$b | wc -l)
  else
    ahead=never-pushed
  fi
  echo "  $r: branch=$b dirty=$dirty unpushed=$ahead"
done
exit 0
