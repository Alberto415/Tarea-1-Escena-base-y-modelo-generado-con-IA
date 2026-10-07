"""Create a portable archive and reimport/run it in a fresh temporary folder."""
from pathlib import Path
import json, zipfile, tempfile, subprocess, sys
R=Path(__file__).resolve().parents[1]
godot=sys.argv[1]
out=R/'output/Skyline_Alberto.zip'
def files():
    for p in R.rglob('*'):
        rel=p.relative_to(R)
        if not p.is_file() or any(x in ['.godot','.git','__pycache__'] for x in rel.parts): continue
        if p.suffix in ['.zip','.avi','.wav','.log','.pyc']: continue
        if p.name.startswith('pdf_') or (p.suffix=='.import' and 'output' in rel.parts): continue
        yield p,rel
def pack():
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p,rel in files(): z.write(p,rel)
pack()
if '--pack-only' in sys.argv:
    print('Repacked:',out)
    sys.exit(0)
clean=Path(tempfile.mkdtemp(prefix='kinetic_alberto_clean_'))
with zipfile.ZipFile(out) as z: z.extractall(clean)
commands=[['--headless','--path',str(clean),'--editor','--import','--quit'],['--headless','--path',str(clean),'res://scenes/level.tscn','--','--test'],['--headless','--path',str(clean),'--','--parkour-test']]
logs=[]
for command in commands:
    result=subprocess.run([godot]+command,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=100)
    logs.append({'args':command,'exit_code':result.returncode,'errors':[s for s in (result.stdout+result.stderr).splitlines() if 'ERROR' in s or 'FAIL' in s]})
    print(result.stdout[-1700:]); print(result.stderr[-1000:])
    if result.returncode or logs[-1]['errors']: raise RuntimeError('Clean copy validation failed')
report={'copy_path':str(clean),'excluded_cache':True,'checks':logs,'legacy_results':json.loads((clean/'output/evidence/results.json').read_text()),'parkour_results':json.loads((clean/'output/evidence/parkour_results.json').read_text()),'success':True}
(R/'output/evidence/skyline_clean_copy.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
pack()
print('Validated portable project:',out, out.stat().st_size,'bytes')
