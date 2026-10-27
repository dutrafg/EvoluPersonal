# Método de montagem dos treinos dos PDFs

Estado: análise funcional para implementação. O aplicativo atual ainda usa séries uniformes; estes recursos não estão implementados. Fontes lidas integralmente: The Last Natural (5 páginas) e Treino Letícia (5 páginas, última vazia).

## Estrutura compartilhada

1. Organizar dias e grupos musculares; ordenar exercícios.
2. Preparar o primeiro exercício de cada grupo muscular no dia: 10 repetições com 40–50% da carga de trabalho.
3. Antes de cada exercício: feeder set, 6 repetições com 60–70% da carga de trabalho.
4. Executar séries de trabalho com volume e faixa de repetições específicos.
5. Somente quando marcado: depois da série mais pesada, reduzir a carga em 30%, descansar 30 segundos e realizar uma série adicional de back-off.
6. Registrar carga, repetições e esforço para orientar a próxima sessão.

As faixas percentuais pertencem aos documentos. A escolha do percentual exato deve ser feita pelo personal. Um valor de carga precisa indicar se é total, por halter, por lado, placas da máquina ou resistência não mensurável.

## The Last Natural

- Divisão PPLUL de 5 sessões: Push, Pull, Legs, Upper e Lower.
- 32 posições de exercícios no cronograma, incluindo exercícios repetidos entre dias.
- Séries de trabalho especificadas por exercício: em geral 2 ou 3. Elevação lateral, desenvolvimento, fly invertido e abdutor apresentam indicação explícita de 8–10 repetições.
- Progressão geral apresentada como 5–9 repetições: buscar mais repetições com a mesma carga e aumentar a carga quando atingir 9. O documento não esclarece se a condição vale para todas as séries ou apenas a principal; isso deve ser configurado pelo personal.
- Esforço proposto pelo autor: RIR 0–1 / falha técnica nas séries de trabalho. Registrar como parâmetro desse modelo, editável por exercício e série; não aplicar automaticamente a todo aluno ou a séries preparatórias.
- Excêntrica de 2–3 segundos e intenção de concêntrica rápida. O próprio documento flexibiliza a referência de cadência 2:3. Usar campos distintos, sem deduzir uma cadência rígida para todos os movimentos.
- Back-off assinalado em supino inclinado articulado, remada baixa triângulo, hack squat, supino inclinado Smith e elevação pélvica.
- Cardio: 150 minutos semanais, com sugestão de 30 minutos em 5 dias. Abdômen: 3 vezes por semana; exercícios e séries não estão definidos.

## Treino Letícia

- Três sessões nomeadas A, B e Sábado, com 7, 7 e 6 exercícios, respectivamente; 20 posições de exercícios.
- A: costas e ombros, incluindo trabalho de braços.
- B: braços, costas, peito e ombros.
- Sábado: peito, antebraços e ombros, incluindo puxada e tríceps.
- Descanso de 1 minuto aparece na coluna principal de todos os exercícios.
- Aquecimento e feeder aparecem nas notas do primeiro exercício de vários grupos; exercícios seguintes do grupo usam feeder sem novo aquecimento.
- Back-off marcado em remada baixa articulada (A), supino reto com barra (B) e desenvolvimento máquina (Sábado).
- Cargas são valores daquela ficha; não devem virar cargas padrão de outros alunos.

## Ambiguidades que o aplicativo não deve resolver silenciosamente

| Ponto | Como aparece | Comportamento necessário |
|---|---|---|
| Repetições da Letícia | Coluna com 10, notas com 8–10 | Importação mantém os dois textos e pede resolução pelo personal; não sobrescrever um com o outro |
| Contagem de séries da Letícia | Coluna com 4 ou 5 e notas de aquecimento/feeder | Definir se a contagem é total ou só de trabalho antes de gerar linhas de séries |
| Progressão Natural | Regra geral 5–9, alguns exercícios 8–10 | Faixa por exercício prevalece após confirmação; não aplicar 5–9 a todos |
| Condição de progressão | Não define todas as séries vs. principal | Campo explícito de critério; padrão de importação pendente de revisão |
| Base do back-off | Natural: série mais pesada; Letícia usa notas semelhantes | Referenciar a série/carga base explicitamente e calcular 70% dessa carga |
| Carga não informada | Traço em algumas linhas | Manter sem carga definida; não converter em 0 kg nem inventar peso |
| Sem exercícios de abdômen/cardio detalhados | Natural define frequência/minutos | Criar metas/blocos pendentes, sem inventar exercícios ou séries |
| Nomes ambíguos | Supino voador, elevação unilateral de ombro, etc. | Vincular somente após definir a variação; consultar auditoria de exercícios |

