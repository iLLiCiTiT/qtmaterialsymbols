#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

CURRENT_DIR = Path(__file__).parent


def convert_variable_font(
    font_path: str,
    weight: int,
    base_name="MaterialSymbolsOutlined",
):
    print(f"--- Converting font ---")
    font_path = Path(font_path)
    codepoints_path = font_path.parent / font_path.name.replace(".ttf", ".codepoints")

    dst_dir = CURRENT_DIR / "src" / "qtmaterialsymbols" / "resources"
    static_file = dst_dir / f"{base_name}.ttf"
    static_file_filled = dst_dir / f"{base_name}Filled.ttf"
    json_file = dst_dir / f"{base_name}.json"

    print(f"- Converting variable font")
    var_font = TTFont(font_path)
    static_font = instantiateVariableFont(
        var_font, {"wght": weight}
    )
    static_font_filled = instantiateVariableFont(
        var_font, {"wght": weight, "FILL": 1.0}
    )

    # Change family name of filled font
    new_base_name = f"{base_name}Filled"
    family_base_name = "Material Symbols Outlined"
    new_family_base_name = "Material Symbols OutlinedFILL"

    for record in static_font_filled["name"].names:
        name_str = record.toUnicode()
        if family_base_name in name_str:
            new_name = name_str.replace(family_base_name, new_family_base_name)
        elif base_name in name_str:
            new_name = name_str.replace(base_name, new_base_name)
        else:
            continue

        static_font_filled["name"].setName(
            new_name,
            record.nameID,
            record.platformID,
            record.platEncID,
            record.langID,
        )

    static_font.save(static_file)
    static_font_filled.save(static_file_filled)
    print(f"  - Saved static fonts")

    # convert code points
    codepoints = Path(codepoints_path)
    print(f"- Converting codepoints {codepoints.name} to {json_file.name}")

    with open(codepoints, "r") as fr:
        data = fr.readlines()
    cp = {}
    for line in data:
        try:
            name, code = line.split(maxsplit=2)
        except ValueError:
            continue
        cp[name] = int(code, 16)
    with open(json_file, "w") as fw:
        json.dump(cp, fw, indent=4)
    print(f"    - Saved {json_file}")
    print(f"Done ! {json_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a variable font to a static font and codepoints to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--font-path",
        required=True,
        help="Path to the variable font file (.ttf)",
    )
    parser.add_argument(
        "-w",
        "--weight",
        type=int,
        default=400,
        help="Font weight value (default: 400)",
    )

    args = parser.parse_args()

    convert_variable_font(
        args.font_path,
        weight=args.weight,
    )
