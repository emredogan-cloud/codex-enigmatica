# CHANGELOG — Codex Enigmatica

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.8.0] — 2026-08-25 · KURUCU VARLIKLARI · İŞLEME + KDP PAKETİ

# ⛔ İKİ BLOKLAYICI AÇIK

**① Genel depodaki bir commit mesajında bir cevap var** (`e341a5f`,
kanarya kip A ile yakaladı; CI kip B'de künye BAYAT olduğu için
görmedi). **② Seçilen onarım (cevabı değiştirmek) uygulanamadı:**
Kapı 3-4-5 üreteci kırık ve bu **değişikliğimden önce de** kırıktı
(`g5-013`, yapı çifti bulunamadı). Ayrıntı:
`06_REPORTS/FINAL_ASSET_PRODUCTION_REPORT.md § 1`.

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

`founder_override_partial` · `sessionsPerformed = 0` ·
`humanValidationPassed = false` · **HARD-STOP**.

### Eklendi — kurucu 111 görsel teslim etti, hepsi ölçüldü

Envanter 111/111, eksik yok. Üç sayı ayrı tutuldu: gerçek piksel,
metadata etiketi (hepsi 72 diyordu — bir iddia) ve **etkin DPI** (gerçek
piksel ÷ fiziksel ölçü — bir ölçüm). Gravürlerin **77/103'ü** 300 dpi
altındaydı, kapaklar 170.

İşleme: Real-ESRGAN 4× → hedefe indir → alfa düzleştir → etiketle.
**111/111 işlendi**, ~64 dk. Gravürler artık 600 dpi, kapaklar 1800×2700,
A+ tam Amazon ölçüsünde. Sayılabilir işaretlerin korunduğu ölçüldü.

### ⭑ Düzeltildi — sözleşmenin KENDİSİ yanlıştı

`2·3` gösterimindeki nokta bir AYRAÇTIR. `measure()` onu işaret sayıyor,
12 levhaya `exactly N of mark '·'` diye olmayan bir şart yazıyordu — ve
o şart istasyon sayısını da bozuyordu. Gravürcü yedi noktaya yer açmak
için sekizinci istasyonu açtı; `pl-g3-03` ve `pl-g3-08` böyle çıktı.
Bulmaca verisine dokunulmadı; veriyi yanlış OKUYAN türetme düzeltildi.
**14 levha yeniden üretilmeli** (12 yanlış sözleşme + `pl-g1-07`,
`pl-g1-08` sayım hatası).

### Eklendi — iki tam sarmal kapak promptu (§ 20-24)

`wrap-cover-option-01/02`, arka·sırt·ön bölgeleriyle. **Nihai piksel
ölçüsü bilerek çivilenmedi** (sırt sayfa sayısından türer, K12) ve bir
denetim çivilemeyi kırmızıya çeviriyor.

### Eklendi — KDP el kitabı ve Türkçe çevrimdışı kılavuz

`08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` · `KDP_UPLOAD_GUIDE.html`.
A–G, 13 adım, 30 kopya düğmesi, 33 kutucuk, localStorage.
Hazırlık göstergesi **dosya sistemine bakarak** doldurulur.

### Eklendi — sayım sayfası, çünkü ajan sayamadı

Otomatik sayım denendi ve güvenilmedi (eşikleme 5 yerine 44 saydı,
özilinti 6 yerine 2,6). Güvenilmez bir sayaç sayaç olmamasından
kötüdür. Ajan sayıyı ölçmez; `asset_ingest.py --sheet` insanın
ölçmesini mümkün kılar.

- Rapor: `06_REPORTS/FINAL_ASSET_PRODUCTION_REPORT.md`

---

## [0.7.1] — 2026-08-24 · GÖRSEL PROMPT KÜTÜPHANESİ · YENİDEN İNŞA

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

Bu sürüm **hiçbir doğrulama durumunu değiştirmez**:
`externalValidation = founder_override_partial` · `sessionsPerformed = 0`
· `humanValidationPassed = false` · ölçülen karar **HARD-STOP**.
`07_ASSETS/raw/` hâlâ **boştur** — **üretilmiş görsel: 0**.

### Değişti — kütüphane bir belge değil, ARAÇ oldu

`07_ASSETS/IMAGE_PROMPT_LIBRARY.html` yeniden inşa edildi: sekiz
bölüm · yapışkan gezinme · **223 kopya düğmesi** (eskiden 0) · 102
katlanır blok · gömülü CSS/JS, dış bağ yok — **çevrimdışı açılır**.

Eski kütüphane doğruydu ama kullanılamazdı: kurucu 103 promptu elle
seçmek zorundaydı. Eksik olan veri değil, belgenin çalışmasıydı.

### Eklendi — ticari promptlar

**2 kapak konsepti** (6 × 9 in · 1800 × 2700 px · metin-güvenli
alanlar; **sırt ölçüsü YOK** — iç blok dondurulmadı, K12) ve
**6 A+ modülü** (gerçek Amazon modül türleri ve ölçüleri). Sekizinin
hepsi bir `BRIEF §` dayanağı taşır; hepsi **metinsizdir**.

Yeni üreteç: `04_BUILD/prompt_catalog.py` — gravür promptları
bulmacadan **ölçülür**, kapak/A+ promptları `BRIEF.md`'den gelen
**ticari karardır**; ikisi ayrı dosyada durur.

### ⭑ Korundu — 103 gravür promptu, ölçülerek kanıtlandı

Eski kütüphane `git show HEAD:` ile çıkarılıp karşılaştırıldı:
**VERİ FARKI: 0**. Dokuz bulmaca-dışı kimlik `VISUAL_ARCHITECTURE § 2`
kuralına uyduruldu (`pl-` → `dc-`/`tl-`); **94 bulmaca kimliğine
dokunulmadı**.

### Eklendi — üreteç kendi HTML'ini denetler

Kopya kimlik · hedefsiz düğme · düğmesiz kutu · kırık çıpa · dengesiz
etiket · dış bağ · sır sızıntısı · dosya adı kalıbı. Üreteç
**22 denetim** çalıştırır. 223 düğmenin hepsi tarayıcıda tıklanarak
ölçüldü: **yanlış metin kopyalayan 0**.

### Düzeltildi — CI kütüphaneyi hiç denetlemiyordu

`plate_prompts.py` yalnızca `qa_all.sh` içinden, yani yerel makinede
çalışıyordu; CI onu hiç çağırmıyordu. Elle düzenlenmiş ya da bayat bir
kütüphane CI'dan **yeşil geçerdi** ve dosya doğru *görüneceği* için
kimse fark etmezdi.

Üstelik `--check` bayrağı kabul ediliyor ama hiçbir şey yapmıyordu —
her koşuda dosyayı yeniden yazıyordu. Hiçbir şey yapmayan bir bayrak,
olmayan bir bayraktan daha kötüdür.

`--check` artık yazmaz, **karşılaştırır**; kapı CI'ya eklendi ve
ısırdığı ölçüldü (tek bir rakam değiştirildi → çıkış kodu 1).

- Rapor: `06_REPORTS/IMAGE_PROMPT_LIBRARY_FINALIZATION_REPORT.md`

---

## [0.7.0] — 2026-08-24 · FAZ 5 · YAKINSAMA + LEVHA + LINE EDITOR

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

`externalValidation` **değişmedi**: `founder_override_partial` ·
`sessionsPerformed = 0` · `humanValidationPassed = false` ·
ölçülen karar **HARD-STOP**. `07_ASSETS/raw/` **boştur** — 103 gravürün
hiçbiri üretilmedi. POD prova **alınmadı**. Doğrulama sayfası **canlı
değil**.

### Eklendi — ön madde, arka madde, kapanış

Başlık · künye · çerçeve anlatı · **SÖZLEŞME SAYFASI** (dört söz) ·
araçlar girişi · ısınma girişi · ipucu girişi · çözüm girişi · şifre
referansı · kaynaklar · kolofon · **çerçeve anlatının kapanışı**.
Ölçülen kelime: **17.612**.

### Eklendi — dört yeni kapı

| kapı | denetim | ne arar |
|---|---:|---|
| `qa_plate_readability.py` | 9 | levha basılabilir mi · ayırt edilebilir mi |
| `qa_crossref.py` | 6 | kitabın kendi içine göndermeleri tutuyor mu |
| `qa_editorial.py` | 8 | line editor'ın bulduğu SINIFLAR |
| `metadata.py` · `plate_prompts.py` | — | KDP paketi · 103 gravür promptu |

### ⭑ LINE EDITOR — üç bağımsız alt-ajan

17.877 kelime tarandı: **23 BLOCKING · 52 MAJOR · 39 MINOR**. Hiçbiri
körü körüne kabul edilmedi; her bulgu kodla doğrulandı ya da
gerekçesiyle reddedildi (`06_REPORTS/LINE_EDITOR_REPORT.md`).

**⛔ TEKİLLİK İSPATI DAİRESELDİ (K43).** Bir çizelge bulmacasının kabul
yordamına CEVABIN KENDİSİ ikinci bir süzgeç olarak yazılmıştı. İspat
daima tek üye buluyor ve kapı YEŞİL yanıyordu — ama okurun elinde o
süzgeç yok ve sayfa ona İKİ satır bırakıyordu.

**⛔ ÜÇ KAPI BULMACASI ÇÖZÜLEMEZDİ.** Levha üç sütun basıyordu ama ipucu
DÖRDÜNCÜ bir sütundan söz ediyordu ve o sütun hiç basılmıyordu. Doğru
cevabı bulan okura levha "bu bulmaca yanlış" diyordu.

**⛔ KİTAP OLMAYAN BİR HATAYI VAAT EDİYORDU (K44).** Yedi sayfa "ters
sıra ad vermez" diyordu; 7/7'de ters sıra AYNI cevabı veriyor.

**⛔ SAYI SÜTUNU CEVABI ELE VERİYORDU.** 7/7 levhada cevabın katalog
numarası akranların dışındaydı: okur levhaya bakmadan çözebilirdi.

**⛔ ÖĞRETİLMEMİŞ İŞLEM (K45).** Üç levha "ayna ekseni" basıyor ve o
işlem kitabın hiçbir yerinde öğretilmiyordu. § 7 AİLEYİ denetliyordu.

Ayrıca: yapım kimlikleri okur sayfasında · aynı çizelge iki kez basılı ·
iki bulmaca aynı levha · beş tekrarlanan başlık · üç anlatı satırında
mekanik · ön madde çizelge sayısını yanlış veriyor · ısınma sırası bozuk
· beş kapı açılışı çizelgesini anmıyor · sözleşme ile çözüm bölümü
çelişiyor · dört ısınma örneğinde kusur · doğrulama sayfası hiç
tanıtılmıyor.

### ⭑ KANARYANIN KÖR NOKTASI (K46) — CI kırmızısı

Yeni üretilen prompt kütüphanesi BEŞ CEVABI taşıdı ve commit edildi.
Kanarya commit'ten ÖNCE koştu ve YEŞİL yandı: `git ls-files` yalnızca
ZATEN TAKİP EDİLEN dosyaları verir. **Süreç doğruydu; kapsam eksikti.**
Kapsam artık takip edilenler + eklenecek olanlar (100 → 106 dosya).

### Onarıldı — görsel

62 sütunu aşan 9 satır · dingbat/emoji bloğundan 15 glif (61 karakter) ·
altı ayrı ok karakteri → iki · sayılan işaretle dolgu karışıyordu ·
26 kutu bir sütun kayıyordu · okur dosya anahtarı görüyordu · ızgara
dolgusu kitabın alfabesinde olmayan harfler taşıyordu.

### Değişti

- Levha bütçesi **112 → 103** (ölçüldü: yedi bulmaca çizelge taşır,
  son sorunun levhası iki kez sayılıyordu)
- Anlatı kuralı **ölçüye göre daraltıldı** (K42) — ve daraltma da
  fikstürle test edildi
- `qa_all.sh` belge tazelemesi ölçüm kapılarından SONRAYA alındı

### Test altyapısı

- `selftest` **213 → 242 denetim**
- Faz 5'te eklenen her kural, kırık bir kurguda ÇÖKTÜĞÜ GÖRÜLEREK eklendi

### Kapı

- `.gate` → **`phase5`**
- Rapor: `06_REPORTS/PHASE_5_REPORT.md` · `06_REPORTS/LINE_EDITOR_REPORT.md`
- Kararlar: **K42 · K43 · K44 · K45 · K46 · K47**

---

## [0.6.0] — 2026-08-24 · FAZ 4 · KAPI III–V + META-MİSTER (kurucu geçersiz kılması)

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

`externalValidation` **değişmedi**: `founder_override_partial` ·
`sessionsPerformed = 0` · `humanValidationPassed = false` ·
ölçülen karar **HARD-STOP**. Bu faz *insan tarafından test edilmiş* ya da
*harici olarak onaylanmış* diye anılamaz.

### Eklendi — 61 bulmaca, dokuz ısınma, bir son soru

- Kapı III · **The Calendar** (★★) · 20 bulmaca
- Kapı IV · **The Labyrinth** (★★★) · 20 bulmaca
- Kapı V · **The Mirror** (★★★) · 20 bulmaca — öz-göndergesel
- **THE LAST QUESTION** — meta-mister · beş kapının çıktısı tek sözcüğe
- **Dokuz ısınma örneği** (w9–w17) · her yeni mekanizma için bir tane
- Toplam **101 taslak** · 303 ipucu · 4762 aday dize elendi

### Eklendi — `qa_meta.py` · 29 denetim (K38)

