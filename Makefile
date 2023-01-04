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

windows: # Windows release
	pyinstaller --onefile --console main.py
	move .\dist\main.exe .\openBriefcase.exe
	if exist .\release rd /s /q .\release
	mkdir release
	zip -r "release/openBriefcase-windows.zip" .\openBriefcase.exe .\resources\

clean: # Linux and macOS only
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase