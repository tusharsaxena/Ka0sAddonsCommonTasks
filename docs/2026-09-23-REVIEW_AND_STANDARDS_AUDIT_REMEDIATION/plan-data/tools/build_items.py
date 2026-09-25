import json, sys
D = sys.argv[1]
R = json.load(open(f"{D}/plan-data/raw_plan.json"))
up = R['upstream']; plans = R['plans']
AB = {'AbsorbTracker': 'AT', 'AuraMaster': 'AM', 'BankLedger': 'BL', 'ConsumableMaster': 'CM', 'KickCD': 'KC', 'LootHistory': 'LH',
      'MultiMeters': 'MM', 'PanelMaster': 'PM', 'PartyFrameEnhanced': 'PF', 'PrettyChat': 'PC', 'WhatGroup': 'WG'}
B = '/home/tushar/.claude/wow-addon/bin/ka0s-bounded'
tag = up['new_libka0s_tag']
items = []
for i in up['items']:
    items.append(dict(i, milestone='M1'))
for repo, ab in AB.items():
    items.append({
        'id': f'RV-{ab}', 'repo': repo, 'milestone': 'M2',
        'title': f'Re-vendor the whole LibKa0s {tag} payload into {repo}',
        'change': (f'Copy ../LibKa0s/LibKa0s/ -> libs/LibKa0s/ and ../LibKa0s/testkit/ -> tests/_kit/ WHOLE from the local tag {tag} '
                   f'(git -C ../LibKa0s archive or worktree at the tag; rm -rf then copy; keep the runner executable), and roll the '
                   f'CLAUDE.md provenance line to {tag} in the same commit. No other edits. If the suite goes red because the new '
                   f'kit/library is stricter, record the failures in the commit body; the fixes are this addon\'s M3 items.'),
        'tests': 'none - payload copy; the suite run is the verification',
        'verify': (f'diff -r <tag checkout>/LibKa0s libs/LibKa0s and diff -r <tag checkout>/testkit tests/_kit both empty; '
                   f'{B} luacheck .; {B} lua5.1 tests/run.lua'),
        'smoke': '', 'finding_ids': [], 'issue_refs': [], 'depends_on': ['LK-33'], 'effort': 'S'})
for repo, p in plans.items():
    for i in p['items']:
        d = dict(i, milestone='M3')
        if not any(x.startswith('RV-') for x in d['depends_on']):
            d['depends_on'] = [f'RV-{AB[repo]}'] + d['depends_on']
        items.append(d)
json.dump({'tag': tag, 'items': items,
           'dispositions': {r: p['dispositions'] for r, p in plans.items()},
           'consumer_followups': up['consumer_followups'], 'upstream_notes': up['notes'],
           'plan_notes': {r: p['notes'] for r, p in plans.items()}},
          open(f"{D}/plan-data/items.json", 'w'), indent=1)
print(len(items))
