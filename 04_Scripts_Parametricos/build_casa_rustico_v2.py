"""
Generador Maestro del Proyecto Chalet Rústico Alpino V2 ("casa_rustico_v2.dxf", .obj, .stl)
Diseño bajo la Skill de Arquitecto Especialista en Estilo Rústico y Chalet para CAD.
Base estructural: casa_modificaciones.dxf

Características Clave del Rediseño V2:
1. Supresión total de la chimenea para máxima amplitud y pureza espacial en el Gran Salón.
2. Doble Balcón Frontal sobre Avenida 4:
   - Gran Balconada Rústica Techada Corrida para el área social (X: 0.15 a 5.20 m, Y: 21.71 a 23.31 m).
   - Balcón Privado Independiente para la Master Suite (X: 5.60 a 9.15 m, Y: 21.71 a 23.31 m), con celosía divisoria.
3. Ampliación Posterior Continua (Sótano a Último Piso):
   - Crujía posterior derecha (X: 6.25 a 9.15 m, Y: 0.00 a 3.50 m) completada para lograr volumetría 100% rectangular (9.00 x 21.71 m).
   - Sótano: Cava Rústica / Taller Subterráneo.
   - Planta Baja: Despacho Comercial Privado / Archivo.
   - Último Piso: Habitación 4 / Suite de Invitados / Estudio Alpino.
   - Columna 32 en (9.075, 0.075) completando la retícula estructural modular 4x9.
4. Preservación Estricta:
   - Sótano original, muros de retención y 8 columnas de 35x35 cm intactos.
   - Salón comercial PB de 98 m2, garaje de 2.80 m libres entre ejes, muro propio Eje 0 y baño intactos.
   - Ambas escaleras (bajada a sótano y subida a P2) 100% intactas en huella y desarrollo geométrico.
   - Terreno poligonal UTM, linderos y retiro de fondo de 3.00 m intactos.
"""

import os
import math
import struct

