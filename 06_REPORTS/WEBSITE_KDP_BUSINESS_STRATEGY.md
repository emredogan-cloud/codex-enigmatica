# WEBSITE + KDP İŞ STRATEJİSİ

> **27 Ağustos 2026** · B2 yönergesi § 8–16 · § 22 · § 23
>
> ## Bu belgedeki her satır üç etiketten birini taşır
>
> | Etiket | Anlamı |
> |---|---|
> | 🅢 **KAYNAK GERÇEĞİ** | birincil kaynaktan **alıntı**; bağı verilmiştir |
> | 🅡 **ÖNERİ** | benim çıkarımım — **kaynak değildir**, tartışılabilir |
> | 🅕 **KURUCU KARARI** | benim veremeyeceğim karar |
>
> ⚠ İkincil kaynaklar (blog, rehber) **ayrıca** işaretlidir. Bir rehberin
> özeti hukuk değildir ve bu belgede hukuk yerine geçmez.
>
> ⛔ **Bu belge hukuki ya da mali tavsiye değildir.** Basıma ve veri
> toplamaya dair kararlar için nitelikli danışman gerekir.

---

# BÖLÜM I — KDP GERÇEKLERİ

## 1 · ⭑ KDP alıcı e-postası VERMEZ ⭑

🅢 **KAYNAK GERÇEĞİ** — KDP Şartlar ve Koşulları, **§ 6**, birebir:

> *"We retain sole ownership and control of all data obtained from
> customers and prospective customers in connection with the Program."*

🅢 **KAYNAK GERÇEĞİ** — aynı sözleşme, **§ 5.3.4**:

> *"we have sole and complete discretion to set the retail customer price
> at which your Books are sold through the Program. We are solely
> responsible for processing payments, payment collection, requests for
> refunds and related customer service."*

