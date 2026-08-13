# FAZ 2 RAPORU — pilot bulmacalar, cevap uzayı ve öldürme kapısı

> **Codex Enigmatica** · 13 Ağustos 2026 · dal `faz/2-pilot` · kapı `phase1`
>
> ⛔ **ÖLDÜRME KAPISI KARARI: `BLOCKED`**
>
> Yirmi bulmaca yazıldı ve bütün teknik kapılardan geçti. Beş harici
> çözücü **belirlendi**. **Hiçbir oturum yapılmadı.**
> Öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz.

---

## 0 · Tek bakışta

| | |
|---|---:|
| Türkçe pilot bulmaca | **20 / 20** yazıldı |
| Cevap uzayı bağımsız doğrulanmış | **20 / 20** |
| Bağımsız üretilip elenen aday dize | **1.072** |
| Onaylanmış alternatif çözüm | **0** |
| Belirsizlik puanı ≤ 2 | **20 / 20** (18 puanı 1, 2 puanı 2) |
| Üç kademeli ipucu | **60** |
| Yeni kalite kapısı | **4** (`answerspace` · `handoff` · `readerpack` · `kill_gate`) |
| Kapıların kendi testi | **123 → 154** denetim |
| Kırmızı takım bulgusu | **28** — hepsi kapatıldı |
| İç çözücü | **3 bağımsız geçiş** — ⚠ **kanıt sayılmaz** |
| **Harici çözücü oturumu** | ⛔ **0 / 5** |
| **Öldürme kapısı** | ⛔ **BLOCKED** |
| Public depoda çözüm sızıntısı | **0** |
| CI | ✅ yeşil |

---

## 1 · Faz 2 kapsamı ve ne yapıldı

Faz 2'nin görevi *"yirmi bulmaca yazmak"* değildi. Görev şuydu:

> Yirmi gerçek bulmaca kur → tam çözülebilirlik sistemine sok →
> beş gerçek insanla test et → kusurları bul → **kök nedeni** düzelt →
> sistemin çalıştığını KANITLA → kitabın devam edip etmeyeceğine karar ver.

Bu zincirin **beşinci halkası hariç** hepsi tamamlandı. Beşinci halka
(*beş gerçek insan*) ajanın yapabileceği bir iş değildir ve yapılmamıştır.

---

## 2 · Türkçe pilot — neden ve hangi sınırla

**A3 kapandı:** beş harici çözücü belirlendi ve **beşi de Türkçe
konuşuyor**. Pilot dilini bu tek olgu belirledi.

Gerekçe tek cümledir: **bir bulmacanın mekaniği ancak çözücünün ana
dilinde ölçülebilir.** Yabancı dilde çözülemeyen bir bulmacada
*"mekanizma mı bozuk, cümle mi anlaşılmadı"* ayrımı yapılamaz — ve ayrım
yapılamayan bir ölçüm gürültüdür.

| Alan | Değer |
|---|---|
| `language.pilotLanguage` | `tr` — **ölçüm aracı** |
| `language.productionLanguage` | `en` — **ürün** |
| `language.pilotIsProductionManuscript` | **`false`** |

> ⚠ **Türkçe başarı, İngilizce çözülebilirliğin kanıtı DEĞİLDİR.**
> Bu bir ihtiyat cümlesi değil, § 12'de **ölçülmüş** bir olgudur.

---

## 3 · Yirmi bulmacanın envanteri

Kapı I · **Eşik** · zorluk ★ · Faz 1'in slotladığı 20 yuva **değiştirilmedi**.

| Mekanizma ailesi | Bulmaca | Pay |
|---|---:|---:|
| `plate-observation` | 5 | %25 |
| `constraint-logic` | 5 | %25 |
| `substitution-cipher` | 3 | %15 |
| `script-decoding` | 2 | %10 |
| `plate-embedded-cipher` | 2 | %10 |
| `transposition-cipher` | 2 | %10 |
| `gate-synthesis` | 1 | %5 |

Çeşitlilik eşikleri: en yüksek aile payı **%25** (tavan %35) · ayrı aile
**7** (taban 4) · en uzun ardışık aynı aile **2** (tavan 6). ✅

| | |
|---|---:|
| Levha taşıyan bulmaca | 10 |
| Levhası **veri taşıyan** bulmaca | 4 |
| Çözüm adımı | 81 |
| Üretilen alternatif aday | 80 (bulmaca başına 4) |
| Modellenen toplam süre | 153 dk |
| Bağımlılık kenarı | 3 zincir + kapı bulmacası (19 girdi) |

