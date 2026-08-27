# B2 — DOĞRULAMA SAYFASI · TESLİM RAPORU

> **27 Ağustos 2026** · B2 yönergesi § 22
>
> ## ⛔ ÖNCE BU: B1 VE B3 ÇÖZÜLMEDİ
>
> Yönerge açıktı: *"Do NOT pretend that the other Founder-owned blockers
> are solved."* Bu rapor **yalnızca B2'yi** kapatır.
>
> | | Durum | Kime ait |
> |---|---|---|
> | **B1** · harici insan doğrulaması | ⛔ **AÇIK** — 0 oturum, öldürme kapısı HARD-STOP | kurucu + 5 insan |
> | **B2** · doğrulama sayfası | ✅ **MEKANİZMA KURULDU** — yayın kurucuda | ⬍ karma |
> | **B3** · ISBN + YZ beyanı | ⛔ **AÇIK** — `metadata.json`'da iki alan boş | kurucu |
>
> B2 bile **yarım kapanmıştır** ve bunu saklamıyorum: kod yazıldı, test
> edildi, kitap adresi bastı — ama **alan adı alınmadı, site yayına
> alınmadı**. Sayfa şu an hiçbir yerde yaşamıyor.

---

## 1 · Kitap ne vaat ediyordu — ve neyi tutmuyordu

Sözleşme sayfası (`matter.py § CONTRACT`) okura **adıyla** söz verir:

> *"You enter it on the VERIFICATION PAGE, whose address is printed on
> the last leaf of this book."*

Ve kapanış (`§ CLOSING`) şunu der:

> *"When you have it, you know where to write it."*

**Ölçüm:** 274 sayfanın hiçbirinde adres yoktu. Yani kitap 11. sayfada
verdiği sözü 273. sayfada bozuyor, sonra okura *"nereye yazacağını
biliyorsun"* diyordu — **bilemezdi.**

### 1.1 · Ve ikinci bir uyuşmazlık: karşılıksız söz

Birinci söz şöyle açıklanıyordu:

> *"If you think you have found a second reading, either the book is
> wrong or you are. **The verification page will tell you which.**"*

⚠ **Bu cümle sayfanın yapamayacağı bir şeydi** — ve yapabilseydi ürünü
bitirirdi.

Bu, `DECISIONS.md § A7`'nin *"doğrulama sayfası 100 cevap alanı taşısın
mı"* sorusudur ve **AÇIK** bir kurucu kararıdır. Şu ölçümü kayda
geçiriyorum çünkü karar bunu bilerek alınmalı:

| | Ölçülen |
|---|---:|
| Cevap uzayının tamamı (elenen aday dize) | **5 086** (`BOOK_STATS § 1`) |
| 101 cevabı kabul eden bir kâhini tüketmek için gereken istek | **~5 086** |
| Bunun için kitabı satın almak gerekir mi | **HAYIR** |

Yani 101 cevap alanı, **kitabı hiç almamış birine çözüm kitabının
tamamını dağıtır**. `PROJECT_CONTEXT § 5·②` bunu tek cümleyle söylüyor:
*"Bir bulmaca kitabının çözümleri ürünün kendisidir."*

**En küçük güvenli değişiklik** — ve yaptığım bu:

| | |
|---|---|
| ~~*"The verification page will tell you which."*~~ | kaldırıldı |
| *"The solution in the back matter settles it: every one of the hundred is printed there, with the reasoning that produced it."* | kondu |

Bu **doğrudur ve zaten kitaptadır**: 100 çözüm arka maddede basılıdır.
Okur ikinci bir okuma bulduğunu sandığında hakem **kitabın kendisidir** —
bir sunucu değil. Dört söz cümlesinin hiçbirine dokunulmadı
(`SOLVABILITY_STANDARD § 1` onları dondurur; dondurduğu **başlıklardır**,
açıklamalar değil).

⚠ **A7 hâlâ AÇIKTIR.** Bu bir öneri ve bir ölçümdür, kurucu kararının
yerine geçmez. Kurucu "evet" derse mekanizma değil **ürün modeli**
değişmelidir (ör. satın alma kanıtına bağlı kimlik) — ve o, § 19'un
yasakladığı ölçekte bir iştir.

