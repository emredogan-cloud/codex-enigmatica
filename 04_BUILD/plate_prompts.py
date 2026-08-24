#!/usr/bin/env python3
"""
GRAVÜR LEVHA PROMPT KÜTÜPHANESİ — kurucunun üreteceği ~110 görselin brifi
================================================================================
⚠ BU BETİK BİR GÖRSEL ÜRETMEZ. Levhaları kurucu üretir (Faz 5 kurucu
bağımlılığı) ve `07_ASSETS/raw/` **şu anda boştur**. Ajanın yapabileceği
ve yaptığı şey, o üretimin **doğru şeyi** üretmesini sağlamaktır.

⭑ VE BU KİTAPTA BİR PROMPT SÜS DEĞİLDİR ⭑

Her levha bir bulmacanın VERİSİNİ taşır. Gravürcü "eski görünümlü bir
kemer" çizerse bulmaca çözülemez hâle gelir; çizmesi gereken şey
**tam olarak şu kadar kilit taşı olan, tam olarak şu kenarında işareti
olan** bir kemerdir. Bu yüzden her prompt üç bölümdür:

    KOMPOZİSYON   nesne ve sahne — üslup buradadır
    ⭑ VERİ ⭑      DEĞİŞTİRİLEMEZ sayılar ve konumlar
    YASAK         gravürcünün koyamayacağı şeyler

⚠ VERİ BÖLÜMÜ ELLE YAZILMAZ: her bulmacanın kendi şeklinden ÜRETİLİR.
Bir levhanın verisi değiştiğinde prompt da değişir; ikisinin ayrışması
imkânsızdır.

⚠ VE PROMPT DOSYASI TAKİP EDİLEN BİR DOSYADIR: içine bir CEVAP düşerse
kanarya onu yakalar. Bu yüzden promptlar cevabı değil ŞEKLİ tarif eder.

Çıkış: `07_ASSETS/IMAGE_PROMPT_LIBRARY.html`
Çıkış kodları:  0 = üretildi   1 = kusurlu   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
import prompt_catalog as CAT                                   # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
OUT = os.path.join(pl.ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")

# ── ⭑ KANONİK VARLIK YOLLARI ⭑ ─────────────────────────────────────────
# ⚠ YENİ DİZİN İCAT EDİLMEZ. Depo bu sözleşmeyi Faz 1'de kurdu ve
# `00_CONTEXT/VISUAL_ARCHITECTURE.md § 2` içinde yazıyor:
#
#     07_ASSETS/raw/      kurucunun ürettiği HAM dosya — SALT OKUNUR
#     07_ASSETS/plates/   işlenmiş iç blok levhası (dört sınıfın hepsi)
#
# Ve sınıf DOSYA ADINDA taşınır:
#     pl-*  bulmaca verisi taşır   ·  tl-*  araç (çizelge/alfabe)
#     dc-*  süs, veri taşımaz      ·  an-*  cevap şeması (depoda DEĞİL)
RAW_DIR = "07_ASSETS/raw"
FINAL_DIR = "07_ASSETS/plates"
COVER_FINAL = "03_COVER"
APLUS_FINAL = "03_APLUS"

# ── ORTAK ÜSLUP ────────────────────────────────────────────────────────
# Kitabın nesne kimliği: bir grimoire gibi ciltlenmiş bulmaca kitabı.
STYLE = (
    "17th–18th century copperplate engraving. Fine parallel hatching and "
    "cross-hatching only — no grey wash, no soft shading, no colour. "
    "Pure black line on cream paper. Square-on, diagrammatic composition; "
    "the object fills the frame and is lit flatly so that no detail is "
    "lost to shadow. Thin ruled border. No text, no lettering, no numerals "
    "anywhere in the image."
)

# ⭑ MUTLAK YASAK ⭑ Bunlar üslup tercihi değil, ÇÖZÜLEBİLİRLİK kuralıdır.
FORBIDDEN = [
    "no text, letters, numerals or captions inside the image — every "
    "symbol the reader needs is typeset by the book, not drawn",
    "no extra ornament: a mark the puzzle did not ask for is a mark the "
    "reader will try to read",
    "no soft focus, blur, vignette or texture overlay — POD printing at "
    "300 dpi loses them and the data with them",
    "no perspective foreshortening on counted elements: if the reader "
    "must count them, they must all be the same size",
    "no colour, no grey fills, no gradients",
]

FAMILY_SCENE = {
    "plate-observation": (
        "A row of near-identical architectural or ritual objects on a "
        "plinth, engraved as a specimen plate. Their sameness is the "
        "point; a single one differs."),
    "plate-embedded-cipher": (
        "A single ring, band or strip of worked metal seen face-on, its "
        "surface divided into regular stations."),
    "substitution-cipher": (
        "An alphabet wheel or slide rule of two concentric bands, the "
        "inner one rotated against the outer."),
    "transposition-cipher": (
        "An empty ruled grid of shallow stone cells, like a printer's "
        "type case seen from above."),
    "polyalphabetic-cipher": (
        "Two long parallel rulers or engraved rods laid one above the "
        "other, their divisions aligned."),
    "script-decoding": (
        "A stone or bone edge carved with grouped notches, seen straight "
        "on so each notch is separable."),
    "constraint-logic": (
        "A ledger or ruled table carved into a slate slab; empty cells."),
    "classification": (
        "Two walled enclosures side by side, each holding specimen "
        "pedestals; the pens are equal and plain."),
    "numeral-system": (
        "A tally stone bearing a short row of distinct incised marks of "
        "two or three different sizes."),
    "cyclic-calendar": (
        "Two toothed wheels of different sizes meshed together, seen "
        "face-on, each tooth clearly separated."),
    "path-graph": (
        "A shallow labyrinth cut into a stone floor slab, seen from "
        "directly above, its cells square and equal."),
    "layered-chain": (
        "Two engraved plates laid one over the other, the upper one "
        "hinged aside to show that the second exists."),
    "back-reference": (
        "An index board with a hanging key-tag rail; the tags are blank."),
    "book-structure": (
        "A codex seen edge-on, its gatherings visible, a rule laid "
        "against the block to measure it."),
    "narrative-embedded": (
        "An open manuscript leaf with a ribbon marker laid across one "
        "line; the writing is illegible engraved squiggle, not letters."),
    "gate-synthesis": (
        "A tall door of banded iron with a row of empty inset panels down "
        "its centre, one panel per contributing puzzle."),
    "meta-synthesis": (
        "Five doors seen in a single receding hall, all closed; a sixth "
        "empty frame stands where a door is missing."),
}

# Şekilden veri çıkaran ölçüler — prompt ELLE yazılmasın diye.
MARKS = "●○◆◇▲△▼▽■□▪▫▵·◦┬▓░x'+/\\"

# ⭑ BULMACA DIŞI LEVHALAR ⭑ Kapı açılışları, ön madde ve son soru da
# gravür ister ve ilk kurguda kütüphanede YOKTULAR: kurucu doksan dört
# prompt alıp yüz dört gravür üretmesi gerektiğini kendi keşfedecekti.
# Bunların VERİSİ yoktur — taşıdıkları tek kısıt, veri TAŞIMAMALARIDIR.
# ⚠ SINIF ÖNEKİ DÜZELTİLDİ · Faz 6 hazırlığı.
# Bu dokuz levha Faz 5'te `pl-*` önekiyle yazılmıştı ama HİÇBİRİ bulmaca
# verisi taşımıyor — `VISUAL_ARCHITECTURE § 2` onları DECORATIVE (dc-) ve
# TOOL (tl-) sınıfına koyar ve sınıfı DOSYA ADINDA taşımayı şart koşar.
# Sınıf, `qa_solution_leak`in ikili dosyaları tarayamamasının yerine
# geçen TEK mekanizmadır; yanlış önek o mekanizmayı kör eder.
#
# ⚠ Bulmacaya bağlı doksan dört levhanın kimliği DEĞİŞMEDİ ve
# değiştirilemez: onlar bulmaca kaydından gelir.
NON_PUZZLE = [
    # ⚠ SAHNE TARİFLERİ İNGİLİZCEDİR ve bu bir tercih değil bir KURALDIR:
    # prompt bir görsel modele gider, ve Türkçe tarif yazıldığında üç
    # sahne bir CEVABI kelimesi kelimesine içeriyordu (K41 · kısa
    # cevaplar kitabın kendi söz dağarcığıyla çarpışır). Üretim anındaki
    # denetim yakaladı.
    ("dc-front-01", "ön madde",
     "Title plate: a closed codex seen face-on, five blank raised panels "
     "set into its front board.",
     "carries NO data — no countable marks, no stations, no notches"),
    ("dc-front-02", "ön madde",
     "Contract plate: a seal press beside four blank wax discs.",
     "exactly four wax discs, all blank and identical"),
    ("tl-front-03", "ön madde",
     "Tools plate: a drafting table bearing dividers, a straight-edge and "
     "an empty ruled board.",
     "the ruled board is blank — the book typesets every chart"),
    ("dc-gate-1", "kapı açılışı",
     "A low threshold stone with one leaf standing open above it; beyond "
     "it, only darkness.",
     "carries NO data — the leaf is plain"),
    ("dc-gate-2", "kapı açılışı",
     "A gallery of empty specimen cages; the pedestals bear no labels.",
     "carries NO data — pedestals are empty and unlabelled"),
    ("dc-gate-3", "kapı açılışı",
     "A clock without walls: a divided celestial dome above two plain "
     "concentric bands.",
     "the two bands are smooth — no teeth, no marks, no divisions"),
    ("dc-gate-4", "kapı açılışı",
     "One passage seen from within, opening into countless identical "
     "passages.",
     "carries NO data — the passages are empty"),
    ("dc-gate-5", "kapı açılışı",
     "An open codex standing before a polished glass; the glass shows its "
     "reverse.",
     "the leaves are blank in both the book and its reflection"),
    ("dc-meta-02", "son soru",
     "Five shut leaves facing a single blank inscription stone; the stone "
     "is uncarved.",
     "the inscription stone is UNCARVED — the answer is not in this book"),
]


def engraving_prompt(entry: dict) -> str:
    """⭑ KOPYALANABİLİR TEK BLOK ⭑ — kurucunun modele vereceği metnin TAMAMI.

    ⚠ FAZ 5'TE BÖYLE BİR BLOK YOKTU. Kütüphane sahneyi, veriyi ve yasağı
    AYRI başlıklar hâlinde basıyordu ve kurucu üçünü elle birleştirmek
    zorundaydı. Elle birleştirilen bir prompt, unutulan bir veri maddesi
    demektir — ve bu kitapta unutulan bir veri maddesi ÇÖZÜLEMEZ bir
    bulmacadır.

    Sıra kasıtlıdır: önce NE çizileceği, sonra DEĞİŞTİRİLEMEZ veri, en
    sonda yasak. Görsel modeller son talimatı en güçlü tutar; yasağın
    sonda olması bu yüzdendir."""
    data = "\n".join("  · " + d for d in entry["data"])
    return (
        "%s\n"
        "\n"
        "STYLE — %s\n"
        "\n"
        "⭑ IMMUTABLE DATA — these values are the puzzle itself and may "
        "NOT be changed, rounded, stylised or \"improved\":\n"
        "%s\n"
        "\n"
        "The engraving must make every counted element separately "
        "countable at 300 dpi: equal size, equal spacing, no overlap, no "
        "foreshortening.\n"
        "\n"
        "ABSOLUTE CONSTRAINTS — %s."
        % (entry["scene"].strip(), STYLE, data,
           "; ".join(f.rstrip(".") for f in FORBIDDEN)))


def skeleton(fig: str) -> str:
    """Şeklin İSKELETİ — harfler değil, GEOMETRİ.

    ⭑⭑ BU FONKSİYON BİR SIZINTIYI ONARIR VE İKİ KEZ HAKLIDIR ⭑⭑

    ① Prompt kütüphanesi ilk yazımda dizgideki şekli OLDUĞU GİBİ
       basıyordu. Bazı levhalar çizelgedir ve çizelgenin bir sütunu
       ADAY CEVAPLARDIR: dosya beş gerçek cevabı düz metin olarak
       taşıdı — ve `07_ASSETS/` TAKİP EDİLEN bir dizindir. Kanarya onu
       bir sonraki koşuda yakaladı.

    ② Ve zaten harflere gerek YOKTU: bu kütüphanenin kendi mutlak
       yasağı *"no text, letters, numerals or captions inside the
       image"* diyor. Gravürcünün ihtiyacı geometridir — kaç göz, kaç
       istasyon, hangi kenar. Harfleri kitap dizer.

    Harf ve rakam `·` olur; çerçeve, işaret ve boşluk korunur."""
    out = []
    for ch in fig:
        if ch.isalpha() or ch.isdigit():
            out.append("·")
        else:
            out.append(ch)
    return "".join(out)


def measure(fig: str) -> list:
    """Levhanın DEĞİŞTİRİLEMEZ sayıları — şeklin kendisinden."""
    out = []
    lines = [x for x in fig.splitlines() if x.strip()]
    counts = {}
    for ch in fig:
        if ch in MARKS:
            counts[ch] = counts.get(ch, 0) + 1
    for ch, n in sorted(counts.items(), key=lambda x: -x[1]):
        # ⚠ Tekil sayıda "evenly spaced / all the same size" saçmaydı:
        # bir tane işaretin aralığı ve akranı yoktur. İfade sayıya göre
        # değişir — prompt okunabilir kalmalı, yoksa gravürcü onu atlar.
        if n == 1:
            out.append("exactly ONE mark '%s' — a single, clearly "
                       "separate incision" % ch)
        else:
            out.append("exactly %d of mark '%s' — countable, evenly "
                       "spaced, all the same size, none overlapping"
                       % (n, ch))
    rows = len(lines)
    if rows:
        out.append("the engraved field is %d bands tall" % rows)
    stations = len(re.findall(r"\d+·\d+", fig))
    if stations:
        out.append("exactly %d stations around the band, each separated by "
                   "a plain gap" % stations)
    return out


def audit_html(doc: str, rep) -> None:
    """⭑ TAKİP EDİLEN HTML'İ MANUSCRIPT OLMADAN DENETLER ⭑

    ⚠ Bunlar dosyanın KENDİSİNİ okur, bulmacaları değil. Bu yüzden
    `02_MANUSCRIPT/` olmayan CI ortamında da koşarlar — kütüphane
    takip edilen bir dosyadır ve orada bozulabilir.
    """
    # ── ⭑ ÜRETİLEN HTML'İN KENDİSİ DENETLENİR ⭑ ────────────────────────
    # ⚠ Bir prompt kütüphanesi ÇALIŞMAZSA yoktur: kopyalamayan bir düğme,
    # boşa düşen bir çıpa ya da iki kez kullanılmış bir kimlik, kurucunun
    # yanlış metni kopyalaması demektir. Bunlar gözle görülmez; ölçülür.
    ids = re.findall(r'\bid="([^"]+)"', doc)
    dupe = sorted({i for i in ids if ids.count(i) > 1})
    rep.check(not dupe,
              "⭑ HİÇBİR HTML KİMLİĞİ İKİ KEZ KULLANILMIYOR ⭑ "
              "(kopya kimlik = yanlış metni kopyalayan düğme)"
              + ("" if not dupe else " — ⛔ %s" % dupe[:6]))

    targets = re.findall(r'data-t="([^"]+)"', doc)
    orphan = sorted({t for t in targets if t not in ids})
    rep.check(not orphan,
              "⭑ HER KOPYA DÜĞMESİNİN HEDEFİ VAR ⭑"
              + ("" if not orphan else " — ⛔ HEDEFSİZ: %s" % orphan[:6]))
    boxes = re.findall(r'class="prompt(?: neg)?" id="([^"]+)"', doc)
    silent = sorted({b for b in boxes if b not in targets})
    rep.check(not silent,
              "her prompt kutusunun bir kopya düğmesi var"
              + ("" if not silent else " — ⛔ DÜĞMESİZ: %s" % silent[:6]))

    anchors = re.findall(r'href="#([^"]+)"', doc)
    broken = sorted({a for a in anchors if a not in ids})
    rep.check(not broken,
              "her iç çıpa çözülüyor"
              + ("" if not broken else " — ⛔ KIRIK: %s" % broken))

    for tag in ("article", "details", "table", "nav", "script", "style"):
        o = len(re.findall(r"<%s[ >]" % tag, doc))
        c = len(re.findall(r"</%s>" % tag, doc))
        rep.check(o == c, "<%s> etiketleri dengeli (%d/%d)" % (tag, o, c))

    rep.check("<!doctype html>" in doc.lower()
              and '<html lang="tr">' in doc
              and 'charset="utf-8"' in doc,
              "HTML iskeleti tam (doctype · lang · charset)")
    rep.check("http://" not in doc and "https://" not in doc,
              "⭑ ÇEVRİMDIŞI ÇALIŞIR ⭑ (dış bağ, CDN ya da uzak yazı tipi yok)")

    # ⚠ SIR TARAMASI — kütüphane takip edilen bir dosyadır.
    secret = re.findall(r"(?i)(CANARY_SALT|api[_-]?key|secret|token|"
                        r"password|BEGIN [A-Z ]*PRIVATE KEY)", doc)
    rep.check(not secret,
              "⭑ SIR SIZINTISI YOK ⭑ (anahtar · jeton · parola)"
              + ("" if not secret else " — ⛔ %s" % sorted(set(secret))))

    # ⚠ DOSYA ADI TUTARLILIĞI — kart kimliği ile basılan dosya adı aynı mı
    named = re.findall(r"<code>07_ASSETS/(?:raw|plates)/([^<]+)\.png</code>",
                       doc)
    # ⚠ § 4 ÜRETİM TABLOSU YER TUTUCU BASAR (`<prompt-kimliği>`, `0N`) ve
    # bunlar dosya adı DEĞİLDİR; kalıp onları eler, gerçek adları eler.
    bad_name = sorted({n for n in named
                       if "&lt;" not in n and "0N" not in n
                       and not re.fullmatch(r"[a-z0-9-]+", n)})
    rep.check(not bad_name,
              "her dosya adı küçük harf-tire kalıbında"
              + ("" if not bad_name else " — ⛔ %s" % bad_name[:6]))



def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  GRAVÜR LEVHA PROMPT KÜTÜPHANESİ")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    book = pl.load_json(BOOK) or {}
    if not book:
        # ⭑ MANUSCRIPT YOK — AMA KÜTÜPHANE VAR ⭑
        # ⚠ `02_MANUSCRIPT/` bilerek takip edilmez (korunan katman), bu
        # yüzden CI kütüphaneyi YENİDEN ÜRETEMEZ ve tazelik denetimi
        # orada koşamaz. Ama kütüphanenin KENDİSİ takip edilir: kopya
        # kimlik, hedefsiz kopya düğmesi, kırık çıpa, dış bağ ya da sır
        # orada bozulabilir ve bunları görmek için bulmacalar gerekmez.
        # Hiçbir şey yapmadan yeşil dönmek, CI'nın koruduğunu SANMAKTIR.
        print("\n  ⊘ manuscript bu ortamda yok — kütüphane ÜRETİLEMEDİ")
        rep.warn("tazelik denetimi ATLANDI (manuscript yok) — "
                 "yalnızca takip edilen HTML denetlendi")
        if not os.path.exists(args.out):
            rep.check(False, "⭑ %s DEPODA YOK ⭑ — kurucu 103 gravürü "
                      "neyden üretecek?" % os.path.relpath(args.out, pl.ROOT))
            return rep.finish("kütüphane yok", None)
        audit_html(open(args.out, encoding="utf-8").read(), rep)
        return rep.finish("manuscript yok · HTML denetlendi", None)

    index = {p["puzzleId"]: p for p in pl.load_index()}
    sols, _ = pl.load_protected()
    answers = {pl.squeeze(r.get("finalAnswer") or "")
               for r in sols.values() if r.get("finalAnswer")}

    entries = []
    for p in book.get("puzzles", []):
        plate = p.get("plateId")
        if not plate:
            continue
        fam = index.get(p["puzzleId"], {}).get("mechanismFamily") or "?"
        fig = str(p.get("figure") or p.get("printedTable") or "")
        entries.append({
            "plate": plate, "puzzle": p["puzzleId"], "gate": p.get("gate"),
            "family": fam,
            "scene": FAMILY_SCENE.get(fam, "An engraved diagrammatic plate."),
            "data": measure(fig),
            "figure": skeleton(fig),
            "kind": "engraving",
        })

    # ⭑ BULMACA DIŞI LEVHALAR — kütüphane 104'ün HEPSİNİ taşımalı ⭑
    used = {e["plate"] for e in entries}
    for plate, where, scene, rule in NON_PUZZLE:
        if plate in used:
            continue
        entries.append({"plate": plate, "puzzle": "—", "gate": where,
                        "family": "non-puzzle", "scene": scene,
                        "data": [rule], "figure": "", "kind": "engraving"})

    # ⚠ HİÇBİR PROMPT BİR CEVAP TAŞIYAMAZ.
    leak = []
    for e in entries:
        # ⚠ `figure` DE TARANIR. İlk kurgu yalnızca `scene` ve `data`ya
        # bakıyordu ve sızıntı tam olarak taranmayan alandaydı.
        blob = pl.squeeze(e["scene"] + " " + " ".join(e["data"])
                          + " " + e.get("figure", ""))
        for a in answers:
            if len(a) >= 4 and a in blob:
                leak.append("%s → %s" % (e["plate"], a))
    # ⚠ KAPAK VE A+ PROMPTLARI DA TARANIR. İlk kurgu yalnızca gravür
    # girdilerine bakıyordu; kapak ve A+ metni aynı dosyaya basılır ve
    # ürün sayfası herkese açıktır — oraya düşen bir cevap kitabın
    # içindekinden DAHA GENİŞ yayılır.
    # ⚠ YALNIZCA PROMPT'A GİREN ALANLAR TARANIR.
    # `name`, `purpose` ve `signal` Türkçe KÜNYEDİR ve kopyalanan metne
    # girmez; kitabın yapısal sözcükleri orada geçmek ZORUNDADIR
    # ("Kapılardan geçen yolculuk"). Bu, ısınma örneklerinde `lead` ve
    # `note`un taranmamasıyla aynı gerekçedir (K41): kısa cevaplar
    # kitabın kendi söz dağarcığıyla çarpışır ve künyeyi taramak kapıyı
    # gürültüye boğar. Kopyalanan metin ise ISTISNASIZ taranır.
    PROMPT_FIELDS = ("concept", "composition", "safe")
    for _x in list(CAT.COVERS) + list(CAT.APLUS):
        blob = pl.squeeze(" ".join(str(_x.get(k) or "")
                                   for k in PROMPT_FIELDS))
        for a in answers:
            if len(a) >= 4 and a in blob:
                leak.append("%s → %s" % (_x["id"], a))

    rep.check(not leak,
              "⭑ HİÇBİR PROMPT BİR CEVABI TAŞIMIYOR ⭑ "
              "(prompt kütüphanesi TAKİP EDİLEN bir dosyadır ve kapak/A+ "
              "metni ÜRÜN SAYFASINA gider)"
              + ("" if not leak else " — ⛔ %s" % leak[:4]))

    # ── ⭑ KAPAK VE A+ EKSİKSİZ Mİ ⭑ ────────────────────────────────────
    rep.check(len(CAT.COVERS) == 2,
              "iki kapak konsepti var (%d)" % len(CAT.COVERS))
    rep.check(len(CAT.APLUS) == 6,
              "altı A+ modülü var (%d)" % len(CAT.APLUS))
    bad_mod = [m["id"] for m in CAT.APLUS if m["module"] not in CAT.APLUS_SPEC]
    rep.check(not bad_mod,
              "her A+ modülü GERÇEK bir Amazon modül türüne bağlı"
              + ("" if not bad_mod else " — ⛔ %s" % bad_mod))
    no_claim = [x["id"] for x in (CAT.COVERS + CAT.APLUS)
                if not str(x.get("claim") or "").startswith("BRIEF")]
    rep.check(not no_claim,
              "⭑ HER TİCARİ İDDİA `BRIEF.md`YE DAYANIYOR ⭑ "
              "(ticari mesaj uydurulmaz)"
              + ("" if not no_claim else " — ⛔ DAYANAKSIZ: %s" % no_claim))

    no_data = [e["plate"] for e in entries if not e["data"]]
    rep.check(not no_data,
              "⭑ HER PROMPT ÖLÇÜLMÜŞ VERİ TAŞIYOR ⭑ "
              "(veri bölümü olmayan bir prompt, gravürcüye 'eskiye benzer "
              "bir şey çiz' demektir)"
              + ("" if not no_data else " — ⛔ VERİSİZ: %s" % no_data[:6]))

    missing_scene = sorted({e["family"] for e in entries
                            if e["family"] not in FAMILY_SCENE
                            and e["family"] != "non-puzzle"})

    # ⭑ KÜTÜPHANE, MODELİN İSTEDİĞİ HER LEVHAYI TAŞIMAK ZORUNDA ⭑
    cfg = pl.load_config()
    pbud = (cfg.get("production") or {}).get("plateBudget") or {}
    gi = pl.load_json(os.path.join(pl.ROOT, "01_SOURCE",
                                   "gate_index.json")) or {}
    model = (sum(g.get("plates", {}).get("opening", 0)
                 + g.get("plates", {}).get("puzzle", 0)
                 for g in gi.get("gates", []))
             + pbud.get("frontMatterPlates", 0)
             + pbud.get("lastQuestionPlates", 0))
    rep.check(len(entries) == model,
              "⭑ KÜTÜPHANE MODELİN İSTEDİĞİ LEVHA SAYISINI TAŞIYOR ⭑ "
              "(%d prompt ↔ %d levha) — eksik bir prompt, kurucunun "
              "eksiğini KENDİ keşfetmesi demektir" % (len(entries), model))
    rep.check(not missing_scene,
              "her mekanizma ailesinin bir sahne tarifi var"
              + ("" if not missing_scene else " — ⛔ %s" % missing_scene))

    print("\n── üretilen ──")
    by_gate = {}
    for e in entries:
        by_gate[e["gate"]] = by_gate.get(e["gate"], 0) + 1
    for g, n in by_gate.items():
        print("  %-14s %3d levha" % (g, n))
    print("  %-14s %3d levha" % ("TOPLAM", len(entries)))

    doc = _render_html(entries)
    rel = os.path.relpath(args.out, pl.ROOT)
    if args.check:
        # ⚠ TAZELİK KAPISI — üreteç YAZMAZ, KARŞILAŞTIRIR. Elle düzenlenmiş
        # ya da bayat bir kütüphane burada yakalanır; CI'da tek koruma
        # budur, çünkü CI'nın çalışma ağacı temiz kalmalıdır.
        onceki = (open(args.out, encoding="utf-8").read()
                  if os.path.exists(args.out) else None)
        rep.check(onceki == doc,
                  "⭑ %s ÜRETEÇLE AYNI ⭑ (elle düzenlenmiş ya da bayat "
                  "değil)" % rel
                  + ("" if onceki == doc else
                     " — ⛔ BAYAT: `python3 04_BUILD/plate_prompts.py` koş"))
        print("\n  ⊙ %s (yalnızca denetlendi, yazılmadı)" % rel)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print("\n  ✍ %s" % rel)

    audit_html(doc, rep)

    rep.facts.update({"plates": len(entries), "byGate": by_gate,
                      "rawAssetsPresent": bool([
                          f for f in os.listdir(
                              os.path.join(pl.ROOT, "07_ASSETS", "raw"))
                          if not f.startswith(".")])})
    if not rep.facts["rawAssetsPresent"]:
        rep.warn("⚑ 07_ASSETS/raw BOŞ — ~110 gravür ÜRETİLMEDİ. "
                 "Bu kurucu işidir (Faz 5) ve ajan onu yapamaz.")

    return rep.finish("%d prompt üretildi" % len(entries), None)


_TEMPLATE = """<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Codex Enigmatica · Görsel Prompt Kütüphanesi</title>
<style>
 :root{--ink:#1c1a17;--paper:#faf7f1;--rule:#d9d2c5;--muted:#6b6459;
       --warn:#8a3324;--ok:#2f5d3a;--chip:#efe9dc;--gold:#7a5c1e}
 @media (prefers-color-scheme:dark){
  :root{--ink:#ece7dd;--paper:#171614;--rule:#3a362f;--muted:#a09889;
        --warn:#e0836f;--ok:#8fc79b;--chip:#26241f;--gold:#c9a75a}}
 *{box-sizing:border-box}
 body{margin:0;background:var(--paper);color:var(--ink);
      font:16px/1.6 "Iowan Old Style",Georgia,"Times New Roman",serif;
      padding:2.5rem 1.25rem 6rem}
 .wrap{max-width:64rem;margin:0 auto}
 h1{font-size:1.9rem;line-height:1.2;margin:0 0 .3rem;letter-spacing:-.01em}
 .sub{color:var(--muted);margin:0 0 1.2rem;font-size:.95rem}
 h2{font-size:1.25rem;margin:3rem 0 .6rem;padding-bottom:.35rem;
    border-bottom:2px solid var(--rule);scroll-margin-top:1rem}
 h3{font-size:1.02rem;margin:0 0 .6rem;font-weight:600}
 h3 small{font-weight:400;color:var(--muted);font-size:.78rem;
          margin-left:.4rem}
 h4{margin:1rem 0 .25rem;font-size:.74rem;letter-spacing:.08em;
    text-transform:uppercase;color:var(--gold)}
 p{margin:.55rem 0}
 nav{position:sticky;top:0;z-index:5;background:var(--paper);
     border-bottom:1px solid var(--rule);margin:0 -1.25rem 1.5rem;
     padding:.6rem 1.25rem;display:flex;flex-wrap:wrap;gap:.4rem}
 nav a{font:12px/1 ui-monospace,Menlo,monospace;color:var(--muted);
       text-decoration:none;border:1px solid var(--rule);border-radius:999px;
       padding:.35rem .7rem;white-space:nowrap}
 nav a:hover{color:var(--ink);border-color:var(--gold)}
 .note{background:var(--chip);border-left:3px solid var(--rule);
       padding:.75rem 1rem;margin:1rem 0;font-size:.93rem}
 .stop{border-left-color:var(--warn)}
 .stop strong{color:var(--warn)}
 .card{border:1px solid var(--rule);border-radius:8px;padding:1rem 1.1rem;
       margin:1.4rem 0;background:var(--paper);scroll-margin-top:4rem}
 .scroll{overflow-x:auto}
 table{width:100%%;border-collapse:collapse;margin:.5rem 0;font-size:.85rem}
 th,td{text-align:left;padding:.35rem .5rem;
       border-bottom:1px solid var(--rule);vertical-align:top}
 table.meta th{width:11rem;font-size:.72rem;text-transform:uppercase;
               letter-spacing:.05em;color:var(--muted);font-weight:400}
 .prompt{position:relative;background:var(--chip);border:1px solid var(--rule);
         border-radius:6px;padding:.9rem 1rem;margin:.35rem 0 .3rem;
         font:12.5px/1.55 ui-monospace,"SF Mono",Menlo,Consolas,monospace;
         white-space:pre-wrap;word-break:break-word}
 .prompt.neg{border-style:dashed;color:var(--muted)}
 .copy{border:1px solid var(--rule);background:var(--paper);color:var(--muted);
       border-radius:4px;font:11px/1 ui-monospace,monospace;
       padding:.4rem .7rem;cursor:pointer;margin:0 0 .6rem}
 .copy:hover{color:var(--ink);border-color:var(--gold)}
 .copy.done{color:var(--ok);border-color:var(--ok)}
 details{margin:.6rem 0;border-top:1px dashed var(--rule);padding-top:.4rem}
 summary{cursor:pointer;font:12px/1.4 ui-monospace,monospace;
         color:var(--muted)}
 summary:hover{color:var(--ink)}
 pre{background:var(--chip);padding:.7rem;overflow-x:auto;
     font:11.5px/1.35 ui-monospace,monospace;border-left:3px solid var(--rule);
     margin:.4rem 0}
 ul,ol{margin:.4rem 0 .4rem 1.2rem;padding:0}
 li{margin:.28rem 0}
 ul.data li{font:12.5px/1.5 ui-monospace,monospace}
 code{background:var(--chip);padding:.1rem .3rem;border-radius:3px;
      font-size:.85em}
 .tag{display:inline-block;background:var(--chip);border:1px solid var(--rule);
      border-radius:999px;padding:.1rem .55rem;font-size:.7rem;
      color:var(--muted);margin-right:.25rem}
 .safe{background:var(--chip);border-left:3px solid var(--gold);
       padding:.5rem .75rem;font-size:.9rem}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));
       gap:.6rem;margin:1rem 0}
 .stat{border:1px solid var(--rule);border-radius:6px;padding:.6rem .8rem}
 .stat b{display:block;font-size:1.5rem;line-height:1.1}
 .stat span{font-size:.74rem;color:var(--muted);text-transform:uppercase;
            letter-spacing:.05em}
