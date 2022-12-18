import CLIbrary, bcrypt, random
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

def moneyPrint(amount: float) -> str:
	if amount >= 0:
		return Fore.GREEN + str(amount) + "€" + Style.RESET_ALL

	else:
		return Fore.RED + str(amount) + "€" + Style.RESET_ALL

# Classes

class user:
	def __init__(self):
		self.name = CLIbrary.strIn({"request": "User", "noSpace": True})

		self.protected = False
		self.passwordHash = ""

		self.accounts = []

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

		self.balance = self.start
		self.movements = []

	def __str__(self):
		self.update()

		return self.name + ": " + moneyPrint(self.balance)

	def update(self):
		self.balance = self.start

		for movement in self.movements:
			self.balance += movement.amount

		self.movements.sort(key = lambda entry: entry.date)

	def addMovement(self):
		newMovement = movement([movement.code for movement in self.movements])

		if newMovement.confirmation:
			self.movements.append(newMovement)

		self.update()

	def summary(self):
		print("Summary for " + str(self))
		print("Opened with " + moneyPrint(self.start) + "\n")

		print("\nFormat: DATE, REASON: AMOUNT #CODE\n")

		years = set([movement.date.split("-")[0] for movement in self.movements])
		years = list(years)
		years.sort()

		for year in years:
			yearMovements = [movement for movement in self.movements if year in movement.date]

			months = set([movement.date.split("-")[1] for movement in yearMovements])
			months = list(months)
			months.sort()

			print(year + ", " + str(len(yearMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in yearMovements])))

			for month in months:
				monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
				monthMovements.sort(key = lambda entry: entry.reason)

				counter = 0
				print("\n\t" + monthName(month) + ", " + str(len(monthMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in monthMovements])) + "\n")

				for movement in monthMovements:
					counter += 1
					print("\t\t" + str(counter) + ". " + str(movement))
			
class movement:
	def __init__(self, otherCodes: list):
		self.reason = CLIbrary.strIn({"request": "Movement reason"})
		self.amount = CLIbrary.numIn({"request": "Movement amount"})
		self.date = CLIbrary.dateIn({"request": "Movement date"})

		while True:
			self.code = str(random.randint(10**6, 10**7-1))

			if self.code not in otherCodes:
				break

		self.confirmation = CLIbrary.boolIn({"request": "Verify \"" + str(self) + "\""})

	def __str__(self):
		return self.date + ", " + self.reason + ": " + moneyPrint(self.amount) + Fore.CYAN + " #" + self.code + Style.RESET_ALL