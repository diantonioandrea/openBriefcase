import bcrypt, random, CLIbrary
from colorama import Fore, Style
from datetime import datetime

# Utilities

def moneyPrint(amount: float) -> str:
	if amount >= 0:
		return Fore.GREEN + "+" + str(round(amount, 2)) + "€" + Style.RESET_ALL

	else:
		return Fore.RED + str(round(amount, 2)) + "€" + Style.RESET_ALL

def genCode(otherCodes: list, length: int) -> str:
	characters = list(range(48, 58)) + list(range(97, 123))

	while True:
		code = "".join([chr(random.choice(characters)) for _ in range(length)])

		if code not in otherCodes:
			return code

# Classes

class user:
	def __init__(self):
		self.name = CLIbrary.strIn({"request": "\nUser", "noSpace": True})

		self.registrationDate = datetime.now()
		self.lastLogin = self.registrationDate

		self.protected = False
		self.passwordHash = ""

		self.darkTheme = False

		self.accounts = []
	
	def __str__(self):
		return self.name

	def login(self, passwordHash):
		password = CLIbrary.strIn({"request": "Password", "noSpace": True, "fixedLength": 8})
		self.passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		return bcrypt.checkpw(password.encode(), passwordHash)

	def register(self):
		self.passwordHash = bcrypt.hashpw(CLIbrary.strIn({"request": "Password", "noSpace": True, "verification": True, "fixedLength": 8}).encode(), bcrypt.gensalt())
		self.protected = True

class account:
	def __init__(self, otherNames: list):
		self.name = CLIbrary.strIn({"request": "Account name", "noSpace": True, "blockedAnswers": otherNames})
		self.start = CLIbrary.numIn({"request": "Starting balance"})

		self.creationDate = datetime.now()
		self.lastModified = self.creationDate

		self.balance = self.start
		self.movements = []

	def __str__(self):
		self.update()
		return self.name + ": " + moneyPrint(self.balance)

	def update(self):
		self.balance = self.start + sum([movement.amount for movement in self.movements])
		self.movements.sort(key = lambda entry: entry.date)

	def addMovement(self):
		newMovement = movement([movement.code for movement in self.movements])

		if newMovement.confirmation:
			self.movements.append(newMovement)
			CLIbrary.output({"type": "verbose", "string": "MOVEMENT ADDED"})
		
		self.update()

	def summary(self):
		print("Summary for: " + self.name + "\n")

		if len(self.movements) != 0:
			print("Account movements [DATE, REASON: AMOUNT #CODE]: ")

			years = set([movement.date.split("-")[0] for movement in self.movements])
			years = list(years)
			years.sort()

			for year in years:
				yearMovements = [movement for movement in self.movements if year in movement.date]

				months = set([movement.date.split("-")[1] for movement in yearMovements])
				months = list(months)
				months.sort()

				print("\n" + year + ", " + str(len(yearMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in yearMovements])))
				print("\n\tMovements by category:\n")

				categories = {movement.category for movement in yearMovements}
				categories = list(categories)
				categories.sort()

				if "others" in categories:
					categories.remove("others")
					categories = ["others"] + categories

				for category in categories:
					print("\t\t" + Fore.BLUE + category + Style.RESET_ALL + ": " + str(moneyPrint(sum([movement.amount for movement in yearMovements if movement.category == category]))))

				for month in months:
					monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
					monthMovements.sort(key = lambda entry: entry.date)

					counter = 0
					print("\n\t" + datetime.strptime(month, "%m").strftime('%B') + ", " + str(len(monthMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in monthMovements])) + "\n")

					for movement in monthMovements:
						counter += 1
						print("\t\t" + str(counter) + ". " + str(movement))

		else:
			CLIbrary.output({"type": "warning", "string": "NO MOVEMENTS"})

		print("\nOpened with " + moneyPrint(self.start))
		print("Balance: " + moneyPrint(self.balance))

	def load(self, fileHandler: dict):
		loadData = CLIbrary.aLoad(fileHandler)

		try:
			if not bcrypt.checkpw("-".join([movement.dump() for movement in loadData["movements"]]).encode(), loadData["hash"]):
				CLIbrary.output({"type": "error", "string": "CORRUPTED DATA"})
				return None
		
		except:
			CLIbrary.output({"type": "error", "string": "DATA ERROR"})

		newMovements = [movement for movement in loadData["movements"] if movement.code not in [movement.code for movement in self.movements]]

		if len(newMovements) == 0:
			CLIbrary.output({"type": "error", "string": "NO LOADABLE MOVEMENTS FOUND"})
			return None

		if CLIbrary.boolIn({"request": "Found " + str(len(newMovements)) + " loadable movement(s): \n\n" + "\n".join([str(movement) for movement in newMovements]) + "\n\nLoad the found movement(s)?"}):
			self.movements += newMovements

		self.update()

	def dump(self, fileHandler: dict, sdOpts):
		dumpData = dict()
		dumpMovements = [movement for movement in self.movements]

		if "s" in sdOpts:
			try:
				dumpMovements = [movement for movement in dumpMovements if movement.date >= sdOpts["s"]]
			except:
				pass

		if "e" in sdOpts:
			try:
				dumpMovements = [movement for movement in dumpMovements if movement.date <= sdOpts["s"]]
			except:
				pass

		dumpData["hash"] = bcrypt.hashpw("-".join([movement.dump() for movement in dumpMovements]).encode(), bcrypt.gensalt())
		dumpData["movements"] = dumpMovements

		fileHandler["data"] = dumpData

		CLIbrary.aDump(fileHandler)

class movement:
	def __init__(self, otherCodes: list):
		self.creationDate = datetime.now()
		self.lastModified = self.creationDate

		self.reason = CLIbrary.strIn({"request": "Movement reason", "allowedChars": ["-", "'", ".", ",", ":"]})
		self.amount = CLIbrary.numIn({"request": "Movement amount"})
		self.date = CLIbrary.dateIn({"request": "Movement date"})

		self.setCategory()

		self.code = genCode(otherCodes, 6)

		self.confirmation = CLIbrary.boolIn({"request": "Verify \"" + str(self) + "\""})
	
	def setCategory(self) -> None:
		categories = ["home", "food", "transports", "travel", "school", "work", "hobbies", "health"]
		categories.sort()

		self.category = CLIbrary.listCh({"request": "Movement category, by index", "list": ["others"] + categories})

	def __str__(self) -> str:
		return self.date + ", " + self.reason + ": " + moneyPrint(self.amount) + Fore.BLUE + " " + self.category + Style.RESET_ALL + Fore.CYAN + " #" + self.code + Style.RESET_ALL

	def dump(self) -> str: # For consistency reasons.
		# date_reason_amount_category_code
		return "_".join([self.date, self.reason, str(self.amount), self.category, self.code])