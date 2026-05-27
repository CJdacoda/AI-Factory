@echo off
title ICARUS FACTORY QUICKSTART
cd /d D:\AI_Factory
echo ==========================================================
echo      ICARUS FACTORY - LOCAL STACK QUICKSTART
echo ==========================================================
echo.
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [!] venv missing. Run: python -m venv venv
    pause
    exit /b 1
)
echo [1] Launch API + Browser HUD
echo [2] Terminal Dashboard Only
echo [3] Storage Offload C -^> D
echo [4] Desktop RAG Cleaner
echo.
set /p CHOICE=Select option: 
if "%CHOICE%"=="1" python launch_icarus_stack.py
if "%CHOICE%"=="2" python factory_dashboard.py
if "%CHOICE%"=="3" python storage_offload_engine.py
if "%CHOICE%"=="4" python desktop_rag_cleaner.py
pause
