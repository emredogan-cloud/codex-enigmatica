# FAZ 4 RAPORU — Kapı III–V + Meta-Mister

> **24 Ağustos 2026** · Kapı: `phase4` · Dal: `main`
>
> ## ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING
>
> | | |
> |---|---|
> | Ölçülen öldürme kapısı | ⛔ **HARD-STOP** (1/5) — **değişmedi** |
> | Yapılan harici oturum (`sessionsPerformed`) | **0** |
> | İnsan doğrulaması geçti mi (`humanValidationPassed`) | **HAYIR** |
> | Dış doğrulama durumu (`externalValidation`) | `founder_override_partial` |
> | Faz 4 girişi ve çıkışı | ⚑ **KURUCU GEÇERSİZ KILMASI** |
>
> ⭑ **ÜÇ ŞEY BİRBİRİNİN YERİNE GEÇMEZ:**
> **ÖLÇÜLEN** (HARD-STOP) · **GEÇERSİZ KILINAN** (faz geçişi) ·
> **HENÜZ DOĞRULANMAMIŞ** (harici insan testi).
>
> Bu faz **"insan tarafından test edilmiş", "insan tarafından
> doğrulanmış" ya da "harici olarak onaylanmış" diye anılamaz.**
> `06_REPORTS/solver/` **boştur** ve gerçek oturumlar gelene kadar boş
> kalır. Geçersiz kılma yalnızca **ilerlemeye** izin verir; ölçümü
> **PASS'a çevirmez** ve `kill_gate.py` kararı her koşuda HARD-STOP
> olarak yazdırmaya devam eder.

---

## 1 · Bulmaca sayıları

| | Ölçülen | Hedef |
|---|---:|---:|
| **Yazılmış taslak (toplam)** | **101** | 100 + meta |
| Kapı I · The Threshold (★) | 20 | 20 |
| Kapı II · The Menagerie (★★) | 20 | 20 |
| **Kapı III · The Calendar (★★)** | **20** | 20 |
| **Kapı IV · The Labyrinth (★★★)** | **20** | 20 |
| **Kapı V · The Mirror (★★★)** | **20** | 20 |
| **Meta-mister (Son Soru)** | **1** | 1 |
| Aday havuzu | 151 | ≥130 |
| **Doğrulanmış (`validated`)** | **0** | 100 |

⚠ `status` alanının tamamı **`drafted`**tir. Hiçbiri `tested` değildir ve
`validate_spec` kurucu onayı yokken bir kaydın `tested` olmasına **izin
vermez** — sahte test kaydı üretilemez.

---

## 2 · Isınma örnekleri (Faz 4 bloklayıcısı ② — kapandı)

Faz 4 dokuz yeni mekanizma getirdi ve **dokuzunun da örneği yoktu**;
`qa_experience § 7` haklı olarak kırmızı yanıyordu.

| örnek | öğrettiği mekanizma | durduğu yer |
|---|---|---|
| w9 | `numeral-system` | Kapı III açılışı |
| w10 | `cyclic-calendar` | Kapı III açılışı |
| w11 | `polyalphabetic-cipher` | Kapı III açılışı |
| w12 | `path-graph` | Kapı IV açılışı |
| w13 | `layered-chain` | Kapı IV açılışı |
| w14 | `back-reference` | Kapı IV açılışı |
| w15 | `book-structure` | Kapı V açılışı |
| w16 | `narrative-embedded` | Kapı V açılışı |
| w17 | `meta-synthesis` | Son Soru öncesi |

**Ölçülen: 17 örnek · 17/17 mekanizma öğretiliyor.**

Her örnek beş parçadır: mekanizma tanıtımı · okurun kapıda göreceği
şeklin aynısı · çözülmüş adımlar (**cevap görünür**) · kısa açıklama ·
"neye dikkat edilecek". Fazlası yoktur (§ 3 · *no unnecessary homework*).

⭑ **Ve ön maddeye konmadılar** (K37): Kapı IV'ün dersini ön maddeye
koymak, okura otuz sayfa önce göremeyeceği bir şeyi anlatmaktır. Her
örnek kendi kapısının açılışında durur.

