import CLIbrary, openBriefcase, report, os, sys
from colorama import init, Fore, Back, Style

dataPath = str(os.getcwd()) + "/data/"
# helpPath = str(os.getcwd()) + "/openBriefcaseHelp.json"

try: # Check the existence or create the data folder.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
except:
	print(Back.RED + Fore.WHITE + "DATA ERROR" + Style.RESET_ALL)
	sys.exit(-1)

init()

print("openBriefcase")
print("Accounting utility written in Python and built with CLIbrary")
print("Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/openBriefcase\n")

# Login or register

user = openBriefcase.user()

fileHandler = {"path": dataPath + user.name + ".obc"}
userData = CLIbrary.aLoad(fileHandler)

if userData != None:
	if userData.protected:
		if user.login(userData.passwordHash):
			user.protected = True
			user.accounts = userData.accounts

			print("\nWelcome back, " + user.name + "\n")

		else:
			print(Back.RED + Fore.WHITE + "LOGIN ERROR" + Style.RESET_ALL)
			sys.exit(-1)
	
	else:
		user.accounts = userData.accounts
		print("\nWelcome back, " + user.name + "\n")

else:
	print("\nWelcome, " + user.name + "\n")

# Interface

accounts = user.accounts
current = None

while True:
	[account.update() for account in accounts]
	user.accounts.sort(key = lambda entry: entry.balance, reverse=True)

	fileHandler["data"] = user # type: ignore
	CLIbrary.aDump(fileHandler)

	cmdString = user.name + "@openBriefcase"
	if current != None:
		cmdString += ">" + current.name

	cmdHandler = {}
	cmdHandler["request"] = cmdString
	cmdHandler["style"] = Fore.GREEN
	cmdHandler["verboseStyle"] = Back.YELLOW

	cmdHandler["allowedCommands"] = ["new", "summary", "edit", "remove"]

	if current == None:
		cmdHandler["allowedCommands"] += ["password", "select", "report"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]
	output = command["output"]

	if current == None:
		if cmd == "exit":
			break

		if cmd == "password":
			user.register()

			print(cmdHandler["verboseStyle"] + "PASSWORD SET" + Style.RESET_ALL)
			continue

		if cmd == "new":
			newAccount = openBriefcase.account([account.name for account in accounts])

			if CLIbrary.boolIn({"request": "Verify \"" + str(newAccount) + "\""}):
				accounts.append(newAccount)

		if cmd == "summary":
			if len(accounts) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO SEE HERE" + Style.RESET_ALL)
				continue

			print("Accounts for " + user.name + "\n")

			counter = 0

			for account in accounts:
				counter += 1

				print(str(counter) + ". " + str(account))

			print("\nTotal amount: " + openBriefcase.moneyPrint(sum([account.balance for account in accounts])))

		if cmd == "select":
			if "n" not in sdOpts:
				print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
				continue

			try:
				current = [account for account in accounts if account.name == sdOpts["n"]].pop()

			except:
				current = None

		if cmd == "edit":
			if "n" not in sdOpts:
				print(Back.RED + Fore.WHITE + "MISSING OPTION(S)" + Style.RESET_ALL)
				continue

			try:
				[account for account in accounts if account.name == sdOpts["n"]].pop().name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": [account.name for account in accounts]})

				print(cmdHandler["verboseStyle"] + "ACCOUNT NAME EDITED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "ACCOUNT NOT FOUND" + Style.RESET_ALL)
				continue

		if cmd == "remove":
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

		if cmd == "report":
			if len(accounts) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO DO HERE" + Style.RESET_ALL)

			report.report(user, sdOpts)
			continue
	
	else:
		if cmd == "exit":
			current = None
			continue

		if cmd == "new":
			current.addMovement()
			continue

		if cmd == "summary":
			if len(current.movements) == 0:
				print(Back.RED + Fore.WHITE + "NOTHING TO SEE HERE" + Style.RESET_ALL)
				continue

			current.summary()
			continue

		if cmd == "edit":
			if "c" not in sdOpts or set(ddOpts).intersection({"reason", "amount", "date"}) == set():
				print(Back.RED + Fore.WHITE + "MISSING OPTION(S)" + Style.RESET_ALL)
				continue

			try:
				toBeEdited = [movement for movement in current.movements if movement.code == sdOpts["c"]].pop()

				if "reason" in ddOpts:
					toBeEdited.reason = CLIbrary.strIn({"request": "Movement reason"})
				
				if "amount" in ddOpts:
					toBeEdited.amount = CLIbrary.numIn({"request": "Movement amount", "round": 2})
				
				if "date" in ddOpts:
					toBeEdited.date = CLIbrary.dateIn({"request": "Movement date"})

				print(cmdHandler["verboseStyle"] + "MOVEMENT EDITED" + Style.RESET_ALL)
				continue

			except:
				print(Back.RED + Fore.WHITE + "MOVEMENT NOT FOUND" + Style.RESET_ALL)
				continue

		if cmd == "remove":
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