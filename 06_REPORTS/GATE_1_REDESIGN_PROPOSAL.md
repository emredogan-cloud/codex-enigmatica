# KAPI I YENİDEN TASARIM ÖNERİSİ

> **Codex Enigmatica** · 13 Ağustos 2026 · A12 sonrası
>
> ⛔ **ÖLDÜRME KAPISI: `HARD-STOP`** — 5 harici Türkçe çözücüden **1'i**
> Kapı I'i bitirdi. Sert durdurma eşiği **<3**.
>
> ⚠ **BU BİR ÖNERİDİR. YENİ BULMACA YAZILMADI.** Kurucu onayı bekleniyor.

---

## 0 · Kapı çalıştı

Bu fazın amacı yirmi bulmaca yazmak değildi; **bulmaca sisteminin gerçek
insanlarda çalışıp çalışmadığını öğrenmekti.** Öğrendik: çalışmıyor.

Ve öğrenme **ucuz tarafta** oldu — yirmi bulmaca yazılmışken, yüz değil.
Yol haritasının Faz 2'ye öldürme kapısı koymasının tek sebebi buydu.

| | |
|---|---:|
| Kapı I'i bitiren | **1 / 5** |
| Geçme eşiği | ≥ 4 / 5 |
| Sert durdurma eşiği | < 3 / 5 |
| **Karar** | ⛔ **HARD-STOP** |
| Kurucu kararı | **YENİDEN TASARLA** (terk etme) |

---

## 1 · Neden düştü — ve neden hiçbir kapı görmedi

Baskın bırakma sebebi *"çözemedim"* **değildi**:

> *"Mekanik yürütme — özellikle kaydırma, yansıma ve anahtarlı alfabe
> bulmacaları — kâğıt kalemle aşırı **sıkıcı ve yorucuydu**."*

Bulmacalar çözülebilirdi. Üç bağımsız iç çözücü yirmisini de **ipucusuz**
çözdü. Sekiz kalite kapısı yeşildi. Cevap uzayı **20/20 tekildi**.

> ### Ve hiçbiri okurun NE KADAR İŞ YAPACAĞINI ölçmüyordu.

### 1.1 · Ölçüm şimdi var — ve insan raporunu birebir doğruluyor

`qa_effort.py` (Faz 2 sonunda yazıldı) elle yapılan işlem sayısını
**cevap uzayı spesifikasyonundan** hesaplar. Hangi bulmacaların
şikâyet edildiğini **bilmeden** çalıştırıldı:

| Sıra | Bulmaca | Ölçülen | Bütçe | Kat | Çözücüler ne dedi |
|---:|---|---:|---:|---:|---|
| 1 | `g1-006` | 84 EU | 18 | **4,7×** | *"kaydırma"* |
| 2 | `g1-015` | 72 EU | 24 | **3,0×** | *"yansıma"* |
| 3 | `g1-010` | 34 EU | 21 | **1,6×** | *"anahtarlı alfabe"* |

**Aynı üç bulmaca, aynı sırayla.** Model, insan geri bildirimine karşı
kalibre olmuş sayılır.

`g1-006`'nın en kötü hâli **168 elle işlem** — dakikada üç işlemle
**56 dakika**, altı dakikalık bir ★ bulmacası için.

### 1.2 · ⭑ Kök neden: `expectedCompletionMinutes` YANLIŞ ŞEYİ ölçüyordu ⭑

Yazar *"bu fikir ne kadar sürede anlaşılır"* diye tahmin etti.
Okur *"bu işi ne kadar sürede yaparım"* diye yaşadı.

> **Aradaki fark dokuz kattı ve öldürme kapısını o fark düşürdü.**

Alan kavrayışı ölçüyordu, yürütmeyi değil. Ve hiçbir kapı ikisini
ayırmıyordu — çünkü ikincisi hiç tanımlanmamıştı.

### 1.3 · ⭑ İkinci kök neden: tekillik kuralı tembelliği ÖDÜLLENDİRDİ ⭑

`qa_answerspace § minDomainSize: 6` "sayım alanı yeterince büyük olmalı"
der ve bu **doğrudur** — küçük bir alanda tekillik ispatı zayıftır.

Ama ben iki ayrı şeyi karıştırdım:

| İSPATIN saydığı alan | OKURUN gezdiği alan |
|---|---|
| 28 kaydırma — **makine sayar** | 28 kaydırma — **okur kalemle dener** |
| büyük alan = **güçlü ispat** ✅ | büyük alan = **yorucu iş** ⛔ |

Birkaç bulmacayı, okur alanı **elle taransın** diye kurdum. Kural bunu
hiç istememişti. Ve hiçbir kapı okurun alanı gezip gezmediğini sormuyordu.

> **İspat sayar; okur gezmez.** Bu ayrım yeniden tasarımın merkezidir.

### 1.4 · İkinci bırakma sebebi: mantık sıçraması

> *"Mantık sıçraması Kapı I (★) zorluğu için fazla dikti."*

