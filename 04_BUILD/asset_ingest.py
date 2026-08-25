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


SHEET = os.path.join(pl.ROOT, "07_ASSETS", "PLATE_VERIFICATION.html")


def build_sheet(rows: list) -> int:
    """⭑ SAYIM SAYFASI — levhanın YANINDA sözleşmesi ⭑

    ⚠ NEDEN OTOMATİK SAYILMIYOR: denendi ve GÜVENİLMEDİ. Eşikleme
    gravürün taramasını işaret sanıyor (bir levhada 5 yerine 44 saydı),
    özilinti ise armoniklere kilitleniyor (6 yerine 2,6). Güvenilmez bir
    sayaç, sayaç olmamasından KÖTÜDÜR: yanlış yeşil, bakılmamış bir
    levhayı bakılmış gösterir.

    Bu yüzden ajan sayıyı ÖLÇMEZ; insanın ölçmesini MÜMKÜN KILAR.
    Her levha, kendi değiştirilemez sayılarının yanına basılır.
    """
    lib = open(LIB, encoding="utf-8").read()
    import html as _h
    strip = lambda x: _h.unescape(re.sub("<[^>]+>", "", x)).strip()
    data = {}
    for m in re.finditer(r'<article class="card" id="([a-z0-9-]+)">(.*?)'
                         r'(?=<article class="card"|<h2 )', lib, re.S):
        dm = re.search(r'⭑ VERİ — DEĞİŞTİRİLEMEZ ⭑</h4><ul class="data">'
                       r'(.*?)</ul>', m.group(2), re.S)
        if dm:
            data[m.group(1)] = [strip(x) for x in
                                re.findall(r"<li>(.*?)</li>", dm.group(1), re.S)]

    grav = [r for r in rows if r["class"].startswith("GRAVÜR")]
    grav.sort(key=lambda r: r["file"])
    cards, n_count = [], 0
    for r in grav:
        pid = r["file"][:-4]
        items = data.get(pid, [])
        counted = [i for i in items if i.startswith("exactly")]
        if counted:
            n_count += 1
        li = "".join('<li class="%s">%s</li>'
                     % ("k" if i.startswith("exactly") else "", _h.escape(i))
                     for i in items) or "<li class='n'>sayı taahhüdü yok</li>"
        cards.append(
            '<article><label><input type="checkbox" id="v-%s"> '
            '<b>%s</b></label>'
            '<img src="raw/%s" alt="%s" loading="lazy">'
            '<ul>%s</ul></article>' % (pid, pid, r["file"], pid, li))

    doc = """<title>Levha Sayım Sayfası</title>
<style>
:root{--bg:#faf7f2;--ink:#241f1a;--mut:#6d6459;--line:#ded5c7;--card:#fff;
--hot:#8f2f2f;--hotbg:#f6e9e9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--bg:#17150f;--ink:#ece5d8;--mut:#a2988a;--line:#3a3328;--card:#1f1c15;
--hot:#e79191;--hotbg:#2c1c1c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 Georgia,serif;padding:0 18px 70px}
.w{max-width:1280px;margin:0 auto}
h1{margin:26px 0 4px}
p.s{color:var(--mut);margin:0 0 16px}
.bar{position:sticky;top:0;background:var(--bg);padding:10px 0;
border-bottom:1px solid var(--line);z-index:5;font:700 13px monospace}
.g{display:grid;gap:14px;margin-top:16px;
grid-template-columns:repeat(auto-fill,minmax(310px,1fr))}
article{background:var(--card);border:1px solid var(--line);
border-radius:11px;padding:11px}
article img{width:100%;height:auto;border:1px solid var(--line);
border-radius:7px;margin:8px 0;background:#fff}
label{cursor:pointer;font:600 13px monospace}
label input{width:16px;height:16px;vertical-align:-3px}
ul{margin:0;padding-left:17px;font-size:12.5px;color:var(--mut)}
li.k{color:var(--hot);background:var(--hotbg);font-weight:700;
padding:2px 5px;border-radius:4px;margin:2px 0;list-style:none;
margin-left:-17px}
li.n{font-style:italic}
.note{border-left:4px solid var(--hot);background:var(--hotbg);
padding:11px 14px;border-radius:0 9px 9px 0;margin:14px 0}
</style>
<div class="w">
<h1>Levha Sayım Sayfası</h1>
<p class="s">__N__ gravür · __C__ tanesi sayı taahhüdü taşıyor ·
bu dosya <code>04_BUILD/asset_ingest.py --sheet</code> ile üretildi.</p>
<div class="note"><b>⚠ BU SAYIMI AJAN YAPMADI VE YAPAMAZ.</b><br>
Otomatik sayım denendi ve güvenilmedi: eşikleme gravürün kendi
taramasını işaret sanıyor, özilinti armoniklere kilitleniyor. Güvenilmez
bir sayaç sayaç olmamasından <b>kötüdür</b> — bakılmamış bir levhayı
bakılmış gösterir.<br><br>
Kırmızı satırlar <b>sayılacak</b> şartlardır. Levhada sayın. Tutmuyorsa
o levha <b>yeniden üretilir</b>; veri pazarlığa kapalıdır.</div>
<div class="bar" id="c">0 / __N__</div>
<div class="g">__CARDS__</div>
</div>
<script>
(function(){var K="enigmatica-plate-verify";
var s={};try{s=JSON.parse(localStorage.getItem(K))||{}}catch(e){}
var b=[].slice.call(document.querySelectorAll("input"));
function t(){var n=b.filter(function(x){return x.checked}).length;
document.getElementById("c").textContent=n+" / "+b.length+
" doğrulandı";}
b.forEach(function(x){if(s[x.id]){x.checked=true}
x.addEventListener("change",function(){s[x.id]=x.checked;
try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}t()})});
t();})();
</script>"""
    doc = (doc.replace("__CARDS__", "\n".join(cards))
              .replace("__N__", str(len(grav)))
              .replace("__C__", str(n_count)))
    open(SHEET, "w", encoding="utf-8").write(doc)
    return len(grav)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    ap.add_argument("--sheet", action="store_true",
                    help="levha sayım sayfasını üret")
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

    # ── ⭑ LEVHA SAYFAYA SIĞIYOR MU ⭑ ──────────────────────────────────
    # ⚠ ETKİN DPI YETERLİ OLSA BİLE bir levha sayfaya TAM GENİŞLİKTE
    # oturmayabilir: çok uzun bir levha yükseklikten sınırlanır ve
    # sütundan dar basılır. DPI düşmez ama FİZİKSEL detay küçülür —
    # 0,3 mm'lik bir boşluk 0,22 mm olur ve nokta yayılması altında
    # kapanır. Veri taşıyan bir levhada bu, sayılamayan bir işarettir.
    narrow = []
    for r in grav:
        if not r.get("aspect"):
            continue
        need_h = BOX_W_IN / r["aspect"]          # tam genişlikte yükseklik
        if need_h > BOX_H_IN:
            w_in = BOX_H_IN * r["aspect"]        # yükseklikten sınırlanır
            narrow.append((r["file"], round(w_in, 2),
                           round(100 * w_in / BOX_W_IN)))
    if narrow:
        rep.warn("%d levha sütun genişliğine SIĞMIYOR, yükseklikten "
                 "sınırlanıyor ve dar basılacak: %s — en küçük detay "
                 "aynı oranda küçülür (POD provasında ölçülmeli · A9)"
                 % (len(narrow), ", ".join("%s %.2f in (%%%d)" % n
                                           for n in narrow)))
    else:
        rep.check(True, "her levha sütun genişliğine sığıyor")

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

    if args.sheet:
        n = build_sheet(rows)
        print("\n  ✍ %s  (%d levha)"
              % (os.path.relpath(SHEET, pl.ROOT), n))

    rep.facts.update({
        "delivered": len(rows), "expected": len(expected),
        "gravure": len(grav), "cover": len(cov), "aplus": len(apl),
        "missing": missing, "unknown": unknown,
        "belowDpiFloor": [f for f, _ in low],
        "aplusAspectMismatch": [b[0] for b in ap_bad],
        "dpiFloor": DPI_FLOOR,
        "printBoxIn": [BOX_W_IN, BOX_H_IN],
        "narrowPlates": [n[0] for n in narrow],
        "assets": rows,
    })
    return rep.finish("%d varlık ölçüldü" % len(rows), args.json)


if __name__ == "__main__":
    sys.exit(main())
