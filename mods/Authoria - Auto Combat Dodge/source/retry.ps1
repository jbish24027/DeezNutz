param([string]$Name = "build", [int]$Max = 30)
# Rerun build.cmd until BUILD_OK; cl.exe crashes on this machine are transient (unstable CPU).
$root = "C:\Users\User\AppData\Local\Temp\claude\acd"
$env:BUILDDIR = Join-Path $root $Name
$env:BUILDLOG = Join-Path $root "$Name.log"
for ($i = 1; $i -le $Max; $i++) {
    & cmd /c (Join-Path $root "build.cmd")
    $log = Get-Content $env:BUILDLOG
    $last = $log[-1]
    "try ${i}: $last"
    if ($last -match "BUILD_OK") { exit 0 }
    if ($last -match "CONFIGURE_FAILED") { exit 2 }
    $real = $log | Select-String -Pattern "error C\d|error LNK"
    if ($real) { "real compile/link error:"; $real | Select-Object -First 8 | ForEach-Object { $_.Line }; exit 3 }
}
exit 1
