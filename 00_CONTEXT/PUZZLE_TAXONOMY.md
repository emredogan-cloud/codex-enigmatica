# BULMACA TAKSONOMİSİ — on yedi mekanizma ailesi

> Makine okunur hâli: [`../01_SOURCE/mechanism_families.json`](../01_SOURCE/mechanism_families.json)
>
> Sürüm 1.1 · Faz 1 · Değişiklik kurucu kararı gerektirir

---

## 1 · Aile nedir, ne değildir

Bir **mekanizma ailesi** bir bulmacanın *nasıl çözüldüğünü* söyler.
*Neyin* çözüm olduğunu söylemez — bu yüzden bu taksonomi PUBLIC katmandadır.

Bir ailenin var olabilmesi için dört şeyi olmak zorundadır:

| # | Parça | Neden zorunlu |
|---|---|---|
| ① | **Tanım** | Çözme eylemi tek cümlede anlatılamıyorsa aile değildir |
| ② | **Hedef zorluk** | Hangi bantta çalıştığı bilinmeyen aile zorluk eğrisini kırar |
| ③ | **Doğrulama yöntemi** | ⭑ Tekilliğin **mekanik** ispatı ⭑ |
| ④ | **Örnek** | Kitaptan **değil**, kurgu |

`qa_taxonomy § ①` dördünü de denetler.

### ③ neden bu listenin varlık sebebi

> *"Bu bulmacanın tek cevabı var"* bir **kanaattir**.
> *"Anahtar uzayı 25 kaydırmadır ve yalnızca biri kitapta tanımlı sözlüğe
> oturur"* bir **ispattır**.

Bir aile ispat yöntemi tanımlayamıyorsa o aile bu kitaba **giremez**.

---

## 2 · ⚠ Faz 1 kırmızı takım bulgusu — dokuz ailenin ispatı ispat değildi

Bağımsız bir saldırı, on yedi ailenin `validationMethod` alanını denetledi.
Bulgu sert ve **kabul edildi**:

| Yargı | Aile sayısı |
|---|---|
| Gerçek mekanik ispat | 2 |
| **Yanlış önermeyi ispatlıyor** | 5 |
| **Yanlışlanamaz** (alan sayılabilir değil) | 4 |
| **Hedefin yeniden ifadesi** | 3 |
| Sağlam ama eksik | 3 |

Dokuzunda tekrar eden kusur **aynıdır**:

> **Sayım alanını, cevabı zaten bilen yazar tanımlıyor.**
> Yazarın seçtiği bir alan üzerinde yapılan ispat bir totolojidir.

### Kabul edilen düzeltme — `answerSpace`

Faz 2'den itibaren her bulmaca makine okunur bir **cevap uzayı** dosyası
taşır: *okurun, kitabın ona öğrettikleriyle uygulayabileceği herhangi bir
yordamla ulaşabileceği bütün dizeler.*

`qa_uniqueness` şunu ister:

- sayım alanı **proza değil dosya** olmalıdır
- `answerSpace`'in **tam olarak bir** üyesi kabul edilmelidir
- `qa_hints` her ipucunu **bütün** `answerSpace` üyelerine karşı denetler

Bu, Faz 2'nin ilk teslimatıdır ve bulmaca yazımından **önce** gelir.
Gerekçe ve tam liste: [`RED_TEAM_CHECKLIST.md`](RED_TEAM_CHECKLIST.md).

---

## 3 · Aileler

Zorluk bandı `[alt, üst]`; kapı zorluğu bu banda **kırpılır**.

### Gözlem

| Aile | Zorluk | Levha | Künye | Alternatif cevap riski |
|---|---|---|---|---|
| `plate-observation` — levha gözlemi | 1–2 | ✔ | — | **YÜKSEK** |

Gravürde açıkça çizilmiş ama fark edilmesi gereken ayrıntı.

> ⚠ **"Tuhaf olanı bul" bir yüklem değildir.** Kabul edilebilir yüklemler
> **ikili değerlidir ve sayılabilir**: yön, tekrar sayısı, temas, kapalı/açık
> kontur, basılı bir eksenin hangi tarafı. Kabul edilmez, her zaman:
> *saklı · farklı · tuhaf · yersiz · yanlış.*
>
> Ve üretim sırası **terstir**: önce öğe künyesi yazılır, **sonra** levha
> o künyeden gravürlenir. Çizimden çıkarılan bir künye dairesel bir ispattır
> — yazarın fark etmediği öğe, tanımı gereği alanda yoktur.

