import json, hashlib
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
plan_path = root/'production/lote17-plan.json'
plan = json.loads(plan_path.read_text())
cues = [
 'Ajuste o banco para manter os pegadores na altura do peito. Apoie as costas e os pés, empurre os braços da máquina à frente e retorne controlando a carga.',
 'Prenda os tornozelos no apoio do aparelho declinado. Mantenha cabeça e ombros abaixo do quadril e empurre os pegadores acima da parte inferior do peito, aproximando-os sem bater.',
 'Deite no banco horizontal do aparelho e apoie os pés. Empurre os pegadores acima do peito e retorne devagar, mantendo as costas apoiadas.',
 'Deite no banco reto e segure as alças paralelas da barra suíça, com palmas entre si. Desça a barra em direção ao peito e empurre sem dobrar os punhos.',
 'No banco inclinado, mantenha as palmas das mãos voltadas uma para a outra. Desça os halteres ao lado do peito e empurre mantendo ombros e costas apoiados.',
 'No banco reto, inicie com as palmas entre si. Empurre os halteres girando gradualmente os punhos para a pegada pronada no alto e desfaça a rotação na descida.',
 'Ajuste o banco em 30 graus. Com pés firmes e pegada pronada, desça os halteres ao lado da parte superior do peito e empurre sem elevar os ombros.',
 'Ajuste o banco em baixa inclinação, a 15 graus. Apoie os pés e as costas, desça os halteres ao lado do peito e empurre com controle.',
 'Deite no banco reto com um halter em uma mão. Mantenha os dois pés firmes e o tronco sem girar; desça o peso ao lado do peito e empurre. Repita do outro lado.',
 'Posicione o banco inclinado entre duas polias baixas. Com cotovelos levemente flexionados e ângulo estável, aproxime os pegadores acima do peito e abra os braços com controle.',
 'Com a polia na altura do ombro, segure um pegador e mantenha o tronco estável. Leve o braço em arco à frente do peito, conservando a leve flexão do cotovelo; retorne e troque o lado.',
 'Deite no banco reto e segure a barra W acima do peito. Com cotovelos levemente flexionados, leve a barra em arco para trás da cabeça dentro da amplitude controlada e retorne.',
 'Alinhe o corpo em prancha, desça o peito e empurre de forma explosiva. Bata uma palma com as mãos fora do solo e aterrisse amortecendo com os cotovelos, sem perder o alinhamento.',
 'Apoie as coxas sob as almofadas e segure as alças paralelas da barra romana. Puxe em direção à parte superior do peito mantendo o tronco firme e retorne devagar.',
 'Ajuste o apoio das coxas e segure os dois pegadores da máquina articulada. Puxe os braços do aparelho para baixo e para dentro sem balançar o tronco, depois retorne com controle.',
 'Prenda o elástico à barra fixa e apoie um joelho na alça. Segure a barra em pronação, eleve o corpo sem balanço e desça controlando a ajuda do elástico.',
 'Prenda o triângulo à barra fixa e segure as alças com palmas entre si. Mantendo os pés suspensos, incline levemente o tronco para trás e aproxime o esterno do pegador; desça controlando.',
 'Apoie os pés na plataforma e segure a barra romana em pegada neutra. Puxe o pegador ao abdômen com coluna estável e retorne sem projetar o tronco.',
 'Sentado na remada baixa, segure a barra reta com as palmas para cima. Puxe ao abdômen mantendo os cotovelos próximos das costelas e retorne sem balançar.',
 'Apoie o peito no encosto da máquina e segure os pegadores em pronação aberta. Puxe com os cotovelos afastados e aproxime as escápulas, mantendo o peito apoiado.',
 'Incline o tronco a partir do quadril, com joelhos levemente flexionados. Segure a barra do Smith em pronação e puxe ao abdômen sem mudar a posição das costas; desça na guia.',
 'Apoie o peito no banco inclinado com os pés firmes e espaço livre para a barra. Puxe a barra em direção à parte inferior do peito e estenda os braços sem tirar o tronco do apoio.',
 'Fique ao lado e paralelo à barra presa no landmine. Apoie a mão livre no banco, puxe a extremidade carregada em direção ao quadril e retorne sem girar o tronco.',
 'Incline o tronco com os dois pés apoiados no chão. Apoie a mão livre na coxa e puxe a barra do Smith com uma mão em direção à cintura; desça na guia sem girar o tronco.',
 'Afaste os pés e incline o tronco com coluna estável. Apoie uma mão no kettlebell que permanece no chão e reme o outro em direção ao quadril; desça e alterne os lados sem girar o corpo.'
]
equipment = ['Máquina de supino vertical','Máquina articulada declinada','Máquina de supino horizontal','Banco reto e barra suíça','Banco inclinado e halteres','Banco reto e halteres','Banco a 30 graus e halteres','Banco a 15 graus e halteres','Banco reto e um halter','Banco inclinado e duas polias baixas','Polia média e pegador','Banco reto e barra W','Peso corporal','Polia alta e barra romana','Máquina articulada de puxada','Barra fixa e elástico','Barra fixa e triângulo','Polia baixa e barra romana','Polia baixa e barra reta','Máquina de remada com apoio peitoral','Smith','Banco inclinado e barra','Landmine e banco de apoio','Smith','Dois kettlebells']
report=[]
for i,e in enumerate(plan):
 e.update(cue=cues[i],equipment=equipment[i],url='',motion=e['id'],animation=f"assets/exercises/{e['id']}.gif",animation_alt=f"Demonstração em loop de {e['name']}")
 if e['id']=='e423':
  e['movement']='One-arm bent-over Smith row, both feet on floor, free hand on thigh, neutral spine. Pull bar vertically toward waist and lower without torso rotation. No bench.'
 if e['list_id'] in [51,52]: e['muscles']='Peitoral maior e deltoide anterior'
 if e['list_id']==54: e['muscles']='Peitoral maior, latíssimo do dorso e serrátil anterior'
 gif=root/'dist'/e['animation']; im=Image.open(gif)
 assert im.n_frames>=6 and im.info.get('loop')==0,e['id']
 frames=[]
 for f in range(im.n_frames):
  im.seek(f);frames.append(hashlib.sha256(im.convert('RGB').tobytes()).hexdigest())
 assert len(set(frames))>=4,e['id']
 meta=dict(e,source_sheet=f"production/sprites/{e['id']}.png",illustration='Folha original de seis poses convertida em GIF cíclico',generator='OpenAI image generation',references=[e['reference']])
 (root/f"production/{e['id']}-source.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2))
 report.append({'id':e['id'],'list_id':e['list_id'],'frames':im.n_frames,'distinct_frames':len(set(frames)),'loop':0,'size':gif.stat().st_size,'sha256':hashlib.sha256(gif.read_bytes()).hexdigest()})
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
html=root/'dist/index.html'; h=html.read_text()
assert '"id":"e400"' not in h
insertion='\n// Lote 17: variantes da lista MD, IDs estáveis e400–e424.\ncatalog.push(...'+json.dumps(plan,ensure_ascii=False,separators=(',',':'))+');\n'
assert 'const seed=()=>' in h
h=h.replace('const seed=()=>',insertion+'const seed=()=>',1).replace('Alpha 0.8','Alpha 0.9').replace('Alpha 0.2','Alpha 0.9').replace('ALPHA 0.2','ALPHA 0.9').replace('400 exercícios','425 exercícios')
html.write_text(h)
(root/'dist/evolupersonal-425-exercicios.html').write_text(h)
r=root/'README.md';r.write_text(r.read_text().replace('Alpha 0.8','Alpha 0.9').replace('400 exercícios','425 exercícios')+'\n## Lote 17\n\n25 variações da lista MD adicionadas com GIFs originais e IDs e400–e424. Total: 425 GIFs. As 500 linhas da referência não equivalem à contagem do catálogo, que inclui variações e sinônimos anteriores.\n')
guide=root/'EXERCISE_ANIMATION_GUIDE.md';guide.write_text(guide.read_text()+'\n## Lote 17 — e400–e424\n\n25 variantes da lista MD com sprites originais e GIFs em loop. Total: 425 GIFs, faltam 75 para a meta numérica. Produção conforme `production/lote17-plan.json`.\n')
(root/'production/lote17-validation.json').write_text(json.dumps({'total_new_gifs':25,'catalog_total':425,'items':report},indent=2))
print(json.dumps({'created':25,'catalog_total':425,'distinct_list_ids':len(set(e['list_id'] for e in plan))}))
