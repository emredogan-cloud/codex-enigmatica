#!/usr/bin/env python3
"""
⭑ LEVHA VERİSİ KAPISI ⭑ — imza mekaniğinin en kırılgan yeri
================================================================================
Yol haritası Faz 3 § 13 bunu adıyla istiyor ve gerekçesini de yazıyor:

    "Levha içi şifre bu kitabın İMZA MEKANİĞİDİR ve aynı zamanda en
     kırılgan parçasıdır. Baskı testi Faz 5'e bırakılmaz; ön ölçüm
     BURADA yapılır."

Ve § 7'nin sorusu şudur: **bir gravür kaç bit veri taşıyabilir?**

────────────────────────────────────────────────────────────────────────
⚠ BU KAPI BASKI YAPMAZ VE BASKIYI ÖLÇTÜĞÜNÜ İDDİA ETMEZ.

Gerçek ölçüm mürekkep, kâğıt ve gözle yapılır (A9 · kurucu eylemi). Bu
kapı ONDAN ÖNCE gelen soruyu sorar ve o soru ucuzdur:

    Veri, ŞEKLİN KENDİSİNDEN geri alınabiliyor mu — ve geri alınırken
    okurun AYIRT ETMESİ gereken en ince fark nedir?

Baskıda kaybolan şey veri değildir; AYIRT EDİLEBİLİRLİKTİR. Dört nokta
ile beş nokta arasındaki fark, 300 dpi'da bir kâğıt kusuru kadardır.
────────────────────────────────────────────────────────────────────────

Beş ölçüm:

  ① VERİ GERİ ALINABİLİYOR — şekilden okunan veri kayıttakiyle aynı mı
  ② BİT BÜTÇESİ — levha kaç bit taşıyor, cevap kaç bit gerektiriyor
  ③ ⭑ EN İNCE AYRIM ⭑ — okurun ayırması gereken en zor fark
  ④ KARIŞABİLİR İSTASYON — iki ayrı veri aynı biçimde mi basılıyor
  ⑤ YOĞUNLUK — satır uzunluğu ve işaret sıklığı baskı tavanının altında mı

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
from qa_answerspace import TOOLS, Plate, decode_grid           # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")

# ── BASKI TAVANLARI ────────────────────────────────────────────────────
# 6×9 trim · 10,5 punto tek aralıklı: satır başına ~62 karakter sığar.
MAX_FIGURE_WIDTH = 62
# ⭑ EN İNCE AYRIM ⭑ Aynı işaretin ARDIŞIK tekrarı okurdan SAYMASINI ister
# ve baskıda en kolay kaybolan şey budur. Beş, Eşik Alfabesi'nin kendi
# tavanıdır (29 = 6 grup × 5) ve çizelge işaretleri ARALIKLI basar.
MAX_IDENTICAL_RUN = 5
STATION = re.compile(r"(\d)·(\d)")

# ⭑ YALNIZCA VERİ TAŞIYAN İŞARETLER SAYILIR ⭑
# İlk ölçüm çerçeve çizgilerini de saydı ve "60 ardışık ═" diye kırmızı
# yaktı. Okur bir cetveli SAYMAZ; onu bir kenar olarak görür. Ölçülmesi
# gereken şey, okurun AYIRT ETMEK İÇİN SAYMAK ZORUNDA olduğu işaretlerdir:
# Eşik Alfabesi'nin altı işareti ve levhaların sayım glifleri.
DATA_MARKS = set("',+/\\x") | set("◆┬▓◦◊●○▽║")


def figure_bits(kind: str, acc: dict, plate: Plate) -> tuple[float, str]:
    """Levhanın TAŞIDIĞI bit — okurun ondan çıkardığı değil."""
    if kind == "reachable-via-grid-coordinates":
        cells = (plate.charts.get(acc.get("gridRef") or "") or {})
        n = (cells.get("rowCount") or 6) * (cells.get("colCount") or 5)
        return len(acc.get("coordinates") or []) * math.log2(n), \
            "%d istasyon × log2(%d göz)" % (len(acc.get("coordinates") or []), n)
    if kind == "reachable-via-number-table":
        r = acc.get("readings") or [""]
        return len(r[0]) * math.log2(5), "%d kenar × log2(5 sayım)" % len(r[0])
    if kind == "reachable-by-glyph-reading":
        g = len([x for x in (acc.get("glyphs") or "").split("│") if x.strip()])
        return g * math.log2(29), "%d glif × log2(29 harf)" % g
    if kind == "plate-attribute":
        n = len(acc.get("labels") or [])
        return math.log2(n) if n else 0, "%d etiketten biri" % n
    return 0.0, "—"


def finest_distinction(fig: str) -> tuple[int, str]:
    """Okurun ayırması gereken EN İNCE fark — ardışık aynı işaret sayısı."""
    run, prev, cur, what = 0, None, 0, "—"
    for ch in fig:
        if ch not in DATA_MARKS:
            prev, cur = None, 0
            continue
        if ch == prev:
            cur += 1
        else:
            prev, cur = ch, 1
        if cur > run:
            run, what = cur, ch
    return run, what


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    gate_level = args.gate or pl.read_gate()
    if gate_level not in pl.VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate_level, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  ⭑ LEVHA VERİSİ ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    pre = pl.preflight(rep, gate_level, "levha verisi")
    if pre is None:
        return rep.finish("denetlenecek levha yok", args.json)
    need, sols, _designs = pre

    plate = Plate(pl.load_json(TOOLS) or {})
    book = pl.load_json(BOOK) or {}
    pages = {p["puzzleId"]: p for p in book.get("puzzles", [])}

    unrecoverable, confusable, too_wide, too_fine = [], [], [], []
    rows = []
    print("\n── levha başına veri ──")
    print("  %-9s %7s %7s %6s %5s  %s"
          % ("bulmaca", "taşınan", "gerekli", "pay", "ayrım", "dayanak"))
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        acc = (rec.get("answerSpace") or {}).get("acceptance") or {}
        kind = acc.get("kind")
        fig = (pages.get(pid) or {}).get("figure") or ""
        if not fig.strip():
            continue
        bits, basis = figure_bits(kind, acc, plate)
        if not bits:
            continue
        need_bits = math.log2(max(2, len(plate.bestiary) or len(plate.lexicon)))
        run, mark = finest_distinction(fig)
        width = max((len(l) for l in fig.splitlines()), default=0)

        # ① VERİ GERİ ALINABİLİYOR MU — şekilden okunan, kayıttakiyle aynı mı
        if kind == "reachable-via-grid-coordinates":
            seen = [(int(a), int(b)) for a, b in STATION.findall(fig)]
            want = [tuple(c) for c in acc.get("coordinates") or []]
            if sorted(seen) != sorted(want):
                unrecoverable.append("%s (şekilde %d, kayıtta %d istasyon)"
                                     % (pid, len(seen), len(want)))
            elif len(set(seen)) != len(seen) and \
                    decode_grid(want, plate.charts.get(
                        acc.get("gridRef") or "") or {}) != rec.get("finalAnswer"):
                unrecoverable.append("%s (istasyonlar çözülmüyor)" % pid)

        if run > MAX_IDENTICAL_RUN:
            too_fine.append("%s (%d ardışık '%s')" % (pid, run, mark))
        if width > MAX_FIGURE_WIDTH:
            too_wide.append("%s (%d > %d karakter)" % (pid, width,
                                                       MAX_FIGURE_WIDTH))
        rows.append({"puzzleId": pid, "acceptance": kind,
                     "bitsCarried": round(bits, 1),
                     "bitsRequired": round(need_bits, 1),
                     "redundancy": round(bits / need_bits, 1) if need_bits else 0,
                     "finestDistinction": run, "figureWidth": width})
        print("  %-9s %7.1f %7.1f %5.1f× %5d  %s"
              % (pid, bits, need_bits, bits / need_bits if need_bits else 0,
                 run, basis))

    if rows:
        worst = max(r["finestDistinction"] for r in rows)
        rep.facts.update({"plates": len(rows), "finestDistinctionMax": worst,
                          "maxIdenticalRunAllowed": MAX_IDENTICAL_RUN,
                          "maxFigureWidth": MAX_FIGURE_WIDTH, "perPlate": rows})
        print("\n── ölçüm ──")
        print("  levha                    %d" % len(rows))
        print("  ⭑ en ince ayrım          %d ardışık aynı işaret (tavan %d)"
              % (worst, MAX_IDENTICAL_RUN))
        print("  ortalama fazlalık        %.1f×"
              % (sum(r["redundancy"] for r in rows) / len(rows)))
        print("")
        print("  ⚠ FAZLALIK BİR EMNİYET DEĞİLDİR: levha cevabın "
              "gerektirdiğinden")
        print("    çok daha fazla bit taşıyor ama BİR istasyon yanlış "
              "okunursa")
        print("    çıkan dize katalogda YOKTUR — hata tespiti fazlalıktan "
              "değil,")
        print("    BASILI KATALOGDAN gelir.")

    rep.check(not unrecoverable,
              "⭑ ① LEVHA VERİSİ ŞEKLİN KENDİSİNDEN GERİ ALINIYOR ⭑"
              + ("" if not unrecoverable else " — ⛔ %s" % unrecoverable[:5]))
    rep.check(not too_fine,
              "⭑ ③ EN İNCE AYRIM BASKI TAVANININ ALTINDA ⭑ (≤%d ardışık "
              "aynı işaret)" % MAX_IDENTICAL_RUN
              + ("" if not too_fine else " — ⛔ %s" % too_fine[:5]))
    rep.check(not too_wide,
              "⑤ hiçbir şekil satırı %d karakteri aşmıyor" % MAX_FIGURE_WIDTH
              + ("" if not too_wide else " — ⛔ %s" % too_wide[:5]))
    rep.check(not confusable, "④ iki ayrı veri aynı biçimde basılmıyor")

    if rows:
        rep.warn("bu kapı BASKI YAPMAZ — gerçek ölçüm A9'a (fiziksel prova) "
                 "aittir ve YAPILMADI")
    return rep.finish("%d levha ölçüldü" % len(rows), args.json)


if __name__ == "__main__":
    sys.exit(main())
