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
- Biblioteca oficial com os **500 exercícios do arquivo `500 Exercícios Base de Musculação.md`**, na mesma ordem e com os nomes originais. **284 possuem GIF legado vinculado**; **216 aguardam animação específica**. O lote de 30 animações 2D criado anteriormente foi reprovado e não conta como cobertura.
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
- Contagem atual: **500 itens oficiais; 284 com GIF vinculado; 216 ainda sem GIF aprovado**. O catálogo anterior de 425 GIFs permanece como acervo de apoio/histórico; não equivale a 425 itens do MD.
- Primeiro lote de 30 GIFs em `dist/assets/md500/md<ID>.gif`: **REPROVADO** por apresentar bonecos esquemáticos 2D. Arquivos preservados apenas para auditoria, sem vinculação no aplicativo.
- Formato técnico do lote: 144 × 144, 10 quadros, GIF89a, destaque muscular alaranjado. **O padrão obrigatório é anatômico 3D com roupa de compressão cinza, musculatura ativa em laranja, equipamento correto e seis poses por ciclo.**
- A nova fila em `production/FILA_PRIORIDADE_COBERTURA_MD500.json` contém 216 exercícios, com o próximo grupo de 30 definido.
- Validação: `node scripts/validar_cobertura_500.cjs`; testes do aplicativo `node tests.cjs` e `node tests-methods.cjs`.
- O site privado não foi atualizado por este commit. A branch de desenvolvimento é `codex/evolupersonal-media-350`; `main` não foi alterada.

### Reprovação do lote MD500-01

Em 28/10/2026, a amostra de bonecos 2D foi rejeitada. Os 30 arquivos estão preservados no histórico Git, mas desativados em `dist/index.html`. A contagem oficial foi restaurada de 314 para **284 correspondências**, com **216 itens ainda pendentes**. Não recomeçar a produção em 2D ou reutilizar os movimentos genéricos. Qualquer próxima prévia é conceitual até ser gerado e validado um GIF anatômico 3D real.
