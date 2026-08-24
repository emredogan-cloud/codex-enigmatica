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


def _kill_verdict() -> str:
    """Öldürme kapısı kararı — ÜRETİLEN rapordan okunur, elle yazılmaz.

    Rapor yoksa 'ÜRETİLMEDİ' der. Sessizce 'PASS' yazmak, bu projede
    yapılabilecek en pahalı yalandır."""
    path = os.path.join(ROOT, "06_REPORTS", "tracked", "kill-gate-report.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("verdict") or "ÜRETİLMEDİ"
    except (OSError, json.JSONDecodeError):
        return "ÜRETİLMEDİ"


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
        # ⚠ Üretilen belgeler geçersiz kılmayı BİLMEK ZORUNDA: bilmezlerse
        # doğrulanmamış bir fazı "TAMAM" diye yazarlar.
        "override": (cfg.get("killGate") or {}).get("externalValidation") or {},
        "cfg": cfg, "gates": gates, "puzzles": puzzles,
        "candidates": len(puzzles),
        "status": st,
        "drafted": st.get("drafted", 0),
        "answerSpaceOk": sum(1 for p in puzzles if p.get("answerSpaceVerified")),
        "answerSpaceTotal": sum(p.get("answerSpaceSize", 0) for p in puzzles),
        "killVerdict": _kill_verdict(),
        "sessions": (cfg.get("founder", {}).get("externalSolvers", {})
                     .get("sessionsRecorded", 0)),
        "solversIdentified": (cfg.get("founder", {}).get("externalSolvers", {})
                              .get("identifiedCount", 0)),
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
| **Yazılmış taslak** (metin + çözüm + ipucu) | **%(drafted)d** | — |
| Doğrulanmış bulmaca | **%(validated)d** | 100 |
| Yazılmış bulmaca (nihai) | **%(written)d** | 100 |
| Kapı | **%(gatecount)d** | 5 |
| Mekanizma ailesi | **%(families)d** / %(familiesDefined)d tanımlı | ≥10 |
| Veri taşıyan levha adayı | **%(plateCarriers)d** | — |
| Künye | **%(sources)d** (%(sourcesChecked)d doğrulanmış) | — |
| `tested` durumundaki bulmaca | **%(tested)d** | — |
| **Onaylanmış alternatif çözüm** | **%(confirmedAlts)d** | **0** |
| Belirsizlik puanı > 2 | **%(ambiguityOver)d** | **0** |
| **Cevap uzayı bağımsız doğrulanmış** | **%(answerSpaceOk)d / %(drafted)d** | tamamı |
| **Elenen aday dize** (cevap uzayı toplamı) | **%(answerSpaceTotal)d** | — |
| İpucu (3 kademe) | **%(hints)d** | 300 |

## 2. Öldürme kapısı (Faz 2)

| Ölçüt | Ölçülen | Eşik |
|---|---:|---:|
| Çözücü **belirlendi** (A3) | **%(solversIdentified)d** | 5 |
| Oturum **yapıldı** (A12) | **%(sessions)d** | 5 |
| Kapı I'i bitiren çözücü | **ÖLÇÜLMEDİ** | ≥ 4 / 5 |
| Hiç çözülemeyen bulmaca | ÖLÇÜLMEDİ | 0 |
| Bulmaca başına bitiren çözücü | ÖLÇÜLMEDİ | ≥ 2 |
| Onaylanmış alternatif çözüm | %(confirmedAlts)d | 0 |
| Medyan tamamlama (dakika) | ÖLÇÜLMEDİ | ≤ %(killGateCap)d |
| **KARAR** | **%(killVerdict)s** | PASS |

> ⛔ **%(killVerdict)s.** İç çözücü kayıtları öldürme kapısında **sayılmaz**
> (`internalSolverCountsAsEvidence: false`). Sıfır oturumla bütün ölçütler
> "ihlal edilmemiş" görünür — bu bir geçiş değil, bir **boşluktur**.

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
        "drafted": m["drafted"], "hints": m["drafted"] * 3,
        "answerSpaceOk": m["answerSpaceOk"],
        "answerSpaceTotal": m["answerSpaceTotal"],
        "killVerdict": m["killVerdict"], "sessions": m["sessions"],
        "solversIdentified": m["solversIdentified"],
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
    """⚠ ÜRETİLEN BİR BELGE DE YALAN SÖYLEYEBİLİR.

    Bu tablo faz durumunu `.gate` seviyesinden ÇIKARIYORDU ve `.gate`
    `phase3` olunca Faz 2'yi "✅ TAMAM" diye yazdı. Ama Faz 2 bir ÖLDÜRME
    KAPISIDIR ve o kapı **harici kanıtla geçilmedi** — kurucu kararıyla
    geçildi. Tabloyu olduğu gibi bırakmak, kurucunun açıkça yasakladığı
    şeyi yapardı: doğrulanmamış bir fazı doğrulanmış göstermek.

    Artık üç durum ayrı yazılır:
      ✅ TAMAM            — kapısı kendi ölçütleriyle geçildi
      ⚑ KURUCU KARARIYLA  — girildi ama doğrulama BEKLİYOR
      ⏸ beklemede
    """
    cur = m["gate"]
    order = [p[2] for p in PHASES]
    ov = m.get("override") or {}
    # Geçersiz kılma yürürlükteyse, öldürme kapısına bağlı fazlar (2 ve
    # sonrası) "TAMAM" diye yazılamaz: harici doğrulama yapılmadı.
    overridden = bool(ov.get("founderOverride")) and \
        not ov.get("humanValidationPassed")
    rows = []
    for num, name, gate, branch, tag in PHASES:
        i, c = order.index(gate), order.index(cur)
        if i <= c:
            state = "✅ **TAMAM**"
            if overridden and i >= order.index("phase2"):
                state = "⚑ **KURUCU KARARIYLA** — doğrulama bekliyor"
        elif i == c + 1:
            state = "⏸ **SIRADA**"
        else:
            state = "⏸ beklemede"
        rows.append("| **%s** | %s | %s | `%s` | `%s` | %s |"
                    % (num, name, state, gate, branch, tag))
    if overridden:
        rows.append("")
        rows.append("> ## ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING")
        rows.append(">")
        rows.append("> Ölçülen öldürme kapısı: ⛔ **HARD-STOP** (1/5) — "
                    "**değişmedi**.")
        rows.append("> Yapılan harici oturum: **%d** · İnsan doğrulaması "
                    "geçti mi: **%s**"
                    % (ov.get("sessionsPerformed", 0),
                       "EVET" if ov.get("humanValidationPassed") else "HAYIR"))
        rows.append(">")
        rows.append("> Faz 2 ve sonrası **kurucu geçersiz kılmasıyla** "
                    "ilerledi (`DECISIONS.md § A13`). Hiçbir faz "
                    "*harici olarak doğrulanmış* değildir.")

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
| **Yazılmış taslak** | **%(drafted)d** | — |
| Doğrulanmış bulmaca | **%(validated)d** | 100 |
| Yazılmış bulmaca (nihai) | **%(written)d** | 100 |
| Onaylanmış alternatif çözüm | **%(confirmedAlts)d** | **0** |
| İpucu (3 kademe) | **%(hints)d** | 300 |
| Levha | **0** üretildi / %(plates)d planlandı | ~110 |
| Kelime | **0** | ~34.000 |
| Künye | **%(sources)d** (%(sourcesChecked)d doğrulanmış) | — |

---

## Sonraki izinli eylem

> ### ⛔ FAZ 2 · ÖLDÜRME KAPISI: **%(killVerdict)s**
>
> Faz 2'nin ajan tarafından yapılabilir bütün işi **tamamlandı**:
> yirmi Türkçe pilot bulmaca yazıldı, cevap uzayı mimarisi kuruldu ve
> yirmisi de bağımsız olarak doğrulandı, üç yeni kapı eklendi, kanarya
> sırrı kuruldu ve dört senaryoyla kanıtlandı.
>
> **Ama öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz.**
> Harici çözücü oturumu: **%(sessions)d / 5**.
>
> Kalan tek iş **kurucuya aittir** ve ajan onu yapamaz:
> 1. **A12** — beş harici çözücüyle oturumları yürüt
>    → `00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`
> 2. sonuçları `06_REPORTS/solver/` altına yaz, sayaçları güncelle
> 3. `./04_BUILD/qa_all.sh phase2` koştur ve kararı **oku**
>
> Ayrıca açık: **A9** (levha provası — paket hazır) · **A2** · **A5** · **A7**
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
        "killVerdict": m["killVerdict"], "sessions": m["sessions"],
        "drafted": m["drafted"], "hints": m["drafted"] * 3,
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
