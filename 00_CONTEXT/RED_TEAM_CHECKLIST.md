# KIRMIZI TAKIM — kontrol listesi ve bulgu defteri

> *"Zeki bir okur bunu nasıl kırar?"*
>
> Sürüm 1.0 · Faz 1 · Bulgu defteri her fazda **büyür**, kısalmaz

---

## 1 · Bulmaca başına kontrol listesi

Her bulmaca için, harici teste gönderilmeden önce **on iki soru**. Hepsi
`01_SOURCE/design/*.json § redTeamNotes` içine yanıtlanır.

### Cevabın tekilliği

1. **Alternatif cevap** — ölçütü sağlayan ikinci bir dize var mı?
2. **Ters ve ayna** — yolun tersi, dizinin tersi, haritanın aynası da geçerli mi?
3. **Kapsayıcı/dışlayıcı** — sayım bir eksik veya bir fazla yapılabilir mi?
4. **Notasyon önçözümü** — basılı işaret birden çok değere karşılık geliyor mu?

### İfadenin belirsizliği

5. **Eşanlamlı** — cevabın başka bir adı var mı? (Folklor tabanlı bir kitapta
   **genellikle vardır**)
6. **Noktalama** — cümle noktalama olmadan da aynı şeyi mi söylüyor?
7. **Sıfat tuzağı** — *saklı · farklı · tuhaf · yersiz* geçiyor mu?
   Geçiyorsa **yeniden yaz**: bunlar yüklem değildir.
8. **Yön ve başlangıç** — okuma yönü ve başlangıç noktası metinde sabit mi?

### Bilgi ve kaynak

9. **Dış bilgi** — bir adım kitabın dışına çıkıyor mu?
10. **Dış bilgi ÇELİŞKİSİ** — konuyu **bilen** bir okur farklı bir cevaba
    varır mı? (Sözleşmenin dördüncü sözü tam olarak bunun içindir)

### Yapı

11. **Kısayol** — bulmaca, tasarlanan yol dışından çözülebiliyor mu?
12. **Sızıntı** — başlık, ipucu veya levha cevabı erken veriyor mu?

---

## 2 · Sistem düzeyi kontrol listesi

Her fazın sonunda:

- [ ] Bir ipucu, ait olmadığı bir bulmacanın cevabını veriyor mu
- [ ] İki bulmaca aynı cevabı veriyor mu (kapı bulmacası girdileri ayırt edemez)
- [ ] Kapı bulmacasının hata davranışı: bir girdi yanlışsa çıktı
      **tespit edilebilir** biçimde geçersiz mi, yoksa makul görünen başka
      bir dize mi
- [ ] Metne bağlı bulmacaların karması güncel mi
- [ ] Levha düzenlendi mi — düzenlendiyse ispat **yeniden** koştu mu
- [ ] Doğrulama sayfası normalizasyonu sözleşme sayfasıyla aynı mı

---

## 3 · FAZ 1 BULGU DEFTERİ

İki bağımsız alt-ajan saldırdı. **36 bulgu.** Hiçbiri yumuşatılmadı.

### 3.1 · Mimari saldırısı — kabul edilen ve kapatılan

