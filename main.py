import CLIbrary, openBriefcase, report

import os, sys, time, random, shutil
from colorama import init, Fore, Back, Style
init()

version = "1.0.0"
production = True

cmdHandler = {}
cmdHandler["verboseStyle"] = Back.YELLOW

if "openBriefcase" not in "".join(sys.argv):
	production = False

if production: # Production.
	path = os.getenv("PATH")
	basePath = os.getenv("HOME")

	dataPath = basePath + "/Library/openBriefcase" + "/data/"
	resourcesPath = basePath + "/Library/openBriefcase" + "/resources/"
	reportsPath = basePath + "/Documents/Accounting/Reports/"
	installPath = basePath + "/Documents/Accounting/"

else: # Testing.
	basePath = str(os.getcwd())

	dataPath = basePath + "/data/"
	reportsPath = basePath + "/reports/"
	resourcesPath = basePath + "/resources/"

helpPath = resourcesPath + "openBriefcaseHelp.json"
accountHelpPath = resourcesPath + "openBriefcaseAccountHelp.json"
reportTemplatePath = resourcesPath + "report.txt"

if "install" in sys.argv and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		shutil.copy(currentPath + "openBriefcase", installPath + "openBriefcase")

		if installPath not in path:
			print(Back.RED + Fore.WHITE + "MAKE SURE TO ADD \'" + installPath + "\' TO PATH" + Style.RESET_ALL)
		
		print(cmdHandler["verboseStyle"] + "OPENBRIEFCASE INSTALLED SUCCESFULLY" + Style.RESET_ALL)
		sys.exit(0)
	
	except(KeyboardInterrupt):
		print(Back.RED + Fore.WHITE + "INSTALLATION ERROR" + Style.RESET_ALL)
		sys.exit(-1)

try: # Checks folders.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
	if not os.path.exists(reportsPath):
		os.makedirs(reportsPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)
	
except:
	print(Back.RED + Fore.WHITE + "DATA OR RESOURCES ERROR" + Style.RESET_ALL)

	if production:
		print(Back.RED + Fore.WHITE + "TRY REINSTALLING OPENBRIEFCASE" + Style.RESET_ALL)

	sys.exit(-1)

try: # Checks resources.
	resources = [helpPath, accountHelpPath, reportTemplatePath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)

except:
	print(Back.RED + Fore.WHITE + "RESOURCES ERROR" + Style.RESET_ALL)

	if production:
		print(Back.RED + Fore.WHITE + "TRY REINSTALLING OPENBRIEFCASE" + Style.RESET_ALL)

	sys.exit(-1)