### 1.2 · Üçüncü uyuşmazlık: normalizasyon kime aitti

`answerFormat` normalizasyonu **doğrulama sayfasına** atfediyordu — ama
kural kitabın kendi kuralıdır ve arka madde çözümleri için de geçerlidir.
Cümle, kuralı kitaba geri verecek şekilde düzeltildi.

---

## 2 · Basılan adres

```
valicepress.com/codex-enigmatica/verify
```

| | |
|---|---|
| Tek yetke | `project_config.json § founder.verification.printedUrl` |
| Kanonik | `https://valicepress.com/codex-enigmatica/verify` |
| Site rotası | `/codex-enigmatica/verify` |
| Basılı nüshada | **s. 273** (son yaprağın ön yüzü; 274 boş arka yüz) |
| Kindle'da | son bölüm · **gerçek HTTPS bağ**, görünen metin birebir aynı |

### 2.1 · ⚠ Alan adı henüz bizim değil

**26 Ağustos 2026 ölçümü:** `valicepress.com` **kayıtsız ve müsait**
(11,25 $/yıl). Yani adres serbesttir — **ama alınmamıştır.**

⛔ **Alan adını almadım ve alamam:** bu bir ödeme işlemidir ve kurucuya
aittir. Yönerge § 26 zaten yayını yasaklıyor.

⭑ **BU, BU DEPODAKİ EN PAHALI TEK DİZEDİR.** Basılmış bir URL
düzeltilemez. Alan adı başkasının eline geçerse **satılmış her nüsha**
okuru yabancı bir siteye gönderir — ve geri dönüşü yoktur.

---

## 3 · Mekanizma — cevap nerede DEĞİL

Yönerge: *"Do NOT expose the canonical answer client-side. Prefer storing
a cryptographic hash or equivalent server-side secret."*

```
digest = SHA-256( pepper ‖ 0x00 ‖ normalize(cevap) )
```

| Nerede | Ne var |
|---|---|
| Sayfa kaynağı / HTML | **hiçbir şey** |
| JavaScript paketi | **hiçbir şey** |
| Metadata / OG | **hiçbir şey** |
| Depo | **hiçbir şey** |
| Sunucu ortamı | biber **ve** özet — cevap **yok** |

### 3.1 · Biber neden var

Cevap 5 harfli tek bir sözcüktür. Biber olmasaydı **26⁵ ≈ 11,9 milyon**
aday, çıplak bir SHA-256'ya karşı saniyeler içinde denenirdi. Özetin tek
başına sızması bir şey vermemelidir; biber onu sağlar.

### 3.2 · Ölçülen sızıntı taraması

| Yüzey | Cevap | Biber | Özet |
|---|---:|---:|---:|
| `.next/static` (tarayıcıya inen) | **0** | **0** | **0** |
| `.next/server` (sunucu derlemesi) | **0** | **0** | **0** |
| Basılı iç bloğun son 5 sayfası | **YOK** | — | — |
| Kanarya (`qa_solution_leak`) | ✅ 4 denetim yeşil · 146 dosya | | |

---

## 4 · Güvenlik ve kötüye kullanım

| Önlem | Ölçülen davranış |
|---|---|
| Ani hız sınırı | **5 / 60 s** (`codex-verify-burst`) |
| Sürekli hız sınırı | **20 / saat** (`codex-verify-hour`) |
| İkisi de geçmeli | evet |
| Sınırlayıcı yoksa / patlarsa | ⭑ **KAPALI DÜŞER** → 503 |
| Sır çifti eksik / bozuksa | ⭑ **KAPALI DÜŞER** → 503 |
| Doğru cevap | **200** |
| Yanlış cevap | **200** ← durum satırı hiçbir şey sızdırmaz |
| Yanıt gövdesi | `{ ok, result }` — **yankı yok** |
| `Cache-Control` | `no-store` |
| `GET` | **405** (`Allow: POST`) — cevaplar erişim kaydına düşmesin |
| Girdi tavanı | 200 karakter |
| Günlük | ⭑ gönderim **hiçbir zaman** yazılmaz |

