"""
Generador Maestro BIM en FreeCAD 1.1+ (Fase 1: Nivel Sotano + Rampa + Piso 1 Completo)
======================================================================================
Traduce con fidelidad milimetrica (1 m = 1.000 mm) la arquitectura de:
  - "02_Modelos_CAD/casa_proyecto_3_pisos.dxf"
  - "04_Scripts_Parametricos/build_casa_3_pisos.py"

Entregables automaticos:
  1. 03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.FCStd (Nativo FreeCAD + Spreadsheet)
  2. 03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.ifc   (Estandar abierto IFC4)
  3. 01_Planos_y_Documentacion/computos_metricos_fase1_bim.csv (Tabla Excel de partidas)
  4. 01_Planos_y_Documentacion/computos_metricos_fase1_bim.md  (Reporte ejecutivo de obra e insumos)

Ejecucion por consola:
  & "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" 04_Scripts_Parametricos/build_bim_fase1_freecad.py
"""

import csv
import math
import os
import sys

# Asegurar acceso al banco de trabajo BIM de FreeCAD 1.1 en ejecucion por consola
FREECAD_BIM_MOD = r"C:\Program Files\FreeCAD 1.1\Mod\BIM"
if os.path.isdir(FREECAD_BIM_MOD) and FREECAD_BIM_MOD not in sys.path:
    sys.path.append(FREECAD_BIM_MOD)

import FreeCAD
import Part
import Draft
import Arch
from importers import exportIFC


# =============================================================================
# CONSTANTES GEOMETRICAS FIELES A casa_proyecto_3_pisos.dxf (EN METROS -> MM)
# =============================================================================
MM = 1000.0

Z_SOT_FOOT_BOT = -3.05
Z_SOT_SLAB_BOT = -2.70
Z_SOT_FLOOR    = -2.55   # N.P.T. Sotano Gran Bodega y Patio de Maniobra Sur
Z_P1_SLAB_BOT  = -0.15   # Fondo losa entrepiso Planta Baja
Z_P1_FLOOR     =  0.00   # N.P.T. Planta Baja (Comercio + Estacionamiento)
H_P1           =  2.85   # Tope muros Planta Baja / Fondo losa sobre Piso 1
Z_P2_FLOOR     =  3.00   # Tope placa estructural de cierre sobre Piso 1
H_DOOR         =  2.10
H_DOOR_SOT     =  2.05

OFFSET_X = 0.00          # X = 0.00..0.15 pared del vecino INTOCABLE; X >= 0.15 obra propia
OFFSET_Y = 3.00          # Retiro posterior (Patio de Maniobra Sur)
Y_AV4    = 21.71         # Largo del cuerpo edificacion hasta lindero Av. 4

X_GAR_LEFT_IN  = 0.30
X_GAR_RIGHT_IN = 3.30    # 3,00 m libres reales de estacionamiento
X_GAR_WALL_OUT = 3.45

# Poligonal U.T.M. local (m)
P4_LOC = (0.0000,  0.0000)
P1_LOC = (0.0000, 24.7060)
P2_LOC = (11.3703, 24.9409)
P3_LOC = (10.8043,  0.2311)


def x_right(y_terr):
    return P3_LOC[0] + (P2_LOC[0] - P3_LOC[0]) * ((y_terr - P3_LOC[1]) / (P2_LOC[1] - P3_LOC[1]))


def y_rear(x_terr):
    return P4_LOC[1] + (P3_LOC[1] - P4_LOC[1]) * (x_terr / P3_LOC[0])


def v_terr(x_m, y_m, z_m):
    """Vector en milimetros en coordenadas absolutas de parcela."""
    return FreeCAD.Vector(float(x_m) * MM, float(y_m) * MM, float(z_m) * MM)


def v_house(x_m, y_casa_m, z_m):
    """Vector en milimetros en coordenadas de casa desplazadas por (OFFSET_X, OFFSET_Y)."""
    return FreeCAD.Vector(
        float(OFFSET_X + x_m) * MM,
        float(OFFSET_Y + y_casa_m) * MM,
        float(z_m) * MM,
    )


def box_terr(x1, y1, z1, x2, y2, z2):
    xa, xb = min(x1, x2) * MM, max(x1, x2) * MM
    ya, yb = min(y1, y2) * MM, max(y1, y2) * MM
    za, zb = min(z1, z2) * MM, max(z1, z2) * MM
    return Part.makeBox(xb - xa, yb - ya, zb - za, FreeCAD.Vector(xa, ya, za))


def box_house(x1, y1, z1, x2, y2, z2):
    return box_terr(
        OFFSET_X + x1, OFFSET_Y + y1, z1,
        OFFSET_X + x2, OFFSET_Y + y2, z2,
    )


def hexa_solid(pts8_m):
    """
    Construye un Part.Solid exacto a partir de 8 vertices (en metros, coordenadas absolutas):
    p0..p3 cara inferior (sentido antihorario visto desde arriba), p4..p7 cara superior.
    """
    pts = [v_terr(px, py, pz) for (px, py, pz) in pts8_m]
    p0, p1, p2, p3, p4, p5, p6, p7 = pts

    def quad_face(a, b, c, d):
        # Si los 4 puntos no son perfectamente coplanares, triangular en 2 caras planas
        w1 = Part.makePolygon([a, b, c, a])
        w2 = Part.makePolygon([a, c, d, a])
        return [Part.Face(w1), Part.Face(w2)]

    faces = []
    faces.extend(quad_face(p0, p3, p2, p1))  # Inferior
    faces.extend(quad_face(p4, p5, p6, p7))  # Superior
    faces.extend(quad_face(p0, p1, p5, p4))  # Sur / Frente 1
    faces.extend(quad_face(p3, p7, p6, p2))  # Norte / Frente 2
    faces.extend(quad_face(p0, p4, p7, p3))  # Oeste
    faces.extend(quad_face(p1, p2, p6, p5))  # Este
    shell = Part.makeShell(faces)
    solid = Part.makeSolid(shell)
    if solid.Volume < 0:
        solid.reverse()
    return solid


def hexa_house(pts8_house_m):
    shifted = [(OFFSET_X + px, OFFSET_Y + py, pz) for (px, py, pz) in pts8_house_m]
    return hexa_solid(shifted)


def fuse_shapes(shapes):
    valid = [s for s in shapes if s is not None and not s.isNull()]
    if not valid:
        return None
    if len(valid) == 1:
        return valid[0]
    acc = valid[0]
    for s in valid[1:]:
        acc = acc.fuse(s)
    return acc


def compound_shapes(shapes):
    valid = [s for s in shapes if s is not None and not s.isNull()]
    if not valid:
        return None
    if len(valid) == 1:
        return valid[0]
    return Part.makeCompound(valid)


