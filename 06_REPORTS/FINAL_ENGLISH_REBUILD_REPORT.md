# FINAL ENGLISH REBUILD REPORT — Codex Enigmatica

> **26 Ağustos 2026** · kurucu yönergesi: *"THE FINAL COMMERCIAL BOOK MUST
> BE 100% ENGLISH."*
>
> Bu rapor bir çeviri raporu DEĞİLDİR. Yapılan iş bir **kaynak düzeyinde
> yeniden inşadır**: alfabe değişti, bütün cevaplar yeniden atandı, bütün
> şifreli dizeler yeniden üretildi, kataloglar sıfırdan kuruldu ve
> etkilenen levhalar yeniden çizildi.
>
> ⚠ **BU RAPOR CEVAP TAŞIMAZ.** Kanarya onu her koşuda tarar.

---

## 0 · Tek bakışta

| | Önce (Türkçe pilot) | Sonra (İngilizce ürün) |
|---|---|---|
| Manuscript dili | `tr` | **`en`** |
| Alfabe | 29 harf · 6 grup (5·5+4) | **26 harf · 6 grup (5·5·4·4·4·4)** |
| Kaydırma uzayı · ayna ekseni | 28 · 29 | **25 · 26** |
| Basılı sözcük katalogu | 5 (Türkçe) | **5 (İngilizce, sıfırdan)** |
| Bulmaca | 101 | **101** |
| İpucu | 303 | **303** |
| Ticari yüzeyde Türkçe sözcük | 9 533 | **0** |
| İç blok (ciltsiz / ciltli) | 262 / 263 sayfa | **274 / 274 sayfa** |
| Kelime (ölçülen) | 17 612 | **26 062** |
| Kalite kapıları | 2 kırmızı | **hepsi yeşil · `release` seviyesinde de** |

---

## 1 · Neden çeviri değil, yeniden inşa

Yönerge § 1 bunu talep ediyordu ve ölçüm onu doğruladı. Tek bir sayı
zinciri kırar:

```
Türk alfabesi 29 harf → altı işaret grubu 5·5+4
İngiliz alfabesi 26   → beşerli bölünce 5·5+1
```

**Beşerli bölme reddedildi ve gerekçesi ölçüldü.** 26 harfi beşerli
bölmek altıncı gruba TEK harf bırakır (Z). Kapı levhası her slot için o
harfin GRUBUNU basar — tek üyeli bir grup, o harfi bedava verir ve
kesişim ızgarasının bir satırını yok eder. Bölme dengelendi:

| grup | I | II | III | IV | V | VI |
|---|---|---|---|---|---|---|
| harf | A–E | F–J | K–N | O–R | S–V | W–Z |
| üye | 5 | 5 | 4 | 4 | 4 | 4 |

Ve **Çizelge F (Halka Tablosu) artık bu gruplardan türetilir**: bir
harfin Çizelge A'daki GRUBU ile Çizelge F'deki SATIRI aynı sayıdır.
Türkçe pilotta bu bir tesadüftü; İngilizcede bir garantidir.

`04_BUILD/english_readiness.py` bunu her koşuda ölçer ve tek üyeli bir
grubun geri gelmesini reddeder.

---

## 2 · Cevapları ÇÖZÜCÜ atadı, yazar değil

Yönerge § 8: *"The solver is the source of truth."*

Türkçe pilot Kapı I'in on dokuz cevabını **elle** listeliyor ve sonradan
assert'lerle doğruluyordu. Bu, yönergenin açıkça yasakladığı yordamdır ve
üç cevabın depoyla çarpışmasının da sebebiydi.

İngilizce katmanda `gate_common.assign()` **101 cevabın hepsini** dağıtır.
Kapı I'de bu tek bir çağrı değil, bir **aramadır**: üç koşul aynı anda
tutmak zorunda —

1. on beş slotun her biri kendi harfini taşıyan bir sözcük alır;
2. g1-011'in cevabıyla **aynı uzunlukta** bir sözcük artakalır (g1-008'in
   cevabının uzunluğu, g1-011'in basılı sütun kuralıdır);
3. artakalandan bir **kesişim ızgarası doldurulabilir**.

