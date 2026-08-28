# KDP RET ONARIM RAPORU — Codex Enigmatica

> **28 Ağustos 2026** · Kurucu yönergesi § 15
>
> # KDP REJECTION REPAIRED — REVISED UPLOAD PACKAGE READY
>
> ⛔ **HUMAN VALIDATION: NOT PERFORMED — FOUNDER OVERRIDE.**
> Yüklenmedi · yayımlanmadı.

---

## 1 · Amazon'un tam olarak ne dediği

Kaynak: kurucunun ilettiği KDP e-postası
(*"Attention needed: Please review your title, Codex Enigmatica"*).

**Kapak**
> *"The front cover contains text/graphics that extend beyond the trim
> line and may be cut off during production. Please make sure that all
> elements intended to be viewable appear at least 0.716in (18.175mm)
> away from the outside edges. All front cover text must also stop at
> least 0.4in (10mm) away from the edge of the spine."*

**İç blok**
> *"Fix all conversion errors in the text and images in your manuscript
> file. Example errors include question marks or boxes in the place of
> text, or boxes with an "X" inside where images should be. See examples
> on PDF page(s) 135."*

> ⭑ **VE YEREL KAPILARIN HEPSİ YEŞİLDİ.** Sebep utandırıcı ölçüde basit:
> hiçbiri bu soruları sormuyordu. `covers.py` yalnızca **karşıtlık**
> ölçüyordu — yazının **okunur** olduğunu doğruluyor, **sayfada
> kaldığını** hiç sormuyordu.

---

## 2 · Etkilenen sayfalar — bildirilen ve GERÇEK

| | KDP'nin saydığı | Ölçülen gerçek |
|---|---|---|
| Kapak | "ön kapak" | ciltsiz **3 sözcük** · **ciltli 1 sözcük** (ciltli hiç bildirilmemişti) |
| İç blok | "s. 135" | gömülmeyen yazı tipi **274 sayfanın 274'ünde** · eksik glif **1 sayfada** |

⚠ **KDP bir örnek gösterir, envanter vermez.** Bir önceki turda da
"beş sayfa" denmiş, ölçüm 140 sayfa bulmuştu. Bildirilen sayfayı
düzeltip durmak, kusurun kendisini bırakmaktır.

---

## 3 · Kök sebepler

### ① ⛔ `Helvetica` GÖMÜLÜ DEĞİLDİ — 274 sayfanın hepsinde

```
Helvetica   Type 1   WinAnsi   emb: no   sub: no   uni: no
```

reportlab kanvası varsayılan yazı tipi olarak `Helvetica` ile açılır ve
o ad, **hiç yazı basılmasa bile** her sayfanın kaynak sözlüğüne yazılır.
KDP bütün yazı tiplerinin gömülü olmasını ister; gömülü olmayan bir tip
okuyucuda **ikame edilir** — ve ikame, Amazon'un tarif ettiği şeyi
üretir: *"question marks or boxes in the place of text."*

**Onarım (kaynak düzeyinde):** `rl_config.canvas_basefontname = "Body"`.
Varsayılan yamalanmadı, **değiştirildi** — Helvetica artık hiç doğmuyor.

### ② ⛔ `⚠` (U+26A0) SERİF YÜZLERİNDE YOKTU

| Yüz | Glif |
|---|---|
| DejaVu Sans **Mono** | ✅ var |
| DejaVu **Serif** / Bold / Italic | ⛔ **YOK** |

Gövde metni serif dizilir. reportlab eksik glifi `.notdef` çizer:
sayfada boş kutu.

⭑ **Ve karakter metin çıkarımından TAMAMEN DÜŞER.** `pdftotext` ile
bakan biri kusuru **göremez** — sayfada 8 karakter vardır, çıkarımda 0.
Bu yüzden yeni denetim çıktıda değil **kaynakta**, basılacağı yüze
karşı yapılır.

**Onarım:** işaret basılı şifre referansından kaldırıldı (bir bulmaca
sembolü değil, editoryal vurguydu; cümlenin vurgusu zaten kendi büyük
harflerinde) **ve** dizgi anına bir koruma kondu: bir yüzün taşımadığı
glif basılmaya kalkılırsa **üretim durur**.

### ③ ⛔ KAPAK GÜVENLİ ALANI YANLIŞ YERDEN ÖLÇÜLÜYORDU

`SAFE = 0.25` **kesim çizgisinden** ölçüyordu. KDP **dış kenardan**
ölçer. 0,125" taşmayla birlikte:

```
0,25" (kesimden)  =  0,375" (dış kenardan)     KDP istiyor: 0,716"
```

