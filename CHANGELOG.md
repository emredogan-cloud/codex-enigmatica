# CHANGELOG — Codex Enigmatica

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.2.1] — 2026-08-13 · A12 · ⛔ ÖLDÜRME KAPISI DÜŞTÜ

**5 harici Türkçe çözücüden 1'i Kapı I'i bitirdi.** Eşik ≥4, sert
durdurma <3. Karar: **HARD-STOP**. Kurucu kararı: **yeniden tasarla**.

Baskın bırakma sebebi *"çözemedim"* değildi: **"sıkıldım"**. Kaydırma,
yansıma ve anahtarlı alfabe bulmacaları kâğıt kalemle yorucuydu.

### Eklendi

- **`04_BUILD/qa_effort.py`** — ⭑ öldürme kapısını kaybettiren ÖLÇÜLMEMİŞ
  boyut ⭑. Okurun kaç elle işlem yapacağını **cevap uzayı
  spesifikasyonundan** hesaplar ve bulmacanın **kendi süre iddiasına**
  karşı denetler. Hangi bulmacaların şikâyet edildiğini bilmeden koştu ve
  **aynı üç bulmacayı aynı sırayla** işaretledi (4,7× · 3,0× · 1,6×)
- **`06_REPORTS/GATE_1_REDESIGN_PROPOSAL.md`** — yeni mekanizma karışımı,
  çaba bütçeleri, zorluk rampası, B1–B6 kararları. **Yeni bulmaca
  YAZILMADI**
- `01_SOURCE/playtests/` — ham oturum kayıtları · dizin, içine tek satır
  yazılmadan **ÖNCE** korumalı listeye alındı (mahremiyet)

### Değişti

- `kill_gate.py` — **oturum düzeyi** toplu kaydı okur. Bulmaca başına
  kayıt yoksa kalan beş ölçütü `measured: false` işaretler: *"ihlal
  edilmedi"* ile *"ölçülmedi"* aynı şey değildir
- Pilot kohortun **20/20 kaydı** `testStatus: "failed"` — kohort olarak
  test edildi, kohort olarak düştü
- `PROTECTED_DIRS` 4 → **5**
- `05_TESTS/selftest.py` — **154 → 162** denetim

### Ölçüldü

| | |
|---|---:|
| Kapı I'i bitiren | **1 / 5** |
| Toplam elle işlem | **486 EU** |
| Çabanın ima ettiği süre | **162 dk** (bildirilen 153) |
| Bütçesini aşan bulmaca | **6 / 20** |
| En kötü bulmaca | **9,3×** (6 dk iddia · 56 dk en kötü hâl) |

### Öğrenilen

- **K23** — ölçülmeyen bir boyut, korunmayan bir boyuttur
- **K24** — `expectedCompletionMinutes` **kavrayışı** ölçüyordu,
  **yürütmeyi** değil; fark dokuz kat
- **K25** — **ispat sayar, okur gezmez**: `minDomainSize` ispatın sayım
  alanıdır, okurun elle tarayacağı alan değil

---

## [0.2.0-pilot] — 2026-08-13 · Faz 2 · Pilot bulmacalar, cevap uzayı, öldürme kapısı

**Yirmi Türkçe pilot bulmaca yazıldı ve bütün teknik kapılardan geçti.
Öldürme kapısı kararı: `BLOCKED` — beş harici çözücü oturumu YAPILMADI.**

Bu bir başarısızlık değil, kapının çalışmasıdır: ölçemediği bir şeyi
geçmiş sayan bir öldürme kapısı, olmayan bir kapıdan tehlikelidir.

### Eklendi

- **`04_BUILD/qa_answerspace.py`** — ⭑ Faz 2'nin birinci teslimatı ⭑
  Cevap uzayını **bağımsız açar**: yazarın listesini okumaz, bulmacanın
  girdisinden ve basılı çizelgelerden yeniden üretir. 1.072 aday dize
  üretildi ve elendi; **20/20 tam olarak bir üye kabul etti**
- **`04_BUILD/qa_handoff.py`** — devir ve hata davranışı: hata tespiti,
  teşhis işaretleri, kurtarma yolu, tek bir hatanın yayılma yarıçapı ≤1.
  Hata tespitinin **gücü ölçüldü**: asgari Hamming mesafesi **15**
- **`04_BUILD/qa_readerpack.py`** — bütün kapıların paylaştığı körlüğü
  kapatır: hepsi korumalı katmanı denetliyordu, hiçbiri **okurun eline
  ne geçtiğine** bakmıyordu
- **`04_BUILD/kill_gate.py`** — beş değerli karar; **veri yoksa GEÇMEZ**
- **`04_BUILD/pilot_pages.py`** — model ilk kez **gerçek metne** vuruldu
- **`04_BUILD/english_readiness.py`** — dönüşüm iş listesi (dönüşüm
  BAŞLATILMADI · § 23)
- **`04_BUILD/plate_proof.py`** — baskıya hazır prova paketi (A9 kurucu işi)
- **`00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`** — A12 devir belgesi
- 20 Türkçe pilot bulmaca · 60 ipucu · 80 alternatif aday · 81 çözüm adımı
  (**korumalı katmanda, depoda değil**)

### Değişti

- `_protected_layer` ve `qa_solution_leak` — **Türkçe katlaması** `ı/İ/I → i`.
  NFKD noktasız `ı`yı çözmez; `"IŞIK"` ile `"ışık"` iki farklı normal
  biçime sahipti ve kanarya küçük harfli bir sızıntıyı **kaçırırdı**
