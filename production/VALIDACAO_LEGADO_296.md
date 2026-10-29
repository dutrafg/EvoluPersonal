# Validação cadastral dos 296 GIFs legados — 29/10/2026

**Escopo:** branch `codex/md500-revisao-associacoes-20261029`. Este documento valida referências e metadados de origem, **não a execução biomecânica**. Não houve inspeção visual de quadros dos GIFs.

- 296 associações legadas documentadas e persistidas no catálogo MD500.
- 281 com coerência cadastral/documental e sem divergência específica levantada.
- 15 vínculos foram aprovados visualmente pelo usuário em 29/10/2026; desses, seis em três GIFs compartilhados ainda precisam de solução para exclusividade.
- Todos os 296 GIFs apontam para arquivos existentes na branch, com SHA correspondente ao inventário do GitHub.
- Nenhum GIF novo foi produzido; os 55 sem mídia continuam pendentes. Três GIFs também são compartilhados e requerem uma decisão sobre mídia exclusiva.
- 3 pares de exercícios compartilham arquivo (MD135/341, MD140/340, MD301/302).
- **1 correção feita na branch:** MD319 de `e208` (polia) para `e179` (halter e apoio fixo).

## Casos que exigem inspeção visual específica

- MD46 — Crucifixo na Máquina (Braços estendidos) → `e102`: Confirmar se os braços estão estendidos, e não apoiados como no voador MD45.
- MD66 — Remada Curvada com Barra (Pegada Supinada / Yates Row) → `e128`: Correção anterior e34→e128: fonte explicita pegada supinada; confirmar a execução visual.
- MD89 — Remada Sentado na Máquina (Pegada Neutra) → `e109`: Confirmar pegada neutra na remada articulada da máquina.
- MD102 — Remada Invertida na Barra (Australian Pull-up) → `e229`: e229 mostra remada invertida na barra do Smith, uma variação da barra fixa; conferir escopo.
- MD135 — Crucifixo Inverso no Cabo (Foco em Upper Back/Romboides) → `e171`: e171 compartilhado com MD341; verificar tipo de puxador e trajetória.
- MD140 — Crucifixo Inverso na Máquina (Peck Deck Inverso com escápulas móveis) → `e110`: e110 compartilhado com MD340; confirmar postura e escápulas móveis.
- MD301 — Desenvolvimento na Máquina (Pegada Pronada Aberta) → `e112`: e112 não especifica pegada pronada aberta; confirmar.
- MD302 — Desenvolvimento na Máquina (Pegada Neutra Fechada) → `e112`: e112 não especifica pegada neutra fechada; confirmar.
- MD312 — Desenvolvimento Invertido na Parede (Handstand Push-up / Pike Push-up) → `e88`: e88 mostra pike push-up; não valida handstand push-up, apenas alternativa da descrição.
- MD319 — Elevação Lateral Unilateral Inclinado (Segurando na coluna do aparelho) → `e179`: Reassociado e208→e179 pela especificação de halter e apoio; confirmar visual.
- MD340 — Crucifixo Inverso no Peck Deck / Voador Inverso (Pegada Pronada ou Neutra) → `e110`: e110 compartilhado com MD140; conferir pegada pronada/neutra.
- MD341 — Crucifixo Inverso Cruzado na Polia Alta / Média (Sem puxador, segurando nas bolinhas do cabo) → `e171`: e171 compartilhado com MD135; confirmar execução cruzada sem puxadores.
- MD357 — Rosca no Banco Inclinado 45° com Halteres (Braços alongados atrás do tronco) → `e141`: e141 descreve rosca inclinada com braços atrás do corpo; confirmar ângulo e técnica.
- MD391 — Flexão de Punho em Pé por Trás das Costas com Barra ou no Smith → `e341`: e341 descreve barra atrás do corpo, mas instrução genérica de apoio de antebraços requer inspeção.
- MD471 — Elevação de Joelhos Pendurado na Barra Fixa (Hanging Knee Raise) → `e69`: e69 orienta elevação de joelhos na instrução, apesar de título genérico sobre pernas suspensas.

## Interpretação dos estados

- `coerencia_documental`: o exercício e o arquivo possuem fontes compatíveis, sem contradição técnica textual específica detectada; não equivale a GIF aprovado.
- `revisar_variacao`: há detalhes específicos, ambiguidades ou arquivo compartilhado; manter vínculo provisório até revisão dos quadros.
- `nao_inspecionado`: o GIF binário não foi reproduzido/analisado visualmente nesta etapa.

Arquivo completo de evidências: `production/VALIDACAO_LEGADO_296.json`.
Para revisão visual, abrir `dist/revisao-vinculos-md500.html` e filtrar **Somente GIFs legados (296)**.
Executar `node scripts/validar_cobertura_500.cjs` e `node scripts/validar_legado_296.cjs` antes de qualquer integração.
A publicação da auditoria na main foi autorizada pelo usuário em 29/10/2026, sem declarar GIFs repetidos como únicos.
