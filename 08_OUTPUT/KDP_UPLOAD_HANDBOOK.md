# KDP YÜKLEME EL KİTABI — Codex Enigmatica

> ⚠ **BU BELGE BİR ŞEYİN YAYIMLANDIĞINI İDDİA ETMEZ.**
> Aşağıdaki her dosya durumu üretim anında dosya sistemine
> bakılarak doldurulmuştur. `Publish` düğmesine yalnızca
> kurucu basar.

## 0 · Hazırlık

| | |
|---|---|
| Ölçülen sayfa | 263 |
| Bulmaca · kapı · ipucu | 101 · 5 · 303 |
| İşlenmiş levha | 103 / 103 |
| İşlenmiş ön kapak | 2 / 2 |
| İşlenmiş A+ | 6 / 6 |
| Ajan tarafından hazır adım | 3 / 13 |

## 1 · ⭑ YALNIZCA KURUCUNUN YAPABİLECEĞİ İŞLER ⭑

Ajan bunları **yapmadı ve yapamaz**. Yapıldığını iddia eden
bir rapor yanlıştır.

- **KDP hesabına giriş ve panel kullanımı** — Ajan tarayıcıda hesabınıza giremez, giremeyecektir.
- **Previewer'da sayfa sayfa görsel onay** — Bir insanın bakması gerekir; ölçüm bunu değiştirmez.
- **Yapay zekâ içerik beyanı** — Hukuki bir beyandır ve yalnızca siz verebilirsiniz. `metadata.json → founderPending.aiDisclosureConfirmed` HÂLÂ false.
- **ISBN ve yayın hakkı kararı** — `founderPending.isbn` boş. KDP ücretsiz ISBN mi, kendi ISBN'iniz mi?
- **Yazar biyografisi** — `founderPending.authorBio` boş. Yer tutucu basmak geri alınamaz.
- **Fiziksel POD provası (A9)** — Gravürlerin nokta yayılması altındaki davranışı YALNIZCA basılı provada ölçülür. Ekranda kusursuz görünen levha kâğıtta kapanabilir.
- **Publish düğmesi** — Yayımlama kararı kurucuya aittir.
- **A+ içeriğinin moderasyona gönderilmesi** — Amazon insan moderasyonu uygular; ajan gönderemez.

## A · PAPERBACK

### 🔵 İç blok dosyasını hazırla

| | |
|---|---|
| NE YAPACAĞIM | 6×9 inç trim, krem kâğıt, siyah mürekkep iç blok PDF'i. Sayfa modeli 263 sayfa ölçtü. |
| KDP'DE NEREYE | Bookshelf → Create → Paperback → Manuscript → Upload paperback manuscript |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/PAPERBACK/interior.pdf` |
| NE KONTROL EDECEĞİM | Kenar boşluğu (gutter) sayfa sayısına bağlıdır: 263 sayfa için KDP iç kenarda daha geniş pay ister. Levha sayfalarında kırpma olmamalı. |
| BAŞARILI OLURSA | KDP 'Manuscript uploaded successfully' der ve Previewer açılır. |
| DURUM | **HAZIR** |

### 🔵 Kapak dosyasını hazırla

| | |
|---|---|
| NE YAPACAĞIM | Paperback SARMAL kapak (arka + sırt + ön), tek PDF — ÜRETİLDİ. |
| KDP'DE NEREYE | Paperback Content → Book Cover → Upload a cover you already have |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/PAPERBACK/cover.pdf` |
| NE KONTROL EDECEĞİM | Sırt ÖLÇÜLEN sayfa sayısından türetildi. Previewer'da sırt yazısının ortalandığını ve barkod alanının boş olduğunu doğrulayın. |
| BAŞARILI OLURSA | KDP kapağı kabul eder ve Previewer açılır. |
| DURUM | **HAZIR** |

### 🟢 Fiyat ve dağıtım

| | |
|---|---|
| NE YAPACAĞIM | Liste fiyatı 19.99 $ (paperback). |
| KDP'DE NEREYE | Paperback Rights & Pricing |
| NE GİRECEĞİM | 19.99 USD |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Basım maliyeti sayfa sayısıyla değişir; 263 sayfa değişirse telif de değişir. |
| BAŞARILI OLURSA | KDP net telif tutarını gösterir. |
| DURUM | **BEKLIYOR** |

## B · HARDCOVER

### 🔵 İç blok (hardcover)

| | |
|---|---|
| NE YAPACAĞIM | Aynı iç blok, hardcover trim ve pay kurallarıyla. |
| KDP'DE NEREYE | Create → Hardcover → Manuscript |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/HARDCOVER/interior.pdf` |
| NE KONTROL EDECEĞİM | Hardcover'da KDP daha geniş iç pay ve menteşe (hinge) payı ister; paperback dosyası olduğu gibi KULLANILAMAZ. |
| BAŞARILI OLURSA | Yükleme kabul edilir ve Previewer açılır. |
| DURUM | **BEKLIYOR** |

### 🔴 Kapak (hardcover)

| | |
|---|---|
| NE YAPACAĞIM | Hardcover sarmal — sırt ve menteşe payı paperback'ten FARKLIDIR. |
| KDP'DE NEREYE | Hardcover Content → Book Cover |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `08_OUTPUT/HARDCOVER/cover.pdf` |
| NE KONTROL EDECEĞİM | Hardcover sarmalı ayrı şablondur. Paperback kapağı buraya yüklenmez. |
| BAŞARILI OLURSA | Sarmal sanat gelmeden bu adım açılmaz. |
| DURUM | **BEKLIYOR** |

## C · KINDLE

### 🔴 Kindle sürümü — BU PROJEDE KAPALI

