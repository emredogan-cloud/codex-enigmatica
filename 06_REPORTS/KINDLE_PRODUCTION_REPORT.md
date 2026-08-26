# KINDLE ÜRETİM RAPORU

**Tarih:** 26 Ağustos 2026
**Karar:** Kindle kurucu kararıyla **AÇILDI** (K9 geçersiz kılındı).

## 1 · Mimari — neden akışkan EPUB 3

Üç seçenek vardı ve ikisi ölçülerek elendi:

| Seçenek | Karar | Gerekçe |
|---|---|---|
| Baskı PDF'ini çevir | ⛔ RED | 6×9 sayfayı 6 inçlik ekrana sıkıştırmak 9,5 punto metni okunmaz yapar. Yönerge § 8 açıkça yasaklıyor. |
| Sabit düzen (fixed-layout) | ⛔ RED | Levha için iyi, METİN için felaket: okur yazı tipini büyütemez. Bu kitap 17.648 kelime metin taşıyor. |
| **Akışkan EPUB 3** | ✅ SEÇİLDİ | Metin akar ve büyütülebilir; levhalar tam genişlikte, en-boy korunarak; sayılabilir işaretler ekranda yakınlaştırmayla sayılır. |

## 2 · Üretilen paket

`08_OUTPUT/KINDLE/` → `codex-enigmatica.epub` · `cover.jpg` ·
`metadata.json` · `SHA256SUMS`

| | |
|---|---:|
| EPUB | **46,0 MB** |
| Bölüm | 18 |
| Gömülü gravür | 99 |
| İpucu / çözüm | 303 / **100** (meta hariç) |
| Kapak | **1600 × 2560** (1,6:1) |

**18 denetim yeşil**: mimetype ilk ve sıkıştırılmamış · container ·
OPF · nav · kapak işaretli · her XHTML ayrıştırılabilir · her iç bağ
çözülüyor · baskıya özel terim yok · dil `en`.

⭑ **KAPAK YALNIZCA ÖN.** Sarmaldan ön panel, sarmal geometrisinden
**hesaplanarak** kesildi (kör kırpma değil). Sırt, arka kapak, barkod,
taşma **yok**. Başlık, alt başlık ve yazar aynı ölçülen-karşıtlık
motoruyla basıldı ve **küçük resimde okunur** (120 px'te doğrulandı).

⭑ **Son sorunun cevabı Kindle'da da basılmadı** — kitabın kendi
sözleşmesi. Bir kapı bunu zorlar.

## 3 · ⭑ TELİF PLANI — kitap başına 3,41 $ fark ⭑

KDP'nin **%70** planı teslimat ücreti keser; **%35** planı kesmez.

```
dosya            46,0 MB
teslimat ücreti  46,0 × 0,15 $ = 6,90 $
liste            9,99 $

%70 planı: 0,70 × 9,99 − 6,90 = 0,09 $
%35 planı: 0,35 × 9,99        = 3,50 $
```

⭑ **%35 PLANI SEÇİLMELİDİR.** %70 planı bu dosyada kitap başına
**0,09 $** bırakır — otuz dokuz kat az.

**%70'in kârlı olduğu sınır: ~23,3 MB.** EPUB o boyutun altına
indirilirse (levha çözünürlüğü ya da JPEG kalitesi düşürülerek) %70
planı yeniden değerlendirilebilir; şu hâliyle **hayır**.

Bu bulgu el kitabına da yazıldı — kurucunun panelde plan seçerken
görmesi gerekiyor.

## 4 · Alıcı bilgilendirmesi (§ 9)

Ürün açıklamasının sonuna eklenecek metin — **özür değil, tarif**:

> **About this digital edition** — This is the complete Codex
> Enigmatica: all 101 puzzles, all 303 hints and the full solution
> section. Every engraved plate is reproduced digitally and can be
> enlarged on screen to examine the fine detail each puzzle depends on.
> The puzzles are solved by observation and inference, so nothing here
> requires you to write in the book. If you prefer to annotate the
> plates by hand, or want the engravings at their printed size, the
> paperback and hardcover editions are made for that.

Ne yapmadığına dikkat: caydırmıyor, özür dilemiyor, olmayan bir
etkileşim vaat etmiyor ve "yazamazsınız" demiyor — baskı sürümünün
**kimin için** olduğunu söylüyor.

## 5 · ⛔ Açık kalan

**EPUB Türkçedir** (3.091 Türkçe sözcük ölçüldü). Kurucu kararı gereği
ticari kitap İngilizce olmalıdır; dönüşüm yapılmadan Kindle
yüklenmemelidir. Ayrıntı: `06_REPORTS/FINAL_LANGUAGE_AND_FORMAT_REPORT.md`

`epubcheck` bu makinede kurulu değil; doğrulama kendi yapısal
kapılarımızla yapıldı (XML ayrıştırma, manifest, bağlar, mimetype).
**Resmî epubcheck koşturulmadı ve koşturulmuş gibi bildirilmiyor.**
