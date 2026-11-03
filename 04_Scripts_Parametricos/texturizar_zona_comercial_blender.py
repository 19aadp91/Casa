"""
Script de Automatización para Blender (bpy)
Aplica Texturas PBR Fotorrealistas, Iluminación Comercial y Cámaras a la Zona Comercial
(Frutería y Verdulería Alpina, Gran Almacén 33 m² y Estacionamiento Fluido)
Compatible con Blender 4.x y 5.x (Principled BSDF v2, Cycles y Eevee Next).
"""

import os
import math
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
# 1. GENERADORES DE MATERIALES PBR PROCEDURALES FOTORREALISTAS
# =============================================================================

def create_mat_madera_roble():
    """Madera de roble cálido macizo encerado con vetas procedurales."""
    mat = bpy.data.materials.get("MAT_Madera_Roble") or bpy.data.materials.new("MAT_Madera_Roble")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.38)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.5)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-900, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-720, 0)
    mapping.inputs['Scale'].default_value = (1.5, 4.0, 1.5)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    # Textura de onda para vetas de madera
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-520, 100)
    wave.wave_type = 'RINGS'
    wave.inputs['Scale'].default_value = 2.2
    wave.inputs['Distortion'].default_value = 4.5
    wave.inputs['Detail'].default_value = 5.0
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    
    # Rampa de color para tonos de roble cálido
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-280, 100)
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.42, 0.26, 0.12, 1.0) # Veta oscura
    ramp.color_ramp.elements[1].position = 0.8
    ramp.color_ramp.elements[1].color = (0.65, 0.44, 0.25, 1.0) # Roble dorado cálido
    links.new(wave.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    # Bump sutil de vetas
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-280, -150)
    bump.inputs['Strength'].default_value = 0.15
    bump.inputs['Distance'].default_value = 0.05
    links.new(wave.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_madera_oscura():
    """Madera alpina oscura envejecida para vigas, marquesina y portón."""
    mat = bpy.data.materials.get("MAT_Madera_Oscura_Chalet") or bpy.data.materials.new("MAT_Madera_Oscura_Chalet")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.55)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (1.2, 5.0, 1.2)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-420, 100)
    noise.inputs['Scale'].default_value = 6.0
    noise.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.16, 0.09, 0.05, 1.0)
    ramp.color_ramp.elements[1].color = (0.28, 0.17, 0.10, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.25
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_piedra_laja():
    """Piedra laja alpina con relieve pronunciado y tonos terrosos."""
    mat = bpy.data.materials.get("MAT_Piedra_Laja") or bpy.data.materials.new("MAT_Piedra_Laja")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.88)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (4.0, 4.0, 4.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-420, 100)
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 3.5
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.22, 0.19, 0.17, 1.0) # Gris oscuro pizarra
    ramp.color_ramp.elements[1].color = (0.45, 0.38, 0.32, 1.0) # Ocre piedra laja
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.45
    bump.inputs['Distance'].default_value = 0.10
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_piso_fruteria():
    """Microcemento rústico / losetas de barro cocido claro con juntas."""
    mat = bpy.data.materials.get("MAT_Piso_Fruteria") or bpy.data.materials.new("MAT_Piso_Fruteria")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.42)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.45)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-420, 100)
    noise.inputs['Scale'].default_value = 12.0
    noise.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.75, 0.70, 0.63, 1.0)
    ramp.color_ramp.elements[1].color = (0.84, 0.80, 0.74, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.08
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_piso_almacen_epoxi():
    """Concreto epóxico gris industrial para el Gran Almacén (33,09 m²)."""
    mat = bpy.data.materials.get("MAT_Piso_Almacen_Epoxi") or bpy.data.materials.new("MAT_Piso_Almacen_Epoxi")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.68, 0.71, 0.70, 1.0))
    set_socket(bsdf, ['Roughness'], 0.18) # Acabado brillante epoxi limpio
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.6)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 25.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.02
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_piso_estacionamiento():
    """Pavimento de concreto fratasado antideslizante para el estacionamiento."""
    mat = bpy.data.materials.get("MAT_Piso_Estacionamiento") or bpy.data.materials.new("MAT_Piso_Estacionamiento")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.55, 0.55, 0.54, 1.0))
    set_socket(bsdf, ['Roughness'], 0.72)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 18.0
    noise.inputs['Detail'].default_value = 5.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.12
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_inox_industrial():
    """Acero inoxidable satinado para balanzas, mesón de lavado y puerta cuarto frío."""
    mat = bpy.data.materials.get("MAT_Inox_Industrial") or bpy.data.materials.new("MAT_Inox_Industrial")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.85, 0.86, 0.87, 1.0))
    set_socket(bsdf, ['Metallic'], 1.0)
    set_socket(bsdf, ['Roughness'], 0.22)
    set_socket(bsdf, ['Anisotropic', 'Anisotropy'], 0.35)
    
    return mat

