#!/usr/bin/env python3
"""LK-F02 (D-03, D-06, D-07): the 2026-10-30 bundle's font_metrics_shipped.py, carried forward for the
faces of this run. Every width is read from the SHIPPED bytes, LibKa0s/LibKa0s/media/fonts, and every
face lib.FONTS names is measured, which is the per-face table SkinDefs carries for font overrides.
Changes from that script: FACES comes from Media.lua; real Friz Quadrata is measured, and a skin's
sizes are no longer fixed for WoW Default; the screenshot fit (its section 6) is dropped, since those
inputs measured the layout model and the model has not moved; the size grid reaches 8.0 .. 18.0, which
the display faces need.

OUTLINE: the client strokes each glyph about one pixel. Whether it also widens each advance is not on
record, so every layout model runs twice: OUTLINE adding 0 px to each advance (ink only), and 1 px
(the stroke on both sides of a one-pixel advance gap). A size has to hold under both.

Read-only. Needs fontTools and uharfbuzz.
Run (a venv that has them):  <venv>/bin/python -I font_metrics_shipped.py > font_metrics_shipped.txt

WoW sizes a font by SetFont(path, height): the height is the EM size in UI units (FreeType char size),
so text width = sum(advance) / unitsPerEm * height.
"""
import math
import os
import re
import sys
from fontTools.ttLib import TTFont

try:
    import uharfbuzz as hb
except ImportError:  # shaped widths are optional
    hb = None

GIT = "/mnt/d/Profile/Users/Tushar/Documents/GIT"
LK = GIT + "/LibKa0s/LibKa0s/media/fonts/"
MEDIA = GIT + "/LibKa0s/LibKa0s/Media.lua"

with open(MEDIA, encoding="utf-8") as fh:
    FACES = {k: LK + v for k, v in re.findall(r'\["([^"]+)"\]\s*=\s*\{ file = "([^"]+\.ttf)"', fh.read())}

