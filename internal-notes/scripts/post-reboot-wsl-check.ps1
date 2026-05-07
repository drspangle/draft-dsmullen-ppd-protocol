$ErrorActionPreference = "Continue"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$logPath = Join-Path $PSScriptRoot "post-reboot-wsl-check.log"
"Starting post-reboot WSL check at $(Get-Date -Format o)" | Set-Content -Path $logPath

function Invoke-Logged {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command
    )

    "`n> $Command" | Tee-Object -FilePath $logPath -Append
    Invoke-Expression $Command 2>&1 | Tee-Object -FilePath $logPath -Append
}

Invoke-Logged "wsl --version"
Invoke-Logged "wsl --status"
Invoke-Logged "wsl -l -v"

"`nRepository root: $repoRoot" | Tee-Object -FilePath $logPath -Append
"Completed post-reboot WSL check at $(Get-Date -Format o)" | Tee-Object -FilePath $logPath -Append
