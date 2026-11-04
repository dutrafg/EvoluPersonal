# Publicar EvoluPersonal na Vercel

1. Importe o repositório `dutrafg/EvoluPersonal` e selecione a branch de integração aprovada.
2. Defina **Root Directory** como `dist`.
3. Use preset **Other**, sem comando de build e com saída `.`.
4. Publique em HTTPS e abra o endereço no Chrome/Edge para instalar o PWA.

`index.html`, manifesto, ícones, service worker e biblioteca de exercícios ficam no mesmo diretório. O service worker salva a interface no primeiro acesso; a biblioteca de imagens é baixada pelo controle offline do aplicativo. Para publicar atualizações futuras, incremente o nome do cache em `sw.js`.

Os dados de alunos e avaliações permanecem no navegador. Esta versão não sincroniza dados entre aparelhos nem oferece autenticação de contas.
