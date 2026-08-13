#!/usr/bin/env python3
"""
SAYFA VE LEVHA BÜTÇESİ — Codex Enigmatica
================================================================================
Bu kapı ÜÇ iş görür ve üçüncüsü bu projeye özgüdür:

  ① fiyat ve telif matematiğinin dayandığı sayfa sayısını ÜRETİR
  ② levha bütçesinin üretim kapasitesiyle uyumunu denetler
  ③ ⭑ KAPI V'İ BAĞLAR ⭑

③ NEDEN: Kapı V öz-göndergeseldir — bulmacaları kitabın sayfa
numaralarına, dizinine ve kolofonuna dayanır. Sayfa sayısı değişirse
Kapı V KIRILIR (K12). Bu yüzden sayfa sayısı bir "tahmin" değil, bir
SÖZLEŞMEDİR: Faz 5'te dondurulur ve Faz 6 onu yalnızca doğrular.

Model tek kaynaktan türer:
  · kapı sayfaları  → 01_SOURCE/gate_index.json § pageBudget
  · ön/arka madde   → project_config.json § production.pageModel
İki yerde yazılmış bir sayı, er geç iki farklı sayı olur (D1).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None,
                    help="kabul edilir ve yok sayılır — bu kapı faz "
                         "seviyesinden bağımsızdır; ortak çağrı biçimi korunur")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  SAYFA VE LEVHA BÜTÇESİ")
    print("=" * 74)

    rep = Report(args.verbose)

    if not os.path.exists(GATE_INDEX):
        print("\n  ⊘ gate_index.json yok — Faz 1 teslimatı")
        print("=" * 74)
        return 0

    cfg = load(CONFIG)
    gidx = load(GATE_INDEX)
    prod = cfg.get("production", {})
    pm = prod.get("pageModel")
    pb = prod.get("plateBudget")

    if not pm or not pb:
        rep.check(False, "project_config.json § production.pageModel/plateBudget var")
        print("=" * 74)
        return 1

    gates = gidx.get("gates", [])

    # ── sayfa modeli ────────────────────────────────────────────────────
    print("\n── sayfa modeli ──")
    # $comment anahtarları sayfa değildir; yalnızca tamsayılar toplanır.
    def pages(block: dict) -> int:
        return sum(v for k, v in block.items()
                   if isinstance(v, int) and not k.endswith("$comment"))

    front = pages(pm["frontMatter"])
    back = pages(pm["backMatter"])
    gate_pages = {g["id"]: g.get("pageBudget", 0) for g in gates}
    body = sum(gate_pages.values())
    total = front + body + back

    rep.facts.update({"frontMatter": front, "backMatter": back,
                      "gatePages": gate_pages, "bodyPages": body,
                      "modelPages": total})

    target = pm["targetPages"]
    tol = pm["tolerancePct"]
    lo, hi = target * (1 - tol / 100), target * (1 + tol / 100)
    dev = (total - target) / target * 100
    rep.facts["targetPages"] = target
    rep.facts["deviationPct"] = round(dev, 2)

    print("  ön madde %d + gövde %d + arka madde %d = %d sayfa"
          % (front, body, back, total))
    for g in gates:
        print("     · %-14s %3d sayfa" % (g["id"], g.get("pageBudget", 0)))

    rep.check(lo <= total <= hi,
              "model %d sayfa · hedef %d ± %%%d (%.0f–%.0f) · sapma %%%.2f"
              % (total, target, tol, lo, hi, dev))

    # ⚠ ARKA MADDE ARTIK ELLE DEĞİL, İÇERİKTEN TÜRETİLİR.
    # 24 sayfalık eski bütçe fiziksel olarak imkânsızdı: 300 ipucu ve 100
    # tam çözüm oraya SIĞMIYORDU. Ve bu bir dizgi meselesi değil bir
    # ÇÖZÜLEBİLİRLİK meselesidir — arka madde taşarsa kitap yeniden
    # sayfalanır ve Kapı V'in sayfa numarasına dayanan sekiz bulmacası
    # kırılır (K12), üstelik takvimin bittiği yerde.
    der = pm.get("backMatterDerivation")
    if der:
        wpp = der["wordsPerPage"]
        need_hint = -(-der["hintsTotal"] * der["wordsPerHint"] // wpp)
        need_sol = -(-der["solutionsTotal"] * der["wordsPerSolution"] // wpp)
        need_back = need_hint + need_sol + der["fixedPages"]
        rep.facts["backMatterDerived"] = need_back
        print("  arka madde türetimi: ipucu %d + çözüm %d + sabit %d = %d sayfa"
              % (need_hint, need_sol, der["fixedPages"], need_back))
        rep.check(back >= need_back,
                  "⭑ arka madde İÇERİĞE YETİYOR ⭑ (bildirilen %d ≥ türetilen %d)"
                  % (back, need_back))
    else:
        rep.check(False, "pageModel.backMatterDerivation tanımlı")

    # KDP baskı kısıtları — sayfa sayısı BASILAMAZ olmamalı
    kdp = prod.get("kdpPrintCost", {})
    for eid, key in (("paperback", "paperbackRegularTrimBW"),
                     ("hardcover", "hardcoverRegularTrimBW")):
        band = kdp.get(key, {})
        enabled = any(e.get("id") == eid and e.get("enabled")
                      for e in prod.get("editionsHypothesis", []))
        if not enabled or not band:
            continue
        rep.check(band.get("minPages", 0) <= total <= band.get("maxPages", 10**6),
                  "%s KDP sayfa aralığında (%d–%d)"
                  % (eid, band.get("minPages", 0), band.get("maxPages", 0)))

    if total % 2:
        rep.warn("model sayfa sayısı TEK (%d) — dizgide bir boş sayfaya "
                 "yuvarlanır ve Kapı V bundan etkilenir" % total)

    # ── levha bütçesi ───────────────────────────────────────────────────
    print("\n── levha bütçesi ──")
    gate_plates = {}
    for g in gates:
        pl = g.get("plates", {})
        gate_plates[g["id"]] = pl.get("opening", 0) + pl.get("puzzle", 0)
    plates_total = (sum(gate_plates.values())
                    + pb["frontMatterPlates"] + pb["lastQuestionPlates"])
    rep.facts["gatePlates"] = gate_plates
    rep.facts["modelPlates"] = plates_total

    ptarget = pb["targetPlates"]
    ptol = pb["tolerancePct"]
    plo, phi = ptarget * (1 - ptol / 100), ptarget * (1 + ptol / 100)
    print("  kapı levhaları %d + ön madde %d + son soru %d = %d levha"
          % (sum(gate_plates.values()), pb["frontMatterPlates"],
             pb["lastQuestionPlates"], plates_total))
    rep.check(plo <= plates_total <= phi,
              "model %d levha · hedef %d ± %%%d" % (plates_total, ptarget, ptol))

    # ── bulmaca yoğunluğu ve süre modeli ────────────────────────────────
    print("\n── bulmaca yoğunluğu ve süre modeli ──")
    scope = cfg.get("scope", {})
    puzzles = scope.get("puzzles", 0)
    if puzzles:
        per_puzzle = body / puzzles
        rep.facts["pagesPerPuzzle"] = round(per_puzzle, 2)
        print("  gövde %d sayfa / %d bulmaca = %.2f sayfa/bulmaca"
              % (body, puzzles, per_puzzle))
        # Bir bulmaca + levhası bir sayfanın altına sıkışamaz.
        rep.check(per_puzzle >= 1.0,
                  "bulmaca başına ≥1,0 sayfa (levha + metin sığıyor)")
        rep.check(per_puzzle <= 2.5,
                  "bulmaca başına ≤2,5 sayfa (kitap şişmiyor)")

    if os.path.exists(PUZZLE_INDEX):
        idx = load(PUZZLE_INDEX)
        pilot = [p for p in idx.get("puzzles", []) if p.get("pilotCohort")]
        if pilot:
            kg = cfg.get("killGate", {}).get("passCriteria", {})
            cap = kg.get("medianCompletionMinutesMax", 0)
            overhead = kg.get("pilotSessionOverheadMinutes", 0)
            puzzle_mins = sum(p.get("expectedCompletionMinutes", 0)
                              for p in pilot)
            mins = puzzle_mins + overhead
            rep.facts["pilotPuzzles"] = len(pilot)
            rep.facts["pilotPuzzleMinutes"] = puzzle_mins
            rep.facts["pilotSessionOverhead"] = overhead
            rep.facts["pilotModelledMinutes"] = mins
            rep.facts["killGateMinutesMax"] = cap
            print("  pilot kohort %d bulmaca · bulmaca süresi %d dk + oturum "
                  "yükü %d dk = %d dk · öldürme kapısı tavanı %d dk"
                  % (len(pilot), puzzle_mins, overhead, mins, cap))
            # Model tavana yapışıksa öldürme kapısı ölçmeden önce kaybedilmiştir.
            rep.check(cap == 0 or mins <= cap * 0.85,
                      "modellenen pilot süresi tavanın ≤%%85'i "
                      "(%d ≤ %d) — ipucu arayışı için pay var"
                      % (mins, int(cap * 0.85)))
            # Düz bir süre eğrisi, ölçülmemiş bir şablon sabitinin işaretidir.
            distinct = len({p.get("expectedCompletionMinutes") for p in pilot})
            rep.check(distinct >= 4,
                      "pilot süre tahminleri şablon sabiti değil "
                      "(%d ayrı değer)" % distinct)

    # ── kelime bütçesi ──────────────────────────────────────────────────
    wt = pm.get("wordTarget")
    if wt:
        rep.facts["wordTarget"] = wt
        rep.check(scope.get("manuscriptWordTarget") == wt,
                  "kelime hedefi scope ile pageModel arasında tutarlı")

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · model %d sayfa · %d levha"
              % (rep.checks, total, plates_total))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
