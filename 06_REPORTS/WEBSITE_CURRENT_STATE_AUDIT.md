# WEBSITE CURRENT STATE AUDIT — `enterprise-web-site`

> **27 Ağustos 2026** · B2 yönergesi § 3 · § 22
>
> Bu belge siteyi **olduğu gibi** kaydeder. Yönerge açıktı:
> *"The website is an unfinished future sales channel for the Founder. It
> must be treated as an existing product, not as a blank project."*
> Bu yüzden aşağıda **hiçbir mimari öneri yoktur**; yalnızca ölçüm vardır.
> Öneriler ayrı bir belgededir (`WEBSITE_KDP_BUSINESS_STRATEGY.md`).

---

## 0 · Tek cümlelik sonuç

Site **bitmiş bir ürün değil, çalışan bir iskelettir**: 27 sayfa rotası,
6 API rotası, 34 259 satır TypeScript, ticaret hattı (Paddle) ve yetki
hattı (Clerk + Neon) kurulu — ama **hiçbir yere yayınlanmamıştır** ve
kendi alan adı yoktur.

> ⛔ **SİTE YAYINDA DEĞİLDİR.** Bu ölçülmüştür, tahmin değildir:
> Vercel projesi `live: false`, üretim hedefi `target: null`, özel alan
> adı **yok**. En yeni dağıtım Haziran 2026'dan kalma bir **önizlemedir**
> ve bu oturumun işini içermez.

---

## 1 · Ölçülen envanter

| | Ölçülen |
|---|---:|
| Sayfa rotası | **27** |
| API rotası | **6** |
| React bileşeni (`.tsx`) | **142** |
| `src/lib` modülü | **41** |
| Toplam TS/TSX dosyası | **242** |
| `src/` satır sayısı | **34 259** |
| Test dosyası | **9** |
| Test | **105** (bu oturumdan önce 53) |

### 1.1 · Sayfa rotaları

```
/                          /books                  /account/library
/about                     /books/[slug]           /account/orders
/authors                   /cart                   /account/settings
/authors/[slug]            /order/[id]             /admin
/blog                      /read/[bookId]          /admin/books/[slug]/edit
/blog/[slug]               /search                 /genres
/blog/category/[slug]      /categories             (legal)/privacy
/blog/tag/[slug]           /categories/[slug]      (legal)/terms
                                                   (legal)/kvkk
⭑ /codex-enigmatica/verify   ← BU OTURUMDA EKLENDİ  (legal)/refund
```

### 1.2 · API rotaları

| Rota | İş |
|---|---|
| `/api/cart/count` | sepet rozeti |
| `/api/entitlement` | okuma hakkı denetimi |
| `/api/inngest` | arka plan iş kuyruğu |
| `/api/newsletter` | Resend Audiences aboneliği |
| `/api/webhooks/paddle` | ödeme olayları |
| ⭑ `/api/codex-enigmatica/verify` | **bu oturumda eklendi** |

---

## 2 · Yığın — ölçülen sürümler

| Katman | Seçim | Sürüm |
|---|---|---|
| Çatı | Next.js **App Router** | `16.2.6` |
| Görünüm | React | `19.2.4` |
| Stil | Tailwind CSS | `v4` |
| Kimlik | Clerk (`src/proxy.ts`) | `^7.4.2` |
| Veri | Neon PostgreSQL + Drizzle | `^1.1.0` / `^0.45.2` |
| Dosya | Cloudflare R2 (AWS S3 SDK) | `^3.1055.0` |
| Ödeme | Paddle (**Merchant of Record**) | `^3.8.0` |
| Posta | Resend (işlemsel + Audiences) | `^6.12.4` |
| Hız sınırı | Upstash Redis + Ratelimit | `^1.38.0` / `^2.0.8` |
| Hata | Sentry | `^10.55.0` |
| Ölçüm | Vercel Analytics + Speed Insights | `^2.0.1` / `^2.0.0` |
| Kuyruk | Inngest | `^4.5.0` |
| Test | Vitest | `^4.1.7` |

⚠ **Next 16 ayrıntısı:** ara katman `middleware.ts` değil **`src/proxy.ts`**
adındadır — Next 16'nın dosya sözleşmesi. Bunu bilmeyen biri ara katmanı
"yok" sanır.

---

## 3 · Tasarım dili — doğrulama sayfası buna uydu

Sayfa **yeni bir görsel dil kurmadı**; sitenin kendi dilini kullandı:

| Belirteç | Nerede |
|---|---|
| `.cinematic-root` | kök kabuk |
| `fg-hi` · `fg-mid` · `fg-soft` · `fg-fade` | metin kademeleri |
| `emerald-bright` (`#33f0aa`) | vurgu |
| Fraunces (`font-serif`) | başlık |
| `home-glass` | kart yüzeyi |
| `home-cta-primary` | birincil düğme |
| `catalog-diamond` | süs |

`src/app/codex-enigmatica/layout.tsx`, `src/app/(legal)/layout.tsx` ile
**yapı olarak birebir aynıdır** (CinematicHeader + HomeFooter). Yani
doğrulama sayfası siteye eklenmiş bir yama değil, sitenin kendi
kabuğunda duran bir sayfadır.