</style></head><body><div class="wrap">

<h1>Görsel Prompt Kütüphanesi</h1>
<p class="sub"><strong>Codex Enigmatica</strong> · %(total)d prompt ·
üretilen dosya (<code>04_BUILD/plate_prompts.py</code>) — elle
düzenlemeyin, üreteç ezer.</p>

<nav>%(nav)s</nav>

<h2 id="durum">1 · Durum</h2>
<div class="grid">
 <div class="stat"><b>%(n_eng)d</b><span>gravür levhası</span></div>
 <div class="stat"><b>%(n_cov)d</b><span>kapak konsepti</span></div>
 <div class="stat"><b>%(n_ap)d</b><span>A+ modülü</span></div>
 <div class="stat"><b>0</b><span>üretilmiş görsel</span></div>
</div>
<div class="note stop">
<strong>⚠ HİÇBİR GÖRSEL ÜRETİLMEDİ.</strong>
<code>%(raw)s/</code> <strong>boştur</strong>. Görselleri kurucu üretir;
bu dosya yalnızca <em>ne üretileceğini</em> söyler. Fiziksel POD provası
(A9) da <strong>alınmadı</strong>.
</div>

<h2 id="uslup">2 · Ortak görsel üslup</h2>
<div class="note stop">
<strong>⭑ LEVHA BİR RESİM DEĞİL, BULMACANIN VERİSİDİR ⭑</strong><br>
Her kartın &ldquo;VERİ — DEĞİŞTİRİLEMEZ&rdquo; bölümü bulmacanın kendi
şeklinden <em>üretilmiştir</em>. Bir sayı değişirse o bulmaca
<strong>çözülemez</strong> olur — ve bunu okur öğrenir, siz değil.
Gravürcü nesneyi ve geometriyi çizer; <strong>işaretleri kitap dizer.</strong>
</div>
<p>%(style)s</p>

