#!/usr/bin/env python3
"""
KORUMALI KATMAN OKUYUCUSU — üç çözülebilirlik kapısının ortak tabanı
================================================================================
⚠ BU BİR ORTAK KÜTÜPHANE DEĞİLDİR — K1'in yasakladığı şey PROJELER ARASI
paylaşılan kütüphanedir. Bu dosya tek bir projenin içindedir ve tek bir
şey yapar: korumalı katmanı okur.

NEDEN AYRI BİR DOSYA: qa_solvability, qa_uniqueness ve qa_hints AYNI
katmanı okur. Okuma mantığı üç yere kopyalansaydı, katman taşındığında
ikisi güncellenir biri unutulurdu — ve unutulan kapı SESSİZCE BOŞ KOŞARDI.
Boş koşan bir kapı, olmayan bir kapıdan daha tehlikelidir: yeşil yanar.

⭑ BU DOSYA HİÇBİR ZAMAN ÇÖZÜM İÇERİĞİ YAZDIRMAZ. ⭑
Raporlara yalnızca bulmaca kimliği ve sayılar gider. Bir doğrulayıcının
kendi raporu üzerinden sızıntı yapması, bu projede en sinsi kaçış yoludur
(rapor 06_REPORTS/ altında ve o dizin TAKİP EDİLİYOR).
"""

from __future__ import annotations

import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(HERE)

# ⚠ TEST KANCASI. Yalnızca selftest kullanır; CI bunu ASLA kurmaz.
# Kurulu olduğunda kapılar kurgu bir köke bakar ve gerçek depo okunmaz.
ROOT = os.environ.get("ENIGMATICA_ROOT", _DEFAULT_ROOT)

SOLUTIONS_DIR = os.path.join(ROOT, "01_SOURCE", "solutions")
DESIGN_DIR = os.path.join(ROOT, "01_SOURCE", "design")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")
CONFIG = os.path.join(ROOT, "project_config.json")

