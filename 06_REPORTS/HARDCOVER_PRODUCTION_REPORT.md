# CİLTLİ (HARDCOVER) ÜRETİM RAPORU

**Tarih:** 26 Ağustos 2026
**Geometri kaynağı:** `hardcover-calculator.png` → `03_COVER/HARDCOVER_CALCULATOR_VALUES.md`

## 1 · Değerler OKUNDU, türetilmedi

Ciltli sırt **hesaplanamaz**: sayfa payına ek olarak tahta ve sarma payı
taşır. Ölçüm kanıtı:

```
263 sayfa × 0,002252 (beyaz kâğıt) = 0,592 in
hesaplayıcının verdiği sırt        = 0,781 in
fark (tahta + yapı)                = 0,189 in
```

Yani formülle üretilseydi sırt **%24 dar** çıkardı. Bu yüzden değerler
kurucunun teslim ettiği KDP hesaplayıcı ekranından okundu.

## 2 · Üretilen dosyalar

`08_OUTPUT/HARDCOVER/` → `interior.pdf` · `cover.pdf` · `metadata.json`
· `SHA256SUMS`

| | Ciltli | Ciltsiz | Fark |
|---|---:|---:|---:|
| Sayfa | **264** | 264 | — |
| **İç kenar payı** | **0,625 in** | 0,500 in | +0,125 |
| Sırt | **0,7833 in** | 0,6600 in | +0,123 |
| Tam kapak | **14,359 × 10,417** | 12,910 × 9,250 | +1,449 × +1,167 |
| Menteşe | **0,394 in** | — | ciltliye özgü |
| Sarma/taşma | **0,591 in** | 0,125 in | +0,466 |
| Kâğıt | beyaz | krem | — |
| PDF | 68,6 MB | 71,7 MB | — |

⭑ **İç kenar payı ciltliye göre yeniden hesaplandı.** KDP'nin ciltli
tablosu 151–300 sayfa için **0,625 inç** ister; ciltsizin 0,5'ini
kullanmak, düz açılmayan bir ciltte metni oluğa gömerdi. Bir kapı bunu
zorlar (`kdp_package.py`).

⭑ **Ciltsiz geometrisi KOPYALANMADI.** Bir kapı iki kapağın genişliğinin
**en az 1 inç** farklı olmasını arar — aynı çıksalardı biri
kopyalanmış olurdu.

## 3 · Tipografi

Baskı kapağıyla aynı motor (`04_BUILD/cover_type.py`): mürekkep harfin
altındaki piksellerden seçilir, gerekirse vektör hâle eklenir.
**17 satır** hâleli, en düşük kenar karşıtlığı **17,69 : 1**.

Barkod alanı (0,25 × 0,375 in pay) **boş** bırakıldı; numara
uydurulmadı.

## 4 · ⚠ Hesaplayıcı bir sayfa bayat

Hesaplayıcı **263** sayfayla koştu; iç blok çift sayfaya tamamlanınca
**264** oldu.

```
fark: 1 sayfa × 0,002252 in = 0,00225 in
KDP kapak toleransı        = ±0,0625 in
kullanılan pay             = %3,6
```

Sırt bu farkla **düzeltildi** (0,781 → 0,7833). Tolerans içinde olduğu
için kapı kırmızı yakmıyor, **uyarı** veriyor. Kesinlik isteniyorsa
hesaplayıcı 264 sayfayla yeniden koşturulup değerler güncellenmelidir.

## 5 · ⚠ Sanat çözünürlüğü

Sarmal sanat ciltlide **82,1 dpi doğal** (ciltsizde 92,4). Ciltli kapak
fiziksel olarak daha büyük olduğu için aynı sanat daha da yetersiz
kalıyor. 300 dpi'a yükseltildi ama **kazanılan detay tahmindir**.

Gereken: **4308 × 3125 px** (300 dpi) · önerilen **8614 × 6250** (2×).
Ayrıntı: `06_REPORTS/COVER_ARTWORK_GENERATION_GUIDE.md`

**Bu KDP'yi engellemez** — ölçüler ve paylar doğru, dosya geçerli.
Baskıda yumuşak görünme riski vardır.

## 6 · Ekonomi

| | |
|---|---:|
| Liste | 29,99 $ |
| Baskı maliyeti (264 s) | **8,82 $** |
| **Telif** | **9,18 $** |
| Marj | %30,6 |

BRIEF § 7'deki hipotez 208 sayfaya dayanıyordu (maliyet 8,15 · telif
9,85). Ölçülen 264 sayfa maliyeti **0,67 $ artırdı**.
