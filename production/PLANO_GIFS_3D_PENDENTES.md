# Pendências reais de GIFs 3D — EvoluPersonal / MD500

Data: 29/10/2026. Fonte: `production/INVENTARIO_MD500.json` e lista original `docs/500-exercicios-base.md`. Todos os IDs referem-se à lista de 500 movimentos, sem novos exercícios adicionados.

## Cobertura confirmada

- **500/500** exercícios cadastrados; **445** com mídia vinculada; **55** ainda sem GIF.
- **442 GIFs distintos em uso** entre os 445 vínculos; três arquivos exatos são usados duas vezes.
- **149 GIFs 3D novos** associados anteriormente, com aprovação visual final não concluída; **296 vínculos legados**.
- **15 vínculos** tiveram aprovação visual informada pelo usuário. Desses, **9 não compartilham GIF**; **6 compõem três pares que compartilham o mesmo arquivo**. Essa aprovação não equivale à criação de novo GIF para as variações.
- **58 tarefas para uma biblioteca com animação exclusiva por exercício**, sendo 55 GIFs ausentes mais 3 possíveis substituições de arquivos compartilhados. Essa é uma previsão mínima condicionada à verificação de outros GIFs visivelmente iguais e à possibilidade de reaproveitar o legado e267.

## Três duplicações exatas — prioridade

| GIF | MDs | Plano |
|---|---|---|
| `e171.gif` | MD135, MD341 | Verificar terminal do cabo e criar animação específica do MD341 se e171 não mostrar a variação sem puxador. |
| `e110.gif` | MD140, MD340 | Manter compartilhamento provisório; avaliar `e267.gif` para uma das variações (arquivo não aprovado) e criar animação distinta se necessário. |
| `e112.gif` | MD301, MD302 | Pegadas abertas/pronadas e neutras/fechadas exigem mídias próprias. MD302 é candidato inicial à nova produção; confirmar visualmente antes de atribuição definitiva. |

**Não foi feita nenhuma substituição artificial nem remoção de animação válida.** As três duplicações permanecem sinalizadas no inventário até criação/validação dos arquivos novos.

## Cronograma de produção sugerido

Os 58 itens foram divididos em três lotes, respeitando a cadência de produção anterior:

- Lote 01: 25 exercícios — MD341, MD140, MD302, MD153, ….
- Lote 02: 25 exercícios — MD381, MD396, MD397, MD412, ….
- Lote 03: 8 exercícios — MD486, MD487, MD489, MD490, ….

## Necessidades por grupo (incluindo os três casos compartilhados)

- Ombros: 9.
- Costas: 1.
- Quadríceps: 5.
- Posteriores: 4.
- Glúteos/Adutores/Abdutores: 5.
- Bíceps/Antebraços: 4.
- Tríceps: 11.
- Panturrilha: 4.
- Abdômen/Core: 15.

## Critério de finalização

Cada GIF novo deve ser renderizado individualmente, representar equipamento, pegada, amplitude e grupo muscular do exercício correspondente, e ser aprovado antes da associação definitiva. Verificar arquivo, SHA, ID e ausência de duplicação exata; manter testes de renderização e responsividade no Android e tablet.

Dados completos e lotes: `production/FILA_PRODUCAO_3D_MD500.json`. A lista de 55 sem GIF não é alterada e continua em `production/FILA_MD500_ATUAL.json`.
