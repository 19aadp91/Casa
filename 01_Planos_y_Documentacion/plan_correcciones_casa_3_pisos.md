# Plan de Correcciones Arquitectónicas y Funcionales (`casa_proyecto_3_pisos.dxf`)

> [!IMPORTANT]
> **Alcance de la intervención:** Estas **7 mejoras** se aplicarán exclusivamente sobre [`build_casa_3_pisos.py`](file:///c:/Users/alvar/Documents/casa/04_Scripts_Parametricos/build_casa_3_pisos.py) y [`casa_proyecto_3_pisos.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_proyecto_3_pisos.dxf) una vez apruebes este plan. El proyecto previo [`casa_nuevo_proyecto.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_nuevo_proyecto.dxf) seguirá intacto.

---

## 1. Segundo Piso (`Z = +3,00 m`): Despensa Bajo Escalera + Ubicación de la Nevera

### Diagnóstico del problema actual
El cuarto cerrado de despensa en `X = 3,00..4,55 m, Y = 6,35..7,50 m` y el bloque frente a la escalera estrechaban el paso entre el núcleo de escaleras y la cocina, desaprovechando el volumen libre bajo el tramo alto de la escalera que sube al Piso 3 (`X = 0,30..1,45 m, Y = 4,40 → 7,40 m`).

### Solución proyectada
1. **Eliminación total del cuarto de despensa central (`X = 3,00..4,55 m`):** Se libera un hall diáfano de **`3,10 m` de ancho libre** conectando fluidamente escaleras, cocina con isla, baño social y mirador sur.
2. **Nueva Despensa Walk-In Bajo la Escalera al Piso 3 (`X = 0,30..1,45 m, Y = 5,55..7,40 m`):**
   * En el tramo Norte (`Y = 5,55 → 7,40 m`), los peldaños ya van subiendo entre `Z = +4,15 m` y `Z = +6,00 m`, dejando debajo una cavidad limpia de `1,15 × 1,85 m` con altura máxima de `2,70 m` en su frente hacia la cocina.
   * Se cierra lateralmente bajo la zanca diagonal con tabique de madera machihembrada (`X = 1,45..1,52 m`), **puerta rústica frontal en `Y = 7,40 m` (`0,85 × 2,10 m`)** abriendo directo hacia la cocina, e interior equipado con **4 niveles de estanterías escalonadas en "L"**.
3. **Ubicación Ergonómica y Detallada de la Nevera + Torre de Hornos:**
   * Se reubica en el **remate Norte del Mesón Lineal Oeste (`X = 0,30..1,08 m, Y = 11,55..13,10 m`)**, adosada a la medianera ciega para no bloquear ninguna visual ni circulación:
     * **Nevera *French Door* (`0,90 × 0,78 × 1,92 m`):** Modelada en detalle (2 puertas superiores con manillas verticales + gavetón inferior de congelador en acero/grafito `Y = 12,15..13,05 m`), abriendo hacia un pasillo libre de `1,32 m` frente a la isla.
     * **Torre de Horno y Microondas empotrados (`0,60 m`, `Y = 11,52..12,12 m`)** contigua al sur, seguida del **Tope de 5 Hornillas + Campana (`Y = 10,15..11,15 m`)** y el **Fregadero Doble (`Y = 8,65..9,65 m`)**, dejando `Y = 7,40..8,55 m` completamente despejado frente a la puerta de la nueva Despensa bajo escalera.

```
   COCINA Y ESCALERAS EN PISO 2 (CORREGIDO)
   +-----------------------+-----------------------------------------------+
   | [NEVERA] (Y=12,1..13) |                                               |
   | [HORNOS] (Y=11,5..12) |                                               |
   | [COCINA 5H + CAMPANA] |        [ GRAN ISLA CENTRAL + 4 BANCOS ]       |
   | [FREGADERO DOBLE]     |        (Recibe brisa directa desde el Este)   |
   |    (Paso libre 1,40m) |                                               |
   +---[Puerta Despensa]---+               PASO AMPLIO Y LIBRE (3,10 m)    | Y = 7,40
   | DESPENSA BAJO ESCALERA|  LLEGA DE PB   (Sin muros ni muebles en medio)|
   | (Aprovecha bajo rampa |  (X=1,55..2,65)                               |
   |  alta a P3, Y=5,5..7,4|                                               |
   | - - - - - - - - - - - |                                               |
   | ARRANCA SUBIDA A P3 ^ |                                               | Y = 4,40
   +-----------------------+-----------------------------------------------+
```

---

## 2. Tercer Piso (`Z = +6,00 m`): Eliminación de Habitación 4 → Gran Terraza Mirador & BBQ en Esquina

### Diagnóstico del problema actual
La `Habitación 4` en el Piso 3 cerraba la esquina Sureste (`X = 6,00..9,00 m, Y = 0,15..4,30 m`), reduciendo la terraza sur a una franja central estrecha (cuando la casa ya cuenta con 3 amplios dormitorios arriba más la habitación de huéspedes en Piso 2).

### Solución proyectada
* Se eliminan los muros cerrados y mobiliario de la `Habitación 4` del Piso 3, unificando toda la franja Sur-Centro y Sur-Este (`X = 2,90..9,15 m, Y = 0,00..4,30 m`) en una **Gran Terraza Mirador & Quincho Panorámico de `26,88 m²` (`6,25 × 4,30 m`)**.
* **Doble frente abierto a la brisa (`Este + Sur`):** Baranda alpina continua en Cruz de San Andrés a lo largo de todo el borde Sur (`X = 2,92..9,07 m`) y del borde Este (`Y = 0,08..4,30 m`), manteniendo vistas las **columnas metálicas negras** que sostienen el alero del techo chalet.
* **Zonificación del mobiliario exterior:**
  * **Barra de Parrillera / BBQ + Fregadero Auxiliar (`X = 6,25..8,65 m, Y = 3,65..4,28 m`):** Adosada inteligentemente al muro sur del Baño Familiar para compartir su misma pared hidrosanitaria.
  * **Comedor Exterior de 8 puestos (`Centro, X = 3,60..5,60 m`)** + **Sala Lounge Mirador en la esquina Sureste (`X = 6,60..8,75 m, Y = 0,55..2,45 m`)**.

---

## 3. Buhardilla de Tanques (`Z = +8,68 m`): Reorientación de la Baranda de la Escotilla

### Diagnóstico del problema actual
Al terminar de subir la escalera inclinada (`X = 0,40..1,10 m, Y = 2,55 → 3,70 m`), la baranda guarda-escotilla corría a lo largo del costado derecho completo (`X = 1,21 m, Y = 2,52..3,70 m`), encerrando al usuario contra el muro norte y dificultando girar/bajarse hacia el área de los tanques y el hidroneumático.

### Solución proyectada
* **Se modifica únicamente la orientación de la baranda guarda-escotilla:**
  * Se coloca la protección en **"L" sobre el borde Sur (`X = 0,38..1,25 m, Y = 2,50 m`) y solo la mitad Sur del borde Este (`X = 1,25 m, Y = 2,50..3,05 m`)** para resguardar la caída profunda del hueco.
  * Se deja **100% libre de baranda el costado de desembarque (`X = 1,20 m, Y = 3,05..4,25 m`, `1,20 m` de paso franco lateral y frontal)**, añadiendo únicamente el poste vertical pasamanos de agarre seguro en `Y = 3,70 m` para que uno pueda bajarse cómodamente tanto de frente como de lado hacia los equipos.

---

## 4. Tercer Piso: Accesos Claros y Visibles al Gran Vestier y al Baño Spa Master

### Diagnóstico del problema actual
El muro entre el Vestier y el Baño Spa estaba cerrado, en `3D` los vanos no tenían marcos ni hojas visibles, y en la lámina `2D` se dibujaban como rectángulos cerrados sin indicar por dónde se entraba.

### Solución proyectada (Circuito claro en 3D y en 2D)
1. **Entrada Principal al Gran Vestier desde el Dormitorio Master (`X = 4,35..4,50 m, Y = 17,05..18,35 m`):**
   * Se modela un **Portal amplio de `1,30 m` con Puerta Corrediza tipo Granero (*Barn Door*)** sobre riel de hierro negro visto, con las hojas abiertas enmarcando la vista hacia el pouf central del vestier.
2. **Paso Interno Directo Vestier ↔ Baño Spa (`Y = 15,90..16,05 m, X = 1,65..2,50 m`):**
   * Se abre una **puerta interna de `0,85 × 2,10 m`** con marco de madera y **hoja entreabierta a `45°`**, conectando el pasillo central del vestier directamente con el área de tocador doble, ducha y tina.
3. **Puerta Auxiliar Dormitorio ↔ Baño Spa (`X = 4,35..4,50 m, Y = 14,55..15,35 m`):**
   * Se incorpora su marco completo y hoja batiente semiabierta hacia el interior del baño, y en `PLANTA_TERCER_PISO_2D` se recortan los muros y se trazan las hojas abiertas de las puertas para lectura inmediata en plano.

---

## 5. Cubierta y Claraboya Central Ventilada: Recorte Real del Techo para Luz y Aire

### Diagnóstico del problema actual
La linterna `CLARABOYA_VENTILADA_3D` existía sobre la cumbrera, pero los faldones `CUBIERTA_CHALET_3D` pasaban continuos y macizos por debajo sin perforación, bloqueando el paso real de los rayos solares y del aire.

### Solución proyectada
1. **Perforación Geométrica Real en Ambos Faldones del Techo (`X = 2,45..5,55 m, Y = 5,50..11,30 m = 17,98 m²` de boca de luz):**
   * Tanto el Faldón Oeste como el Faldón Este se subdividen en **3 paños exactos cada uno** (Tramo Sur `Y < 5,50 m`, Faldón Lateral Exterior al vano, y Tramo Norte `Y > 11,30 m`), eliminando por completo la plancha de techo bajo la claraboya y cortando/enmarcando las vigas con un **anillo estructural metálico negro (`X = 2,45..5,55 m`)**.
2. **Doble Función (Luz Cenital + Chimenea de Ventilación Natural):**
   * Los costados verticales de la linterna (`Z = +10,20 a +12,20 m`) combinan **ventanales fijos de vidrio transparente** (que inundan de luz natural la escalera de P3, la escalera de P2 y el *Family Room*) con **celosías inclinadas cortaviento abiertas** bajo el alero superior de la linterna para que el aire caliente salga por convección sin que entre lluvia.

---

## 6. Sótano Bodega (`Z = -2,55 m`): Redistribución Fluida para Caminar y Abrir la Puerta de Escaleras

### Diagnóstico del problema actual
El `Rack 3` quedaba a solo `45 cm` frente a la puerta de la escalera (`X = 1,55 → 2,00 m`), los pallets del suroeste estrangulaban el paso a `40 cm`, y la báscula/escritorio obstaculizaban la entrada directa desde el portón doble Sur.

### Solución proyectada (Pasillos despejados de `1,80 m` a `2,25 m`)
Se reordena todo el mobiliario sobre el perímetro dejando **una cruz de circulación ancha y 100% libre de obstáculos**:

```
   PLANTA SÓTANO BODEGA CORREGIDA (9,00 x 8,30 m — Z = -2,55 m)
   +-------------------+-------------------------------+-------------------+ Y = 8,15
   | CUARTO ÚTILES     |   CÁMARA DE PRE-FRÍO Y        | [RACK NORTE 1]    |
   | BAJO ESCALERA     |   MADURACIÓN MAYORISTA        | (X=5,85..8,85)    |
   | - - - - - - - - - |   (X=1,60..5,55, Y=5,55..8,1) |                   |
   |                   +-----------[Puerta Corrediza]--+                   | Y = 5,55
   | ESCALERA INTACTA  :                               :                   |
   | (X=0,30..1,40)    :   GRAN PASILLO CENTRAL LIBRE  : AVENIDA PRINCIPAL |
   |                   [P] (Ancho libre = 1,95 m!)     : DE CARGA          | [RACK
   | ESCLUSA ESCALERA   \  • Puerta escalera [P] abre  : (Ancho = 2,20 m   |  MURAL
   | (Y=3,60..4,55)      \   100% libre sin estorbos   :  recto sin nada   |  ESTE]
   +-------------------+-------------------------------:  atravesado)      | (Fondo
   | [RACK]  ZONA DE   | BAÑO OPERATIVO | [MESA GUÍAS] :                   |  0,65m
   | [OESTE] PALLETS   | PERSONAL       | (Adosada)    :                   |  bajo
   | (0,65m) CON PASO  | (X=2,95..4,55, | [BÁSCULA     :                   |  vent.
   |         DE 1,50m  |  Y=0,15..2,70) |  500 kg]     :                   |  altas)
   | [RACK SUR OESTE]  |                | (Al costado) :                   |
   +-------------------+----------------+--------------+===[PORTÓN 2,20m]==+ Y = 0,15
                                                        ^ ENTRADA LIMPIA DESDE RAMPA AV.4
```

* **Mejoras logísticas inmediatas:**
  1. **Puerta de Escalera (`X = 1,40..1,55 m, Y = 3,70..4,55 m`):** Abre con hoja batiente completa hacia un vestíbulo despejado de **`1,95 m` de ancho libre** (`Y = 3,55..5,50 m`) sin ningún mueble enfrente.
  2. **Entrada desde Portón Doble (`X = 6,35..8,55 m`):** Queda una **Avenida Principal Recta de `2,20 m` de ancho (`X = 6,00..8,20 m`)** desde la puerta hasta el fondo Norte; la **Báscula de Plataforma (`500 kg`)** y el **Escritorio de Control** se adosan limpiamente al muro Este del baño (`X = 4,75..5,75 m`), al alcance inmediato de la entrada pero sin atravesarse jamás en el camino.
  3. **Zona Suroeste transitable:** Se retira un pallet sobrante y se deja un pasillo cómodo de **`1,50 m` libres** frente a los racks perimetrales Suroeste para caminar y cargar sin tropiezos.

---

## 7. Planta Baja Comercial (`Z = 0,00 m`): Eliminación de la Bodega Posterior y Redistribución del Baño y el Fondo

### Diagnóstico del problema actual
En Planta Baja todavía quedaba el antiguo **`Gran Almacén Unificado de PB` (`X = 0,30..9,00 m, Y = 0,15..3,50 m`, `33,1 m²`)** cerrado tras un muro transversal ciego en `Y = 3,50..3,65 m`, más el **`Baño Comercial` (`X = 5,85..9,00 m, Y = 3,50..5,55 m`)** atravesado sobre la fachada Este. Ahora que toda la operación de acopio y cámara fría mayorista bajó al **Sótano Bodega (`74,70 m²`)**, ese almacén trasero en Planta Baja resulta redundante, desperdicia metros comerciales de alto valor y tapona las ventanas Sur y Este del salón de ventas.

### Solución proyectada (Aprovechamiento integral del fondo `Y = 0,15..6,20 m`)
Se demuele por completo el muro divisorio de la antigua bodega (`Y = 3,50..3,65 m`) y el cajón del baño Este (`X = 5,85..9,00 m, Y = 3,50..5,55 m`), extendiendo el salón comercial hasta el fondo Sur y alineando los nuevos espacios con la retícula estructural existente (`Eje 1: X = 2,825 m`, `Eje 2: X = 5,925 m` y `Eje G: Y = 3,575 m`):

```
   FONDO DE PLANTA BAJA COMERCIAL REDISTRIBUIDO (Z = 0,00 m — Y = 0,00..8,95 m)
   +-----------------------+-----------------------------------------------+ Y = 8,95
   | ESCLUSA ESCALERA      |                                               |
   | [Puerta Sótano c/llave|    SALÓN COMERCIAL AMPLIADO (~112 m²)         |
   |  + Subida a Piso 2]   |    • [ISLA FRUTAS 4] (X=5,15..6,70, Y=8,1..9,6)|
   | - - - - - - - - - - - |                                               |
   | CUARTO DE ASEO DIARIO |    • [ISLA DEGUSTACIÓN 5]   [MURAL FRIGORÍFICO|
   | BAJO ESCALERA P2      |      (X=5,15..6,70,          LÁCTEOS / QUESOS |
   | (X=1,45..2,75,        |       Y=5,00..6,40)          Y FRUTA PICADA]  |
   |  Y=3,65..5,75)        |                              (X=8,25..8,98)   |
   +---[Entrada Discreta]--+----------------------------+------------------+ Y = 3,60
   | NÚCLEO DE BAÑOS       | BARRA GOURMET DE JUGOS,    | OFICINA          |
   | CLIENTES / PERSONAL   | BATIDOS, CAFÉ Y ENSALADAS  | ACRISTALADA DE   |
   | (Esquina Suroeste     | DE FRUTAS (10,20 m²)       | ADMINISTRACIÓN Y |
   |  ciega: 8,20 m²)      | • Mostrador rústico madera/| CAJA MAYORISTA   |
   | • Antebaño con doble  |   piedra + 4 taburetes     | (10,05 m²)       |
   |   lavamanos exterior  | • Contra-barra inox con    | • Frente en      |
   | • Cabina Damas (PMR)  |   licuadoras y fregadero   |   vidrio y hierro|
   | • Cabina Caballeros   | • Gran ventana Sur abierta |   negro con      |
   | • Baja plomería recta |   que mete luz y ventilac. |   control visual |
   |   desde Lavandería P2 |   cruzada N–S al local!    |   de toda tienda |
   +====[Vent. Alta Sur]===+=====[Ventanal Sur Luz]=====+==[Vent. Sur/Este]+ Y = 0,00
```

* **Ventajas funcionales, sanitarias y comerciales de esta redistribución:**
  1. **Reubicación estratégica del Baño al rincón Suroeste ciego (`X = 0,30..2,75 m, Y = 0,15..3,50 m = 8,20 m²`):**
     * Aprovecha la esquina medianera Oeste detrás del núcleo de escaleras (el punto menos comercial del lote) y **coincide milimétricamente debajo del Cuarto de Lavado del Piso 2 (`X = 0,30..2,75 m, Y = 0,15..3,50 m`)**, unificando una sola bajante hidrosanitaria vertical hacia el baño del Sótano.
     * Cuenta con **antebaño de privacidad** (doble lavamanos y espejo, evitando vista directa desde las frutas hacia los sanitarios), **2 cabinas separadas (Damas accesible + Caballeros)**, ventilación natural alta hacia el Sur (`Y = 0,00 m`) y un práctico **Cuarto de Aseo Diario bajo el tramo alto de la escalera a P2 (`X = 1,45..2,75 m, Y = 3,65..5,75 m`)**.
  2. **Liberación de la Fachada Este + Nuevo Mural Frigorífico (`X = 8,25..8,98 m, Y = 4,90..6,20 m`) e Isla 5 (`X = 5,15..6,70 m, Y = 5,00..6,40 m`):**
     * Al quitar el antiguo baño que tapaba el muro Este, se destapa la ventana `Y = 4,10..5,00 m` y se incorpora exhibición refrigerada vertical para quesos, lácteos, jugos embotellados y bandejas listas para llevar.
  3. **Barra Gourmet de Jugos Naturales, Café y Fruta Picada en el Fondo Central (`X = 2,90..5,85 m, Y = 0,15..3,60 m = 10,20 m²`):**
     * Funciona como **"ancla imán" al fondo del local** (haciendo que el cliente recorra todas las islas de frutas), rentabiliza al máximo la fruta madura del día sin merma, y mantiene el eje central Sur abierto con ventana panorámica (`X = 3,40..5,40 m`) para garantizar **ventilación cruzada Norte–Sur y Este–Sur** en toda la zona comercial.
  4. **Oficina Acristalada de Administración y Atención a Proveedores (`X = 6,00..9,00 m, Y = 0,15..3,50 m = 10,05 m²`):**
     * Cerramiento estilo industrial-chalet en madera, hierro negro y **vidrio transparente** hacia el salón comercial (`Y = 3,50..3,65 m` y `X = 5,85..6,00 m`), brindando supervisión visual completa de las cajas e islas desde el escritorio gerencial, con luz y brisa natural de esquina (`Este + Sur`).

---

## 8. Hoja de Ruta al Aprobar
1. Actualizar [`build_casa_3_pisos.py`](file:///c:/Users/alvar/Documents/casa/04_Scripts_Parametricos/build_casa_3_pisos.py) aplicando las **7 correcciones** tanto en el **modelo 3D** como en las **láminas 2D** (`PLANTA_SOTANO_2D`, `PLANTA_BAJA_2D`, `PLANTA_SEGUNDO_PISO_2D`, `PLANTA_TERCER_PISO_2D`, `PLANTA_TANQUES_2000L_2D` y `FACHADAS_2D`).
2. Regenerar [`casa_proyecto_3_pisos.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_proyecto_3_pisos.dxf) y ejecutar verificación automática de paso libre en puertas, abertura real de claraboya, redistribución comercial de Planta Baja y respeto estricto de linderos (`minX = 0,1500 m`).