İlk koşu ① ve ②'yi tutturdu, ③'ü kırdı: çözücü uzun sözcükleri açgözlü
seçiyor ve zincire dayanacak bir şey bırakmıyordu. Arama artık üçünü de
koşul olarak taşır.

### Cevap yasağı ÖLÇÜLÜR, elde tutulmaz

Pilot, kanaryanın yakaladığı sözcükleri **elle** bir listede tutuyordu.
Böyle bir liste çürür. İngilizce katmanda yasak üretim anında hesaplanır:
kanaryanın kendi kurallarıyla (düz · sıkıştırılmış · TERS) takip edilen
dosyalar ve son iki yüz commit mesajı taranır.

Ölçülen: Eşik Sözlüğü'nün 72 üyesinden **2'si cevap olamaz**, yaratıklar
katalogunun ham listesinden **2 ad**, gök/geçit/ayna katalogundan
**17 ad** havuza hiç girmedi.

⚠ Ve bir sözcük **ön maddenin kendi cümlesinin içinde** yakalandı:
sözleşmenin ikinci sözü *"…knowledge from outside this book"* der ve bir
aday sözcük tam olarak orada saklanıyordu. Sözleşme cümlesi bir üretim
kısıtıdır ve değiştirilemez; **süzgeç genişledi, söz daralmadı**.

---

## 3 · Şifreli dizelerin tamamı yeniden üretildi

Türk alfabesiyle üretilmiş **hiçbir dize hayatta kalmadı**. Yeniden
üretilenler:

| mekanizma | ne değişti |
|---|---|
| kaydırmalı şifre | kaydırma uzayı 28 → 25; iki levhanın kaydırma miktarı yeniden seçildi |
| ızgara (yer değiştirme) | genişlik ve dize yeni cevaptan türetildi |
| çizgi yazısı (glif) | grup yapısı 5·5+4 → 5·5·4·4·4·4; her glif yeniden kodlandı |
| Polybius koordinatları | Çizelge F yeniden kuruldu; her istasyon çifti yeni |
| anahtarlı alfabe | üç anahtar yeniden seçildi (aşağıya bakınız) |
| ayna ekseni | eksen uzayı 29 → 26; eksenler yeniden seçildi |
| sayı işaretleri | katalog satır numaraları değişti → bütün işaret dizileri yeni |
| çevrim çizelgesi | katalog konumları değişti → bütün (dış, iç) çiftleri yeni |

### Anahtarlı alfabenin anahtarları

Pilotta üç anahtardan **ikisi başka bir bulmacanın cevabıydı** ve levha
onları satırın başında basıyordu. İngilizce katmanda anahtarlar **hiçbir
katalogun üyesi değildir** ve çakışma `assert_keys_clean` ile üretim
anında denetlenir. Kapı II'nin anahtarı da aynı sebeple değişti: pilotun
anahtarı katalog üyesiydi ve yalnızca çekilmediği için sızmamıştı.

---

## 4 · Meta-mister yeniden kuruldu — ve bir kez reddedildi

Beş kapı ifadesi birleştirilmez: her kapı kendi SAYISINI verir ve o sayı
**sondan** sayılan bir konumdur. Beş harf tek bir sözcük verir ve o sözcük
**kitapta yoktur**.

⚠ **İLK SEÇİM ÖLÇÜMLE REDDEDİLDİ.** Seçilen beş harfli sözcük,
`member` sözcüğünün İÇİNDE yaşıyordu — ve bu kitap neredeyse her sayfada
*"the answer is a member of Chart B"* der. `qa_meta § ⑦` son cevabı her
sayfanın SIKIŞTIRILMIŞ metninde arar; yüz kısıt cümlesinin her biri onu
"basılmış" diye bildirecekti. Kural yazıldı: **son cevap, kitabın
kullanacağı sıradan bir İngilizce sözcüğün alt dizesi olamaz.**

Beş kapı ifadesi buna göre yeniden seçildi. Ve on bir "dekor" ifadenin
**meta konumunda farklı harf taşıması** artık beş kapının beşinde de
üretim anında denetlenir — yoksa okur doğru ifadeyi bilmeden son soruyu
çözebilirdi.