⚠ **Bir örnek, öğretmeye çalıştığı şeyin yanlış olduğunu gösteriyordu.**
Son sorunun ısınması "sondan sayınca sözcük çıkar" diyor ama uydurma
sözleri `ÜĞU` veriyordu. Sözler artık **aranarak** seçiliyor (baştan
`DĞR` — sözcük değil; sondan `ATA` — sözcük) ve seçim üretim anında
doğrulanıyor.

---

## 3 · Nihai aha politikası (Faz 4 bloklayıcısı ① — kapandı)

Ayrıntı: **`DECISIONS.md § K36`** · Eşikler:
**`project_config.json § experience`** · Fikstürler: **`selftest § ⑨`**

### Sorun ölçüldü, varsayılmadı

Kitap geneli `ahaScore` ortancası **4,0**'dı ve **yeşildi**. Kapı kapı
bakıldığında sebep çıktı: Kapı III–V'te öğretilmiş bir mekanizmanın
**tekrarına** da 4 ve 5 yazılmıştı. `g3-007`, `g3-011` ve `g3-015`,
`g3-001` ile **kelimesi kelimesine aynı talimatı**, aynı kısıtları ve
aynı adım sayısını taşıyor — yalnızca verileri farklı.

**Kitap geneli ortanca, kapı düzeyindeki şişmeyi gizliyordu.**

### Karar

**① Tavan artık ölçülüyor.** Yazar tavanın altına inebilir, üstüne
çıkamaz:

| durum | tavan |
|---|---|
| mekanizmanın **ilk kullanımı** | **5** — keşif |
| tekrar · çıkarım oranı ilk kullanımdan **büyük** | **4** — derinleşme |
| tekrar · çıkarım oranı büyük **değil** | **3** — yordam |

**② Eşik kapı bazında ve kapının türüne göre:**

    keşif kapıları (I · II)      aha ortancası ≥ 4
    akıcılık kapıları (III–V)    aha ortancası ≥ 3

**③ Yenilikten vazgeçilen yere çıkarım konur.** Ölçüt uydurulmadı,
veride zaten duruyordu:

    çıkarım oranı = bildirilen dakika ÷ ölçülen elle işlem

### Ölçülen sonuç

| kapı | tür | aha ortancası | çıkarım oranı | yeni/derin |
|---|---|---:|---:|---:|
| I · Threshold | keşif | **4,0** | 1,00 | 13 |
| II · Menagerie | keşif | **4,0** | 1,27 | 18 |
| III · Calendar | akıcılık | **3,0** | **2,32** | 15 |
| IV · Labyrinth | akıcılık | **3,0** | **3,43** | 15 |
| V · Mirror | akıcılık | **3,5** | **4,42** | 14 |
| Son Soru | — | 5,0 | 6,00 | 1 |

Elle işlem beş kapıda da **6–8 EU** bandında sabittir; artan tek şey
düşünmedir. Akıcılık kapıları için oran tabanı **2,0** ve oran kapıdan
kapıya **yükselmek zorunda**. Kapı başına en az **4** ilk kullanım ya da
ölçülmüş derinleşme (ölçülen 15 · 15 · 14).

### On puan DÜŞÜRÜLDÜ — hiçbiri şişirilmedi

`g3-007` 4→3 · `g3-011` 4→3 · `g4-007` 4→3 · `g4-008` 4→3 ·
`g4-012` 4→3 · `g4-015` 5→3 · `g5-012` 4→3 · `g5-013` 5→4 ·
`g5-014` 4→3 · `g5-018` 5→4

Aynı mekanizma koruması **kaldırılmadı, SERTLEŞTİRİLDİ**: tekrar artık
5 **alamaz** ve 4'ü ancak **ölçülmüş** bir derinleşmeyle alır.

> ⭑ Korunan değişmez: *daha sonraki bir bulmaca öğrenilmiş bir
> mekanizmayı DERİNLEŞTİREBİLİR — ama yeni bir keşif ilan EDEMEZ.*

---

## 4 · Meta-mister

`04_BUILD/qa_meta.py` — **29 denetim · hepsi yeşil** (K38).

