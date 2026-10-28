"""Assemble generated keyframes without changing anatomy; final review remains pending."""
from pathlib import Path
import json,re,shutil,hashlib
from PIL import Image,ImageChops,ImageStat
R=Path(__file__).resolve().parent
sources=json.loads((R/'fontes.json').read_text())
for d in ['sheets','gifs']: (R/d).mkdir(exist_ok=True)
results=[]
orders={215:[0,1,2,1,4,5],221:[1,2,3,4,2,1],254:[1,2,3,4,1],367:[0,1,2,3,1,0]}
for x in sources:
 p=Path(re.search(r'(/workspace/[^\s]+\.png)',x['hint']).group(1))
 dst=R/'sheets'/f"md{x['id']}.png";shutil.copyfile(p,dst)
 im=Image.open(dst).convert('RGB');w,h=im.size
 frames=[im.crop((round(c*w/3)+4,round(r*h/2)+4,round((c+1)*w/3)-4,round((r+1)*h/2)-4)).resize((144,144),Image.Resampling.LANCZOS) for r in range(2) for c in range(3)]
 frames=[frames[i] for i in orders.get(x['id'],range(6))]
 out=R/'gifs'/f"md{x['id']}.gif"
 frames[0].save(out,save_all=True,append_images=frames[1:],duration=220,loop=0,disposal=2,optimize=False)
 check=Image.open(out)
 for n in range(check.n_frames):check.seek(n);check.load()
 assert check.n_frames>=3
 data=out.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 target=R.parents[1]/'dist/assets/md500-3d'/out.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(out,target)
 results.append({'md_id':x['id'],'name':x['name'],'output_path':str(target.relative_to(R.parents[1])),'frames':check.n_frames,'size':[144,144],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'gif_blob_sha':blob,'frame_order':orders.get(x['id'],list(range(6))),'visual_qa_approved':False})
assert len(results)==25 and len({x['sha256'] for x in results})==25
(R/'technical-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({'gifs':len(results),'bytes':sum(x['bytes'] for x in results),'approved':0}))
