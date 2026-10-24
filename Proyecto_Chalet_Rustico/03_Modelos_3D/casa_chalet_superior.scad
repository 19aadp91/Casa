// ==============================================================================
// PROYECTO: CASA CHALET RÚSTICO Y ALPINO DE ALTA MONTAÑA
// Ubicación: Avenida 4 entre Calles 30 y 31, Municipio Independencia, Yaracuy
// Especialidad: Arquitectura Rústica, Timber Frame y Modelado Paramétrico
// Software: OpenSCAD / OpenCAD (CADCraft)
// ==============================================================================

/* [Parámetros Generales de Parcela y Envolvente] */
ANCHO_CASA              = 9.00;    // Ancho total entre linderos oeste-este (m)
LARGO_CASA              = 21.71;   // Longitud total extendida hasta Avenida 4 (m)
OFFSET_MURO_PROPIO      = 0.15;    // Separación de pared vecina izquierda (m)
GROSOR_MURO_PIEDRA      = 0.30;    // Zócalo de mampostería en Planta Baja (m)
GROSOR_MURO_MADERA      = 0.20;    // Cerramientos exteriores Planta Alta (m)
GROSOR_TABIQUE_INT      = 0.15;    // Tabiquería interior de madera (m)
ALTURA_PB               = 3.00;    // Altura de entrepiso Planta Baja (m)
ALTURA_P2_MUROS         = 2.85;    // Altura de arranque de cubierta en P2 (m)
ALTURA_ENTREPISO        = 0.20;    // Espesor de losa y vigas de entrepiso (m)

/* [Parámetros de la Cubierta Alpina (Gable Roof)] */
ANGULO_TECHO            = 38.0;    // Pendiente alpina pronunciada (grados)
ALERO_FRONTAL           = 1.20;    // Voladizo sobre Avenida 4 (m)
ALERO_LATERAL           = 1.10;    // Voladizo sobre muros laterales este/oeste (m)
ALERO_POSTERIOR         = 1.10;    // Voladizo sobre patio posterior (m)
GROSOR_CUBIERTA         = 0.22;    // Tablero + aislamiento + teja rústica (m)
CUMBRERA_X              = ANCHO_CASA / 2; // Eje longitudinal de cumbrera (4.50 m)

/* [Parámetros de Viguería y Canecillos Vistos (Timber Frame)] */
SECCION_VIGA_X          = 0.12;    // Ancho vigas vistas (m)
SECCION_VIGA_Z          = 0.18;    // Canto vigas vistas (m)
INTEREJE_CANECILLOS     = 0.90;    // Separación entre pares vistos (m)

/* [Parámetros de Balconada Corrida y Barandillas] */
FONDO_BALCON            = 1.60;    // Profundidad de balconada hacia fachada (m)
ALTURA_BARANDILLA       = 1.05;    // Altura reglamentaria barandilla (m)
SECCION_POSTE_BALCON    = 0.14;    // Sección postes de madera (m)

/* [Parámetros de Chimenea Rústica Dominante] */
CHIMENEA_ANCHO_X        = 1.10;    // Ancho transversal de chimenea (m)
CHIMENEA_FONDO_Y        = 0.85;    // Fondo longitudinal de chimenea (m)
CHIMENEA_POS_X          = 4.80;    // Ubicación en Salón (m)
CHIMENEA_POS_Y          = 17.50;   // Ubicación longitudinal (m)

/* [Holgura Booleana Anti-Z-Fighting] */
EPS                     = 0.05;    // Margen para operaciones booleanas limpias (m)

// ==============================================================================
// FUNCIONES AUXILIARES DE MODELADO
// ==============================================================================
module caja_coords(x1, y1, z1, x2, y2, z2) {
    translate([min(x1, x2), min(y1, y2), min(z1, z2)])
        cube([abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)]);
}

