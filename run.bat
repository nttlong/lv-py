@echo off
chcp 1252
set run_path=C:\BFS\LVCore2021\lv.Web\python\ocr
set venv_dir=venv39
cd "%run_path%\%venv_dir%"
echo %run_path%\%venv_dir%\scripts\activate.bat
call %run_path%\%venv_dir%\scripts\activate.bat
python %run_path%\main.py
