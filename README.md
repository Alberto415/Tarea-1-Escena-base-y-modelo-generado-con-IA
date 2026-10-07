# SKYLINE | Rooftop Run

Actualización visual y jugable del **6 de octubre de 2026** para Alberto.
Abre `project.godot` con **Godot 4.7.2** y pulsa **F5**. Ahora inicia SKYLINE.

- Mensajero con casco, visor, mochila y bufanda; brazos y piernas animados mediante pivotes.
- 16 azoteas flotantes circulares/rectangulares sobre una ciudad al atardecer.
- 15 cristales, 3 checkpoints intermedios, cronómetro, récord local y pantalla de meta.
- Caer devuelve al último checkpoint. R también regresa; en la meta, R inicia otra partida.
- WASD mueve, Espacio salta, ratón/flechas giran cámara, Esc libera el cursor, clic captura.
- F alterna límite 30/144 FPS. El nuevo corredor usa velocidad 6 m/s y salto 9 m/s;
  el laboratorio conserva sus valores originales 5 m/s y 8 m/s.

Escenas editables: `scenes/parkour.tscn`, `scenes/courier_player.tscn`,
`scenes/courier_visual.tscn`. Procedencia: `assets/parkour/PROCEDENCIA.md`.
Sin plugins, servicios externos ni texturas que descargar. Animación rígida, sin skinning.

Prueba del recorrido (saltos reales, cristales, meta y recuperación desde checkpoints):

```powershell
godot --path . -- --parkour-test
```

Evidencia: `output/evidence/parkour_results.json` y capturas `skyline_*.png`.
Proyecto actualizado: `output/Skyline_Alberto.zip`. Copia limpia validada en
`output/evidence/skyline_clean_copy.json`. El arte se reproduce con
`tools/build_parkour.py`; sobrescribe solamente las escenas de SKYLINE.

## Documentación actual de SKYLINE

- [Informe de seis páginas](output/pdf/Informe_SKYLINE_Alberto.pdf): estructura,
  movimiento y delta, diagrama FSM, cámara, tres capturas y pruebas.
- [Video actual (1 min 10 s)](output/evidence/Skyline_Alberto.mp4): demostración
  automatizada del recorrido, personaje, puntos de control y meta.
- [Proyecto completo actualizado](output/Skyline_Alberto.zip).
- [Ficha medida del mensajero](assets/parkour/FICHA.md).
- Solicitud exacta, bitácora y comparación: `Prompts/SKYLINE_*`.

Son enlaces a archivos locales. Falta publicar en la plataforma de entrega si se
requieren enlaces web; no se han inventado URLs. El PDF incluye enlaces relativos.

La auditoría del personaje actual usa 6 m/s y salto 9 m/s. Resultado: 11.23112 m
en 120 pasos físicos a 30 y a 144 FPS, diferencia 0.00000 m. La prueba se ejecuta
con render normal; no se utiliza el tiempo acelerado del grabador como evidencia.
Malla: 30 piezas, 23,112 triángulos indexados, cinco materiales y cero texturas.
Se registran 928 triángulos de área casi nula de las primitivas; no se declara
optimización topológica ni preparación para deformación. Véase la ficha completa.

```powershell
godot --path . --script tests/skyline_audit.gd -- --test
godot --path . --write-movie output/evidence/Skyline_demo.avi --fixed-fps 30 -- --parkour-test --skyline-video
```

`tools/document_skyline.py` reproduce el PDF y los documentos de trazabilidad actuales
con Python + reportlab, a partir de los JSON y capturas en output/evidence.
`skyline_video_results.json` conserva las 20 comprobaciones de la grabación por separado.
El informe registra las 11 comprobaciones de la auditoría y las 20 del recorrido.

## Entrega anterior: Kinetic Lab (archivo histórico)

El PDF, video y ZIP llamados Informe/Demostracion/Proyecto_Alberto corresponden a la
versión anterior del laboratorio. **No describen esta actualización de parkour.**
Se conservan como registro de la primera entrega. Los scripts build_assets.py y
document_delivery.py reconstruyen esa entrega anterior; no ejecutarlos para actualizar SKYLINE.
Para ejecutar el laboratorio, abrir `scenes/level.tscn` y pulsar F6.

