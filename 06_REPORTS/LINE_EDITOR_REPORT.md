# LINE EDITOR RAPORU — Codex Enigmatica · Faz 5

> **24 Ağustos 2026** · Yol haritası Faz 5 § 2 ve § 13 gereği.
>
> Üç **bağımsız** line editor alt-ajanı, okurun gördüğü metnin tamamını
> (ön madde · 17 ısınma örneği · 5 kapı açılışı · 101 bulmaca sayfası ·
> kapanış · arka madde — **17.877 kelime**) taradı. Hiçbiri çözümleri ya
> da ipuçlarını görmedi: işleri ifadeyi ve belirsizliği ölçmekti, cevabı
> bilmek değil.
>
> ## ⚠ ALT-AJAN KÖRÜ KÖRÜNE KABUL EDİLMEZ
>
> Yol haritası Faz 5 § 13'ün kendi sözü: *"Line Editor bir alt-ajandır
> ve körü körüne kabul edilmez."* Aşağıdaki her bulgu ana ajan
> tarafından **kodla doğrulanmış** ya da **gerekçesiyle reddedilmiştir**;
> hangisi olduğu her maddede yazılıdır.
>
> Hiçbir alt-ajan bir kapıyı zayıflatmayı önermedi ve önerseydi
> uygulanmazdı (§ 12: *"The sub-agent MUST NOT directly weaken gates"*).

---

## Toplam

| | BLOCKING | MAJOR | MINOR |
|---|---:|---:|---:|
| Ön madde · ısınma · açılış · kapanış · arka madde | 5 | 22 | 17 |
| Kapı I–II bulmaca sayfaları (40) | 11 | 18 | 8 |
| Kapı III–V + son soru (61) | 7 | 12 | 14 |
| **TOPLAM** | **23** | **52** | **39** |

---

## ⭑ EN AĞIR BULGU: TEKİLLİK İSPATI DAİRESELDİ ⭑

Editör `g2-016`'nın **iki cevabı olduğunu** bildirdi. Doğruladım ve
sebep bildirilenden daha kötü çıktı:

```
"filters": [ {"col": "<okurun sütunu>", "op": "==", "value": "…"},
             {"col": "<take sütunu>",   "op": "==", "value": "…"} ]
```

İkinci süzgeç `take` sütununa yazılmıştı ve **değeri bulmacanın kendi
cevabıydı**. (Değerler burada YAZILMAZ: bu rapor takip edilen bir
dosyadır ve kanarya ilk taslağı yakaladı — haklıydı.) Yani cevap uzayı, tekilliği
ispatlarken cevabı kendi süzgeci olarak kullanıyordu — ve `qa_answerspace`
bu yüzden yeşil yanıyordu. Okurun elinde böyle bir süzgeç yok: sayfa ona
yalnızca `komşu` sütununu veriyor ve o sütun **iki satır** bırakıyor.

> **Bir tekillik ispatı, ispatladığı şeyi varsayamaz.**

---

## 1 · DOĞRULANDI VE ONARILDI — bloklayıcılar

Her satır kodla ölçüldü; ölçüm komutu ve sonucu yanındadır.

