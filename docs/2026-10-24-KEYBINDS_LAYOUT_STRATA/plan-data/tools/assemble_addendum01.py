"""Assemble plan-data/addendum-01.json and addendum-01.tsv: M3 (item 020, the settings layout), planned after the
owner's review. Inputs: plan-data/design-m3.json (the reviewed upstream design and the per-addon mapping, run
wf_0f27c45a-4b1) and plan-data/accepted.json. Writes plan-data/layout-map.json (the mapping) for the LY items.
Run once; the outputs are then frozen (RESUME.md: further addenda only)."""
import json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REL = 'Ka0sAddonsCommonTasks/docs/2026-10-24-KEYBINDS_LAYOUT_STRATA'
d = json.load(open(f'{B}/plan-data/design-m3.json'))
acc = json.load(open(f'{B}/plan-data/accepted.json'))
items = [dict(i, milestone='M3') for i in d['design']['items']]
mapping = {a['addon']: a['ids'] for a in d['mapping']}
json.dump(mapping, open(f'{B}/plan-data/layout-map.json', 'w'), indent=1, ensure_ascii=False)

ADDONS = [('AbsorbTracker', 'AT'), ('AuraMaster', 'AM'), ('BankLedger', 'BL'), ('ConsumableMaster', 'CM'), ('DpsRace', 'DR'),
          ('DropWatcher', 'DW'), ('KickCD', 'KC'), ('LootHistory', 'LH'), ('MultiMeters', 'MM'), ('PanelMaster', 'PM'),
          ('PartyFrameEnhanced', 'PF'), ('PremadeGroupsFilterExtension', 'PG'), ('PrettyChat', 'PC'), ('QuickComms', 'QC'),
          ('WhatGroup', 'WG')]
GATE = "luacheck . (0/0); lua tests/run.lua green; no authored .lua above 1500 lines (the repo's CLAUDE.md names the exact commands)"


def item(id, repo, title, deps, effort, spec, verify, smoke=(), refs=()):
    return dict(id=id, milestone='M3', repo=repo, title=title, depends_on=list(deps), effort=effort, spec=spec,
                verify=verify, smoke=list(smoke), issue_refs=list(refs))


