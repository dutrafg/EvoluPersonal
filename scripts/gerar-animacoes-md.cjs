// Gerador independente de GIFs didáticos MD500 em paleta indexada.
// Cada movimento possui poses originais, sem reutilização de GIFs de terceiros.
// "node scripts/gerar-animacoes-md.cjs" extrai 30 GIFs em dist/assets/md500,
// e mantém cada GIF individual com nome do exercício da lista MD.
'use strict';
const PALETTE=[
 [248,250,253],[228,236,245],[201,216,229],[22,39,62],
 [43,67,94],[73,101,125],[237,183,143],[242,111,43],
 [252,156,68],[100,121,140],[37,48,61],[226,232,240],
 [255,255,255],[171,189,202],[180,94,49],[113,164,195]
];
const FIRST_30=[
 [292,'press','dumbbells','shoulder','seated'],
 [357,'curl','dumbbells','biceps','seated'],
 [76,'pulldown','cable','back','kneel'],
 [85,'row','cable','back','seated'],
 [88,'row','cable','back','seated'],
 [101,'row','cable','back','seated'],
 [109,'pulldown','cable','back','stand'],
 [131,'raise','dumbbells','back','hinge'],
 [132,'raise','dumbbells','back','hinge'],
 [152,'squat','safety-bar','quads','stand'],
 [153,'squat','pendulum','quads','stand'],
 [155,'squat','machine','quads','stand'],
 [170,'legpress','vertical-leg-press','quads','lying'],
 [171,'legpress','articulated-leg-press','quads','lying'],
 [172,'legpress','leg-press','quads','lying'],
 [178,'lunge','smith','quads','stand'],
 [207,'hinge','dumbbells','hamstrings','stand'],
 [208,'hinge','smith','hamstrings','stand'],
 [226,'legcurl','machine','hamstrings','lying'],
 [229,'nordic','ankle-pad','hamstrings','kneel'],
 [249,'bridge','smith','glutes','lying'],
 [298,'press','smith','shoulder','stand'],
 [303,'press','machine','shoulder','seated'],
 [373,'curl','barbell','biceps','stand'],
 [473,'legraise','mat','core','lying'],
 [38,'landmine','landmine','shoulder','stand'],
 [99,'row','cable','back','hinge'],
 [111,'pullover','cable','back','lying'],
 [115,'hinge','barbell','hamstrings','stand'],
 [120,'shrug','dumbbells','back','seated']
];
const W=144,H=144,FRAME_COUNT=10;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function canvas(){
  const p=new Uint8Array(W*H);p.fill(0);
  function dot(x,y,r,color){x=Math.round(x);y=Math.round(y);r=Math.max(1,Math.round(r));for(let yy=Math.max(0,y-r);yy<=Math.min(H-1,y+r);yy++)for(let xx=Math.max(0,x-r);xx<=Math.min(W-1,x+r);xx++)if((xx-x)**2+(yy-y)**2<=r*r)p[yy*W+xx]=color;}
  function line(a,b,c,d,w,color){const steps=Math.max(1,Math.ceil(Math.hypot(c-a,d-b)*1.4));for(let i=0;i<=steps;i++){const t=i/steps;dot(a+(c-a)*t,b+(d-b)*t,w,color);}}
  function rect(x,y,w,h,color){for(let yy=Math.max(0,Math.floor(y));yy<Math.min(H,Math.ceil(y+h));yy++)for(let xx=Math.max(0,Math.floor(x));xx<Math.min(W,Math.ceil(x+w));xx++)p[yy*W+xx]=color;}
  function oval(x,y,rx,ry,color){for(let yy=Math.max(0,Math.floor(y-ry));yy<Math.min(H,Math.ceil(y+ry));yy++)for(let xx=Math.max(0,Math.floor(x-rx));xx<Math.min(W,Math.ceil(x+rx));xx++)if(((xx-x)/rx)**2+((yy-y)/ry)**2<=1)p[yy*W+xx]=color;}
  return {p,dot,line,rect,oval};
}
function equipment(g,s,t){
 const k=s[2];
 if(k==='cable'){g.rect(11,17,5,112,9);g.dot(14,19,5,10);g.dot(14,119,5,10);g.line(15,20,15,120,1,13);}
 if(k==='smith'){g.line(29,18,29,121,1,9);g.line(116,18,116,121,1,9);g.line(27,20,118,20,1,13);g.line(27,121,118,121,1,13);}
 if(k.includes('leg-press')){
  if(k==='vertical-leg-press'){g.line(104,23,130,23,4,9);g.line(113,23,132,45,2,13);}
  else if(k==='articulated-leg-press'){g.line(126,30,119,116,4,9);g.dot(124,41,9,10);g.line(117,39,137,39,3,3);}
  else{g.line(126,34,126,124,3,9);g.line(117,39,137,39,3,3);g.line(117,120,137,120,3,3);}
 }
 if(k==='machine'||k==='pendulum'){g.line(31,20,31,123,3,9);g.line(31,26,115,26,2,13);g.line(114,26,114,120,2,9);
  if(k==='pendulum'){g.line(114,26,95,87,4,9);g.dot(114,26,7,10);g.line(95,87,108,95,4,9);}
  else{g.rect(31,86,18,12,13);g.line(40,98,40,122,2,9);}
 }
 if(k==='safety-bar'||k==='barbell'){g.line(46,39,104,39,2,10);g.dot(45,39,6,9);g.dot(105,39,6,9);}
 if(k==='landmine'){g.line(22,122,118,47-24*t,3,9);g.dot(22,122,5,10);g.dot(119,47-24*t,5,10);}
 if(k==='ankle-pad'){g.rect(54,121,38,5,9);}
 if(k==='mat'){g.rect(23,120,99,4,15);}
}
function head(g,x,y){g.dot(x,y,10,10);g.dot(x,y-1,8,6);g.oval(x+2,y-3,3,4,12);g.dot(x+3,y+2,1,3);}
function limb(g,a,b,c,d,hi,act){g.line(a,b,c,d,5,10);g.line(a,b,c,d,4,hi);if(act)g.line(a,b,c,d,2,7);g.dot(c,d,4,6);}
function body(g,shx,shy,hipx,hipy,focus){
 g.line(shx,shy,hipx,hipy,12,10);
 g.line(shx-2,shy,hipx-2,hipy,10,3);
 g.line(shx+3,shy,hipx+3,hipy,4,4);
 if(focus==='core'||focus==='back')g.line(shx+5,shy+8,hipx+4,hipy-8,3,7);
 g.dot(hipx,hipy,10,3);
 if(focus==='glutes')g.oval(hipx,hipy-1,9,6,7);
}
function figure(g,s,t){
 const [n,motion,tool,focus,stance]=s;
 const up=1-t, seat=stance==='seated', kneel=stance==='kneel', lie=stance==='lying';
 g.line(10,127,136,127,1,1);
 g.oval(73,130,47,5,1);
 if(lie||motion==='legpress'||motion==='legcurl'||motion==='bridge'||motion==='pullover'||motion==='legraise'){
  if(motion==='legpress'){
   g.line(35,111,67,78,5,9);g.line(35,111,54,120,5,9);
   head(g,47,88);body(g,59,91,83,106,focus);
   const kneex=101-9*t,kneey=93+11*t,footx=tool==='vertical-leg-press'?103:tool==='articulated-leg-press'?125-12*t:124-16*t,footy=tool==='vertical-leg-press'?29+22*t:tool==='articulated-leg-press'?57+16*t:66+13*t;
   limb(g,82,105,kneex,kneey,4,1);limb(g,kneex,kneey,footx,footy,4,1);
   g.line(footx-5,footy-5,footx+6,footy+4,4,9);
   limb(g,76,102,100-8*t,104+13*t,4,0);
  }else if(motion==='legcurl'){
   g.rect(32,89,77,5,9);head(g,43,78);body(g,57,77,84,80,focus);
   limb(g,85,79,109,90,4,1);limb(g,109,90,112-14*t,109-19*t,4,1);
   g.dot(113-14*t,109-19*t,6,9);g.line(126,85,126,120,2,9);
  }else if(motion==='bridge'){
   g.rect(25,113,91,6,9);head(g,34,104);body(g,47,103,86,108-25*t,focus);
   limb(g,86,108-25*t,102,99,4,1);limb(g,102,99,114,116,4,0);
   g.line(75,79-25*t,96,79-25*t,2,10);
  }else if(motion==='pullover'){
   g.rect(26,104,102,5,9);head(g,35,94);body(g,49,94,92,94,focus);
   limb(g,55,88,75-30*t,65-18*t,4,1);
   g.line(69-30*t,65-18*t,86-30*t,65-18*t,2,9);
   limb(g,93,92,113,104,4,0);
  }else{
   g.rect(24,112,104,4,9);head(g,35,104);body(g,51,103+7*t,83,102,focus);
   limb(g,83,102,101,91-24*t,4,1);limb(g,101,91-24*t,115,86-25*t,4,1);
   limb(g,79,101,104,100-17*t,4,1);
  }
  return;
 }
 if(motion==='nordic'){
   const shift=30*t;
   g.line(66,121,79,121,6,4);g.dot(72,116,7,7);
   body(g,73+shift,58+23*t,75,106,focus);head(g,74+shift+2,44+23*t);
   limb(g,74,107,70,121,4,1);limb(g,75,108,89,120,4,1);
   limb(g,74+shift,67+22*t,85+shift,81+20*t,4,0);return;
 }
 const yshift=motion==='squat'?17*t:motion==='calf'?-8*t:0;
 const shx=(motion==='hinge'||motion==='row')?76+26*t:76;
 const shy=(motion==='hinge'||motion==='row')?51+16*t+yshift:51+yshift;
 const hx=75,hy=85+yshift;
 head(g,shx+1,shy-20);body(g,shx,shy,hx,hy,focus);
 const ykneel=seat?112:106;
 if(seat){
  g.rect(59,87,50,5,9);g.line(105,89,105,125,3,9);
  limb(g,75,87,100,102,4,focus==='quads');limb(g,100,102,101,123,4,focus==='quads');
  limb(g,73,87,52,103,4,focus==='quads');limb(g,52,103,49,123,4,focus==='quads');
 }else if(kneel){
  limb(g,74,86,65,112,4,focus==='quads');limb(g,65,112,44,122,4,0);
  limb(g,78,86,91,110,4,focus==='quads');limb(g,91,110,112,121,4,0);
 }else if(motion==='lunge'){
  limb(g,75,86,58,102+13*t,4,focus==='quads');limb(g,58,102+13*t,44,124,4,0);
  limb(g,78,85,93,101+11*t,4,focus==='quads');limb(g,93,101+11*t,117,124,4,0);
 }else{
  const kneeL=motion==='squat'?57:64,kneeR=motion==='squat'?95:87;
  const ky=motion==='squat'?104+5*t:103;
  limb(g,74,86,kneeL,ky,4,focus==='quads'||focus==='hamstrings');
  limb(g,78,85,kneeR,ky,4,focus==='quads'||focus==='hamstrings');
  limb(g,kneeL,ky,51,123,4,focus==='quads');limb(g,kneeR,ky,99,123,4,focus==='quads');
 }
 const ly=shy+5;
 if(motion==='press'||motion==='landmine'){
  limb(g,shx-9,ly,shx-24,70+yshift-10*t,4,focus==='shoulder');
  limb(g,shx+9,ly,shx+22,69+yshift-10*t,4,focus==='shoulder');
  const topy=72+yshift-40*t;
  limb(g,shx-24,70+yshift-10*t,shx-22,topy,4,1);
  limb(g,shx+22,69+yshift-10*t,shx+22,topy,4,1);
  if(tool==='dumbbells'){g.line(shx-33,topy,shx-11,topy,3,10);g.line(shx+11,topy,shx+33,topy,3,10);}
  if(tool==='smith')g.line(shx-30,topy,shx+30,topy,3,10);
 }else if(motion==='pulldown'){
  const y=40+38*t;
  limb(g,shx-10,ly,shx-24,54+18*t,4,1);
  limb(g,shx-24,54+18*t,shx-24,y,4,1);
  limb(g,shx+10,ly,shx+20,53+18*t,4,1);
  limb(g,shx+20,53+18*t,shx+19,y,4,1);
  g.line(shx-34,y,shx+29,y,2,9);
  g.line(15,20,shx,y,1,13);
 }else if(motion==='row'){
  const high=(n===101),one=(n===88||n===99);
  const handx=shx-42+24*t,handy=ly+(high?8:24);
  limb(g,shx-10,ly,shx-19,ly+(high?4:18),4,1);
  limb(g,shx-19,ly+(high?4:18),handx,handy,4,1);
  if(!one){
    limb(g,shx+10,ly,shx+18,ly+(high?3:17),4,1);
    limb(g,shx+18,ly+(high?3:17),shx+39-22*t,handy,4,1);
  }else{
    limb(g,shx+10,ly,shx+18,ly+30,4,0);
  }
  g.line(15,high?35:110,handx,handy,1,13);
 }else if(motion==='raise'){
  const reach=21+24*t;
  if(n===132){
    limb(g,shx-10,ly,shx-reach,shy-5-21*t,4,1);
    limb(g,shx+10,ly,shx+reach,shy-5-21*t,4,1);
    limb(g,shx-reach,shy-5-21*t,shx-reach+7,shy-20-19*t,4,1);
    limb(g,shx+reach,shy-5-21*t,shx+reach-7,shy-20-19*t,4,1);
  }else{
    limb(g,shx-10,ly,shx-reach,shy-5-30*t,4,1);
    limb(g,shx+10,ly,shx+reach,shy-5-30*t,4,1);
    g.dot(shx-reach,shy-5-30*t,5,9);g.dot(shx+reach,shy-5-30*t,5,9);
  }
 }else if(motion==='curl'){
  limb(g,shx-10,ly,shx-19,shy+23,4,1);
  limb(g,shx+10,ly,shx+19,shy+23,4,1);
  limb(g,shx-19,shy+23,shx-22+5*t,shy+48-29*t,4,1);
  limb(g,shx+19,shy+23,shx+22-5*t,shy+48-29*t,4,1);
  g.dot(shx-22+5*t,shy+48-29*t,5,9);g.dot(shx+22-5*t,shy+48-29*t,5,9);
 }else if(motion==='shrug'){
  limb(g,shx-12,ly-10*t,shx-22,shy+37-10*t,4,1);
  limb(g,shx+12,ly-10*t,shx+22,shy+37-10*t,4,1);
  g.dot(shx-23,shy+40-10*t,5,9);g.dot(shx+23,shy+40-10*t,5,9);
 }else{
  limb(g,shx-10,ly,shx-18,shy+38,4,focus==='shoulder');
  limb(g,shx+10,ly,shx+18,shy+38,4,focus==='shoulder');
  if(tool==='dumbbells'){g.dot(shx-18,shy+42,5,9);g.dot(shx+18,shy+42,5,9);}
 }
 if(focus==='hamstrings'){g.line(70,89,63,101,2,7);g.line(84,88,88,101,2,7);}
 if(focus==='quads'){g.line(73,89,65,100,2,7);g.line(82,89,90,100,2,7);}
}
function gifLZW(pixel){
 const codes=[];const min=4,clr=1<<min,end=clr+1;let dict,next,size;
 function reset(){dict=new Map();next=end+1;size=min+1;}
 reset();const out=[];let bits=0,nBits=0;
 function push(v){bits|=v<<nBits;nBits+=size;while(nBits>=8){out.push(bits&255);bits>>>=8;nBits-=8;}}
 push(clr);let phrase=String(pixel[0]);
 for(let i=1;i<pixel.length;i++){
  const k=pixel[i],joined=phrase+','+k;
  if(dict.has(joined)){phrase=joined;continue;}
  const code=phrase.includes(',')?dict.get(phrase):+phrase;
  push(code);
  if(next<4096){dict.set(joined,next++);if(next>(1<<size)&&size<12)size++;}
  else{push(clr);reset();}
  phrase=String(k);
 }
 push(phrase.includes(',')?dict.get(phrase):+phrase);push(end);
 if(nBits)out.push(bits&255);
 return out;
}
function render(s){
 const data=[];const byte=(x)=>data.push(x&255), word=(x)=>{byte(x);byte(x>>8)};
 const ascii=(v)=>{for(let i=0;i<v.length;i++)byte(v.charCodeAt(i))};
 ascii('GIF89a');word(W);word(H);byte(0xf3);byte(0);byte(0);
 for(const p of PALETTE)for(const v of p)byte(v);
 byte(0x21);byte(0xff);byte(11);ascii('NETSCAPE2.0');byte(3);byte(1);word(0);byte(0);
 for(let f=0;f<FRAME_COUNT;f++){
  const t=(1-Math.cos((f/FRAME_COUNT)*Math.PI*2))/2;
  const g=canvas();equipment(g,s,t);figure(g,s,t);
  byte(0x21);byte(0xf9);byte(4);byte(0x04);word(9);byte(0);byte(0);
  byte(0x2c);word(0);word(0);word(W);word(H);byte(0);
  byte(4);
  const packed=gifLZW(g.p);
  for(let i=0;i<packed.length;i+=255){const sub=packed.slice(i,i+255);byte(sub.length);for(const x of sub)byte(x);}
  byte(0);
 }
 byte(0x3b);
 return Uint8Array.from(data);
}
function toBase64(bytes){
 const alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
 let out='';
 for(let i=0;i<bytes.length;i+=3){
  const a=bytes[i],b=i+1<bytes.length?bytes[i+1]:0,c=i+2<bytes.length?bytes[i+2]:0;
  const v=(a<<16)|(b<<8)|c;
  out+=alphabet[(v>>>18)&63]+alphabet[(v>>>12)&63]+(i+1<bytes.length?alphabet[(v>>>6)&63]:'=')+(i+2<bytes.length?alphabet[v&63]:'=');
 }
 return out;
}
if(typeof module!=='undefined')module.exports={FIRST_30,render,toBase64,FRAME_COUNT,W,H};
if(typeof require==='function'&&typeof module!=='undefined'&&require.main===module){
 const fs=require('node:fs'),path=require('node:path');
 const dir=path.join(__dirname,'../dist/assets/md500');fs.mkdirSync(dir,{recursive:true});
 for(const item of FIRST_30){const gif=render(item);const id=String(item[0]);fs.writeFileSync(path.join(dir,'md'+id+'.gif'),gif);}
 console.log('GIFs gerados: '+FIRST_30.length+' em '+dir);
}
