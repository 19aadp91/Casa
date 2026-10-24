"""
Generador del PDF Arquitectónico Oficial del Proyecto Villa Mediterránea
("planos_casa_mediterranea.pdf")
Diseño bajo la Skill de Arquitecto Especialista en Estilo Mediterráneo para CAD.
Basado estrictamente en las dimensiones y columnas de casa_modificaciones.dxf.

Contenido de las 5 Láminas (Formato Tabloid 11x17 in):
- Lámina 1: Plano Planta Arquitectónica Distribución - Planta Baja (Zona Comercial y Garaje) y Sótano
- Lámina 2: Plano Planta Arquitectónica Distribución - Planta Alta Villa Mediterránea (Loggia con 3 Arcos, Pérgolas, Salón, Cocina Ibérica y Suites)
- Lámina 3: Plano Estructural y de Azotea Solárium Transitable (Retícula de 31 Columnas, Viguería de Pérgolas y Antepecho Encalado)
- Lámina 4: Plano Fachadas y Elevaciones Mediterráneas (Principal con Arcos de Medio Punto, Lateral con Talud, Posterior)
- Lámina 5: Levantamiento Poligonal de Linderos, Retícula UTM y Cuadro Normativo de Áreas
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch, PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages

# =============================================================================
# ESTILOS Y COLORES ARQUITECTÓNICOS MEDITERRÁNEOS
# =============================================================================
COLOR_BORDER = '#0000FF'       # Azul normativo de márgenes y recuadros de cajetín
COLOR_HEADER_RED = '#E00000'   # Rojo institucional y títulos de lámina
COLOR_CAJETIN_RED = '#E00000'  # Rojo datos técnicos (Nombre, Ubicación, CI)
COLOR_TEXT_BLACK = '#000000'   # Negro textos de dibujo y cotas
COLOR_WHITE_WALL = '#FAFAFA'   # Blanco puro encalado / estuco
COLOR_WALL_FILL = '#ECEFF1'    # Fondo de muro para contraste técnico
COLOR_WALL_LINE = '#000000'    # Contorno negro muros
COLOR_DOOR = '#3E2723'         # Carpintería puertas madera / forja
COLOR_WINDOW = '#0277BD'       # Vidrio y carpintería azul mediterráneo
COLOR_ARCH = '#00838F'         # Arquería y loggia
COLOR_STAIRS = '#455A64'       # Escaleras
COLOR_COL_RED = '#D32F2F'      # Columnas estructurales
COLOR_PERGOLA = '#6D4C41'      # Viguería de madera de pérgolas (Sombra y cañizo)
COLOR_AXIS_CYAN = '#00838F'    # Líneas de ejes estructurales
COLOR_TERRAIN = '#795548'      # Talud y perfil natural de terreno
COLOR_TERRACOTTA = '#D84315'   # Terracota / teja tradicional
COLOR_SOLARIUM = '#FFF8E1'     # Pavimento cálido de azotea solárium

def draw_sheet_frame(fig, ax_frame, title_line1, title_line2="", escala="1:75", fecha="OCT 2026", is_landscape=False):
    """Dibuja el marco perimetral azul y el cajetín municipal reglamentario."""
    ax_frame.set_xlim(0, 1)
    ax_frame.set_ylim(0, 1)
    ax_frame.axis('off')

    # Marco exterior e interior en azul
    rect_out = Rectangle((0.015, 0.012), 0.970, 0.976, fill=False, edgecolor=COLOR_BORDER, linewidth=2.0)
    ax_frame.add_patch(rect_out)
    rect_in = Rectangle((0.018, 0.015), 0.964, 0.970, fill=False, edgecolor=COLOR_BORDER, linewidth=0.8)
    ax_frame.add_patch(rect_in)

    # Membrete institucional Superior Izquierdo
    ax_frame.text(0.025, 0.972, "REPÚBLICA BOLIVARIANA DE VENEZUELA", 
                  fontsize=13, fontweight='bold', color=COLOR_HEADER_RED, family='sans-serif', va='top')
    ax_frame.text(0.025, 0.954, "MUNICIPIO INDEPENDENCIA YARACUY", 
                  fontsize=12, fontweight='bold', color=COLOR_HEADER_RED, family='sans-serif', va='top')

    # Subtítulo de Especialidad Mediterránea
    ax_frame.text(0.975, 0.972, "PROYECTO VILLA MEDITERRÁNEA (ARQUITECTURA VERNÁCULA IBÉRICA & CICLÁDICA)", 
                  fontsize=8.5, fontweight='bold', color='#006064', family='sans-serif', va='top', ha='right')
    ax_frame.text(0.975, 0.954, "DISEÑO PARAMÉTRICO OPENCAD / OPENSCAD", 
                  fontsize=8.0, fontweight='bold', color='#00838F', family='sans-serif', va='top', ha='right')

    # Cajetín Inferior
    caj_bot = 0.020
    caj_h = 0.076 if not is_landscape else 0.096
    caj_top = caj_bot + caj_h
    caj_w = 0.960
    caj_left = 0.020

    # Línea superior del cajetín
    ax_frame.plot([caj_left, caj_left + caj_w], [caj_top, caj_top], color=COLOR_BORDER, lw=1.5)

    # Título principal del plano (Rojo centrado)
    title_y = caj_top - 0.014
    ax_frame.text(0.50, title_y, title_line1, fontsize=12.0, fontweight='bold', 
                  color=COLOR_HEADER_RED, ha='center', va='center', family='sans-serif')
    if title_line2:
        ax_frame.text(0.50, title_y - 0.013, title_line2, fontsize=10.0, fontweight='bold', 
                      color=COLOR_HEADER_RED, ha='center', va='center', family='sans-serif')

    # Fila de cajas técnicas con bordes azules
    row_top = caj_top - (0.030 if not title_line2 else 0.034)
    row_bot = caj_bot
    ax_frame.plot([caj_left, caj_left + caj_w], [row_top, row_top], color=COLOR_BORDER, lw=1.2)

    col_divs = [0.280, 0.465, 0.655, 0.825, 0.905]
    for cx in col_divs:
        ax_frame.plot([cx, cx], [row_bot, row_top], color=COLOR_BORDER, lw=1.0)

    # Textos del Cajetín
    ax_frame.text(0.023, row_top - 0.007, "UBICACIÓN:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.023, row_top - 0.019, "AVENIDA 4 ENTRE CALLES 30 Y 31 30-7", 
                  fontsize=7.5, fontweight='bold', color=COLOR_CAJETIN_RED)
    ax_frame.text(0.023, row_top - 0.030, "MUNICIPIO INDEPENDENCIA ESTADO YARACUY.", 
                  fontsize=7.2, fontweight='bold', color=COLOR_CAJETIN_RED)

    ax_frame.text(0.283, row_top - 0.007, "PROPIEDAD:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.283, row_top - 0.019, "ALVARO ARGELIO DIAZ FLOREZ.", 
                  fontsize=8.0, fontweight='bold', color=COLOR_CAJETIN_RED)
    ax_frame.text(0.283, row_top - 0.030, "C.I.: 24.633.787", 
                  fontsize=7.5, fontweight='bold', color=COLOR_CAJETIN_RED)

    ax_frame.text(0.468, row_top - 0.007, "ESPECIALISTA ARQ. MEDITERRÁNEA / CAD:", fontsize=6.0, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.468, row_top - 0.019, "ARQ. ESPECIALISTA EN ESTILO MEDITERRÁNEO", 
                  fontsize=7.8, fontweight='bold', color=COLOR_CAJETIN_RED)
    ax_frame.text(0.468, row_top - 0.030, "T.S.U. ANGEL CAMACARO M. (CVPT 1260)", 
                  fontsize=6.8, fontweight='bold', color=COLOR_CAJETIN_RED)

    ax_frame.text(0.658, row_top - 0.007, "REVISADO:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.658, row_top - 0.021, "APROBADO PARA EJECUCIÓN", fontsize=7.0, fontweight='bold', color='#1B5E20')

    ax_frame.text(0.828, row_top - 0.007, "FECHA:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.865, row_top - 0.023, fecha, fontsize=8.5, fontweight='bold', 
                  color=COLOR_CAJETIN_RED, ha='center')

    ax_frame.text(0.908, row_top - 0.007, "ESCALA:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.942, row_top - 0.023, escala, fontsize=9.0, fontweight='bold', 
                  color=COLOR_TEXT_BLACK, ha='center')

def draw_north_arrow(ax, x, y, size=1.5):
    """Dibuja una flecha arquitectónica de Norte."""
    ax.annotate('', xy=(x, y + size), xytext=(x, y),
                arrowprops=dict(facecolor='black', edgecolor='black', width=2.0, headwidth=6.0), zorder=9)
    ax.text(x, y + size + 0.3, "N", fontsize=8.5, fontweight='bold', ha='center', va='bottom', color='#000000', zorder=9)

def draw_rect_wall(ax, x1, y1, x2, y2, color=COLOR_WALL_FILL, hatch=None):
    """Dibuja un segmento de muro relleno con línea de borde y textura."""
    rx = min(x1, x2)
    ry = min(y1, y2)
    rw = abs(x2 - x1)
    rh = abs(y2 - y1)
    rect = Rectangle((rx, ry), rw, rh, facecolor=color, edgecolor=COLOR_WALL_LINE, 
                     linewidth=0.7, hatch=hatch, zorder=3)
    ax.add_patch(rect)

def draw_door_swing(ax, hinge_x, hinge_y, width, angle_start, angle_end):
    """Dibuja una puerta arquitectónica con hoja y arco de apertura de 90°."""
    rad = math.radians(angle_start)
    leaf_x = hinge_x + width * math.cos(rad)
    leaf_y = hinge_y + width * math.sin(rad)
    ax.plot([hinge_x, leaf_x], [hinge_y, leaf_y], color=COLOR_DOOR, lw=1.2, zorder=4)
    arc = Arc((hinge_x, hinge_y), 2*width, 2*width, angle=0, theta1=min(angle_start, angle_end), 
              theta2=max(angle_start, angle_end), color=COLOR_DOOR, lw=0.6, linestyle='-', zorder=4)
    ax.add_patch(arc)

def draw_window_mediterraneo(ax, x1, y1, x2, y2, is_vertical=False, is_abocinado=True):
    """Dibuja vano abocinado mediterráneo (derrame suave para control térmico)."""
    if not is_vertical:
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymid = (y1 + y2) / 2
        thick = abs(y2 - y1)
        ax.add_patch(Rectangle((xmin, min(y1, y2)), xmax - xmin, thick, facecolor='#E1F5FE', edgecolor='none', zorder=4))
        ax.plot([xmin, xmin], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmax, xmax], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmin, xmax], [ymid, ymid], color=COLOR_WINDOW, lw=1.0, zorder=5)
        if is_abocinado:
            ax.plot([xmin, xmin + 0.15], [y1, y1 - 0.08], color='#006064', lw=0.6, linestyle=':', zorder=5)
            ax.plot([xmax, xmax - 0.15], [y1, y1 - 0.08], color='#006064', lw=0.6, linestyle=':', zorder=5)
    else:
        ymin, ymax = min(y1, y2), max(y1, y2)
        xmid = (x1 + x2) / 2
        thick = abs(x2 - x1)
        ax.add_patch(Rectangle((min(x1, x2), ymin), thick, ymax - ymin, facecolor='#E1F5FE', edgecolor='none', zorder=4))
        ax.plot([x1, x2], [ymin, ymin], color='black', lw=0.8, zorder=5)
        ax.plot([x1, x2], [ymax, ymax], color='black', lw=0.8, zorder=5)
        ax.plot([xmid, xmid], [ymin, ymax], color=COLOR_WINDOW, lw=1.0, zorder=5)
        if is_abocinado:
            ax.plot([x1, x1 - 0.08], [ymin, ymin + 0.15], color='#006064', lw=0.6, linestyle=':', zorder=5)
            ax.plot([x1, x1 - 0.08], [ymax, ymax - 0.15], color='#006064', lw=0.6, linestyle=':', zorder=5)

def draw_col_hatch(ax, cx, cy, size=0.25):
    """Dibuja una columna estructural con achurado reglamentario."""
    s2 = size / 2
    rect = Rectangle((cx - s2, cy - s2), size, size, facecolor='#FFEAEA', 
                     edgecolor=COLOR_COL_RED, linewidth=1.1, hatch='///', zorder=6)
    ax.add_patch(rect)

def draw_dim_h(ax, x1, x2, y, text, offset=0.0):
    """Cota horizontal estilo venezolano (coma decimal, ticks a 45°)."""
    yd = y + offset
    ax.plot([x1, x2], [yd, yd], color='#000000', lw=0.6, zorder=7)
    tk = 0.10
    ax.plot([x1 - tk, x1 + tk], [yd - tk, yd + tk], color='#000000', lw=0.8, zorder=7)
    ax.plot([x2 - tk, x2 + tk], [yd - tk, yd + tk], color='#000000', lw=0.8, zorder=7)
    if abs(offset) > 0.05:
        ax.plot([x1, x1], [y, yd + (0.08 if offset > 0 else -0.08)], color='#707070', lw=0.4, linestyle=':', zorder=6)
        ax.plot([x2, x2], [y, yd + (0.08 if offset > 0 else -0.08)], color='#707070', lw=0.4, linestyle=':', zorder=6)
    ax.text((x1 + x2)/2, yd + 0.08, text, fontsize=6.8, ha='center', va='bottom', 
            color='#000000', fontweight='bold', zorder=8)

def draw_dim_v(ax, x, y1, y2, text, offset=0.0):
    """Cota vertical estilo venezolano (coma decimal, ticks a 45°)."""
    xd = x + offset
    ax.plot([xd, xd], [y1, y2], color='#000000', lw=0.6, zorder=7)
    tk = 0.10
    ax.plot([xd - tk, xd + tk], [y1 - tk, y1 + tk], color='#000000', lw=0.8, zorder=7)
    ax.plot([xd - tk, xd + tk], [y2 - tk, y2 + tk], color='#000000', lw=0.8, zorder=7)
    if abs(offset) > 0.05:
        ax.plot([x, xd + (0.08 if offset > 0 else -0.08)], [y1, y1], color='#707070', lw=0.4, linestyle=':', zorder=6)
        ax.plot([x, xd + (0.08 if offset > 0 else -0.08)], [y2, y2], color='#707070', lw=0.4, linestyle=':', zorder=6)
    ax.text(xd - 0.08, (y1 + y2)/2, text, fontsize=6.8, ha='right', va='center', 
            color='#000000', fontweight='bold', rotation=90, zorder=8)


# =============================================================================
# LÁMINA 1: PLANTA BAJA (COMERCIAL Y GARAJE) Y SÓTANO
# =============================================================================
def build_sheet_1(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA DISTRIBUCIÓN", 
                     "PLANTA BAJA (ZONA COMERCIAL Y GARAJE AMPLIADO 2,80 m) Y SÓTANO.", escala="1:75")

    # PLANTA BAJA
    ax_pb = fig.add_axes([0.08, 0.44, 0.84, 0.48])
    ax_pb.set_aspect('equal')
    ax_pb.set_xlim(-2.0, 11.5)
    ax_pb.set_ylim(-2.0, 24.5)
    ax_pb.axis('off')

    ax_pb.text(4.5, -1.2, "PLANTA BAJA - ZONA COMERCIAL (98 m²) Y GARAJE TECHADO (2,80 m LIBRES)", 
               fontsize=9.5, fontweight='bold', ha='center', va='top')
    ax_pb.plot([0.0, 9.0], [-1.55, -1.55], color='black', lw=1.2)
    draw_north_arrow(ax_pb, 10.0, 20.0, size=1.5)

    # 1. Muro Propio Izquierdo (Eje 0)
    draw_rect_wall(ax_pb, 0.15, 0.00, 0.30, 21.71, color='#CFD8DC')
    ax_pb.text(0.225, 22.2, "MURO PROPIO\n(EJE 0)", fontsize=6.2, ha='center', va='bottom', color=COLOR_COL_RED, fontweight='bold')

    # 2. Fachada Frontal Avenida 4 (Y: 21.56 a 21.71 m)
    draw_rect_wall(ax_pb, 0.30, 21.56, 0.40, 21.71, color=COLOR_WALL_FILL)
    ax_pb.plot([0.40, 2.65], [21.63, 21.63], color='#3E2723', lw=2.0)
    ax_pb.text(1.52, 22.1, "PORTÓN GARAJE\nANCHO 2,25 m", fontsize=6.0, ha='center', va='bottom', color='#3E2723', fontweight='bold')
    draw_rect_wall(ax_pb, 2.65, 21.56, 2.75, 21.71, color=COLOR_WALL_FILL)

    # Muro Divisorio Eje 1 (X: 2.75 a 2.90 m)
    draw_rect_wall(ax_pb, 2.75, 0.15, 2.90, 21.71, color='#CFD8DC')
    ax_pb.text(2.825, 22.2, "EJE 1", fontsize=6.2, ha='center', va='bottom', color=COLOR_AXIS_CYAN, fontweight='bold')

    # Vitrinas y Acceso Comercial (X: 2.90 a 9.15 m)
    draw_rect_wall(ax_pb, 2.90, 21.56, 3.15, 21.71, color=COLOR_WALL_FILL)
    ax_pb.plot([3.15, 5.65], [21.63, 21.63], color=COLOR_WINDOW, lw=2.0)
    ax_pb.text(4.40, 22.0, "VITRINA COMERCIAL 1\nL = 2,50 m", fontsize=5.8, ha='center', va='bottom', color=COLOR_WINDOW)
    draw_rect_wall(ax_pb, 5.65, 21.56, 6.20, 21.71, color=COLOR_WALL_FILL)
    ax_pb.plot([6.20, 8.80], [21.63, 21.63], color=COLOR_WINDOW, lw=2.0)
    ax_pb.text(7.50, 22.0, "VITRINA 2 Y ACCESO\nL = 2,60 m", fontsize=5.8, ha='center', va='bottom', color=COLOR_WINDOW)
    draw_rect_wall(ax_pb, 8.80, 21.56, 9.15, 21.71, color=COLOR_WALL_FILL)

    # 3. Muro Lateral Derecho Eje 3 (X = 9.00 a 9.15 m)
    draw_rect_wall(ax_pb, 9.00, 3.50, 9.15, 21.71, color=COLOR_WALL_FILL)
    ax_pb.text(9.075, 22.2, "MURO LATERAL (EJE 3)", fontsize=6.2, ha='center', va='bottom', color=COLOR_COL_RED, fontweight='bold')

    # Garaje Techado
    ax_pb.text(1.52, 15.00, "GARAJE TECHADO\n2,45 x 21,56 m\n(2,80 m libre entre ejes)", 
               fontsize=7.2, ha='center', va='center', fontweight='bold', color='#1A237E')
    veh_rect = Rectangle((0.60, 11.50), 1.85, 4.60, facecolor='#E8EAF6', edgecolor='#3F51B5', lw=1.0, linestyle='--', zorder=4)
    ax_pb.add_patch(veh_rect)
    ax_pb.text(1.52, 13.80, "PUESTO DE\nESTACIONAMIENTO\n(4,60 x 1,85 m)", fontsize=5.5, ha='center', va='center', color='#3F51B5')

    # Gran Salón Comercial
    ax_pb.text(5.95, 13.00, "LOCAL COMERCIAL POLIVALENTE\nÁREA NETA: 98,20 m²\nN.P.T. ±0,00", 
               fontsize=8.5, ha='center', va='center', fontweight='bold', color='#263238')

    # Escalera Intacta de Acceso (PB a P2)
    draw_rect_wall(ax_pb, 1.40, 4.40, 1.55, 7.35, color=COLOR_WALL_FILL)
    draw_rect_wall(ax_pb, 2.65, 4.40, 2.80, 7.35, color=COLOR_WALL_FILL)
    for sy in np.linspace(4.40, 7.35, 13):
        ax_pb.plot([1.55, 2.65], [sy, sy], color=COLOR_STAIRS, lw=0.8)
    ax_pb.annotate('', xy=(2.10, 7.10), xytext=(2.10, 4.60),
                   arrowprops=dict(facecolor='black', edgecolor='black', width=1.0, headwidth=4.0))
    ax_pb.text(2.10, 5.85, "SUBE A P2", rotation=90, fontsize=6.0, ha='center', va='center', fontweight='bold')

    # Baño de Servicio Local Comercial
    draw_rect_wall(ax_pb, 5.85, 3.50, 9.15, 3.65, color=COLOR_WALL_FILL)
    draw_rect_wall(ax_pb, 5.85, 5.40, 9.15, 5.55, color=COLOR_WALL_FILL)
    draw_rect_wall(ax_pb, 5.85, 3.65, 6.00, 5.40, color=COLOR_WALL_FILL)
    draw_door_swing(ax_pb, 6.00, 4.50, 0.75, 270, 180)
    ax_pb.text(7.50, 4.50, "Baño Servicio\nLocal 3,15 x 1,75 m", fontsize=6.2, ha='center', va='center')

    # Depósito / Oficina de Planta Baja
    draw_rect_wall(ax_pb, 0.15, 0.00, 6.40, 0.15, color=COLOR_WALL_FILL)
    draw_rect_wall(ax_pb, 0.15, 3.50, 2.75, 3.65, color=COLOR_WALL_FILL)
    draw_rect_wall(ax_pb, 2.90, 3.50, 6.25, 3.65, color=COLOR_WALL_FILL)
    draw_door_swing(ax_pb, 3.80, 3.65, 0.85, 180, 90)
    ax_pb.text(4.50, 1.85, "Depósito / Logística\n3,35 x 3,35 m", fontsize=6.8, ha='center', va='center', fontweight='bold')

    # Columnas Estructurales Planta Baja (31 columnas fijas)
    cols_p1_p2 = [
        (0.275, 21.585), (2.825, 21.585), (5.925, 21.585), (9.075, 21.585),
        (0.275, 18.575), (2.825, 18.575), (5.925, 18.575), (9.075, 18.575),
        (0.275, 16.325), (2.825, 16.325), (5.925, 16.325),
        (9.075, 14.625),
        (0.275, 12.025), (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
        (0.275, 8.875),  (2.825, 8.875),  (5.925, 8.875),  (9.075, 8.875),
        (0.275, 6.575),  (2.825, 6.575),  (5.925, 6.575),  (9.075, 6.575),
        (0.275, 3.575),  (2.825, 3.575),  (5.925, 3.575),  (9.075, 3.575),
        (0.275, 0.075),  (2.825, 0.075),  (5.925, 0.075)
    ]
    for cx, cy in cols_p1_p2:
        draw_col_hatch(ax_pb, cx, cy, size=0.25)

    # Cotas Planta Baja
    draw_dim_h(ax_pb, 0.30, 2.75, 22.8, "2,45 (Garaje)", offset=0.0)
    draw_dim_h(ax_pb, 2.90, 9.00, 22.8, "6,10 (Local)", offset=0.0)
    draw_dim_h(ax_pb, 0.15, 9.15, 23.6, "9,00 (Total Frente)", offset=0.0)
    draw_dim_v(ax_pb, -0.6, 0.00, 21.71, "21,71 m", offset=0.0)

    # PLANTA SÓTANO
    ax_sot = fig.add_axes([0.15, 0.10, 0.70, 0.32])
    ax_sot.set_aspect('equal')
    ax_sot.set_xlim(-1.5, 11.0)
    ax_sot.set_ylim(-1.5, 9.5)
    ax_sot.axis('off')

    ax_sot.text(4.5, -0.7, "PLANTA SÓTANO (Z = -2,55 m) - FUNDACIÓN Y ESTRUCTURA DE RETENCIÓN", 
               fontsize=9.0, fontweight='bold', ha='center', va='top')
    ax_sot.plot([0.5, 8.5], [-1.0, -1.0], color='black', lw=1.0)

    # Muros Sótano
    draw_rect_wall(ax_sot, 0.15, 0.00, 6.40, 0.15, color='#90A4AE')
    draw_rect_wall(ax_sot, 0.15, 0.00, 0.30, 8.30, color='#90A4AE')
    draw_rect_wall(ax_sot, 0.30, 8.15, 9.15, 8.30, color='#90A4AE')
    draw_rect_wall(ax_sot, 8.95, 3.50, 9.15, 8.30, color='#90A4AE')
    draw_rect_wall(ax_sot, 6.25, 0.15, 6.40, 8.15, color='#90A4AE')
    draw_rect_wall(ax_sot, 0.30, 3.50, 6.00, 3.65, color='#90A4AE')

    ax_sot.text(3.3, 5.8, "Cava - Depósito Subterráneo\n5,80 x 4,35 m", fontsize=6.8, ha='center', va='center', fontweight='bold')
    ax_sot.text(7.6, 5.8, "Área Técnica / Cuarto Bombas\n2,65 x 4,35 m", fontsize=6.8, ha='center', va='center')
    ax_sot.text(3.3, 1.8, "Almacén General de Sótano\n5,80 x 3,20 m", fontsize=6.8, ha='center', va='center')

    # 8 Columnas Sótano 35x35 cm
    for cx, cy in [(0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
                   (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575)]:
        draw_col_hatch(ax_sot, cx, cy, size=0.35)

    draw_dim_h(ax_sot, 0.15, 6.40, 8.8, "6,25")
    draw_dim_h(ax_sot, 6.40, 9.15, 8.8, "2,75")
    draw_dim_v(ax_sot, -0.4, 0.00, 8.30, "8,30 m")

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 1 generada exitosamente.")


# =============================================================================
# LÁMINA 2: PLANTA ALTA - VILLA RESIDENCIAL MEDITERRÁNEA
# =============================================================================
def build_sheet_2(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA DISTRIBUCIÓN - PLANTA ALTA", 
                     "VILLA MEDITERRÁNEA (LOGGIA CON 3 ARCOS, PÉRGOLAS, SALÓN DIÁFANO Y SUITES).", escala="1:75")

    ax = fig.add_axes([0.12, 0.12, 0.76, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 12.0)
    ax.set_ylim(-2.5, 25.0)
    ax.axis('off')

    ax.text(4.5, -1.3, "PLANTA ALTA - RESIDENCIA VILLA MEDITERRÁNEA CON LOGGIA DE ARCOS Y PÉRGOLAS DE SOMBRA", 
            fontsize=9.0, fontweight='bold', ha='center', va='top')
    ax.plot([0.0, 9.0], [-1.65, -1.65], color='black', lw=1.2)
    draw_north_arrow(ax, 10.5, 21.0, size=1.5)

    # 1. PÓRTICO FRONTAL CON 3 ARCOS DE MEDIO PUNTO (Y = 21.41 a 21.71 m)
    draw_rect_wall(ax, 0.15, 21.41, 0.50, 21.71, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 2.80, 21.41, 3.40, 21.71, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 5.70, 21.41, 6.30, 21.71, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 8.60, 21.41, 9.15, 21.71, color=COLOR_WHITE_WALL)

    for ax_start, ax_end, lbl in [(0.50, 2.80, "ARCO 1"), (3.40, 5.70, "ARCO 2"), (6.30, 8.60, "ARCO 3")]:
        mid_x = (ax_start + ax_end) / 2
        r = (ax_end - ax_start) / 2
        arc = Arc((mid_x, 21.41), 2*r, 0.60, angle=0, theta1=0, theta2=180, color=COLOR_ARCH, lw=1.5, zorder=5)
        ax.add_patch(arc)
        ax.text(mid_x, 21.90, f"{lbl}\n(Luz 2,30 m)", fontsize=5.8, ha='center', va='bottom', color=COLOR_ARCH, fontweight='bold')

    # Loggia Sombreada Frontal (Y: 19.56 a 21.41 m)
    ax.add_patch(Rectangle((0.15, 19.56), 9.00, 1.85, facecolor='#FFFDE7', edgecolor=COLOR_PERGOLA, lw=0.8, linestyle='--', zorder=2))
    ax.text(4.65, 20.45, "LOGGIA MEDITERRÁNEA Y SOLÁRIUM SOMBREADO (9,00 x 2,15 m)\nPérgola de Vigas de Madera y Cañizo Filtrante", 
            fontsize=6.8, ha='center', va='center', fontweight='bold', color=COLOR_PERGOLA)

    # Vigas de pérgola sobre la loggia
    for vx in [0.50, 3.40, 6.30, 8.90]:
        ax.plot([vx, vx], [19.56, 21.71], color=COLOR_PERGOLA, lw=2.2, zorder=4)
    for py in np.linspace(19.70, 21.60, 5):
        ax.plot([0.30, 9.00], [py, py], color=COLOR_PERGOLA, lw=0.9, linestyle=':', zorder=4)

    # 2. Muro Interior de Cerramiento (Y = 19.56 a 19.71 m)
    draw_rect_wall(ax, 0.15, 19.56, 1.20, 19.71, color=COLOR_WHITE_WALL)
    ax.plot([1.20, 4.80], [19.63, 19.63], color=COLOR_WINDOW, lw=2.0, zorder=5)
    ax.text(3.00, 19.25, "Ventanero Corredizo Salón a Loggia (L = 3,60 m)", fontsize=5.8, ha='center', color=COLOR_WINDOW)
    draw_rect_wall(ax, 4.80, 19.56, 6.50, 19.71, color=COLOR_WHITE_WALL)
    ax.plot([6.50, 8.50], [19.63, 19.63], color=COLOR_WINDOW, lw=1.8, zorder=5)
    ax.text(7.50, 19.25, "Puerta Balcón Suite (2,00 m)", fontsize=5.5, ha='center', color=COLOR_WINDOW)
    draw_rect_wall(ax, 8.50, 19.56, 9.15, 19.71, color=COLOR_WHITE_WALL)

    # 3. Muro Propio Izquierdo (Eje 0) encalado
    draw_rect_wall(ax, 0.15, 0.00, 0.30, 19.56, color=COLOR_WHITE_WALL)
    ax.text(0.225, 11.0, "MURO PROPIO ENCALADO (EJE 0)", rotation=90, 
            fontsize=6.0, ha='center', va='center', color='#37474F', fontweight='bold')

    # 4. Gran Salón Diáfano Mediterráneo (Living / Comedor)
    ax.text(3.10, 16.50, "GRAN SALÓN MEDITERRÁNEO\nConcepto Abierto y Luz Natural Pasiva\nConexión Directa a la Loggia y Pérgola", 
            fontsize=7.5, ha='center', va='center', fontweight='bold', color='#1B5E20')

    # Cocina Ibérica Integrada con Isla de Obra Encalada
    ax.text(3.10, 13.80, "COCINA IBÉRICA TRADICIONAL\nAcabados de Cal, Cerámica Artesanal y Madera", 
            fontsize=6.8, ha='center', va='center', fontweight='bold', color='#D84315')
    ax.add_patch(Rectangle((2.15, 9.80), 0.95, 2.60, facecolor='#E0F2F1', edgecolor='#00796B', lw=1.2, zorder=4))
    ax.text(2.62, 11.10, "ISLA DE OBRA\n(2,60 x 0,95 m)\nEncimera Roble", fontsize=5.8, ha='center', va='center', color='#004D40', fontweight='bold')

    # Muro Divisorio Eje 2 (X: 5.85 a 6.00 m) Zona Social vs Zona de Noche
    draw_rect_wall(ax, 5.85, 3.65, 6.00, 6.20, color=COLOR_WHITE_WALL)
    draw_door_swing(ax, 6.00, 6.20, 0.85, 90, 0)
    draw_rect_wall(ax, 5.85, 7.10, 6.00, 9.50, color=COLOR_WHITE_WALL)
    draw_door_swing(ax, 6.00, 9.50, 0.85, 90, 0)
    draw_rect_wall(ax, 5.85, 10.40, 6.00, 15.40, color=COLOR_WHITE_WALL)
    draw_door_swing(ax, 6.00, 15.40, 0.85, 90, 0)
    draw_rect_wall(ax, 5.85, 16.30, 6.00, 19.56, color=COLOR_WHITE_WALL)

    # 5. Master Suite Mediterránea (Dormitorio Principal)
    ax.text(7.50, 17.50, "MASTER SUITE\n4,15 x 3,00 m\nSalida a Loggia Arqueada", 
            fontsize=7.2, ha='center', va='center', fontweight='bold', color='#01579B')
    draw_rect_wall(ax, 6.00, 15.20, 9.00, 15.35, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 6.80, 12.70, 9.00, 12.85, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 6.80, 12.85, 6.95, 15.20, color=COLOR_WHITE_WALL)
    ax.text(7.90, 14.00, "Vestidor\n2,20 x 2,35 m", fontsize=6.0, ha='center', va='center')
    ax.text(7.90, 11.50, "Baño Suite\n2,20 x 1,35 m", fontsize=6.0, ha='center', va='center')
    draw_window_mediterraneo(ax, 9.00, 13.15, 9.15, 14.05, is_vertical=True)

    # 6. Habitación 2 Mediterránea
    draw_rect_wall(ax, 6.00, 8.85, 9.00, 9.00, color=COLOR_WHITE_WALL)
    ax.text(7.50, 10.00, "HABITACIÓN 2\n3,00 x 3,60 m\nVano Abocinado", 
            fontsize=7.0, ha='center', va='center', fontweight='bold')
    draw_window_mediterraneo(ax, 9.00, 9.65, 9.15, 11.85, is_vertical=True)

    # 7. Habitación 3 Mediterránea
    draw_rect_wall(ax, 6.00, 5.40, 9.00, 5.55, color=COLOR_WHITE_WALL)
    ax.text(7.50, 7.10, "HABITACIÓN 3\n3,00 x 3,45 m\nVano Abocinado", 
            fontsize=7.0, ha='center', va='center', fontweight='bold')
    draw_window_mediterraneo(ax, 9.00, 6.30, 9.15, 8.00, is_vertical=True)

    # 8. Baño Familiar Compartido
    ax.text(7.50, 4.50, "Baño Familiar\n3,00 x 1,75 m", fontsize=6.2, ha='center', va='center')
    draw_rect_wall(ax, 6.25, 3.50, 9.15, 3.65, color=COLOR_WHITE_WALL)
    draw_window_mediterraneo(ax, 9.00, 4.10, 9.15, 5.00, is_vertical=True)

    # 9. Llegada Escalera Intacta desde PB (X: 1.55 a 2.65, Y: 4.40 a 7.35 m)
    draw_rect_wall(ax, 1.40, 4.40, 1.55, 7.35, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 2.65, 4.40, 2.80, 7.35, color=COLOR_WHITE_WALL)
    for sy in np.linspace(4.40, 7.35, 13):
        ax.plot([1.55, 2.65], [sy, sy], color=COLOR_STAIRS, lw=0.8)
    ax.text(2.10, 5.85, "LLEGA DE PB", rotation=90, fontsize=6.0, ha='center', va='center')

    # 10. Terraza Posterior con Pérgola y Lavandería
    draw_rect_wall(ax, 0.15, 4.30, 2.90, 4.45, color=COLOR_WHITE_WALL)
    draw_rect_wall(ax, 2.75, 0.15, 2.90, 4.30, color=COLOR_WHITE_WALL)
    draw_door_swing(ax, 2.75, 3.50, 0.85, 270, 180)
    ax.text(1.52, 2.20, "Lavadero / Servicio\n2,60 x 4,15 m", fontsize=6.5, ha='center', va='center')

    ax.add_patch(Rectangle((2.90, 0.15), 3.35, 3.35, facecolor='#FFFDE7', edgecolor=COLOR_PERGOLA, lw=0.8, linestyle='--', zorder=2))
    ax.text(4.55, 1.75, "TERRAZA POSTERIOR\nPérgola de Sombreo y Mirador\n3,35 x 3,35 m", 
            fontsize=6.8, ha='center', va='center', fontweight='bold', color=COLOR_PERGOLA)
    for py in np.linspace(0.40, 3.20, 6):
        ax.plot([2.90, 6.25], [py, py], color=COLOR_PERGOLA, lw=1.2, zorder=4)

    draw_rect_wall(ax, 9.00, 3.50, 9.15, 19.56, color=COLOR_WHITE_WALL)

    # 11. Columnas Estructurales fijas (31 columnas de 25x25 cm)
    cols_p1_p2 = [
        (0.275, 21.585), (2.825, 21.585), (5.925, 21.585), (9.075, 21.585),
        (0.275, 18.575), (2.825, 18.575), (5.925, 18.575), (9.075, 18.575),
        (0.275, 16.325), (2.825, 16.325), (5.925, 16.325),
        (9.075, 14.625),
        (0.275, 12.025), (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
        (0.275, 8.875),  (2.825, 8.875),  (5.925, 8.875),  (9.075, 8.875),
        (0.275, 6.575),  (2.825, 6.575),  (5.925, 6.575),  (9.075, 6.575),
        (0.275, 3.575),  (2.825, 3.575),  (5.925, 3.575),  (9.075, 3.575),
        (0.275, 0.075),  (2.825, 0.075),  (5.925, 0.075)
    ]
    for cx, cy in cols_p1_p2:
        draw_col_hatch(ax, cx, cy, size=0.25)

    # Cotas Planta Alta
    draw_dim_h(ax, 0.15, 9.15, 22.8, "9,00 m (Ancho Total Fachada con Arcos)", offset=0.0)
    draw_dim_h(ax, 0.15, 5.85, 20.6, "5,70 m (Zona Social)", offset=0.0)
    draw_dim_h(ax, 5.85, 9.15, 20.6, "3,30 m (Zona Dormitorios)", offset=0.0)
    draw_dim_v(ax, -1.0, 0.00, 21.71, "21,71 m (Cuerpo Edificio)", offset=0.0)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 2 generada exitosamente.")


# =============================================================================
# LÁMINA 3: PLANO ESTRUCTURAL Y DE AZOTEA SOLÁRIUM TRANSITABLE
# =============================================================================
def build_sheet_3(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO ESTRUCTURAL Y AZOTEA SOLÁRIUM TRANSITABLE", 
                     "RETÍCULA MODULAR DE 31 COLUMNAS, PÉRGOLAS Y CUBIERTA PLANA CON ANTEPECHO.", escala="1:75")

    ax = fig.add_axes([0.12, 0.12, 0.76, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-3.0, 12.0)
    ax.set_ylim(-2.5, 25.5)
    ax.axis('off')

    ax.text(4.5, -1.3, "SISTEMA ESTRUCTURAL: PÓRTICOS DE H.A. (31 COLUMNAS 25x25) + CUBIERTA PLANA TRANSITABLE A LA CATALANA", 
            fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax.plot([0.0, 9.0], [-1.65, -1.65], color='black', lw=1.2)
    draw_north_arrow(ax, 10.5, 21.0, size=1.5)

    # 1. Ejes Estructurales Transversales (Ejes 0, 1, 2, 3)
    ejes_x = [(0.275, '0'), (2.825, '1'), (5.925, '2'), (9.075, '3')]
    for ex, label in ejes_x:
        ax.plot([ex, ex], [-1.0, 24.0], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((ex, 24.4), 0.35, facecolor='white', edgecolor=COLOR_AXIS_CYAN, lw=0.9, zorder=5))
        ax.text(ex, 24.4, label, fontsize=8.0, fontweight='bold', color=COLOR_AXIS_CYAN, ha='center', va='center', zorder=6)

    # Ejes Estructurales Longitudinales (Ejes A0 a G y Sótano)
    ejes_y = [
        (21.585, 'A0'), (18.575, 'A'), (16.325, 'B'), (14.625, 'C'),
        (12.025, 'D'), (8.875, 'E'), (6.575, 'F'), (3.575, 'G'), (0.075, 'SOT')
    ]
    for ey, label in ejes_y:
        ax.plot([-1.5, 10.5], [ey, ey], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((-1.9, ey), 0.35, facecolor='white', edgecolor=COLOR_AXIS_CYAN, lw=0.9, zorder=5))
        ax.text(-1.9, ey, label, fontsize=7.5, fontweight='bold', color=COLOR_AXIS_CYAN, ha='center', va='center', zorder=6)

    # Líneas de conexión de vigas principales
    for i in range(len(ejes_x)-1):
        x_a = ejes_x[i][0]
        x_b = ejes_x[i+1][0]
        for ey, _ in ejes_y:
            ax.plot([x_a, x_b], [ey, ey], color='#CFD8DC', lw=1.2, zorder=1)
    for ex, _ in ejes_x:
        for i in range(len(ejes_y)-1):
            y_a = ejes_y[i][0]
            y_b = ejes_y[i+1][0]
            ax.plot([ex, ex], [y_a, y_b], color='#CFD8DC', lw=1.2, zorder=1)

    # 2. COLUMNAS ESTRUCTURALES P.B. Y P.A. (31 unidades de 25x25 cm)
    cols_p1_p2 = [
        (0.275, 21.585), (2.825, 21.585), (5.925, 21.585), (9.075, 21.585),
        (0.275, 18.575), (2.825, 18.575), (5.925, 18.575), (9.075, 18.575),
        (0.275, 16.325), (2.825, 16.325), (5.925, 16.325),
        (9.075, 14.625),
        (0.275, 12.025), (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
        (0.275, 8.875),  (2.825, 8.875),  (5.925, 8.875),  (9.075, 8.875),
        (0.275, 6.575),  (2.825, 6.575),  (5.925, 6.575),  (9.075, 6.575),
        (0.275, 3.575),  (2.825, 3.575),  (5.925, 3.575),  (9.075, 3.575),
        (0.275, 0.075),  (2.825, 0.075),  (5.925, 0.075)
    ]
    for cx, cy in cols_p1_p2:
        draw_col_hatch(ax, cx, cy, size=0.25)

    # 3. COLUMNAS DE SÓTANO (35x35 cm)
    sot_cols = [
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in sot_cols:
        ax.add_patch(Rectangle((cx - 0.175, cy - 0.175), 0.35, 0.35, 
                               fill=False, edgecolor='#0000FF', lw=1.2, zorder=7))

    # 4. AZOTEA SOLÁRIUM TRANSITABLE (CUBIERTA A LA CATALANA)
    ax.add_patch(Rectangle((0.15, 0.00), 9.00, 21.71, facecolor=COLOR_SOLARIUM, edgecolor='#000000', lw=1.5, zorder=2))
    ax.add_patch(Rectangle((0.15, 0.00), 0.30, 21.71, facecolor='#ECEFF1', edgecolor='#000000', lw=0.7, zorder=3))
    ax.add_patch(Rectangle((8.85, 0.00), 0.30, 21.71, facecolor='#ECEFF1', edgecolor='#000000', lw=0.7, zorder=3))
    ax.add_patch(Rectangle((0.15, 0.00), 9.00, 0.30, facecolor='#ECEFF1', edgecolor='#000000', lw=0.7, zorder=3))
    ax.add_patch(Rectangle((0.15, 21.41), 9.00, 0.30, facecolor='#ECEFF1', edgecolor='#000000', lw=0.7, zorder=3))

    for ty in np.linspace(1.0, 20.5, 14):
        ax.plot([0.55, 8.75], [ty, ty], color='#FFE0B2', lw=0.5, linestyle='-', zorder=3)

    ax.add_patch(Rectangle((0.50, 18.00), 0.50, 3.00, facecolor='#E0F2F1', edgecolor='#00695C', lw=0.9, zorder=4))
    ax.add_patch(Rectangle((1.00, 20.50), 2.50, 0.50, facecolor='#E0F2F1', edgecolor='#00695C', lw=0.9, zorder=4))
    ax.text(2.25, 19.50, "BANCADA CICLÁDICA DE OBRA\nMirador Panorámico Solárium", fontsize=5.8, ha='center', va='center', color='#004D40')

    ax.scatter([1.00, 8.30], [1.00, 1.00], marker='o', s=35, color='#0277BD', zorder=5)
    ax.scatter([1.00, 8.30], [20.70, 20.70], marker='o', s=35, color='#0277BD', zorder=5)
    ax.text(1.00, 1.30, "Bajante B.A.P. Ø4\"", fontsize=5.0, ha='center', color='#0277BD')
    ax.text(8.30, 1.30, "Bajante B.A.P. Ø4\"", fontsize=5.0, ha='center', color='#0277BD')

    for vx in [0.50, 3.40, 6.30, 8.90]:
        ax.plot([vx, vx], [19.56, 21.71], color=COLOR_PERGOLA, lw=2.2, zorder=6)

    # 5. Cuadro de Especificaciones Estructurales
    ax.add_patch(Rectangle((-0.8, -0.2), 10.5, 3.4, facecolor='#F9FBE7', edgecolor=COLOR_BORDER, lw=1.0, zorder=8))
    ax.text(-0.5, 2.9, "ESPECIFICACIONES DEL SISTEMA ESTRUCTURAL Y CUBIERTA MEDITERRÁNEA:", 
            fontsize=7.2, fontweight='bold', color=COLOR_BORDER, zorder=9)
    ax.text(-0.5, 2.3, "• Estructura Porticada: 31 Columnas de 25x25 cm en H.A. f'c = 250 kg/cm² con acero de refuerzo Fy = 4.200 kg/cm².", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 1.7, "• Arquería Frontal: 3 Arcos de medio punto (Luz = 2,30 m) integrados a la viga de fachada en Avenida 4.", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 1.1, "• Pérgolas Solares: Viguería de madera de pino laminado tratado 15x8 cm @ 0,45 m con esterilla de cañizo natural.", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 0.5, "• Azotea Transitable: Losa maciza nervada con aislamiento térmico, impermeabilización asfáltica y baldosas de barro cocido.", 
            fontsize=6.5, color='#000000', zorder=9)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 3 generada exitosamente.")


# =============================================================================
# LÁMINA 4: PLANO FACHADAS Y ELEVACIONES MEDITERRÁNEAS (17x11 in)
# =============================================================================
def build_sheet_4(pdf):
    fig = plt.figure(figsize=(17, 11), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO FACHADAS Y ELEVACIONES MEDITERRÁNEAS", 
                     "FACHADA PRINCIPAL (AV. 4 CON 3 ARCOS DE MEDIO PUNTO) — LATERAL CON TALUD — POSTERIOR.", 
                     escala="1:75", is_landscape=True)

    # 1. FACHADA PRINCIPAL (AVENIDA 4)
    ax_prin = fig.add_axes([0.05, 0.52, 0.43, 0.38])
    ax_prin.set_aspect('equal')
    ax_prin.set_xlim(-2.5, 11.5)
    ax_prin.set_ylim(-1.5, 10.5)
    ax_prin.axis('off')

    ax_prin.text(4.5, -0.7, "FACHADA PRINCIPAL (AVENIDA 4) - VILLA MEDITERRÁNEA CON ARQUERÍA", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_prin.plot([0.5, 8.5], [-1.05, -1.05], color='black', lw=1.0)
    ax_prin.plot([-2.0, 11.0], [0.0, 0.0], color='#000000', lw=1.5)

    # Planta Baja Comercial y Garaje (Z: 0.00 a 3.00 m)
    ax_prin.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor=COLOR_WALL_FILL, edgecolor='#000000', lw=1.2))
    
    # Portón Garaje (Z: 0.00 a 2.30 m)
    ax_prin.add_patch(Rectangle((0.35, 0.00), 2.70, 2.30, facecolor='#3E2723', edgecolor='#000000', lw=1.1))
    for gy in np.linspace(0.30, 2.00, 6):
        ax_prin.plot([0.35, 3.05], [gy, gy], color='#5D4037', lw=0.8)
    ax_prin.text(1.70, 1.15, "PORTÓN GARAJE\nANCHO 2,25 m", fontsize=5.8, ha='center', va='center', color='white', fontweight='bold')

    # Vitrinas Comerciales
    for vx, lbl in [(3.35, "VITRINA 1"), (6.35, "VITRINA 2")]:
        ax_prin.add_patch(Rectangle((vx, 0.00), 2.50, 2.40, facecolor='#E0F7FA', edgecolor='#006064', lw=1.2))
        ax_prin.plot([vx + 1.25, vx + 1.25], [0.00, 2.40], color='#006064', lw=1.0)
        ax_prin.plot([vx, vx + 2.50], [1.20, 1.20], color='#006064', lw=0.8)
        ax_prin.text(vx + 1.25, 0.60, lbl, fontsize=5.5, ha='center', va='center', color='#006064')

    # Planta Alta: Fachada con 3 Arcos de Medio Punto (Z: 3.00 a 5.85 m)
    ax_prin.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.2))

    # 3 Arcos de Medio Punto
    arcos_data = [(0.50, 2.80), (3.40, 5.70), (6.30, 8.60)]
    for x_a, x_b in arcos_data:
        luz = x_b - x_a
        r = luz / 2
        mid = (x_a + x_b) / 2
        h_arr = 4.40
        ax_prin.add_patch(Rectangle((x_a, 3.00), luz, 1.40, facecolor='#FFFDE7', edgecolor='none'))
        arc_wedge = Arc((mid, h_arr), 2*r, 2*r, angle=0, theta1=0, theta2=180, color='#006064', lw=1.5)
        ax_prin.add_patch(arc_wedge)
        # Barandilla de forja mediterránea (Z: 3.00 a 3.90 m)
        ax_prin.plot([x_a, x_b], [3.90, 3.90], color='#212121', lw=1.2)
        for fx in np.linspace(x_a + 0.15, x_b - 0.15, 7):
            ax_prin.plot([fx, fx], [3.00, 3.90], color='#212121', lw=0.6)

    # Pilastras encaladas entre arcos
    for px in [0.15, 2.80, 5.70, 8.60]:
        ax_prin.plot([px, px], [3.00, 5.85], color='#78909C', lw=0.8)

    # Pérgola de madera sobresaliendo en cota +5.85 m
    for px in [0.50, 3.40, 6.30, 8.90]:
        ax_prin.add_patch(Rectangle((px - 0.08, 5.85), 0.16, 0.20, facecolor=COLOR_PERGOLA, edgecolor='black', lw=0.6))
    ax_prin.plot([0.15, 9.15], [6.05, 6.05], color=COLOR_PERGOLA, lw=2.0)

    # Antepecho perimetral encalado de Azotea Solárium (Z: 6.00 a 7.00 m)
    ax_prin.add_patch(Rectangle((0.15, 6.00), 9.00, 1.00, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.2))
    ax_prin.add_patch(Rectangle((0.10, 7.00), 9.10, 0.08, facecolor='#ECEFF1', edgecolor='#000000', lw=0.8))
    ax_prin.text(4.65, 6.50, "ANTEPECHO ENCALADO DE AZOTEA (1,00 m)", fontsize=5.8, ha='center', va='center', fontweight='bold', color='#455A64')

    # Cotas de Nivel Fachada Principal
    ax_prin.text(-1.4, 0.05, "N.P.T. ±0,00", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 3.05, "N.P.T. +3,00 (P2)", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 6.00, "N.P.T. +6,00 (Azotea)", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 7.08, "CUMBRERA +7,08 m", fontsize=6.2, fontweight='bold', ha='right')


    # 2. FACHADA POSTERIOR
    ax_post = fig.add_axes([0.52, 0.52, 0.43, 0.38])
    ax_post.set_aspect('equal')
    ax_post.set_xlim(-2.5, 11.5)
    ax_post.set_ylim(-4.5, 10.5)
    ax_post.axis('off')

    ax_post.text(4.5, -3.7, "FACHADA POSTERIOR (SÓTANO - PB - P2 TERRAZA APERGOLADA)", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_post.plot([0.5, 8.5], [-4.05, -4.05], color='black', lw=1.0)

    # Sótano (Z = -2.55 a 0.00 m)
    ax_post.add_patch(Rectangle((0.30, -2.55), 8.85, 2.55, facecolor='#90A4AE', edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((1.00, -1.60), 1.80, 1.10, facecolor='#E0F7FA', edgecolor='#006064', lw=0.8))
    ax_post.text(1.90, -1.05, "Ventana Cava", fontsize=5.5, ha='center', va='center')

    # Planta Baja (Z: 0.00 a 3.00 m)
    ax_post.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor=COLOR_WALL_FILL, edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((0.80, 1.15), 1.80, 1.45, facecolor='#E0F7FA', edgecolor='#006064', lw=0.8))
    ax_post.text(1.70, 1.85, "Ventana Depósito", fontsize=5.5, ha='center', va='center')

    # Planta Alta: Terraza Apergolada y Muros Encalados (Z: 3.00 a 5.85 m)
    ax_post.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.0))
    for px in np.linspace(3.00, 6.20, 6):
        ax_post.plot([px, px], [5.85, 6.10], color=COLOR_PERGOLA, lw=1.5)
    ax_post.plot([2.90, 6.30], [6.10, 6.10], color=COLOR_PERGOLA, lw=2.0)
    ax_post.text(4.60, 5.20, "TERRAZA APERGOLADA", fontsize=5.5, ha='center', color=COLOR_PERGOLA, fontweight='bold')

    # Ventanas con vanos abocinados
    ax_post.add_patch(Rectangle((0.80, 3.80), 1.60, 1.20, facecolor='#E0F7FA', edgecolor='#006064', lw=0.8))
    ax_post.text(1.60, 4.40, "Ventana Lavadero", fontsize=5.5, ha='center', va='center')
    ax_post.add_patch(Rectangle((6.80, 3.80), 1.80, 1.20, facecolor='#E0F7FA', edgecolor='#006064', lw=0.8))
    ax_post.text(7.70, 4.40, "Ventana Baño", fontsize=5.5, ha='center', va='center')

    # Antepecho Azotea posterior
    ax_post.add_patch(Rectangle((0.15, 6.00), 9.00, 1.00, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.2))
    ax_post.add_patch(Rectangle((0.10, 7.00), 9.10, 0.08, facecolor='#ECEFF1', edgecolor='#000000', lw=0.8))


    # 3. FACHADA LATERAL IZQUIERDA CON TALUD
    ax_lat = fig.add_axes([0.05, 0.12, 0.90, 0.36])
    ax_lat.set_aspect('equal')
    ax_lat.set_xlim(-2.0, 26.5)
    ax_lat.set_ylim(-5.5, 10.5)
    ax_lat.axis('off')

    # Terreno y Estrato Geotécnico
    steps_x = [24.71, 15.5, 14.5, 13.5, 12.5, 11.5, 10.5, 8.5, 0.0]
    steps_z = [ 0.00,  0.0, -0.4, -0.8, -1.2, -1.6, -2.0, -2.55, -2.55]
    ground_poly = [(0.0, -4.5)] + list(zip(steps_x, steps_z)) + [(24.71, -4.5)]
    ax_lat.add_patch(Polygon(ground_poly, closed=True, facecolor='#CFD8DC', edgecolor='none', zorder=1))
    ax_lat.plot(steps_x, steps_z, color=COLOR_TERRAIN, lw=2.2, zorder=4)
    ax_lat.text(13.0, -2.2, "PERFIL DE TERRENO NATURAL Y TALUD ESCALONADO", fontsize=7.0, color=COLOR_TERRAIN, fontweight='bold')

    # Sótano Posterior
    ax_lat.add_patch(Rectangle((0.00, -2.55), 8.30, 2.55, facecolor='#90A4AE', edgecolor='#000000', lw=1.2, zorder=2))

    # Planta Baja: Muro Propio Encalado
    ax_lat.add_patch(Rectangle((0.00, 0.00), 21.71, 3.00, facecolor=COLOR_WALL_FILL, edgecolor='#000000', lw=1.2, zorder=2))

    # Planta Alta: Volumen Cúbico Blanco Mediterráneo
    ax_lat.add_patch(Rectangle((0.00, 3.00), 21.71, 2.85, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.2, zorder=2))

    # Antepecho continuo de Azotea Solárium
    ax_lat.add_patch(Rectangle((0.00, 6.00), 21.71, 1.00, facecolor=COLOR_WHITE_WALL, edgecolor='#000000', lw=1.2, zorder=3))
    ax_lat.add_patch(Rectangle((-0.05, 7.00), 21.81, 0.08, facecolor='#ECEFF1', edgecolor='#000000', lw=0.8, zorder=4))

    # Vigas de Pérgola sobresaliendo hacia el frente
    ax_lat.add_patch(Rectangle((19.56, 5.85), 2.15, 0.20, facecolor=COLOR_PERGOLA, edgecolor='black', lw=0.8, zorder=5))
    ax_lat.text(20.60, 6.25, "PÉRGOLA FRONTAL", fontsize=5.8, ha='center', color=COLOR_PERGOLA, fontweight='bold')

    # Pérgola posterior en fachada lateral
    ax_lat.add_patch(Rectangle((0.15, 5.85), 3.35, 0.20, facecolor=COLOR_PERGOLA, edgecolor='black', lw=0.8, zorder=5))
    ax_lat.text(1.80, 6.25, "PÉRGOLA POSTERIOR", fontsize=5.8, ha='center', color=COLOR_PERGOLA, fontweight='bold')

    ax_lat.text(12.5, -4.5, "FACHADA LATERAL IZQUIERDA (SÓTANO + PB COMERCIAL + VOLUMEN ENCALADO MEDITERRÁNEO + AZOTEA)", 
                fontsize=9.0, fontweight='bold', ha='center', va='top')

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 4 generada exitosamente.")


# =============================================================================
# LÁMINA 5: LEVANTAMIENTO POLIGONAL DE LINDEROS, RETÍCULA UTM Y CUADRO DE ÁREAS
# =============================================================================
def build_sheet_5(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "LEVANTAMIENTO TOPOGRÁFICO Y POLIGONAL DE LINDEROS", 
                     "COORDENADAS U.T.M. (REGVEN / WGS84) Y CUADRO DE ÁREAS VILLA MEDITERRÁNEA.", escala="1:200")

    # 1. TABLA CUADRO DE COORDENADAS U.T.M.
    ax_tbl = fig.add_axes([0.05, 0.77, 0.44, 0.16])
    ax_tbl.axis('off')
    ax_tbl.text(0.5, 0.98, "CUADRO DE COORDENADAS U.T.M. (REGVEN / WGS84)", fontsize=7.8, 
                fontweight='bold', color=COLOR_HEADER_RED, ha='center', va='top')

    col_labels = ["LADO\nEST-PV", "RUMBO", "DISTANCIA", "P", "NORTE", "ESTE"]
    table_data = [
        ["1 - 2", "N 57°10'22.40\" E", "11.37 m", "1", "1.141.664,17", "529.755,04"],
        ["2 - 3", "S 30°17'59.36\" E", "24.72 m", "2", "1.141.670,33", "529.764,60"],
        ["3 - 4", "S 57°10'22.40\" W", "10.81 m", "3", "1.141.648,99", "529.777,07"],
        ["4 - 1", "N 31°36'27.01\" W", "24.70 m", "4", "1.141.643,13", "529.767,99"],
    ]
    tbl = ax_tbl.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(6.2)
    tbl.scale(1.0, 1.4)
    for key, cell in tbl.get_celld().items():
        cell.set_edgecolor(COLOR_BORDER)
        if key[0] == 0:
            cell.set_text_props(weight='bold', color=COLOR_BORDER)

    # 2. CUADRO DE LINDEROS
    ax_lind = fig.add_axes([0.50, 0.77, 0.16, 0.16])
    ax_lind.axis('off')
    ax_lind.text(0.5, 0.98, "LINDEROS", fontsize=8.0, fontweight='bold', color=COLOR_HEADER_RED, ha='center', va='top')
    lind_labels = ["LINDERO", "COLINDANTE"]
    lind_data = [
        ["NORESTE", "CASA DE\nMIGUEL RODRIGUEZ"],
        ["SURESTE", "SOLAR DE\nMIGUEL RODRIGUEZ"],
        ["NOROESTE", "AVENIDA 4"],
        ["SUROESTE", "CASA DE\nMARIO GRATEROL"],
    ]
    tbl_l = ax_lind.table(cellText=lind_data, colLabels=lind_labels, loc='center', cellLoc='center')
    tbl_l.auto_set_font_size(False)
    tbl_l.set_fontsize(5.8)
    tbl_l.scale(1.0, 1.4)
    for key, cell in tbl_l.get_celld().items():
        cell.set_edgecolor(COLOR_BORDER)
        if key[0] == 0:
            cell.set_text_props(weight='bold', color=COLOR_BORDER)

    # 3. SITUACIÓN RELATIVA
    ax_sit = fig.add_axes([0.68, 0.76, 0.28, 0.18])
    ax_sit.set_aspect('equal')
    ax_sit.set_xlim(-1, 9)
    ax_sit.set_ylim(-1.5, 9.5)
    ax_sit.axis('off')
    ax_sit.add_patch(Rectangle((0, 0), 8, 8, fill=False, edgecolor=COLOR_BORDER, lw=1.2))
    ax_sit.text(4, -0.8, "SITUACIÓN RELATIVA S/ESC.", fontsize=7.0, fontweight='bold', color=COLOR_HEADER_RED, ha='center')

    manzanas = [
        (0.5, 0.5, 2.0, 2.0), (3.0, 0.5, 2.0, 2.0), (5.5, 0.5, 2.0, 2.0),
        (0.5, 3.0, 2.0, 2.0), (3.0, 3.0, 2.0, 2.0), (5.5, 3.0, 2.0, 2.0),
        (0.5, 5.5, 2.0, 2.0), (3.0, 5.5, 2.0, 2.0), (5.5, 5.5, 2.0, 2.0)
    ]
    for mx, my, mw, mh in manzanas:
        ax_sit.add_patch(Rectangle((mx, my), mw, mh, facecolor='#F0F0F0', edgecolor='#888888', lw=0.6))

    ax_sit.add_patch(Rectangle((3.8, 3.5), 0.7, 1.2, facecolor='#00838F', edgecolor='#006064', lw=1.0))
    ax_sit.text(4.15, 4.1, "LOTE\nVILLA\nMEDIT.", fontsize=4.8, color='white', fontweight='bold', ha='center', va='center')

    ax_sit.text(1.5, 2.65, "Calle 30", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(1.5, 5.15, "Calle 31", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(2.65, 7.0, "Av. Libertador", rotation=90, fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(5.15, 7.0, "Avenida 4", rotation=90, fontsize=5.0, ha='center', color='#555555')

    # 4. CUADRO DE ÁREAS PROYECTO MEDITERRÁNEO
    ax_areas = fig.add_axes([0.05, 0.69, 0.44, 0.07])
    ax_areas.axis('off')
    ax_areas.add_patch(Rectangle((0, 0), 1, 1, facecolor='#E0F7FA', edgecolor=COLOR_BORDER, lw=1.0))
    ax_areas.text(0.04, 0.78, "ÁREA DE TERRENO: 273,81 m²", fontsize=7.5, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.04, 0.52, "ÁREA DE CONSTRUCCIÓN TOTAL: 372,50 m²", fontsize=7.2, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.04, 0.28, "• Planta Baja (Zona Comercial y Garaje 2,80 m): 149,85 m²", fontsize=5.8, color='#000000')
    ax_areas.text(0.04, 0.10, "• Planta Alta (Villa Mediterránea): 142,20 m²  |  Sótano: 80,45 m²", fontsize=5.8, color='#000000')

    # 5. RETÍCULA Y POLÍGONO UTM CON IMPRONTA MEDITERRÁNEA
    ax_utm = fig.add_axes([0.05, 0.12, 0.90, 0.56])
    ax_utm.set_aspect('equal')
    ax_utm.set_xlim(529745, 529795)
    ax_utm.set_ylim(1141635, 1141685)
    ax_utm.axis('off')

    for n in range(1141640, 1141690, 10):
        ax_utm.plot([529745, 529795], [n, n], color='#D0D0D0', lw=0.6, linestyle='-')
        ax_utm.text(529746, n + 0.6, f"N.={n:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), 
                    fontsize=6.5, fontweight='bold', color='#000000')

    for e in range(529750, 529800, 10):
        ax_utm.plot([e, e], [1141635, 1141685], color='#D0D0D0', lw=0.6, linestyle='-')
        ax_utm.text(e + 0.5, 1141636, f"E.={e:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), 
                    fontsize=6.5, fontweight='bold', color='#000000')

    p1 = (529755.04, 1141664.17)
    p2 = (529764.60, 1141670.33)
    p3 = (529777.07, 1141648.99)
    p4 = (529767.99, 1141643.13)
    poly_pts = [p1, p2, p3, p4, p1]
    pxs = [pt[0] for pt in poly_pts]
    pys = [pt[1] for pt in poly_pts]
    ax_utm.plot(pxs, pys, color='#E00000', lw=2.0, zorder=5)

    for pt, lbl, offset in [(p1, "P-1", (-1.8, 0.5)), (p2, "P-2", (0.5, 0.5)), 
                            (p3, "P-3", (0.5, -1.0)), (p4, "P-4", (-1.8, -1.0))]:
        ax_utm.plot(pt[0], pt[1], marker='o', markersize=5, color='#E00000', zorder=6)
        ax_utm.text(pt[0] + offset[0], pt[1] + offset[1], lbl, fontsize=8.0, fontweight='bold', color='#E00000', zorder=7)

    # Impronta de la Edificación Mediterránea
    b1 = (529756.20, 1141662.30)
    b2 = (529763.80, 1141667.20)
    b3 = (529773.50, 1141650.60)
    b4 = (529765.90, 1141645.70)
    b_pts = [b1, b2, b3, b4, b1]
    ax_utm.plot([p[0] for p in b_pts], [p[1] for p in b_pts], color='#00838F', lw=1.8, linestyle='--', zorder=4)
    ax_utm.add_patch(Polygon([b1, b2, b3, b4], closed=True, facecolor='#E0F7FA', edgecolor='#00838F', hatch='//', alpha=0.5, zorder=3))

    ax_utm.text(529765.0, 1141656.0, "IMPRONTA VILLA MEDITERRÁNEA\n(ARQUERÍA, LOGGIA Y AZOTEA TRANSITABLE)\nÁrea Cubierta = 175,80 m²", 
                fontsize=7.2, fontweight='bold', color='#006064', ha='center', va='center', zorder=7)

    draw_north_arrow(ax_utm, 529788.0, 1141672.0, size=4.0)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 5 generada exitosamente.")


# =============================================================================
# GENERADOR MAESTRO DEL PDF
# =============================================================================
def main():
    out_dir_proj = "Proyecto_Mediterraneo/01_Planos_y_Documentacion"
    out_dir_main = "01_Planos_y_Documentacion"
    os.makedirs(out_dir_proj, exist_ok=True)
    os.makedirs(out_dir_main, exist_ok=True)

    pdf_proj = os.path.join(out_dir_proj, "planos_casa_mediterranea.pdf")
    pdf_main = os.path.join(out_dir_main, "planos_casa_mediterranea.pdf")

    print(f"Generando documento PDF oficial de la Villa Mediterránea: {pdf_proj}...")
    with PdfPages(pdf_proj) as pdf:
        build_sheet_1(pdf)
        build_sheet_2(pdf)
        build_sheet_3(pdf)
        build_sheet_4(pdf)
        build_sheet_5(pdf)

    # Copiar a 01_Planos_y_Documentacion para acceso directo
    with open(pdf_proj, 'rb') as f_in:
        content = f_in.read()
    with open(pdf_main, 'wb') as f_out:
        f_out.write(content)

    print(f"¡Éxito total! Se ha generado '{pdf_proj}' y '{pdf_main}' con las 5 láminas arquitectónicas completas.")

if __name__ == "__main__":
    main()
