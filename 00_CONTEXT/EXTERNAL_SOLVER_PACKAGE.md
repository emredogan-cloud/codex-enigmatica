# HARİCİ ÇÖZÜCÜ PAKETİ — kurucu devir belgesi

> **A12'nin kapanması için gereken tek şey bu belgedir.**
>
> Sürüm 1.0 · Faz 2 teslimatı · 13 Ağustos 2026
> Protokol: [`SOLVER_TEST_PROTOCOL.md`](SOLVER_TEST_PROTOCOL.md)

---

## 0 · Durum — ⚠ BU İKİNCİ TURDUR

**Birinci tur yapıldı ve ÖLDÜRME KAPISI DÜŞTÜ: 1/5 çözücü bitirdi.**
Baskın bırakma sebebi *"çözemedim"* değil, **"sıkıldım"**dı.

Kapı I **tamamen yeniden tasarlandı** (B1–B6 onaylı) ve elle yapılacak
iş **486 → 184 işleme** indi. İkinci tur bunu ölçer.

| | |
|---|---|
| Birinci tur | ⛔ **1/5 · HARD-STOP** |
| Kapı I yeniden tasarımı | ✅ B1–B6 onaylı · yirmi bulmaca yeniden yazıldı |
| Isınma bölümü (B4) | ✅ üç çözülmüş örnek |
| Çaba bütçesi (`qa_effort`) | ✅ **20/20 bulmaca kendi süre iddiasına sığıyor** |
| **Bulmaca başına kayıt formu** | ✅ **her bulmacanın altında basılı** |
| **İkinci tur kohortu (B6)** | ⚑ **2 dönen + 3 yeni** |
| **A12b — ikinci tur oturumları** | ⛔ **YAPILMADI · 0 / 5** |

### ⚠ Birinci turun tek en pahalı eksiği

Kayıtlar **oturum düzeyindeydi**. Bulmaca başına veri olmadığı için
öldürme kapısının yedi ölçütünden **beşi ölçülemedi** ve yeniden tasarım
hangi bulmacanın düştüğünü **veriyle değil, çaba ölçümüyle** seçmek
zorunda kaldı.

**İkinci turda bu tekrarlanmamalı.** Kayıt formu artık her bulmacanın
altında basılıdır ve doldurulması iki dakika sürer.

> ### Ajan bu testi YAPAMAZ.
> Çözümü zaten bilir; bildiği bir şeyi "bulmak" bulmak değildir.
> `06_REPORTS/solver/` **boştur** ve beş gerçek oturum olana kadar boş kalır.
>
> Bu bir gecikme değil, **kapının kendisidir**.

---

## 1 · Kurucunun yapacağı altı şey

| # | İş | Süre |
|---|---|---|
| 1 | Pilot paketini beş çözücüye ayrı ayrı ulaştırın | 1 saat |
| 2 | Her çözücüye **kendi** kayıt formunu verin | — |
| 3 | Çözücülerin **birbirinden bağımsız** çalıştığını teyit edin | — |
| 4 | Oturumlar bitince ham kayıtları `06_REPORTS/solver/` altına koyun | 30 dk |
| 5 | `founder.externalSolvers.sessionsRecorded` alanını gerçek sayıya çekin | 1 dk |
| 6 | `./04_BUILD/qa_all.sh phase2` koşturun ve **öldürme kapısını okuyun** | 5 dk |

⚠ Altıncı adımın sonucunu **güzelleştirmeyin**. 3/5 sonucu "neredeyse 4"
değildir.

---

## 2 · Çözücü seçimi — iki kural

| Kural | Değer | Neden |
|---|---|---|
| Sayı | **5** | Öldürme kapısının istatistiksel tabanı |
| Bağımsızlık | **mutlak** | Birbirine ipucu veren iki çözücü **bir** çözücüdür |
| **Tür çeşitliliği** | **≥ 2 kişi bu türü ilk kez alıyor** | ⚠ aşağı |
| Kimlik | `solver-01` … `solver-05` | Ad depoya **girmez** |

### ⚠ Neden en az ikisi bu rafı ilk kez almalı

Beş escape-room emektarı, kurucunun başarmasını **isteyen** beş kişidir ve
perakende okurun kitabı **iade ettiği** yerde ısrarla devam ederler. İade
eden okur hiçbir veri satırı üretmez — yani en önemli başarısızlık sinyali
ölçümün dışında kalır.