def create_mat_cuarto_frio_paneles():
    """Paneles sándwich isotérmicos de poliuretano blanco satinado."""
    mat = bpy.data.materials.get("MAT_Cuarto_Frio_Paneles") or bpy.data.materials.new("MAT_Cuarto_Frio_Paneles")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.94, 0.96, 0.97, 1.0))
    set_socket(bsdf, ['Roughness'], 0.28)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.5)
    
    return mat

def create_mat_metal_negro_forja():
    """Hierro forjado negro mate para bastidor de portón, rieles, balanzas y TPV."""
    mat = bpy.data.materials.get("MAT_Metal_Negro_Forja") or bpy.data.materials.new("MAT_Metal_Negro_Forja")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.12, 0.12, 0.12, 1.0))
    set_socket(bsdf, ['Metallic'], 0.85)
    set_socket(bsdf, ['Roughness'], 0.40)
    
    return mat

def create_mat_santamaria_aluminio():
    """Aluminio galvanizado acanalado para santamarías enrollables de caracol."""
    mat = bpy.data.materials.get("MAT_Santamaria_Aluminio") or bpy.data.materials.new("MAT_Santamaria_Aluminio")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.62, 0.68, 0.72, 1.0))
    set_socket(bsdf, ['Metallic'], 0.92)
    set_socket(bsdf, ['Roughness'], 0.32)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-400, 0)
    wave.wave_type = 'BANDS'
    wave.inputs['Scale'].default_value = 24.0 # Lamas acanaladas horizontales
    links.new(tex_coord.outputs['Object'], wave.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.28
    links.new(wave.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_madera_verde_bosque():
    """Madera satinada verde bosque para estantes de hortalizas y verduras frescas."""
    mat = bpy.data.materials.get("MAT_Madera_Verde_Bosque") or bpy.data.materials.new("MAT_Madera_Verde_Bosque")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.16, 0.28, 0.19, 1.0)) # Verde rústico oscuro
    set_socket(bsdf, ['Roughness'], 0.45)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.4)
    
    return mat

def create_mat_muros_estuco():
    """Estuco rústico blanco cálido para muros comerciales interiores y exteriores."""
    mat = bpy.data.materials.get("MAT_Muros_Estuco_Blanco") or bpy.data.materials.new("MAT_Muros_Estuco_Blanco")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.92, 0.90, 0.86, 1.0))
    set_socket(bsdf, ['Roughness'], 0.85)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 35.0
    noise.inputs['Detail'].default_value = 6.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.08
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_vidrio():
    """Vidrio arquitectónico templado transparente."""
    mat = bpy.data.materials.get("MAT_Vidrio_Comercial") or bpy.data.materials.new("MAT_Vidrio_Comercial")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.95, 0.98, 1.0, 1.0))
    set_socket(bsdf, ['Roughness'], 0.02)
    set_socket(bsdf, ['IOR'], 1.45)
    set_socket(bsdf, ['Transmission Weight', 'Transmission'], 1.0)
    
    return mat

