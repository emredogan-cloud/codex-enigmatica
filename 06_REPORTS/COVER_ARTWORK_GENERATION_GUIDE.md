# KAPAK SANATINI TAM ÖLÇÜDE ÜRETME KILAVUZU

**Soru:** *"Kapak sanatını gelecekte TAM gereken ölçüde nasıl üretirim?"*

Bu belge o soruyu sayılarla yanıtlar ve tekrarlanabilir bir iş akışı verir.

---

## A · Uyuşmazlık neden oldu

Teslim edilen sarmal sanat **1840 × 855 px**, yani **2,152 : 1**.
Ciltsiz kapağın gerektirdiği oran **1,3955 : 1**.

Oran tutmayınca tek seçenek kırpmaktır ve kırpma **genişliğin
%35,2'sini** götürdü: arka kapağın sol kenarı ve ön kapağın sağ kenarı.
Geriye **1193 × 855** kaldı — 12,908 inçlik bir kapakta bu **92 dpi**
demektir. 300 dpi'a yükseltildi ama **kazanılan detay tahmindir**.

**Kök sebep:** görsel modele "sarmal kapak" denildi, **oran verilmedi**.
Model kendi varsayılan geniş formatını üretti.

## B · Hangi ölçü yetkilidir

⭑ **FİZİKSEL İNÇ YETKİLİDİR. PİKSEL ONDAN TÜRER.** ⭑

Sıra asla tersine çevrilmez. Önce KDP'nin verdiği inç, sonra hedef dpi,
sonra piksel. "Şu kadar piksel üretelim, sonra uydururuz" yaklaşımı tam
olarak yukarıdaki kaybı üretir.

## C · Nihai KDP sarmal ölçüsü nasıl hesaplanır

**Ciltsiz (kendiniz hesaplayabilirsiniz):**

```
sırt        = sayfa sayısı × kâğıt kalınlığı
              krem 0,0025 in/sayfa · beyaz 0,002252 in/sayfa
tam genişlik = taşma + 6 + sırt + 6 + taşma      (taşma 0,125)
tam yükseklik = taşma + 9 + taşma
```

**Ciltli (hesaplayamazsınız — KDP hesaplayıcısı verir):**

Ciltlide tahta trimden büyüktür, menteşe (hinge) ve sarma (wrap) payı
vardır. Bunlar formülle türetilmez; KDP'nin **Print Cover Calculator**
sayfasından okunur ve ekran görüntüsü saklanır.
→ `03_COVER/HARDCOVER_CALCULATOR_VALUES.md`

## D · Sayfa sayısı sırtı nasıl değiştirir

Sırt **tamamen** sayfa sayısına bağlıdır. Bu yüzden **sanat, iç blok
dondurulmadan üretilemez**:

| Sayfa | Ciltsiz sırt (krem) | Tam genişlik | Oran |
|---:|---:|---:|---:|
| 200 | 0,500 in | 12,750 | 1,3784 |
| 263 | **0,658 in** | **12,908** | **1,3955** |
| 300 | 0,750 in | 13,000 | 1,4054 |

**Yirmi sayfalık bir değişiklik oranı 0,003 oynatır** — bu küçüktür ama
sırtı 0,05 inç kaydırır ve sırt yazısı ortalanmaz.

⚠ **Bu yüzden sıra şudur: ÖNCE iç blok, SONRA kapak sanatı.**

## E · Ciltsiz ve ciltli farkı

| | Ciltsiz | Ciltli |
|---|---:|---:|
| Kâğıt | krem | beyaz |
| Sırt | 0,6575 in | **0,781 in** |
| Tam kapak | 12,908 × 9,250 | **14,356 × 10,417** |
| Oran | **1,3955** | **1,3781** |
| Dış pay | 0,125 taşma | **0,591 sarma** |
| Menteşe | — | **0,394 in** |

**İki ayrı sanat gerekir.** Oranlar birbirine yakın (1,3955 ↔ 1,3781)
ama aynı değildir; tek dosyayı ikisine birden kırpmak ciltlide
%1,3'lük bir kayma yaratır — sırt yazısı için bu çok fazladır.

## F · İnçten piksele

```
hedef piksel = inç × hedef dpi
```

**300 dpi tabandır** (KDP asgarisi). Bu kitap için:

| Sürüm | inç | 300 dpi | **önerilen 600 dpi** |
|---|---|---:|---:|
| Ciltsiz | 12,908 × 9,250 | 3872 × 2775 | **7745 × 5550** |
| Ciltli | 14,356 × 10,417 | 4307 × 3125 | **8614 × 6250** |

## G–H · Güvenlik payı ve aşırı örnekleme

300 dpi **asgaridir, hedef değildir.** Aşağıdakiler onu yer:

- kırpma (oran tutmazsa)
- yeniden konumlandırma
- sırt genişliğinin sonradan değişmesi
- keskinleştirme ve renk düzeltme

**Öneri: 2× (600 dpi).** 4× yalnızca sanat sonradan yeniden
çerçevelenecekse gerekir; dosya boyutu dörde katlanır.

⭑ **Kural:** üretilen sanatın kısa kenarı, nihai kısa kenarın
**en az iki katı** olmalıdır.

## I–J · Oranı korumak · modelin yanlış oran vermesini önlemek

Görsel modeller oranı **istekten değil, kendi izinli boyut
listesinden** seçer. "Sarmal kapak üret" demek, modelin varsayılanını
kabul etmektir.

**Yapılacaklar:**

1. Prompta oranı **sayıyla** yazın: *"aspect ratio exactly 1.3955 : 1
   (width : height)"*
2. Model açık boyut kabul ediyorsa **piksel verin**, oran değil.
3. Üretimden **sonra** oranı ölçün — göz yanılır:
   ```bash
   identify -format "%w×%h · oran %[fx:w/h]\n" sanat.png
   ```
