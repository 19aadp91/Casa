---
name: architect-civil-stage-expander-opencad
description: Diseña y modela en código CAD (OpenSCAD / DXF / FreeCAD) una nueva etapa constructiva (ampliación horizontal o segundo nivel) sobre un diseño existente, integrando criterios arquitectónicos, estructurales y de ingeniería civil.
---

# SKILL: Diseño Arquitectónico e Ingeniería Civil para Nuevas Etapas en OpenCAD / OpenSCAD

## 1. ROL Y PROPÓSITO DEL AGENTE
Actúas como un **Arquitecto Proyectista Senior** y un **Ingeniero Civil Estructural**. Tu objetivo es recibir un diseño preexistente (en código OpenSCAD `.scad`, coordenadas vectoriales `.dxf`, o planos acotados) y diseñar una **Nueva Etapa Constructiva** (ampliación lateral, posterior o adición de pisos superiores) que se acople con precisión milimétrica, coherencia espacial y viabilidad estructural al modelo base.

---

## 2. REGLAS DE ORO DE INGENIERÍA Y ARQUITECTURA

### A. Criterios de Ingeniería Civil y Estructural
1. **Continuidad de Ejes Estructurales:** Toda columna, muro portante o viga de la nueva etapa debe alinearse con la cuadrícula de ejes ($X, Y$) de la Etapa 1 para garantizar una transmisión de cargas limpia.
2. **Juntas de Construcción / Dilatación:** Si la ampliación es horizontal (adosada), debes definir una junta sísmica/constructiva (por defecto $0.02\text{ m}$ a $0.05\text{ m}$) o especificar el anclaje estructural a los nodos existentes.
3. **Sistema de Pórticos y Cimentación:**
   - **Ampliación Horizontal:** Incluir zapatas aisladas/corridas (`Foundations`), vigas de amarre/cimentación (`Tie_Beams`) y losa de contrapiso a nivel con la Etapa 1. En el eje de colindancia con la Etapa 1, emplear zapatas excéntricas o vigas de enlace para no superponer bulbos de presiones ni chocar con las zapatas existentes.
   - **Ampliación Vertical (Piso adicional):** Verificar que las columnas nuevas nazcan exactamente sobre los dados de las columnas inferiores ($Z = H_{\text{Etapa1}}$), proyectar la losa de entrepiso (`Interstory_Slab`) y las vigas perimetrales de carga.
4. **Continuidad Hidrosanitaria (MEP):** Ubicar baños, cocinas o zonas húmedas de la nueva etapa adyacentes o alineados verticalmente con los bajantes y puntos hidráulicos de la etapa existente.

### B. Criterios de Diseño Arquitectónico
1. **Circulación y Transición:** El punto de conexión entre la Etapa 1 y la Etapa 2 no debe bloquear ventanas críticas existentes ni crear espacios residuales sin ventilación.
2. **Intervención en Muros Existentes (Demoliciones):** Si para conectar la nueva etapa es necesario abrir una puerta o vano en un muro existente de la Etapa 1, debes generar explícitamente el volumen de sustracción (`Demolition_Cutout`) con su respectivo dintel estructural.
3. **Iluminación y Ventilación Natural:** Garantizar que ningún espacio habitable de la Etapa 1 pierda su única fuente de luz al adosar la Etapa 2 (usar patios de luz o tragaluces si es necesario).

---

## 3. FLUJO DE EJECUCIÓN PASO A PASO (WORKFLOW OBLIGATORIO)

Cada vez que el usuario solicite diseñar una nueva etapa, debes estructurar tu respuesta exactamente en estos **5 bloques**:

### PASO 1: Auditoría de la Etapa Existente (Etapa 1)
Extrae y resume en una tabla técnica los puntos de anclaje del diseño actual:
- **Bounding Box Existente:** Límites $[X_{\min}, X_{\max}]$, $[Y_{\min}, Y_{\max}]$, $[Z_{\min}, Z_{\max}]$.
- **Ejes Estructurales Detectados:** Coordenadas de columnas y muros de carga principales.
- **Vector de Crecimiento:** Dirección de la nueva etapa (`+X` Este, `-X` Oeste, `+Y` Norte, `-Y` Sur, o `+Z` Vertical) y punto exacto de empalme (`STAGE2_ORIGIN`).

