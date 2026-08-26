#!/usr/bin/env python3
"""
KAPAK TİPOGRAFİSİ — ÖLÇÜLEN karşıtlıkla, gözle değil
================================================================================
⚠ BU MODÜL BİR ŞİKÂYETTEN DOĞDU: "yazı çok saydam, zor okunuyor."

Önceki sürüm mürekkep rengini bir KUTUNUN ortalama parlaklığından
seçiyordu. Kutu ortalaması yalan söyler: koyu bir kitap ile açık bir
kâğıt yüzey aynı kutuda ortalanınca "orta" çıkar ve metin ikisinin de
üstünde kaybolur.

⭑ BU MODÜL HARFİN ALTINA BAKAR ⭑

  ① Metin bir MASKEYE çizilir (raster, 300 dpi).
  ② Sanatın parlaklığı YALNIZCA harf pikselleri altında örneklenir.
  ③ Mürekkep, WCAG bağıl parlaklığıyla karşıtlığı EN YÜKSEK olan uçtur.
  ④ Karşıtlık eşiğin altındaysa yerel bir PERDE eklenir — dikdörtgen
    kutu değil, harflerin şeklini izleyen yumuşak bir koyulaştırma.
  ⑤ Karşıtlık YENİDEN ölçülür ve rapora yazılır.

⚠ TİPOGRAFİ VEKTÖR KALIR. Maske yalnızca ÖLÇÜM içindir; PDF'e giden
yazı reportlab'ın vektör metnidir — baskıda keskin, küçükte okunur.

⚠ YASAK: opak beyaz panel, dikdörtgen etiket, sahte kâğıt şerit.
Sanat görünür kalır.
"""

from __future__ import annotations

import math
import os

# WCAG 2.x karşıtlık oranı eşikleri.
# ⚠ 4,5 "normal metin" eşiğidir. Kapak başlığı büyük punto olduğu için
# 3,0 da savunulabilir; ama kapak KÜÇÜK KÜÇÜK RESİMDE de okunmalıdır
# (yönerge § B: "readable in thumbnail"), bu yüzden taban 4,5'tir.
MIN_CONTRAST = 4.5
GOOD_CONTRAST = 7.0

DARK = (0.07, 0.06, 0.05)
LIGHT = (0.98, 0.965, 0.93)


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(rgb) -> float:
    """WCAG bağıl parlaklık (0-1). rgb 0-255 ya da 0-1 olabilir."""
    r, g, b = rgb[:3]
    if r > 1 or g > 1 or b > 1:
        r, g, b = r / 255.0, g / 255.0, b / 255.0
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(l1: float, l2: float) -> float:
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def text_mask(text: str, font_path: str, px: int):
    """Metni bir maskeye çizer — ÖLÇÜM için, baskı için değil."""
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(font_path, px)
    box = f.getbbox(text)
    w = max(1, box[2] - box[0] + 4)
    h = max(1, box[3] - box[1] + 4)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((2 - box[0], 2 - box[1]), text, fill=255, font=f)
    return m


def under_glyphs(art, mask, cx_px: int, cy_px: int) -> tuple:
    """⭑ HARFİN ALTINDAKİ PİKSELLER ⭑ — kutu ortalaması DEĞİL.

    Dönüş: (ortalama bağıl parlaklık, en açık, en koyu, piksel sayısı)
    """
    aw, ah = art.size
    mw, mh = mask.size
    x0, y0 = cx_px - mw // 2, cy_px - mh // 2
    x0 = max(0, min(aw - 1, x0))
    y0 = max(0, min(ah - 1, y0))
    x1, y1 = min(aw, x0 + mw), min(ah, y0 + mh)
    if x1 <= x0 or y1 <= y0:
        return (0.5, 0.5, 0.5, 0)

    crop = art.crop((x0, y0, x1, y1)).convert("RGB")
    mc = mask.crop((0, 0, x1 - x0, y1 - y0))
    cp, mp = crop.load(), mc.load()

    lo, hi, tot, n = 1.0, 0.0, 0.0, 0
    step = max(1, int(math.sqrt((x1 - x0) * (y1 - y0) / 4000)) )
    for y in range(0, y1 - y0, step):
        for x in range(0, x1 - x0, step):
            if mp[x, y] < 128:
                continue
            L = rel_luminance(cp[x, y])
            tot += L
            n += 1
            lo = min(lo, L)
            hi = max(hi, L)
    if not n:
        return (0.5, 0.5, 0.5, 0)
    return (tot / n, hi, lo, n)


