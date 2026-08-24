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

### K27 · ⭑ `dakika × 3` bir TAVANDI, hedef değil — ×1,0'a inildi ⭑
**24 Ağustos 2026 · ikinci kurucu yönergesi.** Eski bütçe `dakika × 3`tü.
Üç bir gevşeklik payı değil, **birim çevrimidir** (dakikada üç elle işlem)
— yani eski kural şunu söylüyordu: *bildirilen sürenin tamamı mekanik
yürütmeye gidebilir.* Bir güvenlik tavanı olarak doğru, bir **tasarım
hedefi** olarak anlamsız.

Yeni kural `dakika × 1,0`dır ve okunuşu tektir:

> **Bildirilen sürenin en çok ÜÇTE BİRİ elle iştir.** Kalan üçte iki
> düşünmeye aittir.

⚠ Ve kaçamak yönergede kapatılmıştır: *"Do not simply increase the
expected time."* Bir bulmaca bütçesini aşıyorsa **saat değil, bulmaca**
değişir. Yirmi bulmacanın hiçbirinin süresi yükseltilmedi.

### K28 · ⭑ Çaba modeli ARAMAYI yarılıyordu, ama yalnızca bazılarını ⭑
**24 Ağustos 2026.** `effort()` her mekanizma için (beklenen, en kötü)
döndürür ve bütçe **beklenen**i denetler. Arama tipi mekanizmalarda
beklenen, en kötünün yarısıdır. Ölçüldüğünde:

| | |
|---|---|
| `cyclic-shift` · `reflection-map` | (en kötü/2, en kötü) ✅ |
| `plate-attribute` · `table-row` | (en kötü, en kötü) ⛔ |

Üçü de *"işe yarayanı bulana kadar bak"* yapısındadır. İkisi yarılanmış,
ikisi yarılanmamıştı — bu bir politika değil, bir **gözden kaçmaydı**.
Üç düzeltme yapıldı (levha araması yarılandı · çizelge elemesi ardışık
benzetime geçti · glif okuması TEK yön sayıldı) ve **184 → 130 EU**.

⭑ Ve üçü de **boşta durmuyor**: her biri `qa_readerpack § ⑨⑩⑪`de bir
denetime dayanır. Levha okuma yönünü basmıyorsa, çizelge öbeklenmemişse
veya boş ızgara basılı değilse **ölçüm de düşer**. İki kapı birbirine
dayanır: biri varsayımı kurar, öteki onu doğrular.

### K29 · ⭑ "Sıkıldım"ın ölçülmeyen yarısı: ÖDÜL ⭑
**24 Ağustos 2026.** `qa_effort` işin MİKTARINI ölçer ve iyi ölçer. Ama
sıkıcılığın yalnızca yarısıdır: aynı altı işlem, sonunda bir şey
**keşfediliyorsa** zevkli, keşfedilmiyorsa ev ödevidir.

`qa_experience.py` ikinci yarıyı kısıtlar: `ahaScore` ortancası ≥ 4,
`repetitionBurden` ölçülür, zorluk rampası ve ısınma kapsamı denetlenir.

> ⚠ **VE BU BİR KANIT DEĞİLDİR.** `ahaScore` yazarın kendi puanıdır;
> yönergenin kendi sözü: *"Do NOT use ahaScore as a substitute for real
> testing."* Kapı onu doğrulayamaz — **şişirilmesini zorlaştırır**:
>
> * 4+ veren her bulmaca ödülün **basılı yerini** göstermek zorundadır ve
>   gösterdiği şey okur paketinde bulunmalıdır;
> * **aynı mekanizma ikinci kez 4+ alamaz** — sürpriz bir kez olur;
> * `repetitionBurden` yazardan değil, çaba modelinden **ölçülür**.
>
> Gerçek ölçüm A12b'nin kayıt formundadır (*"sıkıcı mıydı 1–5"*).

