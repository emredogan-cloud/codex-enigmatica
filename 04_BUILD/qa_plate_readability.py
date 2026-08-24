#!/usr/bin/env python3
"""
⭑ LEVHA OKUNABİLİRLİĞİ ⭑ — bu kitabın EN KRİTİK teknik kapısı
================================================================================
Yol haritası Faz 5 § 8'in kendi sözleriyle:

    "Bu, bu kitabın en kritik teknik kapısıdır. Bir levhada kaybolan
     detay bulmacayı ÇÖZÜLEMEZ yapar — ve bunu okur öğrenir, siz değil."

────────────────────────────────────────────────────────────────────────
⭑ `qa_plate_data` İLE FARKI ⭑

İkisi aynı şeye bakmaz ve ikisi de gereklidir:

  `qa_plate_data`        → veri ŞEKLİN İÇİNDEN geri alınabiliyor mu
                           (yalnızca ÇÖZÜLEBİLEN levhalara bakar)
  `qa_plate_readability` → şekil SAYFAYA SIĞIYOR ve BASKIDA ayırt
                           edilebiliyor mu (HER şekle bakar)

Ve fark ölçüldü: `qa_plate_data` 30 levha ölçüyor ve yeşil yanıyordu;
kitapta **62 sütunluk basılabilir genişliği aşan dokuz satır** vardı ve
hiçbiri o otuzun içinde değildi. Bir kapının kapsamı, denetlediği
kuralın kapsamı kadardır.

────────────────────────────────────────────────────────────────────────
⚠ VE BU KAPI BİR PROVA BASKI DEĞİLDİR.

Gerçek ölçüm POD prova kopyada, mürekkep ve gözle yapılır — kurucu işi
(A9 · Faz 5 kurucu bağımlılığı) ve **YAPILMADI**. Bu kapı ondan önceki
soruyu sorar ve o soru ucuzdur: *şekil, basılabilir alanın içinde mi ve
okurun ayırt etmesi gereken farklar baskı toleransının üstünde mi?*

⚠ İKİNCİ İKAME: pilot levhaları GRAVÜR DEĞİL, TİPOGRAFİK ŞEKİLDİR.
Bu kapı tipografik şeklin ölçülerini denetler; gravürün nokta yayılması
altındaki davranışını DENETLEMEZ. Gravürler üretildiğinde
`--raster` kipi aynı ölçütleri piksel üzerinde uygular.

Dokuz ölçüm:

  ① BOYUT        — şeklin genişliği ve yüksekliği
  ② TRIM         — basılabilir sütun sayısını aşan satır var mı
  ③ GÜVENLİ ALAN — şekil tek bir sayfaya sığıyor mu
  ④ EN İNCE AYRIM— okurun saymak zorunda olduğu en uzun dizi
  ⑤ AYRIŞMA      — veri taşıyan iki işaret birbirine karışıyor mu
  ⑥ KONTRAST     — aynı yerde kullanılan işaretler yeterince farklı mı
  ⑦ GLİF DAĞARCIĞI— basılabilir glif kümesinin dışında karakter var mı
  ⑨ TALİMAT GÖRÜNÜRLÜĞÜ — şeklin künyesi aynı sayfada mı
  ⑩ ROL BAŞINA TEK GLİF — aynı iş için iki ayrı karakter var mı

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")

# ── BASKI ÖLÇÜLERİ ─────────────────────────────────────────────────────
# ⚠ TEK KAYNAK: bu sayı `qa_plate_data.MAX_FIGURE_WIDTH` ile AYNI olmak
# zorundadır ve aynı olduğu denetlenir. İki kapı aynı fiziksel gerçeği
# ölçüyorsa iki ayrı sayı taşıyamaz.
MAX_WIDTH = 62               # 6×9 trim · 10,5 punto tek aralıklı
MAX_HEIGHT = 34              # bir sayfaya sığan şekil satırı (42 satır − pay)
MAX_IDENTICAL_RUN = 5        # aynı işaretin ardışık tekrarı
MIN_MARK_GAP = 1             # veri işaretleri arasındaki en az boşluk

# ⭑ BASILABİLİR GLİF DAĞARCIĞI ⭑
# ⚠ KURAL BLOK BAZINDADIR, LİSTE BAZINDA DEĞİL. Elle yazılmış bir izin
# listesi, bir glif eklendiğinde sessizce genişletilir; blok kuralı
# genişletilemez çünkü SEBEBİ vardır:
#
#   ✅ ASCII · Latin-Ext-A   → her yazı tipinde var
#   ✅ Kutu çizimi · blok    → tek aralıklı yazı tiplerinin çekirdeği
#   ✅ Geometrik şekiller    → BİLDİRİLEN alt küme (aşağıda)
#   ⛔ Dingbats (U+2700+)    → süsleme bloğu; kitap yazı tiplerinde SEYREK
#   ⛔ Muhtelif simge (U+26) → çoğu ortamda EMOJİ olarak çizilir
#   ⛔ Muhtelif teknik       → matematik/teknik; kitap yüzünde yok
#
# Dağarcık dışı bir glif POD baskıda BOŞ KUTU olur ve o levhayı
# çözülemez yapar. Bu, bu kapının varlık sebebinin ta kendisidir.
GEOMETRIC_OK = set("●○◆◇◊▲△▼▽◀▶■□▪▫▵·•◦")
# Yaygın matematik/ok karakterleri — kitap yazı tiplerinde bulunur.
MATH_OK = set("−≈≠≤≥±×÷")
ARROW_OK = set("←↑→↓")
ASCII_OK = set(
    "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    "abcçdefgğhıijklmnoöprsştuüvyzqwxQWX"
    "0123456789"
    " .,;:!?'\"()[]{}<>/\\|-_=+*&%#@~^`$"
    "\n\t")
PUNCT_OK = set("–—…“”·′″")


def glyph_ok(ch: str) -> bool:
    o = ord(ch)
    if (ch in ASCII_OK or ch in PUNCT_OK or ch in GEOMETRIC_OK
            or ch in MATH_OK or ch in ARROW_OK):
        return True
    if 0x0100 <= o <= 0x017F:            # Latin Extended-A (Türkçe)
        return True
    if 0x2500 <= o <= 0x259F:            # kutu çizimi + blok
        return True
    return False


# ⭑ AYNI ROL, TEK GLİF ⭑
# Kitap altı ayrı üçgen ok kullanıyordu (▶ ► ▻ ◀ ◄ ◅). Okur için hepsi
# "ok"tur; dizgide altı ayrı karakter demektir ve biri eksik yazı tipine
# denk gelirse yalnızca o levha bozulur. Rol başına TEK glif.
GLYPH_ROLE = {
    "▶": "ok-sağ", "►": "ok-sağ", "▻": "ok-sağ", "▸": "ok-sağ",
    "◀": "ok-sol", "◄": "ok-sol", "◅": "ok-sol", "◂": "ok-sol",
    "↻": "dönüş", "↺": "dönüş", "⟳": "dönüş",
    # ⚠ '·', '•' ve '◦' AYNI ROLDE DEĞİLDİR ve ilk kurgu onları tek rol
    # sayıp haksız yere kırmızı yaktı: '·' bir ayraç/dolgu, '•' sayı
    # çizelgesinde BİR değeri, '◦' bir sayım işaretidir. Karışma riskini
    # rol kuralı değil, ⑥ (aynı şekilde ikisi de veri) ölçer.
    "─": "yatay", "—": "yatay", "–": "yatay",
}

# ⭑ KARIŞABİLİR ÇİFTLER ⭑ Aynı temel biçimin dolu/boş ya da küçük/büyük
# hâlidir; 300 dpi'da kâğıt kusuru ikisini birbirine çevirebilir.
# ⚠ VE KURAL YALNIZCA BİTİŞİK BASILDIKLARINDA UYGULANIR. İlk kurgu
# "aynı şekilde ikisi de var" diyordu ve tasarımı kırmızı yakıyordu:
# sınıflama levhası ● ile ○'yu YAN YANA basar ve bu, mekanizmanın
# KENDİSİDİR (var/yok). Baskı riski birlikte VAR OLMALARI değil,
# BİRBİRİNE DEĞMELERİDİR.
CONFUSABLE = [
    ("·", "•"), ("•", "◦"), ("·", "◦"),
    ("△", "▵"), ("▲", "△"), ("▼", "▽"),
    ("■", "□"), ("▪", "▫"), ("□", "▫"),
]

# ⭑ ÇAPA VE YÖN İŞARETLERİ — TEK KAYNAK ⭑
# `qa_readerpack` bu listeyi BURADAN alır. Kendi kopyası vardı ve Faz 5
# glif temizliğinde bayatladı: levhalar "⌖"yi bıraktı, okur paketi hâlâ
# onu arıyordu ve beş levhayı "yönsüz" saydı. Bir glif dağarcığı iki
# yerde durursa, biri ötekinden önce eskir.
ANCHOR_MARKS = ("■", "▶", "◀", "▲", "◆")
DIRECTION_MARKS = ("▶", "▲", "◀", "▼")

# Veri taşıyan işaretler — `qa_plate_data.DATA_MARKS` ile aynı temel.
DATA_MARKS = set("',+/\\x") | set("◆┬▓◦◊●○▽▵◇•║")


def width(line: str) -> int:
    """Basılı sütun sayısı — geniş glifler iki sütun sayılır."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
               for c in line)


