// Auditoria reproduzivel da biblioteca EvoluPersonal. Executar: node scripts/validar_cobertura_500.cjs
// Valida metadados, referencia de GIF, integridade do mapeamento e a fila de prioridades.
// A correspondencia cadastral nao substitui revisao anatomica/visual dos GIFs.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(base, p), 'utf8');
const html = read('dist/index.html');
const report = read('docs/COMPARACAO_LISTA_500.md');
const priority = JSON.parse(read('production/FILA_PRIORIDADE_COBERTURA_MD500.json'));
const mandatory = JSON.parse(read('docs/EXERCICIOS_OBRIGATORIOS_PDFS.json'));
const initial = [...html.matchAll(/^\['((?:\\'|[^'])+)','/gm)].map((m, i) => ({id:'e'+i, name:m[1], animation:'assets/exercises/e'+i+'.gif'}));
const jsonGroups = [...html.matchAll(/catalog\.push\(\.\.\.(\[\{"id":.*?\}\])\);/gs)]
  .flatMap(m => JSON.parse(m[1]));
const catalog = [...initial, ...jsonGroups];
const byId = new Map();
for(let i=0;i<catalog.length;i++){
  const x=catalog[i];
  assert.equal(x.id,'e'+i, 'ID ausente ou desordenado');
  assert(x.name && x.animation, 'Nome ou referencia de GIF ausente: '+x.id);
  assert.equal(x.animation,'assets/exercises/'+x.id+'.gif', 'GIF incompativel com o ID: '+x.id);
  assert(!byId.has(x.id), 'ID duplicado: '+x.id);
  byId.set(x.id,x);
  const gif=path.join(base,'dist',x.animation);
  assert(fs.existsSync(gif),'GIF ausente: '+gif);
  const fd=fs.openSync(gif,'r');
  let header=Buffer.alloc(6);
  try { assert.equal(fs.readSync(fd,header,0,6,0),6,'GIF vazio: '+gif); }
  finally { fs.closeSync(fd); }
  assert(['GIF87a','GIF89a'].includes(header.toString('ascii')), 'Arquivo nao e GIF: '+gif);
}
const lines=report.split('\n').filter(line=>/^\|\s*\d+\s*\|/.test(line));
assert.equal(lines.length,500,'A comparacao nao tem 500 linhas');
const statuses={ 'correspondência cadastrada':0,'variação relacionada; falta a exata':0,'a criar':0 };
const rows=new Map();
for(const [i,line] of lines.entries()){
  const cells=line.split('|').slice(1,-1).map(x=>x.trim());
  assert.equal(cells.length,4,'Linha malformada: '+line);
  const [number,name,status,ids]=cells;
  const n=Number(number);
  assert.equal(n,i+1,'Sequencia MD quebrada');
  assert(name.trim(),'Nome vazio na linha '+n);
  assert(Object.hasOwn(statuses,status),'Status invalido: '+status+' na linha '+n);
  statuses[status]++;
  const linked=ids?ids.split(',').map(x=>x.trim()):[];
  if(status==='a criar')assert.equal(linked.length,0,'Linha sem cobertura tem ID: '+n);
  else assert(linked.length>0,'Linha mapeada sem ID: '+n);
  for(const id of linked)assert(byId.has(id),'Linha '+n+' referencia GIF inexistente '+id);
  rows.set(n,{name,status,linked});
}
const match=report.match(/Linhas da lista com correspondência documental: \*\*(\d+)\*\*; relacionadas com variante exata pendente: \*\*(\d+)\*\*; demais a criar: \*\*(\d+)\*\*/);
assert(match,'Resumo de cobertura nao encontrado');
assert.deepEqual([+match[1],+match[2],+match[3]],[
 statuses['correspondência cadastrada'],statuses['variação relacionada; falta a exata'],statuses['a criar']
],'Resumo de cobertura desatualizado');
const open=statuses['variação relacionada; falta a exata']+statuses['a criar'];
assert.equal(priority.original_500.pending_total,open,'Fila desatualizada');
assert.equal(priority.original_500.documented_matches,statuses['correspondência cadastrada']);
assert.equal(priority.priority_batches.length,3,'A fila deve ter tres grupos de 25');
const picked=new Set();
for(const batch of priority.priority_batches){
 assert.equal(batch.items.length,25,'Lote prioritario diferente de 25: '+batch.code);
 for(const x of batch.items){
  assert(!picked.has(x.original_md_id),'Prioridade duplicada '+x.original_md_id);
  picked.add(x.original_md_id);
  assert.equal(x.status,rows.get(x.original_md_id)?.status,'Status da fila desatualizado: '+x.original_md_id);
  assert.notEqual(x.status,'correspondência cadastrada','Ja coberto entrou na fila: '+x.original_md_id);
 }
}
assert.equal(picked.size,75,'Nao existem 75 prioridades distintas');
const backlog=new Set(priority.remaining_backlog.map(x=>x.original_md_id));
assert.equal(backlog.size,priority.remaining_backlog.length,'Backlog duplicado');
for(const item of priority.remaining_backlog){
 const n=item.original_md_id;
 assert(!picked.has(n),'Backlog repetido nas prioridades: '+n);
 assert.equal(item.status,rows.get(n)?.status,'Status do backlog desatualizado: '+n);
 assert.notEqual(item.status,'correspondência cadastrada','Item ja coberto no backlog: '+n);
}
assert.equal(backlog.size+picked.size,open,'Fila e backlog nao cobrem todos os pendentes');
const remainingIds = new Set([...picked,...backlog]);
for(const [n,row] of rows)assert.equal(remainingIds.has(n),row.status!=='correspondência cadastrada','Pendencia ausente da fila: '+n);
assert.equal(mandatory.new_required.length,17,'Faltam obrigatorios no inventario');
for(const item of mandatory.new_required){
 assert(byId.has(item.catalog_id||item.proposed_id),'Obrigatorio sem cadastro '+item.name);
 assert(item.animation_status.includes('integrada ao catálogo'),'Status antigo de obrigatorio: '+item.name);
}
console.log(JSON.stringify({gifs_com_cabecalho_valido:catalog.length,linhas_md:lines.length,correspondencias:statuses['correspondência cadastrada'],variantes_a_revisar:statuses['variação relacionada; falta a exata'],a_criar:statuses['a criar'],fila_prioritaria:picked.size,backlog:backlog.size,obrigatorios_documentados:mandatory.new_required.length},null,2));
