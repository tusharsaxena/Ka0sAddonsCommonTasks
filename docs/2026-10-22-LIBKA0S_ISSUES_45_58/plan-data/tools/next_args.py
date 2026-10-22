"""Print the Workflow args for execute_milestone.js: the milestone's items that have NOT landed in git.

    python3 plan-data/tools/next_args.py M1                       # {"items": [...]} for the milestone's remainder
    python3 plan-data/tools/next_args.py M3 --repo LootHistory    # restrict to some repos (repeatable)
    python3 plan-data/tools/next_args.py M3 --order               # {"order": {repo: [ids]}}: serial per repo
    python3 plan-data/tools/next_args.py M1 --unreviewed          # landed items with no refs/notes/ka0s-review note

"Landed" uses the same rule as resume-state.sh: a commit whose subject starts "<ID>: " (or "<ID> + ") among
the run branch's commits on top of the repo's default branch (detected per repo; PGFE's is main), or a row in
exceptions.tsv. Dependencies on landed items are dropped from `deps`, so the scheduler treats them as satisfied.
"""
import json, os, subprocess, sys

BUNDLE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
BR = 'feat/2026-10-22-libka0s-issues-45-58'


def git(repo, *a):
    return subprocess.run(['git', '-C', f'{BASE}/{repo}', *a], capture_output=True, text=True)


def default_branch(repo):
    # bases.tsv pins a repo whose run branch was merged early to its pre-merge default-branch sha.
    if os.path.exists(f'{BUNDLE}/bases.tsv'):
        for line in open(f'{BUNDLE}/bases.tsv').read().splitlines()[1:]:
            f = line.split('\t')
            if len(f) > 1 and f[0] == repo:
                return f[1]
    r = git(repo, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD')
    return r.stdout.strip().split('/', 1)[1] if r.returncode == 0 and '/' in r.stdout else 'master'


args = sys.argv[1:]
ms = args[0]
repos = [args[i + 1] for i, a in enumerate(args) if a == '--repo']
unreviewed = '--unreviewed' in args
order = '--order' in args

items = json.load(open(f'{BUNDLE}/plan-data/items.json'))['items']
# Addenda (RESUME section 5) append items without editing the frozen plan.
import glob
for _a in sorted(glob.glob(f'{BUNDLE}/plan-data/addendum-*.json')):
    items += json.load(open(_a))['items']
excepted = set()
if os.path.exists(f'{BUNDLE}/exceptions.tsv'):
    for line in open(f'{BUNDLE}/exceptions.tsv').read().splitlines()[1:]:
        if line.strip():
            excepted.add(line.split('\t', 1)[0])

landed, reviewed = {}, set()
for repo in sorted({i['repo'] for i in items}):
    if git(repo, 'rev-parse', '--verify', '-q', BR).returncode != 0:
        continue
    out = git(repo, 'log', '--notes=ka0s-review', '--format=%x1e%s%x1f%N', f'{default_branch(repo)}..{BR}').stdout
    for rec in out.split('\x1e')[1:]:
        subj, _, note = rec.partition('\x1f')
        if ':' not in subj:
            continue
        for iid in subj.split(':', 1)[0].split(' + '):
            iid = iid.strip()
            landed[(repo, iid)] = True
            if note.strip():
                reviewed.add((repo, iid))
for i in items:
    if i['id'] in excepted:
        landed[(i['repo'], i['id'])] = True
        reviewed.add((i['repo'], i['id']))

sel = [i for i in items if i['milestone'] == ms and (not repos or i['repo'] in repos)]
if unreviewed:
    print(json.dumps([i['id'] for i in sel if (i['repo'], i['id']) in landed and (i['repo'], i['id']) not in reviewed]))
    sys.exit(0)
land_ids = {iid for (_, iid) in landed}
todo = [i for i in sel if (i['repo'], i['id']) not in landed]
if order:
    seq = {}
    for i in todo:
        seq.setdefault(i['repo'], []).append(i['id'])
    print(json.dumps({'order': seq}, separators=(',', ':')))
    print(f'# {len(todo)} of {len(sel)} {ms} items remaining (per-repo order)', file=sys.stderr)
    sys.exit(0)
print(json.dumps({'items': [{'id': i['id'], 'repo': i['repo'], 'deps': [d for d in i['depends_on'] if d not in land_ids]}
                            for i in todo]}))
print(f'# {len(todo)} of {len(sel)} {ms} items remaining', file=sys.stderr)
