# Asset Upscaling Raporu — AI 4x Görsel Yükseltme + DPI Standardizasyonu

> **Tarih:** 2026-08-18
> **Kim yaptı:** Claude Code (Sonnet 5) — tek bir sohbet oturumu içinde
> **Bu dosya neden var:** Aşağıdaki işlemleri tekrarlaması muhtemel *sonraki bir ajan*
> (insan ya da AI fark etmez) aracı sıfırdan keşfetmesin, AppImage'i tekrar
> çıkarmasın, yanlış model/komut seçip zaman kaybetmesin diye. Bu dosyanın aynı
> kopyası, bu depodaki (`MY-DİGİTAL-BOOK`) 6 KDP projesinin de ana dizinine
> konuldu (bkz. §8), çünkü hangi proje klasöründen çalışılırsa çalışılsın aynı
> kurulu araç kullanılacak.

---

## 1. Özet

Bu oturumda iki farklı iş yapıldı:

1. **Kurulum:** `upscayl-2.15.0-linux.AppImage` masaüstüne düzgün şekilde
   kuruldu (GUI + masaüstü menüsü entegrasyonu) ve içinden, ekran/GUI
   gerektirmeyen bir **komut satırı yükseltme motoru** çıkarılıp kalıcı bir
   konuma kopyalandı.
2. **Toplu işlem:** Kullanıcının "DPI yükseltme" isteği netleştirildi (bkz.
   §3.1) ve 11 kapak/görsel dosyası, 3 farklı KDP projesinde, gerçek AI
   upscaling ile **4 kat büyütülüp** her birine **300 DPI** metadata etiketi
   yazıldı. Orijinal dosyaların hiçbirine dokunulmadı; sonuçlar
   `-4x-300dpi` ekli yeni dosyalar olarak aynı klasörlere kaydedildi.

Toplam: **11 dosya**, 3 proje (`THE-MYTH-HUNTERS-FIELD-BOOK`,
`CODEX_BESTIARIUM`, `THE-GREAT-BOOK-OF-WORLD-MYTHS`, `CODEX_MYTHOLOGICA` —
4 proje), sıfır hata, orijinaller korunmuş durumda.

---

## 2. Kurulan Araçlar ve Konumları

### 2.1 Upscayl GUI uygulaması
- İkili: `~/Applications/upscayl-2.15.0-linux.AppImage` (çalıştırılabilir)
- Masaüstü kısayolu: `~/.local/share/applications/upscayl.desktop`
- İkon: `~/.local/share/icons/hicolor/512x512/apps/upscayl.png`
- GNOME uygulama menüsünden "Upscayl" araması ile açılabilir.

### 2.2 Upscayl CLI motoru (asıl kullanılan, önemli olan bu)
Upscayl'ın GUI'si aslında arka planda saf bir komut satırı ikili programı
çağırıyor. Bu ikili, `--appimage-extract` ile AppImage'in içinden çıkarılıp
**kalıcı ve bağımsız** bir konuma kopyalandı, böylece her seferinde AppImage'i
extract etmeye gerek kalmıyor:

```
~/Applications/upscayl-cli/
├── upscayl-bin          # Real-ESRGAN ncnn-vulkan tabanlı yükseltme motoru
└── models/               # 7 önceden eğitilmiş AI modeli (.bin + .param çiftleri)
    ├── upscayl-standard-4x   ← bu oturumda kullanılan model
    ├── upscayl-lite-4x
    ├── high-fidelity-4x
    ├── ultrasharp-4x
    ├── ultramix-balanced-4x
    ├── digital-art-4x
    └── remacri-4x
```

Bu ikili **Electron/GUI/ekran gerektirmez**, tamamen headless çalışır — bir
sunucuda veya bu ortamda olduğu gibi ekransız bir oturumda bile sorunsuz
çalışır. Vulkan API üzerinden GPU'ya erişir.

