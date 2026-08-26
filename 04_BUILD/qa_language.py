#!/usr/bin/env python3
"""
DİL KAPISI — ticari yüzeyde Türkçe kalmadığını ÖLÇER
================================================================================
⚠ BU KAPI BİR KURUCU KARARINDAN DOĞDU (26 Ağustos 2026):

    "THE ENTIRE COMMERCIAL BOOK MUST BE ENGLISH."

Ve bir tuzağı vardır: **her Türkçe metin yanlış değildir.** Kurucuya
bakan belgeler (raporlar, el kitabı, üreteç yorumları) Türkçe kalır ve
kalmalıdır. Yanlış olan, ALICIYA ULAŞAN yüzeyde Türkçe olmasıdır.

⭑ TİCARİ YÜZEY ⭑ — burada Türkçe KIRMIZIDIR:
  · iç blok (paperback / hardcover PDF)
  · Kindle EPUB
  · kapak metni
  · ürün metadatası: başlık, alt başlık, açıklama, anahtar kelime
  · A+ başlık ve gövde metni

⭑ MUAF ⭑ — burada Türkçe DOĞRUDUR:
  · 06_REPORTS/ · 08_OUTPUT/KDP_UPLOAD_*  (kurucuya bakar)
  · 04_BUILD/ · 01_SOURCE/  (kod ve kaynak)
  · özel adlar (yazar ve yayıncı — metadata'dan okunur)

⚠ NASIL ÖLÇER: Türkçeye özgü harfler (ğ, ı, İ, ş, ö, ü, ç) ve yüksek
sıklıklı Türkçe işlev sözcükleri. Tek bir aksanlı harf yeterli değildir
— özel adlar onları taşır; kapı SÖZCÜK kanıtı arar.

Çıkış kodları:  0 = temiz   1 = ticari yüzeyde Türkçe var
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "08_OUTPUT")
META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "language.json")

# ⚠ ÖZEL ADLAR MUAFTIR: yazar ve yayıncı adı ticari yüzeyde BULUNMAK
# ZORUNDADIR; onları Türkçe kanıtı saymak, yazarın adını yasaklamak
# olurdu. Adlar buraya YAZILMAZ, metadata'dan okunur.
def proper_names() -> tuple:
    """⭑ ÖZEL ADLAR GÖMÜLMEZ, OKUNUR ⭑

    ⚠ Yazar ve yayıncı adını buraya yazmak, tek doğruluk kaynağını
    (project_config → metadata) ikiye böler; `validate_structure` bunu
    kapı olarak zorlar ve haklıdır. Adlar metadata'dan gelir, büyük/
    küçük ve soyad varyantları ondan TÜRETİLİR.
    """
    meta = pl.load_json(META) or {}
    out = set()
    for key in ("author", "publisher", "title"):
        v = (meta.get(key) or "").strip()
        if not v:
            continue
        out.update({v, v.upper()})
        out.update({w for w in v.split() if len(w) > 2})
        out.update({w.upper() for w in v.split() if len(w) > 2})
    return tuple(sorted(out, key=len, reverse=True))

# Türkçe işlev sözcükleri — İngilizce metinde bulunmaları olağandışıdır.
TR_WORDS = [
    "ve", "bir", "bu", "için", "ile", "olan", "var", "yok", "değil",
    "her", "gibi", "daha", "sonra", "önce", "kadar", "ama", "çünkü",
    "yalnızca", "sayfa", "bulmaca", "cevap", "ipucu", "levha", "kapı",
    "çözüm", "okur", "kitap", "sözcük", "harf", "sayı", "çizelge",
]
TR_WORD_RE = re.compile(r"(?<![\wçğıöşüÇĞİÖŞÜ])(%s)(?![\wçğıöşüÇĞİÖŞÜ])"
                        % "|".join(TR_WORDS), re.IGNORECASE)
TR_CHARS = re.compile(r"[ğışĞİŞ]")


def strip_proper(text: str) -> str:
    for p in proper_names():
        text = text.replace(p, " ")
    return text


def turkish_evidence(text: str, sample: int = 4) -> dict:
    """Kanıt: kaç Türkçe sözcük, hangi örnekler."""
    t = strip_proper(text)
    words = TR_WORD_RE.findall(t)
    chars = TR_CHARS.findall(t)
    ex = []
    for m in TR_WORD_RE.finditer(t):
        i = m.start()
        ex.append(re.sub(r"\s+", " ", t[max(0, i - 34):i + 40]).strip())
        if len(ex) >= sample:
            break
    return {"words": len(words), "chars": len(chars), "examples": ex}


def pdf_text(path: str) -> str:
    try:
        r = subprocess.run(["pdftotext", "-q", path, "-"],
                           capture_output=True, text=True, timeout=300)
        return r.stdout if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def epub_text(path: str) -> str:
    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile):
        return ""
    out = []
    for n in z.namelist():
        if n.endswith((".xhtml", ".html", ".opf")):
            out.append(re.sub(r"<[^>]+>", " ",
                              z.read(n).decode("utf-8", "ignore")))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=STATS)
    args = ap.parse_args()

    print("=" * 74)
    print("  DİL KAPISI · ticari yüzey İNGİLİZCE olmalı")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    meta = pl.load_json(META) or {}
    findings = {}

    # ── ① ÜRÜN METADATASI ──────────────────────────────────────────────
    print("\n── ürün metadatası ──")
    fields = {"title": meta.get("title"), "subtitle": meta.get("subtitle"),
              "description": meta.get("description")}
    for i, k in enumerate(meta.get("keywords") or []):
        fields["keyword%d" % (i + 1)] = k
    for i, b in enumerate(meta.get("bisac") or []):
        fields["bisac%d" % (i + 1)] = b.get("label")
    bad = {}
    for k, v in fields.items():
        if not v:
            continue
        ev = turkish_evidence(str(v))
        if ev["words"] or ev["chars"]:
            bad[k] = ev
    findings["metadata"] = bad
    rep.check(not bad, "⭑ ÜRÜN METADATASI İNGİLİZCE ⭑"
              + ("" if not bad else " — ⛔ %s" % sorted(bad)[:6]))
    rep.check((meta.get("language") or "") == "en",
              "metadata.language = en (%s)" % meta.get("language"))

    # ── ② A+ TİCARİ METNİ ──────────────────────────────────────────────
    print("\n── A+ metni ──")
    try:
        import prompt_catalog as CAT
        ap_bad = {}
        for pid, (t, b) in CAT.APLUS_COPY.items():
            ev = turkish_evidence(t + " " + b)
            if ev["words"] or ev["chars"]:
                ap_bad[pid] = ev
        findings["aplus"] = ap_bad
        rep.check(not ap_bad, "⭑ A+ METNİ İNGİLİZCE ⭑"
                  + ("" if not ap_bad else " — ⛔ %s" % sorted(ap_bad)))
    except ImportError:
        rep.warn("prompt_catalog okunamadı — A+ taraması atlandı")

    # ── ③ İÇ BLOKLAR VE KINDLE ─────────────────────────────────────────
    print("\n── ticari dosyalar ──")
    targets = [
        ("paperback iç blok", os.path.join(OUT, "PAPERBACK", "interior.pdf"),
         pdf_text),
        ("hardcover iç blok", os.path.join(OUT, "HARDCOVER", "interior.pdf"),
         pdf_text),
        ("paperback kapak", os.path.join(OUT, "PAPERBACK", "cover.pdf"),
         pdf_text),
        ("hardcover kapak", os.path.join(OUT, "HARDCOVER", "cover.pdf"),
         pdf_text),
        ("Kindle EPUB",
         os.path.join(OUT, "KINDLE", "codex-enigmatica.epub"), epub_text),
    ]
    for label, path, reader in targets:
        if not os.path.isfile(path):
            rep.warn("%s YOK — taranamadı" % label)
            continue
        text = reader(path)
        if not text.strip():
            rep.warn("%s metni çıkarılamadı" % label)
            continue
        ev = turkish_evidence(text)
        findings[label] = {"words": ev["words"], "chars": ev["chars"],
                           "examples": ev["examples"]}
        ok = ev["words"] == 0
        rep.check(ok, "⭑ %s İNGİLİZCE ⭑ (%d Türkçe sözcük)"
                  % (label.upper(), ev["words"]))
        if not ok and args.verbose:
            for e in ev["examples"]:
                print("        … %s …" % e[:96])

    # ── ÖZET ───────────────────────────────────────────────────────────
    tot = sum(v.get("words", 0) for v in findings.values()
              if isinstance(v, dict) and "words" in v)
    print("\n── özet ──")
    print("  %-30s %d" % ("ticari yüzeyde Türkçe sözcük", tot))
    if tot:
        print("\n  ⚠ Bu kapı KIRMIZI olmalıdır: kurucu kararı gereği ticari")
        print("    kitabın TAMAMI İngilizce olacak. Dönüşüm bir çeviri işi")
        print("    DEĞİLDİR — alfabe 29→26 harf değişir, bütün şifreli")
        print("    dizeler ve cevap atamaları YENİDEN ÜRETİLİR.")
        print("    Ayrıntı: 04_BUILD/english_readiness.py")

    rep.facts.update({"turkishWordsOnCommercialSurface": tot,
                      "findings": findings})
    return rep.finish("%d Türkçe sözcük" % tot, args.json)


if __name__ == "__main__":
    sys.exit(main())