# Korumalı kaydı BULUNMASI GEREKEN durumlar. 'candidate' bir fikirdir;
# fikrin çözümü olmaz.
NEEDS_PROTECTED = ("drafted", "validated", "written")

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

    def finish(self, title: str, json_path: str | None, extra: dict | None = None) -> int:
        print("\n" + "=" * 74)
        if self.warnings:
            print("  %d uyarı" % len(self.warnings))
        if self.errors:
            print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(self.errors), self.checks))
            for e in self.errors:
                print("     · %s" % e)
            status = "fail"
        else:
            print("  ✅ %d denetim yeşil · %s" % (self.checks, title))
            status = "pass"
        print("=" * 74)
        if json_path:
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            payload = {"status": status, "checks": self.checks,
                       "errors": self.errors, "warnings": self.warnings,
                       "facts": self.facts}
            if extra:
                payload.update(extra)
            with open(json_path, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
        return 1 if self.errors else 0


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def load_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_config() -> dict:
    return load_json(CONFIG) or {}


def load_index() -> list[dict]:
    idx = load_json(PUZZLE_INDEX)
    if not idx:
        return []
    return idx.get("puzzles", []) if isinstance(idx, dict) else idx


def _read_dir(path: str) -> dict[str, dict]:
    """Korumalı dizindeki her kaydı puzzleId ile anahtarlar.

    Bir dosya birden çok kayıt taşıyabilir ({"puzzles": [...]}) ya da tek
    bir kayıt olabilir. İkisi de kabul edilir: Faz 2 kapı başına tek dosya
    (gate-1.json) kullanacak, Faz 1 fikstürleri tek kayıt kullanıyor."""
    out: dict[str, dict] = {}
    if not os.path.isdir(path):
        return out
    for name in sorted(os.listdir(path)):
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(path, name), encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        records = data if isinstance(data, list) else data.get("puzzles", [data])
        for rec in records:
            if isinstance(rec, dict) and rec.get("puzzleId"):
                out[rec["puzzleId"]] = rec
    return out


def load_protected() -> tuple[dict[str, dict], dict[str, dict]]:
    """(çözüm kayıtları, tasarım kayıtları)"""
    return _read_dir(SOLUTIONS_DIR), _read_dir(DESIGN_DIR)


def preflight(rep: Report, gate_level: str, kind: str) -> tuple[list, dict, dict] | None:
    """Ortak açılış: envanteri ve korumalı katmanı yükler, katmanın
    VARLIĞINI kapı seviyesine göre denetler.

    Dönüş None ise çağıran hemen bitirmelidir."""
    puzzles = load_index()
    sols, designs = load_protected()
    need = [p for p in puzzles if p.get("status") in NEEDS_PROTECTED]

    rep.facts["indexed"] = len(puzzles)
    rep.facts["needProtected"] = len(need)
    rep.facts["solutionRecords"] = len(sols)
    rep.facts["designRecords"] = len(designs)

    print("\n── korumalı katman ──")
    print("  envanter %d · korumalı kayıt bekleyen %d · çözüm kaydı %d · "
          "tasarım kaydı %d" % (len(puzzles), len(need), len(sols), len(designs)))

    if not need:
        # Faz 1: hiçbir bulmaca yazılmadı. Kapı denetleyecek bir şey
        # bulamıyor ve bunu SÖYLÜYOR — sessizce yeşil yanmıyor.
        print("  ⊘ yazılmış bulmaca yok → %s kapısı denetlenecek kayıt "
              "bulamadı" % kind)
        print("     (bu bir GEÇİŞ DEĞİL, BOŞ KOŞUDUR; Faz 2'de kayıt gelir)")
        return None

    missing = [p["puzzleId"] for p in need if p["puzzleId"] not in sols]
    rep.check(not missing,
              "yazılmış her bulmacanın korumalı kaydı var"
              + ("" if not missing else " — ⛔ KAYIP: %s" % missing[:5]))
    return need, sols, designs


# ── metin yardımcıları ─────────────────────────────────────────────────
_WORD = re.compile(r"[^\w\s]", re.UNICODE)

# ⚠ FAZ 2 BULGUSU — TÜRKÇE PİLOT BU KAPIYI KIRDI (K20'nin bedeli).
#
# NFKD çoğu Türkçe harfi çözer: ç→c+çengel, ş→s+çengel, ğ→g+kısa, ö→o+iki
# nokta, ü→u+iki nokta. Ama NOKTASIZ 'ı' (U+0131) ve NOKTALI 'İ' (U+0130)
# ayrışmaz — 'ı' bir taban harftir, aksanlı bir 'i' değildir.
#
# Sonucu şudur: "IŞIK" normalize edilince "isik", "ışık" ise "ışık" olur.
# Yani aynı sözcüğün büyük ve küçük yazımı FARKLI iki dize sayılır — ve
# ipucu sızıntısı denetimi ile kanarya, cevabı 'ışık' diye yazan bir
# sızıntıyı KAÇIRIRDI.
#
# Bu, talimat § 17'nin uyardığı şeyin canlı örneğidir: bir dil değişimi
# ÖLÇÜM MAKİNESİNİ de değiştirir. Katlama küçültmeden ÖNCE uygulanır.
_TR_FOLD = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ﬁ": "fi"})


def norm(text: str) -> str:
    """Karşılaştırma için normalize: küçük harf, aksansız, noktalamasız,
    tek boşluklu. İpucu sızıntısı denetimi bunun üzerinden yürür —
    'THE RAVEN' ile 'the raven!' aynı dizedir.

    ⭑ Türkçe katlaması ı/İ/I → i. Gerekçe yukarıdadır ve bir kaçırılmış
    sızıntıdır, bir üslup tercihi değil."""
    t = (text or "").translate(_TR_FOLD)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = _WORD.sub(" ", t.lower())
    return " ".join(t.split())


def squeeze(text: str) -> str:
    """Boşluksuz normalize — 'THERAVEN' biçimindeki gizlemeyi yakalar."""
    return norm(text).replace(" ", "")


def words(text: str) -> list[str]:
    return norm(text).split()


def content_words(text: str, minlen: int = 4) -> set[str]:
    return {w for w in words(text) if len(w) >= minlen}
