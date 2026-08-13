# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript ve **çözüm katmanı** politikası | **YÜKSEK** | Faz 1 | ✅ **KAPANDI** → K10 + K14 (beş hatlı koruma) |
| **A2** | 5 kapı teması onayı | YÜKSEK | **Faz 2 başlamadan** | AÇIK |
| **A3** | **5 harici çözücü kim** | **YÜKSEK** | **Faz 2 başlamadan** | ✅ **KAPANDI** → K18 · § aşağı |
| **A4** | Doğrulama sayfası barındırma | ORTA | Faz 5 | AÇIK |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | Faz 2 | AÇIK |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |
| **A7** | **Bulmaca başına doğrulama** — doğrulama sayfası 100 cevap alanı taşısın mı | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — biçim kararı · **mekaniği K21 ile kuruldu** |
| **A8** | **Sayfa hedefi 208 → 230** (telif 9,85 $ → 9,58 $) | **YÜKSEK** | **Faz 2 başlamadan** | ✅ **KAPANDI** → K17 onaylandı · § aşağı |
| **A9** | **Pilot levhaların POD provası** Faz 2'ye alınsın mı | **YÜKSEK** | **Faz 2 başlamadan** | ⚑ **KURUCUYA DEVREDİLDİ** · § aşağı |
| **A10** | Faz 3'e **ikinci öldürme kapısı** eklensin mi | ORTA | Faz 3 başlamadan | AÇIK |
| **A11** | `ENIGMATICA_CANARY_SALT` CI sırrı kurulsun | ORTA | **Faz 2 başlamadan** | ✅ **KAPANDI** → K19 · § aşağı |
| **A12** | ⭑ **Harici çözücü oturumları** ⭑ | **KRİTİK** | Faz 2 | ⛔ **KAPANDI · BAŞARISIZ** → K23 · § aşağı |
| **B1** | Yeni mekanizma karışımı | KRİTİK | — | ✅ **ONAYLANDI** → K26 |
| **B2** | Yansıma Kapı IV'e taşınsın | KRİTİK | — | ✅ **ONAYLANDI** |
| **B3** | Anahtarlı alfabe Kapı II'ye ertelensin | KRİTİK | — | ✅ **ONAYLANDI** |
| **B4** | Isınma bölümü yazılsın | KRİTİK | — | ✅ **ONAYLANDI** → yazıldı |
| **B5** | `qa_effort` çarpanı | ORTA | ikinci tur | ⏸ **ERTELENDİ** — gerçek süreyle kalibre |
| **B6** | İkinci tur kohortu | KRİTİK | — | ✅ **C ONAYLANDI** · 2 dönen + 3 yeni |
| **A12b** | ⭑ **İkinci tur oturumları** ⭑ | **KRİTİK** | **Faz 3 için** | ⛔ **AÇIK — TEK BLOKLAYICI** |

---

### A12 · ⛔ KAPANDI — VE ÖLDÜRME KAPISI DÜŞTÜ

**13 Ağustos 2026.** Beş harici Türkçe çözücü Kapı I'i denedi.

| | |
|---|---:|
| Kapı I'i **bitiren** | **1 / 5** |
| Geçme eşiği | ≥ 4 / 5 |
| Sert durdurma eşiği | < 3 / 5 |
| **Karar** | ⛔ **HARD-STOP** |

**Baskın bırakma sebebi *"çözemedim"* değildi:** mekanik yürütme —
kaydırma, yansıma ve anahtarlı alfabe — kâğıt kalemle **sıkıcı ve
yorucuydu**. İkinci sebep: mantık sıçraması ★ için fazla dik.

Kurucu kararı: **YENİDEN TASARLA**, terk etme.
Öneri: [`06_REPORTS/GATE_1_REDESIGN_PROPOSAL.md`](06_REPORTS/GATE_1_REDESIGN_PROPOSAL.md)

⚠ **Bulmaca başına kayıt sağlanmadı** (yalnızca oturum düzeyi). Kalan beş
öldürme kapısı ölçütü **ölçülemedi** ve `kill-gate-report.json` bunları
"geçti" değil **`measured: false`** olarak taşır.

---

### A12 · (kapanmadan önceki hâli) Oturumlar — A3 kapandı, ama test HÂLÂ yapılmadı

> **A3 ile A12 iki ayrı sorudur ve karıştırılmaları sahteciliğin adıdır.**

| | A3 | **A12** |
|---|---|---|
| Soru | Çözücüler **kim** | Oturumlar **yapıldı mı** |
| Durum | ✅ kapandı (5 kişi, Türkçe) | ⛔ **YAPILMADI — 0 oturum** |
| Kim kapatır | kurucu | **kurucu + beş insan** |
| Ajan yapabilir mi | — | **HAYIR. Asla.** |

Ajan bulmacayı çözemez: **çözümü zaten bilir.** Bildiği bir şeyi "bulmak"
bulmak değildir. Bu yüzden `06_REPORTS/solver/` **boştur** ve boş kalacaktır
— ta ki beş gerçek insan beş gerçek oturum yapana kadar.

`validate_spec § check_test_status` bunu belgeyle değil **mekanizmayla**
tutar: `solverTestCount` 0 iken hiçbir kayıt `tested` olamaz, dolayısıyla
hiçbir kayıt `validated`/`written` olamaz, dolayısıyla `.gate` `phase2`ye
**yükselemez**. Sahte kayıt üretmenin yolu kapalıdır.

**Kurucu paketi hazır:** [`00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`](00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md)

---

### A7 · Bulmaca başına doğrulama — kırmızı takımın tek en yüksek değerli önerisi

Kapı bulmacası on dokuz girdinin **hepsine** bağlıdır. Bulmaca başına
doğruluk *p* ise kapıyı temiz bitirme olasılığı *p*¹⁹'dur:

| *p* | *p*¹⁹ | 5 çözücüden ≥4'ünün bitirme olasılığı |
|---:|---:|---:|
| 0,99 | 0,83 | **%79** |
| 0,95 | 0,38 | **%7** |
| 0,90 | 0,14 | **%0,07** |

Öldürme kapısının kararı, **hiç ölçülmemiş** bir parametreye bağlıdır.

Ve 18/19 çözen okur hangi ikisinin yanlış olduğunu **bilemez**. İpucu
merdiveni orada işe yaramaz: okur hangi bulmacaya ipucu alacağını
bilmiyordur. Yani bağımlılık grafiği, sözleşmenin üçüncü sözünü
(*"ipucu almak kaybetmek değildir"*) sessizce iptal eder.

**Öneri:** doğrulama sayfası (zaten Faz 5 teslimatı) tek meta cevabı
yerine **bulmaca başına** cevap kabul etsin ve reddedilen dizeleri
kaydetsin. Meta-mister dokunulmaz — cevabı hâlâ kitapta yoktur.

**Yan kazanç:** reddedilen dize kaydı, ölçekte çalışan bir alternatif
çözüm dedektörüdür. Beş çözücü bir tasnif bulmacasının ikinci cevabını
bulamaz; beş bin okur bir haftada bulur — ve POD iç bloğu revize edilebilir.

`project_config § solvability.perPuzzleVerification` şu an `true` olarak
duruyor ve **kurucu onayı bekliyor**.

---

### A8 · ✅ KAPANDI — sayfa hedefi 230 KABUL EDİLDİ

208'lik model arka maddeye **24 sayfa** ayırıyordu. Arka madde 300 ipucu
ve 100 tam çözüm taşır: 350 kelime/sayfa ile 22 + 18 + 4 = **44 sayfa**.
24 sayfalık bütçe **fiziksel olarak imkânsızdı**.

Bu bir dizgi meselesi değil bir **çözülebilirlik** meselesidir: Kapı V
bulmacaları sayfa numaralarına dayanır (K12). 20 sayfalık bir taşma,
dizgi dondurulduktan sonra keşfedilseydi sekiz bulmacayı Faz 5'te,
takvimin bittiği yerde kırardı.

| | 208 | **230** |
|---|---:|---:|
| Ciltli baskı maliyeti | 8,15 $ | 8,41 $ |
| Ciltli telif | 9,85 $ | **9,58 $** |
| Başabaş ACOS | %32,8 | **%31,9** |

