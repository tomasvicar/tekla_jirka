"""Sestaví files/tekla_balicek.zip pro stránku Živá Tekla.

Obsah zipu:
    CLAUDE_tekla.md
    .claude/skills/tekla-makro/SKILL.md
    makra/*.cs

Spuštění (ze složky workshop/):  uv run python tools/make_tekla_zip.py
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ROOT / "files"
OUT = FILES / "tekla_balicek.zip"
# Pevné datum, ať je zip při stejném obsahu bajtově stejný.
DATE = (2026, 1, 1, 0, 0, 0)


def main() -> None:
    items = [
        (FILES / "CLAUDE_tekla.md", "CLAUDE_tekla.md"),
        (FILES / "skills" / "tekla-makro" / "SKILL.md", ".claude/skills/tekla-makro/SKILL.md"),
    ]
    items += [(p, f"makra/{p.name}") for p in sorted((FILES / "makra").glob("*.cs"))]

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for src, name in items:
            info = zipfile.ZipInfo(name, DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, src.read_bytes())
    print(f"{OUT.relative_to(ROOT)}: {len(items)} souborů")


if __name__ == "__main__":
    main()
