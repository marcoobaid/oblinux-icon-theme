# AGENTS.md — oblinux-icon-theme operating guide

Repository-specific guide. For the broader OBLinux project (the ISO,
package strategy, branding system) see the primary repository's
[`AGENTS.md`](https://github.com/marcoobaid/oblinux/blob/main/AGENTS.md)
and `docs/THEMING.md` (item 4) — this file only covers what's specific to
working in *this* repository.

## Repository purpose

This repository owns exactly one Arch package: `oblinux-icon-theme`, an
**inheriting** icon theme. It recolors only the `places` icon family
(folders and the home/desktop user icons) to OBLinux's Amber, and
inherits everything else — every application, mimetype, device, and
status icon — from `papirus-icon-theme` (an official Arch package,
declared as a `depends=()`, not vendored here). It exists as a separate
repo because it's an independently versioned build artifact, not
free-form config — same reasoning the primary repo's `AGENTS.md`
documents for why `oblinux_repo`-published packages live outside it.

## Relationship to OBLinux

- **Consumer**: the primary `oblinux` repo lists `oblinux-icon-theme` in
  `packages.x86_64` and sets it as the default via
  `org.gnome.desktop.interface icon-theme='OBLinux'` in its gschema
  override. That repo only ever *installs* the built package — it does
  not build it.
- **Publish path**: this repo produces a `.pkg.tar.zst` via `makepkg`;
  that artifact is copied into `oblinux_repo/x86_64/` and published from
  *there* (`update_repo.sh`, signing, `git push`) — this repo has no
  publishing mechanism of its own and never talks to GitHub Pages
  directly.
- **Dependency, not a fork**: `papirus-icon-theme` is a runtime pacman
  dependency, resolved fresh from Arch's official repos on install — this
  repo does not track or vendor Papirus's source.
- **When a change here requires action elsewhere**: any change to the
  files under `OBLinux/` requires bumping `pkgver` in `PKGBUILD`,
  rebuilding, and republishing through `oblinux_repo` before a new
  `oblinux` ISO build will actually pick it up — editing the SVGs alone
  changes nothing for OBLinux users until that happens.

## Repository map

```
OBLinux/                 The theme itself — installed verbatim to
                          /usr/share/icons/OBLinux by PKGBUILD's package().
OBLinux/index.theme       Theme metadata: Inherits=Papirus,hicolor, and the
                          5 size/context directories declared below.
OBLinux/{22,24,32,48,64}x{same}/places/*.svg
                          405 files (81 icons x 5 sizes) — the only
                          content this theme actually ships; everything
                          else comes from the Papirus dependency at
                          install time.
PKGBUILD                  No compile step — package() just copies OBLinux/
                          into place. Version lives here (pkgver/pkgrel).
AUTHORS                   Required attribution: this is a GPL-3.0
                          derivative of Papirus (and, in turn, Paper Icon
                          Set) — do not remove.
```

## Architecture and workflow

There is no build/generation step for the icons themselves — the SVGs
under `OBLinux/` **are** the shipped artifact, edited directly. The only
"build" is packaging:

```bash
makepkg -s
```
produces `oblinux-icon-theme-<pkgver>-<pkgrel>-any.pkg.tar.zst`, which is
then handed to `oblinux_repo` to sign and publish (see that repo's own
`README.md`/`update_repo.sh` — this repo has no equivalent script).

The 5 sizes and their exact directory names match Papirus's own
[`papirus-folders`](https://github.com/PapirusDevelopmentTeam/papirus-folders)
tool precisely (22/24/32/48/64px — Papirus ships no 16px folder color
variants, so there is no `16x16/places` here either). If Papirus ever
adds or drops a size in its own color-variant coverage, this theme's
`Directories=` list and folder structure should be re-checked against it,
not assumed to still match.

## Authoritative vs. generated files

Everything committed here is authoritative hand-derived source — there is
**no generated content in this repo**. The only generated artifact is the
`.pkg.tar.zst` from `makepkg`, which is intentionally **not** committed
here (it's published through `oblinux_repo` instead). There is currently
no `.gitignore` — if you run `makepkg` locally, do not `git add` the
resulting `pkg/`, `src/`, or `*.pkg.tar.zst*` output.

## Common development tasks

- **Recolor or add a places icon**: edit the relevant SVG(s) directly
  under each size's `places/` directory. Each folder SVG uses exactly two
  fill colors for the folder shape itself (front/back — see `README.md`'s
  table for the exact Papirus-orange → OBLinux-amber hex mapping already
  applied); a badge glyph color (e.g. the git branch mark on
  `folder-git.svg`) is unrelated to the folder color and should be left
  alone unless the badge itself is what's changing. **Any new/renamed
  icon needs the same file added at all 5 sizes** to stay consistent.
- **Bump the version**: increment `pkgver`/`pkgrel` in `PKGBUILD` before
  rebuilding — pacman won't upgrade an already-installed package with an
  unchanged version string.
- **Build**: `makepkg -s` (needs `base-devel`; `-s` resolves
  `papirus-icon-theme` as a build-time dependency check, though it's only
  a runtime `depends`, not compiled against).
- **Publish**: see Cross-Repository Change Workflow below.

## Cross-repository change workflow

1. Edit SVGs / `index.theme` / `PKGBUILD` here; bump `pkgver`/`pkgrel`.
2. `makepkg -s` here to produce the `.pkg.tar.zst`.
3. Copy that file into a checkout of `oblinux_repo`'s `x86_64/`.
4. Run `oblinux_repo`'s `x86_64/update_repo.sh` there (signs the package,
   regenerates the signed repo database) — needs the OBLinux repo signing
   key in the calling user's GPG keyring; see the primary repo's
   `docs/PACKAGE_SIGNING.md`.
5. Commit and push `oblinux_repo` to publish via GitHub Pages.
6. Only after that is live does a fresh `oblinux` ISO build's `pacstrap`
   see the new version — no action is needed in the primary repo itself
   unless the theme's *name* or default-selection mechanism changes.

## Validation

- **Source changed**: visually inspect the edited SVG(s) — check fill
  colors match the documented hex values and the icon renders correctly
  at its target size (`file`/an SVG viewer is enough; no automated check
  exists here).
- **Package built**: confirm `makepkg -s` completes and produces the
  expected `.pkg.tar.zst`; sanity-check its contents
  (`tar -tf oblinux-icon-theme-*.pkg.tar.zst`) install to
  `usr/share/icons/OBLinux/...` as expected.
- **Published**: confirmed resolvable via `oblinux_repo` (`pacman -Sy
  oblinux-icon-theme` on a system with that repo configured).
- **Full integration** (does it actually look right as GNOME's default
  icon theme, does Papirus inheritance resolve correctly for everything
  else): only provable by building and booting an `oblinux` ISO — that
  step happens in the primary repo, not here.

## Important architectural decisions

- **Inheriting theme, not a full fork** — deliberately ships only the
  81 `places` icons it actually recolors, relying on `papirus-icon-theme`
  as a real dependency for everything else. Avoids vendoring or
  maintaining a multi-thousand-icon set. Don't add non-`places` icons
  here; extend Papirus's own theme or scope a new inheriting layer
  instead.
- **No compile/build-from-source step** — the SVGs are hand-derived once
  (from Papirus's own `orange` preset) and committed as final files, not
  regenerated by a script. If Papirus's upstream source colors ever
  change, this theme's colors do not automatically follow — a manual
  re-derivation would be needed.
- **`papirus-icon-theme` is a `depends`, never bundled** — keeps this
  package tiny and keeps it automatically benefiting from Papirus's own
  updates (new app icons, bug fixes) without needing a republish here.

## Known pitfalls and lessons learned

- **Symptom**: an icon file recolored via an automated/scripted pass ends
  up containing a literal filesystem path string instead of real SVG
  content. **Cause**: this happened once during the original derivation —
  GitHub serves a *symlinked* file's raw content as the link's target
  path string, not the resolved file content, when fetched naively.
  Several of Papirus's own per-color SVGs are symlinks to a shared
  "default" file. **Correct approach**: if ever re-deriving icons from
  Papirus's upstream source again (e.g. after a Papirus update), verify
  every fetched file actually contains SVG markup (not a bare path
  string) before use — don't trust file count alone.

## Development rules

- Inspect the actual SVG content and `index.theme` before changing
  anything — the two-fill-color convention (front/back) and the 5-size
  structure are load-bearing; breaking either produces a theme that
  installs but looks wrong or fails GTK's icon lookup.
- Keep the `places`-only scope — do not expand into other icon contexts
  without deciding that's an intentional, separate change (and updating
  `index.theme`'s `Directories=` accordingly).
- Never commit `makepkg` build output (`pkg/`, `src/`, the
  `.pkg.tar.zst`) to this repo.
- Keep `AUTHORS` and the GPL-3.0 `LICENSE` intact — this is a licensed
  derivative work, not original-license content.
- Validate a color change against the documented hex table in
  `README.md` before publishing — don't eyeball it.

## Start-of-task workflow

1. Read this file.
2. Check `git status`.
3. Skim `README.md` for the current color mapping and build/publish
   commands.
4. Confirm the requested change is actually owned here (icon content) and
   not in the primary `oblinux` repo (how the theme is *selected/applied*
   system-wide) or `oblinux_repo` (how it's *published*).
5. Make the smallest complete change across all affected sizes.
6. Validate per the section above.
7. State plainly whether publishing through `oblinux_repo` is needed for
   the change to reach a real system, and whether that happened.
8. Summarize what changed and what still needs verification.

## Maintaining this file

Update this file when a change materially affects: what this repository
ships (e.g. expanding beyond `places` icons), its dependency on
`papirus-icon-theme`, the build/publish workflow, or a lesson future
agents need to avoid repeating. Don't update it for routine icon edits
that don't change the workflow. Remove stale content rather than letting
it accumulate.
