#!/usr/bin/env python3
"""
⭑ ÇAPRAZ REFERANS KAPISI ⭑ — kitabın KENDİ İÇİNE yaptığı göndermeler
================================================================================
Bu kitap okura sürekli bir şey gösterir: *"Çizelge J'de bulun"*,
*"Gök Kataloğu'nun bir üyesidir"*, *"bu kapının 1. bulmacası"*,
*"araçlar levhası"*. Her gönderme bir SÖZDÜR ve sözleşmenin ikinci
maddesi onu bağlar:

    "Hiçbiri kitabın dışındaki bilgiyi gerektirmez."

Bir gönderme boşa düşerse okur kitabın dışına çıkmak zorunda kalır — ya
da çıkamaz ve bulmacayı çözülemez sanır. İkisi de sözü bozar.

────────────────────────────────────────────────────────────────────────
⭑ NEDEN AYRI BİR KAPI ⭑

`qa_dependency` BULMACA bağımlılıklarını denetler (DAG, ileri referans).
`qa_readerpack` sayfanın VERİSİNİN orada olduğunu denetler. Hiçbiri
metnin İÇİNDEKİ göndermeleri okumaz: bir kısıt cümlesi olmayan bir
çizelgeyi adıyla anabilir ve iki kapı da yeşil yanar.

⚠ Ve gönderme adları Faz 1'de BİR KEZ değişti. `RED_TEAM_CHECKLIST`
kaydına göre çizelgeler yeniden adlandırıldığında başlıklar ve sözleşme
sayfası güncellendi — ama bir bulmacanın kısıt cümlesi eski adı
taşımaya devam etti. Bu kapı o kusurun tekrarlanmasını imkânsız kılar.

Altı ölçüm:

  ① ÇİZELGE ADI     — "Çizelge X" gerçekten var mı
  ② KATALOG ADI     — "… Kataloğu / Sözlüğü" araçlar levhasında var mı
  ③ BULMACA ATFI    — metinde anılan bulmaca kimliği envanterde var mı
  ④ LEVHA ATFI      — anılan levha kimliği o sayfaya ait mi
  ⑤ ZAMANSAL SIRA   — anılan çizelge okurun ELİNDE mi (ileri gönderme yok)
  ⑥ ÖLÜ ÇİZELGE     — basılan ama hiç anılmayan çizelge var mı

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
GATE_INDEX = os.path.join(pl.ROOT, "01_SOURCE", "gate_index.json")

CHART_REF = re.compile(r"Chart\s+([A-Z]{1,3})\b")
# ⚠ THIS PATTERN WAS TURKISH ("… Kataloğu | Sözlüğü") and it silently
# matched nothing once the charts were renamed for the English edition —
# which reports every catalogue as NEVER MENTIONED. It now matches the
# English chart names, and the comparison strips a leading "The" on both
# sides so that "the Sky Catalogue" in a clue resolves to the chart titled
# "Chart H · The Sky Catalogue".
CATALOGUE_REF = re.compile(
    r"\b((?:[A-Z][a-z]+\s+)+(?:Catalogue|Lexicon|Alphabet|Sayings|Table|"
    r"Marks|Numbers))\b")


def _cat_key(name: str) -> str:
    n = " ".join(str(name).split()).lower()
    return n[4:] if n.startswith("the ") else n
# ⚠ KALIP 'g[1-5]' İDİ VE BİR KUSURU GÖRMÜYORDU: yanlış yazılmış bir
# gönderme (g9-999) kalıba uymadığı için REFERANS SAYILMIYOR, dolayısıyla
# denetlenmiyordu. Fikstür yakaladı. Kalıp artık kapı numarasına
# bakmaz — kapı numarasının kendisi de yanlış olabilir.
PUZZLE_REF = re.compile(r"\b(g\d+-\d{3}|meta-\d{3})\b")
PLATE_REF = re.compile(r"\b(pl-[a-z0-9-]+)\b")

# Metnin okur tarafından görülen alanları. `input` DIŞARIDA: iç kayıttır.
TEXT_FIELDS = ("title", "flavour", "objective", "readerAction",
               "figure", "printedTable")


def page_text(p: dict) -> str:
    return " ".join(
        [str(p.get(f) or "") for f in TEXT_FIELDS]
        + [str(x) for x in (p.get("clues") or [])]
        + [str(x) for x in (p.get("constraints") or [])])


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
    print("  ⭑ ÇAPRAZ REFERANS ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    book = pl.load_json(BOOK) or {}
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "denetim YAPILAMADI")
        rep.warn("çapraz referans BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    charts = book.get("toolsPlate") or {}
    by_letter = {}
    by_name = {}
    for key, ch in charts.items():
        letter = str(ch.get("id") or "").strip()
        if letter:
            by_letter[letter] = key
        title = str(ch.get("title") or "")
        # "Çizelge H · Gök Kataloğu" → "Gök Kataloğu"
        if "·" in title:
            by_name[_cat_key(title.split("·", 1)[1])] = key

    index = {p["puzzleId"]: p for p in pl.load_index()}
    pages = book.get("puzzles", [])
    gi = pl.load_json(GATE_INDEX) or {}
    order = {g.get("id"): i for i, g in enumerate(gi.get("gates", []))}

    # Bir çizelge okurun eline hangi kapıda geçer? Araçlar levhası ÖN
    # MADDEDEDİR — yani hepsi baştan basılıdır. Yine de bir çizelgeye ilk
    # kez ondan ÖNCEKİ bir kapıda gönderme yapılması bir tasarım
    # kusurudur: çizelge o kapının açılışında tanıtılmamıştır.
    first_use: dict = {}
    for p in pages:
        gidx = order.get(p.get("gate"), 99)
        for letter in CHART_REF.findall(page_text(p)):
            key = by_letter.get(letter)
            if key and gidx < first_use.get(key, (99, ""))[0]:
                first_use[key] = (gidx, p["puzzleId"])

    bad_chart, bad_cat, bad_puzzle, bad_plate = [], [], [], []
    used_charts: set = set()
    refs = 0

    for p in pages:
        pid = p["puzzleId"]
        txt = page_text(p)

        for letter in CHART_REF.findall(txt):
            refs += 1
            if letter not in by_letter:
                bad_chart.append("%s → Chart %s" % (pid, letter))
            else:
                used_charts.add(by_letter[letter])

        for name in CATALOGUE_REF.findall(txt):
            refs += 1
            name = _cat_key(name)
            if name not in by_name:
                bad_cat.append("%s → %s" % (pid, name))
            else:
                used_charts.add(by_name[name])

        for ref in PUZZLE_REF.findall(txt):
            refs += 1
            if ref not in index:
                bad_puzzle.append("%s → %s" % (pid, ref))

        for plate in PLATE_REF.findall(txt):
            refs += 1
            if plate != p.get("plateId"):
                bad_plate.append("%s → %s (kendi levhası %s)"
                                 % (pid, plate, p.get("plateId")))

    # Ön/arka madde de gönderme yapar ve o göndermeler de tutmalıdır.
    matter = book.get("matter") or {}
    matter_txt = " ".join(
        str(x) for v in matter.values()
        for x in (v if isinstance(v, list) else
                  sum(([k, str(w)] for k, w in v.items()), [])
                  if isinstance(v, dict) else [v]))
    for letter in CHART_REF.findall(matter_txt):
        refs += 1
        if letter not in by_letter:
            bad_chart.append("ön/arka madde → Chart %s" % letter)
        else:
            used_charts.add(by_letter[letter])
    for name in CATALOGUE_REF.findall(matter_txt):
        refs += 1
        name = _cat_key(name)
        if name not in by_name:
            bad_cat.append("ön/arka madde → %s" % name)
        else:
            used_charts.add(by_name[name])

    # ── ⑤ KAPI AÇILIŞI YENİ ÇİZELGESİNİ ADIYLA ANIYOR MU ─────────────
    # ⚠ FAZ 5 · ÖN MADDE BİR SÖZ VERİYOR: *"Bir kapıda yeni bir çizelge
    # gerektiğinde, o çizelge kapının açılışında ADIYLA anılır — aramanız
    # istenmez."* Line editor ölçtü: BEŞ AÇILIŞIN HİÇBİRİ tek bir çizelge
    # adı anmıyordu. Verilen bir söz, tutulduğu ÖLÇÜLMEDİKÇE bir sözdür.
    frame_key = {"threshold": "frame", "menagerie": "frame2",
                 "calendar": "frame3", "labyrinth": "frame4",
                 "mirror": "frame5"}
    by_gate: dict = {}
    for p in pages:
        s_ = by_gate.setdefault(p.get("gate"), set())
        txt = page_text(p)
        s_.update(L for L in CHART_REF.findall(txt) if L in by_letter)
        for name in CATALOGUE_REF.findall(txt):
            key = by_name.get(_cat_key(name))
            if key:
                s_.add(next(L for L, k in by_letter.items() if k == key))
    introduced: set = set()
    silent = []
    for gid in [g.get("id") for g in gi.get("gates", [])]:
        fresh = sorted(x for x in by_gate.get(gid, set()) if x not in introduced)
        introduced |= set(fresh)
        if not fresh:
            continue
        opening = " ".join((book.get(frame_key.get(gid, "")) or {})
                           .get("opening") or [])
        missing = [x for x in fresh if "Chart %s" % x not in opening]
        if missing:
            silent.append("%s → %s" % (gid, " ".join(missing)))
    rep.check(not silent,
              "⭑ ⑤ HER KAPI AÇILIŞI KENDİ YENİ ÇİZELGESİNİ ADIYLA ANIYOR ⭑ "
              "(ön madde bunu SÖZ VERİYOR)"
              + ("" if not silent else " — ⛔ SESSİZ: %s" % silent))

    # ⑥ ÖLÜ ÇİZELGE — basılan ama hiç anılmayan
    # ⚠ `printed: false` olanlar ispat alanıdır; kitapta basılmazlar ve
    # anılmamaları BEKLENİR.
    printed = {k for k, c in charts.items() if c.get("printed", True)}
    dead = sorted(printed - used_charts)

    print("\n── ölçülen ──")
    print("  basılı çizelge     %d" % len(printed))
    print("  çözülen gönderme   %d" % refs)
    print("  anılan çizelge     %d" % len(used_charts & printed))

    if args.verbose and first_use:
        print("\n── çizelgeye ilk gönderme ──")
        for key, (gidx, pid) in sorted(first_use.items(), key=lambda x: x[1]):
            print("  %-22s %s" % (key, pid))

    rep.facts.update({
        "printedCharts": len(printed), "resolvedRefs": refs,
        "usedCharts": sorted(used_charts & printed), "deadCharts": dead,
        "badChart": bad_chart, "badCatalogue": bad_cat,
        "badPuzzleRef": bad_puzzle, "badPlateRef": bad_plate,
    })

    rep.check(not bad_chart,
              "⭑ ① HER 'ÇİZELGE X' GÖNDERMESİ ÇÖZÜLÜYOR ⭑ "
              "(boşa düşen bir gönderme okuru kitabın DIŞINA iter)"
              + ("" if not bad_chart else " — ⛔ %s" % bad_chart[:5]))
    rep.check(not bad_cat,
              "⭑ ② HER KATALOG ADI ARAÇLAR LEVHASINDA VAR ⭑"
              + ("" if not bad_cat else " — ⛔ %s" % bad_cat[:5]))
    rep.check(not bad_puzzle,
              "③ metinde anılan her bulmaca kimliği envanterde var"
              + ("" if not bad_puzzle else " — ⛔ %s" % bad_puzzle[:5]))
    rep.check(not bad_plate,
              "④ hiçbir sayfa BAŞKA bir sayfanın levhasını anmıyor"
              + ("" if not bad_plate else " — ⛔ %s" % bad_plate[:5]))
    rep.check(not dead,
              "⑥ basılan her çizelge en az bir kez anılıyor"
              + ("" if not dead else " — ⛔ ÖLÜ: %s" % dead))

    return rep.finish("%d gönderme · %d basılı çizelge" % (refs, len(printed)),
                      args.json)


if __name__ == "__main__":
    sys.exit(main())
