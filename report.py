from pdflatex import PDFLaTeX
from colorama import Fore, Back, Style
import os, sys, time

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
		return "\\color{solarized-green} \\Plus" + str(round(amount, 2)) + "€ \\color{solarized-base02}"

	else:
		return "\\color{solarized-red} \\Minus" + str(round(-amount, 2)) + "€ \\color{solarized-base02}"

def report(user, sdOpts: dict, ddOpts: list, reportsPath: str, resourcesPath: str) -> None:
	accounts = user.accounts

	accountSummary = ["\\subsection*{User}"]
	accountSummary += [" \\newline\n".join(["Username: " + str(user), "Liquidity: " + moneyPrint(sum(account.balance for account in accounts)), "Registration date: " + time.strftime("%A, %B %d, %Y at %H:%M", user.registrationDate)])]

	accountSummary += ["\\subsection*{Accounts}"]
	accountSummary += ["\n".join(["\\begin{description}", "\n".join(["\t\\item[" + account.name[0].upper() + account.name[1:] + "] " + str(len(account.movements)) + " registered movement(s), opened with: " + moneyPrint(account.start) + " and with a current balance of: " + moneyPrint(account.balance) for account in accounts]), "\\end{description}"])]

	accountReports = []

	start = ""
	end = ""

	if "s" in sdOpts: # Start date
		start = sdOpts["s"]

	if "e" in sdOpts: # End date
		end = sdOpts["e"]

	for account in accounts:
		movements = account.movements

		if start != "":
			movements = [movement for movement in movements if movement.date >= start]

		if end != "":
			movements = [movement for movement in movements if movement.date <= end]

		if len(movements) == 0:
			continue

		# Summary

		accountString = "\\section*{Summary for: " + account.name[0].upper() + account.name[1:] + "}"
		accountString += "\n\n\\subsection*{General statistics}"

		accountString += "\n\nAccount name: " + account.name + ". \\newline"
		accountString += "\nOpened with: " + moneyPrint(account.start) + " \\newline"
		accountString += "\nAccount "

		if start == end == "":
			accountString += "balance: " + moneyPrint(account.balance)
		
		else:
			accountString += "movements during the specified period: " + moneyPrint(sum([movement.amount for movement in movements]))

		years = set([movement.date.split("-")[0] for movement in movements])
		years = list(years)
		years.sort()

		for year in years:
			yearMovements = [movement for movement in movements if year in movement.date]

			months = set([movement.date.split("-")[1] for movement in yearMovements])
			months = list(months)
			months.sort()

			accountString += "\n\n\\subsection*{" + year + " statistics}"
			accountString += "\n\n" + str(len(yearMovements)) + " movement(s) for a total of " + moneyPrint(sum([movement.amount for movement in yearMovements]))

			income = sum([movement.amount for movement in yearMovements if movement.amount > 0])
			expense = sum([movement.amount for movement in yearMovements if movement.amount < 0])

			accountString += " \\newline\nIncome: " + moneyPrint(income) if income != 0 else ""
			accountString += " \\newline\nExpense: " + moneyPrint(expense) if expense != 0 else ""

			accountString += "\n\n\\begin{description}"

			for month in months:
				monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
				monthMovements.sort(key = lambda entry: entry.date)

				accountString += "\n\t\\item[" + monthName(month) + "] " + str(len(monthMovements)) + " movement(s) for a total of " + moneyPrint(sum([movement.amount for movement in monthMovements]))

				income = sum([movement.amount for movement in monthMovements if movement.amount > 0])
				expense = sum([movement.amount for movement in monthMovements if movement.amount < 0])

				accountString += " \\newline\n\tIncome: " + moneyPrint(income) if income != 0 else ""
				accountString += " \\newline\n\tExpense: " + moneyPrint(expense) if expense != 0 else ""
			
			accountString += "\n\\end{description} \n\n\\newpage"

			accountReports.append(accountString)
		
	# Movements

	for account in accounts:
		movements = account.movements

		if start != "":
			movements = [movement for movement in movements if movement.date >= start]

		if end != "":
			movements = [movement for movement in movements if movement.date <= end]

		if len(movements) == 0:
			continue

		accountString = "\\section*{Movements for: " + account.name[0].upper() + account.name[1:] + "}"

		years = set([movement.date.split("-")[0] for movement in movements])
		years = list(years)
		years.sort()

		for year in years:
			yearMovements = [movement for movement in movements if year in movement.date]

			months = set([movement.date.split("-")[1] for movement in yearMovements])
			months = list(months)
			months.sort()

			accountString += "\n\n\\subsection*{" + year + "}"
			accountString += "\n\n\\begin{multicols*}{2}"
			accountString += "\n\n\\begin{description}"

			for month in months:
				monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
				monthMovements.sort(key = lambda entry: entry.date)

				accountString += "\n\\item[" + monthName(month) + "] \\leavevmode"

				days = set([movement.date.split("-")[2] for movement in monthMovements])
				days = list(days)
				days.sort()

				accountString += "\n\t\\begin{description}"

				for day in days:
					dateString = year + "-" + month + "-" + day
					dayMovements = [movement for movement in monthMovements if movement.date == dateString]
					
					accountString += "\n\t\t\\item[" + day + "] \\leavevmode"
					accountString += "\n\t\t\\begin{description}"

					for movement in dayMovements:
						reasonString = movement.reason[0].upper() + movement.reason[1:]
						accountString += "\n\t\t\t\\item[" + moneyPrint(movement.amount) + "] " + reasonString + " \\newline\n\t\t\t\\color{solarized-cyan} \\Hash" + movement.code + "\\color{solarized-base02}"
					
					accountString += "\n\t\t\\end{description}"
				
				accountString += "\n\t\\end{description}"
		
			accountString += "\n\\end{description}"
			accountString += "\n\n\\end{multicols*} \n\n\\newpage"

		accountReports.append(accountString)
	
	templateFile = open(resourcesPath + "report.txt", "r")
	template = templateFile.read()
	templateFile.close()

	timeRange = ""

	if start == "":
		start = min([min([movement.date for movement in account.movements]) if len(account.movements) else "N/A" for account in accounts])

	if end == "":
		end = max([max([movement.date for movement in account.movements]) if len(account.movements) else "" for account in accounts])

	timeRange += "From " + start + " to " + end

	reportTime = time.strftime("%Y-%m-%dT%H:%M")

	reportText = template.replace("SUMMARY", "\n\n".join(accountSummary))
	reportText = reportText.replace("REPORTCONTENT", "\n\n".join(accountReports))
	reportText = reportText.replace("DATE", "Compiled on " + time.strftime("%A, %B %d, %Y at %H:%M"))
	reportText = reportText.replace("TIMERANGE", timeRange)
	reportText = reportText.replace("USER", str(user))

	reportTexPath = reportsPath + "lastReport.tex"
	reportTex = open(reportTexPath, "w")
	reportTex.write(reportText)
	reportTex.close()

	for _ in range(10):
		pdfl = PDFLaTeX.from_texfile(reportTexPath)
		
	pdf, _, _ = pdfl.create_pdf()

	reportFilePath = reportsPath + "report_" + reportTime + ".pdf"
	reportPdf = open(reportFilePath, "wb")
	reportPdf.write(pdf)
	reportPdf.close()

	if "keep" not in ddOpts:
		try:
			os.remove(reportTexPath)
		
		except:
			pass