4. Ölçülen oran hedeften **%1'den fazla** sapıyorsa **kabul etmeyin**.

## K · Güvenli kırpma

Kırpmak zorundaysanız:

- **merkezden** kırpın (kompozisyonun ağırlık merkezi ortadadır)
- kırpma **%10'u aşıyorsa** sanatı yeniden üretin — bu bir onarım değil,
  kayıptır
- kırpma sonrası dpi'ı **yeniden ölçün**: `kalan piksel ÷ nihai inç`

Bu projede kırpma **%35** oldu; eşiğin üç katından fazla.

## L · Modele verilecek tuval isteği

> Create one continuous full-wrap book cover image.
> **Aspect ratio exactly 1.3955 : 1 (width : height).**
> Target 7745 × 5550 pixels. One single continuous image —
> no panels, no seams, no fold guides, no text.

## M · Model yalnızca sabit oranlar destekliyorsa

Çoğu model 1:1, 3:2, 16:9 gibi sabit oranlar verir. **1,3955 yoktur.**

**En yakın olan 3:2 (1,5) seçilir ve GENİŞ üretilir**, sonra yalnızca
genişlikten kırpılır:

```
3:2 · 8320 × 5547  →  hedef 7745 × 5550
kırpılan genişlik: (8320 − 7745) / 8320 = %6,9   ✓ eşik altında
```

⚠ **Asla dar üretip germeyin.** Germe, geometriyi bozar ve KDP'nin
kabul ettiği ama rafta yanlış duran bir kapak üretir.

## N · Parçalı üretim / sonradan birleştirme

Tek karede yeterli çözünürlük alınamıyorsa:

1. **Aynı sahneyi** üç kez üretmeyin — üç ayrı sahne çıkar.
2. Bir kez üretin, **AI yükselticiyle** büyütün
   (`ASSET_UPSCALING_REPORT.md § 3.2`). Bu projede kapaklar böyle
   işlendi.
3. Parça birleştirme yalnızca sanat **düz bir doku** ise güvenlidir
   (deri, kâğıt dokusu). Nesne taşıyan sahnelerde dikiş görünür.

## O · Tipografi güvenli alanları

Sanat üretilirken **boş bırakılacak** alanlar:

| Bölge | Ne için | Kural |
|---|---|---|
| ÖN üst %22 | başlık | düz, düşük detaylı zemin |
| ÖN alt %15 | yazar | aynı |
| SIRT ortası | sırt yazısı | **kesintisiz malzeme**, panel değil |
| ARKA orta | arka kapak metni | geniş sakin alan |
| ARKA sağ alt | **barkod** | 2,0 × 1,2 in — KDP kendi basar |

⚠ Bu alanlar **çizilmiş kutu olmamalıdır** — sakin ZEMİN olmalıdır.

⭑ Not: bu projede tipografi artık **ölçülen karşıtlıkla** basılıyor
(`04_BUILD/cover_type.py`): mürekkep harfin altındaki piksellerden
seçiliyor ve gerekirse vektör hâle ekleniyor. Yani sakin alan
**yardımcıdır, zorunluluk değildir** — ama sakin alan varsa hâleye
gerek kalmaz ve sonuç daha temiz olur.

## P · Para harcamadan önce doğrulama

```bash
# 1) oranı ölç
identify -format "%w×%h · oran %[fx:w/h]\n" sanat.png

# 2) hedefle karşılaştır (ciltsiz 1.3955 · ciltli 1.3781)
# 3) nihai dpi'ı hesapla
python3 -c "print(GENIŞLIK_PX / 12.908, 'dpi')"
```

**Üçü de geçmeden işleme sokmayın.**

---

## ⭑ İŞ AKIŞI ⭑

```
NİHAİ SAYFA SAYISI            ← iç blok üretilir, SAYILIR (tahmin değil)
        ↓
KDP HESAPLAYICI               ← ciltli için ZORUNLU, ekran görüntüsü saklanır
        ↓
NİHAİ KAPAK İNÇ               ← 12,908 × 9,250  /  14,356 × 10,417
        ↓
HEDEF ORAN                    ← 1,3955  /  1,3781
        ↓
HEDEF PİKSEL (300 dpi)        ← 3872 × 2775  /  4307 × 3125
        ↓
2× AŞIRI ÖRNEKLEME            ← 7745 × 5550  /  8614 × 6250
        ↓
SANATI ÜRET                   ← oran PROMPTA SAYIYLA yazılır
        ↓
ÖLÇ (oran %1 içinde mi)       ← değilse KABUL ETME
        ↓
KIRP / ÖLÇEKLE                ← merkezden, %10'u aşarsa yeniden üret
        ↓
DPI DOĞRULA                   ← kalan piksel ÷ nihai inç ≥ 300
        ↓
NİHAİ KDP SARMALI
```

## Bu projenin gerçek sayıları

| | Ciltsiz | Ciltli |
|---|---|---|
| Sayfa | 263 | 263 |
| Kâğıt | krem | beyaz |
| Sırt | 0,6575 in | 0,781 in |
| Tam kapak | 12,908 × 9,250 in | 14,356 × 10,417 in |
| Oran | 1,3955 | 1,3781 |
| 300 dpi | 3872 × 2775 | 4307 × 3125 |
| **İstenecek (2×)** | **7745 × 5550** | **8614 × 6250** |
| Eldeki sanat | 1840 × 855 (2,152) | aynı |
| Kırpma sonrası | 1193 × 855 → **92 dpi** | daha da düşük |

**Sonuç:** eldeki sarmal her iki sürüm için de yetersizdir. Yeniden
üretilirse yukarıdaki iki piksel hedefi kullanılmalıdır.
