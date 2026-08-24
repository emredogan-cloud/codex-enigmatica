#!/usr/bin/env python3
"""
SAYFA ÖLÇÜMÜ — modelin gerçek içerikle yüzleşmesi
================================================================================
`page_budget.py` MODELİ denetler: bildirilen sayfalar türetilenle tutuyor mu.
Bu betik farklı bir soru sorar:

    MODEL GERÇEK İÇERİKLE TUTUYOR MU?

Faz 1'in sayfa modeli bir hipotezdi: kapı başına 34 sayfa, arka madde 44.
O hipotez tek bir bulmaca yazılmadan kuruldu. Artık yüz bir bulmaca var ve
model KAPI KAPI ölçülebilir.

────────────────────────────────────────────────────────────────────────
⚠ FAZ 4 · BU BETİK YANLIŞ ÖLÇÜYORDU VE YEŞİL YANIYORDU

Betik Faz 2'de yazıldı; o gün kitapta yalnızca Kapı I vardı. Bütün
`book.json` bulmacalarını topluyor, toplamı **Kapı I'in bütçesiyle**
karşılaştırıyor ve arka maddeyi **×5 ile ölçekliyordu**. İki kapı
yazıldığında ölçüm iki katına çıktı ve kimse fark etmedi; beş kapı
yazıldığında beş katına çıktı ve kapı KIRMIZI yandı — ölçülen içerik
büyüdüğü için değil, ÖLÇENİN kendisi bozuk olduğu için.

Ders Faz 2'nin dersiyle aynı: **bir kapı, ölçtüğü şeyin büyüdüğünü
varsaymalıdır.** Ölçüm artık kapı bazındadır ve hiçbir yerde ×5 yoktur.

⭑ VE ÖLÇÜLEN ŞEY METİNDİR, SAYFA DEĞİL ⭑ Bu kitapta her bulmacanın bir
GRAVÜR LEVHASI vardır ve levha sayfayı metinden bağımsız doldurur
(112 levha · `page_budget § levha bütçesi`). Bu yüzden ölçülen metin,
bildirilen bütçenin ALTINDA kalmalıdır — üstüne çıkarsa levhaya yer
kalmaz. Bütçenin çok altında kalması bir hata değil, levhaya ayrılmış
paydır; kapı bunu yine de SÖYLER.

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
    print("  SAYFA ÖLÇÜMÜ · ölçülen metin ↔ bildirilen model")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    pm = cfg.get("production", {}).get("pageModel", {})
    wpp = pm.get("backMatterDerivation", {}).get("wordsPerPage", 350)

    book = pl.load_json(BOOK)
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "ölçüm YAPILAMADI")
        rep.warn("sayfa ölçümü BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    sols, _ = pl.load_protected()
    pages = book.get("puzzles", [])
    gi = pl.load_json(GATE_INDEX) or {}
    budget = {g.get("id"): g.get("pageBudget", 0) for g in gi.get("gates", [])}
    order = [g.get("id") for g in gi.get("gates", [])]

    # ── ① BULMACA GÖVDESİ · KAPI KAPI ──────────────────────────────────
    body_w: dict = {}
    fig_l: dict = {}
    hint_words = solution_words = 0
    per_puzzle = []
    for p in pages:
        pid, gid = p["puzzleId"], p.get("gate") or "?"
        rec = sols.get(pid) or {}
        w = words(p.get("title"), p.get("objective"), p.get("readerAction"),
                  p.get("input"), p.get("clues"), p.get("constraints"),
                  p.get("flavour"))
        fl = 0
        for key in ("figure", "printedTable"):
            if p.get(key):
                fl += len(str(p[key]).splitlines()) + FIGURE_PADDING_LINES
        hw = words(rec.get("hints"))
        sw = words(rec.get("explanation"))
        body_w[gid] = body_w.get(gid, 0) + w
        fig_l[gid] = fig_l.get(gid, 0) + fl
        hint_words += hw
        solution_words += sw
        per_puzzle.append({"puzzleId": pid, "gate": gid, "words": w,
                           "figureLines": fl, "hintWords": hw,
                           "solutionWords": sw})

    # ── ② ISINMA · KENDİ KAPISINDA ─────────────────────────────────────
    # ⭑ Faz 4'te dokuz yeni örnek geldi ve hiçbiri ön maddede DEĞİL.
    # Ölçüm onları kendi kapılarına yazar; bütçeyi ısıtan yer orasıdır.
    warm_w: dict = {}
    warm_l: dict = {}
    for w in book.get("warmUp") or []:
        gid = w.get("gate") or "threshold"
        warm_w[gid] = warm_w.get(gid, 0) + words(
            w.get("title"), w.get("lead"), w.get("solved"), w.get("note"))
        warm_l[gid] = warm_l.get(gid, 0) + len(
            str(w.get("figure") or "").splitlines()) + FIGURE_PADDING_LINES

    # ── ③ KAPI AÇILIŞ ANLATILARI ───────────────────────────────────────
    frame_keys = {"threshold": "frame", "menagerie": "frame2",
                  "calendar": "frame3", "labyrinth": "frame4",
                  "mirror": "frame5"}
    frame_w = {g: words((book.get(k) or {}).get("opening"))
               for g, k in frame_keys.items()}

    # ── ④ ÖN MADDE · ARAÇLAR LEVHASI ───────────────────────────────────
    charts = book.get("toolsPlate", {})
    chart_rows = sum(len(c.get("entries", c.get("table", c.get("rows", []))))
                     for c in charts.values())
    chart_pages = chart_rows / (LINES_PER_PAGE * 3)          # üç sütun

    print("\n── kapı kapı · ölçülen metin ──")
    print("  %-14s %8s %8s %7s %7s %8s %7s"
          % ("kapı", "bulmaca", "ısınma", "açılış", "satır", "ÖLÇÜLEN",
             "bütçe"))
    over, measured_body = [], {}
    for gid in order:
        w = body_w.get(gid, 0) + warm_w.get(gid, 0) + frame_w.get(gid, 0)
        ln = fig_l.get(gid, 0) + warm_l.get(gid, 0)
        pgs = w / wpp + ln / LINES_PER_PAGE
        measured_body[gid] = round(pgs, 1)
        dec = budget.get(gid, 0)
        flag = "  ⛔" if pgs > dec else ""
        print("  %-14s %8d %8d %7d %7d %8.1f %7d%s"
              % (gid, body_w.get(gid, 0), warm_w.get(gid, 0),
                 frame_w.get(gid, 0), ln, pgs, dec, flag))
        if pgs > dec:
            over.append("%s %.1f > %d" % (gid, pgs, dec))
    total_body = sum(measured_body.values())
    total_budget = sum(budget.get(g, 0) for g in order)
    print("  %-14s %8d %8d %7d %7d %8.1f %7d"
          % ("TOPLAM", sum(body_w.values()), sum(warm_w.values()),
             sum(frame_w.values()), sum(fig_l.values()) + sum(warm_l.values()),
             total_body, total_budget))

    bm = pm.get("backMatter", {})
    declared_hints = bm.get("hintSection", 0)
    declared_sols = bm.get("solutionSection", 0)
    hint_pages = hint_words / wpp
    sol_pages = solution_words / wpp

    print("\n── arka madde · ölçülen (ÖLÇEKLEME YOK — hepsi yazıldı) ──")
    print("  ipuçları  %5d kelime → %5.1f sayfa   (bildirilen %d)"
          % (hint_words, hint_pages, declared_hints))
    print("  çözümler  %5d kelime → %5.1f sayfa   (bildirilen %d)"
          % (solution_words, sol_pages, declared_sols))
    print("\n── ön madde ──")
    print("  araçlar levhası %d satır → %.1f sayfa (bildirilen %d)"
          % (chart_rows, chart_pages, pm.get("frontMatter", {})
             .get("toolsPlate", 0)))

    rep.facts.update({
        "puzzles": len(pages), "wordsPerPage": wpp,
        "bodyWordsByGate": body_w, "figureLinesByGate": fig_l,
        "warmUpWordsByGate": warm_w, "warmUpLinesByGate": warm_l,
        "frameWordsByGate": frame_w,
        "measuredBodyPagesByGate": measured_body,
        "declaredBodyPagesByGate": budget,
        "measuredBodyPagesTotal": round(total_body, 1),
        "declaredBodyPagesTotal": total_budget,
        "hintWords": hint_words, "measuredHintPages": round(hint_pages, 1),
        "declaredHintPages": declared_hints,
        "solutionWords": solution_words,
        "measuredSolutionPages": round(sol_pages, 1),
        "declaredSolutionPages": declared_sols,
        "toolsPlateRows": chart_rows, "toolsPlatePages": round(chart_pages, 2),
        "totalWords": (sum(body_w.values()) + sum(warm_w.values())
                       + sum(frame_w.values()) + hint_words + solution_words),
        "perPuzzle": per_puzzle,
    })

    # ⚠ ÖLÇÜM MODELİ AŞARSA KIRMIZI — MODELE UYDURULMAZ.
    # A8 kapandı ve yeniden açılmaz: sayfa hedefi bir dizgi sorununu yok
    # etmek için DEĞİŞTİRİLMEZ. Ölçüm modeli aşıyorsa içerik veya dizgi
    # düzeltilir ve YENİDEN ölçülür.
    rep.check(not over,
              "⭑ HER KAPININ METNİ KENDİ BÜTÇESİNE SIĞIYOR ⭑"
              + ("" if not over else " — ⛔ TAŞAN: %s" % over))
    rep.check(hint_pages <= declared_hints,
              "ipucu bölümü bütçeye sığıyor (%.1f ≤ %d)"
              % (hint_pages, declared_hints))
    rep.check(sol_pages <= declared_sols,
              "çözüm bölümü bütçeye sığıyor (%.1f ≤ %d)"
              % (sol_pages, declared_sols))
    rep.check(chart_pages <= pm.get("frontMatter", {}).get("toolsPlate", 0),
              "araçlar levhası ön madde bütçesine sığıyor (%.1f ≤ %d)"
              % (chart_pages, pm.get("frontMatter", {}).get("toolsPlate", 0)))

    # Bir kapının bütçesinin ÇOK ALTINDA kalması bir hata DEĞİLDİR: kalan
    # payı levhalar doldurur (kapı başına 21 levha). Ama sessiz de kalmaz —
    # Faz 5'te dizgi dondurulurken bu pay ölçülerek kapatılır (K12).
    thin = ["%s %.1f/%d" % (g, measured_body[g], budget.get(g, 0))
            for g in order if budget.get(g) and measured_body[g] < budget[g] * 0.5]
    if thin:
        rep.warn("metin payı bütçenin yarısından az: %s — kalan pay LEVHAYA "
                 "aittir ve Faz 5'te dizgiyle ölçülerek kapanır (K12)"
                 % ", ".join(thin))

    return rep.finish("%d bulmaca · %d kapı · ölçülen gövde %.1f / %d sayfa"
                      % (len(pages), len(order), total_body, total_budget),
                      args.json)


if __name__ == "__main__":
    sys.exit(main())
