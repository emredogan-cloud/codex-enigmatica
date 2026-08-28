#!/usr/bin/env python3
"""
BASKI KAPAĞI — tam sarmal PDF, ölçülen sayfa sayısından
================================================================================
⚠ SIRT GENİŞLİĞİ UYDURULMAZ. Sayfa sayısı × kâğıt kalınlığı eder ve
sayfa sayısı `06_REPORTS/tracked/interior.json` içinden — yani ÜRETİLEN
iç bloktan — okunur. Tahminle basılmış bir sırt, yamuk basılmış bir
kitaptır ve POD'da geri dönüşü yoktur.

Geometri (KDP tam sarmal):

    tam genişlik = taşma + arka(6") + SIRT + ön(6") + taşma
    tam yükseklik = taşma + 9" + taşma          taşma = 0,125"

⭑ TİPOGRAFİ CLI İLE BASILIR ⭑ Kurucudan metni elle yerleştirmesi
istenmez. Başlık, yazar, sırt yazısı ve arka kapak metni vektör olarak
çizilir; sanat değiştirilmez ve opak beyaz kutu KULLANILMAZ — güvenli
alanlar zaten sakin seçildi.

⚠ UYDURULMAZ: ISBN, barkod numarası, ödül, alıntı, "çok satan".
Barkod alanı KDP'nin kendi yerleştirmesi için BOŞ bırakılır.

Bağımlılık: reportlab + Pillow. Çıkış kodu 2 = bağımlılık yok.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
OUTDIR = os.path.join(pl.ROOT, "08_OUTPUT", "PAPERBACK")
META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
INTERIOR = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "interior.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "cover.json")

TRIM_W, TRIM_H = 6.0, 9.0
BLEED = 0.125
SAFE = 0.25                       # kesim çizgisinden metne asgari uzaklık

# ⭑ KDP'NİN GERÇEK REDDİNDEN GELEN GÜVENLİ ALAN ⭑
# ⚠ BU SAYILAR TAHMİN DEĞİL, AMAZON'UN KENDİ RET MESAJINDAN ALINDI
# (28 Ağustos 2026, "Attention needed: Please review your title"):
#
#   "Please make sure that all elements intended to be viewable appear
#    at least 0.716in (18.175mm) away from the outside edges. All front
#    cover text must also stop at least 0.4in (10mm) away from the edge
#    of the spine."
#
# ⚠ VE ÖLÇÜ **DIŞ KENARDAN**DIR, kesim çizgisinden değil. Buradaki
# `SAFE = 0.25` kesimden ölçüyordu: 0,125" taşmayla birlikte dış
# kenardan yalnızca 0,375" ediyordu — KDP'nin istediğinin YARISINDAN AZ.
# Reddin sebebi tam olarak buydu.
KDP_EDGE_IN = 0.716               # dış kenardan görünür her öğeye
KDP_SPINE_IN = 0.40               # sırt kenarından ÖN KAPAK METNİNE

# ⚠ Asgariye dayanmak asgariyi aşmaktır (iç blokta aynı ders alındı):
# yazı tipi ölçüleri, yuvarlama ve raster kenarı birkaç binde bir inç
# oynatır. Pay eklenir.
COVER_SAFETY_IN = 0.06

# ⚠ KDP kâğıt kalınlıkları (sayfa başına inç). Krem kâğıt kalındır;
# beyaz kâğıdın değeriyle hesaplamak sırtı DAR yapar ve sanat kayar.
PAPER_IN = {"cream": 0.0025, "white": 0.002252}

# ⭑ SEÇİM ÖLÇÜLDÜ ⭑ `wrap-01`, dört tipografi bölgesinin üçünde daha
# sakin çıktı (sırt 36,5 / 47,2 · yazar 33,0 / 57,1 · arka 27,4 / 29,2).
# `wrap-02`nin ortasında görünür bir dikey çizgi var — promptun açıkça
# yasakladığı "yapay sırt paneli".
# ⭑ 4× YÜKSELTİLMİŞ SÜRÜM KULLANILIR ⭑ (27 Ağu 2026)
# ⚠ Kurucunun ham sarmal sanatı 1840 × 855 pikseldi. Kapak boyutuna
# yayıldığında GERÇEK bilgi yalnızca 92 (ciltsiz) / 82 (ciltli) ppi
# ediyordu — KDP'nin 300 ppi hedefinin %31'i. PDF 300 ppi'lık PİKSEL
# taşıyordu ama o piksellerin arkasında o kadar BİLGİ yoktu.
#
# Depo bunun için zaten bir hat kurmuştu (ASSET_UPSCALING_REPORT.md,
# Real-ESRGAN / upscayl-standard-4x) ve portföydeki diğer üç kitapta
# kullanılmıştı; Codex Enigmatica'ya HİÇ uygulanmamıştı. Uygulandı:
#
#   1840 × 855  →  7360 × 3420   (4×, upscayl-standard-4x)
#   ciltsiz     92 → 370 ppi
#   ciltli      82 → 328 ppi     (ikisi de 300'ün ÜSTÜNDE)
#
# ⚠ VE BUNUN NE OLMADIĞI: Real-ESRGAN makul detay ÜRETİR, kaybolmuş
# detayı GERİ GETİRMEZ. Dosya artık gerçekten 300 ppi'dır ve bikübik
# büyütmeden belirgin olarak keskindir — ama 300 ppi'da ÜRETİLMİŞ bir
# sanatla aynı şey değildir. Bu ayrım raporda da aynen durur.
DEFAULT_ART = "codex-enigmatica-wrap-cover-option-01-4x-300dpi.png"


def spine_in(pages: int, paper: str) -> float:
    return pages * PAPER_IN.get(paper, PAPER_IN["cream"])


# ═══ CİLT GEOMETRİLERİ ════════════════════════════════════════════════
# ⚠ HARDCOVER DEĞERLERİ TÜRETİLMEDİ — kurucunun teslim ettiği KDP
# hesaplayıcı ekran görüntüsünden OKUNDU:
#   hardcover-calculator.png → 03_COVER/HARDCOVER_CALCULATOR_VALUES.md
# Ciltsiz geometrisini ciltliye kopyalamak 1,45 inç dar bir kapak
# üretir ve KDP reddeder.
# ⭑ HESAPLAYICININ KOŞTUĞU TABAN ⭑ — bunlar GİRDİLERDİR, çıktı değil.
# Sırt bu tabandan TÜRETİLİR (§ geometry) çünkü sırt sayfa sayısına ve
# kâğıda bağlı TEK ölçüdür; kapak tahtası, oluk ve sarma payları sayfa
# sayısından bağımsızdır ve doğrudan okunur.
CALC_PAGES = 263
CALC_PAPER = "white"
CALC_SPINE = 0.781
# Tahta payı = hesaplayıcının verdiği sırt − o sayfa sayısının kâğıt payı.
# Bu, hesaplayıcının kendi çıktısından ÖLÇÜLEN bir sabittir; uydurulmadı.
BOARD_IN = round(CALC_SPINE - CALC_PAGES * 0.002252, 5)   # 0.18872 in

HARDCOVER = {
    "pages": CALC_PAGES, "paper": CALC_PAPER,
    "full_w": 14.356, "full_h": 10.417,
    "front_w": 6.197, "front_h": 9.236,
    "spine_w": 0.781,
    "wrap": 0.591,          # tahta üstüne sarma payı
    "hinge": 0.394,         # sırt ile tahta arası oluk
    "margin": 0.125,
    "spine_safe_w": 0.656, "spine_safe_h": 8.986,
    "spine_margin": 0.062,
    "barcode_w": 0.25, "barcode_h": 0.375,
}


def geometry(binding: str, pages: int, paper: str) -> dict:
    """Kapak geometrisi. Ciltsiz HESAPLANIR, ciltli OKUNUR."""
    if binding == "hardcover":
        g = dict(HARDCOVER)
        # ⭑ SIRT TÜRETİLİR, YAMANMAZ ⭑
        # ⚠ Önceki hâl hesaplayıcının 263 sayfalık sırtına bir "delta"
        # ekliyordu. Sayısal olarak aynı yere varıyordu ama İKİ soruyu
        # birbirine karıştırıyordu: sayfa farkı ve KÂĞIT farkı. İkincisi
        # ölçülünce ortaya çıktı ki asıl tehlike orada:
        #
        #   274 sayfa · beyaz  → 0,8058 in
        #   274 sayfa · krem   → 0,8737 in
        #   fark 0,0680 in     → KDP toleransı ±0,0625 in AŞILIR
        #
        # Yani yanlış kâğıtla basılan bir ciltli kapak REDDEDİLİR.
        # Sırt artık kâğıdı ve sayfa sayısını AÇIKÇA alır.
        g["paper"] = paper
        g["pages"] = pages
        g["calcBasis"] = {"pages": CALC_PAGES, "paper": CALC_PAPER,
                          "spine": CALC_SPINE, "boardIn": BOARD_IN}
        g["boardIn"] = BOARD_IN
        g["spine_w"] = round(pages * PAPER_IN.get(paper, PAPER_IN["cream"])
                             + BOARD_IN, 4)
        g["spineDeltaIn"] = round(g["spine_w"] - CALC_SPINE, 5)
        g["deltaPages"] = pages - CALC_PAGES
        g["paperMatchesCalculator"] = (paper == CALC_PAPER)
        # ⚠ "Bayat" yalnızca sayfa farkının toleransı aşması DEĞİLDİR.
        # Kâğıt hesaplayıcıdan farklıysa geometri BAŞKA bir üründür ve
        # hesaplayıcı o ürün için hiç koşmamıştır.
        g["stale"] = (abs(g["spineDeltaIn"]) > 0.0625
                      or not g["paperMatchesCalculator"])
        g["full_w"] = round(2 * g["front_w"] + g["spine_w"]
                            + 2 * g["wrap"], 4)
        g["binding"] = "hardcover"
        return g
    sp = pages * PAPER_IN.get(paper, PAPER_IN["cream"])
    return {"binding": "paperback", "pages": pages, "paper": paper,
            "full_w": BLEED + TRIM_W + sp + TRIM_W + BLEED,
            "full_h": BLEED + TRIM_H + BLEED,
            "front_w": TRIM_W, "front_h": TRIM_H,
            "spine_w": sp, "wrap": BLEED, "hinge": 0.0,
            "margin": BLEED, "spine_safe_w": max(0.0, sp - 0.125),
            "spine_safe_h": TRIM_H - 0.5, "spine_margin": 0.0625,
            "barcode_w": 2.0, "barcode_h": 1.2, "stale": False}


def build(art: str, pages: int, paper: str, meta: dict, path: str,
          binding: str = "paperback") -> dict:
    from PIL import Image
    from reportlab.lib.pagesizes import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import cover_type as CT

    G = geometry(binding, pages, paper)
    W, H = G["full_w"], G["full_h"]
    Wp, Hp = W * inch, H * inch

    F = "/usr/share/fonts/truetype/dejavu"
    REG, BOLD = (os.path.join(F, "DejaVuSerif.ttf"),
                 os.path.join(F, "DejaVuSerif-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("C", REG))
    pdfmetrics.registerFont(TTFont("C-B", BOLD))

    # ── SANAT: tam sarmal orana kırpılır, sonra 300 dpi'a çıkar ────────
    im = Image.open(art).convert("RGB")
    want = W / H
    iw, ih = im.size
    if iw / ih > want:
        nw = int(round(ih * want))
        im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(round(iw / want))
        im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    src_w, src_h = im.size
    native_dpi = round(src_w / W, 1)

    target_px = int(round(W * 300))
    im = im.resize((target_px, int(round(target_px / want))), Image.LANCZOS)
    PPI = im.width / W                       # piksel / inç

    def px(x_in, y_in):
        """inç (PDF: sol-alt) → piksel (PIL: sol-üst)"""
        return int(round(x_in * PPI)), int(round((H - y_in) * PPI))

    # ── koordinatlar ───────────────────────────────────────────────────
    edge = G["wrap"]                          # dış pay (taşma ya da sarma)
    back_x0 = edge
    spine_x0 = edge + G["front_w"] + G["hinge"]
    front_x0 = spine_x0 + G["spine_w"] + G["hinge"]
    fcx = front_x0 + G["front_w"] / 2
    bcx = back_x0 + G["front_w"] / 2
    scx = spine_x0 + G["spine_w"] / 2

    # ── ⭑ KDP GÜVENLİ BANDI ⭑ ──────────────────────────────────────────
    # ⚠ CİLTLİ İÇİN SAYI KOPYALANMAZ, TÜRETİLİR (yönerge § 9).
    # Ciltli kapakta dış 0,591" **tahtanın arkasına SARILIR** ve
    # görünmez; görünür alan ondan sonra başlar, üstüne hesaplayıcının
    # kendi kenar payı (0,125") biner:
    #     0,591 + 0,125 = 0,716"
    # Ciltsizde ise KDP'nin ret mesajındaki sayı doğrudan 0,716"dır.
    # İki bağımsız yoldan aynı sayıya varılır; yine de ikisi AYRI
    # hesaplanır ve büyüğü alınır — biri değişirse öteki sürüklenmesin.
    edge_min = (max(KDP_EDGE_IN, G["wrap"] + G["margin"])
                if G["binding"] == "hardcover" else KDP_EDGE_IN)
    lo = edge_min + COVER_SAFETY_IN
    front_l = front_x0 + KDP_SPINE_IN + COVER_SAFETY_IN
    front_r = W - lo
    front_cx = (front_l + front_r) / 2
    front_maxw = front_r - front_l
    back_l = lo
    back_r = spine_x0 - KDP_SPINE_IN - COVER_SAFETY_IN
    top_lim = H - lo
    bot_lim = lo
    SAFE_BOX = {"edgeMinIn": round(edge_min, 4),
                "spineMinIn": KDP_SPINE_IN,
                "toleranceIn": COVER_SAFETY_IN,
                "frontBandIn": [round(front_l, 4), round(front_r, 4)],
                "backBandIn": [round(back_l, 4), round(back_r, 4)],
                "vBandIn": [round(bot_lim, 4), round(top_lim, 4)]}

    measured = []

    def fit(txt, font, maxw_in, start, floor=9):
        sz = start
        while sz > floor and pdfmetrics.stringWidth(txt, font, sz) > maxw_in * inch:
            sz -= 0.5
        return sz

    def ink_box(txt, font, size_pt, cx_in, y_in, rot=False):
        """Bir satırın GERÇEK mürekkep kutusu (inç) — tahmin değil.

        ⚠ Yükseklik yazı tipinin KENDİ ascent/descent değerlerinden
        alınır; "boyutun %75'i" gibi bir yaklaşıklık KDP'nin 0,716"
        eşiğinde binde birlerle oynar ve yanlış yeşil üretir.
        """
        w = pdfmetrics.stringWidth(txt, font, size_pt) / inch
        face = pdfmetrics.getFont(font).face
        asc = face.ascent / 1000.0 * size_pt / 72.0
        dsc = abs(face.descent) / 1000.0 * size_pt / 72.0
        if rot:                       # sırt yazısı 90° döner
            return (cx_in - asc, y_in - w / 2, cx_in + dsc, y_in + w / 2)
        return (cx_in - w / 2, y_in - dsc, cx_in + w / 2, y_in + asc)

    def plan(txt, bold, size_pt, cx_in, y_in, label, rot=False):
        """⭑ ÖLÇ, MÜREKKEBİ SEÇ, HÂLEYİ HAZIRLA ⭑ — sanat üstünde."""
        if not txt:
            return None
        r = CT.place(im, txt, BOLD if bold else REG,
                     max(6, int(round(size_pt * PPI / 72.0))),
                     *px(cx_in, y_in), rotate=rot)
        # ⭑ ÖLÇÜLEN KOORDİNAT KAYDA GİRER ⭑
        # ⚠ BU SATIR BİR KUSURDAN DOĞDU: ölçüm bandın ortasına, ÇİZİM
        # ise panelin ortasına yapılıyordu (`front_cx` ↔ `fcx`). İki yer
        # aynı yerleşimi tutunca biri düzeltilip öteki unutuldu ve kapak
        # "ölçüldü, temiz" derken PDF'te taşıyordu. Artık tek kaynak:
        # çizim bu kaydı okur.
        r.update(text=txt, label=label, sizePt=round(size_pt, 1),
                 cxIn=cx_in, yIn=y_in,
                 boxIn=[round(v, 4) for v in
                        ink_box(txt, "C-B" if bold else "C", size_pt,
                                cx_in, y_in, rot)])
        measured.append(r)
        return r

    title = (meta.get("title") or "").upper()
    author = (meta.get("author") or "").upper()
    pub = meta.get("publisher") or ""
    sub = meta.get("subtitle") or ""

    # ⚠ GENİŞLİK ARTIK ÖN PANELDEN DEĞİL, KDP BANDINDAN GELİR.
    # Eskiden `front_w - 2*SAFE - 0.30` idi: 30,5 punto başlık 5,119"
    # eder ve sağ dış kenara yalnızca 0,565" bırakırdı — KDP 0,716"
    # istiyor. Başlık şimdi banda sığdırılır ve BANDIN ortasına
    # yerleşir (panelin ortasına değil; ikisi artık aynı yer değildir).
    t_size = fit(title, "C-B", front_maxw, 46, 16)
    t_y = H - edge - 1.45
    r_title = plan(title, True, t_size, front_cx, t_y, "ön başlık")

    sub_lines = []
    if sub:
        words, line = sub.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, "C", 13) > front_maxw * inch:
                sub_lines.append(line)
                line = w
            else:
                line = t
        sub_lines.append(line)
    r_sub = []
    sy = t_y - 0.62
    for ln in sub_lines[:3]:
        r_sub.append(plan(ln, False, 13, front_cx, sy, "alt başlık"))
        sy -= 0.27

    # ⚠ DİKEY YERLEŞİM DE ÖLÇÜLÜR. Yayıncı satırı `edge + 0.60`da
    # duruyordu; ciltsizde mürekkebin altı 0,689"e iniyor ve 0,716"
    # eşiğini 0,027" ihlal ediyordu. Taban artık eşikten TÜRETİLİR.
    def lift(size_pt, want_bottom):
        """Mürekkebin altı `want_bottom`ın altına inmeyecek taban çizgisi."""
        dsc = abs(pdfmetrics.getFont("C").face.descent) / 1000.0 * size_pt / 72.0
        return want_bottom + dsc

    pub_y = max(edge + 0.60, lift(10.5, bot_lim))
    a_y = max(edge + 0.95, pub_y + 0.35)
    r_auth = plan(author, True, 21, front_cx, a_y, "ön yazar")
    r_pub = plan(pub, False, 10.5, front_cx, pub_y, "yayıncı")

    # ── SIRT ───────────────────────────────────────────────────────────
    spine_ok = G["spine_w"] >= 0.0625
    r_spine = None
    if spine_ok:
        s_size = fit(title, "C-B", G["spine_safe_h"] - 1.2,
                     15 if G["spine_w"] >= 0.5 else 11, 7)
        r_spine = plan(title, True, s_size, scx, H / 2 + 0.05,
                       "sırt başlık", rot=True)
        plan(author, False, s_size * 0.62, scx, H / 2 - 1.9,
             "sırt yazar", rot=True)

    # ── ARKA KAPAK metni ───────────────────────────────────────────────
    desc = (meta.get("description") or "").strip()
    # ⚠ SAYFA SAYISI CİLDE GÖRE DÜZELTİLİR.
    # `description` tek bir alandır ve ciltsizin sayfa sayısını taşır
    # ("… · 274 pages"). Ciltli 276 sayfaya çıkınca aynı cümle CİLTLİ
    # KAPAĞA basılacaktı: basılı, yanlış ve geri alınamaz bir sayı.
    _ed_pages = next((e.get("pages") for e in (meta.get("editions") or [])
                      if e.get("id") == G["binding"]), None)
    if _ed_pages and _ed_pages != meta.get("pageCount"):
        desc = re.sub(r"\b%d pages\b" % meta["pageCount"],
                      "%d pages" % _ed_pages, desc)
    # ⚠ Arka kapak da aynı fiziksel kesim riskini taşır. Eskiden
    # `back_x0 + SAFE + 0.28` = 0,655" idi; 0,716" eşiğinin altında.
    bx0 = max(back_x0 + SAFE + 0.28, back_l)
    bx1 = min(back_x0 + G["front_w"] - SAFE - 0.10, back_r)
    bw_in = bx1 - bx0
    fs = 10.0
    lines = []
    for block in desc.split("\n\n"):
        words, line = block.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, "C", fs) > bw_in * inch:
                lines.append(line)
                line = w
            else:
                line = t
        if line:
            lines.append(line)
        lines.append("")

    by = min(H - edge - 1.30, top_lim - 0.30)
    stop = max(edge + SAFE + G["barcode_h"] + 0.30,
               bot_lim + G["barcode_h"] + 0.20)
    back_rows = []
    for ln in lines:
        if by < stop:
            break
        if ln:
            w_in = pdfmetrics.stringWidth(ln, "C", fs) / inch
            r = CT.place(im, ln, REG, max(6, int(round(fs * PPI / 72.0))),
                         *px(bx0 + w_in / 2, by))
            r.update(text=ln, label="arka kopya", sizePt=fs,
                     boxIn=[round(v, 4) for v in
                            ink_box(ln, "C", fs, bx0 + w_in / 2, by)])
            measured.append(r)
            back_rows.append((ln, by, r))
            by -= fs * 1.5 / 72.0
        else:
            by -= fs * 0.7 / 72.0

    # ── PDF: sanat (perdeli) + VEKTÖR metin ────────────────────────────
    cv = canvas.Canvas(path, pagesize=(Wp, Hp))
    cv.setTitle(meta.get("title") or "")
    cv.drawImage(ImageReader(im), 0, 0, width=Wp, height=Hp)

    def haloed(x_pt, y_pt, text, r, font):
        """⭑ ÖNCE HÂLE, SONRA MÜREKKEP ⭑ — ikisi de VEKTÖR.

        ⚠ `setTextRenderMode` KANVASTA DEĞİL, METİN NESNESİNDEDİR
        (reportlab). Kip 1 yalnızca dış çizgi, kip 0 yalnızca dolgu.
        Kip 2 (ikisi birden) çizgiyi harfin ÜSTÜNE bindirip inceltir;
        hâle harfin DIŞINDA kalmalıdır.
        """
        if r.get("needsHalo"):
            cv.saveState()
            cv.setLineWidth(max(0.6, r["sizePt"] * 0.085))
            cv.setStrokeColorRGB(*r["halo"])
            cv.setLineJoin(1)
            t = cv.beginText(x_pt, y_pt)
            t.setFont(font, r["sizePt"])
            t.setTextRenderMode(1)
            t.textOut(text)
            cv.drawText(t)
            cv.restoreState()
        t = cv.beginText(x_pt, y_pt)
        t.setFont(font, r["sizePt"])
        t.setTextRenderMode(0)
        t.setFillColorRGB(*r["ink"])
        t.textOut(text)
        cv.drawText(t)

    def centred(r, cx_in, y_in, font, text=None):
        if not r:
            return
        txt = text if text is not None else r["text"]
        w = pdfmetrics.stringWidth(txt, font, r["sizePt"])
        haloed(cx_in * inch - w / 2, y_in * inch, txt, r, font)

    def draw_c(r, font):
        """⚠ Koordinat ARTIK PARAMETRE DEĞİL — ölçülen kayıttan gelir."""
        if r:
            centred(r, r["cxIn"], r["yIn"], font)

    draw_c(r_title, "C-B")
    for r in r_sub:
        draw_c(r, "C")
    draw_c(r_auth, "C-B")
    draw_c(r_pub, "C")

    if spine_ok and r_spine:
        cv.saveState()
        cv.translate(scx * inch, Hp / 2)
        cv.rotate(-90)
        w = pdfmetrics.stringWidth(title, "C-B", r_spine["sizePt"])
        haloed(0.05 * inch - w / 2, -r_spine["sizePt"] * 0.34,
               title, r_spine, "C-B")
        sa = [m for m in measured if m["label"] == "sırt yazar"]
        if sa:
            w2 = pdfmetrics.stringWidth(author, "C", sa[0]["sizePt"])
            haloed(-1.95 * inch - w2 / 2, -sa[0]["sizePt"] * 0.34,
                   author, sa[0], "C")
        cv.restoreState()

    for ln, yy, r in back_rows:
        haloed(bx0 * inch, yy * inch, ln, r, "C")

    cv.showPage()
    cv.save()

    worst = min((m["contrast"] for m in measured), default=0)
    return {"binding": G["binding"], "spineIn": round(G["spine_w"], 4),
            "widthIn": round(W, 4), "heightIn": round(H, 4),
            "pages": pages, "paper": G.get("paper", paper),
            "artCropPx": [src_w, src_h], "nativeDpi": native_dpi,
            "renderedPx": [im.width, im.height],
            "hingeIn": G["hinge"], "wrapIn": G["wrap"],
            "spineSafeIn": [G["spine_safe_w"], G["spine_safe_h"]],
            "barcodeBoxIn": [G["barcode_w"], G["barcode_h"]],
            "spineTextPrinted": spine_ok,
            "safeArea": dict(SAFE_BOX,
                             frontSpineEdgeIn=round(front_x0, 4),
                             spineLeftEdgeIn=round(spine_x0, 4)),
            "staleCalculator": G.get("stale", False),
            "spineDeltaIn": G.get("spineDeltaIn", 0),
            "deltaPages": G.get("deltaPages", 0),
            "paperMatchesCalculator": G.get("paperMatchesCalculator", True),
            "calcBasis": G.get("calcBasis"),
            "boardIn": G.get("boardIn"),
            "worstContrast": round(worst, 2),
            "haloUsed": sum(1 for m in measured if m["needsHalo"]),
            "typeRowsTotal": len(measured),
            "edgeContrastMin": round(min((m["edgeContrast"]
                                          for m in measured), default=0), 2),
            "typeMeasured": measured}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--art", default=DEFAULT_ART)
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--binding", default="paperback",
                    choices=("paperback", "hardcover"))
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    print("=" * 74)
    print("  BASKI KAPAĞI · %s" % args.binding.upper())
    print("=" * 74)

    try:
        import reportlab                                       # noqa: F401
        from PIL import Image                                  # noqa: F401
        import cover_type                                      # noqa: F401
    except ImportError as exc:
        print("⛔ bağımlılık yok: %s" % exc)
        return 2

    rep = pl.Report(args.verbose)
    meta = pl.load_json(META) or {}
    # ⭑ HER CİLT KENDİ İÇ BLOĞUNUN SAYFA SAYISINI KULLANIR ⭑
    # ⚠ BURASI HER ZAMAN `interior.json`u (CİLTSİZ) okuyordu. İki cilt
    # aynı sayfa sayısında olduğu sürece kusur GÖRÜNMEZDİ — ve tam
    # olarak öyleydi, ikisi de 274'tü. Ciltli 276'ya çıkınca ciltli
    # kapak hâlâ 274'e göre sırt hesapladı: 0,8058" yerine 0,8103"
    # olmalıydı. Sessiz, ölçülene kadar görünmez ve BASKIDA yanlış.
    inter_path = (INTERIOR if args.binding == "paperback"
                  else INTERIOR.replace("interior.json",
                                        "interior-hardcover.json"))
    inter = (pl.load_json(inter_path) or {}).get("facts") or {}
    pages = args.pages or inter.get("pages") or 0

    # ── ⭑ `--check` ÜRETMEZ ⭑ ─────────────────────────────────────────
    # ⚠ Aynı kusur iç blokta da vardı ve aynı bedeli ödetiyordu: bayrak
    # bildiriliyor, hiç okunmuyor, kapak her koşuda YENİDEN üretiliyordu.
    # `qa_all.sh` içinde bu adım `kdp_package.py`den SONRA koşar; PDF her
    # üretimde gömülü zaman damgası yüzünden değişir ve yayın paketinin
    # SHA256 toplamları TUTMAZ.
    if args.check:
        out = args.out or os.path.join(
            pl.ROOT, "08_OUTPUT", args.binding.upper(), "cover.pdf")
        stats = pl.load_json(
            STATS if args.binding == "paperback"
            else STATS.replace("cover.json", "cover-hardcover.json")) or {}
        f = stats.get("facts", stats)
        ok = os.path.isfile(out)
        rep.check(ok, "kapak PDF var (%s)" % os.path.relpath(out, pl.ROOT))
        rep.check(int(f.get("pages") or 0) == int(pages),
                  "⭑ KAPAK SAYFA SAYISI İÇ BLOKLA TUTUYOR ⭑ (%s / %s)"
                  % (f.get("pages"), pages))
        rep.check(bool(f.get("spineIn")),
                  "sırt genişliği kayıtlı (%s in)" % f.get("spineIn"))
        return rep.finish("%s · --check" % args.binding, None)
    rep.check(bool(pages), "⭑ SAYFA SAYISI ÖLÇÜLEN İÇ BLOKTAN ⭑ (%s)"
              % (pages or "YOK"))
    if not pages:
        return rep.finish("sayfa yok", None)

    paper = "cream"
    for ed in meta.get("editions") or []:
        if ed.get("id") == args.binding:
            paper = ed.get("paper") or paper

    art = os.path.join(RAW, args.art)
    rep.check(os.path.isfile(art), "sarmal sanat var (%s)" % args.art)
    if not os.path.isfile(art):
        return rep.finish("sanat yok", None)

    out = args.out or os.path.join(
        pl.ROOT, "08_OUTPUT", args.binding.upper(), "cover.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    info = build(art, pages, paper, meta, out, args.binding)

    print("\n── geometri ──")
    for k, v in (("sayfa (ölçülen)", pages), ("kâğıt", info["paper"]),
                 ("SIRT", "%.4f in" % info["spineIn"]),
                 ("menteşe", "%.3f in" % info["hingeIn"]),
                 ("sarma/taşma", "%.3f in" % info["wrapIn"]),
                 ("tam kapak", "%.3f × %.3f in"
                  % (info["widthIn"], info["heightIn"])),
                 ("sanat doğal", "%.1f dpi" % info["nativeDpi"]),
                 ("basılan", "%d × %d px" % tuple(info["renderedPx"]))):
        print("  %-24s %s" % (k, v))

    print("\n── ⭑ ÖLÇÜLEN TİPOGRAFİ KARŞITLIĞI ⭑ ──")
    for m in info["typeMeasured"][:9]:
        print("  %-13s %-28s %5.2f:1 %s"
              % (m["label"], m["text"][:28], m["contrast"],
                 "hâle" if m["needsHalo"] else ""))
    n = len(info["typeMeasured"])
    if n > 9:
        print("  … %d satır daha" % (n - 9))

    import cover_type as CT
    # ⭑ OKUNURLUK İKİ YOLDAN BİRİYLE GARANTİ EDİLİR ⭑
    # ⚠ Sadece "mürekkep ↔ zemin" ölçmek yanlış olurdu: hâleli bir harf,
    # zemini ne olursa olsun kendi KENARINDAN okunur. Bu yüzden her
    # satır ya zeminle yeterli karşıtlığa sahiptir YA DA hâlelidir —
    # ve hâlenin kenar karşıtlığı ayrıca ölçülür.
    weak = [m for m in info["typeMeasured"]
            if m["contrast"] < CT.MIN_CONTRAST and not m["needsHalo"]]
    rep.check(not weak,
              "⭑ HER SATIR YA ZEMİNLE ≥%.1f:1 YA DA HÂLELİ ⭑ (%d/%d "
              "hâleli)" % (CT.MIN_CONTRAST, info["haloUsed"],
                           info["typeRowsTotal"])
              + ("" if not weak else " — ⛔ korumasız: %s"
                 % [m["label"] for m in weak][:4]))
    rep.check(info["edgeContrastMin"] >= CT.MIN_CONTRAST,
              "⭑ HÂLE KENAR KARŞITLIĞI ≥%.1f:1 ⭑ (ölçülen %.1f:1) — "
              "harf zeminden BAĞIMSIZ olarak ayrışıyor"
              % (CT.MIN_CONTRAST, info["edgeContrastMin"]))
    if args.binding == "hardcover":
        d = info.get("spineDeltaIn", 0)
        # ⭑ KÂĞIT ÖNCE ÖLÇÜLÜR ⭑ — sayfa farkından DAHA TEHLİKELİDİR.
        # 274 sayfada beyaz→krem geçişi sırtı 0,0680 in oynatır ve KDP'nin
        # ±0,0625 in toleransını AŞAR. Sayfa farkının kendisi ise yalnızca
        # 0,0248 in (toleransın %39,6'sı). Yani "hesaplayıcı eski" diye
        # bakılan yerde asıl kusur başka yerdeydi.
        rep.check(info.get("paperMatchesCalculator", True),
                  "⭑ CİLTLİ KÂĞIDI HESAPLAYICININ KOŞTUĞU KÂĞITLA AYNI ⭑ "
                  "(hesaplayıcı: %s · ürün: %s)"
                  % (CALC_PAPER, info.get("paper"))
                  + ("" if info.get("paperMatchesCalculator", True)
                     else " — ⛔ FARKLI KÂĞIT = BAŞKA GEOMETRİ; "
                          "hesaplayıcı bu ürün için hiç koşmadı"))
        rep.check(not info["staleCalculator"],
                  "⭑ HESAPLAYICI SAPMASI TOLERANS İÇİNDE ⭑ (%+d sayfa → "
                  "sırt %+.5f in · KDP toleransı ±0,0625)"
                  % (info.get("deltaPages", 0), d))
        if info.get("deltaPages"):
            rep.warn("hesaplayıcı %d sayfa · %s kâğıtla koştu, iç blok %d "
                     "sayfa · %s — sırt hesaplayıcının TAHTA PAYINDAN "
                     "(%.5f in) yeniden TÜRETİLDİ: %.4f in. Sapma "
                     "%+.5f in, toleransın %%%.1f'i. Tam kesinlik "
                     "isteniyorsa hesaplayıcı %d sayfa + %s ile yeniden "
                     "koşturulmalı (A15)."
                     % (CALC_PAGES, CALC_PAPER, pages, info.get("paper"),
                        BOARD_IN, info["spineIn"], d,
                        abs(d) / 0.0625 * 100, pages, info.get("paper")))
    # ── ⭑ KDP GÜVENLİ ALANI · HER SATIR ÖLÇÜLÜR ⭑ ──────────────────────
    # ⚠ BU DENETİM BİR KDP REDDİNDEN DOĞDU. Önceki kapı yalnızca
    # KARŞITLIK ölçüyordu — yani yazının OKUNUR olduğunu doğruluyor,
    # SAYFADA KALDIĞINI hiç sormuyordu. Amazon 28 Ağu 2026'da tam olarak
    # bunu reddetti: "text/graphics that extend beyond the trim line".
    #
    # ⚠ Ve "guide'ların içinde duruyor gibi" yetmez (yönerge § 8):
    # her satırın GERÇEK mürekkep kutusu, yazı tipinin kendi
    # ascent/descent değerleriyle hesaplanır ve eşiğe vurulur.
    sa = info.get("safeArea") or {}
    if sa:
        front_spine_edge = sa["frontSpineEdgeIn"]
        spine_left_edge = sa["spineLeftEdgeIn"]
        W, H = info["widthIn"], info["heightIn"]
        fl, fr = sa["frontBandIn"]
        bl, br = sa["backBandIn"]
        vb, vt = sa["vBandIn"]
        FRONT = {"ön başlık", "alt başlık", "ön yazar", "yayıncı"}
        BACK = {"arka kopya"}
        bad = []
        for m in info["typeMeasured"]:
            box = m.get("boxIn")
            if not box:
                continue
            x0, y0, x1, y1 = box
            lab = m.get("label", "")
            if lab in FRONT:
                lo_x, hi_x = fl, fr
            elif lab in BACK:
                lo_x, hi_x = bl, br
            else:
                continue                      # sırt: hesaplayıcının kendi alanı
            if x0 < lo_x - 1e-6 or x1 > hi_x + 1e-6 or y0 < vb - 1e-6 \
                    or y1 > vt + 1e-6:
                bad.append("%s[%s] x %.3f–%.3f y %.3f–%.3f"
                           % (lab, m["text"][:18], x0, x1, y0, y1))
        rep.check(not bad,
                  "⭑ HER ÖN/ARKA KAPAK SATIRI KDP GÜVENLİ ALANINDA ⭑ "
                  "(dış kenar ≥%.3f\" · sırt ≥%.2f\")"
                  % (sa["edgeMinIn"], sa["spineMinIn"])
                  + ("" if not bad else " — ⛔ %d ihlal: %s"
                     % (len(bad), bad[:3])))
        print("\n── ⭑ KDP GÜVENLİ ALANI ⭑ ──")
        print("  %-26s %.3f in" % ("dış kenar asgarisi", sa["edgeMinIn"]))
        print("  %-26s %.3f in" % ("sırt asgarisi (ön metin)", sa["spineMinIn"]))
        print("  %-26s %.3f … %.3f in" % ("ön kapak bandı", fl, fr))
        print("  %-26s %.3f … %.3f in" % ("arka kapak bandı", bl, br))
        print("  %-26s %.3f … %.3f in" % ("dikey band", vb, vt))
        # ⚠ PAY **KDP'NİN EŞİĞİNE** GÖRE RAPORLANIR, BİZİM BANDIMIZA
        # GÖRE DEĞİL. Kendi payımıza göre ölçmek, bandı genişletince
        # sayının kendiliğinden düzelmesi demektir — kapının kendi
        # kendini yeşil yakması. İç blokta aynı ders alınmıştı.
        emin, smin = sa["edgeMinIn"], sa["spineMinIn"]
        worst = (None, None)
        for m in info["typeMeasured"]:
            box, lab = m.get("boxIn"), m.get("label")
            if not box or lab not in FRONT | BACK:
                continue
            x0, y0, x1, y1 = box
            if lab in FRONT:
                gaps = [x0 - (front_spine_edge + smin), (W - x1) - emin]
            else:
                gaps = [x0 - emin, (spine_left_edge - smin) - x1]
            gaps += [y0 - emin, (H - y1) - emin]
            g = min(gaps)
            if worst[0] is None or g < worst[0]:
                worst = (g, lab)
        if worst[0] is not None:
            print("  %-26s %+.3f in (%s) — KDP eşiğine göre"
                  % ("en dar pay", worst[0], worst[1]))

    rep.check(info["spineIn"] > 0.06,
              "sırt yazı basmaya yeter (%.4f in)" % info["spineIn"])
    rep.check(os.path.isfile(out) and open(out, "rb").read(4) == b"%PDF",
              "geçerli PDF üretildi")
    # ⚠ EŞİK NEDEN 60 VE NEDEN KIRMIZI DEĞİL:
    # Dosya ölçü olarak GEÇERLİDİR ve KDP kabul eder — sorun kabul
    # değil, GÖRÜNÜM. Bunu kırmızı yakmak, üretilebilir bir dosyayı
    # üretmemek olurdu; sessiz geçmek ise kurucuya yumuşak basılacak
    # bir kapağı haber vermemek. Doğrusu: ölç, yüksek sesle söyle,
    # üretmeye devam et. 60 dpi altı ise gerçekten kullanılamaz.
    rep.check(info["nativeDpi"] >= 60,
              "sanat asgari kullanılabilirlikte (%.1f dpi ≥ 60)"
              % info["nativeDpi"])
    if info["nativeDpi"] < 300:
        rep.warn("⚑ SANAT DOĞAL %.0f dpi — 300'e yükseltildi ama kazanılan "
                 "detay TAHMİNDİR; baskıda YUMUŞAK görünebilir. Gereken: "
                 "%d × %d px (bkz. COVER_ARTWORK_GENERATION_GUIDE)"
                 % (info["nativeDpi"], round(info["widthIn"] * 300),
                    round(info["heightIn"] * 300)))

    stats = STATS if args.binding == "paperback" else STATS.replace(
        "cover.json", "cover-hardcover.json")
    rep.facts.update(info)
    rep.facts["art"] = args.art
    rep.facts.pop("typeMeasured", None)
    rep.facts["typeRows"] = len(info["typeMeasured"])
    return rep.finish("%s · sırt %.4f in · en zayıf karşıtlık %.2f"
                      % (args.binding, info["spineIn"],
                         info["worstContrast"]), stats)


if __name__ == "__main__":
    sys.exit(main())