// ==============================================================================
// 1. ZÓCALO DE PIEDRA / PLANTA BAJA PESADA (LOCAL COMERCIAL + GARAJE AMPLIADO)
// ==============================================================================
module zocalo_piedra() {
    color([0.45, 0.42, 0.40]) // Color mampostería de piedra natural
    difference() {
        union() {
            // Muro perimetral izquierdo propio (separado del vecino)
            caja_coords(OFFSET_MURO_PROPIO, 0, 0, 
                        OFFSET_MURO_PROPIO + GROSOR_MURO_PIEDRA, LARGO_CASA, ALTURA_PB);

            // Muro perimetral este (lindero derecho)
            caja_coords(ANCHO_CASA - GROSOR_MURO_PIEDRA, 3.50, 0, 
                        ANCHO_CASA, LARGO_CASA, ALTURA_PB);

            // Fachada frontal comercial sobre Avenida 4
            caja_coords(OFFSET_MURO_PROPIO, LARGO_CASA - GROSOR_MURO_PIEDRA, 0, 
                        ANCHO_CASA, LARGO_CASA, ALTURA_PB);

            // Muros de cierre posterior
            caja_coords(OFFSET_MURO_PROPIO, 0, 0, 6.40, GROSOR_MURO_PIEDRA, ALTURA_PB);
            caja_coords(6.40 - GROSOR_MURO_PIEDRA, 0, 0, 6.40, 3.50, ALTURA_PB);
            caja_coords(6.40, 3.50, 0, ANCHO_CASA, 3.50 + GROSOR_MURO_PIEDRA, ALTURA_PB);

            // Muro divisorio estructural entre Garaje y Local Comercial (Eje 1 en X = 2.825 m)
            caja_coords(2.75, 0, 0, 2.90, LARGO_CASA - GROSOR_MURO_PIEDRA, ALTURA_PB);
        }

        // --- VANOS Y HUECOS DE PLANTA BAJA ---
        // Portón de Garaje en Avenida 4 (ancho 2.50 m, alto 2.40 m)
        caja_coords(OFFSET_MURO_PROPIO + 0.15, LARGO_CASA - GROSOR_MURO_PIEDRA - EPS, -EPS,
                    OFFSET_MURO_PROPIO + 2.65, LARGO_CASA + EPS, 2.40);

        // Vitrinas comerciales en Avenida 4 con dintel de piedra
        caja_coords(3.55, LARGO_CASA - GROSOR_MURO_PIEDRA - EPS, -EPS, 5.95, LARGO_CASA + EPS, 2.50);
        caja_coords(6.35, LARGO_CASA - GROSOR_MURO_PIEDRA - EPS, -EPS, 8.65, LARGO_CASA + EPS, 2.50);

        // Puerta privada del garaje a la escalera
        caja_coords(1.65, 8.80 - EPS, -EPS, 2.55, 8.95 + EPS, 2.10);

        // Ventanales laterales del local
        for (vy = [7.0, 11.0, 16.0, 19.5]) {
            caja_coords(ANCHO_CASA - GROSOR_MURO_PIEDRA - EPS, vy, 1.00,
                        ANCHO_CASA + EPS, vy + 1.80, 2.20);
        }
    }
}

// ==============================================================================
// 2. ENTREPISO CON VIGAS DE MADERA LAMINADA VISTA
// ==============================================================================
module entrepiso_vigas() {
    color([0.35, 0.22, 0.12]) // Tono madera oscura nogal
    union() {
        // Tablero de piso P2
        difference() {
            caja_coords(OFFSET_MURO_PROPIO, 0, ALTURA_PB - ALTURA_ENTREPISO,
                        ANCHO_CASA, LARGO_CASA, ALTURA_PB);
            // Hueco de escalera
            caja_coords(1.50 - EPS, 4.30 - EPS, ALTURA_PB - ALTURA_ENTREPISO - EPS,
                        2.75 + EPS, 7.45 + EPS, ALTURA_PB + EPS);
            // Paso de chimenea
            caja_coords(CHIMENEA_POS_X - EPS, CHIMENEA_POS_Y - EPS, ALTURA_PB - ALTURA_ENTREPISO - EPS,
                        CHIMENEA_POS_X + CHIMENEA_ANCHO_X + EPS, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y + EPS, ALTURA_PB + EPS);
        }

        // Vigas maestras transversales vistas desde abajo
        for (y = [1.0 : 1.8 : LARGO_CASA - 1.0]) {
            caja_coords(OFFSET_MURO_PROPIO, y - SECCION_VIGA_X/2, ALTURA_PB - ALTURA_ENTREPISO - SECCION_VIGA_Z,
                        ANCHO_CASA, y + SECCION_VIGA_X/2, ALTURA_PB - ALTURA_ENTREPISO);
        }
    }
}

