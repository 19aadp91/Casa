"""
Generador Maestro del Proyecto Arquitectónico Modificado ("casa_modificaciones.dxf"):
1. Muro Propio Izquierdo (X: 0.15 a 0.30 m) + Eje 0 de Columnas Propias (separado de la pared del vecino en X: 0.00 a 0.15 m)
2. Extensión del Frente hasta el Lindero de la Avenida 4 (Y_casa = 21.71 m / Y_terreno = 24.71 m, Eje A0)
3. Planta Primer Piso (Z = 0.00 a +3.00 m):
   - Gran Local Comercial (~98 m², 6.10 x 16.16 m) hasta la Avenida 4 (sin Hab. 1, 2, 3 ni Baño 1) + Baño y Depósito
   - Garaje Doble Techado (2.45 x 12.76 m) con acceso privado directo a la Escalera (Sótano y 2do Piso)
4. Planta Segundo Piso (Z = +3.00 a +6.00 m): Apartamento de 3 Habitaciones:
   - Sala-Comedor amplia hacia la Avenida 4 + Cocina abierta después de la Sala-Comedor con Isla Central
   - Habitación Principal con Balcón Privado hacia la Avenida 4, Vestier/Closet y Baño Privado En-Suite
   - Habitaciones Secundarias 2 y 3 con Baño Compartido, Lavandería y Estudio/Terraza posterior ventilada
5. Planta Sótano + Terreno Poligonal UTM No Rectangular (P-1..P-4) con los 5 Escalones y Rampa de Fachada Lateral
"""

import math