---

## 5 · Kapıların kendisinde bulunan kusurlar

Yeniden inşa, **kapı katmanında** dört kusur açığa çıkardı. Hiçbiri
İngilizceye özgü değildi; hepsi Türkçe pilotta da vardı ve tesadüfen
görünmüyordu.

| # | kapı | kusur | neden görünmüyordu |
|---|---|---|---|
| ① | `qa_answerspace` | harf grubunu `i // 5` ile hesaplıyordu | 29 harfte doğru sonucu veriyordu; 26'da yedi bulmacayı "0 kabul" yapardı |
| ② | `qa_readerpack` | katalogları **ada göre** buluyordu (`endswith("katalogu")`) | Türkçe adlarla eşleşiyordu; yeniden adlandırma onu sessizce boşaltırdı |
| ③ | `qa_readerpack` | etiket numarasını yalnızca Eşik Sözlüğü'nde arıyordu | Kapı II numaraları tesadüfen `0` rakamı içeriyordu |
| ④ | `qa_crossref` · `qa_editorial` · `qa_meta` | çizelge/uzunluk göndermelerini **Türkçe kalıpla** arıyordu | İngilizce metinde hiçbir şey eşleşmez ve kapı ya sessiz kalır ya yanlış kırmızı yanar |

Dördü de onarıldı ve `05_TESTS/selftest.py` fikstürleri İngilizceye
taşındı: **242 denetim yeşil — bütün kapılar ısırıyor.**

---

## 6 · Dizgi katmanında bulunan kusurlar

Bunlar Türkçe baskıda da vardı ve **ticari kitabı doğrudan bozuyordu**.

| # | nerede | kusur |
|---|---|---|
| ⑤ | iç blok · Kindle | `printed: false` işaretli çizelge **basılıyordu** — o çizelge son sorunun aday listesidir ve **cevabı içerir** |
| ⑥ | iç blok · Kindle | on yedi çözülmüş örneğin **şekli ve çözüm adımları hiç basılmıyordu**; yalnızca onları ANLATAN iki alan basılıyordu |
| ⑦ | iç blok · Kindle | ön/arka madde **satır başına bir paragraf** diziliyordu; kapı açılışları ise ham Python listesi olarak basılıyordu |
| ⑧ | iç blok · Kindle | sözleşmenin dört sözü **(söz, açıklama) demeti** olarak, şifre referansı **on bir demet** olarak basılıyordu |
| ⑨ | iç blok | sözleşme sayfası `verificationPending` alanını — **kurucuya ait açık bir iş kaydını** — okura doğrulama adresi diye basıyordu |
| ⑩ | iç blok | son soru bölümü **iki kez** basılıyor ve altına **Kapı V'in açılışı** kopyalanıyordu |
| ⑪ | iç blok | `**kalın**` işaretleri olduğu gibi basılıyordu — on yedi örnek cevabını yıldızlar içinde gösteriyordu |
| ⑫ | iç blok | bir levha şekli **sayfa sınırında ikiye bölünebiliyordu** (g2-015: yedi istasyonun dördü bir sayfada, üçü ötekinde) |
| ⑬ | iç blok | dört arka madde başlığı **iki kez** basılıyordu (`SOURCES SOURCES`) |
| ⑭ | Kapı III–V (61 sayfa) | `AMAÇ` ve `GİRDİ` **aynı cümleyi** taşıyordu |
| ⑮ | çevrim levhası | gönderdiği çizelgenin adını **kesiyordu** (`→ the Sky C`) |

Hepsi onarıldı. ⑤ ve ⑨ ürünü bitiren cinstendi: biri son sorunun cevabını
kitaba basıyordu, öteki sözleşmenin doğrulama vaadini bir yer tutucuyla
karşılıyordu.

⭑ Dizgi yardımcıları artık **tek yerdedir** (`_protected_layer § TYPESETTING`):
iki üretici (baskı ve Kindle) aynı kodu paylaşır. Kusurların yarısı, iki
üreticinin ayrı ayrı yazılmış kopyalarından doğmuştu.

---

