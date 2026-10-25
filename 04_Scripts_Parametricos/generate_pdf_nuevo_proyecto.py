"""
Generador Oficial de Planos Arquitectónicos en PDF ("01_Planos_y_Documentacion/planos_nuevo_proyecto.pdf")
Estilo Normativo Municipal inspirado fielmente en "planos de casa.pdf" (Independencia, Yaracuy).
Sincronizado 100% al milímetro con el modelo maestro "02_Modelos_CAD/casa_nuevo_proyecto.dxf".

Contenido del Portafolio (6 Láminas Formato Tabloide 11 x 17 pulgadas, 300 DPI Vectorial):
- Lámina 1/6: Planta Arquitectónica Nivel Sótano y Patio Jardín con Pérgola (Z = -2,55 m) — Esc. 1:50
- Lámina 2/6: Planta Arquitectónica Planta Baja: Frutería, Gran Almacén y Estacionamiento (Z = ±0,00 m) — Esc. 1:75
- Lámina 3/6: Planta Arquitectónica Segundo Piso Residencial Chalet + Buhardilla Tanque 1.000L — Esc. 1:75 / 1:50
- Lámina 4/6: Plano Distribución de Columnas, Ejes Estructurales y Sistema de Cubierta — Esc. 1:75
- Lámina 5/6: Plano de Fachadas Arquitectónicas (Principal Av. 4, Posterior Sur y Lateral con Terreno) — Esc. 1:75
- Lámina 6/6: Levantamiento Poligonal de Linderos, Retícula U.T.M., Cuadro de Áreas y Situación Relativa — Esc. 1:200
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages

# =============================================================================
# PALETA OFICIAL ESTILO "planos de casa.pdf" + ACENTOS TÉCNICOS ARQUITECTÓNICOS
# =============================================================================
C_BLUE       = '#0000DD'   # Marco normativo doble y líneas del cajetín
C_RED        = '#D80000'   # Encabezados institucionales, títulos y datos propietario
C_WALL_FILL  = '#757575'   # Poché gris arquitectónico limpio de muros cortados
C_WALL_EDGE  = '#151515'   # Contorno nítido de muros
C_NEIGHBOR   = '#C8C8C8'   # Pared colindante del vecino izquierdo (intacta)
C_WINDOW     = '#007799'   # Vidrios y carpintería de ventanas
C_DOOR       = '#3E2723'   # Hojas de puertas y carpintería de madera
C_FURN_EDGE  = '#5D5D5D'   # Contorno fino de mobiliario fijo y equipamiento
C_WOOD_SOFT  = '#EFE6DD'   # Relleno suave madera (mesones, islas, estantes, camas)
C_STONE_SOFT = '#E4E8EB'   # Relleno suave piedra laja / duchas / terrazas
C_GREEN_SOFT = '#E8F5E9'   # Jardineras, vegetación y detalles frescos
C_COLD_SOFT  = '#E1F5FE'   # Cuarto frío / equipos hidroneumáticos
C_COL_RED    = '#DF0000'   # Columnas estructurales achuradas
C_AXIS_CYAN  = '#0097A7'   # Ejes estructurales y vigas en planta estructural
C_DIM        = '#222222'   # Líneas y textos de cotas

WHITE_HALO = dict(boxstyle='square,pad=0.06', facecolor='white', edgecolor='none', alpha=0.88)


def fmt_m(val):
    """Formatea metros con coma decimal estilo venezolano (ej. 3,00)."""
    return f"{val:.2f}".replace('.', ',')


def draw_sheet_frame(fig, title_line1, title_line2="", escala="1:75", sheet_num="1 / 6", fecha="OCT 2026"):
    """Dibuja el marco doble azul reglamentario y el cajetín fiel a 'planos de casa.pdf'."""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Doble marco perimetral azul
    ax.add_patch(Rectangle((0.018, 0.014), 0.964, 0.972, fill=False, edgecolor=C_BLUE, lw=2.2))
    ax.add_patch(Rectangle((0.022, 0.018), 0.956, 0.964, fill=False, edgecolor=C_BLUE, lw=0.9))

    # Membrete Institucional Superior Izquierdo (idéntico a planos de casa.pdf)
    ax.text(0.030, 0.973, "REPÚBLICA BOLIVARIANA DE VENEZUELA",
            fontsize=13.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')
    ax.text(0.030, 0.955, "MUNICIPIO INDEPENDENCIA YARACUY",
            fontsize=12.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')

    # Identificador de Proyecto Superior Derecho (limpio y elegante)
    ax.text(0.970, 0.972, "PROYECTO INTEGRAL: CHALET RÚSTICO ALPINO & COMERCIO",
            fontsize=8.5, fontweight='bold', color='#263238', family='sans-serif', va='top', ha='right')
    ax.text(0.970, 0.956, f"MODELO MAESTRO VERIFICADO  |  LÁMINA {sheet_num}",
            fontsize=7.8, fontweight='bold', color=C_BLUE, family='sans-serif', va='top', ha='right')

    # Cajetín Inferior Reglamentario
    c_left, c_right = 0.022, 0.978
    c_bot = 0.018
    row_top = 0.058
    caj_top = 0.096

    ax.plot([c_left, c_right], [caj_top, caj_top], color=C_BLUE, lw=1.6)
    ax.plot([c_left, c_right], [row_top, row_top], color=C_BLUE, lw=1.2)

    # Banda de título del plano (cero desbordamiento lateral y jerarquía limpia)
    if title_line2:
        ax.text(0.032, caj_top - 0.012, title_line1, fontsize=10.2, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')
        ax.text(0.032, caj_top - 0.028, title_line2, fontsize=7.6, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')
    else:
        ax.text(0.032, (caj_top + row_top) / 2, title_line1, fontsize=11.0, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')

    # Subtítulo descriptivo derecho en la banda de título
    ax.text(0.968, caj_top - 0.012,
            "ARQUITECTURA EN PIEDRA RÚSTICA Y MADERA",
            fontsize=6.8, fontweight='bold', color='#37474F', ha='right', va='center')
    ax.text(0.968, caj_top - 0.028,
            "RESPETO ESTRICTO DE LINDEROS (0,00 m INVASIÓN)",
            fontsize=6.4, fontweight='bold', color=C_BLUE, ha='right', va='center')

    # Divisiones verticales de celdas inferiores (cero desborde de textos)
    cols = [0.275, 0.465, 0.665, 0.825, 0.905]
    for cx in cols:
        ax.plot([cx, cx], [c_bot, row_top], color=C_BLUE, lw=1.0)

    # 1. UBICACIÓN
    ax.text(0.026, row_top - 0.008, "UBICACIÓN:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.148, row_top - 0.020, "AVENIDA 4 ENTRE CALLES 30 Y 31 30-7",
            fontsize=7.0, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.148, row_top - 0.031, "MUNICIPIO INDEPENDENCIA ESTADO YARACUY.",
            fontsize=6.6, fontweight='bold', color=C_RED, ha='center')

    # 2. PROPIEDAD
    ax.text(0.279, row_top - 0.008, "PROPIEDAD:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.370, row_top - 0.020, "ALVARO ARGELIO DIAZ FLOREZ.",
            fontsize=7.2, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.370, row_top - 0.031, "C.I.: 24.633.787",
            fontsize=7.0, fontweight='bold', color=C_RED, ha='center')

    # 3. LEVANTADO CALCULADO Y DIGITALIZO
    ax.text(0.469, row_top - 0.008, "LEVANTADO CALCULADO Y DIGITALIZO:", fontsize=5.6, fontweight='bold', color=C_BLUE)
    ax.text(0.565, row_top - 0.020, "T.S.U. ANGEL CAMACARO M.",
            fontsize=7.3, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.565, row_top - 0.031, "CVPT.: N° 1260         SOVIT.: N° 0050",
            fontsize=6.3, fontweight='bold', color=C_RED, ha='center')

    # 4. REVISADO
    ax.text(0.669, row_top - 0.008, "REVISADO:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.745, row_top - 0.022, "PROYECTO REDISEÑO\nCHALET ALPINO",
            fontsize=6.4, fontweight='bold', color='#1B5E20', ha='center', va='center')

    # 5. FECHA
    ax.text(0.829, row_top - 0.008, "FECHA:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.865, row_top - 0.024, fecha, fontsize=8.0, fontweight='bold', color=C_RED, ha='center')

    # 6. ESCALA
    ax.text(0.909, row_top - 0.008, "ESCALA:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.942, row_top - 0.024, escala, fontsize=8.5, fontweight='bold', color=C_RED, ha='center')

    return ax


# =============================================================================
# PRIMITIVAS DE DIBUJO ARQUITECTÓNICO DE ALTA PRECISIÓN
# =============================================================================
def draw_wall(ax, x1, y1, x2, y2, facecolor=C_WALL_FILL, zorder=5):
    rx, ry = min(x1, x2), min(y1, y2)
    rw, rh = abs(x2 - x1), abs(y2 - y1)
    if rw < 1e-4 or rh < 1e-4:
        return
    ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=facecolor, edgecolor=C_WALL_EDGE, lw=0.75, zorder=zorder))


def draw_wall_x_openings(ax, x1, x2, y1, y2, openings, facecolor=C_WALL_FILL):
    """Dibuja muro horizontal con vanos limpios [(ox1, ox2, tipo), ...]."""
    cur_x = x1
    for ox1, ox2, kind in sorted(openings, key=lambda t: t[0]):
        if ox1 > cur_x + 1e-3:
            draw_wall(ax, cur_x, y1, ox1, y2, facecolor=facecolor)
        if kind == 'win':
            draw_window_h(ax, ox1, ox2, y1, y2)
        elif kind == 'shutter_win':
            draw_window_h(ax, ox1, ox2, y1, y2, shutters=True)
        cur_x = ox2
    if x2 > cur_x + 1e-3:
        draw_wall(ax, cur_x, y1, x2, y2, facecolor=facecolor)


def draw_wall_y_openings(ax, x1, x2, y1, y2, openings, facecolor=C_WALL_FILL):
    """Dibuja muro vertical con vanos limpios [(oy1, oy2, tipo), ...]."""
    cur_y = y1
    for oy1, oy2, kind in sorted(openings, key=lambda t: t[0]):
        if oy1 > cur_y + 1e-3:
            draw_wall(ax, x1, cur_y, x2, oy1, facecolor=facecolor)
        if kind == 'win':
            draw_window_v(ax, x1, x2, oy1, oy2)
        elif kind == 'shutter_win':
            draw_window_v(ax, x1, x2, oy1, oy2, shutters=True)
        cur_y = oy2
    if y2 > cur_y + 1e-3:
        draw_wall(ax, x1, cur_y, x2, y2, facecolor=facecolor)


def draw_window_h(ax, x1, x2, y1, y2, shutters=False):
    ym = 0.5 * (y1 + y2)
    h = abs(y2 - y1)
    ax.add_patch(Rectangle((x1, min(y1, y2)), x2 - x1, h, facecolor='#F2FBFF', edgecolor=C_WALL_EDGE, lw=0.55, zorder=5))
    ax.plot([x1, x2], [ym - 0.022, ym - 0.022], color=C_WINDOW, lw=0.75, zorder=6)
    ax.plot([x1, x2], [ym + 0.022, ym + 0.022], color=C_WINDOW, lw=0.75, zorder=6)
    if shutters:
        ax.add_patch(Rectangle((x1 - 0.16, min(y1, y2) - 0.03), 0.16, 0.04, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))
        ax.add_patch(Rectangle((x2, min(y1, y2) - 0.03), 0.16, 0.04, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))


def draw_window_v(ax, x1, x2, y1, y2, shutters=False):
    xm = 0.5 * (x1 + x2)
    w = abs(x2 - x1)
    ax.add_patch(Rectangle((min(x1, x2), y1), w, y2 - y1, facecolor='#F2FBFF', edgecolor=C_WALL_EDGE, lw=0.55, zorder=5))
    ax.plot([xm - 0.022, xm - 0.022], [y1, y2], color=C_WINDOW, lw=0.75, zorder=6)
    ax.plot([xm + 0.022, xm + 0.022], [y1, y2], color=C_WINDOW, lw=0.75, zorder=6)
    if shutters:
        ax.add_patch(Rectangle((max(x1, x2) + 0.01, y1 - 0.16), 0.04, 0.16, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))
        ax.add_patch(Rectangle((max(x1, x2) + 0.01, y2), 0.04, 0.16, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))


def draw_door(ax, hx, hy, width, theta_leaf, theta_closed):
    """Puerta abatible estilo planos de casa.pdf (hoja doble línea + arco fino)."""
    rad = math.radians(theta_leaf)
    lx = hx + width * math.cos(rad)
    ly = hy + width * math.sin(rad)
    ax.plot([hx, lx], [hy, ly], color=C_DOOR, lw=1.25, zorder=6)
    t1, t2 = min(theta_leaf, theta_closed), max(theta_leaf, theta_closed)
    ax.add_patch(Arc((hx, hy), 2 * width, 2 * width, angle=0, theta1=t1, theta2=t2,
                     color='#666666', lw=0.55, linestyle='-', zorder=4))


def draw_double_door_h(ax, x1, x2, y_hinge, open_up=True):
    """Puerta doble simétrica horizontal."""
    w = 0.5 * (x2 - x1)
    if open_up:
        draw_door(ax, x1, y_hinge, w, 90, 0)
        draw_door(ax, x2, y_hinge, w, 90, 180)
    else:
        draw_door(ax, x1, y_hinge, w, 270, 360)
        draw_door(ax, x2, y_hinge, w, 270, 180)


def draw_col(ax, cx, cy, size=0.25, hatched=False):
    s2 = 0.5 * size
    if hatched:
        ax.add_patch(Rectangle((cx - s2, cy - s2), size, size, facecolor='#FFEBEE',
                               edgecolor=C_COL_RED, lw=1.0, hatch='////', zorder=8))
    else:
        ax.add_patch(Rectangle((cx - s2, cy - s2), size, size, facecolor='#525252',
                               edgecolor='#111111', lw=0.75, zorder=7))


def draw_stairs_numbered(ax, x1, y1, x2, y2, n_steps, direction='down_y', label_txt='SUBE'):
    """Escalera numerada peldaño a peldaño exactamente como en planos de casa.pdf."""
    ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor='#FAFAFA', edgecolor='#222222', lw=0.75, zorder=3))
    dy = (y2 - y1) / n_steps
    xm = 0.5 * (x1 + x2)
    for i in range(n_steps + 1):
        yy = y1 + i * dy
        ax.plot([x1, x2], [yy, yy], color='#444444', lw=0.55, zorder=4)
    for i in range(n_steps):
        idx = (i + 1) if direction == 'up_y' else (n_steps - i)
        yc = y1 + (i + 0.5) * dy
        ax.text(x1 + 0.16, yc, str(idx), fontsize=4.6, color='#444444', ha='center', va='center', zorder=5)
    if direction == 'up_y':
        ax.annotate('', xy=(xm + 0.08, y2 - 0.18), xytext=(xm + 0.08, y1 + 0.18),
                    arrowprops=dict(arrowstyle='->', color='#111111', lw=0.9), zorder=6)
    else:
        ax.annotate('', xy=(xm + 0.08, y1 + 0.18), xytext=(xm + 0.08, y2 - 0.18),
                    arrowprops=dict(arrowstyle='->', color='#111111', lw=0.9), zorder=6)
    ax.text(xm + 0.08, 0.5 * (y1 + y2), label_txt, fontsize=5.2, fontweight='bold',
            color='#111111', ha='center', va='center', bbox=WHITE_HALO, zorder=7)


def draw_dim_h(ax, x1, x2, y_line, val_str=None, y_ref=None, fontsize=6.2, color=C_DIM):
    """Cota arquitectónica horizontal estilo venezolano (ticks + texto con halo blanco)."""
    if val_str is None:
        val_str = fmt_m(abs(x2 - x1))
    ax.plot([x1, x2], [y_line, y_line], color=color, lw=0.55, zorder=9)
    tk = 0.08
    for xx in (x1, x2):
        ax.plot([xx, xx], [y_line - tk, y_line + tk], color=color, lw=0.75, zorder=9)
        ax.plot([xx - tk * 0.7, xx + tk * 0.7], [y_line - tk * 0.7, y_line + tk * 0.7], color=color, lw=0.65, zorder=9)
        if y_ref is not None:
            ax.plot([xx, xx], [y_ref, y_line], color='#888888', lw=0.35, linestyle='--', zorder=2)
    ax.text(0.5 * (x1 + x2), y_line + 0.06, val_str, fontsize=fontsize, fontweight='bold',
            color=color, ha='center', va='bottom', bbox=WHITE_HALO, zorder=10)


def draw_dim_v(ax, x_line, y1, y2, val_str=None, x_ref=None, fontsize=6.2, color=C_DIM, text_side='left'):
    """Cota arquitectónica vertical estilo venezolano."""
    if val_str is None:
        val_str = fmt_m(abs(y2 - y1))
    ax.plot([x_line, x_line], [y1, y2], color=color, lw=0.55, zorder=9)
    tk = 0.08
    for yy in (y1, y2):
        ax.plot([x_line - tk, x_line + tk], [yy, yy], color=color, lw=0.75, zorder=9)
        ax.plot([x_line - tk * 0.7, x_line + tk * 0.7], [yy - tk * 0.7, yy + tk * 0.7], color=color, lw=0.65, zorder=9)
        if x_ref is not None:
            ax.plot([x_ref, x_line], [yy, yy], color='#888888', lw=0.35, linestyle='--', zorder=2)
    dx = -0.08 if text_side == 'left' else 0.08
    ha = 'right' if text_side == 'left' else 'left'
    ax.text(x_line + dx, 0.5 * (y1 + y2), val_str, fontsize=fontsize, fontweight='bold',
            color=color, ha=ha, va='center', rotation=90, bbox=WHITE_HALO, zorder=10)


def draw_north(ax, x, y, r=0.55):
    """Rosa de los vientos arquitectónica elegante."""
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor='#222222', lw=0.9, zorder=10))
    pts_n = [(x, y + r * 0.92), (x - r * 0.28, y - r * 0.25), (x, y - r * 0.05)]
    pts_s = [(x, y + r * 0.92), (x + r * 0.28, y - r * 0.25), (x, y - r * 0.05)]
    ax.add_patch(Polygon(pts_n, closed=True, facecolor='#111111', edgecolor='#111111', zorder=11))
    ax.add_patch(Polygon(pts_s, closed=True, facecolor='#BBBBBB', edgecolor='#111111', lw=0.5, zorder=11))
    ax.text(x, y + r + 0.12, "N", fontsize=8.5, fontweight='bold', color='#111111', ha='center', va='bottom', zorder=11)


def draw_bed(ax, x1, y1, x2, y2, head='west'):
    """Dibuja cama arquitectónica en planta con almohadas y sobrecama."""
    ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor='#FAF8F5', edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    w, h = x2 - x1, y2 - y1
    if head == 'west':
        ax.add_patch(Rectangle((x1, y1), 0.10, h, facecolor='#8D6E63', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x1 + 0.14, y1 + 0.12), 0.34, h * 0.36, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x1 + 0.14, y2 - 0.12 - h * 0.36), 0.34, h * 0.36, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.plot([x1 + 0.62, x1 + 0.62], [y1, y2], color=C_FURN_EDGE, lw=0.5, zorder=4)
    elif head == 'east':
        ax.add_patch(Rectangle((x2 - 0.10, y1), 0.10, h, facecolor='#8D6E63', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x2 - 0.48, y1 + 0.12), 0.34, h * 0.36, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x2 - 0.48, y2 - 0.12 - h * 0.36), 0.34, h * 0.36, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.plot([x2 - 0.62, x2 - 0.62], [y1, y2], color=C_FURN_EDGE, lw=0.5, zorder=4)


def draw_wc(ax, x, y, orientation='east'):
    """Dibuja inodoro arquitectónico en planta."""
    if orientation == 'east':
        ax.add_patch(Rectangle((x, y - 0.20), 0.20, 0.40, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
        ax.add_patch(Circle((x + 0.40, y), 0.19, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    elif orientation == 'north':
        ax.add_patch(Rectangle((x - 0.20, y), 0.40, 0.20, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
        ax.add_patch(Circle((x, y + 0.40), 0.19, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))


# Columnas maestras compartidas con build_nuevo_proyecto.py
SOT_COLS = [
    (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
    (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
    (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
]

PB_P2_COLS = [
    (0.275, 21.585), (2.825, 21.585), (5.925, 21.585), (9.075, 21.585),
    (0.275, 18.575), (2.825, 18.575), (5.925, 18.575), (9.075, 18.575),
    (0.275, 16.325), (2.825, 16.325), (5.925, 16.325),
    (9.075, 14.625),
    (0.275, 12.025), (2.825, 12.025), (5.925, 12.025), (9.075, 12.025),
    (0.275, 8.875),  (2.825, 8.875),  (5.925, 8.875),  (9.075, 8.875),
    (0.275, 6.575),  (2.825, 6.575),  (5.925, 6.575),  (9.075, 6.575),
    (0.275, 3.575),  (2.825, 3.575),  (5.925, 3.575),  (9.075, 3.575),
    (0.275, 0.125),  (2.825, 0.125),  (5.925, 0.125),  (9.075, 0.125),
]


# =============================================================================
# LÁMINA 1: PLANTA ARQUITECTÓNICA NIVEL SÓTANO Y PATIO JARDÍN (Z = -2,55 m)
# =============================================================================
def build_sheet_1_sotano(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — NIVEL SÓTANO Y JARDÍN",
                     "DISTRIBUCIÓN: CAVA DE VINOS, SALÓN CINE, TABERNA, SUITE HUÉSPEDES Y PÉRGOLA (Z = -2,55 m).",
                     escala="1:50", sheet_num="1 / 6")

    ax = fig.add_axes([0.05, 0.25, 0.90, 0.67])
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 11.4)
    ax.set_ylim(-3.8, 9.8)
    ax.axis('off')

    draw_north(ax, 10.4, 8.6, r=0.45)

    # Pared vecino izquierdo intacta (X = 0.00..0.15)
    ax.add_patch(Rectangle((0.00, -3.00), 0.15, 11.30, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 3.0, "PARED VECINO COLINDANTE (INTACTA — 0,00 m INVASIÓN)", rotation=90,
            fontsize=6.5, fontweight='bold', color='#666666', ha='right', va='center')

    # Piso interior del Sótano y Patio Trasero
    ax.add_patch(Rectangle((0.30, 0.15), 8.65, 8.00, facecolor='#FCFCFA', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.15, -3.00), 9.95, 3.00, facecolor='#F6F9F4', edgecolor='#999999', lw=0.6, linestyle='--', zorder=1))
    ax.add_patch(Rectangle((9.15, 0.00), 0.95, 8.30, facecolor='#F6F9F4', edgecolor='#999999', lw=0.6, linestyle='--', zorder=1))
    ax.text(9.62, 4.15, "CORREDOR JARDÍN ESTE (Z = -2,55 m)", rotation=90, fontsize=6.0, color='#2E7D32', fontweight='bold', ha='center', va='center')

    # Terraza de Piedra Laja y Pérgola Rústica en Patio Trasero (X: 4.85..9.05, Y: -2.20..0.00)
    ax.add_patch(Rectangle((4.85, -2.20), 4.20, 2.20, facecolor=C_STONE_SOFT, edgecolor='#546E7A', lw=0.9, zorder=2))
    for r_i in range(9):
        rx = 4.96 + r_i * 0.49
        ax.plot([rx, rx], [-2.20, 0.00], color='#8D6E63', lw=1.0, linestyle='--', alpha=0.65, zorder=3)
    for pg_x in [4.95, 6.91, 8.82]:
        ax.add_patch(Rectangle((pg_x - 0.04, -2.14), 0.24, 0.24, facecolor='#6D4C41', edgecolor='black', lw=0.7, zorder=4))
    # Muebles exteriores pérgola + jardinera piedra sur
    ax.add_patch(Rectangle((5.05, -2.02), 1.17, 0.70, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((5.35, -1.16), 0.70, 0.48, facecolor='#CFD8DC', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((8.18, -1.96), 0.66, 0.66, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((0.65, -0.52), 1.80, 0.48, facecolor=C_GREEN_SOFT, edgecolor='#2E7D32', lw=0.7, zorder=3))
    ax.text(1.55, -0.28, "Jardinera Piedra", fontsize=5.8, color='#1B5E20', ha='center', va='center', fontweight='bold')
    ax.text(6.95, -2.48, "TERRAZA DE PIEDRA LAJA Y PÉRGOLA RÚSTICA (4,20 x 2,20 m = 9,24 m²)",
            fontsize=6.8, fontweight='bold', color='#3E2723', ha='center', va='top')

    # Muros Perimetrales del Sótano
    draw_wall(ax, 0.15, 0.00, 0.30, 8.30)  # Oeste propio ciego
    draw_wall(ax, 0.15, 8.15, 9.15, 8.30)  # Contención Norte
    draw_wall_x_openings(ax, 0.30, 9.15, 0.00, 0.15, [
        (0.75, 2.35, 'shutter_win'),
        (3.25, 4.30, 'win'),
        (4.88, 5.68, 'win'),
        (6.35, 8.55, 'door_gap'),
    ])
    # Doble puerta francesa abierta hacia afuera (2,20 m)
    draw_double_door_h(ax, 6.35, 8.55, 0.00, open_up=False)
    ax.text(7.45, -0.22, "Doble Puerta Francesa (2,20 m)", fontsize=5.8, fontweight='bold', color=C_DOOR, ha='center', bbox=WHITE_HALO, zorder=8)

    draw_wall_y_openings(ax, 8.95, 9.15, 0.15, 8.30, [
        (1.00, 2.65, 'shutter_win'),
        (4.25, 5.90, 'shutter_win'),
        (7.00, 7.95, 'win'),
    ])

    # Tabiquería Interna del Sótano (Opción A)
    draw_wall_y_openings(ax, 1.40, 1.55, 4.45, 8.15, [(7.22, 7.94, 'door_gap')])
    draw_door(ax, 1.55, 7.94, 0.72, 0, 270)

    draw_wall_x_openings(ax, 0.30, 4.70, 3.45, 3.60, [
        (1.78, 2.58, 'door_gap'),
        (3.62, 4.42, 'door_gap'),
    ])
    draw_door(ax, 2.58, 3.45, 0.80, 270, 180)  # Puerta Suite Huéspedes
    draw_door(ax, 4.42, 3.45, 0.80, 270, 180)  # Puerta Baño Rústico

    draw_wall(ax, 2.80, 0.15, 2.95, 3.45)      # Divisoria Suite / Baño
    draw_wall(ax, 4.55, 0.15, 4.70, 3.45)      # Muro Este Baño / Barra Húmeda

    # Cerramiento Vitrina Cava de Vinos (Hierro Forjado y Vidrio Templado)
    ax.add_patch(Rectangle((1.55, 5.28), 1.70, 0.08, facecolor='#CFD8DC', edgecolor='#263238', lw=0.8, zorder=5))
    ax.add_patch(Rectangle((4.45, 5.28), 1.47, 0.08, facecolor='#CFD8DC', edgecolor='#263238', lw=0.8, zorder=5))
    ax.add_patch(Rectangle((5.88, 5.28), 0.08, 2.87, facecolor='#CFD8DC', edgecolor='#263238', lw=0.8, zorder=5))
    draw_double_door_h(ax, 3.25, 4.45, 5.32, open_up=True)

    # Escalera Tramo 1 (Y: 4.45..7.40) + Maletero
    draw_stairs_numbered(ax, 0.30, 4.45, 1.40, 7.40, 12, direction='up_y', label_txt='SUBE A P.B.')
    ax.add_patch(Rectangle((0.32, 7.78), 1.06, 0.35, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(0.85, 7.58, "Maletero", fontsize=5.6, fontweight='bold', ha='center', va='center')

    # Mobiliario 1: Cava de Vinos
    ax.add_patch(Rectangle((2.15, 7.72), 3.63, 0.38, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((1.56, 5.42), 0.36, 1.63, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((3.75, 6.22), 1.20, 0.70, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    for ts_x in [3.92, 4.48]:
        ax.add_patch(Circle((ts_x + 0.15, 5.99), 0.14, facecolor='#EFEBE9', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
        ax.add_patch(Circle((ts_x + 0.15, 7.15), 0.14, facecolor='#EFEBE9', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(2.82, 7.22, "Cava de Vinos\ny Cata Alpina\n(4,25 x 2,80 m)", fontsize=6.8, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=8)

    # Mobiliario 2: Salón Lounge & Cine 85"
    ax.add_patch(Rectangle((6.35, 7.65), 2.20, 0.42, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.plot([6.50, 8.40], [8.00, 8.00], color='#111111', lw=2.0, zorder=5)
    ax.add_patch(Rectangle((6.22, 4.82), 2.53, 0.90, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((7.88, 5.72), 0.87, 1.18, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((6.65, 6.02), 0.90, 0.63, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.65, zorder=4))
    ax.text(7.25, 7.15, "Salón Lounge &\nCine Familiar 85\"\n(2,95 x 3,30 m)", fontsize=7.0, fontweight='bold', ha='center', va='center', zorder=7)

    # Mobiliario 3: Barra Húmeda (Wet Bar) + Comedor Taberna 6p
    ax.add_patch(Rectangle((4.70, 1.15), 0.62, 2.20, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((4.80, 2.55), 0.40, 0.45, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(5.01, 1.85, "Barra\nHúmeda", rotation=90, fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=5)

    ax.add_patch(Rectangle((7.05, 1.25), 0.95, 1.80, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    for ty_c in [1.48, 2.34]:
        ax.add_patch(Rectangle((6.65, ty_c), 0.36, 0.42, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
        ax.add_patch(Rectangle((8.05, ty_c), 0.36, 0.42, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((7.32, 0.85), 0.42, 0.36, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((7.32, 3.09), 0.42, 0.36, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(6.10, 2.25, "Taberna Social\ny Juegos\n(4,25 x 3,45 m)", fontsize=7.0, fontweight='bold', ha='center', va='center', zorder=7)

    # Mobiliario 4: Suite de Huéspedes
    draw_bed(ax, 0.36, 0.95, 2.18, 2.35, head='west')
    ax.add_patch(Rectangle((0.36, 0.46), 0.38, 0.40, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((0.36, 2.44), 0.38, 0.40, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((0.52, 2.95), 1.15, 0.48, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(1.85, 0.55, "Suite de Huéspedes\n(2,50 x 3,30 m = 8,25 m²)", fontsize=6.6, fontweight='bold', ha='center', va='center', zorder=7)

    # Mobiliario 5: Baño Completo Rústico en Piedra
    ax.add_patch(Rectangle((2.95, 0.15), 1.60, 0.90, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((4.14, 0.17), 0.39, 0.82, facecolor='#CFD8DC', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    draw_wc(ax, 2.98, 1.52, orientation='east')
    ax.add_patch(Rectangle((2.98, 2.05), 0.50, 0.90, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Circle((3.25, 2.50), 0.16, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(3.98, 2.25, "Baño\nPiedra\n1,60x3,30", fontsize=6.2, fontweight='bold', ha='center', va='center', zorder=7)

    ax.text(2.15, 4.15, "Vestíbulo Escalera", fontsize=6.3, fontweight='bold', ha='center', va='center', zorder=7)

    # Columnas Sótano (35 x 35 cm)
    ax.add_patch(Rectangle((0.15, 6.35), 0.15, 0.45, facecolor='#444444', edgecolor='black', lw=0.7, zorder=7))
    for cx, cy in SOT_COLS:
        draw_col(ax, cx, cy, size=0.35, hatched=False)

    # Cotas Exteriores e Interiores estilo planos de casa.pdf
    draw_dim_h(ax, 0.30, 2.80, 8.75, "2,50", y_ref=8.30)
    draw_dim_h(ax, 2.80, 5.925, 8.75, "3,13", y_ref=8.30)
    draw_dim_h(ax, 5.925, 8.95, 8.75, "3,03", y_ref=8.30)
    draw_dim_h(ax, 0.15, 9.15, 9.30, "9,00 (Ancho Propio Edificación)", y_ref=8.30)

    draw_dim_h(ax, 0.30, 2.80, 1.25, "2,50")
    draw_dim_h(ax, 2.95, 4.55, 1.25, "1,60")
    draw_dim_h(ax, 4.70, 8.95, 3.85, "4,25")

    draw_dim_v(ax, -0.55, 0.00, 3.52, "3,52", x_ref=0.15)
    draw_dim_v(ax, -0.55, 3.52, 8.30, "4,78", x_ref=0.15)
    draw_dim_v(ax, -1.15, 0.00, 8.30, "8,30 (Sótano)", x_ref=0.15)
    draw_dim_v(ax, -1.15, -3.00, 0.00, "3,00 (Patio)", x_ref=0.15)
    draw_dim_v(ax, 10.45, 0.15, 3.45, "3,30", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 10.45, 3.60, 8.15, "4,55", x_ref=9.15, text_side='right')

    ax.text(4.65, -3.35, "PLANTA SÓTANO CHALET Y PATIO TRASERO (COTA N.P.T. = -2,55 m)",
            fontsize=10.5, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.40, 7.90], [-3.62, -3.62], color='#111111', lw=1.2)

    # Cuadro Resumen Técnico Inferior del Sótano
    ax_info = fig.add_axes([0.05, 0.115, 0.90, 0.115])
    ax_info.axis('off')
    ax_info.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.0))
    ax_info.text(0.02, 0.80, "PROGRAMA ARQUITECTÓNICO DEL NIVEL SÓTANO (OPCIÓN A — CHALET ALPINO):",
                 fontsize=8.2, fontweight='bold', color=C_RED)
    items_sot = [
        "• Huella Construida Sótano: 9,00 x 8,30 m = 74,70 m²  |  Terraza Exterior Techada con Pérgola: 4,20 x 2,20 m = 9,24 m².",
        "• Zona Social Integrada: Cava de Vinos Climatizada en Hierro/Vidrio (11,9 m²) + Salón Lounge & Cine 85\" + Taberna de Juegos y Barra Húmeda.",
        "• Zona Privada Independiente: Suite de Huéspedes con vista al jardín (8,25 m²) + Baño Completo Rústico en Piedra Pizarra (5,28 m²) + Maletero.",
        "• Relación con el Terreno: Nivel -2,55 m abierto a ras con el Patio Posterior mediante Doble Puerta Francesa de 2,20 m; muro oeste 100% propio (X >= 0,15 m).",
    ]
    for idx, line in enumerate(items_sot):
        ax_info.text(0.02, 0.58 - idx * 0.16, line, fontsize=7.0, color='#222222')

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 2: PLANTA BAJA — FRUTERÍA, GRAN ALMACÉN Y ESTACIONAMIENTO (Z = ±0,00 m)
# =============================================================================
def build_sheet_2_planta_baja(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — PLANTA BAJA",
                     "FRUTERÍA Y VERDULERÍA ALPINO + GRAN ALMACÉN (33,09 m²) + ESTACIONAMIENTO FLUIDO.",
                     escala="1:75", sheet_num="2 / 6")

    ax = fig.add_axes([0.04, 0.115, 0.64, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.9, 10.9)
    ax.set_ylim(-1.8, 24.4)
    ax.axis('off')

    draw_north(ax, 9.9, 23.1, r=0.50)

    # Pared vecino izquierdo intacta (X = 0.00..0.15)
    ax.add_patch(Rectangle((0.00, 0.00), 0.15, 21.71, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 11.0, "PARED DEL VECINO (INTACTA)", rotation=90, fontsize=6.5, fontweight='bold', color='#666666', ha='right', va='center')

    # Pisos zonificados sutiles
    ax.add_patch(Rectangle((0.30, 7.35), 3.00, 14.21, facecolor='#F7F8F9', edgecolor='none', zorder=1))  # Garaje plano
    ax.add_patch(Rectangle((3.45, 5.55), 5.55, 16.01, facecolor='#FFFDF9', edgecolor='none', zorder=1))  # Salón Frutería
    ax.add_patch(Rectangle((0.30, 0.15), 8.70, 3.35, facecolor='#F5F5F3', edgecolor='none', zorder=1))   # Gran Almacén
    ax.add_patch(Rectangle((1.40, 3.50), 1.35, 2.30, facecolor='#F5F5F3', edgecolor='none', zorder=1))   # Bajo escalera almacén

    # 1. Muros Exteriores Planta Baja
    draw_wall(ax, 0.15, 0.00, 0.30, 21.71)  # Muro Oeste propio
    # Fachada Frontal Avenida 4 (Y: 21.56..21.71) con Portón Corredizo + 2 Santamarías de Caracol
    draw_wall(ax, 0.15, 21.56, 0.40, 21.71)
    draw_wall(ax, 2.70, 21.56, 3.65, 21.71)
    draw_wall(ax, 5.75, 21.56, 6.20, 21.71)
    draw_wall(ax, 8.80, 21.56, 9.15, 21.71)

    # Muro Este con sus 7 ventanas reales de build_nuevo_proyecto.py
    draw_wall_y_openings(ax, 9.00, 9.15, 0.00, 21.71, [
        (1.10, 2.50, 'win'),
        (4.10, 5.00, 'win'),
        (6.30, 8.00, 'win'),
        (9.65, 11.85, 'win'),
        (13.15, 14.05, 'win'),
        (15.50, 17.70, 'win'),
        (18.80, 21.00, 'win'),
    ])
    # Muro Sur Posterior con sus 3 ventanas
    draw_wall_x_openings(ax, 0.15, 9.15, 0.00, 0.15, [
        (0.55, 2.35, 'win'),
        (4.10, 5.10, 'win'),
        (7.00, 8.40, 'win'),
    ])

    # 2. Muros Interiores Actualizados (Acceso abierto a escaleras + Gran Almacén de pared a pared)
    draw_wall(ax, 2.75, 3.50, 2.90, 8.95)     # Divisoria escaleras / frutería
    draw_wall(ax, 3.30, 8.80, 3.45, 21.56)    # Divisoria estacionamiento / frutería (3,00 m libres)
    draw_wall(ax, 2.75, 8.80, 3.45, 8.95)     # Cierre quiebre dejando X = 0.30..2.75 100% ABIERTO a escaleras
    draw_wall(ax, 1.40, 4.40, 1.55, 7.35)     # Muro central entre ambas escaleras
    draw_wall(ax, 0.30, 4.25, 1.40, 4.40)     # Muro ciego sur que aísla escalera sótano del almacén
    draw_wall(ax, 1.40, 5.80, 2.75, 5.95)     # Muro ciego bajo escalera P2 que aísla vestíbulo del almacén

    # Baño Comercial (X: 5.85..9.00, Y: 3.50..5.55)
    draw_wall(ax, 5.85, 5.40, 9.00, 5.55)
    draw_wall_y_openings(ax, 5.85, 6.00, 3.65, 5.40, [(3.95, 4.75, 'door_gap')])
    draw_door(ax, 6.00, 3.95, 0.80, 0, 90)

    # Muro Norte del Gran Almacén Unificado (X: 2.90..9.00, Y: 3.50..3.65) con Puerta Doble de Carga (X: 4.00..5.20)
    draw_wall_x_openings(ax, 2.90, 9.00, 3.50, 3.65, [(4.00, 5.20, 'door_gap')])
    draw_double_door_h(ax, 4.00, 5.20, 3.65, open_up=True)

    # 3. Portón Corredizo sobre Riel Curvo Lateral Derecho + 2 Santamarías de Caracol en Av. 4
    # Riel curvo del portón vehicular
    ax.plot([0.40, 3.02], [21.50, 21.50], color='#3E2723', lw=1.2, linestyle='--', zorder=6)
    ax.add_patch(Arc((3.02, 21.30), 0.40, 0.40, angle=0, theta1=0, theta2=90, color='#3E2723', lw=1.2, zorder=6))
    ax.plot([3.22, 3.22], [18.95, 21.30], color='#3E2723', lw=1.2, linestyle='--', zorder=6)
    # 4 hojas dobladas en el bolsillo derecho X = 3.14..3.28
    for gy1, gy2 in [(19.00, 19.55), (19.58, 20.13), (20.16, 20.71), (20.74, 21.29)]:
        ax.add_patch(Rectangle((3.15, gy1), 0.12, gy2 - gy1, facecolor='#8D6E63', edgecolor='black', lw=0.6, zorder=7))
    ax.text(1.55, 21.82, "PORTÓN CORREDIZO RIEL LATERAL\n(2,30 m libre)", fontsize=5.6, fontweight='bold',
            color='#3E2723', ha='center', va='bottom')

    # Tambores superiores (Caracol) de las 2 Santamarías Comerciales + Marquesina punteada
    for sx1, sx2, lbl_s in [(3.65, 5.75, "SANTAMARÍA CARACOL 1\n(2,10 m)"), (6.20, 8.80, "SANTAMARÍA CARACOL 2\n(2,60 m)")]:
        ax.add_patch(Rectangle((sx1, 21.38), sx2 - sx1, 0.28, facecolor='#CFD8DC', edgecolor='#263238', lw=0.8, hatch='---', zorder=6))
        ax.text(0.5 * (sx1 + sx2), 21.82, lbl_s, fontsize=5.6, fontweight='bold', color='#0D47A1', ha='center', va='bottom')
    ax.plot([3.55, 8.90], [21.90, 21.90], color='#8D6E63', lw=0.8, linestyle=':', zorder=4)

    # 4. Estacionamiento Fluido sin topes en fila (2 Plazas planas + acceso libre a escaleras)
    for py1, py2, v_lbl in [(15.20, 20.40, "PLAZA VEHICULAR 1\n(Piso Plano sin Topes)"),
                            (9.40,  14.60, "PLAZA VEHICULAR 2\n(Entrada/Salida Libre)")]:
        ax.add_patch(Rectangle((0.62, py1), 1.86, py2 - py1, facecolor='#ECEFF1', edgecolor='#607D8B',
                               lw=0.8, linestyle='--', zorder=2))
        ax.text(1.55, 0.5 * (py1 + py2), v_lbl, fontsize=6.0, fontweight='bold', color='#37474F', ha='center', va='center', zorder=4)

    ax.annotate('', xy=(0.85, 7.45), xytext=(0.85, 8.85), arrowprops=dict(arrowstyle='->', color='#1B5E20', lw=1.1), zorder=6)
    ax.annotate('', xy=(2.10, 7.45), xytext=(2.10, 8.85), arrowprops=dict(arrowstyle='->', color='#1B5E20', lw=1.1), zorder=6)
    ax.text(1.52, 8.20, "PASO ABIERTO A ESCALERAS", fontsize=5.5, fontweight='bold', color='#1B5E20', ha='center', bbox=WHITE_HALO, zorder=7)

    # Escaleras numeradas (Sótano 1..12 y P2 1..14)
    draw_stairs_numbered(ax, 0.30, 4.45, 1.40, 7.40, 12, direction='down_y', label_txt='BAJA SOT.')
    draw_stairs_numbered(ax, 1.55, 4.40, 2.65, 7.35, 14, direction='down_y', label_txt='SUBE P.A.')

    # 5. Equipamiento de Frutería y Verdulería: Islas en Columnas + Estantes en Paredes + Caja Mejorada
    # Caja en L con 2 Balanzas Digitales + TPV
    ax.add_patch(Rectangle((7.05, 18.25), 1.70, 0.72, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    ax.add_patch(Rectangle((7.05, 17.05), 0.68, 1.20, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    ax.add_patch(Rectangle((7.14, 17.22), 0.42, 0.36, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.7, zorder=5))  # Balanza 1
    ax.add_patch(Rectangle((7.14, 17.82), 0.42, 0.36, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.7, zorder=5))  # Balanza 2
    ax.add_patch(Rectangle((7.78, 18.38), 0.42, 0.38, facecolor='white', edgecolor='#111111', lw=0.7, zorder=5))    # TPV
    ax.add_patch(Rectangle((8.20, 17.00), 0.72, 1.05, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(7.95, 19.22, "CAJA Y PESAJE\n(2 Balanzas + TPV)", fontsize=6.0, fontweight='bold', color='#3E2723', ha='center', va='bottom', zorder=7)

    # 4 Islas Piramidales de Frutas abrazando las Columnas del Eje 2 (X = 5.925)
    islas = [
        (5.15, 6.30, 17.95, 19.20, "Isla Frutas 1"),
        (5.15, 6.70, 15.55, 17.10, "Isla Frutas 2"),
        (5.15, 6.70, 11.25, 12.80, "Isla Frutas 3"),
        (5.15, 6.70,  8.10,  9.65, "Isla Frutas 4"),
    ]
    for ix1, ix2, iy1, iy2, ilbl in islas:
        ax.add_patch(Rectangle((ix1, iy1), ix2 - ix1, iy2 - iy1, facecolor='#FFE0B2', edgecolor='#8D6E63', lw=0.75, zorder=3))
        ax.add_patch(Rectangle((ix1 + 0.22, iy1 + 0.22), (ix2 - ix1) - 0.44, (iy2 - iy1) - 0.44,
                               facecolor='#FFF3E0', edgecolor='#A1887F', lw=0.55, zorder=4))
        ax.text(0.5 * (ix1 + ix2), iy1 - 0.16, ilbl, fontsize=5.5, fontweight='bold', color='#4E342E', ha='center', va='top', zorder=6)

    # Estanterías Murales Inclinadas en todas las paredes
    ax.add_patch(Rectangle((3.45, 9.00), 0.60, 11.60, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.7, hatch='---', zorder=3))
    ax.text(3.75, 14.80, "ESTANTES MURALES DE FRUTAS (ROBLE)", rotation=90, fontsize=5.8, fontweight='bold',
            color='#4E342E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((2.90, 4.10), 0.60, 4.60, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.7, hatch='---', zorder=3))
    ax.text(3.20, 6.40, "ESTANTES CÍTRICOS", rotation=90, fontsize=5.4, fontweight='bold', color='#4E342E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((8.38, 6.20), 0.60, 10.30, facecolor=C_GREEN_SOFT, edgecolor='#2E7D32', lw=0.7, hatch='---', zorder=3))
    ax.text(8.68, 11.35, "ESTANTES VERDURAS Y HORTALIZAS FRESCAS", rotation=90, fontsize=5.6, fontweight='bold',
            color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((6.00, 5.56), 2.85, 0.54, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.7, zorder=3))
    ax.text(7.42, 5.83, "Estantes Tubérculos y Raíces", fontsize=5.4, fontweight='bold', color='#4E342E', ha='center', va='center', zorder=6)

    ax.text(5.95, 14.00, "SALÓN FRUTERÍA Y VERDULERÍA\n(5,55 x 16,01 m = 88,85 m²)\nCirculación Libre de Clientes",
            fontsize=7.4, fontweight='bold', color='#111111', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # 6. Baño Comercial
    ax.add_patch(Rectangle((7.20, 4.90), 1.00, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Circle((7.70, 5.14), 0.16, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    draw_wc(ax, 6.04, 4.05, orientation='east')
    ax.add_patch(Rectangle((6.04, 4.78), 0.30, 0.30, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(7.65, 4.20, "Baño Comercial\n3,00 x 1,75 m", fontsize=6.0, fontweight='bold', ha='center', va='center')

    # 7. Gran Almacén Unificado de Pared a Pared (33,09 m², sin Gerencia)
    ax.add_patch(Rectangle((0.35, 0.20), 2.30, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='xx', zorder=3))
    ax.add_patch(Rectangle((3.20, 0.20), 2.90, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='xx', zorder=3))
    ax.add_patch(Rectangle((0.32, 0.68), 0.48, 3.52, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='xx', zorder=3))
    ax.add_patch(Rectangle((1.45, 4.35), 1.25, 1.38, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='xx', zorder=3))
    ax.add_patch(Rectangle((5.35, 2.98), 2.05, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='xx', zorder=3))
    ax.text(2.07, 5.02, "Racks Bajo\nEscalera", fontsize=5.2, fontweight='bold', color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Cuarto Frío + Mesón Inox Lavado/Selección en Ala Este Unificada
    ax.add_patch(Rectangle((6.35, 0.20), 2.57, 1.45, facecolor=C_COLD_SOFT, edgecolor='#0277BD', lw=0.85, zorder=3))
    ax.text(7.63, 0.92, "CÁMARA FRIGORÍFICA /\nCUARTO FRÍO", fontsize=5.8, fontweight='bold', color='#01579B', ha='center', va='center', zorder=5)
    ax.add_patch(Rectangle((7.85, 1.85), 1.08, 1.55, facecolor=C_STONE_SOFT, edgecolor='#455A64', lw=0.7, zorder=3))
    ax.add_patch(Rectangle((8.05, 2.15), 0.68, 0.85, facecolor='white', edgecolor='#455A64', lw=0.55, zorder=4))
    ax.text(8.39, 2.60, "Lavado y\nSelección", fontsize=5.3, fontweight='bold', color='#263238', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.text(3.55, 1.85, "GRAN ALMACÉN UNIFICADO DE FRUTERÍA\n(8,70 x 3,35 m + Bajo Escalera = 33,09 m²)\nAcceso Exclusivo desde Zona Comercial",
            fontsize=6.8, fontweight='bold', color='#111111', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Columnas Planta Baja (32 columnas 25x25 cm intactas)
    for cx, cy in PB_P2_COLS:
        draw_col(ax, cx, cy, size=0.25, hatched=False)

    # Cotas Exteriores e Interiores limpias
    draw_dim_h(ax, 0.30, 3.30, 22.85, "3,00 (Garaje)", y_ref=21.71)
    draw_dim_h(ax, 3.45, 9.00, 22.85, "5,55 (Frutería)", y_ref=21.71)
    draw_dim_h(ax, 0.15, 9.15, 23.65, "9,00 (Frente Total Propio)", y_ref=21.71)

    draw_dim_h(ax, 4.05, 5.15, 13.30, "1,10")
    draw_dim_h(ax, 6.70, 8.38, 13.30, "1,68")
    draw_dim_h(ax, 0.30, 9.00, -0.55, "8,70 (Ancho Continuo Gran Almacén)", y_ref=0.00)

    draw_dim_v(ax, -0.65, 0.00, 4.25, "4,25", x_ref=0.15)
    draw_dim_v(ax, -0.65, 7.40, 21.56, "14,16 (Garaje Libre)", x_ref=0.15)
    draw_dim_v(ax, -1.35, 0.00, 21.71, "21,71", x_ref=0.15)
    draw_dim_v(ax, 9.85, 0.15, 3.50, "3,35", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.85, 3.65, 5.40, "1,75", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.85, 5.55, 21.56, "16,01", x_ref=9.15, text_side='right')

    ax.text(4.65, -1.15, "PLANTA BAJA — FRUTERÍA Y ESTACIONAMIENTO (N.P.T. ±0,00 m)",
            fontsize=9.8, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.20, 8.10], [-1.45, -1.45], color='#111111', lw=1.2)

    # Panel Derecho: Cuadro Técnico de Áreas y Detalles Operativos de Planta Baja
    ax_side = fig.add_axes([0.69, 0.125, 0.28, 0.79])
    ax_side.axis('off')
    ax_side.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))

    ax_side.text(0.50, 0.965, "CUADRO DE AMBIENTES\nPLANTA BAJA (195,39 m²)",
                 fontsize=9.0, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_side.plot([0.06, 0.94], [0.915, 0.915], color=C_BLUE, lw=0.9)

    zones_pb = [
        ("1. SALÓN DE FRUTERÍA", "88,85 m²",
         "• Doble acceso frontal con Santamarías\n  de Caracol enrollables hacia arriba.\n"
         "• 4 Islas Piramidales de Frutas a 4 caras\n  integradas en las columnas del Eje 2.\n"
         "• Estanterías inclinadas de roble en\n  muros Oeste, Este y Sur (sin mesas).\n"
         "• Pasillos amplios de 1,10 m a 1,68 m."),
        ("2. CAJA Y PESAJE MEJORADA", "Integrada",
         "• Mostrador en 'L' en piedra laja y roble.\n"
         "• 2 Balanzas electrónicas con visor alto,\n  TPV táctil y área trasera de empaque."),
        ("3. GRAN ALMACÉN UNIFICADO", "33,09 m²",
         "• Unión total de Depósito + Área Apoyo\n  + Bajo Escalera + antigua Gerencia.\n"
         "• Ancho libre de pared a pared: 8,70 m.\n"
         "• Cero acceso desde el estacionamiento;\n  entrada exclusiva por puerta doble (1,20m).\n"
         "• Incluye Cuarto Frío, Mesón de Lavado\n  y 4 baterías de racks industriales."),
        ("4. BAÑO COMERCIAL RÚSTICO", "5,70 m²",
         "• Lavamanos en piedra, WC y urinario."),
        ("5. ESTACIONAMIENTO FLUIDO", "46,20 m²",
         "• Portón corredizo sobre riel lateral a 90°\n  alojado en bolsillo derecho (X=3,16..3,28).\n"
         "• 3,00 m entre muros y 14,16 m de largo.\n"
         "• Piso 100% plano SIN topes en fila.\n"
         "• Acceso directo y abierto a las escaleras\n  de Sótano y Segundo Piso."),
    ]
    y_cursor = 0.895
    for z_title, z_area, z_desc in zones_pb:
        ax_side.text(0.06, y_cursor, z_title, fontsize=7.2, fontweight='bold', color='#1A237E', va='top')
        ax_side.text(0.94, y_cursor, z_area, fontsize=7.2, fontweight='bold', color=C_RED, ha='right', va='top')
        y_cursor -= 0.022
        ax_side.text(0.06, y_cursor, z_desc, fontsize=6.3, color='#263238', va='top', linespacing=1.32)
        n_lines = z_desc.count('\n') + 1
        y_cursor -= (n_lines * 0.024 + 0.022)
        ax_side.plot([0.06, 0.94], [y_cursor + 0.008, y_cursor + 0.008], color='#CFD8DC', lw=0.6)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 3: SEGUNDO PISO RESIDENCIAL CHALET + BUHARDILLA TANQUE 1.000 L
# =============================================================================
def build_sheet_3_segundo_piso(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — SEGUNDO PISO Y TANQUE",
                     "RESIDENCIA FAMILIAR CHALET RÚSTICO (Z = +3,00 m) + BUHARDILLA TÉCNICA 1.000 L (Z = +5,68 m).",
                     escala="1:75 / 1:50", sheet_num="3 / 6")

    # 1. PLANTA SEGUNDO PISO (IZQUIERDA)
    ax = fig.add_axes([0.04, 0.115, 0.61, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.9, 10.9)
    ax.set_ylim(-1.8, 24.4)
    ax.axis('off')

    draw_north(ax, 9.9, 23.1, r=0.50)

    # Pared vecino izquierdo intacta + línea de alero derecho propio (X = 10.10 m)
    ax.add_patch(Rectangle((0.00, 0.00), 0.15, 21.71, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 11.0, "PARED VECINO (0,00m ALERO)", rotation=90, fontsize=6.4, fontweight='bold', color='#666666', ha='right', va='center')
    ax.plot([10.10, 10.10], [-1.00, 21.71], color='#8D6E63', lw=0.9, linestyle='--', zorder=2)
    ax.text(10.22, 11.0, "PROYECCIÓN ALERO PROPIO DERECHO (0,95 m)", rotation=90, fontsize=5.8, color='#6D4C41', ha='left', va='center')

    # Pisos interiores y Terrazas Frontales
    ax.add_patch(Rectangle((0.30, 0.15), 8.70, 19.30, facecolor='#FFFDF9', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.30, 19.60), 5.55, 1.96, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.8, zorder=2))
    ax.add_patch(Rectangle((6.00, 19.60), 3.00, 1.96, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.8, zorder=2))
    # Barandas Alpinas en Avenida 4
    ax.add_patch(Rectangle((0.30, 21.52), 5.55, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((6.00, 21.52), 3.07, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((9.03, 19.60), 0.10, 2.04, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))

    # Muros Exteriores de Madera Machihembrada P2
    draw_wall(ax, 0.15, 0.00, 0.30, 21.71, facecolor='#6D4C41')  # Parapeto Oeste propio
    draw_wall(ax, 5.85, 19.45, 6.00, 21.71, facecolor='#6D4C41') # Muro privacidad entre terrazas

    # Muro Frontal Acristalado de Retranqueo de Terrazas (Y: 19.45..19.60)
    draw_wall_x_openings(ax, 0.30, 5.85, 19.45, 19.60, [
        (0.65, 2.55, 'win'),
        (3.15, 5.55, 'win'),
    ], facecolor='#6D4C41')
    draw_wall_x_openings(ax, 6.00, 9.00, 19.45, 19.60, [
        (6.50, 8.50, 'win'),
    ], facecolor='#6D4C41')

    # Fachada Este P2 (X: 9.00..9.15)
    draw_wall_y_openings(ax, 9.00, 9.15, 0.00, 19.60, [
        (1.10, 2.90, 'shutter_win'),
        (4.90, 5.85, 'win'),
        (7.15, 8.55, 'shutter_win'),
        (10.65, 11.65, 'win'),
        (16.00, 18.20, 'shutter_win'),
    ], facecolor='#6D4C41')

    # Fachada Sur P2 (Y: 0.00..0.15)
    draw_wall_x_openings(ax, 0.15, 9.15, 0.00, 0.15, [
        (0.85, 2.35, 'win'),
        (3.35, 5.40, 'shutter_win'),
        (6.65, 8.45, 'shutter_win'),
    ], facecolor='#6D4C41')

    # Tabiquería Interior P2
    draw_wall_y_openings(ax, 5.85, 6.00, 0.15, 19.45, [
        (2.55, 3.35, 'door_gap'),
        (4.60, 5.35, 'door_gap'),
        (6.85, 7.65, 'door_gap'),
        (15.10, 15.95, 'door_gap'),
    ])
    draw_door(ax, 6.00, 3.35, 0.80, 0, 270)   # Hab 3
    draw_door(ax, 6.00, 5.35, 0.75, 0, 270)   # Baño Familiar
    draw_door(ax, 6.00, 6.85, 0.80, 0, 90)    # Hab 2
    draw_door(ax, 6.00, 15.10, 0.85, 0, 90)   # Master Suite

    # Divisiones internas Master Suite, Hab 2, Baño Fam, Hab 3
    draw_wall_x_openings(ax, 6.00, 9.00, 14.80, 14.95, [(7.05, 7.95, 'door_gap')])  # Barn door Vestier
    ax.plot([7.05, 8.75], [14.98, 14.98], color='#3E2723', lw=1.4, zorder=6)        # Riel puerta granero
    draw_wall_x_openings(ax, 6.00, 9.00, 12.45, 12.60, [(7.10, 7.90, 'door_gap')])  # Puerta Baño Spa
    draw_door(ax, 7.10, 12.45, 0.80, 270, 360)
    draw_wall(ax, 6.00, 10.00, 9.00, 10.15)
    draw_wall(ax, 6.00, 6.30, 9.00, 6.45)
    draw_wall(ax, 6.00, 4.30, 9.00, 4.45)

    # Despensa Walk-In + Clóset de Blancos + Escalera + Lavandería + Mirador Sur
    draw_wall(ax, 1.40, 4.40, 1.55, 7.35)
    draw_wall(ax, 0.30, 5.65, 1.40, 5.80)
    draw_wall_x_openings(ax, 0.30, 2.75, 7.35, 7.50, [(0.50, 1.30, 'door_gap')])
    draw_door(ax, 1.30, 7.35, 0.80, 270, 180)  # Puerta Despensa
    draw_wall_x_openings(ax, 0.30, 1.55, 4.40, 4.55, [(0.45, 1.25, 'door_gap')])
    draw_double_door_h(ax, 0.45, 1.25, 4.40, open_up=False)  # Clóset Blancos
    draw_wall_x_openings(ax, 0.30, 2.75, 3.45, 3.60, [(1.65, 2.45, 'door_gap')])
    draw_door(ax, 1.65, 3.45, 0.80, 270, 360)  # Puerta Lavandería
    draw_wall(ax, 2.75, 0.15, 2.90, 3.60)      # Divisoria Lavandería / Mirador Sur (deja Portal 0,91m abierto en Y=3.70..4.61!)
    draw_wall_x_openings(ax, 2.90, 5.85, 3.50, 3.65, [(3.40, 5.30, 'door_gap')])

    # Escalera P2 (14 peldaños) + Baranda dejando Portal Plano abierto en Y: 3.70..4.61
    draw_stairs_numbered(ax, 1.55, 4.40, 2.65, 7.35, 14, direction='down_y', label_txt='BAJA P.B.')
    ax.plot([2.75, 2.75], [4.61, 7.35], color='#6D4C41', lw=1.4, zorder=6)

    # MOBILIARIO COMPLETO P2:
    # Terrazas
    ax.add_patch(Rectangle((0.48, 20.05), 0.74, 1.20, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((3.85, 20.30), 1.30, 0.70, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(2.95, 20.65, "Balconada Social Techada\n(5,55 x 1,96 m)", fontsize=5.8, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((6.12, 20.45), 0.68, 0.68, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((7.52, 20.55), 0.68, 0.68, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((8.38, 20.68), 0.52, 0.68, facecolor=C_GREEN_SOFT, edgecolor='#2E7D32', lw=0.6, zorder=3))
    ax.text(7.45, 19.95, "Terraza Master (3,00x1,96)", fontsize=5.5, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Sala y Comedor 8p
    ax.add_patch(Rectangle((3.05, 18.52), 2.10, 0.88, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((3.05, 16.52), 0.87, 2.00, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((4.18, 17.05), 0.70, 1.10, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    ax.add_patch(Rectangle((5.38, 16.25), 0.42, 2.55, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((0.48, 16.55), 0.74, 0.74, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((0.48, 17.70), 0.74, 0.74, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(2.15, 17.65, "Gran Sala Chalet\n+ Panel TV 75\"", fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=6)

    ax.add_patch(Rectangle((2.30, 13.55), 2.20, 1.05, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    for ch_x in [2.52, 3.18, 3.84]:
        ax.add_patch(Rectangle((ch_x, 13.15), 0.42, 0.36, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
        ax.add_patch(Rectangle((ch_x, 14.64), 0.42, 0.36, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.add_patch(Rectangle((1.88, 13.86), 0.38, 0.42, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.add_patch(Rectangle((4.54, 13.86), 0.38, 0.42, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.add_patch(Rectangle((0.30, 13.65), 0.48, 1.80, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(3.40, 14.07, "Comedor 8 Puestos", fontsize=6.0, fontweight='bold', ha='center', va='center', zorder=6)

    # Cocina Rústica + Isla Central + Nevera/Hornos
    ax.add_patch(Rectangle((0.30, 8.35), 0.66, 4.85, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((0.40, 9.15), 0.50, 0.95, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))   # Fregadero
    ax.add_patch(Rectangle((0.38, 11.00), 0.50, 0.95, facecolor='#ECEFF1', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))# Cocina 5h
    ax.add_patch(Rectangle((1.44, 7.52), 0.88, 0.78, facecolor=C_COLD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=4))# Nevera
    ax.add_patch(Rectangle((2.34, 7.52), 0.38, 0.76, facecolor='#CFD8DC', edgecolor=C_FURN_EDGE, lw=0.65, zorder=4)) # Hornos
    ax.text(1.98, 8.50, "Nevera + Hornos", fontsize=5.2, fontweight='bold', ha='center', va='bottom', zorder=6)

    ax.add_patch(Rectangle((2.10, 9.55), 1.02, 2.60, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    for b_y in [9.80, 10.38, 10.96, 11.54]:
        ax.add_patch(Circle((3.28, b_y), 0.16, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(2.58, 10.85, "Isla\nMaciza", fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=6)
    ax.text(4.55, 10.85, "Cocina Rústica\n(5,55 x 5,70 m)", fontsize=6.4, fontweight='bold', ha='center', va='center', zorder=6)

    # Master Suite + Vestier + Baño Spa
    draw_bed(ax, 6.14, 16.75, 8.03, 18.45, head='west')
    ax.add_patch(Rectangle((6.14, 16.18), 0.44, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((6.14, 18.54), 0.44, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.55, 15.65, "Dormitorio Master Suite\n(3,00 x 4,50 m)", fontsize=6.1, fontweight='bold', ha='center', va='center', zorder=6)

    ax.add_patch(Rectangle((6.05, 12.65), 0.55, 2.10, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='||', zorder=3))
    ax.add_patch(Rectangle((8.40, 12.65), 0.55, 2.10, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='||', zorder=3))
    ax.add_patch(Rectangle((7.22, 13.35), 0.56, 0.70, facecolor='#EFEBE9', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    ax.text(7.50, 14.38, "Vestier Walk-In\n(3,00 x 2,20 m)", fontsize=5.7, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((6.05, 10.30), 0.55, 1.58, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Circle((6.33, 10.71), 0.15, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.add_patch(Circle((6.33, 11.47), 0.15, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    draw_wc(ax, 7.20, 10.18, orientation='north')
    ax.add_patch(Rectangle((7.95, 10.15), 1.00, 2.30, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((8.55, 10.18), 0.39, 1.47, facecolor='#CFD8DC', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(7.25, 11.65, "Baño Spa\n3,00x2,30", fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=6)

    # Habitación 2, Baño Familiar, Habitación 3, Mirador Sur, Despensa, Blancos y Lavandería
    draw_bed(ax, 7.15, 7.25, 8.92, 8.65, head='east')
    ax.add_patch(Rectangle((6.05, 9.40), 1.40, 0.55, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.35, 6.75, "Habitación 2 (3,00 x 3,55 m)", fontsize=5.9, fontweight='bold', ha='center', va='center')

    ax.add_patch(Rectangle((8.05, 4.48), 0.90, 1.78, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    draw_wc(ax, 7.35, 4.48, orientation='north')
    ax.add_patch(Rectangle((6.20, 5.75), 0.90, 0.50, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.05, 5.30, "Baño Fam.\n3,00x1,85", fontsize=5.7, fontweight='bold', ha='center', va='center')

    draw_bed(ax, 7.15, 1.35, 8.92, 2.75, head='east')
    ax.add_patch(Rectangle((6.05, 3.70), 1.40, 0.55, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.45, 0.72, "Habitación 3 (3,00 x 4,15 m)", fontsize=5.9, fontweight='bold', ha='center', va='center')

    ax.text(4.38, 1.85, "Estar / Mirador Sur\n(2,95 x 3,35 m)", fontsize=6.2, fontweight='bold', ha='center', va='center')
    ax.text(0.85, 6.55, "Despensa\n1,10x1,55", fontsize=5.2, fontweight='bold', ha='center', va='center')
    ax.text(0.85, 5.10, "Blancos\n1,10x1,10", fontsize=5.2, fontweight='bold', ha='center', va='center')
    ax.text(1.50, 3.98, "Vestíbulo / Portal 0,91m", fontsize=5.2, fontweight='bold', color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Lavandería + Escalera fija al Tanque
    ax.add_patch(Rectangle((0.38, 2.05), 0.80, 1.25, facecolor='#FFF8E1', edgecolor='#E65100', lw=0.75, linestyle='--', zorder=4))
    for sy_m in np.linspace(2.15, 3.18, 8):
        ax.plot([0.45, 1.05], [sy_m, sy_m], color='#E65100', lw=0.6, zorder=5)
    ax.add_patch(Rectangle((1.95, 0.22), 0.72, 0.68, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3)) # Lavadora
    ax.add_patch(Rectangle((1.18, 0.22), 0.72, 0.68, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3)) # Secadora
    ax.text(1.55, 1.38, "Lavandería\n(2,45 x 3,30 m)\n+ Subida Tanque", fontsize=5.7, fontweight='bold', ha='center', va='center')

    for cx, cy in PB_P2_COLS:
        draw_col(ax, cx, cy, size=0.25, hatched=False)

    # Cotas Segundo Piso
    draw_dim_h(ax, 0.30, 5.85, 22.85, "5,55 (Zona Social)", y_ref=21.71)
    draw_dim_h(ax, 6.00, 9.00, 22.85, "3,00 (Master Suite)", y_ref=21.71)
    draw_dim_h(ax, 0.15, 9.15, 23.65, "9,00 (Ancho Cuerpo Casa)", y_ref=21.71)

    draw_dim_v(ax, -0.65, 0.15, 3.45, "3,30", x_ref=0.15)
    draw_dim_v(ax, -0.65, 7.50, 19.45, "11,95", x_ref=0.15)
    draw_dim_v(ax, -0.65, 19.60, 21.56, "1,96", x_ref=0.15)
    draw_dim_v(ax, -1.35, 0.00, 21.71, "21,71", x_ref=0.15)

    draw_dim_v(ax, 9.75, 0.15, 4.30, "4,15", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 4.45, 6.30, "1,85", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 6.45, 10.00, "3,55", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 10.15, 12.45, "2,30", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 12.60, 14.80, "2,20", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 14.95, 19.45, "4,50", x_ref=9.15, text_side='right')

    ax.text(4.65, -1.15, "PLANTA SEGUNDO PISO RESIDENCIAL CHALET (N.P.T. +3,00 m)",
            fontsize=9.8, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.10, 8.20], [-1.45, -1.45], color='#111111', lw=1.2)

    # 2. PLANTA DETALLE BUHARDILLA TÉCNICA TANQUE 1.000 L (ARRIBA DERECHA)
    ax_t = fig.add_axes([0.67, 0.49, 0.29, 0.42])
    ax_t.set_aspect('equal')
    ax_t.set_xlim(-0.9, 4.3)
    ax_t.set_ylim(-1.2, 5.5)
    ax_t.axis('off')

    ax_t.add_patch(Rectangle((0.00, 0.00), 0.15, 4.45, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax_t.add_patch(Rectangle((0.30, 0.15), 2.45, 4.10, facecolor='#F9FBE7', edgecolor='none', zorder=1))
    draw_wall(ax_t, 0.15, 0.00, 0.30, 4.45, facecolor='#6D4C41')  # Parapeto ciego sin alero
    draw_wall(ax_t, 2.75, 0.00, 2.90, 4.45, facecolor='#6D4C41')
    draw_wall(ax_t, 0.15, 4.25, 2.90, 4.45, facecolor='#6D4C41')
    draw_wall_x_openings(ax_t, 0.15, 2.90, 0.00, 0.15, [(0.88, 2.33, 'win')], facecolor='#6D4C41')

    # Canalón oculto propio (X: 0.30..0.55)
    ax_t.add_patch(Rectangle((0.30, 0.15), 0.22, 4.10, facecolor='#CFD8DC', edgecolor='#455A64', lw=0.5, linestyle='--', zorder=2))

    # Escotilla de acceso (0.80 x 1.25 m en X: 0.38..1.18, Y: 2.05..3.30) + Baranda seguridad
    ax_t.add_patch(Rectangle((0.38, 2.05), 0.80, 1.25, facecolor='#FFF8E1', edgecolor='#E65100', lw=0.9, zorder=4))
    for sy_m in np.linspace(2.15, 3.18, 8):
        ax_t.plot([0.45, 1.05], [sy_m, sy_m], color='#E65100', lw=0.65, zorder=5)
    ax_t.plot([1.21, 1.21], [2.02, 3.30], color=C_COL_RED, lw=1.4, zorder=6)
    ax_t.plot([0.38, 1.21], [2.02, 2.02], color=C_COL_RED, lw=1.4, zorder=6)

    # Pedestal + Tanque 1.000 L (Ø 1,10 m en CX=1.60, CY=1.15)
    ax_t.add_patch(Rectangle((0.95, 0.50), 1.30, 1.30, facecolor='#ECEFF1', edgecolor='#546E7A', lw=0.8, zorder=3))
    ax_t.add_patch(Circle((1.60, 1.15), 0.55, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=1.2, zorder=5))
    ax_t.add_patch(Circle((1.60, 1.15), 0.22, facecolor='white', edgecolor='#0D47A1', lw=0.8, zorder=6))
    ax_t.text(1.60, 1.15, "TANQUE\n1.000 L\nØ 1,10 m", fontsize=5.3, fontweight='bold', color='#0D47A1', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Bancada Hidroneumática (Bomba + Pulmón + Filtro)
    ax_t.add_patch(Rectangle((1.85, 2.15), 0.85, 1.10, facecolor='#ECEFF1', edgecolor='#455A64', lw=0.7, zorder=3))
    ax_t.add_patch(Rectangle((1.95, 2.25), 0.32, 0.38, facecolor='#90CAF9', edgecolor='#0D47A1', lw=0.6, zorder=4))
    ax_t.add_patch(Circle((2.48, 2.45), 0.16, facecolor='#FFCDD2', edgecolor='#B71C1C', lw=0.6, zorder=4))
    ax_t.text(2.28, 2.95, "Bomba +\nPulmón", fontsize=5.2, fontweight='bold', ha='center', va='center', zorder=6)
    ax_t.text(1.60, 3.75, "Desembarque Libre\n(2,45 x 0,95 m)", fontsize=5.6, fontweight='bold', color='#1B5E20', ha='center', va='center')
    ax_t.text(1.60, -0.26, "Celosía Abatible 1,45 m", fontsize=5.5, fontweight='bold', color='#3E2723', ha='center', va='top')

    draw_dim_h(ax_t, 0.30, 2.75, 4.82, "2,45", y_ref=4.45)
    draw_dim_v(ax_t, 3.35, 0.15, 4.25, "4,10", x_ref=2.90, text_side='right')
    ax_t.text(1.50, -0.72, "PLANTA BUHARDILLA TANQUE 1.000 L\n(N.P.T. +5,68 m — ESC. 1:50)",
              fontsize=7.6, fontweight='bold', color='#111111', ha='center', va='top')

    # 3. CUADRO RESUMEN DEL SEGUNDO PISO (ABAJO DERECHA)
    ax_res = fig.add_axes([0.67, 0.115, 0.29, 0.365])
    ax_res.axis('off')
    ax_res.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))
    ax_res.text(0.50, 0.945, "PROGRAMA RESIDENCIAL\nSEGUNDO PISO (195,39 m²)",
                fontsize=8.3, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_res.plot([0.06, 0.94], [0.84, 0.84], color=C_BLUE, lw=0.8)

    p2_notes = [
        "• Doble Terraza Independiente Av. 4:\n  Balconada Social (10,88 m²) + Terraza\n  Privada Master Suite (5,88 m²).",
        "• Master Suite de Gran Formato (32,88 m²):\n  Dormitorio King + Vestier Walk-In doble\n  frente + Baño Spa con ducha pizarra.",
        "• Zona Familiar Posterior:\n  Habitación 2 (10,65 m²), Baño Familiar\n  (5,55 m²), Habitación 3 (12,45 m²) y\n  Estar / Mirador Sur (9,88 m²).",
        "• Área Social Chalet Integrada:\n  Gran Sala TV 75\", Comedor 8 puestos,\n  Cocina Rústica con Isla Central, Despensa\n  Walk-In y Clóset de Blancos.",
        "• Lavandería + Buhardilla Hidroneumática:\n  Tanque vertical de 1.000 L a +5,68 m\n  con acceso seguro y 0,00 m invasión.",
    ]
    yy = 0.805
    for note in p2_notes:
        ax_res.text(0.06, yy, note, fontsize=5.95, color='#263238', va='top', linespacing=1.25)
        yy -= (note.count('\n') + 1) * 0.041 + 0.017

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 4: PLANO DISTRIBUCIÓN DE COLUMNAS Y EJES ESTRUCTURALES (ESC. 1:75)
# =============================================================================
def build_sheet_4_columnas_estructura(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO DISTRIBUCIÓN DE COLUMNAS Y EJES ESTRUCTURALES",
                     "PLANTA BAJA Y SEGUNDO PISO: 25 x 25 (cm) / IPE METÁLICO — SÓTANO: 35 x 35 (cm).",
                     escala="1:75", sheet_num="4 / 6")

    # 1. PANEL PRINCIPAL IZQUIERDO: PLANTA BAJA Y SEGUNDO PISO (32 COLUMNAS)
    ax = fig.add_axes([0.035, 0.115, 0.565, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.4, 11.4)
    ax.set_ylim(-2.0, 24.4)
    ax.axis('off')

    # Contornos arquitectónicos tenues en línea segmentada (fiel a Pág. 3 de planos de casa.pdf)
    ghost_rects = [
        (0.15, 0.00, 9.00, 21.71),   # Perímetro general propio
        (0.30, 8.80, 3.00, 12.76),   # Estacionamiento
        (3.45, 5.55, 5.55, 16.01),   # Frutería / Zona Social P.A.
        (5.85, 3.50, 3.15, 2.05),    # Baño
        (0.30, 0.15, 8.70, 3.35),    # Gran Almacén / Bloque Sur P.A.
        (0.30, 4.45, 1.10, 2.95),    # Escalera Sótano
        (1.55, 4.40, 1.10, 2.95),    # Escalera P.A.
        (6.00, 19.60, 3.00, 1.96),   # Balcón Master P.A.
        (0.30, 19.60, 5.55, 1.96),   # Balcón Social P.A.
    ]
    for gx, gy, gw, gh in ghost_rects:
        ax.add_patch(Rectangle((gx, gy), gw, gh, fill=False, edgecolor='#B0B0B0', lw=0.55, linestyle='--', zorder=1))

    # Peldaños tenues en escaleras de referencia
    for sy_i in np.linspace(4.45, 7.40, 13):
        ax.plot([0.30, 1.40], [sy_i, sy_i], color='#C0C0C0', lw=0.45, linestyle='--', zorder=1)
    for sy_i in np.linspace(4.40, 7.35, 15):
        ax.plot([1.55, 2.65], [sy_i, sy_i], color='#C0C0C0', lw=0.45, linestyle='--', zorder=1)

    # Nombres de referencia sutiles estilo Pág. 3 de planos de casa.pdf
    ref_labels = [
        (1.75, 14.80, "Estacionamiento."),
        (4.60, 20.55, "Balconada P.A."),
        (7.50, 20.55, "Terraza Suite."),
        (4.55, 14.20, "Salón Frutería /\nSala-Comedor P.A."),
        (7.50, 17.20, "Master Suite P.A."),
        (7.50, 10.60, "Habitación 2 P.A."),
        (7.50,  7.40, "Habitación 3 P.A."),
        (7.50,  4.50, "Baño."),
        (4.50,  1.85, "Gran Almacén P.B. /\nLavandería y Mirador P.A."),
    ]
    for rx, ry, rtxt in ref_labels:
        ax.text(rx, ry, rtxt, fontsize=5.8, color='#555555', fontweight='bold', ha='center', va='center', zorder=2)

    # Ejes estructurales verticales (0, 1, 2, 3) y horizontales (A0..H) en cian técnico
    axes_x = [("0", 0.275), ("1", 2.825), ("2", 5.925), ("3", 9.075)]
    axes_y = [
        ("A0", 21.585), ("A", 18.575), ("B", 16.325), ("C", 14.625),
        ("D",  12.025), ("E",  8.875), ("F",  6.575), ("G",  3.575), ("H", 0.125),
    ]

    for lbl_x, gx in axes_x:
        ax.plot([gx, gx], [-0.30, 23.00], color=C_AXIS_CYAN, lw=0.75, linestyle='-', zorder=3)
        ax.add_patch(Circle((gx, 23.42), 0.34, facecolor='white', edgecolor='#111111', lw=0.9, zorder=8))
        ax.text(gx, 23.42, lbl_x, fontsize=7.6, fontweight='bold', ha='center', va='center', zorder=9)

    for lbl_y, gy in axes_y:
        x_start = 5.925 if lbl_y == "C" else 0.275
        ax.plot([x_start, 10.30], [gy, gy], color=C_AXIS_CYAN, lw=0.75, linestyle='-', zorder=3)
        ax.add_patch(Circle((10.72, gy), 0.34, facecolor='white', edgecolor='#111111', lw=0.9, zorder=8))
        ax.text(10.72, gy, lbl_y, fontsize=7.0, fontweight='bold', ha='center', va='center', zorder=9)

    # Cuadrante reforzado de Losa Tanque 1.000 L (Ejes 0-1 / G-H)
    ax.add_patch(Rectangle((0.275, 0.125), 2.55, 3.45, facecolor='#E3F2FD', edgecolor='#1565C0',
                           lw=0.9, linestyle='-.', alpha=0.55, zorder=2))
    ax.text(1.55, 1.85, "Losa Reforzada\nTanque 1.000 L\n(+5,68 m)", fontsize=5.5, fontweight='bold',
            color='#0D47A1', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # 32 Columnas achuradas en rojo (25 x 25 cm)
    for cx, cy in PB_P2_COLS:
        draw_col(ax, cx, cy, size=0.30, hatched=True)

    # Cotas entre ejes estructurales (idéntico a Pág. 3 de planos de casa.pdf)
    draw_dim_h(ax, 0.275, 2.825, 22.35, "2,55", y_ref=21.585)
    draw_dim_h(ax, 2.825, 5.925, 22.35, "3,10", y_ref=21.585)
    draw_dim_h(ax, 5.925, 9.075, 22.35, "3,15", y_ref=21.585)

    draw_dim_h(ax, 0.275, 2.825, -0.55, "2,55", y_ref=0.125)
    draw_dim_h(ax, 2.825, 5.925, -0.55, "3,10", y_ref=0.125)
    draw_dim_h(ax, 5.925, 9.075, -0.55, "3,15", y_ref=0.125)

    y_pairs = [
        (18.575, 21.585, "3,01"),
        (16.325, 18.575, "2,25"),
        (14.625, 16.325, "1,70"),
        (12.025, 14.625, "2,60"),
        ( 8.875, 12.025, "3,15"),
        ( 6.575,  8.875, "2,30"),
        ( 3.575,  6.575, "3,00"),
        ( 0.125,  3.575, "3,45"),
    ]
    for y_a, y_b, lbl_d in y_pairs:
        draw_dim_v(ax, 9.75, y_a, y_b, lbl_d, fontsize=5.8, text_side='left')
    draw_dim_v(ax, -0.65, 0.125, 21.585, "21,46 (Entre Ejes Extremos)", x_ref=0.275)

    ax.text(4.65, -1.25, "PLANTA CASA — PLANTA BAJA Y SEGUNDO PISO\n(32 APOYOS ESTRUCTURALES 25 x 25 cm)",
            fontsize=8.6, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.10, 8.20], [-1.82, -1.82], color='#111111', lw=1.1)

    # 2. PANEL INFERIOR DERECHO: PLANTA ESTRUCTURAL SÓTANO (35 x 35 cm)
    ax_sot = fig.add_axes([0.60, 0.115, 0.37, 0.41])
    ax_sot.set_aspect('equal')
    ax_sot.set_xlim(-0.8, 11.2)
    ax_sot.set_ylim(-1.9, 10.3)
    ax_sot.axis('off')

    # Muros de contención perimetrales y referencia interna
    ax_sot.add_patch(Rectangle((0.15, 0.00), 9.00, 8.30, fill=False, edgecolor='#9E9E9E', lw=0.6, linestyle='--', zorder=1))
    ax_sot.add_patch(Rectangle((0.15, 8.15), 9.00, 0.15, facecolor='#E0E0E0', edgecolor='#616161', lw=0.7, hatch='///', zorder=2))
    ax_sot.add_patch(Rectangle((0.15, 0.00), 0.15, 8.30, facecolor='#E0E0E0', edgecolor='#616161', lw=0.7, hatch='///', zorder=2))
    for sy_i in np.linspace(4.45, 7.40, 13):
        ax_sot.plot([0.30, 1.40], [sy_i, sy_i], color='#C0C0C0', lw=0.45, linestyle='--', zorder=1)

    ax_sot.text(3.75, 5.20, "Cava y Cata.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(7.45, 5.20, "Salón Cine.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(1.55, 1.85, "Suite Huésp.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(3.75, 1.85, "Baño.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(6.85, 1.85, "Taberna.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')

    sot_axes_x = [("0", 0.325), ("1", 2.825), ("2", 5.925), ("3", 8.975)]
    sot_axes_y = [("F", 6.575), ("G", 3.575), ("H", 0.175)]

    for lbl_x, gx in sot_axes_x:
        ax_sot.plot([gx, gx], [0.175, 9.10], color=C_AXIS_CYAN, lw=0.75, zorder=3)
        ax_sot.add_patch(Circle((gx, 9.52), 0.34, facecolor='white', edgecolor='#111111', lw=0.9, zorder=8))
        ax_sot.text(gx, 9.52, lbl_x, fontsize=7.2, fontweight='bold', ha='center', va='center', zorder=9)

    for lbl_y, gy in sot_axes_y:
        ax_sot.plot([0.325, 10.05], [gy, gy], color=C_AXIS_CYAN, lw=0.75, zorder=3)
        ax_sot.add_patch(Circle((10.48, gy), 0.34, facecolor='white', edgecolor='#111111', lw=0.9, zorder=8))
        ax_sot.text(10.48, gy, lbl_y, fontsize=7.0, fontweight='bold', ha='center', va='center', zorder=9)

    # 12 Apoyos / Columnas de Sótano (35 x 35 cm achurados en rojo)
    draw_col(ax_sot, 0.25, 6.575, size=0.35, hatched=True)
    for cx, cy in SOT_COLS:
        draw_col(ax_sot, cx, cy, size=0.38, hatched=True)

    draw_dim_h(ax_sot, 0.325, 2.825, 8.65, "2,50", y_ref=8.30, fontsize=5.8)
    draw_dim_h(ax_sot, 2.825, 5.925, 8.65, "3,10", y_ref=8.30, fontsize=5.8)
    draw_dim_h(ax_sot, 5.925, 8.975, 8.65, "3,05", y_ref=8.30, fontsize=5.8)
    draw_dim_v(ax_sot, 9.65, 3.575, 6.575, "3,00", fontsize=5.8, text_side='left')
    draw_dim_v(ax_sot, 9.65, 0.175, 3.575, "3,40", fontsize=5.8, text_side='left')

    ax_sot.text(4.65, -0.85, "PLANTA SÓTANO (12 APOYOS 35 x 35 cm)",
                fontsize=8.2, fontweight='bold', color='#111111', ha='center', va='top')
    ax_sot.plot([1.30, 8.00], [-1.22, -1.22], color='#111111', lw=1.1)

    # 3. PANEL SUPERIOR DERECHO: ESPECIFICACIONES ESTRUCTURALES Y ALTERNATIVA METÁLICA IPE
    ax_sp = fig.add_axes([0.61, 0.545, 0.355, 0.375])
    ax_sp.axis('off')
    ax_sp.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))
    ax_sp.text(0.50, 0.955, "MEMORIA Y ESPECIFICACIONES\nESTRUCTURALES",
               fontsize=8.6, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_sp.plot([0.06, 0.94], [0.855, 0.855], color=C_BLUE, lw=0.8)

    spec_blocks = [
        ("1. INFRAESTRUCTURA Y SÓTANO (-2,55 m):",
         "• 12 columnas de 35 x 35 cm en concreto armado\n  (f'c = 250 kg/cm², 8 Ø 5/8\" + estribos Ø 3/8\").\n"
         "• Muro de contención norte y muro propio oeste\n  (X = 0,15..0,30 m) sin tocar pared vecina."),
        ("2. PLANTA BAJA COMERCIAL (±0,00 m):",
         "• 32 columnas de 25 x 25 cm en retícula ortogonal\n  intacta (Ejes 0, 1, 2, 3 x A0..H).\n"
         "• Vigas sísmicas de carga de 25 x 35 cm."),
        ("3. ÚLTIMO PISO (+3,00 m) — CONCRETO O IPE:",
         "• Opción A: Continuación en concreto 25 x 25 cm.\n"
         "• Opción B Recomendada: Columnas metálicas tipo\n  IPE 160 / HEA 140 (Acero ASTM A36) sobre\n"
         "  planchas base 250x250x16 mm con 4 pernos Ø 5/8\"\n  anclados en los nodos de +3,00 m (menor peso\n  sísmico y acople directo con cubierta Chalet)."),
        ("4. CUBIERTA CHALET Y TANQUE (+5,68 m):",
         "• Losa maciza reforzada en Ejes 0-1 / G-H para\n  Tanque de 1.000 L + Cerchas Alpinas a 32°."),
    ]
    sy_cur = 0.825
    for stitle, sbody in spec_blocks:
        ax_sp.text(0.06, sy_cur, stitle, fontsize=6.7, fontweight='bold', color='#1A237E', va='top')
        sy_cur -= 0.036
        ax_sp.text(0.06, sy_cur, sbody, fontsize=5.95, color='#263238', va='top', linespacing=1.28)
        sy_cur -= (sbody.count('\n') + 1) * 0.035 + 0.024

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 5: PLANO DE FACHADAS Y ELEVACIONES ARQUITECTÓNICAS (FORMATO 17x11 in)
# =============================================================================
def draw_sheet_frame_landscape(fig, title_line1, title_line2="", escala="1:75", sheet_num="5 / 6", fecha="OCT 2026"):
    """Marco doble azul reglamentario adaptado limpiamente a formato apaisado 17x11 pulgadas."""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.add_patch(Rectangle((0.014, 0.018), 0.972, 0.964, fill=False, edgecolor=C_BLUE, lw=2.2))
    ax.add_patch(Rectangle((0.017, 0.023), 0.966, 0.954, fill=False, edgecolor=C_BLUE, lw=0.9))

    ax.text(0.025, 0.968, "REPÚBLICA BOLIVARIANA DE VENEZUELA",
            fontsize=13.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')
    ax.text(0.025, 0.942, "MUNICIPIO INDEPENDENCIA YARACUY",
            fontsize=12.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')

    ax.text(0.975, 0.966, "PROYECTO INTEGRAL: CHALET RÚSTICO ALPINO & COMERCIO",
            fontsize=9.0, fontweight='bold', color='#263238', ha='right', va='top')
    ax.text(0.975, 0.942, f"ELEVACIONES Y PERFIL TOPOGRÁFICO  |  LÁMINA {sheet_num}",
            fontsize=8.2, fontweight='bold', color=C_BLUE, ha='right', va='top')

    c_left, c_right = 0.017, 0.983
    c_bot = 0.023
    row_top = 0.078
    caj_top = 0.128

    ax.plot([c_left, c_right], [caj_top, caj_top], color=C_BLUE, lw=1.6)
    ax.plot([c_left, c_right], [row_top, row_top], color=C_BLUE, lw=1.2)

    ax.text(0.025, caj_top - 0.016, title_line1, fontsize=11.0, fontweight='bold', color=C_RED, ha='left', va='center')
    if title_line2:
        ax.text(0.025, caj_top - 0.036, title_line2, fontsize=8.8, fontweight='bold', color=C_RED, ha='left', va='center')
    ax.text(0.975, caj_top - 0.016,
            "PIEDRA RÚSTICA + MADERA MACHIHEMBRADA + CUBIERTA ALPINA 32°",
            fontsize=8.0, fontweight='bold', color='#37474F', ha='right', va='center')
    ax.text(0.975, caj_top - 0.036,
            "RESPETO ESTRICTO DE MEDIANERA (0,00 m INVASIÓN LINDERO VECINO)",
            fontsize=7.6, fontweight='bold', color=C_BLUE, ha='right', va='center')

    cols = [0.275, 0.465, 0.665, 0.825, 0.905]
    for cx in cols:
        ax.plot([cx, cx], [c_bot, row_top], color=C_BLUE, lw=1.0)

    ax.text(0.022, row_top - 0.011, "UBICACIÓN:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.146, row_top - 0.027, "AVENIDA 4 ENTRE CALLES 30 Y 31 30-7", fontsize=7.5, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.146, row_top - 0.043, "MUNICIPIO INDEPENDENCIA ESTADO YARACUY.", fontsize=7.0, fontweight='bold', color=C_RED, ha='center')

    ax.text(0.280, row_top - 0.011, "PROPIEDAD:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.370, row_top - 0.027, "ALVARO ARGELIO DIAZ FLOREZ.", fontsize=7.8, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.370, row_top - 0.043, "C.I.: 24.633.787", fontsize=7.4, fontweight='bold', color=C_RED, ha='center')

    ax.text(0.470, row_top - 0.011, "LEVANTADO CALCULADO Y DIGITALIZO:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.565, row_top - 0.027, "T.S.U. ANGEL CAMACARO M.", fontsize=7.8, fontweight='bold', color=C_RED, ha='center')
    ax.text(0.565, row_top - 0.043, "CVPT.: N° 1260         SOVIT.: N° 0050", fontsize=6.8, fontweight='bold', color=C_RED, ha='center')

    ax.text(0.670, row_top - 0.011, "REVISADO:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.745, row_top - 0.032, "PROYECTO REDISEÑO\nCHALET ALPINO", fontsize=6.8, fontweight='bold', color='#1B5E20', ha='center', va='center')

    ax.text(0.830, row_top - 0.011, "FECHA:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.865, row_top - 0.034, fecha, fontsize=8.5, fontweight='bold', color=C_RED, ha='center')

    ax.text(0.910, row_top - 0.011, "ESCALA:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.944, row_top - 0.034, escala, fontsize=9.0, fontweight='bold', color=C_RED, ha='center')


def draw_elev_shuttered_win(ax, x1, x2, z1, z2, shutters=True):
    """Ventana rústica en elevación con marco de madera, vidrio dividido y contraventanas de lamas."""
    ax.add_patch(Rectangle((x1, z1), x2 - x1, z2 - z1, facecolor='#E1F5FE', edgecolor='#222222', lw=0.85, zorder=4))
    xm, zm = 0.5 * (x1 + x2), 0.5 * (z1 + z2)
    ax.plot([xm, xm], [z1, z2], color='#3E2723', lw=0.9, zorder=5)
    ax.plot([x1, x2], [zm, zm], color='#3E2723', lw=0.7, zorder=5)
    if shutters:
        sw = min(0.32, 0.22 * (x2 - x1))
        for sx in (x1 - sw, x2):
            ax.add_patch(Rectangle((sx, z1), sw, z2 - z1, facecolor='#8D6E63', edgecolor='#222222', lw=0.65, zorder=4))
            for zz in np.linspace(z1 + 0.10, z2 - 0.10, 6):
                ax.plot([sx + 0.03, sx + sw - 0.03], [zz, zz], color='#3E2723', lw=0.45, zorder=5)


def draw_elev_x_railing(ax, x1, x2, z_floor, h_rail=1.05, n_bays=3):
    """Baranda alpina con Cruces de San Andrés en elevación."""
    ax.add_patch(Rectangle((x1, z_floor), x2 - x1, h_rail, facecolor='none', edgecolor='#4E342E', lw=0.9, zorder=6))
    ax.add_patch(Rectangle((x1, z_floor + h_rail - 0.08), x2 - x1, 0.08, facecolor='#6D4C41', edgecolor='black', lw=0.6, zorder=7))
    dx = (x2 - x1) / n_bays
    for b in range(n_bays):
        bx1, bx2 = x1 + b * dx, x1 + (b + 1) * dx
        ax.plot([bx1, bx1], [z_floor, z_floor + h_rail], color='#4E342E', lw=1.0, zorder=7)
        ax.plot([bx1 + 0.05, bx2 - 0.05], [z_floor + 0.10, z_floor + h_rail - 0.08], color='#5D4037', lw=0.85, zorder=6)
        ax.plot([bx2 - 0.05, bx1 + 0.05], [z_floor + 0.10, z_floor + h_rail - 0.08], color='#5D4037', lw=0.85, zorder=6)


def build_sheet_5_fachadas(pdf):
    fig = plt.figure(figsize=(17, 11), dpi=300)
    draw_sheet_frame_landscape(fig,
                               "PLANO DE FACHADAS Y ELEVACIONES ARQUITECTÓNICAS",
                               "FACHADA PRINCIPAL AV. 4  •  FACHADA POSTERIOR JARDÍN  •  ELEVACIÓN LATERAL CON DESNIVEL.",
                               escala="1:75", sheet_num="5 / 6")

    # -------------------------------------------------------------------------
    # 1. ARRIBA IZQUIERDA: FACHADA PRINCIPAL AVENIDA 4 (NORTE)
    # -------------------------------------------------------------------------
    ax_p = fig.add_axes([0.035, 0.525, 0.435, 0.395])
    ax_p.set_aspect('equal')
    ax_p.set_xlim(-2.2, 11.4)
    ax_p.set_ylim(-2.0, 9.8)
    ax_p.axis('off')

    ax_p.plot([-0.35, 10.4], [0.0, 0.0], color='#111111', lw=1.6, zorder=8)
    # Línea de lindero vecino intacta (X = 0.00..0.15)
    ax_p.add_patch(Rectangle((0.00, 0.00), 0.15, 6.28, facecolor='#E0E0E0', edgecolor='#777777', lw=0.6, linestyle='--', zorder=2))
    ax_p.text(-0.05, 3.20, "Lindero Vecino (0,00m Alero)", rotation=90, fontsize=5.3, color='#666666', ha='right', va='center')

    # Basamento Planta Baja en Piedra Rústica (Z: 0.00..3.00)
    ax_p.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=1.0, zorder=2))
    for sz in np.linspace(0.35, 2.65, 7):
        ax_p.plot([0.15, 9.15], [sz, sz], color='#B0BEC5', lw=0.45, zorder=2)

    # Portón Corredizo sobre Riel Lateral (X: 0.40..2.70, Z: 0.00..2.25)
    ax_p.add_patch(Rectangle((0.40, 0.00), 2.30, 2.25, facecolor='#D7CCC8', edgecolor='#222222', lw=0.95, zorder=4))
    for gx in np.linspace(0.68, 2.42, 7):
        ax_p.plot([gx, gx], [0.05, 2.20], color='#5D4037', lw=0.65, zorder=5)
    ax_p.add_patch(Rectangle((0.35, 2.25), 2.45, 0.14, facecolor='#37474F', edgecolor='black', lw=0.7, zorder=6))
    ax_p.text(1.55, 1.12, "PORTÓN CORREDIZO\nRIEL LATERAL\n(2,30 x 2,25 m)", fontsize=5.3, fontweight='bold',
              color='#222222', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # 2 Accesos Abiertos Frutería con Santamarías de Caracol Superiores (X: 3.65..5.75 y 6.20..8.80)
    for sx1, sx2, slbl in [(3.65, 5.75, "ACCESO FRUTERÍA 1\nSantamaría Caracol\n(2,10 m)"),
                           (6.20, 8.80, "ACCESO FRUTERÍA 2\nSantamaría Caracol\n(2,60 m)")]:
        ax_p.add_patch(Rectangle((sx1, 0.00), sx2 - sx1, 2.10, facecolor='#FFFDF7', edgecolor='#222222', lw=0.9, zorder=4))
        # Tambor cilíndrico superior (caracol enrollable)
        ax_p.add_patch(Rectangle((sx1, 2.10), sx2 - sx1, 0.34, facecolor='#CFD8DC', edgecolor='#263238', lw=0.85, zorder=5))
        for ry_l in [2.18, 2.27, 2.36]:
            ax_p.plot([sx1 + 0.05, sx2 - 0.05], [ry_l, ry_l], color='#455A64', lw=0.55, zorder=6)
        ax_p.text(0.5 * (sx1 + sx2), 1.05, slbl, fontsize=5.2, fontweight='bold', color='#1A237E', ha='center', va='center', zorder=6)

    # Marquesina frontal de madera sobre accesos comerciales (Z = 2.52..2.66)
    ax_p.add_patch(Rectangle((3.45, 2.52), 5.55, 0.14, facecolor='#6D4C41', edgecolor='black', lw=0.75, zorder=6))

    # Cuerpo Segundo Piso en Madera Machihembrada (Z: 3.00..5.85) + Parapeto Propio Izquierdo (+6.28 m)
    ax_p.add_patch(Rectangle((0.15, 2.85), 9.00, 0.15, facecolor='#90A4AE', edgecolor='black', lw=0.8, zorder=5))
    ax_p.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=1.0, zorder=3))
    for wz in np.linspace(3.25, 5.65, 9):
        ax_p.plot([0.30, 9.15], [wz, wz], color='#BCAAA4', lw=0.45, zorder=3)
    ax_p.add_patch(Rectangle((0.15, 3.00), 0.18, 3.28, facecolor='#6D4C41', edgecolor='black', lw=0.8, zorder=6))

    # Ventanales tras las terrazas + Muro de Privacidad Eje 2 + Poste A0 + Barandas en X
    draw_elev_shuttered_win(ax_p, 0.65, 2.55, 3.00, 5.20, shutters=False)
    draw_elev_shuttered_win(ax_p, 3.15, 5.55, 3.85, 5.20, shutters=False)
    draw_elev_shuttered_win(ax_p, 6.50, 8.50, 3.00, 5.20, shutters=False)
    ax_p.add_patch(Rectangle((2.68, 3.00), 0.29, 2.85, facecolor='#5D4037', edgecolor='black', lw=0.75, zorder=7))
    ax_p.add_patch(Rectangle((5.85, 3.00), 0.15, 2.85, facecolor='#5D4037', edgecolor='black', lw=0.75, zorder=7))
    draw_elev_x_railing(ax_p, 0.35, 2.68, 3.00, h_rail=1.05, n_bays=2)
    draw_elev_x_railing(ax_p, 2.97, 5.85, 3.00, h_rail=1.05, n_bays=3)
    draw_elev_x_railing(ax_p, 6.00, 9.05, 3.00, h_rail=1.05, n_bays=3)

    # Cubierta Alpina Asimétrica 32° (Cumbrera X = 4.85, Z = 8.70 m, Alero Derecho X = 10.10, Z = 5.42 m)
    gable_poly = [(0.33, 5.85), (0.45, 5.95), (4.85, 8.70), (9.15, 6.01), (9.15, 5.85)]
    ax_p.add_patch(Polygon(gable_poly, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.95, zorder=4))
    # Cercha Alpina Vista King-Post
    ax_p.plot([0.45, 9.15], [5.85, 5.85], color='#4E342E', lw=2.0, zorder=6)
    ax_p.plot([4.85, 4.85], [5.85, 8.68], color='#4E342E', lw=2.2, zorder=6)
    ax_p.plot([4.85, 2.65], [6.15, 7.32], color='#4E342E', lw=1.4, zorder=6)
    ax_p.plot([4.85, 7.05], [6.15, 7.32], color='#4E342E', lw=1.4, zorder=6)
    # Faldones de cubierta con espesor 0.18 m
    roof_top = [(0.45, 5.95), (4.85, 8.70), (10.10, 5.42), (10.10, 5.62), (4.85, 8.90), (0.45, 6.15)]
    ax_p.add_patch(Polygon(roof_top, closed=True, facecolor='#5D4037', edgecolor='black', lw=1.0, zorder=7))

    # Cotas y Niveles Fachada Principal
    for z_lv, z_txt in [(0.00, "±0,00"), (3.00, "+3,00"), (5.85, "+5,85"), (8.70, "+8,70")]:
        ax_p.plot([-0.65, 0.10], [z_lv, z_lv], color='#555555', lw=0.5, linestyle=':')
        ax_p.text(-0.72, z_lv, f"N.P.T. {z_txt}", fontsize=5.4, fontweight='bold', color='#222222', ha='right', va='center')

    draw_dim_h(ax_p, 0.15, 9.15, 9.25, "9,00 (Frente Propio)", fontsize=5.8)
    draw_dim_h(ax_p, 9.15, 10.10, 9.25, "0,95", fontsize=5.6)
    draw_dim_v(ax_p, 10.65, 0.00, 3.00, "3,00", fontsize=5.6, text_side='right')
    draw_dim_v(ax_p, 10.65, 3.00, 5.85, "2,85", fontsize=5.6, text_side='right')
    draw_dim_v(ax_p, 10.65, 5.85, 8.70, "2,85", fontsize=5.6, text_side='right')

    ax_p.text(4.85, -0.75, "FACHADA PRINCIPAL AVENIDA 4\n(PLANTA BAJA COMERCIAL Y SEGUNDO PISO CHALET)",
              fontsize=8.0, fontweight='bold', color='#111111', ha='center', va='top')
    ax_p.plot([1.10, 8.60], [-1.72, -1.72], color='black', lw=1.0)

    # -------------------------------------------------------------------------
    # 2. ARRIBA DERECHA: FACHADA POSTERIOR SUR (SÓTANO + P.B. + P.A. + BUHARDILLA)
    # -------------------------------------------------------------------------
    ax_s = fig.add_axes([0.505, 0.525, 0.455, 0.395])
    ax_s.set_aspect('equal')
    ax_s.set_xlim(-2.0, 11.4)
    ax_s.set_ylim(-4.5, 9.8)
    ax_s.axis('off')

    ax_s.plot([-0.35, 10.3], [-2.55, -2.55], color='#4E342E', lw=1.6, zorder=8)

    # Sótano en Piedra Rústica (Z: -2.55..0.00) + Doble Puerta Francesa + Pérgola
    ax_s.add_patch(Rectangle((0.15, -2.55), 9.00, 2.55, facecolor='#CFD8DC', edgecolor='#222222', lw=1.0, zorder=2))
    draw_elev_shuttered_win(ax_s, 0.75, 2.35, -1.60, -0.45, shutters=True)
    draw_elev_shuttered_win(ax_s, 3.25, 4.30, -1.40, -0.45, shutters=False)
    draw_elev_shuttered_win(ax_s, 4.88, 5.68, -1.40, -0.45, shutters=False)
    # Doble Puerta Francesa (6.35..8.55, Z: -2.55..-0.45)
    ax_s.add_patch(Rectangle((6.35, -2.55), 2.20, 2.10, facecolor='#E1F5FE', edgecolor='#3E2723', lw=1.1, zorder=4))
    ax_s.plot([7.45, 7.45], [-2.55, -0.45], color='#3E2723', lw=1.2, zorder=5)
    # Pérgola Rústica de Madera (X: 4.85..9.05, viga en Z = -0.22)
    ax_s.add_patch(Rectangle((4.85, -0.25), 4.20, 0.14, facecolor='#6D4C41', edgecolor='black', lw=0.75, zorder=6))
    for pgx in [4.95, 6.95, 8.85]:
        ax_s.add_patch(Rectangle((pgx, -2.55), 0.18, 2.30, facecolor='#6D4C41', edgecolor='black', lw=0.65, zorder=6))

    # Planta Baja Posterior: Gran Almacén Unificado (Z: 0.00..3.00) con 3 ventanas altas
    ax_s.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=1.0, zorder=2))
    draw_elev_shuttered_win(ax_s, 0.55, 2.35, 1.35, 2.45, shutters=False)
    draw_elev_shuttered_win(ax_s, 4.10, 5.10, 1.45, 2.45, shutters=False)
    draw_elev_shuttered_win(ax_s, 7.00, 8.40, 1.35, 2.45, shutters=False)

    # Segundo Piso Posterior (Z: 3.00..5.85)
    ax_s.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=1.0, zorder=3))
    for wz in np.linspace(3.30, 5.55, 8):
        ax_s.plot([0.30, 9.15], [wz, wz], color='#BCAAA4', lw=0.45, zorder=3)
    draw_elev_shuttered_win(ax_s, 0.85, 2.35, 4.05, 5.15, shutters=False)
    draw_elev_shuttered_win(ax_s, 3.35, 5.40, 3.90, 5.20, shutters=True)
    draw_elev_shuttered_win(ax_s, 6.65, 8.45, 3.95, 5.15, shutters=True)

    # Buhardilla Técnica del Tanque 1.000 L (X: 0.15..3.86, Z: 5.68..8.08) + Parapeto Propio (+7.85 m)
    ax_s.add_patch(Rectangle((0.15, 3.00), 0.18, 4.85, facecolor='#5D4037', edgecolor='black', lw=0.8, zorder=7))
    dorm_poly = [(0.33, 5.68), (2.90, 5.68), (2.90, 7.93), (0.33, 7.56)]
    ax_s.add_patch(Polygon(dorm_poly, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.95, zorder=5))
    # Panel Doble de Celosía Ventilada (0.88..2.33, Z: 5.90..7.35) + Silueta punteada Tanque 1.000 L
    ax_s.add_patch(Rectangle((0.88, 5.90), 1.45, 1.45, facecolor='#BCAAA4', edgecolor='#3E2723', lw=0.9, zorder=6))
    ax_s.plot([1.605, 1.605], [5.90, 7.35], color='#3E2723', lw=0.9, zorder=7)
    for lz in np.linspace(6.02, 7.24, 9):
        ax_s.plot([0.92, 2.29], [lz, lz], color='#4E342E', lw=0.5, zorder=6)
    ax_s.add_patch(Rectangle((1.05, 5.80), 1.10, 1.30, fill=False, edgecolor='#0D47A1', lw=0.75, linestyle='--', zorder=7))
    ax_s.text(1.60, 8.15, "Buhardilla Tanque 1.000 L", fontsize=5.2, fontweight='bold', color='#0D47A1', ha='center')

    # Hastial Principal Sur acoplado a Buhardilla + Cubierta 32°
    gable_s = [(2.90, 5.85), (2.90, 7.93), (3.86, 8.08), (4.85, 8.70), (9.15, 6.01), (9.15, 5.85)]
    ax_s.add_patch(Polygon(gable_s, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.95, zorder=4))
    ax_s.plot([0.40, 3.86], [7.64, 8.16], color='#4E342E', lw=2.2, zorder=7)
    roof_s = [(3.86, 8.08), (4.85, 8.70), (10.10, 5.42), (10.10, 5.62), (4.85, 8.90), (3.86, 8.28)]
    ax_s.add_patch(Polygon(roof_s, closed=True, facecolor='#5D4037', edgecolor='black', lw=1.0, zorder=7))

    for z_lv, z_txt in [(-2.55, "-2,55"), (0.00, "±0,00"), (3.00, "+3,00"), (5.68, "+5,68"), (8.70, "+8,70")]:
        ax_s.plot([-0.60, 0.10], [z_lv, z_lv], color='#555555', lw=0.5, linestyle=':')
        ax_s.text(-0.68, z_lv, f"N.P.T. {z_txt}", fontsize=5.3, fontweight='bold', color='#222222', ha='right', va='center')

    draw_dim_h(ax_s, 0.15, 9.15, 9.25, "9,00", fontsize=5.8)
    draw_dim_v(ax_s, 10.55, -2.55, 0.00, "2,55 (Sótano)", fontsize=5.5, text_side='right')
    draw_dim_v(ax_s, 10.55,  0.00, 3.00, "3,00 (P.B.)", fontsize=5.5, text_side='right')
    draw_dim_v(ax_s, 10.55,  3.00, 5.85, "2,85 (P.A.)", fontsize=5.5, text_side='right')

    ax_s.text(4.85, -3.15, "FACHADA POSTERIOR SUR\n(PATIO PÉRGOLA, SÓTANO, GRAN ALMACÉN, P.A. Y BUHARDILLA TANQUE)",
              fontsize=7.8, fontweight='bold', color='#111111', ha='center', va='top')
    ax_s.plot([0.60, 9.10], [-4.22, -4.22], color='black', lw=1.0)

    # -------------------------------------------------------------------------
    # 3. PANEL INFERIOR ANCHO COMPLETO: ELEVACIÓN LATERAL Y PERFIL DE TERRENO (24,71 m)
    # -------------------------------------------------------------------------
    ax_l = fig.add_axes([0.035, 0.145, 0.930, 0.355])
    ax_l.set_aspect('equal')
    ax_l.set_xlim(-2.2, 27.6)
    ax_l.set_ylim(-4.6, 9.6)
    ax_l.axis('off')

    # Perfil escalonado real del Terreno Natural (Patio Sur Y=0..3 + Sótano Y=3..11.3 a -2.55 m -> Av. 4 Y=24.71 a ±0.00 m)
    terr_y = [0.00, 11.30, 12.10, 12.10, 13.00, 13.00, 13.90, 13.90, 14.80, 14.80, 15.70, 15.70, 25.10]
    terr_z = [-2.55, -2.55, -2.55, -2.04, -2.04, -1.53, -1.53, -1.02, -1.02, -0.51, -0.51,  0.00,  0.00]
    earth_poly = [(0.00, -3.55)] + list(zip(terr_y, terr_z)) + [(25.10, -3.55)]
    ax_l.add_patch(Polygon(earth_poly, closed=True, facecolor='#EFEBE9', edgecolor='none', zorder=1))
    ax_l.plot(terr_y, terr_z, color='#6D4C41', lw=2.0, zorder=6)
    ax_l.text(19.6, -2.10, "PERFIL DE TERRENO NATURAL Y TALUD ESCALONADO", fontsize=6.6, fontweight='bold', color='#5D4037', ha='center')

    # Patio Trasero y Pérgola (Y_loc: 0.80..3.00, Z: -2.55..-0.20)
    ax_l.add_patch(Rectangle((0.80, -0.25), 2.20, 0.14, facecolor='#6D4C41', edgecolor='black', lw=0.7, zorder=4))
    for py_p in [0.90, 1.90]:
        ax_l.add_patch(Rectangle((py_p, -2.55), 0.16, 2.30, facecolor='#6D4C41', edgecolor='black', lw=0.65, zorder=4))
    ax_l.text(1.55, 0.55, "Patio y\nPérgola", fontsize=5.6, fontweight='bold', color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Nivel Sótano Este (Y_loc: 3.00..11.30, Z: -2.55..0.00)
    ax_l.add_patch(Rectangle((3.00, -2.55), 8.30, 2.55, facecolor='#CFD8DC', edgecolor='#222222', lw=1.0, zorder=2))
    for wy1, wy2, sh in [(4.00, 5.65, True), (7.25, 8.90, True), (10.00, 10.95, False)]:
        draw_elev_shuttered_win(ax_l, wy1, wy2, -1.55, -0.45, shutters=sh)

    # Planta Baja Este (Y_loc: 3.00..24.71, Z: 0.00..3.00) con sus 7 ventanas exactas (desplazadas +3.00 m por OFFSET_Y)
    ax_l.add_patch(Rectangle((3.00, 0.00), 21.71, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=1.0, zorder=2))
    pb_wins = [(4.10, 5.50), (7.10, 8.00), (9.30, 11.00), (12.65, 14.85), (16.15, 17.05), (18.50, 20.70), (21.80, 24.00)]
    for wy1, wy2 in pb_wins:
        draw_elev_shuttered_win(ax_l, wy1, wy2, 1.05, 2.25, shutters=False)

    # Segundo Piso Este (Y_loc: 3.00..24.71, Z: 3.00..5.85) con sus 5 ventanas exactas + Balcón Master en Y_loc: 22.60..24.71
    ax_l.add_patch(Rectangle((3.00, 2.85), 21.71, 0.15, facecolor='#90A4AE', edgecolor='black', lw=0.75, zorder=4))
    ax_l.add_patch(Rectangle((3.00, 3.00), 19.60, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=1.0, zorder=3))
    for wz in np.linspace(3.30, 5.55, 7):
        ax_l.plot([3.00, 22.60], [wz, wz], color='#BCAAA4', lw=0.45, zorder=3)

    p2_wins = [(4.10, 5.90, True), (7.90, 8.85, False), (10.15, 11.55, True), (13.65, 14.65, False), (19.00, 21.20, True)]
    for wy1, wy2, sh in p2_wins:
        draw_elev_shuttered_win(ax_l, wy1, wy2, 3.95, 5.15, shutters=sh)

    # Terraza Frontal derecha (Y_loc: 22.60..24.71)
    ax_l.add_patch(Rectangle((22.60, 3.00), 2.11, 2.85, facecolor='#FFFDF9', edgecolor='#4E342E', lw=0.8, zorder=3))
    draw_elev_x_railing(ax_l, 22.60, 24.71, 3.00, h_rail=1.05, n_bays=2)
    ax_l.add_patch(Rectangle((24.52, 3.00), 0.19, 2.85, facecolor='#5D4037', edgecolor='black', lw=0.75, zorder=6))

    # Cubierta Chalet vista longitudinalmente (Alero Sur Y_loc=2.00 hasta Av. 4 Y_loc=24.96; Cumbrera +8,88 m)
    ax_l.add_patch(Rectangle((2.00, 5.62), 22.96, 3.26, facecolor='#795548', edgecolor='#222222', lw=1.0, zorder=4))
    for r_z in np.linspace(6.00, 8.55, 8):
        ax_l.plot([2.00, 24.96], [r_z, r_z], color='#5D4037', lw=0.5, zorder=4)
    # Fascia de alero derecho (Z = 5.42..5.62) + Canecillos de madera vistos cada 1,25 m
    ax_l.add_patch(Rectangle((2.00, 5.42), 22.96, 0.20, facecolor='#4E342E', edgecolor='black', lw=0.8, zorder=6))
    for cy_r in np.linspace(2.35, 24.55, 19):
        ax_l.add_patch(Rectangle((cy_r - 0.06, 5.26), 0.12, 0.16, facecolor='#3E2723', edgecolor='black', lw=0.45, zorder=6))

    # Cotas Longitudinales y Verticales
    draw_dim_h(ax_l, 0.00,  3.00, 9.15, "3,00 (Patio)", fontsize=5.8)
    draw_dim_h(ax_l, 3.00, 24.71, 9.15, "21,71 (Largo Edificación)", fontsize=6.0)
    draw_dim_v(ax_l, -0.75, -2.55, 0.00, "2,55", x_ref=0.00, fontsize=5.6)
    draw_dim_v(ax_l, -0.75,  0.00, 5.85, "5,85", x_ref=3.00, fontsize=5.6)
    draw_dim_v(ax_l, 25.45,  0.00, 8.88, "8,88 (Cumbrera)", x_ref=24.96, fontsize=5.6, text_side='right')
    ax_l.text(26.65, 0.65, "AVENIDA 4\n(±0,00 m)", fontsize=6.0, fontweight='bold', color=C_RED, ha='center')

    ax_l.text(13.5, -3.75, "ELEVACIÓN LATERAL COMPLETA — SÓTANO, PLANTA BAJA, SEGUNDO PISO Y TALUD DE TERRENO NATURAL",
              fontsize=8.5, fontweight='bold', color='#111111', ha='center', va='top')
    ax_l.plot([3.50, 23.50], [-4.32, -4.32], color='black', lw=1.1)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 6: LEVANTAMIENTO POLIGONAL DE LINDEROS, RETÍCULA U.T.M. Y SITUACIÓN
# =============================================================================
def build_sheet_6_terreno_utm(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "LEVANTAMIENTO POLIGONAL DE LINDEROS",
                     "COORDENADAS U.T.M., CUADRO DE ÁREAS, IMPLANTACIÓN Y SITUACIÓN RELATIVA.",
                     escala="1:200", sheet_num="6 / 6")

    # Línea azul divisoria horizontal entre el encabezado técnico y el plano UTM (fiel a Pág. 5)
    ax_bg = fig.axes[0]
    ax_bg.plot([0.022, 0.978], [0.718, 0.718], color=C_BLUE, lw=1.6)

    # -------------------------------------------------------------------------
    # 1. ARRIBA IZQUIERDA: CUADRO DE COORDENADAS U.T.M. + CUADRO DE ÁREAS
    # -------------------------------------------------------------------------
    ax_utmtbl = fig.add_axes([0.032, 0.798, 0.425, 0.138])
    ax_utmtbl.set_xlim(0, 1)
    ax_utmtbl.set_ylim(0, 1)
    ax_utmtbl.axis('off')

    ax_utmtbl.add_patch(Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=C_BLUE, lw=1.5))
    ax_utmtbl.plot([0, 1], [0.82, 0.82], color=C_BLUE, lw=1.1)
    ax_utmtbl.text(0.50, 0.91, "CUADRO DE COORDENADAS U.T.M.", fontsize=7.8,
                   fontweight='bold', color=C_RED, ha='center', va='center')

    # Sub-encabezados fieles a Pág. 5 de planos de casa.pdf
    ax_utmtbl.plot([0, 1], [0.58, 0.58], color=C_BLUE, lw=0.9)
    ax_utmtbl.plot([0, 0.16], [0.70, 0.70], color=C_BLUE, lw=0.7)
    ax_utmtbl.plot([0.64, 1.00], [0.70, 0.70], color=C_BLUE, lw=0.7)
    v_cols = [0.08, 0.16, 0.42, 0.57, 0.64, 0.82]
    for vc in v_cols:
        y_top_c = 0.70 if vc in (0.08, 0.82) else 0.82
        ax_utmtbl.plot([vc, vc], [0.0, y_top_c], color=C_BLUE, lw=0.75)

    ax_utmtbl.text(0.08, 0.76, "LADO", fontsize=5.2, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.04, 0.64, "EST", fontsize=5.0, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.12, 0.64, "PV", fontsize=5.0, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.29, 0.70, "RUMBO", fontsize=5.5, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.495, 0.70, "DISTANCIA", fontsize=5.3, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.605, 0.70, "P", fontsize=5.5, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.82, 0.76, "C O O R D E N A D A S", fontsize=5.2, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.73, 0.64, "NORTE", fontsize=5.2, fontweight='bold', color=C_BLUE, ha='center', va='center')
    ax_utmtbl.text(0.91, 0.64, "ESTE", fontsize=5.2, fontweight='bold', color=C_BLUE, ha='center', va='center')

    utm_rows = [
        ("",  "",  "",                  "",        "1", "1.141.664,17", "529.755,04"),
        ("1", "2", "N 57°10'22,40\" E", "11,37 m", "2", "1.141.670,33", "529.764,60"),
        ("2", "3", "S 30°17'59,36\" E", "24,72 m", "3", "1.141.648,99", "529.777,07"),
        ("3", "4", "S 57°10'22,40\" W", "10,81 m", "4", "1.141.643,13", "529.767,99"),
        ("4", "1", "N 31°36'27,01\" W", "24,70 m", "1", "1.141.664,17", "529.755,04"),
    ]
    row_h = 0.58 / 5.0
    x_centers = [0.04, 0.12, 0.29, 0.495, 0.605, 0.73, 0.91]
    for r_i, r_vals in enumerate(utm_rows):
        ry_bot = 0.58 - (r_i + 1) * row_h
        if r_i < 4:
            ax_utmtbl.plot([0, 1], [ry_bot, ry_bot], color=C_BLUE, lw=0.65)
        ry_mid = ry_bot + 0.5 * row_h
        for c_i, val in enumerate(r_vals):
            ax_utmtbl.text(x_centers[c_i], ry_mid, val, fontsize=5.4, fontweight='bold',
                           color='#111111', ha='center', va='center')

    # Cuadro de Áreas Oficial debajo del Cuadro UTM
    ax_ar = fig.add_axes([0.032, 0.726, 0.425, 0.064])
    ax_ar.set_xlim(0, 1)
    ax_ar.set_ylim(0, 1)
    ax_ar.axis('off')
    ax_ar.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FFFDE7', edgecolor=C_BLUE, lw=1.2))
    ax_ar.text(0.025, 0.74, "ÁREA DE TERRENO POLIGONAL: 273,81 m².",
               fontsize=7.1, fontweight='bold', color=C_RED, va='center')
    ax_ar.text(0.025, 0.44, "ÁREA TOTAL CONSTRUIDA TECHADA: 477,72 m²  (+ 9,24 m² Pérgola).",
               fontsize=6.7, fontweight='bold', color=C_RED, va='center')
    ax_ar.text(0.025, 0.16, "Desglose: Sótano 74,70 m² | P. Baja 195,39 m² | 2do Piso 195,39 m² | Buhardilla 12,24 m²",
               fontsize=5.4, fontweight='bold', color='#263238', va='center')

    # -------------------------------------------------------------------------
    # 2. ARRIBA CENTRO: CUADRO DE LINDEROS (ESTILO EXACTO PÁG. 5)
    # -------------------------------------------------------------------------
    ax_lin = fig.add_axes([0.468, 0.742, 0.132, 0.194])
    ax_lin.set_xlim(0, 1)
    ax_lin.set_ylim(0, 1)
    ax_lin.axis('off')
    ax_lin.add_patch(Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=C_BLUE, lw=1.5))
    ax_lin.plot([0, 1], [0.89, 0.89], color=C_BLUE, lw=1.1)
    ax_lin.text(0.50, 0.945, "LINDEROS.", fontsize=7.0, fontweight='bold', color=C_BLUE, ha='center', va='center')

    linderos_list = [
        ("NORESTE",  "CASA\nDE\nMIGUEL RODRIGUEZ."),
        ("SURESTE",  "SOLAR\nDE\nMIGUEL RODRIGUEZ."),
        ("NOROESTE", "AVENIDA 4."),
        ("SUROESTE", "CASA\nDE\nMARIO GRATEROL."),
    ]
    blk_h = 0.89 / 4.0
    for l_i, (l_dir, l_who) in enumerate(linderos_list):
        y_top_b = 0.89 - l_i * blk_h
        y_hdr_b = y_top_b - 0.055
        y_bot_b = y_top_b - blk_h
        ax_lin.plot([0, 1], [y_hdr_b, y_hdr_b], color=C_BLUE, lw=0.8)
        if l_i < 3:
            ax_lin.plot([0, 1], [y_bot_b, y_bot_b], color=C_BLUE, lw=1.0)
        ax_lin.text(0.50, 0.5 * (y_top_b + y_hdr_b), l_dir, fontsize=5.5, fontweight='bold',
                    color=C_RED, ha='center', va='center')
        ax_lin.text(0.50, 0.5 * (y_hdr_b + y_bot_b), l_who, fontsize=4.8, fontweight='bold',
                    color='#222222', ha='center', va='center', linespacing=1.12)

    # -------------------------------------------------------------------------
    # 3. ARRIBA DERECHA: CROQUIS DE SITUACIÓN RELATIVA S/ESC. (MANZANAS ROTADAS)
    # -------------------------------------------------------------------------
    ax_sit = fig.add_axes([0.612, 0.752, 0.358, 0.184])
    ax_sit.set_aspect('equal')
    ax_sit.set_xlim(0, 11.8)
    ax_sit.set_ylim(0, 7.6)
    ax_sit.set_xticks([])
    ax_sit.set_yticks([])
    for sp in ax_sit.spines.values():
        sp.set_edgecolor(C_BLUE)
        sp.set_linewidth(1.6)

    ang_r = math.radians(38.0)
    ca, sa = math.cos(ang_r), math.sin(ang_r)
    def rot_pt(u, v):
        return (5.8 + u * ca - v * sa, 3.8 + u * sa + v * ca)

    # Manzanas urbanas en coordenadas locales de la trama vial de Independencia (u: SW->NE, v: SE->NW)
    u_intervals = [(-9.5, -3.2), (-2.1, 3.3), (4.4, 10.2)]
    v_intervals = [(-6.8, -2.0), (-1.1, 1.3), (2.5, 7.2)]
    for u1, u2 in u_intervals:
        for v1, v2 in v_intervals:
            pts_b = [rot_pt(u1, v1), rot_pt(u2, v1), rot_pt(u2, v2), rot_pt(u1, v2)]
            ax_sit.add_patch(Polygon(pts_b, closed=True, facecolor='#EFEFEF', edgecolor='#333333', lw=0.8, zorder=2))

    # Lote exacto resaltado en azul rey sobre el frente sureste de AVENIDA 4 entre Calle 30 y Calle 31
    lot_sit_pts = [rot_pt(0.55, -2.00), rot_pt(1.25, -2.00), rot_pt(1.25, -3.25), rot_pt(0.55, -3.25)]
    ax_sit.add_patch(Polygon(lot_sit_pts, closed=True, facecolor=C_BLUE, edgecolor='#000066', lw=1.0, zorder=5))

    # Etiquetas viales rotadas idénticas a Pág. 5 de planos de casa.pdf (con clip_on=True dentro del marco azul)
    lx, ly = rot_pt(-0.8, 1.90)
    ax_sit.text(lx, ly, "Av. LIBERTADOR", rotation=38, fontsize=5.8, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    lx2, ly2 = rot_pt(0.3, -1.55)
    ax_sit.text(lx2, ly2, "AVENIDA 4", rotation=38, fontsize=5.3, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx1, sy1 = rot_pt(3.85, 2.2)
    ax_sit.text(sx1, sy1, "Calle 29", rotation=-52, fontsize=5.1, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx2, sy2 = rot_pt(-2.65, 0.2)
    ax_sit.text(sx2, sy2, "Calle 30", rotation=-52, fontsize=5.1, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx3, sy3 = rot_pt(-2.65, -2.6)
    ax_sit.text(sx3, sy3, "Calle 31", rotation=-52, fontsize=5.1, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)

    ax_bg.text(0.968, 0.730, "SITUACIÓN RELATIVA S/ESC.", fontsize=7.0, fontweight='bold', color=C_BLUE, ha='right', va='center')

    # -------------------------------------------------------------------------
    # 4. PLANO PRINCIPAL DE LEVANTAMIENTO POLIGONAL Y HUELLA EN RETÍCULA U.T.M.
    # -------------------------------------------------------------------------
    ax_u = fig.add_axes([0.025, 0.100, 0.950, 0.614])
    ax_u.set_aspect('equal')
    ax_u.set_xlim(529740.5, 529793.5)
    ax_u.set_ylim(1141631.5, 1141684.5)
    ax_u.axis('off')

    # Retícula U.T.M. cada 10,00 m con tipografía fiel a Pág. 5 de planos de casa.pdf
    for n_val in [1141640, 1141650, 1141660, 1141670, 1141680]:
        ax_u.plot([529740.5, 529793.5], [n_val, n_val], color='#888888', lw=0.55, zorder=1)
        n_num = f"{n_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ax_u.text(529740.8, n_val + 0.35, f"N.={n_num}", fontsize=7.6, fontweight='bold', color='#111111', ha='left', va='bottom', zorder=8)

    for e_val in [529750, 529760, 529770, 529780, 529790]:
        ax_u.plot([e_val, e_val], [1141631.5, 1141684.5], color='#888888', lw=0.55, zorder=1)
        e_num = f"{e_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ax_u.text(e_val - 0.35, 1141632.2, f"E.={e_num}", rotation=90, fontsize=7.6, fontweight='bold', color='#111111', ha='right', va='bottom', zorder=8)

    # Transformación exacta Local Parcela (P-4 origen, eje Y hacia P-1) -> U.T.M.
    P1 = (529755.04, 1141664.17)
    P2 = (529764.60, 1141670.33)
    P3 = (529777.07, 1141648.99)
    P4 = (529767.99, 1141643.13)

    ux_e, ux_n =  0.851615, 0.524164
    uy_e, uy_n = -0.524164, 0.851615

    def loc_to_utm(xl, yl):
        return (P4[0] + xl * ux_e + yl * uy_e, P4[1] + xl * ux_n + yl * uy_n)

    # Trazado urbano real de AVENIDA 4. y CALLE 30. (aceras y calzadas como en Pág. 5)
    # Borde sur de acera Av. 4 pasa por P-1 -> P-2 y llega a esquina Calle 30 en xl = 22.8
    av4_s1 = [loc_to_utm(-20.0, 24.71), P1, P2, loc_to_utm(22.8, 25.18), loc_to_utm(38.0, 0.50)]
    av4_s2 = [loc_to_utm(-20.0, 26.20), loc_to_utm(21.8, 26.90), loc_to_utm(36.8, 2.50)]
    for seq in (av4_s1, av4_s2):
        xs_c, ys_c = zip(*seq)
        ax_u.plot(xs_c, ys_c, color='#444444', lw=0.65, zorder=2)

    # Acera opuesta noroeste de Avenida 4 + esquina norte Calle 30
    av4_n1 = [loc_to_utm(-20.0, 34.20), loc_to_utm(17.5, 35.00), loc_to_utm(19.5, 39.50)]
    av4_n2 = [loc_to_utm(-20.0, 35.60), loc_to_utm(16.2, 36.40), loc_to_utm(18.2, 40.50)]
    for seq in (av4_n1, av4_n2):
        xs_c, ys_c = zip(*seq)
        ax_u.plot(xs_c, ys_c, color='#444444', lw=0.65, zorder=2)

    c30_e1 = [loc_to_utm(29.5, 38.0), loc_to_utm(43.0, 16.0)]
    c30_e2 = [loc_to_utm(31.0, 38.8), loc_to_utm(44.5, 16.8)]
    for seq in (c30_e1, c30_e2):
        xs_c, ys_c = zip(*seq)
        ax_u.plot(xs_c, ys_c, color='#444444', lw=0.65, zorder=2)

    # Poligonal Oficial de Linderos en Rojo (P-1 -> P-2 -> P-3 -> P-4)
    lot_poly = [P1, P2, P3, P4]
    ax_u.add_patch(Polygon(lot_poly, closed=True, facecolor='#FFFDF5', edgecolor=C_RED, lw=1.4, zorder=3))

    # Patio Trasero y Terraza con Pérgola (X_loc: 4.85..9.05, Y_loc: 0.80..3.00)
    perg_pts = [loc_to_utm(4.85, 0.80), loc_to_utm(9.05, 0.80), loc_to_utm(9.05, 3.00), loc_to_utm(4.85, 3.00)]
    ax_u.add_patch(Polygon(perg_pts, closed=True, facecolor=C_STONE_SOFT, edgecolor='#455A64', lw=0.8, hatch='++', zorder=4))

    # Huella Exacta de la Nueva Edificación (X_loc: 0.15..9.15, Y_loc: 3.00..24.71 -> 9,00 x 21,71 m)
    bldg_w_pts = [loc_to_utm(0.15, 3.00), loc_to_utm(4.85, 3.00), loc_to_utm(4.85, 24.71), loc_to_utm(0.15, 24.71)]
    bldg_e_pts = [loc_to_utm(4.85, 3.00), loc_to_utm(9.15, 3.00), loc_to_utm(9.15, 24.71), loc_to_utm(4.85, 24.71)]
    ax_u.add_patch(Polygon(bldg_w_pts, closed=True, facecolor='#E0E0E0', edgecolor='#111111', lw=0.95, hatch='///', zorder=4))
    ax_u.add_patch(Polygon(bldg_e_pts, closed=True, facecolor='#ECEFF1', edgecolor='#111111', lw=0.95, hatch='\\\\\\', zorder=4))

    # Contorno de la Buhardilla Técnica del Tanque (X_loc: 0.15..2.90, Y_loc: 3.00..7.45)
    buh_pts = [loc_to_utm(0.15, 3.00), loc_to_utm(2.90, 3.00), loc_to_utm(2.90, 7.45), loc_to_utm(0.15, 7.45)]
    ax_u.add_patch(Polygon(buh_pts, closed=True, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=0.9, alpha=0.75, zorder=5))

    # Proyección punteada del Alero Derecho Propio (X_loc = 10.10 m, 100% dentro de P-2..P-3)
    eave_p1, eave_p2 = loc_to_utm(10.10, 2.00), loc_to_utm(10.10, 24.71)
    ax_u.plot([eave_p1[0], eave_p2[0]], [eave_p1[1], eave_p2[1]], color='#5D4037', lw=0.85, linestyle='--', zorder=5)

    # Vértices P-1..P-4 con círculos y etiquetas nítidas sin colisión
    v_labels = [
        (P1, "P-1", (-1.55, -0.15)),
        (P2, "P-2", ( 0.05,  1.25)),
        (P3, "P-3", ( 1.45, -0.10)),
        (P4, "P-4", (-0.95, -1.35)),
    ]
    for (vx, vy), v_name, (dx_l, dy_l) in v_labels:
        ax_u.add_patch(Circle((vx, vy), 0.30, facecolor='white', edgecolor='#111111', lw=1.0, zorder=7))
        ax_u.text(vx + dx_l, vy + dy_l, v_name, fontsize=9.0, fontweight='bold', color='#111111', ha='center', va='center', zorder=8)

    # Cotas de Linderos sobre los 4 lados del polígono
    m12 = (0.5 * (P1[0] + P2[0]) - 0.65, 0.5 * (P1[1] + P2[1]) + 0.95)
    m23 = (0.5 * (P2[0] + P3[0]) + 0.95, 0.5 * (P2[1] + P3[1]) + 0.55)
    m34 = (0.5 * (P3[0] + P4[0]) + 0.55, 0.5 * (P3[1] + P4[1]) - 0.95)
    m41 = (0.5 * (P4[0] + P1[0]) - 1.05, 0.5 * (P4[1] + P1[1]) - 0.55)
    ax_u.text(*m12, "11,37 m", rotation=32.8, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m23, "24,72 m", rotation=-59.7, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m34, "10,81 m", rotation=32.8, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m41, "24,70 m", rotation=-58.4, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)

    # Nombres de Calles y Vecinos Colindantes (rotados al estilo exacto de Pág. 5 de planos de casa.pdf)
    ax_u.text(529756.8, 1141672.0, "AVENIDA 4.", rotation=32.8, fontsize=8.8, fontweight='bold', color='#111111', ha='center', va='center')
    ax_u.text(529783.5, 1141676.0, "CALLE 30.", rotation=-58.0, fontsize=8.4, fontweight='bold', color='#111111', ha='center', va='center')
    ax_u.text(529776.2, 1141659.8, "CASA\nDE\nMIGUEL RODRIGUEZ.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')
    ax_u.text(529774.8, 1141641.8, "SOLAR\nDE\nMIGUEL RODRIGUEZ.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')
    ax_u.text(529756.8, 1141650.2, "CASA\nDE\nMARIO GRATEROL.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')

    # Rosa de los Vientos Norte U.T.M. y Leyenda de Implantación
    draw_north(ax_u, 529788.8, 1141680.2, r=1.55)

    leg_box = Rectangle((529780.4, 1141640.8), 12.4, 8.8, facecolor='white', edgecolor=C_BLUE, lw=0.9, alpha=0.96, zorder=9)
    ax_u.add_patch(leg_box)
    ax_u.text(529786.6, 1141648.6, "LEYENDA DE IMPLANTACIÓN", fontsize=5.8, fontweight='bold', color=C_RED, ha='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.9, 1141646.5), 1.3, 0.9, facecolor='#E0E0E0', edgecolor='black', lw=0.6, hatch='///', zorder=10))
    ax_u.text(529782.6, 1141646.95, "Edificación (9,00 x 21,71 m)", fontsize=5.1, color='#111111', va='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.9, 1141644.9), 1.3, 0.9, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=0.6, zorder=10))
    ax_u.text(529782.6, 1141645.35, "Buhardilla Tanque 1.000 L", fontsize=5.1, color='#111111', va='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.9, 1141643.3), 1.3, 0.9, facecolor=C_STONE_SOFT, edgecolor='#455A64', lw=0.6, hatch='++', zorder=10))
    ax_u.text(529782.6, 1141643.75, "Terraza Patio y Pérgola", fontsize=5.1, color='#111111', va='center', zorder=10)
    ax_u.plot([529780.9, 529782.2], [1141642.0, 1141642.0], color='#5D4037', lw=0.9, linestyle='--', zorder=10)
    ax_u.text(529782.6, 1141642.0, "Alero Derecho (0,95 m propio)", fontsize=5.1, color='#111111', va='center', zorder=10)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# EJECUCIÓN PRINCIPAL DEL PORTAFOLIO ARQUITECTÓNICO PDF
# =============================================================================
def main():
    output_pdf = os.path.join("01_Planos_y_Documentacion", "planos_nuevo_proyecto.pdf")
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    print(f"Generando portafolio oficial de 6 láminas: {output_pdf} ...")

    with PdfPages(output_pdf) as pdf:
        build_sheet_1_sotano(pdf)
        print("  [1/6] Nivel Sótano y Patio Jardín con Pérgola completado.")
        build_sheet_2_planta_baja(pdf)
        print("  [2/6] Planta Baja: Frutería, Gran Almacén y Estacionamiento completado.")
        build_sheet_3_segundo_piso(pdf)
        print("  [3/6] Segundo Piso Residencial Chalet + Buhardilla Tanque 1.000 L completado.")
        build_sheet_4_columnas_estructura(pdf)
        print("  [4/6] Distribución de Columnas y Ejes Estructurales completado.")
        build_sheet_5_fachadas(pdf)
        print("  [5/6] Fachadas Arquitectónicas y Perfil de Terreno completado.")
        build_sheet_6_terreno_utm(pdf)
        print("  [6/6] Levantamiento Poligonal de Linderos y Retícula U.T.M. completado.")

    print(f"¡ÉXITO! Portafolio PDF generado correctamente en: {output_pdf}")


if __name__ == "__main__":
    main()
