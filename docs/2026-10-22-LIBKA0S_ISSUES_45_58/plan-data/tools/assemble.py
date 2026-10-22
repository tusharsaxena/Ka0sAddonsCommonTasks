"""Assemble the run's item manifest from the planning workflow output plus the plan-review resolutions.

    python3 plan-data/tools/assemble.py      # writes plan-data/items.json and items.tsv; validates deps and cycles

Input: plan-data/plan-workflow.json (the planners' items and both critics' findings). The resolutions below
are the session lead's dispositions of every critic finding (see plan-data/PLAN_REVIEW_RESOLUTIONS.md).
"""
import json, os, sys

BUNDLE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(f"{BUNDLE}/plan-data/plan-workflow.json"))
items = {i['id']: i for i in d['items']}
order = [i['id'] for i in d['items']]

# 1. Placeholder dependencies (WS/LK/DC were planned in parallel) mapped to real ids.
DEPMAP = {
    'WS-03': ['WS-01', 'LK-07'], 'WS-05': ['WS-01', 'LK-05'], 'WS-06': ['WS-01', 'LK-07', 'LK-08', 'LK-09'],
    'WS-07': ['WS-01', 'LK-16'], 'WS-08': ['WS-01', 'LK-11', 'LK-16'],
    'DC-01': ['WS-01', 'WS-04', 'WS-09', 'LK-01', 'LK-21'], 'DC-02': ['LK-05', 'WS-05'],
    'DC-03': ['DC-01', 'WS-02', 'WS-04', 'WS-09'], 'DC-04': ['DC-01', 'DC-02', 'DC-03', 'WS-11'],
}
for k, v in DEPMAP.items():
    items[k]['depends_on'] = sorted(set([x for x in items[k]['depends_on'] if ':' not in x] + v))


def add(i, *deps):
    items[i]['depends_on'] = sorted(set(items[i]['depends_on']) | set(deps))


# 2. Missing ordering edges.
add('LK-01', 'WS-01')
add('LK-22', 'WS-11')
add('LK-23', 'DW-02', 'DW-03', 'DW-04', 'DW-06', 'DW-07', 'DW-08', 'LH-02', 'LH-03', 'LH-04', 'LH-10', 'LH-11',
    'LH-12', 'LH-13', 'BL-01', 'BL-02', 'BL-03', 'BL-08', 'BL-09', 'BL-10', 'BL-11', 'BL-12', 'QC-01', 'KC-01', 'MM-01')
add('KC-01', 'LK-09', 'WS-06')
for i in list(items):
    if i.endswith('-RV'):
        add(i, 'WS-11', 'DC-04', 'LK-22')
items['DW-04']['depends_on'] = sorted(set(x for x in items['DW-04']['depends_on'] if x != 'LK-10') | {'LK-11'})

