"""Rebuild original practice robot and editable level. Python standard library only."""
from pathlib import Path
import json, struct, base64

ROOT = Path(__file__).resolve().parents[1]
for folder in ['scenes','scripts','assets/robot','Prompts','tests','docs','output/pdf','output/evidence']:
    (ROOT/folder).mkdir(parents=True, exist_ok=True)
def put(path, data):
    (ROOT/path).write_text(data, encoding='utf-8')

# Original hard-surface geometry, outward face winding and split flat normals.
positions=[]; normals=[]; indices=[]
faces=[((1,0,0),[(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),
       ((-1,0,0),[(-1,-1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1)]),
       ((0,1,0),[(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),
       ((0,-1,0),[(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,-1,1)]),
       ((0,0,1),[(1,-1,1),(1,1,1),(-1,1,1),(-1,-1,1)]),
       ((0,0,-1),[(-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1)])]
for n, verts in faces:
    k=len(positions); positions.extend([[v/2 for v in p] for p in verts]); normals.extend([n]*4)
    indices.extend([k,k+1,k+2,k,k+2,k+3])
chunks=[struct.pack('<72f',*[v for p in positions for v in p]),struct.pack('<72f',*[v for n in normals for v in n]),struct.pack('<36H',*indices)]
blob=b''.join(chunks)
materials=[('Ceramica_menta',[.12,.72,.62,1]),('Juntas_grafito',[.055,.085,.13,1]),('Visor_ambar',[1,.57,.12,1])]
parts=[('Torso',[0,1.02,0],[.64,.60,.38],0),('Cabeza',[0,1.56,0],[.58,.44,.43],0),
       ('Visor',[0,1.58,-.225],[.45,.17,.035],2),('Cadera',[0,.66,0],[.45,.15,.3],1),
       ('BrazoL',[-.43,1.04,0],[.17,.52,.22],0),('BrazoR',[.43,1.04,0],[.17,.52,.22],0),
       ('PiernaL',[-.17,.36,0],[.19,.44,.22],1),('PiernaR',[.17,.36,0],[.19,.44,.22],1),
       ('PieL',[-.17,.09,-.06],[.25,.18,.38],0),('PieR',[.17,.09,-.06],[.25,.18,.38],0),
       ('Insignia',[0,1.08,-.2],[.16,.16,.025],2)]
gltf={'asset':{'version':'2.0','generator':'Original practice asset / tools/build_assets.py'},
      'scene':0,'scenes':[{'nodes':list(range(len(parts)))}],
      'nodes':[{'name':n,'mesh':m,'translation':p,'scale':s} for n,p,s,m in parts],
      'materials':[{'name':n,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':.12,'roughnessFactor':.65}} for n,c in materials],
      'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1},'indices':2,'material':i}]} for i in range(3)],
      'buffers':[{'byteLength':len(blob),'uri':'data:application/octet-stream;base64,'+base64.b64encode(blob).decode()}],
      'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':288},{'buffer':0,'byteOffset':288,'byteLength':288},{'buffer':0,'byteOffset':576,'byteLength':72}],
      'accessors':[{'bufferView':0,'componentType':5126,'count':24,'type':'VEC3','min':[-.5]*3,'max':[.5]*3},{'bufferView':1,'componentType':5126,'count':24,'type':'VEC3'},{'bufferView':2,'componentType':5123,'count':36,'type':'SCALAR'}]}
put('assets/robot/robot_practica.gltf',json.dumps(gltf,indent=2))
put('assets/robot/LICENSE.txt','Original procedural practice asset created for this project, 2026-09-26.\nReleased under CC0 1.0 Universal: https://creativecommons.org/publicdomain/zero/1.0/\nNo Tripo/Meshy output; no third-party model or textures.\n')
put('scenes/robot_visual.tscn','''[gd_scene load_steps=2 format=3]
[ext_resource type="PackedScene" path="res://assets/robot/robot_practica.gltf" id="1"]
[node name="RobotVisual" type="Node3D"]
[node name="ImportedModel" parent="." instance=ExtResource("1")]
''')
put('scenes/player.tscn','''[gd_scene load_steps=6 format=3]
[ext_resource type="Script" path="res://scripts/player.gd" id="1"]
[ext_resource type="PackedScene" path="res://scenes/robot_visual.tscn" id="2"]
[ext_resource type="Script" path="res://scripts/camera_rig.gd" id="3"]
[sub_resource type="CapsuleShape3D" id="Body"]
radius = 0.42
height = 1.8
[sub_resource type="SphereShape3D" id="CameraShape"]
radius = 0.22
[node name="Player" type="CharacterBody3D"]
collision_layer = 2
collision_mask = 1
floor_snap_length = 0.25
script = ExtResource("1")
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
position = Vector3(0, 0.9, 0)
shape = SubResource("Body")
[node name="Visual" parent="." instance=ExtResource("2")]
[node name="CameraRig" type="Node3D" parent="."]
position = Vector3(0, 1.35, 0)
script = ExtResource("3")
[node name="Pitch" type="Node3D" parent="CameraRig"]
rotation = Vector3(-0.32, 0, 0)
[node name="SpringArm3D" type="SpringArm3D" parent="CameraRig/Pitch"]
spring_length = 5.5
margin = 0.15
collision_mask = 1
shape = SubResource("CameraShape")
[node name="Camera3D" type="Camera3D" parent="CameraRig/Pitch/SpringArm3D"]
current = true
fov = 65.0
near = 0.08
''')
level=['''[gd_scene format=3]
[ext_resource type="PackedScene" path="res://scenes/player.tscn" id="1"]
[ext_resource type="Script" path="res://scripts/level.gd" id="2"]
[sub_resource type="ProceduralSkyMaterial" id="SkyMat"]
sky_top_color = Color(0.08, 0.19, 0.32, 1)
sky_horizon_color = Color(0.65, 0.79, 0.82, 1)
ground_bottom_color = Color(0.12, 0.17, 0.22, 1)
[sub_resource type="Sky" id="Sky"]
sky_material = SubResource("SkyMat")
[sub_resource type="Environment" id="Env"]
background_mode = 2
sky = SubResource("Sky")
ambient_light_source = 3
ambient_light_color = Color(0.7, 0.83, 1, 1)
ambient_light_energy = 0.55
tonemap_mode = 2
''']
boxes=[('Suelo',(0,-.5,0),(28,1,28),(.17,.24,.29)),('ParedN',(0,2,-14),(28,4,.5),(.28,.4,.45)),('ParedE',(14,2,0),(.5,4,28),(.28,.4,.45)),('ParedS',(0,2,14),(28,4,.5),(.28,.4,.45)),('ParedW',(-14,2,0),(.5,4,28),(.28,.4,.45)),('CuboSalto',(-3,.45,-2),(2,.9,2),(.85,.43,.15)),('BloqueAlto',(2,1,-5),(2,2,2),(.16,.57,.56)),('EsquinaA',(6,1.5,1),(.6,3,6),(.35,.47,.63)),('EsquinaB',(8,1.5,-2),(4,3,.6),(.35,.47,.63)),('Escalon1',(-7,.2,-5),(2,.4,2),(.85,.43,.15)),('Escalon2',(-7,.4,-7),(2,.8,2),(.85,.43,.15)),('Escalon3',(-7,.65,-9),(2,1.3,2),(.85,.43,.15))]
v=lambda p:', '.join(map(str,p))
for i,(n,p,s,c) in enumerate(boxes):
    level.append(f'''[sub_resource type="BoxShape3D" id="Shape{i}"]
size = Vector3({v(s)})
[sub_resource type="StandardMaterial3D" id="Mat{i}"]
albedo_color = Color({v(c)}, 1)
roughness = 0.85
[sub_resource type="BoxMesh" id="Mesh{i}"]
size = Vector3({v(s)})
material = SubResource("Mat{i}")
''')
level.append('''[node name="Laboratorio" type="Node3D"]
script = ExtResource("2")
[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Env")
[node name="Sun" type="DirectionalLight3D" parent="."]
rotation_degrees = Vector3(-55, -32, 0)
light_color = Color(1, 0.91, 0.78, 1)
light_energy = 1.3
shadow_enabled = true
directional_shadow_max_distance = 70.0
''')
for i,(n,p,s,c) in enumerate(boxes):
    level.append(f'''[node name="{n}" type="StaticBody3D" parent="."]
position = Vector3({v(p)})
[node name="Collision" type="CollisionShape3D" parent="{n}"]
shape = SubResource("Shape{i}")
[node name="Mesh" type="MeshInstance3D" parent="{n}"]
mesh = SubResource("Mesh{i}")
''')
for i in range(-12,14,2):
    # Thin stripes are decorative, never colliders.
    for axis in range(2):
        size=(.018,.006,27) if axis==0 else (27,.006,.018)
        pos=(i,.006,0) if axis==0 else (0,.006,i)
        # Resources must precede nodes: append declarations to initial resource section.
        level.insert(1,f'[sub_resource type="BoxMesh" id="Grid{i+12}_{axis}"]\nsize = Vector3({v(size)})\n')
        level.append(f'[node name="Grid{i+12}_{axis}" type="MeshInstance3D" parent="."]\nposition = Vector3({v(pos)})\nmesh = SubResource("Grid{i+12}_{axis}")\n')
level.append('''[node name="Player" parent="." instance=ExtResource("1")]
position = Vector3(0, 0.05, 6)
[node name="HUD" type="CanvasLayer" parent="."]
[node name="Panel" type="ColorRect" parent="HUD"]
offset_left = 22.0
offset_top = 22.0
offset_right = 440.0
offset_bottom = 193.0
color = Color(0.025, 0.05, 0.08, 0.9)
mouse_filter = 2
[node name="Title" type="Label" parent="HUD"]
offset_left = 38.0
offset_top = 30.0
theme_override_colors/font_color = Color(0.31, 0.91, 0.78, 1)
theme_override_font_sizes/font_size = 25
text = "KINETIC / LAB 01"
[node name="Status" type="Label" parent="HUD"]
offset_left = 38.0
offset_top = 66.0
theme_override_font_sizes/font_size = 17
[node name="Help" type="Label" parent="HUD"]
offset_left = 38.0
offset_top = 128.0
theme_override_font_sizes/font_size = 15
text = "WASD mover · Espacio saltar · R reiniciar\nRatón / flechas: cámara · Esc: liberar ratón\nF: 30 / 144 FPS · clic: capturar ratón"
[node name="Caption" type="Label" parent="HUD"]
offset_left = 30.0
offset_top = 630.0
theme_override_colors/font_shadow_color = Color(0, 0, 0, 1)
theme_override_constants/shadow_offset_x = 2
theme_override_constants/shadow_offset_y = 2
theme_override_font_sizes/font_size = 24
text = "01 / MOVIMIENTO, FISICA Y APARIENCIA"
''')
put('scenes/level.tscn','\n'.join(level))
put('node_3d.tscn','''[gd_scene load_steps=2 format=3]
[ext_resource type="PackedScene" path="res://scenes/level.tscn" id="1"]
[node name="Nivel" instance=ExtResource("1")]
''')
print('Generated robot: 132 triangles, 3 materials, 0 textures; editable level.')

