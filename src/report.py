from pdflatex import PDFLaTeX
from datetime import datetime
import os

def moneyPrint(amount: float) -> str:
	if amount >= 0:
		return "\\color{solarized-green} \\Plus" + str(round(amount, 2)) + "\\texteuro \\color{#FONT}"

	else:
		return "\\color{solarized-red} \\Minus" + str(round(-amount, 2)) + "\\texteuro \\color{#FONT}"

def report(user, sdOpts: dict, ddOpts: list, reportsPath: str, reportTemplatePath: str) -> None:
	accounts = user.accounts

	accountSummary = ["\\subsection*{User}"]
	accountSummary += [" \\newline\n".join(["Username: " + str(user), "Liquidity: " + moneyPrint(sum(account.balance for account in accounts)), "Registration date: " + user.registrationDate.strftime("%A, %B %d, %Y at %H:%M")])]

	accountSummary += ["\\subsection*{Accounts}"]
	accountSummary += ["\n".join(["\\begin{description}", "\n".join(["\t\\item[" + account.name[0].upper() + account.name[1:] + "] " + str(len(account.movements)) + " registered movement(s), current balance of: " + moneyPrint(account.balance) + " \\newline \n\tOpened with: " + moneyPrint(account.start) for account in accounts]), "\\end{description}"])]

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
		years.sort(reverse=True)

		for year in years:
			yearMovements = [movement for movement in movements if year in movement.date]

			months = set([movement.date.split("-")[1] for movement in yearMovements])
			months = list(months)
			months.sort()
			
			if year != max(years):
				accountString += "\n\n\\newpage\n\\subsection*{" + year + " statistics}"
			
			else:
				accountString += "\n\n\\subsection*{" + year + " statistics}"

			accountString += "\n\n" + str(len(yearMovements)) + " movement(s) for a total of " + moneyPrint(sum([movement.amount for movement in yearMovements]))

			income = sum([movement.amount for movement in yearMovements if movement.amount > 0])
			expense = sum([movement.amount for movement in yearMovements if movement.amount < 0])

			accountString += " \\newline\nIncome: " + moneyPrint(income) if income != 0 else ""
			accountString += " \\newline\nExpense: " + moneyPrint(expense) if expense != 0 else ""

			accountString += "\n\n\\begin{multicols}{2}"

			accountString += "\n\n\\subsubsection*{Categories}"

			accountString += "\n\n\\begin{description}"

			categories = {movement.category for movement in yearMovements}
			categories = list(categories)
			categories.sort()

			if "others" in categories:
				categories.remove("others")
				categories = ["others"] + categories

			for category in categories:
				categoryMovements = [movement for movement in yearMovements if movement.category == category]

				accountString += "\n\t\\item[" + category[0].upper() + category[1:] + "] " + str(len([movement for movement in categoryMovements])) + " movement(s) for a total of " + moneyPrint(sum([movement.amount for movement in categoryMovements]))

				income = sum([movement.amount for movement in categoryMovements if movement.amount > 0])
				expense = sum([movement.amount for movement in categoryMovements if movement.amount < 0])

				accountString += " \\newline\n\tIncome: " + moneyPrint(income) if income != 0 else ""
				accountString += " \\newline\n\tExpense: " + moneyPrint(expense) if expense != 0 else ""

			accountString += "\n\\end{description}\n\n\\vfill\\null\n\\columnbreak"

			accountString += "\n\n\\subsubsection*{Months}"

			accountString += "\n\n\\begin{description}"

			for month in months:
				monthMovements = [movement for movement in yearMovements if "-" + month + "-" in movement.date]
				monthMovements.sort(key = lambda entry: entry.date)

				accountString += "\n\t\\item[" + datetime.strptime(month, "%m").strftime('%B') + "] " + str(len(monthMovements)) + " movement(s) for a total of " + moneyPrint(sum([movement.amount for movement in monthMovements]))

				income = sum([movement.amount for movement in monthMovements if movement.amount > 0])
				expense = sum([movement.amount for movement in monthMovements if movement.amount < 0])

				accountString += " \\newline\n\tIncome: " + moneyPrint(income) if income != 0 else ""
				accountString += " \\newline\n\tExpense: " + moneyPrint(expense) if expense != 0 else ""
			
			accountString += "\n\\end{description}"

			accountString += "\n\n\\end{multicols}"
		
		accountString += "\n\n\\newpage"
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
		years.sort(reverse=True)

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

				accountString += "\n\\item[" + datetime.strptime(month, "%m").strftime('%B') + "] \\leavevmode"

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
						categoryString = movement.category[0].upper() + movement.category[1:]

						accountString += "\n\t\t\t\\item[" + moneyPrint(movement.amount) + "] " + reasonString + " \\newline\n\t\t\t\\color{#FOURTH} " + categoryString + " \\color{#THIRD} \\Hash " + movement.code + "\\color{#FONT}"
					
					accountString += "\n\t\t\\end{description}"
				
				accountString += "\n\t\\end{description}"
		
			accountString += "\n\\end{description}"
			accountString += "\n\n\\end{multicols*}\n\n\\newpage"

		accountReports.append(accountString)
	
	templateFile = open(reportTemplatePath, "r")
	template = templateFile.read()
	templateFile.close()

	timeRange = ""

	if start == "":
		start = min([min([movement.date for movement in account.movements]) if len(account.movements) else "N/A" for account in accounts])

	if end == "":
		end = max([max([movement.date for movement in account.movements]) if len(account.movements) else "" for account in accounts])

	timeRange += "From " + start + " to " + end

	reportTime = datetime.now().strftime("%Y-%m-%dT%H:%M")

	reportText = template.replace("SUMMARY", "\n\n".join(accountSummary))
	reportText = reportText.replace("REPORTCONTENT", "\n\n".join(accountReports))
	reportText = reportText.replace("DATE", "Compiled on " + datetime.now().strftime("%A, %B %d, %Y at %H:%M"))
	reportText = reportText.replace("TIMERANGE", timeRange)
	reportText = reportText.replace("USER", str(user))

	if "dark" not in ddOpts: # Optional dark themed reports.
		reportText = reportText.replace("#BACKGROUND", "solarized-base3")
		reportText = reportText.replace("#FONT", "solarized-base03")
		reportText = reportText.replace("#ACCENT", "solarized-orange")
		reportText = reportText.replace("#THIRD", "solarized-cyan")
		reportText = reportText.replace("#FOURTH", "solarized-blue")
	
	else:
		reportText = reportText.replace("#BACKGROUND", "solarized-base02")
		reportText = reportText.replace("#FONT", "solarized-base1")
		reportText = reportText.replace("#ACCENT", "solarized-orange")
		reportText = reportText.replace("#THIRD", "solarized-cyan")
		reportText = reportText.replace("#FOURTH", "solarized-blue")

	reportTexPath = reportsPath + "lastReport.tex"
	reportTex = open(reportTexPath, "w")
	reportTex.write(reportText)
	reportTex.close()

	pdfl = PDFLaTeX.from_texfile(reportTexPath)	
	pdf, _, _ = pdfl.create_pdf()

	reportFilePath = reportsPath + "report_" + reportTime + ".pdf"
	reportPdf = open(reportFilePath, "wb")
	reportPdf.write(pdf)
	reportPdf.close()

	try: # Debugging purposes.
		if "keep" not in ddOpts:
			os.remove(reportTexPath)

	except:
		pass