---

## 4 · Bulunan kusurlar

Bu oturum siteyi yeniden tasarlamadı; ama **doğrulama sayfasının
dokunduğu yolda** üç kusur buldu ve ikisini düzeltti.

### ✅ ① Kategori kenar çubuğu abone olmuyordu — **DÜZELTİLDİ**

`src/components/category/category-sidebar.tsx` okura
*"Thanks — you'll hear from us soon"* diyor ve adresi **atıyordu**:

```ts
// TODO: wire to /api/newsletter once a provider lands (STRATEJI §9).
setStatus("ok");
```

⚠ Bunun ağırlığı şudur: `/api/newsletter` rotasının **kendi başlık
yorumu** bu yalanın Faz 2.A'da bittiğini söylüyor — üç formdan üçü
bağlanmış, dördüncüsü unutulmuştu. Yani belge "bitti" diyordu, kod
demiyordu.

Şimdi gerçek uca bağlıdır, `loading`/`error` durumları vardır ve
`category` etiketiyle kaydeder.

### ✅ ② Dış bağ "kırık iç bağ" sayılıyordu — **DÜZELTİLDİ** (kitap tarafı)

`04_BUILD/kindle.py` her `href`i EPUB paketi içinde arıyordu. Doğrulama
adresi gerçek bir bağa dönüşünce kapı onu kırık saydı. Artık mutlak
adresler ayrı ölçülür ve **HTTPS zorunludur**.

### ⚠ ③ Depo adı ile Vercel bağlantısı ayrışıyor — **AÇIK · KURUCU**

| | |
|---|---|
| Yerel `origin` | `emredogan-cloud/**E**terprise-web-site` |
| Vercel projesinin bağlı olduğu depo | `emredogan-cloud/**En**terprise-web-site` |

GitHub yeniden adlandırılan depoları yönlendirir, bu yüzden **şu an
çalışıyor**. Ama bu bir yönlendirmeye bağımlılıktır ve sessizce kırılır.
Düzeltmesi tek satırdır ve kurucunun deposudur:

```bash
git remote set-url origin https://github.com/emredogan-cloud/Enterprise-web-site.git
```

---

## 5 · Dağıtım durumu — ⛔ **YAYINDA DEĞİL**

Vercel'den **okunan** değerler (tahmin değil):

| | Ölçülen |
|---|---|
| Proje | `enterprise-web-site` (`prj_Futeqpob…`) |
| Takım planı | **hobby** |
| `live` | **`false`** |
| En yeni dağıtımın hedefi | **`target: null`** (üretim **değil**) |
| En yeni dağıtım tarihi | **~4 Haziran 2026** |
| Özel alan adı | **YOK** |
| Verilen alan adları | yalnızca `*.vercel.app` |

⭑ **BUNUN ANLAMI:** `https://valicepress.com/codex-enigmatica/verify`
**şu anda mevcut değildir.** Kitap o adresi basacaktır; adres, kurucu
① alan adını alana ② siteyi üretime yükseltene kadar **ölüdür**.

`04_BUILD/qa_verification.py` bunu belgeyle değil **mekanizmayla**
tutar: `release` kapısı üçü de tamamlanmadan **KIRMIZIDIR**.

---

## 6 · Bu oturumda siteye eklenenler

| Dosya | İş |
|---|---|
| `src/app/codex-enigmatica/layout.tsx` | sinematik kabuk |
| `src/app/codex-enigmatica/verify/page.tsx` | sayfa (Server Component) |
| `src/app/api/codex-enigmatica/verify/route.ts` | uç nokta |
| `src/lib/codex-verify.ts` | normalizasyon + biberli özet |
| `src/lib/codex-verify-client.ts` | tarayıcı yardımcısı |
| `src/components/codex/verify-form.tsx` | form + başarı paneli |
| `scripts/codex-verify-digest.mjs` | biber + özet üretici (STDIN) |
| `src/lib/codex-verify.test.ts` | 17 test |
| `src/app/api/codex-enigmatica/verify/route.test.ts` | 15 test |
| `src/app/api/newsletter/route.test.ts` | **20 test** (rota daha önce testsizdi) |

**Değiştirilenler:** `src/lib/analytics.ts` (iki olay), `.env.example`,
`/api/newsletter` (`source` etiketi), üç bülten formu (etiketleme),
`category-sidebar.tsx` (gerçek abonelik).

**Değiştirilmeyenler:** çatı, yönlendirme mimarisi, tasarım sistemi,
ticaret hattı, kimlik hattı, veri şeması. Yönerge § 19 bunu istedi.

---

## 7 · Ölçülen sağlık

```
npm test    →  9 dosya · 105 test · hepsi yeşil
npm run lint →  temiz
npm run build → temiz · /codex-enigmatica/verify  ○ (Static)
npx tsc --noEmit → temiz
```

Cevap sızıntısı taraması (cevap · biber · özet):

```
.next/static  (tarayıcıya inen)  → 0 · 0 · 0
.next/server  (sunucu derlemesi) → 0 · 0 · 0
```
