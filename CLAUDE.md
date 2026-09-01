# CLAUDE.md — oblinux-icon-theme

Read `AGENTS.md` in full. This package builds the complete `OBLinux-Horizon` and
`OBLinux-Horizon-Dark` themes from pinned Arch Papirus input using the reviewed
Debian-reference transformation and approved scalable overlay. `OBLinux` is a
metadata-only compatibility alias for the current Arch ISO setting.

Do not commit generated full theme trees, `src/`/`pkg/` makepkg output, or
package archives. Preserve symbolic-icon handling, exact theme names,
inheritance, attribution, and the Papirus build-input pin. Build on Arch with
`makepkg -s`; validate metadata, the Horizon Dark GNOME default, packaged paths,
and broken symlinks. Publishing
occurs only through `oblinux_repo` and is never implicit.
