"""
Generador Maestro del Proyecto Rediseño Chalet Rústico Mejorado ("02_Modelos_CAD/casa_nuevo_proyecto.dxf")
Basado en "casa_modificaciones.dxf" (dejando el archivo original 100% intacto).

INTEGRA LOS 4 PASOS DEL PLAN APROBADO:
1. PASO 1 — Estacionamiento Ampliado Conservando Columnas Existentes:
   - Se conservan el 100% de las columnas existentes en su posición original (Eje 0 en X = 0,275 m
     y Eje 1 en X = 2,825 m, sección 25 x 25 cm).
   - Muro divisorio no estructural retranqueado a X = 3,30..3,45 m creando bolsillos de 3,00 m de
     pared a pared entre columnas (tramos libres de 4,05 m, 2,90 m y 2,76 m) para abrir puertas
     holgadamente sin demoler ni recalzar ninguna columna existente; portón de 2,30 x 2,40 m entre
     columnas frontales A0.
2. PASO 2 — Regularización Rectangular (9,00 x 21,71 m) + Entrada Exterior al Sótano:
   - Nuevo bloque posterior derecho (X = 6,25..9,15 m, Y_casa = 0,00..3,50 m) continuo desde
     Sótano hasta Último Piso + Columna 32 esquinera.
   - SÓTANO: Mantiene la escalera interior intacta y suma la nueva Entrada Exterior Principal
     desde el Patio Trasero (Y_casa = 0,00 m, Z = -2,55 m) hacia un Recibidor / Estudio Jardín
     conectado a la Sala y al distribuidor; ventilación directa al sur para el baño del sótano.
   - PLANTA BAJA: Nueva Oficina Privada de Gerencia con doble ventana (Este y Sur) conectada
     desde el área administrativa trasera sin afectar el salón comercial ni su baño.
3. PASO 3 — Nueva Distribución Interior del Último Piso Chalet (Z = +3,00 m):
   - Doble terraza frontal independiente en Avenida 4: Gran Balconada Rústica Social (5,55 x 1,96 m)
     y Terraza Privada exclusiva de la Master Suite (3,00 x 1,96 m) separadas por muro en Eje 2.
   - Master Suite Chalet de Gran Formato (32,88 m² totales): Terraza Privada (5,88 m²) + Dormitorio
     (3,00 x 4,50 m) + Gran Vestier Walk-In doble frente (3,00 x 2,20 m) + Gran Baño Spa (3,00 x 2,30 m)
     tomando espacio de la antigua Habitación 2.
   - Reubicación armónica hacia el nuevo bloque rectangular: Habitación 2 (3,00 x 3,55 m),
     Baño Familiar central (3,00 x 1,85 m) y Habitación 3 esquinera ampliada (3,00 x 4,15 m).
   - Gran Salón - Comedor diáfano SIN chimenea + Cocina Rústica con Isla Maciza + Escalera intacta
     + Lavandería y Estar/Mirador Sur.
4. PASO 4 — Envolvente y Cubierta Chalet Rústico Respetando Colindancia Izquierda:
   - CERO invasión al vecino izquierdo (X < 0,15 m libre de muros, contraventanas y aleros).
   - Parapeto cortafuegos propio en X = 0,15..0,30 m + canalón pluvial oculto interno en X = 0,30..0,55 m.
   - Cubierta alpina a dos aguas (32°, cumbrera en X = 4,85 m, Z = +8,70 m) con alero derecho de
     0,95 m (X = 9,15..10,10 m < lindero 10,80 m) y alero sur de 1,00 m sobre patio propio,
     cerchas vistas, canecillos expuestos, barandas en Cruz de San Andrés y carpintería con shutters.
"""

import math
import os