# 3. Spec resolutions, appended verbatim to each item's spec.
R = {
    'BL-12': "Remove `store` from the panel descriptor and its tests (OWNER_SCOPE C.7/C.11: no d.panel.store; the library keeps the dragged point in instance memory). Assert NS.db deep-equal around a drag and that ResetPanelPosition redocks.",
    'LH-13': "Remove `store` from the panel descriptor (OWNER_SCOPE C.7/C.11). The position test asserts NS.db unchanged after a drag and redock after ResetPanelPosition.",
    'DW-02': "(a) The library-absent seam stub carries exactly LK-17's reference stub members (Live, SetProvider, Keys, Unwrapped): no IsGuarded. (b) Lead ruling: OWNER_SCOPE C.11's fixed step-delay constant binds the NEW simulators only; DropWatcher keeps its existing sim.stepDelay schema row (an owner choice from DW's sim feedback batch) and passes it as the timeline's stepDelay. (c) Land as TWO commits, both subject-prefixed 'DW-02: ', each leaving the gate green: first the seam and session (SimSetup, Sim:New, OnStop/OnStopGuarded, stub+parity, Unwrapped) with SimScenario's own machine still driving through the session's Fire/After; then the timeline (prepare/play/defs on the library, DW's step machine deleted, the C.1/C.2 cases).",
    'LH-10': "Land as TWO commits, both subject-prefixed 'LH-10: ', each green: (a) core/SimSeam.lua, the stubs, parity and Unwrapped; (b) modules/Sim.lua session, refusals, auto-stops and the destructive-surface guards. VERIFY adds `wc -l modules/BrowserTable.lua` < 1500.",
    'LK-12': "Decided: LK-12 tests only the idle path, the duplicate-SetProvider raise, Live, Keys and Unwrapped. Every active-path seam case is written in LK-13 against a real session. No `seam.__setActive` hook exists in either item.",
    'LK-13': "No `seam.__setActive` hook: the active-path seam cases deferred from LK-12 are written here against a real session.",
    'LK-11': "Outcome B mechanics: `git revert --no-commit <LK-10 sha>` folded into the single 'LK-11: ' commit, and an exceptions.tsv note in the bundle that LK-10's payload was withdrawn (proof: `test ! -f LibKa0s/WidgetsStepPanel.lua`). Record the outcome (A public / B Sim-private) in the commit subject and in the bundle's 99_EXECUTION_RECORD.md; WS-08 and DW-04 read it.",
    'LK-03': "Cite the kit's own revision contract (a kit member is contract only if a kit version document lists it for consumers; neither was), NOT library-stack-§7's `__` clause, which by WS-01 does not reach the testkit.",
    'LK-02': "Drop the CHANGELOG clause about Quick Comms having re-vendored the unreleased tree (false: QC is on v1.74.0, kit 39); just withdraw the 'No payload file under LibKa0s/ has changed' sentence.",
    'LK-04': "VERIFY adds `wc -l testkit/run-automated-tests.sh` <= 1450 (test_layout_cap counts .sh files; correct the comment that says it does not). If the budget would be exceeded, move the complexity suite into a sourced helper testkit/complexity.sh (copied by the whole-folder testkit vendor) and record the band disposition in LibKa0s CLAUDE.md in the same commit.",
    'LK-05': "Same line budget as LK-04: `wc -l testkit/run-automated-tests.sh` <= 1450, else the sourced helper.",
    'PC-RV': "VERIFY: `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` (0 failed, test_vendor_sync green against v1.75.0); `ka0s-bounded luacheck .` 0/0; `ls libs/LibKa0s/media/icons` lists exactly the declared icons plus LICENSE-open-iconic.txt; the CLAUDE.md provenance line is directly followed by the `LibKa0s icons:` line; `grep -c __releaseChrome settings/OptionsSetup.lua` = 0.",
    'BL-02': "Decided: W.SearchBox accepts opts.icon (LK-06). BankLedger passes NS.Icon('search') and deletes MakeSearchMark and SEARCH_INSET*. No fallback branch.",
    'WG-01': "Add a headless test in tests/test_launcher.lua: 'launcher: a key press in combat takes ToggleFrame's combat route and makes no protected call' (InCombatLockdown true -> OnClick -> alpha/pendingHide route ran, no Show/Hide on a protected frame recorded, UISpecialFrames unchanged).",
    'DW-10': "Cite the recorded #49 rejections at LK-25's API-document entries and the open-evolutions index (WS-10), never a dangling 'What is not here' that no item wrote.",
}
for k, v in R.items():
    items[k]['spec'] += "\n\nPLAN-REVIEW RESOLUTION (binding): " + v
add('DW-10', 'LK-25', 'WS-10')

# 4. Missing items.
NEW = []


def new(id, ms, repo, title, deps, eff, refs, spec, smoke=()):
    NEW.append(dict(id=id, milestone=ms, repo=repo, title=title, depends_on=sorted(set(deps)), effort=eff,
                    issue_refs=refs, smoke=list(smoke), spec=spec))


new('LK-25', 'M1', 'LibKa0s', "Record the #49/#50/#51/#52/#56/#58 rejections in the API documents of the majors they would have joined", ['LK-09'], 'S',
    ['LibKa0s#49', 'LibKa0s#50', 'LibKa0s#51', 'LibKa0s#52', 'LibKa0s#56', 'LibKa0s#58', 'OWNER_SCOPE A'],
    "Docs only, no payload change, no minor bump. Lands before LK-20/LK-22. For each rejected candidate (OWNER_SCOPE A; census and triggers in inputs/analysis-workflow.json), add a 'What is not here' entry (reason against the library-stack-§7 bar, consumers counted, re-check trigger, issue link) to the CURRENT api document of the major it would have joined: Compat (#49 chat sender, tooltip reader + duration decoder, restriction tracker and the four restriction readers, GlobalString pattern compiler), Item (#51 LinkDetail/BetterLink, IdentityKey/SameItem, EffectiveItemLevel, ItemLevelAt/QualityAt, QualityOf, Wowhead URL; the loot-line parser), Options (#50 grid composer), Widgets (#52 Checkbox and a published flat skin), Glow (#56 IconStyle, lifecycle/signature, catalog defaults, O.GlowGroup, LSM 'Solid'), Launcher (#58 binding helper; kit check deferred). test_versioning stays green (no version key moves). Commit 'LK-25: ...'.")
