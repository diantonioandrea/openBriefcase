compile:
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase

# Linux and macOS only

darwin: # macOS release
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase-darwin.zip" openBriefcase resources/

linux: # Linux release
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase-linux.zip" openBriefcase resources/

clean:
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase