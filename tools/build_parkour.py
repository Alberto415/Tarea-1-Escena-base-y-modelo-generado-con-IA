"""Original scene-native art for SKYLINE. Rebuilds only the new parkour assets."""
from pathlib import Path
import math, random
R=Path(__file__).resolve().parents[1]
class Scene:
    def __init__(self): self.resources=[]; self.nodes=[]; self.i=0
    def resource(self,kind,props):
        self.i+=1; rid=f'r{self.i}'
        self.resources.append(f'[sub_resource type="{kind}" id="{rid}"]\n{props}\n')
        return f'SubResource("{rid}")'
    def node(self,name,kind,parent=None,props='',instance=None):
        head=f'[node name="{name}"'
        if kind: head+=f' type="{kind}"'
        if parent is not None: head+=f' parent="{parent}"'
        if instance: head+=f' instance={instance}'
        self.nodes.append(head+']\n'+props+'\n')
    def save(self,path,external=''):
        (R/path).write_text('[gd_scene format=3]\n'+external+'\n'+'\n'.join(self.resources+self.nodes),encoding='utf-8')
    def material(self,c,metal=0,rough=.7,emission=None):
        c=', '.join(str(float(v)) for v in c.split(','))
        if emission: emission=', '.join(str(float(v)) for v in emission.split(','))
        p=f'albedo_color = Color({c}, 1)\nmetallic = {metal}\nroughness = {rough}'
        if emission: p+=f'\nemission_enabled = true\nemission = Color({emission}, 1)\nemission_energy_multiplier = 1.6'
        return self.resource('StandardMaterial3D',p)
    def box(self,size,mat): return self.resource('BoxMesh',f'size = {vec(size)}\nmaterial = {mat}')
    def cylinder(self,r,h,mat,r2=None,sides=32):
        return self.resource('CylinderMesh',f'top_radius = {r}\nbottom_radius = {r if r2 is None else r2}\nheight = {h}\nradial_segments = {sides}\nmaterial = {mat}')
    def sphere(self,r,mat): return self.resource('SphereMesh',f'radius = {r}\nheight = {r*2}\nradial_segments = 24\nrings = 12\nmaterial = {mat}')
    def mesh(self,name,parent,mesh,pos=(0,0,0),extra=''):
        self.node(name,'MeshInstance3D',parent,f'position = {vec(pos)}\nmesh = {mesh}\n'+extra)
def vec(v): return 'Vector3('+', '.join(str(round(x,5)) for x in v)+')'

