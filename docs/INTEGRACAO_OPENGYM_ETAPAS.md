# Integração EvoluPersonal + openGym — etapas

**Branch de trabalho:** `integracao-opengym-ptbr`  
**Progresso:** 10 de 10 marcos técnicos concluídos para a prévia de conceito. A conferência visual final dos movimentos continua sinalizada como pendente dentro do HTML.  
**Publicação:** manter a `main` intacta até aprovação explícita.

## Etapas

- [x] **1. Preparar a integração:** revisar a estrutura, preservar a biblioteca oficial MD500 e manter o trabalho isolado em branch. Registrar os limites de licenciamento; não importar mídia Gym visual.
- [x] **2. Integrar recursos de planejamento e progressão:** indicadores locais, agenda semanal, rotação A/B/C, substitutos por grupo muscular e sugestões de dupla progressão/deload.
- [x] **3. Consultar a execução anterior:** mostrar a última carga/repetições do mesmo exercício e permitir aplicá-la à série atual, respeitando a unidade e sem alterar automaticamente a prescrição.
- [x] **4. Recordes pessoais na execução:** indicar uma nova melhor marca estimada de 1RM apenas para uma série concluída, usando os registros anteriores do mesmo aluno e exercício.
- [x] **5. Comparar os 500 exercícios:** cruzar nomes, grupo, equipamento e instruções disponíveis do catálogo textual openGym. Relatório gravado em `production/COMPARACAO_MD500_OPENGYM_2026-10-30.md` e CSV com todos os candidatos.
- [x] **6. Criar Meus treinos e exportações:** cadastrar rotinas nomeadas por aluno com treinos A–G independentes; levar o atalho de cada aluno à Evolução; consultar histórico de carga apenas no mesmo treino; exportar a rotina e a tabela de evolução pela impressão em PDF.
- [x] **7. Cruzar candidatos com OpenGym:** auditar nome, equipamento e grupo nos 77 candidatos exatos/fortes; 77/77 têm `bodyPart` compatível com o grupo da MD500. A aprovação visual individual dos GIFs permanece pendente.
- [x] **8. Corrigir e conferir a biblioteca oficial:** ajustar a formatação dos itens 127 e 132; conferir 500 IDs únicos (1–500) no inventário e na tabela de comparação. Nenhuma associação ambígua ou sem correspondência confiável foi forçada.
- [x] **9. Completar a prévia conceitual:** adicionar animações inline aos 55 cartões sem GIF na prévia HTML. Cada uma está identificada como conceito e movimento não validado; os arquivos finais continuam pendentes.
- [x] **10. Auditar e preparar a prévia:** confirmar 500 linhas e 500 IDs MD únicos no CSV; manter os estados de mídia e aprovação explícitos; corrigir erros de sintaxe que causavam a tela vazia; gerar o HTML completo para teste em Android.

**Regra da prévia:** após cada dez etapas concluídas (10, 20, 30…), gerar um HTML completo e testável para revisão. Progresso atual: **10 de 10 marcos técnicos da prévia**. Os 55 GIFs finais e a aprovação visual dos movimentos continuam pendentes.

## Etapa 6 — rotinas e evolução por aluno

- `dist/programs.js` cria rotinas nomeadas e atribui cada uma a um aluno; cada rotina tem sete espaços de treino (A–G), e cada treino mantém seu próprio título e exercícios.
- A tela Meus treinos permite criar/editar cada letra, renomear ou remover a rotina, abrir a Evolução já filtrada pelo aluno e exportar a prescrição em formato de impressão/PDF.
- O módulo de Evolução pode ser filtrado por aluno e reúne sessões, séries, cargas, repetições, volume e recordes estimados; oferece exportação em tabela para impressão/PDF.
- A carga anterior só é sugerida quando aluno, exercício, série, unidade e ID do treino correspondem. Rotinas diferentes não compartilham sugestões de carga.
- Backups antigos sem o campo de rotinas continuam importáveis; apagar os dados também remove as rotinas.

## Etapa 7 — cruzamento textual concluído

