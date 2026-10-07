"""Build the six-page report and provenance files from measured evidence."""
from pathlib import Path
import json, math, struct, base64, hashlib, copy
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

R=Path(__file__).resolve().parents[1]
def write(path,text): (R/path).write_text(text,encoding='utf-8')
data=json.loads((R/'output/evidence/results.json').read_text())
gltf=json.loads((R/'assets/robot/robot_practica.gltf').read_text())
variant=copy.deepcopy(gltf)
variant['materials'][0]['pbrMetallicRoughness']['baseColorFactor']=[.72,.75,.78,1]
write('assets/robot/robot_variante_gris.gltf',json.dumps(variant,indent=2))
low=[min(n['translation'][j]-n['scale'][j]/2 for n in gltf['nodes']) for j in range(3)]
high=[max(n['translation'][j]+n['scale'][j]/2 for n in gltf['nodes']) for j in range(3)]
blob=base64.b64decode(gltf['buffers'][0]['uri'].split(',')[1])
pos=struct.unpack('<72f',blob[:288]); nor=struct.unpack('<72f',blob[288:576]); idx=struct.unpack('<36H',blob[576:])
normal_ok=True
for k in range(0,36,3):
    a,b,c=[pos[idx[k+j]*3:idx[k+j]*3+3] for j in range(3)]
    u=[b[j]-a[j] for j in range(3)]; v=[c[j]-a[j] for j in range(3)]
    cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
    n=nor[idx[k]*3:idx[k]*3+3]
    normal_ok &= sum(cross[j]*n[j] for j in range(3))>0
