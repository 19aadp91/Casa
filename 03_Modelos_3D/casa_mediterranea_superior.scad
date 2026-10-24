/**
 * @file casa_mediterranea_superior.scad
 * @brief Modelo CAD 3D Paramétrico y Modular - Proyecto Villa Mediterránea
 * @author Arquitecto Senior Especialista en Estilo Mediterráneo para CAD
 *
 * Base estructural: casa_modificaciones.dxf
 * - Sótano intacto (Z = -2.55 m a -0.15 m, con 8 columnas de 35x35 cm).
 * - Planta Baja comercial y garaje intacta (Z = 0.00 m a 2.85 m).
 * - Escaleras intactas en posición y huella (X: 1.40..2.65, Y: 4.40..7.35 m).
 * - 31 Columnas de 25x25 cm preservadas exactamente en sus ejes originales.
 * - Rediseño Mediterráneo del Último Piso:
 *     * Envolvente encalada en blanco puro y aristas suaves.
 *     * Pórtico frontal con arcos de medio punto sobre Avenida 4.
 *     * Pérgolas de viguería de madera natural y cañizo para filtrado solar.
 *     * Vanos abocinados y profundos para confort térmico pasivo.
 *     * Cubierta plana transitable (Azotea Solárium) con antepecho perimetral de 1.00 m.
 */

// ==============================================================================
// 1. CONSTANTES PARAMÉTRICAS GLOBALES
// ==============================================================================
ANCHO_CASA              = 9.15;    // Ancho total exterior (m)
LARGO_CASA              = 21.71;   // Frente extendido hasta Avenida 4 (m)
OFFSET_MURO_PROPIO      = 0.15;    // Separación del muro lindero oeste (m)

ALTURA_SOTANO           = 2.40;    // Altura libre sótano (m)
Z_SOTANO                = -2.55;   // Nivel piso sótano (m)
ALTURA_PB               = 2.85;    // Tope muros Planta Baja (m)
Z_P2                    = 3.00;    // Nivel piso acabado Último Piso (m)
ALTURA_P2               = 2.85;    // Altura muros Último Piso (m)
Z_CUBIERTA              = 5.85;    // Cota nivel losa de azotea (m)
ALTURA_ANTEPECHO        = 1.00;    // Antepecho perimetral de azotea (m)

GROSOR_MURO_MED         = 0.30;    // Muros mediterráneos encalados (m)
GROSOR_TABIQUE          = 0.15;    // Tabiquería interior (m)

RADIO_ARCO              = 1.15;    // Radio arcos de medio punto (m)
LUZ_ARCO                = 2.30;    // Ancho luz libre arco (m)
PASO_PERGOLA            = 0.50;    // Separación entre viguetas de pérgola (m)
SECCION_VIGA            = [0.12, 0.18]; // Ancho x Canto viga madera (m)

EPS                     = 0.05;    // Margen booleano anti-z-fighting (m)
$fn                     = 36;      // Facetas para arcos y cilindros

// ==============================================================================
// 2. FUNCIONES Y MÓDULOS AUXILIARES
// ==============================================================================
module caja_coords(x1, y1, z1, x2, y2, z2) {
    translate([min(x1, x2), min(y1, y2), min(z1, z2)])
        cube([abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)]);
}

// Vano abocinado con derrame inclinado tradicional
module vano_abocinado(ancho, alto, espesor, derrame = 0.08) {
    polyhedron(
        points = [
            // Cara exterior (más estrecha)
            [derrame, 0, derrame],
            [ancho - derrame, 0, derrame],
            [ancho - derrame, 0, alto - derrame],
            [derrame, 0, alto - derrame],
            // Cara interior (abocinada)
            [0, espesor, 0],
            [ancho, espesor, 0],
            [ancho, espesor, alto],
            [0, espesor, alto]
        ],
        faces = [
            [0, 1, 2, 3], // Exterior
            [5, 4, 7, 6], // Interior
            [0, 4, 5, 1], // Umbral inferior
            [1, 5, 6, 2], // Jamba derecha
            [2, 6, 7, 3], // Dintel superior
            [3, 7, 4, 0]  // Jamba izquierda
        ]
    );
}

// Arco de medio punto para pórticos
module arco_medio_punto(luz, altura_arranque, fondo) {
    radio = luz / 2;
    union() {
        // Vano inferior rectangular
        cube([luz, fondo, altura_arranque]);
        // Medio cilindro superior
        translate([radio, fondo, altura_arranque])
            rotate([90, 0, 0])
                cylinder(r = radio, h = fondo);
    }
}

