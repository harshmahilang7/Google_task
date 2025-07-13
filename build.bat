@echo off
pyinstaller --onefile --windowed ^
    --icon=assets/icon.ico ^
    --add-data "assets;assets" ^
    main.py