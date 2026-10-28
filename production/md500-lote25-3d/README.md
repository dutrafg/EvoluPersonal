# MD500 — lote de 25 GIFs com visual 3D

## Auditoria antes da produção

| Medida | Total |
|---|---:|
| Exercícios na lista original | 500 |
| GIFs legados em dist/assets/exercises | 425 |
| Nomes normalizados distintos no acervo legado | 415 |
| Entradas MD com vínculo cadastrado no aplicativo | 295 |
| GIFs legados distintos usados nesses vínculos | 290 |
| Entradas sem vínculo antes deste lote | 205 |
| Animações 2D reprovadas, excluídas da produção válida | 30 |
| Prévia MD292 anterior, excluída da produção válida | 1 |

A auditoria verifica inventário, nomes, IDs, fontes e hashes. Não certifica a biomecânica de todo o legado. Não foram encontrados arquivos binariamente iguais entre os 425 GIFs legados. Foram identificados dez pares com o mesmo nome normalizado e cinco referências compartilhadas entre linhas do MD; detalhes em auditoria.json.

MD357 não foi recriado: production/e141-source.json já descreve rosca em banco inclinado com braços atrás do tronco. MD16 aponta para e400 (supino sentado), embora e402 declare a variante deitada; essa correção cadastral está registrada, sem alterar o aplicativo neste lote.

## Entrega

25 GIFs animados novos de 25 números MD distintos, produzidos individualmente. Resolução de exportação: 144×144, loop contínuo. Cada exercício usa seis renders-chave; Rosca 21 contém 105 quadros para demonstrar 7 repetições inferiores, 7 superiores e 7 completas, com identificação de fase e repetição. Técnica de criação: renders raster com aspecto 3D via image_gen, recorte das poses e montagem em GIF; não são modelos 3D editáveis.

Os 25 arquivos finais ficam em dist/assets/md500-3d. A galeria local revisao.html usa esses arquivos. Fontes e prompts: fontes.json. Testes de arquivo: technical-validation.json.

**Estado: produzidos, com revisão visual inicial; aprovação final pendente. Não integrados ao aplicativo e não somados à cobertura cadastrada de 295.** Há pequenas variações de enquadramento entre poses em alguns renders; por isso não se presume aprovação final. A main não foi alterada.

## Exercícios deste lote

- MD292 — Desenvolvimento Sentado com Halteres
- MD76 — Puxada Alta Ajoelhado na Polia
- MD88 — Remada Baixa Unilateral na Polia Sentado
- MD101 — Remada Alta na Polia Sentado com Corda (Puxando em direção ao peito/pescoço)
- MD109 — Pulldown Unilateral na Polia Alta
- MD152 — Agachamento com Barra de Segurança (Safety Bar Squat - SSB)
- MD118 — Encolhimento de Ombros com Barra por Trás
- MD122 — Encolhimento de Ombros no Smith
- MD170 — Leg Press Vertical (90 Graus)
- MD123 — Encolhimento de Ombros na Polia Baixa
- MD178 — Afundo Estático no Smith
- MD207 — Stiff com Halteres
- MD208 — RDL no Smith
- MD125 — Encolhimento com Barra Hexagonal (Trap Bar Shrug)
- MD493 — Toque nos Calcanhares Deitado (Heel Touches)
- MD249 — Elevação Pélvica no Smith
- MD298 — Desenvolvimento no Smith (Pela Frente)
- MD303 — Desenvolvimento Articulado Convergente
- MD373 — Rosca 21 (7 repetições metade inferior + 7 metade superior + 7 completas)
- MD473 — Abdominal Infra no Solo ou Banco (Elevação de pernas deitado)
- MD38 — Landmine Press (Empurrada unilateral ou bilateral na barra T)
- MD111 — Pullover no Cabo Declinado ou no Banco Reto
- MD115 — Levantamento Terra com Déficit (Em cima de anilha/caixote)
- MD128 — Remada Alta Pegada Fechada (Foco em Trapézio)
- MD23 — Supino Guilhotina (Neck Press) com Barra

## Saídas rejeitadas

Tentativas de MD153, MD155, MD171 e MD226 apresentaram representação insuficiente ou incorreta dos aparelhos. MD229 apresentou assistência não prevista e MD120 apresentou flexão dos cotovelos em duas tentativas. Não fazem parte destes 25 GIFs e continuam na fila. Foram substituídos por MD118, MD122, MD123, MD125, MD493 e MD128.

## Continuidade sem duplicação

inventario-md500.json registra, separadamente, o vínculo atual e os 25 novos arquivos produzidos. proxima-fila.json contém 179 entradas para produção posterior, excluindo estes 25 e a equivalência MD357/e141. Os 25 novos arquivos e o e141 ainda exigem decisão de integração ao aplicativo; a fila de produção não deve ser reconstruída apenas a partir dos vínculos antigos do HTML.

Verificações antes do envio: 25 IDs únicos e pertencentes ao MD; nomes exatos; 25 hashes únicos; nenhum hash igual aos GIFs preexistentes; decodificação de todos os quadros; dimensões, loop e sequência 7+7+7 da Rosca 21.

