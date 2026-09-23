"""Print the Workflow args for execute_milestone.js: the milestone's items that have NOT landed in git.

    python3 plan-data/tools/next_args.py M2            # {"items": [...]} for the whole milestone's remainder
    python3 plan-data/tools/next_args.py M3 --repo KickCD --repo PrettyChat   # restrict to some repos
    python3 plan-data/tools/next_args.py M1 --unreviewed   # landed items with no refs/notes/ka0s-review note

"Landed" uses the same rule as resume-state.sh: a commit whose subject starts "<ID>: " (or "<ID> + ") on the
remediation branch or the default branch of the owning repo. Dependencies on landed items are dropped from
`deps`, so the scheduler treats them as satisfied.
"""
import json, os, re, subprocess, sys

BUNDLE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
BR = 'feat/2026-09-23-review-audit-remediation'
args = sys.argv[1:]
ms = args[0]
repos = [args[i + 1] for i, a in enumerate(args) if a == '--repo']
unreviewed = '--unreviewed' in args

items = json.load(open(f'{BUNDLE}/plan-data/items.json'))['items']
landed, reviewed = {}, set()
for repo in sorted({i['repo'] for i in items}):
    refs = [r for r in (BR, 'master', 'main')
            if subprocess.run(['git', '-C', f'{BASE}/{repo}', 'rev-parse', '--verify', '-q', r], capture_output=True).returncode == 0]
    if not refs:
        continue
    out = subprocess.run(['git', '-C', f'{BASE}/{repo}', 'log', '--notes=ka0s-review', '--format=%x1e%s%x1f%N', *refs],
                         capture_output=True, text=True).stdout
    for rec in out.split('\x1e')[1:]:
        subj, _, note = rec.partition('\x1f')
        if ':' not in subj:
            continue
        for iid in subj.split(':', 1)[0].split(' + '):
            iid = iid.strip()
            landed[(repo, iid)] = True
            if note.strip():
                reviewed.add((repo, iid))

sel = [i for i in items if i['milestone'] == ms and (not repos or i['repo'] in repos)]
if unreviewed:
    rows = [i['id'] for i in sel if (i['repo'], i['id']) in landed and (i['repo'], i['id']) not in reviewed]
    print(json.dumps(rows))
    sys.exit(0)
land_ids = {iid for (_, iid) in landed}
todo = [i for i in sel if (i['repo'], i['id']) not in landed]
print(json.dumps({'items': [{'id': i['id'], 'repo': i['repo'], 'deps': [d for d in i['depends_on'] if d not in land_ids]}
                            for i in todo]}))
print(f'# {len(todo)} of {len(sel)} {ms} items remaining', file=sys.stderr)
