# EvoluPersonal — padrão visual selecionado: imagem 2

**Decisão visual (28/10/2026):** o usuário preferiu a **segunda imagem** do comparativo de duas grades com 50 exercícios. Esta imagem é uma **referência de layout e acabamento**, não prova de existência de 50 GIFs produzidos/aprovados.

## Identidade e interface

- Fundo escuro **azul-marinho quase preto**, com cards compactos, bordas discretas azuladas, cantos arredondados e separação constante.
- Nome **EvoluPersonal** com destaque laranja na parte “Personal”; organização em catálogo de exercícios.
- Cada card exibe **um exercício canônico da lista MD**, nome legível em português, grupo muscular e demonstração dedicada.
- Layout de referência: **5 colunas em desktop largo**; adaptar para menos colunas em tablet e celular, sem achatar ou recortar o personagem.
- Realçar anatomia e equipamento; evitar ícones chamativos e excesso de textos que compitam com a demonstração.
- Usar a grade de 50 cards apenas como **visão de catálogo**; cada GIF é **um arquivo separado** vinculado a um único ID do MD (nunca uma única imagem contendo todos os exercícios).

## Padrão obrigatório dos recursos visuais

- Personagem humano com anatomia detalhada, iluminação e volume **3D realista**, coerente com a biblioteca legada de GIFs anatômicos.
- Roupa esportiva/ compressão **cinza-escuro**; músculos principais trabalhados em **laranja**, com precisão anatômica.
- Equipamento realista, pegada, apoios, amplitude, posição inicial e final corretamente representados.
- **Mesmo personagem, câmera, equipamento e escala entre os quadros** de um mesmo GIF, sem mudança abrupta de identidade, tamanho ou fundo.
- Fundo da renderização limpo e neutro para favorecer a leitura, mesmo dentro do card escuro.
- **Seis poses específicas** do movimento por GIF, loop contínuo, com revisão de biomecânica e continuidade; priorizar resolução mínima de 448 × 448 pixels.
- Não reutilizar bonecos 2D esquemáticos, nem imagens estáticas de um infográfico rotuladas como GIFs funcionais.

## Fluxo de entrega

1. Selecionar apenas exercícios entre os 500 itens do `500 Exercícios Base de Musculação.md`.
2. Produzir cada exercício **individualmente** com sua própria sequência de seis poses.
3. Validar equipamento e anatomia em cada quadro, transições, GIF decodificável, resolução e identidade visual.
4. Revisar a aparência no catálogo com este estilo, separadamente do teste do GIF.
5. Publicar no GitHub **a cada 25 GIFs concluídos e validados**, na branch `codex/evolupersonal-media-350`. Não modificar `main` sem autorização.

## Status verdadeiro na seleção da referência

- **295 / 500** itens do MD tinham correspondência de GIF legada registrada, sujeita à revisão visual completa.
- **205** itens permaneciam sem GIF correspondente.
- O lote `MD500-25-01` estava **em desenvolvimento com zero novos GIFs 3D aprovados**.
- Os pôsteres gerados por imagem são **mockups de estilo** e não atualizam esta contagem nem autorizam a legenda “50 aprovados” na interface real.

**Regra editorial:** títulos e indicadores devem refletir sempre os GIFs realmente integrados e aprovados, nunca os cartões ilustrativos do conceito.
