import openBriefcase, report
import os, sys, random, shutil, requests, platform, zipfile, CLIbrary
from colorama import Fore, Back, Style
from datetime import datetime

# ---
# From an answer of Ciro Santilli on https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
import stat

def get_umask():
    umask = os.umask(0)
    os.umask(umask)

    return umask

def executable(filePath):
    os.chmod(filePath, os.stat(filePath).st_mode | ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & ~get_umask()))
# ---

version = "v1.4.0_dev"
production = True
if "openBriefcase" not in "".join(sys.argv): # Local testing.
	production = False

system = platform.system()
path = os.getenv("PATH")

print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.MAGENTA + " openBriefcase " + Style.RESET_ALL)
print("Accounting utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on https://github.com/diantonioandrea/openBriefcase")

# PATHS

if production: # Production.
	homePath = os.path.expanduser("~") + "/"
	installPath = homePath
	
	if system == "Darwin":
		installPath += "Library/openBriefcase/"
	
	elif system == "Linux":
		installPath += ".local/bin/openBriefcase/"

	elif system == "Windows":
		installPath += "AppData/Roaming/openBriefcase/"

	reportsPath = homePath + "Documents/Accounting/Reports/"

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

# INSTALLATION

if "install" in sys.argv and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		if system != "Windows":
			shutil.copy(currentPath + "openBriefcase", installPath + "openBriefcase")

		else:
			shutil.copy(currentPath + "openBriefcase.exe", installPath + "openBriefcase.exe")
		
		CLIbrary.output({"type": "verbose", "string": "OPENBRIEFCASE INSTALLED SUCCESFULLY TO " + installPath, "before": "\n"})

		if "openBriefcase" not in path: # type: ignore
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO ADD ITS INSTALLATION DIRECTORY TO PATH TO USE IT ANYWHERE", "after": "\n"})
		
		else:
			print() # Empty line on exit.
	
	except:
		CLIbrary.output({"type": "error", "string": "INSTALLATION ERROR", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

# UPDATE

if production:
	updateFlag = False

	try:
		latestVersion = requests.get("https://github.com/diantonioandrea/openBriefcase/releases/latest").url.split("/")[-1]

		if  version < latestVersion or (latestVersion in version and "_dev" in version):
			CLIbrary.output({"type": "verbose", "string": "UPDATE AVAILABLE: " + version + " \u2192 " + latestVersion, "before": "\n"})

			if CLIbrary.boolIn({"request": "Would you like to download the latest version?"}):
				tempPath = installPath + "temp/"

				if not os.path.exists(tempPath):
					os.makedirs(tempPath)

				filePath = tempPath + "openBriefcase-SYSTEM.zip".replace("SYSTEM", system.lower())
				url = "https://github.com/diantonioandrea/openBriefcase/releases/download/" + latestVersion + "/openBriefcase-SYSTEM.zip".replace("SYSTEM", system.lower())

				file = open(filePath, "wb")
				file.write(requests.get(url).content)
				file.close()

				updatePackage = zipfile.ZipFile(filePath, "r")
				updatePackage.extractall(tempPath)

				for file in os.listdir(tempPath + "resources/"):
					shutil.copy(tempPath + "resources/" + file, resourcesPath + file)

				if system != "Windows":
					shutil.copy(tempPath + "openBriefcase", installPath + "openBriefcase")
					executable(installPath + "openBriefcase")

				else:
					shutil.copy(tempPath + "openBriefcase.exe", installPath + "openBriefcase.exe")
					executable(installPath + "openBriefcase.exe")

				updateFlag = True
				shutil.rmtree(tempPath)
				CLIbrary.output({"type": "verbose", "string": "UPDATED TO: " + latestVersion})
			
			else:
				CLIbrary.output({"type": "verbose", "string": "UPDATE IGNORED"})

	except(requests.exceptions.RequestException):
		CLIbrary.output({"type": "error", "string": "COULDN'T CHECK FOR UPDATES", "before": "\n"})

	except:
		CLIbrary.output({"type": "error", "string": "UPDATE MAY HAVE FAILED", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		if updateFlag:
			CLIbrary.output({"type": "verbose", "string": "THE PROGRAM HAS BEEN CLOSED TO COMPLETE THE UPDATE", "after": "\n"})
			sys.exit(0)

# CHECKS

try:
	# Folders.

	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
	if not os.path.exists(reportsPath):
		os.makedirs(reportsPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)

	# Resources

	resources = [helpPath, accountHelpPath, reportTemplatePath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)
	
except:
	if production:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR, TRY REINSTALLING OPENBRIEFCASE", "before": "\n", "after": "\n"})
	
	else:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR", "before": "\n", "after": "\n"})

	sys.exit(-1)

# LOGIN OR REGISTER

while True:
	user = openBriefcase.user()

	fileHandler = {"path": dataPath + user.name + ".obc", "ignoreMissing": True}
	userData = CLIbrary.aLoad(fileHandler)

	if userData != None:
		if userData.protected:
			if user.login(userData.passwordHash):
				user.protected = True

			else:
				CLIbrary.output({"type": "error", "string": "LOGIN ERROR"})

				if CLIbrary.boolIn({"request": "Exit"}):
					print() # Empty line on exit.
					sys.exit(-1)
				else:
					continue
		
		user.accounts = userData.accounts
		user.registrationDate = userData.registrationDate

		# TIME FIX, SOLVES BREAKS FROM 1.2.0 (time) TO 1.3.0 (datetime)

		import time

		user.registrationDate = datetime.fromtimestamp(time.mktime(user.registrationDate)) if type(user.registrationDate) == time.struct_time else user.registrationDate
		userData.lastLogin = datetime.fromtimestamp(time.mktime(userData.lastLogin)) if type(userData.lastLogin) == time.struct_time else userData.lastLogin

		for account in user.accounts:
			account.creationDate = datetime.fromtimestamp(time.mktime(account.creationDate)) if type(account.creationDate) == time.struct_time else account.creationDate
			account.lastModified = datetime.fromtimestamp(time.mktime(account.lastModified)) if type(account.lastModified) == time.struct_time else account.lastModified

			for movement in account.movements:
				movement.creationDate = datetime.fromtimestamp(time.mktime(movement.creationDate)) if type(movement.creationDate) == time.struct_time else movement.creationDate
				movement.lastModified = datetime.fromtimestamp(time.mktime(movement.lastModified)) if type(movement.lastModified) == time.struct_time else movement.lastModified

		# END OF FIX

		print("\nWelcome back, " + str(user) + "\nLast login: " + userData.lastLogin.strftime("%A, %B %d, %Y at %H:%M"))
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

# INTERFACE

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

	# Prompt turns red should liquidity go below zero.
	if sum([account.balance for account in accounts]) >= 0:
		cmdHandler["style"] = Fore.GREEN
	
	else:
		cmdHandler["style"] = Fore.RED

	cmdHandler["allowedCommands"] = ["new"]

	if current == None:
		cmdHandler["allowedCommands"] += ["password", "clear", "delete"]

		if len(accounts):
			cmdHandler["allowedCommands"] += ["select", "summary", "edit", "remove"]

			# Reports not working on Windows.
			if max([len(account.movements) for account in accounts]) and system != "Windows":
				cmdHandler["allowedCommands"].append("report")

	else:
		cmdHandler["allowedCommands"] += ["summary", "load"]

		if len(current.movements):
			cmdHandler["allowedCommands"] += ["dump", "edit", "remove"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]

	# COMMANDS

	if current == None:

		# EXIT

		if cmd == "exit": # Exits the program.
			break

		# PASSWORD

		elif cmd == "password": # Toggles the password protection.
			if user.protected:
				if user.login(user.passwordHash):
					CLIbrary.output({"type": "verbose", "string": "PASSWORD DISABLED"})
					user.protected = False
					user.passwordHash = ""
					continue
					
				else:
					CLIbrary.output({"type": "error", "string": "WRONG PASSWORD"})
					continue

			user.register()
			CLIbrary.output({"type": "verbose", "string": "PASSWORD SET"})
			continue

		# NEW

		elif cmd == "new": # Creates a new account.
			newAccount = openBriefcase.account([account.name for account in accounts])

			if CLIbrary.boolIn({"request": "Verify \"" + str(newAccount) + "\""}):
				accounts.append(newAccount)
			
			CLIbrary.output({"type": "verbose", "string": "NEW ACCOUNT CREATED"})
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

				CLIbrary.output({"type": "verbose", "string": "PROFILE DELETED"})
				break

			CLIbrary.output({"type": "error", "string": "WRONG VERIFICATION CODE"})
			continue

		# CLEAR

		elif cmd == "clear": # Clears reports and dumps.
			reports = os.listdir(reportsPath)
			dumps = [file for file in os.listdir(dataPath) if ".obcm" in file]

			if len(reports):
				if CLIbrary.boolIn({"request": "Clear " + str(len(reports)) + " report(s)?"}):
					for reportFile in reports:
						os.remove(reportsPath + reportFile)
					
					CLIbrary.output({"type": "verbose", "string": "CLEARED REPORTS"})

			if len(dumps):
				if CLIbrary.boolIn({"request": "Clear " + str(len(dumps)) + " dump(s)?"}):
					for dumpFile in dumps:
						os.remove(dataPath + dumpFile)
					
					CLIbrary.output({"type": "verbose", "string": "CLEARED DUMPS"})

			if not (len(reports) or len(dumps)):
				CLIbrary.output({"type": "error", "string": "NOTHING TO DO HERE"})

			continue

		# REPORT

		elif cmd == "report": # Compiles the report for the selected time range.
			report.report(user, sdOpts, ddOpts, reportsPath, reportTemplatePath)
			CLIbrary.output({"type": "verbose", "string": "REPORT SAVED TO \'" + reportsPath + "\'"})
			continue

		# COMMANDS THAT NEED AN ACCOUNT NAME

		if "n" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

		else:
			try:
				targetAccount = [account for account in accounts if account.name == sdOpts["n"]].pop()

			except:
				CLIbrary.output({"type": "error", "string": "ACCOUNT NOT FOUND"})
				continue

			# SELECT

			if cmd == "select": # Swaps the base environment with the selected account enviroment.
				current = targetAccount
				continue

			# EDIT

			elif cmd == "edit": # Edits an account name.
				targetAccount.name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": [account.name for account in accounts]})
				targetAccount.lastModified = datetime.now()
				continue

			# REMOVE

			elif cmd == "remove": # Removes an account.
				accounts.remove(targetAccount)
				CLIbrary.output({"type": "verbose", "string": "ACCOUNT REMOVED"})
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
				CLIbrary.output({"type": "error", "string": "NOTHING TO DO HERE"})
				continue

			loadFile = CLIbrary.listCh({"list": loadFiles})
			current.load({"path": dataPath + loadFile}) # type: ignore

			CLIbrary.output({"type": "verbose", "string": "LOADED " + str(len(current.movements) - oldMovements) + " MOVEMENTS FROM " + loadFile}) # type: ignore			
			continue

		# COMMANDS THAT NEED AT LEAST ONE MOVEMENT

		if len(current.movements) == 0:
			CLIbrary.output({"type": "error", "string": "NO MOVEMENTS"})
			continue

		else:

			# EDIT OR REMOVE

			if cmd in ["edit", "remove"]: # Edits or removes a movement.
				if "c" not in sdOpts:
					CLIbrary.output({"type": "error", "string": "MISSING OPTION(S)"})
					continue

				try:
					targetMovement = [movement for movement in current.movements if movement.code == sdOpts["c"]].pop()

					if cmd == "edit":
						if set(ddOpts).intersection({"reason", "amount", "date"}) == set():
							CLIbrary.output({"type": "error", "string": "NOTHING TO DO HERE"})
							continue
						
						if "reason" in ddOpts:
							targetMovement.reason = CLIbrary.strIn({"request": "Movement reason", "allowedChars": ["-", "'", ".", ",", ":"]})
						
						if "amount" in ddOpts:
							targetMovement.amount = CLIbrary.numIn({"request": "Movement amount", "round": 2})
						
						if "date" in ddOpts:
							targetMovement.date = CLIbrary.dateIn({"request": "Movement date"})

						targetMovement.lastModified = datetime.now()

						CLIbrary.output({"type": "verbose", "string": "MOVEMENT EDITED"})
						continue
					
					if cmd == "remove":
						current.movements.remove(targetMovement)

						CLIbrary.output({"type": "verbose", "string": "MOVEMENT REMOVED"})
						continue

				except:
					CLIbrary.output({"type": "error", "string": "MOVEMENT NOT FOUND"})
					continue
			
			# DUMP
	
			elif cmd == "dump": # Dumps movements to a ".obcm" file.
				dumpCodes = [filename.replace(current.name + "_", "").replace(".obcm", "") for filename in os.listdir(dataPath) if ".obcm" in filename]
				dumpFile = current.name + "_" + openBriefcase.genCode(dumpCodes, 4) + ".obcm"

				current.dump({"path": dataPath + dumpFile}, sdOpts)

				CLIbrary.output({"type": "verbose", "string": "DUMPED TO \'" + dumpFile + "\'"})
				continue

print("\nGoodbye, " + str(user) + "\n")