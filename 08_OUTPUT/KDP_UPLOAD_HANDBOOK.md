# KDP YÜKLEME EL KİTABI — Codex Enigmatica

> ⚠ **BU BELGE BİR ŞEYİN YAYIMLANDIĞINI İDDİA ETMEZ.**
> Aşağıdaki her dosya durumu üretim anında dosya sistemine
> bakılarak doldurulmuştur. `Publish` düğmesine yalnızca
> kurucu basar.

## 0 · Hazırlık

| | |
|---|---|
| Ölçülen sayfa | 274 |
| Bulmaca · kapı · ipucu | 101 · 5 · 303 |
| İşlenmiş levha | 103 / 103 |
| İşlenmiş ön kapak | 2 / 2 |
| İşlenmiş A+ | 6 / 6 |
| Ajan tarafından hazır adım | 10 / 24 |

## 0.0 · ⛔ İNSAN DOĞRULAMASI YAPILMADI

> **HUMAN VALIDATION: NOT PERFORMED — FOUNDER OVERRIDE.**
>
> Bu kitabı **hiçbir harici insan çözmedi.** Yapılan çözücü
> oturumu: **0**. Ölçülen öldürme kapısı kararı:
> **HARD-STOP**. İnsan doğrulaması geçti mi: **HAYIR**.
>
> Nihai paket, kurucunun **bunu bilerek** verdiği izinle
> üretildi (2026-08-27). Bu bir **risk kabulüdür**, bir doğrulama
> değildir — ve hiçbir rapor onu doğrulama diye yazmaz.

## 0.1 · ⭑ DOĞRULAMA SAYFASI ⭑

> ⚠ **ALAN ADI HENÜZ KALICI DEĞİL.**
>
> Kalıcı adres — ve **kitaba basılan** adres — şudur:
> `valicepress.com/codex-enigmatica/verify`
>
> Bu adres **henüz yayında değildir**: alan adı alınmadı.
> O güne kadar doğrulama sistemi **geçici olarak** şurada
> canlı test edilir: `enterprise-web-site.vercel.app`
>
> ⛔ **Geçici adres kitaba BASILMAZ** ve basılmadı. Bir
> önizleme alan adı kiracıdır; proje adı değişince ölür,
> kitap ise basılmıştır.
>
> ⭑ **Üretim kalıcı olarak yayına alınmış SAYILMAZ**
> ta ki kurucu `valicepress.com` alan adını alıp bağlayana
> kadar.

> ⛔ **BASKIYA HAZIR DEĞİL — VE BU BİR BİÇİM SORUNU DEĞİL.**
>
> Kitap son yaprağına bir adres **basar**. O adres canlı
> değilken basmak, okura ölü bir kapı vermektir; ve alan adı
> başkasının eline geçerse **satılmış her nüsha** okuru
> yabancı bir siteye gönderir. Basılmış bir URL
> **düzeltilemez.**

| | |
|---|---|
| Kitaba BASILAN adres (kalıcı) | valicepress.com/codex-enigmatica/verify |
| Alan adı kurucunun elinde | ⛔ HAYIR |
| Kalıcı alan adı yayında | ⛔ HAYIR |
| Kalıcı adres canlı doğrulandı | ⛔ HİÇ |
| — — — | — — — |
| GEÇİCİ doğrulama adresi | enterprise-web-site.vercel.app |
| Geçici adres KİTABA BASILIYOR mu | ⛔ HAYIR |
| Geçici sayfa canlı | ✅ EVET |
| Geçici uç nokta çalışıyor | ⛔ HAYIR — UPSTASH_REDIS_REST_URL/TOKEN üretimde geçersiz — ana makine adı DNS'te çözülmüyor |

`python3 04_BUILD/qa_verification.py --gate release --live`
koşturun ve **kararı okuyun**. Üçü de yeşil olmadan
`release` kapısı **KIRMIZIDIR**.

## 1 · ⭑ YALNIZCA KURUCUNUN YAPABİLECEĞİ İŞLER ⭑

Ajan bunları **yapmadı ve yapamaz**. Yapıldığını iddia eden
bir rapor yanlıştır.