print(Fore.MAGENTA + "openBriefcase" + Style.RESET_ALL + " v" + version) if production else print("openBriefcase")
print("Accounting utility written in Python and built with CLIbrary")
print("Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/openBriefcase")
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
				print(Back.RED + Fore.WHITE + "LOGIN ERROR" + Style.RESET_ALL)

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

	# The prompt turns red should the liquidity go below zero.
	if sum([account.balance for account in accounts]) >= 0:
		cmdHandler["style"] = Fore.GREEN
	
	else:
		cmdHandler["style"] = Fore.RED

	# The help that gets printed, as do the commands, depends on the environment.
	if current == None:
		cmdHandler["helpPath"] = helpPath
	
	else:
		cmdHandler["helpPath"] = accountHelpPath

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
					print(cmdHandler["verboseStyle"] + "PASSWORD DISABLED" + Style.RESET_ALL)
					user.protected = False
					user.passwordHash = ""
					continue
					
				else:
					print(Back.RED + Fore.WHITE + "WRONG PASSWORD" + Style.RESET_ALL)
					continue

			user.register()
			print(cmdHandler["verboseStyle"] + "PASSWORD SET" + Style.RESET_ALL)
			continue

		if cmd == "new": # Creates a new account.
			newAccount = openBriefcase.account([account.name for account in accounts])

			if CLIbrary.boolIn({"request": "Verify \"" + str(newAccount) + "\""}):
				accounts.append(newAccount)

		if cmd == "summary": # Prints the accounts summary including the latest movements.
			if len(accounts) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO SEE HERE" + Style.RESET_ALL)
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
				print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
				continue

			try:
				current = [account for account in accounts if account.name == sdOpts["n"]].pop()

			except:
				print(Back.RED + Fore.WHITE + "ACCOUNT NOT FOUND" + Style.RESET_ALL)
				current = None

		if cmd == "edit": # Edits an account name.
			if "n" not in sdOpts:
				print(Back.RED + Fore.WHITE + "MISSING OPTION(S)" + Style.RESET_ALL)
				continue

			try:
				editedAccount = [account for account in accounts if account.name == sdOpts["n"]].pop()
				editedAccount.name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": [account.name for account in accounts]})
				editedAccount.lastModified = time.localtime()

				print(cmdHandler["verboseStyle"] + "ACCOUNT NAME EDITED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "ACCOUNT NOT FOUND" + Style.RESET_ALL)
				continue

		if cmd == "remove": # Removes an account.
			if "n" not in sdOpts:
				print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
				continue

			try:
				accounts.remove([account for account in accounts if account.name == sdOpts["n"]].pop())

				print(cmdHandler["verboseStyle"] + "ACCOUNT REMOVED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "ACCOUNT NOT FOUND" + Style.RESET_ALL)
				continue
		
		if cmd == "delete": # Deletes the profile.
			deletionCode = str(random.randint(10**3, 10**4-1))

			if CLIbrary.strIn({"request": "Given that this action is irreversible, insert \"" + deletionCode + "\" to delete your profile"}) == deletionCode:
				os.remove(dataPath + user.name + ".obc")
				print(cmdHandler["verboseStyle"] + "PROFILE DELETED" + Style.RESET_ALL)
				break

			print(Back.RED + Fore.WHITE + "WRONG CODE" + Style.RESET_ALL)
			continue

		if cmd == "clear": # Clears reports and dumps.
			reports = os.listdir(reportsPath)
			dumps = [file for file in os.listdir(dataPath) if ".obcm" in file]

			if len(reports):
				if CLIbrary.boolIn({"request": "Clear " + str(len(reports)) + " report(s)?"}):
					for reportFile in reports:
						os.remove(reportsPath + reportFile)
					
					print(cmdHandler["verboseStyle"] + "CLEARED REPORTS" + Style.RESET_ALL)

			if len(dumps):
				if CLIbrary.boolIn({"request": "Clear " + str(len(dumps)) + " dump(s)?"}):
					for dumpFile in dumps:
						os.remove(dataPath + dumpFile)
					
					print(cmdHandler["verboseStyle"] + "CLEARED DUMPS" + Style.RESET_ALL)

			if not (len(reports) or len(dumps)):
				print(Back.RED + Fore.WHITE + "NOTHING TO CLEAR" + Style.RESET_ALL)

			continue

		if cmd == "report": # Compiles the report for the selected time range.
			if not len(accounts) or not max([len(account.movements) for account in accounts]):
				print(Back.RED + Fore.WHITE + "NOTHING TO DO HERE" + Style.RESET_ALL)
				continue

			report.report(user, sdOpts, ddOpts, reportsPath, reportTemplatePath)
			print(cmdHandler["verboseStyle"] + "REPORT SAVED TO \'" + reportsPath + "\'" + Style.RESET_ALL)
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
				print(Back.RED + Fore.WHITE + "MISSING OPTION(S)" + Style.RESET_ALL)
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

				print(cmdHandler["verboseStyle"] + "MOVEMENT EDITED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "MOVEMENT NOT FOUND" + Style.RESET_ALL)
				continue

		if cmd == "remove": # Removes a movement.
			if "c" not in sdOpts:
				print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
				continue

			try:
				current.movements.remove([movement for movement in current.movements if movement.code == sdOpts["c"]].pop())

				print(cmdHandler["verboseStyle"] + "MOVEMENT REMOVED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "MOVEMENT NOT FOUND" + Style.RESET_ALL)
				continue
		
		if cmd == "load": # Loads movements from a ".obcm" file.
			oldMovements = len(current.movements)
			loadFiles = [filename for filename in os.listdir(dataPath) if ".obcm" in filename]

			if len(loadFiles) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO LOAD" + Style.RESET_ALL)
				continue

			loadFile = CLIbrary.listCh({"list": loadFiles})
			current.load({"path": dataPath + loadFile})

			print(cmdHandler["verboseStyle"] + "LOADED " + str(len(current.movements) - oldMovements) + " MOVEMENTS FROM " + loadFile + Style.RESET_ALL)
			continue
	
		if cmd == "dump": # Dumps movements to a ".obcm" file.
			if len(current.movements) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO DUMP" + Style.RESET_ALL)
				continue

			dumpCodes = [filename.replace(current.name + "_", "").replace(".obcm", "") for filename in os.listdir(dataPath) if ".obcm" in filename]
			dumpCode = openBriefcase.genCode(dumpCodes, 4)

			dumpFile = current.name + "_" + dumpCode + ".obcm"

			current.dump({"path": dataPath + dumpFile}, sdOpts)
			print(cmdHandler["verboseStyle"] + "DUMPED TO " + dumpFile + Style.RESET_ALL)
			continue

print("\nGoodbye, " + str(user))