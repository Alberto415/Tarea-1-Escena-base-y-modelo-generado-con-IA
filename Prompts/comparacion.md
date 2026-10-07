# Antes / después: comparación de variante

| Característica | A: gris | B: menta (final) |
|---|---|---|
| Archivo | robot_variante_gris.gltf | robot_practica.gltf |
| Cerámica, RGB lineal | 0.72 / 0.75 / 0.78 | 0.12 / 0.72 / 0.62 |
| Triángulos instanciados | 132 | 132 |
| Materiales / texturas | 3 / 0 | 3 / 0 |
| Dimensiones | 1.03 × 1.78 × 0.465 m | iguales |
| Decisión | alternativa neutral | seleccionada para reconocimiento visual |

No es una reparación de topología; es una comparación de color. La escena
`scenes/model_comparison.tscn` permite inspeccionar ambas variantes en 3D.

Tres verificaciones sin inventar defectos:
1. Malla: 11 piezas, caras no degeneradas, normales exteriores: True.
   Las piezas se intersectan por diseño de robot rígido; no es una piel continua.
2. Escala: pies en Y=0, altura 1.78 m, envolvente a escala 1; cápsula de 1.8 m.
3. Materiales y articulaciones: tres PBR integrados, cero imágenes externas;
   brazos y piernas separados, sin huesos/pesos. Rig y deformación pendientes de
   Tarea 2. La oscilación global actual es solo indicación visual de Walk.

Auditoría reproducible: `output/evidence/model_audit.json`.
