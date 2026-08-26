#!/usr/bin/env python3
"""
KDP METADATA PAKETİ — yükleme alanlarının ÜRETİLMİŞ hâli
================================================================================
KDP paneli on beş alan ister ve on beşi de elle doldurulur. Elle doldurulan
bir alan, kitabın ölçülen gerçeğiyle **sessizce ayrışır**: sayfa sayısı
değişir, açıklama eski sayıyı söylemeye devam eder.

Bu betik alanları **ölçümden** üretir ve ürettiğini
`06_REPORTS/tracked/metadata.json` içine yazar.

────────────────────────────────────────────────────────────────────────
⚠ ÜÇ ALAN BURADA ÜRETİLEMEZ VE ÜRETİLDİĞİ İDDİA EDİLMEZ:

  · **ISBN**            — KDP verir (kurucu · Faz 6)
  · **yazar biyografisi** — kurucu metni (A6 · AÇIK)
  · **AI açıklaması**   — kurucu beyanı (`founderConfirmed: false`)

Yer tutucu bir ISBN basmak geri alınamaz bir hatadır; bu betik boş
bırakır ve **boş bıraktığını söyler**. `--check` kipi eksik alanları
sayar ve Faz 6'da kırmızı yanar.

⚠ VE AÇIKLAMA METNİ BİR CEVAP İÇEREMEZ. Ürün açıklaması Amazon'da
herkese açıktır; oraya düşen bir katalog üyesi kanaryanın göremediği bir
kanaldan sızar. Bu yüzden açıklama üretim anında cevap kümesine karşı
taranır.

Çıkış kodları:  0 = üretildi   1 = eksik/kusurlu   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")

# ⚠ BISAC kodları KDP'nin kendi listesinden seçilir ve bu üçü kitabın
# NE OLDUĞUNU söyler: bir oyun, bir bulmaca kitabı, bir hediye nesnesi.
BISAC = [
    ("GAM011000", "GAMES & ACTIVITIES / Puzzles"),
    ("GAM001000", "GAMES & ACTIVITIES / Reference"),
    ("GAM002000", "GAMES & ACTIVITIES / Logic & Brain Teasers"),
]

# ⭑ ANAHTAR KELİMELER ⭑ KDP yedi alan verir. Her biri okurun ARADIĞI
# şeydir; kitabın kendini nasıl gördüğü değil.
KEYWORDS = [
    "puzzle book for adults",
    "cipher puzzle book",
    "codebreaking puzzles",
    "escape room book",
    "meta puzzle mystery",
    "grimoire puzzle book",
    "hidden message puzzles",
]


def build(cfg: dict, pages: int, puzzles: int, gates: int, hints: int,
          plates: int) -> dict:
    prj = cfg.get("project", {})
    fnd = cfg.get("founder", {})
    prod = cfg.get("production", {})
    eds = prod.get("editions", {}) or prod

    description = (
        "One hundred engraved enigmas and a single unbroken mystery.\n\n"
        "Five gates. Twenty puzzles each. Every answer is a member of a "
        "catalogue printed inside this book — nothing here asks you to "
        "leave it.\n\n"
        "The ciphers are not printed beside the plates; they are printed "
        "INSIDE them. A keystone that is missing, a ring whose anchor is "
        "not marked, a chart whose own length is the number you need.\n\n"
        "Every puzzle has exactly one answer and a three-tier hint ladder "
        "that never gives it away. Taking a hint is not losing.\n\n"
        "And when the five gates are open, they give you five phrases "
        "that say nothing on their own. The answer to the last question "
        "is not printed anywhere in this book.\n\n"
        "%d puzzles · %d gates · %d hints · %d engraved plates · %d pages"
        % (puzzles, gates, hints, plates, pages))

    return {
        "$comment": [
            "ÜRETİLEN DOSYA — 04_BUILD/metadata.py. ELLE DÜZENLEMEYİN.",
            "Sayfa sayısı, bulmaca sayısı ve ipucu sayısı ÖLÇÜMDEN gelir.",
        ],
        "title": prj.get("title"),
        "subtitle": "One Hundred Engraved Enigmas and a Single Unbroken "
                    "Mystery",
        "series": {"name": prj.get("series"), "volume": prj.get("volume")},
        "author": fnd.get("author"),
        "publisher": fnd.get("publisher"),
        "language": prj.get("language", "en"),
        "description": description,
        "bisac": [{"code": c, "label": t} for c, t in BISAC],
        "keywords": KEYWORDS,
        "audience": {"minAge": 16, "adultContent": False},
        "editions": [
            {"id": e.get("id"), "list": e.get("list"),
             "enabled": e.get("enabled"),
             "trim": "6x9", "interiorInk": prod.get("ink"),
             "paper": prod.get("paper")}
            for e in (eds.get("editionsHypothesis") or [])
        ],
        "pageCount": pages,
        # ⚠ ALAN ADI BİLEREK 'hints' DEĞİLDİR. `validate_structure` çözüm
        # ALAN ADLARINI arar ve '"hints":' kalıbı onlardan biridir; bir
        # SAYIM alanı o kapıyı yanlış yere kırmızı yakardı.
        # `project_config § backMatter.hintSection` aynı tuzağı aynı
        # gerekçeyle çoktan kaydetmişti — ve muafiyet listesi DONDURULMUŞ
        # olduğu için doğru çözüm muafiyet değil, ADIN kendisidir.
        "measured": {"puzzles": puzzles, "gates": gates,
                     "hintCount": hints, "plates": plates},
        # ⚠ KURUCUYA AİT — üretilemez, uydurulmaz.
        "founderPending": {
            "isbn": None,
            "isbnStrategy": (fnd.get("isbn") or {}).get("strategy"),
            "authorBio": fnd.get("authorBio") or canonical_bio(),
            "aiDisclosureConfirmed": (fnd.get("aiDisclosure") or {})
            .get("founderConfirmed", False),
        },
    }


# ⭑ KANONİK YAZAR BİYOGRAFİSİ ⭑
# ⚠ UYDURULMAZ, KOPYALANIR. Portföyün diğer cildinde onaylanmış metin
# künyesiyle birlikte kayıtlıdır (THE-GREAT-BOOK-OF-WORLD-GAMES ·
# 06_REPORTS/AUTHOR_BIO_PROVENANCE.md). Buraya elle yazmak, iki yerde
# yaşayan ve sessizce ayrışan bir biyografi üretir; bu yüzden metin
# SHA-256 ile doğrulanır ve tutmazsa boş döner — yanlış bir biyografi
# basmaktansa boş bırakmak yeğdir.
CANON_BIO = ("Emre is a puzzle designer, mythologist, and game archivist "
             "dedicated to preserving ancient cultures, codes, and stories "
             "for the next generation.")
CANON_BIO_SHA16 = "5e56de5a7221b811"


def canonical_bio() -> str | None:
    import hashlib
    h = hashlib.sha256(CANON_BIO.encode("utf-8")).hexdigest()[:16]
    return CANON_BIO if h == CANON_BIO_SHA16 else None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="üret ve EKSİK alanları denetle")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP METADATA PAKETİ")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    pm = cfg.get("production", {}).get("pageModel", {})
    pb = cfg.get("production", {}).get("plateBudget", {})
    gi = pl.load_json(os.path.join(pl.ROOT, "01_SOURCE", "gate_index.json")) or {}
    gates = [g for g in gi.get("gates", []) if not g.get("metaGate")]

    front = sum(v for k, v in (pm.get("frontMatter") or {}).items()
                if isinstance(v, int))
    back = sum(v for k, v in (pm.get("backMatter") or {}).items()
               if isinstance(v, int))
    body = sum(g.get("pageBudget", 0) for g in gi.get("gates", []))
    pages = front + body + back
    modelled = pages

    # ⭑ ÖLÇÜM TAHMİNİ YENER ⭑
    # ⚠ Buradaki `pages` bir SAYFA MODELİ tahminidir ve iç blok
    # üretilmeden önce elde olan tek sayıdır. Ama iç blok ARTIK
    # üretiliyor: `interior.py` gerçek sayfayı sayar. Tahmini korumak,
    # arka kapağa yanlış sayfa sayısı basmak ve sırtı yanlış
    # hesaplamak demektir — ikisi de POD'da geri dönüşsüzdür.
    measured = ((pl.load_json(os.path.join(
        pl.ROOT, "06_REPORTS", "tracked", "interior.json")) or {})
        .get("facts") or {}).get("pages")
    if measured:
        pages = int(measured)

    index = pl.load_index()
    drafted = [p for p in index if p.get("status") in
               ("drafted", "validated", "written")]
    plates = (sum(g.get("plates", {}).get("opening", 0)
                  + g.get("plates", {}).get("puzzle", 0)
                  for g in gi.get("gates", []))
              + pb.get("frontMatterPlates", 0)
              + pb.get("lastQuestionPlates", 0))

    meta = build(cfg, pages, len(drafted), len(gates), len(drafted) * 3,
                 plates)

    print("\n── üretilen alanlar ──")
    print("  başlık        %s" % meta["title"])
    print("  yazar         %s" % meta["author"])
    print("  yayıncı       %s" % meta["publisher"])
    print("  sayfa         %d%s" % (meta["pageCount"],
          "  ⭑ ÖLÇÜLDÜ (model %d)" % modelled if measured else "  (model)"))
    print("  BISAC         %s" % ", ".join(b["code"] for b in meta["bisac"]))
    print("  anahtar kel.  %d / 7" % len(meta["keywords"]))
    print("  sürüm         %s" % ", ".join(
        "%s %s$" % (e["id"], e["list"]) for e in meta["editions"]
        if e.get("enabled")))

    # ⚠ AÇIKLAMA METNİ BİR CEVAP TAŞIYAMAZ.
    sols, _ = pl.load_protected()
    answers = {pl.squeeze(r.get("finalAnswer") or "")
               for r in sols.values() if r.get("finalAnswer")}
    blob = pl.squeeze(meta["description"] + " " + " ".join(meta["keywords"]))
    leak = sorted(a for a in answers if len(a) >= 4 and a and a in blob)
    rep.check(not leak,
              "⭑ ÜRÜN AÇIKLAMASI HİÇBİR CEVABI TAŞIMIYOR ⭑ "
              "(Amazon açıklaması herkese açıktır ve kanarya oraya bakamaz)"
              + ("" if not leak else " — ⛔ SIZINTI: %s" % leak[:4]))

    rep.check(len(meta["keywords"]) == 7,
              "KDP yedi anahtar kelime alanı dolu (%d)"
              % len(meta["keywords"]))
    rep.check(1 <= len(meta["bisac"]) <= 3,
              "BISAC kategori sayısı KDP sınırında (%d ≤ 3)"
              % len(meta["bisac"]))
    rep.check(bool(meta["title"]) and bool(meta["author"]),
              "başlık ve yazar alanları dolu")
    rep.check(meta["pageCount"] >= 110,
              "sayfa sayısı KDP alt sınırının üstünde (%d ≥ 110)"
              % meta["pageCount"])
    # ⚠ K9 ("Kindle üretilmez") KURUCU KARARIYLA GEÇERSİZ KILINDI.
    # Eski gerekçe: görsel şifreler e-okuyucuda bozulur. Karşılığı:
    # akışkan EPUB + tam genişlik levha + ekranda yakınlaştırma
    # (04_BUILD/kindle.py, mimari gerekçesi orada ölçülerek yazılı).
    # Kapı artık Kindle'ın AÇIK ve ÜRETİLMİŞ olmasını arar.
    kindle = [e for e in meta["editions"] if e.get("id") == "kindle"]
    rep.check(bool(kindle) and kindle[0].get("enabled"),
              "⭑ KINDLE AÇIK ⭑ (kurucu kararı · K9 geçersiz kılındı)")
    epub = os.path.join(pl.ROOT, "08_OUTPUT", "KINDLE",
                        "codex-enigmatica.epub")
    rep.check(os.path.isfile(epub), "Kindle EPUB üretilmiş")

    pending = [k for k, v in meta["founderPending"].items()
               if v in (None, False)]
    if pending:
        rep.warn("⚑ KURUCUYA AİT %d alan boş ve DOLDURULMADI: %s — "
                 "yer tutucu basmak geri alınamaz bir hatadır"
                 % (len(pending), ", ".join(pending)))

    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("\n  ✍ %s" % os.path.relpath(args.json, pl.ROOT))

    return rep.finish("%d alan üretildi · %d kurucu alanı boş"
                      % (len(meta), len(pending)), None)


if __name__ == "__main__":
    sys.exit(main())
