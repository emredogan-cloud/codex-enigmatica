#!/usr/bin/env python3
"""
⭑ OKUR PAKETİ KAPISI ⭑ — bütün kapıların paylaştığı körlük
================================================================================
Faz 2'de şu bulundu ve on bulmacayı etkiliyordu:

    BULMACALAR OKUR PAKETİNDE ÇÖZÜLEMİYORDU.

Levha METNİ vardı — *"altı kemer, her birinin altında bir Sözlük
numarası"* — ama levha VERİSİ yoktu: hangi kemerin kilit taşı çift, hangi
kuş sağa bakıyor, hangi halkanın konturu kapalı. O nitelik haritası
yalnızca **cevap anahtarında** duruyordu.

Ve hiçbir kapı bunu görmedi. Sebebi tek cümledir ve bu kapının varlık
sebebidir:

    BÜTÜN KAPILAR KORUMALI KATMANI DENETLİYORDU.
    HİÇBİRİ OKURUN ELİNE NE GEÇTİĞİNE BAKMIYORDU.

`qa_answerspace` "tam olarak bir üye kabul ediliyor" diyordu ve haklıydı —
ama kabul yordamının dayandığı nitelik okurun elinde yoktu. Kusursuz bir
tekillik ispatı, çözülemeyen bir bulmacanın üzerinde duruyordu.

Sekiz denetim — hepsi TERS YÖNDEN sorar: *okur bunu çözebilir mi?*

  ① her levha bulmacasının okur paketinde bir ŞEKLİ var
  ② ⭑ ŞEKİL AYIRT EDİCİ VERİYİ TAŞIYOR ⭑ — her etiketin künyesi görünür
  ③ her çizelge bulmacasının basılı çizelgesi var ve tam
  ④ her şifre bulmacasının şifreli dizesi okur metninde GÖRÜNÜYOR
  ⑤ her glif bulmacasının glif dizisi şekilde GÖRÜNÜYOR
  ⑥ ⭑ HİÇBİR CEVAP KENDİ SAYFASINDA BEDAVA DURMUYOR ⭑
     (aday kümesinin üyesi olarak durabilir — mantık çizelgesi böyle çalışır)
  ⑦ kapı bulmacasının levhası her girdi için bir satır taşıyor
  ⑧ ⭑ HİÇBİR BULMACA VAR OLMAYAN BİR ÇİZELGEYE GÖNDERMİYOR ⭑

⭑ ⑨⑩⑪ · ÇABA MODELİNİN ÜÇ VARSAYIMI ⭑ (yönerge § 8 sonrası eklendi)

`qa_effort` üç mekanizmayı UCUZ sayar ve üçünün de tek bir gerekçesi var:
okurun aramak zorunda olmadığı şey LEVHADA BASILIDIR. Bu bir varsayımdır
ve varsayımlar boşta durmaz — burada denetlenir:

  ⑨ glif bulmacasının şekli OKUMA YÖNÜNÜ basıyor (▶ veya ▲)
     → yoksa okur iki yönü de dener ve maliyet İKİYE KATLANIR
  ⑩ basılı daraltmanın sütunu çizelgede GERÇEKTEN öbeklenmiş
     → yoksa okur satır satır tarar ve süzgeç 1 değil, n işlemdir
  ⑪ sıra değiştirme bulmacasının BOŞ IZGARASI şekilde basılı

⭑ ⑫ · İKİ SAYFANIN KESİŞİMİ ⭑ — tek sayfaya bakan hiçbir kapının göremediği

Zincirli bir bulmaca, kaynağının cevabını TÜKETİCİNİN sayfasına basmak
ZORUNDADIR: okur elindeki sözcüğü orada arayacaktır. Ama o sütun kaynağın
aday kümesiyle TEK bir üyede kesişirse, okur kaynağı hiç çözmeden cevabını
okur — ve bunu iki ayrı sayfaya bakarak yapar.

⚠ § ⑥ bunu göremez çünkü ⑥ TEK SAYFAYA bakar. İki sayfa ayrı ayrı temizken
kesişimleri sızdırabilir; sızıntı sayfada değil, ARALARINDADIR.
     → yoksa okur ızgarayı kendi çizer ve yazma+okuma iki geçiş olur

⚠ Bu üç denetim düşerse çaba ölçümü de düşer. İki kapı birbirine dayanır:
biri varsayımı kurar, öteki onu doğrular.

⚠ BU KAPI CEVAP İÇERİĞİ YAZDIRMAZ.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
from qa_answerspace import TOOLS, Plate                        # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")

PLATE_ACCEPTANCE = {"plate-attribute", "reachable-via-number-table"}
COORD_ACCEPTANCE = {"reachable-via-grid-coordinates"}
PEN_ACCEPTANCE = {"misclassified-in-printed-pens"}
KEYED_ACCEPTANCE = {"reachable-by-keyed-alphabet"}
# Çapa işaretleri — biri levhada BULUNMALI (çaba modeli buna dayanır).
ANCHOR_MARKS = ("⌖", "▶", "◀", "◄", "▲")
TABLE_ACCEPTANCE = {"table-row"}
GRID_ACCEPTANCE = {"grid-intersection"}
# Okuma yönünü basan işaretler — biri bulunmalı.
DIRECTION_MARKS = ("▶", "▲", "◀", "▼")
CIPHER_GENERATORS = {"cyclic-shift", "reflection-map", "keyed-substitution"}
CIPHER_ACCEPTANCE = {"reachable-by-transposition"}
GLYPH_ACCEPTANCE = {"reachable-by-glyph-reading"}

# Cevabın kendi sayfasında durabilmesi için gereken EN AZ akran sayısı.
# Dört seçildi: bir mantık çizelgesinin en küçük anlamlı hâli beş satırdır
# (cevap + dört akran) ve dörtten az akran, aday kümesini "cevap ve birkaç
# süs" hâline getirir.
MIN_CANDIDATE_PEERS = 4

# ⚠ FAZ 2 BULGUSU — VAR OLMAYAN BİR ÇİZELGEYE GÖNDERME.
# Çizelgeler bir kez yeniden adlandırıldı; başlıklar güncellendi ama üç
# bulmacanın gövdesi eski adlarda kaldı. Sonuç: okur sekiz ayrı cümlede
# olmayan bir çizelgeye gönderiliyordu.
#
# Bu, sözleşmenin DÖRDÜNCÜ sözünün doğrudan ihlalidir ("kitap size bir
# çizelge veriyorsa, o çizelge tek yetkedir") ve en zararlı hata
# cinsindendir: okur bunu KENDİ hatası sanır.
CHART_REF = re.compile(r"Çizelge\s+([A-Z])")


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
    print("  ⭑ OKUR PAKETİ ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)

    pre = pl.preflight(rep, gate_level, "okur paketi")
    if pre is None:
        return rep.finish("denetlenecek okur paketi yok", args.json)
    need, sols, _designs = pre

    book = pl.load_json(BOOK)
    if not book:
        # Manuscript korumalı katmandadır ve CI'da YOKTUR. Orada bu kapı
        # boş koşar ve BUNU SÖYLER — sessizce yeşil yanmaz.
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "okur paketi denetlenemedi")
        rep.warn("okur paketi denetimi BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    plate = Plate(pl.load_json(TOOLS) or {})
    pages = {p["puzzleId"]: p for p in book.get("puzzles", [])}
    lex_no = {w: i + 1 for i, w in enumerate(plate.lexicon)}

    no_page, no_figure, blind_figure, no_table = [], [], [], []
    no_cipher, no_glyph, answer_on_page, gate_rows = [], [], [], []
    dangling_chart = []
    no_direction, no_grouping, no_grid, cross_leak = [], [], [], []
    checked = 0

    # Basılı çizelgelerin GERÇEK harfleri — başlıklardan okunur, elle
    # yazılmaz. İki kaynak, er geç iki farklı liste olur.
    charts = (pl.load_json(TOOLS) or {}).get("charts", {})
    chart_letters = {c.get("id") for c in charts.values() if c.get("id")}
    print("  basılı çizelge harfleri: %s" % ", ".join(sorted(chart_letters)))

    print("\n── okurun eline ne geçiyor ──")
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        page = pages.get(pid)
        if not page:
            no_page.append(pid)
            continue
        checked += 1
        space = rec.get("answerSpace") or {}
        gen, acc = space.get("generator") or {}, space.get("acceptance") or {}
        fig = page.get("figure") or ""
        visible = " ".join(str(page.get(k) or "") for k in
                           ("title", "objective", "readerAction", "input",
                            "figure", "printedTable")) + " " + \
            " ".join(page.get("clues") or []) + " " + \
            " ".join(page.get("constraints") or [])

        # ①② levha
        if acc.get("kind") in PLATE_ACCEPTANCE:
            if not fig.strip():
                no_figure.append(pid)
            elif acc.get("kind") == "plate-attribute":
                # ⭑ Şekil AYIRT EDİCİ olmalı: okur her etiketi künyesinden
                # tanıyabilmeli. Bir etiketin künyesi eksikse o satır
                # okunamaz ve bulmaca eksik veriyle çözülmeye çalışılır.
                missing = [l for l in acc.get("labels", [])
                           if str(lex_no.get(l, 0)) not in fig]
                if missing:
                    blind_figure.append("%s (%d etiket künyesiz)"
                                        % (pid, len(missing)))

        # ③ basılı çizelge
        if acc.get("kind") in GRID_ACCEPTANCE:
            tbl = page.get("printedTable") or ""
            flat = [w for row in acc.get("grid") or [] for w in row]
            if not tbl.strip() or any(w not in tbl for w in flat):
                no_table.append("%s (ızgara eksik)" % pid)

        if acc.get("kind") in TABLE_ACCEPTANCE:
            tbl = page.get("printedTable") or ""
            rows = acc.get("table") or []
            if not tbl.strip():
                no_table.append(pid)
            else:
                miss = [r for r in rows
                        if any(str(v) not in tbl for v in r.values())]
                if miss:
                    no_table.append("%s (%d satır eksik)" % (pid, len(miss)))

        # ④ şifreli dize okur metninde
        ct = gen.get("input") or acc.get("input") or ""
        if (gen.get("kind") in CIPHER_GENERATORS
                or acc.get("kind") in CIPHER_ACCEPTANCE) and ct:
            if ct not in visible:
                no_cipher.append(pid)

        # ⑤ glif dizisi şekilde
        # ⚠ Karşılaştırma BOŞLUKSUZ yapılır: glif işaretleri levhada
        # ARALIKLI basılır (sayma kolaylığı için) ama kayıtta da aynı
        # biçimdedir; ayrılan tek şey satır kırılması ve girintidir.
        if acc.get("kind") in GLYPH_ACCEPTANCE:
            fig_sq = "".join(fig.split())
            groups = ["".join(g.split())
                      for g in (acc.get("glyphs") or "").split("│")]
            groups = [g for g in groups if g]
            if not groups or any(g not in fig_sq for g in groups):
                no_glyph.append(pid)

        # ⑥ ⭑ cevap kendi sayfasında BEDAVA duramaz ⭑
        #
        # ⚠ "Cevap sayfada görünmesin" kuralı OLDUĞU GİBİ YANLIŞTIR ve bunu
        # iki bulmaca gösterdi: bir mantık çizelgesinde cevap, basılı beş
        # satırdan BİRİDİR — okurun işi hangisi olduğunu bulmaktır. Cevabı
        # sayfadan çıkarmak bulmacayı çözülemez yapardı.
        #
        # Doğru kural şudur: cevap sayfada AYIRT EDİLMEMİŞ bir aday kümesinin
        # üyesi olarak durabilir. Tek başına durursa bedavadır.
        ans = rec.get("finalAnswer", "")
        vis_sq = pl.squeeze(visible)
        if ans and pl.squeeze(ans) and pl.squeeze(ans) in vis_sq:
            # ⚠ Kapı II'nin cevapları Çizelge E'dedir. Akranı yalnızca
            # Eşik Sözlüğü'nde aramak, katalog bulmacalarını akransız
            # gösterir ve kapıyı YANLIŞ yerde kırmızı yakardı.
            printed = list(plate.lexicon) + list(plate.bestiary)
            peers = sum(1 for w in printed
                        if w != ans and pl.squeeze(w) in vis_sq)
            if peers < MIN_CANDIDATE_PEERS:
                answer_on_page.append("%s (%d akran)" % (pid, peers))

        # ⭑ ⑨ · ÇABA MODELİNİN BİRİNCİ VARSAYIMI ⭑
        # `qa_effort` glif bulmacasını TEK yön okur sayar. Bunun tek
        # dayanağı levhanın okuma yönünü BASMASIdır. Basmıyorsa okur iki
        # yönü de dener ve gerçek maliyet ölçtüğümüzün iki katıdır.
        if acc.get("kind") in GLYPH_ACCEPTANCE:
            if not any(m in fig for m in DIRECTION_MARKS):
                no_direction.append(pid)

        # ⭑ ⑩ · İKİNCİ VARSAYIM · basılı daraltma ⭑
        # Bir süzgeci "bir bakış" saymak, çizelgenin o sütuna göre
        # ÖBEKLENMİŞ basılmasına dayanır: eşit değerler bitişik durmalı ve
        # öbekler arasında görünür bir ayraç olmalıdır.
        for col in acc.get("printedNarrowing") or []:
            tbl = page.get("printedTable") or ""
            vals = [r.get(col) for r in acc.get("table") or []]
            runs = [v for i, v in enumerate(vals) if i == 0 or v != vals[i - 1]]
            if col not in tbl:
                no_grouping.append("%s (%s sütunu basılı değil)" % (pid, col))
            elif len(runs) != len(set(runs)):
                no_grouping.append("%s (%s değerleri bitişik değil)" % (pid, col))
            elif "───" not in tbl:
                no_grouping.append("%s (öbek ayracı yok)" % pid)

        # ⭑ ⑪ · ÜÇÜNCÜ VARSAYIM · boş ızgara basılı ⭑
        if acc.get("printedGrid"):
            if fig.count("┬") < 1 or fig.count("│") < 2:
                no_grid.append(pid)

        # ⭑ ⑫ · İKİ SAYFANIN KESİŞİMİ ⭑
        for src in p.get("dependencies") or []:
            src_rec = sols.get(src) or {}
            src_acc = ((src_rec.get("answerSpace") or {})
                       .get("acceptance") or {})
            src_ans = src_rec.get("finalAnswer") or ""
            if not src_ans:
                continue
            # Okurun kaynak için elediği aday kümesi: levha bulmacasında
            # etiketler, ötekilerde mekanizmanın açığa vurduğu UZUNLUK.
            if src_acc.get("kind") == "plate-attribute":
                plausible = set(src_acc.get("labels") or [])
            else:
                printed = list(plate.lexicon) + list(plate.bestiary)
                plausible = {w for w in printed if len(w) == len(src_ans)}
            keys = set()
            for f in acc.get("filters") or []:
                keys |= {str(r.get(f["col"]))
                         for r in acc.get("table") or []}
            if not keys:
                continue
            shared = keys & plausible
            if len(shared) < 2:
                cross_leak.append("%s ← %s (%d ortak aday)"
                                  % (pid, src, len(shared)))

        # ⭑ ⑬ · KAPI II · İMZA MEKANİĞİNİN BASILI DAYANAKLARI ⭑
        if acc.get("kind") in COORD_ACCEPTANCE:
            fig_sq = "".join(fig.split())
            miss = [st for st in ("%d·%d" % (r, c)
                                  for r, c in acc.get("coordinates") or [])
                    if st not in fig_sq]
            if not any(m in fig for m in ANCHOR_MARKS):
                no_direction.append("%s (çapa işareti yok)" % pid)
            if miss:
                no_glyph.append("%s (%d istasyon şekilde yok)" % (pid, len(miss)))
        if acc.get("kind") in PEN_ACCEPTANCE:
            tbl = page.get("printedTable") or ""
            need = list(acc.get("items") or []) + list(
                acc.get("candidateRules") or [])
            if not tbl.strip() or any(str(x) not in tbl for x in need):
                no_table.append("%s (nitelik çizelgesi eksik)" % pid)
        if acc.get("kind") in KEYED_ACCEPTANCE:
            row = acc.get("keyedRow") or ""
            if "".join(row.split()) not in "".join(fig.split()):
                no_cipher.append("%s (anahtar satırı basılı değil)" % pid)

        # ⑧ ⭑ var olmayan bir çizelgeye gönderme ⭑
        for letter in set(CHART_REF.findall(visible)):
            if letter not in chart_letters:
                dangling_chart.append("%s → Çizelge %s" % (pid, letter))

        # ⑦ kapı levhası
        if p.get("type") == "gate":
            deps = p.get("dependencies") or []
            lines = [l for l in fig.splitlines() if l.startswith("│")]
            if len(lines) < len(deps):
                gate_rows.append("%s (%d satır < %d girdi)"
                                 % (pid, len(lines), len(deps)))

    rep.facts.update({"checked": checked, "pages": len(pages)})

    rep.check(not no_page, "her yazılmış bulmacanın okur sayfası var"
              + ("" if not no_page else " — ⛔ SAYFASIZ: %s" % no_page[:5]))
    rep.check(not no_figure,
              "⭑ her levha bulmacasının okur paketinde ŞEKLİ var ⭑"
              + ("" if not no_figure else " — ⛔ ÇÖZÜLEMEZ: %s" % no_figure[:5]))
    rep.check(not blind_figure,
              "⭑ ŞEKİL AYIRT EDİCİ VERİYİ TAŞIYOR ⭑ (her etiket künyeli)"
              + ("" if not blind_figure else " — ⛔ KÖR ŞEKİL: %s"
                 % blind_figure[:5]))
    rep.check(not no_table, "her çizelge bulmacasının basılı çizelgesi tam"
              + ("" if not no_table else " — ⛔ EKSİK: %s" % no_table[:5]))
    rep.check(not no_cipher, "şifreli dize okur metninde görünüyor"
              + ("" if not no_cipher else " — ⛔ GÖRÜNMEZ: %s" % no_cipher[:5]))
    rep.check(not no_glyph, "glif dizisi şekilde görünüyor"
              + ("" if not no_glyph else " — ⛔ GÖRÜNMEZ: %s" % no_glyph[:5]))
    rep.check(not answer_on_page,
              "⭑ HİÇBİR CEVAP KENDİ SAYFASINDA BEDAVA DURMUYOR ⭑ "
              "(≥%d akran gerekir)" % MIN_CANDIDATE_PEERS
              + ("" if not answer_on_page
                 else " — ⛔ BEDAVA CEVAP: %s" % answer_on_page[:5]))
    rep.check(not no_direction,
              "⭑ ⑨ GLİF LEVHASI OKUMA YÖNÜNÜ BASIYOR ⭑ (çaba modeli buna "
              "dayanır)"
              + ("" if not no_direction else " — ⛔ YÖNSÜZ: %s" % no_direction[:5]))
    rep.check(not no_grouping,
              "⭑ ⑩ BASILI DARALTMA GERÇEKTEN ÖBEKLENMİŞ ⭑ (çaba modeli buna "
              "dayanır)"
              + ("" if not no_grouping else " — ⛔ %s" % no_grouping[:5]))
    rep.check(not no_grid,
              "⭑ ⑪ SIRA DEĞİŞTİRMENİN BOŞ IZGARASI BASILI ⭑ (çaba modeli "
              "buna dayanır)"
              + ("" if not no_grid else " — ⛔ IZGARASIZ: %s" % no_grid[:5]))
    rep.check(not cross_leak,
              "⭑ ⑫ ZİNCİRİN KAYNAĞI İKİ SAYFANIN KESİŞİMİNDEN OKUNAMIYOR ⭑"
              + ("" if not cross_leak else " — ⛔ %s" % cross_leak[:5]))
    rep.check(not dangling_chart,
              "⭑ HİÇBİR BULMACA VAR OLMAYAN BİR ÇİZELGEYE GÖNDERMİYOR ⭑"
              + ("" if not dangling_chart
                 else " — ⛔ SARKAN GÖNDERME: %s" % dangling_chart[:5]))
    rep.check(not gate_rows, "kapı levhası her girdi için bir satır taşıyor"
              + ("" if not gate_rows else " — EKSİK: %s" % gate_rows[:5]))

    return rep.finish("%d okur sayfası denetlendi" % checked, args.json)


if __name__ == "__main__":
    sys.exit(main())
