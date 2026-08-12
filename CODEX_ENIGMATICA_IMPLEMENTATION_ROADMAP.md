# CODEX ENIGMATICA — UYGULAMA YOL HARİTASI

> **Bu belge tek doğruluk kaynağıdır.** Altı faz, kapılar, testler, DoD.
>
> Sürüm: **1.0 · bootstrap** · Tarih: **12 Ağustos 2026** · Kapı: `phase0`
> Depo: `emredogan-cloud/codex-enigmatica`
>
> **Bu proje diğer bütün projelerden TAMAMEN İZOLEDİR.** Ortak dosya,
> ortak build çıktısı, ortak `.gate`, ortak rapor yoktur.
> Codex projeleri yalnızca **referans uygulama** olarak okunmuştur:
> [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## 0 · Bu kitap nedir

**Codex Enigmatica** — beş "kapı", her kapıda 20 bulmaca, ve 100 bulmacanın
çıktısını tek bir son soruya bağlayan bir meta-mister. Gravür levhaların
**içine gömülmüş** şifreler. Ve kademeli bir ipucu sistemi — çünkü amaç
okuru yenmek değil, **içeride tutmaktır**.

Pazar gerekçesi: mantık/zekâ oyunları Circana'nın büyüyen ekransız
kümesinde; premium/hediyelik baskı eğilimi fiyat toleransını yukarı
çekiyor. Ve bu rafta **talebi kanıtlanmış ama arzı neredeyse yok olan**
bir alt tür var: *tek mistere bağlı, tasarlanmış bulmaca-macera kitabı.*
Journal 29 ve Cain's Jawbone formun çalıştığını kanıtladı — ama dünyada bu
formda **onlarca başlık var, binlerce değil.**

Kaynak: [`AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`](../AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html) § 8 · WS-3 ve § 11 · Kitap C.

| | |
|---|---|
| Fırsat skoru | **8,1 / 10** |
| Prestij | **10 / 10** — portföyün tek "viral olabilir" ürünü |
| Üretim zorluğu | **9 / 10** — portföyün en zoru |
| Sıra | **#3 · en son yazılacak** |
| Ciltli birim telif (hipotez) | **9,85 $** · başabaş ACOS %32,8 |
| AI hendeği | **10 / 10** |

> **Neden en son?** Üç sebep: (1) üretimi 20–26 hafta, yani sermayeyi en
> uzun bağlayan proje; (2) kalite eşiği **kusursuzluk** — bir öğrenme
> deneyi olarak kullanılamaz; (3) asıl gücü Codex ciltlerine köprü kurmak
> ve o köprü ancak portföyün geri kalanı ayaktayken değer üretir.

---

## 1 · BU KİTABIN TANIMLAYICI PROBLEMİ: ÇÖZÜLEBİLİRLİK

Diğer iki kitabın ölüm biçimi *oyun çalışmıyor* ve *çocuk anlamıyor*.
Bu kitabınki daha serttir çünkü **asimetriktir**:

> ## Bir bulmaca "zekice göründüğü" için kabul EDİLEMEZ.
> ## Deterministik olarak çözülemeyen bir bulmaca bir ÜRETİM HATASIDIR.

Ve kusurun bedeli orantısızdır:

| | Kitap A / B | **Kitap C** |
|---|---|---|
| %90 kalite | Satılabilir ürün | **1 yıldız yağmuru** |
| Bir kusurlu madde | O madde zayıf | **Bütün kitap "bozuk"** |
| Okurun tepkisi | Hayal kırıklığı | **Öfke** |

Çözemeyen okur kendini aptal hissetmez — **aldatılmış** hisseder. Ve o
yorumu silemezsiniz.

Öncelik sırası — çakışmada yukarıdaki kazanır:

1. **Çözülebilirlik** — deterministik, tek cevaplı
2. **Belirsizlik yokluğu** — alternatif çözüm analizi yapılmış
3. **İpucu bütünlüğü** — okur pes etmeden ilerleyebiliyor
4. **Bağımlılık bütünlüğü** — DAG döngüsüz, ileri referans yok
5. **Levha okunabilirliği** — POD baskıda detay kaybolmuyor
6. Anlatı ve nesne kalitesi
7. Sayfa / kelime bütçesi

---

## 2 · Altı faz · tek bakışta

| Faz | Ad | Yazım | Kapı | Dal |
|---|---|---|---|---|
| **1** | Bulmaca mimarisi, çözülebilirlik çerçevesi, gizlilik katmanı | **yok** | `phase1` | `faz/1-mimari` |
| **2** | **20 bulmaca + 5 harici çözücü — ÖLDÜRME KAPISI** | ~6.000 kelime | `phase2` | `faz/2-pilot` |
| **3** | Kapı II (20 bulmaca) | ~6.500 kelime | `phase3` | `faz/3-kapi-2` |
| **4** | Kapı III–V (60 bulmaca) + meta-mister | ~15.500 kelime | `phase4` | `faz/4-kapi-3-5` |
| **5** | Editoryal yakınsama + levha üretimi + doğrulama sayfası | ~6.000 kelime | `phase5` | `faz/5-yakinsama` |
| **6** | Nihai üretim + KDP paketi | **yok** | `release` | `faz/6-uretim` |

**Faz 4 sonunda manuscript ÖZÜNDE TAMAMDIR.**

---

# FAZ 1 — BULMACA MİMARİSİ, ÇÖZÜLEBİLİRLİK ÇERÇEVESİ, GİZLİLİK KATMANI

### 1. Faz amacı
Üç şeyi kurmak: **(a)** bulmaca veri mimarisi ve çözülebilirlik tanımı,
**(b)** iki katmanlı gizlilik mimarisi, **(c)** bağımlılık grafiği modeli.
Bu fazda tek bir bulmaca **yazılmaz** — ama ≥130 bulmaca **fikri** kaydedilir.

### 2. Kapsam
- Bulmaca veri şeması: public katman + protected katman ayrımı
- Çözülebilirlik tanımı: "deterministik" ne demek, nasıl ölçülür
- Belirsizlik puanı (ambiguity score) ölçeği ve eşiği
- Üç kademeli ipucu sisteminin spesifikasyonu
- Bağımlılık grafiği (DAG) modeli ve döngü denetimi
- ≥130 bulmaca adayı (100'lük hedefin %30 fazlası)
- **Gizlilik katmanı**: neyin public, neyin protected olduğu

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `01_SOURCE/puzzle.schema.json` | **İki katmanlı** bulmaca şeması |
| `01_SOURCE/puzzle_index.json` | ≥130 aday · **çözümsüz** public kayıt |
| `01_SOURCE/gate_index.json` | 5 kapı · zorluk · bağımlılık kuralı |
| `00_CONTEXT/SOLVABILITY_STANDARD.md` | **Çözülebilirlik sözleşmesi** |
| `00_CONTEXT/CONTENT_PROTECTION.md` | **İki katmanlı gizlilik mimarisi** |
| `00_CONTEXT/HINT_LADDER.md` | Üç kademeli ipucu spesifikasyonu |
| `00_CONTEXT/STYLE.md` v1.0 | Faz 2'de kalibre edilecek |
| `04_BUILD/validate_spec.py` · `validate_structure.py` | Kapılar |
| `04_BUILD/qa_dependency.py` | **DAG bütünlüğü** |
| `05_TESTS/selftest.py` | **Kapıların kendi testi** |
| `06_REPORTS/PHASE_1_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
**YOK.** Bulmaca *fikirleri* kaydedilir, bulmaca *metni* yazılmaz.

### 5. Yaklaşık kelime hedefi
0 (bulmaca). Belgeler ~11.000 kelime.

### 6. Yaklaşık sayfa hedefi
0 manuscript sayfası. Sayfa modeli üretilir:
ön madde 10 + 5 kapı × 34 + son soru 6 + arka madde 24 = **210** →
hedef 208 ile karşılaştırılır.

> ⚠ Arka madde bu kitapta **24 sayfadır** ve kısaltılamaz: üç kademeli
> ipuçları × 100 bulmaca + tam çözümler + şifre referansı.
> **İpucu bölümü kitabın en önemli rekabet farkıdır** ve en çok sayfa yiyen
> kısımdır. Bütçe onu baştan tanır.

### 7. Araştırma gereksinimleri
- Şifre sistemleri (Ogham, runik, Vigenère, Polybius, semaphore) — kamusal alan
- Folklor motifleri — künye zorunlu
- **Rekabet araştırması**: Journal 29, Cain's Jawbone, The Paper Labyrinth'in
  *yapısal dersleri* ve *okur beklentileri*. ⚠ **Bu eserler KOPYALANMAZ**;
  yalnızca konumlanma ve yapı incelenir.

### 8. Test altyapısı
| Betik | Ne denetler |
|---|---|
| `validate_spec.py` | Şema, kimlik tekilliği, kapı dağılımı, kapsam |
| `qa_dependency.py` | **DAG döngüsüz mü · ileri referans var mı** |
| `validate_structure.py` | Depo, belge, gömülü değer, **ÇÖZÜM SIZINTISI** |
| `selftest.py` | **Kapılar gerçekten ısırıyor mu** |

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase1
```

### 10. Definition of Done
- [ ] `puzzle.schema.json` iki katmanlı yapıyı tanımlıyor
- [ ] ≥130 bulmaca adayı kaydedildi (**public kayıt — çözüm içermiyor**)
- [ ] Her adayın kapısı, zorluğu, tipi ve bağımlılıkları belirli
- [ ] **DAG döngüsüz** ve ileri referans yok
- [ ] `SOLVABILITY_STANDARD.md` onaylı
- [ ] `CONTENT_PROTECTION.md` onaylı ve `.gitignore` ile **tutarlı**
- [ ] `HINT_LADDER.md` onaylı
- [ ] `selftest.py` yeşil — **çözüm sızıntısı testi dahil**
- [ ] CI **YEŞİL** · `.gate` → `phase1`

### 11. PASS kriterleri
- ≥130 aday; her kapı ≥26 aday taşıyor
- DAG döngüsüz; her kapı bulmacası **yalnızca önceki** bulmacalara bağlı
- Çözüm sızıntısı taraması 0 bulgu
- Sayfa modeli 208 ± %6

### 12. FAIL kriterleri
- Aday <130 → kapsam gerçekçi değil
- DAG döngü içeriyor → **bloklayıcı**; bağımlılık modeli yeniden tasarlanır
- Herhangi bir çözüm public katmanda → **bloklayıcı**
- Bir kapı <26 aday → o kapının teması zayıf; tema değişir

### 13. Ajan öz-notları
- **Bulmaca fikri ≠ bulmaca.** Bu fazda kaydedilen şey "Kapı II'de gravürün
  tarama yönü veri taşıyacak" gibi bir *tasarım niyetidir*. Çözülebilirliği
  Faz 2 kanıtlar.
- Gizlilik katmanını **ilk gün** kur. Bir çözümü yanlışlıkla public
  katmana yazmak, git geçmişinden silinmesi gereken bir olaydır.
- DAG'i erken kur. Kapı IV'te "bu bulmaca Kapı V'e bağlı" fark etmek,
  60 bulmacayı yeniden sıralamak demektir.

### 14. Kurucu bağımlılıkları
| # | Ne | Ne zaman |
|---|---|---|
| A1 | Manuscript ve çözüm katmanı politikası | **Faz 1 başlamadan** |
| A2 | 5 kapı teması onayı | Faz 1 sonu |
| A3 | **5 harici çözücü kim** | **Faz 2 başlamadan** |
| A4 | Doğrulama sayfası barındırma kararı | Faz 5 |

### 15. Git kilometre taşı
```
dal: faz/1-mimari  ·  etiket: v0.1.0
```

### 16. CI gereksinimleri
`validate.yml` yeşil: `gate` · `data` · `structure` (**çözüm sızıntısı dahil**) ·
`gates-selftest` · `dependency` · `production-model`.

### 17. Beklenen çıktılar
`puzzle.schema.json` · `puzzle_index.json` · `gate_index.json` ·
`qa-dependency.json` · `page-budget.json` · `PHASE_1_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Çözüm public katmana sızar | İki hatlı koruma + `selftest` sızıntı testi |
| DAG karmaşıklaşır | Kural: bir bulmaca **yalnızca kendi kapısındaki önceki** bulmacalara bağlanabilir |
| 130 aday fikir bulunamaz | Aday bir *fikirdir*, çözülmüş bulmaca değil — eşik düşüktür |

### 19. Faz devri
Faz 2'ye girmek için: `.gate` = `phase1`, CI yeşil, A2 kapalı,
**5 harici çözücü belirlenmiş** (A3).

---

# FAZ 2 — ⛔ ÖLDÜRME KAPISI: 20 BULMACA + 5 HARİCİ ÇÖZÜCÜ

> ## BU FAZ DİĞER İKİ PROJEDE OLMAYAN BİR ŞEYE SAHİPTİR: BİR ÖLDÜRME KAPISI.
>
> Bozuk bir bulmaca sistemi üzerine 200 sayfa yazmak, bu portföyün
> yapabileceği **en pahalı hatadır**. Bu faz o hatayı imkânsızlaştırır.

### 1. Faz amacı
Kapı I'in 20 bulmacasını yazmak ve **5 harici çözücüyle test etmek**.
Sonuç, projenin devam edip etmeyeceğini belirler.

### 2. Kapsam
Kapı I · **The Threshold** · 20 bulmaca · zorluk ★
\+ çerçeve anlatının açılışı + sözleşme sayfası + ısınma bölümü
\+ üç kademeli ipuçlarının ilk hâli

> **Neden Kapı I?** Çünkü **bu kapıyı geçemeyen okur kitabı iade eder.**
> En çok test edilmesi gereken bölüm ilk bölümdür.

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `02_MANUSCRIPT/book.json` | 20 bulmaca · **depo dışı** |
| `01_SOURCE/solutions/gate-1.json` | Çözümler · **depo dışı, protected** |
| `06_REPORTS/solver/` | Çözücü test kayıtları · **ham hâli depo dışı** |
| `06_REPORTS/tracked/kill-gate-report.json` | **Öldürme kapısı kararı — depoda durur** |
| `00_CONTEXT/STYLE.md` v2.0 | Ölçümle kalibre |
| `04_BUILD/qa_solvability.py` | **Çözülebilirlik kapısı** |
| `04_BUILD/qa_uniqueness.py` | **Alternatif çözüm analizi** |
| `04_BUILD/qa_hints.py` | İpucu bütünlüğü |
| `06_REPORTS/PHASE_2_REPORT.md` | **Öldürme kapısı raporu** |

### 4. Yazım hedefi
20 bulmaca + çerçeve anlatı açılışı + sözleşme sayfası + 60 ipucu (20×3).

### 5. Yaklaşık kelime hedefi
**~6.000**.

### 6. Yaklaşık sayfa hedefi
**~44 sayfa** dizilmiş (10 ön madde + 34 kapı). 208'lik modelin ilk
gerçek doğrulaması.

### 7. Araştırma gereksinimleri
20 bulmacanın dayandığı her şifre sistemi ve folklor motifi künyeli.

### 8. Test altyapısı

```
qa_solvability.py  → her bulmacanın çözüm yolu adım adım kayıtlı mı
                   → çözüm yolu YALNIZCA kitap içi bilgiyle yürüyor mu
                   → belirsizlik puanı ≤ 2 mi
qa_uniqueness.py   → alternatif çözüm analizi yapılmış mı
                   → onaylanmış alternatif çözüm var mı (VARSA KIRMIZI)
qa_hints.py        → üç kademe eksiksiz mi
                   → ipucu metni cevabı İÇERİYOR MU (içeriyorsa KIRMIZI)
qa_dependency.py   → DAG döngüsüz · ileri referans yok
```

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase2
```

### 10. Definition of Done
- [ ] 20 bulmaca yazıldı, çözümleri **protected katmanda**
- [ ] Her bulmaca için çözüm yolu adım adım kayıtlı
- [ ] Alternatif çözüm analizi 20/20 yapıldı
- [ ] 60 ipucu yazıldı; **hiçbiri cevabı içermiyor**
- [ ] **5 harici çözücü Kapı I'i denedi ve kayıtlar alındı**
- [ ] `kill-gate-report.json` üretildi ve **karar verildi**
- [ ] `STYLE.md` ölçümle güncellendi
- [ ] CI **YEŞİL** · `.gate` → `phase2`

### 11. PASS kriterleri — ÖLDÜRME KAPISI

| Ölçüt | Eşik |
|---|---|
| Kapı I'i **bitiren** çözücü | **≥ 4 / 5** |
| Hiçbir çözücünün çözemediği bulmaca | **0** |
| Onaylanmış alternatif çözüm | **0** |
| Medyan tamamlama süresi | **≤ 240 dakika** |
| Belirsizlik puanı > 2 olan bulmaca | **0** |

### 12. FAIL kriterleri — ⛔ SERT DURDURMA

> ### 5 çözücüden 3'ünden AZI Kapı I'i bitirirse:
> ## PROJE DURUR VEYA YENİDEN TASARLANIR.
> ### YAZIMA DEVAM EDİLMEZ.

Ara sonuçlar:

| Sonuç | Karar |
|---|---|
| 4–5 çözücü bitirdi, 0 alternatif çözüm | ✅ **DEVAM** |
| 4–5 bitirdi ama alternatif çözüm var | ⚠ İlgili bulmacalar yeniden yazılır, **test tekrarlanır** |
| Tam 3 bitirdi | ⚠ **Zorluk eğrisi bozuk.** Kapı I yeniden tasarlanır, test tekrarlanır |
| ≤2 bitirdi | ⛔ **SERT DURDURMA** — sistem çalışmıyor. Kurucu kararı gerekir |

### 13. Ajan öz-notları
- **Çözücü testini sen yapamazsın.** Çözümü zaten biliyorsun; senin
  "çözülebilir" yargın kanıt değildir. Test **harici insanlarladır**.
- Bir çözücü takılıyorsa suç çözücüde değil **bulmacadadır**.
- **Bu fazın sonucunu güzelleştirme.** Öldürme kapısının değeri
  dürüstlüğünden gelir. 3/5 sonucu "neredeyse 4" değildir.
- Çözüm dosyalarını **asla** commit etme. Bir kez sızarsa git geçmişinden
  temizlemek gerekir ve bu, geçmişi yeniden yazmak demektir.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| A3 | **5 harici çözücü** — Faz 2'nin SERT BLOKLAYICISI |
| A5 | Kalibre edilmiş `STYLE.md` onayı |
| — | **Öldürme kapısı kararı** (FAIL hâlinde) |

### 15. Git kilometre taşı
```
dal: faz/2-pilot  ·  etiket: v0.2.0  ·  "öldürme kapısı: GEÇTİ"
```
⚠ Etiket yalnızca **PASS** hâlinde atılır.

### 16. CI gereksinimleri
`gates-selftest` yeni üç kapıyı da kapsamalı. **Çözüm sızıntısı kapısı
her push'ta koşar.**

### 17. Beklenen çıktılar
`book.json` (20) · `kill-gate-report.json` · `qa-solvability.json` ·
`qa-uniqueness.json` · `qa-hints.json` · `PHASE_2_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Çözücü bulunamıyor | Faz 2 **bloklanır**. Sahte test kaydı üretilmez |
| Çözücüler birbirine ipucu veriyor | Test **bağımsız** yapılır; kayıtta doğrulanır |
| Kapı I çok zor çıkıyor | Tam da bunun için var — 20'de bulmak 100'de bulmaktan **beş kat** ucuz |
| Ajan sonucu iyimser yorumluyor | Eşikler **sayısaldır** ve config'de durur; yoruma yer yok |

### 19. Faz devri
Faz 3'e girmek için: **öldürme kapısı GEÇTİ**, `STYLE.md` v2.0 onaylı,
`.gate` = `phase2`.

---

# FAZ 3 — KAPI II · THE MENAGERIE

### 1. Faz amacı
İkinci kapıyı yazmak ve şablonun **ölçekte** ve **daha yüksek zorlukta**
çalıştığını kanıtlamak.

### 2. Kapsam
Kapı II · **The Menagerie** · 20 bulmaca · zorluk ★★

Bu kapı Codex Bestiarium'un motif tabanını bulmacaya çevirir ve
**portföy içi en güçlü çapraz satış tetikleyicisidir**: bulmacayı çözen
kişi kaynağı merak eder.

> ⚠ Bestiarium'dan **motif fikri** alınır, **dosya alınmaz**. İzolasyon
> kuralı geçerlidir; Bestiarium deposu bu projenin bağımlılığı değildir.

### 3. Teslimatlar
- `book.json` → 40 bulmaca
- Kapı II çözümleri (protected)
- 60 yeni ipucu
- Kapı II için **≥2 harici çözücü** testi
- `06_REPORTS/PHASE_3_REPORT.md`

### 4. Yazım hedefi
20 bulmaca + kapı bulmacası + 60 ipucu.

### 5. Yaklaşık kelime hedefi
**~6.500** · kümülatif ~12.500.

### 6. Yaklaşık sayfa hedefi
~34 → kümülatif **~78**.

### 7. Araştırma gereksinimleri
Folklor motifleri künyeli. Levha içi şifreler için **görsel taşıma
kapasitesi** ölçülür: bir gravür kaç bit veri taşıyabilir?

### 8. Test altyapısı
Faz 2 kapıları + `qa_plate_data.py` (levha içi şifrelerin taşıdığı verinin
baskıda okunabilir kalıp kalmadığının ön ölçümü).

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase3
```

### 10. Definition of Done
- [ ] 40 bulmaca yazıldı ve doğrulandı
- [ ] Kapı II için ≥2 harici çözücü testi geçti
- [ ] Alternatif çözüm analizi 40/40
- [ ] DAG hâlâ döngüsüz
- [ ] CI **YEŞİL** · `.gate` → `phase3`

### 11. PASS kriterleri
- 40/40 deterministik ve tek cevaplı
- Kapı II'yi ≥2 çözücüden ≥1'i ipuçlarıyla bitirdi
- Belirsizlik puanı >2 olan bulmaca yok

### 12. FAIL kriterleri
- Alternatif çözüm bulundu → **o bulmaca yeniden yazılır**, havuzdan değişir
- Levha içi şifre baskıda okunmuyor → **mekanik değişir** (Faz 5'e bırakılmaz)
- DAG döngü kazandı → bloklayıcı

### 13. Ajan öz-notları
- Levha içi şifre bu kitabın **imza mekaniğidir** ve aynı zamanda en kırılgan
  parçasıdır. Baskı testi Faz 5'e bırakılmaz; ön ölçüm **burada** yapılır.
- Zorluk ★★'ye çıkarken ipucu kademeleri daha da kritikleşir.

### 14. Kurucu bağımlılıkları
≥2 harici çözücü (süregelen).

### 15. Git kilometre taşı
```
dal: faz/3-kapi-2  ·  etiket: v0.3.0
```

### 16. CI gereksinimleri
Tam `validate.yml`.

### 17. Beklenen çıktılar
`book.json` (40) · `qa-plate-data.json` · `PHASE_3_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Levha şifresi baskıda kayboluyor | Ön ölçüm bu fazda; mekanik değişebilir |
| Zorluk sıçraması çok sert | Çözücü testi kapı bazında yapılır |

### 19. Faz devri
Faz 4: kalan üç kapı + meta-mister.

---

# FAZ 4 — KAPI III–V + META-MİSTER

### 1. Faz amacı
**Manuscript'i özünde tamamlamak** ve 100 bulmacayı tek bir son soruya
bağlamak.

### 2. Kapsam
- Kapı III · **The Calendar** · 20 bulmaca · ★★
- Kapı IV · **The Labyrinth** · 20 bulmaca · ★★★
- Kapı V · **The Mirror** · 20 bulmaca · ★★★ (öz-göndergesel)
- **THE LAST QUESTION** — meta-mister
- Arka madde: 300 ipucu (100×3) · tam çözümler · şifre referansı · kolofon

### 3. Teslimatlar
- `book.json` → **100 bulmaca**
- Meta-mister ve doğrulama mekanizması spesifikasyonu
- Tam ipucu seti (300) ve tam çözüm seti (protected)
- Kapı III–V için harici çözücü testleri
- `06_REPORTS/PHASE_4_REPORT.md`

### 4. Yazım hedefi
60 bulmaca + meta-mister + çerçeve anlatının kapanışı + 180 ipucu.

### 5. Yaklaşık kelime hedefi
**~15.500** · kümülatif **~28.000**.

### 6. Yaklaşık sayfa hedefi
~102 gövde + 6 son soru + 24 arka madde → **~184** (ön madde Faz 5'te).

### 7. Araştırma gereksinimleri
Kalan şifre sistemleri ve motifler künyeli.

### 8. Test altyapısı
Tam kapı seti + `qa_meta.py`:

```
qa_meta.py → meta-misterin girdisi, BEŞ KAPININ ÇIKTISINDAN mı türüyor
           → her kapının katkısı gerçekten üretiliyor mu
           → son sorunun cevabı kitapta YOK mu (olmamalı)
```

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase4
```

### 10. Definition of Done
- [ ] **100 bulmaca yazıldı ve doğrulandı**
- [ ] Meta-mister beş kapıya bağlandı ve mekanik olarak doğrulandı
- [ ] 300 ipucu tamam; **hiçbiri cevabı içermiyor**
- [ ] Alternatif çözüm analizi 100/100
- [ ] DAG döngüsüz; ileri referans yok
- [ ] **Manuscript özünde tamam**
- [ ] CI **YEŞİL** · `.gate` → `phase4`

### 11. PASS kriterleri
- 100 bulmaca · 5 kapı — **alt başlıktaki sayı doğrulandı**
- 100/100 deterministik, tek cevaplı, belirsizlik ≤2
- Meta-mister doğrulandı
- Sayfa modeli 208 ± %6

### 12. FAIL kriterleri
- Bulmaca <100 → **alt başlık değişir** (kurucu kararı) veya havuzdan tamamlanır
- Meta-mister bir kapının çıktısını kullanmıyor → **bloklayıcı**
- Son sorunun cevabı kitapta bulunuyor → **bloklayıcı** (doğrulama sayfasının anlamı kalmaz)

### 13. Ajan öz-notları
- Kapı V öz-göndergeseldir: kitabın **fiziksel yapısını** kullanır
  (sayfa numaraları, dizin, kolofon). Bu, dizgi değişirse **kırılır** —
  Faz 5'te dizgi dondurulmadan Kapı V son hâlini alamaz.
- Meta-mister aceleye gelmez. Bu, kitabın **varlık sebebidir**.

### 14. Kurucu bağımlılıkları
Harici çözücüler (süregelen) · A4 (doğrulama sayfası kararı).

### 15. Git kilometre taşı
```
dal: faz/4-kapi-3-5  ·  etiket: v0.4.0  ·  "manuscript özünde tamam"
```

### 16. CI gereksinimleri
`validate_spec.py --gate phase4` kapsamı **sert** denetler.

### 17. Beklenen çıktılar
`book.json` (100) · `qa-meta.json` · `PHASE_4_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Kapı V dizgiye bağlı, dizgi değişirse kırılır | Kapı V'in son hâli Faz 5'te dizgi donduktan sonra kilitlenir |
| 300 ipucu yazmak sıkıcı ve savsaklanır | İpucu sistemi kitabın **rekabet farkıdır**; `qa_hints` eksik ipucuyu kırmızı yakar |
| Son kapılarda kalite düşer | `qa_drift` + kapı bazında çözücü testi |

### 19. Faz devri
Faz 5'e girmek için manuscript tam, CI yeşil.

---

# FAZ 5 — EDİTORYAL YAKINSAMA + LEVHA ÜRETİMİ + DOĞRULAMA SAYFASI

### 1. Faz amacı
Metni yakınsamak, ~110 levhayı üretmek, **POD baskı testini yapmak** ve
doğrulama sayfasını canlıya almak.

### 2. Kapsam
- Ön madde: çerçeve anlatı açılışı · sözleşme sayfası · araçlar levhası · ısınma
- **LINE EDITOR alt-ajanı** — bulmaca ifadesi ve belirsizlik odaklı
- ~110 gravür levha — hepsi **bulmacayı taşıyan işlevsel görsel**
- **POD baskı testi** — prova kopyada levha detayı okunuyor mu
- Doğrulama sayfası (statik) canlıya alınır
- İç blok dizgisi **dondurulur** → Kapı V kilitlenir

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` | Prompt kütüphanesi |
| `07_ASSETS/raw/` | Kurucunun PNG'leri — **SALT OKUNUR** |
| `06_REPORTS/tracked/plate-print-test.json` | **POD baskı testi ölçümü** |
| `04_BUILD/interior.py` · `metadata.py` | Üretim |
| `06_REPORTS/LINE_EDITOR_REPORT.md` | Alt-ajan bulguları |
| `06_REPORTS/PHASE_5_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
Ön madde ve çerçeve anlatı. **Yeni bulmaca yazılmaz.**

### 5. Yaklaşık kelime hedefi
**~6.000** · kümülatif **~34.000**.

### 6. Yaklaşık sayfa hedefi
10 ön madde → toplam **~208**.

### 7. Araştırma gereksinimleri
Yeni araştırma yok.

### 8. Test altyapısı
Tam kapı seti + görsel hattı + **`qa_plate_readability.py`**:

```
qa_plate_readability.py → levha içi şifrenin taşıdığı detay, POD baskı
                          çözünürlüğünde ayırt edilebiliyor mu
                        → prova kopya ölçümüyle karşılaştırılır
```

> **Bu, bu kitabın en kritik teknik kapısıdır.** Bir levhada kaybolan
> detay bulmacayı **çözülemez** yapar — ve bunu okur öğrenir, siz değil.

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase5
```

### 10. Definition of Done
- [ ] Ön madde ve çerçeve anlatı yazıldı
- [ ] **LINE EDITOR raporu alındı ve geçerli düzeltmeler uygulandı**
- [ ] 110/110 levha üretildi ve doğru bulmacaya bağlandı
- [ ] **POD prova kopya alındı ve levha okunabilirliği ölçüldü**
- [ ] İç blok dizgisi **donduruldu** → Kapı V kilitlendi
- [ ] Doğrulama sayfası **canlı**
- [ ] CI **YEŞİL** · `.gate` → `phase5`

### 11. PASS kriterleri
- Gerçek sayfa 208 ± %6
- **110/110 levhanın taşıdığı veri prova baskıda okunabiliyor**
- Line Editor'ın bloklayıcı bulgusu kalmadı
- Doğrulama sayfası son soruyu doğru kabul ediyor

### 12. FAIL kriterleri
- Bir levhanın verisi baskıda kayboluyor → **bloklayıcı**; levha veya
  bulmaca mekaniği değişir
- Dizgi değişti ve Kapı V kırıldı → **bloklayıcı**
- Doğrulama sayfası yanlış cevabı kabul ediyor → bloklayıcı

### 13. Ajan öz-notları
- **Line Editor bir alt-ajandır ve körü körüne kabul edilmez.**
- Bu kitapta Line Editor'ın özel görevi: **bulmaca ifadesi, belirsizlik ve
  ipucu tutarlılığı**. Bir kelimenin iki anlama gelmesi burada üslup
  meselesi değil, **çözülebilirlik meselesidir**.
- POD baskı testi atlanamaz. Ekranda kusursuz görünen bir gravür,
  kâğıtta 300 dpi'de detay kaybedebilir.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| — | **110 levhanın üretilmesi** |
| — | **POD prova kopya siparişi** |
| A4 | Doğrulama sayfası barındırma |
| A6 | Yazar biyografisi metni |

### 15. Git kilometre taşı
```
dal: faz/5-yakinsama  ·  etiket: v0.5.0
```

### 16. CI gereksinimleri
`validate.yml` + `images.yml` + `build.yml` yeşil.

### 17. Beklenen çıktılar
`IMAGE_PROMPT_LIBRARY.html` · işlenmiş levhalar · `plate-print-test.json` ·
iç blok PDF · `LINE_EDITOR_REPORT.md` · `PHASE_5_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| **Levha detayı POD baskıda kayboluyor** | Bu fazda ölçülür; notasyon Faz 3'ten beri muhafazakâr |
| Dizgi değişikliği Kapı V'i kırar | Dizgi bu fazda **dondurulur**, Kapı V ondan sonra kilitlenir |
| Doğrulama sayfası bakım yükü | Statik sayfa; bağımlılık yok |

### 19. Faz devri
Faz 6: format üretimi ve KDP paketi.

---

# FAZ 6 — NİHAİ ÜRETİM + KDP PAKETİ

### 1. Faz amacı
Yüklemeye hazır dosyaları üretmek ve kurucuya teslim paketi vermek.

### 2. Kapsam
Ciltli · ciltsiz üretimi · kapak · A+ · metadata · teslim kılavuzu.

> **Kindle üretilmez.** Görsel şifreler e-okuyucuda bozulur; iade ve kötü
> yorum üretir. Bu bir gelir kaybı değil, **itibar korumasıdır**.

### 3. Teslimatlar
`08_OUTPUT/PAPERBACK/` · `08_OUTPUT/HARDCOVER/` · `03_APLUS/` ·
`06_REPORTS/tracked/metadata.json` · `KDP_UPLOAD_PLAYBOOK.md` ·
`06_REPORTS/FINAL_RELEASE_REPORT.md`

### 4–6. Yazım / kelime / sayfa
**Yeni yazım yok.** Sayfa sayısı dondurulmuştu (Faz 5); burada yalnızca
doğrulanır — çünkü Kapı V ona bağlıdır.

### 7. Araştırma gereksinimleri
Yok.

### 8. Test altyapısı
`package_selftest.py` · `covers.py --check` · `aplus.py --check` ·
`handoff.py --check` · **`qa_solution_leak.py` (son tarama)**

> Son tarama: yayın paketinde **çözüm dosyası bulunmadığı** doğrulanır.
> Bir çözüm dosyasının yanlışlıkla `08_OUTPUT`'a girmesi, ürünü
> yayımlanmadan değersizleştirir.

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh release
```

### 10. Definition of Done
- [ ] İki format üretildi ve doğrulandı
- [ ] Sayfa sayısı doğrulandı (Kapı V hâlâ geçerli)
- [ ] Kapak geometrisi · sırt · bleed doğrulandı
- [ ] Metadata tam · **`authorBio` dolu**
- [ ] Doğrulama sayfası canlı ve URL metadata'da
- [ ] **Çözüm sızıntısı son taraması temiz**
- [ ] `KDP_UPLOAD_PLAYBOOK.md` yazıldı
- [ ] CI **YEŞİL** · `.gate` → `release`
- [ ] **AJAN DURUR**

### 11. PASS kriterleri
Üretim kapıları yeşil · teslim paketi eksiksiz · **çözüm sızıntısı 0**.

### 12. FAIL kriterleri
- `authorBio` null → kırmızı
- Sahte ISBN → kırmızı
- **Yayın paketinde çözüm dosyası** → kırmızı
- Sayfa sayısı değişti ve Kapı V kırıldı → kırmızı

### 13. Ajan öz-notları
- **KDP paneline dokunma.**
- Son taramayı atlamak, bu projede yapılabilecek en pahalı ihmaldir.
- Nihai raporu yazdıktan sonra **DUR**.

### 14. Kurucu bağımlılıkları
KDP paneli · prova kopya · yayın kararı.

### 15. Git kilometre taşı
```
dal: faz/6-uretim  ·  etiket: v1.0.0  ·  "release candidate"
```

### 16. CI gereksinimleri
`validate.yml` + `build.yml` + `release.yml` yeşil.

### 17. Beklenen çıktılar
Yüklemeye hazır iki format · kapaklar · A+ · metadata · playbook · nihai rapor.

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Çözüm yayın paketine sızar | Son tarama kapısı; `08_OUTPUT` içerik denetimi |
| KDP metadata reddi | Yer tutucu metin YASAK |

### 19. Faz devri
**YOK — proje burada biter.**

---

## 3 · Sürekli kurallar

### Git akışı
Faz dalı → yerel `qa_all.sh` yeşil → commit → push → PR → **CI'ı bekle** →
yeşilse merge + etiket + `.gate` yükselt. **CI kırmızıyken hiçbir şey ilerlemez.**

### İki katmanlı içerik — bu projenin en sert kuralı

| PUBLIC | **PROTECTED** |
|---|---|
| Bulmaca metadatası (kimlik, kapı, zorluk, bağımlılık, durum) | **Çözümler** |
| Kod · CI · şema · doğrulayıcı · üretim aracı | **Çözüm yolları** |
| Belgeler · ölçüm raporları (çözüm içermeyen) | **İpuçları** |
| Bağımlılık grafiği (isimsiz) | **Bulmaca prozası** · **çözücü ham kayıtları** |

İki hat: `.gitignore` **yol** ile dışlar; `validate_structure.py §
check_solution_leak()` takip edilen dosyaların **içeriğine** bakar ve
çözüm alanı görürse CI'ı kırmızı yakar.

> **Bir doğrulayıcının kendisi sır değildir.** Kod public kalır; sır olan
> yalnızca çözümdür. Bu ayrım `CONTENT_PROTECTION.md`'de tanımlıdır.

### Çözülebilirlik kilidi
```
alternatif çözüm analizi yapılmamış  →  DOĞRULANMAMIŞ  →  YAZILAMAZ
belirsizlik puanı > 2                →  KABUL EDİLMEZ
ipucu cevabı içeriyor                →  KIRMIZI
```

### Sürüklenme disiplini
**Ölç → yorumla → düzelt.**

---

## 4 · Bu yol haritasının bilmediği şeyler

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| 130 çözülebilir bulmaca fikri bulunabilir mi | **Faz 1** |
| **Bulmaca sistemi gerçekten çalışıyor mu** | **Faz 2 · ÖLDÜRME KAPISI** |
| Levha içi şifre baskıda okunuyor mu | **Faz 3 ön ölçüm · Faz 5 kesin** |
| 100 bulmaca 208 sayfaya sığıyor mu | **Faz 2** (gerçek dizgi) |
| Meta-mister kurulabiliyor mu | **Faz 4** |
| Kitap viral olur mu | **bilinmiyor ve bilinemez** — raporun kendi uyarısı: bu ürünün varyansı portföyün en yükseğidir |

> Son satır önemlidir: bu kitabın iyimser senaryosu (~900 adet/yıl) ile
> muhafazakâr senaryosu (~65 adet/yıl) arasında **14 kat** fark var.
> Yol haritası bu belirsizliği ortadan kaldıramaz — yalnızca
> **ucuz tarafta** öğrenmeyi garanti eder: Faz 2'de, 100 bulmaca değil
> 20 bulmaca yazılmışken.
