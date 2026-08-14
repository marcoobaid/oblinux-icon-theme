# oblinux-icon-theme

OBLinux's default icon theme: amber-accented `places` icons (folders,
the home/user icon) on top of [Papirus](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme),
which this theme inherits for everything else — application icons,
mimetypes, devices, actions, status icons, and so on. Only the folder
and home-icon family is recolored; application icons keep their own
brand colors, same as every other icon theme's "folder color" feature
(this theme doesn't touch anything Papirus itself doesn't offer a
color variant for).

## License and attribution

GPL-3.0, same as Papirus — this is a derivative work and stays under
its upstream license. All non-`places` icons, and the underlying shape
of the `places` icons themselves, are Papirus's own work
([PapirusDevelopmentTeam/papirus-icon-theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)),
derived in turn from the Paper Icon Set. See `AUTHORS`.

## What was actually changed

Derived from Papirus's `orange` folder-color preset (release
`20260801`), all 81 "places" icon files (base `folder`/`folder-open`,
~70 named kinds — Documents, Downloads, Music, Pictures, Videos, Git,
Steam, etc. — plus the `user-home`/`user-desktop` family), across
every size Papirus itself ships color variants for: 22, 24, 32, 48,
64px (matching Papirus's own [`papirus-folders`](https://github.com/PapirusDevelopmentTeam/papirus-folders)
tool, which only touches these same five sizes — 16px folder icons
have no color variants upstream).

Each source SVG uses exactly two fill colors for the folder shape
itself (plus, on many icons, an unrelated third dark color for a small
badge glyph — e.g. the git branch icon on `folder-git.svg` — which was
left untouched, it's not part of the folder's own color):

| Role | Papirus orange | OBLinux amber |
|---|---|---|
| Main/front fill | `#ee923a` | `#d68a3c` (OBLinux's Amber, exact) |
| Back/shadow fill | `#dd772f` | `#b87027` (derived: same hue/saturation as Amber, ~10 points darker lightness, matching the ratio between Papirus's own two orange tones) |

## Building

```bash
makepkg -s
```

Then publish via [`oblinux_repo`](https://github.com/marcoobaid/oblinux_repo),
same as any other custom OBLinux package:

```bash
cp oblinux-icon-theme-*.pkg.tar.zst /path/to/oblinux_repo/x86_64/
cd /path/to/oblinux_repo/x86_64/
./update_repo.sh
```

## Installing

```
[oblinux_repo]
SigLevel = Required TrustedOnly
Server = https://marcoobaid.github.io/$repo/$arch
```
```bash
sudo pacman -S oblinux-icon-theme
```

`papirus-icon-theme` (official Arch `extra` package) is pulled in
automatically as a dependency — this theme is only the amber override
layer on top of it, not a full icon set on its own.
