@echo off
rem AutoCombatDodge.dll build driver. Log: build.log beside this file.
set "JOB=%~dp0"
if "%BUILDLOG%"=="" (set "BUILDLOG=%JOB%build.log")
call :main > "%BUILDLOG%" 2>&1
exit /b %ERRORLEVEL%

:main
setlocal
set "SRC=%JOB%src"
if "%BUILDDIR%"=="" (set "BUILD=%JOB%build") else (set "BUILD=%BUILDDIR%")
echo [%time%] configure
cmake -S "%SRC%" -B "%BUILD%" -G "Visual Studio 17 2022" -A x64 -DCMAKE_TOOLCHAIN_FILE="%JOB%ext/vcpkg/scripts/buildsystems/vcpkg.cmake" -DVCPKG_TARGET_TRIPLET=x64-windows-static-md -DCOMMONLIB_ENABLE_IPO=OFF
if errorlevel 1 (
  echo [%time%] CONFIGURE_FAILED
  exit /b 1
)
echo [%time%] build
cmake --build "%BUILD%" --config Release --target AutoCombatDodge -- /m:1 /p:CL_MPCount=8
if errorlevel 1 (
  echo [%time%] BUILD_FAILED
  exit /b 1
)
echo [%time%] BUILD_OK
exit /b 0
