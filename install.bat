@echo off
chcp 1252
set python_path=C:\python37
set source_dir=C:\XuLyTam\test1
cd "%run_path%"
cd "%python_path%"
python -m venv  %source_dir%\venv
call %source_dir%\venv\Scripts\activate.bat
%source_dir%\venv\Scripts\python -m pip install --upgrade pip
pip install -r %source_dir%\requirements.txt
echo %run_path%\%venv_dir%\scripts\activate.bat
