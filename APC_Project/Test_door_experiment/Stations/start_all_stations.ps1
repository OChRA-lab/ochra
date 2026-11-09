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

Get-ChildItem -Path $stationsDir -Filter *.py -File |
    Where-Object { $_.Name -ne "solid_addition_station.py" } |
    ForEach-Object {
        $script = $_.FullName
        Write-Host "Starting $($_.Name) in new PowerShell window..."
        # Use `conda run` to execute the script inside the specified conda environment.
        # `--no-capture-output` allows the child process output to stream to the new window.
        # use backtick to escape $ so it's evaluated in the child process, not here
        $cmd = "& { `$env:PYTHONPATH = '$pyRoot'; Set-Location -Path '$stationsDir'; conda run -n '$CondaEnv' --no-capture-output '$Python' '$script' }"
        Start-Process powershell -ArgumentList '-NoExit', '-Command', $cmd
    }
    Write-Host "Launched all station scripts."
