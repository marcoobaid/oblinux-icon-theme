# Maintainer: OBLinux
pkgname=oblinux-icon-theme
pkgver=2.0.0
pkgrel=1
pkgdesc="OBLinux Horizon desktop icon themes, a Papirus derivative"
arch=('any')
url="https://github.com/marcoobaid/oblinux-icon-theme"
license=('GPL-3.0-only')
depends=('glib2' 'hicolor-icon-theme')
makedepends=('papirus-icon-theme=20260801-1' 'python')
source=()
sha256sums=()

prepare() {
  rm -rf -- "$srcdir/generated"
  python "$startdir/source/build_papirus_derivative.py" \
    --overlay "$startdir/source/OBLinux-Horizon" \
    /usr/share/icons \
    "$srcdir/generated"
}

package() {
  install -d "$pkgdir/usr/share/icons"
  cp -a "$srcdir/generated/OBLinux-Horizon" "$pkgdir/usr/share/icons/"
  cp -a "$srcdir/generated/OBLinux-Horizon-Dark" "$pkgdir/usr/share/icons/"

  # Compatibility for the current Arch ISO default. This contains no icons;
  # it resolves every lookup through the reviewed Horizon Dark theme.
  install -d "$pkgdir/usr/share/icons/OBLinux"
  install -m644 "$startdir/source/OBLinux-compat/index.theme" \
    "$pkgdir/usr/share/icons/OBLinux/index.theme"

  install -Dm644 "$startdir/PAPIRUS-NOTICE.md" \
    "$pkgdir/usr/share/doc/$pkgname/PAPIRUS-NOTICE.md"
  install -Dm644 "$startdir/LICENSE" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 "$startdir/source/90_oblinux-icon-theme.gschema.override" \
    "$pkgdir/usr/share/glib-2.0/schemas/90_oblinux-icon-theme.gschema.override"
}
