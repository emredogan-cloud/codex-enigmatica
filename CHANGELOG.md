# CHANGELOG — Codex Enigmatica

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.1.0] — 2026-08-13 · Faz 1 · Bulmaca mimarisi, çözülebilirlik, gizlilik

**Tek bir bulmaca yazılmadı.** Yazılan şey, yüz bulmacanın çözülebilir
olduğunu ispatlayacak makinedir.

### Eklendi

- **`01_SOURCE/mechanism_families.json`** — 17 mekanizma ailesi; her biri
  tanım · hedef zorluk · **tekillik ispatı** · kurgu örnek taşır
- **`01_SOURCE/gate_index.json`** — 5 kapı + son soru; bağımlılık ve
  yedek kuralları
- **`01_SOURCE/puzzle_index.json`** — **151 aday**, çözümsüz public kayıt;
  Kapı I'in 20 slotu Faz 2 pilot kohortu olarak işaretli
- **`01_SOURCE/research/sources.json`** — 16 künye, hepsi kamusal alan
- **`04_BUILD/qa_dependency.py`** — DAG: on kural, döngü yolunu raporlar
- **`04_BUILD/qa_taxonomy.py`** — çeşitlilik, ölü aile, metin karması, yedek havuz
- **`04_BUILD/page_budget.py`** — sayfa ve levha modeli; arka madde **türetilir**
- **`04_BUILD/validate_research.py`** — künye bütünlüğü ve doğrulama durumu
- **`04_BUILD/qa_solvability.py` · `qa_uniqueness.py` · `qa_hints.py`** —
  korumalı katman kapıları; boşken **sessizce yeşil yanmazlar**
- **`04_BUILD/qa_solution_leak.py`** — ⭑ **KANARYA** ⭑ alan adı değil
  **cevabın kendisini** arar: dosya, dosya adı, commit mesajı, yayın paketi
- **`04_BUILD/update_docs.py`** — `BOOK_STATS` ve `ROADMAP_PROGRESS` üretilir
- **`00_CONTEXT/`** — PUZZLE_TAXONOMY · SOLVER_TEST_PROTOCOL ·
  INTERNAL_SOLVER_PROTOCOL · RED_TEAM_CHECKLIST · SOURCING_STANDARD ·
  VISUAL_ARCHITECTURE · VALIDATION_REFERENCE
- **`06_REPORTS/PHASE_1_REPORT.md`**

### Değişti — kırmızı takım düzeltmeleri

İki bağımsız saldırı **36 bulgu** üretti; 30'u kapatıldı.

- `validate_structure.py` **yeniden yazıldı**: `git` aksadığında artık
  **kapalı başarısız** olur (eskiden bütün sızıntı denetimleri boş koşup
  yeşil yanıyordu); tarama bütün metin dosyalarına ve **Türkçeye** genişledi;
  muafiyetler **tam yol** oldu; config senkron denetimi eklendi
- `validate_spec.py` **yeniden yazıldı**: `puzzle.schema.json` artık
  **uygulanıyor** (`additionalProperties: false` → izin listesi) ve
  `testStatus: "tested"` **beş şartla kazanılıyor**
- `selftest.py` **123 denetime** çıktı; `validate_structure` fikstürleri
  **gerçek git deposu** kurar. Muafiyet listesi **donduruldu** — eski
  "gereklilik" testi bir muafiyeti meşrulaştırmanın yolunu tarif ediyordu
- `.gitignore` iki yerde **izin listesine** çevrildi; `06_REPORTS/` ve
  `01_SOURCE/puzzles/` kapatıldı; `01_SOURCE/design/` eklendi
- `puzzle.schema.json` **v2.0** — üç gizlilik sınıfı, `answerFormat`,
  `substitutableFor`, `boundToTextHash`
- **Kapı devri bağı kapatıldı** (K13) — bir yanlış kapı cevabı okuru
  ürünün %80'inden dışarıda bırakıyordu
- **Sayfa hedefi 208 → 230** (K17) — arka madde 24 sayfada imkânsızdı
- Kapı I'in zorluk eğrisi yeniden dizildi; imza mekaniğinin zorluk-1
  örneği eklendi; süre tahminleri şablon sabiti olmaktan çıktı
- Öldürme kapısına üç ölçüt: bulmaca başına çözücü tabanı, ipucu tüketimi
  tavanı, **medyan tanımı**
- Sözleşmenin **dördüncü sözü**: *kitap size bir çizelge veriyorsa, o
  çizelge tek yetkedir*

### Kararlar

**K13** (kapı devri kapatıldı) · **K14** (beşinci hat: kanarya) ·
**K15** (`tested` kazanılır) · **K16** (şema uygulanır) ·
**K17** (sayfa hedefi 230)

### Açık kararlar

A1 ✅ kapandı. Yeni: **A7** (bulmaca başına doğrulama) ·
**A8** (sayfa hedefi onayı) · **A9** (pilot levhalarının POD provası) ·
A10 (Faz 3'e ikinci öldürme kapısı) · **A11** (kanarya CI sırrı)

### Durum

`.gate` = `phase1` · **Faz 2 BAŞLAMADI** ·
⛔ **EXTERNAL VALIDATION PENDING** — beş harici çözücü yok (A3)

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
