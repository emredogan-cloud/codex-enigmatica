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

    measured = []

    def fit(txt, font, maxw_in, start, floor=9):
        sz = start
        while sz > floor and pdfmetrics.stringWidth(txt, font, sz) > maxw_in * inch:
            sz -= 0.5
        return sz

    def plan(txt, bold, size_pt, cx_in, y_in, label, rot=False):
        """⭑ ÖLÇ, MÜREKKEBİ SEÇ, HÂLEYİ HAZIRLA ⭑ — sanat üstünde."""
        if not txt:
            return None
        r = CT.place(im, txt, BOLD if bold else REG,
                     max(6, int(round(size_pt * PPI / 72.0))),
                     *px(cx_in, y_in), rotate=rot)
        r.update(text=txt, label=label, sizePt=round(size_pt, 1))
        measured.append(r)
        return r

    title = (meta.get("title") or "").upper()
    author = (meta.get("author") or "").upper()
    pub = meta.get("publisher") or ""
    sub = meta.get("subtitle") or ""

    t_size = fit(title, "C-B", G["front_w"] - 2 * SAFE - 0.30, 46, 16)
    t_y = H - edge - 1.45
    r_title = plan(title, True, t_size, fcx, t_y, "ön başlık")

    sub_lines = []
    if sub:
        words, line = sub.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, "C", 13) > (G["front_w"] - 1.35) * inch:
                sub_lines.append(line)
                line = w
            else:
                line = t
        sub_lines.append(line)
    r_sub = []
    sy = t_y - 0.62
    for ln in sub_lines[:3]:
        r_sub.append(plan(ln, False, 13, fcx, sy, "alt başlık"))
        sy -= 0.27

    a_y = edge + 0.95
    r_auth = plan(author, True, 21, fcx, a_y, "ön yazar")
    r_pub = plan(pub, False, 10.5, fcx, edge + 0.60, "yayıncı")

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
    bx0 = back_x0 + SAFE + 0.28
    bx1 = back_x0 + G["front_w"] - SAFE - 0.10
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

    by = H - edge - 1.30
    stop = edge + SAFE + G["barcode_h"] + 0.30
    back_rows = []
    for ln in lines:
        if by < stop:
            break
        if ln:
            w_in = pdfmetrics.stringWidth(ln, "C", fs) / inch
            r = CT.place(im, ln, REG, max(6, int(round(fs * PPI / 72.0))),
                         *px(bx0 + w_in / 2, by))
            r.update(text=ln, label="arka kopya", sizePt=fs)
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

    def draw_c(r, cx_in, y_in, font):
        centred(r, cx_in, y_in, font)

    draw_c(r_title, fcx, t_y, "C-B")
    sy = t_y - 0.62
    for r in r_sub:
        draw_c(r, fcx, sy, "C")
        sy -= 0.27
    draw_c(r_auth, fcx, a_y, "C-B")
    draw_c(r_pub, fcx, edge + 0.60, "C")

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
    inter = (pl.load_json(INTERIOR) or {}).get("facts") or {}
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