---

## 4 · ⭑ `answerSpace` — Faz 2'nin birinci teslimatı ⭑

Faz 1'in kırmızı takımı on yedi ailenin **dokuzunda** tekillik ispatının
totoloji olduğunu göstermişti. Tekrar eden kusur:

> **Sayım alanını, cevabı zaten bilen yazar tanımlıyordu.**

### 4.1 · Mimari

Cevap uzayı artık bir **liste değil, bir üreteçtir**. `qa_answerspace.py`
yazarın listesini **okumaz**; bulmacanın girdisinden ve kitabın **basılı
çizelgelerinden** alanı yeniden üretir ve tek soru sorar:

> Okurun kitaptan öğrendiği yordamlarla ulaşabileceği bütün dizeler
> içinde, **basılı** kabul yordamından geçen kaç tane var?

```
0  → bulmaca ÇÖZÜLEMEZ
1  → tekil ✅
≥2 → İKİNCİ CEVAP — çözülemez olmaktan daha kötüdür
```

Üç sahte mekanizma **izin listesiyle** yasaklandı: yazar tarafından
sayılmış alan · tek üyeli alan · *"yazar öyle diyor"* kabul yordamı.

### 4.2 · Ölçüm

| | |
|---|---:|
| Bağımsız üretilen aday dize | **1.072** |
| En küçük alan | 12 |
| En büyük alan | 60 |
| **Tam olarak bir üye kabul edildi** | **20 / 20** |

### 4.3 · ⭑ K22 — kabul yordamı yazardan çizelgeye taşındı ⭑

`answerSpace` bir soruyu açıkta bırakıyordu: bir üyenin *kabul edilmesi*
neye göre? *"Yazar bunu anlamlı buluyor"* bir kabul yordamı değildir —
kapatılan totolojiyi bir adım öteye taşımaktır.

Çözüm **araçlar levhasındadır**: Kapı I'in bütün cevapları ön maddede
**basılı** 60 sözcüklük *Eşik Sözlüğü*'nün üyesidir ve sözleşme sayfası
bunu okura **söyler**. Kabul yordamı böylece mekanikleşir.

**Ödenen bedel açıkça kaydedildi** (`RED_TEAM_CHECKLIST § 5.6`): bir okur
hiçbir şey çözmeden 1/60 ≈ %1,7 olasılıkla tahmin yürütebilir. On dokuz
bulmacayı tahminle bitirme olasılığı 60⁻¹⁹ — sıfır; ama **tek** bir
bulmacayı kaba kuvvetle geçmek mümkündür. Karşı önlem A7'nin yan
kazancıdır: doğrulama sayfası reddedilen dizeleri kaydeder ve kaba kuvvet
kalıbı tespit edilebilirdir.

---

## 5 · İç çözücü sonuçları — ve neden kanıt değiller

Üç bağımsız iç çözücü geçişi yapıldı. Hiçbiri çözüm anahtarını görmedi.

| Geçiş | Çözülen | İpucu | Süre | Bildirilen kusur |
|---|---:|---:|---:|---:|
| Solver B | 20 / 20 | 0 / 60 | ~41 dk | 12 |
| Solver C | 20 / 20 | 0 / 60 | ~94 dk | 11 + **1 bloklayıcı** |
| Solver D | 20 / 20 | 0 / 60 | ~76 dk | 4 · **ikinci cevap: 0** |

Eğri doğru yönde: metin–levha çelişkisi **11 → 3**, ikinci cevap
**2 → 0**. Üçüncü geçiş hiçbir savunulabilir ikinci cevap üretemedi ve
kaba kuvvetle denedi: 28 kaydırmanın tamamı, 29 yansıma ekseninin tamamı,
sekiz levha okumasının tamamı, üç eleme bulmacasının 60 üyelik alanı.

> ### ⛔ BU SATIRLAR ÖLDÜRME KAPISINDA SAYILMAZ.
>
> `internalSolverCountsAsEvidence: false` bir politika değil, bir
> **mekanizmadır**: `validate_spec § check_test_status` iç çözücü
> kayıtlarını `tested` şartına dâhil etmez.
>
> İç çözücüler **yapay**dır, hızlıdır ve pes etmezler. Perakende okurun
> kitabı **iade ettiği** yerde ısrarla devam ederler — ve iade eden okur
> hiçbir veri satırı üretmez. İç çözücünün değeri kusur bulmaktır,
> çözülebilirliği kanıtlamak değil.