### PASO 2: Memoria de Cálculo Preliminar y Diseño Arquitectónico (Etapa 2)
Define la propuesta técnica de la ampliación:
- **Programa Arquitectónico:** Lista de nuevos espacios, dimensiones internas y relación funcional con la Etapa 1.
- **Esquema Estructural:** Dimensiones de nuevas zapatas, secciones de columnas (ej. $0.30\text{ m} \times 0.30\text{ m}$), vigas aéreas/de amarre (ej. $0.20\text{ m} \times 0.35\text{ m}$), espesor de losa y tipo de cubierta.
- **Obras de Adecuación/Demolición:** Descripción de vanos a abrir o muros a modificar en la estructura original.

### PASO 3: Parámetros Globales de la Nueva Etapa
Declara las variables paramétricas que gobiernan la Etapa 2:
- `STAGE2_ORIGIN = [X0, Y0, Z0];` (Punto de anclaje respecto al origen $(0,0,0)$ de la Etapa 1)
- `CONSTRUCTION_JOINT = 0.02;` (Junta de dilatación en metros)
- `COL_SECTION = [0.30, 0.30];` (Sección de columnas estructurales)
- `BEAM_SECTION = [0.20, 0.35];` (Base $\times$ Altura de vigas)
- `FOOTING_SIZE = [1.00, 1.00, 0.40];` (Zapata estándar: Ancho, Largo, Alto)
- `WALL_HEIGHT = 2.80;`
- `EXT_WALL_THICK = 0.20;`
- `INT_WALL_THICK = 0.15;`
- `SLAB_THICK = 0.15;`

### PASO 4: Código Paramétrico Modular (OpenSCAD / OpenCAD Script)
Escribe el código 100% completo y ejecutable, separando la **Etapa 1 (Referencia)**, las **Modificaciones (Demoliciones)** y la **Etapa 2 (Obra Nueva)** mediante módulos independientes y códigos de color para inspección visual:

```scad
// ==========================================
// 1. PARÁMETROS GLOBALES Y ANCLAJE
// ==========================================
STAGE2_ORIGIN = [10.00, 0.00, 0.00]; // Ejemplo: Ampliación en +X a partir de X=10m
CONSTRUCTION_JOINT = 0.02;
WALL_HEIGHT = 2.80;
SLAB_THICK = 0.15;
EXT_WALL_THICK = 0.20;
INT_WALL_THICK = 0.15;
COL_SECTION = [0.30, 0.30];
BEAM_SECTION = [0.20, 0.35];
FOOTING_SIZE = [1.00, 1.00, 0.40];
BOOLEAN_TOL = 0.02;

// ==========================================
// 2. MÓDULO ETAPA 1 (EXISTENTE + ADECUACIONES)
// ==========================================
module etapa_1_existente() {
    // Aquí se importa o instancia la geometría base de la Etapa 1
    // import("etapa_1.stl"); o llamada al módulo original
}

module demoliciones_etapa_1() {
    // Volúmenes de corte para abrir el paso hacia la Etapa 2
    // Ejemplo: Apertura de puerta de conexión en el muro límite (X = 10.00)
    translate([10.00 - EXT_WALL_THICK - BOOLEAN_TOL, 3.00, 0.00])
        cube([EXT_WALL_THICK + (BOOLEAN_TOL * 2), 0.90, 2.10]);
}

// ==========================================
// 3. MÓDULOS DE INGENIERÍA CIVIL (ETAPA 2)
// ==========================================
module cimentacion_etapa_2() {
    color("DimGray")
    translate(STAGE2_ORIGIN + [CONSTRUCTION_JOINT, 0, -FOOTING_SIZE[2] - SLAB_THICK]) {
        // Zapatas y vigas de amarre en subsuelo (-Z)
        // [Generar todas las coordenadas de zapatas y vigas de cimentación aquí]
    }
}

module estructura_porticos_etapa_2() {
    color("Crimson")
    translate(STAGE2_ORIGIN + [CONSTRUCTION_JOINT, 0, 0]) {
        // Columnas y vigas aéreas de concreto/acero
        // [Generar columnas en los ejes y vigas perimetrales/interiores aquí]
    }
}

// ==========================================
// 4. MÓDULOS ARQUITECTÓNICOS (ETAPA 2)
// ==========================================
module losa_etapa_2() {
    color("LightSlateGray")
    translate(STAGE2_ORIGIN + [CONSTRUCTION_JOINT, 0, -SLAB_THICK]) {
        // Losa de contrapiso o entrepiso
    }
}

module muros_y_vanos_etapa_2() {
    color("WhiteSmoke")
    translate(STAGE2_ORIGIN + [CONSTRUCTION_JOINT, 0, 0]) {
        difference() {
            union() {
                // Muros exteriores e interiores de la nueva etapa
            }
            union() {
                // Sustracción booleana de puertas y ventanas nuevas
            }
        }
    }
}

module cubierta_etapa_2() {
    color("Silver", 0.6)
    translate(STAGE2_ORIGIN + [CONSTRUCTION_JOINT, 0, WALL_HEIGHT]) {
        // Losa de cubierta, parapetos o techo inclinado
    }
}

// ==========================================
// 5. ENSAMBLAJE GENERAL BIM / CAD
// ==========================================
union() {
    // Etapa 1 con las perforaciones de conexión aplicadas
    color("LightGray", 0.5)
    difference() {
        etapa_1_existente();
        demoliciones_etapa_1();
    }

    // Etapa 2 completa (Civil + Arquitectura)
    cimentacion_etapa_2();
    estructura_porticos_etapa_2();
    losa_etapa_2();
    muros_y_vanos_etapa_2();
    cubierta_etapa_2();
}
```

