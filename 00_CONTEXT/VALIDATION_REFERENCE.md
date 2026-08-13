# DOĞRULAMA REFERANSI — hangi kapı neyi ısırır

> Sürüm 1.0 · Faz 1
>
> Yerelde hepsi: `./04_BUILD/qa_all.sh phase1`

---

## 1 · Kapı haritası

| Betik | Neyi denetler | Ne zaman doğdu | Kendi testi |
|---|---|---|---|
| `validate_spec.py` | Config tutarlılığı · **şema uygulaması** · kimlik tekilliği · public katmanda çözüm · **test durumu** · kapsam | Faz 0 → **Faz 1'de yeniden yazıldı** | selftest § ② ③ |
| `validate_structure.py` | Zorunlu dosyalar · gömülü değer · manuscript sızıntısı · sır · **çözüm sızıntısı** · sözleşme senkronu | Faz 0 → **Faz 1'de yeniden yazıldı** | selftest § ⑤ |
| `qa_solution_leak.py` | ⭑ **Cevabın kendisi** — dosya, dosya adı, commit mesajı, yayın paketi | Faz 1 | selftest § ⑥ |
| `qa_dependency.py` | DAG: döngü · ileri referans · kapı sınırı · kapı bulmacası girdisi · meta bağı | Faz 1 | selftest § ④ |
| `qa_taxonomy.py` | Aile tanımı · ölü aile · çeşitlilik · zorluk bandı · künye · levha · **metin karması** · yedek havuz | Faz 1 | selftest § ④ |
| `page_budget.py` | Sayfa modeli · **arka madde türetimi** · levha bütçesi · pilot süre modeli | Faz 1 | selftest § ④ |
| `validate_research.py` | Künye bütünlüğü · ölü künye · haklar · dış bilgi yasağı · doğrulama durumu | Faz 1 | selftest § ④ |
| `qa_solvability.py` | Çözüm yolu · **dış bilgi yasağı** · kısıtlar · belirsizlik tutarlılığı | Faz 1 (kayıt bekliyor) | selftest § ⑦ |
| `qa_uniqueness.py` | ≥3 aday · zorlama gerekçe · **onaylanmış alternatif** · çözücü ikinci cevabı · cevap çakışması | Faz 1 (kayıt bekliyor) | selftest § ⑦ |
| `qa_hints.py` | Üç kademe · **dört gizleme biçimi** · merdiven yükselişi · son adım | Faz 1 (kayıt bekliyor) | selftest § ⑦ |
| `selftest.py` | ⭑ **Kapıların gerçekten ısırdığı** ⭑ | Faz 0 → Faz 1'de genişledi | — |

---

## 2 · "Boş koşan kapı" sözleşmesi

Üç kapı (`qa_solvability`, `qa_uniqueness`, `qa_hints`) korumalı katmanı
okur. Faz 1'de o katman **boştur** — hiçbir bulmaca yazılmadı.

Bu kapılar boşken **sessizce yeşil yanmaz**. Şunu yazarlar:

```
⊘ yazılmış bulmaca yok → ... kapısı denetlenecek kayıt bulamadı
   (bu bir GEÇİŞ DEĞİL, BOŞ KOŞUDUR; Faz 2'de kayıt gelir)
```

Ve yazılmış bir bulmaca **varken** korumalı kaydı yoksa **kırmızı**
yanarlar. Yani boş koşu yalnızca yazılacak bir şey yokken mümkündür.

> Gerekçe: metin yokken yeşil kalan bir hat, **kusur geldiğinde de** yeşil
> kalabilir. Bir kapının çıktısında "denetlenecek şey bulamadım" cümlesi,
> "geçti" cümlesinden farklı olmak zorundadır.

Kanarya (`qa_solution_leak`) aynı sözleşmeyi taşır ve **KİP C · KOŞMADI**
durumunu ayrıca `phase2` ve sonrasında **kırmızı** yakar.

---

## 3 · Dört hatlı çözüm koruması — ve beşincisi

| Hat | Mekanizma | Neyi durdurur |
|---|---|---|
| 1 | `.gitignore` **izin listesi** | Yol kalıbıyla dışlama |
| 2 | `PROTECTED_DIRS` | Korumalı dizinde takip edilen dosyanın **varlığı** |
| 3 | `check_solution_leak` | Takip edilen dosyalarda **alan adı** ve **etiketli değer** |
| 4 | `validate_spec` + **şema izin listesi** | Public indekste tanımsız alan |
| **5** | ⭑ `qa_solution_leak` **kanaryası** ⭑ | **Cevabın kendisi** — dosya, ad, commit mesajı, yayın paketi |

Beşinci hat Faz 1'de eklendi çünkü ilk dördü **alan adı** arıyordu,
**cevap** aramıyordu: etiketsiz bir cümle içine yazılmış bir cevap
dördünden de geçiyordu.

### Kanaryanın üç kipi

