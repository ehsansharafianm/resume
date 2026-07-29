@echo off
if "%~1"=="" cls
if "%~1"=="" python "%~dp0resume_tool.py" wizard
if "%~1"=="" exit /b %errorlevel%
python "%~dp0resume_tool.py" create %*
exit /b %errorlevel%
