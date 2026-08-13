#!/usr/bin/env python3
"""
BAĞIMLILIK GRAFİĞİ (DAG) KAPISI — Codex Enigmatica
================================================================================
Bu kapı bulmacalar arası bağların bir AĞAÇ değil bir DAG olduğunu ve
okurun her zaman ileri gidebildiğini denetler.

NEDEN FAZ 1'DE: Kapı IV'te "bu bulmaca Kapı V'e bağlı" fark etmek, altmış
bulmacayı yeniden sıralamak demektir. Bağımlılık modeli en ucuz olduğu
anda — hiçbir bulmaca yazılmamışken — kurulur.

On kural:

  R1  döngü YOK
  R2  her bağımlılık hedefi VAR
  R3  kendine bağımlılık YOK
  R4  aynı kapı içinde YALNIZCA GERİYE bağ (ileri referans yok)
  R5  kapılar arası bağ yalnızca İKİ dar istisnayla
  R6  slotlanmış kapı bulmacası kendi kapısından besleniyor
  R7  meta BEŞ kapı bulmacasının hepsine bağlı
  R8  düşmüş (dropped) bulmacaya bağımlılık YOK
  R9  slot numaraları kapı içinde tekil ve kapı kapasitesi içinde
  R10 kapı seviyesi gerektiriyorsa kapı TAM SLOTLU

R5'in iki istisnası gate_index.json § dependencyRules'ta tanımlıdır:
  ① kapı devri — bir kapının 1. slotu bir ÖNCEKİ kapının kapı bulmacasına
  ② meta       — son soru beş kapı bulmacasına

Başka her kapılar arası bağ REDDEDİLİR. Gerekçe: okur kapıları sırayla
geçer; ileriye bakan bir bağ okuru çözemeyeceği bir şeye yollar.

TASARIM: yalnızca Python standart kütüphanesi (K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")

VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5",
               "release"]

# Hangi kapı seviyesinde hangi kapıların TAM SLOTLU olması beklenir (R10).
FULLY_SLOTTED_AT = {
    "phase2":  ["threshold"],
    "phase3":  ["threshold", "menagerie"],
    "phase4":  ["threshold", "menagerie", "calendar", "labyrinth", "mirror"],
    "phase5":  ["threshold", "menagerie", "calendar", "labyrinth", "mirror"],
    "release": ["threshold", "menagerie", "calendar", "labyrinth", "mirror"],
}


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


def load_json(path: str, rep: Report, required: bool = True):
    if not os.path.exists(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def find_cycles(edges: dict[str, list[str]]) -> list[list[str]]:
    """Tarjan yerine basit renkli DFS — envanter küçük, açıklık daha değerli.

    Bulunan döngü YOLUNU döndürür; yalnızca 'döngü var' demek düzeltmeyi
    zorlaştırır."""
    WHITE, GREY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in edges}
    cycles: list[list[str]] = []

    def walk(node: str, stack: list[str]) -> None:
        color[node] = GREY
        stack.append(node)
        for nxt in edges.get(node, []):
            if nxt not in color:
                continue                       # R2 ayrıca yakalar
            if color[nxt] == GREY:
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif color[nxt] == WHITE:
                walk(nxt, stack)
        stack.pop()
        color[node] = BLACK

    for n in sorted(edges):
        if color[n] == WHITE:
            walk(n, [])
    return cycles


def longest_chain(edges: dict[str, list[str]], nodes: list[str]) -> int:
    """En uzun bağımlılık zinciri. Okurun bir cevaba ulaşmak için kaç
    bulmaca çözmek zorunda olduğunu söyler."""
    depth: dict[str, int] = {}

    def d(n: str, seen: frozenset) -> int:
        if n in depth:
            return depth[n]
        if n in seen:                          # döngü — R1 zaten kırmızı
            return 0
        best = 0
        for nxt in edges.get(n, []):
            if nxt in edges:
                best = max(best, 1 + d(nxt, seen | {n}))
        depth[n] = best
        return best

    return max((d(n, frozenset()) for n in nodes), default=0)


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
    print("  BAĞIMLILIK GRAFİĞİ (DAG) · kapı: %s" % gate_level)
    print("=" * 74)

    rep = Report(args.verbose)
    load_json(CONFIG, rep)
    idx = load_json(PUZZLE_INDEX, rep, required=(gate_level != "phase0"))
    gidx = load_json(GATE_INDEX, rep, required=(gate_level != "phase0"))

    if idx is None or gidx is None:
        if gate_level == "phase0":
            print("\n  ⊘ envanter yok — phase0'da beklenen (Faz 1 üretir)")
            print("=" * 74)
            return 0
        print("\n⛔ envanter okunamadı")
        return 1

    puzzles = idx.get("puzzles", [])
    gates = {g["id"]: g for g in gidx.get("gates", [])}
    rules = gidx.get("dependencyRules", {})

    by_id = {p.get("puzzleId"): p for p in puzzles}
    edges = {pid: list(p.get("dependencies", []))
             for pid, p in by_id.items() if pid}

    rep.facts["nodes"] = len(edges)
    rep.facts["edges"] = sum(len(v) for v in edges.values())

    # ── R9 · slot tekilliği ve kapasitesi ───────────────────────────────
    print("\n── R9 · slot tekilliği ──")
    seen_slots: dict[tuple, list[str]] = {}
    over_capacity: list[str] = []
    for pid, p in by_id.items():
        if "slot" not in p:
            continue
        key = (p.get("gate"), p["slot"])
        seen_slots.setdefault(key, []).append(pid)
        cap = gates.get(p.get("gate"), {}).get("puzzles", 0)
        if p["slot"] > cap:
            over_capacity.append("%s (slot %d > kapasite %d)"
                                 % (pid, p["slot"], cap))
    dup_slots = ["%s slot %d → %s" % (g, s, v)
                 for (g, s), v in sorted(seen_slots.items()) if len(v) > 1]
    rep.check(not dup_slots, "slot numaraları kapı içinde tekil"
              + ("" if not dup_slots else " — ÇAKIŞMA: %s" % dup_slots[:5]))
    rep.check(not over_capacity, "slot numaraları kapı kapasitesi içinde"
              + ("" if not over_capacity else " — AŞIM: %s" % over_capacity[:5]))

    # ── R2 · hedef var mı · R3 · kendine bağ ────────────────────────────
    print("\n── R2/R3 · hedef bütünlüğü ──")
    missing: list[str] = []
    self_dep: list[str] = []
    for pid, deps in edges.items():
        for d in deps:
            if d == pid:
                self_dep.append(pid)
            elif d not in by_id:
                missing.append("%s → %s" % (pid, d))
    rep.check(not missing, "her bağımlılık hedefi envanterde var"
              + ("" if not missing else " — EKSİK: %s" % missing[:5]))
    rep.check(not self_dep, "kendine bağımlılık yok"
              + ("" if not self_dep else " — İHLAL: %s" % self_dep[:5]))

    # ── R8 · düşmüş bulmacaya bağ ───────────────────────────────────────
    print("\n── R8 · düşmüş bulmacaya bağımlılık ──")
    on_dropped = ["%s → %s" % (pid, d) for pid, deps in edges.items()
                  for d in deps
                  if d in by_id and by_id[d].get("status") == "dropped"]
    rep.check(not on_dropped, "düşmüş bulmacaya bağımlılık yok"
              + ("" if not on_dropped else " — İHLAL: %s" % on_dropped[:5]))

    # ── R1 · döngü ──────────────────────────────────────────────────────
    print("\n── R1 · ⭑ DÖNGÜ ⭑ ──")
    cycles = find_cycles(edges)
    rep.facts["cycles"] = len(cycles)
    rep.check(not cycles, "grafik DÖNGÜSÜZ"
              + ("" if not cycles else " — ⛔ DÖNGÜ: %s"
                 % [" → ".join(c) for c in cycles[:3]]))

    # ── R4/R5 · kapı içi geriye bağ ve kapılar arası istisnalar ─────────
    print("\n── R4/R5 · yön ve kapı sınırı ──")
    forward: list[str] = []
    unslotted_target: list[str] = []
    illegal_cross: list[str] = []

    gate_puzzle_ids = {
        g["id"]: pid for pid, p in by_id.items()
        for g in [gates.get(p.get("gate"), {})]
        if g and p.get("mechanismFamily") == "gate-synthesis"
        and p.get("slot") == g.get("gatePuzzleSlot")
    }
    rep.facts["gatePuzzles"] = gate_puzzle_ids

    for pid, deps in edges.items():
        src = by_id[pid]
        for d in deps:
            if d not in by_id:
                continue
            tgt = by_id[d]
            if src.get("gate") == tgt.get("gate"):
                if not rules.get("backwardSlotOnly", True):
                    continue
                if "slot" not in src:
                    continue          # slotlanmamış aday: sıra kuralı yok
                if "slot" not in tgt:
                    unslotted_target.append("%s → %s" % (pid, d))
                elif tgt["slot"] >= src["slot"]:
                    forward.append("%s(slot %s) → %s(slot %s)"
                                   % (pid, src["slot"], d, tgt["slot"]))
                continue

            # kapılar arası: yalnızca iki istisna
            ok = False
            if (rules.get("metaDependsOnAllGatePuzzles", True)
                    and src.get("type") == "meta"
                    and d in gate_puzzle_ids.values()):
                ok = True
            elif (rules.get("crossGateEntryHandoff", True)
                    and src.get("slot") == 1
                    and gates.get(src.get("gate"), {}).get("entryDependsOnGate")
                    == tgt.get("gate")
                    and d == gate_puzzle_ids.get(tgt.get("gate"))):
                ok = True
            if not ok:
                illegal_cross.append("%s(%s) → %s(%s)"
                                     % (pid, src.get("gate"), d, tgt.get("gate")))

    rep.check(not forward, "⭑ İLERİ REFERANS YOK ⭑"
              + ("" if not forward else " — ⛔ İHLAL: %s" % forward[:5]))
    rep.check(not unslotted_target,
              "slotlanmış bulmaca slotsuz bir bulmacaya bağlanmıyor"
              + ("" if not unslotted_target else " — İHLAL: %s"
                 % unslotted_target[:5]))
    rep.check(not illegal_cross, "kapılar arası bağ yalnızca tanımlı istisnalar"
              + ("" if not illegal_cross else " — ⛔ İHLAL: %s"
                 % illegal_cross[:5]))

    # ── R6 · kapı bulmacası kendi kapısından besleniyor ─────────────────
    print("\n── R6 · kapı bulmacasının girdisi ──")
    starved: list[str] = []
    for gid, pid in gate_puzzle_ids.items():
        slotted_peers = [q for q in by_id.values()
                         if q.get("gate") == gid and "slot" in q
                         and q["puzzleId"] != pid]
        if len(slotted_peers) < 1:
            rep.warn("kapı '%s' henüz slotlanmadı — R6 uykuda (Faz %s'te uyanır)"
                     % (gid, "2" if gid == "threshold" else "3/4"))
            continue
        own = [d for d in edges.get(pid, [])
               if d in by_id and by_id[d].get("gate") == gid]
        if not own:
            starved.append(pid)
    rep.check(not starved, "her slotlanmış kapı bulmacası kendi kapısından besleniyor"
              + ("" if not starved else " — AÇ: %s" % starved[:5]))

    # ── R7 · meta beş kapıya bağlı ──────────────────────────────────────
    print("\n── R7 · meta-mister bağlantısı ──")
    metas = [p for p in by_id.values() if p.get("type") == "meta"
             and p.get("status") != "dropped"]
    primary = [p for p in metas if p.get("dependencies")]
    if not primary:
        rep.warn("bağlanmış meta kaydı yok — Faz 4 teslimatı")
    else:
        need = set(gate_puzzle_ids.values())
        for m in primary:
            have = set(m.get("dependencies", []))
            rep.check(need.issubset(have),
                      "meta '%s' BEŞ kapı bulmacasına da bağlı" % m["puzzleId"]
                      + ("" if need.issubset(have)
                         else " — EKSİK: %s" % sorted(need - have)))

    # ── R10 · kapı seviyesi slot kapsamı ────────────────────────────────
    print("\n── R10 · kapı seviyesi slot kapsamı ──")
    required_gates = FULLY_SLOTTED_AT.get(gate_level, [])
    if not required_gates:
        print("  ⊘ bu kapı seviyesinde tam slot beklenmiyor")
    for gid in required_gates:
        want = gates.get(gid, {}).get("puzzles", 0)
        have = sorted(p["slot"] for p in by_id.values()
                      if p.get("gate") == gid and "slot" in p)
        rep.check(have == list(range(1, want + 1)),
                  "kapı '%s' tam slotlu (1–%d)" % (gid, want)
                  + ("" if have == list(range(1, want + 1))
                     else " — ölçülen %d slot" % len(have)))

    # ── türetilen: ardıllar ve zincir derinliği ─────────────────────────
    successors: dict[str, list[str]] = {pid: [] for pid in by_id}
    for pid, deps in edges.items():
        for d in deps:
            if d in successors:
                successors[d].append(pid)
    rep.facts["longestChain"] = longest_chain(edges, list(edges))
    rep.facts["maxFanIn"] = max((len(v) for v in edges.values()), default=0)
    rep.facts["maxFanOut"] = max((len(v) for v in successors.values()), default=0)
    rep.facts["slotted"] = sum(1 for p in by_id.values() if "slot" in p)
    rep.facts["withDependencies"] = sum(1 for v in edges.values() if v)

    print("\n── türetilen ölçümler ──")
    print("  düğüm %d · kenar %d · en uzun zincir %d"
          % (rep.facts["nodes"], rep.facts["edges"], rep.facts["longestChain"]))
    print("  en yüksek girdi sayısı %d · en yüksek ardıl sayısı %d"
          % (rep.facts["maxFanIn"], rep.facts["maxFanOut"]))

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · DAG döngüsüz" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate_level,
                       "checks": rep.checks, "errors": rep.errors,
                       "warnings": rep.warnings, "facts": rep.facts,
                       "successors": {k: v for k, v in successors.items() if v}},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