Meta-mistere **meta olarak** bakan ilk kapı: beş kapının beşi de katkı
veriyor mu · katkılar gerçekten üretilebiliyor mu · **cevap kitapta
YOK mu** · basit birleştirmeyle okunuyor mu · başlıklarda geçiyor mu.

⚠ Ve kapının kendi sızıntı denetimleri **ilk yazımında sessizce yeşil
yanıyordu** (büyük harf anahtar ↔ katlanmış metin). **Fikstürler
yakaladı**, üretim verisi değil.

### Değişti — ⭑ AHA POLİTİKASI ÖLÇÜYE BAĞLANDI (K36) ⭑

Kitap geneli `ahaScore` ortancası 4,0'dı ve **yanıltıyordu**: Kapı
III–V'te tekrarlanan mekanizmalara da 4 ve 5 yazılmıştı. `g3-007`,
`g3-011` ve `g3-015`, `g3-001` ile **kelimesi kelimesine aynı talimatı**
taşıyor.

- **Tavan artık ölçülüyor**: ilk kullanım 5 · ölçülmüş derinleşme 4 ·
  düz tekrar 3. Yazar yalnızca AŞAĞI inebilir.
- **Eşik kapı bazında**: keşif kapıları (I·II) ≥ 4 · akıcılık kapıları
  (III–V) ≥ 3
- **Yerine çıkarım oranı** = dakika ÷ elle işlem — ölçülen
  **1,00 → 1,27 → 2,32 → 3,43 → 4,42**; akıcılık tabanı 2,0 ve
  yükselmek zorunda
- **On puan DÜŞÜRÜLDÜ**, hiçbiri şişirilmedi
- Aynı mekanizma koruması **kaldırılmadı, sertleştirildi**: tekrar artık
  5 alamaz
- Eşikler `project_config § experience` içinde — betiğe gömülü değil

### Onarıldı — ⭑ İKİ GERÇEK SIZINTI · GÖRSEL DENETİM BULDU ⭑

Anahtarlı alfabe levhası anahtar sözcüğü **satırın başında basar** ve
ipucu bunu okura açıkça söyler. İki kapının anahtarı bir CEVAPTI:

    g3-019'un anahtarı → g3-007'nin cevabıydı
    g5-019'un anahtarı → g5-013'ün cevabıydı

⚠ **Ve bu satırlar ilk yazımda sözcükleri AÇIKÇA yazıyordu.** Kanarya
commit'ten önce koştu ve kendi changelog'umu sızıntı olarak yakaladı —
haklıydı: anahtarlar değişti ama o sözcükler HÂLÂ birer cevap. K34'ün
dersi ikinci kez ölçüldü.

Anahtarlar `assign()` cevapları dağıtmadan **önce** elle seçilmişti ve
çakışma denetimi yoktu. Yeni anahtarlar hiçbir katalogun üyesi değildir
ve çakışma artık **üretim anında** çöker (`assert_keys_clean`).

### Onarıldı — 26 kutu bir sütun kayıyordu

Üç ayrı üreteçte bir-sütun hatası: sınıflama kutusunun ayırıcısı ·
sayı taşının içerik satırı · katman taşının "dize" satırı. Ekranda
görünmez, **basılı kutuda görünür**.

### Onarıldı — `pilot_pages.py` yanlış ölçüyordu (K39)

Betik Faz 2'de yazıldı; o gün yalnızca Kapı I vardı. Bütün kitabı
topluyor, **Kapı I'in bütçesiyle** karşılaştırıyor ve arka maddeyi **×5
ölçekliyordu**. Beş kapı yazılınca kırmızı yandı — içerik büyüdüğü için
değil, **ölçen bozuk olduğu için**. Ölçüm artık kapı bazında.

- **Araçlar levhası 2 → 4 sayfa** (408 satır · ölçülen 3,2) — sekiz yeni
  çizelge eklendi ve kısaltmak bir cevap uzayını yok ederdi (K22)
- **Sayfa modeli 236 → 238** · hedef 230 ± %6 içinde
- **Kelime sayısı ölçüldü: 17.211** — üretilen belgeler sabit `0`
  basıyordu

### Onarıldı — okur dosya anahtarı görüyordu (K40)

Kapı V'in yapı levhası `esik-alfabesi` gibi **dosya anahtarları**
basıyordu. Ad artık araçlar levhasından okunur; bilinmeyen anahtar
üretim anında çöker.

### Onarıldı — ölü künye

`caesar-suetonius` kaydedilmiş ama hiçbir bulmacada kullanılmıyordu →
`g1-013` ve `g1-017`e (kaydırmalı şifre) bağlandı.
`rawlinson-cuneiform` **çıkarıldı**: kayıt Babil altmışlık notasyonu
diyordu, kitabın sayı sistemi ise toplamalı/çıkarmalı bir işaret
dizisidir. Kaynağı tutmak, yapılmayan bir işi yapılmış göstermek olurdu.

### Değişti — üretilen belgelerin ÜRETECİ de bayatlayabilir

`ROADMAP_PROGRESS`'in "Sonraki izinli eylem" bölümü Faz 2'ye
**sabitlenmişti** ve Faz 4'te hâlâ "Faz 2'nin işi tamamlandı" diyordu.
Metin artık `.gate`ten türer.

### Test altyapısı

- `selftest` **195 → 213 denetim** · yeni `§ ⑨` bölümü
- **11 meta fikstürü** + **5 K36 fikstürü** — her yeni kural kırık bir
  kurguda ÇÖKÜYOR
- Eski "aynı imza ikinci kez 4+ alamaz" fikstürü yeni kurala taşındı

### Kapı

- `.gate` → **`phase4`**
- Rapor: `06_REPORTS/PHASE_4_REPORT.md`
- Kararlar: **K36 · K37 · K38 · K39 · K40 · K41**

---

## [0.5.0] — 2026-08-24 · FAZ 3 · KAPI II YAZILDI (kurucu geçersiz kılması)

# ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING

Kurucu, ikinci tur insan doğrulaması tamamlanmadan Faz 3'ün başlamasına
açıkça izin verdi. **Ölçülen öldürme kapısı hâlâ `HARD-STOP`'tur** ve
öyle raporlanmaya devam eder.

### Eklendi — kurucu geçersiz kılması, bir DÜĞME değil bir KAYIT (A13)

- `project_config § killGate.externalValidation` + `gates.gateStatus`
  makine okunur hâlde: `status=founder_override_partial` ·
  `sessionsPerformed=0` · `humanValidationPassed=false`
- ⭑ `kill_gate.py` kararı hâlâ **HARD-STOP olarak hesaplar, yazdırır ve
  rapora `verdict` alanıyla yazar**; geçersiz kılma yalnızca **çıkış
  kodunu** değiştirir
- ⭑ **Dört uydurma muhafızı** — sıfır oturumla "doğrulandı" denemez,
  bildirilen oturum sayısı diskte ölçüleni aşamaz, gerekçesiz kayıt
  olmaz, oturum yokken durum `validated` olamaz