| denetim | sonuç |
|---|---|
| Beş kapının **beşi de** katkı veriyor | ✅ `g1-020 … g5-020` |
| Her katkı o kapının **kapı bulmacasından** geliyor | ✅ |
| Bildirilen kapı sözü o kapının **gerçek çıktısı** | ✅ 5/5 |
| İleri referans | ✅ yok |
| Döngü (son sorunun cevabını kullanan bulmaca) | ✅ yok |
| Cevap basılı sözlerden **türetilebiliyor** | ✅ |
| Her kapı **tam olarak bir** harf veriyor | ✅ 5 harf / 5 kapı |
| **Basit birleştirme değil** | ✅ cevap birleşik dizede (ve tersinde) okunmuyor |
| Cevap "ilk harfler" / "son harfler" değil | ✅ |
| Konumlar sabit bir sayı değil | ✅ `[1,2,3,4,5]` |
| **Cevap kitapta YOK** | ✅ 101 sayfa · 15 basılı çizelge · 17 ısınma · 5 açılış tarandı |
| Cevap sayfa başlıklarında yok | ✅ |
| Aday listesinde **tam olarak bir** üye kabul ediliyor | ✅ 9 aday |
| Aday listesi kitapta **basılı değil** | ✅ ispat alanı |
| Kapı sırası manuscript sırasıyla aynı | ✅ |

⚠ **Ve bu kapının kendi sızıntı denetimleri ilk yazımında sessizce yeşil
yanıyordu.** Aranan anahtar büyük harfti, aranan metin `pl.squeeze` ile
küçük harfe indirilmiş ve Türkçe ı/İ/I katlaması yapılmıştı: iki dize
hiçbir zaman eşleşemezdi. **Kusuru fikstürler yakaladı** — kapı üretim
verisinde yeşildi ve öyle kalacaktı.

---

## 5 · Çaba istatistikleri

| | Ölçülen | Tavan |
|---|---:|---:|
| Toplam elle işlem (beklenen) | **686,3 EU** | — |
| Toplam elle işlem (en kötü) | 766,8 EU | — |
| Bildirilen süre | 1786 dk | — |
| Elle işin süredeki payı | **%12,8** | %33 |
| Tavanı aşan bulmaca (`condemned`) | **0** | 0 |
| Kapı başına elle işlem ortancası | **6–8 EU** (beş kapıda da) | — |

⭑ **Kapı III–V'te elle iş ARTMADI.** ★'dan ★★★'e giderken artan tek şey
çıkarımdır — kitabın kurucu felsefesi budur ve artık bir sayıdır.

---

## 6 · Tekrar istatistikleri

| | Ölçülen | Tavan |
|---|---:|---:|
| `repetitionBurden` ortancası | **2,0** | 2 |
| Tavanı aşan bulmaca (kapı bulmacası hariç) | **0** | 0 |
| Ödülsüz bulmaca (`ahaScore` ≤ 2) | **0** | 2 |
| Uzun eziyet dizisi (kapı içinde ≥4 ardışık ağır) | **0** | 0 |
| Küçük zafer payı | **%100** | ≥%40 |
| Ayrı süre değeri | 25 | ≥3/kapı |

---

## 7 · Cevap uzayı

| | Ölçülen |
|---|---:|
| Bağımsız doğrulanmış bulmaca | **101 / 101** |
| Üretilen ve elenen aday dize | **4 762** |
| En küçük cevap uzayı | 9 |
| En büyük cevap uzayı | 60 |
| Yakın-ıska aday | 571 |
| **Onaylanmış alternatif çözüm** | **0** |
| Belirsizlik puanı > 2 | **0** |
| İpucu (3 kademe) | **303** · hiçbiri cevabı içermiyor |

---

## 8 · Sızıntı denetimleri

### Kanarya (`qa_solution_leak`)
✅ **4 denetim yeşil · kip A · 96 takip edilen dosya tarandı.**
Altı harf ve üzeri her cevap, düz ve **ters** biçimde, takip edilen
dosyalarda ve son iki yüz commit mesajında arandı. Bulunan: **yok**.
Kanarya commit'ten **önce** koşturuldu (K34'ün süreç dersi).

