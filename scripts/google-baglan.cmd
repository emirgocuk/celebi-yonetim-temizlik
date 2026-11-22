@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set "ROOT=%~dp0.."
python "%ROOT%\scripts\google-analytics-gsc-report.py" %*
exit /b %ERRORLEVEL%