- ⭑ **İş geçersiz kılınamaz**: `check_gate_scope` yalnızca *doğrulama*
  eşiğini karşılar. Faz 3 girişi ilk denendiğinde kapı **kırmızı yandı**
  (20 < 40) ve ancak Kapı II yazıldıktan sonra yeşile döndü
- `.gate` → `phase3`

### Eklendi — Kapı II · Yaratıklar (20 bulmaca · ★★)

- Karışım: levha içi şifre **6** · sınıflama **5** · kısıt mantığı 3 ·
  levha gözlemi 2 · yazı çözme 2 · yer değiştirme 1 · kapı 1
- Basılı yetke: **Çizelge E** (50 üyelik katalog) · **Çizelge F**
  (6×5 halka tablosu · Polybius) · **Çizelge G** (12 söz)
- ⭑ **B3 kapandı**: anahtarlı alfabe burada — ama satır **basılıdır**;
  okurdan yirmi dokuz harfi dizmesi istenmez
- Isınma **7 → 8 örnek** (sınıflama ailesi eklendi)
- Üç yeni kabul yordamı: `reachable-via-grid-coordinates` ·
  `misclassified-in-printed-pens` · `reachable-by-keyed-alphabet`

### ⭑ ★'dan ★★'ye geçilirken elle iş ARTMADI (K32)

| | Kapı I | Kapı II |
|---|---:|---:|
| Elle işlem | 100,8 | **133,5** |
| Bildirilen süre | 105 dk | **228 dk** |
| ⭑ Elle işin payı | %32 | **%20** |
| Bütçesini aşan | 0/20 | **0/20** |

Zorluk üç eksende arttı ve üçü de **düşüncedir**: kural verilmez bulunur ·
çapa basılı olmaktan çıkar (altı bulmacalık rampa) · mekanizmalar
zincirlenir (yayılma yarıçapı ≤1).

### Değişti — K4 tavanı zorlukla ölçeklenir, SESSİZCE DEĞİL (K33)

★ = 8 (değişmedi) · **★★ = 12**. Gerekçe K4'ün kendi metnidir: *"4–8
**anlamlı**"* ifadesini *"20–40 **tekrarlı**"*ya karşı koyar.
⭑ Asıl emniyet `repetitionBurden`dir ve **o ölçeklenmez**.

### Eklendi — iki yeni ölçüm betiği

- **`qa_plate_data.py`** (5 denetim) — yol haritası Faz 3 § 13'ün istediği
  baskı **ön** ölçümü. En ince ayrım **5** (tavan 5) · bit fazlalığı
  2,9× · trim'i aşan şekil 0. ⚠ **Baskı yapmaz**; gerçek ölçüm A9'dur
- **`solve_from_pack.py`** — cevap anahtarına **bakmadan**, yalnızca
  okurun eline geçenden çözer: **16/40 türetildi, 16 uyuştu, 0 uyuşmadı**.
  ⚠ İnsan testi **değildir**

### Düzeltildi — beş bulgu, hiçbiri okuyarak bulunmadı

1. Zincirler birbirine eklenmişti → yayılma yarıçapı 2
2. ⭑ Bir ad **ters çevrildiğinde** sık bir Türkçe ekin içine düşüyor ve
   beş dosyada geçiyordu (K34) — kanarya ters de arar
3. ⭑ İki çizelge hücresi **bağımlı olmadıkları** bulmacaların cevabını
   basıyordu; § ⑫ oraya bakmıyordu (K35) — artık üretim anında reddedilir
4. Akran havuzu tükendi; son levha iki etiketle kaldı
5. Bir Kapı I levhası trim'e sığmıyordu (66 > 62) — `qa_plate_data` buldu

### Ölçüldü — ve kurucuya girdi

- **Sayfa modeli 232 → 236**: ipucu bölümü 22 → **26** (ölçüldü;
  kısaltmak ipucu merdiveni kuralını kırardı)
- **Kelime yol haritası tahmininin yarısı**: iki kapı da öyle — üslup
  tahmin edilenden yoğun (A8 girdisi)

### Değişmedi

- ⛔ **Öldürme kapısı hâlâ `HARD-STOP`** · harici oturum **0**
- ⛔ **Hiçbir bulmaca `tested` değil** — kırkı da `drafted`
- ⛔ **Faz 4 başlatılmadı**
- ⛔ `EU_PER_MINUTE = 3` hâlâ kalibre edilmemiş (B5)
- `selftest` **185 → 195** denetim

---

## [0.4.0] — 2026-08-24 · DÜŞÜK SÜRTÜNME / YÜKSEK ÖDÜL (ikinci yönerge)

**Tasarım hedefi sıkıldı ve deneyim ölçüye girdi.** Elle iş
**184 → 101 işlem**; elle işin bildirilen süredeki payı **%58 → %32**;
bütçesini aşan bulmaca **0/20** — ama bu kez bütçe `dakika × 1,0`.

⚠ **Bildirilen sürelerin hiçbiri yükseltilmedi** (yönerge § 8 bunu
yasaklıyor). Düşen tek şey iş.

### Değişti — bütçe kuralı

- ⭑ `qa_effort` bütçesi `dakika × 3` → **`dakika × 1,0`** (K27).
  Üç bir gevşeklik payı değil, birim çevrimiydi; eski kural sürenin
  **tamamının** yürütmeye gitmesine izin veriyordu. Yeni kuralın okunuşu:
  **sürenin en çok üçte biri elle iştir**
- ⭑ **K4 tavanı**: en kötü hâlde bile **≤ 8 elle işlem** (kapı hariç)

### Düzeltildi — çaba modelinde bir gözden kaçma (K28)

`effort()` arama tipi mekanizmalarda beklenen maliyeti yarılıyordu — ama
yalnızca **ikisinde**. Levha araması ve çizelge elemesi yarılanmamıştı;
bu bir politika değil, Faz 2'nin son saatinden kalan bir tutarsızlıktı.