| Kip | Koşul | Güç |
|---|---|---|
| **A · yerel** | Korumalı katman diskte | En güçlü; gerçek cevabı arar, yanlış pozitif üretmez |
| **B · CI** | Tuzlu künye + `ENIGMATICA_CANARY_SALT` sırrı | Cevap hiçbir yerde açık durmaz; karma pencere eşleşmesi |
| **C · koşmadı** | İkisi de yok | Faz 2'den itibaren **kırmızı** |

Künye ters karmaları da taşır: ipuçları **ters basılır**
(`HINT_LADDER § 3`) ve ters basılacak bir dizeyi düz aramak onu kaçırır.

---

## 4 · `tested` nasıl kazanılır

Bu durum **elle verilemez**. `validate_spec § check_test_status` şunları
birden arar:

| Şart | Kaynak |
|---|---|
| Kurucu harici çözücüleri **onaylamış** | `founder.externalSolvers.founderConfirmed` |
| Harici çözücü sayısı ≥ kapının şartı (Kapı I: **5**, diğerleri: 2) | `testStatusRequirements` |
| Çözen sayısı ≥ eşik (Kapı I: **4**) | `killGate.passCriteria` |
| Alternatif çözüm analizi **yapılmış** | `alternativeSolutionAnalysisDone` |
| Onaylanmış alternatif çözüm **yok** | `confirmedAlternativeSolutions` |
| Belirsizlik puanı **var ve** ≤ 2 | `ambiguityScore` |

Ve iki bağ:

- `status` ∈ {`validated`, `written`} ⇒ `testStatus` = `tested`
- `testStatus` = `internal-only` ⇒ harici çözücü sayısı **0**

Ayrıca sayaç akıl sağlığı: çözen ≤ deneyen ≤ toplanan havuz. Havuzdan
büyük bir test sayısı bir **uydurma göstergesidir**.

> **Neden bu kadar sert:** Faz 1'e girerken 140 kaydın `status` alanını
> elle `written` yapmak, projeyi `phase1`'den `release`'e kadar
> yürütüyordu — `testStatus` "untested", çözücü sayısı 0, alternatif
> analizi yapılmamışken. Faz 2'ye "öldürme kapısı" deniyordu ama mekanik
> olarak bir **metin alanıydı**.

---

## 5 · Muafiyet politikası

Her muafiyet, kapıda açılmış bir deliktir.

| Liste | Kapsam | Denetim |
|---|---|---|
| `SOLUTION_SCAN_SKIP` | Yalnızca **alan adı** taraması | ⭑ **Tam küme eşitliği** — donduruldu |
| `LEAK_SCAN_SKIP` | Manuscript kalıpları | Canlılık + gereklilik |
| `EMBED_SCAN_SKIP` | Kurucu değeri | Canlılık |
| `PROTECTED_DIR_ALLOW` | **Tam yol**, temel ad değil | selftest fikstürü |

### ⚠ Faz 1'de değişen şey

Eski selftest bir muafiyetin "gerekli" olduğunu, dosyada bir çözüm işareti
**arayarak** doğruluyordu. Yani yeni bir muafiyeti meşrulaştırmanın yolu,
dosyaya bir çözüm işareti koymaktı — test, saldırganın kontrol listesiydi.

Artık liste **dondurulmuştur**: `SOLUTION_SCAN_SKIP` tam olarak iki dosya
içerir ve selftest **küme eşitliği** arar. Listeye ekleme yapmak testi
düzenlemeyi gerektirir, yani gözden geçirilebilir bir eylemdir.

Ve muafiyet **yalnızca alan adı taramasını** kapsar: değer tarafı taraması
ve kanarya **hiçbir dosyayı** muaf tutmaz.

---

## 6 · Kapı sırası ve maliyeti

`qa_all.sh` bütün kapıları saniyeler içinde koşar. Üçüncü taraf paket
kullanılmaz (K7): yazım fazlarında günde onlarca push olur ve iki
dakikalık bir kurulum beklemek disiplini öldürür.

Ağır bağımlılık isteyen kapılar (`qa_plate_readability`, dizgi) `run_optional`
sözleşmesiyle koşar: **çıkış 2 = ATLANDI**, ve bu bir kalite düşüşü değildir.

---

## 7 · Bir kapı eklerken

1. Betik `04_BUILD/` altına, `--verbose --json` arayüzüyle
2. `qa_all.sh`'e satırı **şimdi** eklenir (varlık denetimiyle korunur)
3. `validate.yml`'nin ilgili işine adı eklenir
4. ⭑ `selftest.py`'ye **en az bir kusurlu fikstür** ⭑
5. Bu tablo güncellenir

> **4 atlanırsa kapı yoktur.** Bir kapının varlığı, kusuru yakaladığı
> anlamına gelmez — ve yakalamadığını yalnızca kusurlu bir fikstür
> gösterir.
