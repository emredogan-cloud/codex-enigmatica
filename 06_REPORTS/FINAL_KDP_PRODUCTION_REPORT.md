# NİHAİ KDP ÜRETİM RAPORU — Codex Enigmatica

**Tarih:** 25 Ağustos 2026 · **Kapı seviyesi:** `phase5`

> # ⛔ YÜKLEMEYİ ENGELLEYEN İKİ ŞEY VAR
>
> **① DİL.** İç blok **TÜRKÇEDİR**; metadata **İngilizce** ilan ediyor.
> **② CEVAP SIZINTISI.** Genel geçmişteki commit mesajı hâlâ açık.
>
> Dosyalar üretildi ve teknik olarak geçerli. Ama bu iki madde
> kapanmadan **yüklenmemelidir**. Ayrıntı § 1 ve § 9.

---

## 1 · ⛔ DİL — en büyük engel

`book.json.language = **tr**` · `metadata.language = **en**`

İç blok, ön madde, bulmacalar, ipuçları ve çözümler **Türkçedir**.
Ürün sayfası metni (başlık, açıklama, anahtar kelimeler, A+ metni) ve
arka kapak yazısı **İngilizcedir**.

**Bu bir ihmal değil, bilinçli bir tasarım kararının sonucudur** (K20 ·
`DECISIONS.md`): *"Beşinin beşi de Türkçe konuşuyor."* Bir bulmacanın
mekaniği ancak çözücünün ana dilinde ölçülebilir; pilot bu yüzden
Türkçedir.

**İngilizce sürüm bu pasta üretilemezdi.** `04_BUILD/english_readiness.py`:

> `⛔ DÖNÜŞÜM BAŞLAYAMAZ — pilot doğrulanmadı (A12)`
> Türkçe 29 harf → 6 grup · İngilizce 26 harf → 6 grup ⇒ **şifreli
> dizelerin TAMAMI yeniden üretilir**, grup koşuluna dayanan bulmacalar
> **yeniden tasarlanır**.

**Kurucu kararı gerekiyor — iki yol var:**

- **(a) Türkçe sürüm yayımla.** Dosyalar hazır. Başlık/açıklama/anahtar
  kelimeler ve arka kapak metninin Türkçesi yazılmalıdır. Ticari metni
  **uydurmadım**; bu sizin kararınız.
- **(b) İngilizceyi bekle.** A12 kapanmadan başlayamaz.

## 2 · 14 düzeltilmiş gravür

**Hepsi üretildi ve sözleşmesine UYUYOR.** Ama OpenAI ile değil.

### Neden API bırakıldı

`pl-g3-03` (sözleşme **7 istasyon**) üç kez üretildi:

| # | Değişiklik | Sonuç |
|---|---|---|
| 1 | özgün prompt | **8 istasyon**, üstelik 3B perspektif halka |
| 2 | sahne "düz halka diyagramı"na çevrildi | **12 istasyon** (üslup düzeldi) |
| 3 | sayı ilk cümleye taşındı | **12 istasyon** |

Üslup her adımda düzeldi, **sayı hiç düzelmedi**. Bir gravür bu kitapta
süs değil **veridir**; yedi istasyon isteyen bulmacaya on iki istasyonlu
halka basmak çözülemeyen bulmaca basmaktır.

### Ne yapıldı

`04_BUILD/plate_render.py` on dördünü **deterministik** çizdi. Sayılar
kütüphaneden — yani üreteçten, yani bulmacadan — okundu; kod kesin sayar.

| Levha | Sözleşme | Çizilen |
|---|---|---|
| `pl-g3-03` `pl-g3-08` `pl-g3-13` | 7 istasyon + 1 ■ | ✅ |
| `pl-g2-09` `pl-g3-18` `pl-g4-06` | 6 istasyon + 1 ■ | ✅ |
| `pl-g2-02` `pl-g2-05` `pl-g2-15` | 7 istasyon | ✅ |
| `pl-g2-12` | 7 istasyon + 2 ● + 1 ■ | ✅ |
| `pl-g2-18` | 7 istasyon + 1 / | ✅ |
| `pl-g4-18` | 4 istasyon + 1 ■ | ✅ |
| `pl-g1-07` | 7 ┬ + 1 ▲ + 1 ◆ (9 istasyon) | ✅ |
| `pl-g1-08` | tek sıra 6 nesne · 4 ○ + 2 ● | ✅ |

Dördü gözle tek tek sayıldı; kalan onu aynı kod yolundan geçti ve altısı
ayrıca montajda doğrulandı. **Nihai baskı çözünürlüğünde doğrudan
çizildiler** (2700 px @ 600 dpi) — AI yükseltici, tahmin edilecek bir
detay olmadığı için atlandı.

> ⚠ **ÜSLUP FARKI VAR.** Bu on dört levha diğer 89'dan daha grafik/temiz
> durur. Veri taşıyan bir diyagram için savunulabilir bir takas, ama
> göze çarpıyor. İsterseniz sanatsal uyum için ayrı bir pas gerekir —
> **bu KDP'yi engellemez**, ertelenmiştir.