- Revisão por metadados dos 77 candidatos exatos/fortes: grupo corporal corresponde em 77/77. A lista contém 18 nomes exatos, 1 exato ambíguo e 58 candidatos fortes.
- Criada a página `production/REVISAO_VISUAL_MD500.html` para marcar cada GIF como correto, associação incorreta ou pendente e exportar o resultado em CSV.
- A prévia sinaliza a revisão visual como pendente e oferece os controles do revisor. Correspondência textual ou de `bodyPart` não foi usada para aprovar um GIF.

## Limites de conteúdo

- Os 500 exercícios e IDs `md1…md500` continuam como biblioteca oficial do EvoluPersonal.
- As animações Gym visual não podem ser copiadas, extraídas, vinculadas por hotlink nem reutilizadas sem licença própria.
- O catálogo textual do openGym tem origens distintas: os registros `textSource: "exercisedb"` têm aviso MIT; o restante e as traduções são cobertos pela AGPL-3.0. A etapa 6 deve manter origem, licença e avisos explícitos.
- Não copiar o aplicativo integralmente. Implementações próprias podem reproduzir necessidades funcionais compatíveis, sem reutilizar telas ou trechos protegidos.

## Etapa 3 — implementação

- `dist/training-methods.js`: consulta o registro concluído mais recente do mesmo exercício, série, aluno e unidade. Quando houver correspondência, exibe a carga e as repetições anteriores.
- O botão **Usar carga anterior** aplica o valor apenas à série atual e salva como registro manual; não muda a prescrição nem outras séries.
- Sem registro compatível, a tela continua igual e nenhum valor presumido é preenchido.


## Etapas 4 e 5 — progresso

- **Etapa 4:** a execução agora identifica uma nova melhor 1RM estimada nas séries concluídas, usando apenas sessões anteriores do mesmo aluno e exercício. O cálculo é mostrado como estimativa; não altera o treino.
- **Etapa 5:** a triagem comparou os 500 IDs do inventário com 5.632 exercícios e 5.632 nomes PT-BR do openGym. Resultado: 18 nomes exatos únicos, 1 nome exato ambíguo, 58 candidatos fortes, 165 candidatos para revisão e 258 sem correspondência confiável por nome. Os nomes no CSV são candidatos, não validações biomecânicas.
- A lista Markdown e o inventário contêm 500 exercícios. Os itens 127 e 132 estão presentes, mas sem espaço após o ponto. A revisão dos 77 candidatos exatos/fortes confirmou correspondência de grupo corporal em 77/77; isso não valida visualmente os GIFs.
- Nenhum arquivo de mídia nem instrução longa foi copiado para o EvoluPersonal. A análise usa referências, metadados e contagem de instruções; cada GIF ainda precisa ser conferido individualmente.

## Prévia HTML — correção do carregamento

- O HTML único foi atualizado após o print no Android mostrar somente o cabeçalho. A causa foi uma quebra de linha escapada como texto e quatro aspas escapadas em excesso no JavaScript da página; os separadores e handlers foram corrigidos.
- Os quatro blocos JavaScript embutidos passaram na verificação de sintaxe. O arquivo atualizado está na Library como `EvoluPersonal_Teste_Completo.html` (versão 1).
- A prévia continua buscando GIFs no repositório privado e depende de internet/acesso ao GitHub. O pacote offline requer a versão HTTPS.
- As etapas 7–9 continuam pendentes de validação visual completa e produção das 55 animações. Por isso, o progresso não foi marcado como 10/10.



## Marcos 7–10 — auditoria e prévia conceitual

- O CSV tem 500 linhas, IDs MD únicos de 1 a 500 e sem linhas com quantidade incorreta de colunas. Status OpenGym: 18 nomes exatos, 1 exato ambíguo, 58 candidatos fortes, 165 para revisão manual e 258 sem correspondência confiável.
- A prévia HTML contém animações SVG inline nos 55 exercícios sem GIF. O rótulo deixa claro que é conceito e não valida movimento; nenhuma mídia externa foi copiada ou aprovada por causa dessas animações.
- O HTML foi corrigido para remover sequências `\\n` literais entre instruções JavaScript e escapes excedentes em manipuladores de evento, causa da tela vazia observada no Android.
- Limite desta entrega: ainda requer conferência visual humana dos GIFs ligados e produção de 55 arquivos finais antes de tratar a biblioteca como aprovada para uso real.
