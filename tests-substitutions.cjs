#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8'),methods=fs.readFileSync('dist/training-methods.js','utf8');
const script=html.split('<script>')[1].split('</script>')[0];
const store=new Map(),nodes=new Map();
const el=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',value:'',hidden:false,classList:{toggle(){}},addEventListener(){}});return nodes.get(id)};
const ctx={console,crypto:require('node:crypto').webcrypto,structuredClone,URL,Date,window:{scrollTo(){}},
 setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){},
 document:{body:{classList:{toggle(){}}},getElementById:el},
 localStorage:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}
};
vm.createContext(ctx);vm.runInContext(methods,ctx);vm.runInContext(script,ctx);
const run=x=>vm.runInContext(x,ctx);
const check=(expr,expected)=>assert.deepEqual(JSON.parse(JSON.stringify(run(expr))),expected,expr);
check('validDB(seed())',true);
check('(()=>{let x=seed();let w=x.workouts[0],e=x.exercises.find(e=>e.group===x.exercises.find(z=>z.id===w.items[0].exercise).group&&e.id!==w.items[0].exercise);w.items[0].alternatives=[e.id];return validDB(x)})()',true);
check('(()=>{let x=seed();x.workouts[0].items[0].alternatives=["md999"];return validDB(x)})()',false);
check('(()=>{let x=seed();let a=x.workouts[0].items[0];a.alternatives=[a.exercise];return validDB(x)})()',false);
check('(()=>{let x=seed();let a=x.workouts[0].items[0];a.alternatives=["md1","md1"];return validDB(x)})()',false);
check('(()=>{let w=db.workouts[0];var a=db.exercises.find(e=>e.group===exercise(w.items[0].exercise).group&&e.id!==w.items[0].exercise);w.items[0].alternatives=[a.id];db.drafts[w.id]=makeDraft(w);return validDB(db)})()',true);
check('(()=>{let w=db.workouts[0];chooseSubstitute(w.id,0,a.id);return [db.drafts[w.id].substitutions["0"],db.drafts[w.id].records.filter(r=>r.item===0).every(r=>r.exercise===a.id),validDB(db)]})()',[run('a.id'),true,true]);
check('(()=>{let w=db.workouts[0];return sessionView(w).includes("Exercício nesta sessão")&&sessionView(w).includes("Substituição do exercício")})()',true);
check('(()=>{let w=db.workouts[0];db.drafts[w.id].records[0].done=true;chooseSubstitute(w.id,0,w.items[0].exercise);return db.drafts[w.id].substitutions["0"]===a.id})()',true);
check('(()=>{let w=db.workouts[0];db.drafts[w.id].records[0].done=false;chooseSubstitute(w.id,0,w.items[0].exercise);return [db.drafts[w.id].substitutions["0"]===undefined,validDB(db)]})()',[true,true]);
check('(()=>{let w=db.workouts[0];db.drafts[w.id].substitutions={0:"md999"};return validDB(db)})()',false);
check('(()=>{let w=db.workouts[0];delete db.drafts[w.id].substitutions;return validDB(db)})()',true);
check('(()=>{let w=db.workouts[0];editor=structuredClone(w);editor.items[0].alternatives=[];document.getElementById("altPick-0").value=a.id;addAlternative(0);return [editor.items[0].alternatives[0],document.getElementById("editorItems").innerHTML.includes("Exercícios substitutos")]})()',[run('a.id'),true]);
check('(()=>{removeAlternative(0,a.id);return editor.items[0].alternatives.length})()',0);
assert(html.includes('function chooseSubstitute('));
assert(methods.includes('function substitutePickHTML('));
console.log('PASS: substitutos, bloqueio de séries concluídas, referências, editor e persistência.');