def create_fruit_mats():
    """Materiales de colores vivos para frutas y hortalizas."""
    mats = {}
    colors = {
        'Manzana_Roja': (0.75, 0.08, 0.08, 1.0),
        'Naranja':      (0.92, 0.45, 0.05, 1.0),
        'Limon':        (0.88, 0.82, 0.08, 1.0),
        'Manzana_Verde':(0.22, 0.65, 0.12, 1.0),
        'Platano':      (0.90, 0.72, 0.14, 1.0),
        'Tomate':       (0.85, 0.12, 0.08, 1.0),
    }
    for name, col in colors.items():
        mat_name = f"MAT_Fruta_{name}"
        m = bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name)
        _, _, bsdf = clean_material_nodes(m)
        set_socket(bsdf, ['Base Color'], col)
        set_socket(bsdf, ['Roughness'], 0.25)
        mats[name] = m
    return mats


# =============================================================================
# 2. ASIGNACIÓN INTELIGENTE DE MATERIALES A LAS MALLAS DE PLANTA BAJA
# =============================================================================

def assign_materials():
    print("Creando catálogo completo de materiales PBR...")
    m_roble    = create_mat_madera_roble()
    m_oscura   = create_mat_madera_oscura()
    m_laja     = create_mat_piedra_laja()
    m_piso_frut= create_mat_piso_fruteria()
    m_piso_alm = create_mat_piso_almacen_epoxi()
    m_piso_est = create_mat_piso_estacionamiento()
    m_inox     = create_mat_inox_industrial()
    m_cf_pan   = create_mat_cuarto_frio_paneles()
    m_metal_neg= create_mat_metal_negro_forja()
    m_santam   = create_mat_santamaria_aluminio()
    m_verde_bos= create_mat_madera_verde_bosque()
    m_estuco   = create_mat_muros_estuco()
    m_vidrio   = create_mat_vidrio()
    create_fruit_mats()

    # 1. Zócalo de piedra laja
    obj_zoc = bpy.data.objects.get("PB_ZOCALO_PIEDRA_3D_mesh_")
    if obj_zoc:
        obj_zoc.data.materials.clear()
        obj_zoc.data.materials.append(m_laja)
        print("  -> Asignado MAT_Piedra_Laja a PB_ZOCALO_PIEDRA_3D_mesh_")

    # 2. Timber Frame (Postes y vigas de madera alpina oscura)
    obj_tf = bpy.data.objects.get("PB_TIMBER_FRAME_3D_mesh_")
    if obj_tf:
        obj_tf.data.materials.clear()
        obj_tf.data.materials.append(m_oscura)
        print("  -> Asignado MAT_Madera_Oscura_Chalet a PB_TIMBER_FRAME_3D_mesh_")

    # 3. Losa de Piso de Planta Baja (Frutería, Almacén y Estacionamiento diferenciados por polígono)
    obj_losa = bpy.data.objects.get("LOSA_PISO_3D_mesh_")
    if obj_losa and obj_losa.type == 'MESH':
        obj_losa.data.materials.clear()
        obj_losa.data.materials.append(m_piso_frut) # Index 0: Frutería
        obj_losa.data.materials.append(m_piso_alm)  # Index 1: Almacén
        obj_losa.data.materials.append(m_piso_est)  # Index 2: Estacionamiento
        
        mesh = obj_losa.data
        for poly in mesh.polygons:
            cy = poly.center.y
            cx = poly.center.x
            # Y < 6.65 (offset_y=3.0 + 3.65) es el Gran Almacén
            if cy < 6.65:
                poly.material_index = 1
            # X < 3.45 y Y >= 6.65 es el Estacionamiento
            elif cx < 3.45:
                poly.material_index = 2
            # El resto es el Salón de Frutería y Verdulería
            else:
                poly.material_index = 0
        print("  -> Asignado piso zonificado a LOSA_PISO_3D_mesh_")

    # 4. Mobiliario Comercial de Frutería (Islas, mostrador, estantes, santamarías)
    obj_com = bpy.data.objects.get("PB_MOBILIARIO_COMERCIAL_3D_mesh_")
    if obj_com and obj_com.type == 'MESH':
        obj_com.data.materials.clear()
        obj_com.data.materials.append(m_roble)     # Index 0: Roble natural
        obj_com.data.materials.append(m_laja)      # Index 1: Murete piedra caja
        obj_com.data.materials.append(m_verde_bos) # Index 2: Repisas verduras
        obj_com.data.materials.append(m_santam)    # Index 3: Santamarías
        obj_com.data.materials.append(m_inox)      # Index 4: Balanzas inox
        obj_com.data.materials.append(m_metal_neg) # Index 5: TPV negro
        
        mesh = obj_com.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z
            # Santamarías en fachada frontal (Y > 24.30)
            if cy > 24.30:
                poly.material_index = 3
            # Mostrador de caja (X: 7.05..8.85, Y: 20.00..22.05)
            elif cx >= 7.00 and cy >= 19.90:
                if cz < 0.85:
                    poly.material_index = 1 # Murete piedra
                elif cz >= 0.85 and cz <= 0.95:
                    poly.material_index = 0 # Tope roble
                elif cx < 7.60:
                    poly.material_index = 4 # Balanzas inox
                else:
                    poly.material_index = 5 # TPV negro
            # Estanterías de verduras pared este (X > 8.35)
            elif cx > 8.35:
                poly.material_index = 2
            # Islas piramidales y estantes de roble
            else:
                poly.material_index = 0
        print("  -> Asignados materiales detallados a PB_MOBILIARIO_COMERCIAL_3D_mesh_")

    # 5. Mobiliario del Gran Almacén (Cuarto frío, mesón lavado, racks)
    obj_ofic = bpy.data.objects.get("PB_MOBILIARIO_OFICINA_3D_mesh_")
    if obj_ofic and obj_ofic.type == 'MESH':
        obj_ofic.data.materials.clear()
        obj_ofic.data.materials.append(m_metal_neg) # Index 0: Estructura racks
        obj_ofic.data.materials.append(m_roble)     # Index 1: Bandejas madera
        obj_ofic.data.materials.append(m_cf_pan)    # Index 2: Paneles cuarto frío
        obj_ofic.data.materials.append(m_inox)      # Index 3: Inox lavado/puerta
        
        mesh = obj_ofic.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z
            # Cuarto frío (X: 6.35..8.92, Y: 3.20..4.65)
            if cx >= 6.30 and cy <= 4.70:
                if cy > 4.60 and cx >= 6.80 and cx <= 7.90:
                    poly.material_index = 3 # Puerta inox
                else:
                    poly.material_index = 2 # Paneles poliuretano
            # Mesón de lavado (X: 7.80..8.95, Y: 4.80..6.45)
            elif cx >= 7.80 and cy >= 4.80:
                poly.material_index = 3 # Inox industrial
            # Baterías de racks
            else:
                if cz % 0.45 < 0.08:
                    poly.material_index = 1 # Bandeja madera
                else:
                    poly.material_index = 0 # Montante metal
        print("  -> Asignados materiales industriales a PB_MOBILIARIO_OFICINA_3D_mesh_")

    # 6. Mobiliario de Garaje (Portón corredizo sobre riel curvo)
    obj_gar = bpy.data.objects.get("PB_MOBILIARIO_GARAJE_3D_mesh_")
    if obj_gar and obj_gar.type == 'MESH':
        obj_gar.data.materials.clear()
        obj_gar.data.materials.append(m_metal_neg) # Index 0: Bastidor y riel
        obj_gar.data.materials.append(m_oscura)    # Index 1: Listones teca
        mesh = obj_gar.data
        for poly in mesh.polygons:
            if poly.center.z > 2.20 or poly.center.x > 3.20:
                poly.material_index = 0 # Riel y herrajes
            else:
                poly.material_index = 1 # Duelas de madera
        print("  -> Asignados materiales a PB_MOBILIARIO_GARAJE_3D_mesh_")

    # 7. Muros y Columnas
    for m_name in ["MUROS_EXTERIORES_3D_mesh_", "MUROS_INTERIORES_3D_mesh_"]:
        m_obj = bpy.data.objects.get(m_name)
        if m_obj and m_obj.type == 'MESH':
            m_obj.data.materials.clear()
            m_obj.data.materials.append(m_estuco)
            print(f"  -> Asignado MAT_Muros_Estuco_Blanco a {m_name}")

    obj_col = bpy.data.objects.get("COLUMNAS_3D_mesh_")
    if obj_col and obj_col.type == 'MESH':
        obj_col.data.materials.clear()
        obj_col.data.materials.append(m_laja)
        print("  -> Asignado MAT_Piedra_Laja a COLUMNAS_3D_mesh_")


