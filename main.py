import CLIbrary, openBriefcase, report

import os, sys, time, random, shutil, requests
from colorama import init, Fore, Back, Style
init()

version = "v1.0.0"
production = True

cmdHandler = {}

if "openBriefcase" not in "".join(sys.argv):
	production = False

if production: # Production.
	path = os.getenv("PATH")
	basePath = os.getenv("HOME") + "/"

	installPath = basePath + "Library/openBriefcase/"
	dataPath = installPath + "data/"
	resourcesPath = installPath + "resources/"

	reportsPath = basePath + "Documents/Accounting/Reports/"

else: # Testing.
	basePath = str(os.getcwd()) + "/"

	dataPath = basePath + "data/"
	reportsPath = basePath + "reports/"
	resourcesPath = basePath + "resources/"

helpPath = resourcesPath + "openBriefcaseHelp.json"
accountHelpPath = resourcesPath + "openBriefcaseAccountHelp.json"
reportTemplatePath = resourcesPath + "report.txt"

# Installation
if "install" in sys.argv and "./" in "".join(sys.argv) and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		shutil.copy(currentPath + "openBriefcase", installPath + "openBriefcase")

		if installPath not in path and installPath.replace("openBriefcase/", "openBriefcase") not in path:
			CLIbrary.output({"error": True, "string": "MAKE SURE TO ADD \'" + installPath + "\' TO PATH TO USE IT ANYWHERE"})
		
		CLIbrary.output({"verbose": True, "string": "OPENBRIEFCASE INSTALLED SUCCESFULLY"})
		sys.exit(0)
	
	except(KeyboardInterrupt):
		CLIbrary.output({"error": True, "string": "INSTALLATION ERROR"})
		sys.exit(-1)

try: # Checks folders.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
	if not os.path.exists(reportsPath):
		os.makedirs(reportsPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)
	
except:
	CLIbrary.output({"error": True, "string": "DATA OR RESOURCES ERROR"})

	if production:
		CLIbrary.output({"verbose": True, "string": "TRY REINSTALLING OPENBRIEFCASE"})

	sys.exit(-1)

try: # Checks resources.
	resources = [helpPath, accountHelpPath, reportTemplatePath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)

except:
	CLIbrary.output({"error": True, "string": "RESOURCES ERROR"})

	if production:
		CLIbrary.output({"verbose": True, "string": "TRY REINSTALLING OPENBRIEFCASE"})

	sys.exit(-1)

print(Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL) if production else print(Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL)

print("Accounting utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on https://github.com/diantonioandrea/openBriefcase")
print("Type \'help\' if needed")

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
					sys.exit(-1)
				else:
					continue
		
		user.accounts = userData.accounts
		user.registrationDate = userData.registrationDate

		print("\nWelcome back, " + str(user))
		print("Last login: " + time.strftime("%A, %B %d, %Y at %H:%M", userData.lastLogin) + "\n")
		break

	else:
		if not CLIbrary.boolIn({"request": "User \"" + user.name + "\" does not exist. Would you like to create it?"}):
			if CLIbrary.boolIn({"request": "Exit"}):
				sys.exit(-1)
			continue

		print("\nWelcome, " + str(user) + "\n")
		break