| # | Bulgu | Nasıl kapatıldı |
|---|---|---|
| A1 | **Kapalı başarısızlık:** `git ls-files` çalışmazsa liste boş dönüyor, bütün sızıntı denetimleri boş koşup **yeşil yanıyordu** | `.git` varken boş liste artık **hata**; `≥20 dosya` şartı |
| A2 | `01_SOURCE/design/` — şemanın kendi PROTECTED katmanı — ne `.gitignore`'da ne `PROTECTED_DIRS`'te | İkisine de eklendi; `.gitignore` kapsaması `git check-ignore` ile **denetleniyor** |
| A3 | **Şemayı hiçbir kod okumuyordu.** 355 satır `additionalProperties:false` tanımı, yalnızca "var mı" diye denetleniyordu | `validate_spec` şemayı **uyguluyor**; izin listesi artık gerçek |
| A4 | Uzantı süzgeci: yalnızca 5 uzantı, **büyük/küçük harfe duyarlı**. `ANSWERS.JSON`, `leak.yml`, uzantısız dosya geçiyordu | Takip edilen **her metin dosyası** taranıyor; uzantı küçük harfe çevriliyor |
| A5 | Tarama alan **adı** arıyordu, **cevap** aramıyordu. Türkçe hiç yoktu | Değer tarafı iki dilde eklendi **+** `qa_solution_leak.py` kanaryası |
| A6 | `README.md` / `.gitkeep` muafiyeti **temel adaydı**: her alt dizin bir bedava dosya kazanıyordu | Muafiyet **tam yol**; muaf dosyalar yine içerik taramasından geçiyor |
| A7 | **Öldürme kapısı bir metin alanıydı.** 140 kaydın `status` alanını elle değiştirmek phase1'den release'e yürüyordu | `check_test_status`: beş şart + `status`↔`testStatus` bağı + kurucu onayı kilidi |
| A8 | Belirsizlik denetimi **opt-in**: alanı silmek denetimi kapatıyordu | Alan `validated`/`written` için **zorunlu** |
| A9 | selftest, `validate_structure`'ın **hiçbir** denetimini koşmuyordu | `run_structure_with()` — gerçek git deposu kuran fikstürler |
| A10 | Muafiyet "gereklilik" testi **tersti**: yeni bir muafiyeti meşrulaştırmanın yolu dosyaya çözüm işareti koymaktı | Liste **donduruldu**; tam küme eşitliği aranıyor |
| A11 | `06_REPORTS/*.json` takip ediliyor **ve CI artefaktı olarak yükleniyordu** — `qa_uniqueness` yapısı gereği cevap adaylarını yazacaktı | `.gitignore` izin listesine çevrildi; yalnızca `06_REPORTS/tracked/` |
| A12 | Commit **mesajları** hiç taranmıyordu — kalıcı ve geri alınamaz | Kanarya son 100 mesajı tarıyor |
| A13 | Dosya **adları** taranmıyordu (`plateId` içinde cevap) | Kanarya yolları da tarıyor |
| A14 | `01_SOURCE/puzzles/` yalnızca iki sonek için korunuyordu | İzin listesine çevrildi (`*.public.json`) |
| A15 | `PROTECTED_DIRS` diskte olmayan bir dizin içeriyordu; yazım hatası fark edilmezdi | Dizinler oluşturuldu; varlık + `.gitignore` kapsaması denetleniyor |
| A16 | Belge, kodun yapmadığı korumaları iddia ediyordu (4 muafiyet yazıyor, kodda 2 var) | Belge düzeltildi; selftest tam küme eşitliği arıyor |
| A17 | `SOLUTION_FIELD_MARKERS` elle yazılmış regexler; config listesiyle ayrışabilirdi | Kalıplar **adlardan türetiliyor**; üç yönlü senkron denetimi |
| A18 | Kurucu değeri taraması 4 uzantıyla sınırlıydı | Kod **ve veri** uzantılarına genişletildi (proza bilerek dışarıda — gerekçe kodda) |

### 3.2 · Tasarım saldırısı — kabul edilen ve uygulanan

