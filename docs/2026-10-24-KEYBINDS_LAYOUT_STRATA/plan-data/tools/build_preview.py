"""Build preview.html (the owner's 020/030 review page) from plan-data/preview.json.

    python3 plan-data/tools/build_preview.py

The page embeds the data and stores the owner's per-change decisions in the artifact's db collection
"decisions" (doc id = the change key below). plan-data/tools/fetch_decisions.md says how they are read back.
"""
import html, json, os, re

B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(f'{B}/plan-data/preview.json'))

THRESHOLD = 50  # a proposed change at or above this lands unless the owner rejects it

def norm(cid):
    return cid.split(':')[-1].strip()

ov = {'layout': {}, 'strata': {}}
adds = {'layout': [], 'strata': []}
for kind in ('layout', 'strata'):
    for o in d[kind]['overrides']:
        if o['action'] == 'add':
            adds[kind].append(o)
        else:
            ov[kind].setdefault(norm(o['changeId']), []).append(o)

PFX = {}
addons = []
for e in d['extracts']:
    a = e['addon']
    pfx = (e['layout'] or e['strata'])[0]['id'].split('-')[0]
    PFX[pfx] = a
    def conv(c, kind):
        o = ov[kind].get(c['id'], [])
        sup = any(x['action'] == 'supersede' for x in o)
        return dict(key=f"{a}__{c['id']}", id=c['id'], area=c['area'], change=c['change'], reason=c['reason'],
                    conf=c['confidence'], status=c['status'], superseded=sup,
                    notes=[f"{x['action']}: {x['note']}" for x in o])
    addons.append(dict(addon=a, headline=e['headline'], strataHeadline=e['strataHeadline'],
                       before=e['before'], after=e['after'], currentTree=e['currentTree'],
                       proposedTree=e['proposedTree'], strataMap=e['strataMap'],
                       layout=[conv(c, 'layout') for c in e['layout']],
                       strata=[conv(c, 'strata') for c in e['strata']]))

def owner_of(cid):
    m = re.match(r'^(?:([A-Za-z]+):)?([A-Z]{3})-', cid)
    if not m:
        return None
    if m.group(1) and m.group(1) in [x['addon'] for x in addons]:
        return m.group(1)
    return PFX.get(m.group(2))

by = {x['addon']: x for x in addons}
for kind in ('layout', 'strata'):
    for o in adds[kind]:
        a = owner_of(o['changeId'])
        tgt = by[a][kind] if a else None
        if tgt is None:
            continue
        cid = norm(o['changeId'])
        conf = re.search(r'(\d{2})%', o['note'])
        tgt.append(dict(key=f"{a}__{cid}", id=cid, area='Collection convention', change=o['note'],
                        reason='Required by a collection-wide convention (cross-addon pass).',
                        conf=int(conf.group(1)) if conf else 60, status='proposed', superseded=False,
                        notes=['added by the cross-addon pass']))

CALLS = [
    dict(key='CALL-01', title='QuickComms gets its in-panel key editor back',
         text='QuickComms removed its Binding tab on 2026-10-21 (b902e35) so the key was set only in Options > Keybindings. '
              '015 adds a General > Keybindings tab to all seven windowed addons, QuickComms included, which reverses that call.',
         rec='Proceed: QuickComms gets the same shared Keybindings tab as the other six. The 2026-10-21 decision is recorded as superseded.'),
    dict(key='CALL-02', title='Rename "Master alpha" to "Master opacity" everywhere',
         text='Every host row already says "opacity". The canonical Master controls row still says "alpha". Renaming it is a label change in the '
              'standard (options-ui-§15) and in LibKa0s\'s composer, so all 15 addons change at once. Setting keys stay the same.',
         rec='Rename it (cross-addon convention XC-10, 75%).'),
    dict(key='CALL-03', title='Binding labels in Settings > Keybindings',
         text='Inside a category that already carries the addon name, labels drop the brand and the article. BankLedger: "Toggle ledger window". '
              'DpsRace: "Toggle race HUD", "Toggle results window", "Arm or cancel race". DropWatcher: "Toggle drop feed". '
              'LootHistory: "Toggle history browser". MultiMeters, QuickComms and WhatGroup keep theirs. Binding names (and so saved keys) do not change.',
         rec='Use these labels (60-90%).'),
    dict(key='CALL-04', title='MultiMeters keeps "Dialog" in its strata choices',
         text='The model keeps player-chosen strata below the addon\'s own popups. MultiMeters lets a meter sit at DIALOG. Removing that value would '
              'change a setting, which 020 and 030 may not do, so the plan only adds a tooltip warning.',
         rec='Keep the value and add the warning. Removing it would be a separate settings change.'),
    dict(key='CALL-05', title='Defer the swatch disabledIf idea',
         text='Greying out a colour swatch while its feature is off (QuickComms and others) adds behaviour, which the 020 brief rules out.',
         rec='File it as an issue for a later run instead of doing it here.'),
    dict(key='CALL-06', title='KickCD: charge counts draw above the proc glow',
         text='Today the glow sits at button+4, above the charge text. The strata ladder puts text above effects, so the charges stay readable '
              'while the glow plays. You will see the glow under the numbers instead of over them.',
         rec='Text above glow, with a smoke check for you to look at.'),
]

XC = d['layout']['conventions']
XS = d['strata']['conventions']
UP = [dict(u, kind='Layout') for u in d['layout']['upstream']] + [dict(u, kind='Strata') for u in d['strata']['upstream']]

DATA = dict(addons=addons, calls=CALLS, xc=XC, xs=XS, up=UP, threshold=THRESHOLD,
            libLayout=d['layout']['libka0s'], libStrata=d['strata']['libka0s'])

tpl = open(f'{B}/plan-data/tools/preview_template.html').read()
blob = json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')
out = tpl.replace('/*__DATA__*/null', blob)
open(f'{B}/preview.html', 'w').write(out)
n = sum(len(a['layout']) + len(a['strata']) for a in addons)
print(f'preview.html: {len(addons)} addons, {n} changes, {len(CALLS)} calls, {len(out)//1024} KB')
