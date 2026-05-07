$ErrorActionPreference = "Stop"

$logPath = Join-Path $PSScriptRoot "enable-wsl-features.log"
"Starting WSL feature enablement at $(Get-Date -Format o)" | Set-Content -Path $logPath

function Invoke-LoggedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    "`n> $FilePath $($Arguments -join ' ')" | Add-Content -Path $logPath
    & $FilePath @Arguments 2>&1 | Tee-Object -FilePath $logPath -Append
    if ($LASTEXITCODE -ne 0) {
        throw "$FilePath exited with code $LASTEXITCODE"
    }
}

Invoke-LoggedCommand dism.exe @(
    "/online",
    "/enable-feature",
    "/featurename:Microsoft-Windows-Subsystem-Linux",
    "/all",
    "/norestart"
)

Invoke-LoggedCommand dism.exe @(
    "/online",
    "/enable-feature",
    "/featurename:VirtualMachinePlatform",
    "/all",
    "/norestart"
)

"`nCompleted WSL feature enablement at $(Get-Date -Format o)" | Add-Content -Path $logPath
