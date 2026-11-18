<#
.SYNOPSIS
  Read-only: compares the pc182 reproduction copy of the team code with the upstream commit
  this branch starts from (fd8f0c4), file by file (SHA-256, line endings normalised).

  Expected differences (documented): CONFIG, feature_weather_from_metars.py,
  feature_thunder_from_metars.py. Anything else is printed as UNEXPECTED.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\check_repro_copy.ps1 -OriginalRepo E:\Koopmann-Aziz\repos\prc_2024\team_likable_jelly
#>
param([Parameter(Mandatory = $true)][string]$OriginalRepo)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$base = "fd8f0c45e737848b9da53cb4739fd463c9775504"
$expected = @("CONFIG", "feature_weather_from_metars.py", "feature_thunder_from_metars.py")

function Hash-Text([byte[]]$bytes) {
    # normalise CRLF -> LF so that git autocrlf does not count as a difference
    $s = [System.Text.Encoding]::UTF8.GetString($bytes) -replace "`r`n", "`n"
    $sha = [System.Security.Cryptography.SHA256]::Create()
    return [BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($s)))
}

$files = & git -C $repo ls-tree -r --name-only $base
$tmp = [System.IO.Path]::GetTempFileName()
Write-Host "===== KOOPMANN-AZIZ REPRO-COPY CHECK BEGIN ====="
Write-Host "upstream base $base vs $OriginalRepo"
$nUnexp = 0
foreach ($f in $files) {
    if ($f -like "*.pdf" -or $f -like "ourairports*") { continue }
    $local = Join-Path $OriginalRepo ($f -replace "/", "\")
    if (-not (Test-Path $local)) { Write-Host "MISSING     $f"; if ($expected -notcontains $f) { $nUnexp++ }; continue }
    cmd /c "git -C `"$repo`" show $base`:$f > `"$tmp`"" | Out-Null
    $h1 = Hash-Text ([System.IO.File]::ReadAllBytes($tmp))
    $h2 = Hash-Text ([System.IO.File]::ReadAllBytes($local))
    if ($h1 -ne $h2) {
        if ($expected -contains $f) { Write-Host "expected    $f" } else { Write-Host "UNEXPECTED  $f"; $nUnexp++ }
    }
}
$extra = Get-ChildItem -Path $OriginalRepo -Recurse -File -Include *.py, Makefile, CONFIG |
    Where-Object { $_.FullName -notmatch "\\\.git\\|__pycache__" } |
    ForEach-Object { $_.FullName.Substring($OriginalRepo.TrimEnd("\").Length + 1) -replace "\\", "/" } |
    Where-Object { $files -notcontains $_ }
foreach ($e in $extra) { Write-Host "EXTRA FILE  $e" }
Remove-Item $tmp
Write-Host "unexpected differences: $nUnexp"
Write-Host "===== KOOPMANN-AZIZ REPRO-COPY CHECK END ====="
