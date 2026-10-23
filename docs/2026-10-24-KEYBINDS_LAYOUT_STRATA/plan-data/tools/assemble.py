"""Assemble plan-data/items.json and items.tsv: the reviewed upstream design (M1), the generated addon items (M2)
and the lead's items (M4). Run once at planning time; the outputs are then frozen (RESUME.md: addenda only).
M3 (item 020, the settings layout) is planned after the owner's review of preview.html, as addendum-01."""
import json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REL = 'Ka0sAddonsCommonTasks/docs/2026-10-24-KEYBINDS_LAYOUT_STRATA'
d = json.load(open(f'{B}/plan-data/design-upstream.json'))
items = [dict(i, milestone='M1') for i in d['reviewed']['items']]

ADDONS = [('AbsorbTracker', 'AT'), ('AuraMaster', 'AM'), ('BankLedger', 'BL'), ('ConsumableMaster', 'CM'), ('DpsRace', 'DR'),
          ('DropWatcher', 'DW'), ('KickCD', 'KC'), ('LootHistory', 'LH'), ('MultiMeters', 'MM'), ('PanelMaster', 'PM'),
          ('PartyFrameEnhanced', 'PF'), ('PremadeGroupsFilterExtension', 'PG'), ('PrettyChat', 'PC'), ('QuickComms', 'QC'),
          ('WhatGroup', 'WG')]
WINDOWED = {'BankLedger', 'DpsRace', 'DropWatcher', 'LootHistory', 'MultiMeters', 'QuickComms', 'WhatGroup'}
LABELS = {
    'BankLedger': "the window toggle's label becomes 'Toggle ledger window'",
    'DpsRace': "labels become 'Toggle race HUD', 'Toggle results window', 'Arm or cancel race'",
    'DropWatcher': "the window toggle's label becomes 'Toggle drop feed'",
    'LootHistory': "the window toggle's label becomes 'Toggle history browser'",
    'MultiMeters': "labels unchanged ('Toggle meter windows')",
    'QuickComms': "labels unchanged; Bindings.xml is reordered so 'Toggle Comms Pads' is first, then 'Open Comms Dial 1'..'4' (XC-01, QUI-L32)",
    'WhatGroup': "labels unchanged ('Toggle group popup'); BINDING_HEADER_WHATGROUP reads the brand constant instead of the literal",
}

def item(id, ms, repo, title, deps, effort, spec, verify, smoke=(), refs=()):
    return dict(id=id, milestone=ms, repo=repo, title=title, depends_on=list(deps), effort=effort, spec=spec,
                verify=verify, smoke=list(smoke), issue_refs=list(refs))

