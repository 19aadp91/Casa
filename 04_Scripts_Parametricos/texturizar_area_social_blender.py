"""
Script de Automatización para Blender (bpy)
Aplica Texturas PBR Fotorrealistas, Iluminación Cálida y Cámaras al Área Social de P2:
(Cocina Rústica con Gran Isla, Gran Comedor 8 Puestos, Gran Sala Chalet y Balconada Social Techada)
Sin renderizar nada (solo asigna materiales, iluminación, cámaras y guarda el archivo .blend).
Compatible con Blender 4.x y 5.x.
"""

import os
import math
import mathutils
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
# 1. DEFINICIÓN DE MATERIALES PBR PARA EL ÁREA SOCIAL
# =============================================================================

def get_or_create_mat_madera_roble():
    """Roble satinado para muebles de cocina, isla, mesa de comedor, consolas y piso social."""
    mat = bpy.data.materials.get("MAT_Suite_Madera_Roble")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Madera_Roble")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.35)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.5)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-900, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-720, 0)
    mapping.inputs['Scale'].default_value = (1.5, 3.5, 1.5)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-520, 100)
    wave.wave_type = 'RINGS'
    wave.inputs['Scale'].default_value = 2.5
    wave.inputs['Distortion'].default_value = 4.0
    wave.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-280, 100)
    ramp.color_ramp.elements[0].color = (0.40, 0.25, 0.12, 1.0)
    ramp.color_ramp.elements[1].color = (0.68, 0.46, 0.26, 1.0) # Roble dorado cálido
    links.new(wave.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-280, -150)
    bump.inputs['Strength'].default_value = 0.12
    links.new(wave.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_madera_oscura():
    """Madera alpina oscura para barandillas de balcón, vigas de comedor, campana rústica."""
    mat = bpy.data.materials.get("MAT_Suite_Madera_Oscura")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Madera_Oscura")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.50)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (1.5, 4.0, 1.5)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-420, 100)
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.16, 0.10, 0.05, 1.0)
    ramp.color_ramp.elements[1].color = (0.28, 0.18, 0.11, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.20
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_deck_teca():
    """Madera teca exterior impermeable para piso de balconada y mobiliario exterior."""
    mat = bpy.data.materials.get("MAT_Suite_Deck_Teca")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Deck_Teca")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.45)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (2.0, 5.0, 2.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-420, 100)
    noise.inputs['Scale'].default_value = 6.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.32, 0.18, 0.08, 1.0)
    ramp.color_ramp.elements[1].color = (0.52, 0.32, 0.16, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.22
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_cuero_tabaco():
    """Cuero marrón tabaco natural para taburetes de isla y poltronas de sala."""
    mat = bpy.data.materials.get("MAT_Suite_Cuero_Tabaco")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Cuero_Tabaco")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.42)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.45)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 0)
    voronoi.inputs['Scale'].default_value = 45.0
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-200, 100)
    ramp.color_ramp.elements[0].color = (0.28, 0.15, 0.08, 1.0)
    ramp.color_ramp.elements[1].color = (0.38, 0.22, 0.12, 1.0)
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.10
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_alfombra_yute():
    """Tejido artesanal de yute y lana para la gran alfombra de sala."""
    mat = bpy.data.materials.get("MAT_Suite_Alfombra_Yute")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Alfombra_Yute")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.76, 0.68, 0.56, 1.0))
    set_socket(bsdf, ['Roughness'], 0.90)
    set_socket(bsdf, ['Sheen Weight'], 0.5)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 40.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.25
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_piedra_laja():
    """Piedra laja alpina para panel mural de TV y salpicadero de cocina."""
    mat = bpy.data.materials.get("MAT_Piedra_Laja")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Piedra_Laja")
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
    ramp.color_ramp.elements[0].color = (0.22, 0.19, 0.17, 1.0)
    ramp.color_ramp.elements[1].color = (0.45, 0.38, 0.32, 1.0)
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.45
    bump.inputs['Distance'].default_value = 0.10
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def get_or_create_mat_inox_industrial():
    """Acero inoxidable satinado para nevera French Door, hornos y herrajes."""
    mat = bpy.data.materials.get("MAT_Inox_Industrial")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Inox_Industrial")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.85, 0.86, 0.87, 1.0))
    set_socket(bsdf, ['Metallic'], 1.0)
    set_socket(bsdf, ['Roughness'], 0.22)
    set_socket(bsdf, ['Anisotropic', 'Anisotropy'], 0.35)
    
    return mat

