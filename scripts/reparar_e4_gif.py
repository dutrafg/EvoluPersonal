#!/usr/bin/env python3
"""Repara e4.gif: o GIF antigo continha dois quadros empilhados em CADA frame.

Preserva o original em production/legacy-originals/e4-stacked-original.gif.
Monta uma sequência em que somente UMA posição de supino aparece por quadro.
Não confundir esta correção de layout de mídia com aprovação biomecânica final.
"""
from pathlib import Path
import hashlib
import io
import json
from PIL import Image, ImageChops, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "dist/assets/exercises/e4.gif"
ORIGINAL = ROOT / "production/legacy-originals/e4-stacked-original.gif"
BACKUP_SHA = "1e879245c8d6e764c2c88d74b5178ed1e40bf3af"
def gitsha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

original = ORIGINAL.read_bytes() if ORIGINAL.exists() else PATH.read_bytes()
if gitsha(original) != BACKUP_SHA:
    raise SystemExit("O GIF original não corresponde ao SHA conhecido; inspeção manual necessária.")
ORIGINAL.parent.mkdir(parents=True, exist_ok=True)
if not ORIGINAL.exists():
    ORIGINAL.write_bytes(original)

source = Image.open(io.BytesIO(original))
frames = [f.convert("RGB") for f in ImageSequence.Iterator(source)]
if len(frames) != 6 or frames[0].size != (448, 448):
    raise SystemExit("Layout inesperado. Não é seguro recortar automaticamente.")
# O arquivo histórico possui uma faixa divisória na metade: duas fotografias
# do mesmo exercício empilhadas verticalmente em todos os seis frames.
def isolate(frame, top):
    if top:
        return frame.crop((0, 0, 448, 218))
    return frame.crop((0, 230, 448, 448))
# Alternar posição alta/baixa para obter uma animação real de UMA cena por quadro.
# Mantemos seis posições do arquivo original, sem misturar os dois painéis.
selected = [(0, True), (1, True), (2, False),
            (3, False), (4, True), (5, True)]
pictures = [isolate(frames[i], upper) for i, upper in selected]
if len({p.tobytes() for p in pictures}) < 2:
    raise SystemExit("Os quadros são idênticos; não há animação válida.")

# Salvar GIF retangular (448x218): somente UMA vista por quadro, sem divisor.
pictures[0].save(
    PATH, format="GIF", save_all=True, append_images=pictures[1:],
    duration=[220, 220, 420, 250, 220, 220],
    loop=0, disposal=2, optimize=False)
result = PATH.read_bytes()
new_image = Image.open(io.BytesIO(result))
assert new_image.size == (448, 218)
assert getattr(new_image, "n_frames", 1) >= 2
assert gitsha(result) != BACKUP_SHA
assert result[:6] in (b"GIF87a", b"GIF89a")
sha = gitsha(result)
for path in ["production/INVENTARIO_MD500.json",
             "production/REVISAO_CORRESPONDENCIAS_MD500.json",
             "production/VALIDACAO_LEGADO_296.json"]:
    p = ROOT / path
    data = json.loads(p.read_text(encoding="utf-8"))
    if path.endswith("INVENTARIO_MD500.json"):
        item = data[0]
        assert item["id"] == 1 and item["ref"] == "e4"
        item["gif_blob_sha"] = sha
    elif path.endswith("REVISAO_CORRESPONDENCIAS_MD500.json"):
        item = next(row for row in data["items"] if row["md_id"] == 1)
        assert item["media_ref"] == "e4"
        item["gif_blob_sha"] = sha
    else:
        item = next(row for row in data["records"] if row["md_id"] == 1)
        assert item["media_ref"] == "e4"
        item["git_blob_sha"] = sha
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",encoding="utf-8")

# A galeria de auditoria é autônoma e mantém SHA no JSON incorporado.
gallery = ROOT / "dist/revisao-vinculos-md500.html"
html = gallery.read_text(encoding="utf-8")
assert html.count(BACKUP_SHA) >= 1
html = html.replace(BACKUP_SHA, sha)
gallery.write_text(html, encoding="utf-8")
print(json.dumps({"md_id":1,"ref":"e4","new_sha":sha,
                  "old_frames":len(frames),"new_frames":new_image.n_frames,
                  "old_size":[448,448],"new_size":list(new_image.size),
                  "bytes":len(result),"original_preserved":str(ORIGINAL.relative_to(ROOT))},indent=2))