| # | Bulgu | Nasıl karşılandı |
|---|---|---|
| T1 | **Kapı devri bağı**: bir kapıyı yanlış çözen okur ürünün %80'ine kapanıyordu, hiçbir teşhis olmadan | `crossGateEntryHandoff` → **false**. Devir anlatısal; kapılar bağımsız girilebilir |
| T2 | **Arka madde 24 sayfada imkânsızdı** — 300 ipucu + 100 çözüm ≈ 44 sayfa. Taşma dizgiyi kaydırır ve Kapı V'in sekiz bulmacasını kırar | Sayfa hedefi 208 → **230**; arka madde artık **türetiliyor**, elle yazılmıyor |
| T3 | Kapı I'de altı ardışık aynı aile, **iki kez** | Yeniden dizildi; en uzun ardışık dizi **2** |
| T4 | Kitabın **imza mekaniğinin** zorluk-1 örneği hiçbir yerde yoktu | `plate-embedded-cipher` bandı 1'e indi; Kapı I'e iki örnek |
| T5 | Süre tahminleri **şablon sabitiydi** (27 kayıtta aynı sayı) ve oturum yükü modelde yoktu | Slot bazlı rampa + 45 dk oturum yükü; `page_budget` düz eğriyi **kırmızı yakıyor** |
| T6 | `puzzlesUnsolvedByAllSolvers: 0` ölçütü, 5'te 1 çözülen bulmacayı geçiriyordu | `minSolversPerPuzzle: 2` eklendi |
| T7 | İpucu tüketimi hiç ölçülmüyordu | `maxSolversNeedingLevel3Hint: 2` + kayıt alanı |
| T8 | **Medyan tanımsızdı** — DNF varken hangi medyan? | `dnf-counts-as-cap`: bir DNF medyanı iyileştiremez |
| T9 | Cevap biçimi hiçbir yerde tanımlı değildi | `answerFormat` + `answerNormalization`, sözleşme sayfasında basılı |
| T10 | Metne bağlı 19 bulmaca, metne **bağlı değildi** | `boundToTextHash` + `qa_taxonomy § ⑨` |
| T11 | Her kapıda **tek** kapı bulmacası adayı — en kritik bulmacanın yedeği sıfır | Kapı başına ≥2; yedekler `substitutableFor` ile **çapraz aileye** bağlandı |
| T12 | Dokuz ailenin `validationMethod`'u ispat değildi | `answerSpace` şartı kabul edildi — **Faz 2'nin ilk teslimatı** |
| T13 | `classification` analizle tekilleştirilemez (~5,6 beklenen sahte ayrım) | Aile ancak **basılı nitelik matrisiyle** kullanılabilir; kural taksonomiye yazıldı |
| T14 | `plate-observation` yüklemi öznel; künye çizimden çıkarılıyordu (dairesel) | Kabul edilebilir yüklem listesi + **künye önce, gravür sonra** kuralı |
| T15 | `path-graph` simetrisi risk profilinde vardı, **ispatta yoktu** | Otomorfizma ve yön şartı taksonomiye yazıldı |
| T16 | İpucu alt dize denetimi **ters basımla** atlatılabilir (`HINT_LADDER § 3` ipuçları ters basar) | `qa_hints` dört gizleme biçimini deniyor; kanarya künyesi **ters karmaları** da taşıyor |
| T17 | Ogham/runik: **bilen** okur kitapla çelişebilir | Sözleşmenin **dördüncü sözü** + yalnızca yaygın değerle çakışan glif kuralı |
| T18 | İpucu uzunluk kuralları çelişiyordu (40 kelime vs. "bulmacadan kısa") | Kural "**tek bir ipucu** bulmacadan uzun olamaz" olarak netleşti |

### 3.3 · Kabul edilen ama FAZ 1'DE UYGULANMAYAN — kurucu kararı bekliyor

| # | Bulgu | Neden ertelendi | Karar |
|---|---|---|---|
| T19 | **Bulmaca başına doğrulama** — kapı tamamlama olasılığı p¹⁹; 18/19 çözen okur hangi ikisinin yanlış olduğunu bilemez ve ipucu merdiveni işe yaramaz | Doğrulama sayfası barındırma kararı kurucununn | **A7** |
| T20 | **Pilot levhaların POD provası Faz 2'ye** — 20 pilot bulmacadan 9'u levha taşıyor; ekranda test edilen bir levha bulmacası test edilmemiştir | Prova siparişi kurucununn; yol haritası değişikliği | **A9** |
| T21 | **Faz 3'e ikinci öldürme kapısı** — en yüksek riskli üç aile Kapı I'de **yok**; en sert test en güvenli bulmacalara uygulanıyor | Yol haritası değişikliği | **A10** |
| T22 | Sayfa hedefi 208 → 230 (telif 9,85 $ → 9,58 $) | Ticari etki | **A8** |

### 3.4 · Reddedilen

