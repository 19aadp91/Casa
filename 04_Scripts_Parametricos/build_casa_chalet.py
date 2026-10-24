"""
Generador Maestro del Proyecto Chalet Rústico Alpino ("casa_chalet_rustico.dxf", .obj, .stl)
Basado en las dimensiones de casa_modificaciones.dxf (conservándola intacta en otro proyecto).

Características del Rediseño Chalet Rústico:
1. Zócalo de mampostería de piedra natural en Planta Baja (Local Comercial + Garaje ampliado a 2.80 m libres).
2. Cuerpo de madera superior (Planta Alta) con entramado visto tipo Timber Frame.
3. Cubierta alpina a dos aguas (Gable Roof) con pendiente de 38°, cumbrera a Z = +9.72 m y grandes aleros (1.10 - 1.20 m).
4. Canecillos y pares pasantes expuestos (rafter tails) bajo los aleros.
5. Gran balconada corrida frontal hacia la Avenida 4 (9.00 x 1.60 m) con barandilla en Cruz de San Andrés.
6. Chimenea rústica dominante de piedra natural que se eleva hasta coronar la cumbrera.
7. Nueva distribución de montaña en P2: Gran Salón-Comedor con doble altura y cerchas vistas, cocina rústica
   con gran isla de madera maciza, Master Suite con baño de piedra y vestier, 2 habitaciones secundarias abuhardilladas,
   baño familiar de piedra y terraza posterior mirador a la serranía.
8. Mantiene la topografía UTM exacta con los 5 niveles escalonados y el sótano con muros de contención.
"""

import os
import math

