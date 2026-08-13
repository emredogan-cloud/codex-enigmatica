# HARİCİ ÇÖZÜCÜ TEST PROTOKOLÜ

> Faz 2'nin **öldürme kapısı** bu protokolle ölçülür.
>
> Sürüm 1.0 · Faz 1 teslimatı · Faz 2'de **uygulanır**

---

## 0 · ⛔ DURUM: HARİCİ DOĞRULAMA BEKLİYOR

> ### Bu protokol HAZIRDIR. Test YAPILMAMIŞTIR.
>
> `project_config.json § founder.externalSolvers.founderConfirmed` = **false**
>
> Beş harici çözücü **belirlenmemiştir** (`DECISIONS § A3`).
> Bu, Faz 2'nin **sert bloklayıcısıdır**.

**Sahte test kaydı üretilmez.** Ne isim, ne süre, ne sonuç.
`validate_spec § check_test_status` bunu mekanik olarak imkânsız kılar:
kurucu onayı yokken hiçbir kayıt `testStatus: "tested"` alamaz.

Ajan bu testi **yapamaz**. Çözümü zaten bilir; "çözülebilir" yargısı bir
kanıt değil, bir yanılsamadır. İç çözücü protokolü ayrıdır ve **kanıt
sayılmaz**: [`INTERNAL_SOLVER_PROTOCOL.md`](INTERNAL_SOLVER_PROTOCOL.md).

---

## 1 · Çözücü kim olmalı

| Kural | Değer | Neden |
|---|---|---|
| Kapı I için sayı | **5** | Öldürme kapısının istatistiksel tabanı |
| Diğer kapılar | **≥ 2** | Maliyet/fayda |
| Bağımsızlık | **mutlak** | Birbirine ipucu veren iki çözücü **bir** çözücüdür |
| Kimlik | `solver-01` … `solver-05` | Şema `pattern` ile zorlar; ad depoya **girmez** |
| **Tür çeşitliliği** | **≥ 2 kişi bu türü ilk kez alıyor** | ⚠ aşağı bakınız |

### ⚠ Tür çeşitliliği neden bir kural

Beş escape-room emektarı, kurucunun başarmasını isteyen beş kişidir ve
perakende okurun kitabı **iade ettiği** yerde ısrarla devam ederler.
İade eden okur hiçbir veri satırı üretmez — yani en önemli başarısızlık
sinyali ölçüm dışında kalır.

En az iki çözücü bu rafı **ilk kez** alan biri olmalıdır.

---

## 2 · Çözücü ne görür

| Görür | Görmez |
|---|---|
| Ön madde: çerçeve anlatı, **sözleşme sayfası**, araçlar levhası, ısınma | Çözümler |
| Kapı I'in 20 bulmacası, kitaptaki sırayla | Çözüm yolları |
| Üç kademeli ipuçları — **arka maddede, ters basılı** | Alternatif çözüm analizi |
| Cevap biçimi kuralı (sözleşme sayfasında basılı) | Tasarım kayıtları |
| **POD prova baskı** — ⚠ aşağı bakınız | Diğer çözücülerin kayıtları |

### ⚠ Levha koşulu — Faz 1 kırmızı takım bulgusu

> ### Bir bulmaca, YAYIMLANACAĞI NESNEDEN BAŞKA bir şey üzerinde test edilemez.

Pilot kohortun 20 bulmacasından **9'u levha taşır** ve ikisinde veri
**gravürün içindedir**. Ekranda kusursuz görünen bir gravür, krem kâğıtta
300 dpi'de nokta yayılmasıyla detay kaybeder. Ekranda çözülen bir bulmaca
"geçti" diye kaydedilirse, öldürme kapısı tam olarak önlemesi gereken şeyi
**onaylamış** olur.

İki seçenek vardır ve üçüncüsü yoktur:

| Seçenek | Sonuç |
|---|---|
| **A** — pilot levhalar + araçlar levhası POD provasında basılır | Kapı mekaniği **kapsıyor** |
| **B** — pilot yalnızca levhasız 11 bulmacaya indirilir | Kapı mekaniği **kapsamıyor** ve rapor bunu **açıkça yazar** |

Kapsamadığı bir şeyi kapsıyormuş gibi raporlayan bir öldürme kapısı,
olmayan bir kapıdan daha tehlikelidir.

---

## 3 · Ne kaydedilir

Ham kayıtlar `06_REPORTS/solver/` altındadır ve **depoya girmez**
(`PROTECTED_DIRS`). Depoda yalnızca anonim özet durur.

### Bulmaca başına

| Alan | Tip | Not |
|---|---|---|
| `solver` | `solver-\d{2}` | Şema zorunlu kılar |
| `solverClass` | `external` | ⭑ `internal-*` öldürme kapısında **sayılmaz** |
| `startedAt` / `finishedAt` | zaman damgası | ⚠ **öz-bildirim değil** |
| `minutesToSolve` | tamsayı | damgalardan **türetilir** |
| `result` | `solved` · `solved-with-hints` · `unsolved` | |
| `hintsUsedByLevel` | `[0/1, 0/1, 0/1]` | Hangi kademelere bakıldı |
| `alternativeOffered` | dize | ⭑ **Çözücü başka bir cevap verdiyse buraya** |
| `perceivedAmbiguity` | 1–5 | Çözücünün kanaati |
| `answerConfidence` | 1–5 | "Doğru olduğundan ne kadar eminsin" |
| `notes` | serbest | Nerede takıldı, ne denedi |

