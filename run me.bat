@echo off
:: Suppress command echoing and start process
echo Starting Python package installations...

:: Ensure pip is up to date
python -m pip install --upgrade pip

:: Install each package
echo Installing SpeechRecognition...
pip install SpeechRecognition

echo Installing pyttsx3...
pip install pyttsx3

echo Installing wikipedia...
pip install wikipedia

echo Installing requests...
pip install requests

echo Installing ecapture...
pip install ecapture

echo Installing wolframalpha...
pip install wolframalpha

echo All packages installed successfully!
pause