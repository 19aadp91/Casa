"""
Modelo Parametrico 3D - Casa de Habitacion (Primer Piso / Nivel Calle)
Generado por Arquitecto Virtual Gemini + CADCraft
Ubicacion: Av. 4 entre calles 30 y 31, N 30-7, Municipio Independencia, Yaracuy
Referencia: planos de casa.pdf
"""

import cadquery as cq

# ==============================================================================
# PASO 2: DEFINICION DE PARAMETROS GLOBALES
# ==============================================================================
BUILDING_WIDTH_X = 9.25          # Ancho total exterior (m)
BUILDING_LENGTH_Y = 15.15        # Largo total exterior (m)
WALL_HEIGHT = 2.80               # Altura libre de piso a techo (m)
EXT_WALL_THICKNESS = 0.20        # Espesor muros perimetrales (m)
INT_WALL_THICKNESS = 0.15        # Espesor tabiqueria interna (m)
SLAB_THICKNESS = 0.15            # Espesor losa de entrepiso/piso (m)
DOOR_HEIGHT = 2.10               # Altura estandar de dintel de puerta (m)
WINDOW_SILL = 1.00               # Altura de antepecho estandar (m)
WINDOW_HEIGHT = 1.10             # Altura de ventana estandar (m)
BATH_WINDOW_SILL = 1.80          # Altura antepecho de ventana de banos (m)
BATH_WINDOW_HEIGHT = 0.40        # Altura ventana de banos (m)
PARAPET_HEIGHT = 0.45            # Altura parapeto perimetral de cubierta (m)
BOOLEAN_TOLERANCE = 0.04         # Holgura para cortes booleanos limpios (m)