# Check for updates
if production:
	try:
		latestVersion = requests.get("https://github.com/diantonioandrea/openBriefcase/releases/latest").url.split("/")[-1]

		if  latestVersion > version:
			CLIbrary.output({"verbose": True, "string": "UPDATE AVAILABLE: " + version + " \u2192 " + latestVersion, "after": "\n"})

	except:
		CLIbrary.output({"error": True, "string": "COULD NOT CHECK FOR UPDATES"})

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

	cmdHandler["request"] = cmdString

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

	cmdHandler["allowedCommands"] = ["new", "summary", "edit", "remove"]

	if current == None:
		cmdHandler["allowedCommands"] += ["password", "select", "delete", "clear", "report"]

	else:
		cmdHandler["allowedCommands"] += ["load", "dump"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]
	output = command["output"]

	if cmd == "help": # Prints the help.
		print(output)
		continue

	if current == None:
		if cmd == "exit": # Exits the program.
			break

		if cmd == "password": # Toggles the password protection.
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

		if cmd == "new": # Creates a new account.
			newAccount = openBriefcase.account([account.name for account in accounts])

			if CLIbrary.boolIn({"request": "Verify \"" + str(newAccount) + "\""}):
				accounts.append(newAccount)

		if cmd == "summary": # Prints the accounts summary including the latest movements.
			if len(accounts) == 0:
				CLIbrary.output({"error": True, "string": "NOTHING TO SEE HERE"})
				continue

			print("Accounts and latest movements for " + user.name)

			counter = 0

			for account in accounts:
				counter += 1

				print("\n" + str(counter) + ". " + str(account))
				print("\t" + "\n\t".join([str(movement) for movement in account.movements[-3:]]))

			print("\nTotal amount: " + openBriefcase.moneyPrint(sum([account.balance for account in accounts])))

		if cmd == "select": # Swaps the base environment with the selected account enviroment.
			if "n" not in sdOpts:
				CLIbrary.output({"error": True, "string": "MISSING OPTION"})
				continue

			try:
				current = [account for account in accounts if account.name == sdOpts["n"]].pop()

			except:
				CLIbrary.output({"error": True, "string": "ACCOUNT NOT FOUND"})
				current = None

		if cmd == "edit": # Edits an account name.
			if "n" not in sdOpts:
				CLIbrary.output({"error": True, "string": "MISSING OPTION(S)"})
				continue

			try:
				editedAccount = [account for account in accounts if account.name == sdOpts["n"]].pop()
				editedAccount.name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": [account.name for account in accounts]})
				editedAccount.lastModified = time.localtime()

				CLIbrary.output({"verbose": True, "string": "ACCOUNT NAME EDITED"})
				continue

			except:
				CLIbrary.output({"error": True, "string": "ACCOUNT NOT FOUND"})
				continue

		if cmd == "remove": # Removes an account.
			if "n" not in sdOpts:
				CLIbrary.output({"error": True, "string": "MISSING OPTION"})
				continue

			try:
				accounts.remove([account for account in accounts if account.name == sdOpts["n"]].pop())

				CLIbrary.output({"verbose": True, "string": "ACCOUNT REMOVED"})
				continue

			except:
				CLIbrary.output({"error": True, "string": "ACCOUNT NOT FOUND"})
				continue
		
		if cmd == "delete": # Deletes the profile.
			deletionCode = str(random.randint(10**3, 10**4-1))

			if CLIbrary.strIn({"request": "Given that this action is irreversible, insert \"" + deletionCode + "\" to delete your profile"}) == deletionCode:
				os.remove(dataPath + user.name + ".obc")

				CLIbrary.output({"verbose": True, "string": "PROFILE DELETED"})
				break

			CLIbrary.output({"error": True, "string": "WRONG VERIFICATION CODE"})
			continue

		if cmd == "clear": # Clears reports and dumps.
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

		if cmd == "report": # Compiles the report for the selected time range.
			if not len(accounts) or not max([len(account.movements) for account in accounts]):
				CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})
				continue

			report.report(user, sdOpts, ddOpts, reportsPath, reportTemplatePath)
			CLIbrary.output({"verbose": True, "string": "REPORT SAVED TO \'" + reportsPath + "\'"})
			continue
	
	else:
		if cmd == "exit": # Exits the account enviroment.
			current = None
			continue

		if cmd == "new": # Creates a new movement.
			current.addMovement()
			continue

		if cmd == "summary": # Prints the summary for the current account.
			current.summary()
			continue

		if cmd == "edit": # Edits a movement.
			if "c" not in sdOpts or set(ddOpts).intersection({"reason", "amount", "date"}) == set():
				CLIbrary.output({"error": True, "string": "MISSING OPTION(S)"})
				continue

			try:
				editedMovement = [movement for movement in current.movements if movement.code == sdOpts["c"]].pop()

				if "reason" in ddOpts:
					editedMovement.reason = CLIbrary.strIn({"request": "Movement reason", "allowedChars": ["-", "'", ".", ",", ":"]})
				
				if "amount" in ddOpts:
					editedMovement.amount = CLIbrary.numIn({"request": "Movement amount", "round": 2})
				
				if "date" in ddOpts:
					editedMovement.date = CLIbrary.dateIn({"request": "Movement date"})

				editedMovement.lastModified = time.localtime()

				CLIbrary.output({"verbose": True, "string": "MOVEMENT EDITED"})
				continue

			except:
				CLIbrary.output({"error": True, "string": "MOVEMENT NOT FOUND"})
				continue

		if cmd == "remove": # Removes a movement.
			if "c" not in sdOpts:
				CLIbrary.output({"error": True, "string": "MISSING OPTION"})
				continue

			try:
				current.movements.remove([movement for movement in current.movements if movement.code == sdOpts["c"]].pop())

				CLIbrary.output({"verbose": True, "string": "MOVEMENT REMOVED"})
				continue

			except:
				CLIbrary.output({"error": True, "string": "MOVEMENT NOT FOUND"})
				continue
		
		if cmd == "load": # Loads movements from a ".obcm" file.
			oldMovements = len(current.movements)
			loadFiles = [filename for filename in os.listdir(dataPath) if ".obcm" in filename]

			if len(loadFiles) == 0:
				CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})
				continue

			loadFile = CLIbrary.listCh({"list": loadFiles})
			current.load({"path": dataPath + loadFile})

			CLIbrary.output({"verbose": True, "string": "LOADED " + str(len(current.movements) - oldMovements) + " MOVEMENTS FROM " + loadFile})
			continue
	
		if cmd == "dump": # Dumps movements to a ".obcm" file.
			if len(current.movements) == 0:
				CLIbrary.output({"error": True, "string": "NOTHING TO DO HERE"})
				continue

			dumpCodes = [filename.replace(current.name + "_", "").replace(".obcm", "") for filename in os.listdir(dataPath) if ".obcm" in filename]
			dumpCode = openBriefcase.genCode(dumpCodes, 4)

			dumpFile = current.name + "_" + dumpCode + ".obcm"

			current.dump({"path": dataPath + dumpFile}, sdOpts)

			CLIbrary.output({"verbose": True, "string": "DUMPED TO " + dumpFile})
			continue

print("\nGoodbye, " + str(user))