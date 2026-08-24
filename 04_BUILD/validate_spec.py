#!/usr/bin/env python3
"""
VERİ BÜTÜNLÜĞÜ VE KAPSAM KAPISI — Codex Enigmatica
================================================================================
Bu kapı altı soruyu sorar:

  ① project_config.json kendi içinde tutarlı mı
  ② puzzle_index.json ŞEMAYA uyuyor mu, kimlikler tekil mi
  ③ .gate seviyesinin GEREKTİRDİĞİ kapsam sağlanmış mı
  ④ PUBLIC KATMANDA ÇÖZÜM VAR MI
  ⑤ ⭑ 'tested' DURUMU KAZANILMIŞ MI ⭑
  ⑥ gate_index ile config aynı kapıları mı tanıyor

────────────────────────────────────────────────────────────────────────
② NEDEN YENİDEN YAZILDI: `puzzle.schema.json` 355 satır boyunca üç
gizlilik sınıfı, `additionalProperties: false` ve alan tipleri tanımlıyordu
— ve HİÇBİR SATIR KOD ONU OKUMUYORDU. Şema yalnızca "var mı" diye
denetleniyordu. Yani şema bir doğrulayıcı adı taşıyan bir tasarım
belgesiydi. Artık uygulanıyor: `additionalProperties: false` bu depodaki
en güçlü tek gizlilik mekanizmasıdır, çünkü YASAK LİSTESİ DEĞİL İZİN
LİSTESİDİR — akla gelmemiş bir alan adı da reddedilir.

⑤ NEDEN VAROLUŞSAL: eskiden 140 kaydın `status` alanını elle "written"
yapmak, projeyi phase1'den release'e kadar yürütüyordu — `testStatus`
"untested", çözücü sayısı 0, alternatif analiz yapılmamışken. Faz 2'ye
"ÖLDÜRME KAPISI" deniyordu ama mekanik olarak bir metin alanıydı.
Artık 'tested' BEŞ ŞARTLA KAZANILIR ve iç çözücü kayıtları SAYILMAZ:
ajan çözümü zaten bilir, yargısı kanıt değildir.

Ayrıca en ucuz gerçek kilit burada: kurucu harici çözücüleri ONAYLAMADAN
hiçbir kayıt 'tested' olamaz. Sahte test kaydı üretme yolu böylece
kapanır — belgeyle değil, mekanizmayla.

TASARIM: yalnızca Python standart kütüphanesi (K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")
SCHEMA = os.path.join(ROOT, "01_SOURCE", "puzzle.schema.json")

VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5", "release"]
PRINT_BOUND = ("validated", "written")

# validate_structure.py § SOLUTION_FIELD_NAMES ile SENKRON olmak ZORUNDA.
# Bu liste İÇERİK taramasınındır: dar tutulur, çünkü bütün depoyu gezer.
SCAN_FIELD_NAMES = ["solution", "intendedSolution", "answer", "answerKey",
                    "solutionPath", "hints", "finalAnswer"]


# ── küçük şema uygulayıcısı ────────────────────────────────────────────
# JSON Schema'nın tamamı değil; bu şemanın KULLANDIĞI alt kümesi.
# Üçüncü taraf paket YOK (K7) — validate.yml saniyeler içinde biter.
def schema_errors(rec: dict, defn: dict, path: str = "") -> list[str]:
    out: list[str] = []
    props = defn.get("properties", {})

    for key in defn.get("required", []):
        if key not in rec:
            out.append("%s: zorunlu alan eksik '%s'" % (path, key))

    if defn.get("additionalProperties") is False:
        for key in rec:
            if key not in props:
                out.append("%s: TANIMSIZ ALAN '%s'" % (path, key))

    for key, val in rec.items():
        spec = props.get(key)
        if not spec:
            continue
        t = spec.get("type")
        if t == "string" and not isinstance(val, str):
            out.append("%s.%s: dize olmalı" % (path, key))
            continue
        if t == "integer" and not isinstance(val, int) or (
                t == "integer" and isinstance(val, bool)):
            out.append("%s.%s: tamsayı olmalı" % (path, key))
            continue
        if t == "boolean" and not isinstance(val, bool):
            out.append("%s.%s: mantıksal olmalı" % (path, key))
            continue
        if t == "array" and not isinstance(val, list):
            out.append("%s.%s: dizi olmalı" % (path, key))
            continue
        if "enum" in spec and val not in spec["enum"]:
            out.append("%s.%s: geçersiz değer '%s'" % (path, key, val))
        if "pattern" in spec and isinstance(val, str):
            if not re.match(spec["pattern"], val):
                out.append("%s.%s: kalıba uymuyor '%s'" % (path, key, val))
        if isinstance(val, int) and not isinstance(val, bool):
            if "minimum" in spec and val < spec["minimum"]:
                out.append("%s.%s: %s < %s" % (path, key, val, spec["minimum"]))
            if "maximum" in spec and val > spec["maximum"]:
                out.append("%s.%s: %s > %s" % (path, key, val, spec["maximum"]))
        if t == "array" and isinstance(val, list):
            it = spec.get("items", {})
            if it.get("type") == "string":
                for v in val:
                    if not isinstance(v, str):
                        out.append("%s.%s: dizi öğeleri dize olmalı" % (path, key))
                        break
    return out


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def ok(self, label: str) -> None:
        self.checks += 1
        if self.verbose:
            print("  ✓ %s" % label)

    def fail(self, label: str) -> None:
        self.checks += 1
        self.errors.append(label)
        print("  ✗ %s" % label)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)

    def check(self, cond: bool, label: str) -> bool:
        self.ok(label) if cond else self.fail(label)
        return cond


def load_json(path: str, rep: Report, required: bool = True):
    if not os.path.exists(path):
        if required:
            rep.fail("dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.fail("JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


# ---------------------------------------------------------------------------
def check_config(cfg: dict, rep: Report) -> None:
    print("\n── yapılandırma bütünlüğü ──")

    for key in ("project", "founder", "audience", "scope", "solvability",
                "killGate", "contentProtection", "production", "gates",
                "style", "taxonomy"):
        rep.check(key in cfg, "config bloğu var: %s" % key)

    scope = cfg.get("scope", {})
    gates_ = scope.get("gateStructure", [])
    rep.check(len(gates_) == scope.get("gates", -1),
              "kapı sayısı yapıyla uyuşuyor (%d)" % len(gates_))

    total = sum(g.get("puzzles", 0) for g in gates_)
    puzzles = scope.get("puzzles", 0)
    rep.check(total == puzzles,
              "kapı bulmaca toplamı (%d) hedefe (%d) EŞİT" % (total, puzzles))

    ids = [g.get("id") for g in gates_]
    rep.check(len(ids) == len(set(ids)), "kapı kimlikleri tekil")

    diffs = [g.get("difficulty", 0) for g in gates_]
    rep.check(all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1)),
              "zorluk eğrisi monoton artıyor %s" % diffs)

    # ÇÖZÜLEBİLİRLİK SÖZLEŞMESİ — gevşetilmesi yakalanmalı
    sol = cfg.get("solvability", {})
    rep.check(sol.get("deterministicSolutionRequired") is True,
              "deterministik çözüm şartı duruyor")
    rep.check(sol.get("uniqueSolutionRequired") is True,
              "tek çözüm şartı duruyor")
    rep.check(sol.get("alternativeSolutionAnalysisRequired") is True,
              "alternatif çözüm analizi şartı duruyor")
    rep.check(sol.get("hintMustNotContainAnswer") is True,
              "ipucu cevabı içeremez şartı duruyor")
    rep.check(sol.get("maxAcceptableAmbiguityScore", 99) <= 2,
              "belirsizlik eşiği ≤2")
    rep.check(sol.get("dependencyGraphMustBeAcyclic") is True,
              "DAG döngüsüzlük şartı duruyor")
    tsr = sol.get("testStatusRequirements", {})
    rep.check(bool(tsr), "test durumu şartları tanımlı")
    rep.check(tsr.get("internalSolverCountsAsEvidence") is False,
              "⭑ iç çözücü KANIT SAYILMIYOR ⭑")
    rep.check(tsr.get("minExternalSolversGateI", 0) >= 5,
              "Kapı I için ≥5 harici çözücü şartı duruyor")

    # ÖLDÜRME KAPISI — eşikler sayısal olmalı
    kg = cfg.get("killGate", {})
    rep.check(kg.get("phase") == "phase2", "öldürme kapısı Faz 2'de")
    pc_ = kg.get("passCriteria", {})
    hs = kg.get("hardStopCriteria", {})
    rep.check(pc_.get("solversCompletingGateI", 0) >= 4,
              "öldürme kapısı geçme eşiği ≥4/5 çözücü")
    rep.check(pc_.get("confirmedAlternativeSolutions", 99) == 0,
              "onaylanmış alternatif çözüm eşiği = 0")
    rep.check(hs.get("solversCompletingGateI", 99) <= 3,
              "sert durdurma eşiği ≤3/5 çözücü")
    # Kırmızı takım bulgusu: "hiç çözülemeyen bulmaca 0" ölçütü, 5 çözücüden
    # 1'inin çözdüğü bir bulmacayı GEÇİRİR. Okurların %80'inin takıldığı bir
    # bulmaca geçer bir bulmacadır. İkinci bir taban gerekir.
    rep.check(isinstance(pc_.get("minSolversPerPuzzle"), int)
              and pc_["minSolversPerPuzzle"] >= 2,
              "bulmaca başına en az çözücü tabanı tanımlı (≥2)")
    rep.check(pc_.get("medianDefinition") in ("dnf-counts-as-cap",),
              "medyan tanımı belirsizlik bırakmıyor (DNF tavan sayılır)")

    # GİZLİLİK SÖZLEŞMESİ — iki liste, iki iş
    cp = cfg.get("contentProtection", {})
    rep.check(set(cp.get("solutionFieldNames", [])) == set(SCAN_FIELD_NAMES),
              "çözüm alan adları config ile betik arasında SENKRON")
    fpf = set(cp.get("forbiddenPublicFields", []))
    rep.check(bool(fpf), "public katman yasak alan listesi tanımlı")
    rep.check(set(SCAN_FIELD_NAMES).issubset(fpf),
              "içerik taraması adları yasak public alanların ALT KÜMESİ")
    rep.check(len(cp.get("protectedDirs", [])) >= 4,
              "korumalı dizin listesi tanımlı")

    # Üretim ekonomisi: KDP formülünün kendisi burada doğrulanır.
    prod = cfg.get("production", {})
    pcst = prod.get("kdpPrintCost", {})
    pages = scope.get("pageTarget", 0)
    for ed in prod.get("editionsHypothesis", []):
        if not ed.get("enabled") or ed.get("list") is None:
            continue
        eid, lst = ed["id"], ed["list"]
        band = (pcst.get("paperbackRegularTrimBW", {}) if eid == "paperback"
                else pcst.get("hardcoverRegularTrimBW", {}) if eid == "hardcover"
                else None)
        if band is None:
            continue
        cost = band.get("fixed", 0) + pages * band.get("perPage", 0)
        rate = (pcst.get("royaltyRateAtOrAbove999", 0.6) if lst >= 9.99
                else pcst.get("royaltyRateBelow999", 0.5))
        royalty = lst * rate - cost
        rep.facts["royalty_%s" % eid] = round(royalty, 2)
        rep.facts["printcost_%s" % eid] = round(cost, 2)
        rep.check(royalty > 0,
                  "%s telifi pozitif: %.2f $ (baskı %.2f $ @ %d sayfa)"
                  % (eid, royalty, cost, pages))

    kindle = [e for e in prod.get("editionsHypothesis", [])
              if e.get("id") == "kindle"]
    rep.check(not kindle or not kindle[0].get("enabled"),
              "Kindle devre dışı (görsel şifre koruması)")

    fnd = cfg.get("founder", {})
    rep.check(fnd.get("isbn", {}).get("strategy") in ("kdp-free", "own"),
              "ISBN stratejisi geçerli")


def check_gate_index(cfg: dict, fams, rep: Report) -> set:
    print("\n── kapı dizini ──")
    conf_ids = {g["id"] for g in cfg["scope"]["gateStructure"]}
    if not fams:
        rep.warn("gate_index.json yok — config kapıları kullanılıyor")
        return conf_ids
    entries = fams.get("gates", []) if isinstance(fams, dict) else fams
    gate_ids = {g.get("id") for g in entries}
    missing = conf_ids - gate_ids
    rep.check(not missing, "config'in her kapısı gate_index'te var"
              + ("" if not missing else " — EKSİK: %s" % sorted(missing)))
    extra = [g for g in entries
             if g.get("id") not in conf_ids and not g.get("metaGate")]
    rep.check(not extra,
              "gate_index'teki fazla kayıtlar metaGate işaretli"
              + ("" if not extra else " — İŞARETSİZ: %s"
                 % [g.get("id") for g in extra]))
    for g in entries:
        if g.get("id") in conf_ids:
            cg = next(c for c in cfg["scope"]["gateStructure"]
                      if c["id"] == g["id"])
            rep.check(g.get("difficulty") == cg.get("difficulty")
                      and g.get("puzzles") == cg.get("puzzles"),
                      "kapı '%s' zorluk ve bulmaca sayısı SENKRON" % g["id"])
    return gate_ids


def check_games(cfg: dict, games, gate_ids: set, gate: str, rep: Report,
                schema: dict | None) -> list:
    print("\n── bulmaca envanteri (public katman) ──")

    if games is None:
        if gate == "phase0":
            rep.warn("puzzle_index.json yok — phase0'da beklenen (Faz 1 üretir)")
            rep.facts["games_total"] = 0
            return []
        rep.fail("puzzle_index.json yok ama kapı %s" % gate)
        return []

    entries = games.get("puzzles", []) if isinstance(games, dict) else games
    rep.facts["games_total"] = len(entries)

    ids = [p.get("puzzleId") for p in entries]
    rep.check(len(ids) == len(set(ids)), "bulmaca kimlikleri tekil (%d)" % len(ids))
    rep.check(all(ids), "her bulmacanın puzzleId'si var")

    # ② ⭑ ŞEMA GERÇEKTEN UYGULANIYOR ⭑
    if schema:
        defn = schema.get("$defs", {}).get("publicPuzzle")
        if defn:
            errs: list[str] = []
            for p in entries:
                errs += schema_errors(p, defn, p.get("puzzleId", "?"))
            rep.check(not errs,
                      "⭑ her kayıt publicPuzzle ŞEMASINA uyuyor "
                      "(izin listesi: tanımsız alan REDDEDİLİR) ⭑"
                      + ("" if not errs else " — %d ihlal: %s"
                         % (len(errs), errs[:5])))
        else:
            rep.fail("puzzle.schema.json § $defs.publicPuzzle bulunamadı")
    else:
        rep.fail("puzzle.schema.json okunamadı — şema uygulanamıyor")

    bad_gate = [p["puzzleId"] for p in entries if p.get("gate") not in gate_ids]
    rep.check(not bad_gate,
              "her bulmaca tanımlı bir kapıya ait"
              + ("" if not bad_gate else " — ihlal: %s" % bad_gate[:5]))

    # ④ ⭑ PUBLIC KATMANDA ÇÖZÜM OLAMAZ ⭑ — config'ten sürülen GENİŞ liste.
    # Şema izin listesi bunu zaten kapsar; bu ikinci hat, şema bozulursa
    # veya bir alan yanlışlıkla şemaya eklenirse devreye girer.
    forbidden = cfg["contentProtection"]["forbiddenPublicFields"]

    def deep_scan(obj, prefix: str) -> list[str]:
        hits = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in forbidden:
                    hits.append("%s.%s" % (prefix, k))
                hits += deep_scan(v, "%s.%s" % (prefix, k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                hits += deep_scan(v, "%s[%d]" % (prefix, i))
        return hits

    leaked = []
    for p in entries:
        leaked += deep_scan(p, p.get("puzzleId", "?"))
    rep.check(not leaked,
              "⭑ PUBLIC KATMANDA ÇÖZÜM YOK (iç içe alanlar dâhil) ⭑"
              + ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))

    # Belirsizlik: eşik AŞIMI ve ALANIN YOKLUĞU ayrı iki kusurdur.
    # Eskiden alan yoksa denetim sessizce atlanıyordu — yani kapıyı kapatmanın
    # yolu alanı SİLMEKTİ.
    maxamb = cfg["solvability"]["maxAcceptableAmbiguityScore"]
    over, absent = [], []
    for p in entries:
        if p.get("status") not in PRINT_BOUND:
            continue
        v = p.get("ambiguityScore")
        if not isinstance(v, int):
            absent.append(p["puzzleId"])
        elif v > maxamb:
            over.append(p["puzzleId"])
    rep.check(not absent,
              "yazılmış/doğrulanmış her bulmacada belirsizlik puanı VAR"
              + ("" if not absent else " — EKSİK: %s" % absent[:5]))
    rep.check(not over,
              "doğrulanmış bulmacalarda belirsizlik ≤ %d" % maxamb
              + ("" if not over else " — AŞAN: %s" % over[:5]))

    for st in ("candidate", "drafted", "validated", "written", "dropped"):
        rep.facts["games_%s" % st] = sum(1 for p in entries
                                         if p.get("status") == st)
    rep.facts["gates_used"] = len({p.get("gate") for p in entries})
    rep.facts["pilotCohort"] = sum(1 for p in entries if p.get("pilotCohort"))
    return entries


def check_test_status(cfg: dict, entries: list, gate_ids: set, rep: Report) -> None:
    """⑤ ⭑ 'tested' KAZANILIR, ELLE VERİLMEZ. ⭑"""
    print("\n── ⭑ TEST DURUMU ⭑ ──")
    if not entries:
        print("  ⊘ envanter boş")
        return

    sol = cfg.get("solvability", {})
    tsr = sol.get("testStatusRequirements", {})
    kg = cfg.get("killGate", {}).get("passCriteria", {})
    fnd = cfg.get("founder", {})

    # En ucuz gerçek kilit: harici çözücü onaylanmadan hiçbir şey 'tested'
    # olamaz. Sahte test kaydı üretme yolu burada kapanır.
    confirmed = fnd.get("externalSolvers", {}).get("founderConfirmed") is True
    tested = [p["puzzleId"] for p in entries if p.get("testStatus") == "tested"]
    if not confirmed:
        rep.check(not tested,
                  "harici çözücü ONAYLANMADAN hiçbir kayıt 'tested' olamaz"
                  + ("" if not tested else " — ⛔ SAHTE: %s" % tested[:5]))

    # status ↔ testStatus BAĞI: 'validated'/'written' testsiz verilemez.
    unbound = [p["puzzleId"] for p in entries
               if p.get("status") in PRINT_BOUND
               and p.get("testStatus") != "tested"]
    rep.check(not unbound,
              "⭑ 'validated'/'written' yalnızca 'tested' kayıtlarda ⭑"
              + ("" if not unbound else " — ⛔ TESTSİZ YAZILMIŞ: %s" % unbound[:5]))

    # 'internal-only' ne dediğini demelidir.
    lying = [p["puzzleId"] for p in entries
             if p.get("testStatus") == "internal-only"
             and p.get("solverTestCount", 0) > 0]
    rep.check(not lying,
              "'internal-only' kayıtlarda harici çözücü sayısı 0"
              + ("" if not lying else " — ÇELİŞKİ: %s" % lying[:5]))

    # Sayaç akıl sağlığı: çözen sayısı, deneyen sayısını aşamaz; ve
    # toplanan çözücü havuzundan fazla test olamaz (uydurma göstergesi).
    pool = cfg.get("killGate", {}).get("solversRequired", 5) * 2
    insane = [p["puzzleId"] for p in entries
              if p.get("solverSolvedCount", 0) > p.get("solverTestCount", 0)
              or p.get("solverTestCount", 0) > pool]
    rep.check(not insane,
              "çözücü sayaçları tutarlı (çözen ≤ deneyen ≤ havuz %d)" % pool
              + ("" if not insane else " — ⛔ UYDURMA: %s" % insane[:5]))

    # Beş şart — yalnızca 'tested' iddiasındaki kayıtlara.
    first_gate = None
    for g in cfg["scope"]["gateStructure"]:
        first_gate = g["id"]
        break
    failures: list[str] = []
    for p in entries:
        if p.get("testStatus") != "tested":
            continue
        pid = p["puzzleId"]
        need = (tsr.get("minExternalSolversGateI", 5)
                if p.get("gate") == first_gate
                else tsr.get("minExternalSolversDefault", 2))
        if p.get("solverTestCount", 0) < need:
            failures.append("%s: harici çözücü %d < %d"
                            % (pid, p.get("solverTestCount", 0), need))
        min_solved = (kg.get("solversCompletingGateI", 4)
                      if p.get("gate") == first_gate
                      else max(1, int(need * tsr.get("minSolvedRatio", 0.5))))
        if p.get("solverSolvedCount", 0) < min_solved:
            failures.append("%s: çözen %d < %d"
                            % (pid, p.get("solverSolvedCount", 0), min_solved))
        if tsr.get("requireAlternativeAnalysis") and \
                p.get("alternativeSolutionAnalysisDone") is not True:
            failures.append("%s: alternatif çözüm analizi yapılmamış" % pid)
        if p.get("confirmedAlternativeSolutions", 0) > \
                tsr.get("maxConfirmedAlternatives", 0):
            failures.append("%s: onaylanmış alternatif çözüm var" % pid)
        amb = p.get("ambiguityScore")
        if not isinstance(amb, int) or amb > tsr.get("maxAmbiguityScore", 2):
            failures.append("%s: belirsizlik puanı %s" % (pid, amb))

    rep.check(not failures,
              "⭑ 'tested' iddiası BEŞ ŞARTI da sağlıyor ⭑"
              + ("" if not failures else " — ⛔ KAZANILMAMIŞ: %s" % failures[:6]))
    rep.facts["tested"] = len(tested)


def check_gate_scope(cfg: dict, gate: str, rep: Report) -> None:
    """⭑ KAPI SEVİYESİ KAPSAM — ve KURUCU GEÇERSİZ KILMASININ SINIRI ⭑

    Geçersiz kılma YALNIZCA HARİCİ DOĞRULAMA eksiğini karşılar.
    YAZILMAMIŞ İŞİ KARŞILAMAZ ve bu ayrım burada mekaniktir:

      · `puzzlesDrafted` eşiği HER KOŞULDA aranır — geçersiz kılma bunu
        gevşetmez. Yirmi bulmaca yazılmadıysa hiçbir kurucu kararı onları
        yazılmış yapmaz.
      · `puzzlesValidated` / `puzzlesWritten` eşikleri harici insan
        kanıtına dayanır ve kanıt YOKTUR. Geçersiz kılma yalnızca BU
        ikisini "kurucu kararıyla karşılandı" sayar — ve raporda ölçülen
        sayı ile eşiği YAN YANA yazar.

    ⚠ Hiçbir bulmaca 'tested' olmaz. Durum alanları dokunulmaz kalır."""
    print("\n── kapı seviyesi kapsam denetimi (%s) ──" % gate)

    req = cfg.get("gates", {}).get("requirements", {}).get(gate)
    if req is None:
        rep.fail("kapı seviyesi config'de tanımsız: %s" % gate)
        return

    ov = (cfg.get("killGate") or {}).get("externalValidation") or {}
    override = bool(ov.get("founderOverride")) and not ov.get(
        "humanValidationPassed")

    total = rep.facts.get("games_total", 0)
    # 'written' bir bulmaca zaten 'tested' olmak zorundadır (check_test_status),
    # yani doğrulanmışlığı kapsar. Sayımın toplam olması bu yüzden geçerlidir.
    validated = (rep.facts.get("games_validated", 0)
                 + rep.facts.get("games_written", 0))
    written = rep.facts.get("games_written", 0)
    drafted = (rep.facts.get("games_drafted", 0) + validated)

    rep.check(total >= req["puzzlesCandidate"],
              "aday bulmaca ≥ %d (ölçülen %d)" % (req["puzzlesCandidate"], total))

    if override:
        # ⭑ İŞ eşiği geçersiz kılınamaz ⭑
        rep.check(drafted >= req["puzzlesWritten"],
                  "⭑ YAZILMIŞ (drafted) BULMACA ≥ %d — GEÇERSİZ KILINAMAZ ⭑ "
                  "(ölçülen %d)" % (req["puzzlesWritten"], drafted))
        gap_v = max(0, req["puzzlesValidated"] - validated)
        gap_w = max(0, req["puzzlesWritten"] - written)
        if gap_v or gap_w:
            print("  ⚑ KURUCU GEÇERSİZ KILMASI — doğrulama eşiği karşılanmadı")
            print("     doğrulanmış  %d / %d   (eksik %d)"
                  % (validated, req["puzzlesValidated"], gap_v))
            print("     yazılmış     %d / %d   (eksik %d)"
                  % (written, req["puzzlesWritten"], gap_w))
            print("     ⚠ External human validation remains pending.")
            rep.warn("kapı %s doğrulama eşiği KURUCU KARARIYLA geçildi — "
                     "ölçülen doğrulama %d/%d, yazılmış %d/%d"
                     % (gate, validated, req["puzzlesValidated"],
                        written, req["puzzlesWritten"]))
        rep.facts["gateScopeOverride"] = True
        rep.facts["validatedGap"] = gap_v
        rep.facts["writtenGap"] = gap_w
    else:
        rep.check(validated >= req["puzzlesValidated"],
                  "doğrulanmış bulmaca ≥ %d (ölçülen %d)"
                  % (req["puzzlesValidated"], validated))
        rep.check(written >= req["puzzlesWritten"],
                  "yazılmış bulmaca ≥ %d (ölçülen %d)"
                  % (req["puzzlesWritten"], written))

    if cfg["scope"].get("locked") and gate in ("phase4", "phase5", "release"):
        rep.check(total >= cfg["scope"]["puzzles"], "kilitli kapsam sağlanıyor")


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None, help="kapı seviyesi (yoksa .gate okunur)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None, help="rapor çıktısı")
    args = ap.parse_args()

    gate = args.gate or read_gate()
    if gate not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  VERİ BÜTÜNLÜĞÜ VE KAPSAM · kapı: %s" % gate)
    print("=" * 74)

    rep = Report(args.verbose)

    cfg = load_json(CONFIG, rep)
    if cfg is None:
        print("\n⛔ project_config.json okunamadı — başka hiçbir şey denetlenemez")
        return 1

    check_config(cfg, rep)
    fams = load_json(GATE_INDEX, rep, required=(gate != "phase0"))
    schema = load_json(SCHEMA, rep, required=(gate != "phase0"))
    gate_ids = check_gate_index(cfg, fams, rep)
    games = load_json(PUZZLE_INDEX, rep, required=(gate != "phase0"))
    entries = check_games(cfg, games, gate_ids, gate, rep, schema)
    check_test_status(cfg, entries, gate_ids, rep)
    check_gate_scope(cfg, gate, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kapı: %s" % (rep.checks, gate))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
