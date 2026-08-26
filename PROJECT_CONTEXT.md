# PROJECT CONTEXT — Codex Enigmatica

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk belgedir.**
>
> Son güncelleme: **26 Ağustos 2026** · Faz: **6 · İNGİLİZCE TİCARİ SÜRÜM**
> Kapı: `phase5` (release seviyesinde de yeşil) · Giriş: ⚑ **KURUCU GEÇERSİZ KILMASI**
>
> ## ✅ KİTAP ARTIK İNGİLİZCEDİR — ve bu bir çeviri değildi
>
> | | |
> |---|---|
> | Ticari yüzeyde Türkçe sözcük | **0** (önce 9 533) |
> | Alfabe | **26 harf** · 6 işaret grubu (5·5·4·4·4·4) |
> | Yeniden atanan cevap | **101 / 101** |
> | Yeniden üretilen şifreli dize | **hepsi** |
> | Yeniden çizilen levha | **31 / 103** (sözleşmesi değişenlerin tamamı) |
> | Üç format | ciltsiz **274** · ciltli **274** · Kindle **46,0 MB** |
> | Kalite kapıları | **hepsi yeşil** — `phase5` ve `release` |
>
> → Rapor: [`06_REPORTS/FINAL_ENGLISH_REBUILD_REPORT.md`](06_REPORTS/FINAL_ENGLISH_REBUILD_REPORT.md)
> → Sert denetim: [`06_REPORTS/FINAL_BRUTAL_AUDIT.md`](06_REPORTS/FINAL_BRUTAL_AUDIT.md)
>
> ## ⚠ HARİCİ İNSAN DOĞRULAMASI HÂLÂ BEKLİYOR
>
> **External human validation remains pending.**
>
> | | |
> |---|---|
> | Ölçülen öldürme kapısı | ⛔ **HARD-STOP** (0/5 oturum) — **değişmedi** |
> | Yapılan harici oturum | **0** |
> | İnsan doğrulaması geçti mi | **HAYIR** |
> | Faz 3–6 girişi | ⚑ **kurucu geçersiz kılması** (A13 · A14) |
> | Yazılmış bulmaca | **101** · durum `drafted` |
> | Doğrulanmış bulmaca | **0** — hiçbiri `tested` DEĞİL |
>
> ⭑ **YENİDEN İNŞA BİR DOĞRULAMA DEĞİLDİR.** Türkçe pilot doğrulanmamıştı;
> İngilizce yeniden inşa da doğrulanmadı — ve inşa, ölçülecek şeyi
> DEĞİŞTİRDİĞİ için doğrulamayı devralamaz. Sıfırdan gerektirir.
>
> ⭑ **ÜÇ ŞEY BİRBİRİNİN YERİNE GEÇMEZ:**
> **ÖLÇÜLEN** (HARD-STOP) · **GEÇERSİZ KILINAN** (Faz 3–6 girişi) ·
> **HENÜZ DOĞRULANMAMIŞ** (harici insan testi).
>
> → Karar kaydı: `DECISIONS.md § A13 · A14`
> → Bloklayıcı: **A12b** (harici çözücü) · **A4** (doğrulama sayfası) ·
>   **A9** (POD prova)

---

## 1 · Proje kimliği

| | |
|---|---|
| Başlık | **Codex Enigmatica** |
| Alt başlık (hipotez) | One Hundred Engraved Enigmas and a Single Unbroken Mystery — A Puzzle Book Bound as a Grimoire |
| Seri | **Codex** · Cilt 3 — *ad ortaklığı var, dosya ortaklığı yok* |
| Depo | `emredogan-cloud/codex-enigmatica` |
| Okur | 25–55 bulmaca meraklısı · **alıcı = okur** |
| Kaynak | `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html` § 11 · Kitap C |
| Portföy yeri | **Kitap C · üçüncü** · premium / viral aday |