⚠ **Neden kapalı düşüyor:** çevre hız sınırlayıcısı (`src/proxy.ts`)
açık düşer — genel trafik için doğrudur. Bu uç nokta için **yanlıştır**:
sınırlayıcısız bir kâhin, sınırsız denemedir. Bu yüzden burada ayrı ve
sert bir sınırlayıcı vardır.

⚠ **Neden iki durum da 200:** 401/403 ile 200 ayrımı, HTTP durum
satırından cevap sızdırırdı — gövdeyi hiç okumadan.

### 4.1 · Sızdırılmayanlar

Cevap · kısmi cevap · **cevap uzunluğu** · karakter konumu · "yaklaştın"
sinyali · deneme sayacı · başka bulmacanın bilgisi. Form alanında
`maxLength` bile **yoktur** — uzunluk tavanı bir ipucudur.

---

## 5 · Doğrulama sonrası — ve zorlanmayan e-posta

Yönerge: *"Do not force email collection just to verify an answer."*

Doğru cevap → **VERIFIED** paneli. Altında, **ayrı** bir bölüm:

```
OPTIONAL — Tell me when the next one is built
```

| | |
|---|---|
| Doğrulama abonelikten bağımsız mı | ✅ **evet** |
| Ön işaretli kutu var mı | ❌ **yok** |
| E-posta olmadan tam sonuç görülür mü | ✅ **evet** |
| Panel kim olduğunuzu kaydeder mi | ❌ **hayır** — ve bunu yazıyor |

---

## 6 · Kapı — `04_BUILD/qa_verification.py`

Yeni bir kalite kapısı. **21 denetim** (`phase5`), `release`'te **24**.

| Ölçtüğü | Kırmızı olduğu hâl |
|---|---|
| Yer tutucu adres | `example.com` · `localhost` · `TODO` · **`*.vercel.app`** |
| Biçim | büyük harf · boşluk · 60 karakterden uzun · 3'ten derin |
| Yol ↔ rota | basılan adres site rotasıyla bitmiyorsa |
| Kapsam | `final-answer-only` değilse (101 cevap alanı **kırmızıdır**) |
| Sır modeli | `peppered-sha256` değilse |
| Basılı üründe | adres üç formatta da yoksa |
| Yer tutucu basımı | basılı metin yer tutucu taşıyorsa |
| Karşılıksız söz | basılı metin sayfanın yapmadığını vaat ediyorsa |
| **`release`'te ayrıca** | alan adı kayıtsız · yayında değil · hiç canlı doğrulanmamış |

⚠ **`*.vercel.app` bilerek yasaktır:** önizleme alan adı **kiracıdır**.
Proje silinir ya da adı değişirse adres ölür — ve kitap basılmıştır.

⚠ **Ağ çağrısı varsayılan olarak kapalıdır** (`--live` ile açılır). CI'da
ağ yok, alan adı henüz alınmadı; her koşuda kırmızı yanan bir denetim
kapıyı okunmaz hâle getirir, ve okunmayan kapı yoktur.

### 6.1 · Kapının kendi testi

`05_TESTS/selftest.py § ⑮` — **24 yeni denetim.** Bir kapının varlığı
yetmez, **ısırması** gerekir. Fikstürlerden biri kapının kendi körlüğünü
ölçer:

> *"The founder of the house had left a pending question on an A4 sheet,
> and the ship foundered off the coast."*

Bu cümle **yer tutucu değildir** ve kapı ona kırmızı yanmamalıdır — çünkü
her koşuda kırmızı yanan bir kapı okunmaz. Adres süzgeci sert kalır,
basılı metin süzgeci ayrı ve dardır.

**Toplam:** 249 → **273 denetim.**

---

## 7 · Testler

| | |
|---|---:|
| Site testi (önce) | 53 |
| Site testi (şimdi) | **105** |
| — `codex-verify.ts` birim | 17 |
| — doğrulama rotası (HTTP) | 15 |
| — bülten rotası (**daha önce testsizdi**) | 20 |
| Kitap kapısı öz testi | 249 → **273** |
| `qa_all.sh` | **38 kapı · hepsi yeşil** |
| KDP paketi + preflight | **30 denetim yeşil** |

### 7.1 · Gerçekten koşturulan HTTP matrisi