Kayıp birim başına **0,27 $** (%2,7). Kapsam sayıları Faz 1'e kadar
hipotezdi (K8); bu, o hipotezin düzeltilmesidir.

**13 Ağustos 2026 · kurucu kararı:** 230 sayfa ve buna bağlı ciltli telif
düşüşü **kabul edildi**. `scope.pageTargetFounderApproved` → `true`.

> ⚠ **A8 yeniden açılmaz.** Ve bir dizgi sorununu yok etmek için sayfa
> hedefi **değiştirilmez**: içerik/dizgi sorunu çözülür ve **yeniden
> ölçülür**. Sebep K12'dir — Kapı V sayfa numaralarına bağlıdır. Hedefi
> içeriğe uydurmak, bulmacayı kıran taraftır.

---

### A9 · ⚑ KURUCUYA DEVREDİLDİ — pilot levhalarının POD provası

Pilot kohortun 20 bulmacasından **9'u levha taşır**, ikisinde veri
gravürün **içindedir**, ve beşi araçlar levhasındaki çizelgeye bağlıdır.
Yol haritası levha üretimini Faz 5'e koyuyor; öldürme kapısı Faz 2'de.

> Ekranda çözülen bir levha bulmacası **test edilmemiştir**. Krem kâğıtta
> nokta yayılmasıyla kapanan bir aralık, o bulmacayı çözülemez yapar — ve
> öldürme kapısı tam olarak önlemesi gereken şeyi onaylamış olur.

İki seçenek vardır, üçüncüsü yoktur:

| Seçenek | Sonuç |
|---|---|
| **A** — pilot levhalar + araçlar levhası provada basılır | Kapı mekaniği **kapsıyor** |
| **B** — pilot levhasız 11 bulmacaya indirilir | Kapı mekaniği **kapsamıyor** ve rapor bunu açıkça yazar |

**13 Ağustos 2026 · kurucu kararı:** fiziksel prova **kurucu işidir** ve
Faz 2'nin teknik işini **bloklamaz**.

Ajan üç şeyi **yapmaz**: provayı sipariş etmez, yapıldığını iddia etmez,
ölçüm uydurmaz. Ajan üç şeyi **yaptı**: baskıya hazır prova paketini üretti,
kontrol listesini yazdı, devir talimatını yazdı.

İki durum her raporda **ayrılır** ve birleştirilmeleri yasaktır:

| Durum | Anlamı | Pilot |
|---|---|---|
| `SCREEN-TESTED` | Ekranda çözüldü — **ön eleme** | ✔ 20/20 |
| `PHYSICAL-PROOF-VALIDATED` | POD provada ölçüldü — **kanıt** | ⛔ **0/20** |

⚠ Ve pilotta ikinci bir ikame daha var: pilot levhaları **gravür değil,
tipografik şekildir**. Yani pilot levha bulmacalarının **mantığını** test
eder, gravürün baskı davranışını **etmez**. Bu iki ayrı ölçümdür ve
ikincisi Faz 5'e aittir.

---

### A3 · ✅ KAPANDI — beş harici çözücü belirlendi

**13 Ağustos 2026 · kurucu kararı.** Beş harici çözücü bulundu.
`founder.externalSolvers.founderConfirmed` → `true`.

Ve tek bir olgu bütün Faz 2'nin dilini belirledi:

> ### Beşinin beşi de Türkçe konuşuyor.

Bir bulmacanın **mekaniği** ancak çözücünün ana dilinde ölçülebilir. Yabancı
dilde çözülemeyen bir bulmaca, mekanizması bozuk olduğu için mi yoksa cümle
anlaşılmadığı için mi çözülemedi — bu ayrım yapılamazsa ölçüm **gürültüdür**.
Pilot bu yüzden Türkçedir (→ K20).

Kimlikler anonimdir (`solver-01` … `solver-05`) ve şema bu biçimi zorunlu
kılar. Adlar **hiçbir koşulda** depoya girmez.

⚠ **A3'ün kapanması hiçbir bulmacayı test edilmiş yapmaz** — oturumlar
ayrı bir karardır ve **A12**'dedir.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole
**12 Ağustos 2026 · bootstrap.** Talimat § 31 bir ajanın tek klasörle
çalışabilmesini şart koşuyor. **Kopyalanan kod biraz fazlalıktır;
bağımlılık bir kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur
`--fix` kapıya dokunmaz (Bestiarium dersi).