def create_box(x1, y1, z1, x2, y2, z2):
    """Genera un prisma rectangular definido por dos esquinas opuestas (X, Y, Z)."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    cz = (z1 + z2) / 2.0
    return cq.Workplane("XY").box(dx, dy, dz).translate((cx, cy, cz))


# ==============================================================================
# PASO 3: GENERACION DE GEOMETRIA CADCRAFT
# ==============================================================================

# 1. Losa Base (Floor_Slab) con hueco de escalera hacia el sotano
base_slab = create_box(0.00, 0.00, -SLAB_THICKNESS, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, 0.00)

# Hueco de escalera que desciende al sotano (X: 0.20 a 1.45, Y: 4.45 a 7.40)
stair_cutout = create_box(
    0.20 - BOOLEAN_TOLERANCE,
    4.45,
    -SLAB_THICKNESS - BOOLEAN_TOLERANCE,
    1.45,
    7.40,
    0.00 + BOOLEAN_TOLERANCE
)
floor_slab = base_slab.cut(stair_cutout)


# 2. Levantamiento de Muros (Walls_Volume)
walls_list = [
    # Muros Perimetrales Exteriores (Espesor: 0.20 m)
    ("Muro_Ext_Oeste", 0.00, 0.00, 0.20, BUILDING_LENGTH_Y),
    ("Muro_Ext_Sur", 0.00, 0.00, BUILDING_WIDTH_X, 0.20),
    ("Muro_Ext_Este", BUILDING_WIDTH_X - EXT_WALL_THICKNESS, 0.00, BUILDING_WIDTH_X, BUILDING_LENGTH_Y),
    ("Muro_Ext_Norte_Hab1", 5.90, BUILDING_LENGTH_Y - EXT_WALL_THICKNESS, BUILDING_WIDTH_X, BUILDING_LENGTH_Y),

    # Muros Longitudinales Interiores (Espesor: 0.15 m)
    # Eje 1: Divide sector servicio/garaje de sector social/comedor
    ("Muro_Long_Eje1", 2.80, 0.20, 2.95, 12.90),
    # Eje 2: Divide sector social de crujia de dormitorios y banos
    ("Muro_Long_Eje2", 5.90, 3.55, 6.05, 14.95),

    # Muros Transversales Interiores (Espesor: 0.15 m)
    ("Muro_Trans_Lav_Coc", 0.20, 1.70, 2.80, 1.85),       # Divide Lavadero de Cocina
    ("Muro_Trans_Coc_Esc", 0.20, 4.30, 2.80, 4.45),       # Divide Cocina de Escalera
    ("Muro_Trans_Esc_Gar", 0.20, 7.40, 2.80, 7.55),       # Divide Escalera de Garaje
    ("Muro_Trans_Hab4_Com", 2.95, 3.55, 5.90, 3.70),      # Divide Habitacion 4 de Comedor
    ("Muro_Trans_Hab3_B2", 6.05, 1.95, 9.05, 2.10),       # Divide Bano 2 de Habitacion 3
    ("Muro_Trans_Hab2_Hab3", 6.05, 5.35, 9.05, 5.50),     # Divide Habitacion 3 de Habitacion 2
    ("Muro_Trans_B1_Hab2", 6.05, 9.10, 9.05, 9.25),       # Divide Habitacion 2 de Bano 1
    ("Muro_Trans_Hab1_B1", 6.05, 11.10, 9.05, 11.25),     # Divide Bano 1 de Habitacion 1
    ("Muro_Trans_Porche_Sala", 2.95, 12.90, 5.90, 13.05),  # Fachada interior de acceso Porche-Sala
]

# Construir union solida de todos los muros
walls_volume = create_box(
    walls_list[0][1], walls_list[0][2], 0.00,
    walls_list[0][3], walls_list[0][4], WALL_HEIGHT
)

for wall in walls_list[1:]:
    wall_solid = create_box(wall[1], wall[2], 0.00, wall[3], wall[4], WALL_HEIGHT)
    walls_volume = walls_volume.union(wall_solid)


# 3. Operaciones Booleanas de Vanos (Openings_Cutouts)
# Puertas (Z: 0.00 a DOOR_HEIGHT)
doors_cutouts = [
    # ID, X1, Y1, X2, Y2, Z1, Z2
    ("P_Principal", 3.20, 12.90 - BOOLEAN_TOLERANCE, 4.15, 13.05 + BOOLEAN_TOLERANCE, 0.00, DOOR_HEIGHT),
    ("P_Garaje_Sala", 2.80 - BOOLEAN_TOLERANCE, 9.50, 2.95 + BOOLEAN_TOLERANCE, 10.40, 0.00, DOOR_HEIGHT),
    ("P_Cocina", 2.80 - BOOLEAN_TOLERANCE, 3.20, 2.95 + BOOLEAN_TOLERANCE, 4.00, 0.00, DOOR_HEIGHT),
    ("P_Lavadero_Int", 0.50, 1.70 - BOOLEAN_TOLERANCE, 1.30, 1.85 + BOOLEAN_TOLERANCE, 0.00, DOOR_HEIGHT),
    ("P_Lavadero_Ext", 0.80, 0.00 - BOOLEAN_TOLERANCE, 1.80, 0.20 + BOOLEAN_TOLERANCE, 0.00, DOOR_HEIGHT),
    ("P_Hab1", 5.90 - BOOLEAN_TOLERANCE, 11.50, 6.05 + BOOLEAN_TOLERANCE, 12.20, 0.00, DOOR_HEIGHT),
    ("P_B1", 5.90 - BOOLEAN_TOLERANCE, 9.80, 6.05 + BOOLEAN_TOLERANCE, 10.50, 0.00, DOOR_HEIGHT),
    ("P_Hab2", 5.90 - BOOLEAN_TOLERANCE, 8.10, 6.05 + BOOLEAN_TOLERANCE, 8.80, 0.00, DOOR_HEIGHT),
    ("P_Hab3", 5.90 - BOOLEAN_TOLERANCE, 4.30, 6.05 + BOOLEAN_TOLERANCE, 5.00, 0.00, DOOR_HEIGHT),
    ("P_B2", 5.90 - BOOLEAN_TOLERANCE, 1.00, 6.05 + BOOLEAN_TOLERANCE, 1.70, 0.00, DOOR_HEIGHT),
    ("P_Hab4", 3.50, 3.55 - BOOLEAN_TOLERANCE, 4.20, 3.70 + BOOLEAN_TOLERANCE, 0.00, DOOR_HEIGHT),
    ("Porton_Garaje", 0.20, 15.15 - EXT_WALL_THICKNESS - BOOLEAN_TOLERANCE, 2.80, 15.15 + BOOLEAN_TOLERANCE, 0.00, 2.50),
]

for door in doors_cutouts:
    cutter = create_box(door[1], door[2], door[5], door[3], door[4], door[6])
    walls_volume = walls_volume.cut(cutter)

# Ventanas (Cajas de corte con antepecho y dintel)
windows_cutouts = [
    # Fachada Frontal (Norte)
    ("V_Hab1_Frontal", 6.50, 14.95 - BOOLEAN_TOLERANCE, 8.70, 15.15 + BOOLEAN_TOLERANCE, WINDOW_SILL, WINDOW_SILL + WINDOW_HEIGHT),

    # Fachada Lateral Derecha (Este)
    ("V_Hab1_Lateral", 9.05 - BOOLEAN_TOLERANCE, 12.00, 9.25 + BOOLEAN_TOLERANCE, 14.20, WINDOW_SILL, WINDOW_SILL + WINDOW_HEIGHT),
    ("V_B1_Lateral", 9.05 - BOOLEAN_TOLERANCE, 9.70, 9.25 + BOOLEAN_TOLERANCE, 10.60, BATH_WINDOW_SILL, BATH_WINDOW_SILL + BATH_WINDOW_HEIGHT),
    ("V_Hab2_Lateral", 9.05 - BOOLEAN_TOLERANCE, 6.20, 9.25 + BOOLEAN_TOLERANCE, 8.40, WINDOW_SILL, WINDOW_SILL + WINDOW_HEIGHT),
    ("V_Hab3_Lateral", 9.05 - BOOLEAN_TOLERANCE, 2.60, 9.25 + BOOLEAN_TOLERANCE, 4.80, WINDOW_SILL, WINDOW_SILL + WINDOW_HEIGHT),
    ("V_B2_Lateral", 9.05 - BOOLEAN_TOLERANCE, 0.50, 9.25 + BOOLEAN_TOLERANCE, 1.40, BATH_WINDOW_SILL, BATH_WINDOW_SILL + BATH_WINDOW_HEIGHT),

    # Fachada Posterior (Sur)
    ("V_Hab4_Posterior", 3.70, 0.00 - BOOLEAN_TOLERANCE, 5.60, 0.20 + BOOLEAN_TOLERANCE, WINDOW_SILL, WINDOW_SILL + WINDOW_HEIGHT),
]

for win in windows_cutouts:
    cutter = create_box(win[1], win[2], win[5], win[3], win[4], win[6])
    walls_volume = walls_volume.cut(cutter)


# 4. Cubierta y Elementos Secundarios (Roof_And_Details)
# Losa superior de cubierta plana
roof_slab = create_box(
    0.00, 0.00, WALL_HEIGHT,
    BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT + SLAB_THICKNESS
)

# Parapeto perimetral superior
parapet_outer = create_box(
    0.00, 0.00, WALL_HEIGHT + SLAB_THICKNESS,
    BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT + SLAB_THICKNESS + PARAPET_HEIGHT
)
parapet_inner_void = create_box(
    EXT_WALL_THICKNESS, EXT_WALL_THICKNESS, WALL_HEIGHT + SLAB_THICKNESS - BOOLEAN_TOLERANCE,
    BUILDING_WIDTH_X - EXT_WALL_THICKNESS, BUILDING_LENGTH_Y - EXT_WALL_THICKNESS,
    WALL_HEIGHT + SLAB_THICKNESS + PARAPET_HEIGHT + BOOLEAN_TOLERANCE
)
parapet = parapet_outer.cut(parapet_inner_void)
roof_assembly = roof_slab.union(parapet)


# 5. Ensamblaje y Exportacion
model_assembly = cq.Assembly()
model_assembly.add(floor_slab, name="Losa_Piso", color=cq.Color("gray80"))
model_assembly.add(walls_volume, name="Muros_Primer_Piso", color=cq.Color("whitesmoke"))
model_assembly.add(roof_assembly, name="Cubierta_Parapeto", color=cq.Color("gray60"))

# Exportar a formatos estandar de intercambio CAD
compound_model = model_assembly.toCompound()
cq.exporters.export(compound_model, "casa_primer_piso.step")
cq.exporters.export(compound_model, "casa_primer_piso.stl")

if __name__ == "__main__":
    print("Modelo 3D CADCraft generado exitosamente.")
    print("Archivos exportados: casa_primer_piso.step y casa_primer_piso.stl")
