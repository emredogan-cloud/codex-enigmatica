#!/usr/bin/env python3
"""
ÇÖZÜLEBİLİRLİK KAPISI — Codex Enigmatica
================================================================================
Bu projenin BİRİNCİ varoluşsal kuralını mekanikleştirir (K4):

  > Bir bulmaca "zekice göründüğü" için kabul EDİLEMEZ.
  > Deterministik olarak çözülemeyen bir bulmaca bir ÜRETİM HATASIDIR.

SOLVABILITY_STANDARD § 2'nin beş şartından üçünü bu kapı ölçer
(dördüncüyü qa_uniqueness, beşincisini validate_spec § test durumu):

  ① çözüm yolu ADIM ADIM kayıtlı
  ② her adım YALNIZCA kitap içi bilgiyle yürüyor
  ④ belirsizlik puanı ≤ 2 VE puanın GEREKÇESİ kayıtlı

Ek olarak dört yapısal denetim:

  ⑤ hedef, okur eylemi, girdi ve kısıtlar dolu
  ⑥ ⭑ KISITSIZ BULMACA YOK ⭑ — kısıt yoksa tekillik iddiası dayanaksızdır
  ⑦ talimat cümlesi ≤20 kelime (STYLE § 4)
  ⑧ belirsizlik puanı ile belirsizlik noktaları TUTARLI

② NEDEN EN SERT: sözleşme sayfasında okura "hiçbiri kitabın dışındaki
bilgiyi gerektirmez" denir. Bu pazarlama değil ÜRETİM KISITIDIR. Tek bir
adımda `usesOnlyBookKnowledge: false` görmek, o vaadin yazılı olarak
bozulduğunu görmektir.

⑧ NEDEN VAR: belirsizlik puanı bir SAYIDIR ve sayı yazması kolaydır.
Bir bulmacaya "1" yazıp üç belirsizlik noktası kaydetmek, kapıyı
kandırmaktır. Bu denetim puanı gerekçesine bağlar.

⑥ NEDEN VAR: "tek cevabı var" bir iddiadır. O iddianın taşıyıcısı
KISITLARDIR — cevabı tekleştiren şey onlardır. Kısıt listesi boş bir
bulmacanın tekilliği kanıtlanmamıştır, yalnızca umulmuştur.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

MAX_INSTRUCTION_WORDS = 20
SENTENCE_SPLIT = re.compile(r"[.!?]+\s+|\n+")


def long_sentences(text: str, limit: int) -> list[str]:
    out = []
    for s in SENTENCE_SPLIT.split(text or ""):
        n = len(pl.words(s))
        if n > limit:
            out.append("%d kelime" % n)
    return out


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
    print("  ÇÖZÜLEBİLİRLİK · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    max_amb = cfg.get("solvability", {}).get("maxAcceptableAmbiguityScore", 2)

    pre = pl.preflight(rep, gate_level, "çözülebilirlik")
    if pre is None:
        return rep.finish("denetlenecek çözüm yolu yok", args.json)
    need, sols, designs = pre

    no_path, external_step, no_source = [], [], []
    empty_field, no_constraints, long_instr = [], [], []
    amb_over, amb_missing, amb_inconsistent, amb_unresolved = [], [], [], []
    checked = 0
    step_total = 0

    print("\n── çözüm yolları ──")
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid)
        if not rec:
            continue
        checked += 1
        design = designs.get(pid, {})

        # ① adım adım kayıtlı
        steps = rec.get("solutionPath") or []
        if not steps:
            no_path.append(pid)
            continue
        step_total += len(steps)

        # ② dış bilgi yasağı
        for i, s in enumerate(steps, 1):
            if not isinstance(s, dict):
                no_path.append("%s (adım %d yapısız)" % (pid, i))
                continue
            if s.get("usesOnlyBookKnowledge") is not True:
                external_step.append("%s adım %d" % (pid, i))
            elif not (s.get("sourceInBook") or "").strip():
                no_source.append("%s adım %d" % (pid, i))

        # ⑤ yapısal alanlar
        for field in ("objective", "readerAction", "input", "finalAnswer",
                      "explanation"):
            if not (rec.get(field) or "").strip():
                empty_field.append("%s.%s" % (pid, field))

        # ⑥ kısıtlar
        cons = (rec.get("constraints") or []) or (design.get("constraints") or [])
        if not cons:
            no_constraints.append(pid)

        # ⑦ talimat uzunluğu
        for field in ("objective", "readerAction"):
            over = long_sentences(rec.get(field, ""), MAX_INSTRUCTION_WORDS)
            if over:
                long_instr.append("%s.%s (%s)" % (pid, field, over[0]))

        # ④⑧ belirsizlik
        score = p.get("ambiguityScore")
        points = design.get("ambiguityPoints") or rec.get("ambiguityPoints") or []
        if score is None:
            amb_missing.append(pid)
        else:
            if score > max_amb:
                amb_over.append("%s (%d > %d)" % (pid, score, max_amb))
            # Gerekçe kayıtlı mı: puan 1 iddiası bedava değildir.
            unresolved = [q for q in points
                          if isinstance(q, dict)
                          and not (q.get("resolution") or "").strip()]
            if unresolved:
                amb_unresolved.append("%s (%d çözülmemiş nokta)"
                                      % (pid, len(unresolved)))
            residual = max([q.get("residualRisk", 1) for q in points
                            if isinstance(q, dict)] or [1])
            if residual > score:
                amb_inconsistent.append("%s (puan %d < kalıcı risk %d)"
                                        % (pid, score, residual))
            if score == 1 and len(points) >= 2:
                amb_inconsistent.append("%s (puan 1 ama %d belirsizlik noktası)"
                                        % (pid, len(points)))

    rep.facts.update({"checked": checked, "solutionSteps": step_total,
                      "maxAmbiguityAllowed": max_amb})

    rep.check(not no_path, "her bulmacanın çözüm yolu ADIM ADIM kayıtlı"
              + ("" if not no_path else " — ⛔ YOLSUZ: %s" % no_path[:5]))
    rep.check(not external_step,
              "⭑ HER ADIM YALNIZCA KİTAP İÇİ BİLGİYLE YÜRÜYOR ⭑"
              + ("" if not external_step
                 else " — ⛔ SÖZLEŞME İHLALİ: %s" % external_step[:5]))
    rep.check(not no_source,
              "her adım kitap içindeki dayanağını gösteriyor"
              + ("" if not no_source else " — DAYANAKSIZ: %s" % no_source[:5]))
    rep.check(not empty_field, "yapısal alanlar dolu"
              + ("" if not empty_field else " — BOŞ: %s" % empty_field[:5]))
    rep.check(not no_constraints,
              "⭑ KISITSIZ BULMACA YOK ⭑ (tekilliğin taşıyıcısı kısıtlardır)"
              + ("" if not no_constraints else " — KISITSIZ: %s" % no_constraints[:5]))
    rep.check(not long_instr,
              "talimat cümlesi ≤%d kelime" % MAX_INSTRUCTION_WORDS
              + ("" if not long_instr else " — UZUN: %s" % long_instr[:5]))
    rep.check(not amb_missing, "her yazılmış bulmacada belirsizlik puanı var"
              + ("" if not amb_missing else " — PUANSIZ: %s" % amb_missing[:5]))
    rep.check(not amb_over, "belirsizlik puanı ≤%d" % max_amb
              + ("" if not amb_over else " — ⛔ AŞIM: %s" % amb_over[:5]))
    rep.check(not amb_unresolved,
              "her belirsizlik noktasının metinsel çözümü kayıtlı"
              + ("" if not amb_unresolved
                 else " — ÇÖZÜMSÜZ: %s" % amb_unresolved[:5]))
    rep.check(not amb_inconsistent,
              "⭑ belirsizlik PUANI gerekçesiyle TUTARLI ⭑"
              + ("" if not amb_inconsistent
                 else " — ⛔ ÇELİŞKİ: %s" % amb_inconsistent[:5]))

    return rep.finish("%d bulmaca · %d çözüm adımı denetlendi"
                      % (checked, step_total), args.json)


if __name__ == "__main__":
    sys.exit(main())
