@echo off
setlocal
echo ===============================================================================
echo Running Apache Hop Pipeline / Workflow for apache-hop-agy
echo ===============================================================================

set "HOP_JAVA_HOME=C:\Program Files\Java\jdk-21.0.10"
set "HOP_HOME=C:\hop"
set "PROJECT_NAME=apache-hop-agy"

if "%~1"=="" (
    set "FILE_TO_RUN=hop\workflows\main_etl_workflow.hwf"
) else (
    set "FILE_TO_RUN=%~1"
)

echo Executing: %FILE_TO_RUN% in project: %PROJECT_NAME%
call "%HOP_HOME%\hop-run.bat" -j %PROJECT_NAME% -r local -f "%FILE_TO_RUN%"
exit /b %ERRORLEVEL%
