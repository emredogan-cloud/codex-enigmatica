# KIRMIZI TAKIM — kontrol listesi ve bulgu defteri

> *"Zeki bir okur bunu nasıl kırar?"*
>
> Sürüm 1.0 · Faz 1 · Bulgu defteri her fazda **büyür**, kısalmaz

---

## 1 · Bulmaca başına kontrol listesi

Her bulmaca için, harici teste gönderilmeden önce **on iki soru**. Hepsi
`01_SOURCE/design/*.json § redTeamNotes` içine yanıtlanır.

### Cevabın tekilliği

1. **Alternatif cevap** — ölçütü sağlayan ikinci bir dize var mı?
2. **Ters ve ayna** — yolun tersi, dizinin tersi, haritanın aynası da geçerli mi?
3. **Kapsayıcı/dışlayıcı** — sayım bir eksik veya bir fazla yapılabilir mi?
4. **Notasyon önçözümü** — basılı işaret birden çok değere karşılık geliyor mu?

### İfadenin belirsizliği

5. **Eşanlamlı** — cevabın başka bir adı var mı? (Folklor tabanlı bir kitapta
   **genellikle vardır**)
6. **Noktalama** — cümle noktalama olmadan da aynı şeyi mi söylüyor?
7. **Sıfat tuzağı** — *saklı · farklı · tuhaf · yersiz* geçiyor mu?
   Geçiyorsa **yeniden yaz**: bunlar yüklem değildir.
8. **Yön ve başlangıç** — okuma yönü ve başlangıç noktası metinde sabit mi?

### Bilgi ve kaynak

9. **Dış bilgi** — bir adım kitabın dışına çıkıyor mu?
10. **Dış bilgi ÇELİŞKİSİ** — konuyu **bilen** bir okur farklı bir cevaba
    varır mı? (Sözleşmenin dördüncü sözü tam olarak bunun içindir)

### Yapı

11. **Kısayol** — bulmaca, tasarlanan yol dışından çözülebiliyor mu?
12. **Sızıntı** — başlık, ipucu veya levha cevabı erken veriyor mu?

---

## 2 · Sistem düzeyi kontrol listesi

Her fazın sonunda:

- [ ] Bir ipucu, ait olmadığı bir bulmacanın cevabını veriyor mu
- [ ] İki bulmaca aynı cevabı veriyor mu (kapı bulmacası girdileri ayırt edemez)
- [ ] Kapı bulmacasının hata davranışı: bir girdi yanlışsa çıktı
      **tespit edilebilir** biçimde geçersiz mi, yoksa makul görünen başka
      bir dize mi
- [ ] Metne bağlı bulmacaların karması güncel mi
- [ ] Levha düzenlendi mi — düzenlendiyse ispat **yeniden** koştu mu
- [ ] Doğrulama sayfası normalizasyonu sözleşme sayfasıyla aynı mı

---

## 3 · FAZ 1 BULGU DEFTERİ

İki bağımsız alt-ajan saldırdı. **36 bulgu.** Hiçbiri yumuşatılmadı.

### 3.1 · Mimari saldırısı — kabul edilen ve kapatılan

