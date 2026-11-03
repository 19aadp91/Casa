"""
Script de Automatización para Blender (bpy)
1. Aplica Texturas PBR de Acero Estructural Negro Satinado (Pintura Electrostática)
   a las Columnas del Último Piso (P2_COLUMNAS_3D).
2. Asigna Texturas PBR Fotorrealistas a Todo el Mobiliario y Estructuras Pendientes:
   - Mobiliario Completo del Sótano (Cava de vinos, Salón de cine, Wet bar, Suite de huéspedes, Baño en piedra, Terraza)
   - Mobiliario de Despensa Walk-In y Clóset de Blancos (P2_TIMBER_FRAME_3D)
   - Sistema Hidroneumático y Tanque de 1.000 L (EQUIPO_HIDRONEUMATICO_3D)
   - Escaleras Principal y de Mantenimiento (P2_ESCALERA_3D, ESCALERA_3D, P2_ESCALERA_MANTENIMIENTO_3D)
   - Cubierta Chalet, Canalones Ocultos y Cerca Perimetral
Sin renderizar nada (solo asigna materiales y guarda el archivo .blend).
Compatible con Blender 4.x y 5.x.
"""

import os
import bpy

def clean_material_nodes(mat):
    """Limpia los nodos del material y prepara el Principled BSDF."""
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_out.location = (400, 0)
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (0, 0)
    
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
    return nodes, links, node_bsdf

def set_socket(node, socket_names, value):
    """Establece valor en un socket con compatibilidad de nombres cross-version."""
    for name in socket_names:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return True
    return False

def get_socket(node, socket_names):
    """Obtiene un socket por lista de nombres posibles."""
    for name in socket_names:
        if name in node.inputs:
            return node.inputs[name]
    return None


# =============================================================================
# 1. DEFINICIÓN DE MATERIALES PBR
# =============================================================================

def get_or_create_mat_columnas_metal_negro():
    """Acero estructural con acabado electrostático negro carbón satinado para columnas superiores."""
    mat = bpy.data.materials.get("MAT_Columnas_Metal_Negro") or bpy.data.materials.new("MAT_Columnas_Metal_Negro")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.040, 0.040, 0.042, 1.0)) # Negro carbón industrial
    set_socket(bsdf, ['Metallic'], 0.92) # Metal estructural de alta conductividad óptica
    set_socket(bsdf, ['Roughness'], 0.30) # Acabado satinado uniforme de pintura horneada
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.55)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 80.0 # Fino grano de pintura electrostática
    noise.inputs['Detail'].default_value = 5.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.035
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_tanque_agua():
    """Polietileno tricapa azul cobalto con filtro UV para tanque de 1.000 L."""
    mat = bpy.data.materials.get("MAT_Tanque_Agua_1000L") or bpy.data.materials.new("MAT_Tanque_Agua_1000L")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.035, 0.16, 0.42, 1.0))
    set_socket(bsdf, ['Roughness'], 0.26)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.5)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 35.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.02
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_techo_pizarra():
    """Teja asfáltica / pizarra alpina gris grafito para la cubierta del chalet."""
    mat = bpy.data.materials.get("MAT_Techo_Pizarra_Chalet") or bpy.data.materials.new("MAT_Techo_Pizarra_Chalet")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.14, 0.15, 0.16, 1.0))
    set_socket(bsdf, ['Roughness'], 0.76)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-400, 0)
    wave.wave_type = 'BANDS'
    wave.inputs['Scale'].default_value = 16.0
    links.new(tex_coord.outputs['Object'], wave.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.35
    links.new(wave.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_canalon_zinc():
    """Chapa de zinc / metal galvanizado oscuro para canalones pluviales ocultos."""
    mat = bpy.data.materials.get("MAT_Canalon_Zinc") or bpy.data.materials.new("MAT_Canalon_Zinc")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.30, 0.32, 0.34, 1.0))
    set_socket(bsdf, ['Metallic'], 0.88)
    set_socket(bsdf, ['Roughness'], 0.38)
    return mat


# =============================================================================
# 2. ASIGNACIÓN DE MATERIALES
# =============================================================================

