#!/usr/bin/env node
// Verifica o próximo lote de 25 da fonte MD. Não transforma renders 2D em aprovação 3D.
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const batch=JSON.parse(read('production/lote-md500-25-01.json'));
const queue=JSON.parse(read('production/FILA_PRIORIDADE_COBERTURA_MD500.json'));
const html=read('dist/index.html');
const allMD=JSON.parse((html.match(/const md500Rows=(\[\[.*?\]\]);/s)||[])[1]||'null');
assert.equal(allMD.length,500,'O catálogo precisa ter 500 exercícios originais');
assert.equal(batch.items.length,25,'O lote deve ter exatamente 25 exercícios');
assert.equal(queue.batch_size,25,'Cadência incorreta');
assert.equal(queue.next_batch.length,25,'Fila de 25 alterada');
const ids=new Set();
let approved=0;
const signatures=new Set();
for(let i=0;i<25;i++){
 const a=batch.items[i],b=queue.next_batch[i];
 assert.equal(a.md_id,b.md_id,'Ordem do lote difere da fila');
 assert.equal(a.name,allMD[a.md_id-1][0],'Nome deve ser idêntico ao MD');
 assert(!ids.has(a.md_id),'Mesmo número MD repetido');
 ids.add(a.md_id);
 assert(Array.isArray(a.poses)&&a.poses.length===6,'Seis poses específicas obrigatórias: '+a.md_id);
 assert(a.poses.every(s=>typeof s==='string'&&s.length>=24),'Descrição de pose insuficiente: '+a.md_id);
 assert(a.equipment&&a.camera&&a.highlighted_muscles?.length>0);
 const expected='dist/assets/md500-3d/md'+a.md_id+'.gif';
 assert.equal(a.output_path,expected);
 if(a.status==='aguardando_geracao_3d'){
  assert.equal(a.visual_qa_approved,false);
  continue;
 }
 assert.equal(a.status,'aprovado_3d','Status do GIF inválido: '+a.md_id);
 assert.equal(a.visual_qa_approved,true,'GIF sem aprovação visual');
 assert.equal(a.render_validated,true,'GIF sem verificação dos quadros');
 const file=path.join(root,expected);
 assert(fs.existsSync(file),'Arquivo aprovado não existe: '+expected);
 const data=fs.readFileSync(file);
 assert.equal(data.subarray(0,6).toString('ascii'),'GIF89a','GIF inválido: '+expected);
 const w=data.readUInt16LE(6),h=data.readUInt16LE(8);
 assert(w>=400&&h>=400,'Resolução inferior ao padrão: '+expected);
 const digest=crypto.createHash('sha256').update(data).digest('hex');
 assert(!signatures.has(digest),'GIF idêntico reutilizado para dois exercícios: '+expected);
 signatures.add(digest);
 approved++;
}
assert.equal(batch.completed_gifs,approved,'Contagem de GIFs aprovados inconsistente');
if(batch.status==='CONCLUIDO')assert.equal(approved,25,'Lote marcado concluído antes de 25 GIFs');
console.log(JSON.stringify({lote:batch.batch,exercicios_md:ids.size,gifs_3d_aprovados:approved,restantes_no_lote:25-approved,publicavel:approved===25},null,2));
