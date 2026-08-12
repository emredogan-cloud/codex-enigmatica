# ÇÖZÜLEBİLİRLİK STANDARDI

> Bu kitabın tanımlayıcı teknik problemi budur ve bu belge onu bir
> mekanizmaya bağlar.
>
> Sürüm 1.0 · Faz 1'de onaylanır · Değişiklik kurucu kararı gerektirir

---

## 1 · Sözleşme — okura verilen üç söz

Kitabın **sözleşme sayfasında** okura üç şey açıkça vaat edilir. Bu üç
cümle pazarlama değil, **üretim kısıtıdır**:

> 1. **Her bulmacanın tek bir cevabı vardır.**
> 2. **Hiçbiri kitabın dışındaki bilgiyi gerektirmez.**
> 3. **İpucu almak kaybetmek değildir.**

Aşağıdaki her kural bu üç cümleden birini korur.

---

## 2 · "Çözülebilir" ne demek — ölçülebilir tanım

Bir bulmaca ancak şu beş şart sağlandığında `validated` olur:

| # | Şart | Denetleyen |
|---|---|---|
| 1 | **Çözüm yolu adım adım kayıtlı** | `qa_solvability` |
| 2 | Her adım **yalnızca kitap içi** bilgiyle yürüyor | `qa_solvability` |
| 3 | **Alternatif çözüm analizi yapılmış**, onaylanmış alternatif **yok** | `qa_uniqueness` |
| 4 | **Belirsizlik puanı ≤ 2** | `qa_solvability` |
| 5 | **≥2 harici çözücü** denedi (Kapı I için **5**) | `qa_solvability` |

> **Bir bulmaca "zekice göründüğü" için kabul EDİLEMEZ.**
> Deterministik olarak çözülemeyen bir bulmaca bir **üretim hatasıdır**.

---

## 3 · Belirsizlik puanı

| Puan | Anlam | Kabul |
|---|---|---|
| **1** | Tek okuma mümkün | ✅ |
| **2** | İkinci bir okuma zorlanarak mümkün ama metin onu dışlıyor | ✅ |
| **3** | İki okuma da savunulabilir | ⛔ |
| **4–5** | Metin çözümü belirlemiyor | ⛔ |

Puan **çözücü testinden** türer, yazarın kanaatinden değil: iki çözücü
farklı bir yol tarif ettiyse puan en az 3'tür.

---

## 4 · Alternatif çözüm — bu kitabın en sinsi kusuru

Bir bulmacanın **ikinci bir geçerli cevabı** olması, çözülemez olmasından
daha kötüdür: okur cevabını doğru sanır, doğrulama sayfası reddeder ve
**kitabı bozuk sanır**.

Zorunlu prosedür:

1. Yazar en az **üç** alternatif aday üretir
2. Her biri için **neden geçersiz olduğu** yazılır
3. Gerekçe "zorlama" ise **bulmaca yeniden yazılır**
4. Çözücü testinde bir alternatif ortaya çıkarsa kayıt açılır ve
   bulmaca **yeniden yazılır** — test tekrarlanır

`confirmedAlternativeSolutions > 0` olan hiçbir bulmaca `validated` olamaz.

---

## 5 · Dış bilgi yasağı

Hiçbir bulmaca kitabın dışındaki bilgiyi gerektiremez.

| ✅ Olur | ❌ Olmaz |
|---|---|
| Ogham alfabesi — **araçlar levhasında verilmiş** | Okurun Ogham bilmesini beklemek |
| Bir folklor motifi — **o sayfada anlatılmış** | "Herkesin bildiği gibi…" |
| Önceki bir bulmacanın çıktısı | İnternet araması gerektiren ipucu |

`solutionPath`'in **her adımı** bu kurala göre denetlenir.

---

## 6 · Üç kademeli ipucu — rakiplere doğrudan cevap

Cain's Jawbone'u yalnızca üç kişi çözebildi. Bu bir başarı hikâyesi olarak
anlatılır; **ticari olarak ise bir terk oranıdır**.

Bu kitap tersini yapar: **amaç okuru yenmek değil, içeride tutmaktır.**

| Kademe | Ne verir | Ne vermez |
|---|---|---|
| **1 · yönlendirme** | Nereye bakılacağı | Yöntem |
| **2 · yöntem** | Hangi tekniğin kullanılacağı | Cevap |
| **3 · neredeyse-cevap** | Son adım hariç her şey | Cevabın kendisi |

`qa_hints` her bulmacada **üç kademenin de** bulunduğunu ve **hiçbirinin
cevabı içermediğini** mekanik olarak denetler.

---

## 7 · Bağımlılık grafiği (DAG)

- Grafik **döngüsüz** olmalıdır
- Bir bulmaca **yalnızca kendinden önceki** bulmacalara bağlanabilir
- Kapı bulmacaları yalnızca **kendi kapılarındaki** bulmacalara bağlanır
- Meta-mister **beş kapının çıktısına** bağlanır

`qa_dependency` döngü ve ileri referans arar. Kapı V öz-göndergeseldir ve
kitabın **fiziksel yapısına** (sayfa numaraları, dizin) bağlıdır — bu
yüzden Kapı V ancak **dizgi dondurulduktan sonra** kilitlenir (Faz 5).

---

## 8 · Çözücü testi

**Ajan bu testi yapamaz.** Çözümü zaten bilir; "çözülebilir" yargısı
kanıt değildir.

| Kural | Gerekçe |
|---|---|
| Test **harici** insanlarla yapılır | Yazarın bildiği şey kitapta olmayabilir |
| Çözücüler **bağımsız** çalışır | Birbirine ipucu veren iki çözücü bir çözücüdür |
| Kimlik **anonimdir** (`solver-01`) | Mahremiyet |
| Kapı I için **5 çözücü** | Öldürme kapısının istatistiksel tabanı |
| Diğer kapılar için **≥2** | Maliyet/fayda dengesi |
| Bir çözücü takılırsa suç **bulmacadadır** | Tasarım kusuru, çözücü kusuru değil |

---

## 9 · Öldürme kapısı (Faz 2)

Eşikler `project_config.json § killGate` içinde **sayısal** durur ve
`validate_spec.py` onların düşürülmesini yakalar.

| Sonuç | Karar |
|---|---|
| 4–5 çözücü Kapı I'i bitirdi, 0 alternatif çözüm | ✅ **DEVAM** |
| 4–5 bitirdi, alternatif çözüm var | ⚠ Yeniden yaz, **testi tekrarla** |
| Tam 3 bitirdi | ⚠ Kapı I yeniden tasarlanır, test tekrarlanır |
| **≤2 bitirdi** | ⛔ **SERT DURDURMA — yazıma devam edilmez** |

> Bu fazın sonucu **güzelleştirilmez**. Öldürme kapısının bütün değeri
> dürüstlüğünden gelir. 3/5 sonucu "neredeyse 4" değildir.