# =============================================================================
# 3. ACCESORIOS PROCEDURALES DE AMBIENTACIÓN (CAJAS Y PIRÁMIDES DE FRUTAS)
# =============================================================================

def add_fruit_crates():
    """Genera cajas de madera con productos coloridos en las islas y estantes."""
    print("Creando cajas y pirámides de frutas en las 4 islas y estanterías...")
    col = bpy.data.collections.get("PB_AMBIENTACION_FRUTAS")
    if not col:
        col = bpy.data.collections.new("PB_AMBIENTACION_FRUTAS")
        bpy.context.scene.collection.children.link(col)

    mats = create_fruit_mats()
    m_roble = bpy.data.materials.get("MAT_Madera_Roble")

    # 4 Islas de frutas (coordenadas mundo con OFFSET_Y = 3.0 m)
    islas_data = [
        (5.925, 21.575, ['Manzana_Roja', 'Manzana_Verde'], "Isla_1_Manzanas"),
        (5.925, 19.325, ['Naranja', 'Limon'],              "Isla_2_Citricos"),
        (5.925, 15.025, ['Platano', 'Tomate'],             "Isla_3_Tropical"),
        (5.925, 11.875, ['Manzana_Verde', 'Naranja'],      "Isla_4_Verduras"),
    ]

    for ix, iy, fruit_types, group_name in islas_data:
        for level in range(3):
            z_lvl = 0.55 + level * 0.35
            size_xy = 1.10 - level * 0.25
            
            # Caja de madera contenedora
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ix, iy, z_lvl))
            crate = bpy.context.active_object
            crate.name = f"{group_name}_Caja_L{level+1}"
            crate.scale = (size_xy, size_xy, 0.12)
            crate.data.materials.append(m_roble)
            for c in list(crate.users_collection):
                c.objects.unlink(crate)
            col.objects.link(crate)
            
            # Montículo de fruta coloreada
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ix, iy, z_lvl + 0.10))
            fruit_pile = bpy.context.active_object
            fruit_pile.name = f"{group_name}_Fruta_L{level+1}"
            fruit_pile.scale = (size_xy * 0.88, size_xy * 0.88, 0.10)
            chosen_mat = mats[fruit_types[level % len(fruit_types)]]
            fruit_pile.data.materials.append(chosen_mat)
            for c in list(fruit_pile.users_collection):
                c.objects.unlink(fruit_pile)
            col.objects.link(fruit_pile)

    print("  -> Cajas y pirámides de frutas generadas con éxito.")


