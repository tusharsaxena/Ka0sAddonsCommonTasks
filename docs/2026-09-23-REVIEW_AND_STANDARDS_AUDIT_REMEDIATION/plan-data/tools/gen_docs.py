"""Generate the mechanical parts of the 2026-09-23 bundle from plan-data/items.json and inputs/findings."""
import json, glob, collections, sys

D = sys.argv[1]
P = json.load(open(f"{D}/plan-data/items.json"))
RAW = json.load(open(f"{D}/plan-data/raw_plan.json"))
items = P['items']
clusters = RAW['clusters']['clusters']
F = {}
suite = {}
for p in sorted(glob.glob(f"{D}/inputs/findings/[A-Z]*.json")):
    j = json.load(open(p))
    suite[j['repo']] = j['suite_state']
    for f in j['findings']:
        F[f['id']] = dict(f, repo=j['repo'])
rejected = json.load(open(f"{D}/inputs/findings/_rejected.json"))
SEV = ['critical', 'high', 'medium', 'low', 'info']
REPOS = ['LibKa0s', 'AbsorbTracker', 'AuraMaster', 'BankLedger', 'ConsumableMaster', 'KickCD', 'LootHistory',
         'MultiMeters', 'PanelMaster', 'PartyFrameEnhanced', 'PrettyChat', 'WhatGroup']
MS = {'M1': 'Upstream — WowAddonStandards, LibKa0s (tag v1.56.0 locally), wow-addon plugin',
      'M2': 'Re-vendor the whole LibKa0s v1.56.0 payload into all eleven addons',
      'M3': 'Addon remediation — every finding, consumer follow-up and owner issue, per addon',
      'M4': 'Record and close-out'}


def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()


# finding -> covering items / dispositions
cover = collections.defaultdict(list)
for i in items:
    for fid in i['finding_ids']:
        cover[fid].append(i['id'])
disp = {}
for repo, ds in P['dispositions'].items():
    for d in ds:
        disp[d['finding_id']] = d
fcluster = {fid: c['id'] for c in clusters for fid in c['finding_ids']}

# ---------- items.tsv
with open(f"{D}/items.tsv", 'w') as fh:
    fh.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tfinding_ids\tissue_refs\n')
    for i in items:
        fh.write('\t'.join([i['id'], i['milestone'], i['repo'], cell(i['title']), ','.join(i['depends_on']), i['effort'],
                            'yes' if i['smoke'].strip() else '', ','.join(i['finding_ids']), ','.join(i['issue_refs'])]) + '\n')

# ---------- 01_CONSOLIDATED_FINDINGS.md
L = ['# 01 — Consolidated Findings', '',
     f'**{len(F)} verified findings** from the 2026-09-23 `/wow-addon:review` and `/wow-addon:standards-audit` runs over '
     'LibKa0s and the eleven addons, after adversarial re-verification against the code. '
     f'{len(rejected)} were rejected and are listed at the end.', '',
     'Severity and remediation are the **post-verification** values; `verdict` says whether the verifier confirmed the '
     'finding as written or corrected it. Source bundles: `<Repo>/docs/reviews/2026-09-23/` and '
     '`<Repo>/docs/audits/2026-09-23/`. Machine-readable copy: `inputs/findings/<Repo>.json`.', '',
     '## Totals', '', '| Repo | ' + ' | '.join(SEV) + ' | total | upstream-routed |', '|---|' + '---|' * (len(SEV) + 2)]
for r in REPOS:
    fs = [f for f in F.values() if f['repo'] == r]
    c = collections.Counter(f['severity'] for f in fs)
    L.append(f'| {r} | ' + ' | '.join(str(c[s]) for s in SEV) + f' | {len(fs)} | {sum(1 for f in fs if f["upstream"] and r != "LibKa0s")} |')
c = collections.Counter(f['severity'] for f in F.values())
L.append('| **all** | ' + ' | '.join(f'**{c[s]}**' for s in SEV) + f' | **{len(F)}** | **{sum(1 for f in F.values() if f["upstream"] and f["repo"] != "LibKa0s")}** |')
L += ['', '## Suite state as measured on 2026-09-23', '']
for r in REPOS:
    L.append(f'- **{r}** — {cell(suite.get(r, ""))[:900]}')
L += ['', '## Clusters', '', '| Cluster | Title | Findings | Repos |', '|---|---|---|---|']
for cl in clusters:
    repos = sorted({F[x]['repo'] for x in cl['finding_ids'] if x in F})
    L.append(f'| {cl["id"]} | {cell(cl["title"])} | {len(cl["finding_ids"])} | {", ".join(repos)} |')
