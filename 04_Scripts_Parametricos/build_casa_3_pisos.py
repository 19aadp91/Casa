"""
Generador Maestro del Proyecto Ampliación a 3 Pisos + Bodega Comercial
Archivo de salida: "02_Modelos_CAD/casa_proyecto_3_pisos.dxf"
(Mantiene "02_Modelos_CAD/casa_nuevo_proyecto.dxf" y "build_nuevo_proyecto.py" 100% intactos).

IMPLEMENTA LA OPCIÓN A APROBADA + LAS 7 CORRECCIONES ARQUITECTÓNICAS Y FUNCIONALES:
1. SÓTANO (Z = -2,55 m): Gran Bodega Mayorista (74,70 m²) con pasillo central libre de 1,95 m frente
   a la puerta batiente de la escalera, avenida recta de carga de 2,20 m desde el portón doble Sur,
   racks perimetrales ordenados, cámara de pre-frío y báscula/mesa de control adosadas al baño.
2. PLANTA BAJA (Z = 0,00 m): Eliminada la antigua bodega posterior redundante; salón comercial ampliado
   (~112 m²) con 5 islas y mural frigorífico Este, Núcleo de Baños (Damas/Caballeros + Antebaño) en el
   rincón Suroeste ciego bajo Lavandería P2, Barra de Jugos/Fruta Picada con ventanal Sur y Oficina
   Acristalada de Administración en Sureste + Portón Derecho Av. 4 y Esclusa de Escaleras.
3. SEGUNDO PISO (Z = +3,00 m): Despensa Walk-In integrada bajo el tramo alto de la escalera a Piso 3
   (liberando un hall limpio de 3,10 m), Nevera French Door + Torre de Hornos en el remate Norte del
   mesón Oeste, Cocina con Isla, Comedor 10p, Sala, Estudio acristalado, Hab. 4 Huéspedes y Lavandería.
4. NUEVO TERCER PISO (Z = +6,00 m): Columnas metálicas negras vistas, Master Penthouse Suite con
   accesos visibles en 3D y 2D al Gran Vestier (Barn Door 1,30 m) y al Baño Spa (puerta interna a 45°),
   Habitaciones 2 y 3 al Este, Gran Terraza Mirador & BBQ unificada en esquina Sureste (26,88 m², sin
   Hab. 4), Buhardilla de Tanques (2.000 L) con baranda en "L" que deja libre el desembarque Este, y
   Cubierta Chalet con perforación real (3,10 x 5,80 m) bajo la Claraboya Ventilada para luz y aire.
   CERO invasión al vecino izquierdo (minX >= 0,15 m en todos los niveles y cubiertas).
"""

import math
import os


