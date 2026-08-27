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
import re
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

# ⭑ KDP BASKI GÜVENLİ ALANI — ÖLÇÜLEN ASGARİLER ⭑
# İç (oluk) payı sayfa sayısına göre değişir (§ gutter_for); dış/üst/alt
# için KDP asgarisi 0,25"dir.
KDP_MIN_OUTER = 0.25

# ⭑ VE ASGARİYE DAYAMAK, ASGARİYİ AŞMAKTIR ⭑
# ⚠ BU SAYI BİR KDP REDDİNDEN DOĞDU. İç blok tam 0,5" oluk payıyla
# diziliyordu ve KDP Previewer "Insufficient gutter" dedi. Ölçüm sebebi
# gösterdi: DİZGİ ÇERÇEVEYİ TAŞIRIYOR. reportlab akış nesnelerini
# KIRPMAZ; yaslanmış (justify) bir satırın son glifi kendi ilerleme
# genişliğinin 0,007–0,020" ötesine taşar (italik ve tırnak en kötüsü).
# Çerçeve 0,500"de bitse bile MÜREKKEP 0,480"e kadar geliyordu.
#
# 274 sayfalık ciltsizde 274 sayfanın 140'ı bu yüzden ihlaldeydi.
# Asgariye dayanmak, toleransı sıfıra indirmektir; pay eklenir.
SAFETY_IN = 0.125

# ⚠ DIŞ PAY DARALTILIR — VE BU BİLEREK BÖYLEDİR.
# Oluk payına 0,125" eklenirken dış paydan aynı miktar alınır: gövde
# genişliği DEĞİŞMEZ (ciltsiz 5,000" · ciltli 4,875"), yani dizgi
# birebir aynı akar ve SAYFA SAYISI KORUNUR (274). Sayfa sayısı
# değişseydi sırt genişliği değişir, kapak yeniden üretilirdi.
# 0,375" hâlâ KDP asgarisinin (0,25") 0,125" üstündedir.
OUT_M, TOP_M, BOT_M = 0.375, 0.6, 0.6

# Sayfa numarasının taban çizgisi (kesim kenarından). Eskiden
# BOT_M*0,45 = 0,270" idi — KDP'nin 0,25" asgarisine 0,020" kalıyordu.
FOLIO_Y = 0.38
PLATE_DPI = 300                              # PDF'e gömülen çözünürlük

# ⚠ LEVHALAR GRİ TONA ÇEVRİLİR VE ZEMİN BEYAZA ÇEKİLİR.
# Üretilen gravürlerin zemini KREM'dir (gri ~219). İç blok siyah
# mürekkeple KREM kâğıda basılır: kremin üstüne krem basmak, her
# levhanın arkasında %14'lük gri bir KUTU demektir. Zemin beyaza
# çekilince kâğıdın kendi kremi görünür — istenen budur.
PLATE_WHITE = 212                            # bu ve üstü = kâğıt
PLATE_JPEG_Q = 88


def gutter_for(pages: int, binding: str = "paperback") -> float:
    """⭑ KDP İÇ KENAR TABLOSU ⭑ — sayfa sayısına VE cilde göre.

    ⚠ CİLTLİ DAHA GENİŞ PAY İSTER. Ciltsizin payını ciltliye vermek,
    metnin oluğa gömülmesidir: ciltli kitap düz açılmaz ve cilde
    yakın duran satırlar görünmez. Yönerge § 12 bunu açıkça yasaklıyor
    ("Do NOT copy paperback spine geometry").
    """
    if binding == "hardcover":
        if pages <= 150:
            base = 0.5
        elif pages <= 300:
            base = 0.625
        elif pages <= 500:
            base = 0.75
        else:
            base = 0.875
    elif pages <= 150:
        base = 0.375
    elif pages <= 300:
        base = 0.5
    elif pages <= 500:
        base = 0.625
    elif pages <= 700:
        base = 0.75
    else:
        base = 0.875
    # ⭑ KDP TABLOSU BİR ASGARİDİR, BİR HEDEF DEĞİL ⭑ (§ SAFETY_IN)
    return base + SAFETY_IN