<h2 id="olumsuz">3 · Ortak olumsuz kısıtlar</h2>
<h4>Gravür levhaları için</h4>
<ul>%(forbidden)s</ul>
<h4>Kapak ve A+ için</h4>
<div class="prompt neg" id="neg-common">%(neg_common)s</div>
<button class="copy" data-t="neg-common">olumsuz kopyala</button>

<h2 id="uretim">4 · Üretim ve dosya adlandırma</h2>
<div class="scroll"><table>
<tr><th>Varlık</th><th>HAM konum</th><th>Nihai konum</th><th>Biçim</th></tr>
<tr><td>Gravür levhası</td><td><code>%(raw)s/&lt;prompt-kimliği&gt;.png</code></td>
    <td><code>%(final)s/&lt;prompt-kimliği&gt;.png</code></td><td>PNG · 300 dpi</td></tr>
<tr><td>Kapak</td><td><code>%(raw)s/codex-enigmatica-cover-option-0N.png</code></td>
    <td><code>%(cover_final)s/</code></td><td>PNG · 300 dpi · RGB</td></tr>
<tr><td>A+ modülü</td><td><code>%(raw)s/codex-enigmatica-aplus-0N.png</code></td>
    <td><code>%(aplus_final)s/</code></td><td>PNG · RGB</td></tr>