// ==============================================================================
// 3. SÓTANO (100% INTACTO Y PRESERVADO DE CASA_MODIFICACIONES)
// ==============================================================================
module sotano_intacto() {
    color([0.65, 0.65, 0.65])
    difference() {
        union() {
            // Losa inferior sótano
            caja_coords(0.15, 0.00, -2.70, 6.40, 3.50, Z_SOTANO);
            caja_coords(0.15, 3.50, -2.70, 9.15, 8.30, Z_SOTANO);
            // Muros perimetrales y de contención
            caja_coords(0.15, 0.00, Z_SOTANO, 0.30, 8.30, -0.15);
            caja_coords(0.30, 0.00, Z_SOTANO, 6.40, 0.15, -0.15);
            caja_coords(6.25, 0.15, Z_SOTANO, 6.40, 3.50, -0.15);
            caja_coords(6.00, 3.50, Z_SOTANO, 9.15, 3.65, -0.15);
            caja_coords(8.95, 3.65, Z_SOTANO, 9.15, 8.30, -0.15);
            caja_coords(0.30, 8.15, Z_SOTANO, 9.15, 8.30, -0.15);
            // Tabiquería interior sótano
            caja_coords(0.30, 3.50, Z_SOTANO, 6.00, 3.65, -0.15);
            caja_coords(2.80, 0.15, Z_SOTANO, 2.95, 3.50, -0.15);
            caja_coords(5.85, 3.65, Z_SOTANO, 6.00, 8.15, -0.15);
            caja_coords(1.40, 4.45, Z_SOTANO, 1.55, 8.15, -0.15);
        }
        // Vanos y puertas de sótano
        caja_coords(0.60, -EPS, Z_SOTANO + 1.00, 2.50, 0.15 + EPS, Z_SOTANO + 2.10);
        caja_coords(3.95, 3.50 - EPS, Z_SOTANO, 4.95, 3.65 + EPS, Z_SOTANO + 2.00);
        caja_coords(7.95, 3.50 - EPS, Z_SOTANO, 8.90, 3.65 + EPS, Z_SOTANO + 2.00);
    }

    // 8 Columnas estructurales de fundación (35x35 cm)
    color([0.80, 0.20, 0.20])
    for (pt = [
        [0.275, 6.575], [2.825, 6.575], [5.925, 6.575], [9.075, 6.575],
        [0.275, 3.575], [2.825, 3.575], [5.925, 3.575], [9.075, 3.575]
    ]) {
        caja_coords(pt[0] - 0.175, pt[1] - 0.175, Z_SOTANO,
                    pt[0] + 0.175, pt[1] + 0.175, -0.15);
    }
}

// ==============================================================================
// 4. PLANTA BAJA: LOCAL COMERCIAL Y GARAJE (100% INTACTOS)
// ==============================================================================
module planta_baja_comercial_intacta() {
    color([0.92, 0.92, 0.92]) // Encalado base
    difference() {
        union() {
            // Losa inferior Planta Baja
            caja_coords(0.15, 0.00, -0.15, 9.15, LARGO_CASA, 0.00);
            // Muro propio oeste Eje 0 (separado del vecino)
            caja_coords(0.15, 0.00, 0.00, 0.30, LARGO_CASA, ALTURA_PB);
            // Muro divisorio Eje 1 (Garaje / Local)
            caja_coords(2.75, 0.15, 0.00, 2.90, LARGO_CASA - 0.15, ALTURA_PB);
            // Muro este lindero derecho (Eje 3)
            caja_coords(9.00, 3.50, 0.00, 9.15, LARGO_CASA, ALTURA_PB);
            // Fachada frontal Avenida 4
            caja_coords(0.15, LARGO_CASA - 0.15, 0.00, 9.15, LARGO_CASA, ALTURA_PB);
            // Cierres posteriores
            caja_coords(0.15, 0.00, 0.00, 6.40, 0.15, ALTURA_PB);
            caja_coords(6.25, 0.00, 0.00, 6.40, 3.50, ALTURA_PB);
            caja_coords(6.25, 3.50, 0.00, 9.15, 3.65, ALTURA_PB);
            // Tabiquería interior (Baño local, depósito)
            caja_coords(0.30, 8.80, 0.00, 2.75, 8.95, ALTURA_PB);
            caja_coords(1.40, 4.40, 0.00, 1.55, 7.35, ALTURA_PB);
            caja_coords(5.85, 3.65, 0.00, 6.00, 5.55, ALTURA_PB);
            caja_coords(5.85, 5.40, 0.00, 9.00, 5.55, ALTURA_PB);
            caja_coords(2.90, 3.50, 0.00, 6.25, 3.65, ALTURA_PB);
        }
        // Portón de garaje y vitrinas comerciales en Avenida 4
        caja_coords(0.40, LARGO_CASA - 0.15 - EPS, -EPS, 2.65, LARGO_CASA + EPS, 2.25);
        caja_coords(3.15, LARGO_CASA - 0.15 - EPS, -EPS, 5.65, LARGO_CASA + EPS, 2.40);
        caja_coords(6.20, LARGO_CASA - 0.15 - EPS, -EPS, 8.80, LARGO_CASA + EPS, 2.40);
        // Puertas interiores
        caja_coords(1.65, 8.80 - EPS, -EPS, 2.55, 8.95 + EPS, 2.10);
        caja_coords(3.95, 5.40 - EPS, -EPS, 4.75, 5.55 + EPS, 2.10);
        caja_coords(4.05, 3.50 - EPS, -EPS, 4.90, 3.65 + EPS, 2.10);
    }
}

