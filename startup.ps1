param(
  [string]$Config = "config/phase4_config.yaml",
  [string]$DeployConfig = "config/config.yaml",
  [ValidateSet("dashboard", "desktop", "repl", "cli", "voice")]
  [string]$Mode = "dashboard"
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
  python -m venv venv
}

& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\venv\Scripts\python.exe" .\startup.py --config $Config --deploy-config $DeployConfig --mode $Mode
