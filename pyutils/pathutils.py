#!/usr/bin/env python3

import pathlib

def extractExtensionFrom(filepath):
	suffix = pathlib.Path(filepath).suffix
	if suffix.startswith("."):
		return suffix[1:]
	else:
		return suffix

def extractFilenameFrom(filepath):
	return pathlib.Path(filepath).stem
