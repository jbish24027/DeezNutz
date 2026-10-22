@echo off
rem Padborn.dll build driver. Log: D:\Mods\Code\padborn-build.log
call :main > "D:\Mods\Code\padborn-build.log" 2>&1
exit /b %ERRORLEVEL%

:main
setlocal
set "SRC=C:\1. AUTHORIA\_tools\padborn\Source"
set "BUILD=D:\Mods\Code\padborn-build"
echo [%time%] configure
cmake -S "%SRC%" -B "%BUILD%" -G "Visual Studio 17 2022" -A x64 -DCMAKE_TOOLCHAIN_FILE=D:/Mods/Code/vcpkg/scripts/buildsystems/vcpkg.cmake -DVCPKG_TARGET_TRIPLET=x64-windows-static-md -DCOMMONLIB_ENABLE_IPO=OFF
if errorlevel 1 (
  echo [%time%] CONFIGURE_FAILED
  exit /b 1
)
echo [%time%] build
cmake --build "%BUILD%" --config Release -- /m
if errorlevel 1 (
  echo [%time%] BUILD_FAILED
  exit /b 1
)
echo [%time%] BUILD_OK
exit /b 0
