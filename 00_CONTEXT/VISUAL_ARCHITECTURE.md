# GÖRSEL MİMARİ — dört levha sınıfı

> Faz 1 **spesifikasyondur**. Levhalar Faz 5'te üretilir.
> `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` Faz 5 teslimatıdır ve bu belgedeki
> sınıfları **taşımak zorundadır**.
>
> Sürüm 1.0 · Faz 1

---

## 1 · Bu kitapta levha bir süs değildir

Diğer Codex ciltlerinde gravür bir **estetik** başarıydı. Burada aynı
tutarlılık bir **çözülebilirlik şartıdır**: okur levhanın dilini öğrenir
ve şifreyi o dilde arar. Tutarsız bir levha, yanlış bir ipucudur.

Ve bir levha bulmacayı **çözülemez** yapabilir: kaybolan bir detay,
yanlış bulmacaya bağlanan bir levha, ya da baskıda kapanan bir aralık.

---

## 2 · Dört sınıf

| Sınıf | Ne yapar | Gizlilik | Nerede durur |
|---|---|---|---|
| **PUZZLE VISUAL** | Bulmacanın **verisini taşır** | `restricted` | `07_ASSETS/plates/` — depoda **değil** |
| **TOOL VISUAL** | Araçlar levhası: çizelgeler, alfabeler | `public` | `07_ASSETS/plates/` |
| **DECORATIVE VISUAL** | Kapı açılışı, kolofon süsü — **veri taşımaz** | `public` | `07_ASSETS/plates/` |
| **ANSWER VISUAL** | Çözüm bölümünün açıklayıcı şeması | ⭑ `protected` ⭑ | **yerelde, ayrıca** |

### ⚠ ANSWER VISUAL neden ayrı bir sınıf

Bir çözüm şeması cevabı **resmeder**. Bir sızıntı taraması metin arar;
bir görselin içindeki cevabı **göremez**. Bu yüzden cevap görselleri
metin katmanıyla aynı korumaya tabidir ve `.gitignore` onları yol
kalıbıyla dışlar.

`qa_solution_leak` ikili dosyaları tarayamaz — sınıflandırma bu boşluğun
yerine geçen **tek** mekanizmadır. Bir görselin sınıfı, dosya adında
**taşınır**: `pl-*` (puzzle) · `tl-*` (tool) · `dc-*` (decorative) ·
`an-*` (answer).

---

## 3 · PUZZLE VISUAL — veri taşıyan levha

Bu, kitabın **imza mekaniğidir** ve aynı zamanda en kırılgan parçasıdır.

### Veri bütçesi

Her veri taşıyan levha `plateDataBudget` doldurmak zorundadır:

| Alan | Ne |
|---|---|
| `carrier` | Veriyi ne taşıyor: tarama yönü, sembol sırası, çentik dizisi, temas |
| `bits` | Taşıyıcı kaç bit taşıyor |
| `minPrintFeatureMm` | ⭑ Baskıda **ayırt edilmesi gereken en küçük detay** |

Arz talebi karşılamalıdır: çözüm 12 bit istiyorsa taşıyıcı ≥12 bit
taşımalıdır. Bu, gravür çizilmeden **önce** hesaplanır.

### ⚠ `minPrintFeatureMm` ölçümle doldurulur, tahminle değil

Ekranda kusursuz görünen bir gravür, krem kâğıtta nokta yayılmasıyla
detay kaybeder. İki bitişik çizgi arasındaki 0,3 mm'lik boşluk kapanır ve
dizi okunamaz hâle gelir.

**Kural:** her veri taşıyan **aile** için en az bir temsilci levha, o
ailenin ilk bulmacası yazılmadan önce POD provasında basılır ve ölçülen
değer o ailenin bütün levhaları için **taban** olur.

> Faz 1 ölçümü: **151 adayın 60'ı** `plateCarriesData` işaretli.
> Kapı III adaylarının **%79'u** veri taşıyor — portföydeki en yoğun
> baskı bağımlılığı orada.

---

## 4 · Levha bütçesi

| Kalem | Adet |
|---|---|
| Kapı açılışı (5 × 1) | 5 |
| Bulmaca levhası (5 × 20) | 100 |
| Ön madde (araçlar levhası dâhil) | 3 |
| Son soru | 2 |
| **Toplam** | **112** |

Hedef 110 ± %10. `page_budget.py` denetler.

---

## 5 · Prompt mimarisi (Faz 5'te kütüphaneye dönüşür)

`IMAGE_PROMPT_LIBRARY.html` her kayıtta şunları taşır:

```
plateId          →  pl-g1-08
class            →  PUZZLE | TOOL | DECORATIVE | ANSWER
boundToPuzzle    →  bulmaca kimliği   (⚠ yanlış bağ = çözülemez bulmaca)
carrier          →  veriyi taşıyan görsel öğe
minFeatureMm     →  ölçülmüş taban
prompt           →  üretim metni
negativePrompt   →  veriyi bozacak biçimler
```

### ⚠ ANSWER sınıfı kütüphanede prompt taşımaz

Cevap görselinin prompt'u cevabı tarif eder. `IMAGE_PROMPT_LIBRARY.html`
public bir dosyadır; `an-*` kayıtları orada yalnızca **kimlik ve sınıf**
taşır. Prompt metni korumalı katmandadır.

`validate_structure` bu kural için bir kapı taşır: dosya ortaya çıktığında
(Faz 5) dört sınıf işaretini de taşımak zorundadır ve `an-*` kayıtlarında
`prompt` alanı **bulunamaz**.

---

## 6 · Faz 1'de üretilmeyen şey

Levha **üretilmedi**. Üretilen: sınıflandırma, veri bütçesi alanları,
dosya adı sözleşmesi, gizlilik kuralı ve baskı ölçümü zorunluluğu.

Gerekçe: bir levhayı çizmek ucuzdur, **yanlış bulmacaya bağlanmış** bir
levhayı Faz 5'te bulmak pahalıdır. Ve bir levhanın taşıyabileceği veri
miktarı, o levhaya bağlı bulmacanın mekaniğini **belirler** — yani bu
hesap bulmaca yazımından önce gelmelidir.
