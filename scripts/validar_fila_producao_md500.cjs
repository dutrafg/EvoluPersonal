'use strict';
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'), read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const inv=read('production/INVENTARIO_MD500.json'), queue=read('production/FILA_MD500_ATUAL.json'), plan=read('production/FILA_PRODUCAO_3D_MD500.json'), approved=read('production/APROVACAO_VISUAL_15_2026-10-29.json');
assert.equal(inv.length,500); assert.equal(queue.length,55); assert.equal(plan.items.length,58);
assert.equal(plan.summary.production_tasks,58);
const missing=inv.filter(x=>!x.animation_path);assert.equal(missing.length,55);
assert.deepEqual([...queue.map(x=>x.id)].sort((a,b)=>a-b),missing.map(x=>x.id).sort((a,b)=>a-b));
const assetMap=new Map();for(const x of inv.filter(x=>x.gif_blob_sha)){const a=assetMap.get(x.gif_blob_sha)||[];a.push(x.id);assetMap.set(x.gif_blob_sha,a)}
assert.equal(assetMap.size,442);
const shared=[...assetMap.values()].filter(x=>x.length>1).map(a=>a.sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]);
assert.deepEqual(shared,[[135,341],[140,340],[301,302]]);
const ids=new Set(plan.items.map(x=>x.md_id)); assert.equal(ids.size,58);
const plans=plan.items.filter(x=>x.kind==='gif_3d_ausente').map(x=>x.md_id);
assert.deepEqual(plans,queue.map(x=>x.id));
const uniques=plan.items.filter(x=>x.kind==='substituicao_de_gif_compartilhado');
assert.equal(uniques.length,3);
for(let i=0;i<plan.items.length;i++)assert.equal(plan.items[i].batch,'Lote '+String(Math.floor(i/25)+1).padStart(2,'0'));
for(const t of uniques){const r=inv[t.md_id-1];assert(r?.animation_path);assert(shared.some(g=>g.includes(t.md_id)));assert.equal(t.requires_visual_approval,true)}
assert.equal(approved.summary.approved_by_user,15);
assert.equal(inv.filter(x=>x.review_status==='aprovado_visual_usuario').length,9);
assert.equal(inv.filter(x=>x.review_status==='aprovado_usuario_repeticao_pendente').length,6);
console.log(JSON.stringify({total:500,linked:445,distinct:442,without_gif:55,duplicate_pairs:3,production_tasks:58,batch_sizes:[25,25,8],user_visual_approvals:15}));
