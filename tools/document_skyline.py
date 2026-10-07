"""Generate current SKYLINE report and traceability without rewriting legacy delivery."""
from pathlib import Path
import json, math, hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

R=Path(__file__).resolve().parents[1]
E=R/'output/evidence'
audit=json.loads((E/'skyline_audit.json').read_text())
model=audit['model']
run=json.loads((E/'skyline_video_results.json').read_text())
clean=json.loads((E/'skyline_clean_copy.json').read_text())
def write(path,text): (R/path).write_text(text,encoding='utf-8')
dimensions=' × '.join(f'{x:.3f}' for x in model['aabb_size_m'])
sha=hashlib.sha256((R/'scenes/courier_visual.tscn').read_bytes()).hexdigest()
write('assets/parkour/FICHA.md',f'''# Ficha técnica: mensajero SKYLINE

Autor de entrega: Alberto. Fecha: 2026-10-06 (America/Mexico_City).
Procedencia: recurso original de práctica creado con asistencia de Codex,
generador Python tools/build_parkour.py y primitivas nativas Godot 4.7.2.
Licencia del arte original: CC0 1.0. No generado con Tripo/Meshy.

| Dato | Resultado medido |
|---|---|
| Recurso final | scenes/courier_visual.tscn |
| Formato | escena nativa Godot, no glTF importado |
| MeshInstance3D | {model['parts']} |
| Triángulos indexados, sumados por instancia | {model['triangles']:,} |
| Vértices, sumados por instancia | {model['vertices']:,} |
| Materiales únicos | {model['materials']} |
| Texturas externas | 0 |
| Superficies con UV nativas | {model['uv_surfaces']} |
| Huesos, skinning, clips esqueléticos | 0 |
| AABB en reposo: ancho × alto × fondo | {dimensions} m |
| Límite mínimo Y | {model['aabb_min_m'][1]:.4f} m |
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
dentro de tolerancia 0.01. El contador detectó {model['degenerate_triangles']} triángulos de área
casi nula (producto cruzado al cuadrado < 1e-12), incluidos en el total, en las
primitivas teseladas. Se registra el hallazgo; no se afirma una malla optimizada,
soldada o lista para deformación. No se corrigió topología en esta entrega.

Animación: rotación de pivotes de brazos y piernas, inclinación del torso y bufanda
por courier_visual.gd. No mueve CharacterBody3D ni su cápsula. Preparación de rig,
pesos y revisión de topología para deformación quedan para Tarea 2.

Reproducción de la auditoría (requiere render para medir FPS reales):
`godot --path . --script tests/skyline_audit.gd -- --test`

Evidencia: output/evidence/skyline_audit.json.
SHA256 de courier_visual.tscn: {sha}
''')
write('Prompts/SKYLINE_prompt_exacto.txt','''SOLICITUD EXACTA DE ALBERTO (2026-10-06)
que se vea mejor el juego, algo diferentes, no se como un personaje y escenario como un mejor parkour

DIRECCIÓN DE ARTE COMUNICADA Y APLICADA
Le daré una estética de azoteas flotantes al atardecer: un pequeño corredor con
casco, mochila y animación al correr, plataformas con bordes luminosos, cristales
para recoger y puntos de control. También añadiré cronómetro y reinicio desde
el último punto de control para que las caídas no obliguen a empezar de cero.

HERRAMIENTA Y ALCANCE
Asistencia de Codex para diseño y código; geometría creada por Python y primitivas
nativas de Godot 4.7.2. No hubo envío de prompt ni exportación desde Tripo/Meshy.
La alternativa de recurso original de práctica fue autorizada por Alberto.
No aplican semilla de servicio 3D, créditos de generación ni versión de Tripo/Meshy.
La distribución de edificios usa random.Random(17) en el generador local.
''')
write('Prompts/SKYLINE_bitacora.md','''# Bitácora SKYLINE | Alberto

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
''')
write('Prompts/SKYLINE_comparacion.md',f'''# Antes / después

| Elemento | Kinetic Lab | SKYLINE |
|---|---|---|
| Personaje | robot de cajas, glTF | mensajero, escena nativa .tscn |
| Piezas | 11 | {model['parts']} |
| Triángulos instanciados | 132 | {model['triangles']:,} |
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
1. Geometría/normales: conteos reales, vectores unitarios; {model['degenerate_triangles']} triángulos casi
   nulos registrados. Sin reparación topológica ni afirmación de malla lista para rig.
2. Escala: {dimensions} m con accesorios en reposo, envolvente a escala 1 y cápsula
   de 1.8 m; se declara el pequeño exceso visual respecto a la colisión.
3. Materiales y articulaciones: cinco materiales incluidos, cero imágenes externas;
   pivotes separados, sin huesos ni pesos. Tarea 2 abordará rig y deformación.
''')

