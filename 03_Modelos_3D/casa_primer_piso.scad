// ==============================================================================
// Modelo Parametrico 3D - Casa de Habitacion (Primer Piso / Nivel Calle)
// Generado por Arquitecto Virtual Gemini + CADCraft
// Ubicacion: Av. 4 entre calles 30 y 31, N 30-7, Municipio Independencia, Yaracuy
// ==============================================================================

// PASO 2: PARAMETROS GLOBALES
BUILDING_WIDTH_X = 9.25;
BUILDING_LENGTH_Y = 15.15;
WALL_HEIGHT = 2.80;
EXT_WALL_THICKNESS = 0.20;
INT_WALL_THICKNESS = 0.15;
SLAB_THICKNESS = 0.15;
DOOR_HEIGHT = 2.10;
WINDOW_SILL = 1.00;
WINDOW_HEIGHT = 1.10;
BATH_WINDOW_SILL = 1.80;
BATH_WINDOW_HEIGHT = 0.40;
PARAPET_HEIGHT = 0.45;
EPS = 0.04;

module box_from_coords(x1, y1, z1, x2, y2, z2) {
    translate([min(x1, x2), min(y1, y2), min(z1, z2)])
        cube([abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)]);
}

// 1. Losa de Piso con hueco de escalera
module floor_slab() {
    difference() {
        box_from_coords(0, 0, -SLAB_THICKNESS, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, 0);
        // Hueco de escalera que baja al sotano
        box_from_coords(0.20 - EPS, 4.45, -SLAB_THICKNESS - EPS, 1.45, 7.40, 0 + EPS);
    }
}

// 2. Muros Solidos (sin vanos)
module raw_walls() {
    // Muros Exteriores
    box_from_coords(0.00, 0.00, 0, 0.20, BUILDING_LENGTH_Y, WALL_HEIGHT);
    box_from_coords(0.00, 0.00, 0, BUILDING_WIDTH_X, 0.20, WALL_HEIGHT);
    box_from_coords(BUILDING_WIDTH_X - EXT_WALL_THICKNESS, 0.00, 0, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT);
    box_from_coords(5.90, BUILDING_LENGTH_Y - EXT_WALL_THICKNESS, 0, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT);

    // Muros Longitudinales Interiores
    box_from_coords(2.80, 0.20, 0, 2.95, 12.90, WALL_HEIGHT);
    box_from_coords(5.90, 3.55, 0, 6.05, 14.95, WALL_HEIGHT);

    // Muros Transversales Interiores
    box_from_coords(0.20, 1.70, 0, 2.80, 1.85, WALL_HEIGHT); // Lavadero - Cocina
    box_from_coords(0.20, 4.30, 0, 2.80, 4.45, WALL_HEIGHT); // Cocina - Escalera
    box_from_coords(0.20, 7.40, 0, 2.80, 7.55, WALL_HEIGHT); // Escalera - Garaje
    box_from_coords(2.95, 3.55, 0, 5.90, 3.70, WALL_HEIGHT); // Hab 4 - Comedor
    box_from_coords(6.05, 1.95, 0, 9.05, 2.10, WALL_HEIGHT); // Bano 2 - Hab 3
    box_from_coords(6.05, 5.35, 0, 9.05, 5.50, WALL_HEIGHT); // Hab 3 - Hab 2
    box_from_coords(6.05, 9.10, 0, 9.05, 9.25, WALL_HEIGHT); // Hab 2 - Bano 1
    box_from_coords(6.05, 11.10, 0, 9.05, 11.25, WALL_HEIGHT); // Bano 1 - Hab 1
    box_from_coords(2.95, 12.90, 0, 5.90, 13.05, WALL_HEIGHT); // Porche - Sala
}

