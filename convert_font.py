#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


def convert_variable_font(
    var_font_path: str,
    codepoints_path: str,
    weight=400,
    base_name="MaterialSymbolsOutlined",
):
    print(f"convert_variable_font ------------------------------------------")

    var_file = Path(var_font_path)
    static_file = var_file.parent / f"{base_name}.ttf"

    print(
        f"  - Converting variable font {var_file.name} to {static_file.name}"
    )
    var_font = TTFont(var_file)
    static_font = instantiateVariableFont(var_font, {"wght": weight})
    static_font.save(static_file)
    print(f"    - Saved {static_file}")

    # convert code points
    codepoints = Path(codepoints_path)
    json_file = codepoints.parent / f"{base_name}.json"
    print(f"  - Converting codepoints {codepoints.name} to {json_file.name}")

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
        "-v",
        "--var-font-path",
        required=True,
        help="Path to the variable font file (.ttf)",
    )

    parser.add_argument(
        "-c",
        "--codepoints-path",
        required=True,
        help="Path to the codepoints file",
    )

    parser.add_argument(
        "-w",
        "--weight",
        type=int,
        default=400,
        help="Font weight value (default: 400)",
    )

    parser.add_argument(
        "-b",
        "--base-name",
        default="MaterialSymbolsOutlined",
        help="Base name for output files (default: MaterialSymbolsOutlined)",
    )

    args = parser.parse_args()

    convert_variable_font(
        var_font_path=args.var_font_path,
        codepoints_path=args.codepoints_path,
        weight=args.weight,
        base_name=args.base_name,
    )
