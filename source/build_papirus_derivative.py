#!/usr/bin/env python3
"""Build complete OBLinux Horizon themes from an extracted Papirus package.

Generated themes are build artifacts and must not be committed. Papirus source
and license information must accompany every distributed derivative.
"""

from __future__ import annotations

import argparse
import colorsys
from pathlib import Path
import re
import shutil


HEX = re.compile(r"#([0-9a-fA-F]{6})(?![0-9a-fA-F])")
OPEN_SVG = re.compile(r"(<svg\b[^>]*>)", re.IGNORECASE)
CLOSE_SVG = re.compile(r"</svg>\s*$", re.IGNORECASE)
VIEWBOX = re.compile(r'viewBox="[^" ]+ [^" ]+ ([0-9.]+) ([0-9.]+)"', re.IGNORECASE)
WIDTH = re.compile(r'\bwidth="([0-9.]+)(?:px)?"', re.IGNORECASE)
HEIGHT = re.compile(r'\bheight="([0-9.]+)(?:px)?"', re.IGNORECASE)

NAVY = "#111820"
SLATE = "#1B2836"
OCEAN = "#176B87"
CYAN = "#4CC9D8"
MIST = "#F4F7F9"
WHITE = "#F2F5F7"
GREEN = "#35B98A"
AMBER = "#E5A84B"
RED = "#DF5B61"


def rewrite_papirus_links(destination: Path) -> int:
    """Retarget copied Papirus aliases to the generated Horizon themes."""
    rewritten = 0
    for path in destination.rglob("*"):
        if not path.is_symlink():
            continue
        target = path.readlink()
        updated = Path(str(target).replace("Papirus-Dark", "OBLinux-Horizon-Dark").replace("Papirus", "OBLinux-Horizon"))
        if updated == target:
            continue
        path.unlink()
        path.symlink_to(updated)
        rewritten += 1
    return rewritten


def mix(first: tuple[int, int, int], second: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a + (b - a) * amount) for a, b in zip(first, second))


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def hex_color(value: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{part:02X}" for part in value)


def horizon_color(match: re.Match[str]) -> str:
    original = rgb(match.group(1))
    red, green, blue = (part / 255 for part in original)
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)

    if saturation < 0.16:
        if lightness < 0.18:
            target = rgb(NAVY)
        elif lightness < 0.48:
            target = rgb(SLATE)
        elif lightness < 0.78:
            target = mix(rgb(SLATE), rgb(MIST), (lightness - 0.48) / 0.30)
        else:
            target = mix(rgb(MIST), rgb(WHITE), min(1.0, (lightness - 0.78) / 0.22))
        return hex_color(target)

    degrees = hue * 360
    if degrees < 25 or degrees >= 345:
        anchor = rgb(RED)
    elif degrees < 75:
        anchor = rgb(AMBER)
    elif degrees < 170:
        anchor = rgb(GREEN)
    elif degrees < 285:
        anchor = rgb(CYAN if lightness > 0.53 else OCEAN)
    else:
        anchor = rgb(OCEAN if lightness < 0.55 else CYAN)

    if lightness < 0.38:
        anchor = mix(rgb(NAVY), anchor, max(0.35, lightness / 0.38))
    elif lightness > 0.72:
        anchor = mix(anchor, rgb(MIST), min(0.62, (lightness - 0.72) / 0.28))
    return hex_color(anchor)


def recolor(svg: str) -> str:
    return HEX.sub(horizon_color, svg)


def is_symbolic_icon(path: Path) -> bool:
    """Return whether GTK must render this icon as symbolic artwork."""
    return "symbolic" in path.parts or path.stem.endswith("-symbolic")


def app_container(svg: str) -> str:
    open_match = OPEN_SVG.search(svg)
    close_match = CLOSE_SVG.search(svg)
    viewbox = VIEWBOX.search(svg)
    if not open_match or not close_match:
        return svg

    if viewbox:
        width = float(viewbox.group(1))
        height = float(viewbox.group(2))
    else:
        width_match = WIDTH.search(open_match.group(1))
        height_match = HEIGHT.search(open_match.group(1))
        if not width_match or not height_match:
            return svg
        width = float(width_match.group(1))
        height = float(height_match.group(1))
    if width <= 0 or height <= 0:
        return svg
    inset = min(width, height) * 0.12
    scale = 0.76
    radius = min(width, height) * 0.23
    line_y = height * 0.68
    stroke = max(1.0, min(width, height) * 0.038)
    body = svg[open_match.end():close_match.start()]
    frame = f'''\n  <rect x="{width * .03:.3f}" y="{height * .03:.3f}" width="{width * .94:.3f}" height="{height * .94:.3f}" rx="{radius:.3f}" fill="{SLATE}"/>
  <path d="M{width * .14:.3f} {line_y:.3f}c{width * .20:.3f} {-height * .12:.3f} {width * .37:.3f} {height * .12:.3f} {width * .57:.3f} 0 {width * .12:.3f} {-height * .075:.3f} {width * .22:.3f} {-height * .045:.3f} {width * .30:.3f} {-height * .015:.3f}" fill="none" stroke="{CYAN}" stroke-width="{stroke:.3f}" stroke-linecap="round" opacity=".72"/>
  <g transform="translate({inset:.3f} {inset * .81:.3f}) scale({scale})">\n'''
    return svg[:open_match.end()] + frame + body + "\n  </g>\n" + svg[close_match.start():]


def update_index(path: Path, name: str, inherits: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^Name=.*$", f"Name={name}", text, count=1, flags=re.MULTILINE)
    if re.search(r"^Inherits=.*$", text, flags=re.MULTILINE):
        text = re.sub(r"^Inherits=.*$", f"Inherits={inherits}", text, count=1, flags=re.MULTILINE)
    else:
        text = text.replace("[Icon Theme]\n", f"[Icon Theme]\nInherits={inherits}\n", 1)
    path.write_text(text, encoding="utf-8")


def install_identity_overlay(theme: Path, overlay: Path) -> int:
    """Prepend the approved scalable Horizon identity layer to a full theme."""
    source = overlay / "scalable"
    if not source.is_dir():
        raise SystemExit(f"missing Horizon overlay: {source}")
    target = theme / "oblinux-scalable"
    shutil.copytree(source, target)

    sections = []
    directories = []
    for child in sorted(target.iterdir()):
        if not child.is_dir():
            continue
        relative = f"oblinux-scalable/{child.name}"
        directories.append(relative)
        context = child.name.title()
        sections.append(
            f"\n[{relative}]\nSize=128\nMinSize=16\nMaxSize=256\n"
            f"Type=Scalable\nContext={context}\n"
        )

    index = theme / "index.theme"
    text = index.read_text(encoding="utf-8")
    match = re.search(r"^Directories=(.*)$", text, flags=re.MULTILINE)
    if not match:
        raise SystemExit(f"missing Directories entry: {index}")
    existing = match.group(1)
    text = text[:match.start()] + "Directories=" + ",".join(directories) + "," + existing + text[match.end():]
    text += "".join(sections)
    index.write_text(text, encoding="utf-8")
    return sum(1 for path in target.rglob("*.svg"))


def transform_theme(source: Path, destination: Path, name: str, inherits: str) -> tuple[int, int, int]:
    shutil.copytree(source, destination, symlinks=True)
    cache = destination / "icon-theme.cache"
    if cache.exists():
        cache.unlink()
    aliases = rewrite_papirus_links(destination)
    update_index(destination / "index.theme", name, inherits)
    applications = 0
    system_icons = 0
    for path in destination.rglob("*.svg"):
        if path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8")
        # GNOME Settings panel entries are symbolic icons stored below an
        # `apps` directory. They must remain single-color symbolic artwork;
        # wrapping them in the regular application container makes GTK reduce
        # the entire composition to a solid foreground-colored square.
        if path.parent.name == "apps" and not is_symbolic_icon(path):
            transformed = app_container(text)
            if transformed != text:
                applications += 1
            text = transformed
        else:
            text = recolor(text)
            system_icons += 1
        path.write_text(text, encoding="utf-8")
    return applications, system_icons, aliases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="directory containing Papirus and Papirus-Dark")
    parser.add_argument("destination", type=Path)
    parser.add_argument(
        "--overlay",
        type=Path,
        help="approved OBLinux-Horizon pilot directory to layer over the full base theme",
    )
    args = parser.parse_args()

    themes = (
        ("Papirus", "OBLinux-Horizon", "OBLinux Horizon", "hicolor"),
        ("Papirus-Dark", "OBLinux-Horizon-Dark", "OBLinux Horizon Dark", "OBLinux-Horizon,hicolor"),
    )
    args.destination.mkdir(parents=True, exist_ok=True)
    for source_name, target_name, display_name, inherits in themes:
        source = args.source / source_name
        target = args.destination / target_name
        if target.exists():
            raise SystemExit(f"refusing to overwrite existing output: {target}")
        if not (source / "index.theme").is_file():
            raise SystemExit(f"missing source theme: {source}")
        applications, system_icons, aliases = transform_theme(source, target, display_name, inherits)
        overlay_icons = 0
        if args.overlay and target_name == "OBLinux-Horizon":
            overlay_icons = install_identity_overlay(target, args.overlay)
        print(
            f"{target_name}: {applications} application SVGs; "
            f"{system_icons} recolored system SVGs; {aliases} aliases retargeted; "
            f"{overlay_icons} identity icons overlaid"
        )


if __name__ == "__main__":
    main()
