# FAZ 1 RAPORU — bulmaca mimarisi, çözülebilirlik çerçevesi, gizlilik katmanı

> **Codex Enigmatica** · 13 Ağustos 2026 · dal `faz/1-mimari` · kapı `phase1`
>
> ⚠ Bu fazda **tek bir bulmaca yazılmadı**. Yazılan şey, yüz bulmacanın
> çözülebilir olduğunu **ispatlayacak makinedir**.

---

## 0 · Tek bakışta

| | |
|---|---:|
| Aday bulmaca | **151** (hedef ≥130) |
| Kapı başına aday | 31 · 30 · 29 · 29 · 29 (hedef ≥26) |
| Mekanizma ailesi | **17** tanımlı, **17** kullanımda |
| Pilot kohort (Kapı I) | **20** slotlanmış |
| Bağımlılık grafiği | **döngüsüz**, ileri referans **yok** |
| Sayfa modeli | **230** (hedef 230 ± %6) |
| Levha modeli | **112** (hedef 110 ± %10) |
| Künye | **16**, hepsi kamusal alan |
| Kalite kapısı | **11 betik** |
| Kapıların kendi testi | **123 denetim** |
| Kırmızı takım bulgusu | **36** — 30 kapatıldı, 6 kurucuya |
| **Yazılmış bulmaca** | **0** — bu faz öyle tasarlandı |
| **Harici çözücü testi** | ⛔ **YAPILMADI — HARİCİ DOĞRULAMA BEKLİYOR** |

---

## 1 · ⚠ Kapsam notu: yol haritası ile talimat arasındaki fark

Faz 1 talimatı "20 bulmacalık pilot + 5 harici çözücü" istiyordu.
**Uygulama yol haritası** — talimatın kendisinin *yürütme için
otoritatif* ilan ettiği belge — bunu **Faz 2'ye** koyar ve Faz 1 için
açıkça *"bu fazda tek bir bulmaca yazılmaz"* der.

Bu rapor yol haritasına uydu. Gerekçe üç maddedir:

1. **Talimat kendi içinde de bunu söylüyor** (§ 23: *"Faz 2'yi başlatma"*).
   Yirmi bulmaca yazmak, tanımı gereği Faz 2'yi başlatmaktır.
2. **Beş çözücü henüz yok** (A3). Test edilemeyecek yirmi bulmaca yazmak,
   öldürme kapısını ölçüm olmadan geçmiş saymaya davettir.
3. Pilot **tasarımı** yine de teslim edildi: Kapı I'in 20 slotu, aileleri,
   bağımlılık kenarları, süre modeli ve levha ihtiyacı **belirlenmiş**
   durumda. Faz 2 boş sayfayla değil, **doğrulanmış bir iskeletle** başlar.

Talimatın istediği her mekanizma — şema, taksonomi, çözülebilirlik kapısı,
tekillik kapısı, ipucu kapısı, iç çözücü, kırmızı takım, bağımlılık grafiği,
gizlilik mimarisi, sızıntı dedektörü, test protokolü, selftest — **kuruldu
ve kusurlu fikstürlerle ısırdığı kanıtlandı**.

---

## 2 · Bulmaca envanteri

### 2.1 · Kapı dağılımı

| Kapı | Zorluk | Aday | Hedef | Slotlanmış |
|---|---|---:|---:|---:|
| I · The Threshold | ★ | 31 | 20 | **20** (pilot) |
| II · The Menagerie | ★★ | 30 | 20 | 1 |
| III · The Calendar | ★★ | 29 | 20 | 1 |
| IV · The Labyrinth | ★★★ | 29 | 20 | 1 |
| V · The Mirror | ★★★ | 29 | 20 | 1 |
| — · The Last Question | ★★★ | 3 | 1 | — |

Yedek havuz **51 aday**: her kapı hedefinin %45–55 üstünde. Yol haritası
%30 fazlalık istiyordu.

### 2.2 · Mekanizma aileleri

On yedi aile, dört eksende tanımlı: tanım · hedef zorluk · **tekillik
ispatı** · kurgu örnek.

