"""Assemble plan-data/items.json and items.tsv from the design workflow's items, the lead-owned items and the
plan-review resolutions. Run once at planning time; the outputs are then frozen (RESUME.md: addenda only)."""
import json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(f'{B}/plan-data/design-workflow.json')); d = d.get('result', d)
if isinstance(d, str): d = json.loads(d)
items = [i for x in d['designs'] for i in x['items']]

ADDONS = [('AbsorbTracker','AT'),('AuraMaster','AM'),('BankLedger','BL'),('ConsumableMaster','CM'),('DropWatcher','DW'),
          ('KickCD','KC'),('LootHistory','LH'),('MultiMeters','MM'),('PanelMaster','PM'),('PartyFrameEnhanced','PF'),
          ('PremadeGroupsFilterExtension','PG'),('PrettyChat','PC'),('QuickComms','QC'),('WhatGroup','WG')]
def lead(id, ms, repo, title, deps, effort, spec, verify, smoke=(), refs=()):
    return dict(id=id, milestone=ms, repo=repo, title=title, depends_on=list(deps), effort=effort, spec=spec,
                verify=verify, smoke=list(smoke), issue_refs=list(refs))
L = [
 lead('WS-00','M1','WowAddonStandards','Open v2.87.0: version and date in every place the repo mirrors them; a CHANGELOG section for this run',[], 'S',
      "Follow WowAddonStandards/CLAUDE.md's version-bump ripple (STANDARDS.md title line, every mirror its CLAUDE.md lists, CHANGELOG.md new top section v2.87.0 dated 2026-10-23 with an intro line: 'Simulator auto-run, the mode strip's simulation flavor and header words, and the release re-look of preview and simulation data'). Later WS items add their CHANGELOG bullets under it and never bump the version.",
      'grep -n "v2.87.0" standards/STANDARDS.md CHANGELOG.md; the repo gates its CLAUDE.md names'),
 lead('WS-90','M1','WowAddonStandards','Close v2.87.0: regenerate the context pack and index blurbs, cross-check every citation this run added',['WS-01','WS-05','WS-25','WS-26'],'S',
      "Re-read the v2.87.0 CHANGELOG section against the diffs of WS-01, WS-05, WS-25 and WS-26. Regenerate or hand-update NEW_ADDON_CONTEXT.md / the context pack and STANDARDS.md index blurbs per the repo's CLAUDE.md so they reflect every rule added. Check every new `filename-§N` citation resolves and anti-pattern numbering is contiguous. Run the repo's gates/check scripts.",
      "the repo's own check scripts green; grep for each new citation"),
 lead('LK-00','M1','LibKa0s','Open v1.76.0: a CHANGELOG section per docs/releasing.md',[], 'S',
      "Per LibKa0s/docs/releasing.md, open the v1.76.0 release: CHANGELOG.md top section for v1.76.0 (unreleased, 2026-10-23) with an intro: 'Simulator auto-run (Run all removed), the test strip's simulation flavor, and the release re-look of preview and simulation fixtures'. Do not bump file minors here (each item bumps the files it changes once). Do not tag.",
      'head -20 CHANGELOG.md; lua tests/run.lua; luacheck .'),
 lead('LK-90','M1','LibKa0s','Close v1.76.0: version key, members manifest, docs/api, CONSUMERS.md, test-cases; LOCAL annotated tag v1.76.0',['LK-01','LK-10','LK-25'],'M',
      "Follow docs/releasing.md to the letter for v1.76.0: every version mirror, the module/version keys, tools/gen-api-members.lua output, docs/api pages for Sim and Widgets, docs/test-cases.md regenerated (lua tests/run.lua --list, CRLF as the file is), testkit revision only if testkit/ changed (it should not). CONSUMERS.md: add rows planned at v1.76.0, MultiMeters and KickCD as LibKa0s-Sim-1.0 consumers (adoption lands in this run's M3), and the Widgets TestStrip kind='sim' adopters BankLedger, DropWatcher, LootHistory, MultiMeters, KickCD. Full gates green. Then create the LOCAL annotated tag `git tag -a v1.76.0 -m 'LibKa0s v1.76.0'` on the run branch head. Never push the tag.",
      "git tag -l v1.76.0; git cat-file -t v1.76.0 == tag; full gates", refs=['MultiMeters#60','KickCD#38']),
 lead('DC-00','M1','dev-copilot','Open 2.5.0: plugin.json, marketplace entry and CHANGELOG section',[], 'S',
      "Bump .claude-plugin/plugin.json version 2.4.0 -> 2.5.0 and every mirror dev-copilot/CLAUDE.md names (marketplace.json if present, README version mentions). CHANGELOG.md new top 2.5.0 section dated 2026-10-23: 'WoW bump-version asks whether test-mode data and simulator scenarios are still current'. Run the repo's checks (scripts/check_overlays.py and anything its CLAUDE.md lists).",
      'grep -rn "2.5.0" .claude-plugin CHANGELOG.md; the repo checks'),
]
for repo, p in ADDONS:
    L.append(lead(f'{p}-RV','M2',repo,f'Re-vendor LibKa0s v1.76.0 and refresh the standard reference to v2.87.0',['LK-90','WS-90'],'S',
      "Two parts, one or two commits (both subjects start '%s-RV: '). (1) LibKa0s: follow the INSTALLED /dev-copilot:wow-revendor-libka0s skill's copy-and-prune contract from the LOCAL tag v1.76.0 (git -C ../LibKa0s archive v1.76.0 LibKa0s testkit | tar -x into a mktemp dir; never check the tag out): replace libs/LibKa0s and tests/_kit whole, prune media/icons to the CLAUDE.md 'LibKa0s icons:' line with the tag's tools/prune-icons.lua, roll the CLAUDE.md provenance line, write docs/revendor/2026-10-23-v1.76.0/ (delta report; adoption candidates: list them but DO NOT interview or adopt here, the run's own items do that; file no issues). If the addon's tests break only because of the Sim auto-run (Run all removed) or Widgets minor change, and a later item of this run in this repo owns that fallout (BL-01, DW-01, LH-01), make the minimum test adjustment here and say so, or leave it for that item only if the gate stays green. (2) Standard: follow the INSTALLED /dev-copilot:wow-revendor-standards contract for this repo to v2.87.0 (TOC X-Standard, README badge, CLAUDE.md Standards compliance). Gates green: luacheck 0/0, lua tests/run.lua, 1500-line cap." % p,
      "diff -r libs/LibKa0s <tag copy> (only pruned icons differ); grep v1.76.0 CLAUDE.md; grep v2.87.0 *.toc README.md CLAUDE.md; gates"))
