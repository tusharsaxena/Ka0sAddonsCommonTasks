#!/usr/bin/env python3
"""Assemble the final plan manifest from the per-repo drafts and the plan critic's patches.

Inputs:  plan-data/items/<Repo>.json  ({"repo": ..., "items": [...]})
         plan-data/critic_patches.json ([{"op": "replace"|"add", "id", "item": <JSON string>, "reason"}])
Outputs: plan-data/items.json          ({"items": [...]}, M1 upstreams, M2 RV-* in addon order, M3 per addon)
         items.tsv                     (id, milestone, repo, title, depends_on, effort, smoke, finding_ids)
Then validates the manifest against inputs/verified_findings.json and exits non-zero on any failure.

Usage: python3 plan-data/tools/assemble.py          # assemble + validate
       python3 plan-data/tools/assemble.py --check  # validate the existing items.json only
"""
import json
import os
import sys

BUNDLE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PD = os.path.join(BUNDLE, 'plan-data')

UPSTREAMS = ['WowAddonStandards', 'LibKa0s', 'dev-copilot']
# Addons in ADDONS.md order (alphabetical by folder).
ADDONS = ['AbsorbTracker', 'AuraMaster', 'BankLedger', 'ConsumableMaster', 'KickCD', 'LootHistory',
          'MultiMeters', 'PanelMaster', 'PartyFrameEnhanced', 'PrettyChat', 'WhatGroup']

# Where an added item sits in its repo's list (the M3 runner's --order mode is list order).
PLACE = {
    'DC-15': ('before', 'DC-12'),
    'LH-18': ('after', 'LH-08'),
    'BL-05': ('before', 'BL-STD'),
    'CM-09': ('before', 'CM-STD'),
    'PF-06': ('before', 'PF-STD'),
    'WG-07': ('before', 'WG-STD'),
}


def load_drafts():
    per_repo = {}
    for repo in UPSTREAMS + ADDONS:
        d = json.load(open(os.path.join(PD, 'items', f'{repo}.json'), encoding='utf-8'))
        per_repo[repo] = list(d['items'])
    return per_repo


def apply_patches(per_repo):
    patches = json.load(open(os.path.join(PD, 'critic_patches.json'), encoding='utf-8'))
    for p in patches:
        item = json.loads(p['item'])
        assert item['id'] == p['id'], p['id']
        lst = per_repo[item['repo']]
        idx = [i for i, x in enumerate(lst) if x['id'] == p['id']]
        if p['op'] == 'replace':
            assert len(idx) == 1, f"replace target {p['id']} not found once"
            lst[idx[0]] = item
        elif p['op'] == 'add':
            assert not idx, f"add target {p['id']} already exists"
            where, anchor = PLACE[p['id']]
            a = [i for i, x in enumerate(lst) if x['id'] == anchor]
            assert len(a) == 1, f"anchor {anchor} for {p['id']} not found"
            lst.insert(a[0] + (1 if where == 'after' else 0), item)
        else:
            raise SystemExit(f"unknown op {p['op']}")
    return len(patches)


def order(per_repo):
    out = []
    for repo in UPSTREAMS:
        out += [i for i in per_repo[repo] if i['milestone'] == 'M1']
    for repo in ADDONS:
        out += [i for i in per_repo[repo] if i['milestone'] == 'M2']
    for repo in ADDONS:
        out += [i for i in per_repo[repo] if i['milestone'] == 'M3']
    allitems = [i for r in per_repo.values() for i in r]
    missing = {i['id'] for i in allitems} - {i['id'] for i in out}
    assert not missing, f'items outside M1-M3 or misplaced: {sorted(missing)}'
    return out


def write(items):
    with open(os.path.join(PD, 'items.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'items': items}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    cols = ['id', 'milestone', 'repo', 'title', 'depends_on', 'effort', 'smoke', 'finding_ids']
    with open(os.path.join(BUNDLE, 'items.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(cols) + '\n')
        for i in items:
            row = [i['id'], i['milestone'], i['repo'], i['title'].replace('\t', ' '),
                   ','.join(i['depends_on']), i['effort'],
                   'yes' if (i.get('smoke') or '').strip() else '', ','.join(i['finding_ids'])]
            f.write('\t'.join(row) + '\n')


def validate(items):
    errs = []
    vf = json.load(open(os.path.join(BUNDLE, 'inputs', 'verified_findings.json'), encoding='utf-8'))
    in_scope = {f['id'] for f in vf['findings'] if f['needs_addressing'] != 'no'}
    out_scope = {f['id'] for f in vf['findings'] if f['needs_addressing'] == 'no'}
    ids = [i['id'] for i in items]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        errs.append(f'duplicate ids: {sorted(dup)}')
    traced = {}
    for i in items:
        for fid in i['finding_ids']:
            traced.setdefault(fid, []).append(i['id'])
    for fid in sorted(in_scope):
        n = len(traced.get(fid, []))
        if n != 1:
            errs.append(f'in-scope finding {fid} traced {n} times: {traced.get(fid, [])}')
    for fid in sorted(traced):
        if fid in out_scope:
            errs.append(f'out-of-scope finding {fid} traced by {traced[fid]}')
        elif fid not in in_scope:
            errs.append(f'unknown finding {fid} traced by {traced[fid]}')
    idset = set(ids)
    for i in items:
        for d in i['depends_on']:
            if d not in idset:
                errs.append(f"{i['id']} depends on unknown {d}")
    deps = {i['id']: [d for d in i['depends_on'] if d in idset] for i in items}
    state = {}

    def visit(n, stack):
        state[n] = 1
        for d in deps[n]:
            if state.get(d) == 1:
                errs.append('cycle: ' + ' -> '.join(stack + [n, d]))
            elif d not in state:
                visit(d, stack + [n])
        state[n] = 2
    sys.setrecursionlimit(10000)
    for n in deps:
        if n not in state:
            visit(n, [])
    return errs, len(in_scope)


def report(items):
    from collections import Counter, OrderedDict
    ms = Counter(i['milestone'] for i in items)
    by = OrderedDict()
    for i in items:
        by.setdefault((i['milestone'], i['repo']), 0)
        by[(i['milestone'], i['repo'])] += 1
    print(f'total items: {len(items)}; per milestone: ' + ', '.join(f'{k}={ms[k]}' for k in sorted(ms)))
    for (m, r), n in by.items():
        print(f'  {m}\t{r}\t{n}')


def main():
    if '--check' in sys.argv:
        items = json.load(open(os.path.join(PD, 'items.json'), encoding='utf-8'))['items']
    else:
        per_repo = load_drafts()
        n = apply_patches(per_repo)
        items = order(per_repo)
        write(items)
        print(f'applied {n} patches')
    report(items)
    errs, nscope = validate(items)
    if errs:
        print('VALIDATION FAILED')
        for e in errs:
            print('  ' + e)
        sys.exit(1)
    print(f'VALIDATION OK: {nscope} in-scope findings each traced exactly once; no out-of-scope finding traced; '
          'all depends_on resolve; no cycles; ids unique')


if __name__ == '__main__':
    main()
