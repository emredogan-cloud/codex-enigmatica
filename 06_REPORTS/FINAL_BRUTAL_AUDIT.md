# FINAL BRUTAL AUDIT — Codex Enigmatica

> **26 Ağustos 2026** · İngilizce ticari sürüm
>
> Bu belge kitabın **iyi taraflarını anlatmaz.** Yalnızca şunu sorar:
> *bu kitap bugün KDP'ye yüklenirse ne kırılır?*
>
> ⚠ Cevap taşımaz.

---

## 1 · KARAR

> ### ⛔ KDP'YE YÜKLENEMEZ — üç bloklayıcı var, üçü de KURUCUYA ait.
>
> Ajanın yapabileceği her iş bitti ve bütün kalite kapıları `release`
> seviyesinde yeşil. Bloklayıcılar teknik değil; **doğrulama ve altyapı**.

| # | bloklayıcı | sahibi | neden ajan çözemez |
|---|---|---|---|
| **B1** | Hiçbir insan bu bulmacaları çözmedi | kurucu (A12b) | insan gerektirir |
| **B2** | Doğrulama sayfası yok — son sorunun cevabı hiçbir yere yazılamaz | kurucu (A4) | barındırma gerektirir |
| **B3** | ISBN ve AI açıklaması boş | kurucu | KDP paneli |

---

## 2 · B1 · ÖLDÜRME KAPISI HÂLÂ HARD-STOP

```
Çözücü belirlendi      5 / 5
Oturum YAPILDI         0 / 5      ⛔
Kapı I'i bitiren       ÖLÇÜLMEDİ
Medyan tamamlama       ÖLÇÜLMEDİ
KARAR                  HARD-STOP
```

**Ve İngilizce yeniden inşa bunu DAHA DA GERİYE ALDI.** Türkçe pilot en
azından Türkçe konuşan çözücüler için ölçülebilir hâldeydi. Şimdi
ölçülecek şey İngilizce bir kitaptır ve o kitabın **hiçbir cümlesi, hiçbir
cevabı, hiçbir şifresi** pilottakiyle aynı değildir.

> Bir yeniden inşa, doğrulamayı devralmaz. Sıfırdan gerektirir.

`internalSolverCountsAsEvidence = false` yürürlüktedir: `solve_from_pack`
ve `qa_answerspace` yeşildir ve **kanıt sayılmaz**. İkisi de kitabın
kendi ürettiği veriyle kitabın kendi kabul yordamını çalıştırır.

---

## 3 · KIRILGAN AMA GEÇEN — dört ölçülmüş risk

### ⚠ R1 · Otuz bir levha, kalan yetmiş ikiyle aynı üslupta değil

31 gravürün veri sözleşmesi değişti ve hepsi deterministik olarak yeniden
çizildi (maliyet 0,00 $, sayılar kesin). Kalan 72'si görsel modelden
gelmiş, detay yoğunluğu yüksek gravürlerdir.

* **ölçülen:** üslup sözlüğü ortak — krem zemin (241,228,208), saf siyah
  çizgi, paralel tarama, cetvel çerçeve.
* **ölçülmeyen:** okurun bu farkı "iki ayrı kitap" diye okuyup okumadığı.
* **neden böyle yapıldı:** aynı sözleşme görsel modele üç kez verildi ve
  **8, 12, 12** istasyonla döndü (`OPENAI_14_ENGRAVINGS_COST_REPORT`).
  Yanlış sayılı bir gravür, çözülemeyen bir bulmacadır.
* **maliyeti bilinen alternatif:** 25 levhayı yeniden ısmarlamak
  ~4,20 $ ve **sayıların doğru geleceğinin garantisi yok**.

### ⚠ R2 · Kapak sanatı doğal çözünürlüğün altında

| | ciltsiz | ciltli |
|---|---:|---:|
| gereken | 3 879 × 2 775 px | 4 313 × 3 125 px |
| sanatın doğal dpi'ı | **92,5** | **82,0** |

300 dpi'a yükseltildi ama **kazanılan detay tahmindir**. Baskıda yumuşak
görünebilir. Kurucu daha yüksek çözünürlüklü sarmal üretmedikçe bu risk
kalır (`COVER_ARTWORK_GENERATION_GUIDE`).

### ⚠ R3 · Ciltli hesaplayıcı 263 sayfayla koştu, iç blok 274

Betik sırtı +0,0203 in düzeltti ve bunu **rapor ediyor**. KDP ciltli sırt
toleransı dardır; kurucu `hardcover-calculator.png` değerlerini 274
sayfayla yenilemelidir.

### ⚠ R4 · Kindle %70 planı bu dosyada kayıptır

46,0 MB × 0,15 $ = **6,905 $ teslimat ücreti**. %70 planı 0,088 $ telif
bırakır; %35 planı 3,497 $. **%35 seçilmelidir** — ya da EPUB
~23,3 MB'ın altına indirilmelidir (99 gömülü levha).

---

## 4 · YENİDEN İNŞANIN AÇIĞA ÇIKARDIĞI ONBEŞ KUSUR

Hepsi onarıldı. Hiçbiri İngilizceye özgü değildi — **on beşi de Türkçe
baskıda da vardı** ve tesadüfen görünmüyordu.

### Kapı katmanı (4)

