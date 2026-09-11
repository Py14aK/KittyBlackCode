@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo.
echo === VoP folder check ===
echo.
where python >nul 2>&1 || (echo Python not found on PATH. Install Python 3.11+ and retry. & exit /b 1)

python -m ruff --version >nul 2>&1 && python -m pytest --version >nul 2>&1 || (
  echo installing pytest and ruff...
  python -m pip install --quiet --disable-pip-version-check pytest ruff 2>nul || python -m pip install --quiet --disable-pip-version-check --user pytest ruff 2>nul
)
python -m ruff --version >nul 2>&1 || (echo ruff missing. Try: python -m pip install --user ruff & exit /b 1)
python -m pytest --version >nul 2>&1 || (echo pytest missing. Try: python -m pip install --user pytest & exit /b 1)

echo --- ruff ---
python -m ruff check .
if errorlevel 1 (echo. & echo LINT FAILED. Read the message above; it is usually right. & exit /b 1)
echo --- pytest ---
python -m pytest -q
if errorlevel 1 (echo. & echo TESTS FAILED. Do not commit. & exit /b 1)
echo.
echo Expected: All checks passed, and 16 passed / 5 skipped.
echo If the skip count dropped, check that a decision in docs\DECISIONS.md was actually answered.
endlocal
