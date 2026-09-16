# Instala e inicia o serviço "GestaoSaudeApp" via NSSM.
# Execute em um PowerShell como Administrador.

$ErrorActionPreference = "Stop"

$nssm       = "C:\nssm\nssm.exe"
$python     = "C:\apps\gestao_saude\venv\Scripts\python.exe"
$appDir     = "C:\apps\gestao_saude"
$serviceName = "GestaoSaudeApp"

if (-not (Test-Path $nssm)) { throw "NSSM não encontrado em $nssm" }
if (-not (Test-Path $python)) { throw "Python do venv não encontrado em $python" }

$envVars = @(
    "DATABASE_URL",
    "SECRET_KEY",
    "SESSION_COOKIE_SECURE",
    "EMAIL_USER",
    "EMAIL_PASSWORD",
    "EMAIL_SMTP_SERVER",
    "EMAIL_SMTP_PORT",
    "APP_HOST",
    "APP_PORT",
    "APP_THREADS",
    "SEED_ON_EMPTY"
)

$extra = @()
foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var, "Machine")
    if ($value -ne $null) { $extra += "$var=$value" }
}

& $nssm install $serviceName $python "serve.py"
& $nssm set $serviceName AppDirectory $appDir
& $nssm set $serviceName AppEnvironmentExtra $extra
& $nssm set $serviceName AppStdout "$appDir\logs\app.stdout.log"
& $nssm set $serviceName AppStderr "$appDir\logs\app.stderr.log"
& $nssm set $serviceName Start SERVICE_AUTO_START
& $nssm set $serviceName AppExit Default Restart
& $nssm start $serviceName

Write-Host "Serviço '$serviceName' instalado e iniciado."
