#!/usr/bin/env node
'use strict';
/**
 * Auditoria integral da biblioteca MD500. Não considera arquivo existente como
 * prova de fidelidade anatômica; essa etapa requer revisão visual independente.
 * Uso: node scripts/auditar_md500_integral.cjs [--write]
 */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const stock = read('production/INVENTARIO_MD500.json');
const pending = read('production/FILA_MD500_ATUAL.json');
const production = read('production/FILA_PRODUCAO_3D_MD500.json');
const html = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
const match = html.match(/const md500Rows=(\[\[.*?\]\]);/s);
const rows = match ? JSON.parse(match[1]) : [];
const errors = [], notices = [], distributions = {}, digestOwners = new Map();
let linked = 0, assetsPresent = 0, verifiedBlob = 0, 3dLinked = 0;
let insufficient3d = 0, staticGifs = 0, unusualGifs = 0;
const details = [];

function parseGif(b) {
  if (b.length < 14 || !['GIF87a','GIF89a'].includes(b.toString('ascii', 0, 6))) throw Error('assinatura GIF inválida');
  let width=b.readUInt16LE(6), height=b.readUInt16LE(8), p=13, frames=0, end=false;
  const packed = b[10]; if (packed & 0x80) p += 3 * (1 << ((packed & 7) + 1));
  function blocks() {
    while(p < b.length) {
      const n=b[p++]; if(!n) return;
      if(p + n > b.length) throw Error('sub-bloco incompleto');
      p+=n;
    }
    throw Error('sub-blocos sem terminador');
  }
  while(p < b.length) {
    const type=b[p++];
    if(type===0x3B) {end=true;break;}
    if(type===0x21) {if(p>=b.length)throw Error('extensão truncada');p++;blocks();continue;}
    if(type===0x2C) {
      if(p+9>b.length)throw Error('descritor truncado');
      const flag=b[p+8]; p+=9;
      if(flag & 0x80) p+=3*(1<<((flag&7)+1));
      if(p>=b.length)throw Error('dados de imagem ausentes');
      p++;blocks();frames++;continue;
    }
    throw Error('marcador GIF inesperado: '+type);
  }
  if(!end || frames<1)throw Error('GIF sem trailer ou quadros');
  return {width,height,frames};
}
if(stock.length!==500 || rows.length!==500)errors.push('Catálogo deve ter exatamente 500 itens.');
const missingSet=new Set(pending.map(x=>x.id));
const tasks=production.items || [];
if(pending.length!==55 || missingSet.size!==55)errors.push('Fila original não tem 55 IDs únicos.');
if(tasks.length!==58 || new Set(tasks.map(x=>x.md_id)).size!==58)errors.push('Fila de produção não tem 58 IDs únicos.');
for(let i=0;i<stock.length;i++){
  const x=stock[i], id=i+1;
  if(x.id!==id || !rows[i] || rows[i][0]!==x.name)errors.push('Inconsistência entre catálogo e inventário MD'+id);
  if(missingSet.has(id)!==!x.animation_path)errors.push('Fila de ausentes diverge do MD'+id);
  if(!x.animation_path)continue;
  linked++;
  if(!/^assets\/(exercises\/e\d+|md500-3d\/md\d+)\.gif$/.test(x.animation_path)){errors.push('Caminho inválido MD'+id);continue;}
  const f=path.join(root,'dist',x.animation_path);
  if(!fs.existsSync(f)){errors.push('Mídia não encontrada MD'+id+': '+x.animation_path);continue;}
  assetsPresent++;
  const b=fs.readFileSync(f);
  const sha=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
  if(sha!==x.gif_blob_sha)errors.push('SHA não corresponde ao inventário MD'+id);
  else verifiedBlob++;
  const already=digestOwners.get(sha);
  if(already) notices.push('Mídia duplicada MD'+already+' e MD'+id);
  else digestOwners.set(sha,id);
  let g;
  try {g=parseGif(b);}catch(e){errors.push('MD'+id+' '+e.message);continue;}
  const dims=g.width+'x'+g.height;
  distributions[dims]=(distributions[dims]||0)+1;
  const newly3d=Boolean(x.new_gif);
  if(newly3d) {
    3dLinked++;
    if(g.width<400 || g.height<400){insufficient3d++;errors.push('MD'+id+' 3D '+dims+' inferior ao mínimo de 400x400');}
    if(g.frames<6){errors.push('MD'+id+' 3D com somente '+g.frames+' quadro(s)');}
  }
  if(g.frames<2){staticGifs++;notices.push('GIF com quadro único MD'+id);}
  if(g.width<80 || g.height<80){unusualGifs++;notices.push('GIF muito pequeno MD'+id);}
  details.push({md_id:id,ref:x.ref,path:x.animation_path,sha1:sha,width:g.width,height:g.height,frames:g.frames,new3d:newly3d,review_status:x.review_status});
}
const taskSet=new Set(tasks.map(x=>x.md_id));
for(const id of missingSet)if(!taskSet.has(id))errors.push('MD'+id+' ausente da fila de produção');
const shared=notices.filter(x=>x.startsWith('Mídia duplicada'));
const status=(linked===500 && errors.length===0 && shared.length===0 && production.items.every(x=>x.visual_qa_approved===true))?'APTO_A_REVISAO_FINAL':'INCOMPLETO';
const report={
  generated_utc:new Date().toISOString(),status,
  summary:{source_exercises:stock.length,linked,without_gif:stock.length-linked,
    assets_present:assetsPresent,sha_verified:verifiedBlob,new3d_linked:3dLinked,
    new3d_below_400px:insufficient3d,one_frame_gifs:staticGifs,very_small_gifs:unusualGifs,
    production_tasks:tasks.length,exact_shared_gifs:shared.length,
    visual_review_pending:stock.filter(x=>x.media_review_pending).length,
    image_dimensions:distributions,errors:errors.length,notices:notices.length},
  errors,notices,details
};
if(process.argv.includes('--write')) {
 const outfile=path.join(root,'production/RELATORIO_AUDITORIA_MD500.json');
 fs.writeFileSync(outfile,JSON.stringify(report,null,2)+'\n');
}
console.log(JSON.stringify(report.summary,null,2));
console.log('Resultado:',status);
if(errors.length)console.log('Primeiros problemas:',errors.slice(0,20).join(' | '));
if(status!=='APTO_A_REVISAO_FINAL')process.exitCode=1;