audit={'nodes':len(gltf['nodes']),'triangles_instantiated':len(gltf['nodes'])*12,'materials':len(gltf['materials']),'textures':0,'uv_channels':0,'skeletons':0,'dimensions_m':[round(high[j]-low[j],4) for j in range(3)],'outward_normals':normal_ok,'positive_scales':all(all(x>0 for x in n['scale']) for n in gltf['nodes']),'sha256':hashlib.sha256((R/'assets/robot/robot_practica.gltf').read_bytes()).hexdigest()}
write('output/evidence/model_audit.json',json.dumps(audit,indent=2))
write('Prompts/prompt_exacto.txt','''PROMPT DE DISEÑO USADO PARA EL RECURSO ORIGINAL DE PRÁCTICA
Crear un robot humanoide simple de baja poligonización, 1.78 metros de altura,
con cabeza rectangular, visor ámbar, torso de cerámica verde menta, brazos
separados, juntas de grafito y pies planos. Usar piezas rígidas y normales planas,
sin texturas externas, sin esqueleto y sin animaciones. Orientar el frente hacia
-Z, mantener +Y arriba y colocar los pies en Y=0. Exportar glTF 2.0 con materiales
PBR, escala métrica y origen centrado en el suelo. La apariencia no debe contener
código de movimiento, cámara ni colisiones.

VARIANTE: conservar la misma geometría y sustituir la cerámica menta por gris.

Este texto especificó el diseño del generador local tools/build_assets.py.
NO se envió a Tripo ni a Meshy; no se atribuye a esas herramientas.
''')
write('Prompts/bitacora.md','''# Bitácora | Alberto

Fecha: 26 de septiembre de 2026 (America/Mexico_City).

- Contexto inicial: proyecto Godot vacío, sin modelo ni acceso conectado a Tripo/Meshy.
- Alternativa autorizada por Alberto: "Usar modelo original de práctica".
- Herramientas: asistencia de Codex para código/diseño, Python estándar para geometría,
  exportación glTF 2.0 y Godot 4.7.2 para importación y pruebas.
- No se realizó una generación, descarga o exportación desde Tripo/Meshy.
- Prompt exacto: `prompt_exacto.txt`. No hay semilla, cuenta o versión de servicio
  generativo 3D que reportar: no aplican al generador determinista local.
- Ajustes: once cajas, 132 triángulos instanciados, tres materiales PBR,
  metallic=0.12, roughness=0.65, sin texturas; +Y arriba, frente -Z.
- Comparación: variante gris frente a versión menta; misma geometría y escala.
  Se selecciona menta por identificación visual frente a suelo y paredes.
- No se detectaron defectos de malla que exigieran corrección. Se registran las
  tres verificaciones de comparación.md; no se inventan defectos anteriores.
- Ajustes del proyecto: IDs de recursos de rejilla válidos; ayuda del HUD compacta;
  cámara aislada de entrada manual durante tests; ruta de test de esquina interior.
- Recurso original cedido bajo CC0. Véase assets/robot/LICENSE.txt.
- Autor de entrega: Alberto. Asistencia técnica y recurso procedural declarados.
''')
write('Prompts/comparacion.md',f'''# Antes / después: comparación de variante

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
1. Malla: 11 piezas, caras no degeneradas, normales exteriores: {normal_ok}.
   Las piezas se intersectan por diseño de robot rígido; no es una piel continua.
2. Escala: pies en Y=0, altura 1.78 m, envolvente a escala 1; cápsula de 1.8 m.
3. Materiales y articulaciones: tres PBR integrados, cero imágenes externas;
   brazos y piernas separados, sin huesos/pesos. Rig y deformación pendientes de
   Tarea 2. La oscilación global actual es solo indicación visual de Walk.

Auditoría reproducible: `output/evidence/model_audit.json`.
''')
write('assets/robot/FICHA.md',f'''# Ficha técnica | Robot de práctica

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
- Normales exteriores verificadas: {normal_ok}; escalas positivas: {audit['positive_scales']}.
- Procedencia: tools/build_assets.py; no generado por Tripo/Meshy.
- Variante gris conservada para comparación, misma geometría.
- SHA256 final: {audit['sha256']}
''')
write('README.md','''# Kinetic Lab | Alberto

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
godot --path . -- --test
godot --headless --path . -- --test
godot --path . --write-movie output/evidence/demostracion.avi --fixed-fps 30 -- --demo
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

## Entrega y trazabilidad

- Informe: [PDF de seis páginas](output/pdf/Informe_Alberto.pdf).
- Video: [demostración MP4](output/evidence/Demostracion_Alberto.mp4).
- Proyecto: [ZIP completo](output/Proyecto_Alberto.zip).
- Modelo final y ficha: `assets/robot/`.
- Prompt, bitácora y comparación: `Prompts/`.
- Variante editable: `scenes/model_comparison.tscn`.

Los enlaces son locales/relativos. No se proporcionó cuenta o destino de publicación;
Alberto debe subir ZIP y MP4 e incorporar sus URLs públicas antes de entregar si
la institución exige enlaces web. No se inventaron direcciones publicadas.

Alberto autorizó usar un modelo original de práctica al no disponer aquí de acceso
conectado a Tripo/Meshy. No se afirma haber utilizado esas herramientas. El recurso
es procedural CC0, con asistencia de Codex; sin material externo. No se recibieron
los documentos de apoyo del curso, por lo que no se atribuye revisión de su contenido.

Referencias oficiales:
- https://docs.godotengine.org/en/4.5/classes/class_characterbody3d.html
- https://docs.godotengine.org/en/4.0/classes/class_springarm3d.html
''')

out=R/'output/pdf/Informe_Alberto.pdf'
c=canvas.Canvas(str(out),pagesize=(595.28,841.89))
c.setTitle('Kinetic Lab | Alberto | Informe de escena 3D')
c.setAuthor('Alberto')
ink=HexColor('#172e40'); teal=HexColor('#007f79'); muted=HexColor('#506476')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10.3,leading=15,textColor=ink,spaceAfter=8)
y=0
def text(s):
    global y
    p=Paragraph(s,style); w,h=p.wrap(499,700); p.drawOn(c,48,y-h); y-=h+10
def heading(s):
    global y
    c.setFillColor(teal); c.setFont('Helvetica-Bold',13); c.drawString(48,y-13,s); y-=29
