"""
Exportador de formatos 3D universales (OBJ y STL) para la casa
Genera modelo poligonal 3D listo para cualquier visor 3D o CAD
"""

import os

def create_3d_models():
    # Parametros
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

    boxes = []

    def add_box(name, x1, y1, z1, x2, y2, z2):
        boxes.append((name, min(x1, x2), min(y1, y2), min(z1, z2),
                            max(x1, x2), max(y1, y2), max(z1, z2)))

    # 1. Losa de piso
    add_box("Losa_Sur", 0.00, 0.00, -SLAB_T, W_X, 4.45, 0.00)
    add_box("Losa_Norte", 0.00, 7.40, -SLAB_T, W_X, L_Y, 0.00)
    add_box("Losa_Este", 1.45, 4.45, -SLAB_T, W_X, 7.40, 0.00)
    add_box("Losa_Oeste", 0.00, 4.45, -SLAB_T, 0.20, 7.40, 0.00)

    # 2. Escalera
    for i in range(10):
        y_step = 7.40 - i * (2.95 / 10.0)
        z_step = 0.00 - (i + 1) * (1.40 / 10.0)
        add_box(f"Escalon_{i}", 0.20, y_step - (2.95 / 10.0), z_step, 1.45, y_step, z_step + 0.14)

    # 3. Muros exteriores
    # Muro Oeste
    add_box("Muro_Oeste", 0.00, 0.00, 0.00, 0.20, L_Y, H_WALL)

    # Muro Sur
    add_box("Muro_Sur_1", 0.20, 0.00, 0.00, 0.80, 0.20, H_WALL)
    add_box("Muro_Sur_Dintel_Lav", 0.80, 0.00, H_DOOR, 1.80, 0.20, H_WALL)
    add_box("Muro_Sur_2", 1.80, 0.00, 0.00, 3.70, 0.20, H_WALL)
    add_box("Muro_Sur_Sill_Hab4", 3.70, 0.00, 0.00, 5.60, 0.20, W_SILL)
    add_box("Muro_Sur_Dintel_Hab4", 3.70, 0.00, W_SILL + W_H, 5.60, 0.20, H_WALL)
    add_box("Muro_Sur_3", 5.60, 0.00, 0.00, 7.00, 0.20, H_WALL)
    add_box("Muro_Sur_Sill_B2", 7.00, 0.00, 0.00, 7.90, 0.20, B_SILL)
    add_box("Muro_Sur_Dintel_B2", 7.00, 0.00, B_SILL + B_H, 7.90, 0.20, H_WALL)
    add_box("Muro_Sur_4", 7.90, 0.00, 0.00, 9.05, 0.20, H_WALL)

    # Muro Este
    x_e1, x_e2 = 9.05, 9.25
    add_box("Muro_Este_1", x_e1, 0.00, 0.00, x_e2, 0.50, H_WALL)
    add_box("Muro_Este_Sill_B2", x_e1, 0.50, 0.00, x_e2, 1.40, B_SILL)
    add_box("Muro_Este_Dintel_B2", x_e1, 0.50, B_SILL + B_H, x_e2, 1.40, H_WALL)
    add_box("Muro_Este_2", x_e1, 1.40, 0.00, x_e2, 2.60, H_WALL)
    add_box("Muro_Este_Sill_Hab3", x_e1, 2.60, 0.00, x_e2, 4.80, W_SILL)
    add_box("Muro_Este_Dintel_Hab3", x_e1, 2.60, W_SILL + W_H, x_e2, 4.80, H_WALL)
    add_box("Muro_Este_3", x_e1, 4.80, 0.00, x_e2, 6.20, H_WALL)
    add_box("Muro_Este_Sill_Hab2", x_e1, 6.20, 0.00, x_e2, 8.40, W_SILL)
    add_box("Muro_Este_Dintel_Hab2", x_e1, 6.20, W_SILL + W_H, x_e2, 8.40, H_WALL)
    add_box("Muro_Este_4", x_e1, 8.40, 0.00, x_e2, 9.70, H_WALL)
    add_box("Muro_Este_Sill_B1", x_e1, 9.70, 0.00, x_e2, 10.60, B_SILL)
    add_box("Muro_Este_Dintel_B1", x_e1, 9.70, B_SILL + B_H, x_e2, 10.60, H_WALL)
    add_box("Muro_Este_5", x_e1, 10.60, 0.00, x_e2, 12.00, H_WALL)
    add_box("Muro_Este_Sill_Hab1", x_e1, 12.00, 0.00, x_e2, 14.20, W_SILL)
    add_box("Muro_Este_Dintel_Hab1", x_e1, 12.00, W_SILL + W_H, x_e2, 14.20, H_WALL)
    add_box("Muro_Este_6", x_e1, 14.20, 0.00, x_e2, L_Y, H_WALL)

    # Muro Norte (Fachada)
    add_box("Viga_Porton", 0.20, 14.95, 2.50, 2.80, L_Y, H_WALL)
    add_box("Viga_Porche", 2.80, 14.95, 2.40, 5.90, L_Y, H_WALL)
    add_box("Muro_Norte_1", 5.90, 14.95, 0.00, 6.50, L_Y, H_WALL)
    add_box("Muro_Norte_Sill", 6.50, 14.95, 0.00, 8.70, L_Y, W_SILL)
    add_box("Muro_Norte_Dintel", 6.50, 14.95, W_SILL + W_H, 8.70, L_Y, H_WALL)
    add_box("Muro_Norte_2", 8.70, 14.95, 0.00, 9.05, L_Y, H_WALL)

    # 4. Muros Interiores
    x1_1, x2_1 = 2.80, 2.95
    add_box("Muro_Eje1_1", x1_1, 0.20, 0.00, x2_1, 3.20, H_WALL)
    add_box("Muro_Eje1_Dintel_Coc", x1_1, 3.20, H_DOOR, x2_1, 4.00, H_WALL)
    add_box("Muro_Eje1_2", x1_1, 4.00, 0.00, x2_1, 4.45, H_WALL)
    add_box("Muro_Eje1_3", x1_1, 7.40, 0.00, x2_1, 9.50, H_WALL)
    add_box("Muro_Eje1_Dintel_Gar", x1_1, 9.50, H_DOOR, x2_1, 10.40, H_WALL)
    add_box("Muro_Eje1_4", x1_1, 10.40, 0.00, x2_1, 12.90, H_WALL)

    x1_2, x2_2 = 5.90, 6.05
    add_box("Muro_Eje2_1", x1_2, 0.20, 0.00, x2_2, 1.00, H_WALL)
    add_box("Muro_Eje2_Dintel_B2", x1_2, 1.00, H_DOOR, x2_2, 1.70, H_WALL)
    add_box("Muro_Eje2_2", x1_2, 1.70, 0.00, x2_2, 4.30, H_WALL)
    add_box("Muro_Eje2_Dintel_Hab3", x1_2, 4.30, H_DOOR, x2_2, 5.00, H_WALL)
    add_box("Muro_Eje2_3", x1_2, 5.00, 0.00, x2_2, 8.10, H_WALL)
    add_box("Muro_Eje2_Dintel_Hab2", x1_2, 8.10, H_DOOR, x2_2, 8.80, H_WALL)
    add_box("Muro_Eje2_4", x1_2, 8.80, 0.00, x2_2, 9.80, H_WALL)
    add_box("Muro_Eje2_Dintel_B1", x1_2, 9.80, H_DOOR, x2_2, 10.50, H_WALL)
    add_box("Muro_Eje2_5", x1_2, 10.50, 0.00, x2_2, 11.50, H_WALL)
    add_box("Muro_Eje2_Dintel_Hab1", x1_2, 11.50, H_DOOR, x2_2, 12.20, H_WALL)
    add_box("Muro_Eje2_6", x1_2, 12.20, 0.00, x2_2, 14.95, H_WALL)

    add_box("Muro_Lav_Coc_1", 0.20, 1.70, 0.00, 0.50, 1.85, H_WALL)
    add_box("Muro_Lav_Coc_Dintel", 0.50, 1.70, H_DOOR, 1.30, 1.85, H_WALL)
    add_box("Muro_Lav_Coc_2", 1.30, 1.70, 0.00, 2.80, 1.85, H_WALL)

    add_box("Muro_Coc_Esc", 0.20, 4.30, 0.00, 2.80, 4.45, H_WALL)
    add_box("Muro_Esc_Gar", 0.20, 7.40, 0.00, 2.80, 7.55, H_WALL)

    add_box("Muro_Hab4_Com_1", 2.95, 3.55, 0.00, 3.50, 3.70, H_WALL)
    add_box("Muro_Hab4_Com_Dintel", 3.50, 3.55, H_DOOR, 4.20, 3.70, H_WALL)
    add_box("Muro_Hab4_Com_2", 4.20, 3.55, 0.00, 5.90, 3.70, H_WALL)

    add_box("Muro_B2_Hab3", 6.05, 1.95, 0.00, 9.05, 2.10, H_WALL)
    add_box("Muro_Hab3_Hab2", 6.05, 5.35, 0.00, 9.05, 5.50, H_WALL)
    add_box("Muro_Hab2_B1", 6.05, 9.10, 0.00, 9.05, 9.25, H_WALL)
    add_box("Muro_B1_Hab1", 6.05, 11.10, 0.00, 9.05, 11.25, H_WALL)

    add_box("Muro_Porche_Sala_1", 2.95, 12.90, 0.00, 3.20, 13.05, H_WALL)
    add_box("Muro_Porche_Sala_Dintel", 3.20, 12.90, H_DOOR, 4.15, 13.05, H_WALL)
    add_box("Muro_Porche_Sala_2", 4.15, 12.90, 0.00, 5.90, 13.05, H_WALL)

    # 5. Columnas
    cols = [
        (2.80, 14.90), (2.80, 12.90), (2.80, 10.40), (2.80, 7.40), (2.80, 4.30), (2.80, 0.20),
        (5.90, 14.90), (5.90, 12.90), (5.90, 9.10), (5.90, 5.35), (5.90, 3.55), (5.90, 0.20),
        (9.00, 14.90), (9.00, 11.10), (9.00, 9.10), (9.00, 5.35), (9.00, 1.95), (9.00, 0.20),
        (0.00, 14.90), (0.00, 7.40), (0.00, 0.20)
    ]
    for idx, (cx, cy) in enumerate(cols):
        add_box(f"Columna_{idx}", cx, cy, 0.00, cx + 0.25, cy + 0.25, H_WALL)

    # 6. Escribir formato OBJ
    obj_lines = ["# Casa Primer Piso 3D\n# Generado por Arquitecto Virtual\n\n"]
    vertices = []
    faces = []
    v_idx = 1

    for name, x1, y1, z1, x2, y2, z2 in boxes:
        # 8 vertices por caja
        box_v = [
            (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), # Inferior 0,1,2,3
            (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)  # Superior 4,5,6,7
        ]
        for vx, vy, vz in box_v:
            obj_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f}\n")

        # 6 caras (cada cara dividida en 2 triangulos o quads)
        # OBJ soporta quads directamente:
        b = v_idx
        obj_lines.append(f"o {name}\n")
        obj_lines.append(f"f {b} {b+3} {b+2} {b+1}\n")       # Inferior
        obj_lines.append(f"f {b+4} {b+5} {b+6} {b+7}\n")   # Superior
        obj_lines.append(f"f {b} {b+1} {b+5} {b+4}\n")       # Sur
        obj_lines.append(f"f {b+2} {b+3} {b+7} {b+6}\n")   # Norte
        obj_lines.append(f"f {b+3} {b} {b+4} {b+7}\n")       # Oeste
        obj_lines.append(f"f {b+1} {b+2} {b+6} {b+5}\n")   # Este

        v_idx += 8

    with open("casa_3d.obj", "w", encoding="utf-8") as f:
        f.writelines(obj_lines)
    print("casa_3d.obj generado con exito.")

    # 7. Escribir formato STL ASCII
    stl_lines = ["solid casa_primer_piso\n"]
    def write_tri(p1, p2, p3):
        # Normal aproximada
        stl_lines.append("  facet normal 0 0 0\n")
        stl_lines.append("    outer loop\n")
        stl_lines.append(f"      vertex {p1[0]:.4f} {p1[1]:.4f} {p1[2]:.4f}\n")
        stl_lines.append(f"      vertex {p2[0]:.4f} {p2[1]:.4f} {p2[2]:.4f}\n")
        stl_lines.append(f"      vertex {p3[0]:.4f} {p3[1]:.4f} {p3[2]:.4f}\n")
        stl_lines.append("    endloop\n")
        stl_lines.append("  endfacet\n")

    def write_quad(p1, p2, p3, p4):
        write_tri(p1, p2, p3)
        write_tri(p1, p3, p4)

    for name, x1, y1, z1, x2, y2, z2 in boxes:
        p0, p1 = (x1, y1, z1), (x2, y1, z1)
        p2, p3 = (x2, y2, z1), (x1, y2, z1)
        p4, p5 = (x1, y1, z2), (x2, y1, z2)
        p6, p7 = (x2, y2, z2), (x1, y2, z2)

        write_quad(p0, p3, p2, p1) # Inf
        write_quad(p4, p5, p6, p7) # Sup
        write_quad(p0, p1, p5, p4) # Sur
        write_quad(p2, p3, p7, p6) # Norte
        write_quad(p3, p0, p4, p7) # Oeste
        write_quad(p1, p2, p6, p5) # Este

    stl_lines.append("endsolid casa_primer_piso\n")

    with open("casa_3d.stl", "w", encoding="utf-8") as f:
        f.writelines(stl_lines)
    print("casa_3d.stl generado con exito.")

if __name__ == "__main__":
    create_3d_models()