def build_nuevo_proyecto():
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
    # PARÁMETROS VERTICALES Y GEOMÉTRICOS CENTRALES
    # =========================================================================
    Z_SOT_SLAB_BOT = -2.70
    Z_SOT_FLOOR    = -2.55   # Nivel piso acabado Sótano y Patio Trasero
    Z_P1_SLAB_BOT  = -0.15   # Fondo de losa entrepiso Primer Piso
    Z_P1_FLOOR     =  0.00   # Nivel piso acabado Planta Baja (Local Comercial + Garaje)
    H_P1           =  2.85   # Tope muros Planta Baja / Fondo losa Segundo Piso
    Z_P2_FLOOR     =  3.00   # Nivel piso acabado Último Piso Chalet
    H_P2           =  5.85   # Nivel solera muros Último Piso
    H_DOOR         =  2.10
    H_DOOR_SOT     =  2.05

    # Parámetros de Cubierta Chalet Alpino con Respeto de Colindancia Izquierda
    X_RIDGE        =  4.85   # Eje de cumbrera longitudinal Norte-Sur (m)
    SLOPE_TAN      =  math.tan(math.radians(32.0))  # Pendiente alpina 32° (~62.5%)
    X_GUTTER_IN    =  0.45   # Arranque faldón oeste dentro del canalón oculto propio (X >= 0.15 m!)
    Z_GUTTER_EAVE  =  5.95   # Cota inferior faldón oeste en canalón oculto
    Z_RIDGE        =  Z_GUTTER_EAVE + (X_RIDGE - X_GUTTER_IN) * SLOPE_TAN  # ~8.70 m
    ROOF_THICK     =  0.18   # Espesor tablero + aislamiento + teja rústica/pizarra
    ALERO_ESTE     =  0.95   # Voladizo hacia retiro lateral derecho propio (X = 9.15 -> 10.10 < 10.80 m)
    ALERO_SUR      =  1.00   # Voladizo hacia patio trasero propio (Y_casa = 0.00 -> -1.00 m)
    X_EAVE_EAST    =  9.15 + ALERO_ESTE  # 10.10 m (100% dentro de la parcela)
    Z_EAVE_EAST    =  Z_RIDGE - (X_EAVE_EAST - X_RIDGE) * SLOPE_TAN  # ~5.42 m
    Z_PARAPET_WEST =  6.28   # Tope parapeto cortafuegos izquierdo propio (X = 0.15..0.30 m)

    def z_roof_under(x):
        if x <= X_RIDGE:
            return Z_GUTTER_EAVE + (x - X_GUTTER_IN) * SLOPE_TAN
        return Z_RIDGE - (x - X_RIDGE) * SLOPE_TAN

    # Implantación dentro de la parcela poligonal UTM (24.71 m de largo)
    OFFSET_X = 0.00   # X = 0.00..0.15 pared del vecino INTOCABLE; X = 0.15..0.30 muro propio
    OFFSET_Y = 3.00   # Retiro de fondo de 3.00 m (Patio Trasero a cota Z = -2.55 m)
    Y_AV4    = 21.71  # Lindero frontal Avenida 4 (Y_terreno = 24.71 m)

    # Parámetros Opción A del Estacionamiento (3,00 m libres reales)
    X_GAR_LEFT_IN  = 0.30
    X_GAR_RIGHT_IN = 3.30
    X_GAR_WALL_OUT = 3.45
    X_EJE_1_GAR    = 3.375

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

    # Helper para carpintería rústica (marco + cuarterones + contraventanas shutters exteriores)
    L_CARP = "P2_CARPINTERIA_RUSTICA_3D"

    def add_rustic_window_east(y1, y2, z1, z2, with_shutters=True):
        # Marco perimetral de madera en X = 8.98..9.17
        t_f = 0.06
        add_house_box(L_CARP, 34, 8.98, y1, z1, 9.17, y2, z1 + t_f)
        add_house_box(L_CARP, 34, 8.98, y1, z2 - t_f, 9.17, y2, z2)
        add_house_box(L_CARP, 34, 8.98, y1, z1 + t_f, 9.17, y1 + t_f, z2 - t_f)
        add_house_box(L_CARP, 34, 8.98, y2 - t_f, z1 + t_f, 9.17, y2, z2 - t_f)
        # Parteluz / cuarterones centrales
        ym = 0.5 * (y1 + y2)
        zm = 0.5 * (z1 + z2)
        add_house_box(L_CARP, 34, 9.05, ym - 0.02, z1 + t_f, 9.10, ym + 0.02, z2 - t_f)
        add_house_box(L_CARP, 34, 9.05, y1 + t_f, zm - 0.02, 9.10, y2 - t_f, zm + 0.02)
        # Contraventanas exteriores batientes abiertas sobre fachada Este (propias, X = 9.15..9.21)
        if with_shutters and (y2 - y1) >= 1.20:
            sh_w = min(0.38, 0.35 * (y2 - y1))
            if y1 - sh_w > 0.25:
                add_house_box(L_CARP, 34, 9.15, y1 - sh_w, z1, 9.20, y1 - 0.02, z2)
            if y2 + sh_w < Y_AV4 - 0.25:
                add_house_box(L_CARP, 34, 9.15, y2 + 0.02, z1, 9.20, y2 + sh_w, z2)

    def add_rustic_window_south(x1, x2, z1, z2, with_shutters=True):
        # Marco perimetral de madera en fachada Sur (Y_casa = -0.02..0.17, hacia patio propio)
        t_f = 0.06
        add_house_box(L_CARP, 34, x1, -0.02, z1, x2, 0.17, z1 + t_f)
        add_house_box(L_CARP, 34, x1, -0.02, z2 - t_f, x2, 0.17, z2)
        add_house_box(L_CARP, 34, x1, -0.02, z1 + t_f, x1 + t_f, 0.17, z2 - t_f)
        add_house_box(L_CARP, 34, x2 - t_f, -0.02, z1 + t_f, x2, 0.17, z2 - t_f)
        xm = 0.5 * (x1 + x2)
        zm = 0.5 * (z1 + z2)
        add_house_box(L_CARP, 34, xm - 0.02, 0.05, z1 + t_f, xm + 0.02, 0.10, z2 - t_f)
        add_house_box(L_CARP, 34, x1 + t_f, 0.05, zm - 0.02, x2 - t_f, 0.10, zm + 0.02)
        # Contraventanas siempre respetando X >= 0.20 m (cero invasión vecino izquierdo)
        if with_shutters and (x2 - x1) >= 1.20:
            sh_w = 0.36
            if x1 - sh_w >= 0.25:
                add_house_box(L_CARP, 34, x1 - sh_w, -0.05, z1, x1 - 0.02, 0.00, z2)
            if x2 + sh_w <= 8.95:
                add_house_box(L_CARP, 34, x2 + 0.02, -0.05, z1, x2 + sh_w, 0.00, z2)

    # Helper para barandilla alpina con Cruz de San Andrés
    L_BALC = "P2_BALCON_MADERA_3D"

    def add_alpine_railing_x(x1, x2, y_center, z_floor, h_rail=1.05, n_bays=4):
        half_t = 0.06
        # Zócalo inferior y pasamanos superior de madera labrada
        add_house_box(L_BALC, 30, x1, y_center - half_t, z_floor + 0.05, x2, y_center + half_t, z_floor + 0.13)
        add_house_box(L_BALC, 30, x1, y_center - 0.08, z_floor + h_rail - 0.08, x2, y_center + 0.08, z_floor + h_rail)
        dx = (x2 - x1) / n_bays
        for b in range(n_bays + 1):
            px = x1 + b * dx
            add_house_box(L_BALC, 30, max(x1, px - 0.06), y_center - 0.07, z_floor,
                                      min(x2, px + 0.06), y_center + 0.07, z_floor + h_rail)
        # Aspas diagonales en Cruz de San Andrés (sólidos 3D inclinados limpios)
        for b in range(n_bays):
            bx1 = x1 + b * dx + 0.06
            bx2 = x1 + (b + 1) * dx - 0.06
            bz1 = z_floor + 0.13
            bz2 = z_floor + h_rail - 0.08
            t_d = 0.05
            # Diagonal 1: (bx1, bz1) -> (bx2, bz2)
            add_house_hexa(L_BALC, 30, [
                (bx1, y_center - 0.03, bz1), (bx1 + t_d, y_center - 0.03, bz1),
                (bx1 + t_d, y_center + 0.03, bz1), (bx1, y_center + 0.03, bz1),
                (bx2 - t_d, y_center - 0.03, bz2), (bx2, y_center - 0.03, bz2),
                (bx2, y_center + 0.03, bz2), (bx2 - t_d, y_center + 0.03, bz2),
            ])
            # Diagonal 2: (bx2, bz1) -> (bx1, bz2)
            add_house_hexa(L_BALC, 30, [
                (bx2 - t_d, y_center - 0.03, bz1), (bx2, y_center - 0.03, bz1),
                (bx2, y_center + 0.03, bz1), (bx2 - t_d, y_center + 0.03, bz1),
                (bx1, y_center - 0.03, bz2), (bx1 + t_d, y_center - 0.03, bz2),
                (bx1 + t_d, y_center + 0.03, bz2), (bx1, y_center + 0.03, bz2),
            ])

    def add_alpine_railing_y(x_center, y1, y2, z_floor, h_rail=1.05, n_bays=2):
        half_t = 0.06
        add_house_box(L_BALC, 30, x_center - half_t, y1, z_floor + 0.05, x_center + half_t, y2, z_floor + 0.13)
        add_house_box(L_BALC, 30, x_center - 0.08, y1, z_floor + h_rail - 0.08, x_center + 0.08, y2, z_floor + h_rail)
        dy = (y2 - y1) / n_bays
        for b in range(n_bays + 1):
            py = y1 + b * dy
            add_house_box(L_BALC, 30, x_center - 0.07, max(y1, py - 0.06), z_floor,
                                      x_center + 0.07, min(y2, py + 0.06), z_floor + h_rail)
        for b in range(n_bays):
            by1 = y1 + b * dy + 0.06
            by2 = y1 + (b + 1) * dy - 0.06
            bz1 = z_floor + 0.13
            bz2 = z_floor + h_rail - 0.08
            t_d = 0.05
            add_house_hexa(L_BALC, 30, [
                (x_center - 0.03, by1, bz1), (x_center + 0.03, by1, bz1),
                (x_center + 0.03, by1 + t_d, bz1), (x_center - 0.03, by1 + t_d, bz1),
                (x_center - 0.03, by2 - t_d, bz2), (x_center + 0.03, by2 - t_d, bz2),
                (x_center + 0.03, by2, bz2), (x_center - 0.03, by2, bz2),
            ])
            add_house_hexa(L_BALC, 30, [
                (x_center - 0.03, by2 - t_d, bz1), (x_center + 0.03, by2 - t_d, bz1),
                (x_center + 0.03, by2, bz1), (x_center - 0.03, by2, bz1),
                (x_center - 0.03, by1, bz2), (x_center + 0.03, by1, bz2),
                (x_center + 0.03, by1 + t_d, bz2), (x_center - 0.03, by1 + t_d, bz2),
            ])

    # =========================================================================
    # 1. NIVEL SÓTANO (Z = -2.55 a -0.15 m) — RECTANGULAR + ENTRADA PATIO TRASERO
    # =========================================================================
    L_SOT_SLAB = "SOTANO_LOSA_3D"
    L_SOT_EXT  = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT  = "SOTANO_MUROS_INT_3D"
    L_SOT_COL  = "SOTANO_COLUMNAS_3D"

    # Losa Sótano ahora 100% rectangular (X: 0.15 a 9.15 m, Y: 0.00 a 8.30 m)
    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)
    # Planchada / umbral exterior de piedra hacia el Patio Trasero frente a la nueva puerta del Sótano
    add_house_box(L_SOT_SLAB, 8, 6.40, -0.75, Z_SOT_FLOOR - 0.08, 9.00, 0.00, Z_SOT_FLOOR + 0.02)

    # Escalera Interior Tramo 1 INTACTA: Baja de P1 (Z=0.00 en Y=7.40) a Sótano (Z=-2.55 en Y=4.45), X: 0.30..1.40
    num_steps = 12
    step_dy = (7.40 - 4.45) / num_steps
    step_dz = (0.00 - Z_SOT_FLOOR) / num_steps
    for i in range(num_steps):
        y_s_top = 7.40 - i * step_dy
        y_s_bot = y_s_top - step_dy
        z_s_top = 0.00 - i * step_dz
        add_house_box("ESCALERA_3D", 7, 0.30, y_s_bot, Z_SOT_FLOOR, 1.40, y_s_top, z_s_top)
        add_house_line("ESCALERA_2D", 7, 0.30, y_s_bot, 0.0, 1.40, y_s_bot, 0.0)

    # Muro Oeste Propio en Sótano (X: 0.15..0.30, Y: 0.00..8.30) — Ciego junto a vecino
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur Completo hacia Patio Trasero (Y: 0.00..0.15, X: 0.30..9.15) con NUEVA ENTRADA EXTERIOR SÓTANO:
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 9.15, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.60, 2.50, Z_SOT_FLOOR + 1.00, Z_SOT_FLOOR + 2.10),  # Ventana Habitación 1 Sótano
        (3.40, 4.10, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Celosía Lavadero Sótano
        (5.10, 5.90, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.10),  # Nueva Celosía directa Baño Sótano al Patio
        (6.50, 7.35, Z_SOT_FLOOR + 0.95, Z_SOT_FLOOR + 2.10),  # Nuevo Ventanal Recibidor/Estudio Jardín
        (7.60, 8.70, Z_SOT_FLOOR,        Z_SOT_FLOOR + H_DOOR_SOT),  # NUEVA PUERTA EXTERIOR SÓTANO (1.10 x 2.05m)
    ])
    # Marco rústico de madera para la nueva puerta exterior del Sótano en el Patio Trasero
    add_house_box(L_CARP, 34, 7.54, -0.03, Z_SOT_FLOOR, 7.62, 0.18, Z_SOT_FLOOR + H_DOOR_SOT + 0.06)
    add_house_box(L_CARP, 34, 8.68, -0.03, Z_SOT_FLOOR, 8.76, 0.18, Z_SOT_FLOOR + H_DOOR_SOT + 0.06)
    add_house_box(L_CARP, 34, 7.54, -0.03, Z_SOT_FLOOR + H_DOOR_SOT, 8.76, 0.18, Z_SOT_FLOOR + H_DOOR_SOT + 0.08)

    # Muro Este Completo del Sótano sobre Eje 3 (X: 8.95..9.15, Y: 0.15..8.30) con ventana al jardín en nuevo bloque
    add_wall_with_openings_y(L_SOT_EXT, 4, 8.95, 9.15, 0.15, 8.30, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.15, 2.45, Z_SOT_FLOOR + 0.95, Z_SOT_FLOOR + 2.10),  # Ventana Este del Recibidor/Estudio Sótano
    ])

    # Muro Norte de Contención del Sótano (Y: 8.15..8.30, X: 0.30..9.15)
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # Tabiquería Interna del Sótano (aprovechando el nuevo bloque rectangular):
    add_wall_with_openings_x(L_SOT_INT, 4, 0.30, 6.00, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (3.95, 4.95, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
    ])
    # Vano/Arco amplio (1.80 m) integrando el nuevo Recibidor/Estudio con la Sala del Sótano
    add_wall_with_openings_x(L_SOT_INT, 4, 6.00, 8.95, 3.50, 3.65, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (6.65, 8.45, Z_SOT_FLOOR, Z_SOT_FLOOR + 2.15),
    ])
    # Tabique X = 6.25..6.40 ahora interior con puerta (Y = 2.35..3.25) del Recibidor hacia Baño/Comedor
    add_wall_with_openings_y(L_SOT_INT, 4, 6.25, 6.40, 0.15, 3.50, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (2.35, 3.25, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),
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

    # Columnas Sótano (respetando X >= 0.15 m de medianera vecina y escalera X = 0.30..1.40 m)
    add_house_box(L_SOT_COL, 1, 0.15, 6.35, Z_SOT_FLOOR, 0.30, 6.80, Z_P1_SLAB_BOT)  # Machón enrasado junto a escalera
    sot_cols_axes = [
        (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
        (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
        (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)

    # =========================================================================
    # 2. NIVEL PLANTA BAJA (Z = 0.00 a +2.85 m) — GARAJE 3,00m + NUEVA OFICINA
    # =========================================================================
    L_P1_SLAB   = "LOSA_PISO_3D"
    L_P1_EXT    = "MUROS_EXTERIORES_3D"
    L_P1_INT    = "MUROS_INTERIORES_3D"
    L_P1_COL    = "COLUMNAS_3D"
    L_ZOCALO    = "PB_ZOCALO_PIEDRA_3D"

    # Losa Planta Baja 100% rectangular (9.00 x 21.71 m) respetando caja de escalera al sótano
    add_house_box(L_P1_SLAB, 8, 0.15, 0.00, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR)
    add_house_box(L_P1_SLAB, 8, 0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR)

    # 1. Muro Lateral Izquierdo PROPIO (X: 0.15..0.30, Y: 0.00..21.71 m) — CERO invasión a X < 0.15
    add_house_box(L_P1_EXT, 7, 0.15, 0.00, Z_P1_FLOOR, X_GAR_LEFT_IN, Y_AV4, H_P1)

    # 2. Fachada Frontal sobre Avenida 4 (Columnas existentes A0 conservadas + 2 Vitrinas Comerciales)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, Y_AV4 - 0.15, Y_AV4, Z_P1_FLOOR, H_P1, [
        (0.40, 2.70, 0.00, 2.40),   # Portón Vehicular entre columnas existentes A0 (2.30 x 2.40 m)
        (3.65, 5.75, 0.00, 2.40),   # Vitrina Comercial 1 (2.10 x 2.40 m)
        (6.20, 8.80, 0.00, 2.40),   # Vitrina Comercial 2 (2.60 x 2.40 m)
    ])
    # Pilastras frontales en piedra rústica respetando columnas existentes y vitrinas
    for px1, px2 in [(0.15, 0.40), (2.70, 3.65), (5.75, 6.20), (8.80, 9.15)]:
        add_house_box(L_ZOCALO, 8, px1, Y_AV4 - 0.22, Z_P1_FLOOR, px2, Y_AV4, H_P1)

    # 3. Muro Lateral Derecho continuo sobre Eje 3 desde Y = 0.00 hasta Av. 4 (X: 9.00..9.15)
    add_wall_with_openings_y(L_P1_EXT, 7, 9.00, 9.15, 0.00, Y_AV4, Z_P1_FLOOR, H_P1, [
        (1.10,  2.50, 1.00, 2.10),  # Nueva Ventana Este de Oficina Privada de Gerencia
        (4.10,  5.00, 1.10, 2.00),  # Ventana Baño Local
        (6.30,  8.00, 1.00, 2.10),
        (9.65, 11.85, 1.00, 2.10),
        (13.15, 14.05, 1.10, 2.00),
        (15.50, 17.70, 1.00, 2.10),
        (18.80, 21.00, 1.00, 2.10),
    ])
    # Zócalo rústico de piedra exterior derecho (X = 9.15..9.22, dentro de retiro propio)
    add_house_box(L_ZOCALO, 8, 9.15, 0.00, Z_P1_FLOOR, 9.21, Y_AV4, 0.95)

    # 4. Muro Sur Posterior completo de Planta Baja (Y: 0.00..0.15, X: 0.15..9.15)
    add_wall_with_openings_x(L_P1_EXT, 7, 0.15, 9.15, 0.00, 0.15, Z_P1_FLOOR, H_P1, [
        (0.55, 2.35, 1.15, 2.60),   # Ventana área apoyo
        (4.10, 5.10, 1.00, 2.10),   # Ventana depósito comercial
        (7.00, 8.40, 1.00, 2.10),   # Nuevo Ventanal Sur de Oficina Privada de Gerencia
    ])

    # --- MUROS INTERIORES PLANTA BAJA ---
    # Garaje de 3,00 m libres (Opción A) + escaleras intactas
    add_house_box(L_P1_INT, 7, 2.75, 0.15, Z_P1_FLOOR, 2.90, 8.80, H_P1)
    add_house_box(L_P1_INT, 7, X_GAR_RIGHT_IN, 8.95, Z_P1_FLOOR, X_GAR_WALL_OUT, Y_AV4 - 0.15, H_P1)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, X_GAR_WALL_OUT, 8.80, 8.95, Z_P1_FLOOR, H_P1, [
        (1.65, 2.55, 0.00, H_DOOR),
    ])
    add_house_box(L_P1_INT, 7, 1.40, 4.40, Z_P1_FLOOR, 1.55, 7.35, H_P1)
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 4.25, 4.40, Z_P1_FLOOR, H_P1, [
        (1.65, 2.45, 0.00, H_DOOR),
    ])
    add_wall_with_openings_x(L_P1_INT, 7, 0.30, 2.75, 1.65, 1.80, Z_P1_FLOOR, H_P1, [
        (0.95, 2.05, 0.00, H_DOOR),
    ])

    # Baño Local intacto + Depósito conectado a la NUEVA Oficina Privada de Gerencia (X: 6.40..9.00, Y: 0.15..3.50)
    add_house_box(L_P1_INT, 7, 5.85, 5.40, Z_P1_FLOOR, 9.00, 5.55, H_P1)
    add_wall_with_openings_y(L_P1_INT, 7, 5.85, 6.00, 3.65, 5.40, Z_P1_FLOOR, H_P1, [
        (3.95, 4.75, 0.00, H_DOOR),
    ])
    add_house_box(L_P1_INT, 7, 6.00, 3.50, Z_P1_FLOOR, 9.00, 3.65, H_P1)  # Separa Baño Local de Oficina Gerencia
    add_wall_with_openings_x(L_P1_INT, 7, 2.90, 6.25, 3.50, 3.65, Z_P1_FLOOR, H_P1, [
        (4.05, 4.90, 0.00, H_DOOR),
    ])
    add_wall_with_openings_y(L_P1_INT, 7, 6.25, 6.40, 0.15, 3.50, Z_P1_FLOOR, H_P1, [
        (1.30, 2.20, 0.00, H_DOOR),  # Puerta hacia la nueva Oficina Privada de Gerencia
    ])

    # --- COLUMNAS PLANTA BAJA Y ÚLTIMO PISO (100% CONSERVADAS EN SU POSICIÓN ORIGINAL) ---
    L_P2_COL    = "P2_COLUMNAS_3D"
    L_TIMBER    = "P2_TIMBER_FRAME_3D"

    # Las 28 columnas existentes de 25x25 cm de casa_modificaciones.dxf + 2 nuevas en el bloque posterior (Eje H)
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
        # Columnas de amarre posterior Eje H = 0.125 (cajón portante tanque + nuevo bloque rectangular)
        (0.275, 0.125),  (2.825, 0.125),  (5.925, 0.125),  (9.075, 0.125),
    ]
    for cx, cy in existing_and_new_cols:
        add_house_box(L_P1_COL, 1, cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)
        z_col_p2_top = 5.50 if (cx < 3.0 and cy < 4.0) else H_P2
        add_house_box(L_P2_COL, 1, cx - 0.125, cy - 0.125, Z_P2_FLOOR, cx + 0.125, cy + 0.125, z_col_p2_top)

    # Revestimiento rústico de madera maciza (Timber Frame Posts) en P2 para las columnas vistas de Eje 1 y Eje 0
    for cy_post in [21.585, 18.575, 16.325, 12.025, 8.875, 6.575]:
        y_p2_max = min(Y_AV4, cy_post + 0.145)
        add_house_box(L_TIMBER, 34, 2.68, cy_post - 0.145, Z_P2_FLOOR, 2.97, y_p2_max, H_P2)
    for cy_west in [21.585, 18.575, 16.325]:
        y_w_max = min(Y_AV4, cy_west + 0.145)
        add_house_box(L_TIMBER, 34, 0.15, cy_west - 0.145, Z_P2_FLOOR, 0.42, y_w_max, H_P2)

    # Viga maestra longitudinal Timber Frame en P2 uniendo el tope de toda la fila de columnas Eje 1 (X = 2.825)
    add_house_box(L_TIMBER, 34, 2.68, 6.45, H_P2 - 0.22, 2.97, Y_AV4, H_P2)

    # =========================================================================
    # 3. ÚLTIMO PISO: RESIDENCIA CHALET RÚSTICO MEJORADA (Z = +3.00 m)
    # =========================================================================
    L_P2_SLAB = "P2_LOSA_PISO_3D"
    L_P2_EXT  = "P2_MUROS_MADERA_EXT_3D"
    L_P2_INT  = "P2_MUROS_MADERA_INT_3D"
    L_P2_ISL  = "P2_COCINA_ISLA_3D"
    L_ROOF    = "CUBIERTA_CHALET_3D"
    L_GUTTER  = "CANALON_OCULTO_PROPIO_3D"

    # Losa Entrepiso P2 ahora 100% rectangular (9.00 x 21.71 m) respetando caja de escalera intacta
    add_house_box(L_P2_SLAB, 8, 0.15, 0.00, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 4.40, H_P1, 0.30, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR)

    # Escalera Tramo 2 INTACTA: Sube de P1 (Z=0.00 en Y=7.35) a P2 (Z=+3.00 en Y=4.40), X: 1.55..2.65
    num_steps_p2 = 14
    step_dy_p2 = (7.35 - 4.40) / num_steps_p2
    step_dz_p2 = (Z_P2_FLOOR - Z_P1_FLOOR) / num_steps_p2
    for i in range(num_steps_p2):
        y_s_bot = 7.35 - (i + 1) * step_dy_p2
        y_s_top = 7.35 - i * step_dy_p2
        z_s_bot = Z_P1_FLOOR + i * step_dz_p2
        z_s_top = z_s_bot + step_dz_p2
        add_house_box("P2_ESCALERA_3D", 7, 1.55, y_s_bot, z_s_bot - 0.15, 2.65, y_s_top, z_s_top)

    # --- RESPETO ESTRICTO A MEDIANERA IZQUIERDA (X = 0.15..0.30 m) ---
    # Tramo Buhardilla Tanque (Y: 0.00..4.45 m -> sube hasta Z = 7.85 m) + Tramo Principal (Y: 4.45..21.71 m -> Z = 6.28 m)
    Z_PARAPET_BUH = 7.85
    add_house_box(L_P2_EXT, 34, 0.15, 0.00, Z_P2_FLOOR, 0.30, 4.45, Z_PARAPET_BUH)
    add_house_box(L_P2_EXT, 34, 0.15, 4.45, Z_P2_FLOOR, 0.30, Y_AV4, Z_PARAPET_WEST)
    # Albardillas superiores voladas SOLO hacia adentro (X = 0.15..0.35 m, CERO invasión a X < 0.15 m)
    add_house_box(L_GUTTER, 8, 0.15, -ALERO_SUR, Z_PARAPET_BUH,  0.35, 4.45,  Z_PARAPET_BUH + 0.06)
    add_house_box(L_GUTTER, 8, 0.15,  4.45,      Z_PARAPET_WEST, 0.35, Y_AV4, Z_PARAPET_WEST + 0.06)
    # Canalón Pluvial Oculto Propio: tramo superior Buhardilla (Z = 7.42..7.62) y tramo principal (Z = 5.82..6.02)
    add_house_box(L_GUTTER, 8, 0.30, -ALERO_SUR, 7.42, 0.55, 4.45, 7.48)
    add_house_box(L_GUTTER, 8, 0.50, -ALERO_SUR, 7.48, 0.56, 4.45, 7.62)
    add_house_box(L_GUTTER, 8, 0.30,  4.45,      5.82, 0.55, Y_AV4, 5.88)
    add_house_box(L_GUTTER, 8, 0.50,  4.45,      5.88, 0.56, Y_AV4, 6.02)
    # Bajante interno de transición entre canalón de buhardilla y canalón principal (Y = 4.40..4.52)
    add_house_box(L_GUTTER, 8, 0.32, 4.40, 5.88, 0.46, 4.52, 7.48)

    # --- DOBLE TERRAZA FRONTAL INDEPENDIENTE SOBRE AVENIDA 4 (Y = 19.60 a 21.56 m) ---
    # 1. Gran Balconada Rústica Social Techada dividida limpiamente por el poste maestro A0 (X = 2.68..2.97)
    add_alpine_railing_x(0.42, 2.68, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_x(2.97, 5.85, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=3)
    # 2. Terraza Privada Exclusiva Master Suite (X: 6.00..9.00, Y: 19.60..21.56 -> 3,00 x 1,96 m = 5,88 m²)
    add_alpine_railing_x(6.00, 9.00, Y_AV4 - 0.08, Z_P2_FLOOR, h_rail=1.05, n_bays=3)
    add_alpine_railing_y(9.07, 19.60, Y_AV4 - 0.15, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    # 3. Muro / Pantalla Divisoria Rústica de Privacidad Total en Eje 2 (X: 5.85..6.00, Y: 19.45..21.71)
    add_house_box(L_P2_EXT, 34, 5.85, 19.45, Z_P2_FLOOR, 6.00, Y_AV4, H_P2)
    # Poste esquinero derecho de madera maciza en terraza suite
    add_house_box(L_TIMBER, 34, 8.95, Y_AV4 - 0.20, Z_P2_FLOOR, 9.15, Y_AV4, 6.00)

    # 4. Muro Frontal Acristalado de Retranqueo de Terrazas enmarcando limpiamente Eje 1 (X = 2.70..2.95)
    add_wall_with_openings_x(L_P2_EXT, 34, 0.30, 5.85, 19.45, 19.60, Z_P2_FLOOR, H_P2, [
        (0.65, 2.55, Z_P2_FLOOR,        Z_P2_FLOOR + 2.25),  # Puerta-ventana corrediza Salón (izq. de Eje 1)
        (3.15, 5.55, Z_P2_FLOOR + 0.85, Z_P2_FLOOR + 2.25),  # Ventanal panorámico Comedor (der. de Eje 1)
    ])
    add_wall_with_openings_x(L_P2_EXT, 34, 6.00, 9.00, 19.45, 19.60, Z_P2_FLOOR, H_P2, [
        (6.50, 8.50, Z_P2_FLOOR,        Z_P2_FLOOR + 2.25),  # Puerta-ventana exclusiva Master Suite a su Terraza
    ])

    # --- FACHADA LATERAL DERECHA (ESTE — X: 9.00..9.15, Y: 0.00..19.60) ---
    east_windows_p2 = [
        (1.10,  2.90, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),  # Ventana Este Habitación 3 (Nuevo Bloque)
        (4.90,  5.85, Z_P2_FLOOR + 1.15, Z_P2_FLOOR + 2.05),  # Ventana Alta Baño Familiar
        (7.15,  8.55, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),  # Ventana Habitación 2
        (10.65, 11.65, Z_P2_FLOOR + 1.15, Z_P2_FLOOR + 2.05), # Ventana Alta Gran Baño Spa Master
        (16.00, 18.20, Z_P2_FLOOR + 0.90, Z_P2_FLOOR + 2.20), # Gran Ventanal Este Dormitorio Master Suite
    ]
    add_wall_with_openings_y(L_P2_EXT, 34, 9.00, 9.15, 0.00, 19.60, Z_P2_FLOOR, 6.00, east_windows_p2)
    for wy1, wy2, wz1, wz2 in east_windows_p2:
        add_rustic_window_east(wy1, wy2, wz1, wz2, with_shutters=(wy2 - wy1 >= 1.30))

    # --- FACHADA POSTERIOR SUR COMPLETA (Y: 0.00..0.15) ---
    Z_LAV_CEIL = 5.50  # Altura libre Lavandería = 2.50 m bajo la Losa Técnica del Tanque
    # Tramo Lavandería (X: 0.30..2.90, Z: 3.00..5.50)
    add_wall_with_openings_x(L_P2_EXT, 34, 0.30, 2.90, 0.00, 0.15, Z_P2_FLOOR, Z_LAV_CEIL, [
        (0.85, 2.35, Z_P2_FLOOR + 1.05, Z_P2_FLOOR + 2.15),   # Ventana Lavandería Rústica (1.50 x 1.10 m)
    ])
    add_rustic_window_south(0.85, 2.35, Z_P2_FLOOR + 1.05, Z_P2_FLOOR + 2.15, with_shutters=False)
    # Tramo Mirador Sur + Habitación 3 Esquinera (X: 2.90..9.15, Z: 3.00..5.85)
    south_windows_p2 = [
        (3.35, 5.40, Z_P2_FLOOR + 0.90, Z_P2_FLOOR + 2.20),   # Gran Ventanal Estar / Mirador Posterior
        (6.65, 8.45, Z_P2_FLOOR + 0.95, Z_P2_FLOOR + 2.15),   # Gran Ventanal Sur Habitación 3 Esquinera
    ]
    add_wall_with_openings_x(L_P2_EXT, 34, 2.90, 9.15, 0.00, 0.15, Z_P2_FLOOR, H_P2, south_windows_p2)
    for wx1, wx2, wz1, wz2 in south_windows_p2:
        add_rustic_window_south(wx1, wx2, wz1, wz2, with_shutters=True)

    # --- DISTRIBUCIÓN INTERIOR P2: MASTER SUITE DE LUJO + 2 HABITACIONES + SALÓN SIN CHIMENEA ---
    # 1. Espina longitudinal sobre Eje 2 (X: 5.85..6.00, Y: 0.15..19.45) libre de colisiones con columnas
    add_wall_with_openings_y(L_P2_INT, 6, 5.85, 6.00, 0.15, 19.45, Z_P2_FLOOR, H_P2, [
        (2.55,  3.35, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta Habitación 3 (Nuevo Bloque)
        (4.60,  5.35, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta Baño Familiar Compartido
        (6.85,  7.65, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),       # Puerta Habitación 2
        (15.10, 15.95, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),      # Puerta Principal Master Suite Chalet
    ])

    # 2. División Dormitorio Master (3.00 x 4.50 m) / Gran Vestier Walk-In (3.00 x 2.20 m): Y = 14.80..14.95
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 9.00, 14.80, 14.95, Z_P2_FLOOR, H_P2, [
        (7.05, 7.95, Z_P2_FLOOR, Z_P2_FLOOR + 2.15),          # Puerta corrediza rústica central al Vestier
    ])
    # Closets paralelos de madera natural dentro del Gran Vestier Walk-In (pasillo central libre de 1.80 m)
    add_house_box(L_TIMBER, 34, 6.00, 12.65, Z_P2_FLOOR, 6.58, 14.75, Z_P2_FLOOR + 2.35)
    add_house_box(L_TIMBER, 34, 8.42, 12.65, Z_P2_FLOOR, 9.00, 14.75, Z_P2_FLOOR + 2.35)

    # 3. División Gran Vestier Walk-In / Gran Baño En-Suite Spa (3.00 x 2.30 m): Y = 12.45..12.60
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 9.00, 12.45, 12.60, Z_P2_FLOOR, H_P2, [
        (7.10, 7.90, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),        # Puerta privada al Baño Spa Master
    ])
    # Mueble rústico de doble lavamanos en Baño Spa Master
    add_house_box(L_P2_ISL, 3, 6.00, 10.35, Z_P2_FLOOR, 6.55, 11.95, Z_P2_FLOOR + 0.88)

    # 4. Muro divisorio Sur del Baño Spa Master / Norte de Habitación 2 (Y: 10.00..10.15)
    add_house_box(L_P2_INT, 6, 6.00, 10.00, Z_P2_FLOOR, 9.00, 10.15, H_P2)

    # 5. Muro divisorio Habitación 2 (3.00 x 3.55 m) / Baño Familiar (3.00 x 1.85 m): Y = 6.30..6.45
    add_house_box(L_P2_INT, 6, 6.00, 6.30, Z_P2_FLOOR, 9.00, 6.45, H_P2)

    # 6. Muro divisorio Baño Familiar / Habitación 3 Esquinera (3.00 x 4.15 m): Y = 4.30..4.45
    add_house_box(L_P2_INT, 6, 6.00, 4.30, Z_P2_FLOOR, 9.00, 4.45, H_P2)

    # 7. Cocina Rústica de Montaña con Isla Central Maciza integrada con Columna D (2.825, 12.025)
    add_house_box(L_P2_ISL, 3, 0.30, 7.50, Z_P2_FLOOR, 0.95, 13.20, Z_P2_FLOOR + 0.90)
    add_house_box(L_P2_ISL, 3, 0.95, 7.50, Z_P2_FLOOR, 2.75, 8.15,  Z_P2_FLOOR + 0.90)
    add_house_box(L_P2_ISL, 3, 1.95, 9.55, Z_P2_FLOOR, 2.95, 12.15, Z_P2_FLOOR + 0.90)

    # 8. Protección de Escalera + Baranda Rústica enmarcando limpiamente la Columna F (Y = 6.45..6.70)
    add_house_box(L_P2_INT, 6, 0.30, 7.35, Z_P2_FLOOR, 2.75, 7.50, H_P2)
    add_alpine_railing_y(2.75, 4.40, 6.43, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_y(2.75, 6.72, 7.35, Z_P2_FLOOR, h_rail=1.05, n_bays=1)

    # 9. Lavandería Rústica (X: 0.30..2.75, Y: 0.15..4.25, Z: 3.00..5.50) y Pórtico al Estar / Mirador Sur
    add_wall_with_openings_x(L_P2_INT, 6, 0.30, 2.75, 4.25, 4.40, Z_P2_FLOOR, Z_LAV_CEIL, [
        (1.65, 2.45, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    add_house_box(L_P2_INT, 6, 2.75, 0.15, Z_P2_FLOOR, 2.90, 4.40, Z_LAV_CEIL)
    add_wall_with_openings_x(L_P2_INT, 6, 2.90, 5.85, 3.50, 3.65, Z_P2_FLOOR, H_P2, [
        (3.40, 5.30, Z_P2_FLOOR, Z_P2_FLOOR + 2.40),          # Gran pórtico abierto al Estar/Mirador Sur
    ])

    # =========================================================================
    # 3B. CUARTO HIDRONEUMÁTICO / BUHARDILLA CHALET PARA TANQUE DE 1.000 L
    #     (ENCIMA DE LA LAVANDERÍA: X = 0.15..2.90 m, Y = 0.00..4.40 m, Z = +5.68 m)
    # =========================================================================
    L_TANK_SLAB = "P2_LOSA_TANQUE_3D"
    L_MAINT_ST  = "P2_ESCALERA_MANTENIMIENTO_3D"
    L_HYDRO     = "EQUIPO_HIDRONEUMATICO_3D"
    L_DORMER    = "BUHARDILLA_TECNICA_3D"

    Z_TANK_FLOOR = 5.68   # Losa técnica portante de 18 cm (Z: 5.50 a 5.68 m)
    # Losa portante con abertura de Escotilla de Acceso (X: 0.42..1.22, Y: 2.60..3.85 -> 0,80 x 1,25 m, libre de Col. G)
    add_house_box(L_TANK_SLAB, 8, 0.30, 0.00, Z_LAV_CEIL, 2.90, 2.60, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 0.30, 3.85, Z_LAV_CEIL, 2.90, 4.40, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 0.30, 2.60, Z_LAV_CEIL, 0.42, 3.85, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 1.22, 2.60, Z_LAV_CEIL, 2.90, 3.85, Z_TANK_FLOOR)

    # Pedestal macizo de concreto para el Tanque de 1.000 L (1,30 x 1,30 x 0,12 m) y Bancada Hidroneumática
    TANK_CX, TANK_CY = 1.55, 1.20
    add_house_box(L_TANK_SLAB, 8, TANK_CX - 0.65, TANK_CY - 0.65, Z_TANK_FLOOR,
                                  TANK_CX + 0.65, TANK_CY + 0.65, Z_TANK_FLOOR + 0.12)
    add_house_box(L_TANK_SLAB, 8, 1.85, 2.15, Z_TANK_FLOOR, 2.70, 3.25, Z_TANK_FLOOR + 0.10)

    # Escalera Fija Inclinada (68°) desde Lavandería (Z=3.00, Y=3.80) hacia Escotilla (Z=5.68, Y=2.67), X: 0.44..1.14
    # Largueros inclinados izquierdo y derecho (libres de columna existente Eje 0-G)
    for sx1, sx2 in [(0.44, 0.49), (1.09, 1.14)]:
        add_house_hexa(L_MAINT_ST, 30, [
            (sx1, 3.74, Z_P2_FLOOR), (sx2, 3.74, Z_P2_FLOOR),
            (sx2, 3.84, Z_P2_FLOOR), (sx1, 3.84, Z_P2_FLOOR),
            (sx1, 2.62, Z_TANK_FLOOR), (sx2, 2.62, Z_TANK_FLOOR),
            (sx2, 2.72, Z_TANK_FLOOR), (sx1, 2.72, Z_TANK_FLOOR),
        ])
        # Pasamanos inclinados + prolongación vertical de seguridad (+1.00 m sobre Z_TANK_FLOOR)
        add_house_hexa(L_MAINT_ST, 30, [
            (sx1, 3.55, Z_P2_FLOOR + 0.85), (sx2, 3.55, Z_P2_FLOOR + 0.85),
            (sx2, 3.61, Z_P2_FLOOR + 0.85), (sx1, 3.61, Z_P2_FLOOR + 0.85),
            (sx1, 2.62, Z_TANK_FLOOR + 1.00), (sx2, 2.62, Z_TANK_FLOOR + 1.00),
            (sx2, 2.68, Z_TANK_FLOOR + 1.00), (sx1, 2.68, Z_TANK_FLOOR + 1.00),
        ])
        add_house_box(L_MAINT_ST, 30, sx1, 2.60, Z_TANK_FLOOR, sx2, 2.66, Z_TANK_FLOOR + 1.00)

    # 9 Peldaños planos antideslizantes de 18 cm de huella (ancho útil 60 cm)
    num_m_steps = 9
    for ms in range(1, num_m_steps + 1):
        frac = ms / (num_m_steps + 1)
        ym_c = 3.79 - frac * (3.79 - 2.67)
        zm_c = Z_P2_FLOOR + frac * (Z_TANK_FLOOR - Z_P2_FLOOR)
        add_house_box(L_MAINT_ST, 30, 0.49, ym_c - 0.09, zm_c - 0.04, 1.09, ym_c + 0.09, zm_c)

    # Baranda Guarda-Escotilla de 1.00 m en el Cuarto Técnico (protege lados Este y Norte del hueco)
    add_alpine_railing_y(1.25, 2.60, 3.90, Z_TANK_FLOOR, h_rail=1.00, n_bays=2)
    add_alpine_railing_x(0.42, 1.25, 3.88, Z_TANK_FLOOR, h_rail=1.00, n_bays=1)

    # Tanque Cilíndrico Vertical de 1.000 Litros (Ø 1,10 m x H = 1,30 m, prisma de 12 lados + tapa Ø 0,45 m)
    TANK_R     = 0.55
    Z_TANK_BOT = Z_TANK_FLOOR + 0.12  # 5.80 m
    Z_TANK_SHO = Z_TANK_BOT + 1.18    # 6.98 m (cuerpo cilíndrico)
    Z_TANK_TOP = Z_TANK_BOT + 1.30    # 7.10 m (hombro superior)
    N_SEG      = 12
    for s_i in range(N_SEG):
        a0 = 2.0 * math.pi * s_i / N_SEG
        a1 = 2.0 * math.pi * (s_i + 1) / N_SEG
        x_out0 = TANK_CX + TANK_R * math.cos(a0)
        y_out0 = TANK_CY + TANK_R * math.sin(a0)
        x_out1 = TANK_CX + TANK_R * math.cos(a1)
        y_out1 = TANK_CY + TANK_R * math.sin(a1)
        x_in0  = TANK_CX + 0.22 * math.cos(a0)
        y_in0  = TANK_CY + 0.22 * math.sin(a0)
        x_in1  = TANK_CX + 0.22 * math.cos(a1)
        y_in1  = TANK_CY + 0.22 * math.sin(a1)
        # Gajo cuerpo principal del tanque
        add_house_hexa(L_HYDRO, 5, [
            (TANK_CX, TANK_CY, Z_TANK_BOT), (x_out0, y_out0, Z_TANK_BOT),
            (x_out1,  y_out1,  Z_TANK_BOT), (TANK_CX, TANK_CY, Z_TANK_BOT),
            (TANK_CX, TANK_CY, Z_TANK_SHO), (x_out0, y_out0, Z_TANK_SHO),
            (x_out1,  y_out1,  Z_TANK_SHO), (TANK_CX, TANK_CY, Z_TANK_SHO),
        ])
        # Hombro cónico superior del tanque
        add_house_hexa(L_HYDRO, 5, [
            (TANK_CX, TANK_CY, Z_TANK_SHO), (x_out0, y_out0, Z_TANK_SHO),
            (x_out1,  y_out1,  Z_TANK_SHO), (TANK_CX, TANK_CY, Z_TANK_SHO),
            (TANK_CX, TANK_CY, Z_TANK_TOP), (x_in0,  y_in0,  Z_TANK_TOP),
            (x_in1,   y_in1,   Z_TANK_TOP), (TANK_CX, TANK_CY, Z_TANK_TOP),
        ])
        # Tapa roscada superior de inspección (Ø 0,44 m, Z: 7.10..7.18 m)
        add_house_hexa(L_HYDRO, 7, [
            (TANK_CX, TANK_CY, Z_TANK_TOP),        (x_in0, y_in0, Z_TANK_TOP),
            (x_in1,   y_in1,   Z_TANK_TOP),        (TANK_CX, TANK_CY, Z_TANK_TOP),
            (TANK_CX, TANK_CY, Z_TANK_TOP + 0.08), (x_in0, y_in0, Z_TANK_TOP + 0.08),
            (x_in1,   y_in1,   Z_TANK_TOP + 0.08), (TANK_CX, TANK_CY, Z_TANK_TOP + 0.08),
        ])

    # Equipo Hidroneumático: Bomba Presurizadora + Pulmón + Filtro + Tubería By-Pass Gravedad
    add_house_box(L_HYDRO, 5, 1.98, 2.25, Z_TANK_FLOOR + 0.10, 2.32, 2.65, Z_TANK_FLOOR + 0.42)  # Bomba
    add_house_box(L_HYDRO, 1, 2.36, 2.25, Z_TANK_FLOOR + 0.10, 2.64, 2.65, Z_TANK_FLOOR + 0.68)  # Pulmón
    add_house_box(L_HYDRO, 4, 2.05, 2.80, Z_TANK_FLOOR + 0.10, 2.28, 3.05, Z_TANK_FLOOR + 0.55)  # Filtro
    add_house_box(L_HYDRO, 8, 1.95, 1.65, Z_TANK_FLOOR + 0.22, 2.05, 2.95, Z_TANK_FLOOR + 0.28)  # Tubería succión/by-pass

    # Geometría de la Buhardilla Técnica Chalet (Shed Dormer, pendiente 8.5° hacia canalón propio)
    DORM_SLOPE = 0.15
    def z_dormer_under(x):
        return 7.56 + (x - 0.40) * DORM_SLOPE

    # Encuentro matemático exacto entre plano de Buhardilla y Faldón Oeste Principal (32°)
    X_DORM_JOIN = (7.56 - 0.40 * DORM_SLOPE - (Z_GUTTER_EAVE - X_GUTTER_IN * SLOPE_TAN)) / (SLOPE_TAN - DORM_SLOPE)
    Z_DORM_JOIN = z_roof_under(X_DORM_JOIN)  # X ≈ 3.856 m, Z ≈ 8.078 m

    # Muro Este de Buhardilla en madera machihembrada (X: 2.75..2.90, Y: 0.00..4.40, Z: 5.68 -> techo buhardilla)
    add_house_hexa(L_DORMER, 34, [
        (2.75, 0.00, Z_TANK_FLOOR), (2.90, 0.00, Z_TANK_FLOOR),
        (2.90, 4.40, Z_TANK_FLOOR), (2.75, 4.40, Z_TANK_FLOOR),
        (2.75, 0.00, z_dormer_under(2.75)), (2.90, 0.00, z_dormer_under(2.90)),
        (2.90, 4.40, z_dormer_under(2.90)), (2.75, 4.40, z_dormer_under(2.75)),
    ])
    # Cierre Norte de Buhardilla (Y: 4.25..4.45 para X: 0.30..2.90) + Cachete triangular exterior (X: 2.90..X_DORM_JOIN)
    add_house_hexa(L_DORMER, 34, [
        (0.30, 4.25, Z_TANK_FLOOR), (2.90, 4.25, Z_TANK_FLOOR),
        (2.90, 4.45, Z_TANK_FLOOR), (0.30, 4.45, Z_TANK_FLOOR),
        (0.30, 4.25, z_dormer_under(0.30)), (2.90, 4.25, z_dormer_under(2.90)),
        (2.90, 4.45, z_dormer_under(2.90)), (0.30, 4.45, z_dormer_under(0.30)),
    ])
    add_house_hexa(L_DORMER, 34, [
        (2.90,        4.30, z_roof_under(2.90)), (X_DORM_JOIN, 4.30, Z_DORM_JOIN),
        (X_DORM_JOIN, 4.45, Z_DORM_JOIN),        (2.90,        4.45, z_roof_under(2.90)),
        (2.90,        4.30, z_dormer_under(2.90)), (X_DORM_JOIN, 4.30, Z_DORM_JOIN),
        (X_DORM_JOIN, 4.45, Z_DORM_JOIN),          (2.90,        4.45, z_dormer_under(2.90)),
    ])

    # Fachada Sur de la Buhardilla (Y: 0.00..0.15, X: 0.30..2.90) con Panel Doble de Celosías Rústicas (1.45 x 1.45 m)
    add_wall_with_openings_x(L_DORMER, 34, 0.30, 2.90, 0.00, 0.15, Z_TANK_FLOOR, 7.56, [
        (0.88, 2.33, 5.90, 7.35),  # Vano Puerta Doble de Celosía Rústica para ventilación e izaje del tanque
    ])
    # Remate trapezoidal entre Z = 7.56 y pendiente de cubierta de buhardilla
    add_house_hexa(L_DORMER, 34, [
        (0.30, 0.00, 7.56), (2.90, 0.00, 7.56), (2.90, 0.15, 7.56), (0.30, 0.15, 7.56),
        (0.30, 0.00, z_dormer_under(0.30)), (2.90, 0.00, z_dormer_under(2.90)),
        (2.90, 0.15, z_dormer_under(2.90)), (0.30, 0.15, z_dormer_under(0.30)),
    ])
    # Marco y lamas horizontales de madera del Panel Doble de Celosía Rústica (X: 0.88..2.33, Z: 5.90..7.35)
    add_house_box(L_CARP, 34, 0.85, -0.02, 5.88, 2.36, 0.17, 5.94)
    add_house_box(L_CARP, 34, 0.85, -0.02, 7.31, 2.36, 0.17, 7.37)
    add_house_box(L_CARP, 34, 0.85, -0.02, 5.94, 0.91, 0.17, 7.31)
    add_house_box(L_CARP, 34, 2.30, -0.02, 5.94, 2.36, 0.17, 7.31)
    add_house_box(L_CARP, 34, 1.58, -0.02, 5.94, 1.63, 0.17, 7.31)  # Encuentro central doble hoja
    for sl_i in range(11):
        z_sl = 5.98 + sl_i * 0.125
        add_house_box(L_CARP, 30, 0.91, 0.02, z_sl, 1.58, 0.12, z_sl + 0.04)
        add_house_box(L_CARP, 30, 1.63, 0.02, z_sl, 2.30, 0.12, z_sl + 0.04)

    # Cubierta propia de la Buhardilla Chalet (X: 0.40..X_DORM_JOIN, Y: -1.00..4.45, espesor 0.16 m)
    DORM_THICK = 0.16
    add_house_hexa(L_ROOF, 9, [
        (0.40,        -ALERO_SUR, z_dormer_under(0.40)),              (X_DORM_JOIN, -ALERO_SUR, Z_DORM_JOIN),
        (X_DORM_JOIN,  4.45,      Z_DORM_JOIN),                       (0.40,         4.45,      z_dormer_under(0.40)),
        (0.40,        -ALERO_SUR, z_dormer_under(0.40) + DORM_THICK), (X_DORM_JOIN, -ALERO_SUR, Z_DORM_JOIN + DORM_THICK),
        (X_DORM_JOIN,  4.45,      Z_DORM_JOIN + DORM_THICK),          (0.40,         4.45,      z_dormer_under(0.40) + DORM_THICK),
    ])

    # =========================================================================
    # 4. CUBIERTA ALPINA A DOS AGUAS, HASTIALES Y CERCHAS VISTAS (PASO 4)
    # =========================================================================
    # A1) Hastial Sur en Y = 0.00..0.15 (tramo X = 2.90..9.15 acoplado limpiamente con la Buhardilla)
    add_house_hexa(L_P2_EXT, 34, [
        (2.90,        0.00, H_P2), (X_DORM_JOIN, 0.00, H_P2), (X_DORM_JOIN, 0.15, H_P2), (2.90,        0.15, H_P2),
        (2.90,        0.00, z_dormer_under(2.90)), (X_DORM_JOIN, 0.00, Z_DORM_JOIN),
        (X_DORM_JOIN, 0.15, Z_DORM_JOIN),          (2.90,        0.15, z_dormer_under(2.90)),
    ])
    add_house_hexa(L_P2_EXT, 34, [
        (X_DORM_JOIN, 0.00, H_P2), (X_RIDGE, 0.00, H_P2), (X_RIDGE, 0.15, H_P2), (X_DORM_JOIN, 0.15, H_P2),
        (X_DORM_JOIN, 0.00, Z_DORM_JOIN), (X_RIDGE, 0.00, Z_RIDGE),
        (X_RIDGE,     0.15, Z_RIDGE),     (X_DORM_JOIN, 0.15, Z_DORM_JOIN),
    ])
    add_house_hexa(L_P2_EXT, 34, [
        (X_RIDGE, 0.00, H_P2), (9.15, 0.00, H_P2), (9.15, 0.15, H_P2), (X_RIDGE, 0.15, H_P2),
        (X_RIDGE, 0.00, Z_RIDGE),            (9.15, 0.00, z_roof_under(9.15)),
        (9.15,    0.15, z_roof_under(9.15)), (X_RIDGE, 0.15, Z_RIDGE),
    ])

    # A2) Hastial Norte sobre Retranqueo de Terrazas (Y = 19.45..19.60, completo X = 0.45..9.15)
    add_house_hexa(L_P2_EXT, 34, [
        (0.45,    19.45, H_P2), (X_RIDGE, 19.45, H_P2), (X_RIDGE, 19.60, H_P2), (0.45,    19.60, H_P2),
        (0.45,    19.45, z_roof_under(0.45)), (X_RIDGE, 19.45, Z_RIDGE),
        (X_RIDGE, 19.60, Z_RIDGE),            (0.45,    19.60, z_roof_under(0.45)),
    ])
    add_house_hexa(L_P2_EXT, 34, [
        (X_RIDGE, 19.45, H_P2), (9.15, 19.45, H_P2), (9.15, 19.60, H_P2), (X_RIDGE, 19.60, H_P2),
        (X_RIDGE, 19.45, Z_RIDGE),            (9.15, 19.45, z_roof_under(9.15)),
        (9.15,    19.60, z_roof_under(9.15)), (X_RIDGE, 19.60, Z_RIDGE),
    ])

    # B) Cerchas Alpinas Monumentales Vistas (King-Post Timber Trusses) en Frente Av. 4, Salón y Sur
    truss_y_positions = [21.56, 16.30, 12.00, 7.50, -0.85]
    for ty in truss_y_positions:
        ty2 = ty + 0.15
        x_tie_start = 2.90 if ty < 0.0 else 0.45
        add_house_box(L_TIMBER, 34, x_tie_start, ty, H_P2 - 0.18, 9.15, ty2, H_P2)
        add_house_box(L_TIMBER, 34, X_RIDGE - 0.09, ty, H_P2, X_RIDGE + 0.09, ty2, Z_RIDGE - 0.05)
        if ty > 0.0:
            add_house_hexa(L_TIMBER, 34, [
                (X_RIDGE - 0.08, ty, H_P2 + 0.15), (X_RIDGE, ty, H_P2 + 0.15),
                (X_RIDGE, ty2, H_P2 + 0.15),       (X_RIDGE - 0.08, ty2, H_P2 + 0.15),
                (2.55, ty, z_roof_under(2.55) - 0.12), (2.70, ty, z_roof_under(2.70) - 0.12),
                (2.70, ty2, z_roof_under(2.70) - 0.12),(2.55, ty2, z_roof_under(2.55) - 0.12),
            ])
        add_house_hexa(L_TIMBER, 34, [
            (X_RIDGE, ty, H_P2 + 0.15),        (X_RIDGE + 0.08, ty, H_P2 + 0.15),
            (X_RIDGE + 0.08, ty2, H_P2 + 0.15),(X_RIDGE, ty2, H_P2 + 0.15),
            (7.00, ty, z_roof_under(7.00) - 0.12), (7.15, ty, z_roof_under(7.15) - 0.12),
            (7.15, ty2, z_roof_under(7.15) - 0.12),(7.00, ty2, z_roof_under(7.00) - 0.12),
        ])

    # Viga cumbrera longitudinal vista (Y = -1.00 a 21.71)
    add_house_box(L_TIMBER, 34, X_RIDGE - 0.08, -ALERO_SUR, Z_RIDGE - 0.22, X_RIDGE + 0.08, Y_AV4, Z_RIDGE)

    # C) Dos Faldones de Cubierta Alpina a 32° (Faldón Oeste recortado limpiamente alrededor de la Buhardilla):
    y_roof_s = -ALERO_SUR
    y_roof_n = Y_AV4
    z_w_bot  = z_roof_under(0.40)
    # Faldón Oeste Tramo Norte Principal (Y: 4.45 a 21.71, X: 0.40 a 4.85)
    add_house_hexa(L_ROOF, 9, [
        (0.40,    4.45,     z_w_bot),              (X_RIDGE, 4.45,     Z_RIDGE),
        (X_RIDGE, y_roof_n, Z_RIDGE),              (0.40,    y_roof_n, z_w_bot),
        (0.40,    4.45,     z_w_bot + ROOF_THICK), (X_RIDGE, 4.45,     Z_RIDGE + ROOF_THICK),
        (X_RIDGE, y_roof_n, Z_RIDGE + ROOF_THICK), (0.40,    y_roof_n, z_w_bot + ROOF_THICK),
    ])
    # Faldón Oeste Tramo Sur Superior sobre Buhardilla (Y: -1.00 a 4.45, X: X_DORM_JOIN a 4.85)
    add_house_hexa(L_ROOF, 9, [
        (X_DORM_JOIN, y_roof_s, Z_DORM_JOIN),              (X_RIDGE, y_roof_s, Z_RIDGE),
        (X_RIDGE,     4.45,     Z_RIDGE),                  (X_DORM_JOIN, 4.45, Z_DORM_JOIN),
        (X_DORM_JOIN, y_roof_s, Z_DORM_JOIN + ROOF_THICK), (X_RIDGE, y_roof_s, Z_RIDGE + ROOF_THICK),
        (X_RIDGE,     4.45,     Z_RIDGE + ROOF_THICK),     (X_DORM_JOIN, 4.45, Z_DORM_JOIN + ROOF_THICK),
    ])
    # Faldón Este completo intacto (X: 4.85 a 10.10, Y: -1.00 a 21.71)
    add_house_hexa(L_ROOF, 9, [
        (X_RIDGE,     y_roof_s, Z_RIDGE),              (X_EAVE_EAST, y_roof_s, Z_EAVE_EAST),
        (X_EAVE_EAST, y_roof_n, Z_EAVE_EAST),          (X_RIDGE,     y_roof_n, Z_RIDGE),
        (X_RIDGE,     y_roof_s, Z_RIDGE + ROOF_THICK), (X_EAVE_EAST, y_roof_s, Z_EAVE_EAST + ROOF_THICK),
        (X_EAVE_EAST, y_roof_n, Z_EAVE_EAST + ROOF_THICK), (X_RIDGE, y_roof_n, Z_RIDGE + ROOF_THICK),
    ])

    # D) Canecillos y Pares Pasantes Vistos (Rafter Tails) bajo el Alero Derecho Propio (X: 9.00..10.10)
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

    # --- EJES ESTRUCTURALES Y RÓTULOS 3D POR NIVEL ---
    L_GRID = "EJES_ESTRUCTURALES"
    for label, gx in [("0 (PROPIO - SIN ALERO)", 0.275), ("1 (EXISTENTE)", 2.825), ("2", 5.925), ("3", 9.075)]:
        add_house_line(L_GRID, 1, gx, -1.20, 0.0, gx, Y_AV4 + 0.80, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", gx - 0.35, Y_AV4 + 1.00, 0.0, 0.20)

    for label, gy in [("A0 (AV.4)", 21.585), ("A", 18.575), ("B", 16.325), ("C", 14.625),
                      ("D", 12.025), ("E", 8.875), ("F", 6.575), ("G", 3.575), ("H (POST.)", 0.125)]:
        add_house_line(L_GRID, 1, -0.60, gy, 0.0, 10.40, gy, 0.0)
        add_house_text(L_GRID, 1, f"EJE {label}", 10.50, gy - 0.10, 0.0, 0.22)

    sot_labels = [
        ("SOTANO: Cocina (4,30 x 2,65m)", 2.20, 6.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Comedor", 2.50, 4.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Sala (2,95 x 4,50m)", 6.25, 5.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO NUEVO: Recibidor / Estudio Jardin (2,55 x 3,35m)", 6.45, 1.90, Z_SOT_FLOOR + 0.05),
        ("ACCESO EXTERIOR SOTANO DESDE PATIO TRASERO", 6.35, -0.55, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Habitacion 1 (2,50 x 3,35m)", 0.45, 1.80, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Lavadero", 3.10, 1.40, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Bano (vent. directa al patio)", 4.80, 1.00, Z_SOT_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in sot_labels:
        add_house_text("SOTANO_ROTULOS", 4, txt, rx, ry, rz, 0.18)

    p1_labels = [
        ("P1: GRAN LOCAL COMERCIAL (5,55 x 16,16m = 89,7 m2)", 3.80, 13.50, 0.05),
        ("P1: GARAJE DOBLE (COL. INTACTAS + BOLSILLOS 3,00m)", 0.45, 15.20, 0.05),
        ("P1: Bano Local (3,00 x 1,75m)", 6.30, 4.40, 0.05),
        ("P1: Deposito Comercial (3,35 x 3,35m)", 3.10, 1.80, 0.05),
        ("P1 NUEVO: Oficina Privada Gerencia (2,60 x 3,35m)", 6.50, 1.80, 0.05),
        ("P1: Area Apoyo", 0.50, 2.50, 0.05),
    ]
    for txt, rx, ry, rz in p1_labels:
        add_house_text("ROTULOS_TEXTO", 2, txt, rx, ry, rz, 0.19)

    p2_labels = [
        ("P2: GRAN BALCONADA SOCIAL TECHADA (5,55 x 1,96m)", 0.70, 20.40, Z_P2_FLOOR + 0.05),
        ("P2: TERRAZA PRIVADA MASTER SUITE (3,00 x 1,96m)", 6.10, 20.40, Z_P2_FLOOR + 0.05),
        ("P2: GRAN SALON - COMEDOR CHALET SIN CHIMENEA (5,55 x 6,25m)", 0.65, 16.50, Z_P2_FLOOR + 0.05),
        ("P2: COCINA RUSTICA CON ISLA MACIZA (5,55 x 5,70m)", 0.70, 10.60, Z_P2_FLOOR + 0.05),
        ("P2: MASTER SUITE CHALET (3,00 x 4,50m)", 6.15, 17.20, Z_P2_FLOOR + 0.05),
        ("P2: GRAN VESTIER WALK-IN (3,00 x 2,20m)", 6.15, 13.60, Z_P2_FLOOR + 0.05),
        ("P2: GRAN BANO EN-SUITE SPA (3,00 x 2,30m)", 6.15, 11.20, Z_P2_FLOOR + 0.05),
        ("P2: HABITACION 2 (3,00 x 3,55m)", 6.15, 8.10, Z_P2_FLOOR + 0.05),
        ("P2: BANO FAMILIAR (3,00 x 1,85m)", 6.15, 5.30, Z_P2_FLOOR + 0.05),
        ("P2 NUEVO: HABITACION 3 ESQUINERA (3,00 x 4,15m)", 6.10, 2.10, Z_P2_FLOOR + 0.05),
        ("P2: Estar / Mirador Sur (2,95 x 3,35m)", 3.05, 1.80, Z_P2_FLOOR + 0.05),
        ("P2: Lavanderia + Subida Tanque (2,45 x 4,10m)", 0.45, 2.10, Z_P2_FLOOR + 0.05),
        ("BUHARDILLA TECNICA: TANQUE 1.000L + BOMBA (Z=+5,68m)", 0.38, 0.32, Z_TANK_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in p2_labels:
        add_house_text("P2_ROTULOS", 6, txt, rx, ry, rz, 0.17)

    # =========================================================================
    # 5. TERRENO NO RECTANGULAR UTM Y DESNIVELES 3D (AJUSTADO AL RECTÁNGULO)
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

    # Patio Trasero Propio a cota Sótano (Z = -2.55 m, Y_terreno = 0.00 a 3.00 m)
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

    # Retiro Lateral Derecho a nivel Sótano desde Y_casa = 0.00 hasta 9.50 (caminería hacia Patio Trasero)
    y_b0 = OFFSET_Y + 0.00
    y_b2_1 = OFFSET_Y + 9.50
    add_terrain_strip_y(L_TERR, 3,
                        9.15, x_right(y_b0),   y_b0,   Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        9.15, x_right(y_b2_1), y_b2_1, Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR)
    add_house_box(L_P1_EXT, 7, 9.00, 8.30, Z_SOT_FLOOR, 9.15, 9.50, Z_P1_FLOOR)

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

    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20, Z_SOT_FLOOR,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05)
    add_terrain_strip_y(L_TERR, 3,
                        0.15, 9.00, OFFSET_Y + 11.20, -1.25, -1.05,
                        0.15, 9.00, y_front_av4,      -0.20, -0.15)

    # Pared del vecino izquierdo (X = 0.00..0.15) y cercas perimetrales intactas
    wall_h = 2.50
    add_box(L_FENCE, 8, 0.00, P4_LOC[1], Z_SOT_FLOOR, 0.15, OFFSET_Y + 8.30, Z_P1_FLOOR + wall_h)
    add_box(L_FENCE, 8, 0.00, OFFSET_Y + 8.30, 0.00, 0.15, P1_LOC[1], wall_h)

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
    # 6. LÁMINAS 2D ACTUALIZADAS (SÓTANO RECTANGULAR, P2 CHALET Y FACHADA)
    # =========================================================================
    SX = 16.00
    SY = 2.00
    L_SOT_2D = "PLANTA_SOTANO_2D"
    add_text(L_SOT_2D, 2, "PLANTA SOTANO RECTANGULAR + ACCESO PATIO TRASERO", SX + 0.4, SY - 0.8, 0.0, 0.30)
    add_rect_2d(L_SOT_2D, 7, SX + 0.15, SY + 0.00, SX + 9.15, SY + 8.30)
    add_rect_2d(L_SOT_2D, 4, SX + 0.30, SY + 0.15, SX + 2.80, SY + 3.50)
    add_rect_2d(L_SOT_2D, 4, SX + 2.95, SY + 0.15, SX + 4.60, SY + 2.65)
    add_rect_2d(L_SOT_2D, 4, SX + 4.75, SY + 0.15, SX + 6.25, SY + 1.94)
    add_rect_2d(L_SOT_2D, 4, SX + 6.40, SY + 0.15, SX + 8.95, SY + 3.50)  # Nuevo Recibidor / Estudio Jardín
    add_rect_2d(L_SOT_2D, 4, SX + 6.00, SY + 3.65, SX + 8.95, SY + 8.15)
    # Indicación puerta exterior en patio trasero (X = 7.60..8.70)
    add_line(L_SOT_2D, 1, SX + 7.60, SY - 0.25, 0.0, SX + 8.70, SY - 0.25, 0.0)
    for i in range(13):
        yy = SY + 4.45 + i * ((7.40 - 4.45) / 12.0)
        add_line(L_SOT_2D, 3, SX + 0.30, yy, 0.0, SX + 1.40, yy, 0.0)
    add_text(L_SOT_2D, 2, "Cocina (4,30 x 2,65)", SX + 2.40, SY + 6.50, 0.0, 0.20)
    add_text(L_SOT_2D, 2, "Comedor", SX + 2.60, SY + 4.80, 0.0, 0.20)
    add_text(L_SOT_2D, 2, "Sala (2,95 x 4,50)", SX + 6.30, SY + 5.80, 0.0, 0.20)
    add_text(L_SOT_2D, 2, "Recibidor / Estudio", SX + 6.55, SY + 2.10, 0.0, 0.18)
    add_text(L_SOT_2D, 1, "Entrada Patio Trasero", SX + 6.60, SY - 0.50, 0.0, 0.16)
    add_text(L_SOT_2D, 2, "Habitacion 1 (2,50 x 3,35)", SX + 0.45, SY + 1.80, 0.0, 0.18)
    add_text(L_SOT_2D, 2, "Lavadero", SX + 3.10, SY + 1.30, 0.0, 0.17)
    add_text(L_SOT_2D, 2, "Bano", SX + 5.05, SY + 0.90, 0.0, 0.17)

    P2X = 16.00
    P2Y = 13.00
    L_P2_2D = "PLANTA_SEGUNDO_PISO_2D"
    add_text(L_P2_2D, 6, "PLANTA ALTA CHALET RUSTICO MEJORADA (9,00 x 21,71m)", P2X + 0.2, P2Y - 0.8, 0.0, 0.28)
    add_rect_2d(L_P2_2D, 6, P2X + 0.15, P2Y + 0.00,  P2X + 9.15, P2Y + Y_AV4)
    add_rect_2d(L_P2_2D, 30, P2X + 0.30, P2Y + 19.60, P2X + 5.85, P2Y + 21.56)  # Balconada Social
    add_rect_2d(L_P2_2D, 30, P2X + 6.00, P2Y + 19.60, P2X + 9.00, P2Y + 21.56)  # Terraza Privada Master
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 14.95, P2X + 9.00, P2Y + 19.45)   # Dormitorio Master
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 12.60, P2X + 9.00, P2Y + 14.80)   # Gran Vestier Walk-In
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 10.15, P2X + 9.00, P2Y + 12.45)   # Gran Baño Spa
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 6.45,  P2X + 9.00, P2Y + 10.00)   # Habitación 2
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 4.45,  P2X + 9.00, P2Y + 6.30)    # Baño Familiar
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 0.15,  P2X + 9.00, P2Y + 4.30)    # Habitación 3 Esquinera
    add_rect_2d(L_P2_2D, 6, P2X + 0.30, P2Y + 0.15,  P2X + 2.75, P2Y + 4.25)    # Lavandería
    add_rect_2d(L_P2_2D, 6, P2X + 2.90, P2Y + 0.15,  P2X + 5.85, P2Y + 3.50)    # Estar / Mirador Sur
    add_rect_2d(L_P2_2D, 3, P2X + 1.95, P2Y + 9.55,  P2X + 2.95, P2Y + 12.15)   # Isla Cocina integrada con Col. D
    add_rect_2d(L_P2_2D, 3, P2X + 0.30, P2Y + 7.50,  P2X + 0.95, P2Y + 13.20)   # Mesón Cocina
    for cx, cy in existing_and_new_cols:
        add_rect_2d(L_P2_2D, 1, P2X + cx - 0.125, P2Y + cy - 0.125, P2X + cx + 0.125, P2Y + cy + 0.125)
    add_text(L_P2_2D, 2, "Balconada Social (5,55x1,96)", P2X + 0.70, P2Y + 20.45, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Terraza Suite (3,00x1,96)", P2X + 6.15, P2Y + 20.45, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Gran Salon - Comedor (Sin Chimenea)", P2X + 0.65, P2Y + 16.50, 0.0, 0.19)
    add_text(L_P2_2D, 2, "Cocina Rustica + Isla Maciza", P2X + 0.80, P2Y + 10.80, 0.0, 0.19)
    add_text(L_P2_2D, 2, "Master Suite (3,00x4,50)", P2X + 6.20, P2Y + 17.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Vestier Walk-In (3,00x2,20)", P2X + 6.20, P2Y + 13.60, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Bano Spa Master (3,00x2,30)", P2X + 6.20, P2Y + 11.20, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Habitacion 2 (3,00x3,55)", P2X + 6.20, P2Y + 8.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Bano Familiar (3,00x1,85)", P2X + 6.20, P2Y + 5.25, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Hab. 3 Nueva (3,00x4,15)", P2X + 6.20, P2Y + 2.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Mirador Sur", P2X + 3.40, P2Y + 1.80, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Lavanderia", P2X + 0.65, P2Y + 1.40, 0.0, 0.17)
    # Indicación en planta P2 de Escalera Fija y Proyección Escotilla hacia Tanque 1.000 L
    add_rect_2d(L_P2_2D, 30, P2X + 0.42, P2Y + 2.60, P2X + 1.22, P2Y + 3.85)
    for ms in range(1, num_m_steps + 1):
        ym_2d = P2Y + 3.79 - (ms / (num_m_steps + 1)) * (3.79 - 2.67)
        add_line(L_P2_2D, 30, P2X + 0.49, ym_2d, 0.0, P2X + 1.09, ym_2d, 0.0)
    add_text(L_P2_2D, 30, "Subida Tanque", P2X + 1.28, P2Y + 3.15, 0.0, 0.14)

    # Planta Detalle 2D del Cuarto Hidroneumático / Buhardilla Técnica (Z = +5,68 m)
    TX = 30.00
    TY = 13.00
    L_TANK_2D = "PLANTA_TANQUE_1000L_2D"
    add_text(L_TANK_2D, 5, "PLANTA BUHARDILLA TECNICA TANQUE 1.000L (Z = +5,68m)", TX - 0.2, TY - 1.35, 0.0, 0.25)
    add_rect_2d(L_TANK_2D, 8,  TX + 0.00, TY + 0.00, TX + 0.15, TY + 4.45)  # Medianera Vecino Izquierdo (Cero Invasión)
    add_rect_2d(L_TANK_2D, 34, TX + 0.15, TY + 0.00, TX + 2.90, TY + 4.45)  # Envolvente Exterior Buhardilla
    add_rect_2d(L_TANK_2D, 6,  TX + 0.30, TY + 0.15, TX + 2.75, TY + 4.25)  # Espacio Libre Interior (2,45 x 4,10 m)
    add_rect_2d(L_TANK_2D, 9,  TX + 0.40, TY - 1.00, TX + X_DORM_JOIN, TY + 4.45)  # Proyección Cubierta Buhardilla
    # Escotilla de acceso (0,80 x 1,25 m) + Peldaños + Baranda Guarda-Escotilla (1,00 m)
    add_rect_2d(L_TANK_2D, 30, TX + 0.42, TY + 2.60, TX + 1.22, TY + 3.85)
    for ms in range(1, num_m_steps + 1):
        ym_t = TY + 3.79 - (ms / (num_m_steps + 1)) * (3.79 - 2.67)
        add_line(L_TANK_2D, 30, TX + 0.49, ym_t, 0.0, TX + 1.09, ym_t, 0.0)
    add_line(L_TANK_2D, 1, TX + 1.25, TY + 2.60, 0.0, TX + 1.25, TY + 3.88, 0.0)
    add_line(L_TANK_2D, 1, TX + 0.42, TY + 3.88, 0.0, TX + 1.25, TY + 3.88, 0.0)
    # Pedestal de concreto (1,30 x 1,30 m) + Tanque Cilíndrico 1.000 L (Ø 1,10 m) + Tapa (Ø 0,44 m)
    add_rect_2d(L_TANK_2D, 8, TX + TANK_CX - 0.65, TY + TANK_CY - 0.65, TX + TANK_CX + 0.65, TY + TANK_CY + 0.65)
    for s_i in range(N_SEG):
        a0 = 2.0 * math.pi * s_i / N_SEG
        a1 = 2.0 * math.pi * (s_i + 1) / N_SEG
        add_line(L_TANK_2D, 5, TX + TANK_CX + TANK_R * math.cos(a0), TY + TANK_CY + TANK_R * math.sin(a0), 0.0,
                               TX + TANK_CX + TANK_R * math.cos(a1), TY + TANK_CY + TANK_R * math.sin(a1), 0.0)
        add_line(L_TANK_2D, 7, TX + TANK_CX + 0.22 * math.cos(a0), TY + TANK_CY + 0.22 * math.sin(a0), 0.0,
                               TX + TANK_CX + 0.22 * math.cos(a1), TY + TANK_CY + 0.22 * math.sin(a1), 0.0)
    # Bancada Hidroneumática (Bomba + Pulmón + Filtro)
    add_rect_2d(L_TANK_2D, 8, TX + 1.85, TY + 2.15, TX + 2.70, TY + 3.25)
    add_rect_2d(L_TANK_2D, 5, TX + 1.98, TY + 2.25, TX + 2.32, TY + 2.65)
    add_rect_2d(L_TANK_2D, 1, TX + 2.36, TY + 2.25, TX + 2.64, TY + 2.65)
    # Panel Doble de Celosía Rústica Abatible en Fachada Sur (X: 0.88..2.33)
    add_rect_2d(L_TANK_2D, 30, TX + 0.88, TY - 0.04, TX + 2.33, TY + 0.18)
    add_text(L_TANK_2D, 2, "Escotilla 0,80x1,25", TX + 0.42, TY + 3.96, 0.0, 0.13)
    add_text(L_TANK_2D, 2, "Bomba+Pulmon", TX + 1.82, TY + 3.35, 0.0, 0.13)
    add_text(L_TANK_2D, 5, "TANQUE 1.000L", TX + 1.12, TY + 1.25, 0.0, 0.14)
    add_text(L_TANK_2D, 2, "(D=1,10 x H=1,30m)", TX + 1.02, TY + 1.02, 0.0, 0.12)
    add_text(L_TANK_2D, 30, "Celosia Abatible 1,45m (Izaje/Vent.)", TX + 0.55, TY - 0.35, 0.0, 0.13)
    add_text(L_TANK_2D, 1, "Parapeto Ciego + Canalon Oculto (Alero 0,00m)", TX - 0.10, TY + 4.62, 0.0, 0.13)

    # Fachada frontal esquemática 2D mostrando cubierta alpina y parapeto izquierdo sin alero
    FX = 30.00
    FY = 2.00
    L_FAC = "FACHADAS_2D"
    add_text(L_FAC, 2, "CORTE / FACHADA FRONTAL CHALET (SIN INVASION VECINO IZQ.)", FX, FY - 0.8, 0.0, 0.28)
    add_rect_2d(L_FAC, 8,  FX + 0.00, FY + 0.00, FX + 0.15, FY + 2.50)          # Vecino izquierdo
    add_rect_2d(L_FAC, 7,  FX + 0.15, FY + 0.00, FX + 9.15, FY + 3.00)          # Planta Baja Comercial + Garaje 3m
    add_rect_2d(L_FAC, 34, FX + 0.15, FY + 3.00, FX + 9.15, FY + 5.85)          # Cuerpo Madera P2
    add_rect_2d(L_FAC, 34, FX + 0.15, FY + 5.85, FX + 0.30, FY + Z_PARAPET_WEST)# Parapeto izquierdo sin alero
    add_rect_2d(L_FAC, 34, FX + 0.15, FY + Z_PARAPET_WEST, FX + 0.30, FY + Z_PARAPET_BUH) # Parapeto fondo Buhardilla
    add_line(L_FAC, 8, FX + 0.30, FY + Z_TANK_FLOOR, 0.0, FX + 2.90, FY + Z_TANK_FLOOR, 0.0) # Losa Tanque +5,68m
    add_rect_2d(L_FAC, 5, FX + 1.00, FY + Z_TANK_BOT, FX + 2.10, FY + Z_TANK_TOP) # Silueta Tanque 1.000L
    add_line(L_FAC, 30, FX + 0.40, FY + z_dormer_under(0.40), 0.0, FX + X_DORM_JOIN, FY + Z_DORM_JOIN, 0.0)
    add_line(L_FAC, 9, FX + 0.40, FY + z_w_bot, 0.0, FX + X_RIDGE, FY + Z_RIDGE, 0.0)
    add_line(L_FAC, 9, FX + X_RIDGE, FY + Z_RIDGE, 0.0, FX + X_EAVE_EAST, FY + Z_EAVE_EAST, 0.0)
    add_text(L_FAC, 1, "Vecino Izq. (Alero 0,00m)", FX - 0.50, FY + 8.05, 0.0, 0.17)
    add_text(L_FAC, 5, "Buhardilla Tanque 1.000L", FX + 0.50, FY + 7.72, 0.0, 0.15)
    add_text(L_FAC, 3, "Alero Propio Der. 0,95m", FX + 8.60, FY + 6.20, 0.0, 0.18)

    # Levantamiento Poligonal UTM intacto
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
    # 7. ESCRITURA DEL ARCHIVO DXF R12 (AC1009 ESTRICTO)
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
    w(30, 10.0)
    w(0, "ENDSEC")

    all_layers = [
        ("0", 7),
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
        (L_ZOCALO, 8),
        ("ESCALERA_3D", 7),
        ("ESCALERA_2D", 7),
        ("ROTULOS_TEXTO", 2),
        (L_P2_SLAB, 8),
        (L_P2_EXT, 34),
        (L_P2_INT, 6),
        (L_P2_COL, 1),
        (L_TIMBER, 34),
        (L_BALC, 30),
        (L_CARP, 34),
        (L_P2_ISL, 3),
        ("P2_ESCALERA_3D", 7),
        (L_TANK_SLAB, 8),
        (L_MAINT_ST, 30),
        (L_HYDRO, 5),
        (L_DORMER, 34),
        (L_GUTTER, 8),
        (L_ROOF, 9),
        ("P2_ROTULOS", 6),
        (L_GRID, 1),
        (L_SOT_2D, 4),
        (L_P2_2D, 6),
        (L_TANK_2D, 5),
        (L_FAC, 3),
        (L_UTM, 7),
    ]

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
        w(11, f"{x2:.4f}"); w(21, f"{y2:.4f}"); w(31, f"{z2:.4f}")

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

    out_path = "02_Modelos_CAD/casa_nuevo_proyecto.dxf"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="latin-1", errors="replace") as f:
        f.writelines(dxf_lines)

    print(f"DXF Chalet Rustico Mejorado generado: {out_path}")
    print(f"Total solidos 3D: {len(boxes_3d) + len(hexahedra_3d)} | Lineas 2D: {len(lines_2d)} | Textos: {len(texts)}")


if __name__ == "__main__":
    build_nuevo_proyecto()