def page(n,title,subtitle):
    global y
    c.setFillColor(ink); c.rect(0,748,596,94,fill=1,stroke=0)
    c.setFillColor(HexColor('#64e2c9')); c.setFont('Helvetica-Bold',10); c.drawString(48,809,'KINETIC / LAB 01     •     ALBERTO')
    c.setFillColor(white); c.setFont('Helvetica-Bold',22); c.drawString(48,776,title)
    c.setFillColor(muted); c.setFont('Helvetica',9); c.drawString(48,728,subtitle)
    c.setStrokeColor(HexColor('#d8e3e9')); c.line(48,43,547,43)
    c.setFont('Helvetica',8); c.drawString(48,28,'Godot 4.7.2  /  Recurso original de práctica  /  26.09.2026')
    c.drawRightString(547,28,f'{n} / 6'); y=701
def picture(name,height=235):
    global y
    c.drawImage(str(R/'output/evidence'/name),48,y-height,width=499,height=height,preserveAspectRatio=True,anchor='c'); y-=height+14

page(1,'Escena 3D controlable','Entrega individual · Arquitectura, física, cámara y FSM')
text('Autor: <b>Alberto</b>. Se construyó un laboratorio 3D editable con robot de práctica, obstáculos y cámara orbital. La lógica pertenece al CharacterBody3D; el modelo importado aporta exclusivamente apariencia.')
picture('01_idle.png',281)
heading('Alcance y controles')
text('<b>WASD</b> mueve según la orientación horizontal de cámara. <b>Espacio</b> salta solo con apoyo. <b>Ratón / flechas</b> giran la cámara; <b>Esc</b> libera el cursor y clic lo captura. <b>R</b> reinicia; <b>F</b> alterna límites de 30 y 144 FPS.')
text('Suelo y obstáculos usan StaticBody3D con cajas de colisión. El personaje utiliza una cápsula. El cielo procedural y un sol direccional con sombras hacen visibles la orientación y el contacto con el suelo.')
text('<b>Procedencia declarada:</b> Alberto autorizó el recurso original de práctica. No se utilizó Tripo/Meshy ni se simula una exportación de esos servicios. Animaciones esqueléticas y deformación quedan para Tarea 2.')
c.showPage()

page(2,'Arquitectura editable','Responsabilidad de cada escena y separación del modelo')
heading('Escenas del proyecto')
for title,body in [('level.tscn','Nivel persistente: suelo, paredes, escalones, esquina, cielo, luz, Player y HUD.'),('player.tscn','CharacterBody3D con player.gd, CapsuleShape3D y dos hijos independientes: Visual y CameraRig.'),('robot_visual.tscn','Envolvente a escala 1. Instancia robot_practica.gltf. Sustituir el recurso aquí conserva el controlador.'),('model_comparison.tscn','Comparación editable de la misma geometría en cerámica gris y menta.')]:
    heading(title); text(body)
heading('Jerarquía del personaje')
text('Player (CharacterBody3D)<br/>   CollisionShape3D: cápsula 1.8 m / radio 0.42 m<br/>   Visual: robot_visual.tscn<br/>      ImportedModel: robot_practica.gltf<br/>   CameraRig: yaw y seguimiento del cuerpo<br/>      Pitch: inclinación limitada<br/>         SpringArm3D: prueba de obstáculos<br/>            Camera3D: perspectiva, near 0.08 m')
heading('Cómo inspeccionar')
text('Importar project.godot, abrir las escenas desde FileSystem y usar la vista 3D. El nivel no se crea exclusivamente en tiempo de ejecución: geometría y colisiones están guardadas en .tscn. F5 ejecuta el proyecto. Compatibility y GodotPhysics3D evitan dependencias de complementos.')
c.showPage()

