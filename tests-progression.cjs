#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8');
const script=html.split('<script>')[1].split('</script>')[0];
const ctx={
 console,Date,URL,crypto:require('node:crypto').webcrypto,structuredClone,
 setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){},
 localStorage:{getItem(){return null},setItem(){}},window:{scrollTo(){}},
 document:{body:{classList:{toggle(){}}},getElementById(){return {innerHTML:'',classList:{toggle(){}},addEventListener(){}}}}
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('dist/training-methods.js','utf8'),ctx);
vm.runInContext(script,ctx);
const run=expr=>vm.runInContext(expr,ctx);
const check=(expr,expected)=>assert.deepEqual(JSON.parse(JSON.stringify(run(expr))),expected,expr);
run("var w=seed().workouts[0];w.items[0].progression={criterion:'all',min:8,max:12,increment:2,scheme:'double',deloadAfter:3,deloadPercent:10};var d=makeDraft(w);d.records.filter(r=>r.item===0).forEach(r=>{r.done=true;r.load=50;r.reps='9'});");
check('doubleProgressionStatus(w.items[0],d.records.filter(r=>r.item===0))','middle');
check('advancedProgressionSuggestions(w,d.records,[]).length',1);
check('advancedProgressionSuggestions(w,d.records,[])[0].includes("mantenha a carga")',true);
check('progressionSuggestions(w,d.records).length',0);
run("d.records.filter(r=>r.item===0).forEach(r=>r.reps='12')");
check('doubleProgressionStatus(w.items[0],d.records.filter(r=>r.item===0))','max');
check('progressionSuggestions(w,d.records).length',1);
check('advancedProgressionSuggestions(w,d.records,[]).length',0);
run("d.records.filter(r=>r.item===0).forEach(r=>r.reps='6')");
check('doubleProgressionStatus(w.items[0],d.records.filter(r=>r.item===0))','below');
check('advancedProgressionSuggestions(w,d.records,[])[0].includes("1/3")',true);
run("var prior={student:w.student,workout:w.id,date:'2026-10-26T11:00:00Z',records:structuredClone(d.records)};var second={...prior,date:'2026-10-22T11:00:00Z'};");
check('advancedProgressionSuggestions(w,d.records,[prior,second])[0].includes("deload de 10%")',true);
run("prior.records.filter(r=>r.item===0).forEach(r=>r.reps='10')");
check('advancedProgressionSuggestions(w,d.records,[prior,second])[0].includes("1/3")',true);
run("d.records.filter(r=>r.item===0).forEach(r=>r.exercise='md999')");
check('advancedProgressionSuggestions(w,d.records,[]).length',0);
run("d.records.filter(r=>r.item===0).forEach(r=>{r.exercise=w.items[0].exercise;r.reps='8-12'})");
check('advancedProgressionSuggestions(w,d.records,[]).length',0);
check('(()=>{let x=seed();x.workouts[0].items[0].progression={criterion:"all",min:8,max:12,increment:1,scheme:"bad"};return validDB(x)})()',false);
check('(()=>{let x=seed();x.workouts[0].items[0].progression={criterion:"all",min:8,max:12,increment:1,scheme:"double",deloadAfter:1};return validDB(x)})()',false);
check('(()=>{let x=seed();x.workouts[0].items[0].progression={criterion:"all",min:8,max:12,increment:1,scheme:"double",deloadPercent:50};return validDB(x)})()',false);
check('(()=>{let x=seed();x.workouts[0].items[0].progression={criterion:"all",min:8,max:12,increment:1,scheme:"double",deloadPercent:10,deloadAfter:3};return validDB(x)})()',true);
assert(html.includes('advancedProgressionSuggestions(w,d.records,db.sessions)'));
assert(fs.readFileSync('dist/training-methods.js','utf8').includes('Dupla progressão · repetições'));
console.log('PASS: dupla progressão, critérios de carga, falhas consecutivas, deload e backups anteriores.');
