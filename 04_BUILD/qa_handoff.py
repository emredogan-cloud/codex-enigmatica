#!/usr/bin/env python3
"""
⭑ DEVİR VE HATA DAVRANIŞI KAPISI ⭑ — Faz 1 bulgusu 6.4 geri dönmesin
================================================================================
Faz 1'in kırmızı takımı şunu buldu:

    TEK BİR YANLIŞ CEVAP OKURU ÜRÜNÜN %80'İNDEN DIŞARIDA BIRAKIYORDU.

Kapılar arası devir bağı kapatıldı (`crossGateEntryHandoff: false`) ama
kusurun KÜÇÜK BİR KOPYASI kapının içinde duruyordu: kapı bulmacası on
dokuz girdiye bağlıdır ve bir girdi yanlışsa çıktı SESSİZCE yanlış olur.

Sessiz yanlış, gürültülü yanlıştan daha kötüdür. Okur on dokuz cevabını
birleştirir, makul görünen bir dize elde eder, doğrulama sayfası reddeder
— ve okur hangi bulmacanın yanlış olduğunu BİLEMEZ. On dokuz aday arasında
kaybolur. İpucu merdiveni orada işe yaramaz çünkü okur hangi bulmacaya
ipucu alacağını bilmiyordur. Yani bağımlılık grafiği, sözleşmenin üçüncü
sözünü (*"ipucu almak kaybetmek değildir"*) sessizce iptal eder.

Altı denetim:

  ① `crossGateEntryHandoff` HÂLÂ false (gerileme koruması)
  ② ⭑ KAPI BULMACASININ HATA TESPİTİ VAR ⭑ — çıktı basılı bir listeye düşer
  ③ ⭑ BASILI LİSTE GERÇEKTEN HATA TESPİT EDİYOR ⭑ — asgari Hamming mesafesi ≥2
  ④ ⭑ TEŞHİS İŞARETLERİ VAR VE DOĞRU ⭑ — okur hatayı TEK BİR slota indirebiliyor
  ⑤ kurtarma yolu ve bozucu olmayan ilerleme kayıtlı
  ⑥ ⭑ TEK BİR HATANIN YAYILMA YARIÇAPI ≤ 1 ⭑ (kapı bulmacası hariç)

③ NEDEN ÖLÇÜLÜR, İDDİA EDİLMEZ: "çıktı listede yoksa hata vardır" cümlesi,
listenin iki üyesi birbirine bir harf uzaklıktaysa YANLIŞTIR — o zaman tek
bir hata, okuru BAŞKA BİR GEÇERLİ İFADEYE götürür ve hata tespit edilmez,
GİZLENİR. Bu kapı mesafeyi ölçer.

④ NEDEN VAROLUŞSAL: hata tespiti "bir yerde yanlış var" der; teşhis
"şurada yanlış var" der. Aradaki fark, on dokuz bulmacayı yeniden çözmek
ile birini yeniden çözmek arasındaki farktır.

⚠ BU KAPI CEVAP İÇERİĞİ YAZDIRMAZ.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
from qa_answerspace import TOOLS, Plate                        # noqa: E402

GATE_INDEX = os.path.join(pl.ROOT, "01_SOURCE", "gate_index.json")
MIN_HAMMING = 2
ERROR_DETECTING_ACCEPTANCE = {"in-printed-phrase-list",
                              "matches-positional-extraction",
                              "reachable-via-number-table"}


def hamming_min(entries: list[str], plate: Plate) -> int | None:
    """Aynı uzunluktaki basılı ifadeler arasındaki EN KÜÇÜK harf farkı.

    Harf dizisi normalize edilir (boşluk ve noktalama atılır) çünkü okur
    on dokuz HARF üretir, on dokuz harf artı boşluk değil."""
    seqs = [pl.squeeze(e) for e in entries]
    best = None
    for i in range(len(seqs)):
        for j in range(i + 1, len(seqs)):
            if len(seqs[i]) != len(seqs[j]):
                continue
            d = sum(a != b for a, b in zip(seqs[i], seqs[j]))
            best = d if best is None else min(best, d)
    return best


def blast_radius(puzzles: list[dict], gate_ids: set[str]) -> dict[str, int]:
    """Bir bulmacayı yanlış çözmek kaç bulmacayı daha bloklar.

    Kapı bulmacası hariç tutulur: o tanımı gereği on dokuz girdiyi
    birleştirir ve yarıçapı küçültülerek değil, hata tespiti + teşhis +
    kurtarma yoluyla korunur."""
    succ: dict[str, list[str]] = {}
    for p in puzzles:
        for d in p.get("dependencies") or []:
            succ.setdefault(d, []).append(p["puzzleId"])
    out: dict[str, int] = {}
    for p in puzzles:
        pid = p["puzzleId"]
        seen, stack = set(), list(succ.get(pid, []))
        while stack:
            n = stack.pop()
            if n in seen or n in gate_ids:
                continue
            seen.add(n)
            stack.extend(succ.get(n, []))
        out[pid] = len(seen)
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
    print("  ⭑ DEVİR VE HATA DAVRANIŞI ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    spec = cfg.get("solvability", {}).get("gateHandoff", {})
    max_blast = spec.get("maxSinglePuzzleBlastRadius", 1)

    # ① gerileme koruması — bu denetim korumalı katman OLMADAN da koşar
    print("\n── ① kapılar arası devir bağı ──")
    gi = pl.load_json(GATE_INDEX) or {}
    rules = gi.get("dependencyRules", {})
    rep.check(rules.get("crossGateEntryHandoff") is False,
              "⭑ kapılar arası devir bağı KAPALI ⭑ (Faz 1 bulgusu 6.4)")
    rep.check(spec.get("crossGateEntryHandoff") is False,
              "config aynı şeyi söylüyor (iki kaynak ayrışmıyor)")
    for key, label in (("requireErrorDetection", "hata tespiti şartı"),
                       ("requireRecoveryPath", "kurtarma yolu şartı"),
                       ("requireDiagnosticFeedback", "teşhis şartı"),
                       ("requireNonDestructiveProgression",
                        "bozucu olmayan ilerleme şartı")):
        rep.check(spec.get(key) is True, "%s duruyor" % label)

    pre = pl.preflight(rep, gate_level, "devir")
    if pre is None:
        return rep.finish("denetlenecek kapı bulmacası yok", args.json)
    need, sols, designs = pre
    plate = Plate(pl.load_json(TOOLS) or {})

    puzzles = pl.load_index()
    gate_ids = {p["puzzleId"] for p in puzzles if p.get("type") == "gate"}

    # ⑥ yayılma yarıçapı
    print("\n── ⑥ tek bir hatanın yayılma yarıçapı ──")
    radius = blast_radius(puzzles, gate_ids)
    over = ["%s (%d)" % (k, v) for k, v in sorted(radius.items())
            if v > max_blast and k not in gate_ids]
    rep.facts["maxBlastRadius"] = max(radius.values()) if radius else 0
    rep.check(not over,
              "⭑ TEK BİR HATANIN YAYILMA YARIÇAPI ≤%d ⭑ (kapı hariç)" % max_blast
              + ("" if not over else " — ⛔ AŞAN: %s" % over[:5]))

    # ②③④⑤ kapı bulmacaları
    print("\n── ②③④⑤ kapı bulmacası hata davranışı ──")
    no_detect, weak_list, bad_marks, no_recovery = [], [], [], []
    checked = 0
    for p in need:
        pid = p["puzzleId"]
        if pid not in gate_ids:
            continue
        checked += 1
        rec, dsg = sols.get(pid) or {}, designs.get(pid) or {}
        acc = (rec.get("answerSpace") or {}).get("acceptance") or {}

        # ② hata tespiti var mı
        if acc.get("kind") not in ERROR_DETECTING_ACCEPTANCE:
            no_detect.append("%s (kabul '%s')" % (pid, acc.get("kind")))
            continue

        # ③ basılı liste GERÇEKTEN hata tespit ediyor mu
        d = hamming_min(plate.phrases, plate)
        rep.facts["minHammingDistance"] = d
        if d is not None and d < MIN_HAMMING:
            weak_list.append("%s (asgari mesafe %d < %d)" % (pid, d, MIN_HAMMING))

        # ④ teşhis işaretleri — BAĞIMSIZ hesaplanır, kayıttan okunmaz
        ho = dsg.get("handoff") or {}
        marks = ho.get("diagnosticMarks") or []
        src = acc.get("sources") or []
        pos = acc.get("positions") or []
        if len(marks) != len(src) or not src:
            bad_marks.append("%s (işaret %d ≠ girdi %d)"
                             % (pid, len(marks), len(src)))
        else:
            wrong = 0
            for m, s, q in zip(marks, src, pos):
                letter = s[q - 1]
                if m.get("group") != plate.group(letter):
                    wrong += 1
            if wrong:
                bad_marks.append("%s (%d işaret yanlış)" % (pid, wrong))

        # ⑤ kurtarma yolu ve bozucu olmayan ilerleme
        if not (ho.get("recoveryPath") or "").strip() or \
                ho.get("nonDestructiveProgression") is not True:
            no_recovery.append(pid)

    rep.facts["gatePuzzles"] = checked

    rep.check(checked > 0, "kapı bulmacası bulundu ve denetlendi (%d)" % checked)
    rep.check(not no_detect,
              "⭑ KAPI BULMACASININ HATA TESPİTİ VAR ⭑"
              + ("" if not no_detect else " — ⛔ SESSİZ YANLIŞ: %s" % no_detect[:5]))
    rep.check(not weak_list,
              "⭑ BASILI LİSTE GERÇEKTEN HATA TESPİT EDİYOR ⭑ (asgari Hamming ≥%d)"
              % MIN_HAMMING
              + ("" if not weak_list else " — ⛔ ZAYIF: %s" % weak_list[:5]))
    rep.check(not bad_marks,
              "⭑ TEŞHİS İŞARETLERİ VAR VE BAĞIMSIZ HESAPLA UYUŞUYOR ⭑"
              + ("" if not bad_marks else " — ⛔ TEŞHİS YOK/YANLIŞ: %s"
                 % bad_marks[:5]))
    rep.check(not no_recovery,
              "kurtarma yolu ve bozucu olmayan ilerleme kayıtlı"
              + ("" if not no_recovery else " — EKSİK: %s" % no_recovery[:5]))

    return rep.finish("%d kapı bulmacası · yayılma yarıçapı ≤%d"
                      % (checked, rep.facts.get("maxBlastRadius", 0)), args.json)


if __name__ == "__main__":
    sys.exit(main())
