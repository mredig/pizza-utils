#!/usr/bin/env sh

# set -x

echo "About to install pizza-utils. Press enter to continue."
read NOTHING

if ! echo $PATH | grep -q "/usr/local/bin"; then
	echo "PATH is missing /usr/local/bin. Please add it to the PATH."
fi

FULLPATH="$(pwd)/$0"
DIR=$(dirname "${FULLPATH}")

pushd "${DIR}"

for FILE in *; do
	if [[ "$FILE" == "install.sh" ]] || [[ "$FILE" == "README.md" ]] || [[ "$FILE" == "remote-install.sh" ]]; then
		continue
	fi

	echo "Installing '${FILE}'"
	chmod +x "${FILE}"
	sudo ln -fs "${DIR}/${FILE}" "/usr/local/bin/"
done
