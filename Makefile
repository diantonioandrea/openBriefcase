# Linux and macOS only

compile:
	pyinstaller --onefile --console main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase.zip" openBriefcase resources/

clean:
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase