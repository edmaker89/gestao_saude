# Deploy no Windows Server

Guia para rodar a aplicação como serviço no Windows, atrás do nginx como proxy reverso (TLS).

## Arquitetura

```
LAN/Internet -> nginx (serviço Windows, :80/:443, TLS)
             -> 127.0.0.1:5000 (não exposto externamente)
             -> Waitress (serviço Windows "GestaoSaudeApp")
             -> MariaDB (serviço local, :3306)
```

## Pré-requisitos

- Windows Server (2016+).
- [Python 3.14](https://www.python.org/downloads/).
- [MariaDB](https://mariadb.org/download/) instalado como serviço local.
- [NSSM](https://nssm.cc/download) (extrair para `C:\nssm`).
- [nginx para Windows](https://nginx.org/en/download.html) (extrair para `C:\nginx`).

## Passo a passo

### 1. Código e dependências

```powershell
mkdir C:\apps\gestao_saude
# copie o repositório para C:\apps\gestao_saude
cd C:\apps\gestao_saude
python -m venv venv
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\python -m pip install -r requirements.txt
```

### 2. Banco de dados

1. Instale o MariaDB como serviço e crie o banco/usuário:
   ```sql
   CREATE DATABASE gestao_saude_db;
   CREATE USER 'gestao_saude_user'@'localhost' IDENTIFIED BY 'SENHA_FORTE';
   GRANT ALL PRIVILEGES ON gestao_saude_db.* TO 'gestao_saude_user'@'localhost';
   ```
2. O schema é criado automaticamente pelo bootstrap (`db.create_all()`) caso o banco
   esteja vazio. Para manter um schema já existente, restaure o dump do Linux
   **sem** os dados (só estrutura); o bootstrap insere os dados mínimos.

### 3. Variáveis de ambiente

1. Edite `set-env.ps1` com os valores reais.
2. Rode em um PowerShell **Administrador**:
   ```powershell
   .\deploy\windows\set-env.ps1
   ```

### 4. Serviço da aplicação

```powershell
# criar o diretório de logs
mkdir C:\apps\gestao_saude\logs

# instalar e iniciar o serviço (PowerShell Administrador)
.\deploy\windows\install-app-service.ps1
```

Para remover: `.\deploy\windows\uninstall-app-service.ps1`.

### 5. nginx (proxy reverso + TLS)

1. Copie `deploy\windows\nginx.conf` para `C:\nginx\conf\nginx.conf`.
2. Coloque o certificado e a chave em `C:\nginx\ssl\cert.pem` e
   `C:\nginx\ssl\privkey.pem` (obtidos no servidor, nunca no repositório).
3. Instale como serviço:
   ```powershell
   .\deploy\windows\install-nginx-service.ps1
   ```

### 6. Firewall

Abrir apenas `80` e `443`. A aplicação roda em loopback (`127.0.0.1:5000`) e não deve
ser exposta.

## Credenciais iniciais (seed)

O bootstrap cria um usuário administrador fictício quando o banco está vazio:

- Usuário: `admin`
- E-mail: `admin@example.com`
- Senha: `Mudar@123`

**Troque a senha no primeiro acesso.**

## Variáveis de ambiente

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `DATABASE_URL` | sim | — | URL do MySQL/MariaDB |
| `SECRET_KEY` | sim | — | Chave secreta do Flask |
| `SESSION_COOKIE_SECURE` | não | `true` | Cookie seguro (desligar só p/ teste HTTP) |
| `EMAIL_USER`/`EMAIL_PASSWORD`/`EMAIL_SMTP_SERVER`/`EMAIL_SMTP_PORT` | não | — | Configuração SMTP |
| `APP_HOST`/`APP_PORT`/`APP_THREADS` | não | `127.0.0.1`/`5000`/`8` | Configuração do Waitress |
| `SEED_ON_EMPTY` | não | `true` | Habilita bootstrap de dados mínimos |
