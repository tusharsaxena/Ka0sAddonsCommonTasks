#!/usr/bin/env python3
"""Item 5 (equal font sizes across skins): measure every skin's faces as they will be AFTER the change
and compute the body / title / HUD sizes that give each skin Ka0s Default's text width.

Read-only. Needs fontTools (+ uharfbuzz for shaped/kerned widths, + Pillow for the screenshot check).
Run (a venv that has them):  <venv>/bin/python -I font_metrics.py > font_metrics.txt

WoW sizes a font by SetFont(path, height): the height is the EM size in UI units (FreeType char size),
so text width = sum(advance) / unitsPerEm * height. Section 4 checks that against the owner's
screenshots: the same string at the same nominal size must give one px/em across faces.
"""
import math
import os
import sys
from fontTools.ttLib import TTFont

try:
    import uharfbuzz as hb
except ImportError:  # shaped widths are optional
    hb = None

GIT = "/mnt/d/Profile/Users/Tushar/Documents/GIT"
LK = GIT + "/LibKa0s/LibKa0s/media/fonts/"
CLIENT = "/mnt/g/Games/Blizzard/World of Warcraft/_retail_"
SMM = CLIENT + "/Interface/AddOns/SharedMedia_MyMedia/font/"
SHOTS = GIT + "/Ka0sAddonsCommonTasks/docs/2026-10-30-SKIN_FONTS_AND_FEEDBACK/inputs/screenshots/"

FACES = {
    "Prototype": SMM + "Ka0s Prototype.ttf",
    "Expressway": SMM + "Ka0s Expressway.ttf",
    "FiraSans Medium": SMM + "Ka0s Fira Sans Medium.ttf",
    "Vollkorn": LK + "Vollkorn-Regular.ttf",
    "Vollkorn Bold": LK + "Vollkorn-Bold.ttf",
    "Nunito": LK + "Nunito-Regular.ttf",
    "Nunito SemiBold": LK + "Nunito-SemiBold.ttf",
    "Atkinson": LK + "AtkinsonHyperlegible-Regular.ttf",
    "Atkinson Bold": LK + "AtkinsonHyperlegible-Bold.ttf",
    "Bitter": LK + "Bitter-Regular.ttf",
    "Bitter Bold": LK + "Bitter-Bold.ttf",
    "Philosopher": LK + "Philosopher-Regular.ttf",
    "Philosopher Bold": LK + "Philosopher-Bold.ttf",
    "Friz Quadrata": CLIENT + "/Fonts/FRIZQT__.TTF",
    "JetBrains Mono": LK + "JetBrainsMono-Regular.ttf",
    # today's faces, for reference only (they are being replaced)
    "(now) Oxanium SemiBold": LK + "Oxanium-SemiBold.ttf",
    "(now) Oxanium Bold": LK + "Oxanium-Bold.ttf",
    "(now) Inter": LK + "Inter-Regular.ttf",
    "(now) Inter SemiBold": LK + "Inter-SemiBold.ttf",
    "(now) FiraSans": LK + "FiraSans-Regular.ttf",
    "(now) FiraSans SemiBold": LK + "FiraSans-SemiBold.ttf",
}

# skin, body face, title face, HUD face, current fs, current titleSize (SkinDefs.lua); hud.fontSize is
# 12 in every skin (SkinDefs.lua:336, never overridden).
SKINS = [
    ("Ka0s Default", "Prototype", "Prototype", "Prototype", 12, 14),
    ("Obsidian", "Expressway", "Expressway", "Expressway", 12, 14),
    ("Azeroth", "Vollkorn", "Vollkorn Bold", "Vollkorn Bold", 13, 14),
    ("Glass", "Nunito", "Nunito SemiBold", "Nunito SemiBold", 12.5, 14),
    ("High Contrast", "Atkinson", "Atkinson Bold", "Atkinson Bold", 13.5, 15),
    ("Ember", "Bitter", "Bitter Bold", "Bitter Bold", 12, 13.5),
    ("WoW Default", "Friz Quadrata", "Friz Quadrata", "Friz Quadrata", 12, 14),
    ("WoW Midnight", "Philosopher", "Philosopher Bold", "Philosopher Bold", 12.5, 14),
    ("WoW Forever", "FiraSans Medium", "FiraSans Medium", "FiraSans Medium", 12, 14),
]
BASE_FS, BASE_TS, BASE_HUD = 12, 14, 12