- `plate-attribute` bir **aramadır** → beklenen `(n+1)/2`, en kötü `n`
- `table-row` bir **elemedir** → ardışık benzetim (sözlük için zaten vardı)
- glif okuması **tek yöndür** — levha `▶` basar (K25'in aynısı)

⭑ Ve üçü de boşta durmuyor: `qa_readerpack § ⑨⑩⑪` varsayımları
denetler. Levha yön basmıyorsa, çizelge öbeklenmemişse veya boş ızgara
basılı değilse **ölçüm de düşer**.

Düzeltmenin payı ayrı raporlanır: **184 → 130 model**, **130 → 101
tasarım**.

### Eklendi — `04_BUILD/qa_experience.py` (14 denetim · K29)

Çaba işin **miktarını** ölçer; bu kapı **ödülü** kısıtlar.

- `ahaScore` ortancası ≥ 4 · ödülsüz bulmaca ≤ 2 · `repetitionBurden`
  ölçülür (yazardan değil, çaba modelinden)
- zorluk rampası: kolay başlangıç · uzun eziyet dizisi yok · küçük zaferler
- ısınma **her aileyi** gerektirilmeden önce öğretiyor mu (§ 7)
- ⚠ **`ahaScore` bir kanıt değildir** — yazarın kendi puanıdır. Kapı onu
  doğrulamaz, **şişirilmesini zorlaştırır**: 4+ veren her bulmaca ödülün
  **basılı yerini** göstermek zorundadır ve **aynı mekanizma ikinci kez
  4+ alamaz**

### Değişti — yirmi bulmaca

- ⭑ Altmış üyelik **elle tarama kaldırıldı** → **kesişim ızgarası**
  (18 → 7 işlem). Etiketler iddia değil, **ölçülebilir nitelik**:
  her hücre kendi satır ve sütun etiketine karşı denetlenir (§ 14)
- ⭑ Levha içi şifrede **dört kenar → üç kenar** (5,6 → 4,6 işlem) ve
  başlangıç bir **köşe değil, bir kenar** (köşe iki kenar gösterir)
- ⭑ Sıra değiştirmenin **boş ızgarası sayfaya basıldı** (8 → 6 işlem)
- ⭑ Altı levha bulmacası artık **altı AYRI şey** fark ettiriyor:
  eksik olan · yönelim · uzamsal ilişki · eşlik eşitliği · öbekleme ·
  bakışım (üretim anında denetlenir)
- Isınma bölümü **3 → 7 örnek** (B4 üç aileyi öğretiyordu; dördü
  çözülmüş örnek görmeden geliyordu)
- Kapı ifadesi **on beş harf**; on beş bulmaca harf verir, dördü sonraki
  bir bulmacanın basılı anahtarı olur — **on dokuzunun hepsi kullanılır**
- Çizelge C'nin on iki sözü de **on beş harf** (eskiden 17–24 idi ve okur
  satır sayarak bulmacayı çözmeden bitirebilirdi)

### Düzeltildi — üretimde kapıların yakaladığı beş kusur

1. Zincirler **birbirine eklenmişti** (A→B→C): yayılma yarıçapı 2
   → dört zincirin hiçbiri artık bir zincirin ucuna eklenmiyor
2. Kitabın **kendi adı** cevap olmuştu ve her sayfanın kısıt cümlesinde
   geçiyordu — cevap kendi sayfasında bedava duruyordu
3. *"Üç **basamaklı** okuma"* — ve `BASAMAK` bir çizelge üyesiydi;
   Türkçede hem merdiven basamağı hem sayı hanesi → *"üç haneli"*
4. ⭑ **Sekiz üye cevap olamazdı**: projenin kendi söz dağarcığıdır ve
   biri **commit mesajlarında** geçiyordu — geri alınamaz (K30).
   Yasak liste tahmin edilmedi, **ölçüldü**
5. Üç üçgen levhanın **metni ile şekli ayrışmıştı** ("sağ köşesinde"
   diyordu, şekil tabana basıyordu) → başlangıç kenarı tek kaynaktan

### Eklendi — `qa_readerpack § ⑫` · iki sayfanın kesişimi (K31)

Zincirli bir bulmaca kaynağının cevabını tüketicinin sayfasına basmak
zorundadır. O sütun kaynağın aday kümesiyle **tek üyede** kesişirse okur
kaynağı çözmeden cevabını **iki sayfaya bakarak** okur.

`§ ⑥` bunu göremiyordu — çünkü **tek sayfaya** bakar ve iki sayfa ayrı
ayrı temizdi. İki bulmacada gerçekten vardı.

> **Sızıntı sayfada değildi; sayfaların ARASINDAYDI.**

### Değişmedi

- ⛔ **Öldürme kapısı hâlâ `HARD-STOP`**, `.gate` hâlâ `phase1`
- ⛔ **Faz 3 başlatılmadı** · tek bloklayıcı: **A12b**
- ⛔ `EU_PER_MINUTE = 3` hâlâ **kalibre edilmemiş** (B5)
- ⛔ Fiziksel prova alınmadı (A9)
- `selftest` **162 → 179** denetim: yeni kapıların hepsi kendi kusurlu
  fikstürüyle **ısırdığı kanıtlanarak** duruyor

---

## [0.3.0] — 2026-08-13 · Kapı I YENİDEN TASARLANDI (B1–B6 onaylı)

**Yirmi bulmaca yeniden yazıldı.** Elle yapılacak iş **486 → 184 işlem**;
çabanın ima ettiği süre **162 → 61 dakika**; bütçesini aşan bulmaca
**6 → 0**.

### Değişti — beş tasarım kuralı

- **K1 · anahtar aranmaz, VERİLİR.** Kaydırma miktarı levhada basılı;
  okur işareti okur ve uygular. 84 işlem → **5**. Tekillik zayıflamadı:
  ispat yine altmış üyeyi sayar
- **K2 · her bulmaca kendi süre iddiasına sığar** — `qa_effort` ölçer
- **K3 · ispat sayar, okur gezmez**
- **K4 · her mekanizma çözülmüş bir örnekle önce öğretilir**
- **K5 · "aha" işi transkripsiyon işine baskın gelir**

### Karışım (B1)

levha gözlemi 5→**6** · kısıt mantığı 5→**4** · yazı çözme 2→**3** ·
levha içi şifre 2→**3** · yer değiştirme 3→**2** (anahtar basılı) ·
sıra değiştirme 2→**1** (genişlik basılı) · kapı **1**

- **B2** yansıma Kapı I'den **çıkarıldı** → Kapı IV
- **B3** anahtarlı alfabe **ertelendi** → Kapı II
- **B4** ⭑ **üç sayfalık ısınma bölümü YAZILDI** ⭑ — Faz 1'den beri
  sayfa bütçesindeydi ve boştu; çözücülerin *"mantık sıçraması fazla
  dik"* şikâyetinin doğrudan karşılığı
- **B5** çaba çarpanı **ertelendi** — ikinci turda gerçek süreyle kalibre
- **B6** ikinci tur kohortu: **2 dönen + 3 yeni**; aradaki fark öğrenme
  etkisinin büyüklüğünü verir

### Eklendi

- İki yeni mekanizma türü: `reachable-by-printed-shift` ·
  `reachable-by-printed-grid` — anahtarı basılı şifreler
- Yeni levhalar: tablet · dokuz karo · işaretli halka · sunak kenarı
- **Bulmaca başına kayıt formu** her bulmacanın altında basılı (B6):
  birinci turda yoktu ve öldürme kapısının beş ölçütü bu yüzden
  ölçülemedi

### Üretim sırasında kapılar üç kez ısırdı

- **üç sütun** birden "çentik = sütun numarası" eşitliğini sağlıyordu →
  `qa_answerspace` "kabul edilen 3" dedi