GATE = "luacheck . (0/0); lua tests/run.lua green; no authored .lua above 1500 lines (the repo's CLAUDE.md names the exact commands)"
for repo, p in ADDONS:
    items.append(item(f'{p}-RV', 'M2', repo, 'Re-vendor LibKa0s v1.77.0 and refresh the standards reference to v2.88.0', ['LK-90', 'WS-90'], 'M',
        f"Follow the INSTALLED /dev-copilot:wow-revendor-libka0s procedure for the LOCAL tag v1.77.0 (copy libs/LibKa0s and tests/_kit whole from "
        f"`git -C ../LibKa0s archive v1.77.0 LibKa0s testkit`, roll the CLAUDE.md provenance line, keep the 'LibKa0s icons:' declaration and prune "
        f"media/icons to it with the tag's tools/prune-icons.lua, write docs/revendor/2026-10-24-v1.77.0/). Adoption interview: do NOT interview; the "
        f"adoptions this run needs are the {p}-KB and {p}-ZS items, so record every other candidate as 'deferred (run 2026-10-24)' in the bundle and "
        f"file nothing. If the new kit revision (42) makes existing tests fail, fix the addon side minimally in this item (for example the Options stubs "
        f"gaining OptionsKeybinds members, or a Bindings.xml shape test that now asserts the v2.88.0 shape: for a windowed addon leave that test to "
        f"{p}-KB by marking it pending only if the item's gate cannot otherwise be green, and say so). Then follow the INSTALLED "
        f"/dev-copilot:wow-revendor-standards procedure for this repo only: TOC X-Standard, README badge and CLAUDE.md 'Standards compliance' to v2.88.0. "
        f"One commit, or two (libka0s then standards) with the same id prefix.",
        f"{GATE}; grep v1.77.0 CLAUDE.md; grep 2.88.0 *.toc README.md CLAUDE.md", refs=['OWNER_SCOPE']))
    if repo in WINDOWED:
        items.append(item(f'{p}-KB', 'M2', repo, "Item 015: a Keybindings section of its own in Options -> Keybindings, and the General > Keybindings tab",
            [f'{p}-RV'], 'M',
            f"Implement item 015 for {repo} exactly as launcher-§6 and options-ui-§20 (standard v2.88.0) and the LibKa0s v1.77.0 docs/api page for "
            f"OptionsKeybinds define it; design background in {REL}/inputs/KEYBINDINGS_RESEARCH.md §5.2-§5.4 and LAYOUT_CROSS_ADDON.md XC-01..XC-03. "
            f"1) Bindings.xml: every <Binding> gets category=\"BINDING_HEADER_{repo.upper()}\" and no header=; binding NAMES never change (saved keys survive). "
            f"2) Declare NS.BINDINGS once (Bindings.xml order, Show window binding first) in the module that creates the toggle button; {LABELS[repo]}. "
            f"Labels are locale keys (locales/enUS.lua and any other locale file the addon ships). 3) Add the General > Keybindings tab as the LAST tab "
            f"of the General page through O.KeybindingsTab (no host-drawn rows, no 'before' placement). 4) Tests first: the Bindings.xml shape through the "
            f"kit's Kit.assertBindingsXml, labels, the tab's presence and position, a key bound through the tab (Kit.keybindThroughTab) shows in GetBindingKey "
            f"and a key set via SetBinding shows in the tab after UPDATE_BINDINGS, combat refusal; update the existing binding tests (tests/test_disabled.lua "
            f"step 8 and the repo's launcher/keybinding tests) to the new strings. 5) Docs: README ## Usage and docs/settings-panel.md give the path "
            f"'Options -> Keybindings -> Ka0s <Name>' or 'General > Keybindings in this addon's settings'; ARCHITECTURE if it lists bindings; "
            f"docs/smoke-tests.md gets the smoke checks below (never marked passed)."
            + (" QuickComms: this reintroduces an in-panel key editor that b902e35 (2026-10-21) removed; the owner's 015 brief supersedes that decision. "
               "Record that in the commit body and in docs/ARCHITECTURE.md where the removal is described. Use the library surface, not the retired "
               "Dial.BindKey code." if repo == 'QuickComms' else ''),
            f"{GATE}; grep -c 'header=' Bindings.xml == 0; grep -c 'BINDING_HEADER_{repo.upper()}' Bindings.xml >= 1",
            smoke=[f'SM-{p}-KB1: Options -> Keybindings shows a section titled with the brand, holding this addon\'s bindings with the new labels; no blank spacer row',
                   f'SM-{p}-KB2: binding a key in General > Keybindings shows it in Options -> Keybindings and vice versa, in both account and character-specific modes',
                   f'SM-{p}-KB3: the bound key toggles the window; Escape during capture cancels without closing Settings; in combat the tab refuses'],
            refs=['015']))
    zdeps = [f'{p}-RV'] + ([f'{p}-KB'] if repo in WINDOWED else [])
    items.append(item(f'{p}-ZS', 'M2', repo, 'Item 030: one frame-layering table and the accepted strata changes', zdeps, 'L',
        f"Implement item 030 for {repo}. The rules: frame-layering (standard v2.88.0, every §) and the LibKa0s v1.77.0 surfaces it names. The analysis: "
        f"{REL}/inputs/strata/{repo}.md (inventory, problems, proposed map) and STRATA_MODEL.md (overrides for this addon bind over the addon file). "
        f"WHICH CHANGES: only the ids listed for {repo} under 'strata' in {REL}/plan-data/accepted.json (the owner's decisions applied to the defaults; "
        f"a change not listed there is NOT made, even if the analysis proposes it). Also apply the decided calls listed in accepted.json 'calls' that "
        f"name this addon. 1) Add the one layers table NS.Constants.LAYERS (frame-layering's tier keys) in core/Constants.lua (or the addon's constants "
        f"module) and route every strata and level write through it, relative to the parent (no absolute levels). 2) Make each accepted change, tests "
        f"first through the kit's frame-layer recorder (mock_layers): pin the strata/level/toplevel of every frame class in the proposed map. 3) Player-"
        f"chosen strata rows keep their keys, defaults and value sets (no setting changes); their tooltip becomes O.StrataTooltip(...) where the addon "
        f"has such a row. 4) docs/ARCHITECTURE.md gets a short 'Frame layering' section listing the addon's tiers; docs/smoke-tests.md gets one smoke "
        f"check per visible change (never marked passed). If accepted.json lists no strata change for this addon, still do step 1 for the frames the "
        f"addon creates and the ARCHITECTURE section.",
        f"{GATE}; grep -rn 'SetFrameLevel(%d' --include=*.lua core modules settings returns nothing absolute",
        smoke=[f'SM-{p}-ZS: every visible strata change listed in docs/smoke-tests.md behaves as described (popups over their windows, handles reachable, overlays over their hosts)'],
        refs=['030']))

items.append(item('CT-01', 'M4', 'Ka0sAddonsCommonTasks', 'Record the run: 99_EXECUTION_RECORD.md, checkpoints, 06_SMOKE_TESTS.md complete', [], 'S',
    'Lead-owned. Fill 99_EXECUTION_RECORD.md (outcomes, deviations, tag moves, review notes), 06_SMOKE_TESTS.md (every smoke id from every item, '
    'status pending until the owner reports), and the last checkpoints.tsv row.', 'resume-state.sh shows M1-M3 complete'))
items.append(item('CT-02', 'M4', 'Ka0sAddonsCommonTasks', 'Finalize on the owner\'s go-ahead: merge every repo, push LibKa0s v1.77.0, clean up', ['CT-01'], 'M',
    'ONLY on the owner\'s explicit merge go-ahead. /dev-copilot:finalize in order WowAddonStandards -> LibKa0s (then push tag v1.77.0) -> dev-copilot '
    '-> 15 addons -> Ka0sAddonsCommonTasks. Merge --no-ff, push, delete the run branch locally and on origin; remove every stash and worktree this run '
    'created. No addon version bumps.', 'git branch -a | grep -c keybinds-layout-strata == 0 in every repo'))

json.dump({'items': items}, open(f'{B}/plan-data/items.json', 'w'), indent=1, ensure_ascii=False)
with open(f'{B}/items.tsv', 'w') as f:
    f.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n')
    for i in items:
        f.write('\t'.join([i['id'], i['milestone'], i['repo'], i['title'].replace('\t', ' '), ','.join(i['depends_on']), i['effort'],
                           ','.join(s.split(':')[0] for s in i['smoke']), ','.join(i['issue_refs'])]) + '\n')
print(len(items), 'items;', {m: sum(1 for i in items if i['milestone'] == m) for m in ('M1', 'M2', 'M3', 'M4')})
