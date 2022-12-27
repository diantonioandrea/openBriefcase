compile:
	pyinstaller --onefile --console main.py
	mv dist/main dist/openBriefcase
	mkdir -p release
	zip -r "release/openBriefcase.zip" dist/openBriefcase help/ resources/

clean:
	rm -rf dist build reports release data
	rm -rf *.spec openBriefcase