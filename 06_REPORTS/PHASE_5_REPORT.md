# FAZ 5 RAPORU — Yakınsama · Levha · Doğrulama Sayfası

> **24 Ağustos 2026** · Kapı: `phase5` · Dal: `faz/5-yakinsama` → `main`
>
> ## ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING
>
> | | |
> |---|---|
> | Ölçülen öldürme kapısı | ⛔ **HARD-STOP** (1/5) — **değişmedi** |
> | Yapılan harici oturum (`sessionsPerformed`) | **0** |
> | İnsan doğrulaması geçti mi (`humanValidationPassed`) | **HAYIR** |
> | Dış doğrulama durumu (`externalValidation`) | `founder_override_partial` |
> | Faz 4 ve Faz 5 girişi/çıkışı | ⚑ **KURUCU GEÇERSİZ KILMASI** |
>
> Bu faz **"insan tarafından test edilmiş", "insan tarafından
> doğrulanmış" ya da "harici olarak onaylanmış" diye anılamaz.**
> `06_REPORTS/solver/` **boştur**. `07_ASSETS/raw/` **boştur** — yüz üç
> gravürün hiçbiri üretilmedi. POD prova **alınmadı**. Doğrulama sayfası
> **canlı değil**.
>
> Geçersiz kılma yalnızca **ilerlemeye** izin verir; ölçümü PASS'a
> çevirmez.

---

## 1 · Faz 4 kapanışı

| | |
|---|---|
| Faz 4 raporu | `06_REPORTS/PHASE_4_REPORT.md` |
| Yerel QA | ✅ bütün kapılar yeşil |
| **Gerçek GitHub Actions** | ✅ **YEŞİL** (dal ve `main`) |
| Birleştirme | `faz/4-kapi-3-5` → `main` · ileri sarma · **açık PR yok** |
| `.gate` | `phase3` → **`phase4`** |
| Kalan tek DoD maddesi | *"…ve doğrulandı"* — **A12b · kurucu işi** |

