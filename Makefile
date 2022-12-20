compile:
	pyinstaller --onefile --console main.py
	mv dist/main ./openBriefcase

clean:
	rm -rf dist build report data
	rm -rf *.spec openBriefcase