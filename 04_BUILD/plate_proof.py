#!/usr/bin/env python3
"""
LEVHA PROVA PAKETİ — kurucuya devredilen fiziksel testin hazırlığı
================================================================================
⚠ BU BETİK BİR PROVA SİPARİŞ ETMEZ VE BİR PROVA SONUCU ÜRETMEZ.

A9 kurucu işidir. Ajan üç şeyi YAPAMAZ ve yapmayacaktır: provayı sipariş
etmek, yapıldığını iddia etmek, ölçüm uydurmak. Ajanın yapabileceği ve
yaptığı şey, provanın ALINABİLİR hâle gelmesidir:

  · baskıya hazır dosya      (6×9 trim · gerçek iç blok ölçüsü)
  · kontrol listesi          (neye bakılacak, hangi ölçüt)
  · devir talimatı           (kurucu ne yapacak)

Ve üç durum HER RAPORDA ayrılır — birleştirilmeleri yasaktır:

  SCREEN-TESTED             ekranda çözüldü            → ön eleme
  PAPER-TESTED              lazer baskıda çözüldü      → pilot için yeterli
  PHYSICAL-PROOF-VALIDATED  POD prova kopyada ölçüldü  → Faz 5 · YAPILMADI

⚠ VE PİLOTTA İKİNCİ BİR İKAME DAHA VAR: pilot levhaları GRAVÜR DEĞİL,
TİPOGRAFİK ŞEKİLDİR. Yani bu paket bulmacaların MANTIĞINI kâğıtta test
eder; gravürün nokta yayılması altındaki davranışını ETMEZ. O ölçüm
~110 levha üretildikten sonra, Faz 5'te yapılır.

Bağımlılık: reportlab (04_BUILD/requirements.txt). Yoksa çıkış kodu 2 —
bu bir kalite düşüşü DEĞİLDİR, atlanmış bir üretim adımıdır.

Çıkış kodları:  0 = paket üretildi   1 = hata   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
# ⚠ 08_OUTPUT DEĞİL. Orası YAYIN paketidir ve içinde çözüm bulunması Faz 6'da
# kırmızıdır (qa_solution_leak § yayın paketi). Prova paketi bulmaca taşır,
# dolayısıyla korumalı katmana aittir.
PROOF_DIR = os.path.join(pl.ROOT, "02_MANUSCRIPT", "PROOF")
CHECKLIST = os.path.join(pl.ROOT, "06_REPORTS", "tracked",
                         "plate-proof-checklist.md")

TRIM_W_IN, TRIM_H_IN = 6.0, 9.0
MARGIN_IN = 0.75


def build_pdf(book: dict) -> str:
    from reportlab.lib.pagesizes import inch                   # noqa: E402
    from reportlab.pdfgen import canvas                        # noqa: E402

    os.makedirs(PROOF_DIR, exist_ok=True)
    path = os.path.join(PROOF_DIR, "pilot-plates-proof.pdf")
    W, H = TRIM_W_IN * inch, TRIM_H_IN * inch
    M = MARGIN_IN * inch
    c = canvas.Canvas(path, pagesize=(W, H))

    def page_header(title: str, sub: str = "") -> float:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, H - M, title)
        if sub:
            c.setFont("Helvetica", 7.5)
            c.drawString(M, H - M - 12, sub)
        c.setLineWidth(0.4)
        c.line(M, H - M - 20, W - M, H - M - 20)
        return H - M - 36

    def mono_block(text: str, y: float, size: float) -> float:
        c.setFont("Courier", size)
        for line in text.splitlines():
            if y < M:
                c.showPage()
                y = page_header("(devam)")
            c.drawString(M, y, line)
            y -= size * 1.18
        return y

    # ── kapak ────────────────────────────────────────────────────────────
    y = page_header("CODEX ENIGMATICA · PİLOT LEVHA PROVASI",
                    "Kapı I · Eşik · Türkçe pilot · 6×9 in trim")
    c.setFont("Helvetica", 8.5)
    for line in [
        "",
        "BU DOSYA BIR PROVA SONUCU DEGILDIR. Bir prova ALMAK icindir.",
        "",
        "Durum:  SCREEN-TESTED       — ekranda cozuldu (on eleme)",
        "        PAPER-TESTED        — bu dosya basildiginda kazanilir",
        "        PHYSICAL-PROOF-VALIDATED — YAPILMADI (Faz 5 · A9)",
        "",
        "Pilot levhalari GRAVUR DEGIL, TIPOGRAFIK SEKILDIR. Bu paket",
        "bulmacalarin MANTIGINI kagitta test eder; gravurun nokta",
        "yayilmasi altindaki davranisini ETMEZ.",
        "",
        "Kontrol listesi: 06_REPORTS/tracked/plate-proof-checklist.md",
    ]:
        c.drawString(M, y, line)
        y -= 12

    # ── araçlar levhası ─────────────────────────────────────────────────
    charts = book.get("toolsPlate", {})
    alpha = charts.get("esik-alfabesi", {})
    c.showPage()
    y = page_header("ARAÇLAR LEVHASI · Çizelge A — Eşik Alfabesi",
                    "En kucuk ayirt edilmesi gereken detay: bir isaret.")
    rows = alpha.get("table", [])
    c.setFont("Courier", 7)
    for i in range(0, len(rows), 3):
        line = "   ".join("%-2s %-14s" % (r["letter"], r["glyph"])
                          for r in rows[i:i + 3])
        c.drawString(M, y, line)
        y -= 10

    lex = charts.get("esik-sozlugu", {}).get("entries", [])
    c.showPage()
    y = page_header("ARAÇLAR LEVHASI · Çizelge B — Eşik Sözlüğü")
    c.setFont("Courier", 7.5)
    for i in range(0, len(lex), 4):
        c.drawString(M, y, "   ".join("%2d %-11s" % (e["no"], e["word"])
                                      for e in lex[i:i + 4]))
        y -= 11

    c.showPage()
    y = page_header("ARAÇLAR LEVHASI · Çizelge D ve E")
    c.setFont("Courier", 8)
    for e in charts.get("kapi-sozleri", {}).get("entries", []):
        c.drawString(M, y, "  " + e)
        y -= 12
    y -= 10
    for r in charts.get("esik-sayilari", {}).get("entries", []):
        c.drawString(M, y, "  %2d   %s   -> %d"
                     % (r["sira"], r["okuma"], r["sozlukNo"]))
        y -= 11

    # ── levhalar ────────────────────────────────────────────────────────
    n = 0
    for p in book.get("puzzles", []):
        fig = p.get("figure")
        if not fig:
            continue
        n += 1
        c.showPage()
        y = page_header("LEVHA %s · bulmaca %s"
                        % (p.get("plateId") or "—", p["puzzleId"]),
                        "Okunmasi gereken en kucuk detay bu sayfada ayirt "
                        "edilebiliyor mu?")
        size = 8 if max(len(l) for l in fig.splitlines()) < 60 else 6
        mono_block(fig, y, size)

    c.save()
    return path, n


CHECK_MD = """# LEVHA PROVA KONTROL LİSTESİ — Kapı I pilotu

> ⚠ **BU BELGE BİR PROVA SONUCU DEĞİLDİR.** Bir provanın nasıl
> okunacağını söyler. Ölçüm kurucu tarafından yapılır (A9).
>
> Üretildi: `04_BUILD/plate_proof.py` · Faz 2

---

## 0 · Durum — üçü asla birleştirilmez

| Durum | Anlamı | Pilot |
|---|---|---|
| `SCREEN-TESTED` | Ekranda çözüldü — **ön eleme** | ✔ 20/20 |
| `PAPER-TESTED` | Lazer baskıda çözüldü — pilot için yeterli | ⚑ **kurucu** |
| `PHYSICAL-PROOF-VALIDATED` | POD prova kopyada ölçüldü — **kanıt** | ⛔ **YAPILMADI** |

⚠ Ve pilot levhaları **gravür değil, tipografik şekildir**. Bu paket
bulmacaların **mantığını** kâğıtta test eder; gravürün baskı davranışını
**etmez**. O ölçüm Faz 5'e aittir.

---

## 1 · Kurucunun yapacağı

1. `02_MANUSCRIPT/PROOF/pilot-plates-proof.pdf` dosyasını **%100
   ölçekte**, küçültmeden bastırın. Kâğıt: mümkünse krem, 80–90 g.
2. Aşağıdaki her satırı **basılı sayfada** işaretleyin.
3. Bir satır düşerse ilgili bulmaca **çözülemez** demektir; onu rapora
   yazın ve bulmacayı yeniden tasarlanacaklar listesine koyun.
4. Sonucu `06_REPORTS/tracked/plate-print-test.json` olarak kaydedin.

---

## 2 · Levha başına ölçüt

| Levha | Bulmaca | Ayırt edilmesi gereken en küçük şey | ✓ |
|---|---|---|---|
| pl-g1-01 | g1-001 | Kemer tepesindeki **bir** ile **iki** elmas arasındaki fark | ☐ |
| pl-g1-02 | g1-002 | Gaga yönü: sola bakan ile sağa bakan kuş | ☐ |
| pl-g1-03 | g1-003 | **Aralıklı işaret sayımı**: dört işaret ile beş işaret | ☐ |
| pl-g1-04 | g1-004 | Halka konturundaki **ince kesik** | ☐ |
| pl-g1-05 | g1-007 | Sütun çentiklerinin sayısı ve sütun numarası | ☐ |
| pl-g1-06 | g1-008 | Kenar oyuk kümeleri ve **çapa işaretinin köşesi** | ☐ |
| pl-g1-07 | g1-012 | Dikey söve işaretleri ve **alttaki ok yönü** | ☐ |
| pl-g1-08 | g1-014 | Basamak ön kenarındaki bir/iki oyuk | ☐ |
| pl-g1-09 | g1-016 | Koyu karo sayısı ve **çatlak karo** | ☐ |
| pl-g1-10 | g1-020 | On dokuz satırlık konum/grup çizelgesi | ☐ |

---

## 3 · ⭑ En yüksek riskli üç ölçüt ⭑

Bunlar düşerse bulmaca çözülemez ve **öldürme kapısı yanlış ölçer**.

| # | Risk | Neden |
|---|---|---|
| **1** | **Dört işaret ile beş işaretin ayırt edilmesi** | Ç/D ve T/U yalnızca sayımla ayrılır. İç çözücü bunu bir **sayma yorgunluğu riski** olarak bildirdi; işaretler bu yüzden **aralıklı** basılır. Kâğıtta aralık kapanıyorsa mekanik kırılır. |
| **2** | **Halka konturundaki kesik** | Kesik, nokta yayılmasının kapatabileceği en küçük detaydır. Kapanırsa yedi halkanın yedisi de "kapalı" görünür ve bulmacanın tek ayırıcı yüklemi yok olur. |
| **3** | **Çatlak karo ile koyu karo** | İkisi de koyu sayılır (metin bunu söyler) ama çatlak **görülebilmelidir**: okumanın başlangıç noktasını o belirler. |

---

## 4 · Kayıt biçimi

```json
{
  "date": "YYYY-AA-GG",
  "medium": "laser | POD-proof",
  "paper": "krem 90g",
  "plates": [{"plateId": "pl-g1-01", "legible": true, "note": ""}],
  "failures": [],
  "verdict": "PAPER-TESTED | PHYSICAL-PROOF-VALIDATED | FAILED"
}
```

⚠ `verdict` alanına `PHYSICAL-PROOF-VALIDATED` **yalnızca gerçek bir POD
prova kopyası** ölçüldüyse yazılır. Lazer baskı `PAPER-TESTED`tir.
"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  LEVHA PROVA PAKETİ · Kapı I pilotu")
    print("=" * 74)

    book = pl.load_json(BOOK)
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "prova paketi üretilemedi")
        return 0

    try:
        import reportlab                                       # noqa: F401
    except ImportError:
        print("\n  ⊘ reportlab yok — prova PDF'i ATLANDI")
        print("     pip install -r 04_BUILD/requirements.txt")
        os.makedirs(os.path.dirname(CHECKLIST), exist_ok=True)
        with open(CHECKLIST, "w", encoding="utf-8") as fh:
            fh.write(CHECK_MD)
        print("  ✍ kontrol listesi yine de yazıldı: %s"
              % os.path.relpath(CHECKLIST, pl.ROOT))
        return 2

    if args.check:
        ok = os.path.exists(os.path.join(PROOF_DIR, "pilot-plates-proof.pdf"))
        print("\n  prova paketi %s" % ("VAR" if ok else "YOK"))
        return 0 if ok else 1

    path, n = build_pdf(book)
    os.makedirs(os.path.dirname(CHECKLIST), exist_ok=True)
    with open(CHECKLIST, "w", encoding="utf-8") as fh:
        fh.write(CHECK_MD)

    print("\n  ✍ %s  (%d levha · %.1f KB)"
          % (os.path.relpath(path, pl.ROOT), n, os.path.getsize(path) / 1024))
    print("  ✍ %s" % os.path.relpath(CHECKLIST, pl.ROOT))
    print("\n" + "=" * 74)
    print("  ⚑ KURUCU EYLEMİ GEREKİYOR — prova ALINMADI, ALINABİLİR hâle geldi")
    print("     durum: SCREEN-TESTED · PHYSICAL-PROOF-VALIDATED DEĞİL")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
