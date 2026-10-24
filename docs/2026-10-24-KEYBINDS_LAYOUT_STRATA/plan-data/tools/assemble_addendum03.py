"""Assemble plan-data/addendum-03.{json,tsv}: the owner's answers (2026-10-24, after CT-02) to the four open calls in
99_EXECUTION_RECORD.md: "1. Widen T1  2. Accept ABS-L11  3. Ok  4. Correct it". Milestone M3. Run once; frozen after."""
import json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GATE = "luacheck . (0/0); lua tests/run.lua green; no authored .lua above 1500 lines (the repo's CLAUDE.md names the exact commands)"
def item(id, repo, title, spec, verify, smoke=()):
    return dict(id=id, milestone='M3', repo=repo, title=title, depends_on=[], effort='S', spec=spec, verify=verify,
                smoke=list(smoke), issue_refs=['020'])
items = [
 item('AM-OC1', 'AuraMaster', 'Widen owner ruling T-1 to allow the ellipsis; three confirm buttons gain it',
  "OWNER CALL (binding): 'Widen T1'. Owner ruling T-1 (tests/test_locale.lua 'every value is ASCII, the em dash excepted') is "
  "widened to also allow U+2026 HORIZONTAL ELLIPSIS. Update the test (name, comment citing the owner's 2026-10-24 call, and the "
  "allowed set) and every place that states T-1 (CLAUDE.md, docs, ARCHITECTURE). Then the three buttons that open a confirmation "
  "end in '…' per options-ui-§21: 'Delete container…', 'Delete this category…', 'Forget unreadable categories…' (labels only; "
  "their locale keys and every location string, doc, smoke step and test that quotes them). Remove the now-moot §21 ellipsis "
  "row from docs/ARCHITECTURE.md > Documented deviations (or mark it resolved, matching how that register records resolved "
  "rows). Tooltips that said 'Asks first.' may keep it. Stored settings untouched. Test first: a case pinning the three labels "
  "end in U+2026 and T-1 still failing any other non-ASCII glyph. Smoke check added, pending. Commit subject 'AM-OC1: '.",
  GATE, smoke=["SM-AM-OC1: the three confirm buttons read 'Delete container…', 'Delete this category…', 'Forget unreadable "
               "categories…' and the '…' draws as an ellipsis, not a box, in the owner's font"]),
 item('AT-OC2', 'AbsorbTracker', 'ABS-L11: one band row for every unit',
  "OWNER CALL (binding): 'Accept ABS-L11'. Make layout id ABS-L11 exactly as its row in "
  "Ka0sAddonsCommonTasks/docs/2026-10-24-KEYBINDS_LAYOUT_STRATA/inputs/layout/AbsorbTracker.md (and its '## Review' section) "
  "describes: one band row for every unit, four quarter cells [Unit dropdown][Enable <Unit> bar][Link to Player][Copy from "
  "Player]; for Player the last two cells stay empty so every control sits at the same x and the band height is the same for "
  "all three units (chromeBlockHeight returns the one-row height for every unit); checkboxes and button bottom-aligned with the "
  "dropdown. L01 and L10 already landed in AT-LY. Move/regroup/relabel only: no stored key, default, range or behaviour change; "
  "the AT-LY stored-path guard must stay green. Test first: the band height is equal for Player, Target and Focus, and the four "
  "controls share their x across units. Its fallback (two-row band plus a recorded §14 deviation) applies only if the cells "
  "cannot fit at the Settings canvas's narrowest width by measurement in the mocks; if you take it, say so. Remove the AT-LY "
  "note that flagged the band height. Docs (settings doc, smoke check rewritten or added, pending). Commit subject 'AT-OC2: '.",
  GATE + "; the band-height test passes", smoke=["SM-AT-OC2: General > unit band: switch Player / Target / Focus; the strip "
  "below never jumps, the four controls sit on one row, and 'Enable Target bar' and 'Copy from Player' are not truncated"]),
 item('WG-OC3', 'WhatGroup', 'options-ui-§21 units on Delay after joining, Width and Height',
  "OWNER CALL (binding): 'Ok' to applying options-ui-§21's units rule. Relabel only: 'Delay after joining (seconds)', "
  "'Width (px)', 'Height (px)' (settings/Schema.lua; locale keys if they route through NS.L; docs, smoke steps and tests that "
  "quote them). No key, default or range change; the WG-LY guard stays green. Commit subject 'WG-OC3: '.", GATE),
 item('LK-OC4', 'LibKa0s', 'CONSUMERS: correct the planned ResetAllTooltip adopters',
  "OWNER CALL (binding): 'Correct it'. docs/api/CONSUMERS.md lists MultiMeters as a planned O.ResetAllTooltip adopter, but "
  "MultiMeters' General Defaults is a page reset and does not adopt it (exceptions.tsv MM-LY:MUL-L-new4). Correct the row from "
  "evidence: grep each roster addon's master (../<Addon>, excluding libs/ and tests/) for real ResetAllTooltip( calls (not the "
  "degradation stub) and list exactly those adopters with file:line, in the table's own format; update the 'planned at v1.77.0' "
  "count line and any other mention that names the planned list. Docs only: no payload file, no minor, and do NOT touch the "
  "v1.77.0 tag (it is pushed). Commit subject 'LK-OC4: '.",
  "luacheck 0/0 and lua tests/run.lua 0 failed (docs tests included)"),
 item('CT-05', 'Ka0sAddonsCommonTasks', 'Record the owner calls (addendum-03)', 'Lead-owned.', 'resume-state.sh'),
]
json.dump({'items': items}, open(f'{B}/plan-data/addendum-03.json', 'w'), indent=1, ensure_ascii=False)
with open(f'{B}/plan-data/addendum-03.tsv', 'w') as f:
    f.write('id\tmilestone\trepo\ttitle\tdepends_on\teffort\tsmoke\tissue_refs\n')
    for i in items:
        f.write('\t'.join([i['id'], i['milestone'], i['repo'], i['title'], '', i['effort'],
                           ','.join(s.split(':')[0] for s in i['smoke']), ','.join(i['issue_refs'])]) + '\n')
print(len(items), 'items')