| # | Bulgu | Ölçülen | Onarım | Kapı |
|---|---|---|---|---|
| 1 | **Tekillik ispatı daireseldi** — `take` sütununa cevabın kendisi süzgeç olarak yazılmıştı | 1 bulmaca · okur 2 satırla kalıyordu | Çizelge kitabın kendi yordamıyla onarıldı (akran satırlar anahtarı ekli sayıyla taşır) | `qa_answerspace` süzgeci ATIYOR |
| 2 | **Üç kapı bulmacası çözülemezdi** — levha yön sütunu basmıyordu | g2-020 5 · g4-020 5 · g5-020 16 satır SONDAN sayılıyor | Yön sütunu basılıyor; tek yönlü levhalar yönü açıkça söylüyor | — |
| 3 | **Sayı sütunu cevabı ele veriyordu** | **7 / 7** levhada cevabın numarası uçta | Akranlar cevabın katalog konumunun etrafından seçiliyor · ölçülen 0/7 | `qa_editorial § ⑥` |
| 4 | **Kitap OLMAYAN bir hatayı vaat ediyordu** — "ters sıra ad vermez" | **7 / 7** bulmacada ters sıra AYNI cevabı veriyor | Doğru olan yazıldı; zorluk düşmedi | `qa_editorial § ⑦` |
| 5 | **Öğretilmemiş işlem** — üç levha "ayna ekseni" basıyor | 3 levha · kitapta hiçbir yerde öğretilmiyordu | w13 ve şifre referansı öğretiyor | `qa_experience § 7b` |
| 6 | **Okur sayfasında yapım kimliği** (`g4-001`) | 6 sayfa | Sıra sayısına çevrildi ("BU KAPININ BİRİNCİ bulmacası") | `qa_editorial § ①` |
| 7 | **Aynı çizelge sayfada iki kez** | 6 sayfa | Çizelge tek yerde | `qa_editorial § ②` |
| 8 | **İki bulmaca aynı levhayı basıyor** | 2 çift | Anlatı sözcük numarası aile sırasından türer; çevrim levhası hedef katalogu basar | `qa_editorial § ③` |
| 9 | **Tekrarlanan başlık** | 5 ad (biri ×3) | Kapı III–V başlıkları yeniden adlandırıldı | `qa_editorial § ④` |
| 10 | **Anlatı satırında mekanik** | 3 sayfa (yön/mekanizma) | Yeniden yazıldı | `qa_editorial § ⑤` |
| 11 | **Anlatı, levhanın bastığı sayıyla çelişiyordu** | 3 sayfa | Sıra sayıları başlıklardan çıkarıldı | `qa_editorial § ⑤b` |
| 12 | **Ön madde çizelge sayısını yanlış veriyordu** | 16 denmiş · basılı 15 | Sayı ölçümden geliyor | — |
| 13 | **Isınma sırası bozuktu** — w8, w7'den önce | — | Sıra numaradan türer | — |
| 14 | **Beş kapı açılışı çizelgesini anmıyordu** — ön madde bunu SÖZ VERİYOR | 5 / 5 | Açılışlar yeni çizelgelerini adıyla anıyor | `qa_crossref § ⑤` |
| 15 | **Sözleşme ↔ çözüm bölümü çelişkisi** | — | Çözüm girişi yeniden yazıldı | — |
| 16 | **Kapı bulmacası çizelgesini anmıyordu** | Kapı III–V | Adıyla anılıyor (Türkçe ek okunuşa göre) | `qa_crossref § ①` |
| 17 | **w11 · çözülmüş örnek kendi şeklinden doğrulanamıyordu** | 4 adımın 4'ü görünmeyen harfe gönderme | İki alfabe satırı tam basılıyor | `qa_plate_readability § ②` |
| 18 | **w12 + yol levhaları · işaret yanlış gözü gösteriyordu** | 7 levha | İşaret satırın başında | — |
| 19 | **w15 · sonucun hangi çizelgede aranacağı yoktu** | — | "Sonuç DAİMA artı işaretli çizelgede" | — |
| 20 | **w10 · Çizelge J hakkında yanlış iddia** | çizelge 40 satır · tam tur 260 | Kapsam yazıldı | — |
| 21 | **w7 cevapla kapanmıyordu** — giriş "cevaplarıyla birlikte" der | 17 örneğin 1'i | Kapanıyor ve ibare mekanizmasını söylüyor | — |
| 22 | **Doğrulama sayfası hiç tanıtılmıyordu** — okura 5 kez gönderme yapılıyor | — | Sözleşmede tanımlandı | — |
| 23 | **Sözleşme "sözlük yok" derken kitabın çizelgesi Sözlük'tü** | — | Açıklama yeniden yazıldı | — |

### Ayrıca onarılan — görsel denetimden (line editor dışı)