L += [
 lead('CT-01','M4','Ka0sAddonsCommonTasks','Closeout record: 99_EXECUTION_RECORD.md, 06_SMOKE_TESTS.md final, checkpoints, memory',['LK-90','WS-90','DC-01'],'S',
      'Lead-run. Record per-milestone outcomes, deviations, local tag sha, pushed heads. No merge.', './resume-state.sh'),
 lead('CT-02','M4','Ka0sAddonsCommonTasks','Finalize on the owner go-ahead: merge --no-ff in dependency order, push, push tag v1.76.0, delete branches/stashes/worktrees; confirm MultiMeters#60 and KickCD#38 closed',['CT-01'],'M',
      'Lead-run, ONLY on explicit owner go-ahead. Order: WowAddonStandards, LibKa0s (+ git push origin v1.76.0), dev-copilot, the 14 addons, Ka0sAddonsCommonTasks.', 'git branch -a | grep sim-preview-mode-strips (none)', refs=['MultiMeters#60','KickCD#38']),
]

RES = {
 'MM-17': "Strip API is exactly `W.TestStrip(parent, { kind = \"sim\", text = ..., icon = NS.Icon(\"info\") })` (LK-10); assert `strip.kind == \"sim\"` (not __fill, not a constructor spy); text via strip.text:SetText/GetText; reserve height from W.TEST_STRIP.HEIGHT. The title never contains SIMULATION; TEST MODE appears only under MM-01's rule (test mode on AND minimized or no Widgets); while a simulation runs the title has no mode word even minimized. Depends on MM-01 too. A minimized window during a simulation shows no marker: record that as a Known Limitation in README (the step panel marks the run).",
 'KC-09': "Strip API is exactly `W.TestStrip(parent, { kind = \"sim\", text = ..., icon = NS.Icon(\"info\") })` (LK-10); assert `strip.kind == \"sim\"`; text via strip.text:SetText/GetText; height W.TEST_STRIP.HEIGHT. One strip per shown icon grid (target and focus), anchored to the grid's top; KickCD has no 'party grid' (OWNER B2's 'party icon grid' means KickCD's icon grid(s)). TOC: SimStrip.lua after SimScenario.lua.",
 'MM-13': "Tests cannot use the live NS.Sim before MM-15: MM-14 (or this item, whichever comes first) adds tests/sim_support.lua `S.testSession(steps)` that builds a throwaway `LibStub('LibKa0s-Sim-1.0'):New{ seam = NS.SimSeam, deliver = NS.DeliverEvent, ... }` (LibKa0s tests/test_sim_host.lua shape) and points NS.Sim at it for the case, restoring after. World.New takes the player's role from the live spec role (read inside Live, like GUID/name/class), not a hard-coded DAMAGER; document which read Roster uses.",
 'MM-14': "Use/introduce tests/sim_support.lua S.testSession (see MM-13's resolution) for any case that needs NS.Sim:After/Fire before MM-15 lands.",
 'KC-03': "Add tests/sim_support.lua `S.testSession(steps)` building a throwaway `LibStub('LibKa0s-Sim-1.0'):New{ seam = NS.SimSeam, deliver = NS.DeliverEvent, ... }` (LibKa0s tests/test_sim_host.lua shape), pointing NS.Sim at it for a case and restoring after, so KC-04..KC-07 can test before KC-05's live host exists. The COMMANDS row description follows core/KickCD.lua's existing convention for help descriptions (check what the locale/prose tests require) rather than the spec's NS.L[...] form if they differ.",
 'KC-04': "Use tests/sim_support.lua S.testSession (KC-03) for cases that need an active session before KC-05. LEAD DECISION (binding, recorded in 03_SPEC D-KC): KickCD tracks only the player's own interrupts/CC against target and focus casts; there is no party tracking and this run adds none. The made-up party is narration: their kicks end enemy casts and print [sim] lines. Each KickCD#38 scenario maps to the engine path it stresses.",
 'KC-05': "TOC: insert modules\\Sim.lua after modules\\SimWorld.lua (LOAD-BEARING note). Prepare calls NS.Sim:ShowPanel() (guarded) before ready().",
 'KC-07': "TOC: insert modules\\SimDrivers.lua between SimWorld.lua and Sim.lua.",
 'KC-08': "TOC: SimScenario.lua after Sim.lua. Stepped e2e: start with the member `NS.Sim:Start{scenario=..., seed=...}` (nothing plays, LK-01 A2) then `NS.Sim:Step()` per step, advancing the kit clock only to drain ticks or the gate. One auto-run case: `NS.Sim:RunVerb('start <name>')` then advance by the step delay per step until FINISHED.",
 'KC-10': "README Known Limitations: the simulator narrates the party (no party tracking exists). The commit body carries 'Closes #38'.",
 'MM-15': "Host.Prepare calls NS.Sim:ShowPanel() (guarded) before ready(); assert NS.Sim:IsPanelShown() after a typed start. LEAD DECISION: no sim.stepDelay settings row (MM-18 dropped as outside OWNER_SCOPE); Host.STEP_DELAY = 1 constant as KickCD does.",
 'MM-16': "Stepped e2e: start with the member `NS.Sim:Start{scenario=..., seed=...}` (nothing plays, LK-01 A2) then `NS.Sim:Step()` per step, advancing the kit clock only for fight ticks or the gate. One auto-run case per suite: `NS.Sim:RunVerb('start <name>')`, then advance by 1 s per step until FINISHED.",
 'MM-19': "MM-18 is dropped: no step-delay setting appears in diagnostics.",
 'MM-20': "Depends no longer on MM-18 (dropped). Also update the LibKa0s majors count/table in docs/ARCHITECTURE.md and docs/module-map.md (MultiMeters adopts LibKa0s-Sim-1.0). Known Limitation: a minimized window shows no sim marker. Commit body carries 'Closes #60'.",
 'BL-10': "The strip is a Frame without SetText: write `frame.simStrip.text:SetText(NS.SimHost.MarkerText() or \"\")`. Smoke ids for this item SM-BL-10..13; name the repo-local check id and section in docs/smoke-tests.md and widen its index row.",
 'BL-01': "Bundle smoke ids for this item: SM-BL-01..04 (disjoint from BL-10's SM-BL-10..13).",
 'DW-01': "Bundle smoke ids SM-DW-01..04. For the status line case: check whether the line prints while the Encounter Journal pool is still pending; assert 'building' then, else 'playing' (LK-01 2.2's Status() rule).",
 'DW-10': "Use the literal L key for the sim banner text (define it in locales/enUS.lua; no undefined SIM_FULL constant). Cite test cases by title, not line number, since DW-01 shifts lines. Smoke ids SM-DW-10..13 with the repo-local check id and section named.",
 'LH-01': "Bundle smoke ids SM-LH-01..04.",
 'LH-10': "Smoke ids SM-LH-10..13; name the repo-local check id and section in docs/smoke-tests.md.",
 'LK-10': "Ripple also: regenerate docs/test-cases.md (lua tests/run.lua --list, keep the file's line endings).",
 'QC-02': "LEAD DECISION (critic): the window position PERSISTS in the profile, per standalone-windows' persist MUST (no exemption claimed): an AceDB profile default for the point (e.g. previewWindow = { point = 'TOP', relPoint = 'TOP', x = 0, y = -140 }), written on drag stop, read on build; a profile switch re-reads it; no schema-version migration needed for a new defaulted key unless the repo's conventions say otherwise. SM-QC-7 becomes: drag, end, start: same place; /reload and start: same place.",
 'QC-04': "Document the persisted position (no Known Limitation for it).",
}
items = [i for i in items if i['id'] != 'MM-18']
for i in items:
    if i['id'] == 'MM-20': i['depends_on'] = [x for x in i['depends_on'] if x != 'MM-18']
    if i['id'] == 'MM-17' and 'MM-01' not in i['depends_on']: i['depends_on'].append('MM-01')
    if i['id'] == 'QC-02': i['smoke'] = [s if not s.startswith('SM-QC-7') else 'SM-QC-7: drag the window, end the preview, start it again: same place; /reload and start again: still the dragged place' for s in i['smoke']]
    if i['id'] in RES: i['spec'] += '\n\nPLAN-REVIEW RESOLUTION (binding over the text above): ' + RES[i['id']]
    if i['id'].startswith(('WS-',)) and i['id'] not in ('WS-00',) and 'WS-00' not in i['depends_on']: i['depends_on'].insert(0, 'WS-00')
all_items = L + items
ids = [i['id'] for i in all_items]; assert len(ids) == len(set(ids)), 'dup ids'
known = set(ids)
for i in all_items:
    for dep in i['depends_on']: assert dep in known, (i['id'], dep)
MO = {'M1':1,'M2':2,'M3':3,'M4':4}
def key(i):
    p, n = i['id'].split('-', 1)
    return (MO[i['milestone']], i['repo'], -1 if n == 'RV' else (int(n) if n.isdigit() else 999))
all_items.sort(key=key)
json.dump({'items': all_items}, open(f'{B}/plan-data/items.json', 'w'), indent=1, ensure_ascii=False)
with open(f'{B}/items.tsv', 'w') as f:
    f.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n')
    for i in all_items:
        f.write('\t'.join([i['id'], i['milestone'], i['repo'], i['title'].replace('\t',' '), ','.join(i['depends_on']), i['effort'],
                           ','.join(s.split(':')[0] for s in i['smoke']), ','.join(i['issue_refs'])]) + '\n')
from collections import Counter
print(len(all_items), Counter(i['milestone'] for i in all_items))
