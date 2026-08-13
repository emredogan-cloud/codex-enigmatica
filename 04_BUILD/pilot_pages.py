#!/usr/bin/env python3
"""
PİLOT SAYFA ÖLÇÜMÜ — modelin gerçek içerikle ilk yüzleşmesi
================================================================================
`page_budget.py` MODELİ denetler: bildirilen sayfalar türetilenle tutuyor mu.
Bu betik farklı bir soru sorar ve Faz 2'ye kadar sorulamazdı:

    MODEL GERÇEK İÇERİKLE TUTUYOR MU?

Faz 1'in sayfa modeli bir hipotezdi: kapı başına 34 sayfa, arka madde 44.
O hipotez tek bir bulmaca yazılmadan kuruldu. Şimdi yirmi bulmaca var ve
model ilk kez ÖLÇÜLEBİLİR.

Ve bu, bu kitapta bir dizgi meselesi DEĞİLDİR (K12): Kapı V bulmacaları
sayfa numaralarına dayanır. Yanlış bir sayfa modeli, Faz 5'te dizgi
donduğunda sekiz bulmacayı kırar — takvimin bittiği yerde.

⚠ Manuscript KORUMALI KATMANDADIR ve CI'da YOKTUR. Bu betik orada boş
koşar ve BUNU SÖYLER. Ölçüm yerelde yapılır; sonucu 06_REPORTS/tracked/
altına — SAYI olarak, metin olarak değil — yazılır.

Çıkış kodları:  0 = geçti   1 = ölçüm modelden saptı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
GATE_INDEX = os.path.join(pl.ROOT, "01_SOURCE", "gate_index.json")
OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "pilot-page-measure.json")

# Bir levha şekli sayfada ne kadar yer kaplar. 6×9 iç blokta bir kutulu
# şekil, satır sayısı + başlık + boşluk kadar yer alır; satır başına
# yaklaşık 1/42 sayfa (42 satır/sayfa) ve kutu için 4 satır pay.
LINES_PER_PAGE = 42
FIGURE_PADDING_LINES = 4


def words(*parts) -> int:
    n = 0
    for p in parts:
        if isinstance(p, list):
            n += sum(len(pl.words(str(x))) for x in p)
        elif p:
            n += len(pl.words(str(p)))
    return n


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  PİLOT SAYFA ÖLÇÜMÜ · Kapı I")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    pm = cfg.get("production", {}).get("pageModel", {})
    wpp = pm.get("backMatterDerivation", {}).get("wordsPerPage", 350)

    book = pl.load_json(BOOK)
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "ölçüm YAPILAMADI")
        rep.warn("pilot sayfa ölçümü BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    sols, _ = pl.load_protected()
    pages = book.get("puzzles", [])

    body_words = 0
    figure_lines = 0
    hint_words = 0
    solution_words = 0
    per_puzzle = []

    for p in pages:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        w = words(p.get("title"), p.get("objective"), p.get("readerAction"),
                  p.get("input"), p.get("clues"), p.get("constraints"))
        fl = 0
        for key in ("figure", "printedTable"):
            if p.get(key):
                fl += len(str(p[key]).splitlines()) + FIGURE_PADDING_LINES
        hw = words(rec.get("hints"))
        sw = words(rec.get("explanation"))
        body_words += w
        figure_lines += fl
        hint_words += hw
        solution_words += sw
        per_puzzle.append({"puzzleId": pid, "words": w, "figureLines": fl,
                           "hintWords": hw, "solutionWords": sw})

    # Araçlar levhası: ön maddede basılı çizelgeler
    charts = book.get("toolsPlate", {})
    chart_rows = sum(len(c.get("entries", c.get("table", [])))
                     for c in charts.values())
    chart_pages = round(chart_rows / (LINES_PER_PAGE * 3), 2)   # üç sütun

    body_pages = body_words / wpp + figure_lines / LINES_PER_PAGE
    hint_pages = hint_words / wpp
    sol_pages = solution_words / wpp

    gi = pl.load_json(GATE_INDEX) or {}
    declared = next((g.get("pageBudget", 0) for g in gi.get("gates", [])
                     if g.get("id") == "threshold"), 0)

    # Kitap ölçeğine yansıtma: Kapı I ölçümü × 5 kapı
    proj_body = body_pages * 5
    proj_hints = hint_pages * 5
    proj_sols = sol_pages * 5
    bm = pm.get("backMatter", {})
    declared_hints = bm.get("hintSection", 0)
    declared_sols = bm.get("solutionSection", 0)

    print("\n── Kapı I · ölçülen ──")
    print("  bulmaca metni      %5d kelime → %5.1f sayfa" % (body_words, body_words / wpp))
    print("  levha ve çizelge   %5d satır  → %5.1f sayfa" % (figure_lines, figure_lines / LINES_PER_PAGE))
    print("  ─────────────────────────────────────────────")
    print("  kapı gövdesi                      %5.1f sayfa   (bildirilen %d)"
          % (body_pages, declared))
    print("  araçlar levhası (ön madde)        %5.1f sayfa" % chart_pages)
    print("\n── arka madde · Kapı I payı ──")
    print("  ipuçları  %4d kelime → %4.1f sayfa   (kitap geneli %4.1f · bildirilen %d)"
          % (hint_words, hint_pages, proj_hints, declared_hints))
    print("  çözümler  %4d kelime → %4.1f sayfa   (kitap geneli %4.1f · bildirilen %d)"
          % (solution_words, sol_pages, proj_sols, declared_sols))

    rep.facts.update({
        "gate": "threshold", "puzzles": len(pages),
        "bodyWords": body_words, "figureLines": figure_lines,
        "hintWords": hint_words, "solutionWords": solution_words,
        "wordsPerPage": wpp,
        "measuredBodyPages": round(body_pages, 1),
        "declaredBodyPages": declared,
        "toolsPlatePages": chart_pages,
        "projectedBodyPages": round(proj_body, 1),
        "projectedHintPages": round(proj_hints, 1),
        "declaredHintPages": declared_hints,
        "projectedSolutionPages": round(proj_sols, 1),
        "declaredSolutionPages": declared_sols,
        "perPuzzle": per_puzzle,
    })

    # ⚠ ÖLÇÜM MODELİ AŞARSA KIRMIZI — MODELE UYDURULMAZ.
    # A8 kapandı ve yeniden açılmaz: sayfa hedefi bir dizgi sorununu yok
    # etmek için DEĞİŞTİRİLMEZ. Ölçüm modeli aşıyorsa içerik veya dizgi
    # düzeltilir ve YENİDEN ölçülür.
    rep.check(body_pages <= declared,
              "Kapı I gövdesi bildirilen bütçeye SIĞIYOR (%.1f ≤ %d)"
              % (body_pages, declared))
    rep.check(proj_hints <= declared_hints,
              "ipucu bölümü ölçekte bütçeye sığıyor (%.1f ≤ %d)"
              % (proj_hints, declared_hints))
    rep.check(proj_sols <= declared_sols,
              "çözüm bölümü ölçekte bütçeye sığıyor (%.1f ≤ %d)"
              % (proj_sols, declared_sols))

    # Bir kapının bütçesinin ÇOK ALTINDA kalması da bir bulgudur: sayfa
    # modeli Kapı V'i bağlar ve boş sayfa da yanlış sayfadır.
    if body_pages < declared * 0.5:
        rep.warn("Kapı I gövdesi bütçenin yarısından az (%.1f / %d) — "
                 "levha boyutları veya bulmaca başına sayfa yerleşimi "
                 "Faz 5'te yeniden ölçülmeli" % (body_pages, declared))

    return rep.finish("%d bulmaca ölçüldü" % len(pages), args.json)


if __name__ == "__main__":
    sys.exit(main())
