#!/usr/bin/env python3
"""
⭑ PAKETTEN ÇÖZME ⭑ — cevap anahtarına BAKMADAN, yalnızca okurun gördüğüyle
================================================================================
⚠ BU BİR İNSAN TESTİ DEĞİLDİR VE ONUN YERİNE GEÇMEZ.

Bir makine, bir bulmacanın *eğlenceli* olup olmadığını söyleyemez ve bu
betik öyle bir iddiada bulunmaz. Söyleyebileceği tek şey vardır ve o da
ucuz değildir:

    ⭑ CEVAP, OKURUN ELİNE GEÇEN ŞEYDEN TÜRETİLEBİLİYOR MU? ⭑

`qa_readerpack` şunu sorar: gerekli veri sayfada VAR MI? Bu betik daha
sertini sorar: o veriden cevap GERÇEKTEN ÇIKIYOR MU — ve çıkan şey
cevap anahtarındakiyle aynı mı?

Fark, Faz 2'nin on bulmacasında ölçülmüştü: levha METNİ vardı, levha
VERİSİ yoktu ve sekiz kapı bunu görmedi.

────────────────────────────────────────────────────────────────────────
KURALLAR — ve bu betik onları mekanik olarak uygular:

  ① `01_SOURCE/solutions/` HİÇ AÇILMAZ (karşılaştırma anına kadar).
     Çözüm dosyası yalnızca EN SONDA, sağlama için okunur.
  ② Girdi yalnızca `02_MANUSCRIPT/book.json`tur: sayfa metni, şekil,
     basılı çizelge ve ön maddedeki araçlar levhası.
  ③ Türetilemeyen bulmaca 'kapsam dışı' sayılır — 'geçti' SAYILMAZ.
     ⚠ Bir çözücü olarak beceriksizliğim, bulmacanın kusuru değildir;
       ama kusursuzluğunun kanıtı da değildir.
────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "04_BUILD"))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
STATION = re.compile(r"(\d)·(\d)")
MARKS = "',+/\\x"


def norm(s):
    return pl.squeeze(s or "")


def solve_page(page: dict, charts: dict) -> tuple[str, str]:
    """(türetilen cevap, hangi yoldan) — yalnızca sayfadan."""
    fig = page.get("figure") or ""
    tbl = page.get("printedTable") or ""
    alpha = charts.get("esik-alfabesi", {}).get("alphabet", "")
    lex = [e["word"] for e in charts.get("esik-sozlugu", {}).get("entries", [])]
    best = [e["word"] for e in
            charts.get("yaratiklar-katalogu", {}).get("entries", [])]
    words = lex + best

    # ① IZGARA KOORDİNATI — istasyonları oku, Çizelge F'de ara
    grid = charts.get("halka-tablosu", {}).get("rows")
    if grid and STATION.search(fig):
        # ⚠ HALKADA SATIR SIRASI METİN SIRASI DEĞİLDİR: üst sıra soldan
        # sağa, ALT SIRA SAĞDAN SOLA okunur ve levha onu zaten ters
        # basmıştır. Metni olduğu gibi okuyan bir çözücü halkayı yanlış
        # sırada alır — ilk koşuda tam olarak bu oldu.
        lines = [l for l in fig.splitlines() if STATION.search(l)]
        if len(lines) >= 2:
            pairs = [(int(a), int(b)) for a, b in STATION.findall(lines[0])]
            for l in lines[1:]:
                pairs += list(reversed(
                    [(int(a), int(b)) for a, b in STATION.findall(l)]))
        else:
            pairs = [(int(a), int(b)) for a, b in STATION.findall(fig)]
        cand = []
        n = len(pairs)
        orders = [pairs, list(reversed(pairs))] if "▶" in fig else \
            [p[r:] + p[:r] for p in (pairs, list(reversed(pairs)))
             for r in range(n)]
        for o in orders:
            out = ""
            for r, c in o:
                if not (1 <= r <= len(grid) and 1 <= c <= len(grid[r - 1])):
                    out = ""
                    break
                ch = grid[r - 1][c - 1]
                if ch == "·":
                    out = ""
                    break
                out += ch
            if out in words:
                cand.append(out)
        uniq = sorted(set(cand))
        if len(uniq) == 1:
            return uniq[0], "ızgara koordinatı"
        if uniq:
            return "?ÇOKLU:%s" % ",".join(uniq), "ızgara koordinatı"

    # ② GLİF — işaret gruplarını Çizelge A ile çöz
    # ⚠ İŞARETLER ARALIKLI BASILIR ("' ' '"), bitişik değil. Bitişiklik
    # arayan bir dedektör hiçbir glif levhasını görmez.
    glyph_lines = [l for l in fig.splitlines()
                   if l.count("│") >= 1
                   and sum(l.count(m) for m in MARKS) >= 2]
    if alpha and glyph_lines:
        body = glyph_lines[0]
        for junk in ("║", "╒", "╘", "▶", "◀", "▲", "│  ", "  │"):
            pass
        body = body.strip().lstrip("║│╒╘ ").rstrip("║│╒╘ ")
        for arrow in ("▶", "◀", "▲", "▼"):
            body = body.replace(arrow, "")
        groups = [g for g in re.split(r"[│|]", body) if g.strip()
                  and all(c in MARKS + " " for c in g.strip())]
        out = ""
        for g in groups:
            t = "".join(g.split())
            if not t or len(set(t)) != 1 or t[0] not in MARKS:
                out = ""
                break
            i = MARKS.index(t[0]) * 5 + len(t) - 1
            if i >= len(alpha):
                out = ""
                break
            out += alpha[i]
        for w in (out, out[::-1]):
            if w in words:
                return w, "glif okuma"

    # ③ ANAHTARLI SATIR — iki hizalı satır + dize
    if alpha and "anahtar" in fig and "dize" in fig:
        rows = [l for l in fig.splitlines() if l.strip()]
        try:
            keyed = "".join(rows[1].split()[1:])
            ct = "".join(rows[-1].split()[1:])
            if len(keyed) == len(alpha):
                out = "".join(alpha[keyed.index(c)] for c in ct
                              if c in keyed)
                if out in words:
                    return out, "anahtarlı satır"
        except (IndexError, ValueError):
            pass

    # ④ AĞIL — basılı nitelik çizelgesinden KURALI BUL, sonra aykırıyı
    # ⭑ Bu dal en sert olanıdır: kural sayfada YAZILI DEĞİLDİR. Betik onu
    # basılı sütunlardan çıkarır — okurun yapması beklenen şeyin aynısı.
    if tbl and "bölme" in tbl:
        rows = [[c.strip() for c in l.split("|") if c.strip()]
                for l in tbl.splitlines() if l.strip().startswith("|")]
        if len(rows) >= 3:
            head, body = rows[0], [r for r in rows[2:] if len(r) == len(rows[0])]
            try:
                i_name, i_pen = head.index("yaratık"), head.index("bölme")
            except ValueError:
                body = []
            rules = [h for h in head if h not in ("yaratık", "bölme", "no")]
            hits = []
            for rule in rules:
                j = head.index(rule)
                wrong = [r[i_name] for r in body
                         if (r[j] == "var") != (r[i_pen] == "A")]
                if len(wrong) == 1:
                    hits.append(wrong[0])
            if len(set(hits)) == 1 and hits[0] in words:
                return hits[0], "ağıl · kural türetildi"

    # ⑤ BASILI ÇİZELGE — tek satır bırakan süzgeç yoksa aday kümesi
    if tbl:
        cells = [c.strip() for row in tbl.splitlines()
                 for c in row.split("|") if c.strip()]
        hits = [c for c in cells if c in words]
        if len(set(hits)) == 1:
            return hits[0], "basılı çizelge (tek aday)"
    return "", "türetilemedi"


def main() -> int:
    # ⚠ CI'IN NORMAL DURUMU: manuscript korumalı katmandadır ve klonda
    # HİÇ YOKTUR. Betik BOŞ KOŞAR ve bunu SÖYLER — sessizce yeşil yanmaz
    # ve çökmez. (Faz 2'nin `preflight` dersi; bu betik onu yeni öğrendi.)
    if not os.path.exists(BOOK):
        print("=" * 74)
        print("  ⭑ PAKETTEN ÇÖZME ⭑")
        print("=" * 74)
        print("  ⊘ 02_MANUSCRIPT/book.json bu ortamda YOK (.gitignore) —")
        print("     BOŞ KOŞTU. Bu bir GEÇİŞ DEĞİLDİR.")
        print("     Ölçüm YERELDE yapılır.")
        print("=" * 74)
        return 0
    book = json.load(open(BOOK, encoding="utf-8"))
    charts = book.get("toolsPlate") or {}
    pages = book.get("puzzles") or []

    derived, skipped = {}, []
    for p in pages:
        got, how = solve_page(p, charts)
        if got and not got.startswith("?"):
            derived[p["puzzleId"]] = (got, how)
        else:
            skipped.append((p["puzzleId"], how if not got else got))

    # ⑤ ⭑ SAĞLAMA — çözüm dosyası ANCAK BURADA açılır ⭑
    key = {}
    for g in ("gate-1", "gate-2"):
        f = os.path.join(ROOT, "01_SOURCE", "solutions", "%s.json" % g)
        if os.path.exists(f):
            for r in json.load(open(f, encoding="utf-8"))["puzzles"]:
                key[r["puzzleId"]] = r["finalAnswer"]

    print("=" * 74)
    print("  ⭑ PAKETTEN ÇÖZME ⭑ — cevap anahtarına bakmadan")
    print("=" * 74)
    ok, bad = [], []
    for pid, (got, how) in sorted(derived.items()):
        want = key.get(pid, "")
        (ok if norm(got) == norm(want) else bad).append((pid, got, want, how))
    print("\n── türetilen ──")
    for pid, got, want, how in ok:
        print("  ✓ %-9s %-22s %s" % (pid, how, "anahtarla UYUŞUYOR"))
    for pid, got, want, how in bad:
        print("  ✗ %-9s %-22s ⛔ TÜRETİLEN ≠ ANAHTAR" % (pid, how))
    print("\n── türetilemedi (kapsam dışı, GEÇTİ SAYILMAZ) ──")
    for pid, why in skipped:
        print("  ⊘ %-9s %s" % (pid, why))
    print("\n" + "=" * 74)
    print("  türetilen %d / %d · uyuşan %d · uyuşmayan %d · kapsam dışı %d"
          % (len(derived), len(pages), len(ok), len(bad), len(skipped)))
    print("  ⚠ Bu bir İNSAN TESTİ DEĞİLDİR. Ölçtüğü tek şey: cevap okurun")
    print("    eline geçen şeyden TÜRETİLEBİLİYOR mu.")
    print("=" * 74)
    out = os.path.join(ROOT, "06_REPORTS", "tracked", "solve-from-pack.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"pages": len(pages), "derived": len(derived),
                   "matched": len(ok), "mismatched": len(bad),
                   "outOfScope": [s[0] for s in skipped],
                   "note": "makine yeniden kurulumu · insan testi DEĞİL"},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
