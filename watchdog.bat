@echo off
:loop
echo ?? Restarting FastAPI Server...
call venv\Scripts\activate
uvicorn caliuso_memory_api:app --host 0.0.0.0 --port 8000
echo ? Server crashed. Restarting in 3s...
timeout /t 3 /nobreak >nul
goto loop