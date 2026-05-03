[CmdletBinding()]
param(
    [string]$ShortcutName = "Embodied AI Desktop",
    [string]$DestinationDirectory = [Environment]::GetFolderPath("Desktop"),
    [string]$PackageRoot = "",
    [switch]$UseSourceTree
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$iconPath = Join-Path $projectRoot "ui\desktop\assets\embodied_ai.ico"

if ($UseSourceTree) {
    $targetPath = Join-Path $projectRoot "venv\Scripts\pythonw.exe"
    if (-not (Test-Path -LiteralPath $targetPath)) {
        $targetPath = Join-Path $projectRoot "venv\Scripts\python.exe"
    }
    $arguments = "`"$projectRoot\desktop_entry.py`""
    $workingDirectory = $projectRoot
}
else {
    if ([string]::IsNullOrWhiteSpace($PackageRoot)) {
        $PackageRoot = Join-Path $projectRoot "dist\embodied-ai-package"
    }
    $targetPath = Join-Path $PackageRoot "embodied-ai-desktop\embodied-ai-desktop.exe"
    if (-not (Test-Path -LiteralPath $targetPath)) {
        throw "Desktop executable not found at $targetPath"
    }
    $arguments = ""
    $workingDirectory = Split-Path -Parent $targetPath
}

if (-not (Test-Path -LiteralPath $DestinationDirectory)) {
    New-Item -ItemType Directory -Path $DestinationDirectory -Force | Out-Null
}

$shortcutPath = Join-Path $DestinationDirectory ($ShortcutName + ".lnk")
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDirectory
if (Test-Path -LiteralPath $iconPath) {
    $shortcut.IconLocation = $iconPath
}
else {
    $shortcut.IconLocation = "$targetPath,0"
}
$shortcut.Description = "Launch Embodied AI Desktop with hidden backend + Ollama startup"
$shortcut.Save()

Write-Host "Created shortcut: $shortcutPath"