| # | Bulgu | Nasıl kapatıldı |
|---|---|---|
| A1 | **Kapalı başarısızlık:** `git ls-files` çalışmazsa liste boş dönüyor, bütün sızıntı denetimleri boş koşup **yeşil yanıyordu** | `.git` varken boş liste artık **hata**; `≥20 dosya` şartı |
| A2 | `01_SOURCE/design/` — şemanın kendi PROTECTED katmanı — ne `.gitignore`'da ne `PROTECTED_DIRS`'te | İkisine de eklendi; `.gitignore` kapsaması `git check-ignore` ile **denetleniyor** |
| A3 | **Şemayı hiçbir kod okumuyordu.** 355 satır `additionalProperties:false` tanımı, yalnızca "var mı" diye denetleniyordu | `validate_spec` şemayı **uyguluyor**; izin listesi artık gerçek |
| A4 | Uzantı süzgeci: yalnızca 5 uzantı, **büyük/küçük harfe duyarlı**. `ANSWERS.JSON`, `leak.yml`, uzantısız dosya geçiyordu | Takip edilen **her metin dosyası** taranıyor; uzantı küçük harfe çevriliyor |
| A5 | Tarama alan **adı** arıyordu, **cevap** aramıyordu. Türkçe hiç yoktu | Değer tarafı iki dilde eklendi **+** `qa_solution_leak.py` kanaryası |
| A6 | `README.md` / `.gitkeep` muafiyeti **temel adaydı**: her alt dizin bir bedava dosya kazanıyordu | Muafiyet **tam yol**; muaf dosyalar yine içerik taramasından geçiyor |
| A7 | **Öldürme kapısı bir metin alanıydı.** 140 kaydın `status` alanını elle değiştirmek phase1'den release'e yürüyordu | `check_test_status`: beş şart + `status`↔`testStatus` bağı + kurucu onayı kilidi |
| A8 | Belirsizlik denetimi **opt-in**: alanı silmek denetimi kapatıyordu | Alan `validated`/`written` için **zorunlu** |
| A9 | selftest, `validate_structure`'ın **hiçbir** denetimini koşmuyordu | `run_structure_with()` — gerçek git deposu kuran fikstürler |
| A10 | Muafiyet "gereklilik" testi **tersti**: yeni bir muafiyeti meşrulaştırmanın yolu dosyaya çözüm işareti koymaktı | Liste **donduruldu**; tam küme eşitliği aranıyor |
| A11 | `06_REPORTS/*.json` takip ediliyor **ve CI artefaktı olarak yükleniyordu** — `qa_uniqueness` yapısı gereği cevap adaylarını yazacaktı | `.gitignore` izin listesine çevrildi; yalnızca `06_REPORTS/tracked/` |
| A12 | Commit **mesajları** hiç taranmıyordu — kalıcı ve geri alınamaz | Kanarya son 100 mesajı tarıyor |
| A13 | Dosya **adları** taranmıyordu (`plateId` içinde cevap) | Kanarya yolları da tarıyor |
| A14 | `01_SOURCE/puzzles/` yalnızca iki sonek için korunuyordu | İzin listesine çevrildi (`*.public.json`) |
| A15 | `PROTECTED_DIRS` diskte olmayan bir dizin içeriyordu; yazım hatası fark edilmezdi | Dizinler oluşturuldu; varlık + `.gitignore` kapsaması denetleniyor |
| A16 | Belge, kodun yapmadığı korumaları iddia ediyordu (4 muafiyet yazıyor, kodda 2 var) | Belge düzeltildi; selftest tam küme eşitliği arıyor |
| A17 | `SOLUTION_FIELD_MARKERS` elle yazılmış regexler; config listesiyle ayrışabilirdi | Kalıplar **adlardan türetiliyor**; üç yönlü senkron denetimi |
| A18 | Kurucu değeri taraması 4 uzantıyla sınırlıydı | Kod **ve veri** uzantılarına genişletildi (proza bilerek dışarıda — gerekçe kodda) |

### 3.2 · Tasarım saldırısı — kabul edilen ve uygulanan

