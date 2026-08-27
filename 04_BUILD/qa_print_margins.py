#!/usr/bin/env python3
"""
BASKI PAYI KAPISI — MÜREKKEBİN NEREDE OLDUĞUNU ÖLÇER
================================================================================
⭑ BU KAPI BİR KDP REDDİNDEN DOĞDU ⭑

KDP Print Previewer ciltsiz iç bloğu **"Insufficient gutter"** diyerek
reddetti ve beş sayfa saydı: 60, 94, 96, 122, 224.

Beş değildi. Ölçünce **274 sayfanın 140'ı** ihlaldeydi — KDP yalnızca bir
örnek göstermişti. Ciltlide durum daha kötüydü: **245 sayfa.**

⚠ VE İKİ AYRI KUSUR VARDI:

  ① AYNALAMA HİÇ OLMUYORDU. `interior.py` iki sayfa şablonu (tek/çift)
    kaydediyordu ama aralarında HİÇ geçiş yapmıyordu; reportlab
    `NextPageTemplate` görmedikçe listedeki İLK şablonu bütün kitap
    boyunca kullanır. Yani oluk payı 274 sayfanın 274'ünde de SOLDA
    kaldı. Ciltside çift sayfalarda oluk yerine dış pay bırakıyordu.
    ⚠ Kodun kendi yorumu "İÇ KENAR AYNALANIR" diyordu. Kod demiyordu.

  ② PAYLAR ASGARİYE DAYANMIŞTI. reportlab akış nesnelerini KIRPMAZ;
    yaslanmış bir satırın son glifi kendi ilerleme genişliğinin
    0,007–0,020" ötesine taşar. Çerçeve tam 0,500"de bitse bile
    MÜREKKEP 0,480"e geliyordu. Asgariye dayanmak toleransı sıfırlamaktır.

⭑ NEDEN BU KAPI VAR ⭑ — çünkü hiçbir kapı MÜREKKEBE bakmıyordu.
`interior.py` çerçeveyi doğru kuruyor ve "yeşil" diyordu; çerçevenin
DIŞINA taşan mürekkebi kimse ölçmüyordu. Bir dizgi kapısı, dizginin
niyetini değil ÇIKTISINI denetlemelidir.

⚠ NASIL ÖLÇER: sayfaları raster'a çevirir ve her sayfanın GERÇEK
mürekkep sınırlayıcı kutusunu bulur. Metin, görsel, çizgi, sayfa
numarası — hepsi. Niyet değil, piksel.

⚠ VE EŞİK BİZİM PAYIMIZ DEĞİL, KDP'NİN EŞİĞİDİR (`kdp_min_gutter`).
Payı büyütüp kapıyı da büyütmek, kapıyı kendi kendine yeşil yakar.

Çıkış kodları:  0 = temiz   1 = ihlal   2 = bağımlılık yok (atlandı)
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
import interior as IN                                          # noqa: E402

OUT = os.path.join(pl.ROOT, "08_OUTPUT")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "qa-print-margins.json")

# KDP dış/üst/alt asgarisi (taşmasız iç blok).
KDP_MIN_OUTER = 0.25
# Raster çözünürlüğü: 1 px = 0,0067" — ölçtüğümüz pay farkı 0,1"
# mertebesinde, yani fazlasıyla yeterli.
DPI = 150
# Kâğıttan koyu sayılan eşik. Levha zeminleri beyaza çekilir
# (`interior.PLATE_WHITE`), bu yüzden 245 güvenli bir ayrımdır.
INK = 245


def ink_box(path: str):
    """Sayfadaki HER TÜRLÜ mürekkebin sınırlayıcı kutusu (inç)."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path)
    w, h = im.size
    mask = im.convert("L").point(lambda v: 0 if v < INK else 255)
    bb = mask.point(lambda v: 255 - v).getbbox()
    if not bb:
        return None
    l, t, r, b = bb
    return (l / DPI, t / DPI, (w - r) / DPI, (h - b) / DPI)   # sol üst sağ alt