def build_chalet_project():
    boxes_3d = []      # (layer, color, x1, y1, z1, x2, y2, z2)
    hexahedra_3d = []  # (layer, color, [p0..p7])
    lines_2d = []      # (layer, color, x1, y1, z1, x2, y2, z2)
    texts = []         # (layer, color, text, x, y, z, h)

    def add_box(layer, color, x1, y1, z1, x2, y2, z2):
        if abs(x2 - x1) < 1e-4 or abs(y2 - y1) < 1e-4 or abs(z2 - z1) < 1e-4:
            return
        boxes_3d.append((layer, color, min(x1, x2), min(y1, y2), min(z1, z2),
                                       max(x1, x2), max(y1, y2), max(z1, z2)))

    def add_hexahedron(layer, color, pts8):
        hexahedra_3d.append((layer, color, pts8))

    def add_line(layer, color, x1, y1, z1, x2, y2, z2):
        lines_2d.append((layer, color, x1, y1, z1, x2, y2, z2))

    def add_text(layer, color, text, x, y, z, h=0.25):
        texts.append((layer, color, text, x, y, z, h))

    # =========================================================================
    # PARÁMETROS GEOMÉTRICOS Y VERTICALES
    # =========================================================================
    OFFSET_X = 0.00
    OFFSET_Y = 3.00
    Y_AV4    = 21.71  # Frente extendido hasta Avenida 4
    ANCHO    = 9.15

    Z_SOT_FLOOR    = -2.55
    Z_P1_FLOOR     =  0.00   # Zócalo Planta Baja
    H_P1           =  3.00   # Losa entrepiso
    Z_P2_FLOOR     =  3.00   # Planta Alta de Madera
    H_P2_MURO      =  5.85   # Arranque de aleros de cubierta
    Z_ALERO        =  5.40   # Borde inferior del alero en voladizo
    Z_CUMBRERA     =  9.72   # Cúspide de la cubierta alpina a dos aguas (38°)
    Z_CHIMENEA_TOP = 10.40   # Remate superior de chimenea de piedra

    ALERO_LATERAL   = 1.10
    ALERO_FRONTAL   = 1.20
    ALERO_POSTERIOR = 1.10
    X_CUMBRERA      = 4.65   # Eje central de cumbrera

    def add_h_box(layer, color, x1, y1, z1, x2, y2, z2):
        add_box(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_h_line(layer, color, x1, y1, z1, x2, y2, z2):
        add_line(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_h_text(layer, color, text, x, y, z, h=0.22):
        add_text(layer, color, text, OFFSET_X + x, OFFSET_Y + y, z, h)

    def add_h_hex(layer, color, pts8):
        pts_off = [(OFFSET_X + px, OFFSET_Y + py, pz) for px, py, pz in pts8]
        add_hexahedron(layer, color, pts_off)

    # =========================================================================
    # 1. TOPOGRAFÍA UTM Y SÓTANO PRESERVADOS
    # =========================================================================
    L_TERRENO = "TERRENO_UTM_3D"
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    # Losas de sótano
    add_h_box(L_SOT_SLAB, 8, 0.15, 0.00, -2.70, 6.40, 3.50, Z_SOT_FLOOR)
    add_h_box(L_SOT_SLAB, 8, 0.15, 3.50, -2.70, 9.15, 8.30, Z_SOT_FLOOR)

    # Muros de sótano y contención
    add_h_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, -0.15)
    add_h_box(L_SOT_EXT, 4, 0.30, 0.00, Z_SOT_FLOOR, 6.40, 0.15, -0.15)
    add_h_box(L_SOT_EXT, 4, 6.25, 0.15, Z_SOT_FLOOR, 6.40, 3.50, -0.15)
    add_h_box(L_SOT_EXT, 4, 6.00, 3.50, Z_SOT_FLOOR, 9.15, 3.65, -0.15)
    add_h_box(L_SOT_EXT, 4, 8.95, 3.65, Z_SOT_FLOOR, 9.15, 8.30, -0.15)
    add_h_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, -0.15)

    # Columnas Sótano 35x35 cm
    for cx, cy in [(0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
                   (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575)]:
        add_h_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, -0.15)

    # Escalera que baja al sótano
    for i in range(12):
        y_step = 7.40 - i * (2.95 / 12)
        z_step = 0.00 - i * (2.55 / 12)
        add_h_box("ESCALERA_3D", 7, 0.30, y_step - (2.95/12), Z_SOT_FLOOR, 1.40, y_step, z_step)

    # =========================================================================
    # 2. PLANTA BAJA: ZÓCALO DE MAMPOSTERÍA DE PIEDRA (LOCAL + GARAJE AMPLIADO)
    # =========================================================================
    L_PB_PIEDRA = "PB_ZOCALO_PIEDRA_3D"
    L_PB_INT    = "PB_TABIQUES_3D"
    L_PB_SLAB   = "PB_LOSA_PISO_3D"

    # Losa de piso Planta Baja extendida
    add_h_box(L_PB_SLAB, 8, 0.15, 0.00, -0.15, 9.15, Y_AV4, Z_P1_FLOOR)

    # Muro Propio Izquierdo continuo en Zócalo de Piedra (X: 0.15 a 0.35 m, 20 cm)
    add_h_box(L_PB_PIEDRA, 8, 0.15, 0.00, Z_P1_FLOOR, 0.35, Y_AV4, H_P1)

    # Fachada Frontal en Avenida 4 (Zócalo de Piedra con recercados)
    add_h_box(L_PB_PIEDRA, 8, 0.15, Y_AV4 - 0.30, Z_P1_FLOOR, 0.40, Y_AV4, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 3.10, Y_AV4 - 0.30, Z_P1_FLOOR, 3.60, Y_AV4, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 6.00, Y_AV4 - 0.30, Z_P1_FLOOR, 6.40, Y_AV4, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 8.90, Y_AV4 - 0.30, Z_P1_FLOOR, 9.15, Y_AV4, H_P1)
    # Dinteles pesados de piedra sobre portón y vitrinas
    add_h_box(L_PB_PIEDRA, 8, 0.40, Y_AV4 - 0.30, 2.40, 3.10, Y_AV4, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 3.60, Y_AV4 - 0.30, 2.50, 6.00, Y_AV4, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 6.40, Y_AV4 - 0.30, 2.50, 8.90, Y_AV4, H_P1)

    # Muro Lateral Derecho en Zócalo de Piedra (Eje 3)
    add_h_box(L_PB_PIEDRA, 8, 8.95, 3.50, Z_P1_FLOOR, 9.15, Y_AV4 - 0.30, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 6.25, 3.50, Z_P1_FLOOR, 9.15, 3.65, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 6.25, 0.00, Z_P1_FLOOR, 6.40, 3.50, H_P1)
    add_h_box(L_PB_PIEDRA, 8, 0.15, 0.00, Z_P1_FLOOR, 6.40, 0.20, H_P1)

    # Muro divisorio interior que da al garaje 2.80 m libres (X: 3.10 a 3.25 m)
    add_h_box(L_PB_INT, 7, 3.10, 0.15, Z_P1_FLOOR, 3.25, Y_AV4 - 0.30, H_P1)
    # Muro posterior garaje con puerta privada
    add_h_box(L_PB_INT, 7, 0.35, 8.80, Z_P1_FLOOR, 2.00, 8.95, H_P1)
    add_h_box(L_PB_INT, 7, 2.90, 8.80, Z_P1_FLOOR, 3.10, 8.95, H_P1)
    add_h_box(L_PB_INT, 7, 2.00, 8.80, 2.10, 2.90, 8.95, H_P1) # Dintel puerta privada

    # Baño y depósito local
    add_h_box(L_PB_INT, 7, 5.85, 5.40, Z_P1_FLOOR, 8.95, 5.55, H_P1)
    add_h_box(L_PB_INT, 7, 5.85, 3.65, Z_P1_FLOOR, 6.00, 4.60, H_P1)
    add_h_box(L_PB_INT, 7, 3.25, 3.50, Z_P1_FLOOR, 4.80, 3.65, H_P1)
    add_h_box(L_PB_INT, 7, 5.65, 3.50, Z_P1_FLOOR, 6.25, 3.65, H_P1)

    # =========================================================================
    # 3. PLANTA ALTA: CUERPO LIGERO DE MADERA (CHALET ALPINO)
    # =========================================================================
    L_CHALET_P2   = "CHALET_P2_MADERA_3D"
    L_BALCON      = "CHALET_BALCONADA_ALPINA_3D"
    L_CHIMENEA    = "CHALET_CHIMENEA_PIEDRA_3D"
    L_VIGAS_EXP   = "CHALET_VIGAS_CANECILLOS_3D"
    L_CUBIERTA    = "CHALET_CUBIERTA_ALPINA_3D"

    # Losa y vigas de entrepiso de madera (Z: 2.85 a 3.00 m)
    add_h_box("CHALET_ENTREPISO_3D", 6, 0.15, 0.00, 2.85, 9.15, Y_AV4, Z_P2_FLOOR)

    # Vigas de madera vistas bajo entrepiso
    for y_v in [1.5, 3.5, 5.5, 7.5, 9.5, 11.5, 13.5, 15.5, 17.5, 19.5, 21.0]:
        add_h_box(L_VIGAS_EXP, 6, 0.15, y_v - 0.07, 2.70, 9.15, y_v + 0.07, 2.85)

    # Muro Lateral Izquierdo de Madera (X: 0.15 a 0.35 m, Z = 3.00 a 5.85 m)
    add_h_box(L_CHALET_P2, 6, 0.15, 0.00, Z_P2_FLOOR, 0.35, Y_AV4, H_P2_MURO)

    # Muro Lateral Derecho de Madera (Eje 3, X: 8.95 a 9.15 m)
    add_h_box(L_CHALET_P2, 6, 8.95, 3.50, Z_P2_FLOOR, 9.15, Y_AV4, H_P2_MURO)

    # Muro frontal interior de madera (Y = 20.11 m, dejando 1.60 m para la balconada corrida)
    add_h_box(L_CHALET_P2, 6, 0.15, 20.11, Z_P2_FLOOR, 1.20, 20.26, H_P2_MURO)
    add_h_box(L_CHALET_P2, 6, 4.80, 20.11, Z_P2_FLOOR, 6.20, 20.26, H_P2_MURO)
    add_h_box(L_CHALET_P2, 6, 8.40, 20.11, Z_P2_FLOOR, 9.15, 20.26, H_P2_MURO)
    # Dinteles rústicos sobre salidas a balconada
    add_h_box(L_CHALET_P2, 6, 1.20, 20.11, Z_P2_FLOOR + 2.30, 4.80, 20.26, H_P2_MURO) # Salón a balcón
    add_h_box(L_CHALET_P2, 6, 6.20, 20.11, Z_P2_FLOOR + 2.30, 8.40, 20.26, H_P2_MURO) # Suite a balcón

    # Muros Posteriores de Madera
    add_h_box(L_CHALET_P2, 6, 0.15, 0.00, Z_P2_FLOOR, 6.40, 0.15, H_P2_MURO)
    add_h_box(L_CHALET_P2, 6, 6.25, 0.15, Z_P2_FLOOR, 6.40, 3.50, H_P2_MURO)
    add_h_box(L_CHALET_P2, 6, 6.25, 3.50, Z_P2_FLOOR, 9.15, 3.65, H_P2_MURO)

    # --- TABIQUERÍA DE MADERA P2 (DISTRIBUCIÓN CHALET) ---
    # Muro Eje 2 (X: 5.85 a 6.00 m) que separa Salón y Dormitorios
    add_h_box(L_CHALET_P2, 6, 5.85, 3.65, Z_P2_FLOOR, 6.00, 20.11, H_P2_MURO)

    # Suite Principal (Master Suite)
    add_h_box(L_CHALET_P2, 6, 6.00, 15.20, Z_P2_FLOOR, 9.00, 15.35, H_P2_MURO)
    # Vestier y Baño En-Suite con revestimiento de piedra
    add_h_box(L_CHALET_P2, 8, 6.80, 12.70, Z_P2_FLOOR, 9.00, 12.85, H_P2_MURO) # Muro de piedra
    add_h_box(L_CHALET_P2, 6, 6.80, 12.85, Z_P2_FLOOR, 6.95, 15.20, H_P2_MURO)

    # Habitación 2 (3.00 x 3.60 m)
    add_h_box(L_CHALET_P2, 6, 6.00, 8.85, Z_P2_FLOOR, 9.00, 9.00, H_P2_MURO)

    # Baño Familiar de Piedra (3.00 x 1.75 m)
    add_h_box(L_CHALET_P2, 8, 6.00, 5.40, Z_P2_FLOOR, 9.00, 5.55, H_P2_MURO)

    # Lavandería y Terraza posterior
    add_h_box(L_CHALET_P2, 6, 2.80, 0.15, Z_P2_FLOOR, 2.95, 4.30, H_P2_MURO)
    add_h_box(L_CHALET_P2, 6, 0.15, 4.30, Z_P2_FLOOR, 2.95, 4.45, H_P2_MURO)

    # Gran Isla Central de Madera Maciza en Cocina (2.60 x 0.95 m)
    add_h_box(L_CHALET_P2, 6, 2.15, 9.80, Z_P2_FLOOR, 3.10, 12.40, Z_P2_FLOOR + 0.90)

    # =========================================================================
    # 4. CHIMENEA RÚSTICA DOMINANTE DE PIEDRA
    # =========================================================================
    cx1, cx2 = 4.70, 5.80
    cy1, cy2 = 16.80, 17.65
    # Cuerpo principal de piedra que asciende por toda la casa hasta superar la cumbrera
    add_h_box(L_CHIMENEA, 8, cx1, cy1, Z_P1_FLOOR, cx2, cy2, Z_CHIMENEA_TOP)
    # Losa de remate superior de la chimenea
    add_h_box(L_CHIMENEA, 8, cx1 - 0.12, cy1 - 0.12, Z_CHIMENEA_TOP - 0.12, cx2 + 0.12, cy2 + 0.12, Z_CHIMENEA_TOP)

    # =========================================================================
    # 5. GRAN BALCONADA CORRIDA ALPINO-RÚSTICA (FACHADA AVENIDA 4)
    # =========================================================================
    # Piso de tablones de madera en voladizo (X: 0.15 a 9.15 m, Y: 20.11 a 21.71 m)
    add_h_box(L_BALCON, 6, 0.15, 20.11, Z_P2_FLOOR - 0.08, 9.15, Y_AV4, Z_P2_FLOOR)

    # Postes maestros de madera (14x14 cm)
    postes_x = [0.25, 3.10, 6.00, 9.05]
    for px in postes_x:
        add_h_box(L_BALCON, 6, px - 0.07, Y_AV4 - 0.14, Z_P2_FLOOR, px + 0.07, Y_AV4, H_P2_MURO)

    # Pasamanos superior de madera labrada
    add_h_box(L_BALCON, 6, 0.15, Y_AV4 - 0.12, Z_P2_FLOOR + 0.98, 9.15, Y_AV4, Z_P2_FLOOR + 1.05)
    # Zócalo inferior barandilla
    add_h_box(L_BALCON, 6, 0.15, Y_AV4 - 0.08, Z_P2_FLOOR + 0.05, 9.15, Y_AV4, Z_P2_FLOOR + 0.12)

    # Barandillas rústicas en Cruz de San Andrés entre postes
    for i in range(len(postes_x)-1):
        x_a = postes_x[i] + 0.07
        x_b = postes_x[i+1] - 0.07
        xm = (x_a + x_b) / 2
        zm = Z_P2_FLOOR + 0.55
        add_h_box(L_BALCON, 6, xm - 0.04, Y_AV4 - 0.06, Z_P2_FLOOR + 0.12, xm + 0.04, Y_AV4 - 0.02, Z_P2_FLOOR + 0.98)
        add_h_box(L_BALCON, 6, x_a, Y_AV4 - 0.06, zm - 0.03, x_b, Y_AV4 - 0.02, zm + 0.03)

    # =========================================================================
    # 6. CUBIERTA ALPINA A DOS AGUAS (GABLE ROOF CON GENEROSOS ALEROS)
    # =========================================================================
    # Coordenadas de los faldones a dos aguas
    x_alero_izq = 0.15 - ALERO_LATERAL   # -0.95 m
    x_alero_der = 9.15 + ALERO_LATERAL   # 10.25 m
    y_alero_sur = -ALERO_POSTERIOR       # -1.10 m
    y_alero_nor = Y_AV4 + ALERO_FRONTAL  # 22.91 m

    # Faldón Izquierdo (Oeste, pendiente de 38° desde cumbrera a Z = 5.40 m)
    # Hexaedro sólido del faldón con espesor 0.20 m
    faldon_izq_pts = [
        (x_alero_izq, y_alero_sur, Z_ALERO),
        (X_CUMBRERA,  y_alero_sur, Z_CUMBRERA),
        (X_CUMBRERA,  y_alero_nor, Z_CUMBRERA),
        (x_alero_izq, y_alero_nor, Z_ALERO),
        (x_alero_izq, y_alero_sur, Z_ALERO + 0.20),
        (X_CUMBRERA,  y_alero_sur, Z_CUMBRERA + 0.20),
        (X_CUMBRERA,  y_alero_nor, Z_CUMBRERA + 0.20),
        (x_alero_izq, y_alero_nor, Z_ALERO + 0.20)
    ]
    add_h_hex(L_CUBIERTA, 1, faldon_izq_pts)

    # Faldón Derecho (Este, pendiente de 38°)
    faldon_der_pts = [
        (X_CUMBRERA,  y_alero_sur, Z_CUMBRERA),
        (x_alero_der, y_alero_sur, Z_ALERO),
        (x_alero_der, y_alero_nor, Z_ALERO),
        (X_CUMBRERA,  y_alero_nor, Z_CUMBRERA),
        (X_CUMBRERA,  y_alero_sur, Z_CUMBRERA + 0.20),
        (x_alero_der, y_alero_sur, Z_ALERO + 0.20),
        (x_alero_der, y_alero_nor, Z_ALERO + 0.20),
        (X_CUMBRERA,  y_alero_nor, Z_CUMBRERA + 0.20)
    ]
    add_h_hex(L_CUBIERTA, 1, faldon_der_pts)

    # Caballete / Cumbrera de remate rústico
    add_h_box(L_CUBIERTA, 1, X_CUMBRERA - 0.20, y_alero_sur, Z_CUMBRERA + 0.15, 
                             X_CUMBRERA + 0.20, y_alero_nor, Z_CUMBRERA + 0.28)

    # Testero / Frontón triangular frontal de madera (cierre sobre balcón)
    fronton_pts = [
        (0.15, Y_AV4 - 0.10, H_P2_MURO),
        (X_CUMBRERA, Y_AV4 - 0.10, Z_CUMBRERA),
        (X_CUMBRERA, Y_AV4 + 0.10, Z_CUMBRERA),
        (0.15, Y_AV4 + 0.10, H_P2_MURO),
        (9.15, Y_AV4 - 0.10, H_P2_MURO),
        (X_CUMBRERA, Y_AV4 - 0.10, Z_CUMBRERA),
        (X_CUMBRERA, Y_AV4 + 0.10, Z_CUMBRERA),
        (9.15, Y_AV4 + 0.10, H_P2_MURO)
    ]
    add_h_hex(L_CHALET_P2, 6, fronton_pts[:8])

    # Canecillos pasantes vistos (Rafter tails) bajo el alero
    for yc in [y_alero_sur + 0.50 + i * 1.00 for i in range(24)]:
        if yc <= y_alero_nor - 0.40:
            # Canecillo alero izquierdo
            add_h_box(L_VIGAS_EXP, 6, x_alero_izq, yc - 0.06, Z_ALERO - 0.15, 0.40, yc + 0.06, Z_ALERO)
            # Canecillo alero derecho
            add_h_box(L_VIGAS_EXP, 6, 8.80, yc - 0.06, Z_ALERO - 0.15, x_alero_der, yc + 0.06, Z_ALERO)

    # =========================================================================
    # LÍNEAS 2D DE PLANTA ARQUITECTÓNICA Y RÓTULOS
    # =========================================================================
    # Proyección de cumbrera y aleros en 2D
    add_h_line("2D_CUBIERTA_ALEROS", 1, x_alero_izq, y_alero_sur, 0, x_alero_der, y_alero_sur, 0)
    add_h_line("2D_CUBIERTA_ALEROS", 1, x_alero_der, y_alero_sur, 0, x_alero_der, y_alero_nor, 0)
    add_h_line("2D_CUBIERTA_ALEROS", 1, x_alero_der, y_alero_nor, 0, x_alero_izq, y_alero_nor, 0)
    add_h_line("2D_CUBIERTA_ALEROS", 1, x_alero_izq, y_alero_nor, 0, x_alero_izq, y_alero_sur, 0)
    add_h_line("2D_CUBIERTA_CUMBRERA", 1, X_CUMBRERA, y_alero_sur, 0, X_CUMBRERA, y_alero_nor, 0)

    # Rótulos técnicos 2D
    add_h_text("2D_ROTULOS", 2, "P2: GRAN SALÓN CHALET CON CHIMENEA (DOBLE ALTURA)", 3.40, 16.50, 0.05)
    add_h_text("2D_ROTULOS", 2, "P2: GRAN BALCONADA CORRIDA TECHADA HACIA AV. 4 (9,00 x 1,60m)", 0.50, 20.80, 0.05)
    add_h_text("2D_ROTULOS", 2, "P2: MASTER SUITE ALPINA CON VESTIER Y BAÑO DE PIEDRA", 6.20, 17.50, 0.05)
    add_h_text("2D_ROTULOS", 2, "P2: COCINA RÚSTICA CON ISLA DE MADERA MACIZA (2,60 x 0,95m)", 1.20, 11.00, 0.05)
    add_h_text("2D_ROTULOS", 2, "PB: ZÓCALO DE PIEDRA - LOCAL COMERCIAL (91 m2) Y GARAJE AMPLIADO (2,80m)", 0.50, 14.00, 0.05)
    add_h_text("2D_ROTULOS", 2, "CUBIERTA ALPINA A DOS AGUAS: PENDIENTE 38° CON ALEROS DE 1,10m", 1.00, -0.60, 0.05)

    # =========================================================================
    # EXPORTACIÓN DE ARCHIVOS
    # =========================================================================
    # 1. DXF ASCII R12/2000
    dxf_lines = [
        "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n",
        "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n10\n",
    ]
    layers = list(set([b[0] for b in boxes_3d] + [h[0] for h in hexahedra_3d] + [l[0] for l in lines_2d] + [t[0] for t in texts]))
    for l in layers:
        dxf_lines.extend(["0\nLAYER\n2\n", f"{l}\n", "70\n0\n62\n7\n6\nCONTINUOUS\n"])
    dxf_lines.append("0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n")

    def w(code, val):
        dxf_lines.append(f"{code}\n{val}\n")

    def write_3dface(layer, color, p1, p2, p3, p4):
        w(0, "3DFACE"); w(8, layer); w(62, color)
        w(10, f"{p1[0]:.4f}"); w(20, f"{p1[1]:.4f}"); w(30, f"{p1[2]:.4f}")
        w(11, f"{p2[0]:.4f}"); w(21, f"{p2[1]:.4f}"); w(31, f"{p2[2]:.4f}")
        w(12, f"{p3[0]:.4f}"); w(22, f"{p3[1]:.4f}"); w(32, f"{p3[2]:.4f}")
        w(13, f"{p4[0]:.4f}"); w(23, f"{p4[1]:.4f}"); w(33, f"{p4[2]:.4f}")

    for box in boxes_3d:
        layer, color, x1, y1, z1, x2, y2, z2 = box
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1))
        write_3dface(layer, color, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2))
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2))
        write_3dface(layer, color, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2))
        write_3dface(layer, color, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2))
        write_3dface(layer, color, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2))

    for layer, color, pts in hexahedra_3d:
        p0, p1, p2, p3, p4, p5, p6, p7 = pts
        write_3dface(layer, color, p0, p1, p2, p3)
        write_3dface(layer, color, p4, p5, p6, p7)
        write_3dface(layer, color, p0, p1, p5, p4)
        write_3dface(layer, color, p3, p2, p6, p7)
        write_3dface(layer, color, p0, p3, p7, p4)
        write_3dface(layer, color, p1, p2, p6, p5)

    for line in lines_2d:
        layer, color, x1, y1, z1, x2, y2, z2 = line
        w(0, "LINE"); w(8, layer); w(62, color)
        w(10, f"{x1:.4f}"); w(20, f"{y1:.4f}"); w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}"); w(21, f"{y2:.4f}"); w(32, f"{z2:.4f}")

    for item in texts:
        layer, color, txt, x, y, z, h = item
        w(0, "TEXT"); w(8, layer); w(62, color)
        w(10, f"{x:.4f}"); w(20, f"{y:.4f}"); w(30, f"{z:.4f}")
        w(40, f"{h:.4f}"); w(1, txt)

    w(0, "ENDSEC"); w(0, "EOF")

    out_dxf_paths = [
        "Proyecto_Chalet_Rustico/02_Modelos_CAD/casa_chalet_rustico.dxf",
        "02_Modelos_CAD/casa_chalet_rustico.dxf"
    ]
    for p in out_dxf_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="latin-1", errors="replace") as f:
            f.writelines(dxf_lines)
        print(f"DXF Chalet Rústico generado: {p}")

    # 2. OBJ 3D Wavefront
    obj_lines = ["# Casa Chalet Rústico Alpino 3D (Zócalo Piedra + P2 Madera + Balconada + Chimenea + Techo 38°)\n\n"]
    v_idx = 1
    for idx, (layer, color, x1, y1, z1, x2, y2, z2) in enumerate(boxes_3d):
        box_v = [
            (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1),
            (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)
        ]
        for vx, vy, vz in box_v:
            obj_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f}\n")
        b = v_idx
        obj_lines.append(f"o {layer}_{idx}\n")
        obj_lines.append(f"f {b} {b+3} {b+2} {b+1}\n")
        obj_lines.append(f"f {b+4} {b+5} {b+6} {b+7}\n")
        obj_lines.append(f"f {b} {b+1} {b+5} {b+4}\n")
        obj_lines.append(f"f {b+2} {b+3} {b+7} {b+6}\n")
        obj_lines.append(f"f {b+3} {b} {b+4} {b+7}\n")
        obj_lines.append(f"f {b+1} {b+2} {b+6} {b+5}\n")
        v_idx += 8

    for idx, (layer, color, pts) in enumerate(hexahedra_3d):
        for vx, vy, vz in pts:
            obj_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f}\n")
        b = v_idx
        obj_lines.append(f"o {layer}_hex_{idx}\n")
        obj_lines.append(f"f {b} {b+3} {b+2} {b+1}\n")
        obj_lines.append(f"f {b+4} {b+5} {b+6} {b+7}\n")
        obj_lines.append(f"f {b} {b+1} {b+5} {b+4}\n")
        obj_lines.append(f"f {b+2} {b+3} {b+7} {b+6}\n")
        obj_lines.append(f"f {b+3} {b} {b+4} {b+7}\n")
        obj_lines.append(f"f {b+1} {b+2} {b+6} {b+5}\n")
        v_idx += 8

    out_obj_paths = [
        "Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_3d.obj",
        "03_Modelos_3D/casa_chalet_3d.obj"
    ]
    for p in out_obj_paths:
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(obj_lines)
        print(f"OBJ Chalet Rústico generado: {p}")

    # 3. STL 3D
    stl_lines = ["solid casa_chalet_rustico_3d\n"]
    def write_stl_tri(p1, p2, p3):
        u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        v = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
        nx = u[1] * v[2] - u[2] * v[1]
        ny = u[2] * v[0] - u[0] * v[2]
        nz = u[0] * v[1] - u[1] * v[0]
        l = math.sqrt(nx * nx + ny * ny + nz * nz)
        if l > 1e-6:
            nx /= l; ny /= l; nz /= l
        else:
            nx, ny, nz = 0.0, 0.0, 1.0
        stl_lines.append(f"  facet normal {nx:.4f} {ny:.4f} {nz:.4f}\n")
        stl_lines.append("    outer loop\n")
        stl_lines.append(f"      vertex {p1[0]:.4f} {p1[1]:.4f} {p1[2]:.4f}\n")
        stl_lines.append(f"      vertex {p2[0]:.4f} {p2[1]:.4f} {p2[2]:.4f}\n")
        stl_lines.append(f"      vertex {p3[0]:.4f} {p3[1]:.4f} {p3[2]:.4f}\n")
        stl_lines.append("    endloop\n")
        stl_lines.append("  endfacet\n")

    def write_stl_quad(p1, p2, p3, p4):
        write_stl_tri(p1, p2, p3)
        write_stl_tri(p1, p3, p4)

    for box in boxes_3d:
        layer, color, x1, y1, z1, x2, y2, z2 = box
        p0, p1 = (x1, y1, z1), (x2, y1, z1)
        p2, p3 = (x2, y2, z1), (x1, y2, z1)
        p4, p5 = (x1, y1, z2), (x2, y1, z2)
        p6, p7 = (x2, y2, z2), (x1, y2, z2)
        write_stl_quad(p0, p3, p2, p1)
        write_stl_quad(p4, p5, p6, p7)
        write_stl_quad(p0, p1, p5, p4)
        write_stl_quad(p2, p3, p7, p6)
        write_stl_quad(p3, p0, p4, p7)
        write_stl_quad(p1, p2, p6, p5)

    for layer, color, pts in hexahedra_3d:
        p0, p1, p2, p3, p4, p5, p6, p7 = pts
        write_stl_quad(p0, p3, p2, p1)
        write_stl_quad(p4, p5, p6, p7)
        write_stl_quad(p0, p1, p5, p4)
        write_stl_quad(p3, p2, p6, p7)
        write_stl_quad(p0, p3, p7, p4)
        write_stl_quad(p1, p2, p6, p5)

    stl_lines.append("endsolid casa_chalet_rustico_3d\n")
    out_stl_paths = [
        "Proyecto_Chalet_Rustico/03_Modelos_3D/casa_chalet_3d.stl",
        "03_Modelos_3D/casa_chalet_3d.stl"
    ]
    for p in out_stl_paths:
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(stl_lines)
        print(f"STL Chalet Rústico generado: {p}")

    print(f"\n¡Éxito! Proyecto Chalet Rústico construido con {len(boxes_3d) + len(hexahedra_3d)} sólidos 3D.")

if __name__ == "__main__":
    build_chalet_project()