# =============================================================================
# CONSTRUCCION DEL MODELO BIM Y MOTOR DE COMPUTOS METRICOS
# =============================================================================
def build_bim_fase1():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bim_dir = os.path.join(workspace_root, "03_Modelos_3D", "BIM_FreeCAD")
    doc_dir = os.path.join(workspace_root, "01_Planos_y_Documentacion")
    os.makedirs(bim_dir, exist_ok=True)
    os.makedirs(doc_dir, exist_ok=True)

    fcstd_path = os.path.join(bim_dir, "casa_fase1_sotano_piso1.FCStd")
    ifc_path   = os.path.join(bim_dir, "casa_fase1_sotano_piso1.ifc")
    csv_path   = os.path.join(doc_dir, "computos_metricos_fase1_bim.csv")
    md_path    = os.path.join(doc_dir, "computos_metricos_fase1_bim.md")

    print("=" * 78)
    print("INICIANDO CONSTRUCCION BIM FREECAD 1.1 — FASE 1 (SOTANO + RAMPA + PISO 1)")
    print("=" * 78)

    doc = FreeCAD.newDocument("Casa_Fase1_BIM")
    doc.Label = "Proyecto Casa Chalet & Comercio - Fase 1 BIM (Sotano + Piso 1)"

    # Registro estructurado de partidas para Computos Metricos
    qto_records = []
    own_shapes_for_audit = []

    # Grupo oculto para geometrias base auxiliares (mantiene el arbol BIM 100% limpio)
    base_grp = doc.addObject("App::DocumentObjectGroup", "Geometrias_Base_Internas")
    base_grp.Label = "_Geometrias_Base_Internas"
    base_grp.Visibility = False

    def make_base_feature(name, shape):
        feat = doc.addObject("Part::Feature", f"Base_{name}")
        feat.Shape = shape
        feat.Visibility = False
        base_grp.addObject(feat)
        return feat

    def add_qto_props(obj, chapter, code, level_name, unit, qty_primary, area_m2, vol_m3,
                      mat_label, description="", exclude_qto=False):
        obj.addProperty("App::PropertyString", "BIM_Capitulo", "Computos_BIM", "Capitulo de obra").BIM_Capitulo = chapter
        obj.addProperty("App::PropertyString", "BIM_Partida", "Computos_BIM", "Codigo de partida").BIM_Partida = code
        obj.addProperty("App::PropertyString", "BIM_Nivel", "Computos_BIM", "Nivel espacial").BIM_Nivel = level_name
        obj.addProperty("App::PropertyString", "BIM_Unidad", "Computos_BIM", "Unidad principal").BIM_Unidad = unit
        obj.addProperty("App::PropertyFloat",  "BIM_Cantidad", "Computos_BIM", "Cantidad principal").BIM_Cantidad = round(qty_primary, 3)
        obj.addProperty("App::PropertyFloat",  "BIM_Area_m2", "Computos_BIM", "Area neta m2").BIM_Area_m2 = round(area_m2, 3)
        obj.addProperty("App::PropertyFloat",  "BIM_Volumen_m3", "Computos_BIM", "Volumen neto m3").BIM_Volumen_m3 = round(vol_m3, 4)
        obj.addProperty("App::PropertyBool",   "ExcludeFromQuantities", "Computos_BIM", "Excluir de computos").ExcludeFromQuantities = exclude_qto
        if description and hasattr(obj, "Description"):
            obj.Description = description

        if not exclude_qto:
            qto_records.append({
                "capitulo": chapter,
                "codigo": code,
                "nivel": level_name,
                "nombre": obj.Label,
                "ifc_type": getattr(obj, "IfcType", "Building Element"),
                "material": mat_label,
                "unidad": unit,
                "cantidad": qty_primary,
                "area_m2": area_m2,
                "volumen_m3": vol_m3,
                "descripcion": description,
            })

    def create_bim_element(kind, name, label, shape, ifc_type, material_obj,
                           chapter, code, level_name, unit, qty_primary, area_m2, vol_m3,
                           description="", visible=True, exclude_qto=False, audit_own=True):
        feat = make_base_feature(name, shape)
        if kind == "Wall":
            obj = Arch.makeWall(feat, name=name)
        elif kind == "Structure":
            obj = Arch.makeStructure(feat, name=name)
        elif kind == "Equipment":
            obj = Arch.makeEquipment(feat, name=name)
        elif kind == "Space":
            obj = Arch.makeSpace(feat, name=name)
        else:
            obj = Arch.makeComponent(feat, name=name)

        obj.Label = label
        if hasattr(obj, "IfcType") and ifc_type:
            obj.IfcType = ifc_type
        if material_obj is not None and hasattr(obj, "Material"):
            obj.Material = material_obj
        obj.Visibility = visible

        mat_label = material_obj.Label if material_obj is not None else "Sin Material"
        add_qto_props(
            obj, chapter, code, level_name, unit,
            qty_primary, area_m2, vol_m3, mat_label,
            description=description, exclude_qto=exclude_qto,
        )
        if audit_own and not exclude_qto:
            own_shapes_for_audit.append((label, obj, shape))
        return obj

    # =========================================================================
    # 1. CATALOGO DE MATERIALES CONSTRUCTIVOS BIM (Arch.makeMaterial)
    # =========================================================================
    mat_grp = doc.addObject("App::DocumentObjectGroup", "Catalogo_Materiales_BIM")
    mat_grp.Label = "00_Catalogo_Materiales_BIM"

    def make_mat(name, label, rgb, desc):
        m = Arch.makeMaterial(name=name, color=rgb)
        m.Label = label
        d = dict(m.Material)
        d["Description"] = desc
        m.Material = d
        mat_grp.addObject(m)
        return m

    MAT_CONC_280   = make_mat("Mat_Concreto_280", "Concreto Armado f'c=280 kg/cm2 (Infraestructura)", (0.62, 0.65, 0.68), "Concreto estructural hidrofugado para sotano, zapatas, losas y rampa")
    MAT_CONC_250   = make_mat("Mat_Concreto_250", "Concreto Armado f'c=250 kg/cm2 (Superestructura P1)", (0.72, 0.74, 0.77), "Concreto armado para columnas 25x25, vigas, escaleras y entrepisos")
    MAT_MURO_CONT  = make_mat("Mat_Muro_Contencion", "Muro Contencion Concreto/Bloque Relleno Impermeabilizado e=15cm", (0.52, 0.58, 0.64), "Muro enterrado armado e impermeabilizado en sotano")
    MAT_BLOQ_20    = make_mat("Mat_Bloque_Concreto_20", "Mamposteria Bloque Concreto Pesado e=20cm", (0.68, 0.70, 0.68), "Mamposteria estructural de bloque de concreto de 20 cm")
    MAT_BLOQ_15    = make_mat("Mat_Bloque_15", "Mamposteria Bloque Arcilla/Concreto e=15cm Frisado", (0.88, 0.85, 0.79), "Pared de bloque e=15cm frisada y encamisada ambas caras")
    MAT_BLOQ_10    = make_mat("Mat_Bloque_10", "Tabiqueria Interna Bloque e=10cm (Banos)", (0.91, 0.86, 0.80), "Tabique divisorio interno de bloque de 10 cm")
    MAT_PIEDRA     = make_mat("Mat_Piedra_Laja", "Revestimiento Piedra Laja Rustica Natural", (0.48, 0.43, 0.37), "Zocalos y machones en piedra rustica tipo chalet")
    MAT_PORCEL     = make_mat("Mat_Porcelanato_Com", "Porcelanato Antideslizante Alto Trafico Comercial", (0.86, 0.83, 0.76), "Acabado de piso comercial de alta resistencia")
    MAT_PAV_GAR    = make_mat("Mat_Pavimento_Garaje", "Pavimento Concreto Pulido/Estriado Vehicular", (0.58, 0.60, 0.62), "Piso vehicular de alta resistencia en garaje")
    MAT_CERAM_BAN  = make_mat("Mat_Ceramica_Banos", "Ceramica Rectificada Impermeable en Banos", (0.80, 0.87, 0.89), "Revestimiento ceramico de piso y pared en nucleos humedos")
    MAT_ACERO_FORJ = make_mat("Mat_Acero_Forja", "Acero Estructural y Herreria Forja Negra", (0.20, 0.22, 0.25), "Perfiles metalicos, portones, santamarias y cerramientos de hierro negro")
    MAT_MADERA     = make_mat("Mat_Madera_Roble", "Madera Maciza Tratada (Roble/Pardillo)", (0.58, 0.38, 0.21), "Carpinteria rustica de puertas, ventanas, vigas vistas y mobiliario")
    MAT_VIDRIO     = make_mat("Mat_Cristal_Templado", "Cristal Templado Transparente 8-10 mm", (0.65, 0.85, 0.92), "Acristalamiento de oficina, vitrinas y ventanas")
    MAT_PIR_FRIO   = make_mat("Mat_Panel_PIR_120", "Panel Isotermico Poliisocianurato (PIR) e=12cm", (0.82, 0.90, 0.96), "Aislamiento termico frigorifico con lamina prelacada sanitaria")
    MAT_SANIT      = make_mat("Mat_Loza_Sanitaria", "Porcelana Sanitaria Vitrificada Blanca / Acero Inox", (0.95, 0.96, 0.98), "Aparatos sanitarios y fregaderos industriales")
    MAT_TIERRA     = make_mat("Mat_Terreno_Natural", "Suelo Natural / Terreno Poligonal U.T.M.", (0.46, 0.56, 0.38), "Terreno natural de la parcela")
    MAT_VECINO     = make_mat("Mat_Contexto_Vecino", "Pared Colindante Vecino (EXISTENTE - NO CONTABILIZAR)", (0.45, 0.45, 0.45), "Referencia de lindero izquierdo X=0.00..0.15m excluida de computos")

    # =========================================================================
    # 2. SISTEMA DE EJES ESTRUCTURALES BIM (IfcGrid)
    # =========================================================================
    axes_grp = doc.addObject("App::DocumentObjectGroup", "Sistema_Ejes_Estructurales")
    axes_grp.Label = "01_Ejes_Estructurales_BIM"

    ax_long = Arch.makeAxis(num=4, size=27500.0, name="Ejes_Longitudinales_0_3")
    ax_long.Label = "Ejes Longitudinales (0, 1, 2, 3)"
    ax_long.Distances = [0.0, (2.825 - 0.275) * MM, (5.925 - 2.825) * MM, (9.075 - 5.925) * MM]
    ax_long.Labels = ["0", "1", "2", "3"]
    ax_long.Placement.Base = v_terr(0.275, 1.50, 0.0)
    ax_long.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0.0)

    y_axes_vals = [0.125, 3.575, 6.575, 8.875, 12.025, 14.625, 16.325, 18.575, 21.585]
    y_axes_lbls = ["H", "G", "F", "E", "D", "C", "B", "A", "A0"]
    y_dists = [0.0] + [(y_axes_vals[i] - y_axes_vals[i - 1]) * MM for i in range(1, len(y_axes_vals))]
    ax_trans = Arch.makeAxis(num=len(y_axes_vals), size=11800.0, name="Ejes_Transversales_H_A0")
    ax_trans.Label = "Ejes Transversales (H .. A0)"
    ax_trans.Distances = y_dists
    ax_trans.Labels = y_axes_lbls
    ax_trans.Placement.Base = v_terr(-0.40, OFFSET_Y + y_axes_vals[0], 0.0)
    ax_trans.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), -90.0)

    ax_sys = Arch.makeAxisSystem([ax_long, ax_trans], name="Reticula_Ejes_BIM")
    ax_sys.Label = "Reticula Estructural BIM (Ejes 0..3 x H..A0)"
    axes_grp.addObject(ax_sys)

    # =========================================================================
    # 3. SITIO, EXCAVACION, LINDEROS Y RAMPA LOGISTICA (IfcSite)
    # =========================================================================
    site_objs = []

    # 3.1 Terreno natural bajo frente no excavado (Y_casa = 8.30..21.71) y base Patio Sur
    y_sot_start = OFFSET_Y
    y_r_bot     = OFFSET_Y + 5.50
    y_r_top     = OFFSET_Y + 19.50
    y_av4_tr    = OFFSET_Y + Y_AV4

    terr_patio_base = hexa_solid([
        (0.15, y_rear(0.15), Z_SOT_FLOOR - 0.20), (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR - 0.20),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR - 0.20), (0.15, y_sot_start, Z_SOT_FLOOR - 0.20),
        (0.15, y_rear(0.15), Z_SOT_FLOOR),        (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR),
        (x_right(y_sot_start), y_sot_start, Z_SOT_FLOOR),        (0.15, y_sot_start, Z_SOT_FLOOR),
    ])
    terr_front_1 = hexa_solid([
        (0.15, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20), (9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR - 0.20),
        (9.00, OFFSET_Y + 11.20, -1.25),              (0.15, OFFSET_Y + 11.20, -1.25),
        (0.15, OFFSET_Y + 8.30,  Z_SOT_FLOOR),        (9.00, OFFSET_Y + 8.30,  Z_SOT_FLOOR),
        (9.00, OFFSET_Y + 11.20, -1.05),              (0.15, OFFSET_Y + 11.20, -1.05),
    ])
    terr_front_2 = hexa_solid([
        (0.15, OFFSET_Y + 11.20, -1.25), (9.00, OFFSET_Y + 11.20, -1.25),
        (9.00, y_av4_tr,         -0.20), (0.15, y_av4_tr,         -0.20),
        (0.15, OFFSET_Y + 11.20, -1.05), (9.00, OFFSET_Y + 11.20, -1.05),
        (9.00, y_av4_tr,         -0.15), (0.15, y_av4_tr,         -0.15),
    ])
    terr_comp = compound_shapes([terr_patio_base, terr_front_1, terr_front_2])
    site_objs.append(create_bim_element(
        "Component", "Terreno_Natural_Poligonal", "Terreno Natural Remanente (Poligonal 273,81 m2)",
        terr_comp, "Building Element Proxy", MAT_TIERRA,
        "01_MOVIMIENTO_TIERRAS", "01.00", "Sitio / Parcela", "m2", 273.81, 273.81, terr_comp.Volume / 1e9,
        description="Poligonal U.T.M. P-1..P-4 (273,81 m2) de referencia topografica",
        visible=True, exclude_qto=True, audit_own=True,
    ))

    # 3.2 Volumen de Corte y Excavacion Mecanica (Sotano + Patio Sur + Trinchera Rampa)
    exc_sotano = box_house(0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 8.30, 0.00)
    exc_patio  = box_house(0.15, -2.85, Z_SOT_FLOOR - 0.15, 10.65, 0.00, -0.40)
    exc_rampa  = hexa_solid([
        (9.15, OFFSET_Y, Z_SOT_FLOOR - 0.20), (x_right(OFFSET_Y) - 0.15, OFFSET_Y, Z_SOT_FLOOR - 0.20),
        (x_right(y_r_top) - 0.15, y_r_top, -0.20), (9.15, y_r_top, -0.20),
        (9.15, OFFSET_Y, 0.00), (x_right(OFFSET_Y) - 0.15, OFFSET_Y, 0.00),
        (x_right(y_r_top) - 0.15, y_r_top, 0.00), (9.15, y_r_top, 0.00),
    ])
    exc_total_shape = compound_shapes([exc_sotano, exc_patio, exc_rampa])
    exc_vol_m3 = (exc_sotano.Volume + exc_patio.Volume + exc_rampa.Volume) / 1e9
    site_objs.append(create_bim_element(
        "Component", "Excavacion_Corte_Sotano_Rampa", "Excavacion en Corte para Sotano, Patio y Rampa",
        exc_total_shape, "Building Element Proxy", MAT_TIERRA,
        "01_MOVIMIENTO_TIERRAS", "01.01", "Sitio / Sotano", "m3", exc_vol_m3, 74.70 + 11.63 + 25.40, exc_vol_m3,
        description="Volumen en banco de excavacion para Bodega Sotano (-2,70m), Patio Sur y Rampa 18% (oculto en vista 3D)",
        visible=False, exclude_qto=False, audit_own=True,
    ))

    # 3.3 Pared colindante del vecino izquierdo (X = 0.00..0.15 m — EXCLUIDA DE COMPUTOS)
    vecino_sot = box_terr(0.00, P4_LOC[1], Z_SOT_FLOOR, 0.15, OFFSET_Y + 8.30, 2.50)
    vecino_pb  = box_terr(0.00, OFFSET_Y + 8.30, 0.00, 0.15, P1_LOC[1], 2.50)
    vecino_shape = fuse_shapes([vecino_sot, vecino_pb])
    site_objs.append(create_bim_element(
        "Wall", "Contexto_Pared_Vecino_Oeste", "Pared Colindante Vecino Oeste (X=0..0,15m - INTACTA)",
        vecino_shape, "Wall", MAT_VECINO,
        "00_CONTEXTO", "00.01", "Sitio / Lindero Oeste", "m2", 0.0, 0.0, vecino_shape.Volume / 1e9,
        description="Muro existente del vecino colindante (0,00 m invasion, excluido al 100% de computos)",
        visible=False, exclude_qto=True, audit_own=False,
    ))

    # 3.4 Rampa Logistica Continua desde Porton Derecho Av. 4 hasta Sotano (-2,55 m)
    ramp_umbral = hexa_solid([
        (9.15, y_r_top, -0.20), (x_right(y_r_top) - 0.15, y_r_top, -0.20),
        (P2_LOC[0] - 0.15, P2_LOC[1], -0.20), (9.15, P2_LOC[1], -0.20),
        (9.15, y_r_top,  0.00), (x_right(y_r_top) - 0.15, y_r_top,  0.00),
        (P2_LOC[0] - 0.15, P2_LOC[1],  0.00), (9.15, P2_LOC[1],  0.00),
    ])
    ramp_sloped = hexa_solid([
        (9.15, y_r_bot, Z_SOT_FLOOR - 0.20), (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR - 0.20),
        (x_right(y_r_top) - 0.15, y_r_top, -0.20), (9.15, y_r_top, -0.20),
        (9.15, y_r_bot, Z_SOT_FLOOR),        (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR),
        (x_right(y_r_top) - 0.15, y_r_top,  0.00), (9.15, y_r_top,  0.00),
    ])
    ramp_corredor = hexa_solid([
        (9.15, OFFSET_Y, Z_SOT_FLOOR - 0.20), (x_right(OFFSET_Y) - 0.15, OFFSET_Y, Z_SOT_FLOOR - 0.20),
        (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR - 0.20), (9.15, y_r_bot, Z_SOT_FLOOR - 0.20),
        (9.15, OFFSET_Y, Z_SOT_FLOOR),        (x_right(OFFSET_Y) - 0.15, OFFSET_Y, Z_SOT_FLOOR),
        (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR),        (9.15, y_r_bot, Z_SOT_FLOOR),
    ])
    ramp_full_shape = fuse_shapes([ramp_umbral, ramp_sloped, ramp_corredor])
    ramp_vol_m3  = ramp_full_shape.Volume / 1e9
    ramp_area_m2 = ramp_vol_m3 / 0.20  # Espesor constante de losa rampa e = 0,20 m
    site_objs.append(create_bim_element(
        "Structure", "Rampa_Logistica_Bodega_18pct", "Rampa Logistica Continua 18% y Corredor Este (e=20cm)",
        ramp_full_shape, "Ramp", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.04", "Sitio / Rampa Este", "m3", ramp_vol_m3, ramp_area_m2, ramp_vol_m3,
        description="Losa armada e=20cm acabado estriado antideslizante desde Porton Der. Av.4 (0,00m) a Sotano (-2,55m)",
    ))

    # Muro de acompanamiento bajo Planta Baja a lo largo de la rampa (X = 9.00..9.15)
    p_ac1 = v_terr(9.00, OFFSET_Y + 8.30, Z_SOT_FLOOR)
    p_ac2 = v_terr(9.00, y_r_top,         -0.20)
    p_ac3 = v_terr(9.00, y_r_top,         Z_P1_FLOOR)
    p_ac4 = v_terr(9.00, OFFSET_Y + 8.30, Z_P1_FLOOR)
    muro_acomp_rampa = Part.Face(Part.makePolygon([p_ac1, p_ac2, p_ac3, p_ac4, p_ac1])).extrude(
        FreeCAD.Vector(0.15 * MM, 0.0, 0.0)
    )
    acomp_vol = muro_acomp_rampa.Volume / 1e9
    site_objs.append(create_bim_element(
        "Wall", "Muro_Contencion_Lateral_Rampa", "Muro de Contencion Lateral Bajo P.B. Junto a Rampa",
        muro_acomp_rampa, "Wall", MAT_MURO_CONT,
        "02_INFRAESTRUCTURA_CONCRETO", "02.05", "Sitio / Rampa Este", "m3", acomp_vol, acomp_vol / 0.15, acomp_vol,
        description="Muro de acompanamiento y contencion bajo eje 3 a lo largo de la rampa (Y_casa=8,30..19,50m)",
    ))

    # Cercas perimetrales propias (Sur + Este, X >= 0.15 m para respetar lindero izquierdo)
    cerca_sur = hexa_solid([
        (0.15, y_rear(0.15), Z_SOT_FLOOR),        (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR), (0.15, y_rear(0.15) + 0.15, Z_SOT_FLOOR),
        (0.15, y_rear(0.15), Z_SOT_FLOOR + 2.20), (P3_LOC[0], P3_LOC[1], Z_SOT_FLOOR + 2.20),
        (P3_LOC[0], P3_LOC[1] + 0.15, Z_SOT_FLOOR + 2.20), (0.15, y_rear(0.15) + 0.15, Z_SOT_FLOOR + 2.20),
    ])
    cerca_este_1 = hexa_solid([
        (x_right(P3_LOC[1]) - 0.15, P3_LOC[1], Z_SOT_FLOOR), (x_right(P3_LOC[1]), P3_LOC[1], Z_SOT_FLOOR),
        (x_right(y_r_bot), y_r_bot, Z_SOT_FLOOR),            (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR),
        (x_right(P3_LOC[1]) - 0.15, P3_LOC[1], Z_SOT_FLOOR + 2.20), (x_right(P3_LOC[1]), P3_LOC[1], Z_SOT_FLOOR + 2.20),
        (x_right(y_r_bot), y_r_bot, Z_SOT_FLOOR + 2.20),            (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR + 2.20),
    ])
    cerca_este_2 = hexa_solid([
        (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR), (x_right(y_r_bot), y_r_bot, Z_SOT_FLOOR),
        (P2_LOC[0], P2_LOC[1], 0.00),                    (P2_LOC[0] - 0.15, P2_LOC[1], 0.00),
        (x_right(y_r_bot) - 0.15, y_r_bot, Z_SOT_FLOOR + 2.20), (x_right(y_r_bot), y_r_bot, Z_SOT_FLOOR + 2.20),
        (P2_LOC[0], P2_LOC[1], 2.20),                           (P2_LOC[0] - 0.15, P2_LOC[1], 2.20),
    ])
    cercas_shape = fuse_shapes([cerca_sur, cerca_este_1, cerca_este_2])
    cercas_vol   = cercas_shape.Volume / 1e9
    cercas_area  = cercas_vol / 0.15
    site_objs.append(create_bim_element(
        "Wall", "Cercas_Perimetrales_Sur_y_Este", "Muros de Cerramiento Perimetral Sur y Lindero Este (H=2,20m)",
        cercas_shape, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.01", "Sitio / Linderos", "m2", cercas_area, cercas_area, cercas_vol,
        description="Cerramiento perimetral propio en bloque e=15cm H=2,20m sobre lindero Sur y Este",
    ))

    # =========================================================================
    # 4. NIVEL 00: SOTANO — GRAN BODEGA MAYORISTA (N.P.T. = -2,55 m)
    # =========================================================================
    sot_objs = []
    sot_spaces = []

    # 4.1 Zapatas Aisladas de Fundacion bajo los 12 apoyos del Sotano (X >= 0.15 m!)
    sot_cols_axes = [
        (2.825, 6.575), (5.925, 6.575), (8.975, 6.575),
        (0.325, 3.575), (2.825, 3.575), (5.925, 3.575), (8.975, 3.575),
        (0.325, 0.175), (2.825, 0.175), (5.925, 0.175), (8.975, 0.175),
    ]
    footing_boxes = [box_house(0.15, 6.05, Z_SOT_FOOT_BOT, 1.05, 7.10, Z_SOT_SLAB_BOT)]
    for cx, cy in sot_cols_axes:
        fx1 = max(0.15, cx - 0.55)
        fx2 = fx1 + 1.10 if cx < 0.70 else min(9.55, cx + 0.55)
        fy1 = cy - 0.55
        fy2 = cy + 0.55
        footing_boxes.append(box_house(fx1, fy1, Z_SOT_FOOT_BOT, fx2, fy2, Z_SOT_SLAB_BOT))
    footings_shape = compound_shapes(footing_boxes)
    footings_vol = sum(b.Volume for b in footing_boxes) / 1e9
    sot_objs.append(create_bim_element(
        "Structure", "Zapatas_Fundacion_Sotano_12", "Zapatas Aisladas de Fundacion Sotano (12 und, e=35cm)",
        footings_shape, "Footing", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.01", "Nivel 00 - Sotano", "m3", footings_vol, len(footing_boxes) * 1.21, footings_vol,
        description="12 zapatas de concreto armado f'c=280 kg/cm2 (excentricas en Eje 0 respetando X >= 0,15m)",
    ))

    # 4.2 Losa Maciza de Piso Sotano Bodega (74,70 m2) + Losa Patio de Maniobra Sur (11,63 m2)
    slab_sot_shape = box_house(0.15, 0.00, Z_SOT_SLAB_BOT, 9.15, 8.30, Z_SOT_FLOOR)
    sot_objs.append(create_bim_element(
        "Structure", "Losa_Piso_Sotano_Bodega", "Losa de Fundacion Sotano Gran Bodega (9,00x8,30m, e=15cm)",
        slab_sot_shape, "Slab", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.02", "Nivel 00 - Sotano", "m3",
        slab_sot_shape.Volume / 1e9, 9.00 * 8.30, slab_sot_shape.Volume / 1e9,
        description="Losa de piso armada e hidrofugada e=15cm en Gran Bodega Mayorista (74,70 m2)",
    ))

    slab_patio_shape = box_house(4.50, -2.50, Z_SOT_FLOOR - 0.10, 9.15, 0.00, Z_SOT_FLOOR + 0.01)
    sot_objs.append(create_bim_element(
        "Structure", "Losa_Patio_Maniobra_Sur", "Pavimento Armado Patio de Maniobra y Carga Sur (4,65x2,50m)",
        slab_patio_shape, "Slab", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.03", "Nivel 00 - Sotano", "m3",
        slab_patio_shape.Volume / 1e9, 4.65 * 2.50, slab_patio_shape.Volume / 1e9,
        description="Losa de concreto armado para patio exterior de descarga (11,63 m2, Z=-2,55m)",
    ))

    # 4.3 Las 12 Columnas Estructurales del Sotano (35x35 cm + Machon Oeste 15x45 cm)
    sot_col_shapes = []
    machon_sot = box_house(0.15, 6.35, Z_SOT_FLOOR, 0.30, 6.80, Z_P1_SLAB_BOT)
    sot_col_shapes.append(machon_sot)
    sot_objs.append(create_bim_element(
        "Structure", "Col_Sot_0_F_Machon", "Columna Sotano Eje 0-F (Machon Propio 15x45cm, H=2,40m)",
        machon_sot, "Column", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.06", "Nivel 00 - Sotano", "m3",
        machon_sot.Volume / 1e9, 0.15 * 0.45, machon_sot.Volume / 1e9,
        description="Machon estructural Oeste sobre lindero propio X=0,15..0,30m",
    ))

    sot_axis_names = [
        ("1_F", 2.825, 6.575), ("2_F", 5.925, 6.575), ("3_F", 8.975, 6.575),
        ("0_G", 0.325, 3.575), ("1_G", 2.825, 3.575), ("2_G", 5.925, 3.575), ("3_G", 8.975, 3.575),
        ("0_H", 0.325, 0.175), ("1_H", 2.825, 0.175), ("2_H", 5.925, 0.175), ("3_H", 8.975, 0.175),
    ]
    for cname, cx, cy in sot_axis_names:
        c_sh = box_house(cx - 0.175, cy - 0.175, Z_SOT_FLOOR, cx + 0.175, cy + 0.175, Z_P1_SLAB_BOT)
        sot_col_shapes.append(c_sh)
        sot_objs.append(create_bim_element(
            "Structure", f"Col_Sot_{cname}", f"Columna Sotano Eje {cname.replace('_', '-')} (35x35cm, H=2,40m)",
            c_sh, "Column", MAT_CONC_280,
            "02_INFRAESTRUCTURA_CONCRETO", "02.06", "Nivel 00 - Sotano", "m3",
            c_sh.Volume / 1e9, 0.35 * 0.35, c_sh.Volume / 1e9,
            description=f"Columna estructural de sotano 35x35 cm en nodo {cname.replace('_', '-')}",
        ))
    sot_cols_union = fuse_shapes(sot_col_shapes)

    # 4.4 Muros de Contencion y Exteriores del Sotano (DESCONTANDO COLUMNAS Y VANOS EXACTOS!)
    w_sot_west = box_house(0.15, 0.00, Z_SOT_FLOOR, 0.30, 8.30, Z_P1_SLAB_BOT).cut(sot_cols_union)
    sot_objs.append(create_bim_element(
        "Wall", "Muro_Contencion_Oeste_Sotano", "Muro Contencion Oeste Propio Sotano (e=15cm, Ciego)",
        w_sot_west, "Wall", MAT_MURO_CONT,
        "02_INFRAESTRUCTURA_CONCRETO", "02.07", "Nivel 00 - Sotano", "m2",
        (w_sot_west.Volume / 1e9) / 0.15, (w_sot_west.Volume / 1e9) / 0.15, w_sot_west.Volume / 1e9,
        description="Muro enterrado propio X=0,15..0,30m sin tocar fundacion vecina",
    ))

    w_sot_north = box_house(0.30, 8.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT).cut(sot_cols_union)
    sot_objs.append(create_bim_element(
        "Wall", "Muro_Contencion_Norte_Sotano", "Muro Contencion Norte Sotano contra Terreno (e=15cm)",
        w_sot_north, "Wall", MAT_MURO_CONT,
        "02_INFRAESTRUCTURA_CONCRETO", "02.07", "Nivel 00 - Sotano", "m2",
        (w_sot_north.Volume / 1e9) / 0.15, (w_sot_north.Volume / 1e9) / 0.15, w_sot_north.Volume / 1e9,
        description="Muro norte de contencion de tierras en Y_casa=8,15..8,30m",
    ))

    # Muro Sur Sotano hacia Patio de Maniobra (resta columnas + 3 ventanas altas + porton 2,20x2,10m)
    sot_south_openings = [
        ("Ventana_Alta_Sur_Sot_1", 0.75, 2.35, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        ("Celosia_Alta_Bano_Sot",  3.25, 4.30, Z_SOT_FLOOR + 1.70, Z_SOT_FLOOR + 2.20),
        ("Ventana_Alta_Sur_Sot_2", 4.85, 5.75, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        ("Porton_Carga_Sot",       6.35, 8.55, Z_SOT_FLOOR,        Z_SOT_FLOOR + 2.10),
    ]
    w_sot_south = box_house(0.30, 0.00, Z_SOT_FLOOR, 9.15, 0.15, Z_P1_SLAB_BOT).cut(sot_cols_union)
    for _, ox1, ox2, oz1, oz2 in sot_south_openings:
        w_sot_south = w_sot_south.cut(box_house(ox1, -0.10, oz1, ox2, 0.25, oz2))
    sot_objs.append(create_bim_element(
        "Wall", "Muro_Exterior_Sur_Sotano", "Muro Sur Sotano hacia Patio de Maniobra (e=15cm Neto)",
        w_sot_south, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 00 - Sotano", "m2",
        (w_sot_south.Volume / 1e9) / 0.15, (w_sot_south.Volume / 1e9) / 0.15, w_sot_south.Volume / 1e9,
        description="Muro fachada Sur del sotano descontando columnas, 3 ventanas altas y porton de 2,20x2,10m",
    ))

    # Muro Este Sotano sobre Eje 3 (e=20cm, resta columnas + 3 ventanas altas)
    sot_east_openings = [
        ("Ventana_Alta_Este_Sot_1", 1.00, 2.65, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        ("Ventana_Alta_Este_Sot_2", 4.20, 5.85, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
        ("Ventana_Alta_Este_Sot_3", 6.95, 8.00, Z_SOT_FLOOR + 1.65, Z_SOT_FLOOR + 2.20),
    ]
    w_sot_east = box_house(8.95, 0.15, Z_SOT_FLOOR, 9.15, 8.30, Z_P1_SLAB_BOT).cut(sot_cols_union)
    for _, oy1, oy2, oz1, oz2 in sot_east_openings:
        w_sot_east = w_sot_east.cut(box_house(8.85, oy1, oz1, 9.25, oy2, oz2))
    sot_objs.append(create_bim_element(
        "Wall", "Muro_Exterior_Este_Sotano", "Muro Este Sotano sobre Corredor de Carga (e=20cm Neto)",
        w_sot_east, "Wall", MAT_BLOQ_20,
        "04_ALBANILERIA_Y_ACABADOS", "04.03", "Nivel 00 - Sotano", "m2",
        (w_sot_east.Volume / 1e9) / 0.20, (w_sot_east.Volume / 1e9) / 0.20, w_sot_east.Volume / 1e9,
        description="Muro de bloque de concreto e=20cm descontando columnas y 3 ventanas altas de seguridad",
    ))

    # 4.5 Tabiqueria Interior Sotano (Esclusa de Escalera + Bano Operativo)
    w_esclusa_sot = fuse_shapes([
        box_house(1.40, 3.55, Z_SOT_FLOOR, 1.55, 8.15, Z_P1_SLAB_BOT),
        box_house(0.30, 3.40, Z_SOT_FLOOR, 1.55, 3.55, Z_P1_SLAB_BOT),
    ]).cut(sot_cols_union)
    w_esclusa_sot = w_esclusa_sot.cut(box_house(1.30, 3.70, Z_SOT_FLOOR, 1.65, 4.55, Z_SOT_FLOOR + H_DOOR_SOT))
    w_esclusa_sot = w_esclusa_sot.cut(box_house(1.30, 7.20, Z_SOT_FLOOR, 1.65, 7.95, Z_SOT_FLOOR + 1.90))
    sot_objs.append(create_bim_element(
        "Wall", "Tabique_Esclusa_Escalera_Sotano", "Muros Esclusa Cerrada de Escalera Sotano (e=15cm Neto)",
        w_esclusa_sot, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 00 - Sotano", "m2",
        (w_esclusa_sot.Volume / 1e9) / 0.15, (w_esclusa_sot.Volume / 1e9) / 0.15, w_esclusa_sot.Volume / 1e9,
        description="Cerramiento de seguridad de escalera en sotano con vano hacia pasillo libre de 1,95 m",
    ))

    w_bano_sot = fuse_shapes([
        box_house(2.80, 0.15, Z_SOT_FLOOR, 2.95, 2.55, Z_P1_SLAB_BOT),
        box_house(4.55, 0.15, Z_SOT_FLOOR, 4.70, 2.55, Z_P1_SLAB_BOT),
        box_house(2.80, 2.55, Z_SOT_FLOOR, 4.70, 2.70, Z_P1_SLAB_BOT),
    ]).cut(sot_cols_union)
    w_bano_sot = w_bano_sot.cut(box_house(3.40, 2.45, Z_SOT_FLOOR, 4.18, 2.80, Z_SOT_FLOOR + H_DOOR_SOT))
    sot_objs.append(create_bim_element(
        "Wall", "Tabiques_Bano_Operativo_Sotano", "Muros Bano Operativo Personal y Lava-Mopas (e=15cm Neto)",
        w_bano_sot, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 00 - Sotano", "m2",
        (w_bano_sot.Volume / 1e9) / 0.15, (w_bano_sot.Volume / 1e9) / 0.15, w_bano_sot.Volume / 1e9,
        description="Tabiqueria de bloque e=15cm del bano operativo en sotano",
    ))

    # 4.6 Escalera Interior Tramo 1 (Sotano -2,55m -> P.B. 0,00m, 12 peldanos)
    num_steps_sot = 12
    step_dy_sot = (7.40 - 4.45) / num_steps_sot
    step_dz_sot = (0.00 - Z_SOT_FLOOR) / num_steps_sot
    stair1_parts = []
    for i in range(num_steps_sot):
        y_s_top = 7.40 - i * step_dy_sot
        y_s_bot = y_s_top - step_dy_sot
        z_s_top = 0.00 - i * step_dz_sot
        z_s_bot = max(Z_SOT_FLOOR, z_s_top - 0.22)
        stair1_parts.append(box_house(0.30, y_s_bot, z_s_bot, 1.40, y_s_top, z_s_top))
    stair1_shape = fuse_shapes(stair1_parts)
    sot_objs.append(create_bim_element(
        "Structure", "Escalera_Tramo1_Sotano_PB", "Escalera Concreto Armado Tramo 1: Sotano -> P.B. (12 peldanos)",
        stair1_shape, "Stair", MAT_CONC_280,
        "02_INFRAESTRUCTURA_CONCRETO", "02.08", "Nivel 00 - Sotano", "m3",
        stair1_shape.Volume / 1e9, 1.10 * 2.95, stair1_shape.Volume / 1e9,
        description="Escalera recta de concreto armado ancho 1,10 m (12 peldanos, Z=-2,55 a 0,00 m)",
    ))

    # 4.7 Carpinteria Metalica, Puertas y Ventanas Altas del Sotano
    def build_window_south_shape(x1, x2, z1, z2, with_shutters=False):
        t_f = 0.06
        xm, zm = 0.5 * (x1 + x2), 0.5 * (z1 + z2)
        parts = [
            box_house(x1, -0.02, z1, x2, 0.17, z1 + t_f),
            box_house(x1, -0.02, z2 - t_f, x2, 0.17, z2),
            box_house(x1, -0.02, z1 + t_f, x1 + t_f, 0.17, z2 - t_f),
            box_house(x2 - t_f, -0.02, z1 + t_f, x2, 0.17, z2 - t_f),
            box_house(xm - 0.02, 0.05, z1 + t_f, xm + 0.02, 0.10, z2 - t_f),
            box_house(x1 + t_f, 0.05, zm - 0.02, x2 - t_f, 0.10, zm + 0.02),
            box_house(x1 + t_f, 0.07, z1 + t_f, x2 - t_f, 0.08, z2 - t_f),
        ]
        if with_shutters and (x2 - x1) >= 1.40:
            sh_w = 0.36
            if x1 - sh_w >= 0.25:
                parts.append(box_house(x1 - sh_w, -0.05, z1, x1 - 0.02, 0.00, z2))
            if x2 + sh_w <= 8.95:
                parts.append(box_house(x2 + 0.02, -0.05, z1, x2 + sh_w, 0.00, z2))
        return compound_shapes(parts)

    def build_window_east_shape(y1, y2, z1, z2, with_shutters=False):
        t_f = 0.06
        ym, zm = 0.5 * (y1 + y2), 0.5 * (z1 + z2)
        parts = [
            box_house(8.98, y1, z1, 9.17, y2, z1 + t_f),
            box_house(8.98, y1, z2 - t_f, 9.17, y2, z2),
            box_house(8.98, y1, z1 + t_f, 9.17, y1 + t_f, z2 - t_f),
            box_house(8.98, y2 - t_f, z1 + t_f, 9.17, y2, z2 - t_f),
            box_house(9.05, ym - 0.02, z1 + t_f, 9.10, ym + 0.02, z2 - t_f),
            box_house(9.05, y1 + t_f, zm - 0.02, 9.10, y2 - t_f, zm + 0.02),
            box_house(9.07, y1 + t_f, z1 + t_f, 9.08, y2 - t_f, z2 - t_f),
        ]
        if with_shutters and (y2 - y1) >= 1.40:
            sh_w = min(0.38, 0.35 * (y2 - y1))
            if y1 - sh_w > 0.25:
                parts.append(box_house(9.15, y1 - sh_w, z1, 9.20, y1 - 0.02, z2))
            if y2 + sh_w < Y_AV4 - 0.25:
                parts.append(box_house(9.15, y2 + 0.02, z1, 9.20, y2 + sh_w, z2))
        return compound_shapes(parts)

    for wname, wx1, wx2, wz1, wz2 in sot_south_openings[:3]:
        w_sh = build_window_south_shape(wx1, wx2, wz1, wz2, with_shutters=False)
        area_w = (wx2 - wx1) * (wz2 - wz1)
        sot_objs.append(create_bim_element(
            "Component", wname, f"{wname.replace('_', ' ')} ({wx2-wx1:.2f}x{wz2-wz1:.2f}m con Reja)",
            w_sh, "Window", MAT_ACERO_FORJ,
            "05_HERRERIA_Y_CERRAMIENTOS", "05.05", "Nivel 00 - Sotano", "und", 1.0, area_w, w_sh.Volume / 1e9,
            description=f"Ventana alta basculante en hierro y vidrio con reja de seguridad ({wx2-wx1:.2f}x{wz2-wz1:.2f}m)",
        ))

    for wname, wy1, wy2, wz1, wz2 in sot_east_openings:
        w_sh = build_window_east_shape(wy1, wy2, wz1, wz2, with_shutters=False)
        area_w = (wy2 - wy1) * (wz2 - wz1)
        sot_objs.append(create_bim_element(
            "Component", wname, f"{wname.replace('_', ' ')} ({wy2-wy1:.2f}x{wz2-wz1:.2f}m con Reja)",
            w_sh, "Window", MAT_ACERO_FORJ,
            "05_HERRERIA_Y_CERRAMIENTOS", "05.05", "Nivel 00 - Sotano", "und", 1.0, area_w, w_sh.Volume / 1e9,
            description=f"Ventana alta basculante Este en hierro y vidrio con reja ({wy2-wy1:.2f}x{wz2-wz1:.2f}m)",
        ))

    # Porton Doble Metalico de Carga en Sotano (2,20 x 2,10 m)
    porton_sot_sh = compound_shapes([
        box_house(6.29, -0.04, Z_SOT_FLOOR, 6.36, 0.18, Z_SOT_FLOOR + 2.16),
        box_house(8.54, -0.04, Z_SOT_FLOOR, 8.61, 0.18, Z_SOT_FLOOR + 2.16),
        box_house(6.27, -0.05, Z_SOT_FLOOR + 2.10, 8.63, 0.18, Z_SOT_FLOOR + 2.18),
        box_house(6.32, -1.08, Z_SOT_FLOOR + 0.02, 6.39, -0.02, Z_SOT_FLOOR + 2.08),
        box_house(8.51, -1.08, Z_SOT_FLOOR + 0.02, 8.58, -0.02, Z_SOT_FLOOR + 2.08),
    ])
    sot_objs.append(create_bim_element(
        "Component", "Porton_Doble_Carga_Sotano", "Porton Doble Metalico Reforzado Carga Bodega (2,20x2,10m)",
        porton_sot_sh, "Door", MAT_ACERO_FORJ,
        "05_HERRERIA_Y_CERRAMIENTOS", "05.04", "Nivel 00 - Sotano", "und", 1.0, 2.20 * 2.10, porton_sot_sh.Volume / 1e9,
        description="Porton industrial de doble hoja batiente en lamina y perfileria pesada hacia Patio de Maniobra",
    ))

    # Puerta Metalica de Seguridad en Esclusa Escalera Sotano (a 45 grados)
    pta_esc_sot_sh = compound_shapes([
        box_house(1.38, 3.66, Z_SOT_FLOOR, 1.57, 3.71, Z_SOT_FLOOR + H_DOOR_SOT),
        box_house(1.38, 4.54, Z_SOT_FLOOR, 1.57, 4.59, Z_SOT_FLOOR + H_DOOR_SOT),
        box_house(1.38, 3.66, Z_SOT_FLOOR + H_DOOR_SOT, 1.57, 4.59, Z_SOT_FLOOR + H_DOOR_SOT + 0.06),
        hexa_house([
            (1.55, 4.52, Z_SOT_FLOOR + 0.02), (1.60, 4.56, Z_SOT_FLOOR + 0.02),
            (2.15, 3.96, Z_SOT_FLOOR + 0.02), (2.10, 3.92, Z_SOT_FLOOR + 0.02),
            (1.55, 4.52, Z_SOT_FLOOR + H_DOOR_SOT - 0.02), (1.60, 4.56, Z_SOT_FLOOR + H_DOOR_SOT - 0.02),
            (2.15, 3.96, Z_SOT_FLOOR + H_DOOR_SOT - 0.02), (2.10, 3.92, Z_SOT_FLOOR + H_DOOR_SOT - 0.02),
        ]),
    ])
    sot_objs.append(create_bim_element(
        "Component", "Puerta_Seguridad_Esclusa_Sotano", "Puerta Metalica Seguridad Esclusa Escalera Sotano (0,85x2,05m)",
        pta_esc_sot_sh, "Door", MAT_ACERO_FORJ,
        "05_HERRERIA_Y_CERRAMIENTOS", "05.06", "Nivel 00 - Sotano", "und", 1.0, 0.85 * 2.05, pta_esc_sot_sh.Volume / 1e9,
        description="Puerta metalica entamborada con cerradura de seguridad abriendo hacia pasillo libre de 1,95m",
    ))

    pta_bano_sot_sh = box_house(4.12, 1.85, Z_SOT_FLOOR + 0.02, 4.17, 2.55, Z_SOT_FLOOR + H_DOOR_SOT - 0.02)
    sot_objs.append(create_bim_element(
        "Component", "Puerta_Bano_Operativo_Sotano", "Puerta Bano Operativo Personal Sotano (0,78x2,05m)",
        pta_bano_sot_sh, "Door", MAT_MADERA,
        "06_CARPINTERIA_MADERA_VIDRIO", "06.01", "Nivel 00 - Sotano", "und", 1.0, 0.78 * 2.05, pta_bano_sot_sh.Volume / 1e9,
        description="Puerta batiente hidrofuga para bano operativo de sotano",
    ))

    # 4.8 Camara Isotermica de Pre-Frio (10,07 m2) + Equipamiento Mayorista + Sanitarios Sotano
    cam_frio_panels = fuse_shapes([
        box_house(1.60, 5.55, Z_SOT_FLOOR, 5.55, 5.67, Z_SOT_FLOOR + 2.30),
        box_house(5.43, 5.55, Z_SOT_FLOOR, 5.55, 8.10, Z_SOT_FLOOR + 2.30),
        box_house(1.60, 5.55, Z_SOT_FLOOR + 2.22, 5.55, 8.10, Z_SOT_FLOOR + 2.32),
    ]).cut(box_house(3.15, 5.45, Z_SOT_FLOOR, 4.20, 5.75, Z_SOT_FLOOR + 2.05))
    pir_area_m2 = (3.95 * 2.30 - 1.05 * 2.05) + (2.55 * 2.30) + (3.95 * 2.55)
    sot_objs.append(create_bim_element(
        "Component", "Camara_Isotermica_PreFrio_PIR", "Paneleria Isotermica PIR e=12cm Camara Pre-Frio (10,07 m2)",
        cam_frio_panels, "Covering", MAT_PIR_FRIO,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.01", "Nivel 00 - Sotano", "m2", pir_area_m2, pir_area_m2, cam_frio_panels.Volume / 1e9,
        description="Cerramiento modular y techo en panel frigorifico PIR 120mm para Camara de Pre-Frio Mayorista",
    ))

    cam_frio_door_ctrl = compound_shapes([
        box_house(3.10, 5.48, Z_SOT_FLOOR + 0.03, 4.25, 5.56, Z_SOT_FLOOR + 2.08),
        box_house(4.38, 5.50, Z_SOT_FLOOR + 1.45, 4.62, 5.55, Z_SOT_FLOOR + 1.72),
        *[box_house(1.70, 7.45, Z_SOT_FLOOR + rz_c, 5.35, 8.02, Z_SOT_FLOOR + rz_c + 0.35) for rz_c in [0.35, 0.95, 1.55]],
    ])
    sot_objs.append(create_bim_element(
        "Equipment", "Unidad_Puerta_y_Control_PreFrio", "Puerta Corrediza Frigorifica Inox (1,15x2,05m) + Tablero y Estantes",
        cam_frio_door_ctrl, "Unitary Equipment", MAT_SANIT,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.02", "Nivel 00 - Sotano", "und", 1.0, 1.15 * 2.05, cam_frio_door_ctrl.Volume / 1e9,
        description="Kit frigorifico completo: puerta corrediza sanitaria inox, control digital y estanterias internas",
    ))

    def build_heavy_rack_shape(rx1, ry1, rx2, ry2, max_h=2.20):
        levels = [0.18, 0.78, 1.38, 1.95] if max_h > 1.80 else [0.18, 0.72, 1.26]
        parts = []
        for px in [rx1 + 0.04, rx2 - 0.04]:
            for py in [ry1 + 0.04, ry2 - 0.04]:
                parts.append(box_house(px - 0.04, py - 0.04, Z_SOT_FLOOR, px + 0.04, py + 0.04, Z_SOT_FLOOR + max_h))
        for rz in levels:
            parts.append(box_house(rx1, ry1, Z_SOT_FLOOR + rz, rx2, ry2, Z_SOT_FLOOR + rz + 0.06))
        return compound_shapes(parts)

    racks_specs = [
        ("Rack_Mayorista_Norte_1", "Rack Industrial Pesado Norte (3,00x0,70x2,20m)", 5.85, 7.35, 8.85, 8.05, 2.20),
        ("Rack_Mayorista_Este_1",  "Rack Industrial Mural Este 1 (0,65x2,75x1,58m)", 8.25, 4.05, 8.90, 6.80, 1.58),
        ("Rack_Mayorista_Este_2",  "Rack Industrial Mural Este 2 (0,65x2,50x1,58m)", 8.25, 0.85, 8.90, 3.35, 1.58),
        ("Rack_Mayorista_Sur_SW",  "Rack Industrial Sur Suroeste (2,30x0,66x1,58m)", 0.35, 0.22, 2.65, 0.88, 1.58),
        ("Rack_Mayorista_Oeste_SW","Rack Industrial Oeste Suroeste (0,65x2,20x2,20m)", 0.35, 1.05, 1.00, 3.25, 2.20),
    ]
    for r_id, r_lbl, rx1, ry1, rx2, ry2, r_h in racks_specs:
        r_sh = build_heavy_rack_shape(rx1, ry1, rx2, ry2, max_h=r_h)
        sot_objs.append(create_bim_element(
            "Equipment", r_id, r_lbl, r_sh, "Furniture", MAT_ACERO_FORJ,
            "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.03", "Nivel 00 - Sotano", "und", 1.0, (rx2 - rx1) * (ry2 - ry1), r_sh.Volume / 1e9,
            description="Estanteria industrial selectiva para carga mayorista de frutas y tubérculos",
        ))

    bascula_ctrl_sh = compound_shapes([
        box_house(4.80, 0.35, Z_SOT_FLOOR, 5.70, 1.25, Z_SOT_FLOOR + 0.08),
        box_house(4.82, 1.15, Z_SOT_FLOOR + 0.08, 4.90, 1.23, Z_SOT_FLOOR + 1.25),
        box_house(4.78, 1.10, Z_SOT_FLOOR + 1.10, 4.98, 1.25, Z_SOT_FLOOR + 1.30),
        box_house(4.75, 1.45, Z_SOT_FLOOR, 5.70, 2.50, Z_SOT_FLOOR + 0.78),
        box_house(5.00, 2.58, Z_SOT_FLOOR, 5.48, 3.02, Z_SOT_FLOOR + 0.48),
        box_house(1.95, 1.15, Z_SOT_FLOOR, 2.72, 1.95, Z_SOT_FLOOR + 0.14),
    ])
    sot_objs.append(create_bim_element(
        "Equipment", "Estacion_Pesaje_500kg_y_Control", "Bascula Industrial Plataforma 500 kg + Mesa Control Guias",
        bascula_ctrl_sh, "Unitary Equipment", MAT_ACERO_FORJ,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.04", "Nivel 00 - Sotano", "und", 1.0, 0.90 * 0.90, bascula_ctrl_sh.Volume / 1e9,
        description="Estacion de pesaje mayorista a ras de piso (500 kg) + escritorio de recepcion y estiba",
    ))

    # Piezas sanitarias Bano Sotano
    wc_sot_sh = fuse_shapes([
        box_house(3.02, 0.25, Z_SOT_FLOOR, 3.62, 0.68, Z_SOT_FLOOR + 0.42),
        box_house(3.02, 0.25, Z_SOT_FLOOR + 0.42, 3.22, 0.68, Z_SOT_FLOOR + 0.80),
    ])
    lav_sot_sh = box_house(3.02, 1.25, Z_SOT_FLOOR + 0.50, 3.45, 1.85, Z_SOT_FLOOR + 0.85)
    mop_sot_sh = box_house(3.95, 0.25, Z_SOT_FLOOR, 4.50, 0.85, Z_SOT_FLOOR + 0.45)
    for s_id, s_lbl, s_sh, p_code in [
        ("WC_Bano_Sotano", "Inodoro (WC) Bano Operativo Sotano", wc_sot_sh, "07.01"),
        ("Lavamanos_Bano_Sotano", "Lavamanos Mural Bano Operativo Sotano", lav_sot_sh, "07.02"),
        ("Poceta_LavaMopas_Sotano", "Batea / Poceta Lava-Mopas Aseo Sotano", mop_sot_sh, "07.04"),
    ]:
        sot_objs.append(create_bim_element(
            "Equipment", s_id, s_lbl, s_sh, "Sanitary Terminal", MAT_SANIT,
            "07_INSTALACIONES_SANITARIAS", p_code, "Nivel 00 - Sotano", "und", 1.0, 0.30, s_sh.Volume / 1e9,
            description=s_lbl,
        ))

    # Espacios BIM del Sotano (IfcSpace — ocultos en vista 3D para ver el interior limpio)
    for sp_id, sp_lbl, sx1, sy1, sx2, sy2, sp_area in [
        ("IfcSpace_Sot_Bodega", "Espacio BIM: Gran Bodega Mayorista (Pasillos 1,95-2,25m)", 1.55, 0.15, 8.95, 8.15, 56.40),
        ("IfcSpace_Sot_PreFrio", "Espacio BIM: Camara Isotermica de Pre-Frio", 1.60, 5.55, 5.55, 8.10, 10.07),
        ("IfcSpace_Sot_Bano", "Espacio BIM: Bano Operativo Personal", 2.95, 0.15, 4.55, 2.55, 3.84),
        ("IfcSpace_Sot_Esclusa", "Espacio BIM: Esclusa Cerrada Escalera Sotano", 0.30, 3.55, 1.40, 8.15, 5.06),
    ]:
        sp_sh = box_house(sx1, sy1, Z_SOT_FLOOR, sx2, sy2, Z_P1_SLAB_BOT)
        sot_spaces.append(create_bim_element(
            "Space", sp_id, sp_lbl, sp_sh, "Space", None,
            "00_ESPACIOS_BIM", "00.10", "Nivel 00 - Sotano", "m2", sp_area, sp_area, sp_area * 2.40,
            description=sp_lbl, visible=False, exclude_qto=True, audit_own=True,
        ))

    # =========================================================================
    # 5. NIVEL 01: PLANTA BAJA — COMERCIO + ESTACIONAMIENTO (N.P.T. = 0,00 m)
    # =========================================================================
    pb_objs = []
    pb_spaces = []
    pb_roof_objs = []

    # 5.1 Losa de Entrepiso Planta Baja (Z = -0,15 a 0,00 m, descontando caja escalera al sotano)
    slab_pb_shape = fuse_shapes([
        box_house(0.15, 0.00, Z_P1_SLAB_BOT, 9.15, 4.40, Z_P1_FLOOR),
        box_house(0.15, 4.40, Z_P1_SLAB_BOT, 0.30, 7.35, Z_P1_FLOOR),
        box_house(1.40, 4.40, Z_P1_SLAB_BOT, 9.15, 7.35, Z_P1_FLOOR),
        box_house(0.15, 7.35, Z_P1_SLAB_BOT, 9.15, Y_AV4, Z_P1_FLOOR),
    ])
    slab_pb_vol  = slab_pb_shape.Volume / 1e9
    slab_pb_area = slab_pb_vol / 0.15
    pb_objs.append(create_bim_element(
        "Structure", "Losa_Piso_Planta_Baja", "Losa Estructural de Piso Planta Baja (9,00x21,71m Neto, e=15cm)",
        slab_pb_shape, "Slab", MAT_CONC_250,
        "03_SUPERESTRUCTURA_PISO_1", "03.01", "Nivel 01 - Planta Baja", "m3",
        slab_pb_vol, slab_pb_area, slab_pb_vol,
        description="Placa de piso/entrepiso P.B. e=15cm descontando vano de escalera al sotano (192,15 m2 netos)",
    ))

    # Acabados de piso diferenciados en Planta Baja (IfcCovering)
    piso_com_sh = fuse_shapes([
        box_house(2.90, 0.15, 0.00, 9.00, 8.80, 0.015),
        box_house(3.45, 8.80, 0.00, 9.00, 21.56, 0.015),
    ])
    piso_com_area = (piso_com_sh.Volume / 1e9) / 0.015
    pb_objs.append(create_bim_element(
        "Component", "Acabado_Porcelanato_Comercial_PB", "Piso Porcelanato Alto Trafico Salon Comercial, Barra y Oficina",
        piso_com_sh, "Covering", MAT_PORCEL,
        "04_ALBANILERIA_Y_ACABADOS", "04.06", "Nivel 01 - Planta Baja", "m2",
        piso_com_area, piso_com_area, piso_com_sh.Volume / 1e9,
        description="Acabado de porcelanato comercial antideslizante en Fruteria, Barra de Jugos y Oficina",
    ))

    piso_gar_sh = fuse_shapes([
        box_house(0.30, 8.95, 0.00, 3.30, 21.56, 0.015),
        box_house(0.30, 7.50, 0.00, 2.75, 8.80, 0.015),
    ])
    piso_gar_area = (piso_gar_sh.Volume / 1e9) / 0.015
    pb_objs.append(create_bim_element(
        "Component", "Acabado_Pavimento_Garaje_PB", "Pavimento Concreto Endurecido Estacionamiento 2 Autos y Vestibulo",
        piso_gar_sh, "Covering", MAT_PAV_GAR,
        "04_ALBANILERIA_Y_ACABADOS", "04.07", "Nivel 01 - Planta Baja", "m2",
        piso_gar_area, piso_gar_area, piso_gar_sh.Volume / 1e9,
        description="Acabado vehicular de alta resistencia para 2 plazas de estacionamiento y vestibulo residencial",
    ))

    piso_ban_sw_sh = box_house(0.30, 0.15, 0.00, 2.75, 3.50, 0.015)
    piso_ban_area  = (piso_ban_sw_sh.Volume / 1e9) / 0.015 + 3.84  # Incluye piso ceramico bano sotano
    pb_objs.append(create_bim_element(
        "Component", "Acabado_Ceramica_Banos_PB_y_Sot", "Ceramica Antideslizante e Impermeable en Nucleos de Banos",
        piso_ban_sw_sh, "Covering", MAT_CERAM_BAN,
        "04_ALBANILERIA_Y_ACABADOS", "04.08", "Nivel 01 - Planta Baja", "m2",
        piso_ban_area, piso_ban_area, piso_ban_sw_sh.Volume / 1e9,
        description="Piso ceramico antideslizante en Nucleo de Banos Suroeste P.B. (8,20 m2) y Bano Sotano (3,84 m2)",
    ))

    # 5.2 Las 32 Columnas de Concreto Armado 25x25 cm en Planta Baja (Ejes 0..3 x A0..H)
    pb_cols_grid = [
        ("0_A0", 0.275, 21.585), ("1_A0", 2.825, 21.585), ("2_A0", 5.925, 21.585), ("3_A0", 9.075, 21.585),
        ("0_A",  0.275, 18.575), ("1_A",  2.825, 18.575), ("2_A",  5.925, 18.575), ("3_A",  9.075, 18.575),
        ("0_B",  0.275, 16.325), ("1_B",  2.825, 16.325), ("2_B",  5.925, 16.325),
        ("3_C",  9.075, 14.625),
        ("0_D",  0.275, 12.025), ("1_D",  2.825, 12.025), ("2_D",  5.925, 12.025), ("3_D",  9.075, 12.025),
        ("0_E",  0.275,  8.875), ("1_E",  2.825,  8.875), ("2_E",  5.925,  8.875), ("3_E",  9.075,  8.875),
        ("0_F",  0.275,  6.575), ("1_F",  2.825,  6.575), ("2_F",  5.925,  6.575), ("3_F",  9.075,  6.575),
        ("0_G",  0.275,  3.575), ("1_G",  2.825,  3.575), ("2_G",  5.925,  3.575), ("3_G",  9.075,  3.575),
        ("0_H",  0.275,  0.125), ("1_H",  2.825,  0.125), ("2_H",  5.925,  0.125), ("3_H",  9.075,  0.125),
    ]
    pb_col_shapes = []
    for cname, cx, cy in pb_cols_grid:
        c_sh = box_house(cx - 0.125, cy - 0.125, Z_P1_FLOOR, cx + 0.125, cy + 0.125, H_P1)
        pb_col_shapes.append(c_sh)
        pb_objs.append(create_bim_element(
            "Structure", f"Col_PB_{cname}", f"Columna Concreto P.B. Nodo {cname.replace('_', '-')} (25x25cm, H=2,85m)",
            c_sh, "Column", MAT_CONC_250,
            "03_SUPERESTRUCTURA_PISO_1", "03.02", "Nivel 01 - Planta Baja", "m3",
            c_sh.Volume / 1e9, 0.25 * 0.25, c_sh.Volume / 1e9,
            description=f"Columna estructural de concreto armado f'c=250 kg/cm2 seccion 25x25 cm en eje {cname}",
        ))
    pb_cols_union = fuse_shapes(pb_col_shapes)

    # 5.3 Muros Exteriores de Planta Baja (Netos: descuentan las 32 columnas y todos los vanos!)
    w_pb_west = box_house(0.15, 0.00, Z_P1_FLOOR, X_GAR_LEFT_IN, Y_AV4, H_P1).cut(pb_cols_union)
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Ext_Oeste_PB", "Muro Exterior Oeste Propio P.B. (e=15cm Ciego sobre Lindero)",
        w_pb_west, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_pb_west.Volume / 1e9) / 0.15, (w_pb_west.Volume / 1e9) / 0.15, w_pb_west.Volume / 1e9,
        description="Muro medianero propio ciego X=0,15..0,30m (0,00 m invasion al vecino)",
    ))

    # Fachada Frontal sobre Avenida 4 (Porton Garaje + 2 Santamarias Fruteria)
    w_pb_front = box_house(0.15, Y_AV4 - 0.15, Z_P1_FLOOR, 9.15, Y_AV4, H_P1).cut(pb_cols_union)
    for ox1, ox2, oz1, oz2 in [(0.40, 2.70, 0.00, 2.40), (3.65, 5.75, 0.00, 2.40), (6.20, 8.80, 0.00, 2.40)]:
        w_pb_front = w_pb_front.cut(box_house(ox1, Y_AV4 - 0.25, oz1, ox2, Y_AV4 + 0.10, oz2))
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Fachada_Frontal_Av4_PB", "Muro Fachada Frontal Avenida 4 P.B. (e=15cm Neto)",
        w_pb_front, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_pb_front.Volume / 1e9) / 0.15, (w_pb_front.Volume / 1e9) / 0.15, w_pb_front.Volume / 1e9,
        description="Muro frontal comercial y residencial descontando Porton 2,30m y 2 Santamarias (2,10m y 2,60m)",
    ))

    # Portico Derecho Exclusivo hacia Rampa de Bodega en Av. 4 (X = 9.15..11.37 m)
    portico_bodega_muro = fuse_shapes([
        box_terr(9.15,  OFFSET_Y + Y_AV4 - 0.18, 0.00, 9.35,  OFFSET_Y + Y_AV4 + 0.02, 2.35),
        box_terr(11.12, OFFSET_Y + Y_AV4 - 0.18, 0.00, 11.37, OFFSET_Y + Y_AV4 + 0.02, 2.35),
        box_terr(9.15,  OFFSET_Y + Y_AV4 - 0.20, 2.35, 11.37, OFFSET_Y + Y_AV4 + 0.04, 2.68),
    ])
    pb_objs.append(create_bim_element(
        "Wall", "Portico_Mamposteria_Acceso_Bodega_Av4", "Portico y Dintel Acceso Exclusivo Rampa Bodega en Av. 4",
        portico_bodega_muro, "Wall", MAT_BLOQ_20,
        "04_ALBANILERIA_Y_ACABADOS", "04.03", "Nivel 01 - Planta Baja", "m2",
        (portico_bodega_muro.Volume / 1e9) / 0.20, (portico_bodega_muro.Volume / 1e9) / 0.20, portico_bodega_muro.Volume / 1e9,
        description="Machones laterales y viga dintel del acceso logistico derecho en Avenida 4",
    ))

    # Fachada Lateral Derecha sobre Eje 3 (X = 9.00..9.15 m, 7 ventanas comerciales)
    east_windows_pb = [
        ("Ventana_Este_PB_1_Oficina", 1.10,  2.50, 1.00, 2.10),
        ("Ventana_Este_PB_2_Pasillo", 4.10,  5.00, 1.10, 2.00),
        ("Ventana_Este_PB_3_Mural",   6.30,  8.00, 1.00, 2.10),
        ("Ventana_Este_PB_4_Salon",   9.65, 11.85, 1.00, 2.10),
        ("Ventana_Este_PB_5_Salon",  13.15, 14.05, 1.10, 2.00),
        ("Ventana_Este_PB_6_Salon",  15.50, 17.70, 1.00, 2.10),
        ("Ventana_Este_PB_7_Caja",   18.80, 21.00, 1.00, 2.10),
    ]
    w_pb_east = box_house(9.00, 0.00, Z_P1_FLOOR, 9.15, Y_AV4, H_P1).cut(pb_cols_union)
    for _, wy1, wy2, wz1, wz2 in east_windows_pb:
        w_pb_east = w_pb_east.cut(box_house(8.90, wy1, wz1, 9.25, wy2, wz2))
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Fachada_Este_PB", "Muro Fachada Lateral Este P.B. sobre Rampa (e=15cm Neto)",
        w_pb_east, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_pb_east.Volume / 1e9) / 0.15, (w_pb_east.Volume / 1e9) / 0.15, w_pb_east.Volume / 1e9,
        description="Muro exterior Este de Planta Baja descontando columnas y 7 ventanas comerciales",
    ))

    # Fachada Posterior Sur de Planta Baja (3 ventanales: Banos SW, Barra Jugos, Oficina)
    south_windows_pb = [
        ("Ventana_Sur_PB_1_BanosSW",  0.75, 2.35, 1.55, 2.25),
        ("Ventanal_Sur_PB_2_Jugos",   3.35, 5.45, 0.90, 2.25),
        ("Ventanal_Sur_PB_3_Oficina", 6.85, 8.45, 0.95, 2.20),
    ]
    w_pb_south = box_house(0.15, 0.00, Z_P1_FLOOR, 9.15, 0.15, H_P1).cut(pb_cols_union)
    for _, wx1, wx2, wz1, wz2 in south_windows_pb:
        w_pb_south = w_pb_south.cut(box_house(wx1, -0.10, wz1, wx2, 0.25, oz2 := wz2))
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Fachada_Sur_PB", "Muro Fachada Posterior Sur P.B. (e=15cm Neto)",
        w_pb_south, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_pb_south.Volume / 1e9) / 0.15, (w_pb_south.Volume / 1e9) / 0.15, w_pb_south.Volume / 1e9,
        description="Muro posterior Sur descontando columnas y los 3 ventanales de Banos SW, Barra Jugos y Oficina",
    ))

    # Revestimientos de Piedra Laja Rustica en Fachadas y Garaje (IfcCovering)
    zocalos_piedra_sh = compound_shapes([
        *[box_house(px1, Y_AV4 - 0.22, Z_P1_FLOOR, px2, Y_AV4, H_P1)
          for px1, px2 in [(0.15, 0.40), (2.70, 3.65), (5.75, 6.20), (8.80, 9.15)]],
        box_house(9.15, 0.00, Z_P1_FLOOR, 9.21, Y_AV4, 0.95),
        box_house(0.30, 8.95, Z_P1_FLOOR, 0.36, Y_AV4 - 0.15, 1.05),
    ])
    piedra_area_m2 = (
        (0.25 + 0.95 + 0.45 + 0.35) * 2.85 +  # Machones frontales Av. 4
        (21.71 * 0.95) +                       # Zocalo continuo fachada Este
        (12.46 * 1.05)                         # Zocalo interior garaje
    )
    pb_objs.append(create_bim_element(
        "Component", "Revestimiento_Piedra_Rustica_PB", "Enchape Piedra Laja Rustica en Machones Av.4, Este y Garaje",
        zocalos_piedra_sh, "Covering", MAT_PIEDRA,
        "04_ALBANILERIA_Y_ACABADOS", "04.05", "Nivel 01 - Planta Baja", "m2",
        piedra_area_m2, piedra_area_m2, zocalos_piedra_sh.Volume / 1e9,
        description="Revestimiento arquitectonico de piedra natural estilo chalet en machones y zocalos P.B.",
    ))

    # 5.4 Muros Interiores, Esclusas, Banos Suroeste y Oficina Acristalada
    w_div_gar = fuse_shapes([
        box_house(X_GAR_RIGHT_IN, 8.80, Z_P1_FLOOR, X_GAR_WALL_OUT, Y_AV4 - 0.15, H_P1),
        box_house(2.75, 8.80, Z_P1_FLOOR, X_GAR_WALL_OUT, 8.95, H_P1),
    ]).cut(pb_cols_union)
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Divisorio_Garaje_Fruteria", "Muro Divisorio Estacionamiento / Salon Fruteria (e=15cm Neto)",
        w_div_gar, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_div_gar.Volume / 1e9) / 0.15, (w_div_gar.Volume / 1e9) / 0.15, w_div_gar.Volume / 1e9,
        description="Pared divisoria cortafuegos y acustica entre estacionamiento (3,00m libres) y tienda",
    ))

    w_vest_esc = fuse_shapes([
        box_house(0.30, 8.80, Z_P1_FLOOR, 2.75, 8.95, H_P1),
        box_house(1.40, 4.40, Z_P1_FLOOR, 1.55, 7.50, H_P1),
        box_house(0.30, 7.35, Z_P1_FLOOR, 1.55, 7.50, H_P1),
        box_house(0.30, 4.25, Z_P1_FLOOR, 1.40, 4.40, H_P1),
        box_house(1.55, 5.65, Z_P1_FLOOR, 2.75, 5.78, 1.62),
    ]).cut(pb_cols_union)
    w_vest_esc = w_vest_esc.cut(box_house(1.60, 8.70, Z_P1_FLOOR, 2.55, 9.05, Z_P1_FLOOR + H_DOOR))
    w_vest_esc = w_vest_esc.cut(box_house(0.40, 7.25, Z_P1_FLOOR, 1.32, 7.60, Z_P1_FLOOR + H_DOOR))
    pb_objs.append(create_bim_element(
        "Wall", "Muros_Vestibulo_Escaleras_y_Aseo_PB", "Muros Esclusa Residencial Escaleras y Cuarto Aseo (e=15cm Neto)",
        w_vest_esc, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_vest_esc.Volume / 1e9) / 0.15, (w_vest_esc.Volume / 1e9) / 0.15, w_vest_esc.Volume / 1e9,
        description="Cerramiento del nucleo vertical independiente (acceso Garaje->P2 y seguridad hacia Sotano)",
    ))

    w_long_sw = fuse_shapes([
        box_house(2.75, 0.15, Z_P1_FLOOR, 2.90, 8.80, H_P1),
        box_house(0.30, 3.50, Z_P1_FLOOR, 2.75, 3.62, H_P1),
    ]).cut(pb_cols_union)
    w_long_sw = w_long_sw.cut(box_house(2.65, 2.35, Z_P1_FLOOR, 3.00, 3.20, Z_P1_FLOOR + H_DOOR))
    w_long_sw = w_long_sw.cut(box_house(2.65, 3.75, Z_P1_FLOOR, 3.00, 4.45, Z_P1_FLOOR + 1.95))
    pb_objs.append(create_bim_element(
        "Wall", "Muro_Cierre_Banos_Suroeste_PB", "Muro Principal Nucleo Banos Suroeste / Comercio (e=15cm Neto)",
        w_long_sw, "Wall", MAT_BLOQ_15,
        "04_ALBANILERIA_Y_ACABADOS", "04.02", "Nivel 01 - Planta Baja", "m2",
        (w_long_sw.Volume / 1e9) / 0.15, (w_long_sw.Volume / 1e9) / 0.15, w_long_sw.Volume / 1e9,
        description="Muro longitudinal Oeste de cierre de Banos Comerciales Suroeste y Cuarto de Aseo",
    ))

    # Tabiques internos e=10cm de Cabinas Damas PMR y Caballeros
    w_tab_banos = fuse_shapes([
        box_house(1.48, 0.15, Z_P1_FLOOR, 1.58, 3.50, H_P1),
        box_house(1.58, 1.72, Z_P1_FLOOR, 2.75, 1.82, H_P1),
    ]).cut(pb_cols_union)
    w_tab_banos = w_tab_banos.cut(box_house(1.40, 2.15, Z_P1_FLOOR, 1.66, 2.95, Z_P1_FLOOR + H_DOOR))
    w_tab_banos = w_tab_banos.cut(box_house(1.75, 1.64, Z_P1_FLOOR, 2.48, 1.90, Z_P1_FLOOR + H_DOOR))
    pb_objs.append(create_bim_element(
        "Wall", "Tabiques_Cabinas_Banos_SW_10cm", "Tabiqueria Interna Cabinas Damas PMR y Caballeros (e=10cm Neto)",
        w_tab_banos, "Wall", MAT_BLOQ_10,
        "04_ALBANILERIA_Y_ACABADOS", "04.04", "Nivel 01 - Planta Baja", "m2",
        (w_tab_banos.Volume / 1e9) / 0.10, (w_tab_banos.Volume / 1e9) / 0.10, w_tab_banos.Volume / 1e9,
        description="Tabiques divisorios livianos en bloque de 10 cm para cabinas sanitarias",
    ))

    # Cerramiento Industrial Acristalado de la Oficina de Administracion (10,05 m2)
    ofic_curtain_sh = compound_shapes([
        box_house(5.88, 3.48, 0.00, 6.12, 3.58, 0.90),
        box_house(7.05, 3.48, 0.00, 9.00, 3.58, 0.90),
        box_house(5.88, 0.15, 0.00, 5.98, 3.48, 0.90),
        box_house(5.88, 3.48, 2.20, 9.00, 3.58, H_P1),
        box_house(5.88, 0.15, 2.20, 5.98, 3.58, H_P1),
        box_house(7.05, 3.52, 0.90, 8.98, 3.55, 2.20),
        box_house(5.92, 0.20, 0.90, 5.95, 3.46, 2.20),
        *[box_house(mx_p - 0.03, 3.48, 0.00, mx_p + 0.03, 3.58, 2.20) for mx_p in [6.12, 7.05, 8.02]],
    ])
    ofic_curtain_area = (3.12 + 3.43) * 2.85 - (0.87 * 2.16)
    pb_objs.append(create_bim_element(
        "Component", "Cerramiento_Oficina_Acristalada_PB", "Tabique Industrial Hierro Negro, Zocalo Madera y Cristal Oficina",
        ofic_curtain_sh, "Curtain Wall", MAT_VIDRIO,
        "06_CARPINTERIA_MADERA_VIDRIO", "06.03", "Nivel 01 - Planta Baja", "m2",
        ofic_curtain_area, ofic_curtain_area, ofic_curtain_sh.Volume / 1e9,
        description="Cerramiento panoramico en L (6,55 ml x 2,85 m) en hierro negro, madera y cristal templado 8mm",
    ))

    # 5.5 Escalera Residencial Tramo 2 (P.B. 0,00m -> Piso 2 +3,00m, 14 peldanos)
    num_steps_p2 = 14
    step_dy_p2 = (7.35 - 4.40) / num_steps_p2
    step_dz_p2 = (Z_P2_FLOOR - Z_P1_FLOOR) / num_steps_p2
    stair2_parts = []
    for i in range(num_steps_p2):
        y_s_bot = 7.35 - (i + 1) * step_dy_p2
        y_s_top = 7.35 - i * step_dy_p2
        z_s_bot = Z_P1_FLOOR + i * step_dz_p2
        z_s_top = z_s_bot + step_dz_p2
        stair2_parts.append(box_house(1.55, y_s_bot, max(0.0, z_s_bot - 0.16), 2.65, y_s_top, z_s_top))
    stair2_shape = fuse_shapes(stair2_parts)
    pb_objs.append(create_bim_element(
        "Structure", "Escalera_Tramo2_PB_P2", "Escalera Concreto Armado Tramo 2: P.B. -> Piso 2 (14 peldanos)",
        stair2_shape, "Stair", MAT_CONC_250,
        "03_SUPERESTRUCTURA_PISO_1", "03.03", "Nivel 01 - Planta Baja", "m3",
        stair2_shape.Volume / 1e9, 1.10 * 2.95, stair2_shape.Volume / 1e9,
        description="Escalera residencial recta ancho 1,10 m (14 peldanos, Z=0,00 a +3,00 m)",
    ))

    # 5.6 Portones Especiales, Santamarias de Caracol, Puertas y Ventanas de Planta Baja
    # A. Porton Vehicular Corredizo-Articulado sobre Riel Curvo Lateral a 90 grados
    gar_gate_parts = [
        box_house(0.40, Y_AV4 - 0.22, 2.35, 3.26, Y_AV4 - 0.14, 2.42),
        box_house(2.96, 21.20,        2.35, 3.26, Y_AV4 - 0.14, 2.42),
        box_house(3.18, 18.90,        2.35, 3.28, 21.20,        2.42),
        box_house(0.40, Y_AV4 - 0.20, 0.00, 3.26, Y_AV4 - 0.15, 0.015),
        box_house(3.18, 18.90,        0.00, 3.26, Y_AV4 - 0.15, 0.015),
        box_house(2.36, Y_AV4 - 0.21, 0.03, 2.94, Y_AV4 - 0.13, 2.34),
        box_house(2.94, 21.32,        0.03, 3.22, 21.44,        2.34),
    ]
    for gy1, gy2 in [(19.00, 19.56), (19.59, 20.15), (20.18, 20.74), (20.77, 21.33)]:
        gar_gate_parts.append(box_house(3.16, gy1, 0.03, 3.26, gy2, 2.34))
        gar_gate_parts.append(box_house(3.15, gy1, 2.28, 3.27, gy1 + 0.08, 2.36))
    gar_gate_sh = compound_shapes(gar_gate_parts)
    pb_objs.append(create_bim_element(
        "Component", "Porton_Corredizo_Riel_Curvo_90_Garaje", "Porton Vehicular Corredizo-Articulado Riel Curvo 90° (2,30x2,40m)",
        gar_gate_sh, "Door", MAT_MADERA,
        "05_HERRERIA_Y_CERRAMIENTOS", "05.01", "Nivel 01 - Planta Baja", "und", 1.0, 2.30 * 2.40, gar_gate_sh.Volume / 1e9,
        description="Sistema completo de porton seccional lateral en madera/forja sobre riel curvo 90° (5 hojas + herrajes)",
    ))

    # B. Las 2 Santamarias Enrollables de Caracol en Avenida 4
    for idx_sm, (sm_x1, sm_x2) in enumerate([(3.65, 5.75), (6.20, 8.80)], start=1):
        sm_mid = 0.5 * (sm_x1 + sm_x2)
        sm_sh = compound_shapes([
            box_house(sm_x1,        Y_AV4 - 0.14, 0.00, sm_x1 + 0.07, Y_AV4 - 0.02, 2.40),
            box_house(sm_x2 - 0.07, Y_AV4 - 0.14, 0.00, sm_x2,        Y_AV4 - 0.02, 2.40),
            box_house(sm_x1 + 0.05, Y_AV4 - 0.36, 2.12, sm_x2 - 0.05, Y_AV4 - 0.04, 2.38),
            box_house(sm_x1 + 0.02, Y_AV4 - 0.39, 2.08, sm_x1 + 0.10, Y_AV4 - 0.01, 2.40),
            box_house(sm_x2 - 0.10, Y_AV4 - 0.39, 2.08, sm_x2 - 0.02, Y_AV4 - 0.01, 2.40),
            box_house(sm_x1 + 0.04, Y_AV4 - 0.12, 1.98, sm_x2 - 0.04, Y_AV4 - 0.10 + 0.06, 2.12),
            box_house(sm_mid - 0.25, Y_AV4 - 0.14, 1.99, sm_mid + 0.25, Y_AV4 - 0.02, 2.05),
        ])
        w_sm = sm_x2 - sm_x1
        pb_objs.append(create_bim_element(
            "Component", f"Santamaria_Caracol_{idx_sm}_Av4", f"Santamaria Enrollable de Caracol {idx_sm} Av. 4 ({w_sm:.2f}x2,40m)",
            sm_sh, "Door", MAT_ACERO_FORJ,
            "05_HERRERIA_Y_CERRAMIENTOS", "05.02", "Nivel 01 - Planta Baja", "und", 1.0, w_sm * 2.40, sm_sh.Volume / 1e9,
            description=f"Santamaria comercial microperforada/galvanizada con eje de caracol, carriles U y cerradura ({w_sm:.2f}x2,40m)",
        ))

    # C. Porton Derecho Exclusivo a Rampa de Bodega en Avenida 4 (1,77 x 2,34 m) + Tejadillo
    porton_der_av4_sh = compound_shapes([
        box_terr(9.35,  OFFSET_Y + Y_AV4 - 0.12, 0.02, 10.22, OFFSET_Y + Y_AV4 - 0.04, 2.34),
        box_terr(10.25, OFFSET_Y + Y_AV4 - 0.12, 0.02, 11.12, OFFSET_Y + Y_AV4 - 0.04, 2.34),
    ])
    pb_objs.append(create_bim_element(
        "Component", "Porton_Derecho_Bodega_Av4", "Porton Metalico Doble Acceso Rampa Bodega Av. 4 (1,77x2,34m)",
        porton_der_av4_sh, "Door", MAT_ACERO_FORJ,
        "05_HERRERIA_Y_CERRAMIENTOS", "05.03", "Nivel 01 - Planta Baja", "und", 1.0, 1.77 * 2.34, porton_der_av4_sh.Volume / 1e9,
        description="Puerta doble comercial en forja negra sobre Av. 4 exclusiva hacia la rampa del sotano",
    ))

    # D. Las 7 Puertas Interiores de Planta Baja
    interior_doors_pb = [
        ("Puerta_Residencial_Vestibulo_P2", "Puerta Principal Residencial Garaje <-> Escalera P2 (0,95x2,10m)",
         compound_shapes([
             box_house(1.56, 8.78, 0.00, 1.62, 8.97, H_DOOR),
             box_house(2.53, 8.78, 0.00, 2.59, 8.97, H_DOOR),
             box_house(2.48, 7.92, 0.02, 2.54, 8.80, H_DOOR),
         ]), MAT_MADERA, "06_CARPINTERIA_MADERA_VIDRIO", "06.01", 0.95 * 2.10),
        ("Puerta_Seguridad_Arranque_Sotano", "Puerta Metalica Seguridad Arranque Escalera a Sotano (0,92x2,10m)",
         box_house(0.40, 7.38, 0.02, 1.32, 7.45, H_DOOR),
         MAT_ACERO_FORJ, "05_HERRERIA_Y_CERRAMIENTOS", "05.06", 0.92 * 2.10),
        ("Puerta_Entrada_Antebano_SW", "Puerta Acceso Antebano Clientes/Personal Suroeste (0,85x2,10m)",
         box_house(2.20, 3.14, 0.02, 2.75, 3.20, H_DOOR - 0.02),
         MAT_MADERA, "06_CARPINTERIA_MADERA_VIDRIO", "06.01", 0.85 * 2.10),
        ("Puerta_Cuarto_Aseo_Bajo_Esc", "Puerta Cuarto de Aseo Diario Bajo Escalera (0,70x1,95m)",
         box_house(2.25, 4.39, 0.02, 2.75, 4.45, 1.93),
         MAT_MADERA, "06_CARPINTERIA_MADERA_VIDRIO", "06.01", 0.70 * 1.95),
        ("Puerta_Cabina_Damas_PMR", "Puerta Cabina Sanitaria Damas / PMR (0,80x2,10m)",
         box_house(0.92, 2.90, 0.02, 1.48, 2.95, H_DOOR - 0.02),
         MAT_MADERA, "06_CARPINTERIA_MADERA_VIDRIO", "06.01", 0.80 * 2.10),
        ("Puerta_Cabina_Caballeros", "Puerta Cabina Sanitaria Caballeros (0,73x2,10m)",
         box_house(2.43, 1.10, 0.02, 2.48, 1.72, H_DOOR - 0.02),
         MAT_MADERA, "06_CARPINTERIA_MADERA_VIDRIO", "06.01", 0.73 * 2.10),
        ("Puerta_Cristal_Templado_Oficina", "Puerta Batiente Cristal Templado 10mm Oficina Admin (0,87x2,16m)",
         box_house(6.96, 2.68, 0.03, 7.02, 3.48, 2.16),
         MAT_VIDRIO, "06_CARPINTERIA_MADERA_VIDRIO", "06.04", 0.87 * 2.16),
    ]
    for d_id, d_lbl, d_sh, d_mat, d_chap, d_code, d_area in interior_doors_pb:
        pb_objs.append(create_bim_element(
            "Component", d_id, d_lbl, d_sh, "Door", d_mat,
            d_chap, d_code, "Nivel 01 - Planta Baja", "und", 1.0, d_area, d_sh.Volume / 1e9,
            description=d_lbl,
        ))

    # E. Las 10 Ventanas Rusticas Exteriores de Planta Baja (7 Este + 3 Sur)
    for wname, wy1, wy2, wz1, wz2 in east_windows_pb:
        has_sh = (wy2 - wy1) >= 1.40
        w_sh = build_window_east_shape(wy1, wy2, wz1, wz2, with_shutters=has_sh)
        area_w = (wy2 - wy1) * (wz2 - wz1)
        pb_objs.append(create_bim_element(
            "Component", wname, f"{wname.replace('_', ' ')} ({wy2-wy1:.2f}x{wz2-wz1:.2f}m)",
            w_sh, "Window", MAT_MADERA,
            "06_CARPINTERIA_MADERA_VIDRIO", "06.02", "Nivel 01 - Planta Baja", "und", 1.0, area_w, w_sh.Volume / 1e9,
            description=f"Ventana rustica de madera y cristal en fachada Este ({wy2-wy1:.2f}x{wz2-wz1:.2f}m)",
        ))

    for wname, wx1, wx2, wz1, wz2 in south_windows_pb:
        has_sh = (wx2 - wx1) >= 1.40
        w_sh = build_window_south_shape(wx1, wx2, wz1, wz2, with_shutters=has_sh)
        area_w = (wx2 - wx1) * (wz2 - wz1)
        pb_objs.append(create_bim_element(
            "Component", wname, f"{wname.replace('_', ' ')} ({wx2-wx1:.2f}x{wz2-wz1:.2f}m)",
            w_sh, "Window", MAT_MADERA,
            "06_CARPINTERIA_MADERA_VIDRIO", "06.02", "Nivel 01 - Planta Baja", "und", 1.0, area_w, w_sh.Volume / 1e9,
            description=f"Ventanal rustico de madera y cristal en fachada Sur ({wx2-wx1:.2f}x{wz2-wz1:.2f}m)",
        ))

    # 5.7 Envigado Decorativo de Madera y Revestimiento de Columnas en Salon Comercial
    timber_pb_parts = [
        box_terr(9.12, OFFSET_Y + Y_AV4 - 0.26, 2.68, 11.37, OFFSET_Y + Y_AV4 + 0.08, 2.84),
        box_house(5.82, 3.58, 2.65, 6.03, Y_AV4 - 0.15, 2.85),
        box_house(3.55, Y_AV4 - 0.16, 2.42, 8.90, Y_AV4, 2.52),
        box_house(3.55, Y_AV4 - 0.18, 2.52, 8.90, Y_AV4, 2.70),
    ]
    for vy in [18.575, 16.325, 12.025, 8.875, 6.575]:
        x_w_start = X_GAR_WALL_OUT if vy > 8.80 else 2.90
        timber_pb_parts.append(box_house(x_w_start, vy - 0.105, 2.65, 8.95, vy + 0.105, 2.85))
        if vy > 8.80:
            timber_pb_parts.append(box_house(0.30, vy - 0.105, 2.65, X_GAR_RIGHT_IN, vy + 0.105, 2.85))
        clad_box = box_house(5.735, vy - 0.19, Z_P1_FLOOR, 6.115, vy + 0.19, 2.65).cut(
            box_house(5.775, vy - 0.15, Z_P1_FLOOR - 0.05, 6.075, vy + 0.15, 2.70)
        )
        timber_pb_parts.append(clad_box)
    timber_pb_sh = compound_shapes(timber_pb_parts)
    timber_vol = sum(p.Volume for p in timber_pb_parts) / 1e9
    pb_objs.append(create_bim_element(
        "Structure", "Envigado_y_Forrados_Madera_Chalet_PB", "Vigas Vistas y Forrado de 5 Columnas en Madera Maciza P.B.",
        timber_pb_sh, "Beam", MAT_MADERA,
        "06_CARPINTERIA_MADERA_VIDRIO", "06.05", "Nivel 01 - Planta Baja", "m3",
        timber_vol, timber_vol / 0.05, timber_vol,
        description="Envigado decorativo de techo, dintel comercial, tejadillo bodega y revestimiento de 5 columnas centrales",
    ))

    # 5.8 SUBGRUPO DE CIERRE ESTRUCTURAL SUPERIOR SOBRE PISO 1 (Vigas + Placa Z=+2,85..+3,00m)
    # Permite contabilizar el Piso 1 cerrado con su placa de techo completa, o consultarlo por separado!
    beam_boxes = []
    for gx_b in [0.275, 2.825, 5.925, 9.025]:
        beam_boxes.append(box_house(max(0.15, gx_b - 0.125), 0.00, H_P1 - 0.30, min(9.15, gx_b + 0.125), Y_AV4, H_P1))
    for gy_b in [0.125, 3.575, 6.575, 8.875, 12.025, 16.325, 18.575, 21.585]:
        beam_boxes.append(box_house(0.15, gy_b - 0.125, H_P1 - 0.30, 9.15, gy_b + 0.125, H_P1))
    beams_p1_shape = fuse_shapes(beam_boxes).cut(pb_cols_union)
    beams_p1_vol = beams_p1_shape.Volume / 1e9
    pb_roof_objs.append(create_bim_element(
        "Structure", "Vigas_Sismicas_Corona_Piso1", "Vigas de Carga y Amarre Sismico Corona Piso 1 (25x30cm Netas)",
        beams_p1_shape, "Beam", MAT_CONC_250,
        "03_SUPERESTRUCTURA_PISO_1", "03.04", "Cierre Techo Piso 1 (+2,85m)", "m3",
        beams_p1_vol, beams_p1_vol / 0.30, beams_p1_vol,
        description="Reticula completa de vigas de concreto armado 25x30 cm sobre los ejes 0..3 y A0..H",
    ))

    slab_top_p1 = fuse_shapes([
        box_house(0.15, 0.00, H_P1, 9.15, 4.40, Z_P2_FLOOR),
        box_house(0.15, 4.40, H_P1, 1.55, 7.35, Z_P2_FLOOR),
        box_house(2.65, 4.40, H_P1, 9.15, 7.35, Z_P2_FLOOR),
        box_house(0.15, 7.35, H_P1, 9.15, Y_AV4, Z_P2_FLOOR),
    ])
    slab_top_vol  = slab_top_p1.Volume / 1e9
    slab_top_area = slab_top_vol / 0.15
    pb_roof_objs.append(create_bim_element(
        "Structure", "Losa_Techo_Entrepiso_Sobre_Piso1", "Placa Estructural de Techo / Entrepiso sobre Piso 1 (Z=+2,85..+3,00m)",
        slab_top_p1, "Slab", MAT_CONC_250,
        "03_SUPERESTRUCTURA_PISO_1", "03.05", "Cierre Techo Piso 1 (+2,85m)", "m3",
        slab_top_vol, slab_top_area, slab_top_vol,
        description="Losa de entrepiso superior e=15cm que techa la Zona Comercial y el Garaje (descuenta hueco Escalera Tramo 2)",
    ))

    # 5.9 Mobiliario Comercial Fijo, Barra de Jugos, Oficina y Piezas Sanitarias de Planta Baja
    for idx_isl, (ix1, ix2, iy1, iy2) in enumerate([
        (5.15, 6.30, 17.95, 19.20),
        (5.15, 6.70, 15.55, 17.10),
        (5.15, 6.70, 11.25, 12.80),
        (5.15, 6.70,  8.10,  9.65),
        (5.15, 6.70,  5.30,  6.85),
    ], start=1):
        isl_sh = compound_shapes([
            box_house(ix1 + 0.10, iy1 + 0.10, 0.00, ix2 - 0.10, iy2 - 0.10, 0.32),
            box_house(ix1, iy1, 0.32, ix2, iy2, 0.68),
            box_house(ix1 + 0.22, iy1 + 0.22, 0.76, ix2 - 0.22, iy2 - 0.22, 1.04),
        ])
        pb_objs.append(create_bim_element(
            "Equipment", f"Isla_Exhibicion_Frutas_{idx_isl}", f"Isla Central Piramidal Fruteria {idx_isl} (Base Piedra + Madera)",
            isl_sh, "Furniture", MAT_MADERA,
            "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.05", "Nivel 01 - Planta Baja", "und",
            1.0, (ix2 - ix1) * (iy2 - iy1), isl_sh.Volume / 1e9,
            description=f"Isla de exhibicion central #{idx_isl} con zocalo en mamposteria/piedra y bandejas de roble",
        ))

    estantes_salon_sh = compound_shapes([
        *[box_house(3.46, 9.00, z_sh, 4.05, 20.60, z_sh + 0.10) for z_sh in [0.52, 0.98, 1.44]],
        *[box_house(2.91, 4.65, z_sh, 3.50, 8.70,  z_sh + 0.10) for z_sh in [0.52, 0.98, 1.44]],
        box_house(8.35, 7.80, 0.25, 8.98, 16.50, 0.58),
    ])
    pb_objs.append(create_bim_element(
        "Equipment", "Estanterias_Murales_Fruteria_PB", "Bateria de Estanterias Murales Oeste y Este en Madera Roble",
        estantes_salon_sh, "Furniture", MAT_MADERA,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.06", "Nivel 01 - Planta Baja", "ml",
        (20.60 - 9.00) + (8.70 - 4.65) + (16.50 - 7.80), 15.20, estantes_salon_sh.Volume / 1e9,
        description="24,35 metros lineales de exhibidores murales escalonados en madera tratada",
    ))

    mural_frio_sh = compound_shapes([
        box_house(8.26, 5.10, 0.00, 8.98, 7.55, 2.05),
        box_house(8.24, 5.20, 0.45, 8.30, 7.45, 1.85),
        *[box_house(8.32, 5.20, z_fr, 8.92, 7.45, z_fr + 0.05) for z_fr in [0.55, 0.95, 1.35]],
    ])
    pb_objs.append(create_bim_element(
        "Equipment", "Mural_Frigorifico_Lacteos_PB", "Mural Frigorifico Vertical Abierto Lacteos y Fruta Picada (2,45m)",
        mural_frio_sh, "Unitary Equipment", MAT_SANIT,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.07", "Nivel 01 - Planta Baja", "und",
        1.0, 0.72 * 2.45, mural_frio_sh.Volume / 1e9,
        description="Exhibidor refrigerado multirepisa de cortina de aire (2,45 x 0,72 x 2,05 m)",
    ))

    caja_princ_sh = compound_shapes([
        box_house(7.05, 18.25, 0.00, 8.75, 18.95, 0.92),
        box_house(7.05, 17.05, 0.00, 7.70, 18.25, 0.92),
        box_house(6.98, 18.20, 0.92, 8.80, 19.02, 1.00),
        box_house(6.98, 17.00, 0.92, 7.76, 18.20, 1.00),
    ])
    pb_objs.append(create_bim_element(
        "Equipment", "Mostrador_Caja_y_Pesaje_PB", "Mostrador Principal en 'L' de Caja y Pesaje (Piedra + Madera)",
        caja_princ_sh, "Furniture", MAT_PIEDRA,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.08", "Nivel 01 - Planta Baja", "und",
        1.0, 2.95, caja_princ_sh.Volume / 1e9,
        description="Mueble fijo de facturacion y balanzas en acceso Av. 4 con frente en piedra rustica",
    ))

    barra_jugos_sh = compound_shapes([
        box_house(3.60, 2.85, 0.00, 5.75, 3.48, 0.95),
        box_house(3.55, 2.78, 0.95, 5.80, 3.56, 1.04),
        box_house(4.65, 2.85, 1.04, 5.72, 3.48, 1.42),
        box_house(3.05, 0.18, 0.00, 5.75, 0.85, 0.92),
        *[box_house(bs_x - 0.16, 3.68, 0.00, bs_x + 0.16, 4.00, 0.72) for bs_x in [3.75, 4.28, 4.81, 5.34]],
    ])
    pb_objs.append(create_bim_element(
        "Equipment", "Barra_Gourmet_Jugos_y_Cafe_Sur", "Barra Gourmet Jugos y Cafe Sur + Vitrina Fria + Contra-Barra + 4 Bancos",
        barra_jugos_sh, "Furniture", MAT_PIEDRA,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.09", "Nivel 01 - Planta Baja", "und",
        1.0, 3.85, barra_jugos_sh.Volume / 1e9,
        description="Conjunto de barra de atencion en piedra/madera, vitrina refrigerada, contra-barra Sur y 4 taburetes",
    ))

    fregadero_barra_sh = box_house(3.35, 0.28, 0.88, 4.15, 0.72, 0.96)
    pb_objs.append(create_bim_element(
        "Equipment", "Fregadero_Doble_Inox_Barra_PB", "Fregadero Industrial Doble Tina Acero Inox en Barra de Jugos",
        fregadero_barra_sh, "Sanitary Terminal", MAT_SANIT,
        "07_INSTALACIONES_SANITARIAS", "07.05", "Nivel 01 - Planta Baja", "und",
        1.0, 0.80 * 0.44, fregadero_barra_sh.Volume / 1e9,
        description="Fregadero doble en acero inoxidable con griferia comercial para preparacion de jugos",
    ))

    ofic_furn_sh = compound_shapes([
        box_house(7.25, 1.45, 0.00, 8.65, 2.15, 0.76),
        box_house(8.05, 0.85, 0.00, 8.65, 1.45, 0.76),
        box_house(7.65, 0.85, 0.00, 8.15, 1.35, 0.95),
        box_house(6.45, 2.25, 0.00, 6.90, 2.70, 0.80),
        box_house(7.35, 2.30, 0.00, 7.80, 2.75, 0.80),
        box_house(6.15, 0.20, 0.00, 7.55, 0.65, 0.95),
    ])
    pb_objs.append(create_bim_element(
        "Equipment", "Mobiliario_Oficina_Administracion_PB", "Juego Mobiliario Oficina Admin (Escritorio en L, Credenza y 3 Sillas)",
        ofic_furn_sh, "Furniture", MAT_MADERA,
        "08_EQUIPAMIENTO_COMERCIAL_FRIO", "08.10", "Nivel 01 - Planta Baja", "und",
        1.0, 2.60, ofic_furn_sh.Volume / 1e9,
        description="Equipamiento completo de oficina administrativa y atencion a proveedores",
    ))

    # Piezas Sanitarias Nucleo Suroeste P.B. (Damas PMR + Caballeros + Antebano Doble)
    tocador_sw_sh = box_house(1.62, 3.02, 0.00, 2.68, 3.48, 0.85)
    pb_objs.append(create_bim_element(
        "Equipment", "Tocador_Doble_Antebano_SW", "Mueble Tocador Doble en Madera/Piedra para Antebano Suroeste",
        tocador_sw_sh, "Furniture", MAT_MADERA,
        "07_INSTALACIONES_SANITARIAS", "07.06", "Nivel 01 - Planta Baja", "und",
        1.0, 1.06 * 0.46, tocador_sw_sh.Volume / 1e9,
        description="Meson de lavamanos doble en antebano comercial (1,06 x 0,46 m)",
    ))

    sanit_pb_specs = [
        ("Lavamanos_Antebano_1", "Lavamanos Sobre-Tope 1 Antebano Suroeste",
         box_house(1.72, 3.10, 0.85, 2.08, 3.40, 0.95), "07.02"),
        ("Lavamanos_Antebano_2", "Lavamanos Sobre-Tope 2 Antebano Suroeste",
         box_house(2.22, 3.10, 0.85, 2.58, 3.40, 0.95), "07.02"),
        ("WC_Damas_PMR_PB", "Inodoro (WC) Elongado Cabina Damas / PMR P.B.",
         fuse_shapes([box_house(0.42, 0.25, 0.00, 0.95, 0.78, 0.42), box_house(0.42, 0.25, 0.42, 0.62, 0.78, 0.80)]), "07.01"),
        ("WC_Caballeros_PB", "Inodoro (WC) Cabina Caballeros P.B.",
         fuse_shapes([box_house(1.78, 0.25, 0.00, 2.25, 0.75, 0.42), box_house(1.78, 0.25, 0.42, 2.25, 0.45, 0.80)]), "07.01"),
        ("Urinario_Caballeros_PB", "Urinario Mural Ecologico Cabina Caballeros P.B.",
         box_house(2.42, 0.95, 0.45, 2.70, 1.35, 1.05), "07.03"),
    ]
    for s_id, s_lbl, s_sh, p_code in sanit_pb_specs:
        pb_objs.append(create_bim_element(
            "Equipment", s_id, s_lbl, s_sh, "Sanitary Terminal", MAT_SANIT,
            "07_INSTALACIONES_SANITARIAS", p_code, "Nivel 01 - Planta Baja", "und",
            1.0, 0.28, s_sh.Volume / 1e9,
            description=s_lbl,
        ))

    # Espacios BIM de Planta Baja (IfcSpace — ocultos por defecto para inspeccion limpia)
    for sp_id, sp_lbl, sx1, sy1, sx2, sy2, sp_area in [
        ("IfcSpace_PB_Fruteria",  "Espacio BIM: Salon Fruteria Ampliado (Sin Bodega en PB)", 3.45, 3.58, 9.00, 21.56, 111.80),
        ("IfcSpace_PB_BarraJugos","Espacio BIM: Barra Gourmet Jugos y Cafe Sur",             2.90, 0.15, 5.88,  3.58,  10.60),
        ("IfcSpace_PB_Oficina",   "Espacio BIM: Oficina Administracion Acristalada",         5.95, 0.15, 9.00,  3.48,  10.05),
        ("IfcSpace_PB_BanosSW",   "Espacio BIM: Nucleo Banos Suroeste (Damas/Caballeros)",   0.30, 0.15, 2.75,  3.50,   8.20),
        ("IfcSpace_PB_Garaje",    "Espacio BIM: Estacionamiento Cubierto 2 Vehiculos",       0.30, 8.95, 3.30, 21.56,  37.83),
        ("IfcSpace_PB_Vestibulo", "Espacio BIM: Vestibulo Cerrado de Escaleras",             0.30, 4.40, 2.75,  8.80,   6.67),
    ]:
        sp_sh = box_house(sx1, sy1, Z_P1_FLOOR, sx2, sy2, H_P1)
        pb_spaces.append(create_bim_element(
            "Space", sp_id, sp_lbl, sp_sh, "Space", None,
            "00_ESPACIOS_BIM", "00.20", "Nivel 01 - Planta Baja", "m2", sp_area, sp_area, sp_area * H_P1,
            description=sp_lbl, visible=False, exclude_qto=True, audit_own=True,
        ))

    # =========================================================================
    # 6. ENSAMBLAJE JERARQUICO NORMATIVO IFC4 (Site -> Building -> Storeys)
    # =========================================================================
    sot_space_grp = doc.addObject("App::DocumentObjectGroup", "Espacios_BIM_Sotano")
    sot_space_grp.Label = "Espacios_IfcSpace_Sotano (Activar para ver zonas)"
    sot_space_grp.Visibility = False
    for sp in sot_spaces:
        sot_space_grp.addObject(sp)

    pb_space_grp = doc.addObject("App::DocumentObjectGroup", "Espacios_BIM_PlantaBaja")
    pb_space_grp.Label = "Espacios_IfcSpace_PlantaBaja (Activar para ver zonas)"
    pb_space_grp.Visibility = False
    for sp in pb_spaces:
        pb_space_grp.addObject(sp)

    cierre_p1_part = Arch.makeBuildingPart(pb_roof_objs, name="Subgrupo_Cierre_Techo_Piso1")
    cierre_p1_part.Label = "Cierre_Estructural_Techo_Sobre_Piso1 (Z=+2,85..+3,00m)"
    cierre_p1_part.IfcType = "Building Element Part"

    storey_sot = Arch.makeFloor(sot_objs + [sot_space_grp], name="Nivel_00_Sotano_Bodega")
    storey_sot.Label = "Nivel 00: Sotano — Gran Bodega Mayorista (N.P.T. -2,55 m)"
    storey_sot.Placement.Base = FreeCAD.Vector(0, 0, 0)  # Geometrias ya ubicadas en cota Z real

    storey_pb = Arch.makeFloor(pb_objs + [cierre_p1_part, pb_space_grp], name="Nivel_01_Planta_Baja")
    storey_pb.Label = "Nivel 01: Planta Baja — Fruteria, Barra, Oficina y Garaje (N.P.T. 0,00 m)"
    storey_pb.Placement.Base = FreeCAD.Vector(0, 0, 0)

    building = Arch.makeBuilding([storey_sot, storey_pb, axes_grp], name="Edificacion_Casa_Comercio")
    building.Label = "Edificacion Casa Chalet & Comercio (Fase 1 BIM)"

    site = Arch.makeSite(site_objs + [building], name="Parcela_Av4_Independencia")
    site.Label = "Sitio Poligonal Av. 4 entre Calles 30 y 31 (273,81 m2)"

    doc.recompute()

    # =========================================================================
    # 7. AUDITORIA AUTOMATICA DE SOLIDOS Y LINDERO IZQUIERDO (minX >= 150 mm)
    # =========================================================================
    invalid_solids = []
    min_x_mm = float("inf")
    min_x_label = ""
    for lbl, b_obj, shp in own_shapes_for_audit:
        if shp.isNull() or not shp.isValid() or b_obj.Shape.isNull():
            invalid_solids.append(lbl)
        bx_min = b_obj.Shape.BoundBox.XMin
        if bx_min < min_x_mm:
            min_x_mm = bx_min
            min_x_label = lbl

    assert not invalid_solids, f"ERROR: Solidos invalidos detectados: {invalid_solids}"
    assert min_x_mm >= 149.9, f"INVASION DE LINDERO DETECTADA en {min_x_label}: XMin = {min_x_mm} mm (< 150 mm)"

    print(f"  [OK] Auditoria geometrica superada: {len(own_shapes_for_audit)} elementos propios 100% validos.")
    print(f"  [OK] Respeto estricto de lindero vecino: XMin obra propia = {min_x_mm/MM:.4f} m (>= 0,1500 m).")

    # =========================================================================
    # 8. AGREGACION DE PARTIDAS, INSUMOS COMERCIALES Y SPREADSHEET FREECAD
    # =========================================================================
    PARTIDA_TITULOS = {
        "01.01": "Excavacion Mecanica en Corte (Sotano, Patio y Rampa)",
        "02.01": "Zapatas Aisladas de Fundacion Sotano (f'c=280 kg/cm2)",
        "02.02": "Losa de Fundacion Gran Bodega Sotano e=15cm (f'c=280)",
        "02.03": "Losa Pavimento Armado Patio de Maniobra Sur (f'c=280)",
        "02.04": "Rampa Logistica Continua 18% y Corredor Este e=20cm",
        "02.05": "Muro Contencion Lateral Bajo P.B. Junto a Rampa",
        "02.06": "Columnas Estructurales Sotano 35x35cm (12 apoyos, f'c=280)",
        "02.07": "Muros de Contencion Perimetrales Sotano (Oeste y Norte)",
        "02.08": "Escalera Concreto Armado Tramo 1: Sotano -> P.B. (12 peld.)",
        "03.01": "Losa Estructural de Entrepiso Planta Baja e=15cm (f'c=250)",
        "03.02": "Columnas Concreto Armado P.B. 25x25cm (32 nodos, f'c=250)",
        "03.03": "Escalera Concreto Armado Tramo 2: P.B. -> Piso 2 (14 peld.)",
        "03.04": "Vigas Sismicas y de Carga Corona Piso 1 (25x30cm Netas)",
        "03.05": "Placa Estructural de Techo / Entrepiso sobre Piso 1 (e=15cm)",
        "04.01": "Cerramiento Perimetral Sur y Este en Bloque e=15cm (H=2,20m)",
        "04.02": "Muros Exteriores y Divisorios en Bloque e=15cm (Netos sin vanos)",
        "04.03": "Mamposteria Estructural Pesada en Bloque Concreto e=20cm",
        "04.04": "Tabiqueria Divisoria Interna en Bloque e=10cm (Cabinas Banos)",
        "04.05": "Revestimiento de Piedra Laja Rustica en Machones y Zocalos",
        "04.06": "Piso Porcelanato Antideslizante Alto Trafico Comercial",
        "04.07": "Pavimento Vehicular Endurecido en Garaje y Vestibulo",
        "04.08": "Piso Ceramico Antideslizante Impermeable en Banos",
        "05.01": "Porton Vehicular Corredizo-Articulado Riel Curvo 90° (2,30x2,40m)",
        "05.02": "Santamarias Enrollables de Caracol Comerciales Av. 4 (2 und)",
        "05.03": "Porton Metalico Doble Acceso Exclusivo Bodega Av. 4 (1,77x2,34m)",
        "05.04": "Porton Doble Metalico Reforzado Carga Sotano (2,20x2,10m)",
        "05.05": "Ventanas Altas Basculantes en Hierro con Reja Seguridad Sotano",
        "05.06": "Puertas Metalicas Entamboradas de Seguridad (Esclusa Sotano/PB)",
        "06.01": "Puertas Batientes de Madera Maciza / Entamborada con Marco",
        "06.02": "Ventanas y Ventanales Rusticos de Madera y Cristal en P.B.",
        "06.03": "Cerramiento Industrial Hierro Negro, Madera y Cristal Oficina",
        "06.04": "Puerta Batiente de Cristal Templado 10mm Oficina Admin.",
        "06.05": "Vigas Decorativas de Techo y Forrado Hueco de 5 Columnas Madera",
        "07.01": "Inodoros (WC) de Porcelana Vitrificada (Sotano + Damas + Cab.)",
        "07.02": "Lavamanos con Griferia (Bano Sotano + Doble Antebano P.B.)",
        "07.03": "Urinario Mural Ecologico en Cabina Caballeros P.B.",
        "07.04": "Batea / Poceta Lava-Mopas en Cuarto Sanitario Sotano",
        "07.05": "Fregadero Industrial Doble Tina Acero Inox en Barra de Jugos",
        "07.06": "Mueble Tocador Doble para Lavamanos en Antebano Suroeste",
        "08.01": "Paneleria Frigorifica Isotermica PIR e=12cm Camara Pre-Frio",
        "08.02": "Puerta Corrediza Inox Camara Pre-Frio + Control Digital + Racks",
        "08.03": "Baterias de Racks Industriales Pesados en Bodega Mayorista",
        "08.04": "Bascula Industrial Plataforma 500 kg + Mesa Control Guias",
        "08.05": "Islas Centrales Piramidales de Exhibicion Fruteria (Base Piedra)",
        "08.06": "Estanterias Murales Escalonadas de Madera en Salon Comercial",
        "08.07": "Mural Frigorifico Vertical Abierto Lacteos y Fruta Picada (2,45m)",
        "08.08": "Mostrador Principal en 'L' de Caja y Pesaje (Piedra + Madera)",
        "08.09": "Barra Gourmet de Jugos y Cafe Sur + Vitrina Fria + 4 Taburetes",
        "08.10": "Mobiliario Completo Oficina Administracion (Escritorio L + Sillas)",
    }

    # Agrupar registros por (capitulo, codigo, nivel, unidad, material)
    grouped = {}
    for rec in qto_records:
        key = (rec["capitulo"], rec["codigo"], rec["nivel"], rec["unidad"], rec["material"])
        if key not in grouped:
            grouped[key] = {
                "capitulo": rec["capitulo"],
                "codigo": rec["codigo"],
                "partida": PARTIDA_TITULOS.get(rec["codigo"], rec["material"]),
                "nivel": rec["nivel"],
                "unidad": rec["unidad"],
                "material": rec["material"],
                "elementos": 0,
                "cantidad": 0.0,
                "area_m2": 0.0,
                "volumen_m3": 0.0,
                "ejemplos": [],
            }
        g = grouped[key]
        g["elementos"] += 1
        g["cantidad"] += rec["cantidad"]
        g["area_m2"] += rec["area_m2"]
        g["volumen_m3"] += rec["volumen_m3"]
        if len(g["ejemplos"]) < 2:
            g["ejemplos"].append(rec["nombre"])

    partidas_ordenadas = sorted(grouped.values(), key=lambda x: (x["codigo"], x["nivel"]))

    # Calculos globales para resumen de compra de materiales
    vol_conc_280 = sum(r["volumen_m3"] for r in qto_records if "280" in r["material"] or "Contencion" in r["material"])
    vol_conc_250_sin_techo = sum(
        r["volumen_m3"] for r in qto_records
        if "250" in r["material"] and "Cierre Techo Piso 1" not in r["nivel"]
    )
    vol_conc_250_techo = sum(
        r["volumen_m3"] for r in qto_records
        if "250" in r["material"] and "Cierre Techo Piso 1" in r["nivel"]
    )
    vol_conc_total = vol_conc_280 + vol_conc_250_sin_techo + vol_conc_250_techo

    m2_bloq_20 = sum(r["area_m2"] for r in qto_records if "e=20cm" in r["material"])
    m2_bloq_15 = sum(r["area_m2"] for r in qto_records if "e=15cm" in r["material"] and "Contencion" not in r["material"])
    m2_bloq_10 = sum(r["area_m2"] for r in qto_records if "e=10cm" in r["material"])
    m2_muros_friso = (m2_bloq_20 + m2_bloq_15 + m2_bloq_10) * 2.0  # Ambas caras netas
    m2_imperm_sot = sum(r["area_m2"] for r in qto_records if r["codigo"] == "02.07") + (9.00 * 8.30)

    m2_piedra    = sum(r["area_m2"] for r in qto_records if r["codigo"] == "04.05")
    m2_porcel    = sum(r["area_m2"] for r in qto_records if r["codigo"] == "04.06")
    m2_pav_gar   = sum(r["area_m2"] for r in qto_records if r["codigo"] == "04.07")
    m2_ceram_ban = sum(r["area_m2"] for r in qto_records if r["codigo"] == "04.08") + (m2_bloq_10 * 2.0)

    # Estimacion de insumos comerciales estandar de ingenieria civil (con 5% desperdicio)
    # Concreto f'c 280: ~8.8 sacos cemento (42.5kg)/m3 | f'c 250: ~8.0 sacos/m3
    # Mortero pega + friso (e_prom = 1.8 cm): ~0.22 sacos cemento / m2 de cara frisada/pegada
    sacos_cem_concreto = math.ceil((vol_conc_280 * 8.8 + (vol_conc_250_sin_techo + vol_conc_250_techo) * 8.0) * 1.05)
    sacos_cem_albanil  = math.ceil(((m2_bloq_20 + m2_bloq_15 + m2_bloq_10) * 0.18 + m2_muros_friso * 0.16 + m2_piedra * 0.25) * 1.05)
    sacos_cemento_tot  = sacos_cem_concreto + sacos_cem_albanil

    arena_lavada_m3 = round(vol_conc_total * 0.48 + m2_muros_friso * 0.022, 1)
    piedra_picada_m3 = round(vol_conc_total * 0.72, 1)

    # Acero de refuerzo estimado por cuantia tipica sismorresistente (COVENIN 1753):
    # Losas/Rampa ~65 kg/m3, Zapatas ~75 kg/m3, Columnas/Vigas/Escaleras ~135 kg/m3
    vol_cols_vigas_esc = sum(
        r["volumen_m3"] for r in qto_records
        if r["ifc_type"] in ("Column", "Beam", "Stair") and "Concreto" in r["material"]
    )
    vol_losas_zapatas = vol_conc_total - vol_cols_vigas_esc
    acero_refuerzo_kg = math.ceil((vol_cols_vigas_esc * 135.0 + vol_losas_zapatas * 70.0) * 1.05)

    # Bloques comerciales (12.5 bloques/m2 + 5% desperdicio de corte)
    und_bloq_20 = math.ceil(m2_bloq_20 * 12.5 * 1.05)
    und_bloq_15 = math.ceil(m2_bloq_15 * 12.5 * 1.05)
    und_bloq_10 = math.ceil(m2_bloq_10 * 12.5 * 1.05)

    # Crear Spreadsheet nativo dentro de FreeCAD (.FCStd)
    sheet = doc.addObject("Spreadsheet::Sheet", "Computos_Metricos_BIM")
    sheet.Label = "02_Tabla_Computos_Metricos_Fase1"
    headers = [
        "Codigo", "Capitulo", "Nivel", "Descripcion_Partida",
        "Nro_Elem", "Unidad", "Cantidad_Neta", "Area_m2", "Volumen_m3",
    ]
    cols_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    for c_idx, h_txt in enumerate(headers):
        sheet.set(f"{cols_letters[c_idx]}1", h_txt)
        sheet.setStyle(f"{cols_letters[c_idx]}1", "bold")

    row_i = 2
    for p in partidas_ordenadas:
        sheet.set(f"A{row_i}", p["codigo"])
        sheet.set(f"B{row_i}", p["capitulo"])
        sheet.set(f"C{row_i}", p["nivel"])
        sheet.set(f"D{row_i}", p["partida"])
        sheet.set(f"E{row_i}", str(p["elementos"]))
        sheet.set(f"F{row_i}", p["unidad"])
        sheet.set(f"G{row_i}", f"{p['cantidad']:.2f}")
        sheet.set(f"H{row_i}", f"{p['area_m2']:.2f}")
        sheet.set(f"I{row_i}", f"{p['volumen_m3']:.3f}")
        row_i += 1

    row_i += 1
    sheet.set(f"A{row_i}", "RESUMEN INSUMOS COMERCIALES ESTIMADOS (CON 5% DESPERDICIO)")
    sheet.setStyle(f"A{row_i}", "bold")
    insumos_rows = [
        ("Concreto Estructural Total (con vigas y placa techo P1)", "m3", f"{vol_conc_total:.2f}"),
        ("Concreto Estructural Base (sin vigas ni placa techo P1)", "m3", f"{vol_conc_280 + vol_conc_250_sin_techo:.2f}"),
        ("Cemento Portland Gris (Sacos 42,5 kg: Concreto + Albanileria)", "sacos", str(sacos_cemento_tot)),
        ("Arena Lavada / Cernida", "m3", f"{arena_lavada_m3:.1f}"),
        ("Piedra Picada #1", "m3", f"{piedra_picada_m3:.1f}"),
        ("Acero de Refuerzo (Cabillas + Malla Electrosoldada)", "kg", str(acero_refuerzo_kg)),
        ("Bloques de Concreto e=20 cm (12,5 und/m2 + 5%)", "und", str(und_bloq_20)),
        ("Bloques de Arcilla/Concreto e=15 cm (12,5 und/m2 + 5%)", "und", str(und_bloq_15)),
        ("Bloques de Tabiqueria e=10 cm (12,5 und/m2 + 5%)", "und", str(und_bloq_10)),
        ("Friso / Encamisado Neto (Ambas Caras)", "m2", f"{m2_muros_friso:.2f}"),
        ("Impermeabilizacion Sotano (Muros Contencion + Losa)", "m2", f"{m2_imperm_sot:.2f}"),
        ("Piedra Laja Rustica Natural", "m2", f"{m2_piedra:.2f}"),
        ("Porcelanato Comercial Alto Trafico", "m2", f"{m2_porcel:.2f}"),
        ("Ceramica Antideslizante / Pared en Banos", "m2", f"{m2_ceram_ban:.2f}"),
    ]
    for ins_lbl, ins_u, ins_val in insumos_rows:
        row_i += 1
        sheet.set(f"D{row_i}", ins_lbl)
        sheet.set(f"F{row_i}", ins_u)
        sheet.set(f"G{row_i}", ins_val)

    doc.recompute()

    # =========================================================================
    # 9. GUARDADO DE MODELO .FCStd, EXPORTACION .IFC (IFC4) Y TABLAS .CSV / .MD
    # =========================================================================
    doc.saveAs(fcstd_path)
    print(f"  [OK] Modelo nativo FreeCAD guardado en: {fcstd_path}")

    # Exportar a IFC4 solo los objetos visibles/principales del Sitio (sin auxiliares ocultos)
    exportIFC.export([site], ifc_path)
    print(f"  [OK] Modelo estandar abierto IFC4 exportado en: {ifc_path}")

    # Exportar CSV detallado elemento por elemento + resumen (UTF-8 con BOM para Excel en Windows)
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f_csv:
        writer = csv.writer(f_csv, delimiter=";")
        writer.writerow([
            "Codigo_Partida", "Capitulo", "Nivel_Espacial", "Elemento_BIM",
            "Clase_IFC", "Material_Especificacion", "Unidad",
            "Cantidad_Principal", "Area_Neta_m2", "Volumen_Neto_m3", "Descripcion_Tecnica",
        ])
        for rec in sorted(qto_records, key=lambda r: (r["codigo"], r["nivel"], r["nombre"])):
            writer.writerow([
                rec["codigo"],
                rec["capitulo"],
                rec["nivel"],
                rec["nombre"],
                rec["ifc_type"],
                rec["material"],
                rec["unidad"],
                f"{rec['cantidad']:.3f}",
                f"{rec['area_m2']:.3f}",
                f"{rec['volumen_m3']:.4f}",
                rec["descripcion"],
            ])
    print(f"  [OK] Tabla CSV para Excel generada en: {csv_path}")

    # Generar Reporte Ejecutivo Markdown de Computos Metricos e Insumos Constructivos
    puertas_ventanas = [r for r in qto_records if r["ifc_type"] in ("Door", "Window", "Curtain Wall")]
    sanitarios_list  = [r for r in qto_records if r["ifc_type"] == "Sanitary Terminal"]
    equipos_list     = [r for r in qto_records if r["capitulo"] == "08_EQUIPAMIENTO_COMERCIAL_FRIO"]

    md_lines = [
        "# Cómputos Métricos y Cantidades de Materiales BIM — Fase 1 (Sótano, Rampa y Piso 1 Completo)",
        "",
        "- **Modelo Nativo FreeCAD 1.1.4:** `03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.FCStd`",
        "- **Modelo Estándar Abierto OpenBIM (`IFC4`):** `03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.ifc`",
        "- **Tabla Detallada para Excel:** `01_Planos_y_Documentacion/computos_metricos_fase1_bim.csv`",
        f"- **Auditoría de Lindero Vecino Oeste:** `minX = {min_x_mm/MM:.4f} m` (`0,00 m` invasión; pared vecina excluida de todos los cómputos).",
        f"- **Total de Objetos Constructivos Cuantificados:** `{len(qto_records)}` sólidos BIM verificados (con sustracción booleana exacta de columnas y vanos).",
        "",
        "---",
        "",
        "## 1. Resumen Ejecutivo de Compra de Materiales e Insumos (Incluye 5% de Desperdicio)",
        "",
        "| Insumo / Material Comercial | Unidad | Cantidad Estimada | Uso Principal en Obra |",
        "| :--- | :---: | ---: | :--- |",
        f"| **Concreto Estructural `f'c = 280 kg/cm²`** (Infraestructura) | `m³` | **{vol_conc_280:.2f}** | Zapatas (12), losa sótano, patio maniobra, rampa 18%, muros contención, 12 cols `35×35` y Escalera T1 |",
        f"| **Concreto Estructural `f'c = 250 kg/cm²`** (Piso 1 base sin techo) | `m³` | **{vol_conc_250_sin_techo:.2f}** | Losa entrepiso P.B. (`192,15 m²` netos), 32 columnas `25×25 cm` y Escalera T2 |",
        f"| **Concreto Estructural `f'c = 250 kg/cm²`** (Vigas + Placa Techo P1) | `m³` | **{vol_conc_250_techo:.2f}** | Vigas sísmicas corona Piso 1 (`25×30 cm`) + Placa superior `Z = +2,85..+3,00 m` |",
        f"| **TOTAL CONCRETO ARMADO FASE 1 COMPLETA** | `m³` | **{vol_conc_total:.2f}** | Infraestructura + Piso 1 completamente techado |",
        f"| **Cemento Gris Portland (`Sacos 42,5 kg`)** | `sacos` | **{sacos_cemento_tot}** | `{sacos_cem_concreto}` sacos para concretos (si se vacía en sitio) + `{sacos_cem_albanil}` sacos para morteros/frisos |",
        f"| **Arena Lavada + Arena Cernida** | `m³` | **{arena_lavada_m3:.1f}** | Mezclas de concreto, pega de bloques y frisos |",
        f"| **Piedra Picada `#1`** | `m³` | **{piedra_picada_m3:.1f}** | Concretos estructurales de sótano, rampa y planta baja |",
        f"| **Acero de Refuerzo (Cabillas corrugadas + Malla)** | `kg` | **{acero_refuerzo_kg:,}** | Cuantía sismorresistente en columnas, vigas, zapatas, losas, rampa y escaleras |",
        f"| **Bloques de Concreto Pesado `e = 20 cm`** | `und` | **{und_bloq_20:,}** | `{m2_bloq_20:.2f} m²` netos en Muro Este Sótano y pórtico de carga Av. 4 |",
        f"| **Bloques de Arcilla / Concreto `e = 15 cm`** | `und` | **{und_bloq_15:,}** | `{m2_bloq_15:.2f} m²` netos en fachadas P.B., divisorio garaje, esclusas, cercas y muros sótano |",
        f"| **Bloques de Tabiquería `e = 10 cm`** | `und` | **{und_bloq_10:,}** | `{m2_bloq_10:.2f} m²` netos en divisiones internas de cabinas sanitarias Damas/Caballeros |",
        f"| **Friso y Encamisado de Muros (Ambas Caras Netas)** | `m²` | **{m2_muros_friso:.2f}** | Descontados al 100% todos los vanos de puertas, ventanas, portones y santamarías |",
        f"| **Manto / Impermeabilización Hidrófuga Sótano** | `m²` | **{m2_imperm_sot:.2f}** | Losa de fundación bodega (`74,70 m²`) + muros de contención contra terreno |",
        f"| **Piedra Laja Rústica Natural** | `m²` | **{m2_piedra:.2f}** | Machones frontales Av. 4, zócalo fachada Este y zócalo interior de garaje |",
        f"| **Porcelanato Comercial Antideslizante Alto Tráfico** | `m²` | **{m2_porcel:.2f}** | Salón Frutería ampliado (`~112 m²`), Barra de Jugos y Oficina Acristalada |",
        f"| **Pavimento Vehicular Endurecido (Garaje)** | `m²` | **{m2_pav_gar:.2f}** | Estacionamiento cubierto de 2 vehículos + vestíbulo residencial |",
        f"| **Cerámica Impermeable (Pisos + Paredes Baños)** | `m²` | **{m2_ceram_ban:.2f}** | Núcleo de Baños Suroeste P.B. y Baño Operativo del Sótano |",
        "",
        "---",
        "",
        "## 2. Cómputos Métricos Consolidados por Partida Constructiva",
        "",
        "| Código | Capítulo | Nivel | Especificación / Partida | Elem. | Unid. | Cantidad Neta | Área (`m²`) | Volumen (`m³`) |",
        "| :---: | :--- | :--- | :--- | :---: | :---: | ---: | ---: | ---: |",
    ]

    for p in partidas_ordenadas:
        md_lines.append(
            f"| `{p['codigo']}` | {p['capitulo']} | {p['nivel']} | {p['partida']} | "
            f"{p['elementos']} | `{p['unidad']}` | **{p['cantidad']:.2f}** | {p['area_m2']:.2f} | {p['volumen_m3']:.3f} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 3. Cuadro Detallado de Portones, Santamarías, Puertas, Ventanas y Cerramientos",
        "",
        "| Nivel | Código | Elemento BIM | Clase IFC | Área Vano (`m²`) | Material Principal |",
        "| :--- | :---: | :--- | :---: | ---: | :--- |",
    ])
    for pv in sorted(puertas_ventanas, key=lambda x: (x["nivel"], x["codigo"], x["nombre"])):
        md_lines.append(
            f"| {pv['nivel']} | `{pv['codigo']}` | {pv['nombre']} | `{pv['ifc_type']}` | {pv['area_m2']:.2f} | {pv['material']} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 4. Inventario de Piezas Sanitarias y Equipamiento Comercial / Cadena de Frío",
        "",
        "| Nivel | Código | Equipo / Aparato Sanitario | Unidad | Cantidad |",
        "| :--- | :---: | :--- | :---: | ---: |",
    ])
    for eq in sorted(sanitarios_list + equipos_list, key=lambda x: (x["codigo"], x["nivel"], x["nombre"])):
        md_lines.append(
            f"| {eq['nivel']} | `{eq['codigo']}` | {eq['nombre']} | `{eq['unidad']}` | **{eq['cantidad']:.2f}** |"
        )
    md_lines.append("")

    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write("\n".join(md_lines))
    print(f"  [OK] Reporte ejecutivo Markdown generado en: {md_path}")
    print("=" * 78)
    print("CONVERSION BIM FASE 1 COMPLETADA CON EXITO!")
    print("=" * 78)


if __name__ == "__main__":
    build_bim_fase1()
