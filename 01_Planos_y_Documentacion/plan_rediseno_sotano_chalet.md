# Memoria Técnica: Rediseño Integral del Sótano / Nivel Jardín Chalet Alpino (Opción A)

**Proyecto:** Casa Chalet Rústico Mejorado (`02_Modelos_CAD/casa_nuevo_proyecto.dxf`)  
**Nivel:** Sótano / Nivel Jardín (`Z = -2,55 m` a `-0,15 m`)  
**Área de Planta:** `9,00 × 8,30 m = 74,70 m²` interior + `4,20 × 2,20 m = 9,24 m²` terraza exterior ajardinada  
**Altura Libre:** `2,40 m` (casetones entre vigas maestras; `2,28 m` bajo vigas rústicas)

---

## 1. Justificación y Diagnóstico Topográfico
El nivel inferior no constituye un sótano enterrado u oscuro, sino un **Nivel Jardín (*Walk-Out Garden Level*)** con privilegios ambientales y topográficos únicos:
1. **Fachada Sur (Y = 0,00 m, ancho 9,00 m):** Conectada a ras de piso con el Patio Trasero propio (`~31 m²` a cota `Z = -2,55 m`).
2. **Fachada Este (X = 9,15 m, fondo 8,30 m):** Retiro lateral derecho a cota `-2,55 m` desde `Y = 9,50 m` con acceso peatonal independiente desde la calle (Av. 4) y potencial de ventilación e iluminación natural en toda su longitud.
3. **Muros Norte y Oeste de contención:** Proporcionan inercia térmica ideal para conservación de vino y confort acústico.

Se sustituyó la distribución laberíntica obsoleta (antiguo muro interior residual en `X = 6,25 m`, lavadero bloqueando el jardín sur y sala sin ventanas al este) por la **Opción A**, unificando la planta en un programa social, recreativo y de invitados de alto nivel.

---

## 2. Programa Arquitectónico Implementado

### 2.1 Cava de Vinos y Mesa de Cata Alpina (Noroeste, `4,25 × 2,80 m = 11,76 m²`)
* **Cerramiento:** Vitrina panorámica con zócalo de mampostería de piedra (`0,60 m`), montantes verticales de hierro forjado negro, paños de vidrio templado y doble puerta central (`1,20 × 2,10 m`).
* **Equipamiento:**
  * Botelleros modulares de roble macizo de piso a techo sobre muro norte y testero oeste.
  * Nicho central de piedra pizarra para decantación y cata.
  * Mesa alta de cata sobre barricas rústicas (`1,15 × 0,70 m`, `H = 1,00 m`) con 4 taburetes altos de cuero y hierro.

### 2.2 Maletero y Depósito Bajo Escalera (`X = 0,30..1,40 m, Y = 6,00..8,15 m`)
* Aprovechamiento de la bóveda inferior del tramo alto de la escalera intacta (`ESCALERA_3D`).
* Acceso privado desde la Cava mediante puerta rústica de madera (`0,72 × 1,92 m`).
* Estanterías modulares profundas de almacenamiento en el fondo norte.

### 2.3 Gran Salón-Taberna, Barra Húmeda y Salón Cine 85" (`Centro y Este, ~42 m²`)
* Espacio diáfano continuo articulado visualmente por las vigas maestras de madera:
  * **Barra Húmeda Alpina (*Wet Bar*, `2,20 m`):** Adosada al muro este del baño (aprovechando núcleo de instalaciones) con mesón de piedra pizarra, fregadero auxiliar de bar en acero inoxidable, cava refrigerada bajo mesón y estanterías aéreas de madera y forja para licores y copas.
  * **Salón Lounge & Cine Familiar:** Mueble bajo rústico y pantalla de cine/TV de **`85"`** sobre muro norte de piedra iluminada; sofá esquinero en L de cuero/lino bajo el antepecho este (`0,90 m`) y mesa central de tronco macizo.
  * **Comedor / Mesa de Juegos de Taberna (6 puestos, `1,80 × 0,95 m`):** Centrada frente al jardín sur, iluminada por el ventanal este y con circulación fluida hacia la salida exterior.