# =============================================================================
# 4. ILUMINACIÓN ARQUITECTÓNICA Y COMERCIAL CÁLIDA (3000K)
# =============================================================================

def setup_lighting():
    """Configura luz natural ambiental e iluminación comercial cálida suspendida."""
    print("Configurando iluminación comercial cálida (3000K)...")
    col_lgt = bpy.data.collections.get("PB_ILUMINACION_COMERCIAL")
    if not col_lgt:
        col_lgt = bpy.data.collections.new("PB_ILUMINACION_COMERCIAL")
        bpy.context.scene.collection.children.link(col_lgt)

    # 1. Luz de Sol exterior que entra por Avenida 4 (Norte)
    sun_data = bpy.data.lights.new(name="Sol_Avenida4", type='SUN')
    sun_data.energy = 3.5
    sun_data.color = (1.0, 0.96, 0.90) # Sol matutino cálido
    sun_obj = bpy.data.objects.new("Sol_Avenida4", sun_data)
    sun_obj.location = (6.0, 32.0, 10.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(170))
    col_lgt.objects.link(sun_obj)

    # 2. Luminarias cálidas suspendidas (Spot 3000K) sobre cada una de las 4 islas piramidales
    islas_pos = [(5.925, 21.575), (5.925, 19.325), (5.925, 15.025), (5.925, 11.875)]
    for idx, (lx, ly) in enumerate(islas_pos):
        lgt_data = bpy.data.lights.new(name=f"Spot_Isla_{idx+1}", type='SPOT')
        lgt_data.energy = 160.0 # Potencia focal
        lgt_data.spot_size = math.radians(65)
        lgt_data.spot_blend = 0.35
        lgt_data.color = (1.0, 0.88, 0.72) # Cálido 3000K para realzar fruta
        
        lgt_obj = bpy.data.objects.new(f"Spot_Isla_{idx+1}", lgt_data)
        lgt_obj.location = (lx, ly, 2.65)
        col_lgt.objects.link(lgt_obj)

    # 3. Luz sobre la Caja y Pesaje
    caja_lgt = bpy.data.lights.new(name="Spot_Caja_Pesaje", type='POINT')
    caja_lgt.energy = 90.0
    caja_lgt.color = (1.0, 0.92, 0.82)
    caja_obj = bpy.data.objects.new("Spot_Caja_Pesaje", caja_lgt)
    caja_obj.location = (7.85, 21.00, 2.60)
    col_lgt.objects.link(caja_obj)

    # 4. Luces funcionales neutras (4000K) en el Gran Almacén y Cuarto Frío
    alm_lgt = bpy.data.lights.new(name="Luz_Gran_Almacen", type='POINT')
    alm_lgt.energy = 140.0
    alm_lgt.color = (0.94, 0.96, 1.0)
    alm_obj = bpy.data.objects.new("Luz_Gran_Almacen", alm_lgt)
    alm_obj.location = (4.50, 4.80, 2.60)
    col_lgt.objects.link(alm_obj)

    cf_lgt = bpy.data.lights.new(name="Luz_Cuarto_Frio", type='POINT')
    cf_lgt.energy = 60.0
    cf_lgt.color = (0.88, 0.94, 1.0) # Frío cristalino
    cf_obj = bpy.data.objects.new("Luz_Cuarto_Frio", cf_lgt)
    cf_obj.location = (7.60, 3.90, 2.20)
    col_lgt.objects.link(cf_obj)

    # 5. Luz en Estacionamiento
    gar_lgt = bpy.data.lights.new(name="Luz_Estacionamiento", type='POINT')
    gar_lgt.energy = 120.0
    gar_lgt.color = (0.98, 0.96, 0.92)
    gar_obj = bpy.data.objects.new("Luz_Estacionamiento", gar_lgt)
    gar_obj.location = (1.80, 16.50, 2.60)
    col_lgt.objects.link(gar_obj)

    print("  -> Iluminación configurada.")


