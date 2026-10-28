#!/usr/bin/env node
'use strict';
// Regression tests of the "Imagem 2" gallery, using the real dist/index.html without a browser.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const src=fs.readFileSync(path.join(__dirname,'dist/index.html'),'utf8');
const methods=fs.readFileSync(path.join(__dirname,'dist/training-methods.js'),'utf8');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'production/lote-md500-25-04.json'),'utf8'));
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
"const done=select('animated'),pending=select('pending'),active=select('batch'),review=select('review');mdLibraryPage=1;const reviewLast=libraryCards();mdLibraryPage=2;const reviewThird=libraryCards();",
"mdLibraryStatus='all';mdLibraryPage=0;const firstPage=libraryCards();",
"mdLibraryPage=9;const lastPage=libraryCards();",
"mdLibraryPage=0;libSearch='Supino';const gallerySearch=libraryCards();",
"libSearch='';group='Pernas';const galleryLegs=libraryCards();",
"return {rendered,first,initial,done,pending,active,firstPage,lastPage,gallerySearch,galleryLegs,review,reviewLast,reviewThird,currentIds:[...mdCurrentBatchIds]};"
].join('\n');
const outcome=Function('document','window','localStorage','crypto','structuredClone','URL','setTimeout','clearTimeout','setInterval','clearInterval',methods+'\n'+match[1]+'\n'+suffix)(
 document,{scrollTo(){}},localStorage,{randomUUID:()=>('t'+Date.now())},clone,(typeof URL==='undefined'?class FakeURL{}:URL),()=>1,()=>{},()=>1,()=>{});
const count=s=>(s.match(/class="md-exercise"/g)||[]).length;
assert.equal(outcome.initial.exercises.filter(x=>/^md\d+$/.test(x.id)).length,500);
assert.equal(outcome.initial.exercises.filter(x=>/^md\d+$/.test(x.id)&&x.animation).length,396);
assert.deepEqual(outcome.currentIds,manifest.items.map(x=>x.md_id));
assert.equal(count(outcome.first),50);
assert.equal(count(outcome.firstPage),50);
assert.equal(count(outcome.lastPage),50);
assert.equal(count(outcome.done),50);
assert.equal(count(outcome.pending),50);
assert.equal(count(outcome.active),25);
assert.equal((outcome.active.match(/GIF 3D pendente/g)||[]).length,0);
assert(outcome.active.includes('src="assets/md500-3d/md'),'Current batch must use its produced 3D files');
assert(outcome.done.includes('<img') && outcome.done.includes('src="assets/exercises/e'));
assert(!outcome.pending.includes('<img'),'Pending exercises must not display a stock GIF');
assert(outcome.gallerySearch.includes('Supino')&&!outcome.gallerySearch.includes('Agachamento Livre'));
assert(outcome.galleryLegs.includes('Leg Press')&&!outcome.galleryLegs.includes('Supino Reto'));
assert(outcome.rendered.includes('md-gallery')&&outcome.rendered.includes('mdLibraryPager'));
assert(src.includes('.md-gallery .md-gallery-grid{display:grid;grid-template-columns:repeat(5'));
assert(src.includes('@media(max-width:440px)'));
assert(!src.includes('<script src="md-gifs.js"></script>'),'Rejected 2D assets must stay disabled');

assert.equal(outcome.initial.exercises.filter(e=>e.media_review_pending).length,101);
assert.equal(count(outcome.review),50);
assert.equal(count(outcome.reviewLast),50);
assert.equal(count(outcome.reviewThird),1);
assert.equal((outcome.active.match(/GIF vinculado · em revisão/g)||[]).length,25);
assert(outcome.rendered.includes('101</strong> em revisão'));
assert(outcome.rendered.includes('value="review"'));
assert.equal(outcome.initial.exercises.find(e=>e.id==='md16').animation,'assets/exercises/e402.gif');
assert.equal(outcome.initial.exercises.find(e=>e.id==='md357').animation,'assets/exercises/e141.gif');
console.log('PASS: galeria MD500, 396 vínculos, 104 pendentes, 101 em revisão, lote atual 25 e paginação.');


