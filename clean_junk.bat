@echo off
title ICARUS CLEANUP RUNTIME
cd /d D:\AI_Factory
echo ==========================================================
echo      ICARUS: WORKSPACE + STORAGE CLEANUP
echo ==========================================================
call venv\Scripts\activate.bat
echo.
echo Running workspace radar...
python smart_cleaner.py
echo.
echo Optional: storage offload requires SEC-OPERATOR-99X in-script.
set /p RUNOFF=Run C-to-D duplicate offload now? (y/n): 
if /i "%RUNOFF%"=="y" python storage_offload_engine.py
echo.
echo Done. Use icarus_quickstart.bat to launch full stack.
pause
