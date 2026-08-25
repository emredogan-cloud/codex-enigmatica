#!/usr/bin/env python3
"""
GÖRSEL İŞLEME HATTI — ham teslimattan baskıya hazır dosyaya
================================================================================
ASSET_UPSCALING_REPORT.md § 3.2'deki yöntemi izler:

    ham PNG → [1] Real-ESRGAN 4× GERÇEK yükseltme → [2] 300 dpi etiketi

⚠ VE BİR ADIM EKLER — nedeni burada yazılıdır:

Belgelenmiş hat 4× yükseltip orada durur. Bu, KAPAK için doğrudur (6×9
inçlik tek bir görsel) ama 103 GRAVÜR için değildir: 1254 px'lik bir
levhanın 4×'i 5016 px'tir ve 4,5 inçlik bir baskı alanında bu **1114
dpi** eder. 1114 dpi'ın 600 dpi'a göre kâğıtta hiçbir karşılığı yoktur —
sadece 52 MB'lık bir dosya ve KDP'nin boğulacağı bir PDF üretir.

Bu yüzden hat şudur:

    [1] AI 4× yükselt        → GERÇEK piksel kazanılır (detay sentezlenir)
    [2] hedefe indir         → 4×'ten indirmek, doğrudan büyütmekten İYİDİR
    [3] alfa düzleştir       → baskıda saydamlık yoktur
    [4] DPI etiketi          → artık fiziksel olarak da doğru

⚠ [2] BİR TAVİZ DEĞİLDİR. Yükseltip indirmek (supersampling) doğrudan
yeniden boyutlandırmaktan daha temiz kenar verir; atılan şey çözünürlük
değil, kâğıda hiç ulaşmayacak sahte çözünürlüktür.

HEDEFLER
  GRAVÜR   4,5 × 7,5 in kutusuna 600 dpi    → çizgi sanatı standardı
  KAPAK    6 × 9 in · 300 dpi = 1800 × 2700
  A+       modülün tam piksel ölçüsü         → ekran varlığı

Çıkış kodları:  0 = tamam   1 = hata
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
import asset_ingest as ING                                     # noqa: E402

RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
PLATES = os.path.join(pl.ROOT, "07_ASSETS", "plates")
PRINT = os.path.join(pl.ROOT, "07_ASSETS", "print")
WEB = os.path.join(pl.ROOT, "07_ASSETS", "web")
LOG = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "asset-processing.json")

UPSCAYL = os.path.expanduser("~/Applications/upscayl-cli/upscayl-bin")
MODEL = "upscayl-standard-4x"                # ASSET_UPSCALING_REPORT § 3.3

GRAVURE_DPI = 600.0                          # çizgi sanatı
COVER_DPI = 300.0
BOX_W_IN, BOX_H_IN = ING.BOX_W_IN, ING.BOX_H_IN

# ⚠ Gravürlerin kâğıt zemini kremdir; alfa bu zemine düzleştirilir.
# Beyaza düzleştirmek levhanın kenarında görünmeyen bir halka bırakır.
FLATTEN_BG = (255, 255, 255)


def ai_upscale(src: str, dst: str) -> bool:
    """ASSET_UPSCALING_REPORT § 4.1 — birebir aynı komut."""
    r = subprocess.run([UPSCAYL, "-i", src, "-o", dst, "-n", MODEL,
                        "-s", "4", "-g", "0", "-f", "png"],
                       capture_output=True, text=True, timeout=900)
    return r.returncode == 0 and os.path.exists(dst)


def finish(src: str, dst: str, target: tuple, dpi: float,
           crop_aspect: float | None) -> dict:
    """Kırp (gerekirse) → hedefe indir → düzleştir → DPI etiketle."""
    from PIL import Image
    im = Image.open(src)
    before = im.size

    if crop_aspect:
        # ⚠ MERKEZDEN kırpılır: kompozisyonun ağırlık merkezi ortadadır.
        # Bu bir ONARIM DEĞİL, bir TAVİZDİR ve raporda öyle bildirilir.
        w, h = im.size
        if w / h > crop_aspect:
            nw, nh = int(round(h * crop_aspect)), h
        else:
            nw, nh = w, int(round(w / crop_aspect))
        im = im.crop(((w - nw) // 2, (h - nh) // 2,
                      (w - nw) // 2 + nw, (h - nh) // 2 + nh))

    if target[0] and target[1]:
        # ⚠ resize() İKİ elemanlı demet ister. Üç elemanlıyı vermek
        # ValueError atar ve bu sessizce SEKİZ ticari varlığı düşürdü —
        # gravürler (kutu dalı) geçtiği için hat çalışıyor GÖRÜNDÜ.
        im = im.resize((target[0], target[1]), Image.LANCZOS)
    else:
        im.thumbnail(target[2], Image.LANCZOS)      # kutuya sığdır

    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, FLATTEN_BG)
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "PNG", dpi=(dpi, dpi), optimize=True)
    return {"upscaled": before, "final": im.size}


def plan(name: str) -> dict | None:
    """Her dosya için hedefi belirler. Sınıf ad mimarisinden gelir."""
    cls = ING.classify(name)
    if cls.startswith("GRAVÜR"):
        box = (int(BOX_W_IN * GRAVURE_DPI), int(BOX_H_IN * GRAVURE_DPI))
        return {"class": cls, "dst": os.path.join(PLATES, name),
                "target": (None, None, box), "dpi": GRAVURE_DPI,
                "crop": None}
    if cls == "KAPAK ÖN":
        return {"class": cls,
                "dst": os.path.join(PRINT, name.replace(
                    "codex-enigmatica-", "").replace(".png", "-front.png")),
                "target": (1800, 2700, None), "dpi": COVER_DPI, "crop": None}
    if cls == "A+":
        pid = name[:-4].replace("codex-enigmatica-", "")
        tw, th = ING.aplus_targets().get(pid, (0, 0))
        if not tw:
            return None
        from PIL import Image
        w, h = Image.open(os.path.join(RAW, name)).size
        want = tw / th
        crop = want if abs((w / h) - want) / want > 0.02 else None
        return {"class": cls, "dst": os.path.join(WEB, name),
                "target": (tw, th, None), "dpi": 72.0, "crop": crop}
    return None


def write_index(failed: list | None = None) -> dict:
    """⭑ KAYIT, BİR KOŞUNUN GÜNLÜĞÜ DEĞİL, DİSKİN ÖLÇÜMÜDÜR ⭑

    ⚠ Bu fonksiyon bir hatadan doğdu: kayıt önce "bu koşuda ne yaptım"ı
    yazıyordu ve `--only` ile yapılan sekiz tekil koşu, 103 gravürlük
    koşunun kaydını sırayla EZDİ. Sonunda dosyada tek bir varlık kaldı,
    oysa diskte 111 tane vardı.

    Bir koşunun günlüğü kırılgandır: kısmi koşu, çökme, karışık çağrı
    onu yalancı yapar. Diskin ölçümü kırılgan değildir — ne varsa odur.
    """
    import asset_ingest as ING
    rows = []
    for sub, cls in (("plates", "GRAVÜR"), ("print", "KAPAK ÖN"),
                     ("web", "A+")):
        d = os.path.join(pl.ROOT, "07_ASSETS", sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(x for x in os.listdir(d) if x.endswith(".png")):
            m = ING.measure(os.path.join(d, f))
            if "error" in m:
                continue
            row = {"file": f, "class": cls,
                   "dst": "07_ASSETS/%s/%s" % (sub, f),
                   "final": [m["w"], m["h"]], "dpiMeta": m["dpiMeta"]}
            if cls != "A+":
                box = ((ING.BOX_W_IN, ING.BOX_H_IN) if cls == "GRAVÜR"
                       else (ING.COVER_W_IN, ING.COVER_H_IN))
                _, _, row["effectiveDpi"] = ING.print_fit(m["w"], m["h"], *box)
            rows.append(row)

    doc = {"$comment": ["ÜRETİLEN DOSYA — 04_BUILD/asset_process.py.",
                        "Bir koşunun günlüğü DEĞİL, 07_ASSETS altındaki",
                        "işlenmiş dosyaların ÖLÇÜMÜDÜR."],
           "model": MODEL, "gravureDpi": GRAVURE_DPI, "coverDpi": COVER_DPI,
           "processed": len(rows), "failed": failed or [], "assets": rows}
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    json.dump(doc, open(LOG, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return doc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="tek dosya adı (deneme için)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tmp", default="/tmp/enigmatica-upscale")
    ap.add_argument("--index", action="store_true",
                    help="yükseltme YAPMA, yalnızca diski ölçüp kaydı yaz")
    args = ap.parse_args()

    if args.index:
        d = write_index()
        print("\n  ✍ %s  (%d işlenmiş varlık ölçüldü)"
              % (os.path.relpath(LOG, pl.ROOT), d["processed"]))
        return 0

    if not os.path.exists(UPSCAYL):
        print("⛔ Upscayl CLI yok: %s" % UPSCAYL)
        print("   ASSET_UPSCALING_REPORT.md § 2.2 kurulum yerini söyler.")
        return 1

    os.makedirs(args.tmp, exist_ok=True)
    names = sorted(f for f in os.listdir(RAW) if f.endswith(".png"))
    if args.only:
        names = [n for n in names if n == args.only]
    if args.limit:
        names = names[:args.limit]

    print("=" * 74)
    print("  GÖRSEL İŞLEME · %d dosya · model %s" % (len(names), MODEL))
    print("=" * 74)

    done, failed, t0 = [], [], time.time()
    for i, name in enumerate(names, 1):
        p = plan(name)
        if not p:
            failed.append({"file": name, "why": "sınıf tanınmadı"})
            print("  [%3d/%d] ⛔ %-34s sınıf yok" % (i, len(names), name[:34]))
            continue
        src = os.path.join(RAW, name)
        tmp = os.path.join(args.tmp, "4x-" + name)
        try:
            if not ai_upscale(src, tmp):
                failed.append({"file": name, "why": "AI yükseltme başarısız"})
                print("  [%3d/%d] ⛔ %-34s yükseltilemedi"
                      % (i, len(names), name[:34]))
                continue
            info = finish(tmp, p["dst"], p["target"], p["dpi"], p["crop"])
            done.append({"file": name, "class": p["class"],
                         "dst": os.path.relpath(p["dst"], pl.ROOT),
                         "cropped": bool(p["crop"]), "dpi": p["dpi"], **info})
            el = time.time() - t0
            print("  [%3d/%d] ✓ %-30s %s → %s%s  (%.0f sn, kalan ~%.0f dk)"
                  % (i, len(names), name[:30],
                     "×".join(map(str, info["upscaled"])),
                     "×".join(map(str, info["final"])),
                     " KIRPILDI" if p["crop"] else "",
                     el, (el / i) * (len(names) - i) / 60))
        except Exception as exc:                               # noqa: BLE001
            failed.append({"file": name, "why": str(exc)[:200]})
            print("  [%3d/%d] ⛔ %-34s %s" % (i, len(names), name[:34], exc))
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    write_index(failed)

    print("\n" + "=" * 74)
    print("  ✓ %d işlendi · ⛔ %d başarısız · %.1f dk"
          % (len(done), len(failed), (time.time() - t0) / 60))
    print("=" * 74)
    shutil.rmtree(args.tmp, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
