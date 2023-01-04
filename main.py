import CLIbrary, openBriefcase, report

import os, sys, time, random, shutil, requests, platform
from colorama import init, Fore, Back, Style
init()

version = "v1.1.0_dev"
production = True

system = platform.system()
path = os.getenv("PATH")

if "openBriefcase" not in "".join(sys.argv):
	production = False

print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL)

print("Accounting utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on https://github.com/diantonioandrea/openBriefcase")

if production: # Production.
	installPath = os.path.expanduser("~") + "/"
	
	reportsPath = installPath + "Documents/Accounting/Reports/"

	if system == "Darwin":
		installPath += "Library/openBriefcase/"
	
	elif system == "Linux":
		installPath += ".local/bin/openBriefcase/"

	elif system == "Windows":
		installPath += "AppData/Roaming/openBriefcase/"
	
	dataPath = installPath + "data/"
	resourcesPath = installPath + "resources/"

else: # Testing.
	installPath = str(os.getcwd()) + "/"

	dataPath = installPath + "data/"
	reportsPath = installPath + "reports/"
	resourcesPath = installPath + "resources/"

helpPath = resourcesPath + "openBriefcaseHelp.json"
accountHelpPath = resourcesPath + "openBriefcaseAccountHelp.json"
reportTemplatePath = resourcesPath + "report.txt"

