#!/usr/bin/env python3
"""
⭑ DENEYİM KAPISI ⭑ — çabanın ölçtüğü şeyin ÖTEKİ yarısı
================================================================================
`qa_effort` okurun NE KADAR iş yaptığını ölçer ve bunu iyi yapar. Ama
öldürme kapısını düşüren cümle şuydu:

    "Sıkıldım."

Ve iş MİKTARI, sıkıcılığın yalnızca bir yarısıdır. Öteki yarısı ÖDÜLdür:
aynı altı işlem, sonunda bir şey KEŞFEDİLİYORSA zevkli, keşfedilmiyorsa
ev ödevidir. Kurucunun ikinci yönergesi bu yarıyı ölçüye sokuyor:

    § 9  ahaScore         — ortanca ≥ 4 · en çok 2 bulmaca ≤ 2
    § 10 repetitionBurden — düşük
    § 11 çözüm süresi dağılımı — kolay başlangıç, uzun eziyet YOK
    § 7  ısınma — HER aile, gerekmeden ÖNCE çözülmüş bir örnekle öğretilir

────────────────────────────────────────────────────────────────────────
⚠ VE BURADA DÜRÜST OLMAK ZORUNDAYIM ⭑

`ahaScore` YAZARIN KENDİ PUANIDIR. Yönergenin kendi sözleriyle:

    "Do NOT use ahaScore as a substitute for real testing.
     It is a design heuristic."

Bir yazarın kendi bulmacasına "bu çok zekice" demesi bir ölçüm değildir.
Bu kapı o puanı DOĞRULAYAMAZ — ama ŞİŞİRİLMESİNİ zorlaştırabilir ve üç
yapısal koşulla tam olarak bunu yapar:

  ⭑ 4 ve üstü puan veren her bulmaca, ödülün NEREDE OLDUĞUNU göstermek
    zorundadır (`revelation.evidence`) ve gösterdiği şey OKUR PAKETİNDE
    BASILI olmalıdır. "Zekice" diyip yerini gösterememek geçmez.
  ⭑ PUANIN TAVANI YAZARDAN GELMEZ, ÖLÇÜLÜR (§ K36). Aynı mekanizmayı
    ikinci kez kullanan bulmaca 5 ALAMAZ; 4'ü ancak ÖLÇÜLMÜŞ bir
    derinleşmeyle alır. Yazar yalnızca tavanın ALTINA inebilir.
  ⭑ `repetitionBurden` YAZARDAN GELMEZ — `qa_effort`in modelinden ölçülür.

────────────────────────────────────────────────────────────────────────
⭑ K36 · AHA ÖLÇEKLENMEZ, ÇIKARIM ÖLÇEKLENİR ⭑

Faz 4'e kadar tek bir KİTAP GENELİ eşik vardı ve o eşik yanıltıyordu:
beş kapının beşi de 4,0 gösteriyordu, çünkü Kapı III–V'te öğretilmiş bir
mekanizmanın TEKRARINA da 4 yazılmıştı. Kitap geneli ortanca, kapı
düzeyindeki şişmeyi GİZLİYORDU. Eşik artık KAPI BAZINDADIR:

    keşif kapıları (I · II)      ahaScore ortancası ≥ 4
    akıcılık kapıları (III–V)    ahaScore ortancası ≥ 3
                                 + ÇIKARIM ORANI ortancası ≥ 2,0

Çıkarım oranı = bildirilen dakika ÷ ölçülen elle işlem. Elle işlem beş
kapıda da 6–8 bandında SABİTTİR; artan tek şey düşünmedir. Kapı III–V
mutlak yenilikten vazgeçer — karşılığında bu oranı VERMEK ZORUNDADIR.
────────────────────────────────────────────────────────────────────────

Gerçek ölçüm ikinci turun kayıt formundadır ("bu bulmaca sıkıcı mıydı?",
"aha" tepkisi). Bu kapı onun YERİNE geçmez; ona kadar dayanan bir korkuluk.
────────────────────────────────────────────────────────────────────────

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
from qa_answerspace import TOOLS, Plate                        # noqa: E402
from qa_effort import effort_full, repeat_score                # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")

AHA_LOW_MAX = 2             # § 9 · en çok iki bulmaca 2 ve altı
REPEAT_MEDIAN_MAX = 2       # § 10
REPEAT_HARD_MAX = 3         # § 10 · kapı bulmacası hariç
EVIDENCE_REQUIRED_FROM = 4  # bu puandan itibaren basılı dayanak şart

# ⭑ K36 · eşikler BURADA DEĞİL, project_config § experience İÇİNDEDİR ⭑
# Gerekçe killGate'in gerekçesiyle aynıdır: bir eşik betiğin içinde
# durursa sessizce düşürülebilir. Yapılandırmada durursa `validate_spec`
# onu denetler ve düşürülmesi KIRMIZI yanar.
POLICY_DEFAULT = {
    "discoveryGates": ["threshold", "menagerie"],
    "fluencyGates": ["calendar", "labyrinth", "mirror"],
    "discoveryMedianMin": 4,
    "fluencyMedianMin": 3,
    "lowRewardMax": 2,
    "noveltyFloorPerGate": 4,
}
RATIO_DEFAULT = {"fluencyGateMedianMin": 2.0, "mustRiseGateToGate": True}
GATE_ORDER = ("threshold", "menagerie", "calendar", "labyrinth", "mirror")

# § 9'un kendi örneklerinden türetilmiş kapalı sözlük. Serbest metin
# olsaydı her bulmaca kendine bir ödül adı uydururdu.
REVELATION_KINDS = {
    "hidden-rule-becomes-obvious",   # gizli kural birden apaçık olur
    "two-clues-agree",               # iki ipucu beklenmedik biçimde uyuşur
    "second-reading-of-image",       # görüntü ikinci bir okuma verir
    "pattern-collapses",             # örüntü tek zarif cevaba çöker
    "small-observation-unlocks",     # küçük bir gözlem her şeyi açar
}


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
    print("  ⭑ DENEYİM KAPISI ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    pre = pl.preflight(rep, gate_level, "deneyim")
    if pre is None:
        return rep.finish("denetlenecek deneyim yok", args.json)
    need, sols, designs = pre

    cfg = pl.load_config() or {}
    exp_cfg = cfg.get("experience") or {}
    pol = dict(POLICY_DEFAULT, **{k: v for k, v in
                                  (exp_cfg.get("ahaPolicy") or {}).items()
                                  if not k.endswith("$comment")})
    rat = dict(RATIO_DEFAULT, **{k: v for k, v in
                                 (exp_cfg.get("inferenceRatio") or {}).items()
                                 if not k.startswith("$")})
    discovery = set(pol["discoveryGates"])
    fluency = set(pol["fluencyGates"])

    plate = Plate(pl.load_json(TOOLS) or {})
    book = pl.load_json(BOOK) or {}
    pages = {p["puzzleId"]: p for p in book.get("puzzles", [])}
    charts = (pl.load_json(TOOLS) or {}).get("charts", {})
    warm = book.get("warmUp") or []

    no_exp, bad_kind, no_evidence, over_ceiling = [], [], [], []
    rows, aha, reps = [], [], []
    # sig → (ilk kullanan bulmaca, o bulmacanın çıkarım oranı)
    seen_sig: dict[str, tuple[str, float]] = {}
    by_gate_aha: dict[str, list[int]] = {}
    by_gate_ratio: dict[str, list[float]] = {}
    by_gate_novel: dict[str, int] = {}

    print("\n── bulmaca başına deneyim ──")
    print("  %-9s %4s %4s %6s %7s  %-26s %s"
          % ("bulmaca", "aha", "tav", "çıkarım", "tekrar", "ödül", "dayanak"))
    for p in need:
        pid = p["puzzleId"]
        dsg = designs.get(pid) or {}
        exp = dsg.get("experience") or {}
        if not exp:
            no_exp.append(pid)
            continue
        score = exp.get("ahaScore")
        rev = exp.get("revelation") or {}
        sig = exp.get("mechanismSignature") or ""
        space = (sols.get(pid) or {}).get("answerSpace") or {}
        _e, _w, rcount, _why = effort_full(space, plate)
        rscore = repeat_score(rcount)
        is_gate = p.get("mechanismFamily") == "gate-synthesis"
        gid = p.get("gate") or "?"

        # ⭑ ÇIKARIM ORANI ⭑ — bildirilen KAVRAYIŞ süresi ÷ ölçülen elle
        # işlem. İki alanın da sahibi başkadır: dakikayı `validate_spec`,
        # işlemi `qa_effort` denetler. Yazar tek başına ikisini birden
        # şişiremez — biri artarsa öteki kapı ısırır.
        minutes = p.get("expectedCompletionMinutes") or 0
        ratio = minutes / max(_w, 1)

        # ⭑ K36 · TAVAN ÖLÇÜLÜR ⭑ Yazar tavanın ALTINA inebilir, üstüne
        # çıkamaz. İlk kullanım keşiftir; tekrar ancak okurdan DAHA FAZLA
        # düşünme isteyerek 4 olur; istemiyorsa yordamdır.
        first, first_ratio = seen_sig.get(sig, (None, None))
        if first is None:
            ceiling, why_ceiling = 5, "ilk kullanım"
            seen_sig[sig] = (pid, ratio)
            by_gate_novel[gid] = by_gate_novel.get(gid, 0) + 1
        elif ratio > first_ratio + 1e-9:
            ceiling, why_ceiling = 4, "derinleşme (%s · %.2f > %.2f)" % (
                first, ratio, first_ratio)
            by_gate_novel[gid] = by_gate_novel.get(gid, 0) + 1
        else:
            ceiling, why_ceiling = 3, "yordam (%s · %.2f ≤ %.2f)" % (
                first, ratio, first_ratio)

        aha.append(score if isinstance(score, int) else 0)
        reps.append(rscore)
        by_gate_aha.setdefault(gid, []).append(
            score if isinstance(score, int) else 0)
        by_gate_ratio.setdefault(gid, []).append(ratio)
        rows.append({"puzzleId": pid, "gate": gid, "ahaScore": score,
                     "ahaCeiling": ceiling, "ceilingReason": why_ceiling,
                     "firstUseOfSignature": first or pid,
                     "inferenceRatio": round(ratio, 2),
                     "manualOpsWorst": round(_w, 1),
                     "declaredMinutes": minutes,
                     "revelationKind": rev.get("kind"),
                     "evidence": rev.get("evidence"),
                     "repeatCount": rcount, "repetitionBurden": rscore,
                     "mechanismSignature": sig})
        print("  %-9s %4s %4d %6.2f %5d(%d)  %-26s %s"
              % (pid, score, ceiling, ratio, rcount, rscore,
                 rev.get("kind") or "—", rev.get("evidence") or "—"))

        if isinstance(score, int) and score > ceiling:
            over_ceiling.append("%s aha %d > tavan %d · %s"
                                % (pid, score, ceiling, why_ceiling))

        if not isinstance(score, int) or not 1 <= score <= 5:
            bad_kind.append("%s (aha %r)" % (pid, score))
        if rev.get("kind") not in REVELATION_KINDS:
            bad_kind.append("%s (ödül türü %r)" % (pid, rev.get("kind")))

        # ⭑ 4 ve üstü bir puan, ödülün BASILI yerini göstermek zorunda ⭑
        if isinstance(score, int) and score >= EVIDENCE_REQUIRED_FROM:
            ev, page = rev.get("evidence") or "", pages.get(pid) or {}
            ok = (ev in charts
                  or ev == page.get("plateId")
                  or (ev == "printedTable" and bool(page.get("printedTable"))))
            if not ok:
                no_evidence.append("%s → %s" % (pid, ev or "yok"))

        if not is_gate and rscore > REPEAT_HARD_MAX:
            bad_kind.append("%s (tekrar yükü %d)" % (pid, rscore))

    if no_exp:
        rep.check(False, "her bulmacanın deneyim kaydı var — ⛔ EKSİK: %s"
                  % no_exp[:6])
        return rep.finish("deneyim kaydı eksik", args.json)

    med_aha = statistics.median(aha) if aha else 0
    med_rep = statistics.median(reps) if reps else 0
    low = [r["puzzleId"] for r in rows if (r["ahaScore"] or 0) <= 2]

    # ── ⭑ K36 · KAPI BAZINDA EŞİK ⭑ ────────────────────────────────────
    # Kitap geneli ortanca Faz 4'te YANILTTI: beş kapı da 4,0 gösterdi ve
    # Kapı III–V'in şişmesi o ortalamanın içinde kayboldu. Eşik artık her
    # kapıya AYRI vurur ve kapının TÜRÜNE göre değişir.
    gate_aha_med = {g: statistics.median(v) for g, v in by_gate_aha.items() if v}
    gate_ratio_med = {g: statistics.median(v)
                      for g, v in by_gate_ratio.items() if v}
    aha_bad, ratio_bad, novel_bad = [], [], []
    for g, m in sorted(gate_aha_med.items()):
        if g in discovery and m < pol["discoveryMedianMin"]:
            aha_bad.append("%s %.1f < %g (keşif)"
                           % (g, m, pol["discoveryMedianMin"]))
        if g in fluency:
            if m < pol["fluencyMedianMin"]:
                aha_bad.append("%s %.1f < %g (akıcılık)"
                               % (g, m, pol["fluencyMedianMin"]))
            rm = gate_ratio_med.get(g, 0)
            if rm < rat["fluencyGateMedianMin"]:
                ratio_bad.append("%s çıkarım %.2f < %g"
                                 % (g, rm, rat["fluencyGateMedianMin"]))
        if g != "last-question" and len(by_gate_aha.get(g, [])) >= 10:
            n = by_gate_novel.get(g, 0)
            if n < pol["noveltyFloorPerGate"]:
                novel_bad.append("%s %d < %d" % (g, n,
                                                 pol["noveltyFloorPerGate"]))
    ratio_order = [g for g in GATE_ORDER if g in gate_ratio_med]
    ratio_rising = all(gate_ratio_med[a] <= gate_ratio_med[b]
                       for a, b in zip(ratio_order, ratio_order[1:]))

    # ── § 11 · ZORLUK RAMPASI — ⭑ KAPI BAZINDA ⭑ ──────────────────────
    #
    # ⚠ İLK KURGU KİTAP BAZINDAYDI VE YANLIŞTI. Yüz bir bulmacalık bir
    # kitapta Kapı IV'ün BÜTÜN bulmacaları kitap ortancasının üstündedir —
    # çünkü zorluk kapıdan kapıya YÜKSELMEK ZORUNDADIR (§ 18). Kitap
    # bazında ölçen bir 'uzun eziyet' denetimi, tam da istenen tasarımı
    # kırmızı yakardı.
    #
    # Rampa KAPI İÇİNDE anlamlıdır: bir kapının kendi içinde kolay
    # başlaması, küçük zaferler vermesi ve uzun bir ağır dizi
    # barındırmaması. Kapılar ARASI yükseliş ayrıca ölçülür ve ARTMASI
    # beklenir.
    by_gate: dict[str, list] = {}
    for q in need:
        by_gate.setdefault(q.get("gate") or "?", []).append(q)
    flat_g, easy_bad, grind_bad, win_bad = [], [], [], []
    gate_medians = {}
    for gid, qs in by_gate.items():
        qs = sorted(qs, key=lambda x: x.get("slot") or 0)
        mm = [q.get("expectedCompletionMinutes") or 0 for q in qs]
        if len(mm) < 4:
            continue
        med = statistics.median(mm)
        gate_medians[gid] = med
        if len(set(mm)) < 3:
            flat_g.append("%s (%d ayrı süre)" % (gid, len(set(mm))))
        if not all(m <= med for m in mm[:3]):
            easy_bad.append(gid)
        run = best = 0
        for m in mm:
            run = run + 1 if m > med else 0
            best = max(best, run)
        if best >= 4:
            grind_bad.append("%s (%d ardışık)" % (gid, best))
        if sum(1 for m in mm if m <= med) / len(mm) < 0.4:
            win_bad.append(gid)
    mins = [q.get("expectedCompletionMinutes") or 0 for q in need]
    med_min = statistics.median(mins) if mins else 0
    distinct = len(set(mins))
    # ⭑ KAPILAR ARASI YÜKSELİŞ — burada ARTMASI beklenir ⭑
    order = [g for g in ("threshold", "menagerie", "calendar", "labyrinth",
                         "mirror") if g in gate_medians]
    rising = all(gate_medians[a] <= gate_medians[b]
                 for a, b in zip(order, order[1:]))
    last = need[-1] if need else {}
    gate_last = True
    for gid, qs in by_gate.items():
        if gid == "last-question":
            continue
        top = max(qs, key=lambda x: x.get("slot") or 0)
        if top.get("mechanismFamily") != "gate-synthesis":
            gate_last = False
    grind = max((int(x.split("(")[1].split(" ")[0]) for x in grind_bad),
                default=0)
    small_wins = 1.0 if not win_bad else 0.0

    # ── § 7 · ISINMA HER AİLEYİ ÖĞRETİYOR MU ───────────────────────────
    fams = {q.get("mechanismFamily") for q in need}
    taught = {w.get("teaches") for w in warm}
    untaught = sorted(f for f in fams if f and f not in taught)
    warm_answers = " ".join(pl.squeeze(" ".join(w.get("solved") or []))
                            for w in warm)
    real = [(sols.get(q["puzzleId"]) or {}).get("finalAnswer", "") for q in need]
    spoiled = sorted({a for a in real
                      if a and len(pl.squeeze(a)) >= 4
                      and pl.squeeze(a) in warm_answers})

    rep.facts.update({"ahaMedian": med_aha, "ahaLow": len(low),
                      "ahaMedianByGate": {g: round(v, 2)
                                          for g, v in gate_aha_med.items()},
                      "inferenceRatioByGate": {g: round(v, 2)
                                               for g, v in gate_ratio_med.items()},
                      "noveltyByGate": dict(by_gate_novel),
                      "ahaPolicy": pol, "inferenceRatioPolicy": rat,
                      "repetitionMedian": med_rep,
                      "declaredMinutes": mins, "medianMinutes": med_min,
                      "distinctMinutes": distinct, "longestGrind": grind,
                      "smallWinShare": round(small_wins, 2),
                      "warmUpSections": len(warm),
                      "familiesTaught": len(taught & fams),
                      "perPuzzle": rows})

    print("\n── ⭑ K36 · KAPI BAZINDA AHA VE ÇIKARIM ⭑ ──")
    print("  %-14s %6s %6s %7s %8s" % ("kapı", "tür", "aha", "çıkarım",
                                       "yeni/derin"))
    for g in [x for x in GATE_ORDER if x in gate_aha_med] + \
             [x for x in sorted(gate_aha_med) if x not in GATE_ORDER]:
        kind = ("keşif" if g in discovery else
                "akıcı" if g in fluency else "—")
        # ⚠ BU DEĞİŞKEN 'need' ADINI TAŞIYORDU ve fonksiyonun bulmaca
        # listesini (`need`) EZİYORDU. Kusur gizli kaldı çünkü altındaki
        # kod listeyi bir daha kullanmıyordu — ta ki § 7b eklenene
        # kadar; o zaman 'int' üzerinde döngü kurmaya çalıştı.
        need_med = (pol["discoveryMedianMin"] if g in discovery else
                    pol["fluencyMedianMin"] if g in fluency else 0)
        print("  %-14s %6s %6.1f %7.2f %8d   (aha ≥ %g%s)"
              % (g, kind, gate_aha_med[g], gate_ratio_med.get(g, 0),
                 by_gate_novel.get(g, 0), need_med,
                 " · çıkarım ≥ %g" % rat["fluencyGateMedianMin"]
                 if g in fluency else ""))

    print("\n── kapı toplamı ──")
    print("  aha ortancası (kitap)  %.1f   (⚠ artık EŞİK DEĞİL — K36)" % med_aha)
    print("  ödülsüz bulmaca (≤2)   %d     (tavan %d)" % (len(low), AHA_LOW_MAX))
    print("  tekrar yükü ortancası  %.1f   (tavan %d)" % (med_rep, REPEAT_MEDIAN_MAX))
    print("  ısınma bölümü          %d örnek · %d/%d aile öğretiliyor"
          % (len(warm), len(taught & fams), len(fams)))
    print("  zorluk rampası         %d ayrı süre · en uzun eziyet %d ·"
          " küçük zafer payı %%%d" % (distinct, grind, round(100 * small_wins)))

    rep.check(not bad_kind,
              "deneyim kayıtları biçimce geçerli"
              + ("" if not bad_kind else " — ⛔ %s" % bad_kind[:5]))
    rep.check(not aha_bad,
              "⭑ K36 · HER KAPI KENDİ TÜRÜNÜN AHA EŞİĞİNİ TUTUYOR ⭑ "
              "(keşif ≥ %g · akıcılık ≥ %g)"
              % (pol["discoveryMedianMin"], pol["fluencyMedianMin"])
              + ("" if not aha_bad else " — ⛔ %s" % aha_bad))
    rep.check(not over_ceiling,
              "⭑ K36 · HİÇBİR PUAN ÖLÇÜLEN TAVANINI AŞMIYOR ⭑ "
              "(ilk kullanım 5 · ölçülmüş derinleşme 4 · yordam 3)"
              + ("" if not over_ceiling else " — ⛔ %s" % over_ceiling[:5]))
    rep.check(not ratio_bad,
              "⭑ K36 · AKICILIK KAPILARI ÇIKARIM ORANINI VERİYOR ⭑ "
              "(yenilikten vazgeçilen yerde düşünme ARTMAK ZORUNDA)"
              + ("" if not ratio_bad else " — ⛔ %s" % ratio_bad))
    rep.check(ratio_rising or not rat.get("mustRiseGateToGate"),
              "⭑ K36 · ÇIKARIM ORANI KAPIDAN KAPIYA YÜKSELİYOR ⭑ (%s)"
              % " ≤ ".join("%s:%.2f" % (g, gate_ratio_med[g])
                           for g in ratio_order))
    rep.check(not novel_bad,
              "⭑ K36 · HİÇBİR KAPI YİRMİ DÜZ TEKRARDAN İBARET DEĞİL ⭑ "
              "(kapı başına ≥%d ilk kullanım ya da derinleşme)"
              % pol["noveltyFloorPerGate"]
              + ("" if not novel_bad else " — ⛔ %s" % novel_bad))
    rep.check(len(low) <= AHA_LOW_MAX,
              "§ 9 · en çok %d bulmaca ödülsüz (%d: %s)"
              % (AHA_LOW_MAX, len(low), low[:4]))
    rep.check(not no_evidence,
              "⭑ 4+ PUAN VEREN HER BULMACA ÖDÜLÜN BASILI YERİNİ GÖSTERİYOR ⭑"
              + ("" if not no_evidence else " — ⛔ DAYANAKSIZ: %s" % no_evidence[:5]))
    rep.check(med_rep <= REPEAT_MEDIAN_MAX,
              "⭑ § 10 · TEKRAR YÜKÜ DÜŞÜK ⭑ (ortanca %.1f ≤ %d)"
              % (med_rep, REPEAT_MEDIAN_MAX))
    rep.check(not untaught,
              "⭑ § 7 · HER MEKANİZMA GEREKMEDEN ÖNCE ÖĞRETİLİYOR ⭑"
              + ("" if not untaught else " — ⛔ ÖRNEĞİ YOK: %s" % untaught))

    # ── ⭑ § 7b · AİLE DEĞİL, İŞLEM DÜZEYİNDE ⭑ ─────────────────────────
    # ⚠ FAZ 5 · LINE EDITOR BULGUSU. § 7 AİLEYİ denetliyordu ve
    # `layered-chain` ailesi öğretilmiş görünüyordu — ama o ailenin İKİ
    # işlemi var ve ısınma yalnızca birini gösteriyordu. Üç levha
    # "ayna ekseni" basıyor ve o işlem kitabın HİÇBİR YERİNDE
    # öğretilmiyordu; okur onunla ilk kez Kapı IV'ün ikinci
    # bulmacasında karşılaşıyordu.
    #
    # Bir aile öğretilmiş olabilir; içindeki bir İŞLEM öğretilmemiş
    # olabilir. Kural artık levhanın BASTIĞI işlem adına bakar.
    op_names = {"kaydırma", "ızgara", "ayna ekseni"}
    taught_txt = pl.norm(" ".join(
        " ".join([str(w.get(f) or "") for f in ("lead", "note", "title")]
                 + [str(x) for x in (w.get("solved") or [])])
        for w in warm)
        + " " + " ".join(str(x) for x in
                         ((book.get("matter") or {}).get("cipherReference")
                          or [])))
    printed_ops: set = set()
    for p in need:
        fig = pl.norm(str((pages.get(p["puzzleId"]) or {}).get("figure") or ""))
        printed_ops |= {o for o in op_names if pl.norm(o) in fig}
    untaught_ops = sorted(o for o in printed_ops
                          if pl.norm(o) not in taught_txt)
    rep.check(not untaught_ops,
              "⭑ § 7b · LEVHANIN BASTIĞI HER İŞLEM ÖĞRETİLİYOR ⭑ "
              "(bir AİLE öğretilmiş olabilir; içindeki bir İŞLEM "
              "öğretilmemiş olabilir)"
              + ("" if not untaught_ops
                 else " — ⛔ ÖĞRETİLMEYEN: %s" % untaught_ops))
    rep.check(not spoiled,
              "⭑ ISINMA HİÇBİR GERÇEK CEVABI VERMİYOR ⭑"
              + ("" if not spoiled else " — ⛔ SIZINTI: %d bulmaca" % len(spoiled)))
    rep.check(not flat_g, "§ 11 · hiçbir kapının rampası düz değil"
              + ("" if not flat_g else " — DÜZ: %s" % flat_g))
    rep.check(not easy_bad, "§ 11 · her kapı KOLAY başlıyor (ilk üç bulmaca "
              "kendi kapısının ortancasının altında)"
              + ("" if not easy_bad else " — ⛔ %s" % easy_bad))
    rep.check(not grind_bad, "⭑ § 11 · HİÇBİR KAPIDA UZUN EZİYET YOK ⭑ "
              "(kapı içinde ≥4 ardışık ağır bulmaca)"
              + ("" if not grind_bad else " — ⛔ %s" % grind_bad))
    rep.check(not win_bad, "§ 11 · her kapıda küçük zaferler düzenli (≥%40)"
              + ("" if not win_bad else " — ⛔ %s" % win_bad))
    rep.check(gate_last, "§ 11 · her kapının sonunda kapı bulmacası var")
    rep.check(rising, "⭑ § 18 · ZORLUK KAPIDAN KAPIYA YÜKSELİYOR ⭑ (%s)"
              % " ≤ ".join("%s:%g" % (g, gate_medians[g]) for g in order))

    return rep.finish("%d bulmaca · aha %s · çıkarım %s"
                      % (len(rows),
                         "/".join("%.1f" % gate_aha_med[g]
                                  for g in ratio_order) or "—",
                         "/".join("%.2f" % gate_ratio_med[g]
                                  for g in ratio_order) or "—"), args.json)


if __name__ == "__main__":
    sys.exit(main())
