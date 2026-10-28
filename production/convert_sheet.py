"""Convert an original 3-by-2 sprite sheet to a validated looping GIF."""
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from PIL import Image

ident, source = sys.argv[1:3]
root = Path(__file__).resolve().parent.parent
with Image.open(source) as sheet:
 sheet.load()
 w, h = sheet.size
 if abs(w / h - 1.5) > 0.03:
  raise ValueError('A folha deve ter três colunas e duas linhas de células quadradas.')
 cw, ch = w // 3, h // 2
 frames = []
 for n in range(6):
  x, y = n % 3 * cw, n // 3 * ch
  frames.append(sheet.crop((x + 2, y + 2, x + cw - 2, y + ch - 2)).convert('RGB').resize((512, 512), Image.Resampling.LANCZOS))
out = root / 'dist/assets/exercises' / f'{ident}.gif'
out.parent.mkdir(parents=True, exist_ok=True)
fd, temporary = tempfile.mkstemp(prefix=f'.{ident}-', suffix='.gif', dir=out.parent)
os.close(fd)
try:
 frames[0].save(temporary, format='GIF', save_all=True, append_images=frames[1:], duration=[180, 180, 180, 240, 180, 180], loop=0, disposal=2, optimize=False)
 with Image.open(temporary) as check:
  assert check.n_frames == 6 and check.info.get('loop') == 0
  hashes = []
  for f in range(check.n_frames):
   check.seek(f)
   hashes.append(hashlib.sha256(check.convert('RGB').tobytes()).digest())
  assert len(set(hashes)) >= 4, 'A demonstração precisa de pelo menos quatro quadros diferentes.'
 os.replace(temporary, out)
finally:
 if os.path.exists(temporary): os.unlink(temporary)
print(json.dumps({'id': ident, 'path': str(out), 'bytes': out.stat().st_size, 'source_dimensions': [w, h]}))