## 7 · Levhalar — 103'ün envanteri

Levhanın **değiştirilemez veri sözleşmesi** (kaç işaret, kaç bant, kaç
istasyon) karşılaştırıldı:

| | levha |
|---|---:|
| sözleşmesi DEĞİŞMEDİ | **72** |
| sözleşmesi DEĞİŞTİ → yeniden çizildi | **31** |
| **toplam** | **103** |

31'inin tamamı **deterministik olarak yeniden çizildi** — maliyet 0,00 $.

⭑ **VE BU BİR KISAYOL DEĞİL, PROJENİN KENDİ ÖLÇÜMÜNÜN SONUCUDUR.**
`OPENAI_14_ENGRAVINGS_COST_REPORT` şunu kayda geçirmişti: yedi istasyon
isteyen bir sözleşme görsel modele **üç kez** verildi ve **8, 12, 12**
istasyonla geri geldi. Üslup düzeldi, sayı düzelmedi. Aynı sonuç ikinci
kez geçerlidir: **model sayamıyorsa sayma işi modele verilmez.**

`plate_render.py` bu yüzden genişletildi:

* daha önce yalnızca iki aile çizilebiliyordu (halka · sıra);
* şimdi geri kalan her aile **cetvelli tablet** olarak çizilir — sözleşmesi
  zaten yalnızca (sayılan işaretler, bant sayısı) taşır;
* çerçevesi gravürcünün kendi dokusunu taşır (iki cetvel arasında sık
  paralel burin çizgisi) ve levha kimliğinden türeyen üç ayrı işlemden
  birini alır, böylece 31 tablet birbirinin kopyası olmaz.

⚠ **VE BİR KUSUR ONARILDI:** `_mark` yalnızca dokuz karakteri tanıyordu;
Çizelge A'nın **altı işareti** de aynı dolu noktaya düşüyordu. Yazı çözme
levhaları tam olarak o altı işaretten kuruludur — ikisi ayırt edilemezse
levha bir harf değil, bir nokta dizisi basar. Altı işaret artık **çizgiye
göre** çizilir (üstünde/altında/keserek · dik/eğik) ve çizgi de basılır.

⚑ **DÜRÜST SINIR:** 31 tablet, kalan 72 gravürden **görsel olarak daha
sadedir**. Üslup sözlüğü (krem zemin, siyah çizgi, tarama, cetvel çerçeve)
ortaktır ve sayılar kesindir; ama detay yoğunluğu eşit değildir. Bu bir
kurucu kararıdır: **kesin ama sade** ile **zengin ama yanlış sayılı**
arasında birincisi seçildi.

---

## 8 · Ölçülen ticari sonuç

| | ciltsiz | ciltli | Kindle |
|---|---:|---:|---:|
| sayfa | 274 | 274 | — |
| sırt | 0,6850 in | 0,8058 in | — |
| tam kapak | 12,935 × 9,250 in | 14,382 × 10,417 in | — |
| dosya | 70,4 MB | 67,3 MB | 46,0 MB |
| liste | 19,99 $ | 29,99 $ | 9,99 $ |
| baskı maliyeti | 4,138 $ | 8,938 $ | teslimat 6,905 $ |
| **telif** | **7,856 $** | **9,056 $** | **3,497 $ (%35)** |
| marj | %39,3 | %30,2 | — |

⚠ **KINDLE PLANI %35 OLMALIDIR.** 46,0 MB'lık dosyada %70 planının
teslimat ücreti 6,905 $'dır ve telifi 0,088 $'a düşürür. %70'in kârlı
olduğu sınır ölçüldü: **~23,3 MB**.

⚠ **CİLTLİ HESAPLAYICI 263 SAYFAYLA KOŞMUŞTU**, iç blok 274. Betik sırtı
+0,0203 in düzeltti ve bunu SÖYLÜYOR; kesinlik isteniyorsa kurucu
`hardcover-calculator.png` değerlerini 274 sayfayla yenilemelidir (A-yeni).

---

## 9 · Kalite kapıları

`./04_BUILD/qa_all.sh release` → **bütün kapılar yeşil**.