Yerel Upstash yoktu; bu yüzden Upstash REST sözleşmesini (`POST
/pipeline` · `evalsha` · `[remaining, limit]`) uygulayan küçük bir
taklit yazıldı ve **gerçek** hız sınırı davranışı ölçüldü — tam **5.**
denemede 429, `Retry-After` başlığıyla.

Başarı yolu tarayıcıda **gerçek cevap yazılmadan** doğrulandı: aynı
biberle bir **fikstür özeti** geçici olarak kondu, panel görüldü, sonra
gerçek özet geri yüklendi ve **kitabın kaynağıyla karşılaştırılarak**
doğrulandı (yalnızca boole yazdırılarak).

Son duman testi (gerçek özetle, cevap hiçbir yere yazılmadan):

```
yanlış cevap            → 200 · no-match
eski fikstür sözcüğü    → 200 · no-match
gerçek cevap (küçük harf, boşluk ve noktalama ile) → 200 · match
```

⚠ **Ölçemediğim bir şey:** mobil düzen. Tarayıcı eklentisinin pencere
boyutlandırması içerik görüntü alanına yansımadı (iki denemede de
`2060×1036` kaldı). Masaüstü görünümü **görerek** doğrulandı; mobil
yığılma yalnızca **sınıf denkliğiyle** (`flex-col sm:flex-row`,
`sm:grid-cols-[auto_1fr]`, `px-4 sm:px-6` — sitenin başka sayfalarında
zaten kullanılan ilkeller) doğrulandı. Bunu ölçüm diye sunmuyorum.

---

## 8 · Bülten — bir yalan daha kapandı

Yönerge § 14 tek ana liste + etiket istiyordu. Uygulanırken bulunan
kusur: `category-sidebar.tsx` okura *"you'll hear from us soon"* diyor ve
adresi **atıyordu** — oysa `/api/newsletter` rotasının kendi başlık
yorumu bu yalanın Faz 2.A'da bittiğini söylüyordu. Üç form bağlanmış,
dördüncüsü unutulmuştu.

Şimdi: dört formun dördü de tek Resend Audience'ına yazar ve **kaynağını
etiketler** (`home` · `article` · `category` · `codex-verify`). Etiket
kapalı bir listedir — tarayıcıdan gelen serbest bir dize kişi kaydına
yazılamaz — ve **bilinmeyen etiket düşürülür, abonelik reddedilmez**:
kötü bir etiket bizim hatamızdır, abonenin değil.

⚠ **Bilerek kaydedilmeyenler:** IP · tarayıcı imzası · ülke. Hiçbiri bu
rızayı onurlandırmak için gerekli değildir.

---

## 9 · Yapılmayanlar

| | Neden |
|---|---|
| Alan adı satın alınmadı | ödeme işlemi · **kurucuya ait** |
| Site yayına alınmadı | § 26 · **kurucuya ait** |
| Kitap yayımlanmadı, KDP'ye yüklenmedi | § 26 |
| B1 / B3 kapatılmadı | § 0 · **kurucuya ait** |
| 101 cevap alanı yapılmadı | ölçülen güvenlik gerekçesi · A7 **açık** |
| Site yeniden tasarlanmadı, çatı değişmedi, CRM eklenmedi | § 19 |

---

## 10 · Kurucuya düşen sıra

1. **`valicepress.com` alan adını al** (~11,25 $/yıl · müsait ölçüldü)
2. Vercel'de projeye bağla, **üretime yükselt** (`live: true`)
3. Vercel ortam değişkenleri: `CODEX_VERIFY_PEPPER` · `CODEX_VERIFY_DIGEST`
   — üretimi `node scripts/codex-verify-digest.mjs` ile **STDIN'den**
   (dosyaya ve kabuk geçmişine yazma)
4. `project_config.json § founder.verification` → `domainRegistered`,
   `deployed`, `liveVerifiedAt` alanlarını **gerçekten olduktan sonra** doldur
5. `python3 04_BUILD/qa_verification.py --gate release --live` koştur ve
   **kararı oku**
6. Ancak ondan sonra baskı

⛔ 1–5 tamamlanmadan `release` kapısı **KIRMIZIDIR** ve bu kasıtlıdır.
