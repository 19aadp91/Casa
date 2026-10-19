"""
Generador del PDF Arquitectónico Oficial ("planos_casa_completo.pdf")
Estilo 100% fiel a "planos de casa.pdf" de T.S.U. Angel Camacaro M.
Contiene la información de "casa_completo":
- Lámina 1: Plano Planta Arquitectónica Distribución - Planta Baja (Local Comercial + Garaje) y Sótano
- Lámina 2: Plano Planta Arquitectónica Distribución - Segundo Piso (Apartamento 3 Habitaciones)
- Lámina 3: Plano Distribución de Columnas y Ejes Estructurales (P.B., P.A. y Sótano)
- Lámina 4: Plano Fachadas (Fachada Principal Av. 4, Fachada Lateral Izquierda con desnivel, Fachada Posterior)
- Lámina 5: Levantamiento Poligonal de Linderos, Topografía UTM, Cuadro de Coordenadas y Situación Relativa
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
# ESTILOS Y COLORES ARQUITECTÓNICOS
# =============================================================================
COLOR_BORDER = '#0000FF'       # Azul normativo de márgenes y recuadros de cajetín
COLOR_HEADER_RED = '#E00000'   # Rojo República y títulos de lámina
COLOR_CAJETIN_RED = '#E00000'  # Rojo datos técnicos (Nombre, Ubicación, CI)
COLOR_TEXT_BLACK = '#000000'   # Negro textos de dibujo y cotas
COLOR_WALL_FILL = '#505050'    # Relleno gris oscuro de muros cortados
COLOR_WALL_LINE = '#000000'    # Contorno negro muros
COLOR_DOOR = '#000000'         # Carpintería puertas
COLOR_WINDOW = '#008080'       # Carpintería ventanas / vidrios
COLOR_STAIRS = '#303030'       # Escaleras
COLOR_COL_RED = '#FF0000'      # Columnas estructurales
COLOR_AXIS_CYAN = '#00AAAA'    # Líneas de ejes estructurales
COLOR_TERRAIN = '#8B4513'      # Línea de terreno natural / talud
COLOR_FURNITURE = '#808080'    # Mobiliario arquitectónico tenue

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
        ax_frame.text(0.50, title_y - 0.013, title_line2, fontsize=10.5, fontweight='bold', 
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

    ax_frame.text(0.468, row_top - 0.007, "LEVANTADO CALCULADO Y DIGITALIZO:", fontsize=6.0, fontweight='bold', color=COLOR_BORDER)
    ax_frame.text(0.468, row_top - 0.019, "T.S.U. ANGEL CAMACARO M.", 
                  fontsize=8.0, fontweight='bold', color=COLOR_CAJETIN_RED)
    ax_frame.text(0.468, row_top - 0.030, "CVPT.: N° 1260       SOVIT.: N° 0050", 
                  fontsize=6.8, fontweight='bold', color=COLOR_CAJETIN_RED)

    ax_frame.text(0.658, row_top - 0.007, "REVISADO:", fontsize=6.5, fontweight='bold', color=COLOR_BORDER)

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

# =============================================================================
# FUNCIONES DIBUJO ARQUITECTÓNICO 2D
# =============================================================================
def draw_rect_wall(ax, x1, y1, x2, y2, color=COLOR_WALL_FILL):
    """Dibuja un segmento de muro relleno con línea de borde."""
    rx = min(x1, x2)
    ry = min(y1, y2)
    rw = abs(x2 - x1)
    rh = abs(y2 - y1)
    rect = Rectangle((rx, ry), rw, rh, facecolor=color, edgecolor=COLOR_WALL_LINE, linewidth=0.7, zorder=3)
    ax.add_patch(rect)

def draw_door_swing(ax, hinge_x, hinge_y, width, angle_start, angle_end):
    """Dibuja una puerta arquitectónica con hoja y arco de apertura de 90°."""
    rad = math.radians(angle_start)
    leaf_x = hinge_x + width * math.cos(rad)
    leaf_y = hinge_y + width * math.sin(rad)
    ax.plot([hinge_x, leaf_x], [hinge_y, leaf_y], color=COLOR_DOOR, lw=1.1, zorder=4)
    arc = Arc((hinge_x, hinge_y), 2*width, 2*width, angle=0, theta1=min(angle_start, angle_end), 
              theta2=max(angle_start, angle_end), color=COLOR_DOOR, lw=0.6, linestyle='-', zorder=4)
    ax.add_patch(arc)

def draw_sliding_door(ax, x1, y1, x2, y2, is_vertical=False):
    """Dibuja puerta corrediza de cristal/aluminio."""
    if not is_vertical:
        xmid = (x1 + x2) / 2
        ax.plot([x1, xmid + 0.1], [y1 - 0.02, y1 - 0.02], color='#000000', lw=1.0, zorder=4)
        ax.plot([xmid - 0.1, x2], [y1 + 0.02, y1 + 0.02], color='#000000', lw=1.0, zorder=4)
    else:
        ymid = (y1 + y2) / 2
        ax.plot([x1 - 0.02, x1 - 0.02], [y1, ymid + 0.1], color='#000000', lw=1.0, zorder=4)
        ax.plot([x1 + 0.02, x1 + 0.02], [ymid - 0.1, y2], color='#000000', lw=1.0, zorder=4)

def draw_window_2d(ax, x1, y1, x2, y2, is_vertical=False):
    """Dibuja una ventana en planta con marco y doble línea de vidrio."""
    if not is_vertical:
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymid = (y1 + y2) / 2
        thick = abs(y2 - y1)
        ax.add_patch(Rectangle((xmin, min(y1, y2)), xmax - xmin, thick, facecolor='white', edgecolor='none', zorder=4))
        ax.plot([xmin, xmin], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmax, xmax], [y1, y2], color='black', lw=0.8, zorder=5)
        ax.plot([xmin, xmax], [ymid - 0.02, ymid - 0.02], color=COLOR_WINDOW, lw=0.8, zorder=5)
        ax.plot([xmin, xmax], [ymid + 0.02, ymid + 0.02], color=COLOR_WINDOW, lw=0.8, zorder=5)
    else:
        ymin, ymax = min(y1, y2), max(y1, y2)
        xmid = (x1 + x2) / 2
        thick = abs(x2 - x1)
        ax.add_patch(Rectangle((min(x1, x2), ymin), thick, ymax - ymin, facecolor='white', edgecolor='none', zorder=4))
        ax.plot([x1, x2], [ymin, ymin], color='black', lw=0.8, zorder=5)
        ax.plot([x1, x2], [ymax, ymax], color='black', lw=0.8, zorder=5)
        ax.plot([xmid - 0.02, xmid - 0.02], [ymin, ymax], color=COLOR_WINDOW, lw=0.8, zorder=5)
        ax.plot([xmid + 0.02, xmid + 0.02], [ymin, ymax], color=COLOR_WINDOW, lw=0.8, zorder=5)

def draw_col_hatch(ax, cx, cy, size=0.25):
    """Dibuja una columna estructural con achurado diagonal rojo."""
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
            rotation=90, color='#000000', fontweight='bold', zorder=8)

def draw_stairs_2d(ax, x1, y1, x2, y2, num_steps, label="SUBE"):
    """Dibuja escaleras con huellas y flecha de recorrido."""
    ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor='#F5F5F5', edgecolor='#000000', lw=0.8, zorder=3))
    dy = (y2 - y1) / num_steps
    for i in range(1, num_steps):
        sy = y1 + i * dy
        ax.plot([x1, x2], [sy, sy], color=COLOR_STAIRS, lw=0.6, zorder=4)
    xmid = (x1 + x2) / 2
    if label == "SUBE":
        ax.annotate('', xy=(xmid, y2 - 0.3), xytext=(xmid, y1 + 0.3),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.0), zorder=5)
        ax.text(xmid, (y1 + y2)/2, label, fontsize=6.5, ha='center', va='center', 
                color='#000000', fontweight='bold', backgroundcolor='#F5F5F5', zorder=6)
    else:
        ax.annotate('', xy=(xmid, y1 + 0.3), xytext=(xmid, y2 - 0.3),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.0), zorder=5)
        ax.text(xmid, (y1 + y2)/2, label, fontsize=6.5, ha='center', va='center', 
                color='#000000', fontweight='bold', backgroundcolor='#F5F5F5', zorder=6)


# =============================================================================
# LÁMINA 1: PLANTA BAJA (LOCAL COMERCIAL + GARAJE) Y SÓTANO
# =============================================================================
def build_sheet_1(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA", "DISTRIBUCIÓN - PLANTA BAJA Y SÓTANO.", escala="1:75")

    # Área de dibujo para PLANTA BAJA
    ax = fig.add_axes([0.05, 0.28, 0.52, 0.65])
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 10.8)
    ax.set_ylim(-2.0, 25.5)
    ax.axis('off')

    # Título del dibujo con espacio adecuado
    ax.text(4.5, -1.2, "PLANTA BAJA (LOCAL COMERCIAL Y GARAJE)", 
            fontsize=9.5, fontweight='bold', ha='center', va='top')
    ax.plot([0.5, 8.5], [-1.55, -1.55], color='black', lw=1.2)

    # 1. Lindero y Muro Propio Izquierdo
    ax.plot([-0.05, -0.05], [-0.5, 22.5], color='#888888', lw=1.0, linestyle='--')
    ax.text(-0.25, 11.0, "PARED DEL VECINO", rotation=90, fontsize=6.5, color='#888888', ha='right', va='center')
    draw_rect_wall(ax, 0.15, 0.00, 0.30, 21.71)
    ax.text(0.225, 22.2, "MURO PROPIO\n(EJE 0)", fontsize=6.0, ha='center', va='bottom', color=COLOR_COL_RED, fontweight='bold')

    # 2. Fachada Frontal en Avenida 4 (Y: 21.56 a 21.71 m)
    draw_rect_wall(ax, 0.15, 21.56, 0.40, 21.71)
    draw_rect_wall(ax, 2.65, 21.56, 3.15, 21.71)
    draw_rect_wall(ax, 5.65, 21.56, 6.20, 21.71)
    draw_rect_wall(ax, 8.80, 21.56, 9.15, 21.71)

    draw_sliding_door(ax, 0.40, 21.63, 2.65, 21.63)
    ax.text(1.52, 21.85, "PORTÓN GARAJE 2,25m", fontsize=6.2, ha='center', va='bottom', fontweight='bold')

    draw_window_2d(ax, 3.15, 21.56, 5.65, 21.71)
    draw_window_2d(ax, 6.20, 21.56, 8.80, 21.71)
    ax.text(4.40, 21.85, "VITRINA / ACCESO 2,50m", fontsize=5.8, ha='center', va='bottom', color=COLOR_WINDOW)
    ax.text(7.50, 21.85, "VITRINA / ACCESO 2,60m", fontsize=5.8, ha='center', va='bottom', color=COLOR_WINDOW)

    # 3. Muro Lateral Derecho (X: 9.00 a 9.15 m)
    draw_rect_wall(ax, 9.00, 3.50, 9.15, 4.10)
    draw_window_2d(ax, 9.00, 4.10, 9.15, 5.00, is_vertical=True) # Ventana Baño
    draw_rect_wall(ax, 9.00, 5.00, 9.15, 6.30)
    draw_window_2d(ax, 9.00, 6.30, 9.15, 8.00, is_vertical=True)
    draw_rect_wall(ax, 9.00, 8.00, 9.15, 9.65)
    draw_window_2d(ax, 9.00, 9.65, 9.15, 11.85, is_vertical=True)
    draw_rect_wall(ax, 9.00, 11.85, 9.15, 15.50)
    draw_window_2d(ax, 9.00, 15.50, 9.15, 17.70, is_vertical=True)
    draw_rect_wall(ax, 9.00, 17.70, 9.15, 18.80)
    draw_window_2d(ax, 9.00, 18.80, 9.15, 21.00, is_vertical=True)
    draw_rect_wall(ax, 9.00, 21.00, 9.15, 21.56)

    # 4. Muros Posteriores Planta Baja
    draw_rect_wall(ax, 0.15, 0.00, 6.40, 0.15)
    draw_window_2d(ax, 0.55, 0.00, 2.35, 0.15)
    draw_rect_wall(ax, 6.25, 0.15, 6.40, 3.50)
    draw_window_2d(ax, 6.25, 0.65, 6.40, 2.85, is_vertical=True)
    draw_rect_wall(ax, 6.25, 3.50, 9.15, 3.65)

    # 5. Muro Divisorio Eje 1 (Garaje vs Local)
    draw_rect_wall(ax, 2.75, 0.15, 2.90, 21.56)

    # 6. Muro Posterior Garaje con Puerta a Escalera
    draw_rect_wall(ax, 0.30, 8.80, 1.65, 8.95)
    draw_door_swing(ax, 1.65, 8.95, 0.90, 270, 360)
    draw_rect_wall(ax, 2.55, 8.80, 2.75, 8.95)

    # 7. Escaleras
    draw_stairs_2d(ax, 0.30, 4.45, 1.40, 7.40, 12, label="BAJA")
    draw_stairs_2d(ax, 1.55, 4.40, 2.65, 7.35, 14, label="SUBE")
    draw_rect_wall(ax, 1.40, 4.40, 1.55, 7.35)

    draw_rect_wall(ax, 0.30, 4.25, 1.65, 4.40)
    draw_door_swing(ax, 1.65, 4.40, 0.80, 270, 360)
    draw_rect_wall(ax, 2.45, 4.25, 2.75, 4.40)

    # 8. Baño del Local
    draw_rect_wall(ax, 5.85, 5.40, 9.00, 5.55)
    draw_rect_wall(ax, 5.85, 3.65, 6.00, 3.95)
    draw_door_swing(ax, 6.00, 3.95, 0.80, 0, 90)
    draw_rect_wall(ax, 5.85, 4.75, 6.00, 5.40)
    ax.add_patch(Rectangle((8.1, 3.8), 0.6, 0.45, facecolor='white', edgecolor='#000000', lw=0.6, zorder=4))
    ax.add_patch(Circle((8.4, 4.05), 0.18, facecolor='white', edgecolor='#000000', lw=0.6, zorder=5))
    ax.add_patch(Rectangle((6.2, 3.8), 0.5, 0.4, facecolor='white', edgecolor='#000000', lw=0.6, zorder=4))
    ax.text(7.4, 4.5, "Baño Local\n3,00 x 1,75", fontsize=6.2, ha='center', va='center', fontweight='bold')

    # 9. Depósito / Oficina Local
    draw_rect_wall(ax, 2.90, 3.50, 4.05, 3.65)
    draw_door_swing(ax, 4.05, 3.50, 0.85, 270, 360)
    draw_rect_wall(ax, 4.90, 3.50, 6.25, 3.65)
    ax.text(4.55, 1.80, "Depósito / Oficina\n3,35 x 3,35", fontsize=6.5, ha='center', va='center', fontweight='bold')

    # 10. Garaje Doble
    for vy in [10.2, 16.0]:
        ax.add_patch(Rectangle((0.55, vy), 1.95, 4.30, facecolor='#EAEAEA', edgecolor='#888888', lw=0.8, linestyle='--', zorder=3))
        ax.text(1.52, vy + 2.15, "Vehículo", fontsize=6.0, color='#666666', ha='center', va='center')
    ax.text(1.52, 15.0, "GARAJE DOBLE\nTECHADO\n2,45 x 12,61 m", fontsize=7.2, 
            fontweight='bold', ha='center', va='center', color='#000000', zorder=5)

    # 11. Gran Local Comercial
    ax.text(5.95, 13.5, "GRAN LOCAL COMERCIAL\nÁREA ÚTIL: 98,00 m²\n(6,10 x 16,06 m)", 
            fontsize=8.5, fontweight='bold', ha='center', va='center', color='#000000', zorder=5)
    ax.text(5.95, 10.5, "Piso de Alto Tráfico\nSalón Comercial Diáfano", fontsize=6.8, ha='center', va='center', color='#555555')

    # Cotas Planta Baja (reubicadas sin colisiones)
    draw_dim_h(ax, 0.30, 2.75, 23.4, "2,45")
    draw_dim_h(ax, 2.90, 9.00, 23.4, "6,10")
    draw_dim_h(ax, 0.15, 9.15, 24.5, "9,00")

    draw_dim_v(ax, -0.8, 0.00, 21.71, "21,71")
    draw_dim_v(ax, -0.2, 8.95, 21.56, "12,61")
    draw_dim_v(ax, 10.0, 5.55, 21.56, "16,01")
    draw_dim_v(ax, 10.0, 3.65, 5.40, "1,75")

    # Flecha de Norte
    draw_north_arrow(ax, 9.8, 23.0, size=1.2)


    # ÁREA DE DIBUJO PARA PLANTA SÓTANO
    ax_sot = fig.add_axes([0.55, 0.12, 0.42, 0.45])
    ax_sot.set_aspect('equal')
    ax_sot.set_xlim(-1.0, 10.5)
    ax_sot.set_ylim(-2.0, 10.5)
    ax_sot.axis('off')

    ax_sot.text(4.5, -1.2, "PLANTA SÓTANO", 
                fontsize=9.5, fontweight='bold', ha='center', va='top')
    ax_sot.plot([1.5, 7.5], [-1.55, -1.55], color='black', lw=1.2)

    # Muros Sótano
    draw_rect_wall(ax_sot, 0.15, 0.00, 0.30, 8.30)
    draw_rect_wall(ax_sot, 0.30, 8.15, 9.15, 8.30)
    draw_rect_wall(ax_sot, 8.95, 3.65, 9.15, 8.30)
    draw_rect_wall(ax_sot, 6.00, 3.50, 9.15, 3.65)
    draw_door_swing(ax_sot, 7.95, 3.65, 0.85, 270, 360)
    draw_rect_wall(ax_sot, 6.25, 0.15, 6.40, 3.50)
    draw_rect_wall(ax_sot, 0.30, 0.00, 6.40, 0.15)

    draw_rect_wall(ax_sot, 0.30, 3.50, 3.95, 3.65)
    draw_door_swing(ax_sot, 3.95, 3.65, 0.85, 270, 360)
    draw_rect_wall(ax_sot, 4.80, 3.50, 6.00, 3.65)

    draw_rect_wall(ax_sot, 2.80, 0.15, 2.95, 2.60)
    draw_door_swing(ax_sot, 2.80, 2.60, 0.80, 0, 90)
    draw_rect_wall(ax_sot, 2.80, 3.40, 2.95, 3.50)

    draw_rect_wall(ax_sot, 5.85, 3.65, 6.00, 7.25)
    draw_door_swing(ax_sot, 6.00, 7.25, 0.80, 90, 180)
    draw_rect_wall(ax_sot, 5.85, 8.05, 6.00, 8.15)

    draw_stairs_2d(ax_sot, 0.30, 4.45, 1.40, 7.40, 12, label="LLEGA")

    ax_sot.text(7.5, 6.0, "Sala\n4,50 x 2,90", fontsize=6.8, ha='center', va='center', fontweight='bold')
    ax_sot.text(3.5, 6.0, "Cocina - Comedor\n4,40 x 3,30", fontsize=6.8, ha='center', va='center', fontweight='bold')
    ax_sot.text(1.5, 1.8, "Habitación 1\n2,65 x 3,35", fontsize=6.8, ha='center', va='center', fontweight='bold')
    ax_sot.text(4.5, 1.8, "Lavadero\n1,65 x 2,50", fontsize=6.2, ha='center', va='center')
    ax_sot.text(5.5, 0.8, "Baño\n1,50x1,79", fontsize=6.0, ha='center', va='center')

    for cx, cy in [(2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
                   (2.825, 3.575), (5.925, 3.575), (9.075, 3.575)]:
        draw_col_hatch(ax_sot, cx, cy, size=0.35)

    draw_dim_h(ax_sot, 0.30, 6.00, 8.9, "5,70")
    draw_dim_h(ax_sot, 6.00, 9.00, 8.9, "3,00")
    draw_dim_v(ax_sot, 9.7, 3.65, 8.15, "4,50")
    draw_dim_v(ax_sot, 9.7, 0.15, 3.65, "3,50")

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 1 regenerada.")


# =============================================================================
# LÁMINA 2: PLANTA SEGUNDO PISO (APARTAMENTO RESIDENCIAL 3 HABITACIONES)
# =============================================================================
def build_sheet_2(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO PLANTA ARQUITECTÓNICA", 
                     "DISTRIBUCIÓN - SEGUNDO PISO (APARTAMENTO 3 HABITACIONES).", escala="1:75")

    ax = fig.add_axes([0.15, 0.12, 0.70, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-2.0, 11.5)
    ax.set_ylim(-2.0, 25.5)
    ax.axis('off')

    ax.text(4.5, -1.2, "PLANTA SEGUNDO PISO - APARTAMENTO RESIDENCIAL", 
            fontsize=10.0, fontweight='bold', ha='center', va='top')
    ax.plot([0.0, 9.0], [-1.55, -1.55], color='black', lw=1.2)

    # 1. Muro Propio Izquierdo
    draw_rect_wall(ax, 0.15, 0.00, 0.30, 21.71)
    ax.text(0.225, 22.2, "MURO PROPIO\n(EJE 0)", fontsize=6.2, ha='center', va='bottom', color=COLOR_COL_RED, fontweight='bold')

    # 2. Fachada Frontal en Avenida 4 (Y: 21.56 a 21.71 m)
    draw_rect_wall(ax, 0.15, 21.56, 0.65, 21.71)
    draw_window_2d(ax, 0.65, 21.56, 2.60, 21.71)
    draw_rect_wall(ax, 2.60, 21.56, 3.15, 21.71)
    draw_window_2d(ax, 3.15, 21.56, 5.50, 21.71)
    draw_rect_wall(ax, 5.50, 21.56, 6.00, 21.71)

    # Balcón de la Suite Principal
    ax.plot([6.00, 9.00], [21.71, 21.71], color='#000000', lw=1.5, zorder=5)
    ax.plot([6.00, 9.00], [21.56, 21.56], color='#888888', lw=0.6, linestyle=':')
    ax.text(7.50, 21.85, "BALCÓN TECHADO\n(BARANDA 1,05m)", fontsize=5.8, ha='center', va='bottom', fontweight='bold')

    # Puerta-Ventana Corrediza del Balcón
    draw_rect_wall(ax, 6.00, 19.95, 6.50, 20.10)
    draw_sliding_door(ax, 6.50, 20.02, 8.50, 20.02)
    draw_rect_wall(ax, 8.50, 19.95, 9.15, 20.10)
    ax.text(7.50, 20.25, "Puerta Corrediza 2,00m", fontsize=5.8, ha='center', va='bottom', color='#555555')

    # 3. Muro Lateral Derecho sobre Eje 3
    draw_rect_wall(ax, 9.00, 3.50, 9.15, 4.10)
    draw_window_2d(ax, 9.00, 4.10, 9.15, 5.00, is_vertical=True)
    draw_rect_wall(ax, 9.00, 5.00, 9.15, 6.30)
    draw_window_2d(ax, 9.00, 6.30, 9.15, 8.00, is_vertical=True)
    draw_rect_wall(ax, 9.00, 8.00, 9.15, 9.65)
    draw_window_2d(ax, 9.00, 9.65, 9.15, 11.85, is_vertical=True)
    draw_rect_wall(ax, 9.00, 11.85, 9.15, 13.15)
    draw_window_2d(ax, 9.00, 13.15, 9.15, 14.05, is_vertical=True)
    draw_rect_wall(ax, 9.00, 14.05, 9.15, 16.40)
    draw_window_2d(ax, 9.00, 16.40, 9.15, 18.80, is_vertical=True)
    draw_rect_wall(ax, 9.00, 18.80, 9.15, 20.10)
    ax.plot([9.15, 9.15], [20.10, 21.71], color='#000000', lw=1.5, zorder=5)

    # 4. Muros Posteriores Segundo Piso
    draw_rect_wall(ax, 0.15, 0.00, 6.40, 0.15)
    draw_window_2d(ax, 0.60, 0.00, 2.30, 0.15)
    draw_window_2d(ax, 3.60, 0.00, 5.40, 0.15)
    draw_rect_wall(ax, 6.25, 0.15, 6.40, 3.50)
    draw_window_2d(ax, 6.25, 0.65, 6.40, 2.85, is_vertical=True)
    draw_rect_wall(ax, 6.25, 3.50, 9.15, 3.65)

    # 5. Muro Longitudinal Eje 2
    draw_rect_wall(ax, 5.85, 3.65, 6.00, 3.85)
    draw_door_swing(ax, 6.00, 3.85, 0.70, 0, 90)
    draw_rect_wall(ax, 5.85, 4.55, 6.00, 7.95)
    draw_door_swing(ax, 6.00, 7.95, 0.70, 0, 90)
    draw_rect_wall(ax, 5.85, 8.65, 6.00, 12.10)
    draw_rect_wall(ax, 6.00, 11.95, 6.80, 12.10)
    draw_door_swing(ax, 6.05, 12.10, 0.70, 90, 180)
    draw_rect_wall(ax, 5.85, 13.60, 6.00, 21.56)

    # 6. SUITE PRINCIPAL
    draw_rect_wall(ax, 6.00, 15.15, 6.80, 15.30)
    draw_door_swing(ax, 6.05, 15.30, 0.75, 90, 180)

    # Cama Queen esquemática
    ax.add_patch(Rectangle((6.7, 16.5), 2.0, 1.8, facecolor='#FAFAFA', edgecolor='#AAAAAA', lw=0.6, zorder=3))
    ax.text(7.7, 17.4, "Cama Queen", fontsize=5.5, color='#777777', ha='center', va='center')

    # Vestier
    draw_rect_wall(ax, 6.80, 14.55, 6.95, 15.30)
    ax.add_patch(Rectangle((7.0, 14.65), 1.9, 0.60, facecolor='#F0F0F0', edgecolor='#888888', lw=0.6, linestyle='--', zorder=3))
    ax.text(7.95, 14.95, "Vestier / Closet", fontsize=5.8, ha='center', va='center', color='#555555')

    # Baño Privado En-Suite
    draw_rect_wall(ax, 6.80, 12.70, 9.00, 12.85)
    draw_rect_wall(ax, 6.80, 12.85, 6.95, 13.75)
    draw_door_swing(ax, 6.95, 13.75, 0.70, 0, 90)
    draw_rect_wall(ax, 6.80, 14.45, 6.95, 14.55)
    ax.add_patch(Rectangle((8.1, 12.9), 0.8, 0.8, facecolor='#E0F7FA', edgecolor='#008080', lw=0.6, zorder=3))
    ax.plot([8.1, 8.9], [12.9, 13.7], color='#008080', lw=0.4, zorder=4)
    ax.plot([8.1, 8.9], [13.7, 12.9], color='#008080', lw=0.4, zorder=4)
    ax.add_patch(Rectangle((7.1, 13.0), 0.5, 0.4, facecolor='white', edgecolor='black', lw=0.6, zorder=4))
    ax.text(7.7, 13.8, "Baño Privado\n2,20 x 1,85", fontsize=5.8, ha='center', va='center', fontweight='bold')

    ax.text(7.50, 18.80, "HABITACIÓN PRINCIPAL\n(MASTER SUITE)\n3,00 x 4,65 m", 
            fontsize=7.8, fontweight='bold', ha='center', va='center', color='#000000', zorder=5)

    # 7. HABITACIÓN 2
    draw_rect_wall(ax, 6.00, 8.80, 9.00, 8.95)
    ax.add_patch(Rectangle((7.0, 11.95), 1.9, 0.55, facecolor='#F0F0F0', edgecolor='#888888', lw=0.6, linestyle='--', zorder=3))
    ax.text(7.95, 12.22, "Closet", fontsize=5.8, ha='center', va='center', color='#555555')
    ax.text(7.50, 10.45, "HABITACIÓN 2\n3,00 x 3,60 m", 
            fontsize=7.8, fontweight='bold', ha='center', va='center', color='#000000', zorder=5)

    # 8. HABITACIÓN 3
    draw_rect_wall(ax, 6.00, 5.40, 9.00, 5.55)
    ax.add_patch(Rectangle((7.0, 8.25), 1.9, 0.55, facecolor='#F0F0F0', edgecolor='#888888', lw=0.6, linestyle='--', zorder=3))
    ax.text(7.95, 8.52, "Closet", fontsize=5.8, ha='center', va='center', color='#555555')
    ax.text(7.50, 7.00, "HABITACIÓN 3\n3,00 x 3,25 m", 
            fontsize=7.8, fontweight='bold', ha='center', va='center', color='#000000', zorder=5)

    # 9. BAÑO COMPARTIDO
    ax.add_patch(Rectangle((8.1, 3.8), 0.8, 0.8, facecolor='#E0F7FA', edgecolor='#008080', lw=0.6, zorder=3))
    ax.plot([8.1, 8.9], [3.8, 4.6], color='#008080', lw=0.4, zorder=4)
    ax.plot([8.1, 8.9], [4.6, 3.8], color='#008080', lw=0.4, zorder=4)
    ax.add_patch(Rectangle((6.2, 4.7), 0.5, 0.4, facecolor='white', edgecolor='black', lw=0.6, zorder=4))
    ax.text(7.30, 4.50, "Baño Compartido\n3,00 x 1,75", fontsize=6.2, ha='center', va='center', fontweight='bold')

    # 10. ÁREA SOCIAL ABIERTA
    ax.text(3.10, 18.50, "SALA - COMEDOR\nCONCEPTO ABIERTO\n(5,55 x 7,06 m)", 
            fontsize=8.5, fontweight='bold', ha='center', va='center', color='#000000', zorder=5)
    ax.text(3.10, 16.50, "Vistas panorámicas hacia la Avenida 4", fontsize=6.8, ha='center', va='center', color='#555555')

    # 11. COCINA INTEGRAL CON GRAN ISLA
    ax.add_patch(Rectangle((0.30, 7.50), 0.65, 6.00, facecolor='#FFF3E0', edgecolor='#FF9800', lw=0.8, zorder=3))
    ax.add_patch(Rectangle((0.95, 7.35), 1.80, 0.65, facecolor='#FFF3E0', edgecolor='#FF9800', lw=0.8, zorder=3))
    ax.text(0.62, 10.50, "Mesón Cocina", rotation=90, fontsize=6.0, ha='center', va='center', color='#E65100')

    ax.add_patch(Rectangle((2.15, 9.80), 0.95, 2.60, facecolor='#FFE0B2', edgecolor='#E65100', lw=1.2, zorder=4))
    for ty in [10.15, 10.75, 11.35, 11.95]:
        ax.add_patch(Circle((3.45, ty), 0.18, facecolor='white', edgecolor='#E65100', lw=0.8, zorder=4))
    ax.text(2.62, 11.10, "GRAN ISLA\nCENTRAL\n2,60 x 0,95", fontsize=6.8, 
            fontweight='bold', ha='center', va='center', color='#BF360C', zorder=5)

    # 12. ESCALERA Y BARANDA
    draw_stairs_2d(ax, 1.55, 4.40, 2.65, 7.35, 14, label="LLEGA")
    ax.plot([2.65, 2.65], [4.40, 7.35], color='#000000', lw=1.4, zorder=5)
    ax.plot([0.30, 2.75], [7.35, 7.35], color='#000000', lw=1.2, zorder=5)

    # 13. LAVANDERÍA Y ESTUDIO
    draw_rect_wall(ax, 0.30, 4.25, 1.65, 4.40)
    draw_door_swing(ax, 1.65, 4.40, 0.80, 270, 360)
    draw_rect_wall(ax, 2.45, 4.25, 2.75, 4.40)
    draw_rect_wall(ax, 2.75, 0.15, 2.90, 4.40)
    ax.text(1.50, 2.20, "Lavandería\n2,45 x 4,10 m\n(Batea / Lav.)", fontsize=6.5, ha='center', va='center', fontweight='bold')

    draw_rect_wall(ax, 2.90, 3.50, 4.05, 3.65)
    draw_door_swing(ax, 4.05, 3.50, 0.85, 270, 360)
    draw_rect_wall(ax, 4.90, 3.50, 6.25, 3.65)
    ax.text(4.55, 1.80, "Terraza Posterior / Estar\n3,35 x 3,35 m\n(Vista al Patio)", fontsize=6.8, ha='center', va='center', fontweight='bold')

    # Cotas Planta Alta (reubicadas sin colisiones)
    draw_dim_h(ax, 0.30, 5.85, 23.4, "5,55")
    draw_dim_h(ax, 6.00, 9.00, 23.4, "3,00")
    draw_dim_h(ax, 0.15, 9.15, 24.5, "9,00")

    draw_dim_v(ax, -0.6, 0.00, 21.71, "21,71")
    draw_dim_v(ax, 9.9, 15.30, 19.95, "4,65")
    draw_dim_v(ax, 9.9, 8.95, 12.55, "3,60")
    draw_dim_v(ax, 9.9, 5.55, 8.80, "3,25")
    draw_dim_v(ax, 9.9, 3.65, 5.40, "1,75")

    draw_north_arrow(ax, 10.2, 23.0, size=1.2)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 2 regenerada.")


# =============================================================================
# LÁMINA 3: PLANO DISTRIBUCIÓN DE COLUMNAS Y EJES ESTRUCTURALES
# =============================================================================
def build_sheet_3(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO DISTRIBUCIÓN DE COLUMNAS Y EJES", 
                     "PRIMER Y SEGUNDO PISO: 25 x 25 (cm) — SÓTANO: 35 x 35 (cm).", escala="1:75")

    ax = fig.add_axes([0.10, 0.12, 0.80, 0.80])
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 12.0)
    ax.set_ylim(-3.5, 25.5)
    ax.axis('off')

    # Título sin colisiones
    ax.text(4.5, -2.6, "DISTRIBUCIÓN MODULAR DE EJES Y COLUMNAS", 
            fontsize=10.0, fontweight='bold', ha='center', va='top')
    ax.plot([0.5, 8.5], [-2.9, -2.9], color='black', lw=1.2)

    axes_x = [("0", 0.275), ("1", 2.825), ("2", 5.925), ("3", 9.075)]
    axes_y = [
        ("A0", 21.585), ("A", 18.575), ("B", 16.325), ("C", 14.625),
        ("D", 12.025), ("E", 8.875), ("F", 6.575), ("G", 3.575), ("SOT", 0.075)
    ]

    for label, gx in axes_x:
        ax.plot([gx, gx], [-0.8, 22.8], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((gx, 23.3), 0.35, facecolor='white', edgecolor='#000000', lw=1.0, zorder=5))
        ax.text(gx, 23.3, label, fontsize=8.0, fontweight='bold', ha='center', va='center', zorder=6)
        ax.add_patch(Circle((gx, -1.3), 0.35, facecolor='white', edgecolor='#000000', lw=1.0, zorder=5))
        ax.text(gx, -1.3, label, fontsize=8.0, fontweight='bold', ha='center', va='center', zorder=6)

    for label, gy in axes_y:
        ax.plot([-0.8, 10.2], [gy, gy], color=COLOR_AXIS_CYAN, lw=0.7, linestyle='-.', zorder=2)
        ax.add_patch(Circle((10.7, gy), 0.35, facecolor='white', edgecolor='#000000', lw=1.0, zorder=5))
        ax.text(10.7, gy, label, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=6)

    for i in range(len(axes_x)-1):
        x_a = axes_x[i][1]
        x_b = axes_x[i+1][1]
        for _, gy in axes_y:
            ax.plot([x_a, x_b], [gy, gy], color='#D0D0D0', lw=1.2, zorder=1)

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

    sot_cols = [
        (0.275, 6.575), (2.825, 6.575), (5.925, 6.575), (9.075, 6.575),
        (0.275, 3.575), (2.825, 3.575), (5.925, 3.575), (9.075, 3.575),
    ]
    for cx, cy in sot_cols:
        ax.add_patch(Rectangle((cx - 0.175, cy - 0.175), 0.35, 0.35, 
                               fill=False, edgecolor='#0000FF', lw=1.2, zorder=7))

    draw_dim_h(ax, 0.275, 2.825, 22.0, "2,55")
    draw_dim_h(ax, 2.825, 5.925, 22.0, "3,10")
    draw_dim_h(ax, 5.925, 9.075, 22.0, "3,15")

    draw_dim_v(ax, -1.3, 18.575, 21.585, "3,01")
    draw_dim_v(ax, -1.3, 16.325, 18.575, "2,25")
    draw_dim_v(ax, -1.3, 14.625, 16.325, "1,70")
    draw_dim_v(ax, -1.3, 12.025, 14.625, "2,60")
    draw_dim_v(ax, -1.3, 8.875, 12.025, "3,15")
    draw_dim_v(ax, -1.3, 6.575, 8.875, "2,30")
    draw_dim_v(ax, -1.3, 3.575, 6.575, "3,00")
    draw_dim_v(ax, -1.3, 0.075, 3.575, "3,50")
    draw_dim_v(ax, -2.0, 0.075, 21.585, "21,51")

    # Leyenda estructural limpia
    ax.add_patch(Rectangle((-0.5, 0.5), 10.0, 2.4, facecolor='#FFFFFF', edgecolor='#0000FF', lw=1.0, zorder=8))
    ax.text(-0.2, 2.55, "ESPECIFICACIONES ESTRUCTURALES Y LEYENDA:", fontsize=7.2, fontweight='bold', color=COLOR_BORDER, zorder=9)
    ax.text(-0.2, 2.05, "• Columnas C-1 (P.B. y P.A.): 25 x 25 cm (26 unidades). Refuerzo: 4 Ø 1/2\" + estribos Ø 3/8\" @ 15 cm.", fontsize=6.8, color='#000000', zorder=9)
    ax.text(-0.2, 1.55, "• Columnas C-2 (Sótano): 35 x 35 cm (8 unidades, cuadro azul). Refuerzo: 6 Ø 5/8\" + estribos Ø 3/8\" @ 10 cm.", fontsize=6.8, color='#000000', zorder=9)
    ax.text(-0.2, 1.05, "• Concreto Armado: f'c = 250 kg/cm² — Acero de refuerzo: Fy = 4.200 kg/cm² (Cabillas corrugadas).", fontsize=6.8, color='#000000', zorder=9)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 3 regenerada.")


# =============================================================================
# LÁMINA 4: PLANO FACHADAS Y SECCIONES (FORMATO APAYSADO 17x11 in)
# =============================================================================
def build_sheet_4(pdf):
    fig = plt.figure(figsize=(17, 11), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "PLANO FACHADAS Y ELEVACIONES", 
                     "FACHADA PRINCIPAL (AV. 4) — FACHADA LATERAL IZQUIERDA — FACHADA POSTERIOR.", 
                     escala="1:75", is_landscape=True)

    # 1. FACHADA PRINCIPAL (AVENIDA 4)
    ax_prin = fig.add_axes([0.05, 0.54, 0.42, 0.36])
    ax_prin.set_aspect('equal')
    ax_prin.set_xlim(-1.5, 10.5)
    ax_prin.set_ylim(-1.5, 7.8)
    ax_prin.axis('off')

    ax_prin.text(4.5, -0.7, "FACHADA PRINCIPAL (AVENIDA 4)", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_prin.plot([1.0, 8.0], [-1.05, -1.05], color='black', lw=1.0)

    ax_prin.plot([-1.0, 10.0], [0.0, 0.0], color='#000000', lw=1.5)

    # Portón Garaje
    ax_prin.add_patch(Rectangle((0.40, 0.00), 2.25, 2.25, facecolor='#E8E8E8', edgecolor='#000000', lw=1.0))
    for gy in np.linspace(0.2, 2.05, 8):
        ax_prin.plot([0.40, 2.65], [gy, gy], color='#888888', lw=0.6)
    ax_prin.text(1.52, 1.10, "PORTÓN GARAJE", fontsize=6.0, ha='center', va='center')

    # Vitrinas Comerciales
    ax_prin.add_patch(Rectangle((3.15, 0.00), 2.50, 2.40, facecolor='#E0F7FA', edgecolor='#008080', lw=1.2))
    ax_prin.plot([4.40, 4.40], [0.00, 2.40], color='#008080', lw=0.8)
    ax_prin.text(4.40, 1.20, "VITRINA COMERCIAL 1", fontsize=5.8, ha='center', va='center', color='#006064')

    ax_prin.add_patch(Rectangle((6.20, 0.00), 2.60, 2.40, facecolor='#E0F7FA', edgecolor='#008080', lw=1.2))
    ax_prin.plot([7.50, 7.50], [0.00, 2.40], color='#008080', lw=0.8)
    ax_prin.text(7.50, 1.20, "VITRINA COMERCIAL 2", fontsize=5.8, ha='center', va='center', color='#006064')

    # Losa entrepiso
    ax_prin.add_patch(Rectangle((0.15, 2.85), 9.00, 0.15, facecolor='#B0B0B0', edgecolor='#000000', lw=0.8))

    # Ventanales Sala-Comedor
    ax_prin.add_patch(Rectangle((0.65, 3.85), 1.95, 1.40, facecolor='#E0F7FA', edgecolor='#008080', lw=1.0))
    for vx in np.linspace(1.15, 2.10, 3):
        ax_prin.plot([vx, vx], [3.85, 5.25], color='#008080', lw=0.6)
    ax_prin.text(1.62, 4.55, "Ventanal Sala", fontsize=5.8, ha='center', va='center', color='#006064')

    ax_prin.add_patch(Rectangle((3.15, 3.85), 2.35, 1.40, facecolor='#E0F7FA', edgecolor='#008080', lw=1.0))
    for vx in np.linspace(3.75, 4.90, 3):
        ax_prin.plot([vx, vx], [3.85, 5.25], color='#008080', lw=0.6)
    ax_prin.text(4.32, 4.55, "Ventanal Comedor", fontsize=5.8, ha='center', va='center', color='#006064')

    # Balcón Master Suite
    ax_prin.add_patch(Rectangle((6.00, 3.00), 3.00, 1.05, facecolor='#DEDEDE', edgecolor='#000000', lw=1.0))
    ax_prin.plot([6.00, 9.00], [4.05, 4.05], color='#000000', lw=1.2)
    for bx in np.linspace(6.30, 8.70, 9):
        ax_prin.plot([bx, bx], [3.00, 4.05], color='#444444', lw=0.6)
    ax_prin.text(7.50, 3.55, "BALCÓN MASTER SUITE", fontsize=5.8, ha='center', va='center', fontweight='bold')

    ax_prin.add_patch(Rectangle((-0.10, 5.85), 9.50, 0.20, facecolor='#909090', edgecolor='#000000', lw=1.0))

    ax_prin.text(-0.6, 0.05, "N.P.T. ±0,00", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-0.6, 3.05, "N.P.T. +3,00", fontsize=6.2, fontweight='bold', ha='right')
    ax_prin.text(-0.6, 6.05, "N.P.T. +6,00", fontsize=6.2, fontweight='bold', ha='right')


    # 2. FACHADA POSTERIOR
    ax_post = fig.add_axes([0.52, 0.54, 0.43, 0.36])
    ax_post.set_aspect('equal')
    ax_post.set_xlim(-1.5, 10.5)
    ax_post.set_ylim(-4.2, 7.8)
    ax_post.axis('off')

    ax_post.text(4.5, -3.3, "FACHADA POSTERIOR (SÓTANO - P.B. - P.A.)", fontsize=8.5, fontweight='bold', ha='center', va='top')
    ax_post.plot([1.0, 8.0], [-3.65, -3.65], color='black', lw=1.0)

    # Sótano
    ax_post.add_patch(Rectangle((0.30, -2.55), 6.10, 2.55, facecolor='#EAEAEA', edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((6.40, -2.55), 2.75, 2.55, facecolor='#D8D8D8', edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((0.60, -1.55), 1.90, 1.10, facecolor='#E0F7FA', edgecolor='#008080', lw=0.8))
    ax_post.text(1.55, -1.00, "Ventana Sótano", fontsize=5.5, ha='center', va='center')

    # Planta Baja
    ax_post.add_patch(Rectangle((0.15, 0.00), 6.25, 3.00, facecolor='#F5F5F5', edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((0.55, 1.15), 1.80, 1.45, facecolor='#E0F7FA', edgecolor='#008080', lw=0.8))
    ax_post.text(1.45, 1.85, "Ventana Depósito", fontsize=5.5, ha='center', va='center')

    # Planta Alta
    ax_post.add_patch(Rectangle((0.15, 3.00), 9.00, 3.00, facecolor='#FFFFFF', edgecolor='#000000', lw=1.0))
    ax_post.add_patch(Rectangle((0.60, 4.10), 1.70, 1.15, facecolor='#E0F7FA', edgecolor='#008080', lw=0.8))
    ax_post.text(1.45, 4.70, "Lavandería P.A.", fontsize=5.5, ha='center', va='center')
    ax_post.add_patch(Rectangle((3.60, 3.95), 1.80, 1.20, facecolor='#E0F7FA', edgecolor='#008080', lw=0.8))
    ax_post.text(4.50, 4.55, "Terraza Posterior", fontsize=5.5, ha='center', va='center')

    ax_post.add_patch(Rectangle((-0.10, 5.85), 9.50, 0.20, facecolor='#909090', edgecolor='#000000', lw=1.0))


    # 3. FACHADA LATERAL IZQUIERDA
    ax_lat = fig.add_axes([0.05, 0.14, 0.90, 0.34])
    ax_lat.set_aspect('equal')
    ax_lat.set_xlim(-2.0, 26.5)
    ax_lat.set_ylim(-5.5, 7.8)
    ax_lat.axis('off')

    # Perfil del Terreno y Relleno de Estrato Geotécnico
    steps_x = [24.71, 15.5, 14.5, 13.5, 12.5, 11.5, 10.5, 8.5, 0.0]
    steps_z = [ 0.00,  0.0, -0.4, -0.8, -1.2, -1.6, -2.0, -2.55, -2.55]
    # Polígono de suelo bajo el talud
    ground_poly = [(0.0, -4.0)] + list(zip(steps_x, steps_z)) + [(24.71, -4.0)]
    ax_lat.add_patch(Polygon(ground_poly, closed=True, facecolor='#EFEBE9', edgecolor='none', zorder=1))
    ax_lat.plot(steps_x, steps_z, color=COLOR_TERRAIN, lw=2.2, zorder=4)
    ax_lat.text(13.0, -2.2, "PERFIL DE TERRENO NATURAL Y TALUD", fontsize=7.0, color=COLOR_TERRAIN, fontweight='bold')

    # Muro Propio Planta Baja y Planta Alta
    ax_lat.add_patch(Rectangle((0.00, 0.00), 21.71, 3.00, facecolor='#FAFAFA', edgecolor='#000000', lw=1.2, zorder=2))
    ax_lat.add_patch(Rectangle((0.00, 3.00), 21.71, 2.85, facecolor='#FFFFFF', edgecolor='#000000', lw=1.2, zorder=2))

    # Muro de Sótano posterior
    ax_lat.add_patch(Rectangle((0.00, -2.55), 8.30, 2.55, facecolor='#EEEEEE', edgecolor='#000000', lw=1.2, zorder=2))

    # Ventanas con marcos
    for vy in [1.5, 5.5, 10.5, 16.5, 19.5]:
        ax_lat.add_patch(Rectangle((vy, 4.0), 1.5, 1.2, facecolor='#E0F7FA', edgecolor='#008080', lw=0.9, zorder=3))
        ax_lat.plot([vy, vy + 1.5], [4.6, 4.6], color='#008080', lw=0.6, zorder=4)

    # Cubierta superior con voladizo
    ax_lat.add_patch(Rectangle((-0.5, 5.85), 22.71, 0.25, facecolor='#808080', edgecolor='#000000', lw=1.0, zorder=5))

    ax_lat.text(23.2, 1.5, "AVENIDA 4\n(FRENTE EXTENDIDO)", fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax_lat.text(3.0, -1.2, "SÓTANO\n(Z = -2,55 m)", fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax_lat.text(15.0, 1.5, "PLANTA BAJA: GARAJE TECHADO\n(MURO PROPIO CONTINUO)", fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax_lat.text(15.0, 4.5, "PLANTA ALTA: APARTAMENTO RESIDENCIAL", fontsize=7.2, fontweight='bold', ha='center', va='center')

    # Título sin colisión con el dibujo
    ax_lat.text(12.5, -4.4, "FACHADA LATERAL IZQUIERDA (SÓTANO + P.B. + P.A. + TALUD DE TERRENO)", 
                fontsize=9.5, fontweight='bold', ha='center', va='top')

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 4 regenerada.")


# =============================================================================
# LÁMINA 5: LEVANTAMIENTO POLIGONAL DE LINDEROS, RETÍCULA UTM Y SITUACIÓN
# =============================================================================
def build_sheet_5(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    draw_sheet_frame(fig, ax_frame, "LEVANTAMIENTO POLIGONAL DE LINDEROS", 
                     "TOPOGRAFÍA Y COORDENADAS U.T.M. — SITUACIÓN RELATIVA.", escala="1:200")

    # 1. TABLA CUADRO DE COORDENADAS U.T.M.
    ax_tbl = fig.add_axes([0.05, 0.77, 0.44, 0.16])
    ax_tbl.axis('off')
    ax_tbl.text(0.5, 0.98, "CUADRO DE COORDENADAS U.T.M.", fontsize=8.0, 
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

    # 3. SITUACIÓN RELATIVA S/ESC
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
    ax_sit.text(4.15, 4.1, "LOTE", fontsize=5.5, color='white', fontweight='bold', ha='center', va='center')

    ax_sit.text(1.5, 2.65, "Calle 30", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(1.5, 5.15, "Calle 31", fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(2.65, 7.0, "Av. Libertador", rotation=90, fontsize=5.0, ha='center', color='#555555')
    ax_sit.text(5.15, 7.0, "Avenida 4", rotation=90, fontsize=5.0, ha='center', color='#555555')

    # 4. CUADRO DE ÁREAS ACTUALIZADO
    ax_areas = fig.add_axes([0.05, 0.71, 0.44, 0.05])
    ax_areas.axis('off')
    ax_areas.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FFF8E1', edgecolor=COLOR_BORDER, lw=1.0))
    ax_areas.text(0.05, 0.70, "ÁREA DE TERRENO: 273,81 m²", fontsize=7.5, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.05, 0.35, "ÁREA DE CONSTRUCCIÓN TOTAL: 372,50 m²", fontsize=7.2, fontweight='bold', color=COLOR_HEADER_RED)
    ax_areas.text(0.05, 0.08, "(Sótano: 80,45 m²  |  Planta Baja: 149,85 m²  |  Planta Alta: 142,20 m²)", fontsize=5.8, color='#000000')

    # 5. RETÍCULA Y POLÍGONO UTM
    ax_utm = fig.add_axes([0.05, 0.12, 0.90, 0.58])
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
        ax_utm.text(e + 0.6, 1141637, f"E.={e:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), 
                    rotation=90, fontsize=6.5, fontweight='bold', color='#000000')

    poly_pts = [
        (529755.04, 1141664.17), # P-1
        (529764.60, 1141670.33), # P-2
        (529777.07, 1141648.99), # P-3
        (529767.99, 1141643.13)  # P-4
    ]
    poly_patch = Polygon(poly_pts, closed=True, facecolor='#FFF9C4', edgecolor='#FF0000', lw=1.5, zorder=3)
    ax_utm.add_patch(poly_patch)

    # Impronta de la nueva edificación extendida a la Avenida 4
    house_pts = [
        (529755.30, 1141664.00),
        (529763.50, 1141669.20),
        (529773.80, 1141651.80),
        (529770.80, 1141649.90),
        (529772.00, 1141647.80),
        (529768.20, 1141645.40),
        (529759.50, 1141657.00)
    ]
    ax_utm.add_patch(Polygon(house_pts, closed=True, facecolor='#E0E0E0', edgecolor='#000000', lw=1.2, hatch='///', zorder=4))

    for i, (vx, vy) in enumerate(poly_pts):
        ax_utm.add_patch(Circle((vx, vy), 0.45, facecolor='white', edgecolor='#FF0000', lw=1.2, zorder=6))
        ax_utm.text(vx, vy, f"P-{i+1}", fontsize=7.2, fontweight='bold', ha='center', va='center', zorder=7)

    # Rótulos de dimensiones de linderos
    ax_utm.text(529759.8, 1141667.5, "11,37 m", fontsize=6.8, rotation=32, ha='center', va='bottom', color='#B71C1C', fontweight='bold')
    ax_utm.text(529771.5, 1141660.0, "24,72 m", fontsize=6.8, rotation=-58, ha='center', va='bottom', color='#B71C1C', fontweight='bold')
    ax_utm.text(529772.5, 1141645.5, "10,81 m", fontsize=6.8, rotation=32, ha='center', va='top', color='#B71C1C', fontweight='bold')
    ax_utm.text(529761.0, 1141653.0, "24,70 m", fontsize=6.8, rotation=-58, ha='center', va='top', color='#B71C1C', fontweight='bold')

    ax_utm.text(529762.0, 1141673.0, "AVENIDA 4 (ANCHO 11,37 m)", fontsize=7.5, fontweight='bold', rotation=32, ha='center', color='#333333')
    ax_utm.text(529775.0, 1141663.0, "CASA DE\nMIGUEL RODRIGUEZ", fontsize=7.0, ha='center', rotation=-58, color='#444444')
    ax_utm.text(529774.0, 1141643.0, "SOLAR DE\nMIGUEL RODRIGUEZ", fontsize=7.0, ha='center', color='#444444')
    ax_utm.text(529758.0, 1141648.0, "CASA DE\nMARIO GRATEROL", fontsize=7.0, ha='center', rotation=-58, color='#444444')

    draw_north_arrow(ax_utm, 529788.0, 1141673.0, size=2.5)

    pdf.savefig(fig)
    plt.close(fig)
    print("Lámina 5 regenerada.")


def generate_all_sheets():
    output_pdf = "01_Planos_y_Documentacion/planos_casa_completo.pdf"
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    print(f"Generando documento PDF oficial: {output_pdf}...")

    with PdfPages(output_pdf) as pdf:
        build_sheet_1(pdf)
        build_sheet_2(pdf)
        build_sheet_3(pdf)
        build_sheet_4(pdf)
        build_sheet_5(pdf)

    print(f"¡Éxito total! Se ha generado '{output_pdf}' con las 5 láminas arquitectónicas completas.")

if __name__ == '__main__':
    generate_all_sheets()
