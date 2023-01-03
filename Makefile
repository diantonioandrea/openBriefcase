# Linux and macOS

compile:
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase.zip" openBriefcase resources/

clean:
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase

# Windows

windows:
	pyinstaller --onefile --console main.py
	move -Force dist/main.exe openBriefcase.exe
	mkdir -p release
	zip -r "release/openBriefcase.zip" openBriefcase.exe resources/

windowsClean:
	rd __pycache__ dist build reports release data
	rd *.spec openBriefcase.exe