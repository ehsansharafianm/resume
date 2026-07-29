@echo off
python "%~dp0system\resume_tool.py" migrate --quiet
if "%~1"=="" cls
if "%~1"=="" python "%~dp0system\resume_tool.py" menu
if "%~1"=="" exit /b %errorlevel%
if /i "%~1"=="master" python "%~dp0system\resume_tool.py" %*
if /i "%~1"=="master" exit /b %errorlevel%
python "%~dp0system\resume_tool.py" create %*
exit /b %errorlevel%
