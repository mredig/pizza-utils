#!/usr/bin/env sh

set -x

cd /usr/local/src || exit 1
sudo git clone https://gitlab.com/mredig/pizza-utils
cd pizza-utils
sudo ./install.sh