def scan(pdf: str, binding: str, pages_hint: int, rep, verbose: bool) -> dict:
    if not os.path.isfile(pdf):
        rep.warn("%s iç bloğu YOK — taranamadı (%s)"
                 % (binding, os.path.relpath(pdf, pl.ROOT)))
        return {}
    min_gutter = IN.kdp_min_gutter(pages_hint, binding)
    tmp = tempfile.mkdtemp(prefix="qa-margins-")
    try:
        subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", "-png",
                        pdf, os.path.join(tmp, "pg")],
                       check=True, capture_output=True, timeout=1800)
        files = sorted(glob.glob(os.path.join(tmp, "*.png")))
        odd_l, even_l, bad = [], [], []
        worst = (99.0, None, "")
        for f in files:
            pg = int(re.search(r"pg-?(\d+)\.png", os.path.basename(f)).group(1))
            box = ink_box(f)
            if not box:
                continue                       # boş sayfa: ihlal edemez
            left, top, right, bot = box
            odd = pg % 2 == 1
            (odd_l if odd else even_l).append(left)
            inner = left if odd else right
            outer = right if odd else left
            for name, val, mn in (("inner", inner, min_gutter),
                                  ("outer", outer, KDP_MIN_OUTER),
                                  ("top", top, KDP_MIN_OUTER),
                                  ("bottom", bot, KDP_MIN_OUTER)):
                if val - mn < worst[0]:
                    worst = (val - mn, pg, "%s %.3f (asgari %.3f)"
                             % (name, val, mn))
                if val < mn - 0.002:
                    bad.append({"page": pg, "edge": name,
                                "measured": round(val, 4), "min": mn})
        n = len(files)
        med_odd = sorted(odd_l)[len(odd_l) // 2] if odd_l else 0.0
        med_even = sorted(even_l)[len(even_l) // 2] if even_l else 0.0
        mirrored = abs(med_odd - med_even) > 0.05

        print("\n── %s ── (%d sayfa · oluk asgarisi %.3f\")"
              % (binding.upper(), n, min_gutter))
        print("  tek sayfa sol kenar        %.3f in" % med_odd)
        print("  çift sayfa sol kenar       %.3f in" % med_even)
        print("  en dar pay                 %+.3f in (s. %s · %s)"
              % (worst[0], worst[1], worst[2]))

        # ⭑ AYNALAMA ÖLÇÜLÜR, VARSAYILMAZ ⭑ — kapının doğduğu kusur budur.
        rep.check(mirrored,
                  "⭑ %s · OLUK PAYI GERÇEKTEN AYNALANIYOR ⭑ "
                  "(tek %.3f ↔ çift %.3f)" % (binding.upper(), med_odd, med_even)
                  + ("" if mirrored else
                     " — ⛔ İKİ YÜZ AYNI: `NextPageTemplate` verilmemiş, "
                     "oluk her sayfada aynı kenarda"))
        rep.check(not bad,
                  "⭑ %s · HER SAYFA KDP GÜVENLİ ALANI İÇİNDE ⭑ (%d sayfa)"
                  % (binding.upper(), n)
                  + ("" if not bad else " — ⛔ %d sayfa ihlalde: %s"
                     % (len(bad), [b["page"] for b in bad[:8]])))
        if bad and verbose:
            for b in bad[:20]:
                print("      s.%-4d %-7s %.3f < %.3f"
                      % (b["page"], b["edge"], b["measured"], b["min"]))
        return {"pages": n, "minGutter": min_gutter, "mirrored": mirrored,
                "medianOddLeft": round(med_odd, 4),
                "medianEvenLeft": round(med_even, 4),
                "tightestClearanceIn": round(worst[0], 4),
                "tightestAt": {"page": worst[1], "what": worst[2]},
                "violations": bad}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--json", default=STATS)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    try:
        import PIL                                             # noqa: F401
    except ImportError:
        print("ATLANDI: Pillow yok")
        return 2
    if not shutil.which("pdftoppm"):
        print("ATLANDI: pdftoppm (poppler) yok")
        return 2

    print("=" * 74)
    print("  BASKI PAYI KAPISI · mürekkebin GERÇEK yeri ölçülür")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    facts = {}
    for binding, sub in (("paperback", "PAPERBACK"), ("hardcover", "HARDCOVER")):
        stats = pl.load_json(os.path.join(
            pl.ROOT, "06_REPORTS", "tracked",
            "interior.json" if binding == "paperback"
            else "interior-hardcover.json")) or {}
        pages = (stats.get("facts") or {}).get("pages") or 274
        facts[binding] = scan(os.path.join(OUT, sub, "interior.pdf"),
                              binding, pages, rep, args.verbose)

    print("\n── özet ──")
    for b, f in facts.items():
        if not f:
            continue
        print("  %-11s %d sayfa · en dar pay %+.3f in · ihlal %d"
              % (b, f["pages"], f["tightestClearanceIn"], len(f["violations"])))
    if any(f and f["violations"] for f in facts.values()):
        print()
        print("  ⚠ reportlab akış nesnelerini KIRPMAZ: çerçeve doğru olsa")
        print("    bile mürekkep dışına taşabilir. Payı büyütmek ya da")
        print("    taşan öğeyi daraltmak gerekir — kapıyı gevşetmek DEĞİL.")

    rep.facts.update(facts)
    return rep.finish("baskı payı", args.json)


if __name__ == "__main__":
    sys.exit(main())
