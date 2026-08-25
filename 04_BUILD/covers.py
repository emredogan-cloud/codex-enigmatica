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
DEFAULT_ART = "codex-enigmatica-wrap-cover-option-01.png"


def spine_in(pages: int, paper: str) -> float:
    return pages * PAPER_IN.get(paper, PAPER_IN["cream"])


def build(art: str, pages: int, paper: str, meta: dict, path: str) -> dict:
    from PIL import Image
    from reportlab.lib.pagesizes import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    sp = spine_in(pages, paper)
    W = (BLEED + TRIM_W + sp + TRIM_W + BLEED)
    H = (BLEED + TRIM_H + BLEED)
    Wp, Hp = W * inch, H * inch

    F = "/usr/share/fonts/truetype/dejavu"
    pdfmetrics.registerFont(TTFont("C", os.path.join(F, "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("C-B",
                                   os.path.join(F, "DejaVuSerif-Bold.ttf")))

    # ── SANAT: tam sarmal orana KIRPILIR ───────────────────────────────
    # ⚠ Teslim edilen sanat 2,15:1; gereken oran ~1,40:1. Merkezden
    # kırpmak, arka ve ön kapağın DIŞ kenarlarını kaybettirir. Bu bir
    # taviz olarak yapılır ve raporda öyle bildirilir.
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

    target_px = int(W * 300)
    if im.width < target_px:
        im = im.resize((target_px, int(round(target_px / want))),
                       Image.LANCZOS)

    cv = canvas.Canvas(path, pagesize=(Wp, Hp))
    # ⚠ KURUCU DEĞERLERİ GÖMÜLMEZ (tek doğruluk kaynağı:
    # project_config.json → metadata.json). Buraya bir yazar adı ya da
    # yayıncı yazmak, iki yerde yaşayan ve sessizce ayrışan bir gerçek
    # üretir; `validate_structure` bunu kapı olarak zorlar.
    cv.setTitle(meta.get("title") or "")
    cv.drawImage(ImageReader(im), 0, 0, width=Wp, height=Hp)

    # ── koordinatlar ───────────────────────────────────────────────────
    back_x0 = BLEED * inch
    spine_x0 = (BLEED + TRIM_W) * inch
    front_x0 = (BLEED + TRIM_W + sp) * inch
    pale = (0.97, 0.95, 0.90)
    dark = (0.10, 0.08, 0.06)

    # ⭑ MÜREKKEP RENGİ ZEMİNDEN ÖLÇÜLÜR ⭑
    # ⚠ İlk denemede arka kapak metni AÇIK bir zemin üstüne AÇIK renkle
    # basıldı ve okunmuyordu. Sabit bir renk seçmek, sanatın hangi
    # bölgesinin açık hangisinin koyu olduğunu bilmemek demektir.
    # Zeminin parlaklığı ölçülür; metin ona göre koyu ya da açık olur.
    ipx = im.convert("L")

    def luma(x0, y0, x1, y1):
        """PDF koordinatlarındaki kutunun ortalama parlaklığı (0-255)."""
        sx, sy = ipx.width / Wp, ipx.height / Hp
        box = (max(0, int(x0 * sx)), max(0, int((Hp - y1) * sy)),
               min(ipx.width, max(1, int(x1 * sx))),
               min(ipx.height, max(1, int((Hp - y0) * sy))))
        if box[2] <= box[0] or box[3] <= box[1]:
            return 128
        c = ipx.crop(box)
        h = c.histogram()
        tot = sum(h) or 1
        return sum(i * v for i, v in enumerate(h)) / tot

    def fit(txt, font, maxw, start, floor=9):
        """⭑ BAŞLIK PANELE SIĞDIRILIR ⭑ — taşan başlık kesilmiş başlıktır."""
        sz = start
        while sz > floor and pdfmetrics.stringWidth(txt, font, sz) > maxw:
            sz -= 0.5
        return sz

    def shadowed(txt, font, size, cx, y, force=None):
        cv.setFont(font, size)
        w = pdfmetrics.stringWidth(txt, font, size)
        bg = luma(cx - w / 2, y - size * 0.3, cx + w / 2, y + size)
        col = force or (dark if bg > 150 else pale)
        sh = (1, 1, 1) if col is dark else (0.03, 0.02, 0.02)
        cv.setFillColorRGB(sh[0], sh[1], sh[2], alpha=0.5)
        cv.drawCentredString(cx + 1.1, y - 1.1, txt)
        cv.setFillColorRGB(*col)
        cv.drawCentredString(cx, y, txt)

    # ── ÖN KAPAK ───────────────────────────────────────────────────────
    fcx = front_x0 + TRIM_W * inch / 2
    title = (meta.get("title") or "CODEX ENIGMATICA").upper()
    tw_max = (TRIM_W - 2 * SAFE - 0.35) * inch
    tsize = fit(title, "C-B", tw_max, 46, 18)
    shadowed(title, "C-B", tsize, fcx, Hp - (BLEED + 1.45) * inch)
    sub = meta.get("subtitle") or ""
    if sub:
        words, line, lines = sub.split(), "", []
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, "C", 13) > (TRIM_W - 1.3) * inch:
                lines.append(line)
                line = w
            else:
                line = t
        lines.append(line)
        y = Hp - (BLEED + 2.05) * inch
        for ln in lines[:3]:
            shadowed(ln, "C", 13, fcx, y)
            y -= 19
    author = (meta.get("author") or "").upper()
    shadowed(author, "C-B", 21, fcx, (BLEED + 0.95) * inch)
    shadowed(meta.get("publisher") or "", "C", 10.5, fcx,
             (BLEED + 0.60) * inch)

    # ── SIRT ───────────────────────────────────────────────────────────
    # ⚠ KDP sırta yazı için ASGARİ 0,0625 inç ister; altında yazı basılmaz.
    spine_ok = sp >= 0.0625
    if spine_ok:
        cv.saveState()
        cv.translate(spine_x0 + sp * inch / 2, Hp / 2)
        cv.rotate(-90)
        cv.setFillColorRGB(*pale)
        size = 15 if sp >= 0.5 else 11
        cv.setFont("C-B", size)
        cv.setFillColorRGB(0.05, 0.04, 0.03, alpha=0.55)
        cv.drawCentredString(1.0, -size * 0.34 - 1.0, title)
        cv.setFillColorRGB(*pale)
        cv.drawCentredString(0, -size * 0.34, title)
        cv.setFont("C", size * 0.62)
        cv.drawCentredString(0, -size * 0.34 - size * 1.45, author)
        cv.restoreState()

    # ── ARKA KAPAK ─────────────────────────────────────────────────────
    desc = (meta.get("description") or "").strip()
    # ⚠ Arka kapak metni SIRTA GİRMEMELİ: sağ sınır, sırtın başladığı
    # yerden SAFE kadar geride biter. İlk denemede metin sırta taşıyordu.
    bx0 = back_x0 + (SAFE + 0.28) * inch
    bx1 = spine_x0 - SAFE * inch
    bw = bx1 - bx0
    fs = 10.0
    y = Hp - (BLEED + 1.35) * inch

    def line_out(txt, yy):
        w = pdfmetrics.stringWidth(txt, "C", fs)
        bg = luma(bx0, yy - fs * 0.3, bx0 + w, yy + fs)
        col = dark if bg > 150 else pale
        sh = (1, 1, 1) if col is dark else (0.03, 0.02, 0.02)
        cv.setFillColorRGB(sh[0], sh[1], sh[2], alpha=0.45)
        cv.drawString(bx0 + 0.9, yy - 0.9, txt)
        cv.setFillColorRGB(*col)
        cv.drawString(bx0, yy, txt)

    cv.setFont("C", fs)
    stop = (BLEED + SAFE) * inch + 1.2 * inch + 0.25 * inch   # barkod üstü
    for block in desc.split("\n\n"):
        words, line = block.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, "C", fs) > bw:
                line_out(line, y)
                y -= fs * 1.5
                line = w
            else:
                line = t
        if line:
            line_out(line, y)
            y -= fs * 1.5
        y -= fs * 0.7
        if y < stop:
            break

    # ⚠ BARKOD ALANI BOŞ BIRAKILIR — KDP kendi basar ve numara
    # UYDURULMAZ. 2,0 × 1,2 inçlik alan arka kapağın sağ altındadır.
    bar_w, bar_h = 2.0 * inch, 1.2 * inch
    bar_x = back_x0 + TRIM_W * inch - SAFE * inch - bar_w
    bar_y = (BLEED + SAFE) * inch

    cv.showPage()
    cv.save()
    return {"spineIn": round(sp, 4), "widthIn": round(W, 4),
            "heightIn": round(H, 4), "pages": pages, "paper": paper,
            "artCropPx": [src_w, src_h],
            "barcodeBoxIn": [round(bar_x / inch, 3), round(bar_y / inch, 3),
                             2.0, 1.2],
            "spineTextPrinted": spine_ok}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--art", default=DEFAULT_ART)
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="ÜRETME — çıktı var mı ve ölçümle tutarlı mı")
    ap.add_argument("--out", default=os.path.join(OUTDIR, "cover.pdf"))
    args = ap.parse_args()

    print("=" * 74)
    print("  BASKI KAPAĞI · tam sarmal")
    print("=" * 74)

    try:
        import reportlab                                       # noqa: F401
        from PIL import Image                                  # noqa: F401
    except ImportError:
        print("⛔ reportlab / Pillow yok")
        return 2

    rep = pl.Report(args.verbose)
    meta = pl.load_json(META) or {}
    inter = pl.load_json(INTERIOR) or {}
    pages = args.pages or (inter.get("facts") or {}).get("pages") or 0

    rep.check(bool(pages),
              "⭑ SAYFA SAYISI ÖLÇÜLEN İÇ BLOKTAN GELDİ ⭑ (%s)"
              % (pages or "YOK — önce 04_BUILD/interior.py"))
    if not pages:
        return rep.finish("sayfa sayısı yok", None)

    paper = "cream"
    for ed in meta.get("editions") or []:
        if ed.get("id") == "paperback":
            paper = ed.get("paper") or "cream"

    art = os.path.join(RAW, args.art)
    rep.check(os.path.isfile(art), "sarmal sanat var (%s)" % args.art)
    if not os.path.isfile(art):
        return rep.finish("sanat yok", None)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    info = build(art, pages, paper, meta, args.out)

    print("\n── geometri ──")
    print("  %-26s %d" % ("sayfa (ölçülen)", pages))
    print("  %-26s %s" % ("kâğıt", paper))
    print("  %-26s %.4f in" % ("SIRT", info["spineIn"]))
    print("  %-26s %.3f × %.3f in" % ("tam kapak (taşma dâhil)",
                                      info["widthIn"], info["heightIn"]))
    print("  %-26s %.3f in" % ("taşma", BLEED))
    print("  %-26s %.1f MB" % ("PDF", os.path.getsize(args.out) / 1e6))

    rep.check(info["spineIn"] > 0.06,
              "sırt yazı basmaya yeter (%.4f in ≥ 0,0625)" % info["spineIn"])
    rep.check(abs(info["widthIn"] -
                  (2 * (TRIM_W + BLEED) + info["spineIn"])) < 1e-6,
              "tam genişlik = 2×(trim+taşma) + sırt")
    rep.check(abs(info["heightIn"] - (TRIM_H + 2 * BLEED)) < 1e-6,
              "tam yükseklik = trim + 2×taşma")
    rep.check(os.path.isfile(args.out), "kapak PDF üretildi")

    doc = open(args.out, "rb").read(2048)
    rep.check(doc.startswith(b"%PDF"), "geçerli PDF başlığı")

    rep.facts.update(info)
    rep.facts["art"] = args.art
    return rep.finish("sırt %.4f in" % info["spineIn"], STATS)


if __name__ == "__main__":
    sys.exit(main())