def build_casa_3_pisos():
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

    def add_rect_2d(layer, color, x1, y1, x2, y2, z=0.0):
        add_line(layer, color, x1, y1, z, x2, y1, z)
        add_line(layer, color, x2, y1, z, x2, y2, z)
        add_line(layer, color, x2, y2, z, x1, y2, z)
        add_line(layer, color, x1, y2, z, x1, y1, z)

    def add_text(layer, color, text, x, y, z, h=0.25):
        texts.append((layer, color, text, x, y, z, h))

    # =========================================================================
    # PARÁMETROS VERTICALES Y GEOMÉTRICOS CENTRALES (4 NIVELES + BUHARDILLA)
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso acabado Sótano Bodega y Patio Maniobra
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa entrepiso Planta Baja
    Z_P1_FLOOR     =  0.00   # Nivel piso acabado Planta Baja (Comercio + Garaje)
    H_P1           =  2.85   # Tope muros Planta Baja / Fondo losa Segundo Piso
    Z_P2_FLOOR     =  3.00   # Nivel piso acabado Segundo Piso (Planta Social Día)
    H_P2           =  5.85   # Tope muros Segundo Piso / Fondo losa Steel Deck P3
    Z_P3_FLOOR     =  6.00   # Nivel piso acabado Nuevo Tercer Piso (Planta Privada)
    H_P3           =  8.85   # Nivel solera muros Tercer Piso
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.05

    # Parámetros de Cubierta Chalet Alpino sobre Piso 3 con Respeto de Colindancia Izquierda
    X_RIDGE        =  4.85   # Eje de cumbrera longitudinal Norte-Sur (m)
    SLOPE_TAN      =  math.tan(math.radians(32.0))  # Pendiente alpina 32° (~62.5%)
    X_GUTTER_IN    =  0.45   # Arranque faldón oeste dentro del canalón oculto propio (X >= 0.15 m!)
    Z_GUTTER_EAVE  =  8.95   # Cota inferior faldón oeste en canalón oculto P3
    Z_RIDGE        =  Z_GUTTER_EAVE + (X_RIDGE - X_GUTTER_IN) * SLOPE_TAN  # ~11.70 m
    ROOF_THICK     =  0.18   # Espesor tablero + aislamiento + teja pizarra
    ALERO_ESTE     =  0.95   # Voladizo hacia retiro lateral derecho propio (X = 9.15 -> 10.10 < 10.80 m)
    ALERO_SUR      =  1.00   # Voladizo hacia patio trasero propio (Y_casa = 0.00 -> -1.00 m)
    X_EAVE_EAST    =  9.15 + ALERO_ESTE  # 10.10 m (100% dentro de la parcela)
    Z_EAVE_EAST    =  Z_RIDGE - (X_EAVE_EAST - X_RIDGE) * SLOPE_TAN  # ~8.42 m
    Z_PARAPET_WEST =  9.28   # Tope parapeto cortafuegos izquierdo propio en P3 (X = 0.15..0.30 m)
    Z_PARAPET_BUH  = 10.85   # Tope parapeto cortafuegos en tramo Buhardilla P3 (Y = 0.00..4.45 m)

    def z_roof_under(x):
        if x <= X_RIDGE:
            return Z_GUTTER_EAVE + (x - X_GUTTER_IN) * SLOPE_TAN
        return Z_RIDGE - (x - X_RIDGE) * SLOPE_TAN

    # Implantación dentro de la parcela poligonal UTM (24.71 m de largo)
    OFFSET_X = 0.00   # X = 0.00..0.15 pared del vecino INTOCABLE; X = 0.15..0.30 muro propio
    OFFSET_Y = 3.00   # Retiro de fondo de 3.00 m (Patio Trasero a cota Z = -2.55 m)
    Y_AV4    = 21.71  # Lindero frontal Avenida 4 (Y_terreno = 24.71 m)

    # Parámetros Estacionamiento (3,00 m libres reales)
    X_GAR_LEFT_IN  = 0.30
    X_GAR_RIGHT_IN = 3.30
    X_GAR_WALL_OUT = 3.45

    def add_house_box(layer, color, x1, y1, z1, x2, y2, z2):
        add_box(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_hexa(layer, color, pts8):
        shifted = [(OFFSET_X + px, OFFSET_Y + py, pz) for (px, py, pz) in pts8]
        add_hexahedron(layer, color, shifted)

    def add_house_line(layer, color, x1, y1, z1, x2, y2, z2):
        add_line(layer, color, OFFSET_X + x1, OFFSET_Y + y1, z1, OFFSET_X + x2, OFFSET_Y + y2, z2)

    def add_house_text(layer, color, text, x, y, z, h=0.20):
        add_text(layer, color, text, OFFSET_X + x, OFFSET_Y + y, z, h)

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

    L_CARP = "CARPINTERIA_RUSTICA_3D"
    L_BALC = "BALCONES_BARANDAS_3D"

    def add_rustic_window_east(y1, y2, z1, z2, with_shutters=True, frame_color=34):
        t_f = 0.06
        add_house_box(L_CARP, frame_color, 8.98, y1, z1, 9.17, y2, z1 + t_f)
        add_house_box(L_CARP, frame_color, 8.98, y1, z2 - t_f, 9.17, y2, z2)
        add_house_box(L_CARP, frame_color, 8.98, y1, z1 + t_f, 9.17, y1 + t_f, z2 - t_f)
        add_house_box(L_CARP, frame_color, 8.98, y2 - t_f, z1 + t_f, 9.17, y2, z2 - t_f)
        ym = 0.5 * (y1 + y2)
        zm = 0.5 * (z1 + z2)
        add_house_box(L_CARP, frame_color, 9.05, ym - 0.02, z1 + t_f, 9.10, ym + 0.02, z2 - t_f)
        add_house_box(L_CARP, frame_color, 9.05, y1 + t_f, zm - 0.02, 9.10, y2 - t_f, zm + 0.02)
        add_house_box(L_CARP, 4, 9.07, y1 + t_f, z1 + t_f, 9.08, y2 - t_f, z2 - t_f)
        if with_shutters and (y2 - y1) >= 1.20:
            sh_w = min(0.38, 0.35 * (y2 - y1))
            if y1 - sh_w > 0.25:
                add_house_box(L_CARP, frame_color, 9.15, y1 - sh_w, z1, 9.20, y1 - 0.02, z2)
            if y2 + sh_w < Y_AV4 - 0.25:
                add_house_box(L_CARP, frame_color, 9.15, y2 + 0.02, z1, 9.20, y2 + sh_w, z2)

    def add_rustic_window_south(x1, x2, z1, z2, with_shutters=True, frame_color=34):
        t_f = 0.06
        add_house_box(L_CARP, frame_color, x1, -0.02, z1, x2, 0.17, z1 + t_f)
        add_house_box(L_CARP, frame_color, x1, -0.02, z2 - t_f, x2, 0.17, z2)
        add_house_box(L_CARP, frame_color, x1, -0.02, z1 + t_f, x1 + t_f, 0.17, z2 - t_f)
        add_house_box(L_CARP, frame_color, x2 - t_f, -0.02, z1 + t_f, x2, 0.17, z2 - t_f)
        xm = 0.5 * (x1 + x2)
        zm = 0.5 * (z1 + z2)
        add_house_box(L_CARP, frame_color, xm - 0.02, 0.05, z1 + t_f, xm + 0.02, 0.10, z2 - t_f)
        add_house_box(L_CARP, frame_color, x1 + t_f, 0.05, zm - 0.02, x2 - t_f, 0.10, zm + 0.02)
        add_house_box(L_CARP, 4, x1 + t_f, 0.07, z1 + t_f, x2 - t_f, 0.08, z2 - t_f)
        if with_shutters and (x2 - x1) >= 1.20:
            sh_w = 0.36
            if x1 - sh_w >= 0.25:
                add_house_box(L_CARP, frame_color, x1 - sh_w, -0.05, z1, x1 - 0.02, 0.00, z2)
            if x2 + sh_w <= 8.95:
                add_house_box(L_CARP, frame_color, x2 + 0.02, -0.05, z1, x2 + sh_w, 0.00, z2)

    def add_alpine_railing_x(x1, x2, y_center, z_floor, h_rail=1.05, n_bays=4, layer=L_BALC, col=30):
        half_t = 0.06
        add_house_box(layer, col, x1, y_center - half_t, z_floor + 0.05, x2, y_center + half_t, z_floor + 0.13)
        add_house_box(layer, col, x1, y_center - 0.08, z_floor + h_rail - 0.08, x2, y_center + 0.08, z_floor + h_rail)
        dx = (x2 - x1) / n_bays
        for b in range(n_bays + 1):
            px = x1 + b * dx
            add_house_box(layer, col, max(x1, px - 0.06), y_center - 0.07, z_floor,
                                      min(x2, px + 0.06), y_center + 0.07, z_floor + h_rail)
        for b in range(n_bays):
            bx1 = x1 + b * dx + 0.06
            bx2 = x1 + (b + 1) * dx - 0.06
            bz1 = z_floor + 0.13
            bz2 = z_floor + h_rail - 0.08
            t_d = 0.05
            add_house_hexa(layer, col, [
                (bx1, y_center - 0.03, bz1), (bx1 + t_d, y_center - 0.03, bz1),
                (bx1 + t_d, y_center + 0.03, bz1), (bx1, y_center + 0.03, bz1),
                (bx2 - t_d, y_center - 0.03, bz2), (bx2, y_center - 0.03, bz2),
                (bx2, y_center + 0.03, bz2), (bx2 - t_d, y_center + 0.03, bz2),
            ])
            add_house_hexa(layer, col, [
                (bx2 - t_d, y_center - 0.03, bz1), (bx2, y_center - 0.03, bz1),
                (bx2, y_center + 0.03, bz1), (bx2 - t_d, y_center + 0.03, bz1),
                (bx1, y_center - 0.03, bz2), (bx1 + t_d, y_center - 0.03, bz2),
                (bx1 + t_d, y_center + 0.03, bz2), (bx1, y_center + 0.03, bz2),
            ])

    def add_alpine_railing_y(x_center, y1, y2, z_floor, h_rail=1.05, n_bays=2, layer=L_BALC, col=30):
        half_t = 0.06
        add_house_box(layer, col, x_center - half_t, y1, z_floor + 0.05, x_center + half_t, y2, z_floor + 0.13)
        add_house_box(layer, col, x_center - 0.08, y1, z_floor + h_rail - 0.08, x_center + 0.08, y2, z_floor + h_rail)
        dy = (y2 - y1) / n_bays
        for b in range(n_bays + 1):
            py = y1 + b * dy
            add_house_box(layer, col, x_center - 0.07, max(y1, py - 0.06), z_floor,
                                      x_center + 0.07, min(y2, py + 0.06), z_floor + h_rail)
        for b in range(n_bays):
            by1 = y1 + b * dy + 0.06
            by2 = y1 + (b + 1) * dy - 0.06
            bz1 = z_floor + 0.13
            bz2 = z_floor + h_rail - 0.08
            t_d = 0.05
            add_house_hexa(layer, col, [
                (x_center - 0.03, by1, bz1), (x_center + 0.03, by1, bz1),
                (x_center + 0.03, by1 + t_d, bz1), (x_center - 0.03, by1 + t_d, bz1),
                (x_center - 0.03, by2 - t_d, bz2), (x_center + 0.03, by2 - t_d, bz2),
                (x_center + 0.03, by2, bz2), (x_center - 0.03, by2, bz2),
            ])
            add_house_hexa(layer, col, [
                (x_center - 0.03, by2 - t_d, bz1), (x_center + 0.03, by2 - t_d, bz1),
                (x_center + 0.03, by2, bz1), (x_center - 0.03, by2, bz1),
                (x_center - 0.03, by1, bz2), (x_center + 0.03, by1, bz2),
                (x_center + 0.03, by1 + t_d, bz2), (x_center - 0.03, by1 + t_d, bz2),
            ])

    # =========================================================================
    # 1. NIVEL SÓTANO (Z = -2.55 a -0.15 m): GRAN BODEGA MAYORISTA COMERCIAL
    #    (Reemplaza Taberna; Acceso Comercial Exclusivo por Puerta Derecha Av.4)
    # =========================================================================
    L_SOT_SLAB   = "SOTANO_LOSA_3D"
    L_SOT_EXT    = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT    = "SOTANO_MUROS_INT_3D"
    L_SOT_COL    = "SOTANO_COLUMNAS_3D"
    L_SOT_BODEGA = "SOTANO_BODEGA_EQUIP_3D"

    # Losa Sótano 100% rectangular (X: 0.15 a 9.15 m, Y: 0.00 a 8.30 m) + Patio de Maniobra Sur
    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)
    add_house_box(L_SOT_SLAB, 8, 4.50, -2.50, Z_SOT_FLOOR - 0.10, 9.15, 0.00, Z_SOT_FLOOR + 0.01)

    # Escalera Interior Tramo 1 INTACTA (X: 0.30..1.40, Y: 7.40 -> 4.45)
    num_steps = 12
    step_dy = (7.40 - 4.45) / num_steps
    step_dz = (0.00 - Z_SOT_FLOOR) / num_steps
    for i in range(num_steps):
        y_s_top = 7.40 - i * step_dy
        y_s_bot = y_s_top - step_dy
        z_s_top = 0.00 - i * step_dz
        z_s_bot = max(Z_SOT_FLOOR, z_s_top - 0.55) if i < 6 else Z_SOT_FLOOR
        add_house_box("ESCALERA_3D", 7, 0.30, y_s_bot, z_s_bot, 1.40, y_s_top, z_s_top)
        add_house_line("ESCALERA_2D", 7, 0.30, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muro Oeste Propio en Sótano (X: 0.15..0.30, Y: 0.00..8.30) — Ciego junto a vecino
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)

    # Muro Norte de Contención del Sótano (Y: 8.15..8.30, X: 0.30..9.15)
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur hacia Patio de Maniobra (Y: 0.00..0.15) con Ventanas Altas Seguras + Portón Doble de Carga (2,20x2,10m)
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 9.15, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.75, 2.35, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),  # Ventana Alta Basculante Oeste con Reja
        (3.25, 4.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.20),  # Celosía Alta Baño Operativo
        (4.85, 5.75, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),  # Ventana Alta Basculante Centro
        (6.35, 8.55, Z_SOT_FLOOR,        Z_SOT_FLOOR + 2.10),  # PORTÓN DOBLE METÁLICO DE CARGA BODEGA (2,20 x 2,10 m)
    ])
    for wx1, wx2, wz1, wz2 in [(0.75, 2.35, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
                               (3.25, 4.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.20),
                               (4.85, 5.75, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20)]:
        add_rustic_window_south(wx1, wx2, wz1, wz2, with_shutters=False, frame_color=8)
    # Marco y Hojas Metálicas Reforzadas del Portón Doble de Carga (abiertas 90° hacia patio de maniobra)
    add_house_box(L_CARP, 8, 6.29, -0.04, Z_SOT_FLOOR, 6.36, 0.18, Z_SOT_FLOOR + 2.16)
    add_house_box(L_CARP, 8, 8.54, -0.04, Z_SOT_FLOOR, 8.61, 0.18, Z_SOT_FLOOR + 2.16)
    add_house_box(L_CARP, 8, 6.27, -0.05, Z_SOT_FLOOR + 2.10, 8.63, 0.18, Z_SOT_FLOOR + 2.18)
    add_house_box(L_CARP, 8, 6.32, -1.08, Z_SOT_FLOOR + 0.02, 6.39, -0.02, Z_SOT_FLOOR + 2.08)
    add_house_box(L_CARP, 8, 8.51, -1.08, Z_SOT_FLOOR + 0.02, 8.58, -0.02, Z_SOT_FLOOR + 2.08)

    # Muro Este sobre Eje 3 (X: 8.95..9.15, Y: 0.15..8.30) con 3 Ventanas Altas de Ventilación Segura (antepecho 1,65 m)
    add_wall_with_openings_y(L_SOT_EXT, 4, 8.95, 9.15, 0.15, 8.30, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.00, 2.65, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        (4.20, 5.85, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        (6.95, 8.00, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
    ])
    for wy1, wy2 in [(1.00, 2.65), (4.20, 5.85), (6.95, 8.00)]:
        add_rustic_window_east(wy1, wy2, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20, with_shutters=False, frame_color=8)

    # Columnas Estructurales del Sótano (35 x 35 cm, 100% CONSERVADAS)
    add_house_box(L_SOT_COL, 1, 0.15, 6.35, Z_SOT_FLOOR, 0.30, 6.80, Z_P1_SLAB_BOT)
    sot_cols_axes = [
        (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
        (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
        (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)

    # --- PARTICIONES, ESCLUSA DE ESCALERA Y CIRCULACIÓN AMPLIA EN BODEGA SÓTANO ---
    # 1. Caja Cerrada de Escalera con Puerta Metálica de Seguridad inferior (abre hacia pasillo libre de 1,95 m!)
    add_wall_with_openings_y(L_SOT_INT, 4, 1.40, 1.55, 3.55, 8.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (3.70, 4.55, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),   # Puerta inferior amplia (0,85m) hacia pasillo libre
        (7.20, 7.95, Z_SOT_FLOOR, Z_SOT_FLOOR + 1.90),         # Cuarto útiles bajo escalera
    ])
    add_house_box(L_SOT_INT, 4, 0.30, 3.40, Z_SOT_FLOOR, 1.55, 3.55, Z_P1_SLAB_BOT)  # Cierre Sur esclusa escalera
    # Marco metálico y hoja entreabierta a 45° hacia el gran pasillo central despejado (sin obstáculo enfrente)
    add_house_box(L_CARP, 8, 1.38, 3.66, Z_SOT_FLOOR, 1.57, 3.71, Z_SOT_FLOOR + H_DOOR_SOT)
    add_house_box(L_CARP, 8, 1.38, 4.54, Z_SOT_FLOOR, 1.57, 4.59, Z_SOT_FLOOR + H_DOOR_SOT)
    add_house_box(L_CARP, 8, 1.38, 3.66, Z_SOT_FLOOR + H_DOOR_SOT, 1.57, 4.59, Z_SOT_FLOOR + H_DOOR_SOT + 0.06)
    add_house_hexa(L_CARP, 8, [
        (1.55, 4.52, Z_SOT_FLOOR + 0.02), (1.60, 4.56, Z_SOT_FLOOR + 0.02),
        (2.15, 3.96, Z_SOT_FLOOR + 0.02), (2.10, 3.92, Z_SOT_FLOOR + 0.02),
        (1.55, 4.52, Z_SOT_FLOOR + H_DOOR_SOT - 0.02), (1.60, 4.56, Z_SOT_FLOOR + H_DOOR_SOT - 0.02),
        (2.15, 3.96, Z_SOT_FLOOR + H_DOOR_SOT - 0.02), (2.10, 3.92, Z_SOT_FLOOR + H_DOOR_SOT - 0.02),
    ])

    # 2. Baño Operativo Compacto de Personal + Lava-mopas (X: 2.80..4.70, Y: 0.15..2.70)
    add_house_box(L_SOT_INT, 4, 2.80, 0.15, Z_SOT_FLOOR, 2.95, 2.55, Z_P1_SLAB_BOT)
    add_house_box(L_SOT_INT, 4, 4.55, 0.15, Z_SOT_FLOOR, 4.70, 2.55, Z_P1_SLAB_BOT)
    add_wall_with_openings_x(L_SOT_INT, 4, 2.80, 4.70, 2.55, 2.70, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (3.40, 4.18, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    add_house_box(L_CARP, 34, 4.12, 1.85, Z_SOT_FLOOR + 0.02, 4.17, 2.55, Z_SOT_FLOOR + H_DOOR_SOT - 0.02)
    add_house_box(L_SOT_BODEGA, 7, 3.02, 0.25, Z_SOT_FLOOR, 3.62, 0.68, Z_SOT_FLOOR + 0.42)  # WC personal
    add_house_box(L_SOT_BODEGA, 7, 3.02, 0.25, Z_SOT_FLOOR + 0.42, 3.22, 0.68, Z_SOT_FLOOR + 0.80)
    add_house_box(L_SOT_BODEGA, 7, 3.02, 1.25, Z_SOT_FLOOR + 0.50, 3.45, 1.85, Z_SOT_FLOOR + 0.85)  # Lavamanos
    add_house_box(L_SOT_BODEGA, 8, 3.95, 0.25, Z_SOT_FLOOR, 4.50, 0.85, Z_SOT_FLOOR + 0.45)  # Poceta aseo/lava-mopas

    # --- EQUIPAMIENTO PERIMETRAL ORDENADO DE LA BODEGA (CRUZ DE CIRCULACIÓN DE 1,95m A 2,25m LIBRES!) ---
    # A. Cámara Isotérmica de Pre-Frío y Maduración Mayorista (Noroeste: X: 1.60..5.55, Y: 5.55..8.10 = 10,1 m²)
    add_house_box(L_SOT_BODEGA, 5, 1.60, 5.55, Z_SOT_FLOOR, 5.55, 5.67, Z_SOT_FLOOR + 2.30)  # Panel frontal isotérmico
    add_house_box(L_SOT_BODEGA, 5, 5.43, 5.55, Z_SOT_FLOOR, 5.55, 8.10, Z_SOT_FLOOR + 2.30)  # Panel lateral este
    add_house_box(L_SOT_BODEGA, 5, 1.60, 5.55, Z_SOT_FLOOR + 2.22, 5.55, 8.10, Z_SOT_FLOOR + 2.32)  # Techo cámara
    add_house_box(L_SOT_BODEGA, 7, 3.10, 5.48, Z_SOT_FLOOR + 0.03, 4.25, 5.56, Z_SOT_FLOOR + 2.08)  # Puerta corrediza inox
    add_house_box(L_SOT_BODEGA, 3, 4.38, 5.50, Z_SOT_FLOOR + 1.45, 4.62, 5.55, Z_SOT_FLOOR + 1.72)  # Control digital frío
    for rz_c in [0.35, 0.95, 1.55]:
        add_house_box(L_SOT_BODEGA, 30, 1.70, 7.45, Z_SOT_FLOOR + rz_c, 5.35, 8.02, Z_SOT_FLOOR + rz_c + 0.35)

    # B. Baterías de Racks Industriales Perimetrales (Deja libre Pasillo Central Y=3.55..5.50 y Avenida Carga X=6.00..8.25)
    def add_heavy_rack(rx1, ry1, rx2, ry2, crate_col=30, max_h=2.20):
        levels = [0.18, 0.78, 1.38, 1.95] if max_h > 1.80 else [0.18, 0.72, 1.26]
        for px in [rx1 + 0.04, rx2 - 0.04]:
            for py in [ry1 + 0.04, ry2 - 0.04]:
                add_house_box(L_SOT_BODEGA, 8, px - 0.04, py - 0.04, Z_SOT_FLOOR, px + 0.04, py + 0.04, Z_SOT_FLOOR + max_h)
        for rz in levels:
            add_house_box(L_SOT_BODEGA, 34, rx1, ry1, Z_SOT_FLOOR + rz, rx2, ry2, Z_SOT_FLOOR + rz + 0.06)
            if rz + 0.34 <= max_h:
                add_house_box(L_SOT_BODEGA, crate_col, rx1 + 0.08, ry1 + 0.08, Z_SOT_FLOOR + rz + 0.06,
                              rx2 - 0.08, ry2 - 0.08, Z_SOT_FLOOR + rz + 0.34)

    # Rack Norte 1 (Fondo Noreste): X = 5.85..8.85, Y = 7.35..8.05
    add_heavy_rack(5.85, 7.35, 8.85, 8.05, crate_col=30, max_h=2.20)
    # Rack Mural Este 1 y 2 (Bajo ventanas altas de 1,65m; deja libre Avenida Principal X = 6.00..8.25!)
    add_heavy_rack(8.25, 4.05, 8.90, 6.80, crate_col=3,  max_h=1.58)
    add_heavy_rack(8.25, 0.85, 8.90, 3.35, crate_col=2,  max_h=1.58)
    # Racks Perimetrales Suroeste (Con pasillo amplio de 1,50m libres para caminar sin tropiezos)
    add_heavy_rack(0.35, 0.22, 2.65, 0.88, crate_col=30, max_h=1.58)
    add_heavy_rack(0.35, 1.05, 1.00, 3.25, crate_col=3,  max_h=2.20)

    # C. Estiba Suroeste adosada + Báscula Plataforma 500 kg y Mesa de Guías adosadas al Baño (SIN atravesarse al portón!)
    add_house_box(L_SOT_BODEGA, 34, 1.95, 1.15, Z_SOT_FLOOR, 2.72, 1.95, Z_SOT_FLOOR + 0.14)  # Pallet adosado al baño
    add_house_box(L_SOT_BODEGA, 30, 2.02, 1.22, Z_SOT_FLOOR + 0.14, 2.66, 1.88, Z_SOT_FLOOR + 0.82)
    # Báscula Industrial de Plataforma a ras de piso al costado de la Avenida de Carga (X: 4.80..5.70, Y: 0.35..1.25)
    add_house_box(L_SOT_BODEGA, 8, 4.80, 0.35, Z_SOT_FLOOR, 5.70, 1.25, Z_SOT_FLOOR + 0.08)
    add_house_box(L_SOT_BODEGA, 7, 4.82, 1.15, Z_SOT_FLOOR + 0.08, 4.90, 1.23, Z_SOT_FLOOR + 1.25)  # Columna visor
    add_house_box(L_SOT_BODEGA, 3, 4.78, 1.10, Z_SOT_FLOOR + 1.10, 4.98, 1.25, Z_SOT_FLOOR + 1.30)  # Indicador digital
    # Escritorio / Mesa de Recepción y Control de Guías adosado al muro Este del baño (X: 4.75..5.70, Y: 1.45..2.50)
    add_house_box(L_SOT_BODEGA, 34, 4.75, 1.45, Z_SOT_FLOOR, 5.70, 2.50, Z_SOT_FLOOR + 0.78)
    add_house_box(L_SOT_BODEGA, 8,  5.00, 2.58, Z_SOT_FLOOR, 5.48, 3.02, Z_SOT_FLOOR + 0.48)  # Silla operador

    # =========================================================================
    # 2. NIVEL PLANTA BAJA (Z = 0.00 a +2.85 m):
    #    FRUTERÍA + GARAJE 3,00m + VESTÍBULO CON PUERTA A ESCALERA + PUERTA DER. AV.4
    # =========================================================================
    L_P1_SLAB   = "LOSA_PISO_3D"
    L_P1_EXT    = "MUROS_EXTERIORES_3D"
    L_P1_INT    = "MUROS_INTERIORES_3D"
    L_P1_COL    = "COLUMNAS_3D"
    L_ZOCALO    = "PB_ZOCALO_PIEDRA_3D"
    L_PB_TIMBER   = "PB_TIMBER_FRAME_3D"
    L_PB_COM_FURN = "PB_MOBILIARIO_COMERCIAL_3D"
    L_PB_GAR_FURN = "PB_MOBILIARIO_GARAJE_3D"
    L_PB_ADM_FURN = "PB_MOBILIARIO_OFICINA_3D"

    # Losa Planta Baja 100% rectangular (9.00 x 21.71 m) respetando caja de escalera al sótano
    add_house_box(L_P1_SLAB, 8, 0.15, 0.00, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR)

    # 1. Muro Lateral Izquierdo PROPIO (X: 0.15..0.30, Y: 0.00..21.71 m) — CERO invasión a X < 0.15
    add_house_box(L_P1_EXT, 7, 0.15, 0.00, Z_P1_FLOOR, X_GAR_LEFT_IN, Y_AV4, H_P1)

    # 2. Fachada Frontal sobre Avenida 4 (Portón Garaje + 2 Santamarías Frutería)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P1_FLOOR, H_P1, [
        (0.40, 2.70, 0.00, 2.40),
        (3.65, 5.75, 0.00, 2.40),
        (6.20, 8.80, 0.00, 2.40),
    ])
    for px1, px2 in [(0.15, 0.40), (2.70, 3.65), (5.75, 6.20), (8.80, 9.15)]:
        add_house_box(L_ZOCALO, 8, px1, Y_AV4 - 0.22, Z_P1_FLOOR, px2, Y_AV4, H_P1)

    # 2B. NUEVO PORTÓN / PUERTA DE ACCESO EXCLUSIVO A LA DERECHA DE LA AVENIDA 4 (X = 9.15..11.37 m)
    #     Única entrada exterior hacia la Rampa Logística de la Bodega del Sótano:
    add_box(L_P1_EXT, 7, 9.15, OFFSET_Y + Y_AV4 - 0.18, 0.00, 9.35, OFFSET_Y + Y_AV4 + 0.02, 2.65)   # Machón izq.
    add_box(L_P1_EXT, 7, 11.12, OFFSET_Y + Y_AV4 - 0.18, 0.00, 11.37, OFFSET_Y + Y_AV4 + 0.02, 2.65) # Machón der. P-2
    add_box(L_P1_EXT, 7, 9.15, OFFSET_Y + Y_AV4 - 0.20, 2.35, 11.37, OFFSET_Y + Y_AV4 + 0.04, 2.68)  # Dintel pórtico bodega
    add_box(L_PB_TIMBER, 30, 9.12, OFFSET_Y + Y_AV4 - 0.26, 2.68, 11.37, OFFSET_Y + Y_AV4 + 0.08, 2.84) # Tejadillo rústico
    # Puerta metálica comercial derecha (X = 9.35..11.12 m, ancho libre 1,77 m para carga, hojas de forja negra)
    add_box(L_CARP, 8, 9.35, OFFSET_Y + Y_AV4 - 0.12, 0.02, 10.22, OFFSET_Y + Y_AV4 - 0.04, 2.34)
    add_box(L_CARP, 8, 10.25, OFFSET_Y + Y_AV4 - 0.12, 0.02, 11.12, OFFSET_Y + Y_AV4 - 0.04, 2.34)

    # 3. Muro Lateral Derecho continuo sobre Eje 3 (X: 9.00..9.15)
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 0.00, Y_AV4, Z_P1_FLOOR, H_P1, [
        (1.10,  2.50, 1.00, 2.10),
        (4.10,  5.00, 1.10, 2.00),
        (6.30,  8.00, 1.00, 2.10),
        (9.65, 11.85, 1.00, 2.10),
        (13.15, 14.05, 1.10, 2.00),
        (15.50, 17.70, 1.00, 2.10),
        (18.80, 21.00, 1.00, 2.10),
    ])
    add_house_box(L_ZOCALO, 8, 9.15, 0.00, Z_P1_FLOOR, 9.21, Y_AV4, 0.95)

    # 4. Muro Sur Posterior completo de Planta Baja (Y: 0.00..0.15, X: 0.15..9.15):
    #    Ventana alta privacidad Baños Suroeste + Gran Ventanal Barra Jugos (luz y brisa N-S) + Ventana Oficina
    south_windows_pb = [
        (0.75, 2.35, 1.55, 2.25),   # Ventana alta ventilación Núcleo de Baños Suroeste
        (3.35, 5.45, 0.90, 2.25),   # Gran Ventanal Panorámico Barra de Jugos / Fruta Picada
        (6.85, 8.45, 0.95, 2.20),   # Ventanal Sur Oficina Acristalada Administración
    ]
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, 0.00, 0.15, Z_P1_FLOOR, H_P1, south_windows_pb)
    for wx1, wx2, wz1, wz2 in south_windows_pb:
        add_rustic_window_south(wx1, wx2, wz1, wz2, with_shutters=(wx2 - wx1 >= 1.40))

    # --- MUROS INTERIORES PLANTA BAJA + REDISTRIBUCIÓN DEL FONDO COMERCIAL (SIN BODEGA PB!) ---
    # Muro longitudinal Oeste que separa Escaleras / Cuarto Aseo / Baños Suroeste del Salón Comercial (X = 2.75..2.90)
    add_wall_with_openings_y(L_P1_INT, 7, 2.75, 2.90, 0.15, 8.80, Z_P1_FLOOR, H_P1, [
        (2.35, 3.20, Z_P1_FLOOR, Z_P1_FLOOR + H_DOOR),   # Entrada discreta al Antebaño de Clientes / Personal
        (3.75, 4.45, Z_P1_FLOOR, Z_P1_FLOOR + 1.95),     # Puerta Cuarto de Aseo Diario bajo tramo alto escalera P2
    ])
    # Marcos y hojas entreabiertas de las puertas del costado Suroeste
    add_house_box(L_CARP, 34, 2.20, 3.14, Z_P1_FLOOR + 0.02, 2.75, 3.20, Z_P1_FLOOR + H_DOOR - 0.02)
    add_house_box(L_CARP, 34, 2.25, 4.39, Z_P1_FLOOR + 0.02, 2.75, 4.45, Z_P1_FLOOR + 1.93)

    add_house_box(L_P1_INT, 7, X_GAR_RIGHT_IN, 8.80, Z_P1_FLOOR, X_GAR_WALL_OUT, Y_AV4 - 0.15, H_P1)
    add_house_box(L_P1_INT, 7, 2.75, 8.80, Z_P1_FLOOR, X_GAR_WALL_OUT, 8.95, H_P1)

    # CIERRE DEL VESTÍBULO DE ESCALERAS EN Y = 8.80..8.95 (X = 0.30..2.75):
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 8.80, 8.95, Z_P1_FLOOR, H_P1, [
        (1.60, 2.55, Z_P1_FLOOR, Z_P1_FLOOR + H_DOOR),  # Puerta Residencial Acceso Estacionamiento <-> Escalera P2
    ])
    add_house_box(L_CARP, 34, 1.56, 8.78, Z_P1_FLOOR, 1.62, 8.97, Z_P1_FLOOR + H_DOOR)
    add_house_box(L_CARP, 34, 2.53, 8.78, Z_P1_FLOOR, 2.59, 8.97, Z_P1_FLOOR + H_DOOR)
    add_house_box(L_CARP, 30, 2.48, 7.92, Z_P1_FLOOR + 0.02, 2.54, 8.80, Z_P1_FLOOR + H_DOOR)

    # Cierre y Puerta de Seguridad Superior en Arranque de Escalera a Bodega (X = 0.30..1.55, Y = 7.35..7.50)
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.50, H_P1)  # Muro completo entre ambas escaleras
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 1.55, 7.35, 7.50, Z_P1_FLOOR, H_P1, [
        (0.40, 1.32, Z_P1_FLOOR, Z_P1_FLOOR + H_DOOR),  # Puerta Metálica con Cerradura hacia Bodega Sótano
    ])
    add_house_box(L_CARP, 8, 0.40, 7.38, Z_P1_FLOOR + 0.02, 1.32, 7.45, Z_P1_FLOOR + H_DOOR)
    add_house_box(L_P1_INT, 7, 0.30, 4.25, Z_P1_FLOOR, 1.40, 4.40, H_P1)
    # Cierre norte del Cuarto de Aseo Diario bajo el tramo alto de la escalera a P2 (Y = 5.65..5.78, H = 1,62 m)
    add_house_box(L_P1_INT, 7, 1.55, 5.65, Z_P1_FLOOR, 2.75, 5.78, 1.62)

    # --- 1. NUEVO NÚCLEO DE BAÑOS COMERCIALES EN ESQUINA SUROESTE CIEGA (X = 0.30..2.75, Y = 0.15..3.50 = 8,20 m²) ---
    # Coincide verticalmente bajo la Lavandería de Piso 2 y libera por completo la fachada Este del local!
    add_house_box(L_P1_INT, 7, 0.30, 3.50, Z_P1_FLOOR, 2.75, 3.62, H_P1)  # Separa Baños del Cuarto de Aseo
    # Tabique interno Cabina Damas / Accesible (X = 0.30..1.48) vs Antebaño y Caballeros (X = 1.58..2.75)
    add_wall_with_openings_y(L_P1_INT, 7, 1.48, 1.58, 0.15, 3.50, Z_P1_FLOOR, H_P1, [
        (2.15, 2.95, Z_P1_FLOOR, Z_P1_FLOOR + H_DOOR),   # Puerta Cabina Damas (PMR)
    ])
    add_house_box(L_CARP, 34, 0.92, 2.90, Z_P1_FLOOR + 0.02, 1.48, 2.95, Z_P1_FLOOR + H_DOOR - 0.02)
    # Tabique interno Cabina Caballeros (Y = 1.72..1.82, X = 1.58..2.75)
    add_wall_with_openings_x(L_P1_INT, 7, 1.58, 2.75, 1.72, 1.82, Z_P1_FLOOR, H_P1, [
        (1.75, 2.48, Z_P1_FLOOR, Z_P1_FLOOR + H_DOOR),   # Puerta Cabina Caballeros
    ])
    add_house_box(L_CARP, 34, 2.43, 1.10, Z_P1_FLOOR + 0.02, 2.48, 1.72, Z_P1_FLOOR + H_DOOR - 0.02)
    # Aparatos sanitarios: Doble lavamanos en Antebaño + WC Damas + WC y Urinario Caballeros
    add_house_box(L_PB_ADM_FURN, 34, 1.62, 3.02, Z_P1_FLOOR, 2.68, 3.48, 0.85)       # Tocador doble en Antebaño
    add_house_box(L_PB_ADM_FURN, 7,  1.72, 3.10, 0.85, 2.08, 3.40, 0.92)             # Lavamanos 1
    add_house_box(L_PB_ADM_FURN, 7,  2.22, 3.10, 0.85, 2.58, 3.40, 0.92)             # Lavamanos 2
    add_house_box(L_PB_ADM_FURN, 7,  0.42, 0.25, Z_P1_FLOOR, 0.95, 0.78, 0.42)       # WC Damas / PMR
    add_house_box(L_PB_ADM_FURN, 7,  0.42, 0.25, 0.42, 0.62, 0.78, 0.80)
    add_house_box(L_PB_ADM_FURN, 7,  1.78, 0.25, Z_P1_FLOOR, 2.25, 0.75, 0.42)       # WC Caballeros
    add_house_box(L_PB_ADM_FURN, 7,  1.78, 0.25, 0.42, 2.25, 0.45, 0.80)
    add_house_box(L_PB_ADM_FURN, 7,  2.42, 0.95, 0.45, 2.70, 1.35, 1.05)             # Urinario

    # --- 2. OFICINA ACRISTALADA DE ADMINISTRACIÓN Y CAJA MAYORISTA (Sureste: X = 5.88..9.00, Y = 0.15..3.55 = 10,05 m²) ---
    # Cerramiento transparente en hierro negro + zócalo madera + cristal para supervisión visual de toda la tienda:
    add_house_box(L_PB_ADM_FURN, 34, 5.88, 3.48, 0.00, 6.12, 3.58, 0.90)             # Zócalo esquinero madera
    add_house_box(L_PB_ADM_FURN, 34, 7.05, 3.48, 0.00, 9.00, 3.58, 0.90)             # Zócalo frontal madera
    add_house_box(L_PB_ADM_FURN, 34, 5.88, 0.15, 0.00, 5.98, 3.48, 0.90)             # Zócalo lateral oeste madera
    add_house_box(L_PB_ADM_FURN, 8,  5.88, 3.48, 2.20, 9.00, 3.58, H_P1)             # Dintel hierro negro Norte
    add_house_box(L_PB_ADM_FURN, 8,  5.88, 0.15, 2.20, 5.98, 3.58, H_P1)             # Dintel hierro negro Oeste
    add_house_box(L_CARP,        4,  7.05, 3.52, 0.90, 8.98, 3.55, 2.20)             # Cristal fijo frontal
    add_house_box(L_CARP,        4,  5.92, 0.20, 0.90, 5.95, 3.46, 2.20)             # Cristal fijo lateral hacia Barra
    for mx_p in [6.12, 7.05, 8.02]:
        add_house_box(L_PB_ADM_FURN, 8, mx_p - 0.03, 3.48, 0.00, mx_p + 0.03, 3.58, 2.20)
    # Puerta de vidrio templado entreabierta de la Oficina (X = 6.15..7.02)
    add_house_box(L_CARP, 4, 6.96, 2.68, 0.03, 7.02, 3.48, 2.16)
    # Mobiliario interno Oficina Administración (Escritorio en L + Sillas + Archivador bajo)
    add_house_box(L_PB_ADM_FURN, 34, 7.25, 1.45, 0.00, 8.65, 2.15, 0.76)             # Escritorio gerencial
    add_house_box(L_PB_ADM_FURN, 34, 8.05, 0.85, 0.00, 8.65, 1.45, 0.76)             # Retorno en L
    add_house_box(L_PB_ADM_FURN, 8,  7.65, 0.85, 0.00, 8.15, 1.35, 0.95)             # Silla ejecutiva
    add_house_box(L_PB_ADM_FURN, 30, 6.45, 2.25, 0.00, 6.90, 2.70, 0.80)             # Silla atención proveedor 1
    add_house_box(L_PB_ADM_FURN, 30, 7.35, 2.30, 0.00, 7.80, 2.75, 0.80)             # Silla atención proveedor 2
    add_house_box(L_PB_ADM_FURN, 34, 6.15, 0.20, 0.00, 7.55, 0.65, 0.95)             # Credenza / Archivador

    # --- 3. BARRA GOURMET DE JUGOS NATURALES, CAFÉ Y FRUTA PICADA (Fondo Centro: X = 2.95..5.82, Y = 0.15..3.55) ---
    # Deja paso de barista en X = 2.95..3.58 y abre el gran ventanal Sur para luz y ventilación cruzada N-S!
    add_house_box(L_ZOCALO,      8,  3.60, 2.85, 0.00, 5.75, 3.48, 0.95)             # Frente barra piedra rústica
    add_house_box(L_PB_COM_FURN, 34, 3.55, 2.78, 0.95, 5.80, 3.56, 1.04)             # Tope madera maciza atención
    add_house_box(L_CARP,        4,  4.65, 2.85, 1.04, 5.72, 3.48, 1.42)             # Vitrina fría ensaladas frutas
    for bs_x in [3.75, 4.28, 4.81, 5.34]:
        add_house_box(L_PB_COM_FURN, 30, bs_x - 0.16, 3.68, 0.00, bs_x + 0.16, 4.00, 0.72)  # 4 Taburetes barra jugos
    # Contra-barra posterior en acero/piedra bajo el ventanal Sur (Fregadero doble + Licuadoras + Cafetera)
    add_house_box(L_PB_COM_FURN, 34, 3.05, 0.18, 0.00, 5.75, 0.82, 0.88)
    add_house_box(L_PB_COM_FURN, 8,  3.05, 0.18, 0.88, 5.75, 0.85, 0.92)
    add_house_box(L_PB_COM_FURN, 7,  3.35, 0.28, 0.92, 4.15, 0.72, 0.96)             # Fregadero doble inox
    add_house_box(L_PB_COM_FURN, 1,  4.55, 0.30, 0.92, 4.80, 0.60, 1.32)             # Licuadora industrial 1
    add_house_box(L_PB_COM_FURN, 1,  4.90, 0.30, 0.92, 5.15, 0.60, 1.32)             # Licuadora industrial 2
    add_house_box(L_PB_COM_FURN, 8,  5.28, 0.28, 0.92, 5.68, 0.68, 1.28)             # Máquina café expreso

    # Mobiliario y Acabados del Salón Comercial Ampliado (~112 m²) y Estacionamiento
    add_house_box(L_ZOCALO, 8, 0.30, 8.95, Z_P1_FLOOR, 0.36, Y_AV4 - 0.15, 1.05)
    add_house_box(L_PB_TIMBER, 34, 5.82, 3.58, 2.65, 6.03, Y_AV4 - 0.15, 2.85)
    for vy in [18.575, 16.325, 12.025, 8.875, 6.575]:
        x_w_start = X_GAR_WALL_OUT if vy > 8.80 else 2.90
        add_house_box(L_PB_TIMBER, 34, x_w_start, vy - 0.105, 2.65, 8.95, vy + 0.105, 2.85)
        if vy > 8.80:
            add_house_box(L_PB_TIMBER, 34, 0.30, vy - 0.105, 2.65, X_GAR_RIGHT_IN, vy + 0.105, 2.85)
    add_house_box(L_PB_TIMBER, 34, 3.55, Y_AV4 - 0.16, 2.42, 8.90, Y_AV4, 2.52)
    add_house_box(L_PB_TIMBER, 30, 3.55, Y_AV4 - 0.18, 2.52, 8.90, Y_AV4, 2.70)
    for mx_c in [3.65, 5.75, 6.20, 8.80]:
        add_house_box(L_PB_TIMBER, 34, mx_c - 0.08, Y_AV4 - 0.18, 2.25, mx_c + 0.08, Y_AV4 - 0.02, 2.42)

    # Portón Vehicular Corredizo-Articulado Completo sobre Riel Curvo Lateral a 90° + 2 Plazas de Estacionamiento
    # 1. Riel superior de hierro forjado negro con curva a 90° (Z: 2.35..2.42 m) y guía inferior embutida a ras de suelo
    add_house_box(L_PB_GAR_FURN, 8, 0.40, Y_AV4 - 0.22, 2.35, 3.26, Y_AV4 - 0.14, 2.42)  # Riel dintel frontal
    add_house_box(L_PB_GAR_FURN, 8, 2.96, 21.20,        2.35, 3.26, Y_AV4 - 0.14, 2.42)  # Curva 90° tras columna A0
    add_house_box(L_PB_GAR_FURN, 8, 3.18, 18.90,        2.35, 3.28, 21.20,        2.42)  # Riel lateral muro derecho
    add_house_box(L_PB_GAR_FURN, 8, 0.40, Y_AV4 - 0.20, 0.00, 3.26, Y_AV4 - 0.15, 0.015) # Guía inferior frontal
    add_house_box(L_PB_GAR_FURN, 8, 3.18, 18.90,        0.00, 3.26, Y_AV4 - 0.15, 0.015) # Guía inferior lateral
    # 2. Las 4 hojas articuladas de madera, tablón rústico, ventanilla superior y carros de forja en bolsillo derecho
    for gy1, gy2 in [(19.00, 19.56), (19.59, 20.15), (20.18, 20.74), (20.77, 21.33)]:
        add_house_box(L_PB_GAR_FURN, 34, 3.16, gy1,        0.03, 3.26, gy2,        2.34) # Bastidor hoja madera
        add_house_box(L_PB_GAR_FURN, 30, 3.14, gy1 + 0.05, 0.10, 3.16, gy2 - 0.05, 1.15) # Tablón rústico inferior
        add_house_box(L_PB_GAR_FURN, 4,  3.15, gy1 + 0.08, 1.55, 3.17, gy2 - 0.08, 2.15) # Ventanilla superior vidrio
        add_house_box(L_PB_GAR_FURN, 8,  3.15, gy1,        2.28, 3.27, gy1 + 0.08, 2.36) # Carro rodamiento forja
    # 3. Hoja guía delantera asomando en la curva/vano derecho (X: 2.36..2.94) para lectura visual clara desde Av. 4
    add_house_box(L_PB_GAR_FURN, 34, 2.36, Y_AV4 - 0.21, 0.03, 2.94, Y_AV4 - 0.13, 2.34)
    add_house_box(L_PB_GAR_FURN, 30, 2.41, Y_AV4 - 0.22, 0.10, 2.89, Y_AV4 - 0.12, 1.15)
    add_house_box(L_PB_GAR_FURN, 4,  2.44, Y_AV4 - 0.19, 1.55, 2.86, Y_AV4 - 0.15, 2.15)
    add_house_box(L_PB_GAR_FURN, 8,  2.38, Y_AV4 - 0.23, 0.95, 2.42, Y_AV4 - 0.11, 1.30) # Tirador forja portón
    add_house_box(L_PB_GAR_FURN, 34, 2.94, 21.32,        0.03, 3.22, 21.44,        2.34) # Hoja en transición curva 90°
    for py1, py2 in [(15.20, 20.60), (9.20, 14.60)]:
        add_house_line(L_PB_GAR_FURN, 8, 0.55, py1, 0.005, 2.65, py1, 0.005)
        add_house_line(L_PB_GAR_FURN, 8, 0.55, py2, 0.005, 2.65, py2, 0.005)
        add_house_line(L_PB_GAR_FURN, 8, 0.55, py1, 0.005, 0.55, py2, 0.005)
        add_house_line(L_PB_GAR_FURN, 8, 2.65, py1, 0.005, 2.65, py2, 0.005)

    # Santamarías de Caracol Completas (Carriles en "U" + Tambor Caracol con Platos + Faldón de Lamas y Manillas)
    for sm_x1, sm_x2 in [(3.65, 5.75), (6.20, 8.80)]:
        # 1. Carriles guía laterales en "U" de hierro negro en ambas jambas (Z: 0.00..2.40 m)
        add_house_box(L_PB_COM_FURN, 8,  sm_x1,        Y_AV4 - 0.14, 0.00, sm_x1 + 0.07, Y_AV4 - 0.02, 2.40)
        add_house_box(L_PB_COM_FURN, 8,  sm_x2 - 0.07, Y_AV4 - 0.14, 0.00, sm_x2,        Y_AV4 - 0.02, 2.40)
        # 2. Tambor / Caracol Cilíndrico Superior Enrollable (Z: 2.10..2.39 m) + Platos laterales de soporte
        add_house_box(L_PB_COM_FURN, 8,  sm_x1 + 0.05, Y_AV4 - 0.36, 2.12, sm_x2 - 0.05, Y_AV4 - 0.04, 2.38)
        add_house_box(L_PB_COM_FURN, 9,  sm_x1 + 0.06, Y_AV4 - 0.38, 2.17, sm_x2 - 0.06, Y_AV4 - 0.02, 2.33) # Relieve espiral
        add_house_box(L_PB_COM_FURN, 30, sm_x1 + 0.02, Y_AV4 - 0.39, 2.08, sm_x1 + 0.10, Y_AV4 - 0.01, 2.40) # Plato caracol izq.
        add_house_box(L_PB_COM_FURN, 30, sm_x2 - 0.10, Y_AV4 - 0.39, 2.08, sm_x2 - 0.02, Y_AV4 - 0.01, 2.40) # Plato caracol der.
        # 3. Faldón inferior de lamas metálicas recogidas visible bajo el dintel (Z: 1.98..2.12 m) + cerradura/manilla
        for z_slat, col_sl in [(2.07, 9), (2.02, 8)]:
            add_house_box(L_PB_COM_FURN, col_sl, sm_x1 + 0.05, Y_AV4 - 0.10, z_slat, sm_x2 - 0.05, Y_AV4 - 0.05, z_slat + 0.045)
        add_house_box(L_PB_COM_FURN, 8,  sm_x1 + 0.04, Y_AV4 - 0.12, 1.98, sm_x2 - 0.04, Y_AV4 - 0.04, 2.02) # Perfil T inferior
        sm_mid = 0.5 * (sm_x1 + sm_x2)
        add_house_box(L_PB_COM_FURN, 34, sm_mid - 0.25, Y_AV4 - 0.14, 1.99, sm_mid + 0.25, Y_AV4 - 0.02, 2.05) # Manilla central
    for cy_col, ix1, ix2, iy1, iy2, col_f1, col_f2 in [
        (18.575, 5.15, 6.30, 17.95, 19.20, 1, 2),
        (16.325, 5.15, 6.70, 15.55, 17.10, 30, 3),
        (12.025, 5.15, 6.70, 11.25, 12.80, 1, 3),
        (8.875,  5.15, 6.70,  8.10,  9.65, 2, 30),
        (6.575,  5.15, 6.70,  5.30,  6.85, 3, 1),   # Nueva 5ta Isla Degustación / Orgánicos en espacio liberado!
    ]:
        add_house_box(L_PB_TIMBER, 34, 5.735, cy_col - 0.19, Z_P1_FLOOR, 6.115, cy_col + 0.19, 2.65)
        add_house_box(L_ZOCALO, 8, ix1 + 0.10, iy1 + 0.10, 0.00, ix2 - 0.10, iy2 - 0.10, 0.32)
        add_house_box(L_PB_COM_FURN, 34, ix1, iy1, 0.32, ix2, iy2, 0.68)
        add_house_box(L_PB_COM_FURN, col_f1, ix1 + 0.06, iy1 + 0.06, 0.68, ix2 - 0.06, iy2 - 0.06, 0.76)
        add_house_box(L_PB_COM_FURN, 34, ix1 + 0.22, iy1 + 0.22, 0.76, ix2 - 0.22, iy2 - 0.22, 1.04)
        add_house_box(L_PB_COM_FURN, col_f2, ix1 + 0.26, iy1 + 0.26, 1.04, ix2 - 0.26, iy2 - 0.26, 1.12)

    for z_sh, f_col in [(0.52, 30), (0.98, 1), (1.44, 2)]:
        add_house_box(L_PB_COM_FURN, 34, 3.46, 9.00, z_sh, 4.05, 20.60, z_sh + 0.10)
        add_house_box(L_PB_COM_FURN, f_col, 3.52, 9.08, z_sh + 0.10, 4.00, 20.52, z_sh + 0.22)
        add_house_box(L_PB_COM_FURN, 34, 2.91, 4.65, z_sh, 3.50, 8.70, z_sh + 0.10)
    # Exhibidor verdulería Este + Nuevo Mural Frigorífico Vertical de Lácteos/Quesos/Fruta Picada (donde iba el baño viejo!)
    add_house_box(L_PB_COM_FURN, 34, 8.35, 7.80, 0.25, 8.98, 16.50, 0.58)
    add_house_box(L_PB_COM_FURN, 3,  8.40, 7.88, 0.58, 8.94, 16.42, 0.66)
    add_house_box(L_PB_COM_FURN, 8,  8.26, 5.10, 0.00, 8.98, 7.55, 2.05)              # Mural Frigorífico Abierto
    add_house_box(L_CARP,        4,  8.24, 5.20, 0.45, 8.30, 7.45, 1.85)              # Cortina fría / repisas cristal
    for z_fr in [0.55, 0.95, 1.35]:
        add_house_box(L_PB_COM_FURN, 7, 8.32, 5.20, z_fr, 8.92, 7.45, z_fr + 0.05)
    # Mostrador de Caja Principal junto a entrada Av. 4
    add_house_box(L_ZOCALO, 8, 7.05, 18.25, 0.00, 8.75, 18.95, 0.92)
    add_house_box(L_ZOCALO, 8, 7.05, 17.05, 0.00, 7.70, 18.25, 0.92)
    add_house_box(L_PB_COM_FURN, 34, 6.98, 18.20, 0.92, 8.80, 19.02, 1.00)
    add_house_box(L_PB_COM_FURN, 34, 6.98, 17.00, 0.92, 7.76, 18.20, 1.00)

    # =========================================================================
    # COLUMNAS ESTRUCTURALES EN LOS 3 NIVELES SOBRE RASANTE:
    # PB (Concreto), P2 (Concreto/Madera) y P3 (COLUMNAS METÁLICAS NEGRAS VISTAS)
    # =========================================================================
    L_P2_COL    = "P2_COLUMNAS_3D"
    L_P3_COL    = "P3_COLUMNAS_METAL_NEGRO_3D"
    L_TIMBER    = "ESTRUCTURA_MADERA_CHALET_3D"

    existing_and_new_cols = [
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
        # Eje H posterior (Y = 0.125)
        (0.275, 0.125),  (2.825, 0.125),  (5.925, 0.125),  (9.075, 0.125),
    ]
    for cx, cy in existing_and_new_cols:
        # Planta Baja (Z = 0.00..2.85)
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)
        # Segundo Piso ahora completo (Z = 3.00..5.85, sin buhardilla baja en P2)
        add_house_box(L_P2_COL, 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, H_P2)
        # Nuevo Tercer Piso: Columnas Metálicas Estructurales Negras (25x25 cm + platabandas IPE, color 8)
        z_col_p3_top = 8.50 if (cx < 3.0 and cy < 4.0) else min(H_P3, z_roof_under(cx))
        add_house_box(L_P3_COL, 8, cx - 0.12, cy - 0.12, Z_P3_FLOOR, cx + 0.12, cy + 0.12, z_col_p3_top)
        # Placa base metálica negra empernada en arranque P3 (respetando minX >= 0.15 m en Eje 0)
        add_house_box(L_P3_COL, 8, max(0.15, cx - 0.16), cy - 0.16, Z_P3_FLOOR, cx + 0.16, cy + 0.16, Z_P3_FLOOR + 0.03)

    # Vigas metálicas perimetrales y maestras negras en entrepiso Steel Deck P3 (Z = 5.82..6.00)
    for gx_beam in [0.275, 2.825, 5.925, 9.025]:
        add_house_box(L_P3_COL, 8, gx_beam - 0.09, 0.15, H_P2 - 0.05, gx_beam + 0.09, Y_AV4, H_P2)

    # =========================================================================
    # 3. SEGUNDO PISO — OPCIÓN A (Z = +3.00 a +5.85 m):
    #    PLANTA DE DÍA CON TRIPLE FACHADA ABIERTA + HAB. 4 HUÉSPEDES + ESCALERA A P3
    # =========================================================================
    L_P2_SLAB     = "P2_LOSA_PISO_3D"
    L_P2_EXT      = "P2_MUROS_EXT_3D"
    L_P2_INT      = "P2_MUROS_INT_3D"
    L_P2_ISL      = "P2_COCINA_ISLA_3D"
    L_SOCIAL_FURN = "P2_MOBILIARIO_SOCIAL_3D"

    # Losa Entrepiso P2 (9.00 x 21.71 m):
    # - Hueco en X = 1.55..2.65, Y = 4.40..7.35 (llegada Escalera Tramo 2 desde PB)
    # - Losa maciza en X = 0.15..1.55, Y = 4.40..7.35 (base firme donde arranca Escalera Tramo 3 hacia P3)
    add_house_box(L_P2_SLAB, 8, 0.15, 0.00, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 4.40, H_P1, 1.55, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR)

    # Escalera Tramo 2 INTACTA: Sube de PB (Z=0.00 en Y=7.35) a P2 (Z=+3.00 en Y=4.40), X: 1.55..2.65
    num_steps_p2 = 14
    step_dy_p2 = (7.35 - 4.40) / num_steps_p2
    step_dz_p2 = (Z_P2_FLOOR - Z_P1_FLOOR) / num_steps_p2
    for i in range(num_steps_p2):
        y_s_bot = 7.35 - (i + 1) * step_dy_p2
        y_s_top = 7.35 - i * step_dy_p2
        z_s_bot = Z_P1_FLOOR + i * step_dz_p2
        z_s_top = z_s_bot + step_dz_p2
        add_house_box("P2_ESCALERA_3D", 7, 1.55, y_s_bot, z_s_bot - 0.15, 2.65, y_s_top, z_s_top)

    # NUEVA ESCALERA TRAMO 3 APILADA: Sube de P2 (Z=+3.00 en Y=4.40) a P3 (Z=+6.00 en Y=7.40), X: 0.30..1.45
    # Se apila limpiamente sobre el vacío de la escalera del sótano sin chocar cabezadas
    num_steps_p3 = 14
    step_dy_p3 = (7.40 - 4.40) / num_steps_p3
    step_dz_p3 = (Z_P3_FLOOR - Z_P2_FLOOR) / num_steps_p3
    for i in range(num_steps_p3):
        y3_bot = 4.40 + i * step_dy_p3
        y3_top = y3_bot + step_dy_p3
        z3_bot = Z_P2_FLOOR + i * step_dz_p3
        z3_top = z3_bot + step_dz_p3
        add_house_box("P3_ESCALERA_3D", 30, 0.30, y3_bot, z3_bot - 0.14, 1.45, y3_top, z3_top)

    # Baranda inclinada sobre Escalera Tramo 3 (acompaña subida a P3 sobre el tabique de la Despensa bajo escalera)
    add_house_hexa(L_BALC, 30, [
        (1.44, 4.45, Z_P2_FLOOR + 0.92), (1.52, 4.45, Z_P2_FLOOR + 0.92),
        (1.52, 7.40, Z_P3_FLOOR + 0.92), (1.44, 7.40, Z_P3_FLOOR + 0.92),
        (1.44, 4.45, Z_P2_FLOOR + 1.00), (1.52, 4.45, Z_P2_FLOOR + 1.00),
        (1.52, 7.40, Z_P3_FLOOR + 1.00), (1.44, 7.40, Z_P3_FLOOR + 1.00),
    ])
    for bp_i in range(7):
        f_bp = bp_i / 6.0
        yb_p = 4.50 + f_bp * (7.32 - 4.50)
        zb_p = Z_P2_FLOOR + f_bp * (Z_P3_FLOOR - Z_P2_FLOOR)
        add_house_box(L_BALC, 30, 1.45, yb_p - 0.03, zb_p, 1.51, yb_p + 0.03, zb_p + 0.94)
    add_alpine_railing_y(2.72, 4.65, 7.35, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_x(1.55, 2.72, 7.38, Z_P2_FLOOR, h_rail=1.05, n_bays=1)

    # Muro Oeste Propio Ciego en Piso 2 (X = 0.15..0.30, Y = 0.00..21.71, Z = 3.00..5.85) — CERO invasión
    add_house_box(L_P2_EXT, 34, 0.15, 0.00, Z_P2_FLOOR, 0.30, Y_AV4, H_P2)

    # --- GRAN BALCONADA SOCIAL CONTINUA EN FRENTE AVENIDA 4 (X: 0.30..9.00, Y: 19.60..21.56 = 17,05 m²) ---
    add_alpine_railing_x(0.42, 2.68, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_x(2.97, 5.80, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_x(6.05, 8.95, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_y(9.07, 19.60, Y_AV4 - 0.12, Z_P2_FLOOR, h_rail=1.05, n_bays=2)

    # Muro Frontal Acristalado de Retranqueo en P2 (Y = 19.45..19.60): 3 Mamparas Corredizas de Terraza Completas
    p2_terrace_openings = [
        (0.65, 2.55, Z_P2_FLOOR, Z_P2_FLOOR + 2.25),   # Mampara corrediza Sala Oeste -> Balconada
        (3.15, 5.55, Z_P2_FLOOR, Z_P2_FLOOR + 2.25),   # Mampara corrediza Sala Central -> Balconada
        (6.25, 8.65, Z_P2_FLOOR, Z_P2_FLOOR + 2.25),   # Mampara corrediza Estudio Acristalado -> Balconada
    ]
    add_wall_with_openings_x(L_P2_EXT, 34, 0.30, 9.00, 19.45, 19.60, Z_P2_FLOOR, H_P2, p2_terrace_openings)
    for mx1, mx2, mz1, mz2 in p2_terrace_openings:
        # Marco perimetral de madera maciza + riel inferior doble a ras de piso
        add_house_box(L_CARP, 34, mx1 - 0.04, 19.43, mz1,        mx1 + 0.03, 19.62, mz2 + 0.03)  # Jamba izquierda
        add_house_box(L_CARP, 34, mx2 - 0.03, 19.43, mz1,        mx2 + 0.04, 19.62, mz2 + 0.03)  # Jamba derecha
        add_house_box(L_CARP, 34, mx1 - 0.04, 19.43, mz2 - 0.03, mx2 + 0.04, 19.62, mz2 + 0.04)  # Dintel / riel superior
        add_house_box(L_CARP, 8,  mx1 + 0.03, 19.46, mz1,        mx2 - 0.03, 19.59, mz1 + 0.025) # Riel guía inferior doble
        # Hoja fija/estacionada (carril exterior Y=19.54..19.57) + Hoja corrediza abierta (carril interior Y=19.48..19.51)
        w_leaf = 0.50 * (mx2 - mx1)
        for lx_a, lx_b, ly_a, ly_b in [
            (mx1 + 0.03, mx1 + 0.03 + w_leaf, 19.54, 19.57),
            (mx1 + 0.22, mx1 + 0.22 + w_leaf, 19.48, 19.51),
        ]:
            add_house_box(L_CARP, 34, lx_a,        ly_a, mz1 + 0.025, lx_a + 0.045, ly_b, mz2 - 0.03) # Parante izq. hoja
            add_house_box(L_CARP, 34, lx_b - 0.045, ly_a, mz1 + 0.025, lx_b,        ly_b, mz2 - 0.03) # Parante der. hoja
            add_house_box(L_CARP, 34, lx_a + 0.045, ly_a, mz1 + 0.025, lx_b - 0.045, ly_b, mz1 + 0.07) # Zócalo inf. hoja
            add_house_box(L_CARP, 34, lx_a + 0.045, ly_a, mz2 - 0.075, lx_b - 0.045, ly_b, mz2 - 0.03) # Cabezal sup. hoja
            add_house_box(L_CARP, 4,  lx_a + 0.045, ly_a + 0.008, mz1 + 0.07, lx_b - 0.045, ly_b - 0.008, mz2 - 0.075) # Cristal
        # Tirador negro en la hoja corrediza dejando paso franco abierto hacia la Balconada
        hx_pull = mx1 + 0.22 + w_leaf - 0.06
        add_house_box(L_CARP, 8, hx_pull, 19.46, mz1 + 0.90, hx_pull + 0.025, 19.53, mz1 + 1.25)

    # --- FACHADA ESTE PRIVILEGIADA EN P2 (X = 9.00..9.15, Y = 0.00..19.60): ABIERTA A VIENTOS ALISIOS ---
    east_windows_p2 = [
        (1.10,  3.05, Z_P2_FLOOR + 0.90, Z_P2_FLOOR + 2.20),  # Ventanal Este Habitación 4 (Huéspedes/Adulto Mayor)
        (5.15,  6.35, Z_P2_FLOOR + 1.15, Z_P2_FLOOR + 2.10),  # Ventana Baño Social Completo
        (8.45,  11.35, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25), # GRAN VENTANAL ESTE COCINA GOURMET (Ventilación directa Isla)
        (12.35, 14.75, Z_P2_FLOOR + 0.55, Z_P2_FLOOR + 2.25), # GRAN VENTANAL GALERÍA / DESAYUNADOR ESTE (Luz al Comedor)
        (16.00, 18.60, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25), # GRAN VENTANAL ESTE ESTUDIO / SALA
    ]
    add_wall_with_openings_y(L_P2_EXT, 34, 9.00, 9.15, 0.00, 19.60, Z_P2_FLOOR, H_P2, east_windows_p2)
    for wy1, wy2, wz1, wz2 in east_windows_p2:
        add_rustic_window_east(wy1, wy2, wz1, wz2, with_shutters=(wy2 - wy1 >= 1.40))

    # --- FACHADA POSTERIOR SUR EN P2 (Y = 0.00..0.15): DESFOGUE DE BRISA CRUZADA ---
    south_windows_p2 = [
        (0.75, 2.35, Z_P2_FLOOR + 1.00, Z_P2_FLOOR + 2.15),   # Ventana Lavandería (ahora H = 2,85 m libre!)
        (3.30, 5.45, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25),   # Gran Ventanal Mirador Sur Ventilado
        (6.60, 8.45, Z_P2_FLOOR + 0.90, Z_P2_FLOOR + 2.15),   # Ventanal Sur Habitación 4 Esquinera (90°)
    ]
    add_wall_with_openings_x(L_P2_EXT, 34, 0.30, 9.15, 0.00, 0.15, Z_P2_FLOOR, H_P2, south_windows_p2)
    for wx1, wx2, wz1, wz2 in south_windows_p2:
        add_rustic_window_south(wx1, wx2, wz1, wz2, with_shutters=(wx2 - wx1 >= 1.40))

    # --- TABIQUERÍA BIOCLIMÁTICA DE PISO 2 (OPCIÓN A: SIN MURO CIEGO EN Y = 7.45..19.45!) ---
    # 1. Estudio / Home Office separado con TABIQUE INDUSTRIAL ACRISTALADO (Hierro negro + Vidrio corredizo)
    #    Permite privacidad acústica para trabajar dejando pasar el 100% de la luz y abrir para brisa cruzada:
    add_house_box(L_P3_COL, 8, 5.88, 15.20, Z_P2_FLOOR, 5.96, 19.45, Z_P2_FLOOR + 0.08)   # Solera hierro negro
    add_house_box(L_P3_COL, 8, 5.88, 15.20, Z_P2_FLOOR + 2.35, 5.96, 19.45, H_P2)         # Dintel superior
    add_house_box(L_CARP,   4, 5.91, 15.25, Z_P2_FLOOR + 0.08, 5.93, 19.40, Z_P2_FLOOR + 2.35) # Cristal piso-techo
    for gy_m in [15.20, 16.60, 18.00, 19.42]:
        add_house_box(L_P3_COL, 8, 5.88, gy_m - 0.03, Z_P2_FLOOR + 0.08, 5.96, gy_m + 0.03, Z_P2_FLOOR + 2.35)
    # Cierre Sur acristalado del Estudio (Y = 15.14..15.22, X = 5.96..9.00) con puerta corrediza abierta
    add_house_box(L_P3_COL, 8, 5.96, 15.14, Z_P2_FLOOR + 2.35, 9.00, 15.22, H_P2)
    add_house_box(L_CARP,   4, 7.45, 15.16, Z_P2_FLOOR + 0.05, 8.98, 15.20, Z_P2_FLOOR + 2.35)

    # 2. Bloque Sureste: Baño Social Completo (Y: 4.45..7.40) + Habitación 4 Huéspedes (Y: 0.15..4.30)
    add_wall_with_openings_y(L_P2_INT, 6, 5.85, 6.00, 0.15, 7.45, Z_P2_FLOOR, H_P2, [
        (2.55, 3.40, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),        # Puerta Habitación 4 (Huéspedes/Adulto Mayor)
        (5.25, 6.05, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),        # Puerta Baño Social Completo
    ])
    add_house_box(L_P2_INT, 6, 6.00, 7.35, Z_P2_FLOOR, 9.00, 7.50, H_P2)   # Muro Norte Baño Social
    add_house_box(L_P2_INT, 6, 6.00, 4.30, Z_P2_FLOOR, 9.00, 4.45, H_P2)   # División Baño Social / Hab. 4

    # 3. NUEVA DESPENSA WALK-IN BAJO LA ESCALERA QUE SUBE AL PISO 3 (X: 0.30..1.45, Y: 5.45..7.40)
    #    Aprovecha el volumen alto bajo el tramo Norte de P3_ESCALERA_3D y libera un paso diáfano de 3,10 m
    #    entre las escaleras y la cocina (CERO muros ni muebles estorbando en el centro!).
    add_house_hexa(L_P2_INT, 34, [
        (1.44, 4.65, Z_P2_FLOOR), (1.52, 4.65, Z_P2_FLOOR),
        (1.52, 7.40, Z_P2_FLOOR), (1.44, 7.40, Z_P2_FLOOR),
        (1.44, 4.65, Z_P2_FLOOR + 0.14), (1.52, 4.65, Z_P2_FLOOR + 0.14),
        (1.52, 7.40, Z_P2_FLOOR + 2.72), (1.44, 7.40, Z_P2_FLOOR + 2.72),
    ])  # Cerramiento lateral machihembrado exacto bajo la zanca inclinada de la escalera a P3
    add_house_box(L_P2_INT, 6, 0.30, 5.40, Z_P2_FLOOR, 1.44, 5.48, Z_P2_FLOOR + 0.90)  # Fondo Sur bajo rampa
    add_wall_with_openings_x(L_P2_INT, 34, 0.30, 1.52, 7.34, 7.43, Z_P2_FLOOR, Z_P2_FLOOR + 2.72, [
        (0.44, 1.29, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),        # Puerta Despensa bajo escalera hacia Cocina
    ])
    # Marco de madera y hoja rústica entreabierta hacia la medianera Oeste (sin invadir pasillo)
    add_house_box(L_CARP, 34, 0.40, 7.32, Z_P2_FLOOR, 0.46, 7.45, Z_P2_FLOOR + H_DOOR)
    add_house_box(L_CARP, 34, 1.27, 7.32, Z_P2_FLOOR, 1.33, 7.45, Z_P2_FLOOR + H_DOOR)
    add_house_box(L_CARP, 30, 0.42, 7.43, Z_P2_FLOOR + 0.02, 0.48, 8.20, Z_P2_FLOOR + H_DOOR - 0.02)
    # 4 niveles de estanterías escalonadas en L dentro de la Despensa bajo escalera
    for sh_z, y_min_sh in [(3.42, 5.50), (3.85, 5.75), (4.28, 6.18), (4.72, 6.62)]:
        add_house_box(L_TIMBER, 34, 0.32, y_min_sh, sh_z, 0.72, 7.30, sh_z + 0.04)
    add_house_box(L_TIMBER, 34, 0.72, 5.50, 3.42, 1.40, 5.88, 3.46)
    add_house_box(L_TIMBER, 34, 0.72, 5.75, 3.85, 1.40, 6.12, 3.89)

    # 4. Lavandería Ventilada al Sur (X: 0.30..2.75, Y: 0.15..3.55) — SIN escalera de tanque (libre H = 2,85 m!)
    add_wall_with_openings_x(L_P2_INT, 6, 0.30, 2.75, 3.45, 3.60, Z_P2_FLOOR, H_P2, [
        (1.65, 2.48, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    add_house_box(L_P2_INT, 6, 2.75, 0.15, Z_P2_FLOOR, 2.90, 3.60, H_P2)

    # --- INTERIORISMO Y MOBILIARIO COMPLETO DEL PISO 2 (OPCIÓN A) ---
    # A. Balconada Social Continua (Sofá lounge oeste + Comedor exterior 6p este + Jardineras)
    add_house_box(L_SOCIAL_FURN, 34, 0.50, 20.05, Z_P2_FLOOR, 1.30, 21.25, Z_P2_FLOOR + 0.42)
    add_house_box(L_SOCIAL_FURN, 34, 1.45, 20.35, Z_P2_FLOOR, 1.95, 20.95, Z_P2_FLOOR + 0.42)
    add_house_box(L_SOCIAL_FURN, 34, 6.35, 20.20, Z_P2_FLOOR, 8.15, 21.05, Z_P2_FLOOR + 0.75)  # Mesa terraza Este
    add_house_box(L_SOCIAL_FURN, 30, 6.45, 19.80, Z_P2_FLOOR, 8.05, 20.12, Z_P2_FLOOR + 0.45)
    add_house_box(L_SOCIAL_FURN, 30, 6.45, 21.12, Z_P2_FLOOR, 8.05, 21.44, Z_P2_FLOOR + 0.45)

    # B. Gran Sala Principal Chalet (X: 0.30..5.75, Y: 15.40..19.35)
    add_house_box(L_SOCIAL_FURN, 30, 2.60, 18.45, Z_P2_FLOOR, 5.25, 19.35, Z_P2_FLOOR + 0.42)  # Sofá XL Norte
    add_house_box(L_SOCIAL_FURN, 30, 2.60, 19.15, Z_P2_FLOOR + 0.42, 5.25, 19.35, Z_P2_FLOOR + 0.82)
    add_house_box(L_SOCIAL_FURN, 30, 2.60, 16.30, Z_P2_FLOOR, 3.50, 18.45, Z_P2_FLOOR + 0.42)  # Sofá XL Oeste
    add_house_box(L_SOCIAL_FURN, 34, 3.85, 16.95, Z_P2_FLOOR, 4.65, 18.05, Z_P2_FLOOR + 0.40)  # Mesa centro tronco
    add_house_box(L_SOCIAL_FURN, 34, 0.34, 16.25, Z_P2_FLOOR, 0.88, 18.75, Z_P2_FLOOR + 0.55)  # Mueble TV en muro Oeste!
    add_house_box(L_SOCIAL_FURN, 8,  0.35, 16.65, Z_P2_FLOOR + 0.82, 0.42, 18.35, Z_P2_FLOOR + 1.80) # TV 75" (deja libre vista Este!)

    # C. Estudio / Home Office Acristalado (X: 6.05..8.95, Y: 15.30..19.35)
    add_house_box(L_SOCIAL_FURN, 34, 7.35, 16.60, Z_P2_FLOOR, 8.15, 18.40, Z_P2_FLOOR + 0.76)  # Escritorio ejecutivo
    add_house_box(L_SOCIAL_FURN, 8,  8.25, 17.20, Z_P2_FLOOR, 8.75, 17.80, Z_P2_FLOOR + 0.92)  # Silla ergonómica
    add_house_box(L_SOCIAL_FURN, 34, 6.05, 15.35, Z_P2_FLOOR, 6.45, 17.40, Z_P2_FLOOR + 2.20)  # Biblioteca abierta

    # D. Gran Comedor 10 Puestos (Centro: X: 1.95..4.75, Y: 12.80..14.60) + Desayunador Luminoso Este (X: 6.80..8.60)
    add_house_box(L_SOCIAL_FURN, 34, 2.05, 13.15, Z_P2_FLOOR + 0.70, 4.75, 14.30, Z_P2_FLOOR + 0.77) # Mesa 2,70 x 1,15 m
    add_house_box(L_SOCIAL_FURN, 8,  2.40, 13.35, Z_P2_FLOOR, 2.58, 14.10, Z_P2_FLOOR + 0.70)
    add_house_box(L_SOCIAL_FURN, 8,  4.22, 13.35, Z_P2_FLOOR, 4.40, 14.10, Z_P2_FLOOR + 0.70)
    for ch_x in [2.25, 2.88, 3.51, 4.14]:
        add_house_box(L_SOCIAL_FURN, 30, ch_x, 12.68, Z_P2_FLOOR, ch_x + 0.44, 13.10, Z_P2_FLOOR + 0.46)
        add_house_box(L_SOCIAL_FURN, 30, ch_x, 14.35, Z_P2_FLOOR, ch_x + 0.44, 14.77, Z_P2_FLOOR + 0.46)
    # Desayunador / Galería Este junto al gran ventanal de brisa alisia
    add_house_box(L_SOCIAL_FURN, 34, 7.15, 13.05, Z_P2_FLOOR, 8.25, 14.15, Z_P2_FLOOR + 0.75)
    add_house_box(L_SOCIAL_FURN, 30, 8.35, 13.25, Z_P2_FLOOR, 8.85, 13.95, Z_P2_FLOOR + 0.78)
    add_house_box(L_SOCIAL_FURN, 30, 6.55, 13.25, Z_P2_FLOOR, 7.05, 13.95, Z_P2_FLOOR + 0.78)

    # E. Cocina Gourmet con Gran Isla Central + NEVERA FRENCH DOOR DETALLADA en remate Norte (Y: 8.45..13.10)
    #    Deja 100% despejado Y = 7.43..8.45 frente a la puerta de la Despensa Bajo Escalera y X = 1.55..5.85!
    add_house_box(L_P2_ISL, 34, 0.30, 8.45, Z_P2_FLOOR, 0.94, 11.48, Z_P2_FLOOR + 0.86)         # Mesón lineal Oeste
    add_house_box(L_P2_ISL, 8,  0.30, 8.45, Z_P2_FLOOR + 0.86, 0.98, 11.48, Z_P2_FLOOR + 0.92)  # Tope granito negro
    add_house_box(L_P2_ISL, 7,  0.38, 8.70, Z_P2_FLOOR + 0.92, 0.86, 9.60,  Z_P2_FLOOR + 0.95)  # Fregadero doble inox
    add_house_box(L_P2_ISL, 7,  0.42, 9.12, Z_P2_FLOOR + 0.95, 0.56, 9.18,  Z_P2_FLOOR + 1.25)  # Grifería cuello cisne
    add_house_box(L_P2_ISL, 8,  0.38, 10.18, Z_P2_FLOOR + 0.92, 0.88, 11.12, Z_P2_FLOOR + 0.96) # Tope cocina 5 hornillas
    add_house_box(L_P2_ISL, 8,  0.32, 10.15, Z_P2_FLOOR + 1.65, 0.92, 11.15, Z_P2_FLOOR + 1.82) # Campana extractora
    add_house_box(L_P2_ISL, 8,  0.32, 10.45, Z_P2_FLOOR + 1.82, 0.68, 10.85, H_P2)              # Ducto campana acero
    add_house_box(L_P2_ISL, 34, 0.32, 8.48,  Z_P2_FLOOR + 1.55, 0.68, 9.95,  Z_P2_FLOOR + 2.30) # Gabinete aéreo madera
    # Torre de Horno + Microondas empotrados (Y = 11.48..12.10)
    add_house_box(L_P2_ISL, 34, 0.30, 11.48, Z_P2_FLOOR, 0.98, 12.10, Z_P2_FLOOR + 2.30)
    add_house_box(L_P2_ISL, 8,  0.96, 11.53, Z_P2_FLOOR + 0.72, 1.00, 12.05, Z_P2_FLOOR + 1.32) # Horno empotrado
    add_house_box(L_P2_ISL, 8,  0.96, 11.53, Z_P2_FLOOR + 1.40, 1.00, 12.05, Z_P2_FLOOR + 1.80) # Microondas empotrado
    # NEVERA FRENCH DOOR EN ACERO/GRAFITO (0,90 x 0,78 x 1,92 m en X = 0.32..1.10, Y = 12.14..13.04)
    add_house_box(L_P2_ISL, 34, 0.30, 12.10, Z_P2_FLOOR + 1.98, 1.02, 13.10, Z_P2_FLOOR + 2.30) # Mueble puente sobre nevera
    add_house_box(L_P2_ISL, 34, 0.30, 13.06, Z_P2_FLOOR, 1.02, 13.12, Z_P2_FLOOR + 2.30)        # Costado madera norte
    add_house_box(L_P2_ISL, 8,  0.32, 12.14, Z_P2_FLOOR, 1.05, 13.04, Z_P2_FLOOR + 1.94)        # Cuerpo principal nevera
    add_house_box(L_P2_ISL, 7,  1.05, 12.16, Z_P2_FLOOR + 0.04, 1.10, 13.02, Z_P2_FLOOR + 0.70) # Gavetón congelador inf.
    add_house_box(L_P2_ISL, 7,  1.05, 12.16, Z_P2_FLOOR + 0.74, 1.10, 12.58, Z_P2_FLOOR + 1.92) # Puerta izq. French Door
    add_house_box(L_P2_ISL, 7,  1.05, 12.60, Z_P2_FLOOR + 0.74, 1.10, 13.02, Z_P2_FLOOR + 1.92) # Puerta der. French Door
    add_house_box(L_P2_ISL, 8,  1.09, 12.68, Z_P2_FLOOR + 1.12, 1.12, 12.88, Z_P2_FLOOR + 1.42) # Dispensador agua/hielo
    add_house_box(L_P2_ISL, 8,  1.10, 12.53, Z_P2_FLOOR + 0.88, 1.14, 12.56, Z_P2_FLOOR + 1.75) # Manilla vertical izq.
    add_house_box(L_P2_ISL, 8,  1.10, 12.62, Z_P2_FLOOR + 0.88, 1.14, 12.65, Z_P2_FLOOR + 1.75) # Manilla vertical der.
    add_house_box(L_P2_ISL, 8,  1.10, 12.24, Z_P2_FLOOR + 0.60, 1.14, 12.94, Z_P2_FLOOR + 0.64) # Manilla congelador
    # Gran Isla Central + 4 Bancos altos
    add_house_box(L_P2_ISL, 34, 2.40, 8.85, Z_P2_FLOOR, 3.35, 11.75, Z_P2_FLOOR + 0.86)         # Gran Isla Gourmet 2,90m
    add_house_box(L_P2_ISL, 8,  2.36, 8.85, Z_P2_FLOOR + 0.86, 3.68, 11.75, Z_P2_FLOOR + 0.92)  # Tope volado barra
    for b_y in [9.15, 9.85, 10.55, 11.25]:
        add_house_box(L_SOCIAL_FURN, 30, 3.62, b_y - 0.18, Z_P2_FLOOR, 4.02, b_y + 0.18, Z_P2_FLOOR + 0.68)

    # F. Baño Social Completo (X: 6.00..9.00, Y: 4.45..7.35) + Habitación 4 Huéspedes (X: 6.00..9.00, Y: 0.15..4.30)
    add_house_box(L_SOCIAL_FURN, 8,  7.95, 4.50, Z_P2_FLOOR, 8.95, 5.55, Z_P2_FLOOR + 0.06)    # Plato ducha visitas
    add_house_box(L_SOCIAL_FURN, 4,  7.95, 5.53, Z_P2_FLOOR + 0.06, 8.65, 5.57, Z_P2_FLOOR + 2.05)
    add_house_box(L_SOCIAL_FURN, 7,  7.10, 4.50, Z_P2_FLOOR, 7.55, 5.10, Z_P2_FLOOR + 0.42)    # WC
    add_house_box(L_SOCIAL_FURN, 34, 6.20, 6.75, Z_P2_FLOOR, 7.60, 7.32, Z_P2_FLOOR + 0.85)    # Tocador baño social
    # Habitación 4 Esquinera (Cama Queen + Mesas de Noche + Clóset)
    add_house_box(L_SOCIAL_FURN, 34, 6.05, 1.35, Z_P2_FLOOR, 7.95, 2.95, Z_P2_FLOOR + 0.56)    # Cama Queen huéspedes
    add_house_box(L_SOCIAL_FURN, 34, 6.05, 0.80, Z_P2_FLOOR, 6.50, 1.28, Z_P2_FLOOR + 0.52)
    add_house_box(L_SOCIAL_FURN, 34, 6.25, 3.70, Z_P2_FLOOR, 8.45, 4.28, Z_P2_FLOOR + 2.25)    # Clóset piso a techo

    # G. Lavandería Ventilada sin Escalera de Tanque (X: 0.30..2.75, Y: 0.15..3.45)
    add_house_box(L_SOCIAL_FURN, 7,  0.35, 0.25, Z_P2_FLOOR, 1.05, 0.95, Z_P2_FLOOR + 0.88)    # Lavadora
    add_house_box(L_SOCIAL_FURN, 7,  1.12, 0.25, Z_P2_FLOOR, 1.82, 0.95, Z_P2_FLOOR + 0.88)    # Secadora
    add_house_box(L_SOCIAL_FURN, 8,  1.88, 0.25, Z_P2_FLOOR, 2.70, 0.95, Z_P2_FLOOR + 0.88)    # Batea / Lavadero
    add_house_box(L_SOCIAL_FURN, 34, 0.35, 1.35, Z_P2_FLOOR, 0.90, 3.15, Z_P2_FLOOR + 0.88)    # Mesón doblado y plancha

    # =========================================================================
    # 4. NUEVO TERCER PISO — OPCIÓN A (Z = +6.00 a +8.85 m):
    #    PLANTA PRIVADA FAMILIAR, MASTER PENTHOUSE, CLARABOYA Y TERRAZA BBQ SUR
    # =========================================================================
    L_P3_SLAB  = "P3_LOSA_STEELDECK_3D"
    L_P3_EXT   = "P3_MUROS_EXT_3D"
    L_P3_INT   = "P3_MUROS_INT_3D"
    L_P3_FURN  = "P3_MOBILIARIO_PRIVADO_3D"
    L_ROOF     = "CUBIERTA_CHALET_3D"
    L_GUTTER   = "CANALON_OCULTO_PROPIO_3D"
    L_SKYLIGHT = "CLARABOYA_VENTILADA_3D"

    # Losa Entrepiso Liviana Steel Deck de Piso 3 (Z: 5.85..6.00 m):
    # Deja únicamente el hueco de llegada de Escalera Tramo 3 en X = 0.30..1.45, Y = 4.40..7.40
    add_house_box(L_P3_SLAB, 8, 0.15, 0.00, H_P2, 9.15, 4.40, Z_P3_FLOOR)
    add_house_box(L_P3_SLAB, 8, 0.15, 4.40, H_P2, 0.30, 7.40, Z_P3_FLOOR)
    add_house_box(L_P3_SLAB, 8, 1.45, 4.40, H_P2, 9.15, 7.40, Z_P3_FLOOR)
    add_house_box(L_P3_SLAB, 8, 0.15, 7.40, H_P2, 9.15, Y_AV4, Z_P3_FLOOR)

    # Baranda de protección del desembarque en Piso 3 (deja libre la salida Norte en Y = 7.40)
    add_alpine_railing_y(1.52, 4.40, 7.35, Z_P3_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_x(0.32, 1.52, 4.38, Z_P3_FLOOR, h_rail=1.05, n_bays=1)

    # --- PARAPETO CORTAFUEGOS PROPIO Y CANALÓN OCULTO EN PISO 3 (CERO INVASIÓN X < 0.15 m) ---
    add_house_box(L_P3_EXT, 34, 0.15, 0.00, Z_P3_FLOOR, 0.30, 4.45, Z_PARAPET_BUH)
    add_house_box(L_P3_EXT, 34, 0.15, 4.45, Z_P3_FLOOR, 0.30, Y_AV4, Z_PARAPET_WEST)
    add_house_box(L_GUTTER, 8,  0.15, -ALERO_SUR, Z_PARAPET_BUH,  0.35, 4.45,  Z_PARAPET_BUH + 0.06)
    add_house_box(L_GUTTER, 8,  0.15,  4.45,      Z_PARAPET_WEST, 0.35, Y_AV4, Z_PARAPET_WEST + 0.06)
    add_house_box(L_GUTTER, 8,  0.30, -ALERO_SUR, 10.42, 0.55, 4.45, 10.48)
    add_house_box(L_GUTTER, 8,  0.50, -ALERO_SUR, 10.48, 0.56, 4.45, 10.62)
    add_house_box(L_GUTTER, 8,  0.30,  4.45,       8.82, 0.55, Y_AV4,  8.88)
    add_house_box(L_GUTTER, 8,  0.50,  4.45,       8.88, 0.56, Y_AV4,  9.02)
    add_house_box(L_GUTTER, 8,  0.32,  4.40,       8.88, 0.46, 4.52, 10.48)

    # --- GRAN TERRAZA CONTINUA MASTER PENTHOUSE SOBRE AVENIDA 4 (X: 0.30..9.00, Y: 19.60..21.56 = 17,05 m²) ---
    # Se elimina el muro pantalla exterior (X=4.35..4.50) unificando todo el frente Norte en una sola gran terraza
    # continua con acceso exclusivo desde el Dormitorio Master, y muro ciego sobre el Vestier para proteger la ropa del sol!
    add_alpine_railing_x(0.42, 2.68, Y_AV4 - 0.08, Z_P3_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_x(2.97, 5.80, Y_AV4 - 0.08, Z_P3_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_x(6.05, 8.95, Y_AV4 - 0.08, Z_P3_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_y(9.07, 19.60, Y_AV4 - 0.12, Z_P3_FLOOR, h_rail=1.05, n_bays=2)

    # Muro Frontal Retranqueado P3 (Y = 19.45..19.60):
    # - Tramo Oeste (X = 0.30..4.50): Muro bajo macizo (0,00..2,35 m) que respalda el clóset y protege la ropa +
    #   Ventana Alta Horizontal Clerestory (Opción 1: X = 0.95..3.65, H = 2,35..2,80 m = 2,70 x 0,45 m) con cristal UV!
    # - Tramo Este (X = 4.50..9.00): Gran Ventanal Corredizo Panorámico desde el Dormitorio Master hacia toda la terraza
    add_wall_with_openings_x(L_P3_EXT, 34, 0.30, 4.50, 19.45, 19.60, Z_P3_FLOOR, H_P3, [
        (0.95, 3.65, Z_P3_FLOOR + 2.35, Z_P3_FLOOR + 2.80),   # Ventana Alta Clerestory Vestier (2,70 x 0,45 m, cristal UV)
    ])
    # Carpintería de madera y cristal laminado filtro UV en la Ventana Alta Clerestory del Vestier (3 paños de 0,90 m)
    z_cl_bot, z_cl_top = Z_P3_FLOOR + 2.35, Z_P3_FLOOR + 2.80
    t_cl = 0.045
    add_house_box(L_CARP, 34, 0.95, 19.43, z_cl_bot,        3.65, 19.62, z_cl_bot + t_cl)          # Alféizar madera
    add_house_box(L_CARP, 34, 0.95, 19.43, z_cl_top - t_cl, 3.65, 19.62, z_cl_top)                 # Dintel madera
    add_house_box(L_CARP, 34, 0.95,        19.43, z_cl_bot + t_cl, 0.95 + t_cl, 19.62, z_cl_top - t_cl) # Jamba izq.
    add_house_box(L_CARP, 34, 3.65 - t_cl, 19.43, z_cl_bot + t_cl, 3.65,        19.62, z_cl_top - t_cl) # Jamba der.
    for xm_cl in [1.85, 2.75]:
        add_house_box(L_CARP, 34, xm_cl - 0.02, 19.46, z_cl_bot + t_cl, xm_cl + 0.02, 19.59, z_cl_top - t_cl)
    add_house_box(L_CARP, 4,  0.95 + t_cl, 19.51, z_cl_bot + t_cl, 3.65 - t_cl, 19.54, z_cl_top - t_cl) # Cristal UV

    add_wall_with_openings_x(L_P3_EXT, 34, 4.50, 9.00, 19.45, 19.60, Z_P3_FLOOR, H_P3, [
        (5.25, 8.45, Z_P3_FLOOR, Z_P3_FLOOR + 2.25),   # Gran Ventanal Corredizo Master Penthouse a la Terraza Continua
    ])
    # Marco de madera y hojas corredizas de cristal templado abiertas (paso franco X = 6.88..8.40 hacia la terraza)
    add_house_box(L_CARP, 34, 5.21, 19.43, Z_P3_FLOOR, 5.27, 19.62, Z_P3_FLOOR + 2.27)
    add_house_box(L_CARP, 34, 8.43, 19.43, Z_P3_FLOOR, 8.49, 19.62, Z_P3_FLOOR + 2.27)
    add_house_box(L_CARP, 34, 5.21, 19.43, Z_P3_FLOOR + 2.23, 8.49, 19.62, Z_P3_FLOOR + 2.29)
    add_house_box(L_CARP, 4,  5.27, 19.51, Z_P3_FLOOR + 0.03, 6.88, 19.55, Z_P3_FLOOR + 2.23)

    # --- FACHADA ESTE EN PISO 3 (X = 9.00..9.15, Y = 4.30..19.60): ABIERTA EN ESQUINA SURESTE PARA GRAN TERRAZA! ---
    east_windows_p3 = [
        (4.90,  5.85, Z_P3_FLOOR + 1.15, Z_P3_FLOOR + 2.05),  # Ventana Baño Familiar P3
        (7.35,  9.25, Z_P3_FLOOR + 0.90, Z_P3_FLOOR + 2.15),  # Ventanal Este Habitación 3
        (11.40, 13.45, Z_P3_FLOOR + 0.90, Z_P3_FLOOR + 2.15), # Ventanal Este Habitación 2
        (15.75, 18.45, Z_P3_FLOOR + 0.85, Z_P3_FLOOR + 2.25), # GRAN VENTANAL ESTE MASTER PENTHOUSE
    ]
    add_wall_with_openings_y(L_P3_EXT, 34, 9.00, 9.15, 4.30, 19.60, Z_P3_FLOOR, H_P3, east_windows_p3)
    for wy1, wy2, wz1, wz2 in east_windows_p3:
        add_rustic_window_east(wy1, wy2, wz1, wz2, with_shutters=(wy2 - wy1 >= 1.35))

    # --- GRAN TERRAZA MIRADOR & QUINCHO BBQ EN ESQUINA SURESTE ABIERTA (X = 2.90..9.15, Y = 0.00..4.30 = 26,88 m²) ---
    # Se elimina Habitación 4 del Piso 3 y se unifica toda la esquina Este+Sur bajo cubierta chalet con columnas negras!
    Z_GYM_CEIL = 8.50  # Altura libre Cuarto Apoyo/Gimnasio bajo Buhardilla de Tanques = 2,50 m
    add_wall_with_openings_x(L_P3_EXT, 34, 0.30, 2.90, 0.00, 0.15, Z_P3_FLOOR, Z_GYM_CEIL, [
        (0.85, 2.35, Z_P3_FLOOR + 1.00, Z_P3_FLOOR + 2.10),   # Ventana Cuarto Apoyo / Gimnasio
    ])
    add_rustic_window_south(0.85, 2.35, Z_P3_FLOOR + 1.00, Z_P3_FLOOR + 2.10, with_shutters=False)
    # Barandas Alpinas continuas en "L" sobre borde Sur (Y = 0.08) y borde Este (X = 9.07) respetando columnas negras:
    add_alpine_railing_x(2.96, 5.80, 0.08, Z_P3_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_x(6.05, 8.95, 0.08, Z_P3_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_y(9.07, 0.25, 3.45, Z_P3_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_y(9.07, 3.70, 4.30, Z_P3_FLOOR, h_rail=1.05, n_bays=1)

    # --- DISTRIBUCIÓN INTERIOR DEL TERCER PISO (CON ACCESOS VISIBLES A VESTIER Y BAÑO SPA) ---
    # 1. Master Penthouse Suite (Norte: Y = 12.80..19.45):
    #    - Dormitorio Master (X: 4.50..9.00, Y: 14.60..19.45 = 21,8 m²)
    #    - Gran Vestier Walk-In Doble en crujía Oeste (X: 0.30..4.35, Y: 16.05..19.45 = 13,7 m²)
    #    - Gran Baño Spa Master con Tina (X: 0.30..4.35, Y: 12.80..15.90 = 12,5 m²)
    add_wall_with_openings_y(L_P3_INT, 6, 4.35, 4.50, 12.80, 19.45, Z_P3_FLOOR, H_P3, [
        (14.70, 15.50, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),      # Puerta auxiliar Dormitorio <-> Baño Spa Master
        (17.05, 18.35, Z_P3_FLOOR, Z_P3_FLOOR + 2.20),        # GRAN PORTAL BARN DOOR (1,30 m) Dormitorio -> Vestier!
    ])
    # Riel de hierro negro visto + 2 hojas corredizas tipo Granero (Barn Door) ABIERTAS flanqueando el portal al Vestier:
    add_house_box(L_P3_COL, 8,  4.50, 16.15, Z_P3_FLOOR + 2.22, 4.56, 19.25, Z_P3_FLOOR + 2.28) # Riel hierro negro
    add_house_box(L_CARP,   34, 4.33, 17.00, Z_P3_FLOOR, 4.52, 17.06, Z_P3_FLOOR + 2.22)        # Jamba sur portal
    add_house_box(L_CARP,   34, 4.33, 18.34, Z_P3_FLOOR, 4.52, 18.40, Z_P3_FLOOR + 2.22)        # Jamba norte portal
    add_house_box(L_CARP,   30, 4.52, 16.22, Z_P3_FLOOR + 0.03, 4.58, 16.95, Z_P3_FLOOR + 2.18) # Hoja Barn Door Sur abierta
    add_house_box(L_CARP,   30, 4.52, 18.45, Z_P3_FLOOR + 0.03, 4.58, 19.18, Z_P3_FLOOR + 2.18) # Hoja Barn Door Norte abierta
    for ry_h in [16.35, 16.82, 18.58, 19.05]:
        add_house_box(L_P3_COL, 8, 4.51, ry_h - 0.03, Z_P3_FLOOR + 2.12, 4.59, ry_h + 0.03, Z_P3_FLOOR + 2.30)

    # Marco y hoja entreabierta de la Puerta Dormitorio <-> Baño Spa Master (Y = 14.70..15.50)
    add_house_box(L_CARP, 34, 4.33, 14.66, Z_P3_FLOOR, 4.52, 14.72, Z_P3_FLOOR + H_DOOR)
    add_house_box(L_CARP, 34, 4.33, 15.48, Z_P3_FLOOR, 4.52, 15.54, Z_P3_FLOOR + H_DOOR)
    add_house_hexa(L_CARP, 30, [
        (4.35, 14.72, Z_P3_FLOOR + 0.02), (4.40, 14.76, Z_P3_FLOOR + 0.02),
        (3.82, 14.22, Z_P3_FLOOR + 0.02), (3.78, 14.18, Z_P3_FLOOR + 0.02),
        (4.35, 14.72, Z_P3_FLOOR + H_DOOR - 0.02), (4.40, 14.76, Z_P3_FLOOR + H_DOOR - 0.02),
        (3.82, 14.22, Z_P3_FLOOR + H_DOOR - 0.02), (3.78, 14.18, Z_P3_FLOOR + H_DOOR - 0.02),
    ])

    # Puerta Principal Master Penthouse desde Family Room (Y = 14.45..14.60, X = 4.75..5.65)
    add_wall_with_openings_x(L_P3_INT, 6, 4.50, 9.00, 14.45, 14.60, Z_P3_FLOOR, H_P3, [
        (4.75, 5.65, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),
    ])
    add_house_box(L_CARP, 30, 4.75, 14.60, Z_P3_FLOOR + 0.02, 4.81, 15.42, Z_P3_FLOOR + H_DOOR - 0.02)

    # Tabique divisorio Vestier <-> Baño Spa CON PUERTA INTERNA VISIBLE ABIERTA A 45° (X = 1.65..2.50, Y = 15.90..16.05)!
    add_wall_with_openings_x(L_P3_INT, 6, 0.30, 4.35, 15.90, 16.05, Z_P3_FLOOR, H_P3, [
        (1.65, 2.50, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),        # Paso directo Vestier <-> Baño Spa Master
    ])
    add_house_box(L_CARP, 34, 1.60, 15.88, Z_P3_FLOOR, 1.66, 16.07, Z_P3_FLOOR + H_DOOR)
    add_house_box(L_CARP, 34, 2.49, 15.88, Z_P3_FLOOR, 2.55, 16.07, Z_P3_FLOOR + H_DOOR)
    add_house_hexa(L_CARP, 30, [
        (1.66, 16.05, Z_P3_FLOOR + 0.02), (1.71, 16.01, Z_P3_FLOOR + 0.02),
        (2.25, 16.58, Z_P3_FLOOR + 0.02), (2.20, 16.62, Z_P3_FLOOR + 0.02),
        (1.66, 16.05, Z_P3_FLOOR + H_DOOR - 0.02), (1.71, 16.01, Z_P3_FLOOR + H_DOOR - 0.02),
        (2.25, 16.58, Z_P3_FLOOR + H_DOOR - 0.02), (2.20, 16.62, Z_P3_FLOOR + H_DOOR - 0.02),
    ])
    add_house_box(L_P3_INT, 6, 0.30, 12.65, Z_P3_FLOOR, 4.50, 12.80, H_P3)  # Muro Sur Baño Spa / Norte Family Room

    # 2. Espina Este de Habitaciones Secundarias 2 y 3 + Baño Familiar (X = 5.85..6.00, Y = 4.30..14.45 — sin Hab. 4!)
    add_wall_with_openings_y(L_P3_INT, 6, 5.85, 6.00, 4.30, 14.45, Z_P3_FLOOR, H_P3, [
        (4.90,  5.70, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),       # Puerta Baño Familiar P3
        (7.10,  7.90, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),       # Puerta Habitación Secundaria 3
        (10.85, 11.65, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),      # Puerta Habitación Secundaria 2
    ])
    add_house_box(L_P3_INT, 6,  6.00, 10.15, Z_P3_FLOOR, 9.00, 10.30, H_P3)  # Div. Hab. 2 / Hab. 3
    add_house_box(L_P3_INT, 6,  6.00,  6.30, Z_P3_FLOOR, 9.00,  6.45, H_P3)  # Div. Hab. 3 / Baño Familiar
    add_house_box(L_P3_EXT, 34, 5.85,  4.30, Z_P3_FLOOR, 9.15,  4.45, H_P3)  # Muro Sur Baño Familiar hacia Gran Terraza

    # 3. Cierre acristalado hacia Gran Terraza Mirador Sur / BBQ (Y = 4.30..4.45, X = 2.90..5.85) + Cuarto Apoyo/Gym
    add_wall_with_openings_x(L_P3_EXT, 34, 2.90, 5.85, 4.30, 4.45, Z_P3_FLOOR, H_P3, [
        (3.35, 5.35, Z_P3_FLOOR, Z_P3_FLOOR + 2.25),          # Gran Puerta Corrediza Vidrio hacia Terraza Mirador
    ])
    add_house_box(L_CARP, 4, 3.38, 4.36, Z_P3_FLOOR + 0.04, 4.38, 4.40, Z_P3_FLOOR + 2.22)
    add_house_box(L_P3_INT, 6, 2.75, 0.00, Z_P3_FLOOR, 2.90, 4.45, Z_GYM_CEIL)
    add_wall_with_openings_x(L_P3_INT, 6, 0.30, 2.75, 4.10, 4.25, Z_P3_FLOOR, Z_GYM_CEIL, [
        (1.65, 2.48, Z_P3_FLOOR, Z_P3_FLOOR + H_DOOR),        # Puerta Cuarto Apoyo / Gym / Subida Tanques
    ])
    # Clóset de Blancos en el descanso paralelo a escalera (X: 1.65..2.65, Y: 5.20..6.35)
    add_house_box(L_P3_FURN, 34, 1.65, 5.20, Z_P3_FLOOR, 2.35, 6.35, Z_P3_FLOOR + 2.20)

    # --- INTERIORISMO Y MOBILIARIO 3D DEL NUEVO TERCER PISO ---
    # A. Dormitorio Master Penthouse + Gran Terraza Continua Unificada (Lounge Este + Rincón Lectura/Café Oeste)
    add_house_box(L_P3_FURN, 34, 6.20, 20.30, Z_P3_FLOOR, 8.20, 21.15, Z_P3_FLOOR + 0.45)   # Lounge Este terraza Master
    add_house_box(L_P3_FURN, 30, 0.90, 20.15, Z_P3_FLOOR, 1.65, 20.95, Z_P3_FLOOR + 0.44)   # Poltrona exterior Oeste 1
    add_house_box(L_P3_FURN, 30, 2.45, 20.15, Z_P3_FLOOR, 3.20, 20.95, Z_P3_FLOOR + 0.44)   # Poltrona exterior Oeste 2
    add_house_box(L_P3_FURN, 34, 1.78, 20.25, Z_P3_FLOOR, 2.32, 20.80, Z_P3_FLOOR + 0.48)   # Mesita café terraza Oeste
    add_house_box(L_P3_FURN, 34, 5.75, 14.62, Z_P3_FLOOR, 8.65, 14.74, Z_P3_FLOOR + 2.25)   # Cabecero madera en muro Sur
    add_house_box(L_P3_FURN, 30, 6.20, 14.74, Z_P3_FLOOR, 8.20, 16.78, Z_P3_FLOOR + 0.58)   # Cama King mirando al Norte!
    add_house_box(L_P3_FURN, 34, 5.65, 14.74, Z_P3_FLOOR, 6.12, 15.22, Z_P3_FLOOR + 0.52)   # Mesa noche Oeste
    add_house_box(L_P3_FURN, 34, 8.28, 14.74, Z_P3_FLOOR, 8.75, 15.22, Z_P3_FLOOR + 0.52)   # Mesa noche Este
    add_house_box(L_P3_FURN, 34, 8.25, 17.65, Z_P3_FLOOR, 8.88, 18.65, Z_P3_FLOOR + 0.65)   # Poltrona lectura junto ventana Este

    # B. Gran Vestier Walk-In Doble (X: 0.30..4.35, Y: 16.05..19.45) + Gran Baño Spa con Tina (Y: 12.80..15.90)
    add_house_box(L_P3_FURN, 34, 0.34, 16.12, Z_P3_FLOOR, 0.92, 19.35, Z_P3_FLOOR + 2.30)   # Ebanistería Oeste Vestier
    add_house_box(L_P3_FURN, 34, 0.95, 18.85, Z_P3_FLOOR, 3.65, 19.38, Z_P3_FLOOR + 2.30)   # Ebanistería Norte Vestier
    add_house_box(L_P3_FURN, 34, 3.72, 16.12, Z_P3_FLOOR, 4.30, 16.95, Z_P3_FLOOR + 2.30)   # Módulo Este Sur (libre portal!)
    add_house_box(L_P3_FURN, 34, 3.72, 18.45, Z_P3_FLOOR, 4.30, 19.35, Z_P3_FLOOR + 2.30)   # Módulo Este Norte (libre portal!)
    add_house_box(L_P3_FURN, 30, 1.85, 17.25, Z_P3_FLOOR, 2.65, 18.25, Z_P3_FLOOR + 0.48)   # Isla/Pouf central Vestier
    # Baño Spa Master: Tina Exenta (Freestanding Tub) + Ducha Doble + Tocador Doble (despeja puerta Y=15.90!)
    add_house_box(L_P3_FURN, 7,  0.50, 14.20, Z_P3_FLOOR, 1.32, 15.72, Z_P3_FLOOR + 0.62)   # Tina exenta escultural
    add_house_box(L_P3_FURN, 8,  0.35, 12.85, Z_P3_FLOOR, 1.75, 13.95, Z_P3_FLOOR + 0.06)   # Plato ducha doble pizarra
    add_house_box(L_P3_FURN, 4,  1.72, 12.85, Z_P3_FLOOR + 0.06, 1.76, 13.95, Z_P3_FLOOR + 2.10)
    add_house_box(L_P3_FURN, 34, 2.62, 15.32, Z_P3_FLOOR, 4.22, 15.88, Z_P3_FLOOR + 0.85)   # Tocador doble lavamanos
    add_house_box(L_P3_FURN, 7,  2.55, 12.85, Z_P3_FLOOR, 3.05, 13.48, Z_P3_FLOOR + 0.42)   # WC Master

    # C. Family Room / Sala de Cine Íntima + Coffee Bar Nocturno (X: 0.30..5.80, Y: 7.50..12.65)
    add_house_box(L_P3_FURN, 30, 2.55, 9.35,  Z_P3_FLOOR, 3.55, 12.15, Z_P3_FLOOR + 0.44)   # Gran Sofá Cinema en L
    add_house_box(L_P3_FURN, 30, 1.45, 11.25, Z_P3_FLOOR, 2.55, 12.15, Z_P3_FLOOR + 0.44)
    add_house_box(L_P3_FURN, 34, 1.55, 9.85,  Z_P3_FLOOR, 2.25, 10.85, Z_P3_FLOOR + 0.40)   # Mesa centro cine
    add_house_box(L_P3_FURN, 34, 0.34, 9.45,  Z_P3_FLOOR, 0.85, 12.10, Z_P3_FLOOR + 0.55)   # Consola Cine en muro Oeste
    add_house_box(L_P3_FURN, 8,  0.36, 9.75,  Z_P3_FLOOR + 0.80, 0.42, 11.80, Z_P3_FLOOR + 1.92) # Pantalla Cine 85"
    add_house_box(L_P3_FURN, 34, 0.34, 7.65,  Z_P3_FLOOR, 0.88, 9.10,  Z_P3_FLOOR + 0.90)   # Coffee Bar + Minibar nocturno

    # D. Habitaciones Secundarias 2 y 3 + Baño Familiar P3 + GRAN TERRAZA MIRADOR & QUINCHO BBQ EN ESQUINA (26,88 m²)
    for by_bed, cy_cl in [(11.65, 13.85), (7.65, 9.55)]:
        add_house_box(L_P3_FURN, 30, 6.08, by_bed, Z_P3_FLOOR, 7.95, by_bed + 1.45, Z_P3_FLOOR + 0.55)  # Cama matrimonial
        add_house_box(L_P3_FURN, 34, 6.25, cy_cl,  Z_P3_FLOOR, 8.40, cy_cl + 0.55,  Z_P3_FLOOR + 2.20)  # Clóset
    add_house_box(L_P3_FURN, 8,  7.95, 4.48, Z_P3_FLOOR, 8.95, 6.25, Z_P3_FLOOR + 0.06)     # Ducha Baño Familiar P3
    add_house_box(L_P3_FURN, 34, 6.10, 5.70, Z_P3_FLOOR, 7.45, 6.26, Z_P3_FLOOR + 0.85)     # Tocador doble Baño P3
    add_house_box(L_P3_FURN, 7,  6.95, 4.48, Z_P3_FLOOR, 7.42, 5.08, Z_P3_FLOOR + 0.42)     # WC Baño P3
    # Equipamiento Gran Terraza Mirador Sur-Este (Barra Parrillera adosada al muro hidrosanitario + Comedor 8p + Lounge)
    add_house_box(L_P3_FURN, 8,  6.20, 3.65, Z_P3_FLOOR, 8.65, 4.28, Z_P3_FLOOR + 0.92)     # Barra Parrillera / BBQ piedra
    add_house_box(L_P3_FURN, 7,  6.35, 3.75, Z_P3_FLOOR + 0.92, 7.05, 4.18, Z_P3_FLOOR + 0.96) # Fregadero auxiliar terraza
    add_house_box(L_P3_FURN, 8,  7.45, 3.68, Z_P3_FLOOR + 0.92, 8.48, 4.25, Z_P3_FLOOR + 1.15) # Parrillera acero/carbón
    add_house_box(L_P3_FURN, 8,  7.55, 3.72, Z_P3_FLOOR + 1.85, 8.40, 4.26, Z_P3_FLOOR + 2.45) # Campana quincho negro
    add_house_box(L_P3_FURN, 34, 3.45, 1.35, Z_P3_FLOOR, 5.45, 2.40, Z_P3_FLOOR + 0.76)     # Comedor exterior 8 puestos
    add_house_box(L_P3_FURN, 30, 3.55, 0.85, Z_P3_FLOOR, 5.35, 1.22, Z_P3_FLOOR + 0.45)     # Banca sur comedor
    add_house_box(L_P3_FURN, 30, 3.55, 2.52, Z_P3_FLOOR, 5.35, 2.88, Z_P3_FLOOR + 0.45)     # Banca norte comedor
    add_house_box(L_P3_FURN, 30, 6.55, 0.55, Z_P3_FLOOR, 8.60, 1.32, Z_P3_FLOOR + 0.42)     # Sofá Lounge Mirador Sur
    add_house_box(L_P3_FURN, 30, 7.85, 1.32, Z_P3_FLOOR, 8.60, 2.45, Z_P3_FLOOR + 0.42)     # Sofá Lounge Mirador Este
    add_house_box(L_P3_FURN, 34, 6.75, 1.55, Z_P3_FLOOR, 7.55, 2.25, Z_P3_FLOOR + 0.38)     # Mesa baja mirador

    # =========================================================================
    # 4B. BUHARDILLA TÉCNICA ELEVADA EN PISO 3 (Z = +8.68 m):
    #     RESERVA AMPLIADA DE 2 TANQUES VERTICALES (2 x 1.000 L = 2.000 L) + BOMBA
    # =========================================================================
    L_TANK_SLAB = "P3_LOSA_TANQUES_3D"
    L_MAINT_ST  = "P3_ESCALERA_TANQUES_3D"
    L_HYDRO     = "EQUIPO_HIDRONEUMATICO_2000L_3D"
    L_DORMER    = "BUHARDILLA_TECNICA_P3_3D"

    Z_TANK_FLOOR = 8.68   # Losa portante de 18 cm (Z: 8.50..8.68 m) sobre Cuarto Apoyo/Gimnasio P3
    add_house_box(L_TANK_SLAB, 8, 0.30, 0.00, Z_GYM_CEIL, 2.90, 2.55, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 0.30, 3.70, Z_GYM_CEIL, 2.90, 4.40, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 0.30, 2.55, Z_GYM_CEIL, 0.38, 3.70, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 1.18, 2.55, Z_GYM_CEIL, 2.90, 3.70, Z_TANK_FLOOR)

    # Escalera Fija Inclinada desde Cuarto Apoyo P3 (Z=6.00) hacia Buhardilla (Z=8.68)
    num_m_steps = 9
    for sx1, sx2 in [(0.40, 0.45), (1.05, 1.10)]:
        add_house_hexa(L_MAINT_ST, 30, [
            (sx1, 2.55, Z_P3_FLOOR),   (sx2, 2.55, Z_P3_FLOOR),
            (sx2, 2.65, Z_P3_FLOOR),   (sx1, 2.65, Z_P3_FLOOR),
            (sx1, 3.60, Z_TANK_FLOOR), (sx2, 3.60, Z_TANK_FLOOR),
            (sx2, 3.70, Z_TANK_FLOOR), (sx1, 3.70, Z_TANK_FLOOR),
        ])
    for ms in range(1, num_m_steps + 1):
        frac = ms / (num_m_steps + 1)
        ym_c = 2.60 + frac * (3.65 - 2.60)
        zm_c = Z_P3_FLOOR + frac * (Z_TANK_FLOOR - Z_P3_FLOOR)
        add_house_box(L_MAINT_ST, 30, 0.45, ym_c - 0.09, zm_c - 0.04, 1.05, ym_c + 0.09, zm_c)
    # BARANDA GUARDA-ESCOTILLA REORIENTADA EN "L" (protege caída Sur Y=2.50 y mitad Sureste Y=2.50..3.05,
    # dejando 100% LIBRE el desembarque Este Y=3.05..4.25 para bajarse cómodamente hacia los tanques!):
    add_alpine_railing_x(0.38, 1.25, 2.50, Z_TANK_FLOOR, h_rail=1.00, n_bays=1)
    add_alpine_railing_y(1.24, 2.50, 3.05, Z_TANK_FLOOR, h_rail=1.00, n_bays=1)
    add_house_box(L_BALC, 30, 1.12, 3.66, Z_TANK_FLOOR, 1.18, 3.72, Z_TANK_FLOOR + 1.05)  # Poste agarre desembarque

    # 2 Tanques Verticales Interconectados de 1.000 L c/u (Total = 2.000 L, Ø 1,00 m x H = 1,30 m)
    TANK_R     = 0.50
    Z_TANK_BOT = Z_TANK_FLOOR + 0.12  # 8.80 m
    Z_TANK_SHO = Z_TANK_BOT + 1.18    # 9.98 m
    Z_TANK_TOP = Z_TANK_BOT + 1.30    # 10.10 m
    N_SEG      = 12
    tank_centers = [(1.55, 0.82), (1.55, 1.98)]
    add_house_box(L_TANK_SLAB, 8, 0.95, 0.22, Z_TANK_FLOOR, 2.15, 2.55, Z_TANK_FLOOR + 0.12)  # Pedestal doble
    for tcx, tcy in tank_centers:
        for s_i in range(N_SEG):
            a0 = 2.0 * math.pi * s_i / N_SEG
            a1 = 2.0 * math.pi * (s_i + 1) / N_SEG
            xo0, yo0 = tcx + TANK_R * math.cos(a0), tcy + TANK_R * math.sin(a0)
            xo1, yo1 = tcx + TANK_R * math.cos(a1), tcy + TANK_R * math.sin(a1)
            xi0, yi0 = tcx + 0.20 * math.cos(a0), tcy + 0.20 * math.sin(a0)
            xi1, yi1 = tcx + 0.20 * math.cos(a1), tcy + 0.20 * math.sin(a1)
            add_house_hexa(L_HYDRO, 5, [
                (tcx, tcy, Z_TANK_BOT), (xo0, yo0, Z_TANK_BOT), (xo1, yo1, Z_TANK_BOT), (tcx, tcy, Z_TANK_BOT),
                (tcx, tcy, Z_TANK_SHO), (xo0, yo0, Z_TANK_SHO), (xo1, yo1, Z_TANK_SHO), (tcx, tcy, Z_TANK_SHO),
            ])
            add_house_hexa(L_HYDRO, 5, [
                (tcx, tcy, Z_TANK_SHO), (xo0, yo0, Z_TANK_SHO), (xo1, yo1, Z_TANK_SHO), (tcx, tcy, Z_TANK_SHO),
                (tcx, tcy, Z_TANK_TOP), (xi0, yi0, Z_TANK_TOP), (xi1, yi1, Z_TANK_TOP), (tcx, tcy, Z_TANK_TOP),
            ])
    # Bomba Hidroneumática + Pulmón + Manifold interconexión (X: 1.85..2.70, Y: 2.70..3.65)
    add_house_box(L_HYDRO, 5, 1.95, 2.75, Z_TANK_FLOOR + 0.10, 2.32, 3.15, Z_TANK_FLOOR + 0.45)
    add_house_box(L_HYDRO, 1, 2.36, 2.75, Z_TANK_FLOOR + 0.10, 2.68, 3.15, Z_TANK_FLOOR + 0.72)
    add_house_box(L_HYDRO, 8, 2.08, 0.80, Z_TANK_FLOOR + 0.22, 2.16, 2.95, Z_TANK_FLOOR + 0.28)

    # Envolvente y Cubierta de Buhardilla Técnica P3 (Shed Dormer acoplado al faldón Oeste de P3)
    DORM_SLOPE = 0.15
    def z_dormer_under(x):
        return 10.56 + (x - 0.40) * DORM_SLOPE

    X_DORM_JOIN = (10.56 - 0.40 * DORM_SLOPE - (Z_GUTTER_EAVE - X_GUTTER_IN * SLOPE_TAN)) / (SLOPE_TAN - DORM_SLOPE)
    Z_DORM_JOIN = z_roof_under(X_DORM_JOIN)

    add_house_hexa(L_DORMER, 34, [
        (2.75, 0.00, Z_TANK_FLOOR), (2.90, 0.00, Z_TANK_FLOOR),
        (2.90, 4.40, Z_TANK_FLOOR), (2.75, 4.40, Z_TANK_FLOOR),
        (2.75, 0.00, z_dormer_under(2.75)), (2.90, 0.00, z_dormer_under(2.90)),
        (2.90, 4.40, z_dormer_under(2.90)), (2.75, 4.40, z_dormer_under(2.75)),
    ])
    add_house_hexa(L_DORMER, 34, [
        (0.30, 4.25, Z_TANK_FLOOR), (2.90, 4.25, Z_TANK_FLOOR),
        (2.90, 4.45, Z_TANK_FLOOR), (0.30, 4.45, Z_TANK_FLOOR),
        (0.30, 4.25, z_dormer_under(0.30)), (2.90, 4.25, z_dormer_under(2.90)),
        (2.90, 4.45, z_dormer_under(2.90)), (0.30, 4.45, z_dormer_under(0.30)),
    ])
    add_wall_with_openings_x(L_DORMER, 34, 0.30, 2.90, 0.00, 0.15, Z_TANK_FLOOR, 10.56, [
        (0.88, 2.33, 8.90, 10.35),
    ])
    add_house_hexa(L_ROOF, 9, [
        (0.40,        -ALERO_SUR, z_dormer_under(0.40)),       (X_DORM_JOIN, -ALERO_SUR, Z_DORM_JOIN),
        (X_DORM_JOIN,  4.45,      Z_DORM_JOIN),                (0.40,         4.45,      z_dormer_under(0.40)),
        (0.40,        -ALERO_SUR, z_dormer_under(0.40) + 0.16),(X_DORM_JOIN, -ALERO_SUR, Z_DORM_JOIN + 0.16),
        (X_DORM_JOIN,  4.45,      Z_DORM_JOIN + 0.16),         (0.40,         4.45,      z_dormer_under(0.40) + 0.16),
    ])

    # =========================================================================
    # 4C. CUBIERTA ALPINA 32° CON ABERTURA REAL (3,10 x 5,80 m) BAJO CLARABOYA VENTILADA
    # =========================================================================
    # Hastial interior sobre cierre de Terraza Sur (Y = 4.30..4.45) + Hastial Norte (Y = 19.45..19.60)
    # (Deja el techo de la Gran Terraza Mirador Y = 0.00..4.30 abierto en madera vista!)
    add_house_hexa(L_P3_EXT, 34, [
        (2.90, 4.30, H_P3), (X_DORM_JOIN, 4.30, H_P3), (X_DORM_JOIN, 4.45, H_P3), (2.90, 4.45, H_P3),
        (2.90, 4.30, z_dormer_under(2.90)), (X_DORM_JOIN, 4.30, Z_DORM_JOIN),
        (X_DORM_JOIN, 4.45, Z_DORM_JOIN),   (2.90, 4.45, z_dormer_under(2.90)),
    ])
    add_house_hexa(L_P3_EXT, 34, [
        (X_DORM_JOIN, 4.30, H_P3), (X_RIDGE, 4.30, H_P3), (X_RIDGE, 4.45, H_P3), (X_DORM_JOIN, 4.45, H_P3),
        (X_DORM_JOIN, 4.30, Z_DORM_JOIN), (X_RIDGE, 4.30, Z_RIDGE),
        (X_RIDGE, 4.45, Z_RIDGE),         (X_DORM_JOIN, 4.45, Z_DORM_JOIN),
    ])
    add_house_hexa(L_P3_EXT, 34, [
        (X_RIDGE, 4.30, H_P3), (9.15, 4.30, H_P3), (9.15, 4.45, H_P3), (X_RIDGE, 4.45, H_P3),
        (X_RIDGE, 4.30, Z_RIDGE), (9.15, 4.30, z_roof_under(9.15)),
        (9.15, 4.45, z_roof_under(9.15)), (X_RIDGE, 4.45, Z_RIDGE),
    ])
    add_house_hexa(L_P3_EXT, 34, [
        (0.45, 19.45, H_P3), (X_RIDGE, 19.45, H_P3), (X_RIDGE, 19.60, H_P3), (0.45, 19.60, H_P3),
        (0.45, 19.45, z_roof_under(0.45)), (X_RIDGE, 19.45, Z_RIDGE),
        (X_RIDGE, 19.60, Z_RIDGE),         (0.45, 19.60, z_roof_under(0.45)),
    ])
    add_house_hexa(L_P3_EXT, 34, [
        (X_RIDGE, 19.45, H_P3), (9.15, 19.45, H_P3), (9.15, 19.60, H_P3), (X_RIDGE, 19.60, H_P3),
        (X_RIDGE, 19.45, Z_RIDGE), (9.15, 19.45, z_roof_under(9.15)),
        (9.15, 19.60, z_roof_under(9.15)), (X_RIDGE, 19.60, Z_RIDGE),
    ])

    # Coordenadas exactas de la PERFORACIÓN REAL DE TECHO bajo la Claraboya Ventilada:
    X_SKY_W, X_SKY_E = 2.45, 5.55
    Y_SKY_S, Y_SKY_N = 5.50, 11.30
    y_roof_s = -ALERO_SUR
    y_roof_n = Y_AV4
    z_w_bot  = z_roof_under(0.40)
    z_sky_w  = z_roof_under(X_SKY_W)
    z_sky_e  = z_roof_under(X_SKY_E)

    # Cerchas Alpinas Vistas (con cerchas cabeceras en Y=5.35 y Y=11.30 flanqueando el hueco de claraboya!)
    for ty in [21.56, 16.30, 11.30, 5.35, 0.00, -0.85]:
        ty2 = ty + 0.15
        x_tie_start = 2.90 if ty < 4.30 else 0.45
        add_house_box(L_TIMBER, 34, x_tie_start, ty, H_P3 - 0.18, 9.15, ty2, H_P3)
        add_house_box(L_TIMBER, 34, X_RIDGE - 0.09, ty, H_P3, X_RIDGE + 0.09, ty2, Z_RIDGE - 0.05)
    # Viga cumbrera cortada limpiamente en Y = 5.50..11.30 para dejar 100% libre el pozo de luz y aire!
    add_house_box(L_TIMBER, 34, X_RIDGE - 0.08, -ALERO_SUR, Z_RIDGE - 0.22, X_RIDGE + 0.08, Y_SKY_S, Z_RIDGE)
    add_house_box(L_TIMBER, 34, X_RIDGE - 0.08, Y_SKY_N,    Z_RIDGE - 0.22, X_RIDGE + 0.08, Y_AV4,   Z_RIDGE)

    def add_roof_panel(xa, xb, ya, yb, za, zb):
        add_house_hexa(L_ROOF, 9, [
            (xa, ya, za),              (xb, ya, zb),
            (xb, yb, zb),              (xa, yb, za),
            (xa, ya, za + ROOF_THICK), (xb, ya, zb + ROOF_THICK),
            (xb, yb, zb + ROOF_THICK), (xa, yb, za + ROOF_THICK),
        ])

    # Faldón Oeste subdividido en paños alrededor del hueco real (X = 2.45..4.85, Y = 5.50..11.30 ABIERTO!)
    add_roof_panel(0.40,        X_SKY_W, 4.45,     y_roof_n, z_w_bot,     z_sky_w)   # Paño Oeste exterior continuo
    add_roof_panel(X_SKY_W,     X_RIDGE, 4.45,     Y_SKY_S,  z_sky_w,     Z_RIDGE)   # Paño Oeste al Sur del hueco
    add_roof_panel(X_SKY_W,     X_RIDGE, Y_SKY_N,  y_roof_n, z_sky_w,     Z_RIDGE)   # Paño Oeste al Norte del hueco
    add_roof_panel(X_DORM_JOIN, X_RIDGE, y_roof_s, 4.45,     Z_DORM_JOIN, Z_RIDGE)   # Paño Sur junto a Buhardilla

    # Faldón Este subdividido en paños alrededor del hueco real (X = 4.85..5.55, Y = 5.50..11.30 ABIERTO!)
    add_roof_panel(X_SKY_E, X_EAVE_EAST, y_roof_s, y_roof_n, z_sky_e, Z_EAVE_EAST)   # Paño Este exterior continuo
    add_roof_panel(X_RIDGE, X_SKY_E,     y_roof_s, Y_SKY_S,  Z_RIDGE, z_sky_e)       # Paño Este al Sur del hueco
    add_roof_panel(X_RIDGE, X_SKY_E,     Y_SKY_N,  y_roof_n, Z_RIDGE, z_sky_e)       # Paño Este al Norte del hueco

    # --- LINTERNA / CLARABOYA CENTRAL CON ANILLO METÁLICO, VIDRIO TRANSPARENTE Y CELOSÍAS ABIERTAS DE AIRE ---
    Z_GLASS_TOP = Z_RIDGE + 0.22
    Z_LOUV_TOP  = Z_RIDGE + 0.62
    Z_SKY_TOP   = Z_RIDGE + 0.90
    # 1. Anillo estructural perimetral de acero negro enmarcando el corte real de cubierta
    add_house_box(L_P3_COL, 8, X_SKY_W - 0.08, Y_SKY_S - 0.08, z_sky_w - 0.14, X_SKY_W,        Y_SKY_N + 0.08, z_sky_w + ROOF_THICK + 0.06)
    add_house_box(L_P3_COL, 8, X_SKY_E,        Y_SKY_S - 0.08, z_sky_e - 0.14, X_SKY_E + 0.08, Y_SKY_N + 0.08, z_sky_e + ROOF_THICK + 0.06)
    for y_curb1, y_curb2 in [(Y_SKY_S - 0.08, Y_SKY_S), (Y_SKY_N, Y_SKY_N + 0.08)]:
        add_house_hexa(L_P3_COL, 8, [
            (X_SKY_W, y_curb1, z_sky_w - 0.12), (X_RIDGE, y_curb1, Z_RIDGE - 0.12),
            (X_RIDGE, y_curb2, Z_RIDGE - 0.12), (X_SKY_W, y_curb2, z_sky_w - 0.12),
            (X_SKY_W, y_curb1, Z_GLASS_TOP),    (X_RIDGE, y_curb1, Z_GLASS_TOP),
            (X_RIDGE, y_curb2, Z_GLASS_TOP),    (X_SKY_W, y_curb2, Z_GLASS_TOP),
        ])
        add_house_hexa(L_P3_COL, 8, [
            (X_RIDGE, y_curb1, Z_RIDGE - 0.12), (X_SKY_E, y_curb1, z_sky_e - 0.12),
            (X_SKY_E, y_curb2, z_sky_e - 0.12), (X_RIDGE, y_curb2, Z_RIDGE - 0.12),
            (X_RIDGE, y_curb1, Z_GLASS_TOP),    (X_SKY_E, y_curb1, Z_GLASS_TOP),
            (X_SKY_E, y_curb2, Z_GLASS_TOP),    (X_RIDGE, y_curb2, Z_GLASS_TOP),
        ])
    # 2. Montantes verticales de hierro negro soportando la tapa elevada
    for py_s in [Y_SKY_S, 7.43, 9.37, Y_SKY_N]:
        add_house_box(L_P3_COL, 8, X_SKY_W - 0.07, py_s - 0.04, z_sky_w + ROOF_THICK, X_SKY_W,        py_s + 0.04, Z_LOUV_TOP)
        add_house_box(L_P3_COL, 8, X_SKY_E,        py_s - 0.04, z_sky_e + ROOF_THICK, X_SKY_E + 0.07, py_s + 0.04, Z_LOUV_TOP)
    # 3. Ventanales laterales de vidrio transparente (entrada directa de luz solar al hueco)
    add_house_box(L_SKYLIGHT, 4, X_SKY_W - 0.04, Y_SKY_S + 0.04, z_sky_w + ROOF_THICK + 0.04, X_SKY_W - 0.01, Y_SKY_N - 0.04, Z_GLASS_TOP)
    add_house_box(L_SKYLIGHT, 4, X_SKY_E + 0.01, Y_SKY_S + 0.04, z_sky_e + ROOF_THICK + 0.04, X_SKY_E + 0.04, Y_SKY_N - 0.04, Z_GLASS_TOP)
    # 4. Celosías inclinadas cortaviento CON ABERTURAS REALES DE AIRE (efecto chimenea térmica sin entrada de lluvia)
    for zl_b in [Z_GLASS_TOP + 0.08, Z_GLASS_TOP + 0.21, Z_GLASS_TOP + 0.34]:
        add_house_hexa(L_SKYLIGHT, 8, [
            (X_SKY_W - 0.12, Y_SKY_S, zl_b - 0.03), (X_SKY_W,        Y_SKY_S, zl_b + 0.03),
            (X_SKY_W,        Y_SKY_N, zl_b + 0.03), (X_SKY_W - 0.12, Y_SKY_N, zl_b - 0.03),
            (X_SKY_W - 0.12, Y_SKY_S, zl_b - 0.01), (X_SKY_W,        Y_SKY_S, zl_b + 0.05),
            (X_SKY_W,        Y_SKY_N, zl_b + 0.05), (X_SKY_W - 0.12, Y_SKY_N, zl_b - 0.01),
        ])
        add_house_hexa(L_SKYLIGHT, 8, [
            (X_SKY_E,        Y_SKY_S, zl_b + 0.03), (X_SKY_E + 0.12, Y_SKY_S, zl_b - 0.03),
            (X_SKY_E + 0.12, Y_SKY_N, zl_b - 0.03), (X_SKY_E,        Y_SKY_N, zl_b + 0.03),
            (X_SKY_E,        Y_SKY_S, zl_b + 0.05), (X_SKY_E + 0.12, Y_SKY_S, zl_b - 0.01),
            (X_SKY_E + 0.12, Y_SKY_N, zl_b - 0.01), (X_SKY_E,        Y_SKY_N, zl_b + 0.05),
        ])
    # 5. Cubierta superior a dos aguas de la linterna con aleros protectores de 40 cm
    X_SKY_MID = 0.5 * (X_SKY_W + X_SKY_E)
    add_house_hexa(L_SKYLIGHT, 9, [
        (X_SKY_W - 0.40, Y_SKY_S - 0.35, Z_LOUV_TOP),        (X_SKY_MID,      Y_SKY_S - 0.35, Z_SKY_TOP - 0.10),
        (X_SKY_MID,      Y_SKY_N + 0.35, Z_SKY_TOP - 0.10),  (X_SKY_W - 0.40, Y_SKY_N + 0.35, Z_LOUV_TOP),
        (X_SKY_W - 0.40, Y_SKY_S - 0.35, Z_LOUV_TOP + 0.10), (X_SKY_MID,      Y_SKY_S - 0.35, Z_SKY_TOP),
        (X_SKY_MID,      Y_SKY_N + 0.35, Z_SKY_TOP),         (X_SKY_W - 0.40, Y_SKY_N + 0.35, Z_LOUV_TOP + 0.10),
    ])
    add_house_hexa(L_SKYLIGHT, 9, [
        (X_SKY_MID,      Y_SKY_S - 0.35, Z_SKY_TOP - 0.10),  (X_SKY_E + 0.40, Y_SKY_S - 0.35, Z_LOUV_TOP),
        (X_SKY_E + 0.40, Y_SKY_N + 0.35, Z_LOUV_TOP),        (X_SKY_MID,      Y_SKY_N + 0.35, Z_SKY_TOP - 0.10),
        (X_SKY_MID,      Y_SKY_S - 0.35, Z_SKY_TOP),         (X_SKY_E + 0.40, Y_SKY_S - 0.35, Z_LOUV_TOP + 0.10),
        (X_SKY_E + 0.40, Y_SKY_N + 0.35, Z_LOUV_TOP + 0.10), (X_SKY_MID,      Y_SKY_N + 0.35, Z_SKY_TOP),
    ])

    # Canecillos vistos bajo Alero Este Propio de P3 (X: 9.00..10.10)
    num_rafters = 19
    rafter_dy = (y_roof_n - y_roof_s - 0.12) / (num_rafters - 1)
    z_raf_in  = z_roof_under(9.00)
    for r in range(num_rafters):
        ry1 = y_roof_s + r * rafter_dy
        ry2 = ry1 + 0.10
        add_house_hexa(L_TIMBER, 34, [
            (9.00,        ry1, z_raf_in - 0.14),    (X_EAVE_EAST, ry1, Z_EAVE_EAST - 0.14),
            (X_EAVE_EAST, ry2, Z_EAVE_EAST - 0.14), (9.00,        ry2, z_raf_in - 0.14),
            (9.00,        ry1, z_raf_in),           (X_EAVE_EAST, ry1, Z_EAVE_EAST),
            (X_EAVE_EAST, ry2, Z_EAVE_EAST),        (9.00,        ry2, z_raf_in),
        ])

    # =========================================================================
    # 5. TERRENO POLIGONAL UTM + RAMPA LOGÍSTICA CONTINUA DESDE PUERTA DER. AV.4
    # =========================================================================
    L_TERR  = "TERRENO_3D"
    L_FENCE = "CERCA_PERIMETRAL_3D"
    L_RAMP  = "RAMPA_BODEGA_AV4_3D"

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
            (x_left_b,  y_b, z_bot_b), (x_right_b, y_b, z_bot_b),
            (x_right_f, y_f, z_bot_f), (x_left_f,  y_f, z_bot_f),
            (x_left_b,  y_b, z_top_b), (x_right_b, y_b, z_top_b),
            (x_right_f, y_f, z_top_f), (x_left_f,  y_f, z_top_f),
        ])

    # Patio Trasero a cota Sótano Bodega (Z = -2.55 m, Y_terreno = 0.00..3.00 m)
    y_sot_start = OFFSET_Y
    add_hexahedron(L_TERR, 3, [
        (0.00, y_rear(0.00), Z_SOT_FLOOR - 0.20), (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR - 0.20),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR - 0.20), (0.00, y_sot_start, Z_SOT_FLOOR - 0.20),
        (0.00, y_rear(0.00), Z_SOT_FLOOR),        (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR),        (0.00, y_sot_start, Z_SOT_FLOOR),
    ])

    # CORREDOR / RAMPA LOGÍSTICA CONTINUA EN RETIRO DERECHO (X = 9.15..x_right(y)):
    # Desciende suavemente sin escalones desde la Puerta Derecha de Av. 4 (Y_terr = 24.71, Z = 0.00)
    # pasando por descanso plano inicial (Y_casa = 19.50..21.71) y rampa continua (Y_casa = 19.50 -> 5.50,
    # pendiente ~18% apta para carretillas/zorras de carga con piso estriado) hasta cota Bodega Z = -2.55 m!
    y_r_bot  = OFFSET_Y + 5.50    # Llega a nivel plano -2.55 m frente al costado de la Bodega
    y_r_top  = OFFSET_Y + 19.50   # Inicia descenso tras umbral interno del Portón Derecho de Av. 4
    y_av4_tr = OFFSET_Y + Y_AV4
    # Tramo plano Sur de maniobra lateral (Y_casa = 0.00..5.50, Z = -2.55 m)
    add_terrain_strip_y(L_RAMP, 8,
                        9.15, x_right(OFFSET_Y) - 0.15, OFFSET_Y, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        9.15, x_right(y_r_bot) - 0.15,  y_r_bot,  Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    # Rampa continua antideslizante (Y_casa = 5.50 -> 19.50, Z = -2.55 -> 0.00 m)
    add_terrain_strip_y(L_RAMP, 8,
                        9.15, x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        9.15, x_right(y_r_top) - 0.15, y_r_top, -0.20,              0.00)
    # Umbral plano de recepción tras la Puerta Derecha de Avenida 4 (Y_casa = 19.50..21.71, Z = 0.00 m)
    add_terrain_strip_y(L_RAMP, 8,
                        9.15, x_right(y_r_top) - 0.15, y_r_top, -0.20, 0.00,
                        9.15, P2_LOC[0] - 0.15,        P2_LOC[1], -0.20, 0.00)
    # Muro de acompañamiento bajo Planta Baja a lo largo de la rampa (X = 9.00..9.15)
    add_terrain_strip_y(L_P1_EXT, 7,
                        9.00, 9.15, OFFSET_Y + 8.30, Z_SOT_FLOOR, Z_P1_FLOOR,
                        9.00, 9.15, y_r_top,         0.00,        Z_P1_FLOOR)

    # Terreno natural bajo losa de Planta Baja (Y_casa = 8.30..21.71)
    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05)
    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05,
                        0.15, 9.00, y_av4_tr,         -0.20, -0.15)

    # Pared del vecino izquierdo (X = 0.00..0.15 INTOCABLE) y cercas perimetrales
    wall_h = 2.50
    add_box(L_FENCE, 8, 0.00, P4_LOC[1], Z_SOT_FLOOR, 0.15, OFFSET_Y + 8.30, Z_P1_FLOOR + wall_h)
    add_box(L_FENCE, 8, 0.00, OFFSET_Y + 8.30, 0.00, 0.15, P1_LOC[1], wall_h)
    add_hexahedron(L_FENCE, 8, [
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR),        (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR),        (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR),
        (P4_LOC[0], P4_LOC[1],        Z_SOT_FLOOR + 2.20), (P3_LOC[0], P3_LOC[1],        Z_SOT_FLOOR + 2.20),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR + 2.20), (P4_LOC[0], P4_LOC[1] + 0.15, Z_SOT_FLOOR + 2.20),
    ])
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(P3_LOC[1]) - 0.15, x_right(P3_LOC[1]), P3_LOC[1], Z_SOT_FLOOR, Z_SOT_FLOOR + 2.20,
                        x_right(y_r_bot) - 0.15,   x_right(y_r_bot),   y_r_bot,   Z_SOT_FLOOR, Z_SOT_FLOOR + 2.20)
    add_terrain_strip_y(L_FENCE, 8,
                        x_right(y_r_bot) - 0.15, x_right(y_r_bot), y_r_bot, Z_SOT_FLOOR, Z_SOT_FLOOR + 2.20,
                        P2_LOC[0] - 0.15,        P2_LOC[0],        P2_LOC[1], 0.00,      2.20)
    add_hexahedron(L_FENCE, 1, [
        (P1_LOC[0], P1_LOC[1] - 0.15, -0.20), (P2_LOC[0], P2_LOC[1] - 0.15, -0.20),
        (P2_LOC[0], P2_LOC[1],        -0.20), (P1_LOC[0], P1_LOC[1],        -0.20),
        (P1_LOC[0], P1_LOC[1] - 0.15,  0.10), (P2_LOC[0], P2_LOC[1] - 0.15,  0.10),
        (P2_LOC[0], P2_LOC[1],         0.10), (P1_LOC[0], P1_LOC[1],         0.10),
    ])

    # =========================================================================
    # 6. EJES ESTRUCTURALES, RÓTULOS 3D Y LÁMINAS 2D DE LOS 4 NIVELES
    # =========================================================================
    L_GRID = "EJES_ESTRUCTURALES"
    for label, gx in [("0 (PROPIO - SIN ALERO)", 0.275), ("1 (EXISTENTE)", 2.825), ("2", 5.925), ("3", 9.075)]:
        add_house_line(L_GRID, 1, gx, -1.20, 0.0, gx, Y_AV4 + 0.80, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", gx - 0.35, Y_AV4 + 1.00, 0.0, 0.20)
    for label, gy in [("A0 (AV.4)", 21.585), ("A", 18.575), ("B", 16.325), ("C", 14.625),
                      ("D", 12.025), ("E", 8.875), ("F", 6.575), ("G", 3.575), ("H (POST.)", 0.125)]:
        add_house_line(L_GRID, 1, -0.60, gy, 0.0, 10.40, gy, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", 10.50, gy - 0.10, 0.0, 0.22)

    add_text(L_TERR, 1, "P-1 (N:1141664.17, E:529755.04)", P1_LOC[0] - 0.5, P1_LOC[1] + 0.5, 0.20, 0.26)
    add_text(L_TERR, 1, "P-2 (N:1141670.33, E:529764.60)", P2_LOC[0] - 3.5, P2_LOC[1] + 0.5, 0.20, 0.26)
    add_text(L_TERR, 1, "P-3 (N:1141648.99, E:529777.07)", P3_LOC[0] - 3.5, P3_LOC[1] - 0.6, Z_SOT_FLOOR, 0.26)
    add_text(L_TERR, 1, "P-4 (N:1141643.13, E:529767.99)", P4_LOC[0] - 0.5, P4_LOC[1] - 0.6, Z_SOT_FLOOR, 0.26)

    for txt, rx, ry, rz in [
        ("SOTANO: GRAN BODEGA MAYORISTA (PASILLO CENTRAL LIBRE 1,95m)", 1.95, 4.55, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Camara Pre-Frio y Maduracion (3,95 x 2,55m)", 1.85, 6.75, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Avenida Principal de Carga Libre (2,25m ancho)", 6.05, 5.10, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Bascula 500kg + Mesa Control (Adosadas sin estorbar)", 4.80, 3.15, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Bano Operativo Personal (1,75 x 2,40m)", 2.95, 1.35, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Puerta Escalera Libre (Abre sin obstaculos)", 0.35, 3.85, Z_SOT_FLOOR + 0.05),
        ("PATIO CARGA: Acceso desde Rampa Derecha Av.4", 4.80, -1.40, Z_SOT_FLOOR + 0.05),
    ]:
        add_house_text("SOTANO_ROTULOS", 4, txt, rx, ry, rz, 0.16)

    for txt, rx, ry, rz in [
        ("PB: SALON COMERCIAL AMPLIADO SIN BODEGA (~112 m2)", 3.80, 14.50, 0.05),
        ("PB: ESTACIONAMIENTO 2 AUTOS (3,00m LIBRES)", 0.45, 16.50, 0.05),
        ("PB: VESTIBULO CERRADO + PUERTA ACCESO ESCALERA (GARAJE / P2)", 0.40, 8.15, 0.05),
        ("PB: PUERTA SEGURIDAD CON LLAVE A SOTANO BODEGA", 0.38, 7.10, 0.05),
        ("PB: PORTON DERECHO AV.4 -> UNICO ACCESO COMERCIAL A BODEGA", 9.20, 21.10, 0.05),
        ("PB: Mural Frigorifico Lacteos y Fruta Picada", 6.90, 6.10, 0.05),
        ("PB: BARRA GOURMET JUGOS, CAFE Y ENSALADAS DE FRUTAS", 3.05, 1.90, 0.05),
        ("PB: OFICINA ACRISTALADA ADMINISTRACION (10,05 m2)", 6.05, 1.90, 0.05),
        ("PB: NUCLEO BANOS SUROESTE (DAMAS + CABALLEROS + ANTEBANO)", 0.38, 1.80, 0.05),
        ("PB: Cuarto Aseo Bajo Escalera", 1.50, 4.70, 0.05),
    ]:
        add_house_text("ROTULOS_TEXTO", 2, txt, rx, ry, rz, 0.16)

    for txt, rx, ry, rz in [
        ("P2 OPCION A: GRAN BALCONADA SOCIAL CONTINUA (8,70 x 1,96m)", 1.60, 20.45, Z_P2_FLOOR + 0.05),
        ("P2: GRAN SALA CHALET ABIERTA A NORTE Y ESTE", 1.20, 17.20, Z_P2_FLOOR + 0.05),
        ("P2: ESTUDIO / HOME OFFICE ACRISTALADO (LUZ Y BRISA ESTE)", 6.10, 17.20, Z_P2_FLOOR + 0.05),
        ("P2: GRAN COMEDOR 10 PUESTOS + GALERIA DESAYUNADOR ESTE", 2.00, 13.60, Z_P2_FLOOR + 0.05),
        ("P2: Nevera French Door + Torre Hornos", 0.35, 12.40, Z_P2_FLOOR + 0.05),
        ("P2: COCINA GOURMET CON ISLA + HALL LIBRE 3,10m", 1.35, 10.20, Z_P2_FLOOR + 0.05),
        ("P2: Despensa Walk-In Bajo Escalera P3", 0.35, 6.65, Z_P2_FLOOR + 0.05),
        ("P2: Bano Social Completo con Ducha", 6.15, 5.80, Z_P2_FLOOR + 0.05),
        ("P2: HABITACION 4 HUESPEDES / ADULTO MAYOR (ESQUINERA ESTE+SUR)", 6.10, 2.15, Z_P2_FLOOR + 0.05),
        ("P2: Mirador Ventilado Sur", 3.20, 1.80, Z_P2_FLOOR + 0.05),
        ("P2: Lavanderia Amplia (Libre de escalera tanque, H=2,85m)", 0.40, 1.80, Z_P2_FLOOR + 0.05),
    ]:
        add_house_text("P2_ROTULOS", 6, txt, rx, ry, rz, 0.16)

    for txt, rx, ry, rz in [
        ("P3 OPCION A: GRAN TERRAZA CONTINUA MASTER PENTHOUSE (8,70 x 1,96m)", 1.60, 20.45, Z_P3_FLOOR + 0.05),
        ("P3: MASTER PENTHOUSE SUITE (ACCESO DIRECTO A VESTIER Y SPA)", 4.85, 17.60, Z_P3_FLOOR + 0.05),
        ("P3: GRAN VESTIER WALK-IN (VENTANA ALTA CLERESTORY UV + BARN DOOR)", 0.55, 17.60, Z_P3_FLOOR + 0.05),
        ("P3: GRAN BANO SPA MASTER CON TINA EXENTA (12,5 m2)", 0.80, 14.30, Z_P3_FLOOR + 0.05),
        ("P3: FAMILY ROOM / CINE 85\" (POZO REAL DE LUZ Y AIRE CLARABOYA)", 0.80, 10.50, Z_P3_FLOOR + 0.05),
        ("P3: HABITACION SECUNDARIA 2 (ESTE — VIENTOS ALISIOS)", 6.10, 12.20, Z_P3_FLOOR + 0.05),
        ("P3: HABITACION SECUNDARIA 3 (ESTE — VIENTOS ALISIOS)", 6.10, 8.20, Z_P3_FLOOR + 0.05),
        ("P3: Bano Familiar Compartido Doble Lavamanos", 6.10, 5.25, Z_P3_FLOOR + 0.05),
        ("P3: GRAN TERRAZA MIRADOR & QUINCHO BBQ ESQUINERA (26,88 m2)", 3.25, 2.15, Z_P3_FLOOR + 0.05),
        ("P3: Cuarto Apoyo / Gym + Subida a Tanques 2.000L", 0.40, 1.85, Z_P3_FLOOR + 0.05),
        ("BUHARDILLA P3: 2x1.000L + DESEMBARQUE ESTE LIBRE (Z=+8,68m)", 0.35, 0.35, Z_TANK_FLOOR + 0.05),
    ]:
        add_house_text("P3_ROTULOS", 5, txt, rx, ry, rz, 0.16)

    # --- LÁMINA 2D 1: SÓTANO GRAN BODEGA COMERCIAL REDISTRIBUIDA (SX = 16.0, SY = 2.0) ---
    SX, SY = 16.00, 2.00
    L_SOT_2D = "PLANTA_SOTANO_2D"
    add_text(L_SOT_2D, 2, "PLANTA SOTANO (Z=-2,55m): BODEGA CON PASILLOS AMPLIOS (1,95m-2,25m)", SX - 0.1, SY - 3.1, 0.0, 0.22)
    add_rect_2d(L_SOT_2D, 8, SX + 0.00, SY - 2.50, SX + 0.15, SY + 8.30)
    add_rect_2d(L_SOT_2D, 7, SX + 0.15, SY + 0.00, SX + 9.15, SY + 8.30)
    add_rect_2d(L_SOT_2D, 8, SX + 9.15, SY + 0.00, SX + 10.90, SY + 8.30)     # Corredor/Rampa Este
    add_rect_2d(L_SOT_2D, 8, SX + 4.50, SY - 2.50, SX + 9.15, SY + 0.00)     # Patio Maniobra Carga
    # Esclusa Escalera con vano de puerta recortado y hoja abierta a 45° hacia el pasillo libre
    add_line(L_SOT_2D, 4, SX + 0.30, SY + 3.55, 0.0, SX + 1.55, SY + 3.55, 0.0)
    add_line(L_SOT_2D, 4, SX + 1.55, SY + 3.55, 0.0, SX + 1.55, SY + 3.70, 0.0)
    add_line(L_SOT_2D, 4, SX + 1.55, SY + 4.55, 0.0, SX + 1.55, SY + 8.15, 0.0)
    add_line(L_SOT_2D, 1, SX + 1.55, SY + 4.55, 0.0, SX + 2.15, SY + 3.95, 0.0)  # Hoja puerta abierta sin estorbos!
    for i in range(13):
        yy = SY + 4.45 + i * ((7.40 - 4.45) / 12.0)
        add_line(L_SOT_2D, 3, SX + 0.30, yy, 0.0, SX + 1.40, yy, 0.0)
    add_rect_2d(L_SOT_2D, 5, SX + 1.60, SY + 5.55, SX + 5.55, SY + 8.10)     # Cámara Pre-Frío
    add_rect_2d(L_SOT_2D, 4, SX + 2.80, SY + 0.15, SX + 4.70, SY + 2.68)     # Baño Operativo
    for rx1, ry1, rx2, ry2 in [(5.85, 7.35, 8.85, 8.05), (8.25, 4.05, 8.90, 6.80),
                               (8.25, 0.85, 8.90, 3.35), (0.35, 0.22, 2.65, 0.88), (0.35, 1.05, 1.00, 3.25)]:
        add_rect_2d(L_SOT_2D, 30, SX + rx1, SY + ry1, SX + rx2, SY + ry2)
    add_rect_2d(L_SOT_2D, 34, SX + 1.95, SY + 1.15, SX + 2.72, SY + 1.95)    # Pallet Suroeste adosado
    add_rect_2d(L_SOT_2D, 3,  SX + 4.80, SY + 0.35, SX + 5.70, SY + 1.25)    # Báscula Plataforma 500kg al costado
    add_rect_2d(L_SOT_2D, 34, SX + 4.75, SY + 1.45, SX + 5.70, SY + 2.50)    # Mesa Control adosada al baño
    for cx_s, cy_s in sot_cols_axes:
        add_rect_2d(L_SOT_2D, 1, SX + cx_s - 0.175, SY + cy_s - 0.175, SX + cx_s + 0.175, SY + cy_s + 0.175)
    add_text(L_SOT_2D, 5, "Camara Pre-Frio", SX + 2.20, SY + 6.70, 0.0, 0.15)
    add_text(L_SOT_2D, 2, "Pasillo Libre 1,95m", SX + 2.30, SY + 4.45, 0.0, 0.14)
    add_text(L_SOT_2D, 3, "Av. Carga 2,25m", SX + 6.10, SY + 5.10, 0.0, 0.14)
    add_text(L_SOT_2D, 3, "Bascula + Control", SX + 4.75, SY + 2.80, 0.0, 0.12)
    add_text(L_SOT_2D, 1, "Porton Carga 2,20m", SX + 6.35, SY - 0.40, 0.0, 0.14)
    add_text(L_SOT_2D, 2, "Llega Rampa Av.4", SX + 9.22, SY + 4.00, 0.0, 0.13)

    # --- LÁMINA 2D 2: PLANTA BAJA COMERCIAL REDISTRIBUIDA SIN BODEGA POSTERIOR (BX = 30.0, BY = 2.0) ---
    BX, BY = 30.00, 2.00
    L_PB_2D = "PLANTA_BAJA_2D"
    add_text(L_PB_2D, 2, "PLANTA BAJA (Z=0,00m): COMERCIO AMPLIADO + BARRA JUGOS + OFICINA + BANOS SW", BX - 0.1, BY - 0.8, 0.0, 0.20)
    add_rect_2d(L_PB_2D, 8, BX + 0.00, BY + 0.00, BX + 0.15, BY + Y_AV4)
    add_rect_2d(L_PB_2D, 7, BX + 0.15, BY + 0.00, BX + 9.15, BY + Y_AV4)
    add_rect_2d(L_PB_2D, 8, BX + 9.15, BY + 0.00, BX + 11.22, BY + Y_AV4)
    add_line(L_PB_2D, 1, BX + 9.35, BY + Y_AV4, 0.0, BX + 11.12, BY + Y_AV4, 0.0)
    add_text(L_PB_2D, 1, "PUERTA DER. AV.4 (BODEGA)", BX + 9.15, BY + Y_AV4 + 0.35, 0.0, 0.14)
    add_text(L_PB_2D, 3, "Rampa Continua a Sotano", BX + 9.25, BY + 12.50, 0.0, 0.13)
    # Divisiones Garaje / Vestíbulo Cerrado de Escaleras / Cuarto Aseo / Baños Suroeste
    add_line(L_PB_2D, 7, BX + 2.82, BY + 0.15, 0.0, BX + 2.82, BY + 2.35, 0.0)
    add_line(L_PB_2D, 7, BX + 2.82, BY + 3.20, 0.0, BX + 2.82, BY + 3.75, 0.0)
    add_line(L_PB_2D, 7, BX + 2.82, BY + 4.45, 0.0, BX + 2.82, BY + 8.95, 0.0)
    add_line(L_PB_2D, 3, BX + 2.82, BY + 3.20, 0.0, BX + 2.25, BY + 3.20, 0.0)       # Puerta Antebaño Suroeste
    add_rect_2d(L_PB_2D, 7, BX + 3.30, BY + 8.80, BX + 3.45, BY + Y_AV4 - 0.15)
    add_rect_2d(L_PB_2D, 7, BX + 0.30, BY + 8.80, BX + 1.60, BY + 8.95)
    add_rect_2d(L_PB_2D, 7, BX + 2.55, BY + 8.80, BX + 3.45, BY + 8.95)
    add_line(L_PB_2D, 3, BX + 1.60, BY + 8.88, 0.0, BX + 2.55, BY + 8.88, 0.0)       # Puerta Garaje <-> Escalera P2
    add_line(L_PB_2D, 1, BX + 0.40, BY + 7.42, 0.0, BX + 1.32, BY + 7.42, 0.0)       # Puerta Seguridad a Sótano
    for st_i in range(13):
        st_y = BY + 4.45 + st_i * ((7.40 - 4.45) / 12.0)
        add_line(L_PB_2D, 3, BX + 0.30, st_y, 0.0, BX + 1.40, st_y, 0.0)
    for st_p2 in range(15):
        st2_y = BY + 7.35 - st_p2 * ((7.35 - 4.40) / 14.0)
        add_line(L_PB_2D, 7, BX + 1.55, st2_y, 0.0, BX + 2.65, st2_y, 0.0)
    add_rect_2d(L_PB_2D, 8,  BX + 0.55, BY + 15.20, BX + 2.65, BY + 20.60)
    add_rect_2d(L_PB_2D, 8,  BX + 0.55, BY + 9.20,  BX + 2.65, BY + 14.60)
    # Representación 2D de Portón Corredizo en riel curvo + 2 Santamarías de Caracol en fachada Avenida 4
    add_line(L_PB_2D, 30, BX + 0.40, BY + Y_AV4 - 0.16, 0.0, BX + 3.22, BY + Y_AV4 - 0.16, 0.0) # Riel frontal portón
    add_line(L_PB_2D, 30, BX + 3.22, BY + 18.90,        0.0, BX + 3.22, BY + Y_AV4 - 0.16, 0.0) # Riel/hojas bolsillo der.
    add_rect_2d(L_PB_2D, 9, BX + 3.65, BY + Y_AV4 - 0.36, BX + 5.75, BY + Y_AV4 - 0.04)         # Santamaría Caracol 1
    add_rect_2d(L_PB_2D, 9, BX + 6.20, BY + Y_AV4 - 0.36, BX + 8.80, BY + Y_AV4 - 0.04)         # Santamaría Caracol 2
    add_text(L_PB_2D, 30, "Porton Corredizo", BX + 0.55, BY + Y_AV4 + 0.35, 0.0, 0.13)
    add_text(L_PB_2D, 9,  "2 Santamarias Caracol", BX + 4.45, BY + Y_AV4 + 0.35, 0.0, 0.13)
    # Nuevos espacios del fondo comercial (Banos Suroeste + Barra Jugos + Oficina Acristalada + Isla 5 + Mural Frio)
    add_rect_2d(L_PB_2D, 6,  BX + 0.30, BY + 0.15,  BX + 2.75, BY + 3.55)            # Núcleo Baños Suroeste (Damas/Cab.)
    add_line(L_PB_2D, 6, BX + 1.52, BY + 0.15, 0.0, BX + 1.52, BY + 3.55, 0.0)
    add_line(L_PB_2D, 6, BX + 1.52, BY + 1.78, 0.0, BX + 2.75, BY + 1.78, 0.0)
    add_rect_2d(L_PB_2D, 30, BX + 3.55, BY + 2.80,  BX + 5.78, BY + 3.55)            # Barra Gourmet Jugos / Fruta Picada
    add_rect_2d(L_PB_2D, 34, BX + 3.05, BY + 0.18,  BX + 5.75, BY + 0.85)            # Contra-barra preparación Sur
    add_rect_2d(L_PB_2D, 4,  BX + 5.90, BY + 0.15,  BX + 9.00, BY + 3.55)            # Oficina Acristalada Administración
    add_rect_2d(L_PB_2D, 5,  BX + 8.26, BY + 5.10,  BX + 8.98, BY + 7.55)            # Mural Frigorífico Este
    add_rect_2d(L_PB_2D, 30, BX + 5.15, BY + 5.30,  BX + 6.70, BY + 6.85)            # 5ta Isla Degustación
    for cx_pb, cy_pb in existing_and_new_cols:
        add_rect_2d(L_PB_2D, 1, BX + cx_pb - 0.125, BY + cy_pb - 0.125, BX + cx_pb + 0.125, BY + cy_pb + 0.125)
    add_text(L_PB_2D, 3, "Vestibulo + Puerta Escalera", BX + 0.35, BY + 8.15, 0.0, 0.11)
    add_text(L_PB_2D, 2, "Salon Fruteria Ampliado (~112m2)", BX + 3.80, BY + 14.20, 0.0, 0.16)
    add_text(L_PB_2D, 5, "Mural Frio", BX + 7.15, BY + 6.20, 0.0, 0.13)
    add_text(L_PB_2D, 6, "Banos SW", BX + 0.55, BY + 1.90, 0.0, 0.14)
    add_text(L_PB_2D, 30, "Barra Jugos/Frutas", BX + 3.15, BY + 1.90, 0.0, 0.14)
    add_text(L_PB_2D, 4, "Oficina Vidrio", BX + 6.25, BY + 1.90, 0.0, 0.14)

    # --- LÁMINA 2D 3: SEGUNDO PISO — DESPENSA BAJO ESCALERA + NEVERA NORTE (P2X = 45.0, P2Y = 2.0) ---
    P2X, P2Y = 45.00, 2.00
    L_P2_2D = "PLANTA_SEGUNDO_PISO_2D"
    add_text(L_P2_2D, 6, "PLANTA SEGUNDO PISO (Z=+3,00m — DESPENSA BAJO ESCALERA + NEVERA)", P2X - 0.1, P2Y - 0.8, 0.0, 0.21)
    add_rect_2d(L_P2_2D, 6,  P2X + 0.15, P2Y + 0.00,  P2X + 9.15, P2Y + Y_AV4)
    add_rect_2d(L_P2_2D, 30, P2X + 0.30, P2Y + 19.60, P2X + 9.00, P2Y + 21.56)     # Gran Balconada Continua
    # Muro Norte P2 (Y=19.52) con las 3 Mamparas Corredizas de Terraza en 2D (hojas de cristal superpuestas + paso libre)
    for wx_a, wx_b in [(0.30, 0.65), (2.55, 3.15), (5.55, 6.25), (8.65, 9.00)]:
        add_line(L_P2_2D, 6, P2X + wx_a, P2Y + 19.52, 0.0, P2X + wx_b, P2Y + 19.52, 0.0)
    for mx1, mx2 in [(0.65, 2.55), (3.15, 5.55), (6.25, 8.65)]:
        wl_2d = 0.50 * (mx2 - mx1)
        add_line(L_P2_2D, 4, P2X + mx1,        P2Y + 19.55, 0.0, P2X + mx1 + wl_2d,        P2Y + 19.55, 0.0)
        add_line(L_P2_2D, 4, P2X + mx1 + 0.22, P2Y + 19.49, 0.0, P2X + mx1 + 0.22 + wl_2d, P2Y + 19.49, 0.0)
    add_rect_2d(L_P2_2D, 4,  P2X + 5.92, P2Y + 15.20, P2X + 9.00, P2Y + 19.45)     # Estudio Acristalado Este
    add_rect_2d(L_P2_2D, 34, P2X + 2.05, P2Y + 13.15, P2X + 4.75, P2Y + 14.30)     # Comedor 10p
    add_rect_2d(L_P2_2D, 34, P2X + 7.15, P2Y + 13.05, P2X + 8.25, P2Y + 14.15)     # Desayunador Este
    add_rect_2d(L_P2_2D, 3,  P2X + 2.36, P2Y + 8.85,  P2X + 3.68, P2Y + 11.75)     # Gran Isla Gourmet
    add_rect_2d(L_P2_2D, 3,  P2X + 0.30, P2Y + 8.45,  P2X + 0.98, P2Y + 11.48)     # Mesón Cocina Oeste
    add_rect_2d(L_P2_2D, 34, P2X + 0.30, P2Y + 11.48, P2X + 1.00, P2Y + 12.10)     # Torre Hornos
    add_rect_2d(L_P2_2D, 5,  P2X + 0.30, P2Y + 12.12, P2X + 1.12, P2Y + 13.06)     # Nevera French Door
    add_rect_2d(L_P2_2D, 6,  P2X + 0.30, P2Y + 5.45,  P2X + 1.48, P2Y + 7.40)      # Despensa Bajo Escalera P3!
    add_line(L_P2_2D, 1, P2X + 0.44, P2Y + 7.40, 0.0, P2X + 0.44, P2Y + 8.18, 0.0) # Hoja puerta Despensa abierta
    add_rect_2d(L_P2_2D, 6,  P2X + 6.00, P2Y + 4.45,  P2X + 9.00, P2Y + 7.40)      # Baño Social Completo
    add_rect_2d(L_P2_2D, 6,  P2X + 6.00, P2Y + 0.15,  P2X + 9.00, P2Y + 4.30)      # Habitación 4 Huéspedes
    add_rect_2d(L_P2_2D, 6,  P2X + 0.30, P2Y + 0.15,  P2X + 2.75, P2Y + 3.50)      # Lavandería Libre
    for i in range(num_steps_p2 + 1):
        yy2 = P2Y + 7.35 - i * step_dy_p2
        add_line(L_P2_2D, 7, P2X + 1.55, yy2, 0.0, P2X + 2.65, yy2, 0.0)
    for i in range(num_steps_p3 + 1):
        yy3 = P2Y + 4.40 + i * step_dy_p3
        add_line(L_P2_2D, 30, P2X + 0.30, yy3, 0.0, P2X + 1.45, yy3, 0.0)
    for cx, cy in existing_and_new_cols:
        add_rect_2d(L_P2_2D, 1, P2X + cx - 0.125, P2Y + cy - 0.125, P2X + cx + 0.125, P2Y + cy + 0.125)
    add_text(L_P2_2D, 2, "Balconada Continua (8,70x1,96m)", P2X + 2.40, P2Y + 20.50, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Gran Sala Chalet", P2X + 1.80, P2Y + 17.20, 0.0, 0.17)
    add_text(L_P2_2D, 4, "Estudio Vidrio (Este)", P2X + 6.20, P2Y + 17.20, 0.0, 0.15)
    add_text(L_P2_2D, 2, "Comedor 10p", P2X + 2.50, P2Y + 13.60, 0.0, 0.16)
    add_text(L_P2_2D, 5, "Nevera", P2X + 0.35, P2Y + 12.50, 0.0, 0.13)
    add_text(L_P2_2D, 2, "Cocina + Isla Central", P2X + 1.40, P2Y + 10.20, 0.0, 0.16)
    add_text(L_P2_2D, 3, "Hall Libre 3,10m", P2X + 3.05, P2Y + 6.80, 0.0, 0.14)
    add_text(L_P2_2D, 1, "Despensa Bajo Esc.", P2X + 0.32, P2Y + 6.60, 0.0, 0.11)
    add_text(L_P2_2D, 2, "Bano Social", P2X + 6.35, P2Y + 5.80, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Hab.4 Huespedes", P2X + 6.20, P2Y + 2.15, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Lavanderia", P2X + 0.65, P2Y + 1.80, 0.0, 0.16)

    # --- LÁMINA 2D 4: NUEVO TERCER PISO — GRAN TERRAZA ESQUINERA + ACCESOS VESTIER/SPA (P3X = 60.0, P3Y = 2.0) ---
    P3X, P3Y = 60.00, 2.00
    L_P3_2D = "PLANTA_TERCER_PISO_2D"
    add_text(L_P3_2D, 5, "PLANTA TERCER PISO (Z=+6,00m — GRAN TERRAZA 26,9m2 + PUERTAS VESTIER/SPA)", P3X - 0.1, P3Y - 0.8, 0.0, 0.20)
    add_rect_2d(L_P3_2D, 5,  P3X + 0.15, P3Y + 0.00,  P3X + 9.15, P3Y + Y_AV4)
    add_rect_2d(L_P3_2D, 30, P3X + 0.30, P3Y + 19.60, P3X + 9.00, P3Y + 21.56)     # Gran Terraza Continua Master (17,05 m²)
    # Muro Norte P3 en 2D: muro bajo macizo + proyección Ventana Alta Clerestory (X=0.95..3.65, H=2,35..2,80m) + ventanal Master
    add_line(L_P3_2D, 5, P3X + 0.30, P3Y + 19.52, 0.0, P3X + 5.25, P3Y + 19.52, 0.0)
    add_line(L_P3_2D, 4, P3X + 0.95, P3Y + 19.46, 0.0, P3X + 3.65, P3Y + 19.46, 0.0) # Proyección ventana alta Clerestory UV
    add_line(L_P3_2D, 4, P3X + 0.95, P3Y + 19.58, 0.0, P3X + 3.65, P3Y + 19.58, 0.0)
    add_text(L_P3_2D, 4, "Vent. Alta UV (H=2,35m)", P3X + 1.05, P3Y + 19.12, 0.0, 0.11)
    add_line(L_P3_2D, 5, P3X + 8.45, P3Y + 19.52, 0.0, P3X + 9.00, P3Y + 19.52, 0.0)
    add_line(L_P3_2D, 4, P3X + 5.25, P3Y + 19.52, 0.0, P3X + 6.88, P3Y + 19.52, 0.0) # Hoja corrediza cristal
    # Muros Master / Vestier / Baño Spa CON VANOS DE PUERTAS RECORTADOS Y HOJAS ABIERTAS VISIBLES EN 2D!
    add_line(L_P3_2D, 5, P3X + 4.50, P3Y + 14.52, 0.0, P3X + 4.75, P3Y + 14.52, 0.0)
    add_line(L_P3_2D, 5, P3X + 5.65, P3Y + 14.52, 0.0, P3X + 9.00, P3Y + 14.52, 0.0)
    add_line(L_P3_2D, 3, P3X + 4.75, P3Y + 14.52, 0.0, P3X + 4.75, P3Y + 15.35, 0.0) # Hoja entrada Master
    # Muro longitudinal X = 4.42 con puerta Baño Spa (14.70..15.50) y Portal Barn Door Vestier (17.05..18.35)
    add_line(L_P3_2D, 6, P3X + 4.42, P3Y + 12.80, 0.0, P3X + 4.42, P3Y + 14.70, 0.0)
    add_line(L_P3_2D, 6, P3X + 4.42, P3Y + 15.50, 0.0, P3X + 4.42, P3Y + 17.05, 0.0)
    add_line(L_P3_2D, 6, P3X + 4.42, P3Y + 18.35, 0.0, P3X + 4.42, P3Y + 19.45, 0.0)
    add_line(L_P3_2D, 1, P3X + 4.54, P3Y + 16.22, 0.0, P3X + 4.54, P3Y + 16.95, 0.0) # Barn Door hoja sur abierta
    add_line(L_P3_2D, 1, P3X + 4.54, P3Y + 18.45, 0.0, P3X + 4.54, P3Y + 19.18, 0.0) # Barn Door hoja norte abierta
    add_line(L_P3_2D, 3, P3X + 4.42, P3Y + 14.70, 0.0, P3X + 3.82, P3Y + 14.20, 0.0) # Hoja 45° Dorm -> Baño Spa
    # Muro transversal Vestier / Baño Spa (Y = 15.98) con Puerta Interna abierta a 45° (X = 1.65..2.50)
    add_line(L_P3_2D, 6, P3X + 0.30, P3Y + 15.98, 0.0, P3X + 1.65, P3Y + 15.98, 0.0)
    add_line(L_P3_2D, 6, P3X + 2.50, P3Y + 15.98, 0.0, P3X + 4.42, P3Y + 15.98, 0.0)
    add_line(L_P3_2D, 3, P3X + 1.65, P3Y + 15.98, 0.0, P3X + 2.25, P3Y + 16.58, 0.0) # Hoja 45° Vestier <-> Baño Spa
    add_line(L_P3_2D, 4, P3X + 0.30, P3Y + 12.75, 0.0, P3X + 4.42, P3Y + 12.75, 0.0)
    add_rect_2d(L_P3_2D, 9,  P3X + X_SKY_W, P3Y + Y_SKY_S, P3X + X_SKY_E, P3Y + Y_SKY_N) # Hueco Real Claraboya!
    add_rect_2d(L_P3_2D, 6,  P3X + 6.00, P3Y + 10.30, P3X + 9.00, P3Y + 14.45)     # Habitación Secundaria 2
    add_rect_2d(L_P3_2D, 6,  P3X + 6.00, P3Y + 6.45,  P3X + 9.00, P3Y + 10.15)     # Habitación Secundaria 3
    add_rect_2d(L_P3_2D, 6,  P3X + 6.00, P3Y + 4.45,  P3X + 9.00, P3Y + 6.30)      # Baño Familiar P3
    add_rect_2d(L_P3_2D, 30, P3X + 2.90, P3Y + 0.08,  P3X + 9.07, P3Y + 4.30)      # GRAN TERRAZA MIRADOR ESQUINERA!
    add_rect_2d(L_P3_2D, 8,  P3X + 6.20, P3Y + 3.65,  P3X + 8.65, P3Y + 4.28)      # Barra Parrillera BBQ
    add_rect_2d(L_P3_2D, 6,  P3X + 0.30, P3Y + 0.15,  P3X + 2.75, P3Y + 4.10)      # Cuarto Apoyo / Gym / Tanques
    for i in range(num_steps_p3 + 1):
        yy3 = P3Y + 4.40 + i * step_dy_p3
        add_line(L_P3_2D, 30, P3X + 0.30, yy3, 0.0, P3X + 1.45, yy3, 0.0)
    for cx, cy in existing_and_new_cols:
        add_rect_2d(L_P3_2D, 8, P3X + cx - 0.12, P3Y + cy - 0.12, P3X + cx + 0.12, P3Y + cy + 0.12)
    add_text(L_P3_2D, 2, "Gran Terraza Continua Master (8,70x1,96m)", P3X + 2.15, P3Y + 20.50, 0.0, 0.15)
    add_text(L_P3_2D, 2, "MASTER PENTHOUSE", P3X + 5.30, P3Y + 17.50, 0.0, 0.16)
    add_text(L_P3_2D, 1, "Portal Barn Door ->", P3X + 2.85, P3Y + 17.65, 0.0, 0.12)
    add_text(L_P3_2D, 2, "Vestier (13,7m2)", P3X + 0.55, P3Y + 17.60, 0.0, 0.14)
    add_text(L_P3_2D, 4, "Bano Spa + Tina", P3X + 0.70, P3Y + 14.30, 0.0, 0.14)
    add_text(L_P3_2D, 3, "Family Room / Cine 85\"", P3X + 0.90, P3Y + 10.20, 0.0, 0.14)
    add_text(L_P3_2D, 9, "Hueco Real Luz/Aire", P3X + 2.65, P3Y + 8.30, 0.0, 0.13)
    add_text(L_P3_2D, 2, "Hab. 2 (12,5m2)", P3X + 6.25, P3Y + 12.20, 0.0, 0.16)
    add_text(L_P3_2D, 2, "Hab. 3 (11,1m2)", P3X + 6.25, P3Y + 8.20, 0.0, 0.16)
    add_text(L_P3_2D, 2, "Bano Familiar", P3X + 6.25, P3Y + 5.25, 0.0, 0.15)
    add_text(L_P3_2D, 30, "GRAN TERRAZA MIRADOR & BBQ (26,9m2)", P3X + 3.30, P3Y + 2.15, 0.0, 0.15)
    add_text(L_P3_2D, 5, "Gym + Subida 2000L", P3X + 0.45, P3Y + 1.80, 0.0, 0.13)

    # --- LÁMINA 2D 5: BUHARDILLA 2.000 L CON BARANDA REORIENTADA + CORTE CLARABOYA ABIERTA ---
    TX, TY = 16.00, 14.00
    L_TANK_2D = "PLANTA_TANQUES_2000L_2D"
    add_text(L_TANK_2D, 5, "BUHARDILLA P3: 2x1.000L + BARANDA EN 'L' (PASO ESTE LIBRE)", TX - 0.1, TY - 0.7, 0.0, 0.20)
    add_rect_2d(L_TANK_2D, 8,  TX + 0.00, TY + 0.00, TX + 0.15, TY + 4.45)
    add_rect_2d(L_TANK_2D, 34, TX + 0.15, TY + 0.00, TX + 2.90, TY + 4.45)
    add_rect_2d(L_TANK_2D, 8,  TX + 0.38, TY + 2.55, TX + 1.18, TY + 3.70)        # Escotilla escalera
    # Baranda en "L" sobre borde Sur (Y=2.50) y mitad Sureste (Y=2.50..3.05), dejando libre Y=3.05..4.25!
    add_line(L_TANK_2D, 1, TX + 0.38, TY + 2.50, 0.0, TX + 1.24, TY + 2.50, 0.0)
    add_line(L_TANK_2D, 1, TX + 1.24, TY + 2.50, 0.0, TX + 1.24, TY + 3.05, 0.0)
    add_text(L_TANK_2D, 3, "Paso Libre ->", TX + 1.22, TY + 3.45, 0.0, 0.12)
    for tcx, tcy in tank_centers:
        for s_i in range(N_SEG):
            a0, a1 = 2.0 * math.pi * s_i / N_SEG, 2.0 * math.pi * (s_i + 1) / N_SEG
            add_line(L_TANK_2D, 5, TX + tcx + TANK_R * math.cos(a0), TY + tcy + TANK_R * math.sin(a0), 0.0,
                                   TX + tcx + TANK_R * math.cos(a1), TY + tcy + TANK_R * math.sin(a1), 0.0)
    add_rect_2d(L_TANK_2D, 5, TX + 1.95, TY + 2.75, TX + 2.68, TY + 3.15)
    add_text(L_TANK_2D, 2, "2 Tanques 1000L + Hidroneumatico", TX + 3.20, TY + 2.00, 0.0, 0.16)

    FX, FY = 16.00, 23.00
    L_FAC = "FACHADAS_2D"
    add_text(L_FAC, 2, "CORTE TRANSVERSAL 3 PISOS + CLARABOYA CON ABERTURA REAL DE LUZ Y AIRE", FX - 0.2, FY - 3.3, 0.0, 0.20)
    add_rect_2d(L_FAC, 4,  FX + 0.15, FY + Z_SOT_FLOOR, FX + 9.15, FY + 0.00)        # Sótano Bodega
    add_rect_2d(L_FAC, 8,  FX + 0.00, FY + Z_SOT_FLOOR, FX + 0.15, FY + 2.50)        # Muro vecino izquierdo
    add_rect_2d(L_FAC, 7,  FX + 0.15, FY + 0.00,        FX + 9.15, FY + 3.00)        # Planta Baja
    add_rect_2d(L_FAC, 8,  FX + 9.15, FY + 0.00,        FX + 11.37, FY + 2.68)       # Portón Derecho Av.4 Bodega
    add_rect_2d(L_FAC, 34, FX + 0.15, FY + 3.00,        FX + 9.15, FY + 6.00)        # Segundo Piso Social
    add_rect_2d(L_FAC, 5,  FX + 0.15, FY + 6.00,        FX + 9.15, FY + 8.85)        # Nuevo Tercer Piso Penthouse
    add_rect_2d(L_FAC, 34, FX + 0.15, FY + 8.85,        FX + 0.30, FY + Z_PARAPET_BUH)
    # Faldones recortados en X = 2.45..5.55 mostrando el paso franco de luz y aire bajo la linterna!
    add_line(L_FAC, 9, FX + 0.40,    FY + z_w_bot, 0.0, FX + X_SKY_W,     FY + z_sky_w,     0.0)
    add_line(L_FAC, 9, FX + X_SKY_E, FY + z_sky_e, 0.0, FX + X_EAVE_EAST, FY + Z_EAVE_EAST, 0.0)
    add_line(L_FAC, 4, FX + X_SKY_W, FY + z_sky_w, 0.0, FX + X_SKY_W,     FY + Z_LOUV_TOP,  0.0)
    add_line(L_FAC, 4, FX + X_SKY_E, FY + z_sky_e, 0.0, FX + X_SKY_E,     FY + Z_LOUV_TOP,  0.0)
    add_line(L_FAC, 9, FX + X_SKY_W - 0.40, FY + Z_LOUV_TOP, 0.0, FX + X_SKY_MID,      FY + Z_SKY_TOP,  0.0)
    add_line(L_FAC, 9, FX + X_SKY_MID,      FY + Z_SKY_TOP,  0.0, FX + X_SKY_E + 0.40, FY + Z_LOUV_TOP, 0.0)
    add_text(L_FAC, 1, "Alero Izq. 0,00m (Respeto Vecino)", FX - 0.60, FY + 11.15, 0.0, 0.15)
    add_text(L_FAC, 4, "Boca Real Luz + Aire (3,10m)", FX + 2.35, FY + Z_SKY_TOP + 0.22, 0.0, 0.15)
    add_text(L_FAC, 1, "Puerta Der. Av.4", FX + 9.25, FY + 2.85, 0.0, 0.14)

    # Levantamiento Poligonal UTM intacto
    UX, UY = 75.00, 2.00
    L_UTM = "LEVANTAMIENTO_POLIGONAL_UTM"
    for de in range(0, 41, 10):
        add_line(L_UTM, 8, UX + de, UY + 0.0, 0.0, UX + de, UY + 40.0, 0.0)
        add_text(L_UTM, 7, f"E.={529750 + de},00", UX + de - 1.5, UY - 1.2, 0.0, 0.32)
    for dn in range(0, 41, 10):
        add_line(L_UTM, 8, UX + 0.0, UY + dn, 0.0, UX + 40.0, UY + dn, 0.0)
        add_text(L_UTM, 7, f"N.=1.141.{640 + dn},00", UX - 6.5, UY + dn - 0.15, 0.0, 0.32)
    P1_U, P2_U, P3_U, P4_U = (UX + 5.04, UY + 24.17), (UX + 14.60, UY + 30.33), (UX + 27.07, UY + 8.99), (UX + 17.99, UY + 3.13)
    add_line(L_UTM, 1, P1_U[0], P1_U[1], 0.0, P2_U[0], P2_U[1], 0.0)
    add_line(L_UTM, 1, P2_U[0], P2_U[1], 0.0, P3_U[0], P3_U[1], 0.0)
    add_line(L_UTM, 1, P3_U[0], P3_U[1], 0.0, P4_U[0], P4_U[1], 0.0)
    add_line(L_UTM, 1, P4_U[0], P4_U[1], 0.0, P1_U[0], P1_U[1], 0.0)

    # =========================================================================
    # 7. ESCRITURA DEL ARCHIVO DXF R12 (AC1009 ESTRICTO, CERO CAPAS HUÉRFANAS)
    # =========================================================================
    used_layers = {}
    for b in boxes_3d:
        used_layers.setdefault(b[0], b[1])
    for h in hexahedra_3d:
        used_layers.setdefault(h[0], h[1])
    for ln in lines_2d:
        used_layers.setdefault(ln[0], ln[1])
    for tx in texts:
        used_layers.setdefault(tx[0], tx[1])

    all_layers = [("0", 7)] + [(lname, lcol) for lname, lcol in used_layers.items() if lname != "0"]

    dxf_lines = []
    def w(code, val):
        dxf_lines.append(f"{code:>3}\n{val}\n")

    w(0, "SECTION")
    w(2, "HEADER")
    w(9, "$ACADVER"); w(1, "AC1009")
    w(9, "$INSUNITS"); w(70, 6)
    w(9, "$EXTMIN"); w(10, -5.0); w(20, -10.0); w(30, -4.0)
    w(9, "$EXTMAX"); w(10, 120.0); w(20, 48.0); w(30, 13.5)
    w(0, "ENDSEC")

    w(0, "SECTION")
    w(2, "TABLES")
    w(0, "TABLE")
    w(2, "LAYER")
    w(70, len(all_layers))
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
        w(0, "3DFACE"); w(8, layer); w(62, color)
        w(10, f"{p1[0]:.4f}"); w(20, f"{p1[1]:.4f}"); w(30, f"{p1[2]:.4f}")
        w(11, f"{p2[0]:.4f}"); w(21, f"{p2[1]:.4f}"); w(31, f"{p2[2]:.4f}")
        w(12, f"{p3[0]:.4f}"); w(22, f"{p3[1]:.4f}"); w(32, f"{p3[2]:.4f}")
        w(13, f"{p4[0]:.4f}"); w(23, f"{p4[1]:.4f}"); w(33, f"{p4[2]:.4f}")

    for layer, color, x1, y1, z1, x2, y2, z2 in boxes_3d:
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

    for layer, color, x1, y1, z1, x2, y2, z2 in lines_2d:
        w(0, "LINE"); w(8, layer); w(62, color)
        w(10, f"{x1:.4f}"); w(20, f"{y1:.4f}"); w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}"); w(21, f"{y2:.4f}"); w(31, f"{z2:.4f}")

    for layer, color, txt, x, y, z, h in texts:
        w(0, "TEXT"); w(8, layer); w(62, color)
        w(10, f"{x:.4f}"); w(20, f"{y:.4f}"); w(30, f"{z:.4f}")
        w(40, f"{h:.4f}"); w(1, txt)

    w(0, "ENDSEC")
    w(0, "EOF")

    out_path = "02_Modelos_CAD/casa_proyecto_3_pisos.dxf"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="latin-1", errors="replace") as f:
        f.writelines(dxf_lines)

    # Auditoría geométrica automática de lindero izquierdo (minX >= 0.15 m para toda la edificación)
    house_layers_exclude = {L_TERR, L_FENCE, L_GRID, L_SOT_2D, L_PB_2D, L_P2_2D, L_P3_2D, L_TANK_2D, L_FAC, L_UTM}
    min_x_house = min(
        [b[2] for b in boxes_3d if b[0] not in house_layers_exclude] +
        [pt[0] for h in hexahedra_3d if h[0] not in house_layers_exclude for pt in h[2]]
    )
    max_z_house = max(
        [b[7] for b in boxes_3d if b[0] not in house_layers_exclude] +
        [pt[2] for h in hexahedra_3d if h[0] not in house_layers_exclude for pt in h[2]]
    )

    print(f"DXF 3 Pisos + Bodega generado exitosamente: {out_path}")
    print(f"Solidos 3D: {len(boxes_3d) + len(hexahedra_3d)} | Lineas 2D: {len(lines_2d)} | Textos: {len(texts)} | Capas: {len(all_layers)}")
    print(f"Auditoria Lindero Izquierdo minX edificacion = {min_x_house:.4f} m (Requerido >= 0.1500 m) | Cota maxima Z = {max_z_house:.2f} m")


if __name__ == "__main__":
    build_casa_3_pisos()
