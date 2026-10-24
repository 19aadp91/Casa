// =============================================================================
// PROYECTO CHALET RÚSTICO Y ALPINO V2 - MODELO PARAMÉTRICO CAD
// Archivo: casa_rustico_v2_superior.scad
// Diseño bajo la Skill de Arquitecto Especialista en Estilo Rústico y Chalet para CAD.
// Base estructural: casa_modificaciones.dxf
//
// Innovaciones del Rediseño V2:
// 1. Sin chimenea: Máxima amplitud y pureza espacial en el Gran Salón.
// 2. Doble Balcón Frontal sobre Avenida 4:
//    - Gran Balconada Social Techada (5.05 x 1.60 m) con barandilla Cruz de San Andrés.
//    - Balcón Privado Independiente para la Master Suite (3.55 x 1.60 m).
// 3. Ampliación Posterior Rectangular (Sótano a Último Piso):
//    - Crujía posterior derecha cerrada (9.00 x 21.71 m volumetría 100% rectangular).
//    - Sótano: Cava rústica / taller subterráneo (+9.6 m²).
//    - Planta Baja: Despacho comercial privado / archivo (+9.6 m²).
//    - Último Piso: Habitación 4 / Suite invitados / estudio alpino (+9.6 m²).
//    - Columna 32 en (9.075, 0.075) completando la retícula 4x9.
// 4. Preservación Estricta:
//    - Sótano, planta baja comercial (98 m²), garaje (2.80 m libres) y ambas escaleras intactos.
// =============================================================================

$fn = 40;

// --- VARIABLES PARAMÉTRICAS GLOBALES ---
ancho_casa        = 9.00;
largo_casa        = 21.71;
x_min             = 0.15;
x_max             = 9.15;
y_min             = 0.00;
y_max             = 21.71;

z_sot_floor       = -2.55;
z_pb_floor        =  0.00;
h_pb_muro         =  2.85;
z_pa_floor        =  3.00;
h_pa_muro         =  5.85;
z_alero           =  5.40;
z_cumbrera        =  9.72;
x_cumbrera        =  4.65;

alero_voladizo    =  1.10;
pendiente_techo   =  38; // Grados de inclinación alpina

// --- COLORES ARQUITECTÓNICOS ---
c_piedra          = [0.55, 0.58, 0.60]; // Gris piedra natural zócalo
c_madera_muro     = [0.65, 0.45, 0.32]; // Madera cálida machihembrada
c_madera_viga     = [0.35, 0.22, 0.14]; // Madera oscura vigas y canecillos
c_teja_pizarra    = [0.22, 0.26, 0.28]; // Pizarra / teja alpina
c_columna         = [0.82, 0.25, 0.20]; // Columnas estructurales
c_vidrio          = [0.70, 0.90, 0.95, 0.6]; // Ventanales

// =============================================================================
// 1. SÓTANO INTACTO + CAVA POSTERIOR (Z = -2.55 m)
// =============================================================================
module sotano_intacto_con_cava() {
    color(c_piedra) {
        // Losa de piso sótano rectangular
        translate([x_min, y_min, z_sot_floor - 0.15])
            cube([ancho_casa, 8.30, 0.15]);

        // Muros de contención perimetrales (Oeste, Sur, Este y Norte)
        translate([x_min, y_min, z_sot_floor])
            cube([0.15, 8.30, 2.40]);
        translate([x_min, y_min, z_sot_floor])
            cube([ancho_casa, 0.15, 2.40]);
        translate([x_max - 0.15, y_min, z_sot_floor])
            cube([0.15, 8.30, 2.40]);
        translate([x_min, 8.15, z_sot_floor])
            cube([ancho_casa, 0.15, 2.40]);

        // Muro divisorio de la Nueva Cava Subterránea
        translate([6.25, y_min, z_sot_floor])
            cube([0.15, 3.50, 2.40]);
    }
}

