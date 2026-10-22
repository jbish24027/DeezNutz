# Building Padborn.dll

Source: `C:\1. AUTHORIA\_tools\padborn\Source` (extracted 2026-09-08 from the shipped archive's
`Source\` folder, then extended with `src\Camera.cpp`). `apply_edits.py` is the one-shot diff that
turned the 2.0.0 source into 2.1.0 (already applied; it refuses to run twice).

Library: `Source\extern\CommonLibSSE-NG` is an NTFS junction to `D:\Mods\Code\CommonLibVR`
(alandtse/CommonLibVR, branch `ng`, 7.4.0). vcpkg lives at `D:\Mods\Code\vcpkg` (bootstrapped;
the binary cache in `%LOCALAPPDATA%\vcpkg` survives even when `D:\Mods\Code` is wiped).

Run `build.cmd` (log: `D:\Mods\Code\padborn-build.log`), or by hand:

    cmake -S "C:/1. AUTHORIA/_tools/padborn/Source" -B "D:/Mods/Code/padborn-build" ^
      -G "Visual Studio 17 2022" -A x64 ^
      -DCMAKE_TOOLCHAIN_FILE=D:/Mods/Code/vcpkg/scripts/buildsystems/vcpkg.cmake ^
      -DVCPKG_TARGET_TRIPLET=x64-windows-static-md -DCOMMONLIB_ENABLE_IPO=OFF
    cmake --build "D:/Mods/Code/padborn-build" --config Release -- /m

Output: `D:\Mods\Code\padborn-build\Release\Padborn.dll` + `Padborn.pdb`. `COMMONLIB_ENABLE_IPO=OFF`
is mandatory: LTCG crashes cl.exe on this machine. If `D:\Mods\Code` is gone again:

    git clone --depth 1 -b ng https://github.com/alandtse/CommonLibVR D:\Mods\Code\CommonLibVR
    git clone https://github.com/microsoft/vcpkg D:\Mods\Code\vcpkg && D:\Mods\Code\vcpkg\bootstrap-vcpkg.bat
    New-Item -ItemType Junction -Path "C:\1. AUTHORIA\_tools\padborn\Source\extern\CommonLibSSE-NG" -Target "D:\Mods\Code\CommonLibVR"

Install: copy `Padborn.dll` + `Padborn.pdb` to `mods\Authoria - Padborn\SKSE\Plugins\`, then
repack `Authoria Padborn.zip` (`Core\SKSE\Plugins\` and `Source\`).
