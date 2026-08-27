# NİHAİ SÜRÜM HAZIRLIK RAPORU — Codex Enigmatica

> **27 Ağustos 2026** · Kurucu yönergesi § 28
>
> # ⛔ HUMAN VALIDATION: NOT PERFORMED — FOUNDER OVERRIDE.
>
> Bu kitabı **hiçbir harici insan çözmedi.** Yapılan çözücü oturumu: **0**.
> Ölçülen öldürme kapısı kararı: **HARD-STOP**. İnsan doğrulaması geçti mi:
> **HAYIR**.
>
> Nihai paket, kurucunun bunu **bilerek** verdiği izinle üretildi. Bu bir
> **risk kabulüdür**, bir doğrulama değildir.
>
> ---
>
> ## KDP UPLOAD PACKAGE COMPLETE — HUMAN VALIDATION / ISBN / AI DECLARATION / PERMANENT DOMAIN REMAIN FOUNDER ACTIONS.

---

## 1 · Dört kategori — ve hiçbiri ötekinin yerine geçmez

| | |
|---|---|
| ✅ **ÇÖZÜLDÜ** | ajan yaptı, ölçüldü, kapı yeşil |
| ⚑ **KURUCU GEÇERSİZ KILMASI** | ölçüm değişmedi; kurucu bilerek devam etti |
| 🅕 **KURUCU EYLEMİ** | ajanın yapamayacağı iş |
| ⚠ **BİLİNEN RİSK** | ölçüldü, düzeltilmedi, saklanmıyor |

---

## 2 · Nihai çıktı — ÖLÇÜLEN

| Dosya | Ölçülen |
|---|---|
| `PAPERBACK/interior.pdf` | **274 sayfa** · 432 × 648 pt (6 × 9 in) · 70,4 MB |
| `PAPERBACK/cover.pdf` | 931,32 × 666 pt (**12,935 × 9,250 in**) · 33,5 MB |
| `HARDCOVER/interior.pdf` | **274 sayfa** · 432 × 648 pt · 67,3 MB |
| `HARDCOVER/cover.pdf` | 1035,49 × 750,02 pt (**14,382 × 10,417 in**) · 41,3 MB |
| `KINDLE/codex-enigmatica.epub` | **44,2 MiB (46,3 MB)** · 124 girdi · 19 bölüm · 99 levha |
| `KINDLE/cover.jpg` | **1600 × 2560** · yalnızca ÖN kapak |
| `APLUS/` | **6 modül** + `module-map.json` |

**Sağlama toplamları:** dört paketin dördü de doğrulandı —
PAPERBACK 3/3 · HARDCOVER 3/3 · KINDLE 3/3 · APLUS 7/7 · **hepsi OK**.

### 2.1 · İçerik

| | Ölçülen |
|---|---:|
| Bulmaca | **101** |
| Kapı | **5** |
| İpucu (3 kademe) | **303** |
| Basılan çözüm | **100** (son sorunun cevabı **basılmaz**) |
| Levha | **103** planlandı · **99** gömülü |
| Ticari yüzeyde Türkçe sözcük | **0** |

---

## 3 · Kapaklar — ve düzeltilen iki kusur

### ✅ ① Çözünürlük riski **KALKTI** (A16)

⚠ **Kusur:** kurucunun ham sarmal sanatı **1840 × 855** pikseldi. PDF
300 ppi'lık **piksel** taşıyordu ama arkasında o kadar **bilgi** yoktu:

| | önce | sonra |
|---|---:|---:|
| Ciltsiz doğal çözünürlük | **92,4 ppi** | **369,7 ppi** |
| Ciltli doğal çözünürlük | **82,1 ppi** | **328,3 ppi** |
| KDP hedefi | 300 ppi | 300 ppi |

Depo bunun için **zaten bir hat kurmuştu** (`ASSET_UPSCALING_REPORT.md` ·
Real-ESRGAN / `upscayl-standard-4x`) ve portföydeki diğer üç kitapta
kullanılmıştı; **Codex Enigmatica'ya hiç uygulanmamıştı.** Uygulandı:
`1840 × 855 → 7360 × 3420`.

