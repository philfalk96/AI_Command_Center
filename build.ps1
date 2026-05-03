param(
  [string]$PackageRoot = "embodied-ai-package"
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$projectRoot = (Get-Location).Path

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
  python -m venv venv
}

& ".\venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller

if (Test-Path (".\build\" + $PackageRoot)) { Remove-Item (".\build\" + $PackageRoot) -Recurse -Force }
if (Test-Path (".\dist\" + $PackageRoot)) { Remove-Item (".\dist\" + $PackageRoot) -Recurse -Force }

$addData = @(
  ((Join-Path $projectRoot "config") + ";config"),
  ((Join-Path $projectRoot "avatar") + ";avatar"),
  ((Join-Path $projectRoot "backgrounds") + ";backgrounds"),
  ((Join-Path $projectRoot "ui\dashboard.html") + ";ui"),
  ((Join-Path $projectRoot "config\config.yaml") + ";config")
)

function Invoke-AppBuild {
  param(
    [string]$Name,
    [string]$EntryPoint,
    [switch]$Windowed,
    [string[]]$HiddenImports = @(),
    [string[]]$CollectAll = @(),
    [string[]]$ExcludeModules = @()
  )

  $workPath = Join-Path $PSScriptRoot ("build\" + $PackageRoot + "\" + $Name)
  $args = @(
    "--noconfirm",
    "--onedir",
    "--name", $Name,
    "--distpath", (Join-Path $PSScriptRoot ("dist\" + $PackageRoot)),
    "--workpath", $workPath,
    "--specpath", $workPath,
    "--hidden-import", "uvicorn",
    "--hidden-import", "fastapi",
    "--hidden-import", "edge_tts",
    "--hidden-import", "whisper",
    "--hidden-import", "pyttsx3",
    "--exclude-module", "tensorflow",
    "--exclude-module", "tensorboard",
    "--exclude-module", "jax",
    "--exclude-module", "jaxlib",
    "--exclude-module", "transformers.cli.serving"
  )

  foreach ($entry in $addData) {
    $args += @("--add-data", $entry)
  }
  foreach ($package in $CollectAll) {
    $args += @("--collect-all", $package)
  }
  foreach ($hidden in $HiddenImports) {
    $args += @("--hidden-import", $hidden)
  }
  foreach ($module in $ExcludeModules) {
    $args += @("--exclude-module", $module)
  }
  if ($Windowed) {
    $args += "--windowed"
  }
  $args += $EntryPoint
  & ".\venv\Scripts\pyinstaller.exe" @args
  if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed for $Name with exit code $LASTEXITCODE"
  }
}

Invoke-AppBuild `
  -Name "embodied-ai-backend" `
  -EntryPoint "backend_entry.py" `
  -HiddenImports @("transformers")

Invoke-AppBuild `
  -Name "embodied-ai-desktop" `
  -EntryPoint "desktop_entry.py" `
  -Windowed `
  -HiddenImports @("transformers", "PyQt6", "PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets")

$packageDist = Join-Path $PSScriptRoot ("dist\" + $PackageRoot)
$desktopDist = Join-Path $packageDist "embodied-ai-desktop"
$backendDist = Join-Path $packageDist "embodied-ai-backend"
$desktopExe = Join-Path $desktopDist "embodied-ai-desktop.exe"
$backendExe = Join-Path $backendDist "embodied-ai-backend.exe"

if (-not (Test-Path $desktopExe)) {
  throw "Desktop build did not produce $desktopExe"
}
if (-not (Test-Path $backendExe)) {
  throw "Backend build did not produce $backendExe"
}

New-Item -ItemType Directory -Path (Join-Path $desktopDist "logs") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $desktopDist "data\chroma_db") -Force | Out-Null
Copy-Item .\startup.ps1 (Join-Path $desktopDist "startup.ps1") -Force
Copy-Item .\startup.py (Join-Path $desktopDist "startup.py") -Force
Copy-Item .\config\config.yaml (Join-Path $desktopDist "config.yaml") -Force
Copy-Item .\install-shortcut.ps1 (Join-Path $packageDist "install-shortcut.ps1") -Force

Write-Host "Build completed: $packageDist"
Write-Host "Desktop exe: $desktopExe"
Write-Host "Backend exe: $backendExe"
