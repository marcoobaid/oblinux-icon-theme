#!/usr/bin/env python3
"""Validate generated OBLinux Horizon icon-theme trees."""

from __future__ import annotations

import configparser
from pathlib import Path
import sys
import xml.etree.ElementTree as element_tree


EXPECTED = {
    "OBLinux-Horizon": ("OBLinux Horizon", "hicolor"),
    "OBLinux-Horizon-Dark": (
        "OBLinux Horizon Dark",
        "OBLinux-Horizon,hicolor",
    ),
}


def validate(theme: Path, expected_name: str, expected_inherits: str) -> tuple[int, int]:
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    parser.optionxform = str
    with (theme / "index.theme").open(encoding="utf-8") as stream:
        parser.read_file(stream)

    metadata = parser["Icon Theme"]
    if metadata.get("Name") != expected_name:
        raise ValueError(f"{theme}: unexpected Name={metadata.get('Name')!r}")
    if metadata.get("Inherits") != expected_inherits:
        raise ValueError(f"{theme}: unexpected Inherits={metadata.get('Inherits')!r}")

    directories = [item for item in metadata["Directories"].split(",") if item]
    for relative in directories:
        if relative not in parser:
            raise ValueError(f"{theme}: missing metadata section [{relative}]")
        if not (theme / relative).is_dir():
            raise ValueError(f"{theme}: listed directory is absent: {relative}")

    svg_count = 0
    symlink_count = 0
    for path in theme.rglob("*"):
        if path.is_symlink():
            symlink_count += 1
            if not path.exists():
                raise ValueError(f"{theme}: broken symlink: {path}")
        if path.suffix == ".svg":
            svg_count += 1
            try:
                element_tree.parse(path)
            except element_tree.ParseError as error:
                raise ValueError(f"{theme}: invalid SVG: {path}: {error}") from error
    return svg_count, symlink_count


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} ICON_ROOT")
    root = Path(sys.argv[1])
    for name, expected in EXPECTED.items():
        svg_count, symlink_count = validate(root / name, *expected)
        print(f"{name}: {svg_count} SVGs; {symlink_count} valid symlinks")


if __name__ == "__main__":
    main()
