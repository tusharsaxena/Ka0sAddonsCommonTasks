"""Merge reconcile results and the plan-review critique into plan-data/items.json. Idempotent: rebuilds from raw_plan.json."""
import json, re, sys, subprocess, collections

D = sys.argv[1]
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
subprocess.run(['python3', f'{SP}/build_items.py', D], check=True, stdout=subprocess.DEVNULL)
P = json.load(open(f'{D}/plan-data/items.json'))
W = json.load(open(f'{D}/plan-data/docs_workflow_output.json'))['result']
items = P['items']
I = {i['id']: i for i in items}
AB = {'AbsorbTracker': 'AT', 'AuraMaster': 'AM', 'BankLedger': 'BL', 'ConsumableMaster': 'CM', 'KickCD': 'KC', 'LootHistory': 'LH',
      'MultiMeters': 'MM', 'PanelMaster': 'PM', 'PartyFrameEnhanced': 'PF', 'PrettyChat': 'PC', 'WhatGroup': 'WG'}
log = []


def dep(iid, *ds):
    for d in ds:
        if d not in I[iid]['depends_on']:
            I[iid]['depends_on'].append(d)


def note(iid, text, field='change'):
    I[iid][field] = I[iid][field].rstrip() + f'\n\nPLAN-REVIEW CORRECTION: {text}'


MINIMAP_TESTS_ONLY = ('Minimap rename carry-over (WS-06): the stored LibDBIcon key db.global.minimap.hide does NOT move, so every '
                      'existing player keeps their setting with no SavedVariables migration and no schema-version bump (a stored '
                      '`shown` key would violate anti-pattern #81). Pin it with a test written first: a legacy store with '
                      'minimap = { hide = true, minimapPos = 200 } reads `<slash> get <path>.minimap.shown` as false, the button '
                      'stays hidden, minimapPos is untouched, and no `shown` key is ever written to the raw SV after a set. Record '
                      'the player-facing CLI rename (`...minimap.hide` -> `...minimap.shown`, old path answers unknown setting) in '
                      'the commit body for the next Version History roll.')

# ---- A/B: reconcile results
for r in W['reconcile']:
    for m in r['mapped']:
        iid = m['item_id']
        if iid in ('LH-13', 'WG-11', 'PF-13'):
            I[iid]['change'] = I[iid]['change'].rstrip() + '\n\n' + MINIMAP_TESTS_ONLY
        elif m['amend_change'].strip():
            I[iid]['change'] = I[iid]['change'].rstrip() + '\n\n' + m['amend_change'].strip()
        if m['add_depends_on']:
            dep(iid, *[x.strip() for x in m['add_depends_on'].split(',') if x.strip()])
    for n in r['new_items']:
        if n['id'] in ('PF-26', 'PC-27'):
            log.append(f'dropped {n["id"]} (minimap migration not needed: stored key unchanged)')
            continue
        items.append(dict(n, milestone='M3')); I[n['id']] = items[-1]
# the WhatGroup minimap amend's migration half and the PF-13 "owner requires" text were never merged (replaced above)
# every other addon's minimap rename item gets the same test-only carry-over, for consistency
for iid in ['MM-16', 'BL-12', 'AT-12', 'PM-11', 'KC-17', 'AM-14', 'CM-19', 'PC-13']:
    if iid in I and 'minimap' in (I[iid]['title'] + I[iid]['change']).lower() and MINIMAP_TESTS_ONLY not in I[iid]['change']:
        I[iid]['change'] = I[iid]['change'].rstrip() + '\n\n' + MINIMAP_TESTS_ONLY
        dep(iid, 'WS-06')

# ---- C1: items that must land BEFORE their addon's re-vendor
pre = collections.defaultdict(list)
for i in items:
    if i['milestone'] != 'M3':
        continue
    rv = f'RV-{AB[i["repo"]]}'
    if re.search(r'(runs|lands|land|must land|landing)\s+(immediately\s+)?before\s+' + rv, i['change'], re.I) or \
       re.search(rv + r'\s+depends on (it|this)', i['change'], re.I):
        pre[rv].append(i['id'])