| Bulgu | Neden reddedildi |
|---|---|
| "Yol haritası gövde sayfasında 68 sayfalık çelişki var" | Yanlış okuma: yol haritası Faz 4 § 6'daki *~102 gövde* o fazın **artışıdır**, toplam değil. Gerçek tutarsızlık arka maddedeydi (T2) ve düzeltildi |
| "`classification` ailesi silinsin" | Kapı II'nin teması ve portföy içi çapraz satışın taşıyıcısı. Silmek yerine **ispatlanabilir** hâle getirildi (T13) |

---

## 4 · Kapatılmayan bir şey: taramanın sınırı

`validate_structure` alan **adı** ve **etiket** arar. `qa_solution_leak`
kanaryası cevabın **kendisini** arar — ama yalnızca korumalı katman
yerelde varken veya CI'da tuz kuruluyken.

> **Etiketsiz düz proza içinde, tuz kurulu değilken yazılmış bir cevap
> yakalanmaz.**

Bu sınır burada yazılıdır çünkü bir kapının ne **yapmadığını** bilmemek,
onu olduğundan güçlü sanmaktır. Kapatılması `ENIGMATICA_CANARY_SALT`
CI sırrının kurulmasına bağlıdır (**A11**).

---

## 5 · FAZ 2 BULGU DEFTERİ — pilot kohortu (Kapı I · 20 bulmaca)

> Sürüm 1.1 · 13 Ağustos 2026
>
> Bu bölümdeki her bulgu **ölçülmüştür**, tahmin edilmemiştir. Her birinin
> ya bir kapı denetimi ya da bir kasıtlı-kusur fikstürü vardır — **çoğunun
> ikisi de**. Bir bulguyu düzeltip fikstürünü yazmamak, aynı kusuru bir
> sonraki fazda yeniden bulmaya davetiyedir.

### 5.1 · Bulguların kaynağı

| Kaynak | Bulgu |
|---|---:|
| Ön denetim (bulmaca yazılmadan) | 2 |
| Kapıların üretim verisinde yakaladığı | 9 |
| Solver B — bağımsız iç çözücü | 12 |
| Solver C — doğrulama geçişi | 12 |
| Solver D — son doğrulama geçişi | 4 |
| CI'ın kendisi | 1 |
| **Toplam kapatılan** | **28** |

### 5.2 · ⭑ F2-01 · SAYI TABLOSU HATA TESPİT ETMİYORDU ⭑ — en ağır bulgu

**Bulgu.** Levha içi şifre bulmacalarında (`g1-008`, `g1-016`) okur dört
kenarı okur. Başlangıç köşesi ve yön yanlışsa **sekiz** farklı dörtlü
çıkar. Tasarım *"yanlış okuma Çizelge E'de yoktur, yani hata tespit
edilir"* diyordu.

**Ölçüm.** Sekiz okumanın **beşi** tablodaydı. Yani her levha bulmacasının
**beş ulaşılabilir cevabı** vardı — ve ikisi diğer bulmacanın doğru
cevabıydı.

**Neden hiçbir kapı görmedi.** `qa_answerspace` "tam olarak bir üye kabul
ediliyor" diyordu ve **yanılıyordu**, çünkü kabul yordamı **doğru okumayı
sabit yazıyordu**:

```
"acceptance": {"kind": "reachable-via-number-table", "reading": "2413"}
                                                     ^^^^^^^^^^^^^^^^^
                                     yazar doğru cevabı kapıya SÖYLÜYOR
```

Bu, K21'in öldürmeye çalıştığı totolojinin ta kendisidir — bu kez
**kapının kendi içinde**. *Sayım alanını cevabı zaten bilen yazar
tanımlıyordu.*

**Kapatıldı.** Kabul yordamı artık **sekiz okumanın tamamını** taşır ve
kapı tam olarak birinin tabloda bulunmasını arar. Çizelge E yeniden
tasarlandı: iki levha **ayrı sayı kümesi** kullanır ({1,2,3,4} ve
{1,2,3,5}), böylece birinin yanlış okuması ötekinin doğru okumasına
düşemez. Fikstür: `selftest § ⑧ "SEKİZ OKUMANIN İKİSİ TABLODAYSA KIRMIZI"`.