## Modelo funcional proposto

### Aluno → plano → sessão → exercício → série

Cada série terá tipo próprio: aquecimento, preparatória (feeder), trabalho ou back-off. Uma série de trabalho poderá ser marcada como principal/top set. Back-off deve apontar para a série que fornece sua carga de referência.

Dados por exercício: GIF da biblioteca, ordem, grupo muscular para aquecimento, equipamento, unilateralidade, carga e unidade, faixa de repetições, séries, descanso, RIR alvo e cadência opcional.

Dados por série: tipo, carga fixa ou percentual, referência do percentual, repetições mínimas/máximas, descanso, RIR alvo, observações e registro realizado. Distinguir carga planejada de carga realizada.

Método pertence à prescrição, não à biblioteca: o mesmo GIF deve ser reutilizado em diferentes planos, sem duplicar o exercício por causa de feeder, back-off, carga ou faixa de repetições.

### Editor do personal

1. Escolher aluno e divisão de sessões (PPLUL, A/B/Sábado ou personalizada).
2. Adicionar exercícios obrigatórios disponíveis e indicar variantes ainda sem GIF.
3. Escolher quantidade de séries de trabalho; inserir preparatórias separadamente.
4. Inserir aquecimento no primeiro exercício do grupo do dia com opção de ajuste manual.
5. Aplicar feeder e, quando necessário, back-off por exercício.
6. Configurar descanso, repetições, RIR e critério de progressão.
7. Rever resumo antes de salvar: séries preparatórias, séries de trabalho e back-offs contados separadamente por grupo e sessão.

### Execução pelo aluno

Exibir sequência de séries com rótulos claros e GIF acessível em cada exercício. Registrar carga, repetições e RIR realizados, tempo de descanso e conclusão. Mostrar back-off como série adicional após a referência correspondente; recalcular a sugestão se a carga realizada da série base mudar. O personal pode corrigir a sugestão.

### Progressão

O app sugere, o personal define os critérios. Armazenar faixa por exercício, qual série precisa atingir o teto, esforço esperado e incremento disponível. Mostrar proposta para a próxima sessão, sem alterar retroativamente histórico e sem aumentar carga automaticamente por uma única série parcial. Arredondamento deve respeitar incrementos reais do equipamento e mostrar valor bruto e valor escolhido.

### Preservação de dados existentes

Treinos atuais continuam como séries de trabalho. Evoluir o esquema de backup e migrar sem apagar alunos, treinos ou sessões. Registrar os tipos e parâmetros em sessões concluídas para preservar o que de fato foi executado.

## Etapas de implementação

1. Modelo de séries por tipo, referências percentuais e migração de dados.
2. Editor do personal e resumo de volume por tipo/grupo.
3. Tela do aluno, cargas sugeridas, cronômetro por série e histórico.
4. Sugestões de progressão e critérios editáveis.
5. Modelos PPLUL e A/B/Sábado com revisão obrigatória das ambiguidades acima.
6. Importação assistida dos PDFs; nenhuma publicação automática de treino de aluno.

## Critérios de aceitação

- Feeder, aquecimento e back-off não inflam a contagem de séries de trabalho.
- Back-off mostra 70% da carga de referência antes do arredondamento.
- Alterar uma sessão não modifica registros concluídos.
- Uma linha sem carga permanece sem carga definida.
- Faixas 5–9 e 8–10 podem coexistir no mesmo plano.
- Treinos e backups anteriores permanecem utilizáveis.
- Regras metodológicas dos PDFs são parâmetros de modelos, não afirmações universais de eficácia nem obrigatoriedades para todos os alunos.