Ölçülebilir bir kusur: **araçlar levhası slot 3'te, çözülmüş tek bir örnek
olmadan** devreye giriyordu. Sayfa modelinde Faz 1'den beri **3 sayfalık
ısınma bölümü** var — ve **hiç yazılmadı**. Okur alfabeyi ilk kez gerçek
bir bulmacada gördü.

---

## 2 · Neyi koruyoruz

Yeniden tasarım her şeyi atmaz. Ölçüm, **neyin çalıştığını** da söylüyor:

| Korunur | Ölçüm |
|---|---|
| Basılı **Eşik Sözlüğü** (K22) | tekilliği hesaplanabilir kılan şey |
| **`answerSpace`** mimarisi | 20/20 tekil, 1.072 aday elendi |
| **Kapı bulmacasının grup damgası** | üç çözücü de "sınıfının üstünde" dedi |
| **Hata tespiti** (asgari Hamming 15) | ölçüldü, iddia edilmedi |
| **Levha gözlemi** ailesi | 5–8 EU · bütçenin yarısı · en yüksek "aha" |
| **Çizelge tabanlı mantık** (`g1-009` tipi) | 15 EU · bütçenin altında |
| 29 harflik alfabe | sorun alfabe değil, onu **taramak** |

⚠ **Alfabe kalır.** 29 harflik çizelge kitabın kimliğidir ve Kapı II–V
ona dayanır. Sorun çizelgenin varlığı değil, okurun onu **yirmi sekiz kez
taraması**dır.

---

## 3 · Önerilen mekanizma karışımı

### 3.1 · Tasarım kuralları — ölçümden türetildi

| # | Kural | Neyi kapatır |
|---|---|---|
| **K1** | **Anahtar aranmaz, VERİLİR.** Şifrenin anahtarı levhada basılıdır veya tek bir gözlemle bulunur. | 1.1 · tarama yorgunluğu |
| **K2** | **Her bulmaca kendi süre iddiasına sığar** (`qa_effort` ≤ 1,0×) | 1.2 · kavrayış/yürütme farkı |
| **K3** | **İspat sayar, okur gezmez.** Alan sözlüktür; mekanizma kabul yordamıdır. | 1.3 · alanın elle taranması |
| **K4** | **Her mekanizma, gerektirilmeden ÖNCE çözülmüş bir örnekle öğretilir** | 1.4 · mantık sıçraması |
| **K5** | **"Aha" işi, transkripsiyon işine baskın gelir** | ana şikâyet |

### 3.2 · Yeni karışım — 20 bulmaca

| Aile | Şimdi | **Öneri** | Değişiklik |
|---|---:|---:|---|
| `plate-observation` | 5 | **6** | ↑ en ucuz, en yüksek "aha" |
| `constraint-logic` | 5 | **4** | ↓ ve **basılı çizelge** üzerinde, 60 üyelik listede değil |
| `script-decoding` | 2 | **3** | ↑ kısa sözcük (4–5 glif), çizelge verili |
| `plate-embedded-cipher` | 2 | **3** | ↑ imza mekaniği; okuma **tek geçişte** sabit |
| `substitution-cipher` | 3 | **2** | ↓ ve ⭑ **ANAHTAR LEVHADA BASILI** ⭑ |
| `transposition-cipher` | 2 | **1** | ↓ tek genişlik basılı |
| `gate-synthesis` | 1 | **1** | değişmez — çalışıyor |
| **Toplam** | 20 | **20** | |

Çeşitlilik: en yüksek aile payı **%30** (tavan %35 ✓) · ayrı aile **7**
(taban 4 ✓) · en uzun ardışık aynı aile ≤2 ✓

### 3.3 · Öngörülen çaba

| | Şimdi | **Öneri** |
|---|---:|---:|
| Toplam elle işlem | **486 EU** | **~240 EU** |
| Çabanın ima ettiği süre | **162 dk** | **~80 dk** |
| Bütçesini aşan bulmaca | **6 / 20** | **0 / 20** |
| Oturum (+45 dk yük) | 207 dk | **~125 dk** |
| Öldürme kapısı tavanı | 240 dk | 240 dk |
| Pay | %14 | **%48** |

### 3.4 · Üç mekanizmanın somut dönüşümü

**① Kaydırma şifresi — anahtar levhada**
Şimdi: okur 28 kaydırmayı dener (84 EU).
Öneri: levhadaki halkanın **bir glifi işaretlidir**; o işaret kaydırma
miktarıdır. Okur işareti okur (1) ve altı harfi çevirir (6) → **7 EU**.
*"Aha"* işaretin ne olduğunu fark etmektir — tarama değil, **görme**.

⚠ Tekillik **korunur**: alan basılı sözlüktür (60), kabul yordamı
"bu sözcük, işaretli kaydırmayla bu dizeyi verir mi". Tam olarak biri
geçer. `qa_answerspace` bunu bugünkü koduyla ölçer (K3).

**② Yansıma — Kapı I'den ÇIKARILIR**
29 eksenin elle taranmasının ucuz bir hâli yok. Aile **Kapı IV**'e
(★★★, `layered-chain`/`polyalphabetic` komşuluğu) taşınır; orada okur
araçları öğrenmiştir ve iş beklemektedir.