# Courier model: independent editable pivot hierarchy, no movement/physics code.
s=Scene()
cream=s.material('.87, .91, .84',.1,.4)
navy=s.material('.045, .08, .13',.3,.3)
orange=s.material('1, .24, .07',.05,.55)
cyan=s.material('.08, .8, .86',.2,.25,'.08, .75, .9')
visor=s.material('.025, .085, .13',.7,.18)
s.node('CourierVisual','Node3D',props='script = ExtResource("anim")')
s.node('Body','Node3D','.')
s.mesh('Torso','Body',s.resource('CapsuleMesh',f'radius = 0.29\nheight = 0.67\nmaterial = {cream}'),(0,1.03,0),'scale = Vector3(1, 1, 0.72)')
s.mesh('ChestPlate','Body',s.box((.39,.3,.08),navy),(0,1.09,-.20))
s.mesh('ChestLight','Body',s.box((.20,.035,.025),cyan),(0,1.14,-.255))
s.mesh('Belt','Body',s.box((.49,.105,.36),orange),(0,.79,0))
s.mesh('Helmet','Body',s.sphere(.34,cream),(0,1.57,0),'scale = Vector3(1, 0.91, 0.9)')
s.mesh('FaceVisor','Body',s.sphere(.278,visor),(0,1.56,-.09),'scale = Vector3(1, 0.62, 0.91)')
for x in [-.105,.105]: s.mesh('EyeL' if x<0 else 'EyeR','Body',s.box((.075,.038,.018),cyan),(x,1.57,-.346))
s.mesh('HelmetStripe','Body',s.box((.10,.055,.39),orange),(0,1.867,-.01))
s.mesh('EarL','Body',s.cylinder(.095,.065,orange),(-.34,1.56,0),'rotation_degrees = Vector3(0, 0, 90)')
s.mesh('EarR','Body',s.cylinder(.095,.065,orange),(.34,1.56,0),'rotation_degrees = Vector3(0, 0, 90)')
s.mesh('Backpack','Body',s.box((.39,.42,.20),navy),(0,1.10,.24))
for x in [-.115,.115]: s.mesh('CellL' if x<0 else 'CellR','Body',s.cylinder(.065,.30,cyan),(x,1.10,.37))
s.mesh('ScarfCollar','Body',s.cylinder(.20,.09,orange),(0,1.36,0))
s.node('Scarf','Node3D','Body','position = Vector3(0.12, 1.35, 0.14)')
s.mesh('Fabric','Body/Scarf',s.box((.18,.035,.52),orange),(0,-.08,.21),'rotation_degrees = Vector3(16, -12, 0)')
for side,sign in [('Left',-1),('Right',1)]:
    s.node(side+'Arm','Node3D','Body',f'position = Vector3({sign*.37}, 1.23, 0)')
    path='Body/'+side+'Arm'
    s.mesh('Shoulder',path,s.sphere(.13,orange))
    s.mesh('Sleeve',path,s.resource('CapsuleMesh',f'radius = 0.092\nheight = 0.38\nmaterial = {cream}'),(0,-.19,0))
    s.mesh('Glove',path,s.sphere(.11,navy),(0,-.40,-.015))
    s.node(side+'Leg','Node3D','Body',f'position = Vector3({sign*.15}, 0.73, 0)')
    path='Body/'+side+'Leg'
    s.mesh('Trouser',path,s.resource('CapsuleMesh',f'radius = 0.112\nheight = 0.51\nmaterial = {navy}'),(0,-.25,0))
    s.mesh('Kneepad',path,s.box((.18,.14,.08),orange),(0,-.31,-.10))
    s.mesh('Shoe',path,s.box((.235,.16,.36),cream),(0,-.61,-.055))
    s.mesh('Sole',path,s.box((.24,.045,.365),orange),(0,-.68,-.055))
s.save('scenes/courier_visual.tscn','[ext_resource type="Script" path="res://scripts/courier_visual.gd" id="anim"]')

# Floating rooftop parkour: all platforms and set dressing are saved editor nodes.
s=Scene()
stone=s.material('.17, .23, .29',.2,.65)
top=s.material('.35, .44, .45',.1,.85)
edge=s.material('.10, .70, .72',.25,.4,'.04, .42, .48')
gold=s.material('1, .38, .10',.3,.45,'1, .18, .035')
dark=s.material('.075, .11, .18',.15,.8)
white=s.material('.81, .87, .78',.05,.8)
leaf=s.material('.15, .37, .32',0,1)
leaflight=s.material('.26, .52, .39',0,1)
trunk=s.material('.21, .15, .15',0,1)
s.node('Skyline','Node3D',props='script = ExtResource("level")')
sky_mat=s.resource('ProceduralSkyMaterial','sky_top_color = Color(0.13, 0.22, 0.38, 1)\nsky_horizon_color = Color(0.94, 0.61, 0.46, 1)\nground_bottom_color = Color(0.09, 0.13, 0.23, 1)\nground_horizon_color = Color(0.76, 0.48, 0.43, 1)\nsky_curve = 0.22')
sky=s.resource('Sky',f'sky_material = {sky_mat}')
env=s.resource('Environment',f'background_mode = 2\nsky = {sky}\nambient_light_source = 3\nambient_light_color = Color(0.63, 0.74, 1, 1)\nambient_light_energy = 0.55\ntonemap_mode = 2\nfog_enabled = true\nfog_light_color = Color(0.52, 0.44, 0.54, 1)\nfog_density = 0.006\nfog_sky_affect = 0.18')
s.node('Environment','WorldEnvironment','.',f'environment = {env}')
s.node('Sun','DirectionalLight3D','.','rotation_degrees = Vector3(-28, -38, 0)\nlight_color = Color(1, 0.71, 0.49, 1)\nlight_energy = 1.5\nshadow_enabled = true\ndirectional_shadow_max_distance = 110.0')
s.node('Fill','DirectionalLight3D','.','rotation_degrees = Vector3(-50, 145, 0)\nlight_color = Color(0.37, 0.65, 1, 1)\nlight_energy = 0.45')
sunmat=s.material('1, .69, .36',emission='1, .54, .2')
s.mesh('SunDisc','.',s.sphere(9,sunmat),(-40,19,-115))
s.node('Platforms','Node3D','.')
# Centers and radii ensure gaps within jump reach at 6 m/s, 9 m/s jump impulse.
route=[(0,0,4,3.5),(0,.4,-2,1.7),(2,.85,-6.5,1.65),(-.5,1.3,-11,1.7),
       (-3,1.7,-16,3),(-6,2.1,-21.5,1.7),(-3.5,2.55,-26,1.6),(1,3,-28.5,1.7),
       (5,3.4,-33,3),(8,3.85,-38.5,1.65),(5,4.3,-43,1.65),(1,4.75,-46.5,1.65),
       (-2,5.2,-51.5,3),(-5,5.6,-57,1.8),(-1.5,6,-61.5,2),(2,6.4,-67,3.5)]
