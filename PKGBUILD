# Contributor: Felix Kaiser <felix.kaiser@fxkr.net>

pkgname=reweek
pkgver=0.1.1
pkgrel=1
pkgdesc="adds the weekday to all yyyy-mm-dd strings in a text"
arch=('any')
license=('MIT')
depends=('python2')
makedepends=('setuptools')
source=(reweek-${pkgver}.tar.gz)
md5sums=('...')

build() {
  cd "$srcdir/reweek-$pkgver"
  python2 setup.py install --root="${pkgdir}" --optimize=1 || return 1
}

