"""Validate and package 25 distinct MD500 GIFs without approving app coverage."""
from pathlib import Path
import json, hashlib, shutil
from PIL import Image

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
batch=json.loads((HERE/'lote.json').read_text())
audit=json.loads((HERE/'auditoria.json').read_text())
inventory=json.loads((HERE/'inventario-md500.json').read_text())
rows={x['id']:x for x in inventory}
old_blobs={x['sha'] for x in audit['existing_gif_blobs']}
assert len(batch['items'])==25
assert len({x['md_id'] for x in batch['items']})==25
assert len(inventory)==500
assert len(json.loads((HERE/'fontes.json').read_text()))==25
checks=[]
for item in batch['items']:
    md=item['md_id']
    assert rows[md]['ref']=='—',f'MD{md} already linked'
    assert rows[md]['name']==item['name'],f'MD{md} name mismatch'
    source=HERE/'gifs'/f'md{md}.gif'
    data=source.read_bytes()
    git_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert git_sha not in old_blobs,f'MD{md} repeats an existing file'
    gif=Image.open(source)
    assert gif.size==(144,144)
    assert gif.info.get('loop')==0
    assert gif.n_frames>=6
    duration=0
    frame_hashes=set()
    for k in range(gif.n_frames):
        gif.seek(k);gif.load()
        duration+=gif.info.get('duration',0)
        frame_hashes.add(hashlib.sha256(gif.convert('RGB').tobytes()).hexdigest())
    assert len(frame_hashes)>=3,f'MD{md} lacks motion frames'
    if md==373:
        assert gif.n_frames==105,'Rosca 21 must contain the explicit 7+7+7 sequence'
    destination=REPO/item['output_path']
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,destination)
    checks.append({'md_id':md,'name':item['name'],'file':'../../'+item['output_path'],
        'repository_path':item['output_path'],'frames':gif.n_frames,'size':list(gif.size),
        'loop':0,'duration_ms':duration,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
        'git_blob_sha':git_sha,'all_frames_decoded':True,'technical_qa_passed':True,
        'visual_review':'inicial_realizada_aprovacao_final_pendente','visual_qa_approved':False})
assert len({x['sha256'] for x in checks})==25
allowed={f"md{x['md_id']}.gif" for x in checks}
for path in (HERE/'gifs').glob('*.gif'):
    if path.name not in allowed:
        path.unlink()
(HERE/'technical-validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
template=(HERE/'revisao.html').read_text()
start=template.find("fetch('technical-validation.json')")
if start<0:
    start=template.index('const items=')
template=template[:start]+"const items="+json.dumps(checks,ensure_ascii=False)+";for(const x of items){const card=document.createElement('article');card.className='card';const id=document.createElement('div');id.className='id';id.textContent='MD'+x.md_id;const title=document.createElement('h2');title.textContent=x.name;const image=document.createElement('img');image.src=x.file;image.alt=x.name;const status=document.createElement('div');status.className='status';status.textContent=x.frames+' quadros · '+x.size.join('×')+' · Revisão final pendente';card.append(id,title,image,status);grid.append(card);}</script></html>"
(HERE/'revisao.html').write_text(template)
print(json.dumps({'count':25,'unique_ids':25,'unique_hashes':25,'all_decoded':True,
    'matches_existing_files':0,'bytes':sum(x['bytes'] for x in checks),
    'rosca21_frames':next(x['frames'] for x in checks if x['md_id']==373)},ensure_ascii=False))