checkpoints=[0,4,8,12,15]
for i,(x,y,z,r) in enumerate(route):
    n=f'Roof{i:02}'; path='Platforms/'+n
    s.node(n,'StaticBody3D','Platforms',f'position = {vec((x,y-.35,z))}\ncollision_layer = 1\ncollision_mask = 2')
    rectangular = i in [2, 5, 7, 10, 13]
    width = r * 1.65
    shape=s.resource('BoxShape3D',f'size = {vec((width,.7,r*2))}') if rectangular else s.resource('CylinderShape3D',f'radius = {r}\nheight = 0.7')
    s.node('Collision','CollisionShape3D',path,f'shape = {shape}')
    s.mesh('Deck',path,s.box((width,.7,r*2),stone) if rectangular else s.cylinder(r,.7,stone,r*.92,sides=48))
    s.mesh('Rim',path,s.box((width+.04,.075,r*2+.04),edge) if rectangular else s.cylinder(r+.025,.075,gold if i in checkpoints else edge,sides=48),(0,.285,0))
    s.mesh('Surface',path,s.box((width-.16,.09,r*2-.16),top) if rectangular else s.cylinder(r-.12,.09,top,sides=48),(0,.315,0))
    s.mesh('Base',path,s.cylinder(r*.85,.45,dark,r*.61,sides=12),(0,-.57,0))
    s.mesh('Core',path,s.cylinder(.45,1.8,stone,.21,sides=8),(0,-1.5,0))
    for j in range(4):
        a=j*math.pi/2
        s.mesh(f'Panel{j}',path,s.box((.12,.02,.62),white),(math.sin(a)*r*.67,.372,math.cos(a)*r*.67),f'rotation = Vector3(0, {a}, 0)')
    s.node('Number','Label3D',path,f'position = Vector3(0, 0.385, 0)\nrotation_degrees = Vector3(-90, 0, 0)\ntext = "{i+1:02}"\nfont_size = 120\npixel_size = 0.006\nmodulate = Color(0.72, 0.86, 0.82, 1)\noutline_size = 0')
    if i>0:
        s.node('Crystal','Area3D',path,f'position = Vector3(0, 1.40, 0)\ncollision_layer = 0\ncollision_mask = 2\nscript = ExtResource("pickup")\nindex = {i}')
        col=s.resource('SphereShape3D','radius = 1.15')
        s.node('Collision','CollisionShape3D',path+'/Crystal',f'shape = {col}')
        s.node('Gem','Node3D',path+'/Crystal','rotation_degrees = Vector3(0, 45, 0)')
        s.mesh('Upper',path+'/Crystal/Gem',s.cylinder(0,.30,gold,.19,sides=4),(0,.15,0))
        s.mesh('Lower',path+'/Crystal/Gem',s.cylinder(.19,.30,gold,0,sides=4),(0,-.15,0))
    if i in checkpoints:
        idx=checkpoints.index(i)
        # Side beacon leaves the landing area free.
        for side in [-1,1]:
            s.mesh(f'Post{side}',path,s.box((.16,2.9,.20),dark),(side*(r-.5),1.79,-.45))
            s.mesh(f'Light{side}',path,s.box((.055,2.3,.055),edge),(side*(r-.5),1.9,-.58))
        s.mesh('Gate',path,s.box((2*(r-.5)+.16,.20,.2),gold),(0,3.2,-.45))
        label='SALIDA' if i==0 else ('META' if i==15 else f'CHECKPOINT {idx}')
        s.node('Sign','Label3D',path,f'position = Vector3(0, 3.6, -0.45)\ntext = "{label}"\nfont_size = 58\npixel_size = 0.007\nmodulate = Color(1, 0.79, 0.53, 1)\nbillboard = 1\nvisibility_range_end = 20.0')
        # Small garden behind the edge; no invisible decorative obstacle on the route.
        s.mesh('Planter',path,s.box((.8,.4,.8),white),(r-.7,.56,.9))
        s.mesh('TreeTrunk',path,s.cylinder(.08,1.1,trunk),(r-.7,1.15,.9))
        for j in range(3):
            s.mesh(f'Foliage{j}',path,s.sphere(.46-j*.07,leaflight if j%2 else leaf),(r-.7+(.14 if j%2 else -.09),1.65+j*.34,.9), 'scale = Vector3(1, 0.85, 1)')
    # Dotted aerial line shows the route, stays well below the feet.
    if i<len(route)-1:
        b=route[i+1]
        for j in range(1,7):
            t=j/7
            p=(x+(b[0]-x)*t, y+(b[1]-y)*t-.12,z+(b[2]-z)*t)
            s.mesh(f'Route{i}_{j}','.',s.sphere(.035,edge),p)

