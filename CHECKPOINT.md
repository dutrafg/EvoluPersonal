# Ponto de continuidade — EvoluPersonal / MD500

Data: 28/10/2026.

- Fonte única do catálogo: `500 Exercícios Base de Musculação.md`.
- Biblioteca visível no app: **500 exercícios, exatamente os nomes e a ordem do MD**.
- GIFs associados a entradas do MD: **295** (inclui quatro correspondências adicionais verificadas do acervo legado; lote 2D reprovado não contabilizado).
- Exercícios ainda sem GIF específico: **205**.
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

## Biblioteca Imagem 2 — integração validada

- Interface dark navy/azul: **5 cards por linha** em desktop grande e adaptação responsiva; escopo de estilos limitado à Biblioteca.
- Busca + filtros de grupo, **GIF vinculado / pendente / lote atual de 25**; páginas de **50** com navegação.
- **295** exercícios MD com GIF legado vinculado (cadastral; requer QA anatômico integral) e **205** pendentes.
- Lote `MD500-25-01`: **25 itens com 150 poses descritas**, **0/25 GIFs novos aprovados**.
- Testes da interface: `tests-gallery.cjs` executado com resultado PASS.
- O gerador de imagens devolveu pôsteres de catálogo, **não** folhas válidas de seis poses: nenhuma dessas imagens foi adicionada ao catálogo ou considerada GIF.
- Continuar a produção **por exercício** e salvar no GitHub cada lote com 25 GIFs realmente verificados; preservar `main`.


## Lote de 25 — arquivos animados produzidos

- 25 GIFs novos de IDs MD distintos em `dist/assets/md500-3d/`.
- Inventário, auditoria, prompts, revisão e próxima fila em `production/md500-lote25-3d/`.
- Estado: produzidos para revisão final; **não integrados à cobertura do aplicativo**. O total vinculado continua 295.
- MD357/e141 foi excluído da criação para evitar repetição. Seis tentativas com falhas foram substituídas por outros pendentes; seus IDs permanecem na fila.
- `proxima-fila.json`: 179 entradas para produção posterior, sem repetir os 25 já produzidos nem MD357/e141.
- A `main` permanece intacta. Consultar `production/md500-lote25-3d/README.md` antes de continuar.
