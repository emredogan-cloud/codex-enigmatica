# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript ve **çözüm katmanı** politikası | **YÜKSEK** | Faz 1 | ✅ **KAPANDI** → K10 + K14 (beş hatlı koruma) |
| **A2** | 5 kapı teması onayı | YÜKSEK | **Faz 2 başlamadan** | AÇIK |
| **A3** | **5 harici çözücü kim** | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — **sert bloklayıcı** |
| **A4** | Doğrulama sayfası barındırma | ORTA | Faz 5 | AÇIK |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | Faz 2 | AÇIK |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |
| **A7** | **Bulmaca başına doğrulama** — doğrulama sayfası 100 cevap alanı taşısın mı | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — § aşağı |
| **A8** | **Sayfa hedefi 208 → 230** (telif 9,85 $ → 9,58 $) | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — § aşağı |
| **A9** | **Pilot levhaların POD provası** Faz 2'ye alınsın mı | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — § aşağı |
| **A10** | Faz 3'e **ikinci öldürme kapısı** eklensin mi | ORTA | Faz 3 başlamadan | AÇIK |
| **A11** | `ENIGMATICA_CANARY_SALT` CI sırrı kurulsun | ORTA | **Faz 2 başlamadan** | AÇIK |

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

### A8 · Sayfa hedefi 230

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

---

### A9 · Pilot levhalarının POD provası

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

---

### A3 · Beş harici çözücü — öldürme kapısının tabanı

**Bu, Faz 2'nin sert bloklayıcısıdır ve bütün projenin kaderi ona bağlıdır.**

Ajan bulmaca çözemez — çözümü zaten bilir; "çözülebilir" yargısı kanıt
değildir. Test **harici** insanlarladır ve çözücüler **bağımsız** çalışır.

Çözücü bulunamazsa **Faz 2 bloklanır**. Kabul edilen bir bloktur:
**sahte test kaydı üretilmez.**

Kimlikler anonimdir (`solver-01`) ve şema bu biçimi zorunlu kılar.

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

### K12 · Kapı V dizgiye bağlıdır ve en son kilitlenir
Kapı V öz-göndergeseldir: kitabın **fiziksel yapısını** kullanır
(sayfa numaraları, dizin, kolofon). Dizgi değişirse **kırılır**.

Bu yüzden dizgi Faz 5'te **dondurulur** ve Kapı V ondan **sonra**
kilitlenir. Faz 6 sayfa sayısını yalnızca **doğrular**.