### K30 · ⭑ Bazı sözcükler CEVAP olamaz — çünkü proje onları KONUŞUYOR ⭑
**24 Ağustos 2026.** Kanarya altı harf ve üzeri cevapları bütün takip
edilen dosyalarda **ve commit mesajlarında** arar. Yeni cevap kümesi
seçildiğinde kanarya ısırdı: sekiz üye zaten depoda geçiyordu — çünkü
bu projenin **kendi söz dağarcığıdır** (biri "ipucu merdiveni"nin adı,
biri "cevap anahtarı"nın).

⚠ Ve **commit mesajı geri alınamaz.** Yasak liste bu yüzden tahmin
edilmedi, **ölçüldü** ve üretecin içine kondu (`_CANARY_BAN`).

İki liste ayrı tutulur ve karıştırmak iki ayrı kapıyı yakar:
**cevap olamaz** (kanarya) ≠ **etiket olamaz** (talimatın içinde saklanan
sözcük — Faz 2'nin *"o-kuyu-n"* bulgusu).

### K31 · ⭑ Sızıntı sayfada değil, İKİ SAYFANIN ARASINDA olabilir ⭑
**24 Ağustos 2026.** Zincirli bir bulmaca, kaynağının cevabını
tüketicinin sayfasına **basmak zorundadır** — okur elindeki sözcüğü
orada arayacaktır. Ama o sütun kaynağın aday kümesiyle **tek bir üyede**
kesişirse, okur kaynağı hiç çözmeden cevabını iki sayfaya bakarak okur.

`qa_readerpack § ⑥` bunu **göremez**: ⑥ tek sayfaya bakar ve iki sayfa
ayrı ayrı temizdir. Yeni denetim `§ ⑫` kesişimi ölçer ve en az **iki**
ortak aday ister. Üretimde iki bulmacada gerçekten bulundu.

### ⚑ A13 · KURUCU GEÇERSİZ KILMASI — FAZ 3 DEVAMI
**24 Ağustos 2026 · kurucu kararı.**

> *"The Founder accepts the current redesign evidence as sufficient to
> continue development before second-round human validation is complete."*

| | |
|---|---|
| Ölçülen öldürme kapısı | ⛔ **HARD-STOP** (1/5) — **değişmedi** |
| Harici oturum | **0** |
| İnsan doğrulaması geçti mi | **HAYIR** |
| Faz 3 girişi | **kurucu geçersiz kılması** |
| `.gate` | `phase3` |

#### Açık sınırlar — silinmeyecek

* İkinci tur insan doğrulaması **YAPILMADI**.
* Hiçbir çözücü oturumu yok; `06_REPORTS/solver/` **boş**.
* Öldürme kapısı **harici kanıtla geçilmedi**.
* Bu **kurucu yetkili kısmi devamdır**.
* ⚠ **Faz 3 "harici olarak doğrulanmış" diye anılamaz.**

#### Ve bu bir düğme değil, bir KAYIT

Geçersiz kılma **ölçümü ezmez**. `kill_gate.py` kararı hâlâ HARD-STOP
olarak hesaplar, yazdırır ve rapora `verdict` alanıyla yazar; geçersiz
kılma yalnızca **çıkış kodunu** değiştirir. Rapor her koşuda dört alanı
birlikte taşır: `measuredVerdict` · `overrideActive` ·
`externalValidation.humanValidationPassed` · `sessionsPerformed`.

⭑ **Ve uydurma yapısal olarak imkânsızdır.** Dört muhafız (`kill_gate.py
§ override_state`) kaydın kendisini denetler ve dördü de kendi kusurlu
fikstürüyle ısırdığı kanıtlanmış olarak durur:

| muhafız | ne yakalar |
|---|---|
| ① | `humanValidationPassed=true` iken `sessionsPerformed=0` |
| ② | bildirilen oturum sayısı diskte ÖLÇÜLENİ aşıyor |
| ③ | geçersiz kılma gerekçesiz/tarihsiz |
| ④ | oturum yokken `status` ≠ `founder_override_partial` |

En fazla şunu diyebilir: *"doğrulanmadı, kurucu devam etti."*
*"Doğrulandı"* diyebilmesinin **hiçbir yolu yoktur**.

#### Sınır: iş geçersiz kılınamaz

`validate_spec § check_gate_scope` geçersiz kılmayı **yalnızca doğrulama
eşiğine** uygular. `puzzlesDrafted` eşiği **her koşulda** aranır — Faz 3
girişi denendiğinde kapı önce **kırmızı yandı** (20 < 40) ve ancak Kapı
II gerçekten yazıldıktan sonra yeşile döndü. Kurucu kararı bir bulmacayı
yazılmış yapmaz.

### K32 · ⭑ Kapı II'nin zorluğu İŞTEN değil, ÇIKARIMDAN gelir ⭑
**24 Ağustos 2026 · Faz 3.** ★'dan ★★'ye geçerken elle iş **artmadı**:
yirmi bulmacanın hiçbiri en kötü hâlinde kendi tavanını aşmıyor ve elle
işin bildirilen süredeki payı kitap genelinde **%23**'tür (tavan %33).

Zorluk üç eksende arttı ve üçü de düşüncedir:

1. **Kural verilmez, bulunur** — sınıflama ailesi bölmeleri gösterir,
   kuralı göstermez.
2. **Çapa basılı olmaktan çıkar** — levha içi şifre altı bulmacalık bir
   rampadır: şerit(çapa basılı) → halka(çapa basılı) → halka(çapa
   siluetten çıkarılır) → halka(çapa VE yön çıkarılır). Her adımda okur
   bir şeyi daha kendi bulur; **hiçbir adımda daha fazla iş yapmaz.**
3. **Mekanizmalar zincirlenir** — bir cevap sonraki bulmacanın basılı
   anahtarı olur (yayılma yarıçapı ≤1).

### K33 · K4 tavanı zorlukla ÖLÇEKLENİR — ve bu sessiz değildir
**24 Ağustos 2026.** ★ için tavan 8'dir ve öyle kaldı. ★★ için **12**'dir.

Gerekçe K4'ün kendi metnindedir: *"4–8 **anlamlı** işlem"i "20–40
**tekrarlı** işlem"e karşı koyar* — yasakladığı şey **tekrardır**,
çokluk değil. ★★'de okur bir dizeyi ters yönde bir kez daha okuyabilir
(katalog onu geri çevirir); altı harflik bir şeritte en kötü hâl 12'dir
ve 20–40 bandına uzaktır.

⭑ Ve asıl emniyet tavan değil, **`repetitionBurden`**dir — o ölçüt
**ölçeklenmez** ve bütün kapılarda aynı tavanı taşır. Kapı II'de ortanca
**2,0** (düşük) ölçüldü.

### K34 · ⭑ Kanarya cevabı TERS de arar — ve bir adı o yakaladı ⭑
**24 Ağustos 2026.** Kapı II'nin adları seçilirken elli aday, takip
edilen dosyalara ve iki yüz commit mesajına karşı tarandı. Bir deniz
memelisinin adı **düz biçimde temizdi** ama **ters çevrildiğinde**
Türkçenin en sık eklerinden birinin içine düşüyordu ve **beş ayrı
dosyada** geçiyordu.

> **Ders:** bir adı kanaryaya karşı denerken TERS biçimini de dene.
> Kanarya bunu zaten yapıyordu; ben yapmıyordum.

**Ve ikincisi commit'ten SONRA çıktı.** Bir yazı gerecinin adı cevap
olmuştu; sonra bu projenin kendi raporuna *"gerçek ölçüm ... kâğıt ve
gözle yapılır"* diye yazdım ve kanarya kendi raporumu sızıntı saydı —
**haklıydı.**

> ⭑ **Asıl ders süreçtir:** kanarya commit'ten ÖNCE koşar. Bu kez
> sonra koştu ve CI kırmızı yandı. Commit MESAJI temizdi (geri
> alınamayan kanal); düzeltme bir sonraki commit'e sığdı.

İki üye artık `build_gate2._ANSWER_BAN` içinde, gerekçesiyle birlikte —
ve ikisi de **katalogda akran olarak kalır**. Yasak dar tutulur.

### K35 · Sızıntı, kapının BAKTIĞI YERİN DIŞINDA olabilir
**24 Ağustos 2026.** `qa_readerpack § ⑫` zincirin kaynağını iki sayfanın
kesişiminden okumayı engeller — ama yalnızca **bildirilen bağımlılık**
için. Kapı II'de iki çizelge hücresi, **bağımlı olmadıkları** iki
bulmacanın cevabını basıyordu; ⑫ oraya bakmıyordu.

Artık üreteç, bir çizelge ya da ızgara hücresinin başka bir bulmacanın
cevabını taşımasını **üretim anında** reddeder — zincir değeri olarak
kasıtlı konanlar hariç.

### K12 · Kapı V dizgiye bağlıdır ve en son kilitlenir
Kapı V öz-göndergeseldir: kitabın **fiziksel yapısını** kullanır
(sayfa numaraları, dizin, kolofon). Dizgi değişirse **kırılır**.

Bu yüzden dizgi Faz 5'te **dondurulur** ve Kapı V ondan **sonra**
kilitlenir. Faz 6 sayfa sayısını yalnızca **doğrular**.

### K36 · ⭑ AHA ÖLÇEKLENMEZ, ÇIKARIM ÖLÇEKLENİR ⭑
**24 Ağustos 2026 · Faz 4.** Faz 4'e kadar deneyim kapısının tek eşiği
kitap geneliydi: `ahaScore` ortancası ≥ 4. O eşik **yeşildi ve
yanıltıyordu.**

Beş kapının beşi de 4,0 gösteriyordu. Kapı kapı bakıldığında sebep
çıktı: Kapı III–V'te öğretilmiş bir mekanizmanın **tekrarına** da 4 ve
hatta 5 yazılmıştı. Kitap geneli ortanca, kapı düzeyindeki şişmeyi
**gizliyordu.**

> **Ve tekrarlar gerçekten tekrardı.** `g3-007`, `g3-011` ve `g3-015`,
> `g3-001` ile **kelimesi kelimesine aynı talimatı**, aynı kısıtları ve
> aynı adım sayısını taşıyor; yalnızca verileri farklı. Bu bir keşif
> değildir. On kayıt kendi ölçülen tavanının üstündeydi ve puanları
> **düşürüldü** — şişirilmedi:
>
> `g3-007` 4→3 · `g3-011` 4→3 · `g4-007` 4→3 · `g4-008` 4→3 ·
> `g4-012` 4→3 · `g4-015` 5→3 · `g5-012` 4→3 · `g5-013` 5→4 ·
> `g5-014` 4→3 · `g5-018` 5→4

**① Tavan artık ÖLÇÜLÜYOR.** Yazar tavanın altına inebilir, üstüne
çıkamaz:

| durum | tavan |
|---|---|
| mekanizmanın **ilk kullanımı** | **5** — keşif |
| tekrar · çıkarım oranı ilk kullanımdan **büyük** | **4** — derinleşme |
| tekrar · çıkarım oranı büyük **değil** | **3** — yordam |

**② Eşik KAPI BAZINDA ve kapının TÜRÜNE göre.** Kapı III–V öğretilmiş
mekanizmaları **bilerek** tekrar kullanır; yol haritasının tasarımı
budur. Onlardan Kapı I'in yenilik oranını istemek, ya sahte puan ya da
düzinelerce alâkasız mekanizma üretirdi:

    keşif kapıları (I · II)      aha ortancası ≥ 4
    akıcılık kapıları (III–V)    aha ortancası ≥ 3

**③ Yenilikten vazgeçilen yere ÇIKARIM konur.** Ölçüt uydurulmadı;
veride zaten duruyordu:

    çıkarım oranı = bildirilen dakika ÷ ölçülen elle işlem

Elle işlem beş kapıda da **6–8 bandında sabittir**; artan tek şey
düşünmedir. Ölçülen:

| kapı | I | II | III | IV | V | son soru |
|---|---:|---:|---:|---:|---:|---:|
| çıkarım oranı | 1,00 | 1,27 | **2,32** | **3,43** | **4,42** | 6,00 |
| aha ortancası | 4,0 | 4,0 | 3,0 | 3,0 | 3,5 | 5,0 |

Akıcılık kapıları için taban **2,0**'dır ve oran kapıdan kapıya
**yükselmek zorundadır**. Ayrıca hiçbir kapı yirmi düz tekrardan ibaret
olamaz: kapı başına en az **dört** ilk kullanım ya da ölçülmüş
derinleşme (ölçülen III 15 · IV 15 · V 14).

⭑ **Değişmeyen şey:** *daha sonraki bir bulmaca öğrenilmiş bir
mekanizmayı DERİNLEŞTİREBİLİR — ama yeni bir keşif ilan EDEMEZ.*

Eşikler betiğin içinde değil `project_config.json § experience`
içindedir; gerekçe `killGate` ile aynıdır: betiğe gömülü bir eşik
sessizce düşürülebilir. Fikstürler: `selftest § ⑨`.

### K37 · ⭑ ISINMA ÖN MADDEDE BİTMEZ — DERSİ KENDİ KAPISINA GÖTÜRÜR ⭑
**24 Ağustos 2026 · Faz 4.** `qa_experience § 7` her mekanizmanın,
ticari bulmacada karşılaşılmadan **önce**, çözülmüş küçük bir örnekle
öğretilmesini ister. Faz 4 dokuz yeni mekanizma getirdi ve dokuzunun da
örneği yoktu.

Kolay olan, dokuzunu da ön maddeye eklemekti. **Yanlış olan da oydu:**
Kapı IV'ün dersini ön maddeye koymak, okura otuz sayfa önce, henüz
göremeyeceği bir şeyi anlatmaktır.

Isınma örnekleri artık bir `gate` alanı taşır ve **kendi kapılarının
açılışında** dururlar. Ön madde yalnızca Kapı I'in yedi örneğini taşır.

Ölçüldü: dokuz yeni örnek **5,1 sayfa**; kapı metinleri 10,4–14,1 sayfa
ve bütçeleri 34. **Hiçbir kapı taşmadı ve sayfa sayısı değişmedi.**

⚠ Ve bir örnek, öğretmeye çalıştığı şeyin **yanlış olduğunu**
gösteriyordu: son sorunun ısınması "sondan sayınca sözcük çıkar" diyor
ama uydurma sözleri "ÜĞU" veriyordu. Sözler artık **aranarak** seçilir
(baştan `DĞR` — sözcük değil; sondan `ATA` — sözcük) ve seçim üretim
anında doğrulanır.

### K38 · ⭑ SON SORUNUN CEVABI KİTAPTA BULUNMAMALIDIR — VE BUNU BİR KAPI ARAR ⭑
**24 Ağustos 2026 · Faz 4.** Kitabın yüz cevabı basılı bir katalogda
**bulunmak** zorundadır (K22). Son sorunun cevabı **bulunmamak**
zorundadır — yoksa doğrulama sayfasının anlamı kalmaz (yol haritası
Faz 4 § 12).

Bu tam tersi kural hiçbir kapının işi değildi: `qa_dependency` DAG'a
bakar ama beş kapının **beşinin birden** katkı vermesini istemez;
`qa_answerspace` tekilliği ispatlar ama yokluğu istemez; kanarya cevabı
**depoda** arar, kitabın **sayfalarında** değil.

`qa_meta.py` o üç boşluğun kesiştiği yerde durur ve 29 denetim yapar.
En sertleri:

* beş kapının **beşi de** katkı veriyor mu (§ 12 · bloklayıcı);
* bildirilen kapı sözü o kapının **gerçek çıktısı** mı;
* cevap **birleştirilmiş sözlerin içinden okunuyor mu** — birleştirme bir
  çıkarım değildir, okur onu kazara bulur;
* cevap sayfalarda, başlıklarda, ısınmalarda, basılı çizelgelerde ya da
  açılış anlatılarında geçiyor mu.

⚠ **VE İLK YAZIMINDA O SIZINTI DENETİMLERİ SESSİZCE YEŞİL YANIYORDU.**
Aranan anahtar büyük harfti, aranan metin ise `pl.squeeze` ile küçük
harfe indirilip Türkçe ı/İ/I katlaması yapılmış hâldeydi: iki dize
hiçbir zaman eşleşemezdi. Kusuru **fikstürler** yakaladı — kapı üretim
verisinde yeşildi ve öyle kalacaktı.

> **Ders:** bir sızıntı kapısının yeşili, ancak o kapının bir sızıntıyı
> yakaladığı GÖRÜLDÜKTEN sonra bir şey ifade eder.

### K39 · Bir kapı, ölçtüğü şeyin BÜYÜDÜĞÜNÜ varsaymalıdır
**24 Ağustos 2026 · Faz 4.** `pilot_pages.py` Faz 2'de yazıldı; o gün
kitapta yalnızca Kapı I vardı. Bütün `book.json` bulmacalarını topluyor,
toplamı **Kapı I'in bütçesiyle** karşılaştırıyor ve arka maddeyi **×5
ile ölçekliyordu**.

İki kapı yazıldığında ölçüm iki katına çıktı ve **kimse fark etmedi**
(bütçede pay vardı). Beş kapı yazıldığında beş katına çıktı ve kapı
kırmızı yandı — içerik büyüdüğü için değil, **ölçenin kendisi bozuk
olduğu için.**

Ölçüm artık kapı bazındadır ve hiçbir yerde ×5 yoktur. Ölçtükleri:
kapı metni + ısınma + açılış anlatısı + şekil satırları, kapı kapı.

Aynı koşuda iki şey daha çıktı:

* **Araçlar levhası 2 sayfaya sığmıyordu.** Faz 1'de dört çizelgeydi;
  Faz 4 sekiz çizelge daha ekledi (408 satır → 3,2 sayfa). Kısaltmak
  seçenek değildi: her çizelge bir kapının **cevap uzayıdır** (K22) ve
  bir satırı silmek o satırı kullanan bulmacayı çözülemez yapar. Bütçe
  **2 → 4**; sayfa modeli **236 → 238** (hedef 230 ± %6 içinde).
* **Kelime sayısı üretilen belgelerde sabit `0` basıyordu.** Ölçüm
  izlenen raporda zaten duruyordu; belge ona hiç bakmıyordu. Ölçülen:
  **17.211** kelime.

### K40 · Okur dosya anahtarı görmez
**24 Ağustos 2026 · Faz 4.** Kapı V'in yapı levhası okura çizelge
adlarını basar. Üreteç yalnızca Kapı III–V çizelgelerini tanıyordu;
Kapı I–II'ninkiler **dosya anahtarı** olarak düşüyordu ve okur
levhada `+ esik-alfabesi + esik-sayilari - Çizelge J` görüyordu.

Ad artık araçlar levhasının kendisinden okunur ve bilinmeyen bir anahtar
üretim anında **çöker** — sessizce slug basmaz.

### K41 · Kısa cevaplar kitabın KENDİ SÖZ DAĞARCIĞIYLA çarpışır
**24 Ağustos 2026 · Faz 4.** Faz 4'ün görsel çapraz sayfa denetimi yedi
eşleşme buldu. **İkisi gerçek sızıntıydı** ve onarıldı (anahtarlı
alfabenin anahtarı bir cevaptı — § K38 raporu). **Üçü değildi:**

| görünüm | gerçek |
|---|---|
| `KAPI` · çizelge **başlığı** ve meta levhasının sütun adı | "kapı" bu kitabın **yapısal ismidir** |
| `AYNA` · katmanlı zincir levhasında *"ayna ekseni"* | dönüşümün **adıdır** |
| `ASMA` · `BASMA` sözcüğünün içinde | alt dize artefaktı |

Üçü de **dört harflidir**. Kanaryanın tabanı altı harftir ve onları
**bilerek** görmez: kısa sözcükler olağan nesirle çarpışır ve altı
harfin altında bir kanarya sürekli yalancı kırmızı yakar. Taban bir
tercih değil, `_CANARY_BAN` gerekçesinin kendisidir.

⚠ **Ama bedeli var ve ölçüldü:** ısınma örneği yazarken `KAPI`
çarpışması yüzünden çözülmüş adımlarda "kapı" sözcüğünü **kullanamadım**
ve örnek onun etrafından yazıldı. Bir cevap, kitabın kendi öğretim
metnini kısıtlıyorsa yanlış seçilmiştir.

**Kapı I'in cevapları DEĞİŞTİRİLMEDİ** ve gerekçesi tek cümledir: o
yirmi bulmaca **ölçülen öldürme kapısının kanıt tabanıdır** (A12 · 1/5).
Onları değiştirmek, ölçümün ölçtüğü nesneyi değiştirmek olurdu.

⭑ **Kural ileriye dönüktür:** yeni bir cevap seçilirken sözcük, kanarya
tabanının altında olsa bile, **talimat şablonlarında ve levha
künyelerinde** aranır. `EŞİK` bu yüzden yasaktı (K18); `KAPI` ve `AYNA`
aynı ölçütle yasaklanırdı — ölçüt o gün yoktu.

### K42 · ⭑ ANLATI KURALI ÖLÇÜYE GÖRE DARALTILDI ⭑
**24 Ağustos 2026 · Faz 5.** `STYLE § 1` anlatı satırı için şunu der:
*"bir sayı, bir yön, bir konum veya bir çizelge adı geçemez."*

Kural bir kapıya bağlandığında **otuz dört sayfa** kırmızı yandı. Ve
otuz dördün büyük çoğunluğu şuydu:

> *"İkinci yol birinciyle aynı görünür."*
> *"Üçüncü sayım. Artık ne aradığınızı biliyorsunuz."*

Bunlar mekanik değil, **anlatı sıralamasıdır**: bir kütüphaneci kaçıncı
kayıtta olduğunuzu söyleyebilir. Kuralın koruduğu şey sıralama değil,
**bir üslup düzeltmesinin bir bulmacayı sessizce bozmasıdır**.

Kural daraltıldı ve daraltıldığı yazıldı:

| ⛔ yasak | gerekçe |
|---|---|
| çizelge adı | bir çizelge adı daima mekaniktir |
| yön sözcüğü | bu kitapta yön daima mekaniktir |
| **rakam** | nesirde bir rakam daima bir niceliktir |
| sayfayla çelişki | anlatının sayısı levhanınkiyle tutmuyorsa okur birine inanır |

| ✅ serbest | gerekçe |
|---|---|
| sıra sözcüğü | anlatı sıralamasıdır, mekanik değil |

⭑ Ve daraltmanın kendisi de **fikstürle ölçülür**: sıra sözcüğü taşıyan
bir anlatı satırı kapıdan GEÇMEK zorundadır. Bir kuralı gevşetmek ile
bir kuralı DOĞRU YERE koymak arasındaki fark, ikincisinin de test
edilmesidir.

### K43 · ⭑ BİR TEKİLLİK İSPATI, İSPATLADIĞI ŞEYİ VARSAYAMAZ ⭑
**24 Ağustos 2026 · Faz 5.** Line editor bir çizelge bulmacasının **iki
cevabı olduğunu** bildirdi. Doğrulandı ve sebep bildirilenden ağırdı:
kabul yordamında iki süzgeç vardı — biri okurun sayfadan aldığı sütun,
öteki `take` sütununa yazılmış ve **değeri bulmacanın kendi cevabıydı**.

O süzgeçle ispat daima tek üye bulur ve `qa_answerspace` **yeşil yanar**.
Ama okurun elinde o süzgeç yoktur ve sayfa ona iki satır bırakır.
Sözleşmenin **birinci sözü** o sayfada tutulmuyordu.

`qa_answerspace` artık `take` sütununa yapılan süzgeçleri **atar**:
ispat, okurun gerçekten sahip olduğu süzgeçlerle koşar.

> **Ders:** bir ispatın yeşili, ispatın NEYİ VARSAYDIĞI bilinmeden bir
> şey ifade etmez. Bu kapı yüz bir bulmacada iki yıl yeşil yanabilirdi.

### K44 · ⭑ KİTAP OLMAYAN BİR HATAYI VAAT EDEMEZ ⭑
**24 Ağustos 2026 · Faz 5.** Yedi sayfa şunu basıyordu: *"Katmanlar ters
sırada uygulanırsa ad çıkmaz."* Ölçüldü: **yedi bulmacanın yedisinde**
ters sıra **aynı cevabı** veriyor — katmanlardan biri harf DEĞİŞTİRİR,
öteki harf YERİNİ değiştirir ve bu iki işlem birbirinin yerine geçer.

⚠ **Bu, kolay bir bulmacadan kötüdür.** İki sırayı da deneyen okur aynı
cevabı iki kez alır. Sözleşmenin birinci sözünün açıklaması ona
*"ikinci bir okuma bulduysanız ya siz ya kitap yanılmıştır"* der — yani
kitap, kendi vaadiyle kendini bozuk gösteriyordu.

Kural geneldir ve `qa_editorial § ⑦` onu ölçer: **bir sayfa "şunu
yaparsan cevap ÇIKMAZ" diyorsa, o şey gerçekten cevabı bozmak
zorundadır.**

### K45 · ⭑ AİLE ÖĞRETİLMİŞ OLABİLİR; İŞLEM ÖĞRETİLMEMİŞ OLABİLİR ⭑
**24 Ağustos 2026 · Faz 5.** Üç levha "ayna ekseni" basıyor ve o işlem
kitabın **hiçbir yerinde** öğretilmiyordu — ne ısınmada, ne şifre
referansında. Okur onunla ilk kez Kapı IV'ün **ikinci** bulmacasında
karşılaşıyordu.

Ve `qa_experience § 7` bunu göremiyordu çünkü **AİLEYİ** denetliyor:
`layered-chain` ailesi öğretilmiş görünüyordu. Ama o ailenin iki işlemi
var ve ısınma yalnızca birini gösteriyordu.

§ 7b eklendi: **levhanın BASTIĞI her işlem adı** öğretilmiş olmalıdır.

### K46 · ⭑ KANARYA, HENÜZ TAKİP EDİLMEYEN DOSYAYI GÖRMÜYORDU ⭑
**24 Ağustos 2026 · Faz 5.** Yeni üretilen levha prompt kütüphanesi
**beş cevabı** düz metin taşıyordu ve commit edildi; CI'daki kanarya
onu buldu ve kırmızı yandı.

⚠ **Ve kanarya commit'ten ÖNCE koşmuştu** (K34'ün süreç dersi
uygulanmıştı) — **yeşil yanmıştı**. Çünkü `git ls-files` yalnızca
ZATEN TAKİP EDİLEN dosyaları verir; yeni üretilmiş bir dosya kanaryaya
görünmüyordu.

