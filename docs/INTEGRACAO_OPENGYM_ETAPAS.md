# Integração EvoluPersonal + openGym — etapas

**Branch de trabalho:** `integracao-opengym-ptbr`  
**Progresso:** 3 de 10 etapas concluídas. Ao concluir cada etapa 10, 20, 30… gerar um HTML completo e testável do EvoluPersonal para revisão.  
**Publicação:** manter a `main` intacta até aprovação explícita.

## Etapas

- [x] **1. Preparar a integração:** revisar a estrutura, preservar a biblioteca oficial MD500 e manter o trabalho isolado em branch. Registrar os limites de licenciamento; não importar mídia Gym visual.
- [x] **2. Integrar recursos de planejamento e progressão:** indicadores locais, agenda semanal, rotação A/B/C, substitutos por grupo muscular e sugestões de dupla progressão/deload.
- [x] **3. Consultar a execução anterior:** mostrar a última carga/repetições do mesmo exercício e permitir aplicá-la à série atual, respeitando a unidade e sem alterar automaticamente a prescrição.
- [ ] **4. Recordes pessoais na execução:** indicar quando uma série concluída supera a melhor marca registrada, com cálculo claro e histórico por aluno/exercício.
- [ ] **5. Mais formatos de execução:** melhorar registros de séries cronometradas, isométricos e cardio sem forçar repetições ou carga nesses casos.
- [ ] **6. Biblioteca complementar isolada:** preparar importação selecionada de dados textuais do openGym sem misturar itens externos aos 500 oficiais MD500; incluir atribuição e licença por origem.
- [ ] **7. Busca complementar:** filtrar a biblioteca importada por grupo muscular, equipamento e nome, mantendo os vínculos com exercícios usados em treinos.
- [ ] **8. Rotinas iniciais editáveis:** oferecer modelos de divisão semanal feitos para o EvoluPersonal, sem copiar telas, código ou texto não permitido do openGym.
- [ ] **9. Fluxo de dados entre aparelhos:** definir um caminho de exportação/importação compatível com os backups atuais e preparar a base para sincronização futura.
- [ ] **10. Revisão integrada:** gerar o HTML completo para teste do fluxo ponta a ponta, verificar a navegação e documentar o que ainda precisa de dispositivo Android real.

## Limites de conteúdo

- Os 500 exercícios e IDs `md1…md500` continuam como biblioteca oficial do EvoluPersonal.
- As animações Gym visual não podem ser copiadas, extraídas, vinculadas por hotlink nem reutilizadas sem licença própria.
- O catálogo textual do openGym tem origens distintas: os registros `textSource: "exercisedb"` têm aviso MIT; o restante e as traduções são cobertos pela AGPL-3.0. A etapa 6 deve manter origem, licença e avisos explícitos.
- Não copiar o aplicativo integralmente. Implementações próprias podem reproduzir necessidades funcionais compatíveis, sem reutilizar telas ou trechos protegidos.

## Etapa 3 — implementação

- `dist/training-methods.js`: consulta o registro concluído mais recente do mesmo exercício, série, aluno e unidade. Quando houver correspondência, exibe a carga e as repetições anteriores.
- O botão **Usar carga anterior** aplica o valor apenas à série atual e salva como registro manual; não muda a prescrição nem outras séries.
- Sem registro compatível, a tela continua igual e nenhum valor presumido é preenchido.
