# Proyecto Arquitectónico - Vivienda Unifamiliar y Comercial
**Municipio Independencia, Estado Yaracuy, Venezuela**

Modelo arquitectónico 2D/3D, estructural y topográfico generado con **100% de fidelidad geométrica** a partir de las 5 láminas originales de [`01_Planos_y_Documentacion/planos de casa.pdf`](file:///c:/Users/alvar/Documents/casa/01_Planos_y_Documentacion/planos%20de%20casa.pdf), incluyendo además la versión optimizada con ampliación al frente comercial y redistribución de plantas.

---

## 📁 Estructura del Repositorio

```text
casa/
│
├── 01_Planos_y_Documentacion/
│   ├── planos de casa.pdf                     # Planos originales escaneados (Plantas, Estructura, Fachadas, Linderos UTM)
│   ├── planos_casa_completo.pdf               # NUEVO PDF oficial estilo municipal con información completa de casa_completo (5 láminas)
│   ├── prompt_arquitecto_virtual_cadcraft.md  # Instrucciones y directrices del Arquitecto Virtual
│   └── skill_ampliaci_n_arquitectura_e_ingenier_a_civil_opencad.md # Skill especializada OpenCAD/CADCraft
│
├── 02_Modelos_CAD/
│   ├── casa_fiel_pdf.dxf                      # Modelo 2D/3D fiel 100% al PDF original (Láminas 1-5)
│   ├── casa_fiel_pdf_respaldo.dxf             # Respaldo intacto del diseño original
│   ├── casa_completo.dxf                      # Modelo integral actualizado (Sótano + Local Comercial + Apto 2do Piso)
│   ├── casa_modificaciones.dxf                 # Modelo con las modificaciones de distribución y estructura
│   └── casa.dxf                               # Sincronización CAD estándar
│
├── 03_Modelos_3D/
│   ├── casa_3d.obj                            # Modelo 3D poligonal completo con terreno escalonado y niveles
│   ├── casa_3d.stl                            # Malla sólida 3D para impresión 3D / análisis BIM / CAD
│   ├── casa_3d.skp                            # Modelo 3D compatible con SketchUp
│   └── casa_primer_piso.scad                  # Código paramétrico sólido para OpenSCAD
│
├── 04_Scripts_Parametricos/
│   ├── generate_pdf_planos.py                 # Generador vectorial del PDF arquitectónico oficial (5 láminas completas)
│   ├── build_complete_project.py              # Script maestro generador DXF 2D/3D, OBJ y STL (Ezdxf + Numpy)
│   ├── build_complete_project_respaldo.py     # Script respaldo del levantamiento original
│   ├── build_casa_completa.py                 # Generador paramétrico base
│   ├── export_3d_formats.py                   # Motor de exportación 3D (OBJ, STL, Wavefront)
│   ├── build_dxf.py                           # Utilidades de generación de entidades DXF
│   └── casa_primer_piso.py                    # Script CadQuery / OpenCASCADE
│
├── 05_Software/
│   └── README.md                              # Documentación y enlaces de OpenCADStudio v2026.42
│
├── .gitignore                                 # Exclusiones de binarios pesados (>100MB) y temporales CAD
└── README.md                                  # Especificaciones completas del proyecto
```

---

## 📐 Especificaciones de Ingeniería y Topografía

* **Propietario:** Alvaro Argelio Diaz Florez (C.I.: 24.633.787)
* **Ubicación:** Avenida 4 entre calles 30 y 31, N° 30-7, Municipio Independencia, Estado Yaracuy.
* **Profesional responsable:** T.S.U. Angel Camacaro M. (CVPT: N° 1260 / SOVIT: N° 0050).
* **Área del Terreno:** $273{,}81\text{ m}^2$ (Polígono P-1, P-2, P-3, P-4 con coordenadas U.T.M. REGVEN/WGS84).
* **Topografía y Desniveles:** 5 niveles de terreno escalonado con talud natural en fachada lateral izquierda ($Z = 0{,}00\text{ m}$ en Av. 4 hasta $Z = -2{,}55\text{ m}$ en patio posterior).

---

## 🏗️ Distribución Arquitectónica

### 1. Sótano ($Z = -2{,}55\text{ m}$)
- 6 columnas estructurales principales de $35 \times 35\text{ cm}$.
- Muros de contención perimetrales contra talud de terreno.
- Altura libre de $2{,}40\text{ m}$ ($5{,}63\text{ m}$ cota de coronación posterior).

### 2. Primer Piso / Planta Baja ($Z = 0{,}00\text{ m}$) - Comercial
- **Ampliación frontal hasta Avenida 4:** Eje A0 integrado ($Y = 21{,}71\text{ m}$).
- **Muro y columnas propias a la izquierda (Eje 0):** Estructura independiente respetando la medianera vecina.
- **Local Comercial Abierto:** Área amplia de $\approx 98\text{ m}^2$ para uso comercial / ventas / showroom.
- **Garaje Techado Doble:** $2{,}45\text{ m} \times 12{,}76\text{ m}$ con capacidad para dos vehículos y circulación privada.
- **Acceso independiente:** Conexión directa y privada hacia la caja de escaleras hacia la planta alta.

### 3. Segundo Piso ($Z = +3{,}00\text{ m}$) - Apartamento Residencial
- **Habitación Principal (Master Suite):** Baño privado y ventanal/balcón techado hacia la Avenida 4.
- **Habitaciones 2 y 3:** Closets integrados y ventilación cruzada hacia linderos.
- **Baño Compartido:** Completo, ubicado entre las habitaciones secundarias y el área social.
- **Área Social Abierta:** Sala - Comedor de concepto abierto con vistas a la Avenida 4.
- **Cocina Integral:** Con isla central de $2{,}60\text{ m} \times 0{,}95\text{ m}$.
- **Lavadero y Terraza Posterior:** Vista hacia el patio posterior y la serranía.

---

## 🏔️ Proyecto Chalet Rústico y Alpino (Timber Frame & Zócalo de Piedra)

Diseñado e implementado bajo la **Skill de Arquitecto Especialista en Estilo Rústico y Chalet para CAD (OpenSCAD / OpenCAD)**. Mantiene intactos los modelos base (`casa_modificaciones.dxf` y `casa_completo.dxf`) y crea una propuesta arquitectónica de alta montaña totalmente independiente en [`Proyecto_Chalet_Rustico/`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/) y [`c:\Users\alvar\Documents\casa_chalet`](file:///c:/Users/alvar/Documents/casa_chalet).

### 📐 Características Principales del Chalet:
1. **Garaje Confortable con Apertura Cómoda de Puertas:**
   - Crujía de garaje ampliada a **$2{,}80\text{ m}$ libres** ($X = 0{,}30\text{ a }3{,}10\text{ m}$).
   - Holgura lateral de **$0{,}85\text{ m}$** que permite la apertura total de las puertas del conductor sin riesgo de impacto.
2. **Zócalo de Mampostería Rústica en Planta Baja:**
   - Muros gruesos con acabado de piedra natural y esquisto de $0{,}35\text{ m}$ de espesor.
   - Local comercial diáfano de **$91{,}00\text{ m}^2$** con vitrinas rústicas con parteluces de roble.
3. **Cuerpo Superior Ligero (Timber Frame / Machihembrado):**
   - Estructura entramada de madera a la vista en segundo piso.
   - **Great Room (Gran Salón):** Techo catedral con vigas vistas a doble altura y **Chimenea Monumental de Piedra**.
   - **Cocina Rústica de Montaña:** Con isla central de roble macizo ($2{,}60 \times 0{,}95\text{ m}$).
   - **Master Suite Alpina:** Con baño privado de piedra, vestidor y salida directa a la balconada.
   - **Gran Balcón Corrido Alpino ($9{,}00 \times 1{,}60\text{ m}$):** Voladizo frontal hacia la Avenida 4 sostenido por vigas pasantes y barandilla artesanal con **Cruces de San Andrés**.
   - **Habitaciones 2 y 3:** Techos inclinados con vigas vistas y contraventanas exteriores (*shutters*).
4. **Cubierta Alpina a Dos Aguas (Gable Roof 38° / 78%):**
   - Altura de cumbrera alcanzando los **$Z = +9{,}72\text{ m}$**.
   - **Aleros generosos:** Voladizos de $1{,}10\text{ m}$ laterales y $1{,}20\text{ m}$ frontales.
   - **Canecillos y pares expuestos:** Vigas pasantes (*rafter tails*) a la vista cada $0{,}60\text{ m}$.
   - Remate de chimenea de piedra con losa de pizarra protectora en cubierta.

### 📦 Archivos del Proyecto Chalet:
* **Planos Municipales en PDF (5 Láminas Tabloid 11x17 in):** [`Proyecto_Chalet_Rustico/01_Planos_y_Documentacion/planos_casa_chalet.pdf`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/01_Planos_y_Documentacion/planos_casa_chalet.pdf)
* **Código Paramétrico OpenSCAD / OpenCAD:** [`Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_superior.scad`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_superior.scad)
* **Modelo 2D/3D CAD:** [`Proyecto_Chalet_Rustico/02_Modelos_CAD/casa_chalet_rustico.dxf`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/02_Modelos_CAD/casa_chalet_rustico.dxf)
* **Mallas 3D Poligonales:** [`Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_3d.obj`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_3d.obj) y [`casa_chalet_3d.stl`](file:///c:/Users/alvar/Documents/casa/Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_3d.stl) (147 sólidos independientes).
* **Carpeta Independiente Standalone:** [`c:\Users\alvar\Documents\casa_chalet`](file:///c:/Users/alvar/Documents/casa_chalet)

---

## 🏔️ Proyecto Chalet Rústico Alpino V2 (`casa_rustico_v2.dxf`)

Evolución del diseño rústico basada estrictamente en [`02_Modelos_CAD/casa_modificaciones.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_modificaciones.dxf) y perfeccionada bajo la **Skill de Arquitecto Especialista en Estilo Rústico y Chalet para CAD (OpenSCAD / OpenCAD)**, respondiendo a las correcciones programáticas y formales del usuario:

### 📐 Innovaciones y Características del Rediseño V2:
1. **Supresión Total de la Chimenea:**
   - Se elimina la chimenea de piedra en el salón y la cubierta, logrando un **Gran Salón Rústico (Great Room)** 100% diáfano, despejado y bañado por luz natural, sin obstáculos estructurales interiores.
2. **Doble Balcón Frontal Independiente sobre Avenida 4:**
   - **Gran Balconada Rústica Techada Corrida ($5{,}05 \times 1{,}60\text{ m}$):** Acceso directo y exclusivo desde el Gran Salón y comedor, con vigas pasantes vistas, barandilla artesanal con Cruz de San Andrés y alero voladizo protector.
   - **Balcón Privado Independiente de la Master Suite ($3{,}55 \times 1{,}60\text{ m}$):** Acceso íntimo y privado exclusivamente desde el dormitorio principal, separado de la balconada social por una celosía de madera maciza.
3. **Ampliación Posterior Continua hacia Volumetría 100% Rectangular ($9{,}00 \times 21{,}71\text{ m}$):**
   - Se cierra la hendidura original ($X \in [6{,}25, 9{,}15\text{ m}], Y \in [0{,}00, 3{,}50\text{ m}]$) desde el sótano hasta el último piso:
     - **Sótano ($Z = -2{,}55\text{ m}$):** Nueva **Cava Rústica / Taller Subterráneo** ($+9{,}6\text{ m}^2$) rodeada de muros de contención.
     - **Planta Baja ($Z = 0{,}00\text{ m}$):** Nuevo **Despacho Comercial Privado / Archivo** ($+9{,}6\text{ m}^2$) conectado al local.
     - **Último Piso ($Z = +3{,}00\text{ m}$):** **NUEVA Habitación 4 / Suite de Invitados / Estudio Alpino** ($3{,}80 \times 3{,}50\text{ m}$), completando 4 habitaciones completas en planta alta.
   - **Columna 32 en $(9{,}075, 0{,}075)$:** Completa una retícula estructural modular simétrica y ortogonal de $4 \times 9$ columnas en todos los niveles.
4. **Preservación Rigurosa:**
   - Sótano original, muros de retención y 8 columnas de $35 \times 35\text{ cm}$ intactos.
   - Gran salón comercial de $98\text{ m}^2$, garaje techado con $2{,}80\text{ m}$ entre ejes, muro medianero Eje 0 y baño comercial intactos.
   - **Ambas escaleras (bajada y subida) intactas** sin alteración de huellas ni descansos.
   - Retiro de fondo de $3{,}00\text{ m}$ y linderos perimetrales intactos.
5. **Cubierta Alpina a Dos Aguas (38°):**
   - Cumbrera continua limpia a $Z = +9{,}72\text{ m}$ (sin chimenea emergente), aleros voladizos de $1{,}10\text{ a }1{,}20\text{ m}$ y canecillos pasantes vistos cada $1{,}20\text{ m}$.

### 📦 Archivos del Rediseño Rústico V2:
* **Modelo 2D/3D CAD Maestro:** [`02_Modelos_CAD/casa_rustico_v2.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_rustico_v2.dxf)
* **Mallas 3D Poligonales:** [`03_Modelos_3D/casa_rustico_v2_3d.obj`](file:///c:/Users/alvar/Documents/casa/03_Modelos_3D/casa_rustico_v2_3d.obj) y [`03_Modelos_3D/casa_rustico_v2_3d.stl`](file:///c:/Users/alvar/Documents/casa/03_Modelos_3D/casa_rustico_v2_3d.stl) (336 sólidos constructivos independientes).
* **Código Paramétrico OpenSCAD / OpenCAD:** [`03_Modelos_3D/casa_rustico_v2_superior.scad`](file:///c:/Users/alvar/Documents/casa/03_Modelos_3D/casa_rustico_v2_superior.scad)
* **Script Constructor Automatizado:** [`04_Scripts_Parametricos/build_casa_rustico_v2.py`](file:///c:/Users/alvar/Documents/casa/04_Scripts_Parametricos/build_casa_rustico_v2.py)
* **Plan Arquitectónico Aprobado:** [`plan_rediseño_rustico_v2.md`](file:///C:/Users/alvar/.gemini/antigravity/brain/de3be93c-f4e5-4835-b069-ed2b2f76d657/plan_redise%C3%B1o_rustico_v2.md)

---

## 🏛️ Proyecto Villa Mediterránea (Vernácula Ibérica, Cicládica y Azotea Solárium)

Diseñado e implementado bajo la **Skill de Arquitecto Especialista en Estilo Mediterráneo para CAD (OpenSCAD / OpenCAD)**. Mantiene intactos al 100% el sótano de fundación, la planta baja comercial con garaje, el contorno perimetral, la caja de escaleras y las **31 columnas fijas** de [`02_Modelos_CAD/casa_modificaciones.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_modificaciones.dxf), concentrando la intervención arquitectónica exclusivamente en el último piso y la cubierta. Disponible en [`Proyecto_Mediterraneo/`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/) y en la carpeta independiente [`c:\Users\alvar\Documents\casa_mediterranea`](file:///c:/Users/alvar/Documents/casa_mediterranea).

### 📐 Características Principales de la Villa Mediterránea:
1. **Preservación Estructural Absoluta:**
   - **Sótano ($Z = -2{,}55\text{ m}$):** 100% intacto con muros de contención y sus 8 columnas de $35 \times 35\text{ cm}$.
   - **Planta Baja Comercial ($Z = 0{,}00\text{ m}$):** $98\text{ m}^2$ de salón comercial, garaje techado ($2{,}80\text{ m}$ entre ejes), muro propio en Eje 0 y baño.
   - **Escaleras:** Tramo 1 (bajada a sótano) y Tramo 2 (subida a P2) en huella y desarrollo intactos.
   - **31 Columnas Fijas:** Distribución idéntica en Planta Baja y Planta Alta sobre Ejes 0, 1, 2, 3 x A0..G.
2. **Loggia Frontal con 3 Arcos de Medio Punto sobre Avenida 4:**
   - Arquería monumental encalada con arcos de $2{,}30\text{ m}$ de luz entre pilastras.
   - Barandilla de forja artesanal y galería sombreada pasiva ($9{,}00 \times 2{,}15\text{ m}$).
3. **Pérgolas de Control Solar (Viguería de Madera y Cañizo):**
   - Pérgola en celosía sobre la loggia frontal y sobre la terraza posterior ($15 \times 8\text{ cm} \text{ @ } 0{,}45\text{ m}$) para tamizar la radiación solar y refrescar la envolvente.
4. **Vanos Abocinados y Masa Térmica:**
   - Ventanas con jambas abocinadas para optimizar la entrada de luz difusa y mitigar el calor.
   - Muros encalados al estuco blanco continuo con aristas suaves.
5. **Distribución Interior Mediterránea:**
   - **Gran Salón Diáfano:** Concepto abierto con conexión directa a la loggia exterior.
   - **Cocina Ibérica Tradicional:** Con isla central de obra encalada ($2{,}60 \times 0{,}95\text{ m}$) y encimera de roble macizo.
   - **Master Suite Mediterránea:** Con baño privado, vestidor y acceso exclusivo a la loggia arqueada.
   - **Habitaciones 2 y 3:** Dormitorios luminosos con vanos abocinados y ventilación cruzada.
   - **Terraza Posterior y Lavandería:** Apergolada con vistas abiertas hacia la serranía.
6. **Cubierta en Azotea Solárium Transitable:**
   - Azotea a la catalana accesible con antepecho perimetral encalado de $1{,}00\text{ m}$ de altura ($Z = +7{,}00\text{ m}$).
   - Pavimento de baldosas de terracota artesanal y bancada cicládica integrada de obra.

### 📦 Archivos del Proyecto Mediterráneo:
* **Planos Municipales en PDF (5 Láminas Tabloid 11x17 in):** [`Proyecto_Mediterraneo/01_Planos_y_Documentacion/planos_casa_mediterranea.pdf`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/01_Planos_y_Documentacion/planos_casa_mediterranea.pdf) (y copia en [`01_Planos_y_Documentacion/planos_casa_mediterranea.pdf`](file:///c:/Users/alvar/Documents/casa/01_Planos_y_Documentacion/planos_casa_mediterranea.pdf))
* **Código Paramétrico OpenSCAD / OpenCAD:** [`Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_superior.scad`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_superior.scad) (y copia en [`03_Modelos_3D/casa_mediterranea_superior.scad`](file:///c:/Users/alvar/Documents/casa/03_Modelos_3D/casa_mediterranea_superior.scad))
* **Modelo 2D/3D CAD:** [`Proyecto_Mediterraneo/02_Modelos_CAD/casa_mediterranea.dxf`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/02_Modelos_CAD/casa_mediterranea.dxf) (y copia en [`02_Modelos_CAD/casa_mediterranea.dxf`](file:///c:/Users/alvar/Documents/casa/02_Modelos_CAD/casa_mediterranea.dxf))
* **Mallas 3D Poligonales:** [`Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_3d.obj`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_3d.obj) y [`casa_mediterranea_3d.stl`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_3d.stl) (314 sólidos constructivos independientes).
* **Script Generador Maestro:** [`Proyecto_Mediterraneo/04_Scripts_Parametricos/build_casa_mediterranea.py`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/04_Scripts_Parametricos/build_casa_mediterranea.py)
* **Script Generador PDF:** [`Proyecto_Mediterraneo/04_Scripts_Parametricos/generate_pdf_mediterraneo.py`](file:///c:/Users/alvar/Documents/casa/Proyecto_Mediterraneo/04_Scripts_Parametricos/generate_pdf_mediterraneo.py)
* **Carpeta Independiente Standalone:** [`c:\Users\alvar\Documents\casa_mediterranea`](file:///c:/Users/alvar/Documents/casa_mediterranea)
