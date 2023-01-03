compile:
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase.zip" openBriefcase resources/

windows:
	pyinstaller --onefile --console main.py
	mv -Force dist/main.exe openBriefcase.exe
	mkdir -p release
	zip -r "release/openBriefcase.zip" openBriefcase.exe resources/

clean:
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase