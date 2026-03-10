@echo off
setlocal

set PATH=%~dp0bin;%PATH%

scons %*
