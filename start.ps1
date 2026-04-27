[CmdletBinding()]
param(
    [ValidateSet("check", "init-env", "db-up", "db-status", "schema", "api", "frontend", "all")]
    [string]$Action = "check",

    [string]$EnvFile = ".env"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = $MyInvocation.MyCommand.Path
$envPath = Join-Path $projectRoot $EnvFile
$envExamplePath = Join-Path $projectRoot ".env.example"

function Import-DotEnv {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    foreach ($rawLine in Get-Content -LiteralPath $Path) {
        $line = $rawLine.Trim()

        if (-not $line -or $line.StartsWith("#")) {
            continue
        }

        $parts = $line -split "=", 2
        if ($parts.Count -ne 2) {
            continue
        }

        $name = $parts[0].Trim()
        $value = $parts[1].Trim()

        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }

    return $true
}

function Test-Command {
    param([string]$Name)

    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-PnpmCommandPath {
    $candidates = @()

    $pnpmCmd = Get-Command pnpm.cmd -ErrorAction SilentlyContinue
    if ($pnpmCmd) {
        $candidates += $pnpmCmd.Source
    }

    $pnpm = Get-Command pnpm -ErrorAction SilentlyContinue
    if ($pnpm) {
        $candidates += $pnpm.Source
    }

    if (Test-Command npm) {
        try {
            $prefix = (& npm config get prefix 2>$null | Select-Object -First 1).Trim()
            if ($prefix) {
                $candidates += (Join-Path $prefix "pnpm.cmd")
                $candidates += (Join-Path $prefix "pnpm.ps1")
            }
        }
        catch {
        }
    }

    if ($env:APPDATA) {
        $candidates += (Join-Path $env:APPDATA "npm\pnpm.cmd")
        $candidates += (Join-Path $env:APPDATA "npm\pnpm.ps1")
    }

    foreach ($candidate in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    return $null
}

function New-SecretValue {
    return ([guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N"))
}

function Get-DotEnvMap {
    param([string]$Path)

    $map = [ordered]@{}

    if (-not (Test-Path -LiteralPath $Path)) {
        return $map
    }

    foreach ($rawLine in Get-Content -LiteralPath $Path) {
        $line = $rawLine.Trim()

        if (-not $line -or $line.StartsWith("#")) {
            continue
        }

        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $map[$parts[0].Trim()] = $parts[1].Trim()
        }
    }

    return $map
}

function Set-DotEnvValue {
    param(
        [string[]]$Lines,
        [string]$Name,
        [string]$Value
    )

    $updated = $false
    $escapedName = [regex]::Escape($Name)

    for ($index = 0; $index -lt $Lines.Count; $index++) {
        if ($Lines[$index] -match "^\s*$escapedName=") {
            $Lines[$index] = "$Name=$Value"
            $updated = $true
            break
        }
    }

    if (-not $updated) {
        $Lines += "$Name=$Value"
    }

    return ,$Lines
}

function Resolve-ConfiguredValue {
    param(
        [hashtable]$Map,
        [string]$Name,
        [string]$Default,
        [string[]]$PlaceholderValues = @()
    )

    if ($Map.Contains($Name)) {
        $existing = $Map[$Name]
        if ($PlaceholderValues -notcontains $existing) {
            return $existing
        }
    }

    return $Default
}

function Ensure-EnvFile {
    if (-not (Test-Path -LiteralPath $envPath)) {
        if (-not (Test-Path -LiteralPath $envExamplePath)) {
            throw ".env.example is missing from $projectRoot"
        }

        Copy-Item -LiteralPath $envExamplePath -Destination $envPath
    }

    $current = Get-DotEnvMap -Path $envPath
    $pgHost = Resolve-ConfiguredValue -Map $current -Name "PGHOST" -Default "localhost"
    $pgPort = Resolve-ConfiguredValue -Map $current -Name "PGPORT" -Default "5432"
    $pgUser = Resolve-ConfiguredValue -Map $current -Name "PGUSER" -Default "postgres"
    $pgDatabase = Resolve-ConfiguredValue -Map $current -Name "PGDATABASE" -Default "nagatha_ai"
    $pgPassword = Resolve-ConfiguredValue -Map $current -Name "PGPASSWORD" -Default (New-SecretValue).Substring(0, 24) -PlaceholderValues @("password", "yourpassword", "YOUR_PASSWORD")
    $sessionSecret = Resolve-ConfiguredValue -Map $current -Name "SESSION_SECRET" -Default (New-SecretValue) -PlaceholderValues @("change-me-to-a-random-string-at-least-32-chars", "any-random-string-here")
    $apiPort = Resolve-ConfiguredValue -Map $current -Name "API_PORT" -Default "8080"
    $frontPort = Resolve-ConfiguredValue -Map $current -Name "FRONT_PORT" -Default "3000"
    $ollamaUrl = Resolve-ConfiguredValue -Map $current -Name "OLLAMA_URL" -Default "http://localhost:11434"
    $pgContainer = Resolve-ConfiguredValue -Map $current -Name "NAGATHA_PG_CONTAINER" -Default "nagatha-postgres"
    $pgVolume = Resolve-ConfiguredValue -Map $current -Name "NAGATHA_PG_VOLUME" -Default "nagatha-postgres-data"
    $databaseUrl = "postgresql://${pgUser}:${pgPassword}@${pgHost}:${pgPort}/${pgDatabase}"

    $lines = Get-Content -LiteralPath $envPath
    $updates = [ordered]@{
        "DATABASE_URL" = $databaseUrl
        "PGHOST" = $pgHost
        "PGPORT" = $pgPort
        "PGUSER" = $pgUser
        "PGPASSWORD" = $pgPassword
        "PGDATABASE" = $pgDatabase
        "OLLAMA_URL" = $ollamaUrl
        "SESSION_SECRET" = $sessionSecret
        "API_PORT" = $apiPort
        "FRONT_PORT" = $frontPort
        "NAGATHA_PG_CONTAINER" = $pgContainer
        "NAGATHA_PG_VOLUME" = $pgVolume
    }

    foreach ($entry in $updates.GetEnumerator()) {
        $lines = Set-DotEnvValue -Lines $lines -Name $entry.Key -Value $entry.Value
    }

    Set-Content -LiteralPath $envPath -Value $lines -Encoding utf8
    Import-DotEnv -Path $envPath | Out-Null

    return $envPath
}

function Invoke-Pnpm {
    param([string[]]$Arguments)

    $pnpmCommand = Get-PnpmCommandPath
    if (-not $pnpmCommand) {
        throw "pnpm was not found. Install pnpm globally or add the npm global bin directory to PATH."
    }

    & $pnpmCommand @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "pnpm command failed: $pnpmCommand $($Arguments -join ' ')"
    }
}

function Invoke-Docker {
    param([string[]]$Arguments)

    & docker @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "docker command failed: docker $($Arguments -join ' ')"
    }
}

function Get-DatabaseMode {
    if ((Test-Command psql) -and (Test-Command createdb) -and (Test-Command pg_isready)) {
        return "native"
    }

    if (Test-Command docker) {
        return "docker"
    }

    return "none"
}

function Ensure-DependenciesInstalled {
    $nodeModulesPath = Join-Path $projectRoot "node_modules"
    if (-not (Test-Path -LiteralPath $nodeModulesPath)) {
        Push-Location $projectRoot
        try {
            Invoke-Pnpm -Arguments @("install")
        }
        finally {
            Pop-Location
        }
    }
}

function Get-PostgresContainerName {
    return $(if ($env:NAGATHA_PG_CONTAINER) { $env:NAGATHA_PG_CONTAINER } else { "nagatha-postgres" })
}

function Get-PostgresVolumeName {
    return $(if ($env:NAGATHA_PG_VOLUME) { $env:NAGATHA_PG_VOLUME } else { "nagatha-postgres-data" })
}

function Wait-ForDockerPostgres {
    $container = Get-PostgresContainerName

    for ($attempt = 1; $attempt -le 30; $attempt++) {
        & docker exec $container pg_isready -U $env:PGUSER -d $env:PGDATABASE | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return
        }

        Start-Sleep -Seconds 2
    }

    throw "PostgreSQL container '$container' did not become ready in time."
}

function Ensure-DockerPostgres {
    if (-not (Test-Command docker)) {
        throw "Docker is required for the local PostgreSQL container but was not found."
    }

    & docker ps --format "{{.Names}}" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker CLI is installed, but the Docker daemon is not ready. Start Docker Desktop and try again."
    }

    $container = Get-PostgresContainerName
    $volume = Get-PostgresVolumeName
    $hostPort = if ($env:PGPORT) { $env:PGPORT } else { "5432" }
    $allContainers = & docker ps -a --filter "name=^/$container$" --format "{{.Names}}"
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect Docker containers."
    }

    if (-not $allContainers) {
        Invoke-Docker -Arguments @("volume", "create", $volume)
        Invoke-Docker -Arguments @(
            "run",
            "--name", $container,
            "--detach",
            "--restart", "unless-stopped",
            "-e", "POSTGRES_DB=$($env:PGDATABASE)",
            "-e", "POSTGRES_USER=$($env:PGUSER)",
            "-e", "POSTGRES_PASSWORD=$($env:PGPASSWORD)",
            "-p", "${hostPort}:5432",
            "-v", "${volume}:/var/lib/postgresql/data",
            "postgres:16"
        )
    }
    else {
        $runningContainers = & docker ps --filter "name=^/$container$" --format "{{.Names}}"
        if (-not $runningContainers) {
            Invoke-Docker -Arguments @("start", $container)
        }
    }

    Wait-ForDockerPostgres
}