### K3 · Codex adı taşınır, tür taşınmaz
Bu cilt *Codex* hattının adını taşır ama **referans değil oyundur**.
Bilinçli bir marka genişlemesi: Vâliçe Press'i "referans yayıncısı"ndan
**"deneyim tasarlayan yayıncı"**ya taşır.

Ad ortaklığı **dosya ortaklığı değildir**: Bestiarium'dan motif *fikri*
alınır, **dosya alınmaz**.

### K4 · ⭑ Bir bulmaca "zekice göründüğü" için kabul edilemez ⭑
**Bu projenin birinci kuralı.** Deterministik olarak çözülemeyen bir
bulmaca bir **üretim hatasıdır**. Beş şart
[`00_CONTEXT/SOLVABILITY_STANDARD.md`](00_CONTEXT/SOLVABILITY_STANDARD.md)'de
tanımlıdır ve üç kapı tarafından denetlenir.

### K5 · ⛔ Faz 2 bir ÖLDÜRME KAPISIDIR
20 bulmaca 5 harici çözücüyle test edilir. **≤2 çözücü Kapı I'i bitirirse
proje DURUR veya YENİDEN TASARLANIR.**

Gerekçe: bozuk bir bulmaca sistemi üzerine 200 sayfa yazmak, bu portföyün
yapabileceği **en pahalı hatadır**.

Eşikler `project_config.json § killGate` içinde **sayısaldır**;
`validate_spec.py` düşürülmelerini yakalar. **Yoruma yer yoktur.**

### K6 · Üç kademeli ipucu zorunludur
Cain's Jawbone'u üç kişi çözdü — bu ticari olarak bir **terk oranıdır**.
Bu kitabın konumu tersidir: *amaç okuru yenmek değil, içeride tutmaktır.*
`qa_hints` üç kademenin varlığını ve hiçbirinin cevabı içermediğini
denetler.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz
`validate.yml` saniyeler içinde biter.

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR
`scope.locked: false`.

### K9 · Kindle üretilmez
Görsel şifreler e-okuyucuda bozulur; iade ve kötü yorum üretir.
Bir gelir kaybı değil, **itibar korumasıdır**. `validate_spec` Kindle'ın
açılmasını yakalar.

### K10 · ⭑ İKİ KATMANLI İÇERİK — dört hatlı çözüm koruması ⭑
**Bu projenin ikinci varoluşsal kuralı.**

Çözümler, çözüm yolları ve ipuçları **PROTECTED** katmandadır ve public
depoya giremez. Ama **kod sır değildir**: `04_BUILD/` ve `05_TESTS/`
public kalır.

Dört hat: `.gitignore` (yol) · `PROTECTED_DIRS` (varlık) ·
`check_solution_leak()` (içerik) · `validate_spec` (şema).

Gerekçe: sızıntı **geri alınamaz**. Git geçmişine giren bir çözümü silmek
geçmişi yeniden yazmak demektir — ve o ana kadar klonlamış herkeste kalır.

→ [`00_CONTEXT/CONTENT_PROTECTION.md`](00_CONTEXT/CONTENT_PROTECTION.md)

### K11 · 6×9 normal trim
6,0 ≤ 6,12 ve 9,0 ≤ 9,0 olduğu için **normal trimdir** ve sayfa başına
0,012 $ öder — büyük trimin 0,017 $'ının altında. Codex serisiyle raf
uyumu ve düşük baskı maliyeti aynı anda.

### K13 · ⭑ Kapı devri bağı KAPATILDI — kapılar bağımsız girilir ⭑
**13 Ağustos 2026 · Faz 1.** Pazar raporunun *"her kapının çözümü bir
sonrakinin anahtarını verir"* cümlesi mekanik bir bağa çevrilmişti.
Sonucu: bir kapı bulmacasını yanlış çözen okur, ürünün **%80'ine** tek bir
hatadan ve hiçbir teşhis olmadan kapanıyordu.

Kapı devri artık **anlatısaldır**. Geriye tek birleşim kalır: meta-mister
— ve orası zaten toplam tamamlanma isteyen tek yerdir.

