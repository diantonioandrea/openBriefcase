darwin: # macOS release
	pyinstaller --onefile --console src/main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase-darwin.zip" openBriefcase resources/

linux: # Linux release
	pyinstaller --onefile --console src/main.py
	mv dist/main openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase-linux.zip" openBriefcase resources/

clean:
	rm -rf dist build reports release data src/__pycache__ .vscode
	rm -rf *.spec openBriefcase