> **Ders.** Bir kapı, denetlediği şeyin **tanımını** yazardan alıyorsa
> denetlemiyordur. Kabul yordamının parametreleri de üretilmelidir.

### 5.3 · ⭑ F2-02 · BULMACALAR OKUR PAKETİNDE ÇÖZÜLEMİYORDU ⭑

**Bulgu.** On bulmacanın levha **metni** vardı ama levha **verisi** yoktu.
"Altı kemer, her birinin altında bir Sözlük numarası" yazıyordu; hangi
kemerin kilit taşının çift olduğu **yalnızca cevap anahtarındaydı**.

**Neden hiçbir kapı görmedi.** Sekiz kapının sekizi de **korumalı katmanı**
denetliyordu. Hiçbiri okurun **eline ne geçtiğine** bakmıyordu. Kusursuz
bir tekillik ispatı, çözülemeyen bir bulmacanın üzerinde duruyordu.

**Kapatıldı.** `qa_readerpack.py` — yedi denetim, hepsi ters yönden sorar:
*okur bunu çözebilir mi?* Ve levha şekilleri artık nitelik haritasından
**türetilir**; elle çizilen bir levha ile kabul yordamı sessizce ayrışamaz.

### 5.4 · Solver B bulguları — metin ile levha çelişkileri

Bağımsız iç çözücü yirmi bulmacayı ipucusuz çözdü ama **on bir metin–levha
çelişkisi** bildirdi. Hiçbiri çözümü engellemedi; hepsi çözücüyü **kendi
doğru okumasından şüphe ettirdi**. *Zorluğu artırmadan sürtünme eklemek,
en pahalı redaksiyon kusurudur.*

| # | Bulmaca | Çelişki | Düzeltme |
|---|---|---|---|
| F2-03 | g1-003 | *"her grup farklı"* — **yanlış**, bir grup iki kez geçiyor | ifade düzeltildi |
| F2-04 | g1-005 | *"dört koşul"* — sayfada **üç** madde | sayı düzeltildi |
| F2-05 | g1-017 | *"üç koşul"* + başlıkta karşılıksız "Bir Sayı" — sayfada **dört** madde | başlık ve sayı düzeltildi |
| F2-06 | g1-007 | *"tepesinde"* — Sözlük numaraları levhada **altta** | **ikinci cevap üretiyordu** (§ 5.6) |
| F2-07 | g1-012 | *"iki yanına"* — işaretler **tek** yanda | ifade düzeltildi |
| F2-08 | g1-016 | çatlak karonun koyu sayılıp sayılmadığı **hiçbir yerde yazmıyordu** | kural metne eklendi |
| F2-09 | g1-011 | ızgaranın eksik son satırının nasıl dolduğu yazılmamıştı | kural metne eklendi |
| F2-10 | g1-006 | kaydırma **yönü** tanımsızdı | yön metne eklendi |
| F2-11 | g1-015 | *"karşılıklı iki nokta"* — 29 üyeli **tek sayılı** halkada matematiksel olarak yanlış | tanım düzeltildi |
| F2-12 | g1-010 | madde *"numarası"*, dipnot *"cevabı"* diyordu | ifade düzeltildi |
| F2-13 | g1-009 | *"dilllidir"* yazım hatası + "dilli"→sütun eşlemesi yazılı değildi | ifade düzeltildi |

### 5.5 · ⭑ F2-06 · GERÇEK BİR İKİNCİ CEVAP — ve kaynağı bir yazım hatasıydı ⭑

`g1-007`'de metin *"Her sütunun **tepesinde** bir Sözlük numarası vardır"*
diyordu. Levhada tepede **sütun numarası**, altta Sözlük numarası vardı.

Metni **birebir uygulayan** bir çözücü ikinci sütunun tepesindeki `2`'yi
Sözlük numarası okur ve **kitabın kendi cümlesine dayanan** savunulabilir
bir ikinci cevap üretir.