Bu kuralın o an **hiçbir örneği yoktu** (Kapı II–V slotlanmamıştı); şimdi
kapatmak bedava, Faz 4'te kapatmak altmış bulmacayı yeniden sıralamaktı.

### K14 · ⭑ Beşinci koruma hattı: KANARYA ⭑
**13 Ağustos 2026 · Faz 1.** İlk dört hat çözüm **alan adı** arıyordu,
**cevap** aramıyordu: `BOOK_STATS.md` içine etiketsiz bir cümleyle yazılan
bir cevap dördünden de geçiyordu (POC ile gösterildi).

`qa_solution_leak.py` cevabın kendisini arar — dosya içeriği, **dosya
adları** ve **commit mesajları** dâhil. CI'da tuzlu künyeyle koşar; cevap
hiçbir yerde açık durmaz.

### K15 · ⭑ `tested` mekanik olarak kazanılır ⭑
**13 Ağustos 2026 · Faz 1.** Öldürme kapısı mekanik olarak bir **metin
alanıydı**: 140 kaydın `status` alanını elle değiştirmek projeyi
`phase1`'den `release`'e yürütüyordu. Artık beş şart + kurucu onayı kilidi
aranır ve **iç çözücü kayıtları sayılmaz**.

### K16 · Şema UYGULANIR — public katman bir izin listesidir
**13 Ağustos 2026 · Faz 1.** `puzzle.schema.json` var olduğu hâlde
**hiçbir kod tarafından okunmuyordu**. Artık `validate_spec` onu uygular ve
`additionalProperties: false` sayesinde public indeks bir yasak listesiyle
değil bir **izin listesiyle** korunur: akla gelmemiş bir alan adı da
reddedilir.

### K17 · Sayfa hedefi 230 (kurucu onayı bekliyor · A8)
**13 Ağustos 2026 · Faz 1.** Arka madde 24 sayfada imkânsızdı; içerikten
türetilen değer 44'tür. Model 210 → **230**. Ticari etki ölçüldü ve
raporlandı.

### K18 · ⭑ A3 kapandı — ve pilotun dilini o kapadı ⭑
**13 Ağustos 2026 · Faz 2.** Beş harici çözücü belirlendi; beşi de Türkçe
konuşuyor. `founderConfirmed` → `true`.

Ama config'de **iki ayrı alan** vardır ve ayrımları varoluşsaldır:
`founderConfirmed` (çözücüler **belirlendi**) ve `sessionsRecorded`
(oturumlar **yapıldı**). İkincisi **0**'dır. Birincisi `tested` durumunun
beş şartından yalnızca biridir; kalan dördü gerçek oturum olmadan
sağlanamaz — yani A3'ün kapanması **hiçbir bulmacayı test edilmiş yapmaz**.

### K19 · ⭑ A11 kapandı — kanarya sırrı kuruldu, plaintext hiçbir yerde yok ⭑
**13 Ağustos 2026 · Faz 2.** `ENIGMATICA_CANARY_SALT` üretildi
(`secrets.token_urlsafe(48)` = 384 bit), GitHub Actions deposu sırrı olarak
kuruldu ve **depo dışında** `0600` izinli bir yerel yedeğe yazıldı.

Sır **hiçbir** terminal çıktısında, commit'te, raporda veya kaynak dosyada
görünmedi. Raporlanan şey sırrın **kimliğidir**: adı, parmak izi
(`sha256[:16]`), yedek yolu, döndürme yordamı. Ayrıntı:
`project_config.json § security.canary`.

Ve kanaryanın üç davranışı **kasıtlı fikstürlerle** kanıtlandı:
doğru tuz → yeşil · **eksik tuz → kırmızı** · **yanlış tuz → kırmızı**.
Sessizce yeşil yanan bir kanarya, kanarya değildir.

### K20 · ⭑ Türkçe pilot bir ÖLÇÜM ARACIDIR, manuscript değil ⭑
**13 Ağustos 2026 · Faz 2.** `pilotLanguage: "tr"` ·
`productionLanguage: "en"` · `pilotIsProductionManuscript: false`.

