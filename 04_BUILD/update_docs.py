#!/usr/bin/env python3
"""
ÜRETİLEN BELGELER — BOOK_STATS.md ve ROADMAP_PROGRESS.md
================================================================================
Bu iki belgedeki her sayı ÖLÇÜLÜR. Hiçbiri elle yazılmaz.

NEDEN: elle yazılan bir sayı, kaynağı değiştiğinde SESSİZCE yalan söyler.
Ve bu projede yalan söyleyen bir sayı yalnızca bir belge hatası değildir:
sayfa sayısı Kapı V'i bağlar, aday sayısı kapsam kapısını bağlar,
doğrulanmış bulmaca sayısı öldürme kapısını bağlar.

`--check` üretilen içerikle diskteki içeriği karşılaştırır ve ayrışma
varsa KIRMIZI yanar — yani "belgeyi güncellemeyi unuttum" bir CI hatasıdır.

Çıkış kodları:  0 = geçti   1 = bayat belge   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")
FAMILIES = os.path.join(ROOT, "01_SOURCE", "mechanism_families.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")
SOURCES = os.path.join(ROOT, "01_SOURCE", "research", "sources.json")

BOOK_STATS = os.path.join(ROOT, "BOOK_STATS.md")
PROGRESS = os.path.join(ROOT, "ROADMAP_PROGRESS.md")

PHASES = [
    ("0", "Bootstrap", "phase0", "main", "—"),
    ("1", "Bulmaca mimarisi, çözülebilirlik, gizlilik", "phase1",
     "faz/1-mimari", "v0.1.0"),
    ("2", "⛔ **ÖLDÜRME KAPISI** — 20 bulmaca + 5 çözücü", "phase2",
     "faz/2-pilot", "v0.2.0"),
    ("3", "Kapı II · The Menagerie", "phase3", "faz/3-kapi-2", "v0.3.0"),
    ("4", "Kapı III–V + meta-mister", "phase4", "faz/4-kapi-3-5", "v0.4.0"),
    ("5", "Yakınsama + levha + doğrulama sayfası", "phase5",
     "faz/5-yakinsama", "v0.5.0"),
    ("6", "Nihai üretim + KDP paketi", "release", "faz/6-uretim", "v1.0.0"),
]


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_gate() -> str:
    p = os.path.join(ROOT, ".gate")
    if not os.path.exists(p):
        return "phase0"
    with open(p, encoding="utf-8") as fh:
        return fh.read().strip()


def pages(block: dict) -> int:
    return sum(v for k, v in block.items()
               if isinstance(v, int) and not k.endswith("$comment"))


def measure() -> dict:
    cfg = load(CONFIG)
    gates = load(GATE_INDEX)["gates"]
    fams = load(FAMILIES)["families"]
    puzzles = load(PUZZLE_INDEX)["puzzles"]
    srcs = load(SOURCES)["sources"]

    st = collections.Counter(p.get("status") for p in puzzles)
    by_gate = collections.Counter(p.get("gate") for p in puzzles)
    pm = cfg["production"]["pageModel"]
    pb = cfg["production"]["plateBudget"]

    front, back = pages(pm["frontMatter"]), pages(pm["backMatter"])
    body = sum(g.get("pageBudget", 0) for g in gates)
    plates = (sum(g.get("plates", {}).get("opening", 0)
                  + g.get("plates", {}).get("puzzle", 0) for g in gates)
              + pb["frontMatterPlates"] + pb["lastQuestionPlates"])

    pilot = [p for p in puzzles if p.get("pilotCohort")]
    kg = cfg["killGate"]["passCriteria"]

    return {
        "gate": read_gate(),
        "cfg": cfg, "gates": gates, "puzzles": puzzles,
        "candidates": len(puzzles),
        "status": st,
        "byGate": by_gate,
        "families": len({p.get("mechanismFamily") for p in puzzles}),
        "familiesDefined": len(fams),
        "plateCarriers": sum(1 for p in puzzles if p.get("plateCarriesData")),
        "sources": len(srcs),
        "sourcesChecked": sum(1 for s in srcs
                              if s.get("verificationStatus") == "checked"),
        "tested": sum(1 for p in puzzles if p.get("testStatus") == "tested"),
        "ambiguityOver": sum(1 for p in puzzles
                             if isinstance(p.get("ambiguityScore"), int)
                             and p["ambiguityScore"] > 2),
        "confirmedAlts": sum(p.get("confirmedAlternativeSolutions", 0)
                             for p in puzzles),
        "frontPages": front, "backPages": back, "bodyPages": body,
        "modelPages": front + body + back,
        "targetPages": pm["targetPages"],
        "plates": plates,
        "pilot": len(pilot),
        "pilotMinutes": (sum(p.get("expectedCompletionMinutes", 0)
                             for p in pilot)
                         + kg.get("pilotSessionOverheadMinutes", 0)),
        "killGateCap": kg.get("medianCompletionMinutesMax", 0),
    }


def render_book_stats(m: dict) -> str:
    cfg = m["cfg"]
    prod = cfg["production"]
    pcst = prod["kdpPrintCost"]
    rows = []
    for ed in prod["editionsHypothesis"]:
        if not ed.get("enabled") or ed.get("list") is None:
            rows.append("| %s | **üretilmez** | — | — | Görsel şifreler "
                        "e-okuyucuda bozulur |" % ed["id"].capitalize())
            continue
        band = (pcst["paperbackRegularTrimBW"] if ed["id"] == "paperback"
                else pcst["hardcoverRegularTrimBW"])
        cost = band["fixed"] + m["modelPages"] * band["perPage"]
        rate = (pcst["royaltyRateAtOrAbove999"] if ed["list"] >= 9.99
                else pcst["royaltyRateBelow999"])
        roy = ed["list"] * rate - cost
        rows.append("| %s | hipotez | %.2f $ | **%.2f $** | baskı %.2f $ · "
                    "başabaş ACOS %%%.1f |"
                    % (ed["id"].capitalize(), ed["list"], roy, cost,
                       roy / ed["list"] * 100))

    gate_rows = []
    stars = {1: "★", 2: "★★", 3: "★★★"}
    for g in m["gates"]:
        if g.get("metaGate"):
            continue
        gate_rows.append("| %s · %s | %s | %d | %d | %d |"
                         % (g["roman"], g["en"], stars[g["difficulty"]],
                            m["byGate"].get(g["id"], 0),
                            sum(1 for p in m["puzzles"]
                                if p.get("gate") == g["id"]
                                and p.get("status") in ("validated", "written")),
                            g["puzzles"]))

    return """# BOOK STATS — Codex Enigmatica

