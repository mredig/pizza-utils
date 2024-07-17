#!/usr/bin/env sh

# set -x

INTERACTIVE=1
if [ $1 = "-f" ]; then
	INTERACTIVE=0
fi

if [ $INTERACTIVE = 1 ]; then
	echo "About to install pizza-utils. Press enter to continue."
	read NOTHING
fi

if ! echo $PATH | grep -q "/usr/local/bin"; then
	echo "PATH is missing /usr/local/bin. Please add it to the PATH."
fi

FULLPATH="$(pwd)/$0"
DIR=$(dirname "${FULLPATH}")

cd "${DIR}" || exit 1

for FILE in *; do
	if [ "$FILE" = "install.sh" ] || [ "$FILE" = "README.md" ] || [ "$FILE" = "remote-install.sh" ]; then
		echo "Skipping ${FILE}"
		continue
	fi

	echo "Installing '${FILE}'"
	chmod +x "${FILE}"
	if [ $INTERACTIVE = 1 ]; then
		sudo ln -fs "${DIR}/${FILE}" "/usr/local/bin/"
	else
		ln -fs "${DIR}/${FILE}" "/usr/local/bin/"
	fi
done
