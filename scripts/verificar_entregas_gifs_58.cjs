#!/usr/bin/env node
'use strict';
/**
 * Porta de liberação das 58 entregas. Um arquivo existente não equivale a
 * um GIF aprovado: exigem-se formato, resolução, quadros distintos, unicidade
 * de conteúdo e aceite humano nominal com SHA-256 correspondente.
 */
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const tasks=read('production/FILA_PRODUCAO_3D_MD500.json').items;
const approvals=read('production/APROVACOES_GIFS_MD500.json').approved;
const errors=[],seen=new Map(),result=[];
if(tasks.length!==58||new Set(tasks.map(x=>x.md_id)).size!==58)errors.push('A fila deve conter exatamente 58 IDs distintos.');
function info(b) {
 if(b.length<14||!['GIF87a','GIF89a'].includes(b.toString('ascii',0,6)))throw Error('Cabeçalho GIF inválido');
 let p=13,frames=0,end=false;
 const width=b.readUInt16LE(6),height=b.readUInt16LE(8);
 if(b[10]&128)p+=3*(1<<((b[10]&7)+1));
 function skip() {while(p<b.length){const n=b[p++];if(n===0)return;if(p+n>b.length)throw Error('Subbloco truncado');p+=n;}throw Error('Subbloco sem terminador');}
 while(p<b.length){
   const x=b[p++];
   if(x===0x3B){end=true;break;}
   if(x===0x21){if(p>=b.length)throw Error('Extensão truncada');p++;skip();continue;}
   if(x===0x2C){if(p+9>b.length)throw Error('Descritor truncado');const flag=b[p+8];p+=9;if(flag&128)p+=3*(1<<((flag&7)+1));if(p>=b.length)throw Error('Imagem truncada');p++;skip();frames++;continue;}
   throw Error('Bloco GIF inválido: '+x);
 }
 if(!end)throw Error('Trailer GIF ausente');
 return {width,height,frames};
}
for(const task of tasks){
 const id=task.md_id, target='MD'+id, file=path.join(root,'production/renderizados-md500',target+'.gif');
 if(!fs.existsSync(file)){errors.push(target+': GIF ainda não renderizado');result.push({id,status:'ausente'});continue;}
 let data,meta;try{data=fs.readFileSync(file);meta=info(data);}catch(e){errors.push(target+': '+e.message);result.push({id,status:'invalido'});continue;}
 const sha256=crypto.createHash('sha256').update(data).digest('hex');
 if(meta.width<400||meta.height<400)errors.push(target+': resolução '+meta.width+'x'+meta.height+' inferior a 400x400');
 if(meta.frames<6)errors.push(target+': GIF com '+meta.frames+' quadros (mínimo 6)');
 if(seen.has(sha256))errors.push(target+': conteúdo idêntico a MD'+seen.get(sha256));
 seen.set(sha256,id);
 const qa=approvals[String(id)];
 const approved=qa&&qa.approved===true&&qa.sha256===sha256
    &&typeof qa.reviewer==='string'&&qa.reviewer.trim().length>=3
    &&typeof qa.approved_at==='string'&&!Number.isNaN(Date.parse(qa.approved_at))
    &&qa.motion_correct===true&&qa.equipment_correct===true
    &&qa.anatomy_correct===true&&qa.range_correct===true;
 if(!approved)errors.push(target+': falta aprovação humana documentada e vinculada ao SHA-256');
 result.push({id,status:approved?'qa_aprovado':'qa_pendente',...meta,sha256});
}
const sum={exercicios_esperados:58,arquivos_encontrados:result.filter(x=>x.status!=='ausente').length,
  aprovados:result.filter(x=>x.status==='qa_aprovado').length,
  sem_arquivo:result.filter(x=>x.status==='ausente').length,
  erros:errors.length,concluido:errors.length===0};
console.log(JSON.stringify(sum,null,2));
if(errors.length){console.error(errors.slice(0,30).join('\n'));process.exitCode=1;}