- `qa_hints` — **düz merdiven de kusurdur**: eski kural yalnızca azalmayı
  yakalıyordu, `[4,4,4]` geçiyordu. Merdiven artık çözüm yolundan **türetilir**
- `mechanism_families` — levha içi şifrenin cevap biçimi **ölçümle**
  düzeltildi; `sequence` bir varsayımdı
- `puzzle.schema.json` — `answerSpace` · `languagePortability` ·
  `answerSpaceSize` · `pilotLanguage`
- `project_config.json` — `language` · `security` · `answerSpace` ·
  `gateHandoff` · `plateProof` blokları; A3/A8/A9/A11 kararları
- `05_TESTS/selftest.py` — **123 → 151** denetim

### Düzeltildi (kırmızı takım · 23 bulgu)

- ⭑ **Sayı tablosu hata TESPİT ETMİYORDU.** Sekiz olası okumanın **beşi**
  tablodaydı; her levha bulmacasının beş ulaşılabilir cevabı vardı. Kapı
  bunu görmüyordu çünkü kabul yordamı **doğru okumayı sabit yazıyordu** —
  K21'in öldürmeye çalıştığı totoloji, doğrulayıcının kendi içinde
- ⭑ **On bulmaca okur paketinde ÇÖZÜLEMİYORDU.** Levha metni vardı, levha
  verisi yoktu
- ⭑ **Gerçek bir ikinci cevap** — kaynağı tek bir yanlış edattı. Aynı
  bulmacada ikinci bir ikinci cevap daha bulundu (taban işareti çentik
  sayılabiliyordu) ve **iki okuma da tekillik vaadini yerel olarak
  sağlıyordu**
- Kök neden: şekil üretiliyordu, onu tarif eden cümle **elle yazılıyordu**.
  Levha üreteci artık *(şekil, künye)* çifti döndürür
- Sözlük sırası Türkçe harf sırasına göre **üretiliyor**; sözlük numaraları
  sözcükten **türetiliyor**
- Yansıma işlemi hiçbir yerde tanımlı değildi → araçlar levhasına kural ve
  örnek eklendi
- İki bulmacada okunacak levha basılı değildi → levhalar eklendi
- Çizelge harflerinde C boşluğu vardı

### Ölçüldü

| | |
|---|---:|
| Cevap uzayı · bağımsız üretilen aday | **1.072** |
| Tam olarak bir kabul | **20 / 20** |
| Kapı I gövdesi | 8,5 / 34 sayfa |
| İpucu bölümü (kitap ölçeğinde) | 15,2 / 22 sayfa |
| Çözüm bölümü (kitap ölçeğinde) | 8,4 / 18 sayfa |
| Kapı sözü asgari Hamming mesafesi | **15** |
| **Harici çözücü oturumu** | **0 / 5** |

### Ses kalibrasyonu (kurucu geri bildirimi · A5)

Kurucu pilot metinlerini *"mekanik olarak kusursuz ama anlatısal olarak
ölü"* buldu. Üç iç çözücünün hiçbiri bunu bildirmemişti — **çünkü üçü de
çözebiliyordu.** Okuma yorgunluğu yalnızca insanın ölçebileceği şeydir.

Teşhis üslup değil **mimariydi**: `STYLE § 1` iki kayıt tanımlar ve
pilotun yirmi bulmacası da **yalnızca talimat kaydında** yazılmıştı.

- Her bulmacaya **anlatı satırı** eklendi — mekanik içerik taşımaz
- Talimat sınav registerinden **arşivci** registerine taşındı; ≤20
  kelime/cümle kuralı korundu (ölçülen medyan **7**)
- İpuçlarındaki **kümülatif tekrar** kaldırıldı: üç kademe artık her biri
  YENİ bir adım getirir, köprü cümlesi kapsamı taşır
- Ön madde, sözleşme sayfası ve ipucu sayfası seslendirildi
- **`STYLE.md` v2.0** — bantlar gerçek metinden ölçüldü
- ⚠ Bulmaca metni bandı (90–220) **doğrulanmadı**: ölçülen medyan **51**.
  Bant **düşürülmedi**; zorluğa göre ayrılması Faz 3'e ertelendi

**Kanıt:** `qa_solvability` · `qa_hints` · `qa_uniqueness` yeniden koştu,
üçü de yeşil. Belirsizlik, cevap uzayı ve merdiven kapsamı değişmedi.
Geçiş sırasında kapı bir kez ısırdı: bir fısıltı son çözüm adımıyla iki
içerik kelimesi paylaşıyordu ve *cevap anahtarı* olarak kırmızı yandı.

### Güvenlik

- **`ENIGMATICA_CANARY_SALT`** üretildi (384 bit), GitHub Actions sırrı
  olarak kuruldu, depo dışında `0600` yedeğe yazıldı. **Plaintext hiçbir
  çıktıda, commit'te, raporda veya kaynak dosyada görünmedi.**
- Dört senaryo gerçek bir klonda kanıtlandı: doğru tuz yeşil · **eksik tuz
  kırmızı** · **yanlış tuz kırmızı** · **enjekte edilmiş sızıntı yakalandı**
- Kanarya bu fazda **kendi yazarını iki kez ısırdı**: selftest fikstürünü
  ve bulgu defterini sızıntı olarak bildirdi. İkisinde de haklıydı.

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
