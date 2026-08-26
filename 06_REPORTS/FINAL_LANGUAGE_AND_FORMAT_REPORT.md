# NİHAİ DİL VE FORMAT RAPORU

**Tarih:** 26 Ağustos 2026

> # ⛔ TEK BLOKLAYICI: DİL
>
> Üç formatın **dosyaları üretildi ve geçerlidir**. Ama ticari kitabın
> içeriği hâlâ **TÜRKÇEDİR** ve kurucu kararı İngilizce olmasını
> gerektiriyor. Ölçülen: **9.533 Türkçe sözcük** ticari yüzeyde.
>
> **Bu dönüşüm bir çeviri işi değildir** — § 2'de neden.

---

## 1 · Dil kapısı ne buldu

Yeni kapı: `04_BUILD/qa_language.py` (yönerge § 4). Ticari yüzeyi
tarar, kurucuya bakan Türkçe belgeleri **muaf tutar**, özel adları
metadata'dan okuyup eler.

| Yüzey | Türkçe sözcük | Durum |
|---|---:|---|
| Ürün metadatası (başlık, alt başlık, açıklama, anahtar kelime, BISAC) | **0** | ✅ İngilizce |
| A+ başlık ve gövde metni | **0** | ✅ İngilizce |
| Ciltsiz kapak | **0** | ✅ İngilizce |
| Ciltli kapak | **0** | ✅ İngilizce |
| **Ciltsiz iç blok** | **3.221** | ⛔ TÜRKÇE |
| **Ciltli iç blok** | **3.221** | ⛔ TÜRKÇE |
| **Kindle EPUB** | **3.091** | ⛔ TÜRKÇE |

Yani **ajanın ürettiği her ticari yüzey İngilizcedir**; Türkçe olan
KİTABIN KENDİ İÇERİĞİDİR.

## 2 · ⭑ Dönüşüm neden yapılmadı ⭑

Yönerge şunu söylüyor ve haklı:

> *"DO NOT merely translate the visible prose mechanically if
> translation would change puzzle mechanics."*
> *"If English conversion changes any puzzle-bearing text: REBUILD THE
> AFFECTED PUZZLE DATA FROM SOURCE."*

Kaynaktan yeniden inşa **gerçekten gereklidir** ve ölçüsü şudur:

| Kalem | Ölçü |
|---|---:|
| Çevrilecek metin | **64.598 kelime** |
| Üreteç kodu | **7.706 satır** · 23 dosya |
| Türkçe alfabe | **29 harf** |
| İngilizce alfabe | **26 harf** |
| Yeniden üretilecek şifreli dize | **hepsi** |
| Yeniden çözülecek cevap ataması | **101** |
| Geçersizleşecek gravür | **~94** |

### Alfabe neden her şeyi değiştirir

`04_BUILD/english_readiness.py` bunu zaten ölçüyor:

```
Türkçe   29 harf → 6 grup (5·5+4)
İngilizce 26 harf → 6 grup (5·5+1)   ⚠ GRUP YAPISI DEĞİŞİR
kaydırma uzayı 28 → 25 · yansıma ekseni 29 → 26
⇒ şifreli dizelerin TAMAMI yeniden üretilir
⇒ grup koşuluna dayanan kısıt bulmacaları YENİDEN TASARLANIR
```

### Ve cevaplar elle seçilmiyor

`gate_common.assign()` bir geri izlemeli çözücüdür: her cevap **kapı
ifadesine belirli bir harfi** verir (meta-mister buna bağlıdır) ve aile
başına uzunluk kısıtı vardır. İngilizce cevaplar için **11 tematik
katalog** (toplam ~350 sözcük) yeniden yazılmalı ve çözücü yeniden
koşturulmalıdır.

⚠ Kataloğun **uzunluğu da bulmaca verisidir**: Kapı V'in mekanizması
çizelge satır sayılarını aritmetik işlenen olarak kullanır
(`structure_pair`). Bir kataloğa sözcük eklemek Kapı V'i değiştirir.

### Gravürler

Cevap değişince şekil değişir, şekil değişince levha değişir.
**Teslim edilen 103 gravürün ~94'ü geçersizleşir** ve yeniden
üretilmesi gerekir.

## 3 · ⭑ İYİ HABER: üreteç ONARILDI ⭑

Bu oturumda Kapı 3-4-5 üreteci **çalışır hâle getirildi**.

