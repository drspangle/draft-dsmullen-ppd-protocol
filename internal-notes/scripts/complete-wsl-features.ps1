$ErrorActionPreference = "Stop"

$logPath = Join-Path $PSScriptRoot "complete-wsl-features.log"
"Starting WSL feature completion at $(Get-Date -Format o)" | Set-Content -Path $logPath

function Invoke-LoggedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [int[]]$AllowedExitCodes = @(0)
    )

    "`n> $FilePath $($Arguments -join ' ')" | Add-Content -Path $logPath
    & $FilePath @Arguments 2>&1 | Tee-Object -FilePath $logPath -Append
    $exitCode = $LASTEXITCODE
    "Exit code: $exitCode" | Add-Content -Path $logPath
    if ($AllowedExitCodes -notcontains $exitCode) {
        throw "$FilePath exited with code $exitCode"
    }
}

Invoke-LoggedCommand dism.exe @(
    "/online",
    "/enable-feature",
    "/featurename:VirtualMachinePlatform",
    "/all",
    "/norestart"
) @(0, 3010)

Invoke-LoggedCommand dism.exe @(
    "/online",
    "/Get-FeatureInfo",
    "/FeatureName:Microsoft-Windows-Subsystem-Linux"
)

Invoke-LoggedCommand dism.exe @(
    "/online",
    "/Get-FeatureInfo",
    "/FeatureName:VirtualMachinePlatform"
)

"`nCompleted WSL feature completion at $(Get-Date -Format o)" | Add-Content -Path $logPath
