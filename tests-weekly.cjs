#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8');
const script=html.split('<script>')[1].split('</script>')[0];
const storage=new Map(),nodes=new Map();
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',classList:{toggle(){}},addEventListener(){}});return nodes.get(id)}
const ctx={
 console,crypto:require('node:crypto').webcrypto,structuredClone,URL,Date,
 setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){},
 confirm:()=>true,window:{scrollTo(){}},
 document:{body:{classList:{toggle(){}}},getElementById:node},
 localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('dist/training-methods.js','utf8'),ctx);
vm.runInContext(fs.readFileSync('dist/insights.js','utf8'),ctx);
vm.runInContext(script,ctx);
const check=(expression,expected)=>assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext(expression,ctx))),expected,expression);
check('validDB(seed())',true);
check('weekPlanner().includes("Planejamento semanal")',true);
check('db.weekPlan===undefined',true);
check('WEEK_DAYS.length',7);
check('(()=>{planStudent=db.students[0].id;assignWeek("seg",db.workouts[0].id);return db.weekPlan[planStudent].seg===db.workouts[0].id})()',true);
check('validDB(db)',true);
check('validDB(JSON.parse(localStorage.getItem(KEY)))',true);
check('(()=>{let x=structuredClone(db);x.weekPlan[x.students[0].id].seg="inexistente";return validDB(x)})()',false);
check('(()=>{let x=structuredClone(db);x.weekPlan[x.students[0].id].invalido=x.workouts[0].id;return validDB(x)})()',false);
check('(()=>{assignWeek("seg","id-inexistente");return db.weekPlan[planStudent].seg===db.workouts[0].id})()',true);
check('(()=>{assignWeek("seg","");return db.weekPlan[planStudent].seg===undefined})()',true);
check('validDB(db)',true);
check('(()=>{assignWeek("ter",db.workouts[0].id);let id=db.workouts[0].id;deleteWorkout(id);return db.weekPlan[planStudent].ter===undefined})()',true);
check('validDB(db)',true);
check('(()=>{clearData();return db.students.length===0&&Object.keys(db.weekPlan).length===0&&validDB(db)})()',true);
assert(html.includes('function purgeWeekAssignments(workoutId)'));
assert(html.includes("weekPlanner()+rotationPlanner()}"));
console.log('PASS: agenda semanal, persistência, backup, vínculos e exclusão segura de treinos.');