# =============================================================================
# 5. CÁMARAS CINEMATOGRÁFICAS DE PRESENTACIÓN
# =============================================================================

def setup_cameras():
    """Crea 4 cámaras arquitectónicas en puntos estratégicos."""
    print("Creando cámaras cinematográficas de presentación...")
    col_cam = bpy.data.collections.get("PB_CAMARAS_PRESENTACION")
    if not col_cam:
        col_cam = bpy.data.collections.new("PB_CAMARAS_PRESENTACION")
        bpy.context.scene.collection.children.link(col_cam)

    cameras_def = [
        # 1. Vista Fachada Avenida 4 mirando al interior
        ("Camara_1_Fachada_Avenida4", (6.20, 29.50, 1.65), (math.radians(82), 0, math.radians(180)), 28.0),
        # 2. Vista Interior Frutería desde la entrada
        ("Camara_2_Fruteria_Interior", (7.80, 23.50, 1.60), (math.radians(80), 0, math.radians(155)), 24.0),
        # 3. Vista Gran Almacén y Cuarto Frío
        ("Camara_3_Gran_Almacen", (1.20, 3.40, 1.55), (math.radians(78), 0, math.radians(-50)), 22.0),
        # 4. Vista Estacionamiento y Portón Curvo
        ("Camara_4_Estacionamiento", (1.80, 24.20, 1.60), (math.radians(82), 0, math.radians(180)), 26.0),
    ]

    for name, loc, rot, focal in cameras_def:
        cam_data = bpy.data.cameras.new(name=name)
        cam_data.lens = focal
        cam_data.clip_start = 0.1
        cam_data.clip_end = 150.0
        cam_obj = bpy.data.objects.new(name, cam_data)
        cam_obj.location = loc
        cam_obj.rotation_euler = rot
        col_cam.objects.link(cam_obj)
        print(f"  -> Creada {name} (focal {focal} mm)")

    # Activar Cámara 2 (Interior) como cámara activa por defecto
    cam_active = bpy.data.objects.get("Camara_2_Fruteria_Interior")
    if cam_active:
        bpy.context.scene.camera = cam_active


