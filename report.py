from pdflatex import PDFLaTeX
from datetime import datetime
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
		return "\\color{solarized-green} " + str(amount) + "€ \\color{solarized-base02}"

	else:
		return "\\color{solarized-red} " + str(amount) + "€ \\color{solarized-base02}"

def report(user, sdOpts: dict) -> None:
	accounts = user.accounts
	reportPath = str(os.getcwd()) + "/report/"

	try:
		if not os.path.exists(reportPath):
			os.makedirs(reportPath)
		
	except:
		print(Back.RED + Fore.WHITE + "DATA ERROR" + Style.RESET_ALL)
		sys.exit(-1)

	accountReports = []

	start = ""
	end = ""

	if "s" in sdOpts: # Start date
		start = sdOpts["s"]

	if "e" in sdOpts: # End date
		end = sdOpts["e"]

	for account in accounts:
		counter = 0

		movements = account.movements

		if start != "":
			movements = [movement for movement in movements if movement.date >= start]

		if end != "":
			movements = [movement for movement in movements if movement.date <= end]

		accountString = "\\chapter*{Movements for: " + account.name.upper()

		if start == end == "":
			accountString += ", balance: " + str(account.balance)
		
		else:
			accountString += ", movements: " + str(sum([movement.amount for movement in movements]))

		accountString += "€}\n"

		accountString += "\\thispagestyle{fancy}\n"

		years = set([movement.date.split("-")[0] for movement in movements])
		years = list(years)
		years.sort()

		for year in years:
			yearMovements = [movement for movement in movements if year in movement.date]

			months = set([movement.date.split("-")[1] for movement in yearMovements])
			months = list(months)
			months.sort()

			accountString += "\n\n\\section*{" + year + ", " + str(len(yearMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in yearMovements])) + "}\n"
			accountString += "\\begin{multicols*}{2}"

			for month in months:
				monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
				monthMovements.sort(key = lambda entry: entry.reason)

				accountString += "\n\n\\subsection*{" + monthName(month) + ", " + str(len(monthMovements)) + " movement(s), " + moneyPrint(sum([movement.amount for movement in monthMovements])) + "}"

				for movement in monthMovements:
					counter += 1

					accountString += "\n\n\\textbf{" + movement.reason.upper() + "}" + " $\\cdot$ " + "\n" + monthName(month) + " " + movement.date.split("-")[0] + ", " + year + " $\\cdot$ " + moneyPrint(movement.amount)

			accountString += "\n\n\\end{multicols*}"
		
		if counter != 0:
			accountReports.append(accountString)
	
	templateFile = open("report.txt", "r")
	template = templateFile.read()
	templateFile.close()

	timeRange = ""

	if start != "":
		timeRange += " $\\cdot$ From " + start
	
	if end != "":
		if timeRange != "":
			timeRange += " to " + end

		else:
			timeRange += " $\\cdot$ Until " + end

	reportTime = time.strftime("%Y-%m-%dT%H:%M")
	reportFilePath = reportPath + "report_" + reportTime + ".tex"

	reportText = template.replace("REPORTCONTENT", "\n\n".join(accountReports))
	reportText = reportText.replace("DATE", time.strftime("%Y-%m-%dT%H:%M") + timeRange)
	reportText = reportText.replace("USER", user.name)

	reportFile = open(reportFilePath, "w")
	reportFile.write(reportText)
	reportFile.close()

	pdfl = PDFLaTeX.from_texfile(reportFilePath)
	pdf, _, _ = pdfl.create_pdf()

	reportPdf = open(reportFilePath.replace(".tex", ".pdf"), "wb")
	reportPdf.write(pdf)
	reportPdf.close()