- **KDP hesabına giriş ve panel kullanımı** — Ajan tarayıcıda hesabınıza giremez, giremeyecektir.
- **Previewer'da sayfa sayfa görsel onay** — Bir insanın bakması gerekir; ölçüm bunu değiştirmez.
- **⭑ YAPAY ZEKÂ İÇERİK BEYANINI KDP PANELİNDE SİZ TAMAMLARSINIZ ⭑** — Hukuki bir beyandır ve yalnızca siz verebilirsiniz. Ajan bir değer UYDURMADI ve uydurmayacak: `metadata.json → founderPending.aiDisclosureConfirmed` HÂLÂ false ve öyle kalacak. KDP, YZ-ÜRETİMİ metin/görsel/çevirinin bildirilmesini ister; YZ-DESTEKLİ içerik için bildirim gerekmez — ayrımı siz yaparsınız.
- **⭑ ISBN'İ KDP PANELİNDE SİZ GİRERSİNİZ ⭑** — `founderPending.isbn` BOŞ ve bilerek boş. Ajan ISBN üretmedi, tahmin etmedi, yeniden kullanmadı ve YER TUTUCU BASMADI — basılmış yanlış bir ISBN geri alınamaz. KDP ücretsiz ISBN mi, kendi ISBN'iniz mi: karar sizin ve panelde girilir.
- **⭑ KINDLE TELİF PLANINI SİZ SEÇERSİNİZ ⭑** — Ölçüm: EPUB 46,3 MB → %70 planında teslimat ücreti 6,95 $ (46,3 × 0,15 $) ve telif 2,13 $; %35 planında telif 3,50 $. Yani BU DOSYADA %35 daha çok kazandırır ve başabaş nokta ~33,3 MB'dır. Formül KDP'nin kendi telif sayfasından alındı: %70 × (liste − KDV − teslimat). Seçim panelde sizindir.
- **Yazar biyografisi** — `founderPending.authorBio` boş. Yer tutucu basmak geri alınamaz.
- **Fiziksel POD provası (A9)** — Gravürlerin nokta yayılması altındaki davranışı YALNIZCA basılı provada ölçülür. Ekranda kusursuz görünen levha kâğıtta kapanabilir.
- **⭑ DOĞRULAMA ALAN ADININ KAYDI ⭑** — Kitap `valicepress.com/codex-enigmatica/verify` adresini SON YAPRAĞINA BASAR. Alan adı 26 Ağustos 2026'da KAYITSIZ ölçüldü (~11,25 $/yıl) — yani serbest, ama BİZİM DEĞİL. Alan adı kaydı bir ÖDEME işlemidir ve ajan yapamaz. ⚠ BASILMIŞ BİR URL DÜZELTİLEMEZ: alan adı başkasının eline geçerse satılmış her nüsha okuru yabancı bir siteye gönderir.
- **⭑ DOĞRULAMA SAYFASININ YAYINA ALINMASI ⭑** — Vercel projesi şu an `live: false` ve üretim hedefi `target: null` — site HİÇBİR YERDE yayında değildir. Sayfa yayına alınmadan kitap BASILAMAZ; `qa_verification.py` `release` kapısını KIRMIZI tutar.
- **⭑ DOĞRULAMA SIRLARININ VERCEL'E GİRİLMESİ ⭑** — `CODEX_VERIFY_PEPPER` ve `CODEX_VERIFY_DIGEST`. Üretimi: `node scripts/codex-verify-digest.mjs` — cevabı STDIN'den okur, dosyaya ve kabuk geçmişine YAZMAZ. ⚠ Sunucuda düz cevap saklanmaz; saklanan şey biberli SHA-256 özetidir. İkisi de depoda DEĞİLDİR.
- **Publish düğmesi** — Yayımlama kararı kurucuya aittir.
- **A+ içeriğinin moderasyona gönderilmesi** — Amazon insan moderasyonu uygular; ajan gönderemez.

## 01 · KDP'Yİ AÇMADAN ÖNCE

### 🔵 Paketi doğrula (sağlama toplamları)

| | |
|---|---|
| NE YAPACAĞIM | Dört paketin dördü de sağlama toplamı taşır. Yüklemeden önce bozulmadıklarını DOĞRULAYIN — yarım inen bir PDF'i KDP kabul edip bozuk basar. |
| KDP'DE NEREYE | Terminal (KDP'de değil) |
| NE GİRECEĞİM | cd 08_OUTPUT/PAPERBACK && sha256sum -c SHA256SUMS |
| HANGİ DOSYA | `08_OUTPUT/*/SHA256SUMS` |
| NE KONTROL EDECEĞİM | Dört dizinde de her satır 'OK' demeli. Tek bir FAILED varsa YÜKLEMEYİN. |
| BAŞARILI OLURSA | 16 dosyanın 16'sı OK. |
| DURUM | **HAZIR** |

### 🟢 ISBN kararını verin

