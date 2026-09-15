# Instala e inicia o nginx como serviço Windows via NSSM.
# Execute em um PowerShell como Administrador.

$ErrorActionPreference = "Stop"

$nssm        = "C:\nssm\nssm.exe"
$nginxExe    = "C:\nginx\nginx.exe"
$nginxDir    = "C:\nginx"

if (-not (Test-Path $nssm)) { throw "NSSM não encontrado em $nssm" }
if (-not (Test-Path $nginxExe)) { throw "nginx.exe não encontrado em $nginxExe" }

& $nssm install nginx $nginxExe
& $nssm set nginx AppDirectory $nginxDir
& $nssm set nginx AppStdout "$nginxDir\logs\nginx.stdout.log"
& $nssm set nginx AppStderr "$nginxDir\logs\nginx.stderr.log"
& $nssm set nginx Start SERVICE_AUTO_START
& $nssm set nginx AppExit Default Restart
& $nssm start nginx

Write-Host "Serviço 'nginx' instalado e iniciado."