for rv, ids in pre.items():
    for iid in ids:
        i = I[iid]
        i['depends_on'] = [d for d in i['depends_on'] if d != rv]
        dep(iid, 'LK-33')
        i['milestone'] = 'M2'
        dep(rv, iid)
        note(iid, f'this item lands BEFORE {rv} (it is in M2, ahead of the re-vendor commit) so the re-vendor lands green; it must '
                  f'pass on both the v1.55.0 payload and the v1.56.0 dry-run.')
    log.append(f'{rv} now waits on pre-fixes {ids}')
# a pre-fix may itself depend on another M3 item of the same repo -> pull those forward too
changed = True
while changed:
    changed = False
    for i in items:
        if i['milestone'] == 'M2' and not i['id'].startswith('RV-'):
            for d in i['depends_on']:
                if d in I and I[d]['milestone'] == 'M3':
                    rv = f'RV-{AB[I[d]["repo"]]}'
                    I[d]['depends_on'] = [x for x in I[d]['depends_on'] if x != rv]
                    dep(d, 'LK-33'); I[d]['milestone'] = 'M2'; dep(rv, d); changed = True
                    log.append(f'pulled {d} ahead of {rv} (a pre-fix depends on it)')

# ---- C2/C3: tag contents and the re-vendor bundle
dep('LK-33', 'LK-03')
dep('WG-02', 'LK-03')
for ab in AB.values():
    rv = f'RV-{ab}'
    dep(rv, 'WA-01')
    I[rv]['change'] += ('\n\nThe same commit writes the re-vendor bundle docs/revendor/2026-09-23-v1.56.0/ by hand, following the '
                        'procedure in the LOCAL ../wow-addon/commands/revendor-libka0s.md as amended by WA-01 (the installed '
                        'plugin comes from GitHub and does not have WA-01 until the owner merges wow-addon): 01_DELTA.md whose '
                        'line 1 is exactly "Delta: LibKa0s v1.55.0 -> v1.56.0", per-file LibStub minors, both payload diffs, the '
                        'kit-revision pairing (25 -> 26), which majors this addon consumes, and contract changes; plus '
                        '05_SUMMARY.md. Adoption decisions are NOT taken here: they are this addon\'s M3 items.')
    I[rv]['verify'] += ('; test -f docs/revendor/2026-09-23-v1.56.0/01_DELTA.md && head -1 docs/revendor/2026-09-23-v1.56.0/01_DELTA.md '
                        '| grep -q "v1.55.0 -> v1.56.0"')

# ---- C4: /wow-addon:revendor-standards items are gated on the owner merging WowAddonStandards -> M4
GATE = ('EXECUTION GATE (owner): /wow-addon:revendor-standards fetches the standard from GitHub, so this item runs only after the '
        'WowAddonStandards remediation branch (WS-01..WS-08, v2.65.0) is merged to its default branch and pushed. Before running, '
        'confirm `gh api repos/tusharsaxena/WowAddonStandards/contents/standards/STANDARDS.md --jq .content | base64 -d | grep -m1 v2.65.0` '
        'hits; if it does not, stop and leave the item open. Never hand-edit the three-place reference from the local sibling.')
gated = [i['id'] for i in items if i['milestone'] == 'M3' and 'revendor-standards' in (i['title'] + ' ' + i['change'][:600]).lower()]
for iid in gated:
    I[iid]['milestone'] = 'M4'; dep(iid, 'WS-08')
    if 'EXECUTION GATE' not in I[iid]['change']:
        note(iid, GATE)
# the per-addon docs/record item must not wait on the owner merge: cut that edge, and make the gated item carry its own ripple
for iid in gated:
    ab = iid.split('-')[0]
    docs = f'{ab}-DOCS'
    if docs in I and iid in I[docs]['depends_on']:
        I[docs]['depends_on'] = [d for d in I[docs]['depends_on'] if d != iid]
        dep(iid, docs)
        note(iid, f'runs AFTER {docs} (which no longer waits on this gate). The same commit re-runs the docs ripple the rename '
                  f'touches (README badge, CLAUDE.md, TOC X-Standard) and nothing else; the automated-test bundle from {docs} stands.')
        log.append(f'{docs} decoupled from gated {iid}')
