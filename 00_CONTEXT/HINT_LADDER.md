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
| Hiçbir ipucu **cevap dizesini içermez** | `qa_hints` |
| İpucu metni bulmacanın kendisinden **daha uzun olamaz** | `qa_hints` |
| İpuçları **arka maddede** durur, sayfada değil | dizgi |
| İpuçlar **ters basılır** veya ayrı bölümdedir | dizgi |

> Ters basım kasıtlıdır: okurun **kaza eseri** ipucu görmesini engeller.
> Bir bulmaca kitabında yanlışlıkla görülen ipucu, bozulmuş bir deneyimdir.

---

## 4 · İpuçları çözüm değildir

Bu ayrım `.gitignore` düzeyinde de geçerlidir: **ipuçları PROTECTED
katmandadır**, çünkü üçüncü kademe cevabı dolaylı olarak verir.

`hints` alanı `contentProtection.solutionFieldNames` listesindedir ve
public depoda bulunması CI'ı kırmızı yakar.

---

## 5 · Kapı bulmacaları ve meta-mister

| Bulmaca tipi | İpucu |
|---|---|
| Normal bulmaca | 3 kademe |
| **Kapı bulmacası** | 3 kademe — ama 1. kademe hangi bulmacaların girdi olduğunu söyler |
| **Meta-mister** | 3 kademe — ama 3. kademe **son adımı vermez**; doğrulama sayfası oradadır |

Meta-misterin cevabı kitapta **yoktur** ve hiçbir ipucu onu vermez.
`qa_meta` bunu denetler.