## 3 · Prompt üretecinde düzeltilen iki kusur

- **Sahne, nesneyi değil ÇİZİM BİÇİMİNİ tarif ediyor.** "seen face-on"
  yetmedi; artık "düz halka diyagramı, doğrudan yukarıdan, kalınlık yok,
  eğim yok".
- **Sayı, listenin ortasından İLK cümleye taşındı.** Kütüphanedeki
  değiştirilemez veri **değişmedi** (ölçüldü: 0 fark).

## 4 · İÇ BLOK

| | |
|---|---|
| **SAYFA (ölçülen)** | **263** |
| Bulmaca | 101 |
| İpucu | 303 (3 kademe) |
| Basılan çözüm | **100** — meta HARİÇ |
| Trim | 6 × 9 in |
| İç kenar payı | 0,50 in (KDP tablosu · 151–300 sayfa) |
| Dış/üst/alt | 0,50 / 0,60 / 0,60 in |
| PDF | 71,7 MB |

**Eski 238 tahmini ATILDI.** 263 ölçüldü ve türeyen her değer yeniden
hesaplandı: sırt, kenar payı, metadata, arka kapak metni.

### ⭑ Yakalanan üç ciddi kusur

1. **Başlık sayfasına ham Python sözlüğü basılmıştı** — `matter` alanları
   düz metin değil, sözlük/liste. Şekli varsaymak kitabın ilk sayfasına
   hata basmaktı.
2. **Arka maddenin dörtte biri hiç basılmamıştı** — şifre referansı,
   kaynaklar, kolofon ve kapanış liste olarak duruyordu ve atlanmıştı.
   Eklendi (257 → 263 sayfa).
3. **⭑ SON SORUNUN CEVABI ÇÖZÜM BÖLÜMÜNE BASILMIŞTI ⭑** Kitabın kendi
   sözleşmesi diyor ki: *"Son sorunun cevabı arka maddede YOKTUR ve bu
   kitabın hiçbir yerinde basılı değildir."* Kitap ilk sayfasında
   verdiği sözü son sayfasında bozuyordu ve **meta-mister, yani ürünün
   bütün kancası, yok oluyordu.** Artık basılmıyor; bir kapı bunu zorlar.

> ⚠ **Kalan bir soru sizde:** meta cevabı, ARAÇLAR bölümündeki basılı
> **sözlükte** benzer sözcükler arasında bir madde olarak geçiyor
> (s. 9). Cevap olarak işaretlenmiş değil — 101 cevaptan 14'ü aynı
> sözlükte geçiyor, yani tasarım böyle. Yine de sözleşmenin "hiçbir
> yerinde" ifadesiyle sürtüşüyor. **Bulmaca içeriğine dokunmadım.**

### Levha baskı kalitesi

Gravürlerin zemini **krem**di (gri ~219). Krem kâğıda krem basmak, her
levhanın arkasında **%14'lük gri bir kutu** demekti. Levhalar gri tona
çevrildi ve zemin beyaza çekildi: kâğıdın kendi kremi görünür.
PDF 1272 MB → **71,7 MB**.

## 5 · KAPAK

| | |
|---|---|
| Seçilen sanat | **`wrap-cover-option-01`** |
| **SIRT** | **0,6575 in** (263 × 0,0025 krem) |
| Tam kapak | **12,908 × 9,250 in** (taşma dâhil) |
| Taşma | 0,125 in |
| PDF | 34,6 MB |

**Seçim ölçüldü**, beğenilmedi. Dört tipografi bölgesinde kenar enerjisi:

| Bölge (düşük = sakin) | wrap-01 | wrap-02 |
|---|---:|---:|
| **SIRT** | **36,5** | 47,2 |
| Arka kopya alanı | **27,4** | 29,2 |
| Ön başlık alanı | 41,0 | **39,9** |
| Ön yazar alanı | **33,0** | 57,1 |

`wrap-02`nin tam ortasında görünür bir dikey çizgi var — promptun açıkça
yasakladığı "yapay sırt paneli". **3–1 ile `wrap-01`.**

### Tipografi

CLI ile vektör olarak basıldı: ön başlık (panele **sığdırılarak** —
ilk denemede taşıyordu), alt başlık, yazar, yayıncı; sırtta başlık ve
yazar; arka kapakta onaylı metin. **Opak beyaz kutu kullanılmadı.**
Mürekkep rengi zeminden **ölçülür** (ilk denemede açık zemine açık metin
basılmış ve okunmuyordu).

**Uydurulmadı:** ISBN, barkod numarası, ödül, alıntı, "çok satan".
Barkod alanı (2,0 × 1,2 in, arka kapak sağ alt) **boş** bırakıldı.