Escena individual para Godot 4.x: movimiento, física, cámara y apariencia separados.
Preparada y probada en **Godot 4.7.2 stable**, render Compatibility/OpenGL,
GodotPhysics3D a 60 Hz. No requiere complementos, Blender ni servicios en línea.

## Abrir y jugar

1. Importar `project.godot` en Godot 4.7.2 y esperar la importación del glTF.
2. Abrir `scenes/level.tscn`, `scenes/player.tscn` o `scenes/robot_visual.tscn`
   para editar sus nodos en la vista 3D. F6 prueba la escena; F5 inicia el nivel.
3. WASD: movimiento relativo al giro horizontal de cámara. Espacio: salto en suelo.
   Ratón o flechas: cámara. Esc: liberar ratón; clic: capturar. R: reiniciar.
   F: alternar límite de 30/144 FPS. El contador real puede ser menor al límite.
4. Probar cubo naranja, escalones, esquina azul y paredes del perímetro.

## Estructura

`level.tscn`: suelo/obstáculos StaticBody3D, colisiones BoxShape3D, cielo procedural,
sol con sombras, personaje y HUD. `player.tscn`: CharacterBody3D + cápsula,
envolvente visual y CameraRig/Pitch/SpringArm3D/Camera3D. `robot_visual.tscn`
instancia el glTF sin mezclar física con apariencia. `node_3d.tscn` abre el nivel
como escena heredada para conservar el punto de entrada original.

## Física, tiempo y FSM

`player.gd` usa `_physics_process(delta)` a 60 Hz. Aceleración horizontal y gravedad
se multiplican por delta una vez para cambiar velocity (m/s). El impulso de salto
se asigna en m/s. `move_and_slide()` integra velocity: no pasar velocity * delta.
`_process(delta)` interpola giro visual y oscilación global; no mueve el cuerpo.
El ratón entrega desplazamiento acumulado y no usa delta; las flechas, rad/s, sí.
Movimiento normalizado para evitar ventaja diagonal; proyección sobre XZ a partir
del yaw de cámara, independientemente del pitch. Interpolación física activada.

Idle -> Walk al superar 0.1 m/s en suelo; Walk -> Idle al frenar. Ambos -> Jump al
perder apoyo (salto o caída). Jump -> Idle/Walk al aterrizar según velocidad.
Transiciones legales explícitas, señal state_changed, registro FSM y HUD visible.
Los clips y la deformación esquelética se reservan para Tarea 2.

SpringArm nativo de 5.5 m con esfera de 0.22 m, margen 0.15 m y máscara del nivel;
excluye al jugador. Pitch limitado. Seguimiento por jerarquía e interpolación física.

## Pruebas reproducibles

Desde la carpeta del proyecto (sustituir `godot` por la ruta del ejecutable):

```powershell
godot --headless --path . --editor --import --quit
godot --path . res://scenes/level.tscn -- --test
godot --headless --path . res://scenes/level.tscn -- --test
godot --path . res://scenes/level.tscn --write-movie output/evidence/demostracion.avi --fixed-fps 30 -- --demo
```

El modo test ejecuta 18 comprobaciones, genera results.json y tres capturas reales
cuando hay render. Finaliza con código 0 si pasan. El modo demo dura aproximadamente
80 segundos; usa el grabador nativo y guarda demo_results.json por separado.
La medición válida entre límites usa `--test`, NO el tiempo acelerado del grabador.
Los tests automatizan la entrada del personaje; completar una exploración manual
es recomendable para evaluar la sensación de control.

`output/evidence/results.json`: resultados reales, 30/144 FPS y colisiones.
`output/evidence/model_audit.json`: malla, normales y escala.
`output/evidence/clean_copy.json`: resultado de reimportar y ejecutar copia limpia.
`tools/document_delivery.py`: reproduce documentación (Python + reportlab).
`tools/build_assets.py`: reproduce recurso original y escenas base; sobrescribe esas
escenas. No ejecutar si se desea conservar cambios manuales en ellas.




Referencias oficiales:
- https://docs.godotengine.org/en/4.5/classes/class_characterbody3d.html
- https://docs.godotengine.org/en/4.0/classes/class_springarm3d.html
