"""
Generador del PDF Arquitectónico Oficial del Proyecto Chalet Rústico Alpino
("planos_casa_chalet.pdf")
Diseño bajo la Skill de Arquitecto Especialista en Estilo Rústico y Chalet para CAD.
Basado en las dimensiones de casa_modificaciones.dxf manteniendo intacto el proyecto original.

Contenido de las 5 Láminas (Formato Tabloid 11x17 in):
- Lámina 1: Plano Planta Arquitectónica Distribución - Planta Baja (Zócalo Mampostería) y Sótano
- Lámina 2: Plano Planta Arquitectónica Distribución - Planta Alta Chalet (Timber Frame, Gran Balcón, Chimenea)
- Lámina 3: Plano Estructural y Sistema de Cubierta Alpina (Cerchas de Madera, Vigas Vistas, Canecillos)
- Lámina 4: Plano Fachadas y Elevaciones Rústicas (Principal Av. 4, Lateral con Talud, Posterior)
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
# ESTILOS Y COLORES ARQUITECTÓNICOS CHALET RÚSTICO
# =============================================================================
COLOR_BORDER = '#0000FF'       # Azul normativo de márgenes y recuadros de cajetín
COLOR_HEADER_RED = '#E00000'   # Rojo institucional y títulos de lámina
COLOR_CAJETIN_RED = '#E00000'  # Rojo datos técnicos (Nombre, Ubicación, CI)
COLOR_TEXT_BLACK = '#000000'   # Negro textos de dibujo y cotas
COLOR_STONE_FILL = '#7E8B92'   # Tono piedra natural para zócalo
COLOR_WOOD_WALL = '#8D5B4C'    # Tono madera muros superiores
COLOR_WALL_LINE = '#000000'    # Contorno negro muros
COLOR_DOOR = '#4E3629'         # Carpintería puertas madera
COLOR_WINDOW = '#006680'       # Carpintería ventanas con cuarterones
COLOR_SHUTTER = '#3E2723'      # Contraventanas de madera maciza
COLOR_STAIRS = '#3E2723'       # Escaleras huella madera
COLOR_COL_RED = '#D32F2F'      # Columnas estructurales
COLOR_BEAM_WOOD = '#A0522D'    # Vigas de madera (Sienna / Roble)
COLOR_AXIS_CYAN = '#00838F'    # Líneas de ejes estructurales
COLOR_TERRAIN = '#5D4037'      # Talud y perfil natural de terreno
COLOR_CHIMNEY = '#607D8B'      # Mampostería de chimenea

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

    # Subtítulo de Especialidad Rústica
    ax_frame.text(0.975, 0.972, "PROYECTO CHALET RÚSTICO Y ALPINO (TIMBER FRAME)", 
                  fontsize=9.0, fontweight='bold', color='#4E3629', family='sans-serif', va='top', ha='right')
    ax_frame.text(0.975, 0.954, "DISEÑO PARAMÉTRICO OPENCAD / OPENSCAD", 
                  fontsize=8.0, fontweight='bold', color='#6D4C41', family='sans-serif', va='top', ha='right')

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

    ax_frame.text(0.468, row_top - 0.007, "ESPECIALISTA ARQ. RÚSTICA / DIGITALIZO:", fontsize=6.0, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.468, row_top - 0.019, "ARQ. ESPECIALISTA CHALET & TIMBER FRAME", 
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

def draw_rect_wall(ax, x1, y1, x2, y2, color=COLOR_STONE_FILL, hatch=None):
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

def draw_sliding_door(ax, x1, y1, x2, y2, is_vertical=False):
    """Dibuja puerta corrediza de madera/vidrio."""
    if not is_vertical:
        xmid = (x1 + x2) / 2
        ax.plot([x1, xmid + 0.1], [y1 - 0.02, y1 - 0.02], color='#000000', lw=1.2, zorder=4)
        ax.plot([xmid - 0.1, x2], [y1 + 0.02, y1 + 0.02], color='#000000', lw=1.2, zorder=4)
    else:
        ymid = (y1 + y2) / 2
        ax.plot([x1 - 0.02, x1 - 0.02], [y1, ymid + 0.1], color='#000000', lw=1.2, zorder=4)
        ax.plot([x1 + 0.02, x1 + 0.02], [ymid - 0.1, y2], color='#000000', lw=1.2, zorder=4)

def draw_window_chalet(ax, x1, y1, x2, y2, is_vertical=False, cuarterones=3):
    """Dibuja ventana de estilo chalet con contraventanas (shutters) de madera."""
    if not is_vertical:
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymid = (y1 + y2) / 2
        thick = abs(y2 - y1)
        # Vano
        ax.add_patch(Rectangle((xmin, min(y1, y2)), xmax - xmin, thick, facecolor='#E0F7FA', edgecolor='none', zorder=4))
        ax.plot([xmin, xmin], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmax, xmax], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmin, xmax], [ymid, ymid], color=COLOR_WINDOW, lw=0.9, zorder=5)
        # Cuarterones
        xs = np.linspace(xmin, xmax, cuarterones + 1)
        for px in xs[1:-1]:
            ax.plot([px, px], [min(y1, y2), max(y1, y2)], color=COLOR_WINDOW, lw=0.6, zorder=5)
        # Contraventanas exteriores (Shutters de madera)
        ax.add_patch(Rectangle((xmin - 0.20, min(y1,y2)), 0.18, thick, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.5, zorder=6))
        ax.add_patch(Rectangle((xmax + 0.02, min(y1,y2)), 0.18, thick, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.5, zorder=6))
    else:
        ymin, ymax = min(y1, y2), max(y1, y2)
        xmid = (x1 + x2) / 2
        thick = abs(x2 - x1)
        # Vano
        ax.add_patch(Rectangle((min(x1, x2), ymin), thick, ymax - ymin, facecolor='#E0F7FA', edgecolor='none', zorder=4))
        ax.plot([x1, x2], [ymin, ymin], color='black', lw=0.8, zorder=5)
        ax.plot([x1, x2], [ymax, ymax], color='black', lw=0.8, zorder=5)
        ax.plot([xmid, xmid], [ymin, ymax], color=COLOR_WINDOW, lw=0.9, zorder=5)
        # Cuarterones
        ys = np.linspace(ymin, ymax, cuarterones + 1)
        for py in ys[1:-1]:
            ax.plot([min(x1, x2), max(x1, x2)], [py, py], color=COLOR_WINDOW, lw=0.6, zorder=5)
        # Contraventanas exteriores
        ax.add_patch(Rectangle((min(x1,x2), ymin - 0.20), thick, 0.18, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.5, zorder=6))
        ax.add_patch(Rectangle((min(x1,x2), ymax + 0.02), thick, 0.18, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.5, zorder=6))

def draw_col_hatch(ax, cx, cy, size=0.25, is_wood=False):
    """Dibuja una columna con achurado (rojo hormigón o madera marrón)."""
    s2 = size / 2
    if is_wood:
        rect = Rectangle((cx - s2, cy - s2), size, size, facecolor='#D7CCC8', 
                         edgecolor='#5D4037', linewidth=1.1, hatch='xx', zorder=6)
    else:
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
# LÁMINA 1: PLANTA BAJA (ZÓCALO MAMPOSTERÍA) Y SÓTANO
# =============================================================================
def build_sheet_1(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA DISTRIBUCIÓN", 
                     "PLANTA BAJA (ZÓCALO DE MAMPOSTERÍA RÚSTICA) Y SÓTANO.", escala="1:75")

    # PLANTA BAJA
    ax_pb = fig.add_axes([0.08, 0.44, 0.84, 0.48])
    ax_pb.set_aspect('equal')
    ax_pb.set_xlim(-2.0, 11.5)
    ax_pb.set_ylim(-2.0, 24.5)
    ax_pb.axis('off')

    ax_pb.text(4.5, -1.2, "PLANTA BAJA - ZÓCALO RÚSTICO Y GARAJE AMPLIADO (2,80 m LIBRES)", 
               fontsize=9.5, fontweight='bold', ha='center', va='top')
    ax_pb.plot([0.0, 9.0], [-1.55, -1.55], color='black', lw=1.2)
    draw_north_arrow(ax_pb, 10.0, 20.0, size=1.5)

    # 1. Muro Propio Izquierdo (Eje 0)
    draw_rect_wall(ax_pb, 0.15, 0.00, 0.30, 21.71, color=COLOR_STONE_FILL, hatch='...')
    ax_pb.text(0.225, 22.2, "MURO PROPIO\n(EJE 0)", fontsize=6.2, ha='center', va='bottom', color=COLOR_COL_RED, fontweight='bold')

    # 2. Fachada Frontal Avenida 4 (Y: 21.56 a 21.71 m)
    draw_rect_wall(ax_pb, 0.15, 21.56, 0.40, 21.71, color=COLOR_STONE_FILL)
    ax_pb.plot([0.40, 2.90], [21.71, 21.71], color='#5D4037', lw=2.0)
    ax_pb.text(1.65, 21.90, "PORTÓN GARAJE MADERA (2,50 m)", fontsize=6.2, ha='center', va='bottom', fontweight='bold', color='#4E3629')
    draw_rect_wall(ax_pb, 2.90, 21.56, 3.25, 21.71, color=COLOR_STONE_FILL)

    # Vitrinas Rústicas con parteluces de madera
    draw_window_chalet(ax_pb, 3.25, 21.56, 5.80, 21.71, cuarterones=4)
    draw_rect_wall(ax_pb, 5.80, 21.56, 6.20, 21.71, color=COLOR_STONE_FILL)
    draw_window_chalet(ax_pb, 6.20, 21.56, 8.85, 21.71, cuarterones=4)
    draw_rect_wall(ax_pb, 8.85, 21.56, 9.15, 21.71, color=COLOR_STONE_FILL)

    # 3. Muro Medianero Eje 1 (X = 3.10 m) - Garaje Ampliado a 2,80 m libres!
    draw_rect_wall(ax_pb, 3.10, 5.65, 3.25, 21.71, color=COLOR_STONE_FILL)
    ax_pb.text(1.70, 13.5, "GARAJE TECHADO DOBLE\nAncho Libre: 2,80 m\n(Apertura Cómoda de Puertas)", 
               fontsize=7.5, ha='center', va='center', fontweight='bold', color='#1B5E20')
    
    # Silueta de coche y radio de giro de puerta
    ax_pb.add_patch(Rectangle((0.70, 7.50), 1.75, 4.40, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.8, linestyle='--'))
    ax_pb.text(1.57, 9.70, "VEHÍCULO 1 (Sedán / SUV)\nAncho 1,80 m", fontsize=5.8, ha='center', va='center', color='#2E7D32')
    ax_pb.plot([0.70, 0.70 - 0.35], [9.20, 9.70], color='#2E7D32', lw=0.8) # Puerta abierta
    ax_pb.text(0.35, 9.70, "Puerta\n0,85m holgura", fontsize=5.0, ha='center', color='#2E7D32')

    ax_pb.add_patch(Rectangle((0.70, 14.50), 1.75, 4.40, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.8, linestyle='--'))
    ax_pb.text(1.57, 16.70, "VEHÍCULO 2", fontsize=5.8, ha='center', va='center', color='#2E7D32')

    # Puerta privada al fondo del garaje
    draw_rect_wall(ax_pb, 3.10, 4.75, 3.25, 5.65, color=COLOR_STONE_FILL)
    draw_door_swing(ax_pb, 3.10, 4.75, 0.90, 0, 90)

    # Gran Salón Comercial (Zócalo Mampostería)
    ax_pb.text(6.15, 13.5, "GRAN LOCAL COMERCIAL RÚSTICO\nÁrea Libre: 91,00 m² (5,75 x 16,00 m)\nAcabado de Muros: Mampostería de Piedra y Cantería", 
               fontsize=7.5, ha='center', va='center', fontweight='bold', color='#37474F')

    # Muro Lateral Derecho Eje 3 (X = 9.00 a 9.15 m)
    draw_rect_wall(ax_pb, 9.00, 3.50, 9.15, 21.71, color=COLOR_STONE_FILL)

    # Escalera hacia Planta Alta
    draw_rect_wall(ax_pb, 6.20, 0.00, 6.35, 3.65, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_pb, 7.35, 0.00, 7.50, 3.65, color=COLOR_STONE_FILL)
    for sy in np.linspace(0.25, 3.40, 11):
        ax_pb.plot([6.35, 7.35], [sy, sy], color=COLOR_STAIRS, lw=0.7)
    ax_pb.annotate('', xy=(6.85, 3.20), xytext=(6.85, 0.50),
                   arrowprops=dict(facecolor='black', edgecolor='black', width=1.0, headwidth=4.0))
    ax_pb.text(6.85, 1.85, "SUBE AL CHALET", rotation=90, fontsize=5.5, ha='center', va='center', fontweight='bold')

    # Baño de Servicio Local Comercial
    draw_rect_wall(ax_pb, 6.20, 3.50, 9.15, 3.65, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_pb, 6.20, 5.65, 9.15, 5.80, color=COLOR_STONE_FILL)
    draw_door_swing(ax_pb, 6.35, 5.65, 0.80, 270, 180)
    ax_pb.text(7.65, 4.65, "Baño Servicio\n2,80 x 1,85 m", fontsize=6.5, ha='center', va='center')

    # Depósito / Oficina de Planta Baja
    draw_rect_wall(ax_pb, 0.15, 0.00, 6.20, 0.15, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_pb, 0.15, 3.50, 3.10, 3.65, color=COLOR_STONE_FILL)
    draw_door_swing(ax_pb, 3.25, 3.65, 0.85, 180, 90)
    ax_pb.text(4.50, 1.85, "Depósito / Logística\n2,95 x 3,35 m", fontsize=6.8, ha='center', va='center', fontweight='bold')

    # Columnas Estructurales Planta Baja (Zona Comercial y Garaje) según casa_modificaciones.dxf
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
    draw_dim_h(ax_pb, 0.30, 3.10, 22.8, "2,80 (Garaje)", offset=0.0)
    draw_dim_h(ax_pb, 3.10, 9.00, 22.8, "5,90 (Local)", offset=0.0)
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
    draw_rect_wall(ax_sot, 0.30, 0.15, 6.40, 0.30, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_sot, 0.30, 0.15, 0.45, 8.15, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_sot, 0.30, 8.00, 9.15, 8.15, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_sot, 9.00, 3.50, 9.15, 8.15, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_sot, 6.25, 0.15, 6.40, 8.15, color=COLOR_STONE_FILL)
    draw_rect_wall(ax_sot, 0.45, 3.50, 6.25, 3.65, color=COLOR_STONE_FILL)

    ax_sot.text(3.3, 5.8, "Cava - Depósito Rústico / Sala Subterránea\n5,80 x 4,35 m", fontsize=6.8, ha='center', va='center', fontweight='bold')
    ax_sot.text(7.6, 5.8, "Área Técnica / Taller\n2,65 x 4,35 m", fontsize=6.8, ha='center', va='center')
    ax_sot.text(3.3, 1.8, "Bodega de Montaña / Almacén\n5,80 x 3,20 m", fontsize=6.8, ha='center', va='center')

    for cx, cy in [(0.375, 8.075), (6.325, 8.075), (9.075, 8.075),
                   (0.375, 3.575), (6.325, 3.575), (9.075, 3.575),
                   (0.375, 0.225), (6.325, 0.225)]:
        draw_col_hatch(ax_sot, cx, cy, size=0.35)

    draw_dim_h(ax_sot, 0.30, 6.40, 8.8, "6,10")
    draw_dim_h(ax_sot, 6.40, 9.15, 8.8, "2,75")
    draw_dim_v(ax_sot, -0.4, 0.15, 8.15, "8,00 m")

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 1 generada exitosamente.")

# =============================================================================
# LÁMINA 2: PLANTA ALTA CHALET (TIMBER FRAME, BALCÓN Y CHIMENEA)
# =============================================================================
def build_sheet_2(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA DISTRIBUCIÓN - PLANTA ALTA", 
                     "CHALET RÚSTICO Y ALPINO (TIMBER FRAME, BALCONADA Y CHIMENEA).", escala="1:75")

    ax = fig.add_axes([0.12, 0.12, 0.76, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 12.0)
    ax.set_ylim(-2.5, 25.0)
    ax.axis('off')

    ax.text(4.5, -1.3, "PLANTA ALTA - RESIDENCIA CHALET CON TECHOS DE VIGAS VISTAS Y BALCÓN CORRIDO", 
            fontsize=9.5, fontweight='bold', ha='center', va='top')
    ax.plot([0.0, 9.0], [-1.65, -1.65], color='black', lw=1.2)
    draw_north_arrow(ax, 10.5, 21.0, size=1.5)

    # 1. Gran Balcón Corrido Alpino hacia Avenida 4 (Y: 21.71 a 23.31 m)
    # Voladizo sobre vigas pasantes
    balcon_poly = [(0.15, 21.71), (9.15, 21.71), (9.15, 23.31), (0.15, 23.31)]
    ax.add_patch(Polygon(balcon_poly, closed=True, facecolor='#D7CCC8', edgecolor='#5D4037', lw=1.2, zorder=2))
    # Vigas pasantes de soporte del balcón
    for vx in np.linspace(0.40, 8.90, 8):
        ax.plot([vx, vx], [21.00, 23.31], color='#4E3629', lw=2.0, zorder=3)
    # Barandilla de madera con Cruz de San Andrés
    ax.plot([0.15, 9.15], [23.31, 23.31], color='#3E2723', lw=2.0, zorder=5)
    for bx in np.linspace(0.15, 8.15, 8):
        # Módulo de baranda con X de San Andrés
        ax.plot([bx, bx + 1.0], [23.31, 23.31], color='#3E2723', lw=1.5, zorder=6)
        ax.plot([bx, bx], [23.05, 23.31], color='#3E2723', lw=1.0, zorder=6)
        ax.plot([bx, bx + 1.0], [23.05, 23.31], color='#5D4037', lw=0.7, zorder=6)
        ax.plot([bx + 1.0, bx], [23.05, 23.31], color='#5D4037', lw=0.7, zorder=6)
    ax.text(4.65, 23.50, "GRAN BALCÓN CORRIDO ALPINO (9,00 x 1,60 m)\nBarandilla en Cruz de San Andrés y Canecillos Vistos", 
            fontsize=6.8, ha='center', va='bottom', fontweight='bold', color='#3E2723')

    # 2. Fachada Frontal (Y = 21.71 m)
    # Sala Great Room (X: 0.15 a 4.50 m)
    draw_rect_wall(ax, 0.15, 21.56, 0.60, 21.71, color=COLOR_WOOD_WALL)
    draw_window_chalet(ax, 0.60, 21.56, 2.40, 21.71, cuarterones=4)
    draw_rect_wall(ax, 2.40, 21.56, 2.90, 21.71, color=COLOR_WOOD_WALL)
    # Puerta francesa hacia balcón
    draw_door_swing(ax, 2.90, 21.71, 0.90, 90, 180)
    draw_rect_wall(ax, 3.80, 21.56, 5.00, 21.71, color=COLOR_WOOD_WALL)
    # Suite Principal (X: 5.00 a 9.15 m)
    draw_door_swing(ax, 5.00, 21.71, 0.90, 90, 0)
    draw_rect_wall(ax, 5.90, 21.56, 6.40, 21.71, color=COLOR_WOOD_WALL)
    draw_window_chalet(ax, 6.40, 21.56, 8.60, 21.71, cuarterones=4)
    draw_rect_wall(ax, 8.60, 21.56, 9.15, 21.71, color=COLOR_WOOD_WALL)

    # 3. Muro Propio Izquierdo (Eje 0) en madera machihembrada
    draw_rect_wall(ax, 0.15, 0.00, 0.35, 21.71, color=COLOR_WOOD_WALL)
    ax.text(0.25, 11.0, "ESTRUCTURA TIMBER FRAME Y MACHIHEMBRADO", rotation=90, 
            fontsize=5.8, ha='center', va='center', color='white', fontweight='bold')

    # 4. CHIMENEA RÚSTICA MONUMENTAL DE PIEDRA (Núcleo Central en Salón)
    chim_poly = [(0.35, 17.20), (1.55, 17.20), (1.55, 18.80), (0.35, 18.80)]
    ax.add_patch(Polygon(chim_poly, closed=True, facecolor=COLOR_CHIMNEY, edgecolor='black', lw=1.2, hatch='OO', zorder=5))
    ax.add_patch(Rectangle((0.35, 17.50), 0.60, 1.00, facecolor='#212121', edgecolor='black', lw=0.8, zorder=6))
    ax.text(0.95, 18.00, "CHIMENEA\nRÚSTICA\nDE PIEDRA", fontsize=5.8, ha='center', va='center', fontweight='bold', color='white', zorder=7)

    # Gran Salón Great Room (Techo Catedral)
    ax.text(2.65, 19.50, "SALA GREAT ROOM\nTecho Catedral Visto (Pendiente 38°)\nVigas Expuestas de Madera Maciza", 
            fontsize=7.2, ha='center', va='center', fontweight='bold', color='#3E2723')

    # Cocina Rústica de Montaña y Comedor Familiar
    ax.text(2.65, 14.80, "COMEDOR RÚSTICO Y COCINA ALPINA\nIsla Central de Madera Maciza\nAcabado de Troncos y Cantería", 
            fontsize=7.0, ha='center', va='center', fontweight='bold', color='#4E3629')
    # Isla maciza de cocina
    ax.add_patch(Rectangle((1.50, 13.00), 2.60, 0.95, facecolor='#A1887F', edgecolor='#3E2723', lw=1.1, zorder=4))
    ax.text(2.80, 13.475, "ISLA CENTRAL (2,60 x 0,95 m)", fontsize=6.0, ha='center', va='center', color='#3E2723', fontweight='bold')

    # División Living / Dormitorios
    draw_rect_wall(ax, 0.35, 11.85, 4.80, 12.00, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 3.80, 12.00, 0.85, 180, 270)

    # Master Suite (Dormitorio Principal)
    ax.text(7.00, 18.50, "MASTER SUITE ALPINA\n4,15 x 3,85 m\nVigas de Techo Expuestas\nAcceso Directo al Balcón", 
            fontsize=7.2, ha='center', va='center', fontweight='bold', color='#3E2723')
    # Vestidor / Walk-in Closet
    draw_rect_wall(ax, 4.80, 16.40, 9.15, 16.55, color=COLOR_WOOD_WALL)
    draw_rect_wall(ax, 4.80, 16.55, 4.95, 21.56, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 6.80, 16.55, 0.80, 0, 90)
    ax.text(5.90, 15.20, "Baño Master Suite\nPiedra Natural\n2,20 x 2,40 m", fontsize=6.2, ha='center', va='center')
    ax.text(8.00, 15.20, "Vestidor Rústico\n1,95 x 2,40 m", fontsize=6.2, ha='center', va='center')
    draw_rect_wall(ax, 7.00, 14.00, 7.15, 16.40, color=COLOR_WOOD_WALL)

    # Habitación 2 (Alpina)
    draw_rect_wall(ax, 0.35, 6.80, 4.80, 6.95, color=COLOR_WOOD_WALL)
    draw_rect_wall(ax, 4.80, 6.80, 4.95, 12.00, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 3.80, 6.95, 0.85, 90, 180)
    ax.text(2.50, 9.40, "HABITACIÓN 2\n3,85 x 4,85 m\nTecho Inclinado de Madera", 
            fontsize=7.0, ha='center', va='center', fontweight='bold')
    draw_window_chalet(ax, 0.15, 8.50, 0.35, 10.30, is_vertical=True, cuarterones=3)

    # Habitación 3 (Alpina)
    draw_rect_wall(ax, 4.80, 8.00, 9.15, 8.15, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 5.00, 8.15, 0.85, 90, 0)
    ax.text(7.00, 10.20, "HABITACIÓN 3\n4,20 x 3,70 m\nContraventanas Rústicas", 
            fontsize=7.0, ha='center', va='center', fontweight='bold')
    draw_window_chalet(ax, 9.00, 9.20, 9.15, 11.00, is_vertical=True, cuarterones=3)

    # Baño Familiar Principal
    draw_rect_wall(ax, 4.80, 3.50, 9.15, 3.65, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 5.00, 3.65, 0.80, 90, 0)
    ax.text(7.00, 5.80, "Baño Familiar de Piedra\nLavamanos en Madera Rústica\n4,20 x 2,15 m", fontsize=6.5, ha='center', va='center')

    # Escalera de Acceso desde PB
    draw_rect_wall(ax, 6.20, 0.00, 6.35, 3.50, color=COLOR_WOOD_WALL)
    draw_rect_wall(ax, 7.35, 0.00, 7.50, 3.50, color=COLOR_WOOD_WALL)
    for sy in np.linspace(0.25, 3.25, 10):
        ax.plot([6.35, 7.35], [sy, sy], color=COLOR_STAIRS, lw=0.7)
    ax.text(6.85, 1.75, "LLEGA DE P.B.", rotation=90, fontsize=5.5, ha='center', va='center')

    # Terraza Mirador Posterior (Vista Montaña) y Lavandería Rústica
    draw_rect_wall(ax, 0.35, 0.00, 0.35, 3.50, color=COLOR_WOOD_WALL)
    draw_rect_wall(ax, 0.35, 3.50, 4.80, 3.65, color=COLOR_WOOD_WALL)
    draw_door_swing(ax, 3.80, 3.65, 0.85, 270, 180)
    ax.text(2.50, 1.75, "TERRAZA MIRADOR POSTERIOR\nPérgola de Vigas y Lavadero\n4,45 x 3,50 m", 
            fontsize=6.8, ha='center', va='center', fontweight='bold', color='#3E2723')
    ax.plot([0.35, 6.20], [0.00, 0.00], color='#5D4037', lw=1.5, linestyle='--')

    # Muro Lateral Derecho Eje 3 (X = 9.00 a 9.15 m)
    draw_rect_wall(ax, 9.00, 3.50, 9.15, 21.71, color=COLOR_WOOD_WALL)

    # Columnas estructurales y postes de madera maciza (Timber Frame) según casa_modificaciones.dxf
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
        draw_col_hatch(ax, cx, cy, size=0.25, is_wood=True)

    # Cotas Planta Alta
    draw_dim_h(ax, 0.15, 9.15, 24.3, "9,00 m (Ancho Total Frente Balcón)", offset=0.0)
    draw_dim_h(ax, 0.15, 4.80, 22.0, "4,65 m (Zona Social)", offset=0.0)
    draw_dim_h(ax, 4.80, 9.15, 22.0, "4,35 m (Master Suite)", offset=0.0)
    draw_dim_v(ax, -1.0, 0.00, 21.71, "21,71 m (Cuerpo Casa)", offset=0.0)
    draw_dim_v(ax, -1.8, 0.00, 23.31, "23,31 m (Total con Balcón)", offset=0.0)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 2 generada exitosamente.")

# =============================================================================
# LÁMINA 3: PLANO ESTRUCTURAL Y SISTEMA DE CUBIERTA ALPINA
# =============================================================================
def build_sheet_3(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO ESTRUCTURAL Y SISTEMA DE CUBIERTA ALPINA", 
                     "ENTRAMADO DE VIGAS VISTAS, CERCHAS A DOS AGUAS Y TIJERAS DE MADERA.", escala="1:75")

    ax = fig.add_axes([0.12, 0.12, 0.76, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-3.0, 12.0)
    ax.set_ylim(-2.5, 25.5)
    ax.axis('off')

    ax.text(4.5, -1.3, "SISTEMA ESTRUCTURAL HÍBRIDO: ZÓCALO DE HORMIGÓN/PIEDRA + TIMBER FRAME + CERCHAS 38°", 
            fontsize=9.0, fontweight='bold', ha='center', va='top')
    ax.plot([0.0, 9.0], [-1.65, -1.65], color='black', lw=1.2)
    draw_north_arrow(ax, 10.5, 21.0, size=1.5)

    # 1. Ejes Estructurales Transversales (Ejes 0, 1, 2, 3) según casa_modificaciones.dxf
    ejes_x = [(0.275, '0'), (2.825, '1'), (5.925, '2'), (9.075, '3')]
    for ex, label in ejes_x:
        ax.plot([ex, ex], [-1.0, 24.0], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((ex, 24.4), 0.35, facecolor='white', edgecolor=COLOR_AXIS_CYAN, lw=0.9, zorder=5))
        ax.text(ex, 24.4, label, fontsize=8.0, fontweight='bold', color=COLOR_AXIS_CYAN, ha='center', va='center', zorder=6)

    # Ejes Estructurales Longitudinales (Ejes A0 a G y Sótano) según casa_modificaciones.dxf
    ejes_y = [
        (21.585, 'A0'), (18.575, 'A'), (16.325, 'B'), (14.625, 'C'),
        (12.025, 'D'), (8.875, 'E'), (6.575, 'F'), (3.575, 'G'), (0.075, 'SOT')
    ]
    for ey, label in ejes_y:
        ax.plot([-1.5, 10.5], [ey, ey], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((-1.9, ey), 0.35, facecolor='white', edgecolor=COLOR_AXIS_CYAN, lw=0.9, zorder=5))
        ax.text(-1.9, ey, label, fontsize=7.5, fontweight='bold', color=COLOR_AXIS_CYAN, ha='center', va='center', zorder=6)

    # Líneas de conexión de retícula estructural
    for i in range(len(ejes_x)-1):
        x_a = ejes_x[i][0]
        x_b = ejes_x[i+1][0]
        for ey, _ in ejes_y:
            ax.plot([x_a, x_b], [ey, ey], color='#D5D5D5', lw=0.8, zorder=1)

    # 2. COLUMNAS ESTRUCTURALES P.B. Y P.A. (31 unidades de 25x25 cm según casa_modificaciones.dxf)
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

    # 2. Cumbrera Central del Techo Alpino a Dos Aguas (X = 4.65 m, Z = +9.72 m)
    ax.plot([4.65, 4.65], [-1.0, 23.5], color='#D50000', lw=2.2, linestyle='-', zorder=5)
    ax.text(4.65, 24.0, "EJE CUMBRERA PRINCIPAL (Z = +9,72 m)", fontsize=7.0, ha='center', va='bottom', color='#D50000', fontweight='bold')

    # 3. Pares de Techo (Rafters) y Correas de Madera cada 1.20 m
    for ry in np.linspace(0.0, 22.0, 19):
        # Vigas transversales cayendo desde cumbrera hacia ambos aleros (voladizo de 1.10 m)
        ax.plot([-0.95, 10.25], [ry, ry], color=COLOR_BEAM_WOOD, lw=0.9, zorder=3)
        # Canecillos expuestos en los extremos
        ax.plot([-0.95, -0.65], [ry, ry], color='#3E2723', lw=2.2, zorder=4)
        ax.plot([9.95, 10.25], [ry, ry], color='#3E2723', lw=2.2, zorder=4)

    # 4. Cerchas Alpinas Principales (King Post / Tijera) sobre ejes
    cerchas_y = [0.075, 6.875, 11.925, 16.475, 21.635]
    for cy in cerchas_y:
        ax.plot([-0.95, 10.25], [cy, cy], color='#3E2723', lw=3.0, zorder=6)
        ax.text(10.45, cy, f"CERCHA TIPO ALPINA C-{cerchas_y.index(cy)+1} (Pendiente 38°)", 
                fontsize=5.5, va='center', fontweight='bold', color='#3E2723')

    # 5. Voladizo Perimetral de Techo (Línea de Aleros)
    alero_poly = [(-0.95, -1.00), (10.25, -1.00), (10.25, 23.50), (-0.95, 23.50)]
    ax.add_patch(Polygon(alero_poly, closed=True, fill=False, edgecolor='#FF6F00', lw=1.2, linestyle='--', zorder=4))
    ax.text(10.35, 12.0, "LÍNEA DE ALERO Y VOLADIZO (1,10 m lateral / 1,20 m frontal)", 
            rotation=270, fontsize=6.2, color='#FF6F00', fontweight='bold', ha='center', va='bottom')

    # 6. Chimenea de Piedra en Planta Estructural
    chim_poly = [(0.35, 17.20), (1.55, 17.20), (1.55, 18.80), (0.35, 18.80)]
    ax.add_patch(Polygon(chim_poly, closed=True, facecolor=COLOR_CHIMNEY, edgecolor='black', lw=1.5, hatch='///', zorder=7))
    ax.text(0.95, 18.00, "NÚCLEO\nCHIMENEA", fontsize=5.8, ha='center', va='center', fontweight='bold', color='white', zorder=8)

    # 7. Cuadro de Especificaciones Estructurales
    ax.add_patch(Rectangle((-0.8, -0.2), 10.5, 3.4, facecolor='#FFFDE7', edgecolor=COLOR_BORDER, lw=1.0, zorder=8))
    ax.text(-0.5, 2.9, "ESPECIFICACIONES DEL SISTEMA ESTRUCTURAL Y CUBIERTA CHALET:", 
            fontsize=7.2, fontweight='bold', color=COLOR_BORDER, zorder=9)
    ax.text(-0.5, 2.3, "• Cubierta Alpina: Cerchas de madera maciza (Escuadría 8\"x4\"), pendiente 38° (78%), cumbrera a Z = +9,72 m.", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 1.7, "• Voladizos y Canecillos: Aleros de 1,10 m en laterales y 1,20 m en frontón con pares vistos de 6\"x3\" @ 0,60 m.", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 1.1, "• Entramado Superior: Muros Timber Frame con montantes de pino tratado 4\"x4\" y revestimiento machihembrado.", 
            fontsize=6.5, color='#000000', zorder=9)
    ax.text(-0.5, 0.5, "• Zócalo y Sótano: Concreto f'c = 250 kg/cm² con enchape de mampostería de piedra natural y esquisto de 35 cm.", 
            fontsize=6.5, color='#000000', zorder=9)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 3 generada exitosamente.")

# =============================================================================
# LÁMINA 4: PLANO FACHADAS Y ELEVACIONES RÚSTICAS (17x11 in)
# =============================================================================
def build_sheet_4(pdf):
    fig = plt.figure(figsize=(17, 11), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO FACHADAS Y ELEVACIONES RÚSTICAS (CHALET ALPINO)", 
                     "FACHADA PRINCIPAL (AV. 4) — FACHADA LATERAL CON TALUD — FACHADA POSTERIOR.", 
                     escala="1:75", is_landscape=True)

    # 1. FACHADA PRINCIPAL (AVENIDA 4)
    ax_prin = fig.add_axes([0.05, 0.52, 0.43, 0.38])
    ax_prin.set_aspect('equal')
    ax_prin.set_xlim(-2.5, 11.5)
    ax_prin.set_ylim(-1.5, 11.5)
    ax_prin.axis('off')

    ax_prin.text(4.5, -0.7, "FACHADA PRINCIPAL (AVENIDA 4) - ESTILO CHALET ALPINO", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_prin.plot([0.5, 8.5], [-1.05, -1.05], color='black', lw=1.0)
    ax_prin.plot([-2.0, 11.0], [0.0, 0.0], color='#000000', lw=1.5)

    # Planta Baja: Zócalo de Mampostería de Piedra (Z: 0.00 a 3.00 m)
    ax_prin.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor=COLOR_STONE_FILL, edgecolor='#000000', lw=1.2, hatch='..'))
    
    # Portón Garaje Madera Rústica
    ax_prin.add_patch(Rectangle((0.35, 0.00), 2.70, 2.30, facecolor='#5D4037', edgecolor='#000000', lw=1.1))
    for gy in np.linspace(0.25, 2.05, 7):
        ax_prin.plot([0.35, 3.05], [gy, gy], color='#8D6E63', lw=0.8)
    ax_prin.text(1.70, 1.15, "PORTÓN GARAJE\nTABLONES MACIZOS", fontsize=5.8, ha='center', va='center', color='white', fontweight='bold')

    # Vitrinas Rústicas con parteluces de madera
    for vx, lbl in [(3.35, "VITRINA 1"), (6.35, "VITRINA 2")]:
        ax_prin.add_patch(Rectangle((vx, 0.00), 2.50, 2.40, facecolor='#E0F7FA', edgecolor='#3E2723', lw=1.2))
        ax_prin.plot([vx + 1.25, vx + 1.25], [0.00, 2.40], color='#3E2723', lw=1.0)
        ax_prin.plot([vx, vx + 2.50], [1.20, 1.20], color='#3E2723', lw=0.8)
        ax_prin.text(vx + 1.25, 0.60, lbl, fontsize=5.5, ha='center', va='center', color='#006064')

    # Planta Alta: Fachada de Madera Machihembrada (Z: 3.00 a 5.40 m)
    ax_prin.add_patch(Rectangle((0.15, 3.00), 9.00, 2.40, facecolor=COLOR_WOOD_WALL, edgecolor='#000000', lw=1.2))
    for my in np.linspace(3.20, 5.20, 10):
        ax_prin.plot([0.15, 9.15], [my, my], color='#5D4037', lw=0.5)

    # Ventana Master Suite con cuarterones y contraventanas (Shutters)
    ax_prin.add_patch(Rectangle((6.20, 3.60), 2.20, 1.30, facecolor='#E0F7FA', edgecolor='#3E2723', lw=1.0))
    ax_prin.plot([7.30, 7.30], [3.60, 4.90], color='#3E2723', lw=0.8)
    ax_prin.plot([6.20, 8.40], [4.25, 4.25], color='#3E2723', lw=0.8)
    # Contraventanas
    ax_prin.add_patch(Rectangle((5.85, 3.60), 0.35, 1.30, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.7))
    ax_prin.add_patch(Rectangle((8.40, 3.60), 0.35, 1.30, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.7))
    ax_prin.text(7.30, 4.60, "Ventana & Contraventanas", fontsize=5.0, ha='center', color='#006064')

    # Gran Balcón Corrido Alpino (Z: 3.00 a 4.10 m)
    ax_prin.add_patch(Rectangle((0.00, 2.90), 9.30, 0.15, facecolor='#3E2723', edgecolor='black', lw=1.0)) # Losa balcón
    # Canecillos de soporte de balcón
    for bx in np.linspace(0.40, 8.90, 8):
        ax_prin.add_patch(Polygon([(bx-0.08, 2.40), (bx+0.08, 2.40), (bx+0.08, 2.90), (bx-0.08, 2.90)], closed=True, facecolor='#4E3629', edgecolor='black', lw=0.6))
    # Barandilla con Cruz de San Andrés
    ax_prin.plot([0.00, 9.30], [4.00, 4.00], color='#3E2723', lw=1.5)
    for bx in np.linspace(0.00, 8.30, 8):
        ax_prin.plot([bx, bx + 1.0], [3.05, 4.00], color='#3E2723', lw=0.8)
        ax_prin.plot([bx + 1.0, bx], [3.05, 4.00], color='#3E2723', lw=0.8)
        ax_prin.plot([bx, bx], [3.05, 4.00], color='#3E2723', lw=1.0)
    ax_prin.text(4.65, 3.50, "BALCÓN CORRIDO ALPINO (CRUZ DE SAN ANDRÉS)", fontsize=5.8, ha='center', va='center', fontweight='bold', color='white')

    # Frontón Triangular de la Cubierta Alpina (Z: 5.40 a 9.72 m) - Pendiente 38°
    fronton_poly = [(0.15, 5.40), (9.15, 5.40), (4.65, 8.92)]
    ax_prin.add_patch(Polygon(fronton_poly, closed=True, facecolor='#6D4C41', edgecolor='#000000', lw=1.2))
    # Ventana de buhardilla / ático
    ax_prin.add_patch(Circle((4.65, 6.80), 0.55, facecolor='#E0F7FA', edgecolor='#3E2723', lw=1.1))
    ax_prin.plot([4.10, 5.20], [6.80, 6.80], color='#3E2723', lw=0.8)
    ax_prin.plot([4.65, 4.65], [6.25, 7.35], color='#3E2723', lw=0.8)

    # Techo a Dos Aguas con Gran Alero Voladizo (1,10 m lateral, 1,20 m frontal)
    techo_left = [(-0.95, 5.40), (4.65, 9.72), (4.65, 9.45), (-0.95, 5.15)]
    techo_right = [(10.25, 5.40), (4.65, 9.72), (4.65, 9.45), (10.25, 5.15)]
    ax_prin.add_patch(Polygon(techo_left, closed=True, facecolor='#37474F', edgecolor='black', lw=1.2))
    ax_prin.add_patch(Polygon(techo_right, closed=True, facecolor='#263238', edgecolor='black', lw=1.2))
    
    # Canecillos expuestos bajo el alero
    for cx in np.linspace(-0.8, 4.2, 6):
        cz = 5.40 + (cx - (-0.95)) * 0.78
        ax_prin.plot([cx, cx], [cz - 0.25, cz], color='#8D6E63', lw=1.5)
    for cx in np.linspace(5.1, 10.1, 6):
        cz = 9.72 - (cx - 4.65) * 0.78
        ax_prin.plot([cx, cx], [cz - 0.25, cz], color='#8D6E63', lw=1.5)

    # Chimenea Monumental de Piedra coronando la cubierta
    chim_front = [(1.00, 6.50), (2.00, 6.50), (2.00, 10.50), (1.00, 10.50)]
    ax_prin.add_patch(Polygon(chim_front, closed=True, facecolor=COLOR_CHIMNEY, edgecolor='black', lw=1.2, hatch='OO'))
    # Losa de remate de chimenea
    ax_prin.add_patch(Rectangle((0.85, 10.50), 1.30, 0.15, facecolor='#37474F', edgecolor='black', lw=1.0))
    ax_prin.text(1.50, 10.85, "CHIMENEA", fontsize=5.5, ha='center', va='bottom', color='#37474F', fontweight='bold')

    # Cotas de Nivel Fachada Principal
    ax_prin.text(-1.4, 0.05, "N.P.T. ±0,00", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 3.05, "N.P.T. +3,00 (Chalet)", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 5.40, "N.A. +5,40 (Aleros)", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-1.4, 9.72, "N.C. +9,72 (Cumbrera)", fontsize=6.2, fontweight='bold', ha='right')


    # 2. FACHADA POSTERIOR
    ax_post = fig.add_axes([0.52, 0.52, 0.43, 0.38])
    ax_post.set_aspect('equal')
    ax_post.set_xlim(-2.5, 11.5)
    ax_post.set_ylim(-4.5, 11.5)
    ax_post.axis('off')

    ax_post.text(4.5, -3.7, "FACHADA POSTERIOR (SÓTANO - ZÓCALO - CHALET)", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_post.plot([0.5, 8.5], [-4.05, -4.05], color='black', lw=1.0)

    # Sótano
    ax_post.add_patch(Rectangle((0.30, -2.55), 8.85, 2.55, facecolor='#546E7A', edgecolor='#000000', lw=1.0, hatch='..'))
    ax_post.add_patch(Rectangle((1.00, -1.60), 1.80, 1.10, facecolor='#E0F7FA', edgecolor='#3E2723', lw=0.8))
    ax_post.text(1.90, -1.05, "Ventana Cava", fontsize=5.5, ha='center', va='center')

    # Planta Baja (Zócalo)
    ax_post.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor=COLOR_STONE_FILL, edgecolor='#000000', lw=1.0, hatch='..'))
    ax_post.add_patch(Rectangle((0.80, 1.15), 1.80, 1.45, facecolor='#E0F7FA', edgecolor='#3E2723', lw=0.8))
    ax_post.text(1.70, 1.85, "Ventana Depósito", fontsize=5.5, ha='center', va='center')

    # Planta Alta y Terraza Posterior
    ax_post.add_patch(Rectangle((0.15, 3.00), 9.00, 2.40, facecolor=COLOR_WOOD_WALL, edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((0.80, 3.80), 1.80, 1.20, facecolor='#E0F7FA', edgecolor='#3E2723', lw=0.8))
    ax_post.text(1.70, 4.40, "Ventana Terraza", fontsize=5.5, ha='center', va='center')
    ax_post.add_patch(Rectangle((5.50, 3.80), 2.20, 1.20, facecolor='#E0F7FA', edgecolor='#3E2723', lw=0.8))
    ax_post.text(6.60, 4.40, "Ventana Dormitorio", fontsize=5.5, ha='center', va='center')

    # Frontón Posterior y Techo
    fronton_p = [(0.15, 5.40), (9.15, 5.40), (4.65, 8.92)]
    ax_post.add_patch(Polygon(fronton_p, closed=True, facecolor='#6D4C41', edgecolor='#000000', lw=1.2))
    ax_post.add_patch(Polygon(techo_left, closed=True, facecolor='#37474F', edgecolor='black', lw=1.2))
    ax_post.add_patch(Polygon(techo_right, closed=True, facecolor='#263238', edgecolor='black', lw=1.2))


    # 3. FACHADA LATERAL IZQUIERDA CON TALUD
    ax_lat = fig.add_axes([0.05, 0.12, 0.90, 0.36])
    ax_lat.set_aspect('equal')
    ax_lat.set_xlim(-2.0, 26.5)
    ax_lat.set_ylim(-5.5, 11.5)
    ax_lat.axis('off')

    # Terreno y Estrato Geotécnico
    steps_x = [24.71, 15.5, 14.5, 13.5, 12.5, 11.5, 10.5, 8.5, 0.0]
    steps_z = [ 0.00,  0.0, -0.4, -0.8, -1.2, -1.6, -2.0, -2.55, -2.55]
    ground_poly = [(0.0, -4.5)] + list(zip(steps_x, steps_z)) + [(24.71, -4.5)]
    ax_lat.add_patch(Polygon(ground_poly, closed=True, facecolor='#D7CCC8', edgecolor='none', zorder=1))
    ax_lat.plot(steps_x, steps_z, color=COLOR_TERRAIN, lw=2.2, zorder=4)
    ax_lat.text(13.0, -2.2, "PERFIL DE TERRENO NATURAL Y TALUD ESCALONADO", fontsize=7.0, color=COLOR_TERRAIN, fontweight='bold')

    # Sótano Posterior
    ax_lat.add_patch(Rectangle((0.00, -2.55), 8.30, 2.55, facecolor='#546E7A', edgecolor='#000000', lw=1.2, hatch='..', zorder=2))

    # Planta Baja: Zócalo de Mampostería Rústica
    ax_lat.add_patch(Rectangle((0.00, 0.00), 21.71, 3.00, facecolor=COLOR_STONE_FILL, edgecolor='#000000', lw=1.2, hatch='..', zorder=2))

    # Planta Alta: Pared de Madera Machihembrada
    ax_lat.add_patch(Rectangle((0.00, 3.00), 21.71, 2.40, facecolor=COLOR_WOOD_WALL, edgecolor='#000000', lw=1.2, zorder=2))
    for my in np.linspace(3.20, 5.20, 10):
        ax_lat.plot([0.00, 21.71], [my, my], color='#5D4037', lw=0.4, zorder=3)

    # Ventanas con Shutters de Madera
    for vy in [2.5, 7.5, 14.0, 19.0]:
        ax_lat.add_patch(Rectangle((vy, 3.8), 1.6, 1.2, facecolor='#E0F7FA', edgecolor='#3E2723', lw=0.9, zorder=3))
        ax_lat.add_patch(Rectangle((vy - 0.25, 3.8), 0.25, 1.2, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.6, zorder=4))
        ax_lat.add_patch(Rectangle((vy + 1.60, 3.8), 0.25, 1.2, facecolor=COLOR_SHUTTER, edgecolor='black', lw=0.6, zorder=4))

    # Gran Balcón Frontal en Voladizo
    ax_lat.add_patch(Rectangle((21.71, 2.90), 1.60, 0.15, facecolor='#3E2723', edgecolor='black', lw=1.0, zorder=5))
    ax_lat.plot([21.71, 23.31], [4.00, 4.00], color='#3E2723', lw=1.2, zorder=6)
    # Soporte diagonal del balcón (Jabalcones)
    ax_lat.plot([21.71, 23.00], [2.10, 2.90], color='#4E3629', lw=2.0, zorder=5)
    ax_lat.text(22.50, 4.30, "BALCÓN FRONTAL (1,60 m)", fontsize=6.0, ha='center', fontweight='bold', color='#3E2723')

    # Cubierta Alpina Longitudinal con Aleros
    ax_lat.add_patch(Rectangle((-1.10, 5.40), 24.00, 0.35, facecolor='#37474F', edgecolor='#000000', lw=1.2, zorder=6))
    # Canecillos expuestos continuos
    for rx in np.linspace(-0.8, 22.5, 20):
        ax_lat.plot([rx, rx], [5.15, 5.40], color='#8D6E63', lw=1.8, zorder=5)

    # Chimenea Monumental de Piedra en la Vista Lateral
    chim_lat = [(17.0, 5.40), (18.6, 5.40), (18.6, 10.50), (17.0, 10.50)]
    ax_lat.add_patch(Polygon(chim_lat, closed=True, facecolor=COLOR_CHIMNEY, edgecolor='black', lw=1.2, hatch='OO', zorder=7))
    ax_lat.add_patch(Rectangle((16.8, 10.50), 2.00, 0.15, facecolor='#37474F', edgecolor='black', lw=1.0, zorder=8))
    ax_lat.text(17.8, 10.85, "CHIMENEA DE PIEDRA", fontsize=6.2, ha='center', va='bottom', color='#37474F', fontweight='bold')

    ax_lat.text(12.5, -4.5, "FACHADA LATERAL IZQUIERDA (SÓTANO + ZÓCALO MAMPOSTERÍA + CUERPO TIMBER FRAME + CHIMENEA)", 
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
                     "COORDENADAS U.T.M. (REGVEN / WGS84) Y CUADRO DE ÁREAS DEL CHALET.", escala="1:200")

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

    ax_sit.add_patch(Rectangle((3.8, 3.5), 0.7, 1.2, facecolor='#0000FF', edgecolor='#000080', lw=1.0))
    ax_sit.text(4.15, 4.1, "LOTE\nCHALET", fontsize=5.0, color='white', fontweight='bold', ha='center', va='center')

    ax_sit.text(1.5, 2.65, "Calle 30", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(1.5, 5.15, "Calle 31", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(2.65, 7.0, "Av. Libertador", rotation=90, fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(5.15, 7.0, "Avenida 4", rotation=90, fontsize=5.0, ha='center', color='#555555')

    # 4. CUADRO DE ÁREAS PROYECTO CHALET RÚSTICO
    ax_areas = fig.add_axes([0.05, 0.69, 0.44, 0.07])
    ax_areas.axis('off')
    ax_areas.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FFF8E1', edgecolor=COLOR_BORDER, lw=1.0))
    ax_areas.text(0.04, 0.78, "ÁREA DE TERRENO: 273,81 m²", fontsize=7.5, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.04, 0.52, "ÁREA DE CONSTRUCCIÓN TOTAL: 372,50 m²", fontsize=7.2, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.04, 0.28, "• Planta Baja (Zócalo Mampostería y Garaje 2,80 m): 149,85 m²", fontsize=5.8, color='#000000')
    ax_areas.text(0.04, 0.10, "• Planta Alta (Residencia Chalet Timber Frame): 142,20 m²  |  Sótano: 80,45 m²", fontsize=5.8, color='#000000')

    # 5. RETÍCULA Y POLÍGONO UTM CON IMPRONTA DEL CHALET
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

    # Impronta de la Cubierta del Chalet Rústico con voladizos
    b1 = (529756.20, 1141662.30)
    b2 = (529763.80, 1141667.20)
    b3 = (529773.50, 1141650.60)
    b4 = (529765.90, 1141645.70)
    b_pts = [b1, b2, b3, b4, b1]
    ax_utm.plot([p[0] for p in b_pts], [p[1] for p in b_pts], color='#2E7D32', lw=1.5, linestyle='--', zorder=4)
    ax_utm.add_patch(Polygon([b1, b2, b3, b4], closed=True, facecolor='#E8F5E9', edgecolor='#2E7D32', hatch='//', alpha=0.5, zorder=3))

    ax_utm.text(529765.0, 1141656.0, "HUELLA CUBIERTA CHALET\n(ALEROS VOLADIZOS 1,10 - 1,20 m)\nÁrea Cubierta = 188,50 m²", 
                fontsize=7.2, fontweight='bold', color='#1B5E20', ha='center', va='center', zorder=7)

    draw_north_arrow(ax_utm, 529788.0, 1141672.0, size=4.0)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 5 generada exitosamente.")

# =============================================================================
# GENERADOR MAESTRO DEL PDF
# =============================================================================
def main():
    out_dir_proj = "Proyecto_Chalet_Rustico/01_Planos_y_Documentacion"
    out_dir_main = "01_Planos_y_Documentacion"
    os.makedirs(out_dir_proj, exist_ok=True)
    os.makedirs(out_dir_main, exist_ok=True)

    pdf_proj = os.path.join(out_dir_proj, "planos_casa_chalet.pdf")
    pdf_main = os.path.join(out_dir_main, "planos_casa_chalet.pdf")

    print(f"Generando documento PDF oficial del Chalet: {pdf_proj}...")
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
