@echo off
title MoneyChess2 Runner
cd /d "P:\Develop\ChessGame2"
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Game crashed. Check the logs above.
    pause
)