**③ Anahtarlı alfabe — Kapı II'ye ertelenir**
29 harflik alfabeyi elden yeniden dizmek (29 EU) ★ için pahalıdır.
Mekanik **Kapı II**'de doğar; Kapı I yalnızca **basit yer değiştirme**
öğretir.

---

## 4 · Zorluk rampası — ikinci bırakma sebebinin cevabı

| Slot | Ne öğretilir | Araç |
|---|---|---|
| **1–4** | **Bakmak.** Saf levha gözlemi. | levha |
| **5** | ⭑ Alfabe, **çözülmüş bir örnekle** tanıtılır ⭑ | araçlar levhası |
| 6–8 | Kısa glif okuma (4–5 harf) | çizelge A |
| 9–12 | Basılı çizelge üzerinde eleme | çizelge |
| 13–16 | Levha içi şifre + **anahtarı basılı** yer değiştirme | levha + çizelge |
| 17–19 | Birleşim (iki adım) | tümü |
| **20** | Kapı bulmacası — **değişmez** | tümü |

### ⭑ Isınma bölümü YAZILIR ⭑

Sayfa modelinde Faz 1'den beri **3 sayfa** ayrılmış ve hiç yazılmamıştı.
İçeriği: her mekanizma için **tam çözülmüş** bir örnek — cevabıyla
birlikte. Okur alfabeyi ilk kez bir bulmacada değil, **bir örnekte** görür.

Bu, *"mantık sıçraması fazla dik"* şikâyetinin doğrudan karşılığıdır ve
sayfa bütçesi zaten buna hazırdır.

---

## 5 · Yeni kalite kapısı

**`04_BUILD/qa_effort.py`** — Faz 2 sonunda yazıldı ve **koşuyor**.

| Denetim | Kural |
|---|---|
| Bulmaca başına çaba | `EU ≤ expectedCompletionMinutes × 3` |
| Kapı toplamı | ima edilen süre ≤ bildirilen sürenin 1,5 katı |

⚠ **Sınır açıkça yazılıdır:** bu kapı *sıkıcılığı* ölçmez, **iş miktarını**
ölçer. İkisi aynı şey değildir — ama iş miktarı ölçülebilir ve sıkıcılık
ölçülemez. Yakın bir vekil, olmayan bir ölçümden iyidir.

### Önerilen ikinci kural: çaba modelinin kendisi kalibre edilmeli

Model şu an **bir** insan raporuna karşı doğrulandı (üç bulmaca, doğru
sıra). Bu iyi bir işaret, kanıt değil. İkinci tur harici testte gerçek
süreler ölçülür ve `EU_PER_MINUTE = 3` sabiti **ölçümle** güncellenir.

---

## 6 · Kurucudan istenen kararlar

| # | Karar | Öneri |
|---|---|---|
| **B1** | Yeni mekanizma karışımı (§ 3.2) onaylanıyor mu? | onay |
| **B2** | `reflection-map` Kapı I'den **çıkarılsın** mı? | evet → Kapı IV |
| **B3** | Anahtarlı alfabe **Kapı II'ye** ertelensin mi? | evet |
| **B4** | Isınma bölümü (3 sayfa) **yazılsın** mı? | evet |
| **B5** | `qa_effort` bütçesi ★ için `dakika × 3` doğru mu? | ikinci turda kalibre |
| **B6** | Yeniden test: **aynı beş çözücü mü, yeni beş kişi mi?** | ⚠ § 6.1 |

### 6.1 · ⚠ B6 önemsiz değil

Aynı beş çözücü Kapı I'i **bir kez gördü**. Yeniden test edildiklerinde
mekanizmaları biliyor olacaklar ve **daha hızlı** bitirecekler — ölçüm
iyimser çıkar ve öldürme kapısı yanlış yeşil yanar.

| Seçenek | Sonuç |
|---|---|
| **A** — beş YENİ çözücü | temiz ölçüm · maliyet: yeni kişi bulmak |
| **B** — aynı beş kişi | ⛔ **öğrenme etkisi** ölçümü bozar |
| **C** — karma (2 eski + 3 yeni) | eski/yeni farkı **ölçülebilir** hâle gelir |

**Öneri: C.** Eskilerin süresi ile yenilerinkinin farkı, öğrenme etkisinin
büyüklüğünü verir — ve bu, Kapı II–V testleri için kalıcı bir kalibrasyon
sabitidir.

---

## 7 · Sonraki adım

> ### YENİ BULMACA YAZILMADI VE YAZILMAYACAK.
>
> Talimat açıktır: *"Provide a proposal for the new Gate I mechanical mix
> **before** writing the new puzzles."*
>
> B1–B6 kapanınca yirmi bulmaca yeniden yazılır, `qa_effort` dâhil dokuz
> kapıdan geçirilir ve **ikinci bir harici tur** yapılır.

⚠ Ve bir şey daha: bu turun verisi **oturum düzeyindeydi**. İkinci turda
**bulmaca başına** kayıt alınırsa, hangi bulmacanın düştüğü tahmin değil
**ölçüm** olur. Devir paketi bu formu zaten taşıyor
([`EXTERNAL_SOLVER_PACKAGE.md § 5`](../00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md)).
