"""
Script de Automatización para Blender (bpy)
Aplica Texturas PBR Fotorrealistas, Iluminación Cálida y Cámaras a la Master Suite
(Dormitorio King, Terraza Privada, Gran Vestier Walk-In y Baño Spa en Piedra Pizarra)
Sin renderizar nada (solo asigna materiales, iluminación, cámaras y guarda el archivo .blend).
Compatible con Blender 4.x y 5.x.
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
# 1. MATERIALES PBR PARA LA MASTER SUITE, TERRAZA, VESTIER Y BAÑO SPA
# =============================================================================

def create_mat_suite_madera_roble():
    """Roble satinado para cama King, mesas de noche y muebles de vestier/baño."""
    mat = bpy.data.materials.get("MAT_Suite_Madera_Roble") or bpy.data.materials.new("MAT_Suite_Madera_Roble")
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

def create_mat_suite_madera_oscura():
    """Madera alpina oscura para riel de granero, puerta granero, vigas y molduras."""
    mat = bpy.data.materials.get("MAT_Suite_Madera_Oscura") or bpy.data.materials.new("MAT_Suite_Madera_Oscura")
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

def create_mat_suite_deck_teca():
    """Madera de teca impregnada para deck de terraza exterior y poltronas."""
    mat = bpy.data.materials.get("MAT_Suite_Deck_Teca") or bpy.data.materials.new("MAT_Suite_Deck_Teca")
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

def create_mat_suite_cuero_tabaco():
    """Cuero natural marrón tabaco cálido para cabecero de cama y pouf."""
    mat = bpy.data.materials.get("MAT_Suite_Cuero_Tabaco") or bpy.data.materials.new("MAT_Suite_Cuero_Tabaco")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.42)
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.45)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 0)
    voronoi.inputs['Scale'].default_value = 45.0 # Poro de cuero fino
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

def create_mat_suite_lino_blanco():
    """Lino natural blanco marfil suave para colchón, sobrecama y almohadas."""
    mat = bpy.data.materials.get("MAT_Suite_Lino_Blanco") or bpy.data.materials.new("MAT_Suite_Lino_Blanco")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.94, 0.93, 0.90, 1.0))
    set_socket(bsdf, ['Roughness'], 0.75)
    set_socket(bsdf, ['Sheen Weight'], 0.4) # Aspecto aterciopelado textil
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 65.0 # Trama de tejido textil
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.06
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_suite_alfombra_yute():
    """Tejido rústico de yute / lana natural para alfombra de dormitorio."""
    mat = bpy.data.materials.get("MAT_Suite_Alfombra_Yute") or bpy.data.materials.new("MAT_Suite_Alfombra_Yute")
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

def create_mat_suite_pizarra_negra():
    """Piedra pizarra gris grafito/negra antideslizante para plato de ducha y baño spa."""
    mat = bpy.data.materials.get("MAT_Suite_Pizarra_Negra") or bpy.data.materials.new("MAT_Suite_Pizarra_Negra")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Roughness'], 0.65)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-620, 0)
    mapping.inputs['Scale'].default_value = (5.0, 5.0, 5.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-420, 100)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 5.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-220, 100)
    ramp.color_ramp.elements[0].color = (0.12, 0.12, 0.13, 1.0) # Grafito oscuro
    ramp.color_ramp.elements[1].color = (0.24, 0.25, 0.26, 1.0) # Pizarra media
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], get_socket(bsdf, ['Base Color']))
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-220, -150)
    bump.inputs['Strength'].default_value = 0.35
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], get_socket(bsdf, ['Normal']))
    
    return mat

def create_mat_suite_ceramica_blanca():
    """Cerámica sanitaria blanca brillante para lavamanos vessel e inodoro."""
    mat = bpy.data.materials.get("MAT_Suite_Ceramica_Blanca") or bpy.data.materials.new("MAT_Suite_Ceramica_Blanca")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.96, 0.97, 0.98, 1.0))
    set_socket(bsdf, ['Roughness'], 0.10) # Acabado esmaltado vitrificado
    set_socket(bsdf, ['Specular IOR Level', 'Specular'], 0.7)
    
    return mat

def create_mat_suite_metal_negro():
    """Metal negro mate para grifería, perfiles de mampara, regadera y barras de vestier."""
    mat = bpy.data.materials.get("MAT_Suite_Metal_Negro") or bpy.data.materials.new("MAT_Suite_Metal_Negro")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.10, 0.10, 0.10, 1.0))
    set_socket(bsdf, ['Metallic'], 0.85)
    set_socket(bsdf, ['Roughness'], 0.35)
    
    return mat

def create_mat_suite_espejo():
    """Espejo de alta reflexión sin distorsión para vestier y baño spa."""
    mat = bpy.data.materials.get("MAT_Suite_Espejo") or bpy.data.materials.new("MAT_Suite_Espejo")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.98, 0.98, 0.98, 1.0))
    set_socket(bsdf, ['Metallic'], 1.0)
    set_socket(bsdf, ['Roughness'], 0.005) # Espejo nítido
    
    return mat

def create_mat_suite_vidrio_ducha():
    """Cristal templado transparente para mampara de ducha."""
    mat = bpy.data.materials.get("MAT_Suite_Vidrio_Ducha") or bpy.data.materials.new("MAT_Suite_Vidrio_Ducha")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.96, 0.98, 1.0, 1.0))
    set_socket(bsdf, ['Roughness'], 0.02)
    set_socket(bsdf, ['IOR'], 1.45)
    set_socket(bsdf, ['Transmission Weight', 'Transmission'], 1.0)
    
    return mat

def create_mat_suite_follaje():
    """Follaje verde natural para jardinera de terraza."""
    mat = bpy.data.materials.get("MAT_Suite_Follaje") or bpy.data.materials.new("MAT_Suite_Follaje")
    nodes, links, bsdf = clean_material_nodes(mat)
    
    set_socket(bsdf, ['Base Color'], (0.15, 0.42, 0.12, 1.0))
    set_socket(bsdf, ['Roughness'], 0.50)
    set_socket(bsdf, ['Subsurface Weight'], 0.15) # Translucidez de hojas
    
    return mat


# =============================================================================
# 2. ASIGNACIÓN DE MATERIALES EN P2 (SUITE, TERRAZA, VESTIER Y BAÑO SPA)
# =============================================================================

def assign_suite_materials():
    print("Creando catálogo de materiales PBR para la Master Suite...")
    m_roble    = create_mat_suite_madera_roble()
    m_oscura   = create_mat_suite_madera_oscura()
    m_deck     = create_mat_suite_deck_teca()
    m_cuero    = create_mat_suite_cuero_tabaco()
    m_lino     = create_mat_suite_lino_blanco()
    m_yute     = create_mat_suite_alfombra_yute()
    m_pizarra  = create_mat_suite_pizarra_negra()
    m_ceramica = create_mat_suite_ceramica_blanca()
    m_metal_neg= create_mat_suite_metal_negro()
    m_espejo   = create_mat_suite_espejo()
    m_vidrio_d = create_mat_suite_vidrio_ducha()
    m_follaje  = create_mat_suite_follaje()
    m_laja     = bpy.data.materials.get("MAT_Piedra_Laja") # Reutilizar laja de PB

    # 1. Mobiliario de la Suite (Cama King, vestier, baño spa y terraza)
    obj_suite = bpy.data.objects.get("P2_MOBILIARIO_SUITE_3D_mesh_")
    if obj_suite and obj_suite.type == 'MESH':
        obj_suite.data.materials.clear()
        obj_suite.data.materials.append(m_roble)     # Index 0: Roble natural
        obj_suite.data.materials.append(m_oscura)    # Index 1: Madera oscura
        obj_suite.data.materials.append(m_cuero)     # Index 2: Cuero tabaco
        obj_suite.data.materials.append(m_lino)      # Index 3: Lino blanco
        obj_suite.data.materials.append(m_yute)      # Index 4: Alfombra yute
        obj_suite.data.materials.append(m_laja)      # Index 5: Piedra laja
        obj_suite.data.materials.append(m_pizarra)   # Index 6: Pizarra negra
        obj_suite.data.materials.append(m_ceramica)  # Index 7: Cerámica blanca
        obj_suite.data.materials.append(m_metal_neg) # Index 8: Metal negro
        obj_suite.data.materials.append(m_espejo)    # Index 9: Espejo
        obj_suite.data.materials.append(m_vidrio_d)  # Index 10: Vidrio ducha
        obj_suite.data.materials.append(m_deck)      # Index 11: Deck teca terraza
        obj_suite.data.materials.append(m_follaje)   # Index 12: Follaje terraza
        
        mesh = obj_suite.data
        for poly in mesh.polygons:
            cx, cy, cz = poly.center.x, poly.center.y, poly.center.z
            
            # --- ZONA 1: TERRAZA PRIVADA (Y >= 22.45) ---
            if cy >= 22.45:
                if cx >= 8.35 and cz < 3.55:
                    poly.material_index = 5  # Jardinera piedra laja
                elif cx >= 8.35 and cz >= 3.55:
                    poly.material_index = 12 # Follaje verde aromático
                elif cz <= 3.42:
                    poly.material_index = 11 # Poltronas / mesa madera teca
                else:
                    poly.material_index = 3  # Cojines lino
            
            # --- ZONA 2: DORMITORIO MASTER SUITE (Y in [17.80, 22.45]) ---
            elif cy in [17.80, 22.45] or (cy >= 17.80 and cy < 22.45):
                # Muro cabecero oeste (X <= 6.15)
                if cx <= 6.16:
                    if cy >= 19.60 and cy <= 21.60:
                        poly.material_index = 5 # Paño central piedra laja
                    else:
                        poly.material_index = 1 # Marco madera oscura
                # Alfombra bajo la cama
                elif cz <= 3.03:
                    poly.material_index = 4 # Alfombra yute/lana
                # Cama King
                elif cx >= 6.14 and cx <= 8.05 and cy >= 19.70 and cy <= 21.50:
                    if cz <= 3.33:
                        poly.material_index = 0 # Base madera roble
                    elif cz <= 3.59:
                        poly.material_index = 3 # Colchón y sobrecama lino
                    elif cx <= 6.28 and cz >= 3.58:
                        poly.material_index = 2 # Cabecero cuero tabaco
                    else:
                        poly.material_index = 3 # Almohadas lino blanco
                # Mesas de noche y consola
                elif cz <= 3.65:
                    poly.material_index = 0 # Roble
                # Lámparas colgantes
                else:
                    poly.material_index = 8 # Metal negro
            
            # --- ZONA 3: GRAN VESTIER WALK-IN (Y in [15.55, 17.80]) ---
            elif cy >= 15.55 and cy < 17.80:
                # Puerta granero en Y=17.95
                if cy >= 17.75:
                    if cz >= 5.15:
                        poly.material_index = 8 # Riel hierro negro
                    else:
                        poly.material_index = 1 # Hoja madera granero
                # Pouf central
                elif cx >= 7.15 and cx <= 7.85 and cy >= 16.25 and cy <= 17.15:
                    poly.material_index = 2 # Cuero tabaco
                # Espejo cuerpo entero (Y <= 15.70)
                elif cy <= 15.70 and cx >= 6.60 and cx <= 7.10:
                    if cx >= 6.65 and cx <= 7.02 and cz >= 3.12 and cz <= 5.02:
                        poly.material_index = 9 # Luna espejo
                    else:
                        poly.material_index = 8 # Marco metal negro
                # Módulos de closet y maleteros
                else:
                    if cz >= 4.80 and cz <= 4.92:
                        poly.material_index = 8 # Barra colgar ropa
                    else:
                        poly.material_index = 0 # Madera roble
            
            # --- ZONA 4: BAÑO EN-SUITE SPA (Y in [13.15, 15.55]) ---
            else:
                # Ducha Spa (X >= 7.90)
                if cx >= 7.90:
                    if cz <= 3.10 or (cx >= 8.50 and cz <= 3.55):
                        poly.material_index = 6  # Plato pizarra antideslizante y banco
                    elif cz >= 5.10:
                        poly.material_index = 8  # Regadera rain shower / perfil superior
                    elif cx <= 8.05 and cz <= 5.10:
                        if cz >= 3.05 and cz <= 5.10 and cy >= 13.20 and cy <= 14.50:
                            poly.material_index = 10 # Mampara cristal templado
                        else:
                            poly.material_index = 8  # Perfilería negra
                    else:
                        poly.material_index = 6  # Muro pizarra
                # Inodoro (cx in [6.95, 7.45])
                elif cx >= 6.95 and cx <= 7.45:
                    poly.material_index = 7 # Cerámica blanca brillante
                # Tocador doble y espejos
                else:
                    if cz >= 3.85 and cz <= 4.05 and cy in [13.45, 13.95, 14.25, 14.75]:
                        poly.material_index = 7 # Lavamanos vessel cerámica
                    elif cz >= 4.05 and cx <= 6.22 and cz <= 4.20:
                        poly.material_index = 8 # Grifo monomando negro
                    elif cz >= 4.10 and cz <= 5.15 and cx <= 6.12:
                        poly.material_index = 9 # Espejos
                    else:
                        poly.material_index = 0 # Mueble y tope madera roble

        print("  -> Materiales detallados asignados a P2_MOBILIARIO_SUITE_3D_mesh_")

    # 2. Piso de Losa P2 (Dormitorio y Vestier en roble, Terraza en deck teca, Baño en pizarra)
    obj_losa2 = bpy.data.objects.get("P2_LOSA_PISO_3D_mesh_")
    if obj_losa2 and obj_losa2.type == 'MESH':
        obj_losa2.data.materials.clear()
        obj_losa2.data.materials.append(m_roble)   # Index 0: Roble dormitorio/vestier
        obj_losa2.data.materials.append(m_deck)    # Index 1: Deck teca terraza
        obj_losa2.data.materials.append(m_pizarra) # Index 2: Pizarra baño spa
        
        mesh = obj_losa2.data
        for poly in mesh.polygons:
            cx, cy = poly.center.x, poly.center.y
            if cx >= 5.85:
                if cy >= 22.45:
                    poly.material_index = 1 # Terraza suite
                elif cy >= 15.55:
                    poly.material_index = 0 # Dormitorio y vestier
                elif cy >= 13.15:
                    poly.material_index = 2 # Baño spa
                else:
                    poly.material_index = 0
            else:
                poly.material_index = 0
        print("  -> Piso de P2_LOSA_PISO_3D_mesh_ zonificado (Deck, Roble, Pizarra)")

    # 3. Barandilla alpina de madera en la terraza de la suite
    obj_balc = bpy.data.objects.get("P2_BALCON_MADERA_3D_mesh_")
    if obj_balc and obj_balc.type == 'MESH':
        obj_balc.data.materials.clear()
        obj_balc.data.materials.append(m_oscura)
        print("  -> Asignado MAT_Suite_Madera_Oscura a P2_BALCON_MADERA_3D_mesh_")

    # 4. Muros interiores P2 (Suite, vestier, baño)
    m_estuco = bpy.data.materials.get("MAT_Muros_Estuco_Blanco")
    obj_m_int = bpy.data.objects.get("P2_MUROS_MADERA_INT_3D_mesh_")
    if obj_m_int and obj_m_int.type == 'MESH':
        obj_m_int.data.materials.clear()
        obj_m_int.data.materials.append(m_estuco)
        print("  -> Asignado MAT_Muros_Estuco_Blanco a P2_MUROS_MADERA_INT_3D_mesh_")

    # 5. Muros exteriores P2
    obj_m_ext = bpy.data.objects.get("P2_MUROS_MADERA_EXT_3D_mesh_")
    if obj_m_ext and obj_m_ext.type == 'MESH':
        obj_m_ext.data.materials.clear()
        obj_m_ext.data.materials.append(m_oscura)
        print("  -> Asignado MAT_Suite_Madera_Oscura a P2_MUROS_MADERA_EXT_3D_mesh_")

    # 6. Carpintería rústica (puertas corredizas terraza, ventanas este con shutters)
    obj_carp = bpy.data.objects.get("P2_CARPINTERIA_RUSTICA_3D_mesh_")
    if obj_carp and obj_carp.type == 'MESH':
        obj_carp.data.materials.clear()
        obj_carp.data.materials.append(m_oscura)
        print("  -> Asignado MAT_Suite_Madera_Oscura a P2_CARPINTERIA_RUSTICA_3D_mesh_")


# =============================================================================
# 3. ILUMINACIÓN INTERIOR CÁLIDA (3000K) PARA LA MASTER SUITE
# =============================================================================

def setup_suite_lighting():
    """Configura luces ambientales cálidas en veladores, vestier, baño y terraza."""
    print("Configurando iluminación cálida para la Master Suite...")
    col_lgt = bpy.data.collections.get("P2_ILUMINACION_SUITE")
    if not col_lgt:
        col_lgt = bpy.data.collections.new("P2_ILUMINACION_SUITE")
        bpy.context.scene.collection.children.link(col_lgt)

    lights_data = [
        # Veladores cama King (Spot cálido suave 2800K)
        ("Luz_Velador_Sur",      (6.40, 19.41, 4.20), 'POINT', 25.0, (1.0, 0.85, 0.68)),
        ("Luz_Velador_Norte",    (6.40, 21.79, 4.20), 'POINT', 25.0, (1.0, 0.85, 0.68)),
        # Luz ambiental dormitorio
        ("Luz_Techo_Dormitorio", (7.50, 20.60, 5.40), 'POINT', 70.0, (1.0, 0.90, 0.78)),
        # Luz Vestier Walk-In (foco cálido sobre el pouf y roperos)
        ("Luz_Vestier_Central",  (7.50, 16.70, 5.20), 'POINT', 65.0, (1.0, 0.92, 0.82)),
        # Luz Baño Spa (foco sobre tocador doble y espejos)
        ("Luz_Bano_Tocador",     (6.35, 14.10, 4.80), 'POINT', 60.0, (1.0, 0.94, 0.86)),
        # Luz relajante Ducha Spa
        ("Luz_Bano_DuchaSpa",    (8.45, 14.10, 4.80), 'POINT', 40.0, (0.92, 0.95, 1.0)),
        # Aplique exterior cálido en la terraza privada
        ("Luz_Terraza_Suite",    (6.15, 23.50, 4.20), 'POINT', 35.0, (1.0, 0.82, 0.60)),
    ]

    for name, loc, ltype, energy, color in lights_data:
        l_data = bpy.data.lights.new(name=name, type=ltype)
        l_data.energy = energy
        l_data.color = color
        l_obj = bpy.data.objects.new(name, l_data)
        l_obj.location = loc
        col_lgt.objects.link(l_obj)

    print("  -> 7 luminarias de ambiente instaladas en la Master Suite.")


# =============================================================================
# 4. CÁMARAS DE PRESENTACIÓN PARA LA MASTER SUITE
# =============================================================================

def setup_suite_cameras():
    """Configura 4 cámaras específicas para la Suite sin alterar las anteriores."""
    print("Configurando cámaras cinematográficas de la Master Suite...")
    col_cam = bpy.data.collections.get("P2_CAMARAS_SUITE")
    if not col_cam:
        col_cam = bpy.data.collections.new("P2_CAMARAS_SUITE")
        bpy.context.scene.collection.children.link(col_cam)

    cams_suite = [
        # 1. Vista principal Dormitorio King mirando al cabecero y ventanal
        ("Camara_Suite_1_Dormitorio", (8.60, 18.20, 4.20), (math.radians(75), 0, math.radians(-35)), 22.0),
        # 2. Vista Terraza Privada hacia Avenida 4
        ("Camara_Suite_2_Terraza",    (6.20, 22.00, 4.30), (math.radians(82), 0, math.radians(15)),  20.0),
        # 3. Vista Gran Vestier Walk-In y Puerta Granero
        ("Camara_Suite_3_Vestier",    (7.50, 15.65, 4.40), (math.radians(78), 0, math.radians(0)),   20.0),
        # 4. Vista Baño En-Suite Spa (Tocador doble y Ducha de piedra)
        ("Camara_Suite_4_BanoSpa",    (6.20, 15.30, 4.35), (math.radians(76), 0, math.radians(-40)), 20.0),
    ]

    for name, loc, rot, focal in cams_suite:
        c_data = bpy.data.cameras.new(name=name)
        c_data.lens = focal
        c_data.clip_start = 0.1
        c_data.clip_end = 100.0
        c_obj = bpy.data.objects.new(name, c_data)
        c_obj.location = loc
        c_obj.rotation_euler = rot
        col_cam.objects.link(c_obj)
        print(f"  -> Cámara creada: {name}")


# =============================================================================
# 5. GUARDADO DEL ARCHIVO BLENDER (SIN RENDERIZAR)
# =============================================================================

def save_blend_files():
    """Guarda casaBlender.blend y casaBlender_texturizada.blend sin renderizar nada."""
    print("Guardando archivos .blend actualizados con la Master Suite texturizada...")
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
    print("TEXTURIZADO DE LA MASTER SUITE, TERRAZA, VESTIER Y BAÑO SPA")
    print("==================================================================")
    assign_suite_materials()
    setup_suite_lighting()
    setup_suite_cameras()
    save_blend_files()
    print("==================================================================")
    print("¡PROCESO COMPLETADO SATISFACTORIAMENTE (SIN RENDERIZAR)!")
    print("==================================================================")

if __name__ == "__main__":
    main()
