"""Fold plan-data/plan-review.json (M0) into items.json / items.tsv before any item runs."""
import json, os
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = json.load(open(f'{H}/plan-data/plan-review.json'))['synth']
items = json.load(open(f'{H}/plan-data/items.json'))['items']
byid = {i['id']: i for i in items}
for r in R['resolutions']:
    t = r['text'] if r['text'].startswith('PLAN-REVIEW RESOLUTION') else 'PLAN-REVIEW RESOLUTION: ' + r['text']
    byid[r['item']]['spec'] += '\n\n' + t
for n in R['new_items']:
    it = dict(id=n['id'], milestone=n['milestone'], repo=n['repo'], title=n['title'], depends_on=n['depends_on'],
              effort='M', smoke='', issue_refs='M0 plan review (plan-data/plan-review.json)', spec=n['spec'], verify=[])
    items.insert(items.index(byid[n['after']]) + 1, it); byid[it['id']] = it
for c in R['dependency_changes']:
    byid[c['item']]['depends_on'] = c['depends_on']
json.dump({'items': items}, open(f'{H}/plan-data/items.json', 'w'), indent=1, ensure_ascii=False)
with open(f'{H}/items.tsv', 'w') as f:
    f.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n')
    for i in items:
        f.write('\t'.join([i['id'], i['milestone'], i['repo'], i['title'], ','.join(i['depends_on']), i['effort'], i['smoke'], i['issue_refs']]) + '\n')
print(len(items), 'items')
