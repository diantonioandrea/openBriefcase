[![GitHub license](https://img.shields.io/github/license/diantonioandrea/openBriefcase)](https://github.com/diantonioandrea/openBriefcase/blob/main/LICENSE)

# openBriefcase

Accounting utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **openBriefcase**.

1. Compilation
	* pyinstaller, compilation of **openBriefcase**.
2. Usage
	* bcrypt, profile password-protection.
	* colorama, coloured outputs.
	* requests, update system.
3. Reports
	* pdflatex, compilation of LaTeX reports.

Reports also need a full compy of TeX Live.

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