// ==============================================================================
// 5. ESCALERAS (100% INTACTAS EN POSICIÓN Y DIMENSIONES)
// ==============================================================================
module escalera_intacta() {
    color([0.40, 0.35, 0.30])
    union() {
        // Tramo 1: Baja al sótano (Y: 7.40 a 4.45, X: 0.30 a 1.40)
        for (i = [0:11]) {
            y_top = 7.40 - i * (2.95 / 12);
            y_bot = y_top - (2.95 / 12);
            z_top = 0.00 - i * (2.55 / 12);
            caja_coords(0.30, y_bot, Z_SOTANO, 1.40, y_top, z_top);
        }
        // Tramo 2: Sube a Planta Alta (Y: 4.40 a 7.35, X: 1.55 a 2.65)
        for (i = [0:11]) {
            y_bot = 4.40 + i * (2.95 / 12);
            y_top = y_bot + (2.95 / 12);
            z_top = 0.00 + (i + 1) * (3.00 / 12);
            caja_coords(1.55, y_bot, 0.00, 2.65, y_top, z_top);
        }
    }
}

// ==============================================================================
// 6. COLUMNAS ESTRUCTURALES FIJAS (PRESERVADAS EXACTAMENTE DONDE ESTÁN)
// ==============================================================================
module columnas_estructurales_fijas() {
    color([0.85, 0.20, 0.20]) // Rojo estructural normativo
    union() {
        cols = [
            [0.275, 21.585], [2.825, 21.585], [5.925, 21.585], [9.075, 21.585], // Eje A0
            [0.275, 18.575], [2.825, 18.575], [5.925, 18.575], [9.075, 18.575], // Eje A
            [0.275, 16.325], [2.825, 16.325], [5.925, 16.325],                  // Eje B
            [9.075, 14.625],                                                      // Eje C
            [0.275, 12.025], [2.825, 12.025], [5.925, 12.025], [9.075, 12.025], // Eje D
            [0.275, 8.875],  [2.825, 8.875],  [5.925, 8.875],  [9.075, 8.875],  // Eje E
            [0.275, 6.575],  [2.825, 6.575],  [5.925, 6.575],  [9.075, 6.575],  // Eje F
            [0.275, 3.575],  [2.825, 3.575],  [5.925, 3.575],  [9.075, 3.575],  // Eje G
            [0.275, 0.075],  [2.825, 0.075],  [5.925, 0.075]                    // Eje Posterior
        ];
        // 31 Columnas en Planta Baja (Z = 0.00 a 2.85 m)
        for (c = cols) {
            caja_coords(c[0] - 0.125, c[1] - 0.125, 0.00,
                        c[0] + 0.125, c[1] + 0.125, ALTURA_PB);
        }
        // 31 Columnas en Planta Alta (Z = 3.00 a 5.85 m)
        for (c = cols) {
            caja_coords(c[0] - 0.125, c[1] - 0.125, Z_P2,
                        c[0] + 0.125, c[1] + 0.125, Z_CUBIERTA);
        }
    }
}

