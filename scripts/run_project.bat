@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py generate_powerbi_project.py
) else (
    python generate_powerbi_project.py
)
if errorlevel 1 (
    echo Project generation failed.
    pause
    exit /b 1
)
start "" "%~dp0..\powerbi\Hossain_Group_Turnover.pbip"
endlocal