### Görsel çapraz sayfa denetimi — ⭑ İKİ GERÇEK SIZINTI BULUNDU VE ONARILDI ⭑

Ölçüm değil, **render edilmiş sayfaların taranması** bunu buldu:

> **Anahtarlı alfabe levhası anahtar sözcüğü satırın başında BASAR** ve
> bulmacanın ipucu bunu okura açıkça söyler (*"alt satırın başında bir
> sözcük vardır"*). İki kapının anahtarı bir CEVAPTI:
>
> | levha | eski anahtarı kimin cevabıydı |
> |---|---|
> | `g3-019` | **`g3-007`** |
> | `g5-019` | **`g5-013`** |
>
> ⚠ Sözcüklerin kendisi burada **yazılmaz**: anahtarlar değişti ama o
> iki sözcük **hâlâ birer cevaptır** ve bu rapor takip edilen bir
> dosyadır. Kanarya bu raporun ilk taslağını sızıntı olarak yakaladı —
> haklıydı (K34).
>
> Yani o iki levha, iki bulmacayı **bedava veriyordu**.

**Kök sebep:** anahtarlar `assign()` cevapları dağıtmadan **önce** elle
seçilmişti ve hiçbir yerde çakışma denetimi yoktu.

**Onarım:** yeni anahtarlar **hiçbir katalogun üyesi değildir** — cevap havuzuna hiç giremezler — ve
çakışma artık **üretim anında** denetlenir (`assert_keys_clean`).

### Kalan çakışmalar — incelendi, sızıntı DEĞİL

| görünüm | gerçek |
|---|---|
| `KAPI` · `g1-007` çizelge başlığı ve `meta-001` levhası | sütun **başlığı** olarak "kapı" sözcüğü — kitabın yapısal ismi |
| `AYNA` · `g4-002`, `g5-006`, `g5-014` | *"ayna ekseni"* — dönüşümün adı |
| `ASMA` · `g5-003` | `BASMA` sözcüğünün içinde kalan alt dize |

Üçü de dört harflidir ve kanaryanın tabanı (altı harf) onları **bilerek**
görmez — kısa sözcükler olağan nesirle çarpışır. Bulgu K41'de
kayıtlıdır; Kapı I'in cevapları **değiştirilmedi**, çünkü o yirmi
bulmaca ölçülen öldürme kapısının kanıt tabanıdır.

---

## 9 · Görsel denetim

Kapı III, IV ve V'in **bütün levhaları**, son soru, on yedi ısınma
örneği, kapı açılışları ve meta sayfası render edildi ve tarandı.

| denetim | sonuç |
|---|---|
| Eksik glif / denetim karakteri | ✅ **0** |
| Şekilsiz levha atfı (metin/diyagram ayrışması) | ✅ **0** |
| Cevap okuma sırasında görünüyor mu | ✅ `qa_readerpack` 14 denetim yeşil |
| Çapraz sayfa sızıntısı | ⛔ **2 bulundu → onarıldı** (§ 8) |
| **Kutu hizası (kırpılma)** | ⛔ **26 bulundu → onarıldı** |
| Trim taşması (şekil satırı > 66 sütun) | ⚠ **9 satır** — Faz 5'e devredildi |

### Kutu hizası — üç ayrı bir-sütun kayması

| üreteç | kusur | onarım |
|---|---|---|
| `plates2` sınıflama kutusu | ayırıcı satır bir `─` fazla (48 ≠ 47) | 44 → 43 |
| `plates345.sayi_tasi` | içerik satırı bir sütun içeri kayıyordu (43 ≠ 44) | `ljust(w-3)` → `ljust(w-2)` |
| `plates345.katman_tasi` | yalnızca "dize" satırı kısa (47 ≠ 48) | `ljust(35)` → `ljust(36)` |

Bir sütunluk kayma ekranda görünmez, **basılı bir kutuda görünür**.
Ölçüm bunu bulamazdı; sayfaların kendisine bakmak buldu.

### Kalan: trim taşması

Dokuz şekil satırı 66 sütunu aşıyor (67–79). Sekizi anahtarlı alfabenin
iki satırıdır (29 harf × 2 sütun = 67) ve biri Kapı II'nin bir çizelge
başlığıdır (79).

⚠ **Bu Faz 5'in işidir ve orada ölçülecektir**: yol haritası
`qa_plate_readability.py`i Faz 5'e koyar ve basılabilir genişlik dizgi
dondurulmadan **bildirilmiş bir sayı değildir**. Faz 4 bunu ölçtü ve
devretti; sessizce geçmedi.

### Önceki kusurlar — hâlâ kapalı

| kusur | durum |
|---|---|
| Cevap okuma sırasında görünüyordu | ✅ kapalı (`qa_readerpack § ⑫`) |
| İki sayfanın kesişiminden okuma (K35) | ✅ kapalı — üretim anında reddediliyor |
| Raporun kendi cümlesini sızdırması (K34) | ✅ kapalı — kanarya commit'ten önce koşuyor |
| Diyagram/metin ayrışması | ✅ kapalı — şekil ve künye aynı kaynaktan |

---

## 10 · Sayfa modeli — GERÇEK METİNDEN yeniden ölçüldü

### Ölçülen (kapı kapı, ×5 ölçekleme YOK)

| kapı | bulmaca | ısınma | açılış | şekil satırı | **ÖLÇÜLEN** | bütçe |
|---|---:|---:|---:|---:|---:|---:|
| threshold | 1704 | 645 | 56 | 303 | **14,1** | 34 |
| menagerie | 1778 | 108 | 59 | 275 | **12,1** | 34 |
| calendar | 1615 | 282 | 42 | 234 | **11,1** | 34 |
| labyrinth | 1561 | 309 | 36 | 312 | **12,9** | 34 |
| mirror | 1430 | 173 | 36 | 242 | **10,4** | 34 |
| last-question | 132 | 120 | 0 | 28 | **1,4** | 6 |
| **TOPLAM** | **8220** | **1637** | **229** | **1394** | **62,0** | **176** |

| arka / ön madde | ölçülen | bildirilen |
|---|---:|---:|
| İpuçları | 4446 kelime → **12,7** sayfa | 26 |
| Çözümler | 2679 kelime → **7,7** sayfa | 18 |
| Araçlar levhası | 408 satır → **3,2** sayfa | **4** |
| **Toplam kelime** | **17 211** | ~34 000 hedef |

### Model değişti: 236 → **238**

**Neden:** araçlar levhası 2 sayfaya sığmıyordu. Faz 1'de dört
çizelgeydi; Faz 4 sekiz çizelge daha ekledi (H·I·J·K·L·M·N·O). Kısaltmak
**seçenek değildi**: her çizelge bir kapının **cevap uzayıdır** (K22) ve
bir satırı silmek o satırı kullanan bulmacayı çözülemez yapar.

Hedef 230 ± %6 (216–244) → **238 içeride**.

⚠ **Dokuz yeni ısınma örneği sayfa sayısını DEĞİŞTİRMEDİ**: ölçülen 5,1
sayfa, kapı bütçelerinin içinde kaldı (kapı metni 10,4–14,1 / 34).
Hiçbir içerik sayıyı tutturmak için **kısaltılmadı**.

> ⚠ **Yol haritasıyla bir fark var ve gizlenmiyor:** Faz 4 § 11 PASS
> ölçütü *"sayfa modeli 208 ± %6"* diyor. O sayı **A8/K17'den önceki**
> hedeftir; kurucu sayfa hedefini **230**'a çıkardı ve `page_budget.py`
> onu denetler. Yol haritası metni bu noktada bayattır.

⭑ **Ölçülen metin bütçenin çok altındadır (62 / 176) ve bu bir hata
değildir:** bu kitapta her bulmacanın bir **gravür levhası** vardır ve
kalan payı levhalar doldurur (112 levha). Pay Faz 5'te dizgi
dondurulurken ölçülerek kapanacaktır (K12).

⚠ **Kelime sayısı hedefin altında: 17 211 / ~34 000.** Sebep tasarımdır:
içerik nesirden **basılı çizelgelere ve levhalara** taşındı (K22). Bu bir
FAIL ölçütü değildir (Faz 4 § 12'de kelime yoktur) ama Faz 5'in ön madde
ve çerçeve anlatısı yazılırken bilinmesi gereken bir sayıdır.

---

## 11 · Kalite kapıları — Faz 4 tam koşusu

`./04_BUILD/qa_all.sh` · kapı `phase4`

| kapı | sonuç |
|---|---|
| veri bütünlüğü ve kapsam (`validate_spec`) | ✅ 58 denetim |
| depo ve belge bütünlüğü (`validate_structure`) | ✅ 98 denetim |
| **KAPILARIN KENDİ TESTİ** (`selftest`) | ✅ **213 denetim** (195 → 213) |
| araştırma kayıtları | ✅ 9 denetim · 15 künye · 15 referanslı |
| bağımlılık grafiği (DAG) | ✅ 16 denetim · döngüsüz |
| mekanizma çeşitliliği | ✅ 39 denetim · 17 aile |
| ⭑ çözüm kanaryası ⭑ | ✅ 4 denetim · 96 dosya |
| ⭑ cevap uzayı ⭑ | ✅ 10 denetim · 101 bulmaca · 4762 aday |
| devir ve hata davranışı | ✅ 13 denetim · yayılma yarıçapı ≤1 |
| ⭑ çaba bütçesi ⭑ | ✅ 4 denetim · 686 EU |
| ⭑ deneyim ⭑ (K36) | ✅ **18 denetim** (15 → 18) |
| paketten çözme | ✅ |
| ⭑ levha verisi ⭑ | ✅ 5 denetim |
| ⭑ okur paketi ⭑ | ✅ 14 denetim · 101 sayfa |
| çözülebilirlik | ✅ 11 denetim · 404 adım |
| alternatif çözüm | ✅ 9 denetim · 404 aday |
| ipucu bütünlüğü | ✅ 9 denetim · 303 ipucu |
| **meta-mister bütünlüğü** (`qa_meta` · YENİ) | ✅ **29 denetim** |
| İngilizce dönüşüm hazırlığı | ⚑ başlatılmadı (A12 bekliyor) |
| ⛔ öldürme kapısı ⛔ | ⛔ **HARD-STOP** — geçersiz kılmayla ilerlendi |
| sayfa bütçesi | ✅ 10 denetim · 238 sayfa · 112 levha |
| sayfa ölçümü (`pilot_pages`) | ✅ 4 denetim · 6 kapı |
| üretilen belgeler güncel | ✅ |

⚠ **Bu tabloda ilk yazımda olmayan bir satır vardı** ("KDP metadata
paketi"). `04_BUILD/metadata.py` **henüz yoktur** ve `qa_all.sh` onu
sessizce atlar — yani o kapı koşmadı. Satır kaldırıldı. `metadata.py`,
`interior.py` ve `editions.py` **Faz 5–6 teslimatlarıdır**.

**Kırmızı kapı: yok** (öldürme kapısının ölçülen kararı hariç — o bir
kalite ölçümü değil, bir **karardır** ve kurucu geçersiz kılmasıyla
ilerlemeye izin verir).

### Yeni fikstürler — her yeni kural kırık bir kurguda ÇÖKÜYOR

`selftest § ⑨` · 16 yeni denetim:

**Meta (11):** katkısız kapı · ileri referans · döngü · üretilemeyen kapı
sözü · birleştirmeyle okunan cevap · sayfada basılı cevap · başlıkta
cevap · ısınmada cevap · kitapta basılı aday listesi · bozuk kapı sırası
· sabit konumlar.

**K36 (5):** temiz kurgu geçer · tekrara 5 verilirse kırmızı · ölçülmüş
derinleşme olmadan 4 verilirse kırmızı · yenilik tabanı tutmuyorsa
kırmızı · çıkarım oranı tabanı tutmuyorsa kırmızı.

---

## 12 · Git / CI

| | |
|---|---|
| Dal | `main` |
| Kapı dosyası (`.gate`) | `phase3` → **`phase4`** |
| Yerel `qa_all.sh` | ✅ **YEŞİL** |
| Uzak GitHub Actions | § 14'e bakınız |

---

## 13 · Faz 4 · Definition of Done

Yol haritası Faz 4 § 10:

| # | Madde | Durum |
|---|---|---|
| 1 | **100 bulmaca yazıldı** | ✅ **101** (100 + meta) |
| 1b | **…ve doğrulandı** | ⛔ **YAPILMADI** — 0 harici oturum · ⚑ geçersiz kılma |
| 2 | Meta-mister beş kapıya bağlandı ve **mekanik olarak doğrulandı** | ✅ `qa_meta` 29 denetim |
| 3 | 300 ipucu tamam; **hiçbiri cevabı içermiyor** | ✅ **303** · `qa_hints` yeşil |
| 4 | Alternatif çözüm analizi 100/100 | ✅ **101/101** · onaylanmış alternatif **0** |
| 5 | DAG döngüsüz; ileri referans yok | ✅ `qa_dependency` + `qa_meta` |
| 6 | **Manuscript özünde tamam** | ✅ 101 sayfa · 17 ısınma · 5 kapı açılışı |
| 7 | CI **YEŞİL** · `.gate` → `phase4` | ✅ / ✅ |

### PASS ölçütleri (§ 11)

| ölçüt | sonuç |
|---|---|
| 100 bulmaca · 5 kapı | ✅ |
| 100/100 deterministik, tek cevaplı, belirsizlik ≤2 | ✅ 101/101 |
| Meta-mister doğrulandı | ✅ |
| Sayfa modeli | ✅ **238** (hedef 230 ± %6) · ⚠ yol haritasındaki 208 bayat (K17/A8) |

### FAIL ölçütleri (§ 12) — hiçbiri gerçekleşmedi

| ölçüt | sonuç |
|---|---|
| Bulmaca < 100 | ✅ hayır (101) |
| Meta-mister bir kapının çıktısını kullanmıyor | ✅ hayır — beşi de kullanılıyor |
| Son sorunun cevabı kitapta bulunuyor | ✅ hayır — `qa_meta § ⑦` |

### ⛔ Kapanmayan tek madde

**1b — "…ve doğrulandı".** Bu madde **ajan tarafından yapılamaz**.
Kapanması için gereken tek şey **A12b**: harici çözücü oturumları.

---

## 14 · Kurucuya kalan işler

| # | Ne | Neden ajan yapamaz |
|---|---|---|
| **A12b** | ⭑ **Harici çözücü oturumları** ⭑ | İnsan gerekir. Sahte kayıt üretilmez ve `validate_spec` üretilmesine izin vermez. |
| **A9** | Levha POD provası | Fiziksel baskı |
| A2 | 5 kapı teması onayı | Kurucu kararı |
| A4 | Doğrulama sayfası barındırma | Hesap/altyapı |
| A5 | Kalibre `STYLE.md` onayı | Kurucu kararı |
| A6 | Yazar biyografisi | Kurucu metni |
| A7 | Bulmaca başına doğrulama biçimi | Kurucu kararı |
| A10 | Faz 3'e ikinci öldürme kapısı | Kurucu kararı |
| — | 15 künyenin insan gözüyle doğrulanması | Kaynak erişimi |

---

## 15 · Faz 4'ün yeni kararları

| # | Karar |
|---|---|
| **K36** | Aha ölçeklenmez, **çıkarım ölçeklenir** — tavan ölçülür, eşik kapı bazındadır |
| **K37** | Isınma ön maddede bitmez — dersi **kendi kapısına** götürür |
| **K38** | Son sorunun cevabı kitapta **bulunmamalıdır** — ve bunu bir kapı arar |
| **K39** | Bir kapı, ölçtüğü şeyin **büyüdüğünü** varsaymalıdır |
| **K40** | Okur **dosya anahtarı** görmez |
| **K41** | Kısa cevaplar kitabın **kendi söz dağarcığıyla** çarpışır (§ 8) |

---

*Bu rapor `06_REPORTS/tracked/` altındaki üretilen ölçüm dosyalarından
yazılmıştır. Hiçbir sayı elle tahmin edilmemiştir.*
