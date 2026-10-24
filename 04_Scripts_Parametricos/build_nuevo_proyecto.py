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
    # 1. NIVEL SÓTANO CHALET ALPINO (Z = -2.55 a -0.15 m) — OPCIÓN A:
    #    TABERNA RÚSTICA, CAVA DE VINOS, SALÓN CINE, SUITE HUÉSPEDES Y PÉRGOLA
    # =========================================================================
    L_SOT_SLAB   = "SOTANO_LOSA_3D"
    L_SOT_EXT    = "SOTANO_MUROS_EXT_3D"
    L_SOT_INT    = "SOTANO_MUROS_INT_3D"
    L_SOT_COL    = "SOTANO_COLUMNAS_3D"
    L_SOT_TIMBER = "SOTANO_PIEDRA_MADERA_3D"
    L_SOT_FURN   = "SOTANO_MOBILIARIO_3D"

    # Losa Sótano 100% rectangular (X: 0.15 a 9.15 m, Y: 0.00 a 8.30 m)
    add_house_box(L_SOT_SLAB, 8, 0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)
    # Gran Terraza Exterior de Piedra Laja en Patio Trasero (4.20 x 2.20 m = 9.24 m2)
    add_house_box(L_SOT_SLAB, 8, 4.85, -2.20, Z_SOT_FLOOR - 0.08, 9.05, 0.00, Z_SOT_FLOOR + 0.02)

    # Escalera Interior Tramo 1 INTACTA (X: 0.30..1.40, Y: 7.40 -> 4.45), liberando bóveda bajo tramo alto para Maletero
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

    # Muro Oeste Propio en Sótano (X: 0.15..0.30, Y: 0.00..8.30) — Ciego junto a vecino (minX >= 0.15 m)
    add_house_box(L_SOT_EXT, 4, 0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT)

    # Muro Sur hacia Patio Trasero (Y: 0.00..0.15, X: 0.30..9.15) — Abierto al Jardín y Pérgola:
    add_wall_with_openings_x(L_SOT_EXT, 4, 0.30, 9.15, 0.00, 0.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (0.75, 2.35, Z_SOT_FLOOR + 0.85, Z_SOT_FLOOR + 2.10),  # Ventanal Rústico Suite de Huéspedes (1.60 x 1.25 m)
        (3.25, 4.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.15),  # Celosía Alta Baño Rústico en Piedra (1.05 x 0.45 m)
        (4.88, 5.68, Z_SOT_FLOOR + 0.85, Z_SOT_FLOOR + 2.10),  # Ventanal Mirador Sur Barra/Taberna (0.80 x 1.25 m)
        (6.35, 8.55, Z_SOT_FLOOR,        Z_SOT_FLOOR + 2.10),  # GRAN DOBLE PUERTA FRANCESA AL JARDÍN (2.20 x 2.10 m)
    ])
    # Carpintería rústica en fachada Sur del Sótano + hojas plegadas hacia afuera dejando paso libre de 2.06 m
    add_rustic_window_south(0.75, 2.35, Z_SOT_FLOOR + 0.85, Z_SOT_FLOOR + 2.10, with_shutters=True)
    add_rustic_window_south(3.25, 4.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.15, with_shutters=False)
    add_rustic_window_south(4.88, 5.68, Z_SOT_FLOOR + 0.85, Z_SOT_FLOOR + 2.10, with_shutters=False)
    add_house_box(L_CARP, 34, 6.29, -0.04, Z_SOT_FLOOR, 6.36, 0.18, Z_SOT_FLOOR + 2.16)
    add_house_box(L_CARP, 34, 8.54, -0.04, Z_SOT_FLOOR, 8.61, 0.18, Z_SOT_FLOOR + 2.16)
    add_house_box(L_CARP, 34, 6.27, -0.05, Z_SOT_FLOOR + 2.10, 8.63, 0.18, Z_SOT_FLOOR + 2.18)
    # Hojas acristaladas francesas abatidas contra las pilastras exteriores de piedra
    add_house_box(L_CARP, 34, 5.76, -0.10, Z_SOT_FLOOR + 0.02, 6.28, -0.04, Z_SOT_FLOOR + 2.08)
    add_house_box(L_CARP, 34, 8.62, -0.10, Z_SOT_FLOOR + 0.02, 9.10, -0.04, Z_SOT_FLOOR + 2.08)

    # Muro Este Completo sobre Eje 3 (X: 8.95..9.15, Y: 0.15..8.30) con 3 Ventanales al Corredor Jardín (cota -2.55 m):
    add_wall_with_openings_y(L_SOT_EXT, 4, 8.95, 9.15, 0.15, 8.30, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.00, 2.65, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10),  # Ventanal Este 1: Comedor / Juegos Taberna
        (4.25, 5.90, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10),  # Ventanal Este 2: Salón Taberna Central
        (7.00, 7.95, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10),  # Ventanal Este 3: Salón Lounge / Cine
    ])
    add_rustic_window_east(1.00, 2.65, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10, with_shutters=True)
    add_rustic_window_east(4.25, 5.90, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10, with_shutters=True)
    add_rustic_window_east(7.00, 7.95, Z_SOT_FLOOR + 0.90, Z_SOT_FLOOR + 2.10, with_shutters=False)

    # Muro Norte de Contención del Sótano (Y: 8.15..8.30, X: 0.30..9.15) — Inercia térmica para Cava y Lounge
    add_house_box(L_SOT_EXT, 4, 0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT)

    # --- TABIQUERÍA INTERNA REDISEÑADA (OPCIÓN A — ESPACIO SOCIAL DIÁFANO + SUITE + BAÑO + CAVA) ---
    # 1. Cierre lateral de Escalera y Maletero bajo escalera (X: 1.40..1.55, Y: 4.45..8.15) con puerta desde Cava
    add_wall_with_openings_y(L_SOT_INT, 4, 1.40, 1.55, 4.45, 8.15, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (7.22, 7.94, Z_SOT_FLOOR, Z_SOT_FLOOR + 1.92),  # Puerta rústica al Maletero bajo escalera (0.72 x 1.92 m)
    ])
    add_house_box(L_CARP, 34, 1.44, 7.22, Z_SOT_FLOOR, 1.50, 7.94, Z_SOT_FLOOR + 1.92)  # Hoja madera Maletero

    # 2. Muro Norte de Suite de Huéspedes y Baño Rústico sobre Eje G (Y: 3.45..3.60, X: 0.30..4.70)
    add_wall_with_openings_x(L_SOT_INT, 4, 0.30, 4.70, 3.45, 3.60, Z_SOT_FLOOR, Z_P1_SLAB_BOT, [
        (1.78, 2.58, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),  # Puerta Suite de Huéspedes (0.80 x 2.05 m)
        (3.62, 4.42, Z_SOT_FLOOR, Z_SOT_FLOOR + H_DOOR_SOT),  # Puerta Baño Completo Rústico (0.80 x 2.05 m)
    ])
    # Marcos y hojas entreabiertas hacia interior de Suite y Baño
    add_house_box(L_CARP, 34, 1.78, 3.43, Z_SOT_FLOOR + H_DOOR_SOT, 2.58, 3.62, Z_SOT_FLOOR + H_DOOR_SOT + 0.06)
    add_house_box(L_CARP, 34, 2.52, 2.75, Z_SOT_FLOOR, 2.58, 3.45, Z_SOT_FLOOR + H_DOOR_SOT)
    add_house_box(L_CARP, 34, 3.62, 3.43, Z_SOT_FLOOR + H_DOOR_SOT, 4.42, 3.62, Z_SOT_FLOOR + H_DOOR_SOT + 0.06)
    add_house_box(L_CARP, 34, 4.36, 2.75, Z_SOT_FLOOR, 4.42, 3.45, Z_SOT_FLOOR + H_DOOR_SOT)

    # 3. Tabique divisorio entre Suite de Huéspedes y Baño Rústico (X: 2.80..2.95, Y: 0.15..3.45)
    add_house_box(L_SOT_INT, 4, 2.80, 0.15, Z_SOT_FLOOR, 2.95, 3.45, Z_P1_SLAB_BOT)

    # 4. Muro Este del Baño Rústico / Respaldo Hidráulico de la Barra Húmeda (X: 4.55..4.70, Y: 0.15..3.45)
    add_house_box(L_SOT_INT, 4, 4.55, 0.15, Z_SOT_FLOOR, 4.70, 3.45, Z_P1_SLAB_BOT)

    # --- COLUMNAS ESTRUCTURALES DEL SÓTANO (100% CONSERVADAS EN POSICIÓN Y SECCIÓN) ---
    add_house_box(L_SOT_COL, 1, 0.15, 6.35, Z_SOT_FLOOR, 0.30, 6.80, Z_P1_SLAB_BOT)  # Machón enrasado junto a escalera
    sot_cols_axes = [
        (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
        (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
        (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
    ]
    for cx, cy in sot_cols_axes:
        add_house_box(L_SOT_COL, 1, cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)

    # --- ARQUITECTURA INTERIOR Y EXTERIOR CHALET EN PIEDRA Y MADERA (SOTANO_PIEDRA_MADERA_3D) ---
    # 1. Zócalo Exterior de Piedra Rústica hacia Patio Trasero y Corredor Este
    for sx1, sx2 in [(0.15, 0.75), (2.35, 3.25), (4.30, 4.88), (5.68, 6.29), (8.61, 9.20)]:
        add_house_box(L_SOT_TIMBER, 8, sx1, -0.05, Z_SOT_FLOOR, sx2, 0.00, Z_SOT_FLOOR + 1.05)
    for px1, px2 in [(0.15, 0.52), (2.63, 3.02), (5.73, 6.12), (8.78, 9.20)]:
        add_house_box(L_SOT_TIMBER, 8, px1, -0.07, Z_SOT_FLOOR, px2, 0.00, Z_P1_SLAB_BOT)  # Pilastras pétreas Sur
    add_house_box(L_SOT_TIMBER, 8, 9.15, 0.00, Z_SOT_FLOOR, 9.20, 8.30, Z_SOT_FLOOR + 0.90)  # Zócalo pétreo Este

    # 2. Muro interior de Mampostería de Piedra en Contención Norte (Cava + Salón Cine) y Forro de Columnas Libres
    add_house_box(L_SOT_TIMBER, 8, 1.55, 8.07, Z_SOT_FLOOR, 8.95, 8.15, Z_P1_SLAB_BOT)
    for pcx, pcy in [(2.825, 6.575), (5.925, 6.575), (5.925, 3.575)]:
        add_house_box(L_SOT_TIMBER, 8,  pcx - 0.21, pcy - 0.21, Z_SOT_FLOOR, pcx + 0.21, pcy + 0.21, Z_P1_SLAB_BOT - 0.22)
        add_house_box(L_SOT_TIMBER, 34, pcx - 0.24, pcy - 0.24, Z_P1_SLAB_BOT - 0.22, pcx + 0.24, pcy + 0.24, Z_P1_SLAB_BOT - 0.12)

    # 3. Vigas Maestras Rústicas de Techo sobre Ejes de Columnas (peralte 12 cm -> 2.28 m bajo viga y 2.40 m en casetones)
    add_house_box(L_SOT_TIMBER, 34, 1.40, 3.465, Z_P1_SLAB_BOT - 0.12, 8.95, 3.685, Z_P1_SLAB_BOT)  # Viga Eje G
    add_house_box(L_SOT_TIMBER, 34, 1.55, 6.465, Z_P1_SLAB_BOT - 0.12, 8.95, 6.685, Z_P1_SLAB_BOT)  # Viga Eje F
    add_house_box(L_SOT_TIMBER, 34, 5.815, 0.15, Z_P1_SLAB_BOT - 0.12, 6.035, 8.15, Z_P1_SLAB_BOT)  # Viga Eje 2

    # 4. Cerramiento Vitrina de la Cava de Vinos (Zócalo de Piedra + Hierro Forjado Negro + Vidrio Templado)
    # Frente Sur de Cava (Y: 5.25..5.37, X: 1.55..5.80) con Portal Doble Central (X: 3.25..4.45)
    add_house_box(L_SOT_TIMBER, 8, 1.55, 5.25, Z_SOT_FLOOR, 3.25, 5.37, Z_SOT_FLOOR + 0.62)
    add_house_box(L_SOT_TIMBER, 8, 4.45, 5.25, Z_SOT_FLOOR, 5.80, 5.37, Z_SOT_FLOOR + 0.62)
    add_house_box(L_SOT_TIMBER, 34, 1.55, 5.24, Z_SOT_FLOOR + 2.12, 5.80, 5.38, Z_P1_SLAB_BOT)  # Dintel madera Cava
    add_house_box(L_SOT_TIMBER, 4, 1.58, 5.30, Z_SOT_FLOOR + 0.62, 3.23, 5.32, Z_SOT_FLOOR + 2.12)  # Paño vidrio izq
    add_house_box(L_SOT_TIMBER, 4, 4.47, 5.30, Z_SOT_FLOOR + 0.62, 5.78, 5.32, Z_SOT_FLOOR + 2.12)  # Paño vidrio der
    for mx in [1.58, 2.13, 2.68, 3.25, 4.45, 5.12, 5.77]:
        add_house_box(L_SOT_TIMBER, 8, mx - 0.02, 5.27, Z_SOT_FLOOR + (0.0 if mx in (3.25, 4.45) else 0.62),
                      mx + 0.02, 5.35, Z_SOT_FLOOR + 2.12)
    # Hojas dobles de hierro y vidrio de entrada a la Cava (semiabiertas invitando a pasar)
    add_house_box(L_SOT_TIMBER, 4, 3.27, 5.32, Z_SOT_FLOOR + 0.04, 3.82, 5.36, Z_SOT_FLOOR + 2.10)
    add_house_box(L_SOT_TIMBER, 4, 3.88, 5.32, Z_SOT_FLOOR + 0.04, 4.43, 5.36, Z_SOT_FLOOR + 2.10)

    # Frente Este de Cava hacia el Salón Lounge (X: 5.86..5.98, Y: 5.25..6.36 y Y: 6.79..8.07)
    for cy1, cy2 in [(5.25, 6.36), (6.79, 8.07)]:
        add_house_box(L_SOT_TIMBER, 8,  5.86, cy1, Z_SOT_FLOOR, 5.98, cy2, Z_SOT_FLOOR + 0.62)
        add_house_box(L_SOT_TIMBER, 34, 5.85, cy1, Z_SOT_FLOOR + 2.12, 5.99, cy2, Z_P1_SLAB_BOT)
        add_house_box(L_SOT_TIMBER, 4,  5.91, cy1 + 0.02, Z_SOT_FLOOR + 0.62, 5.93, cy2 - 0.02, Z_SOT_FLOOR + 2.12)
        add_house_box(L_SOT_TIMBER, 8,  5.89, 0.5 * (cy1 + cy2) - 0.02, Z_SOT_FLOOR + 0.62,
                      5.95, 0.5 * (cy1 + cy2) + 0.02, Z_SOT_FLOOR + 2.12)

    # 5. Pérgola Rústica de Piedra y Madera en el Patio Trasero (X: 4.85..9.05, Y_casa: -2.15..0.00)
    for pg_x in [4.95, 6.91, 8.82]:
        add_house_box(L_SOT_TIMBER, 8,  pg_x - 0.04, -2.14, Z_SOT_FLOOR + 0.02, pg_x + 0.22, -1.88, Z_SOT_FLOOR + 0.72)
        add_house_box(L_SOT_TIMBER, 34, pg_x,        -2.10, Z_SOT_FLOOR + 0.72, pg_x + 0.18, -1.92, Z_P1_SLAB_BOT - 0.13)
        # Tornapuntas rústicos superiores
        add_house_box(L_SOT_TIMBER, 34, pg_x - 0.16, -2.07, Z_P1_SLAB_BOT - 0.35, pg_x + 0.34, -1.95, Z_P1_SLAB_BOT - 0.25)
    # Viga maestra frontal Sur y viga mural de la Pérgola + 9 cabrios de sombra (Z máx = -0.04 m < P1)
    add_house_box(L_SOT_TIMBER, 34, 4.85, -2.12, Z_P1_SLAB_BOT - 0.13, 9.08, -1.90, Z_P1_SLAB_BOT - 0.01)
    add_house_box(L_SOT_TIMBER, 34, 4.85, -0.14, Z_P1_SLAB_BOT - 0.13, 9.08,  0.00, Z_P1_SLAB_BOT - 0.01)
    for r_i in range(9):
        rx = 4.96 + r_i * 0.49
        add_house_box(L_SOT_TIMBER, 30, rx, -2.24, Z_P1_SLAB_BOT - 0.01, rx + 0.09, -0.01, Z_P1_FLOOR - 0.04)

    # --- MOBILIARIO COMPLETO DEL SÓTANO Y JARDÍN (SOTANO_MOBILIARIO_3D) ---
    # A. Cava de Vinos: Botelleros de Roble de Piso a Techo + Mesa Alta de Cata / Barrica + 4 Taburetes
    add_house_box(L_SOT_FURN, 34, 2.15, 7.72, Z_SOT_FLOOR, 5.78, 8.07, Z_SOT_FLOOR + 2.18)  # Botellero Muro Norte
    add_house_box(L_SOT_FURN, 8,  2.17, 7.69, Z_SOT_FLOOR + 0.92, 5.76, 8.06, Z_SOT_FLOOR + 0.98)  # Nicho piedra decantación
    for wx in [2.75, 3.35, 3.95, 4.55, 5.15]:
        add_house_box(L_SOT_FURN, 30, wx, 7.70, Z_SOT_FLOOR + 0.05, wx + 0.04, 8.06, Z_SOT_FLOOR + 2.12)
    add_house_box(L_SOT_FURN, 34, 1.56, 5.42, Z_SOT_FLOOR, 1.92, 7.05, Z_SOT_FLOOR + 2.18)  # Botellero Oeste Reserva
    # Mesa Alta de Cata sobre barricas rústicas (1.15 x 0.70 m, H = 1.00 m) + 4 Taburetes
    add_house_box(L_SOT_FURN, 34, 3.85, 6.32, Z_SOT_FLOOR, 4.18, 6.82, Z_SOT_FLOOR + 0.94)  # Pedestal Barrica 1
    add_house_box(L_SOT_FURN, 34, 4.52, 6.32, Z_SOT_FLOOR, 4.85, 6.82, Z_SOT_FLOOR + 0.94)  # Pedestal Barrica 2
    add_house_box(L_SOT_FURN, 30, 3.75, 6.22, Z_SOT_FLOOR + 0.94, 4.95, 6.92, Z_SOT_FLOOR + 1.01)  # Tablero Roble Cata
    for ts_x in [3.92, 4.48]:
        add_house_box(L_SOT_FURN, 30, ts_x, 5.84, Z_SOT_FLOOR, ts_x + 0.30, 6.14, Z_SOT_FLOOR + 0.72)
        add_house_box(L_SOT_FURN, 30, ts_x, 7.00, Z_SOT_FLOOR, ts_x + 0.30, 7.30, Z_SOT_FLOOR + 0.72)

    # B. Maletero Bajo Escalera: Estanterías de madera al fondo Norte (X: 0.32..1.38, Y: 7.78..8.13)
    for sh_z in [0.45, 0.95, 1.45, 1.90]:
        add_house_box(L_SOT_FURN, 34, 0.32, 7.78, Z_SOT_FLOOR + sh_z, 1.38, 8.13, Z_SOT_FLOOR + sh_z + 0.04)

    # C. Barra Húmeda Alpina (Wet Bar) adosada al muro Este del Baño (X: 4.70..5.30, Y: 1.15..3.35)
    add_house_box(L_SOT_FURN, 34, 4.70, 1.15, Z_SOT_FLOOR, 5.28, 3.35, Z_SOT_FLOOR + 0.88)        # Mueble bajo madera
    add_house_box(L_SOT_FURN, 8,  4.70, 1.13, Z_SOT_FLOOR + 0.88, 5.32, 3.37, Z_SOT_FLOOR + 0.94) # Tope piedra pizarra
    add_house_box(L_SOT_FURN, 7,  4.80, 2.55, Z_SOT_FLOOR + 0.89, 5.20, 3.00, Z_SOT_FLOOR + 0.95) # Bar sink inox
    add_house_box(L_SOT_FURN, 5,  4.74, 1.25, Z_SOT_FLOOR + 0.05, 5.29, 1.85, Z_SOT_FLOOR + 0.86) # Vinera refrigerada
    add_house_box(L_SOT_FURN, 34, 4.70, 1.20, Z_SOT_FLOOR + 1.45, 4.98, 3.30, Z_SOT_FLOOR + 1.50) # Repisa licores 1
    add_house_box(L_SOT_FURN, 34, 4.70, 1.20, Z_SOT_FLOOR + 1.85, 4.98, 3.30, Z_SOT_FLOOR + 1.90) # Repisa licores 2

    # D. Salón Lounge & Cine Familiar (Noreste: X: 6.15..8.90, Y: 4.75..8.07)
    # Mueble bajo rústico + Pantalla Cine/TV 85" sobre el muro Norte de piedra
    add_house_box(L_SOT_FURN, 34, 6.35, 7.62, Z_SOT_FLOOR, 8.55, 8.05, Z_SOT_FLOOR + 0.54)
    add_house_box(L_SOT_FURN, 8,  6.50, 7.96, Z_SOT_FLOOR + 0.72, 8.40, 8.04, Z_SOT_FLOOR + 1.82)  # TV 85" (1.90 x 1.10 m)
    # Gran Sofá Lounge en L (mirando a la pantalla 85" y a la Cava iluminada, bajo antepecho Este 0.90 m)
    add_house_box(L_SOT_FURN, 30, 6.22, 4.82, Z_SOT_FLOOR, 8.75, 5.72, Z_SOT_FLOOR + 0.44)  # Asiento Sur
    add_house_box(L_SOT_FURN, 30, 6.22, 4.82, Z_SOT_FLOOR + 0.44, 8.75, 5.04, Z_SOT_FLOOR + 0.84)  # Respaldo Sur
    add_house_box(L_SOT_FURN, 30, 7.88, 5.72, Z_SOT_FLOOR, 8.75, 6.90, Z_SOT_FLOOR + 0.44)  # Chaise Este
    add_house_box(L_SOT_FURN, 30, 8.53, 5.04, Z_SOT_FLOOR + 0.44, 8.75, 6.90, Z_SOT_FLOOR + 0.84)  # Respaldo Este
    # Mesa de centro de tronco macizo
    add_house_box(L_SOT_FURN, 34, 6.65, 6.02, Z_SOT_FLOOR, 7.55, 6.65, Z_SOT_FLOOR + 0.40)

    # E. Comedor / Mesa de Juegos de Taberna frente al Jardín (Sureste: X: 7.05..8.00, Y: 1.25..3.05, 6 puestos)
    add_house_box(L_SOT_FURN, 34, 7.05, 1.25, Z_SOT_FLOOR + 0.70, 8.00, 3.05, Z_SOT_FLOOR + 0.77)  # Tablero 1.80 x 0.95 m
    add_house_box(L_SOT_FURN, 34, 7.25, 1.48, Z_SOT_FLOOR, 7.80, 1.66, Z_SOT_FLOOR + 0.70)
    add_house_box(L_SOT_FURN, 34, 7.25, 2.64, Z_SOT_FLOOR, 7.80, 2.82, Z_SOT_FLOOR + 0.70)
    for ty_ch in [1.48, 2.34]:
        add_house_box(L_SOT_FURN, 30, 6.60, ty_ch, Z_SOT_FLOOR, 7.00, ty_ch + 0.44, Z_SOT_FLOOR + 0.46)
        add_house_box(L_SOT_FURN, 30, 6.60, ty_ch, Z_SOT_FLOOR + 0.46, 6.68, ty_ch + 0.44, Z_SOT_FLOOR + 0.88)
        add_house_box(L_SOT_FURN, 30, 8.05, ty_ch, Z_SOT_FLOOR, 8.45, ty_ch + 0.44, Z_SOT_FLOOR + 0.46)
        add_house_box(L_SOT_FURN, 30, 8.37, ty_ch, Z_SOT_FLOOR + 0.46, 8.45, ty_ch + 0.44, Z_SOT_FLOOR + 0.88)
    add_house_box(L_SOT_FURN, 30, 7.30, 0.80, Z_SOT_FLOOR, 7.75, 1.20, Z_SOT_FLOOR + 0.46)
    add_house_box(L_SOT_FURN, 30, 7.30, 3.10, Z_SOT_FLOOR, 7.75, 3.48, Z_SOT_FLOOR + 0.46)

    # F. Suite de Huéspedes (Suroeste: X: 0.30..2.80, Y: 0.15..3.45) — Cama Doble + Mesas Noche + Clóset Rústico
    add_house_box(L_SOT_FURN, 34, 0.32, 0.88, Z_SOT_FLOOR, 0.40, 2.42, Z_SOT_FLOOR + 1.18)        # Cabecero madera
    add_house_box(L_SOT_FURN, 30, 0.40, 0.95, Z_SOT_FLOOR, 2.22, 2.35, Z_SOT_FLOOR + 0.34)        # Base cama 1.40 x 1.82
    add_house_box(L_SOT_FURN, 7,  0.42, 0.99, Z_SOT_FLOOR + 0.34, 2.18, 2.31, Z_SOT_FLOOR + 0.56) # Colchón + lencería
    add_house_box(L_SOT_FURN, 34, 0.34, 0.45, Z_SOT_FLOOR + 0.15, 0.72, 0.86, Z_SOT_FLOOR + 0.54) # Mesa noche Sur
    add_house_box(L_SOT_FURN, 34, 0.34, 2.44, Z_SOT_FLOOR + 0.15, 0.72, 2.85, Z_SOT_FLOOR + 0.54) # Mesa noche Norte
    add_house_box(L_SOT_FURN, 34, 0.52, 2.92, Z_SOT_FLOOR, 1.66, 3.43, Z_SOT_FLOOR + 2.15)        # Clóset rústico huéspedes

    # G. Baño Completo Rústico en Piedra (X: 2.95..4.55, Y: 0.15..3.45) — Ducha Walk-In + WC + Tocador Piedra
    add_house_box(L_SOT_FURN, 8,  2.96, 0.16, Z_SOT_FLOOR, 4.54, 1.05, Z_SOT_FLOOR + 0.05)        # Plato ducha pizarra
    add_house_box(L_SOT_FURN, 8,  4.14, 0.17, Z_SOT_FLOOR + 0.05, 4.53, 0.98, Z_SOT_FLOOR + 0.46) # Banco de piedra ducha
    add_house_box(L_SOT_FURN, 4,  2.96, 1.03, Z_SOT_FLOOR + 0.05, 3.85, 1.06, Z_SOT_FLOOR + 2.02) # Mampara vidrio fija
    add_house_box(L_SOT_FURN, 7,  2.98, 1.32, Z_SOT_FLOOR, 3.64, 1.72, Z_SOT_FLOOR + 0.42)        # Taza WC
    add_house_box(L_SOT_FURN, 7,  2.98, 1.32, Z_SOT_FLOOR + 0.42, 3.20, 1.72, Z_SOT_FLOOR + 0.80) # Tanque WC
    add_house_box(L_SOT_FURN, 34, 2.98, 2.02, Z_SOT_FLOOR + 0.48, 3.50, 2.96, Z_SOT_FLOOR + 0.82) # Tocador madera suspendido
    add_house_box(L_SOT_FURN, 8,  3.10, 2.30, Z_SOT_FLOOR + 0.82, 3.44, 2.68, Z_SOT_FLOOR + 0.97) # Lavamanos piedra tallada
    add_house_box(L_SOT_FURN, 8,  2.96, 2.08, Z_SOT_FLOOR + 1.05, 2.99, 2.90, Z_SOT_FLOOR + 1.95) # Espejo marco hierro

    # H. Mobiliario Exterior bajo la Pérgola del Patio Trasero + Jardinera de Piedra Sur
    add_house_box(L_SOT_FURN, 34, 5.05, -2.02, Z_SOT_FLOOR + 0.02, 6.22, -1.32, Z_SOT_FLOOR + 0.44) # Sofá exterior jardín
    add_house_box(L_SOT_FURN, 34, 5.05, -2.02, Z_SOT_FLOOR + 0.44, 6.22, -1.84, Z_SOT_FLOOR + 0.82)
    add_house_box(L_SOT_FURN, 8,  5.35, -1.16, Z_SOT_FLOOR + 0.02, 6.05, -0.68, Z_SOT_FLOOR + 0.40) # Mesa piedra jardín
    add_house_box(L_SOT_FURN, 34, 8.18, -1.96, Z_SOT_FLOOR + 0.02, 8.84, -1.30, Z_SOT_FLOOR + 0.46) # Poltrona exterior Este
    add_house_box(L_SOT_FURN, 8,  0.65, -0.52, Z_SOT_FLOOR, 2.45, -0.04, Z_SOT_FLOOR + 0.45)        # Jardinera piedra Sur
    add_house_box(L_SOT_FURN, 3,  0.72, -0.46, Z_SOT_FLOOR + 0.45, 2.38, -0.10, Z_SOT_FLOOR + 0.72) # Vegetación jardinera

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
    # Poste Timber Frame en Columna 1-G (2.825, 3.575) enmarcando el nuevo Portal de Conexión al Vestíbulo
    add_house_box(L_TIMBER, 34, 2.68, 3.43, Z_P2_FLOOR, 2.97, 3.72, 5.50)
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

    # Losa Entrepiso P2 ahora 100% rectangular (9.00 x 21.71 m) cerrando el vacío izquierdo (X: 0.15..1.55, Y: 4.40..7.35)
    add_house_box(L_P2_SLAB, 8, 0.15, 0.00, H_P1, 9.15, 4.40, Z_P2_FLOOR)
    add_house_box(L_P2_SLAB, 8, 0.15, 4.40, H_P1, 1.55, 7.35, Z_P2_FLOOR)  # Nuevo piso Despensa + Clóset de Blancos
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

    # 3. División Gran Vestier Walk-In / Gran Baño En-Suite Spa (3.00 x 2.30 m): Y = 12.45..12.60
    add_wall_with_openings_x(L_P2_INT, 6, 6.00, 9.00, 12.45, 12.60, Z_P2_FLOOR, H_P2, [
        (7.10, 7.90, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),        # Puerta privada al Baño Spa Master
    ])

    # --- INTERIORISMO Y MOBILIARIO 3D DE LA MASTER SUITE CHALET (TERRAZA + SUITE + VESTIER + BAÑO SPA) ---
    L_SUITE_FURN = "P2_MOBILIARIO_SUITE_3D"

    # A) Terraza Privada Master Suite (X: 6.00..9.00, Y: 19.60..21.56):
    #    Dos poltronas bajas de madera teca y cuerda + mesa de tronco macizo + jardinera aromática en piedra
    add_house_box(L_SUITE_FURN, 34, 6.12, 20.45, Z_P2_FLOOR,        6.82, 21.15, Z_P2_FLOOR + 0.40)  # Asiento poltrona 1
    add_house_box(L_SUITE_FURN, 30, 6.12, 20.45, Z_P2_FLOOR + 0.40, 6.26, 21.15, Z_P2_FLOOR + 0.80)  # Respaldo poltrona 1
    add_house_box(L_SUITE_FURN, 34, 6.95, 20.60, Z_P2_FLOOR,        7.40, 21.05, Z_P2_FLOOR + 0.44)  # Mesa tronco macizo
    add_house_box(L_SUITE_FURN, 34, 7.52, 20.55, Z_P2_FLOOR,        8.22, 21.25, Z_P2_FLOOR + 0.40)  # Asiento poltrona 2
    add_house_box(L_SUITE_FURN, 30, 7.52, 21.11, Z_P2_FLOOR + 0.40, 8.22, 21.25, Z_P2_FLOOR + 0.80)  # Respaldo poltrona 2
    add_house_box(L_SUITE_FURN, 8,  8.38, 20.68, Z_P2_FLOOR,        8.92, 21.38, Z_P2_FLOOR + 0.50)  # Jardinera piedra/madera
    add_house_box(L_SUITE_FURN, 3,  8.44, 20.74, Z_P2_FLOOR + 0.50, 8.86, 21.32, Z_P2_FLOOR + 0.92)  # Follaje aromático

    # B) Dormitorio Master Suite Chalet (X: 6.00..9.00, Y: 14.95..19.45):
    #    Muro cabecero protagonista en madera envejecida y piedra laja (X: 6.05..6.13, Y: 16.10..19.30, Z: 3.00..5.40)
    add_house_box(L_SUITE_FURN, 34, 6.05, 16.10, Z_P2_FLOOR, 6.11, 19.30, Z_P2_FLOOR + 2.40)
    add_house_box(L_SUITE_FURN, 8,  6.11, 16.65, Z_P2_FLOOR, 6.14, 18.55, Z_P2_FLOOR + 2.40)         # Paño central piedra laja
    #    Alfombra tejida natural + Cama Queen/King orientada al Ventanal Este (paso libre frontal de 0,97 m)
    add_house_box(L_SUITE_FURN, 30, 6.30, 16.35, Z_P2_FLOOR,        8.32, 18.85, Z_P2_FLOOR + 0.02)  # Alfombra yute/lana
    add_house_box(L_SUITE_FURN, 34, 6.14, 16.75, Z_P2_FLOOR,        8.03, 18.45, Z_P2_FLOOR + 0.32)  # Base madera maciza
    add_house_box(L_SUITE_FURN, 7,  6.18, 16.79, Z_P2_FLOOR + 0.32, 7.99, 18.41, Z_P2_FLOOR + 0.58)  # Colchón + lino crudo
    add_house_box(L_SUITE_FURN, 30, 6.14, 16.72, Z_P2_FLOOR + 0.58, 6.26, 18.48, Z_P2_FLOOR + 1.22)  # Cabecero cuero/lino
    add_house_box(L_SUITE_FURN, 7,  6.27, 16.86, Z_P2_FLOOR + 0.58, 6.56, 17.54, Z_P2_FLOOR + 0.74)  # Almohadón sur
    add_house_box(L_SUITE_FURN, 7,  6.27, 17.66, Z_P2_FLOOR + 0.58, 6.56, 18.34, Z_P2_FLOOR + 0.74)  # Almohadón norte
    #    Dos mesas de noche flotantes en madera maciza + lámparas colgantes en hierro negro
    for ny1, ny2, ly in [(16.14, 16.68, 16.41), (18.52, 19.06, 18.79)]:
        add_house_box(L_SUITE_FURN, 34, 6.14, ny1, Z_P2_FLOOR + 0.38, 6.60, ny2, Z_P2_FLOOR + 0.54)
        add_house_box(L_SUITE_FURN, 8,  6.34, ly - 0.02, Z_P2_FLOOR + 1.05, 6.38, ly + 0.02, Z_P2_FLOOR + 2.40)
        add_house_box(L_SUITE_FURN, 30, 6.26, ly - 0.10, Z_P2_FLOOR + 0.88, 6.46, ly + 0.10, Z_P2_FLOOR + 1.05)
    #    Consola baja rústica en paño noreste (sin obstruir el ventanal panorámico Y: 16.00..18.20)
    add_house_box(L_SUITE_FURN, 34, 8.50, 18.28, Z_P2_FLOOR, 8.94, 19.32, Z_P2_FLOOR + 0.62)

    # C) Gran Vestier Walk-In (X: 6.00..9.00, Y: 12.60..14.80):
    #    Puerta corredera rústica tipo Granero (Barn Door) con riel de hierro negro visto
    add_house_box(L_CARP, 8,  7.00, 14.95, Z_P2_FLOOR + 2.16, 8.90, 15.00, Z_P2_FLOOR + 2.22)        # Riel hierro negro
    add_house_box(L_CARP, 30, 7.98, 14.96, Z_P2_FLOOR + 0.02, 8.88, 15.01, Z_P2_FLOOR + 2.16)        # Hoja granero abierta
    #    Ebanistería paralela de madera y celosía ventilada (4,20 m lineales: gaveteros + colgado + maletero)
    for wx1, wx2 in [(6.05, 6.60), (8.40, 8.95)]:
        add_house_box(L_TIMBER, 34, wx1, 12.65, Z_P2_FLOOR,        wx2, 14.75, Z_P2_FLOOR + 0.85)    # Módulo gavetero/zapatera
        add_house_box(L_TIMBER, 34, wx1, 12.65, Z_P2_FLOOR + 2.00, wx2, 14.75, Z_P2_FLOOR + 2.40)    # Maletero superior
        add_house_box(L_TIMBER, 34, wx1, 12.65, Z_P2_FLOOR + 0.85, wx2, 12.73, Z_P2_FLOOR + 2.00)    # Costado sur
        add_house_box(L_TIMBER, 34, wx1, 13.66, Z_P2_FLOOR + 0.85, wx2, 13.74, Z_P2_FLOOR + 2.00)    # Divisoria central
        add_house_box(L_TIMBER, 34, wx1, 14.67, Z_P2_FLOOR + 0.85, wx2, 14.75, Z_P2_FLOOR + 2.00)    # Costado norte
        x_bar = (wx1 + wx2) * 0.5
        add_house_box(L_SUITE_FURN, 8, x_bar - 0.02, 12.73, Z_P2_FLOOR + 1.85, x_bar + 0.02, 14.67, Z_P2_FLOOR + 1.89)
    #    Pouf / Banqueta central tapizada en cuero + Espejo de cuerpo entero con marco de hierro negro
    add_house_box(L_SUITE_FURN, 34, 7.22, 13.35, Z_P2_FLOOR,        7.78, 14.05, Z_P2_FLOOR + 0.18)
    add_house_box(L_SUITE_FURN, 30, 7.20, 13.33, Z_P2_FLOOR + 0.18, 7.80, 14.07, Z_P2_FLOOR + 0.44)
    add_house_box(L_SUITE_FURN, 8,  6.63, 12.60, Z_P2_FLOOR + 0.08, 7.05, 12.64, Z_P2_FLOOR + 2.05)  # Marco espejo hierro
    add_house_box(L_SUITE_FURN, 4,  6.67, 12.64, Z_P2_FLOOR + 0.12, 7.01, 12.66, Z_P2_FLOOR + 2.01)  # Cristal espejo

    # D) Gran Baño En-Suite Tipo Spa Alpino (X: 6.00..9.00, Y: 10.15..12.45):
    #    1. Tocador doble en madera maciza + 2 lavamanos de piedra sobre tope + grifería negra + 2 espejos retroiluminados
    add_house_box(L_P2_ISL,     34, 6.05, 10.30, Z_P2_FLOOR + 0.18, 6.58, 11.88, Z_P2_FLOOR + 0.25)  # Repisa inferior toallas
    add_house_box(L_P2_ISL,     34, 6.05, 10.30, Z_P2_FLOOR + 0.76, 6.60, 11.88, Z_P2_FLOOR + 0.86)  # Tope madera maciza
    for sy1, sy2, scy in [(10.50, 10.92, 10.71), (11.26, 11.68, 11.47)]:
        add_house_box(L_SUITE_FURN, 7, 6.16, sy1, Z_P2_FLOOR + 0.86, 6.50, sy2, Z_P2_FLOOR + 1.02)   # Vessel sink piedra/cerámica
        add_house_box(L_SUITE_FURN, 8, 6.08, scy - 0.03, Z_P2_FLOOR + 0.86, 6.20, scy + 0.03, Z_P2_FLOOR + 1.16) # Grifo negro
        add_house_box(L_SUITE_FURN, 8, 6.05, sy1 - 0.03, Z_P2_FLOOR + 1.12, 6.08, sy2 + 0.03, Z_P2_FLOOR + 2.15) # Marco espejo
        add_house_box(L_SUITE_FURN, 4, 6.08, sy1,        Z_P2_FLOOR + 1.15, 6.10, sy2,        Z_P2_FLOOR + 2.12) # Luna espejo
    #    2. Ducha Walk-In Panorámica Spa (X: 7.95..8.95, Y: 10.15..12.45): piedra pizarra, mampara perfil negro y banco
    add_house_box(L_SUITE_FURN, 8,  7.95, 10.15, Z_P2_FLOOR,        8.95, 12.45, Z_P2_FLOOR + 0.05)  # Plato pizarra antideslizante
    add_house_box(L_SUITE_FURN, 8,  8.55, 10.18, Z_P2_FLOOR + 0.05, 8.94, 11.65, Z_P2_FLOOR + 0.48)  # Banco corrido de piedra
    add_house_box(L_SUITE_FURN, 8,  7.95, 10.15, Z_P2_FLOOR + 0.05, 8.01, 10.21, Z_P2_FLOOR + 2.15)  # Perfil vertical sur mampara
    add_house_box(L_SUITE_FURN, 8,  7.95, 11.50, Z_P2_FLOOR + 0.05, 8.01, 11.56, Z_P2_FLOOR + 2.15)  # Perfil vertical norte mampara
    add_house_box(L_SUITE_FURN, 8,  7.95, 10.15, Z_P2_FLOOR + 2.10, 8.01, 11.56, Z_P2_FLOOR + 2.16)  # Perfil superior negro
    add_house_box(L_SUITE_FURN, 4,  7.97, 10.21, Z_P2_FLOOR + 0.05, 7.99, 11.50, Z_P2_FLOOR + 2.10)  # Cristal templado ducha
    add_house_box(L_SUITE_FURN, 8,  8.38, 11.92, Z_P2_FLOOR + 2.12, 8.94, 12.16, Z_P2_FLOOR + 2.20)  # Regadera Rain Shower negra
    #    3. Inodoro discreto fuera del eje visual de entrada (X: 6.98..7.42, Y: 10.16..10.78)
    add_house_box(L_SUITE_FURN, 7,  6.98, 10.16, Z_P2_FLOOR, 7.42, 10.36, Z_P2_FLOOR + 0.82)         # Tanque bajo
    add_house_box(L_SUITE_FURN, 7,  7.02, 10.36, Z_P2_FLOOR, 7.38, 10.78, Z_P2_FLOOR + 0.42)         # Taza elongada

    # 4. Muro divisorio Sur del Baño Spa Master / Norte de Habitación 2 (Y: 10.00..10.15)
    add_house_box(L_P2_INT, 6, 6.00, 10.00, Z_P2_FLOOR, 9.00, 10.15, H_P2)

    # 5. Muro divisorio Habitación 2 (3.00 x 3.55 m) / Baño Familiar (3.00 x 1.85 m): Y = 6.30..6.45
    add_house_box(L_P2_INT, 6, 6.00, 6.30, Z_P2_FLOOR, 9.00, 6.45, H_P2)

    # 6. Muro divisorio Baño Familiar / Habitación 3 Esquinera (3.00 x 4.15 m): Y = 4.30..4.45
    add_house_box(L_P2_INT, 6, 6.00, 4.30, Z_P2_FLOOR, 9.00, 4.45, H_P2)

    # 7. Cocina Rústica de Montaña + Mobiliario Integral de Área Social (Cocina, Comedor, Sala y Balconada)
    L_SOCIAL_FURN = "P2_MOBILIARIO_SOCIAL_3D"

    # A) COCINA RÚSTICA: Bloque Alto de Nevera/Hornos + Mesón Lineal con Fregadero y Tope 5 Hornillas + Isla +15 cm
    #    1. Bloque Alto Sur Empotrado (X: 1.42..2.74, Y: 7.50..8.28): Nevera French Door + Torre Horno/Microondas
    add_house_box(L_P2_ISL,      34, 1.42, 7.50, Z_P2_FLOOR,        1.46, 8.28, Z_P2_FLOOR + 2.28)  # Costado madera izq.
    add_house_box(L_P2_ISL,      34, 2.70, 7.50, Z_P2_FLOOR,        2.74, 8.28, Z_P2_FLOOR + 2.28)  # Costado madera der.
    add_house_box(L_P2_ISL,      34, 1.42, 7.50, Z_P2_FLOOR + 1.92, 2.74, 8.28, Z_P2_FLOOR + 2.28)  # Mueble puente superior
    add_house_box(L_SOCIAL_FURN, 8,  1.46, 7.52, Z_P2_FLOOR + 0.02, 2.32, 8.30, Z_P2_FLOOR + 0.68)  # Gaveta freezer nevera
    add_house_box(L_SOCIAL_FURN, 8,  1.46, 7.52, Z_P2_FLOOR + 0.70, 1.88, 8.30, Z_P2_FLOOR + 1.90)  # Puerta izq. French Door
    add_house_box(L_SOCIAL_FURN, 8,  1.90, 7.52, Z_P2_FLOOR + 0.70, 2.32, 8.30, Z_P2_FLOOR + 1.90)  # Puerta der. French Door
    add_house_box(L_SOCIAL_FURN, 30, 1.84, 8.30, Z_P2_FLOOR + 0.85, 1.94, 8.34, Z_P2_FLOOR + 1.65)  # Tiradores bronce/madera
    add_house_box(L_P2_ISL,      34, 2.34, 7.50, Z_P2_FLOOR,        2.70, 8.26, Z_P2_FLOOR + 0.66)  # Base torre de hornos
    add_house_box(L_SOCIAL_FURN, 8,  2.34, 7.52, Z_P2_FLOOR + 0.67, 2.70, 8.27, Z_P2_FLOOR + 1.27)  # Horno empotrado
    add_house_box(L_SOCIAL_FURN, 4,  2.38, 8.27, Z_P2_FLOOR + 0.74, 2.66, 8.29, Z_P2_FLOOR + 1.18)  # Cristal horno
    add_house_box(L_SOCIAL_FURN, 8,  2.34, 7.52, Z_P2_FLOOR + 1.29, 2.70, 8.27, Z_P2_FLOOR + 1.68)  # Microondas empotrado
    add_house_box(L_P2_ISL,      34, 2.34, 7.50, Z_P2_FLOOR + 1.70, 2.70, 8.26, Z_P2_FLOOR + 1.92)  # Alacena sobre microondas

    #    2. Mesón Lineal Oeste (X: 0.30..0.96, Y: 8.35..13.20): Fregadero Farmhouse + Cocina 5 Hornillas + Campana Chalet
    add_house_box(L_P2_ISL,      34, 0.30, 8.35, Z_P2_FLOOR,        0.92, 13.20, Z_P2_FLOOR + 0.85) # Mueble bajo madera
    add_house_box(L_P2_ISL,      8,  0.30, 8.35, Z_P2_FLOOR + 0.85, 0.96, 13.20, Z_P2_FLOOR + 0.91) # Tope piedra gris mate
    add_house_box(L_SOCIAL_FURN, 8,  0.30, 8.35, Z_P2_FLOOR + 0.91, 0.34, 13.20, Z_P2_FLOOR + 1.48) # Salpicadero piedra laja
    add_house_box(L_SOCIAL_FURN, 7,  0.88, 9.15, Z_P2_FLOOR + 0.66, 0.98, 10.10, Z_P2_FLOOR + 0.92) # Fregadero Farmhouse doble
    add_house_box(L_SOCIAL_FURN, 8,  0.36, 9.60, Z_P2_FLOOR + 0.91, 0.58, 9.66,  Z_P2_FLOOR + 1.28) # Grifería alta negra
    add_house_box(L_SOCIAL_FURN, 8,  0.38, 11.00, Z_P2_FLOOR + 0.91, 0.88, 11.95, Z_P2_FLOOR + 0.95)# Cocina a gas 5 hornillas
    add_house_box(L_SOCIAL_FURN, 8,  0.91, 11.05, Z_P2_FLOOR + 0.16, 0.95, 11.90, Z_P2_FLOOR + 0.76)# Frente horno bajo tope
    #    Campana extractora piramidal en madera y cinchos de hierro + Alacenas aéreas (bajo cota canalón Z=5.82)
    add_house_box(L_SOCIAL_FURN, 8,  0.30, 10.95, Z_P2_FLOOR + 1.55, 0.94, 12.00, Z_P2_FLOOR + 1.65)# Faldón hierro campana
    add_house_hexa(L_SOCIAL_FURN, 34, [
        (0.30, 10.95, Z_P2_FLOOR + 1.65), (0.92, 10.95, Z_P2_FLOOR + 1.65),
        (0.92, 12.00, Z_P2_FLOOR + 1.65), (0.30, 12.00, Z_P2_FLOOR + 1.65),
        (0.30, 11.15, Z_P2_FLOOR + 2.45), (0.62, 11.15, Z_P2_FLOOR + 2.45),
        (0.62, 11.80, Z_P2_FLOOR + 2.45), (0.30, 11.80, Z_P2_FLOOR + 2.45),
    ])
    add_house_box(L_P2_ISL, 34, 0.30, 8.40,  Z_P2_FLOOR + 1.48, 0.66, 10.80, Z_P2_FLOOR + 2.30)     # Alacena aérea sur
    add_house_box(L_P2_ISL, 34, 0.30, 12.15, Z_P2_FLOOR + 1.48, 0.66, 13.18, Z_P2_FLOOR + 2.30)     # Alacena estación café

    #    3. Isla Central Maciza desplazada +15 cm al Este (X: 2.10..3.12 -> pasillo trabajo 1,14 m) + 4 Taburetes
    add_house_box(L_P2_ISL, 34, 2.10, 9.55, Z_P2_FLOOR,        2.82, 12.15, Z_P2_FLOOR + 0.85)      # Cuerpo isla madera/piedra
    add_house_box(L_P2_ISL, 8,  2.08, 9.55, Z_P2_FLOOR + 0.85, 2.86, 12.15, Z_P2_FLOOR + 0.91)      # Tope piedra isla
    add_house_box(L_P2_ISL, 30, 2.82, 9.55, Z_P2_FLOOR + 0.84, 3.14, 11.86, Z_P2_FLOOR + 0.90)      # Barra volada tablón rústico
    for b_y in [9.80, 10.38, 10.96, 11.54]:
        add_house_box(L_SOCIAL_FURN, 8,  3.06, b_y - 0.17, Z_P2_FLOOR,        3.42, b_y + 0.17, Z_P2_FLOOR + 0.62)
        add_house_box(L_SOCIAL_FURN, 30, 3.04, b_y - 0.19, Z_P2_FLOOR + 0.62, 3.44, b_y + 0.19, Z_P2_FLOOR + 0.70)
        add_house_box(L_SOCIAL_FURN, 30, 3.36, b_y - 0.18, Z_P2_FLOOR + 0.70, 3.44, b_y + 0.18, Z_P2_FLOOR + 0.95)
    for l_y in [10.25, 11.35]:
        add_house_box(L_SOCIAL_FURN, 8,  2.48, l_y - 0.12, Z_P2_FLOOR + 1.85, 2.68, l_y + 0.12, Z_P2_FLOOR + 2.02)

    # B) GRAN COMEDOR RÚSTICO 8 PUESTOS (Claro sin columnas Y: 13.10..15.10) + BUFFET / VINERA
    add_house_box(L_SOCIAL_FURN, 8,  2.55, 13.68, Z_P2_FLOOR,        2.70, 14.47, Z_P2_FLOOR + 0.70) # Base hierro oeste
    add_house_box(L_SOCIAL_FURN, 8,  4.10, 13.68, Z_P2_FLOOR,        4.25, 14.47, Z_P2_FLOOR + 0.70) # Base hierro este
    add_house_box(L_SOCIAL_FURN, 34, 2.30, 13.55, Z_P2_FLOOR + 0.70, 4.50, 14.60, Z_P2_FLOOR + 0.77) # Tablón comedor 2,20x1,05m
    for ch_x in [2.52, 3.18, 3.84]:
        # 3 sillas sur + 3 sillas norte
        add_house_box(L_SOCIAL_FURN, 30, ch_x, 13.10, Z_P2_FLOOR,        ch_x + 0.44, 13.52, Z_P2_FLOOR + 0.46)
        add_house_box(L_SOCIAL_FURN, 34, ch_x, 13.10, Z_P2_FLOOR + 0.46, ch_x + 0.44, 13.18, Z_P2_FLOOR + 0.90)
        add_house_box(L_SOCIAL_FURN, 30, ch_x, 14.63, Z_P2_FLOOR,        ch_x + 0.44, 15.05, Z_P2_FLOOR + 0.46)
        add_house_box(L_SOCIAL_FURN, 34, ch_x, 14.97, Z_P2_FLOOR + 0.46, ch_x + 0.44, 15.05, Z_P2_FLOOR + 0.90)
    # 2 sillas cabeceras de honor (Oeste y Este)
    add_house_box(L_SOCIAL_FURN, 30, 1.84, 13.84, Z_P2_FLOOR,        2.26, 14.31, Z_P2_FLOOR + 0.46)
    add_house_box(L_SOCIAL_FURN, 34, 1.84, 13.84, Z_P2_FLOOR + 0.46, 1.92, 14.31, Z_P2_FLOOR + 0.92)
    add_house_box(L_SOCIAL_FURN, 30, 4.54, 13.84, Z_P2_FLOOR,        4.96, 14.31, Z_P2_FLOOR + 0.46)
    add_house_box(L_SOCIAL_FURN, 34, 4.88, 13.84, Z_P2_FLOOR + 0.46, 4.96, 14.31, Z_P2_FLOOR + 0.92)
    # Lámpara lineal de viga rústica sobre comedor + Buffet / Vinera en muro oeste (X: 0.30..0.78, Y: 13.65..15.45)
    add_house_box(L_SOCIAL_FURN, 34, 2.65, 14.01, Z_P2_FLOOR + 1.88, 4.15, 14.14, Z_P2_FLOOR + 1.98)
    add_house_box(L_SOCIAL_FURN, 34, 0.30, 13.65, Z_P2_FLOOR,        0.78, 15.45, Z_P2_FLOOR + 0.88)
    add_house_box(L_SOCIAL_FURN, 30, 0.30, 13.85, Z_P2_FLOOR + 1.25, 0.58, 15.25, Z_P2_FLOOR + 2.10) # Vinera mural

    # C) GRAN SALA CHALET (Y: 16.10..19.42) + BALCONADA SOCIAL AMOBLADA (Y: 19.60..21.56)
    #    1. Sofá en L bajo ventanal panorámico (altura 0,82 m < antepecho 0,85 m) + Mesa Tronco + Pared TV 75"
    add_house_box(L_SOCIAL_FURN, 30, 3.05, 16.25, Z_P2_FLOOR,        5.45, 19.20, Z_P2_FLOOR + 0.02) # Gran alfombra sala
    add_house_box(L_SOCIAL_FURN, 7,  3.05, 18.52, Z_P2_FLOOR + 0.02, 5.15, 19.40, Z_P2_FLOOR + 0.42) # Sofá L tramo norte
    add_house_box(L_SOCIAL_FURN, 30, 3.05, 19.22, Z_P2_FLOOR + 0.42, 5.15, 19.40, Z_P2_FLOOR + 0.82) # Respaldo norte sofá
    add_house_box(L_SOCIAL_FURN, 7,  3.05, 16.52, Z_P2_FLOOR + 0.02, 3.92, 18.52, Z_P2_FLOOR + 0.42) # Sofá L tramo oeste
    add_house_box(L_SOCIAL_FURN, 30, 3.05, 16.52, Z_P2_FLOOR + 0.42, 3.23, 19.22, Z_P2_FLOOR + 0.82) # Respaldo oeste sofá
    add_house_box(L_SOCIAL_FURN, 34, 4.18, 17.05, Z_P2_FLOOR + 0.02, 4.88, 18.15, Z_P2_FLOOR + 0.40) # Mesa centro maciza
    add_house_box(L_SOCIAL_FURN, 8,  5.72, 16.30, Z_P2_FLOOR,        5.80, 18.75, Z_P2_FLOOR + 2.25) # Panel piedra laja TV
    add_house_box(L_SOCIAL_FURN, 34, 5.35, 16.25, Z_P2_FLOOR,        5.80, 18.80, Z_P2_FLOOR + 0.52) # Consola baja TV
    add_house_box(L_SOCIAL_FURN, 8,  5.66, 16.68, Z_P2_FLOOR + 0.82, 5.71, 18.36, Z_P2_FLOOR + 1.78) # Smart TV 75"
    #    2. Dos poltronas de cuero en crujía oeste + mesita auxiliar (dejando libre el corredor al balcón X: 1.32..2.65)
    add_house_box(L_SOCIAL_FURN, 30, 0.48, 16.55, Z_P2_FLOOR,        1.24, 17.30, Z_P2_FLOOR + 0.42)
    add_house_box(L_SOCIAL_FURN, 34, 0.48, 16.55, Z_P2_FLOOR + 0.42, 0.64, 17.30, Z_P2_FLOOR + 0.82)
    add_house_box(L_SOCIAL_FURN, 34, 0.62, 17.38, Z_P2_FLOOR,        1.06, 17.62, Z_P2_FLOOR + 0.48) # Mesita auxiliar
    add_house_box(L_SOCIAL_FURN, 30, 0.48, 17.70, Z_P2_FLOOR,        1.24, 18.45, Z_P2_FLOOR + 0.42)
    add_house_box(L_SOCIAL_FURN, 34, 0.48, 17.70, Z_P2_FLOOR + 0.42, 0.64, 18.45, Z_P2_FLOOR + 0.82)
    #    3. Mobiliario Exterior en Gran Balconada Social (Sofá terraza oeste + Comedor mirador 4p este)
    add_house_box(L_SOCIAL_FURN, 34, 0.48, 20.05, Z_P2_FLOOR,        1.22, 21.25, Z_P2_FLOOR + 0.40) # Sofá exterior oeste
    add_house_box(L_SOCIAL_FURN, 30, 0.48, 20.05, Z_P2_FLOOR + 0.40, 0.62, 21.25, Z_P2_FLOOR + 0.78)
    add_house_box(L_SOCIAL_FURN, 34, 1.38, 20.40, Z_P2_FLOOR,        1.80, 20.90, Z_P2_FLOOR + 0.42) # Mesa café terraza
    add_house_box(L_SOCIAL_FURN, 34, 3.85, 20.30, Z_P2_FLOOR,        5.15, 21.00, Z_P2_FLOOR + 0.74) # Mesa mirador 4p
    add_house_box(L_SOCIAL_FURN, 30, 3.95, 19.90, Z_P2_FLOOR,        5.05, 20.22, Z_P2_FLOOR + 0.45) # Banca sur mirador
    add_house_box(L_SOCIAL_FURN, 30, 3.95, 21.08, Z_P2_FLOOR,        5.05, 21.40, Z_P2_FLOOR + 0.45) # Banca norte mirador

    # 8. OPCIÓN A: DESPENSA WALK-IN DE COCINA + CLÓSET DE BLANCOS (X: 0.30..1.55, Y: 4.40..7.35)
    # Tabique longitudinal plomado sobre el muro existente de P1 (X: 1.40..1.55, sin tocar los 1.10 m de escalera)
    add_house_box(L_P2_INT, 6, 1.40, 4.40, Z_P2_FLOOR, 1.55, 7.35, H_P2)
    # Tabique transversal divisorio entre Despensa Walk-In (Norte) y Clóset de Blancos (Sur)
    add_house_box(L_P2_INT, 6, 0.30, 5.65, Z_P2_FLOOR, 1.40, 5.80, H_P2)

    # A) Muro Sur de Cocina (Y: 7.35..7.50) con Puerta Rústica Abierta hacia el Interior de la Despensa (libera muro de Nevera)
    add_wall_with_openings_x(L_P2_INT, 6, 0.30, 2.75, 7.35, 7.50, Z_P2_FLOOR, H_P2, [
        (0.50, 1.30, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    add_house_box(L_CARP, 30, 1.32, 6.55, Z_P2_FLOOR + 0.02, 1.38, 7.35, Z_P2_FLOOR + H_DOOR)        # Hoja abierta al interior
    # 4 niveles de estanterías de madera en L dentro de la Despensa Walk-In (librando Columna 0-F en Y: 6.45..6.70)
    for sh_z in [3.60, 4.10, 4.60, 5.10]:
        add_house_box(L_TIMBER, 34, 0.41, 5.80, sh_z, 0.66, 7.33, sh_z + 0.04)
        add_house_box(L_TIMBER, 34, 0.66, 5.80, sh_z, 1.38, 6.10, sh_z + 0.04)

    # B) Muro Sur del Clóset de Blancos (Y: 4.40..4.55) con Puerta Doble (X: 0.45..1.25) hacia el Nuevo Vestíbulo
    add_wall_with_openings_x(L_P2_INT, 6, 0.30, 1.55, 4.40, 4.55, Z_P2_FLOOR, H_P2, [
        (0.45, 1.25, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),
    ])
    # 4 repisas profundas de madera para lencería dentro del Clóset de Blancos
    for lb_z in [3.55, 4.05, 4.55, 5.05]:
        add_house_box(L_TIMBER, 34, 0.32, 5.23, lb_z, 1.38, 5.65, lb_z + 0.04)

    # 9. NUEVO VESTÍBULO EN EJE G (Y: 3.60..4.61) + PORTAL PLANO DE 0,91 m SIN DESNIVELES (Y: 3.70..4.61)
    # Poste maestro (Newel Post) en Y = 4.61..4.75 justo donde inician los peldaños en bajada + Baranda Oriental
    add_house_box(L_TIMBER, 34, 2.68, 4.61, Z_P2_FLOOR, 2.84, 4.75, Z_P2_FLOOR + 1.12)
    add_alpine_railing_y(2.75, 4.75, 6.43, Z_P2_FLOOR, h_rail=1.05, n_bays=2)
    add_alpine_railing_y(2.75, 6.72, 7.35, Z_P2_FLOOR, h_rail=1.05, n_bays=1)
    # Viga Dintel Timber Frame sobre el Portal Abierto (X: 2.72..2.92, Y: 3.72..4.40, Z: 5.25..5.50 -> paso libre 2,25 m)
    add_house_box(L_TIMBER, 34, 2.72, 3.72, 5.25, 2.92, 4.40, Z_LAV_CEIL)

    # 10. Lavandería Rústica alineada al Eje Estructural G (X: 0.30..2.75, Y: 0.15..3.45 = 8,09 m²) y Mirador Sur
    add_wall_with_openings_x(L_P2_INT, 6, 0.40, 2.70, 3.45, 3.60, Z_P2_FLOOR, Z_LAV_CEIL, [
        (1.65, 2.45, Z_P2_FLOOR, Z_P2_FLOOR + H_DOOR),          # Puerta Lavandería conectada al Nuevo Vestíbulo
    ])
    add_house_box(L_P2_INT, 6, 2.75, 0.25, Z_P2_FLOOR, 2.90, 3.45, Z_LAV_CEIL)
    add_wall_with_openings_x(L_P2_INT, 6, 2.90, 5.85, 3.50, 3.65, Z_P2_FLOOR, H_P2, [
        (3.40, 5.30, Z_P2_FLOOR, Z_P2_FLOOR + 2.40),          # Gran pórtico abierto al Estar/Mirador Sur
    ])

    # =========================================================================
    # 3B. CUARTO HIDRONEUMÁTICO / BUHARDILLA CHALET PARA TANQUE DE 1.000 L
    #     (ENCIMA DE LA LAVANDERÍA Y VESTÍBULO: X = 0.15..2.90 m, Y = 0.00..4.40 m, Z = +5.68 m)
    # =========================================================================
    L_TANK_SLAB = "P2_LOSA_TANQUE_3D"
    L_MAINT_ST  = "P2_ESCALERA_MANTENIMIENTO_3D"
    L_HYDRO     = "EQUIPO_HIDRONEUMATICO_3D"
    L_DORMER    = "BUHARDILLA_TECNICA_3D"

    Z_TANK_FLOOR = 5.68   # Losa técnica portante de 18 cm (Z: 5.50 a 5.68 m)
    # Losa portante con Escotilla desplazada a Lavandería (X: 0.38..1.18, Y: 2.05..3.30 -> 0,80 x 1,25 m)
    add_house_box(L_TANK_SLAB, 8, 0.30, 0.00, Z_LAV_CEIL, 2.90, 2.05, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 0.30, 3.30, Z_LAV_CEIL, 2.90, 4.40, Z_TANK_FLOOR)  # Plataforma desembarque norte (0,95x2,45m)
    add_house_box(L_TANK_SLAB, 8, 0.30, 2.05, Z_LAV_CEIL, 0.38, 3.30, Z_TANK_FLOOR)
    add_house_box(L_TANK_SLAB, 8, 1.18, 2.05, Z_LAV_CEIL, 2.90, 3.30, Z_TANK_FLOOR)

    # Pedestal macizo de concreto para el Tanque de 1.000 L (1,30 x 1,30 x 0,12 m) y Bancada Hidroneumática
    TANK_CX, TANK_CY = 1.60, 1.15
    add_house_box(L_TANK_SLAB, 8, TANK_CX - 0.65, TANK_CY - 0.65, Z_TANK_FLOOR,
                                  TANK_CX + 0.65, TANK_CY + 0.65, Z_TANK_FLOOR + 0.12)
    add_house_box(L_TANK_SLAB, 8, 1.85, 2.15, Z_TANK_FLOOR, 2.70, 3.25, Z_TANK_FLOOR + 0.10)

    # Escalera Fija Inclinada (68°) subiendo de Sur a Norte: desde Lavandería (Y=2.11, Z=3.00) hacia Plataforma Norte (Y=3.23, Z=5.68)
    for sx1, sx2 in [(0.40, 0.45), (1.05, 1.10)]:
        add_house_hexa(L_MAINT_ST, 30, [
            (sx1, 2.06, Z_P2_FLOOR),   (sx2, 2.06, Z_P2_FLOOR),
            (sx2, 2.16, Z_P2_FLOOR),   (sx1, 2.16, Z_P2_FLOOR),
            (sx1, 3.18, Z_TANK_FLOOR), (sx2, 3.18, Z_TANK_FLOOR),
            (sx2, 3.28, Z_TANK_FLOOR), (sx1, 3.28, Z_TANK_FLOOR),
        ])
        # Pasamanos inclinados + prolongación vertical de seguridad (+1.00 m sobre Z_TANK_FLOOR en el desembarque norte)
        add_house_hexa(L_MAINT_ST, 30, [
            (sx1, 2.25, Z_P2_FLOOR + 0.85),   (sx2, 2.25, Z_P2_FLOOR + 0.85),
            (sx2, 2.31, Z_P2_FLOOR + 0.85),   (sx1, 2.31, Z_P2_FLOOR + 0.85),
            (sx1, 3.22, Z_TANK_FLOOR + 1.00), (sx2, 3.22, Z_TANK_FLOOR + 1.00),
            (sx2, 3.28, Z_TANK_FLOOR + 1.00), (sx1, 3.28, Z_TANK_FLOOR + 1.00),
        ])
        add_house_box(L_MAINT_ST, 30, sx1, 3.24, Z_TANK_FLOOR, sx2, 3.30, Z_TANK_FLOOR + 1.00)

    # 9 Peldaños planos antideslizantes de 18 cm de huella (ancho útil 60 cm, ascenso Sur -> Norte)
    num_m_steps = 9
    for ms in range(1, num_m_steps + 1):
        frac = ms / (num_m_steps + 1)
        ym_c = 2.11 + frac * (3.23 - 2.11)
        zm_c = Z_P2_FLOOR + frac * (Z_TANK_FLOOR - Z_P2_FLOOR)
        add_house_box(L_MAINT_ST, 30, 0.45, ym_c - 0.09, zm_c - 0.04, 1.05, ym_c + 0.09, zm_c)

    # Baranda Guarda-Escotilla de 1.00 m en el Cuarto Técnico (protege lados Este y Sur; lado Norte abierto al desembarque)
    add_alpine_railing_y(1.21, 2.02, 3.30, Z_TANK_FLOOR, h_rail=1.00, n_bays=2)
    add_alpine_railing_x(0.38, 1.21, 2.02, Z_TANK_FLOOR, h_rail=1.00, n_bays=1)

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
        ("SOTANO: Cava de Vinos y Cata Alpina (4,25 x 2,80m)", 1.95, 7.15, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Maletero Bajo Escalera", 0.35, 7.50, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Vestibulo Escalera", 1.70, 4.30, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Salon Lounge & Cine 85\" (2,95 x 4,40m)", 6.15, 7.15, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Taberna Social & Barra Humeda (4,25 x 3,45m)", 5.35, 2.20, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Suite de Huespedes (2,50 x 3,30m)", 0.42, 1.75, Z_SOT_FLOOR + 0.05),
        ("SOTANO: Bano Completo Rustico en Piedra (1,60 x 3,30m)", 3.00, 1.85, Z_SOT_FLOOR + 0.05),
        ("PATIO TRASERO: Pergola Rustica & Terraza de Laja (4,20 x 2,20m)", 4.95, -1.55, Z_SOT_FLOOR + 0.05),
    ]
    for txt, rx, ry, rz in sot_labels:
        add_house_text("SOTANO_ROTULOS", 4, txt, rx, ry, rz, 0.16)

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
        ("P2: Despensa Walk-In (1,10 x 1,55m)", 0.36, 6.45, Z_P2_FLOOR + 0.05),
        ("P2: Closet Blancos (1,10 x 1,10m)", 0.36, 4.95, Z_P2_FLOOR + 0.05),
        ("P2: Vestibulo Eje G + Portal 0,91m", 0.55, 3.95, Z_P2_FLOOR + 0.05),
        ("P2: Lavanderia + Subida Tanque (2,45 x 3,30m)", 0.45, 1.50, Z_P2_FLOOR + 0.05),
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
    add_text(L_SOT_2D, 2, "PLANTA SOTANO CHALET: CAVA, TABERNA, SUITE HUESPEDES Y PERGOLA", SX - 0.1, SY - 2.95, 0.0, 0.25)
    add_rect_2d(L_SOT_2D, 8, SX + 0.00, SY - 2.65, SX + 0.15, SY + 8.30)   # Medianera Vecino Izquierdo (Cero Invasión)
    add_rect_2d(L_SOT_2D, 7, SX + 0.15, SY + 0.00, SX + 9.15, SY + 8.30)   # Perímetro Sótano Rectangular (9,00 x 8,30m)
    # Particiones interiores rediseñadas (Opción A)
    add_rect_2d(L_SOT_2D, 4, SX + 0.30, SY + 0.15, SX + 2.80, SY + 3.45)   # Suite de Huéspedes (2,50 x 3,30m)
    add_rect_2d(L_SOT_2D, 4, SX + 2.95, SY + 0.15, SX + 4.55, SY + 3.45)   # Baño Completo Rústico (1,60 x 3,30m)
    add_rect_2d(L_SOT_2D, 34, SX + 1.55, SY + 5.31, SX + 5.92, SY + 8.07)  # Cava de Vinos (Vitrina Hierro/Vidrio)
    add_line(L_SOT_2D, 4, SX + 1.47, SY + 4.45, 0.0, SX + 1.47, SY + 8.15, 0.0)  # Cierre Escalera + Maletero
    # Indicación de Puertas interiores y Doble Puerta Francesa al Jardín (2,20 m)
    add_line(L_SOT_2D, 34, SX + 1.78, SY + 3.52, 0.0, SX + 2.58, SY + 3.52, 0.0) # Puerta Suite Huéspedes
    add_line(L_SOT_2D, 34, SX + 3.62, SY + 3.52, 0.0, SX + 4.42, SY + 3.52, 0.0) # Puerta Baño Rústico
    add_line(L_SOT_2D, 34, SX + 3.25, SY + 5.31, 0.0, SX + 4.45, SY + 5.31, 0.0) # Puerta Doble Vitrina Cava
    add_line(L_SOT_2D, 34, SX + 1.47, SY + 7.22, 0.0, SX + 1.47, SY + 7.94, 0.0) # Puerta Maletero Bajo Escalera
    add_line(L_SOT_2D, 1,  SX + 6.35, SY - 0.08, 0.0, SX + 8.55, SY - 0.08, 0.0) # Doble Puerta Francesa 2,20m
    # Escalera intacta + Estantería Maletero
    for i in range(13):
        yy = SY + 4.45 + i * ((7.40 - 4.45) / 12.0)
        add_line(L_SOT_2D, 3, SX + 0.30, yy, 0.0, SX + 1.40, yy, 0.0)
    add_rect_2d(L_SOT_2D, 34, SX + 0.32, SY + 7.78, SX + 1.38, SY + 8.13)  # Estantes Maletero
    # Columnas Sótano intactas en 2D
    add_rect_2d(L_SOT_2D, 1, SX + 0.15, SY + 6.35, SX + 0.30, SY + 6.80)
    for cx_s, cy_s in sot_cols_axes:
        add_rect_2d(L_SOT_2D, 1, SX + cx_s - 0.175, SY + cy_s - 0.175, SX + cx_s + 0.175, SY + cy_s + 0.175)
    # Mobiliario 2D Cava de Vinos
    add_rect_2d(L_SOT_2D, 34, SX + 2.15, SY + 7.72, SX + 5.78, SY + 8.07)  # Botellero Roble Norte
    add_rect_2d(L_SOT_2D, 34, SX + 1.56, SY + 5.42, SX + 1.92, SY + 7.05)  # Botellero Roble Oeste
    add_rect_2d(L_SOT_2D, 30, SX + 3.75, SY + 6.22, SX + 4.95, SY + 6.92)  # Mesa Alta de Cata / Barrica
    for ts_x in [3.92, 4.48]:
        add_rect_2d(L_SOT_2D, 30, SX + ts_x, SY + 5.84, SX + ts_x + 0.30, SY + 6.14)
        add_rect_2d(L_SOT_2D, 30, SX + ts_x, SY + 7.00, SX + ts_x + 0.30, SY + 7.30)
    # Mobiliario 2D Salón Lounge & Cine 85" + Barra Húmeda + Comedor/Juegos Taberna 6p
    add_rect_2d(L_SOT_2D, 34, SX + 6.35, SY + 7.62, SX + 8.55, SY + 8.05)  # Mueble + TV Cine 85"
    add_rect_2d(L_SOT_2D, 30, SX + 6.22, SY + 4.82, SX + 8.75, SY + 5.72)  # Sofá L Lounge (tramo Sur)
    add_rect_2d(L_SOT_2D, 30, SX + 7.88, SY + 5.72, SX + 8.75, SY + 6.90)  # Sofá L Lounge (chaise Este)
    add_rect_2d(L_SOT_2D, 34, SX + 6.65, SY + 6.02, SX + 7.55, SY + 6.65)  # Mesa Centro Tronco
    add_rect_2d(L_SOT_2D, 3,  SX + 4.70, SY + 1.15, SX + 5.32, SY + 3.35)  # Barra Húmeda (Sink + Vinera)
    add_rect_2d(L_SOT_2D, 34, SX + 7.05, SY + 1.25, SX + 8.00, SY + 3.05)  # Mesa Taberna / Juegos 6p
    for ty_ch in [1.48, 2.34]:
        add_rect_2d(L_SOT_2D, 30, SX + 6.60, SY + ty_ch, SX + 7.00, SY + ty_ch + 0.44)
        add_rect_2d(L_SOT_2D, 30, SX + 8.05, SY + ty_ch, SX + 8.45, SY + ty_ch + 0.44)
    add_rect_2d(L_SOT_2D, 30, SX + 7.30, SY + 0.80, SX + 7.75, SY + 1.20)
    add_rect_2d(L_SOT_2D, 30, SX + 7.30, SY + 3.10, SX + 7.75, SY + 3.48)
    # Mobiliario 2D Suite de Huéspedes + Baño Completo en Piedra
    add_rect_2d(L_SOT_2D, 30, SX + 0.34, SY + 0.95, SX + 2.22, SY + 2.35)  # Cama Doble + Cabecero
    add_rect_2d(L_SOT_2D, 34, SX + 0.34, SY + 0.45, SX + 0.72, SY + 0.86)  # Mesa noche Sur
    add_rect_2d(L_SOT_2D, 34, SX + 0.34, SY + 2.44, SX + 0.72, SY + 2.85)  # Mesa noche Norte
    add_rect_2d(L_SOT_2D, 34, SX + 0.52, SY + 2.92, SX + 1.66, SY + 3.43)  # Clóset Rústico Huéspedes
    add_rect_2d(L_SOT_2D, 8,  SX + 2.96, SY + 0.16, SX + 4.54, SY + 1.05)  # Ducha Walk-In Pizarra
    add_rect_2d(L_SOT_2D, 8,  SX + 4.14, SY + 0.17, SX + 4.53, SY + 0.98)  # Banco Piedra Ducha
    add_rect_2d(L_SOT_2D, 7,  SX + 2.98, SY + 1.32, SX + 3.64, SY + 1.72)  # WC
    add_rect_2d(L_SOT_2D, 3,  SX + 2.98, SY + 2.02, SX + 3.50, SY + 2.96)  # Tocador + Lavamanos Piedra
    # Terraza de Piedra Laja + Pérgola Rústica en Patio Trasero (SY - 2.20..SY + 0.00)
    add_rect_2d(L_SOT_2D, 8,  SX + 4.85, SY - 2.20, SX + 9.05, SY + 0.00)  # Solado Piedra Laja
    for pg_x in [4.95, 6.91, 8.82]:
        add_rect_2d(L_SOT_2D, 34, SX + pg_x - 0.04, SY - 2.14, SX + pg_x + 0.22, SY - 1.88)
    add_rect_2d(L_SOT_2D, 34, SX + 5.05, SY - 2.02, SX + 6.22, SY - 1.32)  # Sofá Jardín bajo Pérgola
    add_rect_2d(L_SOT_2D, 8,  SX + 5.35, SY - 1.16, SX + 6.05, SY - 0.68)  # Mesa Piedra Jardín
    add_rect_2d(L_SOT_2D, 34, SX + 8.18, SY - 1.96, SX + 8.84, SY - 1.30)  # Poltrona Jardín Este
    add_rect_2d(L_SOT_2D, 3,  SX + 0.65, SY - 0.52, SX + 2.45, SY - 0.04)  # Jardinera Piedra Sur
    # Textos 2D Sótano Chalet
    add_text(L_SOT_2D, 2, "Cava Vinos + Cata", SX + 2.05, SY + 6.52, 0.0, 0.16)
    add_text(L_SOT_2D, 2, "Maletero", SX + 0.36, SY + 7.50, 0.0, 0.12)
    add_text(L_SOT_2D, 2, "Vestibulo", SX + 1.85, SY + 4.30, 0.0, 0.15)
    add_text(L_SOT_2D, 2, "Lounge & Cine 85\"", SX + 6.18, SY + 7.22, 0.0, 0.15)
    add_text(L_SOT_2D, 2, "Wet Bar", SX + 4.74, SY + 3.48, 0.0, 0.13)
    add_text(L_SOT_2D, 2, "Taberna / Juegos", SX + 5.45, SY + 2.10, 0.0, 0.14)
    add_text(L_SOT_2D, 2, "Suite Huespedes", SX + 0.55, SY + 1.60, 0.0, 0.15)
    add_text(L_SOT_2D, 2, "Bano Piedra", SX + 3.08, SY + 3.08, 0.0, 0.13)
    add_text(L_SOT_2D, 1, "Puerta Francesa 2,20m", SX + 6.38, SY - 0.38, 0.0, 0.13)
    add_text(L_SOT_2D, 30, "Pergola + Terraza Laja (4,20x2,20m)", SX + 5.15, SY - 2.48, 0.0, 0.14)

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
    # Mobiliario 2D Master Suite (Terraza + Cama/Cabecero + Vestier + Baño Spa)
    add_rect_2d(L_P2_2D, 34, P2X + 6.12, P2Y + 20.45, P2X + 6.82, P2Y + 21.15)  # Poltrona 1 Terraza
    add_rect_2d(L_P2_2D, 34, P2X + 6.95, P2Y + 20.60, P2X + 7.40, P2Y + 21.05)  # Mesa Tronco
    add_rect_2d(L_P2_2D, 34, P2X + 7.52, P2Y + 20.55, P2X + 8.22, P2Y + 21.25)  # Poltrona 2 Terraza
    add_rect_2d(L_P2_2D, 3,  P2X + 8.38, P2Y + 20.68, P2X + 8.92, P2Y + 21.38)  # Jardinera Aromática
    add_rect_2d(L_P2_2D, 30, P2X + 6.14, P2Y + 16.75, P2X + 8.03, P2Y + 18.45)  # Cama Master + Cabecero
    add_rect_2d(L_P2_2D, 34, P2X + 6.14, P2Y + 16.14, P2X + 6.60, P2Y + 16.68)  # Mesa de noche Sur
    add_rect_2d(L_P2_2D, 34, P2X + 6.14, P2Y + 18.52, P2X + 6.60, P2Y + 19.06)  # Mesa de noche Norte
    add_rect_2d(L_P2_2D, 34, P2X + 8.50, P2Y + 18.28, P2X + 8.94, P2Y + 19.32)  # Consola Baja TV
    add_rect_2d(L_P2_2D, 34, P2X + 6.05, P2Y + 12.65, P2X + 6.60, P2Y + 14.75)  # Clóset Oeste Vestier
    add_rect_2d(L_P2_2D, 34, P2X + 8.40, P2Y + 12.65, P2X + 8.95, P2Y + 14.75)  # Clóset Este Vestier
    add_rect_2d(L_P2_2D, 30, P2X + 7.20, P2Y + 13.33, P2X + 7.80, P2Y + 14.07)  # Pouf Central Vestier
    add_rect_2d(L_P2_2D, 3,  P2X + 6.05, P2Y + 10.30, P2X + 6.60, P2Y + 11.88)  # Tocador Doble Lavamanos
    add_rect_2d(L_P2_2D, 7,  P2X + 6.98, P2Y + 10.16, P2X + 7.42, P2Y + 10.78)  # WC Discreto
    add_rect_2d(L_P2_2D, 4,  P2X + 7.95, P2Y + 10.15, P2X + 8.95, P2Y + 12.45)  # Ducha Walk-In Spa
    add_rect_2d(L_P2_2D, 8,  P2X + 8.55, P2Y + 10.18, P2X + 8.94, P2Y + 11.65)  # Banco de Piedra Ducha
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 6.45,  P2X + 9.00, P2Y + 10.00)   # Habitación 2
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 4.45,  P2X + 9.00, P2Y + 6.30)    # Baño Familiar
    add_rect_2d(L_P2_2D, 6, P2X + 6.00, P2Y + 0.15,  P2X + 9.00, P2Y + 4.30)    # Habitación 3 Esquinera
    add_rect_2d(L_P2_2D, 6, P2X + 0.30, P2Y + 0.15,  P2X + 2.75, P2Y + 3.45)    # Lavandería alineada a Eje G
    add_rect_2d(L_P2_2D, 6, P2X + 0.30, P2Y + 5.80,  P2X + 1.40, P2Y + 7.35)    # Despensa Walk-In Cocina
    add_rect_2d(L_P2_2D, 6, P2X + 0.30, P2Y + 4.55,  P2X + 1.40, P2Y + 5.65)    # Clóset de Blancos / Lencería
    # Escalera P2 (X: 1.55..2.65, Y: 4.40..7.35) + Baranda solo en Y: 4.61..7.35 dejando Portal plano Y: 3.70..4.61
    for i in range(num_steps_p2 + 1):
        yy_p2 = P2Y + 7.35 - i * step_dy_p2
        add_line(L_P2_2D, 7, P2X + 1.55, yy_p2, 0.0, P2X + 2.65, yy_p2, 0.0)
    add_line(L_P2_2D, 30, P2X + 2.75, P2Y + 4.61, 0.0, P2X + 2.75, P2Y + 7.35, 0.0)
    add_line(L_P2_2D, 34, P2X + 0.50, P2Y + 7.42, 0.0, P2X + 1.30, P2Y + 7.42, 0.0)  # Puerta Granero Despensa
    add_line(L_P2_2D, 34, P2X + 0.45, P2Y + 4.47, 0.0, P2X + 1.25, P2Y + 4.47, 0.0)  # Puerta Clóset Blancos
    add_line(L_P2_2D, 34, P2X + 1.65, P2Y + 3.52, 0.0, P2X + 2.45, P2Y + 3.52, 0.0)  # Puerta Lavandería en Eje G
    add_rect_2d(L_P2_2D, 6, P2X + 2.90, P2Y + 0.15,  P2X + 5.85, P2Y + 3.50)    # Estar / Mirador Sur
    # Mobiliario 2D Cocina + Comedor 8p + Gran Sala Chalet + Balconada Social
    add_rect_2d(L_P2_2D, 3,  P2X + 2.10, P2Y + 9.55,  P2X + 3.12, P2Y + 12.15)  # Isla Central (+15 cm al Este)
    for b_y in [9.80, 10.38, 10.96, 11.54]:
        add_rect_2d(L_P2_2D, 30, P2X + 3.06, P2Y + b_y - 0.17, P2X + 3.42, P2Y + b_y + 0.17)  # 4 Taburetes Isla
    add_rect_2d(L_P2_2D, 3,  P2X + 0.30, P2Y + 8.35,  P2X + 0.96, P2Y + 13.20)  # Mesón Lineal Oeste
    add_rect_2d(L_P2_2D, 7,  P2X + 0.40, P2Y + 9.15,  P2X + 0.94, P2Y + 10.10)  # Fregadero Farmhouse Doble
    add_rect_2d(L_P2_2D, 8,  P2X + 0.38, P2Y + 11.00, P2X + 0.88, P2Y + 11.95)  # Cocina 5 Hornillas + Campana
    add_rect_2d(L_P2_2D, 5,  P2X + 1.46, P2Y + 7.52,  P2X + 2.32, P2Y + 8.30)   # Nevera Doble French Door
    add_rect_2d(L_P2_2D, 8,  P2X + 2.34, P2Y + 7.52,  P2X + 2.72, P2Y + 8.28)   # Torre Horno / Microondas
    add_rect_2d(L_P2_2D, 34, P2X + 0.30, P2Y + 13.65, P2X + 0.78, P2Y + 15.45)  # Buffet / Vinera
    add_rect_2d(L_P2_2D, 34, P2X + 2.30, P2Y + 13.55, P2X + 4.50, P2Y + 14.60)  # Mesa Comedor 8 Puestos
    for ch_x in [2.52, 3.18, 3.84]:
        add_rect_2d(L_P2_2D, 30, P2X + ch_x, P2Y + 13.12, P2X + ch_x + 0.44, P2Y + 13.50)
        add_rect_2d(L_P2_2D, 30, P2X + ch_x, P2Y + 14.65, P2X + ch_x + 0.44, P2Y + 15.03)
    add_rect_2d(L_P2_2D, 30, P2X + 1.84, P2Y + 13.84, P2X + 2.26, P2Y + 14.31)
    add_rect_2d(L_P2_2D, 30, P2X + 4.54, P2Y + 13.84, P2X + 4.96, P2Y + 14.31)
    add_rect_2d(L_P2_2D, 30, P2X + 3.05, P2Y + 18.52, P2X + 5.15, P2Y + 19.40)  # Sofá L Sala (tramo norte)
    add_rect_2d(L_P2_2D, 30, P2X + 3.05, P2Y + 16.52, P2X + 3.92, P2Y + 18.52)  # Sofá L Sala (tramo oeste)
    add_rect_2d(L_P2_2D, 34, P2X + 4.18, P2Y + 17.05, P2X + 4.88, P2Y + 18.15)  # Mesa Centro Sala
    add_rect_2d(L_P2_2D, 34, P2X + 5.35, P2Y + 16.25, P2X + 5.80, P2Y + 18.80)  # Mueble + Panel TV 75"
    add_rect_2d(L_P2_2D, 30, P2X + 0.48, P2Y + 16.55, P2X + 1.24, P2Y + 17.30)  # Poltrona Cuero 1
    add_rect_2d(L_P2_2D, 30, P2X + 0.48, P2Y + 17.70, P2X + 1.24, P2Y + 18.45)  # Poltrona Cuero 2
    add_rect_2d(L_P2_2D, 34, P2X + 0.48, P2Y + 20.05, P2X + 1.22, P2Y + 21.25)  # Sofá Terraza Social
    add_rect_2d(L_P2_2D, 34, P2X + 3.85, P2Y + 20.30, P2X + 5.15, P2Y + 21.00)  # Mesa Mirador Balconada
    for cx, cy in existing_and_new_cols:
        add_rect_2d(L_P2_2D, 1, P2X + cx - 0.125, P2Y + cy - 0.125, P2X + cx + 0.125, P2Y + cy + 0.125)
    add_text(L_P2_2D, 2, "Balconada Social (5,55x1,96)", P2X + 1.85, P2Y + 20.55, 0.0, 0.15)
    add_text(L_P2_2D, 2, "Terraza Suite (3,00x1,96)", P2X + 6.15, P2Y + 20.00, 0.0, 0.15)
    add_text(L_P2_2D, 2, "Gran Sala Chalet + TV 75\"", P2X + 3.12, P2Y + 16.20, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Comedor 8p", P2X + 2.85, P2Y + 14.00, 0.0, 0.16)
    add_text(L_P2_2D, 2, "Nevera+Hornos", P2X + 1.44, P2Y + 8.42, 0.0, 0.13)
    add_text(L_P2_2D, 2, "Cocina + Isla", P2X + 1.02, P2Y + 10.80, 0.0, 0.15)
    add_text(L_P2_2D, 2, "Master Suite (3,00x4,50)", P2X + 6.20, P2Y + 17.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Vestier Walk-In (3,00x2,20)", P2X + 6.20, P2Y + 13.60, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Bano Spa Master (3,00x2,30)", P2X + 6.20, P2Y + 11.20, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Habitacion 2 (3,00x3,55)", P2X + 6.20, P2Y + 8.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Bano Familiar (3,00x1,85)", P2X + 6.20, P2Y + 5.25, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Hab. 3 Nueva (3,00x4,15)", P2X + 6.20, P2Y + 2.10, 0.0, 0.18)
    add_text(L_P2_2D, 2, "Mirador Sur", P2X + 3.40, P2Y + 1.80, 0.0, 0.17)
    add_text(L_P2_2D, 2, "Despensa", P2X + 0.36, P2Y + 6.48, 0.0, 0.13)
    add_text(L_P2_2D, 2, "Blancos", P2X + 0.40, P2Y + 5.02, 0.0, 0.13)
    add_text(L_P2_2D, 3, "Vestibulo / Portal 0,91m", P2X + 0.50, P2Y + 3.95, 0.0, 0.13)
    add_text(L_P2_2D, 2, "Lavanderia", P2X + 1.35, P2Y + 1.40, 0.0, 0.16)
    # Indicación en planta P2 de Escalera Fija (Sur->Norte) y Escotilla hacia Tanque 1.000 L
    add_rect_2d(L_P2_2D, 30, P2X + 0.38, P2Y + 2.05, P2X + 1.18, P2Y + 3.30)
    for ms in range(1, num_m_steps + 1):
        ym_2d = P2Y + 2.11 + (ms / (num_m_steps + 1)) * (3.23 - 2.11)
        add_line(L_P2_2D, 30, P2X + 0.45, ym_2d, 0.0, P2X + 1.05, ym_2d, 0.0)
    add_text(L_P2_2D, 30, "Subida Tanque", P2X + 1.24, P2Y + 2.60, 0.0, 0.13)

    # Planta Detalle 2D del Cuarto Hidroneumático / Buhardilla Técnica (Z = +5,68 m)
    TX = 30.00
    TY = 13.00
    L_TANK_2D = "PLANTA_TANQUE_1000L_2D"
    add_text(L_TANK_2D, 5, "PLANTA BUHARDILLA TECNICA TANQUE 1.000L (Z = +5,68m)", TX - 0.2, TY - 1.35, 0.0, 0.25)
    add_rect_2d(L_TANK_2D, 8,  TX + 0.00, TY + 0.00, TX + 0.15, TY + 4.45)  # Medianera Vecino Izquierdo (Cero Invasión)
    add_rect_2d(L_TANK_2D, 34, TX + 0.15, TY + 0.00, TX + 2.90, TY + 4.45)  # Envolvente Exterior Buhardilla
    add_rect_2d(L_TANK_2D, 6,  TX + 0.30, TY + 0.15, TX + 2.75, TY + 4.25)  # Espacio Libre Interior (2,45 x 4,10 m)
    add_rect_2d(L_TANK_2D, 9,  TX + 0.40, TY - 1.00, TX + X_DORM_JOIN, TY + 4.45)  # Proyección Cubierta Buhardilla
    # Escotilla de acceso (0,80 x 1,25 m en Y: 2.05..3.30) + Peldaños Sur->Norte + Baranda Guarda-Escotilla (1,00 m)
    add_rect_2d(L_TANK_2D, 30, TX + 0.38, TY + 2.05, TX + 1.18, TY + 3.30)
    for ms in range(1, num_m_steps + 1):
        ym_t = TY + 2.11 + (ms / (num_m_steps + 1)) * (3.23 - 2.11)
        add_line(L_TANK_2D, 30, TX + 0.45, ym_t, 0.0, TX + 1.05, ym_t, 0.0)
    add_line(L_TANK_2D, 1, TX + 1.21, TY + 2.02, 0.0, TX + 1.21, TY + 3.30, 0.0)
    add_line(L_TANK_2D, 1, TX + 0.38, TY + 2.02, 0.0, TX + 1.21, TY + 2.02, 0.0)
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
    add_text(L_TANK_2D, 3, "Desembarque Norte (2,45x0,95m)", TX + 0.38, TY + 3.70, 0.0, 0.12)
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
        (L_SOT_TIMBER, 34),
        (L_SOT_FURN, 30),
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
        (L_SUITE_FURN, 30),
        (L_SOCIAL_FURN, 30),
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
