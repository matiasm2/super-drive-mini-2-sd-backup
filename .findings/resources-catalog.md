# Resources/ — Catálogo completo

Investigación realizada en junio 2026 por análisis de bytes y heurística de
similitud entre filas (inter-row similarity) para confirmar dimensiones RGBA.

---

## Dimensiones RGBA — confirmadas

Las imágenes son raw RGBA (4 bytes/px, orden R G B A, alpha siempre 0xFF).
Las dimensiones se detectaron midiendo la similitud entre filas adyacentes: el
ancho correcto minimiza la diferencia media entre filas. Los scores son medias
de diferencia absoluta por pixel; cuanto más bajo, más segura la dimensión.

| Bytes      | Píxeles | Dimensión | Score | Interpretación                       |
|------------|---------|-----------|-------|--------------------------------------|
| 1 637 760  | 409 440 | **853×480** | 7.1  | Fondo de pantalla completa (16:9 480p) |
|   491 520  | 122 880 | **256×480** | 6.65 | Panel lateral (portrait)             |
|   191 040  |  47 760 | **597×80**  | 1.03 | Franja horizontal de UI              |
|    32 116  |   8 029 | **217×37**  | 14.7 | Elemento pequeño / overlay           |

La resolución 853×480 es exactamente 16:9 a 480p — el SoC renderiza la UI aquí
y el codificador HDMI escala a 720p o 1080p.

Los PNGs correspondientes están en `.findings/resources/`.

---

## Catálogo de archivos

### Fondos completos — 853×480 (1 637 760 bytes)

Trece archivos de pantalla completa en dos generaciones: 6 originales de fábrica
(dic-2020) y 7 de una actualización posterior (ago-2021).

