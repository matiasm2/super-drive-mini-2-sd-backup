# ZMD File Format

Reverse-engineered from `adventure/test.zmd` (June 2023).  
Reference tool: `.utils/build_zmd.py`.

---

## File layout

```
[0 … 119 807]   RGBA thumbnail  — 144 × 208 px, 4 bytes/px (R G B A), alpha = 0xFF
[119 808 …]     WQW container   — ZIP-like, see below
```

Thumbnail size: `144 × 208 × 4 = 119 808 bytes` exactly.  
The pixel order is row-major RGBA; there is no header or footer.

---

## WQW container — ZIP with PK → WQW

WQW is standard ZIP with the two-byte magic `PK` replaced by `WQW` and the third byte acting as a block-type indicator.  The internal field layout is **bit-for-bit identical to ZIP** (little-endian, same offsets, same field widths).

| Block | ZIP magic | WQW magic | Notes |
|-------|-----------|-----------|-------|
| Local file header | `PK\x03\x04` | `WQW\x03` | precedes compressed data |
| Central directory  | `PK\x01\x02` | `WQW\x02` | one entry per ROM |
| End of central dir | `PK\x05\x06` | `WQW\x01` | 22 bytes, points to CD |

Compression method: **raw DEFLATE** (method = 8, no zlib wrapper).

### Offsets inside `test.zmd` payload (payload = file offset 119 808)

| Payload offset | Block | Size |
|----------------|-------|------|
| 0 | `WQW\x03` local header | 51 bytes (4 + 26 fixed + 21 fname + 0 extra) |
| 51 | DEFLATE-compressed ROM | 915 193 bytes |
| 915 244 | `WQW\x02` central directory | 103 bytes (4 + 42 fixed + 21 fname + 36 NTFS extra) |
| 915 347 | `WQW\x01` EOCD | 22 bytes |

### Key values from test.zmd

| Field | Value |
|-------|-------|
| CRC-32 of ROM | `0xE5A24999` |
| Compressed size | 915 193 bytes |
| Uncompressed size | 2 097 152 bytes (2 MB) |
| Filename (internal) | 21 bytes, scrambled (`d6 c5 ab 8c …`) |
| Extra field in CD | 36-byte NTFS timestamp block (header ID `0x000A`) |
| External file attrs | `0x00000020` (FILE_ATTRIBUTE_ARCHIVE) |
| Local header offset | 0 (CD field `relative offset of local header`) |

The internal filename is scrambled with high bytes (≥ 0x80) — the firmware ignores it for display, using the `.zmd` filename instead.

---

## WQW\x03 — Local file header

```
Offset  Size  Field
0       4     Magic: WQW\x03
4       2     Version needed: 0x0014 = 20
6       2     Flags: 0x0000
8       2     Compression: 0x0008 (DEFLATE)
10      2     Last mod time (DOS format)
12      2     Last mod date (DOS format)
14      4     CRC-32 of uncompressed ROM
18      4     Compressed size
22      4     Uncompressed size
26      2     Filename length
28      2     Extra field length (0 in local header)
30      N     Filename (scrambled)
30+N    0     Extra field (none)
30+N    …     DEFLATE data begins here
```

## WQW\x02 — Central directory

Same fields as ZIP central directory (`PK\x01\x02`) with WQW\x02 magic.  
Fixed part is 46 bytes (4 magic + 42 ZIP fields), followed by filename + 36-byte NTFS extra.

## WQW\x01 — End of central directory

```
Offset  Size  Field
0       4     Magic: WQW\x01
4       2     Disk number: 0
6       2     Disk with start of CD: 0
8       2     Entries on this disk: 1
10      2     Total entries: 1
12      4     Size of CD (bytes)
16      4     Offset of CD from payload start
20      2     Comment length: 0
```

---

## Game identified in test.zmd

| Field | Value |
|-------|-------|
| Title | 3 Ninjas Kick Back |
| Publisher | Acclaim (T-113) |
| Release | October 1994 |
| Platform | Sega Genesis / Mega Drive |
| ROM size | 2 MB (2 097 152 bytes) |

---

## Building a .zmd file

See `.utils/build_zmd.py`.

```bash
# Placeholder thumbnail (solid blue-grey, same as test.zmd)
python3 .utils/build_zmd.py game.md --out adventure/game.zmd

# Custom thumbnail (any image; resized to 144×208, requires Pillow)
python3 .utils/build_zmd.py game.md --thumb cover.png --out adventure/game.zmd
```

The script produces a valid WQW container (not a plain ZIP), which is the safe choice
given the firmware may be stricter than the SF2000 (a similar device that accepts plain ZIPs).
