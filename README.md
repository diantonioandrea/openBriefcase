[![GitHub license](https://img.shields.io/github/license/diantonioandrea/openBriefcase)](https://github.com/diantonioandrea/openBriefcase/blob/main/LICENSE)

# openBriefcase

Accounting utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).

## Usage

**openBriefcase** can be built by:

	make compile

## Commands

**openBriefcase** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain, out of the account environment:

	exit
		Exits the program.
	password
		Lets the user pick a password to protect its account or disable it.
	select
		Enters the specified account environment.
		Options:
			-n ACCOUNT_NAME
	new
		Creates a new account.
	edit
		Edits an account name.
		Options:
			-n ACCOUNT_NAME
	remove
		Removes an account.
		Options:
			-n ACCOUNT_NAME
	summary
		Prints a summary of the accounts.
	report
		compile a report of all the account in the specified time range, if present. Make sure to have at least a registered movement.
		Options:
			-s STARTING_TIME, -e ENDING_TIME

and, in the account environment:

	exit
		Exits the account environment.
	new
		Creates a new movement.
	edit
		Edits a movement's features.
		Options:
			-c MOVEMENT_CODE, [--reason --amount --date]
	remove
		Removes a movement.
		Options:
			-c MOVEMENT_CODE
	summary
		Prints a summary of the account's movements.
	load
		Loads a set of movements from a file.
		Options:
			-c MOVEMENT_CODE
	dump
		Dumps a set of movements to a file.
		Options:
			-s STARTING_TIME, -e ENDING_TIME