| | |
|---|---|
| NE YAPACAĞIM | `metadata.json → editions.kindle.enabled = false`. Kindle bu kitabın mimarisinde açık DEĞİLDİR ve burada açılmaz. |
| KDP'DE NEREYE | — |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Bu kitap basılı levha okumaya dayanır: gravür VERİ taşır ve ekranda yeniden ölçeklenirse sayılabilirliği bozulur. Kindle açılacaksa bu ayrı bir karardır. |
| BAŞARILI OLURSA | — |
| DURUM | **YOK** |

## D · A+ İÇERİK

### 🔵 Altı A+ modül görselini yükle

| | |
|---|---|
| NE YAPACAĞIM | Görseller METİNSİZDİR; başlık ve gövde metni Amazon'un kendi alanlarına yazılır. |
| KDP'DE NEREYE | Bookshelf → ⋯ → Edit A+ Content → Create A+ Content |
| NE GİRECEĞİM | Her modülün başlık ve gövde metni (aşağıda kopyalanabilir). |
| HANGİ DOSYA | `07_ASSETS/web/ (6/6 hazır)` |
| NE KONTROL EDECEĞİM | Modül türü ve piksel ölçüsü kartla aynı olmalı. Görselde metin GÖRÜNMEMELİ. |
| BAŞARILI OLURSA | Önizlemede görsel + metin ayrı ayrı görünür. |
| DURUM | **HAZIR** |

### 🟢 Moderasyona gönder

| | |
|---|---|
| NE YAPACAĞIM | Amazon insan moderasyonu uygular (birkaç gün). |
| KDP'DE NEREYE | A+ Content → Submit for approval |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Reddedilirse gerekçe e-postayla gelir; en sık sebep görselde metin olmasıdır. |
| BAŞARILI OLURSA | Durum 'Submitted' → 'Approved' olur. |
| DURUM | **BEKLIYOR** |

## E · SON ÖNİZLEME

### 🟢 Previewer'da sayfa sayfa bak

| | |
|---|---|
| NE YAPACAĞIM | Özellikle 103 levha sayfası. |
| KDP'DE NEREYE | Paperback/Hardcover Content → Launch Previewer |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Her levhada: kırpılma yok · çizgiler kapanmamış · sayılabilir işaretler sayılabilir · sayfa numarası levhanın üstüne binmiyor. |
| BAŞARILI OLURSA | Previewer hata vermez ve levhalar okunur. |
| DURUM | **BEKLIYOR** |

### 🟢 Fiziksel prova (A9)

| | |
|---|---|
| NE YAPACAĞIM | Basılı prova kopya sipariş edilir. |
| KDP'DE NEREYE | Proof or author copy |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | ⭑ EKRAN PROVASI BUNUN YERİNE GEÇMEZ. Nokta yayılması yalnızca kâğıtta ölçülür. |
| BAŞARILI OLURSA | Elinizde basılı kopya olur ve levhalar ÖLÇÜLEREK doğrulanır. |
| DURUM | **BEKLIYOR** |

## F · FİYAT

### 🟢 Liste fiyatlarını gir

| | |
|---|---|
| NE YAPACAĞIM | Hardcover 29.99 $ · Paperback 19.99 $ |
| KDP'DE NEREYE | Rights & Pricing |
| NE GİRECEĞİM | Yukarıdaki tutarlar |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | Sayfa sayısı değişirse basım maliyeti ve dolayısıyla telif değişir — fiyat modeli 263 sayfaya göre kuruldu. |
| BAŞARILI OLURSA | KDP her pazar için telif tutarını gösterir. |
| DURUM | **BEKLIYOR** |

## G · YAYIMLAMA

### 🟢 Yapay zekâ içerik beyanı

| | |
|---|---|
| NE YAPACAĞIM | KDP, AI kullanımını sorar. Bu bir HUKUKİ BEYANDIR. |
| KDP'DE NEREYE | Paperback Details → AI-Generated Content |
| NE GİRECEĞİM | Kendi doğru cevabınız |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | `founderPending.aiDisclosureConfirmed` = false. Ajan bunu sizin yerinize dolduramaz. |
| BAŞARILI OLURSA | Beyan kaydedilir. |
| DURUM | **BEKLIYOR** |

### 🟢 Publish

| | |
|---|---|
| NE YAPACAĞIM | Yayımlama kararı. |
| KDP'DE NEREYE | Publish Your Paperback Book |
| NE GİRECEĞİM | — |
| HANGİ DOSYA | `—` |
| NE KONTROL EDECEĞİM | ⭑ BU KİTAP HİÇBİR İNSANIN ELİNDE ÇÖZÜLMEDİ. Harici çözücü oturumu: 0/5 (A12b). Ölçülen öldürme kapısı kararı HARD-STOP'tur. |
| BAŞARILI OLURSA | Kitap 24–72 saat içinde yayında olur. |
| DURUM | **BEKLIYOR** |

## H · Panele girilecek alanlar

| Alan | Değer |
|---|---|
| Başlık | Codex Enigmatica |
| Alt başlık | One Hundred Engraved Enigmas and a Single Unbroken Mystery |
| Yazar | Emre Doğan |
| Yayıncı | Vâliçe Press |
| Seri | Codex · cilt 3 |
| Açıklama | One hundred engraved enigmas and a single unbroken mystery.  Five gates. Twenty puzzles each. Every answer is a member of a catalogue printed inside this book — nothing here asks you to leave it.  The ciphers are not printed beside the plates; they are printed INSIDE them. A keystone that is missing |
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
| Yazar biyografisi | ⛔ KURUCU YAZMADI — boş bırakılamaz |
| ISBN | ⛔ KARAR VERİLMEDİ (strateji: kdp-free) |

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
