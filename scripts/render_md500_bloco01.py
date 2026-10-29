#!/usr/bin/env python3
"""Procedural 3D proof-of-concept animation, five distinct exercises (MD214-MD250).
These are REVIEW CANDIDATES, NOT biomechanically approved final 3D assets.
"""
import vtk, math, os, json, hashlib, numpy as np
from PIL import Image, ImageDraw
from vtk.util.numpy_support import vtk_to_numpy
from pathlib import Path

BASE=Path('production/revisoes-md500-3d/bloco01');BASE.mkdir(exist_ok=True)
RES=448; F=18
colors={'skin':(.66,.70,.74),'shirt':(.31,.38,.45),'short':(.18,.24,.31), 'orange':(.97,.39,.18),'orange2':(.97,.59,.22),'metal':(.35,.46,.57),'metal2':(.19,.27,.36),'pad':(.12,.17,.24),'steel':(.63,.72,.79),'shoe':(.12,.15,.21),'floor':(.075,.12,.17)}

class Scene:
 def __init__(self,name):
  self.name=name
  self.r=vtk.vtkRenderer();self.r.SetBackground(.039,.082,.127);self.r.SetBackground2(.088,.151,.218);self.r.GradientBackgroundOn()
  self.w=vtk.vtkRenderWindow();self.w.SetOffScreenRendering(1);self.w.SetMultiSamples(8);self.w.AddRenderer(self.r);self.w.SetSize(RES,RES)
  self.cam=self.r.GetActiveCamera();self.cam.SetPosition(3.65,7.0,3.0);self.cam.SetFocalPoint(.10,0,1.15);self.cam.SetViewUp(0,0,1);self.cam.ParallelProjectionOn();self.cam.SetParallelScale(2.10)
  self.light=vtk.vtkLight();self.light.SetPosition(-3,6,8);self.light.SetIntensity(.95);self.r.AddLight(self.light)
  self.side=vtk.vtkLight();self.side.SetPosition(4,-3,5);self.side.SetIntensity(.7);self.r.AddLight(self.side)
  self.dynamic=[]
  self.floor()
 def add(self,source,color,pos=None,scale=None,angle=None,dynamic=True,opacity=1):
  mapper=vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(source.GetOutputPort())
  a=vtk.vtkActor();a.SetMapper(mapper)
  a.GetProperty().SetColor(colors.get(color,color));a.GetProperty().SetSpecular(.35);a.GetProperty().SetSpecularPower(35);a.GetProperty().SetOpacity(opacity)
  tr=vtk.vtkTransform();tr.PostMultiply()
  if scale:tr.Scale(*scale)
  if angle: tr.RotateWXYZ(angle[0],*angle[1])
  if pos is not None: tr.Translate(*pos)
  a.SetUserTransform(tr)
  self.r.AddActor(a)
  if dynamic:self.dynamic.append(a)
  return a
 def sphere(self,pt,r=.1,color='skin',scale=(1,1,1),dynamic=True):
  s=vtk.vtkSphereSource();s.SetRadius(r);s.SetThetaResolution(20);s.SetPhiResolution(16);return self.add(s,color,pt,scale,dynamic=dynamic)
 def bar(self,p,q,rad=.03,color='metal',dynamic=True):
  # Ellipsoid with its axis along the input vector, creating rounded tapered limbs
  p=np.array(p,dtype=float);q=np.array(q,dtype=float);c=(p+q)/2;d=q-p;L=np.linalg.norm(d)
  if L<1e-4:return
  yy=np.array([0.,1.,0.]);dest=d/L;axis=np.cross(yy,dest);axislen=np.linalg.norm(axis);ang=math.degrees(math.acos(np.clip(np.dot(yy,dest),-1,1)))
  if axislen<1e-8:axis=np.array([0,0,1.])
  else:axis/=axislen
  s=vtk.vtkSphereSource();s.SetRadius(1);s.SetThetaResolution(16);s.SetPhiResolution(16)
  return self.add(s,color,c,scale=(rad,L/2+rad*.28,rad),angle=(ang,axis),dynamic=dynamic)
 def box(self,p,scale,color='metal',dynamic=False):
  c=vtk.vtkCubeSource();c.SetXLength(scale[0]);c.SetYLength(scale[1]);c.SetZLength(scale[2]);return self.add(c,color,pos=p,dynamic=dynamic)
 def floor(self):
  self.box((0,0,-.10),(4.8,2.8,.12),'floor')
  for i in np.arange(-2,2.2,.36):
   self.bar((i,-.65,-.03),(i,.55,-.03),.006, (.13,.21,.28),False)
 def clear(self):
  for a in self.dynamic:self.r.RemoveActor(a)
  self.dynamic.clear()
 def machine_hack(self,pendulum=False):
  for y in (-.5,.5):
   self.bar((.88,y,.04),(1.4,y,2.58),.067,'metal',False)
   self.bar((.88,y,2.58),(1.63,y,2.7),.06,'metal2',False)
   self.bar((.0,y,.1),(1.35,y,.12),.055,'metal2',False)
  self.box((-.14,0,.1),(.9,1.5,.10),'metal2')
  self.bar((1.45,-.73,2.08),(1.45,.73,2.08),.09,'metal',False)
  self.sphere((1.45,-.7,2.08),.20,'steel',dynamic=False)
  self.sphere((1.45,.7,2.08),.20,'steel',dynamic=False)
 def machine_curl(self):
  self.box((-.28,0,.16),(1.9,1.05,.14),'metal2')
  self.bar((-.65,-.48,.16),(-.65,-.48,1.35),.075,'metal',False)
  self.bar((.53,.48,.16),(.53,.48,1.40),.075,'metal',False)
  self.box((-.19,0,.61),(.55,1.0,.19),'pad')
  self.box((.62,0,1.28),(.14,1.0,.72),'metal2')
  self.sphere((.55,0,1.07),.24,'pad',scale=(.55,1.65,.6),dynamic=False)
  self.bar((.77,.6,1.61),(.77,-.6,1.61),.06,'steel',False)
 def machine_ghr(self):
  self.box((-.30,0,.12),(2.6,1.1,.20),'metal2')
  self.bar((-.55,-.42,.15),(-.45,-.42,.97),.08,'metal',False)
  self.bar((.63,-.42,.15),(.58,-.42,.84),.08,'metal',False)
  self.box((-.45,0,.98),(.63,.85,.24),'pad')
  for y in (-.3,.3):
   self.bar((-.93,y,.88),(-.93,y,1.13),.12,'pad',False)
   self.bar((-.72,y,.7),(-.72,y,.94),.11,'pad',False)
  self.sphere((.3,0,.96),.21,'pad',scale=(1.2,1.4,.65),dynamic=False)
 def machine_hip(self):
  self.box((-.7,0,.20),(2.7,1.0,.20),'metal2')
  self.bar((-.90,-.43,.20),(-.90,-.43,1.15),.075,'metal',False)
  self.bar((.76,.43,.20),(.76,.43,1.45),.075,'metal',False)
  self.box((-.66,0,.95),(.53,.85,.16),'pad')
  self.box((-.88,0,1.23),(.14,.9,.66),'metal2')
  for y in (-.5,.5):self.sphere((.85,y,1.45),.16,'metal',dynamic=False)
 def person(self,joints,active=('glutes','hamstrings'),outfit=True):
  j={k:np.array(v) for k,v in joints.items()}
  hip=j['hip'];sho=j['shoulder'];neck=sho+np.array([0,0,.12]);head=sho+np.array([.045,0,.3]);
  self.bar(hip,sho,.19,'shirt');self.bar(hip,sho,.12,'orange',dynamic=True)
  self.sphere(hip,.18,'short',scale=(1.0,1.0,.8));self.sphere(sho,.21,'shirt',scale=(1.05,.98,.78));self.sphere(head,.17,'skin',scale=(.75,.84,1.08))
  # three-dimensional nose and facial plane
  self.sphere(head+np.array([.145,.015,.005]),.035,'skin',scale=(1.5,.8,.65))
  for y in (-.15,.15):
   shoulder=sho+np.array([.01,y,0]);elbow= j.get('elbowL' if y<0 else 'elbowR',sho+np.array([.15,y,-.35]));hand=j.get('handL' if y<0 else 'handR',elbow+np.array([.10,0,-.30]));
   self.bar(shoulder,elbow,.09,'skin');self.bar(elbow,hand,.065,'skin');self.sphere(hand,.075,'skin')
   hipJoint=hip+np.array([0,y*.7,0]);knee=j.get('kneeL' if y<0 else 'kneeR',hip+np.array([.28,y,-.55]));ankle=j.get('ankleL' if y<0 else 'ankleR',knee+np.array([-.2,0,-.5]));
   self.bar(hipJoint,knee,.145,'short' if not active else 'orange');self.bar(knee,ankle,.10,'skin');self.sphere(knee,.115,'skin')
   self.sphere(ankle+np.array([.06,0,-.055]),.11,'shoe',scale=(1.48,.85,.44))
   if 'hamstrings' in active:
    self.bar(hipJoint*.55+knee*.45,hipJoint*.3+knee*.7,.122,'orange2')
   if 'glutes' in active:
    self.sphere(hipJoint+np.array([-.015,0,-.04]),.145,'orange2',scale=(.95,.78,.8))
 def screenshot(self):
  self.w.Render()
  f=vtk.vtkWindowToImageFilter();f.SetInput(self.w);f.SetInputBufferTypeToRGB();f.ReadFrontBufferOff();f.Update()
  img=f.GetOutput();size=img.GetDimensions();arr=vtk_to_numpy(img.GetPointData().GetScalars()).reshape(size[1],size[0],3)
  return Image.fromarray(np.flipud(arr.copy()))