# anything depending on a gated item is gated too
changed = True
while changed:
    changed = False
    for i in items:
        if i['milestone'] == 'M3' and any(I.get(d, {}).get('milestone') == 'M4' for d in i['depends_on']):
            i['milestone'] = 'M4'; changed = True; log.append(f'{i["id"]} moved to M4 (depends on a gated item)')
log.append(f'gated to M4: {gated}')

# ---- C5-C6: dependency tightening
dep('MM-16', 'MM-12'); dep('LK-19', 'WS-07')
for iid, d in [('BL-06', 'LK-11'), ('LH-17', 'LK-11'), ('BL-11', 'WS-03'), ('MM-12', 'WS-03'), ('LH-12', 'WS-03'), ('WG-08', 'WS-03'),
               ('BL-12', 'WS-06'), ('KC-17', 'WS-06'), ('LH-26', 'WS-05'), ('PC-15', 'WS-05')]:
    if iid in I: dep(iid, d)

# ---- C7-C8: re-vendor span bases and bundle grammar
note('WA-01', 'every addon had a kit-only re-vendor of v1.54.2 (AuraMaster 329e1a3, ConsumableMaster 1f86d4e, BankLedger 6b12edf, '
              'PrettyChat 8421342, WhatGroup 7f38ddd), so the frozen v1.55.0 bundles correctly read "v1.54.2 -> v1.55.0". Cross-check '
              'the base with `git log -1 -- libs/LibKa0s tests/_kit`, drop the claim that AuraMaster\'s base is misstated, and expect '
              'v1.54.2 (329e1a3) in the dry-run.')
note('WS-01', 'the vendored-side loop walks `git log -- libs/LibKa0s tests/_kit` (both paths), so kit-only re-vendors count.')
note('CM-28', 'delete the "misstated base" note; the v1.54.2 kit-only re-vendor makes the frozen bundle correct.')
SPAN = ('normalize the span bundle to WS-01\'s exact grammar: line 1 is `Delta: LibKa0s v<A> -> v<B> (span: v<A> ... v<B>)` with A = '
        'the first unrecorded tag and B = the last (derive the tag list from `git log -- libs/LibKa0s tests/_kit`, so kit-only '
        're-vendors such as v1.54.2 are in the span), the folder named docs/revendor/<date>-v<A>-v<B>/, and the true previous '
        'base stated in the body, never on line 1.')
for iid in ['BL-23', 'CM-28', 'PC-25', 'WG-29', 'LH-34', 'PM-18', 'AM-02', 'MM-30', 'KC-24', 'PF-24']:
    if iid in I: note(iid, SPAN); dep(iid, 'WA-01')

# ---- C9: LK-28 must fit AuraMaster's disabled rendering (AM-17)
note('LK-28', 'disabledFor answering true draws the disabledNotice ABOVE the rows and renders the rows disabled (RenderRows '
              'opts.disabled plus ctx.__renderDisabled around bespoke render); it does not replace them. A `tabs` entry whose key '
              'equals a schema group takes that group\'s place in the strip and is handed the group\'s rows (render(ctx, rows)). '
              'Library tests pin both, so AM-17 adopts without changing its disabled-state characterization.')
dep('AM-17', 'LK-28')

# ---- C10: MultiMeters corrections
note('MM-14', 'LibKa0s-Schema-1.0 instance members are dot-defined (LibKa0s/Schema.lua: `function S.Get(path, instanceId)` ...). '
              'Write the shims in dot form: NS.FindSchemaRow = S.FindRow; NS.RegisterSchemaRows = function(rows) S.AddRows(rows) end; '
              'NS.GetSetting = function(p, id) return S.Get(p, id) end; NS.SetByPath = S.Set; NS.ApplyDefault = function(row, id) '
              'return S.ApplyDefault(row, id) end; and S.SetMany(entries, { instanceId = windowId, act = ..., scope = ... }). '
              '`NS.X = S:FindRow` is not valid Lua.')
note('MM-16', 'correct cites: CURRENT_DB_VERSION is core/Database.lua:53, and the step that moves minimap to the global store is '
              'migrations[14] (:895-935; the runner indexes by from-version). Test (f) seeds schemaVersion 14.')
