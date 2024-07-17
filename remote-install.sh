#!/usr/bin/env sh

INTERACTIVE=1
if [ "$1" = "-f" ]; then
	INTERACTIVE=0
fi

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
	if [ $INTERACTIVE = 1 ]; then
		sudo git clone https://gitlab.com/mredig/pizza-utils
	else
		git clone https://gitlab.com/mredig/pizza-utils
	fi
fi
cd pizza-utils

if [ $INTERACTIVE = 1 ]; then
	sudo git pull
	sudo ./install.sh
else
	git pull
	./install.sh -f
fi	
