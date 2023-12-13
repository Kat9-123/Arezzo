@echo off
set /p version=<data\VERSION
title Arezzo - %version%
py src\Main.py %*
pause