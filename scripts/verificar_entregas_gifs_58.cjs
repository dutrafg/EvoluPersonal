'use strict';
// Validação de entregáveis finais — sem gerar ou associar GIFs automaticamente.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const queue = JSON.parse(fs.readFileSync(path.join(root, 'production/FILA_PRODUCAO_3D_MD500.json'), 'utf8'));
const ids = queue.items.map(x => x.md_id);
const errors = [];
const hashes = new Map();
let ready = 0;
if (ids.length !== 58 || new Set(ids).size !== 58) errors.push('A fila deve conter 58 IDs únicos.');
for (const id of ids) {
  const file = path.join(root, 'production/renderizados-md500', 'MD' + id + '.gif');
  if (!fs.existsSync(file)) { errors.push('Ausente: MD' + id); continue; }
  const b = fs.readFileSync(file);
  if (b.length < 32 || !['GIF87a', 'GIF89a'].includes(b.toString('ascii', 0, 6))) {
    errors.push('Formato GIF inválido: MD' + id); continue;
  }
  const w = b.readUInt16LE(6), h = b.readUInt16LE(8);
  if (w < 400 || h < 400) errors.push('Resolução abaixo de 400x400: MD' + id + ' (' + w + 'x' + h + ')');
  const hash = crypto.createHash('sha256').update(b).digest('hex');
  if (hashes.has(hash)) errors.push('GIFs idênticos: MD' + hashes.get(hash) + ' e MD' + id);
  hashes.set(hash, id);
  ready++;
}
console.log(JSON.stringify({expected:58,files_present:ready,missing:58-ready,distinct_hashes:hashes.size,errors},null,2));
if (errors.length) process.exitCode=1;
// AVISO: validação de frames, fidelidade anatômica e aprovação visual são controles separados.
// Um arquivo sintaticamente válido NÃO equivale a animação concluída.