İstenenin **yarısından azı**.

### ④ ⛔ ÖLÇÜM VE ÇİZİM AYRI YERLERDEYDİ — ve bu kusuru GİZLEDİ

İlk onarımdan sonra kapak *"ölçüldü, temiz"* diyordu ama **nihai PDF
hâlâ taşıyordu**: `plan()` yeni bandın ortasına ölçüyor, çizim
döngüsü ise hâlâ eski panel ortasını (`fcx`) kullanıyordu.

⭑ Bu tam olarak deponun daha önce dizgi yardımcılarında yaşadığı ders:
**aynı yerleşimi iki yerde tutmak, birini düzeltip ötekini unutmaktır.**
Çizim artık koordinatı **ölçülen kayıttan** okur; tek kaynak.

### ⑤ ⛔ CİLTLİ KAPAK CİLTSİZİN SAYFA SAYISINI OKUYORDU

`covers.py` her zaman `interior.json`u (ciltsiz) okuyordu. İki cilt
274'te eşitken **görünmezdi**. Ciltli 276'ya çıkınca ciltli kapak hâlâ
274'e göre sırt hesapladı: **0,8058"** — olması gereken **0,8103"**.
Sessiz, ölçülene kadar görünmez ve **baskıda yanlış**.

---

## 4 · Yeni kapak ölçüleri — **NİHAİ PDF'TEN** okundu

Ölçüm `pdftotext -bbox` ile nihai PDF'in **metin katmanından** yapıldı;
"guide'ların içinde duruyor gibi" değil (yönerge § 8).

| | Ciltsiz | Ciltli |
|---|---:|---:|
| Tam kapak | 12,935 × 9,250 in | **14,386** × 10,417 in |
| Sırt | 0,6850 in | **0,8103 in** (274 → 276 sayfa) |
| Ölçülen sözcük | 156 | 156 |
| **KDP eşiğine göre en dar pay** | **+0,060 in** | **+0,092 in** |
| İhlal eden sözcük | **0** | **0** |

**Uygulanan eşikler** — Amazon'un kendi sayıları, üstüne 0,06" pay:

| | |
|---|---|
| Dış kenar | **0,716 in** |
| Sırt (ön kapak metni) | **0,40 in** |

