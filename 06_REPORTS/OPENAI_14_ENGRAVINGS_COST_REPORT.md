# OPENAI HARCAMA RAPORU — 14 düzeltilmiş gravür

**Tarih:** 25 Ağustos 2026 · **Model:** `gpt-image-1` · 1024×1024 · high

| | |
|---|---|
| Yetkilendirilen hedef | **3,00 $** |
| Sert tavan | **4,00 $** |
| **Gerçekleşen toplam** | **0,5049 $** |
| API çağrısı | **3** |
| Hedefin altında mı | ✅ evet (%17'si kullanıldı) |
| Tavana yaklaşıldı mı | ❌ hayır (%12,6) |

## 1 · Neden 14 değil 3 çağrı

Plan 14 görsel × ~0,175 $ = 2,45 $ idi. Üç çağrı yapıldı ve **hat orada
durduruldu** — çünkü model işi yapamıyordu.

Aynı levha (`pl-g3-03`, sözleşme **7 istasyon**) üç kez üretildi:

| # | Değişiklik | Sonuç | Maliyet |
|---|---|---|---|
| 1 | özgün prompt | **8 istasyon** · üstelik 3B perspektif halka | 0,1681 $ |
| 2 | sahne "düz halka diyagramı"na çevrildi | **12 istasyon** (üslup düzeldi) | 0,1683 $ |
| 3 | sayı listeden çıkarılıp İLK cümleye taşındı | **12 istasyon** | 0,1685 $ |

Üslup her adımda düzeldi. **Sayı hiç düzelmedi.**

> ⚠ Yönerge açıkça "no unnecessary retries" ve "no aesthetic
> experimentation" diyor. Dördüncü bir denemenin yakınsayacağına dair
> hiçbir belirti yoktu; para harcamayı sürdürmek yönergenin kendisine
> aykırı olurdu.

## 2 · Kalan 11 görsel neden API'ye gitmedi

Bu levhalar **saf geometridir**: N eşit kama, bir işaretli istasyon.
Bir gravür bu kitapta süs değil **veridir** — yedi istasyon isteyen bir
bulmacaya on iki istasyonlu halka basmak, çözülemeyen bir bulmaca
basmaktır.

Kod bunu kesin sayar. `04_BUILD/plate_render.py` on dördünü de
deterministik çizdi: **maliyet 0,00 $**, sonuç tartışmasız, sayılar
kütüphaneden (yani bulmacadan) okundu.

**Görsel model sayamıyorsa, sayma işi görsel modele verilmez.**

## 3 · Bütçe koruması

`04_BUILD/engrave_openai.py` içinde, her çağrıdan **önce** ve döngü
**içinde** kontrol edilir:

- harcama defteri **diskte** tutulur (`06_REPORTS/tracked/openai-spend.json`)
  — yeniden koşuda toplam sıfırlanmaz
- maliyet, çağrının **döndürdüğü token sayısıyla** hesaplanır (tahminle
  değil): 4160 çıktı tokeni × 40 $/1M + giriş tokenleri × 5 $/1M
- tahmini toplam tavanı aşacaksa **hiçbir çağrı yapılmaz**
- var olan dosya **asla** yeniden üretilmez (`--force` olmadan)

Fikstürle ölçüldü: defter 3,90 $'a kurulduğunda kapı ısırdı ve
"TAVAN AŞILIR — HİÇBİR ÇAĞRI YAPILMADI" verip çıktı.

## 4 · Güvenlik

- `OPENAI_API_KEY` `.env`den okundu; **ekrana basılmadı**, bu rapora
  yazılmadı, commit edilmedi. `.env` `.gitignore § ⑥`dadır (doğrulandı).
- Harcama defteri **anahtar içermez**: yalnızca levha kimliği, token
  sayısı, maliyet ve süre.
