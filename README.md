# Super Drive Mini 2 - Backup de SD/TF Card

**Backup completo del sistema de archivos** de la consola retro clone **Super Drive Mini 2** (también conocida como **SG800** y otros rebrands).

## ¿Qué es esto?

Este es un **backup crudo del firmware y librería de juegos** de una consola emuladora **Mega Drive/Genesis clone**. No se trata de un proyecto de software tradicional, sino del sistema de archivos completo de la tarjeta SD/TF que el SoC (System-on-Chip) de la consola lee para cargar:

- 🎮 Menú de usuario con interfaz gráfica
- 🖼️ Recursos visuales (fondos, logos, botones)
- 🎵 Audio del menú y sonidos
- 🗂️ Librería de juegos organizados por categoría
- ⚙️ Configuración del firmware

## Hardware

La consola utiliza un **SoC genérico chino** que emula la arquitectura del **Sega Mega Drive / Genesis**:

- **Procesador**: Emulador 68000/Z80
- **Salida**: HDMI
- **Controles**: 2 mandos inalámbricos de 2.4 GHz (incluidos)
- **Almacenamiento**: MicroSD expandible
- **Juegos preinstalados**: ~688-5000 juegos (varía según versión)

### Características importantes

⚠️ **El firmware ejecutable NO está en esta tarjeta.** El programa principal (menú de inicio + emulador) reside en la **memoria flash interna** del SoC. Esta SD es solo una capa intercambiable que contiene "interfaz + librería de juegos".

## Estructura de archivos

```
Resources/              → Assets del firmware y UI (imágenes, fuente, audio)
sport/                  → Juegos de deportes (Mega Drive)
shooting/               → Juegos de disparo (Mega Drive)
fighting/               → Juegos de lucha (Mega Drive)
puzzle/                 → Juegos de puzzle (Mega Drive)
adventure/              → Juegos de aventura (Mega Drive)
roms/                   → Juegos de NES (emulador compatible)
```

Cada categoría contiene:
- Archivos ROM (`.zmd` para Mega Drive en categorías específicas, `.nes`/`.md`/`.zip` en `roms/`)
- Carpeta `save/` para guardados y datos SRAM

## Formatos de juegos

### `.zmd` - Contenedor Mega Drive propietario
- **No es un ROM estándar** (sin firma `SEGA` en 0x100)
- Estructura: `[Miniatura RGBA] + [Payload WQW comprimido]`
- El formato WQW es el contenedor genérico del fabricante (también usado en audio)
- **No se puede cargar directamente** en emuladores estándar — requiere desempaquetar con las herramientas del fabricante

### Archivos en `roms/` - Múltiples formatos
La carpeta `roms/` es un cargador universal que acepta (confirmado):

- **`.nes`** - Archivos iNES estándar (firma `4E 45 53 1A`)
- **`.md`** - ROMs Mega Drive sin empacar (raw binaries)
- **`.zip`** - Archivos comprimidos (ROM + assets en ZIP)

Todos se cargan sin necesidad de conversión a `.zmd` propietario. Otros formatos pueden funcionar pero no han sido probados.

## ⚠️ Las extensiones son engañosas

**Los nombres de archivo NO indican su contenido real.** Los archivos están disfrazados con extensiones del sistema Windows (`.nec`, `.dll`, `.sys`, `.cpl`, `.occ`, `.bvs`, `.pal`, `.asd`, `.ocx`, `.gdb`, etc.).

**Identificar siempre por contenido**, nunca por nombre:
- Usar `file`, `xxd`, `od -x` para inspeccionar bytes
- La mayoría son **bitmaps RGBA crudo** (4 bytes/píxel, sin encabezado)
- `bisrv.nec` = imagen RGBA de splash, no código
- `pcm.asd` = audio con magic `WQW`
- `yahei_Arial.ttf` = única excepción (TrueType legítimo)

## Configuración del menú: `Resources/Foldername.ini`

Archivo de texto (CRLF) que configura las categorías del menú:

```
.zmd                    → Extensión de juegos Mega Drive
sport                   → Carpeta 1 (mostrada en menú)
shooting                → Carpeta 2
fighting                → Carpeta 3
roms                    → Carpeta 4
puzzle                  → Carpeta 5
adventure               → Carpeta 6
[colores de UI...]
[parámetros de layout...]
```

**Advertencia**: Los cambios de tamaño de archivo pueden romper el menú de inicio. Editar solo con inspección previa.

## Trabajar con este backup

### ✅ Operaciones seguras
- Inspeccionar contenido de archivos (`file`, `xxd`, `strings`)
- Agregar juegos ROM nuevos a las carpetas de categoría
- Renderizar/convertir assets RGBA (instalar `PIL`, `ImageMagick`, o `ffmpeg`)

### ⚠️ Operaciones delicadas
- **No renombrar archivos** sin entender su propósito en `Foldername.ini`
- **No modificar tamaños** de archivos del menú sin confirmación
- **Hacer backup antes de editar** — no hay control de versión
- Preservar exactitud de bytes en assets de UI

### 🔧 Herramientas útiles
```bash
# Inspeccionar contenido
file <archivo>
xxd -l 256 <archivo>        # Primeros 256 bytes
strings <archivo>

# Trabajar con imágenes RGBA
python3 -c "from PIL import Image; Image.frombytes('RGBA', (W, H), open('file.bin', 'rb').read()).save('out.png')"
```

## Compatibilidad con otros clones

Este backup es específico del **Super Drive Mini 2 / SG800**, pero **la arquitectura es compartida por otras consolas retro clone**:

- 🎮 **Sega Mega Drive 2 Retro** (versiones budget)
- 🎮 **Super Console** (variantes basadas en el mismo SoC)
- 🎮 **Retro Game Stick** (arquitectura similar)
- 🎮 **Otras marcas rebranded** del mismo SoC chino

⚠️ Los TF/SD de otras marcas **pueden no ser 100% compatibles** — el layout de menú, dimensiones de assets y `Foldername.ini` varían, pero la estructura base es idéntica.

## Palabras clave para búsqueda

- Super Drive Mini 2
- SG800 Retro Console
- Sega Mega Drive Clone SD Backup
- Sega Genesis Emulator MicroSD
- Retro Console Firmware
- Emulador Mega Drive
- Backup SD Consola Retro
- Genesis Clone ROM