# ── corpus: real strings ────────────────────────────────────────────────────────────────────────
BODY = [
    # LootHistory (image-17): tabs, filters, column headers, rows, footer
    "History", "Insights", "Timeline", "Holdings",
    "Group: Day", "Direction: 3 selected", "Search items...", "Save", "Reset", "Clear", "Export",
    "Date: All", "Bound: All", "Quality: Common+", "Type: All", "SubType: All", "Source: All",
    "Zone: All", "Character: Current",
    "Date", "Time", "Direction", "iLvl", "Item", "Qty", "Quality", "Type", "SubType", "Source", "Zone",
    "Vendor Price", "Auction Price", "Character",
    "Day: 29-Oct-2026 (2)", "Day: 27-Oct-2026 (19)",
    "29-Oct-2026", "27-Oct-2026", "09:47", "23:49", "23:35", "Gain", "Loss",
    "Gold", "Nebulous Voidcore", "Dawn Crystal", "Swirling Arcane Essence", "Artisan Enchanter's Moxie",
    "Bulwark of the Consecrated Flame", "Design: Prismatic Focusing Iris", "Petrified Root",
    "Enchant Chest - Mark of the Worlds", "Mythic Keystone", "Keystone: Kings' Rest (15)",
    "Venomblight Manaflux",
    "+3g 1s 24c", "+5g 40s 62c", "+5000g", "-5000g", "+1", "-1", "+5", "-6", "+1940g 54s",
    "-1940g 54s", "1g 5s", "66g 98s", "58g 96s 31c", "50g", "96g", "2g", "84g", "5g", "59g 5s 17c",
    "315", "318", "Epic", "Rare",
    "Currency", "Tradeskill", "Miscellaneous", "Armor", "Recipe", "Item Enhancement", "Reagent",
    "Midnight", "Enchanting", "Other", "Professions", "Plate", "Jewelcrafting", "Chest", "Keystone",
    "Season 2",
    "Warband Withdraw", "Quest", "Warband Deposit", "Disenchant", "Deconstructed", "Guild Deposit",
    "Auction House", "AH Bought", "Murder Row", "Silvermoon City", "Sacrilege-Frostmourne",
    "Showing 842 of 4252", "Database = 1.6 MB",
    # settings labels (LibKa0s Options* rows)
    "Bar opacity", "Bar texture", "Border style", "Border thickness (px)", "Debug console",
    "Font flags", "Font shadow", "Font size", "Font", "General visibility", "Lock frame",
    "Master opacity", "Master scale", "Minimap button", "Show border", "Test mode",
    "Use the skin's border", "Use the skin's font", "Use the skin's texture",
    "Draw this text in the skin's font. The font picker is not read while this is on.",
]
TITLE = [
    "Ka0s Loot History", "Ka0s Drop Watcher", "Ka0s Multi Meters", "Ka0s KickCD", "Ka0s Aura Master",
    "Ka0s Premade Groups Filter Extension", "Appearance", "Font and texture", "Scope", "General",
    "Profiles", "Skin", "Keybindings", "Insights", "Timeline",
]
HUD = [
    "Kick", "Interrupt", "Counterspell", "Sacrilege", "Frostmourne", "12.3", "0:45", "1:02", "23",
    "1.2M", "345.6K", "8,123,456", "98.7%", "DPS", "HPS", "Mythic+ pull", "KickCD", "Party",
    "Absorb 12.4K", "Power Word: Shield", "Damage Done", "Healing Done", "Epic", "+1940g 54s",
    "Ready", "Cooldown", "Focus", "Target", "Player",
]
SPECIAL = "≈·—–…›‹»«•×↑↓▲▼✓ →←±°"