- bir levha etiketi (`KUYU`) sıradan bir Türkçe fiilin **içinde** geçiyordu
  (`o-kuyu-n`) → `qa_answerspace ⑦` yakaladı
- sözlük elemesi **33 işlem** tutuyordu (bütçe 21) → altı harfli adaya
  taşındı, **18 işleme** indi

---

## [0.2.1] — 2026-08-13 · A12 · ⛔ ÖLDÜRME KAPISI DÜŞTÜ

**5 harici Türkçe çözücüden 1'i Kapı I'i bitirdi.** Eşik ≥4, sert
durdurma <3. Karar: **HARD-STOP**. Kurucu kararı: **yeniden tasarla**.

Baskın bırakma sebebi *"çözemedim"* değildi: **"sıkıldım"**. Kaydırma,
yansıma ve anahtarlı alfabe bulmacaları kâğıt kalemle yorucuydu.

### Eklendi

- **`04_BUILD/qa_effort.py`** — ⭑ öldürme kapısını kaybettiren ÖLÇÜLMEMİŞ
  boyut ⭑. Okurun kaç elle işlem yapacağını **cevap uzayı
  spesifikasyonundan** hesaplar ve bulmacanın **kendi süre iddiasına**
  karşı denetler. Hangi bulmacaların şikâyet edildiğini bilmeden koştu ve
  **aynı üç bulmacayı aynı sırayla** işaretledi (4,7× · 3,0× · 1,6×)
- **`06_REPORTS/GATE_1_REDESIGN_PROPOSAL.md`** — yeni mekanizma karışımı,
  çaba bütçeleri, zorluk rampası, B1–B6 kararları. **Yeni bulmaca
  YAZILMADI**
- `01_SOURCE/playtests/` — ham oturum kayıtları · dizin, içine tek satır
  yazılmadan **ÖNCE** korumalı listeye alındı (mahremiyet)

### Değişti

- `kill_gate.py` — **oturum düzeyi** toplu kaydı okur. Bulmaca başına
  kayıt yoksa kalan beş ölçütü `measured: false` işaretler: *"ihlal
  edilmedi"* ile *"ölçülmedi"* aynı şey değildir
- Pilot kohortun **20/20 kaydı** `testStatus: "failed"` — kohort olarak
  test edildi, kohort olarak düştü
- `PROTECTED_DIRS` 4 → **5**
- `05_TESTS/selftest.py` — **154 → 162** denetim

### Ölçüldü

| | |
|---|---:|
| Kapı I'i bitiren | **1 / 5** |
| Toplam elle işlem | **486 EU** |
| Çabanın ima ettiği süre | **162 dk** (bildirilen 153) |
| Bütçesini aşan bulmaca | **6 / 20** |
| En kötü bulmaca | **9,3×** (6 dk iddia · 56 dk en kötü hâl) |

### Öğrenilen

- **K23** — ölçülmeyen bir boyut, korunmayan bir boyuttur
- **K24** — `expectedCompletionMinutes` **kavrayışı** ölçüyordu,
  **yürütmeyi** değil; fark dokuz kat
- **K25** — **ispat sayar, okur gezmez**: `minDomainSize` ispatın sayım
  alanıdır, okurun elle tarayacağı alan değil

---

## [0.2.0-pilot] — 2026-08-13 · Faz 2 · Pilot bulmacalar, cevap uzayı, öldürme kapısı

**Yirmi Türkçe pilot bulmaca yazıldı ve bütün teknik kapılardan geçti.
Öldürme kapısı kararı: `BLOCKED` — beş harici çözücü oturumu YAPILMADI.**

Bu bir başarısızlık değil, kapının çalışmasıdır: ölçemediği bir şeyi
geçmiş sayan bir öldürme kapısı, olmayan bir kapıdan tehlikelidir.

### Eklendi

- **`04_BUILD/qa_answerspace.py`** — ⭑ Faz 2'nin birinci teslimatı ⭑
  Cevap uzayını **bağımsız açar**: yazarın listesini okumaz, bulmacanın
  girdisinden ve basılı çizelgelerden yeniden üretir. 1.072 aday dize
  üretildi ve elendi; **20/20 tam olarak bir üye kabul etti**
- **`04_BUILD/qa_handoff.py`** — devir ve hata davranışı: hata tespiti,
  teşhis işaretleri, kurtarma yolu, tek bir hatanın yayılma yarıçapı ≤1.
  Hata tespitinin **gücü ölçüldü**: asgari Hamming mesafesi **15**
- **`04_BUILD/qa_readerpack.py`** — bütün kapıların paylaştığı körlüğü
  kapatır: hepsi korumalı katmanı denetliyordu, hiçbiri **okurun eline
  ne geçtiğine** bakmıyordu
- **`04_BUILD/kill_gate.py`** — beş değerli karar; **veri yoksa GEÇMEZ**
- **`04_BUILD/pilot_pages.py`** — model ilk kez **gerçek metne** vuruldu
- **`04_BUILD/english_readiness.py`** — dönüşüm iş listesi (dönüşüm
  BAŞLATILMADI · § 23)
- **`04_BUILD/plate_proof.py`** — baskıya hazır prova paketi (A9 kurucu işi)
- **`00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`** — A12 devir belgesi
- 20 Türkçe pilot bulmaca · 60 ipucu · 80 alternatif aday · 81 çözüm adımı
  (**korumalı katmanda, depoda değil**)

### Değişti

- `_protected_layer` ve `qa_solution_leak` — **Türkçe katlaması** `ı/İ/I → i`.
  NFKD noktasız `ı`yı çözmez; `"IŞIK"` ile `"ışık"` iki farklı normal
  biçime sahipti ve kanarya küçük harfli bir sızıntıyı **kaçırırdı**
- `qa_hints` — **düz merdiven de kusurdur**: eski kural yalnızca azalmayı
  yakalıyordu, `[4,4,4]` geçiyordu. Merdiven artık çözüm yolundan **türetilir**
- `mechanism_families` — levha içi şifrenin cevap biçimi **ölçümle**
  düzeltildi; `sequence` bir varsayımdı
- `puzzle.schema.json` — `answerSpace` · `languagePortability` ·
  `answerSpaceSize` · `pilotLanguage`
- `project_config.json` — `language` · `security` · `answerSpace` ·
  `gateHandoff` · `plateProof` blokları; A3/A8/A9/A11 kararları
- `05_TESTS/selftest.py` — **123 → 151** denetim

### Düzeltildi (kırmızı takım · 23 bulgu)

- ⭑ **Sayı tablosu hata TESPİT ETMİYORDU.** Sekiz olası okumanın **beşi**
  tablodaydı; her levha bulmacasının beş ulaşılabilir cevabı vardı. Kapı
  bunu görmüyordu çünkü kabul yordamı **doğru okumayı sabit yazıyordu** —
  K21'in öldürmeye çalıştığı totoloji, doğrulayıcının kendi içinde
