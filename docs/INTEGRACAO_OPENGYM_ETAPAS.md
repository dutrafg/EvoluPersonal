# Integração EvoluPersonal + openGym — etapas

**Branch de trabalho:** `integracao-opengym-ptbr`  
**Progresso:** 3 de 10 etapas concluídas. Ao concluir cada etapa 10, 20, 30… gerar um HTML completo e testável do EvoluPersonal para revisão.  
**Publicação:** manter a `main` intacta até aprovação explícita.

## Etapas

- [x] **1. Preparar a integração:** revisar a estrutura, preservar a biblioteca oficial MD500 e manter o trabalho isolado em branch. Registrar os limites de licenciamento; não importar mídia Gym visual.
- [x] **2. Integrar recursos de planejamento e progressão:** indicadores locais, agenda semanal, rotação A/B/C, substitutos por grupo muscular e sugestões de dupla progressão/deload.
- [x] **3. Consultar a execução anterior:** mostrar a última carga/repetições do mesmo exercício e permitir aplicá-la à série atual, respeitando a unidade e sem alterar automaticamente a prescrição.
- [x] **4. Recordes pessoais na execução:** indicar uma nova melhor marca estimada de 1RM apenas para uma série concluída, usando os registros anteriores do mesmo aluno e exercício.
- [x] **5. Comparar os 500 exercícios:** cruzar nomes, grupo, equipamento e instruções disponíveis do catálogo textual openGym. Relatório gravado em `production/COMPARACAO_MD500_OPENGYM_2026-10-30.md` e CSV com todos os candidatos.
- [ ] **6. Validar movimentos candidatos:** conferir instruções PT-BR, grupo muscular e equipamento dos candidatos contra a execução dos GIFs próprios. A ficha externa serve como referência textual; não aprova um GIF sozinha.
- [ ] **7. Corrigir biblioteca oficial:** corrigir nomes, grupos, instruções e associações incorretas, mantendo os IDs `md1…md500`.
- [ ] **8. Completar as animações ausentes:** criar GIFs próprios para os exercícios ainda sem mídia; não copiar nem vincular mídia do Gym visual.
- [ ] **9. Auditar os 500 vínculos:** revisar exercício, movimento, equipamento, arquivo GIF e estado de aprovação de cada item; exportar a fila de pendências.
- [ ] **10. Revisão integrada:** gerar o HTML completo para teste do fluxo e da biblioteca revisada; documentar o que ainda precisa de verificação em Android físico.

**Regra da prévia:** após cada dez etapas concluídas (10, 20, 30…), gerar um HTML completo e testável para revisão. Progresso atual: **5 de 10**.

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
- **Etapa 5:** a triagem comparou os 500 IDs do inventário com 5.632 exercícios e 5.632 nomes PT-BR do openGym. Resultado: 18 nomes exatos únicos, 1 nome exato ambíguo, 60 candidatos fortes, 129 candidatos para revisão e 292 sem correspondência confiável por nome. Os nomes no CSV são candidatos, não validações biomecânicas.
- A lista Markdown tem somente 498 linhas numeradas; faltam nela os números 127 e 132, que constam do inventário oficial. O inventário foi usado como referência para comparar todos os 500.
- Nenhum arquivo de mídia nem instrução longa foi copiado para o EvoluPersonal. A análise usa referências, metadados e contagem de instruções; cada GIF ainda precisa ser conferido individualmente.