### Şifre

| Aile | Zorluk | Levha | Künye | Risk |
|---|---|---|---|---|
| `plate-embedded-cipher` — levha içi şifre | **1**–3 | ✔ veri | — | **YÜKSEK** |
| `substitution-cipher` — yer değiştirme | 1–2 | — | — | düşük |
| `transposition-cipher` — sıralama | 1–3 | — | — | orta |
| `polyalphabetic-cipher` — çok alfabeli | 2–3 | — | — | orta |
| `script-decoding` — yazı sistemi | 1–2 | ✔ veri | ✔ | orta |

`plate-embedded-cipher` kitabın **imza mekaniğidir**. Faz 1'de alt sınırı
2'den **1'e indirildi**: Kapı II'nin görevi bu mekaniği öğretmekti ama
kitapta onun zorluk-1 örneği **hiç yoktu**. Kapı I'e iki örnek konuldu
(slot 8 ve 16).

> ⚠ Bu ailede okuma **yönü** ve **başlangıç noktası** metinde
> sabitlenmezse iki geçerli okuma doğar. İkisi de sabitlenir.

`script-decoding` için **sözleşmenin dördüncü sözü** geçerlidir:
*kitap size bir çizelge veriyorsa, o çizelge tek yetkedir.* Ogham, runik ve
semaphore'u **bilen** okur ile bilmeyen okur aynı cevapta buluşmalıdır —
yoksa bilen okur savunulabilir bir ikinci cevap üretir.

### Mantık

| Aile | Zorluk | Levha | Künye | Risk |
|---|---|---|---|---|
| `constraint-logic` — kısıtlı mantık | 1–3 | — | — | **düşük** |
| `classification` — işlevsel tasnif | 2 | ✔ | ✔ | **EN YÜKSEK** |
| `numeral-system` — sayı sistemi | 2 | ✔ veri | ✔ | orta |
| `cyclic-calendar` — çevrimsel takvim | 2–3 | ✔ veri | ✔ | orta |

> ### ⚠ `classification` — analizle tekilleştirilemez
>
> Altı öğelik bir küme **6** farklı "biri diğerlerinden ayrı" bölünmesi
> kabul eder. Her öğe *m* ikili nitelik taşırsa, rastgele bir nitelik tam
> olarak birini ayırma olasılığı 2·C(6,1)·2⁻⁶ = **0,1875**'tir. Gerçek bir
> folklor motifi rahatlıkla otuz kullanışlı nitelik taşır → beklenen sahte
> 5–1 ayrımı sayısı **~5,6**.
>
> Kültürel bir nesnenin nitelik ekseni **sonlu değildir ve listelenemez** —
> yani bu ailenin ispat yöntemi yanlışlanamaz.
>
> **Kabul edilen düzeltme:** aile ancak *nitelik matrisi sayfada basılıysa*
> ve metin *"bu matris bütün dünyadır"* diyorsa kullanılabilir. O zaman
> ispat gerçek olur: tam olarak bir sütunun 5–1 ayrımı vardır. Okurun
> yaratık hakkında **düşünmeye** davet edildiği bir tasnif bulmacası bu
> kitaba giremez.

