"""Write plan-data/accepted.json: the owner's decisions from preview.html applied to the defaults.

    1. Export the decisions:  ArtifactData list, url https://claude.ai/artifact/3iN2yVj3u9rrV9ndLB5PU8,
       collection "decisions", query.limit 1000, out_dir plan-data/decisions-export
       (one JSON file per decided change, plan-data/decisions-export/decisions/<key>.json, body {d, at}).
    2. python3 plan-data/tools/make_accepted.py

A change lands when the owner accepted it, or when it is proposed, not superseded, at or above the page's
threshold and not rejected. The same rule as the page (preview_template.html outcome()).
"""
import glob, json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXPORT = f'{B}/plan-data/decisions-export'

dec = {}
for f in glob.glob(f'{EXPORT}/**/*.json', recursive=True):
    body = json.load(open(f))
    body = body.get('data', body)
    if body.get('d') in ('accept', 'reject'):
        dec[os.path.splitext(os.path.basename(f))[0]] = body['d']

html = open(f'{B}/preview.html').read()
start = html.index('const D = ') + len('const D = ')
data, _ = json.JSONDecoder().raw_decode(html[start:])
T = data['threshold']

def lands(c):
    v = dec.get(c['key'])
    if v:
        return v == 'accept'
    return c['status'] == 'proposed' and not c['superseded'] and c['conf'] >= T

out = {'source': 'preview.html decisions + defaults', 'threshold': T, 'decided': len(dec), 'addons': {}, 'calls': {}}
for a in data['addons']:
    out['addons'][a['addon']] = {
        'layout': [c['id'] for c in a['layout'] if lands(c)],
        'strata': [c['id'] for c in a['strata'] if lands(c)],
        'rejected': [c['id'] for c in a['layout'] + a['strata'] if dec.get(c['key']) == 'reject'],
    }
for c in data['calls']:
    v = dec.get(c['key'])
    out['calls'][c['key']] = {'title': c['title'], 'decision': 'opposite of recommendation' if v == 'reject' else 'recommendation',
                              'explicit': bool(v), 'recommendation': c['rec']}
json.dump(out, open(f'{B}/plan-data/accepted.json', 'w'), indent=1, ensure_ascii=False)
n = sum(len(v['layout']) + len(v['strata']) for v in out['addons'].values())
print(f'accepted.json: {len(dec)} explicit decisions, {n} changes land')