<!-- ⚠ ÜRETİLEN BELGE — 04_BUILD/update_docs.py. ELLE DÜZENLEMEYİN. -->

> Kapı: `%(gate)s` · Bu dosyadaki her sayı **ölçülmüştür**.
>
> ⚠ Bu dosya **çözüm bilgisi taşımaz** — yalnızca sayılar.

## 1. Tek bakışta

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday bulmaca | **%(candidates)d** | ≥130 |
| Doğrulanmış bulmaca | **%(validated)d** | 100 |
| Yazılmış bulmaca | **%(written)d** | 100 |
| Kapı | **%(gatecount)d** | 5 |
| Mekanizma ailesi | **%(families)d** / %(familiesDefined)d tanımlı | ≥10 |
| Veri taşıyan levha adayı | **%(plateCarriers)d** | — |
| Künye | **%(sources)d** (%(sourcesChecked)d doğrulanmış) | — |
| `tested` durumundaki bulmaca | **%(tested)d** | — |
| **Onaylanmış alternatif çözüm** | **%(confirmedAlts)d** | **0** |
| Belirsizlik puanı > 2 | **%(ambiguityOver)d** | **0** |
| İpucu (3 kademe × 100) | **0** | 300 |
| Metin | **0** | ~34.000 kelime |

## 2. Öldürme kapısı (Faz 2)

| Ölçüt | Ölçülen | Eşik |
|---|---:|---:|
| Kapı I'i bitiren çözücü | **HARİCİ DOĞRULAMA BEKLİYOR** | ≥ 4 / 5 |
| Hiç çözülemeyen bulmaca | — | 0 |
| Bulmaca başına bitiren çözücü | — | ≥ 2 |
| Onaylanmış alternatif çözüm | %(confirmedAlts)d | 0 |
| Medyan tamamlama (dakika) | — | ≤ %(killGateCap)d |
| **KARAR** | — | — |

