# STYLE — Codex Enigmatica

> Sürüm **1.0 · bootstrap**. Faz 2'de ölçümle kalibre edilir ve v2.0 olur.

---

## 1 · İki kayıt, bir kural

| Kayıt | Nerede | Ses |
|---|---|---|
| **Anlatı** | çerçeve anlatı · kapı açılışları · kolofon | kuru, kesin, hafif tekinsiz — bir kütüphanecinin sesi |
| **Talimat** | bulmaca metni · sözleşme sayfası · araçlar levhası | **kristal netlikte** |

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

| Ölçüt | Hedef | Kapı |
|---|---|---|
| Bulmaca metni | 90–220 kelime | `qa_length` |
| **Talimat cümlesi azami** | **20 kelime** | `qa_solvability` |
| Anlatı cümle ortalaması | 13–20 kelime | `qa_drift` |
| Kapı açılışı | ~500 kelime | `qa_length` |
| İpucu (kademe başına) | ≤40 kelime | `qa_hints` |

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

## 6 · Belirsizlik: anlatıda serbest, talimatta YASAK

Çerçeve anlatı çok anlamlı olabilir — hatta olmalıdır; tekinsizlik oradan
gelir.

Ama **bulmaca metni** tek anlamlıdır. İkisi arasındaki sınır
`qa_solvability`'nin belirsizlik puanıyla korunur.

> Anlatının tekinsizliği okuru içeri çeker.
> Talimatın belirsizliği okuru kaybeder.
