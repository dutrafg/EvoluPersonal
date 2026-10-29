# Auditoria remota — 29/10/2026

## Resultado

**Biblioteca MD500 não aprovada.** A contagem de arquivos vinculados é uma contagem administrativa, não a contagem de animações validadas.

- 500 exercícios oficiais cadastrados.
- 445 com caminho de GIF no inventário; 55 sem GIF.
- 442 referências de GIF distintas em uso; três reutilizações exatas (MD135/341, MD140/340, MD301/302).
- 149 vínculos rotulados `vinculado_3d` no inventário.
- **148 desses 149 arquivos foram consultados individualmente no GitHub e apresentam 144×144 px.** Seus SHA de arquivo correspondem ao inventário. Logo, **148 falham o critério vigente de resolução mínima 400×400**.
- **MD373 (1/149) permanece sem tamanho comprovado pela inspeção remota:** o conector retornou o SHA `89147e8023ba7dc6dc00a4fd35be43bef32dd898` e conteúdo vazio. Isso não prova que o arquivo esteja vazio; pode ser limitação da API para conteúdo binário grande. Inspecionar pelo checkout integral/CI.
- A amostra visual realizada no MD23 mostra uma figura digital com aspecto 3D. Isso não constitui validação biomecânica do movimento nem dos 149 GIFs.
- O relatório `production/INVENTARIO_MD500.json` registra 155 vínculos com revisão de mídia pendente, incluindo novos GIFs e duplicações.

## Impacto no escopo

A fila de **58 tarefas** cobre apenas 55 GIFs ausentes e três substituições de GIFs compartilhados. Ela não resolve a qualidade dos GIFs já associados.

Se o padrão mínimo de **400×400 pixels** continuar obrigatório, é necessário corrigir **pelo menos 206 entregas de mídia**:

- 55 animações ausentes;
- 3 variantes com compartilhamento de GIF, sujeitas à revisão e possível substituição;
- 148 GIFs novos com resolução insuficiente.

O total poderá ser **207 ou superior** depois de verificar a resolução do MD373 e a fidelidade biomecânica dos outros 296 vínculos legados. Não aumentar artificialmente a contagem de GIFs nem fazer upscale de 144 para 400: redimensionar não cria detalhe anatômico.

## O que foi concluído de fato

1. Verificação documental de 500 IDs e da fila de 58 itens.
2. Auditoria remota dos cabeçalhos e SHA dos 149 arquivos rotulados como novos, exceto leitura binária limitada do MD373.
3. Scripts para auditoria integral do checkout, verificação de entregas e CI.
4. Página HTML para revisar visualmente todos os 500, registrar decisão local e exportar JSON.
5. Nenhuma nova animação anatômica 3D foi gerada, aprovada ou associada nesta etapa.

## Regras para fechamento

- Gerar novos renders 3D do movimento correto, a no mínimo 400×400 px (não usar 2D ou aumentar artificialmente a imagem).
- Validar no mínimo seis poses com variação real; validar equipamentos, trajetórias, apoios, pegadas e amplitude com um revisor.
- Evitar a reutilização de GIFs em variantes que exigem movimentos diferentes.
- Executar `node scripts/auditar_md500_integral.cjs --write` e `node scripts/verificar_entregas_gifs_58.cjs` sobre o checkout contendo todos os GIFs.
- A **aprovação final é independente** da passagem de testes de arquivos. Ausência de revisão visual impede a certificação.
- Não alterar `main` até que todos os critérios estejam atendidos.