function Ensure-NativePostgres {
    if (-not ((Test-Command psql) -and (Test-Command createdb) -and (Test-Command pg_isready))) {
        throw "Native PostgreSQL tooling is incomplete. Install PostgreSQL locally or use Docker."
    }

    & pg_isready -h $env:PGHOST -p $env:PGPORT -U $env:PGUSER -d postgres | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "PostgreSQL is installed but not reachable at $($env:PGHOST):$($env:PGPORT)."
    }

    $dbExists = & psql -h $env:PGHOST -p $env:PGPORT -U $env:PGUSER -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$($env:PGDATABASE)'"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to query PostgreSQL for database '$($env:PGDATABASE)'."
    }

    if (-not ($dbExists | Where-Object { $_.Trim() -eq "1" })) {
        & createdb -h $env:PGHOST -p $env:PGPORT -U $env:PGUSER $env:PGDATABASE
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create PostgreSQL database '$($env:PGDATABASE)'."
        }
    }
}

function Ensure-DatabaseReady {
    $mode = Get-DatabaseMode

    switch ($mode) {
        "native" {
            Ensure-NativePostgres
            return "native"
        }
        "docker" {
            Ensure-DockerPostgres
            return "docker"
        }
        default {
            throw "No PostgreSQL runtime is available. Install PostgreSQL locally or start Docker Desktop."
        }
    }
}

