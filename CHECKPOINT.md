# Continuidade — EvoluPersonal / MD500

Atualizado em 28/10/2026.

## Situação atual

- Fonte: docs/500-exercicios-base.md, 500 nomes e IDs oficiais.
- Aplicativo: 295 entradas vinculadas a GIFs legados; 205 ainda sem vínculo no HTML.
- Acervo legado: 425 arquivos GIF (415 nomes normalizados distintos). A revisão biomecânica integral desse legado não está concluída.
- Novos arquivos com visual 3D: **50 GIFs produzidos em dois lotes de 25**, ainda para revisão final e sem integração ao aplicativo.
- Equivalência para evitar repetição: MD357 possui candidato legado e141, conforme production/e141-source.json; confirmar vínculo em vez de gerar novamente.
- Fila de criação: **154 entradas**. A soma 295 vinculadas + 50 produzidas sem vínculo + 1 equivalência candidata + 154 a produzir fecha os 500 IDs.
- Os 30 GIFs 2D reprovados e a prévia antiga MD292 não entram nos novos lotes nem na cobertura.

## Arquivos de controle atuais

- production/INVENTARIO_MD500.json — situação das 500 linhas, incluindo os 50 novos arquivos.
- production/FILA_MD500_ATUAL.json — 154 exercícios que ainda exigem criação.
- production/lote-md500-25-01.json — primeiro lote de 25.
- production/lote-md500-25-02.json — segundo lote de 25.
- production/md500-lote25-3d/ — auditoria e revisão do lote 01.
- production/md500-lote25-3d-02/ — auditoria, prompts, revisão e validação do lote 02.
- dist/assets/md500-3d/ — 50 GIFs novos, com revisão final pendente.

## Regras para continuar

Produzir individualmente, usando apenas nomes/variantes da lista MD. Conferir o inventário atual, o equipamento, o movimento e o hash antes de incluir um novo arquivo. Não reconstruir a fila apenas a partir do HTML, pois os novos GIFs ainda não estão vinculados. Manter as tentativas com equipamento incorreto fora dos arquivos finais. Somente integrar à cobertura após revisão final; um arquivo gerado não implica aprovação biomecânica.

Trabalhar em codex/evolupersonal-media-350 e enviar lotes de 25. **Não alterar main sem autorização.** Nenhum vínculo do aplicativo foi alterado na produção destes dois lotes. Alguns validadores e filas históricos contêm contagens antigas; preferir os controles atuais indicados acima.
