# AGENTS.md — oblinux-icon-theme operating guide

This repository owns the Arch `oblinux-icon-theme` package. It provides the
OBLinux Horizon icon experience originally approved and implemented in
`oblinux-debian-iso-dev`; do not modify that repository from here.

## Shipped themes

- `OBLinux-Horizon`: complete Papirus coverage transformed into the Obsidian
  Horizon palette, with regular application SVGs placed in the Horizon
  container and the original scalable identity layer taking lookup priority.
  It inherits `hicolor`.
- `OBLinux-Horizon-Dark`: transformed Papirus-Dark coverage. It inherits
  `OBLinux-Horizon,hicolor`, avoiding duplicate light application assets.
- `OBLinux`: metadata-only compatibility alias inheriting Horizon Dark. Keep it
  until the Arch ISO changes its existing `icon-theme='OBLinux'` setting.

## Repository map

```text
source/build_papirus_derivative.py   Reviewed Debian-reference transformation.
source/test_build_papirus_derivative.py
                                  Regression test for symbolic app handling.
source/validate_icon_themes.py     Metadata, SVG, and symlink validator.
source/90_oblinux-icon-theme.gschema.override
                                  GNOME system default (Horizon Dark).
source/OBLinux-Horizon/scalable/     Approved original 20-icon identity overlay.
source/OBLinux-compat/index.theme    Legacy Arch consumer compatibility alias.
PKGBUILD                          Generates and packages both full themes.
PAPIRUS-NOTICE.md                 Required derivative attribution.
```

The complete generated themes are build artifacts and must not be committed.
Arch `papirus-icon-theme=20260801-1` is pinned as a build dependency so a given
package revision always transforms the reviewed upstream input. It is not a
runtime dependency because the package contains the generated full light theme;
`hicolor-icon-theme` is the standards-compliant runtime fallback.

## Design and implementation rules

- Preserve the exact GNOME theme identifiers `OBLinux-Horizon` and
  `OBLinux-Horizon-Dark`.
- Preserve the GNOME system default `OBLinux-Horizon-Dark`; a schema override
  must not rewrite an existing user's explicit setting.
- Preserve Debian parity in the generator and scalable overlay. Intentional
  divergence requires documentation and visual/runtime validation.
- Do not wrap symbolic application icons in the regular Horizon application
  container; GTK otherwise renders solid foreground-colored squares.
- Generated symlinks must remain internal to the packaged theme trees and pass
  a `find -L ... -type l` broken-link check.
- Keep `AUTHORS`, `LICENSE`, and `PAPIRUS-NOTICE.md` with every derivative.
- Generated `src/`, `pkg/`, and `*.pkg.tar.zst*` output is ignored and must not
  be forced into Git.

## Build and validation

Run on Arch Linux:

```bash
python source/test_build_papirus_derivative.py
makepkg -s
tar -tf oblinux-icon-theme-*.pkg.tar.zst
python source/validate_icon_themes.py pkg/oblinux-icon-theme/usr/share/icons
```

Then verify all three `/usr/share/icons/<theme>/index.theme` files, ensure every
listed directory exists, confirm no broken symlinks, and run
`gtk-update-icon-cache --force` against both full theme directories in a staged
package tree. Full GNOME visual integration remains an ISO/runtime test.

## Versioning and publishing

Any payload or generator change requires a `pkgver`/`pkgrel` bump. Publishing
is deliberately outside this repository: copy the built archive into
`oblinux_repo/x86_64/`, run its `update_repo.sh` with the OBLinux signing key,
commit and push that repository, then confirm pacman can resolve the new
version. Never publish, commit, or push unless explicitly requested.

## Start-of-task checklist

Read this file and `CLAUDE.md` if present; inspect `git status`, `README.md`, the
generator, overlay, metadata, and `PKGBUILD`; compare any Horizon behavior change
against `oblinux-debian-iso-dev`; make the smallest complete in-repository
change; run proportional static, package, symlink, metadata, and visual checks;
state plainly whether publishing occurred and what remains for runtime proof.
