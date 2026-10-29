"""Validate the actual deliverables and their catalog associations before upload."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
R=Path(__file__).resolve().parent;P=R.parents[1]
batch=json.loads((R/'lote.json').read_text())
report=json.loads((R/'technical-validation.json').read_text())
inventory={x['id']:x for x in json.loads((P/'production/INVENTARIO_MD500.json').read_text())}
existing=set(json.loads((R/'existing-gif-shas.json').read_text()))
assert len(batch['items'])==len(report)==25
assert len({x['md_id'] for x in report})==25
hashes=set()
for item in batch['items']:
 i=item['md_id'];t=next(x for x in report if x['md_id']==i)
 data=(P/item['output_path']).read_bytes()
 assert data[:6] in [b'GIF87a',b'GIF89a']
 assert hashlib.sha256(data).hexdigest()==t['sha256']
 blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert blob==t['gif_blob_sha']==inventory[i]['gif_blob_sha']
 assert blob not in existing and blob not in hashes
 hashes.add(blob)
 assert inventory[i]['name']==item['name']
 assert inventory[i]['animation_path']==item['output_path'].removeprefix('dist/')
 assert inventory[i]['media_review_pending'] and not item['visual_qa_approved']
 im=Image.open(P/item['output_path']);assert im.size==(144,144) and im.n_frames>=3
 assert im.info.get('loop')==0
 for n in range(im.n_frames):im.seek(n);im.load()
print(json.dumps({'files_decoded':25,'unique_sha':25,'catalog_associations':25,'final_approval':False}))