// =============================================================================
// 2. PLANTA BAJA: LOCAL COMERCIAL + GARAJE + NUEVO DESPACHO POSTERIOR
// =============================================================================
module planta_baja_comercial_con_despacho() {
    color(c_piedra) {
        // Losa Planta Baja 100% rectangular
        translate([x_min, y_min, -0.15])
            cube([ancho_casa, largo_casa, 0.15]);

        // Muro propio Eje 0 (Oeste)
        translate([x_min, y_min, 0])
            cube([0.15, largo_casa, h_pb_muro]);

        // Muro divisorio Garaje Eje 1 (2.80 m libres)
        translate([2.75, y_min, 0])
            cube([0.15, largo_casa - 0.15, h_pb_muro]);

        // Muro Este Eje 3 completo rectangular
        translate([x_max - 0.15, y_min, 0])
            cube([0.15, largo_casa, h_pb_muro]);

        // Muro Sur Posterior completo
        translate([x_min, y_min, 0])
            cube([ancho_casa, 0.15, h_pb_muro]);

        // Muro divisorio del Nuevo Despacho Comercial Posterior
        translate([6.25, 3.50, 0])
            cube([2.75, 0.15, h_pb_muro]);
        translate([6.25, y_min, 0])
            cube([0.15, 3.50, h_pb_muro]);

        // Fachada comercial Avenida 4 con vanos de vitrinas y portón
        difference() {
            translate([x_min, y_max - 0.15, 0])
                cube([ancho_casa, 0.15, h_pb_muro]);
            // Portón garaje
            translate([0.40, y_max - 0.20, 0])
                cube([2.25, 0.30, 2.25]);
            // Vitrina 1
            translate([3.15, y_max - 0.20, 0])
                cube([2.50, 0.30, 2.40]);
            // Vitrina 2
            translate([6.20, y_max - 0.20, 0])
                cube([2.60, 0.30, 2.40]);
        }
    }
}

// =============================================================================
// 3. ESCALERAS INTACTAS
// =============================================================================
module escaleras_intactas() {
    color([0.40, 0.40, 0.40]) {
        // Tramo 1: Baja a sótano (X: 0.30..1.40, Y: 4.45..7.40)
        for (i = [0:11]) {
            translate([0.30, 7.40 - (i+1)*(2.95/12), z_sot_floor])
                cube([1.10, 2.95/12, (12-i)*(2.55/12)]);
        }
        // Tramo 2: Sube a planta alta (X: 1.55..2.65, Y: 4.40..7.35)
        for (i = [0:11]) {
            translate([1.55, 4.40 + i*(2.95/12), 0])
                cube([1.10, 2.95/12, (i+1)*(3.00/12)]);
        }
    }
}

// =============================================================================
// 4. RETÍCULA MODULAR DE 32 COLUMNAS (31 ORIGINALES + COLUMNA 32)
// =============================================================================
module reticula_columnas_32() {
    cols = [
        [0.275, 21.585], [2.825, 21.585], [5.925, 21.585], [9.075, 21.585],
        [0.275, 18.575], [2.825, 18.575], [5.925, 18.575], [9.075, 18.575],
        [0.275, 16.325], [2.825, 16.325], [5.925, 16.325],
        [9.075, 14.625],
        [0.275, 12.025], [2.825, 12.025], [5.925, 12.025], [9.075, 12.025],
        [0.275, 8.875],  [2.825, 8.875],  [5.925, 8.875],  [9.075, 8.875],
        [0.275, 6.575],  [2.825, 6.575],  [5.925, 6.575],  [9.075, 6.575],
        [0.275, 3.575],  [2.825, 3.575],  [5.925, 3.575],  [9.075, 3.575],
        [0.275, 0.075],  [2.825, 0.075],  [5.925, 0.075],  [9.075, 0.075] // Columna 32
    ];