</table></div>
<div class="note">
<strong>SINIF DOSYA ADINDA TAŞINIR</strong> —
<code>pl-</code> bulmaca verisi · <code>tl-</code> araç ·
<code>dc-</code> süs · <code>an-</code> cevap şeması (depoda
<strong>durmaz</strong>). Sınıf, ikili dosyaları tarayamayan sızıntı
kapısının yerine geçen tek mekanizmadır
(<code>00_CONTEXT/VISUAL_ARCHITECTURE.md § 2</code>).
</div>
<div class="note stop">
<strong>HAM DOSYA TESLİMDEN SONRA DEĞİŞTİRİLMEZ.</strong>
İşleme her zaman <code>%(raw)s/</code> kopyasından yeniden yapılır.
</div>

<h2 id="gravur">5 · Gravür levha promptları · %(n_eng)d</h2>
%(cards)s

<h2 id="kapak">6 · Kapak sanatı promptları · %(n_cov)d</h2>
<div class="note stop">
<strong>YALNIZCA ÖN KAPAK.</strong> Sırt genişliği sayfa sayısından
türer ve iç blok <strong>henüz dondurulmadı</strong> (K12 · Kapı V sayfa
numaralarına bağlıdır). Sarmal kapak, seçilen ön kapak sanatından ve
dizgi araçlarından <em>sonradan</em> kurulur. Bu kartlarda sırt ölçüsü
YOKTUR ve olamaz.
</div>
%(covers)s