// 3. Vanos (Cortes Booleanos)
module openings() {
    // Puertas
    box_from_coords(3.20, 12.90 - EPS, 0, 4.15, 13.05 + EPS, DOOR_HEIGHT); // Principal
    box_from_coords(2.80 - EPS, 9.50, 0, 2.95 + EPS, 10.40, DOOR_HEIGHT); // Garaje - Sala
    box_from_coords(2.80 - EPS, 3.20, 0, 2.95 + EPS, 4.00, DOOR_HEIGHT); // Cocina
    box_from_coords(0.50, 1.70 - EPS, 0, 1.30, 1.85 + EPS, DOOR_HEIGHT); // Lavadero Int
    box_from_coords(0.80, 0.00 - EPS, 0, 1.80, 0.20 + EPS, DOOR_HEIGHT); // Lavadero Ext
    box_from_coords(5.90 - EPS, 11.50, 0, 6.05 + EPS, 12.20, DOOR_HEIGHT); // Hab 1
    box_from_coords(5.90 - EPS, 9.80, 0, 6.05 + EPS, 10.50, DOOR_HEIGHT); // Bano 1
    box_from_coords(5.90 - EPS, 8.10, 0, 6.05 + EPS, 8.80, DOOR_HEIGHT); // Hab 2
    box_from_coords(5.90 - EPS, 4.30, 0, 6.05 + EPS, 5.00, DOOR_HEIGHT); // Hab 3
    box_from_coords(5.90 - EPS, 1.00, 0, 6.05 + EPS, 1.70, DOOR_HEIGHT); // Bano 2
    box_from_coords(3.50, 3.55 - EPS, 0, 4.20, 3.70 + EPS, DOOR_HEIGHT); // Hab 4
    box_from_coords(0.20, 15.15 - EXT_WALL_THICKNESS - EPS, 0, 2.80, 15.15 + EPS, 2.50); // Porton Garaje

    // Ventanas
    box_from_coords(6.50, 14.95 - EPS, WINDOW_SILL, 8.70, 15.15 + EPS, WINDOW_SILL + WINDOW_HEIGHT); // Hab 1 Frontal
    box_from_coords(9.05 - EPS, 12.00, WINDOW_SILL, 9.25 + EPS, 14.20, WINDOW_SILL + WINDOW_HEIGHT); // Hab 1 Lateral
    box_from_coords(9.05 - EPS, 9.70, BATH_WINDOW_SILL, 9.25 + EPS, 10.60, BATH_WINDOW_SILL + BATH_WINDOW_HEIGHT); // B1 Lateral
    box_from_coords(9.05 - EPS, 6.20, WINDOW_SILL, 9.25 + EPS, 8.40, WINDOW_SILL + WINDOW_HEIGHT); // Hab 2 Lateral
    box_from_coords(9.05 - EPS, 2.60, WINDOW_SILL, 9.25 + EPS, 4.80, WINDOW_SILL + WINDOW_HEIGHT); // Hab 3 Lateral
    box_from_coords(9.05 - EPS, 0.50, BATH_WINDOW_SILL, 9.25 + EPS, 1.40, BATH_WINDOW_SILL + BATH_WINDOW_HEIGHT); // B2 Lateral
    box_from_coords(3.70, 0.00 - EPS, WINDOW_SILL, 5.60, 0.20 + EPS, WINDOW_SILL + WINDOW_HEIGHT); // Hab 4 Posterior
}

module finished_walls() {
    difference() {
        raw_walls();
        openings();
    }
}

// 4. Cubierta y Parapeto
module roof_structure() {
    // Losa de techo
    box_from_coords(0, 0, WALL_HEIGHT, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT + SLAB_THICKNESS);

    // Parapeto perimetral
    difference() {
        box_from_coords(0, 0, WALL_HEIGHT + SLAB_THICKNESS, BUILDING_WIDTH_X, BUILDING_LENGTH_Y, WALL_HEIGHT + SLAB_THICKNESS + PARAPET_HEIGHT);
        box_from_coords(EXT_WALL_THICKNESS, EXT_WALL_THICKNESS, WALL_HEIGHT + SLAB_THICKNESS - EPS, BUILDING_WIDTH_X - EXT_WALL_THICKNESS, BUILDING_LENGTH_Y - EXT_WALL_THICKNESS, WALL_HEIGHT + SLAB_THICKNESS + PARAPET_HEIGHT + EPS);
    }
}

// 5. Ensamblaje Final
color([0.75, 0.75, 0.75]) floor_slab();
color([0.95, 0.95, 0.95]) finished_walls();
color([0.65, 0.65, 0.70]) roof_structure();