- ⭑ **On bulmaca okur paketinde ÇÖZÜLEMİYORDU.** Levha metni vardı, levha
  verisi yoktu
- ⭑ **Gerçek bir ikinci cevap** — kaynağı tek bir yanlış edattı. Aynı
  bulmacada ikinci bir ikinci cevap daha bulundu (taban işareti çentik
  sayılabiliyordu) ve **iki okuma da tekillik vaadini yerel olarak
  sağlıyordu**
- Kök neden: şekil üretiliyordu, onu tarif eden cümle **elle yazılıyordu**.
  Levha üreteci artık *(şekil, künye)* çifti döndürür
- Sözlük sırası Türkçe harf sırasına göre **üretiliyor**; sözlük numaraları
  sözcükten **türetiliyor**
- Yansıma işlemi hiçbir yerde tanımlı değildi → araçlar levhasına kural ve
  örnek eklendi
- İki bulmacada okunacak levha basılı değildi → levhalar eklendi
- Çizelge harflerinde C boşluğu vardı

### Ölçüldü

| | |
|---|---:|
| Cevap uzayı · bağımsız üretilen aday | **1.072** |
| Tam olarak bir kabul | **20 / 20** |
| Kapı I gövdesi | 8,5 / 34 sayfa |
| İpucu bölümü (kitap ölçeğinde) | 15,2 / 22 sayfa |
| Çözüm bölümü (kitap ölçeğinde) | 8,4 / 18 sayfa |
| Kapı sözü asgari Hamming mesafesi | **15** |
| **Harici çözücü oturumu** | **0 / 5** |

### Ses kalibrasyonu (kurucu geri bildirimi · A5)

Kurucu pilot metinlerini *"mekanik olarak kusursuz ama anlatısal olarak
ölü"* buldu. Üç iç çözücünün hiçbiri bunu bildirmemişti — **çünkü üçü de
çözebiliyordu.** Okuma yorgunluğu yalnızca insanın ölçebileceği şeydir.

Teşhis üslup değil **mimariydi**: `STYLE § 1` iki kayıt tanımlar ve
pilotun yirmi bulmacası da **yalnızca talimat kaydında** yazılmıştı.

- Her bulmacaya **anlatı satırı** eklendi — mekanik içerik taşımaz
- Talimat sınav registerinden **arşivci** registerine taşındı; ≤20
  kelime/cümle kuralı korundu (ölçülen medyan **7**)
- İpuçlarındaki **kümülatif tekrar** kaldırıldı: üç kademe artık her biri
  YENİ bir adım getirir, köprü cümlesi kapsamı taşır
- Ön madde, sözleşme sayfası ve ipucu sayfası seslendirildi
- **`STYLE.md` v2.0** — bantlar gerçek metinden ölçüldü
- ⚠ Bulmaca metni bandı (90–220) **doğrulanmadı**: ölçülen medyan **51**.
  Bant **düşürülmedi**; zorluğa göre ayrılması Faz 3'e ertelendi

**Kanıt:** `qa_solvability` · `qa_hints` · `qa_uniqueness` yeniden koştu,
üçü de yeşil. Belirsizlik, cevap uzayı ve merdiven kapsamı değişmedi.
Geçiş sırasında kapı bir kez ısırdı: bir fısıltı son çözüm adımıyla iki
içerik kelimesi paylaşıyordu ve *cevap anahtarı* olarak kırmızı yandı.

### Güvenlik

- **`ENIGMATICA_CANARY_SALT`** üretildi (384 bit), GitHub Actions sırrı
  olarak kuruldu, depo dışında `0600` yedeğe yazıldı. **Plaintext hiçbir
  çıktıda, commit'te, raporda veya kaynak dosyada görünmedi.**
- Dört senaryo gerçek bir klonda kanıtlandı: doğru tuz yeşil · **eksik tuz
  kırmızı** · **yanlış tuz kırmızı** · **enjekte edilmiş sızıntı yakalandı**
- Kanarya bu fazda **kendi yazarını iki kez ısırdı**: selftest fikstürünü
  ve bulgu defterini sızıntı olarak bildirdi. İkisinde de haklıydı.

---

## [0.1.0] — 2026-08-13 · Faz 1 · Bulmaca mimarisi, çözülebilirlik, gizlilik

**Tek bir bulmaca yazılmadı.** Yazılan şey, yüz bulmacanın çözülebilir
olduğunu ispatlayacak makinedir.

### Eklendi

- **`01_SOURCE/mechanism_families.json`** — 17 mekanizma ailesi; her biri
  tanım · hedef zorluk · **tekillik ispatı** · kurgu örnek taşır
- **`01_SOURCE/gate_index.json`** — 5 kapı + son soru; bağımlılık ve
  yedek kuralları
- **`01_SOURCE/puzzle_index.json`** — **151 aday**, çözümsüz public kayıt;
  Kapı I'in 20 slotu Faz 2 pilot kohortu olarak işaretli
- **`01_SOURCE/research/sources.json`** — 16 künye, hepsi kamusal alan
- **`04_BUILD/qa_dependency.py`** — DAG: on kural, döngü yolunu raporlar
- **`04_BUILD/qa_taxonomy.py`** — çeşitlilik, ölü aile, metin karması, yedek havuz
- **`04_BUILD/page_budget.py`** — sayfa ve levha modeli; arka madde **türetilir**
- **`04_BUILD/validate_research.py`** — künye bütünlüğü ve doğrulama durumu
- **`04_BUILD/qa_solvability.py` · `qa_uniqueness.py` · `qa_hints.py`** —
  korumalı katman kapıları; boşken **sessizce yeşil yanmazlar**
- **`04_BUILD/qa_solution_leak.py`** — ⭑ **KANARYA** ⭑ alan adı değil
  **cevabın kendisini** arar: dosya, dosya adı, commit mesajı, yayın paketi
- **`04_BUILD/update_docs.py`** — `BOOK_STATS` ve `ROADMAP_PROGRESS` üretilir
- **`00_CONTEXT/`** — PUZZLE_TAXONOMY · SOLVER_TEST_PROTOCOL ·
  INTERNAL_SOLVER_PROTOCOL · RED_TEAM_CHECKLIST · SOURCING_STANDARD ·
  VISUAL_ARCHITECTURE · VALIDATION_REFERENCE
- **`06_REPORTS/PHASE_1_REPORT.md`**

### Değişti — kırmızı takım düzeltmeleri

İki bağımsız saldırı **36 bulgu** üretti; 30'u kapatıldı.

- `validate_structure.py` **yeniden yazıldı**: `git` aksadığında artık
  **kapalı başarısız** olur (eskiden bütün sızıntı denetimleri boş koşup
  yeşil yanıyordu); tarama bütün metin dosyalarına ve **Türkçeye** genişledi;
  muafiyetler **tam yol** oldu; config senkron denetimi eklendi