page(3,'Movimiento y tiempo','Velocidad en m/s; aceleración en m/s²; física a 60 Hz')
heading('Un solo paso de integración')
text('En <b>_physics_process(delta)</b>, Input.get_vector limita la entrada diagonal. La base horizontal de CameraRig transforma (x, 0, y) a mundo, de modo que W sigue el frente de cámara sin ganar velocidad al mirar arriba o abajo.')
text('La aceleración horizontal usa move_toward con <b>aceleración × delta</b>. En aire, <b>velocity.y -= gravedad × delta</b>. Al presionar salto y estar en suelo se asigna <b>velocity.y = 8 m/s</b>. No se multiplica ese impulso por delta.')
text('<b>move_and_slide()</b> recibe velocity en m/s e integra internamente el paso físico. Multiplicar antes velocity por delta aplicaría el tiempo dos veces. Las colisiones, la gravedad y la posición real permanecen en el paso físico.')
heading('Actualización visual')
text('<b>_process(delta)</b> interpola el giro del modelo con 1 - exp(-14 × delta) y actualiza una oscilación de 2.5 cm en Walk. No mueve la cápsula. El ratón ya contiene desplazamiento acumulado: no usa delta; el giro con flechas expresa radianes por segundo y sí lo utiliza.')
heading('Experimento: 120 pasos = 2 segundos simulados')
text(f'Límite de render <b>30 FPS: {data["distance_30"]:.5f} m</b>.<br/>Límite de render <b>144 FPS: {data["distance_144"]:.5f} m</b>.<br/>Diferencia: <b>{abs(data["distance_30"]-data["distance_144"]):.5f} m</b>. Resultados del modo test con render, no del grabador.')
text('El recorrido es menor a 10 m porque se acelera desde reposo hasta 5 m/s. Cambiar el límite de render no cambia los 60 pasos físicos por segundo. El límite es un máximo, no una garantía de FPS alcanzados. En otros equipos puede haber diferencias pequeñas por muestreo de entrada, pasos en el borde del intervalo o saturación de CPU.')
heading('Fuente técnica')
text('<link href="https://docs.godotengine.org/en/4.5/classes/class_characterbody3d.html" color="#007f79">Godot: CharacterBody3D, velocity y move_and_slide()</link>. La documentación confirma que velocity no debe multiplicarse por delta antes de llamar al método.')
c.showPage()

page(4,'FSM y cámara','Transiciones explícitas y tratamiento nativo de obstáculos')
heading('Estados observables')
# Compact directed FSM diagram with all six legal transitions.
for x,label in [(70,'Idle'),(355,'Walk')]:
    c.setFillColor(teal); c.roundRect(x,575,150,44,8,fill=1,stroke=0); c.setFillColor(white); c.setFont('Helvetica-Bold',14); c.drawCentredString(x+75,592,label)
c.setFillColor(ink); c.roundRect(213,438,150,44,8,fill=1,stroke=0); c.setFillColor(white); c.drawCentredString(288,455,'Jump')
def arrow(x1,y1,x2,y2):
    c.setStrokeColor(muted); c.setLineWidth(1.2); c.line(x1,y1,x2,y2)
    angle=math.atan2(y2-y1,x2-x1)
    for d in [-.5,.5]: c.line(x2,y2,x2-8*math.cos(angle+d),y2-8*math.sin(angle+d))
arrow(220,606,355,606); arrow(355,584,220,584)
arrow(122,575,238,482); arrow(270,482,183,575)
arrow(453,575,340,482); arrow(308,482,391,575)
c.setFillColor(ink); c.setFont('Helvetica',9); c.drawCentredString(287,620,'suelo + velocidad > 0.1'); c.drawCentredString(287,570,'suelo + velocidad <= 0.1')
c.drawString(62,519,'pierde apoyo'); c.drawString(401,519,'pierde apoyo')
c.drawCentredString(288,414,'Aterriza: Idle si se detiene; Walk si sigue moviéndose')
y=391
text('Jump incluye ascenso y caída, también al abandonar una plataforma. La decisión se toma después de move_and_slide(), usando apoyo actualizado y velocidad horizontal. Una tabla de transiciones legales valida los cambios; el HUD y el registro FSM muestran el estado activo.')
heading('Seguimiento y colisión de cámara')
text('SpringArm3D sigue al personaje mediante la jerarquía. Longitud 5.5 m, esfera de barrido de 0.22 m, margen 0.15 m y máscara del nivel. Se excluye expresamente el RID del jugador. Al encontrar una pared, el brazo se acorta; pitch entre -1.1 y 0.25 rad evita inclinaciones extremas.')
text('La prueba recorre 360° cerca de la pared sur y comprueba la posición de cámara. El brazo llega a 1.085 m en la posición de ensayo, sin salir del límite interior. Esta prueba cubre esa pared; se añade comprobación del cuerpo en una esquina y conviene explorar manualmente todas las combinaciones.')
text('<link href="https://docs.godotengine.org/en/4.0/classes/class_springarm3d.html" color="#007f79">Referencia oficial: SpringArm3D</link>. No se utiliza complemento externo.')
c.showPage()

