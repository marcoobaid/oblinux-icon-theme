# Maintainer: OBLinux
pkgname=oblinux-icon-theme
pkgver=1.0.0
pkgrel=1
pkgdesc="OBLinux amber-accented places icons, a Papirus derivative"
arch=('any')
url="https://github.com/marcoobaid/oblinux-icon-theme"
license=('GPL3')
depends=('papirus-icon-theme')
source=()
sha256sums=()

package() {
  install -d "$pkgdir/usr/share/icons/OBLinux"
  cp -r "$startdir/OBLinux/." "$pkgdir/usr/share/icons/OBLinux/"
}