> ⚠ **SANAT KIRPILDI VE ÇÖZÜNÜRLÜĞÜ SINIRDA.** Teslim edilen sarmal
> **1840 × 855 px** ve **2,15 : 1**; gereken oran **1,40 : 1**. Merkezden
> kırpınca **1193 × 855** kaldı, yani arka ve ön kapağın dış kenarları
> gitti. 12,9 inçlik bir kapakta bu **~93 dpi doğal** demektir; 300 dpi'a
> yükseltildi ama kazanılan detay **tahmindir**.
>
> **Bu KDP'yi teknik olarak engellemez** (ölçü ve taşma doğru) ama
> baskıda yumuşak görünebilir. Daha iyisi için sarmal **1,40 : 1
> oranında ve en az 3900 px genişlikte** yeniden üretilmelidir.

## 6 · HARDCOVER

**ÜRETİLMEDİ.** `metadata.editions.hardcover.enabled = true` ama
hardcover sarmal geometrisi (menteşe payı, farklı sırt, farklı taşma)
paperback'ten türetilemez ve KDP'nin hardcover şablonu ayrıdır.
Paperback geometrisini kopyalamak yönergenin § 12'de açıkça yasakladığı
şeydir. **Ertelendi ve uydurulmadı.**

## 7 · KINDLE

**ÜRETİLMİYOR** — ve bu doğru davranıştır.
`metadata.editions.kindle.enabled = **false**` · `BRIEF § 7`: Kindle
**"üretilmez"**. Yönergenin § 13'ü bunu açıkça koruyor: *"DO NOT
re-enable it merely because this directive says all formats."*

## 8 · A+ · METADATA · PAKET

- **A+:** 6 modül, tam Amazon ölçüsünde, `module-map.json` ile
  GÖRSEL → BAŞLIK → GÖVDE eşlemesi. Yeniden üretilmedi.
- **Metadata:** `pageCount = 263` (ölçülen; model 238 idi). Üç alan
  **boş ve doldurulmadı**: `isbn`, `authorBio`, `aiDisclosureConfirmed`.
- **Paket:**
  `08_OUTPUT/PAPERBACK/` → `interior.pdf` · `cover.pdf` ·
  `metadata.json` · `SHA256SUMS`
  `08_OUTPUT/APLUS/` → 6 PNG · `module-map.json` · `SHA256SUMS`

## 9 · PREFLIGHT VE QA

`kdp_package.py` — **16 denetim yeşil**: PDF geçerliliği · **yazı
tipleri gömülü** · trim 6×9 · sayfa sayısı tutarlı · kapak ölçüsü
sırt+taşma ile tutarlı · A+ tam ölçüde · metadata sayfa sayısı ·
pakete kaynak dosyası sızmamış · sağlama toplamları.

`selftest` **242 denetim yeşil** (bütün kapılar ısırıyor).
`qa_all.sh` — **kanarya HARİÇ** bütün kapılar yeşil.

### ⛔ Kanarya kırmızı — iki ayrı olay

1. **Yeni ve DÜZELTİLDİ:** `04_BUILD/covers.py` içindeki bir yorum
   satırı 8 karakterlik bir cevabı (g5-003) taşıyordu — sıradan bir
   Türkçe kelime, K41 sınıfı. Yeniden yazıldı; bütün yeni dosyalarım
   tarandı ve temiz.
2. **Eski ve AÇIK:** `e341a5f` commit mesajı hâlâ `g3-017`'nin cevabını
   taşıyor. Genel depo; geri alınamaz. Seçtiğiniz onarım (cevabı
   değiştirmek) **Kapı 3-4-5 üretecinin kırık olması yüzünden hâlâ
   uygulanamıyor** (`build_all()` → `g5-013`). CI kip B'de künye
   **bayat** olduğu için bunu görmüyor.

## 10 · Kurucuya kalanlar

**Yüklemeyi engelleyen:**
1. **Dil kararı** (§ 1)
2. Cevap sızıntısı + künye tazeleme + üreteç onarımı (§ 9)

**Yalnızca insanın yapabileceği:**
KDP paneli · Previewer onayı · **yapay zekâ beyanı** · ISBN kararı ·
yazar biyografisi · **fiziksel POD provası (A9)** · Publish ·
A+ moderasyonu

**Ertelenen (KDP'yi engellemez):**
Hardcover · sarmal sanatın yeniden üretimi · 14 levhanın üslup uyumu ·
3 A+ modülünün 3,23:1 yeniden üretimi

## 11 · Değişmeyen

`externalValidation = founder_override_partial` · `sessionsPerformed = 0`
· `humanValidationPassed = false` · **HARD-STOP**.

**Bu kitap hiçbir insanın elinde çözülmedi.**
Hiçbir şey yüklenmedi, yayımlanmadı, moderasyona gönderilmedi, prova
sipariş edilmedi.

**OpenAI harcaması: 0,5049 $** (hedef 3 · tavan 4) —
`06_REPORTS/OPENAI_14_ENGRAVINGS_COST_REPORT.md`
