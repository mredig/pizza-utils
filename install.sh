#!/usr/bin/env sh

if ! echo $PATH | grep -q "/usr/local/bin"; then
	echo "PATH is missing /usr/local/bin. Please add it to the PATH."
fi

FULLPATH="$(pwd)/$0"
DIR=$(dirname "${FULLPATH}")

pushd "${DIR}"

for FILE in *; do
	if [[ "$FILE" == "install.sh" ]]; then
		continue
	fi

	chmod +x "${FILE}"
	sudo ln -fs "${DIR}/${FILE}" "/usr/local/bin/temp/"
done
