"""Decode every linked GIF and staged preview. Never grants visual approval."""
import hashlib
import json
import os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa-md500'
OUT.mkdir(exist_ok=True)
inventory = json.loads((ROOT / 'production/INVENTARIO_MD500.json').read_text())
assert len(inventory) == 500 and [r['id'] for r in inventory] == list(range(1, 501))
comparison = json.loads((ROOT / 'docs/COMPARACAO_LISTA_500.json').read_text())['items']
assert len(comparison) == 500
cache = {}
errors = []

def inspect(relative, expected_sha=None, expected_size=None, expected_sha256=None, expected_frames=None):
    if relative not in cache:
        try:
            p = ROOT / relative
            data = p.read_bytes()
            assert data[:6] in (b'GIF87a', b'GIF89a'), 'invalid GIF header'
            sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            frame_hashes = set()
            duration = 0
            with Image.open(p) as im:
                assert im.format == 'GIF'
                width, height = im.size
                frames = im.n_frames
                assert width > 0 and height > 0 and frames >= 2, 'not an animation'
                for n in range(frames):
                    im.seek(n)
                    pixels = im.convert('RGB')
                    pixels.load()
                    frame_hashes.add(hashlib.sha256(pixels.tobytes()).hexdigest())
                    duration += im.info.get('duration', 0)
            assert len(frame_hashes) > 1, 'all rendered frames identical'
            assert duration > 0, 'animation has no positive duration'
            cache[relative] = dict(path=relative, ok=True, git_blob_sha=sha,
                sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), frames=frames,
                width=width, height=height, distinct_frames=len(frame_hashes), duration_ms=duration)
        except Exception as exc:
            cache[relative] = dict(path=relative, ok=False, error=str(exc))
    result = dict(cache[relative])
    if result['ok']:
        checks = [(expected_sha, result['git_blob_sha'], 'Git SHA'),
                  (expected_size, result['bytes'], 'size'),
                  (expected_sha256, result['sha256'], 'SHA256'),
                  (expected_frames, result['frames'], 'frame count')]
        for expected, actual, label in checks:
            if expected is not None and expected != actual:
                result.update(ok=False, error=f'{label} mismatch: {actual} != {expected}')
    if not result['ok']:
        errors.append(result)
    return result

previews = {}
for manifest in sorted((ROOT / 'production/revisoes-md500-3d').glob('bloco*/manifest.json')):
    for entry in json.loads(manifest.read_text()):
        mid = entry['id']
        assert mid not in previews, f'duplicate preview MD{mid}'
        assert not inventory[mid-1]['animation_path'], f'preview would replace linked MD{mid}'
        gif = manifest.parent / f'md{mid}.gif'
        previews[mid] = inspect(str(gif.relative_to(ROOT)), expected_size=entry['size_bytes'],
            expected_sha256=entry['sha256'], expected_frames=entry['frames'])

items = []
for row, doc in zip(inventory, comparison):
    assert row['id'] == doc['list_id'] and row['name'] == doc['name']
    assert row['animation_path'] == doc['animation_path']
    item = dict(id=row['id'], name=row['name'], official_path=row['animation_path'],
                visual_status=row.get('review_status'), preview=previews.get(row['id']))
    if row['animation_path']:
        assert not row['animation_path'].startswith('assets/md500/'), 'rejected 2D media'
        item['technical'] = inspect('dist/' + row['animation_path'], expected_sha=row['gif_blob_sha'])
    else:
        item['technical'] = None
    items.append(item)

groups = {}
for item in items:
    if item['technical'] and item['technical']['ok']:
        groups.setdefault(item['technical']['sha256'], []).append(item['id'])
duplicates = [ids for ids in groups.values() if len(ids) > 1]
linked = [i for i in items if i['official_path']]
unlinked = [i['id'] for i in items if not i['official_path']]
no_preview = [mid for mid in unlinked if mid not in previews]
report = dict(source_commit=os.environ.get('GITHUB_SHA'), exercises=500,
    linked=len(linked), official_unlinked_ids=unlinked, staged_previews=len(previews),
    no_official_or_preview_ids=no_preview, duplicate_binary_groups=duplicates,
    decoded_unique_files=len(cache), technical_errors=errors,
    visual_approval_claimed=False, complete=False, items=items)
(OUT / 'validacao-integral.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
summary = f'''# Auditoria integral MD500

Commit auditado: {report['source_commit']}

- Exercícios: 500.
- Vínculos oficiais: {len(linked)}; sem vínculo oficial: {len(unlinked)}.
- Prévias separadas: {len(previews)}; IDs sem oficial nem prévia: {no_preview}.
- Arquivos únicos decodificados: {len(cache)}.
- Erros técnicos: {len(errors)}.
- Grupos com binário idêntico: {duplicates}.

Cada arquivo foi aberto, todos os quadros foram decodificados, e foram conferidos
cabeçalho, duração, dimensões, variação entre quadros e hashes de referência.
Os nomes e IDs foram comparados com o documento de correspondências.
Uma animação que passa nesses testes ainda pode representar o movimento errado.
Este resultado não aprova anatomia, trajetória, pegada ou equipamento.
As prévias continuam fora do catálogo oficial. A biblioteca não está homologada.
'''
(OUT / 'RELATORIO.md').write_text(summary)
print(summary)
assert not errors, f'{len(errors)} technical errors; inspect validacao-integral.json'
