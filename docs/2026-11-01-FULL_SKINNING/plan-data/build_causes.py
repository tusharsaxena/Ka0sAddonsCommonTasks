import csv,collections,sys
SRC='/mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-31-FINDINGS_REMEDIATION/SKIN_DEFAULT_GAPS.csv'
rows=list(csv.reader(open(SRC,encoding='utf-8-sig')))
SHORT={'LibKa0s':'LibKa0s','LibKa0sSkinTester':'Tester','AbsorbTracker':'AT','AuraMaster':'AM','BankLedger':'BL','ConsumableMaster':'CM','DpsRace':'DR','DropWatcher':'DW','KickCD':'KC','LootHistory':'LH','MultiMeters':'MM','PanelMaster':'PM','PartyFrameEnhanced':'PFE','PremadeGroupsFilterExtension':'PGFE','PrettyChat':'PC','QuickComms':'QC','WhatGroup':'WG'}
C={ # id: (see in game, reach or None=computed, effort, rec, rows)
'L1':("Minimap button tooltip text, including the green and red Yes/No words, ignores the skin","Library, every addon","S","Fix: one change, the launcher just needs the skin",
 [44,45,73,74,117,132,180,308,373,418,448,479,511,550,551,614,644,719,720]),
'L2':("Hover tooltips: the text lines stay Blizzard's color, on settings rows and a few windows","Library, every addon; plus AM, PC, QC","S","Fix: the standard already says lines follow the skin",
 [26,113,434,540,541,580,607,676,685]),
'L3':("Settings, Scope cleared: header divider, nav rail edge, id suggestion popup and tab edges keep Blizzard art or ignore the skin","Library, every addon","M","Fix: your ruling, every element supports skins",
 [36,656,661,669,692]),
'L4':("Settings, Scope cleared: section headings and some labels stay or snap back to the Blizzard font","Library, every addon; plus DW, MM, PM, PGFE","S","Fix: your ruling",
 [254,414,437,492,666]),
'L5':("Settings, Scope cleared: fixed colors remain, on slash command rows, AuraMaster dropdown values, PanelMaster hints and an id list warning","Library, every addon; plus AM, PM","S","Fix: your ruling",
 [111,112,433,435,493,538,668]),
'L6':("Blizzard or plain white marks (tick, cross, remove, refresh, help, hover flash) beside skinned controls, Scope cleared included","Library, every addon; plus CM, DR, KC, LH, MM, QC","M","Fix: use the Ka0s icons and tint them",
 [27,32,191,192,195,196,227,299,360,362,376,413,603,604,605,608,677,678,681,684,701]),
'L7':("Scroll bars: the small up and down arrow buttons stay Blizzard's","Library, every addon","M","Fix: visible in every window",
 [42,364,691]),
'L8':("Small misses: odd labels never painted, a resize grip with no skin, wrong color role, widget leftovers","Library plus 8 addons","S","Fix: quick, one by one",
 [16,108,136,158,267,346,361,363,385,390,392,393,395,404,409,497,499,500,583,597,697,704,705,707,711,718]),
'L9':("Title bars differ between windows: 24 to 30 high, left or centered","Library, every addon; plus BL, DR, DW, LH, MM, PGFE, WG","M","Fix: most visible on export and tool windows",
 [152,153,251,271,290,367,391,411,503,635,636,698]),
'L10':("Icon shapes and the minimap ring look the same in every skin; only icon color changes","Library, every addon","L","Leave: an icon set is not skin data",
 [30,31,60,72,77,107,131,175,178,226,249,280,286,307,372,417,447,478,505,506,510,532,549,573,590,612,699,700,702,721]),
'L11':("Text size comes from each window's layout; the skin only scales it","Library, every addon","L","Leave: your size ruling, it protects layouts",
 [18,38,155,156,168,208,209,210,288,317,318,345,366,396,456,468,502,576,632,633,686]),
'L12':("Debug console, copy boxes and arrow glyphs always use the fixed-width font","Library, every addon","S","Leave: fixed width is required, and no skin changes it",
 [40,41,76,110,137,138,184,250,258,289,332,347,348,349,410,450,477,508,529,530,617,645,695,696]),
'L13':("Chat lines: cyan [tag], yellow commands, gold, gray, debug ON/OFF words are fixed","Library, every addon","M","Leave: the standard fixes them; chat is not a skinned surface",
 [50,51,78,79,80,81,82,83,84,123,124,125,126,145,146,185,186,187,188,242,243,291,292,293,294,295,333,334,335,336,371,419,420,444,445,481,513,514,515,516,517,518,519,521,522,523,524,525,526,527,618,619,620,621,622,647,648,649,650,651,652,653,654,723,724]),
'D1':("Settings builder: 'use the skin' options start off, and new font, border and bar rows start on Blizzard picks","Library, every addon","S","Fix: every future setting then follows the skin",
 [712,713,714,715,716,717]),
'D2':("HUD text keeps its stored color: bar names, timers, labels, counts","AT, AM, CM, DR, KC, MM, PFE","L","Fix: needs a new HUD text color in every skin, and reverses the 'HUD colors are the player's' decision",
 [55,86,104,167,170,206,311,316,324,325,329,382,383,403,455]),
'D3':("HUD bar fill keeps its stored color","AT, AM, PFE","L","Fix: needs a new HUD fill color in every skin; class and interrupt colors stay",
 [52,88,451]),
'D4':("HUD backgrounds, borders and their thickness keep stored values; some borders are off so the skin's never shows","AT, AM, CM, DR, DW, KC, MM, PFE","M","Fix: skin colors exist, add 'use the skin' and start it on",
 [53,54,89,91,92,93,160,161,162,163,165,176,177,213,218,261,310,322,323,388,389,401,402,454,458]),
'D5':("Glow, pandemic, running-out and cooldown tint colors keep stored values","AM, DW, KC","M","Fix glow; Leave warning tints, they carry meaning",
 [99,100,103,259,312,313]),
'D6':("Text shadows: HUD text ignores the skin's shadow setting","Library; plus AT, AM, CM, DR, DW, KC, MM, PFE, QC","M","Fix: new HUD shadow setting, on the same pass as D2",
 [56,87,169,207,256,320,397,457,577,688]),
'D7':("QuickComms pads and dials keep their own look: every fill, edge and text color, plus the shine","QC only","L","Fix: the biggest single holdout; needs 'use the skin' on each block",
 [555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,574,575,585,586,588,589,591,592,593,594,595,596]),
'D8':("Window text has no outline even though Ka0s Default lists one","Library, every addon","S","Leave: your ruling of Oct 31, HUD text only",
 [39,139,211,255,344,430,467,485,533,634,687]),
'D9':("Ka0s Default keeps Blizzard's resize grip and hover art; other skins tint them","Library, every addon","S","Leave: your earlier ruling, and it does follow the skin",
 [28,29,229,281,509,693,694]),
'A1':("Hand-built tabs, column header bands, footers, row hover, boxes and icon edges skip the skin's versions; some icons have no border at all","BL, DR, DW, LH, MM, PFE, WG","M","Fix: changes Ka0s Default a little, but makes windows match",
 [150,151,219,230,266,269,270,272,273,274,350,351,352,384,387,461,628]),
'A2':("Menus that are Blizzard's although a skinned Ka0s menu exists: DpsRace row menus, MultiMeters segment picker, PGFE dropdowns","DR, MM, PGFE","M","Fix: swap to the Ka0s menu",
 [247,394,487]),
'A3':("Skins with gloss (Glass) show no gloss on HUD bars","AT, AM, KC, MM, PFE","M","Fix: no change under Ka0s Default",
 [59,90,327,379,459]),
'A4':("Delete profile confirmation stays stock under every setting","Every addon with Profiles; found in AT, PM","M","Fix with care: Ace shares this box with non-Ka0s addons",
 [69,443]),
'A5':("Skin Tester's own sample rows that are not painted, so it misreports a skin","Tester","S","Fix: the tester has to tell the truth",
 [9,10,11,12,14,15,17,19,20,23,34,35,37,49]),
'A6':("Cooldown sweep, cast spark, shield, button press and flash, proc glow, text selection stay Blizzard's","AM, CM, DW, KC, PFE, PGFE, WG","L","Leave: game feedback players know; no skin setting exists",
 [95,96,97,171,172,173,260,315,326,463,464,501,630]),
'A7':("Fades and dims, flat thin bars, and skin settings nothing reads: corner radius, scroll width","CM, BL, DR, DW, KC, LH, QC, WG, library","M","Leave: nothing to see today, or a stated rule",
 [147,148,149,154,159,197,241,263,264,265,268,298,353,365,579,584,598,629,689,690,703]),
'A8':("PanelMaster panels keep the colors and textures the player chose","PM","M","Leave: panels are the player's own content",
 [421,422,423,425,428]),
'A9':("DpsRace clocks, bar colors and missing tracks stay as you set them","DR","S","Leave: your own calls, Oct 25 to 31",
 [203,204,212,214,215,216,217]),
}
ORDER=list(C)
MC=[94,101,102,128,140,141,142,194,205,224,234,235,236,237,238,239,240,275,276,277,301,321,342,354,355,356,377,380,381,400,405,407,426,452,453,488,489,490,571,582,602,706,708,709,710]
NG={
'follows the Scope':[2,6,63,85,114,127,189,190,244,253,296,297,337,338,339,340,341,412,431,432,469,470,483,534,535,536,537,599,600,601,606,624,655,657,658,659,660,662,663,664,665,667,670,671,672,673,674,675],
'LSM30 picker, being replaced':[7,65,438],
"can't skin: Settings window":[3,64,121,130,202,285,304,441,484,544,625,727],
"can't skin: GameTooltip frame":[43,62,120,134,201,245,282,283,302,330,331,368,399,440,496,542,581,641,725],
"can't skin: StaticPopup":[46,47,67,68,119,135,200,246,284,303,369,370,415,442,471,498,543,615,642,726],
"can't skin: ColorPickerFrame":[48,66,439,494,616,728],
"can't skin: client Menu":[8,75,118,133,181,309,374,449,512,552,613,722],
"can't skin: other Blizzard frames":[231,233,466,491,520,646],
'game art':[33,98,143,144,174,193,220,221,222,223,225,228,278,279,300,314,328,357,358,359,386,406,462,465,476,572,587,609,623,627,631],
'addon logo':[4,70,71,115,116,129,179,199,248,287,305,306,343,416,436,446,480,495,545,548,553,554,610,611,626,643,680],
'layout':[57,58,61,105,109,157,164,166,198,252,262,319,398,408,424,427,429,460,504,507,531,546,578,637,638,639,640],
'preview by design':[5,13,21,22,24,25,122,182,183,257,375,472,473,474,475,486,528,539,547,679,682,683],
'missing-media fallback':[106,232,378,482],
}
m={}
def put(n,cid,b):
    if n in m: sys.exit(f'dup {n}: {m[n]} vs {cid}')
    if not 2<=n<=728: sys.exit(f'range {n}')
    m[n]=(cid,b)