Gerekçe tek cümledir: **bir bulmacanın mekaniği ancak çözücünün ana
dilinde ölçülebilir.** Yabancı dilde çözülemeyen bir bulmacada "mekanizma
mı bozuk, cümle mi anlaşılmadı" ayrımı yapılamaz — ve ayrım yapılamayan
bir ölçüm gürültüdür.

İki yasak buradan doğar ve config'de mekaniktir:

1. **Türkçe başarı, İngilizce çözülebilirliğin kanıtı değildir.** Dil
   değişimi cevap uzayını, eşanlamlı uzayını, akrostişleri ve kelime
   oyununu değiştirir. İngilizce sürüm **çeviri değil yeniden tasarımdır**
   ve sekiz kapıdan **baştan** geçer.
2. **Pilot nihai manuscript olamaz.** Ticari kitap İngilizcedir.

### K21 · ⭑ `answerSpace` — sayım alanı prozadan DOSYAYA taşındı ⭑
**13 Ağustos 2026 · Faz 2'nin birinci teslimatı.** Faz 1 kırmızı takımı on
yedi ailenin **dokuzunda** tekillik ispatının totoloji olduğunu gösterdi:
*sayım alanını, cevabı zaten bilen yazar tanımlıyordu.*

Artık her bulmaca makine okunur bir **üreteç** taşır. `qa_answerspace.py`
üreteci **bağımsız açar** — yazarın listesini okumaz, bulmacanın
girdisinden yeniden türetir — ve alanın **tam olarak bir** üyesinin basılı
kabul yordamından geçtiğini doğrular. 0 → çözülemez, ≥2 → ikinci cevap.

Üç sahte mekanizma açıkça yasaklandı: yazar tarafından sayılmış alan ·
tek üyeli alan · "yazar öyle diyor" kabul yordamı.

### K22 · ⭑ Basılı Sözlük — kabul yordamı yazardan ÇİZELGEYE taşındı ⭑
**13 Ağustos 2026 · Faz 2.** K21 bir soruyu açıkta bırakıyordu: alanın bir
üyesinin *kabul edilmesi* neye göre? "Yazar bunu anlamlı buluyor" bir kabul
yordamı değildir — K21'in kapattığı totolojiyi bir adım öteye taşımaktır.

Çözüm **araçlar levhasındadır**: Kapı I'in bütün cevapları, ön maddede
**basılı** 60 kelimelik *Eşik Sözlüğü*'nün üyesidir ve sözleşme sayfası
bunu okura **söyler**. Böylece kabul yordamı mekanikleşir: bir dize kabul
edilir ⟺ Sözlük'te vardır.

