# 02_MANUSCRIPT — bu dizin neden boş

Bu depo **public**tir. Ama bu projede depoda durmayan **üç katman** vardır
ve ikisi ticari olarak hassastır:

1. **Bulmaca prozası** — `.gitignore § ①`
2. **⭑ ÇÖZÜMLER ⭑** — `.gitignore § ①b`. Bir bulmaca kitabının çözümleri
   **ürünün kendisidir**. Public depoda duran bir çözüm, kitabı
   **yayımlanmadan** değersizleştirir.
3. **İpuçları** — üçüncü kademe cevabı dolaylı verir; çözümle aynı sınıfta.

Ve bu hata **geri alınamaz**: git geçmişine giren bir çözümü silmek,
geçmişi yeniden yazmak demektir — ve o ana kadar klonlamış herkeste kalır.

## Ama kod sır değildir

`04_BUILD/` ve `05_TESTS/` **public**tir ve öyle kalmalıdır. Bir
doğrulayıcının nasıl çalıştığını herkes görebilir; **neyi doğruladığını**
göremez.

## Dört hat

| Hat | Ne yapar |
|---|---|
| `.gitignore` | Yol kalıbıyla dışlar |
| `PROTECTED_DIRS` | Korumalı dizinde takip edilen dosya **varlığını** yakalar |
| `check_solution_leak()` | Takip edilen dosyalarda **çözüm alan adı** arar |
| `validate_spec` | Public indekste yasak alan arar |

Tam mimari: [`../00_CONTEXT/CONTENT_PROTECTION.md`](../00_CONTEXT/CONTENT_PROTECTION.md)
