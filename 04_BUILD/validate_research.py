#!/usr/bin/env python3
"""
ARAŞTIRMA VE KÜNYE KAPISI — Codex Enigmatica
================================================================================
Bu kitapta olgu hatası iki ayrı yerden vurur:

  ① okur bir motifin yanlış anlatıldığını görür        → itibar
  ② bulmaca YANLIŞ BİR OLGUYA dayanır ve çözülemez     → ürün hatası

②, bu projede ①'den ağırdır. Bir bulmaca "Ogham'da şu harf şudur"
varsayımıyla kuruluysa ve o varsayım yanlışsa, bulmacanın çözümü
DETERMİNİSTİK OLMAKTAN ÇIKAR — ve kusuru okur bulur.

Bu yüzden kural sert: BULMACA KOLAYLIĞI İÇİN OLGU UYDURULMAZ.
Bir motifin işe yarayan hâli yoksa BULMACA değişir, olgu değil.

Altı denetim:

  ① her künye kaydı tam (kimlik · başlık · yıl · haklar · kullanım)
  ② her sourceRefs anahtarı künye kaydında VAR
  ③ ölü künye yok — kaydedilen her kaynak en az bir bulmacada kullanılıyor
  ④ telifli kaynak yalnızca DOĞRULAMA için; hiçbiri çoğaltılmıyor
  ⑤ hiçbir kaynak OKURDAN talep edilmiyor (dış bilgi yasağı)
  ⑥ ⭑ yazılmış bulmacaların kaynağı 'checked' ⭑ — Faz 2'den itibaren

⑥ NEDEN FAZ 2'DEN İTİBAREN: aday bir FİKİRDİR, basılacak bir olgu
değildir. 'asserted' bir künye aday aşamasında yeterlidir. Ama bir
bulmaca yazıldığı anda dayandığı olgu insan gözüyle doğrulanmış
olmalıdır — ajanın "bu kaynak gerçektir" kanaati bir doğrulama değildir.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SOURCES = os.path.join(ROOT, "01_SOURCE", "research", "sources.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")

REQUIRED_FIELDS = ("id", "kind", "title", "year", "rightsStatus",
                   "verificationStatus", "usage")
VALID_RIGHTS = ("public-domain", "licensed", "permission-granted",
                "verification-only")
VALID_VERIFICATION = ("asserted", "checked")
# Bu durumlardaki bulmacalar BASILACAK metne dönüşmüştür; künyeleri
# artık 'asserted' kalamaz.
PRINT_BOUND_STATUS = ("validated", "written")
VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5",
               "release"]


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    gate_level = args.gate or read_gate()
    if gate_level not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate_level, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  ARAŞTIRMA VE KÜNYE · kapı: %s" % gate_level)
    print("=" * 74)

    rep = Report(args.verbose)

    if not os.path.exists(SOURCES):
        if gate_level == "phase0":
            print("\n  ⊘ sources.json yok — phase0'da beklenen")
            print("=" * 74)
            return 0
        rep.check(False, "01_SOURCE/research/sources.json var")
        print("=" * 74)
        return 1

    srcs = load(SOURCES).get("sources", [])
    by_id = {s.get("id"): s for s in srcs}
    rep.facts["sources"] = len(srcs)

    # ── ① kayıt bütünlüğü ───────────────────────────────────────────────
    print("\n── ① künye bütünlüğü ──")
    incomplete = [s.get("id", "?") for s in srcs
                  if any(not s.get(k) for k in REQUIRED_FIELDS)]
    rep.check(not incomplete, "her künye kaydı tam"
              + ("" if not incomplete else " — EKSİK: %s" % incomplete[:5]))
    rep.check(len(by_id) == len(srcs), "künye kimlikleri tekil")

    bad_rights = [s["id"] for s in srcs
                  if s.get("rightsStatus") not in VALID_RIGHTS]
    rep.check(not bad_rights, "haklar durumu geçerli"
              + ("" if not bad_rights else " — GEÇERSİZ: %s" % bad_rights[:5]))
    bad_ver = [s["id"] for s in srcs
               if s.get("verificationStatus") not in VALID_VERIFICATION]
    rep.check(not bad_ver, "doğrulama durumu geçerli"
              + ("" if not bad_ver else " — GEÇERSİZ: %s" % bad_ver[:5]))

    # ── ④ haklar ────────────────────────────────────────────────────────
    print("\n── ④ haklar ──")
    non_pd = [s for s in srcs if s.get("rightsStatus") != "public-domain"]
    reproduced = [s["id"] for s in non_pd if s.get("reproduced") is True]
    rep.check(not reproduced,
              "kamusal alanda olmayan hiçbir kaynak ÇOĞALTILMIYOR"
              + ("" if not reproduced else " — İHLAL: %s" % reproduced[:5]))
    rep.facts["publicDomain"] = len(srcs) - len(non_pd)
    if non_pd:
        rep.warn("%d kaynak kamusal alanda değil — yalnızca doğrulama için "
                 "kullanılabilir: %s" % (len(non_pd), [s["id"] for s in non_pd]))

    # ── ⑤ dış bilgi yasağı ──────────────────────────────────────────────
    print("\n── ⑤ dış bilgi yasağı ──")
    reader_needs = [s["id"] for s in srcs if s.get("readerNeedsIt") is True]
    rep.check(not reader_needs,
              "hiçbir kaynak OKURDAN talep edilmiyor (sözleşme § 2)"
              + ("" if not reader_needs else " — ⛔ İHLAL: %s" % reader_needs[:5]))

    # ── ②③⑥ bulmaca bağlantısı ─────────────────────────────────────────
    if not os.path.exists(PUZZLE_INDEX):
        rep.warn("puzzle_index.json yok — kaynak/bulmaca bağı denetlenemedi")
        puzzles = []
    else:
        puzzles = load(PUZZLE_INDEX).get("puzzles", [])

    print("\n── ② künye referansları ──")
    used: set[str] = set()
    dangling: list[str] = []
    for p in puzzles:
        for key in p.get("sourceRefs", []) or []:
            used.add(key)
            if key not in by_id:
                dangling.append("%s → %s" % (p.get("puzzleId"), key))
    rep.check(not dangling, "her sourceRefs anahtarı künye kaydında var"
              + ("" if not dangling else " — KAYIP: %s" % dangling[:5]))
    rep.facts["referenced"] = len(used)

    print("\n── ③ ölü künye ──")
    dead = sorted(set(by_id) - used)
    # Ölü künye bir hata değil bir SARKMADIR: kaydedildi ama kullanılmadı.
    # Faz 4'te (manuscript özünde tamam) artık kabul edilmez.
    if gate_level in ("phase4", "phase5", "release"):
        rep.check(not dead, "kullanılmayan künye yok"
                  + ("" if not dead else " — ÖLÜ: %s" % dead))
    elif dead:
        rep.warn("%d künye henüz hiçbir bulmacada kullanılmıyor "
                 "(Faz 4'te KIRMIZI olur): %s" % (len(dead), dead))

    print("\n── ⑥ ⭑ yazılmış bulmacanın künyesi doğrulanmış mı ⭑ ──")
    unverified: list[str] = []
    for p in puzzles:
        if p.get("status") not in PRINT_BOUND_STATUS:
            continue
        for key in p.get("sourceRefs", []) or []:
            s = by_id.get(key)
            if s and s.get("verificationStatus") != "checked":
                unverified.append("%s → %s" % (p.get("puzzleId"), key))
    rep.check(not unverified,
              "basılacak her bulmacanın kaynağı 'checked'"
              + ("" if not unverified
                 else " — ⛔ DOĞRULANMAMIŞ: %s" % unverified[:5]))

    n_asserted = sum(1 for s in srcs if s.get("verificationStatus") == "asserted")
    rep.facts["asserted"] = n_asserted
    rep.facts["checked"] = len(srcs) - n_asserted
    if n_asserted:
        rep.warn("%d künye hâlâ 'asserted' — bir bulmaca yazılmadan ÖNCE "
                 "insan gözüyle doğrulanmalıdır (KURUCU BAĞIMLILIĞI)"
                 % n_asserted)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d künye · %d referanslı"
              % (rep.checks, len(srcs), len(used)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate_level,
                       "checks": rep.checks, "errors": rep.errors,
                       "warnings": rep.warnings, "facts": rep.facts},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
