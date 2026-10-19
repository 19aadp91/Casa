"""
Generador del modelo arquitectonico integral (Primer Piso + Sotano)
Segun especificaciones de planos de casa.pdf
"""

import os

def build_complete_house():
    # Coordenadas y Dimensiones Globales
    W_X = 9.25
    L_Y = 15.15
    L_SOTANO_Y = 7.55
    
    # Alturas y Espesores
    H_WALL_P1 = 2.80       # Altura libre primer piso (Z: 0.00 a 2.80)
    H_WALL_SOT = 2.40      # Altura libre sotano (Z: -2.55 a -0.15)
    Z_SLAB_SOT = -2.70     # Losa de piso sotano (Z: -2.70 a -2.55)
    Z_SLAB_P1 = -0.15      # Losa entrepiso (Z: -0.15 a 0.00)
    Z_SLAB_ROOF = 2.80     # Losa de techo (Z: 2.80 a 2.95)
    H_PARAPET = 0.45       # Parapeto (Z: 2.95 a 3.40)
    
    T_EXT = 0.20
    T_INT = 0.15
    SLAB_T = 0.15
    
    H_DOOR = 2.10
    H_DOOR_SOT = 2.00
    
    boxes_3d = []  # (layer, color, x1, y1, z1, x2, y2, z2)
    lines_2d = []  # (layer, color, x1, y1, z1, x2, y2, z2)
    texts = []     # (layer, color, text, x, y, z, h)

    def add_box(layer, color, x1, y1, z1, x2, y2, z2):
        boxes_3d.append((layer, color, min(x1, x2), min(y1, y2), min(z1, z2),
                                       max(x1, x2), max(y1, y2), max(z1, z2)))

    def add_line(layer, color, x1, y1, z1, x2, y2, z2):
        lines_2d.append((layer, color, x1, y1, z1, x2, y2, z2))

    def add_text(layer, color, text, x, y, z, h=0.30):
        texts.append((layer, color, text, x, y, z, h))

    # =========================================================================
    # NIVEL SÓTANO (Z = -2.70 a -0.15)
    # =========================================================================
    # 1. Losa de piso del Sótano (Z = -2.70 a -2.55)
    LAYER_SOT_SLAB = "SOTANO_LOSA_3D"
    COLOR_SOT_SLAB = 8  # Gris
    add_box(LAYER_SOT_SLAB, COLOR_SOT_SLAB, 0.00, 0.00, Z_SLAB_SOT, W_X, L_SOTANO_Y, -2.55)

    # 2. Escalera completa del sótano (12 escalones desde Z=0.00 hasta Z=-2.55)
    # Ubicacion: X in [0.20, 1.45], Y in [4.45, 7.40]
    num_steps = 12
    step_l = (7.40 - 4.45) / num_steps
    step_h = 2.55 / num_steps
    for i in range(num_steps):
        y_top = 7.40 - i * step_l
        y_bot = y_top - step_l
        z_top = 0.00 - i * step_h
        z_bot = z_top - step_h
        add_box("ESCALERA_3D", 7, 0.20, y_bot, -2.55, 1.45, y_top, z_top)
        add_line("SOTANO_2D", 7, 0.20, y_bot, -2.55, 1.45, y_bot, -2.55)

    # 3. Muros Exteriores / Contención de Sótano (Espesor 0.20 m, Z: -2.55 a -0.15)
    LAYER_SOT_EXT = "SOTANO_MUROS_EXT_3D"
    COLOR_SOT_EXT = 4  # Cyan para diferenciar sótano
    
    z_sot_bot = -2.55
    z_sot_top = -0.15

    # Muro Oeste Sótano (Contención terreno)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 0.00, 0.00, z_sot_bot, 0.20, L_SOTANO_Y, z_sot_top)

    # Muro Norte Sótano (Muro frontal de contención hacia el frente de la casa)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 0.00, L_SOTANO_Y - 0.20, z_sot_bot, W_X, L_SOTANO_Y, z_sot_top)

    # Muro Este Sótano (Lateral derecho - Sala Sótano con puerta/ventana)
    # Puerta salida lateral Sala: Y in [5.50, 6.45], dintel
    x_se1, x_se2 = W_X - 0.20, W_X
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, x_se1, 0.00, z_sot_bot, x_se2, 5.50, z_sot_top)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, x_se1, 5.50, z_sot_bot + H_DOOR_SOT, x_se2, 6.45, z_sot_top)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, x_se1, 6.45, z_sot_bot, x_se2, L_SOTANO_Y - 0.20, z_sot_top)

    # Muro Sur Sótano (Fachada posterior sótano)
    # Puerta patio: X in [1.00, 2.00]
    # Ventana Habitación: X in [2.50, 4.40] (ancho 1.90 m)
    # Celosía Lavadero: X in [4.70, 5.40] (ancho 0.70 m)
    # Celosía Baño: X in [6.00, 6.75] (ancho 0.75 m)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 0.20, 0.00, z_sot_bot, 1.00, 0.20, z_sot_top)
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 1.00, 0.00, z_sot_bot + H_DOOR_SOT, 2.00, 0.20, z_sot_top) # Dintel P_Patio
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 2.00, 0.00, z_sot_bot, 2.50, 0.20, z_sot_top)
    # Ventana Habitación Sótano
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 2.50, 0.00, z_sot_bot, 4.40, 0.20, z_sot_bot + 1.00) # Sill
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 2.50, 0.00, z_sot_bot + 2.10, 4.40, 0.20, z_sot_top) # Dintel
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 4.40, 0.00, z_sot_bot, 4.70, 0.20, z_sot_top)
    # Celosía Lavadero Sótano
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 4.70, 0.00, z_sot_bot, 5.40, 0.20, z_sot_bot + 1.60) # Sill
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 4.70, 0.00, z_sot_bot + 2.00, 5.40, 0.20, z_sot_top) # Dintel
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 5.40, 0.00, z_sot_bot, 6.00, 0.20, z_sot_top)
    # Celosía Baño Sótano
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 6.00, 0.00, z_sot_bot, 6.75, 0.20, z_sot_bot + 1.60) # Sill
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 6.00, 0.00, z_sot_bot + 2.00, 6.75, 0.20, z_sot_top) # Dintel
    add_box(LAYER_SOT_EXT, COLOR_SOT_EXT, 6.75, 0.00, z_sot_bot, W_X - 0.20, 0.20, z_sot_top)

    # 4. Muros Interiores de Sótano (Espesor 0.15 m, Z: -2.55 a -0.15)
    LAYER_SOT_INT = "SOTANO_MUROS_INT_3D"
    COLOR_SOT_INT = 4

    # Muro Transversal Principal del Sótano (Y in [3.55, 3.70])
    # Separa Hab1/Lav/Baño de Cocina/Comedor/Sala
    # P_Hab1_Sot: X in [1.50, 2.30]
    # P_Lav_Sot: X in [4.00, 4.70]
    # P_Bano_Sot: X in [5.70, 6.40]
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 0.20, 3.55, z_sot_bot, 1.50, 3.70, z_sot_top)
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 1.50, 3.55, z_sot_bot + H_DOOR_SOT, 2.30, 3.70, z_sot_top) # Dintel
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 2.30, 3.55, z_sot_bot, 4.00, 3.70, z_sot_top)
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 4.00, 3.55, z_sot_bot + H_DOOR_SOT, 4.70, 3.70, z_sot_top) # Dintel
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 4.70, 3.55, z_sot_bot, 5.70, 3.70, z_sot_top)
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 5.70, 3.55, z_sot_bot + H_DOOR_SOT, 6.40, 3.70, z_sot_top) # Dintel
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 6.40, 3.55, z_sot_bot, W_X - 0.20, 3.70, z_sot_top)

    # Muro divisorio Habitación Sótano / Lavadero Sótano (X in [3.55, 3.70], Y in [0.20, 3.55])
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 3.55, 0.20, z_sot_bot, 3.70, 3.55, z_sot_top)

    # Muro divisorio Lavadero Sótano / Baño Sótano (X in [5.35, 5.50], Y in [0.20, 2.70])
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 5.35, 0.20, z_sot_bot, 5.50, 2.70, z_sot_top)

    # Muro divisorio Baño Sótano lateral derecho (X in [6.85, 7.00], Y in [0.20, 2.00])
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 6.85, 0.20, z_sot_bot, 7.00, 2.00, z_sot_top)

    # Muro Mocheta divisoria Cocina/Comedor - Sala Sótano (X in [6.10, 6.25], Y in [4.50, 7.35])
    # Paso libre de 1.80 m entre comedor y sala
    add_box(LAYER_SOT_INT, COLOR_SOT_INT, 6.10, 5.50, z_sot_bot, 6.25, 7.35, z_sot_top)

    # 5. Columnas Robustas de Sótano (35x35 cm, Z: -2.55 a -0.15)
    LAYER_SOT_COL = "SOTANO_COLUMNAS_3D"
    COLOR_SOT_COL = 1  # Rojo
    sot_cols = [
        # Eje F (Y = 7.20 aprox)
        (2.75, 7.20), (5.85, 7.20), (8.90, 7.20),
        # Eje G (Y = 4.10 aprox)
        (2.75, 4.10), (5.85, 4.10), (8.90, 4.10),
        # Eje Sur (Muro posterior)
        (0.00, 0.00), (2.75, 0.00), (5.85, 0.00), (8.90, 0.00)
    ]
    for cx, cy in sot_cols:
        add_box(LAYER_SOT_COL, COLOR_SOT_COL, cx, cy, z_sot_bot, cx + 0.35, cy + 0.35, z_sot_top)

    # Rotulos Sótano
    LAYER_SOT_TXT = "SOTANO_ROTULOS"
    COLOR_SOT_TXT = 2
    sot_rooms = [
        ("SOTANO - COCINA", 3.50, 5.80, z_sot_bot + 0.05),
        ("SOTANO - COMEDOR", 3.80, 4.40, z_sot_bot + 0.05),
        ("SOTANO - SALA", 7.50, 5.50, z_sot_bot + 0.05),
        ("SOTANO - HABITACION 1", 2.00, 1.80, z_sot_bot + 0.05),
        ("SOTANO - LAVADERO", 4.50, 1.40, z_sot_bot + 0.05),
        ("SOTANO - BANO", 6.20, 1.00, z_sot_bot + 0.05),
    ]
    for name, rx, ry, rz in sot_rooms:
        add_text(LAYER_SOT_TXT, COLOR_SOT_TXT, name, rx, ry, rz, 0.30)

    # =========================================================================
    # NIVEL PRIMER PISO (Z = 0.00 a 2.80) + LOSA ENTREPISO (Z = -0.15 a 0.00)
    # =========================================================================
    LAYER_P1_SLAB = "LOSA_PISO_3D"
    COLOR_P1_SLAB = 8

    # Losa entrepiso con hueco de escalera
    add_box(LAYER_P1_SLAB, COLOR_P1_SLAB, 0.00, 0.00, -SLAB_T, W_X, 4.45, 0.00)
    add_box(LAYER_P1_SLAB, COLOR_P1_SLAB, 0.00, 7.40, -SLAB_T, W_X, L_Y, 0.00)
    add_box(LAYER_P1_SLAB, COLOR_P1_SLAB, 1.45, 4.45, -SLAB_T, W_X, 7.40, 0.00)
    add_box(LAYER_P1_SLAB, COLOR_P1_SLAB, 0.00, 4.45, -SLAB_T, 0.20, 7.40, 0.00)

    # Muros P1
    LAYER_P1_EXT = "MUROS_EXTERIORES_3D"
    COLOR_P1_EXT = 7

    # Muro Oeste P1
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 0.00, 0.00, 0.00, 0.20, L_Y, H_WALL_P1)

    # Muro Sur P1
    W_SILL = 1.00
    W_H = 1.10
    B_SILL = 1.80
    B_H = 0.40
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 0.20, 0.00, 0.00, 0.80, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 0.80, 0.00, H_DOOR, 1.80, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 1.80, 0.00, 0.00, 3.70, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 3.70, 0.00, 0.00, 5.60, 0.20, W_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 3.70, 0.00, W_SILL + W_H, 5.60, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 5.60, 0.00, 0.00, 7.00, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 7.00, 0.00, 0.00, 7.90, 0.20, B_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 7.00, 0.00, B_SILL + B_H, 7.90, 0.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 7.90, 0.00, 0.00, 9.05, 0.20, H_WALL_P1)

    # Muro Este P1
    x_e1, x_e2 = 9.05, 9.25
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 0.00, 0.00, x_e2, 0.50, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 0.50, 0.00, x_e2, 1.40, B_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 0.50, B_SILL + B_H, x_e2, 1.40, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 1.40, 0.00, x_e2, 2.60, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 2.60, 0.00, x_e2, 4.80, W_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 2.60, W_SILL + W_H, x_e2, 4.80, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 4.80, 0.00, x_e2, 6.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 6.20, 0.00, x_e2, 8.40, W_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 6.20, W_SILL + W_H, x_e2, 8.40, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 8.40, 0.00, x_e2, 9.70, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 9.70, 0.00, x_e2, 10.60, B_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 9.70, B_SILL + B_H, x_e2, 10.60, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 10.60, 0.00, x_e2, 12.00, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 12.00, 0.00, x_e2, 14.20, W_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 12.00, W_SILL + W_H, x_e2, 14.20, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, x_e1, 14.20, 0.00, x_e2, L_Y, H_WALL_P1)

    # Muro Norte P1
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 0.20, 14.95, 2.50, 2.80, L_Y, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 2.80, 14.95, 2.40, 5.90, L_Y, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 5.90, 14.95, 0.00, 6.50, L_Y, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 6.50, 14.95, 0.00, 8.70, L_Y, W_SILL)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 6.50, 14.95, W_SILL + W_H, 8.70, L_Y, H_WALL_P1)
    add_box(LAYER_P1_EXT, COLOR_P1_EXT, 8.70, 14.95, 0.00, 9.05, L_Y, H_WALL_P1)

    # Muros Interiores P1
    LAYER_P1_INT = "MUROS_INTERIORES_3D"
    COLOR_P1_INT = 7

    # Eje 1
    x1_1, x2_1 = 2.80, 2.95
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 0.20, 0.00, x2_1, 3.20, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 3.20, H_DOOR, x2_1, 4.00, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 4.00, 0.00, x2_1, 4.45, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 7.40, 0.00, x2_1, 9.50, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 9.50, H_DOOR, x2_1, 10.40, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_1, 10.40, 0.00, x2_1, 12.90, H_WALL_P1)

    # Eje 2
    x1_2, x2_2 = 5.90, 6.05
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 0.20, 0.00, x2_2, 1.00, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 1.00, H_DOOR, x2_2, 1.70, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 1.70, 0.00, x2_2, 4.30, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 4.30, H_DOOR, x2_2, 5.00, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 5.00, 0.00, x2_2, 8.10, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 8.10, H_DOOR, x2_2, 8.80, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 8.80, 0.00, x2_2, 9.80, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 9.80, H_DOOR, x2_2, 10.50, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 10.50, 0.00, x2_2, 11.50, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 11.50, H_DOOR, x2_2, 12.20, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, x1_2, 12.20, 0.00, x2_2, 14.95, H_WALL_P1)

    # Transversales P1
    add_box(LAYER_P1_INT, COLOR_P1_INT, 0.20, 1.70, 0.00, 0.50, 1.85, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 0.50, 1.70, H_DOOR, 1.30, 1.85, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 1.30, 1.70, 0.00, 2.80, 1.85, H_WALL_P1)

    add_box(LAYER_P1_INT, COLOR_P1_INT, 0.20, 4.30, 0.00, 2.80, 4.45, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 0.20, 7.40, 0.00, 2.80, 7.55, H_WALL_P1)

    add_box(LAYER_P1_INT, COLOR_P1_INT, 2.95, 3.55, 0.00, 3.50, 3.70, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 3.50, 3.55, H_DOOR, 4.20, 3.70, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 4.20, 3.55, 0.00, 5.90, 3.70, H_WALL_P1)

    add_box(LAYER_P1_INT, COLOR_P1_INT, 6.05, 1.95, 0.00, 9.05, 2.10, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 6.05, 5.35, 0.00, 9.05, 5.50, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 6.05, 9.10, 0.00, 9.05, 9.25, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 6.05, 11.10, 0.00, 9.05, 11.25, H_WALL_P1)

    add_box(LAYER_P1_INT, COLOR_P1_INT, 2.95, 12.90, 0.00, 3.20, 13.05, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 3.20, 12.90, H_DOOR, 4.15, 13.05, H_WALL_P1)
    add_box(LAYER_P1_INT, COLOR_P1_INT, 4.15, 12.90, 0.00, 5.90, 13.05, H_WALL_P1)

    # Columnas P1 (25x25 cm)
    LAYER_P1_COL = "COLUMNAS_3D"
    COLOR_P1_COL = 1
    p1_cols = [
        (2.80, 14.90), (2.80, 12.90), (2.80, 10.40), (2.80, 7.40), (2.80, 4.30), (2.80, 0.20),
        (5.90, 14.90), (5.90, 12.90), (5.90, 9.10), (5.90, 5.35), (5.90, 3.55), (5.90, 0.20),
        (9.00, 14.90), (9.00, 11.10), (9.00, 9.10), (9.00, 5.35), (9.00, 1.95), (9.00, 0.20),
        (0.00, 14.90), (0.00, 7.40), (0.00, 0.20)
    ]
    for cx, cy in p1_cols:
        add_box(LAYER_P1_COL, COLOR_P1_COL, cx, cy, 0.00, cx + 0.25, cy + 0.25, H_WALL_P1)

    # Cubierta P1
    LAYER_ROOF = "CUBIERTA_3D"
    COLOR_ROOF = 9
    add_box(LAYER_ROOF, COLOR_ROOF, 0.00, 0.00, H_WALL_P1, W_X, L_Y, H_WALL_P1 + SLAB_T)
    z_p1 = H_WALL_P1 + SLAB_T
    z_p2 = z_p1 + H_PARAPET
    add_box(LAYER_ROOF, COLOR_ROOF, 0.00, 0.00, z_p1, 0.20, L_Y, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, W_X - 0.20, 0.00, z_p1, W_X, L_Y, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, 0.20, 0.00, z_p1, W_X - 0.20, 0.20, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, 0.20, L_Y - 0.20, z_p1, W_X - 0.20, L_Y, z_p2)

    # Rotulos P1
    LAYER_P1_TXT = "ROTULOS_TEXTO"
    COLOR_P1_TXT = 2
    p1_rooms = [
        ("PORCHE", 4.35, 14.00, 0.05),
        ("GARAJE", 1.50, 11.20, 0.05),
        ("SALA", 4.40, 11.00, 0.05),
        ("COMEDOR", 4.40, 7.20, 0.05),
        ("COCINA", 1.50, 3.10, 0.05),
        ("LAVADERO", 1.50, 0.90, 0.05),
        ("HABITACION 1", 7.55, 13.10, 0.05),
        ("BANO 1", 7.55, 10.15, 0.05),
        ("HABITACION 2", 7.55, 7.30, 0.05),
        ("HABITACION 3", 7.55, 3.70, 0.05),
        ("BANO 2", 7.55, 1.05, 0.05),
        ("HABITACION 4", 4.40, 1.85, 0.05),
    ]
    for name, rx, ry, rz in p1_rooms:
        add_text(LAYER_P1_TXT, COLOR_P1_TXT, name, rx, ry, rz, 0.35)

    # Lineas 2D
    add_line("DISTRIBUCION_2D", 3, 0.0, 0.0, 0.0, W_X, 0.0, 0.0)
    add_line("DISTRIBUCION_2D", 3, W_X, 0.0, 0.0, W_X, L_Y, 0.0)
    add_line("DISTRIBUCION_2D", 3, W_X, L_Y, 0.0, 0.0, L_Y, 0.0)
    add_line("DISTRIBUCION_2D", 3, 0.0, L_Y, 0.0, 0.0, 0.0, 0.0)

    # =========================================================================
    # GENERAR ARCHIVO DXF COMPLETO
    # =========================================================================
    dxf_lines = []
    def w(code, val):
        dxf_lines.append(f"{code:>3}\n{val}\n")

    w(0, "SECTION")
    w(2, "HEADER")
    w(9, "$ACADVER")
    w(1, "AC1009")
    w(9, "$INSUNITS")
    w(70, 6)
    w(9, "$EXTMIN")
    w(10, -2.0)
    w(20, -2.0)
    w(30, -3.5)
    w(9, "$EXTMAX")
    w(10, W_X + 2.0)
    w(20, L_Y + 2.0)
    w(30, H_WALL_P1 + 1.0)
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "TABLES")
    w(0, "TABLE")
    w(2, "LAYER")
    w(70, 14)

    all_layers = [
        (LAYER_SOT_SLAB, COLOR_SOT_SLAB),
        (LAYER_SOT_EXT, COLOR_SOT_EXT),
        (LAYER_SOT_INT, COLOR_SOT_INT),
        (LAYER_SOT_COL, COLOR_SOT_COL),
        (LAYER_SOT_TXT, COLOR_SOT_TXT),
        ("SOTANO_2D", 4),
        (LAYER_P1_SLAB, COLOR_P1_SLAB),
        (LAYER_P1_EXT, COLOR_P1_EXT),
        (LAYER_P1_INT, COLOR_P1_INT),
        (LAYER_P1_COL, COLOR_P1_COL),
        (LAYER_ROOF, COLOR_ROOF),
        ("ESCALERA_3D", 7),
        ("DISTRIBUCION_2D", 3),
        (LAYER_P1_TXT, COLOR_P1_TXT),
    ]
    for lname, lcol in all_layers:
        w(0, "LAYER")
        w(2, lname)
        w(70, 0)
        w(62, lcol)
        w(6, "CONTINUOUS")

    w(0, "ENDTAB")
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "BLOCKS")
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "ENTITIES")

    def write_3dface(layer, color, p1, p2, p3, p4):
        w(0, "3DFACE")
        w(8, layer)
        w(62, color)
        w(10, f"{p1[0]:.4f}")
        w(20, f"{p1[1]:.4f}")
        w(30, f"{p1[2]:.4f}")
        w(11, f"{p2[0]:.4f}")
        w(21, f"{p2[1]:.4f}")
        w(31, f"{p2[2]:.4f}")
        w(12, f"{p3[0]:.4f}")
        w(22, f"{p3[1]:.4f}")
        w(32, f"{p3[2]:.4f}")
        w(13, f"{p4[0]:.4f}")
        w(23, f"{p4[1]:.4f}")
        w(33, f"{p4[2]:.4f}")

    for box in boxes_3d:
        layer, color, x1, y1, z1, x2, y2, z2 = box
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1))
        write_3dface(layer, color, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2))
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2))
        write_3dface(layer, color, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2))
        write_3dface(layer, color, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2))
        write_3dface(layer, color, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2))

    for line in lines_2d:
        layer, color, x1, y1, z1, x2, y2, z2 = line
        w(0, "LINE")
        w(8, layer)
        w(62, color)
        w(10, f"{x1:.4f}")
        w(20, f"{y1:.4f}")
        w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}")
        w(21, f"{y2:.4f}")
        w(32, f"{z2:.4f}")

    for item in texts:
        layer, color, txt, x, y, z, h = item
        w(0, "TEXT")
        w(8, layer)
        w(62, color)
        w(10, f"{x:.4f}")
        w(20, f"{y:.4f}")
        w(30, f"{z:.4f}")
        w(40, f"{h:.4f}")
        w(1, txt)

    w(0, "ENDSEC")
    w(0, "EOF")

    # Guardar en las rutas
    for path in ["casa.dxf", "02_Modelos_CAD/casa.dxf"]:
        with open(path, "w", encoding="ascii") as f:
            f.writelines(dxf_lines)
    print(f"DXF integral generado con {len(boxes_3d)} solidos 3D ({len(boxes_3d)*6} caras 3DFACE).")

    # =========================================================================
    # GENERAR OBJ COMPLETO
    # =========================================================================
    obj_lines = ["# Casa Completa: Primer Piso + Sotano\n\n"]
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

    for p in ["03_Modelos_3D/casa_3d.obj"]:
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(obj_lines)
    print("OBJ integral generado en 03_Modelos_3D/casa_3d.obj.")

if __name__ == "__main__":
    build_complete_house()
