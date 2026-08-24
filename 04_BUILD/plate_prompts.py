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

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
OUT = os.path.join(pl.ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")

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
NON_PUZZLE = [
    # ⚠ SAHNE TARİFLERİ İNGİLİZCEDİR ve bu bir tercih değil bir KURALDIR:
    # prompt bir görsel modele gider, ve Türkçe tarif yazıldığında üç
    # sahne bir CEVABI kelimesi kelimesine içeriyordu (K41 · kısa
    # cevaplar kitabın kendi söz dağarcığıyla çarpışır). Üretim anındaki
    # denetim yakaladı.
    ("pl-front-01", "ön madde",
     "Title plate: a closed codex seen face-on, five blank raised panels "
     "set into its front board.",
     "carries NO data — no countable marks, no stations, no notches"),
    ("pl-front-02", "ön madde",
     "Contract plate: a seal press beside four blank wax discs.",
     "exactly four wax discs, all blank and identical"),
    ("pl-front-03", "ön madde",
     "Tools plate: a drafting table bearing dividers, a straight-edge and "
     "an empty ruled board.",
     "the ruled board is blank — the book typesets every chart"),
    ("pl-gate-1", "kapı açılışı",
     "A low threshold stone with one leaf standing open above it; beyond "
     "it, only darkness.",
     "carries NO data — the leaf is plain"),
    ("pl-gate-2", "kapı açılışı",
     "A gallery of empty specimen cages; the pedestals bear no labels.",
     "carries NO data — pedestals are empty and unlabelled"),
    ("pl-gate-3", "kapı açılışı",
     "A clock without walls: a divided celestial dome above two plain "
     "concentric bands.",
     "the two bands are smooth — no teeth, no marks, no divisions"),
    ("pl-gate-4", "kapı açılışı",
     "One passage seen from within, opening into countless identical "
     "passages.",
     "carries NO data — the passages are empty"),
    ("pl-gate-5", "kapı açılışı",
     "An open codex standing before a polished glass; the glass shows its "
     "reverse.",
     "the leaves are blank in both the book and its reflection"),
    ("pl-meta-02", "son soru",
     "Five shut leaves facing a single blank inscription stone; the stone "
     "is uncarved.",
     "the inscription stone is UNCARVED — the answer is not in this book"),
]


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
        out.append("exactly %d of mark '%s' — countable, evenly spaced, "
                   "all the same size" % (n, ch))
    rows = len(lines)
    if rows:
        out.append("the engraved field is %d bands tall" % rows)
    stations = len(re.findall(r"\d+·\d+", fig))
    if stations:
        out.append("exactly %d stations around the band, each separated by "
                   "a plain gap" % stations)
    return out


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
        print("\n  ⊘ manuscript bu ortamda yok — kütüphane ÜRETİLEMEDİ")
        rep.warn("prompt kütüphanesi BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", None)

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
        })

    # ⭑ BULMACA DIŞI LEVHALAR — kütüphane 104'ün HEPSİNİ taşımalı ⭑
    used = {e["plate"] for e in entries}
    for plate, where, scene, rule in NON_PUZZLE:
        if plate in used:
            continue
        entries.append({"plate": plate, "puzzle": "—", "gate": where,
                        "family": "non-puzzle", "scene": scene,
                        "data": [rule], "figure": ""})

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
    rep.check(not leak,
              "⭑ HİÇBİR PROMPT BİR CEVABI TAŞIMIYOR ⭑ "
              "(prompt kütüphanesi TAKİP EDİLEN bir dosyadır)"
              + ("" if not leak else " — ⛔ %s" % leak[:4]))

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

    _write_html(args.out, entries)
    print("\n  ✍ %s" % os.path.relpath(args.out, pl.ROOT))

    rep.facts.update({"plates": len(entries), "byGate": by_gate,
                      "rawAssetsPresent": bool([
                          f for f in os.listdir(
                              os.path.join(pl.ROOT, "07_ASSETS", "raw"))
                          if not f.startswith(".")])})
    if not rep.facts["rawAssetsPresent"]:
        rep.warn("⚑ 07_ASSETS/raw BOŞ — ~110 gravür ÜRETİLMEDİ. "
                 "Bu kurucu işidir (Faz 5) ve ajan onu yapamaz.")

    return rep.finish("%d prompt üretildi" % len(entries), None)


def _write_html(path: str, entries: list) -> None:
    e = html.escape
    rows = []
    for x in entries:
        rows.append(
            '<section class="p" id="%s">\n'
            '<h3>%s <small>%s · %s · %s</small></h3>\n'
            '<h4>Kompozisyon</h4><p>%s</p>\n'
            '<h4>⭑ VERİ — DEĞİŞTİRİLEMEZ ⭑</h4><ul>%s</ul>\n'
            '<h4>Dizgideki karşılığı</h4><pre>%s</pre>\n'
            '</section>'
            % (e(x["plate"]), e(x["plate"]), e(x["puzzle"]), e(x["gate"]),
               e(x["family"]), e(x["scene"]),
               "".join("<li>%s</li>" % e(d) for d in x["data"]),
               e(x["figure"])))
    doc = """<!doctype html>
<meta charset="utf-8">
<title>Codex Enigmatica · Gravür Levha Prompt Kütüphanesi</title>
<style>
 body{font:15px/1.6 Georgia,serif;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a;background:#fbf8f2}
 h1{font-size:1.7rem;border-bottom:2px solid #1a1a1a;padding-bottom:.4rem}
 h3{margin:2.4rem 0 .3rem;font-size:1.1rem}
 h3 small{font-weight:400;color:#666;font-size:.8rem}
 h4{margin:1rem 0 .2rem;font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;color:#7a5c1e}
 pre{background:#f2ece0;padding:.7rem;overflow-x:auto;font:12px/1.35 ui-monospace,monospace;border-left:3px solid #c9b48a}
 ul{margin:.2rem 0 .2rem 1.1rem}
 .warn{background:#fff4e0;border-left:4px solid #b8860b;padding:.9rem 1.1rem;margin:1.4rem 0}
 .p{border-top:1px solid #e0d6c2;padding-top:.6rem}
 code{background:#f2ece0;padding:.1rem .3rem}
</style>
<h1>Gravür Levha Prompt Kütüphanesi</h1>
<p><strong>Codex Enigmatica</strong> · %d levha · üretilen dosya
(<code>04_BUILD/plate_prompts.py</code>) — elle düzenlemeyin.</p>

<div class="warn">
<strong>⚠ VERİ BÖLÜMÜ PAZARLIĞA KAPALIDIR.</strong> Bu kitapta levha bir
resim değil, bulmacanın <em>verisidir</em>. &ldquo;Veri&rdquo; başlığı
altındaki sayılar ve konumlar bulmacanın kendi şeklinden üretilmiştir;
biri değişirse o bulmaca <strong>çözülemez</strong> olur ve bunu okur
öğrenir, siz değil.
</div>

<h4>Bütün levhalar için ortak üslup</h4>
<p>%s</p>

<h4>Bütün levhalar için mutlak yasak</h4>
<ul>%s</ul>

%s
""" % (len(entries), e(STYLE),
       "".join("<li>%s</li>" % e(f) for f in FORBIDDEN),
       "\n".join(rows))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)


if __name__ == "__main__":
    sys.exit(main())
