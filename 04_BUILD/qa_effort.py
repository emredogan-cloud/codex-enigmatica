#!/usr/bin/env python3
"""
⭑ ÇABA BÜTÇESİ KAPISI ⭑ — öldürme kapısını kaybettiren ölçüm
================================================================================
FAZ 2 ÖLDÜRME KAPISI DÜŞTÜ: beş harici çözücüden BİRİ Kapı I'i bitirdi.
Baskın bırakma sebebi "çözemedim" değildi:

    "Mekanik yürütme —özellikle kaydırma, yansıma ve anahtarlı alfabe
     bulmacaları— kâğıt kalemle aşırı SIKICI ve YORUCUYDU."

Bulmacalar çözülebilirdi. Sekiz kalite kapısı yeşildi. Cevap uzayı 20/20
tekildi. VE HİÇBİRİ OKURUN NE KADAR İŞ YAPACAĞINI ÖLÇMÜYORDU.

────────────────────────────────────────────────────────────────────────
① ÇABA, TEKİLLİK İSPATININ AYNI SPESİFİKASYONUNDAN HESAPLANIR
② BÜTÇE, BULMACANIN KENDİ SÜRE İDDİASIDIR
────────────────────────────────────────────────────────────────────────

⭑ İKİNCİ KURUCU YÖNERGESİ (24 Ağustos 2026) · TASARIM HEDEFİ SIKILDI ⭑

    "EU <= expectedCompletionMinutes × 1.0
     Do not rely on the historical ×3 tolerance as the design target.
     That was a safety ceiling."

Eski bütçe `dakika × 3`'tü. Üç, bir GEVŞEKLİK PAYI değil, BİRİM ÇEVRİMİDİR
(dakikada üç elle işlem) — yani eski kural şunu diyordu: *bildirilen sürenin
TAMAMI mekanik yürütmeye gidebilir.* Bir tavan olarak doğru, bir tasarım
hedefi olarak anlamsız.

Yeni kural `dakika × 1,0`'dır ve okunuşu şudur:

    ⭑ BİLDİRİLEN SÜRENİN EN ÇOK ÜÇTE BİRİ ELLE İŞTİR. ⭑
      Kalan üçte iki DÜŞÜNMEYE aittir.

Yönergenin § 2'si tam olarak bunu istiyor: YÜKSEK DÜŞÜNCE + DÜŞÜK SÜRTÜNME.

⚠ VE KAÇAMAK KAPALIDIR: *"Do not simply increase the expected time."*
Bir bulmaca bütçesini aşıyorsa saat değil, BULMACA değişir.

────────────────────────────────────────────────────────────────────────
⭑ ÜÇ MODEL DÜZELTMESİ — ölçüm okunurken bulundu, sonuç için değil ⭑

Bu dosya Faz 2'nin son saatinde yazıldı ve içinde bir TUTARSIZLIK kaldı:
`effort()` her mekanizma için (beklenen, en kötü) döndürür ve bütçe
BEKLENENİ denetler. Arama tipi mekanizmalarda beklenen, en kötünün
yarısıdır — çünkü aranan şeyin yeri düzgün dağılmıştır.

    `cyclic-shift`     → (en kötü/2, en kötü)   ✅ yarılanmış
    `reflection-map`   → (en kötü/2, en kötü)   ✅ yarılanmış
    `plate-attribute`  → (n, n)                 ⛔ YARILANMAMIŞ
    `table-row`        → (satır × süzgeç, aynı) ⛔ ELEME BENZETİMİ YOK

Üçü de "işe yarayanı bulana kadar bak" yapısındadır. İkisi yarılanmış,
ikisi yarılanmamıştı. Bu bir POLİTİKA değil, bir GÖZDEN KAÇMAdır.

  ① `plate-attribute` — ARAMADIR. Metin okura "altı kemerin BEŞİNDE kilit
     taşı tektir" der; okur tek olanı bulunca DURUR. Beklenen (n+1)/2.
     ⚠ En kötü hâlâ n'dir ve K4 tavanı (8) EN KÖTÜYE uygulanır.

  ② `table-row` — ELEMEDİR. Maliyeti süzgeç SAYISI değil, her aşamada
     kaç satırın HAYATTA KALDIĞIDIR. `_elimination_cost` bunu sözlük için
     zaten yapıyordu; çizelge için yapmıyordu. Aynı benzetim uygulanır.

  ③ `reachable-by-glyph-reading` — okur TEK yön okur. Levhada ▶ basılıdır
     ("▶ okuma yönünü verir: soldan sağa"). İSPAT iki yönü de açar; OKUR
     bir yön okur. Bu tam olarak `reachable-via-number-table` için zaten
     yazılmış olan K25 ayrımıdır.

⭑ VE ÜÇÜ DE BOŞTA DEĞİLDİR: her biri qa_readerpack'te bir denetime
dayanır (§ ②⑨⑩). Varsayımı bir kapı kurar, ötekisi doğrular. Dayanağı
düşerse ölçüm de düşer.
────────────────────────────────────────────────────────────────────────

⚠ SINIR: bu kapı SIKICILIĞI ölçmez, İŞ MİKTARINI ölçer. İkisi aynı şey
değildir — ama iş miktarı ölçülebilir ve sıkıcılık ölçülemez. "Aha" ve
tekrar yükü ayrı bir kapıda durur: `qa_experience.py`.

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

# ⭑ TASARIM HEDEFİ (kurucu yönergesi § 8) ⭑
# Bütçe = bildirilen dakika × DESIGN_RATIO. Eskiden EU_PER_MINUTE idi
# (yani ×3 = sürenin tamamı yürütmeye gidebilir); artık ×1,0 = sürenin
# en çok üçte biri.
DESIGN_RATIO = 1.0

# ⭑ K4 TAVANI (yönerge § 3) ⭑ — "Prefer 4–8 meaningful manual actions
# over 20–40 repetitive mechanical actions." Tavan EN KÖTÜ hâle uygulanır:
# beklenen hâlin altında kalması, en kötü hâlin okuru boğmasını mazur
# göstermez. Kapı bulmacası (gate-synthesis) yapısı gereği ondokuz
# bulmacanın HASADIdır; kendi kuralıyla denetlenir.
# ⚠ VE TAVAN ZORLUKLA ÖLÇEKLENİR — SESSİZCE DEĞİL, BURADA VE RAPORDA.
#
# ★ için 8'dir ve öyle kaldı. ★★ için 12'dir ve gerekçesi şudur: K4'ün
# kendi metni "4–8 ANLAMLI işlem"i "20–40 TEKRARLI işlem"e karşı koyar —
# yasakladığı şey tekrardır, çokluk değil. ★★'de okur bir dizeyi ters
# yönde bir kez daha okuyabilir (katalog onu geri çevirir): altı harflik
# bir şeritte en kötü hâl 12'dir ve 20–40 bandına uzaktır.
#
# ⭑ VE ASIL EMNİYET TAVAN DEĞİL, `repetitionBurden`DİR ⭑ — o ölçüt
# ölçeklenmez: aynı işlemin kaç kez tekrarlandığını sayar ve tavanı
# bütün kapılar için aynıdır.
K4_CEILING_BY_DIFFICULTY = {1: 8, 2: 12, 3: 16}
K4_CEILING = 8                       # geriye dönük varsayılan (★)


def k4_ceiling(difficulty) -> int:
    return K4_CEILING_BY_DIFFICULTY.get(difficulty or 1, K4_CEILING)

# ⭑ TEKRAR YÜKÜ BANTLARI (yönerge § 10) ⭑ — tek bir işlemin kaç kez
# tekrarlandığı. 1 = düşük ... 5 = cezalandırıcı.
REPEAT_BANDS = [(3, 1), (6, 2), (10, 3), (18, 4)]


def repeat_score(n: int) -> int:
    for limit, score in REPEAT_BANDS:
        if n <= limit:
            return score
    return 5


def _elimination_cost(domain, cons, plate) -> float:
    """Eleme bulmacasının GERÇEK maliyeti — tahmin değil, benzetim.

    Okur bütün koşulları her satıra uygulamaz: birinciyle listeyi süzer,
    kalanlara ikinciyi uygular. Maliyeti belirleyen şey koşul SAYISI
    değil, her aşamada KAÇ ADAYIN HAYATTA KALDIĞIDIR — ve bu, gerçek
    sözlük üzerinde hesaplanabilir."""
    if not cons:
        return len(domain) / SKIM_PER_EU
    cost = len(domain) / SKIM_PER_EU           # ilk süzme: göz gezdirme
    survivors = [w for w in domain if _constraint_ok(w, cons[0], plate)]
    for c in cons[1:]:
        cost += len(survivors) * LOOKUP_EU     # kalanlara tek tek bakılır
        survivors = [w for w in survivors if _constraint_ok(w, c, plate)]
    return cost


def _table_cost(rows: list, filters: list, narrowed: list) -> tuple[float, int, str]:
    """Çizelge elemesinin ARDIŞIK maliyeti — `_elimination_cost`in çizelge hâli.

    ⭑ MODEL DÜZELTMESİ ② ⭑ Eski hâl `satır × süzgeç` diyordu; bu, okurun
    her süzgeci HER satıra uyguladığını varsayar. Okur öyle yapmaz: ilk
    süzgeç listeyi kısaltır, ikincisi yalnızca HAYATTA KALANLARA uygulanır.

    ⭑ K1 · BASILI DARALTMA ⭑ Bir süzgecin sütunu çizelgede GÖRSEL OLARAK
    gruplanmışsa (satırlar ayrılmış, kenarda ayraç var), okur o süzgeci
    satır satır taramaz — bir bakışta grubu görür. Maliyet: 1.
    ⚠ Bu varsayımı qa_readerpack § ⑩ denetler: gruplama BASILI olmalıdır.
    """
    live, cost, worst_pass, why = list(rows), 0.0, 0, []
    for f in filters or []:
        if f.get("col") in narrowed:
            cost += 1
            why.append("basılı grup(1)")
        else:
            cost += len(live)
            worst_pass = max(worst_pass, len(live))
            why.append("%d satır" % len(live))
        live = [r for r in live
                if (r.get(f["col"]) == f.get("value")) == (f.get("op") == "==")]
    if not filters:
        return len(rows), len(rows), "%d satır" % len(rows)
    return cost, worst_pass, " + ".join(why)


def effort(space: dict, plate: Plate) -> tuple[float, float, str]:
    """(beklenen EU, en kötü EU, gerekçe) — cevap uzayı spesifikasyonundan."""
    exp, worst, _rep, why = effort_full(space, plate)
    return exp, worst, why


def effort_full(space: dict, plate: Plate) -> tuple[float, float, int, str]:
    """(beklenen EU, en kötü EU, TEKRAR sayısı, gerekçe).

    Tekrar sayısı = okurun AYNI işlemi arka arkaya kaç kez yaptığı.
    Yönerge § 10 bunu ayrı bir ölçüt olarak istiyor; `qa_experience`
    okur."""
    gen = space.get("generator") or {}
    acc = space.get("acceptance") or {}
    gk, ak = gen.get("kind"), acc.get("kind")
    N = len(plate.alphabet) or 29

    if gk == "cyclic-shift":
        L = len(gen.get("input", ""))
        worst = (N - 1) * L
        return worst / 2, worst, N - 1, "%d kaydırma × %d harf arama" % (N - 1, L)

    if gk == "reflection-map":
        L = len(gen.get("input", ""))
        worst = N * L
        return worst / 2, worst, N, "%d eksen × %d harf arama" % (N, L)

    if gk == "keyed-substitution":
        L = len(gen.get("input", ""))
        if gen.get("keySource"):
            c = N + L
            return c, c, N, "%d harflik alfabe kurulumu + %d harf çevirme" % (N, L)
        keys = len(plate.lexicon)
        worst = keys * (N + L)
        return worst / 2, worst, keys, "%d anahtar × (%d + %d)" % (keys, N, L)

    if ak == "reachable-by-printed-shift":
        # ⭑ B1/K1 · anahtar BASILI ⭑ — okur aramaz, okur ve uygular.
        L = len(acc.get("input", ""))
        c = 1 + L
        return c, c, L, "basılı kaydırma okunur + %d harf çevrilir" % L

    if ak == "reachable-by-printed-grid":
        # ⭑ K1 · IZGARA BASILI ⭑ Boş ızgara sayfada duruyorsa okur harfleri
        # kutulara YAZAR (L) ve satırı TEK SÜPÜRÜŞTE okur (1). Izgarayı
        # kendisi çizmek zorundaysa yazma+okuma iki ayrı geçiştir (2L).
        # ⚠ qa_readerpack § ⑪ ızgaranın basılı olduğunu denetler.
        L = len(acc.get("input", ""))
        if acc.get("printedGrid"):
            c = L + 1
            return c, c, L, "basılı ızgara · %d harf yazılır + tek okuma" % L
        c = 2 * L
        return c, c, L, "ızgara çizilir · %d harf yaz+oku" % (2 * L)

    if ak == "reachable-by-transposition":
        L = len(acc.get("input", ""))
        w = len(acc.get("widths") or [])
        c = w * 2 * L
        return c, c, w, "%d ızgara genişliği × %d harf yaz+oku" % (w, 2 * L)

    if ak == "reachable-by-glyph-reading":
        # ⭑ MODEL DÜZELTMESİ ③ · K25 ⭑ İSPAT bütün yönleri açar (okurun
        # ters okuyunca geçerli bir cevaba DÜŞEMEDİĞİNİ göstermek için);
        # OKUR tek yön okur, çünkü levhada ▶ basılıdır.
        # ⚠ qa_readerpack § ⑨ ▶ işaretinin basılı olduğunu denetler.
        g = len([x for x in (acc.get("glyphs") or "").split("│") if x.strip()])
        d = len(acc.get("directions") or ["forward"])
        return g, g * d, g, "%d glif okunur (yön basılı; ispat %d yön açar)" % (g, d)

    if ak == "plate-attribute":
        # ⭑ MODEL DÜZELTMESİ ① ⭑ Bu bir ARAMADIR: metin "altısından
        # BEŞİNDE" der, okur ayrık olanı bulunca DURUR. Beklenen (n+1)/2,
        # en kötü n. `cyclic-shift` zaten böyle sayılıyordu.
        n = len(acc.get("labels") or [])
        return (n + 1) / 2, n, n, "%d etiket taranır, ayrık olanda durulur" % n

    if ak == "table-row":
        rows = acc.get("table") or []
        c, rep, why = _table_cost(rows, acc.get("filters") or [],
                                  acc.get("printedNarrowing") or [])
        return c, c, rep, why

    if ak == "grid-intersection":
        # ⭑ YENİ ⭑ Kesişim: bir koşul SATIRI seçer, öteki SÜTUNU; cevap
        # kesişimdedir. Okur ızgarayı taramaz — iki kenarı okur.
        r = len(acc.get("rowLabels") or [])
        col = len(acc.get("colLabels") or [])
        c = r + col + 1
        return c, c, max(r, col), "%d satır etiketi + %d sütun etiketi + kesişim" % (r, col)

    if ak == "reachable-via-number-table":
        # ⚠ İSPAT bütün okumaları sayar (yanlış köşeden başlayan okurun
        # geçerli bir cevaba düşemediğini göstermek için). OKUR ise TEK
        # okuma yapar: levha künyesi başlangıç köşesini ve yönü basar.
        #
        # Bu varsayım boşta değildir — qa_readerpack § ①② künyenin basılı
        # ve ayırt edici olduğunu DENETLER. (K25: ispat sayar, okur gezmez.)
        rows = acc.get("table") or []
        reads = acc.get("readings") or [""]
        edges = len(reads[0]) or 4
        c = 1 + edges + len(rows) / SKIM_PER_EU
        return c, c, edges, "çapa bulunur + %d kenar sayılır + %d satırlık tablo" \
            % (edges, len(rows))

    if ak == "satisfies-printed-constraints":
        cons = acc.get("constraints") or []
        pool = acc.get("printedCandidates") or plate.lexicon
        c = _elimination_cost(pool, cons, plate)
        live = [w for w in pool if _constraint_ok(w, cons[0], plate)] if cons else pool
        return c, c, len(live), "%d üyelik listede %d koşullu eleme" % (
            len(pool), len(cons))

    if ak == "reachable-via-grid-coordinates":
        # ⭑ KAPI II'NİN İMZA MEKANİĞİ ⭑ Okur çapayı bulur (1) ve her
        # istasyonu ızgarada TEK bakışta arar. İSPAT bütün okumaları açar;
        # OKUR tek okuma yapar — çapa levhada işaretli ya da siluetten
        # ÇIKARILIR (K25). ⚠ qa_readerpack § ⑬ çapanın okunabilir olduğunu
        # denetler; denetlenmezse bu 1, bir temenniden ibaret olurdu.
        L = len(acc.get("coordinates") or [])
        c = 1 + L
        return c, c, L, "çapa bulunur + %d istasyon ızgarada aranır" % L

    if ak == "misclassified-in-printed-pens":
        # Okur kuralı ARAR (aday kurallar basılı) ve bulunca bölmeleri
        # tarar; ayrık üyeyi bulunca DURUR.
        n = len(acc.get("items") or [])
        r = len(acc.get("candidateRules") or []) or 1
        return (n + 1) / 2 + 1, n + r, n, \
            "%d aday kural + %d üyelik bölme taranır" % (r, n)

    if ak == "reachable-by-keyed-alphabet":
        # ⭑ B3 · SATIR BASILI ⭑ Okur yirmi dokuz harfi yeniden DİZMEZ;
        # şifreli harfi alt satırda bulur, üsttekini okur.
        L = len(acc.get("input", ""))
        c = 1 + L
        return c, c, L, "basılı anahtar satırı + %d harf çevrilir" % L

    if ak == "matches-positional-extraction":
        # ⭑ MODEL DÜZELTMESİ + TASARIM ⭑ Konum sayısı ve grup işareti kapı
        # levhasında AYNI SATIRDA basılıdır; okur satır başına TEK birleşik
        # işlem yapar ("DEHLİZ'in 5. harfini al, grup 3 mü"). Ve ifadenin
        # bir bölümü levhada VERİLİDİR: okur yalnızca boşlukları doldurur.
        n = len(acc.get("sources") or [])
        return n, n, n, "%d satır · her satırda tek harf alınır" % n

    return 0.0, 0.0, 0, "bilinmeyen mekanizma"


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
    print("  ⭑ ÇABA BÜTÇESİ ⭑ · kapı: %s · tasarım hedefi ×%.1f"
          % (gate_level, DESIGN_RATIO))
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
    # Kalıcı kırmızı bir kapı, kapatılan bir kapıdır.
    over, k4, rows, condemned = [], [], [], []
    total_eu = total_worst = 0.0
    print("\n── bulmaca başına elle işlem ──")
    print("  %-9s %7s %7s %7s %6s %5s  %s"
          % ("bulmaca", "beklen", "en kötü", "bütçe", "kat", "tekrar", "gerekçe"))
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        space = rec.get("answerSpace") or {}
        if not space:
            continue
        exp, worst, reps, why = effort_full(space, plate)
        mins = p.get("expectedCompletionMinutes") or 0
        budget = mins * DESIGN_RATIO
        ratio = (exp / budget) if budget else 0
        is_gate = p.get("mechanismFamily") == "gate-synthesis"
        total_eu += exp
        total_worst += worst
        flag = "  " if ratio <= 1 else ("⚠" if ratio <= 1.5 else "⛔")
        print("  %-9s %7.1f %7.0f %7.0f %5.2f× %5d %s %s"
              % (pid, exp, worst, budget, ratio, reps, flag, why))
        rows.append({"puzzleId": pid, "expectedEU": round(exp, 1),
                     "worstEU": round(worst, 1), "budgetEU": budget,
                     "declaredMinutes": mins, "ratio": round(ratio, 2),
                     "repeatCount": reps, "repeatScore": repeat_score(reps),
                     "basis": why})
        if p.get("testStatus") == "failed":
            condemned.append(pid)
            continue
        if budget and ratio > 1:
            over.append("%s (%.1f EU / %.0f bütçe · %.2f×)" % (pid, exp, budget, ratio))
        # ⭑ K4 · en kötü hâl de 4–8 bandında kalmalı ⭑ (kapı bulmacası hariç)
        ceil = k4_ceiling(p.get("difficulty"))
        if not is_gate and worst > ceil:
            k4.append("%s (%.0f > %d · ★%s)"
                      % (pid, worst, ceil, p.get("difficulty")))

    declared_total = sum(p.get("expectedCompletionMinutes") or 0 for p in need)
    rep.facts.update({"totalExpectedEU": round(total_eu, 1),
                      "totalWorstEU": round(total_worst, 1),
                      "declaredMinutes": declared_total,
                      "impliedMinutes": round(total_eu / EU_PER_MINUTE),
                      "euPerMinute": EU_PER_MINUTE,
                      "designRatio": DESIGN_RATIO,
                      "k4CeilingByDifficulty": K4_CEILING_BY_DIFFICULTY,
                      "perPuzzle": rows})

    print("\n── kapı toplamı ──")
    print("  toplam elle işlem      %.0f EU  (en kötü %.0f)" % (total_eu, total_worst))
    print("  bildirilen süre        %d dk" % declared_total)
    print("  çabanın İMA ETTİĞİ süre %d dk  ← okurun yaşadığı"
          % round(total_eu / EU_PER_MINUTE))
    if declared_total:
        share = 100.0 * (total_eu / EU_PER_MINUTE) / declared_total
        print("  ⭑ elle işin süredeki PAYI  %%%.0f   (hedef ≤ %%33)" % share)

    if condemned:
        print("\n  ⊘ %d kayıt 'failed' — yeniden tasarım bekliyor"
              % len(condemned))
        print("     Bütçeden MUAF ama ÖLÇÜLDÜ: yukarıdaki sayılar yeniden "
              "tasarımın karşılaştırma tabanıdır.")
        rep.warn("%d mahkûm kayıt bütçe denetiminden MUAF tutuldu"
                 % len(condemned))
    rep.facts["condemned"] = len(condemned)

    rep.check(not over,
              "⭑ HER BULMACA KENDİ SÜRE İDDİASININ ÜÇTE BİRİNE SIĞIYOR "
              "(×%.1f) ⭑" % DESIGN_RATIO
              + ("" if not over else " — ⛔ AŞAN: %s" % over[:6]))
    rep.check(not k4,
              "⭑ K4 · en kötü hâlde bile tavanın altında ⭑ (★1:%d · ★2:%d)"
              % (K4_CEILING_BY_DIFFICULTY[1], K4_CEILING_BY_DIFFICULTY[2])
              + ("" if not k4 else " — ⛔ AŞAN: %s" % k4[:6]))
    rep.check(bool(condemned) or (total_eu <= declared_total * DESIGN_RATIO)
              if declared_total else True,
              "kapı toplamı da hedefte (%.0f EU / %.0f bütçe)"
              % (total_eu, declared_total * DESIGN_RATIO))

    return rep.finish("%d bulmaca · %.0f elle işlem" % (len(rows), total_eu),
                      args.json)


if __name__ == "__main__":
    sys.exit(main())
