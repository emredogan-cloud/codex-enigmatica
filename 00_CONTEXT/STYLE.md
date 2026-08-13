# STYLE — Codex Enigmatica

> Sürüm **2.0 · Faz 2'de ÖLÇÜMLE kalibre edildi** (13 Ağustos 2026).
>
> v1.0'ın bantları yazılmış tek bir bulmaca yokken konulmuş **hipotezlerdi**.
> Aşağıdaki sayılar artık yirmi gerçek bulmacadan **ölçülmüştür** — ve biri
> hipotezi doğrulamadı (§ 4.1).

---

## 0 · ⭑ FAZ 2 BULGUSU: EKSİK OLAN KAYIT ⭑

Kurucu pilot metinleri için şunu bildirdi: *"mekanik olarak kusursuz ama
anlatısal olarak ölü — bir matematik sınavı gibi okunuyor, bir grimoire
gibi değil."*

Teşhis **üslup değil, mimariydi.** § 1 iki kayıt tanımlar. Pilotun yirmi
bulmacasının yirmisi de **yalnızca talimat kaydında** yazılmıştı. Anlatı
kaydı hiç yoktu.

> Sınav gibi okunmasının sebebi talimatların kötü olması değil,
> **anlatının eksik olmasıydı.**

Ve bu ayrım düzeltmenin biçimini belirledi: talimatı **süslemedik** —
o, çözülebilirliği bozardı. Eksik kaydı **ekledik**.

| Ne yapıldı | Ne YAPILMADI |
|---|---|
| Her bulmacaya bir **anlatı satırı** eklendi | Talimat süslenmedi |
| Talimat sınav registerinden **arşivci** registerine taşındı | Talimat uzatılmadı |
| İpuçları **kümülatif tekrardan** kurtarıldı | Merdiven yapısı değiştirilmedi |
| Ölçüm bantları gerçek metne vuruldu | Bant ölçüme uydurulmadı (§ 4.1) |

**Kanıt:** geçişten sonra `qa_solvability`, `qa_hints` ve `qa_uniqueness`
yeniden koştu ve **üçü de yeşil** kaldı. Belirsizlik puanı, cevap uzayı
ve merdiven kapsamı **değişmedi**. Üslup mekanikten ayrı tutulabilir —
bu, onun kanıtıdır.

⚠ Ve geçiş sırasında kapı **bir kez ısırdı**: bir fısıltı, son çözüm
adımıyla iki içerik kelimesi paylaşıyordu ve `qa_hints § ⑦` onu *cevap
anahtarı* olarak kırmızı yaktı. Bir üslup değişikliği mekaniği **sessizce
bozabilir**; yakalayan şey disiplin değil, kapıydı.

---

## 1 · İki kayıt, bir kural

| Kayıt | Nerede | Ses |
|---|---|---|
| **Anlatı** | çerçeve anlatı · kapı açılışları · **bulmaca başına anlatı satırı** · kolofon | kuru, kesin, hafif tekinsiz — bir kütüphanecinin sesi |
| **Talimat** | bulmaca hedefi · okur eylemi · maddeler · sözleşme sayfası · araçlar levhası | **kristal netlikte** |

⚠ **Anlatı satırı Faz 2'de eklendi** ve mekanik içerik **taşımaz**: bir
sayı, bir yön, bir konum veya bir çizelge adı geçemez. Taşısaydı, bir
üslup geçişi bir bulmacayı bozabilirdi.

⚠ Ve **üretilen levha künyeleri** anlatı kaydına GİRMEZ. Onlar levha
şekliyle **aynı kaynaktan** üretilir ve harfi harfine korunur: mekanik
yetke onlardadır.

> **Anlatı süslü olabilir; TALİMAT ASLA.**
> Belirsiz bir talimat, belirsiz bir bulmacadır — ve belirsizlik bu
> kitapta üslup meselesi değil, **çözülebilirlik meselesidir**.

---

## 2 · Anlatı sesi

Bir kütüphanecinin sesi; bir sunucunun değil. Okura seslenmez, ona
**bir şey uzatır**.

| ✅ | ❌ |
|---|---|
| *Enigma VII. The plate conceals what the margin repeats.* | *Are you ready for the next challenge?* |
| *What you seek was set down before the ink dried.* | *Can you solve this tricky puzzle?* |
| *Turn to the leaf that carries no number.* | *Let's dive into the mystery!* |

---

## 3 · Sabit kalıplar

```
Enigma [ROMAN]:        → bulmaca başlığı
What you seek …        → hedef cümlesi
The plate conceals …   → levha içi şifre işareti
Turn to the leaf …     → çapraz referans
```