| Archivo       | Fecha      | Avg RGB       | Tono predominante  | Observaciones                        |
|---------------|------------|---------------|--------------------|--------------------------------------|
| `cero.phl`    | 2020-12-14 | (50, 62, 84)  | Azul               | Original fábrica, 1 de 6 categorías  |
| `dism.cef`    | 2020-12-14 | (32, 23, 13)  | Muy oscuro / marrón| Idem                                 |
| `efsui.stc`   | 2020-12-14 | (73, 68, 46)  | Naranja / ocre     | Idem                                 |
| `ihds.bke`    | 2020-12-14 | (66, 46, 56)  | Rojizo / morado    | Idem                                 |
| `sdclt.occ`   | 2020-12-14 | (84, 59, 65)  | Rojizo             | Idem                                 |
| `spmpm.gdp`   | 2020-12-14 | (43, 65, 47)  | Verde              | Idem                                 |
| `c1e.pal`     | 2021-08-05 | (61, 68, 98)  | Azulado            | Actualización ago-2021               |
| `desk.cpl`    | 2021-08-05 | (64, 76, 91)  | Azulado / cian     | Idem (primer pixel teal #6DD9D3)     |
| `fdbil.ph`    | 2021-08-05 | (57, 60, 107) | Azul-violeta       | Idem                                 |
| `fltmc.sta`   | 2021-08-05 | (62, 36, 45)  | Rojizo / magenta   | Idem (primer pixel #6D0B59 — púrpura)|
| `url.bvs`     | 2021-08-05 | (74, 50, 90)  | Azul-morado        | Idem                                 |
| `wshom.ocx`   | 2021-08-05 | (70, 64, 85)  | Azulado            | Idem                                 |
| `x86e.hgp`    | 2021-08-05 | (68, 56, 71)  | Lila / salmón      | Idem                                 |

Los 6 fondos de dic-2020 corresponden con alta probabilidad a los 6 tabs de
categoría (`sport`, `shooting`, `fighting`, `roms`, `puzzle`, `adventure`).
Los 7 de ago-2021 son reemplazos o variaciones del mismo set, posiblemente
un "tema" alternativo que el firmware carga según configuración.

---

### Paneles laterales — 256×480 (491 520 bytes)

Seis archivos, todos comienzan con el mismo pixel oscuro `rgb(28,19,7)` (marrón
oscuro casi negro). El contenido varía sutilmente (≈175 colores únicos por
archivo) — son gradientes de oscuro a más oscuro que actúan como paneles de
fondo a los lados del área de selección de juego. Probablemente uno por categoría.

| Archivo      | Fecha      | Primer RGB   |
|--------------|------------|--------------|
| `bisrv.nec`  | 2020-12-14 | (28, 19, 7)  |
| `cca.bvs`    | 2020-12-14 | (28, 19, 7)  |
| `d2d1.hgp`   | 2020-12-14 | (28, 19, 7)  |
| `fhshl.skb`  | 2020-12-14 | (28, 19, 7)  |
| `gpapi.bvs`  | 2020-12-14 | (28, 19, 7)  |
| `pwsso.occ`  | 2020-12-14 | (28, 19, 7)  |

> **Nota:** `bisrv.nec` es el panel lateral, **no** una BIOS ROM ni código
> ejecutable. El nombre es deliberadamente engañoso. Verificado por bytes.

---

### Franjas horizontales — 597×80 (191 040 bytes)

Once archivos. Todos de dic-2020. Se dividen en dos grupos por color promedio,
lo que sugiere dos estados (activo/inactivo) de los tabs de categoría, o
elementos de UI distintos:

**Grupo A — tono naranja medio `~(63,43,17)` (5 archivos):**
| Archivo      | Centro avg   |
|--------------|--------------|
| `gpsvc.bvs`  | (63, 43, 17) |
| `hgcpl.cke`  | (63, 43, 17) |
| `ksxbar.ax`  | (63, 43, 17) |
| `mfsvr.nkf`  | (63, 43, 17) |
| `msdmo.gdb`  | (63, 43, 17) |

**Grupo B — tono oscuro variable (6 archivos):**
| Archivo      | Centro avg   |
|--------------|--------------|
| `dsreg.bvs`  | (40, 31, 22) |
| `dxva2.nec`  | (43, 34, 26) |
| `hlink.bvs`  | (44, 35, 27) |
| `lfsvc.dll`  | (71, 63, 55) |
| `t2ac.sgf`   | (28, 20, 12) |
| `werui.ioc`  | (82, 75, 68) |

Hipótesis: 5 franjas "estado A" + 6 franjas "estado B", donde A/B son variantes
visuales (p.ej. tab seleccionado vs no seleccionado o tab con foco vs sin foco).

---

### Overlays pequeños — 217×37 (32 116 bytes)

| Archivo      | Tipo        | Descripción                                              |
|--------------|-------------|----------------------------------------------------------|
| `igc64.dll`  | rgba-overlay | Todos los píxeles `#FFFFFF00` (blanco totalmente transparente). Placeholder o máscara vacía de 217×37. |
| `wshrm.nec`  | rgba-gradient| Máscara blanca con alpha en gradiente: 0 → 255 (pico en px 1769 de 8029) → 0. Efecto de transición / fade. |

---

### Audio

El firmware usa dos formatos: WQW (comprimido, igual que en .zmd) para el audio
principal, y PCM raw de 16-bit (signed LE) para samples cortos.

| Archivo         | Bytes      | Formato  | Duración aprox¹ | Hipótesis de uso    |
|-----------------|------------|----------|-----------------|---------------------|
| `pcm.asd`       | 3 008 126  | WQW      | ~17s comprimido | Música/audio de arranque |
| `pagefile.sys`  | 3 119 630  | PCM raw  | ~17.7s @ 44.1kHz stereo | Música de fondo del menú |
| `dpnet.dll`     | 5 886      | PCM raw  | ~0.7s @ 8kHz mono | Efecto de sonido UI  |
| `help.lis`      | 10 500     | PCM raw  | ~1.3s @ 8kHz mono | Efecto de sonido UI  |
| `nyquest.gdb`   | 11 414     | PCM raw  | ~1.4s @ 8kHz mono | Efecto de sonido UI  |
| `oldversion.kbe`| 16 908     | PCM raw  | ~2.1s @ 8kHz mono | Efecto de sonido UI  |
| `swapfile.sys`  | 14 734     | PCM raw  | ~1.8s @ 8kHz mono | Efecto de sonido UI  |

¹ Las duraciones son estimaciones; el sample rate real no está confirmado.
  Para PCM raw, los valores más probables son 8000 Hz mono o 22050 Hz mono.

---

### Tablas de datos / curvas

| Archivo      | Bytes | Contenido                                                              |
|--------------|-------|------------------------------------------------------------------------|
| `c2fkec.pgt` | 4 236 | Tabla de lookup de 16-bit. Valores `0x00FE/0x00FF` (≈−1,−2) al inicio que suben gradualmente a valores positivos — perfil de onda sinusoidal. Usada probablemente para animaciones del menú. |
| `qasf.bef`   | 3 256 | Tabla mixta: primeros 0x30 bytes en cero, luego una campana de valores uint32 BE (0 → 193 → 0), seguida de valores RGBA en BE (`140F08FF`, `2A221AFF`…). Posible kernel de blur o tabla de color para efectos de UI. |

---

### Archivos de sistema / configuración

| Archivo          | Bytes     | Tipo        | Descripción                                                |
|------------------|-----------|-------------|------------------------------------------------------------|
| `Archive.sys`    | 8         | state marker| Dos uint32 LE: `00000000` y `02000000`. Estado del sistema (último acceso / flags). Se actualizó al 2026-06-23 (última lectura de la SD). |
| `Foldername.ini` | 201       | config      | Configuración de tabs del menú — ver análisis en CLAUDE.md. |
| `yahei_Arial.ttf`| 1 840 356 | TrueType    | Fuente YaHei+Arial usada por el menú. Único archivo con nombre honesto. |

---

## Resumen de tipos

```
853×480 RGBA    13 archivos   fondos de pantalla completa
256×480 RGBA     6 archivos   paneles laterales
597×80  RGBA    11 archivos   franjas horizontales de UI
217×37  RGBA     2 archivos   overlays pequeños / transición
Audio WQW        1 archivo    boot audio (pcm.asd)
Audio PCM raw    5 archivos   efectos de sonido
Audio PCM raw    1 archivo    música de fondo (pagefile.sys)
TTF font         1 archivo    yahei_Arial.ttf
Config           1 archivo    Foldername.ini
Tablas           2 archivos   c2fkec.pgt, qasf.bef
State marker     1 archivo    Archive.sys
────────────────────────────────────────────────────────
TOTAL           44 archivos
```

---

## Metodología de detección de dimensiones

Para cada grupo de tamaño, se calcula un score por ancho candidato W:

```
score(W) = mean over sampled rows of:
    (Σ |row[y][x,channel] - row[y+1][x,channel]| for all x,channels) / W
```

El ancho correcto produce filas adyacentes más similares (imágenes tienen
continuidad vertical natural). Scores confirmados:

```
597×80   score=1.03  ← más confiable (diferencia 10× con el siguiente)
256×480  score=6.65
853×480  score=7.10
217×37   score=14.7
```

Para factorizar posibles dimensiones se usó la factorización prima de cada
tamaño en píxeles — e.g., 409440 = 2⁵ × 3 × 5 × 853, lo que deja a 853×480
como el único par de factores con aspecto razonable (16:9).