function Test-DatabaseReady {
    $mode = Get-DatabaseMode

    switch ($mode) {
        "native" {
            try {
                & pg_isready -h $env:PGHOST -p $env:PGPORT -U $env:PGUSER -d $env:PGDATABASE 2>$null | Out-Null
                return ($LASTEXITCODE -eq 0)
            }
            catch {
                return $false
            }
        }
        "docker" {
            $container = Get-PostgresContainerName
            try {
                & docker exec $container pg_isready -U $env:PGUSER -d $env:PGDATABASE 2>$null | Out-Null
                return ($LASTEXITCODE -eq 0)
            }
            catch {
                return $false
            }
        }
        default {
            return $false
        }
    }
}

function Start-NagathaProcess {
    param([string]$TargetAction)

    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", $scriptPath,
        "-Action", $TargetAction,
        "-EnvFile", $EnvFile
    ) | Out-Null
}

$loadedEnv = Import-DotEnv -Path $envPath

if (-not $env:API_PORT) {
    $env:API_PORT = "8080"
}

if (-not $env:FRONT_PORT) {
    $env:FRONT_PORT = "3000"
}

switch ($Action) {
    "check" {
        $pnpmCommand = Get-PnpmCommandPath
        Write-Host "Project root: $projectRoot"
        Write-Host ".env file: $(if ($loadedEnv) { $envPath } else { 'missing' })"
        Write-Host "node: $(if (Test-Command node) { 'ok' } else { 'missing' })"
        Write-Host "pnpm: $(if ($pnpmCommand) { $pnpmCommand } else { 'missing' })"
        Write-Host "ollama: $(if (Test-Command ollama) { 'ok' } else { 'missing' })"
        Write-Host "docker: $(if (Test-Command docker) { 'ok' } else { 'missing' })"
        Write-Host "database mode: $(Get-DatabaseMode)"
        Write-Host "DATABASE_URL: $(if ($env:DATABASE_URL) { 'set' } else { 'missing' })"
        Write-Host "database ready: $(if ($loadedEnv -and (Test-DatabaseReady)) { 'yes' } else { 'no' })"
        Write-Host "API port: $($env:API_PORT)"
        Write-Host "Frontend port: $($env:FRONT_PORT)"
        break
    }

    "init-env" {
        $createdPath = Ensure-EnvFile
        Write-Host "Local environment ready: $createdPath"
        break
    }

    "db-up" {
        Ensure-EnvFile | Out-Null
        $mode = Ensure-DatabaseReady
        Write-Host "PostgreSQL ready using: $mode"
        break
    }

    "db-status" {
        Ensure-EnvFile | Out-Null
        Write-Host "Database mode: $(Get-DatabaseMode)"
        Write-Host "Database ready: $(if (Test-DatabaseReady) { 'yes' } else { 'no' })"
        break
    }

    "schema" {
        Ensure-EnvFile | Out-Null
        Ensure-DatabaseReady | Out-Null

        Push-Location $projectRoot
        try {
            Invoke-Pnpm -Arguments @("--filter", "@workspace/db", "run", "push")
        }
        finally {
            Pop-Location
        }
        break
    }

    "api" {
        Ensure-EnvFile | Out-Null
        if (-not $env:DATABASE_URL) {
            throw "DATABASE_URL is required. Run '.\\start.ps1 -Action init-env' first."
        }

        $env:PORT = $env:API_PORT
        $env:NODE_ENV = "development"

        Push-Location $projectRoot
        try {
            Invoke-Pnpm -Arguments @("--filter", "@workspace/api-server", "run", "dev")
        }
        finally {
            Pop-Location
        }
        break
    }

    "frontend" {
        Ensure-EnvFile | Out-Null
        $env:PORT = $env:FRONT_PORT
        $env:BASE_PATH = "/"
        $env:NODE_ENV = "development"

        Push-Location $projectRoot
        try {
            Invoke-Pnpm -Arguments @("--filter", "@workspace/nagatha-ai", "run", "dev")
        }
        finally {
            Pop-Location
        }
        break
    }

    "all" {
        Ensure-EnvFile | Out-Null
        Ensure-DependenciesInstalled
        Ensure-DatabaseReady | Out-Null

        Push-Location $projectRoot
        try {
            Invoke-Pnpm -Arguments @("--filter", "@workspace/db", "run", "push")
        }
        finally {
            Pop-Location
        }

        Start-NagathaProcess -TargetAction "api"
        Start-NagathaProcess -TargetAction "frontend"
        Start-Process "http://localhost:$($env:FRONT_PORT)" | Out-Null

        Write-Host "Nagatha AI Control launched."
        Write-Host "Frontend: http://localhost:$($env:FRONT_PORT)"
        Write-Host "API: http://localhost:$($env:API_PORT)/api/healthz"
        break
    }
}