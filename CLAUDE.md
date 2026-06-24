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

Known hardware (physical inspection, June 2026):
- **RAM:** SK Hynix H5PS1G63EFA — DDR2 SDRAM, **128 MB**
- **Flash:** XMC XM25QE16B — SPI NOR, **2 MB** — this is where the firmware lives
- **SoC:** unidentified QFP, markings covered with epoxy

Important consequence confirmed by byte analysis: **the executable firmware is NOT on this card.**
There is not a single CPU binary in `Resources/` — every file is UI data (RGBA images), the font,
audio, config, or games. The real program (boot menu + emulator) lives in the **2 MB SPI NOR flash
chip** on the PCB. The card is just a swappable "skin + game library" layer the firmware reads from.

**Community tools (SF2000/frogtool) may not apply directly.** The SF2000 (closest known relative)
uses an Ingenic JZ4760B (MIPS32, no HDMI, LPDDR). This device has HDMI and DDR2 → different SoC.
The SD card asset layout (RGBA files, WQW/ZMD format) is very similar, but tool assumptions about
the SoC or firmware structure should be verified before use.

## Card layout

```
/Resources/            UI assets (images, font, audio, config) — see below
/<category>/           one folder per game category; names come from Foldername.ini
/<category>/save/      game saves / SRAM for that category (empty = no saves yet)

/.findings/            RESEARCH NOTES — not part of the SD card backup; safe to edit
/.utils/               HELPER SCRIPTS — not part of the SD card backup; safe to edit
```

The category folders match `Resources/Foldername.ini` exactly: `sport`, `shooting`, `fighting`,
`roms`, `puzzle`, `adventure`. Each holds the playable ROMs for that menu tab plus a `save/`
subfolder. **To add a game, drop its ROM in the matching category folder** — the menu is built
from `Foldername.ini` + whatever ROMs are present.

The `.findings/` and `.utils/` directories were added during reverse-engineering and are **not**
part of the original SD card backup. They will be ignored by the console.

## Game ROM formats

Multiple formats coexist, confirmed by content:

- **`.zmd`** (sport/shooting/fighting/puzzle/adventure) — the proprietary **Genesis/Mega Drive**
  container. Format fully reverse-engineered; see `.findings/zmd-format.md`.
  Layout: `[119 808-byte RGBA thumbnail (144×208 px)] + [WQW container]`.
  The WQW container is ZIP-format with `PK` replaced by `WQW`; compression is raw DEFLATE.
  Use `.utils/build_zmd.py` to pack a standard Genesis ROM into a `.zmd`.
- **`.zfc`** (roms/) — the **Famicom/NES** variant of the same container format. Structure is
  **byte-for-byte identical to `.zmd`**: same 119 808-byte RGBA thumbnail (144×208 px) followed
  by the same WQW container. The only difference is the ROM inside is an iNES (`.nes`) file
  instead of a Mega Drive binary. ZFC = Z + FC (Famicom); ZMD = Z + MD (Mega Drive).
- **`roms/` tab — universal loader** accepting (confirmed working):
  - **`.nes`** — standard iNES files (`4E 45 53 1A` "NES\x1a" header)
  - **`.md`** — raw Mega Drive ROMs (unpackaged Genesis binaries)
  - **`.zip`** — compressed ROM archives containing NES or MD ROMs

  Confirmed NOT working (firmware hangs on "loading" screen):
  - **SNES / `.sfc` / `.smc`** — not emulated; the SoC has no SNES support
  - **Famicom Disk System / `.fds`** — requires FDS BIOS (`diskrom.sys`) absent from firmware
  - **Game Boy / `.gb`** — not emulated
  - **Game Boy Color / `.gbc`** — not emulated
  - **Game Boy Advance / `.gba`** — not emulated

  The ZIP container is recognized and opened by the firmware, but if the content inside
  is an unsupported system the firmware hangs instead of showing an error.
  This console emulates **NES/Famicom and Mega Drive/Genesis only** — no other systems.

## WQW container format (summary)

WQW is ZIP with `PK` replaced by `WQW`. The three block types mirror ZIP exactly:

| Block | WQW magic | ZIP equivalent |
|-------|-----------|----------------|
| Local file header | `WQW\x03` | `PK\x03\x04` |
| Central directory  | `WQW\x02` | `PK\x01\x02` |
| End of central dir | `WQW\x01` | `PK\x05\x06` |

Internal filenames are scrambled (bytes ≥ 0x80); the firmware uses the `.zmd` filename instead.
The same WQW container is used for `pcm.asd` (boot audio) and all `.zmd` game files.

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
  container also used inside every `.zmd` game (see above).
- **`yahei_Arial.ttf`** — the only honestly-named file: the TrueType font used by the menu UI.
- **`Archive.sys`** — 8-byte binary marker/state file.

Note: the files in `Resources/` are firmware/UI only — **none of them are games**. The playable
ROMs live in the category folders described above, not in `Resources/`.

## Menu configuration: `Resources/Foldername.ini`

Plain-text (CRLF) file that drives the on-screen game-category menu. Structure:

- Line 1 (`.zmd`): the ROM/save file extension marker the firmware looks for.
- Following lines: the category folder names shown in the menu, in order
  (`sport`, `shooting`, `fighting`, `roms`, `puzzle`, `adventure`).
- `FFFFFFFF` then a row of `AARRGGBB`/`RRGGBBAA`-style hex words: UI color palette for the menu
  (6 colour values, one per category tab).
- Trailing integer rows: menu layout parameters (counts, pixel coordinates, and per-item
  index/color tables). Edit these only if you understand the layout math — small changes move or
  recolor menu elements.

## Working in this repo

- There are no commands to build/lint/test. Verification means inspecting bytes and (ideally)
  rendering an asset to confirm a change.
- Treat every file as load-bearing firmware data. Before editing or deleting anything, inspect it
  and preserve its exact size unless you have confirmed the firmware tolerates a different size.
- Keep a backup before modifying any file — there is no version control to undo a mistake.
- `.findings/` and `.utils/` are safe to edit freely — they are not read by the console.