> Bu, projenin en sinsi kusurunun canlı örneğidir: **cevabı doğru sanan
> okur, çözemeyen okurdan daha öfkelidir.** Ve kaynağı bir mekanizma
> hatası değil, **tek bir yanlış edattı**.

`qa_answerspace` bunu yakalayamazdı: mekanizma doğruydu, **metin** yanlıştı.
Bu kusur sınıfını yalnızca bir insan (veya bağımsız bir çözücü) bulur —
harici çözücü testinin neden vazgeçilmez olduğunun mekanik kanıtı.

### 5.6 · F2-14 · Basılı Sözlüğün bedeli — kabul edilmiş bir takas

K22 kabul yordamını yazardan çizelgeye taşıdı ve tekilliği hesaplanabilir
kıldı. Bedeli açıkça kaydedilir:

Bir okur hiçbir şey çözmeden 60 üyeli Sözlük'ten tahmin yürütebilir
(**1/60 ≈ %1,7**). On dokuz bulmacayı tahminle bitirme olasılığı 60⁻¹⁹'dur
— sıfır. Ama **tek** bir bulmacayı kaba kuvvetle geçmek mümkündür.

**Karşı önlem** A7'nin yan kazancıdır: doğrulama sayfası reddedilen
dizeleri kaydeder ve kaba kuvvet kalıbı (aynı bulmacaya kısa sürede çok
sayıda farklı Sözlük üyesi) **tespit edilebilirdir**.

### 5.7 · F2-15 · Sayma yorgunluğu — bir dizgi tercihi değil, çözülebilirlik

Eşik Alfabesi'nde `Ç` dört işaret, `D` beş işarettir. Bitişik bir dizide
dördü beşten ayırmak **göz sayımına** bağlıdır ve iç çözücü bunu bir risk
olarak bildirdi.

**Kapatıldı (kısmen).** İşaretler artık **aralıklı** basılır: `' ' ' '`
ile `' ' ' ' '` arasındaki fark, `''''` ile `'''''` arasındakinden
ölçülebilir biçimde kolaydır.

⚠ **Tam kapanış POD provasına bağlıdır (A9).** Kâğıtta aralık nokta
yayılmasıyla kapanıyorsa mekanik yine kırılır. Prova kontrol listesinin
**birinci** maddesi budur.

### 5.8 · F2-16 · Kanarya kendi test dosyasını yakaladı

Yeni selftest fikstürleri gerçek Sözlük'ten sözcük kullanıyordu ve
kanarya `05_TESTS/selftest.py`'yi **sızıntı olarak** bildirdi. Haklıydı:
bir fikstür cevabı gerçek bir cevapla aynıysa, o cevap public depoda düz
metin olarak durur.

Fikstür sözlüğü tamamen sentetik hâle getirildi ve gerçek Sözlük'le
**hiçbir üye paylaşmaz**. Bu bulgu, kanaryanın gerçekten çalıştığının en
temiz kanıtıdır — kendi yazarını yakaladı.

### 5.9 · F2-17 · Bir cevap sözcüğü deponun kendi terimiyle çakıştı

Bir Sözlük üyesi `g1-005`'in cevabıydı ve kanarya **üç dosyada** sızıntı
bildirdi: sözcük aynı zamanda bir yazılım terimidir (*"window"*) ve deponun
kendi kod yorumlarında (`kelime penceresi`, `karakter penceresi`) geçiyordu.

**Kural doğdu:** bir cevap sözcüğü, deponun public prozasında geçen bir
terim olamaz. Ölçüldü: altmış üyenin kanarya eşiğini aşan **on yedisinden
yedisi** depo prozasında geçiyor. Cevap, depo prozasında geçmeyen bir Sözlük üyesiyle değiştirildi.

### 5.10 · F2-18 · Türkçe pilot ölçüm makinesini kırdı

`unicodedata.normalize("NFKD")` Türkçe harflerin çoğunu çözer ama
**noktasız `ı`** (U+0131) ve **noktalı `İ`** (U+0130) taban harflerdir ve
ayrışmazlar.

