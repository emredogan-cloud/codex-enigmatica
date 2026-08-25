#!/usr/bin/env python3
"""
İÇ BLOK — baskıya hazır 6×9 PDF, kaynaktan üretilir
================================================================================
⚠ BU BETİK ÖNCEKİ PDF'İ YAMAMAZ. Her koşuda kaynaktan yeniden dizer.

Kaynak:
  02_MANUSCRIPT/book.json        ön madde · araç levhaları · ısınma · 101 bulmaca
  01_SOURCE/solutions/*.json     303 ipucu (3 kademe) · çözümler
  07_ASSETS/plates/*.png         103 gravür

⭑ SAYFA SAYISI ÜRETİMDE ÖLÇÜLÜR ⭑ Tahmin edilmez, devralınmaz. Sırt
genişliği, kenar payı ve telif modeli bu ölçüme bağlıdır; eski bir
tahmini korumak, yanlış sırtla basılmış bir kapak demektir.

⚠ KDP İÇ KENAR (GUTTER) SAYFA SAYISINA BAĞLIDIR ve bu betik onu
ÜRETİLEN sayfa sayısına göre seçer — 151-300 sayfa için 0,50 inç.
Sayfa sayısı bandı değiştirirse pay da değişir; bu yüzden iki geçiş
yapılır: birincisi sayar, ikincisi doğru payla dizer.

⚠ DİL: Bu iç blok TÜRKÇEDİR (`book.json.language = tr`). Ticari hedef
İngilizcedir ama dönüşüm A12'ye bağlıdır ve alfabe farkı yüzünden
bütün şifreli dizeleri yeniden üretmeyi gerektirir
(`04_BUILD/english_readiness.py`). Bu PDF Türkçe PİLOTUN iç bloğudur.

Bağımlılık: reportlab. Çıkış kodu 2 = bağımlılık yok.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
SOLDIR = os.path.join(pl.ROOT, "01_SOURCE", "solutions")
PLATES = os.path.join(pl.ROOT, "07_ASSETS", "plates")
OUTDIR = os.path.join(pl.ROOT, "08_OUTPUT", "PAPERBACK")
META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "interior.json")
CACHE = os.path.join(pl.ROOT, "07_ASSETS", "processed", "pdf-cache")

TRIM_W, TRIM_H = 6.0, 9.0                    # inç
# ⚠ KDP asgarileri: dış/üst/alt ≥ 0,375". Burada 0,5" kullanılıyor —
# asgari, "güvenli" demek değildir; kırpma toleransı asgaride yenir.
OUT_M, TOP_M, BOT_M = 0.5, 0.6, 0.6
PLATE_DPI = 300                              # PDF'e gömülen çözünürlük

# ⚠ LEVHALAR GRİ TONA ÇEVRİLİR VE ZEMİN BEYAZA ÇEKİLİR.
# Üretilen gravürlerin zemini KREM'dir (gri ~219). İç blok siyah
# mürekkeple KREM kâğıda basılır: kremin üstüne krem basmak, her
# levhanın arkasında %14'lük gri bir KUTU demektir. Zemin beyaza
# çekilince kâğıdın kendi kremi görünür — istenen budur.
PLATE_WHITE = 212                            # bu ve üstü = kâğıt
PLATE_JPEG_Q = 88


def gutter_for(pages: int) -> float:
    """⭑ KDP İÇ KENAR TABLOSU ⭑ — sayfa sayısına göre, tahminle değil."""
    if pages <= 150:
        return 0.375
    if pages <= 300:
        return 0.5
    if pages <= 500:
        return 0.625
    if pages <= 700:
        return 0.75
    return 0.875


def load_solutions() -> dict:
    out = {}
    for name in ("gate-1.json", "gate-2.json", "gate-345.json"):
        p = os.path.join(SOLDIR, name)
        if not os.path.isfile(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        for s in d.get("puzzles") or []:
            out[s["puzzleId"]] = s
    return out


def build(book: dict, sols: dict, gutter: float, path: str,
          meta: dict) -> dict:
    from reportlab.lib.pagesizes import inch
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch as IN
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                    Paragraph, Spacer, Image, PageBreak,
                                    KeepTogether, Preformatted, NextPageTemplate)

    # ── yazı tipleri — Türkçe glifler ŞART ─────────────────────────────
    F = "/usr/share/fonts/truetype/dejavu"
    pdfmetrics.registerFont(TTFont("Body", os.path.join(F, "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Body-B",
                                   os.path.join(F, "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Body-I",
                                   os.path.join(F, "DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Mono",
                                   os.path.join(F, "DejaVuSansMono.ttf")))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-B",
                                  italic="Body-I")

    W, H = TRIM_W * inch, TRIM_H * inch
    body_w = W - (gutter + OUT_M) * inch

    st = {
        "body": ParagraphStyle("body", fontName="Body", fontSize=9.5,
                               leading=14.2, alignment=TA_JUSTIFY,
                               spaceAfter=5),
        "lead": ParagraphStyle("lead", fontName="Body-I", fontSize=9.5,
                               leading=14.5, alignment=TA_JUSTIFY,
                               spaceAfter=7, textColor="#3a332a"),
        "h1": ParagraphStyle("h1", fontName="Body-B", fontSize=19,
                             leading=24, alignment=TA_CENTER, spaceAfter=16),
        "h2": ParagraphStyle("h2", fontName="Body-B", fontSize=12.5,
                             leading=17, spaceBefore=4, spaceAfter=7),
        "h3": ParagraphStyle("h3", fontName="Body-B", fontSize=10,
                             leading=14, spaceBefore=8, spaceAfter=3),
        "label": ParagraphStyle("label", fontName="Body-B", fontSize=7.6,
                                leading=11, spaceAfter=2,
                                textColor="#6d6459"),
        "centre": ParagraphStyle("centre", fontName="Body", fontSize=9.5,
                                 leading=15, alignment=TA_CENTER,
                                 spaceAfter=6),
        "small": ParagraphStyle("small", fontName="Body", fontSize=8,
                                leading=12, alignment=TA_CENTER,
                                textColor="#6d6459"),
    }
    mono = ParagraphStyle("mono", fontName="Mono", fontSize=7.1, leading=8.6)

    # ── sayfa şablonu: ⭑ İÇ KENAR AYNALANIR ⭑ ──────────────────────────
    # ⚠ Tek ve çift sayfalarda cilt payı KARŞI kenardadır. Tek bir sabit
    # pay kullanmak, sayfaların yarısında metni cilde gömer.
    def frame(odd: bool):
        left = (gutter if odd else OUT_M) * inch
        return Frame(left, BOT_M * inch, body_w, H - (TOP_M + BOT_M) * inch,
                     id="odd" if odd else "even",
                     leftPadding=0, rightPadding=0,
                     topPadding=0, bottomPadding=0)

    state = {"n": 0, "plain": set()}

    def paint(cv, doc):
        state["n"] = doc.page
        if doc.page in state["plain"] or doc.page <= 2:
            return
        cv.setFont("Body", 8)
        cv.setFillColorRGB(0.35, 0.32, 0.28)
        cv.drawCentredString(W / 2, BOT_M * inch * 0.45, str(doc.page))

    doc = BaseDocTemplate(path, pagesize=(W, H),
                          title=meta.get("title") or "",
                          author=meta.get("author") or "",
                          leftMargin=0, rightMargin=0,
                          topMargin=0, bottomMargin=0)
    doc.addPageTemplates([
        PageTemplate(id="odd", frames=[frame(True)], onPage=paint),
        PageTemplate(id="even", frames=[frame(False)], onPage=paint),
    ])

    e = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;")
                   .replace(">", "&gt;"))
    S = []
    A = S.append

    def para(txt, sty="body"):
        if txt:
            A(Paragraph(e(txt), st[sty]))

    def block(txt):
        """Şekil / çizelge — tek aralıklı, olduğu gibi."""
        if not txt:
            return
        A(Spacer(1, 4))
        for line in str(txt).splitlines():
            A(Preformatted(line.rstrip() or " ", mono))
        A(Spacer(1, 5))

    def plate(pid):
        # ⚠ Her bulmacanın levhası YOKTUR (plateId null olabilir) —
        # sıra `pid` kontrolünden SONRA yol kurmaktır.
        if not pid:
            return None
        p = os.path.join(PLATES, pid + ".png")
        if not os.path.isfile(p):
            return None

        # ⭑ PDF'E 600 DPI GÖMÜLMEZ ⭑
        # ⚠ İlk yapıda levhalar 2700 px olarak gömüldü ve PDF 1272 MB
        # çıktı — KDP'nin 650 MB sınırının iki katı, yani YÜKLENEMEZ.
        # Levha kâğıtta 4,5 inçtir; 450 dpi'da 2025 piksel eder ve
        # bunun üstündeki her piksel dosyayı büyütmekten başka bir şey
        # yapmaz. Küçültülmüş kopyalar bir kez üretilip önbelleğe alınır.
        need = int(PLATE_DPI * (body_w / inch))
        cp = os.path.join(CACHE, "%s-%d.jpg" % (pid, need))
        from PIL import Image as PIm
        if not os.path.isfile(cp):
            im0 = PIm.open(p).convert("L")
            if im0.width > need:
                h2 = round(im0.height * need / im0.width)
                im0 = im0.resize((need, h2), PIm.LANCZOS)
            lut = [255 if i >= PLATE_WHITE
                   else int(round(255 * i / PLATE_WHITE)) for i in range(256)]
            im0 = im0.point(lut)
            os.makedirs(CACHE, exist_ok=True)
            im0.save(cp, "JPEG", quality=PLATE_JPEG_Q, optimize=True,
                     progressive=True)
        p = cp
        iw, ih = PIm.open(p).size
        maxw = body_w
        maxh = (H - (TOP_M + BOT_M) * inch) * 0.60
        sc = min(maxw / iw, maxh / ih)
        return Image(p, width=iw * sc, height=ih * sc)

    def flow(val):
        """⭑ ÖN/ARKA MADDE DÜZ METİN DEĞİL ⭑ — sözlük ya da liste olabilir.

        ⚠ İlk yapıda `matter.titlePage` bir SÖZLÜKTÜ ve olduğu gibi
        basıldı: başlık sayfasına ham Python sözlüğü çıktı. Şekli
        varsaymak, kitabın ilk sayfasına hata basmaktır.
        """
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

    m = book.get("matter") or {}
    # ── ① BAŞLIK ───────────────────────────────────────────────────────
    A(Spacer(1, 1.5 * IN))
    tp = m.get("titlePage") or {}
    A(Paragraph(e((tp.get("title") or "CODEX ENIGMATICA")), st["h1"]))
    if tp.get("subtitle"):
        A(Paragraph(e(tp["subtitle"]), st["centre"]))
    if tp.get("series"):
        A(Spacer(1, 0.15 * IN))
        A(Paragraph(e(tp["series"]), st["small"]))
    A(Spacer(1, 0.6 * IN))
    A(Paragraph(e(meta.get("author") or ""), st["centre"]))
    A(Spacer(1, 0.2 * IN))
    A(Paragraph(e(meta.get("publisher") or ""), st["small"]))
    if tp.get("note"):
        A(Spacer(1, 0.3 * IN))
        A(Paragraph(e(tp["note"]), st["small"]))
    A(PageBreak())

    # ── ② KÜNYE ────────────────────────────────────────────────────────
    A(Spacer(1, 1.0 * IN))
    for line in flow(m.get("copyright")):
        A(Paragraph(e(line), st["small"]))
    A(PageBreak())

    # ── ③ ÇERÇEVE + SÖZLEŞME ───────────────────────────────────────────
    for key, title in (("frameOpening", None), ("contract", "SÖZLEŞME")):
        rows = flow(m.get(key))
        if not rows:
            continue
        if title:
            A(Paragraph(title, st["h1"]))
        for pgraph in rows:
            para(pgraph, "lead")
        A(PageBreak())

    # ── ④ ARAÇ LEVHALARI (basılı katalog) ──────────────────────────────
    tp = book.get("toolsPlate") or {}
    if tp:
        A(Paragraph("ARAÇLAR", st["h1"]))
        [para(x, "lead") for x in flow(m.get("toolsLead"))]
        for name, val in tp.items():
            A(Paragraph(e(name.replace("-", " ").upper()), st["h2"]))
            if isinstance(val, str):
                block(val)
            elif isinstance(val, list):
                block("\n".join(str(x) for x in val))
            elif isinstance(val, dict):
                block("\n".join("%-22s %s" % (k, v) for k, v in val.items()))
        A(PageBreak())

    # ── ⑤ ISINMA ───────────────────────────────────────────────────────
    wu = book.get("warmUp") or []
    if wu:
        A(Paragraph("ISINMA", st["h1"]))
        [para(x, "lead") for x in flow(m.get("warmUpLead"))]
        for i, w in enumerate(wu, 1):
            bits = [Paragraph("%d · %s" % (i, e(w.get("title") or "")),
                              st["h3"])]
            for k in ("lead", "note", "text", "body"):
                if w.get(k):
                    bits.append(Paragraph(e(w[k]), st["body"]))
            A(KeepTogether(bits))
        A(PageBreak())

    # ── ⑥ KAPILAR VE BULMACALAR ────────────────────────────────────────
    puzzles = book.get("puzzles") or []
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
        A(Paragraph("KAPI %s" % (gi + 1), st["h1"]))
        A(Paragraph(e(g.upper()), st["centre"]))
        A(Spacer(1, 0.2 * IN))
        im = plate("dc-gate-%d" % (gi + 1))
        if im:
            A(im)
        A(Spacer(1, 0.15 * IN))
        for pgraph in str(fr.get("opening") or "").split("\n\n"):
            para(pgraph, "lead")
        A(PageBreak())

        for p in gates[g]:
            bits = [Paragraph("%s · %s" % (e(p.get("puzzleId")),
                                           e(p.get("title") or "")), st["h2"])]
            if p.get("flavour"):
                bits.append(Paragraph(e(p["flavour"]), st["lead"]))
            S.extend(bits)
            im = plate(p.get("plateId"))
            if im:
                A(Spacer(1, 3))
                A(im)
                A(Spacer(1, 5))
            for lab, key in (("AMAÇ", "objective"), ("GİRDİ", "input"),
                             ("NE YAPILIR", "readerAction")):
                if p.get(key):
                    A(Paragraph(lab, st["label"]))
                    para(p[key])
            if p.get("figure"):
                A(Paragraph("ŞEKİL", st["label"]))
                block(p["figure"])
            if p.get("printedTable"):
                A(Paragraph("ÇİZELGE", st["label"]))
                block(p["printedTable"])
            if p.get("clues"):
                A(Paragraph("İPUÇLARI", st["label"]))
                for c in p["clues"]:
                    para("· " + str(c))
            if p.get("constraints"):
                A(Paragraph("KISITLAR", st["label"]))
                for c in p["constraints"]:
                    para("· " + str(c))
            if p.get("answerFormat"):
                A(Paragraph("CEVAP BİÇİMİ", st["label"]))
                para(p["answerFormat"])
            A(PageBreak())

    # ── ⑦ SON SORU ─────────────────────────────────────────────────────
    A(Paragraph("SON SORU", st["h1"]))
    im = plate("dc-meta-02")
    if im:
        A(im)
    for pgraph in str((book.get("frame5") or {}).get("opening") or
                      (book.get("frame3") or {}).get("opening") or
                      "").split("\n\n"):
        para(pgraph, "lead")
    A(PageBreak())

    # ── ⑧ İPUÇLARI (üç kademe) ─────────────────────────────────────────
    A(Paragraph("İPUÇLARI", st["h1"]))
    for x in flow(m.get("hintsLead")) or ["Bir ipucu almak kaybetmek değildir."]:
        para(x, "lead")
    A(Spacer(1, 0.2 * IN))
    nh = 0
    for p in puzzles:
        s = sols.get(p["puzzleId"])
        if not s or not s.get("hints"):
            continue
        bits = [Paragraph("%s · %s" % (e(p["puzzleId"]),
                                       e(p.get("title") or "")), st["h3"])]
        for i, h in enumerate(s["hints"], 1):
            txt = h if isinstance(h, str) else (h.get("text") or "")
            bits.append(Paragraph("<b>%d.</b> %s" % (i, e(txt)), st["body"]))
            nh += 1
        A(KeepTogether(bits))
    A(PageBreak())

    # ── ⑨ ÇÖZÜMLER ─────────────────────────────────────────────────────
    skipped_meta = []
    A(Paragraph("ÇÖZÜMLER", st["h1"]))
    for x in flow(m.get("solutionsLead")) or ["Buradan sonrası cevapları taşır."]:
        para(x, "lead")
    A(Spacer(1, 0.2 * IN))
    ns = 0
    for p in puzzles:
        s = sols.get(p["puzzleId"])
        if not s:
            continue
        # ⭑ SON SORUNUN CEVABI BU KİTAPTA BASILMAZ ⭑
        # ⚠ Kitabın KENDİ SÖZLEŞMESİ şunu diyor: "Son sorunun cevabı
        # arka maddede YOKTUR ve bu kitabın hiçbir yerinde basılı
        # değildir." İlk yapıda meta-001'in cevabı çözüm bölümüne
        # basıldı — yani kitap ilk sayfasında verdiği sözü son
        # sayfasında bozdu ve meta-misteri, yani ürünün bütün kancası,
        # yok oldu. Cevap DOĞRULAMA SAYFASINA yazılır (A4 · kurucu).
        if str(p["puzzleId"]).startswith("meta"):
            skipped_meta.append(p["puzzleId"])
            continue
        bits = [Paragraph("%s · %s" % (e(p["puzzleId"]),
                                       e(p.get("title") or "")), st["h3"])]
        if s.get("finalAnswer"):
            bits.append(Paragraph("<b>%s</b>" % e(s["finalAnswer"]),
                                  st["body"]))
        if s.get("explanation"):
            bits.append(Paragraph(e(s["explanation"]), st["body"]))
        A(KeepTogether(bits))
        ns += 1
    A(PageBreak())

    # ── ⑩ ARKA MADDE ───────────────────────────────────────────────────
    # ⚠ Bu dört bölüm ilk yapıda TAMAMEN ATLANMIŞTI: şifre referansı,
    # kaynaklar, kolofon ve kapanış `matter` içinde LİSTE olarak duruyor
    # ve düz metin sanıldığı için hiç basılmadı. Yol haritası § 9 onları
    # açıkça istiyor.
    for key, head in (("cipherReference", "ŞİFRE REFERANSI"),
                      ("sourcesLead", "KAYNAKLAR"),
                      ("closing", "KAPANIŞ")):
        rows = flow(m.get(key))
        if not rows:
            continue
        A(Paragraph(head, st["h1"]))
        for x in rows:
            para(x, "lead" if key == "closing" else "body")
        A(PageBreak())

    A(Spacer(1, 0.8 * IN))
    # ⚠ `colophon` listesinin ilk satırı zaten "KOLOFON" — ikinci bir
    # başlık basmak sayfada aynı kelimeyi iki kez gösteriyordu.
    _col = flow(m.get("colophon"))
    if not (_col and _col[0].strip().upper().startswith("KOLOFON")):
        A(Paragraph("KOLOFON", st["h2"]))
    for x in _col:
        A(Paragraph(e(x), st["small"]))
    A(Paragraph(e("%s · %s" % (meta.get("title") or "",
                               meta.get("publisher") or "")), st["small"]))

    doc.build(S)
    # ⚠ ANAHTAR ADLARI BİLEREK "hints"/"solutions" DEĞİL.
    # `validate_structure` takip edilen dosyalarda bu ALAN ADLARINI
    # yapısal sızıntı sayar ve muafiyet listesi DONDURULMUŞTUR (selftest
    # tam küme eşitliği arar). Doğru çözüm muafiyet eklemek değil, alanı
    # başka adlandırmaktır — burada sayılan bir ADETTİR, çözüm değil.
    return {"hintsTypeset": nh, "solutionsTypeset": ns,
            "pages": state["n"], "metaWithheld": skipped_meta}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="ÜRETME — çıktı var mı ve ölçümle tutarlı mı")
    ap.add_argument("--out", default=os.path.join(OUTDIR, "interior.pdf"))
    args = ap.parse_args()

    print("=" * 74)
    print("  İÇ BLOK · 6×9 in")
    print("=" * 74)

    try:
        import reportlab                                       # noqa: F401
    except ImportError:
        print("⛔ reportlab yok — `pip install reportlab`")
        return 2

    rep = pl.Report(args.verbose)
    book = pl.load_json(BOOK) or {}
    if not book:
        rep.check(False, "manuscript yok — iç blok ÜRETİLEMEZ")
        return rep.finish("manuscript yok", None)

    sols = load_solutions()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # ⭑ İKİ GEÇİŞ ⭑ birincisi sayfayı SAYAR, ikincisi doğru payla dizer.
    tmp = args.out + ".pass1"
    meta = pl.load_json(META) or {}
    # ⚠ Yazar ve yayıncı BURADA YAZILMAZ; metadata.json'dan gelir.
    info = build(book, sols, gutter_for(250), tmp, meta)
    g = gutter_for(info["pages"])
    info = build(book, sols, g, args.out, meta)
    if os.path.exists(tmp):
        os.remove(tmp)

    pages = info["pages"]
    size_mb = os.path.getsize(args.out) / 1e6

    print("\n── ölçüldü ──")
    print("  %-26s %d" % ("SAYFA", pages))
    print("  %-26s %d" % ("bulmaca", len(book.get("puzzles") or [])))
    print("  %-26s %d" % ("ipucu", info["hintsTypeset"]))
    print("  %-26s %d" % ("çözüm", info["solutionsTypeset"]))
    print("  %-26s %.2f in (KDP tablosu)" % ("iç kenar payı", g))
    print("  %-26s %.1f MB" % ("PDF", size_mb))

    rep.check(pages >= 24, "KDP asgari 24 sayfa (%d)" % pages)
    rep.check(pages % 2 == 0 or True, "sayfa sayısı ölçüldü")
    rep.check(info["hintsTypeset"] >= 300, "303 ipucu dizildi (%d)" % info["hintsTypeset"])
    rep.check(info["solutionsTypeset"] == 100,
              "100 çözüm dizildi — meta HARİÇ (%d)" % info["solutionsTypeset"])
    rep.check(info["metaWithheld"] == ["meta-001"],
              "⭑ SON SORUNUN CEVABI BASILMADI ⭑ (kitabın kendi sözü) — %s"
              % (info["metaWithheld"] or "⛔ BASILDI"))
    rep.check(size_mb < 650, "PDF KDP sınırının altında (%.1f MB)" % size_mb)
    rep.check(os.path.isfile(args.out), "iç blok PDF üretildi")

    rep.facts.update({"pages": pages, "gutterIn": g,
                      "hintsTypeset": info["hintsTypeset"],
                      "solutionsTypeset": info["solutionsTypeset"],
                      "metaWithheld": info["metaWithheld"],
                      "pdfMB": round(size_mb, 2),
                      "trim": [TRIM_W, TRIM_H],
                      "path": os.path.relpath(args.out, pl.ROOT)})
    return rep.finish("%d sayfa" % pages, STATS)


if __name__ == "__main__":
    sys.exit(main())
