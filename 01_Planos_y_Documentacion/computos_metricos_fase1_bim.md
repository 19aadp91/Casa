# Cómputos Métricos y Cantidades de Materiales BIM — Fase 1 (Sótano, Rampa y Piso 1 Completo)

- **Modelo Nativo FreeCAD 1.1.4:** `03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.FCStd`
- **Modelo Estándar Abierto OpenBIM (`IFC4`):** `03_Modelos_3D/BIM_FreeCAD/casa_fase1_sotano_piso1.ifc`
- **Tabla Detallada para Excel:** `01_Planos_y_Documentacion/computos_metricos_fase1_bim.csv`
- **Auditoría de Lindero Vecino Oeste:** `minX = 0.1500 m` (`0,00 m` invasión; pared vecina excluida de todos los cómputos).
- **Total de Objetos Constructivos Cuantificados:** `135` sólidos BIM verificados (con sustracción booleana exacta de columnas y vanos).

---

## 1. Resumen Ejecutivo de Compra de Materiales e Insumos (Incluye 5% de Desperdicio)

| Insumo / Material Comercial | Unidad | Cantidad Estimada | Uso Principal en Obra |
| :--- | :---: | ---: | :--- |
| **Concreto Estructural `f'c = 280 kg/cm²`** (Infraestructura) | `m³` | **37.63** | Zapatas (12), losa sótano, patio maniobra, rampa 18%, muros contención, 12 cols `35×35` y Escalera T1 |
| **Concreto Estructural `f'c = 250 kg/cm²`** (Piso 1 base sin techo) | `m³` | **35.70** | Losa entrepiso P.B. (`192,15 m²` netos), 32 columnas `25×25 cm` y Escalera T2 |
| **Concreto Estructural `f'c = 250 kg/cm²`** (Vigas + Placa Techo P1) | `m³` | **39.56** | Vigas sísmicas corona Piso 1 (`25×30 cm`) + Placa superior `Z = +2,85..+3,00 m` |
| **TOTAL CONCRETO ARMADO FASE 1 COMPLETA** | `m³` | **112.90** | Infraestructura + Piso 1 completamente techado |
| **Cemento Gris Portland (`Sacos 42,5 kg`)** | `sacos` | **1172** | `980` sacos para concretos (si se vacía en sitio) + `192` sacos para morteros/frisos |
| **Arena Lavada + Arena Cernida** | `m³` | **69.4** | Mezclas de concreto, pega de bloques y frisos |
| **Piedra Picada `#1`** | `m³` | **81.3** | Concretos estructurales de sótano, rampa y planta baja |
| **Acero de Refuerzo (Cabillas corrugadas + Malla)** | `kg` | **9,781** | Cuantía sismorresistente en columnas, vigas, zapatas, losas, rampa y escaleras |
| **Bloques de Concreto Pesado `e = 20 cm`** | `und` | **223** | `16.94 m²` netos en Muro Este Sótano y pórtico de carga Av. 4 |
| **Bloques de Arcilla / Concreto `e = 15 cm`** | `und` | **4,184** | `318.73 m²` netos en fachadas P.B., divisorio garaje, esclusas, cercas y muros sótano |
| **Bloques de Tabiquería `e = 10 cm`** | `und` | **127** | `9.67 m²` netos en divisiones internas de cabinas sanitarias Damas/Caballeros |
| **Friso y Encamisado de Muros (Ambas Caras Netas)** | `m²` | **690.68** | Descontados al 100% todos los vanos de puertas, ventanas, portones y santamarías |
| **Manto / Impermeabilización Hidrófuga Sótano** | `m²` | **113.10** | Losa de fundación bodega (`74,70 m²`) + muros de contención contra terreno |
| **Piedra Laja Rústica Natural** | `m²` | **39.41** | Machones frontales Av. 4, zócalo fachada Este y zócalo interior de garaje |
| **Porcelanato Comercial Antideslizante Alto Tráfico** | `m²` | **123.58** | Salón Frutería ampliado (`~112 m²`), Barra de Jugos y Oficina Acristalada |
| **Pavimento Vehicular Endurecido (Garaje)** | `m²` | **41.02** | Estacionamiento cubierto de 2 vehículos + vestíbulo residencial |
| **Cerámica Impermeable (Pisos + Paredes Baños)** | `m²` | **31.39** | Núcleo de Baños Suroeste P.B. y Baño Operativo del Sótano |