<h2 id="aplus">7 · A+ içerik promptları · %(n_ap)d</h2>
<div class="note stop">
<strong>A+ GÖRSELİ BİR MANUSCRIPT SAYFASI DEĞİLDİR.</strong>
Ürün sayfası herkese açıktır: oraya düşen bir cevap, kitabın
içindekinden <strong>daha geniş</strong> yayılır. Hiçbir A+ görseli
cevap, çözülmüş bir levha ya da okunabilir bir işaret gösteremez.
</div>
<div class="note">
<strong>METİN AMAZON'DA, GÖRSELDE DEĞİL.</strong> Görsel yalnızca imgedir;
başlık ve gövde metni Amazon'un kendi modül alanlarına girer. Böylece
kopya değiştiğinde görsel yeniden üretilmez.
</div>
<div class="note">
<strong>TİCARİ MESAJ UYDURULMADI.</strong> Her modülün
&ldquo;ticari dayanak&rdquo; satırı <code>BRIEF.md</code> içindeki
onaylı ifadeye işaret eder.
</div>
%(aplus)s

<h2 id="teslim">8 · Kurucu teslim kontrol listesi</h2>
<ol>
<li>Her prompt kartında <strong>prompt kopyala</strong> ile metni al —
    düğme <em>yalnızca</em> nihai promptu kopyalar, künyeyi değil.</li>
