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
