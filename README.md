# EvoluPersonal — Alpha 0.2

Aplicativo separado para personal trainer, com identidade visual inspirada no EvoluFísico2. O nome é provisório.

## Funcionalidades disponíveis

- Início com contadores reais da base e alunos sem treino.
- Cadastro, edição, pesquisa e perfil de alunos.
- Prescrição, edição, duplicação e exclusão de treinos.
- Ordem de exercícios e séries individuais: aquecimento, feeder, trabalho, principal e back-off.
- Percentuais sobre carga base ou série anterior, carga não definida e unidade por equipamento.
- Descanso antes de cada série, RIR alvo/realizado, GIF na execução e histórico de séries.
- Sugestões de progressão por todas as séries de trabalho ou pela principal, sem alterar cargas automaticamente.
- Migração de backups e bases versão 1 para versão 2 sem excluir registros.
- Biblioteca com 100 exercícios e GIFs originais em loop, destaque muscular em laranja e instruções em português brasileiro; cadastro e edição de exercícios próprios e links externos de demonstração.
- Prévia local da área do aluno: carga e repetições por série, marcação de conclusão, cronômetro, esforço e feedback.
- Histórico de sessões com cópia dos registros na conclusão.
- Persistência no navegador, exportação e restauração de backup JSON com validação.
- Tema claro e escuro e layout responsivo.

## Limites desta Alpha

Não há autenticação individual, sincronização entre personal e aluno, envio de mensagens, cobranças, agenda ou módulo de avaliações. O seletor de aluno é uma ferramenta de demonstração local. O site está publicado com acesso privado do proprietário. Dados de uso não são enviados a um servidor pela aplicação: ficam no localStorage da origem e do perfil do navegador. Abrir o HTML avulso e abrir o site são bases distintas. Manter backups e testar apenas com dados de demonstração nesta fase.

## Executar

A entrada está em `dist/index.html`. Não há dependências ou build. Pode ser servida por qualquer servidor estático. Mantenha `training-methods.js` e a pasta de GIFs junto ao HTML. A persistência depende do armazenamento do navegador.

## Verificação da Alpha 0.2

`node tests.cjs` e `node tests-methods.cjs`: 47 verificações passaram, incluindo migração, referências, carga em branco, percentuais, back-off, critérios de progressão e preservação de histórico. A validação visual desta versão ainda está pendente; o Chromium local não está instalado.

### Verificações da Alpha anterior

`node tests.cjs` executa 30 verificações: esquema de backup, relações de alunos e exercícios, limites numéricos, sessões, identificadores, links inseguros, escape HTML, persistência, pesquisas, filtro e tema.

Testes de navegador realizados na prévia: cadastro de aluno; treino com duas séries; atribuição; alteração de carga e repetições; bloqueio de conclusão incompleta; descanso e pausa; conclusão com feedback; histórico após recarregar; pesquisa da biblioteca e filtro combinado; visual desktop nos temas claro e escuro. Responsividade móvel definida por CSS, ainda sem teste em aparelho Android real. Exportação/restauração de arquivos tem validação de dados automatizada; o ciclo de download/upload não foi testado em aparelho real.

## Próxima etapa

Contas e permissões por aluno, banco de dados e sincronização entre aparelhos. Depois, ampliar avaliações, acompanhamento, agenda e mensalidades.
