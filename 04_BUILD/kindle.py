#!/usr/bin/env python3
"""
KINDLE SÜRÜMÜ — EPUB 3, sabit değil AKIŞKAN, levhalar ölçekli
================================================================================
⚠ MİMARİ SEÇİMİ BİR TERCİH DEĞİL, BİR ÖLÇÜMÜN SONUCUDUR.

Üç seçenek vardı:

  ① BASKI PDF'İNİ ÇEVİR — reddedildi. 6×9 sayfayı 6 inçlik bir ekrana
    sıkıştırmak, 9,5 punto metni okunmaz yapar. Yönerge § 8 bunu açıkça
    yasaklıyor ("Do not simply convert the print PDF into a broken
    reflowable ebook").

  ② SABİT DÜZEN (fixed-layout) — reddedildi. Levhalar için iyi, METİN
    için felaket: okur yazı tipini büyütemez, telefonda 6×9 bir sayfa
    avuç içinde okunmaz. Bu kitabın metni levhadan ÇOK daha uzundur
    (17.648 kelime metin, 103 levha).

  ③ ⭑ AKIŞKAN EPUB 3 + TAM GENİŞLİK LEVHA ⭑ — seçildi. Metin akar ve
    büyütülebilir; her levha kendi bloğunda, en-boy korunarak, ekranın
    tam genişliğinde durur. Sayılabilir işaretler ekranda YAKINLAŞTIRMA
    ile sayılır — Kindle'ın kendi görsel büyütmesi bunu destekler.

⚠ KAPAK YALNIZCA ÖNDÜR. Sırt, arka kapak, barkod, taşma YOKTUR —
sarmal bir baskı kapağını Kindle'a koymak, ürün sayfasında yan yatmış
bir kitap göstermektir.

⚠ SON SORUNUN CEVABI BURADA DA BASILMAZ (kitabın kendi sözleşmesi).

Çıkış: 08_OUTPUT/KINDLE/  → codex-enigmatica.epub · cover.jpg · metadata
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
SOLDIR = os.path.join(pl.ROOT, "01_SOURCE", "solutions")
PLATES = os.path.join(pl.ROOT, "07_ASSETS", "plates")
RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
OUTDIR = os.path.join(pl.ROOT, "08_OUTPUT", "KINDLE")
META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "kindle.json")

# ⚠ KDP Kindle kapak önerisi: 1,6:1 (yükseklik:genişlik), en az 1000 px
# uzun kenar, ideal 2560 × 1600. Baskı sarmalı BURAYA KONULMAZ.
COVER_W, COVER_H = 1600, 2560
PLATE_PX = 1400                      # ekran için yeterli, dosya için makul
PLATE_Q = 82


def esc(s) -> str:
    return html.escape(str(s), quote=False)


def load_solutions() -> dict:
    out = {}
    for name in ("gate-1.json", "gate-2.json", "gate-345.json"):
        p = os.path.join(SOLDIR, name)
        if os.path.isfile(p):
            for s in (json.load(open(p, encoding="utf-8")).get("puzzles")
                      or []):
                out[s["puzzleId"]] = s
    return out


def flow(val) -> list:
    if val is None:
        return []
    if isinstance(val, str):
        return [x for x in val.split("\n\n") if x.strip()]
    if isinstance(val, list):
        return [str(x) for x in val if str(x).strip()]
    if isinstance(val, dict):
        out = []
        for v in val.values():
            out += flow(v)
        return out
    return [str(val)]


CSS = """
@page { margin: 0.6em; }
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55;
       margin: 0 0.4em; }
h1 { font-size: 1.5em; text-align: center; margin: 1.2em 0 0.6em;
     page-break-before: always; }
