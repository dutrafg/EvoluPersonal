# Guia da biblioteca ilustrada EvoluPersonal

## Direção

Construir um catálogo de aproximadamente 500 exercícios, com nome, orientação, equipamento, grupo muscular, nível e demonstração visual, em português brasileiro. Cada exercício da biblioteca deve ter um GIF original em loop, com poses próprias, modelo 3D vestido em roupa de compressão e músculos principais destacados em laranja. Usar as fontes externas para conferir movimento e cobertura; não incorporar arquivos de imagem ou animação de terceiros. Ícones estáticos não contam como exercício animado.

## Referências para pesquisa e estrutura

- `https://github.com/bryllim/workout-guide`: estudar consistência entre quadros, organização de assets e metadados. A arte do repositório é CC BY-SA 4.0 e deriva de Everkinetic; não copiar suas figuras para o EvoluPersonal.
- `https://github.com/rfivesix/OpenExerciseDB`: estudar esquema de exercícios, grupos musculares, equipamento, identificadores e validação de catálogo. Os dados são CC BY-SA 4.0 e a documentação informa que registros upstream podem ter licenças próprias; não importar registros ou mídia sem verificar as respectivas licenças.
- `https://www.acefitness.org/resources/everyone/exercise-library/`: referência técnica por movimento para conferir posição inicial, trajetória e retorno. Registrar internamente a página consultada para cada exercício.

## Requisitos por exercício

Identificador estável; nome brasileiro; sinônimos de pesquisa; região e músculos primários/secundários; equipamento; nível; instrução curta; posição inicial e final; amplitude ilustrada; alertas técnicos relevantes; origem da consulta; autor/revisor da demonstração; GIF próprio em loop e descrição acessível da animação.

## Sequência de produção

1. Concluído: lote 1 (e0–e24), com 25 GIFs ligados ao catálogo.
2. Concluído: lote 2 (e25–e49), total de 50 GIFs.
3. Concluído: lote 3 (e50–e74), total de 75 GIFs.
4. Concluído: lote 4 (e75–e99), total de 100 GIFs.
5. Concluído: lote 5 (e100–e124), total de 125 GIFs.
6. Concluído: lote 6 (e125–e149), corrigindo a ligação entre mídia e catálogo; total de 150 GIFs.
7. Concluído: lote 7 (e150–e174), total de 175 GIFs.
8. Concluído: lote 8 (e175–e199), total de 200 GIFs.
9. Concluído: lote 9 (e200–e224), total de 225 GIFs.
10. Concluído: lote 10 (e225–e249), total de 250 GIFs.
11. Concluído: lote 11 (e250–e274), total de 275 GIFs.
12. Concluído: lote 12 (e275–e299), total de 300 GIFs.
13. Concluído: lote 13 (e300–e324), total de 325 GIFs.
14. Concluído: lote 14 (e325–e349), total de 350 GIFs.
15. Concluído: lote 15 (e350–e374), total de 375 GIFs. Faltam 125 para a meta.
15. Próximo marco: ampliar por padrões de movimento até 500 exercícios.
16. Cada lote publicado atualiza o catálogo, o contador e os metadados em português brasileiro.
17. Conferir nomes brasileiros, duplicatas, equipamento, músculos e instruções; explicitar diferenças de pegada, posição, equipamento ou objetivo nas variações.
18. Produzir GIFs originais individuais; não incorporar mídia de terceiros.

- StrengthLog: referências dos exercícios do lote 11 estão registradas em `production/e250-source.json` a `production/e274-source.json`.

- StrengthLog: referências dos exercícios do lote 12 estão registradas em `production/e275-source.json` a `production/e299-source.json`.
- StrengthLog: referências dos exercícios do lote 13 estão registradas individualmente em `production/e300-source.json` a `production/e324-source.json`.
- ACE: consulta técnica registrada por exercício em `production/e325-source.json` a `production/e349-source.json`.

## Fontes técnicas consultadas

- StrengthLog e ACE: referências de execução consultadas no lote 10, registradas por exercício em `production/e225-source.json` a `production/e249-source.json`.

- StrengthLog e ACE: referências de execução do lote 9 registradas individualmente em `production/e200-source.json` a `production/e224-source.json`.

- StrengthLog, biblioteca e guias técnicos de crossover, elevação lateral, crucifixo inverso, abdutora/adutora na polia, extensão de quadril, flexão nórdica, flexão de joelhos na bola, abdominal na máquina e caminhada unilateral: páginas por exercício registradas nos arquivos `production/e175-source.json` a `production/e199-source.json`.
- ACE, biblioteca de exercícios: https://www.acefitness.org/resources/everyone/exercise-library/

- Biblioteca de exercícios ACE: https://www.acefitness.org/resources/everyone/exercise-library/ — referência de execução e grupos musculares.
- ACE, protocolo baseado em evidências para posteriores da coxa: https://www.acefitness.org/resources/pros/expert-articles/9015/the-hamstrings-blueprint-evidence-based-exercises-for-better-function/ — referência para flexão de joelho e levantamento unilateral.
- ACE, guia de exercícios para glúteos: https://www.acefitness.org/resources/pros/expert-articles/8807/strength-training-the-glutes-an-evidence-based-approach/ — referência para agachamentos, passada e extensão de quadril.

As ilustrações são didáticas e não substituem avaliação individual ou instrução de profissional de Educação Física. Movimentos com limitações clínicas exigem revisão profissional antes de recomendação.

- ACE: consulta de movimento por exercício para o lote 15 registrada em `production/e350-source.json` a `production/e374-source.json`; sprites originais individuais em `production/sprites/`.


## Lote 16 — e375–e399

25 exercícios da lista de 500, com 25 folhas de sprites originais e 25 GIFs cíclicos em pt-BR. Total após publicação: 400 GIFs; faltam 100.

## Lote 17 — e400–e424

25 variantes da lista MD com sprites originais e GIFs em loop. Total: 425 GIFs, faltam 75 para a meta numérica. Produção conforme `production/lote17-plan.json`.
