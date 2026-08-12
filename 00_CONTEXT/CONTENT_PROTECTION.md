# İÇERİK KORUMA MİMARİSİ — iki katmanlı gizlilik

> Bu belge bu projenin **varoluşsal** kuralını tanımlar: bir bulmaca
> kitabının çözümleri **ürünün kendisidir** ve public depoya giremez.
>
> Sürüm 1.0 · Faz 1'de onaylanır · Değişiklik kurucu kararı gerektirir

---

## 1 · Neden bu belge var

Diğer iki projede depoda durmayan tek şey **proza**dır. Burada üç şey vardır
ve ikisi ticari olarak hassastır:

| | Risk |
|---|---|
| Bulmaca prozası | Diğer projelerle aynı — telif |
| **Çözümler** | **Ürünü yayımlanmadan değersizleştirir** |
| **İpuçları** | Aynı — çözümü dolaylı verir |

Ve bu hata **geri alınamaz**: git geçmişine giren bir çözümü silmek,
geçmişi yeniden yazmak demektir — ve o ana kadar depoyu klonlamış herkeste
çözüm kalır.

---

## 2 · Ama kod sır değildir

Bu ayrım önemlidir ve talimatın kendisi bunu söyler:

> **KOD / TEST ALTYAPISI public olabilir.
> HASSAS BULMACA İÇERİĞİ ve CEVAPLAR korunmalıdır.**

Bir doğrulayıcının kendisi sır değildir. `qa_solvability.py`'nin nasıl
çalıştığını herkes görebilir; **neyi doğruladığını** göremez.

| PUBLIC | PROTECTED |
|---|---|
| Kod · CI · şema · doğrulayıcı · üretim aracı | **Çözümler** |
| Belgeler · yol haritası · kararlar | **Çözüm yolları** |
| Bulmaca **metadatası** (kimlik, kapı, tip, zorluk, bağımlılık, durum) | **İpuçları (3 kademe)** |
| Bağımlılık grafiği (yapısı, içeriği değil) | **Bulmaca prozası** |
| Ölçüm raporları (çözüm içermeyen) | **Çözücü ham kayıtları** |
| Belirsizlik puanı, test sayısı | Levha ham dosyaları |

---

## 3 · Mekanizma — üç hat

### Hat 1 · `.gitignore` (yol)
```
01_SOURCE/solutions/*
09_ARCHIVE/solutions/*
06_REPORTS/solver/*
01_SOURCE/puzzles/*.private.json
01_SOURCE/puzzles/*.solutions.json
02_MANUSCRIPT/*
```

### Hat 2 · korumalı dizin denetimi (varlık)
`validate_structure.py § PROTECTED_DIRS` — bu dizinlerde **takip edilen bir
dosyanın varlığı** tek başına ihlaldir. İçeriğe bakılmaz.

Neden ayrı bir hat: `.gitignore` yalnızca *henüz takip edilmeyen* dosyaları
dışlar. Bir dosya bir kez `git add` edilmişse `.gitignore` onu **durduramaz**.

### Hat 3 · içerik taraması (alan adı)
`validate_structure.py § check_solution_leak()` — takip edilen bütün
dosyalarda çözüm **alan adlarını** arar:

```
"solution":  ·  "intendedSolution":  ·  "answer":
"answerKey":  ·  "solutionPath":  ·  "hints":
SOLUTION:  ·  ANSWER KEY
```

Neden üçüncü hat: bir çözüm **yeni bir ada konan** bir dosyaya taşınırsa
yol kalıbı onu yakalamaz. Politikayı disipline değil mekanizmaya bağlarız.

### Ve bir dördüncü: şema düzeyi
`validate_spec.py` `puzzle_index.json` içindeki **her kayıt** için yasak
alan adlarını arar. Public indeks çözüm taşıyamaz.

---

## 4 · Muafiyet listesi KISA tutulur

`SOLUTION_SCAN_SKIP` yalnızca dört dosya içerir ve bu sayı
`selftest.py § ④` tarafından **denetlenir**:

```python
rep.check(len(vs.SOLUTION_SCAN_SKIP) <= 4, "muafiyet listesi kısa")
```

Gerekçe: her muafiyet, çözüm sızıntısı kapısında açılmış bir deliktir.
Gereksiz bir tanesi bile fazladır.

Muaf dosyalar ve nedenleri:

| Dosya | Neden muaf |
|---|---|
| `01_SOURCE/puzzle.schema.json` | Alan adlarını **tanımlar**, değer taşımaz |
| `04_BUILD/validate_structure.py` | Tarama kalıplarının kendisini taşır |
| `05_TESTS/selftest.py` | Kurgu çözüm dizesiyle kapıyı test eder |
| `00_CONTEXT/CONTENT_PROTECTION.md` | Bu belge — kalıpları açıklar |

Ve her muafiyet **iki kez** denetlenir: dosya var mı, muafiyet gerçekten
gerekli mi (yani muaf olmasaydı yakalanır mıydı).

---

## 5 · Yayın paketi son taraması (Faz 6)

Faz 6'da `qa_solution_leak.py` **yayın paketini** tarar: `08_OUTPUT/`
içinde bir çözüm dosyası bulunursa CI kırmızı yanar.

Gerekçe: bir çözüm dosyasının yanlışlıkla dağıtım paketine girmesi,
depoya girmesinden **daha kötüdür** — çünkü doğrudan alıcıya ulaşır.

---

## 6 · Çözücü mahremiyeti

Harici çözücülerin adları **hiçbir koşulda** depoya girmez. Kayıtlar
yalnızca anonim kimlik (`solver-01`), kullanılan ipucu sayısı, süre ve
sonuç taşır. Şema bu biçimi `pattern` ile zorunlu kılar.

---

## 7 · Bir çözüm sızarsa ne yapılır

1. **Push etme.** Henüz push edilmediyse `git reset` yeterlidir.
2. Push edildiyse: geçmiş yeniden yazılır (`filter-repo`), depo force-push
   edilir ve **etkilenen bulmacalar yeniden tasarlanır**.
3. Üçüncüsü zorunludur: temizlenen bir çözüm, klonlamış olanlarda kalır.

> Bu prosedürün var olması, onun kullanılmayacağı anlamına gelmez.
> Kullanılmaması için üç hat vardır.
