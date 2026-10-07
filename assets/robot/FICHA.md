# Ficha técnica | Robot de práctica

- Autor de entrega: Alberto. Recurso original creado con asistencia de Codex y Python.
- Fecha: 2026-09-26. Licencia: CC0 1.0; archivo LICENSE.txt.
- Formato: glTF 2.0, buffer embebido; sin dependencias de red.
- 11 piezas rígidas; 132 triángulos visibles instanciados, 264 vértices instanciados.
  Tres recursos mesh comparten el accessor de una caja de 12 triángulos.
- 3 materiales PBR: cerámica menta, juntas grafito y visor ámbar.
- 0 texturas, 0 UV, 0 esqueletos, 0 clips; normales planas explícitas.
- Tamaño: 1.03 m ancho × 1.78 m alto × 0.465 m fondo; 1 unidad = 1 metro.
- Origen: pies en Y=0; +Y arriba, frente -Z; escala de envolvente 1,1,1.
  Las escalas locales positivas de las cajas describen dimensiones, no errores de importación.
- Colisión independiente: cápsula de radio 0.42 m y altura 1.8 m.
  Los brazos sobresalen ligeramente de la cápsula; no tienen colisión individual.
- Articulaciones: piezas rígidas separadas; todavía no hay rig ni skinning.
- Normales exteriores verificadas: True; escalas positivas: True.
- Procedencia: tools/build_assets.py; no generado por Tripo/Meshy.
- Variante gris conservada para comparación, misma geometría.
- SHA256 final: 917dd0caefd952f6955994da0bd88354b18f2db9bdbf92c65d6c615e3c84cd3a