add('LK-20', 'LK-25')
new('MM-04', 'M3', 'MultiMeters', "Compat.ChatSender comment points at the LibKa0s#49 rejection record (comment-only)", ['MM-RV', 'WS-10', 'LK-25'], 'S', ['LibKa0s#49'],
    "Comment-only. core/Compat.lua near :763-766: replace the stale 'exactly one consumer in the collection (anti-pattern #55)' with: two consumers (DropWatcher, MultiMeters), no content beyond a presence guard; promotion rejected at LibKa0s#49 (record: LibKa0s docs/api/Compat 'What is not here', open-evolutions). Gate green. Commit 'MM-04: ...'.")
SR = {'AT': ('AbsorbTracker', ['AT-RV']), 'AM': ('AuraMaster', ['AM-RV']), 'CM': ('ConsumableMaster', ['CM-RV']),
      'DW': ('DropWatcher', ['DW-05', 'DW-06', 'DW-07', 'DW-08', 'DW-09', 'DW-10']), 'KC': ('KickCD', ['KC-01']),
      'LH': ('LootHistory', ['LH-01', 'LH-02', 'LH-03', 'LH-04', 'LH-05', 'LH-14']), 'MM': ('MultiMeters', ['MM-01', 'MM-02', 'MM-04']),
      'PM': ('PanelMaster', ['PM-RV']), 'PF': ('PartyFrameEnhanced', ['PF-RV']), 'PG': ('PremadeGroupsFilterExtension', ['PG-RV']),
      'PC': ('PrettyChat', ['PC-RV']), 'QC': ('QuickComms', ['QC-01', 'QC-02', 'QC-03']), 'WG': ('WhatGroup', ['WG-01'])}
NEXT = {'AT': '01', 'AM': '01', 'CM': '01', 'DW': '12', 'KC': '03', 'LH': '15', 'MM': '05', 'PM': '01', 'PF': '01',
        'PG': '01', 'PC': '01', 'QC': '04', 'WG': '03'}
for p, (repo, deps) in SR.items():
    extra = ""
    if p == 'AM':
        extra = " ALSO (preview-mode marker, WS-03): read AuraMaster's explicit Test mode (NS.State.testMode, modules/Preview.lua, modules/Container.lua placeholder auras) against the marker MUST: visible, localized text in every layout where placeholder data shows (a locked test mode draws no box: check it). Record evidence (file:line) in the commit body. If a gap exists, fix it in this item test-first (headless test plus a smoke line SM-AM-1) and update docs/smoke-tests.md."
    if p == 'QC':
        extra = " Record the preview-mode marker evidence for the pads' drag strip and the dial hub in the commit body."
    if p == 'WG':
        extra = " Read for meaning: 'Test Group — …' content as the preview-mode marker (OWNER_SCOPE F)."
    sid = f"{p}-{NEXT[p]}"
    new(sid, 'M3', repo, "Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations",
        deps + ['WS-11', 'DC-04'], 'S', ['OWNER_SCOPE F', 'design-std D'],
        f"Run the INSTALLED /dev-copilot:wow-revendor-standards procedure (plugin 2.4.0 after the owner's update; read its skill file under ~/.claude/plugins/cache/dev-copilot/, never the ../dev-copilot checkout) in {repo}: TOC X-Standard, README badge and CLAUDE.md 'Standards compliance' agree with v2.86.0; retired notation and unresolvable section references swept outside libs/, tests/_kit/ and frozen bundles. Every citation this run added (launcher-§6, preview-mode, standalone-windows, documentation-§1 item 12, library-stack-§7, slash-commands-§7, automated-tests-§3) resolves against v2.86.0. Gate green. Commit '{sid}: standards reference to v2.86.0'. If nothing changes, add an exceptions.tsv row with a proof command instead of a commit.{extra}",
        ['SM-AM-1: AuraMaster test mode shows a visible TEST marker in every layout (only if AM-01 found a gap)'] if p == 'AM' else ())