def movement(scene,md,t):
 # smooth eccentric then concentric (0 -> 1 -> 0)
 cycle=(1-math.cos(2*math.pi*t))/2
 if md in (214,219):
  scene.machine_hack(pendulum=(md==219))
  a=(.13 + (.8 if md==214 else .96)*cycle)
  hx=-.22-.25*cycle;hz=1.16-.10*cycle
  hip=np.array([hx,0,hz]);sho=hip+np.array([.7*math.sin(a),0,.70*math.cos(a)])
  knee=np.array([-.045,0,.63]);ankle=np.array([.01,0,.17])
  elbow=sho+np.array([.11,0,-.30]);hand=elbow+np.array([.07,0,-.27])
  j={'hip':hip,'shoulder':sho, 'kneeL':knee+np.array([0,-.15,0]),'kneeR':knee+np.array([0,.15,0]),'ankleL':ankle+np.array([0,-.15,0]),'ankleR':ankle+np.array([0,.15,0]),'elbowL':elbow+np.array([0,-.2,0]),'elbowR':elbow+np.array([0,.2,0]),'handL':hand+np.array([0,-.2,0]),'handR':hand+np.array([0,.2,0])}
  scene.person(j)
  # moving shoulder yoke/pad from machine arm
  scene.bar((1.3,0,2.36),sho+np.array([0,0,.07]),.055,'metal')
  scene.box(sho+np.array([.1,0,.02]),(.22,.66,.15),'pad',True)
 elif md==228:
  scene.machine_curl()
  hip=np.array([-.1,0,1.10]);sho=np.array([.18,0,1.61]);
  kL=np.array([-.23,-.16,.67]);aL=np.array([-.66+.70*cycle,.37,.12+.65*cycle]);
  kR=np.array([-.23,.15,.67]);aR=np.array([-.29,.15,.17]);
  elbow=sho+np.array([.19,0,-.15]);hand=elbow+np.array([.27,0,-.27]);
  j={'hip':hip,'shoulder':sho,'kneeL':kL,'kneeR':kR,'ankleL':aL,'ankleR':aR,'elbowL':elbow+np.array([0,-.18,0]),'elbowR':elbow+np.array([0,.18,0]),'handL':hand+np.array([0,-.18,0]),'handR':hand+np.array([0,.18,0])}
  scene.person(j)
  scene.bar(aL+np.array([-.07,-.26,0]),aL+np.array([-.07,.26,0]),.115,'pad')
 elif md==240:
  scene.machine_ghr()
  kne=np.array([.14,0,1.04]);hip=kne+np.array([.32-.10*cycle,0,.29+.15*cycle]);
  angle=.25+.95*cycle;sho=hip+np.array([.69*math.sin(angle),0,.69*math.cos(angle)])
  ankle=np.array([-.83,0,.92]);elbow=sho+np.array([.04,0,-.29]);hand=elbow+np.array([.17,0,-.28]);
  j={'hip':hip,'shoulder':sho,'kneeL':kne+np.array([0,-.15,0]),'kneeR':kne+np.array([0,.15,0]),'ankleL':ankle+np.array([0,-.15,0]),'ankleR':ankle+np.array([0,.15,0]),'elbowL':elbow+np.array([0,-.19,0]),'elbowR':elbow+np.array([0,.19,0]),'handL':hand+np.array([0,-.19,0]),'handR':hand+np.array([0,.19,0])}
  scene.person(j)
 elif md==250:
  scene.machine_hip()
  hip=np.array([.05,0,.62+.36*cycle]);sho=np.array([-.52,0,1.03]);
  knee=np.array([.62,0,.73]);ankle=np.array([.79,0,.16]);
  elbow=sho+np.array([.28,0,-.14]);hand=elbow+np.array([.25,0,-.13])
  j={'hip':hip,'shoulder':sho,'kneeL':knee+np.array([0,-.15,0]),'kneeR':knee+np.array([0,.15,0]),'ankleL':ankle+np.array([0,-.15,0]),'ankleR':ankle+np.array([0,.15,0]),'elbowL':elbow+np.array([0,-.18,0]),'elbowR':elbow+np.array([0,.18,0]),'handL':hand+np.array([0,-.18,0]),'handR':hand+np.array([0,.18,0])}
  scene.person(j)
  scene.box(hip+np.array([0,0,.16]),(.47,.72,.16),'pad',True)
  scene.bar((.83,0,1.42),hip+np.array([0,0,.16]),.06,'metal')
 else:raise ValueError(md)

def main():
 results=[]
 for md,name in [(214,'RDL Hack / V-Squat invertido'),(219,'Bom Dia na Máquina'),(228,'Flexora Ajoelhada'),(240,'Razor Curl GHR'),(250,'Elevação Pélvica na Máquina')]:
  scene=Scene(name);frames=[]
  if md==228: scene.cam.SetPosition(5.2,4.8,2.6)
  for n in range(F):
   scene.clear();movement(scene,md,n/F);im=scene.screenshot();frames.append(im)
  path=BASE/f'md{md}.gif';frames[0].save(path,save_all=True,append_images=frames[1:],loop=0,duration=85,disposal=2,optimize=False,colors=128)
  frames[4].save(BASE/f'md{md}_preview.png')
  img=Image.open(path);print(md, img.size,img.n_frames,path.stat().st_size)
  results.append({'id':md,'name':name,'frames':img.n_frames,'size_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'geometric_3d_prototype_unapproved'})
 (BASE/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
