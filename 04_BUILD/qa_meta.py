#!/usr/bin/env python3
"""
⭑ META-MİSTER KAPISI ⭑ — kitabın VARLIK SEBEBİNİN denetimi
================================================================================
Yol haritası Faz 4 § 8 bu kapıdan üç şey ister:

    → meta-misterin girdisi BEŞ KAPININ ÇIKTISINDAN mı türüyor
    → her kapının katkısı gerçekten ÜRETİLEBİLİYOR mu
    → son sorunun cevabı kitapta YOK mu (olmamalı)

Ve § 12 ikisini **bloklayıcı** ilan eder: bir kapının çıktısı
kullanılmıyorsa, ya da cevap kitapta bulunuyorsa, doğrulama sayfasının
anlamı kalmaz.

────────────────────────────────────────────────────────────────────────
⭑ NEDEN AYRI BİR KAPI ⭑

Meta-misterin her parçası zaten başka bir kapının denetiminde:
bağımlılıklar `qa_dependency`de, tekillik `qa_answerspace`te, sızıntı
`qa_solution_leak`te. Ama HİÇBİRİ meta-mistere META OLARAK bakmıyordu:

  · `qa_dependency` DAG'ın döngüsüz olduğunu ispatlar — ama son sorunun
    BEŞ kapının BEŞİNE birden bağlı olmasını istemez;
  · `qa_answerspace` cevabın tek olduğunu ispatlar — ama cevabın
    kitapta BULUNMAMASINI istemez (öteki yüz cevap için tam tersi doğru:
    hepsi basılı bir katalogda BULUNMAK zorundadır, K22);
  · kanarya cevabı DEPODA arar — kitabın SAYFALARINDA değil.

Bu kapı o üç boşluğun kesiştiği yerde durur.

⚠ VE BİR ŞEYİ ÖZELLİKLE ARAR: **BASİT BİRLEŞTİRME**. Beş kapı sözünü
uç uca eklemek bir çıkarım değildir; okur onu kazara da yapar. Son soru
bir SENTEZ olmak zorundadır — her sözden yalnızca bir harf alınır ve
alınan harfin yeri o kapının KENDİ SAYISIDIR.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
GATE_INDEX = os.path.join(pl.ROOT, "01_SOURCE", "gate_index.json")
TOOLS = os.path.join(pl.ROOT, "01_SOURCE", "design", "tools-plate.json")

META_FAMILY = "meta-synthesis"
META_GATE = "last-question"
GATE_FAMILY = "gate-synthesis"


def _letters(text: str) -> str:
    """KONUM ARİTMETİĞİ için harf dizisi — büyük harf, katlanmamış.

    ⚠ Metin İÇİNDE ARAMA için bunu KULLANMAYIN: `pl.squeeze` küçük
    harfe indirir ve Türkçe ı/İ/I katlaması yapar. İkisini karıştırmak
    sızıntı denetimini sessizce YEŞİL yakar — ve tam olarak öyle oldu:
    ⑦ ve ⑧ ilk yazımda hiçbir sızıntıyı görmüyordu, fikstürler yakaladı.
    Metinde aranan anahtar `_key()`tir."""
    return "".join(c for c in (text or "").upper() if c.isalpha())


def _key(text: str) -> str:
    """Metin içinde aranacak biçim — `pl.squeeze` ile AYNI uzayda."""
    return pl.squeeze(text or "")


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
    print("  ⭑ META-MİSTER KAPISI ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    pre = pl.preflight(rep, gate_level, "meta")
    if pre is None:
        return rep.finish("denetlenecek meta yok", args.json)
    need, sols, designs = pre

    index = {p["puzzleId"]: p for p in pl.load_index()}
    gi = pl.load_json(GATE_INDEX) or {}
    gate_order = [g.get("id") for g in gi.get("gates", [])
                  if not g.get("metaGate")]
    book = pl.load_json(BOOK) or {}
    pages = {p["puzzleId"]: p for p in book.get("puzzles", [])}
    charts = (pl.load_json(TOOLS) or {}).get("charts", {})

    metas = [p for p in need if p.get("mechanismFamily") == META_FAMILY]
    if not metas:
        print("\n  ⊘ meta-mister henüz yazılmadı — kapı BOŞ KOŞTU")
        rep.warn("meta-mister kaydı yok (Faz 4'te yazılır)")
        return rep.finish("meta yok", args.json)

    # ── ① TEK BİR SON SORU ─────────────────────────────────────────────
    print("\n── ① son soru ──")
    rep.check(len(metas) == 1,
              "kitapta TEK bir son soru var (%d)" % len(metas))
    meta = metas[0]
    mid = meta["puzzleId"]
    msol = sols.get(mid) or {}
    mdes = designs.get(mid) or {}
    answer = msol.get("finalAnswer") or ""
    acc = ((msol.get("answerSpace") or {}).get("acceptance") or {})
    phrases = list(acc.get("gatePhrases") or [])
    positions = list(acc.get("positions") or [])
    print("  %s · kapı %s · aile %s · %d harf"
          % (mid, meta.get("gate"), meta.get("mechanismFamily"), len(answer)))
    rep.check(meta.get("gate") == META_GATE,
              "son soru `%s` kapısında" % META_GATE)
    rep.check(acc.get("kind") == META_FAMILY,
              "kabul yordamı meta-sentez (%r)" % acc.get("kind"))

    # ── ② HER KAPI KATKI VERİYOR MU ────────────────────────────────────
    # Yol haritası § 12: bir kapının çıktısı kullanılmıyorsa BLOKLAYICI.
    print("\n── ② beş kapının katkısı ──")
    deps = list(index.get(mid, {}).get("dependencies") or [])
    dep_gates = [index.get(d, {}).get("gate") for d in deps]
    missing = [g for g in gate_order if g not in dep_gates]
    print("  %-10s %-12s %-24s %s"
          % ("bağımlılık", "kapı", "kapı sözü", "konum"))
    for d, ph, k in zip(deps, phrases + [None] * len(deps),
                        positions + [None] * len(deps)):
        print("  %-10s %-12s %-24s %s"
              % (d, index.get(d, {}).get("gate") or "—", ph or "—", k or "—"))
    rep.check(not missing,
              "⭑ BEŞ KAPININ BEŞİ DE SON SORUYA KATKI VERİYOR ⭑"
              + ("" if not missing else " — ⛔ KATKISIZ KAPI: %s" % missing))
    rep.check(len(set(dep_gates)) == len(dep_gates),
              "hiçbir kapı iki kez katkı vermiyor (%s)" % dep_gates)
    not_gate = [d for d in deps
                if index.get(d, {}).get("mechanismFamily") != GATE_FAMILY]
    rep.check(not not_gate,
              "her katkı o kapının KAPI BULMACASINDAN geliyor"
              + ("" if not_gate == [] else " — ⛔ %s" % not_gate))

    # ── ③ BAĞIMLILIKLAR GEÇERLİ · İLERİ REFERANS YOK · DÖNGÜ YOK ───────
    print("\n── ③ bağımlılık bütünlüğü ──")
    unknown = [d for d in deps if d not in index]
    rep.check(not unknown, "her bağımlılık envanterde var"
              + ("" if not unknown else " — ⛔ KAYIP: %s" % unknown))
    rank = {g: i for i, g in enumerate(gate_order)}
    rank[META_GATE] = len(gate_order)
    future = [d for d in deps
              if rank.get(index.get(d, {}).get("gate"), 99)
              >= rank[META_GATE]]
    rep.check(not future,
              "⭑ İLERİ REFERANS YOK ⭑ (son soru yalnızca KENDİNDEN ÖNCEKİ "
              "kapılara bağlanır)"
              + ("" if not future else " — ⛔ %s" % future))
    # Döngü: son soruya bağımlı olan hiçbir kayıt olamaz.
    consumers = [p["puzzleId"] for p in index.values()
                 if mid in (p.get("dependencies") or [])]
    rep.check(not consumers,
              "⭑ DÖNGÜ YOK ⭑ (hiçbir bulmaca son sorunun cevabını "
              "kullanmıyor)"
              + ("" if not consumers else " — ⛔ %s" % consumers))

    # ── ④ KATKI GERÇEKTEN ÜRETİLEBİLİYOR MU ────────────────────────────
    # Bildirilen kapı sözü, O KAPININ kapı bulmacasının GERÇEK cevabı
    # olmalıdır. Aksi hâlde okur "elindeki" sanılan bir şeyi hiç elde
    # etmemiş olur ve son soru çözülemez.
    print("\n── ④ katkılar gerçekten üretiliyor mu ──")
    unproducible = []
    for d, ph in zip(deps, phrases):
        real = (sols.get(d) or {}).get("finalAnswer")
        if pl.squeeze(real or "") != pl.squeeze(ph or ""):
            unproducible.append("%s: bildirilen %r ≠ üretilen %r"
                                % (d, ph, real))
    rep.check(len(phrases) == len(deps),
              "kapı sözü sayısı bağımlılık sayısıyla eşit (%d/%d)"
              % (len(phrases), len(deps)))
    rep.check(not unproducible,
              "⭑ HER KAPI SÖZÜ O KAPININ GERÇEK ÇIKTISI ⭑"
              + ("" if not unproducible else " — ⛔ %s" % unproducible))

    # ── ⑤ CEVAP BASILI MALZEMEDEN TÜRÜYOR MU ───────────────────────────
    print("\n── ⑤ cevap türetimi ──")
    rep.check(len(positions) == len(phrases),
              "her kapı sözünün bir konumu var (%d/%d)"
              % (len(positions), len(phrases)))
    built_tail, built_head = "", ""
    ok_pos = True
    for ph, k in zip(phrases, positions):
        q = _letters(ph)
        if not isinstance(k, int) or not 1 <= k <= len(q):
            ok_pos = False
            continue
        built_tail += q[-k]
        built_head += q[k - 1]
    rep.check(ok_pos, "her konum kendi sözünün İÇİNDE (1 ≤ k ≤ uzunluk)")
    derived = built_tail if built_tail == _letters(answer) else built_head
    rep.check(derived == _letters(answer),
              "⭑ CEVAP BASILI SÖZLERDEN TÜRETİLEBİLİYOR ⭑ (%s)"
              % ("türetildi" if derived == _letters(answer)
                 else "⛔ %r ≠ %r" % (derived, _letters(answer))))
    rep.check(len(_letters(answer)) == len(phrases),
              "her kapı TAM OLARAK BİR harf veriyor (%d harf / %d kapı)"
              % (len(_letters(answer)), len(phrases)))

    # ── ⑥ SON ÇIKARIM BASİT BİRLEŞTİRME DEĞİL ──────────────────────────
    # Beş sözü uç uca eklemek bir çıkarım değildir. Cevap, birleştirilmiş
    # dizenin İÇİNDEN okunabiliyorsa okur onu kazara bulur.
    print("\n── ⑥ basit birleştirme değil ──")
    joined = "".join(_key(p) for p in phrases)
    key = _key(answer)
    prefixes = _key("".join(_letters(p)[0] for p in phrases))
    suffixes = _key("".join(_letters(p)[-1] for p in phrases))
    rep.check(key not in joined,
              "⭑ CEVAP BİRLEŞTİRİLMİŞ SÖZLERİN İÇİNDE OKUNMUYOR ⭑")
    rep.check(key not in joined[::-1],
              "cevap birleştirilmiş sözlerin TERSİNDE de okunmuyor")
    rep.check(key != prefixes,
              "cevap 'her sözün ilk harfi' DEĞİL (%s)" % prefixes.upper())
    rep.check(key != suffixes,
              "cevap 'her sözün son harfi' DEĞİL (%s)" % suffixes.upper())
    rep.check(len(set(positions)) > 1,
              "konumlar sabit bir sayı değil (%s)" % positions)

    # ── ⑦ CEVAP KİTAPTA YOK ────────────────────────────────────────────
    # ⚠ BU, KİTABIN ÖTEKİ YÜZ CEVABININ TAM TERSİDİR. Onlar basılı bir
    # katalogda BULUNMAK zorundadır (K22); bu bulunMAmak zorundadır —
    # yoksa doğrulama sayfasının anlamı kalmaz (§ 12).
    print("\n── ⑦ ⭑ CEVAP KİTAPTA YOK ⭑ ──")
    hits = []
    for pid, page in pages.items():
        if pid == mid:
            continue
        blob = pl.squeeze(" ".join(str(page.get(f) or "") for f in (
            "title", "flavour", "objective", "readerAction", "input",
            "figure", "printedTable"))
            + " " + " ".join(str(x) for x in (page.get("clues") or []))
            + " " + " ".join(str(x) for x in (page.get("constraints") or [])))
        if key in blob:
            hits.append("sayfa %s" % pid)
    for name, ch in charts.items():
        if not ch.get("printed", True):
            continue                      # ispat alanı; kitapta basılı değil
        blob = pl.squeeze(str(ch.get("entries") or ch.get("table")
                              or ch.get("rows") or ""))
        if key in blob:
            hits.append("çizelge %s" % name)
    for pid, rec in sols.items():
        if pid == mid:
            continue
        if pl.squeeze(rec.get("finalAnswer") or "") == key:
            hits.append("cevap %s" % pid)
    for k in ("frame", "frame2", "frame3", "frame4", "frame5"):
        if key in pl.squeeze(" ".join((book.get(k) or {}).get("opening") or [])):
            hits.append("açılış %s" % k)
    for w in book.get("warmUp") or []:
        blob = pl.squeeze(" ".join(str(w.get(f) or "") for f in
                                   ("title", "lead", "note", "figure"))
                          + " " + " ".join(w.get("solved") or []))
        if key in blob:
            hits.append("ısınma %s" % w.get("id"))
    print("  aranan: %d harflik cevap · %d sayfa · %d basılı çizelge · "
          "%d ısınma" % (len(key), len(pages),
                         sum(1 for c in charts.values() if c.get("printed", True)),
                         len(book.get("warmUp") or [])))
    rep.check(not hits,
              "⭑ SON SORUNUN CEVABI KİTABIN HİÇBİR YERİNDE BASILI DEĞİL ⭑"
              + ("" if not hits else " — ⛔ BULUNDU: %s" % hits[:6]))

    # ── ⑧ CEVAP SAYFA BAŞLIKLARINDA GÖRÜNMÜYOR ─────────────────────────
    # Başlık ayrı denetlenir: içerik gözden geçirilirken en son bakılan
    # ve dizgide en BÜYÜK basılan yer başlıktır.
    print("\n── ⑧ başlıklar ──")
    title_hits = [pid for pid, p in pages.items()
                  if key in pl.squeeze(str(p.get("title") or ""))]
    title_hits += ["ısınma %s" % w.get("id") for w in book.get("warmUp") or []
                   if key in pl.squeeze(str(w.get("title") or ""))]
    rep.check(not title_hits,
              "⭑ CEVAP HİÇBİR SAYFA BAŞLIĞINDA GEÇMİYOR ⭑"
              + ("" if not title_hits else " — ⛔ %s" % title_hits))

    # ── ⑨ TEKİLLİK · BASILI ADAY LİSTESİ ───────────────────────────────
    print("\n── ⑨ tekillik ──")
    gen = (msol.get("answerSpace") or {}).get("generator") or {}
    listref = gen.get("listRef")
    cand = charts.get(listref) or {}
    entries = [str(x) for x in (cand.get("entries") or [])]
    accepted = [w for w in entries if _key(w) == key]
    rep.check(bool(entries),
              "aday listesi var (%s · %d üye)" % (listref, len(entries)))
    rep.check(len(accepted) == 1,
              "⭑ ADAY LİSTESİNDE TAM OLARAK BİR ÜYE KABUL EDİLİYOR ⭑ (%d)"
              % len(accepted))
    rep.check(cand.get("printed") is False,
              "⭑ ADAY LİSTESİ KİTAPTA BASILI DEĞİL ⭑ (ispat alanıdır; "
              "basılsaydı cevap dokuz adaya inerdi)")

    # ── ⑩ SIRA MANUSCRIPT'LE TUTUYOR MU ────────────────────────────────
    print("\n── ⑩ sıra ──")
    rep.check(dep_gates == gate_order,
              "⭑ KAPI SIRASI MANUSCRIPT SIRASIYLA AYNI ⭑ (%s)"
              % " → ".join(str(g) for g in dep_gates))
    page = pages.get(mid) or {}
    rep.check(bool(page),
              "son sorunun okur sayfası var")
    declared_len = [c for c in (msol.get("constraints") or [])
                    if "harf" in c.lower()]
    rep.check(bool(declared_len),
              "okura cevabın kaç harf olduğu SÖYLENİYOR")

    rep.facts.update({
        "metaId": mid, "answerLength": len(key),
        "dependencies": deps, "dependencyGates": dep_gates,
        "gateOrder": gate_order, "positions": positions,
        "phraseLengths": [len(_letters(p)) for p in phrases],
        "candidateList": listref, "candidateCount": len(entries),
        "leakHits": hits, "titleHits": title_hits,
    })
    return rep.finish("%d kapı katkısı · %d harf · cevap kitapta YOK"
                      % (len(deps), len(key)), args.json)


if __name__ == "__main__":
    sys.exit(main())
