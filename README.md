# openBriefcase

Accounting utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).  

**openBriefcase** is an accounting utility written in Python and built with CLIbrary, designed to help people easily manage their finances. It features an intuitive command line interface and powerful features, allowing users to *create and manage multiple accounts*, *track expenses and income*, *generate reports* and more. With openBriefcase, you can quickly and easily manage your finances and get a better understanding of your financial situation.  

Make sure to take a look at the [contributing guidelines](https://github.com/diantonioandrea/openBriefcase/blob/main/.github/CONTRIBUTING.md).

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **openBriefcase**.

1. Compilation
	* pyinstaller: compilation of **openBriefcase**.
2. Usage
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): interface, inputs and outputs.
	* bcrypt: profile password-protection.
	* requests: update system.
3. Reports
	* pdflatex: compilation of LaTeX reports.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller CLIbrary bcrypt requests pdflatex

Reports also need a full copy of TeX Live.

### Compiling and installing from source

**openBriefcase** can be compiled by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* linux
* darwin (macOS)

based on the platform on which **openBriefcase** will be compiled. This will also produce a release package under ./release/openBriefcase-PLATFORM.zip.  
Note that the Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).  
**openBriefcase** can be then installed by:

	./openBriefcase install

or

	.\openBriefcase.exe install

on Windows.
	
### Installing from release

After decompressing *openBriefcase-PLATFORM.zip*, it can be installed by:

	./openBriefcase install

or

	.\openBriefcase.exe install

on Windows.

## Commands

**openBriefcase** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain the list of available commands.
