# Bitácora SKYLINE | Alberto

## 2026-09-26: base conservada
Se desarrolló Kinetic Lab con robot original glTF, controlador, cámara, FSM y pruebas.
Alberto autorizó "Usar modelo original de práctica". Esa autorización se conserva.

## 2026-10-06: revisión visual solicitada
- Petición exacta y dirección de arte: SKYLINE_prompt_exacto.txt.
- Se creó un mensajero de piezas redondeadas, traje marfil y detalles naranja/cian.
- Se guardaron escena de apariencia, escena de controlador y nivel por separado.
- Se diseñaron 16 azoteas, 15 cristales, inicio/meta y checkpoints en azoteas 5, 9 y 13.
- Herramientas: Python, Godot 4.7.2, asistencia de Codex. Sin Tripo/Meshy ni plugins.
- Distribución de ciudad: semilla local 17; parámetros exactos en build_parkour.py.
- Física: 60 Hz, velocidad 6 m/s, aceleración y gravedad 22 m/s², salto 9 m/s.
- Se corrigió la lectura de aterrizaje tras teletransporte: physics_stepped informa
  al nivel después de mover el cuerpo, evitando reutilizar contactos anteriores.
- Se sustituyó la dependencia JSON de ruta por un recurso .gd precargado para
  incluir los datos en exportaciones. El JSON permanece como referencia legible.

## 2026-10-06: documentación actualizada
- Auditoría del mensajero y pruebas a 30/144 FPS: skyline_audit.json.
- Recorrido de 15 saltos, cristales, meta y dos caídas controladas: parkour_results.json
  y skyline_video_results.json. El video usa el modo de grabación del motor.
- Se declaran los triángulos de área casi nula de las primitivas y ausencia de rig;
  no se inventan reparaciones de malla ni generación por servicios externos.
- PDF actual: output/pdf/Informe_SKYLINE_Alberto.pdf. Video y ZIP relativos en el PDF.
- No se proporcionó destino web de publicación; los enlaces son a archivos locales.
