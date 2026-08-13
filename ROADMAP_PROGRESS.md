# ROADMAP PROGRESS — Codex Enigmatica

<!-- ⚠ ÜRETİLEN BELGE — 04_BUILD/update_docs.py. ELLE DÜZENLEMEYİN. -->

> Kapı: `phase1`

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Bulmaca mimarisi, çözülebilirlik, gizlilik | ✅ **TAMAM** | `phase1` | `faz/1-mimari` | v0.1.0 |
| **2** | ⛔ **ÖLDÜRME KAPISI** — 20 bulmaca + 5 çözücü | ⏸ **SIRADA** | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Kapı II · The Menagerie | ⏸ beklemede | `phase3` | `faz/3-kapi-2` | v0.3.0 |
| **4** | Kapı III–V + meta-mister | ⏸ beklemede | `phase4` | `faz/4-kapi-3-5` | v0.4.0 |
| **5** | Yakınsama + levha + doğrulama sayfası | ⏸ beklemede | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday bulmaca | **151** | ≥130 |
| Mekanizma ailesi | **17** | ≥10 |
| Pilot kohort (Kapı I) | **20** | 20 |
| **Yazılmış taslak** | **20** | — |
| Doğrulanmış bulmaca | **0** | 100 |
| Yazılmış bulmaca (nihai) | **0** | 100 |
| Onaylanmış alternatif çözüm | **0** | **0** |
| İpucu (3 kademe) | **60** | 300 |
| Levha | **0** üretildi / 112 planlandı | ~110 |
| Kelime | **0** | ~34.000 |
| Künye | **16** (0 doğrulanmış) | — |

---

## Sonraki izinli eylem

> ### ⛔ FAZ 2 · ÖLDÜRME KAPISI: **HARD-STOP**
>
> Faz 2'nin ajan tarafından yapılabilir bütün işi **tamamlandı**:
> yirmi Türkçe pilot bulmaca yazıldı, cevap uzayı mimarisi kuruldu ve
> yirmisi de bağımsız olarak doğrulandı, üç yeni kapı eklendi, kanarya
> sırrı kuruldu ve dört senaryoyla kanıtlandı.
>
> **Ama öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz.**
> Harici çözücü oturumu: **0 / 5**.
>
> Kalan tek iş **kurucuya aittir** ve ajan onu yapamaz:
> 1. **A12** — beş harici çözücüyle oturumları yürüt
>    → `00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`
> 2. sonuçları `06_REPORTS/solver/` altına yaz, sayaçları güncelle
> 3. `./04_BUILD/qa_all.sh phase2` koştur ve kararı **oku**
>
> Ayrıca açık: **A9** (levha provası — paket hazır) · **A2** · **A5** · **A7**
>
> Ayrıntı: `DECISIONS.md § AÇIK KARARLAR`
