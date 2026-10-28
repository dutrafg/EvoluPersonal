# Associação de GIFs aos exercícios MD500

Atualização de 28/10/2026, branch codex/evolupersonal-media-350.

- 50 GIFs já armazenados no GitHub foram associados aos números MD correspondentes, sem recriar ou duplicar os arquivos.
- A galeria, os filtros, o visualizador e as bases locais antigas reconhecem os novos caminhos assets/md500-3d/.
- Os 50 novos vínculos são identificados como em revisão. O filtro GIFs em revisão reúne esses 50 e MD357/e141.
- MD357 reutiliza e141, cuja ficha de produção descreve rosca em banco inclinado com braços atrás do tronco. A revisão final dessa equivalência continua pendente.
- MD16 passa a usar e402 (versão deitada/horizontal), em vez de e400 (versão sentada/vertical).
- Resultado cadastral: 346 exercícios vinculados, 154 sem GIF, 51 vínculos para revisão final.
- GIFs 2D reprovados permanecem desativados. Nenhuma aprovação biomecânica foi presumida.

## Verificação

Os caminhos de todos os 346 vínculos foram confrontados com a árvore real do repositório. O inventário registra os SHAs dos arquivos existentes. Os testes executam o JavaScript do aplicativo e verificam os 50 vínculos, visualização, filtros, paginação, atualização da base antiga sem perda de alunos/treinos e consistência entre HTML, inventário, tabela e fila.

Resultados: 41 verificações de base/persistência; 17 do método de treino; testes de mídia; testes da galeria; validador de cobertura com 500 linhas, 346 vínculos, 154 pendentes e 51 em revisão.

A main não foi alterada. Não houve criação de novos GIFs nesta atualização; foram corrigidas e registradas as associações dos arquivos já produzidos.

