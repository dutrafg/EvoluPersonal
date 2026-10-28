"""Assemble source render sheets into review GIFs; no automatic visual approval."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageChops, ImageStat
import numpy as np

ROOT=Path(__file__).resolve().parent
batch=json.loads((ROOT/'lote.json').read_text())
results=[]
for item in batch['items']:
    source=ROOT/'sheets'/f"md{item['md_id']}.png"
    if not source.exists():
        continue
    sheet=Image.open(source).convert('RGB')
    w,h=sheet.size
    # Remove thin generated grid separators when present; never alter anatomy.
    arr=np.asarray(sheet)
    whites=(arr.min(axis=2)>230)
    cuts_x=[0]
    for k in (1,2):
        center=round(k*w/3)
        candidates=[x for x in range(max(0,center-18),min(w,center+19)) if whites[:,x].mean()>.9]
        cuts_x.append(round(sum(candidates)/len(candidates)) if candidates else center)
    cuts_x.append(w)
    center=h//2
    candidates=[y for y in range(max(0,center-24),min(h,center+25)) if whites[y,:].mean()>.9]
    if candidates:
        split=round(sum(candidates)/len(candidates))
    else:
        # Some generated sheets have an unequal row split; detect the actual
        # background seam at tile margins so heads and weights are not clipped.
        xs=[min(w-1,max(0,round(w*k/3)+offset)) for k in range(4) for offset in (-3,0,3)]
        delta=np.abs(np.diff(arr[:,xs].astype(float),axis=0)).mean(axis=(1,2))
        ys=range(max(1,center-64),min(h-1,center+65))
        split=max(ys,key=lambda y:delta[y-1])
        if delta[split-1]<3:
            split=center
    cuts_y=[0,split,h]
    frames=[sheet.crop((cuts_x[c]+4,cuts_y[r]+4,cuts_x[c+1]-4,cuts_y[r+1]-4)).resize((144,144),Image.Resampling.LANCZOS) for r in range(2) for c in range(3)]
    diffs=[sum(ImageStat.Stat(ImageChops.difference(a,b)).mean) for a,b in zip(frames,frames[1:])]
    output=ROOT/'gifs'/f"md{item['md_id']}.gif"
    orders_file=ROOT/'frame-order.json'
    orders=json.loads(orders_file.read_text()) if orders_file.exists() else {}
    if str(item['md_id']) in orders:
        frames=[frames[k] for k in orders[str(item['md_id'])]]
    durations=[220,160,160,220,160,160]
    if item['md_id']==305:
        # Six source poses contain a separate three-pose ascent for each arm.
        frames=[frames[i] for i in [0,1,2,1,3,4,5,4]]
        durations=[180]*len(frames)
    frames[0].save(output,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)
    check=Image.open(output)
    for k in range(check.n_frames):
        check.seek(k);check.load()
    results.append({'md_id':item['md_id'],'name':item['name'],'file':str(output.relative_to(ROOT)),'frames':check.n_frames,'size':list(check.size),'loop':check.info.get('loop'),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'adjacent_frame_differences':diffs,'visual_qa_approved':False})
assert len({x['sha256'] for x in results})==len(results),'Duplicate bytes in new batch'
(ROOT/'technical-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({'assembled':len(results),'approved':sum(x['visual_qa_approved'] for x in results)},ensure_ascii=False))