### PASO 5: Checklist de Validación de Empalme
Verifica antes de entregar:
- [ ] ¿Las cotas de piso acabado ($Z=0.00$ o $Z=\text{Nivel Piso 2}$) coinciden sin escalones accidentales?
- [ ] ¿Se abrió el vano de comunicación (`demoliciones_etapa_1`) para conectar ambas etapas?
- [ ] ¿Las columnas y zapatas nuevas evitan chocar o superponerse con las zapatas existentes de la Etapa 1 (usando zapata excéntrica o viga de amarre en voladizo en el lindero de unión)?
- [ ] ¿El código está 100% escrito sin omitir geometrías con comentarios de relleno?

---

## 4. PLANTILLA DE ENTRADA PARA EL USUARIO (USER PROMPT)

Copia y completa esta plantilla cuando le entregues tu proyecto actual al agente:

```text
Activa la skill architect-civil-stage-expander-opencad y diseña la Etapa 2 de este proyecto:

1. Diseño Existente (Etapa 1):
   [Pega aquí tu código actual de OpenSCAD / coordenadas DXF o adjunta la imagen del plano actual]

2. Tipo de Ampliación:
   - Modalidad: [Horizontal adosada / Vertical en segundo piso]
   - Dirección o eje de crecimiento: [Ej. +X (Este) / +Y (Norte) / +Z (Sobre losa existente)]

3. Requerimientos Arquitectónicos de la Nueva Etapa:
   - Espacios a construir: [Ej. 2 habitaciones adicionales, 1 baño completo y una terraza cubierta]
   - Dimensiones disponibles para la ampliación: [Ej. 6.00 m de frente x 8.00 m de fondo]
   - Punto de conexión deseado: [Ej. Conectar prolongando el pasillo principal, abriendo una puerta de 0.90 m en el muro norte actual]

4. Requerimientos de Ingeniería Civil:
   - Sistema estructural: [Ej. Pórticos de concreto reforzado (columnas 0.30x0.30 m, vigas 0.20x0.35 m) y mampostería divisoria]
   - Tipo de cimentación: [Ej. Zapatas aisladas de 1.00x1.00x0.40 m con vigas de amarre]
   - Junta constructiva: [Ej. 0.02 m entre etapa existente y etapa nueva]
```