⚠ **Ciltli için sayı kopyalanmadı, türetildi** (yönerge § 9): ciltli
kapakta dış 0,591" tahtanın arkasına **sarılır** ve görünmez; üstüne
hesaplayıcının kendi kenar payı (0,125") biner → **0,716"**. İki
bağımsız yol aynı sayıya çıkar ama ayrı hesaplanır.

**Korunanlar:** sanat · görsel hiyerarşi · tipografi · sırt ortalaması ·
arka kapak okunurluğu. **Opak beyaz kutu eklenmedi.** Kurucunun sanatı
yeniden üretilmedi — gerekmedi.

---

## 5 · Yeni kurucu varlıkları — § 2

Projeye konan iki dosya incelendi (**ada güvenilmedi, açıldı**):

| Dosya | Gerçekte ne |
|---|---|
| `Screenshot from 2026-08-28 12-11-33.png` | KDP ret e-postasının ekran görüntüsü |
| `Screenshot from 2026-08-28 12-11-36.png` | aynı e-posta · konu satırı görünür |

⭑ **İkisi de kapak varlığı DEĞİLDİR.** Yeni bir kapak sanatı
teslim edilmemiştir; mevcut sanat korunmuştur ve doğru olan buydu.

> ⚠ **VE BİR ŞEY ORTAYA ÇIKTI:** e-postanın konu satırı **bir ISBN
> taşıyor** — yani KDP artık bu başlığa bir numara atamış.
>
> ⛔ **Numara bu depoya HİÇBİR YERE yazılmadı** — ne yapılandırmaya, ne
> bu rapora. İki sebep:
>
> 1. Bir **ekran görüntüsünden** okunan, geri alınamaz bir tanımlayıcıyı
>    tek hane yanlış aktarmak düzeltilemez bir hatadır.
> 2. `validate_structure` zaten **doğrulanmamış ISBN'i takip edilen
>    hiçbir dosyada kabul etmez** — ve bu raporun ilk taslağını da tam
>    olarak bu yüzden reddetti. Kapı haklıydı; rapor düzeltildi.
>
> **Kurucu numarayı kendi KDP panelinden okur ve kaydeder.**

---

## 6 · Yazı tipi denetimi — § 4

| | Önce | Sonra |
|---|---|---|
| Gömülü olmayan yazı tipi | **1** (`Helvetica`) | **0** ✅ |
| Gömülü + alt küme | 4 | **4** ✅ |
| Kaynaktaki ASCII dışı karakter | 67 | 67 |
| Hiçbir yüzde glifi olmayan | 0 | **0** ✅ |
| **Serif yüzlerde eksik** | **1** (`⚠`) | **0** ✅ |

⭑ **Sembol AYIKLANMADI, DENETLENDİ** (yönerge § 4). Kitabın 67 ASCII
dışı karakterinin **66'sı bulmaca sembolüdür ve hepsi korunmuştur** —
kutu çizgileri, `■ □ ◆ ○ ● ▲ ▶ ≈ → ↓ ░ ▓ ╱ ╲`… Hiçbir bulmaca
zayıflatılmadı. Kaldırılan tek işaret editoryal bir vurguydu.

---

## 7 · Görsel denetimi — § 5

| | Ölçülen |
|---|---|
| Levha PNG'si (disk) | **103** |
| `plateId` taşıyan bulmaca | 94 → **hepsinin dosyası var** ✅ |
| Dosyası eksik `plateId` | **0** ✅ |
| Gömülü görsel XObject | **99** (94 bulmaca + 5 kapı açılışı) |
| Bozuk / sıfır boyutlu | **0** ✅ |
| Yer tutucu ("X" kutusu) | **0** ✅ |

`plateId` taşımayan 7 bulmaca (`g1-004 · g1-007 · g1-011 · g1-016 ·
g2-006 · g2-011 · g2-016`) **bilerek** metin şekillidir — eksik görsel
değildir.

---

## 8 · Sayfa sayfa dönüşüm denetimi — § 3 · § 7

274 + 276 sayfanın **tamamı** tarandı.

| Denetim | Ciltsiz | Ciltli |
|---|---|---|
| İkame karakteri (U+FFFD) | 0 ✅ | 0 ✅ |
| Sözcük içinde `?` | 0 ✅ | 0 ✅ |
| Gömülmeyen yazı tipi | 0 ✅ | 0 ✅ |
| Glifi olmayan basılı karakter | 0 ✅ | 0 ✅ |
| Bozuk görsel | 0 ✅ | 0 ✅ |

### ⚠ Bir yanlış pozitif — ve dedektör KESKİNLEŞTİRİLDİ

İlk tarama `□` (U+25A1) için **8 uyarı** verdi. İnceleme: sekizinin
sekizi de **yazılmış bulmaca içeriğidir** (cevap kutuları `□ □ □`,
s. 20 ve s. 224), kaynakta birebir 8 kez geçer ve **her yüzde glifi
vardır**.

⭑ Ölçüt görüntü değil, **basılacağı yüzde glif olup olmadığıdır.**
Dedektör körleştirilmedi (§ 13): `□` hata listesinden çıkarılmadı —
hata listesi zaten yalnızca *gerçek* ikame karakterlerini içerir, ve
ayrı bir kapsama denetimi her karakteri yüzüne karşı ölçer.

Aynı biçimde, `printed: false` işaretli aday çizelgesi kapsama
denetiminden **açıkça** çıkarıldı: o çizelge bir ispat yüzeyidir,
kitaba hiç girmez. Muafiyet **dar** tutuldu — "muhtemelen basılmaz"
diye bir kural yoktur.

---

## 9 · Sayfa 135 — § 6

Yüklenen dosyada s. 135, `g3-018`in **şekil sayfasıydı**: kutu
çizgileri, `■`, `≈`, `→`, `·`. Yeniden üretimden sonra içerik bir sayfa
kaydı (⚠ kaldırılması satır sonunu değiştirdi) ve o sayfa şimdi
**s. 136**.

**İkisi de yüksek çözünürlükte görsel olarak denetlendi:**

| | Sonuç |
|---|---|
| s. 135 (yeni: `g3-018` levha sayfası) | ✅ halka gravürü tam, temiz |
| s. 136 (eski 135: şekil sayfası) | ✅ kutu · `■` · `≈` · `→` hepsi basılı |
| s. 270 (şifre referansı — eski kusur) | ✅ `.notdef` kutusu yok |

> ⚠ **Dürüst sınır:** KDP'nin dönüştürücüsü burada koşturulamaz. Bu
> yüzden "KDP'nin s. 135'te gördüğü şey buydu" diye bir iddia
> yazılmıyor. Yazılabilecek olan şudur: **Amazon'un tarif ettiği iki
> kusur sınıfı da dosyada nesnel olarak vardı** (gömülmeyen yazı tipi ·
> eksik glif), ikisi de **ölçülerek** bulundu, kaynakta onarıldı ve
> ölçülerek doğrulandı.

---

## 10 · Ciltsiz durumu

| | |
|---|---|
| Sayfa | **274** (değişmedi) |
| İç kenar payı | 0,625" (KDP asgarisi 0,500") |
| En dar baskı payı | **+0,103 in** |
| Kapak | 12,935 × 9,250 in · sırt 0,6850" |
| Kapak en dar pay | **+0,060 in** |
| Yazı tipi | 4 · hepsi gömülü |
| Doğrulama adresi | **s. 274** (son yaprak) |

