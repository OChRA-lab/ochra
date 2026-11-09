param(
    [string]$Python = "python",
    [string]$CondaEnv = "ochra-apc-devices"
)

# Directory containing this script (Stations)
$stationsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# Workspace root (two levels up from Stations)
$workspaceRoot = Resolve-Path (Join-Path $stationsDir "..\..")
$pyRoot = $workspaceRoot.Path

Write-Host "Stations directory: $stationsDir"
Write-Host "Workspace root (PYTHONPATH): $pyRoot"

$stationScripts = Get-ChildItem -Path $stationsDir -Filter *.py -File |
    Where-Object { $_.Name -ne "solid_addition_station.py" }
if ($stationScripts.Count -eq 0) {
    Write-Error "No station scripts found in $stationsDir"
    exit 1
}

$wt = Get-Command wt.exe -ErrorAction SilentlyContinue
if (-not $wt) {
    Write-Error "wt.exe (Windows Terminal) not found in PATH. Install Windows Terminal or use start_all_stations.ps1 instead."
    exit 1
}

Write-Host "Windows Terminal found. Opening station scripts in tabs..."

$wtArgs = @("-w", "0")
$firstTab = $true

foreach ($stationScript in $stationScripts) {
    if (-not $firstTab) {
        $wtArgs += ";"
    }

    # Use `conda run` to execute each station inside the specified conda environment.
    # `--no-capture-output` allows output to stream directly to each tab.
    # Encode the command so Windows Terminal does not split the inner PowerShell semicolons.
    $cmd = @"
`$env:PYTHONPATH = '$pyRoot'
Set-Location -Path '$stationsDir'
conda run -n '$CondaEnv' --no-capture-output '$Python' '$($stationScript.FullName)'
"@
    $encodedCmd = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))

    $wtArgs += @(
        "new-tab",
        "--title",
        $stationScript.BaseName,
        "powershell",
        "-NoExit",
        "-EncodedCommand",
        $encodedCmd
    )

    $firstTab = $false
}

& $wt.Source @wtArgs

Write-Host "Launched all station scripts."
