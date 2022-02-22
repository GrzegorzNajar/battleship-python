#!/bin/sh

# wget https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe
# wine python-3.9.9-amd64.exe
# wine ~/.wine/drive_c/users/michal/Local\ Settings/Application\ Data/Programs/Python/Python39/Scripts/pip.exe install pyinstaller
# wine ~/.wine/drive_c/users/michal/Local\ Settings/Application\ Data/Programs/Python/Python39/Scripts/pip.exe install -r requirements.txt

wine ~/.wine/drive_c/users/michal/Local\ Settings/Application\ Data/Programs/Python/Python39/Scripts/pyinstaller.exe --onefile main.py