### 2.3 Donanım / bağımlılıklar
- GPU: **NVIDIA GeForce GTX 1660 Ti** (Vulkan sürücü 580.159.3.0) — `-g 0`
  ile açıkça seçildi.
- Yedek: `llvmpipe` (yazılım/CPU tabanlı Vulkan render) sistemde mevcut ama
  **çok daha yavaş**; GPU'suz ortamda otomatik devreye girer.
- `libvulkan.so.1` ve ilgili sürücüler sistemde zaten kuruluydu, ek kurulum
  gerekmedi.

### 2.4 Yardımcı araçlar (metadata için)
- **ImageMagick** (`convert`, `identify`) — sistemde zaten kuruluydu, boyut/
  format doğrulama için kullanıldı.
- **Python 3 + Pillow** (`from PIL import Image`) — sistemde zaten kuruluydu,
  DPI metadata'sını PNG `pHYs` chunk'ına **kuşkuya yer bırakmayacak şekilde**
  (inç-bazlı) yazmak için kullanıldı. ImageMagick'in `-density`/`-units`
  bayrakları bu sistemde PNG çıktısında etiketi "PixelsPerCentimeter" olarak
  raporluyor (değer matematiksel olarak doğru olsa da — 118.11 px/cm =
  tam 300 px/inç — kafa karıştırıcı olabiliyor); Pillow ile yazınca etiket
  doğrudan ve net biçimde `(300, 300)` DPI olarak kayıtlı oluyor.

---

## 3. Yöntem / Teknik Detaylar

### 3.1 "DPI yükseltme" ne anlama geliyor — kritik ayrım

Kullanıcıya bu netleştirildi çünkü ikisi çok farklı sonuç verir:

| Yaklaşım | Ne olur | Kullanıldı mı |
|---|---|---|
| **Sadece metadata etiketini değiştir** | Piksel sayısı **aynı kalır**, dosyaya "bu 300 DPI'dır" yazılır. Görsel kalitesi hiç değişmez. | ❌ Hayır |
| **AI ile gerçek çözünürlüğü artır** | Piksel sayısı gerçekten artar (ör. 4 kat), AI eksik detayı tahmin ederek doldurur, görsel gerçekten daha büyük/net olur. | ✅ Evet |

Kullanıcı ikinciyi seçti. Bu yüzden pipeline **iki adımlı**:

### 3.2 İşlem hattı (pipeline)

```
girdi.png (ör. 1536×1024)
    │
    ▼
[1] upscayl-bin --n upscayl-standard-4x -s 4 -g 0
    → AI gerçek piksel sayısını 4× artırır (her kenar ×4 → toplam alan ×16)
    → çıktı: girdi-4x-300dpi.png (ör. 6144×4096)
    │
    ▼
[2] Python Pillow: im.save(path, dpi=(300, 300))
    → PNG pHYs metadata'sına 300×300 DPI yazılır (piksel SAYISI değişmez,
      sadece "bu görsel 300 DPI'da yorumlanmalı" bilgisi eklenir)
    │
    ▼
girdi-4x-300dpi.png  (aynı klasöre, orijinal dosya dokunulmadan)
```

300 DPI etiketi artık **fiziksel olarak da gerçek**: piksel sayısı gerçekten
arttığı için, ör. 6144×4096 px görsel 300 DPI'da ≈ 20.5"×13.7" basılabilir —
KDP'nin herhangi bir kapak trim boyutu için fazlasıyla yeterli.

### 3.3 Model seçimi

Bu oturumda **tüm dosyalar için `upscayl-standard-4x`** kullanıldı (genel
amaçlı, dengeli model). Bu bilinçli bir basitleştirme: tutarlılık için tek
model tercih edildi. İçerik türüne göre daha iyi sonuç verebilecek
alternatifler için bkz. §6.4.

---

## 4. Kullanılan Tam Komutlar

### 4.1 Tek dosya — tam pipeline (kopyala-yapıştır şablonu)