# Installation
if "install" in sys.argv and production:
	print() # Empty line needed.

	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		if system != "Windows":
			shutil.copy(currentPath + "openBriefcase", installPath + "openBriefcase")

			if "openBriefcase" not in path: # type: ignore
				CLIbrary.output({"error": True, "string": "MAKE SURE TO ADD \'" + installPath + "\' TO PATH TO USE IT ANYWHERE"})

		else:
			shutil.copy(currentPath + "openBriefcase.exe", installPath + "openBriefcase.exe")

			if "openBriefcase" not in path: # type: ignore
				CLIbrary.output({"error": True, "string": "MAKE SURE TO ADD \'" + installPath + "\' TO PATH TO USE IT ANYWHERE"})
		
		CLIbrary.output({"verbose": True, "string": "OPENBRIEFCASE INSTALLED SUCCESFULLY TO " + installPath, "after": "\n"})
	
	except:
		CLIbrary.output({"error": True, "string": "INSTALLATION ERROR", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

try: # Checks folders.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
	if not os.path.exists(reportsPath):
		os.makedirs(reportsPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)
	
except:
	CLIbrary.output({"error": True, "string": "DATA OR RESOURCES ERROR", "before": "\n"})

	if production:
		CLIbrary.output({"verbose": True, "string": "TRY REINSTALLING OPENBRIEFCASE", "after": "\n"})
	
	else:
		print() # Empty line on exit.

	sys.exit(-1)

try: # Checks resources.
	resources = [helpPath, accountHelpPath, reportTemplatePath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)

except:
	CLIbrary.output({"error": True, "string": "RESOURCES ERROR", "before": "\n"})

	if production:
		CLIbrary.output({"verbose": True, "string": "TRY REINSTALLING OPENBRIEFCASE", "after": "\n"})
	
	else:
		print() # Empty line on exit.

	sys.exit(-1)

# Login or register
while True:
	user = openBriefcase.user()

	fileHandler = {"path": dataPath + user.name + ".obc", "ignoreMissing": True}
	userData = CLIbrary.aLoad(fileHandler)

	if userData != None:
		if userData.protected:
			if user.login(userData.passwordHash):
				user.protected = True

			else:
				CLIbrary.output({"error": True, "string": "LOGIN ERROR"})

				if CLIbrary.boolIn({"request": "Exit"}):
					print() # Empty line on exit.
					sys.exit(-1)
				else:
					continue
		
		user.accounts = userData.accounts
		user.registrationDate = userData.registrationDate

		print("\nWelcome back, " + str(user) + "\nLast login: " + time.strftime("%A, %B %d, %Y at %H:%M", userData.lastLogin))
		break

	else:
		if not CLIbrary.boolIn({"request": "User \"" + user.name + "\" does not exist. Would you like to create it?"}):
			if CLIbrary.boolIn({"request": "Exit"}):
				print() # Empty line on exit.
				sys.exit(-1)
			continue

		print("\nWelcome, " + str(user))
		break

print("Type \'help\' if needed\n")

# Interface
accounts = user.accounts
current = None

while True:
	for account in accounts:
		account.update()

	accounts.sort(key = lambda entry: entry.balance, reverse=True)

	fileHandler["data"] = user # type: ignore
	CLIbrary.aDump(fileHandler)

	# Prompt.
	cmdString = "[" + user.name + "@openBriefcase"
	if current != None:
		cmdString += "/" + current.name
	cmdString += "]"

	cmdHandler = {"request": cmdString}

	# The help that gets printed and the commands depend on the environment.
	if current == None:
		cmdHandler["helpPath"] = helpPath
	
	else:
		cmdHandler["helpPath"] = accountHelpPath

	# The prompt turns red should liquidity go below zero.
	if sum([account.balance for account in accounts]) >= 0:
		cmdHandler["style"] = Fore.GREEN
	
	else:
		cmdHandler["style"] = Fore.RED

	cmdHandler["allowedCommands"] = ["new"]

	if current == None:
		cmdHandler["allowedCommands"] += ["update", "password", "clear", "delete"]

		if len(accounts):
			cmdHandler["allowedCommands"] += ["select", "summary"]

			if max([len(account.movements) for account in accounts]) and system != "Windows":
				cmdHandler["allowedCommands"].append("report")

	else:
		cmdHandler["allowedCommands"] += ["summary", "load"]

		if len(current.movements):
			cmdHandler["allowedCommands"] += ["summary", "dump", "edit", "remove"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]
	output = command["output"]

	# COMMANDS

	if cmd == "help": # Prints the help.
		print(output)
		continue

	if current == None:

		# EXIT

		if cmd == "exit": # Exits the program.
			break

		# UPDATE

		elif cmd == "update": # Checks for updates
			if production:
				try:
					latestVersion = requests.get("https://github.com/diantonioandrea/openBriefcase/releases/latest").url.split("/")[-1]

					if version == latestVersion:
						CLIbrary.output({"verbose": True, "string": "YOU'RE ON THE LATEST VERSION"})
						continue

					elif  version < latestVersion:
						CLIbrary.output({"verbose": True, "string": "UPDATE AVAILABLE: " + version + " \u2192 " + latestVersion})

						if CLIbrary.boolIn({"request": "Would you like to download the latest version?"}):
							if not os.path.exists(installPath + "Downloads/"):
								os.makedirs(installPath + "Downloads/")

							filePath = installPath + "Downloads/openBriefcase.zip"
							url = "https://github.com/diantonioandrea/openBriefcase/releases/download/" + latestVersion + "/openBriefcase-SYSTEM.zip".replace("SYSTEM", system.lower())

							file = open(filePath, "wb")
							file.write(requests.get(url).content)
							file.close()

							CLIbrary.output({"verbose": True, "string": "SAVED TO: " + filePath})
						
						else:
							CLIbrary.output({"erorr": True, "string": "UPDATE IGNORED"})
						
						continue

					elif version > latestVersion:
						CLIbrary.output({"verbose": True, "string": "YOU'RE ON A NEWER VERSION THAN THE LATEST RELEASE"})
						continue

				except:
					CLIbrary.output({"error": True, "string": "UPDATE SYSTEM ERROR"})
					continue
			
			else:
				CLIbrary.output({"error": True, "string": "MUST BE ON PRODUCTION"})
				continue

		# PASSWORD

		elif cmd == "password": # Toggles the password protection.
			if user.protected:
				if user.login(user.passwordHash):
					CLIbrary.output({"verbose": True, "string": "PASSWORD DISABLED"})
					user.protected = False
					user.passwordHash = ""
					continue
					
				else:
					CLIbrary.output({"error": True, "string": "WRONG PASSWORD"})
					continue

			user.register()
			CLIbrary.output({"verbose": True, "string": "PASSWORD SET"})
			continue

		# NEW

		elif cmd == "new": # Creates a new account.
			newAccount = openBriefcase.account([account.name for account in accounts])

			if CLIbrary.boolIn({"request": "Verify \"" + str(newAccount) + "\""}):
				accounts.append(newAccount)
			
			CLIbrary.output({"verbose": True, "string": "NEW ACCOUNT CREATED"})
			continue

		# SUMMARY

		elif cmd == "summary": # Prints the accounts summary including the latest three movements.
			print("Accounts and latest movements for " + user.name)
			print("\n".join(["\n" + str(accounts.index(account) + 1) + ". " + str(account) + ("\n\t" + "\n\t".join([str(movement) for movement in account.movements[-3:]]) if len(account.movements) else "") for account in accounts]))
			print("\nTotal amount: " + openBriefcase.moneyPrint(sum([account.balance for account in accounts])))
			continue

		# DELETE
		
		elif cmd == "delete": # Deletes the profile.
			deletionCode = str(random.randint(10**3, 10**4-1))

			if CLIbrary.strIn({"request": "Given that this action is irreversible, insert \"" + deletionCode + "\" to delete your profile"}) == deletionCode:
				os.remove(dataPath + user.name + ".obc")

				CLIbrary.output({"verbose": True, "string": "PROFILE DELETED"})
				break

			CLIbrary.output({"error": True, "string": "WRONG VERIFICATION CODE"})
			continue

		# CLEAR

		elif cmd == "clear": # Clears reports and dumps.
			reports = os.listdir(reportsPath)
			dumps = [file for file in os.listdir(dataPath) if ".obcm" in file]

			if len(reports):
				if CLIbrary.boolIn({"request": "Clear " + str(len(reports)) + " report(s)?"}):
					for reportFile in reports:
						os.remove(reportsPath + reportFile)
					
					CLIbrary.output({"verbose": True, "string": "CLEARED REPORTS"})

			if len(dumps):
				if CLIbrary.boolIn({"request": "Clear " + str(len(dumps)) + " dump(s)?"}):
					for dumpFile in dumps:
						os.remove(dataPath + dumpFile)
					
					CLIbrary.output({"verbose": True, "string": "CLEARED DUMPS"})

			if not (len(reports) or len(dumps)):
				CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})

			continue

		# REPORT

		elif cmd == "report": # Compiles the report for the selected time range.
			report.report(user, sdOpts, ddOpts, reportsPath, reportTemplatePath)
			CLIbrary.output({"verbose": True, "string": "REPORT SAVED TO \'" + reportsPath + "\'"})
			continue

		# COMMANDS THAT NEED AN ACCOUNT NAME

		if "n" not in sdOpts:
			CLIbrary.output({"error": True, "string": "MISSING OPTION"})
			continue

		else:
			try:
				targetAccount = [account for account in accounts if account.name == sdOpts["n"]].pop()

			except:
				CLIbrary.output({"error": True, "string": "ACCOUNT NOT FOUND"})
				continue

			# SELECT

			if cmd == "select": # Swaps the base environment with the selected account enviroment.
				current = targetAccount
				continue

			# EDIT

			elif cmd == "edit": # Edits an account name.
				targetAccount.name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": [account.name for account in accounts]})
				targetAccount.lastModified = time.localtime()
				continue

			# REMOVE

			elif cmd == "remove": # Removes an account.
				accounts.remove(targetAccount)
				CLIbrary.output({"verbose": True, "string": "ACCOUNT REMOVED"})
				continue
	
	else:

		# EXIT

		if cmd == "exit": # Exits the account enviroment.
			current = None
			continue

		# NEW

		elif cmd == "new": # Creates a new movement.
			current.addMovement()
			continue

		# SUMMARY

		elif cmd == "summary": # Prints the summary for the current account.
			current.summary()
			continue

		# LOAD
		
		elif cmd == "load": # Loads movements from a ".obcm" file.
			oldMovements = len(current.movements)
			loadFiles = [filename for filename in os.listdir(dataPath) if ".obcm" in filename]

			if len(loadFiles) == 0:
				CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})
				continue

			loadFile = CLIbrary.listCh({"list": loadFiles})
			current.load({"path": dataPath + loadFile}) # type: ignore

			CLIbrary.output({"verbose": True, "string": "LOADED " + str(len(current.movements) - oldMovements) + " MOVEMENTS FROM " + loadFile}) # type: ignore			
			continue

		# COMMANDS THAT NEED AT LEAST ONE MOVEMENT

		if len(current.movements) == 0:
			CLIbrary.output({"error": True, "string": "NO MOVEMENTS"})
			continue

		else:

			# EDIT OR REMOVE

			if cmd in ["edit", "remove"]: # Edits or removes a movement.
				if "c" not in sdOpts:
					CLIbrary.output({"error": True, "string": "MISSING OPTION(S)"})
					continue

				try:
					targetMovement = [movement for movement in current.movements if movement.code == sdOpts["c"]].pop()

					if cmd == "edit":
						if set(ddOpts).intersection({"reason", "amount", "date"}) == set():
							CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})
							continue
						
						if "reason" in ddOpts:
							targetMovement.reason = CLIbrary.strIn({"request": "Movement reason", "allowedChars": ["-", "'", ".", ",", ":"]})
						
						if "amount" in ddOpts:
							targetMovement.amount = CLIbrary.numIn({"request": "Movement amount", "round": 2})
						
						if "date" in ddOpts:
							targetMovement.date = CLIbrary.dateIn({"request": "Movement date"})

						targetMovement.lastModified = time.localtime()

						CLIbrary.output({"verbose": True, "string": "MOVEMENT EDITED"})
						continue
					
					if cmd == "remove":
						current.movements.remove(targetMovement)

						CLIbrary.output({"verbose": True, "string": "MOVEMENT REMOVED"})
						continue

				except:
					CLIbrary.output({"error": True, "string": "MOVEMENT NOT FOUND"})
					continue
			
			# DUMP
	
			elif cmd == "dump": # Dumps movements to a ".obcm" file.
				dumpCodes = [filename.replace(current.name + "_", "").replace(".obcm", "") for filename in os.listdir(dataPath) if ".obcm" in filename]
				dumpFile = current.name + "_" + openBriefcase.genCode(dumpCodes, 4) + ".obcm"

				current.dump({"path": dataPath + dumpFile}, sdOpts)

				CLIbrary.output({"verbose": True, "string": "DUMPED TO " + dumpFile})
				continue

print("\nGoodbye, " + str(user) + "\n")