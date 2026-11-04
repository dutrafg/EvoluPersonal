# EvoluPersonal — Alpha 0.9 · Biblioteca MD500

Aplicativo separado para personal trainer, com identidade visual inspirada no EvoluFísico2. O nome é provisório.

## Funcionalidades disponíveis

- Início com contadores reais da base e alunos sem treino.
- Cadastro, edição, pesquisa e perfil de alunos.
- Prescrição, edição, duplicação e exclusão de treinos.
- Ordem de exercícios e séries individuais: aquecimento, feeder, trabalho, principal e back-off.
- Percentuais sobre carga base ou série anterior, carga não definida e unidade por equipamento.
- Descanso antes de cada série, RIR alvo/realizado, GIF na execução e histórico de séries.
- Sugestões de progressão por todas as séries de trabalho ou pela principal, sem alterar cargas automaticamente.
- Migração de backups e bases versão 1 para versão 2 sem excluir registros; mudança para catálogo MD500 preserva as referências históricas de treinos antigos e cria cópia local antes da adaptação.
- Biblioteca oficial com os **500 exercícios do arquivo `500 Exercícios Base de Musculação.md`**, na mesma ordem e com os nomes originais. **445 com GIF vinculado** (296 legados e 149 novos GIFs 3D), **55 sem GIF**. Desses 445 vínculos, são **442 arquivos distintos**, pois três GIFs são compartilhados por dois exercícios. **58 tarefas** para obter uma animação exclusiva em cada exercício (55 ausentes + 3 substituições condicionais). Os 30 GIFs 2D reprovados continuam excluídos.
- Prévia local da área do aluno: carga e repetições por série, marcação de conclusão, cronômetro, esforço e feedback.
- Histórico de sessões com cópia dos registros na conclusão.
- Persistência no navegador, exportação e restauração de backup JSON com validação.
- Tema claro e escuro e layout responsivo.

## Limites desta Alpha

Não há autenticação individual, sincronização entre personal e aluno, envio de mensagens, cobranças, agenda ou módulo de avaliações. O seletor de aluno é uma ferramenta de demonstração local. O site está publicado com acesso privado do proprietário. Dados de uso não são enviados a um servidor pela aplicação: ficam no localStorage da origem e do perfil do navegador. Abrir o HTML avulso e abrir o site são bases distintas. Manter backups e testar apenas com dados de demonstração nesta fase.

## Executar

A entrada está em `dist/index.html`. Não há dependências ou build. Pode ser servida por qualquer servidor estático. Mantenha `training-methods.js`, `assets/exercises/` e `assets/md500/` junto ao HTML. A persistência depende do armazenamento do navegador.

## Verificação da Alpha 0.2

`node tests.cjs` e `node tests-methods.cjs`: 47 verificações passaram, incluindo migração, referências, carga em branco, percentuais, back-off, critérios de progressão e preservação de histórico. A validação visual desta versão ainda está pendente; o Chromium local não está instalado.

### Verificações da Alpha anterior

`node tests.cjs` executa 30 verificações: esquema de backup, relações de alunos e exercícios, limites numéricos, sessões, identificadores, links inseguros, escape HTML, persistência, pesquisas, filtro e tema.

Testes de navegador realizados na prévia: cadastro de aluno; treino com duas séries; atribuição; alteração de carga e repetições; bloqueio de conclusão incompleta; descanso e pausa; conclusão com feedback; histórico após recarregar; pesquisa da biblioteca e filtro combinado; visual desktop nos temas claro e escuro. Responsividade móvel definida por CSS, ainda sem teste em aparelho Android real. Exportação/restauração de arquivos tem validação de dados automatizada; o ciclo de download/upload não foi testado em aparelho real.

## Próxima etapa

Contas e permissões por aluno, banco de dados e sincronização entre aparelhos. Depois, ampliar avaliações, acompanhamento, agenda e mensalidades.

## Lote 17

25 variações da lista MD adicionadas com GIFs originais e IDs e400–e424. Total: 425 GIFs. As 500 linhas da referência não equivalem à contagem do catálogo, que inclui variações e sinônimos anteriores.


## Biblioteca original MD500 — lote 01 de 30

