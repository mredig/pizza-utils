#!/usr/bin/env sh

set -x

cd /usr/local/src || exit 1

if ! which git; then
	#install git

	. /etc/os-release

	case "$ID" in
		ubuntu|debian)
			apt-get update
			apt-get install -y git
		;;
		fedora|centos)
			if command -v dnf > /dev/null 2>&1; then
				dnf install -y git
			else
				yum install -y git
			fi
		;;
		alpine)
			apk update
			apk add git
		;;
		*)
			echo "Unsupported distro"
			exit 1
		;;
	esac
fi

if [ ! -d pizza-utils ]; then
	sudo git clone https://gitlab.com/mredig/pizza-utils
fi
cd pizza-utils
sudo git pull
sudo ./install.sh
