# Backup do catálogo

Repositório: `dutrafg/EvoluPersonal`.

Branch de backup: `codex/evolupersonal-media-350`. O nome é histórico; o catálogo atual tem 425 GIFs. A branch `main` não recebe estas alterações.

Os lotes 1 a 14 tiveram o envio dos GIFs completado, e os lotes 15 e 16 foram preservados. O lote 17 acrescenta os GIFs e400–e424, suas 25 folhas originais de seis poses, instruções e vínculos com a lista MD. Os arquivos de referência e metadados disponíveis também fazem parte deste checkpoint.

Para restaurar a aplicação, obtenha esta branch e sirva a pasta `dist/` inteira. Mantenha `index.html`, `training-methods.js` e `assets/exercises/` nas posições originais. O HTML não incorpora os GIFs.

`production/backup-manifest.json` registra os hashes dos arquivos. `production/lote17-validation.json` contém a validação dos 25 GIFs novos. Os dados pessoais gravados no navegador são independentes deste backup de código e mídia.

Validação: `node tests.cjs`, `node tests-methods.cjs` e `node tests-media.cjs`.