---

## 2. Cómputos Métricos Consolidados por Partida Constructiva

| Código | Capítulo | Nivel | Especificación / Partida | Elem. | Unid. | Cantidad Neta | Área (`m²`) | Volumen (`m³`) |
| :---: | :--- | :--- | :--- | :---: | :---: | ---: | ---: | ---: |
| `01.01` | 01_MOVIMIENTO_TIERRAS | Sitio / Sotano | Excavacion Mecanica en Corte (Sotano, Patio y Rampa) | 1 | `m3` | **320.18** | 111.73 | 320.182 |
| `02.01` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Zapatas Aisladas de Fundacion Sotano (f'c=280 kg/cm2) | 1 | `m3` | **4.99** | 14.52 | 4.989 |
| `02.02` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Losa de Fundacion Gran Bodega Sotano e=15cm (f'c=280) | 1 | `m3` | **11.21** | 74.70 | 11.205 |
| `02.03` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Losa Pavimento Armado Patio de Maniobra Sur (f'c=280) | 1 | `m3` | **1.28** | 11.62 | 1.279 |
| `02.04` | 02_INFRAESTRUCTURA_CONCRETO | Sitio / Rampa Este | Rampa Logistica Continua 18% y Corredor Este e=20cm | 1 | `m3` | **7.98** | 39.91 | 7.982 |
| `02.05` | 02_INFRAESTRUCTURA_CONCRETO | Sitio / Rampa Este | Muro Contencion Lateral Bajo P.B. Junto a Rampa | 1 | `m3` | **2.31** | 15.40 | 2.310 |
| `02.06` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Columnas Estructurales Sotano 35x35cm (12 apoyos, f'c=280) | 12 | `m3` | **3.40** | 1.42 | 3.396 |
| `02.07` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Muros de Contencion Perimetrales Sotano (Oeste y Norte) | 2 | `m2` | **38.40** | 38.40 | 5.760 |
| `02.08` | 02_INFRAESTRUCTURA_CONCRETO | Nivel 00 - Sotano | Escalera Concreto Armado Tramo 1: Sotano -> P.B. (12 peld.) | 1 | `m3` | **0.71** | 3.25 | 0.712 |
| `03.01` | 03_SUPERESTRUCTURA_PISO_1 | Nivel 01 - Planta Baja | Losa Estructural de Entrepiso Planta Baja e=15cm (f'c=250) | 1 | `m3` | **28.82** | 192.15 | 28.822 |
| `03.02` | 03_SUPERESTRUCTURA_PISO_1 | Nivel 01 - Planta Baja | Columnas Concreto Armado P.B. 25x25cm (32 nodos, f'c=250) | 32 | `m3` | **5.70** | 2.00 | 5.700 |
| `03.03` | 03_SUPERESTRUCTURA_PISO_1 | Nivel 01 - Planta Baja | Escalera Concreto Armado Tramo 2: P.B. -> Piso 2 (14 peld.) | 1 | `m3` | **1.18** | 3.25 | 1.177 |
| `03.04` | 03_SUPERESTRUCTURA_PISO_1 | Cierre Techo Piso 1 (+2,85m) | Vigas Sismicas y de Carga Corona Piso 1 (25x30cm Netas) | 1 | `m3` | **10.74** | 35.81 | 10.743 |
| `03.05` | 03_SUPERESTRUCTURA_PISO_1 | Cierre Techo Piso 1 (+2,85m) | Placa Estructural de Techo / Entrepiso sobre Piso 1 (e=15cm) | 1 | `m3` | **28.82** | 192.15 | 28.822 |
| `04.01` | 04_ALBANILERIA_Y_ACABADOS | Sitio / Linderos | Cerramiento Perimetral Sur y Este en Bloque e=15cm (H=2,20m) | 1 | `m2` | **77.48** | 77.48 | 11.622 |
| `04.02` | 04_ALBANILERIA_Y_ACABADOS | Nivel 00 - Sotano | Muros Exteriores y Divisorios en Bloque e=15cm (Netos sin vanos) | 3 | `m2` | **36.11** | 36.11 | 5.417 |
| `04.02` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Muros Exteriores y Divisorios en Bloque e=15cm (Netos sin vanos) | 7 | `m2` | **205.14** | 205.14 | 30.771 |
| `04.03` | 04_ALBANILERIA_Y_ACABADOS | Nivel 00 - Sotano | Mamposteria Estructural Pesada en Bloque Concreto e=20cm | 1 | `m2` | **15.01** | 15.01 | 3.002 |
| `04.03` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Mamposteria Estructural Pesada en Bloque Concreto e=20cm | 1 | `m2` | **1.94** | 1.94 | 0.387 |
| `04.04` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Tabiqueria Divisoria Interna en Bloque e=10cm (Cabinas Banos) | 1 | `m2` | **9.67** | 9.67 | 0.967 |
| `04.05` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Revestimiento de Piedra Laja Rustica en Machones y Zocalos | 1 | `m2` | **39.41** | 39.41 | 3.286 |
| `04.06` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Piso Porcelanato Antideslizante Alto Trafico Comercial | 1 | `m2` | **123.58** | 123.58 | 1.854 |
| `04.07` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Pavimento Vehicular Endurecido en Garaje y Vestibulo | 1 | `m2` | **41.02** | 41.02 | 0.615 |
| `04.08` | 04_ALBANILERIA_Y_ACABADOS | Nivel 01 - Planta Baja | Piso Ceramico Antideslizante Impermeable en Banos | 1 | `m2` | **12.05** | 12.05 | 0.123 |
| `05.01` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 01 - Planta Baja | Porton Vehicular Corredizo-Articulado Riel Curvo 90° (2,30x2,40m) | 1 | `und` | **1.00** | 5.52 | 0.751 |
| `05.02` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 01 - Planta Baja | Santamarias Enrollables de Caracol Comerciales Av. 4 (2 und) | 2 | `und` | **2.00** | 11.28 | 0.552 |
| `05.03` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 01 - Planta Baja | Porton Metalico Doble Acceso Exclusivo Bodega Av. 4 (1,77x2,34m) | 1 | `und` | **1.00** | 4.14 | 0.323 |
| `05.04` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 00 - Sotano | Porton Doble Metalico Reforzado Carga Sotano (2,20x2,10m) | 1 | `und` | **1.00** | 4.62 | 0.416 |
| `05.05` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 00 - Sotano | Ventanas Altas Basculantes en Hierro con Reja Seguridad Sotano | 6 | `und` | **6.00** | 4.29 | 0.288 |
| `05.06` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 00 - Sotano | Puertas Metalicas Entamboradas de Seguridad (Esclusa Sotano/PB) | 1 | `und` | **1.00** | 1.74 | 0.154 |
| `05.06` | 05_HERRERIA_Y_CERRAMIENTOS | Nivel 01 - Planta Baja | Puertas Metalicas Entamboradas de Seguridad (Esclusa Sotano/PB) | 1 | `und` | **1.00** | 1.93 | 0.134 |
| `06.01` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 00 - Sotano | Puertas Batientes de Madera Maciza / Entamborada con Marco | 1 | `und` | **1.00** | 1.60 | 0.070 |
| `06.01` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 01 - Planta Baja | Puertas Batientes de Madera Maciza / Entamborada con Marco | 5 | `und` | **5.00** | 8.36 | 0.405 |
| `06.02` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 01 - Planta Baja | Ventanas y Ventanales Rusticos de Madera y Cristal en P.B. | 10 | `und` | **10.00** | 18.25 | 1.109 |
| `06.03` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 01 - Planta Baja | Cerramiento Industrial Hierro Negro, Madera y Cristal Oficina | 1 | `m2` | **16.79** | 16.79 | 1.165 |
| `06.04` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 01 - Planta Baja | Puerta Batiente de Cristal Templado 10mm Oficina Admin. | 1 | `und` | **1.00** | 1.88 | 0.102 |
| `06.05` | 06_CARPINTERIA_MADERA_VIDRIO | Nivel 01 - Planta Baja | Vigas Decorativas de Techo y Forrado Hueco de 5 Columnas Madera | 1 | `m3` | **3.54** | 70.79 | 3.539 |
| `07.01` | 07_INSTALACIONES_SANITARIAS | Nivel 00 - Sotano | Inodoros (WC) de Porcelana Vitrificada (Sotano + Damas + Cab.) | 1 | `und` | **1.00** | 0.30 | 0.141 |
| `07.01` | 07_INSTALACIONES_SANITARIAS | Nivel 01 - Planta Baja | Inodoros (WC) de Porcelana Vitrificada (Sotano + Damas + Cab.) | 2 | `und` | **2.00** | 0.56 | 0.293 |
| `07.02` | 07_INSTALACIONES_SANITARIAS | Nivel 00 - Sotano | Lavamanos con Griferia (Bano Sotano + Doble Antebano P.B.) | 1 | `und` | **1.00** | 0.30 | 0.090 |
| `07.02` | 07_INSTALACIONES_SANITARIAS | Nivel 01 - Planta Baja | Lavamanos con Griferia (Bano Sotano + Doble Antebano P.B.) | 2 | `und` | **2.00** | 0.56 | 0.022 |
| `07.03` | 07_INSTALACIONES_SANITARIAS | Nivel 01 - Planta Baja | Urinario Mural Ecologico en Cabina Caballeros P.B. | 1 | `und` | **1.00** | 0.28 | 0.067 |
| `07.04` | 07_INSTALACIONES_SANITARIAS | Nivel 00 - Sotano | Batea / Poceta Lava-Mopas en Cuarto Sanitario Sotano | 1 | `und` | **1.00** | 0.30 | 0.149 |
| `07.05` | 07_INSTALACIONES_SANITARIAS | Nivel 01 - Planta Baja | Fregadero Industrial Doble Tina Acero Inox en Barra de Jugos | 1 | `und` | **1.00** | 0.35 | 0.028 |
| `07.06` | 07_INSTALACIONES_SANITARIAS | Nivel 01 - Planta Baja | Mueble Tocador Doble para Lavamanos en Antebano Suroeste | 1 | `und` | **1.00** | 0.49 | 0.414 |
| `08.01` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 00 - Sotano | Paneleria Frigorifica Isotermica PIR e=12cm Camara Pre-Frio | 1 | `m2` | **22.87** | 22.87 | 2.449 |
| `08.02` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 00 - Sotano | Puerta Corrediza Inox Camara Pre-Frio + Control Digital + Racks | 1 | `und` | **1.00** | 2.36 | 2.376 |
| `08.03` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 00 - Sotano | Baterias de Racks Industriales Pesados en Bodega Mayorista | 5 | `und` | **5.00** | 8.46 | 1.969 |
| `08.04` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 00 - Sotano | Bascula Industrial Plataforma 500 kg + Mesa Control Guias | 1 | `und` | **1.00** | 0.81 | 1.044 |
| `08.05` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Islas Centrales Piramidales de Exhibicion Fruteria (Base Piedra) | 5 | `und` | **5.00** | 11.05 | 8.170 |
| `08.06` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Estanterias Murales Escalonadas de Madera en Salon Comercial | 1 | `ml` | **24.35** | 15.20 | 4.579 |
| `08.07` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Mural Frigorifico Vertical Abierto Lacteos y Fruta Picada (2,45m) | 1 | `und` | **1.00** | 1.76 | 4.008 |
| `08.08` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Mostrador Principal en 'L' de Caja y Pesaje (Piedra + Madera) | 1 | `und` | **1.00** | 2.95 | 2.007 |
| `08.09` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Barra Gourmet de Jugos y Cafe Sur + Vitrina Fria + 4 Taburetes | 1 | `und` | **1.00** | 3.85 | 3.660 |
| `08.10` | 08_EQUIPAMIENTO_COMERCIAL_FRIO | Nivel 01 - Planta Baja | Mobiliario Completo Oficina Administracion (Escritorio L + Sillas) | 1 | `und` | **1.00** | 2.60 | 2.178 |

---

## 3. Cuadro Detallado de Portones, Santamarías, Puertas, Ventanas y Cerramientos

| Nivel | Código | Elemento BIM | Clase IFC | Área Vano (`m²`) | Material Principal |
| :--- | :---: | :--- | :---: | ---: | :--- |
| Nivel 00 - Sotano | `05.04` | Porton Doble Metalico Reforzado Carga Bodega (2,20x2,10m) | `Door` | 4.62 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Celosia Alta Bano Sot (1.05x0.50m con Reja) | `Window` | 0.53 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Ventana Alta Este Sot 1 (1.65x0.55m con Reja) | `Window` | 0.91 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Ventana Alta Este Sot 2 (1.65x0.55m con Reja) | `Window` | 0.91 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Ventana Alta Este Sot 3 (1.05x0.55m con Reja) | `Window` | 0.58 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Ventana Alta Sur Sot 1 (1.60x0.55m con Reja) | `Window` | 0.88 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.05` | Ventana Alta Sur Sot 2 (0.90x0.55m con Reja) | `Window` | 0.50 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `05.06` | Puerta Metalica Seguridad Esclusa Escalera Sotano (0,85x2,05m) | `Door` | 1.74 | Acero Estructural y Herreria Forja Negra |
| Nivel 00 - Sotano | `06.01` | Puerta Bano Operativo Personal Sotano (0,78x2,05m) | `Door` | 1.60 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `05.01` | Porton Vehicular Corredizo-Articulado Riel Curvo 90° (2,30x2,40m) | `Door` | 5.52 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `05.02` | Santamaria Enrollable de Caracol 1 Av. 4 (2.10x2,40m) | `Door` | 5.04 | Acero Estructural y Herreria Forja Negra |
| Nivel 01 - Planta Baja | `05.02` | Santamaria Enrollable de Caracol 2 Av. 4 (2.60x2,40m) | `Door` | 6.24 | Acero Estructural y Herreria Forja Negra |
| Nivel 01 - Planta Baja | `05.03` | Porton Metalico Doble Acceso Rampa Bodega Av. 4 (1,77x2,34m) | `Door` | 4.14 | Acero Estructural y Herreria Forja Negra |
| Nivel 01 - Planta Baja | `05.06` | Puerta Metalica Seguridad Arranque Escalera a Sotano (0,92x2,10m) | `Door` | 1.93 | Acero Estructural y Herreria Forja Negra |
| Nivel 01 - Planta Baja | `06.01` | Puerta Acceso Antebano Clientes/Personal Suroeste (0,85x2,10m) | `Door` | 1.78 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.01` | Puerta Cabina Sanitaria Caballeros (0,73x2,10m) | `Door` | 1.53 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.01` | Puerta Cabina Sanitaria Damas / PMR (0,80x2,10m) | `Door` | 1.68 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.01` | Puerta Cuarto de Aseo Diario Bajo Escalera (0,70x1,95m) | `Door` | 1.36 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.01` | Puerta Principal Residencial Garaje <-> Escalera P2 (0,95x2,10m) | `Door` | 1.99 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 1 Oficina (1.40x1.10m) | `Window` | 1.54 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 2 Pasillo (0.90x0.90m) | `Window` | 0.81 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 3 Mural (1.70x1.10m) | `Window` | 1.87 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 4 Salon (2.20x1.10m) | `Window` | 2.42 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 5 Salon (0.90x0.90m) | `Window` | 0.81 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 6 Salon (2.20x1.10m) | `Window` | 2.42 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Este PB 7 Caja (2.20x1.10m) | `Window` | 2.42 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventana Sur PB 1 BanosSW (1.60x0.70m) | `Window` | 1.12 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventanal Sur PB 2 Jugos (2.10x1.35m) | `Window` | 2.84 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.02` | Ventanal Sur PB 3 Oficina (1.60x1.25m) | `Window` | 2.00 | Madera Maciza Tratada (Roble/Pardillo) |
| Nivel 01 - Planta Baja | `06.03` | Tabique Industrial Hierro Negro, Zocalo Madera y Cristal Oficina | `Curtain Wall` | 16.79 | Cristal Templado Transparente 8-10 mm |
| Nivel 01 - Planta Baja | `06.04` | Puerta Batiente Cristal Templado 10mm Oficina Admin (0,87x2,16m) | `Door` | 1.88 | Cristal Templado Transparente 8-10 mm |

---

## 4. Inventario de Piezas Sanitarias y Equipamiento Comercial / Cadena de Frío

| Nivel | Código | Equipo / Aparato Sanitario | Unidad | Cantidad |
| :--- | :---: | :--- | :---: | ---: |
| Nivel 00 - Sotano | `07.01` | Inodoro (WC) Bano Operativo Sotano | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.01` | Inodoro (WC) Cabina Caballeros P.B. | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.01` | Inodoro (WC) Elongado Cabina Damas / PMR P.B. | `und` | **1.00** |
| Nivel 00 - Sotano | `07.02` | Lavamanos Mural Bano Operativo Sotano | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.02` | Lavamanos Sobre-Tope 1 Antebano Suroeste | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.02` | Lavamanos Sobre-Tope 2 Antebano Suroeste | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.03` | Urinario Mural Ecologico Cabina Caballeros P.B. | `und` | **1.00** |
| Nivel 00 - Sotano | `07.04` | Batea / Poceta Lava-Mopas Aseo Sotano | `und` | **1.00** |
| Nivel 01 - Planta Baja | `07.05` | Fregadero Industrial Doble Tina Acero Inox en Barra de Jugos | `und` | **1.00** |
| Nivel 00 - Sotano | `08.01` | Paneleria Isotermica PIR e=12cm Camara Pre-Frio (10,07 m2) | `m2` | **22.87** |
| Nivel 00 - Sotano | `08.02` | Puerta Corrediza Frigorifica Inox (1,15x2,05m) + Tablero y Estantes | `und` | **1.00** |
| Nivel 00 - Sotano | `08.03` | Rack Industrial Mural Este 1 (0,65x2,75x1,58m) | `und` | **1.00** |
| Nivel 00 - Sotano | `08.03` | Rack Industrial Mural Este 2 (0,65x2,50x1,58m) | `und` | **1.00** |
| Nivel 00 - Sotano | `08.03` | Rack Industrial Oeste Suroeste (0,65x2,20x2,20m) | `und` | **1.00** |
| Nivel 00 - Sotano | `08.03` | Rack Industrial Pesado Norte (3,00x0,70x2,20m) | `und` | **1.00** |
| Nivel 00 - Sotano | `08.03` | Rack Industrial Sur Suroeste (2,30x0,66x1,58m) | `und` | **1.00** |
| Nivel 00 - Sotano | `08.04` | Bascula Industrial Plataforma 500 kg + Mesa Control Guias | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.05` | Isla Central Piramidal Fruteria 1 (Base Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.05` | Isla Central Piramidal Fruteria 2 (Base Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.05` | Isla Central Piramidal Fruteria 3 (Base Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.05` | Isla Central Piramidal Fruteria 4 (Base Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.05` | Isla Central Piramidal Fruteria 5 (Base Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.06` | Bateria de Estanterias Murales Oeste y Este en Madera Roble | `ml` | **24.35** |
| Nivel 01 - Planta Baja | `08.07` | Mural Frigorifico Vertical Abierto Lacteos y Fruta Picada (2,45m) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.08` | Mostrador Principal en 'L' de Caja y Pesaje (Piedra + Madera) | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.09` | Barra Gourmet Jugos y Cafe Sur + Vitrina Fria + Contra-Barra + 4 Bancos | `und` | **1.00** |
| Nivel 01 - Planta Baja | `08.10` | Juego Mobiliario Oficina Admin (Escritorio en L, Credenza y 3 Sillas) | `und` | **1.00** |