h2 { font-size: 1.15em; margin: 1.3em 0 0.4em; }
h3 { font-size: 1.0em; margin: 1.1em 0 0.3em; }
p  { margin: 0 0 0.65em; text-align: justify; }
p.lead { font-style: italic; color: #3a332a; }
p.label { font-size: 0.72em; letter-spacing: 0.08em; text-transform: uppercase;
          color: #6d6459; margin: 0.8em 0 0.15em; font-weight: bold; }
pre { font-family: 'Courier New', monospace; font-size: 0.68em;
      line-height: 1.25; white-space: pre; overflow-x: auto;
      margin: 0.5em 0; }
div.plate { text-align: center; margin: 0.9em 0; page-break-inside: avoid; }
div.plate img { max-width: 100%; height: auto; }
p.note { border-left: 3px solid #8a6a3b; padding-left: 0.7em;
         font-size: 0.92em; color: #3a332a; }
hr { border: 0; border-top: 1px solid #ded5c7; margin: 1.2em 0; }
"""


def xhtml(title: str, body: str) -> bytes:
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" '
            'lang="en">\n<head>\n<meta charset="utf-8"/>\n'
            '<title>%s</title>\n'
            '<link rel="stylesheet" type="text/css" href="style.css"/>\n'
            '</head>\n<body>\n%s\n</body>\n</html>\n'
            % (esc(title), body)).encode("utf-8")


def make_cover(src: str, dst: str, meta: dict, cover_stats: dict) -> tuple:
    """⭑ YALNIZCA ÖN KAPAK + TİPOGRAFİ ⭑

    ⚠ İLK SÜRÜM SAĞ KENARDAN KÖR BİR KUTU KESTİ ve açık folyonun sol
    yarısını kırptı — üstelik başlık, alt başlık ve yazar HİÇ YOKTU
    (yönerge § D bunları açıkça istiyor).

    Ön panelin yeri TAHMİN EDİLMEZ, sarmal geometrisinden HESAPLANIR:
        ön panel başlangıcı = (taşma + arka + sırt) / tam genişlik
    Tipografi baskı kapağıyla AYNI motorla basılır: mürekkep harfin
    altındaki piksellerden seçilir, gerekirse vektör hâle eklenir.
    """
    from PIL import Image, ImageDraw, ImageFont
    import cover_type as CT

    full_w = cover_stats.get("widthIn") or 12.908
    full_h = cover_stats.get("heightIn") or 9.250
    spine = cover_stats.get("spineIn") or 0.6575
    edge = cover_stats.get("wrapIn") or 0.125
    trim_w = (full_w - spine - 2 * edge) / 2

    im = Image.open(src).convert("RGB")
    # ① sarmal oranına kırp (covers.py ile aynı işlem)
    want = full_w / full_h
    iw, ih = im.size
    if iw / ih > want:
        nw = int(round(ih * want))
        im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(round(iw / want))
        im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))

    # ② ÖN PANELİ kes — hesaplanan orandan
    w, h = im.size
    x0 = int(round(w * (edge + trim_w + spine) / full_w))
    x1 = int(round(w * (edge + trim_w + spine + trim_w) / full_w))
    y0 = int(round(h * edge / full_h))
    y1 = int(round(h * (edge + (full_h - 2 * edge)) / full_h))
    im = im.crop((x0, y0, x1, y1))

    # ③ 1,6:1 Kindle oranına oturt (yükseklikten kırp, ortadan)
    tw, th = COVER_W, COVER_H
    cw, ch = im.size
    if cw / ch > tw / th:
        nw = int(round(ch * tw / th))
        im = im.crop(((cw - nw) // 2, 0, (cw - nw) // 2 + nw, ch))
    else:
        nh = int(round(cw * th / tw))
        im = im.crop((0, (ch - nh) // 2, cw, (ch - nh) // 2 + nh))
    im = im.resize((tw, th), Image.LANCZOS)

    # ④ TİPOGRAFİ — ölçülen karşıtlık + vektör benzeri hâle (raster)
    F = "/usr/share/fonts/truetype/dejavu"
    REG, BOLD = (os.path.join(F, "DejaVuSerif.ttf"),
                 os.path.join(F, "DejaVuSerif-Bold.ttf"))
    dr = ImageDraw.Draw(im)
    rows = []

    def draw_line(text, font_path, size, cy, bold=False):
        if not text:
            return None
        f = ImageFont.truetype(font_path, size)
        bb = dr.textbbox((0, 0), text, font=f)
        tw_ = bb[2] - bb[0]
        while tw_ > tw * 0.86 and size > 14:
            size = int(size * 0.94)
            f = ImageFont.truetype(font_path, size)
            bb = dr.textbbox((0, 0), text, font=f)
            tw_ = bb[2] - bb[0]
        cx = tw // 2
        r = CT.place(im, text, font_path, size, cx, cy)
        ink = tuple(int(round(c * 255)) for c in r["ink"])
        halo = tuple(int(round(c * 255)) for c in r["halo"])
        x = cx - tw_ // 2 - bb[0]
        y = cy - (bb[3] - bb[1]) // 2 - bb[1]
        if r["needsHalo"]:
            dr.text((x, y), text, font=f, fill=ink,
                    stroke_width=max(2, size // 14), stroke_fill=halo)
        else:
            dr.text((x, y), text, font=f, fill=ink)
        r.update(text=text, sizePx=size)
        rows.append(r)
        return r

    title = (meta.get("title") or "").upper()
    sub = meta.get("subtitle") or ""
    author = (meta.get("author") or "").upper()

    draw_line(title, BOLD, int(th * 0.062), int(th * 0.115))
    if sub:
        words, line, lines = sub.split(), "", []
        f = ImageFont.truetype(REG, int(th * 0.026))
        for wd in words:
            t = (line + " " + wd).strip()
            if dr.textlength(t, font=f) > tw * 0.80:
                lines.append(line)
                line = wd
            else:
                line = t
        lines.append(line)
        yy = int(th * 0.185)
        for ln in lines[:3]:
            draw_line(ln, REG, int(th * 0.026), yy)
            yy += int(th * 0.036)
    draw_line(author, BOLD, int(th * 0.036), int(th * 0.915))

    im.save(dst, "JPEG", quality=92, optimize=True, progressive=True)
    return im.size, rows


def plate_img(pid: str, cache: str) -> str | None:
    """Levhayı ekran için hazırlar: gri, zemin beyaz, JPEG."""
    # ⚠ Her bulmacanın levhası YOKTUR (plateId null olabilir).
    if not pid:
        return None
    src = os.path.join(PLATES, pid + ".png")
    if not os.path.isfile(src):
        return None
    out = os.path.join(cache, pid + ".jpg")
    if not os.path.isfile(out):
        from PIL import Image
        im = Image.open(src).convert("L")
        if im.width > PLATE_PX:
            im = im.resize((PLATE_PX,
                            round(im.height * PLATE_PX / im.width)),
                           Image.LANCZOS)
        lut = [255 if i >= 212 else int(round(255 * i / 212))
               for i in range(256)]
        im.point(lut).save(out, "JPEG", quality=PLATE_Q, optimize=True)
    return out


# ⭑ KINDLE ALICI BİLGİLENDİRMESİ ⭑ (yönerge § 9)
# ⚠ ÖZÜR DEĞİL, TARİF. Ne olduğunu söyler, olmayan bir şey vaat etmez
# ve satın almaktan caydırmaz. "Yazamazsınız" demez — "baskı sürümü
# üstüne yazmak isteyenler için" der.
KINDLE_NOTE_EN = (
    "About this digital edition — This is the complete Codex Enigmatica: "
    "all 101 puzzles, all 303 hints and the full solution section. Every "
    "engraved plate is reproduced digitally and can be enlarged on screen "
    "to examine the fine detail each puzzle depends on. The puzzles are "
    "solved by observation and inference, so nothing here requires you to "
    "write in the book. If you prefer to annotate the plates by hand, or "
    "want the engravings at their printed size, the paperback and "
    "hardcover editions are made for that."
)


def build_epub(book, sols, meta, out_dir):
    from PIL import Image                                      # noqa: F401
    cache = os.path.join(pl.ROOT, "07_ASSETS", "processed", "kindle-cache")
    os.makedirs(cache, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    m = book.get("matter") or {}
    puzzles = book.get("puzzles") or []
    title = meta.get("title") or ""
    author = meta.get("author") or ""

    docs, images, nav = [], {}, []

    def add(fid, heading, body, in_nav=True):
        docs.append((fid, heading, body))
        if in_nav:
            nav.append((fid, heading))

    # ① başlık
    add("title", title,
        '<h1>%s</h1>\n<p style="text-align:center">%s</p>\n'
        '<p style="text-align:center">%s</p>\n'
        '<p style="text-align:center;font-size:.85em;color:#6d6459">%s</p>'
        % (esc(title), esc(meta.get("subtitle") or ""), esc(author),
           esc(meta.get("publisher") or "")))

    # ② künye + dijital sürüm notu
    body = "".join("<p>%s</p>" % esc(x) for x in flow(m.get("copyright")))
    body += '<hr/><p class="note">%s</p>' % esc(KINDLE_NOTE_EN)
    add("copyright", "Copyright", body, in_nav=False)

    # ③ çerçeve + sözleşme
    for key, head in (("frameOpening", "Opening"), ("contract", "The Contract")):
        rows = flow(m.get(key))
        if rows:
            add(key, head, "<h1>%s</h1>" % esc(head)
                + "".join('<p class="lead">%s</p>' % esc(x) for x in rows))

    # ④ araçlar
    tp = book.get("toolsPlate") or {}
    if tp:
        b = "<h1>Tools</h1>"
        b += "".join('<p class="lead">%s</p>' % esc(x)
                     for x in flow(m.get("toolsLead")))
        for name, val in tp.items():
            b += "<h2>%s</h2>" % esc(name.replace("-", " ").title())
            if isinstance(val, dict):
                txt = "\n".join("%-22s %s" % (k, v) for k, v in val.items())
            elif isinstance(val, list):
                txt = "\n".join(str(x) for x in val)
            else:
                txt = str(val)
            b += "<pre>%s</pre>" % esc(txt)
        add("tools", "Tools", b)

    # ⑤ ısınma
    wu = book.get("warmUp") or []
    if wu:
        b = "<h1>Warm-up</h1>"
        b += "".join('<p class="lead">%s</p>' % esc(x)
                     for x in flow(m.get("warmUpLead")))
        for i, w in enumerate(wu, 1):
            b += "<h3>%d · %s</h3>" % (i, esc(w.get("title") or ""))
            for k in ("lead", "note", "text", "body"):
                if w.get(k):
                    b += "<p>%s</p>" % esc(w[k])
        add("warmup", "Warm-up", b)

    # ⑥ kapılar
    gates, order = {}, []
    for p in puzzles:
        g = p.get("gate") or "?"
        if g not in gates:
            gates[g] = []
            order.append(g)
        gates[g].append(p)
    frames = [book.get("frame"), book.get("frame2"), book.get("frame3"),
              book.get("frame4"), book.get("frame5")]

    for gi, g in enumerate(order):
        fr = frames[gi] if gi < len(frames) and frames[gi] else {}
        b = "<h1>Gate %d — %s</h1>" % (gi + 1, esc(g.title()))
        ip = plate_img("dc-gate-%d" % (gi + 1), cache)
        if ip:
            images[os.path.basename(ip)] = ip
            b += '<div class="plate"><img src="img/%s" alt="Gate %d"/></div>' \
                 % (os.path.basename(ip), gi + 1)
        b += "".join('<p class="lead">%s</p>' % esc(x)
                     for x in flow(fr.get("opening")))
        for p in gates[g]:
            b += "<h2>%s · %s</h2>" % (esc(p.get("puzzleId")),
                                       esc(p.get("title") or ""))
            if p.get("flavour"):
                b += '<p class="lead">%s</p>' % esc(p["flavour"])
            ip = plate_img(p.get("plateId"), cache)
            if ip:
                images[os.path.basename(ip)] = ip
                b += ('<div class="plate"><img src="img/%s" alt="%s"/></div>'
                      % (os.path.basename(ip), esc(p.get("plateId"))))
            for lab, key in (("Objective", "objective"), ("Input", "input"),
                             ("What to do", "readerAction")):
                if p.get(key):
                    b += '<p class="label">%s</p><p>%s</p>' % (lab, esc(p[key]))
            for lab, key in (("Figure", "figure"), ("Table", "printedTable")):
                if p.get(key):
                    b += '<p class="label">%s</p><pre>%s</pre>' \
                         % (lab, esc(p[key]))
            for lab, key in (("Clues", "clues"), ("Constraints", "constraints")):
                if p.get(key):
                    b += '<p class="label">%s</p>' % lab
                    b += "".join("<p>· %s</p>" % esc(c) for c in p[key])
            if p.get("answerFormat"):
                b += '<p class="label">Answer format</p><p>%s</p>' \
                     % esc(p["answerFormat"])
        add("gate%d" % (gi + 1), "Gate %d" % (gi + 1), b)

    # ⑦ ipuçları
    b = "<h1>Hints</h1>"
    b += "".join('<p class="lead">%s</p>' % esc(x)
                 for x in flow(m.get("hintsLead")))
    nh = 0
    for p in puzzles:
        s = sols.get(p["puzzleId"])
        if not s or not s.get("hints"):
            continue
        b += "<h3>%s · %s</h3>" % (esc(p["puzzleId"]),
                                   esc(p.get("title") or ""))
        for i, h in enumerate(s["hints"], 1):
            t = h if isinstance(h, str) else (h.get("text") or "")
            b += "<p><b>%d.</b> %s</p>" % (i, esc(t))
            nh += 1
    add("hints", "Hints", b)

    # ⑧ çözümler — META HARİÇ
    b = "<h1>Solutions</h1>"
    b += "".join('<p class="lead">%s</p>' % esc(x)
                 for x in flow(m.get("solutionsLead")))
    ns, withheld = 0, []
    for p in puzzles:
        s = sols.get(p["puzzleId"])
        if not s:
            continue
        # ⭑ Kitabın kendi sözleşmesi: son sorunun cevabı HİÇBİR YERDE.
        if str(p["puzzleId"]).startswith("meta"):
            withheld.append(p["puzzleId"])
            continue
        b += "<h3>%s · %s</h3>" % (esc(p["puzzleId"]),
                                   esc(p.get("title") or ""))
        if s.get("finalAnswer"):
            b += "<p><b>%s</b></p>" % esc(s["finalAnswer"])
        if s.get("explanation"):
            b += "<p>%s</p>" % esc(s["explanation"])
        ns += 1
    add("solutions", "Solutions", b)

    # ⑨ arka madde
    for key, head in (("cipherReference", "Cipher Reference"),
                      ("sourcesLead", "Sources"), ("closing", "Closing"),
                      ("colophon", "Colophon")):
        rows = flow(m.get(key))
        if rows:
            add(key, head, "<h1>%s</h1>" % esc(head)
                + "".join("<p>%s</p>" % esc(x) for x in rows))

    # ── kapak ──────────────────────────────────────────────────────────
    art = os.path.join(RAW, "codex-enigmatica-wrap-cover-option-01.png")
    cover_jpg = os.path.join(out_dir, "cover.jpg")
    cstats = (pl.load_json(os.path.join(
        pl.ROOT, "06_REPORTS", "tracked", "cover.json")) or {}).get("facts") or {}
    (cw, ch), type_rows = make_cover(art, cover_jpg, meta, cstats)

    # ── EPUB paketi ────────────────────────────────────────────────────
    epub = os.path.join(out_dir, "codex-enigmatica.epub")
    uid = "urn:uuid:codex-enigmatica-kindle-1"
    with zipfile.ZipFile(epub, "w") as z:
        z.writestr("mimetype", "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<container version="1.0" xmlns="urn:oasis:names:tc:'
                   'opendocument:xmlns:container">\n<rootfiles>\n'
                   '<rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/>\n'
                   '</rootfiles>\n</container>\n')
        z.writestr("OEBPS/style.css", CSS)
        z.write(cover_jpg, "OEBPS/cover.jpg")
        for name, path in images.items():
            z.write(path, "OEBPS/img/" + name)
        for fid, head, body in docs:
            z.writestr("OEBPS/%s.xhtml" % fid, xhtml(head, body))

        items = ['<item id="css" href="style.css" media-type="text/css"/>',
                 '<item id="cover-image" href="cover.jpg" '
                 'media-type="image/jpeg" properties="cover-image"/>',
                 '<item id="nav" href="nav.xhtml" '
                 'media-type="application/xhtml+xml" properties="nav"/>']
        spine = []
        for fid, _h, _b in docs:
            items.append('<item id="%s" href="%s.xhtml" '
                         'media-type="application/xhtml+xml"/>' % (fid, fid))
            spine.append('<itemref idref="%s"/>' % fid)
        for i, name in enumerate(sorted(images)):
            items.append('<item id="img%d" href="img/%s" '
                         'media-type="image/jpeg"/>' % (i, name))

        z.writestr("OEBPS/nav.xhtml", xhtml("Contents",
            '<h1>Contents</h1>\n<nav epub:type="toc" id="toc" '
            'xmlns:epub="http://www.idpf.org/2007/ops">\n<ol>\n'
            + "".join('<li><a href="%s.xhtml">%s</a></li>\n' % (f, esc(h))
                      for f, h in nav)
            + '</ol>\n</nav>'))

        z.writestr("OEBPS/content.opf",
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
            'unique-identifier="bookid" xml:lang="en">\n'
            '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            '<dc:identifier id="bookid">%s</dc:identifier>\n'
            '<dc:title>%s</dc:title>\n<dc:creator>%s</dc:creator>\n'
            '<dc:language>en</dc:language>\n<dc:publisher>%s</dc:publisher>\n'
            '<dc:description>%s</dc:description>\n'
            '<meta property="dcterms:modified">2026-08-26T00:00:00Z</meta>\n'
            '</metadata>\n<manifest>\n%s\n</manifest>\n'
            '<spine>\n%s\n</spine>\n</package>\n'
            % (uid, esc(meta.get("title") or ""), esc(author),
               esc(meta.get("publisher") or ""),
               esc((meta.get("description") or "").replace("\n", " ")[:900]),
               "\n".join(items), "\n".join(spine)))

    return {"epub": epub, "cover": cover_jpg, "coverPx": [cw, ch],
            "coverType": [{"text": r["text"], "contrast": r["contrast"],
                           "halo": r["needsHalo"]} for r in type_rows],
            "docs": len(docs), "images": len(images),
            "hintsTypeset": nh, "solutionsTypeset": ns,
            "metaWithheld": withheld,
            "bytes": os.path.getsize(epub)}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KINDLE · akışkan EPUB 3")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    book = pl.load_json(BOOK) or {}
    meta = pl.load_json(META) or {}
    if not book:
        rep.check(False, "manuscript yok")
        return rep.finish("manuscript yok", None)

    info = build_epub(book, load_solutions(), meta, OUTDIR)

    print("\n── paket ──")
    print("  %-24s %s" % ("EPUB", os.path.relpath(info["epub"], pl.ROOT)))
    print("  %-24s %.1f MB" % ("boyut", info["bytes"] / 1e6))
    print("  %-24s %d" % ("belge (bölüm)", info["docs"]))
    print("  %-24s %d" % ("gömülü levha", info["images"]))
    print("  %-24s %d × %d" % ("kapak (YALNIZCA ÖN)", *info["coverPx"]))
    print("  %-24s %d / %d" % ("ipucu / çözüm",
                               info["hintsTypeset"], info["solutionsTypeset"]))

    # ── DENETİMLER ─────────────────────────────────────────────────────
    z = zipfile.ZipFile(info["epub"])
    names = z.namelist()
    rep.check(names[0] == "mimetype",
              "⭑ mimetype İLK GİRDİ ve sıkıştırılmamış ⭑ (EPUB kuralı)")
    rep.check(z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED,
              "mimetype STORED")
    for need in ("META-INF/container.xml", "OEBPS/content.opf",
                 "OEBPS/nav.xhtml", "OEBPS/cover.jpg"):
        rep.check(need in names, "%s var" % need)

    opf = z.read("OEBPS/content.opf").decode("utf-8")
    rep.check('properties="cover-image"' in opf, "kapak görseli işaretli")
    rep.check("<dc:language>en</dc:language>" in opf, "dil = en")
    rep.check(info["coverPx"][1] >= 1000,
              "kapak uzun kenar ≥1000 px (%d)" % info["coverPx"][1])
    rep.check(abs(info["coverPx"][1] / info["coverPx"][0] - 1.6) < 0.01,
              "⭑ KAPAK 1,6:1 (KDP önerisi) ⭑ — sarmal DEĞİL, yalnızca ön")

    xh = [n for n in names if n.endswith(".xhtml")]
    rep.check(len(xh) >= 10, "%d bölüm dosyası" % len(xh))
    import xml.etree.ElementTree as ET
    bad = []
    for n in xh + ["OEBPS/content.opf", "META-INF/container.xml"]:
        try:
            ET.fromstring(z.read(n))
        except ET.ParseError as exc:
            bad.append("%s: %s" % (n, str(exc)[:60]))
    rep.check(not bad, "⭑ HER XML/XHTML AYRIŞTIRILABİLİR ⭑"
              + ("" if not bad else " — ⛔ %s" % bad[:3]))

    # ⚠ Kırık iç bağ = okurun ulaşamadığı bölüm.
    hrefs = set()
    for n in xh:
        hrefs |= set(re.findall(r'href="([^"#]+)', z.read(n).decode("utf-8")))
    inside = {n.split("/")[-1] for n in names}
    broken = sorted(h for h in hrefs if h.split("/")[-1] not in inside)
    rep.check(not broken, "her iç bağ çözülüyor"
              + ("" if not broken else " — ⛔ %s" % broken[:4]))

    # ⚠ BASKIYA AİT HİÇBİR ŞEY: sırt, barkod, taşma, kırım.
    blob = " ".join(z.read(n).decode("utf-8", "ignore") for n in xh).lower()
    print_only = [w for w in ("spine", "barcode", "bleed", "trim size",
                              "gutter") if w in blob]
    rep.check(not print_only, "baskıya özel terim yok"
              + ("" if not print_only else " — ⛔ %s" % print_only))

    rep.check(info["metaWithheld"] == ["meta-001"],
              "⭑ SON SORUNUN CEVABI KINDLE'DA DA BASILMADI ⭑ (%s)"
              % (info["metaWithheld"] or "⛔ BASILDI"))
    rep.check(info["solutionsTypeset"] == 100,
              "100 çözüm (meta hariç) — %d" % info["solutionsTypeset"])
    rep.check(info["hintsTypeset"] >= 300,
              "303 ipucu — %d" % info["hintsTypeset"])
    rep.check("About this digital edition" in
              z.read("OEBPS/copyright.xhtml").decode("utf-8"),
              "⭑ ALICI BİLGİLENDİRMESİ PAKETTE ⭑ (§ 9)")

    rep.facts.update({k: v for k, v in info.items() if k != "epub"})
    rep.facts["epub"] = os.path.relpath(info["epub"], pl.ROOT)
    rep.facts["buyerNote"] = KINDLE_NOTE_EN
    return rep.finish("%d bölüm · %d levha · %.1f MB"
                      % (info["docs"], info["images"],
                         info["bytes"] / 1e6), STATS)


if __name__ == "__main__":
    sys.exit(main())