// ==============================================================================
// 3. PLANTA CHALET DE MADERA (SEGUNDO PISO - DISTRIBUCIÓN REDISEÑADA)
// ==============================================================================
module planta_chalet_madera() {
    z_base = ALTURA_PB;
    z_tope = z_base + ALTURA_P2_MUROS;

    color([0.72, 0.52, 0.35]) // Tono madera natural / alerce
    difference() {
        union() {
            // Muro lateral izquierdo propio (madera sobre zócalo)
            caja_coords(OFFSET_MURO_PROPIO, 0, z_base, 
                        OFFSET_MURO_PROPIO + GROSOR_MURO_MADERA, LARGO_CASA, z_tope);

            // Muro lateral derecho (Eje 3)
            caja_coords(ANCHO_CASA - GROSOR_MURO_MADERA, 3.50, z_base, 
                        ANCHO_CASA, LARGO_CASA, z_tope);

            // Fachada frontal interior detrás de la gran balconada corrida (Y = LARGO_CASA - FONDO_BALCON)
            caja_coords(OFFSET_MURO_PROPIO, LARGO_CASA - FONDO_BALCON, z_base, 
                        ANCHO_CASA, LARGO_CASA - FONDO_BALCON + GROSOR_MURO_MADERA, z_tope);

            // Muros posteriores P2
            caja_coords(OFFSET_MURO_PROPIO, 0, z_base, 6.40, GROSOR_MURO_MADERA, z_tope);
            caja_coords(6.40 - GROSOR_MURO_MADERA, 0, z_base, 6.40, 3.50, z_tope);
            caja_coords(6.40, 3.50, z_base, ANCHO_CASA, 3.50 + GROSOR_MURO_MADERA, z_tope);

            // --- TABIQUERÍA INTERIOR RÚSTICA ---
            // Muro Eje 2 que separa Zona Social de Dormitorios
            caja_coords(5.85, 3.50, z_base, 6.00, LARGO_CASA - FONDO_BALCON, z_tope);

            // Separación Master Suite vs Habitación 2
            caja_coords(6.00, 15.20, z_base, ANCHO_CASA, 15.35, z_tope);

            // Separación Habitación 2 vs Habitación 3
            caja_coords(6.00, 8.85, z_base, ANCHO_CASA, 9.00, z_tope);

            // Cierre Baño Compartido
            caja_coords(6.00, 5.40, z_base, ANCHO_CASA, 5.55, z_tope);

            // Cierre Vestier y Baño En-Suite en Master Suite
            caja_coords(6.80, 12.70, z_base, ANCHO_CASA, 12.85, z_tope);
            caja_coords(6.80, 12.85, z_base, 6.95, 15.20, z_tope);

            // Muro divisorio Lavandería / Terraza posterior
            caja_coords(2.80, 0, z_base, 2.95, 4.30, z_tope);
            caja_coords(OFFSET_MURO_PROPIO, 4.30, z_base, 2.95, 4.45, z_tope);

            // Gran Isla Central de Madera Maciza en Cocina (2.60 x 0.95 m)
            caja_coords(2.15, 9.80, z_base, 3.10, 12.40, z_base + 0.90);
        }

        // --- VANOS Y HUECOS DE PLANTA ALTA ---
        y_frente_int = LARGO_CASA - FONDO_BALCON;

        // Gran salida acristalada del Salón hacia la Balconada (3.20 x 2.30 m)
        caja_coords(1.20, y_frente_int - EPS, z_base - EPS, 4.60, y_frente_int + GROSOR_MURO_MADERA + EPS, z_base + 2.30);

        // Puerta-ventana rústica de la Master Suite a la Balconada (1.80 x 2.30 m)
        caja_coords(6.50, y_frente_int - EPS, z_base - EPS, 8.50, y_frente_int + GROSOR_MURO_MADERA + EPS, z_base + 2.30);

        // Puertas de habitaciones y baños
        caja_coords(5.85 - EPS, 16.00, z_base - EPS, 6.00 + EPS, 16.90, z_base + 2.10); // Puerta Master Suite
        caja_coords(5.85 - EPS, 12.20, z_base - EPS, 6.00 + EPS, 13.00, z_base + 2.10); // Puerta Hab. 2
        caja_coords(5.85 - EPS, 7.80, z_base - EPS, 6.00 + EPS, 8.60, z_base + 2.10);  // Puerta Hab. 3
        caja_coords(5.85 - EPS, 4.00, z_base - EPS, 6.00 + EPS, 4.80, z_base + 2.10);  // Puerta Baño Común

        // Ventanales rústicos en muro lateral este con recercados
        for (vy = [4.2, 6.8, 10.2, 13.4, 16.8]) {
            caja_coords(ANCHO_CASA - GROSOR_MURO_MADERA - EPS, vy, z_base + 0.95,
                        ANCHO_CASA + EPS, vy + 1.60, z_base + 2.15);
        }

        // Ventanal de terraza posterior y ventilación lavandería
        caja_coords(3.60, -EPS, z_base + 0.95, 5.40, GROSOR_MURO_MADERA + EPS, z_base + 2.15);
        caja_coords(0.60, -EPS, z_base + 1.20, 2.20, GROSOR_MURO_MADERA + EPS, z_base + 2.15);
    }
}

// ==============================================================================
// 4. CHIMENEA RÚSTICA DOMINANTE DE MAMPOSTERÍA DE PIEDRA
// ==============================================================================
module chimenea_piedra() {
    z_base = ALTURA_PB;
    altura_total_chimenea = ALTURA_PB + ALTURA_P2_MUROS + 4.80; // Sobresale de la cumbrera

    color([0.38, 0.35, 0.33]) // Color piedra volcánica / granito
    difference() {
        union() {
            // Cuerpo principal macizo de la chimenea
            caja_coords(CHIMENEA_POS_X, CHIMENEA_POS_Y, z_base,
                        CHIMENEA_POS_X + CHIMENEA_ANCHO_X, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y, altura_total_chimenea);

            // Remate superior protector con losa de piedra
            caja_coords(CHIMENEA_POS_X - 0.10, CHIMENEA_POS_Y - 0.10, altura_total_chimenea - 0.12,
                        CHIMENEA_POS_X + CHIMENEA_ANCHO_X + 0.10, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y + 0.10, altura_total_chimenea);
        }

        // Boca / Hogar de la chimenea abierto hacia el Gran Salón
        caja_coords(CHIMENEA_POS_X - EPS, CHIMENEA_POS_Y + 0.10, z_base + 0.10,
                    CHIMENEA_POS_X + 0.45, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y - 0.10, z_base + 0.95);

        // Tiro de humos interior hueco
        caja_coords(CHIMENEA_POS_X + 0.25, CHIMENEA_POS_Y + 0.20, z_base + 0.50,
                    CHIMENEA_POS_X + CHIMENEA_ANCHO_X - 0.25, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y - 0.20, altura_total_chimenea + EPS);
    }
}

// ==============================================================================
// 5. GRAN BALCONADA ALPINO-RÚSTICA CORRIDA (FACHADA AVENIDA 4)
// ==============================================================================
module balconada_alpina() {
    z_base = ALTURA_PB;
    y1 = LARGO_CASA - FONDO_BALCON;
    y2 = LARGO_CASA;

    color([0.48, 0.30, 0.16]) // Madera rústica teca
    union() {
        // Suelo de tablones de la balconada
        caja_coords(OFFSET_MURO_PROPIO, y1, z_base - 0.10, ANCHO_CASA, y2, z_base);

        // Vigas pasantes en voladizo bajo el balcón
        for (x = [OFFSET_MURO_PROPIO + 0.20 : 1.50 : ANCHO_CASA - 0.20]) {
            caja_coords(x - 0.07, y1 - 0.50, z_base - 0.28, x + 0.07, y2, z_base - 0.10);
        }

        // Postes maestros de madera ($14 \times 14\text{ cm}$)
        for (x = [OFFSET_MURO_PROPIO + 0.10, 3.10, 6.00, ANCHO_CASA - 0.10]) {
            caja_coords(x - SECCION_POSTE_BALCON/2, y2 - SECCION_POSTE_BALCON, z_base,
                        x + SECCION_POSTE_BALCON/2, y2, z_base + ALTURA_P2_MUROS);
        }

        // Pasamanos superior continuo de madera labrada
        caja_coords(OFFSET_MURO_PROPIO, y2 - 0.12, z_base + ALTURA_BARANDILLA - 0.08,
                    ANCHO_CASA, y2, z_base + ALTURA_BARANDILLA);
        // Zócalo inferior de la barandilla
        caja_coords(OFFSET_MURO_PROPIO, y2 - 0.08, z_base + 0.05,
                    ANCHO_CASA, y2, z_base + 0.12);

        // Entramado rústico en Cruz de San Andrés entre postes
        postes_x = [OFFSET_MURO_PROPIO + 0.10, 3.10, 6.00, ANCHO_CASA - 0.10];
        for (i = [0 : len(postes_x) - 2]) {
            px1 = postes_x[i] + SECCION_POSTE_BALCON/2;
            px2 = postes_x[i+1] - SECCION_POSTE_BALCON/2;
            pmid_x = (px1 + px2) / 2;
            pmid_z = z_base + (ALTURA_BARANDILLA / 2);

            // Cruces en listones de madera
            caja_coords(pmid_x - 0.04, y2 - 0.06, z_base + 0.12, pmid_x + 0.04, y2 - 0.02, z_base + ALTURA_BARANDILLA - 0.08);
            caja_coords(px1, y2 - 0.06, pmid_z - 0.03, px2, y2 - 0.02, pmid_z + 0.03);
        }
    }
}

// ==============================================================================
// 6. CERCHAS, PARES Y CANECILLOS EXPUESTOS (RAFTER TAILS)
// ==============================================================================
module vigas_expuestas_y_canecillos() {
    z_alero = ALTURA_PB + ALTURA_P2_MUROS - 0.10;
    x_min = OFFSET_MURO_PROPIO - ALERO_LATERAL;
    x_max = ANCHO_CASA + ALERO_LATERAL;
    y_min = -ALERO_POSTERIOR;
    y_max = LARGO_CASA + ALERO_FRONTAL;

    color([0.40, 0.24, 0.12]) // Madera noble envejecida
    union() {
        // Canecillos pasantes transversales a lo largo de los aleros
        for (y = [y_min + 0.40 : INTEREJE_CANECILLOS : y_max - 0.40]) {
            // Canecillo alero izquierdo
            caja_coords(x_min, y - SECCION_VIGA_X/2, z_alero, 
                        OFFSET_MURO_PROPIO + 0.40, y + SECCION_VIGA_X/2, z_alero + SECCION_VIGA_Z);
            // Canecillo alero derecho
            caja_coords(ANCHO_CASA - 0.40, y - SECCION_VIGA_X/2, z_alero, 
                        x_max, y + SECCION_VIGA_X/2, z_alero + SECCION_VIGA_Z);
        }

        // Viga cumbrera maestra longitudinal en la cúspide alpina
        h_cumbrera = (ANCHO_CASA/2 + ALERO_LATERAL) * tan(ANGULO_TECHO);
        z_cumbrera = z_alero + h_cumbrera;
        caja_coords(CUMBRERA_X - 0.10, y_min, z_cumbrera - 0.30, 
                    CUMBRERA_X + 0.10, y_max, z_cumbrera);
    }
}

// ==============================================================================
// 7. CUBIERTA ALPINA A DOS AGUAS (GABLE ROOF CON GENEROSOS ALEROS)
// ==============================================================================
module cubierta_alpina() {
    z_alero = ALTURA_PB + ALTURA_P2_MUROS;
    x_min = OFFSET_MURO_PROPIO - ALERO_LATERAL;
    x_max = ANCHO_CASA + ALERO_LATERAL;
    y_min = -ALERO_POSTERIOR;
    y_max = LARGO_CASA + ALERO_FRONTAL;

    semi_ancho = CUMBRERA_X - x_min;
    altura_vert = semi_ancho * tan(ANGULO_TECHO);
    z_cumbrera = z_alero + altura_vert;

