import CLIbrary, bcrypt, random, time
from colorama import Fore, Style

# Utilities

def monthName(monthNumber: str) -> str:
	if monthNumber == "01":
		return "January"
	if monthNumber == "02":
		return "February"
	if monthNumber == "03":
		return "March"
	if monthNumber == "04":
		return "April"
	if monthNumber == "05":
		return "May"
	if monthNumber == "06":
		return "June"
	if monthNumber == "07":
		return "July"
	if monthNumber == "08":
		return "August"
	if monthNumber == "09":
		return "September"
	if monthNumber == "10":
		return "October"
	if monthNumber == "11":
		return "November"
	if monthNumber == "12":
		return "December"

	return ""

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

		self.registrationDate = time.localtime()
		self.lastLogin = self.registrationDate

		self.protected = False
		self.passwordHash = ""

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

		self.creationDate = time.localtime()
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
			CLIbrary.output({"verbose": True, "string": "MOVEMENT ADDED"})
		
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

				for month in months:
					monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
					monthMovements.sort(key = lambda entry: entry.date)

					counter = 0
					print("\n\t" + monthName(month) + ", " + str(len(monthMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in monthMovements])) + "\n")

					for movement in monthMovements:
						counter += 1
						print("\t\t" + str(counter) + ". " + str(movement))
		else:
			CLIbrary.output({"error": True, "string": "NO MOVEMENTS"})

		print("\nOpened with " + moneyPrint(self.start))
		print("Balance: " + moneyPrint(self.balance))

	def load(self, fileHandler: dict):
		loadData = CLIbrary.aLoad(fileHandler)

		try:
			if not bcrypt.checkpw("".join([movement.dump() for movement in loadData["movements"]]).encode(), loadData["hash"]): # type: ignore
				CLIbrary.output({"error": True, "string": "CORRUPTED DATA"})
				return None
		
		except:
			CLIbrary.output({"error": True, "string": "DATA ERROR"})

		newMovements = [movement for movement in loadData["movements"] if movement.code not in [movement.code for movement in self.movements]] # type: ignore

		if len(newMovements) == 0:
			CLIbrary.output({"error": True, "string": "NO LOADABLE MOVEMENTS FOUND"})
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

		dumpData["hash"] = bcrypt.hashpw("".join([movement.dump() for movement in dumpMovements]).encode(), bcrypt.gensalt())
		dumpData["movements"] = dumpMovements

		fileHandler["data"] = dumpData

		CLIbrary.aDump(fileHandler)

class movement:
	def __init__(self, otherCodes: list):
		self.creationDate = time.localtime()
		self.lastModified = self.creationDate

		self.reason = CLIbrary.strIn({"request": "Movement reason", "allowedChars": ["-", "'", ".", ",", ":"]})
		self.amount = CLIbrary.numIn({"request": "Movement amount"})
		self.date = CLIbrary.dateIn({"request": "Movement date"})

		self.code = genCode(otherCodes, 6)

		self.confirmation = CLIbrary.boolIn({"request": "Verify \"" + str(self) + "\""})
	
	def __str__(self):
		return self.date + ", " + self.reason + ": " + moneyPrint(self.amount) + Fore.CYAN + " #" + self.code + Style.RESET_ALL

	def dump(self) -> str:
		# date_reason_amount_code
		return "_".join([self.date, self.reason, str(self.amount), self.code])