    color(c_columna) {
        // En Planta Baja
        for (c = cols) {
            translate([c[0] - 0.125, c[1] - 0.125, 0])
                cube([0.25, 0.25, h_pb_muro]);
        }
        // En Planta Alta (Postes de madera vista)
        for (c = cols) {
            translate([c[0] - 0.125, c[1] - 0.125, z_pa_floor])
                cube([0.25, 0.25, h_pa_muro - z_pa_floor]);
        }
        // En Sótano (35x35 cm)
        for (cx = [0.275, 2.825, 5.925, 9.075]) {
            for (cy = [0.075, 3.575, 6.575]) {
                translate([cx - 0.175, cy - 0.175, z_sot_floor])
                    cube([0.35, 0.35, -z_sot_floor - 0.15]);
            }
        }
    }
}

// =============================================================================
// 5. PLANTA ALTA: RESIDENCIA CHALET RÚSTICO V2 (SIN CHIMENEA)
// =============================================================================
module planta_alta_chalet_v2() {
    color(c_madera_muro) {
        // Muros perimetrales en madera machihembrada
        difference() {
            translate([x_min, y_min, z_pa_floor])
                cube([ancho_casa, largo_casa, h_pa_muro - z_pa_floor]);

            // Vacío interior general
            translate([x_min + 0.18, y_min + 0.18, z_pa_floor - 0.05])
                cube([ancho_casa - 0.36, largo_casa - 0.36, h_pa_muro - z_pa_floor + 0.10]);

            // Hueco salida a Balcón Social (Gran Salón)
            translate([2.60, y_max - 0.25, z_pa_floor])
                cube([1.80, 0.50, 2.30]);

            // Hueco salida a Balcón Privado (Master Suite)
            translate([6.80, y_max - 0.25, z_pa_floor])
                cube([1.60, 0.50, 2.30]);

            // Ventanales con contraventanas
            translate([x_max - 0.25, 1.00, z_pa_floor + 1.00])
                cube([0.50, 1.60, 1.10]); // Habitación 4 Posterior
            translate([x_max - 0.25, 6.50, z_pa_floor + 1.00])
                cube([0.50, 1.70, 1.10]); // Habitación 3
            translate([x_max - 0.25, 16.50, z_pa_floor + 1.00])
                cube([0.50, 1.80, 1.10]); // Master Suite lateral
        }

        // Muros interiores (Zona Social vs Íntima, Habitaciones y Baños)
        translate([5.20, 3.50, z_pa_floor])
            cube([0.15, largo_casa - 3.65, h_pa_muro - z_pa_floor]); // Divisorio longitudinal

        translate([5.35, 15.00, z_pa_floor])
            cube([3.65, 0.15, h_pa_muro - z_pa_floor]); // Master suite sur

        translate([5.35, 8.85, z_pa_floor])
            cube([3.65, 0.15, h_pa_muro - z_pa_floor]); // Hab 3 sur

        // NUEVA HABITACIÓN 4 POSTERIOR
        translate([5.35, 3.50, z_pa_floor])
            cube([3.65, 0.15, h_pa_muro - z_pa_floor]); // Hab 4 norte
    }

    // Isla de roble en cocina alpina
    color(c_madera_viga) {
        translate([1.80, 10.80, z_pa_floor])
            cube([2.60, 0.95, 0.90]);
    }
}

// =============================================================================
// 6. DOBLE BALCÓN FRONTAL INDEPENDIENTE SOBRE AVENIDA 4
// =============================================================================
module doble_balcon_frontal() {
    // 1. Gran Balconada Social Techada (X: 0.15 a 5.20 m)
    color(c_madera_viga) {
        translate([x_min, y_max, z_pa_floor - 0.15])
            cube([5.05, 1.60, 0.15]); // Losa madera

        // Barandilla frontal social (Cruz de San Andrés)
        translate([x_min, y_max + 1.55, z_pa_floor])
            cube([5.05, 0.05, 1.05]);
        translate([x_min, y_max, z_pa_floor])
            cube([0.05, 1.60, 1.05]);

        // Vigas pasantes de soporte
        for (vx = [0.40, 1.60, 2.80, 4.00, 5.10]) {
            translate([vx - 0.08, y_max - 0.60, z_pa_floor - 0.35])
                cube([0.16, 2.20, 0.20]);
        }
    }

