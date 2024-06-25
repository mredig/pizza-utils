#!/usr/bin/env sh

set -x

cd /usr/local/src || exit 1

if [ ! -d pizza-utils ]; then
	sudo git clone https://gitlab.com/mredig/pizza-utils
fi
cd pizza-utils
sudo git pull
sudo ./install.sh
