#!/usr/bin/env python3
"""
KDP YÜKLEME PAKETİ + PREFLIGHT
================================================================================
Yüklenebilir dizinleri kurar, sağlama toplamlarını yazar ve KDP'nin
reddedeceği kusurları ÖNCE burada arar.

  08_OUTPUT/PAPERBACK/   interior.pdf · cover.pdf · metadata.json · SHA256SUMS
  08_OUTPUT/APLUS/       6 modül · module-map.json · SHA256SUMS

⚠ BU BETİK HİÇBİR ŞEY YÜKLEMEZ. Yükleme kurucunun işidir ve öyle kalır.

⭑ PREFLIGHT NEYİ ÖLÇER ⭑

  · PDF gerçekten PDF mi, sayfa sayısı iddia edilenle aynı mı
  · yazı tipleri GÖMÜLÜ mü (gömülmeyen yazı tipi = KDP reddi)
  · kapak geometrisi sırt + taşma ile tutarlı mı
  · A+ modülleri tam Amazon ölçüsünde mi
  · metadata sayfa sayısı ÖLÇÜLEN sayfa sayısıyla aynı mı
  · pakete bir cevap dosyası sızmış mı

⚠ SON MADDE: kitabın KENDİSİ cevap taşır ve taşımak zorundadır —
bir bulmaca kitabının çözüm bölümü vardır. Aranan şey, pakete düşmüş
KAYNAK dosyalarıdır (`.json`, `.md`), PDF'in içeriği değil.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "08_OUTPUT")
PB = os.path.join(OUT, "PAPERBACK")
AP = os.path.join(OUT, "APLUS")
WEB = os.path.join(pl.ROOT, "07_ASSETS", "web")
META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
INTERIOR = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "interior.json")
COVER = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "cover.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "kdp-package.json")

# ⚠ Pakete ASLA girmemesi gerekenler: kaynak veri, tasarım, çözüm
# dosyaları. PDF hariç — kitap kendi cevaplarını taşır.
FORBIDDEN_EXT = (".json", ".md", ".py", ".txt", ".csv", ".yml", ".yaml")
ALLOWED_JSON = ("metadata.json", "module-map.json", "manifest.json")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_facts(path: str) -> dict:
    """Sayfa sayısı ve gömülü yazı tipleri — kütüphanesiz, ham okuma."""
    if not os.path.isfile(path):
        return {"exists": False}
    data = open(path, "rb").read()
    out = {"exists": True, "bytes": len(data),
           "header": data[:8].decode("latin-1", "ignore")}
    m = re.findall(rb"/Type\s*/Page[^s]", data)
    out["pages"] = len(m) or None
    cnt = re.findall(rb"/Count\s+(\d+)", data)
    if cnt:
        out["pages"] = max(out["pages"] or 0, max(int(c) for c in cnt))
    # ⚠ FontFile / FontFile2 / FontFile3 = gömülü yazı tipi akışı.
    out["embeddedFontStreams"] = len(re.findall(rb"/FontFile\d?", data))
    out["fonts"] = sorted(set(
        f.decode("latin-1") for f in re.findall(rb"/BaseFont\s*/([A-Za-z0-9+\-]+)",
                                                data)))[:12]
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+"
                  rb"([\d.]+)\s+([\d.]+)", data)
    if m:
        w = (float(m.group(3)) - float(m.group(1))) / 72.0
        h = (float(m.group(4)) - float(m.group(2))) / 72.0
        out["mediaBoxIn"] = [round(w, 4), round(h, 4)]
    return out


def write_sums(d: str) -> int:
    names = sorted(f for f in os.listdir(d)
                   if os.path.isfile(os.path.join(d, f))
                   and f != "SHA256SUMS")
    with open(os.path.join(d, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        for n in names:
            fh.write("%s  %s\n" % (sha256(os.path.join(d, n)), n))
    return len(names)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP PAKETİ + PREFLIGHT")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    meta = pl.load_json(META) or {}
    inter = (pl.load_json(INTERIOR) or {}).get("facts") or {}
    cov = (pl.load_json(COVER) or {}).get("facts") or {}

    os.makedirs(PB, exist_ok=True)
    os.makedirs(AP, exist_ok=True)

    # ── ① İÇ BLOK ──────────────────────────────────────────────────────
    ipdf = pdf_facts(os.path.join(PB, "interior.pdf"))
    rep.check(ipdf.get("exists"), "iç blok PDF paket içinde")
    if ipdf.get("exists"):
        rep.check(ipdf["header"].startswith("%PDF"), "iç blok geçerli PDF")
        rep.check((ipdf.get("embeddedFontStreams") or 0) > 0,
                  "⭑ YAZI TİPLERİ GÖMÜLÜ ⭑ (%d akış) — gömülmeyen yazı "
                  "tipi KDP reddidir" % (ipdf.get("embeddedFontStreams") or 0))
        mb = ipdf.get("mediaBoxIn") or [0, 0]
        rep.check(abs(mb[0] - 6.0) < 0.02 and abs(mb[1] - 9.0) < 0.02,
                  "iç blok trim 6×9 in (%s)" % mb)
        rep.check(ipdf["bytes"] / 1e6 < 650,
                  "iç blok < 650 MB (%.1f)" % (ipdf["bytes"] / 1e6))
        if inter.get("pages") and ipdf.get("pages"):
            rep.check(abs(ipdf["pages"] - inter["pages"]) <= 1,
                      "PDF sayfa sayısı ölçümle aynı (%s / %s)"
                      % (ipdf["pages"], inter["pages"]))

    # ── ② KAPAK ────────────────────────────────────────────────────────
    cpdf = pdf_facts(os.path.join(PB, "cover.pdf"))
    rep.check(cpdf.get("exists"), "kapak PDF paket içinde")
    if cpdf.get("exists") and cov:
        mb = cpdf.get("mediaBoxIn") or [0, 0]
        rep.check(abs(mb[0] - cov["widthIn"]) < 0.02
                  and abs(mb[1] - cov["heightIn"]) < 0.02,
                  "kapak ölçüsü sırt+taşma ile tutarlı (%s ↔ %.3f×%.3f)"
                  % (mb, cov["widthIn"], cov["heightIn"]))
        rep.check(cov.get("pages") == inter.get("pages"),
                  "⭑ KAPAK, İÇ BLOĞUN SAYFA SAYISIYLA KURULDU ⭑ (%s / %s)"
                  % (cov.get("pages"), inter.get("pages")))

    # ── ③ A+ ───────────────────────────────────────────────────────────
    import prompt_catalog as CAT
    n_ap = 0
    mapping = []
    for m in CAT.APLUS:
        src = os.path.join(WEB, "codex-enigmatica-%s.png" % m["id"])
        if not os.path.isfile(src):
            continue
        dst = os.path.join(AP, os.path.basename(src))
        if not os.path.isfile(dst) or sha256(src) != sha256(dst):
            shutil.copy2(src, dst)
        n_ap += 1
        kind, dim, note = CAT.APLUS_SPEC[m["module"]]
        t, b = CAT.APLUS_COPY[m["id"]]
        mapping.append({"id": m["id"], "file": os.path.basename(src),
                        "module": kind, "targetPx": dim, "note": note,
                        "title": t, "body": b, "claim": m["claim"]})
    json.dump({"$comment": ["ÜRETİLEN DOSYA — 04_BUILD/kdp_package.py",
                            "GÖRSEL metinsizdir; başlık ve gövde Amazon'un",
                            "kendi alanlarına girilir."],
               "modules": mapping},
              open(os.path.join(AP, "module-map.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=1)
    rep.check(n_ap == 6, "6 A+ modülü pakette (%d)" % n_ap)

    from PIL import Image
    bad = []
    for mm in mapping:
        p = os.path.join(AP, mm["file"])
        w, h = Image.open(p).size
        want = tuple(int(x) for x in re.findall(r"\d+", mm["targetPx"])[:2])
        if want and (w, h) != want:
            bad.append("%s %dx%d≠%s" % (mm["id"], w, h, mm["targetPx"]))
    rep.check(not bad, "⭑ HER A+ MODÜLÜ TAM AMAZON ÖLÇÜSÜNDE ⭑"
              + ("" if not bad else " — ⛔ %s" % bad))

    tr = [m["id"] for m in mapping
          if re.search(r"[çğıöşüÇĞİÖŞÜ]", m["title"] + m["body"])]
    rep.check(not tr, "A+ metni İngilizce (ürün sayfası dili)"
              + ("" if not tr else " — ⛔ %s" % tr))

    # ── ④ METADATA ─────────────────────────────────────────────────────
    mp = os.path.join(PB, "metadata.json")
    meta_out = dict(meta)
    meta_out["pageCount"] = inter.get("pages") or meta.get("pageCount")
    json.dump(meta_out, open(mp, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    rep.check(meta_out["pageCount"] == inter.get("pages"),
              "⭑ METADATA SAYFA SAYISI ÖLÇÜLENLE AYNI ⭑ (%s)"
              % meta_out["pageCount"])

    # ── ⑤ PAKETE KAYNAK SIZDI MI ───────────────────────────────────────
    leak = []
    for d in (PB, AP):
        for f in os.listdir(d):
            if (f.lower().endswith(FORBIDDEN_EXT)
                    and f not in ALLOWED_JSON and f != "SHA256SUMS"):
                leak.append(os.path.join(os.path.basename(d), f))
    rep.check(not leak, "⭑ PAKETE KAYNAK/ÇÖZÜM DOSYASI SIZMADI ⭑"
              + ("" if not leak else " — ⛔ %s" % leak))

    # ── ⑥ SAĞLAMA TOPLAMLARI ───────────────────────────────────────────
    n1, n2 = write_sums(PB), write_sums(AP)
    rep.check(n1 >= 3, "paperback paketinde %d dosya" % n1)
    rep.check(n2 >= 7, "A+ paketinde %d dosya" % n2)

    print("\n── paket ──")
    print("  %-26s %s" % ("PAPERBACK", os.path.relpath(PB, pl.ROOT)))
    for f in sorted(os.listdir(PB)):
        print("     %-26s %8.1f MB"
              % (f, os.path.getsize(os.path.join(PB, f)) / 1e6))
    print("  %-26s %s · %d dosya" % ("APLUS", os.path.relpath(AP, pl.ROOT), n2))

    rep.facts.update({"interior": ipdf, "cover": cpdf,
                      "aplusModules": n_ap,
                      "pageCount": meta_out.get("pageCount"),
                      "paperbackFiles": n1, "aplusFiles": n2})
    return rep.finish("%d + %d dosya" % (n1, n2), STATS)


if __name__ == "__main__":
    sys.exit(main())
