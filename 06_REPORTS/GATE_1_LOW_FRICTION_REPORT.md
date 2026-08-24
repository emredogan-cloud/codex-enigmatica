# KAPI I · DÜŞÜK SÜRTÜNME / YÜKSEK ÖDÜL

> **Codex Enigmatica** · 24 Ağustos 2026 · ikinci kurucu yönergesi
>
> ⚠ **BU BİR ÖLÇÜM RAPORUDUR, BİR GEÇİŞ BELGESİ DEĞİL.** Öldürme kapısı
> hâlâ `HARD-STOP`, `.gate` hâlâ `phase1` ve Faz 3 **başlatılamaz**.
> Tek bloklayıcı değişmedi: **A12b** — ikinci harici tur.

---

## 0 · Yönergenin sorusu

> *"Can I remove half the physical work while keeping the same amount of
> thinking?"*

Cevap ölçüldü. **Evet — ve ikinci kez.**

| | birinci tasarım | birinci yeniden tasarım | **bu tur** |
|---|---:|---:|---:|
| Elle işlem (EU) | 486 | 184 | **101** |
| En kötü hâl | — | 161 | **128** |
| Çabanın ima ettiği süre | 162 dk | 61 dk | **34 dk** |
| Bildirilen süre | 153 dk | 105 dk | **105 dk** |
| ⭑ Elle işin süredeki payı | %106 | %58 | **%32** |
| Bütçesini aşan bulmaca | 6 / 20 | 0 / 20 | **0 / 20** |
| En kötü oran | 4,7× | 1,0× (×3 bütçe) | **1,00× (×1,0 bütçe)** |

⭑ **Bildirilen süre YÜKSELTİLMEDİ.** Yönerge bunu adıyla yasakladı
(*"Do not simply increase the expected time."*) ve yirmi bulmacanın
hiçbirinin dakikası değişmedi. Düşen tek şey **iş**.

---

## 1 · Bütçe neden `×3`ten `×1,0`a indi

Eski bütçe `dakika × 3`tü ve üç bir **gevşeklik payı değil, birim
çevrimiydi** (dakikada üç elle işlem). Yani eski kural şunu söylüyordu:

> *Bildirilen sürenin **tamamı** mekanik yürütmeye gidebilir.*

Bir güvenlik tavanı olarak doğru; bir tasarım hedefi olarak anlamsız.
Yeni kuralın tek okunuşu var ve yönergenin § 2'si tam olarak bunu ister:

> ### Bildirilen sürenin en çok ÜÇTE BİRİ elle iştir.
> Kalan üçte iki **düşünmeye** aittir.

Ölçülen pay: **%32**. (K27)

---

## 2 · İki ayrı sebep, ayrı ayrı raporlanır

184 → 101 düşüşünün **tamamı yeniden tasarım değildir** ve bunu
gizlemek, ölçümü ölçüm olmaktan çıkarırdı:

| kaynak | katkı | ne oldu |
|---|---:|---|
| **Model düzeltmesi** | 184 → **130** | ölçüm yanlıştı, düzeltildi |
| **Yeniden tasarım** | 130 → **101** | iş gerçekten azaldı |

### 2.1 · Model düzeltmesi — sonuç için değil, tutarlılık için

`effort()` her mekanizma için *(beklenen, en kötü)* döndürür ve bütçe
**beklenen**i denetler. Arama tipi mekanizmalarda beklenen, en kötünün
yarısıdır. Dosya bunu ikisine uyguluyordu, ikisine uygulamıyordu:

| | |
|---|---|
| `cyclic-shift` · `reflection-map` | (en kötü/2, en kötü) ✅ |
| `plate-attribute` · `table-row` | (en kötü, en kötü) ⛔ |

Üçü de *"işe yarayanı bulana kadar bak"* yapısındadır. Bu bir politika
değil, Faz 2'nin son saatinde kalmış bir **gözden kaçmaydı** (K28).

Üç düzeltme:

1. **`plate-attribute` bir aramadır.** Metin okura *"altısından beşinde"*
   der; okur ayrık olanı bulunca **durur**. Beklenen `(n+1)/2`.
   ⚠ En kötü hâlâ `n`dir ve K4 tavanı (8) **en kötüye** uygulanır.