### Oturum başına

| Alan | Not |
|---|---|
| `gateCompleted` | Kapı bulmacası çözüldü mü |
| `failurePoint` | Bıraktıysa hangi slotta |
| `abandonReason` | Sıkıldı · takıldı · zaman · ilgi kaybı |
| `difficultyRating` | 1–5 |
| `sessionCount` | Kaç oturumda |
| `wouldContinue` | Kapı II'yi okumak ister mi |

### ⚠ Ölçüm aracı

Süre **öz-bildirim değildir**. Çözücü her bulmacanın başında ve sonunda
damga atar; üç akşama yayılmış bir "sanırım dört saat" ölçüm değildir.
`abandonReason` alanı da zorunludur: *sıkılarak* bırakmak ile *takılarak*
bırakmak iki ayrı kusurdur ve iki ayrı düzeltme ister.

---

## 4 · Öldürme kapısı eşikleri

`project_config.json § killGate` içinde **sayısaldır**. Yoruma yer yoktur.

| Ölçüt | Eşik |
|---|---|
| Kapı I'i **bitiren** çözücü | **≥ 4 / 5** |
| Hiçbir çözücünün çözemediği bulmaca | **0** |
| **Bulmaca başına bitiren çözücü** | **≥ 2** |
| **3. kademe ipucuna ihtiyaç duyan çözücü / bulmaca** | **≤ 2** |
| Onaylanmış alternatif çözüm | **0** |
| Medyan tamamlama süresi | **≤ 240 dk** |
| Belirsizlik puanı > 2 olan bulmaca | **0** |

### ⚠ Faz 1'de eklenen iki eşik ve bir tanım

**`minSolversPerPuzzle: 2`.** Eski ölçüt yalnızca *hiç kimsenin çözemediği*
bulmacayı yakalıyordu. Beş çözücüden **yalnızca birinin** çözdüğü bir
bulmaca geçiyordu — yani okurların %80'inin takıldığı bir bulmaca "geçer"
sayılıyordu. Bir yıldızı yazan tam olarak o okurdur.

**`maxSolversNeedingLevel3Hint: 2`.** İpucu tüketimi ölçülmeden "zorluk ★"
bir iddiadır. Beş çözücünün beşinin 3. kademeye indiği bir kapı bütün
sayısal eşikleri geçer ve yine de çok zordur. İpucu merdiveni bir emniyet
ağıdır; **ana yol** olursa zorluk eğrisi kırıktır.

**`medianDefinition: dnf-counts-as-cap`.** Bitiremeyen çözücünün süresi
tanımsızdır ve tanımsız bir değer medyanı istenen yöne çeker: beş kişinin
medyanı ile dört bitirenin medyanı **farklı sayılardır**. Kural:
bitiremeyen çözücü tavan süreyi almış sayılır. Bir DNF medyanı
**iyileştiremez**.

---

## 5 · Karar tablosu

| Sonuç | Karar |
|---|---|
| 4–5 çözücü bitirdi, 0 alternatif çözüm | ✅ **DEVAM** |
| 4–5 bitirdi ama alternatif çözüm var | ⚠ İlgili bulmacalar yeniden yazılır, **test tekrarlanır** |
| Tam 3 bitirdi | ⚠ **Zorluk eğrisi bozuk.** Kapı I yeniden tasarlanır, test tekrarlanır |
| ≤ 2 bitirdi | ⛔ **SERT DURDURMA** — kurucu kararı gerekir |

> Bu fazın sonucu **güzelleştirilmez**. Öldürme kapısının bütün değeri
> dürüstlüğünden gelir. 3/5 sonucu "neredeyse 4" **değildir**.

---

## 6 · Bir çözücü takılırsa

> **Suç çözücüde değil, bulmacadadır.**

Takılma bir tasarım kusurudur ve şu sırayla incelenir:

1. Talimat iki anlama mı geliyor → `qa_solvability` belirsizlik puanı
2. Bir ipucu eksik mi → çözüm yolunun adımı kitapta gösterilebiliyor mu
3. Gerekli bilgi kitapta mı → `usesOnlyBookKnowledge`
4. Levha baskıda okunuyor mu → POD ölçümü
5. Cevap biçimi belli mi → `answerFormat` + normalizasyon kuralı

Beşi de temizse ve çözücü yine takılıyorsa, bulmaca **kapının zorluk
bandının dışındadır** ve yer değiştirir.

---

## 7 · Çözücü mahremiyeti

Harici çözücülerin adları **hiçbir koşulda** depoya girmez. Ne commit
mesajında, ne rapor dosyasında, ne dosya adında. Eşleştirme tablosu
kurucudadır ve depoda **yoktur**.

Kayıtlar yalnızca anonim kimlik, süre, ipucu tüketimi ve sonuç taşır.

---

## 8 · Faz 2'ye devir listesi

- [ ] **A3 kapandı** — beş çözücü belirlendi (kurucu)
- [ ] `founder.externalSolvers.founderConfirmed` → `true`
- [ ] En az ikisi bu türü ilk kez alan kişi
- [ ] Levha koşulu için A veya B seçildi (kurucu)
- [ ] Zaman damgası aracı çözücülere verildi
- [ ] `06_REPORTS/solver/` yerelde hazır ve **takip edilmiyor**
