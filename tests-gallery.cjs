#!/usr/bin/env node
'use strict';
// Regression tests of the "Imagem 2" gallery, using the real dist/index.html without a browser.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const src=fs.readFileSync(path.join(__dirname,'dist/index.html'),'utf8');
const methods=fs.readFileSync(path.join(__dirname,'dist/training-methods.js'),'utf8');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'production/lote-md500-25-01.json'),'utf8'));
const match=src.match(/<script>\s*('use strict';[\s\S]*?)<\/script>/);
assert(match,'Main script not found');
const store=new Map(),nodes=new Map();
function element(id){if(!nodes.has(id))nodes.set(id,{id,innerHTML:'',textContent:'',hidden:false,addEventListener(){},classList:{toggle(){}},getBoundingClientRect(){return {left:0,right:100,top:0,bottom:100}}});return nodes.get(id)}
const document={body:{classList:{toggle(){}}},getElementById:element};
const localStorage={getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)};
const clone=x=>JSON.parse(JSON.stringify(x));
const suffix=[
"go('book');",
"const rendered=document.getElementById('app').innerHTML;",
"const first=libraryCards();",
"const initial=JSON.parse(localStorage.getItem(KEY));",
"function select(status){mdLibraryStatus=status;mdLibraryPage=0;return libraryCards()}",
"const done=select('animated'),pending=select('pending'),active=select('batch');",
"mdLibraryStatus='all';mdLibraryPage=0;const firstPage=libraryCards();",
"mdLibraryPage=9;const lastPage=libraryCards();",
"mdLibraryPage=0;libSearch='Supino';const search=libraryCards();",
"libSearch='';group='Pernas';const legs=libraryCards();",
"return {rendered,first,initial,done,pending,active,firstPage,lastPage,search,legs,currentIds:[...mdCurrentBatchIds]};"
].join('\n');
const outcome=Function('document','window','localStorage','crypto','structuredClone','URL','setTimeout','clearTimeout','setInterval','clearInterval',methods+'\n'+match[1]+'\n'+suffix)(
 document,{scrollTo(){}},localStorage,{randomUUID:()=>('t'+Date.now())},clone,URL,()=>1,()=>{},()=>1,()=>{});
const count=s=>(s.match(/class="md-exercise"/g)||[]).length;
assert.equal(outcome.initial.exercises.filter(x=>/^md\d+$/.test(x.id)).length,500);
assert.equal(outcome.initial.exercises.filter(x=>/^md\d+$/.test(x.id)&&x.animation).length,295);
assert.deepEqual(outcome.currentIds,manifest.items.map(x=>x.md_id));
assert.equal(count(outcome.first),50);
assert.equal(count(outcome.firstPage),50);
assert.equal(count(outcome.lastPage),50);
assert.equal(count(outcome.done),50);
assert.equal(count(outcome.pending),50);
assert.equal(count(outcome.active),25);
assert.equal((outcome.active.match(/GIF 3D pendente/g)||[]).length,25);
assert(!outcome.active.includes('src="assets/'),'Current batch must not contain fabricated GIFs');
assert(outcome.done.includes('<img') && outcome.done.includes('src="assets/exercises/e'));
assert(!outcome.pending.includes('<img'),'Pending exercises must not display a stock GIF');
assert(outcome.search.includes('Supino')&&!outcome.search.includes('Agachamento Livre'));
assert(outcome.legs.includes('Leg Press')&&!outcome.legs.includes('Supino Reto'));
assert(outcome.rendered.includes('md-gallery')&&outcome.rendered.includes('mdLibraryPager'));
assert(src.includes('.md-gallery .md-gallery-grid{display:grid;grid-template-columns:repeat(5'));
assert(src.includes('@media(max-width:440px)'));
assert(!src.includes('<script src="md-gifs.js"></script>'),'Rejected 2D assets must stay disabled');
console.log('PASS: gallery checks (source=500, GIFs=295, pending=205, batch=25, pagination, responsive, no invented animation).');