    color([0.55, 0.22, 0.15]) // Tono teja rústica de arcilla / pizarra
    difference() {
        union() {
            // Faldón izquierdo (caída hacia Eje 0 / Oeste)
            polyhedron(
                points = [
                    [x_min, y_min, z_alero],
                    [CUMBRERA_X, y_min, z_cumbrera],
                    [CUMBRERA_X, y_max, z_cumbrera],
                    [x_min, y_max, z_alero],
                    [x_min, y_min, z_alero + GROSOR_CUBIERTA],
                    [CUMBRERA_X, y_min, z_cumbrera + GROSOR_CUBIERTA],
                    [CUMBRERA_X, y_max, z_cumbrera + GROSOR_CUBIERTA],
                    [x_min, y_max, z_alero + GROSOR_CUBIERTA]
                ],
                faces = [
                    [0,1,2,3], [4,7,6,5], [0,4,5,1],
                    [1,5,6,2], [2,6,7,3], [3,7,4,0]
                ]
            );

            // Faldón derecho (caída hacia Eje 3 / Este)
            polyhedron(
                points = [
                    [CUMBRERA_X, y_min, z_cumbrera],
                    [x_max, y_min, z_alero],
                    [x_max, y_max, z_alero],
                    [CUMBRERA_X, y_max, z_cumbrera],
                    [CUMBRERA_X, y_min, z_cumbrera + GROSOR_CUBIERTA],
                    [x_max, y_min, z_alero + GROSOR_CUBIERTA],
                    [x_max, y_max, z_alero + GROSOR_CUBIERTA],
                    [CUMBRERA_X, y_max, z_cumbrera + GROSOR_CUBIERTA]
                ],
                faces = [
                    [0,1,2,3], [4,7,6,5], [0,4,5,1],
                    [1,5,6,2], [2,6,7,3], [3,7,4,0]
                ]
            );

            // Caballete / Cumbrera de remate impermeable
            caja_coords(CUMBRERA_X - 0.20, y_min, z_cumbrera, 
                        CUMBRERA_X + 0.20, y_max, z_cumbrera + GROSOR_CUBIERTA + 0.08);
        }

        // Hueco para perforación de la chimenea de piedra
        caja_coords(CHIMENEA_POS_X - 0.05, CHIMENEA_POS_Y - 0.05, z_alero - EPS,
                    CHIMENEA_POS_X + CHIMENEA_ANCHO_X + 0.05, CHIMENEA_POS_Y + CHIMENEA_FONDO_Y + 0.05, z_cumbrera + 1.0);
    }
}

// ==============================================================================
// 8. CARPINTERÍAS RÚSTICAS (VENTANAS CON CUARTERONES Y CONTRAVENTANAS / SHUTTERS)
// ==============================================================================
module ventana_rustica_con_shutters(ancho, alto, tiene_shutters=true) {
    color([0.30, 0.18, 0.10]) // Madera oscura
    union() {
        // Marco perimetral prominente
        difference() {
            cube([ancho, 0.08, alto]);
            translate([0.08, -EPS, 0.08])
                cube([ancho - 0.16, 0.08 + 2*EPS, alto - 0.16]);
        }
        // Cuarterones / Parteluces
        translate([ancho/2 - 0.02, 0, 0.08])
            cube([0.04, 0.06, alto - 0.16]);
        translate([0.08, 0, alto/2 - 0.02])
            cube([ancho - 0.16, 0.06, 0.04]);

        // Contraventanas de lamas exteriores abiertas a 90 grados
        if (tiene_shutters) {
            sh_ancho = ancho / 2 - 0.02;
            translate([-sh_ancho, -0.04, 0])
                cube([sh_ancho, 0.04, alto]);
            translate([ancho, -0.04, 0])
                cube([sh_ancho, 0.04, alto]);
        }
    }
}