2. **`table-row` bir elemedir.** Maliyeti süzgeç sayısı değil, her
   aşamada kaç satırın **hayatta kaldığıdır**. Sözlük için zaten yapılan
   ardışık benzetim çizelgeye de uygulandı.
3. **Glif okuması tek yöndür.** Levha `▶` basar. **İspat** iki yönü de
   açar (ters okuyan okurun geçerli bir cevaba düşemediğini göstermek
   için); **okur** bir yön okur. Bu, sayı tablosu için zaten yazılmış
   olan K25 ayrımının aynısıdır.

### 2.2 · ⭑ Ve üç düzeltme de BOŞTA DURMUYOR ⭑

Bir ölçümü ucuzlatan varsayım, denetlenmiyorsa bir temennidir.
`qa_readerpack` üç yeni denetim aldı ve **ölçüm onlara dayanır**:

| § | denetim | düşerse |
|---|---|---|
| ⑨ | glif levhası okuma yönünü basıyor | maliyet **iki katı** |
| ⑩ | basılı daraltmanın sütunu gerçekten öbeklenmiş | süzgeç 1 değil **n** |
| ⑪ | sıra değiştirmenin boş ızgarası basılı | yazma+okuma **iki geçiş** |

Üçü de `05_TESTS/selftest.py`de kendi kusurlu fikstürüyle **ısırdığı
kanıtlanarak** duruyor.

---

## 3 · Yeniden tasarım — beş kural, yirmi bulmaca

| # | kural | ne yapıldı |
|---|---|---|
| **K1** | kör arama yok | anahtar levhada basılı · ızgara sayfada basılı · daraltma öbeklenmiş |
| **K2** | düşünce > yazım | elle işin payı %58 → **%32** |
| **K3** | her bulmacanın ödülü var | `ahaScore` ölçüldü, **basılı dayanak** şartıyla |
| **K4** | kısa yürütme | **en kötü hâlde bile ≤ 8 işlem** (kapı hariç) |
| **K5** | ev ödevi yok | altmış üyelik elle tarama **kaldırıldı** |

### 3.1 · Üç mekanizmanın somut dönüşümü

**① Altmış üyelik eleme → KESİŞİM.** Yönerge adıyla yasaklıyor:
*"Never require the player to manually scan a 60-item candidate list."*
Eski hâl 18 işlemdi (bütçe 7). Yeni hâlde okur ızgarayı **taramaz**, iki
**kenarını** okur: 4 satır etiketi + 2 sütun etiketi + kesişim = **7**.

⚠ Tekillik zayıflamadı, **güçlendi**: her hücre kendi satır ve sütun
etiketine karşı denetlenir (`grid_consistent`). Yazar *"üçüncü satır
III. gruptur"* deyip içine IV. gruptan bir sözcük koyarsa kabul yordamı
**hiçbir üyeyi kabul etmez** ve kapı kırmızı yanar. § 14'ün istediği tam
olarak budur: etiket bir **iddia** değil, ölçülebilir bir **nitelik**.

**② Dört kenar → ÜÇ kenar.** Çapa + dört kenar + tablo = 5,6 işlemdi ve
bütçe 5'ti. Kenar sayısını düşürmek okurun işini **gerçekten** azaltır
(4,6); bütçeyi yükseltmek yalnızca saati oynatırdı.
⭑ Ve başlangıç artık bir **köşe değil, bir kenardır**: köşe iki kenarın
ortak noktasıdır ve *"çapanın köşesinden başla"* okura **iki** kenar
gösterir. Üç levhanın üçü de **ayrı** kenardan başlar — hiçbiri
ötekinin ezberiyle çözülmez.

**③ Izgara okurdan alındı, sayfaya basıldı.** Okur harfleri kutulara
yazar ve satırı tek süpürüşte okur: 8 → **6** işlem. Ve kaybolacak bir
çizim yok.

### 3.2 · Altı levha bulmacası, altı AYRI gözlem

Yönerge § 6 levha gözlemini en güçlü aile ilan ediyor ve neyin
sömürüleceğini sayıyor. Eski altı bulmacanın altısı da *"ayrık niteliği
bul"*du. Yenileri:

| eksik olan | yönelim | uzamsal ilişki | eşlik eşitliği | öbekleme | bakışım |
|---|---|---|---|---|---|

