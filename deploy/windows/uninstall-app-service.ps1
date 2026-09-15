# Para e remove o serviço "GestaoSaudeApp".
# Execute em um PowerShell como Administrador.

$nssm        = "C:\nssm\nssm.exe"
$serviceName = "GestaoSaudeApp"

if (-not (Test-Path $nssm)) { throw "NSSM não encontrado em $nssm" }

& $nssm stop $serviceName
& $nssm remove $serviceName confirm

Write-Host "Serviço '$serviceName' removido."
