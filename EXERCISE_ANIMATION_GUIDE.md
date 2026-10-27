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

1. Concluído: lote 1 com 25 GIFs próprios ligados ao catálogo em `dist/assets/exercises/`.
2. Concluído: lote 2 (exercícios e25–e49), elevando a biblioteca para 50 GIFs. Cada animação é um GIF original em loop e está ligada ao exercício correspondente.
3. Concluído: lote 3 (e50–e74), elevando a biblioteca para 75 GIFs.
4. Concluído: lote 4 (e75–e99), atingindo 100 GIFs originais.
5. Próximo marco: ampliar por padrão de movimento até cerca de 500 exercícios.
6. Cada lote publicado deve atualizar o catálogo, o contador e os metadados em português brasileiro.
7. Conferir nomes brasileiros, duplicatas, equipamento, músculos e instruções de cada novo lote; não contar variações quase idênticas sem explicitar equipamento, pegada, posição ou objetivo.
8. Produzir GIFs originais individuais; não incorporar mídia de terceiros.

## Fontes técnicas consultadas

- Biblioteca de exercícios ACE: https://www.acefitness.org/resources/everyone/exercise-library/ — referência de execução e grupos musculares.
- ACE, protocolo baseado em evidências para posteriores da coxa: https://www.acefitness.org/resources/pros/expert-articles/9015/the-hamstrings-blueprint-evidence-based-exercises-for-better-function/ — referência para flexão de joelho e levantamento unilateral.
- ACE, guia de exercícios para glúteos: https://www.acefitness.org/resources/pros/expert-articles/8807/strength-training-the-glutes-an-evidence-based-approach/ — referência para agachamentos, passada e extensão de quadril.

As ilustrações são didáticas e não substituem avaliação individual ou instrução de profissional de Educação Física. Movimentos com limitações clínicas exigem revisão profissional antes de recomendação.
