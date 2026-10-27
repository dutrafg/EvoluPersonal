const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('dist/index.html','utf8');
const js=html.split('<script>')[1].split('</script>')[0];
const stored=new Map(),nodes=new Map();
const ctx={console,crypto:require('crypto').webcrypto,structuredClone,URL,Date,setTimeout:()=>1,clearTimeout:()=>{},setInterval:()=>1,clearInterval:()=>{},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},document:{body:{classList:{toggle(){}}},getElementById:id=>{if(!nodes.has(id))nodes.set(id,{classList:{toggle(){}},addEventListener(){}});return nodes.get(id)}}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('dist/training-methods.js','utf8'),ctx);vm.runInContext(js,ctx);
let n=0;function check(expr,expected=true){assert.equal(vm.runInContext(expr,ctx),expected,expr);n++}
check('validDB(seed())');
check('seed().students.length',4);
check('makeDraft(seed().workouts[0]).records.length',9);
check('makeDraft(seed().workouts[0]).records.every(r=>!r.done&&r.load===0)');
check('safeURL("javascript:alert(1)")',null);
check('safeURL("data:text/html,evil")',null);
check('safeURL("https://example.com/demo")','https://example.com/demo');
check('esc("<img onerror=x>")','&lt;img onerror=x&gt;');
const invalid=[
 'x.version=99','x.students[0].id="a\'b"','x.students[0].id="__proto__"',
 'x.students.push(x.students[0])','x.students[0].name=" "',
 'x.workouts[0].student="missing"','x.workouts[0].items[0].exercise="missing"',
 'x.workouts[0].items[0].sets=0','x.workouts[0].items[0].sets=1.5',
 'x.workouts[0].items[0].load=-1','x.workouts[0].items[0].rest=Infinity',
 'x.exercises[0].url="javascript:alert(1)"','x.drafts={missing:{records:[]}}'
];
for(const mutation of invalid)check('(()=>{let x=seed();'+mutation+';return validDB(x)})()',false);
check('(()=>{let x=seed(),w=x.workouts[0];x.drafts[w.id]=makeDraft(w);return validDB(x)})()');
check('(()=>{let x=seed(),w=x.workouts[0];x.drafts[w.id]=makeDraft(w);x.drafts[w.id].records.pop();return validDB(x)})()',false);
check('(()=>{let x=seed(),w=x.workouts[0],records=makeDraft(w).records;records.forEach(r=>r.done=true);x.sessions.push({id:"test",student:w.student,title:w.title,date:new Date().toISOString(),effort:"Moderado",feedback:"",records});return validDB(x)})()');
check('validDB(JSON.parse(JSON.stringify(db)))');
check('JSON.parse(localStorage.getItem(KEY)).students.length',4);
check('(()=>{bind();document.getElementById("libSearch").oninput({currentTarget:{value:"Supino"}});return document.getElementById("libGrid").innerHTML.includes("Supino reto")&&!document.getElementById("libGrid").innerHTML.includes("Agachamento livre")})()');
check('(()=>{document.getElementById("groupFilter").onchange({currentTarget:{value:"Pernas"}});return document.getElementById("libGrid").innerHTML.includes("Nenhum exercício encontrado")})()');
check('(()=>{document.getElementById("studentSearch").oninput({currentTarget:{value:"Carlos"}});return document.getElementById("studentGrid").innerHTML.includes("Carlos Mendes")&&!document.getElementById("studentGrid").innerHTML.includes("Ana Oliveira")})()');
check('(()=>{toggleTheme();return JSON.parse(localStorage.getItem(KEY)).theme==="dark"})()');
console.log(n+' verificações passaram: backup, vínculos, limites de prescrição, sessão, segurança de links e persistência.');