def build_full_project():
    boxes_3d = []      # (layer, color, x1, y1, z1, x2, y2, z2)
    hexahedra_3d = []  # (layer, color, [p0..p7]) para solidos trapezoidales y con pendiente
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

    def add_rect_2d(layer, color, x1, y1, x2, y2, z=0.0):
        add_line(layer, color, x1, y1, z, x2, y1, z)
        add_line(layer, color, x2, y1, z, x2, y2, z)
        add_line(layer, color, x2, y2, z, x1, y2, z)
        add_line(layer, color, x1, y2, z, x1, y1, z)

    def add_text(layer, color, text, x, y, z, h=0.25):
        texts.append((layer, color, text, x, y, z, h))

    # =========================================================================
    # PARÁMETROS VERTICALES (EJE Z) — SÓTANO + PRIMER PISO + SEGUNDO PISO
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso acabado Sótano (Altura libre = 2.40 m)
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa entrepiso Primer Piso
    Z_P1_FLOOR     =  0.00   # Nivel piso acabado Primer Piso (Local Comercial + Garaje)
    H_P1           =  2.85   # Tope muros Primer Piso / Fondo losa Segundo Piso
    Z_P2_FLOOR     =  3.00   # Nivel piso acabado Segundo Piso (Apartamento 3 Habitaciones)
    H_P2           =  5.85   # Tope muros Segundo Piso / Fondo losa Cubierta
    Z_ROOF_TOP     =  6.00   # Nivel superior cubierta Segundo Piso
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.00

    # Implantación dentro de la parcela poligonal UTM (24.71 m de largo)
    OFFSET_X = 0.00   # X = 0.00..0.15 es la pared del vecino; X = 0.15..0.30 es la pared propia izquierda
    OFFSET_Y = 3.00   # Retiro de fondo hacia Solar de Miguel Rodríguez
    Y_AV4    = 21.71  # Frente extendido hasta el lindero de la Avenida 4 (Y_terreno = 24.71 m)

    def add_house_box(layer, color, x1, y1, z1, x2, y2, z2):
        add_box(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_line(layer, color, x1, y1, z1, x2, y2, z2):
        add_line(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_text(layer, color, text, x, y, z, h=0.22):
        add_text(layer, color, text, OFFSET_X + x, OFFSET_Y + y, z, h)

    def add_wall_with_openings_x(layer, color, x1, x2, y1, y2, z_bot, z_top, openings):
        openings = sorted(openings, key=lambda o: o[0])
        curr_x = x1
        for ox1, ox2, oz1, oz2 in openings:
            if ox1 > curr_x:
                add_house_box(layer, color, curr_x, y1, z_bot, ox1, y2, z_top)
            if oz1 > z_bot:
                add_house_box(layer, color, ox1, y1, z_bot, ox2, y2, oz1)  # Antepecho
            if oz2 < z_top:
                add_house_box(layer, color, ox1, y1, oz2, ox2, y2, z_top)  # Dintel
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
                add_house_box(layer, color, x1, oy1, z_bot, x2, oy2, oz1)  # Antepecho
            if oz2 < z_top:
                add_house_box(layer, color, x1, oy1, oz2, x2, oy2, z_top)  # Dintel
            curr_y = oy2
        if curr_y < y2:
            add_house_box(layer, color, x1, curr_y, z_bot, x2, y2, z_top)

    # =========================================================================
    # 1. NIVEL SÓTANO (Z = -2.55 a -0.15 m)
    # =========================================================================
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT  = "SOTANO_MUROS_INT_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 6.40, 3.50, Z_SOT_FLOOR)
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
        add_house_line("ESCALERA_2D", 7, 0.30, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muro Oeste Propio en Sótano (X: 0.15 a 0.30, Y: 0.00 a 8.30) adosado a la pared del vecino
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur Sótano Posterior (Y: 0.00 a 0.15, X: 0.30 a 6.40)
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 6.40, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 2.50, Z_SOT_FLOOR + 1.00, Z_SOT_FLOOR + 2.10),  # Ventana 1.90 x 1.10
        (3.40, 4.10, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Celosía 0.70 x 0.40
    ])

    # Muro Este del bloque posterior del Sótano (X: 6.25 a 6.40, Y: 0.15 a 3.50) con 2 celosías
    add_wall_with_openings_y(L_SOT_EXT, 4, 6.25, 6.40, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 1.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
        (2.10, 2.80, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
    ])

    # Muro Sur de Sala Sótano sobre Eje G (Y: 3.50 a 3.65, X: 6.00 a 9.15)
    add_wall_with_openings_x(L_SOT_EXT, 4, 6.00, 9.15, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (6.60, 7.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
        (7.95, 8.90, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])

    # Muro Este de Sala Sótano sobre Eje 3 (X: 8.95 a 9.15, Y: 3.65 a 8.30)
    add_house_box(L_SOT_EXT, 4, 8.95, 3.65, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Muro Norte de Contención del Sótano (Y: 8.15 a 8.30, X: 0.30 a 9.15)
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Tabiquería Interna del Sótano:
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

    # Columnas Sótano 35x35 cm en Ejes (0, 1, 2, 3) x (F, G)
    sot_cols_axes = [
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)


    # =========================================================================
    # 2. NIVEL PRIMER PISO (Z = 0.00 a +2.85 m):
    #    GRAN LOCAL COMERCIAL HASTA AVENIDA 4 + GARAJE DOBLE CON MURO PROPIO
    # =========================================================================
    L_P1_SLAB = "LOSA_PISO_3D"
    L_P1_EXT  = "MUROS_EXTERIORES_3D"
    L_P1_INT  = "MUROS_INTERIORES_3D"
    L_P1_COL  = "COLUMNAS_3D"

    # Losa de Piso Primer Piso extendida hasta la Avenida 4 (Y = 21.71 m)
    add_house_box(L_P1_SLAB, 8, 0.15, 0.00, Z_P1_SLAB_BOT, 6.40, 3.50, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 3.50, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR)

    # --- MUROS EXTERIORES PRIMER PISO ---
    # 1. Muro Lateral Izquierdo PROPIO (X: 0.15 a 0.30, Y: 0.00 a 21.71 m — separado de la pared del vecino en X: 0.00..0.15)
    add_house_box(L_P1_EXT, 7, 0.15, 0.00, Z_P1_FLOOR, 0.30, Y_AV4, H_P1)

    # 2. Fachada Frontal sobre la Avenida 4 (Eje A0, Y: 21.56 a 21.71, X: 0.15 a 9.15):
    #    - Portón del Garaje Doble (X: 0.40 a 2.65)
    #    - Vitrina y Entrada Comercial Izquierda (X: 3.15 a 5.65)
    #    - Vitrina y Entrada Comercial Derecha (X: 6.20 a 8.80)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P1_FLOOR, H_P1, [
        (0.40, 2.65, 0.00, 2.25),   # Portón Vehicular en Avenida 4 (2.25 m ancho)
        (3.15, 5.65, 0.00, 2.40),   # Vitrina / Acceso Comercial 1 (2.50 m ancho)
        (6.20, 8.80, 0.00, 2.40),   # Vitrina / Acceso Comercial 2 (2.60 m ancho)
    ])

    # 3. Muro Lateral Derecho sobre Eje 3 extendido hasta Avenida 4 (X: 9.00 a 9.15, Y: 3.50 a 21.71 — 18.21 m)
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 3.50, Y_AV4, Z_P1_FLOOR, H_P1, [
        (4.10,  5.00, 1.10, 2.00),  # Ventana Baño del Local (0.90 x 0.90)
        (6.30,  8.00, 1.00, 2.10),  # Ventanal Local tramo sur (1.70 x 1.10)
        (9.65, 11.85, 1.00, 2.10),  # Ventanal Local tramo central (2.20 x 1.10)
        (13.15, 14.05, 1.10, 2.00), # Ventana alta Local (0.90 x 0.90)
        (15.50, 17.70, 1.00, 2.10), # Ventanal Local tramo norte (2.20 x 1.10)
        (18.80, 21.00, 1.00, 2.10), # Nuevo Ventanal Local en ampliación hacia Av. 4 (2.20 x 1.10)
    ])

    # 4. Muro Sur del Baño del Local sobre Eje G (Y: 3.50 a 3.65, X: 6.25 a 9.15)
    add_house_box(L_P1_EXT, 7, 6.25, 3.50, Z_P1_FLOOR, 9.15, 3.65, H_P1)

    # 5. Muro Este de Depósito/Oficina del Local (X: 6.25 a 6.40, Y: 0.00 a 3.50) con ventana de 2.20 x 1.10 m
    add_wall_with_openings_y(L_P1_EXT, 7, 6.25, 6.40, 0.00, 3.50, Z_P1_FLOOR, H_P1, [
        (0.65, 2.85, 1.00, 2.10),
    ])

    # 6. Muro Sur Posterior de Servicio y Depósito (Y: 0.00 a 0.15, X: 0.15 a 6.40)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 6.40, 0.00, 0.15, Z_P1_FLOOR, H_P1, [
        (0.55, 2.35, 1.15, 2.60),
        (4.10, 5.10, 1.00, 2.10),
    ])

    # --- MUROS INTERIORES PRIMER PISO (LOCAL COMERCIAL + GARAJE PRIVADO) ---
    # (Se eliminaron Habitación 1, Baño 1, Habitación 2, Habitación 3 y tabiques de Sala/Comedor)

    # 1. Muro divisorio completo en Eje 1 que separa el Garaje/Escalera privada del Local Comercial (X: 2.75 a 2.90, Y: 0.15 a 21.56)
    add_house_box(L_P1_INT, 7, 2.75, 0.15, Z_P1_FLOOR, 2.90, Y_AV4 - 0.15, H_P1)

    # 2. Muro posterior del Garaje sobre Eje E (Y: 8.80 a 8.95, X: 0.30 a 2.75) con puerta privada hacia la Escalera
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 8.80, 8.95, Z_P1_FLOOR, H_P1, [
        (1.65, 2.55, 0.00, H_DOOR), # Puerta privada de 0.90 m del Garaje a la Escalera del 2do Piso y Sótano
    ])

    # 3. Muro central del núcleo de escalera de doble tramo (X: 1.40 a 1.55, Y: 4.40 a 7.35)
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.35, H_P1)

    # 4. Muros del área posterior izquierda de apoyo (Y: 4.25 a 4.40 con puerta, y Y: 1.65 a 1.80)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 4.25, 4.40, Z_P1_FLOOR, H_P1, [
        (1.65, 2.45, 0.00, H_DOOR),
    ])
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 1.65, 1.80, Z_P1_FLOOR, H_P1, [
        (0.95, 2.05, 0.00, H_DOOR),
    ])

    # 5. Cierre del Baño del Local Comercial (X: 5.85 a 9.00, Y: 3.65 a 5.55)
    add_house_box(L_P1_INT, 7, 5.85, 5.40, Z_P1_FLOOR, 9.00, 5.55, H_P1)
    add_wall_with_openings_y(L_P1_INT, 7, 5.85, 6.00, 3.65, 5.40, Z_P1_FLOOR, H_P1, [
        (3.95, 4.75, 0.00, H_DOOR), # Puerta de 0.80 m al Baño del Local
    ])

    # 6. Muro norte de Depósito/Oficina del Local sobre Eje G (Y: 3.50 a 3.65, X: 2.90 a 6.25) con puerta de 0.85 m
    add_wall_with_openings_x(L_P1_INT, 7, 2.90, 6.25, 3.50, 3.65, Z_P1_FLOOR, H_P1, [
        (4.05, 4.90, 0.00, H_DOOR),
    ])

    # --- COLUMNAS PRIMER PISO (25x25 cm) INCLUYENDO NUEVO EJE 0 IZQUIERDO Y NUEVO EJE A0 EN AVENIDA 4 ---
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
        (0.275, 8.875), (2.825, 8.875), (5.925, 8.875), (9.075, 8.875),
        # Eje F (Y = 6.575)
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        # Eje G (Y = 3.575)
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in p1_cols_axes:
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)


    # =========================================================================
    # 3. NIVEL SEGUNDO PISO (Z = +3.00 a +6.00 m):
    #    APARTAMENTO DE 3 HABITACIONES (PRINCIPAL CON BAÑO Y BALCÓN + 2 SECUNDARIAS
    #    CON BAÑO COMPARTIDO + SALA-COMEDOR A AVENIDA 4 + COCINA CON ISLA CENTRAL)
    # =========================================================================
    L_P2_SLAB = "P2_LOSA_PISO_3D"
    L_P2_EXT  = "P2_MUROS_EXT_3D"
    L_P2_INT  = "P2_MUROS_INT_3D"
    L_P2_COL  = "P2_COLUMNAS_3D"
    L_P2_ISL  = "P2_COCINA_ISLA_3D"
    L_P2_ROOF = "P2_CUBIERTA_3D"

    # Losa de Entrepiso del Segundo Piso (Z: 2.85 a 3.00 m) respetando el hueco de escalera (X: 0.30..2.65, Y: 4.40..7.35)
    add_house_box(L_P2_SLAB, 8, 0.15, 0.00, H_P1, 6.40, 3.50, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 3.50, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 4.40, H_P1, 0.30, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR)

    # Escalera Tramo 2: Sube del Primer Piso (Z = 0.00 en Y = 7.35) al Segundo Piso (Z = +3.00 en Y = 4.40), X: 1.55 a 2.65
    num_steps_p2 = 14
    step_dy_p2 = (7.35 - 4.40) / num_steps_p2
    step_dz_p2 = (Z_P2_FLOOR - Z_P1_FLOOR) / num_steps_p2
    for i in range(num_steps_p2):
        y_s_bot = 7.35 - (i + 1) * step_dy_p2
        y_s_top = 7.35 - i * step_dy_p2
        z_s_bot = Z_P1_FLOOR + i * step_dz_p2
        z_s_top = z_s_bot + step_dz_p2
        add_house_box("P2_ESCALERA_3D", 7, 1.55, y_s_bot, z_s_bot - 0.15, 2.65, y_s_top, z_s_top)

    # --- MUROS EXTERIORES SEGUNDO PISO ---
    # 1. Muro Lateral Izquierdo PROPIO (X: 0.15 a 0.30, Y: 0.00 a 21.71 m)
    add_house_box(L_P2_EXT, 6, 0.15, 0.00, Z_P2_FLOOR, 0.30, Y_AV4, H_P2)

    # 2. Fachada Frontal sobre Avenida 4 (Y: 21.56 a 21.71 m, X: 0.15 a 9.15 m):
    #    - Izquierda/Centro (X: 0.30 a 5.85): Gran Sala-Comedor con 2 ventanales panorámicos hacia la Avenida 4
    #    - Derecha (X: 6.00 a 9.00): Balcón Privado de la Habitación Principal con baranda de 1.05 m y vano abierto superior
    add_wall_with_openings_x(L_P2_EXT, 6, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P2_FLOOR, H_P2, [
        (0.65, 2.60, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25),  # Ventanal Panorámico Sala (1.95 x 1.40 m)
        (3.15, 5.50, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25),  # Ventanal Panorámico Comedor (2.35 x 1.40 m)
        (6.05, 8.95, Z_P2_FLOOR + 1.05, Z_P2_FLOOR + 2.55),  # Abertura frontal del Balcón Principal (antepecho de 1.05 m)
    ])

    # 3. Muro interior del Balcón de la Habitación Principal (Y: 19.95 a 20.10, X: 6.00 a 9.00)
    #    Deja un Balcón Privado de 3.00 x 1.60 m hacia la Avenida 4 con puerta-ventana corrediza de 2.00 m
    add_wall_with_openings_x(L_P2_EXT, 6, 6.00, 9.00, 19.95, 20.10, Z_P2_FLOOR, H_P2, [
        (6.50, 8.50, Z_P2_FLOOR, Z_P2_FLOOR + 2.20),         # Puerta-ventana corrediza al Balcón Principal
    ])

    # 4. Muro Lateral Derecho sobre Eje 3 (X: 9.00 a 9.15, Y: 3.50 a 21.71 m) con ventanas de las 3 habitaciones, 2 baños y balcón
    add_wall_with_openings_y(L_P2_EXT, 6, 9.00, 9.15, 3.50, Y_AV4, Z_P2_FLOOR, H_P2, [
        (4.10,  5.00, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.00), # Ventana Baño Compartido (0.90 x 0.90)
        (6.30,  8.00, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15), # Ventana Habitación 3 (1.70 x 1.20)
        (9.65, 11.85, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15), # Ventana Habitación 2 (2.20 x 1.20)
        (13.15, 14.05, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.00),# Ventana Baño Privado Hab. Principal (0.90 x 0.90)
        (16.40, 18.80, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),# Ventana Habitación Principal (2.40 x 1.20)
        (20.25, 21.40, Z_P2_FLOOR + 1.05, Z_P2_FLOOR + 2.55),# Abertura lateral del Balcón Principal
    ])

    # 5. Muros Posteriores del Segundo Piso (Y: 3.50..3.65, X: 6.25..9.15; X: 6.25..6.40, Y: 0.00..3.50; Y: 0.00..0.15, X: 0.15..6.40)
    add_house_box(L_P2_EXT, 6, 6.25, 3.50, Z_P2_FLOOR, 9.15, 3.65, H_P2)
    add_wall_with_openings_y(L_P2_EXT, 6, 6.25, 6.40, 0.00, 3.50, Z_P2_FLOOR, H_P2, [
        (0.65, 2.85, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),  # Ventanal Estudio/Terraza posterior
    ])
    add_wall_with_openings_x(L_P2_EXT, 6, 0.15, 6.40, 0.00, 0.15, Z_P2_FLOOR, H_P2, [
        (0.60, 2.30, Z_P2_FLOOR + 1.10, Z_P2_FLOOR + 2.25),  # Ventilación Lavandería P2
        (3.60, 5.40, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),  # Ventana posterior para ventilación cruzada Norte-Sur
    ])

    # --- MUROS INTERIORES Y MOBILIARIO FIJO DEL SEGUNDO PISO ---
    # 1. Eje 2 (X: 5.85 a 6.00): Separa el Área Social (Sala-Comedor-Cocina) de la Zona Privada de Habitaciones
    #    - Tramo inferior (Y: 3.65 a 12.10): con puertas a Baño Compartido y Habitación 3, finalizando en la puerta de Habitación 2
    add_wall_with_openings_y(L_P2_INT, 6, 5.85, 6.00, 3.65, 12.10, Z_P2_FLOOR, H_P2, [
        (3.85, 4.55, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta Baño Compartido (0.70 m)
        (7.95, 8.65, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta Habitación 3 (0.70 m)
    ])
    #    - Tramo superior (Y: 15.15 a 21.56): separa la Sala-Comedor de la Habitación Principal y su Balcón,
    #      finalizando exactamente en la puerta de la Habitación Principal (Y = 15.15).
    add_house_box(L_P2_INT, 6, 5.85, 15.15, Z_P2_FLOOR, 6.00, Y_AV4 - 0.15, H_P2)

    # 2. Suite Habitación Principal + Closet + Baño Privado En-Suite (X: 6.00 a 9.00, Y: 12.70 a 19.95):
    #    - Puerta de entrada a la Habitación Principal (Y: 15.15 a 15.30, X: 6.00 a 6.80) finalizando la pared izquierda
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 6.80, 15.15, 15.30, Z_P2_FLOOR, H_P2, [
        (6.05, 6.75, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    #    - Closet/Vestier de la Habitación Principal (X: 6.80 a 9.00, Y: 14.70 a 15.30)
    add_house_box(L_P2_INT, 6, 6.80, 14.70, Z_P2_FLOOR, 6.95, 15.30, H_P2)
    add_house_box(L_P2_INT, 6, 6.80, 14.55, Z_P2_FLOOR, 9.00, 14.70, H_P2)
    #    - Baño Privado En-Suite (X: 6.80 a 9.00, Y: 12.70 a 14.55):
    #      Cerrado hacia el pasillo exterior y con acceso interno desde el vestíbulo privado de la Habitación Principal
    add_house_box(L_P2_INT, 6, 6.00, 14.55, Z_P2_FLOOR, 6.80, 14.70, H_P2) # Cierra hacia el pasillo general
    add_wall_with_openings_y(L_P2_INT, 6, 6.80, 6.95, 12.70, 14.55, Z_P2_FLOOR, H_P2, [
        (13.75, 14.45, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),     # Puerta del Baño Privado
    ])
    #      Puerta en el muro de Y = 14.55..14.70 para pasar del dormitorio principal a su baño privado:
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 6.80, 14.55, 14.70, Z_P2_FLOOR, H_P2, [
        (6.05, 6.75, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    #      Muro oeste de cierre del antebaño privado (X: 5.85 a 6.00, Y: 13.60 a 15.15)
    add_house_box(L_P2_INT, 6, 5.85, 13.60, Z_P2_FLOOR, 6.00, 15.15, H_P2)
    add_house_box(L_P2_INT, 6, 6.00, 13.60, Z_P2_FLOOR, 6.80, 13.75, H_P2)

    # 3. Habitación Secundaria 2 (X: 6.00 a 9.00, Y: 8.95 a 12.55 — 3.00 x 3.60 m):
    #    - Puerta de entrada (Y: 11.95 a 12.10, X: 6.00 a 6.80) finalizando la pared izquierda
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 6.80, 11.95, 12.10, Z_P2_FLOOR, H_P2, [
        (6.05, 6.75, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    add_house_box(L_P2_INT, 6, 6.80, 11.95, Z_P2_FLOOR, 6.95, 12.70, H_P2)
    add_house_box(L_P2_INT, 6, 6.80, 12.55, Z_P2_FLOOR, 9.00, 12.70, H_P2)

    # 4. Muros divisorios de Habitación 3 (Y: 5.55 a 8.80) y Baño Compartido (Y: 3.65 a 5.40)
    add_house_box(L_P2_INT, 6, 6.00, 8.80, Z_P2_FLOOR, 9.00, 8.95, H_P2)
    add_house_box(L_P2_INT, 6, 6.00, 5.40, Z_P2_FLOOR, 9.00, 5.55, H_P2)

    # 5. Cocina Abierta con Isla Central (después de la Sala-Comedor, en X: 0.30 a 5.85, Y: 7.35 a 14.50):
    #    - Mesón en L de Cocina (altura 0.90 m: Z = 3.00 a 3.90 m)
    add_house_box(L_P2_ISL, 3, 0.30, 7.50, Z_P2_FLOOR, 0.95, 13.50, Z_P2_FLOOR + 0.90) # Mesón largo izquierdo
    add_house_box(L_P2_ISL, 3, 0.95, 7.35, Z_P2_FLOOR, 2.75, 8.00,  Z_P2_FLOOR + 0.90) # Mesón en L sur
    #    - Gran Isla Central Desayunadora (2.60 x 0.95 m, en X: 2.15 a 3.10, Y: 9.80 a 12.40, altura 0.90 m)
    add_house_box(L_P2_ISL, 3, 2.15, 9.80, Z_P2_FLOOR, 3.10, 12.40, Z_P2_FLOOR + 0.90)

    # 6. Baranda / Muro de protección alrededor de la caja de escalera en Segundo Piso (Y: 4.25..7.50)
    add_house_box(L_P2_INT, 6, 0.30, 7.35, Z_P2_FLOOR, 2.75, 7.50, H_P2) # Respaldo sur del mesón de cocina
    add_house_box(L_P2_INT, 6, 2.65, 5.20, Z_P2_FLOOR, 2.80, 7.35, Z_P2_FLOOR + 1.05) # Baranda lateral escalera

    # 7. Lavandería y Estudio/Terraza Posterior del Segundo Piso (Y: 0.15 a 4.25)
    add_wall_with_openings_x(L_P2_INT, 6, 0.30, 2.75, 4.25, 4.40, Z_P2_FLOOR, H_P2, [
        (1.65, 2.45, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta a Lavandería P2
    ])
    add_house_box(L_P2_INT, 6, 2.75, 0.15, Z_P2_FLOOR, 2.90, 4.40, H_P2)
    add_wall_with_openings_x(L_P2_INT, 6, 2.90, 6.25, 3.50, 3.65, Z_P2_FLOOR, H_P2, [
        (3.90, 5.10, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Vano amplio hacia Estudio/Estar posterior
    ])

    # --- COLUMNAS SEGUNDO PISO (25x25 cm) PROLONGADAS DESDE EL PRIMER PISO ---
    for cx, cy in p1_cols_axes:
        add_house_box(L_P2_COL, 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, H_P2)

    # --- CUBIERTA SUPERIOR DEL SEGUNDO PISO (Z = +5.85 a +6.00 m) ---
    add_house_box(L_P2_ROOF, 9, 0.15, 0.00, H_P2, 6.40, 3.50, Z_ROOF_TOP)
    add_house_box(L_P2_ROOF, 9, 0.15, 3.50, H_P2, 9.15, Y_AV4, Z_ROOF_TOP)


    # --- EJES ESTRUCTURALES Y RÓTULOS 3D POR NIVEL ---
    L_GRID = "EJES_ESTRUCTURALES"
    for label, gx in [("0 (PROPIO)", 0.275), ("1", 2.825), ("2", 5.925), ("3", 9.075)]:
        add_house_line(L_GRID, 1, gx, -0.80, 0.0, gx, Y_AV4 + 0.80, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", gx - 0.30, Y_AV4 + 1.00, 0.0, 0.24)

    for label, gy in [("A0 (AV.4)", 21.585), ("A", 18.575), ("B", 16.325), ("C", 14.625), ("D", 12.025), ("E", 8.875), ("F", 6.575), ("G", 3.575)]:
        add_house_line(L_GRID, 1, -0.60, gy, 0.0, 10.00, gy, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", 10.20, gy - 0.10, 0.0, 0.24)

    # Rótulos Primer Piso (Local Comercial + Garaje Doble)
    p1_labels = [
        ("P1: GRAN LOCAL COMERCIAL (6,10 x 16,16m = 98,5 m2)", 3.40, 13.50, 0.05),
        ("P1: GARAJE DOBLE PRIVADO (2,45 x 12,76m)", 0.45, 15.00, 0.05),
        ("P1: Baño Local (3,00 x 1,75)", 6.40, 4.40, 0.05),
        ("P1: Deposito / Oficina Local (3,35 x 3,35)", 3.10, 1.70, 0.05),
        ("P1: Area Apoyo / Servicio", 0.50, 2.50, 0.05),
    ]
    for txt, rx, ry, rz in p1_labels:
        add_house_text("ROTULOS_TEXTO", 2, txt, rx, ry, rz, 0.22)

    # Rótulos Segundo Piso (Apartamento 3 Habitaciones)
    p2_labels = [
        ("P2: SALA - COMEDOR HACIA AV. 4 (5,55 x 7,00m)", 1.10, 18.00, Z_P2_FLOOR + 0.05),
        ("P2: COCINA CON ISLA CENTRAL (5,55 x 5,75m)", 1.10, 11.00, Z_P2_FLOOR + 0.05),
        ("P2: ISLA (2,60 x 0,95m)", 2.20, 11.40, Z_P2_FLOOR + 0.95),
        ("P2: BALCON PRIVADO HAB. PRINCIPAL (3,00 x 1,60m)", 6.15, 20.80, Z_P2_FLOOR + 0.05),
        ("P2: HABITACION PRINCIPAL (3,00 x 4,65m)", 6.20, 17.50, Z_P2_FLOOR + 0.05),
        ("P2: Baño Privado Suite (2,05 x 1,85m)", 7.00, 13.50, Z_P2_FLOOR + 0.05),
        ("P2: HABITACION 2 (3,00 x 3,60m)", 6.20, 10.50, Z_P2_FLOOR + 0.05),
        ("P2: HABITACION 3 (3,00 x 3,25m)", 6.20, 7.00, Z_P2_FLOOR + 0.05),
        ("P2: Baño Compartido (3,00 x 1,75m)", 6.30, 4.40, Z_P2_FLOOR + 0.05),
        ("P2: Lavanderia (2,45 x 4,10m)", 0.50, 2.20, Z_P2_FLOOR + 0.05),
        ("P2: Estudio / Terraza Posterior (3,35 x 3,35m)", 3.10, 1.70, Z_P2_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in p2_labels:
        add_house_text("P2_ROTULOS", 6, txt, rx, ry, rz, 0.20)

    # Rótulos Sótano
    sot_labels = [
        ("SOTANO: Cocina (4,40 x 3,30)", 2.20, 6.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Comedor (3,40)", 2.50, 4.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Sala (2,90 x 4,50)", 6.30, 5.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Habitacion 1 (2,50 x 3,35)", 0.45, 1.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Lavadero (1,65 x 2,50)", 3.10, 1.40, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Baño (1,50 x 1,79)", 4.85, 1.00, Z_SOT_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in sot_labels:
        add_house_text("SOTANO_ROTULOS", 4, txt, rx, ry, rz, 0.20)


    # =========================================================================
    # 4. TERRENO NO RECTANGULAR (CUADRO DE COORDENADAS UTM) Y DESNIVELES 3D
    #    SEGÚN FACHADA LATERAL IZQUIERDA (PÁGINAS 4 Y 5 DEL PDF)
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

    def add_terrain_strip_y(layer, color, x_left_b, x_right_b, y_b, z_bot_b, z_top_b,
                            x_left_f, x_right_f, y_f, z_bot_f, z_top_f):
        add_hexahedron(layer, color, [
            (x_left_b,  y_b, z_bot_b),
            (x_right_b, y_b, z_bot_b),
            (x_right_f, y_f, z_bot_f),
            (x_left_f,  y_f, z_bot_f),
            (x_left_b,  y_b, z_top_b),
            (x_right_b, y_b, z_top_b),
            (x_right_f, y_f, z_top_f),
            (x_left_f,  y_f, z_top_f),
        ])

    # A) Patio Posterior a nivel Sótano (Z = -2.55 m)
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

    # B) Retiro Lateral a nivel Sótano (Y_casa: 0.00 a 9.50)
    y_b1_0 = OFFSET_Y + 0.00
    y_b1_1 = OFFSET_Y + 3.50
    add_terrain_strip_y(L_TERR, 3,
                        6.40, x_right(y_b1_0), y_b1_0, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        6.40, x_right(y_b1_1), y_b1_1, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    y_b2_0 = OFFSET_Y + 3.50
    y_b2_1 = OFFSET_Y + 9.50
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_b2_0), y_b2_0, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        9.15, x_right(y_b2_1), y_b2_1, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    add_house_box(L_P1_EXT, 7, 9.00, 8.30, Z_SOT_FLOOR, 9.15, 9.50, Z_P1_FLOOR)

    # C) Los 5 Escalones de Desnivel (Y_casa: 9.50 a 11.20)
    num_terr_steps = 5
    t_step_dy = (11.20 - 9.50) / num_terr_steps
    t_step_dz = (-1.05 - Z_SOT_FLOOR) / num_terr_steps
    for s in range(num_terr_steps):
        yh0 = 9.50 + s * t_step_dy
        yh1 = yh0 + t_step_dy
        y0  = OFFSET_Y + yh0
        y1  = OFFSET_Y + yh1
        z_step_top = Z_SOT_FLOOR + (s + 1) * t_step_dz
        add_terrain_strip_y(L_TERR, 3,
                            9.15, x_right(y0), y0, Z_SOT_FLOOR - 0.20, z_step_top,
                            9.15, x_right(y1), y1, Z_SOT_FLOOR - 0.20, z_step_top)
        add_house_box(L_P1_EXT, 7, 9.00, yh0, z_step_top, 9.15, yh1, Z_P1_FLOOR)

    # D) Rampa inclinada continua (Y_casa: 11.20 a 18.65) y llegada plana a Avenida 4 (Y_casa: 18.65 a 21.71)
    y_slope_0 = OFFSET_Y + 11.20
    y_slope_1 = OFFSET_Y + 18.65
    y_front_av4 = OFFSET_Y + Y_AV4
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_slope_0), y_slope_0, -1.25, -1.05,
                        9.15, x_right(y_slope_1), y_slope_1, -0.20,  0.00)
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_slope_1), y_slope_1, -0.20, 0.00,
                        9.15, P2_LOC[0],          P2_LOC[1], -0.20, 0.00)
    add_terrain_strip_y(L_P1_EXT, 7,
                        9.00, 9.15, y_slope_0, -1.05, Z_P1_FLOOR,
                        9.00, 9.15, y_slope_1, -0.02, Z_P1_FLOOR)

    # Relleno natural bajo el Garaje y Local Comercial (Y_casa: 8.30 a 21.71, X: 0.15 a 9.00)
    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05)
    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05,
                        0.15, 9.00, y_front_av4,      -0.20, -0.15)

    # E) Pared del Vecino en el Lindero Izquierdo (X: 0.00 a 0.15, de P-4 a P-1 = 24.70 m) y Cerca Perimetral Derecha/Fondo
    wall_h = 2.50
    # Pared del vecino (Casa de Mario Graterol) en X: 0.00 a 0.15 a lo largo de los 24.70 m:
    add_box(L_FENCE, 8, 0.00, P4_LOC[1], Z_SOT_FLOOR, 0.15, OFFSET_Y + 8.30, Z_P1_FLOOR + wall_h)
    add_box(L_FENCE, 8, 0.00, OFFSET_Y + 8.30, 0.00, 0.15, P1_LOC[1], wall_h)

    # Lado 3-4 Fondo (P-4 a P-3, 10.81 m):
    add_hexahedron(L_FENCE, 8, [
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR),
        (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR),
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR + 2.20),
        (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR + 2.20),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR + 2.20),
        (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR + 2.20),
    ])

    # Lado 2-3 Derecho oblicuo (P-3 a P-2, 24.72 m) siguiendo los desniveles:
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(P3_LOC[1]) - 0.15, x_right(P3_LOC[1]), P3_LOC[1], Z_SOT_FLOOR, Z_SOT_FLOOR + 2.20,
                        x_right(y_b2_1) - 0.15,    x_right(y_b2_1),    y_b2_1,    Z_SOT_FLOOR, Z_SOT_FLOOR + 2.20)
    for s in range(num_terr_steps):
        y0 = OFFSET_Y + 9.50 + s * t_step_dy
        y1 = y0 + t_step_dy
        z_st = Z_SOT_FLOOR + (s + 1) * t_step_dz
        add_terrain_strip_y(L_FENCE, 8,
                            x_right(y0) - 0.15, x_right(y0), y0, z_st, z_st + 2.20,
                            x_right(y1) - 0.15, x_right(y1), y1, z_st, z_st + 2.20)
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(y_slope_0) - 0.15, x_right(y_slope_0), y_slope_0, -1.05, -1.05 + 2.20,
                        x_right(y_slope_1) - 0.15, x_right(y_slope_1), y_slope_1,  0.00,  2.20)
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(y_slope_1) - 0.15, x_right(y_slope_1), y_slope_1, 0.00, 2.20,
                        P2_LOC[0] - 0.15,          P2_LOC[0],          P2_LOC[1], 0.00, 2.20)

    # Brocal Frontal sobre Avenida 4 (Lado 1-2: P-1 a P-2, 11.37 m)
    add_hexahedron(L_FENCE, 1, [
        (P1_LOC[0], P1_LOC[1] - 0.15, -0.20),
        (P2_LOC[0], P2_LOC[1] - 0.15, -0.20),
        (P2_LOC[0], P2_LOC[1],        -0.20),
        (P1_LOC[0], P1_LOC[1],        -0.20),
        (P1_LOC[0], P1_LOC[1] - 0.15,  0.10),
        (P2_LOC[0], P2_LOC[1] - 0.15,  0.10),
        (P2_LOC[0], P2_LOC[1],         0.10),
        (P1_LOC[0], P1_LOC[1],         0.10),
    ])

    add_text(L_TERR, 1, "P-1 (N:1141664.17, E:529755.04)", P1_LOC[0] - 0.5, P1_LOC[1] + 0.5, 0.20, 0.28)
    add_text(L_TERR, 1, "P-2 (N:1141670.33, E:529764.60)", P2_LOC[0] - 3.5, P2_LOC[1] + 0.5, 0.20, 0.28)
    add_text(L_TERR, 1, "P-3 (N:1141648.99, E:529777.07)", P3_LOC[0] - 3.5, P3_LOC[1] - 0.6, Z_SOT_FLOOR, 0.28)
    add_text(L_TERR, 1, "P-4 (N:1141643.13, E:529767.99)", P4_LOC[0] - 0.5, P4_LOC[1] - 0.6, Z_SOT_FLOOR, 0.28)
    add_text(L_TERR, 2, "FRENTE AVENIDA 4 (11,37 m)", 3.20, 25.50, 0.20, 0.30)


    # =========================================================================
    # 5. LÁMINAS 2D COMPLEMENTARIAS (PLANTA SÓTANO Y PLANTA SEGUNDO PISO)
    # =========================================================================
    SX = 16.00
    SY = 2.00
    L_SOT_2D = "PLANTA_SOTANO_2D"
    add_text(L_SOT_2D, 2, "PLANTA SOTANO (ESCALA 1:75)", SX + 2.0, SY - 0.8, 0.0, 0.35)
    add_rect_2d(L_SOT_2D, 7, SX + 0.15, SY + 0.00, SX + 6.40, SY + 3.50)
    add_rect_2d(L_SOT_2D, 7, SX + 0.15, SY + 3.50, SX + 9.15, SY + 8.30)
    add_rect_2d(L_SOT_2D, 4, SX + 0.30, SY + 0.15, SX + 2.80, SY + 3.50)
    add_rect_2d(L_SOT_2D, 4, SX + 2.95, SY + 0.15, SX + 4.60, SY + 2.65)
    add_rect_2d(L_SOT_2D, 4, SX + 4.75, SY + 0.15, SX + 6.25, SY + 1.94)
    add_rect_2d(L_SOT_2D, 4, SX + 6.00, SY + 3.65, SX + 8.95, SY + 8.15)
    for i in range(13):
        yy = SY + 4.45 + i * ((7.40 - 4.45) / 12.0)
        add_line(L_SOT_2D, 3, SX + 0.30, yy, 0.0, SX + 1.40, yy, 0.0)
    add_text(L_SOT_2D, 2, "Cocina (4,40 x 3,30)", SX + 2.40, SY + 6.50, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Comedor (3,40)", SX + 2.60, SY + 4.80, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Sala (2,90 x 4,50)", SX + 6.40, SY + 5.80, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Habitacion 1 (2,50 x 3,35)", SX + 0.45, SY + 1.80, 0.0, 0.20)
    add_text(L_SOT_2D, 2, "Lavadero (1,65 x 2,50)", SX + 3.05, SY + 1.30, 0.0, 0.18)
    add_text(L_SOT_2D, 2, "Baño (1,50 x 1,79)", SX + 4.85, SY + 0.90, 0.0, 0.18)

    # LÁMINA 2D DE PLANTA SEGUNDO PISO (APARTAMENTO 3 HABITACIONES) EN Y = 13.00
    P2X = 16.00
    P2Y = 13.00
    L_P2_2D = "PLANTA_SEGUNDO_PISO_2D"
    add_text(L_P2_2D, 6, "PLANTA SEGUNDO PISO - APARTAMENTO 3 HABITACIONES", P2X + 0.5, P2Y - 0.8, 0.0, 0.32)
    add_rect_2d(L_P2_2D, 6, P2X + 0.15, P2Y + 0.00, P2X + 6.40, P2Y + 3.50)
    add_rect_2d(L_P2_2D, 6, P2X + 0.15, P2Y + 3.50, P2X + 9.15, P2Y + Y_AV4)
    # Divisiones 2D del Segundo Piso
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 20.10, P2X + 9.00, P2Y + Y_AV4) # Balcón Principal
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 14.70, P2X + 9.00, P2Y + 19.95) # Habitación Principal
    add_rect_2d(L_P2_2D, 6, P2X + 6.80, P2Y + 12.70, P2X + 9.00, P2Y + 14.55) # Baño Privado Suite
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 8.95,  P2X + 9.00, P2Y + 12.55) # Habitación 2
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 5.55,  P2X + 9.00, P2Y + 8.80)  # Habitación 3
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 3.65,  P2X + 9.00, P2Y + 5.40)  # Baño Compartido
    add_rect_2d(L_P2_2D, 3, P2X + 2.15, P2Y + 9.80,  P2X + 3.10, P2Y + 12.40) # Isla de Cocina
    add_rect_2d(L_P2_2D, 3, P2X + 0.30, P2Y + 7.50,  P2X + 0.95, P2Y + 13.50) # Mesón Cocina
    add_text(L_P2_2D, 2, "Sala - Comedor (5,55 x 7,00m)", P2X + 1.20, P2Y + 18.00, 0.0, 0.22)
    add_text(L_P2_2D, 2, "Cocina + Isla Central", P2X + 1.20, P2Y + 11.20, 0.0, 0.22)
    add_text(L_P2_2D, 2, "Balcon Principal (3,00 x 1,60)", P2X + 6.20, P2Y + 20.80, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Hab. Principal (3,00 x 4,65)", P2X + 6.20, P2Y + 17.50, 0.0, 0.20)
    add_text(L_P2_2D, 2, "Baño Suite (2,05 x 1,85)", P2X + 6.95, P2Y + 13.50, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Habitacion 2 (3,00 x 3,60)", P2X + 6.20, P2Y + 10.50, 0.0, 0.20)
    add_text(L_P2_2D, 2, "Habitacion 3 (3,00 x 3,25)", P2X + 6.20, P2Y + 7.00, 0.0, 0.20)
    add_text(L_P2_2D, 2, "Baño Comp. (3,00 x 1,75)", P2X + 6.20, P2Y + 4.40, 0.0, 0.18)


    # =========================================================================
    # 6. LÁMINA 2D DE LAS FACHADAS Y LEVANTAMIENTO POLIGONAL UTM
    # =========================================================================
    FX = 30.00
    FY = 2.00
    L_FAC = "FACHADAS_2D"

    add_text(L_FAC, 2, "FACHADA LATERAL IZQUIERDA - P2 / P1 / SOTANO", FX + 0.5, FY - 0.8, 0.0, 0.32)
    add_rect_2d(L_FAC, 4, FX + 0.00, FY + 0.00, FX + 3.80, FY + 2.40)
    add_rect_2d(L_FAC, 7, FX + 0.00, FY + 2.40, FX + 3.80, FY + 5.43)
    add_rect_2d(L_FAC, 6, FX + 0.00, FY + 5.43, FX + 3.80, FY + 8.43)
    add_rect_2d(L_FAC, 7, FX + 3.80, FY + 2.40, FX + 22.00, FY + 5.43)
    add_rect_2d(L_FAC, 6, FX + 3.80, FY + 5.43, FX + 22.00, FY + 8.43)
    add_line(L_FAC, 1, FX + 3.80, FY + 0.00, 0.0, FX + 9.50, FY + 0.00, 0.0)
    for s in range(num_terr_steps):
        sx0 = FX + 9.50 + s * t_step_dy
        sx1 = sx0 + t_step_dy
        sy0 = FY + s * 0.30
        sy1 = sy0 + 0.30
        add_line(L_FAC, 1, sx0, sy0, 0.0, sx0, sy1, 0.0)
        add_line(L_FAC, 1, sx0, sy1, 0.0, sx1, sy1, 0.0)
    add_line(L_FAC, 1, FX + 11.20, FY + 1.50, 0.0, FX + 18.95, FY + 2.40, 0.0)
    add_line(L_FAC, 1, FX + 18.95, FY + 2.40, 0.0, FX + 22.00, FY + 2.40, 0.0)

    UX = 55.00
    UY = 0.00
    L_UTM = "LEVANTAMIENTO_POLIGONAL_UTM"
    for de in range(0, 41, 10):
        add_line(L_UTM, 8, UX + de, UY + 0.0, 0.0, UX + de, UY + 40.0, 0.0)
        add_text(L_UTM, 7, f"E.={529750 + de},00", UX + de - 1.5, UY - 1.2, 0.0, 0.35)
    for dn in range(0, 41, 10):
        add_line(L_UTM, 8, UX + 0.0, UY + dn, 0.0, UX + 40.0, UY + dn, 0.0)
        add_text(L_UTM, 7, f"N.=1.141.{640 + dn},00", UX - 6.5, UY + dn - 0.15, 0.0, 0.35)

    P1 = (UX + 5.04,  UY + 24.17)
    P2 = (UX + 14.60, UY + 30.33)
    P3 = (UX + 27.07, UY + 8.99)
    P4 = (UX + 17.99, UY + 3.13)
    add_line(L_UTM, 1, P1[0], P1[1], 0.0, P2[0], P2[1], 0.0)
    add_line(L_UTM, 1, P2[0], P2[1], 0.0, P3[0], P3[1], 0.0)
    add_line(L_UTM, 1, P3[0], P3[1], 0.0, P4[0], P4[1], 0.0)
    add_line(L_UTM, 1, P4[0], P4[1], 0.0, P1[0], P1[1], 0.0)
    add_text(L_UTM, 1, "P-1 (N:1141664.17, E:529755.04)", P1[0] - 4.5, P1[1] + 0.4, 0.0, 0.30)
    add_text(L_UTM, 1, "P-2 (N:1141670.33, E:529764.60)", P2[0] - 1.0, P2[1] + 0.6, 0.0, 0.30)
    add_text(L_UTM, 1, "P-3 (N:1141648.99, E:529777.07)", P3[0] + 0.5, P3[1] - 0.2, 0.0, 0.30)
    add_text(L_UTM, 1, "P-4 (N:1141643.13, E:529767.99)", P4[0] - 2.0, P4[1] - 0.9, 0.0, 0.30)


    # =========================================================================
    # 7. ESCRITURA DEL ARCHIVO DXF (casa_modificaciones.dxf) Y 3D OBJ
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
    w(10, -5.0)
    w(20, -15.0)
    w(30, -4.0)
    w(9, "$EXTMAX")
    w(10, 100.0)
    w(20, 45.0)
    w(30, 8.0)
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "TABLES")
    w(0, "TABLE")
    w(2, "LAYER")
    w(70, 28)

    all_layers = [
        (L_TERR, 3),
        (L_FENCE, 8),
        (L_SOT_SLAB, 8),
        (L_SOT_EXT, 4),
        (L_SOT_INT, 4),
        (L_SOT_COL, 1),
        ("SOTANO_ROTULOS", 4),
        (L_P1_SLAB, 8),
        (L_P1_EXT, 7),
        (L_P1_INT, 7),
        (L_P1_COL, 1),
        ("ESCALERA_3D", 7),
        ("ESCALERA_2D", 7),
        ("ROTULOS_TEXTO", 2),
        (L_P2_SLAB, 8),
        (L_P2_EXT, 6),
        (L_P2_INT, 6),
        (L_P2_COL, 1),
        (L_P2_ISL, 3),
        ("P2_ESCALERA_3D", 7),
        (L_P2_ROOF, 9),
        ("P2_ROTULOS", 6),
        (L_GRID, 1),
        (L_SOT_2D, 4),
        (L_P2_2D, 6),
        (L_FAC, 3),
        (L_UTM, 7),
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
        w(0, "LINE")
        w(8, layer)
        w(62, color)
        w(10, f"{x1:.4f}"); w(20, f"{y1:.4f}"); w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}"); w(21, f"{y2:.4f}"); w(32, f"{z2:.4f}")

    for item in texts:
        layer, color, txt, x, y, z, h = item
        w(0, "TEXT")
        w(8, layer)
        w(62, color)
        w(10, f"{x:.4f}"); w(20, f"{y:.4f}"); w(30, f"{z:.4f}")
        w(40, f"{h:.4f}")
        w(1, txt)

    w(0, "ENDSEC")
    w(0, "EOF")

    # Escribir sobre casa_modificaciones.dxf y casa_completo.dxf (manteniendo casa_fiel_pdf.dxf y casa_fiel_pdf_respaldo.dxf intactos)
    for p in ["02_Modelos_CAD/casa_modificaciones.dxf", "02_Modelos_CAD/casa_completo.dxf", "02_Modelos_CAD/casa.dxf", "casa.dxf"]:
        try:
            with open(p, "w", encoding="latin-1", errors="replace") as f:
                f.writelines(dxf_lines)
            print(f"DXF actualizado con exito: {p}")
        except PermissionError:
            print(f"Archivo en uso por OpenCADStudio (se abrira la nueva copia): {p}")

    # Exportar OBJ actualizado
    obj_lines = ["# Modelo 3D Modificado (Sotano + Piso 1 Local Comercial y Garaje + Piso 2 Apartamento 3 Habs)\n\n"]
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

    with open("03_Modelos_3D/casa_3d.obj", "w", encoding="utf-8") as f:
        f.writelines(obj_lines)
    print(f"OBJ actualizado con {len(boxes_3d) + len(hexahedra_3d)} solidos 3D.")

    # Exportar STL para SketchUp Web (app.sketchup.com/app acepta .stl nativamente)
    stl_lines = ["solid casa_completa_3d\n"]
    def write_stl_tri(p1, p2, p3):
        # Calcular vector normal
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
        write_stl_quad(p0, p3, p2, p1) # Base
        write_stl_quad(p4, p5, p6, p7) # Tope
        write_stl_quad(p0, p1, p5, p4) # Sur
        write_stl_quad(p2, p3, p7, p6) # Norte
        write_stl_quad(p3, p0, p4, p7) # Oeste
        write_stl_quad(p1, p2, p6, p5) # Este

    for layer, color, pts in hexahedra_3d:
        p0, p1, p2, p3, p4, p5, p6, p7 = pts
        write_stl_quad(p0, p3, p2, p1) # Base
        write_stl_quad(p4, p5, p6, p7) # Tope
        write_stl_quad(p0, p1, p5, p4) # Sur
        write_stl_quad(p3, p2, p6, p7) # Norte
        write_stl_quad(p0, p3, p7, p4) # Oeste
        write_stl_quad(p1, p2, p6, p5) # Este

    stl_lines.append("endsolid casa_completa_3d\n")
    with open("03_Modelos_3D/casa_3d.stl", "w", encoding="utf-8") as f:
        f.writelines(stl_lines)
    print("STL actualizado con exito para SketchUp Web: 03_Modelos_3D/casa_3d.stl")

if __name__ == "__main__":
    build_full_project()