## 11 · Ciltli durumu

| | |
|---|---|
| Sayfa | **276** ⚠ (274 → 276) |
| İç kenar payı | 0,750" (KDP asgarisi 0,625") |
| En dar baskı payı | **+0,103 in** |
| Kapak | **14,386** × 10,417 in · sırt **0,8103"** |
| Kapak en dar pay | **+0,092 in** |
| Doğrulama adresi | **s. 275** / 276 (son yaprak) |

⚠ **Neden 276:** `⚠` kaldırılınca şifre referansında bir satır sonu
değişti ve ciltlinin **dar** gövdesinde (4,875") bir sayfa sınırını
aştı; çift sayfa kuralı bir sayfa daha ekledi. Bağımlı olan her şey
yeniden hesaplandı: sırt · kapak genişliği · baskı maliyeti · telif ·
arka kapaktaki sayfa sayısı.

## 12 · Kindle durumu

| | |
|---|---|
| EPUB | **46,3 MB** · 19 bölüm · 99 levha |
| Kapak | 1600 × 2560 · **yalnızca ön** |
| Baskıya ait öğe (sırt/arka/barkod/taşma) | **yok** ✅ |

Kindle'a baskı güvenli alanı **uygulanmadı** (yönerge § 9) — ön kapak
ayrı denetlendi.

---

## 13 · KDP preflight — § 12

```
[x] margin ihlali yok            ciltsiz 0 · ciltli 0
[x] güvenli alan ihlali yok      +0,060" · +0,092"
[x] kesim dışında metin yok      NİHAİ PDF'te ölçüldü
[x] sırta çok yakın metin yok    KDP 0,40"
[x] eksik glif yok               67 ASCII dışı karakter denetlendi
[x] '?' yer tutucu yok
[x] 'X' görsel yer tutucu yok
[x] boş/bozuk görsel yok
[x] bütün yazı tipleri gömülü    4 tip · 0 gömülmeyen
[x] bütün görseller gömülü       99
[x] bütün sayfalar basılıyor     274 · 276
[x] metadata uyuşuyor            sayfa sayısı SÜRÜM BAŞINA
[x] sağlama toplamları           16/16
```

### Yeni kalıcı kapılar

| Kapı | Ne ölçer |
|---|---|
| `qa_kdp_conversion.py` | yazı tipi gömme · glif kapsaması · ikame karakteri · görsel · **nihai PDF'te kapak güvenli alanı** |
| `qa_print_margins.py` | (önceki tur) her sayfanın gerçek mürekkep kutusu |
| `interior.assert_glyphs` | **dizgi anında** eksik glif → üretim durur |

`selftest` **289 → 302 denetim**.

---

## 14 · Git / CI

Bu raporun altındaki commit'te kaydedilir. **Yerel yeşil, gerçek
GitHub Actions yerine geçmez** (yönerge § 17).

---

## 15 · Kalan bloklayıcılar

| # | Konu | Durum |
|---|---|---|
| 1 | **KDP Previewer'ın yeniden koşturulması** | 🅕 **kurucu** — bu onarım Previewer değildir |
| 2 | KDP'nin atadığı ISBN'in kaydı | 🅕 kurucu panelden okur (§ 5) |
| 3 | YZ içerik beyanı | 🅕 kurucu |
| 4 | `valicepress.com` alan adı | 🅕 kurucu |
| 5 | Upstash üretim kimlik bilgisi | 🅕 kurucu · uç nokta 503 |
| 6 | Harici insan doğrulaması | ⚑ kurucu geçersiz kılması · **0 oturum** |
| 7 | Ciltli hesaplayıcı 276 + beyaz ile yenilenmeli | ⚠ sapma toleransın %41'i (A15) |

> ⭑ **EN ÖNEMLİSİ:** bu rapor kitabın KDP'yi **geçeceğini** iddia etmez.
> İddia ettiği şudur: Amazon'un adını koyduğu iki kusur sınıfı dosyada
> **nesnel olarak vardı**, kökünden onarıldı ve **ölçülerek** doğrulandı.
> Kararı yine **gerçek KDP Previewer** verir.
