# FAZ 3 RAPORU — KAPI II · YARATIKLAR

> **Codex Enigmatica** · 24 Ağustos 2026
> Kapı: `phase3` · Giriş: ⚑ **KURUCU GEÇERSİZ KILMASI**

---

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

Bu cümle bu raporda **kalıcıdır** ve silinmeyecektir.

| | |
|---|---|
| Ölçülen öldürme kapısı | ⛔ **HARD-STOP** (1/5) — **değişmedi** |
| Yapılan harici oturum | **0** |
| İnsan doğrulaması geçti mi | **HAYIR** |
| Faz 3 girişi | ⚑ **kurucu geçersiz kılması** |
| Gerekçe | *founder-authorized continuation* |

> ### Faz 3 "harici olarak doğrulanmış" DEĞİLDİR ve öyle anılamaz.

---

## 1 · Kurucu geçersiz kılması

Kurucu 24 Ağustos 2026'da Faz 3'ün, ikinci tur insan doğrulaması
tamamlanmadan başlamasına açıkça izin verdi. Karar `DECISIONS.md § A13`
ve `project_config.json § killGate.externalValidation` içinde makine
okunur hâlde durur:

```
status:                 founder_override_partial
sessionsPerformed:      0
humanValidationPassed:  false
founderOverride:        true
```

### ⭑ Ve bu bir düğme değil, bir KAYIT ⭑

`kill_gate.py` kararı hâlâ **HARD-STOP olarak hesaplar, yazdırır ve
rapora `verdict` alanıyla yazar.** Geçersiz kılma yalnızca **çıkış
kodunu** değiştirir. Her koşuda dört alan birlikte durur:
`measuredVerdict` · `overrideActive` · `humanValidationPassed` ·
`sessionsPerformed`.

**Uydurma yapısal olarak imkânsızdır.** Dört muhafız kaydın kendisini
denetler ve dördü de kendi kusurlu fikstürüyle ısırdığı **kanıtlanmış**
olarak durur:

| muhafız | ne yakalar |
|---|---|
| ① | `humanValidationPassed=true` iken `sessionsPerformed=0` |
| ② | bildirilen oturum sayısı diskte **ölçüleni aşıyor** |
| ③ | geçersiz kılma gerekçesiz/tarihsiz |
| ④ | oturum yokken `status` ≠ `founder_override_partial` |

En fazla şunu diyebilir: *"doğrulanmadı, kurucu devam etti."*

### Ve geçersiz kılmanın SINIRI ölçüldü

`validate_spec § check_gate_scope` geçersiz kılmayı **yalnızca doğrulama
eşiğine** uygular. `puzzlesDrafted` eşiği her koşulda aranır — Faz 3
girişi ilk denendiğinde kapı **kırmızı yandı** (20 < 40) ve ancak Kapı II
gerçekten yazıldıktan sonra yeşile döndü.

> **Kurucu kararı bir bulmacayı yazılmış yapmaz.**

---

## 2 · Önceki hard-stop durumu

| | |
|---|---:|
| Kapı I'i bitiren harici çözücü | **1 / 5** |
| Geçme eşiği | ≥ 4 |
| Sert durdurma eşiği | < 3 |
| **Ölçülen karar** | ⛔ **HARD-STOP** |
| Baskın bırakma sebebi | *"sıkıldım"* |

Bu karar **silinmedi, değiştirilmedi, yumuşatılmadı.** Kapı I iki kez
yeniden tasarlandı (486 → 184 → **101 elle işlem**) ama yeniden tasarım
bir ölçüm değildir; **düzeltme iddiasıdır** ve doğrulanması A12b'ye
bağlıdır.

---

## 3 · Yazılan bulmaca

| | |
|---|---:|
| Kapı II · bu fazda yazılan | **20** |
| Kitap toplamı (`drafted`) | **40** / 100 |
| **Doğrulanmış (`validated`)** | **0** / 100 |
| **Test edilmiş (`tested`)** | **0** — ⚠ hiçbiri |

⚠ Hiçbir kaydın `status` alanı elle yükseltilmedi. Kırk bulmaca da
`drafted` · `external-pending` durumundadır.

---

## 4 · Mekanizma dağılımı

| Aile | Kapı II | pay |
|---|---:|---:|
| `plate-embedded-cipher` | **6** | %30 |
| `classification` | **5** | %25 |
| `constraint-logic` | 3 | %15 |
| `plate-observation` | 2 | %10 |
| `script-decoding` | 2 | %10 |
| `substitution-cipher` | 1 | %5 |
| `gate-synthesis` | 1 | %5 |

