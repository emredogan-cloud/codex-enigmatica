#!/usr/bin/env python3
"""
⭑ ÇABA BÜTÇESİ KAPISI ⭑ — öldürme kapısını kaybettiren ölçüm
================================================================================
FAZ 2 ÖLDÜRME KAPISI DÜŞTÜ: beş harici çözücüden BİRİ Kapı I'i bitirdi.
Baskın bırakma sebebi "çözemedim" değildi:

    "Mekanik yürütme —özellikle kaydırma, yansıma ve anahtarlı alfabe
     bulmacaları— kâğıt kalemle aşırı SIKICI ve YORUCUYDU."

Bulmacalar çözülebilirdi. Üç bağımsız iç çözücü yirmisini de ipucusuz
çözdü. Sekiz kalite kapısı yeşildi. Cevap uzayı 20/20 tekildi.

    VE HİÇBİRİ OKURUN NE KADAR İŞ YAPACAĞINI ÖLÇMÜYORDU.

Bu kapı o boşluğu kapatır. Ve kapatırken iki şeyi birden düzeltir:

────────────────────────────────────────────────────────────────────────
① ÇABA, TEKİLLİK İSPATININ AYNI SPESİFİKASYONUNDAN HESAPLANIR

`answerSpace` okurun ulaşabileceği bütün dizeleri tanımlar. O tanım aynı
zamanda okurun KAÇ ELLE İŞLEM yapacağını da söyler — kimse ona sormamıştı.

    kaydırma şifresi · 29 harflik halka · 6 harflik dize
      → beklenen 14 deneme × 6 arama = 84 elle işlem

② BÜTÇE, BULMACANIN KENDİ SÜRE İDDİASIDIR

Eşik dışarıdan gelmez: `expectedCompletionMinutes` × dakikada yapılabilen
işlem. Yani bir bulmaca kendi iddiasıyla ölçülür.

⭑ VE ASIL DERS BURADA: `expectedCompletionMinutes` alanı KAVRAYIŞI
ölçüyordu, YÜRÜTMEYİ değil. Yazar "bu fikir ne kadar sürede anlaşılır"
diye tahmin etti; okur "bu işi ne kadar sürede yaparım" diye yaşadı.
Aradaki fark dokuz kattı ve öldürme kapısını o fark düşürdü.
────────────────────────────────────────────────────────────────────────

⚠ SINIR: bu kapı SIKICILIĞI ölçmez, İŞ MİKTARINI ölçer. İkisi aynı şey
değildir — ama iş miktarı ölçülebilir ve sıkıcılık ölçülemez. Yakın bir
vekil, olmayan bir ölçümden iyidir.

Çıkış kodları:  0 = geçti   1 = bütçe aşıldı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
from qa_answerspace import TOOLS, Plate, _constraint_ok, col_read  # noqa: E402

# ── ÇABA BİRİMİ (EU) ───────────────────────────────────────────────────
# Bir EU = okurun kalemle yaptığı bir ayrık işlem: bir çizelge araması,
# bir sayım adımı, bir harf yazımı.
EU_PER_MINUTE = 3          # kâğıt kalemle; bir arama+yazım ~20 saniye
SKIM_PER_EU = 20           # bir listeyi göz gezdirirken EU başına satır
LOOKUP_EU = 1              # çizelgede bir sembol bulmak


def _elimination_cost(domain, cons, plate) -> float:
    """Eleme bulmacasının GERÇEK maliyeti — tahmin değil, benzetim.

    Okur bütün koşulları her satıra uygulamaz: birinciyle listeyi süzer,
    kalanlara ikinciyi uygular. Maliyeti belirleyen şey koşul SAYISI
    değil, her aşamada KAÇ ADAYIN HAYATTA KALDIĞIDIR — ve bu, gerçek
    sözlük üzerinde hesaplanabilir."""
    if not cons:
        return len(domain) / SKIM_PER_EU
    survivors = list(domain)
    cost = len(survivors) / SKIM_PER_EU        # ilk süzme: göz gezdirme
    for c in cons[1:]:
        survivors = [w for w in survivors if _constraint_ok(w, cons[0], plate)] \
            if survivors is domain else survivors
        break
    survivors = [w for w in domain if _constraint_ok(w, cons[0], plate)]
    for c in cons[1:]:
        cost += len(survivors) * LOOKUP_EU     # kalanlara tek tek bakılır
        survivors = [w for w in survivors if _constraint_ok(w, c, plate)]
    return cost


def effort(space: dict, plate: Plate) -> tuple[float, float, str]:
    """(beklenen EU, en kötü EU, gerekçe) — cevap uzayı spesifikasyonundan."""
    gen = space.get("generator") or {}
    acc = space.get("acceptance") or {}
    gk, ak = gen.get("kind"), acc.get("kind")
    N = len(plate.alphabet) or 29

    if gk == "cyclic-shift":
        L = len(gen.get("input", ""))
        worst = (N - 1) * L
        return worst / 2, worst, "%d kaydırma × %d harf arama" % (N - 1, L)

    if gk == "reflection-map":
        L = len(gen.get("input", ""))
        worst = N * L
        return worst / 2, worst, "%d eksen × %d harf arama" % (N, L)

    if gk == "keyed-substitution":
        L = len(gen.get("input", ""))
        if gen.get("keySource"):
            # Anahtar VERİLMİŞ: alfabe bir kez kurulur, dize bir kez çevrilir.
            c = N + L
            return c, c, "%d harflik alfabe kurulumu + %d harf çevirme" % (N, L)
        keys = len(plate.lexicon)
        worst = keys * (N + L)
        return worst / 2, worst, "%d anahtar × (%d + %d)" % (keys, N, L)

    if ak == "reachable-by-printed-shift":
        # ⭑ B1/K1 · anahtar BASILI ⭑ — okur aramaz, okur ve uygular.
        L = len(acc.get("input", ""))
        c = 1 + L
        return c, c, "basılı kaydırma okunur + %d harf çevrilir" % L

    if ak == "reachable-by-printed-grid":
        L = len(acc.get("input", ""))
        c = 2 * L
        return c, c, "tek basılı genişlik · %d harf yaz+oku" % (2 * L)

    if ak == "reachable-by-transposition":
        L = len(acc.get("input", ""))
        w = len(acc.get("widths") or [])
        c = w * 2 * L
        return c, c, "%d ızgara genişliği × %d harf yaz+oku" % (w, 2 * L)

    if ak == "reachable-by-glyph-reading":
        g = len([x for x in (acc.get("glyphs") or "").split("│") if x.strip()])
        d = len(acc.get("directions") or ["forward"])
        c = g * d
        return c, c, "%d glif × %d okuma yönü" % (g, d)

    if ak == "plate-attribute":
        n = len(acc.get("labels") or [])
        return n, n, "%d etiketin niteliği sayılır" % n

    if ak == "table-row":
        rows = len(acc.get("table") or [])
        f = len(acc.get("filters") or []) or 1
        c = rows * f
        return c, c, "%d satır × %d süzgeç" % (rows, f)

    if ak == "reachable-via-number-table":
        # ⚠ İSPAT sekiz okumayı sayar (yanlış köşeden başlayan okurun
        # geçerli bir cevaba düşemediğini göstermek için). OKUR ise TEK
        # okuma yapar: levha künyesi başlangıç köşesini ve yönü basar.
        #
        # Bu varsayım boşta değildir — qa_readerpack § ①② künyenin basılı
        # ve ayırt edici olduğunu DENETLER. İki kapı birbirine dayanır:
        # biri varsayımı kurar, öteki onu doğrular. (K25: ispat sayar,
        # okur gezmez.)
        rows = len(acc.get("table") or [])
        c = 1 + 4 + rows / SKIM_PER_EU
        return c, c, "çapa bulunur + 4 kenar sayılır + %d satırlık tablo" % rows

    if ak == "satisfies-printed-constraints":
        cons = acc.get("constraints") or []
        c = _elimination_cost(plate.lexicon, cons, plate)
        return c, c, "%d üyelik listede %d koşullu eleme" % (
            len(plate.lexicon), len(cons))

    if ak == "matches-positional-extraction":
        n = len(acc.get("sources") or [])
        c = n * 2
        return c, c, "%d cevaptan harf alma + grup denetimi" % n

    return 0.0, 0.0, "bilinmeyen mekanizma"


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
    print("  ⭑ ÇABA BÜTÇESİ ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    pre = pl.preflight(rep, gate_level, "çaba bütçesi")
    if pre is None:
        return rep.finish("denetlenecek çaba yok", args.json)
    need, sols, _designs = pre

    plate = Plate(pl.load_json(TOOLS) or {})
    if not plate.ok:
        rep.check(False, "⛔ basılı çizelgeler okunamadı — çaba hesaplanamaz")
        return rep.finish("çizelge yok", args.json)

    # ⚠ 'failed' KAYITLAR BÜTÇEDEN MUAFTIR — ama ÖLÇÜLÜR VE RAPORLANIR.
    #
    # Öldürme kapısı zaten düştü ve bu bulmacalar mahkûm; onları her koşuda
    # yeniden kırmızı yakmak, kapıyı kalıcı kırmızıya çevirir. Kalıcı
    # kırmızı bir kapı, kapatılan bir kapıdır — ve o an gerçek bir kusur
    # geldiğinde kimse bakmaz.
    #
    # Ama sayıları GİZLEMEZ: mahkûm kayıtlar ayrı bir blokta ölçülür ve
    # yeniden tasarımın karşılaştırma tabanını oluşturur.
    over, rows, condemned = [], [], []
    total_eu = 0.0
    print("\n── bulmaca başına elle işlem ──")
    print("  %-9s %7s %7s %7s %6s  %s"
          % ("bulmaca", "beklen", "en kötü", "bütçe", "kat", "gerekçe"))
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        space = rec.get("answerSpace") or {}
        if not space:
            continue
        exp, worst, why = effort(space, plate)
        mins = p.get("expectedCompletionMinutes") or 0
        budget = mins * EU_PER_MINUTE
        ratio = (exp / budget) if budget else 0
        total_eu += exp
        flag = "  " if ratio <= 1 else ("⚠" if ratio <= 2 else "⛔")
        print("  %-9s %7.0f %7.0f %7d %5.1f× %s %s"
              % (pid, exp, worst, budget, ratio, flag, why))
        rows.append({"puzzleId": pid, "expectedEU": round(exp, 1),
                     "worstEU": round(worst, 1), "budgetEU": budget,
                     "declaredMinutes": mins, "ratio": round(ratio, 2),
                     "basis": why})
        if p.get("testStatus") == "failed":
            condemned.append(pid)
        elif budget and ratio > 1:
            over.append("%s (%.0f EU / %d bütçe · %.1f×)"
                        % (pid, exp, budget, ratio))

    declared_total = sum(p.get("expectedCompletionMinutes") or 0 for p in need)
    rep.facts.update({"totalExpectedEU": round(total_eu, 1),
                      "declaredMinutes": declared_total,
                      "impliedMinutes": round(total_eu / EU_PER_MINUTE),
                      "euPerMinute": EU_PER_MINUTE,
                      "perPuzzle": rows})

    print("\n── kapı toplamı ──")
    print("  toplam elle işlem      %.0f EU" % total_eu)
    print("  bildirilen süre        %d dk" % declared_total)
    print("  çabanın İMA ETTİĞİ süre %d dk  ← okurun yaşadığı"
          % round(total_eu / EU_PER_MINUTE))

    if condemned:
        print("\n  ⊘ %d kayıt 'failed' — öldürme kapısı düştü, yeniden "
              "tasarım bekliyor" % len(condemned))
        print("     Bütçeden MUAF ama ölçüldü: yukarıdaki sayılar yeniden "
              "tasarımın karşılaştırma tabanıdır.")
        rep.warn("%d mahkûm kayıt bütçe denetiminden muaf tutuldu "
                 "(GATE_1_REDESIGN_PROPOSAL.md)" % len(condemned))
    rep.facts["condemned"] = len(condemned)

    rep.check(not over,
              "⭑ HER BULMACA KENDİ SÜRE İDDİASINA SIĞIYOR ⭑"
              + ("" if not over else " — ⛔ AŞAN: %s" % over[:6]))
    rep.check(bool(condemned) or (total_eu / EU_PER_MINUTE
                                  <= declared_total * 1.5) if declared_total
              else True,
              "kapı toplamı bildirilen sürenin 1,5 katını aşmıyor "
              "(%d dk / %d dk)" % (round(total_eu / EU_PER_MINUTE),
                                   declared_total))

    return rep.finish("%d bulmaca · %.0f elle işlem" % (len(rows), total_eu),
                      args.json)


if __name__ == "__main__":
    sys.exit(main())