### 2.4 Suite de Huéspedes / Estudio Jardín (Suroeste, `2,50 × 3,30 m = 8,25 m²`)
* Cama matrimonial con cabecero rústico de tablones de madera (`1,40 × 1,88 m`), mesas de noche flotantes y clóset empotrado de madera maciza.
* Gran ventanal rústico de `1,60 × 1,25 m` hacia el patio trasero con contraventanas exteriores de madera (*shutters*).

### 2.5 Baño Completo Rústico en Piedra (Centro-Sur, `1,60 × 3,30 m = 5,28 m²`)
* Ducha *walk-in* con piso y banco lateral en piedra pizarra oscura y mampara fija de vidrio templado.
* Ventilación e iluminación directa al patio mediante celosía alta de madera (`1,05 × 0,45 m`).
* Inodoro discreto y mueble suspendido de madera maciza con lavamanos tipo *vessel* de piedra natural tallada y espejo enmarcado en hierro forjado.

### 2.6 Terraza de Piedra Laja y Pérgola Rústica en Patio Trasero (`4,20 × 2,20 m = 9,24 m²`)
* **Acceso:** Gran Doble Puerta Francesa rústica de madera y vidrio (`2,20 × 2,10 m`), con hojas replegables contra las pilastras de piedra dejando vano libre de `2,06 m`.
* **Estructura de Pérgola:** 3 pilares frontales con basamento de piedra (`Z = -2,55..-1,85 m`) y postes cuadrados de madera maciza con tornapuntas (`Z = -1,85..-0,28 m`), vigas maestras y 9 cabrios de sombra (`Z máx = -0,04 m`, cota inferior a la losa de Planta Baja sin interferir con ventanas superiores).
* **Mobiliario Exterior:** Banco/sala de exterior bajo pérgola, mesa baja de piedra y jardinera de mampostería con vegetación ornamental bajo el ventanal de la Suite.

---

## 3. Cuadro de Capas DXF Incorporadas
| Capa | Color AutoCAD | Descripción |
|---|---|---|
| `SOTANO_LOSA_3D` | 8 (Gris) | Losa de piso sótano + Terraza exterior de piedra laja |
| `SOTANO_MUROS_EXT_3D` | 4 (Cian) | Envolvente perimetral exterior y muros de contención |
| `SOTANO_MUROS_INT_3D` | 4 (Cian) | Tabiquería interior (Suite, Baño, Maletero) |
| `SOTANO_COLUMNAS_3D` | 1 (Rojo) | 12 columnas/machones estructurales 100% conservados |
| `SOTANO_PIEDRA_MADERA_3D` | 34 (Madera) / 8 (Piedra) | Zócalos pétreos, forros de columnas, vigas de techo, vitrina Cava y Pérgola |
| `SOTANO_MOBILIARIO_3D` | 30 / 34 / 8 / 7 / 3 | Mobiliario 3D detallado de Cava, Wet Bar, Cine, Taberna, Suite, Baño y Terraza |
| `SOTANO_ROTULOS` | 4 (Cian) | Identificadores espaciales en 3D |
| `PLANTA_SOTANO_2D` | Variable | Lámina arquitectónica técnica 2D completa con mobiliario y pérgola |

---

## 4. Parámetros de Seguridad e Integridad Estructural
* **Cero invasión a colindancias:** `minX >= 0,15 m` en toda la envolvente; retiro lateral derecho `maxX <= 10.10 m`; retiro sur respetado frente a cerca perimetral posterior (`minY >= 0.65 m` en terreno).
* **Escalera principal intacta:** Tramo 1 (`X = 0,30..1,40 m`, `Y = 4,45..7,40 m`) 100% transitable sin obstrucciones.
* **Modelo R12 AC1009 verificado:** Líneas pares, 0 códigos inválidos, 0 capas huérfanas, 944 sólidos 3D y 757 líneas 2D.