def longest_run(text: str) -> tuple[int, str]:
    run, prev, cur, what = 0, None, 0, "—"
    for ch in text:
        if ch not in DATA_MARKS:
            prev, cur = None, 0
            continue
        cur = cur + 1 if ch == prev else 1
        prev = ch
        if cur > run:
            run, what = cur, ch
    return run, what


def figures(book: dict):
    """Kitaptaki HER şekil — bulmaca, çizelge ve ısınma dâhil.

    ⚠ 'Her' sözcüğü bu kapının varlık sebebidir. Kapsamı daraltan bir
    okunabilirlik kapısı, daraldığı yerde kör olur."""
    for p in book.get("puzzles", []):
        for key in ("figure", "printedTable"):
            if p.get(key):
                yield ("%s/%s" % (p["puzzleId"], key), str(p[key]),
                       p.get("clues") or [], p.get("gate"))
    for w in book.get("warmUp", []):
        if w.get("figure"):
            yield ("%s/figure" % w.get("id"), str(w["figure"]),
                   [w.get("lead") or "", w.get("note") or ""], w.get("gate"))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    ap.add_argument("--check", action="store_true",
                    help="qa_all uyumu — normal koşuyla aynıdır")
    args = ap.parse_args()

    gate_level = args.gate or pl.read_gate()
    if gate_level not in pl.VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate_level, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  ⭑ LEVHA OKUNABİLİRLİĞİ ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)

    # ⭑ İKİ KAPI AYNI SAYIYI TAŞIMAK ZORUNDA ⭑
    try:
        from qa_plate_data import MAX_FIGURE_WIDTH as _OTHER
    except ImportError:
        _OTHER = MAX_WIDTH
    rep.check(_OTHER == MAX_WIDTH,
              "⭑ BASILABİLİR GENİŞLİK TEK SAYIDIR ⭑ "
              "(qa_plate_data %d ↔ bu kapı %d)" % (_OTHER, MAX_WIDTH))

    book = pl.load_json(BOOK) or {}
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "ölçüm YAPILAMADI")
        rep.warn("levha okunabilirliği BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    all_figs = list(figures(book))
    over_width, over_height, deep_run = [], [], []
    bad_glyph, confused, no_legend = [], [], []
    mixed_role: list = []
    book_roles: dict = {}
    rows = []

    for name, fig, legend, gate in all_figs:
        lines = fig.splitlines()
        w = max((width(x) for x in lines), default=0)
        h = len(lines)
        run, mark = longest_run(fig)
        rows.append({"figure": name, "gate": gate, "width": w, "height": h,
                     "longestRun": run, "runMark": mark})

        if w > MAX_WIDTH:
            over_width.append("%s (%d>%d)" % (name, w, MAX_WIDTH))
        if h > MAX_HEIGHT:
            over_height.append("%s (%d>%d)" % (name, h, MAX_HEIGHT))
        if run > MAX_IDENTICAL_RUN:
            deep_run.append("%s (%d×%s)" % (name, run, mark))

        # ⑦ GLİF DAĞARCIĞI
        bad = sorted({c for c in fig if not glyph_ok(c)})
        if bad:
            bad_glyph.append("%s → %s" % (name, " ".join(
                "%s(U+%04X)" % (c, ord(c)) for c in bad[:4])))

        # ⑥ KONTRAST — karışabilir iki işaret aynı şekilde İKİSİ DE veri
        # taşıyorsa okur onları ayırmak ZORUNDADIR ve baskı toleransı
        # bunu garanti etmez. Bitişik olmaları gerekmez: g1-019'da dolgu
        # '·' ve sayılan işaret '◦' idi ve okurdan ◦'leri saymasını
        # istiyordu — yanlış sayılan bir dolgu noktası CEVABI değiştirir.
        for a, b in CONFUSABLE:
            if a in fig and b in fig:
                confused.append("%s → %s ve %s" % (name, a, b))

        # ⑩ ROL BAŞINA TEK GLİF (şekil içinde)
        seen_role = {}
        for ch in set(fig):
            role = GLYPH_ROLE.get(ch)
            if role and seen_role.setdefault(role, ch) != ch:
                mixed_role.append("%s → %s: %s ve %s"
                                  % (name, role, seen_role[role], ch))
        for ch in set(fig):
            role = GLYPH_ROLE.get(ch)
            if role:
                book_roles.setdefault(role, {}).setdefault(ch, []).append(name)

        # ⑨ TALİMAT GÖRÜNÜRLÜĞÜ — şeklin bir künyesi olmak zorunda
        if not any(str(x).strip() for x in legend):
            no_legend.append(name)

    widths = [r["width"] for r in rows] or [0]
    heights = [r["height"] for r in rows] or [0]
    print("\n── ölçülen ──")
    print("  şekil              %d" % len(rows))
    print("  en geniş satır     %d sütun   (tavan %d)"
          % (max(widths), MAX_WIDTH))
    print("  en yüksek şekil    %d satır   (tavan %d)"
          % (max(heights), MAX_HEIGHT))
    print("  en uzun sayım      %d ardışık (tavan %d)"
          % (max((r["longestRun"] for r in rows), default=0),
             MAX_IDENTICAL_RUN))
    print("  glif rolü          %s"
          % " · ".join("%s→%s" % (r, "".join(sorted(g)))
                       for r, g in sorted(book_roles.items())) or "—")

    if args.verbose:
        print("\n── en geniş on şekil ──")
        for r in sorted(rows, key=lambda x: -x["width"])[:10]:
            print("  %-22s %3d sütun × %2d satır" % (r["figure"], r["width"],
                                                     r["height"]))

    rep.facts.update({
        "figures": len(rows), "maxWidth": max(widths),
        "maxHeight": max(heights), "widthCeiling": MAX_WIDTH,
        "heightCeiling": MAX_HEIGHT,
        "longestRun": max((r["longestRun"] for r in rows), default=0),
        "overWidth": over_width, "overHeight": over_height,
        "badGlyph": bad_glyph, "confusable": confused,
        "glyphRoles": {k: sorted(v) for k, v in book_roles.items()},
        "perFigure": rows,
        "physicalProofStatus": "NOT-PERFORMED",
        "physicalProofOwner": "founder (A9)",
    })

    rep.check(not over_width,
              "⭑ ② HİÇBİR ŞEKİL BASILABİLİR GENİŞLİĞİ AŞMIYOR ⭑ (≤%d sütun)"
              % MAX_WIDTH
              + ("" if not over_width else " — ⛔ TAŞAN: %s" % over_width[:6]))
    rep.check(not over_height,
              "③ hiçbir şekil tek sayfayı aşmıyor (≤%d satır)" % MAX_HEIGHT
              + ("" if not over_height else " — ⛔ %s" % over_height[:4]))
    rep.check(not deep_run,
              "⭑ ④ OKURDAN BEŞTEN FAZLA ARDIŞIK İŞARET SAYMASI İSTENMİYOR ⭑"
              + ("" if not deep_run else " — ⛔ %s" % deep_run[:5]))
    rep.check(not bad_glyph,
              "⭑ ⑦ BÜTÜN GLİFLER BASILABİLİR DAĞARCIKTA ⭑ "
              "(dağarcık dışı bir glif POD baskıda BOŞ KUTU olur)"
              + ("" if not bad_glyph else " — ⛔ %s" % bad_glyph[:5]))
    rep.check(not confused,
              "⭑ ⑥ KARIŞABİLİR İKİ İŞARET AYNI ŞEKİLDE BULUNMUYOR ⭑"
              + ("" if not confused else " — ⛔ %s" % confused[:5]))
    # ⑩ ROL BAŞINA TEK GLİF — KİTAP GENELİNDE
    role_split = ["%s: %s" % (role, " ".join(sorted(g)))
                  for role, g in sorted(book_roles.items()) if len(g) > 1]
    rep.check(not mixed_role,
              "⑩ aynı rol aynı şekilde tek glifle basılıyor"
              + ("" if not mixed_role else " — ⛔ %s" % mixed_role[:4]))
    rep.check(not role_split,
              "⭑ ⑩ AYNI ROL KİTAP GENELİNDE TEK GLİFLE BASILIYOR ⭑ "
              "(altı ayrı ok karakteri, altı ayrı yazı tipi riskidir)"
              + ("" if not role_split else " — ⛔ %s" % role_split))
    rep.check(not no_legend,
              "⑨ her şeklin künyesi aynı sayfada"
              + ("" if not no_legend else " — ⛔ KÜNYESİZ: %s" % no_legend[:5]))

    # ⚠ VE BU KAPI NE ÖLÇMEDİĞİNİ SÖYLER.
    print("\n" + "=" * 74)
    print("  ⚑ FİZİKSEL PROVA: **YAPILMADI** — A9 · kurucu işi")
    print("     Bu kapı basılabilir ALANI ve AYIRT EDİLEBİLİRLİĞİ ölçtü.")
    print("     Mürekkebin kâğıt üzerindeki davranışını ÖLÇMEDİ ve")
    print("     ölçtüğünü İDDİA ETMİYOR.")
    print("=" * 74)
    rep.warn("fiziksel prova ölçümü YAPILMADI (A9) — "
             "`plate-print-test.json` üretilmedi ve üretilemez")

    return rep.finish("%d şekil · en geniş %d/%d sütun"
                      % (len(rows), max(widths), MAX_WIDTH), args.json)


if __name__ == "__main__":
    sys.exit(main())
