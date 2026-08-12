# 01_SOURCE/solutions — KORUMALI KATMAN

⛔ **Bu dizindeki hiçbir dosya git tarafından takip edilemez.**

`04_BUILD/validate_structure.py` bu dizini `PROTECTED_DIRS` listesinde
tutar: burada **takip edilen bir dosyanın varlığı** tek başına ihlaldir
ve CI kırmızı yanar. İçeriğine bakılmaz.

Bu dizinde durması gerekenler (yerelde, ayrıca yedeklenmiş):

- `gate-1.json` … `gate-5.json` — çözümler, çözüm yolları
- `hints.json` — üç kademeli ipuçları
- `meta.json` — meta-misterin çözümü

Neden: bir bulmaca kitabının çözümleri **ürünün kendisidir**.

Tam mimari: [`../../00_CONTEXT/CONTENT_PROTECTION.md`](../../00_CONTEXT/CONTENT_PROTECTION.md)