for repo, p in ADDONS:
    ids = mapping[repo]
    assert {x['id'] for x in ids} == set(acc['addons'][repo]['layout']), repo
    make = [x for x in ids if not x['veto']]
    veto = [x for x in ids if x['veto']]
    items.append(item(f'{p}-RV2', repo, 'Re-vendor LibKa0s v1.77.0 again after the tag moved (LK-95)', ['LK-95', 'WS-95', f'{p}-ZS'], 'S',
        f"The local annotated tag v1.77.0 in ../LibKa0s was moved by LK-95 (M3 layout surface: OptionsCompose minors 9-11). Re-vendor it "
        f"exactly as {p}-RV did, following the INSTALLED /dev-copilot:wow-revendor-libka0s procedure (copy libs/LibKa0s and tests/_kit whole "
        f"from `git -C ../LibKa0s archive v1.77.0 LibKa0s testkit`, keep the 'LibKa0s icons:' declaration and prune media/icons with the tag's "
        f"tools/prune-icons.lua). The CLAUDE.md provenance line stays v1.77.0; if it records a sha or kit revision, roll it. Do NOT write a new "
        f"bundle: append a section '## Re-vendor after the tag moved (M3)' to docs/revendor/2026-10-24-v1.77.0/05_SUMMARY.md naming the old and "
        f"new tag sha and the per-file minors that moved. If kit surface parity fails, add the new public Options members (for example "
        f"ResetAllTooltip) to the addon's Options degradation stub as inert members, as {p}-RV did. No adoption here: {p}-LY adopts. "
        f"Standards half: nothing, unless the installed wow-revendor-standards check finds drift.",
        f"{GATE}; git -C ../LibKa0s rev-parse v1.77.0^{{}} equals the sha named in the 05_SUMMARY section"))
    lines = '\n'.join(f"- {x['id']}" + (f" (needs {', '.join(x['needs'])})" if x['needs'] else '') + f": {x['note']}" for x in make)
    vlines = '\n'.join(f"- {x['id']}: {x['veto_reason']}" for x in veto) or '- none'
    items.append(item(f'{p}-LY', repo, f'Item 020: the accepted settings-layout changes ({len(make)})', [f'{p}-RV2'], 'L',
        f"Implement item 020 (settings layout) for {repo}. WHAT: exactly the layout ids below, no others. Each id's full text is its row in "
        f"{REL}/inputs/layout/{repo}.md (and its '## Review' section); the {repo} rows of LAYOUT_CROSS_ADDON.md §2 (overrides) bind over the "
        f"addon file; the note below (from the reviewed mapping, plan-data/layout-map.json) binds over both. RULES: options-ui §5, §7, "
        f"§12-§16, §20 and the new §21 (label and tooltip conventions) of standard v2.88.0 as on the WowAddonStandards run branch after WS-95, "
        f"and the LibKa0s v1.77.0 OptionsCompose surface after LK-95 (MasterControls notes / resetPositionTooltip / lockIsPreview, spec.tooltips, "
        f"O.ResetAllTooltip; read the library's docs/api pages, never guess a field).\n"
        f"OWNER RULE (binding): move, regroup and relabel only. Rows may move between sections, tabs and pages; tabs and pages may merge or "
        f"split; headings, labels and tooltips may be reworded. Setting KEYS (stored paths), DEFAULTS, RANGES, BEHAVIOUR and the SET of settings "
        f"stay untouched. A row's Defaults scope following its page is an allowed consequence of a move, provided the tooltips say so (§12/§14). "
        f"If an id cannot be made without breaking the rule, do not make it: list it in the commit body and in your deviations.\n"
        f"Vetoed ids, NOT made:\n{vlines}\n"
        f"Ids to make:\n{lines}\n"
        f"TESTS FIRST: (1) a guard test that the set of stored setting paths and their defaults is unchanged by this item: build the list from the "
        f"addon's schema/defaults at HEAD before your first edit and pin it (path -> default), so any key or default drift fails; (2) update the "
        f"settings tests for the new labels, tab names, order and placement; (3) the kit's surface/schema checks stay green. "
        f"DOCS: docs/settings-panel.md (or the addon's settings doc), README ## Usage paths, any location string in core/, modules/, locales/, "
        f"settings/ (drag-handle tooltips, chat route lines) per §21; docs/smoke-tests.md gets one check per settings page touched (never marked "
        f"passed). Locale keys for every changed visible string in every locale file the addon ships (keep other locales' values if present; "
        f"change only enUS text). COMMITS: several logical commits are fine (one per page or tab group); every subject starts '{p}-LY: '.",
        f"{GATE}; the stored-path/default guard test exists and passes",
        smoke=[f'SM-{p}-LY: every settings page this item touched reads as docs/smoke-tests.md describes; no setting lost, moved key, or changed default; values survive a /reload'],
        refs=['020']))

items.append(item('CT-03', 'Ka0sAddonsCommonTasks', 'Record M3 in 99_EXECUTION_RECORD.md and 06_SMOKE_TESTS.md', [], 'S',
    'Lead-owned: M3 outcomes, vetoes, deviations, the tag move (old and new sha), and every new smoke id, pending.', 'resume-state.sh shows M3 complete'))
json.dump({'items': items}, open(f'{B}/plan-data/addendum-01.json', 'w'), indent=1, ensure_ascii=False)
with open(f'{B}/plan-data/addendum-01.tsv', 'w') as f:
    f.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n')
    for i in items:
        f.write('\t'.join([i['id'], i['milestone'], i['repo'], i['title'].replace('\t', ' '), ','.join(i['depends_on']), i['effort'],
                           ','.join(s.split(':')[0] for s in i['smoke']), ','.join(i['issue_refs'])]) + '\n')
print(len(items), 'M3 items;', sum(1 for i in items if i['id'].endswith('-LY')), 'LY,', sum(len([x for x in v if not x['veto']]) for v in mapping.values()), 'layout ids to make')
