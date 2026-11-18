<#
.SYNOPSIS
  Koopmann-Aziz run script for likable_jelly: regression.py -what val|final.

.DESCRIPTION
  1. sets the venv, TEMP and caches (on E:), and LJ_CONFIG = koopmann_aziz\config\CONFIG.<Machine>
  2. checks free RAM, free disk and that no other training is running
  3. smoke step first (SmokeDays day files, SmokeTrees trees), then the real run, one seed after
     the other; stops at the first failure
  4. logs to <EXT_FOLDER>\logs, outputs to <EXT_FOLDER>\preds|submissions|scores
  5. prints a summary block between two marker lines: paste exactly that block back.

  Expected runtime per seed on pc182: CPU 511 bins ~2 h, CPU 255 bins ~1 h 46 min, GPU 255 bins ~38 min.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\run_lj.ps1 -What val -Seeds 0
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\run_lj.ps1 -What final -Seeds 0 -CompareTo E:\Koopmann-Aziz\results\prc2024\likable_jelly\preds
.EXAMPLE
  laptop test on synthetic data:
  powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\run_lj.ps1 -Machine laptop -Python C:\Users\azizf\venvs\Koopmann-Aziz-lj24\Scripts\python.exe -MinFreeRamGB 1 -Extra "-n_estimators 100 -min_child_samples 5"
#>
param(
    [ValidateSet("val", "final")][string]$What = "val",
    [string]$Variant = "baseline",
    [string]$Seeds = "0",                 # "0" | "0,1,2" | "0-19"
    [ValidateSet("cpu", "gpu")][string]$Device = "cpu",
    [int]$MaxBin = 511,
    [string]$Extra = "",                  # further regression.py arguments, e.g. "-num_leaves 20"
    [int]$SmokeDays = 2,
    [int]$SmokeTrees = 200,
    [switch]$SkipSmoke,
    [switch]$SmokeOnly,
    [string]$Machine = "pc182",
    [string]$Python = "E:\Koopmann-Aziz\venvs\Koopmann-Aziz-lj24\Scripts\python.exe",
    [double]$MinFreeRamGB = 25,           # one training peaks at ~24 GB
    [double]$MinFreeDiskGB = 10,
    [string]$CompareTo = "",              # final only: folder with lj_full_seed<k>.csv to compare seed k with
    [int]$HeartbeatSec = 300
)