new('LH-16', 'M4', 'LootHistory', "GitHub: LootHistory#36 and #37 confirmed closed by the merge and labelled state:done (no commit; exceptions.tsv)", ['LH-04', 'LH-14', 'CT-02'], 'S', ['LootHistory#36', 'LootHistory#37'],
    "After the owner's go-ahead and the --no-ff merge into master: `gh issue view 36/37 --repo tusharsaxena/LootHistory --json state,labels`; swap state:triaged for state:done; if still open, close with a comment naming the merge commit. exceptions.tsv row with the gh proof command.")
new('PG-02', 'M4', 'PremadeGroupsFilterExtension', "GitHub: PGFE#25 confirmed closed by PG-RV's merge into main and labelled state:done (no commit)", ['PG-RV', 'CT-02'], 'S', ['PremadeGroupsFilterExtension#25'],
    "After the owner's go-ahead and the --no-ff merge into MAIN: verify #25 closed (gh issue view 25 --repo tusharsaxena/PremadeGroupsFilterExtension --json state,labels); swap state:* for state:done; close with a comment if still open. exceptions.tsv row with proof.")
new('CT-01', 'M4', 'Ka0sAddonsCommonTasks', "Run records before finalize: 06_SMOKE_TESTS.md results column, 99_EXECUTION_RECORD.md, checkpoints.tsv, exceptions.tsv, RESUME.md state", ['LK-23', 'DC-04'], 'S', ['OWNER_SCOPE H'],
    "Bundle docs/2026-10-22-LIBKA0S_ISSUES_45_58/ only; the plan files (00-05, items.*) stay frozen. 06_SMOKE_TESTS.md keeps every SM-* check with 'Result: owed' until the owner reports; agents never mark a smoke passed. 99_EXECUTION_RECORD.md records per milestone what landed, LK-11's outcome (A/B), any moved local tag (old/new sha) and RV2 refreshes, deviations, and test totals. Commit 'CT-01: ...'.")
new('CT-02', 'M4', 'Ka0sAddonsCommonTasks', "Finalize on the owner's go-ahead: --no-ff merges in dependency order, push the LibKa0s v1.75.0 tag, then delete every run branch, stash and worktree", ['CT-01'], 'M', ['OWNER_SCOPE H'],
    "ONLY on the owner's explicit merge go-ahead. /dev-copilot:finalize across the run's repos in dependency order: WowAddonStandards; LibKa0s (then `git push origin v1.75.0` after confirming `git ls-remote --tags origin v1.75.0` is empty and the local tag points at the merged release commit); dev-copilot; every addon (default branch detected per repo: PGFE main); Ka0sAddonsCommonTasks last. Merge --no-ff, push, delete the feature branch locally and on origin. Then remove any stash and worktree this run created (git stash list / git worktree list in every repo) and record it in 99_EXECUTION_RECORD.md (a post-finalize commit on master). Addon versions are never bumped. After this item, the M4 GitHub closure items run.")

all_items = [items[i] for i in order] + NEW
byid = {i['id']: i for i in all_items}
for cid in ['LK-24', 'WS-12', 'BL-15', 'MM-03', 'KC-02', 'WG-02', 'DW-11']:
    byid[cid]['depends_on'] = sorted(set(byid[cid]['depends_on']) | {'CT-02'})

ids = set(byid)
bad = {i['id']: [x for x in i['depends_on'] if x not in ids] for i in all_items}
bad = {k: v for k, v in bad.items() if v}
if bad:
    sys.exit(f"unresolved deps: {bad}")
state = {}


def visit(n, stack):
    if state.get(n) == 1:
        sys.exit(f"cycle: {stack + [n]}")
    if state.get(n) == 2:
        return
    state[n] = 1
    for x in byid[n]['depends_on']:
        visit(x, stack + [n])
    state[n] = 2


for n in sorted(ids):
    visit(n, [])

json.dump({'items': all_items}, open(f"{BUNDLE}/plan-data/items.json", "w"), indent=1, ensure_ascii=False)
with open(f"{BUNDLE}/items.tsv", "w") as f:
    f.write("id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n")
    for i in all_items:
        smoke = "; ".join(s.split(':')[0].strip() for s in i['smoke'])
        f.write("\t".join([i['id'], i['milestone'], i['repo'], i['title'].replace('\t', ' '), ",".join(i['depends_on']),
                           i['effort'], smoke, ",".join(i['issue_refs'])]) + "\n")
print(f"{len(all_items)} items; deps resolved; acyclic")
