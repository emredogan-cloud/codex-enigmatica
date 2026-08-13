#!/usr/bin/env python3
"""
İPUCU BÜTÜNLÜĞÜ KAPISI — Codex Enigmatica
================================================================================
Üç kademeli ipucu bu kitabın en somut rekabet farkıdır (K6): Cain's
Jawbone'u üç kişi çözdü ve bu, ticari olarak bir TERK ORANIDIR. Buradaki
konum tersidir — amaç okuru yenmek değil, İÇERİDE TUTMAKTIR.

Ama bir ipucu iki yönden bozulabilir ve bu kapı ikisini de arar:

  EKSİK  → okur takılır ve pes eder            (rekabet farkı kaybolur)
  FAZLA  → ipucu cevabı verir                  (bulmaca yok olur)

Yedi denetim:

  ① tam ÜÇ kademe var ve hiçbiri boş değil
  ② hiçbir kademe cevabı İÇERMİYOR — dört gizleme biçimine karşı
  ③ kademeler birbirinin AYNISI değil
  ④ ipucu uzunluğu bandında (kademe başına ≤40 kelime)
  ⑤ ipucu metni bulmacadan UZUN değil
  ⑥ ⭑ MERDİVEN GERÇEKTEN YÜKSELİYOR ⭑ — kapsam monoton artıyor
  ⑦ ⭑ 3. KADEME SON ADIMI VERMİYOR ⭑

② NEDEN DÖRT BİÇİM: düz alt dize araması naiftir. Bir ipucu cevabı
şu dört yolla da verebilir ve hepsi düz aramayı atlatır:
  · noktalama ve büyük harf farkı        → normalize edilir
  · boşlukların kaldırılması             → sıkıştırılmış biçim aranır
  · cevabın TERSTEN yazılması            → ters biçim aranır
  · çok kelimeli cevabın kelimelerinin   → kelime kümesi kapsaması aranır
    dağıtılması

⑦ NEDEN VAROLUŞSAL: 3. kademe "neredeyse-cevap"tır — son adım HARİÇ her
şeyi verir. Son adımı da verirse ipucu bir cevap anahtarıdır ve arka
maddedeki çözüm bölümünün anlamı kalmaz. Meta-misterde bu daha da sert:
son sorunun cevabı kitapta HİÇ YOKTUR.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

MAX_HINT_WORDS = 40
# Bir çözüm adımının "verilmiş" sayılması için ipucuyla paylaşması gereken
# içerik kelimesi sayısı. 2 bilerek seçildi: 1 rastlantısaldır, 3 kaçırır.
STEP_TOUCH_MIN = 2


def leaks_answer(hint: str, answers: list[str]) -> str | None:
    """İpucu cevabı DÖRT gizleme biçiminden biriyle veriyor mu."""
    h_norm, h_squeeze = pl.norm(hint), pl.squeeze(hint)
    h_words = set(pl.words(hint))
    for ans in answers:
        if not ans:
            continue
        a_norm, a_squeeze = pl.norm(ans), pl.squeeze(ans)
        if len(a_squeeze) < 3:
            continue                      # çok kısa: rastlantı üretir
        if a_norm and a_norm in h_norm:
            return "düz"
        if a_squeeze in h_squeeze:
            return "boşluksuz"
        if a_squeeze[::-1] in h_squeeze:
            return "ters"
        a_words = {w for w in pl.words(ans) if len(w) >= 3}
        if len(a_words) >= 2 and a_words.issubset(h_words):
            return "dağıtılmış"
    return None


def step_coverage(hint: str, steps: list[str]) -> set[int]:
    """İpucunun DOKUNDUĞU çözüm adımlarının kümesi."""
    hw = pl.content_words(hint)
    touched = set()
    for i, s in enumerate(steps):
        if len(hw & pl.content_words(s)) >= STEP_TOUCH_MIN:
            touched.add(i)
    return touched


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
    print("  İPUCU BÜTÜNLÜĞÜ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    levels = cfg.get("solvability", {}).get("hintLadderLevels", 3)

    pre = pl.preflight(rep, gate_level, "ipucu")
    if pre is None:
        return rep.finish("denetlenecek ipucu yok", args.json)
    need, sols, _designs = pre

    counts = {"records": 0, "hints": 0, "leaks": 0}
    missing_ladder, leaked, duplicated = [], [], []
    too_long, longer_than_puzzle = [], []
    not_monotonic, gives_last_step = [], []

    print("\n── ipucu kayıtları ──")
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid)
        if not rec:
            continue
        counts["records"] += 1
        hints = rec.get("hints") or []

        # ① üç kademe
        if len(hints) != levels or any(not (h or "").strip() for h in hints):
            missing_ladder.append("%s (%d kademe)" % (pid, len(hints)))
            continue
        counts["hints"] += len(hints)

        # ② cevap sızıntısı
        answers = [rec.get("finalAnswer", ""), rec.get("intendedSolution", "")]
        for i, h in enumerate(hints, 1):
            how = leaks_answer(h, answers)
            if how:
                counts["leaks"] += 1
                leaked.append("%s kademe %d (%s gizleme)" % (pid, i, how))

        # ③ tekrar
        norms = [pl.norm(h) for h in hints]
        if len(set(norms)) != len(norms):
            duplicated.append(pid)

        # ④ uzunluk bandı
        for i, h in enumerate(hints, 1):
            n = len(pl.words(h))
            if n > MAX_HINT_WORDS:
                too_long.append("%s kademe %d (%d kelime)" % (pid, i, n))

        # ⑤ TEK BİR ipucu bulmacadan uzun olamaz.
        # ⚠ Kural Faz 1'de düzeltildi. Eski hâli üç ipucunun TOPLAMINI
        # bulmaca metniyle karşılaştırıyordu ve STYLE § 4 ile çelişiyordu:
        # ipucu başına 40 kelime tavanı ile üç kademe 120 kelime eder, ama
        # bulmaca metninin alt sınırı 90 kelimedir. Yani kurallar birlikte
        # 90 kelimelik bir bulmaca için kademe başına 30 kelime bırakıyordu
        # — ve katmanlı bir zincir için 30 kelimede "neredeyse-cevap"
        # YAZILAMAZ. Bir kuralın diğerini yazılamaz kılması, kural değil
        # çelişkidir.
        puzzle_text = " ".join(
            [rec.get("objective", ""), rec.get("readerAction", "")]
            + list(rec.get("clues") or []))
        if puzzle_text.strip():
            plen = len(pl.words(puzzle_text))
            for i, h in enumerate(hints, 1):
                if len(pl.words(h)) > plen:
                    longer_than_puzzle.append("%s kademe %d" % (pid, i))

        # ⑥⑦ merdiven
        steps = [s.get("step", "") if isinstance(s, dict) else str(s)
                 for s in (rec.get("solutionPath") or [])]
        if steps:
            cov = [step_coverage(h, steps) for h in hints]
            sizes = [len(c) for c in cov]
            if not (sizes[0] <= sizes[1] <= sizes[2]):
                not_monotonic.append("%s (kapsam %s)" % (pid, sizes))
            if (len(steps) - 1) in cov[2]:
                gives_last_step.append(pid)

    rep.facts.update(counts)

    rep.check(not missing_ladder,
              "her bulmacada tam %d kademe var ve hiçbiri boş değil" % levels
              + ("" if not missing_ladder else " — EKSİK: %s" % missing_ladder[:5]))
    rep.check(not leaked,
              "⭑ HİÇBİR İPUCU CEVABI İÇERMİYOR ⭑"
              + ("" if not leaked else " — ⛔ SIZINTI: %s" % leaked[:5]))
    rep.check(not duplicated, "kademeler birbirinin aynısı değil"
              + ("" if not duplicated else " — TEKRAR: %s" % duplicated[:5]))
    rep.check(not too_long, "ipucu uzunluğu ≤%d kelime" % MAX_HINT_WORDS
              + ("" if not too_long else " — AŞIM: %s" % too_long[:5]))
    rep.check(not longer_than_puzzle,
              "hiçbir ipucu tek başına bulmacadan uzun değil"
              + ("" if not longer_than_puzzle
                 else " — AŞIM: %s" % longer_than_puzzle[:5]))
    rep.check(not not_monotonic,
              "⭑ MERDİVEN YÜKSELİYOR ⭑ (kapsam monoton artıyor)"
              + ("" if not not_monotonic else " — DÜZ/İNEN: %s" % not_monotonic[:5]))
    rep.check(not gives_last_step,
              "⭑ 3. KADEME SON ADIMI VERMİYOR ⭑"
              + ("" if not gives_last_step
                 else " — ⛔ CEVAP ANAHTARI: %s" % gives_last_step[:5]))

    return rep.finish("%d kayıt · %d ipucu denetlendi"
                      % (counts["records"], counts["hints"]), args.json)


if __name__ == "__main__":
    sys.exit(main())
