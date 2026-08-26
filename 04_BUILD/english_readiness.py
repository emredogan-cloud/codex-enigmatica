#!/usr/bin/env python3
"""
İNGİLİZCE YENİDEN İNŞA DOĞRULAMASI — dönüşüm GERÇEKTEN oldu mu
================================================================================
⚠ BU BETİK BİR KEZ YENİDEN YAZILDI VE SEBEBİ ÖNEMLİDİR.

Eski hâli bir **iş listesiydi**: dönüşüm henüz yapılmamışken neyin
yapılması gerektiğini sayıyordu ve her koşuda *"DÖNÜŞÜM BAŞLAYAMAZ"*
yazdırıyordu. Dönüşüm 26 Ağustos 2026'da kurucu yönergesiyle YAPILDI.
O günden sonra aynı cümleyi yazdırmaya devam eden bir kapı, kitabın
durumu hakkında YALAN SÖYLER — ve bu depoda bir belgenin bayat kalması,
bir kapının kırmızı yanmasından daha tehlikelidir.

Betik artık ÖLÇER: yeniden inşanın gerçekten olup olmadığını.

  ① manuscript üretim dilinde mi
  ② alfabe 26 harf mi ve grup yapısı BASILI mı
  ③ şifreli dizeler yeni alfabeden mi üretilmiş
  ④ katalogların hepsi İngilizce mi
  ⑤ ticari yüzeyde Türkçe kalmış mı  (⚠ ayrıntısı `qa_language.py`)
  ⑥ ve DEĞİŞMEYEN gerçek: harici insan doğrulaması hâlâ 0

⭑ ⑥ BİR KUSUR DEĞİL, BİR SINIRDIR ⭑ Yeniden inşa kurucu geçersiz
kılmasıyla yapıldı; ölçülen öldürme kapısı HÂLÂ HARD-STOP'tur ve bu
betik onu yumuşatmaz. Türkçe pilot doğrulanmadı, İngilizce yeniden inşa
da doğrulanmadı — ikisi de aynı boşluğa bakar.

Çıkış kodları:  0 = doğrulandı   1 = yeniden inşa eksik   2 = kullanım
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked",
                   "english-readiness.json")
BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")
TOOLS = os.path.join(pl.ROOT, "01_SOURCE", "design", "tools-plate.json")

# ⚠ TÜRKÇEYE ÖZGÜ HARFLER. Bir katalog üyesinde bunlardan biri varsa o
# katalog Türkçe pilottan taşınmış demektir — İngiliz alfabesi 26 harftir
# ve bu harflerin hiçbiri onda yoktur.
TR_LETTERS = set("çğışöüÇĞİŞÖÜ")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  İNGİLİZCE YENİDEN İNŞA DOĞRULAMASI")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config() or {}
    lang = cfg.get("language", {})
    fnd = cfg.get("founderInputs", {}) or {}

    book = pl.load_json(BOOK)
    tools = pl.load_json(TOOLS) or {}
    charts = tools.get("charts") or {}

    if not book:
        # Korumalı katman CI'da YOKTUR. Kapı orada boş koşar ve BUNU SÖYLER.
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman)")
        rep.warn("yeniden inşa doğrulaması BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    # ── ① MANUSCRIPT ÜRETİM DİLİNDE Mİ ─────────────────────────────────
    print("\n── ① manuscript ──")
    prod = lang.get("productionLanguage") or "en"
    book_lang = book.get("language")
    print("  üretim dili           %s" % prod)
    print("  manuscript dili       %s" % book_lang)
    print("  sürüm                 %s" % book.get("version"))
    rep.check(book_lang == prod,
              "⭑ MANUSCRIPT ÜRETİM DİLİNDE ⭑ (%s)" % book_lang)
    pages = book.get("puzzles") or []
    off = [p["puzzleId"] for p in pages if p.get("language") not in (None, prod)]
    rep.check(not off, "her okur sayfası üretim dilinde (%d sayfa)" % len(pages)
              + ("" if not off else " — ⛔ %s" % off[:5]))

    # ── ② ALFABE ───────────────────────────────────────────────────────
    print("\n── ② alfabe ──")
    alpha = (charts.get("threshold-alphabet") or {})
    letters = alpha.get("alphabet") or ""
    groups = alpha.get("markGroups") or []
    sizes = [len(g.get("letters") or "") for g in groups]
    print("  harf                  %d" % len(letters))
    print("  işaret grubu          %d · boyutlar %s"
          % (len(groups), "·".join(str(x) for x in sizes) or "—"))
    print("  kaydırma uzayı        %d · yansıma ekseni %d"
          % (max(0, len(letters) - 1), len(letters)))
    rep.check(len(letters) == 26,
              "⭑ ALFABE 26 HARF ⭑ (%d)" % len(letters))
    rep.check(not (set(letters) & TR_LETTERS),
              "alfabede Türkçeye özgü harf yok")
    rep.check(sum(sizes) == len(letters) and len(groups) == 6,
              "⭑ GRUP YAPISI BASILI VE ALFABEYİ TAM KAPLIYOR ⭑ "
              "(%d grup · toplam %d)" % (len(groups), sum(sizes)))
    # ⚠ TEK ÜYELİ BİR GRUP BİR HARFİ BEDAVA VERİR. 26 harfi beşerli bölmek
    # altıncı gruba TEK harf bırakır; kitap dengeli bölmeyi seçti ve bu
    # kapı onu ölçer — bir sonraki düzenleme sessizce geri almasın diye.
    rep.check(all(s >= 4 for s in sizes) if sizes else False,
              "⭑ HİÇBİR İŞARET GRUBU DÖRTTEN KÜÇÜK DEĞİL ⭑ "
              "(tek üyeli bir grup harfini ele verir) — %s"
              % ("·".join(str(x) for x in sizes) or "ölçülemedi"))

    # ── ③ ŞİFRELİ DİZELER YENİ ALFABEDEN Mİ ────────────────────────────
    print("\n── ③ şifreli dizeler ──")
    sols, designs = pl.load_protected()
    strings, foreign = 0, []
    for pid, rec in sols.items():
        acc = ((rec.get("answerSpace") or {}).get("acceptance") or {})
        for key in ("input", "glyphs", "keyedRow"):
            v = acc.get(key)
            if not isinstance(v, str) or not v:
                continue
            strings += 1
            bad = {c for c in v if c.isalpha() and c.upper() not in letters}
            if bad:
                foreign.append("%s/%s → %s" % (pid, key, "".join(sorted(bad))))
    print("  denetlenen dize       %d" % strings)
    rep.check(not foreign,
              "⭑ HER ŞİFRELİ DİZE YENİ ALFABEDEN ⭑"
              + ("" if not foreign else " — ⛔ %s" % foreign[:4]))

    # ── ④ KATALOGLAR ───────────────────────────────────────────────────
    print("\n── ④ basılı kataloglar ──")
    cats, tr_words = 0, []
    for name, ch in charts.items():
        if not pl.chart_is_printed(ch):
            continue
        words = [e.get("word") for e in (ch.get("entries") or [])
                 if isinstance(e, dict) and e.get("word")]
        if not words:
            continue
        cats += 1
        hit = [w for w in words if set(w) & TR_LETTERS]
        if hit:
            tr_words.append("%s → %s" % (name, hit[:3]))
    print("  sözcük katalogu       %d" % cats)
    rep.check(not tr_words,
              "⭑ HİÇBİR KATALOG PİLOTTAN TAŞINMADI ⭑"
              + ("" if not tr_words else " — ⛔ %s" % tr_words))

    # ── ⑤ TAŞINABİLİRLİK SINIFLARI — ARTIK BİR İŞ LİSTESİ DEĞİL ────────
    print("\n── ⑤ taşınabilirlik (yeniden inşa edildi) ──")
    buckets: dict[str, int] = {}
    for p in pages:
        d = designs.get(p["puzzleId"]) or {}
        k = d.get("languagePortability") or "unclassified"
        buckets[k] = buckets.get(k, 0) + 1
    for k in sorted(buckets):
        print("  %-13s %3d bulmaca" % (k, buckets[k]))

    # ── ⑥ DEĞİŞMEYEN GERÇEK ────────────────────────────────────────────
    print("\n── ⑥ harici doğrulama ──")
    sessions = fnd.get("sessionsRecorded", 0)
    print("  harici çözücü oturumu %d" % sessions)
    print("  insan doğrulaması     %s"
          % ("GEÇTİ" if sessions else "YAPILMADI"))
    if not sessions:
        print("\n  ⚠ YENİDEN İNŞA BİR DOĞRULAMA DEĞİLDİR. Türkçe pilot")
        print("    doğrulanmamıştı; İngilizce yeniden inşa da doğrulanmadı.")
        print("    Ölçülen öldürme kapısı HÂLÂ HARD-STOP'tur (A12/A12b).")
        rep.warn("harici insan doğrulaması 0 — yeniden inşa bunu değiştirmez")

    rep.facts.update({
        "manuscriptLanguage": book_lang,
        "productionLanguage": prod,
        "rebuildComplete": book_lang == prod and len(letters) == 26,
        "alphabet": {"letters": len(letters), "groupSizes": sizes,
                     "shiftSpace": max(0, len(letters) - 1),
                     "reflectionAxes": len(letters)},
        "cipherStringsChecked": strings,
        "wordCatalogues": cats,
        "portability": buckets,
        "externalSolverSessions": sessions,
        "humanValidationPassed": bool(sessions),
    })
    return rep.finish("%d harf · %d dize · %d katalog"
                      % (len(letters), strings, cats), args.json)


if __name__ == "__main__":
    sys.exit(main())