| # | ne olmuştu | neden hiçbir kapı yakalamamıştı |
|---|---|---|
| ① | harf grubu `i // 5` ile hesaplanıyordu | 29 harfte doğru sonucu veriyordu |
| ② | katalog listeleri **çizelge ADINA göre** bulunuyordu | Türkçe adla eşleşiyordu |
| ③ | levha etiket numarası yalnızca tek katalogda aranıyordu | öteki numaralar tesadüfen `0` içeriyordu |
| ④ | çizelge/uzunluk göndermeleri **Türkçe kalıpla** aranıyordu | Türkçe metinde eşleşiyordu |

⭑ ①'in bedeli ölçüldü: yedi bulmaca "0 kabul" olurdu — yani cevap uzayı
kapısı **çözülemez yedi bulmacayı yeşil değil, sessiz** yapardı.

### Dizgi katmanı (11)

| # | ne olmuştu | ağırlık |
|---|---|---|
| ⑤ | `printed: false` çizelge basılıyordu — **son sorunun cevabını içerir** | ⛔ ürünü bitirir |
| ⑥ | on yedi çözülmüş örneğin **şekli ve adımları** hiç basılmıyordu | ⛔ ön maddenin sözü tutulmuyordu |
| ⑦ | ön/arka madde satır başına bir paragraf; kapı açılışları **ham Python listesi** | ⛔ okunamaz |
| ⑧ | sözleşme sözleri ve şifre referansı **Python demeti** olarak | ⛔ okunamaz |
| ⑨ | sözleşme sayfası **kurucuya ait açık iş kaydını** doğrulama adresi diye basıyordu | ⛔ söz tutulmuyordu |
| ⑩ | son soru bölümü iki kez, altında **Kapı V'in açılışı** | ⚠ |
| ⑪ | `**kalın**` işaretleri olduğu gibi basılıyordu | ⚠ |
| ⑫ | levha şekli sayfa sınırında **ikiye bölünebiliyordu** | ⚠ yedi istasyonun dördü/üçü |
| ⑬ | dört arka madde başlığı iki kez | ⚠ |
| ⑭ | Kapı III–V'in 61 sayfasında `AMAÇ` = `GİRDİ` | ⚠ |
| ⑮ | çevrim levhası gönderdiği çizelgenin adını kesiyordu | ⚠ |

⭑ Kök sebep ortaktır ve adı vardır: **iki üretici (baskı ve Kindle) aynı
işi iki ayrı kopyayla yapıyordu.** Yardımcılar tek yere alındı
(`_protected_layer § TYPESETTING`); on beş kusurun sekizi o ayrışmadan
doğmuştu.

### Ve bir tanesi levha çiziciydi

`_mark` dokuz karakteri tanıyordu; Çizelge A'nın **altı işaretinin altısı
da** aynı dolu noktaya düşüyordu. Yazı çözme levhası tam olarak o altı
işaretten kuruludur. Onarıldı: işaretler **çizgiye göre** çizilir.

---

## 5 · NE ÖLÇÜLDÜ, NE ÖLÇÜLMEDİ

| | |
|---|---|
| ✅ ÖLÇÜLDÜ | 101/101 tekil cevap · 5 086 aday dize elendi |
| ✅ ÖLÇÜLDÜ | 719 elle işlem · hiçbiri çaba tavanını aşmıyor |
| ✅ ÖLÇÜLDÜ | çıkarım oranı 1,00 → 4,08 (yükseliyor) |
| ✅ ÖLÇÜLDÜ | ticari yüzeyde **0** Türkçe sözcük — beş dosyada |
| ✅ ÖLÇÜLDÜ | son sorunun cevabı 101 sayfada, 15 çizelgede, 17 örnekte, 5 açılışta **YOK** |
| ✅ ÖLÇÜLDÜ | 143 takip edilen dosyada cevap sızıntısı yok |
| ✅ ÖLÇÜLDÜ | 274 sayfa · 0,6850 / 0,8058 in sırt · KDP preflight |
| ⛔ **ÖLÇÜLMEDİ** | **hiçbir insanın bu bulmacaları çözüp çözemediği** |
| ⛔ **ÖLÇÜLMEDİ** | **mürekkebin kâğıt üzerindeki davranışı** (A9) |
| ⛔ **ÖLÇÜLMEDİ** | 31 tabletin 72 gravürle yan yana nasıl göründüğü |
| ⛔ **ÖLÇÜLMEDİ** | kapak sanatının 300 dpi'a yükseltilmiş hâlinin baskıdaki keskinliği |

---

## 6 · EN SERT SORU

> **Bu kitap bugün satışa çıksa, bir okur onu bitirebilir mi?**

Bilmiyoruz. Ve bu cümle bir alçakgönüllülük gösterisi değil, **ölçümün
kendisidir**: sıfır harici oturum, sıfır insan kanıtı.

Bildiğimiz şu: kitabın kendi kabul yordamı 101 bulmacanın 101'inde tam
olarak bir cevap kabul ediyor, ipucu merdiveni son adımı hiçbir yerde
vermiyor, ve son sorunun cevabı kitabın hiçbir yerinde basılı değil.

Bu, **çözülebilirliğin gerekli koşuludur. Yeterli koşulu değildir.**

---

*— Faz 6 · brutal audit · 26 Ağustos 2026*
