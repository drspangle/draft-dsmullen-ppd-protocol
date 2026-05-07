$ErrorActionPreference = "Stop"

$logPath = Join-Path $PSScriptRoot "install-wsl-ubuntu.log"
"Starting WSL Ubuntu install at $(Get-Date -Format o)" | Set-Content -Path $logPath

function Invoke-LoggedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [int[]]$AllowedExitCodes = @(0, 3010)
    )

    "`n> $FilePath $($Arguments -join ' ')" | Add-Content -Path $logPath
    & $FilePath @Arguments 2>&1 | Tee-Object -FilePath $logPath -Append
    $exitCode = $LASTEXITCODE
    "Exit code: $exitCode" | Add-Content -Path $logPath
    if ($AllowedExitCodes -notcontains $exitCode) {
        throw "$FilePath exited with code $exitCode"
    }
}

Invoke-LoggedCommand wsl.exe @("--install", "-d", "Ubuntu", "--no-launch")

"`nCompleted WSL Ubuntu install at $(Get-Date -Format o)" | Add-Content -Path $logPath
