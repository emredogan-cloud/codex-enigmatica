# LEVHA PROVA KONTROL LİSTESİ — Kapı I pilotu

> ⚠ **BU BELGE BİR PROVA SONUCU DEĞİLDİR.** Bir provanın nasıl
> okunacağını söyler. Ölçüm kurucu tarafından yapılır (A9).
>
> Üretildi: `04_BUILD/plate_proof.py` · Faz 2

---

## 0 · Durum — üçü asla birleştirilmez

| Durum | Anlamı | Pilot |
|---|---|---|
| `SCREEN-TESTED` | Ekranda çözüldü — **ön eleme** | ✔ 20/20 |
| `PAPER-TESTED` | Lazer baskıda çözüldü — pilot için yeterli | ⚑ **kurucu** |
| `PHYSICAL-PROOF-VALIDATED` | POD prova kopyada ölçüldü — **kanıt** | ⛔ **YAPILMADI** |

⚠ Ve pilot levhaları **gravür değil, tipografik şekildir**. Bu paket
bulmacaların **mantığını** kâğıtta test eder; gravürün baskı davranışını
**etmez**. O ölçüm Faz 5'e aittir.

---

## 1 · Kurucunun yapacağı

1. `02_MANUSCRIPT/PROOF/pilot-plates-proof.pdf` dosyasını **%100
   ölçekte**, küçültmeden bastırın. Kâğıt: mümkünse krem, 80–90 g.
2. Aşağıdaki her satırı **basılı sayfada** işaretleyin.
3. Bir satır düşerse ilgili bulmaca **çözülemez** demektir; onu rapora
   yazın ve bulmacayı yeniden tasarlanacaklar listesine koyun.
4. Sonucu `06_REPORTS/tracked/plate-print-test.json` olarak kaydedin.

---

## 2 · Levha başına ölçüt

| Levha | Bulmaca | Ayırt edilmesi gereken en küçük şey | ✓ |
|---|---|---|---|
| pl-g1-01 | g1-001 | Kemer tepesindeki **bir** ile **iki** elmas arasındaki fark | ☐ |
| pl-g1-02 | g1-002 | Gaga yönü: sola bakan ile sağa bakan kuş | ☐ |
| pl-g1-03 | g1-003 | **Aralıklı işaret sayımı**: dört işaret ile beş işaret | ☐ |
| pl-g1-04 | g1-004 | Halka konturundaki **ince kesik** | ☐ |
| pl-g1-05 | g1-007 | Sütun çentiklerinin sayısı ve sütun numarası | ☐ |
| pl-g1-06 | g1-008 | Kenar oyuk kümeleri ve **çapa işaretinin köşesi** | ☐ |
| pl-g1-07 | g1-012 | Dikey söve işaretleri ve **alttaki ok yönü** | ☐ |
| pl-g1-08 | g1-014 | Basamak ön kenarındaki bir/iki oyuk | ☐ |
| pl-g1-09 | g1-016 | Koyu karo sayısı ve **çatlak karo** | ☐ |
| pl-g1-10 | g1-020 | On dokuz satırlık konum/grup çizelgesi | ☐ |

---

## 3 · ⭑ En yüksek riskli üç ölçüt ⭑

Bunlar düşerse bulmaca çözülemez ve **öldürme kapısı yanlış ölçer**.

| # | Risk | Neden |
|---|---|---|
| **1** | **Dört işaret ile beş işaretin ayırt edilmesi** | Ç/D ve T/U yalnızca sayımla ayrılır. İç çözücü bunu bir **sayma yorgunluğu riski** olarak bildirdi; işaretler bu yüzden **aralıklı** basılır. Kâğıtta aralık kapanıyorsa mekanik kırılır. |
| **2** | **Halka konturundaki kesik** | Kesik, nokta yayılmasının kapatabileceği en küçük detaydır. Kapanırsa yedi halkanın yedisi de "kapalı" görünür ve bulmacanın tek ayırıcı yüklemi yok olur. |
| **3** | **Çatlak karo ile koyu karo** | İkisi de koyu sayılır (metin bunu söyler) ama çatlak **görülebilmelidir**: okumanın başlangıç noktasını o belirler. |

---

## 4 · Kayıt biçimi

```json
{
  "date": "YYYY-AA-GG",
  "medium": "laser | POD-proof",
  "paper": "krem 90g",
  "plates": [{"plateId": "pl-g1-01", "legible": true, "note": ""}],
  "failures": [],
  "verdict": "PAPER-TESTED | PHYSICAL-PROOF-VALIDATED | FAILED"
}
```

⚠ `verdict` alanına `PHYSICAL-PROOF-VALIDATED` **yalnızca gerçek bir POD
prova kopyası** ölçüldüyse yazılır. Lazer baskı `PAPER-TESTED`tir.
