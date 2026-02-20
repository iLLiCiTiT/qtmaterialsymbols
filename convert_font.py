#!/usr/bin/env python3

import json
from pathlib import Path

CURRENT_DIR = Path(__file__).parent


def convert_font_codepoints():
    print(f"--- Converting font codepoints ---")

    base_name = "MaterialSymbolsOutlined[FILL,GRAD,opsz,wght]"

    fond_dir = CURRENT_DIR / "src" / "qtmaterialsymbols" / "resources"
    codepoints_path = fond_dir / f"{base_name}.codepoints"
    json_path = fond_dir / f"{base_name}.json"
    data = codepoints_path.read_text().splitlines()
    cp = {}
    for line in data:
        name, code = line.split(" ", maxsplit=2)
        cp[name] = int(code, 16)

    with open(json_path, "w") as fw:
        json.dump(cp, fw, indent=4)
    print(f"--- Done! ---")


if __name__ == "__main__":
    convert_font_codepoints()