En yüksek aile payı **%30** (tavan %35 ✓) · ayrı aile **7** (taban 4 ✓) ·
en uzun ardışık aynı aile **1** ✓

⭑ **`plate-embedded-cipher` en büyük paydır ve bu kasıtlıdır:** yol
haritası bu kapının amacını *"levha içi şifreyi öğretmek — kitabın imza
mekaniği burada doğar"* diye yazar. Altı bulmaca aynı mekanizmayı, her
seferinde bir adım daha az söyleyerek kullanır.

⭑ **B3 kapandı:** anahtarlı alfabe Kapı II'ye ertelenmişti ve burada —
ama okurdan yirmi dokuz harfi yeniden dizmesi **istenmez**. Satır levhada
basılıdır; okur onu **kullanır**. (Yönerge § 6: *"Can I rewrite the
alphabet correctly?"* bir bulmaca değildir.)

---

## 5 · Kelime

| | Kapı I | **Kapı II** |
|---|---:|---:|
| Bulmaca metni | 1.675 | **1.785** |
| İpuçları (60) | 844 | **922** |
| Çözüm açıklamaları | 540 | **581** |
| **Toplam** | 3.059 | **3.288** |

Isınma bölümü 722 · çerçeve anlatı 281 → **kümülatif ≈ 7.350 kelime**.

⚑ **Yol haritası Faz 3 için ~6.500 kelime (kümülatif ~12.500) öngörüyordu.
Ölçülen değer bunun yarısı kadardır** — ve bu Kapı II'ye özgü değil,
iki kapıda da aynı: üslup tahmin edilenden **yoğun**. Sayfa modeli
ölçülen metinle çalıştığı için kapı yeşildir; ama **kurucu bunu bilmeli**
(A8 · sayfa hedefi).

---

## 6 · Sayfa

| | |
|---:|---|
| **236** | model toplamı (önceki 232) |
| +4 | ipucu bölümü 22 → **26** — ⭑ **ÖLÇÜLDÜ, tahmin edilmedi** |
| 19,7 | Kapı I gövdesi · **ölçülen** (bildirilen bütçe 34) |
| 112 | levha |

⚑ **İpucu bütçesi neden büyüdü:** `pilot_pages.py` yazılmış Kapı I
ipuçlarını saydı — 1.787 kelime → 5,1 sayfa; kitap ölçeğinde **25,5
sayfa**, bütçe 22'ydi. **Kısaltmak seçenek değildi:** ipucu merdiveni
"kapsam monoton artar" kuralına uyar ve üçüncü kademe önceki adımları
sözcükleriyle taşımak zorundadır. Kısaltmak kuralı kırardı.

⚑ Ve gövde **bütçesinin çok altında ölçülüyor** (19,7 / 34). Sayfa
hedefi A8'de kurucu onayı bekliyor; bu iki ölçüm oraya girdi.

---

## 7 · Çaba ölçümü

| | Kapı I | **Kapı II** | kitap |
|---|---:|---:|---:|
| Elle işlem (beklenen) | 100,8 | **133,5** | **234,3** |
| En kötü hâl | 128 | **168** | 296 |
| Bildirilen süre | 105 dk | **228 dk** | 333 dk |
| Bütçesini aşan bulmaca | 0/20 | **0/20** | **0/40** |
| En yüksek kat | 1,00× | **0,95×** | — |
| ⭑ Elle işin süredeki payı | %32 | **%20** | **%23** |

> ### ★'dan ★★'ye geçilirken elle iş ARTMADI (K32).

Zorluk üç eksende arttı ve **üçü de düşüncedir**:

1. **Kural verilmez, bulunur.** Sınıflama ailesi bölmeleri gösterir,
   kuralı göstermez.
2. **Çapa basılı olmaktan çıkar.** Levha içi şifre altı bulmacalık bir
   rampadır: şerit(çapa basılı) → halka(çapa basılı) → halka(çapa
   **siluetten çıkarılır**) → halka(çapa **ve yön** çıkarılır).
   Her adımda okur bir şeyi daha kendi bulur; **hiçbir adımda daha fazla
   iş yapmaz.**
3. **Mekanizmalar zincirlenir** — bir cevap sonraki bulmacanın basılı
   anahtarı olur (yayılma yarıçapı **≤1**).

### ⚑ Bir eşik değişti ve sessiz değil (K33)

K4 tavanı zorlukla ölçeklenir: **★ = 8** (değişmedi) · **★★ = 12**.
Gerekçe K4'ün kendi metnindedir — *"4–8 **anlamlı**"* ifadesini
*"20–40 **tekrarlı**"*ya karşı koyar; yasakladığı şey **tekrardır**.
★★'de okur bir dizeyi ters yönde bir kez daha okuyabilir; altı harflik
bir şeritte en kötü hâl 12'dir.

⭑ Asıl emniyet tavan değil, **`repetitionBurden`**dir — ve **o
ölçeklenmez**.

---

## 8 · ahaScore

| | Kapı I | **Kapı II** | kitap |
|---|---:|---:|---:|
| Ortanca | 4,0 | **4,0** | **4,0** |
| Ödülsüz (≤2) | 0 | **0** | **0** |

### ⚠ Ve bu bir kanıt değildir

`ahaScore` **yazarın kendi puanıdır.** Kapı onu doğrulayamaz;
**şişirilmesini zorlaştırır** ve Kapı II'de bunu somut olarak yaptı:

> **Aynı mekanizma ikinci kez 4+ alamaz.** Kapı II Kapı I'in
> mekanizmalarının çoğunu yeniden kullanır ve bu kural, ilk taslakta
> verdiğim puanları **aşağı çekmeye zorladı**: çizelge araması, glif
> okuma, kesişim ızgarası ve kapı bulmacası **3'e indi** — çünkü okur
> onları ilk kez Kapı I'de gördü.

Ortanca 4,0'a ancak **tasarımı değiştirerek** ulaşıldı, puanı
değiştirerek değil: Kapı II'nin kapı bulmacası artık **iki yönlü konum**
kullanıyor (▸ baştan / ◂ **sondan**) ve işaret **yük taşıyor** —
görmezden gelen okur Çizelge G'de söz bulamaz. Bu, üretim anında
her satır için ayrı ayrı ispatlanır.

Gerçek ölçüm A12b'nin kayıt formundadır: *"anladım! anı yaşadım mı"*.

---

## 9 · repetitionBurden

| | Kapı I | **Kapı II** |
|---|---:|---:|
| Ortanca | 2,0 | **2,0** (düşük) |
| Tavanı aşan | 0 | **0** |

Ölçüt **yazardan gelmez**; `qa_effort`in modelinden hesaplanır ve
zorlukla **ölçeklenmez**.

---

## 10 · answerSpace istatistiği

| | |
|---|---:|
| Denetlenen bulmaca | **40** |
| Bağımsız üretilen aday dize | **2.114** |
| **Tam olarak bir kabul** | **40 / 40** ✅ |
| En küçük alan | 12 (kapı ifadesi listesi) |
| Kapı II alanı | **50 üyelik basılı katalog** |

Kapı II üç yeni kabul yordamı getirdi ve **üçü de kendi kusurlu
fikstürüyle ısırdığı kanıtlanarak** duruyor:

| yordam | ne ispatlar |
|---|---|
| `reachable-via-grid-coordinates` | ispat **bütün** okumaları açar; yanlış istasyondan başlayan okur geçerli bir ada **düşemez** |
| `misclassified-in-printed-pens` | kuralı **basılı nitelik tablosu** belirler; iki kural da açıklıyorsa **kırmızı** |
| `reachable-by-keyed-alphabet` | anahtar satırı **basılıdır**; okur kurmaz |

---

## 11 · İç çözücü istatistiği

⚠ **İNSAN İÇ ÇÖZÜCÜSÜ ÇALIŞTIRILMADI.** Bunun yerine daha dar ama
bağımsız bir ölçüm yapıldı: `05_TESTS/solve_from_pack.py`.

Betik **cevap anahtarına bakmadan**, yalnızca okurun eline geçen şeyden
(sayfa metni, şekil, basılı çizelge, araçlar levhası) cevabı türetmeye
çalışır; çözüm dosyası **ancak en sonda**, sağlama için açılır.

| | |
|---|---:|
| Türetilen | **16 / 40** |
| **Anahtarla uyuşan** | **16** |
| **Uyuşmayan** | **0** |
| Kapsam dışı | 24 |

⭑ En sert dal sınıflamadır: **kural sayfada yazılı değildir** ve betik
onu basılı sütunlardan **kendisi çıkarır** — okurdan beklenen şeyin
aynısı. Beşinde de doğru kuralı ve doğru aykırı üyeyi buldu.

⚠ **Kapsam dışı kalan 24 bulmaca "geçti" SAYILMAZ.** Bir çözücü olarak
betiğin beceriksizliği, bulmacanın kusuru değildir — ama kusursuzluğunun
kanıtı da değildir.

⚠ **VE BU BİR İNSAN TESTİ DEĞİLDİR.** Bir makine bir bulmacanın
*eğlenceli* olup olmadığını söyleyemez.

---

## 12 · Kırmızı takım bulguları

Faz 3'te **beş** bulgu; hiçbiri okuyarak bulunmadı.

| # | bulgu | yakalayan |
|---|---|---|
| F3-01 | Zincirler birbirine eklenmişti → yayılma yarıçapı 2 | `qa_handoff` |
| F3-02 | ⭑ Bir ad **ters çevrildiğinde** Türkçenin en sık eklerinden birinin içine düşüyor ve **beş dosyada** geçiyordu | `qa_solution_leak` |
| F3-03 | İki çizelge hücresi, **bağımlı olmadıkları** bulmacaların cevabını basıyordu — § ⑫ oraya bakmıyordu | üretim assert'i |
| F3-04 | Akran havuzu tükendi; son levha **iki etiketle** kaldı | `qa_effort` |
| F3-05 | Bir Kapı I levhası **trim'e sığmıyordu** (66 > 62 karakter) | `qa_plate_data` |
| F3-06 | ⭑ Bir cevap, bu raporun **kendi cümlesinde** geçiyordu — commit'ten SONRA | `qa_solution_leak` |

### ⭑ F3-02 · kanarya ters de arar (K34)

Elli aday ad tarandı. Biri **düz biçimde temizdi** ama ters çevrildiğinde
sık bir Türkçe ekin içine düşüyordu. **Ders: bir adı kanaryaya karşı
denerken ters biçimini de dene.** Kanarya bunu zaten yapıyordu; ben
yapmıyordum.

### ⭑ F3-06 · kanarya bu raporun kendi cümlesini yakaladı

Bir yazı gerecinin adı Kapı II'nin cevaplarından biriydi. Sonra bu rapora
*"gerçek ölçüm ... kâğıt ve gözle yapılır"* diye yazdım — ve kanarya
kendi raporumu **sızıntı** saydı. Haklıydı.

⚠ Ve bu kez **commit'ten sonra** koştu: CI kırmızı yandı. Commit
**mesajı** temizdi (geri alınamayan kanal) ve düzeltme bir sonraki
commit'e sığdı, ama ders süreçtir: **kanarya commit'ten ÖNCE koşar.**

İki katalog üyesi artık cevap olamaz (biri ters okumada, biri bu
cümlede yakalandı) ve ikisi de **akran olarak katalogda kalır**.

### ⭑ F3-03 · sızıntı kapının BAKTIĞI YERİN DIŞINDA (K35)

`§ ⑫` zincirin kaynağını iki sayfanın kesişiminden okumayı engeller —
ama yalnızca **bildirilen bağımlılık** için. İki hücre, bağımlı
olmadıkları bulmacaların cevabını basıyordu. Artık üreteç bunu **üretim
anında** reddeder.

---

## 13 · Görsel QA bulguları

**`04_BUILD/qa_plate_data.py`** (yeni · 5 denetim) — yol haritası Faz 3
§ 13'ün istediği baskı **ön** ölçümü.

| | |
|---|---:|
| Ölçülen levha | **22** |
| ⭑ En ince ayrım | **5** ardışık aynı işaret (tavan 5) |
| Ortalama bit fazlalığı | **2,9×** |
| Trim'i aşan şekil | **0** (bir tanesi bulundu ve düzeltildi) |

### Yol haritasının sorusu: bir gravür kaç bit taşır?

| levha türü | taşınan | gereken | fazlalık |
|---|---:|---:|---:|
| ızgara koordinatı (7 istasyon) | 34,3 bit | 5,6 bit | **6,1×** |
| glif şeridi (6 glif) | 29,1 bit | 5,6 bit | **5,2×** |
| üç kenarlı sayı levhası | 7,0 bit | 5,6 bit | 1,2× |

⚠ **Fazlalık bir emniyet değildir.** Levha cevabın gerektirdiğinden çok
daha fazla bit taşır ama **bir istasyon yanlış okunursa çıkan dize
katalogda yoktur** — hata tespiti fazlalıktan değil, **basılı
katalogdan** gelir.

⭑ **En ince ayrım tam tavanda: 5.** Eşik Alfabesi'nin kendi yapısı bunu
gerektirir (29 = 6 grup × 5) ve çizelge işaretleri aralıklı basar.
**Gerçek risk buradadır** ve bu kapı onu ölçebildiği yere kadar ölçer.

> ⚠ **BU KAPI BASKI YAPMAZ.** Gerçek ölçüm mürekkep, kâğıt ve gözle
> yapılır — **A9 · fiziksel prova · YAPILMADI.**

---

## 14 · CI durumu

| | |
|---|---|
| `.gate` | `phase3` |
| Kalite kapısı | **17 betik** |
| `selftest` | **195 denetim — bütün kapılar ısırıyor** |
| `qa_all.sh` | ✅ **BÜTÜN KAPILAR YEŞİL** |
| Kanarya | ✅ kip A yerel · kip B temiz klonda doğrulandı (261 karma) |
| Açık PR | **0** |

⚠ Kanarya künyesi **yeniden üretildi**: cevap kümesi değiştiğinde künye
bayatlar ve kip A yeşilken kip B kırmızı yanar. Bu kapının **doğru**
davranışıdır.

---

## 15 · Harici doğrulama durumu

# ⛔ YAPILMADI

| | |
|---|---:|
| Kapı I harici oturum (A12) | **0 / 5** |
| **Kapı II harici oturum** | **0 / ≥2** |
| `06_REPORTS/solver/` | **boş** |

Faz 3'ün Definition of Done'ı *"Kapı II için ≥2 harici çözücü testi
geçti"* der. **Bu madde karşılanmadı** ve ajan tarafından karşılanamaz.

Paket hazır:
`02_MANUSCRIPT/PILOT_TR/PILOT_TR_KAPI2.md` (bulmacalar + bulmaca başına
kayıt formu) ve `PILOT_TR_KAPI2_IPUCLARI.md` (**ayrı zarf**).

---

## 16 · Bekleyen kurucu kararları

| # | karar | durum |
|---|---|---|
| **A12 / A12b** | harici çözücü oturumları (Kapı I) | ⛔ **bloklayıcı** |
| **A13b** | Kapı II için ≥2 harici çözücü | ⛔ **bloklayıcı** |
| **A9** | fiziksel prova — paket hazır | ⚑ bekliyor |
| **A8** | sayfa hedefi — model **236**, ölçülen gövde bütçenin altında, kelime tahminin yarısı | ⚑ **girdi geldi** |
| **B5** | `EU_PER_MINUTE = 3` kalibrasyonu | ⚑ hâlâ `calibrated: false` |
| **A2 · A7 · A10** | Faz 1'den açık | ⚑ bekliyor |
| — | 16 künyenin `asserted` doğrulaması | ⚑ bekliyor |

---

## 17 · Faz 4 hazırlığı

| Faz 4 gereksinimi | durum |
|---|---|
| Kapı III–V + meta-mister (60 bulmaca) | mimari hazır · **yazılmadı** |
| `qa_meta.py` | **yazılmadı** (Faz 4 test altyapısı) |
| Meta bağlantısı | ✅ `meta-001` beş kapı bulmacasına bağlı; Kapı II bağı **yazılan** bulmacaya taşındı |
| DAG | ✅ döngüsüz · ileri referans yok |
| Aday havuzu | ✅ 151 aday · Kapı III–V için 87 |
| Sözlük kapasitesi | ⚠ **dar** — 50 üyelik katalogun 19'u cevap oldu; Kapı III–V kendi basılı listelerini isteyecek |

### ⛔ FAZ 4 BAŞLATILMADI

Yönerge § 12 açıktır: *"Do NOT automatically jump into Phase 4."*

---

## Kapanış — üç şey birbirinin yerine geçmez

| | |
|---|---|
| **ÖLÇÜLEN** | 40/40 tekil cevap · çaba %23 · aha 4,0 · levha verisi geri alınabilir |
| **GEÇERSİZ KILINAN** | Faz 3 girişi — kurucu kararı, ölçüm değil |
| **HENÜZ DOĞRULANMAMIŞ** | **hiçbir insanın bu bulmacaları çözüp çözemediği** |

> # FAZ 3 TAMAM · HARİCİ İNSAN DOĞRULAMASI HÂLÂ BEKLİYOR
