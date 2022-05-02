@echo off
set arg_install_mode=%1
set arg_base_python_path=%~2

if %arg_install_mode%==using_python_path goto build_from_base_path
if %arg_install_mode%==standalone goto build_standalone
goto unknown_mode


:build_from_base_path
    if exist %arg_base_python_path% (
        %arg_base_python_path% -m venv env
        set PYTHON_PATH=env\Scripts\python.exe
        %PYTHON_PATH% -m pip install -r requirements.txt
        copy sqlite3.dll env\Scripts
    ) else (
        echo ERROR: Python path not found: %arg_base_python_path%
    )
    goto end_script


:build_standalone
    if not exist "python/" mkdir "python/"
    tar -xf python-3.8.10-embed-amd64.zip -C python/
    copy get-pip.py python\
    cd python
    python get-pip.py
    ren python38._pth python38._pth.dummy
    cd ..
    set PYTHON_PATH=python\python.exe
    %PYTHON_PATH% -m pip install -r requirements.txt
    goto end_script


:unknown_mode
    echo ERROR: Unknown installation mode


:end_script