<li>Görseli üret ve <code>%(raw)s/</code> altına
    <strong>kart üzerindeki adla</strong> kaydet.</li>
<li>Gravürde <strong>hiçbir harf, rakam ya da uydurma işaret</strong>
    bulunmadığını gözle doğrula. Bir tane varsa görsel yeniden üretilir.</li>
<li>&ldquo;VERİ&rdquo; bölümündeki her sayıyı görselde <strong>say</strong>.
    Tutmuyorsa görsel yeniden üretilir — veri pazarlığa kapalıdır.</li>
<li>Kapakta ve A+ görselinde <strong>metin-güvenli alanın</strong> düz ve
    sakin kaldığını doğrula.</li>
<li>Bittiğinde <code>./04_BUILD/qa_all.sh</code> koştur.</li>
</ol>
<div class="note stop">
<strong>⚠ SON SORUNUN CEVABI HİÇBİR GÖRSELDE GÖRÜNEMEZ.</strong>
O cevap kitabın içinde de yazmaz; doğrulama sayfasına girilir.
</div>

<script>
document.querySelectorAll(".copy").forEach(function(b){
  b.addEventListener("click", function(){
    var box = document.getElementById(b.dataset.t);
    if(!box){ return; }
    var text = box.innerText.trim();
    var done = function(){
      var old = b.textContent;
      b.textContent = "kopyalandı"; b.classList.add("done");
      setTimeout(function(){ b.textContent = old; b.classList.remove("done"); },
                 1600);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(done, function(){ fallback(); });
    } else { fallback(); }
    function fallback(){
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly","");
      ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch(err){}
      document.body.removeChild(ta);
    }
  });
});
</script>
</div></body></html>
"""


def _card(cid, title, meta_rows, blocks, prompt_text, negative_text,
          collapsed=None):
    """Tek prompt kartı — bütün türler AYNI iskeleti paylaşır.

    ⚠ Aynı iskelet kasıtlıdır: kurucu gravür kartından kapak kartına
    geçtiğinde yeni bir yerleşim öğrenmek zorunda kalmaz."""
    e = html.escape
    out = ['<article class="card" id="%s">' % e(cid)]
    out.append('<h3>%s</h3>' % title)
    if meta_rows:
        out.append('<div class="scroll"><table class="meta">')
        for k, v in meta_rows:
            out.append('<tr><th>%s</th><td>%s</td></tr>' % (e(k), v))
        out.append('</table></div>')
    if collapsed:
        out.append('<details><summary>Ayrıntıyı göster</summary>')
        for label, body in collapsed:
            out.append('<h4>%s</h4>%s' % (e(label), body))
        out.append('</details>')
    for label, body in blocks:
        out.append('<h4>%s</h4>%s' % (e(label), body))
    out.append(
        '<h4>Nihai GPT Image promptu</h4>'
        '<div class="prompt" id="%s-p">%s</div>'
        '<button class="copy" data-t="%s-p">prompt kopyala</button>'
        % (e(cid), e(prompt_text), e(cid)))
    if negative_text:
        out.append(
            '<h4>Olumsuz prompt</h4>'
            '<div class="prompt neg" id="%s-n">%s</div>'
            '<button class="copy" data-t="%s-n">olumsuz kopyala</button>'
            % (e(cid), e(negative_text), e(cid)))
    out.append('</article>')
    return "\n".join(out)


def _render_html(entries: list) -> str:
    e = html.escape
    eng = [x for x in entries if x.get("kind") == "engraving"]

    # ── GRAVÜR KARTLARI ────────────────────────────────────────────────
    cards = []
    for x in eng:
        pid = x["plate"]
        cls = ("bulmaca verisi" if pid.startswith("pl-") else
               "araç" if pid.startswith("tl-") else "süs")
        meta = [
            ("Prompt kimliği", "<code>%s</code>" % e(pid)),
            ("Bulmaca", "<code>%s</code>" % e(x["puzzle"])),
            ("Kapı", e(x["gate"] or "—")),
            ("Mekanizma", "<code>%s</code>" % e(x["family"])),
            ("Görsel sınıfı", '<span class="tag">%s</span>' % e(cls)),
            ("HAM dosya", "<code>%s/%s.png</code>" % (RAW_DIR, e(pid))),
            ("İşlenmiş dosya", "<code>%s/%s.png</code>" % (FINAL_DIR, e(pid))),
        ]
        blocks = [("Kompozisyon", "<p>%s</p>" % e(x["scene"])),
                  ("⭑ VERİ — DEĞİŞTİRİLEMEZ ⭑",
                   '<ul class="data">%s</ul>'
                   % "".join("<li>%s</li>" % e(d) for d in x["data"]))]
        collapsed = ([("Dizgideki karşılığı (iskelet)",
                       "<pre>%s</pre>" % e(x["figure"]))]
                     if x["figure"].strip() else None)
        cards.append(_card(pid, "<code>%s</code> <small>%s · %s</small>"
                           % (e(pid), e(x["puzzle"]), e(x["family"])),
                           meta, blocks, engraving_prompt(x),
                           "; ".join(f.rstrip(".") for f in FORBIDDEN) + ".",
                           collapsed))

    # ── KAPAK KARTLARI ─────────────────────────────────────────────────
    covers = []
    for c in CAT.COVERS:
        meta = [
            ("Prompt kimliği", "<code>%s</code>" % e(c["id"])),
            ("Konsept", e(c["concept"][:120]) + "…"),
            ("Trim", "%s · %s" % (CAT.COVER_TRIM, CAT.COVER_ASPECT)),
            ("Önerilen piksel", CAT.COVER_PIXELS),
            ("HAM dosya",
             "<code>%s/codex-enigmatica-%s.png</code>" % (RAW_DIR, e(c["id"]))),
            ("Nihai hedef", "<code>%s/</code> · sarmal SONRADAN kurulur"
             % COVER_FINAL),
            ("Ticari dayanak", "<code>%s</code>" % e(c["claim"])),
        ]
        blocks = [
            ("Sinyal", "<p>%s</p>" % e(c["signal"])),
            ("Metin-güvenli alan",
             "<p class='safe'>%s</p>" % e(c["safe"]).replace("\n", "<br>")),
        ]
        collapsed = [("Kompozisyon notu", "<p>%s</p>" % e(c["composition"]))]
        covers.append(_card(
            c["id"], "%s <small><code>%s</code></small>"
            % (e(c["name"]), e(c["id"])), meta, blocks,
            CAT.commercial_prompt(
                c, CAT.COVER_NEGATIVE,
                "FORMAT — front cover art only, %s, %s. Leave the "
                "text-safe zones described above visually calm."
                % (CAT.COVER_TRIM, CAT.COVER_ASPECT)),
            "; ".join(n.rstrip(".") for n in CAT.COVER_NEGATIVE) + ".",
            collapsed))

    # ── A+ KARTLARI ────────────────────────────────────────────────────
    aplus = []
    for m in CAT.APLUS:
        kind, dim, note = CAT.APLUS_SPEC[m["module"]]
        meta = [
            ("Modül kimliği", "<code>%s</code>" % e(m["id"])),
            ("Amaç", e(m["purpose"])),
            ("Amazon modül türü", "<span class='tag'>%s</span>" % e(kind)),
            ("Hedef ölçü", "%s <span class='tag'>%s</span>" % (e(dim), e(note))),
            ("HAM dosya",
             "<code>%s/codex-enigmatica-%s.png</code>" % (RAW_DIR, e(m["id"]))),
            ("Nihai hedef", "<code>%s/</code>" % APLUS_FINAL),
            ("Ticari dayanak", "<code>%s</code>" % e(m["claim"])),
            ("Metin işlenişi",
             "GÖRSEL = yalnızca imge · BAŞLIK + GÖVDE = Amazon'un kendi alanı"),
        ]
        blocks = [("Metin-güvenli alan",
                   "<p class='safe'>%s</p>" % e(m["safe"]))]
        collapsed = [("Kompozisyon notu", "<p>%s</p>" % e(m["composition"]))]
        aplus.append(_card(
            m["id"], "%s <small><code>%s</code></small>"
            % (e(m["name"]), e(m["id"])), meta, blocks,
            CAT.commercial_prompt(
                m, CAT.APLUS_NEGATIVE,
                "FORMAT — %s, %s. The image is a background: the "
                "text-safe zone stays flat and low-contrast."
                % (dim, kind)),
            "; ".join(n.rstrip(".") for n in CAT.APLUS_NEGATIVE) + ".",
            collapsed))

    nav = ("".join(
        '<a href="#%s">%s</a>' % (a, b) for a, b in
        (("durum", "Durum"), ("uslup", "Üslup"), ("olumsuz", "Olumsuz"),
         ("uretim", "Üretim"), ("gravur", "Gravür · %d" % len(eng)),
         ("kapak", "Kapak · %d" % len(covers)),
         ("aplus", "A+ · %d" % len(aplus)),
         ("teslim", "Teslim"))))

    doc = _TEMPLATE % {
        "n_eng": len(eng), "n_cov": len(covers), "n_ap": len(aplus),
        "total": len(eng) + len(covers) + len(aplus),
        "nav": nav,
        "style": e(STYLE),
        "forbidden": "".join("<li>%s</li>" % e(f) for f in FORBIDDEN),
        "neg_common": e("; ".join(n.rstrip(".")
                                  for n in CAT.NEGATIVE_COMMON) + "."),
        "raw": RAW_DIR, "final": FINAL_DIR,
        "cover_final": COVER_FINAL, "aplus_final": APLUS_FINAL,
        "cards": "\n".join(cards),
        "covers": "\n".join(covers),
        "aplus": "\n".join(aplus),
    }
    return doc


if __name__ == "__main__":
    sys.exit(main())