$ErrorActionPreference = "Stop"
# numbers in the summary always as 1234.56, whatever the Windows locale
[System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
$BEGIN = "===== KOOPMANN-AZIZ SUMMARY BEGIN ====="
$END = "===== KOOPMANN-AZIZ SUMMARY END ====="
$t0 = Get-Date
$summary = New-Object System.Collections.Generic.List[string]
$status = "OK"
$failLog = $null
$logFiles = New-Object System.Collections.Generic.List[string]

function Add-Line([string]$s) { $summary.Add($s) | Out-Null }

function Parse-Seeds([string]$s) {
    $out = @()
    foreach ($part in $s.Split(",")) {
        $p = $part.Trim()
        if ($p -match "^(\d+)-(\d+)$") { $out += [int]$Matches[1]..[int]$Matches[2] }
        elseif ($p -match "^\d+$") { $out += [int]$p }
        elseif ($p -ne "") { throw "bad -Seeds value '$s'" }
    }
    return , $out
}

function Read-Config([string]$file) {
    $cfg = @{}
    foreach ($line in Get-Content $file) {
        $l = $line.Trim()
        if ($l -eq "" -or $l.StartsWith("#")) { continue }
        $i = $l.IndexOf("=")
        if ($i -gt 0) { $cfg[$l.Substring(0, $i).Trim()] = $l.Substring($i + 1).Trim() }
    }
    return $cfg
}

function Quote-Arg([string]$a) { if ($a -match '[\s"]') { return '"' + ($a -replace '"', '\"') + '"' } else { return $a } }

function Invoke-Regression([string]$label, [string[]]$pyArgs) {
    # runs python regression.py <pyArgs>; returns the parsed KA_RESULT object (throws on failure)
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $log = Join-Path $script:logDir "$stamp`__$label.log"
    $outF = "$log.stdout"; $errF = "$log.stderr"
    $argLine = (@("regression.py") + $pyArgs | ForEach-Object { Quote-Arg $_ }) -join " "
    Write-Host ("[{0:HH:mm:ss}] start {1}: python {2}" -f (Get-Date), $label, $argLine)
    Write-Host "           log: $log"
    $p = Start-Process -FilePath $script:Python -ArgumentList $argLine -WorkingDirectory $script:repo `
        -NoNewWindow -PassThru -RedirectStandardOutput $outF -RedirectStandardError $errF
    $null = $p.Handle  # keeps the exit code available in Windows PowerShell 5.1
    $ts = Get-Date
    while (-not $p.WaitForExit($HeartbeatSec * 1000)) {
        $ram = ""
        try {
            # the venv python.exe may be a launcher: count its child interpreter too
            $ids = @($p.Id) + @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" | ForEach-Object { $_.ProcessId })
            $ram = "{0:F1} GB" -f (((Get-Process -Id $ids -ErrorAction SilentlyContinue) | Measure-Object WorkingSet64 -Sum).Sum / 1GB)
        } catch {}
        Write-Host ("[{0:HH:mm:ss}] ... {1} running for {2:F0} min, RAM {3}" -f (Get-Date), $label, ((Get-Date) - $ts).TotalMinutes, $ram)
    }
    $p.WaitForExit()
    $code = $p.ExitCode
    # one combined log: stdout then stderr
    Get-Content $outF | Set-Content -Encoding UTF8 $log
    Add-Content -Encoding UTF8 $log "----- stderr -----"
    Get-Content $errF | Add-Content -Encoding UTF8 $log
    Remove-Item $outF, $errF
    $script:logFiles.Add($log) | Out-Null
    $res = Select-String -Path $log -Pattern "^KA_RESULT " | Select-Object -Last 1
    if ($code -ne 0 -or $null -eq $res) {
        $script:failLog = $log
        throw "$label failed (exit code $code)"
    }
    Write-Host ("[{0:HH:mm:ss}] done  {1} in {2:F1} min" -f (Get-Date), $label, ((Get-Date) - $ts).TotalMinutes)
    return ($res.Line.Substring(10) | ConvertFrom-Json)
}

try {
    $repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
    Set-Location $repo
    $seedList = Parse-Seeds $Seeds
    if ($seedList.Count -eq 0) { throw "no seeds given" }

    # ---------- config and environment ----------
    $cfgFile = Join-Path $repo "koopmann_aziz\config\CONFIG.$Machine"
    if (-not (Test-Path $cfgFile)) { throw "config file not found: $cfgFile" }
    $cfg = Read-Config $cfgFile
    foreach ($k in @("FOLDER_DATA", "EXT_FOLDER", "TEMP_FOLDER")) { if (-not $cfg.ContainsKey($k)) { throw "$k missing in $cfgFile" } }
    $ext = $cfg["EXT_FOLDER"] -replace "/", "\"
    $tmp = $cfg["TEMP_FOLDER"] -replace "/", "\"
    foreach ($bad in @("\likable_jelly\preds", "\likable_jelly\scores", "\likable_jelly\experiments", "\prc2024\lj\submissions")) {
        if ($ext.ToLower().Contains($bad)) { throw "EXT_FOLDER $ext points into a reproduction folder" }
    }
    if (-not (Test-Path $Python)) { throw "python not found: $Python" }
    $script:logDir = Join-Path $ext "logs"
    foreach ($d in @($ext, $script:logDir, (Join-Path $ext "preds"), (Join-Path $ext "scores"), (Join-Path $ext "submissions"), $tmp)) {
        if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
    }
    $env:LJ_CONFIG = $cfgFile
    $env:TEMP = $tmp; $env:TMP = $tmp
    $env:NUMBA_CACHE_DIR = Join-Path $tmp "numba"
    $env:MPLCONFIGDIR = Join-Path $tmp "matplotlib"
    $env:XDG_CACHE_HOME = Join-Path $tmp "cache"
    $env:PIP_CACHE_DIR = Join-Path $tmp "pip"
    $env:UV_CACHE_DIR = Join-Path $tmp "uv"
    $env:LOKY_MAX_CPU_COUNT = "$([Environment]::ProcessorCount)"
    $env:PYTHONUNBUFFERED = "1"
    $env:PYTHONUTF8 = "1"
    $env:PYTHONIOENCODING = "utf-8"

    $commit = "unknown"; $dirty = "unknown"
    try {
        $commit = (& git -C $repo rev-parse HEAD).Trim()
        $dirty = [string]([bool](& git -C $repo status --porcelain --untracked-files=no))
    } catch {}

    $perSeedH = @{ "cpu511" = 2.0; "cpu255" = 1.77; "gpu255" = 0.63 }["$Device$MaxBin"]
    $expect = if ($perSeedH) { "{0:F1} h ({1} seed(s) x {2:F2} h)" -f ($perSeedH * $seedList.Count), $seedList.Count, $perSeedH } else { "unknown for $Device/$MaxBin bins" }

    Write-Host "Koopmann-Aziz likable_jelly run   commit $commit (dirty: $dirty)"
    Write-Host "what=$What variant=$Variant seeds=$($seedList -join ',') device=$Device bins=$MaxBin extra='$Extra'"
    Write-Host "expected runtime (pc182): $expect"

    # ---------- resource checks ----------
    $avail = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory).AvailableBytes / 1GB
    $drive = (Split-Path -Qualifier $ext).TrimEnd(":")
    $free = (Get-PSDrive $drive).Free / 1GB
    Write-Host ("available RAM {0:F1} GB (need {1}), free disk {2}: {3:F1} GB (need {4})" -f $avail, $MinFreeRamGB, $drive, $free, $MinFreeDiskGB)
    if ($avail -lt $MinFreeRamGB) { throw ("not enough free RAM: {0:F1} GB available, {1} GB needed (close other programs)" -f $avail, $MinFreeRamGB) }
    if ($free -lt $MinFreeDiskGB) { throw ("not enough free disk on {0}: {1:F1} GB, {2} GB needed" -f $drive, $free, $MinFreeDiskGB) }
    $others = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match "regression\.py" }
    if ($others) { throw "another regression.py is already running (PID $(($others | ForEach-Object { $_.ProcessId }) -join ',')): never two trainings at once" }

    $common = @("-what", $What, "-variant", $Variant, "-device", $Device, "-max_bin", "$MaxBin")
    $extraArgs = @()
    if ($Extra.Trim() -ne "") { $extraArgs = $Extra.Trim() -split "\s+" }

    Add-Line "commit      : $commit (dirty: $dirty)"
    Add-Line "machine     : $Machine   config: koopmann_aziz\config\CONFIG.$Machine"
    Add-Line "what        : $What   variant: $Variant   device: $Device   bins: $MaxBin"
    Add-Line "extra args  : $Extra"
    Add-Line "seeds       : $($seedList -join ',')"
    Add-Line ("resources   : RAM available {0:F1} GB, disk {1}: free {2:F1} GB" -f $avail, $drive, $free)

    # ---------- smoke ----------
    if (-not $SkipSmoke) {
        $r = Invoke-Regression "SMOKE-$What`__$Variant" ($common + @("-random_state", "$($seedList[0])", "-smoke_days", "$SmokeDays") + $extraArgs + @("-n_estimators", "$SmokeTrees"))
        $msg = "smoke       : OK ($SmokeDays days, $SmokeTrees trees, {0:F0} s, peak RAM {1:F2} GB" -f $r.runtime_s, $r.peak_ram_gb
        if ($What -eq "val") { $msg += (", n_train {0}, n_val {1}, val RMSE {2:F1} kg)" -f $r.n_train, $r.n_val, $r.val_rmse) } else { $msg += (", n_pred {0})" -f $r.n_pred) }
        Add-Line $msg
    } else { Add-Line "smoke       : skipped" }

    # ---------- real run ----------
    $rmses = @()
    if (-not $SmokeOnly) {
        foreach ($s in $seedList) {
            $r = Invoke-Regression "$What`__$Variant`__$Device`_b$MaxBin`__seed$s" ($common + @("-random_state", "$s") + $extraArgs)
            if ($What -eq "val") {
                $rmses += [double]$r.val_rmse
                Add-Line ("seed {0,-6} : val RMSE {1:F2} kg  (n_train {2}, n_val {3})  runtime {4:F1} min  peak RAM {5:F1} GB" -f $s, $r.val_rmse, $r.n_train, $r.n_val, ($r.runtime_s / 60), $r.peak_ram_gb)
            } else {
                Add-Line ("seed {0,-6} : n_pred {1}  runtime {2:F1} min  peak RAM {3:F1} GB  -> {4}" -f $s, $r.n_pred, ($r.runtime_s / 60), $r.peak_ram_gb, $r.output)
                if ($CompareTo -ne "") {
                    $ref = Join-Path $CompareTo "lj_full_seed$s.csv"
                    if (Test-Path $ref) {
                        $cmp = & $Python -m koopmann_aziz.average --compare $r.output $ref 2>$null | Select-String "^KA_COMPARE"
                        Add-Line ("  vs repro  : " + ($(if ($cmp) { $cmp.Line.Substring(11) } else { "comparison failed" })))
                    } else { Add-Line "  vs repro  : $ref not found" }
                }
            }
        }
        if ($What -eq "val") {
            $mean = ($rmses | Measure-Object -Average).Average
            $std = 0.0
            if ($rmses.Count -gt 1) { $std = [math]::Sqrt((($rmses | ForEach-Object { ($_ - $mean) * ($_ - $mean) }) | Measure-Object -Sum).Sum / ($rmses.Count - 1)) }
            Add-Line ("val RMSE    : {0:F2} +- {1:F2} kg (mean +- std over {2} seed(s))" -f $mean, $std, $rmses.Count)
        } else {
            Add-Line "final set   : not scored here (score with score_atow.py)"
        }
    }
} catch {
    $status = "FAILED: $($_.Exception.Message)"
}

$elapsed = (Get-Date) - $t0
Add-Line ("total time  : {0:F0} min" -f $elapsed.TotalMinutes)
foreach ($l in $logFiles) { Add-Line "log         : $l" }
Add-Line "status      : $status"
if ($status -ne "OK" -and $failLog -and (Test-Path $failLog)) {
    Add-Line "----- last 30 lines of $failLog -----"
    foreach ($l in (Get-Content $failLog -Tail 30)) { Add-Line $l }
}
$block = @($BEGIN) + $summary + @($END)
Write-Host ""
$block | ForEach-Object { Write-Host $_ }
if ($script:logDir -and (Test-Path $script:logDir)) {
    $block | Set-Content -Encoding UTF8 (Join-Path $script:logDir ("{0:yyyyMMdd-HHmmss}__summary__{1}__{2}.txt" -f $t0, $What, $Variant))
}
if ($status -ne "OK") { exit 1 }
