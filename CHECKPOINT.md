# Ponto de continuidade — EvoluPersonal / MD500

Data: 28/10/2026.

- Fonte única do catálogo: `500 Exercícios Base de Musculação.md`.
- Biblioteca visível no app: **500 exercícios, exatamente os nomes e a ordem do MD**.
- GIFs associados a entradas do MD: **288** (inclui quatro correspondências adicionais verificadas do acervo legado; lote 2D reprovado não contabilizado).
- Exercícios ainda sem GIF específico: **212**.
- O repositório retém 425 GIFs legados para histórico; mídias antigas não correspondentes ao MD não aparecem como exercícios extras na interface.
- Lote MD500-01: `production/lote-md500-01.json`; 30 GIFs 2D reprovados, arquivos preservados somente para histórico.
- Gerador reprodutível: `scripts/gerar-animacoes-md.cjs`.
- Próximo lote de 30: `production/FILA_PRIORIDADE_COBERTURA_MD500.json`.
- QA: `scripts/validar_cobertura_500.cjs`. Os GIFs foram decodificados tecnicamente; validação de estética/biomecânica pendente. O lote 2D foi rejeitado e não integra a biblioteca oficial.
- Atualizar **somente a branch de trabalho**, com um commit de mídia a cada 30 exercícios. `main` não foi alterada.

## Publicação

Site privado anterior: https://evolupersonal-alpha-dutra.chirpyzebra12.chatgpt.site

Este checkpoint representa o **repositório de desenvolvimento**, não garante atualização do site privado.

## Padrão visual obrigatório

Modelo anatômico de aspecto 3D, roupa de compressão cinza, músculos ativos destacados em laranja, mesmo personagem e câmera, equipamento correto e seis poses coerentes em loop. Somente contar novos GIFs após validação visual. Permanecem **216 pendentes** e o lote reprovado não reduz essa contagem.

## Continuidade em lotes de 25

- Próxima etapa `production/lote-md500-25-01.json`: **25 exercícios e 150 poses técnicas** com animação ainda pendente de geração/QA.
- Padrão de exportação `scripts/montar_gif_3d.py`; validadores `scripts/validar_lote_25.cjs` e `scripts/validar_cobertura_500.cjs`.
- A produção anterior de 30 bonecos 2D permanece reprovada; não subir como GIF aprovado.
