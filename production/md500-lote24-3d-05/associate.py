from pathlib import Path
import json,re,collections
R=Path(__file__).resolve().parent;P=R.parents[1]
def read(p):return json.loads((P/p).read_text())
def save(p,x):(P/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
src=json.loads((R/'fontes.json').read_text());tech=json.loads((R/'technical-validation.json').read_text());ids={x['id'] for x in src}
assert len(ids)==24
oldshas=set(json.loads((R/'existing-gif-shas.json').read_text()))
assert not oldshas.intersection(x['gif_blob_sha'] for x in tech)
inventory=read('production/INVENTARIO_MD500.json');queue=read('production/FILA_MD500_ATUAL.json')
assert ids.issubset(x['id'] for x in queue)
assert all(not inventory[i-1]['animation_path'] for i in ids)
muscles={x['id']:x['muscles'] for x in src}
items=[]
for x,t in zip(src,tech):
 i=x['id'];assert t['md_id']==i;r=inventory[i-1]
 r.update(ref=f'md{i}',new_gif=t['output_path'],animation_path=t['output_path'].removeprefix('dist/'),gif_blob_sha=t['gif_blob_sha'],batch_id='MD500-24-05',production_state='vinculado_3d_revisao_pendente',media_review_pending=True,association_status='associado',review_status='pendente',existing_candidate=None)
 items.append(dict(md_id=i,name=r['name'],highlighted_muscles=muscles[i],movement=x['detail'],output_path=t['output_path'],status='associado_revisao_final_pendente',visual_qa_approved=False,render_validated=True,associated_with_exercise=True))
manifest=dict(schema_version=1,batch='MD500-24-05',date='2026-10-28',repo='dutrafg/EvoluPersonal',branch='codex/evolupersonal-media-350',source='docs/500-exercicios-base.md',target=24,completed_gifs=24,status='ASSOCIADO_REVISAO_FINAL_PENDENTE',counted_in_app_coverage=True,associated_with_exercises=True,coverage_kind='vinculo_cadastral_nao_aprovacao_biomecanica',approved_gifs=0,items=items)
save('production/lote-md500-24-05.json',manifest);save('production/md500-lote24-3d-05/lote.json',manifest)
save('production/INVENTARIO_MD500.json',inventory);save('production/FILA_MD500_ATUAL.json',[x for x in queue if x['id'] not in ids])
f=P/'dist/index.html';html=f.read_text();m=re.search(r'const md3dMedia=(\{.*?\});\n',html,re.S);media=json.loads(m[1])
for i in ids:media[str(i)]=dict(animation=f'assets/md500-3d/md{i}.gif',batch='MD500-24-05',muscles=muscles[i])
html=html[:m.start(1)]+json.dumps(media,ensure_ascii=False,separators=(',',':'))+html[m.end(1):]
html=re.sub(r'mdCurrentBatchIds=new Set\(\[.*?\]\)', 'mdCurrentBatchIds=new Set('+json.dumps([x['id'] for x in src])+')',html)
f.write_text(html)
doc=read('docs/COMPARACAO_LISTA_500.json')
for x in doc['items']:
 i=x['list_id']
 if i in ids:
  r=inventory[i-1];x.update(catalog_ids=[f'md{i}'],catalog_names=[r['name']],planned_id=None,status='GIF 3D vinculado; revisão pendente',production_status=r['production_state'],media_ref=r['ref'],animation_path=r['animation_path'],review_pending=True)
counts=dict(collections.Counter(x['status'] for x in doc['items']));counts.update(exercicios_com_midia=420,novos_gifs_3d_associados=124,revisao_pendente=125,sem_gif=80,referencias_distintas_em_uso=len({x['animation_path'] for x in inventory if x['animation_path']}),bases_principais_total=sum(x['primary'] for x in doc['items']),bases_com_correspondencia=sum(x['primary'] and bool(x['animation_path']) for x in doc['items']),observacao='Vínculo cadastral não significa aprovação visual ou biomecânica. GIFs 2D reprovados continuam desativados.')
doc['summary']=counts;save('docs/COMPARACAO_LISTA_500.json',doc)
md='# EvoluPersonal — catálogo exclusivo da lista MD (500 exercícios)\n\nFonte única: **500 Exercícios Base de Musculação.md**. Nomes e ordem preservados.\n\n**500 exercícios · 420 com GIF vinculado · 80 sem GIF.** Os 124 GIFs novos e a equivalência MD357/e141 estão associados para revisão: vínculo cadastral não significa aprovação visual ou biomecânica.\n\nOs identificadores `eN` apontam para `dist/assets/exercises/`; os `mdN` para `dist/assets/md500-3d/`. O lote 2D reprovado continua fora do catálogo.\n\n| Nº MD | Nome original no MD | GIF |\n|---:|---|---|\n'
md+='\n'.join(f"| {x['id']} | {x['name']} | `"+x['ref']+'` |' for x in inventory)+'\n';(P/'docs/COMPARACAO_LISTA_500.md').write_text(md)

for name in ['tests.cjs','tests-gallery.cjs','tests-media.cjs']:
 f=P/name;s=f.read_text().replace("length',396","length',420").replace('length,396','length,420').replace(',ctx),396)',',ctx),420)').replace('396 vínculos','420 vínculos').replace('104 pendentes','80 pendentes').replace('length,101','length,125').replace(',ctx),101)',',ctx),125)').replace('101</strong>','125</strong>').replace('101 em revisão','125 em revisão')
 if name=='tests-media.cjs':
  s=s.replace("const items=[1,2,3,4].flatMap(n=>JSON.parse(fs.readFileSync('production/lote-md500-25-0'+n+'.json','utf8')).items);", "const items=[1,2,3,4].flatMap(n=>JSON.parse(fs.readFileSync('production/lote-md500-25-0'+n+'.json','utf8')).items).concat(JSON.parse(fs.readFileSync('production/lote-md500-24-05.json','utf8')).items);")
  s=s.replace('items.length,100','items.length,124').replace('e.md_id)).size,100','e.md_id)).size,124').replace('PASS: 100 associações','PASS: 124 associações')
 if name=='tests-gallery.cjs':s=s.replace('lote-md500-25-04.json','lote-md500-24-05.json').replace('count(outcome.active),25','count(outcome.active),24').replace('||[]).length,25','||[]).length,24').replace('count(outcome.reviewThird),1','count(outcome.reviewThird),25').replace('lote atual 25','lote atual 24')
 f.write_text(s)
(P/'CHECKPOINT.md').write_text('# EvoluPersonal — checkpoint\n\nBranch `codex/evolupersonal-media-350`; main somente com autorização.\n\n500 exercícios:420 vinculados,80 sem GIF,125 em revisão.124 GIFs3D novos:quatro lotes de25 e um lote de24 solicitado pelo usuário. Todos associados para revisão, sem aprovação automática.\n\nContinuar pela production/FILA_MD500_ATUAL.json; conferir duplicações e associar cada GIF ao exercício oficial. Fonte docs/500-exercicios-base.md. Sem deploy de produção.\n')
(P/'production/ASSOCIACOES_MD500.md').write_text('# Associações MD500\n\n124 GIFs novos associados;420 exercícios vinculados,80 sem GIF,125 em revisão. MD357 reutiliza e141; MD16 usa e402. Main preservada. Lote atual24 conforme solicitação.\n')
(R/'README.md').write_text('# Lote MD500-24-05\n\n24 GIFs produzidos individualmente e associados. Ferramenta de geração de imagens:fontes3x2 montadas em GIF144x144 em loop. Prompts em fontes.json. Revisão final visual e biomecânica pendente. Conferir enquadramento, continuidade e apoios em todos.\n\nTentativas390,397,436 excluídas por inconsistências de pegada/equipamento/resistência; continuam na fila. Substituídas neste lote por470,476,498.\n')
print(json.dumps({'associated':len(items),'linked':420,'pending':80,'review':125}))
