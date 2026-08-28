#!/usr/bin/env python3
"""
KDP DÖNÜŞÜM KAPISI — AMAZON'UN GERÇEK REDDİNDEN DOĞDU
================================================================================
⭑ 28 Ağustos 2026 · KDP kitabı REDDETTİ ⭑

    Cover:   "The front cover contains text/graphics that extend beyond
              the trim line... at least 0.716in (18.175mm) away from the
              outside edges. All front cover text must also stop at least
              0.4in (10mm) away from the edge of the spine."

    Interior: "Fix all conversion errors in the text and images...
              question marks or boxes in the place of text, or boxes with
              an 'X' inside where images should be. See examples on PDF
              page(s) 135."

⚠ VE YEREL KAPILARIN HEPSİ YEŞİLDİ. Sebep basit: hiçbiri BU SORULARI
sormuyordu. `covers.py` yalnızca KARŞITLIK ölçüyordu — yazının OKUNUR
olduğunu doğruluyor, SAYFADA KALDIĞINI hiç sormuyordu. `interior.py`
çerçeveyi kuruyor ama gömülmeyen bir yazı tipini fark etmiyordu.

Bu kapı üç kök sebebi ölçer:

  ① GÖMÜLMEYEN YAZI TİPİ — `Helvetica` reportlab kanvasının varsayılanı
    olarak her sayfanın kaynak sözlüğüne yazılıyordu: `emb: no`. Gömülü
    olmayan tip okuyucuda İKAME EDİLİR; ikame, Amazon'un tarif ettiği
    "question marks or boxes" tablosunu üretir.

  ② EKSİK GLİF — `⚠` (U+26A0) DejaVu Sans MONO'da vardır, DejaVu
    SERIF'te YOKTUR. Gövde serif dizilir; reportlab `.notdef` çizer.
    ⚠ Ve karakter metin çıkarımından TAMAMEN DÜŞER — yani `pdftotext`
    ile bakan biri kusuru göremez. Bu yüzden denetim KAYNAK metni,
    basılacağı YÜZE karşı ölçer.

  ③ KAPAK GÜVENLİ ALANI — ölçü KESİMDEN değil DIŞ KENARDAN alınır.
    Eski `SAFE = 0.25` kesimden ölçüyordu: 0,125" taşmayla dış kenardan
    0,375" ediyordu, KDP'nin istediğinin yarısından az.

⭑ YANLIŞ POZİTİF KÖRLÜĞÜ ⭑ (yönerge § 7)
`□` (U+25A1) kitapta SEKİZ kez geçer ve hepsi YAZILMIŞ bulmaca
içeriğidir — cevap kutuları ("□ □ □"). Bir karakteri "tofu" saymak için
görüntüsü yetmez; ölçüt şudur: **basılacağı yüzde glifi VAR MI**. Varsa
o bir semboldür, kusur değil. Dedektör körleştirilmez, KESKİNLEŞTİRİLİR.

Çıkış kodları:  0 = temiz   1 = ihlal   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "08_OUTPUT")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "qa-kdp-conversion.json")

# Gerçekten hatalı olan karakterler — bunlar hiçbir bağlamda içerik değildir.
ERROR_CHARS = {
    "�": "REPLACEMENT CHARACTER",
    "￼": "OBJECT REPLACEMENT CHARACTER",
    "⍰": "APL FUNCTIONAL SYMBOL QUAD QUESTION",
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FACES = {"Body": "DejaVuSerif.ttf", "Body-B": "DejaVuSerif-Bold.ttf",
         "Body-I": "DejaVuSerif-Italic.ttf", "Mono": "DejaVuSansMono.ttf"}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=kw.pop("timeout", 900), **kw)


def source_strings():
    """Kitabın gerçekten BASILAN dizeleri.

    ⚠ DEDEKTÖR KESKİNLEŞTİRİLİR, KÖRLEŞTİRİLMEZ (yönerge § 7·§ 13).
    `toolsPlate` içindeki `printed: false` çizelge — son sorunun ADAY
    LİSTESİ — bir İSPAT YÜZEYİDİR ve kitaba hiç girmez; notundaki `⚠`
    hiçbir zaman bir serif yüze düşmez. Onu saymak, var olmayan bir
    kusuru üretimi durdurmak için kullanmak olurdu.
    ⚠ Ama kural DAR tutulur: yalnızca AÇIKÇA `printed: false` işaretli
    çizelgeler atlanır. "Muhtemelen basılmaz" diye bir muafiyet yoktur.
    """
    out, skipped = [], []

    def walk(o):
        if isinstance(o, str):
            out.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                walk(v)

    p = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
    if os.path.isfile(p):
        book = json.load(open(p, encoding="utf-8"))
        charts = book.get("toolsPlate") or {}
        for key, ch in list(charts.items()):
            if isinstance(ch, dict) and ch.get("printed") is False:
                skipped.append(key)
                charts.pop(key)
        walk(book)
    if skipped:
        print("  ⊘ basılmayan çizelge atlandı: %s" % ", ".join(skipped))
    return out


def glyph_audit(rep):
    """⭑ KAYNAK METİN, BASILACAĞI YÜZE KARŞI ⭑"""
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        rep.warn("reportlab yok — glif denetimi atlandı")
        return {}
    faces = {}
    for n, f in FACES.items():
        path = os.path.join(FONT_DIR, f)
        if not os.path.isfile(path):
            rep.warn("yazı tipi yok: %s" % path)
            return {}
        try:
            pdfmetrics.getFont(n)
        except Exception:                                   # noqa: BLE001
            pdfmetrics.registerFont(TTFont(n, path))
        faces[n] = pdfmetrics.getFont(n).face

    chars = set("".join(source_strings()))
    nonascii = sorted(c for c in chars if ord(c) > 127)
    # Gövde metni serif dizilir; şekiller mono. Bir karakter EN AZ BİR
    # yüzde bulunmalı, ve serif yüzlerde eksikse bu bir RİSKTİR çünkü
    # anlatı metni oraya düşer.
    nowhere, serif_gap = [], []
    for c in nonascii:
        if not any(faces[n].charToGlyph.get(ord(c)) for n in faces):
            nowhere.append(c)
        elif not all(faces[n].charToGlyph.get(ord(c))
                     for n in ("Body", "Body-B", "Body-I")):
            serif_gap.append(c)
    print("\n── glif kapsaması ──")
    print("  %-34s %d" % ("kaynaktaki ASCII dışı karakter", len(nonascii)))
    print("  %-34s %s" % ("hiçbir yüzde yok",
                          " ".join(nowhere) if nowhere else "—"))
    print("  %-34s %s" % ("serif yüzlerde eksik",
                          " ".join(serif_gap) if serif_gap else "—"))
    rep.check(not nowhere,
              "⭑ HER KARAKTERİN EN AZ BİR YÜZDE GLİFİ VAR ⭑"
              + ("" if not nowhere else " — ⛔ %s" % " ".join(nowhere)))
    rep.check(not serif_gap,
              "⭑ GÖVDE (SERIF) YÜZLERİ HER KARAKTERİ TAŞIYOR ⭑ — anlatı "
              "metni serif dizilir; eksik glif `.notdef` kutusu basar ve "
              "metin çıkarımından SESSİZCE düşer"
              + ("" if not serif_gap else " — ⛔ %s (U+%s)"
                 % (" ".join(serif_gap),
                    " ".join("%04X" % ord(c) for c in serif_gap))))
    return {"nonAscii": len(nonascii), "missingEverywhere": nowhere,
            "missingInSerif": serif_gap}


def interior_audit(rep, binding, sub):
    pdf = os.path.join(OUT, sub, "interior.pdf")
    if not os.path.isfile(pdf):
        rep.warn("%s iç bloğu YOK" % binding)
        return {}
    info = run(["pdfinfo", pdf]).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    txt = run(["pdftotext", "-q", pdf, "-"]).stdout

    print("\n── %s · %d sayfa ──" % (binding.upper(), pages))

    # ① yazı tipleri gömülü mü
    lines = [l for l in run(["pdffonts", pdf]).stdout.splitlines()[2:] if l.strip()]
    notemb = [l.split()[0] for l in lines if len(l.split()) >= 6
              and l.split()[-4] == "no"]
    print("  %-30s %d" % ("yazı tipi", len(lines)))
    rep.check(not notemb,
              "⭑ %s · HER YAZI TİPİ GÖMÜLÜ ⭑" % binding.upper()
              + ("" if not notemb else " — ⛔ GÖMÜLMEYEN: %s "
                 "(KDP ikame eder ve '?'/kutu basar)" % notemb))

    # ② gerçek hata karakterleri (yazılmış semboller DEĞİL)
    found = {ERROR_CHARS[c]: txt.count(c) for c in ERROR_CHARS if c in txt}
    rep.check(not found,
              "%s · ikame/hata karakteri yok" % binding
              + ("" if not found else " — ⛔ %s" % found))

    # ③ harf arasında sıkışmış '?' — ikame edilmiş glifin izi
    qs = re.findall(r"(?<=[A-Za-zÀ-ÿ])\?(?=[A-Za-zÀ-ÿ])", txt)
    rep.check(not qs,
              "%s · sözcük içinde '?' yok (%d)" % (binding, len(qs)))

    # ④ görseller
    il = [l for l in run(["pdfimages", "-list", pdf]).stdout.splitlines()[2:]
          if l.strip()]
    zero = [l for l in il if re.search(r"\s0\s+0\s", l)]
    print("  %-30s %d" % ("gömülü görsel", len(il)))
    rep.check(not zero, "%s · sıfır boyutlu görsel yok" % binding)
    rep.check(len(il) > 0, "%s · görseller gömülü (%d)" % (binding, len(il)))
    return {"pages": pages, "fonts": len(lines), "notEmbedded": notemb,
            "images": len(il), "errorChars": found,
            "innerQuestionMarks": len(qs)}


def cover_audit(rep, binding, sub, stats_name):
    """⭑ NİHAİ PDF'TE ÖLÇÜLÜR ⭑ — 'guide'ların içinde duruyor gibi' değil."""
    pdf = os.path.join(OUT, sub, "cover.pdf")
    st = (pl.load_json(os.path.join(pl.ROOT, "06_REPORTS", "tracked",
                                    stats_name)) or {}).get("facts") or {}
    sa = st.get("safeArea")
    if not os.path.isfile(pdf) or not sa:
        rep.warn("%s kapağı ya da güvenli alan kaydı YOK" % binding)
        return {}
    out = run(["pdftotext", "-bbox", "-q", pdf, "-"]).stdout
    m = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', out)
    if not m:
        rep.warn("%s kapağında metin katmanı bulunamadı" % binding)
        return {}
    W, H = float(m.group(1)) / 72.0, float(m.group(2)) / 72.0
    words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" '
                       r'xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', out)
    emin, smin = sa["edgeMinIn"], sa["spineMinIn"]
    fse, sle = sa["frontSpineEdgeIn"], sa["spineLeftEdgeIn"]
    worst, bad = (99.0, None), []
    for xmn, ymn, xmx, ymx, t in words:
        x0, x1 = float(xmn) / 72.0, float(xmx) / 72.0
        y1, y0 = H - float(ymn) / 72.0, H - float(ymx) / 72.0
        if x0 >= fse:                       # ön kapak
            gaps = [x0 - (fse + smin), (W - x1) - emin]
        elif x1 <= sle:                     # arka kapak
            gaps = [x0 - emin, (sle - smin) - x1]
        else:
            continue                        # sırt: hesaplayıcının alanı
        gaps += [y0 - emin, (H - y1) - emin]
        g = min(gaps)
        if g < worst[0]:
            worst = (g, t)
        if g < -0.002:
            bad.append((t, round(g, 3)))
    print("\n── %s kapağı ── (%.3f × %.3f in · %d sözcük)"
          % (binding.upper(), W, H, len(words)))
    print("  %-30s %.3f in" % ("dış kenar asgarisi (KDP)", emin))
    print("  %-30s %.3f in" % ("sırt asgarisi (KDP)", smin))
    print("  %-30s %+.3f in (%s)" % ("en dar ölçülen pay", worst[0], worst[1]))
    rep.check(not bad,
              "⭑ %s KAPAĞI · NİHAİ PDF'TE HER SÖZCÜK GÜVENLİ ALANDA ⭑"
              % binding.upper()
              + ("" if not bad else " — ⛔ %d sözcük taşıyor: %s"
                 % (len(bad), bad[:4])))
    return {"widthIn": round(W, 4), "heightIn": round(H, 4),
            "words": len(words), "edgeMinIn": emin, "spineMinIn": smin,
            "tightestIn": round(worst[0], 4), "tightestWord": worst[1],
            "violations": bad}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--json", default=STATS)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    for tool in ("pdffonts", "pdftotext", "pdfimages", "pdfinfo"):
        if not shutil.which(tool):
            print("ATLANDI: %s (poppler) yok" % tool)
            return 2

    print("=" * 74)
    print("  KDP DÖNÜŞÜM KAPISI · Amazon'un reddettiği üç şey")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    facts = {"glyphs": glyph_audit(rep)}
    for b, s in (("paperback", "PAPERBACK"), ("hardcover", "HARDCOVER")):
        facts[b] = interior_audit(rep, b, s)
    facts["coverPaperback"] = cover_audit(rep, "paperback", "PAPERBACK",
                                          "cover.json")
    facts["coverHardcover"] = cover_audit(rep, "hardcover", "HARDCOVER",
                                          "cover-hardcover.json")
    rep.facts.update(facts)
    return rep.finish("KDP dönüşümü", args.json)


if __name__ == "__main__":
    sys.exit(main())