Sonucu: `"IŞIK"` normalize edilince `isik`, `"ışık"` ise `ışık` oluyordu.
Aynı sözcüğün iki farklı normal biçimi vardı — yani **ipucu sızıntısı
denetimi ve kanarya, cevabı küçük harfle yazan bir sızıntıyı kaçırırdı.**

**Kapatıldı.** `ı/İ/I → i` katlaması hem `_protected_layer` hem
`qa_solution_leak` içinde, küçültmeden **önce** uygulanır. İki dosyanın
ayrışmaması bir fikstürle korunur.

> Bu, talimat § 17'nin uyardığı şeyin canlı örneğidir: **bir dil değişimi
> ölçüm makinesinin kendisini de değiştirir.** İngilizce dönüşümde aynı
> soru yeniden sorulacaktır.

### 5.11 · F2-19 · Düz merdiven de bir kusurdur

`qa_hints` merdivenin **azalmasını** yakalıyordu ama **düz kalmasını**
yakalamıyordu: kapsam `[4,4,4]` geçiyordu. Bu üç kademeli bir merdiven
değil, üç kez tekrarlanan tek bir ipucudur.

Bir bulmaca (`g1-017`) tam olarak buydu ve eski kuraldan **geçmişti**.
Kural artık **yükselmeyi** arar. Ve merdiven artık çözüm yolundan
**türetilir** — bir yapı şartını disipline değil türetime bağlarız.

### 5.12 · F2-20 · Levha etiketi nesnenin kendi adını taşıyamaz

`qa_answerspace § ⑦` dört bulmacada ipucunun **yakın kaçırma** kümesinden
bir üyeyi adıyla andığını bildirdi. Sebep: kemer bulmacasında etiketlerden
biri `KEMER`, halka bulmacasında `HALKA`, sütun bulmacasında `SÜTUN`,
basamak bulmacasında `BASAMAK` idi.

*"Altı kemerin tepesine bakın"* cümlesi, levhadaki `KEMER` etiketini adıyla
anıyor ve okuru yanlış bir üyeye götürüyordu. Sınıf adları etiketlerden
çıkarıldı.

### 5.13 · F2-21 · Sahte doğrulama tuzağı

`g1-001`'de levha iki sayı satırı taşıyordu: kemer sıra numaraları
(1–6) ve Sözlük numaraları. Birinci kemerin Sözlük numarası da **1**'di.

Satırları karıştıran çözücü Sözlük'ün birinci satırına düşüyordu — ve o
satır **nihai kapı sözünün anahtar sözcüğüydü**. Yani okur yanlış cevabını
sonradan "doğru yoldayım" diye yorumlayabilirdi.

> Sahte bir doğrulama hissi, çözememekten daha tehlikelidir.

Sıra numarası satırı levhadan **kaldırıldı**.

### 5.14 · Kapatılmayan sınırlar — açıkça yazılıdır

| Sınır | Neden açık | Ne zaman kapanır |
|---|---|---|
| Gravür levhaların baskı davranışı | Pilot levhaları **tipografik şekildir**, gravür değil | Faz 5 · A9 |
| Sayma yorgunluğu (4 ↔ 5 işaret) | Aralıklandırma yardım eder; kâğıtta ölçülmedi | POD provası · A9 |
| 6 karakterden kısa cevapların kanarya koruması | `MIN_ANSWER_CHARS = 6`; kısaltmak yanlış pozitif üretir | Açık — kısa cevaplar alan adı hattıyla korunur |
| İç çözücünün insan çözücüyü temsil etmesi | **Etmez.** İç çözücü kanıt değildir | **A12 · harici oturumlar** |

### 5.15 · F2-22 · Bu defterin kendisi bir sızıntıydı

Yukarıdaki F2-17 ilk yazımında düzeltmeyi anlatırken **yeni cevabı adıyla
andı**. Kanarya bu dosyayı sızıntı olarak bildirdi ve haklıydı.

> *"Bir sızıntı raporunun kendisinin sızıntı olması, bu depoda
> düşülebilecek en gülünç tuzaktır."* — `qa_solution_leak.py` başlığı,
> Faz 1'de yazıldı ve Faz 2'de **doğrulandı**.