def apply_columns_and_furniture_materials():
    print("Cargando catálogo completo de materiales PBR...")
    m_col_neg    = get_or_create_mat_columnas_metal_negro()
    m_tanque     = get_or_create_mat_tanque_agua()
    m_techo      = get_or_create_mat_techo_pizarra()
    m_zinc       = get_or_create_mat_canalon_zinc()
    
    m_roble      = bpy.data.materials.get("MAT_Suite_Madera_Roble") or bpy.data.materials.get("MAT_Madera_Roble")
    m_oscura     = bpy.data.materials.get("MAT_Suite_Madera_Oscura") or bpy.data.materials.get("MAT_Madera_Oscura_Chalet")
    m_lino_sofa  = bpy.data.materials.get("MAT_Social_Sofa_Lino")
    m_lino_blanco= bpy.data.materials.get("MAT_Suite_Lino_Blanco")
    m_pizarra    = bpy.data.materials.get("MAT_Suite_Pizarra_Negra")
    m_laja       = bpy.data.materials.get("MAT_Piedra_Laja")
    m_inox       = bpy.data.materials.get("MAT_Inox_Industrial")
    m_ceramica   = bpy.data.materials.get("MAT_Suite_Ceramica_Blanca")
    m_metal_neg  = bpy.data.materials.get("MAT_Suite_Metal_Negro") or bpy.data.materials.get("MAT_Metal_Negro_Forja")
    m_tv_screen  = bpy.data.materials.get("MAT_Social_Pantalla_TV")
    m_vidrio     = bpy.data.materials.get("MAT_Vidrio_Comercial")
    m_deck       = bpy.data.materials.get("MAT_Suite_Deck_Teca")
    m_estuco     = bpy.data.materials.get("MAT_Muros_Estuco_Blanco")
    m_epoxi      = bpy.data.materials.get("MAT_Piso_Almacen_Epoxi")

    # -------------------------------------------------------------------------
    # 1. COLUMNAS DEL ÚLTIMO PISO (P2): ACERO ESTRUCTURAL NEGRO SATINADO
    # -------------------------------------------------------------------------
    obj_cols = bpy.data.objects.get("P2_COLUMNAS_3D_mesh_")
    if obj_cols and obj_cols.type == 'MESH':
        obj_cols.data.materials.clear()
        obj_cols.data.materials.append(m_col_neg)
        for poly in obj_cols.data.polygons:
            poly.material_index = 0
        print(f"  -> Asignado MAT_Columnas_Metal_Negro a P2_COLUMNAS_3D_mesh_ ({len(obj_cols.data.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # 2. MOBILIARIO DE TIMBER FRAME: DESPENSA WALK-IN Y CLÓSET DE BLANCOS
    # -------------------------------------------------------------------------
    obj_timber = bpy.data.objects.get("P2_TIMBER_FRAME_3D_mesh_")
    if obj_timber and obj_timber.type == 'MESH':
        obj_timber.data.materials.clear()
        obj_timber.data.materials.append(m_oscura) # Index 0: Vigas y postes madera oscura
        obj_timber.data.materials.append(m_roble)  # Index 1: Estanterías despensa / clóset roble
        
        for poly in obj_timber.data.polygons:
            cx, cy = poly.center.x, poly.center.y
            # Estanterías de Despensa Walk-In y Clóset de Blancos (X in [0.30, 1.45], Y in [7.35, 10.35])
            if cx <= 1.45 and cy >= 7.35 and cy <= 10.35:
                poly.material_index = 1 # Madera roble
            else:
                poly.material_index = 0 # Postes y viga longitudinal maestra en madera oscura
        print(f"  -> Asignados materiales a P2_TIMBER_FRAME_3D_mesh_ ({len(obj_timber.data.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # 3. MOBILIARIO INTEGRAL DEL SÓTANO (390 polígonos)
    # -------------------------------------------------------------------------
    obj_sot_furn = bpy.data.objects.get("SOTANO_MOBILIARIO_3D_mesh_")
    if obj_sot_furn and obj_sot_furn.type == 'MESH':
        obj_sot_furn.data.materials.clear()
        obj_sot_furn.data.materials.append(m_roble)       # Index 0: Madera roble
        obj_sot_furn.data.materials.append(m_oscura)      # Index 1: Madera oscura
        obj_sot_furn.data.materials.append(m_lino_sofa)   # Index 2: Sofá lino cálido
        obj_sot_furn.data.materials.append(m_lino_blanco) # Index 3: Lino blanco cama
        obj_sot_furn.data.materials.append(m_pizarra)     # Index 4: Pizarra negra
        obj_sot_furn.data.materials.append(m_inox)        # Index 5: Inox
        obj_sot_furn.data.materials.append(m_ceramica)    # Index 6: Porcelana blanca
        obj_sot_furn.data.materials.append(m_metal_neg)   # Index 7: Metal negro
        obj_sot_furn.data.materials.append(m_tv_screen)   # Index 8: Pantalla Cine 85"
        obj_sot_furn.data.materials.append(m_vidrio)      # Index 9: Vidrio
        obj_sot_furn.data.materials.append(m_deck)        # Index 10: Teca exterior
        obj_sot_furn.data.materials.append(m_laja)        # Index 11: Piedra laja / tallada

        mesh = obj_sot_furn.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z

            # A) Patio exterior / Jardín Sur (Y < 2.50)
            if cy < 2.50:
                if cx >= 5.30 and cx <= 6.10:
                    poly.material_index = 11 # Mesa piedra jardín
                else:
                    poly.material_index = 10 # Sofá exterior teca

            # B) Suite de Huéspedes (X <= 2.85, Y in [2.50, 6.50])
            elif cx <= 2.85 and cy <= 6.50:
                if cz >= -2.20 and cz <= -1.90 and cx <= 2.25 and cy <= 5.40:
                    poly.material_index = 3  # Colchón y sobrecama lino blanco
                else:
                    poly.material_index = 0  # Cabecero, base cama, mesas noche y clóset en roble

            # C) Baño Rústico de Piedra (X in [2.90, 4.60], Y in [3.00, 6.50])
            elif cx >= 2.90 and cx <= 4.60 and cy <= 6.50:
                if cy <= 4.10: # Zona Ducha
                    if cz >= -2.45 and cy >= 3.98 and cy <= 4.12:
                        poly.material_index = 9  # Mampara cristal fijo
                    else:
                        poly.material_index = 4  # Plato ducha y banco pizarra negra
                elif cy >= 4.25 and cy <= 4.80:
                    poly.material_index = 6      # Inodoro porcelana blanca
                else: # Tocador, lavamanos y espejo (cy >= 4.90)
                    if cz >= -1.50:
                        poly.material_index = 7  # Espejo marco hierro negro
                    elif cz >= -1.75 and cz <= -1.45 and cx >= 3.05 and cx <= 3.48:
                        poly.material_index = 11 # Lavamanos piedra tallada
                    else:
                        poly.material_index = 0  # Mueble tocador roble

            # D) Barra Húmeda / Wet Bar (X in [4.65, 5.35], Y in [4.10, 6.40])
            elif cx >= 4.65 and cx <= 5.35 and cy <= 6.40:
                if cz >= -1.65 and cz <= -1.52:
                    poly.material_index = 4      # Tope piedra pizarra
                elif cz >= -1.62 and cx >= 4.75 and cx <= 5.25 and cy >= 5.50 and cy <= 6.05:
                    poly.material_index = 5      # Bar sink inox
                elif cy <= 4.90 and cz <= -1.60:
                    poly.material_index = 5      # Vinera refrigerada inox
                else:
                    poly.material_index = 0      # Mueble bajo y repisas roble

            # E) Comedor / Mesa de Juegos de Taberna (X >= 6.50, Y in [3.70, 6.50])
            elif cx >= 6.50 and cy <= 6.50:
                if cz <= -2.00:
                    poly.material_index = 2      # Sillas tapizadas lino cálido
                else:
                    poly.material_index = 0      # Mesa tablero y patas roble

            # F) Cava de Vinos (X <= 5.80, Y >= 8.30)
            elif cx <= 5.80 and cy >= 8.30:
                if cz >= -1.62 and cz <= -1.48 and cy >= 10.60:
                    poly.material_index = 4      # Nicho piedra pizarra decantación
                else:
                    poly.material_index = 0      # Botelleros, mesa de cata barrica y taburetes roble

            # G) Salón Lounge & Cine Familiar (X >= 6.10, Y >= 7.60)
            elif cx >= 6.10 and cy >= 7.60:
                if cx >= 6.45 and cx <= 8.45 and cy >= 10.90 and cz >= -1.82: # TV Cine 85"
                    if abs(poly.normal.y) > 0.7:
                        poly.material_index = 8  # Pantalla Cine 85" ultra-black
                    else:
                        poly.material_index = 7  # Marco metal negro
                elif cz >= -2.52 and cz <= -1.62 and cy <= 10.00:
                    poly.material_index = 2      # Gran sofá lounge en L lino cálido
                else:
                    poly.material_index = 0      # Mueble TV y mesa de centro roble

            # H) Maletero bajo escalera (X <= 1.45, Y >= 10.70)
            else:
                poly.material_index = 0          # Repisas roble

        print(f"  -> Asignados materiales a SOTANO_MOBILIARIO_3D_mesh_ ({len(mesh.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # 4. SISTEMA HIDRONEUMÁTICO Y TANQUE 1.000 L
    # -------------------------------------------------------------------------
    obj_hydro = bpy.data.objects.get("EQUIPO_HIDRONEUMATICO_3D_mesh_")
    if obj_hydro and obj_hydro.type == 'MESH':
        obj_hydro.data.materials.clear()
        obj_hydro.data.materials.append(m_tanque)   # Index 0: Tanque azul cobalto
        obj_hydro.data.materials.append(m_inox)     # Index 1: Bomba / calderín inox
        obj_hydro.data.materials.append(m_col_neg)  # Index 2: Tuberías / zunchos metal negro
        obj_hydro.data.materials.append(m_epoxi)    # Index 3: Pedestal concreto
        
        for poly in obj_hydro.data.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z
            if cz <= 5.82:
                poly.material_index = 3 # Pedestal
            elif cx <= 2.25 and cy <= 5.00:
                poly.material_index = 0 # Tanque de agua 1.000 L azul cobalto
            else:
                poly.material_index = 1 # Bomba presurizadora y calderín inox
        print(f"  -> Asignados materiales a EQUIPO_HIDRONEUMATICO_3D_mesh_ ({len(obj_hydro.data.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # 5. ESCALERAS (Principal, Sótano y Mantenimiento)
    # -------------------------------------------------------------------------
    for esc_name in ["P2_ESCALERA_3D_mesh_", "ESCALERA_3D_mesh_"]:
        obj_esc = bpy.data.objects.get(esc_name)
        if obj_esc and obj_esc.type == 'MESH':
            obj_esc.data.materials.clear()
            obj_esc.data.materials.append(m_roble)
            for poly in obj_esc.data.polygons:
                poly.material_index = 0
            print(f"  -> Asignado MAT_Suite_Madera_Roble a {esc_name}")

    obj_maint = bpy.data.objects.get("P2_ESCALERA_MANTENIMIENTO_3D_mesh_")
    if obj_maint and obj_maint.type == 'MESH':
        obj_maint.data.materials.clear()
        obj_maint.data.materials.append(m_col_neg)
        for poly in obj_maint.data.polygons:
            poly.material_index = 0
        print("  -> Asignado MAT_Columnas_Metal_Negro a P2_ESCALERA_MANTENIMIENTO_3D_mesh_")

    # -------------------------------------------------------------------------
    # 6. CUBIERTA CHALET, CANALONES Y CERCA PERIMETRAL
    # -------------------------------------------------------------------------
    obj_roof = bpy.data.objects.get("CUBIERTA_CHALET_3D_mesh_")
    if obj_roof and obj_roof.type == 'MESH':
        obj_roof.data.materials.clear()
        obj_roof.data.materials.append(m_techo)
        for poly in obj_roof.data.polygons:
            poly.material_index = 0
        print("  -> Asignado MAT_Techo_Pizarra_Chalet a CUBIERTA_CHALET_3D_mesh_")

    obj_gut = bpy.data.objects.get("CANALON_OCULTO_PROPIO_3D_mesh_")
    if obj_gut and obj_gut.type == 'MESH':
        obj_gut.data.materials.clear()
        obj_gut.data.materials.append(m_zinc)
        for poly in obj_gut.data.polygons:
            poly.material_index = 0
        print("  -> Asignado MAT_Canalon_Zinc a CANALON_OCULTO_PROPIO_3D_mesh_")

    obj_cerca = bpy.data.objects.get("CERCA_PERIMETRAL_3D_mesh_")
    if obj_cerca and obj_cerca.type == 'MESH':
        obj_cerca.data.materials.clear()
        obj_cerca.data.materials.append(m_metal_neg)
        obj_cerca.data.materials.append(m_laja)
        for poly in obj_cerca.data.polygons:
            if poly.center.z <= 0.60:
                poly.material_index = 1 # Zócalo piedra laja
            else:
                poly.material_index = 0 # Rejas hierro negro
        print("  -> Asignado acabado a CERCA_PERIMETRAL_3D_mesh_")

    # -------------------------------------------------------------------------
    # 7. ESTRUCTURAS DE SÓTANO RESTANTES (Muros, Losas, Columnas)
    # -------------------------------------------------------------------------
    obj_sot_col = bpy.data.objects.get("SOTANO_COLUMNAS_3D_mesh_")
    if obj_sot_col and obj_sot_col.type == 'MESH':
        obj_sot_col.data.materials.clear()
        obj_sot_col.data.materials.append(m_laja)
        for poly in obj_sot_col.data.polygons:
            poly.material_index = 0

    obj_sot_m_ext = bpy.data.objects.get("SOTANO_MUROS_EXT_3D_mesh_")
    if obj_sot_m_ext and obj_sot_m_ext.type == 'MESH':
        obj_sot_m_ext.data.materials.clear()
        obj_sot_m_ext.data.materials.append(m_laja)
        for poly in obj_sot_m_ext.data.polygons:
            poly.material_index = 0

    obj_sot_m_int = bpy.data.objects.get("SOTANO_MUROS_INT_3D_mesh_")
    if obj_sot_m_int and obj_sot_m_int.type == 'MESH':
        obj_sot_m_int.data.materials.clear()
        obj_sot_m_int.data.materials.append(m_estuco)
        for poly in obj_sot_m_int.data.polygons:
            poly.material_index = 0

    obj_sot_losa = bpy.data.objects.get("SOTANO_LOSA_3D_mesh_")
    if obj_sot_losa and obj_sot_losa.type == 'MESH':
        obj_sot_losa.data.materials.clear()
        obj_sot_losa.data.materials.append(m_roble)
        obj_sot_losa.data.materials.append(m_pizarra)
        for poly in obj_sot_losa.data.polygons:
            cx, cy = poly.center.x, poly.center.y
            if cx >= 2.90 and cx <= 4.60 and cy >= 3.00 and cy <= 6.50:
                poly.material_index = 1 # Baño pizarra
            else:
                poly.material_index = 0 # Suelo roble

    obj_sot_pm = bpy.data.objects.get("SOTANO_PIEDRA_MADERA_3D_mesh_")
    if obj_sot_pm and obj_sot_pm.type == 'MESH':
        obj_sot_pm.data.materials.clear()
        obj_sot_pm.data.materials.append(m_laja)
        obj_sot_pm.data.materials.append(m_oscura)
        for poly in obj_sot_pm.data.polygons:
            if poly.center.z >= -0.40:
                poly.material_index = 1 # Vigas techo madera oscura
            else:
                poly.material_index = 0 # Muro piedra

    obj_buh = bpy.data.objects.get("BUHARDILLA_TECNICA_3D_mesh_")
    if obj_buh and obj_buh.type == 'MESH':
        obj_buh.data.materials.clear()
        obj_buh.data.materials.append(m_oscura)
        for poly in obj_buh.data.polygons:
            poly.material_index = 0

    obj_los_tanq = bpy.data.objects.get("P2_LOSA_TANQUE_3D_mesh_")
    if obj_los_tanq and obj_los_tanq.type == 'MESH':
        obj_los_tanq.data.materials.clear()
        obj_los_tanq.data.materials.append(m_epoxi)
        for poly in obj_los_tanq.data.polygons:
            poly.material_index = 0


# =============================================================================
# 3. GUARDADO DEL ARCHIVO BLENDER (SIN RENDERIZAR NADA)
# =============================================================================

def save_blend_files():
    print("Guardando archivos .blend actualizados con columnas y mobiliario texturizado...")
    blend_path = bpy.data.filepath
    if not blend_path:
        blend_path = os.path.abspath("02_Modelos_CAD/casaBlender.blend")

    texturized_path = os.path.join(os.path.dirname(blend_path), "casaBlender_texturizada.blend")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"  -> Guardado con éxito en: {blend_path}")

    bpy.ops.wm.save_as_mainfile(filepath=texturized_path, copy=True)
    print(f"  -> Guardado con éxito en: {texturized_path}")


def main():
    print("==================================================================")
    print("APLICACIÓN DE TEXTURAS A COLUMNAS METÁLICAS P2 Y MOBILIARIO COMPLETO")
    print("==================================================================")
    apply_columns_and_furniture_materials()
    save_blend_files()
    print("==================================================================")
    print("¡PROCESO COMPLETADO SATISFACTORIAMENTE (SIN RENDERIZAR)!")
    print("==================================================================")

if __name__ == "__main__":
    main()
