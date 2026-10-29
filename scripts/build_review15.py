#!/usr/bin/env python3
"""Gera HTML autônomo com os 15 GIFs de auditoria, sem serviços externos.

A fonte de verdade é dist/revisao-vinculos-md500.html, gerada da lista MD500.
Executar na raiz: python3 scripts/build_review15.py
O resultado é dist/revisao-visual-15-offline.html.
"""
import base64
import json
import pathlib
import re

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'dist/revisao-vinculos-md500.html'
OUT=ROOT/'dist/revisao-visual-15-offline.html'
text=BASE.read_text(encoding='utf-8')
pattern=r'const ITEMS=(\[[\s\S]*?\]);\nconst ASSETS=(\[[\s\S]*?\]);\nconst byId'
m=re.search(pattern,text)
if not m: raise RuntimeError('Dados da galeria não encontrados')
items=json.loads(m.group(1))
assets=json.loads(m.group(2))
chosen=[x for x in items if x.get('source')=='legado' and x.get('priority')]
if len(chosen)!=15: raise RuntimeError(f'Esperados 15 vínculos, encontrados {len(chosen)}')
paths=set(x['path'] for x in chosen)
selected=[x for x in assets if x['path'] in paths]
if len(selected)!=12: raise RuntimeError(f'Esperados 12 GIFs distintos, encontrados {len(selected)}')
media={}
for x in selected:
    path=ROOT/'dist'/x['path']
    raw=path.read_bytes()
    if raw[:6] not in (b'GIF87a',b'GIF89a'):
        raise RuntimeError('Arquivo GIF inválido: '+str(path))
    media[x['path']]='data:image/gif;base64,'+base64.b64encode(raw).decode('ascii')
text=text[:m.start()]+(
    'const ITEMS='+json.dumps(chosen,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    'const ASSETS='+json.dumps(selected,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    'const byId'
)+text[m.end():]
text=text.replace('<title>EvoluPersonal · Auditoria dos 500 GIFs</title>',
                  '<title>EvoluPersonal · Revisão visual de 15 GIFs — offline</title>')
text=text.replace('Auditoria de correspondências · MD500',
                  'Revisão visual · 15 GIFs legados')
text=text.replace('As decisões ficam no navegador e podem ser exportadas para aplicação posterior no código.',
                  'As decisões ficam no navegador; copie e cole o resultado no ChatGPT ou exporte o JSON.')
text=text.replace('Atenção:</b> os GIFs carregam de <code>dist/assets/</code>. Abra esta página dentro da pasta <code>dist</code> com os diretórios de mídia preservados.',
                  'Arquivo autônomo:</b> os 12 GIFs originais estão incorporados, sem depender de pastas, conexão ou login no GitHub.')
text=text.replace('500 registros · versão 2026-10-29',
                  '15 exercícios · 12 GIFs originais embutidos · versão 2026-10-29')
text=text.replace('const ITEMS=', 'const EMBEDDED_MEDIA='+json.dumps(media,separators=(',',':'))+';\n'
                  'const resolveMedia=path=>EMBEDDED_MEDIA[path]||path;\n'
                  'const ITEMS=',1)
text=text.replace('im.src=path;', 'im.src=resolveMedia(path);')
# Apenas o GIF selecionado é executado, evitando 12 animações simultâneas no celular.
text=re.sub(r'const srcHtml=.*?;\nfunction renderCounts',
            'const srcHtml=(path,id)=>path?\\'<span class="noimage">Toque em Conferir GIF para reproduzir</span>\\':\\'<span class="noimage">Sem GIF</span>\\';\nfunction renderCounts',
            text,count=1,flags=re.DOTALL)
text=text.replace('<button id="export" class="primary" type="button">Exportar revisão JSON</button>',
                  '<button id="copy" class="primary" type="button">Copiar resultado para o ChatGPT</button>'
                  '<button id="export" type="button">Exportar revisão JSON</button>')
# Corrige o progresso para apenas os 15 vínculos.
text=text.replace('const KEY="evolupersonal:revisao-vinculos-md500:20261029"',
                  'const KEY="evolupersonal:auditoria-15-offline:20261029"')
inject=r'''
function reviewSummary(){
 const names={aprovado:"APROVADO",reprovado:"REPROVADO",pendente:"PENDENTE"};
 return "EVOLUPERSONAL | REVISAO VISUAL 15 GIFS\n"
 +ITEMS.map(x=>{const r=reviewOf(x),checks=Array.isArray(r.checks)?r.checks.filter(Boolean).length:0;
 return "MD"+x.id+" ("+x.ref+"): "+(names[r.status]||"PENDENTE")
 +", criterios "+checks+"/4"+(r.candidate?" | sugestao: "+r.candidate:"")
 +(r.notes?" | OBS: "+String(r.notes).replace(/\s+/g," ").slice(0,500):"")}).join("\n")
 +"\nFim do resultado. Nao alterar a main automaticamente.";
}
$("copy").onclick=async()=>{
 const value=reviewSummary();
 try{
  if(!navigator.clipboard?.writeText)throw Error("sem API");
  await navigator.clipboard.writeText(value);
  alert("Resultado copiado. Volte à conversa e cole aqui.");return;
 }catch(e){}
 const t=document.createElement("textarea");t.value=value;document.body.appendChild(t);t.select();
 let ok=false;try{ok=document.execCommand("copy")}catch(e){}
 t.remove();alert(ok?"Resultado copiado. Cole no ChatGPT.":"Use Exportar JSON e anexe o arquivo nesta conversa.");
};
'''
text=text.replace('doFilter();\n</script>', inject+'\ndoFilter();\n</script>')
if text.count('const ITEMS=')!=1 or len(media)!=12 or 'resolveMedia(path)' not in text or 'reviewSummary()' not in text:
    raise RuntimeError('Falha ao construir a página')
OUT.write_text(text,encoding='utf-8')
print(json.dumps({'output':str(OUT.relative_to(ROOT)),'size':OUT.stat().st_size,
                  'review_items':len(chosen),'embedded_gifs':len(media)},ensure_ascii=False))
