# HARDCOVER — KDP HESAPLAYICI DEĞERLERİ

**Kaynak görüntü:** `hardcover-calculator.png` (depo kökü, kurucu teslimi)
**Okundu:** 26 Ağustos 2026 · doğrudan görüntüden, hafızadan DEĞİL

> ⚠ **BU DEĞERLER TÜRETİLMEDİ, OKUNDU.** KDP'nin kendi hesaplayıcısının
> ekran görüntüsünden alındı. Eski bir proje dosyasıyla çelişen her
> değerde **kurucu teslimi hesaplayıcı kazanır**.

## Girdiler (hesaplayıcıya yazılan)

| Alan | Değer |
|---|---|
| Binding type | **Hardcover** |
| Interior type | Black & white |
| Paper type | **White paper** |
| Reading direction | Left to Right |
| Measurement units | Inches |
| Interior trim size | **6 × 9 in** |
| **Page count** | **263** |

⚠ **KÂĞIT FARKI:** hardcover **beyaz** kâğıtla hesaplandı; ciltsiz sürüm
`metadata.editions.paperback.paper = cream`. Bu bir çelişki değil, iki
ayrı üründür — ama sırt genişlikleri bu yüzden farklıdır ve **ciltsizin
sırtı hardcover'ınkine eşit değildir.**

⚠ **SAYFA SAYISI DOĞRULANDI:** hesaplayıcıdaki 263, üretilen iç bloğun
ölçülen sayfa sayısıyla **aynıdır** (`06_REPORTS/tracked/interior.json`).
Bayat değer kullanılmadı.

## Çıktılar (hesaplayıcının verdiği)

| # | Açıklama | Genişlik (in) | Yükseklik (in) |
|---|---|---:|---:|
| 1 | **Full Cover** | **14.356** | **10.417** |
| 2 | Front Cover | 6.197 | 9.236 |
| 3 | Margin | 0.125 | 0.125 |
| 4 | Wrap | 0.591 | 0.591 |
| 5 | Hinge | 0.394 | 10.417 |
| 6 | **Spine** | **0.781** | 9.236 |
| 7 | Spine Safe Area | 0.656 | 8.986 |
| 8 | Spine Margin | 0.062 | 0.062 |
| 9 | Barcode Margin | 0.25 | 0.375 |

## Geometri doğrulaması

Değerler kendi içinde tutarlı — ölçülerek denetlendi:

```
tam genişlik = 2 × ön(6.197) + sırt(0.781) + 2 × sarma(0.591)
             = 12.394 + 0.781 + 1.182
             = 14.357  ≈ 14.356  ✓

tam yükseklik = ön yükseklik(9.236) + 2 × sarma(0.591)
              = 10.418  ≈ 10.417  ✓
```

**Kapak tahtası trimden BÜYÜKTÜR** (ciltli kitaplarda standarttır):
6.197 − 6.000 = **0.197 in** genişlikte, 9.236 − 9.000 = **0.236 in**
yükseklikte taşma.

## ⭑ CİLTSİZLE KARIŞTIRILAMAZ ⭑

| | Ciltsiz (paperback) | Ciltli (hardcover) |
|---|---:|---:|
| Kâğıt | krem | **beyaz** |
| Sırt | 0.6575 in | **0.781 in** |
| Tam kapak | 12.908 × 9.250 | **14.356 × 10.417** |
| Taşma/sarma | 0.125 taşma | **0.591 sarma** |
| Menteşe | yok | **0.394 in** |

Ciltsiz geometrisini ciltliye kopyalamak, **1.448 inç dar** ve
**1.167 inç kısa** bir kapak üretir — KDP bunu reddeder.

## Piksel hedefleri (300 dpi)

| | inç | 300 dpi piksel |
|---|---:|---:|
| Tam kapak | 14.356 × 10.417 | **4307 × 3125** |
| Sırt | 0.781 × 9.236 | 234 × 2771 |
| Sırt güvenli alan | 0.656 × 8.986 | 197 × 2696 |

**Tam kapak en-boy oranı: 14.356 / 10.417 = 1.378 : 1**