`numeral-system` ve `cyclic-calendar`'da tehlike aritmetikte değil
**notasyondadır**: Roma çıkarma notasyonu, Babil'de sıfır yer tutucusunun
yokluğu (değer 60ᵏ'ye kadar belirsizdir), takvimde kapsayıcı/dışlayıcı
sayım. Üçü de metinde **sabitlenir**.

### Uzam ve zincir

| Aile | Zorluk | Levha | Risk |
|---|---|---|---|
| `path-graph` — yol ve çizge | 3 | ✔ veri | **YÜKSEK** |
| `layered-chain` — katmanlı zincir | 3 | — | sessiz yanlış |

`path-graph`'ta **iki bedava ikinci cevap** vardır ve ikisi de kapatılmak
zorundadır: yolun **tersi** ve haritanın **ayna simetrisi**. Etiketli
çizgenin otomorfizma grubu **birim** olmalı ya da her simetri basılı
asimetrik bir etiketle kırılmalıdır. Ve ispat **son gravürden çıkarılan**
çizge üzerinde tekrarlanır: Faz 5'te eklenen dekoratif tek bir bağ, tekil
yolu üçe çıkarabilir.

`layered-chain`'in riski belirsizlik değil **sessiz yanlıştır**: yanlış bir
ara değer de beş harfliyse zincir ilerlemeye devam eder ve okur sonuna
kadar hata sinyali almaz. Halka başına hata **tespit edilebilir** olmalıdır.

### Öz-göndergesel

| Aile | Zorluk | Metne bağlı | Risk |
|---|---|---|---|
| `back-reference` — geriye gönderme | 3 | ✔ | kayan alan |
| `book-structure` — kitabın yapısı | 3 | ✔ | **kırılganlık** |
| `narrative-embedded` — anlatıya gömülü | 3 | ✔ | **kırılganlık** |

Üçü de `textBound` işaretlidir ve `boundToTextHash` taşımak **zorundadır**
(status `drafted` ve sonrası). Gerekçe: Faz 5'in LINE EDITOR alt-ajanı tam
olarak bu bulmacaların saklandığı prozayı düzeltmekle görevlidir. Karma
olmadan bir düzeltme bulmacayı **sessizce** kırar — ve hiçbir test kırmızı
yanmaz, çünkü hiçbir test metne bağlı değildir.

`qa_taxonomy § ⑨` bu kuralı uygular.

### Kapanış

| Aile | Zorluk | Risk |
|---|---|---|
| `gate-synthesis` — kapı bulmacası | 1–3 | **bağımlılık** |
| `meta-synthesis` — meta-mister | 3 | **kritik** |

`gate-synthesis` için girdi bütünlüğü yetmez: çıkarım fonksiyonunun
**hata davranışı** da tanımlanmalıdır. Tek bir girdi yanlışsa çıktı
*tespit edilebilir biçimde geçersiz* mi oluyor (iyi), yoksa *makul görünen
başka bir dize* mi (ölümcül)? Bu bir hata-tespit-kodu şartıdır.

---

## 4 · Çeşitlilik kuralları

`project_config.json § taxonomy` içinde sayısaldır ve `qa_taxonomy § ⑤`
uygular:

| Kural | Değer | Neden |
|---|---|---|
| Kapı içi tek aile payı | **≤ %35** | Okur bir mekanizmayı üçüncü tekrarında öğrenir |
| Kapı başına ayrı aile | **≥ 4** | Tek aileli kapı bir bulmaca değil bir işlemdir |
| Kitap genelinde ayrı aile | **≥ 10** | "Yüz bulmaca" vaadi çeşitlilik vaadidir |
| Ardışık aynı aile | **≤ 6** | — |

> ⚠ **Faz 1 düzeltmesi.** Kapı I'in ilk dizilimi altı ardışık levha gözlemi
> ve altı ardışık mantık bulmacası içeriyordu; her ikisi de eşiğe tam
> oturuyordu ve **ikisi de kusurdu**. Otuz dolar ödeyen okur beşinci
> "farkı bul"da kitabın ne olduğuna karar verir, ve o karar bir iadedir.
> Yeni dizilimde en uzun ardışık dizi **2**'dir.

---

## 5 · Yedek havuz kuralı

Bir yedek, **kötü bir bulmacaya** karşı korur. Bir **ailenin** çökmesine
karşı korumaz — ve aile çöküşü tam olarak beklenen kusurdur.

| Kural | Değer |
|---|---|
| Kapı başına kapı bulmacası adayı | **≥ 2** |
| Yedek havuzdaki ayrı aile | **≥ 3** |
| Yedek `substitutableFor` taşır | zorunlu |
| Yedek **çapraz aileden** olmalı | zorunlu |

Gerekçe: Faz 1'e girerken her kapıda **tek** kapı bulmacası adayı vardı —
yani kitabın en yüksek bağımlılıklı bulmacasının, düşerse on dokuz
bulmacayı da götüren bulmacanın yedeği **sıfırdı**.
