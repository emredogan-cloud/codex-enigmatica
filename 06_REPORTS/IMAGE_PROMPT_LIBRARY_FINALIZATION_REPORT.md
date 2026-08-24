# GÖRSEL PROMPT KÜTÜPHANESİ · SONLANDIRMA RAPORU

**Tarih:** 24 Ağustos 2026 · **Kapı seviyesi:** `phase5`
**Üreteç:** `04_BUILD/plate_prompts.py` + `04_BUILD/prompt_catalog.py`
**Çıktı:** `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` (429 KB · 4.008 satır)

> Bu rapor bir görselin üretildiğini **iddia etmez**. `07_ASSETS/raw/`
> boştur. Bu belge yalnızca *ne üretileceğini* söyleyen dosyanın
> yeniden inşa edildiğini ve ölçülerek doğrulandığını bildirir.

---

## 1 · Önceki durum

| | eski | yeni |
|---|---|---|
| bayt | 92.955 | 428.944 |
| satır | 1.192 | 4.008 |
| kart | 103 | **111** |
| kopya düğmesi | **0** | **223** |
| gezinilebilir bölüm | **0** | **8** |
| katlanır blok | 0 | 102 |

Eski kütüphane doğruydu ama **kullanılamazdı**: tek bir uzun akış,
gezinme yok, kopyalanabilir prompt bloğu yok. Kurucu her prompt için
metni elle seçmek zorundaydı — 103 kez. Eksik olan veri değil,
**belgenin bir araç olarak çalışmasıydı.**

## 2 · Yeni yapı

Sekiz bölüm, yapışkan gezinme çubuğuyla:

`1 Durum` · `2 Ortak görsel üslup` · `3 Ortak olumsuz kısıtlar` ·
`4 Üretim ve dosya adlandırma` · `5 Gravür promptları (103)` ·
`6 Kapak promptları (2)` · `7 A+ modülleri (6)` · `8 Teslim listesi`

Tek dosya · CSS ve JS gömülü · dış bağ, CDN ya da uzak yazı tipi
**yok** — çevrimdışı açılır. Bu bir denetimle zorlanır.

## 3 · ⭑ 103 GRAVÜR PROMPTU KORUNDU — ÖLÇÜLDÜ ⭑

Sunum değişti; **veri değişmedi**. Bu iddia edilmedi, kanıtlandı:
eski kütüphane `git show HEAD:` ile çıkarıldı, iki dosyanın
`⭑ VERİ — DEĞİŞTİRİLEMEZ ⭑` blokları ayrıştırıldı ve karşılaştırıldı.

```
eski kart: 103 · yeni gravür kartı: 103
kayıp kart: yok
VERİ FARKI: 0
```

İki bilinçli fark, karşılaştırmada normalleştirildi ve burada açıkça
bildirilir:

1. **Tekil ifade.** `exactly 1 of mark '◆' — countable, evenly
   spaced…` → `exactly ONE mark '◆' — a single, clearly separate
   incision`. Sayı aynıdır; "evenly spaced" tek bir işaret için
   anlamsız bir yönergeydi.
2. **Dokuz kimlik yeniden sınıflandırıldı** — `VISUAL_ARCHITECTURE.md
   § 2` kuralına uydurmak için, hiçbiri bulmacaya bağlı değil:
   `pl-front-01/02` → `dc-`, `pl-front-03` → `tl-`,
   `pl-gate-1..5` → `dc-`, `pl-meta-02` → `dc-`.

Sonuç dağılım: **94 `pl-`** (bulmaca verisi · dokunulmadı) · 8 `dc-`
(süs) · 1 `tl-` (araç).

## 4 · Kapak promptları (2)

| kimlik | konsept | dayanak |
|---|---|---|
| `cover-option-01` | BİLGİNİN MASASI | BRIEF § 4.3 · § 4.1 |
| `cover-option-02` | BÜYÜK BULMACA ARŞİVİ | BRIEF § 6.3 · § 6.1 |

6 × 9 in · 2 : 3 · 1800 × 2700 px · 300 dpi · RGB. Her kart ÜST %22
ve ALT %15 için **metin-güvenli alan** tanımlar.

**Sırt ölçüsü YOKTUR ve olamaz.** Sırt genişliği sayfa sayısından
türer, iç blok henüz dondurulmadı (K12). Kartlar **yalnızca ön kapak
sanatı** ister; sarmal kapak sonradan kurulur.