- Fonte: `500 Exercícios Base de Musculação.md`; **não cadastrar exercícios externos** na biblioteca oficial.
- Contagem atual: **500 itens oficiais; 295 com GIF vinculado; 205 ainda sem GIF aprovado**. O catálogo anterior de 425 GIFs permanece como acervo de apoio/histórico; não equivale a 425 itens do MD.
- Primeiro lote de 30 GIFs em `dist/assets/md500/md<ID>.gif`: **REPROVADO** por apresentar bonecos esquemáticos 2D. Arquivos preservados apenas para auditoria, sem vinculação no aplicativo.
- Formato técnico do lote: 144 × 144, 10 quadros, GIF89a, destaque muscular alaranjado. **O padrão obrigatório é anatômico 3D com roupa de compressão cinza, musculatura ativa em laranja, equipamento correto e seis poses por ciclo.**
- A nova fila em `production/FILA_PRIORIDADE_COBERTURA_MD500.json` contém 205 exercícios, com o próximo grupo de 25 definido.
- Validação: `node scripts/validar_cobertura_500.cjs`; testes do aplicativo `node tests.cjs` e `node tests-methods.cjs`.
- O site privado não foi atualizado por este commit. A branch de desenvolvimento é `codex/evolupersonal-media-350`; `main` não foi alterada.

### Reprovação do lote MD500-01

Em 28/10/2026, a amostra de bonecos 2D foi rejeitada. Os 30 arquivos estão preservados no histórico Git, mas desativados em `dist/index.html`. A contagem oficial foi restaurada de 314 para **284 correspondências**, com **216 itens ainda pendentes**. Não recomeçar a produção em 2D ou reutilizar os movimentos genéricos. Qualquer próxima prévia é conceitual até ser gerado e validado um GIF anatômico 3D real.


## Nova cadência de produção — 25 por lote

- Lote de trabalho `production/lote-md500-25-01.json`: 25 exercícios originais do MD, seis poses técnicas por exercício (150 posições) em planejamento; **nenhum novo GIF 3D deste lote foi aprovado**.
- Quatro correspondências preexistentes aproveitadas por inspeção: MD85→e165, MD131→e299, MD132→e300 e MD172→e259. Cobertura documental atual **295/500**; pendências **205**.
- Compositor de sprites aprovados em `scripts/montar_gif_3d.py`; saída de rascunho em `production/previews-md500-3d/`; entrega definitiva em `dist/assets/md500-3d/`.
- Verificador `scripts/validar_lote_25.cjs` exige 25 assets diferentes, GIFs ≥400 px e validação de QA registrada antes de declarar o lote concluído. A análise da fidelidade anatômica é uma etapa humana independente.
- Preservar `main`, preparar um commit com **25 GIFs aprovados de uma só vez**, sem reutilizar o material 2D reprovado.


## Biblioteca no visual da imagem 2 — implementação

O módulo **Biblioteca** em `dist/index.html` agora utiliza o layout escuro azul-marinho da imagem 2, com até cinco cards por linha no desktop, redução responsiva em tablet e celular, pesquisa, filtros por grupo e status, paginação de 50 itens e filtro dedicado ao lote atual de 25. A aparência não altera os demais módulos, nem insere exercícios fora da lista MD original.

Cada card utiliza **um GIF real já vinculado** ao MD ou a indicação explícita **“GIF 3D pendente”**. Nenhuma montagem de pôster e nenhum GIF 2D reprovado foi integrado. Em 28/10/2026: **295/500 GIFs vinculados** (ainda sujeitos à revisão biomecânica) e **205** pendentes; novo lote `MD500-25-01` ainda com **0/25 GIFs 3D gerados e aprovados**.

Regressão de interface: `node tests-gallery.cjs` (fonte MD500, contagens, 25 itens no lote, GIFs verdadeiros, busca, filtros, paginação e CSS responsivo). Os testes passaram em execução isolada do JavaScript da aplicação.

## Auditoria e pendências MD500 (29/10/2026)

Aprovação visual relatada para 15 vínculos legados, preservando alerta para três pares de GIFs repetidos. A biblioteca não está concluída até resolver GIFs ausentes e vínculos compartilhados. Consulte `production/PLANO_GIFS_3D_PENDENTES.md` e `production/FILA_PRODUCAO_3D_MD500.json`.