# skin, body face, title face, HUD face, its size before this run (fs, titleSize). D-06.
SKINS = [
    ("Ka0s Default", "Ka0s Prototype", "Ka0s Prototype", "Ka0s Prototype", 12, 14),
    ("Obsidian", "Ka0s Expressway", "Ka0s Expressway", "Ka0s Expressway", 12.5, 14.5),
    ("Azeroth", "Ka0s Open Sans Semibold", "Ka0s Open Sans Bold", "Ka0s Open Sans Semibold", 12, 12.5),
    ("Glass", "Ka0s Avant Garde", "Ka0s Avant Garde", "Ka0s Avant Garde", 11.5, 13),
    ("High Contrast", "Ka0s Doris PP", "Ka0s Doris PP", "Ka0s Doris PP", 12, 13),
    ("Ember", "Ka0s Emblem", "Ka0s Emblem", "Ka0s Emblem", 11.5, 12.5),
    ("WoW Default", "Ka0s Friz Quadrata TT", "Ka0s Friz Quadrata TT", "Ka0s Friz Quadrata TT", 12, 14),
    ("WoW Midnight", "Ka0s Segoe UI Semibold", "Ka0s Segoe UI Bold", "Ka0s Segoe UI Semibold", 12.5, 13.5),
    ("WoW Forever", "Ka0s Fira Sans Medium", "Ka0s Fira Sans SemiBold", "Ka0s Fira Sans SemiBold", 12, 13.5),
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
    w("# Friz Quadrata below is the shipped FrizQuadrataTT-Regular.ttf (D-01), not the client's file.\n\n")

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

    base = faces["Ka0s Prototype"]
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

    snapped(faces, rows, w)
    recommend(faces, rows, w)
    width_table(faces, w)
    face_table(faces, w)


SNAP = {"lin": lambda a: a, "round": round, "ceil": math.ceil}


# ── 7. the same equalization under pixel snapping ───────────────────────────────────────────────
LAYOUTS = [("lin", 1.0), ("ceil", 1.0), ("round", 1.08), ("ceil", 1.25), ("round", 1.5), ("round", 1.875)]
OUTLINE_PX = (0, 1)   # px OUTLINE adds to each advance (see the header)
MODELS = [(m, s, o) for o in OUTLINE_PX for (m, s) in LAYOUTS]
CANDS = [x / 2 for x in range(16, 37)]   # 8.0 .. 18.0


def snapped_width(face, corpus, size, mode, scale, outline=0):
    """Corpus width in UI units: HarfBuzz advances (kerning on), each snapped at ppem = size*scale,
    plus `outline` px per glyph."""
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
        tot += sum(SNAP[mode](a / face.upm * size * scale) + outline for a in advs) / scale
    return tot


def snapped(faces, rows, w):
    base = faces["Ka0s Prototype"]
    w("\n## 7. Width error vs Ka0s Default under each layout model\n\n")
    w("model = snap@px-per-UI-unit ('ceil@1.0' is what the owner's screenshots fit). For each skin: its error\n")
    w("at its CURRENT size (now), at the 0.5 step with the smallest worst-case |error| over every model\n")
    w("(best), and at the largest 0.5 step never more than +1% wider than Ka0s Default under any model\n")
    w("(safe: wider is the direction that truncates). Errors listed per model in MODELS order.\n")
    w("REC (section 8) = best, stepped down 0.5 when best runs more than +2% wide under any model.\n\n")
    cands = CANDS
    sizes_now = {sk: (fs, ts, 12) for sk, _b, _t, _h, fs, ts in SKINS}
    w("models: %s\n\n" % ", ".join("%s@%s+%dpx" % m for m in MODELS))
    for role, corpus, bsz, idx in (("body", BODY, BASE_FS, 1), ("title", TITLE, BASE_TS, 2), ("hud", HUD, BASE_HUD, 3)):
        w("### %s (Ka0s Default %s)\n" % (role, bsz))
        w("%-14s %-17s %5s %-8s | %5s %-6s | %5s %-6s | errs at safe\n" % (
            "skin", "face", "now", "now err", "best", "worst", "safe", "worst"))
        bw = {m: snapped_width(base, corpus, bsz, *m) for m in MODELS}
        for r in rows:
            skin, face = r[0], r[idx]
            if skin == "Ka0s Default":
                continue
            table = {}
            for c in cands:
                table[c] = [snapped_width(face, corpus, c, *m) / bw[m] - 1 for m in MODELS]
            now = sizes_now[skin][idx - 1]
            nerr = [snapped_width(face, corpus, now, *m) / bw[m] - 1 for m in MODELS]
            best = min(cands, key=lambda c: max(abs(e) for e in table[c]))
            rec = best - 0.5 if max(table[best]) > 0.02 else best
            if skin not in FIXED:
                REC.setdefault(skin, [None, None, None])[idx - 1] = rec
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
REC = {"Ka0s Default": [12, 14, 12]}   # the reference; filled by snapped()
FIXED = ("Ka0s Default",)


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
    base = faces["Ka0s Prototype"]
    w("\n## 8. Recommended sizes (REC) and their width error vs Ka0s Default, per model\n\n")
    w("models: %s\n\n" % ", ".join("%s@%s+%dpx" % m for m in MODELS))
    for role, corpus, bsz, idx in (("body", BODY, BASE_FS, 1), ("title", TITLE, BASE_TS, 2), ("hud", HUD, BASE_HUD, 3)):
        bw = {m: snapped_width(base, corpus, bsz, *m) for m in MODELS}
        w("### %s\n" % role)
        for r in rows:
            skin, face = r[0], r[idx]
            size = REC[skin][idx - 1]
            errs = [snapped_width(face, corpus, size, *m) / bw[m] - 1 for m in MODELS]
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


def width_table(faces, w):
    w("\n## 9. The WIDTH table tests/test_skin_width_parity.lua pins (linear, shaped, kerning on)\n\n")
    w("avg advance per em over each role's corpus, and each skin's REC size * advance / Ka0s Default's - 1.\n\n")
    base = faces["Ka0s Prototype"]
    w("%-20s %7s %7s %7s\n" % ("face", "body", "title", "hud"))
    for k in sorted({x for s in SKINS for x in s[1:4]}):
        f = faces[k]
        w("%-20s %7.4f %7.4f %7.4f\n" % (k, per_char(f, BODY), per_char(f, TITLE), per_char(f, HUD)))
    w("\n%-14s %-16s %s\n" % ("skin", "REC fs/ts/hud", "linear err % body / title / hud"))
    for skin, bf, tf, hf, _fs, _ts in SKINS:
        r = REC[skin]
        errs = []
        for i, (face, corpus, bsz) in enumerate(((bf, BODY, BASE_FS), (tf, TITLE, BASE_TS), (hf, HUD, BASE_HUD))):
            errs.append(r[i] * per_char(faces[face], corpus) / (bsz * per_char(base, corpus)) - 1)
        w("%-14s %-16s %s\n" % (skin, "%g / %g / %g" % tuple(r), " / ".join("%+.1f" % (e * 100) for e in errs)))
    w("\nHUD_SIZE (hud.fontSize; Ka0s Default 12 is the reference S.HudFontSize scales by):\n")
    for skin, *_ in SKINS:
        w("  %-14s %g  (factor %.4f)\n" % (skin, REC[skin][2], REC[skin][2] / BASE_HUD))


def pick(face, corpus, bsz, base, bw):
    """Section 8's rule for one face and one role."""
    table = {c: [snapped_width(face, corpus, c, *m) / bw[m] - 1 for m in MODELS] for c in CANDS}
    best = min(CANDS, key=lambda c: max(abs(e) for e in table[c]))
    rec = best - 0.5 if max(table[best]) > 0.02 else best
    return rec, table[rec]


def face_table(faces, w):
    base = faces["Ka0s Prototype"]
    w("\n## 10. Every shipped face at Ka0s Default's width (D-07): SkinDefs' FACE_SIZES\n\n")
    w("Section 8's rule per face and role; a face's own row, so an override of it matches Prototype.\n")
    w("lin = linear error, span = min..max over every layout model, outline both ways.\n\n")
    w("%-26s %6s %6s %6s | %-6s %-6s %-6s | %s\n" % (
        "face", "body", "title", "hud", "lin b", "lin t", "lin h", "span b / t / h"))
    lua = []
    for k in sorted(faces):
        f = faces[k]
        got, lins, spans = [], [], []
        for corpus, bsz in ((BODY, BASE_FS), (TITLE, BASE_TS), (HUD, BASE_HUD)):
            bw = {m: snapped_width(base, corpus, bsz, *m) for m in MODELS}
            rec, errs = pick(f, corpus, bsz, base, bw)
            if k == "Ka0s Prototype":
                rec, errs = bsz, [0.0]
            got.append(rec)
            lins.append(rec * per_char(f, corpus) / (bsz * per_char(base, corpus)) - 1)
            spans.append("%+.1f..%+.1f" % (min(errs) * 100, max(errs) * 100))
        w("%-26s %6g %6g %6g | %+5.1f  %+5.1f  %+5.1f  | %s\n" % (
            k, got[0], got[1], got[2], lins[0] * 100, lins[1] * 100, lins[2] * 100, " / ".join(spans)))
        lua.append('  ["%s"] = { %g, %g, %g },' % (k, got[0], got[1], got[2]))
    w("\nLua rows (body, title, hud):\n" + "\n".join(lua) + "\n")
    w("\nThe advances tests/test_skin_width_parity.lua pins (body, title, hud):\n")
    for k in sorted(faces):
        f = faces[k]
        w('  ["%s"] = { body = %.4f, title = %.4f, hud = %.4f },\n' % (
            k, per_char(f, BODY), per_char(f, TITLE), per_char(f, HUD)))


if __name__ == "__main__":
    main()
