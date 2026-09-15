# Configura as variáveis de ambiente da aplicação em nível de máquina.
# Execute em um PowerShell como Administrador.

$vars = @{
    DATABASE_URL           = "mysql+pymysql://gestao_saude_user:SENHA_FORTE@127.0.0.1:3306/gestao_saude_db"
    SECRET_KEY             = "CHANGE_ME"
    SESSION_COOKIE_SECURE  = "true"
    EMAIL_USER             = ""
    EMAIL_PASSWORD         = ""
    EMAIL_SMTP_SERVER      = "smtp.gmail.com"
    EMAIL_SMTP_PORT        = "587"
    APP_HOST               = "127.0.0.1"
    APP_PORT               = "5000"
    APP_THREADS            = "8"
    SEED_ON_EMPTY          = "true"
}

foreach ($key in $vars.Keys) {
    [Environment]::SetEnvironmentVariable($key, $vars[$key], "Machine")
}

Write-Host "Variáveis de ambiente configuradas em nível de máquina."