class Face:
    def __init__(self, name, path):
        self.name, self.path = name, path
        self.ok = os.path.exists(path)
        if not self.ok:
            return
        f = TTFont(path, lazy=True)
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        os2 = f["OS/2"] if "OS/2" in f else None
        hhea = f["hhea"]
        self.asc, self.desc, self.gap = hhea.ascent, hhea.descent, hhea.lineGap
        self.winA = os2.usWinAscent if os2 else None
        self.winD = os2.usWinDescent if os2 else None
        self.cap = getattr(os2, "sCapHeight", 0) or self.glyph_h("H")
        self.xh = getattr(os2, "sxHeight", 0) or self.glyph_h("x")
        if not self.cap:
            self.cap = self.glyph_h("H")
        if not self.xh:
            self.xh = self.glyph_h("x")
        self.family = f["name"].getDebugName(4)
        self.blob = None
        if hb:
            with open(path, "rb") as fh:
                self.blob = hb.Blob(fh.read())
            self.hbfont = hb.Font(hb.Face(self.blob))

    def glyph_h(self, ch):
        f = TTFont(self.path)
        gs = f.getGlyphSet()
        from fontTools.pens.boundsPen import BoundsPen
        g = self.cmap.get(ord(ch))
        if not g:
            return 0
        p = BoundsPen(gs)
        gs[g].draw(p)
        return p.bounds[3] if p.bounds else 0

    def missing(self, text):
        return sorted({c for c in text if c != " " and ord(c) not in self.cmap})

    def adv_raw(self, s):
        """Sum of advances in em, no kerning; a missing glyph counts as .notdef."""
        tot = 0
        for c in s:
            g = self.cmap.get(ord(c), ".notdef")
            tot += self.hmtx[g][0] if g in self.hmtx.metrics else 0
        return tot / self.upm

    def adv_shaped(self, s):
        if not hb:
            return self.adv_raw(s)
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": False})
        return sum(p.x_advance for p in buf.glyph_positions) / self.upm


def per_char(face, corpus, shaped=True):
    fn = face.adv_shaped if shaped else face.adv_raw
    return sum(fn(s) for s in corpus) / sum(len(s) for s in corpus)


def r05(x):
    return round(x * 2) / 2


