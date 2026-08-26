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

    Dönüş None ise çağıran hemen bitirmelidir.

    ⚠ FAZ 2 BULGUSU — İKİ FARKLI 'KAYIT YOK' DURUMU VARDIR VE KARIŞTIRMAK
    YA CI'I YALANCI KIRMIZI YAKAR YA DA GERÇEK BİR KUSURU GİZLER:

      ① KATMAN TAMAMEN YOK   → CI'ın NORMAL durumu. Korumalı katman
         .gitignore ile dışlanır; klonda hiç yoktur. Kapı BOŞ KOŞAR ve
         bunu SÖYLER. Körlüğü selftest kapatır (fikstürler gerçek
         kayıtlarla koşar).
      ② KATMAN VAR AMA EKSİK → GERÇEK KUSUR. Yazarın bir bulmacayı
         yazıp çözümünü yazmayı unutmasıdır. KIRMIZI.

    Faz 1'de bu ayrım GEREKMİYORDU çünkü hiçbir bulmaca 'drafted'
    değildi; ① durumu ② ile aynı koda düşüyordu ve kimse fark etmedi.
    İlk yirmi bulmaca yazıldığında CI kırmızı yandı — kapı, kendisine
    hiç gösterilmemiş bir dosyayı 'kayıp' sanıyordu."""
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

    if not sols and not designs:
        # ① Katman TAMAMEN yok — CI. Boş koşar ve bunu YÜKSEK SESLE söyler.
        rep.facts["protectedLayerPresent"] = False
        print("  ⊘ korumalı katman bu ortamda HİÇ YOK (.gitignore § ①b) —")
        print("     %s kapısı BOŞ KOŞTU. Bu bir GEÇİŞ DEĞİLDİR." % kind)
        print("     Ölçüm YERELDE yapılır; körlüğü 05_TESTS/selftest.py kapatır.")
        rep.warn("%s: korumalı katman yok, kapı boş koştu (CI'ın normal "
                 "durumu — yerelde koşturun)" % kind)
        return None

    # ② Katman VAR ama eksik → gerçek kusur.
    rep.facts["protectedLayerPresent"] = True
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


# ═══════════════════════════════════════════════════════════════════════
#  TYPESETTING HELPERS — SHARED BY THE PRINT AND THE KINDLE BUILDERS
# ═══════════════════════════════════════════════════════════════════════
# ⚠ THEY LIVE HERE BECAUSE THEY DRIFTED. `interior.py` and `kindle.py`
# each carried their own copy of `flow()`, each rendered the tools plate
# their own way, and each independently printed the front matter as raw
# Python: a list of hard-wrapped lines set as one paragraph per line, the
# contract's (promise, explanation) pairs shown as tuples with their
# brackets, and — in both — the chart marked `printed: false`, which is the
# domain of the last question's uniqueness proof and CONTAINS ITS ANSWER.
#
# Two builders, one book. What the reader sees has one implementation.

def paragraphs(val) -> list[str]:
    """Front/back matter → paragraphs. NOT one paragraph per line.

    The narrative blocks are written as hard-wrapped lines. Lines join into
    a paragraph; a blank line ends it; a line beginning with whitespace is a
    laid-out line (a hint-ladder rung, a signature) and stands on its own.
    """
    if val is None:
        return []
    if isinstance(val, str):
        return [x.strip() for x in val.split("\n\n") if x.strip()]
    if isinstance(val, dict):
        out = []
        for v in val.values():
            out += paragraphs(v)
        return out
    if not isinstance(val, (list, tuple)):
        return [str(val)]
    out, buf = [], []
    for raw in val:
        if isinstance(raw, (list, tuple)):
            # ⭑ A TWO-PART ENTRY IS A DEFINITION, NOT TWO PARAGRAPHS ⭑
            # ⚠ The cipher reference is written as (TERM, explanation) pairs
            # and the print builder set each pair down with `str()`: eleven
            # Python tuples, brackets and quotes included, on the reference
            # page of a book whose fourth promise is that its own charts are
            # the authority. The pair is rendered as one definition line and
            # the term is emphasised — which both builders can typeset.
            if buf:
                out.append(" ".join(buf))
                buf = []
            parts = [str(x).strip() for x in raw if str(x).strip()]
            if len(parts) == 2:
                out.append("**%s** — %s" % (parts[0], parts[1]))
            else:
                out += parts
            continue
        ln = str(raw)
        if not ln.strip():
            if buf:
                out.append(" ".join(buf))
                buf = []
        elif ln[:1].isspace():
            if buf:
                out.append(" ".join(buf))
                buf = []
            out.append(ln.strip())
        else:
            buf.append(ln.strip())
    if buf:
        out.append(" ".join(buf))
    return out


def emphasis(escaped: str) -> str:
    """`**bold**` and `*italic*` → tags. Applied AFTER escaping.

    ⚠ The source marks emphasis the way the rest of this project writes it,
    and both targets accept the same two tags — reportlab's Paragraph and
    XHTML. Before this existed the book printed the asterisks: seventeen
    worked examples showed their answer wrapped in stars."""
    import re as _re
    t = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    return _re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", t)


def chart_is_printed(ch) -> bool:
    """⭑ A CHART MARKED `printed: false` IS NOT PRINTED ⭑

    The last question's candidate list is a chart like any other so that
    the uniqueness proof has a domain to count — and it contains the final
    answer. The contract's own words are "printed nowhere in this book"."""
    return isinstance(ch, dict) and bool(ch.get("printed", True))


