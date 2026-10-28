#!/usr/bin/env python3
"""Monta um GIF de 6 poses anatômicas 3D a partir de uma folha 3x2 aprovada.
Uso: python scripts/montar_gif_3d.py --id 292 --sheet trabalho/md292.png
A geração e o QA do render 3D são etapas ANTERIORES a este empacotador.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "production" / "lote-md500-25-01.json"
DRAFT_FOLDER = ROOT / "production" / "previews-md500-3d"
FINAL_FOLDER = ROOT / "dist" / "assets" / "md500-3d"

def validate_frames(frames, md_id):
    if len(frames) != 6:
        raise ValueError("São obrigatórias exatamente seis poses por exercício")
    if any(frame.width < 400 or frame.height < 400 for frame in frames):
        raise ValueError("Resolução insuficiente: cada quadro precisa ter pelo menos 400x400")
    if len({frame.size for frame in frames}) != 1:
        raise ValueError("Os quadros precisam compartilhar o mesmo enquadramento")
    for i in range(1, len(frames)):
        diff = ImageChops.difference(frames[i-1].convert("RGB"), frames[i].convert("RGB"))
        channel_means = ImageStat.Stat(diff).mean
        if sum(channel_means) < 1.5:
            raise ValueError(f"Poses {i} e {i+1} praticamente idênticas para MD{md_id}")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, dest="md_id")
    parser.add_argument("--sheet", type=Path, required=True)
    parser.add_argument("--approved", action="store_true", help="Somente após aprovação visual humana")
    parser.add_argument("--duration", type=int, default=150, help="Milissegundos por pose")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    item = next((x for x in manifest["items"] if x["md_id"] == args.md_id), None)
    if not item:
        raise SystemExit("Exercício não consta do lote de 25 do arquivo MD")
    if args.duration < 90 or args.duration > 500:
        raise SystemExit("Duração fora dos limites para GIF")
    if not args.sheet.is_file():
        raise SystemExit("Folha 3x2 não encontrada")
    sheet = Image.open(args.sheet).convert("RGB")
    if sheet.width % 3 or sheet.height % 2:
        raise SystemExit("Dimensões incompatíveis com grade 3x2")
    width, height = sheet.width // 3, sheet.height // 2
    frames = [
        sheet.crop((col*width, row*height, (col+1)*width, (row+1)*height))
        for row in range(2) for col in range(3)
    ]
    validate_frames(frames, args.md_id)
    output_folder = FINAL_FOLDER if args.approved else DRAFT_FOLDER
    output_folder.mkdir(parents=True, exist_ok=True)
    file = output_folder / f"md{args.md_id}.gif"
    # Converter os seis renders RGB, sem reutilizar qualquer GIF 2D reprovado.
    frames[0].save(
        file, format="GIF", save_all=True, append_images=frames[1:],
        duration=args.duration, loop=0, optimize=False, disposal=2
    )
    candidate = Image.open(file)
    if getattr(candidate, "n_frames", 1) != 6:
        file.unlink(missing_ok=True)
        raise ValueError("GIF gerado não possui seis quadros")
    print(json.dumps({
        "exercise": item["name"], "md_id": args.md_id, "gif": str(file.relative_to(ROOT)),
        "size": [width, height], "frames": 6,
        "state": "aprovado_pelo_operador" if args.approved else "rascunho_sem_qa"
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