# Distant city: intentional silhouettes, warm windows and rooftop antennae.
s.node('City','Node3D','.')
rng=random.Random(17)
building_mats=[s.material(c,.15,.9) for c in ['.13, .17, .26','.19, .21, .31','.24, .24, .33','.28, .28, .35']]
window=s.material('.81, .59, .35',emission='.38, .21, .08')
for i in range(64):
    side=-1 if i%2 else 1
    x=side*rng.uniform(18,70); z=rng.uniform(-110,24); h=rng.uniform(10,36); w=rng.uniform(3,8)
    y=-23+h/2
    s.mesh(f'Tower{i}','City',s.box((w,h,w*.8),building_mats[i%4]),(x,y,z))
    s.mesh(f'RoofCap{i}','City',s.box((w+.2,.22,w*.8+.2),dark),(x,y+h/2,z))
    for j in range(int(h/3)):
        s.mesh(f'Window{i}_{j}','City',s.box((w*.7,.07,.02),window),(x,-21+j*3,z+w*.4+.015))
    if i%5==0: s.mesh(f'Antenna{i}','City',s.cylinder(.045,3,edge),(x,y+h/2+1.5,z))

s.node('Player',None,'.','position = Vector3(0, 0.08, 4)\nspeed = 6.0\njump_speed = 9.0', 'ExtResource("player")')
s.node('HUD','CanvasLayer','.','script = ExtResource("hud")')
s.save('scenes/parkour.tscn','''[ext_resource type="Script" path="res://scripts/parkour.gd" id="level"]
[ext_resource type="PackedScene" path="res://scenes/courier_player.tscn" id="player"]
[ext_resource type="Script" path="res://scripts/crystal.gd" id="pickup"]
[ext_resource type="Script" path="res://scripts/parkour_hud.gd" id="hud"]''')

source=(R/'scenes/player.tscn').read_text(encoding='utf-8-sig')
source=source.replace('res://scenes/robot_visual.tscn','res://scenes/courier_visual.tscn').replace('spring_length = 5.5','spring_length = 6.0').replace('fov = 65.0','fov = 72.0')
(R/'scenes/courier_player.tscn').write_text(source,encoding='utf-8')
(R/'assets/parkour').mkdir(exist_ok=True)
(R/'assets/parkour/route.json').write_text(__import__('json').dumps(route))
(R/'assets/parkour/route.gd').write_text('extends RefCounted\nconst POINTS: Array = '+__import__('json').dumps(route)+'\n',encoding='utf-8')
print('Built SKYLINE: 16 rooftops, 15 crystals, 3 checkpoints, procedural courier and city.')