Altısı **ayrı** şey fark ettirir ve üretim anında denetlenir
(`len(set(obs)) == 6`). Aynı iş, altı farklı düşünce.

---

## 4 · "Sıkıldım"ın ölçülmeyen yarısı

`qa_effort` işin **miktarını** ölçer ve iyi ölçer. Ama sıkıcılığın
yalnızca yarısıdır: aynı altı işlem, sonunda bir şey **keşfediliyorsa**
zevkli, keşfedilmiyorsa ev ödevidir.

**`04_BUILD/qa_experience.py`** (yeni · 14 denetim):

| ölçüt | hedef | ölçülen |
|---|---|---:|
| `ahaScore` ortancası | ≥ 4 | **4,0** |
| ödülsüz bulmaca (≤2) | ≤ 2 | **0** |
| `repetitionBurden` ortancası | ≤ 2 | **2,0** |
| ısınma · öğretilen aile | 7 / 7 | **7 / 7** |
| en uzun ardışık ağır dizi | < 4 | **1** |
| küçük zafer payı | ≥ %40 | **%80** |

### ⚠ Ve burada dürüst olmak zorundayım

`ahaScore` **yazarın kendi puanıdır.** Yönergenin kendi sözü:

> *"Do NOT use ahaScore as a substitute for real testing.
> It is a design heuristic."*

Bir yazarın kendi bulmacasına *"bu zekice"* demesi bir ölçüm değildir ve
bu kapı onu **doğrulayamaz**. Yaptığı şey, şişirilmesini **zorlaştırmak**:

* **4 ve üstü** veren her bulmaca ödülün **basılı yerini** göstermek
  zorundadır (`revelation.evidence`) ve gösterdiği şey okur paketinde
  bulunmalıdır. *"Zekice"* deyip yerini gösterememek geçmez.
* **Aynı mekanizma ikinci kez 4+ alamaz.** Sürpriz bir kez olur; ikincisi
  yordamdır. Bu kural, üç glif bulmacasının ikisini ve üç sayı levhasının
  ikisini 3'e **indirmeye zorladı** — puanları yazarken değil, kapı
  koşarken.
* `repetitionBurden` yazardan gelmez; çaba modelinden **ölçülür**.

Gerçek ölçüm A12b'nin kayıt formundadır: her bulmacanın altında
**"sıkıcı mıydı 1–5"** satırı basılıdır.

---

## 5 · Isınma bölümü üçten YEDİYE çıktı

B4'te yazılan üç örnek üç aileyi öğretiyordu. Geri kalan **dördü** —
kısıt mantığı, levha içi şifre, sıra değiştirme ve kapı bulmacası —
okurun karşısına **çözülmüş bir örnek görmeden** çıkıyordu. Yönerge § 7
bunu kapatıyor:

> *"Create a short solved example for every new mechanism family
> BEFORE that mechanism becomes necessary."*

Artık **yedi aile, yedi örnek** ve `qa_experience` kapsamı denetliyor.

⭑ Ve örneklerin sayıları **uydurma değildir**: satır numaraları Çizelge
B'den, tablo göndermesi Çizelge D'den **hesaplanır**. Okur örneği okurken
çizelgeye bakarsa sayı **tutar**. Uydurma bir satır numarası, kitabın
dördüncü sözünü ilk sayfada kırardı.

⚠ Ve hiçbir ısınma cevabı gerçek bir bulmacanın cevabı **değildir** —
`qa_experience` bunu ayrıca denetler.

---

## 6 · Üretimde kapıların yakaladığı dört kusur

Hiçbiri okuyarak bulunmadı. Dördü de **makine** buldu.

| # | kusur | kapı |
|---|---|---|
| 1 | Yayılma yarıçapı 2: zincirler **birbirine eklenmişti** (A→B→C); birinci bulmacadaki tek hata İKİ bulmacayı düşürüyordu | `qa_handoff` |
| 2 | Kitabın **kendi adı** bir cevap olmuştu ve her sayfanın kısıt cümlesinde geçiyordu — cevap kendi sayfasında bedava duruyordu | `qa_readerpack § ⑥` |
| 3 | *"Üç **basamaklı** okuma"* — ve `BASAMAK` bir Çizelge D üyesiydi. Türkçede **basamak** hem merdiven basamağı hem sayı hanesidir | `qa_answerspace § ⑦` |
| 4 | ⭑ Sekiz üye **cevap olamazdı**: projenin kendi söz dağarcığıdır ve biri **commit mesajlarında** geçiyordu — geri alınamaz | `qa_solution_leak` |

