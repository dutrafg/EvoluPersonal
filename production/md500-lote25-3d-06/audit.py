from pathlib import Path
import json
R=Path(__file__).resolve().parent;P=R.parents[1]
inv=json.loads((P/'production/INVENTARIO_MD500.json').read_text())
tech=json.loads((R/'technical-validation.json').read_text())
files={x['path']:x['sha'] for x in json.loads((R/'remote-files.json').read_text())}
files.update({x['output_path']:x['gif_blob_sha'] for x in tech})
items=[];shared={}
for x in inv:
 path='dist/'+x['animation_path'] if x['animation_path'] else None
 if path:
  assert files.get(path)==x['gif_blob_sha'],(x['id'],path)
  shared.setdefault(path,[]).append(x['id'])
 items.append({'md_id':x['id'],'name':x['name'],'media_ref':x['ref'],'path':path,'gif_blob_sha':x['gif_blob_sha'],'file_present':bool(path),'correspondence':'vinculo_cadastral_verificado' if path else 'sem_midia','visual_review':x['review_status']})
linked=sum(x['file_present'] for x in items);review=sum(x['media_review_pending'] for x in inv)
assert len(items)==500 and linked==445 and review==155
report={'scope':'Revisão cadastral de IDs, nomes, referências, caminhos e hashes. Não equivale a aprovação visual/biomecânica integral.','total':500,'linked':linked,'missing':500-linked,'new_3d':149,'visual_review_pending':review,'correction':{'md_id':66,'old_ref':'e34','new_ref':'e128','evidence':'production/e128-source.json descreve underhand barbell bent-over row, palms forward.'},'variant_review_ids':[135,301,302,341],'shared_legacy_references':{k:v for k,v in shared.items() if len(v)>1},'items':items}
(P/'production/REVISAO_CORRESPONDENCIAS_MD500.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
md='# Revisão de correspondências MD500\n\n500 registros: **445 com GIF vinculado;55 sem mídia**.149 GIFs3D novos associados.155 vínculos em revisão.\n\nConferidos IDs, nomes, catálogo/inventário/documentação, caminhos e hashes dos445 arquivos, além da fila de55 pendentes. GIFs2D reprovados continuam desativados.\n\nCorreção:MD66 Remada Curvada Supinada passou de e34 para e128, arquivo existente com fonte que especifica pegada supinada. Nenhuma nova animação duplicada foi criada.\n\nMD135/341 e MD301/302 compartilham arquivos cuja fonte não detalha toda a variação de pegada/acessório; ficaram marcados em revisão. MD140/340 compartilham a mesma base de crucifixo inverso na máquina.\n\nA revisão cadastral não certifica a biomecânica de todas as animações. As149 mídias novas e seis vínculos legados estão sinalizados em revisão. Outros legados não foram integralmente auditados visualmente.\n\n## Sem mídia\n\n'
md+='\n'.join('- MD'+str(x['id'])+' — '+x['name'] for x in inv if not x['animation_path'])+'\n'
(P/'production/REVISAO_CORRESPONDENCIAS_MD500.md').write_text(md)
print(json.dumps({'records':500,'linked':linked,'missing':500-linked,'review':review,'corrected_mapping':66}))