// ==============================================================================
// 8. COLUMNAS ESTRUCTURALES PLANTA BAJA (ZONA COMERCIAL Y GARAJE)
// Tomando en cuenta casa_modificaciones.dxf (25x25 cm, Ejes 0, 1, 2, 3 y A0 a G)
// ==============================================================================
module columnas_zona_comercial() {
    color([0.80, 0.20, 0.20]) // Rojo normativo estructural / concreto armado
    union() {
        // Red modular de columnas 25x25 cm según casa_modificaciones.dxf
        cols_pb = [
            [0.275, 21.585], [2.825, 21.585], [5.925, 21.585], [9.075, 21.585], // Eje A0 (Av. 4)
            [0.275, 18.575], [2.825, 18.575], [5.925, 18.575], [9.075, 18.575], // Eje A
            [0.275, 16.325], [2.825, 16.325], [5.925, 16.325],                  // Eje B
            [9.075, 14.625],                                                      // Eje C
            [0.275, 12.025], [2.825, 12.025], [5.925, 12.025], [9.075, 12.025], // Eje D
            [0.275, 8.875],  [2.825, 8.875],  [5.925, 8.875],  [9.075, 8.875],  // Eje E
            [0.275, 6.575],  [2.825, 6.575],  [5.925, 6.575],  [9.075, 6.575],  // Eje F
            [0.275, 3.575],  [2.825, 3.575],  [5.925, 3.575],  [9.075, 3.575],  // Eje G
            [0.275, 0.075],  [2.825, 0.075],  [5.925, 0.075]                    // Eje Posterior
        ];
        for (pt = cols_pb) {
            caja_coords(pt[0] - 0.125, pt[1] - 0.125, 0,
                        pt[0] + 0.125, pt[1] + 0.125, ALTURA_PB);
        }
    }
}

// ==============================================================================
// 9. COLUMNAS ESTRUCTURALES Y POSTES TIMBER FRAME - ÚLTIMO PISO (PLANTA ALTA)
// Tomando en cuenta casa_modificaciones.dxf (25x25 cm, Z = 3.00 a 5.85 m)
// ==============================================================================
module columnas_ultimo_piso() {
    color([0.50, 0.30, 0.18]) // Tono madera maciza estructural (Roble / Timber Frame)
    union() {
        // Prolongación vertical de las columnas en el piso superior hasta solera
        cols_p2 = [
            [0.275, 21.585], [2.825, 21.585], [5.925, 21.585], [9.075, 21.585], // Eje A0 (Av. 4)
            [0.275, 18.575], [2.825, 18.575], [5.925, 18.575], [9.075, 18.575], // Eje A
            [0.275, 16.325], [2.825, 16.325], [5.925, 16.325],                  // Eje B
            [9.075, 14.625],                                                      // Eje C
            [0.275, 12.025], [2.825, 12.025], [5.925, 12.025], [9.075, 12.025], // Eje D
            [0.275, 8.875],  [2.825, 8.875],  [5.925, 8.875],  [9.075, 8.875],  // Eje E
            [0.275, 6.575],  [2.825, 6.575],  [5.925, 6.575],  [9.075, 6.575],  // Eje F
            [0.275, 3.575],  [2.825, 3.575],  [5.925, 3.575],  [9.075, 3.575],  // Eje G
            [0.275, 0.075],  [2.825, 0.075],  [5.925, 0.075]                    // Eje Posterior
        ];
        for (pt = cols_p2) {
            caja_coords(pt[0] - 0.125, pt[1] - 0.125, ALTURA_PB,
                        pt[0] + 0.125, pt[1] + 0.125, ALTURA_PB + ALTURA_P2);
        }
    }
}

// ==============================================================================
// ENSAMBLAJE MAESTRO DEL MODELO COMPLETO
// ==============================================================================
module casa_chalet_completa() {
    // 1. Zócalo pétreo en Planta Baja (Local Comercial + Garaje)
    zocalo_piedra();

    // 2. Entrepiso estructural con vigas vistas
    entrepiso_vigas();

    // 3. Planta Alta de madera con distribución de montaña
    planta_chalet_madera();

    // 4. Gran Balconada frontal corrida hacia Avenida 4
    balconada_alpina();

    // 5. Chimenea dominante de piedra natural
    chimenea_piedra();

    // 6. Entramado de pares, cumbrera y canecillos pasantes
    vigas_expuestas_y_canecillos();

    // 7. Cubierta alpina a dos aguas con aleros pronunciados
    cubierta_alpina();

    // 8. Columnas estructurales de Planta Baja (Zona Comercial y Garaje)
    columnas_zona_comercial();

    // 9. Columnas estructurales del Último Piso (Planta Alta Chalet Timber Frame)
    columnas_ultimo_piso();
}

// Invocar modelo completo para renderizado
casa_chalet_completa();
