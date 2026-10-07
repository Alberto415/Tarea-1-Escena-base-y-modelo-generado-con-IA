# Ficha técnica: mensajero SKYLINE

Autor de entrega: Alberto. Fecha: 2026-10-06 (America/Mexico_City).
Procedencia: recurso original de práctica creado con asistencia de Codex,
generador Python tools/build_parkour.py y primitivas nativas Godot 4.7.2.
Licencia del arte original: CC0 1.0. No generado con Tripo/Meshy.

| Dato | Resultado medido |
|---|---|
| Recurso final | scenes/courier_visual.tscn |
| Formato | escena nativa Godot, no glTF importado |
| MeshInstance3D | 30 |
| Triángulos indexados, sumados por instancia | 23,112 |
| Vértices, sumados por instancia | 13,516 |
| Materiales únicos | 5 |
| Texturas externas | 0 |
| Superficies con UV nativas | 30 |
| Huesos, skinning, clips esqueléticos | 0 |
| AABB en reposo: ancho × alto × fondo | 0.998 × 1.867 × 0.973 m |
| Límite mínimo Y | 0.0275 m |
| Escala de la escena envolvente | 1, 1, 1 |
| Ejes | +Y arriba; frente -Z; 1 unidad = 1 m |
| Cápsula física | altura 1.8 m; radio 0.42 m |

La envolvente incluye casco, mochila y bufanda. Las poses animadas pueden ampliar
ese volumen. El casco y accesorios exceden la cápsula; no colisionan por separado.
Las escalas locales de primitivas describen su forma y se conservaron.

Materiales PBR: traje marfil, piezas azul oscuro, naranja, luz cian y visor oscuro.
Rugosidad entre 0.18 y 0.55; metalicidad entre 0.05 y 0.7. Emisión en el material cian.
No existen imágenes a resolver. Las primitivas sí generan UV aunque no se usen texturas.

Verificación de normales: todos los vectores son finitos y de longitud unitaria
dentro de tolerancia 0.01. El contador detectó 928 triángulos de área
casi nula (producto cruzado al cuadrado < 1e-12), incluidos en el total, en las
primitivas teseladas. Se registra el hallazgo; no se afirma una malla optimizada,
soldada o lista para deformación. No se corrigió topología en esta entrega.

Animación: rotación de pivotes de brazos y piernas, inclinación del torso y bufanda
por courier_visual.gd. No mueve CharacterBody3D ni su cápsula. Preparación de rig,
pesos y revisión de topología para deformación quedan para Tarea 2.

Reproducción de la auditoría (requiere render para medir FPS reales):
`godot --path . --script tests/skyline_audit.gd -- --test`

Evidencia: output/evidence/skyline_audit.json.
SHA256 de courier_visual.tscn: f4aca2e36d9d668677f32bd06d0dd6701b9a5e75f2048c7974ea9c284336203d