page(5,'Modelo y trazabilidad','Recurso original de práctica autorizado; sin servicio 3D externo')
heading('Especificación exacta y herramienta')
text('Robot simple de baja poligonización, cabeza rectangular, visor ámbar, cerámica menta, juntas de grafito, pies planos y piezas rígidas separadas. Altura 1.78 m, +Y arriba, frente -Z y origen en el suelo. El texto completo se conserva en <b>Prompts/prompt_exacto.txt</b>.')
text('Herramienta: generador local determinista en Python con asistencia de Codex; exportación glTF 2.0 e importación en Godot 4.7.2. Fecha: 26.09.2026. No aplican semilla ni parámetros de Tripo/Meshy. Licencia original: CC0 1.0. No se usaron modelos descargados ni texturas externas.')
heading('Ficha técnica final')
text('<b>132 triángulos instanciados / 11 piezas / 264 vértices instanciados.</b><br/>Tres materiales PBR; metallic 0.12, roughness 0.65. Cero texturas y UV.<br/>Dimensiones: 1.03 × 1.78 × 0.465 m. Una unidad = un metro.<br/>Cero huesos, pesos de skin o clips; articulaciones aún no preparadas para deformación. Los brazos exceden ligeramente la cápsula y no colisionan por separado.')
heading('Comparación A / B')
for x,col,label in [(48,'#b8bfc7','A / gris'),(302,'#1fb89e','B / menta final')]:
    c.setFillColor(HexColor(col)); c.roundRect(x,y-47,238,47,6,fill=1,stroke=0)
    c.setFillColor(ink); c.setFont('Helvetica-Bold',12); c.drawString(x+15,y-29,label)
y-=65
text('La variante gris conserva geometría y materiales salvo el color base de cerámica. Se eligió menta para reconocer al personaje. Ambas se conservan en assets/robot y en una escena de comparación editable. No se presenta como reparación de un defecto.')
heading('Tres verificaciones registradas')
text('1. Caras no degeneradas y normales exteriores coherentes con el winding.<br/>2. Pies en Y=0, escala positiva y altura compatible con cápsula de 1.8 m.<br/>3. Materiales integrados, sin imágenes faltantes; piezas rígidas separadas y ausencia de rig declarada. Evidencia: model_audit.json y FICHA.md.')
c.showPage()

page(6,'Pruebas y entrega','Capturas del motor · resultados reproducibles · enlaces locales')
picture('02_jump.png',187)
text('<b>Captura 2:</b> Jump en aire. Repetir Espacio no incrementó el contador de saltos; el personaje aterrizó y volvió a Idle.')
picture('03_camera.png',187)
text('<b>Captura 3:</b> cámara retraída junto a pared. El cuerpo no atravesó suelo, cubo, pared ni esquina. La captura 1, en página 1, muestra Idle y el entorno.')
text(f'<b>{len(data["results"])} comprobaciones / {data["failures"]} fallos</b> en ejecución con render. Se conserva JSON con medidas. La copia limpia se reimporta y ejecuta sin incluir .godot; su resultado se registra en clean_copy.json.')
text('<link href="../Proyecto_Alberto.zip" color="#007f79"><b>Proyecto completo (ZIP)</b></link> · <link href="../evidence/Demostracion_Alberto.mp4" color="#007f79"><b>Video de demostración (MP4)</b></link><br/>Enlaces relativos a archivos adjuntos. Falta destino de publicación: subir ambos y sustituir por URLs si se exigen enlaces web. Autor: Alberto.')
c.save()
print(out)
