@echo off
color 0a
:a
cls
start python3 ../vpn_server/mserver.py
start python3 localserv.py
pause
taskkill /f /im python3.exe
goto a