[CmdletBinding()]
param(
    [string]$ShortcutName = "Nagatha AI Control Center",
    [string]$DestinationDirectory = [Environment]::GetFolderPath("Desktop")
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$startScript = Join-Path $projectRoot "start.ps1"

if (-not (Test-Path -LiteralPath $startScript)) {
    throw "start.ps1 was not found at $startScript"
}

if (-not (Test-Path -LiteralPath $DestinationDirectory)) {
    New-Item -ItemType Directory -Path $DestinationDirectory -Force | Out-Null
}

$shortcutPath = Join-Path $DestinationDirectory ($ShortcutName + ".lnk")
$workingDirectory = $projectRoot
$iconPath = "$env:SystemRoot\System32\SHELL32.dll,220"
$targetPath = (Get-Command powershell.exe -ErrorAction Stop).Source
$arguments = "-NoExit -ExecutionPolicy Bypass -File `"$startScript`" -Action all"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDirectory
$shortcut.IconLocation = $iconPath
$shortcut.Description = "Launch Nagatha AI Control Center"
$shortcut.Save()

Write-Host "Created shortcut: $shortcutPath"