| | |
|---|---|
| NE YAPACAĞIM | KDP ÜCRETSİZ ISBN verir (yalnızca Amazon'da geçerlidir) ya da kendi ISBN'inizi girersiniz (her yerde geçerli, ücretli). Depo hiçbir değer TAŞIMIYOR ve taşımayacak. |
| KDP'DE NEREYE | Paperback/Hardcover Details → ISBN → 'Get a free KDP ISBN' veya 'Use my own ISBN' |
| NE GİRECEĞİM | ⛔ AJAN GİRMEDİ — kurucu panelde seçer |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Ciltsiz ve ciltli AYRI ISBN ister. Kindle ISBN İSTEMEZ (ASIN alır). |
| BAŞARILI OLURSA | Her baskı sürümünün kendi ISBN'i olur. |
| DURUM | **BEKLIYOR** |

### 🟢 Yapay zekâ içerik beyanını hazırlayın

| | |
|---|---|
| NE YAPACAĞIM | KDP, YZ-ÜRETİMİ metin/görsel/çevirinin bildirilmesini ister; YZ-DESTEKLİ içerik için bildirim gerekmez. Ayrımı yalnızca siz yapabilirsiniz — bu hukuki bir beyandır. |
| KDP'DE NEREYE | Details ekranı → 'Did you use AI tools...?' |
| NE GİRECEĞİM | ⛔ AJAN BEYAN VERMEDİ — kurucu panelde doldurur |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | `metadata.json → founderPending.aiDisclosureConfirmed` HÂLÂ false ve öyle kalacak. Bir ajan sizin adınıza beyan veremez. |
| BAŞARILI OLURSA | Beyan panelde kaydedilir. |
| DURUM | **BEKLIYOR** |

## 02 · PAPERBACK

### 🔵 İç blok

| | |
|---|---|
| NE YAPACAĞIM | 6 × 9 in trim · KREM kâğıt · siyah mürekkep · 274 sayfa (ÖLÇÜLDÜ). |
| KDP'DE NEREYE | Bookshelf → Create → Paperback → Paperback Content → Manuscript → Upload paperback manuscript |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/PAPERBACK/interior.pdf` |
| NE KONTROL EDECEĞİM | Previewer'da: iç kenar payı (gutter) hiçbir levhayı kesmemeli · taşma (bleed) yok, iç blok taşmasızdır · sayfa numaraları 3. sayfadan başlar · SON YAPRAK doğrulama adresini taşır (s. 273). |
| BAŞARILI OLURSA | 'Manuscript uploaded successfully' ve Previewer açılır. |
| DURUM | **HAZIR** |

### 🔵 Sarmal kapak

| | |
|---|---|
| NE YAPACAĞIM | Arka + sırt + ön, TEK PDF. Tam kapak 12.935 × 9.250 in · sırt 0.6850 in (KREM kâğıt, 274 sayfadan türetildi). |
| KDP'DE NEREYE | Paperback Content → Book Cover → Upload a cover you already have (print-ready PDF) |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/PAPERBACK/cover.pdf` |
| NE KONTROL EDECEĞİM | Sırt yazısı ORTALANMIŞ olmalı · sağ altta barkod alanı BOŞ bırakıldı (KDP kendi barkodunu oraya basar) · güvenli alan içinde hiçbir metin kesilmemeli. |
| BAŞARILI OLURSA | Kapak kabul edilir, Previewer açılır. |
| DURUM | **HAZIR** |

## 03 · HARDCOVER

### 🔵 İç blok (ciltli)

| | |
|---|---|
| NE YAPACAĞIM | Aynı içerik, ciltli iç pay kurallarıyla yeniden dizildi · 274 sayfa · iç kenar payı ciltsizden GENİŞTİR. |
| KDP'DE NEREYE | Create → Hardcover → Hardcover Content → Manuscript |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/HARDCOVER/interior.pdf` |
| NE KONTROL EDECEĞİM | ⛔ CİLTSİZ İÇ BLOĞUNU BURAYA YÜKLEMEYİN — iç payları farklıdır ve ciltli baskıda metin cilde gömülür. |
| BAŞARILI OLURSA | Ciltli Previewer açılır. |
| DURUM | **HAZIR** |

### 🔵 Sarmal kapak (ciltli)

| | |
|---|---|
| NE YAPACAĞIM | Tam kapak 14.386 × 10.417 in · sırt 0.8103 in · menteşe (hinge) 0.394 in · sarma (wrap) 0.591 in. ⚠ KÂĞIT: BEYAZ. |
| KDP'DE NEREYE | Hardcover Content → Book Cover → Upload a cover you already have |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/HARDCOVER/cover.pdf` |
| NE KONTROL EDECEĞİM | ⛔ CİLTSİZ KAPAK GEOMETRİSİNİ KULLANMAYIN. Ciltli kapak tahtası trimden BÜYÜKTÜR (6.197 × 9.236 in) ve ayrıca menteşe payı vardır. Geometri kurucunun KDP hesaplayıcı ekran görüntüsünden OKUNDU (03_COVER/HARDCOVER_CALCULATOR_VALUES.md). |
| BAŞARILI OLURSA | Ciltli kapak kabul edilir. |
| DURUM | **HAZIR** |

### 🟡 ⚠ Kâğıdı BEYAZ seçin

| | |
|---|---|
| NE YAPACAĞIM | Ciltli sürüm BEYAZ kâğıtla hesaplandı. Panelde KREM seçerseniz sırt 0,8737 in olur — üretilen kapak 0,8058 in'dir ve fark 0,0680 in, KDP'nin ±0,0625 in toleransını AŞAR. |
| KDP'DE NEREYE | Hardcover Content → Print Options → Paper type |
| NE GİRECEĞİM | White paper |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Krem seçilirse kapak REDDEDİLİR ya da sırt kayar. Ciltsiz KREM kalır — iki ayrı üründür. |
| BAŞARILI OLURSA | Sırt genişliği kapakla örtüşür. |
| DURUM | **BEKLIYOR** |

## 04 · KINDLE

### 🔵 EPUB yükle

| | |
|---|---|
| NE YAPACAĞIM | Akışkan EPUB 3 · 0.0 MB · 19 bölüm · 99 gömülü levha. Baskıyla AYNI içerik. |
| KDP'DE NEREYE | Create → Kindle eBook → Kindle eBook Content → Manuscript → Upload |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/KINDLE/codex-enigmatica.epub` |
| NE KONTROL EDECEĞİM | Yükleme sonrası Kindle Previewer'da levhaların yakınlaştırılabildiğini doğrulayın. |
| BAŞARILI OLURSA | Dönüştürme hatasız biter. |
| DURUM | **HAZIR** |

### 🔵 Kapak (YALNIZCA ÖN)

| | |
|---|---|
| NE YAPACAĞIM | 1600 × 2560 px JPEG. ⛔ Sırt yok · arka kapak yok · barkod yok · taşma yok — bunlar BASKIYA aittir. |
| KDP'DE NEREYE | Kindle eBook Content → Kindle eBook Cover → Upload a cover you already have |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/KINDLE/cover.jpg` |
| NE KONTROL EDECEĞİM | Küçük resimde (thumbnail) başlık okunabilir olmalı — mağazada kapak bu boyutta görünür. |
| BAŞARILI OLURSA | Kapak kabul edilir. |
| DURUM | **HAZIR** |

### 🟢 ⭑ Telif planını SİZ seçersiniz ⭑

| | |
|---|---|
| NE YAPACAĞIM | Bu dosyada (0.0 MB) ölçülen sonuç: %70 planı teslimat ücreti keser (6.95 $) ve 2.13 $ telif bırakır; %35 planı ücret kesmez ve 3.50 $ bırakır. |
| KDP'DE NEREYE | Kindle eBook Pricing → Royalty and Pricing |
| NE GİRECEĞİM | %%35 (bu dosya boyutunda ölçülen öneri) |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | %%70'in kârlı olduğu sınır ~33,3 MB'dır; bu dosya onun ÜSTÜNDE. Formül KDP'nin kendi telif sayfasından: %%70 × (liste − KDV − teslimat). |
| BAŞARILI OLURSA | KDP net telifi gösterir ve %%35 daha yüksektir. |
| DURUM | **BEKLIYOR** |

## 05 · A+ İÇERİK

### 🔵 Altı modülü yükle

| | |
|---|---|
| NE YAPACAĞIM | 3 × tam genişlik (1940 × 600) + 3 × kare (600 × 600). Hepsi KDP'nin standart modül ölçülerinin 2× sürümüdür. |
| KDP'DE NEREYE | Marketing → A+ Content Manager → Create A+ → Add module |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/APLUS/codex-enigmatica-aplus-01..06.png` |
| NE KONTROL EDECEĞİM | Sıra `module-map.json` içindeki `id` sırasıdır: 01 → 02 → 03 → 04 → 05 → 06. |
| BAŞARILI OLURSA | Altı modül de yüklenir. |
| DURUM | **HAZIR** |

### 🟢 Başlık ve gövde metnini gir

| | |
|---|---|
| NE YAPACAĞIM | ⭑ GÖRSELLER METİNSİZDİR ⭑ — bu bilerek böyledir. Ticari metin Amazon'un KENDİ metin alanlarına girilir; görselin içine gömülmüş metin çevrilemez ve moderasyonda sorun çıkarır. |
| KDP'DE NEREYE | Her modülün 'Headline' ve 'Body text' alanı |
| NE GİRECEĞİM | 08_OUTPUT/APLUS/module-map.json → title / body |
| HANGİ DOSYA | `08_OUTPUT/APLUS/module-map.json` |
| NE KONTROL EDECEĞİM | Metin İNGİLİZCEDİR (ürün sayfası dili). Kopyala-yapıştır: bu kılavuzun § I bölümünde kopyalama düğmeleriyle duruyor. |
| BAŞARILI OLURSA | Altı modülün altısında da metin dolu. |
| DURUM | **BEKLIYOR** |

### 🟢 Moderasyona gönder

| | |
|---|---|
| NE YAPACAĞIM | Amazon A+ içeriğini İNSAN moderasyonundan geçirir. Onay genellikle birkaç iş günü sürer. |
| KDP'DE NEREYE | A+ Content Manager → Submit for approval |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Reddedilirse gerekçe e-postayla gelir; en sık sebep görselin içindeki metindir — bizde yok. |
| BAŞARILI OLURSA | Durum 'Approved' olur. |
| DURUM | **BEKLIYOR** |

## 06 · DOĞRULAMA SAYFASI

### 🟢 ⭑ Kalıcı alan adını alın ve bağlayın ⭑

| | |
|---|---|
| NE YAPACAĞIM | Kitap SON YAPRAĞINA (s. 273) şu adresi BASAR: valicepress.com/codex-enigmatica/verify — ve basılmış bir URL DÜZELTİLEMEZ. |
| KDP'DE NEREYE | Alan adı sağlayıcısı + Vercel → Project → Settings → Domains |
| NE GİRECEĞİM | valicepress.com |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | 26 Ağu 2026 ölçümü: alan adı KAYITSIZ ve müsaitti (~11,25 $/yıl). Alınmazsa başkası alabilir ve satılmış her nüsha okuru YABANCI bir siteye gönderir. |
| BAŞARILI OLURSA | Kalıcı adres yanıt verir. |
| DURUM | **BEKLIYOR** |

### 🟢 Sunucu sırlarını girin

| | |
|---|---|
| NE YAPACAĞIM | İki değişken: biber ve özet. Sunucuda DÜZ CEVAP SAKLANMAZ — saklanan şey biberli SHA-256 özetidir. İkisi de depoda DEĞİLDİR. |
| KDP'DE NEREYE | Vercel → Project → Settings → Environment Variables (Production) |
| NE GİRECEĞİM | CODEX_VERIFY_PEPPER · CODEX_VERIFY_DIGEST (değerler bu belgede YAZILI DEĞİLDİR) |
| HANGİ DOSYA | `scripts/codex-verify-digest.mjs (site deposu)` |
| NE KONTROL EDECEĞİM | Üretimi: `node scripts/codex-verify-digest.mjs` — cevabı STDIN'den okur, dosyaya ve kabuk geçmişine YAZMAZ. |
| BAŞARILI OLURSA | İkisi de 'Sensitive' olarak görünür. |
| DURUM | **HAZIR** |

### 🔴 ⛔ Upstash hız sınırı arka ucunu kurun

| | |
|---|---|
| NE YAPACAĞIM | Doğrulama uç noktası şu an CANLIDA 503 veriyor ve bu DOĞRU davranıştır: hız sınırlayıcısı olmayan bir doğrulama servisi SINIRSIZ DENEMEDİR, o yüzden bilerek KAPALI düşer. |
| KDP'DE NEREYE | upstash.com → Redis database → REST API |
| NE GİRECEĞİM | UPSTASH_REDIS_REST_URL · UPSTASH_REDIS_REST_TOKEN (Vercel Production) |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | ÖLÇÜLDÜ: üretimdeki URL bir URL DEĞİL (şema yok, ana makine adı 0 karakter) ve belirteç 11 karakter — 89 gün önce konmuş YER TUTUCULAR. Aynı sebep sitenin çevre sınırlayıcısını da sessizce AÇIK düşürüyor. |
| BAŞARILI OLURSA | `qa_verification.py --gate release --live` yeşil döner. |
| DURUM | **BEKLIYOR** |

## 07 · METADATA

### 🟢 Panel alanlarını doldurun

| | |
|---|---|
| NE YAPACAĞIM | Başlık, alt başlık, yazar, yayıncı, açıklama, 7 anahtar kelime ve 3 BISAC kategorisi. |
| KDP'DE NEREYE | Paperback/Hardcover/Kindle → Details |
| NE GİRECEĞİM | § H'deki tablodan kopyalayın (kopyalama düğmeleri var) |
| HANGİ DOSYA | `06_REPORTS/tracked/metadata.json` |
| NE KONTROL EDECEĞİM | ÜÇ SÜRÜMDE DE AYNI olmalı — başlık ya da yazar farklı yazılırsa Amazon sürümleri birbirine BAĞLAMAZ ve üç ayrı ürün gibi listelenir. |
| BAŞARILI OLURSA | Üç sürüm tek ürün sayfasında birleşir. |
| DURUM | **HAZIR** |

## 08 · FİYAT

### 🟢 Liste fiyatlarını girin

| | |
|---|---|
| NE YAPACAĞIM | Ciltsiz 19.99 $ · Ciltli 29.99 $ · Kindle 9.99 $ (ABD). |
| KDP'DE NEREYE | Her sürümün Rights & Pricing ekranı |
| NE GİRECEĞİM | 19.99 / 29.99 / 9.99 USD |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Gerekçeler ve ölçülen telifler § J'de. Diğer pazarlar için KDP otomatik dönüştürme önerir — kabul edebilirsiniz. |
| BAŞARILI OLURSA | KDP her sürüm için net telifi gösterir ve § J'deki sayılarla örtüşür. |
| DURUM | **BEKLIYOR** |

## 09 · PREVIEWER — ZORUNLU

### 🔴 ⭑ Baskı Previewer'ında sayfa sayfa bakın ⭑

| | |
|---|---|
| NE YAPACAĞIM | Bu adım ATLANAMAZ. Yerel ölçümlerin hepsi yeşil olabilir ve Previewer yine de gerçek bir kusur gösterebilir — dizgi motoru başkadır. |
| KDP'DE NEREYE | Yükleme sonrası açılan Previewer |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | ① kapak · ② SIRT yazısı ortalı mı · ③ kenar payları · ④ iç pay (gutter) hiçbir levhayı kesmiyor mu · ⑤ sayfa geçişleri · ⑥ levhalar/şekiller · ⑦ metin · ⑧ boş sayfalar · ⑨ ÇÖZÜM bölümü · ⑩ SON YAPRAKTA doğrulama adresi. |
| BAŞARILI OLURSA | Previewer 'no errors' der VE göz denetimi temiz geçer. |
| DURUM | **BEKLIYOR** |

### 🔴 Kindle Previewer

| | |
|---|---|
| NE YAPACAĞIM | Akışkan metin, farklı cihazlarda farklı kırılır. Levhaların yakınlaştırılabildiğini görün. |
| KDP'DE NEREYE | Kindle eBook Content → Preview |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Telefon + tablet + e-mürekkep görünümlerinde bakın; levhalar ve çizelgeler okunabilir olmalı. |
| BAŞARILI OLURSA | Üç görünümde de içerik okunur. |
| DURUM | **BEKLIYOR** |

### 🟡 Fiziksel prova (önerilir)

| | |
|---|---|
| NE YAPACAĞIM | Gravür levhaların nokta yayılması altındaki davranışı YALNIZCA basılı provada ölçülür. Ekranda kusursuz görünen levha kâğıtta kapanabilir. |
| KDP'DE NEREYE | Previewer → Print a proof copy |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | A9 · kurucu kararı. Zorunlu değil ama bu kitapta LEVHALAR ÜRÜNÜN KENDİSİDİR. |
| BAŞARILI OLURSA | Prova elinizde ve levhalar okunur. |
| DURUM | **BEKLIYOR** |

## 10 · SON GÖNDERİM

### 🔴 ⛔ GERÇEK BİR KUSUR VARSA YAYIMLAMAYIN

| | |
|---|---|
| NE YAPACAĞIM | Yerel yeşil preflight, gerçek bir KDP Previewer kusurunu GEÇERSİZ KILMAZ. Previewer bir hata gösteriyorsa önce o düzelir. |
| KDP'DE NEREYE | — |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Kusur gerçek mi yoksa Previewer'ın bilinen görüntüleme tuhaflığı mı — emin değilseniz prova alın. |
| BAŞARILI OLURSA | Bilinen gerçek kusur YOK. |
| DURUM | **BEKLIYOR** |

### 🔴 Publish

| | |
|---|---|
| NE YAPACAĞIM | Üç sürümü de yayımlayın. Amazon 24–72 saat içinde canlıya alır. |
| KDP'DE NEREYE | Her sürümün son ekranı → Publish Your Book |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | ⚠ Bu kitabı HİÇBİR HARİCİ İNSAN ÇÖZMEDİ (0/5 oturum, ölçülen karar HARD-STOP). Yayımlama kararını bunu BİLEREK verin. |
| BAŞARILI OLURSA | Üç sürüm de 'Live' olur. |
| DURUM | **BEKLIYOR** |

## H · Panele girilecek alanlar

| Alan | Değer |
|---|---|
| Başlık | Codex Enigmatica |
| Alt başlık | One Hundred Engraved Enigmas and a Single Unbroken Mystery |
| Yazar | Emre Doğan |
| Yayıncı | Vâliçe Press |
| Seri | Codex · cilt 3 |
| Açıklama | One hundred engraved enigmas and a single unbroken mystery.  Five gates. Twenty puzzles each. Every answer is a member of a catalogue printed inside this book — nothing here asks you to leave it.  The ciphers are not printed beside the plates; they are printed INSIDE them. A keystone that is missing, a ring whose anchor is not marked, a chart whose own length is the number you need.  Every puzzle has exactly one answer and a three-tier hint ladder that never gives it away. Taking a hint is not losing.  And when the five gates are open, they give you five phrases that say nothing on their own. The answer to the last question is not printed anywhere in this book.  101 puzzles · 5 gates · 303 hints · 103 engraved plates · 274 pages |
| Anahtar kelime 1 | puzzle book for adults |
| Anahtar kelime 2 | cipher puzzle book |
| Anahtar kelime 3 | codebreaking puzzles |
| Anahtar kelime 4 | escape room book |
| Anahtar kelime 5 | meta puzzle mystery |
| Anahtar kelime 6 | grimoire puzzle book |
| Anahtar kelime 7 | hidden message puzzles |
| Kategori 1 | GAM011000 — GAMES & ACTIVITIES / Puzzles |
| Kategori 2 | GAM001000 — GAMES & ACTIVITIES / Reference |
| Kategori 3 | GAM002000 — GAMES & ACTIVITIES / Logic & Brain Teasers |
| Yazar biyografisi | Emre is a puzzle designer, mythologist, and game archivist dedicated to preserving ancient cultures, codes, and stories for the next generation. |
| Dil | English |
| Baskı | First edition |
| Sürümler | hardcover 29.99 $ · paperback 19.99 $ · kindle 9.99 $ |
| Sayfa (baskı) | 274 |
| ISBN | ⛔ KURUCU KDP PANELİNDE GİRECEK (strateji: kdp-free) |
| YZ içerik beyanı | ⛔ KURUCU KDP PANELİNDE TAMAMLAYACAK |

## I · A+ metni (İngilizce — ürün sayfası dili)

| Modül | Başlık | Gövde |
|---|---|---|
| `aplus-01` | Not a puzzle book. An object with a hidden system. | One hundred engraved enigmas and a single unbroken mystery. Five gates, twenty puzzles each, bound as a volume meant to sit on a shelf rather than be thrown away. |
| `aplus-02` | The cipher is inside the plate. | The code is not printed beside the engraving — it is printed inside it: in the direction of the hatching, the order of the symbols, the ornament along the edge. Over one hundred original plates, each one carrying its own puzzle. |
| `aplus-03` | You are allowed to give up. | Every puzzle carries a three-tier hint ladder that narrows the search without ever handing over the answer. Taking a hint is not losing. |
| `aplus-04` | From observation to inference. | Every answer is a member of a catalogue printed inside this book. Nothing here asks you to leave it, and nothing here rewards guessing. |
| `aplus-05` | Five gates. One passage. | The gates open in order, and each one changes what the next one asks of you. What you learn in the first is the tool you need in the last. |
| `aplus-06` | The last question. | When the five gates are open they give you five phrases that say nothing on their own. The answer to the last question is not printed anywhere in this book — it is verified online. |

> Görsellerde **metin yoktur**; bu metin Amazon'un kendi
> başlık ve gövde alanlarına girilir.

## I.5 · ⛔ KDP'NİN GERÇEK ÖNİZLEMESİNDE HATA ÇIKARSA

> **Bu bölüm bir tahmin değil, yaşanmış bir reddin kaydıdır.**
> 28 Ağustos 2026'da KDP kitabı reddetti — ve o gün bütün
> yerel kapılar **yeşildi**.

### 1 · Yerel yeşile GÜVENMEYİN

Yerel kapılar yalnızca **sordukları soruları** yanıtlar.
O gün hiçbiri şunu sormuyordu: *yazı tipleri gömülü mü*,
*her glif yüzünde var mı*, *metin sayfada kalıyor mu*.
Kapak kapısı yalnızca **karşıtlık** ölçüyordu: yazının
**okunur** olduğunu doğruluyor, **sayfada kaldığını** hiç
sormuyordu.

⭑ **Gerçek KDP Previewer, yerel preflight'tan ÜSTÜNDÜR.**

### 2 · Hatayı BİREBİR kaydedin

Amazon'un cümlesini ve verdiği **sayıları** olduğu gibi not
edin — 0,716 in gibi bir sayı, düzeltmenin tek yetkesidir.
Verdiği sayfa numarasını da yazın.

### 3 · ⚠ Bildirilen sayfa bir ÖRNEKTİR, envanter DEĞİL

İki kez yaşandı ve iki kez de aynı çıktı:

| KDP'nin dediği | Ölçülen gerçek |
|---|---|
| "5 sayfa" (pay) | **140 sayfa** |
| "s. 135" (dönüşüm) | **274 sayfanın hepsi** |

Bildirilen sayfayı düzeltip durmak, kusuru bırakmaktır.

### 4 · KAYNAĞA dönün, PDF'i yamamayın

Düzeltme `04_BUILD/` ve `01_SOURCE/` içindedir. Nihai PDF'i
elle düzenlemek, bir sonraki üretimde kusuru geri getirir.

### 5 · Yeniden üretin ve ÖLÇÜN

```
python3 04_BUILD/interior.py
python3 04_BUILD/interior.py --binding hardcover
python3 04_BUILD/covers.py
python3 04_BUILD/covers.py --binding hardcover
python3 04_BUILD/kindle.py
python3 04_BUILD/qa_kdp_conversion.py     # yazı tipi · glif · kapak
python3 04_BUILD/qa_print_margins.py      # her sayfanın mürekkebi
./04_BUILD/qa_all.sh --fix
python3 04_BUILD/kdp_package.py           # sağlama toplamları
```

### 6 · ⚠ Sayfa sayısı değişebilir — ve her şey ona bağlıdır

Tek bir karakter kaldırmak satır sonunu değiştirir. Bu onarımda
ciltli **274 → 276** sayfaya çıktı ve şunların hepsi yeniden
hesaplandı: **sırt · kapak genişliği · baskı maliyeti · telif ·
arka kapağa basılan sayfa sayısı**. Sayfa sayısı değişirse
kapağı da yeniden üretin.

### 7 · Düzeltilmiş dosyayı yükleyin ve BİLDİRİLEN SAYFAYA bakın

KDP Bookshelf → ilgili sürüm → *Upload a revised manuscript* /
*Update a revised cover*. Sonra Previewer'da **Amazon'un
saydığı sayfaları** tek tek açın.

### 8 · KDP geçene kadar tekrarlayın

> ⛔ **Yerel yeşil, yayımlama izni değildir.** Previewer gerçek
> bir kusur gösteriyorsa yayımlamayın — kapıyı gevşetmek,
> eşiği düşürmek ya da denetimi kaldırmak **çözüm değildir**.

## J · 📂 DOSYA HARİTASI — hangi dosya, nereye

Her satır **tek bir dosyayı tek bir KDP alanına** bağlar.
Yol proje kökünden görelidir.

| Sürüm | Dosya | KDP alanı |
|---|---|---|
| Paperback · iç blok | `08_OUTPUT/PAPERBACK/interior.pdf` | Paperback Content → Manuscript |
| Paperback · kapak | `08_OUTPUT/PAPERBACK/cover.pdf` | Paperback Content → Book Cover (upload your own) |
| Hardcover · iç blok | `08_OUTPUT/HARDCOVER/interior.pdf` | Hardcover Content → Manuscript |
| Hardcover · kapak | `08_OUTPUT/HARDCOVER/cover.pdf` | Hardcover Content → Book Cover (upload your own) |
| Kindle · EPUB | `08_OUTPUT/KINDLE/codex-enigmatica.epub` | Kindle eBook Content → Manuscript |
| Kindle · kapak | `08_OUTPUT/KINDLE/cover.jpg` | Kindle eBook Content → Kindle eBook Cover |
| A+ · 6 görsel | `08_OUTPUT/APLUS/codex-enigmatica-aplus-01..06.png` | A+ Content Manager → Add module → Image |
| A+ · metin | `08_OUTPUT/APLUS/module-map.json` | A+ Content Manager → Headline / Body text |
| Metadata (üç sürüm) | `06_REPORTS/tracked/metadata.json` | Details → başlık · alt başlık · açıklama · anahtar kelime |
| Sağlama toplamları | `08_OUTPUT/*/SHA256SUMS` | — (yüklemeden ÖNCE yerelde doğrulanır) |

## K · ⭑ FİYAT ÖNERİSİ VE GEREKÇESİ ⭑

| Sürüm | Liste | Baskı maliyeti | **Telif** | Marj |
|---|---:|---:|---:|---:|
| Ciltsiz | 19.99 $ | 4.14 $ | **7.86 $** | %39.3 |
| Ciltli | 29.99 $ | 8.96 $ | **9.03 $** | %30.1 |
| Kindle · %35 planı · 46.3 MB | 9.99 $ | — | **3.50 $** | %35.0 |

> ⚠ **Bunlar garanti edilmiş kazanç değildir.** Baskı maliyeti
> KDP'nin ABD fiyat modelinden **hesaplanmıştır** (alınmış bir
> teklif değildir); telif pazara ve dağıtım seçimine göre
> değişir; Kindle telifi seçtiğiniz plana bağlıdır.

