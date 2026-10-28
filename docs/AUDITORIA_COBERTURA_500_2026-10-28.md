# Auditoria de cobertura do catálogo — 28/10/2026

## Escopo

Fonte normativa: `500 Exercícios Base de Musculação.md` (500 itens numerados).
Catálogo do aplicativo: `dist/index.html`, 425 registros e0–e424 com caminhos declarados de GIF.
Mapeamento: `docs/COMPARACAO_LISTA_500.md`.
Esta auditoria verifica **correspondência de cadastro**; não certifica execução biomecânica nem qualidade visual quadro a quadro.

| Indicador | Antes das revisões | Depois |
|---|---:|---:|
| Itens MD com correspondência documental | 197 | **284** |
| Itens com variante relacionada, ainda não confirmada | 11 | **25** |
| Itens a criar/sem correspondência | 292 | **191** |
| Itens do MD sem cobertura específica confirmada | 303 | **216** |
| Registros/GIFs declarados no catálogo | 425 | 425 |

Foram recuperadas **87 correspondências cadastrais** que estavam indevidamente pendentes nos relatórios anteriores (43 na primeira revisão e 44 nesta). Nenhum GIF novo foi criado apenas por fazer esta reclassificação.

## Principais e obrigatórios

- Dos 65 exercícios intitulados «Base / Principais» na lista, **63 têm vínculo cadastral** após a identificação do **Bom Dia com Barra (MD nº 206)** como e136.
- Ainda exigem especificação ou verificação visual: **MD nº 292 — Desenvolvimento Sentado com Halteres** (e8 genérico não atesta postura) e **MD nº 357 — Rosca Inclinada a 45° com Halteres** (e141 não atesta ângulo).
- Requisitos dos dois PDFs de treino: **38 de 43** têm cobertura declarada (21 já existentes + 17 adicionados como e100–e116); **5** descrições seguem ambíguas: panturrilha horizontal, remada pronada, stiff, supino voador na máquina e elevação unilateral de ombro.
- Os 17 obrigatórios e100–e116 foram reclassificados como integrados no catálogo. GIFs e100, e108 e e116 tiveram existência confirmada no repositório; não foi feita validação visual integral dos 17.

## Duplicações potenciais nos planos anteriores

Os planos `production/lote18-plan.json`, `lote19-plan.json` e `lote20-plan.json` **não foram alterados**, porque o lote 18 pode ter trabalho já produzido fora do backup registrado. Os pares abaixo requerem conferência antes de qualquer nova geração; diferenças reais de técnica ou implemento devem ser documentadas em vez de eliminadas por semelhança de nome.

| Item já planejado | Registro existente potencialmente equivalente |
|---|---|
| e435 — Flexão de braços com pés elevados | e164 — Flexão declinada |
| e436 — Flexão de braços com mãos elevadas | e25 — Flexão inclinada |
| e437 — Flexão com toque no ombro | e70 — Prancha com toque nos ombros (confirmar se houve flexão) |
| e441 — Pullover com halter no banco | e38 — Pullover com halter |
| e443 — Elevação lateral sentada com halteres | e59 — Elevação lateral sentada |
| e446 — Rosca martelo na corda | e188 — Rosca martelo com corda na polia |
| e448 — Rosca direta na polia baixa | e111 — Rosca direta na polia |
| e455 — Supino reto com halteres em pegada neutra | e225 — Supino com halteres e pegada neutra |
| e456 — Supino inclinado com halteres em pegada neutra | e404 — Supino Inclinado com Halteres e Pegada Neutra |
| e464 — Barra fixa com pegada neutra | e127 — Barra fixa neutra |
| e478 — Hip thrust na máquina | e157 — Elevação pélvica na máquina |
| e493 — Prancha lateral com abdução da perna | e395 — Prancha lateral com abdução de quadril |
| e497 — Woodchop de cima para baixo na polia | e246 — Rotação diagonal alta para baixa na polia |

**Lote 18:** os arquivos `dist/assets/exercises/e425.gif` e `e449.gif` não foram encontrados na branch auditada na verificação de GitHub; isso impede confirmar o backup completo, mas não prova que o material não exista em outro local. Recuperar e confrontar o trabalho anterior antes de sobrescrever e425–e449.

## Fila de execução

A fila completa está em `production/FILA_PRIORIDADE_COBERTURA_MD500.json`, com **216 pendências**: três grupos de 25 prioridades (A, B e C) e **141** casos no backlog. As prioridades A, B e C são **fila editorial, não GIFs criados ou lotes já publicados**. Elas não ocupam automaticamente os IDs e425–e499.

- **Prioridade A (25):** resolver as duas bases restantes e melhorar puxadas, equipamentos de pernas e exercícios fundamentais.
- **Prioridade B (25):** exercícios compostos, acessórios e alternativas de equipamentos, distinguindo versões já previstas nos lotes antigos.
- **Prioridade C (25):** deltoides, bíceps, tríceps, panturrilhas e core.

Quatro prioridades já têm cadastro de produção *planejada* e requerem reconciliação: MD nº 386 → e449 (lote 18), nº 373 → e467 (lote 19), nº 208 → e484 (lote 20) e nº 476 → e495 (lote 20).

## Critérios de aceite antes de encerrar a biblioteca

1. Preservar e validar a produção existente e os backups do lote 18.
2. Para cada exercício novo, registrar o número do MD (1–500), o ID do catálogo, a variante exata, equipamento, posição, pegada, músculos, instrução de movimento e a demonstração GIF original.
3. Validar presença e assinatura do arquivo GIF, navegação no catálogo, controles de seleção e ausência de duplicações; revisar amplitude e biomecânica visualmente.
4. Subir cada lote de 25 para a **branch de trabalho**, preservando `main` até autorização.
5. Executar `node scripts/validar_cobertura_500.cjs` após cada atualização e atualizar a comparação. **O script foi adicionado, mas ainda não foi executado em um checkout completo nesta sessão.**
6. Não anunciar cobertura de 500 itens com base exclusivamente na contagem de GIFs. Mesmo acrescentando 75 GIFs, a lista original pode continuar incompleta.

## Arquivos e mudanças

- `docs/COMPARACAO_LISTA_500.md`: tabela detalhada corrigida; **284 / 500** correspondências documentais.
- `docs/EXERCICIOS_OBRIGATORIOS_PDFS.json`: status corrigido dos 17 obrigatórios.
- `production/FILA_PRIORIDADE_COBERTURA_MD500.json`: fila integral com 216 pendências.
- `scripts/validar_cobertura_500.cjs`: verificação local de estrutura, GIFs, tabela, obrigatórios e fila.