def main():
    faces = {k: Face(k, v) for k, v in FACES.items()}
    out = sys.stdout
    w = out.write
    w("# font_metrics.txt: generated by font_metrics.py (read-only measurement)\n")
    w("# harfbuzz shaping (kerning on): %s\n" % ("yes" if hb else "NO, raw advances"))
    w("# NOTE: the owner's client replaces Fonts/FRIZQT__.TTF (and ARIALN, FRIENDS, MORPHEUS, skurri) with\n")
    w("# Prototype (identical md5), so \"Friz Quadrata\" below IS Prototype; real Friz is not on disk.\n\n")

    w("## 1. Per-face metrics (per em; avg advance = shaped width / characters over each corpus)\n\n")
    w("%-24s %5s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s\n" % (
        "face", "upm", "body", "raw", "title", "hud", "digits", "cap", "xh", "hhAsc", "hhDsc", "winA+D"))
    digits = ["0123456789", "1940g 54s", "27-Oct-2026", "23:49", "8,123,456", "98.7%"]
    for k, f in faces.items():
        if not f.ok:
            w("%-24s MISSING %s\n" % (k, f.path))
            continue
        w("%-24s %5d %6.4f %6.4f %6.4f %6.4f %6.4f %6.3f %6.3f %6.3f %6.3f %6.3f\n" % (
            k, f.upm, per_char(f, BODY), per_char(f, BODY, False), per_char(f, TITLE), per_char(f, HUD),
            per_char(f, digits), f.cap / f.upm, f.xh / f.upm, f.asc / f.upm, -f.desc / f.upm,
            ((f.winA or 0) + (f.winD or 0)) / f.upm))

    base = faces["Prototype"]
    bB, bT, bH = per_char(base, BODY), per_char(base, TITLE), per_char(base, HUD)

    w("\n## 2. Width equalization vs Ka0s Default (Prototype at fs 12 / title 14 / HUD 12)\n\n")
    w("ratio = skin face's avg advance / Prototype's; exact = base size / ratio; proposed = exact to 0.5;\n")
    w("err = proposed*adv / (base*adv_base) - 1 (+ = wider than Ka0s Default, truncates first);\n")
    w("now = width error at the skin's CURRENT size with the new face.\n\n")
    hdr = "%-14s %-16s | %4s %5s | %6s %6s %5s %6s %6s | %6s %6s %5s %6s %6s | %6s %5s %6s\n"
    w(hdr % ("skin", "body face", "fs", "ts", "bRatio", "fsEx", "fsP", "err%", "now%",
             "tRatio", "tsEx", "tsP", "err%", "now%", "hRatio", "hudP", "err%"))
    rows = []
    for skin, bf, tf, hf, fs, ts in SKINS:
        fb, ft, fh = faces[bf], faces[tf], faces[hf]
        if not (fb.ok and ft.ok and fh.ok):
            w("%-14s missing face\n" % skin)
            continue
        rb, rt, rh = per_char(fb, BODY) / bB, per_char(ft, TITLE) / bT, per_char(fh, HUD) / bH
        fsx, tsx, hx = BASE_FS / rb, BASE_TS / rt, BASE_HUD / rh
        fsp, tsp, hp = r05(fsx), r05(tsx), r05(hx)
        if skin == "Ka0s Default":
            fsp, tsp, hp = BASE_FS, BASE_TS, BASE_HUD
        eb, et, eh = fsp * rb / BASE_FS - 1, tsp * rt / BASE_TS - 1, hp * rh / BASE_HUD - 1
        nb, nt = fs * rb / BASE_FS - 1, ts * rt / BASE_TS - 1
        rows.append((skin, fb, ft, fh, fsp, tsp, hp, rb, rt, rh))
        w(hdr.replace("%6s %6s %5s %6s %6s | %6s %6s %5s %6s %6s | %6s %5s %6s",
                      "%6.3f %6.2f %5.1f %+6.1f %+6.1f | %6.3f %6.2f %5.1f %+6.1f %+6.1f | %6.3f %5.1f %+6.1f")
          % (skin, bf, fs, ts, rb, fsx, fsp, eb * 100, nb * 100, rt, tsx, tsp, et * 100, nt * 100,
             rh, hp, eh * 100))

    w("\n## 3. Spread: per-string width error at the proposed body size (body corpus)\n\n")
    w("min / median / max of (string width / Prototype's at 12) - 1, and the widest-error strings.\n\n")
    for skin, fb, ft, fh, fsp, tsp, hp, rb, rt, rh in rows:
        errs = []
        for s in BODY:
            a = base.adv_shaped(s) * BASE_FS
            if a <= 0 or len(s) < 4:   # "-1" / "+5" are one-glyph noise
                continue
            errs.append((fb.adv_shaped(s) * fsp / a - 1, s))
        errs.sort()
        med = errs[len(errs) // 2][0]
        w("%-14s fs %4.1f  min %+5.1f%%  med %+5.1f%%  max %+5.1f%%   widest: %s (%+.1f%%)\n" % (
            skin, fsp, errs[0][0] * 100, med * 100, errs[-1][0] * 100, errs[-1][1][:40], errs[-1][0] * 100))

    w("\n## 4. Vertical metrics at the proposed sizes (UI units = size * per-em value)\n\n")
    w("cap / x-height in UI units vs Ka0s Default; hhea asc+desc and win asc+desc vs the size (the\n")
    w("FontString line box WoW gives a string is about its font height; >1.0 means glyphs reach past it).\n\n")
    w("%-14s %5s | %6s %6s | %6s %6s | %7s %7s\n" % ("skin", "fs", "capU", "base", "xhU", "base", "hhea/em", "win/em"))
    for skin, fb, ft, fh, fsp, tsp, hp, rb, rt, rh in rows:
        w("%-14s %5.1f | %6.2f %6.2f | %6.2f %6.2f | %7.3f %7.3f\n" % (
            skin, fsp, fb.cap / fb.upm * fsp, base.cap / base.upm * BASE_FS, fb.xh / fb.upm * fsp,
            base.xh / base.upm * BASE_FS, (fb.asc - fb.desc) / fb.upm, ((fb.winA or 0) + (fb.winD or 0)) / fb.upm))

    w("\n## 5. Glyph coverage: corpus characters and common UI symbols each face cannot draw\n\n")
    allc = "".join(BODY + TITLE + HUD)
    for k, f in faces.items():
        if not f.ok:
            continue
        miss_corpus = f.missing(allc)
        miss_sp = f.missing(SPECIAL)
        w("%-24s corpus-missing: %-10s symbols-missing: %s\n" % (
            k, "".join(miss_corpus) or "-", " ".join("U+%04X" % ord(c) for c in miss_sp) or "-"))

    shot_check(faces, w)
    snapped(faces, rows, w)
    recommend(faces, rows, w)


# ── 6. screenshot check: how does WoW lay a string out? ─────────────────────────────────────────
# Ink widths (px) of five strings on one row each of image-17 (Ka0s Default + Prototype override),
# image-18 (Obsidian + Expressway override) and image-28 (WoW Forever + Fira Sans Medium override),
# every one at fs 12. Boxes are (x0, y0, x1, y1); a pixel is ink when its brightest channel > 140.
SHOT_STRINGS = ["Bulwark of the Consecrated Flame", "Warband Withdraw", "Miscellaneous", "Silvermoon City",
                "Sacrilege-Frostmourne"]
SHOT_BOXES = {
    ("image-17.png", "Prototype"): [(350, 447, 600, 461), (1025, 274, 1150, 288), (797, 360, 900, 374),
                                    (1152, 274, 1300, 288), (1512, 274, 1660, 288)],
    ("image-18.png", "Expressway"): [(345, 442, 600, 456), (1020, 269, 1142, 283), (790, 355, 890, 369),
                                     (1146, 269, 1295, 283), (1505, 269, 1655, 283)],
    ("image-28.png", "FiraSans Medium"): [(352, 441, 600, 455), (1025, 268, 1152, 282), (795, 354, 895, 368),
                                          (1152, 268, 1300, 282), (1510, 268, 1660, 282)],
}
SNAP = {"lin": lambda a: a, "round": round, "ceil": math.ceil}


def ink_model(face, s, ppem, mode):
    """Predicted ink width: pen to the last glyph (each advance snapped by `mode`) + its xMax - first xMin."""
    f = TTFont(face.path)
    gl, names = f["glyf"] if "glyf" in f else None, [face.cmap[ord(c)] for c in s]
    pen = sum(SNAP[mode](face.hmtx[g][0] / face.upm * ppem) for g in names[:-1])
    if gl is None:
        return pen + face.hmtx[names[-1]][0] / face.upm * ppem
    x0 = getattr(gl[names[0]], "xMin", 0) / face.upm * ppem
    x1 = getattr(gl[names[-1]], "xMax", 0) / face.upm * ppem
    return pen + x1 - x0


def shot_check(faces, w):
    try:
        from PIL import Image
    except ImportError:
        w("\n## 6. screenshot check skipped (no Pillow)\n")
        return
    w("\n## 6. Screenshot check: em sizing and per-glyph pixel snapping\n\n")
    meas = {}
    for (fn, face), boxes in SHOT_BOXES.items():
        im = Image.open(SHOTS + fn).convert("RGB")
        px = im.load()
        for s, (x0, y0, x1, y1) in zip(SHOT_STRINGS, boxes):
            xs = [x for x in range(x0, x1) for y in range(y0, y1) if max(px[x, y]) > 140]
            meas[(face, s)] = max(xs) - min(xs) + 1
    w("measured ink px (fs 12):\n")
    for face in ("Prototype", "Expressway", "FiraSans Medium"):
        w("  %-16s %s\n" % (face, "  ".join("%s=%d" % (s.split()[0], meas[(face, s)]) for s in SHOT_STRINGS)))
    w("\nbest-fit px per UI unit for each layout model (ppem = 12 * scale), and the residuals:\n")
    for mode in ("lin", "round", "ceil"):
        best = None
        for i in range(900, 1300):
            sc = i / 1000
            e = [ink_model(faces[f], s, 12 * sc, mode) - m for (f, s), m in meas.items()]
            sq = sum(x * x for x in e)
            if best is None or sq < best[0]:
                best = (sq, sc, e)
        w("  %-5s scale %.3f  rms %.2f px  residuals %s\n" % (
            mode, best[1], (best[0] / len(best[2])) ** 0.5, " ".join("%+.1f" % x for x in best[2])))
    w("A linear (unsnapped em) layout leaves Expressway 4-5 px short where the other faces fit; snapping\n")
    w("each glyph's advance to a whole pixel fits all three faces (ceil at exactly 1 px per UI unit best).\n")


# ── 7. the same equalization under pixel snapping ───────────────────────────────────────────────
MODELS = [("lin", 1.0), ("ceil", 1.0), ("round", 1.08), ("ceil", 1.25), ("round", 1.5), ("round", 1.875)]


def snapped_width(face, corpus, size, mode, scale):
    """Corpus width in UI units: HarfBuzz advances (kerning on), each snapped at ppem = size*scale."""
    tot = 0.0
    for s in corpus:
        if hb:
            buf = hb.Buffer()
            buf.add_str(s)
            buf.guess_segment_properties()
            hb.shape(face.hbfont, buf, {"kern": True, "liga": False})
            advs = [p.x_advance for p in buf.glyph_positions]
        else:
            advs = [face.hmtx[face.cmap.get(ord(c), ".notdef")][0] for c in s]
        tot += sum(SNAP[mode](a / face.upm * size * scale) for a in advs) / scale
    return tot


def snapped(faces, rows, w):
    base = faces["Prototype"]
    w("\n## 7. Width error vs Ka0s Default under each layout model\n\n")
    w("model = snap@px-per-UI-unit ('ceil@1.0' is what the owner's screenshots fit). For each skin: its error\n")
    w("at its CURRENT size (now), at the 0.5 step with the smallest worst-case |error| over every model\n")
    w("(best), and at the largest 0.5 step never more than +1% wider than Ka0s Default under any model\n")
    w("(safe: wider is the direction that truncates). Errors listed per model in MODELS order.\n\n")
    cands = [x / 2 for x in range(20, 31)]   # 10.0 .. 15.0
    sizes_now = {sk: (fs, ts, 12) for sk, _b, _t, _h, fs, ts in SKINS}
    w("models: %s\n\n" % ", ".join("%s@%s" % m for m in MODELS))
    for role, corpus, bsz, idx in (("body", BODY, BASE_FS, 1), ("title", TITLE, BASE_TS, 2), ("hud", HUD, BASE_HUD, 3)):
        w("### %s (Ka0s Default %s)\n" % (role, bsz))
        w("%-14s %-17s %5s %-8s | %5s %-6s | %5s %-6s | errs at safe\n" % (
            "skin", "face", "now", "now err", "best", "worst", "safe", "worst"))
        bw = {m: snapped_width(base, corpus, bsz, m[0], m[1]) for m in MODELS}
        for r in rows:
            skin, face = r[0], r[idx]
            if skin == "Ka0s Default":
                continue
            table = {}
            for c in cands:
                table[c] = [snapped_width(face, corpus, c, m[0], m[1]) / bw[m] - 1 for m in MODELS]
            now = sizes_now[skin][idx - 1]
            nerr = [snapped_width(face, corpus, now, m[0], m[1]) / bw[m] - 1 for m in MODELS]
            best = min(cands, key=lambda c: max(abs(e) for e in table[c]))
            safe_l = [c for c in cands if max(table[c]) <= 0.01]
            safe = max(safe_l) if safe_l else None
            def span(es):
                return "%+.1f..%+.1f" % (min(es) * 100, max(es) * 100)
            w("%-14s %-17s %5.1f %-11s | %5.1f %-11s | %5s %-11s | %s\n" % (
                skin, face.name, now, span(nerr), best, span(table[best]),
                safe, span(table[safe]) if safe else "-",
                " ".join("%+.1f" % (e * 100) for e in table[safe]) if safe else "-"))
        w("\n")


# ── 8. the recommendation ───────────────────────────────────────────────────────────────────────
# Rule: per role, the 0.5 step with the smallest worst-case |error| over MODELS (section 7 "best"),
# stepped down 0.5 when that pick is more than +2% wider than Ka0s Default under any model.
REC = {  # skin: (font.bodySize, font.titleSize, hud.fontSize)
    "Ka0s Default": (12, 14, 12), "Obsidian": (12.5, 14.5, 13), "Azeroth": (12, 12.5, 11),
    "Glass": (11.5, 13, 11), "High Contrast": (12, 13, 11), "Ember": (11.5, 12.5, 11),
    "WoW Default": (12, 14, 12), "WoW Midnight": (12.5, 13.5, 12), "WoW Forever": (12, 13.5, 12),
}


def ink_extent(face, corpus):
    f = TTFont(face.path)
    gl = f["glyf"] if "glyf" in f else None
    if gl is None:
        return face.asc / face.upm, face.desc / face.upm
    hi = lo = 0
    for c in set("".join(corpus)):
        g = gl[face.cmap[ord(c)]] if ord(c) in face.cmap else None
        if g is not None and hasattr(g, "yMax"):
            hi, lo = max(hi, g.yMax), min(lo, g.yMin)
    return hi / face.upm, lo / face.upm


def recommend(faces, rows, w):
    base = faces["Prototype"]
    w("\n## 8. Recommended sizes (REC) and their width error vs Ka0s Default, per model\n\n")
    w("models: %s\n\n" % ", ".join("%s@%s" % m for m in MODELS))
    for role, corpus, bsz, idx in (("body", BODY, BASE_FS, 1), ("title", TITLE, BASE_TS, 2), ("hud", HUD, BASE_HUD, 3)):
        bw = {m: snapped_width(base, corpus, bsz, m[0], m[1]) for m in MODELS}
        w("### %s\n" % role)
        for r in rows:
            skin, face = r[0], r[idx]
            size = REC[skin][idx - 1]
            errs = [snapped_width(face, corpus, size, m[0], m[1]) / bw[m] - 1 for m in MODELS]
            w("%-14s %-17s %5.1f  %s\n" % (skin, face.name, size, " ".join("%+5.1f%%" % (e * 100) for e in errs)))
        w("\n")
    w("### vertical, body face at REC body size (UI units): corpus ink top / bottom, cap, x-height\n")
    w("(LootHistory rows are 18 units, defaults/Profile.lua:50)\n")
    bt, bb = ink_extent(base, BODY)
    for r in rows:
        skin, face = r[0], r[1]
        size = REC[skin][0]
        t, b = ink_extent(face, BODY)
        w("%-14s %5.1f  top %5.2f bottom %+5.2f span %5.2f  cap %5.2f  xh %5.2f   (base span %5.2f cap %5.2f xh %5.2f)\n" % (
            skin, size, t * size, b * size, (t - b) * size, face.cap / face.upm * size, face.xh / face.upm * size,
            (bt - bb) * BASE_FS, base.cap / base.upm * BASE_FS, base.xh / base.upm * BASE_FS))


if __name__ == "__main__":
    main()