→ [KDP Terms and Conditions](https://kdp.amazon.com/en_US/help/topic/G200627430)

🅡 **ÖNERİ · sonuç:** Kurucunun **alıcı listesi yoktur ve olmayacaktır.**
Amazon müşteri ilişkisinin sahibidir; kurucu telif alan tedarikçidir.

⛔ **Bu yüzden şunların hiçbiri yapılmadı ve yapılmamalıdır:**
Amazon'u kazımak · KDP alıcılarını kimliklendirmeye çalışmak · Amazon
müşteri verisini izinsiz içe aktarmak · gizli izleme · elimizde olmayan
bir e-posta erişimine sahipmiş gibi davranmak.

### 1.1 · Elde kalan tek dürüst yol

🅡 **ÖNERİ:** Liste **alıcıdan değil, okurdan** kurulur — ve okurun
Amazon'dan çıkıp bize gelmesi için bir **sebebi** olmalıdır. Codex
Enigmatica'da o sebep zaten vardır ve tasarımın kendisidir:

> Son sorunun cevabı kitapta **yoktur**. Okur onu doğrulamak için
> doğrulama sayfasına **gelmek zorundadır**.

Bu, izleme değildir: okur kendi ayağıyla gelir, ne istediğini bilir, ve
abonelik **isteğe bağlıdır**. Kitabı bitirmiş bir okur, ana sayfadan
gelen bir ziyaretçiden **maddeten farklı** bir kitledir — ve bu fark
`codex-verify` etiketiyle kaydedilir.

⚠ Ama şu abartılmamalı: doğrulama sayfasına gelen herkes abone olmaz ve
olmamalıdır. Yönerge § 15: *"Do not force email collection just to verify
an answer."*

---

## 2 · Kitabın içine adres basmak serbest mi

🅢 **KAYNAK GERÇEĞİ** — KDP Hyperlink Guidelines: dış bağlar okur
deneyimini doğrudan geliştiriyorsa kabul edilir; kabul edilen kullanımlar
arasında **"ek yardımcı malzemeye"** bağlar ve **yazarın kendi
sitesine/sosyal hesabına** bağlar açıkça sayılır.

🅢 **KAYNAK GERÇEĞİ** — aynı belge, kırık bağlar için: elde olmayan
sebeplerle kırılan dış bağlar **devre dışı bırakılmalı** ve yanına
*"(URL inactive)"* gibi bir not konmalıdır.

→ [Hyperlink Guidelines](https://kdp.amazon.com/en_US/help/topic/GQ6JQ7FM6C72HE4X)

🅡 **ÖNERİ:** Doğrulama sayfası tam olarak *"ek yardımcı malzeme"*
tanımına oturur. Bu yüzden Kindle sürümünde adres **gerçek bir HTTPS
bağdır** (ilk yapıda düz metindi; gerekçesi yanlıştı ve düzeltildi).

⚠ Ve ikinci alıntı, alan adı kaydının neden `release` kapısında zorunlu
olduğunu Amazon'un kendi ağzından söyler: **Amazon kırık bağı bir kalite
kusuru sayar.** Basılı kitapta ise "devre dışı bırakmak" diye bir şey
yoktur.

---

## 3 · YZ içerik beyanı — **B3, AÇIK**

🅢 **KAYNAK GERÇEĞİ** — KDP, yeni bir kitap yayımlarken ya da mevcut bir
kitabı düzenleyip yeniden yayımlarken **YZ-üretimi** içeriğin (metin,
görsel, çeviri) bildirilmesini **ister**. **YZ-destekli** içeriğin
bildirilmesi gerekmez. Kapak ve iç görseller "görsel" kapsamındadır.

→ [Content Guidelines](https://kdp.amazon.com/en_US/help/topic/G200672390)

🅕 **KURUCU KARARI · B3:** `project_config.json` şu an iki alanı **boş**
tutuyor ve doldurmayı reddediyor:

```
founder.isbn.paperback          → null
founder.isbn.hardcover          → null
founder.aiDisclosure.founderConfirmed → false
```

⚠ Bu boşluk **kasıtlıdır ve doğrudur**: yer tutucu bir ISBN basmak geri
alınamaz bir hatadır, ve YZ beyanı kurucunun kendi üretim sürecine dair
**onun bileceği** bir beyandır. Ajan bunu dolduramaz ve doldurmadı.

⛔ **B3 AÇIKTIR.** Bu rapor onu kapatmıyor.

---

# BÖLÜM II — E-POSTA LİSTESİ

## 4 · Tek ana liste + etiket · **uygulandı**

🅡 **ÖNERİ (uygulandı):** Bir liste, çok kaynak. **İkinci bir liste,
ikinci bir abonelikten çıkma yüzeyidir**; "bültenden" çıkıp "Codex
listesinden" mektup almaya devam eden bir okur segmente edilmemiş,
**yok sayılmıştır**.

🅢 **KAYNAK GERÇEĞİ** — Resend Contacts API `email`, `firstName`,
`lastName`, `unsubscribed` alanlarına **ek olarak** özel özellikler
(*custom properties*), **segmentler** ve **konular** (*topics*, `opt_in` /
`opt_out`) kabul eder.

→ [Resend · create contact](https://resend.com/docs/api-reference/contacts/create-contact)

🅡 **ÖNERİ · sonuç:** Yeni bir satıcıya gerek yok. Tek Audience + özel
özellik yeterlidir. Şu an kaydedilenler:

| Alan | Değer | Nereden |
|---|---|---|
| e-posta | normalize (küçük harf, kırpılmış) | form |
| `source` | `home` · `article` · `category` · `codex-verify` | **kapalı liste** |
| `signup_purpose` | `product-updates` | sabit |
| `unsubscribed` | Resend'in kendi alanı | sağlayıcı |
| zaman damgası | Resend kaydı | sağlayıcı |

⚠ **Kapalı liste neden:** `source` tarayıcıdan gelir, yani **güvenilmez
girdidir**. Serbest bir dizeyi kişi kaydına yazmak, çağıranın kayda ne
isterse yazması demektir. Listede olmayan değer **düşürülür, abonelik
reddedilmez** — kötü etiket bizim hatamızdır, abonenin değil.

### 4.1 · Bilerek toplanmayanlar

⛔ IP adresi · tarayıcı imzası · **ülke** · yönlendiren · cihaz kimliği.

🅡 **ÖNERİ:** Yönerge "country if lawfully necessary" diyordu — ve şu an
**gerekli değildir**. Ülke, ancak bir gün ülkeye göre farklı içerik ya da
farklı rıza rejimi uygulanırsa gerekir. O gün gelmeden toplamak, bir
posta listesini bir **gözetim kaydına** çevirmektir.

---

## 5 · Rıza — ne gerekiyor

🅢 **KAYNAK GERÇEĞİ** — GDPR **md. 4(11)**: rıza *"freely given, specific,
informed and unambiguous"* olmalı ve *"a clear affirmative action"* ile
verilmelidir. **md. 7(1)**: veri sorumlusu rızayı **ispat edebilmelidir**.
**md. 7(3)**: geri çekmek, vermek kadar kolay olmalıdır.

🅢 **KAYNAK GERÇEĞİ** — ABD **CAN-SPAM**: ticari e-postada geçerli fiziksel
posta adresi, aldatıcı olmayan konu satırı ve **işleyen bir çıkış
mekanizması** zorunludur.

🅜 *ikincil kaynak* — çift onay (double opt-in) GDPR'ın **zorunlu tuttuğu**
bir şey değildir; ama rızanın ispatını güçlendirdiği için yaygın olarak
önerilir.
→ [TermsFeed](https://www.termsfeed.com/blog/gdpr-double-opt-in-email-marketing/) ·
[Mailgenius](https://www.mailgenius.com/gdpr-email-marketing/)

### 5.1 · Şu an sağlananlar ve sağlanmayanlar

| | Durum |
|---|---|
| Ön işaretli kutu yok | ✅ |
| Rıza, doğrulamadan **ayrı** bir eylem | ✅ |
| Amaç yazılı (*"when the next one is built"*) | ✅ |
| Abonelikten çıkma | ✅ Resend altyapısı |
| `signup_purpose` kaydı | ✅ |
| **Çift onay** | ❌ **yok** |
| **Gizlilik metninde Codex akışının adı** | ❌ **yok** |
| **CAN-SPAM fiziksel adresi** | ❌ 🅕 **kurucu** |

🅡 **ÖNERİ (uygulanmadı — § 19 kapsam dışı):** İlk gerçek gönderimden
**önce** çift onay eklenmeli ve gizlilik metnine `codex-verify` kaynağı
işlenmelidir. Kapsam sınırı yüzünden yapılmadı; **açık iş olarak
kaydediyorum.**

🅕 **KURUCU KARARI:** Bültende kullanılacak **fiziksel posta adresi**.
CAN-SPAM bunu ister ve bir ajan bir adres uyduramaz.

---

# BÖLÜM III — KAMU MALI KATALOG STRATEJİSİ

> ⚠ Yönergenin en sert cümlesi buradaydı:
> **"Do NOT treat 'old' as equivalent to 'public domain.'"**
> Aşağıdaki her satır o cümleyi korumak içindir.

## 6 · "Eski" ile "kamu malı" aynı şey değildir

🅢 **KAYNAK GERÇEĞİ** — Cornell Kamu Malı tablosu (ABD'de yayımlanmış
eserler), **2026 itibarıyla**:

| Yayım yılı | Durum |
|---|---|
| **1931'den önce** | **kamu malı** (telif süresi doldu) |
| 1931–1963 · künyeli **ve yenilenmiş** | yayımdan **95 yıl** — **hâlâ korumalı** |
| 1931–1963 · künyeli ama **yenilenmemiş** | **kamu malı** |
| 1964–1977 · künyeli | yayımdan **95 yıl** — **hâlâ korumalı** |
| 1978 – 1 Mart 1989 · künyesiz ve 5 yıl içinde tescilsiz | **kamu malı** |

→ [Cornell · Copyright Term and the Public Domain](https://guides.library.cornell.edu/copyright/publicdomain)

⭑ **1931–1963 aralığı bu tablonun tuzağıdır:** aynı yılın iki kitabından
biri kamu malı, öteki 95 yıl korumalı olabilir — fark **yenileme
kaydıdır**, yaş değil. "1940 kitabı, yeterince eski" cümlesi bir tahmindir
ve tahminle basmak dava demektir.

## 7 · Her başlık için ayrı ayrı sorulacak sekiz soru

🅡 **ÖNERİ:** Aşağıdakilerin **her biri ayrı bir haktır** ve biri kamu
malı olduğunda ötekiler olmayabilir.

| # | Katman | Tuzak |
|---|---|---|
| 1 | **Eserin telif durumu** | yenileme kaydı · künye · yıl |
| 2 | **Basım hakları** | modern eleştirel basımın **editoryal aygıtı** kendi telifini taşır |
| 3 | **Çeviri** | çevirinin **kendi** telif süresi vardır — çevirinin tarihine göre |
| 4 | **Şerh / dipnot** | özgün katkıdır, korumalıdır |
| 5 | **İllüstrasyon** | metin kamu malı olsa da **çizimler** olmayabilir |
| 6 | **Kapak / tasarım** | ayrı eser · ayrı hak |
| 7 | **Marka** | ⭐ aşağıya bak |
| 8 | **Yargı yetkisi** | ABD 95 yıl · AB **yaşam + 70** — aynı eser bir ülkede serbest, ötekinde korumalı olabilir |

### 7.1 · Marka tuzağı

🅜 *ikincil kaynak* — Telif ile marka **farklı işler görür**: telif ifadeyi
korur, marka **kaynağı gösterir**. Bir karakter kamu malına girdiğinde
adı, logosu ve ticari kullanımdaki ayırt edici unsurları **marka olarak
korumalı kalabilir**. Winnie-the-Pooh'un 1926 kitabı kamu malıdır; Disney
tasvirleri hem telif hem marka ile korumalıdır.
→ [IPWatchdog](https://ipwatchdog.com/2022/02/22/public-public-domain-winnie-pooh-illustrates-copyright-limitations-public-domain-works/) ·
[Duke CSPD](https://web.law.duke.edu/cspd/publicdomainday/2023/bcvpd/)

🅡 **ÖNERİ:** "Telif doldu" **kapak ve başlıkta o adı kullanabilirim**
demek değildir.

## 8 · Ve KDP'nin kendi kamu malı rejimi

🅢 **KAYNAK GERÇEĞİ** — KDP, mağazada ücretsiz bir sürümü bulunan kamu
malı başlıklar için **yalnızca farklılaştırılmış** sürüme izin verir.
Kabul edilen üç farklılaştırma:

| Tür | KDP'nin şartı |
|---|---|
| **Translated** | özgün çeviri |
| **Annotated** | özgün şerh (çalışma rehberi, eleştiri, ayrıntılı biyografi, tarihsel bağlam) |
| **Illustrated** | **10 veya daha fazla** özgün ve ilgili illüstrasyon |

Başlık alanında `(Translated)`, `(Annotated)` ya da `(Illustrated)`
**bulunmalıdır**; ürün açıklamasının başında özgünlüğün madde imli
özeti (**en fazla 80 karakter**) istenir.

🅢 **Farklılaştırma SAYILMAYANLAR:** bağlantılı içindekiler · biçimlendirme
iyileştirmesi · derleme · fiyat/satış sırası farkı · internette serbestçe
bulunan içerik.

🅢 **Ve bir ekonomik kısıt:** *"Public domain content is not eligible for
all eBook royalty options or KDP Select."*

→ [Publishing Public Domain Content](https://kdp.amazon.com/en_US/help/topic/G200743940)

🅡 **ÖNERİ · sonuç:** Kamu malı bir katalog, **telif oranı düşük ve
KDP Select dışı** bir katalogdur. Bu, onu kötü bir fikir yapmaz — ama
Codex Enigmatica'nın ekonomisiyle **aynı modele oturtulamaz**, ve bunu
planlamadan önce bilmek gerekir.

⚠ Bu depoda `/categories/pd-spine` adında bir rota **zaten vardır**. Yani
kamu malı fikri sitede başlamış durumda. Bu belge onu **kapsam dışı**
bırakıyor (§ 19) ama üstündeki sekiz katmanın **her başlık için** ayrı
ayrı yanıtlanması gerektiğini kayda geçiriyor.

---

# BÖLÜM IV — AÇIK KALANLAR

| # | İş | Kime ait |
|---|---|---|
| 1 | `valicepress.com` alan adı kaydı | 🅕 **kurucu** (ödeme) |
| 2 | Sitenin üretime yükseltilmesi | 🅕 **kurucu** |
| 3 | Vercel sırları (`CODEX_VERIFY_*`) | 🅕 **kurucu** |
| 4 | **B1** · harici çözücü oturumları | 🅕 **kurucu + 5 insan** |
| 5 | **B3** · ISBN + YZ beyanı | 🅕 **kurucu** |
| 6 | **A7** · 101 cevap alanı biçim kararı | 🅕 **kurucu** (öneri: hayır · § I·1) |
| 7 | Çift onay + gizlilik metnine `codex-verify` | 🅡 ilk gönderimden önce |
| 8 | CAN-SPAM fiziksel adresi | 🅕 **kurucu** |
| 9 | Kamu malı katalog · başlık başına 8 katman | 🅕 **kurucu** + danışman |
| 10 | `git remote` yazım düzeltmesi | 🅡 tek satır |