Üç kazanç: tekillik **hesaplanabilir** olur · cevap biçimi tartışması
biter (K: `answerNormalization`) · sözleşmenin dördüncü sözü (*"kitap size
bir çizelge veriyorsa, o çizelge tek yetkedir"*) somut bir nesne kazanır.

**Ödenen bedel açıkça kaydedilir:** bir okur hiçbir şey çözmeden 60 üyeli
sözlükten tahmin yürütebilir (1/60 ≈ %1,7). On dokuz bulmacayı tahminle
bitirme olasılığı 60⁻¹⁹'dur — yani sıfırdır — ama **tek** bir bulmacayı
kaba kuvvetle geçmek mümkündür. Karşı önlem A7'nin yan kazancıdır:
doğrulama sayfası **reddedilen dizeleri kaydeder** ve kaba kuvvet kalıbı
(aynı bulmacaya kısa sürede çok sayıda farklı sözlük üyesi) tespit
edilebilirdir. Bkz. `RED_TEAM_CHECKLIST § 4` bulgu **F2-14**.

### K26 · ⭑ Kapı I yeniden tasarlandı — ve çaba yarıdan aza indi ⭑
**13 Ağustos 2026 · B1–B6 onaylı.** Yirmi bulmaca yeniden yazıldı.

| | Önce | **Sonra** |
|---|---:|---:|
| Elle işlem | 486 | **184** |
| Çabanın ima ettiği süre | 162 dk | **61 dk** |
| Bütçesini aşan bulmaca | 6 / 20 | **0 / 20** |
| En kötü oran | 4,7× | **1,0×** |

Beş tasarım kuralı config'de mekanik olarak durur
(`scope.gateOneRedesign.designRules`):

**K1 · Anahtar aranmaz, VERİLİR.** Şifrenin kaydırma miktarı levhada
basılıdır. Aynı bulmaca 84 işlemden **5 işleme** indi ve tekillik
ZAYIFLAMADI — çünkü ispat yine altmış üyeyi sayar.

**K2 · Her bulmaca kendi süre iddiasına sığar.** `qa_effort` bunu ölçer.

**K3 · İspat sayar, okur gezmez.** Alan basılı sözlüktür; mekanizma kabul
yordamıdır.

**K4 · Her mekanizma çözülmüş bir örnekle önce öğretilir.** Üç sayfalık
ısınma bölümü **yazıldı** — Faz 1'den beri bütçedeydi ve boştu.

**K5 · "Aha" işi, transkripsiyon işine baskın gelir.**

Ve iki aile Kapı I'den **çıkarıldı**: yansıma → Kapı IV (B2), anahtarlı
alfabe → Kapı II (B3). Bir mekanizmayı kaldırmak, onu kötü yapmaktan
ucuzdur.

### K23 · ⭑ ÖLDÜRME KAPISI DÜŞTÜ — ve düşüren şey ÖLÇÜLMEYEN boyuttu ⭑
**13 Ağustos 2026 · Faz 2 · A12.** 1/5 çözücü Kapı I'i bitirdi.

Sekiz kalite kapısı yeşildi. Cevap uzayı 20/20 tekildi. Üç bağımsız iç
çözücü yirmisini de ipucusuz çözdü. **Ve dört çözücü SIKILDIĞI için
bıraktı.**

Kusur çözülebilirlikte değil, **çözme İŞİNİN MİKTARINDAYDI** — ve o
boyutu hiçbir kapı ölçmüyordu. `qa_effort.py` yazıldı: elle yapılacak
işlem sayısını **cevap uzayı spesifikasyonundan** hesaplar ve bulmacanın
**kendi süre iddiasına** karşı denetler.

Model, hangi bulmacaların şikâyet edildiğini bilmeden koştu ve **aynı üç
bulmacayı aynı sırayla** işaretledi (4,7× · 3,0× · 1,6×).

> **Ölçülmeyen bir boyut, korunmayan bir boyuttur.** Projenin kurucu
> ilkesi, bu kez projenin kendisine uygulandı.

### K24 · `expectedCompletionMinutes` KAVRAYIŞI ölçüyordu, YÜRÜTMEYİ değil
**13 Ağustos 2026 · Faz 2.** Yazar *"bu fikir ne kadar sürede anlaşılır"*
diye tahmin etti; okur *"bu işi ne kadar sürede yaparım"* diye yaşadı.
Bir bulmacada fark **dokuz kattı** (6 dk iddia · 56 dk en kötü hâl).

Alan artık bir tahmin değil bir **bütçedir**: `qa_effort` onu
`dakika × 3 elle işlem` olarak okur ve aşımı kırmızı yakar.

### K25 · İspat sayar, okur GEZMEZ
**13 Ağustos 2026 · Faz 2.** `minDomainSize: 6` kuralı "sayım alanı
yeterince büyük olmalı" der — **ispat için**. Birkaç bulmaca, okur alanı
**elle taransın** diye kuruldu; kural bunu hiç istememişti.

| İSPATIN saydığı | OKURUN gezdiği |
|---|---|
| 28 kaydırma — makine sayar ✅ | 28 kaydırma — okur kalemle dener ⛔ |

Bundan sonra: alan **basılı sözlüktür**, mekanizma **kabul yordamıdır** ve
anahtar **verilir**. Tekillik korunur, çaba düşer.

### K12 · Kapı V dizgiye bağlıdır ve en son kilitlenir
Kapı V öz-göndergeseldir: kitabın **fiziksel yapısını** kullanır
(sayfa numaraları, dizin, kolofon). Dizgi değişirse **kırılır**.

Bu yüzden dizgi Faz 5'te **dondurulur** ve Kapı V ondan **sonra**
kilitlenir. Faz 6 sayfa sayısını yalnızca **doğrular**.
