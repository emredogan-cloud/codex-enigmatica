#!/usr/bin/env python3
"""
ALTERNATİF ÇÖZÜM KAPISI — Codex Enigmatica
================================================================================
Bu kitabın EN SİNSİ kusuru burada aranır.

Bir bulmacanın ikinci geçerli cevabı olması, çözülemez olmasından
DAHA KÖTÜDÜR: okur cevabını doğru sanır, doğrulama sayfası reddeder ve
okur kitabı BOZUK sanır. Çözemeyen okur kendini aptal hisseder;
çift cevap bulan okur ALDATILMIŞ hisseder — ve o yorumu silemezsiniz.

Yedi denetim:

  ① alternatif çözüm analizi YAPILMIŞ (public bayrak)
  ② en az ÜÇ alternatif aday üretilmiş (SOLVABILITY_STANDARD § 4)
  ③ her aday için REDDEDİLME GEREKÇESİ yazılmış
  ④ ⭑ 'ZORLAMA' GEREKÇE YOK ⭑ — varsa bulmaca YENİDEN YAZILIR
  ⑤ ⭑ ONAYLANMIŞ ALTERNATİF ÇÖZÜM YOK ⭑
  ⑥ public sayaç gerçek kayıtla TUTARLI
  ⑦ ⭑ ÇÖZÜCÜNÜN ÖNERDİĞİ İKİNCİ CEVAP YOK ⭑ + aynı cevap iki bulmacada yok

④ NEDEN AYRI BİR DENETİM: bir alternatifi "zorlama" diye reddetmek,
onu reddetmemektir. Yazar orada bir kusur GÖRMÜŞ ve geçiştirmiştir.
SOLVABILITY_STANDARD § 4 açık: gerekçe zorlamaysa bulmaca YENİDEN YAZILIR.
Bu kapı o kararı yazarın insafına bırakmaz.

⑦ NEDEN: bir çözücü test sırasında BAŞKA bir cevap önerdiyse, o bulmacanın
tekilliği ampirik olarak çürütülmüştür — yazarın analizi ne derse desin.
Ayrıca iki bulmacanın AYNI cevabı vermesi kapı bulmacasını bozar: kapı
girdilerini ayırt edemez.

⚠ BU KAPI ÇÖZÜM İÇERİĞİ YAZDIRMAZ. Aynı cevap denetimi karşılaştırmayı
karma (hash) üzerinden yapar; rapora yalnızca bulmaca kimliği gider.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

MIN_ALTERNATIVES = 3
FORCED = "forced"


def fingerprint(text: str) -> str:
    """Cevabın karması. Rapora bu bile GİRMEZ — yalnızca bellekte
    karşılaştırma için kullanılır."""
    return hashlib.sha256(pl.squeeze(text).encode("utf-8")).hexdigest()[:16]


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
    print("  ALTERNATİF ÇÖZÜM ANALİZİ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)

    pre = pl.preflight(rep, gate_level, "alternatif çözüm")
    if pre is None:
        return rep.finish("denetlenecek alternatif analizi yok", args.json)
    need, sols, _designs = pre

    not_flagged, too_few, no_reason = [], [], []
    forced_reason, confirmed_alt, counter_mismatch = [], [], []
    solver_alt = []
    answers: dict[str, list[str]] = collections.defaultdict(list)
    checked = 0
    alt_total = 0

    print("\n── alternatif çözüm kayıtları ──")
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid)
        if not rec:
            continue
        checked += 1

        # ① public bayrak
        if p.get("alternativeSolutionAnalysisDone") is not True:
            not_flagged.append(pid)

        alts = rec.get("alternativeSolutionsConsidered") or []
        alt_total += len(alts)

        # ② en az üç aday
        if len(alts) < MIN_ALTERNATIVES:
            too_few.append("%s (%d aday)" % (pid, len(alts)))

        rejected_false = 0
        for i, a in enumerate(alts, 1):
            if not isinstance(a, dict):
                no_reason.append("%s aday %d (yapısız)" % (pid, i))
                continue
            # ③ gerekçe
            if not (a.get("reason") or "").strip():
                no_reason.append("%s aday %d" % (pid, i))
            # ④ zorlama gerekçe
            if a.get("reasonStrength") == FORCED:
                forced_reason.append("%s aday %d" % (pid, i))
            # ⑤ onaylanmış alternatif
            if a.get("rejected") is not True:
                rejected_false += 1
                confirmed_alt.append("%s aday %d" % (pid, i))

        # ⑥ public sayaç tutarlılığı
        declared = p.get("confirmedAlternativeSolutions", 0)
        if declared != rejected_false:
            counter_mismatch.append("%s (bildirilen %d ≠ ölçülen %d)"
                                    % (pid, declared, rejected_false))

        # ⑦ çözücünün önerdiği ikinci cevap
        for t in rec.get("solverTests") or []:
            if isinstance(t, dict) and (t.get("alternativeOffered") or "").strip():
                solver_alt.append("%s (%s)" % (pid, t.get("solver", "?")))

        fa = rec.get("finalAnswer") or ""
        if fa.strip():
            answers[fingerprint(fa)].append(pid)

    collisions = ["/".join(v) for v in answers.values() if len(v) > 1]

    rep.facts.update({"checked": checked, "alternativesConsidered": alt_total,
                      "answerCollisions": len(collisions)})

    rep.check(not not_flagged, "alternatif çözüm analizi public katmanda işaretli"
              + ("" if not not_flagged else " — İŞARETSİZ: %s" % not_flagged[:5]))
    rep.check(not too_few,
              "her bulmaca için ≥%d alternatif aday üretilmiş" % MIN_ALTERNATIVES
              + ("" if not too_few else " — YETERSİZ: %s" % too_few[:5]))
    rep.check(not no_reason, "her adayın reddedilme gerekçesi yazılmış"
              + ("" if not no_reason else " — GEREKÇESİZ: %s" % no_reason[:5]))
    rep.check(not forced_reason,
              "⭑ 'ZORLAMA' GEREKÇE YOK ⭑ (varsa bulmaca yeniden yazılır)"
              + ("" if not forced_reason else " — ⛔ ZORLAMA: %s" % forced_reason[:5]))
    rep.check(not confirmed_alt,
              "⭑ ONAYLANMIŞ ALTERNATİF ÇÖZÜM YOK ⭑"
              + ("" if not confirmed_alt else " — ⛔ İKİNCİ CEVAP: %s"
                 % confirmed_alt[:5]))
    rep.check(not counter_mismatch,
              "public sayaç korumalı kayıtla tutarlı"
              + ("" if not counter_mismatch else " — ÇELİŞKİ: %s"
                 % counter_mismatch[:5]))
    rep.check(not solver_alt,
              "⭑ HİÇBİR ÇÖZÜCÜ İKİNCİ BİR CEVAP ÖNERMEDİ ⭑"
              + ("" if not solver_alt else " — ⛔ AMPİRİK ÇİFT CEVAP: %s"
                 % solver_alt[:5]))
    rep.check(not collisions,
              "iki bulmaca aynı cevabı vermiyor"
              + ("" if not collisions else " — ÇAKIŞMA: %s" % collisions[:5]))

    return rep.finish("%d bulmaca · %d alternatif aday denetlendi"
                      % (checked, alt_total), args.json)


if __name__ == "__main__":
    sys.exit(main())
