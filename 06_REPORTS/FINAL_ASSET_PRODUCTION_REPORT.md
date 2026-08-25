# NİHAİ VARLIK ÜRETİM RAPORU — Codex Enigmatica

**Tarih:** 25 Ağustos 2026 · **Kapı seviyesi:** `phase5`

> # ⛔ İKİ BLOKLAYICI AÇIK — ÖNCE BUNLAR OKUNMALI
>
> **① GENEL DEPODAKİ BİR COMMIT MESAJINDA BİR CEVAP VAR.**
> **② O CEVABI DEĞİŞTİRMEK ŞU AN MÜMKÜN DEĞİL** — Kapı 3-4-5 üreteci
> kırık ve bu **benim değişikliğimden önce de** kırıktı.
>
> Ayrıntı § 1. Bunlar kapanmadan yayımlama yapılmamalıdır.

---

## 1 · ⛔ CEVAP SIZINTISI — ve kapatılamayan onarım

### Ne oldu

Kanarya, **benim yazdığım** `e341a5f` commit mesajında `g3-017`'nin
7 karakterlik cevabını yakaladı. Cevap, sıradan bir Türkçe kelimenin
**içinde**, çekim ekiyle uzamış bir gövdenin ortasında geçiyor.
Yazarken cevap yazdığımı bilmiyordum.

> ⚠ **O CÜMLE BURAYA YAZILMAZ.** İlk taslakta örnek olsun diye
> alıntılamıştım ve kanarya bu raporu da yakaladı — rapor takip edilen
> bir dosyadır. Sızıntıyı tarif etmek onu tekrarlamayı gerektirmez.

Commit **itilmişti**. Depo **PUBLIC**. Git geçmişi geri alınamaz.

### Neden CI yakalamadı

CI kanaryası **kip B**'de koşar: tuzlu künyeyle. Künye **261 karma**
taşıyor, yerel cevap kümesi ise **281 dize**. Künye **bayat** — yani
CI eksik bir cevap kümesiyle tarıyor ve bu cevabı hiç aramadı.

Yerelde (kip A, tam küme) kapı **kırmızı**.

> ⚠ Bu, CI'nın yeşil görünmesinin korumanın çalıştığı anlamına
> gelmediği ikinci vaka. Künye tazelenmeden CI'nın yeşili bu konuda
> bir şey söylemiyor.

### Seçilen onarım ve neden uygulanamadı