for cl in clusters:
    L += ['', f'### {cl["id"]} — {cl["title"]}', '', cell(cl['summary']), '']
    for r in REPOS:
        fs = sorted([F[x] for x in cl['finding_ids'] if x in F and F[x]['repo'] == r], key=lambda f: SEV.index(f['severity']))
        if not fs:
            continue
        L.append(f'**{r}**')
        L.append('')
        for f in fs:
            up = f' · upstream → {f["upstream_repo"]}' if f['upstream'] and r != 'LibKa0s' else ''
            L.append(f'- **{f["id"]}** `{f["severity"]}` ({f["source"]} {f["source_id"]}; {f["verdict"]}{up}) — {cell(f["title"])}  ')
            L.append(f'  *Where:* {cell(f["locations"])}  ')
            L.append(f'  *Evidence:* {cell(f["evidence"])}  ')
            L.append(f'  *Remediation:* {cell(f["remediation"])}  ')
            if f['rule_ref']:
                L.append(f'  *Rule:* {cell(f["rule_ref"])}  ')
            L.append(f'  *Planned in:* {", ".join(cover.get(f["id"], [])) or ("disposition → " + disp[f["id"]]["covered_by"] if f["id"] in disp else "**UNMAPPED**")}')
        L.append('')
L += ['## Rejected by verification', '']
for f in rejected:
    L.append(f'- **{f["id"]}** ({f["repo"]}) — {cell(f["title"])}. *Why rejected:* {cell(f["verify_reason"])}')
open(f"{D}/01_CONSOLIDATED_FINDINGS.md", 'w').write('\n'.join(L) + '\n')

# ---------- 05_TRACEABILITY.md
unm = [fid for fid in F if not cover.get(fid) and fid not in disp]
L = ['# 05 — Traceability', '',
     'Every verified finding → cluster → work item(s) → milestone. Generated from `plan-data/items.json`; regenerate, '
     'do not hand-edit.', '',
     f'**Coverage: {len(F) - len(unm)}/{len(F)} findings mapped.** '
     + ('Unmapped: ' + ', '.join(unm) if unm else 'No finding is unmapped.'), '',
     '## Owner-scope issues', '', '| Issue | Item(s) |', '|---|---|']
iss = collections.defaultdict(list)
for i in items:
    for r in i['issue_refs']:
        iss[r].append(i['id'])
for k in sorted(iss):
    L.append(f'| {k} | {", ".join(iss[k])} |')
L += ['', '## Findings', '', '| Finding | Sev | Cluster | Item(s) | Milestone |', '|---|---|---|---|---|']
ms = {i['id']: i['milestone'] for i in items}
for r in REPOS:
    for fid, f in F.items():
        if f['repo'] != r:
            continue
        its = cover.get(fid, [])
        if its:
            L.append(f'| {fid} | {f["severity"]} | {fcluster.get(fid, "")} | {", ".join(its)} | {", ".join(sorted({ms[x] for x in its}))} |')
        elif fid in disp:
            d = disp[fid]
            L.append(f'| {fid} | {f["severity"]} | {fcluster.get(fid, "")} | → {d["covered_by"]} ({cell(d["reason"])[:120]}) | {ms.get(d["covered_by"], "")} |')
        else:
            L.append(f'| {fid} | {f["severity"]} | {fcluster.get(fid, "")} | **UNMAPPED** | |')
open(f"{D}/05_TRACEABILITY.md", 'w').write('\n'.join(L) + '\n')

# ---------- 04 tables (appended to the hand-written head)
L = []
for m in ['M1', 'M2', 'M3']:
    L += ['', f'## {m} — {MS[m]}', '']
    repos = [r for r in dict.fromkeys(i['repo'] for i in items if i['milestone'] == m)]
    for r in repos:
        its = [i for i in items if i['milestone'] == m and i['repo'] == r]
        L += [f'### {r} ({len(its)} items)', '']
        for i in its:
            flag = ' ⚠' if i['smoke'].strip() else ''
            L.append(f'#### {i["id"]} — {cell(i["title"])}{flag}')
            L.append('')
            L.append(f'- **Effort** {i["effort"]} · **Depends on** {", ".join(i["depends_on"]) or "—"}'
                     + (f' · **Issues** {", ".join(i["issue_refs"])}' if i['issue_refs'] else ''))
            L.append(f'- **Findings** {", ".join(i["finding_ids"]) or "—"}')
            L.append(f'- **Change** {cell(i["change"])}')
            L.append(f'- **Test first** {cell(i["tests"])}')
            L.append(f'- **Verify** {cell(i["verify"])}')
            if i['smoke'].strip():
                L.append(f'- **Smoke** {cell(i["smoke"])}')
            L.append('')
open(f"{D}/plan-data/04_tables.md", 'w').write('\n'.join(L) + '\n')
print('items', len(items), 'findings', len(F), 'unmapped', len(unm),
      collections.Counter(i['milestone'] for i in items))