out=R/'output/pdf/Informe_SKYLINE_Alberto.pdf'
c=canvas.Canvas(str(out),pagesize=(595.28,841.89))
c.setTitle('SKYLINE - Rooftop Run | Informe de Alberto')
c.setAuthor('Alberto')
ink=HexColor('#182b3a'); accent=HexColor('#007e83'); orange=HexColor('#e87632'); pale=HexColor('#e9f1f3')
body=ParagraphStyle('Body',fontName='Helvetica',fontSize=10.4,leading=14.5,textColor=ink)
small=ParagraphStyle('Small',parent=body,fontSize=8.8,leading=12)
y=0
def page(n,title,sub):
    global y
    c.setFillColor(ink); c.rect(0,744,596,98,fill=1,stroke=0)
    c.setFillColor(HexColor('#70dfd7')); c.setFont('Helvetica-Bold',10); c.drawString(43,811,'S K Y L I N E    /    R O O F T O P   R U N')
    c.setFillColor(white); c.setFont('Helvetica-Bold',23); c.drawString(43,777,title)
    c.setFillColor(accent); c.setFont('Helvetica',9); c.drawString(43,722,sub)
    c.setFillColor(ink); c.setFont('Helvetica',8); c.drawString(43,29,'Alberto  /  Godot 4.7.2  /  06.10.2026')
    c.drawRightString(552,29,f'{n} / 6')
    c.setStrokeColor(HexColor('#d5e2e7')); c.line(43,44,552,44)
    y=696
def para(s,style=body):
    global y
    p=Paragraph(s,style); w,h=p.wrap(509,700)
    assert y-h>53, f'Page overflow at {s[:70]}: {y-h}'
    p.drawOn(c,43,y-h); y-=h+10
def heading(s):
    global y
    c.setFillColor(accent); c.setFont('Helvetica-Bold',12.5); c.drawString(43,y-13,s); y-=26
def image_file(filename,width=509,height=None,x=43):
    global y
    height=height or width*9/16
    c.drawImage(str(E/filename),x,y-height,width=width,height=height,preserveAspectRatio=True,anchor='c')
    y-=height+9
def table(rows,widths):
    global y
    cells=[[Paragraph(str(cell),small) for cell in row] for row in rows]
    t=Table(cells,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),pale),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f5f8f9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.7,accent)]))
    w,h=t.wrap(509,700); assert y-h>53; t.drawOn(c,43,y-h); y-=h+12
def end(): c.showPage()

page(1,'Parkour entre azoteas','Entrega individual de Alberto | Entorno, física, cámara y apariencia')
para('SKYLINE transforma el laboratorio inicial en un circuito de <b>16 azoteas flotantes</b> sobre una ciudad al atardecer. El objetivo es llegar a la meta; se pueden recoger 15 cristales y guardar avance en tres puntos de control intermedios.')
image_file('skyline_gameplay.png')
para('<b>Captura 1.</b> Inicio sobre una plataforma con colisión, personaje en Idle y HUD de tiempo, estado y progreso.',small)
heading('Controles y objetivo')
table([['Acción','Control'],['Moverse / saltar','WASD / Espacio (solo con apoyo)'],['Cámara / cursor','Ratón o flechas / Esc libera; clic captura'],['Reintentar / rendimiento','R vuelve al checkpoint; en meta reinicia / F: límite 30 o 144 FPS']],[148,361])
para('La ciudad, árboles y accesorios son decorativos. Las azoteas transitables tienen colisiones de caja o cilindro. Cielo procedural, iluminación cálida y sombras definen el entorno. El récord se guarda localmente; las caídas mantienen el cronómetro.',small)
end()

page(2,'Arquitectura y movimiento','Separación de física, presentación y reglas de la partida')
table([['Escena / archivo','Responsabilidad'],['parkour.tscn + parkour.gd','Nivel editable, aterrizajes, checkpoints, cristales, tiempo y meta.'],['courier_player.tscn + player.gd','CharacterBody3D, cápsula, movimiento y FSM.'],['courier_visual.tscn + courier_visual.gd','Modelo nativo independiente; pivotes de extremidades y bufanda.'],['CameraRig / Pitch / SpringArm3D','Yaw, inclinación, seguimiento y prueba de obstáculos.'],['crystal.gd / parkour_hud.gd','Recogida por Area3D / interfaz y estado activo.']],[216,293])
heading('Jerarquía editable del personaje')
para('Player (CharacterBody3D)<br/>   CollisionShape3D: cápsula, altura 1.8 m y radio 0.42 m<br/>   Visual: instancia de courier_visual.tscn<br/>      Body: casco, torso, mochila y pivotes de brazos/piernas<br/>   CameraRig / Pitch / SpringArm3D / Camera3D',small)
heading('Dónde se utiliza delta')
para('En <b>_physics_process(delta)</b>, a 60 Hz, Input.get_vector limita la diagonal. La base de yaw de la cámara transforma la entrada al plano XZ. Mirar arriba o abajo no altera la rapidez horizontal.')
para('<b>Velocidad:</b> 6 m/s. <b>Aceleración:</b> 22 m/s². <b>Gravedad:</b> 22 m/s². La aceleración y gravedad se multiplican por delta una sola vez para modificar velocity. El salto asigna directamente <b>9 m/s</b> al componente vertical cuando hay suelo.')
para('<b>move_and_slide()</b> integra velocity usando el paso físico; multiplicar antes esa velocidad por delta aplicaría el tiempo dos veces. En <b>_process(delta)</b> solo se actualizan orientación y poses visuales. Las flechas usan delta para girar por segundo; el ratón ya proporciona desplazamiento acumulado.')
para('La señal physics_stepped se emite después de mover y actualizar la FSM. El nivel examina esos contactos actualizados para guardar el checkpoint, evitando reutilizar el suelo de una posición anterior tras reaparecer.',small)
end()

page(3,'FSM y cámara','Estados explícitos, seguimiento y recuperación de caídas')
heading('Diagrama de transiciones')
def box(x,z,label):
    c.setFillColor(accent); c.roundRect(x,z,130,40,7,fill=1,stroke=0); c.setFillColor(white); c.setFont('Helvetica-Bold',14); c.drawCentredString(x+65,z+14,label)
def arrow(x1,y1,x2,y2):
    c.setStrokeColor(ink); c.setLineWidth(1); c.line(x1,y1,x2,y2); a=math.atan2(y2-y1,x2-x1)
    for d in [-.5,.5]: c.line(x2,y2,x2-7*math.cos(a+d),y2-7*math.sin(a+d))
