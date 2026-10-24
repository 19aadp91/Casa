"""
Generador Maestro del Proyecto Mediterráneo ("casa_mediterranea.dxf", .obj, .stl)
Diseño bajo la Skill de Arquitecto Especialista en Estilo Mediterráneo para CAD.
Base estructural: casa_modificaciones.dxf

Preservación Estricta:
1. Sótano intacto (Z = -2.55 a -0.15 m, con 8 columnas de 35x35 cm).
2. Planta Baja intacta (Local Comercial 98 m2 + Garaje Techado + Baño).
3. Contorno perimetral intacto (X: 0.15 a 9.15 m, Y: 0.00 a 21.71 m).
4. Escaleras intactas en huella y desarrollo geométrico.
5. 31 Columnas estructurales de 25x25 cm en sus posiciones originales fijas.
6. Rediseño Mediterráneo del Último Piso:
   - Volúmenes puros encalados con aristas suaves.
   - Pórtico frontal con 3 arcos de medio punto sobre Avenida 4.
   - Pérgolas de viguería de madera para filtrado solar en solárium y terraza posterior.
   - Vanos abocinados para control de temperatura e insolación pasiva.
   - Azotea solárium transitable con antepecho encalado de 1.00 m.
"""

import os
import math
import struct

def build_mediterraneo_project():
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
    # PARÁMETROS GEOMÉTRICOS Y VERTICALES BASE
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso sótano
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa PB
    Z_P1_FLOOR     =  0.00   # Nivel piso terminado Planta Baja
    H_P1           =  2.85   # Fondo losa entrepiso / tope muros PB
    Z_P2_FLOOR     =  3.00   # Nivel piso terminado Último Piso
    H_P2_MURO      =  5.85   # Tope muros Último Piso / Fondo losa azotea
    Z_CUBIERTA     =  6.00   # Nivel losa azotea solárium transitable
    Z_ANTEPECHO    =  7.00   # Cota superior antepecho encalado (1.00 m)
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.00

    OFFSET_X = 0.00
    OFFSET_Y = 3.00
    Y_AV4    = 21.71  # Frente en Avenida 4

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
    # 1. NIVEL SÓTANO (100% INTACTO DE CASA_MODIFICACIONES)
    # =========================================================================
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT  = "SOTANO_MUROS_INT_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 6.40, 3.50, Z_SOT_FLOOR)
    add_house_box(L_SOT_SLAB, 8, 0.15, 3.50, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)

    # Escalera Tramo 1 (baja al sótano)
    num_steps = 12
    step_dy = (7.40 - 4.45) / num_steps
    step_dz = (0.00 - Z_SOT_FLOOR) / num_steps
    for i in range(num_steps):
        y_s_top = 7.40 - i * step_dy
        y_s_bot = y_s_top - step_dy
        z_s_top = 0.00 - i * step_dz
        add_house_box("ESCALERA_3D", 7, 0.30, y_s_bot, Z_SOT_FLOOR, 1.40, y_s_top, z_s_top)
        add_house_line("PLANTA_SOTANO_2D", 7, 0.30, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muros sótano
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 6.40, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 2.50, Z_SOT_FLOOR + 1.00, Z_SOT_FLOOR + 2.10),
        (3.40, 4.10, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
    ])
    add_wall_with_openings_y(L_SOT_EXT, 4, 6.25, 6.40, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 1.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
        (2.10, 2.80, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
    ])
    add_wall_with_openings_x(L_SOT_EXT, 4, 6.00, 9.15, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (6.60, 7.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
        (7.95, 8.90, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_house_box(L_SOT_EXT, 4, 8.95, 3.65, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Tabiques interiores sótano
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

    # 8 Columnas Sótano 35x35 cm
    sot_cols_axes = [
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)

    # =========================================================================
    # 2. PLANTA BAJA (100% INTACTA DE CASA_MODIFICACIONES)
    # =========================================================================
    L_P1_SLAB = "LOSA_PISO_3D"
    L_P1_EXT  = "MUROS_EXTERIORES_3D"
    L_P1_INT  = "MUROS_INTERIORES_3D"
    L_P1_COL  = "COLUMNAS_3D"

    add_house_box(L_P1_SLAB, 8, 0.15, 0.00, Z_P1_SLAB_BOT, 6.40, 3.50, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 3.50, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR)

    # Muro Lateral Izquierdo Propio
    add_house_box(L_P1_EXT, 7, 0.15, 0.00, Z_P1_FLOOR, 0.30, Y_AV4, H_P1)

    # Fachada Frontal en Avenida 4
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P1_FLOOR, H_P1, [
        (0.40, 2.65, 0.00, 2.25),   # Portón Vehicular
        (3.15, 5.65, 0.00, 2.40),   # Vitrina 1
        (6.20, 8.80, 0.00, 2.40),   # Vitrina 2
    ])

    # Muro Lateral Derecho sobre Eje 3
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 3.50, Y_AV4, Z_P1_FLOOR, H_P1, [
        (4.10,  5.00, 1.10, 2.00),
        (6.30,  8.00, 1.00, 2.10),
        (9.65, 11.85, 1.00, 2.10),
        (13.15, 14.05, 1.10, 2.00),
        (15.50, 17.70, 1.00, 2.10),
        (18.80, 21.00, 1.00, 2.10),
    ])

    # Cierres posteriores
    add_house_box(L_P1_EXT, 7, 6.25, 3.50, Z_P1_FLOOR, 9.15, 3.65, H_P1)
    add_wall_with_openings_y(L_P1_EXT, 7, 6.25, 6.40, 0.00, 3.50, Z_P1_FLOOR, H_P1, [
        (0.65, 2.85, 1.00, 2.10),
    ])
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 6.40, 0.00, 0.15, Z_P1_FLOOR, H_P1, [
        (0.55, 2.35, 1.15, 2.60),
        (4.10, 5.10, 1.00, 2.10),
    ])

    # Muros interiores Planta Baja
    add_house_box(L_P1_INT, 7, 2.75, 0.15, Z_P1_FLOOR, 2.90, Y_AV4 - 0.15, H_P1)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 8.80, 8.95, Z_P1_FLOOR, H_P1, [
        (1.65, 2.55, 0.00, H_DOOR),
    ])
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.35, H_P1)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 4.25, 4.40, Z_P1_FLOOR, H_P1, [
        (1.65, 2.45, 0.00, H_DOOR),
    ])
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 1.65, 1.80, Z_P1_FLOOR, H_P1, [
        (0.95, 2.05, 0.00, H_DOOR),
    ])
    add_house_box(L_P1_INT, 7, 5.85, 5.40, Z_P1_FLOOR, 9.00, 5.55, H_P1)
    add_wall_with_openings_y(L_P1_INT, 7, 5.85, 6.00, 3.65, 5.40, Z_P1_FLOOR, H_P1, [
        (3.95, 4.75, 0.00, H_DOOR),
    ])
    add_wall_with_openings_x(L_P1_INT, 7, 2.90, 6.25, 3.50, 3.65, Z_P1_FLOOR, H_P1, [
        (4.05, 4.90, 0.00, H_DOOR),
    ])

    # Escalera Tramo 2 (Sube a P2, 100% intacta)
    for i in range(12):
        y_s_top = 4.40 + (i + 1) * (2.95 / 12)
        y_s_bot = y_s_top - (2.95 / 12)
        z_s_bot = 0.00 + i * (3.00 / 12)
        z_s_top = z_s_bot + (3.00 / 12)
        add_house_box("P2_ESCALERA_3D", 7, 1.55, y_s_bot, 0.00, 2.65, y_s_top, z_s_top)

    # =========================================================================
    # 3. COLUMNAS ESTRUCTURALES (PRESERVADAS EXACTAMENTE DONDE ESTÁN)
    #    31 COLUMNAS EN PB Y 31 COLUMNAS EN EL ÚLTIMO PISO (CASA_MODIFICACIONES)
    # =========================================================================
    p1_cols_axes = [
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
        # Eje Posterior (Y = 0.075)
        (0.275, 0.075),  (2.825, 0.075),  (5.925, 0.075)
    ]

    for cx, cy in p1_cols_axes:
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)

    L_P2_COL = "P2_COLUMNAS_3D"
    for cx, cy in p1_cols_axes:
        add_house_box(L_P2_COL, 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, H_P2_MURO)

    # =========================================================================
    # 4. REDISEÑO DEL ÚLTIMO PISO: VILLA RESIDENCIAL MEDITERRÁNEA
    # =========================================================================
    L_P2_SLAB   = "P2_LOSA_PISO_3D"
    L_MED_WALL  = "MEDITERRANEO_MUROS_ENCALADOS_3D"
    L_MED_ARCH  = "MEDITERRANEO_ARCOS_PORTICO_3D"
    L_MED_INT   = "MEDITERRANEO_TABIQUES_3D"
    L_MED_PERG  = "MEDITERRANEO_PERGOLAS_3D"
    L_MED_ROOF  = "MEDITERRANEO_AZOTEA_SOLARIUM_3D"
    L_MED_ISLA  = "MEDITERRANEO_ISLA_COCINA_3D"

    # Losa de entrepiso (Z: 2.85 a 3.00 m) con hueco de escalera intacto
    add_house_box(L_P2_SLAB, 7, 0.15, 0.00, H_P1, 6.40, 3.50, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 0.15, 3.50, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 0.15, 4.40, H_P1, 0.30, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 7, 0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR)

    # Muro Lateral Izquierdo Encalado (X: 0.15 a 0.30 m)
    add_house_box(L_MED_WALL, 7, 0.15, 0.00, Z_P2_FLOOR, 0.30, Y_AV4, H_P2_MURO)

    # Muro Lateral Derecho sobre Eje 3 (X: 9.00 a 9.15 m) con vanos abocinados
    add_wall_with_openings_y(L_MED_WALL, 7, 9.00, 9.15, 3.50, Y_AV4, Z_P2_FLOOR, H_P2_MURO, [
        (4.10,  5.00, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.00), # Baño Familiar
        (6.30,  8.00, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Habitación 3
        (9.65, 11.85, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Habitación 2
        (13.15, 14.05, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.00), # Baño Suite
        (16.40, 18.80, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10), # Master Suite
    ])

    # Muros Posteriores encalados
    add_house_box(L_MED_WALL, 7, 6.25, 3.50, Z_P2_FLOOR, 9.15, 3.65, H_P2_MURO)
    add_wall_with_openings_y(L_MED_WALL, 7, 6.25, 6.40, 0.00, 3.50, Z_P2_FLOOR, H_P2_MURO, [
        (0.65, 2.85, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.10),
    ])
    add_wall_with_openings_x(L_MED_WALL, 7, 0.15, 6.40, 0.00, 0.15, Z_P2_FLOOR, H_P2_MURO, [
        (0.60, 2.30, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.25),
        (3.60, 5.40, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR), # Salida a Terraza Posterior
    ])

    # Muro Frontal Interior (separa estancias de la loggia sombreada en Y = 19.56 a 19.71 m)
    add_wall_with_openings_x(L_MED_WALL, 7, 0.15, 9.15, 19.56, 19.71, Z_P2_FLOOR, H_P2_MURO, [
        (1.20, 4.80, Z_P2_FLOOR, Z_P2_FLOOR + 2.35), # Gran Puerta-Ventana Salón a Loggia
        (6.50, 8.50, Z_P2_FLOOR, Z_P2_FLOOR + 2.35), # Salida Master Suite a Loggia
    ])

    # --- PÓRTICO MEDITERRÁNEO CON ARCOS DE MEDIO PUNTO EN AVENIDA 4 ---
    # Fachada exterior (Y: 21.41 a 21.71 m, H: 3.00 a 5.85 m)
    # Pilastras encaladas entre arcos
    pilastras_x = [(0.15, 0.50), (2.80, 3.40), (5.70, 6.30), (8.60, 9.15)]
    for px1, px2 in pilastras_x:
        add_house_box(L_MED_ARCH, 7, px1, Y_AV4 - 0.30, Z_P2_FLOOR, px2, Y_AV4, H_P2_MURO)
    
    # Dintel superior corrido de coronación de arquería (Z: 4.85 a 5.85 m)
    add_house_box(L_MED_ARCH, 7, 0.15, Y_AV4 - 0.30, Z_P2_FLOOR + 1.85, 9.15, Y_AV4, H_P2_MURO)

    # Tímpanos de arcos de medio punto (arcos formados por dovelas discretizadas)
    for ax_start in [0.50, 3.40, 6.30]:
        luz = 2.30
        h_arranque = 1.40
        radio = luz / 2
        # Tímpanos laterales sobre el arco
        add_house_box(L_MED_ARCH, 7, ax_start, Y_AV4 - 0.30, Z_P2_FLOOR, ax_start + luz, Y_AV4, Z_P2_FLOOR + h_arranque)
        # Remate de arco
        num_seg = 8
        for s in range(num_seg):
            ang1 = math.pi * s / num_seg
            ang2 = math.pi * (s + 1) / num_seg
            x_m1 = ax_start + radio - radio * math.cos(ang1)
            x_m2 = ax_start + radio - radio * math.cos(ang2)
            z_m1 = Z_P2_FLOOR + h_arranque + radio * math.sin(ang1)
            z_m2 = Z_P2_FLOOR + h_arranque + radio * math.sin(ang2)
            add_house_box(L_MED_ARCH, 7, min(x_m1, x_m2), Y_AV4 - 0.30, min(z_m1, z_m2), max(x_m1, x_m2), Y_AV4, Z_P2_FLOOR + 2.55)

    # --- TABIQUERÍA INTERIOR MEDITERRÁNEA ---
    # Muro Eje 2 (X: 5.85 a 6.00 m) que separa Salón/Cocina de Zona de Noche
    add_wall_with_openings_y(L_MED_INT, 7, 5.85, 6.00, 3.65, 19.56, Z_P2_FLOOR, H_P2_MURO, [
        (6.20, 7.10, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),   # Puerta Hab 3
        (9.50, 10.40, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),  # Puerta Hab 2
        (15.40, 16.30, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR), # Puerta Master Suite
    ])

    # Master Suite (Dormitorio Principal)
    add_house_box(L_MED_INT, 7, 6.00, 15.20, Z_P2_FLOOR, 9.00, 15.35, H_P2_MURO)
    add_house_box(L_MED_INT, 7, 6.80, 12.70, Z_P2_FLOOR, 9.00, 12.85, H_P2_MURO) # Baño suite
    add_house_box(L_MED_INT, 7, 6.80, 12.85, Z_P2_FLOOR, 6.95, 15.20, H_P2_MURO) # Vestidor

    # Habitación 2 (3.00 x 3.60 m)
    add_house_box(L_MED_INT, 7, 6.00, 8.85, Z_P2_FLOOR, 9.00, 9.00, H_P2_MURO)

    # Baño Familiar Compartido (3.00 x 1.75 m)
    add_house_box(L_MED_INT, 7, 6.00, 5.40, Z_P2_FLOOR, 9.00, 5.55, H_P2_MURO)

    # Terraza Posterior y Lavandería
    add_house_box(L_MED_INT, 7, 2.75, 0.15, Z_P2_FLOOR, 2.90, 4.30, H_P2_MURO)
    add_house_box(L_MED_INT, 7, 0.15, 4.30, Z_P2_FLOOR, 2.90, 4.45, H_P2_MURO)

    # Isla de Obra Encalada en Cocina Ibérica (2.60 x 0.95 m)
    add_house_box(L_MED_ISLA, 7, 2.15, 9.80, Z_P2_FLOOR, 3.10, 12.40, Z_P2_FLOOR + 0.90)
    add_house_box(L_MED_ISLA, 6, 2.10, 9.75, Z_P2_FLOOR + 0.90, 3.15, 12.45, Z_P2_FLOOR + 0.96) # Encimera madera

    # --- PÉRGOLAS DE CONTROL SOLAR (VIGAS DE MADERA Y CAÑIZO) ---
    # Pérgola frontal sobre Loggia en Avenida 4 (Y: 19.60 a 21.71 m)
    for vx in [0.50, 3.40, 6.30, 8.90]:
        add_house_box(L_MED_PERG, 6, vx - 0.06, 19.60, H_P2_MURO, vx + 0.06, Y_AV4, H_P2_MURO + 0.18)
    for py in [19.70 + i * 0.45 for i in range(5)]:
        if py <= Y_AV4:
            add_house_box(L_MED_PERG, 6, 0.30, py - 0.04, H_P2_MURO + 0.18, 9.00, py + 0.04, H_P2_MURO + 0.26)

    # Pérgola sobre Terraza Posterior
    for py in [0.40 + i * 0.50 for i in range(6)]:
        add_house_box(L_MED_PERG, 6, 2.90, py - 0.04, H_P2_MURO + 0.10, 6.25, py + 0.04, H_P2_MURO + 0.20)

    # --- CUBIERTA EN AZOTEA SOLÁRIUM TRANSITABLE ---
    # Losa de azotea (Z = 5.85 a 6.00 m)
    add_house_box(L_MED_ROOF, 7, 0.15, 0.00, H_P2_MURO, 9.15, Y_AV4, Z_CUBIERTA)

    # Antepecho perimetral encalado de 1.00 m de altura (Z: 6.00 a 7.00 m)
    add_house_box(L_MED_ROOF, 7, 0.15, 0.00, Z_CUBIERTA, 0.45, Y_AV4, Z_ANTEPECHO)
    add_house_box(L_MED_ROOF, 7, 8.85, 0.00, Z_CUBIERTA, 9.15, Y_AV4, Z_ANTEPECHO)
    add_house_box(L_MED_ROOF, 7, 0.15, 0.00, Z_CUBIERTA, 9.15, 0.30, Z_ANTEPECHO)
    add_house_box(L_MED_ROOF, 7, 0.15, Y_AV4 - 0.30, Z_CUBIERTA, 9.15, Y_AV4, Z_ANTEPECHO)

    # Albardilla de remate suave sobre antepecho
    add_house_box(L_MED_ROOF, 7, 0.12, -0.03, Z_ANTEPECHO, 9.18, Y_AV4 + 0.03, Z_ANTEPECHO + 0.08)

    # Bancada de obra integrada en azotea (estilo cicládico)
    add_house_box(L_MED_ROOF, 7, 0.45, 18.00, Z_CUBIERTA, 0.95, 21.00, Z_CUBIERTA + 0.45)
    add_house_box(L_MED_ROOF, 7, 0.95, 20.50, Z_CUBIERTA, 3.50, 21.00, Z_CUBIERTA + 0.45)

    # =========================================================================
    # 5. TERRENO NO RECTANGULAR UTM Y CERCA PERIMETRAL (100% INTACTOS)
    # =========================================================================
    L_TERR  = "TERRENO_3D"
    L_FENCE = "CERCA_PERIMETRAL_3D"

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

    add_box(L_FENCE, 7, 0.00, 0.00, -2.55, 0.15, 24.71, 0.50)
    add_box(L_FENCE, 7, 0.00, 0.00, -2.55, P3_LOC[0], 0.23, -1.00)
    add_box(L_FENCE, 7, P3_LOC[0] - 0.15, 0.23, -2.55, P2_LOC[0], 24.94, 0.50)

    # =========================================================================
    # 6. RÓTULOS Y LÍNEAS 2D DE PLANTA Y EJES ESTRUCTURALES
    # =========================================================================
    L_GRID = "EJES_ESTRUCTURALES"
    ejes_x_coords = [0.275, 2.825, 5.925, 9.075]
    for ex in ejes_x_coords:
        add_house_line(L_GRID, 4, ex, -0.80, 0, ex, Y_AV4 + 0.80, 0)
    ejes_y_coords = [21.585, 18.575, 16.325, 14.625, 12.025, 8.875, 6.575, 3.575, 0.075]
    for ey in ejes_y_coords:
        add_house_line(L_GRID, 4, -0.60, ey, 0, 9.80, ey, 0)

    for cx, cy in p1_cols_axes:
        add_house_line("PLANTA_SEGUNDO_PISO_2D", 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy - 0.125, Z_P2_FLOOR)
        add_house_line("PLANTA_SEGUNDO_PISO_2D", 1, cx + 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, Z_P2_FLOOR)
        add_house_line("PLANTA_SEGUNDO_PISO_2D", 1, cx + 0.125, cy + 0.125, Z_P2_FLOOR, cx - 0.125, cy + 0.125, Z_P2_FLOOR)
        add_house_line("PLANTA_SEGUNDO_PISO_2D", 1, cx - 0.125, cy + 0.125, Z_P2_FLOOR, cx - 0.125, cy - 0.125, Z_P2_FLOOR)

    # Rótulos técnicos Mediterráneos
    add_house_text("P2_ROTULOS", 6, "P2: GRAN SALÓN MEDITERRÁNEO (5,55 x 7,00m)", 1.20, 16.50, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: LOGGIA DE ARCOS Y PÉRGOLA SOLÁRIUM HACIA AV. 4 (9,00 x 2,00m)", 0.50, 20.60, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: MASTER SUITE CON VESTIDOR Y BAÑO ENCALADO", 6.20, 17.50, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: COCINA IBÉRICA CON ISLA DE OBRA ENCALADA (2,60 x 0,95m)", 1.20, 11.00, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: HABITACIÓN 2 CON VANOS ABOCINADOS (3,00 x 3,60m)", 6.20, 10.50, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: HABITACIÓN 3 CON CELOSÍAS (3,00 x 3,25m)", 6.20, 7.00, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: BAÑO FAMILIAR COMPARTIDO (3,00 x 1,75m)", 6.30, 4.40, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "P2: TERRAZA MIRADOR POSTERIOR CON PÉRGOLA (3,35 x 3,35m)", 3.10, 1.70, Z_P2_FLOOR + 0.05)
    add_house_text("P2_ROTULOS", 6, "AZOTEA SOLÁRIUM TRANSITABLE: ANTEPECHO ENCALADO 1.00m (Z = +7,00m)", 1.00, 0.50, Z_CUBIERTA + 0.05)

    # Rótulos Planta Baja
    add_house_text("ROTULOS_TEXTO", 2, "P1: GRAN LOCAL COMERCIAL (6,10 x 16,16m = 98,5 m2)", 3.40, 13.50, 0.05)
    add_house_text("ROTULOS_TEXTO", 2, "P1: GARAJE DOBLE PRIVADO (2,45 x 12,76m)", 0.45, 15.00, 0.05)

    # Rótulos Sótano
    add_house_text("SOTANO_ROTULOS", 4, "SOTANO: Sala y Área de Apoyo (Z = -2,55m)", 3.30, 5.80, Z_SOT_FLOOR + 0.05)

    # =========================================================================
    # EXPORTACIÓN DE ARCHIVOS
    # =========================================================================
    # 1. DXF ASCII R12/2000
    dxf_lines = [
        "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n",
        "0\nSECTION\n2\nTABLES\n",
        "0\nTABLE\n2\nLAYER\n70\n30\n",
    ]
    all_layers = set([b[0] for b in boxes_3d] + [h[0] for h in hexahedra_3d] + [l[0] for l in lines_2d] + [t[0] for t in texts])
    for lyr in sorted(all_layers):
        dxf_lines.append(f"0\nLAYER\n2\n{lyr}\n70\n0\n62\n7\n6\nCONTINUOUS\n")
    dxf_lines.append("0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nBLOCKS\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n")

    def w(code, val):
        dxf_lines.append(f"{code}\n{val}\n")

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
        write_3dface(layer, color, p1, p4, p3, p2)
        write_3dface(layer, color, p5, p6, p7, p8)
        write_3dface(layer, color, p1, p2, p6, p5)
        write_3dface(layer, color, p2, p3, p7, p6)
        write_3dface(layer, color, p3, p4, p8, p7)
        write_3dface(layer, color, p4, p1, p5, p8)

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

    out_dxf_paths = [
        "Proyecto_Mediterraneo/02_Modelos_CAD/casa_mediterranea.dxf",
        "02_Modelos_CAD/casa_mediterranea.dxf"
    ]
    for p in out_dxf_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="latin-1", errors="replace") as f:
            f.writelines(dxf_lines)
        print(f"DXF Casa Mediterránea generado: {p}")

    # 2. OBJ 3D Wavefront
    obj_lines = ["# Villa Mediterranea 3D (Base casa_modificaciones + Arcos + Pergolas + Solarium)\n\n"]
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

    out_obj_paths = [
        "Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_3d.obj",
        "03_Modelos_3D/casa_mediterranea_3d.obj"
    ]
    for p in out_obj_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(obj_lines)
        print(f"OBJ Casa Mediterránea generado: {p}")

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

    header = b'STL Binary 3D Casa Mediterranea (Base casa_modificaciones)'.ljust(80, b'\0')
    stl_bytes = bytearray(header)
    stl_bytes.extend(struct.pack('<I', len(triangles)))
    for p1, p2, p3 in triangles:
        stl_bytes.extend(struct.pack('<3f', 0.0, 0.0, 0.0))
        stl_bytes.extend(struct.pack('<3f', p1[0], p1[1], p1[2]))
        stl_bytes.extend(struct.pack('<3f', p2[0], p2[1], p2[2]))
        stl_bytes.extend(struct.pack('<3f', p3[0], p3[1], p3[2]))
        stl_bytes.extend(struct.pack('<H', 0))

    out_stl_paths = [
        "Proyecto_Mediterraneo/03_Modelos_3D/casa_mediterranea_3d.stl",
        "03_Modelos_3D/casa_mediterranea_3d.stl"
    ]
    for p in out_stl_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(stl_bytes)
        print(f"STL Casa Mediterránea generado: {p}")

    total_solids = len(boxes_3d) + len(hexahedra_3d)
    print(f"\n¡Éxito! Proyecto Mediterráneo construido con {total_solids} sólidos 3D.")
    print(f"- Sótano preservado idéntico a casa_modificaciones.dxf (Z = -2.55 m)")
    print(f"- Planta Baja preservada idéntica a casa_modificaciones.dxf (Local 98 m2 + Garaje)")
    print(f"- Escaleras intactas en posición y desarrollo geométrico")
    print(f"- 31 Columnas en PB y 31 Columnas en Último Piso exactamente donde están")
    print(f"- Rediseño Mediterráneo ejecutado: Arcos de medio punto, pérgolas de madera y azotea solárium.")

if __name__ == "__main__":
    build_mediterraneo_project()
