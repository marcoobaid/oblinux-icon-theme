# CLAUDE.md — oblinux-icon-theme

Operating guide for Claude Code in this repository. Keep it short and
practical. The authoritative, detailed guide is **`AGENTS.md`** at the
repo root — read it in full before making changes; this file only
summarizes and points into it. For the broader OBLinux project (ISO,
package strategy, branding, signing) see the primary `oblinux` repo's
`AGENTS.md` and its `docs/`. This repository has no `docs/` directory of
its own — `README.md` and `AGENTS.md` are the only local docs.

## Purpose and scope

This repo owns exactly one Arch package, `oblinux-icon-theme`: an
**inheriting** icon theme that recolors only the `places` icon family
(folders and the `user-home` / `user-desktop` icons) to OBLinux's amber,
and inherits everything else from `papirus-icon-theme`, which is a real
pacman `depends` (never vendored or forked here).

## Repository map

```
OBLinux/index.theme            Theme metadata: Inherits=Papirus,hicolor;
                               declares the 5 size/places directories.
OBLinux/{22,24,32,48,64}x{same}/places/*.svg
                               The entire shipped artifact: 81 icons per
                               size, 405 SVGs total, identical filename
                               set across all 5 sizes. Edited by hand —
                               there is no generator.
PKGBUILD                       No compile step; package() just copies
                               OBLinux/ to /usr/share/icons/OBLinux.
                               Version lives here (pkgver / pkgrel).
AUTHORS, LICENSE               GPL-3.0 derivative-work attribution
                               (Papirus, in turn Paper Icon Set).
```

## Design conventions (load-bearing — verify before editing)

- **`places`-only scope.** Do not add icons in other contexts. Changing
  scope means updating `OBLinux/index.theme`'s `Directories=` too.
- **Two folder fill colors**, front/back, per folder SVG. The exact
  Papirus-orange → OBLinux-amber hex mapping is in `README.md`'s table
  (`#d68a3c` front, `#b87027` back). Every shipped SVG currently contains
  `#d68a3c` and none contains the old `#ee923a`.
- **Badge glyph colors** (e.g. the dark mark on `folder-git.svg`) are not
  part of the folder color — leave them unless the badge itself changes.
- **All 5 sizes stay in lockstep.** Any new, renamed, or removed icon
  must be applied identically under `22x22`, `24x24`, `32x32`, `48x48`,
  and `64x64`. The five sizes match Papirus's `papirus-folders` coverage
  (no 16px variants upstream, so none here).
- **No generated content.** Every committed file is authoritative
  hand-derived source; only the `.pkg.tar.zst` is generated, and it is
  not committed here.

## Build / validate

```bash
makepkg -s        # needs base-devel; produces oblinux-icon-theme-<pkgver>-<pkgrel>-any.pkg.tar.zst
tar -tf oblinux-icon-theme-*.pkg.tar.zst   # sanity-check install paths
```

There is no test suite or CI. Validation is: visually inspect edited
SVGs, confirm hex fills against `README.md`, confirm `makepkg -s`
produces the package with the expected `usr/share/icons/OBLinux/...`
layout. Full "does it look right as GNOME's default" is only provable by
building and booting an `oblinux` ISO in the primary repo.

## Cross-repository workflow

Editing SVGs alone changes nothing for OBLinux users. To ship a change:
bump `pkgver` / `pkgrel` in `PKGBUILD` → `makepkg -s` here → copy the
`.pkg.tar.zst` into `oblinux_repo/x86_64/` → run that repo's
`update_repo.sh` (signs, rebuilds the repo DB) → commit and push
`oblinux_repo`. This repo has no publishing mechanism of its own. See
`AGENTS.md` "Cross-repository change workflow" for the full sequence and
the signing-key requirement.

## Special care

- `AUTHORS` and `LICENSE` — GPL-3.0 derivative attribution; do not remove
  or alter.
- `OBLinux/index.theme` — breaking `Directories=` / the size structure
  produces a theme that installs but fails icon lookup.
- Re-deriving icons from Papirus upstream: verify each fetched file
  contains real SVG markup, not a path string — several Papirus per-color
  SVGs are symlinks (see `AGENTS.md` "Known pitfalls").

## Git and commits

- No `.gitignore` exists. Never `git add` `makepkg` output (`pkg/`,
  `src/`, `*.pkg.tar.zst*`).
- Match existing history: short, imperative subject lines
  (e.g. `Add OBLinux amber places icon theme`).
- Do not add Claude/Anthropic attribution, `Co-Authored-By`, or
  generated-by notes to commits or repository content.

## Documentation expectations

Update `AGENTS.md` only when a change materially affects what the repo
ships, its Papirus dependency, or the build/publish workflow — not for
routine icon edits. Keep `README.md`'s color table accurate if fills
change. Do not duplicate `AGENTS.md` content into this file.