box(63,586,'Idle'); box(401,586,'Walk'); box(232,465,'Jump')
arrow(193,617,401,617); arrow(401,594,193,594)
arrow(111,586,249,505); arrow(280,505,158,586)
arrow(485,586,346,505); arrow(315,505,438,586)
c.setFillColor(ink); c.setFont('Helvetica',9)
c.drawCentredString(297,633,'suelo + rapidez horizontal > 0.1 m/s')
c.drawCentredString(297,578,'suelo + rapidez horizontal <= 0.1 m/s')
c.drawString(58,533,'pierde apoyo'); c.drawRightString(536,533,'pierde apoyo')
c.drawCentredString(297,446,'Al aterrizar: Idle si se detiene, Walk si continúa')
y=425
para('Jump incluye tanto ascenso como caída. Las transiciones se deciden después de move_and_slide() y se validan con una tabla de cambios legales. El estado aparece en el HUD y en el registro FSM. Las poses de brazos y piernas acompañan el estado; no controlan la física.')
heading('Cámara orbital nativa')
para('El SpringArm3D de SKYLINE mide <b>6 m</b>, usa una esfera de 0.22 m y margen de 0.15 m. Su máscara consulta el nivel y excluye el RID del personaje. Pitch se limita entre -1.1 y 0.25 rad; FOV es 72° y el plano cercano 0.08 m.')
para('En la prueba con una pared temporal, el brazo se retrajo a <b>1.078 m</b> y un giro completo de 360° mantuvo la cámara del lado interior. Se utilizó el controlador actual. Los edificios y portales decorativos no son paredes físicas.',small)
heading('Puntos de control y meta')
para('Al aterrizar en las azoteas 5, 9 y 13 se guarda la posición de regreso. Si el personaje cae por debajo de Y = -12 m, se reinician posición, velocidad e interpolación. Llegar a la azotea 16 finaliza el tiempo. Los cristales son opcionales para completar el recorrido.')
end()

page(4,'Personaje y procedencia','Mensajero original de práctica | Modelo nativo, sin servicio 3D externo')
para('Alberto autorizó el recurso original de práctica. SKYLINE utiliza <b>primitivas de Godot generadas por Python</b>, con asistencia de Codex. No se usó Tripo/Meshy. El modelo actual es .tscn; el glTF del robot anterior se conserva como comparación. Ambos separan apariencia y controlador.')
table([['Ficha medida en reposo','Resultado'],['Piezas / triángulos / vértices',f'{model["parts"]} / {model["triangles"]:,} / {model["vertices"]:,} (sumados por instancia)'],['Materiales / texturas / UV',f'5 PBR / 0 imágenes / {model["uv_surfaces"]} superficies con UV nativas'],['Ancho × alto × fondo',f'{dimensions} m, incluidos mochila y bufanda'],['Escala / orientación','Envolvente 1,1,1; una unidad = un metro; frente -Z, arriba +Y'],['Huesos / pesos / clips','0; animación de piezas rígidas mediante pivotes']],[210,299])
heading('Antes y después')
table([['Criterio','Robot anterior','Mensajero actual'],['Forma y detalle','11 cajas; 132 triángulos','30 piezas redondeadas; 23,112 triángulos'],['Materiales y movimiento','3; oscilación global','5; extremidades, torso y bufanda'],['Resultado','Prueba funcional','Mayor identidad visual y mayor costo geométrico']],[125,171,213])
heading('Verificaciones y límites declarados')
para('<b>1. Malla y normales:</b> vectores finitos y unitarios. Se detectaron <b>928 triángulos de área casi nula</b> en las primitivas, incluidos en el total; no se hizo reparación topológica ni se afirma una malla optimizada.<br/><b>2. Escala:</b> altura visual 1.867 m y cápsula 1.8 m; casco y accesorios sobresalen ligeramente de la colisión.<br/><b>3. Materiales y articulaciones:</b> cinco materiales incluidos, sin imágenes faltantes; no hay rig ni skinning. La deformación corresponde a Tarea 2.',small)
para('Fecha: 06.10.2026. Arte original CC0. Generador: tools/build_parkour.py; semilla local de ciudad 17. Solicitud exacta, dirección aplicada y bitácora en Prompts/SKYLINE_*. Ficha completa y hash en assets/parkour/FICHA.md.',small)
end()