Ve tam olarak bunu yaptılar: **28 kusurun 28'ini** iç çözücüler ve kapılar
buldu, hiçbiri okura ulaşmadan.

### 5.1 · Süre — ve iç çözücünün neden süreyi ölçemediği

İç çözücüler 41 ve 94 dakika bildirdi. Model 198 dakika diyor
(153 bulmaca + 45 oturum yükü). İkisi **karşılaştırılabilir değildir**:
iç çözücü yirmi dokuz harflik bir halkayı milisaniyede tarar, insan
kâğıtla tarar. Solver B'nin kendi tahmini insan için **3–5 kat**, yani
2–3 saat.

⚠ Ve bir tasarım kokusu bildirildi: üç şifre bulmacası (kaydırma,
anahtarlı alfabe, yansıma) **kâğıt kalemle sıkıcı** — zor değil, sıkıcı.
Bu, harici testin ölçmesi gereken ilk şeydir.

---

## 6 · Kırmızı takım — 28 bulgu

Tam defter: [`RED_TEAM_CHECKLIST.md § 5`](../00_CONTEXT/RED_TEAM_CHECKLIST.md).
Buradaki üç tanesi en ağırlardır.

### 6.1 · ⭑ Sayı tablosu hata TESPİT ETMİYORDU — ve kapı bunu görmüyordu ⭑

Levha içi şifrede okur dört kenarı okur; yanlış köşe veya yön **sekiz**
farklı dörtlü verir. Tasarım *"yanlış okuma tabloda yoktur"* diyordu.

**Ölçüldüğünde sekiz okumanın BEŞİ tablodaydı.** Her levha bulmacasının
beş ulaşılabilir cevabı vardı — ve ikisi diğer bulmacanın doğru cevabıydı.

Kapı bunu görmemişti çünkü kabul yordamı **doğru okumayı sabit
yazıyordu**. Yani K21'in öldürmeye çalıştığı totoloji, bu kez
**doğrulayıcının kendi içinde** duruyordu.

> **Ders:** bir kapı, denetlediği şeyin **tanımını yazardan alıyorsa**
> denetlemiyordur.

**Kapatıldı:** sekiz okumanın tamamı açılır; tablo yeniden tasarlandı,
iki levha ayrı sayı kümesi kullanır; fikstür yazıldı.

### 6.2 · ⭑ Bulmacalar okur paketinde ÇÖZÜLEMİYORDU ⭑

On bulmacanın levha **metni** vardı, levha **verisi** yoktu. Nitelik
haritası yalnızca cevap anahtarındaydı.

Sekiz kapının sekizi de **korumalı katmanı** denetliyordu; hiçbiri okurun
**eline ne geçtiğine** bakmıyordu. Kusursuz bir tekillik ispatı,
çözülemeyen bir bulmacanın üzerinde duruyordu.

**Kapatıldı:** `qa_readerpack.py` — yedi denetim, hepsi ters yönden sorar:
*okur bunu çözebilir mi?*

### 6.3 · ⭑ Gerçek bir ikinci cevap — kaynağı tek bir yanlış edattı ⭑

Bir sütun bulmacasında metin *"Her sütunun **tepesinde** bir Sözlük
numarası vardır"* diyordu; levhada numaralar **alttaydı**. Metni birebir
uygulayan çözücü, **kitabın kendi cümlesine dayanan** savunulabilir bir
ikinci cevap üretiyordu.

İkinci bir çözücü aynı bulmacada **ikinci** bir ikinci cevap buldu:
sütunların dibindeki taban işareti "yatay kollu" olduğu için çentik
sayılabiliyordu — ve **iki okuma da** *"beş sütundan birinde"* tekillik
vaadini **yerel olarak** sağlıyordu. Okurun yanlış olduğunu anlamasının
hiçbir yolu yoktu.

> `qa_answerspace` bu sınıfı yakalayamaz: **mekanizma doğruydu, metin
> yanlıştı.** Bunu ancak bir insan (veya bağımsız bir çözücü) bulur —
> harici çözücü testinin neden vazgeçilmez olduğunun mekanik kanıtı.

**Kök neden kapatıldı:** şekil üretiliyordu, onu tarif eden cümle **elle
yazılıyordu**. Levha üreteci artık *(şekil, künye)* çifti döndürür ve
künye cümlesi maddelere olduğu gibi girer. Elle yazılmış konum iddiası
kalmadı.

### 6.4 · Türkçe pilot ölçüm makinesini kırdı