Kurucu **cevabın değiştirilmesini** seçti (deponun emsali: `0251692`
ve `f9580c7`'de aynı sınıf çarpışmada cevap değişti). Force-push
elenmişti çünkü GitHub eski nesneyi SHA ile erişilebilir bırakır.

Uygulanamadı. Sebep:

- Cevaplar **elle seçilmez**. `gate_common.assign()` bir geri izlemeli
  çözücüdür: her cevap kapı ifadesine **belirli bir harfi** verir —
  meta-mister buna bağlıdır — ve aile başına uzunluk kısıtı vardır.
- Çözücünün zaten bir **`banned=`** parametresi var; denendi.
- Ama `01_SOURCE/design/_generator/build_gate345.py` → `build_all()`
  **koşmuyor**: `AssertionError: ('g5-013', 'yapı çifti bulunamadı')`.
- Bu hata **benim değişikliğim geri alındıktan sonra da** aynen
  tekrarlanıyor. Yani üreteç, işlenmiş `gate-345.json`'u **yeniden
  üretemiyor**; kod ile kayıtlı çıktı birbirinden **ayrışmış**.
- Ek kanıt: `g3-017`'nin cevabı, üretecin bugünkü üç kataloğunun
  **hiçbirinde yok**.

**Hiçbir bulmaca verisine dokunulmadı.** `book.json`,
`solutions/gate-345.json` ve `design/gate-345.json` bit bit aynı;
denedeğim düzenleme tamamen geri alındı.

### Kurucuya düşen

1. `ENIGMATICA_CANARY_SALT=… python3 04_BUILD/qa_solution_leak.py --emit-manifest`
   ile künyeyi tazeleyin. **Uyarı:** tazelenince CI bu sızıntıyı
   görecek ve main kırmızıya dönecek. Bu doğru davranıştır.
2. Kapı 3-4-5 üretecinin `g5-013` kırığı onarılmadan cevap
   değiştirilemez.
3. Risk değerlendirmesi sizindir: eşleşme, sıradan bir kelimenin
   ortasındaki 7 karakterlik bir parçadır; bir çözücünün bunu cevap
   olarak çıkarma ihtimali pratikte sıfıra yakındır. Ama kapı kırmızı
   ve **kapıyı rahatsız ettiği için gevşetmedim.**

---

## 2 · Teslim alınan varlıklar

| | |
|---|---|
| Teslim edilen dosya | **111** |
| Beklenen prompt | **111** |
| Eksik | **0** |
| Tanınmayan | **0** |
| Reddedilen | **0** |
| Biçim | 111/111 PNG · sRGB · alfa |

Gravür **103** · ön kapak **2** · A+ **6**. Ad mimarisi (`pl-` `dc-`
`tl-` `cover-` `aplus-`) eksiksiz; hiçbir dosya sınıfsız değil.

## 3 · Gerçek çözünürlük — önce ve sonra

⚠ Üç sayı ayrı tutuldu. **Metadata DPI etiketi bir iddiadır, etkin DPI
bir ölçümdür.** Teslim edilen 111 dosyanın hepsi etiketinde `72 dpi`
diyordu; bu hiçbir şey ifade etmez.

**Etkin DPI = gerçek piksel ÷ basılacağı fiziksel ölçü.**
Gravür kutusu `4,5 × 7,5 in` (6×9 trim − 2×0,75 kenar, `plate_proof.py`).

| | önce (ham) | sonra (işlenmiş) |
|---|---|---|
| Gravür · en düşük | **225,5 dpi** | **600 dpi** |
| Gravür · ortanca | 278,7 dpi | 600 dpi |
| Gravür · 300 altı | **77 / 103** | **0 / 103** |
| Ön kapak | **170,7 dpi** | **300 dpi** (1800 × 2700) |

## 4 · ImageMagick / Upscayl işlemleri

`ASSET_UPSCALING_REPORT.md § 3.2` izlendi ve **bir adım eklendi**:

```
ham PNG → [1] Real-ESRGAN 4× (upscayl-standard-4x, GPU 0)
        → [2] hedefe indir (Lanczos)
        → [3] alfa düzleştir
        → [4] DPI etiketle
```

**[2] neden eklendi:** belgelenmiş hat 4×'te durur. 1254 px'lik bir
levhanın 4×'i 5016 px'tir ve 4,5 inçte **1114 dpi** eder — 600 dpi'a
göre kâğıtta karşılığı yok, sadece 52 MB'lık dosya ve boğulan bir PDF.
Yükseltip indirmek (supersampling) doğrudan büyütmekten **daha temiz**
kenar verir; atılan şey kâğıda hiç ulaşmayacak sahte çözünürlüktür.

`identify` ile ölçüm, `montage`/`convert` ile görsel denetim yapıldı.
**111/111 işlendi**, süre ~64 dk (103 gravür 60,6 dk + 8 ticari varlık).

Kalite karşılaştırması gözle yapıldı: AI çıktısı çizgileri belirgin
şekilde keskinleştiriyor (nokta yayılması için doğru yön), buna karşılık
kâğıt dokusunu ve yumuşak tonlamayı düzleştiriyor — gravür için kabul
edilebilir takas. **Sayılabilir işaretler korundu:** `pl-g2-01`'de
9 dolu + 3 boş daire ham ve işlenmişte birebir aynı; en-boy oranları
üç örnekte de 0,00000 fark.

## 5 · 103 gravür — durum

**İşleme:** 103/103, hepsi 600 dpi. **Kabul edildi.**

### ⛔ Ama sözleşme uyumu ayrı bir hikâye

> ⚠ **SAYIMI AJAN YAPMADI.** Otomatik sayım denendi ve **güvenilmedi**:
> eşikleme gravürün kendi taramasını işaret sanıyor (bir levhada 5
> yerine 44 saydı), özilinti armoniklere kilitleniyor (6 yerine 2,6).
> Güvenilmez bir sayaç, sayaç olmamasından **kötüdür** — bakılmamış bir
> levhayı bakılmış gösterir. Bu yüzden ajan sayıyı ölçmedi;
> **insanın ölçmesini mümkün kıldı.**

`python3 04_BUILD/asset_ingest.py --sheet` → `07_ASSETS/PLATE_VERIFICATION.html`
103 levhayı **kendi değiştirilemez sayılarının yanına** basar; sayılacak
şartlar kırmızıdır, kutucuk durumu `localStorage`'da kalır.

**Gözle doğrulanan örneklemde bulunanlar:**

| Levha | Sözleşme | Görselde | Karar |
|---|---|---|---|
| `pl-g1-01` | 5 × ◆ · 5 bant | 5 ◆ · 5 sıra | ✅ |
| `pl-g1-02` | 1 × ◆ · 6 bant | 1 ◆ · 6 sıra | ✅ |
| `pl-g1-07` | **7 × ┬** | **8 ┬** | ⛔ **UYMUYOR** |
| `pl-g1-08` | 4 × ○ + 2 × ● (6 nesne) | **45 kaide**, ~43 ○ | ⛔ **UYMUYOR** |
| `pl-g2-01` | 9 × ● · 3 × ○ | 9 ● · 3 ○ | ✅ |
| `pl-g3-03` | 7 × · · 1 × ■ · **7 istasyon** | 7 nokta · 1 ■ · **8 istasyon** | ⛔ **UYMUYOR** |
| `pl-g3-08` | aynı | 7 nokta · 1 ■ · 8 istasyon | ⛔ **UYMUYOR** |
| `pl-g2-05`, `pl-g4-04`, `pl-g3-08*` | — | sayılar tuttu | ✅ |

**Kalan 90+ levha doğrulanmadı** ve doğrulanmış gibi bildirilmiyor.

### ⭑ VE SEBEBİN BİR KISMI BENDEYDİ ⭑

`2·3` gösterimindeki nokta bir **ayraçtır**, gravüre edilecek bir işaret
değil. `measure()` onu işaret sayıyordu ve **12 levhanın** sözleşmesine
`exactly N of mark '·'` diye **olmayan bir şart** yazmıştı. O şart
istasyon sayısını da bozdu: gravürcü yedi noktaya yer açmak için
sekizinci istasyonu açtı. `pl-g3-03` ve `pl-g3-08` tam olarak böyle
çıktı.

**Düzeltildi** (`04_BUILD/plate_prompts.py`). Bulmaca verisine
dokunulmadı; düzeltilen, veriyi yanlış **okuyan** türetmedir.

**Yeniden üretilmesi gereken 12 levha** (promptları değişti):
`pl-g2-02` `pl-g2-05` `pl-g2-09` `pl-g2-12` `pl-g2-15` `pl-g2-18`
`pl-g3-03` `pl-g3-08` `pl-g3-13` `pl-g3-18` `pl-g4-06` `pl-g4-18`

**Ayrıca yeniden üretilmesi gerekenler** (model sayamamış):
`pl-g1-07` `pl-g1-08`

### Baskı genişliği uyarısı

Dört levha `4,5 in` sütuna **sığmıyor**, yükseklikten sınırlanıyor:
`pl-g1-16` (%92) · `pl-g2-20` (%74) · `pl-g3-20` (%73) · `pl-g5-20` (%73).
Etkin DPI düşmez ama **fiziksel detay küçülür** — %73'te 0,3 mm'lik bir
boşluk 0,22 mm olur. POD provasında (A9) ölçülmelidir.

## 6 · A+ durumu

**6/6 işlendi**, hepsi tam Amazon ölçüsünde (`1940 × 600` ve `600 × 600`,
`prompt_catalog.APLUS_SPEC`).

**Üçü merkezden kırpıldı** — teslim edilen oran 1,82 / 1,90 / 1,62 iken
modül 3,23 istiyor: `aplus-01` `aplus-05` `aplus-06`.

Kırpma **bir taviz olarak** yapıldı ve gözle denetlendi:
- `aplus-05` — kompozisyon zaten yatay bir şerit; kırpma onu **iyileştirdi**
- `aplus-01` — yoğunluk solda, sağda geniş sakin alan; **sorunsuz**
- `aplus-06` — sol sakin alan korundu, alttaki zarf hafif kesildi; **kabul edilebilir**

Üçü de kullanılabilir. Daha iyisi isteniyorsa 3,23:1 oranında yeniden
üretilmelidir — bu **sizin kararınız**.

Görsellerin hepsi **metinsizdir**. Ticari metin (İngilizce, her satırın
bir `BRIEF §` dayanağı var) Amazon'un kendi başlık/gövde alanlarına
girer; kılavuzda kopyalanabilir hâlde.

## 7 · Ön kapak durumu

İkisi de işlendi: `1024×1536 → 4096×6144 (AI 4×) → 1800×2700 @ 300 dpi`.
`07_ASSETS/print/cover-option-0N-front.png`.

Gözle: ikisi de metinsiz ve yüksek kaliteli. **`cover-option-01`** üst ve
alt tipografi bantlarını belirgin şekilde daha iyi koruyor;
`cover-option-02`'de nesneler üst kenara kadar çıkıyor.

⚠ **Bu sanat SARMAL DEĞİLDİR** ve sarmala gerdirilmedi.

## 8 · Tam sarmal kapak promptları — eklendi

`wrap-cover-option-01` (“Sürekli Arşiv Yüzeyi”) ve `wrap-cover-option-02`
(“Gizli Bilginin Haritası”) kütüphaneye **§ 8** olarak eklendi
(üreteç: `04_BUILD/prompt_catalog.py`, elle HTML düzenlenmedi).

Her biri § 23 sözleşmesini taşır: konsept · üslup · kompozisyon ·
**arka / sırt / ön bölgesi** · güvenli alanlar · olumsuz prompt ·
beklenen en-boy · piksel yönergesi · ham dosya ve konumu · CLI tipografi
notu.

⭑ **Nihai piksel ölçüsü bilerek çivilenmedi** — sırt genişliği sayfa
sayısından türer ve iç blok dondurulmadı (K12). Bir denetim bunu zorlar:
sarmal promptuna `NNNN × NNNN` yazılırsa kapı kırmızıya döner (fikstürle
ölçüldü).

Sekiz yeni denetim eklendi (bölgeler · yasaklar · dosya adları · çivileme).

## 9 · Kitap üretimi durumu

| | |
|---|---|
| İç blok PDF (paperback) | ⛔ **YOK** |
| İç blok PDF (hardcover) | ⛔ **YOK** |
| Kindle | ⛔ **ÜRETİLMİYOR** — `editions.kindle.enabled=false`, BRIEF § 7 |
| Sarmal kapak PDF | ⛔ **YOK** — sanat bekleniyor |
| Sayfa modeli | 238 (ölçülen) |

**İç blok üretilmedi ve bu bilerek böyledir:** depoda `interior.py`,
`epub.py`, `covers.py` **yoktur** — bunlar Faz 6 teslimatıdır. Dizgi
dondurulmadı (K12). Var gibi göstermek, kurucuyu olmayan bir dosyayı
aramaya göndermek olurdu.

⚠ **BRIEF § 7 telif modeli 208 sayfaya dayanıyor, ölçülen 238.**
Sayfa sayısı değişirse basım maliyeti ve telif değişir — fiyat modeli
gözden geçirilmelidir.

## 10 · El kitabı durumu

- `08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` — 238 satır
- `08_OUTPUT/KDP_UPLOAD_GUIDE.html` — 30 KB · Türkçe · **çevrimdışı**

A–G bölümleri (Paperback · Hardcover · Kindle · A+ · Önizleme · Fiyat ·
Yayımlama), 13 adım, her adımda § 28'in yedi başlığı. Yapışkan gezinme ·
30 kopya düğmesi · 33 kutucuk · ilerleme sayacı · `localStorage`.
20 denetim yeşil; JS `node --check` ile doğrulandı.

⭑ **Hazırlık göstergesi elle yazılmaz** — `os.path.exists` ile doldurulur.
Bir denetim, olmayan bir dosyanın "hazır" görünmesini engeller.

> ⚠ Tarayıcı testi bu dosyada **yapılamadı** — Chrome uzantısı oturum
> ortasında bağlantıyı kaybetti. Yapısal denetim (kimlik tekilliği,
> düğme hedefleri, etiket bağlantıları, çıpalar, etiket dengesi) ve JS
> sözdizimi doğrulandı; **canlı tıklama testi yapılmadı.**

## 11 · Kurucuya kalan işler

**Bloklayıcı:**
1. Kanarya künyesini tazeleyin (§ 1) — tuz bende yok
2. Kapı 3-4-5 üretecinin `g5-013` kırığı — cevap değişimi buna bağlı
3. Cevap sızıntısı kararı (§ 1)

**Varlık:**
4. **14 levhayı yeniden üretin** (12 yanlış sözleşme + 2 sayım hatası)
5. `07_ASSETS/PLATE_VERIFICATION.html` ile kalan levhaları **sayın**
6. İki **sarmal kapak** sanatını üretin
7. İsteğe bağlı: 3 A+ modülünü 3,23:1 oranında yeniden üretin

**Yalnızca insanın yapabileceği (§ 31) — hiçbiri yapılmadı:**
KDP paneli · Previewer onayı · **yapay zekâ beyanı** · ISBN kararı ·
yazar biyografisi · **fiziksel POD provası (A9)** · Publish ·
A+ moderasyonu

## 12 · Değişmeyen

`externalValidation = founder_override_partial` · `sessionsPerformed = 0`
· `humanValidationPassed = false` · ölçülen öldürme kapısı **HARD-STOP**
· `06_REPORTS/solver/` **BOŞ**.

**Bu kitap hiçbir insanın elinde çözülmedi.**

---

# ⏳ KURUCUNUN TAM SARMAL KAPAK VARLIKLARI BEKLENİYOR

`codex-enigmatica-wrap-cover-option-01.png`
`codex-enigmatica-wrap-cover-option-02.png`
→ `07_ASSETS/raw/`

Bu iki dosya **yoktur** ve var gibi gösterilmemiştir. Geldiklerinde
"CONTINUE" deyin; nihai baskı kapakları o zaman kurulur.