Bu kural karşılanmıyorsa öldürme kapısı **iyimser** ölçer ve rapor bunu
açıkça yazmak zorundadır.

---

## 3 · ⚠ Levha koşulu — A veya B, üçüncüsü yok

Pilotun 20 bulmacasından **9'u levha taşır**, ikisinde veri **levhanın
içindedir**.

> ### Bir bulmaca, YAYIMLANACAĞI NESNEDEN BAŞKA bir şey üzerinde test edilemez.

| Seçenek | Ne yapılır | Sonuç |
|---|---|---|
| **A** | Pilot levhalar + araçlar levhası **kâğıda basılır** ve çözücüye kâğıt verilir | Kapı mekaniği **kapsıyor** |
| **B** | Ekranda test edilir | Kapı mekaniği levhaları **kapsamıyor** — rapor bunu **açıkça yazar** |

**Öneri: A.** Pilot levhaları bu fazda **gravür değil, tipografik
şekildir** — yani lazer yazıcıdan çıkan bir A4 sayfası, nihai nesneye POD
provasından çok daha yakındır. Maliyet: on sayfa baskı.

⚠ Ama A seçeneği bile **POD provası değildir**. Gravür levhaların baskı
davranışı Faz 5'te ölçülür. Üç durumu asla birleştirmeyin:

```
SCREEN-TESTED            ekranda çözüldü            → ön eleme
PAPER-TESTED             lazer baskıda çözüldü      → pilot için yeterli
PHYSICAL-PROOF-VALIDATED POD prova kopyada ölçüldü  → Faz 5 · YAPILMADI
```

---

## 4 · Çözücü ne görür, ne görmez

| Görür | Görmez |
|---|---|
| Çerçeve anlatı · **sözleşme sayfası** · **araçlar levhası** (Çizelge A–E) | Çözümler |
| Kapı I'in 20 bulmacası, kitaptaki sırayla | Çözüm yolları |
| Üç kademeli ipuçları — **ayrı bir zarfta** | Alternatif çözüm analizi |
| Cevap biçimi kuralı | Tasarım kayıtları |
| Kayıt formu ve zaman damgası aracı | Diğer çözücülerin kayıtları |

⚠ **İpuçları ayrı zarfta.** Kitapta ters basılacaklar; pilotta bu mümkün
değil, o yüzden fiziksel olarak ayrılırlar. Kazayla görülen bir ipucu
ölçümü bozar ve o bulmacanın verisi **çöpe gider**.

---

## 5 · Kayıt formu — bulmaca başına

Her çözücü, **her bulmaca için** şunu doldurur. Boş bırakılan bir alan
eksik veri değil, **ölçülmemiş bir kapıdır**.

```
bulmaca            : g1-0__
başlangıç damgası  : SS:DD          ← öz-bildirim DEĞİL, saate bakarak
bitiş damgası      : SS:DD
sonuç              : çözdüm | ipuçlarıyla çözdüm | çözemedim
bakılan ipuçlar    : [ ] 1. kademe  [ ] 2. kademe  [ ] 3. kademe
verdiğim cevap     : ______________
başka bir cevap    : ______________   ← ⭑ EN DEĞERLİ ALAN ⭑
bu cevaptan eminim : 1 2 3 4 5
belirsiz buldum    : 1 2 3 4 5
nerede takıldım    : ______________________________
```

### ⭑ "Başka bir cevap" alanı neden en değerli

Bir çözücü savunulabilir **ikinci** bir cevap ürettiyse, o bulmacanın
tekilliği **ampirik olarak çürütülmüştür** — `qa_answerspace`'in ölçümü ne
derse desin. Makine yalnızca kendisine öğretilen yordamları sayar; bir
insan öğretilmemiş bir yordam icat edebilir.

`qa_uniqueness § ⑦` bu alanı doldurulmuş her kaydı **kırmızı** yakar ve
bulmaca yeniden yazılır. Bu bir kusur değil, kapının çalışmasıdır.

---

## 6 · Kayıt formu — oturum başına

```
çözücü               : solver-0_
bu türü ilk kez mi   : evet | hayır          ← § 2'nin kuralı
levha koşulu         : A (kâğıt) | B (ekran)
kapıyı bitirdim      : evet | hayır
bitiremediysem slot  : __
bırakma sebebi       : sıkıldım | takıldım | zaman | ilgi kaybı
zorluk               : 1 2 3 4 5
kaç oturumda         : __
Kapı II'yi okur muydum: evet | hayır
```

### ⚠ `bırakma sebebi` neden zorunlu

*Sıkılarak* bırakmak ile *takılarak* bırakmak **iki ayrı kusurdur** ve iki
ayrı düzeltme ister. Birincisi zorluk eğrisi sorunudur, ikincisi
çözülebilirlik sorunu. Ayrım kaydedilmezse ikisi de "başarısız" diye
yazılır ve hiçbiri düzeltilemez.

---

## 7 · Mahremiyet — pazarlık yok

Harici çözücülerin adları **hiçbir koşulda** depoya girmez: ne commit
mesajında, ne rapor dosyasında, ne dosya adında. Eşleştirme tablosu
**yalnızca kurucudadır**.

Kayıtlar yalnızca `solver-01` biçiminde anonim kimlik, süre, ipucu
tüketimi ve sonuç taşır. Şema bu biçimi `pattern` ile **zorunlu kılar**.

Ham kayıtlar `06_REPORTS/solver/` altındadır ve o dizin
`PROTECTED_DIRS`'tedir: orada **takip edilen** bir dosyanın varlığı tek
başına ihlaldir ve `validate_structure` onu kırmızı yakar.

---

## 8 · Sonuçlar geldikten sonra

1. Ham kayıtları `06_REPORTS/solver/solver-0N.json` olarak yazın
2. `01_SOURCE/solutions/gate-1.json` → her bulmacanın `solverTests[]`
   dizisine **anonim** özetleri işleyin (`solverClass: "external"`)
3. `01_SOURCE/puzzle_index.json` → `solverTestCount` ve
   `solverSolvedCount` sayaçlarını gerçek değerlere çekin
4. `project_config.json § founder.externalSolvers.sessionsRecorded` → 5
5. `./04_BUILD/qa_all.sh phase2`

Beşinci adımda `validate_spec § check_test_status` beş şartı **birden**
arar. Sağlanırsa kayıtlar `tested` olur, `status` `validated`e yükselebilir
ve `.gate` `phase2`ye çıkabilir. Sağlanmazsa **hiçbiri olmaz** — ve bu,
belgeyle değil **mekanizmayla** tutulur.

---

## 9 · Öldürme kapısı eşikleri — yoruma yer yok

`project_config.json § killGate` içinde **sayısaldır**.

| Ölçüt | Eşik |
|---|---:|
| Kapı I'i **bitiren** çözücü | **≥ 4 / 5** |
| Hiçbir çözücünün çözemediği bulmaca | **0** |
| **Bulmaca başına bitiren çözücü** | **≥ 2** |
| **3. kademe ipucuna inen çözücü / bulmaca** | **≤ 2** |
| Onaylanmış alternatif çözüm | **0** |
| Medyan tamamlama süresi | **≤ 240 dk** (DNF = tavan) |
| Belirsizlik puanı > 2 olan bulmaca | **0** |

| Sonuç | Karar |
|---|---|
| 4–5 bitirdi · 0 alternatif çözüm | ✅ **DEVAM** |
| 4–5 bitirdi · alternatif çözüm var | ⚠ Yeniden yaz, **testi tekrarla** |
| Tam 3 bitirdi | ⚠ Kapı I yeniden tasarlanır, test tekrarlanır |
| ≤ 2 bitirdi | ⛔ **SERT DURDURMA** — kurucu kararı gerekir |

---

## 10 · Modelin tahmini — ve neden bir tahmin

| | |
|---|---:|
| 20 bulmacanın toplam süresi (model) | 153 dk |
| Oturum yükü (ön madde, ipucu zarfı, kapı aktarımı) | 45 dk |
| **Modellenen oturum** | **198 dk** |
| Öldürme kapısı tavanı | 240 dk |
| Pay | **%17,5** |

⚠ Bu bir **model**dir. Değeri, gerçek süreyle karşılaştırılabilir
olmasındadır. Gerçek medyan 198'in belirgin üstüne çıkarsa zorluk eğrisi
kırıktır — sayısal eşiği geçse bile.
