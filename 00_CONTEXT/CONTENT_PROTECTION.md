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

## 3 · Mekanizma — BEŞ hat

> ⚠ **Faz 1'de üçten beşe çıktı.** Bağımsız bir saldırı, ilk üç hattın
> yalnızca *alan adı* aradığını gösterdi: `BOOK_STATS.md` içine etiketsiz
> bir cümleyle yazılmış bir cevap **hiçbir kapıya takılmıyordu**.

### Hat 1 · `.gitignore` — YASAK değil İZİN listesi
```
01_SOURCE/solutions/*      01_SOURCE/design/*
09_ARCHIVE/solutions/*     06_REPORTS/solver/*
01_SOURCE/puzzles/*        → yalnızca *.public.json açık
06_REPORTS/*               → yalnızca tracked/ ve faz raporları açık
02_MANUSCRIPT/*
```

⚠ Faz 1'de iki dizin **yasak listesinden izin listesine** çevrildi.
`01_SOURCE/puzzles/` yalnızca iki soneki dışlıyordu — `g1-007.json` hiçbir
yasağa takılmıyordu. `06_REPORTS/` ise takip ediliyor **ve CI artefaktı
olarak yükleniyordu**; `qa_uniqueness` yapısı gereği *reddedilmiş cevap
adaylarını* yazacak bir kapıdır.

### Hat 2 · korumalı dizin denetimi (varlık)
`validate_structure.py § PROTECTED_DIRS` — bu dizinlerde **takip edilen bir
dosyanın varlığı** tek başına ihlaldir. İçeriğe bakılmaz.

Neden ayrı bir hat: `.gitignore` yalnızca *henüz takip edilmeyen* dosyaları
dışlar. Bir dosya bir kez `git add` edilmişse `.gitignore` onu **durduramaz**.

### Hat 3 · içerik taraması (alan adı **ve etiket**)
`validate_structure.py § check_solution_leak()` iki şey arar:

- **alan adı** — `"solution":` biçimindeki JSON anahtarları; kalıplar
  `SOLUTION_FIELD_NAMES` listesinden **türetilir**, elle yazılmaz
- **etiketli değer** — `SOLUTION: …` / `ÇÖZÜM: …` biçimi, **iki dilde**

Faz 1 düzeltmeleri: tarama beş uzantıyla sınırlıydı ve `str.endswith`
büyük/küçük harfe duyarlıydı (`ANSWERS.JSON` geçiyordu); Türkçe hiç yoktu;
ve `git ls-files` çalışmazsa **bütün hat boş koşup yeşil yanıyordu**.

### Hat 4 · şema İZİN listesi
`validate_spec.py` artık `puzzle.schema.json`'u **uygular**.
`publicPuzzle` tanımı `additionalProperties: false` taşır — yani public
indeks bir **yasak listesiyle** değil bir **izin listesiyle** korunur:
akla gelmemiş bir alan adı da reddedilir.

> Faz 1'e kadar bu şemayı **hiçbir kod okumuyordu**. Yalnızca "var mı"
> diye denetleniyordu. 355 satırlık bir doğrulayıcı adı taşıyan tasarım
> belgesiydi.

### Hat 5 · ⭑ KANARYA — cevabın kendisi ⭑
`qa_solution_leak.py` alan adı değil **cevabın kendisini** arar: takip
edilen dosya içerikleri, **dosya adları** ve **commit mesajları**, ve
Faz 6'da yayın paketi.

Üç kipi vardır ve üçüncüsü sessiz kalmaz:

| Kip | Koşul | Davranış |
|---|---|---|
| **A · yerel** | Korumalı katman diskte | Gerçek cevabı arar |
| **B · CI** | Tuzlu künye + `ENIGMATICA_CANARY_SALT` sırrı | Karma pencere eşleşmesi; cevap açıkta durmaz |
| **C · koşmadı** | İkisi de yok | Faz 2'den itibaren **KIRMIZI** |

Künye **ters karmaları** da taşır: ipuçları ters basılır ve ters
basılacak bir dizeyi düz aramak onu kaçırır.

---

## 4 · Muafiyet listesi DONDURULMUŞTUR

`SOLUTION_SCAN_SKIP` **tam olarak iki dosya** içerir ve `selftest § ④`
**küme eşitliği** arar:

| Dosya | Neden muaf |
|---|---|
| `01_SOURCE/puzzle.schema.json` | Alan adlarını **tanımlar**, değer taşımaz |
| `00_CONTEXT/CONTENT_PROTECTION.md` | Bu belge — kalıpları açıklar |

Listeye ekleme yapmak testi düzenlemeyi gerektirir, yani **gözden
geçirilebilir bir eylemdir**.

> ⚠ **Faz 1'de bulunan kusur.** Eski test bir muafiyetin "gerekli"
> olduğunu, muaf dosyada bir çözüm işareti **arayarak** doğruluyordu.
> Yani yeni bir muafiyeti meşrulaştırmanın yolu, o dosyaya bir çözüm
> işareti koymaktı — test, saldırganın kontrol listesiydi. Bir POC bunu
> gösterdi: public indeks muaf listeye alındı ve test `✓ muafiyet
> GEREKLİ` yazdı.

Ve muafiyet **yalnızca alan adı taramasını** kapsar. Değer tarafı
taraması ve kanarya **hiçbir dosyayı** muaf tutmaz — yani bu iki dosyaya
gerçek bir cevap yazmak yine yakalanır.

### Korumalı dizin muafiyetleri TAM YOLDUR

`README.md` ve `.gitkeep` muafiyeti eskiden **temel ada** bakıyordu, yani
her alt dizin bedava bir serbest dosya kazanıyordu:
`01_SOURCE/solutions/gate-1/README.md` bir cevap anahtarı taşıyabiliyordu
ve kapı ona hiç bakmıyordu.

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
