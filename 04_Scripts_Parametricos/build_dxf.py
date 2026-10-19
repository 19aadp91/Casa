"""
Generador del archivo DXF (2D y 3D) de la vivienda
Ubicacion: Av. 4 entre calles 30 y 31, Yaracuy
Autor: Arquitecto Virtual Gemini + CADCraft
"""

import math

def generate_house_dxf(output_path):
    boxes_3d = []  # List of tuples: (layer, color, x1, y1, z1, x2, y2, z2)
    lines_2d = []  # List of tuples: (layer, color, x1, y1, z1, x2, y2, z2)
    texts = []     # List of tuples: (layer, color, text, x, y, z, height)

    # Parametros Globales
    W_X = 9.25
    L_Y = 15.15
    H_WALL = 2.80
    T_EXT = 0.20
    T_INT = 0.15
    SLAB_T = 0.15
    H_DOOR = 2.10
    W_SILL = 1.00
    W_H = 1.10
    B_SILL = 1.80
    B_H = 0.40
    H_ROOF_PARAPET = 0.45

    def add_box(layer, color, x1, y1, z1, x2, y2, z2):
        boxes_3d.append((layer, color, min(x1, x2), min(y1, y2), min(z1, z2),
                                       max(x1, x2), max(y1, y2), max(z1, z2)))

    def add_line(layer, color, x1, y1, z1, x2, y2, z2):
        lines_2d.append((layer, color, x1, y1, z1, x2, y2, z2))

    def add_text(layer, color, text, x, y, z, height=0.30):
        texts.append((layer, color, text, x, y, z, height))

    # =========================================================================
    # 1. LOSA DE PISO (Z = -0.15 a 0.00)
    # Hueco escalera: X in [0.20, 1.45], Y in [4.45, 7.40]
    # =========================================================================
    LAYER_SLAB = "LOSA_PISO_3D"
    COLOR_SLAB = 8  # Gris

    add_box(LAYER_SLAB, COLOR_SLAB, 0.00, 0.00, -SLAB_T, W_X, 4.45, 0.00)
    add_box(LAYER_SLAB, COLOR_SLAB, 0.00, 7.40, -SLAB_T, W_X, L_Y, 0.00)
    add_box(LAYER_SLAB, COLOR_SLAB, 1.45, 4.45, -SLAB_T, W_X, 7.40, 0.00)
    add_box(LAYER_SLAB, COLOR_SLAB, 0.00, 4.45, -SLAB_T, 0.20, 7.40, 0.00)

    # Peldanos de la escalera al sotano (10 escalones visibles)
    for i in range(10):
        y_step = 7.40 - i * (2.95 / 10.0)
        z_step = 0.00 - (i + 1) * (1.40 / 10.0)
        add_box("ESCALERA_3D", 7, 0.20, y_step - (2.95 / 10.0), z_step, 1.45, y_step, z_step + 0.14)
        add_line("ESCALERA_2D", 7, 0.20, y_step, 0.0, 1.45, y_step, 0.0)

    # =========================================================================
    # 2. MUROS EXTERIORES (Espesor 0.20 m)
    # =========================================================================
    LAYER_EXT = "MUROS_EXTERIORES_3D"
    COLOR_EXT = 7  # Blanco/Negro segun fondo

    # Muro Oeste (Lateral Izquierdo) continuo
    add_box(LAYER_EXT, COLOR_EXT, 0.00, 0.00, 0.00, 0.20, L_Y, H_WALL)

    # Muro Sur (Posterior): Puerta Lavadero Ext, Ventana Hab4, Ventana Bano2
    # P_Lavadero_Ext: X in [0.80, 1.80]
    # V_Hab4: X in [3.70, 5.60]
    # V_B2: X in [7.00, 7.90]
    add_box(LAYER_EXT, COLOR_EXT, 0.20, 0.00, 0.00, 0.80, 0.20, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, 0.80, 0.00, H_DOOR, 1.80, 0.20, H_WALL)  # Dintel puerta
    add_box(LAYER_EXT, COLOR_EXT, 1.80, 0.00, 0.00, 3.70, 0.20, H_WALL)
    # V_Hab4
    add_box(LAYER_EXT, COLOR_EXT, 3.70, 0.00, 0.00, 5.60, 0.20, W_SILL)   # Antepecho
    add_box(LAYER_EXT, COLOR_EXT, 3.70, 0.00, W_SILL + W_H, 5.60, 0.20, H_WALL)  # Dintel
    add_box(LAYER_EXT, COLOR_EXT, 5.60, 0.00, 0.00, 7.00, 0.20, H_WALL)
    # V_B2
    add_box(LAYER_EXT, COLOR_EXT, 7.00, 0.00, 0.00, 7.90, 0.20, B_SILL)   # Antepecho
    add_box(LAYER_EXT, COLOR_EXT, 7.00, 0.00, B_SILL + B_H, 7.90, 0.20, H_WALL)  # Dintel
    add_box(LAYER_EXT, COLOR_EXT, 7.90, 0.00, 0.00, 9.05, 0.20, H_WALL)

    # Muro Este (Lateral Derecho): Ventanas de Hab3, Hab2, Bano1, Hab1
    # Y=0.00 a 15.15
    # V_B2_Lat: Y in [0.50, 1.40]
    # V_Hab3_Lat: Y in [2.60, 4.80]
    # V_Hab2_Lat: Y in [6.20, 8.40]
    # V_B1_Lat: Y in [9.70, 10.60]
    # V_Hab1_Lat: Y in [12.00, 14.20]
    x_e1, x_e2 = 9.05, 9.25
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 0.00, 0.00, x_e2, 0.50, H_WALL)
    # V_B2_Lat
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 0.50, 0.00, x_e2, 1.40, B_SILL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 0.50, B_SILL + B_H, x_e2, 1.40, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 1.40, 0.00, x_e2, 2.60, H_WALL)
    # V_Hab3_Lat
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 2.60, 0.00, x_e2, 4.80, W_SILL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 2.60, W_SILL + W_H, x_e2, 4.80, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 4.80, 0.00, x_e2, 6.20, H_WALL)
    # V_Hab2_Lat
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 6.20, 0.00, x_e2, 8.40, W_SILL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 6.20, W_SILL + W_H, x_e2, 8.40, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 8.40, 0.00, x_e2, 9.70, H_WALL)
    # V_B1_Lat
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 9.70, 0.00, x_e2, 10.60, B_SILL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 9.70, B_SILL + B_H, x_e2, 10.60, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 10.60, 0.00, x_e2, 12.00, H_WALL)
    # V_Hab1_Lat
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 12.00, 0.00, x_e2, 14.20, W_SILL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 12.00, W_SILL + W_H, x_e2, 14.20, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, x_e1, 14.20, 0.00, x_e2, L_Y, H_WALL)

    # Muro Norte (Fachada Frontal):
    # Porton Garaje: X in [0.20, 2.80]
    add_box(LAYER_EXT, COLOR_EXT, 0.20, 14.95, 2.50, 2.80, L_Y, H_WALL)  # Viga sobre porton
    # Viga dintel frontal del Porche: X in [2.80, 5.90]
    add_box(LAYER_EXT, COLOR_EXT, 2.80, 14.95, 2.40, 5.90, L_Y, H_WALL)
    # Fachada Hab1: X in [5.90, 9.05], Ventana X in [6.50, 8.70]
    add_box(LAYER_EXT, COLOR_EXT, 5.90, 14.95, 0.00, 6.50, L_Y, H_WALL)
    add_box(LAYER_EXT, COLOR_EXT, 6.50, 14.95, 0.00, 8.70, L_Y, W_SILL)  # Antepecho
    add_box(LAYER_EXT, COLOR_EXT, 6.50, 14.95, W_SILL + W_H, 8.70, L_Y, H_WALL)  # Dintel
    add_box(LAYER_EXT, COLOR_EXT, 8.70, 14.95, 0.00, 9.05, L_Y, H_WALL)

    # =========================================================================
    # 3. MUROS INTERIORES (Espesor 0.15 m)
    # =========================================================================
    LAYER_INT = "MUROS_INTERIORES_3D"
    COLOR_INT = 7

    # Muro Longitudinal Eje 1 (X in [2.80, 2.95])
    # Separa Garaje/Servicio de Sala/Comedor/Hab4 (Y: 0.20 a 12.90)
    # P_Cocina: Y in [3.20, 4.00]
    # P_Garaje_Sala: Y in [9.50, 10.40]
    x1_1, x2_1 = 2.80, 2.95
    add_box(LAYER_INT, COLOR_INT, x1_1, 0.20, 0.00, x2_1, 3.20, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_1, 3.20, H_DOOR, x2_1, 4.00, H_WALL) # Dintel P_Cocina
    add_box(LAYER_INT, COLOR_INT, x1_1, 4.00, 0.00, x2_1, 4.45, H_WALL)
    # Entre 4.45 y 7.40 es el tramo de escalera / paso
    add_box(LAYER_INT, COLOR_INT, x1_1, 7.40, 0.00, x2_1, 9.50, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_1, 9.50, H_DOOR, x2_1, 10.40, H_WALL) # Dintel P_Garaje
    add_box(LAYER_INT, COLOR_INT, x1_1, 10.40, 0.00, x2_1, 12.90, H_WALL)

    # Muro Longitudinal Eje 2 (X in [5.90, 6.05])
    # Separa Sala/Comedor de crujia Habitaciones (Y: 3.55 a 14.95)
    # P_B2: Y in [1.00, 1.70] (en zona fondo)
    # P_Hab3: Y in [4.30, 5.00]
    # P_Hab2: Y in [8.10, 8.80]
    # P_B1: Y in [9.80, 10.50]
    # P_Hab1: Y in [11.50, 12.20]
    x1_2, x2_2 = 5.90, 6.05
    add_box(LAYER_INT, COLOR_INT, x1_2, 0.20, 0.00, x2_2, 1.00, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_2, 1.00, H_DOOR, x2_2, 1.70, H_WALL) # Dintel P_B2
    add_box(LAYER_INT, COLOR_INT, x1_2, 1.70, 0.00, x2_2, 4.30, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_2, 4.30, H_DOOR, x2_2, 5.00, H_WALL) # Dintel P_Hab3
    add_box(LAYER_INT, COLOR_INT, x1_2, 5.00, 0.00, x2_2, 8.10, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_2, 8.10, H_DOOR, x2_2, 8.80, H_WALL) # Dintel P_Hab2
    add_box(LAYER_INT, COLOR_INT, x1_2, 8.80, 0.00, x2_2, 9.80, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_2, 9.80, H_DOOR, x2_2, 10.50, H_WALL) # Dintel P_B1
    add_box(LAYER_INT, COLOR_INT, x1_2, 10.50, 0.00, x2_2, 11.50, H_WALL)
    add_box(LAYER_INT, COLOR_INT, x1_2, 11.50, H_DOOR, x2_2, 12.20, H_WALL) # Dintel P_Hab1
    add_box(LAYER_INT, COLOR_INT, x1_2, 12.20, 0.00, x2_2, 14.95, H_WALL)

    # Muros Transversales:
    # 1. Lavadero - Cocina: Y in [1.70, 1.85], X in [0.20, 2.80]
    # P_Lavadero_Int: X in [0.50, 1.30]
    add_box(LAYER_INT, COLOR_INT, 0.20, 1.70, 0.00, 0.50, 1.85, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 0.50, 1.70, H_DOOR, 1.30, 1.85, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 1.30, 1.70, 0.00, 2.80, 1.85, H_WALL)

    # 2. Cocina - Escalera: Y in [4.30, 4.45], X in [0.20, 2.80]
    add_box(LAYER_INT, COLOR_INT, 0.20, 4.30, 0.00, 2.80, 4.45, H_WALL)

    # 3. Escalera - Garaje: Y in [7.40, 7.55], X in [0.20, 2.80]
    add_box(LAYER_INT, COLOR_INT, 0.20, 7.40, 0.00, 2.80, 7.55, H_WALL)

    # 4. Hab4 - Comedor: Y in [3.55, 3.70], X in [2.95, 5.90]
    # P_Hab4: X in [3.50, 4.20]
    add_box(LAYER_INT, COLOR_INT, 2.95, 3.55, 0.00, 3.50, 3.70, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 3.50, 3.55, H_DOOR, 4.20, 3.70, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 4.20, 3.55, 0.00, 5.90, 3.70, H_WALL)

    # 5. Bano2 - Hab3: Y in [1.95, 2.10], X in [6.05, 9.05]
    add_box(LAYER_INT, COLOR_INT, 6.05, 1.95, 0.00, 9.05, 2.10, H_WALL)

    # 6. Hab3 - Hab2: Y in [5.35, 5.50], X in [6.05, 9.05]
    add_box(LAYER_INT, COLOR_INT, 6.05, 5.35, 0.00, 9.05, 5.50, H_WALL)

    # 7. Hab2 - Bano1: Y in [9.10, 9.25], X in [6.05, 9.05]
    add_box(LAYER_INT, COLOR_INT, 6.05, 9.10, 0.00, 9.05, 9.25, H_WALL)

    # 8. Bano1 - Hab1: Y in [11.10, 11.25], X in [6.05, 9.05]
    add_box(LAYER_INT, COLOR_INT, 6.05, 11.10, 0.00, 9.05, 11.25, H_WALL)

    # 9. Porche - Sala: Y in [12.90, 13.05], X in [2.95, 5.90]
    # P_Principal: X in [3.20, 4.15]
    add_box(LAYER_INT, COLOR_INT, 2.95, 12.90, 0.00, 3.20, 13.05, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 3.20, 12.90, H_DOOR, 4.15, 13.05, H_WALL)
    add_box(LAYER_INT, COLOR_INT, 4.15, 12.90, 0.00, 5.90, 13.05, H_WALL)

    # =========================================================================
    # 4. COLUMNAS 25x25 cm (Estructura destacada)
    # =========================================================================
    LAYER_COL = "COLUMNAS_3D"
    COLOR_COL = 1  # Rojo
    col_points = [
        # Eje 1 (X=2.80)
        (2.80, 14.90), (2.80, 12.90), (2.80, 10.40), (2.80, 7.40), (2.80, 4.30), (2.80, 0.20),
        # Eje 2 (X=5.90)
        (5.90, 14.90), (5.90, 12.90), (5.90, 9.10), (5.90, 5.35), (5.90, 3.55), (5.90, 0.20),
        # Eje 3 (X=9.00)
        (9.00, 14.90), (9.00, 11.10), (9.00, 9.10), (9.00, 5.35), (9.00, 1.95), (9.00, 0.20),
        # Eje Izquierdo Garaje (X=0.00)
        (0.00, 14.90), (0.00, 7.40), (0.00, 0.20)
    ]
    for cx, cy in col_points:
        add_box(LAYER_COL, COLOR_COL, cx, cy, 0.00, cx + 0.25, cy + 0.25, H_WALL)

    # =========================================================================
    # 5. CUBIERTA Y PARAPETO (Z = 2.80 a 3.40)
    # =========================================================================
    LAYER_ROOF = "CUBIERTA_3D"
    COLOR_ROOF = 9  # Gris claro
    # Losa de techo
    add_box(LAYER_ROOF, COLOR_ROOF, 0.00, 0.00, H_WALL, W_X, L_Y, H_WALL + SLAB_T)
    # Parapeto perimetral (altura 0.45 m)
    z_p1 = H_WALL + SLAB_T
    z_p2 = z_p1 + H_ROOF_PARAPET
    add_box(LAYER_ROOF, COLOR_ROOF, 0.00, 0.00, z_p1, 0.20, L_Y, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, W_X - 0.20, 0.00, z_p1, W_X, L_Y, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, 0.20, 0.00, z_p1, W_X - 0.20, 0.20, z_p2)
    add_box(LAYER_ROOF, COLOR_ROOF, 0.20, L_Y - 0.20, z_p1, W_X - 0.20, L_Y, z_p2)

    # =========================================================================
    # 6. LINEAS 2D Y ROTULACION DE ESPACIOS
    # =========================================================================
    LAYER_2D = "DISTRIBUCION_2D"
    COLOR_2D = 3  # Verde

    # Perimetro exterior 2D
    add_line(LAYER_2D, COLOR_2D, 0.00, 0.00, 0.0, W_X, 0.00, 0.0)
    add_line(LAYER_2D, COLOR_2D, W_X, 0.00, 0.0, W_X, L_Y, 0.0)
    add_line(LAYER_2D, COLOR_2D, W_X, L_Y, 0.0, 0.00, L_Y, 0.0)
    add_line(LAYER_2D, COLOR_2D, 0.00, L_Y, 0.0, 0.00, 0.00, 0.0)

    # Rotulos de Espacios (Centrados en cada ambiente)
    LAYER_TEXT = "ROTULOS_TEXTO"
    COLOR_TEXT = 2  # Amarillo
    rooms = [
        ("PORCHE", 4.35, 14.00),
        ("GARAJE", 1.50, 11.20),
        ("SALA", 4.40, 11.00),
        ("COMEDOR", 4.40, 7.20),
        ("COCINA", 1.50, 3.10),
        ("LAVADERO", 1.50, 0.90),
        ("HABITACION 1", 7.55, 13.10),
        ("BANO 1", 7.55, 10.15),
        ("HABITACION 2", 7.55, 7.30),
        ("HABITACION 3", 7.55, 3.70),
        ("BANO 2", 7.55, 1.05),
        ("HABITACION 4", 4.40, 1.85),
    ]
    for name, rx, ry in rooms:
        add_text(LAYER_TEXT, COLOR_TEXT, name, rx, ry, 0.05, 0.35)

    # Ejes Estructurales
    LAYER_GRID = "EJES_ESTRUCTURALES"
    COLOR_GRID = 1  # Rojo
    # Ejes X: 1 (2.80), 2 (5.90), 3 (9.15)
    for num, gx in [("1", 2.875), ("2", 5.975), ("3", 9.15)]:
        add_line(LAYER_GRID, COLOR_GRID, gx, -1.0, 0.0, gx, L_Y + 1.0, 0.0)
        add_text(LAYER_GRID, COLOR_GRID, f"EJE {num}", gx - 0.20, L_Y + 1.2, 0.0, 0.30)

    # =========================================================================
    # ENSAMBLAJE DEL ARCHIVO DXF (R12 ASCII COMPLETO)
    # =========================================================================
    dxf_lines = []

    def w(code, val):
        dxf_lines.append(f"{code:>3}\n{val}\n")

    # HEADER
    w(0, "SECTION")
    w(2, "HEADER")
    w(9, "$ACADVER")
    w(1, "AC1009")  # DXF R12 altamente compatible
    w(9, "$INSUNITS")
    w(70, 6)        # Metros
    w(9, "$EXTMIN")
    w(10, -2.0)
    w(20, -2.0)
    w(30, -0.5)
    w(9, "$EXTMAX")
    w(10, W_X + 2.0)
    w(20, L_Y + 2.0)
    w(30, H_WALL + 1.0)
    w(0, "ENDSEC")

    # TABLES
    w(0, "SECTION")
    w(2, "TABLES")
    w(0, "TABLE")
    w(2, "LAYER")
    w(70, 8)

    layer_defs = [
        (LAYER_SLAB, COLOR_SLAB),
        (LAYER_EXT, COLOR_EXT),
        (LAYER_INT, COLOR_INT),
        (LAYER_COL, COLOR_COL),
        (LAYER_ROOF, COLOR_ROOF),
        (LAYER_2D, COLOR_2D),
        (LAYER_TEXT, COLOR_TEXT),
        (LAYER_GRID, COLOR_GRID),
        ("ESCALERA_3D", 7),
        ("ESCALERA_2D", 7),
    ]
    for lname, lcol in layer_defs:
        w(0, "LAYER")
        w(2, lname)
        w(70, 0)
        w(62, lcol)
        w(6, "CONTINUOUS")

    w(0, "ENDTAB")
    w(0, "ENDSEC")

    # BLOCKS
    w(0, "SECTION")
    w(2, "BLOCKS")
    w(0, "ENDSEC")

    # ENTITIES
    w(0, "SECTION")
    w(2, "ENTITIES")

    # Escribir 3DFACEs para cada caja 3D
    def write_3dface(layer, color, p1, p2, p3, p4):
        w(0, "3DFACE")
        w(8, layer)
        w(62, color)
        w(10, f"{p1[0]:.4f}")
        w(20, f"{p1[1]:.4f}")
        w(30, f"{p1[2]:.4f}")
        w(11, f"{p2[0]:.4f}")
        w(21, f"{p2[1]:.4f}")
        w(31, f"{p2[2]:.4f}")
        w(12, f"{p3[0]:.4f}")
        w(22, f"{p3[1]:.4f}")
        w(32, f"{p3[2]:.4f}")
        w(13, f"{p4[0]:.4f}")
        w(23, f"{p4[1]:.4f}")
        w(33, f"{p4[2]:.4f}")

    for box in boxes_3d:
        layer, color, x1, y1, z1, x2, y2, z2 = box
        # 6 caras de la caja
        # Inferior (Z1)
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1))
        # Superior (Z2)
        write_3dface(layer, color, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2))
        # Sur (Y1)
        write_3dface(layer, color, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2))
        # Norte (Y2)
        write_3dface(layer, color, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2))
        # Oeste (X1)
        write_3dface(layer, color, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2))
        # Este (X2)
        write_3dface(layer, color, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2))

    # Escribir LINEAS 2D
    for line in lines_2d:
        layer, color, x1, y1, z1, x2, y2, z2 = line
        w(0, "LINE")
        w(8, layer)
        w(62, color)
        w(10, f"{x1:.4f}")
        w(20, f"{y1:.4f}")
        w(30, f"{z1:.4f}")
        w(11, f"{x2:.4f}")
        w(21, f"{y2:.4f}")
        w(32, f"{z2:.4f}")

    # Escribir TEXTOS
    for item in texts:
        layer, color, txt, x, y, z, h = item
        w(0, "TEXT")
        w(8, layer)
        w(62, color)
        w(10, f"{x:.4f}")
        w(20, f"{y:.4f}")
        w(30, f"{z:.4f}")
        w(40, f"{h:.4f}")
        w(1, txt)

    w(0, "ENDSEC")
    w(0, "EOF")

    with open(output_path, "w", encoding="ascii") as f:
        f.writelines(dxf_lines)

    print(f"DXF generado exitosamente en: {output_path}")
    print(f"Total cajas 3D: {len(boxes_3d)} (equivale a {len(boxes_3d)*6} caras 3DFACE)")
    print(f"Total lineas 2D: {len(lines_2d)}")
    print(f"Total textos: {len(texts)}")

if __name__ == "__main__":
    import os
    target = os.path.abspath("casa.dxf")
    generate_house_dxf(target)
