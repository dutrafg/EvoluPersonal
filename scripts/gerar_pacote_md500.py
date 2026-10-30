#!/usr/bin/env python3
"""Gera um ZIP com os 500 exercícios oficiais e GIFs reais presentes no dist/."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import zipfile

def read_json_const(source,name):
    marker='const '+name+'='
    pos=source.find(marker)
    if pos<0: raise RuntimeError('Constante ausente: '+name)
    return json.JSONDecoder().raw_decode(source[pos+len(marker):].lstrip())[0]

def group(n):
    return 'Peito' if n<=60 else 'Costas' if n<=140 else 'Pernas' if n<=290 else 'Ombros' if n<=350 else 'Braços' if n<=440 else 'Pernas' if n<=460 else 'Core'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',default='.')
    parser.add_argument('--output',default='dist/downloads/md500-completo.zip')
    a=parser.parse_args()
    root=Path(a.root).resolve()
    dist=root/'dist'
    html=(dist/'index.html').read_text(encoding='utf-8')
    rows=read_json_const(html,'md500Rows')
    extras=read_json_const(html,'md3dMedia')
    if len(rows)!=500: raise RuntimeError('Catálogo original não contém exatamente 500 itens')
    exercises=[]
    files={}
    links=0
    for number,(name,legacy) in enumerate(rows,1):
        media=extras.get(str(number))
        candidates=[media['animation']] if media else []
        if legacy:candidates.append('assets/exercises/'+legacy+'.gif')
        asset=next((p for p in candidates if (dist/p).is_file()),None)
        if asset: files[asset]=dist/asset;links+=1
        status=('em_revisao' if media else 'vinculado_nao_validado') if asset else 'pendente'
        exercises.append({'id':'md'+str(number),'md_id':number,'name':name,'group':group(number),
          'muscles':media.get('muscles','') if media else '',
          'animation':asset or '', 'media_review_status':status})
    manifest={'schema':'evolupersonal-md500-pack','version':1,
       'catalog':'500 Exercícios Base de Musculação.md','exercise_count':500,
       'gif_links':links,'gif_files':len(files),'gif_pending':500-links,'exercises':exercises}
    target=Path(a.output)
    if not target.is_absolute():target=root/target
    target.parent.mkdir(parents=True,exist_ok=True)
    temp=target.with_name(target.name+'.partial')
    with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        z.writestr('manifest.json',json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
        for path,local in sorted(files.items()):z.write(local,arcname=path)
    os.replace(temp,target)
    with zipfile.ZipFile(target) as z:
        assert len(z.namelist())==len(files)+1
        assert z.testzip() is None
    print(json.dumps({'package':str(target),'exercises':500,'gif_links':links,
        'unique_gifs':len(files),'pending':500-links,'bytes':target.stat().st_size},ensure_ascii=False))

if __name__=='__main__':main()
