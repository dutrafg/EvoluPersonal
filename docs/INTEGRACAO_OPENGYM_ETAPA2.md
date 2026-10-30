# EvoluPersonal — integração funcional inspirada no openGym

**Ambiente:** branch `integracao-opengym-ptbr` (não publicar em `main` sem aprovação).

## Base preservada

- Mantidos os 500 exercícios oficiais do MD500, seus identificadores `md1…md500`, GIFs locais e pendências de revisão.
- Mantidos o banco `evolupersonal.alpha1`, o formato de backup (versão 2), os registros de alunos, as sessões e os métodos de prescrição existentes.
- Nenhum arquivo de imagem, vídeo ou animação da Gym visual foi importado.
- As implementações desta etapa são código novo do EvoluPersonal; **não representam a importação integral do código ou do catálogo do openGym**.

## Recursos integrados nesta branch

1. **Evolução de treinos:** `dist/insights.js`. Volume, 1RM estimada, sessões, séries, gráfico de oito semanas, CSV com neutralização de fórmulas.
2. **Agenda semanal:** `db.weekPlan` opcional, por aluno, com dias de descanso; não afeta histórico.
3. **Rotação de treinos:** `db.rotationPlan` opcional, objeto por aluno `{order: [ids], cursor: número}`. Ordem A/B/C; avanço somente quando o treino esperado é concluído. A exclusão e a mudança de proprietário removem referências inválidas.
4. **Exercícios substitutos:** em cada item de treino, `alternatives` opcional (até cinco IDs de exercícios do mesmo grupo). No rascunho, `substitutions` opcional (índice do item → exercício efetivo). A prescrição não é alterada; séries concluídas impedem trocas; registros históricos guardam o exercício efetivamente executado.
5. **Dupla progressão:** em `item.progression`, `scheme: "double"` é opcional. Até atingir a faixa máxima, sugere progredir repetições sem aumentar carga; quando todas as séries elegíveis alcançam o máximo, preserva a regra preexistente de sugestão de aumento de carga.
6. **Deload sugerido:** somente com dupla progressão; `deloadAfter` opcional (2–6, padrão 3) e `deloadPercent` opcional (5–30, padrão 10). Considera consecutivamente as sessões anteriores do mesmo treino, sem automatizar ajuste de carga.

## Segurança e dados

- Propriedades adicionais são opcionais: backups anteriores continuam válidos e não são convertidos automaticamente.
- Validação rejeita referências cruzadas inválidas, IDs substitutos duplicados, substitutos de outro grupo, rotação fora de limite e parâmetros inválidos de deload.
- Ao excluir treinos, a agenda semanal e a rotação são limpas; o histórico permanece.
- A exportação CSV protege contra células interpretadas como fórmulas.
- Um protótipo HTML não substitui testes em navegador móvel real.

## Testes automatizados

Executar a partir da raiz do repositório com Node.js 22:

```sh
node tests.cjs
node tests-methods.cjs
node tests-gallery.cjs
node tests-insights.cjs
node tests-weekly.cjs
node tests-rotation.cjs
node tests-substitutions.cjs
node tests-progression.cjs
```

Workflow: `.github/workflows/qa-integracao-opengym.yml` na branch de desenvolvimento.

## Não realizados nesta etapa

- Importação do catálogo textual de milhares de exercícios do openGym. A biblioteca MD500 continua como única biblioteca oficial e não admite entrada automática de itens externos.
- Migração completa dos módulos e do código do openGym (AGPL-3.0) e adaptação de notificações, sincronização e integração com sistemas de saúde.
- Cópia das imagens e animações da Gym visual, cuja reutilização independente requer licença.
- Compilação de APK híbrido e testes em Android físico; o app atual permanece HTML/PWA.
- Publicação na `main` ou implantação de produção.

## Referências de licenciamento

- [Licença de código do openGym (AGPL-3.0)](https://github.com/DuarteSantos8/openGym/blob/main/LICENSE)
- [Avisos de terceiros e catálogo](https://github.com/DuarteSantos8/openGym/blob/main/NOTICE.md)
- [Restrições específicas das mídias](https://github.com/DuarteSantos8/openGym/blob/main/catalogue/media/NOTICE.md)