`NFKD` noktasız `ı` ile noktalı `İ`yi **çözmez**. Yani `"IŞIK"` ile
`"ışık"` iki farklı normal biçime sahipti — ipucu sızıntısı denetimi ve
kanarya, cevabı küçük harfle yazan bir sızıntıyı **kaçırırdı**.

Katlama (`ı/İ/I → i`) iki dosyada birden, küçültmeden **önce** uygulanır;
ayrışmamaları bir fikstürle korunur.

> Talimat § 17'nin uyardığı şeyin canlı örneği: **bir dil değişimi ölçüm
> makinesinin kendisini de değiştirir.**

### 6.5 · Var olmayan bir çizelgeye gönderme

Üçüncü çözücü ikinci cevap **bulamadı** ama sekiz ayrı cümlede bir künye
hatası buldu: çizelgeler bir kez yeniden adlandırılmış, üç bulmacanın
gövdesi **eski adlarda kalmıştı**. Okur bir bulmacada **hiç var olmayan**
bir çizelgeye gönderiliyordu.

Sözleşmenin dördüncü sözünün doğrudan ihlali — ve en zararlı hata
cinsinden: **okur bunu kendi hatası sanır.** Kök neden yine aynıydı: okur
paketinin başlıkları elle yazılıyordu. Artık çizelge verisinden okunur ve
`qa_readerpack § ⑧` sarkan göndermeyi kırmızı yakar.

### 6.6 · ⭑ CI'ın kendisi bir körlük yarattı ⭑

İlk yirmi bulmaca `drafted` olur olmaz **CI kırmızı yandı — ve haksızdı.**

Korumalı katman klonda **hiç yoktur** (tasarım gereği). Kapı bunu
*"korumalı kayıt KAYIP"* diye okuyordu: kendisine hiç gösterilmemiş bir
dosyayı kayıp sanıyordu. Faz 1'de bu ayrım gerekmiyordu çünkü hiçbir
bulmaca `drafted` değildi — kusur, kodun ilk kez **gerçek veriyle**
karşılaştığı anda doğdu.

| Durum | Davranış |
|---|---|
| Katman **tamamen** yok (CI) | **boş koşar ve "bu bir GEÇİŞ DEĞİLDİR" der** |
| Katman **var ama eksik** | **KIRMIZI** — yazar çözümü yazmayı unuttu |

İkisinin de fikstürü yazıldı.

### 6.7 · Kanarya iki kez kendi yazarını yakaladı

- Yeni selftest fikstürleri gerçek Sözlük'ten sözcük kullanıyordu →
  `05_TESTS/selftest.py` sızıntı olarak bildirildi.
- Bu raporun kardeşi olan bulgu defteri, bir düzeltmeyi anlatırken **yeni
  cevabı adıyla andı** → `RED_TEAM_CHECKLIST.md` sızıntı olarak bildirildi.

İkisinde de kanarya haklıydı. Faz 1'de yazılan cümle Faz 2'de doğrulandı:
*"Bir sızıntı raporunun kendisinin sızıntı olması, bu depoda düşülebilecek
en gülünç tuzaktır."*

---

## 7 · İpucu sistemi

| | |
|---|---:|
| İpucu | **60** (20 × 3) |
| Cevabı içeren ipucu | **0** (dört gizleme biçimine karşı) |
| Merdiven kapsamı | **20 / 20** monoton **ve** yükselen |
| 3. kademe son adımı veriyor | **0** |
| Alanın yanlış bir üyesine götüren ipucu | **0** |

Ve iki kural Faz 2'de eklendi:

**⑧ Düz merdiven de bir kusurdur.** Eski kural yalnızca *azalmayı*
yakalıyordu; kapsam `[4,4,4]` geçiyordu. Bu üç kademeli bir merdiven
değil, üç kez tekrarlanan tek bir ipucudur. Bir bulmaca tam olarak buydu
ve eski kuraldan **geçmişti**.

**Merdiven artık çözüm yolundan TÜRETİLİR.** Kademe 1 → adım 1 · kademe 2
→ adım 1–2 · kademe 3 → adım 1–3, **son adım hariç**. Bir yapı şartını
disipline değil türetime bağlarız.

---

## 8 · Devir ve hata davranışı (talimat § 13)

Faz 1'in bulgusu — *tek bir yanlış cevap okuru ürünün %80'inden dışarıda
bırakıyordu* — geri dönmedi ve dönemez:

| Şart | Ölçüm |
|---|---|
| `crossGateEntryHandoff` | **`false`** — iki kaynakta birden, gerileme fikstürlü |
| Tek bir hatanın yayılma yarıçapı | **≤ 1** (kapı bulmacası hariç) |
| Kapı bulmacasının hata tespiti | **var** — çıktı basılı ifade listesine düşer |
| **Hata tespitinin GÜCÜ** | asgari Hamming mesafesi **15** |
| Teşhis | **slot başına grup işareti** — bağımsız hesapla doğrulanır |
| Kurtarma yolu | kayıtlı · **bozucu olmayan ilerleme** |

⭑ **Asgari Hamming mesafesi 15** şu demektir: on dokuz harflik çıktıda
**yedi**ye kadar eş zamanlı hata bile *tespit edilir* — okur yanlışlıkla
başka bir geçerli kapı sözüne düşemez. Bu ölçülmüştür, iddia edilmemiştir.

Ve teşhis, hatayı **tek bir slota** indirir: her satırın yanındaki grup
işareti alınan harfin Çizelge A grubunu verir (grup başına 5 harf), yani
işaret hatayı **yerelleştirir** ama bulmacayı çözmez. On dokuz bulmacayı
yeniden çözmekle **birini** yeniden çözmek arasındaki fark budur.

Bağımsız çözücülerin ikisi de bu mekanizmayı raporlarının en güçlü kanıtı
olarak kullandı: on dokuz satırın **on dokuzunda da** grup damgası tuttu.

---

## 9 · Sayfa modeli — modelin gerçek içerikle ilk yüzleşmesi

| | Ölçülen | Bildirilen | Durum |
|---|---:|---:|---|
| Kapı I gövdesi | **8,5** sayfa | 34 | ✅ sığıyor |
| İpucu bölümü (kitap ölçeğinde) | **15,2** sayfa | 22 | ✅ sığıyor |
| Çözüm bölümü (kitap ölçeğinde) | **8,4** sayfa | 18 | ✅ sığıyor |
| Araçlar levhası | **0,9** sayfa | (ön madde) | ✅ |

**A8'in doğrulanması budur.** Faz 1, 208 sayfalık modelin arka maddesinin
*fiziksel olarak imkânsız* olduğunu hesapla göstermişti (24 sayfada 300
ipucu + 100 çözüm). 230'a çıkarılan model şimdi **gerçek metinle**
ölçüldü ve arka madde bütçesi **rahat sığıyor**.

### ⚠ İki dürüst uyarı

1. **Kapı gövdesi bütçenin dörtte biri çıktı** (8,5 / 34) ve bu bir
   *başarı değil*, bir **ölçüm sınırıdır**: pilot levhaları gravür değil,
   tipografik şekildir. Gerçek kitapta kapı başına ~20 gravür levha vardır
   ve bir gravür sayfanın yarısını veya tamamını kaplar. 34 sayfalık bütçe
   **levha alanının** bütçesidir ve o alan Faz 5'e kadar ölçülemez.
2. **Çözüm bölümü ölçümü eksik tahmindir**: pilotun `explanation` alanı
   şu an kısadır (bulmaca başına ~30 kelime); basılacak çözüm metni daha
   uzun olacaktır. 18 sayfalık bütçe hâlâ geçerli görünüyor ama bu ölçüm
   Faz 4'te tekrarlanmalıdır.

---

## 10 · Levha durumu (A9)

| Durum | Anlamı | Pilot |
|---|---|---|
| `SCREEN-TESTED` | ekranda çözüldü — **ön eleme** | ✔ **20 / 20** |
| `PAPER-TESTED` | lazer baskıda çözüldü | ⚑ **kurucu** |
| `PHYSICAL-PROOF-VALIDATED` | POD prova kopyada ölçüldü — **kanıt** | ⛔ **0 / 20** |

Ajan üç şeyi **yapmadı ve yapmayacaktır**: provayı sipariş etmek,
yapıldığını iddia etmek, ölçüm uydurmak.

Ajan şunları **yaptı**:

- baskıya hazır 6×9 prova paketi (`02_MANUSCRIPT/PROOF/`, 10 levha)
- prova kontrol listesi (`06_REPORTS/tracked/plate-proof-checklist.md`)
- en yüksek riskli üç ölçütün adlandırılması

⚠ **Ve pilotta ikinci bir ikame daha var:** pilot levhaları **gravür
değil, tipografik şekildir**. Bu paket bulmacaların **mantığını** kâğıtta
test eder; gravürün nokta yayılması altındaki davranışını **etmez**. O
ölçüm Faz 5'e aittir ve bu rapor onu **geçmiş saymaz**.

