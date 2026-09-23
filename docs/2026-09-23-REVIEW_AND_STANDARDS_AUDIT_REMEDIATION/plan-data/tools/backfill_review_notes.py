"""Record refs/notes/ka0s-review notes for items a workflow reviewed, from its journal.jsonl.

    python3 plan-data/tools/backfill_review_notes.py <journal.jsonl> [--dry-run]

Used for runs started before the executor wrote notes itself (the M1 run wf_9a447572-ab2). An item is
noted when its journal shows a finished review with ok=true, or a finished fix round. The note goes on the
item's newest commit on the remediation branch. Re-running is safe (-f overwrites the same note).
"""
import json, os, subprocess, sys

BASE = '/mnt/d/Profile/Users/Tushar/Documents/GIT'
BR = 'feat/2026-09-23-review-audit-remediation'
BUNDLE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
journal, dry = sys.argv[1], '--dry-run' in sys.argv
repo_of = {i['id']: i['repo'] for i in json.load(open(f'{BUNDLE}/plan-data/items.json'))['items']}

rows = [json.loads(l) for l in open(journal)]
label = {r['key']: r.get('label', '') for r in rows if r['type'] == 'started'}
closed = {}
for r in rows:
    if r['type'] != 'result':
        continue
    lab = label.get(r.get('key'), '')
    kind, _, iid = lab.partition(':')
    res = r.get('result') or {}
    if kind == 'review' and isinstance(res, dict) and res.get('ok'):
        closed[iid] = 'reviewed ok'
    elif kind == 'fix' and isinstance(res, dict):
        closed[iid] = 'reviewed, fixed'

for iid, what in sorted(closed.items()):
    repo = repo_of.get(iid)
    if not repo:
        continue
    log = subprocess.run(['git', '-C', f'{BASE}/{repo}', 'log', '--format=%H %s', BR], capture_output=True, text=True).stdout
    shas = [l.split(' ', 1)[0] for l in log.splitlines() if l.split(' ', 1)[1].startswith((f'{iid}:', f'{iid} + '))]
    if not shas:
        print(f'{iid}: no commit found, skipped'); continue
    cmd = ['git', '-C', f'{BASE}/{repo}', 'notes', '--ref=ka0s-review', 'add', '-f', '-m', f'{what} {iid} (backfilled from journal)', shas[0]]
    print(('DRY ' if dry else '') + f'{iid} -> {repo} {shas[0][:7]} ({what})')
    if not dry:
        subprocess.run(cmd, check=True, capture_output=True)