> **Süreç doğruydu; kapsam eksikti.** Bir kapının ne zaman koştuğu,
> neye baktığı bilinmeden bir şey ifade etmez.

Kapsam artık: takip edilenler **+ `.gitignore`'un dışlamadığı her yeni
dosya** — yani bir sonraki commit'e girecek her şey, girmeden önce.
Taranan dosya 100 → 106.

### K47 · Levha bir resim değil, bulmacanın VERİSİDİR
**24 Ağustos 2026 · Faz 5.** Gravür prompt kütüphanesi levhanın dizgi
karşılığını **olduğu gibi** basıyordu ve bazı levhalar çizelgedir:
dosya gerçek cevapları taşıdı (K46).

Ama harflere zaten gerek yoktu. Kütüphanenin kendi mutlak yasağı
*"no text, letters, numerals or captions inside the image"* der:
gravürcünün ihtiyacı **geometridir** — kaç göz, kaç istasyon, hangi
kenar. Harfleri kitap dizer.

Şekil artık **iskelet** olarak basılır: harf ve rakam `·`, çerçeve ve
işaret korunur. Ve prompt kütüphanesi, sayfa modelinin istediği levha
sayısının **hepsini** taşımak zorundadır — eksik bir prompt, kurucunun
eksiği kendi keşfetmesi demektir.