### Neden bu fiyatlar

**Ciltsiz · 19,99 $** — 20 doların ALTINDA kalan en yüksek basamak. 274 sayfa ve 103 gravür levha için 19,99 $ premium bir bulmaca kitabının olağan yeridir; 21,99 $ psikolojik 20 $ eşiğini aşar ve tanınmayan bir yazarın ilk kitabında dönüşümü düşürür. 17,99 $ ise kopya başına 1,20 $'ı sebepsiz bırakır.

**Ciltli · 29,99 $** — 30 doların ALTINDA kalan en yüksek basamak ve klasik hediye kitabı yeri. Ciltsizin tam 10 $ üstü — yani %50 net premium: alıcı farkı GÖREBİLİR ve gerekçelendirebilir. 32,99 $ hem 30 $ eşiğini aşar hem de ciltsizle arayı 13 $'a çıkarıp ciltsizi 'ucuz sürüm' gibi gösterir.

**Kindle · 9,99 $** — Ciltsizin TAM YARISI — merdiven okunur ve tutarlıdır. Dosya 46,3 MB olduğu için %35 planı seçilir ve o planda fiyat bandı kısıtı bağlamaz. 6,99 $ 274 sayfalık resimli bir kitabı ucuza düşürür ve baskıyı yer; 8,99 $ makul bir alternatiftir ve dönüşüm yavaşsa ilk denenecek basamaktır (kopya başına 0,35 $).

### Fiyat denetimi

| Soru | Ölçülen |
|---|---|
| Kötü telif üretiyor mu | HAYIR — ciltsiz %39,3 · ciltli %30,2 marj |
| Müşteri fiyatı ürkütücü mü | HAYIR — ikisi de psikolojik eşiğin ALTINDA (20 $ / 30 $) |
| Ciltli premiumu net mi | EVET — +10,00 $ (%50 üstü) |
| Kindle baskının anlamlı altında mı | EVET — ciltsizin tam yarısı |
| Üretim kalitesiyle tutarlı mı | EVET — 274 sayfa · 103 levha · sarmal kapak |
