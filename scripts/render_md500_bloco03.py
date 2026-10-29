#!/usr/bin/env python3
"""Five separate VTK exercise-motion previews; not final approved 3D anatomy."""
import sys,math,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from render_md500_bloco01 import Scene
BASE=Path('production/revisoes-md500-3d/bloco03');BASE.mkdir(parents=True,exist_ok=True)
F=18

def pose(s,md,t):
 q=(1-math.cos(2*math.pi*t))/2
 hip=np.array([0.,0.,1.17]);sho=np.array([.02,0.,1.77]);knee=np.array([.08,0.,.71]);ankle=np.array([.09,0.,.17]);elbow=np.array([.25,0.,1.56]);hand=np.array([.38,0.,1.28]);
 j={'hip':hip,'shoulder':sho,'kneeL':knee+np.array([0,-.17,0]),'kneeR':knee+np.array([0,.17,0]),'ankleL':ankle+np.array([0,-.17,0]),'ankleR':ankle+np.array([0,.17,0]),'elbowL':elbow+np.array([0,-.20,0]),'elbowR':elbow+np.array([0,.20,0]),'handL':hand+np.array([0,-.20,0]),'handR':hand+np.array([0,.20,0])}
 if md==311:
  s.cam.SetPosition(4.5,5.5,2.9)
  # Bradford press: from front, above head, then behind the head
  phase=2*q
  if phase<=1:
   x=.36*(1-phase);z=1.56+.57*phase
  else:x=-.27*(phase-1);z=2.13-.44*(phase-1)
  for sd,y in [('L',-.18),('R',.18)]:
   j['elbow'+sd]=np.array([x*.52+.1,y*1.25,1.81+.17*q]);j['hand'+sd]=np.array([x,y, z]);
  s.person(j)
  s.bar((x,-.78,z),(x,.78,z),.043,'steel');
  for y in (-.74,.74):s.sphere((x,y,z),.17,'metal2')
 elif md==318:
  s.cam.SetPosition(3.0,7.2,2.85)
  for y in (-1.16,1.16):
   s.bar((.3,y,.1),(.3,y,2.25),.08,'metal',False)
   s.sphere((.3,y,.42),.11,'steel',dynamic=False)
  for sd,y in [('L',-1),('R',1)]:
   j['elbow'+sd]=np.array([.0,.55*y*q+.35*y,1.47+.18*q]);j['hand'+sd]=np.array([.05,.73*y+.40*y*q,1.24+.63*q]);
  s.person(j)
  for sd,y in [('L',-1),('R',1)]:s.bar((.3,-y*1.16,.42),j['hand'+sd],.007,'steel')
 elif md==321:
  s.cam.SetPosition(4.4,5.7,2.8)
  s.bar((-.82,-.32,.20),(.32,-.32,1.33),.10,'metal',False)
  s.bar((-.82,.32,.20),(.32,.32,1.33),.10,'metal',False)
  s.box((-.20,0,.74),(.66,1.1,.15),'pad',False)
  hip=np.array([-.42,0,.92]);sho=np.array([.04,0,1.53]);j['hip']=hip;j['shoulder']=sho
  for sd,y in [('L',-1),('R',1)]:
   j['elbow'+sd]=np.array([.20,y*(.25+.36*q),1.35+.17*q]);j['hand'+sd]=np.array([.27,y*(.45+.56*q),1.13+.48*q])
  j['kneeL']=np.array([-.32,-.18,.55]);j['kneeR']=np.array([-.32,.18,.55]);j['ankleL']=np.array([-.39,-.18,.15]);j['ankleR']=np.array([-.39,.18,.15]);
  s.person(j)
  for y in (-1,1):s.sphere(np.array([.27,y*(.45+.56*q),1.13+.48*q]),.11,'metal2',scale=(1.45,.9,.85))
 elif md==346:
  s.cam.SetPosition(3.8,6.5,2.7)
  s.bar((-.81,-.3,.18),(.34,-.3,1.22),.095,'metal',False)
  s.bar((-.81,.3,.18),(.34,.3,1.22),.095,'metal',False)
  s.box((-.24,0,.72),(.78,1.15,.13),'pad',False)
  hip=np.array([-.46,0,.93]);sho=np.array([.10,0,1.42]);j['hip']=hip;j['shoulder']=sho
  j['kneeL']=np.array([-.4,-.17,.61]);j['kneeR']=np.array([-.4,.17,.61]);j['ankleL']=np.array([-.55,-.17,.18]);j['ankleR']=np.array([-.55,.17,.18]);
  j['elbowL']=np.array([.20,-.22,1.12]);j['handL']=np.array([.32,-.22,.95]);
  j['elbowR']=np.array([.28,.35+.42*q,1.34+.22*q]);j['handR']=np.array([.40,.45+.64*q,1.23+.53*q]);
  s.person(j)
  s.sphere(j['handR'],.12,'metal2',scale=(1.3,.85,.8))
 elif md==347:
  s.cam.SetPosition(3.45,6.3,2.8)
  s.bar((1.45,-.45,.15),(1.45,-.45,2.38),.075,'metal',False)
  s.bar((1.45,.45,.15),(1.45,.45,2.38),.075,'metal',False)
  pulley=np.array([1.4,0,2.22]);s.sphere(pulley,.14,'steel',dynamic=False)
  for sd,y in [('L',-1),('R',1)]:
   j['elbow'+sd]=np.array([.20-.12*q,.28*y,1.72+.08*q]);j['hand'+sd]=np.array([.65-.50*q,(.24+.09*q)*y,1.81+.21*q]);
  s.person(j)
  for side in ('L','R'):s.bar(pulley,j['hand'+side],.009,'steel')
 else:raise ValueError(md)

def main():
 results=[]
 for md,name in [(311,'Bradford Press'),(318,'Elevação lateral cruzada nos cabos'),(321,'Elevação lateral com peito apoiado'),(346,'Powell Raise'),(347,'Face Pull com rotação externa')]:
  scene=Scene(name);frames=[]
  for n in range(F):scene.clear();pose(scene,md,n/F);frames.append(scene.screenshot())
  path=BASE/f'md{md}.gif';frames[0].save(path,save_all=True,append_images=frames[1:],duration=85,loop=0,disposal=2,optimize=False,colors=128)
  frames[4].save(BASE/f'md{md}_preview.png')
  image=Image.open(path);assert image.n_frames>=8
  results.append({'id':md,'name':name,'frames':image.n_frames,'size_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'geometric_3d_preview_not_approved'})
  print(md,image.n_frames,path.stat().st_size)
 (BASE/'manifest.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
