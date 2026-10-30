"""Zkopíruje zprávy z ../research do pruzkum/, aby je Quarto vyrenderovalo jako stránky webu."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src, dst = root.parent / "research", root / "pruzkum"
dst.mkdir(exist_ok=True)
for f in sorted(src.glob("*.md")):
    shutil.copyfile(f, dst / f.name)