for c in ORDER:
    for n in C[c][4]: put(n,c,'')
for n in MC: put(n,'MC','meaning color')
for b,l in NG.items():
    for n in l: put(n,'not a gap',b)
miss=[n for n in range(2,729) if n not in m]
if miss:
    for n in miss: x=rows[n-1]; print('MISSING',n,x[0],x[2][:60],x[8])
    sys.exit(1)
with open('SKIN_CAUSES_map.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['row','addon','component','reason','cause_id','bucket'])
    for n in range(2,729):
        x=rows[n-1]; w.writerow([n,x[0],x[2],x[8],m[n][0],m[n][1]])
cnt=collections.Counter(v[0] for v in m.values())
bk=collections.Counter(v[1] for v in m.values() if v[0]=='not a gap')
for c in ORDER:
    print(c,cnt[c],sorted({SHORT[rows[n-1][0]] for n in C[c][4]}))
print('MC',cnt['MC'],'notgap',cnt['not a gap'],'sum',sum(cnt.values()))
fix=sum(cnt[c] for c in ORDER if C[c][3].startswith('Fix')); lv=sum(cnt[c] for c in ORDER if C[c][3].startswith('Leave'))
out=[]
out.append("# Skin causes: yes or no\n")
out.append(f"Goal: change the skin and every addon changes with it. The 727 rows reduce to **{len(ORDER)} causes**, the meaning-color line and {cnt['not a gap']} rows that are not gaps. Settings panel rows count only if they stay stock with the Scope cleared. Recommended Fix: {sum(1 for c in ORDER if C[c][3].startswith('Fix'))} causes, {fix} rows. Recommended Leave: {sum(1 for c in ORDER if C[c][3].startswith('Leave'))} causes, {lv} rows.\n")
out.append("| ID | What you'd see in game | Where it reaches | Rows | Effort | Recommendation |\n|---|---|---|---:|---|---|")
for c in ORDER:
    s,r,e,rec,_=C[c]
    out.append(f"| {c} | {s} | {r} | {cnt[c]} | {e} | {rec} |")
out.append(f"\nL = library, D = default flip, A = addon-specific. Effort: S under a day, M a few days, L a week or more; these are my estimates.\n")
out.append("**One thing to decide with D2 to D7.** A flip reaches new profiles only. Existing profiles keep their stored colors unless we also migrate them, which overwrites choices players made. My recommendation is new profiles plus a one-click 'use the skin for everything' button.\n")
out.append("## What can't be skinned\n")
b=lambda k:bk[k]
out.append(f"- **Blizzard's Settings window** ({b(chr(99)+'an'+chr(39)+'t skin: Settings window')} rows): the frame around our pages belongs to the client, and the standard forbids restyling it.")
out.append(f"- **Client Menu popups** ({b(chr(99)+'an'+chr(39)+'t skin: client Menu')} rows): the minimap right-click menu. The client draws it and offers no paint hook; the only route is replacing it, as A2 does inside windows.")
out.append(f"- **Tooltip frame, confirmation popups, color picker** ({b(chr(99)+'an'+chr(39)+'t skin: GameTooltip frame')}, {b(chr(99)+'an'+chr(39)+'t skin: StaticPopup')} and {b(chr(99)+'an'+chr(39)+'t skin: ColorPickerFrame')} rows): Blizzard frames shared with every addon. The lines we write in a tooltip can follow the skin (L1, L2); the frame can't.")
out.append(f"- **Chat frame font, Group Finder rows, raid warnings, party frames, big countdown** ({b(chr(99)+'an'+chr(39)+'t skin: other Blizzard frames')} rows): client frames the addons only write into or attach to.\n")
out.append("## Meaning colors: confirm\n")
out.append(f"**MC ({cnt['MC']} rows):** class colors, item quality, dispel types, cast states, stat, category, region and data hues stay the same in every skin, because the color is the information. Yes or no?\n")
out.append("## Not gaps\n")
out.append(f"{cnt['not a gap']} rows, no answer needed: follow the Scope {b('follows the Scope')}, LSM30 pickers being replaced {b('LSM30 picker, being replaced')}, can't skin {sum(v for k,v in bk.items() if k.startswith(chr(99)+'an'))}, game art {b('game art')}, addon logos {b('addon logo')}, layout {b('layout')}, previews by design {b('preview by design')}, missing-media fallbacks {b('missing-media fallback')}.\n")
total=sum(cnt[c] for c in ORDER)
out.append(f"Totals: {total} rows in causes + {cnt['MC']} MC + {cnt['not a gap']} not gaps = {total+cnt['MC']+cnt['not a gap']}. Row numbers are the CSV's line numbers (header is line 1). The row-by-row map is `SKIN_CAUSES_map.csv` beside this file.")
open('SKIN_CAUSES.md','w').write('\n'.join(out)+'\n')
