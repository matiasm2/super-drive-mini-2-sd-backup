#!/usr/bin/env python3
"""
build_zmd.py — Build .zmd files for the Super Drive Mini 2 / SG800 console.

Usage:
    python3 build_zmd.py <rom.md|rom.bin> [--thumb thumbnail.png] [--out output.zmd]

If no thumbnail is given, a solid blue-gray placeholder (matching the
original test.zmd colour) is used.  Requires Pillow only when a thumbnail
image is supplied.

ZMD layout:
    [119 808 bytes]  RGBA thumbnail  (144 × 208 px, 4 bytes/px)
    [variable]       WQW container   (ZIP-like, WQW replaces PK)
"""

import sys, zlib, struct, os
from pathlib import Path

THUMB_W = 144
THUMB_H = 208
THUMB_BYTES = THUMB_W * THUMB_H * 4  # 119 808

# Placeholder colour matching test.zmd: RGBA = (0x48, 0x48, 0x68, 0xFF)
PLACEHOLDER_PIXEL = bytes([0x48, 0x48, 0x68, 0xFF])


def make_thumbnail_rgba(image_path: Path) -> bytes:
    """Convert any image to 144×208 RGBA bytes."""
    from PIL import Image
    img = Image.open(image_path).convert("RGBA").resize(
        (THUMB_W, THUMB_H), Image.LANCZOS
    )
    return img.tobytes()  # raw RGBA, row-major


def placeholder_thumbnail() -> bytes:
    return PLACEHOLDER_PIXEL * (THUMB_W * THUMB_H)


# Scrambled 21-byte filename copied from test.zmd.
# The firmware doesn't display this; it's an internal WQW field.
_SCRAMBLED_FNAME = bytes.fromhex("d6c5ab8c8b8f8496c5ae8c868ec5a784868ecba8a1")


def _ntfs_extra(mtime_ns: int) -> bytes:
    """Build a 36-byte NTFS timestamp extra field (ZIP header ID 0x000A)."""
    # Windows FILETIME = 100-ns intervals since 1601-01-01
    # Python time.time_ns() is since 1970-01-01; offset = 116 444 736 000 000 000 ns
    offset_100ns = 116_444_736_000_000_000
    ft = mtime_ns // 100 + offset_100ns
    tag = struct.pack("<HH", 0x000A, 32)        # header ID, data size
    reserved = struct.pack("<I", 0)
    attr_tag = struct.pack("<HH", 1, 24)        # attr tag 1 = NTFS times, size 24
    times = struct.pack("<QQQ", ft, ft, ft)     # mtime, atime, ctime (same)
    return tag + reserved + attr_tag + times    # 4 + 4 + 4 + 24 = 36 bytes


def build_wqw(rom: bytes, fname: bytes = _SCRAMBLED_FNAME) -> bytes:
    """Wrap ROM bytes in a WQW container (ZIP-equivalent with WQW magic)."""
    import time

    comp_data = zlib.compress(rom, level=9)[2:-4]   # strip 2-byte zlib header + 4-byte adler32
    crc32     = zlib.crc32(rom) & 0xFFFFFFFF
    comp_sz   = len(comp_data)
    uncomp_sz = len(rom)
    fname_len = len(fname)

    # DOS timestamp for "now"
    t = time.localtime()
    dos_time = (t.tm_sec // 2) | (t.tm_min << 5) | (t.tm_hour << 11)
    dos_date = t.tm_mday | (t.tm_mon << 5) | ((t.tm_year - 1980) << 9)
    mtime_ns = int(time.time() * 1e9)
    ntfs_extra = _ntfs_extra(mtime_ns)
    extra_len  = len(ntfs_extra)  # 36

    # --- WQW\x03 local file header ---
    lf = struct.pack(
        "<4sHHHHHIIIHH",
        b"WQW\x03",
        20,          # version needed
        0,           # flags
        8,           # compression = DEFLATE
        dos_time,
        dos_date,
        crc32,
        comp_sz,
        uncomp_sz,
        fname_len,
        0,           # extra field length (none in local header)
    ) + fname

    # --- compressed data ---
    data_block = comp_data

    # --- WQW\x02 central directory header ---
    lf_offset = 0   # local header starts at offset 0 in the payload
    cd = struct.pack(
        "<4sHHHHHHIIIHHHHHII",
        b"WQW\x02",
        0x001F,      # version made by (3.1, MS-DOS)
        20,          # version needed
        0,           # flags
        8,           # compression
        dos_time,
        dos_date,
        crc32,
        comp_sz,
        uncomp_sz,
        fname_len,
        extra_len,   # 36 (NTFS timestamps)
        0,           # comment length
        0,           # disk number start
        0,           # internal file attributes
        32,          # external file attributes (= FILE_ATTRIBUTE_ARCHIVE)
        lf_offset,
    ) + fname + ntfs_extra

    cd_offset = len(lf) + len(data_block)
    cd_size   = len(cd)

    # --- WQW\x01 end of central directory ---
    eocd = struct.pack(
        "<4sHHHHIIH",
        b"WQW\x01",
        0,       # disk number
        0,       # disk with start of CD
        1,       # entries on this disk
        1,       # total entries
        cd_size,
        cd_offset,
        0,       # comment length
    )

    return lf + data_block + cd + eocd


def build_zmd(rom_path: Path, thumb_path: Path | None, out_path: Path) -> None:
    rom = rom_path.read_bytes()
    if not rom:
        raise ValueError("ROM file is empty")

    if thumb_path:
        thumb = make_thumbnail_rgba(thumb_path)
        if len(thumb) != THUMB_BYTES:
            raise ValueError(f"Thumbnail must be {THUMB_BYTES} bytes after conversion")
    else:
        thumb = placeholder_thumbnail()

    wqw = build_wqw(rom)
    out_path.write_bytes(thumb + wqw)
    print(f"Written {out_path}  ({len(thumb) + len(wqw):,} bytes)")
    print(f"  Thumbnail : {THUMB_W}×{THUMB_H} RGBA  ({len(thumb):,} bytes)")
    print(f"  ROM       : {len(rom):,} bytes uncompressed")
    print(f"  WQW       : {len(wqw):,} bytes")


def main():
    import argparse
    p = argparse.ArgumentParser(description="Build .zmd for Super Drive Mini 2 / SG800")
    p.add_argument("rom", help="ROM file (.md / .bin / .nes)")
    p.add_argument("--thumb", metavar="IMG", help="Thumbnail image (any format Pillow reads)")
    p.add_argument("--out",   metavar="OUT", help="Output .zmd path (default: <rom>.zmd)")
    args = p.parse_args()

    rom_path = Path(args.rom)
    if not rom_path.exists():
        sys.exit(f"ROM not found: {rom_path}")

    thumb_path = Path(args.thumb) if args.thumb else None
    if thumb_path and not thumb_path.exists():
        sys.exit(f"Thumbnail not found: {thumb_path}")

    out_path = Path(args.out) if args.out else rom_path.with_suffix(".zmd")
    build_zmd(rom_path, thumb_path, out_path)


if __name__ == "__main__":
    main()
