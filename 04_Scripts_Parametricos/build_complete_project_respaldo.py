"""
Generador Maestro del Proyecto Arquitectónico Exacto según "planos de casa.pdf"
Incluye:
1. Planta Primer Piso (volumetría 3D y planta 2D exacta con retiros, recovecos, closets y cotas)
2. Planta Sótano (volumetría 3D y planta 2D alineada en Ejes 1-2-3 y F-G, escalera de 12 peldaños)
3. Distribución de Columnas (17 columnas 25x25 cm en Primer Piso, 6 columnas 35x35 cm en Sótano)
4. Fachadas 2D (Principal, Posterior y Lateral Izquierda con perfil escalonado del terreno)
5. Levantamiento Poligonal de Linderos con Coordenadas UTM exactas y Cajetín Oficial
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
        """
        Agrega un solido 3D de 8 vertices (base p0..p3 y tope p4..p7) para terrenos no rectangulares y en pendiente.
        """
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
    # PARÁMETROS VERTICALES (EJE Z) SEGÚN FACHADAS DEL PDF (PÁGINA 4)
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso acabado Sótano (Altura libre = 2.40 m)
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa entrepiso
    Z_P1_FLOOR     =  0.00   # Nivel piso acabado Primer Piso
    H_P1           =  2.85   # Altura muros Primer Piso (3.00 m con losa techo)
    Z_ROOF_TOP     =  3.00   # Nivel superior cubierta
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.00

    # Offset de implantación dentro de la parcela local (11.00 x 24.71 m)
    PLOT_W   = 11.00
    PLOT_L   = 24.71
    OFFSET_X =  0.00  # Pared de Garaje, Escalera, Cocina y Lavadero pegada al lindero izquierdo (X = 0.00)
    OFFSET_Y =  3.00  # Retiro de fondo hacia Solar de Miguel Rodríguez

    def add_house_box(layer, color, x1, y1, z1, x2, y2, z2):
        add_box(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_line(layer, color, x1, y1, z1, x2, y2, z2):
        add_line(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_text(layer, color, text, x, y, z, h=0.22):
        add_text(layer, color, text, OFFSET_X + x, OFFSET_Y + y, z, h)

    def add_wall_with_openings_x(layer, color, x1, x2, y1, y2, z_bot, z_top, openings):
        """
        Genera un muro horizontal (a lo largo de X) con vanos ordenados por X.
        openings: lista de tuplas (ox1, ox2, oz1, oz2)
        """
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
        """
        Genera un muro longitudinal (a lo largo de Y) con vanos ordenados por Y.
        openings: lista de tuplas (oy1, oy2, oz1, oz2)
        """
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
    # 1. NIVEL SÓTANO (PÁGINAS 2, 3 Y 4 DEL PDF)
    # Ubicado desde Y = 0.00 hasta Y = 8.30 m
    #   - Bloque Posterior (Y: 0.00 a 3.65, X: 0.00 a 6.40):
    #       * Habitación 1 Sótano (2.65/1.92 x 3.35 m)
    #       * Lavadero Sótano (1.65 x 2.50 m)
    #       * Baño Sótano (1.50 x 1.79 m)
    #   - Bloque Principal Ejes F-G (Y: 3.50 a 8.30, X: 0.00 a 9.15):
    #       * Escalera de 12 escalones (X: 0.15 a 1.40, Y: 4.45 a 7.40)
    #       * Cocina (4.40 x 3.30 m) y Comedor (3.40 m) (X: 1.40 a 5.85)
    #       * Sala Sótano (2.90 x 4.50 m) (X: 6.00 a 8.95, Y: 3.65 a 8.15)
    # =========================================================================
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT  = "SOTANO_MUROS_INT_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    # Losa de piso de Sótano (en L: bloque posterior 6.40x3.50 + bloque F-G 9.15x4.80)
    add_house_box(L_SOT_SLAB, 8, 0.00, 0.00, Z_SOT_SLAB_BOT, 6.40, 3.50, Z_SOT_FLOOR)
    add_house_box(L_SOT_SLAB, 8, 0.00, 3.50, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)

    # Escalera de 12 escalones (conecta Z = -2.55 en Y = 4.45 hasta Z = 0.00 en Y = 7.40)
    num_steps = 12
    step_dy = (7.40 - 4.45) / num_steps
    step_dz = (0.00 - Z_SOT_FLOOR) / num_steps
    for i in range(num_steps):
        y_s_top = 7.40 - i * step_dy
        y_s_bot = y_s_top - step_dy
        z_s_top = 0.00 - i * step_dz
        add_house_box("ESCALERA_3D", 7, 0.15, y_s_bot, Z_SOT_FLOOR, 1.40, y_s_top, z_s_top)
        add_house_line("ESCALERA_2D", 7, 0.15, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muro Oeste Sótano (Y: 0.00 a 8.30, X: 0.00 a 0.15): Muro lindero ciego pegado al límite del terreno
    add_house_box(L_SOT_EXT, 4, 0.00, 0.00, Z_SOT_FLOOR, 0.15, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur Sótano Posterior (Y: 0.00 a 0.15, X: 0.15 a 6.40)
    # Según Fachada Posterior: Ventana 1.90x1.10 en Hab1 y Celosía 0.70x0.40 en Lavadero/Baño
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.15, 6.40, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 2.50, Z_SOT_FLOOR + 1.00, Z_SOT_FLOOR + 2.10),  # Ventana 1.90 x 1.10
        (3.40, 4.10, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Celosía 0.70 x 0.40
    ])

    # Muro Este del bloque posterior del Sótano (X: 6.25 a 6.40, Y: 0.15 a 3.50)
    # Con las 2 celosías de 0.70x0.40 m en el tramo posterior de 3.80 m (Baño y Lavadero Sótano)
    add_wall_with_openings_y(L_SOT_EXT, 4, 6.25, 6.40, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 1.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
        (2.10, 2.80, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),
    ])

    # Muro Sur de Sala Sótano sobre Eje G (Y: 3.50 a 3.65, X: 6.00 a 9.15)
    # Incluye puerta exterior de 0.95 m (X: 7.95 a 8.90) y celosía alta según Fachada Posterior y Planta Sótano
    add_wall_with_openings_x(L_SOT_EXT, 4, 6.00, 9.15, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (6.60, 7.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Celosía alta
        (7.95, 8.90, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),   # Puerta 0.95 m
    ])

    # Muro Este de Sala Sótano sobre Eje 3 (X: 8.95 a 9.15, Y: 3.65 a 8.30)
    add_house_box(L_SOT_EXT, 4, 8.95, 3.65, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Muro Norte de Contención del Sótano (Y: 8.15 a 8.30, X: 0.15 a 9.15)
    add_house_box(L_SOT_EXT, 4, 0.15, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Tabiquería Interna del Sótano (Página 2):
    # 1. Muro en Eje G entre Habitación 1 / Pasillo y Comedor (Y: 3.50 a 3.65, X: 0.15 a 6.00)
    #    Con vano de paso de 1.00 m hacia el distribuidor (X: 3.95 a 4.95)
    add_wall_with_openings_x(L_SOT_INT, 4, 0.15, 6.00, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (3.95, 4.95, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])

    # 2. Muro divisorio Habitación 1 Sótano / Lavadero (X: 2.80 a 2.95, Y: 0.15 a 3.50)
    #    Con puerta de 0.80 m hacia Habitación 1 en Y: 2.60 a 3.40 y recoveco inferior de 1.92 m
    add_wall_with_openings_y(L_SOT_INT, 4, 2.80, 2.95, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (2.60, 3.40, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    # Closet/mocheta interior de Habitación 1 Sótano (deja 1.92 m libres abajo)
    add_house_box(L_SOT_INT, 4, 2.07, 0.15, Z_SOT_FLOOR, 2.80, 0.75, Z_P1_SLAB_BOT)

    # 3. Muro divisorio Lavadero / Baño Sótano (X: 4.60 a 4.75, Y: 0.15 a 2.65)
    add_house_box(L_SOT_INT, 4, 4.60, 0.15, Z_SOT_FLOOR, 4.75, 2.65, Z_P1_SLAB_BOT)

    # 4. Muro superior de Baño Sótano (Y: 1.94 a 2.09, X: 4.75 a 6.25, puerta de 0.70 m en X: 4.80 a 5.50)
    add_wall_with_openings_x(L_SOT_INT, 4, 4.75, 6.25, 1.94, 2.09, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (4.80, 5.50, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])

    # 5. Muro en Eje 2 entre Cocina/Comedor y Sala Sótano (X: 5.85 a 6.00, Y: 3.65 a 8.15)
    #    Con vano superior de 0.80 m (Y: 7.25 a 8.05) según cota "0,80" en Planta Sótano
    add_wall_with_openings_y(L_SOT_INT, 4, 5.85, 6.00, 3.65, 8.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (7.25, 8.05, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])

    # 6. Muro lateral de la Escalera en Sótano (X: 1.40 a 1.55, Y: 4.45 a 8.15)
    add_house_box(L_SOT_INT, 4, 1.40, 4.45, Z_SOT_FLOOR, 1.55, 8.15, Z_P1_SLAB_BOT)

    # Columnas Sótano 35x35 cm en Ejes (1, 2, 3) x (F, G) según Página 3 del PDF
    sot_cols_axes = [
        (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),  # Eje F: 1-F, 2-F, 3-F
        (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),  # Eje G: 1-G, 2-G, 3-G
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)


    # =========================================================================
    # 2. NIVEL PRIMER PISO (PÁGINAS 1, 2, 3 Y 4 DEL PDF)
    # Silueta escalonada exacta:
    #   - Bloque Posterior (Y: 0.00 a 3.50, X: 0.00 a 6.40): Lavadero + Cocina + Habitación 4
    #   - Cuerpo Central/Derecho (Y: 3.50 a 16.40, X: 0.00 a 9.15): Garaje + Sala/Comedor + Habs 2,3 y Baños
    #   - Frente Porche + Habitación 1 (Y: 16.40 a 18.65, X: 2.75 a 9.15)
    # =========================================================================
    L_P1_SLAB = "LOSA_PISO_3D"
    L_P1_EXT  = "MUROS_EXTERIORES_3D"
    L_P1_INT  = "MUROS_INTERIORES_3D"
    L_P1_COL  = "COLUMNAS_3D"

    # Losa de Entrepiso / Piso Primer Piso (Z: -0.15 a 0.00) respetando la silueta exacta y hueco de escalera
    add_house_box(L_P1_SLAB, 8, 0.00, 0.00, Z_P1_SLAB_BOT, 6.40, 3.50, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.00, 3.50, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    # Alrededor del hueco de escalera (X: 0.15 a 1.40, Y: 4.40 a 7.35)
    add_house_box(L_P1_SLAB, 8, 0.00, 4.40, Z_P1_SLAB_BOT, 0.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.00, 7.35, Z_P1_SLAB_BOT, 9.15, 16.40, Z_P1_FLOOR)
    # Losa de Porche y Habitación 1 (Y: 16.40 a 18.65, X: 2.75 a 9.15)
    add_house_box(L_P1_SLAB, 8, 2.75, 16.40, Z_P1_SLAB_BOT, 9.15, 18.65, Z_P1_FLOOR)

    # --- MUROS EXTERIORES PRIMER PISO ---
    # 1. Muro Lateral Izquierdo (Oeste, X: 0.00 a 0.15, Y: 0.00 a 16.40):
    #    Pared de Lavadero, Cocina, Escalera y Garaje PEGADA al lindero izquierdo del terreno (ciega)
    add_house_box(L_P1_EXT, 7, 0.00, 0.00, Z_P1_FLOOR, 0.15, 16.40, H_P1)

    # 2. Frente del Garaje (Y: 16.25 a 16.40, X: 0.00 a 2.75) con portón de garaje
    add_wall_with_openings_x(L_P1_EXT, 7, 0.00, 2.75, 16.25, 16.40, Z_P1_FLOOR, H_P1, [
        (0.25, 2.60, 0.00, 2.10),   # Portón de Garaje
    ])

    # 3. Porche (X: 2.75 a 5.85, Y: 16.40 a 18.65): ABIERTO sin paredes en el lado izquierdo ni al frente
    # 4. Frente de Habitación 1 sobre Eje A (Y: 18.50 a 18.65, X: 5.85 a 9.15) con ventana de 1.22 x 1.10 m
    add_wall_with_openings_x(L_P1_EXT, 7, 5.85, 9.15, 18.50, 18.65, Z_P1_FLOOR, H_P1, [
        (6.90, 8.12, 1.00, 2.10),   # Ventana frontal Habitación 1 (1.22 x 1.10 m)
    ])

    # 5. Muro Lateral sobre Eje 3 (X: 9.00 a 9.15, Y: 3.50 a 18.65 — Longitud = 15.15 m!)
    #    Con las 5 ventanas exactas del tramo de 15.15 m (Página 4: 0.90, 1.70, 2.20, 0.90, 2.20)
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 3.50, 18.65, Z_P1_FLOOR, H_P1, [
        (4.10,  5.00, 1.10, 2.00),  # Ventana Baño 2 (0.90 x 0.90)
        (6.30,  8.00, 1.00, 2.10),  # Ventana Habitación 3 (1.70 x 1.10)
        (9.65, 11.85, 1.00, 2.10),  # Ventana Habitación 2 (2.20 x 1.10)
        (13.15, 14.05, 1.10, 2.00), # Ventana Baño 1 (0.90 x 0.90)
        (15.50, 17.70, 1.00, 2.10), # Ventana Habitación 1 (2.20 x 1.10)
    ])

    # 6. Muro Sur de Baño 2 sobre Eje G (Y: 3.50 a 3.65, X: 6.25 a 9.15)
    add_house_box(L_P1_EXT, 7, 6.25, 3.50, Z_P1_FLOOR, 9.15, 3.65, H_P1)

    # 7. Muro Este de Habitación 4 (X: 6.25 a 6.40, Y: 0.00 a 3.50) con ventana de 2.20 x 1.10 m (tramo 3.80 m)
    add_wall_with_openings_y(L_P1_EXT, 7, 6.25, 6.40, 0.00, 3.50, Z_P1_FLOOR, H_P1, [
        (0.65, 2.85, 1.00, 2.10),   # Ventana lateral Habitación 4 (2.20 x 1.10 m)
    ])

    # 8. Muro Sur Posterior de Lavadero y Habitación 4 (Y: 0.00 a 0.15, X: 0.00 a 6.40)
    #    Según Fachada Posterior: Celosía/reja en Lavadero y Ventana 1.00x1.10 en Habitación 4
    add_wall_with_openings_x(L_P1_EXT, 7, 0.00, 6.40, 0.00, 0.15, Z_P1_FLOOR, H_P1, [
        (0.50, 2.35, 1.15, 2.60),   # Reja/ventilación posterior de Lavadero (1.85 m)
        (4.10, 5.10, 1.00, 2.10),   # Ventana posterior Habitación 4 (1.00 x 1.10 m)
    ])

    # --- MUROS INTERIORES PRIMER PISO ---
    # 1. Muro entre Lavadero y Cocina (Y: 1.65 a 1.80, X: 0.15 a 2.75) con vano central de 1.20 m
    add_wall_with_openings_x(L_P1_INT, 7, 0.15, 2.75, 1.65, 1.80, Z_P1_FLOOR, H_P1, [
        (0.85, 2.05, 0.00, H_DOOR),
    ])

    # 2. Muro de cierre de Lavadero en Eje 1 (X: 2.75 a 2.90, Y: 0.15 a 1.80)
    add_house_box(L_P1_INT, 7, 2.75, 0.15, Z_P1_FLOOR, 2.90, 1.80, H_P1)

    # 3. Muro norte de Habitación 4 sobre Eje G (Y: 3.50 a 3.65, X: 2.90 a 6.25) con puerta de 0.70 m
    add_wall_with_openings_x(L_P1_INT, 7, 2.90, 6.25, 3.50, 3.65, Z_P1_FLOOR, H_P1, [
        (4.10, 4.80, 0.00, H_DOOR),
    ])

    # 4. Muro oeste de Habitación 4 en Eje 1 (X: 2.75 a 2.90, Y: 1.80 a 3.65)
    add_house_box(L_P1_INT, 7, 2.75, 1.80, Z_P1_FLOOR, 2.90, 3.65, H_P1)

    # 5. Muro entre Cocina y Escalera (Y: 4.25 a 4.40, X: 0.15 a 1.55)
    add_house_box(L_P1_INT, 7, 0.15, 4.25, Z_P1_FLOOR, 1.55, 4.40, H_P1)

    # 6. Muro divisorio lateral de la Escalera (X: 1.40 a 1.55, Y: 4.40 a 7.35)
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.35, H_P1)

    # 7. Muro posterior del Garaje sobre Eje E (Y: 8.80 a 8.95, X: 0.15 a 2.75)
    add_house_box(L_P1_INT, 7, 0.15, 8.80, Z_P1_FLOOR, 2.75, 8.95, H_P1)

    # 8. Muro longitudinal de Sala y Comedor en Eje 1 (X: 2.75 a 2.90, Y: 6.05 a 16.25 — Longitud = 10.20 m!)
    add_house_box(L_P1_INT, 7, 2.75, 6.05, Z_P1_FLOOR, 2.90, 16.25, H_P1)

    # 9. Muro frontal de Sala hacia el Porche en Eje B (Y: 16.25 a 16.40, X: 2.75 a 5.85)
    #    Tramo izquierdo de 1.95 m con ventana de 2.20/1.20 m + Puerta principal de 0.95 m a la derecha
    add_wall_with_openings_x(L_P1_INT, 7, 2.75, 5.85, 16.25, 16.40, Z_P1_FLOOR, H_P1, [
        (3.15, 4.55, 1.00, 2.10),   # Ventana de Sala hacia el Porche
        (4.90, 5.85, 0.00, H_DOOR), # Puerta Principal de 0.95 m
    ])

    # 10. Muro longitudinal en Eje 2 (X: 5.85 a 6.00)
    #     Tramo inferior (Y: 3.65 a 12.10): separa Comedor/Sala de Baño 2, Habitación 3 y Habitación 2,
    #     finalizando exactamente en la Columna 2-D (Y = 12.025) y en la puerta de Habitación 2.
    add_wall_with_openings_y(L_P1_INT, 7, 5.85, 6.00, 3.65, 12.10, Z_P1_FLOOR, H_P1, [
        (3.85, 4.55, 0.00, H_DOOR), # Puerta Baño 2 (0.70 m)
        (5.70, 6.60, 0.00, H_DOOR), # Paso / vano intermedio
        (8.00, 8.70, 0.00, H_DOOR), # Puerta Habitación 3 (0.70 m)
    ])
    #     Tramo superior (Y: 15.15 a 18.50): separa Porche/Sala de Habitación 1,
    #     finalizando exactamente en la puerta de Habitación 1 (Y = 15.15).
    add_house_box(L_P1_INT, 7, 5.85, 15.15, Z_P1_FLOOR, 6.00, 18.50, H_P1)

    # 11. Vestíbulo de Baño 1, Habitación 1 y Habitación 2 (Y: 11.95 a 15.30, X: 6.00 a 9.00)
    #     - Puerta de entrada a Habitación 2 (Y: 11.95 a 12.10, X: 6.00 a 6.80) finalizando la pared izquierda
    add_wall_with_openings_x(L_P1_INT, 7, 6.00, 6.80, 11.95, 12.10, Z_P1_FLOOR, H_P1, [
        (6.05, 6.75, 0.00, H_DOOR),
    ])
    #     - Closet de Habitación 2 (X: 6.80 a 9.00, Y: 11.95 a 12.70 — 2.05 x 0.60 m)
    add_house_box(L_P1_INT, 7, 6.80, 11.95, Z_P1_FLOOR, 6.95, 12.70, H_P1)
    add_house_box(L_P1_INT, 7, 6.80, 12.55, Z_P1_FLOOR, 9.00, 12.70, H_P1)
    #     - Muro de entrada a Baño 1 (X: 6.80 a 6.95, Y: 12.70 a 14.55) con puerta de 0.70 m
    add_wall_with_openings_y(L_P1_INT, 7, 6.80, 6.95, 12.70, 14.55, Z_P1_FLOOR, H_P1, [
        (13.75, 14.45, 0.00, H_DOOR),
    ])
    #     - Muro entre Baño 1 y Closet de Habitación 1 (Y: 14.55 a 14.70, X: 6.80 a 9.00)
    add_house_box(L_P1_INT, 7, 6.80, 14.55, Z_P1_FLOOR, 9.00, 14.70, H_P1)
    #     - Closet inferior de Habitación 1 (X: 6.80 a 9.00, Y: 14.70 a 15.30 — 2.05 x 0.60 m)
    add_house_box(L_P1_INT, 7, 6.80, 14.70, Z_P1_FLOOR, 6.95, 15.30, H_P1)
    #     - Puerta de entrada a Habitación 1 (Y: 15.15 a 15.30, X: 6.00 a 6.80) finalizando la pared izquierda
    add_wall_with_openings_x(L_P1_INT, 7, 6.00, 6.80, 15.15, 15.30, Z_P1_FLOOR, H_P1, [
        (6.05, 6.75, 0.00, H_DOOR),
    ])

    # 12. Muro divisorio entre Baño 2 y Habitación 3 (Y: 5.40 a 5.55, X: 6.00 a 9.00)
    add_house_box(L_P1_INT, 7, 6.00, 5.40, Z_P1_FLOOR, 9.00, 5.55, H_P1)

    # 13. Muro divisorio entre Habitación 3 y Habitación 2 sobre Eje E (Y: 8.80 a 8.95, X: 6.00 a 9.00)
    add_house_box(L_P1_INT, 7, 6.00, 8.80, Z_P1_FLOOR, 9.00, 8.95, H_P1)

    # --- COLUMNAS PRIMER PISO (25x25 cm) EN LA RETÍCULA EXACTA DE LA PÁGINA 3 ---
    p1_cols_axes = [
        # Eje A (Y = 18.575)
        (5.925, 18.575), (9.075, 18.575),
        # Eje B (Y = 16.325)
        (2.825, 16.325), (5.925, 16.325),
        # Eje C (Y = 14.625 — muro entre Baño 1 y Closet de Habitación 1)
        (9.075, 14.625),
        # Eje D (Y = 12.025 — fin de la pared izquierda y puerta de Habitación 2)
        (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
        # Eje E (Y = 8.875)
        (2.825, 8.875), (5.925, 8.875), (9.075, 8.875),
        # Eje F (Y = 6.575)
        (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        # Eje G (Y = 3.575)
        (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in p1_cols_axes:
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)

    # --- CUBIERTA (Losa superior siguiendo la silueta exacta de la casa) ---
    L_ROOF = "CUBIERTA_3D"
    add_house_box(L_ROOF, 9, 0.00, 0.00, H_P1, 6.40, 3.50, Z_ROOF_TOP)
    add_house_box(L_ROOF, 9, 0.00, 3.50, H_P1, 9.15, 16.40, Z_ROOF_TOP)
    add_house_box(L_ROOF, 9, 2.75, 16.40, H_P1, 9.15, 18.65, Z_ROOF_TOP)

    # --- EJES ESTRUCTURALES Y RÓTULOS DE PLANTA ---
    L_GRID = "EJES_ESTRUCTURALES"
    for label, gx in [("1", 2.825), ("2", 5.925), ("3", 9.075)]:
        add_house_line(L_GRID, 1, gx, -0.80, 0.0, gx, 19.60, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", gx - 0.30, 19.80, 0.0, 0.28)

    for label, gy in [("A", 18.575), ("B", 16.325), ("C", 14.625), ("D", 12.025), ("E", 8.875), ("F", 6.575), ("G", 3.575)]:
        add_house_line(L_GRID, 1, -0.60, gy, 0.0, 10.00, gy, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", 10.20, gy - 0.10, 0.0, 0.28)

    # Rótulos de Ambientes Primer Piso
    p1_labels = [
        ("Porche. (2,10 x 2,25)", 3.30, 17.50, 0.05),
        ("Garaje. (2,60 x 7,45)", 0.60, 12.50, 0.05),
        ("Sala. (2,95 x 3,95)", 3.50, 12.50, 0.05),
        ("Comedor. (2,95 x 3,10)", 3.40, 7.50, 0.05),
        ("Cocina. (2,60 x 2,45)", 0.60, 2.90, 0.05),
        ("Lavadero. (2,60 x 1,50)", 0.50, 0.80, 0.05),
        ("Habitacion 1. (3,00 x 3,80)", 6.30, 16.80, 0.05),
        ("Baño. (2,05 x 1,85)", 7.20, 13.50, 0.05),
        ("Habitacion 2. (3,00 x 3,60)", 6.30, 10.50, 0.05),
        ("Habitacion 3. (3,00 x 3,25)", 6.30, 7.00, 0.05),
        ("Baño. (3,00 x 1,75)", 6.50, 4.40, 0.05),
        ("Habitacion 4. (3,35 x 3,35)", 3.30, 1.70, 0.05),
    ]
    for txt, rx, ry, rz in p1_labels:
        add_house_text("ROTULOS_TEXTO", 2, txt, rx, ry, rz, 0.22)

    # Rótulos de Ambientes Sótano
    sot_labels = [
        ("SOTANO: Cocina (4,40 x 3,30)", 2.20, 6.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Comedor (3,40)", 2.50, 4.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Sala (2,90 x 4,50)", 6.30, 5.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Habitacion 1 (2,65 x 3,35)", 0.35, 1.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Lavadero (1,65 x 2,50)", 3.10, 1.40, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Baño (1,50 x 1,79)", 4.85, 1.00, Z_SOT_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in sot_labels:
        add_house_text("SOTANO_ROTULOS", 4, txt, rx, ry, rz, 0.20)

    # =========================================================================
    # 3. TERRENO NO RECTANGULAR (CUADRO DE COORDENADAS UTM) Y DESNIVELES 3D
    #    SEGÚN FACHADA LATERAL IZQUIERDA (PÁGINAS 4 Y 5 DEL PDF)
    # =========================================================================
    # Transformación exacta de los 4 vértices UTM al sistema local de la casa
    # (con P-4 en el origen (0.00, 0.00) y el lado izquierdo P-4 -> P-1 sobre X = 0.00):
    #   P-4 (Fondo-Izq):  (0.0000,  0.0000)  [N: 1.141.643,13 | E: 529.767,99]
    #   P-1 (Frente-Izq): (0.0000, 24.7060)  [N: 1.141.664,17 | E: 529.755,04] -> Lado 4-1 = 24,70 m
    #   P-2 (Frente-Der): (11.3703, 24.9409) [N: 1.141.670,33 | E: 529.764,60] -> Lado 1-2 = 11,37 m
    #   P-3 (Fondo-Der):  (10.8043,  0.2311) [N: 1.141.648,99 | E: 529.777,07] -> Lado 2-3 = 24,72 m, Lado 3-4 = 10,81 m
    L_TERR  = "TERRENO_3D"
    L_FENCE = "CERCA_PERIMETRAL_3D"

    P4_LOC = (0.0000,  0.0000)
    P1_LOC = (0.0000, 24.7060)
    P2_LOC = (11.3703, 24.9409)
    P3_LOC = (10.8043,  0.2311)

    def x_right(y):
        """Coordenada X exacta sobre el lindero derecho oblicuo P-3 -> P-2 (24,72 m)."""
        return P3_LOC[0] + (P2_LOC[0] - P3_LOC[0]) * ((y - P3_LOC[1]) / (P2_LOC[1] - P3_LOC[1]))

    def y_rear(x):
        """Coordenada Y exacta sobre el lindero de fondo oblicuo P-4 -> P-3 (10,81 m)."""
        return P4_LOC[1] + (P3_LOC[1] - P4_LOC[1]) * (x / P3_LOC[0])

    def y_front(x):
        """Coordenada Y exacta sobre el lindero frontal oblicuo P-1 -> P-2 (11,37 m)."""
        return P1_LOC[1] + (P2_LOC[1] - P1_LOC[1]) * (x / P2_LOC[0])

    def add_terrain_strip_y(layer, color, x_left_b, x_right_b, y_b, z_bot_b, z_top_b,
                            x_left_f, x_right_f, y_f, z_bot_f, z_top_f):
        """Genera un prisma 3D trapezoidal/inclinado entre y_b y y_f adaptado al lindero oblicuo y pendiente."""
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

    # A) TRAMO 1: PATIO POSTERIOR DESDE EL LINDERO SURESTE OBLICUO (P-4 -> P-3) HASTA LA CASA (Y = 3.00)
    #    Nivel plano de Sótano (Z = -2.55 m, espesor 0.20 m)
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

    # B) TRAMO 2: RETIRO LATERAL A NIVEL DE SÓTANO (Z = -2.55 m) DESDE Y_CASA = 0.00 HASTA Y_CASA = 9.50
    #    - Subtramo B1 (Y_casa: 0.00 a 3.50, al lado del bloque posterior de 6.40 m de ancho):
    y_b1_0 = OFFSET_Y + 0.00
    y_b1_1 = OFFSET_Y + 3.50
    add_terrain_strip_y(L_TERR, 3,
                        6.40, x_right(y_b1_0), y_b1_0, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        6.40, x_right(y_b1_1), y_b1_1, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    #    - Subtramo B2 (Y_casa: 3.50 a 9.50, al lado del cuerpo principal de 9.15 m de ancho):
    y_b2_0 = OFFSET_Y + 3.50
    y_b2_1 = OFFSET_Y + 9.50
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_b2_0), y_b2_0, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        9.15, x_right(y_b2_1), y_b2_1, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    #    - Cierre de sobrecimiento bajo Primer Piso entre el fin del Sótano (Y_casa = 8.30) y el inicio de los escalones (Y_casa = 9.50)
    add_house_box(L_P1_EXT, 7, 9.00, 8.30, Z_SOT_FLOOR, 9.15, 9.50, Z_P1_FLOOR)

    # C) TRAMO 3: LOS 5 ESCALONES DE DESNIVEL DEL TERRENO SEGÚN FACHADA LATERAL IZQUIERDA (PÁGINA 4)
    #    Suben desde Z = -2.55 m en Y_casa = 9.50 hasta Z = -1.05 m en Y_casa = 11.20 (5 peldaños de 0.34 m x 0.30 m)
    num_terr_steps = 5
    t_step_dy = (11.20 - 9.50) / num_terr_steps   # 0.34 m por escalón
    t_step_dz = (-1.05 - Z_SOT_FLOOR) / num_terr_steps  # +0.30 m por escalón
    for s in range(num_terr_steps):
        yh0 = 9.50 + s * t_step_dy
        yh1 = yh0 + t_step_dy
        y0  = OFFSET_Y + yh0
        y1  = OFFSET_Y + yh1
        z_step_top = Z_SOT_FLOOR + (s + 1) * t_step_dz
        # Escalón de terreno en el retiro lateral (desde X = 9.15 hasta el lindero oblicuo x_right(y))
        add_terrain_strip_y(L_TERR, 3,
                            9.15, x_right(y0), y0, Z_SOT_FLOOR - 0.20, z_step_top,
                            9.15, x_right(y1), y1, Z_SOT_FLOOR - 0.20, z_step_top)
        # Muro de sobrecimiento/fundación escalonado bajo la fachada lateral (X: 9.00 a 9.15)
        add_house_box(L_P1_EXT, 7, 9.00, yh0, z_step_top, 9.15, yh1, Z_P1_FLOOR)

    # D) TRAMO 4: RAMPA / PENDIENTE INCLINADA CONTINUA DEL TERRENO (Y_CASA: 11.20 A 18.65)
    #    Sube en diagonal continua desde Z = -1.05 m en Y_casa = 11.20 hasta Z = 0.00 m en Y_casa = 18.65 (frente casa)
    y_slope_0 = OFFSET_Y + 11.20
    y_slope_1 = OFFSET_Y + 18.65
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_slope_0), y_slope_0, -1.25, -1.05,
                        9.15, x_right(y_slope_1), y_slope_1, -0.20,  0.00)
    # Muro de fundación triangular bajo el Eje 3 (X: 9.00 a 9.15, Y_casa: 11.20 a 18.65) tal como en la Fachada Lateral
    add_terrain_strip_y(L_P1_EXT, 7,
                        9.00, 9.15, y_slope_0, -1.05, Z_P1_FLOOR,
                        9.00, 9.15, y_slope_1, -0.02, Z_P1_FLOOR)
    # Relleno natural del terreno bajo el Garaje y Sala (Y_casa: 8.30 a 16.40/18.65, X: 0.00 a 9.00)
    add_terrain_strip_y(L_TERR, 3,
                        0.00, 9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        0.00, 9.00, OFFSET_Y + 11.20, -1.25, -1.05)
    add_terrain_strip_y(L_TERR, 3,
                        0.00, 9.00, OFFSET_Y + 11.20, -1.25, -1.05,
                        0.00, 9.00, OFFSET_Y + 16.40, -0.20, -0.15)

    # E) TRAMO 5: JARDÍN FRONTAL Y ACCESO VEHICULAR A NIVEL DE CALLE (Z = 0.00 m) HASTA EL LINDERO P-1 -> P-2
    #    - Acceso frente al Garaje (X: 0.00 a 2.75, desde Y_casa = 16.40 hasta Y = 21.65):
    add_terrain_strip_y(L_TERR, 3,
                        0.00, 2.75, OFFSET_Y + 16.40, -0.20, 0.00,
                        0.00, 2.75, OFFSET_Y + 18.65, -0.20, 0.00)
    #    - Franja frontal completa desde el frente de la casa (Y = 21.65) hasta la línea oblicua P-1 -> P-2 (Avenida 4):
    y_house_front = OFFSET_Y + 18.65
    add_hexahedron(L_TERR, 3, [
        (0.00,                  y_house_front, -0.20),
        (x_right(y_house_front), y_house_front, -0.20),
        (P2_LOC[0],             P2_LOC[1],     -0.20),
        (P1_LOC[0],             P1_LOC[1],     -0.20),
        (0.00,                  y_house_front,  0.00),
        (x_right(y_house_front), y_house_front,  0.00),
        (P2_LOC[0],             P2_LOC[1],      0.00),
        (P1_LOC[0],             P1_LOC[1],      0.00),
    ])

    # F) CERCA PERIMETRAL 3D SIGUIENDO LA POLIGONAL NO RECTANGULAR EXACTA (P-1, P-2, P-3, P-4) Y SUS DESNIVELES
    wall_h = 2.20
    # 1. Lado 4-1 Izquierdo (X: 0.00 a 0.15, longitud total = 24,70 m):
    #    - Tramo trasero (de P-4 en Y = 0.00 hasta el inicio del Lavadero en Y = 3.00):
    add_box(L_FENCE, 8, 0.00, P4_LOC[1], Z_SOT_FLOOR, 0.15, OFFSET_Y, Z_SOT_FLOOR + wall_h)
    #    - Entre Y = 3.00 y Y = 19.40 la pared de Lavadero, Cocina, Escalera y Garaje está pegada al lindero (X = 0.00)
    #    - Tramo delantero (desde el frente del Garaje en Y = 19.40 hasta el vértice P-1 en Y = 24.706):
    add_box(L_FENCE, 8, 0.00, OFFSET_Y + 16.40, 0.00, 0.15, P1_LOC[1], wall_h)

    # 2. Lado 3-4 Fondo (de P-4 a P-3, longitud = 10,81 m, S 57°10'22.40" W):
    add_hexahedron(L_FENCE, 8, [
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR),
        (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR),
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR + wall_h),
        (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR + wall_h),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR + wall_h),
        (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR + wall_h),
    ])

    # 3. Lado 2-3 Derecho oblicuo (de P-3 a P-2, longitud = 24,72 m, S 30°17'59.36" E) siguiendo los desniveles:
    #    - Tramo bajo Sótano (de P-3 hasta Y = OFFSET_Y + 9.50):
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(P3_LOC[1]) - 0.15, x_right(P3_LOC[1]), P3_LOC[1], Z_SOT_FLOOR, Z_SOT_FLOOR + wall_h,
                        x_right(y_b2_1) - 0.15,    x_right(y_b2_1),    y_b2_1,    Z_SOT_FLOOR, Z_SOT_FLOOR + wall_h)
    #    - Tramo de los 5 escalones (Y: OFFSET_Y + 9.50 a OFFSET_Y + 11.20):
    for s in range(num_terr_steps):
        y0 = OFFSET_Y + 9.50 + s * t_step_dy
        y1 = y0 + t_step_dy
        z_st = Z_SOT_FLOOR + (s + 1) * t_step_dz
        add_terrain_strip_y(L_FENCE, 8,
                            x_right(y0) - 0.15, x_right(y0), y0, z_st, z_st + wall_h,
                            x_right(y1) - 0.15, x_right(y1), y1, z_st, z_st + wall_h)
    #    - Tramo en rampa inclinada (Y: OFFSET_Y + 11.20 a OFFSET_Y + 18.65):
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(y_slope_0) - 0.15, x_right(y_slope_0), y_slope_0, -1.05, -1.05 + wall_h,
                        x_right(y_slope_1) - 0.15, x_right(y_slope_1), y_slope_1,  0.00,  0.00 + wall_h)
    #    - Tramo frontal alto hasta P-2 (Y: OFFSET_Y + 18.65 a P-2):
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(y_house_front) - 0.15, x_right(y_house_front), y_house_front, 0.00, wall_h,
                        P2_LOC[0] - 0.15,              P2_LOC[0],              P2_LOC[1],     0.00, wall_h)

    # 4. Lado 1-2 Frente oblicuo sobre Avenida 4 (de P-1 a P-2, longitud = 11,37 m, N 57°10'22.40" E):
    #    Brocal/delimitación frontal a nivel de acera (Z: -0.20 a +0.15 m) para dejar libre el acceso y vista frontal
    add_hexahedron(L_FENCE, 1, [
        (P1_LOC[0], P1_LOC[1] - 0.15, -0.20),
        (P2_LOC[0], P2_LOC[1] - 0.15, -0.20),
        (P2_LOC[0], P2_LOC[1],        -0.20),
        (P1_LOC[0], P1_LOC[1],        -0.20),
        (P1_LOC[0], P1_LOC[1] - 0.15,  0.15),
        (P2_LOC[0], P2_LOC[1] - 0.15,  0.15),
        (P2_LOC[0], P2_LOC[1],         0.15),
        (P1_LOC[0], P1_LOC[1],         0.15),
    ])

    # Rótulos 3D de los Vértices UTM y Linderos directamente en el modelo 3D del terreno:
    add_text(L_TERR, 1, "P-1 (N:1141664.17, E:529755.04)", P1_LOC[0] - 0.5, P1_LOC[1] + 0.5, 0.20, 0.28)
    add_text(L_TERR, 1, "P-2 (N:1141670.33, E:529764.60)", P2_LOC[0] - 3.5, P2_LOC[1] + 0.5, 0.20, 0.28)
    add_text(L_TERR, 1, "P-3 (N:1141648.99, E:529777.07)", P3_LOC[0] - 3.5, P3_LOC[1] - 0.6, Z_SOT_FLOOR, 0.28)
    add_text(L_TERR, 1, "P-4 (N:1141643.13, E:529767.99)", P4_LOC[0] - 0.5, P4_LOC[1] - 0.6, Z_SOT_FLOOR, 0.28)
    add_text(L_TERR, 2, "FRENTE AVENIDA 4 (11,37 m)", 3.50, 25.40, 0.20, 0.30)
    add_text(L_TERR, 2, "FONDO SOLAR MIGUEL RODRIGUEZ (10,81 m)", 2.50, -1.20, Z_SOT_FLOOR, 0.28)


    # =========================================================================
    # 4. LÁMINA 2D DE PLANTA SÓTANO INDEPENDIENTE (AL LADO DERECHO, COMO EN PÁG. 2)
    # =========================================================================
    SX = 16.00
    SY = 2.00
    L_SOT_2D = "PLANTA_SOTANO_2D"
    add_text(L_SOT_2D, 2, "PLANTA SOTANO (ESCALA 1:75)", SX + 2.0, SY - 0.8, 0.0, 0.35)
    # Contorno en L del Sótano
    add_rect_2d(L_SOT_2D, 7, SX + 0.00, SY + 0.00, SX + 6.40, SY + 3.50)
    add_rect_2d(L_SOT_2D, 7, SX + 0.00, SY + 3.50, SX + 9.15, SY + 8.30)
    # Divisiones internas 2D del Sótano
    add_rect_2d(L_SOT_2D, 4, SX + 0.15, SY + 0.15, SX + 2.80, SY + 3.50) # Hab 1
    add_rect_2d(L_SOT_2D, 4, SX + 2.95, SY + 0.15, SX + 4.60, SY + 2.65) # Lavadero
    add_rect_2d(L_SOT_2D, 4, SX + 4.75, SY + 0.15, SX + 6.25, SY + 1.94) # Baño
    add_rect_2d(L_SOT_2D, 4, SX + 6.00, SY + 3.65, SX + 8.95, SY + 8.15) # Sala
    # Escalera 12 peldaños 2D
    for i in range(13):
        yy = SY + 4.45 + i * ((7.40 - 4.45) / 12.0)
        add_line(L_SOT_2D, 3, SX + 0.15, yy, 0.0, SX + 1.40, yy, 0.0)
    add_text(L_SOT_2D, 2, "Cocina (4,40 x 3,30)", SX + 2.40, SY + 6.50, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Comedor (3,40)", SX + 2.60, SY + 4.80, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Sala (2,90 x 4,50)", SX + 6.40, SY + 5.80, 0.0, 0.22)
    add_text(L_SOT_2D, 2, "Habitacion 1 (2,65 x 3,35)", SX + 0.35, SY + 1.80, 0.0, 0.20)
    add_text(L_SOT_2D, 2, "Lavadero (1,65 x 2,50)", SX + 3.05, SY + 1.30, 0.0, 0.18)
    add_text(L_SOT_2D, 2, "Baño (1,50 x 1,79)", SX + 4.85, SY + 0.90, 0.0, 0.18)


    # =========================================================================
    # 5. LÁMINA 2D DE LAS 3 FACHADAS EXACTAS DEL PDF (PÁGINA 4)
    # =========================================================================
    FX = 30.00
    FY = 2.00
    L_FAC = "FACHADAS_2D"

    # A) FACHADA PRINCIPAL - PRIMER PISO (Ancho: 1.47 + 3.90 + 3.70 = 9.07/9.25 m)
    add_text(L_FAC, 2, "FACHADA PRINCIPAL - PRIMER PISO", FX + 1.5, FY + 11.2, 0.0, 0.32)
    # Garaje izquierda
    add_rect_2d(L_FAC, 7, FX + 0.00, FY + 12.0, FX + 1.47, FY + 12.0 + 2.50)
    add_rect_2d(L_FAC, 3, FX + 0.20, FY + 12.0, FX + 1.23, FY + 12.0 + 2.03) # Portón
    # Cuerpo central Porche/Sala (ancho 3.90 m, alto 3.00 / 3.20 m)
    add_rect_2d(L_FAC, 7, FX + 1.47, FY + 12.0, FX + 5.37, FY + 12.0 + 3.00)
    add_rect_2d(L_FAC, 4, FX + 1.90, FY + 12.0 + 0.90, FX + 4.10, FY + 12.0 + 2.00) # Ventana 2.20x1.10
    add_rect_2d(L_FAC, 3, FX + 4.30, FY + 12.0, FX + 5.25, FY + 12.0 + 2.00)        # Puerta 0.95x2.00
    # Cuerpo derecho Habitación 1 (ancho 3.70 m, alto 3.00 m)
    add_rect_2d(L_FAC, 7, FX + 5.37, FY + 12.0, FX + 9.07, FY + 12.0 + 3.00)
    add_rect_2d(L_FAC, 4, FX + 6.00, FY + 12.0 + 0.90, FX + 7.22, FY + 12.0 + 2.00) # Ventana 1.22x1.10

    # B) FACHADA POSTERIOR - PRIMER PISO Y SÓTANO (Ancho: 9.25 m, Alto: 3.00 + 2.40 m)
    PY = FY + 18.0
    add_text(L_FAC, 2, "FACHADA POSTERIOR - PRIMER PISO / SOTANO (9,25 m)", FX + 1.0, PY - 0.8, 0.0, 0.32)
    # Nivel Sótano (Z: 0 a 2.40 en dibujo)
    add_rect_2d(L_FAC, 4, FX + 0.00, PY + 0.00, FX + 6.20, PY + 2.40)
    add_rect_2d(L_FAC, 4, FX + 6.20, PY + 0.00, FX + 9.25, PY + 2.40)
    add_rect_2d(L_FAC, 3, FX + 0.60, PY + 0.90, FX + 2.50, PY + 2.00) # Ventana 1.90x1.10
    add_rect_2d(L_FAC, 3, FX + 3.40, PY + 1.60, FX + 4.10, PY + 2.00) # Celosía 0.70x0.40
    add_rect_2d(L_FAC, 3, FX + 7.95, PY + 0.00, FX + 8.95, PY + 2.00) # Puerta 1.00x2.00
    # Nivel Primer Piso (Z: 2.40 a 5.40 en dibujo: 2.60 + 3.60 + 2.75)
    add_rect_2d(L_FAC, 7, FX + 0.00, PY + 2.40, FX + 2.60, PY + 5.40) # Lavadero + tejas
    add_rect_2d(L_FAC, 7, FX + 2.60, PY + 2.40, FX + 6.20, PY + 5.40) # Habitación 4
    add_rect_2d(L_FAC, 7, FX + 6.20, PY + 2.40, FX + 9.25, PY + 5.40) # Baño 2
    add_rect_2d(L_FAC, 4, FX + 3.90, PY + 3.40, FX + 4.90, PY + 4.50) # Ventana 1.00x1.10

    # C) FACHADA LATERAL IZQUIERDA - PRIMER PISO Y SÓTANO (3.80 m + 15.15 m, altura máx 5.63 m)
    add_text(L_FAC, 2, "FACHADA LATERAL IZQUIERDA - PRIMER PISO / SOTANO (3,80 + 15,15 m)", FX + 0.5, FY - 0.8, 0.0, 0.32)
    # Bloque trasero izquierdo (ancho 3.80 m, Primer Piso + Sótano, altura total 5.63 m)
    add_rect_2d(L_FAC, 4, FX + 0.00, FY + 0.00, FX + 3.80, FY + 2.40) # Sótano 2.40 m
    add_rect_2d(L_FAC, 7, FX + 0.00, FY + 2.40, FX + 3.80, FY + 5.43) # Primer Piso
    add_rect_2d(L_FAC, 3, FX + 0.80, FY + 3.30, FX + 3.00, FY + 4.40) # Ventana 2.20x1.10
    add_rect_2d(L_FAC, 3, FX + 0.60, FY + 1.60, FX + 1.30, FY + 2.00) # Celosía 0.70x0.40
    add_rect_2d(L_FAC, 3, FX + 1.80, FY + 1.60, FX + 2.50, FY + 2.00) # Celosía 0.70x0.40
    # Cuerpo principal de 15.15 m (X: 3.80 a 18.95, altura 3.03 m en Y: 2.40 a 5.43)
    add_rect_2d(L_FAC, 7, FX + 3.80, FY + 2.40, FX + 18.95, FY + 5.43)
    # 5 Ventanas laterales (0.90, 1.70, 2.20, 0.90, 2.20)
    add_rect_2d(L_FAC, 3, FX + 4.50,  FY + 3.50, FX + 5.40,  FY + 4.40)
    add_rect_2d(L_FAC, 3, FX + 6.50,  FY + 3.30, FX + 8.20,  FY + 4.40)
    add_rect_2d(L_FAC, 3, FX + 9.40,  FY + 3.30, FX + 11.60, FY + 4.40)
    add_rect_2d(L_FAC, 3, FX + 12.80, FY + 3.50, FX + 13.70, FY + 4.40)
    add_rect_2d(L_FAC, 3, FX + 15.00, FY + 3.30, FX + 17.20, FY + 4.40)
    # Perfil exacto del terreno bajo los 15.15 m (plano Sótano -> 5 escalones -> rampa inclinada hasta Calle)
    add_line(L_FAC, 1, FX + 3.80, FY + 0.00, 0.0, FX + 9.50, FY + 0.00, 0.0)
    for s in range(num_terr_steps):
        sx0 = FX + 9.50 + s * t_step_dy
        sx1 = sx0 + t_step_dy
        sy0 = FY + s * 0.30
        sy1 = sy0 + 0.30
        add_line(L_FAC, 1, sx0, sy0, 0.0, sx0, sy1, 0.0)
        add_line(L_FAC, 1, sx0, sy1, 0.0, sx1, sy1, 0.0)
    add_line(L_FAC, 1, FX + 11.20, FY + 1.50, 0.0, FX + 18.95, FY + 2.40, 0.0)


    # =========================================================================
    # 6. LEVANTAMIENTO POLIGONAL DE LINDEROS CON GEOMETRÍA UTM EXACTA (PÁGINA 5)
    # Coordenadas UTM reales trasladadas a origen relativo (E0 = 529750, N0 = 1141640)
    #   P-1: E = 529755.04 (+5.04),  N = 1141664.17 (+24.17)
    #   P-2: E = 529764.60 (+14.60), N = 1141670.33 (+30.33)  [11.37 m, N 57°10'22.40" E]
    #   P-3: E = 529777.07 (+27.07), N = 1141648.99 (+8.99)   [24.72 m, S 30°17'59.36" E]
    #   P-4: E = 529767.99 (+17.99), N = 1141643.13 (+3.13)   [10.81 m, S 57°10'22.40" W]
    # =========================================================================
    UX = 55.00
    UY = 0.00
    L_UTM = "LEVANTAMIENTO_POLIGONAL_UTM"

    # Cuadrícula UTM 10x10 m (E = 529.750 a 529.790, N = 1.141.640 a 1.141.680)
    for de in range(0, 41, 10):
        add_line(L_UTM, 8, UX + de, UY + 0.0, 0.0, UX + de, UY + 40.0, 0.0)
        add_text(L_UTM, 7, f"E.={529750 + de},00", UX + de - 1.5, UY - 1.2, 0.0, 0.35)
    for dn in range(0, 41, 10):
        add_line(L_UTM, 8, UX + 0.0, UY + dn, 0.0, UX + 40.0, UY + dn, 0.0)
        add_text(L_UTM, 7, f"N.=1.141.{640 + dn},00", UX - 6.5, UY + dn - 0.15, 0.0, 0.35)

    # Vértices exactos P-1, P-2, P-3, P-4
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

    # Textos de Linderos en la Poligonal UTM
    add_text(L_UTM, 2, "NOROESTE: AVENIDA 4 (11.37m - N 57*10'22.40\" E)", UX + 2.0, UY + 32.5, 0.0, 0.35)
    add_text(L_UTM, 2, "NORESTE: CASA DE MIGUEL RODRIGUEZ (24.72m)", UX + 22.0, UY + 21.0, 0.0, 0.32)
    add_text(L_UTM, 2, "SUROESTE: CASA DE MARIO GRATEROL (24.70m)", UX + 1.0, UY + 12.0, 0.0, 0.32)
    add_text(L_UTM, 2, "SURESTE: SOLAR DE MIGUEL RODRIGUEZ (10.81m)", UX + 16.0, UY + 1.2, 0.0, 0.32)
    add_text(L_UTM, 2, "CALLE 30", UX + 32.0, UY + 30.0, 0.0, 0.40)

    # Cuadro de Coordenadas UTM y Cajetín Oficial (debajo de la poligonal UTM)
    TX = UX
    TY = UY - 12.0
    add_rect_2d(L_UTM, 7, TX, TY, TX + 40.0, TY + 9.5)
    add_text(L_UTM, 1, "REPUBLICA BOLIVARIANA DE VENEZUELA - MUNICIPIO INDEPENDENCIA YARACUY", TX + 1.0, TY + 8.6, 0.0, 0.42)
    add_text(L_UTM, 2, "PROPIEDAD: ALVARO ARGELIO DIAZ FLOREZ (C.I.: 24.633.787) | UBICACION: AV. 4 ENTRE CALLES 30 Y 31 N 30-7", TX + 1.0, TY + 7.7, 0.0, 0.30)
    add_text(L_UTM, 2, "LEVANTADO, CALCULADO Y DIGITALIZO: T.S.U. ANGEL CAMACARO M. (CVPT: N 1260 / SOVIT: N 0050) | FECHA: MAR 2026", TX + 1.0, TY + 6.9, 0.0, 0.28)
    add_text(L_UTM, 3, "AREA DE TERRENO: 273,81 m2   |   AREA DE CONSTRUCCION: 215,98 m2   |   ESCALA: 1:75 / 1:200", TX + 1.0, TY + 6.0, 0.0, 0.32)
    add_text(L_UTM, 7, "LADO    RUMBO               DISTANCIA    VERTICE     NORTE (U.T.M.)     ESTE (U.T.M.)      LINDEROS", TX + 1.0, TY + 4.8, 0.0, 0.28)
    add_text(L_UTM, 7, "1 - 2   N 57*10'22.40\" E     11.37 m        1        1.141.664,17       529.755,04         NOROESTE: AVENIDA 4", TX + 1.0, TY + 3.8, 0.0, 0.26)
    add_text(L_UTM, 7, "2 - 3   S 30*17'59.36\" E     24.72 m        2        1.141.670,33       529.764,60         NORESTE: CASA DE MIGUEL RODRIGUEZ", TX + 1.0, TY + 2.9, 0.0, 0.26)
    add_text(L_UTM, 7, "3 - 4   S 57*10'22.40\" W     10.81 m        3        1.141.648,99       529.777,07         SURESTE: SOLAR DE MIGUEL RODRIGUEZ", TX + 1.0, TY + 2.0, 0.0, 0.26)
    add_text(L_UTM, 7, "4 - 1   N 31*36'27.01\" W     24.70 m        4        1.141.643,13       529.767,99         SUROESTE: CASA DE MARIO GRATEROL", TX + 1.0, TY + 1.1, 0.0, 0.26)


    # =========================================================================
    # 7. ESCRITURA DEL ARCHIVO DXF Y DEL ARCHIVO 3D OBJ/STL
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
    w(30, 6.0)
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "TABLES")
    w(0, "TABLE")
    w(2, "LAYER")
    w(70, 20)

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
        (L_ROOF, 9),
        ("ESCALERA_3D", 7),
        ("ESCALERA_2D", 7),
        ("ROTULOS_TEXTO", 2),
        (L_GRID, 1),
        (L_SOT_2D, 4),
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
        write_3dface(layer, color, p0, p1, p2, p3)  # Base
        write_3dface(layer, color, p4, p5, p6, p7)  # Tope
        write_3dface(layer, color, p0, p1, p5, p4)  # Sur/Atrás
        write_3dface(layer, color, p3, p2, p6, p7)  # Norte/Frente
        write_3dface(layer, color, p0, p3, p7, p4)  # Oeste/Izq
        write_3dface(layer, color, p1, p2, p6, p5)  # Este/Der

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

    for p in ["02_Modelos_CAD/casa_fiel_pdf.dxf", "02_Modelos_CAD/casa_completo.dxf", "02_Modelos_CAD/casa.dxf", "casa.dxf"]:
        try:
            with open(p, "w", encoding="latin-1", errors="replace") as f:
                f.writelines(dxf_lines)
            print(f"DXF actualizado con exito: {p}")
        except PermissionError:
            print(f"Archivo en uso por OpenCADStudio (se abrira la nueva copia): {p}")

    # Exportar OBJ actualizado
    obj_lines = ["# Modelo 3D Fiel al PDF (Planta Primer Piso + Sotano + Terreno Poligonal UTM)\n\n"]
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

if __name__ == "__main__":
    build_full_project()