// ==============================================================================
// 7. PÓRTICO FRONTAL CON ARCOS DE MEDIO PUNTO (ESTILO MEDITERRÁNEO)
// ==============================================================================
module portico_arcos_medio_punto() {
    color([0.98, 0.98, 0.96]) // Blanco puro encalado
    difference() {
        // Muro masivo frontal sobre Avenida 4 (Y = 21.41 a 21.71 m, H = 3.00 a 5.85 m)
        caja_coords(0.15, LARGO_CASA - GROSOR_MURO_MED, Z_P2,
                    ANCHO_CASA, LARGO_CASA, Z_CUBIERTA);

        // Arquería de 3 arcos de medio punto sobre pilastras
        // Arco 1 (Salón oeste)
        translate([0.50, LARGO_CASA - GROSOR_MURO_MED - EPS, Z_P2])
            arco_medio_punto(2.30, 1.40, GROSOR_MURO_MED + 2*EPS);

        // Arco 2 (Salón central)
        translate([3.40, LARGO_CASA - GROSOR_MURO_MED - EPS, Z_P2])
            arco_medio_punto(2.30, 1.40, GROSOR_MURO_MED + 2*EPS);

        // Arco 3 (Master suite este)
        translate([6.30, LARGO_CASA - GROSOR_MURO_MED - EPS, Z_P2])
            arco_medio_punto(2.30, 1.40, GROSOR_MURO_MED + 2*EPS);
    }
}

// ==============================================================================
// 8. REDISEÑO DEL ÚLTIMO PISO (VILLA RESIDENCIAL MEDITERRÁNEA)
// ==============================================================================
module planta_alta_mediterranea() {
    color([0.96, 0.96, 0.94]) // Blanco encalado cálido
    difference() {
        union() {
            // Losa de entrepiso
            caja_coords(0.15, 0.00, ALTURA_PB, ANCHO_CASA, LARGO_CASA, Z_P2);

            // Muro lateral oeste (Eje 0) encalado continuo
            caja_coords(0.15, 0.00, Z_P2, 0.30, LARGO_CASA, Z_CUBIERTA);

            // Muro lateral este (Eje 3)
            caja_coords(9.00, 3.50, Z_P2, 9.15, LARGO_CASA, Z_CUBIERTA);

            // Muro frontal interior (separa estancias de la loggia sombreada en Y = 19.71 m)
            caja_coords(0.15, 19.56, Z_P2, ANCHO_CASA, 19.71, Z_CUBIERTA);

            // Muros de cierre posterior
            caja_coords(0.15, 0.00, Z_P2, 6.40, 0.15, Z_CUBIERTA);
            caja_coords(6.25, 0.00, Z_P2, 6.40, 3.50, Z_CUBIERTA);
            caja_coords(6.25, 3.50, Z_P2, 9.15, 3.65, Z_CUBIERTA);

            // Tabiquería interior mediterránea
            // Muro separador Eje 2 (Salón / Dormitorios)
            caja_coords(5.85, 3.65, Z_P2, 6.00, 19.56, Z_CUBIERTA);
            // Master Suite (Vestidor y Baño)
            caja_coords(6.00, 15.20, Z_P2, 9.00, 15.35, Z_CUBIERTA);
            caja_coords(6.80, 12.70, Z_P2, 9.00, 12.85, Z_CUBIERTA);
            caja_coords(6.80, 12.85, Z_P2, 6.95, 15.20, Z_CUBIERTA);
            // Habitación 2
            caja_coords(6.00, 8.85, Z_P2, 9.00, 9.00, Z_CUBIERTA);
            // Baño familiar
            caja_coords(6.00, 5.40, Z_P2, 9.00, 5.55, Z_CUBIERTA);
            // Terraza posterior / Lavandería
            caja_coords(2.75, 0.15, Z_P2, 2.90, 4.30, Z_CUBIERTA);
            caja_coords(0.15, 4.30, Z_P2, 2.90, 4.45, Z_CUBIERTA);
        }

        // Hueco de escalera intacto
        caja_coords(1.50, 4.35, ALTURA_PB - EPS, 2.70, 7.40, Z_P2 + EPS);

        // Vanos abocinados y puertas interiores
        caja_coords(1.20, 19.56 - EPS, Z_P2, 4.80, 19.71 + EPS, Z_P2 + 2.35); // Salón a Loggia
        caja_coords(6.50, 19.56 - EPS, Z_P2, 8.50, 19.71 + EPS, Z_P2 + 2.35); // Suite a Loggia
        caja_coords(3.60, -EPS, Z_P2, 5.40, 0.15 + EPS, Z_P2 + 2.10);          // Terraza posterior
        caja_coords(5.85 - EPS, 6.20, Z_P2, 6.00 + EPS, 7.10, Z_P2 + 2.10);   // Puerta Hab 3
        caja_coords(5.85 - EPS, 9.50, Z_P2, 6.00 + EPS, 10.40, Z_P2 + 2.10);  // Puerta Hab 2
        caja_coords(5.85 - EPS, 15.40, Z_P2, 6.00 + EPS, 16.30, Z_P2 + 2.10); // Puerta Master Suite
    }

