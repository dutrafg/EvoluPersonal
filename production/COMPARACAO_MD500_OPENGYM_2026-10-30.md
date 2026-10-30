# Comparação de nomes MD500 × openGym

**Data:** 30/10/2026  
**Escopo:** comparação de nomes e metadados de 500 exercícios do inventário MD500 com os 5.632 registros do catálogo openGym e suas 5.632 entradas PT-BR. O catálogo externo foi usado como referência de pesquisa; nenhuma imagem/animação foi copiada, vinculada ou incluída no aplicativo.

**Fonte da lista oficial:** `production/INVENTARIO_MD500.json` (500 IDs)  
**Fonte de comparação:** `DuarteSantos8/openGym`, catálogo PT-BR e índice de exercícios; revisão feita somente por nome, grupo muscular, equipamento declarado e existência de instruções.  
**Versão consultada do openGym:** `b6cfe2bbd3f099523ffbf2677438864e9a09a06f`

## Resultado

| Classificação | Quantidade |
|---|---:|
| Nome exato único | 18 |
| Nome exato com mais de um registro | 1 |
| Candidato forte (nome, grupo e equipamento compatíveis) | 60 |
| Candidato para revisão manual | 165 |
| Sem correspondência confiável por nome | 258 |
| **Total** | **500** |

A classificação automática é uma triagem, não uma aprovação biomecânica. “Candidato” indica que vale conferir a ficha textual; não comprova que um GIF específico representa o movimento. O campo `Passos PT-BR` no CSV informa se o candidato tem instruções traduzidas. Nenhum texto de instruções ou mídia do catálogo externo foi copiado para a biblioteca oficial.

## Divergência encontrada na lista MD500

O arquivo `docs/500-exercicios-base.md` contém **498 linhas numeradas**, enquanto o inventário oficial contém 500 itens. Os números ausentes da lista Markdown são **127 e 132**; ambos existem no inventário e possuem associações no acervo atual. A comparação usou o inventário de 500 IDs para não omitir exercícios.

## Próximos passos

1. Revisar primeiro os candidatos fortes e as correspondências exatas, conferindo se grupo/equipamento e a execução exibida no GIF correspondem ao nome oficial.
2. Conferir manualmente os candidatos em revisão; não aceitar só pela semelhança textual.
3. Para os 279 itens sem correspondência confiável, pesquisar o movimento por sinônimos/nomes em inglês e usar as instruções do openGym apenas como referência de validação.
4. Completar os GIFs ausentes com animações próprias, seguindo o padrão 3D já definido; manter os itens ainda não validados com estado de revisão.
5. Revalidar individualmente a associação dos 500 GIFs antes de considerar a biblioteca fechada.

O CSV ao lado traz os 500 itens, estado atual da mídia e até três candidatos por nome.
