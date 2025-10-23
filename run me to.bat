@echo off
REM Batch file to install PyAudio

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.x first.
    pause
    exit /b 1
)

REM Check if pip is installed
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

REM Attempt to install PyAudio using pip
echo Installing PyAudio...
REM Using precompiled wheel from PyPI if available
python -m pip install --upgrade pip
python -m pip install PyAudio

REM Verify installation
python - <<END
try:
    import pyaudio
    print(f"PyAudio version {pyaudio.__version__} installed successfully!")
except ImportError:
    print("PyAudio installation failed. You may need additional dependencies like Visual C++ Redistributable.")
END

pause