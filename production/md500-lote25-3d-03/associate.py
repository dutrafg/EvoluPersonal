from pathlib import Path
import json,re,collections
R=Path(__file__).resolve().parent;P=R.parents[1]
def read(p):return json.loads((P/p).read_text())
def save(p,x):(P/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
src=json.loads((R/'fontes.json').read_text());tech=json.loads((R/'technical-validation.json').read_text());ids={x['id'] for x in src}
assert len(ids)==25
oldshas=set(json.loads((R/'existing-gif-shas.json').read_text()))
assert not oldshas.intersection(x['gif_blob_sha'] for x in tech)
inventory=read('production/INVENTARIO_MD500.json');queue=read('production/FILA_MD500_ATUAL.json')
assert ids.issubset(x['id'] for x in queue)
assert all(not inventory[i-1]['animation_path'] for i in ids)
muscles={104:'latíssimo do dorso, romboides, trapézio médio, bíceps',120:'trapézio superior',121:'trapézio médio e superior',160:'quadríceps, glúteos',209:'isquiotibiais, glúteos, eretores da coluna',215:'isquiotibiais, glúteos',221:'glúteos, isquiotibiais, eretores da coluna',224:'glúteos, isquiotibiais, core',231:'isquiotibiais',232:'isquiotibiais',234:'isquiotibiais',239:'isquiotibiais, glúteos',254:'glúteos',263:'glúteos, quadríceps',270:'glúteos, isquiotibiais',282:'glúteo médio',283:'glúteo médio',288:'adutores, glúteos, quadríceps',320:'deltoide lateral',323:'deltoides, trapézio, serrátil',324:'deltoide lateral',331:'deltoide anterior',339:'deltoide posterior, romboides',349:'infraespinal, redondo menor',367:'bíceps, braquial'}
items=[]
for x,t in zip(src,tech):
 i=x['id'];assert t['md_id']==i;r=inventory[i-1]
 r.update(ref=f'md{i}',new_gif=t['output_path'],animation_path=t['output_path'].removeprefix('dist/'),gif_blob_sha=t['gif_blob_sha'],batch_id='MD500-25-03',production_state='vinculado_3d_revisao_pendente',media_review_pending=True,association_status='associado',review_status='pendente',existing_candidate=None)
 items.append(dict(md_id=i,name=r['name'],highlighted_muscles=muscles[i],movement=x['detail'],output_path=t['output_path'],status='associado_revisao_final_pendente',visual_qa_approved=False,render_validated=True,associated_with_exercise=True))
manifest=dict(schema_version=1,batch='MD500-25-03',date='2026-10-28',repo='dutrafg/EvoluPersonal',branch='codex/evolupersonal-media-350',source='docs/500-exercicios-base.md',target=25,completed_gifs=25,status='ASSOCIADO_REVISAO_FINAL_PENDENTE',counted_in_app_coverage=True,associated_with_exercises=True,coverage_kind='vinculo_cadastral_nao_aprovacao_biomecanica',approved_gifs=0,items=items)
save('production/lote-md500-25-03.json',manifest);save('production/md500-lote25-3d-03/lote.json',manifest)
save('production/INVENTARIO_MD500.json',inventory);save('production/FILA_MD500_ATUAL.json',[x for x in queue if x['id'] not in ids])
f=P/'dist/index.html';html=f.read_text();m=re.search(r'const md3dMedia=(\{.*?\});\n',html,re.S);media=json.loads(m[1])
for i in ids:media[str(i)]=dict(animation=f'assets/md500-3d/md{i}.gif',batch='MD500-25-03',muscles=muscles[i])
html=html[:m.start(1)]+json.dumps(media,ensure_ascii=False,separators=(',',':'))+html[m.end(1):]
html=re.sub(r'mdCurrentBatchIds=new Set\(\[.*?\]\)', 'mdCurrentBatchIds=new Set('+json.dumps([x['id'] for x in src])+')',html)
f.write_text(html)
doc=read('docs/COMPARACAO_LISTA_500.json')
for x in doc['items']:
 i=x['list_id']
 if i in ids:
  r=inventory[i-1];x.update(catalog_ids=[f'md{i}'],catalog_names=[r['name']],planned_id=None,status='GIF 3D vinculado; revisão pendente',production_status=r['production_state'],media_ref=r['ref'],animation_path=r['animation_path'],review_pending=True)
counts=dict(collections.Counter(x['status'] for x in doc['items']));counts.update(exercicios_com_midia=371,novos_gifs_3d_associados=75,revisao_pendente=76,sem_gif=129,referencias_distintas_em_uso=len({x['animation_path'] for x in inventory if x['animation_path']}),bases_principais_total=sum(x['primary'] for x in doc['items']),bases_com_correspondencia=sum(x['primary'] and bool(x['animation_path']) for x in doc['items']),observacao='Vínculo cadastral não significa aprovação visual ou biomecânica. GIFs 2D reprovados continuam desativados.')
doc['summary']=counts;save('docs/COMPARACAO_LISTA_500.json',doc)
md='# EvoluPersonal — catálogo exclusivo da lista MD (500 exercícios)\n\nFonte única: **500 Exercícios Base de Musculação.md**. Nomes e ordem preservados.\n\n**500 exercícios · 371 com GIF vinculado · 129 sem GIF.** Os 75 GIFs novos e a equivalência MD357/e141 estão associados para revisão: vínculo cadastral não significa aprovação visual ou biomecânica.\n\nOs identificadores `eN` apontam para `dist/assets/exercises/`; os `mdN` para `dist/assets/md500-3d/`. O lote 2D reprovado continua fora do catálogo.\n\n| Nº MD | Nome original no MD | GIF |\n|---:|---|---|\n'
md+='\n'.join(f"| {x['id']} | {x['name']} | `"+x['ref']+'` |' for x in inventory)+'\n';(P/'docs/COMPARACAO_LISTA_500.md').write_text(md)
for name in ['tests.cjs','tests-gallery.cjs','tests-media.cjs']:
 f=P/name;s=f.read_text().replace('346','371').replace('154 pendentes','129 pendentes').replace('51','76')
 if name=='tests-media.cjs':s=s.replace('[1,2].flatMap','[1,2,3].flatMap').replace('items.length,50','items.length,75').replace('e.md_id)).size,50','e.md_id)).size,75').replace('PASS: 50 associações','PASS: 75 associações')
 if name=='tests-gallery.cjs':s=s.replace('lote-md500-25-02.json','lote-md500-25-03.json')
 f.write_text(s)
(P/'CHECKPOINT.md').write_text('# EvoluPersonal — checkpoint\n\nBranch: `codex/evolupersonal-media-350`. Não alterar `main` sem autorização.\n\n500 exercícios: 371 com GIF vinculado; 129 sem GIF. 75 GIFs 3D novos em três lotes de 25, todos associados e em revisão. MD357/e141 também em revisão: total76 vínculos em revisão. Legados não foram integralmente auditados.\n\nPróxima fila: `production/FILA_MD500_ATUAL.json`. Conferir inventário antes de gerar; associar cada GIF ao exercício correspondente. Fonte oficial: `docs/500-exercicios-base.md`. Nenhum deploy de produção executado.\n')
(R/'README.md').write_text('# Lote MD500-25-03\n\n25 GIFs gerados individualmente e associados ao catálogo. Todos em revisão final, sem aprovação biomecânica automática. Método: ferramenta de geração de imagens, fontes3×2, recorte e montagem em GIF144×144 em loop. Prompts completos em `fontes.json`; montagem em `assemble.py`.\n\nRevisão: conferir continuidade/enquadramento em todos; amplitude reduzida do Kas usa apenas quadros superiores; hiperextensão unilateral exclui posição hiperestendida; distinguir elevação lateral apoiada MD321 permanece pendente fora deste lote. Fontes iniciais MD77, MD321 e versões substituídas não foram associadas.\n\nIDs: '+', '.join(str(x['id']) for x in src)+'.\n')
(P/'production/ASSOCIACOES_MD500.md').write_text('# Associações MD500\n\nTrês lotes de25: 75 novos GIFs associados aos exercícios oficiais. MD357 reutiliza e141; MD16 usa e402. Total371 vinculados,129 sem GIF,76 em revisão. Main preservada. Consultar inventário e manifestos para referências exatas.\n')
print(json.dumps({'linked':371,'pending':129,'review':76,'new_batch':len(items),'duplicates':0}))