> **Pazar raporu bu depoda DEĞİLDİR.** `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`
> kurucunun çalışma dizininde duran **özel bir strateji belgesidir** ve üç
> public depoya kopyalanmaz. Bu belgede ona **künyeyle** atıf yapılır, bağ
> verilmez: bir depoyu klonlayan kişi o dosyaya ulaşamaz ve kırık bir bağ
> görmemelidir.

---

## 2 · Amaç

Beş kapı, her kapıda 20 bulmaca, ve 100 bulmacanın çıktısını tek bir son
soruya bağlayan bir meta-mister. Gravür levhaların **içine gömülmüş**
şifreler. Ve kademeli bir ipucu sistemi — çünkü amaç okuru yenmek değil,
**içeride tutmaktır**.

| | |
|---|---|
| Fırsat skoru | **8,1 / 10** |
| Prestij | **10 / 10** — portföyün tek "viral olabilir" ürünü |
| Üretim zorluğu | **9 / 10** — portföyün en zoru |
| AI hendeği | **10 / 10** |

---

## 3 · Bu proje ne DEĞİLDİR

| Değildir | Neden |
|---|---|
| *Codex serisinin üçüncü referans cildi* | Ad ortak, **tür değil**: bu bir oyundur (K3) |
| *Journal 29 / Cain's Jawbone taklidi* | O eserler yalnızca **konumlanma ve yapı** olarak incelendi; **kopyalanmadı** |
| *Bestiarium'un bulmaca eki* | Motif fikri alınır, **dosya alınmaz**; izolasyon geçerlidir |
| *Zor bir bulmaca kitabı* | Zorluk hedef değil; **çözülebilirlik** hedef |

---

## 4 · Şu anki durum

| | |
|---|---|
| Faz | **6 · İngilizce ticari sürüm** (kurucu geçersiz kılmasıyla) |
| Kapı (`.gate`) | `phase5` — `release` seviyesinde de yeşil |
| Manuscript dili | **`en`** · kaynak: `01_SOURCE/design/_generator_en/` |
| Aday bulmaca | **151** / ≥130 ✅ |
| Yazılmış (`drafted`) | **101** / 100 — beş kapı + son soru |
| **Doğrulanmış (`validated`)** | **0** / 100 — ⚠ harici kanıt YOK |
| Elle iş (kitap) | **719 işlem** · hiçbiri çaba tavanını aşmıyor |
| aha (kapı bazında) | **4,0 / 4,0 / 3,0 / 3,0 / 3,0** — K36 |
| **Çıkarım oranı** | **1,00 → 1,25 → 2,42 → 3,17 → 4,08** (yükseliyor) |
| Isınma | **17 örnek · 17/17 mekanizma** öğretiliyor |
| Kalite kapısı | **24 betik · selftest 242 denetim · hepsi yeşil** |
| Sayfa (ÖLÇÜLEN) | **274** ciltsiz · **274** ciltli · levha **103** · kelime **26.062** |
| **Sonraki adım** | **A12b** — harici çözücü oturumları (kurucu) |

⚠ **FAZ 6'NIN AJAN İŞİ BİTTİ; ÜÇ MADDESİ KURUCUYA AİT.** POD prova
**alınmadı**, doğrulama sayfası **canlı değil**, ISBN **yok**. Hiçbiri
uydurulmadı.

### Ne ölçüldü, ne ölçülmedi

| | |
|---|---|
| ✅ ÖLÇÜLDÜ | 101/101 tekil cevap · 5 086 aday dize elendi |
| ✅ ÖLÇÜLDÜ | çaba · aha tavanı · çıkarım oranı · levha verisi |
| ✅ ÖLÇÜLDÜ | DAG döngüsüz · yayılma yarıçapı ≤1 · sızıntı yok |
| ✅ ÖLÇÜLDÜ | meta-mister: beş kapı katkısı · cevap kitapta **YOK** |
| ✅ ÖLÇÜLDÜ | ticari yüzeyde **0** Türkçe sözcük (beş dosya) |
| ⛔ **ÖLÇÜLMEDİ** | **mürekkebin kâğıt üzerindeki davranışı** (A9) |
| ⛔ **ÖLÇÜLMEDİ** | **hiçbir insanın bu bulmacaları çözüp çözemediği** |