def choose_ink(mean_l: float, hi: float, lo: float) -> tuple:
    """⭑ MÜREKKEP, EN KÖTÜ DURUMA GÖRE SEÇİLİR ⭑

    ⚠ Ortalamaya göre seçmek, alacalı bir zeminde metnin bir kısmının
    kaybolmasıdır. Koyu mürekkep zemindeki EN KOYU pikselle, açık
    mürekkep EN AÇIK pikselle yarışır; hangisi daha iyi dayanıyorsa o
    seçilir.
    """
    dl, ll = rel_luminance(DARK), rel_luminance(LIGHT)

    # ⚠ SEÇİM ORTALAMAYA GÖRE YAPILIR, EN KÖTÜ PİKSELE GÖRE DEĞİL.
    # İlk sürüm en kötü pikseli ölçüt aldı ve açık kâğıt yüzey zeminli
    # arka kapakta BEYAZ metin seçti: teknik olarak "dayanıklı" ama
    # gözle yanlış — açık zemine koyu yazılır. En kötü pikseli HÂLE
    # zaten kapatıyor; seçimin işi tipografik olarak DOĞRU olanı
    # bulmaktır.
    c_dark = contrast(dl, mean_l)
    c_light = contrast(ll, mean_l)
    if c_dark >= c_light:
        return DARK, contrast(dl, lo), "koyu"
    return LIGHT, contrast(ll, hi), "açık"


def halo_for(ink) -> tuple:
    """Hâlenin rengi mürekkebin ZIDDIDIR — kenarı garanti eder."""
    return LIGHT if rel_luminance(ink) < 0.5 else DARK


def place(art, text, font_path, px, cx_px, cy_px, want=MIN_CONTRAST,
          rotate: bool = False):
    """⭑ ÖLÇ, MÜREKKEBİ SEÇ, HÂLE İLE GARANTİ ET ⭑

    ⚠ İKİ SÜRÜM ÖNCE RASTER PERDE DENENDİ VE BIRAKILDI. Perde,
    karşıtlığı 1,47 → 4,7 çıkardı ama gözle bakınca metnin arkasında
    DİKDÖRTGEN bir bant olarak okunuyordu — yönergenin § B'de açıkça
    yasakladığı şey ("no opaque rectangular panels"). Ölçü düzeldi,
    tasarım bozuldu; ikisi birden doğru olmalıydı.

    Çözüm hâledir: harfin KENDİ ŞEKLİNİ izleyen, mürekkebin zıddı
    renkte ince bir dış çizgi. Vektördür, kutusu yoktur, sanat altından
    tamamen görünür ve kenar karşıtlığı zeminden BAĞIMSIZ olarak
    garanti edilir (koyu ↔ açık ≈ 19:1).

    ⚠ `rotate`: sırt yazısı DİK basılır. Maskeyi döndürmemek, ölçümü
    yanlış piksellerden almak demektir — ilk sürümde tam olarak bu oldu
    ve sırtın ortasına yatay bir bant düştü.
    """
    mask = text_mask(text, font_path, px)
    if rotate:
        mask = mask.rotate(90, expand=True)
    mean_l, hi, lo, n = under_glyphs(art, mask, cx_px, cy_px)
    ink, c, which = choose_ink(mean_l, hi, lo)
    halo = halo_for(ink)
    edge = contrast(rel_luminance(ink), rel_luminance(halo))
    return {"ink": ink, "halo": halo, "contrast": round(c, 2),
            "edgeContrast": round(edge, 2), "needsHalo": c < want,
            "side": which, "pixels": n,
            "worstDark": round(lo, 4), "worstLight": round(hi, 4)}
