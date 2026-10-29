#!/usr/bin/env python3
"""3D geometric review previews; NOT anatomically approved final catalog media."""
import sys,math,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from render_md500_bloco01 import Scene
BASE=Path('production/revisoes-md500-3d/bloco02');BASE.mkdir(parents=True,exist_ok=True)
F=18

def pose(s,md,t):
 q=(1-math.cos(2*math.pi*t))/2
 hip=np.array([0.,0.,1.15]);sho=np.array([.04,0,1.78]);knee=np.array([.1,0,.7]);ankle=np.array([.08,0,.19]);elbow=sho+np.array([.1,0,-.25]);hand=elbow+np.array([.03,0,-.25]);
 j={'hip':hip,'shoulder':sho,'kneeL':knee+np.array([0,-.17,0]),'kneeR':knee+np.array([0,.17,0]),'ankleL':ankle+np.array([0,-.17,0]),'ankleR':ankle+np.array([0,.17,0]),'elbowL':elbow+np.array([0,-.20,0]),'elbowR':elbow+np.array([0,.20,0]),'handL':hand+np.array([0,-.20,0]),'handR':hand+np.array([0,.20,0])}
 if md==269:
  s.cam.SetPosition(4,6,2.6)
  for y in (-.6,.6):s.bar((-1.15,y,.06),(-1.15,y,2.48),.068,'metal',False)
  s.bar((-1.15,-.6,2.42),(-1.15,.6,2.42),.06,'steel',False)
  s.box((-.35,0,.10),(1.9,1.3,.1),'pad',False)
  hip=np.array([-.20,0,.69]);sho=np.array([.38,0,.70]);j['hip']=hip;j['shoulder']=sho
  j['kneeL']=np.array([-.28,-.16,.24]);j['ankleL']=np.array([-.52,-.16,.13]);j['kneeR']=np.array([-.15,.16,.41]);j['ankleR']=np.array([-.47+.31*q,.16,.46+.57*q]);
  for side,y in [('L',-.2),('R',.2)]:j['elbow'+side]=np.array([.55,y,.43]);j['hand'+side]=np.array([.82,y,.13])
  s.person(j)
  a=j['ankleR'];s.bar((-1.05,-.5,a[2]+.06),(.70,.6,a[2]+.06),.065,'steel')
 elif md==275:
  s.cam.SetPosition(2.0,6.5,2.8)
  s.box((1.05,0,.15),(.45,1.5,.13),'metal2',False)
  s.bar((1.1,-.6,.15),(1.1,-.6,2.0),.07,'metal',False)
  s.bar((1.1,.6,.15),(1.1,.6,2.0),.07,'metal',False)
  s.box((.90,0,1.25),(.38,1.1,.18),'pad',False)
  j['kneeR']=np.array([.1,.2+.60*q,.68]);j['ankleR']=np.array([.10,.2+.74*q,.14+.05*q]);
  j['handL']=np.array([.95,-.24,1.28]);j['handR']=np.array([.95,.24,1.28]);j['elbowL']=np.array([.65,-.2,1.35]);j['elbowR']=np.array([.65,.2,1.35]);
  s.person(j)
  s.box((.12,.4+.60*q,.65),(.35,.20,.2),'pad',True)
 elif md==278:
  s.cam.SetPosition(2.5,6.0,2.3)
  s.box((-.20,0,.05),(2.9,1.45,.1),'metal2',False)
  s.bar((1.42,.25,.04),(1.42,.25,1.75),.065,'metal',False)
  s.sphere((1.42,.25,1.55),.13,'steel',dynamic=False)
  j['hip']=np.array([-.02,0,.37]);j['shoulder']=np.array([-.62,0,.40]);
  j['kneeL']=np.array([.37,-.16,.26]);j['ankleL']=np.array([.84,-.16,.19]);
  j['kneeR']=np.array([.38,.19+.35*q,.33+.30*q]);j['ankleR']=np.array([.84,.19+.64*q,.26+.54*q]);
  for sd,y in [('L',-.2),('R',.2)]:j['elbow'+sd]=np.array([-.85,y,.29]);j['hand'+sd]=np.array([-.95,y,.13]);
  s.person(j)
  s.bar((1.42,.25,1.55),j['ankleR'],.008,'steel')
 elif md==290:
  s.cam.SetPosition(2.7,6.2,2.8)
  s.box((.88,0,.14),(.7,1.3,.16),'metal2',False)
  for y in (-.55,.55):s.bar((.87,y,.14),(.87,y,2.25),.063,'metal',False)
  s.box((.79,0,1.32),(.26,1.1,.21),'pad',False)
  phase=int(t*4)%4;v=(1-math.cos(2*math.pi*((t*4)%1)))/2
  if phase==0: foot=np.array([.45+.60*v,.17,.18]);kne=np.array([.23+.39*v,.17,.7])
  elif phase==1:foot=np.array([-.21-.40*v,.17,.18]);kne=np.array([.01-.35*v,.17,.7])
  elif phase==2:foot=np.array([.03,.17+.74*v,.16]);kne=np.array([.04,.17+.52*v,.65])
  else: foot=np.array([.04,.65-.50*v,.16]);kne=np.array([.05,.56-.30*v,.65])
  j['kneeR']=kne;j['ankleR']=foot
  for side,y in [('L',-.19),('R',.19)]:j['elbow'+side]=np.array([.4,y,1.5]);j['hand'+side]=np.array([.72,y,1.34])
  s.person(j)
  s.sphere(j['kneeR']*.35+j['ankleR']*.65,.13,'pad',scale=(.75,.8,1.1))
 elif md==308:
  s.cam.SetPosition(3.8,6,2.7)
  hip=np.array([-.31,0,1.13]);sho=np.array([-.12,0,1.72]);j['hip']=hip;j['shoulder']=sho
  j['kneeL']=np.array([-.23,-.18,.66]);j['kneeR']=np.array([-.23,.18,.66]);j['ankleL']=np.array([-.28,-.18,.15]);j['ankleR']=np.array([-.28,.18,.15]);
  for sd,y in [('L',-.25),('R',.25)]:
   j['elbow'+sd]=np.array([.20+.14*q,y,1.38+.38*q]);j['hand'+sd]=np.array([.50+.24*q,y,1.39+.71*q])
  s.person(j)
  s.bar((1.33,0,.17),(.50+.24*q,0,1.39+.71*q),.08,'metal')
  s.bar((.50+.24*q,-.42,1.39+.71*q),(.50+.24*q,.42,1.39+.71*q),.085,'steel')
  s.sphere((1.33,0,.17),.15,'metal2',dynamic=False)
 else:raise ValueError(md)

def main():
 out=[]
 for md,name in [(269,'Coice no Smith em quatro apoios'),(275,'Abdutora em pé na máquina'),(278,'Abdução de quadril deitado na polia'),(290,'Máquina multiquadril (quatro direções)'),(308,'Viking Press')]:
  s=Scene(name);frames=[]
  for n in range(F):s.clear();pose(s,md,n/F);frames.append(s.screenshot())
  path=BASE/f'md{md}.gif';frames[0].save(path,save_all=True,append_images=frames[1:],duration=90,loop=0,disposal=2,optimize=False,colors=128)
  frames[4].save(BASE/f'md{md}_preview.png')
  image=Image.open(path)
  assert image.n_frames>=8,(md,image.n_frames)
  out.append({'id':md,'name':name,'frames':image.n_frames,'size_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'geometric_3d_preview_not_approved'})
  print(md,image.n_frames,path.stat().st_size)
 (BASE/'manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