# =============================================================================
# 6. CONFIGURACIÓN DE RENDERIZADO Y GUARDADO DEL PROYECTO
# =============================================================================

def configure_render_and_save():
    print("Configurando motor de renderizado y guardando proyecto...")
    scene = bpy.context.scene
    
    # Configuración de resolución (Full HD 1920x1080)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Manejo de color cinematográfico AgX / Filmic
    if hasattr(scene.view_settings, 'view_transform'):
        try:
            scene.view_settings.view_transform = 'AgX'
            scene.view_settings.look = 'AgX - Medium High Contrast'
        except:
            try:
                scene.view_settings.view_transform = 'Filmic'
                scene.view_settings.look = 'Medium High Contrast'
            except:
                pass
    
    # Configurar motor EEVEE Next para renderizado rápido y limpio
    scene.render.image_settings.file_format = 'PNG'
    if hasattr(scene, 'eevee'):
        try:
            scene.eevee.taa_render_samples = 32
        except:
            pass
    if hasattr(scene, 'cycles'):
        scene.cycles.samples = 32

    # Guardar archivo maestro actualizado
    blend_path = bpy.data.filepath
    if not blend_path:
        blend_path = os.path.abspath("02_Modelos_CAD/casaBlender.blend")
    
    # Guardar copia de respaldo y archivo texturizado
    backup_path = os.path.join(os.path.dirname(blend_path), "casaBlender_backup.blend")
    texturized_path = os.path.join(os.path.dirname(blend_path), "casaBlender_texturizada.blend")
    
    try:
        bpy.ops.wm.save_as_mainfile(filepath=backup_path, copy=True)
        print(f"  -> Respaldo creado en: {backup_path}")
    except Exception as e:
        print(f"  (Aviso respaldo: {e})")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"  -> Archivo maestro guardado en: {blend_path}")

    bpy.ops.wm.save_as_mainfile(filepath=texturized_path, copy=True)
    print(f"  -> Archivo texturizado guardado en: {texturized_path}")

    # Renderizar imágenes de presentación de las 4 cámaras
    render_dir = os.path.abspath("01_Planos_y_Documentacion/renders")
    os.makedirs(render_dir, exist_ok=True)
    
    cams_to_render = [
        ("Camara_1_Fachada_Avenida4",  "render_1_fachada_avenida4.png"),
        ("Camara_2_Fruteria_Interior", "render_2_fruteria_interior.png"),
        ("Camara_3_Gran_Almacen",      "render_3_gran_almacen.png"),
        ("Camara_4_Estacionamiento",   "render_4_estacionamiento.png"),
    ]
    
    for cam_name, file_name in cams_to_render:
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            scene.camera = cam_obj
            out_file = os.path.join(render_dir, file_name)
            scene.render.filepath = out_file
            try:
                print(f"Renderizando {cam_name} en: {out_file} ...")
                bpy.ops.render.render(write_still=True)
                print(f"  [OK] Guardado {file_name}")
            except Exception as e:
                print(f"  [Aviso render {cam_name}]: {e}")


def main():
    print("==================================================================")
    print("TEXTURIZADO AUTOMÁTICO DE LA ZONA COMERCIAL EN BLENDER")
    print("==================================================================")
    assign_materials()
    add_fruit_crates()
    setup_lighting()
    setup_cameras()
    configure_render_and_save()
    print("==================================================================")
    print("¡PROCESO COMPLETADO SATISFACTORIAMENTE!")
    print("==================================================================")

if __name__ == "__main__":
    main()
