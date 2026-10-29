'use strict';
/**
 * EvoluPersonal MD500 — validação de correspondências estruturais.
 * Verifica nomes, IDs, caminhos, cabeçalho GIF e inventário de mídia.
 * NÃO aprova biomecânica nem verifica visualmente a execução.
 * Uso: node scripts/validar_associacoes_md500.cjs
 *      node scripts/validar_associacoes_md500.cjs --sha
 *      node scripts/validar_associacoes_md500.cjs --review /caminho/revisao.json
 */
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const inventory=JSON.parse(read('production/INVENTARIO_MD500.json'));
const comparison=JSON.parse(read('docs/COMPARACAO_LISTA_500.json'));
const original=read('docs/500-exercicios-base.md');
const html=read('dist/index.html');
const auditoria=read('dist/revisao-vinculos-md500.html');
const rows=JSON.parse(html.match(/const md500Rows=(\[\[.*?\]\]);/s)?.[1]||'null');
const md3d=JSON.parse(html.match(/const md3dMedia=(\{.*?\});\n/s)?.[1]||'null');
const pageEntries=JSON.parse(auditoria.match(/const ITEMS=(\[.*?\]);\nconst ASSETS=/s)?.[1]||'null');
const pageAssets=JSON.parse(auditoria.match(/const ASSETS=(\[.*?\]);\nconst byId=/s)?.[1]||'null');
const script=auditoria.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert(script,'Script da galeria ausente');
new vm.Script(script,{filename:'dist/revisao-vinculos-md500.html'});
assert.equal(inventory.length,500);
assert.equal(rows.length,500);
assert.equal(comparison.items.length,500);
assert.equal(pageEntries.length,500);
assert.equal(original.split(/\r?\n/).filter(x=>/^\s*\d+\.\s/.test(x)).length,500);
const abs=p=>path.join(root,'dist',p);
const seen=new Map(),warnings=[],missing=[],paths=new Set(pageAssets.map(x=>x.path));
let linked=0,new3d=0,review=0,legacy=0;
for(let i=0;i<500;i++){
 const row=inventory[i],doc=comparison.items[i],page=pageEntries[i];
 assert.equal(row.id,i+1);
 assert.equal(doc.list_id,i+1);
 assert.equal(page.id,i+1);
 assert.equal(row.name,doc.name);
 assert.equal(row.name,page.name);
 assert.equal(row.name,rows[i][0]);
 assert.equal(row.animation_path,doc.animation_path);
 assert.equal(row.animation_path,page.path||null);
 assert.equal(row.media_review_pending,page.reviewListed);
 if(row.media_review_pending)review++;
 if(!row.animation_path){missing.push(row.id);continue}
 linked++;
 const p=row.animation_path;
 assert.match(p,/^assets\/(?:exercises\/e\d+|md500-3d\/md\d+)\.gif$/);
 assert(!p.startsWith('assets/md500/'),'GIFs 2D reprovados não podem ser usados');
 assert(paths.has(p),'GIF fora do inventário da página: '+p);
 assert(fs.existsSync(abs(p)),'Arquivo GIF não encontrado: '+p);
 const buffer=fs.readFileSync(abs(p));
 assert(['GIF87a','GIF89a'].includes(buffer.subarray(0,6).toString('ascii')),'Arquivo não é um GIF: '+p);
 assert(buffer.length>100,'GIF vazio: '+p);
 if(process.argv.includes('--sha')){
   const header=Buffer.from('blob '+buffer.length+'\0');
   const sha=crypto.createHash('sha1').update(header).update(buffer).digest('hex');
   assert.equal(sha,row.gif_blob_sha,'Hash inesperado: '+p);
 }
 const old=seen.get(p)||[];old.push(row.id);seen.set(p,old);
 if(p.startsWith('assets/md500-3d/')){
   new3d++;
   assert.equal(p,'assets/md500-3d/md'+row.id+'.gif','GIF novo de MD incorreto: '+row.id);
   assert.equal(md3d[String(row.id)]?.animation,p,'Mapa do app divergente: '+row.id);
 }else{
   legacy++;
   assert.equal(p,'assets/exercises/'+rows[i][1]+'.gif','Mapa legado divergente: '+row.id);
 }
}
assert.equal(linked+missing.length,500);
assert.deepEqual(Object.keys(md3d).map(Number).sort((a,b)=>a-b),inventory.filter(x=>x.animation_path?.includes('md500-3d/')).map(x=>x.id).sort((a,b)=>a-b));
const grouped=[...seen].filter(([,ids])=>ids.length>1).map(([media,ids])=>({media,ids}));
for(const x of grouped)warnings.push('Arquivo compartilhado: '+x.media+' → MD'+x.ids.join('/MD'));
for(const id of [46,135,140,301,302,319,340,341,357,471]) assert(pageEntries[id-1].priority,'Prioridade ausente: MD'+id);
warnings.push('MD471/e69: conferir se o GIF realmente mostra joelhos flexionados');
const reviewIndex=process.argv.indexOf('--review');
if(reviewIndex!==-1){
 const p=process.argv[reviewIndex+1];
 assert(p,'Informe o JSON de revisão');
 const data=JSON.parse(fs.readFileSync(p,'utf8'));
 assert.equal(data.kind,'auditoria_de_correspondencias');
 for(const r of data.items||[]){
  const exercise=inventory[r.md_id-1];
  assert(exercise,'MD desconhecido: '+r.md_id);
  assert.equal(r.originalSha,exercise.gif_blob_sha||'','Vínculo mudou após a revisão: MD'+r.md_id);
  assert(['pendente','aprovado','reprovado'].includes(r.status));
  if(r.status==='aprovado'){
   assert(r.checks?.length===4&&r.checks.every(Boolean),'Aprovação sem quatro critérios MD'+r.md_id);
   assert(r.proposedPath||exercise.animation_path,'Aprovação sem GIF MD'+r.md_id);
  }
  if(r.status==='reprovado')assert(String(r.notes||'').trim(),'Reprovação sem justificativa MD'+r.md_id);
  if(r.proposedPath)assert(paths.has(r.proposedPath),'Proposta de mídia inexistente MD'+r.md_id);
 }
}
const result={md:500,linked,pending:missing.length,new3d,legacy,review_flagged:review,unique_gif_links:seen.size,shared_files:grouped,review_tool_records:pageEntries.length,review_tool_assets:pageAssets.length,review_tool_script:'syntax_ok',sha_checked:process.argv.includes('--sha'),warnings};
console.log(JSON.stringify(result,null,2));