page(5,'Evidencias de ejecución','Capturas reales del motor y mediciones del controlador actual')
image_file('skyline_jump.png',height=185)
para('<b>Captura 2.</b> Salto del mensajero entre plataformas. El estado Jump se muestra en el HUD. La prueba técnica verifica que pulsar Espacio de nuevo en el aire no genera otro salto.',small)
image_file('skyline_checkpoint.png',height=185)
para('<b>Captura 3.</b> Aterrizaje en el checkpoint de la azotea 9. La prueba fuerza una caída y comprueba el regreso al punto guardado; después completa el recorrido y recoge 15 cristales.',small)
heading('Comparación con dos límites de render')
table([['Intervalo','30 FPS','144 FPS'],['120 pasos físicos = 2 s',f'{audit["distance_30"]:.5f} m',f'{audit["distance_144"]:.5f} m'],['FPS observados en la medición','30','144']],[225,142,142])
para('Diferencia: <b>0.00000 m</b> en esta ejecución. La distancia es menor que 12 m por la aceleración desde reposo. La física permanece a 60 Hz; el render no cambia ese paso. La medición se realizó con render normal sobre un suelo temporal amplio, no con el grabador de video. Otros equipos pueden presentar pequeñas diferencias de muestreo.',small)
end()

page(6,'Reproducción y entrega','Proyecto completo, video y registro de pruebas')
heading('Abrir una copia del proyecto')
para('Extraer Skyline_Alberto.zip, importar project.godot con Godot 4.7.2 y esperar la importación. <b>F5</b> inicia SKYLINE; abrir parkour.tscn, courier_player.tscn o courier_visual.tscn permite editar sus nodos en la vista 3D. Compatibility/OpenGL y GodotPhysics3D no requieren plugins.')
heading('Resultados y cobertura')
table([['Prueba','Resultado registrado'],['Recorrido actual','20 comprobaciones: inicio, 15 saltos, checkpoint intermedio, meta, cristales y regreso tras caída. Sin fallos.'],['Auditoría actual','11 comprobaciones: 30/144 FPS, Idle/Walk/Jump, doble salto, dirección de cámara y giro junto a pared. Sin fallos.'],['Copia limpia','Reimportación sin .godot y ejecución del parkour y laboratorio de regresión. Sin errores registrados.']],[155,354])
para('Las pruebas son automatizadas con el controlador real. El video es una demostración automatizada de aproximadamente un minuto, con pausas para observar personaje, checkpoints y meta; no es una partida manual ni una medición de rendimiento.',small)
heading('Archivos de entrega')
para('<link href="../Skyline_Alberto.zip" color="#007e83"><b>Proyecto completo: Skyline_Alberto.zip</b></link><br/><link href="../evidence/Skyline_Alberto.mp4" color="#007e83"><b>Video: Skyline_Alberto.mp4</b></link><br/>README.md: controles, versión, escenas, pruebas e instrucciones.<br/>Prompts/SKYLINE_*: solicitud, bitácora y comparación.<br/>assets/parkour/FICHA.md: malla, materiales, escala y procedencia.')
para('<b>Enlaces locales:</b> conservar PDF en output/pdf, video en output/evidence y ZIP en output. Si la institución exige URLs web, subir ZIP y video y sustituir estos enlaces. No se proporcionó destino de publicación.',small)
heading('Cómo repetir y consultar')
para('<font face="Courier" size="8.5">godot --path . -- --parkour-test<br/>godot --path . --script tests/skyline_audit.gd -- --test</font><br/>Evidencia en output/evidence: parkour_results.json, skyline_audit.json y skyline_clean_copy.json.',small)
para('Referencias técnicas: <link href="https://docs.godotengine.org/en/4.5/classes/class_characterbody3d.html" color="#007e83">CharacterBody3D y move_and_slide()</link> y <link href="https://docs.godotengine.org/en/4.0/classes/class_springarm3d.html" color="#007e83">SpringArm3D</link> (documentación oficial). Los materiales de apoyo internos del curso no se proporcionaron; no se atribuye revisión de su contenido.',small)
end()
c.save()
print(out)