---

## 11 · Gizlilik ve kanarya (A11)

| | |
|---|---|
| Sır adı | **`ENIGMATICA_CANARY_SALT`** |
| Üretim | `secrets.token_urlsafe(48)` — **384 bit** |
| Üretim tarihi | **13 Ağustos 2026** |
| Tuz parmak izi | `5879fbaf09da12f7` (`sha256[:16]` — geri çevrilemez) |
| CI | GitHub Actions **depo sırrı** · `emredogan-cloud/codex-enigmatica` |
| Güvenli yedek | `~/.config/enigmatica/canary_salt` · `0600` · dizin `0700` · **depo dışında** |
| Döndürme yordamı | `project_config.json § security.canary.rotationProcedure` (6 adım) |
| **Plaintext hiçbir yerde** | terminal · commit · rapor · README · kaynak · CI log · PR ❌ |

### Üç senaryo — iddia değil, ölçüm

Gerçek bir klon üzerinde (75 takip edilen dosya, korumalı katman **yok** —
CI'ın birebir koşulu):

| Senaryo | Beklenen | Ölçülen |
|---|---|---|
| Doğru tuz | KİP B · yeşil | ✅ çıkış 0 |
| **Eksik tuz** | KİP C · **kırmızı** | ✅ çıkış 1 |
| **Yanlış tuz** | parmak izi uyuşmaz · **kırmızı** | ✅ çıkış 1 |
| **Enjekte edilmiş sızıntı** | yakalanır | ✅ çıkış 1 · dosya adıyla bildirdi |

Dördüncü satır en önemlisidir: etiketsiz düz proza içine yazılmış bir
cevap, korumalı katmanın **var olmadığı** bir ortamda, yalnızca tuzlu
künye ile **yakalandı**.

### Public depo taraması

**0 bulgu.** Ve iki gerçek yakalama bu fazda yaşandı (§ 6.5) — kanarya
kendi yazarını iki kez ısırdı.

---

## 12 · İngilizce dönüşüm hazırlığı (talimat § 23)

> ⛔ **DÖNÜŞÜM BAŞLATILMADI.** Talimat § 23 dönüşümü pilotun
> **doğrulanmasına** bağlar; doğrulama A12'ye bağlıdır ve A12 açıktır.

Ölçülen iş listesi (`06_REPORTS/tracked/english-readiness.json`):

| Taşınabilirlik | Bulmaca | Gereken iş |
|---|---:|---|
| `mechanical` | **14** | mekanizma taşınır, **veri yeniden üretilir** |
| `lexical` | **5** | harf grubu yapısı yeniden kurulur, **kısıt yeniden tasarlanır** |
| `phonetic` | **1** | **bulmaca yeniden tasarlanır** |

### ⭑ Ve rahatsız edici olan sonuç: hiçbir bulmaca "çevrilebilir" değil ⭑

Sebep tek bir sayıdır: **Türk alfabesi 29, İngiliz alfabesi 26 harf.**

| | Türkçe | İngilizce |
|---|---:|---:|
| Harf | 29 | 26 |
| İşaret grubu yapısı | 5·5 + 4 | **5·5 + 1** |
| Kaydırma uzayı | 28 | **25** |
| Yansıma ekseni | 29 | **26** |

Grup yapısı değişir → grup koşuluna dayanan **beş** kısıt bulmacası
yeniden tasarlanır. Kaydırma ve yansıma uzayı değişir → **şifreli
dizelerin tamamı** yeniden üretilir. Basılı Sözlük yeniden yazılır → **her
cevap değişir**. Kapı ifadesinin on dokuz harfi **baştan atanır**.

> **K20 bir ihtiyat cümlesi değil, ölçülmüş bir olgudur:** Türkçe başarı,
> İngilizce çözülebilirliğin kanıtı değildir. İngilizce sürüm sekiz
> kapıdan **baştan** geçer.

---

## 13 · Test altyapısı

| Kapı | Yeni? | Ne denetler |
|---|---|---|
| `validate_spec` | | şema · kapsam · **`tested` kazanılmış mı** |
| `validate_structure` | | depo · gömülü değer · **çözüm sızıntısı** |
| `qa_taxonomy` | | mekanizma çeşitliliği · cevap biçimi |
| `qa_dependency` | | DAG döngüsüz · ileri referans yok |
| **`qa_answerspace`** | ⭑ | **alan bağımsız açılır · tam olarak bir kabul** |
| **`qa_handoff`** | ⭑ | **hata tespiti · teşhis · kurtarma · yayılma yarıçapı** |
| **`qa_readerpack`** | ⭑ | **okur bunu çözebilir mi** |
| `qa_solvability` · `qa_uniqueness` · `qa_hints` | | çözülebilirlik sözleşmesi |
| `qa_solution_leak` | | ⭑ kanarya — cevabın **kendisi** |
| `pilot_pages` · `page_budget` | ⭑ | model **gerçek metne** vurulur |
| `english_readiness` | ⭑ | dönüşüm iş listesi |
| **`kill_gate`** | ⭑ | **karar — veri yoksa GEÇMEZ** |

### Kapıların kendi testi: 123 → **154** denetim

Her yeni fikstür Faz 2'de **gerçekten yaşanmış** bir kusuru yeniden kurar.
En önemli ikisi:

- **Öldürme kapısı veri yokken `BLOCKED` verir** — ve **tam veriyle
  `PASS` verir.** İkinci fikstür birincisinden daha önemlidir: *hiç
  geçmemiş bir kapı, geçemiyor da olabilir.*
- **Sekiz okumanın ikisi tablodaysa kırmızı** — § 6.1'in fikstürü.

---

## 14 · ⛔ ÖLDÜRME KAPISI KARARI

```
KARAR: BLOCKED
SEBEP: Harici çözücü oturumları YAPILMADI (0/5).
       Öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz.
BLOKLAYAN: A12
```

### 14.1 · Neden "BLOCKED" ve neden "PASS" değil

Sıfır oturumla **bütün ölçütler teknik olarak "ihlal edilmemiş"
görünür**: hiçbir çözücü başarısız olmadı, hiçbir alternatif cevap
bildirilmedi, hiçbir bulmaca çözülemedi diye işaretlenmedi.

> Bir kapının boş veriyle yeşil yanması, bu projede yapılabilecek en
> pahalı yalandır. Öldürme kapısının **bütün** değeri dürüstlüğünden
> gelir.

Bu yüzden karar dört değil **beş** değerlidir ve `BLOCKED` bir sonuç
değil, bir **boşluktur**.

### 14.2 · Ölçülemeyenler

| Ölçüt | Eşik | Durum |
|---|---:|---|
| Kapı I'i bitiren çözücü | ≥ 4/5 | **ÖLÇÜLMEDİ** |
| Hiç çözülemeyen bulmaca | 0 | **ÖLÇÜLMEDİ** |
| Bulmaca başına bitiren çözücü | ≥ 2 | **ÖLÇÜLMEDİ** |
| 3. kademeye inen çözücü / bulmaca | ≤ 2 | **ÖLÇÜLMEDİ** |
| Medyan tamamlama | ≤ 240 dk | **ÖLÇÜLMEDİ** |
| Onaylanmış alternatif çözüm | 0 | 0 (analizle) · **çözücüyle ölçülmedi** |
| Belirsizlik puanı > 2 | 0 | **0** ✅ (analizle) |

### 14.3 · Hazır olan

- 20 pilot bulmaca · bütün teknik kapılar yeşil
- cevap uzayı **20/20** bağımsız doğrulanmış
- 60 ipucu · hiçbiri cevabı içermiyor
- devir paketi: [`EXTERNAL_SOLVER_PACKAGE.md`](../00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md)
- kayıt şeması · sayısal eşikler · anonimlik kuralı
- prova paketi (A9) · kontrol listesi

---

## 15 · Faz 2 DoD

| | |
|---|---|
| A3 kurucu kararı kaydedildi | ✅ |
| Beş Türkçe harici çözücü **belirlendi** | ✅ |
| Test protokolü işler durumda | ✅ |
| **20 pilot bulmaca Türkçe yazıldı** | ✅ |
| `answerSpace` uygulandı | ✅ **20/20 bağımsız doğrulandı** |
| 20/20 şema geçerli | ✅ |
| İç çözücü denetimleri | ✅ 3 geçiş · ⚠ **kanıt değil** |
| Tekillik (analitik) | ✅ |
| Çözülebilirlik | ✅ |
| İpucu sistemi | ✅ |
| Devir / hata davranışı | ✅ **ölçüldü** (Hamming 15) |
| **Harici çözücü kayıtları gerçek** | ⛔ **KAYIT YOK — sahte üretilmedi** |
| Sahte test kaydı yok | ✅ **mekanik olarak imkânsız** |
| Belirsizlik bulguları çözüldü | ✅ 28/28 |
| Sayfa modeli gerçek içerikle ölçüldü | ✅ |
| Arka madde modeli doğrulandı | ✅ |
| Levha prova hattı hazırlandı | ✅ |
| Fiziksel prova durumu dürüst kaydedildi | ✅ **YAPILMADI** |
| A8 kabul edildi | ✅ |
| A11 kanarya sırrı kuruldu | ✅ **dört senaryoyla kanıtlandı** |
| Çözüm sızıntısı dedektörü geçiyor | ✅ |
| Kanarya CI'da koşuyor | ✅ |
| Public depoda çözüm sızıntısı | ✅ **0** |
| CI yeşil | ✅ |
| Gereksiz açık PR yok | ✅ |
| Faz 2 raporu | ✅ bu belge |
| Yol haritası ilerlemesi güncellendi | ✅ |
| **ÖLDÜRME KAPISI GEÇTİ** | ⛔ **BLOCKED** |

⚠ `.gate` **`phase1`de kaldı**. `phase2` seviyesi 20 *doğrulanmış* bulmaca
ister; `validated` durumu `tested` ister; `tested` beş harici çözücü ister.
Zincir **mekaniktir** ve belgeyle gevşetilemez — bu, kapının çalışmasıdır.

---

## 16 · Faz 3 hazırlığı ve kalan kurucu bağımlılıkları

> ### FAZ 3 BAŞLATILMADI VE BAŞLATILAMAZ.
>
> Yol haritası Faz 3'e girişi **öldürme kapısının GEÇMESİNE** bağlar.
> Karar `BLOCKED`. Yirmi bulmacanın yazılmış olması bir geçiş değildir.

| # | Ne | Kim | Aciliyet |
|---|---|---|---|
| **A12** | **Beş harici çözücü oturumu** | kurucu + 5 insan | ⛔ **ÖLDÜRME KAPISININ TEK BLOKLAYICISI** |
| **A9** | Levha provası — paket hazır | kurucu | YÜKSEK |
| **A2** | Beş kapı teması onayı | kurucu | YÜKSEK |
| **A5** | Kalibre `STYLE.md` onayı | kurucu | ORTA |
| **A7** | Bulmaca başına doğrulama biçimi | kurucu | ORTA (mekaniği K21 ile kuruldu) |
| **A10** | Faz 3'e ikinci öldürme kapısı | kurucu | Faz 3 başlamadan |
| — | 16 künyenin insan gözüyle doğrulanması | kurucu | Faz 3'te KIRMIZI olur |

---

## 17 · Kapatılmayan sınırlar — açıkça yazılıdır

| Sınır | Neden açık |
|---|---|
| **Gravür levhaların baskı davranışı** | Pilot levhaları tipografik şekildir |
| **Sayma yorgunluğu** (4 ↔ 5 işaret) | Aralıklandırma yardım eder; kâğıtta ölçülmedi |
| **6 karakterden kısa cevaplar** | Kanarya eşiği; kısaltmak yanlış pozitif üretir |
| **İç çözücünün insanı temsil etmesi** | **Etmez** — bu raporun ana teması |
| **Kapı gövdesi sayfa ölçümü** | Levha alanı ölçülemedi (34'ün 8,5'i) |
| **Çözüm bölümü sayfa ölçümü** | `explanation` alanı henüz kısa |

> Bir kapının ne **yapmadığını** bilmemek, onu olduğundan güçlü sanmaktır.

---

## 18 · Sonuç

**FAZ 2 · TEKNİK İŞ TAMAMLANDI · ÖLDÜRME KAPISI BLOCKED.**

Yirmi bulmaca var, hepsi çalışıyor, hepsi tekil, hepsi okur paketinde
çözülebilir, hiçbiri cevabını sızdırmıyor. Ölçüm makinesi Faz 1'e göre
dört yeni kapı ve yirmi sekiz yeni fikstür kazandı — ve **kendi
yazarlarını üç kez yakaladı**.

Ama bu fazın sorusu *"yirmi bulmaca yazılabilir mi"* değildi. Soru şuydu:
**bulmaca sistemi gerçek insanlarda çalışıyor mu?**

O soru **hâlâ cevapsızdır** ve cevaplayacak olan ajan değildir.

> ### AJAN DURDU. FAZ 3 BAŞLATILMADI.
> ### BEŞ GERÇEK OTURUM BEKLENİYOR (A12).