| # | Bulgu | Nasıl karşılandı |
|---|---|---|
| T1 | **Kapı devri bağı**: bir kapıyı yanlış çözen okur ürünün %80'ine kapanıyordu, hiçbir teşhis olmadan | `crossGateEntryHandoff` → **false**. Devir anlatısal; kapılar bağımsız girilebilir |
| T2 | **Arka madde 24 sayfada imkânsızdı** — 300 ipucu + 100 çözüm ≈ 44 sayfa. Taşma dizgiyi kaydırır ve Kapı V'in sekiz bulmacasını kırar | Sayfa hedefi 208 → **230**; arka madde artık **türetiliyor**, elle yazılmıyor |
| T3 | Kapı I'de altı ardışık aynı aile, **iki kez** | Yeniden dizildi; en uzun ardışık dizi **2** |
| T4 | Kitabın **imza mekaniğinin** zorluk-1 örneği hiçbir yerde yoktu | `plate-embedded-cipher` bandı 1'e indi; Kapı I'e iki örnek |
| T5 | Süre tahminleri **şablon sabitiydi** (27 kayıtta aynı sayı) ve oturum yükü modelde yoktu | Slot bazlı rampa + 45 dk oturum yükü; `page_budget` düz eğriyi **kırmızı yakıyor** |
| T6 | `puzzlesUnsolvedByAllSolvers: 0` ölçütü, 5'te 1 çözülen bulmacayı geçiriyordu | `minSolversPerPuzzle: 2` eklendi |
| T7 | İpucu tüketimi hiç ölçülmüyordu | `maxSolversNeedingLevel3Hint: 2` + kayıt alanı |
| T8 | **Medyan tanımsızdı** — DNF varken hangi medyan? | `dnf-counts-as-cap`: bir DNF medyanı iyileştiremez |
| T9 | Cevap biçimi hiçbir yerde tanımlı değildi | `answerFormat` + `answerNormalization`, sözleşme sayfasında basılı |
| T10 | Metne bağlı 19 bulmaca, metne **bağlı değildi** | `boundToTextHash` + `qa_taxonomy § ⑨` |
| T11 | Her kapıda **tek** kapı bulmacası adayı — en kritik bulmacanın yedeği sıfır | Kapı başına ≥2; yedekler `substitutableFor` ile **çapraz aileye** bağlandı |
| T12 | Dokuz ailenin `validationMethod`'u ispat değildi | `answerSpace` şartı kabul edildi — **Faz 2'nin ilk teslimatı** |
| T13 | `classification` analizle tekilleştirilemez (~5,6 beklenen sahte ayrım) | Aile ancak **basılı nitelik matrisiyle** kullanılabilir; kural taksonomiye yazıldı |
| T14 | `plate-observation` yüklemi öznel; künye çizimden çıkarılıyordu (dairesel) | Kabul edilebilir yüklem listesi + **künye önce, gravür sonra** kuralı |
| T15 | `path-graph` simetrisi risk profilinde vardı, **ispatta yoktu** | Otomorfizma ve yön şartı taksonomiye yazıldı |
| T16 | İpucu alt dize denetimi **ters basımla** atlatılabilir (`HINT_LADDER § 3` ipuçları ters basar) | `qa_hints` dört gizleme biçimini deniyor; kanarya künyesi **ters karmaları** da taşıyor |
| T17 | Ogham/runik: **bilen** okur kitapla çelişebilir | Sözleşmenin **dördüncü sözü** + yalnızca yaygın değerle çakışan glif kuralı |
| T18 | İpucu uzunluk kuralları çelişiyordu (40 kelime vs. "bulmacadan kısa") | Kural "**tek bir ipucu** bulmacadan uzun olamaz" olarak netleşti |

### 3.3 · Kabul edilen ama FAZ 1'DE UYGULANMAYAN — kurucu kararı bekliyor

| # | Bulgu | Neden ertelendi | Karar |
|---|---|---|---|
| T19 | **Bulmaca başına doğrulama** — kapı tamamlama olasılığı p¹⁹; 18/19 çözen okur hangi ikisinin yanlış olduğunu bilemez ve ipucu merdiveni işe yaramaz | Doğrulama sayfası barındırma kararı kurucununn | **A7** |
| T20 | **Pilot levhaların POD provası Faz 2'ye** — 20 pilot bulmacadan 9'u levha taşıyor; ekranda test edilen bir levha bulmacası test edilmemiştir | Prova siparişi kurucununn; yol haritası değişikliği | **A9** |
| T21 | **Faz 3'e ikinci öldürme kapısı** — en yüksek riskli üç aile Kapı I'de **yok**; en sert test en güvenli bulmacalara uygulanıyor | Yol haritası değişikliği | **A10** |
| T22 | Sayfa hedefi 208 → 230 (telif 9,85 $ → 9,58 $) | Ticari etki | **A8** |

### 3.4 · Reddedilen

| Bulgu | Neden reddedildi |
|---|---|
| "Yol haritası gövde sayfasında 68 sayfalık çelişki var" | Yanlış okuma: yol haritası Faz 4 § 6'daki *~102 gövde* o fazın **artışıdır**, toplam değil. Gerçek tutarsızlık arka maddedeydi (T2) ve düzeltildi |
| "`classification` ailesi silinsin" | Kapı II'nin teması ve portföy içi çapraz satışın taşıyıcısı. Silmek yerine **ispatlanabilir** hâle getirildi (T13) |

---

## 4 · Kapatılmayan bir şey: taramanın sınırı

`validate_structure` alan **adı** ve **etiket** arar. `qa_solution_leak`
kanaryası cevabın **kendisini** arar — ama yalnızca korumalı katman
yerelde varken veya CI'da tuz kuruluyken.

> **Etiketsiz düz proza içinde, tuz kurulu değilken yazılmış bir cevap
> yakalanmaz.**

Bu sınır burada yazılıdır çünkü bir kapının ne **yapmadığını** bilmemek,
onu olduğundan güçlü sanmaktır. Kapatılması `ENIGMATICA_CANARY_SALT`
CI sırrının kurulmasına bağlıdır (**A11**).
