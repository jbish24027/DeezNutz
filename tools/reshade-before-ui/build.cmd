@echo off
rem Builds AuthoriaReShadeBeforeUI.dll (no dependencies; ReShade 6.7.3 add-on headers in include\)
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul || exit /b 1
cd /d "%~dp0build"
cl /nologo /std:c++20 /O2 /MT /EHsc /W3 /DUNICODE /D_UNICODE /I..\include ..\src\main.cpp /LD /Fe:AuthoriaReShadeBeforeUI.dll /link version.lib shell32.lib ole32.lib /DEBUG /OPT:REF /OPT:ICF
exit /b %ERRORLEVEL%
