# Auditoria inicial das associações MD500 — 29/10/2026

Escopo: branch de revisão `codex/md500-revisao-associacoes-20261029`. Não altera a `main`. Verificação dos nomes, IDs, fontes, existência e SHA dos GIFs; **não é uma aprovação visual**.

- Registros da lista original: **500**; com GIF associado: **445**; sem GIF: **55**.
- Novos GIFs 3D: **149**, todos associados ao MD pretendido pelos lotes de origem.
- Vínculos legados: **296**. Os nomes e arquivos são consistentes cadastralmente; resta confirmar cada execução.
- Arquivos compartilhados em vínculos: **6 registros**, referentes a **3 arquivos**.
- Vínculos com marcador anterior de revisão: **155**. Não equivale a contagem de aprovados.

## Casos para verificação prioritária

- MD46 — Crucifixo na Máquina (Braços estendidos) → `e102` — Confirmar braços estendidos e pegadores, não apoios de antebraço.
- MD135 — Crucifixo Inverso no Cabo (Foco em Upper Back/Romboides) → `e171` — GIF compartilhado com MD341; conferir pegadores e trajetória.
- MD140 — Crucifixo Inverso na Máquina (Peck Deck Inverso com escápulas móveis) → `e110` — GIF compartilhado com MD340; conferir aparelho e mobilidade escapular.
- MD301 — Desenvolvimento na Máquina (Pegada Pronada Aberta) → `e112` — GIF compartilhado com MD302; confirmar pegada pronada aberta.
- MD302 — Desenvolvimento na Máquina (Pegada Neutra Fechada) → `e112` — GIF compartilhado com MD301; confirmar pegada neutra fechada.
- MD319 — Elevação Lateral Unilateral Inclinado → `e179` (antes `e208`) — corrigida a divergência documental: `e179` descreve exercício com halter e apoio; `e208` descreve polia. Mídia permanece sem inspeção visual.
- MD340 — Crucifixo Inverso no Peck Deck / Voador Inverso (Pegada Pronada ou Neutra) → `e110` — GIF compartilhado com MD140; confirmar pegada.
- MD341 — Crucifixo Inverso Cruzado na Polia Alta / Média (Sem puxador, segurando nas bolinhas do cabo) → `e171` — GIF compartilhado com MD135; confirmar ausência de puxadores.
- MD357 — Rosca no Banco Inclinado 45° com Halteres (Braços alongados atrás do tronco) → `e141` — Correspondência e141 plausível, aprovação visual pendente.
- MD471 — Elevação de Joelhos Pendurado na Barra Fixa (Hanging Knee Raise) → `e69` — Título do GIF e69 é genérico, mas sua instrução técnica orienta elevar os joelhos; confirmar execução visual.

## Como revisar

1. Abra `dist/revisao-vinculos-md500.html` mantendo `dist/assets/` no mesmo diretório.
2. Filtre os casos prioritários e verifique a execução real (equipamento, pegada, trajetória, amplitude e ciclo).
3. Se correto, marque os quatro critérios e aprove; em caso de divergência, registre o motivo e, se possível, proponha outra referência de GIF existente.
4. Exporte o JSON de auditoria. Aprovação/reprovação apenas no navegador **não** modifica o inventário ou `dist/index.html`.
5. Reconciliar manualmente o JSON aprovado com os arquivos oficiais, revalidar e só publicar na `main` após autorização explícita.

## Regras de segurança

- Os 55 exercícios sem GIF não receberão substituições genéricas.
- Os GIFs 2D reprovados em `dist/assets/md500/` são excluídos das opções de associação.
- Não confundir consistência de nome/ID/SHA com fidelidade visual ou biomecânica.
- Mídia compartilhada não será considerada correta para variações distintas sem confirmação.
