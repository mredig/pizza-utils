#!/usr/bin/env python3

import os
import argparse
import getpass
import subprocess

# assistant to set up secrets in podman or docker.
#
# Simply create a file named `secretlist` and put the name of a secret on each line
# then run `container-secret-setup -s` to initially set up your secrets. If you need to
# change any, run `container-secret-setup -u [secretName]`

def checkIfSecretExists(secretName, toolName):
	# command = f"docker secret inspect '{secretName}'"
	command = [toolName, "secret", "inspect", secretName]
	result = __runCommand(command)
	return result.returncode == 0

def deleteSecret(secretName, toolName):
	# command = f"docker secret rm '{secretName}'"
	command = [toolName, "secret", "rm", secretName]
	result = __runCommand(command)
	return result.returncode == 0

def saveSecret(name, secret, toolName):
	with open('/tmp/pw.tmp', 'w') as f:
		f.write(secret)

	# command = f"docker secret create {name} /tmp/pw.tmp"\
	command = [toolName, "secret", "create", name, "/tmp/pw.tmp"]
	result = __runCommand(command)
	os.remove("/tmp/pw.tmp")
	if result.returncode != 0:
		print(f"Error creating secret {name}")
		exit(1)

def retrieveSecret(secretName, toolName, verify=True):
	secret = getpass.getpass(f"Enter secret for {secretName}: ")

	if verify:
		print(f"Entered value starting with {secret[0]} and ending with {secret[-1]}")

	return secret

def setupSecrets(secretlist, toolName):
	for secretname in secretlist:
		secret = retrieveSecret(secretname, toolName)

		if checkIfSecretExists(secretname, toolName) == False:
			saveSecret(secretname, secret, toolName)
		else:
			print(f"Secret {secretname} already exists. Skipping.")

def updateSecret(secretName, toolName):
	updatedValue = retrieveSecret(secretName, toolName)
	if checkIfSecretExists(secretName, toolName):
		if deleteSecret(secretName, toolName):
			print(f"deleted previous {secretName}")
		else:
			print(f"Error removing existing {secretName}")
			exit(1)
	saveSecret(secretName, updatedValue, toolName)

def isToolInstalled(toolName):
	tests = [["command", "-v"], ["which"]]

	for test in tests:
		command = test
		command.append(toolName)
		try:
			result = __runCommand(command, False)
			return result.returncode == 0
		except Exception as e:
			print(f"exception on command {command}: {e}")
	return False

def getTool(toolName):
	if isToolInstalled(toolName):
		return toolName

	known = set()
	known.add("docker")
	known.add("podman")
	known.remove(toolName)

	for tool in known:
		if isToolInstalled(tool):
			userinput = input(f"{toolName} isn't installed, but {tool} is. Proceed with {tool}? [Y/n]")
			if userinput.lower() != "n":
				return tool
	print(f"Can't find {toolName}. Please try again")
	exit(1)

def __runCommand(command, printOutput=True):
	try:
		result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		if printOutput:
			print(result.stdout)
		return result
	except Exception as e:
		return CompletedProcess()

def pickSecret(validSecrets):
	print("Select a secret to update:")
	for i, name in enumerate(validSecrets):
		print(f"  {i + 1}. {name}")
	while True:
		try:
			choice = int(input("Enter number: "))
			if 1 <= choice <= len(validSecrets):
				return validSecrets[choice - 1]
			print(f"Please enter a number between 1 and {len(validSecrets)}.")
		except ValueError:
			print("Please enter a valid number.")

def main():
	parser = argparse.ArgumentParser(description="Setup secrets")

	parser.add_argument('--setup', "-s", action="store_true", help="Setup secrets initially")
	parser.add_argument('--update', "-u", nargs='?', const='', help="Update a secret by name, or omit value to pick interactively")
	parser.add_argument('--tool', "-t", default="docker", help="Use this tool to manage secrets (must be docker compatible)")

	validSecrets = []
	try:
		with open('secretlist') as f:
			for line in f.readlines():
				validSecrets.append(line.strip())
	except FileNotFoundError as error:
		print("'secretlist' doesn't exist. Please create 'secretlist' with each secret name on a new line.")
		exit(1)

	args = parser.parse_args()
	toolName = args.tool

	toolName = getTool(toolName)

	if args.setup:
		setupSecrets(validSecrets, toolName)
		exit(0)

	if args.update is not None:
		if args.update == '':
			secretName = pickSecret(validSecrets)
		elif args.update in validSecrets:
			secretName = args.update
		else:
			print(f"Unknown secret '{args.update}'. Valid secrets: {', '.join(validSecrets)}")
			exit(1)
		updateSecret(secretName, toolName)
		exit(0)

	print("You must either specify `-s` or `-u [secretname]`.")
	exit(1)


if __name__ == '__main__':
	main()
