$ErrorActionPreference = 'Continue'
$log = 'C:\1. AUTHORIA\_tools\vss-sexdisabler\vss-recover.log'
$out = 'C:\1. AUTHORIA\_tools\vss-sexdisabler\recovered'
function L($m){ $m | Out-File -FilePath $log -Append -Encoding utf8 }
"=== VSS recovery run $(Get-Date -Format s) ===" | Out-File -FilePath $log -Encoding utf8

L "--- vssadmin list shadows ---"
(vssadmin list shadows 2>&1) | ForEach-Object { L $_ }

L ""
L "--- vssadmin list shadowstorage ---"
(vssadmin list shadowstorage 2>&1) | ForEach-Object { L $_ }

L ""
L "--- Win32_ShadowCopy ---"
$shadows = @()
try { $shadows = @(Get-CimInstance -ClassName Win32_ShadowCopy -ErrorAction Stop) } catch { L ("ERR " + $_.Exception.Message) }
L ("count=" + $shadows.Count)
foreach($s in $shadows){ L ("ID=" + $s.ID + " Vol=" + $s.VolumeName + " Dev=" + $s.DeviceObject + " Installed=" + $s.InstallDate) }

if($shadows.Count -eq 0){ L "NO SHADOW COPIES AVAILABLE - nothing to search."; exit 0 }

New-Item -ItemType Directory -Force -Path $out | Out-Null
$mountRoot = 'C:\1. AUTHORIA\_tools\vss-sexdisabler\mnt'
New-Item -ItemType Directory -Force -Path $mountRoot | Out-Null

$targets = @(
  'Mods\Code\RacemenuSexDisabler',
  'Mods\Code',
  'Mods'
)

$i = 0
foreach($s in $shadows){
  $i++
  $link = Join-Path $mountRoot ("s{0}" -f $i)
  if(Test-Path $link){ cmd /c rmdir "$link" | Out-Null }
  $dev = $s.DeviceObject
  if($dev -notmatch '\$'){ $dev = $dev + '\' }
  cmd /c mklink /d "$link" "$dev" | Out-Null
  if(-not (Test-Path $link)){ L ("mount FAILED for " + $s.ID); continue }
  L ""
  L ("--- shadow $i  ($($s.VolumeName))  installed $($s.InstallDate) mounted at $link ---")
  foreach($t in $targets){
    $p = Join-Path $link $t
    if(Test-Path -LiteralPath $p){
      L ("  HIT: " + $t)
      $dest = Join-Path $out ("shadow{0}_{1}" -f $i, ($t -replace '[\:]','_'))
      try {
        Copy-Item -LiteralPath $p -Destination $dest -Recurse -Force -ErrorAction Stop
        L ("  COPIED -> " + $dest)
      } catch { L ("  COPY ERR " + $_.Exception.Message) }
      break
    }
  }
  # broad sweep for the source file name anywhere shallow on this shadow
  $found = Get-ChildItem -LiteralPath $link -Recurse -Depth 6 -Force -ErrorAction SilentlyContinue |
           Where-Object { $_.Name -match 'RaceGate|RacemenuSexDisabler|RacemenuHeadpartsExcluder' }
  foreach($f in $found){ L ("  FOUND: " + $f.FullName) }
}

foreach($n in (Get-ChildItem -LiteralPath $mountRoot -Force -ErrorAction SilentlyContinue)){ cmd /c rmdir "$($n.FullName)" | Out-Null }
L ""
L "=== done ==="
