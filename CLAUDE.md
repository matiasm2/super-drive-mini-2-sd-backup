# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This is **not a software project** — it is a raw backup of the SD/TF card from a clone
Sega Genesis/Mega Drive console: the **Super Drive Mini 2** (also sold as **SG800** and other
rebrands). There is no source code, build system, tests, or git history. Work here means
inspecting, identifying, and editing the console's firmware data, UI assets, and game library.

`Resources/` holds the UI assets the menu uses. The console reads those files by their exact
(disguised) names — renaming, reordering, or changing file sizes can brick the boot menu.

## Hardware & where the firmware actually lives

The console is an **emulator-on-chip** clone: a generic (Chinese) SoC that emulates the Mega
Drive 68000/Z80 — there is **no original Sega silicon**. The retail unit advertises HDMI output,
2.4 GHz wireless pads, ~688 built-in games, and a microSD slot.

Important consequence confirmed by byte analysis: **the executable firmware is NOT on this card.**
There is not a single CPU binary in `Resources/` — every file is UI data (RGBA images), the font,
audio, config, or games. The real program (boot menu + emulator) lives in the **SoC's internal
flash**. The card is just a swappable "skin + game library" layer the firmware reads from.

## Card layout

```
/Resources/            firmware + UI assets (see below)
/<category>/            one folder per game category; names come from Foldername.ini
/<category>/save/       game saves / SRAM for that category (empty = no saves yet)
```

The category folders match `Resources/Foldername.ini` exactly: `sport`, `shooting`, `fighting`,
`roms`, `puzzle`, `adventure`. Each holds the playable ROMs for that menu tab plus a `save/`
subfolder. **To add a game, drop its ROM in the matching category folder** — the menu is built
from `Foldername.ini` + whatever ROMs are present.

## Game ROM formats

Multiple formats coexist, confirmed by content:

- **`.zmd`** (sport/shooting/fighting/puzzle/adventure) — the proprietary **Genesis/Mega Drive**
  container. It is **not** a raw `.bin`/`.md`/`.smd` ROM: there is no `SEGA`/`SEGA MEGA DRIVE`
  signature at 0x100 and no readable Genesis header, so it will not load directly in an emulator.
  Layout confirmed by content: `[RGBA cover thumbnail at the front] + [payload in the vendor's
  "WQW" container]`. The trailing payload begins with the **`WQW` magic — the same magic as
  `pcm.asd`** — so `WQW` is the vendor's generic packing/compression format, reused for both audio
  and games. The ROM is therefore not arbitrarily encrypted; it is wrapped in WQW. The titles
  present (e.g. *Gleylancer*, *Aa Harimanada*) are Mega Drive-exclusive, so the payload is genuine
  Genesis game data. Converting a standard Genesis ROM into `.zmd` is unsolved here and needs the
  vendor's WQW packer, not just a rename.
- **`roms/` tab — universal loader** accepting (confirmed):
  - **`.nes`** — standard iNES files (`4E 45 53 1A` "NES\x1a" header)
  - **`.md`** — raw Mega Drive ROMs (unpackaged Genesis binaries)
  - **`.zip`** — compressed ROM archives (ROM + assets bundled)
  
  All tested formats load without conversion. Other formats may be supported but remain untested.
  This tab effectively plays both NES and Genesis titles.

## Critical: file extensions are fake

To obscure the contents, every payload file is given a Windows-system-looking name and extension
(`.nec`, `.dll`, `.sys`, `.cpl`, `.occ`, `.bvs`, `.pal`, `.phl`, `.asd`, `.ocx`, `.gdb`, …).
**These extensions are meaningless** — almost none of the files are what their extension claims.
Always identify a file by its actual byte content (`file`, `xxd`, `strings`), never by its name.

Observed real content types:

- **Raw RGBA bitmap assets** — the majority of `data` files. 4 bytes per pixel (`RR GG BB AA`,
  alpha almost always `0xff`), no header. These are the menu backgrounds, logos, button graphics,
  and other UI imagery. File sizes cluster around reused dimensions (e.g. `1637760`, `491520`,
  `191040`, `32116` bytes — all divisible by 4). They have no embedded width/height, so dimensions
  must be inferred (try common console resolutions) before they can be rendered. There is no image
  tooling installed in this environment; install PIL/ImageMagick/ffmpeg if you need to view them.
- **`bisrv.nec`** — name suggests "BIOS/boot resource", but it is a **boot/splash RGBA image**
  (solid dark fill `0x1C1307` + `0xFF` alpha), not executable code. Misleading name; verify by bytes.
- **`pcm.asd`** — audio payload (boot/UI sound); starts with the **`WQW` magic**, the vendor's
  generic container also used inside every `.zmd` game (see above).
- **`yahei_Arial.ttf`** — the only honestly-named file: the TrueType font used by the menu UI.
- **`Archive.sys`** — 8-byte binary marker/state file.

Note: the files in `Resources/` are firmware/UI only — **none of them are games**. The playable
ROMs live in the category folders described above, not in `Resources/`.

## Menu configuration: `Resources/Foldername.ini`

Plain-text (CRLF) file that drives the on-screen game-category menu. Structure:

- Line 1 (`.zmd`): the ROM/save file extension marker the firmware looks for.
- Following lines: the category folder names shown in the menu, in order
  (`sport`, `shooting`, `fighting`, `roms`, `puzzle`, `adventure`).
- `FFFFFFFF` then a row of `AARRGGBB`/`RRGGBBAA`-style hex words: UI color palette for the menu.
- Trailing integer rows: menu layout parameters (counts, pixel coordinates, and per-item
  index/color tables). Edit these only if you understand the layout math — small changes move or
  recolor menu elements.

## Working in this repo

- There are no commands to build/lint/test. Verification means inspecting bytes and (ideally)
  rendering an asset to confirm a change.
- Treat every file as load-bearing firmware data. Before editing or deleting anything, inspect it
  and preserve its exact size unless you have confirmed the firmware tolerates a different size.
- Keep a backup before modifying any file — there is no version control to undo a mistake.
