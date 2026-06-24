# Hardware — Super Drive Mini 2 / SG800

Inspección física de placa, junio 2026.

---

## PCBs

| Placa       | Identificador      | Fecha        |
|-------------|--------------------|--------------|
| Principal   | **DFG01_A_HDMI_V1.1** | —         |
| Secundaria  | **SG801_B**        | 2022-05-16   |

La placa secundaria (marrón) aloja los dos puertos USB de los receptores inalámbricos
2.4 GHz (USB1, USB2) y el LED de encendido. Se conecta a la placa principal mediante
cable ribbon plano. El nombre "SG801" es consistente con el modelo comercial "SG800".

---

## Componentes identificados

### RAM — Hynix H5PS1G63EFA

- **Fabricante:** SK Hynix
- **Tipo:** DDR2 SDRAM
- **Capacidad:** 1 Gbit = **128 MB**
- **Sufijo de placa:** 20L / lote 917A
- **Función:** RAM de sistema del SoC

### Flash — XMC XM25QE16B (SPI NOR, confirmado)

- **Fabricante:** XMC (武汉新芯 / Wuhan Xinxin Semiconductor)
- **Modelo completo:** XM25QE16B ZIG — **16 Mbit = 2 MB** de SPI NOR Flash
- **Encapsulado:** SOIC-8 (ZIG = variante de package)
- **Fecha de fabricación:** semana 09 de 2021 (marcado "2109Y")
- **Función:** almacenamiento del firmware ejecutable — bootloader + emulador NES +
  emulador MD + código de menú UI. 2 MB es suficiente para todo el código compilado.
  **Este chip es donde vive el código** que no está en la SD card.
  Confirmación definitiva: la tarjeta SD es solo "skin + librería de juegos".

### Transceptor inalámbrico — XN297LBW (confirmado)

- **Fabricante:** compatible con familia nRF24L01 (fabricante: probablemente Beken/Beijing o similar ODM)
- **Modelo completo:** XN297LBW — "L" = low power, "BW" = variante de encapsulado
- **Tipo:** transceptor RF 2.4 GHz FSK/GFSK, encapsulado 8 pines
- **Fecha de fabricación:** semana 42 de 2022 (marcado "2242D")
- **Función:** comunicación inalámbrica con los mandos 2.4 GHz
- **Nota:** este chip está en la **placa principal**. Los puertos USB de la placa SG801_B
  son para mandos USB cableados adicionales o los dongles opcionales; el XN297LBW es
  el receptor 2.4 GHz integrado principal.

### SoC principal (sin identificar)

- Encapsulado QFP con muchos pines, tamaño mediano-grande
- Marcas **cubiertas deliberadamente** con epoxi — práctica habitual para dificultar
  clonación o análisis
- Candidatos por las características (HDMI, DDR2, microSD, NES+MD, 2022):
  - **Ingenic JZ4760B** — MIPS32, DDR2, SF2000 (sin HDMI nativo)
  - **Ingenic X1000/X1830** — Ingenic más nuevo con HDMI
  - **ASIC propietario** de ODM chino

---

## Referencia cruzada con SF2000

La SF2000 (Sup, mismo tipo de clon) usa:
- SoC: Ingenic JZ4760B (MIPS32, 600 MHz)
- RAM: 128 MB LPDDR (coincide en capacidad con este dispositivo)
- Flash: 8 MB SPI NOR
- Sin HDMI (solo AV compuesto)

Este dispositivo tiene HDMI y DDR2 en lugar de LPDDR → SoC diferente o versión más
nueva. Las herramientas de la comunidad SF2000 (frogtool, etc.) pueden no aplicar
directamente, pero la arquitectura de la SD card (assets RGBA, WQW/ZMD) es muy similar.

---

## Pendiente

- [ ] Identificar modelo exacto del SoC (buscar "DFG01_A_HDMI_V1.1" en comunidades
      de hardware chino / retro-gaming; o quitar el epoxi)
