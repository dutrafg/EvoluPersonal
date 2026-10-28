const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const bootstrap=fs.readFileSync('tests.cjs','utf8').split('let n=0;')[0];
const checks=`
const current=JSON.parse(JSON.stringify(vm.runInContext('catalog',ctx)));
assert.equal(current.length,425);
assert.equal(new Set(current.map(e=>e.id)).size,425);
const previous=JSON.parse(fs.readFileSync('production/catalog-400.json','utf8'));
for(const e of previous){const now=current.find(x=>x.id===e.id);assert(now);assert.equal(now.name,e.name);assert.equal(now.animation,e.animation);}
const plan=JSON.parse(fs.readFileSync('production/lote17-plan.json','utf8'));
assert.equal(plan.length,25);assert.equal(new Set(plan.map(e=>e.list_id)).size,25);
for(const e of current){assert(fs.existsSync('dist/'+e.animation),e.id);}
for(const e of plan){assert.equal(current.find(x=>x.id===e.id).name,e.name);assert(fs.existsSync('production/sprites/'+e.id+'.png'));assert(fs.existsSync('production/'+e.id+'-source.json'));}
assert(vm.runInContext('validDB(JSON.parse(JSON.stringify(db)))',ctx));
vm.runInContext("libSearch='Serrote no Smith';group='Costas'",ctx);
assert(vm.runInContext('libraryCards()',ctx).includes('e423.gif'));
assert(!vm.runInContext('libraryCards()',ctx).includes('e400.gif'));
vm.runInContext("group='Peito'",ctx);
assert(!vm.runInContext('libraryCards()',ctx).includes('e423.gif'));
console.log('Mídia: 425 IDs e caminhos; preservação dos 400 anteriores; 25 vínculos MD e originais; restauração e filtro combinado passaram.');
`;
eval(bootstrap+checks);