- `validate_spec.py` **yeniden yazıldı**: `puzzle.schema.json` artık
  **uygulanıyor** (`additionalProperties: false` → izin listesi) ve
  `testStatus: "tested"` **beş şartla kazanılıyor**
- `selftest.py` **123 denetime** çıktı; `validate_structure` fikstürleri
  **gerçek git deposu** kurar. Muafiyet listesi **donduruldu** — eski
  "gereklilik" testi bir muafiyeti meşrulaştırmanın yolunu tarif ediyordu
- `.gitignore` iki yerde **izin listesine** çevrildi; `06_REPORTS/` ve
  `01_SOURCE/puzzles/` kapatıldı; `01_SOURCE/design/` eklendi
- `puzzle.schema.json` **v2.0** — üç gizlilik sınıfı, `answerFormat`,
  `substitutableFor`, `boundToTextHash`
- **Kapı devri bağı kapatıldı** (K13) — bir yanlış kapı cevabı okuru
  ürünün %80'inden dışarıda bırakıyordu
- **Sayfa hedefi 208 → 230** (K17) — arka madde 24 sayfada imkânsızdı
- Kapı I'in zorluk eğrisi yeniden dizildi; imza mekaniğinin zorluk-1
  örneği eklendi; süre tahminleri şablon sabiti olmaktan çıktı
- Öldürme kapısına üç ölçüt: bulmaca başına çözücü tabanı, ipucu tüketimi
  tavanı, **medyan tanımı**
- Sözleşmenin **dördüncü sözü**: *kitap size bir çizelge veriyorsa, o
  çizelge tek yetkedir*

### Kararlar

**K13** (kapı devri kapatıldı) · **K14** (beşinci hat: kanarya) ·
**K15** (`tested` kazanılır) · **K16** (şema uygulanır) ·
**K17** (sayfa hedefi 230)

### Açık kararlar

A1 ✅ kapandı. Yeni: **A7** (bulmaca başına doğrulama) ·
**A8** (sayfa hedefi onayı) · **A9** (pilot levhalarının POD provası) ·
A10 (Faz 3'e ikinci öldürme kapısı) · **A11** (kanarya CI sırrı)

### Durum

`.gate` = `phase1` · **Faz 2 BAŞLAMADI** ·
⛔ **EXTERNAL VALIDATION PENDING** — beş harici çözücü yok (A3)

---

## [0.0.1] — 2026-08-12 · Bootstrap

Proje altyapısı kuruldu. **Hiçbir kitap içeriği üretilmedi.**

### Eklendi

- **Dizin mimarisi** — 26 dizin, `00_CONTEXT` … `09_ARCHIVE` şemasına uygun,
  bu projeye özgü eklerle: `01_SOURCE/puzzles`, **`01_SOURCE/solutions`**
  (korumalı), `05_TESTS/puzzle`, **`09_ARCHIVE/solutions`** (korumalı),
  `07_ASSETS/plates`
- **`project_config.json`** — makine okunur tek doğruluk kaynağı. Pazar
  raporunun sayıları `scope.locked: false` ile **hipotez** olarak işaretlendi
- **`CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md`** — altı faz,
  her fazda 19 alan: amaç, kapsam, teslimatlar, yazım hedefi, kelime/sayfa
  hedefi, araştırma, test altyapısı, QA kapıları, DoD, PASS, FAIL, ajan
  notları, kurucu bağımlılıkları, git kilometre taşı, CI, çıktılar, riskler,
  faz devri
- **`00_CONTEXT/SOLVABILITY_STANDARD.md`** — bu projenin birinci varoluşsal
  kuralı: *bir bulmaca "zekice göründüğü" için kabul edilemez*. Beş şart,
  belirsizlik ölçeği, alternatif çözüm prosedürü, dış bilgi yasağı ve
  **öldürme kapısı eşikleri**
- **`00_CONTEXT/CONTENT_PROTECTION.md`** — ikinci varoluşsal kural:
  iki katmanlı içerik ve **dört hatlı** çözüm koruması. *Ama kod sır değildir*
- **`00_CONTEXT/HINT_LADDER.md`** — üç kademeli ipucu (yönlendirme → yöntem →
  neredeyse-cevap); Cain's Jawbone'un terk oranına doğrudan cevap
- **`00_CONTEXT/STYLE.md`** v1.0 — anlatı süslü olabilir, **talimat asla**;
  belirsizlik anlatıda serbest, talimatta bir *çözülebilirlik ihlali*
- **`00_CONTEXT/LESSONS_FROM_CODEX.md`** — iki referans projeden taşınan
  yedi mekanizma ve altı ders; **kod taşınmadı, disiplin taşındı**
- **`01_SOURCE/puzzle.schema.json`** — **iki katmanlı** şema:
  `publicPuzzle` (depoda durur, çözüm alanı taşıyamaz) ve
  `protectedSolution` (depoda durmaz)
- **Test altyapısı** — `validate_spec.py` (veri + kapsam + kapı +
  **public katmanda çözüm taraması** + sözleşme ve öldürme kapısı
  eşiklerinin korunması), `validate_structure.py` (dosya + gömülü değer +
  sızıntı + sır + **⭑ çözüm sızıntısı ⭑**),
  `selftest.py` (**kapıların kendi testi**, **on altı** kusurlu kurgu)
- **`04_BUILD/qa_all.sh`** — CI'ın birebir aynısı; Faz 1–5'te doğacak
  kapılar için satırlar şimdiden yazıldı (K18 dersi: ölü betik olmasın)
- **`.github/workflows/validate.yml`** — altı iş; `structure` işi
  **çözüm sızıntısını** her push'ta denetler
- **`.gitignore`** — **dört hatlı** çözüm koruması

### Kararlar

K1 (ortak kütüphane yok) · K2 (`.gate`) · K3 (Codex adı taşınır, tür
taşınmaz) · **K4 (bir bulmaca "zekice göründüğü" için kabul edilemez)** ·
**K5 (⛔ Faz 2 bir ÖLDÜRME KAPISIDIR)** · K6 (üç kademeli ipucu) ·
K7 (kapılar üçüncü taraf paket kullanmaz) · K8 (kapsam hipotez) ·
K9 (Kindle üretilmez) · **K10 (iki katmanlı içerik, dört hatlı koruma)** ·
K11 (6×9 normal trim) · K12 (Kapı V dizgiye bağlı, en son kilitlenir)

### Açık kararlar

A1 (manuscript ve **çözüm katmanı** politikası · Faz 1 başlamadan) ·
A2 (5 kapı teması) · **A3 (5 harici çözücü · Faz 2 bloklayıcısı)** ·
A4 (doğrulama sayfası) · A5 (STYLE onayı) · A6 (yazar biyografisi)

### Durum

`.gate` = `phase0` · **Faz 1 BAŞLAMADI** · kurucu onayı bekleniyor