## 5 · A+ modülleri (6)

| kimlik | modül | Amazon türü · ölçü |
|---|---|---|
| `aplus-01` | CODEX ENIGMATICA'NIN DÜNYASI | Standard Image & Text Overlay · 1940 × 600 |
| `aplus-02` | BİR BULMACANIN ANATOMİSİ | Standard Single Image & Sidebar · 600 × 600 |
| `aplus-03` | KEŞİF DENEYİMİ | Standard Single Left Image · 600 × 600 |
| `aplus-04` | GÖZLEMDEN ÇIKARIMA | Standard Single Image & Sidebar · 600 × 600 |
| `aplus-05` | KAPILARDAN GEÇEN YOLCULUK | Standard Image Header with Text · 1940 × 600 |
| `aplus-06` | SON AÇILIŞ | Standard Image & Text Overlay · 1940 × 600 |

Ölçüler **hafızadan uydurulmadı**; portföyün üretim şartnamesinden
alındı. Deponun kendi A+ şartnamesi yoktur (`aplus.py` bir Faz 6
teslimidir) — bu rapor o boşluğu doldurmaz, işaret eder.

Sekiz ticari kartın **hepsi** bir `BRIEF §` dayanağı taşır. Bu bir
denetimle zorlanır: dayanaksız bir kart eklenemez.

**Bütün görseller metinsizdir.** Başlık ve gövde Amazon'un kendi
alanıdır; modüle metin çizmek onu iki kez basar.

## 6 · Dosya konumları

Yeni dizin **icat edilmedi**; deponun kendi kuralı kullanıldı:

| aşama | konum |
|---|---|
| ham üretim | `07_ASSETS/raw/` |
| işlenmiş levha | `07_ASSETS/plates/` |
| nihai kapak | `03_COVER/` |
| nihai A+ | `03_APLUS/` |

## 7 · Kopya düğmeleri — tarayıcıda ölçüldü

Kütüphane yerel bir sunucuda açıldı, `navigator.clipboard.writeText`
yakalandı ve **223 düğmenin hepsi tıklandı**:

```
düğme 223 · hedefsiz 0 · panoya yazmayan 0 · yanlış metin kopyalayan 0
```

Ayrıca: 8 gezinme çıpasının hepsi çözülüyor · 102 katlanır bloğun
hepsi açılıyor · düğme geribildirimi çalışıyor (`kopyala → kopyalandı`)
· yatay taşma yok · **konsol temiz** (sıfır hata).

## 8 · Üreteç bütünlüğü

`.html` **elle düzenlenmedi.** Değişiklikler üretece yazıldı; belge
`plate_prompts.py` tarafından basılır ve "üretilen belgeler güncel"
kapısı bunu her CI koşusunda zorlar.

Ticari promptlar ayrı bir dosyada (`prompt_catalog.py`) durur: gravür
promptları bulmaca geometrisinden **ölçülür**, kapak ve A+ promptları
ise `BRIEF.md`'den gelen **ticari kararlardır**. İkisini aynı dosyada
tutmak, ölçülen bir sayının bir pazarlama tercihiyle karıştırılması
riskini doğururdu.

## 9 · Doğrulama

`04_BUILD/qa_all.sh` — **bütün kapılar yeşil** · kapı seviyesi
`phase5`. Üreteç kendi çıktısını denetler: **23 denetim yeşil**
(tazelik denetimi dâhil).

Üretilen HTML'e karşı çalışan yeni denetimler:

- hiçbir HTML kimliği iki kez kullanılmıyor *(kopya kimlik = yanlış
  metni kopyalayan düğme)*
- her kopya düğmesinin bir hedefi var · her prompt kutusunun bir
  düğmesi var · her iç çıpa çözülüyor
- `<article> <details> <table> <nav> <script> <style>` dengeli
- HTML iskeleti tam · **çevrimdışı çalışır**
- **sır sızıntısı yok** (anahtar · jeton · parola · `CANARY_SALT`)
- her dosya adı küçük harf-tire kalıbında
- 2 kapak · 6 A+ · geçerli Amazon modül türü · her kart bir `BRIEF`
  dayanağı taşıyor

### 9.1 · Doğrulama sırasında bulunan boşluk — kapatıldı