def chart_body(ch: dict) -> str:
    """A printed chart, laid out by the SHAPE of its entries, not its name.

    ⚠ Before this, both builders dumped the chart's raw dictionary: `id`,
    `title`, `note` and the entry list ran together as one line of Python
    repr on the page. A chart is the book's fourth promise made visible; it
    cannot be printed as a debug dump."""
    if ch.get("rows"):                            # a coordinate grid
        rows = ch["rows"]
        out = ["     " + " ".join("%3d" % (c + 1) for c in range(len(rows[0]))),
               ""]
        for r, row in enumerate(rows, 1):
            out.append("%3d  " % r + " ".join("%3s" % c for c in row))
        return "\n".join(out)
    entries = ch.get("entries") or ch.get("table") or []
    if not entries:
        return ""
    first = entries[0]
    if isinstance(first, str):                    # a list of sayings
        return "\n".join("%3d  %s" % (i, x) for i, x in enumerate(entries, 1))
    if isinstance(first, dict) and "letter" in first:
        out = []
        for i in range(0, len(entries), 2):
            out.append("   ".join(
                "%s  %-14s gp %d" % (x["letter"], x.get("glyph", ""),
                                     x.get("group", 0))
                for x in entries[i:i + 2]))
        return "\n".join(out)
    if isinstance(first, dict) and "word" in first:
        cols = 3
        rows_n = (len(entries) + cols - 1) // cols
        out = []
        for r in range(rows_n):
            cells = []
            for c in range(cols):
                k = r + c * rows_n
                if k < len(entries):
                    cells.append("%3d %-12s" % (entries[k].get("no", k + 1),
                                                entries[k]["word"]))
            out.append("  ".join(cells).rstrip())
        return "\n".join(out)
    if isinstance(first, dict) and "symbol" in first:
        return "\n".join("  %s   = %d" % (x["symbol"], x["value"])
                         for x in entries)
    keys = list(first.keys())
    out = ["  ".join("%-8s" % k for k in keys),
           "  ".join("-" * 8 for _ in keys)]
    for x in entries:
        out.append("  ".join("%-8s" % x.get(k, "") for k in keys))
    return "\n".join(out)


GATE_ROMAN = {"threshold": "I", "menagerie": "II", "calendar": "III",
              "labyrinth": "IV", "mirror": "V"}
GATE_NAME = {"threshold": "The Threshold", "menagerie": "The Menagerie",
             "calendar": "The Calendar", "labyrinth": "The Labyrinth",
             "mirror": "The Mirror", "last-question": "The Last Question"}


def gate_heading(gid: str, index: int) -> str:
    """⚠ THE SIXTH "GATE" IS NOT A GATE. The last question carries its own
    gate id, so a loop numbering the gates asked for a sixth Roman numeral
    — and in the print builder it fell over on that line."""
    if gid == "last-question":
        return "The Last Question"
    return "Gate %s — %s" % (GATE_ROMAN.get(gid, str(index + 1)),
                             GATE_NAME.get(gid, gid.title()))


def drop_heading(rows, head: str) -> list:
    """⭑ THE SAME HEADING TWICE IS A TYPESETTING ERROR, NOT A STYLE ⭑

    ⚠ Several back-matter blocks open with their own heading line — the
    source is written to be readable on its own. The builders print a
    heading too, so the book showed "SOURCES SOURCES", "HINTS HINTS" and
    "CIPHERS AND NOTATIONS" twice over, on four separate pages."""
    out = list(rows)
    if out and norm(out[0]) == norm(head):
        out = out[1:]
    return out