def kdp_min_gutter(pages: int, binding: str = "paperback") -> float:
    """KDP'nin DENETLEDİĞİ asgari — payımız değil, onun eşiği.

    ⚠ `gutter_for` bunun ÜSTÜNE pay ekler. İkisi ayrı tutulur çünkü
    kapı, kullandığımız payı değil KDP'nin eşiğini denetlemelidir:
    payı büyütüp kapıyı da büyütmek, kapıyı kendi kendine yeşil yakar.
    """
    return gutter_for(pages, binding) - SAFETY_IN


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
          meta: dict, pad: bool = False) -> dict:
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
        cv.drawCentredString(W / 2, FOLIO_Y * inch, str(doc.page))

    # ⭑ AYNALAMA GERÇEKTEN OLMALI — VE OLMUYORDU ⭑
    # ⚠ BU, KDP REDDİNİN ASIL SEBEBİYDİ. Yukarıdaki `frame()` iki ayrı
    # şablon üretiyor ve iki şablon da KAYITLIYDI — ama hiçbir yerde
    # ARALARINDA GEÇİŞ YAPILMIYORDU. reportlab, `NextPageTemplate`
    # görmedikçe listedeki İLK şablonu bütün kitap boyunca kullanır:
    # yani oluk payı 274 sayfanın 274'ünde de SOLDA kaldı.
    #
    # Ölçüm: tek ve çift sayfaların sol kenarı BİREBİR AYNI çıkıyordu
    # (ciltli 0,620 / 0,620). Ciltside bu, çift sayfalarda oluk yerine
    # 0,5" dış pay bırakıyordu — KDP 0,625" istiyor, 245 sayfa ihlal.
    # Ciltsizde görünmüyordu, çünkü orada oluk ve dış pay eşitti (0,5).
    #
    # ⚠ Ve yorum satırı "İÇ KENAR AYNALANIR" diyordu. Kod demiyordu.
    class MirroredDoc(BaseDocTemplate):
        """Recto tek, verso çift — oluk payı her yaprakta cilde bakar."""

        def handle_pageBegin(self):
            self._handle_pageBegin()
            # Şu an başlayan sayfa `self.page`; BİR SONRAKİ sayfanın
            # şablonu şimdi seçilir.
            self._handle_nextPageTemplate(
                "odd" if (self.page + 1) % 2 == 1 else "even")

    doc = MirroredDoc(path, pagesize=(W, H),
                      title=meta.get("title") or "",
                      author=meta.get("author") or "",
                      leftMargin=0, rightMargin=0,
                      topMargin=0, bottomMargin=0)
    doc.addPageTemplates([
        PageTemplate(id="odd", frames=[frame(True)], onPage=paint),
        PageTemplate(id="even", frames=[frame(False)], onPage=paint),
    ])

    def e(s):
        """Escape for reportlab, then render the source's own emphasis.

        ⚠ THE WARM-UP WRITES ITS ANSWERS IN BOLD and the book printed the
        asterisks. The source marks emphasis the way the rest of this
        project writes it; the typesetter speaks reportlab. Shared with the
        Kindle builder — see _protected_layer § TYPESETTING.
        """
        return pl.emphasis(str(s).replace("&", "&amp;")
                           .replace("<", "&lt;").replace(">", "&gt;"))
    S = []
    A = S.append

    def para(txt, sty="body"):
        if txt:
            A(Paragraph(e(txt), st[sty]))

    def block(txt, keep=True):
        """Figure / chart — monospaced, exactly as generated.

        ⭑⭑ A PLATE'S DATA MAY NOT BREAK ACROSS A PAGE ⭑⭑
        ⚠ Each line was appended on its own, so reportlab was free to break
        a figure wherever the page ended — and it did: the ring plate of
        g2-015 put four of its seven stations on page 88 and the other
        three on page 89. The reader has to count stations on a ring; half
        a ring is not a harder puzzle, it is a broken one.

        ⚠ Charts longer than a page are the exception and must stay
        breakable — the Lexicon and the Cycle Table cannot fit on one page
        and keeping them together would overflow the frame."""
        if not txt:
            return
        lines = [Preformatted(x.rstrip() or " ", mono)
                 for x in str(txt).splitlines()]
        A(Spacer(1, 4))
        if keep and len(lines) <= 40:
            A(KeepTogether(lines))
        else:
            S.extend(lines)
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

    # ⚠ ONE IMPLEMENTATION FOR BOTH BUILDERS —
    # see _protected_layer § TYPESETTING.
    flow = pl.paragraphs

    chart_body = pl.chart_body

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
    for pgraph in flow(m.get("frameOpening")):
        para(pgraph, "lead")
    A(PageBreak())

    # ⭑⭑ THE CONTRACT IS THE ONE PAGE THAT MAY NOT BE GUESSED AT ⭑⭑
    # ⚠ It was: `flow()` walked the contract dictionary and printed every
    # value it found, so the four promises — a list of (promise,
    # explanation) PAIRS — came out as Python tuples, brackets and quotes
    # included, on the page that tells the reader what this book guarantees.
    # And the last field in that dictionary is `verificationPending`, an
    # internal note to the Founder, which was printed to the buyer as if it
    # were the verification address.
    ct = m.get("contract") or {}
    if ct:
        A(Paragraph("THE CONTRACT", st["h1"]))
        for pgraph in flow(ct.get("lead")):
            para(pgraph, "lead")
        A(Spacer(1, 0.12 * IN))
        for i, pr in enumerate(ct.get("promises") or [], 1):
            if isinstance(pr, (list, tuple)) and len(pr) == 2:
                head, body = pr
            else:
                head, body = str(pr), ""
            A(Paragraph("%d · %s" % (i, e(head)), st["h3"]))
            if body:
                para(body)
        for key in ("answerFormat", "verification"):
            rows = flow(ct.get(key))
            if not rows:
                continue
            A(Spacer(1, 0.10 * IN))
            for j, pgraph in enumerate(rows):
                para(pgraph, "h3" if j == 0 and pgraph.isupper() else "body")
        # ⚠ `verificationPending` IS NOT PRINTED. It is the Founder's open
        # item (A4), not a sentence for the reader — and a placeholder in
        # place of a real address is worse than no address at all. The
        # page-count gate and the production report both carry it as a
        # blocker instead.
        A(PageBreak())

    # ── ④ ARAÇ LEVHALARI (basılı katalog) ──────────────────────────────
    tp = book.get("toolsPlate") or {}
    if tp:
        A(Paragraph("THE TOOLS", st["h1"]))
        [para(x, "lead") for x in flow(m.get("toolsLead"))]
        for name, val in tp.items():
            if not isinstance(val, dict):
                continue
            # ⭑⭑ A CHART MARKED `printed: false` IS NOT PRINTED ⭑⭑
            # ⚠ THIS LINE CLOSES A LEAK THAT WOULD HAVE ENDED THE BOOK.
            # The last question's answer space is a chart like any other —
            # it exists so the uniqueness proof has a domain to count — and
            # it CONTAINS THE FINAL ANSWER. It carries `printed: false` and
            # every gate honours that. The interior did not: it walked the
            # whole tools plate and dumped each chart's raw dictionary, so
            # the candidate list, the final answer inside it, went onto a
            # page of the book. The contract's own words are "the last
            # question's answer is printed nowhere in this book."
            if not pl.chart_is_printed(val):
                continue
            A(Paragraph(e(val.get("title") or
                          name.replace("-", " ").title()), st["h2"]))
            if val.get("note"):
                para(val["note"], "small")
            A(Spacer(1, 4))
            block(chart_body(val), keep=False)
            A(Spacer(1, 8))
        A(PageBreak())

    # ── ⑤ ISINMA ───────────────────────────────────────────────────────
    wu = book.get("warmUp") or []
    if wu:
        A(Paragraph("WARM-UP", st["h1"]))
        [para(x, "lead") for x in flow(m.get("warmUpLead"))]
        # ⭑⭑ A SOLVED EXAMPLE THAT SHOWS NEITHER ITS FIGURE NOR ITS
        # WORKING IS NOT A SOLVED EXAMPLE ⭑⭑
        # ⚠ The first build printed only `lead` and `note` — the two fields
        # that TALK ABOUT the mechanism — and dropped `figure` and
        # `solved`, the two that SHOW it. Seventeen worked examples went
        # into the book as seventeen paragraphs of description, and the
        # front matter's promise ("they stand already solved — answers and
        # all") was not kept on a single page.
        for i, w in enumerate(wu, 1):
            A(Paragraph("%d · %s" % (i, e(w.get("title") or "")), st["h3"]))
            if w.get("lead"):
                para(w["lead"])
            if w.get("figure"):
                A(Spacer(1, 4))
                block(w["figure"])
                A(Spacer(1, 4))
            for j, line in enumerate(w.get("solved") or [], 1):
                para("%d. %s" % (j, line))
            if w.get("note"):
                A(Spacer(1, 3))
                para(w["note"], "small")
            A(Spacer(1, 10))
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
    # ⚠ THE SIXTH "GATE" IS NOT A GATE. `order` is built from the pages
    # themselves and the last question carries its own gate id, so the loop
    # asked for a sixth Roman numeral and fell over. It is not numbered —
    # it is named, and it opens with its own plate.
    ROMAN = {"threshold": "I", "menagerie": "II", "calendar": "III",
             "labyrinth": "IV", "mirror": "V"}
    NAME = {"threshold": "THE THRESHOLD", "menagerie": "THE MENAGERIE",
            "calendar": "THE CALENDAR", "labyrinth": "THE LABYRINTH",
            "mirror": "THE MIRROR", "last-question": "THE LAST QUESTION"}
    for gi, g in enumerate(order):
        last = g == "last-question"
        fr = frames[gi] if gi < len(frames) and frames[gi] else {}
        if last:
            A(Paragraph("THE LAST QUESTION", st["h1"]))
            fr = {}
        else:
            A(Paragraph("GATE %s" % ROMAN.get(g, str(gi + 1)), st["h1"]))
            A(Paragraph(e(NAME.get(g, g.upper())), st["centre"]))
        A(Spacer(1, 0.2 * IN))
        im = plate("dc-meta-01" if last else "dc-gate-%d" % (gi + 1))
        if im:
            A(im)
        A(Spacer(1, 0.15 * IN))
        for pgraph in flow(fr.get("opening")):
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
            for lab, key in (("OBJECTIVE", "objective"), ("WHAT YOU SEE", "input"),
                             ("WHAT TO DO", "readerAction")):
                if p.get(key):
                    A(Paragraph(lab, st["label"]))
                    para(p[key])
            # ⚠ THE LABEL TRAVELS WITH THE FIGURE. Keeping only the figure
            # together left "FIGURE" alone at the foot of one page and the
            # plate itself at the head of the next — the reader is told to
            # look at something that is not there.
            for lab, key in (("FIGURE", "figure"), ("CHART", "printedTable")):
                if not p.get(key):
                    continue
                lines = [Preformatted(x.rstrip() or " ", mono)
                         for x in str(p[key]).splitlines()]
                A(Spacer(1, 4))
                grp = [Paragraph(lab, st["label"])] + lines
                if len(lines) <= 38:
                    A(KeepTogether(grp))
                else:
                    S.extend(grp)
                A(Spacer(1, 5))
            if p.get("clues"):
                A(Paragraph("CLUES", st["label"]))
                for c in p["clues"]:
                    para("· " + str(c))
            if p.get("constraints"):
                A(Paragraph("CONSTRAINTS", st["label"]))
                for c in p["constraints"]:
                    para("· " + str(c))
            if p.get("answerFormat"):
                A(Paragraph("ANSWER FORM", st["label"]))
                para(p["answerFormat"])
            A(PageBreak())

    # ⚠ THE STANDALONE LAST-QUESTION SECTION WAS REMOVED. It printed the
    # heading a second time and then RE-PRINTED GATE V's opening under it,
    # so the book's most important page opened with a paragraph belonging
    # to the section before it. The last question is now rendered in the
    # loop above, in its own place, with its own plate.

    # ── ⑧ İPUÇLARI (üç kademe) ─────────────────────────────────────────
    A(Paragraph("HINTS", st["h1"]))
    for x in pl.drop_heading(flow(m.get("hintsLead")), "HINTS") \
            or ["Taking a hint is not losing."]:
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
    A(Paragraph("SOLUTIONS", st["h1"]))
    for x in pl.drop_heading(flow(m.get("solutionsLead")), "SOLUTIONS") \
            or ["Everything past this point carries answers."]:
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
    for key, head in (("cipherReference", "CIPHERS AND NOTATIONS"),
                      ("sourcesLead", "SOURCES"),
                      ("closing", "THE CLOSE")):
        rows = pl.drop_heading(flow(m.get(key)), head)
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
    if not (_col and _col[0].strip().upper().startswith("COLOPHON")):
        A(Paragraph("COLOPHON", st["h2"]))
    for x in _col:
        A(Paragraph(e(x), st["small"]))
    A(Paragraph(e("%s · %s" % (meta.get("title") or "",
                               meta.get("publisher") or "")), st["small"]))

    # ── ⑪ ⭑ THE LAST LEAF · THE VERIFICATION ADDRESS ⭑ ─────────────────
    # ⚠ THE CONTRACT PAGE PROMISES THIS LEAF BY NAME: *"You enter it on
    # the VERIFICATION PAGE, whose address is printed on the last leaf of
    # this book."* It was promised on page 11 and never printed — the
    # close then told the reader *"you know where to write it"* when the
    # reader could not possibly know. This block is that leaf, and it is
    # LAST on purpose: the final thing the book says is where the answer
    # goes.
    # ⚠ Not emitted when `verificationLeaf` is None. A leaf that says
    # "THE VERIFICATION PAGE" above an empty line is worse than no leaf,
    # and `qa_verification.py` holds `release` RED in that case anyway.
    _leaf = flow(m.get("verificationLeaf"))
    if _leaf:
        # ⚠ The address is identified by VALUE, not by indentation:
        # `pl.paragraphs` strips leading whitespace, so an indent test
        # here would silently never fire and the URL would be justified
        # into a body paragraph — the one line in the book that must not
        # be re-wrapped.
        _addr = (m.get("contract") or {}).get("verificationAddress") or ""
        A(PageBreak())
        A(Paragraph("THE VERIFICATION PAGE", st["h1"]))
        for x in pl.drop_heading(_leaf, "THE VERIFICATION PAGE"):
            if _addr and x.strip() == _addr:
                A(Spacer(1, 0.14 * IN))
                A(Paragraph("<b>%s</b>" % e(_addr), st["centre"]))
                A(Spacer(1, 0.14 * IN))
            else:
                para(x, "lead")

    # ⭑ SAYFA SAYISI ÇİFT OLMALI ⭑
    # ⚠ Basılı bir kitabın YAPRAKLARI vardır: her yaprak iki sayfadır.
    # Tek sayılı bir iç blok sonuna boş sayfa eklenerek basılır — ama o
    # sayfayı MATBAA eklerse sırt hesabı bir sayfa şaşar. Kitap kendi
    # son sayfasını kendisi koyar.
    # ⚠ `pad` KOMPOZİSYON ANINDA eklenir, build'den SONRA değil.
    # İlk denemede doc.build(S) çağrıldıktan sonra aynı S listesine
    # ekleyip yeniden inşa edilmişti — reportlab akış nesnelerini
    # TÜKETİR, bu yüzden ikinci geçiş içerik KAYBETTİ (263 → 262).
    # Doğrusu: sayfayı say, sonra hikâyeyi BAŞTAN kur.
    if pad:
        S.append(PageBreak())
        S.append(Spacer(1, 2))
    doc.build(S)
    # ⚠ ANAHTAR ADLARI BİLEREK "hints"/"solutions" DEĞİL.
    # `validate_structure` takip edilen dosyalarda bu ALAN ADLARINI
    # yapısal sızıntı sayar ve muafiyet listesi DONDURULMUŞTUR (selftest
    # tam küme eşitliği arar). Doğru çözüm muafiyet eklemek değil, alanı
    # başka adlandırmaktır — burada sayılan bir ADETTİR, çözüm değil.
    return {"hintsTypeset": nh, "solutionsTypeset": ns,
            "pages": state["n"], "metaWithheld": skipped_meta,
            "padded": pad}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="ÜRETME — çıktı var mı ve ölçümle tutarlı mı")
    ap.add_argument("--binding", default="paperback",
                    choices=("paperback", "hardcover"))
    ap.add_argument("--out", default="")
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

    # ⭑ İKİ GEÇİŞ ⭑ birincisi sayfayı SAYAR, ikincisi doğru payla dizer.
    meta = pl.load_json(META) or {}
    args.out = args.out or os.path.join(
        pl.ROOT, "08_OUTPUT", args.binding.upper(), "interior.pdf")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # ── ⭑ `--check` ÜRETMEZ ⭑ ─────────────────────────────────────────
    # ⚠⚠ BU BAYRAK BİLDİRİLMİŞTİ VE HİÇ OKUNMUYORDU. Yardım metni
    # "ÜRETME — çıktı var mı ve ölçümle tutarlı mı" diyor; betik her
    # koşuda YENİDEN ÜRETİYORDU. İki sonucu vardı ve ikincisi ürünü
    # etkiliyordu:
    #
    #   ① Bayat bir çıktıyı yakalaması BEKLENEN kapı, onu yakalamak
    #      yerine TAZELİYORDU. Yakalayamayan bir kapı, kapı değildir.
    #   ② `qa_all.sh` sırasında `kdp_package.py` SHA256 toplamlarını
    #      ÖNCE yazıyor, bu adım PDF'i SONRA yeniden üretiyordu. PDF her
    #      üretimde gömülü zaman damgası yüzünden bayt olarak değişir —
    #      yani yayın paketinin toplamları TUTMUYORDU. Ölçüldü:
    #      `sha256sum -c` ciltsizde iki dosyada FAILED verdi.
    if args.check:
        stats = pl.load_json(
            STATS if args.binding == "paperback"
            else STATS.replace("interior.json", "interior-hardcover.json")) or {}
        facts = stats.get("facts", stats)
        ok = os.path.isfile(args.out)
        rep.check(ok, "iç blok PDF var (%s)"
                  % os.path.relpath(args.out, pl.ROOT))
        if ok:
            mb = os.path.getsize(args.out) / 1e6
            rep.check(abs(mb - float(facts.get("pdfMB") or 0)) < 0.6,
                      "PDF boyutu ölçümle tutuyor (%.1f MB / kayıt %.1f MB)"
                      % (mb, float(facts.get("pdfMB") or 0)))
            rep.check(int(facts.get("pages") or 0) >= 24
                      and int(facts.get("pages") or 0) % 2 == 0,
                      "kayıtlı sayfa sayısı geçerli (%s)" % facts.get("pages"))
            rep.check(facts.get("metaWithheld") == ["meta-001"],
                      "⭑ SON SORUNUN CEVABI BASILMADI ⭑ (kayıt)")
            rep.check(int(facts.get("hintsTypeset") or 0) >= 300
                      and int(facts.get("solutionsTypeset") or 0) == 100,
                      "kayıtlı ipucu/çözüm sayısı tam (%s / %s)"
                      % (facts.get("hintsTypeset"),
                         facts.get("solutionsTypeset")))
        return rep.finish("%s · --check" % args.binding, None)
    tmp = args.out + ".pass1"
    # ⚠ Yazar ve yayıncı BURADA YAZILMAZ; metadata.json'dan gelir.
    info = build(book, sols, gutter_for(250, args.binding), tmp, meta)
    g = gutter_for(info["pages"], args.binding)
    info = build(book, sols, g, args.out, meta)
    if info["pages"] % 2 == 1:
        # tek çıktı → son sayfa eklenip BAŞTAN dizilir
        info = build(book, sols, g, args.out, meta, pad=True)
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
    rep.check(pages % 2 == 0,
              "⭑ SAYFA SAYISI ÇİFT ⭑ (%d) — yaprak tam, sırt şaşmaz"
              % pages)
    rep.check(info["hintsTypeset"] >= 300, "303 ipucu dizildi (%d)" % info["hintsTypeset"])
    rep.check(info["solutionsTypeset"] == 100,
              "100 çözüm dizildi — meta HARİÇ (%d)" % info["solutionsTypeset"])
    rep.check(info["metaWithheld"] == ["meta-001"],
              "⭑ SON SORUNUN CEVABI BASILMADI ⭑ (kitabın kendi sözü) — %s"
              % (info["metaWithheld"] or "⛔ BASILDI"))
    rep.check(size_mb < 650, "PDF KDP sınırının altında (%.1f MB)" % size_mb)
    rep.check(os.path.isfile(args.out), "iç blok PDF üretildi")

    rep.facts.update({"pages": pages, "gutterIn": g,
                      "binding": args.binding,
                      "hintsTypeset": info["hintsTypeset"],
                      "solutionsTypeset": info["solutionsTypeset"],
                      "metaWithheld": info["metaWithheld"],
                      "pdfMB": round(size_mb, 2),
                      "trim": [TRIM_W, TRIM_H],
                      "path": os.path.relpath(args.out, pl.ROOT)})
    stats = (STATS if args.binding == "paperback"
             else STATS.replace("interior.json", "interior-hardcover.json"))
    return rep.finish("%s · %d sayfa" % (args.binding, pages), stats)


if __name__ == "__main__":
    sys.exit(main())
