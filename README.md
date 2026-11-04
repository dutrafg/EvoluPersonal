# OpenGym Personal PWA — fase 4

Pacote estático e instalável baseado na prévia interativa da fase 4. Inclui manifesto, ícones, cache offline e configuração de cabeçalhos para Vercel. Não requer dependências nem etapa de build.

## Publicar pela Vercel

1. Importe `dutrafg/EvoluPersonal` na Vercel.
2. Em **Root Directory**, selecione `opengym-pwa`.
3. Use preset **Other**; deixe build command e output directory vazios ou configure output `.`.
4. Publique. A raiz desse diretório contém `index.html`.
5. Abra o domínio em HTTPS no Chrome/Edge e escolha **Instalar OpenGym** ou **Adicionar à tela inicial**.

O service worker salva a interface e os ícones no primeiro acesso. Depois disso, a navegação principal abre offline. Para atualizar o cache em uma versão futura, aumente `CACHE_NAME` em `sw.js`; a ativação remove somente caches antigos com o prefixo deste PWA.

## Dados

Este é um protótipo local: registros ficam no `localStorage` deste navegador e origem, sem sincronização, autenticação real ou envio a servidor. Instalar noutro aparelho cria uma base separada. Use apenas dados fictícios até existir backend e autenticação.
