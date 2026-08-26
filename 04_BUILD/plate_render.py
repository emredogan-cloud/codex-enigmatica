#!/usr/bin/env python3
"""
LEVHA ÇİZİCİ — sayılabilir veriyi DETERMİNİSTİK çizer
================================================================================
⚠ BU BETİK BİR GÖRSEL MODELİN YAPAMADIĞI İŞİ YAPAR: SAYAR.

Neden var — ölçülmüş bir başarısızlık:

  Aynı levha (`pl-g3-03`, sözleşme **7 istasyon**) OpenAI Image ile üç
  kez üretildi. Sonuçlar: **8**, **12**, **12** istasyon. Prompt her
  seferinde güçlendirildi — "seen face-on" → düz halka diyagramı, sayı
  listeden çıkarılıp ilk cümleye taşındı. Üslup düzeldi; **sayı
  düzelmedi.**

  Bir gravür bu kitapta SÜS DEĞİL VERİDİR. Yedi istasyon isteyen bir
  bulmacaya on iki istasyonlu bir halka basmak, çözülemeyen bir bulmaca
  basmaktır. Üretici model bu işi yapamıyorsa, iş modele verilmez.

  Bu levhalar saf geometridir: N eşit kama, bir işaretli istasyon. Kod
  bunu kesin sayar. Maliyeti sıfırdır ve sonucu tartışmasızdır.

⭑ VERİ BURADA UYDURULMAZ ⭑ Her sayı prompt kütüphanesinden — yani
üreteçten, yani bulmacanın kendisinden — okunur.

Üslup mevcut levhalarla eşleşir: krem zemin (241,228,208), saf siyah
çizgi, ince paralel tarama, ince cetvel çerçeve. Kenar yumuşaklığı için
4× süper-örnekleme ile çizilir, sonra indirilir.

Çıkış: 07_ASSETS/raw/<id>.png   (sonra normal işleme hattına girer)
"""

from __future__ import annotations

import argparse
import html
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

LIB = os.path.join(pl.ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")
RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
PLATES = os.path.join(pl.ROOT, "07_ASSETS", "plates")

# ⚠ BU ON DÖRT LEVHA AI YÜKSELTİCİYE GİRMEZ — ve bu bir kısayol değil.
# Real-ESRGAN, fotoğrafta OLMAYAN detayı tahmin ederek üretir. Burada
# tahmin edilecek bir şey yok: geometri zaten kesin. Yükseltici, kesin
# kenarları yumuşatır ve tarama çizgilerine olmayan doku ekler. Doğru
# olan, nihai baskı çözünürlüğünde DOĞRUDAN çizmektir.
PRINT_PX = 2700                  # 4,5 inç × 600 dpi
PRINT_DPI = 600.0

CREAM = (241, 228, 208)
INK = (26, 22, 18)
SIZE = 1254                      # teslim edilen levhalarla aynı taban
SS = 4                           # süper-örnekleme çarpanı


def read_data() -> dict:
    """Kütüphaneden {pid: (mekanizma, [veri satırları])}."""
    doc = open(LIB, encoding="utf-8").read()
    strip = lambda s: html.unescape(re.sub("<[^>]+>", "", s)).strip()
    out = {}
    for m in re.finditer(r'<article class="card" id="([a-z0-9-]+)">(.*?)'
                         r'(?=<article class="card"|<h2 )', doc, re.S):
        pid, body = m.group(1), m.group(2)
        mech = re.search(r"<tr><th>Mekanizma</th><td><code>([^<]+)</code>",
                         body)
        dm = re.search(r"⭑ VERİ — DEĞİŞTİRİLEMEZ ⭑</h4><ul class=\"data\">"
                       r"(.*?)</ul>", body, re.S)
        if mech and dm:
            out[pid] = (mech.group(1),
                        [strip(x) for x in
                         re.findall(r"<li>(.*?)</li>", dm.group(1), re.S)])
    return out


def parse(items: list) -> dict:
    """⭑ SAYILAR OKUNUR, TAHMİN EDİLMEZ ⭑"""
    spec = {"marks": [], "stations": None, "bands": None}
    for it in items:
        m = re.match(r"exactly (\d+|ONE) (?:of )?marks? '(.+?)'", it)
        if m:
            n = 1 if m.group(1) == "ONE" else int(m.group(1))
            spec["marks"].append((m.group(2), n))
            continue
        m = re.match(r"exactly (\d+) stations", it)
        if m:
            spec["stations"] = int(m.group(1))
            continue
        m = re.match(r"the engraved field is (\d+) bands", it)
        if m:
            spec["bands"] = int(m.group(1))
    return spec


def _mark(dr, cx, cy, r, glyph):
    """İşaret — kütüphanedeki karakterin geometrik karşılığı."""
    if glyph == "●":
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    elif glyph == "○":
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK,
                   width=int(max(2, r // 3)))
    elif glyph == "■":
        dr.rectangle([cx - r, cy - r, cx + r, cy + r], fill=INK)
    elif glyph == "□":
        dr.rectangle([cx - r, cy - r, cx + r, cy + r], outline=INK,
                     width=int(max(2, r // 3)))
    elif glyph == "◆":
        dr.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                   fill=INK)
    elif glyph == "▲":
        dr.polygon([(cx, cy - r), (cx + r, cy + r * 0.8),
                    (cx - r, cy + r * 0.8)], fill=INK)
    elif glyph == "▼":
        dr.polygon([(cx, cy + r), (cx + r, cy - r * 0.8),
                    (cx - r, cy - r * 0.8)], fill=INK)
    elif glyph == "┬":
        w = int(max(2, r // 3))
        dr.rectangle([cx - r, cy - r * 0.55, cx + r, cy - r * 0.55 + w],
                     fill=INK)
        dr.rectangle([cx - w // 2, cy - r * 0.55, cx + w // 2, cy + r],
                     fill=INK)
    elif glyph in TALLY:
        _tally(dr, cx, cy, r, glyph)
    elif glyph in NUMERAL:
        _numeral(dr, cx, cy, r, glyph)
    else:                                   # · ve tanınmayanlar
        rr = max(2, r // 2)
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=INK)


# ⭑⭑ ÇİZELGE A'NIN ALTI İŞARETİ BİRBİRİNDEN AYIRT EDİLEBİLİR OLMALIDIR ⭑⭑
#
# ⚠ ÖLÇÜLDÜ VE KUSURDU. `_mark` yalnızca dokuz karakteri tanıyordu; geri
# kalan her şey aynı DOLU NOKTAYA düşüyordu. Yazı çözme levhaları tam da
# bu altı işaretten kuruludur ve ikisi ayırt edilemezse levha bir HARF
# değil, bir nokta dizisi basar — okunamaz bir bulmaca.
#
# Altı işaret ÇİZGİYE GÖRE tanımlıdır (`plate.py § MARK_NAMES`):
#     '  çizginin ÜSTÜNDE dik        /  çizginin ÜSTÜNDE eğik
#     ,  çizginin ALTINDA dik        \\  çizginin ALTINDA eğik
#     +  çizgiyi KESEN dik           x  çizgiyi KESEN eğik
# Bu yüzden çizgi de çizilir: işaretin anlamı ona göredir.
TALLY = "',+/\\x"
NUMERAL = "•▵◇▽◻"


def _tally(dr, cx, cy, r, glyph):
    w = int(max(2, r // 3))
    slant = glyph in "/\\x"
    if glyph in "',/":                       # üstte
        y0, y1 = cy - r * 1.5, cy
    elif glyph in ",\\":                     # altta
        y0, y1 = cy, cy + r * 1.5
    else:                                    # kesen
        y0, y1 = cy - r * 1.1, cy + r * 1.1
    dx = r * 0.45 if slant else 0
    dr.line([(cx - dx, y1), (cx + dx, y0)], fill=INK, width=w)


def _numeral(dr, cx, cy, r, glyph):
    w = int(max(2, r // 3))
    if glyph == "•":
        rr = max(2, r // 2)
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=INK)
    elif glyph == "▵":
        dr.polygon([(cx, cy - r), (cx + r, cy + r * 0.8),
                    (cx - r, cy + r * 0.8)], outline=INK, width=w)
    elif glyph == "▽":
        dr.polygon([(cx, cy + r), (cx + r, cy - r * 0.8),
                    (cx - r, cy - r * 0.8)], outline=INK, width=w)
    elif glyph == "◇":
        dr.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                   outline=INK, width=w)
    else:                                    # ◻
        dr.rectangle([cx - r * 0.85, cy - r * 0.85,
                      cx + r * 0.85, cy + r * 0.85], outline=INK, width=w)


def draw_ring(spec: dict, size: int = SIZE):
    """⭑ DÜZ HALKA DİYAGRAMI ⭑ — N eşit kama, kesin sayıda."""
    from PIL import Image, ImageDraw
    S = size * SS
    im = Image.new("RGB", (S, S), CREAM)
    dr = ImageDraw.Draw(im)
    c = S / 2
    R, r = S * 0.40, S * 0.24
    lw = max(2, int(S * 0.0022))

    marks = spec["marks"]
    total_marks = sum(n for _, n in marks)
    # İstasyon sayısı: bildirilmişse o, değilse işaretler kadar.
    n = spec["stations"] or total_marks or 8

    # ── ince cetvel çerçeve ────────────────────────────────────────────
    for pad, w in ((S * 0.035, lw), (S * 0.052, max(1, lw // 2))):
        dr.rectangle([pad, pad, S - pad, S - pad], outline=INK, width=w)

    # ── halka gövdesi ──────────────────────────────────────────────────
    dr.ellipse([c - R, c - R, c + R, c + R], outline=INK, width=lw * 2)
    dr.ellipse([c - r, c - r, c + r, c + r], outline=INK, width=lw * 2)

    # ── ince eş merkezli tarama (gravür dokusu) ────────────────────────
    step = max(3, int(S * 0.0042))
    rad = r + step
    while rad < R - step * 0.5:
        dr.ellipse([c - rad, c - rad, c + rad, c + rad],
                   outline=INK, width=max(1, lw // 2))
        rad += step

    # ── ⭑ N EŞİT KAMA — RADYAL AYIRICILAR ⭑ ────────────────────────────
    # ⚠ Kamalar boşluk BIRAKARAK ayrılır: sözleşme "each separated by a
    # plain gap" diyor. Boşluk, taramanın kesildiği düz bir şerittir.
    gap = math.radians(2.2)
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        for da in (-gap, gap):
            x0, y0 = c + r * math.cos(a + da), c + r * math.sin(a + da)
            x1, y1 = c + R * math.cos(a + da), c + R * math.sin(a + da)
            dr.line([(x0, y0), (x1, y1)], fill=INK, width=lw)
        # boşluğu krem ile temizle
        pts = [(c + r * math.cos(a - gap), c + r * math.sin(a - gap)),
               (c + R * math.cos(a - gap), c + R * math.sin(a - gap)),
               (c + R * math.cos(a + gap), c + R * math.sin(a + gap)),
               (c + r * math.cos(a + gap), c + r * math.sin(a + gap))]
        dr.polygon(pts, fill=CREAM)
        for da in (-gap, gap):
            x0, y0 = c + r * math.cos(a + da), c + r * math.sin(a + da)
            x1, y1 = c + R * math.cos(a + da), c + R * math.sin(a + da)
            dr.line([(x0, y0), (x1, y1)], fill=INK, width=lw)

    # ── işaretler: istasyon ORTASINA, sırayla ──────────────────────────
    seq = []
    for g, cnt in marks:
        seq += [g] * cnt
    mr = (R - r) * 0.22
    for i, g in enumerate(seq[:n]):
        a = -math.pi / 2 + 2 * math.pi * (i + 0.5) / n
        mid = (R + r) / 2
        mx, my = c + mid * math.cos(a), c + mid * math.sin(a)
        # işaretin altındaki taramayı temizle ki sayılabilir kalsın
        dr.ellipse([mx - mr * 1.7, my - mr * 1.7,
                    mx + mr * 1.7, my + mr * 1.7], fill=CREAM)
        _mark(dr, mx, my, mr, g)

    return im.resize((size, size), Image.LANCZOS)


def draw_row(spec: dict, size: int = SIZE):
    """⭑ TEK SATIR NESNE ⭑ — adet veriden, ızgara YOK."""
    from PIL import Image, ImageDraw
    S = size * SS
    im = Image.new("RGB", (S, S), CREAM)
    dr = ImageDraw.Draw(im)
    lw = max(2, int(S * 0.0022))

    seq = []
    for g, cnt in spec["marks"]:
        seq += [g] * cnt
    n = len(seq) or spec["bands"] or 6

    for pad, w in ((S * 0.035, lw), (S * 0.052, max(1, lw // 2))):
        dr.rectangle([pad, pad, S - pad, S - pad], outline=INK, width=w)

    left, right = S * 0.11, S * 0.89
    slot = (right - left) / n
    body_w = slot * 0.62
    top, base = S * 0.30, S * 0.66

    for i, g in enumerate(seq[:n]):
        cx = left + slot * (i + 0.5)
        x0, x1 = cx - body_w / 2, cx + body_w / 2
        # gövde
        dr.rectangle([x0, top, x1, base], outline=INK, width=lw)
        # başlık ve taban silmeleri
        dr.rectangle([x0 - body_w * 0.12, top - body_w * 0.13,
                      x1 + body_w * 0.12, top], outline=INK, width=lw)
        dr.rectangle([x0 - body_w * 0.16, base,
                      x1 + body_w * 0.16, base + body_w * 0.15],
                     outline=INK, width=lw)
        # dikey tarama
        step = max(3, int(body_w * 0.075))
        x = x0 + step
        while x < x1 - step * 0.4:
            dr.line([(x, top + lw * 2), (x, base - lw * 2)],
                    fill=INK, width=max(1, lw // 2))
            x += step
        # işaret
        my = (top + base) / 2
        mr = body_w * 0.20
        dr.ellipse([cx - mr * 1.8, my - mr * 1.8,
                    cx + mr * 1.8, my + mr * 1.8], fill=CREAM)
        _mark(dr, cx, my, mr, g)

    # ortak kaide
    py = base + body_w * 0.15
    dr.rectangle([left - slot * 0.10, py, right + slot * 0.10,
                  py + S * 0.030], outline=INK, width=lw)
    return im.resize((size, size), Image.LANCZOS)


def draw_tablet(spec: dict, size: int = SIZE, seed: int = 0):
    """⭑ RULED TABLET ⭑ — N bands, and EXACTLY the counted marks.

    ⭑ WHY THIS EXISTS, AND WHY IT IS NOT A SHORTCUT ⭑

    The English rebuild changed the immutable data contract of twenty-nine
    plates: different answer lengths mean different glyph counts, different
    numerals, different band heights. Twenty-five of them belong to
    families the ring and row drawers do not cover.

    The obvious move was to re-commission them from the image model. The
    cost report for the last batch settles that: the same plate was asked
    for THREE times with a contract of seven stations and came back with
    eight, twelve and twelve. The prompt was strengthened each time; the
    style improved and THE NUMBER DID NOT. An engraving in this book is
    data, not decoration — a plate that contradicts the printed figure
    beside it is a puzzle that cannot be solved.

    So the same conclusion applies a second time, and for the same reason:
    if the generative model cannot count, the counting is not given to it.
    This costs nothing, and the result is not open to argument.

    The style is the delivered plates': cream ground, pure black line, fine
    parallel hatching, thin ruled frame. The border treatment varies with
    the plate id so that twenty-five tablets are not twenty-five copies —
    and it varies DETERMINISTICALLY, so the same plate always redraws the
    same way.
    """
    from PIL import Image, ImageDraw
    S = size * SS
    im = Image.new("RGB", (S, S), CREAM)
    dr = ImageDraw.Draw(im)
    lw = max(2, int(S * 0.0022))

    bands = max(2, min(int(spec.get("bands") or 4), 20))
    seq = []
    for g, cnt in spec["marks"]:
        seq += [g] * cnt

    # ── ruled frame + hatched border band · three treatments ───────────
    # ⚠ THE BORDER IS NOT DECORATION FOR ITS OWN SAKE. These tablets sit in
    # the same book as seventy-four commissioned engravings; a bare ruled
    # box beside them reads as a printing error rather than as a plate. The
    # band carries the engraver's own texture — close parallel burin lines
    # between two rules — which is the one thing the delivered plates all
    # share. The treatment varies with the plate id so the tablets are not
    # copies of one another, and it varies deterministically.
    for pad, w in ((S * 0.030, lw * 2), (S * 0.066, lw)):
        dr.rectangle([pad, pad, S - pad, S - pad], outline=INK, width=w)
    o0, o1 = S * 0.030, S * 0.066
    style = seed % 3
    hs = max(3, int(S * 0.010)) + style          # hatch pitch varies
    x = o0 + hs
    while x < S - o0:
        dr.line([(x, o0), (x, o1)], fill=INK, width=max(1, lw // 2))
        dr.line([(x, S - o1), (x, S - o0)], fill=INK, width=max(1, lw // 2))
        x += hs
    y = o0 + hs
    while y < S - o0:
        dr.line([(o0, y), (o1, y)], fill=INK, width=max(1, lw // 2))
        dr.line([(S - o1, y), (S - o0, y)], fill=INK, width=max(1, lw // 2))
        y += hs
    dr.rectangle([o0, o0, o1, o1], fill=CREAM, outline=INK, width=lw)
    dr.rectangle([S - o1, o0, S - o0, o1], fill=CREAM, outline=INK, width=lw)
    dr.rectangle([o0, S - o1, o1, S - o0], fill=CREAM, outline=INK, width=lw)
    dr.rectangle([S - o1, S - o1, S - o0, S - o0], fill=CREAM, outline=INK,
                 width=lw)
    if style == 1:
        d = S * 0.086
        dr.rectangle([d, d, S - d, S - d], outline=INK, width=max(1, lw // 2))
    elif style == 2:
        d, t = S * 0.086, S * 0.020
        for (x, y) in ((d, d), (S - d, d), (d, S - d), (S - d, S - d)):
            dr.line([(x - t, y), (x + t, y)], fill=INK, width=lw)
            dr.line([(x, y - t), (x, y + t)], fill=INK, width=lw)

    # ── the tablet body ────────────────────────────────────────────────
    left, right = S * 0.155, S * 0.845
    top, base = S * 0.185, S * 0.815
    dr.rectangle([left, top, right, base], outline=INK, width=lw * 2)

    band_h = (base - top) / bands
    for i in range(1, bands):
        y = top + band_h * i
        dr.line([(left, y), (right, y)], fill=INK, width=lw)

    # ── fine parallel hatching inside every band ───────────────────────
    step = max(3, int(band_h * 0.20))
    for i in range(bands):
        y0 = top + band_h * i + lw * 2
        y1 = top + band_h * (i + 1) - lw * 2
        y = y0 + step
        while y < y1:
            dr.line([(left + lw * 3, y), (right - lw * 3, y)],
                    fill=INK, width=max(1, lw // 3))
            y += step

    # ── ⭑ THE MARKS · EXACTLY AS MANY AS THE CONTRACT SAYS ⭑ ───────────
    # They are laid along the middle band, evenly spaced and never
    # overlapping, and the hatching beneath each one is cleared so that it
    # stays countable on paper.
    if seq:
        mid = top + band_h * (bands // 2) + band_h / 2
        span = (right - left) * 0.78
        x0 = (left + right) / 2 - span / 2
        gapx = span / max(1, len(seq))
        mr = min(band_h * 0.30, gapx * 0.28)
        tally = any(g in TALLY for g in seq)
        # ⭑ THE TALLY MARKS ARE DEFINED AGAINST A LINE ⭑ — above it, below
        # it, or crossing it. Without the line drawn, three of the six
        # marks are the same stroke and the plate is unreadable.
        clear_h = mr * 3.4 if tally else mr * 1.9
        dr.rectangle([x0 - mr, mid - clear_h, x0 + span + mr,
                      mid + clear_h], fill=CREAM)
        if tally:
            dr.line([(x0 - mr, mid), (x0 + span + mr, mid)],
                    fill=INK, width=lw)
        for i, g in enumerate(seq):
            cx = x0 + gapx * (i + 0.5)
            if not tally:
                dr.rectangle([cx - mr * 1.9, mid - mr * 1.9,
                              cx + mr * 1.9, mid + mr * 1.9], fill=CREAM)
            _mark(dr, cx, mid, mr, g)

    return im.resize((size, size), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plates", nargs="*", help="levha kimlikleri")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--print", dest="do_print", action="store_true",
                    help="ayrıca nihai baskı çözünürlüğünde plates/ altına yaz")
    args = ap.parse_args()

    print("=" * 74)
    print("  LEVHA ÇİZİCİ · deterministik · %d × %d px" % (SIZE, SIZE))
    print("=" * 74)

    rep = pl.Report(args.verbose)
    data = read_data()
    todo = args.plates or []
    if not todo:
        print("⛔ levha kimliği verilmedi")
        return 2

    os.makedirs(RAW, exist_ok=True)
    made = []
    for pid in todo:
        if pid not in data:
            rep.check(False, "%s kütüphanede yok" % pid)
            continue
        mech, items = data[pid]
        spec = parse(items)
        seed = sum(ord(c) for c in pid)

        def _draw(px):
            if mech == "plate-embedded-cipher":
                return draw_ring(spec, px)
            if mech == "plate-observation":
                return draw_row(spec, px)
            # ⭑ EVERY OTHER FAMILY GETS THE RULED TABLET ⭑ — its contract
            # is only ever (counted marks, band count), and a tablet holds
            # both exactly. Previously these families were refused here and
            # the work went to the image model, which cannot count.
            return draw_tablet(spec, px, seed)

        im = _draw(SIZE)
        path = os.path.join(RAW, pid + ".png")
        im.save(path, "PNG", optimize=True)
        if args.do_print:
            big = _draw(PRINT_PX)
            os.makedirs(PLATES, exist_ok=True)
            big.save(os.path.join(PLATES, pid + ".png"), "PNG",
                     dpi=(PRINT_DPI, PRINT_DPI), optimize=True)
        n = spec["stations"] or sum(c for _, c in spec["marks"])
        made.append(pid)
        print("  ✓ %-9s %-18s istasyon/nesne=%s işaret=%s"
              % (pid, mech.replace("plate-", ""), n,
                 " ".join("%d×%s" % (c, g) for g, c in spec["marks"]) or "—"))

    rep.check(len(made) == len(todo),
              "⭑ İSTENEN HER LEVHA ÇİZİLDİ ⭑ (%d/%d)" % (len(made), len(todo)))
    rep.facts.update({"rendered": made, "size": SIZE})
    return rep.finish("%d levha çizildi" % len(made), None)


if __name__ == "__main__":
    sys.exit(main())
