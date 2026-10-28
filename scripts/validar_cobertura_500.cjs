// QA do catálogo exclusivo MD500. Rode: node scripts/validar_cobertura_500.cjs
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('dist/index.html');
const matched=html.match(/const md500Rows=(\[\[.*?\]\]);/s);
assert(matched,'Array MD500 ausente do HTML');
const official=JSON.parse(matched[1]);
assert.equal(official.length,500);
const lines=read('docs/COMPARACAO_LISTA_500.md').split('\n').filter(x=>/^\|\s*\d+\s*\|/.test(x));
assert.equal(lines.length,500);
const entries=lines.map((line,i)=>{
 const p=line.split('|').slice(1,-1).map(x=>x.trim());
 assert.equal(p.length,3,'Linha malformada '+(i+1));
 const [number,name,media]=p;
 assert.equal(Number(number),i+1,'Ordem inválida');
 assert.equal(name,official[i][0],'Nome divergente do MD: '+number);
 const ref=media.replace(/\x60/g,'');
 assert(ref==='—'||/^(e|md)\d+$/.test(ref),'Referência inválida: '+number);
 return {id:i+1,name,ref};
});
const mapped=entries.filter(x=>x.ref!=='—');
assert.equal(mapped.length,314);assert.equal(entries.length-mapped.length,186);
const batch=JSON.parse(read('production/lote-md500-01.json'));
assert.equal(batch.files.length,30);
const batchIDs=new Set(batch.files.map(x=>x.md_id));
assert.equal(batchIDs.size,30);
const codeIDs=JSON.parse((html.match(/const mdBatch1Animated=new Set\((\[[^\]]+\])\)/)||[])[1]||'null');
assert.deepEqual(new Set(codeIDs),batchIDs,'IDs do lote não coincidem com o aplicativo');
const signatures=new Set();
function gifInfo(p){
 const bytes=fs.readFileSync(path.join(root,p));
 assert(['GIF87a','GIF89a'].includes(bytes.subarray(0,6).toString('ascii')),'Cabeçalho inválido: '+p);
 assert(bytes.length>300,'GIF curto: '+p);
 let off=13;if(bytes[10]&128)off+=3*(1<<((bytes[10]&7)+1));
 let frames=0;
 while(off<bytes.length){
  const type=bytes[off++];
  if(type===0x3b)break;
  if(type===0x21){off++;while(true){const n=bytes[off++];if(!n)break;off+=n;}continue;}
  assert.equal(type,0x2c,'Bloco GIF corrompido: '+p);
  const flags=bytes[off+8];off+=9;
  if(flags&128)off+=3*(1<<((flags&7)+1));
  off++;
  while(true){const n=bytes[off++];if(!n)break;off+=n;}
  frames++;
 }
 assert.equal(bytes[off-1],0x3b,'Arquivo GIF sem terminador: '+p);
 return {frames,width:bytes.readUInt16LE(6),height:bytes.readUInt16LE(8),hash:crypto.createHash('sha256').update(bytes).digest('hex')};
}
for(const entry of mapped){
 const newGIF=entry.ref.startsWith('md');
 const p=newGIF?'dist/assets/md500/'+entry.ref+'.gif':'dist/assets/exercises/'+entry.ref+'.gif';
 const info=gifInfo(p);
 if(newGIF){
  assert(batchIDs.has(entry.id),'GIF MD não declarado no lote: '+entry.id);
  assert.equal(info.frames,10);assert.equal(info.width,144);assert.equal(info.height,144);
  assert(!signatures.has(info.hash),'GIF repetido: '+p);
  signatures.add(info.hash);
 }
}
assert.equal(signatures.size,30);
const queue=JSON.parse(read('production/FILA_PRIORIDADE_COBERTURA_MD500.json'));
assert.equal(queue.batch_size,30);assert.equal(queue.to_produce,186);
assert.equal(queue.next_batch.length,30);assert.equal(queue.remaining_after_next.length,156);
const queued=new Set([...queue.next_batch,...queue.remaining_after_next].map(x=>x.md_id));
assert.equal(queued.size,186);
for(const entry of entries)assert.equal(queued.has(entry.id),entry.ref==='—','Fila divergente: '+entry.id);
console.log(JSON.stringify({original_md:500,with_gif:mapped.length,distinct_new_gifs:signatures.size,remaining:queued.size,next_batch:queue.batch_size},null,2));
