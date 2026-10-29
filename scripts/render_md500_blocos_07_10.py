#!/usr/bin/env python3
"""Generate individual geometric VTK exercise previews for MD500 blocks 07–10.
Not final approved anatomical/biomechanical media. No catalog associations.
Run: xvfb-run -a python3 scripts/render_md500_blocos_07_10.py --block 7
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib,json,math,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_md500_bloco01 import Scene
A=np.array
N=18
BLOCKS={
 7:[(440,"Pin Press Fechado"),(451,"Panturrilha no V-Squat / Pendulo"),(456,"Panturrilha Agachado"),(457,"Caminhada na Ponta dos Pes com Halteres"),(459,"Elevacao Tibial com Barra Tibial")],
 8:[(468,"Abdominal no Banco Declinado"),(472,"Elevacao de Pernas na Cadeira Romana"),(474,"Abdominal Reverso no Banco Inclinado"),(477,"Abdominal GHD"),(478,"Abdominal Janda")],
 9:[(479,"Dragon Flag"),(480,"L-Sit"),(486,"Lenhador Baixo para Alto na Polia"),(487,"Lenhador Horizontal na Polia"),(489,"Rotacao de Tronco no Landmine")],
 10:[(490,"Elevar Pernas Oblíquas na Barra Fixa"),(492,"Flexao Lateral Banco Romano"),(494,"Prancha Dinamica na Bola Suica"),(495,"Prancha RKC"),(500,"Vacuum Abdominal")],
}
def sj(hip=(0,0,1.15),shoulder=(0,0,1.72),knee=(.08,0,.68),ankle=(.10,0,.14)):
 j={'hip':A(hip,dtype=float),'shoulder':A(shoulder,dtype=float)}
 for sign,side in [(-1,'L'),(1,'R')]:
  j['knee'+side]=A(knee,dtype=float)+A([0,sign*.17,0])
  j['ankle'+side]=A(ankle,dtype=float)+A([0,sign*.17,0])
  j['elbow'+side]=A(shoulder,dtype=float)+A([.12,sign*.22,-.22])
  j['hand'+side]=A(shoulder,dtype=float)+A([.22,sign*.24,-.48])
 return j
def arms(j,x,y,handz,elbowx=None,elbowz=None):
 for sign,side in [(-1,'L'),(1,'R')]:
  j['elbow'+side]=A([x-.13 if elbowx is None else elbowx,sign*y,handz-.20 if elbowz is None else elbowz])
  j['hand'+side]=A([x,sign*y,handz])
def figures(s,j,area="core"):
 # Unlike the generic scene.person(), active=() DOES NOT highlight legs.
 s.person(j,active=())
 if area in ('core','glutes','obliques'):
  s.bar(j['hip'],j['shoulder'],.135,'orange2')
 if area in ('calf','tibialis'):
  for sd in ('L','R'):
   s.bar(j['knee'+sd],j['ankle'+sd],.113,'orange')
 if area in ('triceps','shoulders'):
  for sign,sd in [(-1,'L'),(1,'R')]:
   sh=j['shoulder']+A([.01,sign*.15,0])
   s.bar(sh,j['elbow'+sd],.097,'orange')
   s.bar(j['elbow'+sd],j['hand'+sd],.072,'orange2')
def platform(s,height=.10):
 s.box((0,0,height*.5),(2.2,1.2,height),'metal2')
def bench(s,angle=0,center=(0,0,.79),length=1.85):
 x,y,z=center
 if angle==0:s.box(center,(length,.72,.16),'pad')
 else:
  xdelta=length/2*math.cos(angle);zdelta=length/2*math.sin(angle)
  for yy in (-.29,.29):s.bar((x-xdelta,yy,z-zdelta),(x+xdelta,yy,z+zdelta),.11,'pad')
 for xx in (x-.5,x+.5):
  for yy in (-.25,.25):s.bar((xx,yy,.06),(xx,yy,max(.14,z-.12)),.058,'metal')
def cage(s,x=.9):
 for yy in (-.53,.53):
  s.bar((x,yy,.07),(x,yy,2.65),.065,'metal')
  s.bar((x-.8,yy,.07),(x-.8,yy,2.3),.052,'metal')
 s.bar((x,-.54,2.55),(x,.54,2.55),.055,'steel')
def step_smith(s):
 cage(s,x=1.1)
 for yy in (-.54,.54):s.bar((.95,yy,.3),(.95,yy,2.1),.048,'steel')
def cable(s,level,x=1.32,y=-.7):
 s.bar((x,y,.09),(x,y,2.50),.073,'metal')
 s.sphere((x,y,level),.105,'steel')
 s.box((x,y,.25),(.27,.27,.16),'metal2')
 return A([x,y,level])
def dumbbell(s,p):
 p=A(p,dtype=float)
 s.bar(p+A([0,-.14,0]),p+A([0,.14,0]),.055,'steel')
 for yy in (-.14,.14):s.sphere(p+A([0,yy,0]),.11,'metal2')
def mat(s):
 s.box((0,0,.095),(2.65,1.4,.09),'pad')
def main_pose(s,md,t):
 # For explicitly static exercises q represents breathing/isometric tension.
 q=(1-math.cos(2*math.pi*t))/2
 s.cam.SetPosition(3.85,6.0,2.7)
 if md==440:
  bench(s,center=(-.15,0,.67));cage(s,x=.83)
  j=sj(hip=(.14,0,.92),shoulder=(-.52,0,.94),knee=(.56,0,.68),ankle=(.79,0,.12))
  arms(j,-.16,.17,1.48+.22*q,elbowx=-.34,elbowz=1.21+.17*q)
  figures(s,j,'triceps')
  p=(j['handL']+j['handR'])/2
  s.bar(p+A([0,-.69,0]),p+A([0,.69,0]),.047,'steel')
  for yy in (-.66,.66):s.sphere(p+A([0,yy,0]),.145,'metal2')
  for yy in (-.54,.54):s.bar((.15,yy,1.50),(.84,yy,1.50),.052,'metal')
 elif md==451:
  step_smith(s);platform(s,.22)
  # Raise heel while shoulder pads remain on the V-squat structure
  lift=.15*q
  j=sj(hip=(-.25,0,1.08+lift),shoulder=(-.25,0,1.73+lift),
    knee=(-.14,0,.66+lift*.42),ankle=(.02,0,.26+lift))
  figures(s,j,'calf')
  s.box((-.22,0,1.84+lift),(.44,.73,.17),'pad')
  for y in (-.36,.36):s.bar((1.08,y,2.26),(-.13,y,1.84+lift),.059,'metal')
 elif md==456:
  s.cam.SetPosition(3.0,6.8,2.65)
  j=sj(hip=(-.18,0,.76+.12*q),shoulder=(-.25,0,1.35+.12*q),
       knee=(.32,0,.69+.05*q),ankle=(.04,0,.16+.12*q))
  figures(s,j,'calf')
  for yy in (-.17,.17):s.sphere((.44,yy,.145),.13,'shoe',scale=(1.5,.95,.5))
 elif md==457:
  stride=.20*math.cos(t*2*math.pi);rise=.10+.035*math.cos(t*4*math.pi)
  j=sj(hip=(-.02,0,1.20+rise),shoulder=(-.02,0,1.78+rise),
    knee=(.06,0,.73),ankle=(.10,0,.23))
  j['kneeL']+=A([stride,0,.05]);j['ankleL']+=A([stride*.9,0,.12+rise*.12])
  j['kneeR']-=A([stride,0,-.05]);j['ankleR']-=A([stride*.9,0,-.12-rise*.12])
  figures(s,j,'calf')
  for side in ('L','R'):dumbbell(s,j['hand'+side])
 elif md==459:
  bench(s,center=(-.43,0,.77),length=.80)
  j=sj(hip=(-.47,0,.92),shoulder=(-.45,0,1.47),knee=(.18,0,.73),ankle=(.55+.20*q,0,.19+.29*q))
  figures(s,j,'tibialis')
  for sign in (-1,1):
   p=j['ankleL' if sign<0 else 'ankleR']+A([.13,sign*.06,-.02])
   s.bar(p,p+A([.38,0,.08]),.046,'metal')
   s.sphere(p+A([.37,0,.08]),.105,'metal2')
 elif md==468:
  bench(s,angle=-.30,center=(0,0,.73))
  a=.26+.85*q
  hip=A([.18,0,.81]);sho=hip+A([-.72*math.sin(a),0,.69*math.cos(a)])
  j=sj(hip=hip,shoulder=sho,knee=(.66,0,.51),ankle=(.99,0,.37))
  figures(s,j,'core')
  for y in (-.23,.23):s.bar((.95,y,.31),(.95,y,.53),.105,'pad')
 elif md==472:
  for y in (-.5,.5):
   s.bar((.0,y,.08),(.0,y,1.74),.069,'metal')
   s.box((.06,y,1.38),(.56,.30,.14),'pad')
  s.box((-.25,0,1.58),(.20,.95,.87),'pad')
  hip=A([-.15,0,1.16]);sho=A([-.18,0,1.72])
  j=sj(hip=hip,shoulder=sho,knee=(.39,0,.82+.22*q),ankle=(.64,0,.41+.54*q))
  arms(j,.16,.48,1.52,elbowx=.03,elbowz=1.51)
  figures(s,j,'core')
 elif md==474:
  bench(s,angle=.27,center=(0,0,.68))
  j=sj(hip=(.24,0,.86+.20*q),shoulder=(-.51,0,.94),knee=(.57-.30*q,0,.76+.42*q),ankle=(.72-.31*q,0,.45+.45*q))
  arms(j,-.66,.27,.80,elbowx=-.54,elbowz=.90)
  figures(s,j,'core')
 elif md==477:
  for y in (-.39,.39):s.bar((-.83,y,.10),(-.79,y,1.14),.075,'metal')
  s.box((.12,0,1.06),(.70,.75,.22),'pad')
  for y in (-.18,.18):s.sphere((-.98,y,1.13),.13,'pad')
  hip=A([.18,0,1.14]);a=.08+1.03*q
  sho=hip+A([.65*math.cos(a),0,.65*math.sin(a)])
  j=sj(hip=hip,shoulder=sho,knee=(-.30,0,1.13),ankle=(-.87,0,1.13))
  figures(s,j,'core')
 elif md==478:
  mat(s)
  hip=A([-.12,0,.24]);a=.13+1.0*q
  sho=hip+A([-.63*math.cos(a),0,.62*math.sin(a)])
  j=sj(hip=hip,shoulder=sho,knee=(.32,0,.38),ankle=(.64,0,.17))
  figures(s,j,'core')
  for y in (-.17,.17):s.box((.69,y,.17),(.3,.17,.19),'pad')
 elif md==479:
  bench(s,center=(-.17,0,.67))
  hip=A([.12,0,.80+.27*q]);sho=A([-.54,0,.85])
  j=sj(hip=hip,shoulder=sho,knee=(.58,0,1.24+.40*q),ankle=(.90,0,1.65+.25*q))
  arms(j,-.81,.30,.68,elbowx=-.62,elbowz=.80)
  figures(s,j,'core')
 elif md==480:
  for y in (-.34,.34):
   s.bar((-.12,y,.06),(-.12,y,1.15),.067,'metal')
   s.bar((-.4,y,1.15),(.33,y,1.15),.052,'steel')
  sway=.018*math.cos(2*math.pi*t)
  j=sj(hip=(-.11,0,1.18+sway),shoulder=(-.13,0,1.77+sway),knee=(.38,0,1.10),ankle=(.91,0,1.10))
  arms(j,-.02,.34,1.15,elbowx=-.11,elbowz=1.48)
  figures(s,j,'core')
 elif md in (486,487):
  origin=cable(s,level=.38 if md==486 else 1.32,x=1.29,y=-1.18)
  # Pull diagonal upwards, or horizontally across torso
  twist=(q-.5)*.58
  j=sj(hip=(0,0,1.13),shoulder=(twist,0,1.71))
  if md==486:
   dest=A([.22+.32*q,.29+.60*q,1.04+.85*q])
  else:
   dest=A([.23,.2+.92*q,1.38])
  for side in ('L','R'):
   j['elbow'+side]=j['shoulder']+A([.23,.1 if side=='L' else -.1,-.20])
   j['hand'+side]=dest+A([0,-.10 if side=='L' else .10,0])
  figures(s,j,'obliques')
  s.bar(origin,dest,.010,'steel')
 elif md==489:
  s.cam.SetPosition(3.2,6.8,2.65)
  anchor=A([1.15,0,.10])
  az=-.78+1.56*q
  grip=A([.15,math.sin(az)*.77,1.58+.13*math.cos(az)])
  j=sj(hip=(-.06,0,1.12),shoulder=(-.02,.18*math.sin(az),1.70))
  for sign,sd in [(-1,'L'),(1,'R')]:
   j['elbow'+sd]=grip+A([-.16,.14*sign,-.18])
   j['hand'+sd]=grip+A([0,.10*sign,0])
  figures(s,j,'obliques')
  s.bar(anchor,grip,.062,'steel')
  s.sphere(anchor,.14,'metal2')
 elif md==490:
  s.cam.SetPosition(3.3,6.3,2.75)
  for y in (-.58,.58):s.bar((0,y,.08),(0,y,2.63),.069,'metal')
  s.bar((0,-.68,2.63),(0,.68,2.63),.059,'steel')
  hip=A([.03,0,1.53])
  sho=A([0,0,2.14])
  j=sj(hip=hip,shoulder=sho,knee=(.55,.65*(q-.5),1.16),ankle=(.82,1.18*(q-.5),1.02))
  arms(j,.0,.39,2.59,elbowx=0,elbowz=2.28)
  figures(s,j,'obliques')
 elif md==492:
  # Roman bench, hips anchored, lateral trunk bend visible along Y
  s.cam.SetPosition(4.6,5.1,2.8)
  bench(s,angle=.20,center=(-.34,0,.76))
  hip=A([0,0,1.03]);sho=hip+A([.11,.46*(q-.5),.64])
  j=sj(hip=hip,shoulder=sho,knee=(-.52,0,.65),ankle=(-.83,0,.27))
  figures(s,j,'obliques')
 elif md==494:
  # Swiss ball stir-the-pot, elliptical forearm track with stable hips
  s.cam.SetPosition(3.4,6.8,2.3)
  s.sphere((.83,0,.43),.47,'metal2',scale=(1.0,1.0,1.0))
  theta=2*math.pi*t
  shoulder=A([.14,0,.89]);hip=A([-.42,0,.85])
  j=sj(hip=hip,shoulder=shoulder,knee=(-.78,0,.48),ankle=(-1.03,0,.16))
  for sign,sd in [(-1,'L'),(1,'R')]:
   j['elbow'+sd]=A([.50+.10*math.cos(theta),sign*.24+.09*math.sin(theta),.77])
   j['hand'+sd]=A([.73+.11*math.cos(theta),sign*.20+.11*math.sin(theta),.82])
  figures(s,j,'core')
 elif md==495:
  mat(s)
  # Isometric RKC plank; subtle tension/breathing, not invented limb repetitions.
  breath=.028*q
  j=sj(hip=(-.22,0,.65-breath),shoulder=(.42,0,.73-breath),knee=(-.68,0,.41),ankle=(-1.0,0,.16))
  for sign,sd in [(-1,'L'),(1,'R')]:
   j['elbow'+sd]=A([.71,sign*.20,.20])
   j['hand'+sd]=A([1.0,sign*.20,.19])
  figures(s,j,'core')
 elif md==500:
  # Vacuum breathing cycle, stable feet; navel contraction shown with oval overlay.
  j=sj(hip=(-.035*q,0,1.13),shoulder=(0,0,1.72))
  figures(s,j,'core')
  # Visible gradual compression of abdominal wall without spinal flexion.
  s.sphere((.198-.087*q,0,1.38),.16,'orange',scale=(.53-.14*q,.88,1.10))
  s.sphere((.20-.080*q,0,1.49),.10,'orange2',scale=(.52-.16*q,.76,.90))
 else:raise ValueError("Unsupported MD"+str(md))
def generate(block):
 target=Path("production/revisoes-md500-3d")/("bloco%02d"%block)
 target.mkdir(parents=True,exist_ok=True)
 inventory=json.loads(Path("production/INVENTARIO_MD500.json").read_text(encoding="utf-8"))
 results=[]
 for md,name in BLOCKS[block]:
  assert inventory[md-1]["id"]==md and not inventory[md-1]["animation_path"],(md,"already linked")
  scene=Scene(name);frames=[]
  for n in range(N):
   scene.clear();main_pose(scene,md,n/N);frames.append(scene.screenshot())
  gif=target/("md%d.gif"%md)
  frames[0].save(gif,format="GIF",save_all=True,append_images=frames[1:],
                 loop=0,duration=90,disposal=2,optimize=False,colors=128)
  frames[4].save(target/("md%d_preview.png"%md))
  image=Image.open(gif)
  assert image.size==(448,448) and image.n_frames>=8
  results.append(dict(id=md,name=name,frames=image.n_frames,size_bytes=gif.stat().st_size,
        sha256=hashlib.sha256(gif.read_bytes()).hexdigest(),status="geometric_3d_preview_not_approved",catalog_linked=False))
  print("MD",md,"frames",image.n_frames,"bytes",gif.stat().st_size,flush=True)
 (target/"manifest.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--block",type=int,required=True,choices=(7,8,9,10))
 generate(a.parse_args().block)
