# Revisão dos 15 GIFs — retorno do usuário (29/10/2026)

**Resultado declarado:** «Aprovados, mas tem alguns repetidos». A decisão foi registrada para os **15 vínculos**, sem arquivo JSON de critérios individuais. A aprovação não resolve a exigência de mídias distintas para variações diferentes.

## Conferência de arquivos repetidos

| GIF exato | IDs da lista MD500 | Avaliação |
|---|---|---|
| `e171.gif` | MD135 e MD341 | Variação de pegadores e execução no crossover. Não atribuir automaticamente a mesma execução como exclusiva. |
| `e110.gif` | MD140 e MD340 | Mesmo equipamento e família de movimento; examinar se a duplicidade é aceitável ou se a variante exige outra mídia. |
| `e112.gif` | MD301 e MD302 | Pegada pronada aberta versus neutra fechada; requer demonstrações diferenciadas. |

## Status quantitativo

- 15 associações aprovadas visualmente conforme mensagem do usuário.
- 12 arquivos GIF fisicamente distintos entre os 15.
- 3 pares com arquivo idêntico (SHA igual) e sem resolução de exclusividade.
- 9 vínculos de arquivo não compartilhado nesse grupo; 6 vínculos envolvidos nos 3 compartilhamentos.
- Todos os 500 exercícios permanecem cadastrados; 445 continuam com mídia e 55 sem GIF (nenhum novo GIF gerado).

## Próximas ações para deduplicação

1. **MD301/MD302:** identificar qual pegada e112 ilustra e produzir GIF específico para a outra variação.
2. **MD135/MD341:** confirmar se e171 utiliza puxadores e gerar/anexar alternativa sem puxadores quando necessário.
3. **MD140/MD340:** candidato legado não utilizado `e267.gif` (crucifixo inverso com apoio de peito) existe e possui outro SHA. **Não foi inspecionado nem reatribuído**, exige revisão técnica para decidir se representa a variação.
4. Executar auditoria também para **semelhanças visuais** que não compartilhem arquivo: a análise por SHA não identifica essas ocorrências.

**Branch:** `codex/md500-revisao-associacoes-20261029` — **não modificar main sem autorização.**