LINECAP = "git ls-files '*.lua' | grep -v -e '^libs/' -e '^tests/_kit/' | xargs wc -l | awk '$2!=\"total\" && $1>1500' (no output)"
for i in items:
    if i['repo'] == 'MultiMeters' and 'line-cap awk' in i['verify']:
        i['verify'] = i['verify'].replace('line-cap awk', LINECAP)
note('MM-20', 'the peel target is a new modules/Row_Cells.lua holding RowProto:Release (Row.lua:1446-1455) and the cell-clear loop, '
              'added to MultiMeters.toc right after modules\\Row.lua with a LOAD-BEARING comment; and the `local live = {}` at '
              'Row.lua:1311 is replaced by the reused self.liveCells (no per-call allocation).')

# ---- C11: consistency-check fixes (second review pass)
c = I['MM-16']['change']
cut = c.find('If the implementer finds any path string persisted')
if cut >= 0:
    end = c.find('gets its own test.', cut)
    I['MM-16']['change'] = c[:cut] + ('If the implementer finds any path string persisted in SavedVariables (a saved reset-exempt list, a '
                                     'bookmark or similar), STOP and raise it with the owner: this plan adds no SavedVariables migration '
                                     'for the rename.') + c[end + len('gets its own test.'):]
I['WG-02']['change'] = I['WG-02']['change'].replace(
    "If RV-WG's own commit cannot be green without this re-pin, fold this item into the RV-WG commit.",
    "Any red at RV-WG is listed in that commit's body and this item clears it; it is never folded into the copy-only RV-WG commit.")
note('MM-32', GATE + ' This supersedes the "run against ../WowAddonStandards" wording above.')
for iid in ('LH-36', 'WG-30'):
    I[iid]['change'] = re.sub(r'\bmerged to (its )?main\b', 'merged to its default branch (master)', I[iid]['change'])
    I[iid]['change'] = I[iid]['change'].replace('(WowAddonStandards main)', '(WowAddonStandards master)')
for iid in ('WS-02', 'LK-23'):
    I[iid]['change'] = I[iid]['change'].replace('AbsorbTracker AT-62/Info-6', "AbsorbTracker's review item 62 / Info-6 (not plan item AT-62)")
for ab in AB.values():
    I[f'RV-{ab}']['change'] = I[f'RV-{ab}']['change'].replace(
        'record the failures in the commit body; the fixes are this addon\'s M3 items.',
        'record the failures in the commit body; this addon\'s M3 items clear them, and the addon is green again at the latest by '
        f'{ab}-DOCS. docs/test-cases.md and the README test badge are regenerated by a later item, never by this commit.')

# ---- sanity: ids, deps, cycles
ids = [i['id'] for i in items]
assert len(ids) == len(set(ids)), 'duplicate ids'
bad = [(i['id'], d) for i in items for d in i['depends_on'] if d not in I]
assert not bad, bad
order = {'M1': 1, 'M2': 2, 'M3': 3, 'M4': 4}
back = [(i['id'], i['milestone'], d, I[d]['milestone']) for i in items for d in i['depends_on'] if order[I[d]['milestone']] > order[i['milestone']]]
assert not back, back
state = {}
def visit(n, stack=()):
    if state.get(n) == 2: return
    if state.get(n) == 1: raise SystemExit(f'cycle: {stack + (n,)}')
    state[n] = 1
    for d in I[n]['depends_on']: visit(d, stack + (n,))
    state[n] = 2
for n in I: visit(n)
# every M1 item reachable from LK-33 or from each RV?
anc = set()
def up(n):
    for d in I[n]['depends_on']:
        if d not in anc: anc.add(d); up(d)
up('RV-AT')
unreached = [i['id'] for i in items if i['milestone'] == 'M1' and i['id'] not in anc]
log.append(f'M1 items not ancestors of RV-AT: {unreached}')
P['items'] = sorted(items, key=lambda i: (order[i['milestone']], ids.index(i['id'])))
P['amendment_log'] = log
json.dump(P, open(f'{D}/plan-data/items.json', 'w'), indent=1)
print('\n'.join(log))
print(collections.Counter(i['milestone'] for i in items), len(items))
