# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript ve **çözüm katmanı** politikası | **YÜKSEK** | **Faz 1 başlamadan** | AÇIK (varsayım: § K10) |
| **A2** | 5 kapı teması onayı | YÜKSEK | Faz 1 sonu | AÇIK |
| **A3** | **5 harici çözücü kim** | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK |
| **A4** | Doğrulama sayfası barındırma | ORTA | Faz 5 | AÇIK |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | Faz 2 | AÇIK |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |

---

### A3 · Beş harici çözücü — öldürme kapısının tabanı

**Bu, Faz 2'nin sert bloklayıcısıdır ve bütün projenin kaderi ona bağlıdır.**

Ajan bulmaca çözemez — çözümü zaten bilir; "çözülebilir" yargısı kanıt
değildir. Test **harici** insanlarladır ve çözücüler **bağımsız** çalışır.

Çözücü bulunamazsa **Faz 2 bloklanır**. Kabul edilen bir bloktur:
**sahte test kaydı üretilmez.**

Kimlikler anonimdir (`solver-01`) ve şema bu biçimi zorunlu kılar.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole
**12 Ağustos 2026 · bootstrap.** Talimat § 31 bir ajanın tek klasörle
çalışabilmesini şart koşuyor. **Kopyalanan kod biraz fazlalıktır;
bağımlılık bir kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur
`--fix` kapıya dokunmaz (Bestiarium dersi).

### K3 · Codex adı taşınır, tür taşınmaz
Bu cilt *Codex* hattının adını taşır ama **referans değil oyundur**.
Bilinçli bir marka genişlemesi: Vâliçe Press'i "referans yayıncısı"ndan
**"deneyim tasarlayan yayıncı"**ya taşır.

Ad ortaklığı **dosya ortaklığı değildir**: Bestiarium'dan motif *fikri*
alınır, **dosya alınmaz**.

### K4 · ⭑ Bir bulmaca "zekice göründüğü" için kabul edilemez ⭑
**Bu projenin birinci kuralı.** Deterministik olarak çözülemeyen bir
bulmaca bir **üretim hatasıdır**. Beş şart
[`00_CONTEXT/SOLVABILITY_STANDARD.md`](00_CONTEXT/SOLVABILITY_STANDARD.md)'de
tanımlıdır ve üç kapı tarafından denetlenir.

### K5 · ⛔ Faz 2 bir ÖLDÜRME KAPISIDIR
20 bulmaca 5 harici çözücüyle test edilir. **≤2 çözücü Kapı I'i bitirirse
proje DURUR veya YENİDEN TASARLANIR.**

Gerekçe: bozuk bir bulmaca sistemi üzerine 200 sayfa yazmak, bu portföyün
yapabileceği **en pahalı hatadır**.

Eşikler `project_config.json § killGate` içinde **sayısaldır**;
`validate_spec.py` düşürülmelerini yakalar. **Yoruma yer yoktur.**

### K6 · Üç kademeli ipucu zorunludur
Cain's Jawbone'u üç kişi çözdü — bu ticari olarak bir **terk oranıdır**.
Bu kitabın konumu tersidir: *amaç okuru yenmek değil, içeride tutmaktır.*
`qa_hints` üç kademenin varlığını ve hiçbirinin cevabı içermediğini
denetler.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz
`validate.yml` saniyeler içinde biter.

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR
`scope.locked: false`.

### K9 · Kindle üretilmez
Görsel şifreler e-okuyucuda bozulur; iade ve kötü yorum üretir.
Bir gelir kaybı değil, **itibar korumasıdır**. `validate_spec` Kindle'ın
açılmasını yakalar.

### K10 · ⭑ İKİ KATMANLI İÇERİK — dört hatlı çözüm koruması ⭑
**Bu projenin ikinci varoluşsal kuralı.**

Çözümler, çözüm yolları ve ipuçları **PROTECTED** katmandadır ve public
depoya giremez. Ama **kod sır değildir**: `04_BUILD/` ve `05_TESTS/`
public kalır.

Dört hat: `.gitignore` (yol) · `PROTECTED_DIRS` (varlık) ·
`check_solution_leak()` (içerik) · `validate_spec` (şema).

Gerekçe: sızıntı **geri alınamaz**. Git geçmişine giren bir çözümü silmek
geçmişi yeniden yazmak demektir — ve o ana kadar klonlamış herkeste kalır.

→ [`00_CONTEXT/CONTENT_PROTECTION.md`](00_CONTEXT/CONTENT_PROTECTION.md)

### K11 · 6×9 normal trim
6,0 ≤ 6,12 ve 9,0 ≤ 9,0 olduğu için **normal trimdir** ve sayfa başına
0,012 $ öder — büyük trimin 0,017 $'ının altında. Codex serisiyle raf
uyumu ve düşük baskı maliyeti aynı anda.

### K12 · Kapı V dizgiye bağlıdır ve en son kilitlenir
Kapı V öz-göndergeseldir: kitabın **fiziksel yapısını** kullanır
(sayfa numaraları, dizin, kolofon). Dizgi değişirse **kırılır**.

Bu yüzden dizgi Faz 5'te **dondurulur** ve Kapı V ondan **sonra**
kilitlenir. Faz 6 sayfa sayısını yalnızca **doğrular**.