`06_REPORTS/solver/` **boştur** ve gerçek oturumlar gelene kadar boş kalır.

## 5 · Bu projenin iki varoluşsal kuralı

### ① ÇÖZÜLEBİLİRLİK
> **Bir bulmaca "zekice göründüğü" için kabul EDİLEMEZ.
> Deterministik olarak çözülemeyen bir bulmaca bir ÜRETİM HATASIDIR.**

Ve kusurun bedeli asimetriktir: diğer iki kitapta %90 kalite satılabilir
bir üründür; burada **%98 kalite bile 1 yıldızlarla cezalandırılır**.
Çözemeyen okur aptal hissetmez — **aldatılmış** hisseder.

→ [`00_CONTEXT/SOLVABILITY_STANDARD.md`](00_CONTEXT/SOLVABILITY_STANDARD.md)

### ② ÇÖZÜM KORUMASI
> **Bir bulmaca kitabının çözümleri ürünün kendisidir.**

Public depoda duran bir çözüm kitabı **yayımlanmadan** değersizleştirir —
ve hata **geri alınamaz**. Bu yüzden burada **beş hatlı** koruma vardır;
beşincisi (kanarya) alan adı değil **cevabın kendisini** arar.

Ama **kod sır değildir**: `04_BUILD/` ve `05_TESTS/` public kalır.

→ [`00_CONTEXT/CONTENT_PROTECTION.md`](00_CONTEXT/CONTENT_PROTECTION.md)

Öncelik sırası — çakışmada yukarıdaki kazanır:

1. **Çözülebilirlik**
2. **Belirsizlik yokluğu**
3. İpucu bütünlüğü
4. Bağımlılık bütünlüğü (DAG)
5. Levha okunabilirliği
6. Anlatı ve nesne kalitesi
7. Sayfa / kelime bütçesi

---

## 6 · ⛔ FAZ 2 BİR ÖLDÜRME KAPISIDIR

Bu, üç yeni projede **yalnızca burada** vardır.

20 bulmaca yazılır ve **5 harici çözücüyle** test edilir.

| Sonuç | Karar |
|---|---|
| 4–5 çözücü Kapı I'i bitirdi, 0 alternatif çözüm | ✅ **DEVAM** |
| Tam 3 bitirdi | ⚠ Kapı I yeniden tasarlanır, test tekrarlanır |
| **≤2 bitirdi** | ⛔ **PROJE DURUR veya YENİDEN TASARLANIR** |

Gerekçe: bozuk bir bulmaca sistemi üzerine 200 sayfa yazmak, bu portföyün
yapabileceği **en pahalı hatadır**.

Eşikler `project_config.json § killGate` içinde **sayısaldır** ve
`validate_spec.py` onların düşürülmesini yakalar — **yoruma yer yoktur**.

---

## 7 · İzolasyon kuralı

Bu depo bütün diğer projelerden **tamamen ayrıdır**. Ortak dosya, ortak
build, ortak `.gate`, ortak rapor yoktur. *Codex Mythologica* ve
*Codex Bestiarium* ile **ad ortaklığı vardır, dosya ortaklığı yoktur**.

