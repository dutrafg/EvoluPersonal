'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('dist/index.html'),inventory=JSON.parse(read('production/INVENTARIO_MD500.json'));
const queue=JSON.parse(read('production/FILA_MD500_ATUAL.json'));
const rows=JSON.parse(html.match(/const md500Rows=(\[\[.*?\]\]);/s)[1]);
const media=JSON.parse(html.match(/const md3dMedia=(\{.*?\});\n/s)[1]);
const table=read('docs/COMPARACAO_LISTA_500.md').split('\n').filter(x=>/^\|\s*\d+\s*\|/.test(x));
assert.equal(rows.length,500);assert.equal(inventory.length,500);assert.equal(table.length,500);
let linked=0,review=0;
for(let i=0;i<500;i++){
 const r=inventory[i],m=media[String(i+1)],legacy=rows[i][1],expected=m?'md'+(i+1):legacy||'—';
 const p=table[i].split('|').slice(1,-1).map(x=>x.trim());
 assert.equal(r.id,i+1);assert.equal(r.name,rows[i][0]);assert.equal(p[1],r.name);
 assert.equal(p[2].replaceAll(String.fromCharCode(96),''),expected);assert.equal(r.ref,expected);
 const src=m?.animation||(legacy?'assets/exercises/'+legacy+'.gif':null);
 assert.equal(r.animation_path,src);
 if(src){assert(/^(?:assets\/exercises\/e\d+\.gif|assets\/md500-3d\/md\d+\.gif)$/.test(src));assert(/^[a-f0-9]{40}$/.test(r.gif_blob_sha));linked++;}
 if(r.media_review_pending)review++;
}
const q=new Set(queue.map(x=>x.id));assert.equal(q.size,queue.length);
for(const r of inventory)assert.equal(q.has(r.id),!r.animation_path);
const json=JSON.parse(read('docs/COMPARACAO_LISTA_500.json'));assert.equal(json.summary.exercicios_com_midia,linked);
for(const x of json.items)assert.equal(x.animation_path,inventory[x.list_id-1].animation_path);
assert.equal(json.summary.revisao_pendente,review);
assert(html.includes('const mdBatch1Animated=new Set([]);'));
console.log(JSON.stringify({md:500,linked,pending:queue.length,in_review:review,new_3d:Object.keys(media).length}));

