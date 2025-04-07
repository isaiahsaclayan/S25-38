if exist build (
    rmdir /s /q build
)

pyinstaller --clean build/transpiler
pyinstaller --name transpiler ^
    --onefile ^
    --windowed ^
    --specpath build ^
    --distpath build/output ^
    --workpath build/temp ^
    --paths=source/transpiler ^
    source/transpiler/__main__.py