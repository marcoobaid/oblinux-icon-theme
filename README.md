# oblinux-icon-theme

OBLinux's Horizon icon-theme package for Arch Linux. It provides the same two
GNOME theme names and visual treatment as `oblinux-debian-iso-dev`:

- `OBLinux-Horizon` — complete Papirus coverage transformed into the Obsidian
  Horizon palette, with recognizable application artwork placed in the Horizon
  container and the approved 20-icon scalable identity layer overlaid first.
- `OBLinux-Horizon-Dark` — transformed Papirus Dark coverage, inheriting
  `OBLinux-Horizon,hicolor`.
- `OBLinux` — metadata-only compatibility alias inheriting Horizon Dark. It
  keeps the current Arch ISO default working until that consumer explicitly
  selects `OBLinux-Horizon-Dark`.

The packaged GLib schema override selects `OBLinux-Horizon-Dark` as GNOME's
system default, matching Debian without overwriting an existing user's explicit
setting.

The generated full icon trees are package build artifacts, not committed
source. The tracked inputs are the approved OBLinux scalable overlay and the
reviewed transformation used by the Debian implementation. Arch's
`papirus-icon-theme` `20260801-1` is an exact build dependency; it is transformed
during `makepkg` and is not required at runtime.

## Building

On Arch Linux:

```bash
makepkg -s
```

This produces `oblinux-icon-theme-2.0.0-1-any.pkg.tar.zst`. The package installs
its themes below `/usr/share/icons/` and includes the Papirus attribution notice
and GPL-3.0 license. Arch's GLib and icon-cache hooks process the installed
metadata. Generated `src/`, `pkg/`, and package archives must not be committed.

## Validation

```bash
tar -tf oblinux-icon-theme-2.0.0-1-any.pkg.tar.zst
python source/validate_icon_themes.py pkg/oblinux-icon-theme/usr/share/icons
find -L pkg/oblinux-icon-theme/usr/share/icons/OBLinux-Horizon \
  pkg/oblinux-icon-theme/usr/share/icons/OBLinux-Horizon-Dark -type l -print
```

The second command must print nothing. Both generated `index.theme` files must
list only directories present in their respective theme and preserve these
inheritance chains:

```text
OBLinux-Horizon      -> hicolor
OBLinux-Horizon-Dark -> OBLinux-Horizon,hicolor
OBLinux              -> OBLinux-Horizon-Dark,OBLinux-Horizon,hicolor
```

## License and attribution

GPL-3.0-only. The complete generated themes are derivatives of Papirus Icon
Theme, itself derived from Paper Icon Set. See `AUTHORS`, `LICENSE`, and
`PAPIRUS-NOTICE.md`.

## Publishing

Do not publish from this repository. Copy the built package to
`oblinux_repo/x86_64/`, sign it and regenerate that repository's signed database
with `update_repo.sh`, commit the repository changes, and push `oblinux_repo`.
