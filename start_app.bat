@echo off
echo Activating environment...
cd F:\AI_SDS_Parserapp
call venv\Scripts\activate

echo Adding Node to PATH for this session...
set PATH=%PATH%; path to node binaries 

echo Starting backend...
start cmd /k "uvicorn backend.main:app --reload"

timeout /t 2 >nul

echo Starting frontend...
cd frontend\sds-frontend
start cmd /k "npm run dev"

echo All systems running 🚀