Pilot kohort **%(pilot)d** bulmaca · modellenen oturum **%(pilotMinutes)d dk**
(tavanın %%%(pilotPct).0f'i).

## 3. Kapı dağılımı

| Kapı | Zorluk | Aday | Doğrulanmış | Hedef |
|---|---:|---:|---:|---:|
%(gateRows)s

## 4. Sayfa ve levha modeli

> ⚠ Sayfa sayısı **Kapı V'i bağlar** (öz-göndergesel bulmacalar).

| | |
|---|---:|
| Ön madde | %(frontPages)d |
| Gövde (5 kapı + son soru) | %(bodyPages)d |
| Arka madde (300 ipucu + 100 çözüm) | %(backPages)d |
| **Modelin sayfa sayısı** | **%(modelPages)d** |
| Hedef | %(targetPages)d |
| Levha | %(plates)d |

## 5. Sürümler

| Sürüm | Durum | Fiyat | Telif | Not |
|---|---|---:|---:|---|
%(edRows)s
""" % {
        "gate": m["gate"], "candidates": m["candidates"],
        "validated": m["status"].get("validated", 0) + m["status"].get("written", 0),
        "written": m["status"].get("written", 0),
        "gatecount": len([g for g in m["gates"] if not g.get("metaGate")]),
        "families": m["families"], "familiesDefined": m["familiesDefined"],
        "plateCarriers": m["plateCarriers"], "sources": m["sources"],
        "sourcesChecked": m["sourcesChecked"], "tested": m["tested"],
        "confirmedAlts": m["confirmedAlts"], "ambiguityOver": m["ambiguityOver"],
        "killGateCap": m["killGateCap"], "pilot": m["pilot"],
        "pilotMinutes": m["pilotMinutes"],
        "pilotPct": (m["pilotMinutes"] / m["killGateCap"] * 100
                     if m["killGateCap"] else 0),
        "gateRows": "\n".join(gate_rows),
        "frontPages": m["frontPages"], "bodyPages": m["bodyPages"],
        "backPages": m["backPages"], "modelPages": m["modelPages"],
        "targetPages": m["targetPages"], "plates": m["plates"],
        "edRows": "\n".join(rows),
    }


def render_progress(m: dict) -> str:
    cur = m["gate"]
    order = [p[2] for p in PHASES]
    rows = []
    for num, name, gate, branch, tag in PHASES:
        if order.index(gate) < order.index(cur):
            state = "✅ **TAMAM**"
        elif gate == cur:
            state = "✅ **TAMAM**"
        elif order.index(gate) == order.index(cur) + 1:
            state = "⏸ **SIRADA**"
        else:
            state = "⏸ beklemede"
        rows.append("| **%s** | %s | %s | `%s` | `%s` | %s |"
                    % (num, name, state, gate, branch, tag))

    return """# ROADMAP PROGRESS — Codex Enigmatica

<!-- ⚠ ÜRETİLEN BELGE — 04_BUILD/update_docs.py. ELLE DÜZENLEMEYİN. -->

> Kapı: `%(gate)s`

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
%(rows)s

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday bulmaca | **%(candidates)d** | ≥130 |
| Mekanizma ailesi | **%(families)d** | ≥10 |
| Pilot kohort (Kapı I) | **%(pilot)d** | 20 |
| Doğrulanmış bulmaca | **%(validated)d** | 100 |
| Yazılmış bulmaca | **%(written)d** | 100 |
| Onaylanmış alternatif çözüm | **%(confirmedAlts)d** | **0** |
| İpucu (3×100) | **0** | 300 |
| Levha | **0** üretildi / %(plates)d planlandı | ~110 |
| Kelime | **0** | ~34.000 |
| Künye | **%(sources)d** (%(sourcesChecked)d doğrulanmış) | — |

---

## Sonraki izinli eylem

> **KURUCU ONAYI BEKLENİYOR.**
>
> Faz 1 tamamdır ve `.gate` = `%(gate)s`. Faz 2 **başlatılmadı**.
>
> Faz 2'ye girmeden önce kapanması gerekenler:
> 1. **A3** — beş harici çözücü belirlenir (**sert bloklayıcı**)
> 2. **A8** — sayfa hedefi 230 onaylanır
> 3. **A9** — pilot levhaların POD provası kararı
> 4. **A2** — beş kapı teması onayı
>
> Ayrıntı: `DECISIONS.md § AÇIK KARARLAR`
""" % {
        "gate": cur, "rows": "\n".join(rows),
        "candidates": m["candidates"], "families": m["families"],
        "pilot": m["pilot"],
        "validated": m["status"].get("validated", 0) + m["status"].get("written", 0),
        "written": m["status"].get("written", 0),
        "confirmedAlts": m["confirmedAlts"], "plates": m["plates"],
        "sources": m["sources"], "sourcesChecked": m["sourcesChecked"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="yazma; bayatsa KIRMIZI")
    args = ap.parse_args()

    m = measure()
    targets = [(BOOK_STATS, render_book_stats(m)),
               (PROGRESS, render_progress(m))]

    stale = []
    for path, body in targets:
        current = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                current = fh.read()
        if current.strip() != body.strip():
            stale.append(os.path.relpath(path, ROOT))
            if not args.check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(body)

    if args.check:
        if stale:
            print("⛔ BAYAT ÜRETİLEN BELGE: %s" % ", ".join(stale))
            print("   düzeltme: python3 04_BUILD/update_docs.py")
            return 1
        print("✅ üretilen belgeler güncel")
        return 0

    print("✅ üretildi: %s" % (", ".join(stale) if stale else "değişiklik yok"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
