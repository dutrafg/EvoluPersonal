> Atualização de associação — 28/10/2026: os 25 GIFs deste lote agora estão vinculados aos exercícios no aplicativo da branch de desenvolvimento, com identificação de revisão pendente. O texto abaixo registra a situação no momento da produção; não constitui aprovação biomecânica.

# MD500-25-02 — segundo lote de GIFs com visual 3D

25 GIFs novos, de números MD distintos, sem repetir os 25 GIFs do lote MD500-25-01. A fonte dos nomes continua sendo docs/500-exercicios-base.md.

## Estado

- Produzidos e tecnicamente validados; revisão visual inicial feita, **aprovação final visual/biomecânica pendente**.
- Não integrados ao aplicativo. A cobertura cadastrada permanece em 295/500.
- Arquivos finais em dist/assets/md500-3d; a galeria revisao.html lista apenas este lote.
- Total dos dois lotes: 50 novos GIFs produzidos. Fila de criação posterior: 154 entradas, além da equivalência já encontrada MD357/e141 que precisa de decisão de vínculo.
- A main não foi alterada.

## Exercícios

- MD116 — Levantamento Terra Snatch Grip (Pegada muito aberta)
- MD162 — Agachamento Acima da Cabeça (Overhead Squat)
- MD163 — Agachamento Jefferson (Barra entre as pernas)
- MD166 — Agachamento Sumô no Smith
- MD168 — Agachamento Hack com Barra Livre (Barra por trás das pernas)
- MD176 — Afundo Estático com Barra Livre (Split Squat)
- MD177 — Afundo Estático com Halteres
- MD184 — Agachamento Búlgaro com Barra Livre
- MD187 — Subida no Banco com Barra
- MD188 — Step-up Lateral na Caixa
- MD191 — Agachamento Pistol (Unilateral com peso do corpo)
- MD211 — RDL em Base Assimétrica (B-Stance RDL com Barra ou Halteres)
- MD213 — RDL na Polia Baixa
- MD217 — Bom Dia no Smith
- MD218 — Bom Dia com Barra de Segurança (SSB Good Morning)
- MD251 — Elevação Pélvica com Halter ou Kettlebell
- MD257 — Frog Pump (Ponte de glúteo com solas dos pés unidas)
- MD258 — Elevação Pélvica com Pés Elevados no Banco
- MD305 — Desenvolvimento Alternado Sentado com Halteres
- MD306 — Push Press com Barra (Desenvolvimento com impulso das pernas)
- MD307 — Z-Press (Desenvolvimento sentado no chão com pernas estendidas à frente)
- MD313 — Desenvolvimento com Kettlebell de Cabeça para Baixo (Bottoms-up KB Press)
- MD374 — Rosca Arrasto com Barra ou no Smith (Drag Curl - cotovelos vão para trás)
- MD379 — Rosca Garçom (Waiter's Curl - segurando a cabeça de um único halter com as duas mãos)
- MD380 — Rosca com Anilha (Plate Curl)

## Produção e revisão

Renders raster anatômicos com aspecto 3D, personagem cinza, músculos destacados em laranja e fundo navy. Não são modelos 3D editáveis. A folha de cada exercício foi criada separadamente. MD163 recebeu edição corretiva para remover alças inventadas e colocar as mãos diretamente na barra reta. A tentativa anterior não compõe o GIF final.

A montagem recorta as poses, retira separadores quando presentes e aplica frame-order.json para organizar os retornos. MD305 usa oito quadros para alternar os braços; os demais usam seis. Exportação 144×144 e loop contínuo. Alguns renders têm deriva de enquadramento, sobretudo nos step-ups, que permanece registrada em revisao-visual.json para revisão final. Nenhum arquivo foi marcado como aprovado automaticamente.

## Verificação

25 IDs e nomes pertencentes à lista; nenhuma interseção com os IDs do primeiro lote; 25 hashes distintos; nenhum arquivo binariamente igual a qualquer GIF preexistente; decodificação de todos os quadros; dimensões e loop conferidos. technical-validation.json registra os hashes dos bytes enviados.

## Continuidade

Use production/INVENTARIO_MD500.json e production/FILA_MD500_ATUAL.json como controles atuais. Os inventários e filas dentro das pastas de cada lote preservam o estado daquele lote. Não reconstrua a fila de criação apenas pelos vínculos antigos do HTML, pois isso repetiria os 50 GIFs já produzidos e ainda não integrados.

Partição atual da lista: 295 vínculos existentes + 50 novos produzidos sem vínculo + 1 candidato de equivalência existente + 154 a produzir = 500.