> ⚠ **VE BUNUN NE OLMADIĞI:** Real-ESRGAN **makul detay üretir**,
> kaybolmuş detayı **geri getirmez**. Dosya artık gerçekten 300 ppi'dır ve
> bikübik büyütmeden belirgin olarak keskindir — ama **300 ppi'da
> ÜRETİLMİŞ bir sanatla aynı şey değildir.** Yönerge § 14 bunu açıkça
> istedi ve burada aynen duruyor.

### ✅ ② Ciltli **kâğıt çelişkisi** — ürünü bitirebilirdi

⚠ Yönerge § 11 "bayat 263 sayfa değerlerini kullanma" diyordu. Ölçünce
asıl tehlikenin **başka yerde** olduğu çıktı:

| | Sırt | Toleransa oranı |
|---|---:|---:|
| Sayfa farkı (263 → 274) | **+0,0248 in** | %39,7 — **içinde** |
| **Kâğıt farkı (beyaz → krem)** | **+0,0680 in** | **%109 — AŞIYOR** |

`metadata` ciltliyi **krem** listeliyordu; kurucunun KDP hesaplayıcısı
**beyaz** kâğıtla koşmuştu. Kapak beyaz matematiğiyle üretiliyor, ürün
krem diye listeleniyordu. **KDP toleransı ±0,0625 in** — yani yanlış
kâğıtla basılan kapak **reddedilir ya da sırt kayar**.

**Yapılan:** kâğıt artık **sürüm başınadır**. Ciltli = **beyaz**
(hesaplayıcının koştuğu kâğıt · yönerge § 11 onu yetke ilan ediyor),
ciltsiz = **krem**. Sırt artık hesaplayıcının kendi çıktısından ölçülen
**tahta payından** (0,18872 in) türetilir, "delta yaması" ile değil.
Kapak kâğıdı hesaplayıcıdan farklıysa kapı artık **KIRMIZI** yanar.

| | Ölçülen |
|---|---:|
| Ciltsiz sırt (krem · 274 s.) | **0,6850 in** |
| Ciltli sırt (beyaz · 274 s.) | **0,8058 in** |

### Tipografi

Deterministik vektör tipografi · **opak dikdörtgen yok** · hâle yalnızca
gerektiğinde. Her satır ya zeminle ≥ eşik karşıtlığa sahiptir **ya da**
hâlelidir, ve hâlenin **kenar** karşıtlığı ayrıca ölçülür. Başlık, alt
başlık, yazar, sırt ve arka kopya: **ölçüldü**.

⚠ **Kapaktaki başlık `Codex Enigmatica`dır** ve metadata'dan okunur —
başka bir projenin başlığı kopyalanmadı (§ 12).

---

## 4 · Kindle ve ekonomi

### ✅ Düzeltilen bir FORMÜL hatası

⚠ `economics.py` %70 telifini `0,70 × liste − teslimat` diye hesaplıyordu.
KDP'nin **kendi telif sayfası** tersini söyler ve birebir şöyledir:

> *"70% Royalty Rate x (List Price – applicable VAT - Delivery Costs) = Royalty"*
> → [KDP · eBook royalty](https://kdp.amazon.com/en_US/help/topic/G200634500)

Teslimat **orandan ÖNCE** düşülür. Bu dosyada fark küçük değildi:

| | yanlış | **doğru** |
|---|---:|---:|
| %70 planı telifi | 0,05 $ | **2,13 $** |
| Başabaş dosya boyutu | 23,3 MB | **33,3 MB** |

Öneri değişmedi — ama **yanlış bir sayı, doğru bir karara götürse bile
yanlıştır.**

### Ölçülen ekonomi

| Sürüm | Liste | Baskı maliyeti | **Telif** | Marj |
|---|---:|---:|---:|---:|
| Ciltsiz · 274 s. | 19,99 $ | 4,14 $ | **7,86 $** | %39,3 |
| Ciltli · 274 s. | 29,99 $ | 8,94 $ | **9,06 $** | %30,2 |

| Kindle | Ölçülen |
|---|---:|
| Dosya | **46,3 MB** |
| Liste | 9,99 $ |
| Teslimat ücreti (%70 planı) | 46,3 × 0,15 $ = **6,95 $** |
| Telif · **%70 planı** | **2,13 $** |
| Telif · **%35 planı** | **3,50 $** |
| ⭑ Ölçülen öneri | **%35** |
| %70'in kârlı olduğu sınır | **~33,3 MB** |

🅕 **Plan seçimi kurucuya aittir** ve KDP panelinde yapılır.

> ⚠ Baskı maliyetleri **KDP'nin fiyat modeline göre hesaplanmıştır**,
> alınmış bir teklif değildir. Yönerge § 24: *"Do not present projections
> as measured facts."*

---

## 5 · Doğrulama sayfası — GEÇİCİ Vercel durumu

### 5.1 · Basılan adres **DEĞİŞMEDİ**

```
valicepress.com/codex-enigmatica/verify
```

Basılı iç blokta **s. 273** (son yaprağın ön yüzü) · Kindle son bölümünde
**gerçek HTTPS bağ**, görünen metin birebir aynı.

⛔ **Geçici Vercel adresi kitaba BASILMADI** ve basılamaz. Bir önizleme
alan adı **kiracıdır**: proje adı değişince adres ölür, kitap ise
basılmıştır.

### 5.2 · ⚑ FOUNDER_TEMPORARY_VERCEL_OVERRIDE

| | |
|---|---|
| Geçici temel adres | `enterprise-web-site.vercel.app` |
| Yetkilendirme | **27 Ağustos 2026** · kurucu |
| Kitaba basılıyor mu | ⛔ **HAYIR** |
| Kalıcılık kuralı | üretim adresi `valicepress.com/...` **olmak zorundadır** |
| Kaldırma koşulu | kalıcı alan adı alınıp bağlandığında |

⭑ **KALICI KURAL ZAYIFLATILMADI.** `qa_verification.py` hâlâ
`*.vercel.app` adreslerini **basım adresi olarak REDDEDER** — ve
`selftest § ⑮` bunu geçici blok **varken bile** ispatlar.

### 5.3 · Canlı ölçüm — 27 Ağustos 2026

| Test | Sonuç |
|---|---|
| Sayfa açılıyor | ✅ **200** |
| HTTPS | ✅ zorunlu (`http` → **308**) |
| Doğru rota | ✅ `/codex-enigmatica/verify` |
| `GET` uç noktaya | ✅ **405** (`Allow: POST`) |
| `Cache-Control` | ✅ `no-store` |
| İstemcide cevap | ✅ **YOK** |
| İstemcide özet | ✅ **YOK** |
| İstemcide biber | ✅ **YOK** |
| *(901.852 bayt canlı HTML + 16 JS parçası tarandı)* | |
| **Doğru/yanlış cevap · hız sınırı** | ⛔ **ÖLÇÜLEMEDİ** — § 5.4 |

### 5.4 · ⚠ **BİLİNEN RİSK · KURUCU EYLEMİ** — Upstash yapılandırılmamış

Uç nokta canlıda **503 döndürüyor** ve bu **doğru davranıştır**:

```
[codex/verify] rate-limit backend unreachable; refusing: fetch failed
[rate-limit]   check failed; allowing request: fetch failed
```

**Ölçülen sebep:** üretimdeki `UPSTASH_REDIS_REST_URL` **URL değil** —
şeması yok, ana makine adı **0 karakter**; `UPSTASH_REDIS_REST_TOKEN`
**11 karakter**. Bunlar gerçek kimlik bilgisi değil, **89 gün önce
konmuş yer tutuculardır.**

⚠ **Kusur yeni değil ve bu oturumun ürünü değil.** Aynı sebeple sitenin
**çevre** hız sınırlayıcısı da üretimde **sessizce açık düşüyor** —
yani sitenin tamamı bugüne dek sınırsız istek kabul etmiş.

⭑ **Doğrulama uç noktası ise KAPALI düşer** — çünkü sınırlayıcısı olmayan
bir kâhin **sınırsız denemedir**. Yeşil bir test için bu davranış
**zayıflatılmadı** (yönerge § 25).

🅕 **Kurucu eylemi:** gerçek bir Upstash Redis oluştur, iki değişkeni
Vercel üretim ortamına gir, yeniden dağıt. Ondan sonra:

```
python3 04_BUILD/qa_verification.py --gate release --live
```

> `CODEX_VERIFY_PEPPER` ve `CODEX_VERIFY_DIGEST` **girildi** ve üretimde
> **Sensitive** olarak duruyor. Değerleri hiçbir yere yazdırılmadı.

---

## 6 · Kalite kapıları — § 20

| Kapı | Sonuç |
|---|---|
| `qa_language` | ✅ 8 · **ticari yüzeyde 0 Türkçe sözcük** |
| `qa_answerspace` | ✅ 10 · 101 bulmaca · **5.086 aday dize** elendi |
| `qa_solvability` | ✅ 11 · 404 çözüm adımı |
| `qa_uniqueness` | ✅ 9 · 404 alternatif aday |
| `qa_hints` | ✅ 9 · 303 ipucu |
| `qa_meta` | ✅ 29 · 5 harf · **cevap kitapta YOK** |
| `qa_effort` | ✅ 4 · 719 elle işlem |
| `qa_experience` | ✅ 19 |
| `qa_plate_readability` | ✅ 9 · 125 şekil |
| `qa_crossref` | ✅ 6 · 243 gönderme |
| `qa_editorial` | ✅ 8 |
| **`qa_verification`** | ✅ **29** |
| `metadata` | ✅ 7 · **2 kurucu alanı boş** |
| `covers` | ✅ ciltsiz 7 · ciltli **9** |
| `kindle` | ✅ **19** |
| `kdp_package` + preflight | ✅ **30** |
| **`selftest`** | ✅ **279** — bütün kapılar ısırıyor |
| **çözüm kanaryası** | ✅ 4 · **149 dosya** |
| **`qa_all.sh`** | ✅ **38 kapı · 0 kırmızı denetim** |

---

## 7 · Cevap sızıntısı — § 21

| Yüzey | Cevap | Biber | Özet |
|---|---|---|---|
| Ciltsiz iç blok + kapak | ✅ | ✅ | ✅ |
| Ciltli iç blok + kapak | ✅ | ✅ | ✅ |
| Kindle EPUB | ✅ | ✅ | ✅ |
| A+ `module-map.json` | ✅ | ✅ | ✅ |
| `metadata.json` | ✅ | ✅ | ✅ |
| KDP el kitabı + kılavuz | ✅ | ✅ | ✅ |
| `README.md` | ✅ | ✅ | ✅ |
| **Takip edilen 156 dosya** (kitap deposu) | ✅ | ✅ | ✅ |
| **Canlı site** (901.852 bayt) | ✅ | ✅ | ✅ |

### ⚠ Bir bulgu — **denetlendi ve elendi**

Site deposundaki `GORSEL_PROMPT_ENVANTERI_TR.md` cevabı **bir sözcük
olarak içeriyor** — ama bağlamı `business.webp` kategorisi için yazılmış
bir **stok görsel istemidir** ve dosyada *codex*, *enigmatica* ya da
bulmacaya dair **tek bir gönderme yoktur**.

Cevap **yaygın bir İngilizce isimdir**; bir bulmaca cevabının olağan
hâli budur. İlgisiz bir dosyadaki sözcüğü değiştirmek **güvenlik
tiyatrosu** olurdu ve cevabın güvenliği zaten sözcüğün nadirliğine değil
**biberli özete** dayanır. Kayda geçirildi, düzeltilmedi.

---

## 8 · Kurucuya ait — ve hiçbiri "tamam" işaretlenmedi

| # | İş | Kategori |
|---|---|---|
| 1 | **Harici insan doğrulaması** (A12b · 0/5 oturum) | ⚑ geçersiz kılındı · 🅕 |
| 2 | **ISBN** — KDP panelinde girilir | 🅕 |
| 3 | **YZ içerik beyanı** — KDP panelinde tamamlanır | 🅕 |
| 4 | **`valicepress.com` alan adı** — alım + bağlama | 🅕 (ödeme) |
| 5 | **Kalıcı üretim doğrulaması** | 🅕 · 4'e bağlı |
| 6 | **Upstash Redis** — gerçek kimlik bilgisi | 🅕 · § 5.4 |
| 7 | **Kindle telif planı** (%35 önerilir) | 🅕 |
| 8 | **KDP Previewer** — sayfa sayfa görsel onay | 🅕 |
| 9 | **Fiziksel POD provası** (A9) | 🅕 |
| 10 | Ciltli hesaplayıcının 274 sayfa + beyaz ile yenilenmesi (A15) | ⚠ tolerans **içinde** |
| 11 | 31 deterministik tabletin gravür üslubuna yükseltilmesi (A17) | ⚠ bütçe |
| 12 | **Yayımlama** | 🅕 |

---

## 9 · Bilinen riskler — ölçüldü, saklanmıyor

| Risk | Durum |
|---|---|
| **İnsan doğrulaması yok** | ⚑ kurucu geçersiz kılması · ölçüm **HARD-STOP** olarak duruyor |
| **Canlı uç nokta çalışmıyor** | ⚠ Upstash yer tutucu · kapalı düşüyor (**doğru davranış**) |
| **Sitenin çevre hız sınırı açık düşüyor** | ⚠ aynı sebep · bu oturumun ürünü değil |
| **Kapak sanatı yükseltilmiş** | ⚠ 300 ppi **gerçek**, ama üretilmiş detay ≠ çekilmiş detay |
| **Ciltli hesaplayıcı 263 s. ile koştu** | ⚠ sapma toleransın %39,7'si · sırt tahta payından türetildi |
| **31 tablet üslupça sade** | ⚠ diğer 72 gravürden ayrışıyor (A17) |
| **Baskı maliyetleri model** | ⚠ KDP fiyat modelinden hesaplandı, teklif değil |

---

## 10 · Durdurma koşulu — § 29

| | |
|---|---|
| Tam İngilizce ticari kitap | ✅ **0** Türkçe sözcük |
| Ciltsiz | ✅ 274 s. |
| Ciltli | ✅ 274 s. |
| Kindle | ✅ 46,3 MB |
| A+ | ✅ 6 modül |
| Nihai kapaklar | ✅ ciltsiz + ciltli sarmal · Kindle ön |
| **Geçici Vercel doğrulaması** | ⬍ **sayfa canlı · uç nokta Upstash'e bağlı** |
| Kalıcı basılı adres doğru | ✅ `valicepress.com/...` |
| KDP preflight | ✅ 30 denetim |
| Cevap sızıntısı temiz | ✅ |
| Dil temiz | ✅ |
| Sağlama toplamları | ✅ 16/16 |
| Tam CI | ✅ |
| El kitabı güncel | ✅ |
| Nihai sert denetim | ✅ bu belge |

### ⛔ Yapılmayanlar

KDP'ye **yüklenmedi** · **yayımlanmadı** · prova **sipariş edilmedi** ·
alan adı **satın alınmadı** · ISBN **girilmedi** · YZ beyanı
**verilmedi** · insan doğrulaması **uydurulmadı**.

---

> # KDP UPLOAD PACKAGE COMPLETE — HUMAN VALIDATION / ISBN / AI DECLARATION / PERMANENT DOMAIN REMAIN FOUNDER ACTIONS.
