#!/usr/bin/env python3
"""
KURUCU GÖRSEL ENVANTERİ — teslim edilen ham varlıklar ölçülür
================================================================================
⚠ BU BETİK BİR GÖRSELİ "GÜZEL" BULMAZ. Ölçer.

Kurucu `07_ASSETS/raw/` altına görselleri koyar. Bu betik onları prompt
sözleşmesiyle karşılaştırır ve her biri için ÜÇ ayrı sayı üretir:

  GERÇEK PİKSEL      dosyada kaç piksel var
  METADATA DPI       dosyanın kendi hakkında ne İDDİA ettiği
  ⭑ ETKİN DPI ⭑      gerçek piksel ÷ basılacağı fiziksel ölçü

⚠ ÜÇÜ AYNI ŞEY DEĞİLDİR ve bu ayrım bu betiğin varlık sebebidir.
Bir dosyanın pHYs etiketine "300 dpi" yazmak onu 300 dpi YAPMAZ; piksel
sayısı değişmediği sürece baskıda hiçbir şey düzelmez. Metadata etiketi
bir iddiadır, etkin DPI bir ölçümdür. (ASSET_UPSCALING_REPORT.md § 3.1)

FİZİKSEL HEDEFLER — nereden geldikleri:

  GRAVÜR   4,5 × 7,5 inç   6×9 trim eksi 0,75 kenar boşluğu
                           (plate_proof.py · TRIM_W_IN/MARGIN_IN)
  KAPAK    6 × 9 inç       prompt_catalog.COVER_TRIM
  A+       piksel hedefi   ekran varlığı — DPI'ı yoktur, ölçüsü vardır
                           (prompt_catalog.APLUS_SPEC)

Çıkış kodları:  0 = bütün denetimler yeşil   1 = kırmızı denetim var
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
import prompt_catalog as CAT                                   # noqa: E402

RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
LIB = os.path.join(pl.ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")
OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "asset-inventory.json")

# ── FİZİKSEL HEDEFLER ─────────────────────────────────────────────────────
# ⚠ plate_proof.py ile AYNI sayılar. Orada 6×9 trim ve 0,75 inç kenar
# boşluğu tanımlı; levha o kutunun İÇİNE sığar. Bir levhanın tam sayfa
# genişliğini kapladığını varsaymak EN KÖTÜ DURUMDUR ve ölçüm en kötü
# durumdan yapılır — iyimser varsayım baskıda okunmayan levha demektir.
TRIM_W_IN, TRIM_H_IN = 6.0, 9.0
MARGIN_IN = 0.75
BOX_W_IN = TRIM_W_IN - 2 * MARGIN_IN                              # 4,5
BOX_H_IN = TRIM_H_IN - 2 * MARGIN_IN                              # 7,5

COVER_W_IN, COVER_H_IN = 6.0, 9.0

# ⚠ KDP baskı için kabul edilen taban. 300 dpi endüstri standardıdır;
# KDP 300'ün altındaki kapakları uyarır. Gravür VERİ taşır — okunmayan
# bir gravür çözülemeyen bir bulmacadır, bu yüzden taviz yok.
DPI_TARGET = 300.0
DPI_FLOOR = 300.0

CLASSES = {
    "pl-": "GRAVÜR · bulmaca verisi",
    "dc-": "GRAVÜR · süs",
    "tl-": "GRAVÜR · araç",
    "codex-enigmatica-cover-": "KAPAK ÖN",
    "codex-enigmatica-aplus-": "A+",
}


def classify(name: str) -> str:
    """⭑ DOSYA ADINA DEĞİL, AD MİMARİSİNE GÜVENİLİR ⭑

    ⚠ Ön ek bu depoda bir GÜVENLİK sınıfıdır (VISUAL_ARCHITECTURE § 2),
    süs değil: `pl-` bulmaca verisi taşır ve asla cevap taşımaz. Sınıfı
    tahmin etmek, veri taşıyan bir levhayı süs sanmak demektir.
    """
    for pre, cls in CLASSES.items():
        if name.startswith(pre):
            return cls
    return "TANINMAYAN"


def measure(path: str) -> dict:
    """ImageMagick ile tek bir dosyayı ölçer."""
    fmt = "%w|%h|%m|%[colorspace]|%A|%x|%y|%[bit-depth]|%B"
    try:
        raw = subprocess.run(["identify", "-format", fmt, path + "[0]"],
                             capture_output=True, text=True, timeout=60)
        if raw.returncode != 0:
            return {"error": (raw.stderr or "identify başarısız").strip()[:200]}
        p = raw.stdout.strip().split("|")
        return {"w": int(p[0]), "h": int(p[1]), "format": p[2],
                "colorspace": p[3], "alpha": p[4] == "True",
                "dpiMeta": round(float(p[5].split()[0]), 1) if p[5] else None,
                "bitDepth": int(p[7]) if p[7].isdigit() else None,
                "bytes": int(p[8]) if p[8].isdigit() else None}
    except Exception as exc:                                   # noqa: BLE001
        return {"error": str(exc)[:200]}


def print_fit(w: int, h: int, box_w: float, box_h: float) -> tuple:
    """⭑ ETKİN DPI ⭑ — görsel kutuya en-boy korunarak sığdırılır.

    Sığdırma oranını hangi kenarın belirlediği önemlidir: geniş bir levha
    genişlikten, uzun bir levha yükseklikten sınırlanır. Yanlış kenardan
    ölçmek, olmayan bir çözünürlük bildirmektir.
    """
    if not w or not h:
        return (0.0, 0.0, 0.0)
    scale = min(box_w / w, box_h / h)          # inç/piksel
    phys_w, phys_h = w * scale, h * scale
    return (round(phys_w, 3), round(phys_h, 3), round(1.0 / scale, 1))


def expected_from_library() -> dict:
    """Beklenen HAM dosya adları KÜTÜPHANEDEN okunur.

    ⚠ Elle yazılmış bir liste değil: kütüphane üreteçten doğar, üreteç
    bulmacalardan doğar. Beklentiyi başka yerde tutmak, iki kaynağın
    sessizce ayrışması demektir.
    """
    doc = open(LIB, encoding="utf-8").read()
    return {n: True for n in
            re.findall(r"<code>07_ASSETS/raw/([a-z0-9-]+\.png)</code>", doc)}


def aplus_targets() -> dict:
    """A+ modül kimliği → (hedef genişlik, hedef yükseklik) piksel."""
    out = {}
    for item in CAT.APLUS:
        spec = CAT.APLUS_SPEC[item["module"]]
        m = re.findall(r"(\d+)\s*×\s*(\d+)", spec[1])
        if m:
            out[item["id"]] = (int(m[0][0]), int(m[0][1]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  KURUCU GÖRSEL ENVANTERİ")
    print("=" * 74)

    rep = pl.Report(args.verbose)

    if not os.path.isdir(RAW):
        rep.check(False, "⭑ 07_ASSETS/raw YOK ⭑")
        return rep.finish("dizin yok", args.json)

    files = sorted(f for f in os.listdir(RAW) if f.lower().endswith(".png"))
    expected = expected_from_library()
    ap_target = aplus_targets()

    if not files:
        print("\n  ⊘ 07_ASSETS/raw BOŞ — kurucu henüz görsel teslim etmedi")
        rep.warn("hiç görsel yok — envanter BOŞ KOŞTU")
        rep.facts.update({"delivered": 0, "expected": len(expected)})
        return rep.finish("görsel yok", args.json)

    rows = []
    for name in files:
        path = os.path.join(RAW, name)
        m = measure(path)
        cls = classify(name)
        row = {"file": name, "class": cls, "expected": name in expected}
        row.update(m)
        if "error" in m:
            rows.append(row)
            continue

        w, h = m["w"], m["h"]
        row["megapixel"] = round(w * h / 1e6, 2)
        row["aspect"] = round(w / h, 3) if h else 0

        if cls.startswith("GRAVÜR"):
            pw, ph, dpi = print_fit(w, h, BOX_W_IN, BOX_H_IN)
            row.update({"printW_in": pw, "printH_in": ph, "effectiveDpi": dpi,
                        "target": "%.2f × %.2f in kutusuna sığar"
                                  % (BOX_W_IN, BOX_H_IN)})
        elif cls == "KAPAK ÖN":
            pw, ph, dpi = print_fit(w, h, COVER_W_IN, COVER_H_IN)
            row.update({"printW_in": pw, "printH_in": ph, "effectiveDpi": dpi,
                        "target": "%.0f × %.0f in" % (COVER_W_IN, COVER_H_IN)})
        elif cls == "A+":
            pid = name[:-4].replace("codex-enigmatica-", "")
            tw, th = ap_target.get(pid, (0, 0))
            row.update({"targetPx": "%d × %d" % (tw, th) if tw else None,
                        "targetAspect": round(tw / th, 3) if th else None,
                        # ⚠ A+ EKRAN varlığıdır: DPI'ı yoktur. Ölçüsü vardır.
                        "effectiveDpi": None})
        rows.append(row)

    # ── DENETİMLER ────────────────────────────────────────────────────────
    delivered = {r["file"] for r in rows}
    missing = sorted(set(expected) - delivered)
    unknown = sorted(r["file"] for r in rows if r["class"] == "TANINMAYAN")
    broken = sorted(r["file"] for r in rows if "error" in r)

    rep.check(not broken, "her dosya okunabiliyor"
              + ("" if not broken else " — ⛔ %s" % broken[:5]))
    # ⚠ SARMAL KAPAKLAR HENÜZ İSTENDİ, HENÜZ TESLİM EDİLMEDİ — ve bu
    # oturumun DURMA KOŞULUDUR. Onları "eksik" saymak, kurucudan daha
    # yeni istenmiş bir şeyi gecikmiş göstermek olurdu. Ayrı sayılır.
    awaited = {w["file"] for w in CAT.WRAPS}
    pending = sorted(m for m in missing if m in awaited)
    overdue = sorted(m for m in missing if m not in awaited)

    rep.check(not overdue,
              "⭑ İSTENEN HER GÖRSEL TESLİM EDİLDİ ⭑ (%d/%d)"
              % (len(expected) - len(missing), len(expected) - len(pending))
              + ("" if not overdue else " — ⛔ EKSİK: %s" % overdue[:8]))
    if pending:
        rep.warn("⏳ KURUCU TESLİMATI BEKLENİYOR: %s — bu bir eksiklik "
                 "değil, sıradaki adımdır" % ", ".join(pending))
    rep.check(not unknown,
              "⭑ HİÇBİR DOSYA SINIFSIZ DEĞİL ⭑ (ad mimarisi = güvenlik "
              "sınıfı)" + ("" if not unknown else " — ⛔ %s" % unknown[:5]))

    good = [r for r in rows if "error" not in r]
    grav = [r for r in good if r["class"].startswith("GRAVÜR")]
    cov = [r for r in good if r["class"] == "KAPAK ÖN"]
    apl = [r for r in good if r["class"] == "A+"]

    rep.check(len(grav) == 103, "103 gravür teslim edildi (%d)" % len(grav))
    rep.check(len(cov) == 2, "2 ön kapak teslim edildi (%d)" % len(cov))
    rep.check(len(apl) == 6, "6 A+ modülü teslim edildi (%d)" % len(apl))

    fmt_bad = sorted(r["file"] for r in good if r["format"] != "PNG")
    rep.check(not fmt_bad, "her dosya PNG"
              + ("" if not fmt_bad else " — ⛔ %s" % fmt_bad[:5]))

    # ⚠ HAM DOSYANIN DÜŞÜK DPI'I BİR HATA DEĞİLDİR — yükseltmenin
    # SEBEBİDİR. Ham katmanda bu bir UYARIDIR ve bir iş listesidir.
    # Sert kapı İŞLENMİŞ çıktıya aittir: orada düşük DPI, baskıya
    # gitmiş okunmayan bir levha demektir.
    low = sorted((r["file"], r["effectiveDpi"]) for r in grav + cov
                 if (r.get("effectiveDpi") or 0) < DPI_FLOOR)
    if low:
        rep.warn("HAM katmanda %d dosya <%d dpi (en düşük %s @ %s) — "
                 "yükseltme GEREKLİ, `04_BUILD/asset_process.py`"
                 % (len(low), DPI_FLOOR, low[0][0], low[0][1]))
    else:
        rep.check(True, "ham dosyaların hepsi zaten ≥%d dpi" % DPI_FLOOR)

    # ── ⭑ İŞLENMİŞ ÇIKTI — SERT KAPI ⭑ ────────────────────────────────
    proc, proc_low = [], []
    for r in grav + cov:
        dst = (os.path.join(pl.ROOT, "07_ASSETS", "plates", r["file"])
               if r["class"].startswith("GRAVÜR") else
               os.path.join(pl.ROOT, "07_ASSETS", "print",
                            r["file"].replace("codex-enigmatica-", "")
                            .replace(".png", "-front.png")))
        if not os.path.exists(dst):
            continue
        m = measure(dst)
        if "error" in m:
            continue
        box = ((BOX_W_IN, BOX_H_IN) if r["class"].startswith("GRAVÜR")
               else (COVER_W_IN, COVER_H_IN))
        _, _, dpi = print_fit(m["w"], m["h"], *box)
        proc.append((r["file"], dpi))
        if dpi < DPI_FLOOR:
            proc_low.append((r["file"], dpi))

    if proc:
        rep.check(not proc_low,
                  "⭑ İŞLENMİŞ GÖRSELLERİN HEPSİ ETKİN ≥%d DPI ⭑ (%d/%d "
                  "işlendi · metadata etiketi DEĞİL, gerçek ölçüm)"
                  % (DPI_FLOOR, len(proc), len(grav) + len(cov))
                  + ("" if not proc_low else
                     " — ⛔ %s @ %s dpi" % proc_low[0]))
        if len(proc) < len(grav) + len(cov):
            rep.warn("işleme TAMAMLANMADI: %d/%d dosya hazır"
                     % (len(proc), len(grav) + len(cov)))
    else:
        rep.warn("hiçbir dosya işlenmemiş — `04_BUILD/asset_process.py` "
                 "koşturulmadı")

    # ⚠ A+ EN-BOY — Amazon modülü sabit orandadır. Oranı tutmayan bir
    # görsel ya gerilir (bozulur) ya kırpılır (kompozisyon kaybolur).
    ap_bad = []
    for r in apl:
        t = r.get("targetAspect")
        if t and abs(r["aspect"] - t) / t > 0.02:
            ap_bad.append((r["file"], r["aspect"], t))
    # ⚠ HAM katmanda oran sapması bir KARARDIR, hata değil: hat onu
    # merkezden kırpar. Ama kırpmak KOMPOZİSYON KAYBIDIR ve sessizce
    # yapılmamalıdır — kurucu neyin kesildiğini bilmeli, gerekirse
    # o modülü doğru oranda yeniden üretmelidir.
    if ap_bad:
        rep.warn("HAM katmanda %d A+ modülü modül oranında DEĞİL "
                 "(%s) — hat merkezden KIRPACAK; kırpma kompozisyon "
                 "kaybıdır, kurucu onayına tabidir"
                 % (len(ap_bad), ", ".join("%s %.2f≠%.2f" % b
                                           for b in ap_bad)))
    else:
        rep.check(True, "ham A+ modüllerinin hepsi zaten modül oranında")

    # ⭑ SERT KAPI: İŞLENMİŞ A+ TAM ÖLÇÜDE Mİ ⭑
    web_bad, web_seen = [], 0
    for r in apl:
        dst = os.path.join(pl.ROOT, "07_ASSETS", "web", r["file"])
        if not os.path.exists(dst):
            continue
        web_seen += 1
        m = measure(dst)
        want = r.get("targetPx")
        if "error" in m or not want:
            continue
        if "%d × %d" % (m["w"], m["h"]) != want:
            web_bad.append((r["file"], "%d×%d" % (m["w"], m["h"]), want))
    if web_seen:
        rep.check(not web_bad,
                  "⭑ İŞLENMİŞ A+ MODÜLLERİ TAM AMAZON ÖLÇÜSÜNDE ⭑ (%d/%d)"
                  % (web_seen, len(apl))
                  + ("" if not web_bad else " — ⛔ %s" % web_bad[:3]))

    # ── ÖZET ──────────────────────────────────────────────────────────────
    print("\n── teslim ──")
    print("  %-28s %3d" % ("toplam dosya", len(rows)))
    for label, grp in (("gravür", grav), ("ön kapak", cov), ("A+", apl)):
        print("  %-28s %3d" % (label, len(grp)))

    if grav:
        d = sorted(r["effectiveDpi"] for r in grav)
        print("\n── gravür ETKİN DPI (4,5 × 7,5 in kutusu) ──")
        print("  %-28s %.1f" % ("en düşük", d[0]))
        print("  %-28s %.1f" % ("ortanca", d[len(d) // 2]))
        print("  %-28s %.1f" % ("en yüksek", d[-1]))
        print("  %-28s %d / %d" % ("300 dpi ALTINDA",
                                   sum(1 for x in d if x < DPI_FLOOR), len(d)))
    if cov:
        print("\n── ön kapak ──")
        for r in cov:
            print("  %-34s %d×%d · etkin %.1f dpi"
                  % (r["file"][:34], r["w"], r["h"], r["effectiveDpi"]))
    if apl:
        print("\n── A+ ──")
        for r in apl:
            t = r.get("targetPx") or "?"
            flag = "" if not any(b[0] == r["file"] for b in ap_bad) else "  ⛔"
            print("  %-34s %d×%d (hedef %s)%s"
                  % (r["file"][:34], r["w"], r["h"], t, flag))

    meta_dpi = {r.get("dpiMeta") for r in good}
    print("\n── metadata DPI etiketi ──")
    print("  %s   ⚠ bu bir İDDİADIR, ölçüm değil" % sorted(
        x for x in meta_dpi if x is not None))

    rep.facts.update({
        "delivered": len(rows), "expected": len(expected),
        "gravure": len(grav), "cover": len(cov), "aplus": len(apl),
        "missing": missing, "unknown": unknown,
        "belowDpiFloor": [f for f, _ in low],
        "aplusAspectMismatch": [b[0] for b in ap_bad],
        "dpiFloor": DPI_FLOOR,
        "printBoxIn": [BOX_W_IN, BOX_H_IN],
        "assets": rows,
    })
    return rep.finish("%d varlık ölçüldü" % len(rows), args.json)


if __name__ == "__main__":
    sys.exit(main())
