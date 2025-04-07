:: Description: This batch script automates the process of generating an executable file from a Python script using PyInstaller.

:: Remove any existing build directory
if exist build (
    rmdir /s /q build
)

:: Generate the executable
pyinstaller --name transpiler ^
    --onefile ^
    --windowed ^
    --specpath build ^
    --distpath build/output ^
    --workpath build/temp ^
    --paths=source/transpiler ^
    source/transpiler/__main__.py