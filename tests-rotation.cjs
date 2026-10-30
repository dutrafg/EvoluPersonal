#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8'),script=html.split('<script>')[1].split('</script>')[0];
const store=new Map(),nodes=new Map();
const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',classList:{toggle(){}},addEventListener(){}});return nodes.get(id)};
const ctx={console,Date,crypto:require('node:crypto').webcrypto,structuredClone,URL,
 window:{scrollTo(){}},confirm:()=>true,setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){},
 document:{body:{classList:{toggle(){}}},getElementById:node},
 localStorage:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('dist/training-methods.js','utf8'),ctx);
vm.runInContext(script,ctx);
const run=expr=>vm.runInContext(expr,ctx);
const check=(expr,expected)=>assert.deepEqual(JSON.parse(JSON.stringify(run(expr))),expected,expr);
check('validDB(seed())',true);
check('db.rotationPlan===undefined',true);
check('(()=>{planStudent=db.students[0].id;let w=db.workouts[0];editRotation("add",w.id);return [rotationRecord(planStudent).order.length,rotationRecord(planStudent).cursor,validDB(db)]})()',[1,0,true]);
check('(()=>{let w=db.workouts[0];editRotation("add",w.id);return rotationRecord(planStudent).order.length})()',1);
check('(()=>{editRotation("add","inexistente");return rotationRecord(planStudent).order.length})()',1);
check('(()=>{let w=db.workouts[0];let x=structuredClone(w);x.id="testB";x.title="Treino B";db.workouts.push(x);editRotation("add",x.id);return [rotationRecord(planStudent).order.length,validDB(db)]})()',[2,true]);
check('(()=>{editRotation("down",0);return rotationRecord(planStudent).order[rotationRecord(planStudent).cursor]===db.workouts[0].id})()',true);
check('(()=>{advanceRotationAfterSession(db.workouts[1]);return rotationRecord(planStudent).order[rotationRecord(planStudent).cursor]===db.workouts[0].id})()',true);
check('(()=>{advanceRotationAfterSession(db.workouts[0]);return rotationRecord(planStudent).order[rotationRecord(planStudent).cursor]==="testB"})()',true);
check('(()=>{let x=structuredClone(db);x.rotationPlan[x.students[0].id].order.push("inexistente");return validDB(x)})()',false);
check('(()=>{let x=structuredClone(db);x.rotationPlan[x.students[0].id].cursor=999;return validDB(x)})()',false);
check('(()=>{let x=structuredClone(db);x.rotationPlan[x.students[0].id].order.push(x.rotationPlan[x.students[0].id].order[0]);return validDB(x)})()',false);
check('(()=>{let x=structuredClone(db);x.rotationPlan["alunoInexistente"]={order:[],cursor:0};return validDB(x)})()',false);
check('(()=>{removeRotationWorkout("testB");return [rotationRecord(planStudent).order.length,rotationRecord(planStudent).cursor,validDB(db)]})()',[1,0,true]);
check('(()=>{editRotation("remove",0);return [rotationRecord(planStudent).order.length,rotationRecord(planStudent).cursor,validDB(db)]})()',[0,0,true]);
check('(()=>{clearData();return db.students.length===0&&Object.keys(db.rotationPlan).length===0&&validDB(db)})()',true);
assert(html.includes('advanceRotationAfterSession(w);delete db.drafts[id]'));
console.log('PASS: rotação A/B/C, ordenação, avanço, referências, exclusão, backup e migração compatível.');
