# Codex Enigmatica

**One Hundred Engraved Enigmas and a Single Unbroken Mystery —
A Puzzle Book Bound as a Grimoire**

---

## Bu depo nedir

Bu depo bir **kitap üretim sistemidir**, kitabın kendisi değil.

Beş kapı. Her kapıda yirmi bulmaca. Ve yüz bulmacanın çıktısını tek bir
son soruya bağlayan bir meta-mister.

Bu rafta talep kanıtlanmış — Journal 29, Cain's Jawbone — ama arz
**onlarca başlıktan ibaret**. Ve neredeyse hepsi modern/soyut estetikte:
**folklor-gravür dünyasında kurulmuş bir tanesi yok.**

Bu kitap oraya girer, ve bir şey daha yapar: **pes etmenize izin verir.**
Cain's Jawbone'u üç kişi çözdü — bu bir efsane olarak anlatılır ama
ticari olarak bir **terk oranıdır**. Burada her bulmacanın üç kademeli
ipucu vardır. *Amaç okuru yenmek değil, içeride tutmaktır.*

Depoda duran şey: **bulmaca metadatası, iki katmanlı şema, doğrulama
kapıları, CI/CD, dizgi ve KDP üretim hattı, ölçüm raporları ve belgeler.**

Depoda **durmayan** şey: **çözümler.**

---

## Durum

| | |
|---|---|
| Faz | **0 · Bootstrap** |
| Kapı (`.gate`) | `phase0` |
| Aday bulmaca | 0 / ≥130 |
| Doğrulanmış bulmaca | 0 / 100 |
| Yazılmış bulmaca | 0 / 100 |
| Levha | 0 / ~110 |
| **Sonraki adım** | **Faz 1 — kurucu onayı bekliyor** |

Ölçülmüş güncel durum: [`BOOK_STATS.md`](BOOK_STATS.md) ·
[`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md)

---

## İki varoluşsal kural

### ① Çözülebilirlik
> **Bir bulmaca "zekice göründüğü" için kabul EDİLEMEZ.
> Deterministik olarak çözülemeyen bir bulmaca bir ÜRETİM HATASIDIR.**

Kusurun bedeli asimetriktir: başka bir kitapta %90 kalite satılabilir bir
üründür; burada **%98 kalite bile 1 yıldızlarla cezalandırılır**. Çözemeyen
okur aptal hissetmez — **aldatılmış** hisseder.

→ [`00_CONTEXT/SOLVABILITY_STANDARD.md`](00_CONTEXT/SOLVABILITY_STANDARD.md)

### ② Çözüm koruması
> **Bir bulmaca kitabının çözümleri ürünün kendisidir.**

Public depoda duran bir çözüm kitabı **yayımlanmadan** değersizleştirir —
ve hata **geri alınamaz**. Bu yüzden burada **dört hatlı** koruma vardır:
`.gitignore` (yol) · korumalı dizin denetimi (varlık) · içerik taraması
(alan adı) · şema denetimi (public indeks).

**Ama kod sır değildir.** `04_BUILD/` ve `05_TESTS/` public kalır: bir
doğrulayıcının nasıl çalıştığını herkes görebilir, **neyi doğruladığını**
göremez.

→ [`00_CONTEXT/CONTENT_PROTECTION.md`](00_CONTEXT/CONTENT_PROTECTION.md)

---

## ⛔ Faz 2 bir öldürme kapısıdır

20 bulmaca yazılır ve **5 harici çözücüyle** test edilir.

| Sonuç | Karar |
|---|---|
| 4–5 çözücü Kapı I'i bitirdi, 0 alternatif çözüm | ✅ **DEVAM** |
| Tam 3 bitirdi | ⚠ Kapı I yeniden tasarlanır |
| **≤2 bitirdi** | ⛔ **PROJE DURUR veya YENİDEN TASARLANIR** |

Bozuk bir bulmaca sistemi üzerine 200 sayfa yazmak, bu portföyün
yapabileceği **en pahalı hatadır**.

---

## Hızlı başlangıç

```bash
git clone https://github.com/emredogan-cloud/codex-enigmatica.git
cd codex-enigmatica

# Bütün kalite kapıları — CI'ın koştuğu komutun birebir aynısı.
# Hiçbiri venv gerektirmez; hepsi Python standart kütüphanesiyle koşar.
./04_BUILD/qa_all.sh

# Ağır işler (görsel ölçümü, dizgi) için:
python3 -m venv 04_BUILD/.venv
04_BUILD/.venv/bin/pip install -r 04_BUILD/requirements.txt
```

Yeşilse CI de yeşil olur. Kırmızıysa ilerleme yoktur.

---

## Dizin yapısı

```
00_CONTEXT/     proje bağlamı, üslup, ÇÖZÜLEBİLİRLİK ve İÇERİK KORUMA standardı
01_SOURCE/       bulmaca metadatası (public), kapı indeksi, iki katmanlı şema
  └ solutions/   ⛔ KORUMALI — takip edilen dosya bulunması İHLALDİR
02_MANUSCRIPT/  bulmaca prozası — DEPO DIŞINDA
03_COVER/       kapak çalışması
03_APLUS/       A+ içerik modülleri
04_BUILD/       doğrulayıcılar, kalite kapıları, üretim hattı  ← PUBLIC
05_TESTS/       kapıların kendi testi ve kurgu üreteci          ← PUBLIC
06_REPORTS/     ölçüm raporları (çözüm içermeyen)
  └ solver/      ⛔ KORUMALI — çözücü ham kayıtları
07_ASSETS/      levhalar: raw (salt okunur) → processed → print
08_OUTPUT/      üretilmiş yayın dosyaları — depoda durmaz
09_ARCHIVE/     düşen bulmacalar
  └ solutions/   ⛔ KORUMALI
```

---

## Altı faz

| Faz | Ad | Kapı |
|---|---|---|
| 1 | Bulmaca mimarisi, çözülebilirlik, gizlilik katmanı | `phase1` |
| 2 | ⛔ **ÖLDÜRME KAPISI** — 20 bulmaca + 5 çözücü | `phase2` |
| 3 | Kapı II · The Menagerie | `phase3` |
| 4 | Kapı III–V + meta-mister | `phase4` |
| 5 | Yakınsama + levha üretimi + doğrulama sayfası | `phase5` |
| 6 | Nihai üretim + KDP paketi | `release` |

Tam yol haritası:
[`CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md`](CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md)

---

## İzolasyon

Bu proje bütün diğer projelerden **tamamen ayrıdır**.
*Codex Mythologica* ve *Codex Bestiarium* ile **ad ortaklığı vardır,
dosya ortaklığı yoktur**.
Ortak dosya, ortak build, ortak `.gate` yoktur. Bu depo tek başına
klonlanabilir, test edilebilir ve üretilebilir.

Taşınan disiplin ve gerekçeleri:
[`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## Lisans ve künye

Yayıncı: **Vâliçe Press** · Belgeler Türkçe, kitap İngilizcedir.