def build_rustico_v2_project():
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
    # PARÁMETROS VERTICALES Y GEOMÉTRICOS BASE
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso sótano (Altura libre = 2.40 m)
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa Planta Baja
    Z_P1_FLOOR     =  0.00   # Nivel piso acabado Planta Baja (Comercial + Garaje)
    H_P1           =  2.85   # Fondo de losa entrepiso / tope muros PB
    Z_P2_FLOOR     =  3.00   # Nivel piso acabado Último Piso (Planta Alta Chalet)
    H_P2_MURO      =  5.85   # Tope de muros madera / arranque de aleros
    Z_ALERO        =  5.40   # Cota inferior de aleros voladizos
    Z_CUMBRERA     =  9.72   # Cúspide de la cubierta alpina a dos aguas (38°)
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.00

    OFFSET_X = 0.00
    OFFSET_Y = 3.00   # Retiro posterior exacto
    Y_AV4    = 21.71  # Frente en Avenida 4 (Y_terreno = 24.71 m)
    X_CUMBRERA = 4.65 # Eje central longitudinal de cumbrera alpina

    ALERO_LATERAL   = 1.10
    ALERO_FRONTAL   = 1.20
    ALERO_POSTERIOR = 1.10

    def add_house_box(layer, color, x1, y1, z1, x2, y2, z2):
        add_box(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_line(layer, color, x1, y1, z1, x2, y2, z2):
        add_line(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_text(layer, color, text, x, y, z, h=0.22):
        add_text(layer, color, text, OFFSET_X + x, OFFSET_Y + y, z, h)

    def add_house_hex(layer, color, pts8):
        pts_off = [(OFFSET_X + px, OFFSET_Y + py, pz) for px, py, pz in pts8]
        add_hexahedron(layer, color, pts_off)

    def add_wall_with_openings_x(layer, color, x1, x2, y1, y2, z_bot, z_top, openings):
        openings = sorted(openings, key=lambda o: o[0])
        curr_x = x1
        for ox1, ox2, oz1, oz2 in openings:
            if ox1 > curr_x:
                add_house_box(layer, color, curr_x, y1, z_bot, ox1, y2, z_top)
            if oz1 > z_bot:
                add_house_box(layer, color, ox1, y1, z_bot, ox2, y2, oz1)
            if oz2 < z_top:
                add_house_box(layer, color, ox1, y1, oz2, ox2, y2, z_top)
            curr_x = ox2
        if curr_x < x2:
            add_house_box(layer, color, curr_x, y1, z_bot, x2, y2, z_top)

    def add_wall_with_openings_y(layer, color, x1, x2, y1, y2, z_bot, z_top, openings):
        openings = sorted(openings, key=lambda o: o[0])
        curr_y = y1
        for oy1, oy2, oz1, oz2 in openings:
            if oy1 > curr_y:
                add_house_box(layer, color, x1, curr_y, z_bot, x2, oy1, z_top)
            if oz1 > z_bot:
                add_house_box(layer, color, x1, oy1, z_bot, x2, oy2, oz1)
            if oz2 < z_top:
                add_house_box(layer, color, x1, oy1, oz2, x2, oy2, z_top)
            curr_y = oy2
        if curr_y < y2:
            add_house_box(layer, color, x1, curr_y, z_bot, x2, y2, z_top)

    # =========================================================================
    # 1. PLANTA SÓTANO (Z = -2.55 m) - INTACTO + NUEVA CAVA POSTERIOR RECTANGULAR
    # =========================================================================
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT  = "SOTANO_MUROS_INT_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    # Losa Sótano: original + ampliación rectangular hasta X=9.15 m en Y=0.00..3.50 m
    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 3.50, Z_SOT_FLOOR)
    add_house_box(L_SOT_SLAB, 8, 0.15, 3.50, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)

    # Escalera Tramo 1: Baja del Primer Piso (Z = 0.00 en Y = 7.40) al Sótano (Z = -2.55 en Y = 4.45), X: 0.30 a 1.40
    num_steps = 12
    step_dy = (7.40 - 4.45) / num_steps
    step_dz = (0.00 - Z_SOT_FLOOR) / num_steps
    for i in range(num_steps):
        y_s_top = 7.40 - i * step_dy
        y_s_bot = y_s_top - step_dy
        z_s_top = 0.00 - i * step_dz
        add_house_box("ESCALERA_3D", 7, 0.30, y_s_bot, Z_SOT_FLOOR, 1.40, y_s_top, z_s_top)
        add_house_line("PLANTA_SOTANO_2D", 7, 0.30, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muro Oeste Propio en Sótano (X: 0.15 a 0.30, Y: 0.00 a 8.30)
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur Sótano Posterior Rectangular Completo (Y: 0.00 a 0.15, X: 0.30 a 9.15)
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 9.15, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 2.50, Z_SOT_FLOOR + 1.00, Z_SOT_FLOOR + 2.10),  # Ventana Bodega Oeste
        (3.40, 4.10, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Celosía Central
        (7.00, 8.50, Z_SOT_FLOOR + 1.30, Z_SOT_FLOOR + 2.10),  # Ventana Nueva Cava Este
    ])

    # Muro Este de Sótano Completo Rectangular (X: 8.95 a 9.15, Y: 0.15 a 8.30)
    add_wall_with_openings_y(L_SOT_EXT, 4, 8.95, 9.15, 0.15, 8.30, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.20, 2.50, Z_SOT_FLOOR + 1.30, Z_SOT_FLOOR + 2.10),  # Ventana Cava Este
    ])

    # Muro Norte de Contención del Sótano (Y: 8.15 a 8.30, X: 0.30 a 9.15)
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Tabiquería Interna del Sótano Original
    add_wall_with_openings_x(L_SOT_INT, 4, 0.30, 6.00, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (3.95, 4.95, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_wall_with_openings_y(L_SOT_INT, 4, 2.80, 2.95, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (2.60, 3.40, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_house_box(L_SOT_INT, 4, 2.07, 0.15, Z_SOT_FLOOR, 2.80, 0.75, Z_P1_SLAB_BOT)
    add_house_box(L_SOT_INT, 4, 4.60, 0.15, Z_SOT_FLOOR, 4.75, 2.65, Z_P1_SLAB_BOT)
    add_wall_with_openings_x(L_SOT_INT, 4, 4.75, 6.25, 1.94, 2.09, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (4.80, 5.50, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_wall_with_openings_y(L_SOT_INT, 4, 5.85, 6.00, 3.65, 8.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (7.25, 8.05, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_house_box(L_SOT_INT, 4, 1.40, 4.45, Z_SOT_FLOOR, 1.55, 8.15, Z_P1_SLAB_BOT)

    # Tabique Divisorio de la NUEVA CAVA SUBTERRÁNEA (X: 6.25 a 6.40, Y: 0.15 a 3.50) con puerta
    add_wall_with_openings_y(L_SOT_INT, 4, 6.25, 6.40, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.50, 2.40, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT), # Puerta acceso a nueva cava
    ])

    # 8 Columnas Sótano 35x35 cm Originales
    sot_cols_axes = [
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)

    # NUEVA COLUMNA 32 EN SÓTANO (35x35 cm en Eje 3 x Posterior)
    add_house_box(L_SOT_COL, 1, 9.075 - 0.175, 0.075 - 0.175, Z_SOT_FLOOR, 9.075 + 0.175, 0.075 + 0.175, Z_P1_SLAB_BOT)

    # =========================================================================
    # 2. PLANTA BAJA (Z = 0.00 m) - INTACTA + NUEVO DESPACHO COMERCIAL RECTANGULAR
    # =========================================================================
    L_P1_SLAB = "LOSA_PISO_3D"
    L_P1_EXT  = "MUROS_EXTERIORES_3D"
    L_P1_INT  = "MUROS_INTERIORES_3D"
    L_P1_COL  = "COLUMNAS_3D"

    # Losa Planta Baja extendida completa rectangular (X: 0.15..9.15, Y: 0.00..21.71)
    add_house_box(L_P1_SLAB, 8, 0.15, 0.00, Z_P1_SLAB_BOT, 9.15, 3.50, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 3.50, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR)

    # Muro Lateral Izquierdo PROPIO (X: 0.15 a 0.30, Y: 0.00 a 21.71 m)
    add_house_box(L_P1_EXT, 7, 0.15, 0.00, Z_P1_FLOOR, 0.30, Y_AV4, H_P1)

    # Fachada Frontal en Avenida 4 (Eje A0, Y: 21.56 a 21.71, X: 0.15 a 9.15):
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P1_FLOOR, H_P1, [
        (0.40, 2.65, 0.00, 2.25),   # Portón Vehicular Garaje 2.25 m
        (3.15, 5.65, 0.00, 2.40),   # Vitrina Comercial 1
        (6.20, 8.80, 0.00, 2.40),   # Vitrina Comercial 2 y Acceso
    ])

    # Muro Lateral Derecho sobre Eje 3 Completo Rectangular (X: 9.00 a 9.15, Y: 0.00 a 21.71 m)
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 0.00, Y_AV4, Z_P1_FLOOR, H_P1, [
        (1.00,  2.50, 1.00, 2.10),  # Ventana Nuevo Despacho Comercial
        (4.10,  5.00, 1.10, 2.00),  # Ventana Baño del Local
        (6.30,  8.00, 1.00, 2.10),  # Ventanal Local tramo sur
        (9.65, 11.85, 1.00, 2.10),  # Ventanal Local tramo centro-sur
        (13.15, 14.05, 1.10, 2.00), # Ventana baño / ventilación
        (15.50, 17.70, 1.00, 2.10), # Ventanal Local tramo norte
        (18.80, 21.00, 1.00, 2.10), # Ventanal Comercial frente
    ])

    # Muro Sur Posterior Rectangular Completo PB (Y: 0.00 a 0.15, X: 0.15 a 9.15 m)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, 0.00, 0.15, Z_P1_FLOOR, H_P1, [
        (0.55, 2.35, 1.15, 2.60),  # Ventana Depósito Original
        (4.10, 5.10, 1.00, 2.10),  # Ventanal Taller/Oficina
        (7.00, 8.50, 1.00, 2.10),  # Ventana Nuevo Despacho Posterior
    ])

    # Muros Interiores Planta Baja Originales (Intactos)
    add_house_box(L_P1_INT, 7, 2.75, 0.15, Z_P1_FLOOR, 2.90, Y_AV4 - 0.15, H_P1) # Muro Divisorio Garaje
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 8.80, 8.95, Z_P1_FLOOR, H_P1, [(1.65, 2.55, 0.00, H_DOOR)])
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.35, H_P1)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 4.25, 4.40, Z_P1_FLOOR, H_P1, [(1.65, 2.45, 0.00, H_DOOR)])
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 1.65, 1.80, Z_P1_FLOOR, H_P1, [(0.95, 2.05, 0.00, H_DOOR)])
    # Baño del Local PB
    add_house_box(L_P1_INT, 7, 5.85, 5.40, Z_P1_FLOOR, 9.00, 5.55, H_P1)
    add_wall_with_openings_y(L_P1_INT, 7, 5.85, 6.00, 3.65, 5.40, Z_P1_FLOOR, H_P1, [(3.95, 4.75, 0.00, H_DOOR)])
    add_wall_with_openings_x(L_P1_INT, 7, 2.90, 6.25, 3.50, 3.65, Z_P1_FLOOR, H_P1, [(4.05, 4.90, 0.00, H_DOOR)])

    # NUEVO DESPACHO COMERCIAL POSTERIOR (X: 6.25 a 9.00, Y: 0.15 a 3.50 m)
    # Muro divisorio norte del despacho sobre Eje G (Y: 3.50 a 3.65, X: 6.25 a 9.00 m) con puerta de acceso
    add_wall_with_openings_x(L_P1_INT, 7, 6.25, 9.00, 3.50, 3.65, Z_P1_FLOOR, H_P1, [
        (7.00, 7.90, 0.00, H_DOOR), # Puerta desde Local Comercial a Nuevo Despacho
    ])
    # Muro divisorio oeste del despacho (X: 6.25 a 6.40, Y: 0.15 a 3.50 m)
    add_house_box(L_P1_INT, 7, 6.25, 0.15, Z_P1_FLOOR, 6.40, 3.50, H_P1)

    # Escalera Tramo 2 (Sube a P2, 100% intacta, X: 1.55 a 2.65, Y: 4.40 a 7.35 m)
    for i in range(12):
        y_s_top = 4.40 + (i + 1) * (2.95 / 12)
        y_s_bot = y_s_top - (2.95 / 12)
        z_s_bot = 0.00 + i * (3.00 / 12)
        z_s_top = z_s_bot + (3.00 / 12)
        add_house_box("P2_ESCALERA_3D", 7, 1.55, y_s_bot, 0.00, 2.65, y_s_top, z_s_top)

    # =========================================================================
    # 3. COLUMNAS ESTRUCTURALES (31 ORIGINALES + COLUMNA 32 NUEVA)
    # =========================================================================
    cols_all_axes = [
        # Eje A0 sobre Avenida 4 (Y = 21.585)
        (0.275, 21.585), (2.825, 21.585), (5.925, 21.585), (9.075, 21.585),
        # Eje A (Y = 18.575)
        (0.275, 18.575), (2.825, 18.575), (5.925, 18.575), (9.075, 18.575),
        # Eje B (Y = 16.325)
        (0.275, 16.325), (2.825, 16.325), (5.925, 16.325),
        # Eje C (Y = 14.625)
        (9.075, 14.625),
        # Eje D (Y = 12.025)
        (0.275, 12.025), (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
        # Eje E (Y = 8.875)
        (0.275, 8.875),  (2.825, 8.875),  (5.925, 8.875),  (9.075, 8.875),
        # Eje F (Y = 6.575)
        (0.275, 6.575),  (2.825, 6.575),  (5.925, 6.575),  (9.075, 6.575),
        # Eje G (Y = 3.575)
        (0.275, 3.575),  (2.825, 3.575),  (5.925, 3.575),  (9.075, 3.575),
        # Eje Posterior (Y = 0.075) - 3 Originales + COLUMNA 32 NUEVA
        (0.275, 0.075),  (2.825, 0.075),  (5.925, 0.075),  (9.075, 0.075)
    ]

    for cx, cy in cols_all_axes:
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)

    L_P2_COL = "P2_COLUMNAS_TIMBER_3D"
    for cx, cy in cols_all_axes:
        add_house_box(L_P2_COL, 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, H_P2_MURO)

    # =========================================================================
    # 4. REDISEÑO DEL ÚLTIMO PISO: RESIDENCIA CHALET RÚSTICO ALPINO V2
    #    (SIN CHIMENEA, CON DOBLE BALCÓN Y HABITACIÓN POSTERIOR RECTANGULAR)
    # =========================================================================
    L_P2_SLAB   = "P2_LOSA_PISO_3D"
    L_P2_WALL   = "P2_MUROS_TIMBER_3D"
    L_P2_INT    = "P2_TABIQUES_MADERA_3D"
    L_P2_BALC_S = "P2_BALCON_SOCIAL_3D"
    L_P2_BALC_M = "P2_BALCON_MASTER_3D"
    L_P2_ISLA   = "P2_ISLA_COCINA_3D"

    # Losa de entrepiso Último Piso (Z: 2.85 a 3.00 m) 100% rectangular con hueco de escalera
    add_house_box(L_P2_SLAB, 7, 0.15, 0.00, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 0.15, 4.40, H_P1, 0.30, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR)

    # Muro Lateral Izquierdo Propio en Madera Machihembrada (X: 0.15 a 0.35, Y: 0.00 a 21.71 m)
    add_house_box(L_P2_WALL, 34, 0.15, 0.00, Z_P2_FLOOR, 0.35, Y_AV4, H_P2_MURO)

    # Muro Lateral Derecho sobre Eje 3 en Madera (X: 8.95 a 9.15, Y: 0.00 a 21.71 m)
    add_wall_with_openings_y(L_P2_WALL, 34, 8.95, 9.15, 0.00, Y_AV4, Z_P2_FLOOR, H_P2_MURO, [
        (1.00,  2.60, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana Habitación 4 (Posterior)
        (4.20,  5.10, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.00), # Ventana Baño Familiar
        (6.50,  8.20, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana Habitación 3
        (10.00, 11.80, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana Habitación 2 / Pasillo
        (13.20, 14.20, Z_P2_FLOOR + 1.20, Z_P2_FLOOR + 2.00), # Ventana Baño Master Suite
        (16.50, 18.50, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana lateral Master Suite
    ])

    # Muro Sur Posterior en Madera Machihembrada (Y: 0.00 a 0.18, X: 0.15 a 9.15 m)
    add_wall_with_openings_x(L_P2_WALL, 34, 0.15, 9.15, 0.00, 0.18, Z_P2_FLOOR, H_P2_MURO, [
        (0.80,  2.20, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.10), # Ventana Lavandería
        (3.00,  4.20, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana Galería
        (6.50,  8.20, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Ventana Habitación 4 hacia patio
    ])

    # Fachada Frontal sobre Avenida 4 (Y: 21.53 a 21.71 m, X: 0.15 a 9.15 m)
    # Puertas francesas independientes para ambos balcones
    add_wall_with_openings_x(L_P2_WALL, 34, 0.15, 9.15, Y_AV4 - 0.18, Y_AV4, Z_P2_FLOOR, H_P2_MURO, [
        (0.60, 2.20, Z_P2_FLOOR + 0.90, Z_P2_FLOOR + 2.20),   # Ventana Gran Salón
        (2.60, 4.40, Z_P2_FLOOR, Z_P2_FLOOR + 2.30),          # PUERTA FRANCESA GRAN SALÓN -> BALCÓN SOCIAL
        (6.80, 8.40, Z_P2_FLOOR, Z_P2_FLOOR + 2.30),          # PUERTA FRANCESA MASTER SUITE -> BALCÓN PRIVADO
    ])

    # --- DOBLE BALCÓN FRONTAL RÚSTICO SOBRE AVENIDA 4 ---
    # 1. GRAN BALCONADA SOCIAL TECHADA (X: 0.15 a 5.20 m, Y: 21.71 a 23.31 m - Voladizo 1.60 m)
    add_house_box(L_P2_BALC_S, 30, 0.15, Y_AV4, H_P1, 5.20, Y_AV4 + 1.60, Z_P2_FLOOR) # Losa madera
    # Vigas pasantes de soporte del balcón social
    for vx in [0.40, 1.60, 2.80, 4.00, 5.10]:
        add_house_box(L_P2_BALC_S, 30, vx - 0.08, Y_AV4 - 0.80, H_P1 - 0.22, vx + 0.08, Y_AV4 + 1.60, H_P1)
    # Barandilla frontal social con Cruz de San Andrés
    add_house_box(L_P2_BALC_S, 30, 0.15, Y_AV4 + 1.55, Z_P2_FLOOR, 5.20, Y_AV4 + 1.60, Z_P2_FLOOR + 1.05)
    add_house_box(L_P2_BALC_S, 30, 0.15, Y_AV4, Z_P2_FLOOR, 0.20, Y_AV4 + 1.60, Z_P2_FLOOR + 1.05) # Baranda oeste

    # 2. BALCÓN PRIVADO INDEPENDIENTE PARA MASTER SUITE (X: 5.60 a 9.15 m, Y: 21.71 a 23.31 m)
    add_house_box(L_P2_BALC_M, 30, 5.60, Y_AV4, H_P1, 9.15, Y_AV4 + 1.60, Z_P2_FLOOR) # Losa madera
    # Vigas pasantes de soporte balcón Master Suite
    for vx in [5.80, 6.90, 8.00, 9.05]:
        add_house_box(L_P2_BALC_M, 30, vx - 0.08, Y_AV4 - 0.80, H_P1 - 0.22, vx + 0.08, Y_AV4 + 1.60, H_P1)
    # Barandilla frontal Master Suite con Cruz de San Andrés
    add_house_box(L_P2_BALC_M, 30, 5.60, Y_AV4 + 1.55, Z_P2_FLOOR, 9.15, Y_AV4 + 1.60, Z_P2_FLOOR + 1.05)
    add_house_box(L_P2_BALC_M, 30, 9.10, Y_AV4, Z_P2_FLOOR, 9.15, Y_AV4 + 1.60, Z_P2_FLOOR + 1.05) # Baranda este

    # CELOSÍA DIVISORIA DE MADERA MACIZA ENTRE AMBOS BALCONES (X: 5.20 a 5.60 m)
    add_house_box(L_P2_WALL, 34, 5.20, Y_AV4, Z_P2_FLOOR, 5.60, Y_AV4 + 1.60, Z_P2_FLOOR + 1.80)

    # --- TABIQUERÍA INTERIOR DEL CHALET RÚSTICO V2 ---
    # Muro Divisorio Eje 2 (X: 5.20 a 5.35 m) separando Gran Salón/Cocina de Zona Íntima (Y: 3.65 a 21.53 m)
    add_wall_with_openings_y(L_P2_INT, 34, 5.20, 5.35, 3.65, Y_AV4 - 0.18, Z_P2_FLOOR, H_P2_MURO, [
        (4.50, 5.40, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),   # Puerta Habitación 4 (Posterior)
        (7.20, 8.10, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),   # Puerta Baño Familiar
        (9.50, 10.40, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),  # Puerta Habitación 3
        (15.40, 16.30, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR), # Puerta Master Suite
    ])

    # Master Suite: División de Baño y Vestidor
    add_house_box(L_P2_INT, 34, 5.35, 15.00, Z_P2_FLOOR, 8.95, 15.15, H_P2_MURO) # Muro sur suite
    add_house_box(L_P2_INT, 34, 6.80, 12.70, Z_P2_FLOOR, 8.95, 12.85, H_P2_MURO) # Baño suite
    add_house_box(L_P2_INT, 34, 6.80, 12.85, Z_P2_FLOOR, 6.95, 15.00, H_P2_MURO) # Vestidor

    # Habitación 3: Muros divisorios (Y: 8.85 a 12.70 m, X: 5.35 a 8.95 m)
    add_house_box(L_P2_INT, 34, 5.35, 8.85, Z_P2_FLOOR, 8.95, 9.00, H_P2_MURO)

    # Baño Familiar Principal (Y: 6.80 a 8.85 m, X: 5.35 a 8.95 m)
    add_house_box(L_P2_INT, 34, 5.35, 6.80, Z_P2_FLOOR, 8.95, 6.95, H_P2_MURO)

    # NUEVA HABITACIÓN 4 / ESTUDIO DE MONTAÑA (Crujía Posterior Derecha, Y: 0.18 a 3.65 m, X: 5.35 a 8.95 m)
    # Muro divisorio norte de Hab 4 sobre Eje G (Y: 3.50 a 3.65 m, X: 5.35 a 8.95 m) con puerta
    add_wall_with_openings_x(L_P2_INT, 34, 5.35, 8.95, 3.50, 3.65, Z_P2_FLOOR, H_P2_MURO, [
        (6.00, 6.90, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR), # Puerta acceso Habitación 4
    ])

    # Habitación 2 (Izquierda, Y: 4.40 a 8.85 m, X: 0.35 a 5.20 m)
    add_house_box(L_P2_INT, 34, 0.35, 8.85, Z_P2_FLOOR, 5.20, 9.00, H_P2_MURO)
    add_house_box(L_P2_INT, 34, 0.35, 4.40, Z_P2_FLOOR, 5.20, 4.55, H_P2_MURO)

    # Lavandería y Galería Posterior (Izquierda, Y: 0.18 a 4.40 m, X: 0.35 a 5.20 m)
    add_wall_with_openings_y(L_P2_INT, 34, 2.75, 2.90, 0.18, 4.40, Z_P2_FLOOR, H_P2_MURO, [
        (2.00, 2.90, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])

    # Isla Central de Madera Maciza en Cocina Alpina (2.60 x 0.95 m, X: 1.80 a 4.40 m, Y: 10.80 a 11.75 m)
    add_house_box(L_P2_ISLA, 30, 1.80, 10.80, Z_P2_FLOOR, 4.40, 11.75, Z_P2_FLOOR + 0.90) # Mueble roble
    add_house_box(L_P2_ISLA, 34, 1.75, 10.75, Z_P2_FLOOR + 0.90, 4.45, 11.80, Z_P2_FLOOR + 0.96) # Encimera maciza

    # =========================================================================
    # 5. CUBIERTA ALPINA A DOS AGUAS (38° PENDIENTE, ALEROS Y CANECILLOS)
    #    (SIN PENETRACIÓN DE CHIMENEA, CUMBRERA CONTINUA A Z = +9.72 m)
    # =========================================================================
    L_ROOF      = "CUBIERTA_ALPINA_3D"
    L_RAFTERS   = "CUBIERTA_VIGAS_CANECILLOS_3D"
    L_GABLE     = "FRONTON_MADERA_3D"

    X_CUMBRERA  = 4.65
    X_EAVE_LEFT = -0.95
    X_EAVE_RGHT = 10.25
    Y_ROOF_MIN  = -1.10
    Y_ROOF_MAX  = 23.31

    # Faldón Izquierdo (Oeste, X: -0.95 a 4.65 m)
    p_ro_w1 = (X_EAVE_LEFT, Y_ROOF_MIN, Z_ALERO)
    p_ro_w2 = (X_CUMBRERA,  Y_ROOF_MIN, Z_CUMBRERA)
    p_ro_w3 = (X_CUMBRERA,  Y_ROOF_MAX, Z_CUMBRERA)
    p_ro_w4 = (X_EAVE_LEFT, Y_ROOF_MAX, Z_ALERO)
    p_ro_w5 = (X_EAVE_LEFT, Y_ROOF_MIN, Z_ALERO + 0.20)
    p_ro_w6 = (X_CUMBRERA,  Y_ROOF_MIN, Z_CUMBRERA + 0.20)
    p_ro_w7 = (X_CUMBRERA,  Y_ROOF_MAX, Z_CUMBRERA + 0.20)
    p_ro_w8 = (X_EAVE_LEFT, Y_ROOF_MAX, Z_ALERO + 0.20)
    add_house_hex(L_ROOF, 9, [p_ro_w1, p_ro_w2, p_ro_w3, p_ro_w4, p_ro_w5, p_ro_w6, p_ro_w7, p_ro_w8])

    # Faldón Derecho (Este, X: 4.65 a 10.25 m)
    p_ro_e1 = (X_CUMBRERA,  Y_ROOF_MIN, Z_CUMBRERA)
    p_ro_e2 = (X_EAVE_RGHT, Y_ROOF_MIN, Z_ALERO)
    p_ro_e3 = (X_EAVE_RGHT, Y_ROOF_MAX, Z_ALERO)
    p_ro_e4 = (X_CUMBRERA,  Y_ROOF_MAX, Z_CUMBRERA)
    p_ro_e5 = (X_CUMBRERA,  Y_ROOF_MIN, Z_CUMBRERA + 0.20)
    p_ro_e6 = (X_EAVE_RGHT, Y_ROOF_MIN, Z_ALERO + 0.20)
    p_ro_e7 = (X_EAVE_RGHT, Y_ROOF_MAX, Z_ALERO + 0.20)
    p_ro_e8 = (X_CUMBRERA,  Y_ROOF_MAX, Z_CUMBRERA + 0.20)
    add_house_hex(L_ROOF, 9, [p_ro_e1, p_ro_e2, p_ro_e3, p_ro_e4, p_ro_e5, p_ro_e6, p_ro_e7, p_ro_e8])

    # Frontón Frontal en Madera Machihembrada sobre Avenida 4 (Y = 21.71 m, Z: 5.85 a 9.72 m)
    fronton_f1 = (0.15, Y_AV4, H_P2_MURO)
    fronton_f2 = (X_CUMBRERA, Y_AV4, Z_CUMBRERA)
    fronton_f3 = (9.15, Y_AV4, H_P2_MURO)
    fronton_f4 = (0.15, Y_AV4 + 0.15, H_P2_MURO)
    fronton_f5 = (X_CUMBRERA, Y_AV4 + 0.15, Z_CUMBRERA)
    fronton_f6 = (9.15, Y_AV4 + 0.15, H_P2_MURO)
    add_house_hex(L_GABLE, 34, [fronton_f1, fronton_f2, fronton_f3, fronton_f1, fronton_f4, fronton_f5, fronton_f6, fronton_f4])

    # Frontón Posterior sobre Patio (Y = 0.00 m, Z: 5.85 a 9.72 m)
    fronton_p1 = (0.15, 0.00, H_P2_MURO)
    fronton_p2 = (X_CUMBRERA, 0.00, Z_CUMBRERA)
    fronton_p3 = (9.15, 0.00, H_P2_MURO)
    fronton_p4 = (0.15, 0.15, H_P2_MURO)
    fronton_p5 = (X_CUMBRERA, 0.15, Z_CUMBRERA)
    fronton_p6 = (9.15, 0.15, H_P2_MURO)
    add_house_hex(L_GABLE, 34, [fronton_p1, fronton_p2, fronton_p3, fronton_p1, fronton_p4, fronton_p5, fronton_p6, fronton_p4])

    # Canecillos Vistos y Pares de Techo Expuestos bajo los aleros (cada 1.20 m longitudinal)
    num_canecillos = 21
    dy_can = (Y_ROOF_MAX - Y_ROOF_MIN) / num_canecillos
    for i in range(num_canecillos + 1):
        cy = Y_ROOF_MIN + i * dy_can
        # Canecillo Alero Oeste
        add_house_box(L_RAFTERS, 30, X_EAVE_LEFT, cy - 0.06, Z_ALERO - 0.18, 0.35, cy + 0.06, Z_ALERO)
        # Canecillo Alero Este
        add_house_box(L_RAFTERS, 30, 8.95, cy - 0.06, Z_ALERO - 0.18, X_EAVE_RGHT, cy + 0.06, Z_ALERO)

    # =========================================================================
    # 6. TERRENO NO RECTANGULAR UTM Y CERCA PERIMETRAL (100% INTACTOS)
    # =========================================================================
    L_TERR  = "TERRENO_3D"
    P4_LOC = (0.0000,  0.0000)
    P1_LOC = (0.0000, 24.7060)
    P2_LOC = (11.3703, 24.9409)
    P3_LOC = (10.8043,  0.2311)

    def x_right(y):
        return P3_LOC[0] + (P2_LOC[0] - P3_LOC[0]) * ((y - P3_LOC[1]) / (P2_LOC[1] - P3_LOC[1]))

    def y_rear(x):
        return P4_LOC[1] + (P3_LOC[1] - P4_LOC[1]) * (x / P3_LOC[0])

    y_sot_start = OFFSET_Y
    add_hexahedron(L_TERR, 3, [
        (0.00,        y_rear(0.00),    Z_SOT_FLOOR - 0.20),
        (P3_LOC[0],   P3_LOC[1],       Z_SOT_FLOOR - 0.20),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR - 0.20),
        (0.00,        y_sot_start,     Z_SOT_FLOOR - 0.20),
        (0.00,        y_rear(0.00),    Z_SOT_FLOOR),
        (P3_LOC[0],   P3_LOC[1],       Z_SOT_FLOOR),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR),
        (0.00,        y_sot_start,     Z_SOT_FLOOR),
    ])

    steps = [
        (OFFSET_Y + 0.00, OFFSET_Y + 3.50, -2.55, -2.00),
        (OFFSET_Y + 3.50, OFFSET_Y + 7.35, -2.00, -1.20),
        (OFFSET_Y + 7.35, OFFSET_Y + 11.85, -1.20, -0.60),
        (OFFSET_Y + 11.85, OFFSET_Y + 16.35, -0.60, -0.20),
        (OFFSET_Y + 16.35, OFFSET_Y + 21.71, -0.20,  0.00),
    ]
    for y1_s, y2_s, z1_s, z2_s in steps:
        add_hexahedron(L_TERR, 3, [
            (9.15, y1_s, z1_s - 0.20),
            (x_right(y1_s), y1_s, z1_s - 0.20),
            (x_right(y2_s), y2_s, z2_s - 0.20),
            (9.15, y2_s, z2_s - 0.20),
            (9.15, y1_s, z1_s),
            (x_right(y1_s), y1_s, z1_s),
            (x_right(y2_s), y2_s, z2_s),
            (9.15, y2_s, z2_s),
        ])

    # =========================================================================
    # 7. EXPORTADORES A FORMATOS DXF, OBJ Y STL
    # =========================================================================
    # 1. DXF 2D/3D Completo
    dxf_lines = []
    def w(code, val):
        dxf_lines.append(f"{code}\n{val}\n")

    w(0, "SECTION"); w(2, "HEADER")
    w(9, "$ACADVER"); w(1, "AC1015")
    w(9, "$INSUNITS"); w(70, 6) # Metros
    w(0, "ENDSEC")

    w(0, "SECTION"); w(2, "TABLES")
    w(0, "TABLE"); w(2, "LAYER"); w(70, 15)
    layers_def = [
        ("0", 7), ("DEFPOINTS", 7),
        ("SOTANO_LOSA_3D", 8), ("SOTANO_MUROS_EXT_3D", 4), ("SOTANO_MUROS_INT_3D", 4), ("SOTANO_COLUMNAS_3D", 1),
        ("LOSA_PISO_3D", 8), ("MUROS_EXTERIORES_3D", 7), ("MUROS_INTERIORES_3D", 7), ("COLUMNAS_3D", 1),
        ("ESCALERA_3D", 7), ("P2_ESCALERA_3D", 7), ("P2_COLUMNAS_TIMBER_3D", 1),
        ("P2_LOSA_PISO_3D", 7), ("P2_MUROS_TIMBER_3D", 34), ("P2_TABIQUES_MADERA_3D", 34),
        ("P2_BALCON_SOCIAL_3D", 30), ("P2_BALCON_MASTER_3D", 30), ("P2_ISLA_COCINA_3D", 30),
        ("CUBIERTA_ALPINA_3D", 9), ("CUBIERTA_VIGAS_CANECILLOS_3D", 30), ("FRONTON_MADERA_3D", 34),
        ("TERRENO_3D", 3), ("EJES_COTAS_2D", 3)
    ]
    for lname, lcol in layers_def:
        w(0, "LAYER"); w(2, lname); w(70, 0); w(62, lcol); w(6, "CONTINUOUS")
    w(0, "ENDSEC"); w(0, "ENDSEC")

    w(0, "SECTION"); w(2, "ENTITIES")

    def write_3dface(layer, color, p1, p2, p3, p4):
        w(0, "3DFACE"); w(8, layer); w(62, color)
        w(10, f"{p1[0]:.4f}"); w(20, f"{p1[1]:.4f}"); w(30, f"{p1[2]:.4f}")
        w(11, f"{p2[0]:.4f}"); w(21, f"{p2[1]:.4f}"); w(31, f"{p2[2]:.4f}")
        w(12, f"{p3[0]:.4f}"); w(22, f"{p3[1]:.4f}"); w(32, f"{p3[2]:.4f}")
        w(13, f"{p4[0]:.4f}"); w(23, f"{p4[1]:.4f}"); w(33, f"{p4[2]:.4f}")

    for item in boxes_3d:
        layer, color, x1, y1, z1, x2, y2, z2 = item
        p1, p2, p3, p4 = (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1)
        p5, p6, p7, p8 = (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)
        write_3dface(layer, color, p1, p4, p3, p2) # Abajo
        write_3dface(layer, color, p5, p6, p7, p8) # Arriba
        write_3dface(layer, color, p1, p2, p6, p5) # Sur
        write_3dface(layer, color, p2, p3, p7, p6) # Este
        write_3dface(layer, color, p3, p4, p8, p7) # Norte
        write_3dface(layer, color, p4, p1, p5, p8) # Oeste

    for item in hexahedra_3d:
        layer, color, pts = item
        p0, p1, p2, p3, p4, p5, p6, p7 = pts
        write_3dface(layer, color, p0, p3, p2, p1)
        write_3dface(layer, color, p4, p5, p6, p7)
        write_3dface(layer, color, p0, p1, p5, p4)
        write_3dface(layer, color, p1, p2, p6, p5)
        write_3dface(layer, color, p2, p3, p7, p6)
        write_3dface(layer, color, p3, p0, p4, p7)

    for item in lines_2d:
        layer, color, x1, y1, z1, x2, y2, z2 = item
        w(0, "LINE"); w(8, layer); w(62, color)
        w(10, f"{x1:.4f}"); w(20, f"{y1:.4f}"); w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}"); w(21, f"{y2:.4f}"); w(31, f"{z2:.4f}")

    for item in texts:
        layer, color, txt, x, y, z, h = item
        w(0, "TEXT"); w(8, layer); w(62, color)
        w(10, f"{x:.4f}"); w(20, f"{y:.4f}"); w(30, f"{z:.4f}")
        w(40, f"{h:.4f}"); w(1, txt)

    w(0, "ENDSEC"); w(0, "EOF")

    out_dxf_path = "02_Modelos_CAD/casa_rustico_v2.dxf"
    os.makedirs(os.path.dirname(out_dxf_path), exist_ok=True)
    with open(out_dxf_path, "w", encoding="latin-1", errors="replace") as f:
        f.writelines(dxf_lines)
    print(f"DXF Chalet Rústico V2 generado: {out_dxf_path}")

    # 2. OBJ 3D Wavefront
    obj_lines = ["# Casa Chalet Rústico Alpino V2 3D (Sin chimenea, doble balcón, ampliación rectangular)\n\n"]
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
        obj_lines.append(f"f {b+1} {b+2} {b+6} {b+5}\n")
        obj_lines.append(f"f {b+2} {b+3} {b+7} {b+6}\n")
        obj_lines.append(f"f {b+3} {b} {b+4} {b+7}\n")
        v_idx += 8

    for idx, (layer, color, pts) in enumerate(hexahedra_3d):
        for vx, vy, vz in pts:
            obj_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f}\n")
        b = v_idx
        obj_lines.append(f"o {layer}_hex_{idx}\n")
        obj_lines.append(f"f {b} {b+3} {b+2} {b+1}\n")
        obj_lines.append(f"f {b+4} {b+5} {b+6} {b+7}\n")
        obj_lines.append(f"f {b} {b+1} {b+5} {b+4}\n")
        obj_lines.append(f"f {b+1} {b+2} {b+6} {b+5}\n")
        obj_lines.append(f"f {b+2} {b+3} {b+7} {b+6}\n")
        obj_lines.append(f"f {b+3} {b} {b+4} {b+7}\n")
        v_idx += 8

    out_obj_path = "03_Modelos_3D/casa_rustico_v2_3d.obj"
    os.makedirs(os.path.dirname(out_obj_path), exist_ok=True)
    with open(out_obj_path, "w", encoding="utf-8") as f:
        f.writelines(obj_lines)
    print(f"OBJ Chalet Rústico V2 generado: {out_obj_path}")

    # 3. STL Binario
    triangles = []
    def add_quad(p1, p2, p3, p4):
        triangles.append((p1, p2, p3))
        triangles.append((p1, p3, p4))

    for item in boxes_3d:
        _, _, x1, y1, z1, x2, y2, z2 = item
        p1, p2, p3, p4 = (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1)
        p5, p6, p7, p8 = (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)
        add_quad(p1, p4, p3, p2)
        add_quad(p5, p6, p7, p8)
        add_quad(p1, p2, p6, p5)
        add_quad(p2, p3, p7, p6)
        add_quad(p3, p4, p8, p7)
        add_quad(p4, p1, p5, p8)

    for item in hexahedra_3d:
        _, _, pts = item
        p0, p1, p2, p3, p4, p5, p6, p7 = pts
        add_quad(p0, p3, p2, p1)
        add_quad(p4, p5, p6, p7)
        add_quad(p0, p1, p5, p4)
        add_quad(p1, p2, p6, p5)
        add_quad(p2, p3, p7, p6)
        add_quad(p3, p0, p4, p7)

    header = b'STL Binary 3D Casa Chalet Rustico V2 (Rectangular, sin chimenea)'.ljust(80, b'\0')
    stl_bytes = bytearray(header)
    stl_bytes.extend(struct.pack('<I', len(triangles)))
    for p1, p2, p3 in triangles:
        stl_bytes.extend(struct.pack('<3f', 0.0, 0.0, 0.0))
        stl_bytes.extend(struct.pack('<3f', p1[0], p1[1], p1[2]))
        stl_bytes.extend(struct.pack('<3f', p2[0], p2[1], p2[2]))
        stl_bytes.extend(struct.pack('<3f', p3[0], p3[1], p3[2]))
        stl_bytes.extend(struct.pack('<H', 0))

    out_stl_path = "03_Modelos_3D/casa_rustico_v2_3d.stl"
    os.makedirs(os.path.dirname(out_stl_path), exist_ok=True)
    with open(out_stl_path, "wb") as f:
        f.write(stl_bytes)
    print(f"STL Chalet Rústico V2 generado: {out_stl_path}")

    total_solids = len(boxes_3d) + len(hexahedra_3d)
    print(f"\n¡Éxito! Proyecto Chalet Rústico V2 construido con {total_solids} sólidos 3D.")
    print(f"- Sótano preservado idéntico + Nueva Cava Posterior")
    print(f"- Planta Baja preservada idéntica (Local 98m2 + Garaje + Baño) + Nuevo Despacho Comercial")
    print(f"- Contorno perimetral completamente rectangular (9.00 x 21.71 m)")
    print(f"- 32 Columnas en total perfectamente alineadas en PB y P2")
    print(f"- Rediseño V2 ejecutado: Sin chimenea, Doble Balcón (Social y Master Suite), Habitación 4 posterior y cubierta alpina a 38°.")

if __name__ == "__main__":
    build_rustico_v2_project()
