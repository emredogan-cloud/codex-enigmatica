# CODEX PROJELERİNDEN DERSLER — bu projeye taşınanlar

> Bu proje bütün diğer projelerden **izoledir**. Kod taşınmadı;
> **disiplin** taşındı.
>
> ⚠ *Codex Mythologica* ve *Codex Bestiarium* ile **ad ortaklığı vardır,
> dosya ortaklığı yoktur.* Bu cilt Codex hattının adını taşır ama
> **referans değil oyundur** — bilinçli bir marka genişlemesi (`K3`).

---

## 1 · Taşınan mekanizmalar

| # | Mekanizma | Nereden | Bu projede |
|---|---|---|---|
| 1 | `.gate` faz kapısı | ikisi de | `phase0…release` |
| 2 | Tek doğruluk kaynağı | World Myths | Gömülü sabit değer CI'ı kırmızı yakar |
| 3 | **Kapıların kendi testi** | World Myths | **On altı** kusurlu kurgu |
| 4 | İki hatlı sızıntı koruması | Bestiarium D8/D29 | Burada **dört hatlı** (§ 3) |
| 5 | Ölü muafiyet yasağı | Bestiarium D28 · WM K14 | Muafiyet listesi **sayıca sınırlı** |
| 6 | `run_optional` sözleşmesi | World Myths | Çıkış 2 = ATLANDI |
| 7 | Gravür görsel dili | Bestiarium | **İşlevsel** hâle geldi: levha veri taşır |

---

## 2 · Taşınan dersler

### D1 · Yazar adı üç betikte gömülüydü
World Myths Faz 6'da kapak ile metadata **farklı yazar** taşıyordu.
→ `project_config.json § founder` tek kaynak.

### D2 · Yer tutucu metin KDP tarafından reddedildi
→ `founder.authorBio` null iken Faz 6 kırmızıdır.

### D3 · `--fix` kapıyı sessizce düşürüyordu
→ Kapı yalnızca açıkça verilirse değişir.

### D4 · Muafiyetler sessizce ölüyordu
→ `selftest § ④` her muafiyeti **iki kez** denetler; bu projede ayrıca
muafiyet listesinin **uzunluğunu** da denetler.

### D5 · Bir kapının varlığı, koştuğu anlamına gelmiyordu
→ `qa_all.sh` gelecekteki kapıların satırlarını şimdiden taşır.

### D6 · Yanlış nesneye bağlanmış kusursuz görsel bütün kapılardan geçer
→ Bu projede risk **en yüksektir**: yanlış bulmacaya bağlanmış bir levha,
bulmacayı **çözülemez** yapar. `asset_inventory` ölçümden önce koşar.

### D7 · Bestiarium'un illüstrasyon tutarlılığı dersi burada işlevselleşti
Bestiarium'da 112 levhanın **tek dilde** olması bir estetik başarıydı.
Burada aynı tutarlılık bir **çözülebilirlik şartıdır**: okur levhanın
dilini öğrenir ve şifreyi o dilde arar. Tutarsız bir levha, yanlış bir
ipucudur.

---

## 3 · Bu projenin kendi mekanizması: dört hatlı çözüm koruması

Diğer iki projede iki hat vardır (yol + içerik). Burada dört vardır:

| Hat | Ne yapar | Neden gerekli |
|---|---|---|
| 1 · `.gitignore` | Yol kalıbıyla dışlar | Standart |
| 2 · `PROTECTED_DIRS` | Korumalı dizinde **takip edilen dosya varlığını** yakalar | `.gitignore` bir kez `git add` edilmiş dosyayı durduramaz |
| 3 · `check_solution_leak()` | Takip edilen dosyalarda **çözüm alan adı** arar | Yeni ada konan dosyayı yol kalıbı yakalamaz |
| 4 · `validate_spec` | Public indekste yasak alan arar | Çözüm indekse yazılırsa şema düzeyinde yakalanır |

Gerekçe: bu projede sızıntı **geri alınamaz**. Diğer iki projede sızan
proza telif meselesidir; burada sızan çözüm **ürünü yok eder**.

---

## 4 · Taşınmayanlar

| Taşınmadı | Neden |
|---|---|
| Bestiarium'un `kin_map` sistemi | Burada tasnif ekseni **kapı ve zorluk** |
| World Myths'in `qa_age.py` | Okur yetişkin |
| Ortak Python kütüphanesi | `DECISIONS.md § K1` |

---

## 5 · Bu projenin peşin dersi

> **Bir bulmaca "zekice göründüğü" için kabul edilemez.**

Bestiarium'un dersi *görsel tutarlılıktı*. World Myths'inki *yaş
uygunluğuydu*. Bu projeninki **çözülebilirliktir** — ve ikisinden farklı
olarak, kusuru **okur bulur, siz değil**.

Bu yüzden Faz 2 bir öldürme kapısıdır.