| Bulgu | Ölçülen | Kapı |
|---|---|---|
| Anahtarlı alfabe levhası **bir CEVABI** basıyordu | 2 kapıda | üretim anında `assert_keys_clean` |
| Basılabilir genişliği aşan şekil | 9 satır (67–79 / tavan 62) | `qa_plate_readability § ②` |
| Dingbat/emoji/teknik bloğundan glif | 15 glif · 61 karakter | `qa_plate_readability § ⑦` |
| Aynı rol için altı ayrı ok karakteri | 6 → 2 | `qa_plate_readability § ⑩` |
| Sayılan işaretle dolgu karışıyordu (`◦` ↔ `·`) | 1 levha | `qa_plate_readability § ⑥` |
| Kutu bir sütun kayıyordu | 26 kutu · 3 üreteç | — |
| Okur **dosya anahtarı** görüyordu (`esik-alfabesi`) | Kapı V yapı levhaları | üretim anında çöker |
| Izgara dolgusu kitabın alfabesinde OLMAYAN harfler taşıyordu | X · Q · W | — |
| **Kanarya yeni dosyayı görmüyordu** | 5 cevap commit edildi · CI kırmızı | kapsam: takip edilen **+ eklenecek** |

---

## 2 · DOĞRULANDI VE REDDEDİLDİ

| Bulgu | Neden reddedildi |
|---|---|
| *"g1-013 ve g1-017'de levhada şifreli dize YOK"* | Dize okur sayfasının `input` alanında BASILI ("dört harflik dize: …"). Şeklin onu tekrarlaması gerekmez. |
| *"STYLE § 1 gereği anlatıdaki her sayı kusurdur"* | Kural harfi harfine **34 sayfayı** kırmızı yakıyordu ve çoğunluğu anlatı sıralamasıydı ("İkinci yol"). Kural ölçüye göre daraltıldı ve daraltıldığı yazıldı (**K42**); sıra sözcüğünün geçtiği bir fikstürle de ölçülüyor. |

---

## 3 · KABUL EDİLDİ — AMA BU FAZDA UYGULANMADI

Aşağıdakiler **geçerli bulgulardır** ve reddedilmiş değildir. Faz 5'te
uygulanmadılar; gerekçeleri tek tek yazılıdır.

| Bulgu | Neden ertelendi |
|---|---|
| Kapı I'in **dört kısa cevabı** kitabın söz dağarcığıyla çarpışıyor (adları K41'de) | **K41.** O yirmi bulmaca ÖLÇÜLEN öldürme kapısının kanıt tabanıdır (A12 · 1/5). Onları değiştirmek, ölçümün ölçtüğü nesneyi değiştirmek olurdu. Kural ileriye dönüktür. |
| Kapı IV'te dört yol sayfası birbirinin kopyası | Mekanizma yeniden tasarımı gerektirir ve `qa_effort`/K36 tavanlarını yeniden ölçmeyi zorunlu kılar. Faz 6 öncesi tasarım kararı. |
| Yaratık çizelgelerinde olgusal tuhaflıklar (kanatsız kartal vb.) | Katalog içeriği kurucu onayına bağlı (A2 · beş kapı teması). |
| `çember`/`halka` · `şerit` iki mekanizma için · `Sözlük`/`Katalog` | Terim birleştirmesi çizelge adlarını değiştirir ve **her kısıt cümlesine** dokunur; ayrı ve ölçülebilir bir geçiş ister. |
| `g2-010`, `g2-011`, `g2-015`, `g2-018`, `g1-003`, `g1-010` şekil/metin ayrışmaları | Altısı da Kapı I–II'dedir ve levha mekaniğine dokunur; öldürme kapısının ölçtüğü kohort. |
| `■` işareti istasyona bitişik değil | Levha yerleşimi; Faz 5'in dizgi dondurma adımında ölçülecek. |

> ⚠ **Bu tablo bir savunma değil, bir borç kaydıdır.** Hiçbiri
> "geçersiz" diye işaretlenmedi; her biri bir sonraki fazın girdisidir.