### 6.1 · ⭑ Ve bir kusuru HİÇBİR kapı görmüyordu ⭑

Zincirli bir bulmaca, kaynağının cevabını tüketicinin sayfasına **basmak
zorundadır**. Ama o sütun kaynağın aday kümesiyle **tek bir üyede**
kesişirse, okur kaynağı hiç çözmeden cevabını **iki sayfaya bakarak**
okur.

İki bulmacada gerçekten vardı ve `§ ⑥` göremiyordu — çünkü ⑥ **tek
sayfaya** bakar ve iki sayfa ayrı ayrı temizdi.

> **Sızıntı sayfada değildi; sayfaların ARASINDAYDI.** (K31)

Yeni denetim `qa_readerpack § ⑫` kesişimi ölçer ve en az **iki** ortak
aday ister.

---

## 6.2 · ⚑ Sayfa modeli 230 → 232 (kurucu bilgisi)

Isınma bölümü üç sayfaya yazılmıştı ve **yedi örnek üç sayfaya sığmıyor**:
ölçüldü, 155 satır — sayfa başına 42 satırla **~3,7 sayfa**. Model
dürüstçe **beş sayfaya** çıkarıldı ve toplam **230 → 232** oldu.

⚠ Sayfa hedefi **A8'de kurucu onayı bekliyor** (K17). İki sayfalık artış
sessizce yutulmadı; burada duruyor. Alternatif — ısınmayı kısaltmak —
yönergenin § 7'siyle çelişirdi: *"a short solved example for every new
mechanism family"*.

---

## 7 · Kapı durumu

| kapı | sonuç |
|---|---|
| `qa_effort` (×1,0 · K4) | ✅ 4 · **101 EU** · 0/20 aşım |
| `qa_experience` (yeni) | ✅ 14 · aha 4,0 · tekrar 2,0 |
| `qa_answerspace` | ✅ 10 · 1.152 aday · **20/20 tam olarak bir** |
| `qa_readerpack` (⑨⑩⑪⑫ yeni) | ✅ 14 |
| `qa_handoff` | ✅ 13 · yayılma yarıçapı ≤1 |
| `qa_solvability` · `qa_uniqueness` · `qa_hints` | ✅ 11 · 9 · 9 |
| `qa_solution_leak` (kanarya) | ✅ kip A · 88 dosya |
| `selftest` | ✅ **179** denetim — bütün kapılar ısırıyor |

---

## 8 · Ne YAPILMADI

* ⛔ **Faz 3 başlatılmadı.** `.gate` hâlâ `phase1`.
* ⛔ **Öldürme kapısı elle oynatılmadı.** Hâlâ `HARD-STOP`; kararı
  değiştirecek olan tek şey **gerçek oturum kayıtlarıdır**.
* ⛔ **Hiçbir çözücü oturumu uydurulmadı.** A12b henüz **yapılmadı**.
* ⛔ **`EU_PER_MINUTE = 3` hâlâ kalibre edilmemiştir** (B5 ertelendi;
  config'de `calibrated: false`). İkinci turun gerçek süreleri onu
  düzeltecek — ve %32 payı da onunla birlikte yeniden hesaplanacak.
* ⛔ **Fiziksel prova alınmadı** (A9 · kurucu eylemi).

---

## 9 · Sonraki adım — A12b

Paket hazır: `02_MANUSCRIPT/PILOT_TR/PILOT_TR.md` (bulmacalar + ısınma +
kayıt formları) ve `PILOT_TR_IPUCLARI.md` (**ayrı zarf**).

⚠ Aynı dizindeki `*(1).html` dosyaları **ESKİ tasarımdandır** ve
çözücülere verilmemelidir.

Kohort B6'da kilitlendi: **2 dönen + 3 yeni**. Eşik **yeni** çözücülere
karşı okunur — dönen bir çözücünün bitirmesi, kitabın çalıştığını değil,
onun öğrendiğini kanıtlar.

En önemli nitel soru değişmedi:

> *"At what point, if any, did this start feeling like work instead of
> a puzzle?"*
