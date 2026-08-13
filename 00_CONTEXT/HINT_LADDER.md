# İPUCU MERDİVENİ — üç kademe

> Bu kitabın rakiplerinden ayrıldığı en somut yer burasıdır ve aynı
> zamanda arka maddenin en çok sayfa yiyen kısmıdır (300 ipucu).
>
> Sürüm 1.0 · Faz 1'de onaylanır

---

## 1 · Neden var

Cain's Jawbone'u yalnızca üç kişi çözdü. Bu, edebî bir efsane olarak
anlatılır — ama **ticari olarak bir terk oranıdır**: kitabı alan
insanların ezici çoğunluğu onu bitiremedi.

Bu kitabın konumu bilinçli olarak farklıdır:

> **Amaç okuru yenmek değil, içeride tutmaktır.**

Ve bu, A+ içeriğinde doğrudan bir satış argümanına dönüşür:
*"pes etmenize izin verilir."*

---

## 2 · Üç kademe

| Kademe | Adı | Ne verir | Ne VERMEZ |
|---|---|---|---|
| **1** | yönlendirme | Nereye bakılacağı | Yöntem, cevap |
| **2** | yöntem | Hangi tekniğin kullanılacağı | Cevap |
| **3** | neredeyse-cevap | Son adım hariç her şey | **Cevabın kendisi** |

### Örnek yapı (kurgu bir bulmaca üzerinde)

| Kademe | Metin |
|---|---|
| 1 | *"Levhanın kenar süsü tekrar etmiyor."* |
| 2 | *"Tekrar etmeyen bir dizi, bir alfabe olabilir. Araçlar levhasına dönün."* |
| 3 | *"Ogham harflerini soldan sağa okuyun. İlk beşi bir ad veriyor."* |

Üçüncü kademe adı **söylemez** — okuma yöntemini verir ve son adımı
okura bırakır.

---

## 3 · Mekanik kurallar

| Kural | Denetleyen |
|---|---|
| Her bulmacada **üç kademe de** bulunur | `qa_hints` |
| Hiçbir ipucu **cevap dizesini içermez** — dört gizleme biçimine karşı | `qa_hints` |
| **Tek bir** ipucu bulmacadan uzun olamaz | `qa_hints` |
| Merdiven gerçekten **yükselir** — kapsam monoton artar | `qa_hints` |
| 3. kademe **son adımı vermez** | `qa_hints` |
| İpuçları **arka maddede** durur, sayfada değil | dizgi |
| İpuçlar **ters basılır** veya ayrı bölümdedir | dizgi |

> Ters basım kasıtlıdır: okurun **kaza eseri** ipucu görmesini engeller.
> Bir bulmaca kitabında yanlışlıkla görülen ipucu, bozulmuş bir deneyimdir.

### ⚠ Ama ters basım bir denetim boşluğu açar

Ters basılacak bir ipucu, kaynak metinde **tersten** yazılmış bir cevap
içerebilir: düz bir alt dize araması onu göremez, **kâğıtta ise cevap
düzgün okunur.** `qa_hints` bu yüzden dört biçimi birden dener:

| Gizleme | Nasıl yakalanır |
|---|---|
| Noktalama ve büyük harf | Normalizasyon |
| Boşlukların kaldırılması | Sıkıştırılmış biçim |
| **Tersten yazım (ayna baskı)** | Ters biçim |
| Kelimelerin dağıtılması | Kelime kümesi kapsaması |

Kanarya künyesi de **ters karmaları** taşır — aynı sebeple.

### ⚠ Uzunluk kuralı Faz 1'de düzeltildi

Eski kural üç ipucunun **toplamını** bulmaca metniyle karşılaştırıyordu ve
`STYLE § 4` ile çelişiyordu: ipucu başına 40 kelime tavanı üç kademede
120 kelime eder, ama bulmaca metninin alt sınırı 90 kelimedir. İkisi
birlikte, 90 kelimelik bir bulmaca için kademe başına 30 kelime bırakıyordu
— ve katmanlı bir zincir için 30 kelimede "neredeyse-cevap" **yazılamaz**.

Yeni kural: **tek bir** ipucu bulmacadan uzun olamaz.

---

## 4 · İpuçları çözüm değildir

Bu ayrım `.gitignore` düzeyinde de geçerlidir: **ipuçları PROTECTED
katmandadır**, çünkü üçüncü kademe cevabı dolaylı olarak verir.

`hints` alanı `contentProtection.solutionFieldNames` listesindedir ve
public depoda bulunması CI'ı kırmızı yakar.

Ayrıca **3. kademe ipucu kanaryanın cevap kümesine dâhildir**:
"neredeyse-cevap" public bir dosyada durursa, cevap durmuş sayılır.

---

## 5 · Kapı bulmacaları ve meta-mister

| Bulmaca tipi | İpucu |
|---|---|
| Normal bulmaca | 3 kademe |
| **Kapı bulmacası** | 3 kademe — ama 1. kademe hangi bulmacaların girdi olduğunu söyler |
| **Meta-mister** | 3 kademe — ama 3. kademe **son adımı vermez**; doğrulama sayfası oradadır |

Meta-misterin cevabı kitapta **yoktur** ve hiçbir ipucu onu vermez.
`qa_meta` bunu denetler.
