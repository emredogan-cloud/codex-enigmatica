# CHANGELOG — Codex Enigmatica

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.0.1] — 2026-08-12 · Bootstrap

Proje altyapısı kuruldu. **Hiçbir kitap içeriği üretilmedi.**

### Eklendi

- **Dizin mimarisi** — 26 dizin, `00_CONTEXT` … `09_ARCHIVE` şemasına uygun,
  bu projeye özgü eklerle: `01_SOURCE/puzzles`, **`01_SOURCE/solutions`**
  (korumalı), `05_TESTS/puzzle`, **`09_ARCHIVE/solutions`** (korumalı),
  `07_ASSETS/plates`
- **`project_config.json`** — makine okunur tek doğruluk kaynağı. Pazar
  raporunun sayıları `scope.locked: false` ile **hipotez** olarak işaretlendi
- **`CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md`** — altı faz,
  her fazda 19 alan: amaç, kapsam, teslimatlar, yazım hedefi, kelime/sayfa
  hedefi, araştırma, test altyapısı, QA kapıları, DoD, PASS, FAIL, ajan
  notları, kurucu bağımlılıkları, git kilometre taşı, CI, çıktılar, riskler,
  faz devri
- **`00_CONTEXT/SOLVABILITY_STANDARD.md`** — bu projenin birinci varoluşsal
  kuralı: *bir bulmaca "zekice göründüğü" için kabul edilemez*. Beş şart,
  belirsizlik ölçeği, alternatif çözüm prosedürü, dış bilgi yasağı ve
  **öldürme kapısı eşikleri**
- **`00_CONTEXT/CONTENT_PROTECTION.md`** — ikinci varoluşsal kural:
  iki katmanlı içerik ve **dört hatlı** çözüm koruması. *Ama kod sır değildir*
- **`00_CONTEXT/HINT_LADDER.md`** — üç kademeli ipucu (yönlendirme → yöntem →
  neredeyse-cevap); Cain's Jawbone'un terk oranına doğrudan cevap
- **`00_CONTEXT/STYLE.md`** v1.0 — anlatı süslü olabilir, **talimat asla**;
  belirsizlik anlatıda serbest, talimatta bir *çözülebilirlik ihlali*
- **`00_CONTEXT/LESSONS_FROM_CODEX.md`** — iki referans projeden taşınan
  yedi mekanizma ve altı ders; **kod taşınmadı, disiplin taşındı**
- **`01_SOURCE/puzzle.schema.json`** — **iki katmanlı** şema:
  `publicPuzzle` (depoda durur, çözüm alanı taşıyamaz) ve
  `protectedSolution` (depoda durmaz)
- **Test altyapısı** — `validate_spec.py` (veri + kapsam + kapı +
  **public katmanda çözüm taraması** + sözleşme ve öldürme kapısı
  eşiklerinin korunması), `validate_structure.py` (dosya + gömülü değer +
  sızıntı + sır + **⭑ çözüm sızıntısı ⭑**),
  `selftest.py` (**kapıların kendi testi**, **on altı** kusurlu kurgu)
- **`04_BUILD/qa_all.sh`** — CI'ın birebir aynısı; Faz 1–5'te doğacak
  kapılar için satırlar şimdiden yazıldı (K18 dersi: ölü betik olmasın)
- **`.github/workflows/validate.yml`** — altı iş; `structure` işi
  **çözüm sızıntısını** her push'ta denetler
- **`.gitignore`** — **dört hatlı** çözüm koruması

### Kararlar

K1 (ortak kütüphane yok) · K2 (`.gate`) · K3 (Codex adı taşınır, tür
taşınmaz) · **K4 (bir bulmaca "zekice göründüğü" için kabul edilemez)** ·
**K5 (⛔ Faz 2 bir ÖLDÜRME KAPISIDIR)** · K6 (üç kademeli ipucu) ·
K7 (kapılar üçüncü taraf paket kullanmaz) · K8 (kapsam hipotez) ·
K9 (Kindle üretilmez) · **K10 (iki katmanlı içerik, dört hatlı koruma)** ·
K11 (6×9 normal trim) · K12 (Kapı V dizgiye bağlı, en son kilitlenir)

### Açık kararlar

A1 (manuscript ve **çözüm katmanı** politikası · Faz 1 başlamadan) ·
A2 (5 kapı teması) · **A3 (5 harici çözücü · Faz 2 bloklayıcısı)** ·
A4 (doğrulama sayfası) · A5 (STYLE onayı) · A6 (yazar biyografisi)

### Durum

`.gate` = `phase0` · **Faz 1 BAŞLAMADI** · kurucu onayı bekleniyor