```bash
UPSCAYL=~/Applications/upscayl-cli/upscayl-bin
IN="/tam/yol/girdi.png"
OUT="/tam/yol/girdi-4x-300dpi.png"

# 1) AI 4x upscale (GPU 0 = NVIDIA, PNG çıktı)
"$UPSCAYL" -i "$IN" -o "$OUT" -n upscayl-standard-4x -s 4 -g 0 -f png

# 2) 300 DPI metadata etiketi (piksel sayısı değişmez)
python3 -c "
from PIL import Image
im = Image.open('$OUT')
im.save('$OUT', dpi=(300, 300))
"
```

### 4.2 Bu oturumda kullanılan toplu (batch) betik

10 dosyalık ikinci parti için kullanılan tam betik, ileride referans olması
için burada:

```bash
#!/bin/bash
set -e
UPSCAYL=~/Applications/upscayl-cli/upscayl-bin
MODEL=upscayl-standard-4x

process() {
  local IN="$1" OUT="$2"
  "$UPSCAYL" -i "$IN" -o "$OUT" -n "$MODEL" -s 4 -g 0 -f png
  python3 - "$OUT" <<'PYEOF'
import sys
from PIL import Image
p = sys.argv[1]
im = Image.open(p)
im.save(p, dpi=(300, 300))
PYEOF
}

BASE="/home/emre/Downloads/MY-DİGİTAL-BOOK"

process "$BASE/CODEX_BESTIARIUM/03_COVER/artwork/bestiarium-wrap-textless.png" \
        "$BASE/CODEX_BESTIARIUM/03_COVER/artwork/bestiarium-wrap-textless-4x-300dpi.png"

RG="$BASE/THE-GREAT-BOOK-OF-WORLD-MYTHS/07_ASSETS/raw/re-generated"
for name in cover-back-panel cover-front-variant-figures cover-front-variant-object \
            cover-hardcover-wrap cover-paperback-front cover-paperback-wrap \
            cover-thumbnail cover-thumbnail-test; do
  process "$RG/$name.png" "$RG/$name-4x-300dpi.png"
done

process "$BASE/CODEX_MYTHOLOGICA/03_COVER/artwork/paperback-artwork-textless.png" \
        "$BASE/CODEX_MYTHOLOGICA/03_COVER/artwork/paperback-artwork-textless-4x-300dpi.png"
```

Büyük partiler için bu betik arka planda (`run_in_background`) çalıştırıldı;
her dosya ortalama **35-40 saniye** sürdü (GTX 1660 Ti üzerinde).

---

## 5. İşlenen Dosyalar (bu oturumda, tam liste)