def get_or_create_mat_ceramica_blanca():
    """Porcelana cerámica blanca esmaltada para fregadero Farmhouse doble."""
    mat = bpy.data.materials.get("MAT_Suite_Ceramica_Blanca")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Ceramica_Blanca")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.97, 0.97, 0.97, 1.0))
    set_socket(bsdf, ['Roughness'], 0.08)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.7)
    return mat

def get_or_create_mat_metal_negro():
    """Hierro negro mate para grifería, estufa 5 hornillas, bases comedor y marco TV."""
    mat = bpy.data.materials.get("MAT_Suite_Metal_Negro")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Suite_Metal_Negro")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.08, 0.08, 0.08, 1.0))
    set_socket(bsdf, ['Metallic'], 0.85)
    set_socket(bsdf, ['Roughness'], 0.38)
    return mat

def get_or_create_mat_vidrio():
    """Vidrio templado transparente para cristales de hornos y carpintería."""
    mat = bpy.data.materials.get("MAT_Vidrio_Comercial")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Vidrio_Comercial")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.95, 0.98, 0.98, 1.0))
    set_socket(bsdf, ['Roughness'], 0.04)
    set_socket(bsdf, ['Transmission Weight', 'Transmission'], 0.95)
    set_socket(bsdf, ['IOR'], 1.52)
    return mat

def get_or_create_mat_estuco_blanco():
    """Estuco rústico blanco cálido para muros interiores sociales."""
    mat = bpy.data.materials.get("MAT_Muros_Estuco_Blanco")
    if mat and mat.use_nodes:
        return mat
    mat = mat or bpy.data.materials.new("MAT_Muros_Estuco_Blanco")
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

# --- NUEVOS MATERIALES EXCLUSIVOS DEL ÁREA SOCIAL ---

def create_mat_social_sofa_lino():
    """Lino gris cálido / crudo con tejido fino y sheen aterciopelado para sofá modular en L."""
    mat = bpy.data.materials.get("MAT_Social_Sofa_Lino") or bpy.data.materials.new("MAT_Social_Sofa_Lino")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.72)
    set_socket(bsdf, ['Sheen Weight'], 0.5)
    set_socket(bsdf, ['Sheen Tint'], (1.0, 0.95, 0.90, 1.0))
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (30.0, 30.0, 30.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-420, 100)
    wave.wave_type = 'BANDS'
    wave.inputs['Scale'].default_value = 12.0
    wave.inputs['Distortion'].default_value = 2.0
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.75, 0.72, 0.67, 1.0) # Gris cálido lino medio
    ramp.color_ramp.elements[1].color = (0.89, 0.86, 0.82, 1.0) # Blanco roto marfil
    links.new(wave.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.08
    links.new(wave.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_social_cocina_tope():
    """Cuarzo / granito gris antracita mate sedoso con micro-granos para topes de cocina e isla."""
    mat = bpy.data.materials.get("MAT_Social_Cocina_Tope") or bpy.data.materials.new("MAT_Social_Cocina_Tope")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.28) # Pulido mate sedoso
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.55)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-550, 0)
    noise.inputs['Scale'].default_value = 65.0
    noise.inputs['Detail'].default_value = 8.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-300, 100)
    ramp.color_ramp.elements[0].color = (0.13, 0.14, 0.15, 1.0) # Gris antracita profundo
    ramp.color_ramp.elements[1].color = (0.24, 0.25, 0.26, 1.0) # Granito satinado
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-300, -100)
    bump.inputs['Strength'].default_value = 0.03
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_social_pantalla_tv():
    """Cristal negro brillante de Smart TV 75\" con reflejos nítidos de alta gama."""
    mat = bpy.data.materials.get("MAT_Social_Pantalla_TV") or bpy.data.materials.new("MAT_Social_Pantalla_TV")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.015, 0.015, 0.015, 1.0))
    set_socket(bsdf, ['Roughness'], 0.06)
    set_socket(bsdf, ['Metallic'], 0.85)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.90)
    return mat