Okunan dersler: [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## 8 · Altı faz — özet

| Faz | Ad | Yazım | Kapı |
|---|---|---|---|
| 1 | Bulmaca mimarisi, çözülebilirlik, gizlilik katmanı | yok | `phase1` |
| 2 | **20 bulmaca + 5 çözücü — ÖLDÜRME KAPISI** | ~6.000 | `phase2` |
| 3 | Kapı II | ~6.500 | `phase3` |
| 4 | Kapı III–V + meta-mister | ~15.500 | `phase4` |
| 5 | Yakınsama + levha üretimi + doğrulama sayfası | ~6.000 | `phase5` |
| 6 | Nihai üretim + KDP paketi | yok | `release` |

Tam yol haritası:
[`CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md`](CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md)

---

## 9 · Belge haritası

| Belge | Ne söyler | Kim değiştirir |
|---|---|---|
| [`CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md`](CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md) | **Tek doğruluk kaynağı** | kurucu onayıyla |
| [`BRIEF.md`](BRIEF.md) | Ürün, kitle, ticari model | kurucu |
| [`00_CONTEXT/SOLVABILITY_STANDARD.md`](00_CONTEXT/SOLVABILITY_STANDARD.md) | **Çözülebilirlik sözleşmesi** | kurucu onayıyla |
| [`00_CONTEXT/CONTENT_PROTECTION.md`](00_CONTEXT/CONTENT_PROTECTION.md) | **İki katmanlı gizlilik** | kurucu onayıyla |
| [`00_CONTEXT/HINT_LADDER.md`](00_CONTEXT/HINT_LADDER.md) | Üç kademeli ipucu | kurucu onayıyla |
| [`00_CONTEXT/PUZZLE_TAXONOMY.md`](00_CONTEXT/PUZZLE_TAXONOMY.md) | **17 mekanizma ailesi** ve tekillik ispatı | kurucu onayıyla |
| [`00_CONTEXT/SOLVER_TEST_PROTOCOL.md`](00_CONTEXT/SOLVER_TEST_PROTOCOL.md) | **Harici çözücü protokolü** | kurucu onayıyla |
| [`00_CONTEXT/INTERNAL_SOLVER_PROTOCOL.md`](00_CONTEXT/INTERNAL_SOLVER_PROTOCOL.md) | Solver A/B — **kanıt değil ön eleme** | sabit |
| [`00_CONTEXT/RED_TEAM_CHECKLIST.md`](00_CONTEXT/RED_TEAM_CHECKLIST.md) | Kontrol listesi + **bulgu defteri** | her faz |
| [`00_CONTEXT/SOURCING_STANDARD.md`](00_CONTEXT/SOURCING_STANDARD.md) | Künye ve olgu disiplini | kurucu onayıyla |
| [`00_CONTEXT/VISUAL_ARCHITECTURE.md`](00_CONTEXT/VISUAL_ARCHITECTURE.md) | Dört levha sınıfı | kurucu onayıyla |
| [`00_CONTEXT/VALIDATION_REFERENCE.md`](00_CONTEXT/VALIDATION_REFERENCE.md) | Hangi kapı neyi ısırır | her faz |
| [`00_CONTEXT/STYLE.md`](00_CONTEXT/STYLE.md) | Ses, kalıplar, yasaklar | Faz 2'de kalibre |
| [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md) | Taşınan disiplin | sabit |
| [`DECISIONS.md`](DECISIONS.md) | Kararlar + **AÇIK KARARLAR** | her faz |
| [`CHANGELOG.md`](CHANGELOG.md) | Ne değişti, neden | her faz |
| [`BOOK_STATS.md`](BOOK_STATS.md) | Ölçülen sayılar | **üretilir** |
| [`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md) | Faz ilerlemesi | **üretilir** |

---

## 10 · Bir ajan işe nasıl başlar

```bash
cd CODEX-ENIGMATICA

cat .gate                            # aktif faz kapısı
cat ROADMAP_PROGRESS.md              # ÜRETİLEN ilerleme tablosu
grep -n "AÇIK" DECISIONS.md          # kurucudan yanıt bekleyenler

./04_BUILD/qa_all.sh                 # yeşilse CI de yeşil olur
python3 05_TESTS/selftest.py         # kapılar gerçekten ısırıyor mu
```

Hangi kapının neyi denetlediği:
[`00_CONTEXT/VALIDATION_REFERENCE.md`](00_CONTEXT/VALIDATION_REFERENCE.md)

⚠ **Çözüm dosyalarını asla commit etme.** Bir kez sızarsa git geçmişinden
temizlemek gerekir ve bu, geçmişi yeniden yazmak demektir.

---

## 11 · Açık bağımlılıklar

| # | Ne | Kimden | Ne zaman |
|---|---|---|---|
| A1 | Manuscript ve çözüm katmanı politikası | — | ✅ **KAPANDI** (K10 + K14) |
| A2 | 5 kapı teması onayı | kurucu | **Faz 2 başlamadan** |
| A3 | **5 harici çözücü kim** | kurucu | ✅ **KAPANDI** (K18) |
| A4 | Doğrulama sayfası barındırma | kurucu | Faz 5 |
| A5 | Kalibre edilmiş `STYLE.md` onayı | kurucu | Faz 2 |
| A6 | Yazar biyografisi metni | kurucu | Faz 5 |
| **A7** | **Bulmaca başına doğrulama** | kurucu | **Faz 2 başlamadan** |
| **A8** | **Sayfa hedefi 230 onayı** | kurucu | ✅ **KAPANDI** (K17) |
| **A9** | **Pilot levhalarının POD provası** | kurucu | **Faz 2 başlamadan** |
| A10 | Faz 3'e ikinci öldürme kapısı | kurucu | Faz 3 başlamadan |
| A11 | `ENIGMATICA_CANARY_SALT` CI sırrı | kurucu | ✅ **KAPANDI** (K19) |
| — | **Öldürme kapısı kararı** (FAIL hâlinde) | kurucu | Faz 2 |
| — | 110 levhanın üretilmesi | kurucu | Faz 5 |
| — | **POD prova kopya siparişi** | kurucu | Faz 5 |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

---

## 12 · Sonraki izinli eylem

> ### ⚑ FAZ 6'NIN AJAN İŞİ BİTTİ — ÜÇ MADDE KURUCUYA AİT
>
> Yapıldı: **kaynak düzeyinde İngilizce yeniden inşa.** Alfabe 26 harfe
> indi, altı işaret grubu yeniden kuruldu, **101 cevabın hepsi çözücüyle
> yeniden atandı**, bütün şifreli dizeler yeniden üretildi, beş katalog
> sıfırdan yazıldı, **31 levha** yeniden çizildi ve üç formatın üçü de
> yeniden üretildi. Ticari yüzeyde **0** Türkçe sözcük.
>
> Yeniden inşa **kapı katmanında dört, dizgi katmanında on bir kusur**
> açığa çıkardı; on beşi de Türkçe baskıda da vardı ve onarıldı. İkisi
> ürünü bitiren cinstendi: biri son sorunun cevabını kitaba basıyordu.
>
> **Ama Definition of Done'ın üç maddesi ajan tarafından yapılamaz:**
>
> 1. **A12b** — harici çözücü oturumları · **0 / 5**
>    → `00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`
> 2. **A4** — doğrulama sayfasının barındırılması ve adresi
>    (son sorunun cevabı başka hiçbir yere yazılamaz)
> 3. **A9** — POD prova kopyası · mürekkebin kâğıt üzerindeki davranışı
>
> Ayrıca açık: **ISBN** · **AI açıklaması** · ciltli hesaplayıcının 274
> sayfayla yenilenmesi · kapak sanatının doğal çözünürlüğü (92,5 / 82,0 dpi)
>
> Ve hepsinin üstünde duran gerçek değişmedi:
> ölçülen öldürme kapısı **HARD-STOP** · harici oturum **0 / 5**.
>
> Ayrıntı: `DECISIONS.md § AÇIK KARARLAR` ·
> [`06_REPORTS/FINAL_ENGLISH_REBUILD_REPORT.md`](06_REPORTS/FINAL_ENGLISH_REBUILD_REPORT.md) ·
> [`06_REPORTS/FINAL_BRUTAL_AUDIT.md`](06_REPORTS/FINAL_BRUTAL_AUDIT.md)