| # | Proje | Dosya | Orijinal | Yeni (4x) | Orijinal boyut | Yeni boyut |
|---|---|---|---|---|---|---|
| 1 | THE-MYTH-HUNTERS-FIELD-BOOK | `07_ASSETS/raw/kdp-cover-option-01.png` | 1569×1003 | 6276×4012 | 3.15 MB | 37.25 MB |
| 2 | CODEX_BESTIARIUM | `03_COVER/artwork/bestiarium-wrap-textless.png` | 1536×1024 | 6144×4096 | 2.9 MB | 29 MB |
| 3 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-back-panel.png` | 1023×1537 | 4092×6148 | 2.2 MB | 23 MB |
| 4 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-front-variant-figures.png` | 1023×1537 | 4092×6148 | 3.0 MB | 31 MB |
| 5 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-front-variant-object.png` | 1023×1537 | 4092×6148 | 2.8 MB | 30 MB |
| 6 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-hardcover-wrap.png` | 1465×1073 | 5860×4292 | 2.9 MB | 32 MB |
| 7 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-paperback-front.png` | 1024×1536 | 4096×6144 | 2.7 MB | 29 MB |
| 8 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-paperback-wrap.png` | 1478×1064 | 5912×4256 | 2.8 MB | 31 MB |
| 9 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-thumbnail.png` | 959×1641 | 3836×6564 | 3.1 MB | 33 MB |
| 10 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `.../re-generated/cover-thumbnail-test.png` | 942×1670 | 3768×6680 | 3.1 MB | 32 MB |
| 11 | CODEX_MYTHOLOGICA | `03_COVER/artwork/paperback-artwork-textless.png` | 1472×1069 | 5888×4276 | 2.7 MB | 25 MB |

Hepsinde: model = `upscayl-standard-4x`, ölçek = 4x, DPI = 300×300, format =
PNG, GPU = NVIDIA GTX 1660 Ti (Vulkan). Tüm orijinal dosyalar değiştirilmeden
aynı klasörde duruyor.

---

## 6. Sonraki Ajanlar İçin Rehber — Nasıl Tekrar Kullanılır

### 6.1 Aracı yeniden kurma — GEREK YOK

`~/Applications/upscayl-cli/upscayl-bin` zaten kurulu ve çalışır durumda.
AppImage'i tekrar `--appimage-extract` etmeye, Upscayl'ı tekrar indirmeye
**gerek yok**. Doğrudan §4.1'deki şablonu kullan.

### 6.2 Yeni bir dosyayı işlemeden önce kontrol listesi

1. Dosya adının sonunda zaten `-4x-300dpi` var mı? Varsa **tekrar işleme** —
   üstüne bir daha 4x uygularsan piksel sayısı anlamsız şekilde şişer (16x
   üstüne bir 16x daha) ve kalite düşer, sadece disk israfı olur.
2. Kaynak dosya zaten çok yüksek çözünürlüklü mü (ör. >4000px kenar)? 4x
   uygulamadan önce gerçekten gerekip gerekmediğini düşün — çıktı devasa
   olur (bkz. §7).
3. `~/Applications/upscayl-cli/models/` altındaki model listesine göre en
   uygun modeli seç (§6.4).

### 6.3 Toplu işlem şablonu

§4.2'deki `process()` fonksiyonunu kopyala, `BASE` ve dosya listesini
değiştir. 3'ten fazla dosya işleniyorsa **arka planda çalıştır**
(`run_in_background: true`) ve tamamlanma bildirimini bekle — GUI/terminal
bloklamadan devam edilebilir. Süre tahmini: dosya başına ~35-40 saniye
(1000-1700px kenar uzunluğundaki kaynaklar için, bu GPU'da).

### 6.4 Model seçim rehberi

| Model | Ne zaman kullan |
|---|---|
| `upscayl-standard-4x` | Genel amaçlı, bilinmeyen/karışık içerik (bu oturumda hepsinde kullanıldı) |
| `high-fidelity-4x` | Fotoğraf-gerçekçi içerik, ince detay korunması önemliyse |
| `ultrasharp-4x` | Daha keskin/kontrastlı sonuç isteniyorsa |
| `digital-art-4x` | Çizim/illüstrasyon/boyama tarzı sanat eseri (KDP kapaklarının çoğu muhtemelen bu kategoriye giriyor — ileride karşılaştırmalı test edilebilir) |
| `remacri-4x`, `ultramix-balanced-4x`, `upscayl-lite-4x` | Alternatif/deneysel sonuçlar için |

`-n <model-adı>` bayrağıyla seçilir. `-s` (output-scale) ile 2x/3x/4x
arasında da seçim yapılabilir, `-s 4` varsayılan ve bu oturumda kullanılan
değerdi.

### 6.5 Uyarılar

- **GPU zorunlu değil ama şiddetle önerilir.** `-g 0` verilmezse ya da GPU
  yoksa `llvmpipe` yazılım render'a düşer — çok daha yavaş (dakikalar
  sürebilir).
- **Disk alanı:** 4x upscale dosya boyutunu tipik olarak ~10 kat büyütüyor
  (2-3 MB → 25-37 MB). Çok sayıda dosya işlenecekse önce `df -h` ile boş
  alan kontrol edilmeli.
- **`upscayl-bin` Upscayl'ın resmi/desteklenen bir dış arayüzü değil** —
  GUI'nin arkasında kullandığı dahili ikili. Upscayl güncellenirse
  (`~/Applications/upscayl-2.15.0-linux.AppImage` yeni sürümle değişirse)
  bu ikilinin flag'leri/davranışı değişebilir; şüphe halinde yeni AppImage'i
  `--appimage-extract` edip `resources/bin/` ve `resources/models/` içeriğini
  bu rapordakiyle karşılaştır.
- **Orijinal dosyaya asla yazma.** Her zaman yeni isimle
  (`<orijinal-ad>-4x-300dpi.png`) aynı klasöre kaydet, üstüne yazma.

---

## 7. Sınırlamalar ve Notlar

- **300 DPI etiketi = fiziksel olarak doğru, ama "yeterli mi" sorusu ayrı.**
  Her kapağın gerçek KDP trim boyutuna (ör. 6"×9", 8.5"×11" vb.) göre gerekli
  minimum piksel boyutu değişir. Bu oturumda sadece "4 kat büyüt + 300 DPI
  etiketle" yapıldı; **final KDP yüklemesinden önce her kapağın seçilen trim
  boyutuna göre yeterli olduğu ayrıca doğrulanmalı** (KDP'nin kendi kapak
  hesaplayıcısı/şablonuyla).
- **Dosya boyutları büyük** (23-37 MB). KDP'nin kapak yükleme arayüzü veya
  bu projelerin `04_PRINT`/`04_BUILD` adımlarında kullanılan araçlar dosya
  boyutu sınırı koyuyorsa, yükleme öncesi sıkıştırma/format dönüşümü
  gerekebilir — bu rapor kapsamında yapılmadı.
- **Görsel kalite kontrolü yapılmadı.** AI upscaling bazen özellikle ince
  çizgilerde/metinde/tekrarlayan desenlerde artefakt üretebilir. Bu dosyalar
  otomatik olarak üretildi; **finale gitmeden önce bir insanın veya ayrı bir
  ajanın görsel olarak gözden geçirmesi önerilir.**
- `re-generated` klasöründeki `cover-thumbnail` ve `cover-thumbnail-test`
  dosyalarının basılı/print amaçlı mı yoksa yalnızca web/önizleme amaçlı mı
  olduğu bu oturumda doğrulanmadı; kullanıcı klasördeki tüm kapakları
  kapsayacak şekilde talep ettiği için hepsi işlendi.
- Bu rapor yalnızca **görsel/kapak dosyalarını** kapsar; manüskript metni,
  iç sayfa illüstrasyonları veya diğer varlık türleri bu işlemin kapsamı
  dışındadır.

---

## 8. Bu Raporun Bulunduğu Yerler

Bu dosyanın birebir aynı kopyası, `MY-DİGİTAL-BOOK` altındaki 6 KDP
projesinin (klasör yapısında `00_CONTEXT/01_.../02_MANUSCRIPT/...` şeklindeki
numaralı üretim hattına sahip projeler) ana dizinine kondu:

1. `CODEX_BESTIARIUM/ASSET_UPSCALING_REPORT.md`
2. `CODEX-ENIGMATICA/ASSET_UPSCALING_REPORT.md`
3. `CODEX_MYTHOLOGICA/ASSET_UPSCALING_REPORT.md`
4. `THE-GREAT-BOOK-OF-WORLD-GAMES/ASSET_UPSCALING_REPORT.md`
5. `THE-GREAT-BOOK-OF-WORLD-MYTHS/ASSET_UPSCALING_REPORT.md`
6. `THE-MYTH-HUNTERS-FIELD-BOOK/ASSET_UPSCALING_REPORT.md`

(`CODEX-ENIGMATICA` ve `THE-GREAT-BOOK-OF-WORLD-GAMES` bu oturumda hiç görsel
işlenmedi ama aynı üretim hattı yapısına sahip oldukları için rapor
tutarlılık amacıyla oraya da kondu — ileride bu projelerde de aynı araç
kullanılacaksa referans hazır olsun diye.)