# =============================================================================
# 2. ASIGNACIÓN DETALLADA DE MATERIALES A LOS OBJETOS DEL ÁREA SOCIAL
# =============================================================================

def assign_social_materials():
    """Asigna con precisión milimétrica los materiales a cada polígono del área social."""
    print("Inicializando y cargando paleta de materiales PBR del Área Social...")
    m_roble      = get_or_create_mat_madera_roble()
    m_oscura     = get_or_create_mat_madera_oscura()
    m_deck       = get_or_create_mat_deck_teca()
    m_cuero      = get_or_create_mat_cuero_tabaco()
    m_yute       = get_or_create_mat_alfombra_yute()
    m_laja       = get_or_create_mat_piedra_laja()
    m_inox       = get_or_create_mat_inox_industrial()
    m_ceramica   = get_or_create_mat_ceramica_blanca()
    m_metal_neg  = get_or_create_mat_metal_negro()
    m_vidrio     = get_or_create_mat_vidrio()
    m_estuco     = get_or_create_mat_estuco_blanco()
    m_sofa_lino  = create_mat_social_sofa_lino()
    m_tope_cuarzo= create_mat_social_cocina_tope()
    m_tv_screen  = create_mat_social_pantalla_tv()
    m_pizarra    = bpy.data.materials.get("MAT_Suite_Pizarra_Negra")

    # -------------------------------------------------------------------------
    # A) P2_COCINA_ISLA_3D_mesh_ (Muebles bajos, torre, alacenas, isla y topes)
    # -------------------------------------------------------------------------
    obj_cocina = bpy.data.objects.get("P2_COCINA_ISLA_3D_mesh_")
    if obj_cocina and obj_cocina.type == 'MESH':
        obj_cocina.data.materials.clear()
        obj_cocina.data.materials.append(m_roble)       # Index 0: Madera roble rústico
        obj_cocina.data.materials.append(m_tope_cuarzo) # Index 1: Cuarzo gris oscuro mate
        
        mesh = obj_cocina.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z
            # Topes de piedra/cuarzo en mesón oeste e isla (Z = 3.84..3.92)
            if cz >= 3.84 and cz <= 3.92:
                # Barra desayunadora volada tablón rústico este de la isla (X >= 2.82)
                if cx >= 2.82 and cy <= 15.00:
                    poly.material_index = 0 # Madera roble
                else:
                    poly.material_index = 1 # Tope cuarzo oscuro
            else:
                poly.material_index = 0 # Muebles, gabinetes, torre y alacenas en roble
        print(f"  -> Asignados materiales a P2_COCINA_ISLA_3D_mesh_ ({len(mesh.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # B) P2_MOBILIARIO_SOCIAL_3D_mesh_ (Cocina, Comedor, Gran Sala y Balconada)
    # -------------------------------------------------------------------------
    obj_soc = bpy.data.objects.get("P2_MOBILIARIO_SOCIAL_3D_mesh_")
    if obj_soc and obj_soc.type == 'MESH':
        obj_soc.data.materials.clear()
        obj_soc.data.materials.append(m_roble)       # Index 0: Madera roble
        obj_soc.data.materials.append(m_oscura)      # Index 1: Madera oscura
        obj_soc.data.materials.append(m_sofa_lino)   # Index 2: Sofá lino gris cálido
        obj_soc.data.materials.append(m_yute)        # Index 3: Alfombra yute/lana
        obj_soc.data.materials.append(m_laja)        # Index 4: Piedra laja
        obj_soc.data.materials.append(m_inox)        # Index 5: Inox electrodomésticos
        obj_soc.data.materials.append(m_ceramica)    # Index 6: Cerámica blanca fregadero
        obj_soc.data.materials.append(m_metal_neg)   # Index 7: Metal negro forja
        obj_soc.data.materials.append(m_cuero)       # Index 8: Cuero tabaco
        obj_soc.data.materials.append(m_vidrio)      # Index 9: Vidrio hornos/vinera
        obj_soc.data.materials.append(m_deck)        # Index 10: Deck teca exterior
        obj_soc.data.materials.append(m_tv_screen)   # Index 11: Pantalla Smart TV 75"

        mesh = obj_soc.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z

            # 1. ZONA BALCONADA SOCIAL TECHADA (Y >= 22.50)
            if cy >= 22.50:
                if cx <= 1.30: # Sofá exterior oeste
                    if cz <= 3.40:
                        poly.material_index = 10 # Base madera teca
                    else:
                        poly.material_index = 2  # Cojines lino impermeable
                elif cx <= 2.20: # Mesa café terraza
                    poly.material_index = 10     # Madera teca
                else: # Mesa mirador 4p y bancas
                    poly.material_index = 10     # Madera teca exterior

            # 2. ZONA GRAN SALA CHALET (Y in [18.50, 22.50))
            elif cy >= 18.50:
                if cx <= 1.30: # Poltronas de lectura y mesita auxiliar oeste
                    if cx >= 0.60 and cy >= 20.35 and cy <= 20.65:
                        poly.material_index = 0 # Mesita auxiliar roble
                    else:
                        poly.material_index = 8 # Poltronas cuero marrón tabaco
                elif cx >= 3.00 and cz <= 3.03: # Alfombra gran salón
                    poly.material_index = 3     # Alfombra yute / lana rústica
                elif cx >= 5.30: # Zona Muro TV este
                    if cx >= 5.71:
                        poly.material_index = 4 # Panel piedra laja
                    elif cz <= 3.55:
                        poly.material_index = 0 # Consola baja TV roble
                    else: # Smart TV 75"
                        if abs(poly.normal.x) > 0.7:
                            poly.material_index = 11 # Pantalla TV ultra-black gloss
                        else:
                            poly.material_index = 7  # Marco y soporte metal negro
                elif cx >= 4.10 and cx <= 4.95 and cy >= 20.00 and cy <= 21.20 and cz <= 3.45:
                    poly.material_index = 0     # Mesa centro maciza tipo tronco
                elif cx >= 3.00 and cx <= 5.20 and (cy >= 21.50 or (cx <= 3.95 and cy >= 19.50)):
                    poly.material_index = 2     # Gran Sofá modular en L (lino gris cálido)
                else:
                    poly.material_index = 0

            # 3. ZONA GRAN COMEDOR 8 PUESTOS (Y in [15.50, 18.50))
            elif cy >= 15.50:
                if cx <= 1.00: # Buffet y vinera mural oeste
                    poly.material_index = 0     # Madera roble macizo
                elif cz >= 4.80: # Lámpara lineal suspendida sobre comedor
                    poly.material_index = 1     # Viga madera oscura rústica
                elif cx >= 2.25 and cx <= 4.55 and cy >= 16.50 and cy <= 17.65: # Mesa comedor 8p
                    if cz <= 3.70 and (cx <= 2.75 or cx >= 4.05):
                        poly.material_index = 7 # Bases trapecio hierro negro
                    else:
                        poly.material_index = 0 # Tablón macizo roble 2,20x1,05m
                else: # Sillas de comedor
                    if cz <= 3.48:
                        poly.material_index = 2 # Asiento tapizado lino cálido
                    else:
                        poly.material_index = 0 # Respaldo roble

            # 4. ZONA COCINA RÚSTICA DE MONTAÑA (Y < 15.50)
            else:
                if cx >= 3.00 and cx <= 3.50: # 4 Taburetes altos de barra
                    if cz <= 3.62:
                        poly.material_index = 7 # Patas metal negro
                    else:
                        poly.material_index = 8 # Asiento cuero tabaco acolchado
                elif cz >= 4.80: # Lámparas colgantes sobre isla
                    poly.material_index = 7     # Metal negro
                elif cx >= 1.40 and cx <= 2.33 and cy <= 11.35: # Nevera French Door
                    if cy >= 11.29 and cz >= 3.84 and cz <= 4.66:
                        poly.material_index = 7 # Tiradores metal negro
                    else:
                        poly.material_index = 5 # Acero inoxidable cepillado
                elif cx >= 2.33 and cx <= 2.75 and cy <= 11.35: # Torre de hornos empotrada
                    if cy >= 11.26:
                        poly.material_index = 9 # Cristal horno / microondas
                    else:
                        poly.material_index = 5 # Acero inoxidable
                elif cx <= 1.05: # Mesón lineal oeste y cocción
                    if cx <= 0.35:
                        poly.material_index = 4 # Salpicadero piedra laja
                    elif cx >= 0.86 and cy >= 12.10 and cy <= 13.15:
                        poly.material_index = 6 # Fregadero Farmhouse porcelana blanca
                    elif cy >= 12.55 and cy <= 12.72 and cz >= 3.90:
                        poly.material_index = 7 # Grifería alta monomando negra
                    elif cy >= 13.98 and cy <= 15.00 and cz >= 3.90 and cz <= 3.96:
                        poly.material_index = 7 # Cocina 5 hornillas gas negro mate
                    elif cx >= 0.90 and cy >= 14.00 and cy <= 14.95 and cz <= 3.80:
                        poly.material_index = 5 # Horno bajo encimera inox
                    elif cy >= 13.90 and cy <= 15.05 and cz >= 4.50: # Campana extractora piramidal
                        if cz <= 4.66:
                            poly.material_index = 7 # Cinchos / faldón forja negra
                        else:
                            poly.material_index = 1 # Campana madera rústica
                    else:
                        poly.material_index = 0
                else:
                    poly.material_index = 0
        print(f"  -> Asignados materiales a P2_MOBILIARIO_SOCIAL_3D_mesh_ ({len(mesh.polygons)} polígonos)")

    # -------------------------------------------------------------------------
    # C) P2_LOSA_PISO_3D_mesh_ (Pisos zonificados: Roble, Teca, Pizarra)
    # -------------------------------------------------------------------------
    obj_losa = bpy.data.objects.get("P2_LOSA_PISO_3D_mesh_")
    if obj_losa and obj_losa.type == 'MESH':
        obj_losa.data.materials.clear()
        obj_losa.data.materials.append(m_roble)   # Index 0: Roble interior
        obj_losa.data.materials.append(m_deck)    # Index 1: Deck teca terrazas
        if m_pizarra:
            obj_losa.data.materials.append(m_pizarra) # Index 2: Pizarra baño spa
        
        mesh = obj_losa.data
        for poly in mesh.polygons:
            cx, cy = poly.center.x, poly.center.y
            if cx >= 5.85: # Crujía Este (Suite, Terraza privada, Vestier, Baño)
                if cy >= 22.45:
                    poly.material_index = 1 # Terraza suite deck teca
                elif cy >= 15.55:
                    poly.material_index = 0 # Dormitorio y vestier roble
                elif cy >= 13.15 and len(obj_losa.data.materials) > 2:
                    poly.material_index = 2 # Baño spa pizarra
                else:
                    poly.material_index = 0
            else: # Crujía Oeste (Área Social)
                if cy >= 22.50:
                    poly.material_index = 1 # Balcón social techado deck teca
                else:
                    poly.material_index = 0 # Cocina, comedor, sala y pasillos roble
        print("  -> Piso de P2_LOSA_PISO_3D_mesh_ zonificado (Roble en sala/comedor/cocina, Deck teca en balcón)")

    # -------------------------------------------------------------------------
    # D) P2_BALCON_MADERA_3D_mesh_ (Barandillas alpinas en X de madera oscura)
    # -------------------------------------------------------------------------
    obj_balc = bpy.data.objects.get("P2_BALCON_MADERA_3D_mesh_")
    if obj_balc and obj_balc.type == 'MESH':
        obj_balc.data.materials.clear()
        obj_balc.data.materials.append(m_oscura)
        print("  -> Asignado MAT_Suite_Madera_Oscura a P2_BALCON_MADERA_3D_mesh_")

    # -------------------------------------------------------------------------
    # E) P2_MUROS_MADERA_INT_3D_mesh_ (Estuco blanco cálido rústico)
    # -------------------------------------------------------------------------
    obj_m_int = bpy.data.objects.get("P2_MUROS_MADERA_INT_3D_mesh_")
    if obj_m_int and obj_m_int.type == 'MESH':
        obj_m_int.data.materials.clear()
        obj_m_int.data.materials.append(m_estuco)
        print("  -> Asignado MAT_Muros_Estuco_Blanco a P2_MUROS_MADERA_INT_3D_mesh_")

    # -------------------------------------------------------------------------
    # F) P2_CARPINTERIA_RUSTICA_3D_mesh_ (Marcos madera oscura y vidrio)
    # -------------------------------------------------------------------------
    obj_carp = bpy.data.objects.get("P2_CARPINTERIA_RUSTICA_3D_mesh_")
    if obj_carp and obj_carp.type == 'MESH':
        obj_carp.data.materials.clear()
        obj_carp.data.materials.append(m_oscura)
        obj_carp.data.materials.append(m_vidrio)
        print("  -> Asignada carpintería rústica a P2_CARPINTERIA_RUSTICA_3D_mesh_")


# =============================================================================
# 3. ILUMINACIÓN INTERIOR CÁLIDA Y ACOGEDORA PARA EL ÁREA SOCIAL
# =============================================================================

def setup_social_lighting():
    """Instala iluminación cálida en isla, cocina, comedor, gran sala y balconada."""
    print("Configurando iluminación cálida (2700K - 3000K) para el Área Social...")
    col_lgt = bpy.data.collections.get("P2_ILUMINACION_SOCIAL")
    if not col_lgt:
        col_lgt = bpy.data.collections.new("P2_ILUMINACION_SOCIAL")
        bpy.context.scene.collection.children.link(col_lgt)
    else:
        # Limpiar luces previas en caso de re-ejecución
        for o in list(col_lgt.objects):
            bpy.data.objects.remove(o, do_unlink=True)

    lights_data = [
        # 1. Luces colgantes sobre la Isla de Cocina (focos cálidos 2800K)
        ("Luz_Social_Isla_Sur",         (2.48, 13.25, 4.35), 'POINT', 45.0, (1.0, 0.88, 0.70)),
        ("Luz_Social_Isla_Norte",       (2.48, 14.35, 4.35), 'POINT', 45.0, (1.0, 0.88, 0.70)),
        # 2. Luz general de trabajo en Cocina
        ("Luz_Social_Techo_Cocina",     (1.60, 13.50, 5.20), 'POINT', 65.0, (1.0, 0.92, 0.82)),
        # 3. Lámpara lineal sobre Gran Comedor 8 Puestos (cálida 2700K)
        ("Luz_Social_Comedor_Arana",    (3.40, 17.05, 4.55), 'POINT', 75.0, (1.0, 0.86, 0.65)),
        # 4. Luz principal ambiental Gran Sala Chalet
        ("Luz_Social_Techo_Sala",       (4.20, 20.80, 5.30), 'POINT', 85.0, (1.0, 0.90, 0.78)),
        # 5. Luz de lectura cálida sobre poltronas oeste
        ("Luz_Social_Lectura_Poltronas",(0.85, 20.50, 4.20), 'POINT', 35.0, (1.0, 0.85, 0.68)),
        # 6. Iluminación indirecta panel de piedra TV (tira LED cálida trasera)
        ("Luz_Social_Panel_TV",         (5.70, 20.50, 4.00), 'POINT', 30.0, (1.0, 0.82, 0.60)),
        # 7. Apliques exteriores en balconada social techada
        ("Luz_Social_Balcon_Oeste",     (1.80, 22.75, 4.40), 'POINT', 40.0, (1.0, 0.85, 0.65)),
        ("Luz_Social_Balcon_Este",      (4.50, 22.75, 4.40), 'POINT', 40.0, (1.0, 0.85, 0.65)),
    ]

    for name, loc, ltype, energy, color in lights_data:
        l_data = bpy.data.lights.new(name=name, type=ltype)
        l_data.energy = energy
        l_data.color = color
        l_obj = bpy.data.objects.new(name, l_data)
        l_obj.location = loc
        col_lgt.objects.link(l_obj)

    print(f"  -> {len(lights_data)} luminarias ambientales instaladas en el Área Social.")


# =============================================================================
# 4. CÁMARAS DE PRESENTACIÓN PARA EL ÁREA SOCIAL
# =============================================================================

def set_camera_look_at(cam_obj, target_pos):
    """Orienta una cámara de forma precisa hacia un punto de mira 3D."""
    loc = cam_obj.location
    direction = mathutils.Vector(target_pos) - loc
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

def setup_social_cameras():
    """Configura 4 cámaras cinematográficas para la Cocina, Comedor, Sala y Balconada."""
    print("Configurando cámaras cinematográficas de presentación para el Área Social...")
    col_cam = bpy.data.collections.get("P2_CAMARAS_SOCIAL")
    if not col_cam:
        col_cam = bpy.data.collections.new("P2_CAMARAS_SOCIAL")
        bpy.context.scene.collection.children.link(col_cam)
    else:
        for o in list(col_cam.objects):
            bpy.data.objects.remove(o, do_unlink=True)

    cams_data = [
        # 1. Gran Sala: Mirando al sofá modular en L, panel de piedra TV y ventanales
        ("Camara_Social_1_Gran_Sala",       (1.50, 18.50, 4.25), (4.50, 21.00, 3.80), 20.0),
        # 2. Gran Comedor y Cocina: Perspectiva amplia del comedor 8p y la isla
        ("Camara_Social_2_Comedor_Cocina",  (4.80, 19.80, 4.35), (2.50, 14.50, 3.80), 22.0),
        # 3. Cocina Rústica con Isla: Encuadre cercano de la isla, taburetes y muebles
        ("Camara_Social_3_Isla_Cocina",     (4.00, 12.00, 4.20), (2.10, 13.80, 3.80), 24.0),
        # 4. Balconada Social Techada: Perspectiva hacia Avenida 4 con barandas alpinas
        ("Camara_Social_4_Balconada_Social",(1.00, 22.80, 4.20), (4.80, 23.80, 3.85), 20.0),
    ]

    for name, loc, target, focal in cams_data:
        c_data = bpy.data.cameras.new(name=name)
        c_data.lens = focal
        c_data.clip_start = 0.1
        c_data.clip_end = 120.0
        c_obj = bpy.data.objects.new(name, c_data)
        c_obj.location = loc
        set_camera_look_at(c_obj, target)
        col_cam.objects.link(c_obj)
        print(f"  -> Cámara creada: {name} en {loc} apuntando a {target}")


# =============================================================================
# 5. GUARDADO DEL ARCHIVO BLENDER (SIN RENDERIZAR NADA)
# =============================================================================

def save_blend_files():
    """Guarda directamente casaBlender.blend y casaBlender_texturizada.blend."""
    print("Guardando archivos .blend actualizados con el Área Social texturizada...")
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
    print("TEXTURIZADO INTEGRAL DE ÁREA SOCIAL P2: COCINA, COMEDOR, SALA Y BALCÓN")
    print("==================================================================")
    assign_social_materials()
    setup_social_lighting()
    setup_social_cameras()
    save_blend_files()
    print("==================================================================")
    print("¡PROCESO COMPLETADO SATISFACTORIAMENTE (SIN RENDERIZAR)!")
    print("==================================================================")

if __name__ == "__main__":
    main()