    // 2. Balcón Privado Independiente Master Suite (X: 5.60 a 9.15 m)
    color(c_madera_viga) {
        translate([5.60, y_max, z_pa_floor - 0.15])
            cube([3.55, 1.60, 0.15]); // Losa madera

        // Barandilla frontal Master Suite
        translate([5.60, y_max + 1.55, z_pa_floor])
            cube([3.55, 0.05, 1.05]);
        translate([x_max - 0.05, y_max, z_pa_floor])
            cube([0.05, 1.60, 1.05]);

        // Vigas pasantes de soporte Master Suite
        for (vx = [5.80, 6.90, 8.00, 9.05]) {
            translate([vx - 0.08, y_max - 0.60, z_pa_floor - 0.35])
                cube([0.16, 2.20, 0.20]);
        }
    }

    // Celosía divisoria de madera maciza entre ambos balcones
    color(c_madera_muro) {
        translate([5.20, y_max, z_pa_floor])
            cube([0.40, 1.60, 1.80]);
    }
}

// =============================================================================
// 7. CUBIERTA ALPINA A DOS AGUAS (38° PENDIENTE, ALEROS Y CANECILLOS)
// =============================================================================
module cubierta_alpina_38() {
    color(c_teja_pizarra) {
        // Faldón Oeste
        polyhedron(
            points = [
                [-0.95, -1.10, z_alero], [4.65, -1.10, z_cumbrera],
                [4.65, 23.31, z_cumbrera], [-0.95, 23.31, z_alero],
                [-0.95, -1.10, z_alero + 0.20], [4.65, -1.10, z_cumbrera + 0.20],
                [4.65, 23.31, z_cumbrera + 0.20], [-0.95, 23.31, z_alero + 0.20]
            ],
            faces = [
                [0,1,2,3], [4,7,6,5], [0,4,5,1], [1,5,6,2], [2,6,7,3], [3,7,4,0]
            ]
        );

        // Faldón Este
        polyhedron(
            points = [
                [4.65, -1.10, z_cumbrera], [10.25, -1.10, z_alero],
                [10.25, 23.31, z_alero], [4.65, 23.31, z_cumbrera],
                [4.65, -1.10, z_cumbrera + 0.20], [10.25, -1.10, z_alero + 0.20],
                [10.25, 23.31, z_alero + 0.20], [4.65, 23.31, z_cumbrera + 0.20]
            ],
            faces = [
                [0,1,2,3], [4,7,6,5], [0,4,5,1], [1,5,6,2], [2,6,7,3], [3,7,4,0]
            ]
        );
    }

    // Canecillos expuestos bajo el alero
    color(c_madera_viga) {
        for (i = [0:20]) {
            cy = -1.10 + i * (24.41 / 20);
            translate([-0.95, cy - 0.06, z_alero - 0.18])
                cube([1.30, 0.12, 0.18]);
            translate([8.95, cy - 0.06, z_alero - 0.18])
                cube([1.30, 0.12, 0.18]);
        }
    }
}

// =============================================================================
// ENSAMBLAJE GENERAL DEL CHALET RÚSTICO V2
// =============================================================================
module casa_rustico_v2_completa() {
    sotano_intacto_con_cava();
    planta_baja_comercial_con_despacho();
    escaleras_intactas();
    reticula_columnas_32();
    planta_alta_chalet_v2();
    doble_balcon_frontal();
    cubierta_alpina_38();
}

casa_rustico_v2_completa();
