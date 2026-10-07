# Antes / después

| Elemento | Kinetic Lab | SKYLINE |
|---|---|---|
| Personaje | robot de cajas, glTF | mensajero, escena nativa .tscn |
| Piezas | 11 | 30 |
| Triángulos instanciados | 132 | 23,112 |
| Materiales / texturas | 3 / 0 | 5 / 0 |
| Apariencia | menta, grafito, ámbar | marfil, azul, naranja, cian, visor |
| Animación | giro y oscilación global | pivotes de extremidades y bufanda |
| Entorno | laboratorio cerrado | ciudad y 16 azoteas flotantes |
| Objetivo | pruebas de movimiento | saltos, cristales, checkpoints y meta |
| Evidencia visual | output/evidence/01_idle.png | output/evidence/skyline_gameplay.png |

El aumento de detalle también aumenta el costo geométrico. No se presenta como
optimización. El archivo glTF anterior sigue en assets/robot; el personaje actual
no pasa por un importador externo. La separación apariencia/controlador se mantiene.

Tres verificaciones del nuevo recurso:
1. Geometría/normales: conteos reales, vectores unitarios; 928 triángulos casi
   nulos registrados. Sin reparación topológica ni afirmación de malla lista para rig.
2. Escala: 0.998 × 1.867 × 0.973 m con accesorios en reposo, envolvente a escala 1 y cápsula
   de 1.8 m; se declara el pequeño exceso visual respecto a la colisión.
3. Materiales y articulaciones: cinco materiales incluidos, cero imágenes externas;
   pivotes separados, sin huesos ni pesos. Tarea 2 abordará rig y deformación.
