# Continuidade — EvoluPersonal / MD500

Atualizado em 28/10/2026.

## Situação atual

- Fonte: docs/500-exercicios-base.md, 500 nomes e IDs oficiais.
- Aplicativo da branch de mídia: **346 exercícios com GIF vinculado e 154 sem GIF**.
- Os 50 GIFs novos dos lotes MD500-25-01/02 estão associados por número MD e usam dist/assets/md500-3d/.
- **51 vínculos em revisão**: os 50 novos e a equivalência legada MD357/e141. Associação não significa aprovação visual ou biomecânica.
- MD16 foi corrigido de e400 (supino sentado) para e402 (supino deitado/horizontal).
- Acervo legado: 425 arquivos. O lote de 30 GIFs 2D reprovados continua desativado.
- A fila de criação permanece em **154 exercícios**. Não recriar os 50 novos ou o MD357 já associado.

## Controles atuais

- production/INVENTARIO_MD500.json: 500 linhas, caminho associado, SHA do arquivo e estado de revisão.
- production/FILA_MD500_ATUAL.json: 154 exercícios sem mídia.
- docs/COMPARACAO_LISTA_500.md e .json: vínculos sincronizados com o aplicativo.
- production/lote-md500-25-01.json e lote-md500-25-02.json: associados; aprovação final pendente.
- production/ASSOCIACOES_MD500.md: resumo da associação e validação.
- scripts/validar_cobertura_500.cjs: verifica app, inventário, tabela e fila sem depender das contagens históricas antigas.

## Continuidade

Criar um exercício por vez somente quando não houver mídia correspondente. Conferir equipamento e variante; reutilizar arquivos equivalentes em vez de duplicar. Enviar lotes de 25 com a associação ao número MD registrada, preservando o estado de revisão. A mídia reprovada em dist/assets/md500/ não pode voltar a ser ativada.

Trabalhar em codex/evolupersonal-media-350. **Não alterar main sem autorização.** A atualização das associações aplica-se ao código de desenvolvimento; não implica publicação do site de produção.