Bu kalıplar **değişmez** ve `qa_voice` tutarlılıklarını denetler.
Sabit kalıp, okurun kitabı **öğrenmesini** sağlar — ve bir bulmaca
kitabında bu, çözülebilirliğin parçasıdır.

---

## 4 · Ölçülen bantlar

| Ölçüt | v1.0 hipotezi | **Kapı I'de ÖLÇÜLEN** | Kapı |
|---|---|---|---|
| Bulmaca metni (anlatı dâhil) | 90–220 kelime | **41–83 · medyan 51** ⚠ | `qa_length` |
| Anlatı satırı (bulmaca başına) | — *(yoktu)* | **7–20 · medyan 13** | — |
| **Talimat cümlesi azami** | **20 kelime** | **4–10 · medyan 7** ✅ | `qa_solvability` |
| İpucu (kademe başına) | ≤40 kelime | **9–25 · medyan 13** ✅ | `qa_hints` |
| Kapı açılışı | ~500 kelime | *henüz yazılmadı* | `qa_length` |

### 4.1 · ⚠ Ölçüm hipotezi DOĞRULAMADI — ve bant değiştirilmedi

Bulmaca metni **90–220 kelime** hedefinin çok altında çıktı: medyan **51**.

Bu bant, tek bir bulmaca yazılmadan önce ve **kitabın tamamı için**
konulmuştu. Kapı I zorluk ★'dır — dört dakikalık bir bulmacanın iki yüz
kelimelik girişi, atmosfer değil **sürtünmedir**.

> ⚠ **Bant yine de DÜŞÜRÜLMEDİ.** Bir hedefi ölçüme uydurmak, ölçmenin
> tersidir. Doğru hamle bandı **zorluğa göre ayırmaktır** ve bunun için
> Kapı II (★★) ile Kapı IV (★★★) ölçümü gerekir.

| Zorluk | Durum |
|---|---|
| ★ · Kapı I | **51 medyan · ÖLÇÜLDÜ** |
| ★★ · Kapı II–III | hipotez — **Faz 3'te ölçülecek** |
| ★★★ · Kapı IV–V | hipotez — **Faz 4'te ölçülecek** |

Karar Faz 3'e ertelendi: üç bant birden ölçülmeden tek bir sayı yazmak,
aynı hatayı ikinci kez yapmaktır.

---

## 5 · Yasak kalıplar

- "sadece … değil, aynı zamanda" / "not only … but also"
- *"Are you ready?"* · *"Can you solve it?"* — okura meydan okuyan ikinci
  şahıs soruları. Bu kitap meydan okumaz, **kapıyı açık bırakır**
- "dive into" · "unlock the secrets"
- Ünlem işareti — **anlatıda hiç**, talimatta hiç
- Bir kelimenin iki anlama geldiği her yapı — bu bir **çözülebilirlik
  ihlalidir**, üslup tercihi değil

---

## 5b · ⭑ İpucu merdiveni: kümülatif tekrar bir kusurdur ⭑

Pilotun ilk hâlinde üç kademe çözüm adımlarını **kümülatif** olarak
yeniden yazıyordu: ikinci kademe birinciyi, üçüncü ikisini birden.
Kurucunun *"robotik tekrar"* dediği şey buydu.

> Aynı cümleyi üç kez okumak bir merdiven değil, bir **form**dur.

| Kademe | Ne getirir | Nasıl bağlanır |
|---|---|---|
| **1 · yönlendirme** | adım 1 | bulmacanın nesnesine bağlı bir **giriş** |
| **2 · yöntem** | adım 2 | okurun nerede kaldığını söyleyen bir **köprü** |
| **3 · neredeyse-cevap** | adım 3 | iki adımı özetleyen köprü + bir **kapanış** |

Ve her bulmaca **kendi** dört parçasını taşır: yirmi bulmaca × üç kademe,
altmış ipucunun altmışı da aynı üç kalıptan çıkmaz.

⚠ Kapsam kuralı **değişmedi**: kademe *n* çözüm yolunun ilk *n* adımına
dokunur ve **3. kademe son adımı asla vermez**. `qa_hints` bunu ölçer;
üslup onu gevşetemez.

---

## 6 · Belirsizlik: anlatıda serbest, talimatta YASAK

Çerçeve anlatı çok anlamlı olabilir — hatta olmalıdır; tekinsizlik oradan
gelir.

Ama **bulmaca metni** tek anlamlıdır. İkisi arasındaki sınır
`qa_solvability`'nin belirsizlik puanıyla korunur.

> Anlatının tekinsizliği okuru içeri çeker.
> Talimatın belirsizliği okuru kaybeder.
