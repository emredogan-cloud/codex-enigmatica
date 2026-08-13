# İÇ ÇÖZÜCÜ PROTOKOLÜ — Solver A / Solver B

> **Bu bir kanıt üretmez. Bir ön eleme üretir.**
>
> Sürüm 1.0 · Faz 1 teslimatı

---

## 1 · Neden var ve neden yetmez

Harici çözücü testi pahalıdır: beş insan, saatler, ve tek kullanımlık.
Bir bulmacayı harici teste **bariz bir kusurla** göndermek o testi israf
eder — çünkü beş kişi de aynı kusura takılır ve o oturumdan tek bir bilgi
çıkar.

İç çözücü bu israfı önler. Yaptığı iş budur ve **başka bir şey değildir**.

> ### ⛔ İç çözücü kaydı öldürme kapısında SAYILMAZ.
>
> `project_config.json § solvability.testStatusRequirements.internalSolverCountsAsEvidence`
> = **false** ve `validate_spec § check_test_status` bunu uygular.
>
> Gerekçe: ajan çözümü zaten bilir. Bildiği bir şeyi "bulmak", bulmak
> değildir. Bu protokolün ürettiği en iyi sonuç bile bir **hipotezdir**.

`testStatus: "internal-only"` bu durumun adıdır ve `validated` sayılmaz.

---

## 2 · İki çözücü, iki bilgi durumu

| Rol | Kim | Ne bilir | Ne yapar |
|---|---|---|---|
| **Solver A** | Ana ajan | Tasarım niyetini biliyor | Çözüm yolunun **yürüdüğünü** doğrular |
| **Solver B** | Bağımsız alt-ajan | ⭑ Çözümü **görmez** ⭑ | Bulmacayı **sıfırdan** çözmeye çalışır |

Solver B'nin bilgi kısıtı bu protokolün **tek değerli parçasıdır** ve
mekanik olarak korunur: alt-ajana yalnızca public katman ve bulmaca metni
verilir. Korumalı katmana erişimi yoktur.

### Kural

Solver B **ilk denemesinde** çözüm anahtarını kullanamaz. Kullanırsa
protokol çalışmamıştır ve kayıt geçersizdir.

---

## 3 · Sonuç tablosu

| A | B | Yorum | Eylem |
|---|---|---|---|
| ✔ | ✔ **aynı yoldan** | Ön eleme geçildi | Harici teste gönder |
| ✔ | ✔ **farklı yoldan** | ⚠ **Muhtemel belirsizlik** | İki yol da geçerliyse belirsizlik puanı **≥3** → yeniden yaz |
| ✔ | ✘ | Talimat veya ipucu eksik | **İncele** — kusur bulmacadadır |
| ✘ | — | Çözüm yolu yürümüyor | ⛔ Bloklayıcı — bulmaca kırık |
| ✔ | ✔ **ama farklı cevap** | ⛔ **Alternatif çözüm** | `qa_uniqueness` kırmızı; yeniden yaz |

> **"İkisi de çözdü ama farklı yoldan" bir başarı değildir.**
> Bu kitapta iki geçerli okuma, bir geçerli okuma eksikliğidir.

---

## 4 · Faz 1'de ne yapıldı

Faz 1'de **hiçbir bulmaca yazılmadı**, dolayısıyla çözülecek bir bulmaca
da yoktu. Protokol bu fazda **tasarıma** uygulandı:

| Saldırı | Hedef | Sonuç |
|---|---|---|
| Mimari kırmızı takım | Doğrulayıcılar, gizlilik katmanı, şema | **18 bulgu** — 5'i kritik |
| Tasarım kırmızı takım | 17 aile, pilot dizilim, bağımlılık yapısı, ipucu kuralı | **18 bulgu** — 6'sı yapısal |

Her ikisi de **bağımsız alt-ajanlarla** yürütüldü ve bulguların hiçbiri
kabul edilmeden önce yumuşatılmadı. Kabul edilen, ertelenen ve reddedilen
bulguların tam listesi: [`RED_TEAM_CHECKLIST.md`](RED_TEAM_CHECKLIST.md).

> Bu, bir çözücü testinin yerine geçmez. Bir bulmaca sisteminin
> çözülebilirliğini yalnızca **insanlar** kanıtlar.

---

## 5 · Faz 2'de nasıl koşacak

Her bulmaca için, harici teste gönderilmeden **önce**:

1. Solver A çözüm yolunu adım adım yürür; her adımın kitap içi dayanağını
   gösterir (`usesOnlyBookKnowledge` + `sourceInBook`)
2. Solver B'ye **yalnızca** bulmaca metni ve ön madde verilir
3. Solver B en fazla 3 kademede ipucu isteyebilir; her istek kaydedilir
4. Solver B'nin yolu Solver A'nınkiyle **karşılaştırılır**
5. Ayrışma varsa belirsizlik puanı yeniden hesaplanır
6. `redTeamNotes`'a "zeki bir okur bunu nasıl kırar" bulguları yazılır

Kayıt `01_SOURCE/solutions/*.json § solverTests[]` içine
`solverClass: "internal-a"` / `"internal-b"` ile düşer ve
`qa_uniqueness` bu kayıtlardaki `alternativeOffered` alanını **kırmızı**
yakar.

---

## 6 · Bu protokolün kendi kusuru

Solver B bir dil modelidir ve bir insan okurun **iki şeyini** taşımaz:

- **Sabırsızlık** — bir insan sıkılır ve bırakır; model bırakmaz
- **Bedel** — bir insan otuz dolar ödemiştir; model ödemedi

Yani Solver B *çözülebilirliği* test eder, *terk oranını* test **etmez**.
Terk oranı bu kitabın asıl ticari riskidir ve yalnızca
[`SOLVER_TEST_PROTOCOL.md`](SOLVER_TEST_PROTOCOL.md) ile ölçülür.

Bu kusurun yazılı olması, protokolün olduğundan güçlü sanılmasını önler.
