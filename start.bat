@echo off
echo Python Flask Eltex App Start (Windows)


IF NOT EXIST venv (
    echo Virtual env generating...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

IF NOT EXIST .env (
    echo .env not found, generating...
    python env_generator.py 
	if errorlevel 1 (
	echo Error when generating .env
	pause
	exit /b
	)
) ELSE (
    echo .env already exist
)
python app.py
