#!/usr/bin/env node
'use strict';
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const source=fs.readFileSync('dist/insights.js','utf8');
const html=fs.readFileSync('dist/index.html','utf8');
const ctx={module:{exports:{}},globalThis:null};
ctx.globalThis=ctx;
vm.createContext(ctx);
vm.runInContext(source,ctx,{filename:'dist/insights.js'});
const m=ctx.module.exports;
const date1='2026-10-20T12:00:00.000Z';
const date2='2026-10-22T12:00:00.000Z';
const session=(id,student,date,records)=>({id,student,date,title:'Treino A',records});
const rec=(exercise,name,load,reps,done=true)=>({exercise,name,load,reps,done,set:1,type:'trabalho'});
const data={sessions:[
  session('a1','a',date1,[rec('md5','Supino',50,'10'),rec('md6','Puxada',40,'8-12')]),
  session('b1','b',date1,[rec('md5','Supino',30,'10')]),
  session('a2','a',date2,[rec('md5','Supino',55,'10'),rec('md6','Puxada',45,'8',false)]),
  session('bad','a','data inválida',[rec('md7','Inválido',100,'10')])
]};
assert.equal(m.actualReps(' 10 '),10);
assert.equal(m.actualReps('8–12'),null);
assert.equal(m.actualReps('8-12'),null);
assert.equal(m.actualReps('12 kg'),null);
assert.equal(m.estimated1RM(50,'10'),66.7);
assert.equal(m.estimated1RM(50,'13'),null);
assert.equal(m.estimated1RM(0,'10'),null);
assert.equal(m.estimated1RM(50,'8-12'),null);
const a=m.aggregate(data,'a',Date.parse('2026-10-29T14:00:00Z'));
assert.equal(a.sessions,2);
assert.equal(a.loggedSets,3);
assert.equal(a.totalVolume,1050);
assert.equal(a.personalRecords,2);
assert.equal(a.exercises.length,2);
assert.equal(a.exercises.find(e=>e.id==='md5').best1RM,73.3);
assert.equal(a.weeks.length,8);
assert(a.weeks.some(w=>w.volume===1050));
const all=m.aggregate(data,'all',Date.parse('2026-10-29T14:00:00Z'));
assert.equal(all.sessions,3);
assert.equal(all.totalVolume,1350);
assert.equal(m.aggregate({sessions:[]},'all').totalVolume,0);
assert.equal(m.aggregate({},'all').sessions,0);
const injection=m.exportCSV({rows:[{date:date1,student:'a',title:'=1+1',name:'@SUM(1)',set:1,load:10,reps:10,volume:100,estimated1RM:13.3}]});
assert(injection.startsWith('\uFEFF'));
assert(injection.includes("'=1+1"));
assert(injection.includes("'@SUM(1)"));
assert(!html.includes('src="https://gymvisual.com'));
assert(html.includes('<script src="insights.js"></script>'));
assert(html.includes("['insights','Evolução']"));
assert(html.includes('function exportInsights()'));
const inline=html.split('<script>')[1].split('</script>')[0];
assert.doesNotThrow(()=>new Function(inline));
console.log('PASS: motor de evolução, filtros, 1RM, volume, CSV seguro e integração de interface.');
