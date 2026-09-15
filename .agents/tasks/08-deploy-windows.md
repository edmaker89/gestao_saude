# Task 8 — Artefatos de deploy Windows (NSSM + nginx)

## Objetivo
Versionar tudo o que é necessário para rodar a app como serviço no Windows Server, atrás de um nginx como proxy reverso (TLS no nginx).

## Arquivos a criar em `deploy/windows/`
1. `README.md` — runbook completo:
   - Instalar Python 3.14 + venv + `pip install -r requirements.txt`.
   - Instalar MariaDB como serviço local; criar banco/usuário.
   - Rodar `set-env.ps1` com os valores reais.
   - Instalar serviços via NSSM.
   - Firewall: abrir apenas `80/443`.
   - Credenciais iniciais do seed: `admin` / `admin@example.com` / `Mudar@123` (trocar no 1º acesso).
2. `set-env.ps1` — grava as variáveis em nível Machine (`[Environment]::SetEnvironmentVariable(...,'Machine')`): `DATABASE_URL`, `SECRET_KEY`, `SESSION_COOKIE_SECURE`, `EMAIL_*`, `APP_*`, `SEED_ON_EMPTY`.
3. `install-app-service.ps1` — instala serviço `GestaoSaudeApp` via NSSM apontando para o `python.exe` do venv executando `serve.py`, com `AppDirectory`, `AppEnvironmentExtra` e `Recovery=restart`.
4. `uninstall-app-service.ps1` — remove o serviço.
5. `nginx.conf` — proxy reverso:
   - `listen 80` e `listen 443 ssl`; `proxy_pass http://127.0.0.1:5000;`
   - Headers `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`.
   - Config de TLS (certificado obtido no servidor, nunca no repo).
6. `install-nginx-service.ps1` — registra o `nginx.exe` como serviço via NSSM.

## Observações
- NSSM é pré-requisito no servidor (documentar no README).
- nginx no Windows não se registra sozinho como serviço — por isso o NSSM.

## Critérios de aceite
- `deploy/windows/` contém os 6 arquivos.
- README permite reproduzir o deploy do zero.

## Commit sugerido
`adicionar artefatos de deploy para windows (nssm + nginx)`