| kapı | sonuç |
|---|---|
| veri bütünlüğü · depo bütünlüğü | 58 + 98 denetim |
| **kapıların kendi testi** | **242 denetim — hepsi ısırıyor** |
| bağımlılık (DAG) · devir | döngüsüz · yayılma yarıçapı ≤ 1 |
| **cevap uzayı** | **101/101 tekil · 5 086 aday dize elendi** |
| çözülebilirlik · alternatif çözüm | 404 adım · 404 aday |
| ipucu bütünlüğü | 303 ipucu · merdiven yükseliyor · son adım verilmiyor |
| çaba bütçesi | 719 elle işlem · hiçbiri tavanı aşmıyor |
| deneyim | aha 4,0/4,0/3,0/3,0/3,0 · çıkarım 1,00→4,08 |
| okur paketi | 101 sayfa · 14 denetim |
| meta-mister | 5 kapı katkısı · **cevap kitapta YOK** |
| levha okunabilirliği | 125 şekil · en geniş 61/62 sütun |
| **çözüm kanaryası** | **143 dosya · sızıntı yok · künye yenilendi (293 cevap → 457 karma)** |
| **dil kapısı** | **0 Türkçe sözcük** |
| KDP paketi + preflight | 30 denetim · 3 + 7 dosya |

---

## 10 · ⚠ DEĞİŞMEYEN GERÇEK

> ### HARİCİ İNSAN DOĞRULAMASI YAPILMADI.
>
> | | |
> |---|---|
> | Ölçülen öldürme kapısı | ⛔ **HARD-STOP** — değişmedi |
> | Harici çözücü oturumu | **0 / 5** |
> | `humanValidationPassed` | **false** |
> | `founder_override_partial` | **true** |
>
> **Yeniden inşa bir doğrulama değildir.** Türkçe pilot doğrulanmamıştı;
> İngilizce yeniden inşa da doğrulanmadı. İkisi aynı boşluğa bakar ve o
> boşluk A12/A12b'dir.

Kalan kurucu işleri:

| # | ne | neden ajan yapamaz |
|---|---|---|
| **A12b** | beş harici çözücü oturumu | insan gerektirir |
| **A9** | POD prova kopyası — mürekkebin kâğıt üzerindeki davranışı | fiziksel |
| **A4** | doğrulama sayfasının barındırılması ve adresi | kurucu altyapısı |
| **A-yeni** | ciltli hesaplayıcının 274 sayfayla yenilenmesi | kurucu aracı |
| — | ISBN · AI açıklaması | KDP paneli |
| — | 31 tabletin gravür üslubuna yükseltilmesi (isteğe bağlı) | bütçe kararı |

---

## 11 · Kaynak doğruluk ilişkisi

```
01_SOURCE/design/_generator_en/     ← ⭑ İNGİLİZCE KAYNAK · TEK YETKE ⭑
        │  plate · bestiary · charts345      alfabe ve basılı çizelgeler
        │  gate_common                       kanarya süzgeci + ÇÖZÜCÜ
        │  build_gate1 · build_gate2 · build_gate345
        │  plates · plates2 · plates345      şekil VE künye tek kaynaktan
        │  voice · voice2 · voice345         anlatı ve talimat
        │  warmup345 · matter                ısınma · ön/arka madde
        │  emit · emit2 · emit345            korumalı katmanı yazar
        │  index_update                      public metadata
        ▼
01_SOURCE/design/*.json · 01_SOURCE/solutions/*.json · 02_MANUSCRIPT/book.json
        ▼
04_BUILD/interior · covers · kindle · metadata · kdp_package
        ▼
08_OUTPUT/PAPERBACK · HARDCOVER · KINDLE · APLUS

09_ARCHIVE/pilot-tr/                ← Türkçe pilot · TARİHSEL · üretim OKUMAZ
        generator/ · design/ · solutions/ · manuscript/
```

Türkçe pilot **silinmedi**: üreteci ve bütün çıktısı
`09_ARCHIVE/pilot-tr/` altında durur. Üretim hattı oraya **hiç bakmaz**.

---

*— Faz 6 · İngilizce ticari sürüm · 26 Ağustos 2026*
