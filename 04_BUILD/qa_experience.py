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
  ⭑ AYNI mekanizmayı ikinci kez kullanan bulmaca 4 alamaz. Sürpriz bir
    kez olur; ikinci kez yordamdır.
  ⭑ `repetitionBurden` YAZARDAN GELMEZ — `qa_effort`in modelinden ölçülür.

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

AHA_MEDIAN_MIN = 4          # § 9
AHA_LOW_MAX = 2             # § 9 · en çok iki bulmaca 2 ve altı
REPEAT_MEDIAN_MAX = 2       # § 10
REPEAT_HARD_MAX = 3         # § 10 · kapı bulmacası hariç
EVIDENCE_REQUIRED_FROM = 4  # bu puandan itibaren basılı dayanak şart

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

    plate = Plate(pl.load_json(TOOLS) or {})
    book = pl.load_json(BOOK) or {}
    pages = {p["puzzleId"]: p for p in book.get("puzzles", [])}
    charts = (pl.load_json(TOOLS) or {}).get("charts", {})
    warm = book.get("warmUp") or []

    no_exp, bad_kind, no_evidence, dup_signature = [], [], [], []
    rows, aha, reps = [], [], []
    seen_sig: dict[str, str] = {}

    print("\n── bulmaca başına deneyim ──")
    print("  %-9s %4s %7s  %-28s %s"
          % ("bulmaca", "aha", "tekrar", "ödül", "dayanak"))
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

        aha.append(score if isinstance(score, int) else 0)
        reps.append(rscore)
        rows.append({"puzzleId": pid, "ahaScore": score,
                     "revelationKind": rev.get("kind"),
                     "evidence": rev.get("evidence"),
                     "repeatCount": rcount, "repetitionBurden": rscore,
                     "mechanismSignature": sig})
        print("  %-9s %4s %5d(%d)  %-28s %s"
              % (pid, score, rcount, rscore, rev.get("kind") or "—",
                 rev.get("evidence") or "—"))

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
            # ⭑ aynı mekanizma ikinci kez sürpriz olamaz ⭑
            if sig in seen_sig:
                dup_signature.append("%s (aynı mekanizma: %s)"
                                     % (pid, seen_sig[sig]))
            else:
                seen_sig[sig] = pid

        if not is_gate and rscore > REPEAT_HARD_MAX:
            bad_kind.append("%s (tekrar yükü %d)" % (pid, rscore))

    if no_exp:
        rep.check(False, "her bulmacanın deneyim kaydı var — ⛔ EKSİK: %s"
                  % no_exp[:6])
        return rep.finish("deneyim kaydı eksik", args.json)

    med_aha = statistics.median(aha) if aha else 0
    med_rep = statistics.median(reps) if reps else 0
    low = [r["puzzleId"] for r in rows if (r["ahaScore"] or 0) <= 2]

    # ── § 11 · ZORLUK RAMPASI ──────────────────────────────────────────
    order = sorted(need, key=lambda q: q.get("slot") or 0)
    mins = [q.get("expectedCompletionMinutes") or 0 for q in order]
    med_min = statistics.median(mins) if mins else 0
    distinct = len(set(mins))
    easy_start = all(m <= med_min for m in mins[:3])
    grind, run = 0, 0
    for m in mins:
        run = run + 1 if m > med_min else 0
        grind = max(grind, run)
    small_wins = sum(1 for m in mins if m <= med_min) / max(1, len(mins))
    gate_last = (order[-1].get("mechanismFamily") == "gate-synthesis")

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
                      "repetitionMedian": med_rep,
                      "declaredMinutes": mins, "medianMinutes": med_min,
                      "distinctMinutes": distinct, "longestGrind": grind,
                      "smallWinShare": round(small_wins, 2),
                      "warmUpSections": len(warm),
                      "familiesTaught": len(taught & fams),
                      "perPuzzle": rows})

    print("\n── kapı toplamı ──")
    print("  aha ortancası          %.1f   (hedef ≥ %d)" % (med_aha, AHA_MEDIAN_MIN))
    print("  ödülsüz bulmaca (≤2)   %d     (tavan %d)" % (len(low), AHA_LOW_MAX))
    print("  tekrar yükü ortancası  %.1f   (tavan %d)" % (med_rep, REPEAT_MEDIAN_MAX))
    print("  ısınma bölümü          %d örnek · %d/%d aile öğretiliyor"
          % (len(warm), len(taught & fams), len(fams)))
    print("  zorluk rampası         %d ayrı süre · en uzun eziyet %d ·"
          " küçük zafer payı %%%d" % (distinct, grind, round(100 * small_wins)))

    rep.check(not bad_kind,
              "deneyim kayıtları biçimce geçerli"
              + ("" if not bad_kind else " — ⛔ %s" % bad_kind[:5]))
    rep.check(med_aha >= AHA_MEDIAN_MIN,
              "⭑ § 9 · AHA ORTANCASI ≥ %d ⭑ (%.1f)" % (AHA_MEDIAN_MIN, med_aha))
    rep.check(len(low) <= AHA_LOW_MAX,
              "§ 9 · en çok %d bulmaca ödülsüz (%d: %s)"
              % (AHA_LOW_MAX, len(low), low[:4]))
    rep.check(not no_evidence,
              "⭑ 4+ PUAN VEREN HER BULMACA ÖDÜLÜN BASILI YERİNİ GÖSTERİYOR ⭑"
              + ("" if not no_evidence else " — ⛔ DAYANAKSIZ: %s" % no_evidence[:5]))
    rep.check(not dup_signature,
              "⭑ AYNI MEKANİZMA İKİNCİ KEZ 'SÜRPRİZ' SAYILMIYOR ⭑"
              + ("" if not dup_signature else " — ⛔ %s" % dup_signature[:5]))
    rep.check(med_rep <= REPEAT_MEDIAN_MAX,
              "⭑ § 10 · TEKRAR YÜKÜ DÜŞÜK ⭑ (ortanca %.1f ≤ %d)"
              % (med_rep, REPEAT_MEDIAN_MAX))
    rep.check(not untaught,
              "⭑ § 7 · HER MEKANİZMA GEREKMEDEN ÖNCE ÖĞRETİLİYOR ⭑"
              + ("" if not untaught else " — ⛔ ÖRNEĞİ YOK: %s" % untaught))
    rep.check(not spoiled,
              "⭑ ISINMA HİÇBİR GERÇEK CEVABI VERMİYOR ⭑"
              + ("" if not spoiled else " — ⛔ SIZINTI: %d bulmaca" % len(spoiled)))
    rep.check(distinct >= 3, "§ 11 · rampa düz değil (%d ayrı süre)" % distinct)
    rep.check(easy_start, "§ 11 · kolay başlangıç (ilk üç bulmaca ortancanın "
                          "altında)")
    rep.check(grind < 4, "⭑ § 11 · UZUN EZİYET YOK ⭑ (en uzun ardışık ağır "
                         "dizi %d < 4)" % grind)
    rep.check(small_wins >= 0.4,
              "§ 11 · küçük zaferler düzenli (%%%d ≥ %%40)" % round(100 * small_wins))
    rep.check(gate_last, "§ 11 · tatmin edici final (kapı bulmacası sonda)")

    return rep.finish("%d bulmaca · aha ortancası %.1f · tekrar %.1f"
                      % (len(rows), med_aha, med_rep), args.json)


if __name__ == "__main__":
    sys.exit(main())
