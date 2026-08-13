# KÜNYE STANDARDI — olgu, kaynak ve okur

> Makine okunur hâli: [`../01_SOURCE/research/sources.json`](../01_SOURCE/research/sources.json)
> Kapısı: `04_BUILD/validate_research.py`
>
> Sürüm 1.0 · Faz 1

---

## 1 · Bu kitapta olgu hatası iki kez vurur

| | Sonuç |
|---|---|
| Okur bir motifin yanlış anlatıldığını görür | **İtibar** kaybı |
| **Bulmaca yanlış bir olguya dayanır** | **Ürün hatası** |

İkincisi bu projede birincisinden ağırdır. Bir bulmaca *"bu işaretin
değeri şudur"* varsayımıyla kuruluysa ve o varsayım yanlışsa, bulmacanın
çözümü **deterministik olmaktan çıkar** — ve kusuru okur bulur, siz değil.

---

## 2 · İki kural

### ① Bulmaca kolaylığı için olgu uydurulmaz

Bir motifin işe yarayan hâli yoksa **bulmaca değişir, olgu değişmez.**

Bu kural en çok baskı altında kalınan yerde geçerlidir: bir kapı bulmacası
on dokuz girdiye bağlıdır ve on sekizincisi "neredeyse" uyuyordur.
Uydurulan tek bir harf, çözülemez bir kapı üretir.

### ② Okur hiçbir kaynağa ihtiyaç duymaz

Künye **bizim** doğrulama aracımızdır; okurun değil. Bulmacanın
gerektirdiği her şey araçlar levhasında veya sayfanın kendisinde
**verilir** (`SOLVABILITY_STANDARD § 5`).

`sources.json § readerNeedsIt: true` olan tek bir kayıt bile
`validate_research § ⑤`'i kırmızı yakar.

---

## 3 · ⚠ Sözleşmenin dördüncü sözü

Üç söz yeterli değildi:

> 1. Her bulmacanın tek bir cevabı vardır.
> 2. Hiçbiri kitabın dışındaki bilgiyi gerektirmez.
> 3. İpucu almak kaybetmek değildir.
> 4. **Kitap size bir çizelge veriyorsa, o çizelge tek yetkedir.**

İkinci söz, dış bilginin **farklı bir cevap üretmesini** engellemez.
Hedef okur bir bulmaca meraklısıdır ve Ogham'ı, runik yazıyı, Roma
sayılarını **biliyor olabilir**. Kitabın çizelgesi ile bildiği çizelge
ayrışırsa, o okur savunulabilir bir **ikinci cevap** üretir, doğrulama
sayfası reddeder ve okur kitabı bozuk sanır.

### Ve bir üretim kuralı doğurur

> Yalnızca kitaptaki değeri **yaygın değerle çakışan** glifler ve
> notasyonlar kullanılır.

Bilen okur ile bilmeyen okur **aynı cevapta buluşmalıdır**. Tartışmalı bir
glif, bir bulmacanın içine konmaz — araçlar levhasının süsüne konabilir.

---

## 4 · Künye kaydı

Her kaynak yedi alan taşır:

| Alan | Not |
|---|---|
| `id` | `sourceRefs` bu anahtara işaret eder |
| `kind` | `script-system` · `cipher-system` · `numeral-system` · `calendar-system` · `signal-system` · `folklore-motif` |
| `title` · `author` · `year` | Künye |
| `rightsStatus` | `public-domain` · `licensed` · `permission-granted` · `verification-only` |
| `verificationStatus` | `asserted` · `checked` — ⚠ § 5 |
| `usage` | Bu kaynak **neyi** doğruluyor |
| `readerNeedsIt` | **Daima `false`** |

---

## 5 · `asserted` ve `checked` — ajanın kanaati bir doğrulama değildir

| Durum | Anlamı |
|---|---|
| `asserted` | Künye kaydedildi, **insan gözüyle doğrulanmadı** |
| `checked` | Birincil veya tıpkıbasım kaynak **görüldü**; tarih ve içerik teyitli |

> ### ⛔ Bir bulmaca `validated` veya `written` olamaz eğer dayandığı kaynak hâlâ `asserted` ise.

`validate_research § ⑥` bunu uygular. Aday aşamasında `asserted` kabul
edilir — aday bir **fikirdir**, basılacak bir olgu değildir.

**Faz 1 durumu: 16 kaynağın 16'sı `asserted`.** Bu bir kurucu
bağımlılığıdır ve Faz 2'nin ilk işlerindendir.

---

## 6 · Kamusal alan tercihi

Bu kitap yüz levha ve yüz bulmaca üretecek. Telifli bir motif tabanına
yaslanmak, Faz 5'te çözülemeyecek bir hak sorunu yaratır.

Faz 1'de kaydedilen **16 kaynağın 16'sı kamusal alandadır**: şifre ve yazı
sistemleri için birincil metinler ve 19.–20. yüzyıl başı derlemeleri;
folklor için Frazer, Grimm, Evans-Wentz, Afanasyev, Lönnrot, Sturluson.

Kamusal alanda **olmayan** bir kaynak yalnızca `verification-only` olarak
kullanılabilir ve `reproduced: true` işaretlenemez.

### İki uyarı kaydın içinde durur

- **Frazer'ın karşılaştırma yöntemi** bugün tartışmalıdır. Motif
  **varlığı** için kullanılır, motif **yorumu** için değil.
- **Landa'nın kaydı** sömürge dönemine aittir ve kusurludur. Bir bulmaca
  yalnızca ona dayanamaz; Förstemann ile **çapraz doğrulanır**.

---

## 7 · Ölü künye

Kaydedilip hiçbir bulmacada kullanılmayan bir kaynak bir **sarkmadır**:
taksonomiyi zenginmiş gibi gösterir.

| Kapı seviyesi | Davranış |
|---|---|
| `phase1` – `phase3` | **Uyarı** |
| `phase4` ve sonrası | **Kırmızı** |

Faz 4'te manuscript özünde tamamdır; hâlâ kullanılmayan bir kaynak
kullanılmayacak demektir.

---

## 8 · Notasyon tuzakları — künyeye yazılır, bulmacada sabitlenir

Bu üçü, gerçek kaynaklarda **gerçekten** değişkendir ve her biri temiz,
savunulabilir bir ikinci cevap üretir:

| Sistem | Değişken | Bulmacada ne yapılır |
|---|---|---|
| Roma sayıları | Çıkarma notasyonu (IV / IIII) | Metin **hangisini** kullandığını söyler |
| Babil sayıları | Sıfır yer tutucusu ve ayraç yok → değer 60ᵏ'ye kadar belirsiz | Basamak sayısı metinde **sabitlenir** |
| Takvim çevrimi | Kapsayıcı / dışlayıcı sayım, yön, 0/1 indeksleme | Üçü de **basılı metinle** sabitlenir |

> Bir notasyon belirsizliği, çözücü testinde "çözemedi" olarak değil,
> **"başka bir cevap verdi"** olarak görünür — ve bu daha kötüdür.