Kural: bulgu defteri ve faz raporları bir cevabı **adıyla anmaz**; kusuru
ve düzeltmeyi anlatır, dizeyi anmaz. Bu, disipline değil kanaryaya
bağlıdır — ve kanarya ısırdı.

### 5.16 · F2-23 · Var olmayan bir çizelgeye gönderme

Üçüncü bağımsız çözücü (Solver D) **ikinci cevap bulamadı** — mekanizma
düzeltmeleri tuttu. Ama sekiz ayrı cümlede bir künye hatası buldu.

Çizelgeler bir kez yeniden adlandırılmıştı. Başlıklar ve sözleşme sayfası
güncellendi; **üç bulmacanın gövdesi eski adlarda kaldı**. Okur iki
bulmacada var olan ama yanlış bir çizelgeye, bir bulmacada ise **hiç var
olmayan** bir çizelgeye gönderiliyordu.

> Bu, sözleşmenin **dördüncü sözünün** doğrudan ihlalidir — *"kitap size
> bir çizelge veriyorsa, o çizelge tek yetkedir"* — ve en zararlı hata
> cinsindendir: **okur bunu kendi hatası sanır.**

**Kök neden aynıydı:** okur paketinin başlıkları elle yazılıyordu.
Başlıklar artık çizelge verisinden **okunur**. Ve `qa_readerpack § ⑧`
artık okur metnindeki her `Çizelge X` göndermesini basılı çizelge
harfleriyle karşılaştırır — sarkan bir gönderme kırmızı yanar.

### 5.17 · ⭑ F2-24 · CI'ın kendisi bir körlük yarattı ⭑

İlk yirmi bulmaca `drafted` olur olmaz **CI kırmızı yandı** — ve haksızdı.

Korumalı katman `.gitignore` ile dışlanır ve **klonda hiç yoktur**. Kapı
bunu "yazılmış bulmacanın korumalı kaydı KAYIP" diye okuyordu: kendisine
hiç gösterilmemiş bir dosyayı kayıp sanıyordu.

Faz 1'de bu ayrım **gerekmiyordu** çünkü hiçbir bulmaca `drafted`
değildi. Kusur, kodun ilk kez gerçek veriyle karşılaştığı anda doğdu.

**İki durum artık ayrılıyor ve ikisinin de fikstürü var:**

| Durum | Anlam | Davranış |
|---|---|---|
| Katman **tamamen** yok | CI'ın normal durumu | **boş koşar ve SÖYLER** |
| Katman **var ama eksik** | yazar çözümü yazmayı unuttu | **KIRMIZI** |

⚠ Ve boş koşan kapı *"bu bir GEÇİŞ DEĞİLDİR"* der. Sessizce yeşil yanan
bir kapı, olmayan bir kapıdan tehlikelidir — bu kural burada da geçerlidir.

### 5.18 · Üç çözücü geçişinin karşılaştırması

| | Solver B | Solver C | Solver D |
|---|---:|---:|---:|
| Çözülen | 20/20 | 20/20 | **20/20** |
| Kullanılan ipucu | 0/60 | 0/60 | **0/60** |
| Süre | ~41 dk | ~94 dk | ~76 dk |
| Metin–levha çelişkisi | 11 | 8 | **3** |
| Tanımsız kural | 3 | 8 | **1** |
| **İkinci cevap** | 0 | **2** | **0** ✅ |

Eğri doğru yönde: **ikinci cevaplar kapandı** ve çelişki sayısı 11 → 3'e
indi. Kalan üçü de bu fazda kapatıldı (§ 5.16).

> ⚠ Ve hiçbiri kanıt değildir. Üç yapay çözücü de yirmi bulmacayı ipucusuz
> çözdü; bir insan çözücünün bunu yapacağının **hiçbir göstergesi yoktur**.
> Solver B'nin kendi tahmini insan için 3–5 kat süre. Öldürme kapısı bu
> satırların hiçbirini saymaz.
