@echo off
echo ==========================================
echo  LMU Clock Overlay - Build Script
echo  Author: cento789
echo ==========================================
echo.

pip install pyinstaller 2>nul

echo Building LMUClockOverlay.exe ...
pyinstaller --onefile --noconsole --name LMUClockOverlay --version-file version_info.py clock_overlay.py

echo.
if exist dist\LMUClockOverlay.exe (
    echo BUILD SUCCESS: dist\LMUClockOverlay.exe
) else (
    echo BUILD FAILED
)
pause
