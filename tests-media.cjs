'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8'),code=html.split('<script>')[1].split('</script>')[0];
const nodes=new Map(),stored=new Map();
function boot(){const ctx={console,crypto:require('crypto').webcrypto,structuredClone,URL,Date,setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},document:{body:{classList:{toggle(){}}},getElementById(id){if(!nodes.has(id))nodes.set(id,{classList:{toggle(){}},addEventListener(){}});return nodes.get(id)}}};vm.createContext(ctx);vm.runInContext(fs.readFileSync('dist/training-methods.js','utf8'),ctx);vm.runInContext(code,ctx);return ctx}
let ctx=boot();
const catalog=JSON.parse(vm.runInContext('JSON.stringify(catalog)',ctx));
const inventory=JSON.parse(fs.readFileSync('production/INVENTARIO_MD500.json','utf8'));
const items=[1,2,3,4].flatMap(n=>JSON.parse(fs.readFileSync('production/lote-md500-25-0'+n+'.json','utf8')).items).concat(JSON.parse(fs.readFileSync('production/lote-md500-24-05.json','utf8')).items,JSON.parse(fs.readFileSync('production/lote-md500-25-06.json','utf8')).items);
assert.equal(vm.runInContext('legacyCatalog.length',ctx),425);
assert.equal(vm.runInContext('mdBatch1Animated.size',ctx),0);
assert.equal(catalog.length,500);assert.equal(new Set(catalog.map(e=>e.id)).size,500);
for(const row of inventory){const e=catalog[row.id-1];assert.equal(e.name,row.name);assert.equal(e.animation,row.animation_path||'');if(e.animation)assert(/^[a-f0-9]{40}$/.test(row.gif_blob_sha));}
assert.equal(items.length,149);assert.equal(new Set(items.map(e=>e.md_id)).size,149);
for(const item of items){const e=catalog[item.md_id-1];assert.equal(e.animation,item.output_path.replace(/^dist\//,''));assert.equal(e.media_review_pending,true);assert(vm.runInContext('exerciseArt(catalog['+(item.md_id-1)+'])',ctx).includes('src="'+e.animation+'"'));}
for(const invalid of ['assets/md500/md292.gif','https://evil.invalid/1.gif','assets/md500-3d/../x.gif','javascript:alert(1)']){ctx.invalid=invalid;assert.equal(vm.runInContext('mdMediaSource({animation:invalid})',ctx),'');}
const key=vm.runInContext('KEY',ctx),old=JSON.parse(stored.get(key));
old.students[0].notes='Preservar observação do aluno';old.workouts[0].notes='Preservar treino';
for(const e of old.exercises){if(items.some(x=>x.md_id===e.md_id))e.animation='';delete e.media_review_pending;delete e.media_batch;}
old.exercises.find(e=>e.id==='md357').animation='';
stored.set(key,JSON.stringify(old));ctx=boot();
assert.equal(vm.runInContext('db.students[0].notes',ctx),'Preservar observação do aluno');
assert.equal(vm.runInContext('db.workouts[0].notes',ctx),'Preservar treino');
assert.equal(vm.runInContext('db.exercises.filter(e=>e.animation).length',ctx),445);
assert.equal(vm.runInContext('db.exercises.filter(e=>e.media_review_pending).length',ctx),155);
assert(vm.runInContext('validDB(db)',ctx));
console.log('PASS: 149 associações, arquivos no inventário remoto, caminhos seguros e atualização da base antiga sem perder dados.');

