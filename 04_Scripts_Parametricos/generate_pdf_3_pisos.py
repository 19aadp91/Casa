"""
Generador Oficial de Planos Arquitectónicos en PDF ("01_Planos_y_Documentacion/planos_casa_3_pisos.pdf")
Estilo Normativo Municipal inspirado fielmente en "planos_nuevo_proyecto.pdf" y "planos de casa.pdf" (Independencia, Yaracuy).
Sincronizado 100% al milímetro con el modelo maestro "02_Modelos_CAD/casa_proyecto_3_pisos.dxf" ("build_casa_3_pisos.py").

Contenido del Portafolio (7 Láminas Formato Tabloide 11 x 17 / 17 x 11 pulgadas, 300 DPI Vectorial):
- Lámina 1/7: Planta Arquitectónica Nivel Sótano — Gran Bodega Mayorista y Patio de Maniobra (Z = -2,55 m) — Esc. 1:50
- Lámina 2/7: Planta Arquitectónica Planta Baja — Frutería Ampliada, Barra Jugos, Oficina, Garaje y Rampa (Z = ±0,00 m) — Esc. 1:75
- Lámina 3/7: Planta Arquitectónica Segundo Piso Social Bioclimático, Mamparas y Despensa Bajo Escalera (Z = +3,00 m) — Esc. 1:75
- Lámina 4/7: Planta Arquitectónica Nuevo Tercer Piso Privado, Claraboya, Terraza BBQ + Buhardilla 2.000L — Esc. 1:75 / 1:50
- Lámina 5/7: Plano Distribución de Columnas, Acero Negro P3, Hueco Claraboya y Ejes Estructurales — Esc. 1:75
- Lámina 6/7: Plano de Fachadas y Elevaciones de 3 Pisos + Sótano + Rampa Logística + Claraboya — Esc. 1:75 / 1:100
- Lámina 7/7: Levantamiento Poligonal de Linderos, Retícula U.T.M., Cuadro de Áreas (673,11 m²) y Situación — Esc. 1:200
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle
from matplotlib.backends.backend_pdf import PdfPages

# =============================================================================
# PALETA OFICIAL ESTILO "planos_nuevo_proyecto.pdf" + ACENTOS ARQUITECTÓNICOS
# =============================================================================
C_BLUE       = '#0000DD'   # Marco normativo doble y líneas del cajetín
C_RED        = '#D80000'   # Encabezados institucionales, títulos y datos propietario
C_WALL_FILL  = '#757575'   # Poché gris arquitectónico limpio de muros cortados
C_WALL_EDGE  = '#151515'   # Contorno nítido de muros
C_NEIGHBOR   = '#C8C8C8'   # Pared colindante del vecino izquierdo (intacta)
C_WINDOW     = '#007799'   # Vidrios y carpintería de ventanas / mamparas
C_DOOR       = '#3E2723'   # Hojas de puertas y carpintería de madera
C_FURN_EDGE  = '#5D5D5D'   # Contorno fino de mobiliario fijo y equipamiento
C_WOOD_SOFT  = '#EFE6DD'   # Relleno suave madera (mesones, islas, estantes, camas)
C_STONE_SOFT = '#E4E8EB'   # Relleno suave piedra laja / duchas / terrazas
C_GREEN_SOFT = '#E8F5E9'   # Jardineras, vegetación y detalles frescos
C_COLD_SOFT  = '#E1F5FE'   # Cámara pre-frío / mural frigorífico / hidroneumático
C_COL_RED    = '#DF0000'   # Columnas estructurales achuradas
C_STEEL_BLK  = '#212121'   # Columnas metálicas estructurales negras Piso 3
C_AXIS_CYAN  = '#0097A7'   # Ejes estructurales y proyecciones cenitales
C_DIM        = '#222222'   # Líneas y textos de cotas

WHITE_HALO = dict(boxstyle='square,pad=0.06', facecolor='white', edgecolor='none', alpha=0.88)


def fmt_m(val):
    """Formatea metros con coma decimal estilo venezolano (ej. 3,00)."""
    return f"{val:.2f}".replace('.', ',')


def draw_sheet_frame(fig, title_line1, title_line2="", escala="1:75", sheet_num="1 / 7", fecha="NOV 2026"):
    """Dibuja el marco doble azul reglamentario y el cajetín fiel a 'planos_nuevo_proyecto.pdf'."""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Doble marco perimetral azul
    ax.add_patch(Rectangle((0.018, 0.014), 0.964, 0.972, fill=False, edgecolor=C_BLUE, lw=2.2))
    ax.add_patch(Rectangle((0.022, 0.018), 0.956, 0.964, fill=False, edgecolor=C_BLUE, lw=0.9))

    # Membrete Institucional Superior Izquierdo
    ax.text(0.030, 0.973, "REPÚBLICA BOLIVARIANA DE VENEZUELA",
            fontsize=13.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')
    ax.text(0.030, 0.955, "MUNICIPIO INDEPENDENCIA YARACUY",
            fontsize=12.0, fontweight='bold', color=C_RED, family='sans-serif', va='top')

    # Identificador de Proyecto Superior Derecho
    ax.text(0.970, 0.972, "PROYECTO AMPLIACIÓN: 3 PISOS CHALET ALPINO & COMERCIO",
            fontsize=8.4, fontweight='bold', color='#263238', family='sans-serif', va='top', ha='right')
    ax.text(0.970, 0.956, f"MODELO MAESTRO VERIFICADO  |  LÁMINA {sheet_num}",
            fontsize=7.8, fontweight='bold', color=C_BLUE, family='sans-serif', va='top', ha='right')

    # Cajetín Inferior Reglamentario
    c_left, c_right = 0.022, 0.978
    c_bot = 0.018
    row_top = 0.058
    caj_top = 0.096

    ax.plot([c_left, c_right], [caj_top, caj_top], color=C_BLUE, lw=1.6)
    ax.plot([c_left, c_right], [row_top, row_top], color=C_BLUE, lw=1.2)

    # Banda de título del plano
    if title_line2:
        ax.text(0.032, caj_top - 0.012, title_line1, fontsize=10.0, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')
        ax.text(0.032, caj_top - 0.028, title_line2, fontsize=7.2, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')
    else:
        ax.text(0.032, (caj_top + row_top) / 2, title_line1, fontsize=10.8, fontweight='bold',
                color=C_RED, ha='left', va='center', family='sans-serif')

    # Subtítulo descriptivo derecho en la banda de título
    ax.text(0.968, caj_top - 0.012,
            "PIEDRA RÚSTICA + MADERA + ACERO NEGRO P3",
            fontsize=6.6, fontweight='bold', color='#37474F', ha='right', va='center')
    ax.text(0.968, caj_top - 0.028,
            "RESPETO ESTRICTO DE LINDEROS (0,00 m INVASIÓN)",
            fontsize=6.2, fontweight='bold', color=C_BLUE, ha='right', va='center')

    # Divisiones verticales de celdas inferiores
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
    ax.text(0.745, row_top - 0.022, "PROYECTO AMPLIACIÓN\n3 PISOS + BODEGA",
            fontsize=6.3, fontweight='bold', color='#1B5E20', ha='center', va='center')

    # 5. FECHA
    ax.text(0.829, row_top - 0.008, "FECHA:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.865, row_top - 0.024, fecha, fontsize=8.0, fontweight='bold', color=C_RED, ha='center')

    # 6. ESCALA
    ax.text(0.909, row_top - 0.008, "ESCALA:", fontsize=6.0, fontweight='bold', color=C_BLUE)
    ax.text(0.942, row_top - 0.024, escala, fontsize=8.2, fontweight='bold', color=C_RED, ha='center')

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
        elif kind == 'high_win':
            draw_high_window_h(ax, ox1, ox2, y1, y2)
        elif kind == 'mampara':
            draw_mampara_h(ax, ox1, ox2, y1, y2)
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
        elif kind == 'high_win':
            draw_high_window_v(ax, x1, x2, oy1, oy2)
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


def draw_high_window_h(ax, x1, x2, y1, y2):
    """Ventana alta / clerestory sobre muro bajo (representación normativa en línea segmentada cian)."""
    ym = 0.5 * (y1 + y2)
    h = abs(y2 - y1)
    ax.add_patch(Rectangle((x1, min(y1, y2)), x2 - x1, h, facecolor='#E8F4F8', edgecolor=C_WALL_EDGE, lw=0.55, linestyle='--', zorder=5))
    ax.plot([x1, x2], [ym, ym], color=C_WINDOW, lw=0.85, linestyle='--', zorder=6)


def draw_mampara_h(ax, x1, x2, y1, y2):
    """Mampara corrediza de terraza en planta (doble riel + 2 hojas traslapadas de cristal templado)."""
    y_lo, y_hi = min(y1, y2), max(y1, y2)
    ym = 0.5 * (y_lo + y_hi)
    w_leaf = 0.52 * (x2 - x1)
    ax.add_patch(Rectangle((x1, y_lo), x2 - x1, y_hi - y_lo, facecolor='#F7FDFF', edgecolor='#4E342E', lw=0.55, zorder=5))
    # Hoja fija exterior y hoja corrediza interior traslapada
    ax.plot([x1 + 0.03, x1 + 0.03 + w_leaf], [ym + 0.028, ym + 0.028], color=C_WINDOW, lw=1.25, zorder=6)
    ax.plot([x1 + 0.22, x1 + 0.22 + w_leaf], [ym - 0.028, ym - 0.028], color='#01579B', lw=1.25, zorder=6)


def draw_window_v(ax, x1, x2, y1, y2, shutters=False):
    xm = 0.5 * (x1 + x2)
    w = abs(x2 - x1)
    ax.add_patch(Rectangle((min(x1, x2), y1), w, y2 - y1, facecolor='#F2FBFF', edgecolor=C_WALL_EDGE, lw=0.55, zorder=5))
    ax.plot([xm - 0.022, xm - 0.022], [y1, y2], color=C_WINDOW, lw=0.75, zorder=6)
    ax.plot([xm + 0.022, xm + 0.022], [y1, y2], color=C_WINDOW, lw=0.75, zorder=6)
    if shutters:
        ax.add_patch(Rectangle((max(x1, x2) + 0.01, y1 - 0.16), 0.04, 0.16, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))
        ax.add_patch(Rectangle((max(x1, x2) + 0.01, y2), 0.04, 0.16, facecolor='#5D4037', edgecolor='black', lw=0.4, zorder=6))


def draw_high_window_v(ax, x1, x2, y1, y2):
    xm = 0.5 * (x1 + x2)
    w = abs(x2 - x1)
    ax.add_patch(Rectangle((min(x1, x2), y1), w, y2 - y1, facecolor='#E8F4F8', edgecolor=C_WALL_EDGE, lw=0.55, linestyle='--', zorder=5))
    ax.plot([xm, xm], [y1, y2], color=C_WINDOW, lw=0.85, linestyle='--', zorder=6)


def draw_door(ax, hx, hy, width, theta_leaf, theta_closed):
    """Puerta abatible (admite apertura a 90° o entreabierta a 45°) con arco de barrido fino."""
    rad = math.radians(theta_leaf)
    lx = hx + width * math.cos(rad)
    ly = hy + width * math.sin(rad)
    ax.plot([hx, lx], [hy, ly], color=C_DOOR, lw=1.30, zorder=6)
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


def draw_col(ax, cx, cy, size=0.25, hatched=False, steel_black=False):
    s2 = 0.5 * size
    if hatched:
        ax.add_patch(Rectangle((cx - s2, cy - s2), size, size, facecolor='#FFEBEE',
                               edgecolor=C_COL_RED, lw=1.0, hatch='////', zorder=8))
    elif steel_black:
        ax.add_patch(Rectangle((cx - s2, cy - s2), size, size, facecolor=C_STEEL_BLK,
                               edgecolor='#000000', lw=0.85, zorder=8))
        ax.plot([cx - s2 + 0.04, cx + s2 - 0.04], [cy, cy], color='#90A4AE', lw=0.55, zorder=9)
    else:
        ax.add_patch(Rectangle((cx - s2, cy - s2), size, size, facecolor='#525252',
                               edgecolor='#111111', lw=0.75, zorder=7))


def draw_stairs_numbered(ax, x1, y1, x2, y2, n_steps, direction='down_y', label_txt='SUBE'):
    """Escalera numerada peldaño a peldaño exactamente como en planos_nuevo_proyecto.pdf."""
    ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor='#FAFAFA', edgecolor='#222222', lw=0.75, zorder=3))
    dy = (y2 - y1) / n_steps
    xm = 0.5 * (x1 + x2)
    for i in range(n_steps + 1):
        yy = y1 + i * dy
        ax.plot([x1, x2], [yy, yy], color='#444444', lw=0.55, zorder=4)
    for i in range(n_steps):
        idx = (i + 1) if direction == 'up_y' else (n_steps - i)
        yc = y1 + (i + 0.5) * dy
        ax.text(x1 + 0.16, yc, str(idx), fontsize=4.5, color='#444444', ha='center', va='center', zorder=5)
    if direction == 'up_y':
        ax.annotate('', xy=(xm + 0.08, y2 - 0.18), xytext=(xm + 0.08, y1 + 0.18),
                    arrowprops=dict(arrowstyle='->', color='#111111', lw=0.9), zorder=6)
    else:
        ax.annotate('', xy=(xm + 0.08, y1 + 0.18), xytext=(xm + 0.08, y2 - 0.18),
                    arrowprops=dict(arrowstyle='->', color='#111111', lw=0.9), zorder=6)
    ax.text(xm + 0.08, 0.5 * (y1 + y2), label_txt, fontsize=5.0, fontweight='bold',
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
    """Dibuja cama arquitectónica en planta con almohadas y sobrecama (west, east o south)."""
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
    elif head == 'south':
        ax.add_patch(Rectangle((x1, y1), w, 0.10, facecolor='#8D6E63', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x1 + 0.14, y1 + 0.14), w * 0.36, 0.34, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.add_patch(Rectangle((x2 - 0.14 - w * 0.36, y1 + 0.14), w * 0.36, 0.34, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
        ax.plot([x1, x2], [y1 + 0.62, y1 + 0.62], color=C_FURN_EDGE, lw=0.5, zorder=4)


def draw_wc(ax, x, y, orientation='east'):
    """Dibuja inodoro arquitectónico en planta."""
    if orientation == 'east':
        ax.add_patch(Rectangle((x, y - 0.20), 0.20, 0.40, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
        ax.add_patch(Circle((x + 0.40, y), 0.19, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    elif orientation == 'north':
        ax.add_patch(Rectangle((x - 0.20, y), 0.40, 0.20, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
        ax.add_patch(Circle((x, y + 0.40), 0.19, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))


# Columnas maestras sincronizadas 100% con build_casa_3_pisos.py
SOT_COLS = [
    (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
    (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
    (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
]

PB_P2_P3_COLS = [
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
# LÁMINA 1/7: PLANTA ARQUITECTÓNICA NIVEL SÓTANO — GRAN BODEGA MAYORISTA
# =============================================================================
def build_sheet_1_sotano(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — NIVEL SÓTANO BODEGA",
                     "GRAN BODEGA MAYORISTA COMERCIAL, CÁMARA PRE-FRÍO Y PATIO DE MANIOBRA (Z = -2,55 m).",
                     escala="1:50", sheet_num="1 / 7")

    ax = fig.add_axes([0.05, 0.25, 0.90, 0.67])
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 11.8)
    ax.set_ylim(-3.8, 9.8)
    ax.axis('off')

    draw_north(ax, 10.8, 8.6, r=0.45)

    # Pared vecino izquierdo intacta (X = 0.00..0.15)
    ax.add_patch(Rectangle((0.00, -3.00), 0.15, 11.30, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 3.0, "PARED VECINO COLINDANTE (INTACTA — 0,00 m INVASIÓN)", rotation=90,
            fontsize=6.5, fontweight='bold', color='#666666', ha='right', va='center')

    # Piso interior de la Bodega + Patio Posterior + Llegada Rampa Derecha
    ax.add_patch(Rectangle((0.30, 0.15), 8.65, 8.00, facecolor='#FCFCFA', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.15, -3.00), 10.65, 3.00, facecolor='#F6F9F4', edgecolor='#999999', lw=0.6, linestyle='--', zorder=1))
    # Losa Patio de Maniobra Sur (X: 4.50..9.15, Y: -2.50..0.00)
    ax.add_patch(Rectangle((4.50, -2.50), 4.65, 2.50, facecolor=C_STONE_SOFT, edgecolor='#546E7A', lw=0.9, zorder=2))
    ax.text(6.85, -2.15, "PATIO DE MANIOBRA Y CARGA (4,65 x 2,50 m — Z = -2,55 m)",
            fontsize=6.4, fontweight='bold', color='#263238', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Corredor y llegada de Rampa Logística Derecha desde Av. 4 (X: 9.15..10.75)
    ax.add_patch(Rectangle((9.15, 0.00), 1.60, 5.50, facecolor=C_STONE_SOFT, edgecolor='#546E7A', lw=0.75, zorder=2))
    ax.add_patch(Rectangle((9.15, 5.50), 1.60, 2.80, facecolor='#ECEFF1', edgecolor='#546E7A', lw=0.75, hatch='---', zorder=2))
    ax.annotate('', xy=(9.95, 5.10), xytext=(9.95, 8.15),
                arrowprops=dict(arrowstyle='->', color='#1B5E20', lw=1.3), zorder=6)
    ax.text(9.95, 6.95, "BAJA RAMPA\nDESDE AV. 4\n(Pend. 18%)", fontsize=5.5, fontweight='bold',
            color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)
    ax.text(9.95, 2.60, "CORREDOR PLANO DE CARGA (Z = -2,55 m)", rotation=90,
            fontsize=5.8, fontweight='bold', color='#37474F', ha='center', va='center')

    # Muros Perimetrales del Sótano Bodega
    draw_wall(ax, 0.15, 0.00, 0.30, 8.30)  # Oeste propio ciego
    draw_wall(ax, 0.15, 8.15, 9.15, 8.30)  # Muro Norte de Contención
    draw_wall_x_openings(ax, 0.30, 9.15, 0.00, 0.15, [
        (0.75, 2.35, 'high_win'),
        (3.25, 4.30, 'high_win'),
        (4.85, 5.75, 'high_win'),
        (6.35, 8.55, 'door_gap'),
    ])
    # Portón Doble Metálico de Carga (6.35..8.55 = 2,20 m, hojas abiertas 90° hacia Patio de Maniobra)
    draw_double_door_h(ax, 6.35, 8.55, 0.00, open_up=False)
    ax.text(7.45, -1.25, "PORTÓN DOBLE DE CARGA\n(2,20 x 2,10 m)", fontsize=5.8, fontweight='bold',
            color=C_DOOR, ha='center', va='center', bbox=WHITE_HALO, zorder=8)

    draw_wall_y_openings(ax, 8.95, 9.15, 0.15, 8.30, [
        (1.00, 2.65, 'high_win'),
        (4.20, 5.85, 'high_win'),
        (6.95, 8.00, 'high_win'),
    ])

    # 1. Esclusa Cerrada de Escalera (X: 0.30..1.55, Y: 3.40..8.15) con Puerta Metálica a 45° hacia Pasillo Libre
    draw_wall(ax, 0.30, 3.40, 1.55, 3.55)
    draw_wall_y_openings(ax, 1.40, 1.55, 3.55, 8.15, [
        (3.70, 4.55, 'door_gap'),
        (7.20, 7.95, 'door_gap'),
    ])
    draw_door(ax, 1.55, 4.55, 0.85, 315, 270)  # Hoja metálica abierta a 45° hacia pasillo despejado!
    draw_door(ax, 1.55, 7.95, 0.75, 0, 270)    # Cuarto útiles bajo escalera
    draw_stairs_numbered(ax, 0.30, 4.45, 1.40, 7.40, 12, direction='up_y', label_txt='SUBE P.B.')
    ax.text(0.85, 7.75, "Útiles\nBajo Esc.", fontsize=5.2, fontweight='bold', ha='center', va='center')

    # 2. Baño Operativo Compacto + Lava-mopas (X: 2.80..4.70, Y: 0.15..2.70)
    draw_wall(ax, 2.80, 0.15, 2.95, 2.55)
    draw_wall(ax, 4.55, 0.15, 4.70, 2.55)
    draw_wall_x_openings(ax, 2.80, 4.70, 2.55, 2.70, [(3.40, 4.18, 'door_gap')])
    draw_door(ax, 4.18, 2.55, 0.78, 270, 180)
    draw_wc(ax, 3.02, 0.48, orientation='east')
    ax.add_patch(Rectangle((3.02, 1.25), 0.43, 0.60, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Circle((3.24, 1.55), 0.14, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
    ax.add_patch(Rectangle((3.95, 0.25), 0.55, 0.60, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(3.85, 1.45, "Baño Personal\n+ Lava-mopas\n(1,60 x 2,40 m)", fontsize=5.5, fontweight='bold', ha='center', va='center', zorder=6)

    # 3. Cámara Isotérmica de Pre-Frío y Maduración Mayorista (X: 1.60..5.55, Y: 5.55..8.10 = 10,1 m²)
    ax.add_patch(Rectangle((1.60, 5.55), 3.95, 2.55, facecolor=C_COLD_SOFT, edgecolor='#0277BD', lw=1.0, zorder=3))
    ax.add_patch(Rectangle((1.70, 7.45), 3.65, 0.57, facecolor='#B3E5FC', edgecolor='#01579B', lw=0.65, hatch='---', zorder=4))
    ax.plot([3.10, 4.25], [5.52, 5.52], color='#0D47A1', lw=2.2, zorder=6)  # Puerta corrediza inox
    ax.text(3.98, 6.52, "CÁMARA ISOTÉRMICA DE PRE-FRÍO\nY MADURACIÓN MAYORISTA\n(3,95 x 2,55 m = 10,07 m²)",
            fontsize=5.9, fontweight='bold', color='#01579B', ha='center', va='center', bbox=WHITE_HALO, zorder=9)

    # 4. Baterías Perimetrales de Racks Pesados (dejando libre la Cruz de Circulación!)
    racks_sot = [
        (5.85, 7.35, 3.00, 0.70, "RACK NORTE MAYORISTA", 0),
        (8.25, 4.05, 0.65, 2.75, "RACK ESTE 1", 90),
        (8.25, 0.85, 0.65, 2.50, "RACK ESTE 2", 90),
        (0.35, 0.22, 2.30, 0.66, "RACK SUR", 0),
        (0.35, 1.05, 0.65, 2.20, "RACK OESTE", 90),
    ]
    for rx, ry, rw, rh, rlbl, rrot in racks_sot:
        ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=C_WOOD_SOFT, edgecolor='#5D4037', lw=0.75, hatch='xx', zorder=3))
        ax.text(rx + 0.5 * rw, ry + 0.5 * rh, rlbl, rotation=rrot, fontsize=5.3, fontweight='bold',
                color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Estiba + Báscula Plataforma 500 kg + Mesa Control adosadas al baño (sin obstruir el portón!)
    ax.add_patch(Rectangle((1.95, 1.15), 0.77, 0.80, facecolor='#FFE0B2', edgecolor='#8D6E63', lw=0.65, zorder=3))
    ax.text(2.33, 1.55, "Pallet", fontsize=5.0, fontweight='bold', color='#4E342E', ha='center', va='center')

    ax.add_patch(Rectangle((4.80, 0.35), 0.90, 0.90, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.85, zorder=4))
    ax.text(5.25, 0.80, "BÁSCULA\n500 kg", fontsize=5.2, fontweight='bold', color='#1B5E20', ha='center', va='center')

    ax.add_patch(Rectangle((4.75, 1.45), 0.95, 1.05, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    ax.add_patch(Circle((5.24, 2.76), 0.18, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(5.22, 1.98, "Control\nGuías", fontsize=5.2, fontweight='bold', color='#3E2723', ha='center', va='center')

    # Flechas de Circulación Despejada (Pasillo Central 1,95 m + Avenida de Carga 2,25 m)
    ax.plot([2.25, 7.15], [4.55, 4.55], color='#2E7D32', lw=1.0, linestyle='--', zorder=4)
    ax.plot([7.15, 7.15], [0.25, 7.05], color='#2E7D32', lw=1.0, linestyle='--', zorder=4)
    ax.text(4.35, 4.55, "PASILLO CENTRAL DESPEJADO (1,95 m LIBRES)", fontsize=6.1, fontweight='bold',
            color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)
    ax.text(7.12, 3.30, "AVENIDA RECTA DE CARGA\n(2,25 m LIBRES)", rotation=90, fontsize=6.1, fontweight='bold',
            color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Columnas Sótano (35 x 35 cm)
    ax.add_patch(Rectangle((0.15, 6.35), 0.15, 0.45, facecolor='#444444', edgecolor='black', lw=0.7, zorder=7))
    for cx, cy in SOT_COLS:
        draw_col(ax, cx, cy, size=0.35, hatched=False)

    # Cotas Exteriores e Interiores
    draw_dim_h(ax, 0.30, 2.825, 8.75, "2,53", y_ref=8.30)
    draw_dim_h(ax, 2.825, 5.925, 8.75, "3,10", y_ref=8.30)
    draw_dim_h(ax, 5.925, 8.95, 8.75, "3,03", y_ref=8.30)
    draw_dim_h(ax, 0.15, 9.15, 9.30, "9,00 (Ancho Propio Bodega)", y_ref=8.30)
    draw_dim_h(ax, 6.00, 8.25, 2.15, "2,25")
    draw_dim_v(ax, 2.55, 3.55, 5.50, "1,95")

    draw_dim_v(ax, -0.55, 0.00, 3.55, "3,55", x_ref=0.15)
    draw_dim_v(ax, -0.55, 3.55, 8.30, "4,75", x_ref=0.15)
    draw_dim_v(ax, -1.15, 0.00, 8.30, "8,30 (Bodega)", x_ref=0.15)
    draw_dim_v(ax, -1.15, -3.00, 0.00, "3,00 (Patio)", x_ref=0.15)

    ax.text(4.85, -3.32, "PLANTA NIVEL SÓTANO — GRAN BODEGA MAYORISTA (COTA N.P.T. = -2,55 m)",
            fontsize=10.2, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.10, 8.60], [-3.60, -3.60], color='#111111', lw=1.2)

    # Cuadro Resumen Técnico Inferior del Sótano
    ax_info = fig.add_axes([0.05, 0.115, 0.90, 0.115])
    ax_info.axis('off')
    ax_info.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.0))
    ax_info.text(0.02, 0.80, "PROGRAMA LOGÍSTICO Y FUNCIONAL — GRAN BODEGA MAYORISTA EN SÓTANO (74,70 m²):",
                 fontsize=8.2, fontweight='bold', color=C_RED)
    items_sot = [
        "• Acceso Logístico Independiente: Rampa lateral derecha desde Portón exclusivo en Av. 4 hasta Patio de Maniobra Sur (Z = -2,55 m) y Portón Doble (2,20 m).",
        "• Circulación Ergonómica Despejada: Esclusa cerrada de escalera con puerta metálica a 45° hacia pasillo libre de 1,95 m + Avenida de Carga recta de 2,25 m.",
        "• Cadena de Frío y Almacenaje: Cámara Isotérmica de Pre-Frío y Maduración (10,07 m²) + 5 baterías perimetrales de racks pesados de alta rotación.",
        "• Control y Servicios: Báscula industrial a ras de piso (500 kg) + Mesa de recepción/guías + Baño operativo de personal con lava-mopas.",
    ]
    for idx, line in enumerate(items_sot):
        ax_info.text(0.02, 0.58 - idx * 0.16, line, fontsize=6.9, color='#222222')

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 2/7: PLANTA BAJA — FRUTERÍA AMPLIADA, JUGOS, OFICINA, GARAJE Y RAMPA
# =============================================================================
def build_sheet_2_planta_baja(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — PLANTA BAJA",
                     "FRUTERÍA AMPLIADA (~112 m²) + BARRA DE JUGOS + OFICINA + GARAJE Y RAMPA BODEGA.",
                     escala="1:75", sheet_num="2 / 7")

    ax = fig.add_axes([0.035, 0.115, 0.645, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.9, 12.1)
    ax.set_ylim(-1.8, 24.4)
    ax.axis('off')

    draw_north(ax, 11.1, 23.1, r=0.50)

    # Pared vecino izquierdo intacta (X = 0.00..0.15)
    ax.add_patch(Rectangle((0.00, 0.00), 0.15, 21.71, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 11.0, "PARED DEL VECINO (INTACTA)", rotation=90, fontsize=6.5, fontweight='bold', color='#666666', ha='right', va='center')

    # Pisos zonificados sutiles
    ax.add_patch(Rectangle((0.30, 8.95), 3.00, 12.61, facecolor='#F7F8F9', edgecolor='none', zorder=1))  # Garaje
    ax.add_patch(Rectangle((2.90, 0.15), 6.10, 21.41, facecolor='#FFFDF9', edgecolor='none', zorder=1))  # Salón Frutería ampliado
    ax.add_patch(Rectangle((0.30, 0.15), 2.45, 3.35, facecolor='#F4F6F7', edgecolor='none', zorder=1))   # Núcleo Baños Suroeste
    ax.add_patch(Rectangle((5.88, 0.15), 3.12, 3.40, facecolor='#F5F8FA', edgecolor='none', zorder=1))   # Oficina Acristalada

    # Corredor y Rampa Logística Derecha hacia Bodega Sótano (X: 9.15..11.22, Y: 0.00..21.71)
    ax.add_patch(Rectangle((9.15, 19.50), 2.05, 2.21, facecolor=C_STONE_SOFT, edgecolor='#607D8B', lw=0.7, zorder=1))
    ax.add_patch(Rectangle((9.15, 5.50), 1.90, 14.00, facecolor='#ECEFF1', edgecolor='#607D8B', lw=0.7, hatch='---', zorder=1))
    ax.add_patch(Rectangle((9.15, 0.00), 1.75, 5.50, facecolor='#E8F5E9', edgecolor='#607D8B', lw=0.7, zorder=1))
    ax.annotate('', xy=(10.10, 6.20), xytext=(10.10, 19.10),
                arrowprops=dict(arrowstyle='->', color='#1B5E20', lw=1.2), zorder=5)
    ax.text(10.12, 12.60, "RAMPA EXCLUSIVA A BODEGA SÓTANO (Pend. 18%)", rotation=90,
            fontsize=5.6, fontweight='bold', color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # 1. Muros Exteriores Planta Baja + Pórtico Derecho Bodega en Av. 4 (X: 9.15..11.37)
    draw_wall(ax, 0.15, 0.00, 0.30, 21.71)
    draw_wall(ax, 0.15, 21.56, 0.40, 21.71)
    draw_wall(ax, 2.70, 21.56, 3.65, 21.71)
    draw_wall(ax, 5.75, 21.56, 6.20, 21.71)
    draw_wall(ax, 8.80, 21.56, 9.35, 21.71)
    draw_wall(ax, 11.12, 21.56, 11.37, 21.71)
    # Puerta doble metálica comercial derecha hacia Rampa Bodega (X: 9.35..11.12 = 1,77 m)
    draw_double_door_h(ax, 9.35, 11.12, 21.56, open_up=False)
    ax.text(10.25, 21.82, "PORTÓN BODEGA\n(1,77 m)", fontsize=5.3, fontweight='bold', color='#1B5E20', ha='center', va='bottom')

    # Muro Este con sus 7 ventanas reales
    draw_wall_y_openings(ax, 9.00, 9.15, 0.00, 21.71, [
        (1.10, 2.50, 'win'), (4.10, 5.00, 'win'), (6.30, 8.00, 'win'),
        (9.65, 11.85, 'win'), (13.15, 14.05, 'win'), (15.50, 17.70, 'win'), (18.80, 21.00, 'win'),
    ])
    # Muro Sur Posterior redistribuido (Ventana alta Baños + Gran Ventanal Barra Jugos + Ventanal Oficina)
    draw_wall_x_openings(ax, 0.15, 9.15, 0.00, 0.15, [
        (0.75, 2.35, 'high_win'),
        (3.35, 5.45, 'shutter_win'),
        (6.85, 8.45, 'shutter_win'),
    ])

    # 2. Muros Interiores: Esclusa Residencial de Escaleras + Cuarto Aseo + Núcleo Baños Suroeste
    draw_wall_y_openings(ax, 2.75, 2.90, 0.15, 8.80, [
        (2.35, 3.20, 'door_gap'),  # Entrada Antebaño Comercial
        (3.75, 4.45, 'door_gap'),  # Cuarto Aseo bajo escalera P2
    ])
    draw_door(ax, 2.75, 3.20, 0.80, 180, 270)
    draw_door(ax, 2.75, 4.45, 0.68, 180, 270)

    draw_wall(ax, 3.30, 8.80, 3.45, 21.56)    # Divisoria estacionamiento / frutería
    draw_wall(ax, 2.75, 8.80, 3.45, 8.95)
    # Cierre del Vestíbulo de Escaleras (Y: 8.80..8.95) con Puerta Residencial (1.60..2.55)
    draw_wall_x_openings(ax, 0.30, 2.75, 8.80, 8.95, [(1.60, 2.55, 'door_gap')])
    draw_door(ax, 2.55, 8.80, 0.90, 270, 180)
    # Muro entre escaleras + Puerta Metálica de Seguridad en arranque a Bodega (0.40..1.32 en Y=7.35..7.50)
    draw_wall(ax, 1.40, 4.40, 1.55, 7.50)
    draw_wall_x_openings(ax, 0.30, 1.55, 7.35, 7.50, [(0.40, 1.32, 'door_gap')])
    draw_door(ax, 0.40, 7.50, 0.88, 90, 0)
    draw_wall(ax, 0.30, 4.25, 1.40, 4.40)
    draw_wall(ax, 1.55, 5.65, 2.75, 5.78)

    # Núcleo de Baños Comerciales Suroeste (X: 0.30..2.75, Y: 0.15..3.50 = 8,20 m²)
    draw_wall(ax, 0.30, 3.50, 2.75, 3.62)
    draw_wall_y_openings(ax, 1.48, 1.58, 0.15, 3.50, [(2.15, 2.95, 'door_gap')])
    draw_door(ax, 1.48, 2.95, 0.76, 180, 270)  # Cabina Damas / PMR
    draw_wall_x_openings(ax, 1.58, 2.75, 1.72, 1.82, [(1.75, 2.48, 'door_gap')])
    draw_door(ax, 2.48, 1.72, 0.72, 270, 180)  # Cabina Caballeros
    ax.add_patch(Rectangle((1.62, 3.02), 1.06, 0.46, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Circle((1.90, 3.25), 0.13, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
    ax.add_patch(Circle((2.40, 3.25), 0.13, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
    draw_wc(ax, 0.42, 0.52, orientation='east')
    draw_wc(ax, 2.02, 0.25, orientation='north')
    ax.add_patch(Rectangle((2.44, 0.95), 0.26, 0.38, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(0.90, 1.55, "Baño\nDamas\n(PMR)", fontsize=5.1, fontweight='bold', ha='center', va='center')
    ax.text(2.12, 1.15, "Cab.", fontsize=5.0, fontweight='bold', ha='center', va='center')
    ax.text(2.15, 4.95, "Aseo", fontsize=4.8, fontweight='bold', ha='center', va='center')

    # 3. Portón Corredizo-Articulado Completo sobre Riel Curvo 90° + 2 Santamarías de Caracol Completas
    ax.plot([0.40, 3.02], [21.48, 21.48], color='#212121', lw=1.3, linestyle='--', zorder=6)
    ax.add_patch(Arc((3.02, 21.28), 0.40, 0.40, angle=0, theta1=0, theta2=90, color='#212121', lw=1.3, zorder=6))
    ax.plot([3.22, 3.22], [18.92, 21.28], color='#212121', lw=1.3, linestyle='--', zorder=6)
    # Hoja guía delantera asomando en X=2.36..2.94 + 4 hojas articuladas en bolsillo derecho X=3.16..3.26
    ax.add_patch(Rectangle((2.36, 21.37), 0.58, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.65, zorder=7))
    for gy1, gy2 in [(19.00, 19.56), (19.59, 20.15), (20.18, 20.74), (20.77, 21.33)]:
        ax.add_patch(Rectangle((3.15, gy1), 0.12, gy2 - gy1, facecolor='#8D6E63', edgecolor='black', lw=0.6, zorder=7))
    ax.text(1.50, 21.82, "PORTÓN CORREDIZO\nRIEL 90° (2,30 m)", fontsize=5.3, fontweight='bold', color='#3E2723', ha='center', va='bottom')

    for sx1, sx2, lbl_s in [(3.65, 5.75, "SANTAMARÍA CARACOL 1\n(2,10 m)"), (6.20, 8.80, "SANTAMARÍA CARACOL 2\n(2,60 m)")]:
        ax.add_patch(Rectangle((sx1, 21.30), sx2 - sx1, 0.34, facecolor='#CFD8DC', edgecolor='#263238', lw=0.85, hatch='---', zorder=6))
        ax.add_patch(Rectangle((sx1, 21.56), 0.08, 0.14, facecolor='#212121', edgecolor='black', lw=0.5, zorder=7))
        ax.add_patch(Rectangle((sx2 - 0.08, 21.56), 0.08, 0.14, facecolor='#212121', edgecolor='black', lw=0.5, zorder=7))
        ax.text(0.5 * (sx1 + sx2), 21.82, lbl_s, fontsize=5.2, fontweight='bold', color='#0D47A1', ha='center', va='bottom')

    # 4. Estacionamiento 2 Plazas + Escaleras Numeradas con Esclusa
    for py1, py2, v_lbl in [(15.20, 20.60, "PLAZA VEHICULAR 1\n(Piso Plano)"),
                            (9.20,  14.60, "PLAZA VEHICULAR 2\n(Acceso Residencial)")]:
        ax.add_patch(Rectangle((0.55, py1), 2.10, py2 - py1, facecolor='#ECEFF1', edgecolor='#607D8B', lw=0.8, linestyle='--', zorder=2))
        ax.text(1.60, 0.5 * (py1 + py2), v_lbl, fontsize=5.8, fontweight='bold', color='#37474F', ha='center', va='center', zorder=4)

    ax.text(1.52, 8.15, "Vestíbulo\nResidencial", fontsize=5.2, fontweight='bold', color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)
    draw_stairs_numbered(ax, 0.30, 4.45, 1.40, 7.40, 12, direction='down_y', label_txt='BAJA SOT.')
    draw_stairs_numbered(ax, 1.55, 4.40, 2.65, 7.35, 14, direction='down_y', label_txt='SUBE P.2')

    # 5. Salón Comercial Ampliado (~112 m²): Caja + 5 Islas Centrales + Mural Frigorífico + Estantes
    ax.add_patch(Rectangle((7.05, 18.25), 1.70, 0.72, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    ax.add_patch(Rectangle((7.05, 17.05), 0.68, 1.20, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    ax.text(7.92, 19.15, "CAJA Y PESAJE\n(2 Balanzas + TPV)", fontsize=5.6, fontweight='bold', color='#3E2723', ha='center', va='bottom', zorder=7)

    islas = [
        (5.15, 6.30, 17.95, 19.20, "Isla Frutas 1"),
        (5.15, 6.70, 15.55, 17.10, "Isla Frutas 2"),
        (5.15, 6.70, 11.25, 12.80, "Isla Frutas 3"),
        (5.15, 6.70,  8.10,  9.65, "Isla Frutas 4"),
        (5.15, 6.70,  5.30,  6.85, "Isla 5 Orgánicos"),
    ]
    for ix1, ix2, iy1, iy2, ilbl in islas:
        ax.add_patch(Rectangle((ix1, iy1), ix2 - ix1, iy2 - iy1, facecolor='#FFE0B2', edgecolor='#8D6E63', lw=0.75, zorder=3))
        ax.add_patch(Rectangle((ix1 + 0.22, iy1 + 0.22), (ix2 - ix1) - 0.44, (iy2 - iy1) - 0.44,
                               facecolor='#FFF3E0', edgecolor='#A1887F', lw=0.55, zorder=4))
        ax.text(0.5 * (ix1 + ix2), iy1 - 0.14, ilbl, fontsize=5.2, fontweight='bold', color='#4E342E', ha='center', va='top', zorder=6)

    ax.add_patch(Rectangle((3.46, 9.00), 0.59, 11.60, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.7, hatch='---', zorder=3))
    ax.text(3.75, 14.80, "ESTANTES MURALES DE FRUTAS (ROBLE)", rotation=90, fontsize=5.6, fontweight='bold',
            color='#4E342E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)
    ax.add_patch(Rectangle((2.91, 4.65), 0.59, 4.05, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.7, hatch='---', zorder=3))
    ax.text(3.20, 6.65, "CÍTRICOS", rotation=90, fontsize=5.2, fontweight='bold', color='#4E342E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((8.35, 7.80), 0.63, 8.70, facecolor=C_GREEN_SOFT, edgecolor='#2E7D32', lw=0.7, hatch='---', zorder=3))
    ax.text(8.66, 12.15, "ESTANTES HORTALIZAS FRESCAS", rotation=90, fontsize=5.5, fontweight='bold',
            color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Mural Frigorífico Abierto (X: 8.26..8.98, Y: 5.10..7.55)
    ax.add_patch(Rectangle((8.26, 5.10), 0.72, 2.45, facecolor=C_COLD_SOFT, edgecolor='#0277BD', lw=0.85, zorder=4))
    ax.text(8.62, 6.32, "MURAL FRÍO\nLÁCTEOS", rotation=90, fontsize=5.1, fontweight='bold', color='#01579B', ha='center', va='center', zorder=6)

    ax.text(5.95, 13.85, "SALÓN FRUTERÍA AMPLIADO\n(~112,00 m² — SIN BODEGA EN P.B.)\n5 Islas Centrales + Brisa Norte-Sur",
            fontsize=6.9, fontweight='bold', color='#111111', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # 6. Barra Gourmet de Jugos Naturales y Café (Centro Sur: X: 3.05..5.80, Y: 0.18..4.00)
    ax.add_patch(Rectangle((3.55, 2.78), 2.25, 0.78, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    ax.add_patch(Rectangle((4.65, 2.85), 1.07, 0.63, facecolor=C_COLD_SOFT, edgecolor='#0277BD', lw=0.6, zorder=5))
    for bs_x in [3.75, 4.28, 4.81, 5.34]:
        ax.add_patch(Circle((bs_x, 3.84), 0.15, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.add_patch(Rectangle((3.05, 0.18), 2.70, 0.65, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.text(4.42, 1.75, "Barra Gourmet\nJugos y Café", fontsize=5.8, fontweight='bold', color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # 7. Oficina Acristalada de Administración Sureste (X: 5.88..9.00, Y: 0.15..3.58 = 10,05 m²)
    ax.add_patch(Rectangle((5.88, 3.48), 0.27, 0.09, facecolor='#263238', edgecolor='black', lw=0.6, zorder=5))
    ax.add_patch(Rectangle((7.02, 3.48), 1.98, 0.09, facecolor='#B0BEC5', edgecolor='#263238', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((5.88, 0.15), 0.09, 3.33, facecolor='#B0BEC5', edgecolor='#263238', lw=0.7, zorder=5))
    draw_door(ax, 7.02, 3.48, 0.85, 270, 180)
    ax.add_patch(Rectangle((7.25, 1.45), 1.40, 0.70, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((8.05, 0.85), 0.60, 0.60, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((6.15, 0.20), 1.40, 0.45, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.98, 2.78, "Oficina Admin.\nAcristalada\n(10,05 m²)", fontsize=5.4, fontweight='bold', color='#1A237E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Columnas Planta Baja (32 columnas 25x25 cm)
    for cx, cy in PB_P2_P3_COLS:
        draw_col(ax, cx, cy, size=0.25, hatched=False)

    # Cotas Exteriores e Interiores
    draw_dim_h(ax, 0.30, 3.30, 22.85, "3,00 (Garaje)", y_ref=21.71)
    draw_dim_h(ax, 3.45, 9.00, 22.85, "5,55 (Frutería)", y_ref=21.71)
    draw_dim_h(ax, 9.15, 11.37, 22.85, "2,22 (Rampa)", y_ref=21.71)
    draw_dim_h(ax, 0.15, 9.15, 23.65, "9,00 (Cuerpo Edificación)", y_ref=21.71)
    draw_dim_h(ax, 0.30, 2.75, -0.55, "2,45", y_ref=0.00)
    draw_dim_h(ax, 2.90, 5.88, -0.55, "2,98", y_ref=0.00)
    draw_dim_h(ax, 5.88, 9.00, -0.55, "3,12", y_ref=0.00)

    draw_dim_v(ax, -0.65, 0.00, 3.55, "3,55", x_ref=0.15)
    draw_dim_v(ax, -0.65, 8.95, 21.56, "12,61 (Garaje)", x_ref=0.15)
    draw_dim_v(ax, -1.35, 0.00, 21.71, "21,71", x_ref=0.15)

    ax.text(5.10, -1.15, "PLANTA BAJA — COMERCIO AMPLIADO, GARAJE Y RAMPA BODEGA (N.P.T. ±0,00 m)",
            fontsize=9.4, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.00, 9.20], [-1.45, -1.45], color='#111111', lw=1.2)

    # Panel Derecho: Cuadro Técnico de Ambientes de Planta Baja
    ax_side = fig.add_axes([0.69, 0.125, 0.28, 0.79])
    ax_side.axis('off')
    ax_side.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))

    ax_side.text(0.50, 0.965, "CUADRO DE AMBIENTES\nPLANTA BAJA (195,39 m²)",
                 fontsize=8.8, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_side.plot([0.06, 0.94], [0.915, 0.915], color=C_BLUE, lw=0.9)

    zones_pb = [
        ("1. SALÓN FRUTERÍA AMPLIADO", "~112,0 m²",
         "• Eliminada antigua bodega trasera (trasladada\n  al Sótano) ganando amplitud comercial.\n"
         "• 2 Santamarías de Caracol completas en Av. 4\n  (carriles U, tambor espiral y faldón).\n"
         "• 5 Islas centrales + Mural Frío de Lácteos."),
        ("2. BARRA JUGOS Y CAFÉ SUR", "10,60 m²",
         "• Atención con vitrina fría y 4 taburetes.\n"
         "• Gran ventanal Sur para luz y brisa N-S."),
        ("3. OFICINA ADMIN. ACRISTALADA", "10,05 m²",
         "• Cerramiento en hierro negro y cristal con\n  control visual completo de la tienda."),
        ("4. NÚCLEO BAÑOS SUROESTE", "8,20 m²",
         "• Antebaño doble + Cabinas Damas (PMR) y\n  Caballeros bajo columna húmeda de P2."),
        ("5. GARAJE Y ESCLUSA ESCALERA", "44,50 m²",
         "• Portón corredizo-articulado sobre riel a 90°\n  (4 hojas en bolsillo + hoja guía visible).\n"
         "• Vestíbulo cerrado con puerta residencial a\n  P2 y puerta de seguridad a Sótano."),
        ("6. PORTÓN Y RAMPA BODEGA", "Retiro Der.",
         "• Puerta doble en Av. 4 (1,77 m) exclusiva\n  hacia rampa continua (18%) al Sótano."),
    ]
    y_cursor = 0.895
    for z_title, z_area, z_desc in zones_pb:
        ax_side.text(0.06, y_cursor, z_title, fontsize=6.9, fontweight='bold', color='#1A237E', va='top')
        ax_side.text(0.94, y_cursor, z_area, fontsize=6.9, fontweight='bold', color=C_RED, ha='right', va='top')
        y_cursor -= 0.021
        ax_side.text(0.06, y_cursor, z_desc, fontsize=6.0, color='#263238', va='top', linespacing=1.28)
        n_lines = z_desc.count('\n') + 1
        y_cursor -= (n_lines * 0.022 + 0.020)
        ax_side.plot([0.06, 0.94], [y_cursor + 0.008, y_cursor + 0.008], color='#CFD8DC', lw=0.6)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 3/7: SEGUNDO PISO SOCIAL BIOCLIMÁTICO, MAMPARAS Y DESPENSA BAJO ESC.
# =============================================================================
def build_sheet_3_segundo_piso(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — SEGUNDO PISO SOCIAL",
                     "PLANTA DE DÍA: BALCONADA CON MAMPARAS, SALA, ESTUDIO, COCINA CON ISLA Y HAB. 4 (Z = +3,00 m).",
                     escala="1:75", sheet_num="3 / 7")

    ax = fig.add_axes([0.035, 0.115, 0.645, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.9, 10.9)
    ax.set_ylim(-1.8, 24.4)
    ax.axis('off')

    draw_north(ax, 9.9, 23.1, r=0.50)

    # Pared vecino izquierdo intacta + proyección alero derecho (X = 10.10 m)
    ax.add_patch(Rectangle((0.00, 0.00), 0.15, 21.71, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 11.0, "PARED VECINO (0,00 m INVASIÓN)", rotation=90, fontsize=6.4, fontweight='bold', color='#666666', ha='right', va='center')
    ax.plot([10.10, 10.10], [-1.00, 21.71], color='#8D6E63', lw=0.85, linestyle='--', zorder=2)
    ax.text(10.22, 11.0, "PROYECCIÓN ALERO CUBIERTA P3 (0,95 m)", rotation=90, fontsize=5.6, color='#6D4C41', ha='left', va='center')

    # Pisos interiores y Gran Balconada Social Continua (8,70 x 1,96 m = 17,05 m²)
    ax.add_patch(Rectangle((0.30, 0.15), 8.70, 19.30, facecolor='#FFFDF9', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.30, 19.60), 8.70, 1.96, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.8, zorder=2))
    # Barandas Alpinas en Avenida 4 y costado derecho
    ax.add_patch(Rectangle((0.30, 21.52), 8.77, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((9.03, 19.60), 0.10, 2.04, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))

    # Muro Oeste Propio Ciego en Piso 2
    draw_wall(ax, 0.15, 0.00, 0.30, 21.71, facecolor='#6D4C41')

    # Muro Frontal Retranqueado (Y: 19.45..19.60) con las 3 MAMPARAS CORREDIZAS DE TERRAZA COMPLETAS
    draw_wall_x_openings(ax, 0.30, 9.00, 19.45, 19.60, [
        (0.65, 2.55, 'mampara'),
        (3.15, 5.55, 'mampara'),
        (6.25, 8.65, 'mampara'),
    ], facecolor='#6D4C41')

    # Fachada Este P2 abierta a vientos alisios (5 grandes ventanales)
    draw_wall_y_openings(ax, 9.00, 9.15, 0.00, 19.60, [
        (1.10,  3.05, 'shutter_win'),
        (5.15,  6.35, 'win'),
        (8.45, 11.35, 'shutter_win'),
        (12.35, 14.75, 'shutter_win'),
        (16.00, 18.60, 'shutter_win'),
    ], facecolor='#6D4C41')

    # Fachada Sur P2 (Lavandería + Mirador Sur + Habitación 4)
    draw_wall_x_openings(ax, 0.15, 9.15, 0.00, 0.15, [
        (0.75, 2.35, 'win'),
        (3.30, 5.45, 'shutter_win'),
        (6.60, 8.45, 'shutter_win'),
    ], facecolor='#6D4C41')

    # 1. Tabique Industrial Acristalado del Estudio / Home Office (Hierro negro + Cristal corredizo)
    ax.add_patch(Rectangle((5.88, 15.14), 0.08, 4.31, facecolor='#B0BEC5', edgecolor='#212121', lw=0.8, zorder=5))
    ax.add_patch(Rectangle((5.88, 15.14), 1.55, 0.08, facecolor='#E1F5FE', edgecolor='#212121', lw=0.65, linestyle='--', zorder=5))
    ax.add_patch(Rectangle((7.45, 15.14), 1.55, 0.08, facecolor='#B0BEC5', edgecolor='#212121', lw=0.8, zorder=5))

    # 2. Bloque Sureste: Baño Social Completo (Y: 4.45..7.35) + Habitación 4 Huéspedes (Y: 0.15..4.30)
    draw_wall_y_openings(ax, 5.85, 6.00, 0.15, 7.45, [
        (2.55, 3.40, 'door_gap'),
        (5.25, 6.05, 'door_gap'),
    ])
    draw_door(ax, 6.00, 3.40, 0.82, 0, 270)   # Habitación 4 Huéspedes
    draw_door(ax, 6.00, 6.05, 0.78, 0, 270)   # Baño Social Completo
    draw_wall(ax, 6.00, 7.35, 9.00, 7.50)
    draw_wall(ax, 6.00, 4.30, 9.00, 4.45)

    # 3. Núcleo de Escaleras Apiladas + NUEVA DESPENSA WALK-IN BAJO ESCALERA A PISO 3 (X: 0.30..1.52, Y: 5.45..7.40)
    draw_stairs_numbered(ax, 1.55, 4.40, 2.65, 7.35, 14, direction='down_y', label_txt='BAJA P.B.')
    draw_stairs_numbered(ax, 0.30, 4.40, 1.45, 7.40, 14, direction='up_y',   label_txt='SUBE P.3')
    # Tabique bajo zanca y puerta Norte de la Despensa Walk-In bajo el tramo alto de la escalera a P3
    ax.add_patch(Rectangle((0.32, 5.48), 1.12, 1.88, facecolor='#FFF8E1', edgecolor='#8D6E63', lw=0.8, linestyle='--', zorder=4))
    draw_wall_x_openings(ax, 0.30, 1.52, 7.34, 7.43, [(0.44, 1.29, 'door_gap')])
    draw_door(ax, 0.44, 7.43, 0.82, 90, 0)
    ax.plot([1.48, 1.48], [4.45, 7.40], color='#5D4037', lw=1.3, zorder=6)
    ax.plot([2.72, 2.72], [4.65, 7.35], color='#6D4C41', lw=1.3, zorder=6)
    ax.plot([1.55, 2.72], [7.38, 7.38], color='#6D4C41', lw=1.3, zorder=6)
    ax.text(0.88, 6.45, "Despensa\nBajo Esc.\nP3", fontsize=4.9, fontweight='bold', color='#4E342E', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # 4. Lavandería Ventilada Sur sin Escalera de Tanque (X: 0.30..2.75, Y: 0.15..3.45, H = 2,85 m libre!)
    draw_wall_x_openings(ax, 0.30, 2.75, 3.45, 3.60, [(1.65, 2.48, 'door_gap')])
    draw_door(ax, 1.65, 3.45, 0.80, 270, 360)
    draw_wall(ax, 2.75, 0.15, 2.90, 3.60)

    # --- MOBILIARIO COMPLETO DEL SEGUNDO PISO ---
    # A. Balconada Continua (Lounge Oeste + Comedor exterior 6p Este)
    ax.add_patch(Rectangle((0.50, 20.05), 0.80, 1.20, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((1.45, 20.35), 0.50, 0.60, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((6.35, 20.20), 1.80, 0.85, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(4.35, 20.62, "BALCONADA SOCIAL CONTINUA (8,70 x 1,96 m = 17,05 m²)\n3 Mamparas Corredizas de Cristal",
            fontsize=5.6, fontweight='bold', color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # B. Gran Sala Chalet (TV 75" en muro Oeste para abrir vista Este)
    ax.add_patch(Rectangle((2.60, 18.45), 2.65, 0.90, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((2.60, 16.30), 0.90, 2.15, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((3.85, 16.95), 0.80, 1.10, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    ax.add_patch(Rectangle((0.34, 16.25), 0.54, 2.50, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.plot([0.42, 0.42], [16.65, 18.35], color='#111111', lw=2.0, zorder=5)
    ax.text(1.72, 17.55, "Gran Sala\nChalet\n(TV 75\" Oeste)", fontsize=6.2, fontweight='bold', ha='center', va='center', zorder=6)

    # C. Estudio / Home Office Acristalado (X: 5.96..9.00, Y: 15.22..19.45)
    ax.add_patch(Rectangle((7.35, 16.60), 0.80, 1.80, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Circle((8.50, 17.50), 0.22, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.add_patch(Rectangle((6.05, 15.35), 0.40, 2.05, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(7.55, 18.85, "Estudio / Home Office\n(Hierro Negro y Cristal)", fontsize=5.6, fontweight='bold', color='#1A237E', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # D. Gran Comedor 10 Puestos + Desayunador Este
    ax.add_patch(Rectangle((2.05, 13.15), 2.70, 1.15, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    for ch_x in [2.25, 2.88, 3.51, 4.14]:
        ax.add_patch(Rectangle((ch_x, 12.68), 0.44, 0.40, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
        ax.add_patch(Rectangle((ch_x, 14.35), 0.44, 0.40, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.add_patch(Rectangle((1.62, 13.48), 0.38, 0.48, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.add_patch(Rectangle((4.80, 13.48), 0.38, 0.48, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.5, zorder=3))
    ax.text(3.40, 13.72, "Gran Comedor 10p", fontsize=5.9, fontweight='bold', ha='center', va='center', zorder=6)

    ax.add_patch(Rectangle((7.15, 13.05), 1.10, 1.10, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((6.55, 13.25), 0.48, 0.70, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((8.35, 13.25), 0.48, 0.70, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.70, 12.65, "Desayunador Este", fontsize=5.4, fontweight='bold', color='#3E2723', ha='center', va='top', zorder=6)

    # E. Cocina Gourmet: Mesón Oeste + Torre Hornos + NEVERA FRENCH DOOR NORTE + Gran Isla Central 2,90 m
    ax.add_patch(Rectangle((0.30, 8.45), 0.68, 3.03, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((0.38, 8.70), 0.48, 0.90, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))   # Fregadero doble
    ax.add_patch(Rectangle((0.38, 10.18), 0.50, 0.94, facecolor='#ECEFF1', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))# Cocina 5h
    ax.add_patch(Rectangle((0.30, 11.48), 0.68, 0.62, facecolor='#CFD8DC', edgecolor=C_FURN_EDGE, lw=0.65, zorder=4))# Torre Hornos
    # Nevera French Door (X: 0.32..1.10, Y: 12.14..13.04)
    ax.add_patch(Rectangle((0.32, 12.14), 0.78, 0.90, facecolor=C_COLD_SOFT, edgecolor='#0277BD', lw=0.85, zorder=5))
    ax.plot([1.04, 1.04], [12.16, 13.02], color='#01579B', lw=1.0, zorder=6)
    ax.text(1.18, 12.58, "Nevera\nFrench Door", fontsize=5.1, fontweight='bold', color='#01579B', ha='left', va='center', bbox=WHITE_HALO, zorder=7)
    ax.text(1.18, 11.78, "Hornos", fontsize=5.0, fontweight='bold', color='#37474F', ha='left', va='center')

    ax.add_patch(Rectangle((2.36, 8.85), 1.32, 2.90, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.75, zorder=4))
    for b_y in [9.15, 9.85, 10.55, 11.25]:
        ax.add_patch(Circle((3.84, b_y), 0.17, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=4))
    ax.text(3.00, 10.30, "Gran Isla\nGourmet\n(2,90 m)", fontsize=5.7, fontweight='bold', ha='center', va='center', zorder=6)
    ax.text(6.45, 10.15, "Cocina Bioclimática\nAbierta al Este", fontsize=6.2, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Hall libre de 3,10 m entre Escaleras y Baño Social (gracias a Despensa bajo escalera!)
    ax.text(4.30, 6.20, "Hall Social Despejado\n(3,10 m Libres)", fontsize=5.7, fontweight='bold', color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # F. Baño Social Completo + Habitación 4 Huéspedes / Adulto Mayor + Mirador Sur + Lavandería
    ax.add_patch(Rectangle((7.95, 4.50), 1.00, 1.05, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    draw_wc(ax, 7.32, 4.50, orientation='north')
    ax.add_patch(Rectangle((6.20, 6.75), 1.40, 0.57, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.15, 5.85, "Baño Social\nCompleto", fontsize=5.6, fontweight='bold', ha='center', va='center')

    draw_bed(ax, 6.05, 1.35, 7.95, 2.95, head='west')
    ax.add_patch(Rectangle((6.25, 3.70), 2.20, 0.58, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.50, 0.76, "Habitación 4 Huéspedes\n(3,00 x 4,15 m)", fontsize=5.4, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=8)

    ax.text(4.38, 2.15, "Galería / Mirador Sur\n(Brisa Cruzada)", fontsize=5.9, fontweight='bold', ha='center', va='center')

    ax.add_patch(Rectangle((0.35, 0.25), 0.70, 0.70, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((1.12, 0.25), 0.70, 0.70, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((1.88, 0.25), 0.82, 0.70, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((0.35, 1.35), 0.55, 1.80, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(1.75, 2.10, "Lavandería Libre\n(H = 2,85 m)", fontsize=5.6, fontweight='bold', ha='center', va='center')

    for cx, cy in PB_P2_P3_COLS:
        draw_col(ax, cx, cy, size=0.25, hatched=False)

    # Cotas Segundo Piso
    draw_dim_h(ax, 0.30, 5.88, 22.85, "5,58 (Gran Sala)", y_ref=21.71)
    draw_dim_h(ax, 5.96, 9.00, 22.85, "3,04 (Estudio)", y_ref=21.71)
    draw_dim_h(ax, 0.15, 9.15, 23.65, "9,00 (Ancho Cuerpo Casa)", y_ref=21.71)
    draw_dim_h(ax, 2.75, 5.85, 5.55, "3,10")

    draw_dim_v(ax, -0.65, 0.15, 3.45, "3,30", x_ref=0.15)
    draw_dim_v(ax, -0.65, 7.43, 19.45, "12,02", x_ref=0.15)
    draw_dim_v(ax, -0.65, 19.60, 21.56, "1,96", x_ref=0.15)
    draw_dim_v(ax, -1.35, 0.00, 21.71, "21,71", x_ref=0.15)

    draw_dim_v(ax, 9.75, 0.15, 4.30, "4,15", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 4.45, 7.35, "2,90", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 7.50, 15.14, "7,64", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 15.22, 19.45, "4,23", x_ref=9.15, text_side='right')

    ax.text(4.65, -1.15, "PLANTA SEGUNDO PISO SOCIAL BIOCLIMÁTICO (N.P.T. +3,00 m)",
            fontsize=9.6, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([1.05, 8.25], [-1.45, -1.45], color='#111111', lw=1.2)

    # Panel Derecho: Cuadro Técnico del Segundo Piso
    ax_side = fig.add_axes([0.69, 0.125, 0.28, 0.79])
    ax_side.axis('off')
    ax_side.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))

    ax_side.text(0.50, 0.965, "CUADRO DE AMBIENTES\nSEGUNDO PISO (195,39 m²)",
                 fontsize=8.8, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_side.plot([0.06, 0.94], [0.915, 0.915], color=C_BLUE, lw=0.9)

    zones_p2 = [
        ("1. BALCONADA Y 3 MAMPARAS", "17,05 m²",
         "• Balcón continuo de 8,70 x 1,96 m en Av. 4.\n"
         "• 3 Mamparas corredizas de cristal templado\n  con doble riel y paso franco al exterior."),
        ("2. GRAN SALA Y COMEDOR 10p", "64,80 m²",
         "• Planta social abierta a 3 fachadas (N, E, S)\n  para iluminación y brisa alisia directa.\n"
         "• Comedor 10 puestos + Desayunador Este."),
        ("3. ESTUDIO ACRISTALADO", "12,85 m²",
         "• Tabique industrial en hierro negro y vidrio\n  corredizo (privacidad sin perder luz)."),
        ("4. COCINA + NEVERA + ISLA", "32,40 m²",
         "• Mesón granito negro + Torre de Hornos.\n"
         "• Nevera French Door ubicada en nicho Norte\n  (X=0,32..1,10, Y=12,14..13,04).\n"
         "• Gran Isla central de 2,90 m con 4 bancos."),
        ("5. DESPENSA BAJO ESCALERA P3", "Aprovech.",
         "• Integrada bajo el tramo alto que sube a P3,\n  liberando un Hall limpio de 3,10 m."),
        ("6. HAB. 4, BAÑO Y LAVANDERÍA", "29,20 m²",
         "• Habitación 4 Huéspedes / Adulto Mayor +\n  Baño Social + Lavandería libre (H=2,85 m)."),
    ]
    y_cursor = 0.895
    for z_title, z_area, z_desc in zones_p2:
        ax_side.text(0.06, y_cursor, z_title, fontsize=6.8, fontweight='bold', color='#1A237E', va='top')
        ax_side.text(0.94, y_cursor, z_area, fontsize=6.8, fontweight='bold', color=C_RED, ha='right', va='top')
        y_cursor -= 0.021
        ax_side.text(0.06, y_cursor, z_desc, fontsize=5.95, color='#263238', va='top', linespacing=1.28)
        n_lines = z_desc.count('\n') + 1
        y_cursor -= (n_lines * 0.022 + 0.020)
        ax_side.plot([0.06, 0.94], [y_cursor + 0.008, y_cursor + 0.008], color='#CFD8DC', lw=0.6)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 4/7: NUEVO TERCER PISO PRIVADO + DETALLE BUHARDILLA TANQUES 2.000 L
# =============================================================================
def build_sheet_4_tercer_piso(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO PLANTA ARQUITECTÓNICA — TERCER PISO Y TANQUES",
                     "PENTHOUSE, CLARABOYA, TERRAZA MIRADOR BBQ (+6,00 m) + BUHARDILLA 2.000 L (+8,68 m).",
                     escala="1:75 / 1:50", sheet_num="4 / 7")

    # 1. PLANTA NUEVO TERCER PISO (IZQUIERDA)
    ax = fig.add_axes([0.04, 0.115, 0.61, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.9, 10.9)
    ax.set_ylim(-1.8, 24.4)
    ax.axis('off')

    draw_north(ax, 9.9, 23.1, r=0.50)

    # Pared vecino izquierdo intacta + línea de alero derecho propio (X = 10.10 m)
    ax.add_patch(Rectangle((0.00, 0.00), 0.15, 21.71, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax.text(-0.12, 11.0, "PARED VECINO (0,00 m ALERO)", rotation=90, fontsize=6.4, fontweight='bold', color='#666666', ha='right', va='center')
    ax.plot([10.10, 10.10], [-1.00, 21.71], color='#8D6E63', lw=0.9, linestyle='--', zorder=2)
    ax.text(10.22, 11.0, "PROYECCIÓN ALERO CUBIERTA (0,95 m)", rotation=90, fontsize=5.8, color='#6D4C41', ha='left', va='center')

    # Pisos interiores + GRAN TERRAZA CONTINUA MASTER NORTE (sin muro pantalla!) + GRAN TERRAZA MIRADOR SURESTE
    ax.add_patch(Rectangle((0.30, 4.30), 8.70, 15.15, facecolor='#FFFDF9', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.30, 0.15), 2.45, 4.15,  facecolor='#FFFDF9', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0.30, 19.60), 8.70, 1.96, facecolor=C_WOOD_SOFT, edgecolor='#6D4C41', lw=0.85, zorder=2))
    ax.add_patch(Rectangle((2.90, 0.00), 6.25, 4.30,  facecolor=C_STONE_SOFT, edgecolor='#546E7A', lw=0.85, zorder=2))

    # Barandas Alpinas en Terraza Continua Master Norte y en Gran Terraza Mirador BBQ Sureste
    ax.add_patch(Rectangle((0.30, 21.52), 8.77, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((9.03, 19.60), 0.10, 2.04, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((2.90, 0.02),  6.23, 0.12, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))
    ax.add_patch(Rectangle((9.03, 0.02),  0.10, 4.30, facecolor='#8D6E63', edgecolor='black', lw=0.7, zorder=5))

    # Muro Oeste Propio Parapeto Ciego P3
    draw_wall(ax, 0.15, 0.00, 0.30, 21.71, facecolor='#6D4C41')

    # Muro Frontal Retranqueado P3 (Y: 19.45..19.60):
    # - Oeste (0.30..4.50): Muro bajo protector de ropa + VENTANA ALTA CLERESTORY UV (0.95..3.65, H=2,35..2,80 m)
    # - Este (4.50..9.00): Gran Mampara Corrediza desde Dormitorio Master hacia toda la Terraza Continua
    draw_wall_x_openings(ax, 0.30, 9.00, 19.45, 19.60, [
        (0.95, 3.65, 'high_win'),
        (5.25, 8.45, 'mampara'),
    ], facecolor='#6D4C41')
    ax.text(2.30, 19.72, "Ventana Alta Clerestory UV (H=2,35..2,80m)", fontsize=4.8, fontweight='bold',
            color='#01579B', ha='center', va='bottom', bbox=WHITE_HALO, zorder=7)

    # Fachada Este P3 (Y: 4.30..19.60; esquina Sureste Y=0.00..4.30 abierta a Gran Terraza Mirador!)
    draw_wall_y_openings(ax, 9.00, 9.15, 4.30, 19.60, [
        (4.90,  5.85, 'win'),
        (7.35,  9.25, 'shutter_win'),
        (11.40, 13.45, 'shutter_win'),
        (15.75, 18.45, 'shutter_win'),
    ], facecolor='#6D4C41')

    # Muro Sur Cuarto Apoyo / Gym (X: 0.15..2.90, Y: 0.00..0.15)
    draw_wall_x_openings(ax, 0.15, 2.90, 0.00, 0.15, [(0.85, 2.35, 'win')], facecolor='#6D4C41')

    # --- TABIQUERÍA INTERIOR DEL TERCER PISO ---
    # 1. Master Penthouse Suite: Muro divisorio Dormitorio <-> Vestier / Baño Spa (X: 4.35..4.50, Y: 12.80..19.45)
    draw_wall_y_openings(ax, 4.35, 4.50, 12.80, 19.45, [
        (14.70, 15.50, 'door_gap'),   # Puerta auxiliar a 45° Dormitorio <-> Baño Spa
        (17.05, 18.35, 'door_gap'),   # GRAN PORTAL BARN DOOR (1,30 m) al Vestier!
    ])
    draw_door(ax, 4.35, 14.70, 0.78, 225, 270)
    # Riel de hierro negro visto + 2 hojas Barn Door abiertas flanqueando el portal (16.22..16.95 y 18.45..19.18)
    ax.plot([4.54, 4.54], [16.15, 19.25], color='#212121', lw=1.5, zorder=6)
    ax.add_patch(Rectangle((4.51, 16.22), 0.08, 0.73, facecolor='#8D6E63', edgecolor='black', lw=0.6, zorder=7))
    ax.add_patch(Rectangle((4.51, 18.45), 0.08, 0.73, facecolor='#8D6E63', edgecolor='black', lw=0.6, zorder=7))

    # Puerta Principal Master Penthouse desde Family Room (X: 4.75..5.65 en Y=14.45..14.60)
    draw_wall_x_openings(ax, 4.50, 9.00, 14.45, 14.60, [(4.75, 5.65, 'door_gap')])
    draw_door(ax, 4.75, 14.60, 0.85, 90, 0)

    # Tabique Vestier <-> Baño Spa con PUERTA INTERNA VISIBLE A 45° (X: 1.65..2.50 en Y=15.90..16.05)
    draw_wall_x_openings(ax, 0.30, 4.35, 15.90, 16.05, [(1.65, 2.50, 'door_gap')])
    draw_door(ax, 1.65, 16.05, 0.82, 45, 0)
    draw_wall(ax, 0.30, 12.65, 4.50, 12.80)

    # 2. Espina Este de Habitaciones Secundarias 2 y 3 + Baño Familiar (Y: 4.30..14.45 — SIN Hab. 4!)
    draw_wall_y_openings(ax, 5.85, 6.00, 4.30, 14.45, [
        (4.90,  5.70, 'door_gap'),
        (7.10,  7.90, 'door_gap'),
        (10.85, 11.65, 'door_gap'),
    ])
    draw_door(ax, 6.00, 5.70,  0.78, 0, 270)   # Baño Familiar P3
    draw_door(ax, 6.00, 7.10,  0.80, 0, 90)    # Habitación 3
    draw_door(ax, 6.00, 10.85, 0.80, 0, 90)    # Habitación 2
    draw_wall(ax, 6.00, 10.15, 9.00, 10.30)
    draw_wall(ax, 6.00,  6.30, 9.00,  6.45)
    draw_wall(ax, 5.85,  4.30, 9.15,  4.45, facecolor='#6D4C41')

    # 3. Cierre acristalado hacia Gran Terraza Mirador BBQ (X: 2.90..5.85, Y: 4.30..4.45) + Cuarto Apoyo/Gym
    draw_wall_x_openings(ax, 2.90, 5.85, 4.30, 4.45, [(3.35, 5.35, 'mampara')], facecolor='#6D4C41')
    draw_wall(ax, 2.75, 0.00, 2.90, 4.45)
    draw_wall_x_openings(ax, 0.30, 2.75, 4.10, 4.25, [(1.65, 2.48, 'door_gap')])
    draw_door(ax, 1.65, 4.10, 0.80, 270, 360)

    # Escalera Tramo 3 llegando desde P2 (X: 0.30..1.45, Y: 4.40..7.40) + Baranda desembarque + Clóset Blancos
    draw_stairs_numbered(ax, 0.30, 4.40, 1.45, 7.40, 14, direction='down_y', label_txt='BAJA P.2')
    ax.plot([1.52, 1.52], [4.40, 7.35], color='#6D4C41', lw=1.4, zorder=6)
    ax.plot([0.32, 1.52], [4.38, 4.38], color='#6D4C41', lw=1.4, zorder=6)
    ax.add_patch(Rectangle((1.65, 5.20), 0.70, 1.15, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(2.00, 5.77, "Blancos", rotation=90, fontsize=5.0, fontweight='bold', ha='center', va='center')

    # --- PROYECCIÓN DEL HUECO REAL DE CLARABOYA VENTILADA (X: 2.45..5.55, Y: 5.50..11.30 = 3,10 x 5,80 m) ---
    ax.add_patch(Rectangle((2.45, 5.50), 3.10, 5.80, facecolor='#E0F7FA', edgecolor=C_AXIS_CYAN,
                           lw=1.15, linestyle='--', alpha=0.38, zorder=2))
    ax.plot([2.45, 5.55], [5.50, 11.30], color=C_AXIS_CYAN, lw=0.6, linestyle=':', zorder=2)
    ax.plot([2.45, 5.55], [11.30, 5.50], color=C_AXIS_CYAN, lw=0.6, linestyle=':', zorder=2)
    ax.text(4.20, 8.20, "POZO DE LUZ Y AIRE\nCLARABOYA VENTILADA\n(Hueco Real 3,10 x 5,80 m)",
            fontsize=5.5, fontweight='bold', color='#006064', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # --- MOBILIARIO Y EQUIPAMIENTO DEL TERCER PISO ---
    # A. Gran Terraza Continua Master (Lounge Este + Rincón Café Oeste) + Dormitorio Master Penthouse
    ax.add_patch(Rectangle((6.20, 20.30), 2.00, 0.85, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((0.90, 20.15), 0.75, 0.80, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((2.45, 20.15), 0.75, 0.80, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((1.78, 20.25), 0.54, 0.55, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(4.55, 20.92, "GRAN TERRAZA CONTINUA MASTER (8,70 x 1,96 m = 17,05 m²)",
            fontsize=5.4, fontweight='bold', color='#3E2723', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    draw_bed(ax, 6.20, 14.74, 8.20, 16.78, head='south')
    ax.add_patch(Rectangle((5.65, 14.74), 0.47, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((8.28, 14.74), 0.47, 0.48, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((8.25, 17.65), 0.63, 1.00, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.05, 18.05, "Master Penthouse\n(4,50 x 4,85 m = 21,8 m²)", fontsize=6.0, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # B. Gran Vestier Walk-In Doble + Baño Spa Master con Tina Exenta
    ax.add_patch(Rectangle((0.34, 16.12), 0.58, 3.23, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='||', zorder=3))
    ax.add_patch(Rectangle((0.95, 18.85), 2.70, 0.53, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='---', zorder=3))
    ax.add_patch(Rectangle((3.72, 16.12), 0.58, 0.83, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='||', zorder=3))
    ax.add_patch(Rectangle((3.72, 18.45), 0.58, 0.90, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, hatch='||', zorder=3))
    ax.add_patch(Rectangle((1.85, 17.25), 0.80, 1.00, facecolor='#EFEBE9', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    ax.text(2.15, 16.68, "Gran Vestier Walk-In\n(13,7 m² • Barn Door 1,30m)", fontsize=5.2, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=9)

    # Tina Exenta + Ducha Doble Pizarra + Tocador Doble + WC
    ax.add_patch(FancyTub := Circle((0.91, 14.96), 0.01, facecolor='none', edgecolor='none'))
    ax.add_patch(Rectangle((0.50, 14.20), 0.82, 1.52, facecolor='white', edgecolor='#0277BD', lw=0.85, zorder=4))
    ax.add_patch(Rectangle((0.60, 14.32), 0.62, 1.28, facecolor=C_COLD_SOFT, edgecolor='#0288D1', lw=0.55, zorder=4))
    ax.add_patch(Rectangle((0.35, 12.85), 1.40, 1.10, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((2.62, 15.32), 1.60, 0.56, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Circle((3.08, 15.60), 0.14, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
    ax.add_patch(Circle((3.76, 15.60), 0.14, facecolor='white', edgecolor=C_FURN_EDGE, lw=0.5, zorder=4))
    draw_wc(ax, 2.80, 12.88, orientation='north')
    ax.text(2.95, 14.15, "Baño Spa Master\ncon Tina (12,5 m²)", fontsize=5.4, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # C. Family Room / Cine 85" + Coffee Bar
    ax.add_patch(Rectangle((2.55, 9.35), 1.00, 2.80, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((1.45, 11.25), 1.10, 0.90, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.65, zorder=3))
    ax.add_patch(Rectangle((1.55, 9.85), 0.70, 1.00, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=4))
    ax.add_patch(Rectangle((0.34, 9.45), 0.51, 2.65, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.plot([0.42, 0.42], [9.75, 11.80], color='#111111', lw=2.0, zorder=5)
    ax.add_patch(Rectangle((0.34, 7.65), 0.54, 1.45, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(4.65, 11.95, "Family Room &\nCine 85\"", fontsize=5.8, fontweight='bold', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # D. Habitaciones 2 y 3 + Baño Familiar + GRAN TERRAZA MIRADOR & QUINCHO BBQ (26,88 m²)
    draw_bed(ax, 6.08, 11.65, 7.95, 13.10, head='west')
    ax.add_patch(Rectangle((6.25, 13.85), 2.15, 0.55, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.55, 10.95, "Habitación 2 (12,45 m²)", fontsize=5.6, fontweight='bold', ha='center', va='center')

    draw_bed(ax, 6.08, 7.65, 7.95, 9.10, head='west')
    ax.add_patch(Rectangle((6.25, 9.55), 2.15, 0.55, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(7.55, 6.95, "Habitación 3 (11,10 m²)", fontsize=5.6, fontweight='bold', ha='center', va='center')

    ax.add_patch(Rectangle((7.95, 4.48), 1.00, 1.77, facecolor=C_STONE_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    draw_wc(ax, 7.18, 4.48, orientation='north')
    ax.add_patch(Rectangle((6.10, 5.70), 1.35, 0.56, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.text(6.95, 5.28, "Baño Fam.", fontsize=5.3, fontweight='bold', ha='center', va='center')

    # Equipamiento Gran Terraza Mirador & Quincho BBQ (Barra BBQ + Comedor 8p + Lounge)
    ax.add_patch(Rectangle((6.20, 3.65), 2.45, 0.63, facecolor='#CFD8DC', edgecolor='#263238', lw=0.75, zorder=4))
    ax.add_patch(Rectangle((7.45, 3.68), 1.03, 0.57, facecolor='#455A64', edgecolor='black', lw=0.65, zorder=5))
    ax.text(7.42, 3.35, "Barra Quincho BBQ", fontsize=5.1, fontweight='bold', color='#263238', ha='center', va='top', bbox=WHITE_HALO, zorder=6)

    ax.add_patch(Rectangle((3.45, 1.35), 2.00, 1.05, facecolor='#D7CCC8', edgecolor=C_FURN_EDGE, lw=0.7, zorder=4))
    ax.add_patch(Rectangle((3.55, 0.85), 1.80, 0.37, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((3.55, 2.52), 1.80, 0.36, facecolor='#FAFAFA', edgecolor=C_FURN_EDGE, lw=0.55, zorder=3))
    ax.add_patch(Rectangle((6.55, 0.55), 2.05, 0.77, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((7.85, 1.32), 0.75, 1.13, facecolor=C_WOOD_SOFT, edgecolor=C_FURN_EDGE, lw=0.6, zorder=3))
    ax.text(5.85, 0.38, "GRAN TERRAZA MIRADOR & QUINCHO BBQ (26,88 m²)",
            fontsize=5.4, fontweight='bold', color='#1B5E20', ha='center', va='bottom', bbox=WHITE_HALO, zorder=7)

    # Cuarto de Apoyo / Gimnasio + Escalera fija a Buhardilla 2.000 L (X: 0.38..1.18, Y: 2.55..3.70)
    ax.add_patch(Rectangle((0.38, 2.55), 0.80, 1.15, facecolor='#FFF8E1', edgecolor='#E65100', lw=0.8, linestyle='--', zorder=4))
    for sy_m in np.linspace(2.65, 3.60, 8):
        ax.plot([0.45, 1.05], [sy_m, sy_m], color='#E65100', lw=0.6, zorder=5)
    ax.text(1.55, 1.55, "Cuarto Apoyo /\nGimnasio\n+ Subida Tanques", fontsize=5.3, fontweight='bold', ha='center', va='center')

    # Columnas Metálicas Estructurales Negras en Piso 3 (25 x 25 cm)
    for cx, cy in PB_P2_P3_COLS:
        draw_col(ax, cx, cy, size=0.25, steel_black=True)

    # Cotas Tercer Piso
    draw_dim_h(ax, 0.30, 4.35, 22.85, "4,05 (Vestier/Spa)", y_ref=21.71)
    draw_dim_h(ax, 4.50, 9.00, 22.85, "4,50 (Master)", y_ref=21.71)
    draw_dim_h(ax, 0.15, 9.15, 23.65, "9,00 (Ancho Cuerpo Casa)", y_ref=21.71)

    draw_dim_v(ax, -0.65, 0.15, 4.10, "3,95", x_ref=0.15)
    draw_dim_v(ax, -0.65, 12.80, 19.45, "6,65", x_ref=0.15)
    draw_dim_v(ax, -0.65, 19.60, 21.56, "1,96", x_ref=0.15)
    draw_dim_v(ax, -1.35, 0.00, 21.71, "21,71", x_ref=0.15)

    draw_dim_v(ax, 9.75, 0.00, 4.30, "4,30 (Mirador)", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 4.45, 6.30, "1,85", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 6.45, 10.15, "3,70", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 10.30, 14.45, "4,15", x_ref=9.15, text_side='right')
    draw_dim_v(ax, 9.75, 14.60, 19.45, "4,85", x_ref=9.15, text_side='right')

    ax.text(4.65, -1.15, "PLANTA NUEVO TERCER PISO PRIVADO Y MIRADOR BBQ (N.P.T. +6,00 m)",
            fontsize=9.3, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([0.95, 8.35], [-1.45, -1.45], color='#111111', lw=1.2)

    # 2. PLANTA DETALLE BUHARDILLA TÉCNICA RESERVA 2.000 L (ARRIBA DERECHA)
    ax_t = fig.add_axes([0.67, 0.495, 0.29, 0.415])
    ax_t.set_aspect('equal')
    ax_t.set_xlim(-0.85, 4.35)
    ax_t.set_ylim(-1.25, 5.45)
    ax_t.axis('off')

    ax_t.add_patch(Rectangle((0.00, 0.00), 0.15, 4.45, facecolor=C_NEIGHBOR, edgecolor='#777777', lw=0.6, hatch='///', zorder=2))
    ax_t.add_patch(Rectangle((0.30, 0.15), 2.45, 4.10, facecolor='#F9FBE7', edgecolor='none', zorder=1))
    draw_wall(ax_t, 0.15, 0.00, 0.30, 4.45, facecolor='#6D4C41')
    draw_wall(ax_t, 2.75, 0.00, 2.90, 4.45, facecolor='#6D4C41')
    draw_wall(ax_t, 0.15, 4.25, 2.90, 4.45, facecolor='#6D4C41')
    draw_wall_x_openings(ax_t, 0.15, 2.90, 0.00, 0.15, [(0.88, 2.33, 'win')], facecolor='#6D4C41')

    # Escotilla de acceso (X: 0.38..1.18, Y: 2.55..3.70) + BARANDA REORIENTADA EN "L" (deja libre Este Y=3.05..4.25!)
    ax_t.add_patch(Rectangle((0.38, 2.55), 0.80, 1.15, facecolor='#FFF8E1', edgecolor='#E65100', lw=0.9, zorder=4))
    for sy_m in np.linspace(2.65, 3.60, 8):
        ax_t.plot([0.45, 1.05], [sy_m, sy_m], color='#E65100', lw=0.65, zorder=5)
    # Baranda en "L" protegiendo Sur (Y=2.50) y mitad Sureste (X=1.24, Y=2.50..3.05)
    ax_t.plot([0.38, 1.24], [2.50, 2.50], color=C_COL_RED, lw=1.6, zorder=6)
    ax_t.plot([1.24, 1.24], [2.50, 3.05], color=C_COL_RED, lw=1.6, zorder=6)
    ax_t.annotate('', xy=(1.85, 3.62), xytext=(0.95, 3.62),
                  arrowprops=dict(arrowstyle='->', color='#1B5E20', lw=1.2), zorder=7)
    ax_t.text(1.62, 4.00, "Paso Libre Este (1,20 m)", fontsize=4.9, fontweight='bold',
              color='#1B5E20', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Pedestal doble + 2 Tanques Verticales de 1.000 L c/u (Total = 2.000 L, Ø 1,00 m)
    ax_t.add_patch(Rectangle((0.95, 0.22), 1.20, 2.33, facecolor='#ECEFF1', edgecolor='#546E7A', lw=0.8, zorder=3))
    for t_idx, (tcx, tcy) in enumerate([(1.55, 0.82), (1.55, 1.98)], start=1):
        ax_t.add_patch(Circle((tcx, tcy), 0.50, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=1.15, zorder=5))
        ax_t.add_patch(Circle((tcx, tcy), 0.18, facecolor='white', edgecolor='#0D47A1', lw=0.75, zorder=6))
        ax_t.text(tcx, tcy, f"TANQUE {t_idx}\n1.000 L", fontsize=4.8, fontweight='bold',
                  color='#0D47A1', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # Bomba Hidroneumática + Pulmón (X: 1.95..2.68, Y: 2.75..3.15)
    ax_t.add_patch(Rectangle((1.95, 2.70), 0.75, 0.55, facecolor='#ECEFF1', edgecolor='#455A64', lw=0.7, zorder=3))
    ax_t.add_patch(Circle((2.50, 2.97), 0.15, facecolor='#FFCDD2', edgecolor='#B71C1C', lw=0.6, zorder=4))
    ax_t.text(2.34, 3.34, "Bomba+Pulmón", fontsize=4.5, fontweight='bold', color='#263238', ha='center', va='bottom', bbox=WHITE_HALO, zorder=7)
    ax_t.text(1.60, -0.26, "Celosía Abatible 1,45 m", fontsize=5.3, fontweight='bold', color='#3E2723', ha='center', va='top')

    draw_dim_h(ax_t, 0.30, 2.75, 4.80, "2,45", y_ref=4.45)
    draw_dim_v(ax_t, 3.35, 0.15, 4.25, "4,10", x_ref=2.90, text_side='right')
    ax_t.text(1.55, -0.72, "PLANTA BUHARDILLA RESERVA 2.000 L\n(N.P.T. +8,68 m — ESC. 1:50)",
              fontsize=7.3, fontweight='bold', color='#111111', ha='center', va='top')

    # 3. CUADRO RESUMEN DEL TERCER PISO (ABAJO DERECHA)
    ax_res = fig.add_axes([0.67, 0.115, 0.29, 0.365])
    ax_res.axis('off')
    ax_res.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))
    ax_res.text(0.50, 0.95, "PROGRAMA ARQUITECTÓNICO\nTERCER PISO (195,39 m²)",
                fontsize=8.2, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_res.plot([0.06, 0.94], [0.845, 0.845], color=C_BLUE, lw=0.8)

    p3_notes = [
        "• Terraza Continua Master (17,05 m²):\n  Frente unificado sin muro pantalla; acceso\n  exclusivo desde el Dormitorio Master.",
        "• Gran Vestier (13,7 m²) + Clerestory UV:\n  Portal Barn Door (1,30 m), ventana alta\n  (H=2,35..2,80 m) sobre clóset Norte y\n  puerta interna a 45° al Baño Spa con Tina.",
        "• Claraboya Ventilada (3,10 x 5,80 m):\n  Hueco real en cubierta sobre Family Room\n  para luz cenital y efecto chimenea solar.",
        "• Gran Terraza Mirador & BBQ (26,88 m²):\n  Esquina Sureste abierta (sin Hab. 4) con\n  columnas metálicas negras vistas.",
        "• Buhardilla 2.000 L (+8,68 m):\n  2 tanques x 1.000 L con baranda en 'L'\n  que deja libre el desembarque Este.",
    ]
    yy = 0.815
    for note in p3_notes:
        ax_res.text(0.06, yy, note, fontsize=5.8, color='#263238', va='top', linespacing=1.24)
        yy -= (note.count('\n') + 1) * 0.039 + 0.015

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 5/7: PLANO DISTRIBUCIÓN DE COLUMNAS, ACERO P3 Y EJES ESTRUCTURALES
# =============================================================================
def build_sheet_5_columnas_estructura(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "PLANO DISTRIBUCIÓN DE COLUMNAS Y EJES ESTRUCTURALES",
                     "SÓTANO (35x35 cm) • P.B. Y P2 CONCRETO (25x25 cm) • P3 COLUMNAS METÁLICAS NEGRAS + STEEL DECK.",
                     escala="1:75", sheet_num="5 / 7")

    # 1. PANEL PRINCIPAL IZQUIERDO: PLANTA ESTRUCTURAL P.B., P2 Y NUEVO P3 (32 APOYOS)
    ax = fig.add_axes([0.035, 0.115, 0.565, 0.815])
    ax.set_aspect('equal')
    ax.set_xlim(-1.4, 11.4)
    ax.set_ylim(-2.0, 24.4)
    ax.axis('off')

    # Contornos arquitectónicos tenues de referencia
    ghost_rects = [
        (0.15, 0.00, 9.00, 21.71),   # Perímetro general propio
        (0.30, 8.80, 3.00, 12.76),   # Estacionamiento PB
        (0.30, 19.60, 8.70, 1.96),   # Balconada / Terraza Continua P2-P3
        (2.90, 0.00, 6.25, 4.30),    # Terraza Mirador BBQ P3
        (0.30, 4.40, 1.15, 3.00),    # Escalera Sótano / P3
        (1.55, 4.40, 1.10, 2.95),    # Escalera P2
    ]
    for gx, gy, gw, gh in ghost_rects:
        ax.add_patch(Rectangle((gx, gy), gw, gh, fill=False, edgecolor='#B0B0B0', lw=0.55, linestyle='--', zorder=1))

    # Vigas metálicas longitudinales negras de entrepiso Steel Deck P3 (Ejes 0, 1, 2, 3)
    for gx_b in [0.275, 2.825, 5.925, 9.025]:
        ax.plot([gx_b, gx_b], [0.125, 21.585], color='#546E7A', lw=1.6, alpha=0.45, zorder=2)

    # Anillo estructural de acero negro del Hueco de Claraboya en Cubierta P3 (X: 2.45..5.55, Y: 5.50..11.30)
    ax.add_patch(Rectangle((2.45, 5.50), 3.10, 5.80, facecolor='#E0F7FA', edgecolor='#006064',
                           lw=1.1, linestyle='--', alpha=0.45, zorder=2))
    ax.text(4.00, 8.40, "Anillo Metálico\nHueco Claraboya\n(3,10 x 5,80 m)", fontsize=5.5, fontweight='bold',
            color='#006064', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    # Cuadrante reforzado de Losa Tanques 2.000 L (Ejes 0-1 / G-H a +8,68 m)
    ax.add_patch(Rectangle((0.275, 0.125), 2.55, 3.45, facecolor='#E3F2FD', edgecolor='#1565C0',
                           lw=0.95, linestyle='-.', alpha=0.55, zorder=2))
    ax.text(1.55, 1.85, "Losa Portante\n2 x 1.000 L = 2.000 L\n(N.P.T. +8,68 m)", fontsize=5.3, fontweight='bold',
            color='#0D47A1', ha='center', va='center', bbox=WHITE_HALO, zorder=6)

    ref_labels = [
        (1.65, 15.20, "Garaje P.B. /\nVestier-Spa P3"),
        (4.55, 20.55, "Balconada Continua P2 / Terraza Master P3"),
        (4.45, 14.20, "Comercio P.B. /\nSala-Comedor P2"),
        (7.50, 17.20, "Estudio P2 /\nMaster Penthouse P3"),
        (7.50, 12.30, "Habitación 2 P3"),
        (7.50,  8.10, "Habitación 3 P3"),
        (6.00,  2.15, "Hab. 4 P2 /\nTerraza Mirador BBQ P3"),
    ]
    for rx, ry, rtxt in ref_labels:
        ax.text(rx, ry, rtxt, fontsize=5.4, color='#555555', fontweight='bold', ha='center', va='center', zorder=2)

    # Ejes estructurales verticales (0, 1, 2, 3) y horizontales (A0..H)
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

    # 32 Columnas achuradas en rojo + núcleo negro indicando transición a Acero Negro en P3
    for cx, cy in PB_P2_P3_COLS:
        draw_col(ax, cx, cy, size=0.30, hatched=True)
        ax.add_patch(Rectangle((cx - 0.07, cy - 0.07), 0.14, 0.14, facecolor=C_STEEL_BLK, edgecolor='white', lw=0.4, zorder=9))

    # Cotas entre ejes estructurales
    draw_dim_h(ax, 0.275, 2.825, 22.35, "2,55", y_ref=21.585)
    draw_dim_h(ax, 2.825, 5.925, 22.35, "3,10", y_ref=21.585)
    draw_dim_h(ax, 5.925, 9.075, 22.35, "3,15", y_ref=21.585)

    draw_dim_h(ax, 0.275, 2.825, -0.55, "2,55", y_ref=0.125)
    draw_dim_h(ax, 2.825, 5.925, -0.55, "3,10", y_ref=0.125)
    draw_dim_h(ax, 5.925, 9.075, -0.55, "3,15", y_ref=0.125)

    y_pairs = [
        (18.575, 21.585, "3,01"), (16.325, 18.575, "2,25"), (14.625, 16.325, "1,70"),
        (12.025, 14.625, "2,60"), ( 8.875, 12.025, "3,15"), ( 6.575,  8.875, "2,30"),
        ( 3.575,  6.575, "3,00"), ( 0.125,  3.575, "3,45"),
    ]
    for y_a, y_b, lbl_d in y_pairs:
        draw_dim_v(ax, 9.75, y_a, y_b, lbl_d, fontsize=5.8, text_side='left')
    draw_dim_v(ax, -0.65, 0.125, 21.585, "21,46 (Entre Ejes Extremos)", x_ref=0.275)

    ax.text(4.65, -1.22, "PLANTA ESTRUCTURAL P.B., P2 Y NUEVO P3\n(32 NODOS: CONCRETO 25x25 cm EN P.B./P2 + ACERO NEGRO EN P3)",
            fontsize=8.1, fontweight='bold', color='#111111', ha='center', va='top')
    ax.plot([0.85, 8.45], [-1.82, -1.82], color='#111111', lw=1.1)

    # 2. PANEL INFERIOR DERECHO: PLANTA ESTRUCTURAL SÓTANO BODEGA (35 x 35 cm)
    ax_sot = fig.add_axes([0.60, 0.115, 0.37, 0.41])
    ax_sot.set_aspect('equal')
    ax_sot.set_xlim(-0.8, 11.2)
    ax_sot.set_ylim(-1.9, 10.3)
    ax_sot.axis('off')

    ax_sot.add_patch(Rectangle((0.15, 0.00), 9.00, 8.30, fill=False, edgecolor='#9E9E9E', lw=0.6, linestyle='--', zorder=1))
    ax_sot.add_patch(Rectangle((0.15, 8.15), 9.00, 0.15, facecolor='#E0E0E0', edgecolor='#616161', lw=0.7, hatch='///', zorder=2))
    ax_sot.add_patch(Rectangle((0.15, 0.00), 0.15, 8.30, facecolor='#E0E0E0', edgecolor='#616161', lw=0.7, hatch='///', zorder=2))
    for sy_i in np.linspace(4.45, 7.40, 13):
        ax_sot.plot([0.30, 1.40], [sy_i, sy_i], color='#C0C0C0', lw=0.45, linestyle='--', zorder=1)

    ax_sot.text(3.55, 6.80, "Pre-Frío.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(7.25, 5.10, "Avenida Carga.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(1.55, 1.85, "Racks S.O.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')
    ax_sot.text(3.75, 1.45, "Baño.", fontsize=5.8, color='#555555', fontweight='bold', ha='center')

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

    draw_col(ax_sot, 0.25, 6.575, size=0.35, hatched=True)
    for cx, cy in SOT_COLS:
        draw_col(ax_sot, cx, cy, size=0.38, hatched=True)

    draw_dim_h(ax_sot, 0.325, 2.825, 8.65, "2,50", y_ref=8.30, fontsize=5.8)
    draw_dim_h(ax_sot, 2.825, 5.925, 8.65, "3,10", y_ref=8.30, fontsize=5.8)
    draw_dim_h(ax_sot, 5.925, 8.975, 8.65, "3,05", y_ref=8.30, fontsize=5.8)
    draw_dim_v(ax_sot, 9.65, 3.575, 6.575, "3,00", fontsize=5.8, text_side='left')
    draw_dim_v(ax_sot, 9.65, 0.175, 3.575, "3,40", fontsize=5.8, text_side='left')

    ax_sot.text(4.65, -0.85, "PLANTA SÓTANO BODEGA (12 APOYOS 35 x 35 cm)",
                fontsize=8.0, fontweight='bold', color='#111111', ha='center', va='top')
    ax_sot.plot([1.20, 8.10], [-1.22, -1.22], color='#111111', lw=1.1)

    # 3. PANEL SUPERIOR DERECHO: MEMORIA Y ESPECIFICACIONES ESTRUCTURALES (4 NIVELES)
    ax_sp = fig.add_axes([0.61, 0.545, 0.355, 0.375])
    ax_sp.axis('off')
    ax_sp.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FAFAFA', edgecolor=C_BLUE, lw=1.1))
    ax_sp.text(0.50, 0.955, "MEMORIA Y ESPECIFICACIONES\nESTRUCTURALES (3 PISOS + SÓTANO)",
               fontsize=8.1, fontweight='bold', color=C_RED, ha='center', va='top')
    ax_sp.plot([0.06, 0.94], [0.855, 0.855], color=C_BLUE, lw=0.8)

    spec_blocks = [
        ("1. SÓTANO BODEGA MAYORISTA (-2,55 m):",
         "• 12 columnas de 35 x 35 cm en concreto armado\n  (f'c = 280 kg/cm²) + muros de contención N/O.\n"
         "• Cero contacto con fundación vecina (X >= 0,15 m)."),
        ("2. PLANTA BAJA Y SEGUNDO PISO (0,00 / +3,00 m):",
         "• 32 columnas de 25 x 25 cm en retícula ortogonal\n  continua (Ejes 0, 1, 2, 3 x A0..H) + vigas 25x40 cm."),
        ("3. TERCER PISO LIVIANO EN ACERO (+6,00 m):",
         "• Entrepiso colaborante Steel Deck (e = 15 cm)\n  sobre vigas metálicas negras para reducir masa\n  sísmica en el nivel superior.\n"
         "• 32 Columnas metálicas estructurales negras\n  25x25 cm / IPE con placas base empernadas."),
        ("4. CUBIERTA 32°, CLARABOYA Y 2.000 L (+8,68 m):",
         "• Anillo metálico perimetral en hueco de claraboya\n  (3,10 x 5,80 m) + Losa portante para 2.000 kg."),
    ]
    sy_cur = 0.825
    for stitle, sbody in spec_blocks:
        ax_sp.text(0.06, sy_cur, stitle, fontsize=6.4, fontweight='bold', color='#1A237E', va='top')
        sy_cur -= 0.034
        ax_sp.text(0.06, sy_cur, sbody, fontsize=5.8, color='#263238', va='top', linespacing=1.25)
        sy_cur -= (sbody.count('\n') + 1) * 0.034 + 0.020

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 6/7: PLANO DE FACHADAS Y ELEVACIONES DE 3 PISOS (APAISADO 17x11 in)
# =============================================================================
def draw_sheet_frame_landscape(fig, title_line1, title_line2="", escala="1:75 / 1:100", sheet_num="6 / 7", fecha="NOV 2026"):
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

    ax.text(0.975, 0.966, "PROYECTO AMPLIACIÓN: 3 PISOS CHALET ALPINO & COMERCIO",
            fontsize=9.0, fontweight='bold', color='#263238', ha='right', va='top')
    ax.text(0.975, 0.942, f"ELEVACIONES, RAMPA Y CLARABOYA  |  LÁMINA {sheet_num}",
            fontsize=8.2, fontweight='bold', color=C_BLUE, ha='right', va='top')

    c_left, c_right = 0.017, 0.983
    c_bot = 0.023
    row_top = 0.078
    caj_top = 0.128

    ax.plot([c_left, c_right], [caj_top, caj_top], color=C_BLUE, lw=1.6)
    ax.plot([c_left, c_right], [row_top, row_top], color=C_BLUE, lw=1.2)

    ax.text(0.025, caj_top - 0.016, title_line1, fontsize=10.8, fontweight='bold', color=C_RED, ha='left', va='center')
    if title_line2:
        ax.text(0.025, caj_top - 0.036, title_line2, fontsize=8.3, fontweight='bold', color=C_RED, ha='left', va='center')
    ax.text(0.975, caj_top - 0.016,
            "PIEDRA + MADERA + ACERO NEGRO P3 + CLARABOYA VENTILADA",
            fontsize=7.8, fontweight='bold', color='#37474F', ha='right', va='center')
    ax.text(0.975, caj_top - 0.036,
            "RESPETO ESTRICTO DE MEDIANERA (0,00 m INVASIÓN LINDERO VECINO)",
            fontsize=7.4, fontweight='bold', color=C_BLUE, ha='right', va='center')

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
    ax.text(0.745, row_top - 0.032, "PROYECTO AMPLIACIÓN\n3 PISOS + BODEGA", fontsize=6.8, fontweight='bold', color='#1B5E20', ha='center', va='center')

    ax.text(0.830, row_top - 0.011, "FECHA:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.865, row_top - 0.034, fecha, fontsize=8.5, fontweight='bold', color=C_RED, ha='center')

    ax.text(0.910, row_top - 0.011, "ESCALA:", fontsize=6.2, fontweight='bold', color=C_BLUE)
    ax.text(0.944, row_top - 0.034, escala, fontsize=8.4, fontweight='bold', color=C_RED, ha='center')


def draw_elev_shuttered_win(ax, x1, x2, z1, z2, shutters=True):
    """Ventana rústica en elevación con marco de madera, vidrio dividido y contraventanas de lamas."""
    ax.add_patch(Rectangle((x1, z1), x2 - x1, z2 - z1, facecolor='#E1F5FE', edgecolor='#222222', lw=0.80, zorder=4))
    xm, zm = 0.5 * (x1 + x2), 0.5 * (z1 + z2)
    ax.plot([xm, xm], [z1, z2], color='#3E2723', lw=0.85, zorder=5)
    ax.plot([x1, x2], [zm, zm], color='#3E2723', lw=0.65, zorder=5)
    if shutters:
        sw = min(0.32, 0.22 * (x2 - x1))
        for sx in (x1 - sw, x2):
            ax.add_patch(Rectangle((sx, z1), sw, z2 - z1, facecolor='#8D6E63', edgecolor='#222222', lw=0.6, zorder=4))
            for zz in np.linspace(z1 + 0.10, z2 - 0.10, 6):
                ax.plot([sx + 0.03, sx + sw - 0.03], [zz, zz], color='#3E2723', lw=0.42, zorder=5)


def draw_elev_mampara(ax, x1, x2, z1, z2):
    """Mampara corrediza de terraza en elevación (marco madera + 2 hojas cristal + flecha corredera)."""
    ax.add_patch(Rectangle((x1, z1), x2 - x1, z2 - z1, facecolor='#E1F5FE', edgecolor='#4E342E', lw=0.95, zorder=4))
    xm = 0.5 * (x1 + x2)
    ax.plot([xm, xm], [z1, z2], color='#3E2723', lw=1.1, zorder=5)
    ax.annotate('', xy=(xm - 0.18, 0.5 * (z1 + z2)), xytext=(x1 + 0.22, 0.5 * (z1 + z2)),
                arrowprops=dict(arrowstyle='->', color='#0277BD', lw=0.75), zorder=5)


def draw_elev_x_railing(ax, x1, x2, z_floor, h_rail=1.05, n_bays=3):
    """Baranda alpina con Cruces de San Andrés en elevación."""
    ax.add_patch(Rectangle((x1, z_floor), x2 - x1, h_rail, facecolor='none', edgecolor='#4E342E', lw=0.85, zorder=6))
    ax.add_patch(Rectangle((x1, z_floor + h_rail - 0.08), x2 - x1, 0.08, facecolor='#6D4C41', edgecolor='black', lw=0.55, zorder=7))
    dx = (x2 - x1) / n_bays
    for b in range(n_bays):
        bx1, bx2 = x1 + b * dx, x1 + (b + 1) * dx
        ax.plot([bx1, bx1], [z_floor, z_floor + h_rail], color='#4E342E', lw=0.95, zorder=7)
        ax.plot([bx1 + 0.05, bx2 - 0.05], [z_floor + 0.10, z_floor + h_rail - 0.08], color='#5D4037', lw=0.8, zorder=6)
        ax.plot([bx2 - 0.05, bx1 + 0.05], [z_floor + 0.10, z_floor + h_rail - 0.08], color='#5D4037', lw=0.8, zorder=6)


def build_sheet_6_fachadas(pdf):
    fig = plt.figure(figsize=(17, 11), dpi=300)
    draw_sheet_frame_landscape(fig,
                               "PLANO DE FACHADAS Y ELEVACIONES ARQUITECTÓNICAS (3 PISOS + SÓTANO)",
                               "FACHADA PRINCIPAL AV. 4  •  FACHADA POSTERIOR SUR  •  ELEVACIÓN LATERAL CON RAMPA Y CLARABOYA.",
                               escala="1:75 / 1:100", sheet_num="6 / 7")

    # -------------------------------------------------------------------------
    # 1. ARRIBA IZQUIERDA: FACHADA PRINCIPAL AVENIDA 4 (3 PISOS + PORTÓN BODEGA)
    # -------------------------------------------------------------------------
    ax_p = fig.add_axes([0.030, 0.515, 0.450, 0.405])
    ax_p.set_aspect('equal')
    ax_p.set_xlim(-2.6, 12.8)
    ax_p.set_ylim(-2.5, 14.2)
    ax_p.axis('off')

    ax_p.plot([-0.35, 11.75], [0.0, 0.0], color='#111111', lw=1.6, zorder=8)
    # Línea de lindero vecino intacta (X = 0.00..0.15)
    ax_p.add_patch(Rectangle((0.00, 0.00), 0.15, 9.28, facecolor='#E0E0E0', edgecolor='#777777', lw=0.6, linestyle='--', zorder=2))
    ax_p.text(-0.08, 4.60, "Lindero Vecino (0,00m Alero)", rotation=90, fontsize=4.8, color='#555555', ha='right', va='center', bbox=WHITE_HALO, zorder=6)

    # Basamento Planta Baja en Piedra Rústica (Z: 0.00..3.00) + Pórtico Derecho Bodega (X: 9.15..11.37)
    ax_p.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=0.95, zorder=2))
    for sz in np.linspace(0.40, 2.60, 6):
        ax_p.plot([0.15, 9.15], [sz, sz], color='#B0BEC5', lw=0.42, zorder=2)

    # Portón Vehicular Corredizo-Articulado sobre Riel 90° (X: 0.40..2.70; hoja guía visible en 2.36..2.70)
    ax_p.add_patch(Rectangle((0.40, 0.00), 1.96, 2.35, facecolor='#F7F8F9', edgecolor='#222222', lw=0.85, zorder=4))
    ax_p.add_patch(Rectangle((2.36, 0.00), 0.34, 2.35, facecolor='#8D6E63', edgecolor='#222222', lw=0.85, zorder=5))
    ax_p.add_patch(Rectangle((2.41, 1.55), 0.24, 0.60, facecolor='#E1F5FE', edgecolor='#3E2723', lw=0.55, zorder=6))
    ax_p.add_patch(Rectangle((0.35, 2.35), 2.55, 0.10, facecolor='#212121', edgecolor='black', lw=0.65, zorder=6))
    ax_p.text(1.38, 1.15, "PORTÓN CORREDIZO\nRIEL 90° (2,30m)", fontsize=4.7, fontweight='bold',
              color='#222222', ha='center', va='center', bbox=WHITE_HALO, zorder=7)

    # 2 Santamarías de Caracol Completas (X: 3.65..5.75 y 6.20..8.80: carriles U + faldón + tambor espiral)
    for sx1, sx2, slbl in [(3.65, 5.75, "FRUTERÍA 1\nSantamaría\nCaracol"),
                           (6.20, 8.80, "FRUTERÍA 2\nSantamaría\nCaracol")]:
        ax_p.add_patch(Rectangle((sx1, 0.00), sx2 - sx1, 1.98, facecolor='#FFFDF7', edgecolor='#222222', lw=0.85, zorder=4))
        ax_p.add_patch(Rectangle((sx1, 0.00), 0.07, 2.40, facecolor='#212121', edgecolor='black', lw=0.5, zorder=6))
        ax_p.add_patch(Rectangle((sx2 - 0.07, 0.00), 0.07, 2.40, facecolor='#212121', edgecolor='black', lw=0.5, zorder=6))
        ax_p.add_patch(Rectangle((sx1 + 0.05, 1.98), sx2 - sx1 - 0.10, 0.14, facecolor='#90A4AE', edgecolor='#263238', lw=0.6, zorder=5))
        ax_p.add_patch(Rectangle((sx1 + 0.03, 2.12), sx2 - sx1 - 0.06, 0.28, facecolor='#CFD8DC', edgecolor='#263238', lw=0.8, zorder=6))
        ax_p.text(0.5 * (sx1 + sx2), 0.98, slbl, fontsize=4.2, fontweight='bold', color='#1A237E', ha='center', va='center', zorder=6)
    ax_p.add_patch(Rectangle((3.55, 2.52), 5.35, 0.15, facecolor='#6D4C41', edgecolor='black', lw=0.7, zorder=6))

    # Pórtico Derecho Exclusivo hacia Rampa de Bodega (X: 9.15..11.37)
    ax_p.add_patch(Rectangle((9.15, 0.00), 2.22, 2.68, facecolor='#ECEFF1', edgecolor='#222222', lw=0.9, zorder=3))
    ax_p.add_patch(Rectangle((9.35, 0.00), 1.77, 2.35, facecolor='#37474F', edgecolor='black', lw=0.85, zorder=4))
    ax_p.plot([10.235, 10.235], [0.00, 2.35], color='#111111', lw=1.0, zorder=5)
    ax_p.add_patch(Rectangle((9.12, 2.68), 2.28, 0.16, facecolor='#6D4C41', edgecolor='black', lw=0.7, zorder=5))
    ax_p.text(10.24, 1.18, "PORTÓN\nBODEGA", fontsize=4.6, fontweight='bold', color='white', ha='center', va='center', zorder=6)

    # Segundo Piso Social (Z: 3.00..5.85): Balconada Continua + 3 Mamparas Corredizas
    ax_p.add_patch(Rectangle((0.15, 2.85), 9.00, 0.15, facecolor='#90A4AE', edgecolor='black', lw=0.75, zorder=5))
    ax_p.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    for mx1, mx2 in [(0.65, 2.55), (3.15, 5.55), (6.25, 8.65)]:
        draw_elev_mampara(ax_p, mx1, mx2, 3.00, 5.25)
    for px_c in [2.70, 5.80]:
        ax_p.add_patch(Rectangle((px_c, 3.00), 0.25, 2.85, facecolor='#5D4037', edgecolor='black', lw=0.65, zorder=7))
    draw_elev_x_railing(ax_p, 0.35, 2.70, 3.00, h_rail=1.05, n_bays=2)
    draw_elev_x_railing(ax_p, 2.95, 5.80, 3.00, h_rail=1.05, n_bays=3)
    draw_elev_x_railing(ax_p, 6.05, 9.05, 3.00, h_rail=1.05, n_bays=3)

    # Nuevo Tercer Piso Privado (Z: 6.00..8.85): Losa Steel Deck + Terraza Continua (SIN muro pantalla!) + Clerestory UV
    ax_p.add_patch(Rectangle((0.15, 5.85), 9.00, 0.15, facecolor='#263238', edgecolor='black', lw=0.8, zorder=5))
    ax_p.add_patch(Rectangle((0.15, 6.00), 9.00, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    for wz in np.linspace(6.30, 8.15, 6):
        ax_p.plot([0.30, 4.50], [wz, wz], color='#BCAAA4', lw=0.45, zorder=3)
    # Ventana Alta Clerestory UV sobre Vestier (X: 0.95..3.65, Z: 8.35..8.80, 3 paños)
    ax_p.add_patch(Rectangle((0.95, 8.35), 2.70, 0.45, facecolor='#B3E5FC', edgecolor='#3E2723', lw=0.85, zorder=5))
    ax_p.plot([1.85, 1.85], [8.35, 8.80], color='#3E2723', lw=0.75, zorder=6)
    ax_p.plot([2.75, 2.75], [8.35, 8.80], color='#3E2723', lw=0.75, zorder=6)
    # Gran Mampara Master Penthouse (X: 5.25..8.45, Z: 6.00..8.25)
    draw_elev_mampara(ax_p, 5.25, 8.45, 6.00, 8.25)
    # Columnas Metálicas Negras vistas en Terraza Continua P3 + Parapeto Oeste (+9,28 m)
    ax_p.add_patch(Rectangle((0.15, 6.00), 0.18, 3.28, facecolor='#5D4037', edgecolor='black', lw=0.75, zorder=7))
    for sc_x in [2.70, 5.80, 8.95]:
        ax_p.add_patch(Rectangle((sc_x, 6.00), 0.22, 2.85, facecolor=C_STEEL_BLK, edgecolor='black', lw=0.65, zorder=7))
    draw_elev_x_railing(ax_p, 0.35, 2.70, 6.00, h_rail=1.05, n_bays=2)
    draw_elev_x_railing(ax_p, 2.92, 5.80, 6.00, h_rail=1.05, n_bays=3)
    draw_elev_x_railing(ax_p, 6.02, 8.95, 6.00, h_rail=1.05, n_bays=3)

    # Cubierta Alpina 32° sobre P3 (Cumbrera X=4.85, Z=11.70 m; Alero Derecho X=10.10, Z=8.42 m) + Claraboya (+12,60 m)
    gable_poly = [(0.33, 8.85), (0.45, 8.95), (4.85, 11.70), (9.15, 9.01), (9.15, 8.85)]
    ax_p.add_patch(Polygon(gable_poly, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.9, zorder=4))
    ax_p.plot([0.45, 9.15], [8.85, 8.85], color='#4E342E', lw=1.8, zorder=6)
    ax_p.plot([4.85, 4.85], [8.85, 11.68], color='#4E342E', lw=2.0, zorder=6)
    roof_top = [(0.45, 8.95), (4.85, 11.70), (10.10, 8.42), (10.10, 8.62), (4.85, 11.90), (0.45, 9.15)]
    ax_p.add_patch(Polygon(roof_top, closed=True, facecolor='#5D4037', edgecolor='black', lw=0.95, zorder=7))
    # Linterna / Claraboya Ventilada en cumbrera (X: 2.05..5.95, Z: 11.70..12.60)
    ax_p.add_patch(Rectangle((2.45, 10.35), 3.10, 1.95, facecolor='#E1F5FE', edgecolor='#212121', lw=0.75, zorder=3))
    sky_cap = [(2.05, 12.32), (4.00, 12.60), (5.95, 12.32), (5.95, 12.22), (4.00, 12.50), (2.05, 12.22)]
    ax_p.add_patch(Polygon(sky_cap, closed=True, facecolor='#37474F', edgecolor='black', lw=0.8, zorder=8))
    ax_p.text(4.00, 12.75, "Claraboya Ventilada (+12,60m)", fontsize=4.8, fontweight='bold', color='#006064', ha='center')

    for z_lv, z_txt in [(0.00, "±0,00"), (3.00, "+3,00"), (6.00, "+6,00"), (8.85, "+8,85"), (11.70, "+11,70")]:
        ax_p.plot([-0.65, 0.10], [z_lv, z_lv], color='#555555', lw=0.5, linestyle=':')
        ax_p.text(-0.72, z_lv, f"N.P.T. {z_txt}", fontsize=5.0, fontweight='bold', color='#222222', ha='right', va='center')

    draw_dim_h(ax_p, 0.15, 9.15, 13.45, "9,00 (Cuerpo Casa)", fontsize=5.4)
    draw_dim_h(ax_p, 9.15, 11.37, 13.45, "2,22", fontsize=5.2)
    draw_dim_v(ax_p, 11.95, 0.00, 3.00, "3,00", fontsize=5.2, text_side='right')
    draw_dim_v(ax_p, 11.95, 3.00, 6.00, "3,00", fontsize=5.2, text_side='right')
    draw_dim_v(ax_p, 11.95, 6.00, 8.85, "2,85", fontsize=5.2, text_side='right')

    ax_p.text(5.50, -0.80, "FACHADA PRINCIPAL AVENIDA 4\n(PORTÓN BODEGA, COMERCIO, PISO 2 Y PENTHOUSE P3 CON CLERESTORY)",
              fontsize=7.4, fontweight='bold', color='#111111', ha='center', va='top')
    ax_p.plot([0.80, 10.20], [-2.05, -2.05], color='black', lw=1.0)

    # -------------------------------------------------------------------------
    # 2. ARRIBA DERECHA: FACHADA POSTERIOR SUR (SÓTANO BODEGA + 3 PISOS + 2.000L)
    # -------------------------------------------------------------------------
    ax_s = fig.add_axes([0.505, 0.515, 0.465, 0.405])
    ax_s.set_aspect('equal')
    ax_s.set_xlim(-2.4, 12.0)
    ax_s.set_ylim(-4.6, 14.2)
    ax_s.axis('off')

    ax_s.plot([-0.35, 10.9], [-2.55, -2.55], color='#4E342E', lw=1.6, zorder=8)

    # Sótano Bodega Mayorista (Z: -2.55..0.00): 3 ventanas altas seguras + Portón Doble de Carga (6.35..8.55)
    ax_s.add_patch(Rectangle((0.15, -2.55), 9.00, 2.55, facecolor='#CFD8DC', edgecolor='#222222', lw=0.95, zorder=2))
    draw_elev_shuttered_win(ax_s, 0.75, 2.35, -0.90, -0.35, shutters=False)
    draw_elev_shuttered_win(ax_s, 3.25, 4.30, -0.85, -0.35, shutters=False)
    draw_elev_shuttered_win(ax_s, 4.85, 5.75, -0.90, -0.35, shutters=False)
    ax_s.add_patch(Rectangle((6.35, -2.55), 2.20, 2.10, facecolor='#455A64', edgecolor='#111111', lw=1.0, zorder=4))
    ax_s.plot([7.45, 7.45], [-2.55, -0.45], color='#111111', lw=1.2, zorder=5)
    ax_s.text(7.45, -1.50, "PORTÓN CARGA\nBODEGA\n(2,20 m)", fontsize=4.1, fontweight='bold', color='white', ha='center', va='center', bbox=dict(boxstyle='square,pad=0.04', facecolor='#455A64', edgecolor='none'), zorder=6)

    # Planta Baja Sur (Z: 0.00..3.00): Ventana alta Baños + Ventanal Barra Jugos + Ventanal Oficina
    ax_s.add_patch(Rectangle((0.15, 0.00), 9.00, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=0.95, zorder=2))
    draw_elev_shuttered_win(ax_s, 0.75, 2.35, 1.55, 2.25, shutters=False)
    draw_elev_shuttered_win(ax_s, 3.35, 5.45, 0.90, 2.25, shutters=True)
    draw_elev_shuttered_win(ax_s, 6.85, 8.45, 0.95, 2.20, shutters=True)

    # Segundo Piso Sur (Z: 3.00..5.85)
    ax_s.add_patch(Rectangle((0.15, 3.00), 9.00, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    draw_elev_shuttered_win(ax_s, 0.75, 2.35, 4.00, 5.15, shutters=False)
    draw_elev_shuttered_win(ax_s, 3.30, 5.45, 3.85, 5.25, shutters=True)
    draw_elev_shuttered_win(ax_s, 6.60, 8.45, 3.90, 5.15, shutters=True)

    # Tercer Piso Sur (Z: 6.00..8.85): Cuarto Gym Oeste + GRAN TERRAZA MIRADOR & QUINCHO BBQ ABIERTA (X: 2.90..9.15)
    ax_s.add_patch(Rectangle((0.15, 5.85), 9.00, 0.15, facecolor='#263238', edgecolor='black', lw=0.8, zorder=5))
    ax_s.add_patch(Rectangle((0.15, 6.00), 2.75, 2.50, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    draw_elev_shuttered_win(ax_s, 0.85, 2.35, 7.00, 8.10, shutters=False)
    # Fondo abierto de la Terraza Mirador BBQ (Mampara Family Room + Campana BBQ + Columnas Metálicas Negras)
    ax_s.add_patch(Rectangle((2.90, 6.00), 6.25, 2.85, facecolor='#FFFDF9', edgecolor='#4E342E', lw=0.8, zorder=3))
    draw_elev_mampara(ax_s, 3.35, 5.35, 6.00, 8.25)
    ax_s.add_patch(Rectangle((6.20, 6.00), 2.45, 0.92, facecolor='#90A4AE', edgecolor='#263238', lw=0.7, zorder=4))
    ax_s.add_patch(Rectangle((7.55, 7.85), 0.85, 0.65, facecolor='#263238', edgecolor='black', lw=0.7, zorder=5))
    for sc_x in [2.72, 5.82, 8.95]:
        ax_s.add_patch(Rectangle((sc_x, 6.00), 0.22, 2.85, facecolor=C_STEEL_BLK, edgecolor='black', lw=0.7, zorder=7))
    draw_elev_x_railing(ax_s, 2.95, 5.82, 6.00, h_rail=1.05, n_bays=3)
    draw_elev_x_railing(ax_s, 6.04, 8.95, 6.00, h_rail=1.05, n_bays=3)

    # Buhardilla Técnica 2.000 L en P3 (X: 0.15..3.86, Z: 8.68..11.08) + Parapeto (+10,85 m) + Cubierta 32°
    ax_s.add_patch(Rectangle((0.15, 6.00), 0.18, 4.85, facecolor='#5D4037', edgecolor='black', lw=0.8, zorder=7))
    dorm_poly = [(0.33, 8.68), (2.90, 8.68), (2.90, 10.93), (0.33, 10.56)]
    ax_s.add_patch(Polygon(dorm_poly, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.9, zorder=5))
    ax_s.add_patch(Rectangle((0.88, 8.90), 1.45, 1.45, facecolor='#BCAAA4', edgecolor='#3E2723', lw=0.85, zorder=6))
    ax_s.add_patch(Rectangle((1.05, 8.80), 1.00, 1.30, fill=False, edgecolor='#0D47A1', lw=0.75, linestyle='--', zorder=7))
    ax_s.text(1.60, 11.18, "Buhardilla 2.000 L", fontsize=4.8, fontweight='bold', color='#0D47A1', ha='center')

    gable_s = [(2.90, 8.85), (2.90, 10.93), (3.86, 11.08), (4.85, 11.70), (9.15, 9.01), (9.15, 8.85)]
    ax_s.add_patch(Polygon(gable_s, closed=True, facecolor='#D7CCC8', edgecolor='#222222', lw=0.9, zorder=4))
    ax_s.plot([0.40, 3.86], [10.64, 11.16], color='#4E342E', lw=2.0, zorder=7)
    roof_s = [(3.86, 11.08), (4.85, 11.70), (10.10, 8.42), (10.10, 8.62), (4.85, 11.90), (3.86, 11.28)]
    ax_s.add_patch(Polygon(roof_s, closed=True, facecolor='#5D4037', edgecolor='black', lw=0.95, zorder=7))
    ax_s.add_patch(Polygon([(2.05, 12.32), (4.00, 12.60), (5.95, 12.32), (5.95, 12.22), (4.00, 12.50), (2.05, 12.22)],
                           closed=True, facecolor='#37474F', edgecolor='black', lw=0.8, zorder=8))

    for z_lv, z_txt in [(-2.55, "-2,55"), (0.00, "±0,00"), (3.00, "+3,00"), (6.00, "+6,00"), (8.68, "+8,68"), (11.70, "+11,70")]:
        ax_s.plot([-0.60, 0.10], [z_lv, z_lv], color='#555555', lw=0.5, linestyle=':')
        ax_s.text(-0.68, z_lv, f"N.P.T. {z_txt}", fontsize=4.9, fontweight='bold', color='#222222', ha='right', va='center')

    draw_dim_h(ax_s, 0.15, 9.15, 13.45, "9,00", fontsize=5.4)
    draw_dim_v(ax_s, 10.65, -2.55, 0.00, "2,55", fontsize=5.1, text_side='right')
    draw_dim_v(ax_s, 10.65,  0.00, 3.00, "3,00", fontsize=5.1, text_side='right')
    draw_dim_v(ax_s, 10.65,  3.00, 6.00, "3,00", fontsize=5.1, text_side='right')
    draw_dim_v(ax_s, 10.65,  6.00, 8.85, "2,85", fontsize=5.1, text_side='right')

    ax_s.text(4.85, -3.15, "FACHADA POSTERIOR SUR\n(BODEGA SÓTANO, JUGOS P.B., PISO 2, TERRAZA MIRADOR BBQ Y 2.000 L)",
              fontsize=7.4, fontweight='bold', color='#111111', ha='center', va='top')
    ax_s.plot([0.40, 9.30], [-4.32, -4.32], color='black', lw=1.0)

    # -------------------------------------------------------------------------
    # 3. PANEL INFERIOR ANCHO COMPLETO: ELEVACIÓN LATERAL ESTE, RAMPA Y CLARABOYA
    # -------------------------------------------------------------------------
    ax_l = fig.add_axes([0.030, 0.145, 0.940, 0.350])
    ax_l.set_aspect('equal')
    ax_l.set_xlim(-2.2, 28.2)
    ax_l.set_ylim(-4.9, 14.0)
    ax_l.axis('off')

    # Perfil de Rampa Logística Derecha (Y_loc: 0..8.50 a -2.55m -> sube 18% hasta Y_loc=22.50 a ±0.00m -> Av. 4 Y_loc=24.71)
    ramp_y = [0.00, 8.50, 22.50, 25.20]
    ramp_z = [-2.55, -2.55, 0.00, 0.00]
    earth_poly = [(0.00, -3.55)] + list(zip(ramp_y, ramp_z)) + [(25.20, -3.55)]
    ax_l.add_patch(Polygon(earth_poly, closed=True, facecolor='#EFEBE9', edgecolor='none', zorder=1))
    ax_l.plot(ramp_y, ramp_z, color='#1B5E20', lw=2.0, zorder=6)
    ax_l.text(16.6, -2.05, "RAMPA LOGÍSTICA CONTINUA A BODEGA (Pend. 18% desde Portón Der. Av. 4)",
              fontsize=6.0, fontweight='bold', color='#1B5E20', ha='center', bbox=WHITE_HALO, zorder=7)
    ax_l.text(1.50, -1.75, "Patio Maniobra\n(-2,55 m)", fontsize=5.2, fontweight='bold', color='#3E2723', ha='center', bbox=WHITE_HALO, zorder=7)

    # Nivel Sótano Bodega Este (Y_loc: 3.00..11.30, Z: -2.55..0.00)
    ax_l.add_patch(Rectangle((3.00, -2.55), 8.30, 2.55, facecolor='#CFD8DC', edgecolor='#222222', lw=0.95, zorder=2))
    for wy1, wy2 in [(4.00, 5.65), (7.20, 8.85), (9.95, 11.00)]:
        draw_elev_shuttered_win(ax_l, wy1, wy2, -0.90, -0.35, shutters=False)

    # Planta Baja Este (Y_loc: 3.00..24.71, Z: 0.00..3.00) con sus 7 ventanas
    ax_l.add_patch(Rectangle((3.00, 0.00), 21.71, 3.00, facecolor='#ECEFF1', edgecolor='#222222', lw=0.95, zorder=2))
    for wy1, wy2 in [(4.10, 5.50), (7.10, 8.00), (9.30, 11.00), (12.65, 14.85), (16.15, 17.05), (18.50, 20.70), (21.80, 24.00)]:
        draw_elev_shuttered_win(ax_l, wy1, wy2, 1.00, 2.15, shutters=False)

    # Segundo Piso Social Este (Y_loc: 3.00..24.71, Z: 3.00..5.85) + Balconada Norte (22.60..24.71)
    ax_l.add_patch(Rectangle((3.00, 2.85), 21.71, 0.15, facecolor='#90A4AE', edgecolor='black', lw=0.7, zorder=4))
    ax_l.add_patch(Rectangle((3.00, 3.00), 19.60, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    for wy1, wy2, sh in [(4.10, 6.05, True), (8.15, 9.35, False), (11.45, 14.35, True), (15.35, 17.75, True), (19.00, 21.60, True)]:
        draw_elev_shuttered_win(ax_l, wy1, wy2, 3.90, 5.20, shutters=sh)
    ax_l.add_patch(Rectangle((22.60, 3.00), 2.11, 2.85, facecolor='#FFFDF9', edgecolor='#4E342E', lw=0.8, zorder=3))
    draw_elev_x_railing(ax_l, 22.60, 24.71, 3.00, h_rail=1.05, n_bays=2)

    # Tercer Piso Este (Z: 6.00..8.85): Terraza Mirador BBQ Sur (3.00..7.30) + Cuerpo Central + Terraza Continua Norte (22.60..24.71)
    ax_l.add_patch(Rectangle((3.00, 5.85), 21.71, 0.15, facecolor='#263238', edgecolor='black', lw=0.75, zorder=4))
    # Esquina Sur abierta: Terraza Mirador BBQ (Y_loc: 3.00..7.30)
    ax_l.add_patch(Rectangle((3.00, 6.00), 4.30, 2.85, facecolor='#FFFDF9', edgecolor='#4E342E', lw=0.8, zorder=3))
    draw_elev_x_railing(ax_l, 3.00, 7.30, 6.00, h_rail=1.05, n_bays=3)
    for sc_y in [3.02, 6.48]:
        ax_l.add_patch(Rectangle((sc_y, 6.00), 0.22, 2.85, facecolor=C_STEEL_BLK, edgecolor='black', lw=0.65, zorder=6))
    # Cuerpo central cerrado P3 (Y_loc: 7.30..22.60) con 4 ventanas Este
    ax_l.add_patch(Rectangle((7.30, 6.00), 15.30, 2.85, facecolor='#EFEBE9', edgecolor='#222222', lw=0.95, zorder=3))
    for wy1, wy2, sh in [(7.90, 8.85, False), (10.35, 12.25, True), (14.40, 16.45, True), (18.75, 21.45, True)]:
        draw_elev_shuttered_win(ax_l, wy1, wy2, 6.90, 8.15, shutters=sh)
    # Terraza Continua Master Norte (Y_loc: 22.60..24.71)
    ax_l.add_patch(Rectangle((22.60, 6.00), 2.11, 2.85, facecolor='#FFFDF9', edgecolor='#4E342E', lw=0.8, zorder=3))
    draw_elev_x_railing(ax_l, 22.60, 24.71, 6.00, h_rail=1.05, n_bays=2)
    ax_l.add_patch(Rectangle((24.49, 6.00), 0.22, 2.85, facecolor=C_STEEL_BLK, edgecolor='black', lw=0.65, zorder=6))

    # Cubierta Chalet P3 vista longitudinalmente (Y_loc: 2.00..24.96, Z: 8.42..11.88) + Canecillos
    ax_l.add_patch(Rectangle((2.00, 8.62), 22.96, 3.26, facecolor='#795548', edgecolor='#222222', lw=0.95, zorder=4))
    for r_z in np.linspace(9.05, 11.55, 7):
        ax_l.plot([2.00, 24.96], [r_z, r_z], color='#5D4037', lw=0.45, zorder=4)
    ax_l.add_patch(Rectangle((2.00, 8.42), 22.96, 0.20, facecolor='#4E342E', edgecolor='black', lw=0.75, zorder=6))
    for cy_r in np.linspace(2.35, 24.55, 19):
        ax_l.add_patch(Rectangle((cy_r - 0.06, 8.26), 0.12, 0.16, facecolor='#3E2723', edgecolor='black', lw=0.42, zorder=6))

    # Linterna / Claraboya Central Ventilada (Y_loc: 8.50..14.30 = 5,80 m; Z: 11.88..12.60 m)
    ax_l.add_patch(Rectangle((8.50, 11.88), 5.80, 0.52, facecolor='#B3E5FC', edgecolor='#212121', lw=0.8, zorder=5))
    for py_s in [8.50, 10.43, 12.37, 14.30]:
        ax_l.plot([py_s, py_s], [11.88, 12.40], color='#212121', lw=1.0, zorder=6)
    ax_l.add_patch(Rectangle((8.15, 12.40), 6.50, 0.20, facecolor='#37474F', edgecolor='black', lw=0.8, zorder=7))
    ax_l.text(11.40, 12.78, "Claraboya Ventilada (5,80 m)", fontsize=5.1, fontweight='bold', color='#006064', ha='center')

    # Cotas Longitudinales y Verticales
    draw_dim_h(ax_l, 0.00,  3.00, 13.35, "3,00 (Patio)", fontsize=5.4)
    draw_dim_h(ax_l, 3.00, 24.71, 13.35, "21,71 (Largo Edificación)", fontsize=5.6)
    draw_dim_v(ax_l, -0.75, -2.55, 0.00, "2,55", x_ref=0.00, fontsize=5.2)
    draw_dim_v(ax_l, -0.75,  0.00, 8.85, "8,85 (3 Pisos)", x_ref=3.00, fontsize=5.2)
    draw_dim_v(ax_l, 25.55,  0.00, 11.88, "11,88 (Cumbrera)", x_ref=24.96, fontsize=5.2, text_side='right')
    ax_l.text(26.95, 0.85, "AVENIDA 4\n(±0,00 m)", fontsize=5.6, fontweight='bold', color=C_RED, ha='center')

    ax_l.text(13.5, -3.85, "ELEVACIÓN LATERAL ESTE — SÓTANO BODEGA, 3 PISOS, TERRAZA MIRADOR, CLARABOYA Y RAMPA LOGÍSTICA",
              fontsize=8.0, fontweight='bold', color='#111111', ha='center', va='top')
    ax_l.plot([2.50, 24.50], [-4.52, -4.52], color='black', lw=1.1)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# LÁMINA 7/7: LEVANTAMIENTO POLIGONAL DE LINDEROS, RETÍCULA U.T.M. Y ÁREAS
# =============================================================================
def build_sheet_7_terreno_utm(pdf):
    fig = plt.figure(figsize=(11, 17), dpi=300)
    draw_sheet_frame(fig,
                     "LEVANTAMIENTO POLIGONAL DE LINDEROS",
                     "COORDENADAS U.T.M., CUADRO DE ÁREAS (3 PISOS + BODEGA), IMPLANTACIÓN Y SITUACIÓN.",
                     escala="1:200", sheet_num="7 / 7")

    ax_bg = fig.axes[0]
    ax_bg.plot([0.022, 0.978], [0.718, 0.718], color=C_BLUE, lw=1.6)

    # 1. ARRIBA IZQUIERDA: CUADRO DE COORDENADAS U.T.M. + CUADRO DE ÁREAS ACTUALIZADO
    ax_utmtbl = fig.add_axes([0.032, 0.798, 0.425, 0.138])
    ax_utmtbl.set_xlim(0, 1)
    ax_utmtbl.set_ylim(0, 1)
    ax_utmtbl.axis('off')

    ax_utmtbl.add_patch(Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=C_BLUE, lw=1.5))
    ax_utmtbl.plot([0, 1], [0.82, 0.82], color=C_BLUE, lw=1.1)
    ax_utmtbl.text(0.50, 0.91, "CUADRO DE COORDENADAS U.T.M.", fontsize=7.8,
                   fontweight='bold', color=C_RED, ha='center', va='center')

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

    # Cuadro de Áreas Oficial Actualizado a 3 Pisos + Sótano Bodega + Buhardilla 2.000 L
    ax_ar = fig.add_axes([0.032, 0.726, 0.425, 0.064])
    ax_ar.set_xlim(0, 1)
    ax_ar.set_ylim(0, 1)
    ax_ar.axis('off')
    ax_ar.add_patch(Rectangle((0, 0), 1, 1, facecolor='#FFFDE7', edgecolor=C_BLUE, lw=1.2))
    ax_ar.text(0.025, 0.75, "ÁREA DE TERRENO POLIGONAL: 273,81 m².",
               fontsize=7.0, fontweight='bold', color=C_RED, va='center')
    ax_ar.text(0.025, 0.45, "ÁREA TOTAL CONSTRUIDA TECHADA: 673,11 m²  (+ Rampa y Patio Maniobra).",
               fontsize=6.5, fontweight='bold', color=C_RED, va='center')
    ax_ar.text(0.025, 0.16, "Sótano 74,70 | P.B. 195,39 | 2do Piso 195,39 | 3er Piso 195,39 | Buhardilla 12,24 m²",
               fontsize=5.2, fontweight='bold', color='#263238', va='center')

    # 2. ARRIBA CENTRO: CUADRO DE LINDEROS
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

    # 3. ARRIBA DERECHA: CROQUIS DE SITUACIÓN RELATIVA S/ESC.
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

    u_intervals = [(-9.5, -3.2), (-2.1, 3.3), (4.4, 10.2)]
    v_intervals = [(-6.8, -2.0), (-1.1, 1.3), (2.5, 7.2)]
    for u1, u2 in u_intervals:
        for v1, v2 in v_intervals:
            pts_b = [rot_pt(u1, v1), rot_pt(u2, v1), rot_pt(u2, v2), rot_pt(u1, v2)]
            ax_sit.add_patch(Polygon(pts_b, closed=True, facecolor='#EFEFEF', edgecolor='#333333', lw=0.8, zorder=2))

    lot_sit_pts = [rot_pt(0.55, -2.00), rot_pt(1.25, -2.00), rot_pt(1.25, -3.25), rot_pt(0.55, -3.25)]
    ax_sit.add_patch(Polygon(lot_sit_pts, closed=True, facecolor=C_BLUE, edgecolor='#000066', lw=1.0, zorder=5))

    lx, ly = rot_pt(-0.8, 1.90)
    ax_sit.text(lx, ly, "Av. LIBERTADOR", rotation=38, fontsize=5.8, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    lx2, ly2 = rot_pt(0.3, -1.55)
    ax_sit.text(lx2, ly2, "AVENIDA 4", rotation=38, fontsize=5.3, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx1, sy1 = rot_pt(3.85, 2.2)
    ax_sit.text(sx1, sy1, "Calle 29", rotation=-52, fontsize=5.1, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx2, sy2 = rot_pt(-2.65, 0.2)
    ax_sit.text(sx2, sy2, "Calle 30", rotation=-52, fontsize=5.1, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)
    sx3, sy3 = rot_pt(-2.15, -2.15)
    ax_sit.text(sx3, sy3, "Calle 31", rotation=-52, fontsize=5.0, fontweight='bold', color=C_RED, ha='center', va='center', clip_on=True, zorder=6)

    ax_bg.text(0.968, 0.730, "SITUACIÓN RELATIVA S/ESC.", fontsize=7.0, fontweight='bold', color=C_BLUE, ha='right', va='center')

    # 4. PLANO PRINCIPAL DE LEVANTAMIENTO POLIGONAL Y HUELLA EN RETÍCULA U.T.M.
    ax_u = fig.add_axes([0.025, 0.100, 0.950, 0.614])
    ax_u.set_aspect('equal')
    ax_u.set_xlim(529740.5, 529793.5)
    ax_u.set_ylim(1141631.5, 1141684.5)
    ax_u.axis('off')

    for n_val in [1141640, 1141650, 1141660, 1141670, 1141680]:
        ax_u.plot([529740.5, 529793.5], [n_val, n_val], color='#888888', lw=0.55, zorder=1)
        n_num = f"{n_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ax_u.text(529740.8, n_val + 0.35, f"N.={n_num}", fontsize=7.6, fontweight='bold', color='#111111', ha='left', va='bottom', zorder=8)

    for e_val in [529750, 529760, 529770, 529780, 529790]:
        ax_u.plot([e_val, e_val], [1141631.5, 1141684.5], color='#888888', lw=0.55, zorder=1)
        e_num = f"{e_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ax_u.text(e_val - 0.35, 1141632.2, f"E.={e_num}", rotation=90, fontsize=7.6, fontweight='bold', color='#111111', ha='right', va='bottom', zorder=8)

    P1 = (529755.04, 1141664.17)
    P2 = (529764.60, 1141670.33)
    P3 = (529777.07, 1141648.99)
    P4 = (529767.99, 1141643.13)

    ux_e, ux_n =  0.851615, 0.524164
    uy_e, uy_n = -0.524164, 0.851615

    def loc_to_utm(xl, yl):
        return (P4[0] + xl * ux_e + yl * uy_e, P4[1] + xl * ux_n + yl * uy_n)

    av4_s1 = [loc_to_utm(-20.0, 24.71), P1, P2, loc_to_utm(22.8, 25.18), loc_to_utm(38.0, 0.50)]
    av4_s2 = [loc_to_utm(-20.0, 26.20), loc_to_utm(21.8, 26.90), loc_to_utm(36.8, 2.50)]
    for seq in (av4_s1, av4_s2):
        xs_c, ys_c = zip(*seq)
        ax_u.plot(xs_c, ys_c, color='#444444', lw=0.65, zorder=2)

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

    # Poligonal Oficial de Linderos en Rojo
    ax_u.add_patch(Polygon([P1, P2, P3, P4], closed=True, facecolor='#FFFDF5', edgecolor=C_RED, lw=1.4, zorder=3))

    # Patio de Maniobra Sur (X_loc: 4.50..9.15, Y_loc: 0.50..3.00) + Rampa Derecha desde Portón Av. 4
    patio_pts = [loc_to_utm(4.50, 0.50), loc_to_utm(9.15, 0.50), loc_to_utm(9.15, 3.00), loc_to_utm(4.50, 3.00)]
    ax_u.add_patch(Polygon(patio_pts, closed=True, facecolor=C_STONE_SOFT, edgecolor='#455A64', lw=0.75, hatch='++', zorder=4))

    ramp_pts = [loc_to_utm(9.15, 3.00), loc_to_utm(10.65, 3.00), loc_to_utm(11.22, 24.92), loc_to_utm(9.15, 24.71)]
    ax_u.add_patch(Polygon(ramp_pts, closed=True, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.8, hatch='---', zorder=4))

    # Huella Exacta de la Edificación de 3 Pisos (X_loc: 0.15..9.15, Y_loc: 3.00..24.71)
    bldg_w_pts = [loc_to_utm(0.15, 3.00), loc_to_utm(4.85, 3.00), loc_to_utm(4.85, 24.71), loc_to_utm(0.15, 24.71)]
    bldg_e_pts = [loc_to_utm(4.85, 3.00), loc_to_utm(9.15, 3.00), loc_to_utm(9.15, 24.71), loc_to_utm(4.85, 24.71)]
    ax_u.add_patch(Polygon(bldg_w_pts, closed=True, facecolor='#E0E0E0', edgecolor='#111111', lw=0.95, hatch='///', zorder=4))
    ax_u.add_patch(Polygon(bldg_e_pts, closed=True, facecolor='#ECEFF1', edgecolor='#111111', lw=0.95, hatch='\\\\\\', zorder=4))

    # Claraboya Central Ventilada en Cubierta P3 (X_loc: 2.45..5.55, Y_loc: 8.50..14.30)
    sky_pts = [loc_to_utm(2.45, 8.50), loc_to_utm(5.55, 8.50), loc_to_utm(5.55, 14.30), loc_to_utm(2.45, 14.30)]
    ax_u.add_patch(Polygon(sky_pts, closed=True, facecolor='#B2EBF2', edgecolor='#006064', lw=0.9, alpha=0.85, zorder=5))

    # Buhardilla Técnica Reserva 2.000 L (X_loc: 0.15..2.90, Y_loc: 3.00..7.45)
    buh_pts = [loc_to_utm(0.15, 3.00), loc_to_utm(2.90, 3.00), loc_to_utm(2.90, 7.45), loc_to_utm(0.15, 7.45)]
    ax_u.add_patch(Polygon(buh_pts, closed=True, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=0.9, alpha=0.80, zorder=5))

    # Proyección punteada del Alero Derecho Propio (X_loc = 10.10 m)
    eave_p1, eave_p2 = loc_to_utm(10.10, 2.00), loc_to_utm(10.10, 24.71)
    ax_u.plot([eave_p1[0], eave_p2[0]], [eave_p1[1], eave_p2[1]], color='#5D4037', lw=0.85, linestyle='--', zorder=5)

    # Vértices P-1..P-4
    v_labels = [
        (P1, "P-1", (-1.55, -0.15)),
        (P2, "P-2", ( 0.05,  1.25)),
        (P3, "P-3", ( 1.45, -0.10)),
        (P4, "P-4", (-0.95, -1.35)),
    ]
    for (vx, vy), v_name, (dx_l, dy_l) in v_labels:
        ax_u.add_patch(Circle((vx, vy), 0.30, facecolor='white', edgecolor='#111111', lw=1.0, zorder=7))
        ax_u.text(vx + dx_l, vy + dy_l, v_name, fontsize=9.0, fontweight='bold', color='#111111', ha='center', va='center', zorder=8)

    # Cotas de Linderos
    m12 = (0.5 * (P1[0] + P2[0]) - 0.65, 0.5 * (P1[1] + P2[1]) + 0.95)
    m23 = (0.5 * (P2[0] + P3[0]) + 0.95, 0.5 * (P2[1] + P3[1]) + 0.55)
    m34 = (0.5 * (P3[0] + P4[0]) + 0.55, 0.5 * (P3[1] + P4[1]) - 0.95)
    m41 = (0.5 * (P4[0] + P1[0]) - 1.05, 0.5 * (P4[1] + P1[1]) - 0.55)
    ax_u.text(*m12, "11,37 m", rotation=32.8, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m23, "24,72 m", rotation=-59.7, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m34, "10,81 m", rotation=32.8, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)
    ax_u.text(*m41, "24,70 m", rotation=-58.4, fontsize=6.6, fontweight='bold', color=C_RED, ha='center', va='center', bbox=WHITE_HALO, zorder=8)

    # Nombres de Calles y Vecinos Colindantes
    ax_u.text(529756.8, 1141672.0, "AVENIDA 4.", rotation=32.8, fontsize=8.8, fontweight='bold', color='#111111', ha='center', va='center')
    ax_u.text(529783.5, 1141676.0, "CALLE 30.", rotation=-58.0, fontsize=8.4, fontweight='bold', color='#111111', ha='center', va='center')
    ax_u.text(529776.2, 1141659.8, "CASA\nDE\nMIGUEL RODRIGUEZ.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')
    ax_u.text(529774.8, 1141641.8, "SOLAR\nDE\nMIGUEL RODRIGUEZ.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')
    ax_u.text(529756.8, 1141650.2, "CASA\nDE\nMARIO GRATEROL.", rotation=32.8, fontsize=7.2, color='#222222', ha='center', va='center')

    draw_north(ax_u, 529788.8, 1141680.2, r=1.55)

    # Leyenda de Implantación actualizada a 3 pisos + claraboya + rampa
    leg_box = Rectangle((529779.8, 1141639.2), 13.0, 10.4, facecolor='white', edgecolor=C_BLUE, lw=0.9, alpha=0.96, zorder=9)
    ax_u.add_patch(leg_box)
    ax_u.text(529786.3, 1141648.6, "LEYENDA DE IMPLANTACIÓN", fontsize=5.7, fontweight='bold', color=C_RED, ha='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.3, 1141646.6), 1.3, 0.85, facecolor='#E0E0E0', edgecolor='black', lw=0.6, hatch='///', zorder=10))
    ax_u.text(529782.0, 1141647.02, "Edificación 3 Pisos (9,00x21,71m)", fontsize=4.9, color='#111111', va='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.3, 1141645.1), 1.3, 0.85, facecolor='#B2EBF2', edgecolor='#006064', lw=0.6, zorder=10))
    ax_u.text(529782.0, 1141645.52, "Claraboya Ventilada (3,10x5,80m)", fontsize=4.9, color='#111111', va='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.3, 1141643.6), 1.3, 0.85, facecolor='#BBDEFB', edgecolor='#0D47A1', lw=0.6, zorder=10))
    ax_u.text(529782.0, 1141644.02, "Buhardilla Tanques 2.000 L", fontsize=4.9, color='#111111', va='center', zorder=10)
    ax_u.add_patch(Rectangle((529780.3, 1141642.1), 1.3, 0.85, facecolor='#E8F5E9', edgecolor='#2E7D32', lw=0.6, hatch='---', zorder=10))
    ax_u.text(529782.0, 1141642.52, "Rampa Derecha + Patio Bodega", fontsize=4.9, color='#111111', va='center', zorder=10)
    ax_u.plot([529780.3, 529781.6], [1141640.5, 1141640.5], color='#5D4037', lw=0.9, linestyle='--', zorder=10)
    ax_u.text(529782.0, 1141640.5, "Alero Derecho (0,95 m propio)", fontsize=4.9, color='#111111', va='center', zorder=10)

    pdf.savefig(fig)
    plt.close(fig)


# =============================================================================
# EJECUCIÓN PRINCIPAL DEL PORTAFOLIO ARQUITECTÓNICO PDF (7 LÁMINAS)
# =============================================================================
def main():
    output_pdf = os.path.join("01_Planos_y_Documentacion", "planos_casa_3_pisos.pdf")
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    print(f"Generando portafolio oficial de 7 laminas: {output_pdf} ...")

    with PdfPages(output_pdf) as pdf:
        build_sheet_1_sotano(pdf)
        print("  [1/7] Nivel Sotano: Gran Bodega Mayorista y Patio de Maniobra completado.")
        build_sheet_2_planta_baja(pdf)
        print("  [2/7] Planta Baja: Fruteria Ampliada, Jugos, Oficina, Garaje y Rampa completado.")
        build_sheet_3_segundo_piso(pdf)
        print("  [3/7] Segundo Piso Social: Mamparas, Isla, Nevera y Despensa Bajo Escalera completado.")
        build_sheet_4_tercer_piso(pdf)
        print("  [4/7] Nuevo Tercer Piso: Penthouse, Claraboya, Terraza BBQ y Buhardilla 2.000 L completado.")
        build_sheet_5_columnas_estructura(pdf)
        print("  [5/7] Distribucion de Columnas, Acero Negro P3 y Ejes Estructurales completado.")
        build_sheet_6_fachadas(pdf)
        print("  [6/7] Fachadas Arquitectonicas de 3 Pisos, Rampa y Claraboya completado.")
        build_sheet_7_terreno_utm(pdf)
        print("  [7/7] Levantamiento Poligonal de Linderos y Reticula U.T.M. completado.")

    print(f"EXITO! Portafolio PDF generado correctamente en: {output_pdf}")


if __name__ == "__main__":
    main()
