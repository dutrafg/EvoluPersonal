#!/usr/bin/env python3
"""Pré-visualizações geométricas VTK por exercício MD500, blocos 4–6.
Produz mídia provisória, não aprovada biomecanicamente. Não altera catálogo.
Uso: xvfb-run -a python3 scripts/render_md500_blocos_04_06.py --block 4
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_md500_bloco01 import Scene

BLOCKS = {
 4: [(350,"Cuban Press"),(372,"Rosca na Máquina"),(381,"Rosca Inclinada na Polia Baixa"),(396,"Pronação e Supinação de Antebraço"),(397,"Flexão Radial e Ulnar do Punho")],
 5: [(412,"Rolling Triceps Extension"),(413,"JM Press"),(414,"California Press"),(415,"Tate Press"),(421,"Paralelas no Gravitron")],
 6: [(427,"Tríceps Francês Sentado na Máquina"),(428,"PJR Pullover"),(432,"Tríceps Cruzado no Cabo"),(436,"Tríceps Coice na Polia"),(437,"Tríceps Sentado na Máquina")]
}
FRAMES=18
A=np.array
def jbase(hip=(0,0,1.14),sho=(.01,0,1.75),seated=False):
 h=A(hip,dtype=float); s=A(sho,dtype=float)
 knee=A([.1,0,.70]); ankle=A([.11,0,.17])
 if seated:knee=A([.57,0,.67]);ankle=A([.67,0,.16])
 j={'hip':h,'shoulder':s}
 for sign,sd in [(-1,"L"),(1,"R")]:
  y=.17*sign
  j['knee'+sd]=knee+A([0,y,0])
  j['ankle'+sd]=ankle+A([0,y,0])
  j['elbow'+sd]=s+A([.10,sign*.27,-.22])
  j['hand'+sd]=s+A([.16,sign*.29,-.49])
 return j
def seat(s,x=-.22,z=.75,back=True):
 s.box((x,0,z),(.63,.68,.15),'pad',True)
 s.bar((x,-.24,.05),(x,-.24,z-.05),.07,'metal')
 s.bar((x,.24,.05),(x,.24,z-.05),.07,'metal')
 if back:
  s.box((x-.32,0,z+.39),(.14,.68,.77),'pad',True)
def bench(s,x=0,z=.69):
 s.box((x,0,z),(1.80,.72,.16),'pad',True)
 for px in (-.65,.65):
  for py in (-.22,.22):s.bar((px,py,.12),(px,py,z-.08),.055,'metal')
def cable(s,positions):
 for x,y in positions:
  s.bar((x,y,.07),(x,y,2.45),.071,'metal')
  s.sphere((x,y,2.32),.11,'steel')
  s.box((x,y,.22),(.32,.30,.18),'metal2',True)
def joint(s,j,side,el,ha):
 j['elbow'+side]=A(el,dtype=float);j['hand'+side]=A(ha,dtype=float)
def dumbbell(s,hand,angle=0):
 p=A(hand);v=A([.02, .18*math.cos(angle), .18*math.sin(angle)])
 s.bar(p-v,p+v,.046,'metal2')
 for pt in (p-v,p+v):s.sphere(pt,.096,'steel',scale=(.65,1,.9))
def barbell(s,p,z=None):
 p=A(p)
 s.bar(p+A([0,-.75,0]),p+A([0,.75,0]),.042,'steel')
 for y in (-.69,.69):s.sphere(p+A([0,y,0]),.15,'metal2')
def pose(s,md,t):
 q=(1-math.cos(2*math.pi*t))/2
 j=jbase()
 s.cam.SetPosition(3.95,6.4,2.7)
 if md==350: # Cuban press: upright row -> external rotation -> overhead press
  s.cam.SetPosition(3.4,6.4,2.75)
  phase=q*3
  for sign,side in [(-1,'L'),(1,'R')]:
   y=sign*.41
   if phase<1:
    u=phase; el=[.17,y,1.48+.42*u];ha=[.19,y,1.23+.48*u]
   elif phase<2:
    u=phase-1; el=[.17,y,1.90];ha=[.19,y,1.71+.46*u]
   else:
    u=phase-2;el=[.17,y,1.90+.28*u];ha=[.19,y,2.17+.45*u]
   joint(s,j,side,el,ha)
  s.person(j,active=('shoulders',))
  for side in ('L','R'):dumbbell(s,j['hand'+side])
 elif md==372: # biceps machine seated, arms horizontal on support
  seat(s, -.1,.76,True);s.cam.SetPosition(4.0,5.8,2.55)
  s.box((.40,0,1.12),(.42,.90,.17),'pad',True)
  s.bar((.62,-.45,.12),(.62,-.45,1.35),.07,'metal')
  j=jbase(hip=(-.18,0,.87),sho=(-.29,0,1.45),seated=True)
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.24*sign; el=[.36,y,1.30]; ha=[.78-.20*q,y,1.13+.47*q]
   joint(s,j,sd,el,ha)
  s.person(j,active=('biceps',))
  for sd in ('L','R'):
   s.sphere(j['hand'+sd],.08,'steel')
  s.bar((.7,-.39,.73),(.7,.39,.73),.045,'metal')
 elif md==381: # incline cable curl, arms behind torso
  s.cam.SetPosition(4.6,5.9,2.6)
  seat(s,-.08,.74,True)
  # angled backrest to keep torso inclined
  s.bar((-.46,-.32,.64),(-.74,-.32,1.55),.09,'metal')
  s.bar((-.46,.32,.64),(-.74,.32,1.55),.09,'metal')
  cable(s,[(1.37,-.55),(1.37,.55)])
  j=jbase(hip=(-.34,0,.90),sho=(-.68,0,1.48),seated=True)
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.27*sign;el=[-.63,y,1.20];ha=[-.36+.20*q,y,1.03+.40*q]
   joint(s,j,sd,el,ha)
  s.person(j,active=('biceps',))
  for sd,y in [('L',-.55),('R',.55)]:
   s.bar((1.37,y,.27),j['hand'+sd],.007,'steel')
 elif md==396: # seated/standing forearm pronation-supination
  s.cam.SetPosition(3.0,6.0,3.0)
  seat(s,-.2,.72,False)
  j=jbase(hip=(-.25,0,.85),sho=(-.24,0,1.47),seated=True)
  joint(s,j,'L',[.04,-.29,1.26],[.42,-.29,1.25])
  joint(s,j,'R',[.04,.29,1.26],[.42,.29,1.25])
  s.person(j,active=('forearm',))
  a=q*math.pi
  p=j['handR'];axis=A([.05,.27*math.cos(a),.27*math.sin(a)])
  s.bar(p-axis,p+axis,.035,'metal2')
  s.sphere(p-axis,.12,'steel',scale=(.72,.9,.8))
  s.sphere(p+axis,.12,'steel',scale=(.72,.9,.8))
 elif md==397: # radial-ulnar wrist deviation, hammer in hand
  s.cam.SetPosition(3.5,6.1,2.85)
  j=jbase()
  joint(s,j,'R',[.17,.26,1.43],[.29+.11*q,.27,1.14+.16*q])
  joint(s,j,'L',[.17,-.26,1.43],[.29,-.27,1.12])
  s.person(j,active=('forearm',))
  p=j['handR']; v=A([.12*math.cos((q-.5)*1.5),.04,.31*math.sin((q-.5)*1.5)+.10])
  s.bar(p,p+v,.043,'metal2');s.sphere(p+v,.11,'steel')
 elif md in (412,413,414,415,428): # supine press/extension variation
  s.cam.SetPosition(3.45,6.4,2.25)
  bench(s,-.12,.69)
  j=jbase(hip=(.12,0,.94),sho=(-.60,0,.97),seated=True)
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.25*sign
   if md==412:
    el=[-.37,y,1.35+.15*q];ha=[-.24-.34*q,y,1.73-.33*q]
   elif md==413:
    el=[-.28,y,1.30+.28*q];ha=[-.20+.10*q,y,1.79-.42*q]
   elif md==414:
    el=[-.27,y,1.20+.30*q];ha=[-.05+.21*q,y,1.72-.45*q]
   elif md==415:
    el=[-.38,sign*.50,1.42];ha=[-.15,sign*(.44-.26*q),1.75-.34*q]
   else:
    el=[-.78,y,1.31];ha=[-.91-.32*q,y,1.60-.22*q]
   joint(s,j,sd,el,ha)
  s.person(j,active=('triceps',))
  if md==415:
   for sd in ('L','R'):dumbbell(s,j['hand'+sd])
  elif md==428:
   p=(j['handL']+j['handR'])/2
   dumbbell(s,p)
  else:
   p=(j['handL']+j['handR'])/2
   barbell(s,p)
 elif md==421: # assisted parallel dips on counterweight knee pad
  s.cam.SetPosition(3.9,6.1,2.9)
  s.box((0,0,.10),(1.5,1.2,.17),'metal2',True)
  for y in (-.37,.37):
   s.bar((.20,y,.12),(.20,y,1.66),.065,'metal')
   s.bar((.20,y,1.66),(.75,y,1.66),.048,'steel')
  s.box((.18,0,.78+.19*q),(.65,.43,.13),'pad',True)
  j=jbase(hip=(.0,0,1.42-.18*q),sho=(0,0,2.03-.18*q))
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.38*sign
   joint(s,j,sd,[.23,sign*.41,1.81-.21*q],[.57,y,1.66])
   j['knee'+sd]=A([.12,sign*.18,1.06-.15*q])
   j['ankle'+sd]=A([-.19,sign*.18,.84-.18*q])
  s.person(j,active=('triceps',))
 elif md==427: # French seated on dedicated triceps machine
  s.cam.SetPosition(4,5.9,2.65)
  seat(s,-.2,.73,True)
  for y in (-.56,.56):
   s.bar((.72,y,.10),(.72,y,2.44),.07,'metal')
  s.box((.2,0,1.63),(.33,.72,.17),'pad',True)
  j=jbase(hip=(-.2,0,.86),sho=(-.23,0,1.49),seated=True)
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.22*sign;j['elbow'+sd]=A([-.1,y,2.01]);j['hand'+sd]=A([.21+.24*q,y,1.82+.42*q])
  s.person(j,active=('triceps',))
  s.bar(j['handL'],j['handR'],.053,'steel')
  s.bar((.72,0,2.25),(j['handL']+j['handR'])/2,.055,'metal')
 elif md==432: # cross-body cable triceps
  s.cam.SetPosition(3.55,6.5,2.85)
  cable(s,[(1.22,-.89),(1.22,.89)])
  j=jbase()
  for sign,sd in [(-1,'L'),(1,'R')]:
   joint(s,j,sd,[.24,sign*.23,1.53],[.30+.40*q,(-sign)*(.08+.24*q),1.22+.18*q])
  s.person(j,active=('triceps',))
  for sd,y in [('L',.89),('R',-.89)]:
   s.bar((1.22,y,2.30),j['hand'+sd],.008,'steel')
 elif md==436: # triceps cable kickback, torso 45 degrees
  s.cam.SetPosition(4.3,5.8,2.7)
  cable(s,[(1.15,-.47)])
  j=jbase(hip=(-.22,0,1.12),sho=(.28,0,1.48))
  joint(s,j,'L',[.52,-.25,1.22],[.52+.49*q,-.25,1.12+.12*q])
  joint(s,j,'R',[.51,.25,1.22],[.78,.25,1.00])
  s.person(j,active=('triceps',))
  s.bar((1.15,-.47,.22),j['handL'],.008,'steel')
 elif md==437: # seated triceps pushdown machine, inverse Scott support
  s.cam.SetPosition(4.1,5.9,2.7)
  seat(s,-.30,.76,True)
  s.box((.37,0,1.15),(.60,.90,.22),'pad',True)
  for y in (-.45,.45):s.bar((.79,y,.12),(.79,y,1.47),.07,'metal')
  j=jbase(hip=(-.31,0,.87),sho=(-.34,0,1.49),seated=True)
  for sign,sd in [(-1,'L'),(1,'R')]:
   y=.24*sign
   joint(s,j,sd,[.24,y,1.28],[.49+.28*q,y,1.07-.35*q])
  s.person(j,active=('triceps',))
  s.bar(j['handL'],j['handR'],.05,'steel')
 else:raise ValueError("MD não implementado: "+str(md))
def main():
 p=argparse.ArgumentParser();p.add_argument('--block',type=int,required=True,choices=(4,5,6));args=p.parse_args()
 block=args.block
 output=Path('production/revisoes-md500-3d')/('bloco%02d'%block)
 output.mkdir(parents=True,exist_ok=True)
 # Validate that all requested MDs are genuinely missing official animation.
 inventory=json.loads(Path('production/INVENTARIO_MD500.json').read_text(encoding='utf-8'))
 for md,_ in BLOCKS[block]:
  assert inventory[md-1]['id']==md and inventory[md-1]['animation_path'] is None, "ID já vinculado: "+str(md)
 results=[]
 for md,name in BLOCKS[block]:
  scene=Scene(name);frames=[]
  for n in range(FRAMES):
   scene.clear();pose(scene,md,n/FRAMES);frames.append(scene.screenshot())
  target=output/('md%d.gif'%md)
  frames[0].save(target,format='GIF',save_all=True,append_images=frames[1:],
                 duration=90,loop=0,disposal=2,optimize=False,colors=128)
  frames[4].save(output/('md%d_preview.png'%md))
  gif=Image.open(target)
  assert gif.size==(448,448) and gif.n_frames>=8,(md,gif.size,gif.n_frames)
  results.append({'id':md,'name':name,'frames':gif.n_frames,'size_bytes':target.stat().st_size,
                  'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                  'status':'geometric_3d_preview_not_approved',
                  'catalog_linked':False})
  print('MD',md,'frames',gif.n_frames,'bytes',target.stat().st_size,flush=True)
 (output/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Bloco %d: 5 GIFs de prévia, sem associação ao catálogo'%block)
if __name__=='__main__':main()