Kırık: `structure_pair()` üç terimli aramada `a−b−c` ve `a+b−c`
deniyordu ama **`a+b+c` denemiyordu**. `g5-013` hedef 46 istiyor ve
`29+12+5 = 46` tam olarak bunu veriyor. Tek eksik kural yüzünden
`build_all()` hiç koşmuyordu.

Onarımdan sonra üreteç **60 cevabın 56'sını birebir yeniden üretiyor**.
Dört cevap farklı çıkıyor — ve bunlardan biri **`g3-017`**, yani commit
mesajına sızan cevabın sahibi.

⭑ **Bu şu demektir:** dil dönüşümü yapıldığında bütün cevaplar yeniden
atanacak ve **sızan dize artık bir cevap olmayacak** — ikinci
bloklayıcı, birincisi çözülünce kendiliğinden kapanır.

## 4 · Bu oturumda ÜRETİLENLER

| | Ciltsiz | Ciltli | Kindle |
|---|---:|---:|---:|
| Sayfa / bölüm | **264** | **264** | 18 bölüm |
| İç kenar payı | 0,500 in | **0,625 in** | — |
| Sırt | 0,6600 in | **0,7833 in** | — |
| Kapak | 12,910 × 9,250 | **14,359 × 10,417** | 1600 × 2560 |
| Menteşe | — | **0,394 in** | — |
| Dosya | 71,7 MB | 68,6 MB | 46,0 MB |

Hepsi çift sayfa (yaprak tam), yazı tipleri gömülü, sağlama toplamları
yazılı. **Preflight 30 denetim yeşil.**

### Kapak tipografisi düzeltildi

Şikâyet: *"çok saydam, zor okunuyor."* Ölçüldü ve doğrulandı — en zayıf
satır **1,47 : 1** karşıtlıktaydı (WCAG tabanı 4,5).

İki yaklaşım denendi:

1. **Raster perde** — karşıtlığı 4,7'ye çıkardı ama gözle bakınca
   metnin arkasında **dikdörtgen bant** olarak okunuyordu; yönergenin
   § B'de yasakladığı şey. *Ölçü düzeldi, tasarım bozuldu.*
2. **⭑ Vektör hâle ⭑** — harfin kendi şeklini izleyen ince dış çizgi.
   Kutusu yok, sanat tamamen görünür, kenar karşıtlığı zeminden
   bağımsız **17,69 : 1**.

Mürekkep artık **harfin altındaki piksellerden** seçiliyor (kutu
ortalamasından değil) ve açık zeminde koyu, koyu zeminde açık oluyor.

## 5 · Ekonomi (ölçülen 264 sayfadan)

| | Liste | Maliyet | **Telif** | Marj |
|---|---:|---:|---:|---:|
| Ciltsiz | 19,99 $ | 4,02 $ | **7,98 $** | %39,9 |
| Ciltli | 29,99 $ | 8,82 $ | **9,18 $** | %30,6 |
| Kindle (%35) | 9,99 $ | — | **3,50 $** | %35 |
| Kindle (%70) | 9,99 $ | 6,90 $ teslimat | **0,09 $** | %0,9 |

⭑ **Kindle'da %35 planı seçilmeli** — %70 planı 46 MB'lık dosyada
kitap başına 3,41 $ kaybettirir. Sınır ~23,3 MB.

BRIEF § 7 hipotezi 208 sayfaya dayanıyordu; ölçülen 264 sayfa ciltsizde
maliyeti 0,52 $, ciltlide 0,67 $ artırdı.

## 6 · Kurucuya kalanlar

**Bloklayıcı:**
1. **Dil dönüşümü kararı** — § 2'deki ölçüyü gördükten sonra: tam
   yeniden inşa mı, yoksa Türkçe sürüm mü?
2. Cevap sızıntısı — dil dönüşümü yapılırsa **kendiliğinden kapanır**

**Yalnızca insanın yapabileceği:** KDP paneli · Previewer onayı ·
**yapay zekâ beyanı** · ISBN kararı · fiziksel POD provası (A9) ·
Publish · A+ moderasyonu · **Kindle telif planı seçimi (%35)**

**Ertelenen:** sarmal sanatın 1,40:1 ve ≥3900 px yeniden üretimi ·
14 levhanın üslup uyumu · hesaplayıcının 264 sayfayla tazelenmesi

## 7 · Değişmeyen

`externalValidation = founder_override_partial` · `sessionsPerformed = 0`
· `humanValidationPassed = false` · **HARD-STOP**.

**Bu kitap hiçbir insanın elinde çözülmedi.** Hiçbir şey yüklenmedi,
yayımlanmadı, moderasyona gönderilmedi, prova sipariş edilmedi.