    // Isla de obra encalada en Cocina Ibérica (2.60 x 0.95 m)
    color([0.98, 0.98, 0.96])
    caja_coords(2.15, 9.80, Z_P2, 3.10, 12.40, Z_P2 + 0.90);
    // Encimera de madera cálida
    color([0.55, 0.35, 0.18])
    caja_coords(2.10, 9.75, Z_P2 + 0.90, 3.15, 12.45, Z_P2 + 0.95);
}

// ==============================================================================
// 9. PÉRGOLAS DE MADERA Y CONTROL SOLAR (SOLÁRIUM Y TERRAZAS)
// ==============================================================================
module pergola_solarium() {
    color([0.58, 0.38, 0.20]) // Madera marina tratada
    union() {
        // Pérgola sobre Loggia Frontal en Avenida 4 (Y: 19.71 a 21.71 m)
        // Vigas maestras longitudinales
        for (vx = [0.50, 3.40, 6.30, 8.90]) {
            caja_coords(vx - 0.06, 19.60, Z_CUBIERTA,
                        vx + 0.06, LARGO_CASA, Z_CUBIERTA + 0.18);
        }
        // Viguetillas transversales de sombreamiento cada 40 cm
        for (py = [19.70 : PASO_PERGOLA : LARGO_CASA]) {
            caja_coords(0.30, py - 0.04, Z_CUBIERTA + 0.18,
                        ANCHO_CASA - 0.15, py + 0.04, Z_CUBIERTA + 0.28);
        }

        // Pérgola sobre Terraza Posterior (Y: 0.15 a 3.50 m, X: 2.90 a 6.25 m)
        for (py = [0.30 : PASO_PERGOLA : 3.40]) {
            caja_coords(2.90, py - 0.04, Z_CUBIERTA + 0.10,
                        6.25, py + 0.04, Z_CUBIERTA + 0.20);
        }
    }
}

// ==============================================================================
// 10. CUBIERTA PLANA: AZOTEA TRANSITABLE SOLÁRIUM CON ANTEPECHO ENCALADO
// ==============================================================================
module cubierta_azotea_transitable() {
    color([0.96, 0.96, 0.94])
    union() {
        // Losa de cubierta transitable
        caja_coords(0.15, 0.00, Z_CUBIERTA - 0.15, ANCHO_CASA, LARGO_CASA, Z_CUBIERTA);

        // Antepecho perimetral encalado de 1.00 m de altura
        difference() {
            caja_coords(0.15, 0.00, Z_CUBIERTA, ANCHO_CASA, LARGO_CASA, Z_CUBIERTA + ALTURA_ANTEPECHO);
            // Hueco interior de azotea
            caja_coords(0.15 + GROSOR_MURO_MED, 0.00 + GROSOR_MURO_MED, Z_CUBIERTA - EPS,
                        ANCHO_CASA - GROSOR_MURO_MED, LARGO_CASA - GROSOR_MURO_MED, Z_CUBIERTA + ALTURA_ANTEPECHO + EPS);
        }

        // Remate de albardilla suave sobre antepecho
        caja_coords(0.12, -0.03, Z_CUBIERTA + ALTURA_ANTEPECHO,
                    ANCHO_CASA + 0.03, LARGO_CASA + 0.03, Z_CUBIERTA + ALTURA_ANTEPECHO + 0.08);
    }
}

// ==============================================================================
// 11. ENSAMBLAJE MAESTRO: VILLA MEDITERRÁNEA COMPLETA
// ==============================================================================
module casa_mediterranea_completa() {
    // 1. Sótano intacto con fundación y columnas de 35x35 cm
    sotano_intacto();

    // 2. Planta Baja intacta (Local Comercial + Garaje)
    planta_baja_comercial_intacta();

    // 3. Escaleras intactas en huella y desarrollo
    escalera_intacta();

    // 4. 31 Columnas estructurales fijas en sus ejes originales
    columnas_estructurales_fijas();

    // 5. Planta Alta: Villa Residencial Mediterránea
    planta_alta_mediterranea();

    // 6. Pórtico con Arcos de Medio Punto en Avenida 4
    portico_arcos_medio_punto();

    // 7. Pérgolas de viguería de madera para control solar
    pergola_solarium();

    // 8. Azotea Solárium transitable con antepecho encalado
    cubierta_azotea_transitable();
}

// Visualización completa
casa_mediterranea_completa();