| Grup | Aileler |
|---|---|
| Gözlem | plate-observation |
| Şifre | plate-embedded-cipher · substitution · transposition · polyalphabetic · script-decoding |
| Mantık | constraint-logic · classification · numeral-system · cyclic-calendar |
| Uzam | path-graph · layered-chain |
| Öz-göndergesel | back-reference · book-structure · narrative-embedded |
| Kapanış | gate-synthesis · meta-synthesis |

**Çeşitlilik ölçümü:** hiçbir kapıda tek aile payı %35'i aşmıyor
(en yüksek: Kapı I'de plate-observation %25); her kapı ≥4 aile taşıyor
(ölçülen 6–7); kitap genelinde 17 ayrı mekanizma.

---

## 3 · Çözülebilirlik ölçümleri

Bu fazda **çözülebilirlik ölçülmedi** — ölçülecek bir bulmaca yoktu.
Ölçülen şey, ölçüm makinesinin **ısırdığıdır**:

| Kapı | Kusurlu fikstür | Yakalandı |
|---|---:|---:|
| `validate_spec` — şema, kapsam, test durumu | 38 | 38 |
| `validate_structure` — depo ve sızıntı | 18 | 18 |
| `qa_solution_leak` — kanarya | 6 | 6 |
| `qa_solvability` · `qa_uniqueness` · `qa_hints` | 26 | 26 |
| Muafiyet ve korumalı dizin denetimleri | 35 | 35 |
| **Toplam** | **123** | **123** |

### Pilot süre modeli

| | |
|---|---:|
| 20 bulmacanın toplam süresi | 153 dk |
| Oturum yükü (ön madde, ters basılı ipuçlar, aktarım) | 45 dk |
| **Modellenen oturum** | **198 dk** |
| Öldürme kapısı tavanı | 240 dk |
| Pay | **%17,5** |

⚠ Bu bir **model**dir, ölçüm değil. Değeri, Faz 2'de gerçek süreyle
karşılaştırılabilir olmasındadır.

---

## 4 · Belirsizlik bulguları

Bu fazda hiçbir bulmaca metni olmadığı için **ölçülmüş** belirsizlik puanı
yoktur. Bulunan şey daha temeldir: **ispat yönteminin kendisi kusurluydu.**

Bağımsız bir saldırı, on yedi ailenin `validationMethod` alanını denetledi:

| Yargı | Aile |
|---|---:|
| Gerçek mekanik ispat | 2 |
| Yanlış önermeyi ispatlıyor | 5 |
| **Yanlışlanamaz** | 4 |
| Hedefin yeniden ifadesi | 3 |
| Sağlam ama eksik | 3 |

Dokuzunda tekrar eden kusur aynı: **sayım alanını, cevabı zaten bilen
yazar tanımlıyor.** Yazarın seçtiği bir alan üzerinde yapılan ispat bir
totolojidir.

**En sert örnek — `classification`.** Altı öğelik bir küme 6 farklı
"biri ayrı" bölünmesi kabul eder. Her öğe *m* ikili nitelik taşırsa,
rastgele bir niteliğin tam olarak birini ayırma olasılığı 0,1875'tir;
gerçek bir folklor motifi rahatlıkla otuz kullanışlı nitelik taşır →
beklenen **sahte 5–1 ayrımı ~5,6**. Kültürel bir nesnenin nitelik ekseni
listelenemez, dolayısıyla bu ailenin ispatı **yanlışlanamaz**.

**Kabul edilen düzeltme (Faz 2'nin ilk teslimatı):** her bulmaca makine
okunur bir `answerSpace` dosyası taşır — okurun, kitabın ona
öğrettikleriyle ulaşabileceği bütün dizeler. `qa_uniqueness` sayım
alanının **proza değil dosya** olmasını ister.
`classification` ailesi yalnızca **basılı nitelik matrisiyle**
kullanılabilir hâle getirildi.

---

## 5 · İç çözücü bulguları

Solver A (ana ajan) ve Solver B (bağımsız alt-ajan) protokolü kuruldu
([`INTERNAL_SOLVER_PROTOCOL.md`](../00_CONTEXT/INTERNAL_SOLVER_PROTOCOL.md)).

Bu fazda çözülecek bulmaca olmadığı için protokol **tasarıma** uygulandı:
iki bağımsız kırmızı takım, biri mimariye biri tasarıma saldırdı.

> ⛔ **İç çözücü kaydı öldürme kapısında SAYILMAZ** ve bu artık bir
> politika değil bir mekanizmadır: `internalSolverCountsAsEvidence: false`
> ve `validate_spec` bunu uygular.

---

## 6 · Kırmızı takım — 36 bulgu

Tam defter:
[`RED_TEAM_CHECKLIST.md § 3`](../00_CONTEXT/RED_TEAM_CHECKLIST.md).
Buradaki özet en ağır beşidir.

### 6.1 · Öldürme kapısı mekanik olarak bir METİN ALANIYDI

140 kaydın `status` alanını elle `written` yapmak, projeyi `phase1`'den
`release`'e yürütüyordu — `testStatus` "untested", çözücü sayısı 0,
alternatif analizi yapılmamışken. Eski selftest bu manevrayı **geçmesi
gereken bir test** olarak yapıyordu.

**Kapatıldı:** `tested` beş şartla + kurucu onayı kilidiyle kazanılır.

### 6.2 · Sızıntı kapısı `git` aksadığında AÇIK BAŞARISIZ oluyordu

`git ls-files` çalışmazsa liste boş dönüyor, bütün sızıntı denetimleri boş
koşup **yeşil yanıyordu** — depoda çözüm dosyaları dururken bile.

**Kapatıldı:** `.git` varken boş liste bir hatadır.

### 6.3 · Şemayı hiçbir kod okumuyordu

`puzzle.schema.json` 355 satır boyunca üç gizlilik sınıfı ve
`additionalProperties: false` tanımlıyordu; yalnızca "var mı" diye
denetleniyordu.

**Kapatıldı:** şema uygulanıyor; public indeks bir **izin listesidir**.

### 6.4 · Kapı devri bağı okuru ürünün %80'inden dışarıda bırakıyordu

Bir kapı bulmacasını yanlış çözen okur, tek bir hatadan ve hiçbir teşhis
olmadan sonraki bütün kapılara kapanıyordu. Ve 18/19 çözen okur hangi
ikisinin yanlış olduğunu bilemediği için **ipucu merdiveni de işe
yaramıyordu** — yani bağımlılık grafiği sözleşmenin üçüncü sözünü sessizce
iptal ediyordu.

**Kapatıldı:** `crossGateEntryHandoff: false`. Devir anlatısal.

### 6.5 · Arka madde 24 sayfada fiziksel olarak imkânsızdı

300 ipucu + 100 çözüm ≈ **44 sayfa**. Bu bir dizgi meselesi değil bir
**çözülebilirlik** meselesidir: taşma dizgiyi kaydırır ve Kapı V'in sayfa
numarasına dayanan sekiz bulmacasını, takvimin bittiği yerde kırar.

**Kapatıldı:** sayfa hedefi 230; arka madde artık **türetiliyor**.

---

## 7 · Gizlilik bulguları

### Beş hatlı koruma

| Hat | Mekanizma | Faz 1'de ne oldu |
|---|---|---|
| 1 | `.gitignore` | Yasak listesinden **izin listesine** çevrildi |
| 2 | `PROTECTED_DIRS` | `01_SOURCE/design/` eklendi; muafiyet **tam yol** oldu |
| 3 | İçerik taraması | Bütün metin dosyalarına genişledi; **Türkçe** eklendi |
| 4 | Şema | **Uygulanmaya başlandı** — izin listesi |
| **5** | ⭑ **Kanarya** ⭑ | **Yeni** — cevabın kendisini arar |

### Sızıntı dedektörü kanıtlandı

Talimat § 12'nin istediği kasıtlı sızıntı testi kuruldu ve **koşuyor**.
Her fikstür gerçek bir git deposu kurar, sızıntıyı commit eder ve kapının
**kırmızı yandığını** doğrular:

- çözüm alanı taşıyan `.json` · **büyük harfli** `.JSON`
- taranmayan uzantılar: `.yml` · `.py` · `.svg` · `.tex` · **uzantısız**
- **Türkçe** etiketli cevap
- korumalı dizinde **alt dizin README'si** (`git add -f` ile)
- manuscript alt dizin README'si · bulmaca başlığı · sır dizesi
- gömülü kurucu değeri · config ↔ betik ayrışması
- **takip listesi boşken kapının kapanması**

Ve kanarya için: **etiketsiz proza içindeki cevap** · **dosya adındaki
cevap** · **commit mesajındaki cevap** · kanaryanın koşmaması.

### Kapatılmayan sınır — açıkça yazıldı

`validate_structure` alan **adı** ve **etiket** arar. Kanarya cevabın
kendisini arar, ama yalnızca korumalı katman yereldeyken veya CI'da tuz
kuruluyken (**A11**). Etiketsiz düz proza içinde, tuz kurulu değilken
yazılmış bir cevap yakalanmaz.

> Bir kapının ne **yapmadığını** bilmemek, onu olduğundan güçlü sanmaktır.

### Public depoda çözüm taraması

**0 bulgu.** 151 aday kaydının hiçbiri çözüm, ipucu, başlık, proza veya
tasarım niyeti taşımıyor.

---

## 8 · Test altyapısı ve CI

| İş | Ne koşar |
|---|---|
| `gate` | `.gate` seviyesini okur ve doğrular |
| `data` | `validate_spec` · `validate_research` · `qa_taxonomy` |
| `structure` | `validate_structure` (**çözüm sızıntısı dâhil**) |
| `gates-selftest` | **123 denetim** — kapılar ısırıyor mu |
| `text` | `qa_solvability` · `qa_uniqueness` · `qa_hints` · `qa_dependency` |
| **`canary`** | ⭑ `qa_solution_leak` — tam geçmişle, commit mesajları dâhil |
| `production-model` | `page_budget` |

⚠ CI artefakt yüklemesi Faz 1'de **daraltıldı**: yalnızca
`06_REPORTS/tracked/`. Doğrulayıcı raporları yapıları gereği cevap
adaylarına yaklaşır ve bir artefakt, depoya bakmayan birinin bile
indirebileceği bir dosyadır.

---

## 9 · Tester hazırlığı

| | |
|---|---|
| Protokol | ✅ [`SOLVER_TEST_PROTOCOL.md`](../00_CONTEXT/SOLVER_TEST_PROTOCOL.md) |
| Kayıt şeması | ✅ `solverTests[]` — anonim kimlik `pattern` ile zorunlu |
| Ölçüm aracı | ✅ zaman damgası kuralı · `hintsUsedByLevel` · `abandonReason` |
| Eşikler | ✅ sayısal, config'de, üçü Faz 1'de eklendi |
| Sahte kayıt koruması | ✅ **mekanik** — kurucu onayı olmadan `tested` verilemez |
| **Beş çözücü** | ⛔ **YOK — A3 · FAZ 2'NİN SERT BLOKLAYICISI** |

> ### FOUNDER / EXTERNAL TESTER DEPENDENCY
> Beş harici çözücü belirlenmemiştir. Hiçbir test yapılmamıştır ve
> **hiçbir test kaydı üretilmemiştir**. Faz 2 bu karar olmadan başlayamaz.

---

## 10 · Riskler

| Risk | Durum | Azaltma |
|---|---|---|
| Dokuz ailenin tekillik ispatı yetersiz | **AÇIK** | `answerSpace` — Faz 2'nin ilk teslimatı |
| `classification` ailesi analizle tekilleştirilemez | **Azaltıldı** | Yalnızca basılı nitelik matrisiyle kullanılır |
| Levha bulmacaları ekranda test edilirse test edilmemiş sayılır | **AÇIK** | **A9** — kurucu kararı |
| Kapı I'in 19-girdili kapı bulmacası tek hatada çöküyor | **AÇIK** | **A7** — bulmaca başına doğrulama |
| Kapı III'ün %79'u baskı çözünürlüğüne bağlı | **AÇIK** | Aile başına POD ön ölçümü (Faz 3) |
| Metne bağlı 19 bulmaca Line Editor'la sessizce kırılır | **Kapatıldı** | `boundToTextHash` + `qa_taxonomy § ⑨` |
| Kanarya CI'da koşmuyor | **AÇIK** | **A11** — CI sırrı |
| En sert test en güvenli bulmacalara uygulanıyor | **AÇIK** | **A10** — Faz 3'e ikinci kapı |

---

## 11 · Çözülmemiş kurucu bağımlılıkları

| # | Ne | Ne zaman |
|---|---|---|
| **A3** | **Beş harici çözücü** | **Faz 2 SERT BLOKLAYICISI** |
| **A7** | Bulmaca başına doğrulama | Faz 2 başlamadan |
| **A8** | Sayfa hedefi 230 onayı | Faz 2 başlamadan |
| **A9** | Pilot levhalarının POD provası | Faz 2 başlamadan |
| **A11** | `ENIGMATICA_CANARY_SALT` CI sırrı | Faz 2 başlamadan |
| A2 | Beş kapı teması onayı | Faz 2 başlamadan |
| A5 | Kalibre `STYLE.md` onayı | Faz 2 |
| A10 | Faz 3'e ikinci öldürme kapısı | Faz 3 başlamadan |
| A4 · A6 | Doğrulama sayfası · yazar biyografisi | Faz 5 |

Ayrıca **16 künyenin 16'sı** hâlâ `asserted` — bir bulmaca yazılmadan önce
insan gözüyle doğrulanmaları gerekir.

---

## 12 · Faz 1 DoD

| | |
|---|---|
| Bulmaca şeması iki katmanlı ve **uygulanıyor** | ✅ |
| Bulmaca taksonomisi (17 aile, dört eksen) | ✅ |
| ≥130 aday · her kapı ≥26 | ✅ 151 |
| Pilot kohort tasarımı (20 slot) | ✅ |
| DAG döngüsüz · ileri referans yok | ✅ |
| İç çözücü mimarisi | ✅ |
| Belirsizlik denetimi | ✅ |
| Çözüm doğrulama kapısı | ✅ (kayıt bekliyor) |
| İpucu sistemi kapısı | ✅ (kayıt bekliyor) |
| Harici tester protokolü | ✅ |
| Gizlilik mimarisi (**beş hat**) | ✅ |
| Çözüm sızıntısı dedektörü **kanıtlanmış** | ✅ 123 denetim |
| Public katmanda çözüm sızıntısı | ✅ **0** |
| Sayfa modeli hedefte | ✅ 230 / 230 ± %6 |
| CI yeşil | ✅ |
| Faz 1 raporu | ✅ bu belge |
| **20 bulmaca yazıldı** | ⛔ **YAZILMADI** — Faz 2 kapsamı (§ 1) |
| **5 harici çözücü testi** | ⛔ **EXTERNAL VALIDATION PENDING** |

---

## 13 · Faz 2 hazırlığı

**Hazır olan:** şema · taksonomi · pilot iskeleti · bağımlılık modeli ·
üç çözülebilirlik kapısı · kanarya · test protokolü · kayıt şeması ·
sayfa ve levha modeli · künye altyapısı.

**Hazır olmayan:** beş çözücü (A3) · `answerSpace` üreticisi ·
pilot levhaları · CI kanarya sırrı (A11).

> ### FAZ 2 BAŞLATILMADI.
>
> Faz 2 bir **öldürme kapısıdır** ve A3 olmadan başlayamaz. Beş çözücü
> belirlenmeden yazılan yirmi bulmaca, test edilemeyecek yirmi bulmacadır.
>
> **AJAN DURDU. KURUCU ONAYI BEKLENİYOR.**