CI yeşildi ama **kütüphaneyi denetlemiyordu.** `plate_prompts.py` yalnızca
`qa_all.sh` içinden, yani yerel makinede çalışıyordu; `.github/workflows/`
onu hiç çağırmıyordu. Sonuç: elle düzenlenmiş ya da bayat bir kütüphane
CI'dan **yeşil geçerdi** — ve dosya doğru *görüneceği* için kimse fark
etmezdi.

Daha kötüsü, üretecin `--check` bayrağı kabul ediliyor ama **hiçbir şey
yapmıyordu**: her koşuda dosyayı yeniden yazıyordu. Hiçbir şey yapmayan
bir bayrak, olmayan bir bayraktan daha kötüdür — çünkü korunduğunuzu
sanırsınız.

İkisi de kapatıldı:

- `--check` artık **yazmaz, karşılaştırır**: üreteç HTML'i belleğe basar
  ve diskteki dosyayla eşitliğini denetler. CI'nın çalışma ağacı temiz
  kalır.
- Kapı CI'ya eklendi (`depo, belge ve manuscript koruması` işi).

Sonra ikinci bir boşluk çıktı: kapı CI'da koştu ama **hiçbir şey
denetlemedi** — `0 denetim yeşil · manuscript yok`. `02_MANUSCRIPT/`
bilerek takip edilmez (korunan katman), bu yüzden CI kütüphaneyi
yeniden üretemez ve tazelik karşılaştırması orada **koşamaz**. Bu bir
hata değil, mimarinin sonucudur — ama hiçbir şey yapmadan yeşil dönen
bir adım, korunduğunuzu sanmanızdır.

Denetimler ikiye ayrıldı:

- **Manuscript gerektiren** (yeniden üret + karşılaştır) — yerelde.
- **Takip edilen HTML'i okuyan** (kopya kimlik · hedefsiz düğme ·
  düğmesiz kutu · kırık çıpa · dengesiz etiket · dış bağ · sır ·
  dosya adı) — bunlar bulmacaları gerektirmez ve **CI'da koşar**.

CI ortamında artık **0 değil 14 denetim** çalışır.

Kapının **ısırdığı ölçüldü**: kütüphanedeki tek bir rakam elle
değiştirildi (`exactly 5 of mark` → `exactly 9`), üreteç bunu yakaladı
ve **çıkış kodu 1** verdi; dosya geri alınınca 0'a döndü.

Manuscript'siz (CI) kipte de yedi bozuk fikstür denendi — kırık çıpa,
hedefsiz düğme, kopya kimlik, dengesiz etiket, CDN bağı, `api_key`
ve sağlam dosya: **altısı da çıkış 1, sağlam olan 0**.

**Cevap sızıntısı:** `qa_solution_leak.py` — 4 denetim yeşil, kip A,
281 cevap dizesi, **109 takip edilen dosya** (429 KB'lık yeni
kütüphane dâhil), dosya adları ve commit mesajları tarandı.

Yeniden yazım sırasında kanarya **üç gerçek çarpışma yakaladı** ve
metin değiştirildi; biri İngilizce prompt içinde kelime sınırı aşan
bir kesitti ("a sma…"), ikisi Türkçe künye alanlarındaydı. Tarama
prompta giden alanlarla (`concept`, `composition`, `safe`) sınırlandı
— ısınma `lead`/`note` alanlarının dışlanmasıyla aynı K41 gerekçesi.

## 10 · Değişmeyen

Bu iş **hiçbir doğrulama durumunu değiştirmez**:

`externalValidation = founder_override_partial` ·
`sessionsPerformed = 0` · `humanValidationPassed = false` ·
ölçülen öldürme kapısı **HARD-STOP** · `07_ASSETS/raw/` **BOŞ** ·
`06_REPORTS/solver/` **BOŞ**.

**Üretilmiş görsel: 0.** Bu kitabın hiçbir levhası çizilmedi ve
hiçbir insan bu kitabı çözmedi.

## 11 · Durulan yer

Yapılmadı ve **bilerek** yapılmadı: görsel üretimi · nihai kapak
dosyaları · kapak tipografisi · KDP sarmal kapağı · A+ paketleri.

Bunlar kurucuya aittir. Kütüphane, o iş başladığında kopyalanmaya
hazır 111 promptu tutar.
