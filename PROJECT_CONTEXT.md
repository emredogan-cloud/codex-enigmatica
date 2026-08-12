# PROJECT CONTEXT — Codex Enigmatica

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk belgedir.**
>
> Son güncelleme: **12 Ağustos 2026** · Faz: **0 · Bootstrap** · Kapı: `phase0`

---

## 1 · Proje kimliği

| | |
|---|---|
| Başlık | **Codex Enigmatica** |
| Alt başlık (hipotez) | One Hundred Engraved Enigmas and a Single Unbroken Mystery — A Puzzle Book Bound as a Grimoire |
| Seri | **Codex** · Cilt 3 — *ad ortaklığı var, dosya ortaklığı yok* |
| Depo | `emredogan-cloud/codex-enigmatica` |
| Okur | 25–55 bulmaca meraklısı · **alıcı = okur** |
| Kaynak | [`AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`](../AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html) § 11 · Kitap C |
| Portföy yeri | **Kitap C · üçüncü** · premium / viral aday |

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
| Faz | **0 · Bootstrap** — altyapı kuruldu, Faz 1 **başlamadı** |
| Kapı (`.gate`) | `phase0` |
| Aday bulmaca | 0 / ≥130 |
| Doğrulanmış / yazılmış | 0 / 100 |
| **Sonraki adım** | **KURUCU ONAYI** → sonra Faz 1 |

⚠ **Faz 1 BAŞLAMADI ve kurucu onayı olmadan başlamaz.**

---

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
ve hata **geri alınamaz**. Bu yüzden burada **dört hatlı** koruma vardır.

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
cat ROADMAP_PROGRESS.md              # ilerleme
grep -n "AÇIK KARAR" DECISIONS.md    # kurucudan yanıt bekleyenler

./04_BUILD/qa_all.sh                 # yeşilse CI de yeşil olur
```

⚠ **Çözüm dosyalarını asla commit etme.** Bir kez sızarsa git geçmişinden
temizlemek gerekir ve bu, geçmişi yeniden yazmak demektir.

---

## 11 · Açık bağımlılıklar

| # | Ne | Kimden | Ne zaman |
|---|---|---|---|
| A1 | Manuscript ve çözüm katmanı politikası | kurucu | **Faz 1 başlamadan** |
| A2 | 5 kapı teması onayı | kurucu | Faz 1 sonu |
| A3 | **5 harici çözücü kim** | kurucu | **Faz 2 bloklayıcısı** |
| A4 | Doğrulama sayfası barındırma | kurucu | Faz 5 |
| A5 | Kalibre edilmiş `STYLE.md` onayı | kurucu | Faz 2 |
| A6 | Yazar biyografisi metni | kurucu | Faz 5 |
| — | **Öldürme kapısı kararı** (FAIL hâlinde) | kurucu | Faz 2 |
| — | 110 levhanın üretilmesi | kurucu | Faz 5 |
| — | **POD prova kopya siparişi** | kurucu | Faz 5 |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

---

## 12 · Sonraki izinli eylem

> **KURUCU ONAYI BEKLENİYOR.**
>
> Bootstrap tamamlandı. Faz 1 **başlatılmadı**.
> İzin verildiğinde ilk iş: `faz/1-mimari` dalını açmak ve
> **gizlilik katmanını ilk gün kurmak** — bir çözümü yanlışlıkla public
> katmana yazmak, git geçmişinden silinmesi gereken bir olaydır.