⚠ Faz 4 raporunda **koşmamış bir kapı yeşil sayılmıştı** ("KDP metadata
paketi"); `metadata.py` o gün yoktu ve `qa_all.sh` onu sessizce
atlıyordu. Satır kaldırıldı ve neden kaldırıldığı yazıldı. *Koşmayan bir
kapının yeşili yoktur.*

---

## 2 · Faz 5 işi

### Yazıldı

| | Ölçülen |
|---|---|
| **Ön madde** | başlık · künye · çerçeve anlatı · **SÖZLEŞME SAYFASI** (dört söz) · araçlar girişi · ısınma girişi |
| **Arka madde** | ipucu girişi · çözüm girişi · **şifre referansı** (10 dizge) · kaynaklar · kolofon |
| **Çerçeve anlatının kapanışı** | son sorudan sonra okunan metin |
| Toplam kelime | **17 612** (ölçülen) |

### Üretildi

| Teslimat | Durum |
|---|---|
| `04_BUILD/qa_plate_readability.py` | ✅ 9 denetim · 125 şekil |
| `04_BUILD/qa_crossref.py` | ✅ 6 denetim · 223 gönderme |
| `04_BUILD/qa_editorial.py` | ✅ 8 denetim · 101 sayfa |
| `04_BUILD/metadata.py` | ✅ KDP paketi · 15 alan |
| `04_BUILD/plate_prompts.py` | ✅ **103 prompt** |
| `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` | ✅ üretildi |
| `06_REPORTS/LINE_EDITOR_REPORT.md` | ✅ üç alt-ajan |
| `06_REPORTS/tracked/metadata.json` | ✅ üretildi |
| `04_BUILD/interior.py` | ⛔ **YAZILMADI** — § 8 |
| `06_REPORTS/tracked/plate-print-test.json` | ⛔ **ÜRETİLEMEZ** — A9 · kurucu |

---

## 3 · Nihai bulmaca sayısı

| | Ölçülen |
|---|---:|
| Yazılmış taslak | **101** (5 × 20 + meta) |
| Doğrulanmış (`validated`) | **0** |
| Isınma örneği | **17** · **17 / 17 mekanizma** öğretiliyor |
| Basılı çizelge | **15** (+1 basılmayan ispat alanı) |
| Levha (model) | **103** · prompt **103 / 103** |

---

## 4 · Mekanizma dağılımı ve deneyim

| kapı | tür | aha ortancası | çıkarım oranı |
|---|---|---:|---:|
| I · Threshold | keşif | **4,0** | 1,00 |
| II · Menagerie | keşif | **4,0** | 1,27 |
| III · Calendar | akıcılık | **3,0** | **2,32** |
| IV · Labyrinth | akıcılık | **3,0** | **3,43** |
| V · Mirror | akıcılık | **3,0** | **4,42** |
| Son Soru | — | 5,0 | 6,00 |

Elle işlem beş kapıda da **6–8 EU** bandında sabit; artan tek şey
düşünme (K36). Ödülsüz bulmaca **0** · tekrar yükü ortancası **2,0**.

⚠ Kapı V'in aha ortancası Faz 4'te 3,5'ti, şimdi 3,0. Sebep bir kalite
düşüşü değil: ikiz levha onarımı anlatı sözcük numaralarını değiştirdi,
bir bulmacanın **ölçülen çıkarım oranı** ilk kullanımın altına düştü ve
K36'nın tavanı 4'ten 3'e indi. **Puan ölçüyü izler, ölçü puanı değil.**

---

## 5 · Line editor

Yol haritası Faz 5 § 2 ve § 13 gereği **üç bağımsız alt-ajan** okurun
gördüğü metnin tamamını taradı (**17 877 kelime**, çözümler ve ipuçları
hariç — işleri ifadeyi ölçmekti, cevabı bilmek değil).

| | BLOCKING | MAJOR | MINOR |
|---|---:|---:|---:|
| Ön madde · ısınma · açılış · kapanış · arka madde | 5 | 22 | 17 |
| Kapı I–II (40 sayfa) | 11 | 18 | 8 |
| Kapı III–V + son soru (61 sayfa) | 7 | 12 | 14 |
| **TOPLAM** | **23** | **52** | **39** |

**Hiçbiri körü körüne kabul edilmedi** (§ 13). Her bulgu kodla
doğrulandı ya da gerekçesiyle reddedildi. Tam ledger:
`06_REPORTS/LINE_EDITOR_REPORT.md`.

| | sayı |
|---|---:|
| Doğrulandı ve **onarıldı** | **23 bloklayıcı sınıf** |
| Doğrulandı ve **reddedildi** (gerekçeli) | 2 |
| Kabul edildi, **bu fazda uygulanmadı** (gerekçeli borç) | 6 sınıf |

### En ağır üç bulgu

**① Tekillik ispatı daireseldi (K43).** Bir çizelge bulmacasının kabul
yordamına, cevabın kendisi ikinci bir süzgeç olarak yazılmıştı. İspat
daima tek üye buluyor ve kapı **yeşil yanıyordu** — ama okurun elinde o
süzgeç yok ve sayfa ona **iki satır** bırakıyordu. Sözleşmenin birinci
sözü o sayfada tutulmuyordu.

**② Üç kapı bulmacası çözülemezdi.** Levha üç sütun basıyordu ama ipucu
**dördüncü** bir sütundan söz ediyordu ve o sütun hiç basılmıyordu.
Ölçüldü: g2-020'de 5, g4-020'de 5, g5-020'de 16 satır SONDAN sayılıyor.
Doğru cevabı bulan okura levha *"bu bulmaca yanlış"* diyordu.

**③ Kitap olmayan bir hatayı vaat ediyordu (K44).** Yedi sayfa *"ters
sıra ad vermez"* diyordu; ölçüldü, **7/7'de ters sıra aynı cevabı
veriyor.** İki yolu da deneyen okur aynı cevabı iki kez alır ve
sözleşme gereği **kitabı** bozuk sanar.

---

## 6 · Çaba · tekrar · aha

| | Ölçülen | Tavan |
|---|---:|---:|
| Toplam elle işlem | 686 EU | — |
| Elle işin süredeki payı | **%12,8** | %33 |
| Tavanı aşan bulmaca | **0** | 0 |
| `repetitionBurden` ortancası | **2,0** | 2 |
| Ödülsüz bulmaca (aha ≤ 2) | **0** | 2 |
| Uzun eziyet dizisi | **0** | 0 |
| Küçük zafer payı | **%100** | ≥%40 |

⭑ **§ 15 · YÜKSEK DÜŞÜNCE / DÜŞÜK SÜRTÜNME** korundu: bu fazda hiçbir
onarım okurun elle işini ARTIRMADI. Katmanlı zincirin sahte tuzağı
kaldırılırken zorluk düşmedi (okur hâlâ iki katmanı da uygulamak
zorunda); ısınma örneklerine eklenen her cümle **iş değil bilgi**
verdi.

---

## 7 · Cevap uzayı

| | Ölçülen |
|---|---:|
| Bağımsız doğrulanmış | **101 / 101** |
| Elenen aday dize | **4 762** |
| Onaylanmış alternatif çözüm | **0** |
| Belirsizlik > 2 | **0** |
| İpucu | **303** · hiçbiri cevabı içermiyor |

⚠ Bu sayı Faz 4'te de aynıydı **ama anlamı değişti**: o gün bir
bulmacanın ispatı daireseldi ve gerçekte iki cevap kabul ediliyordu
(K43). Aynı yeşil, artık gerçekten yeşil.

---

## 8 · Levha okunabilirliği — bu kitabın en kritik teknik kapısı

`qa_plate_readability.py` · **9 denetim · 125 şekil**

| ölçüm | sonuç |
|---|---|
| En geniş satır | **62 / 62** sütun |
| En yüksek şekil | 24 / 34 satır |
| En uzun sayım | 5 / 5 ardışık |
| Glif dağarcığı | ✅ dingbat · emoji · teknik blok **YOK** |
| Rol başına tek glif | ✅ (6 ayrı ok → 2) |
| Karışabilir veri işareti | ✅ yok |
| Künyesiz şekil | ✅ yok |

### ⚠ ÖLÇÜLMEYEN — VE ÖLÇÜLDÜĞÜ İDDİA EDİLMİYOR

| | |
|---|---|
| Fiziksel POD prova | ⛔ **YAPILMADI** — A9 · kurucu |
| `plate-print-test.json` | ⛔ **ÜRETİLMEDİ** ve üretilemez |
| Gravür üretimi | ⛔ `07_ASSETS/raw/` **BOŞ** — 103 levhanın 0'ı |

Bu kapı basılabilir **alanı** ve **ayırt edilebilirliği** ölçtü.
Mürekkebin kâğıt üzerindeki davranışını **ölçmedi**. Ayrıca pilot
levhaları gravür değil **tipografik şekildir**; gerçek gravürler
geldiğinde aynı ölçütler piksel üzerinde yeniden koşacaktır.

---

## 9 · Sızıntı denetimi

| | sonuç |
|---|---|
| Kanarya (çalışma ağacı) | ✅ 4 denetim · **106 dosya** |
| Kanarya (commit mesajları) | ✅ son 200 mesaj |
| Kanarya (temiz klon · CI) | ✅ **gerçek GitHub Actions yeşil** |
| Son sorunun cevabı kitapta | ✅ **YOK** (`qa_meta § ⑦`) |
| Çapraz sayfa | ✅ `qa_editorial` + `qa_crossref` |

### ⭑ VE KANARYANIN KENDİSİNDE BİR KÖR NOKTA BULUNDU (K46)

Yeni üretilen prompt kütüphanesi **beş cevabı** taşıdı ve commit edildi;
**CI kırmızı yandı.** Kanarya commit'ten ÖNCE koşmuştu ve yeşildi —
çünkü `git ls-files` yalnızca **zaten takip edilen** dosyaları verir.

> **Süreç doğruydu; kapsam eksikti.** Bir kapının ne zaman koştuğu,
> neye baktığı bilinmeden bir şey ifade etmez.

Kapsam artık takip edilenler **+ eklenecek olanlar**. Ve prompt
kütüphanesi harf yerine **iskelet** basıyor — gravürcünün ihtiyacı
zaten geometriydi (K47).

Bu fazda kanarya **üç kez daha** ısırdı ve üçünde de haklıydı: iki kez
kendi açıklama yorumlarımı, bir kez ön madde metnini yakaladı.

---

## 10 · Sayfa modeli

| | Ölçülen | Bildirilen |
|---|---:|---:|
| Gövde metni (5 kapı + son soru) | **61,6** | 176 |
| İpuçları | 12,7 | 26 |
| Çözümler | 7,7 | 18 |
| Araçlar levhası | 3,2 | 4 |
| **Model toplamı** | — | **238** |
| Hedef | — | 230 ± %6 |
| Levha | — | **103** (hedef 110 ± %10) |

⭑ Ölçülen metin bütçenin altındadır ve bu bir hata değildir: kalan payı
**levhalar** doldurur. Pay, dizgi dondurulduğunda kapanacaktır.

⚠ **Levha sayısı 112 → 103 düzeltildi.** Bildirim her bulmacanın bir
gravürü olduğunu varsayıyordu; yedi bulmaca gravür değil **basılı
çizelge** taşır, ve son sorunun levhası **iki kez sayılıyordu**. Fazla
bildirilen levha, kurucudan üretilmeyecek dokuz gravür istemek demekti.

---

## 11 · Kalite kapıları

`./04_BUILD/qa_all.sh` · kapı `phase5` · **bütün kapılar yeşil**

| kapı | sonuç |
|---|---|
| veri bütünlüğü · depo bütünlüğü | ✅ |
| **KAPILARIN KENDİ TESTİ** | ✅ **242 denetim** (213 → 242) |
| araştırma · DAG · taksonomi | ✅ |
| ⭑ çözüm kanaryası ⭑ | ✅ 106 dosya |
| ⭑ cevap uzayı ⭑ | ✅ 101 · 4762 aday |
| devir · çaba · deneyim (**19 denetim**) | ✅ |
| paketten çözme · levha verisi · okur paketi | ✅ |
| çözülebilirlik · alternatif çözüm · ipucu | ✅ |
| **EDİTORYAL BÜTÜNLÜK** (yeni · 8) | ✅ |
| **meta-mister** (29) | ✅ |
| **ÇAPRAZ REFERANS** (yeni · 6) | ✅ |
| **⭑ LEVHA OKUNABİLİRLİĞİ ⭑** (yeni · 9) | ✅ |
| gravür prompt kütüphanesi (yeni) | ✅ 103 |
| ⛔ öldürme kapısı ⛔ | ⛔ **HARD-STOP** — geçersiz kılmayla ilerlendi |
| sayfa bütçesi · sayfa ölçümü | ✅ 238 sayfa · 103 levha |
| KDP metadata paketi (yeni) | ✅ · 3 kurucu alanı boş |
| üretilen belgeler güncel | ✅ |

**Fikstür:** 213 → **242** denetim. Faz 5'te eklenen her kural, kırık
bir kurguda **çöktüğü görülerek** eklendi.

---

## 12 · Git / CI

| | |
|---|---|
| Dal | `faz/5-yakinsama` |
| Commit | 8 parça · her biri ayrı CI koşusu |
| CI kırmızı olayı | **1** (K46) — kök sebep bulundu ve kapatıldı |
| `.gate` | `phase4` → **`phase5`** |
| Birleştirme | `main` · ileri sarma · **açık PR yok** |

---

## 13 · Faz 5 · Definition of Done

Yol haritası Faz 5 § 10:

| # | Madde | Durum |
|---|---|---|
| 1 | Ön madde ve çerçeve anlatı yazıldı | ✅ |
| 2 | **LINE EDITOR raporu alındı ve geçerli düzeltmeler uygulandı** | ✅ 23 bloklayıcı sınıf onarıldı · ledger yazıldı |
| 3 | 110/110 levha üretildi ve doğru bulmacaya bağlandı | ⛔ **0 / 103** — kurucu işi |
| 4 | **POD prova alındı ve levha okunabilirliği ölçüldü** | ⛔ **YAPILMADI** — A9 |
| 5 | İç blok dizgisi **donduruldu** → Kapı V kilitlendi | ⛔ **YAPILMADI** — § 14 |
| 6 | Doğrulama sayfası **canlı** | ⛔ **YAPILMADI** — A4 |
| 7 | CI **YEŞİL** · `.gate` → `phase5` | ✅ / ✅ |

### ⛔ Kapanmayan dört madde ve neden

| madde | neden ajan yapamaz |
|---|---|
| **110 levha** | Gravür üretimi kurucunun görsel hattıdır. Ajanın yapabileceği — **103 promptun tamamı, ölçülmüş veri bölümleriyle** — yapıldı. |
| **POD prova** | Fiziksel baskı ve göz. Ajan bir provayı ne sipariş eder, ne alındığını iddia eder, ne ölçüm uydurur. |
| **Dizgi dondurma** | `interior.py` reportlab ister ve **gerçek levhalar gelmeden** dizgi dondurulamaz: Kapı V sayfa numaralarına bağlıdır (K12) ve 103 gravürün sayfa yerleşimi bilinmeden sayfa numarası kesinleşmez. Dondurmak, kırılacak bir şeyi kilitlemek olurdu. |
| **Doğrulama sayfası** | A4 · barındırma kararı kurucuya aittir. |

> ⚠ **Faz 5 bu dört madde olmadan "TAMAM" diye anılamaz.** Ajanın
> yapabileceği bütün Faz 5 işi bitti; kalan dördü kurucuya aittir ve
> hiçbiri uydurulmadı.

---

## 14 · Kurucuya kalan işler

| # | Ne | Neden ajan yapamaz |
|---|---|---|
| **A12b** | ⭑ **Harici çözücü oturumları** ⭑ | İnsan gerekir. `validate_spec` sahte kayda izin vermez. |
| **A9** | POD prova kopya | Fiziksel baskı |
| — | **103 gravürün üretilmesi** | Görsel hat · prompt kütüphanesi hazır |
| **A4** | Doğrulama sayfası barındırma | Altyapı kararı |
| **A6** | Yazar biyografisi | Kurucu metni |
| A2 · A5 · A7 · A10 | Tema · üslup · biçim · ikinci öldürme kapısı | Kurucu kararı |
| — | 15 künyenin insan gözüyle doğrulanması | Kaynak erişimi |
| — | AI açıklaması beyanı | Kurucu beyanı |

---

## 15 · Faz 5'in yeni kararları

| # | Karar |
|---|---|
| **K42** | Anlatı kuralı **ölçüye göre daraltıldı** — ve daraltma da test edildi |
| **K43** | Bir tekillik ispatı, **ispatladığı şeyi varsayamaz** |
| **K44** | Kitap **olmayan bir hatayı vaat edemez** |
| **K45** | Aile öğretilmiş olabilir; **işlem** öğretilmemiş olabilir |
| **K46** | Kanarya, henüz **takip edilmeyen** dosyayı görmüyordu |
| **K47** | Levha bir resim değil, bulmacanın **verisidir** |

---

## 16 · Kalan borç — bir sonraki fazın girdisi

`LINE_EDITOR_REPORT § 3`'te altı sınıf **kabul edildi ama uygulanmadı**;
her birinin gerekçesi yazılıdır. Özetle:

* Kapı I'in dört kısa cevabı kitabın söz dağarcığıyla çarpışıyor (K41) —
  o kohort **ölçülen öldürme kapısının kanıt tabanıdır**;
* Kapı IV'te dört yol sayfası birbirinin kopyası — mekanizma yeniden
  tasarımı ve K36 tavanlarının yeniden ölçülmesi gerekir;
* terim birleştirmesi (`çember`/`halka`, `Sözlük`/`Katalog`) her kısıt
  cümlesine dokunur;
* Kapı I–II'de altı şekil/metin ayrışması — öldürme kapısının ölçtüğü
  kohort;
* `■` işaretinin yerleşimi — dizgi dondurmayla birlikte ölçülecek;
* yaratık çizelgelerinde olgusal tuhaflıklar — A2'ye bağlı.

---

## 17 · DURUM

```
FAZ 4                COMPLETE       (kurucu geçersiz kılmasıyla)
FAZ 5                COMPLETE       (ajan işi · dört kurucu maddesi AÇIK)
İNSAN DOĞRULAMASI    HÂLÂ BEKLİYOR
KURUCU GEÇERSİZ KILMASI  AKTİF
```

⚠ Bu kitap **insan tarafından test edilmedi**, **harici olarak
doğrulanmadı** ve **basılmadı**. Yüz bir bulmacanın hiçbiri bir insanın
elinde çözülmedi.

---

*Bu rapordaki her sayı `06_REPORTS/tracked/` altındaki üretilen ölçüm
dosyalarından alınmıştır. Hiçbiri elle tahmin edilmemiştir.*
